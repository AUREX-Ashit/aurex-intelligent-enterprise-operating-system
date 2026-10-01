"""
TD-171 remediation tranche (WP-23 Charter §21a), slice 3: environment
reconciliation and the OD-5 deployment-level block
(`services/bar_reconciliation.py`, `scripts/bar_reconcile.py`).

The classifier is exercised with in-memory row snapshots for every one of
the seven OD-5 states, and end to end against a SQLite store written only
through the governed operation (slice 2). SQLite results are NOT
PostgreSQL evidence and NOT evidence of a read-only principal (EP-03);
see `tests/test_bar_postgres.py`.
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from pathlib import Path

import pytest
from sqlalchemy import event, select
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

import models  # noqa: F401  (registers every table on Base.metadata)
from models.bar_registration import BarRegistration
from models.database import Base
from scripts import bar_reconcile
from services.bar_governance_evidence import load_governance_evidence
from services.bar_governed_registration import (
    DeploymentWriteCapability,
    GovernedBarRegistrationOperation,
    GovernedRegistrationRequest,
)
from services.bar_reconciliation import (
    EXIT_INTEGRITY_FAILURE,
    EXIT_RECONCILIATION_FAILURE,
    EXIT_VALID,
    ReconciliationState,
    reconcile,
    reconcile_environment,
)
from tests.bar_governance_fixtures import (
    GovernanceRepository,
    authorization_text,
    index_row,
    snapshot,
)

S = ReconciliationState
RUNTIME_URL = "postgresql+asyncpg://runtime-user@runtime-host:5432/authservice"


@pytest.fixture
def repo(tmp_path: Path) -> GovernanceRepository:
    repository = GovernanceRepository(tmp_path / "checkout")
    repository.write_index()
    return repository


def _states(rows, repo: GovernanceRepository):
    report = reconcile(rows, load_governance_evidence(repo.root))
    return report, sorted((r.state for r in report.results), key=lambda s: s.value)


# ---------------------------------------------------- the seven OD-5 states


def test_valid_registered_row(repo):
    repo.write_index(repo.governed("ADR-9301", "BA-01 (GOV TEST)", "BA-000001"))
    report, states = _states([snapshot("BA-000001", "BA-01 (GOV TEST)", "ADR-9301")], repo)
    assert states == [S.VALID_REGISTERED_ROW]
    assert not report.blocking and report.exit_code == EXIT_VALID


def test_valid_retroactive_registered_row(repo):
    repo.write_index(repo.governed("ADR-9302", "BA-01 (GOV TEST)", "BA-000001", retroactive=True))
    _, states = _states([snapshot("BA-000001", "BA-01 (GOV TEST)", "ADR-9302", retroactive=True)], repo)
    assert states == [S.VALID_REGISTERED_ROW]


def test_missing_governing_act_when_addendum_not_committed(repo):
    """TDS §11 S: authorization committed, addendum not yet committed."""
    repo.write_act("ADR-9303", authorization_text("ADR-9303", "BA-01 (GOV TEST)"))
    report, states = _states([snapshot("BA-000001", "BA-01 (GOV TEST)", "ADR-9303")], repo)
    assert states == [S.MISSING_GOVERNING_ACT]
    assert "no committed execution addendum" in report.results[0].detail
    assert report.exit_code == EXIT_INTEGRITY_FAILURE


def test_missing_governing_act_when_index_cites_an_absent_act(repo):
    repo.write_index(index_row("BA-000001", "BA-01 (GOV TEST)", "ADR-9304"))
    _, states = _states([snapshot("BA-000001", "BA-01 (GOV TEST)", "ADR-9304")], repo)
    assert states == [S.MISSING_GOVERNING_ACT]


def test_malformed_governing_act(repo):
    repo.write_act("ADR-9305", authorization_text("ADR-9305", "BA-01 (GOV TEST)", owning_capability="capability nine"))
    _, states = _states([snapshot("BA-000001", "BA-01 (GOV TEST)", "ADR-9305")], repo)
    assert states == [S.MALFORMED_GOVERNING_ACT]


def test_malformed_act_with_no_row_still_blocks(repo):
    repo.write_act("ADR-9306", authorization_text("ADR-9306", "BA-01 (GOV TEST)", act_type="SOMETHING-ELSE"))
    report, states = _states([], repo)
    assert states == [S.MALFORMED_GOVERNING_ACT] and report.blocking


@pytest.mark.parametrize(
    "row",
    [
        snapshot("BA-000001", "BA-01 (GOV TEST)", "ADR-9307", capability="C-998"),
        snapshot("BA-000001", "BA-01 (GOV TEST)", "ADR-9307", work_package="WP-TEST-OTHER"),
        snapshot("BA-000001", "BA-01 (GOV TEST)", "ADR-9307", retroactive=True),
        snapshot("BA-000001", "BA-01 (GOV TEST)", "ADR-9307", registered_at=datetime(2026, 9, 30, 23, 0, tzinfo=timezone.utc)),
        snapshot("BA-000001", "BA-01 (GOV TEST)", "ADR-9307", status="SUSPENDED"),
        snapshot("BA-000002", "BA-01 (GOV TEST)", "ADR-9307"),
    ],
)
def test_mismatched_governing_act_between_row_and_act(repo, row):
    repo.write_index(repo.governed("ADR-9307", "BA-01 (GOV TEST)", "BA-000001"))
    report, states = _states([row], repo)
    assert S.MISMATCHED_GOVERNING_ACT in states
    assert S.VALID_REGISTERED_ROW not in states
    assert report.blocking


def test_mismatched_governing_act_when_index_row_is_missing(repo):
    repo.governed("ADR-9308", "BA-01 (GOV TEST)", "BA-000001")
    report, states = _states([snapshot("BA-000001", "BA-01 (GOV TEST)", "ADR-9308")], repo)
    assert states == [S.MISMATCHED_GOVERNING_ACT]
    assert "no BAR-INDEX.md §3 row" in report.results[0].detail


def test_mismatched_governing_act_when_index_disagrees_with_row(repo):
    repo.governed("ADR-9309", "BA-01 (GOV TEST)", "BA-000001")
    repo.write_index(index_row("BA-000001", "BA-01 (GOV TEST)", "ADR-9309", registered_on="2026-09-30"))
    _, states = _states([snapshot("BA-000001", "BA-01 (GOV TEST)", "ADR-9309")], repo)
    assert states == [S.MISMATCHED_GOVERNING_ACT]


def test_index_only_and_addendum_only_evidence_is_mismatched(repo):
    repo.write_index(repo.governed("ADR-9310", "BA-01 (GOV TEST)", "BA-000001"))
    report, states = _states([], repo)
    assert states == [S.MISMATCHED_GOVERNING_ACT, S.MISMATCHED_GOVERNING_ACT]
    assert report.blocking


def test_duplicate_conflicting_evidence_two_acts_for_one_identifier(repo):
    repo.write_index(repo.governed("ADR-9311", "BA-01 (GOV TEST)", "BA-000001"))
    repo.governed("ADR-9312", "BA-02 (GOV TEST)", "BA-000001")
    report, states = _states([snapshot("BA-000001", "BA-01 (GOV TEST)", "ADR-9311")], repo)
    row_result = next(r for r in report.results if r.subject == "bar_registration BA-000001")
    assert row_result.state is S.DUPLICATE_CONFLICTING_EVIDENCE


def test_duplicate_conflicting_evidence_two_index_rows(repo):
    row = repo.governed("ADR-9313", "BA-01 (GOV TEST)", "BA-000001")
    repo.write_index(row, row)
    _, states = _states([snapshot("BA-000001", "BA-01 (GOV TEST)", "ADR-9313")], repo)
    assert states == [S.DUPLICATE_CONFLICTING_EVIDENCE]


def test_ungoverned_row(repo):
    report, states = _states([snapshot("BA-000001", "BA-01 (GOV TEST)", "free text citation")], repo)
    assert states == [S.UNGOVERNED_ROW]
    assert report.exit_code == EXIT_INTEGRITY_FAILURE


def test_reconciliation_failure_on_unreadable_evidence(tmp_path):
    async def run():
        engine = create_async_engine(f"sqlite+aiosqlite:///{(tmp_path / 'r.db').as_posix()}")
        try:
            async with async_sessionmaker(engine, class_=AsyncSession)() as session:
                return await reconcile_environment(session, tmp_path / "no-checkout")
        finally:
            await engine.dispose()

    report = asyncio.run(run())
    assert [r.state for r in report.results] == [S.RECONCILIATION_FAILURE]
    assert report.exit_code == EXIT_RECONCILIATION_FAILURE


async def test_reconciliation_failure_on_unreadable_store(repo, tmp_path):
    engine = create_async_engine(f"sqlite+aiosqlite:///{(tmp_path / 'no_tables.db').as_posix()}")
    try:
        async with async_sessionmaker(engine, class_=AsyncSession)() as session:
            report = await reconcile_environment(session, repo.root)
    finally:
        await engine.dispose()
    assert [r.state for r in report.results] == [S.RECONCILIATION_FAILURE]
    assert "registration store unreadable" in report.results[0].detail
    assert report.exit_code == EXIT_RECONCILIATION_FAILURE


def test_one_bad_row_blocks_even_when_others_are_valid(repo):
    repo.write_index(repo.governed("ADR-9314", "BA-01 (GOV TEST)", "BA-000001"))
    report, states = _states(
        [snapshot("BA-000001", "BA-01 (GOV TEST)", "ADR-9314"), snapshot("BA-000002", "BA-02 (GOV TEST)", "unknown")], repo
    )
    assert states == [S.UNGOVERNED_ROW, S.VALID_REGISTERED_ROW]
    assert report.blocking and report.exit_code == EXIT_INTEGRITY_FAILURE


def test_empty_environment_and_empty_evidence_is_not_blocked(repo):
    report, states = _states([], repo)
    assert states == [] and report.exit_code == EXIT_VALID


# ------------------------------------- end to end against a SQLite store


@pytest.fixture
def transactional_sqlite():
    """Same recipe as `test_bar_governed_registration.py` (explicit BEGIN, foreign keys on)."""

    def on_connect(dbapi_connection, _record):
        dbapi_connection.isolation_level = None
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    def on_begin(conn):
        conn.exec_driver_sql("BEGIN")

    event.listen(Engine, "connect", on_connect)
    event.listen(Engine, "begin", on_begin)
    yield
    event.remove(Engine, "connect", on_connect)
    event.remove(Engine, "begin", on_begin)


@pytest.fixture
async def store(tmp_path, transactional_sqlite):
    url = f"sqlite+aiosqlite:///{(tmp_path / 'bar_env.db').as_posix()}"
    engine = create_async_engine(url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield url, engine
    await engine.dispose()


async def _reconcile(engine, repo: GovernanceRepository):
    async with async_sessionmaker(engine, class_=AsyncSession)() as session:
        return await reconcile_environment(session, repo.root)


async def test_governed_lifecycle_moves_from_missing_act_to_valid(store, repo):
    url, engine = store
    operation = GovernedBarRegistrationOperation(DeploymentWriteCapability.validate(url, runtime_database_url=RUNTIME_URL))
    act_path = repo.write_act("ADR-9315", authorization_text("ADR-9315", "BA-01 (GOV TEST)"))

    executed = await operation.execute(
        act_path,
        GovernedRegistrationRequest("BA-01 (GOV TEST)", "C-999", "WP-TEST-GOV", is_retroactive=False),
    )
    report = await _reconcile(engine, repo)
    assert [r.state for r in report.results] == [S.MISSING_GOVERNING_ACT]  # §11 S: blocks
    assert report.exit_code == EXIT_INTEGRITY_FAILURE

    act_path.write_text(act_path.read_text(encoding="utf-8") + "\n" + executed.execution_addendum, encoding="utf-8")
    report = await _reconcile(engine, repo)
    assert [r.state for r in report.results] == [S.MISMATCHED_GOVERNING_ACT]  # not yet indexed

    repo.write_index(
        index_row(
            executed.bar_business_activity_identifier, "BA-01 (GOV TEST)", "ADR-9315",
            registered_on=executed.executed_on.isoformat(),
        )
    )
    report = await _reconcile(engine, repo)
    assert [r.state for r in report.results] == [S.VALID_REGISTERED_ROW]
    assert report.exit_code == EXIT_VALID
    await operation.confirm(act_path)


async def test_reconciliation_issues_only_selects_and_preserves_rows(store, repo):
    url, engine = store
    operation = GovernedBarRegistrationOperation(DeploymentWriteCapability.validate(url, runtime_database_url=RUNTIME_URL))
    await operation.execute(
        repo.write_act("ADR-9316", authorization_text("ADR-9316", "BA-01 (GOV TEST)")),
        GovernedRegistrationRequest("BA-01 (GOV TEST)", "C-999", "WP-TEST-GOV", is_retroactive=False),
    )

    async def rows():
        async with async_sessionmaker(engine, class_=AsyncSession)() as session:
            return [
                (r.id, r.identifier, r.registering_act, r.registered_at, r.registration_status)
                for r in (await session.execute(select(BarRegistration))).scalars()
            ]

    before = await rows()
    statements: list[str] = []

    def capture(_conn, _cursor, statement, *_args):
        statements.append(statement.strip().split()[0].upper())

    event.listen(engine.sync_engine, "before_cursor_execute", capture)
    try:
        report = await _reconcile(engine, repo)
    finally:
        event.remove(engine.sync_engine, "before_cursor_execute", capture)
    assert report.results[0].state is S.MISSING_GOVERNING_ACT  # an ungoverned-for-now row is blocked, not adopted
    assert "SELECT" in statements
    assert set(statements) <= {"SELECT", "BEGIN"}  # BEGIN is this harness's own transaction recipe
    assert not {"INSERT", "UPDATE", "DELETE", "REPLACE"} & set(statements)
    assert await rows() == before


# ------------------------------------------------------- deployment step


def test_deployment_step_fails_closed_without_a_database_url(repo, capsys):
    assert bar_reconcile.main(["--repository-root", str(repo.root)], environ={}) == EXIT_RECONCILIATION_FAILURE
    assert "reconciliation failure" in capsys.readouterr().out


def test_deployment_step_fails_closed_on_an_invalid_database_url(repo):
    environ = {bar_reconcile.RECONCILIATION_URL_ENV: "not a url"}
    assert bar_reconcile.main(["--repository-root", str(repo.root)], environ=environ) == EXIT_RECONCILIATION_FAILURE


def test_deployment_step_blocks_an_ungoverned_row(repo, tmp_path, transactional_sqlite, capsys):
    url = f"sqlite+aiosqlite:///{(tmp_path / 'step.db').as_posix()}"

    async def seed():
        from models.bar_identifier_ledger import BarIdentifierLedger

        engine = create_async_engine(url)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        async with async_sessionmaker(engine, class_=AsyncSession)() as session:
            # A row written outside the governed operation (the condition TD-171 guards against).
            session.add(BarIdentifierLedger(identifier="BA-000001"))
            session.add(
                BarRegistration(
                    identifier="BA-000001", business_activity_reference="BA-01 (GOV TEST)", owning_capability="C-999",
                    owning_work_package="WP-TEST-GOV", registering_act="no act", is_retroactive=False,
                )
            )
            await session.commit()
        await engine.dispose()

    asyncio.run(seed())
    environ = {bar_reconcile.RECONCILIATION_URL_ENV: url}
    assert bar_reconcile.main(["--repository-root", str(repo.root)], environ=environ) == EXIT_INTEGRITY_FAILURE
    out = capsys.readouterr().out
    assert "[ungoverned row] bar_registration BA-000001" in out
    assert "BLOCKED (OD-5 deployment-level block)" in out


# ------------------------- slice 3 review: one state per evidence condition


def test_duplicate_pending_authorizations_without_rows_are_duplicate_conflicting(repo):
    repo.write_act("ADR-9320", authorization_text("ADR-9320", "BA-01 (GOV TEST)"))
    repo.write_act("ADR-9321", authorization_text("ADR-9321", "BA-01 (GOV TEST)"))
    report, states = _states([], repo)
    assert states == [S.DUPLICATE_CONFLICTING_EVIDENCE]
    assert report.results[0].subject == "authorized (WP, reference) WP-TEST-GOV / BA-01 (GOV TEST)"


def test_one_act_id_in_two_records_without_rows_is_duplicate_conflicting(repo):
    text = authorization_text("ADR-9322", "BA-01 (GOV TEST)")
    repo.write_act("ADR-9322", text)
    repo.write_act("ADR-9322", text, name="ADR-9322-copy.md")
    _, states = _states([], repo)
    # same act id and the same authorized activity: two duplicate groups, nothing else
    assert states == [S.DUPLICATE_CONFLICTING_EVIDENCE, S.DUPLICATE_CONFLICTING_EVIDENCE]


def test_two_addenda_for_one_unpersisted_identifier_are_duplicate_not_mismatched(repo):
    repo.governed("ADR-9323", "BA-01 (GOV TEST)", "BA-000001")
    repo.governed("ADR-9324", "BA-02 (GOV TEST)", "BA-000001")
    report, states = _states([], repo)
    assert states == [S.DUPLICATE_CONFLICTING_EVIDENCE]
    assert report.results[0].subject == "issued identifier BA-000001"


def test_two_index_rows_for_one_unpersisted_identifier_are_duplicate_not_mismatched(repo):
    row = index_row("BA-000001", "BA-01 (GOV TEST)", "ADR-9325")
    repo.write_index(row, row)
    _, states = _states([], repo)
    assert states == [S.DUPLICATE_CONFLICTING_EVIDENCE, S.DUPLICATE_CONFLICTING_EVIDENCE]  # identifier and (WP, reference)


def test_row_whose_identifier_was_issued_under_another_act_is_mismatched(repo):
    repo.write_index(repo.governed("ADR-9326", "BA-01 (GOV TEST)", "BA-000001"))
    report, states = _states([snapshot("BA-000001", "BA-01 (GOV TEST)", "ADR-9399")], repo)
    assert states == [S.MISMATCHED_GOVERNING_ACT]
    assert "but the row cites 'ADR-9399'" in report.results[0].detail


def test_malformed_index_only_row_reports_its_format_problems(repo):
    repo.write_index(index_row("BA-1", "BA-01 (GOV TEST)", "ADR-9327"))
    report, states = _states([], repo)
    assert states == [S.MISMATCHED_GOVERNING_ACT]
    assert "malformed: identifier 'BA-1' is not BA-NNNNNN" in report.results[0].detail


def test_every_non_valid_state_blocks_and_only_valid_is_clean():
    from services.bar_reconciliation import ReconciliationReport, ReconciliationResult

    for state in ReconciliationState:
        report = ReconciliationReport((ReconciliationResult(state, "s", "d"),))
        assert report.blocking is (state is not S.VALID_REGISTERED_ROW)
        assert (report.exit_code == EXIT_VALID) is (state is S.VALID_REGISTERED_ROW)
