"""
TD-171 remediation tranche (WP-23 Charter §21a), R-08: PostgreSQL test path.

SKIPPED unless PostgreSQL is configured. No PostgreSQL evidence exists until
these tests have actually run against PostgreSQL; a skip is not a pass, and
the SQLite results of the other TD-171 test modules do not count (TDS §10).

Configuration (environment variables; nothing is assumed or defaulted):

  BAR_POSTGRES_TEST_DATABASE_URL
      `postgresql+asyncpg://...` URL of a DISPOSABLE database in which the
      BAR tables do not exist. The tests create `bar_identifier_ledger` and
      `bar_registration` from the models, use them, and drop them. If either
      table already exists the module refuses to run (it never touches an
      existing BAR table).

  BAR_POSTGRES_REQUIRED=1  (CI)
      PostgreSQL is mandatory: an unset URL fails the module instead of
      skipping it, so the CI job can never report a skip as a pass.

  BAR_POSTGRES_RUNTIME_ROLE_URL  (optional; role-separation tests only)
      URL for the same database as the runtime principal, which per TDS §5
      must hold SELECT only on both BAR tables. Provisioning that principal
      is EP-02 (external); no role name is assumed here. Without it the
      role-separation tests are skipped.

Covers TDS §11: A/M (governed registration end to end), E (duplicate), K
(rollback), the TD-176 concurrent collision, O (reconciliation queries),
H (ungoverned row blocks) and, with a runtime-role URL, I/J/N/R.
"""

from __future__ import annotations

import asyncio
import os
from pathlib import Path

import pytest
from sqlalchemy import inspect, select
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from models.bar_identifier_ledger import BarIdentifierLedger
from models.bar_registration import BarRegistration
from models.database import Base
from repositories.bar_identifier_repository import BarIdentifierRepository
from repositories.bar_registration_repository import BarRegistrationRepository
from services.bar_governed_registration import (
    DeploymentWriteCapability,
    GovernedBarRegistrationOperation,
    GovernedRegistrationRequest,
)
from services.bar_identifier_service import BarIdentifierService
from services.bar_reconciliation import ReconciliationState, reconcile_environment
from services.bar_registration_service import BarRegistrationAlreadyExists, BarRegistrationService
from tests.bar_governance_fixtures import GovernanceRepository, authorization_text, index_row

POSTGRES_URL_ENV = "BAR_POSTGRES_TEST_DATABASE_URL"
RUNTIME_ROLE_URL_ENV = "BAR_POSTGRES_RUNTIME_ROLE_URL"
POSTGRES_URL = os.environ.get(POSTGRES_URL_ENV, "").strip()
RUNTIME_ROLE_URL = os.environ.get(RUNTIME_ROLE_URL_ENV, "").strip()
BAR_TABLES = [BarIdentifierLedger.__table__, BarRegistration.__table__]
RUNTIME_URL = "postgresql+asyncpg://runtime-not-used@runtime-host:5432/not-used"

REQUIRED_ENV = "BAR_POSTGRES_REQUIRED"
if os.environ.get(REQUIRED_ENV) == "1" and not POSTGRES_URL:
    raise RuntimeError(f"{REQUIRED_ENV}=1 but {POSTGRES_URL_ENV} is unset: PostgreSQL BAR tests cannot be skipped here.")

pytestmark = pytest.mark.skipif(
    not POSTGRES_URL, reason=f"PostgreSQL not configured ({POSTGRES_URL_ENV} unset): NOT VERIFIED, not passed"
)
requires_runtime_role = pytest.mark.skipif(
    not RUNTIME_ROLE_URL, reason=f"runtime principal not provisioned ({RUNTIME_ROLE_URL_ENV} unset; EP-02 external)"
)


@pytest.fixture
async def pg_engine():
    engine = create_async_engine(POSTGRES_URL)
    async with engine.begin() as conn:
        existing = await conn.run_sync(lambda sync: [t.name for t in BAR_TABLES if inspect(sync).has_table(t.name)])
        if existing:
            await engine.dispose()
            pytest.fail(f"{POSTGRES_URL_ENV} must be a disposable database without BAR tables; found {existing}.")
        await conn.run_sync(lambda sync: Base.metadata.create_all(sync, tables=BAR_TABLES))
    try:
        yield engine
    finally:
        async with engine.begin() as conn:
            await conn.run_sync(lambda sync: Base.metadata.drop_all(sync, tables=BAR_TABLES))
        await engine.dispose()


@pytest.fixture
def operation(pg_engine):
    return GovernedBarRegistrationOperation(DeploymentWriteCapability.validate(POSTGRES_URL, runtime_database_url=RUNTIME_URL))


@pytest.fixture
def repo(tmp_path: Path) -> GovernanceRepository:
    repository = GovernanceRepository(tmp_path / "checkout")
    repository.write_index()
    return repository


def _request(reference: str) -> GovernedRegistrationRequest:
    return GovernedRegistrationRequest(reference, "C-999", "WP-TEST-GOV", is_retroactive=False)


async def _rows(engine) -> list[BarRegistration]:
    async with async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)() as session:
        return list((await session.execute(select(BarRegistration).order_by(BarRegistration.identifier))).scalars())


async def _reconcile(engine, repo):
    async with async_sessionmaker(engine, class_=AsyncSession)() as session:
        return await reconcile_environment(session, repo.root)


async def test_governed_registration_end_to_end_reconciles_valid(pg_engine, operation, repo):
    act_path = repo.write_act("ADR-9401", authorization_text("ADR-9401", "BA-01 (GOV TEST)"))
    executed = await operation.execute(act_path, _request("BA-01 (GOV TEST)"))
    assert [r.state for r in (await _reconcile(pg_engine, repo)).results] == [ReconciliationState.MISSING_GOVERNING_ACT]

    act_path.write_text(act_path.read_text(encoding="utf-8") + "\n" + executed.execution_addendum, encoding="utf-8")
    repo.write_index(
        index_row(executed.bar_business_activity_identifier, "BA-01 (GOV TEST)", "ADR-9401", registered_on=executed.executed_on.isoformat())
    )
    assert [r.state for r in (await _reconcile(pg_engine, repo)).results] == [ReconciliationState.VALID_REGISTERED_ROW]
    await operation.confirm(act_path)


async def test_duplicate_registration_is_refused(pg_engine, operation, repo):
    await operation.execute(repo.write_act("ADR-9402", authorization_text("ADR-9402", "BA-01 (GOV TEST)")), _request("BA-01 (GOV TEST)"))
    with pytest.raises(BarRegistrationAlreadyExists):
        await operation.execute(repo.write_act("ADR-9403", authorization_text("ADR-9403", "BA-01 (GOV TEST)")), _request("BA-01 (GOV TEST)"))
    assert [r.registering_act for r in await _rows(pg_engine)] == ["ADR-9402"]


async def test_failure_after_register_rolls_back(pg_engine, operation, repo, monkeypatch):
    real_register = BarRegistrationService.register

    async def register_then_fail(self, **kwargs):
        await real_register(self, **kwargs)
        raise RuntimeError("failure after the registration insert")

    monkeypatch.setattr(BarRegistrationService, "register", register_then_fail)
    with pytest.raises(RuntimeError):
        await operation.execute(repo.write_act("ADR-9404", authorization_text("ADR-9404", "BA-01 (GOV TEST)")), _request("BA-01 (GOV TEST)"))
    assert await _rows(pg_engine) == []


async def test_concurrent_registrations_receive_distinct_identifiers(pg_engine, operation, repo):
    """TD-176: concurrent allocation on a real transactional database."""
    paths = [
        repo.write_act(f"ADR-94{10 + i}", authorization_text(f"ADR-94{10 + i}", f"BA-{i:02d} (GOV TEST)")) for i in range(1, 6)
    ]
    outcomes = await asyncio.gather(
        *(operation.execute(path, _request(f"BA-{i:02d} (GOV TEST)")) for i, path in enumerate(paths, start=1))
    )
    identifiers = [o.bar_business_activity_identifier for o in outcomes]
    assert len(set(identifiers)) == len(identifiers)
    assert sorted(r.identifier for r in await _rows(pg_engine)) == sorted(identifiers)


async def test_ungoverned_row_blocks_and_is_preserved(pg_engine, repo):
    async with async_sessionmaker(pg_engine, class_=AsyncSession)() as session:
        await BarRegistrationService(BarRegistrationRepository(session), BarIdentifierRepository(session)).register(
            business_activity_reference="BA-01 (GOV TEST)", owning_capability="C-999", owning_work_package="WP-TEST-GOV",
            registering_act="no act", is_retroactive=False,
        )
        await session.commit()
    before = [(r.id, r.identifier, r.registered_at) for r in await _rows(pg_engine)]
    report = await _reconcile(pg_engine, repo)
    assert [r.state for r in report.results] == [ReconciliationState.UNGOVERNED_ROW]
    assert report.blocking
    assert [(r.id, r.identifier, r.registered_at) for r in await _rows(pg_engine)] == before


# ------------------------------------------------- role separation (EP-02)


@requires_runtime_role
async def test_runtime_principal_cannot_register(pg_engine):
    runtime = create_async_engine(RUNTIME_ROLE_URL)
    try:
        async with async_sessionmaker(runtime, class_=AsyncSession)() as session:
            with pytest.raises(DBAPIError):
                await BarRegistrationService(BarRegistrationRepository(session), BarIdentifierRepository(session)).register(
                    business_activity_reference="BA-01 (GOV TEST)", owning_capability="C-999",
                    owning_work_package="WP-TEST-GOV", registering_act="ADR-9420", is_retroactive=False,
                )
                await session.commit()
    finally:
        await runtime.dispose()
    assert await _rows(pg_engine) == []


@requires_runtime_role
async def test_runtime_principal_cannot_issue_an_identifier(pg_engine):
    runtime = create_async_engine(RUNTIME_ROLE_URL)
    try:
        async with async_sessionmaker(runtime, class_=AsyncSession)() as session:
            with pytest.raises(DBAPIError):
                await BarIdentifierService(BarIdentifierRepository(session)).issue_identifier()
                await session.commit()
    finally:
        await runtime.dispose()
    async with async_sessionmaker(pg_engine, class_=AsyncSession)() as session:
        assert (await session.execute(select(BarIdentifierLedger))).scalars().all() == []


@requires_runtime_role
async def test_runtime_principal_can_read_for_reconciliation(pg_engine, repo):
    runtime = create_async_engine(RUNTIME_ROLE_URL)
    try:
        report = await _reconcile(runtime, repo)
    finally:
        await runtime.dispose()
    assert report.results == ()
