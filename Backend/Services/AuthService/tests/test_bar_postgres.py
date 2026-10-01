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
from sqlalchemy import CheckConstraint, UniqueConstraint, func, inspect, select, text
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
MIGRATED_URL_ENV = "BAR_POSTGRES_MIGRATED_DATABASE_URL"
RUNTIME_ROLE_URL_ENV = "BAR_POSTGRES_RUNTIME_ROLE_URL"
REQUIRED_ENV = "BAR_POSTGRES_REQUIRED"
URLS = {
    "models": os.environ.get(POSTGRES_URL_ENV, "").strip(),
    "migrated": os.environ.get(MIGRATED_URL_ENV, "").strip(),
}
URL_ENVS = {"models": POSTGRES_URL_ENV, "migrated": MIGRATED_URL_ENV}
RUNTIME_ROLE_URL = os.environ.get(RUNTIME_ROLE_URL_ENV, "").strip()
BAR_TABLES = [BarIdentifierLedger.__table__, BarRegistration.__table__]
RUNTIME_URL = "postgresql+asyncpg://runtime-not-used@runtime-host:5432/not-used"
SERVICE_ROOT = Path(__file__).resolve().parents[1]

if os.environ.get(REQUIRED_ENV) == "1":
    missing = [URL_ENVS[source] for source, url in URLS.items() if not url]
    if missing:
        raise RuntimeError(f"{REQUIRED_ENV}=1 but {', '.join(missing)} is unset: PostgreSQL BAR tests cannot be skipped here.")

requires_runtime_role = pytest.mark.skipif(
    not RUNTIME_ROLE_URL, reason=f"runtime principal not provisioned ({RUNTIME_ROLE_URL_ENV} unset; EP-02 external)"
)
requires_migrated = pytest.mark.skipif(
    not URLS["migrated"], reason=f"migrated PostgreSQL not configured ({MIGRATED_URL_ENV} unset): NOT VERIFIED, not passed"
)


def _skip_unless_configured(source: str) -> None:
    if not URLS[source]:
        pytest.skip(f"PostgreSQL ({source} schema) not configured ({URL_ENVS[source]} unset): NOT VERIFIED, not passed")


async def _bar_table_names(conn) -> list[str]:
    return await conn.run_sync(lambda sync: [t.name for t in BAR_TABLES if inspect(sync).has_table(t.name)])


async def _model_schema_engine():
    """A disposable database with no BAR tables: create them from the models, drop them afterwards."""
    engine = create_async_engine(URLS["models"])
    async with engine.begin() as conn:
        existing = await _bar_table_names(conn)
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


async def _migrated_schema_engine():
    """
    A disposable database already migrated by `alembic upgrade head` (the real
    migration chain, run as its own process exactly as the CI bootstrap job
    does). The BAR tables must exist and be empty; the rows a test writes are
    deleted afterwards. The schema itself is never created or dropped here.
    """
    engine = create_async_engine(URLS["migrated"])
    async with engine.connect() as conn:
        existing = await _bar_table_names(conn)
        if len(existing) != len(BAR_TABLES):
            await engine.dispose()
            pytest.fail(f"{MIGRATED_URL_ENV} has BAR tables {existing}; run `alembic upgrade head` against it first.")
        counts = [(await conn.execute(select(func.count()).select_from(t))).scalar_one() for t in BAR_TABLES]
        if any(counts):
            await engine.dispose()
            pytest.fail(f"{MIGRATED_URL_ENV} BAR tables are not empty ({counts}); a disposable database is required.")
    try:
        yield engine
    finally:
        async with engine.begin() as conn:
            for table in reversed(BAR_TABLES):  # registration rows reference the ledger
                await conn.execute(table.delete())
        await engine.dispose()


@pytest.fixture(params=["models", "migrated"])
async def pg_source(request):
    """(schema source, engine, url) — every behaviour test runs on both schema sources."""
    _skip_unless_configured(request.param)
    factory = _model_schema_engine if request.param == "models" else _migrated_schema_engine
    generator = factory()
    engine = await generator.__anext__()
    try:
        yield request.param, engine, URLS[request.param]
    finally:
        await generator.aclose()


@pytest.fixture
async def migrated_engine():
    """The migrated database alone (role-separation tests run against the real migrated schema)."""
    _skip_unless_configured("migrated")
    generator = _migrated_schema_engine()
    engine = await generator.__anext__()
    try:
        yield engine
    finally:
        await generator.aclose()


@pytest.fixture
def pg_engine(pg_source):
    return pg_source[1]


@pytest.fixture
def operation(pg_source):
    return GovernedBarRegistrationOperation(DeploymentWriteCapability.validate(pg_source[2], runtime_database_url=RUNTIME_URL))


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


async def test_concurrent_registrations_collide_and_receive_distinct_identifiers(pg_engine, operation, repo, monkeypatch):
    """
    TD-176: a genuine concurrent collision on PostgreSQL. Five governed
    executions run concurrently, each on its own engine and connection. Every
    first sequence read is held until all five have read, so all five pick the
    same candidate identifier and four must lose a real UNIQUE violation and
    retry through the unchanged service's savepoint/classification path.
    """
    contenders = 5
    real_max = BarIdentifierRepository.max_identifier_sequence
    real_is_issued = BarIdentifierRepository.is_issued
    first_reads: list[int] = []
    all_read = asyncio.Event()
    collisions: list[str] = []
    connections: set[int] = set()

    async def racing_max(self):
        value = await real_max(self)
        if not all_read.is_set():
            first_reads.append(value)
            connections.add((await self.session.execute(text("SELECT pg_backend_pid()"))).scalar_one())
            if len(first_reads) == contenders:
                all_read.set()
            await asyncio.wait_for(all_read.wait(), timeout=30)
        return value

    async def counting_is_issued(self, identifier):
        issued = await real_is_issued(self, identifier)
        if issued:
            collisions.append(identifier)  # only reached after an IntegrityError
        return issued

    monkeypatch.setattr(BarIdentifierRepository, "max_identifier_sequence", racing_max)
    monkeypatch.setattr(BarIdentifierRepository, "is_issued", counting_is_issued)
    paths = [
        repo.write_act(f"ADR-94{10 + i}", authorization_text(f"ADR-94{10 + i}", f"BA-{i:02d} (GOV TEST)"))
        for i in range(1, contenders + 1)
    ]
    outcomes = await asyncio.gather(
        *(operation.execute(path, _request(f"BA-{i:02d} (GOV TEST)")) for i, path in enumerate(paths, start=1))
    )

    assert first_reads == [0] * contenders  # every contender started from the same empty sequence
    assert len(connections) == contenders  # five distinct PostgreSQL backend processes
    assert len(collisions) >= contenders - 1  # the losers hit a real UNIQUE violation
    identifiers = sorted(o.bar_business_activity_identifier for o in outcomes)
    assert identifiers == [f"BA-{n:06d}" for n in range(1, contenders + 1)]
    assert sorted(r.identifier for r in await _rows(pg_engine)) == identifiers


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
async def test_runtime_principal_cannot_register(migrated_engine):
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
    assert await _rows(migrated_engine) == []


@requires_runtime_role
async def test_runtime_principal_cannot_issue_an_identifier(migrated_engine):
    runtime = create_async_engine(RUNTIME_ROLE_URL)
    try:
        async with async_sessionmaker(runtime, class_=AsyncSession)() as session:
            with pytest.raises(DBAPIError):
                await BarIdentifierService(BarIdentifierRepository(session)).issue_identifier()
                await session.commit()
    finally:
        await runtime.dispose()
    async with async_sessionmaker(migrated_engine, class_=AsyncSession)() as session:
        assert (await session.execute(select(BarIdentifierLedger))).scalars().all() == []


@requires_runtime_role
async def test_runtime_principal_can_read_for_reconciliation(migrated_engine, repo):
    runtime = create_async_engine(RUNTIME_ROLE_URL)
    try:
        report = await _reconcile(runtime, repo)
    finally:
        await runtime.dispose()
    assert report.results == ()


# ------------------------------------------- migrated schema (Alembic head)


@requires_migrated
async def test_migrated_database_is_at_the_alembic_head():
    from alembic.config import Config
    from alembic.script import ScriptDirectory

    head = ScriptDirectory.from_config(Config(str(SERVICE_ROOT / "alembic.ini"))).get_current_head()
    engine = create_async_engine(URLS["migrated"])
    try:
        async with engine.connect() as conn:
            versions = (await conn.execute(text("SELECT version_num FROM alembic_version"))).scalars().all()
    finally:
        await engine.dispose()
    assert versions == [head]


@requires_migrated
@pytest.mark.parametrize("table", BAR_TABLES, ids=lambda t: t.name)
async def test_migrated_bar_schema_matches_the_models(table):
    """
    The migration chain and the models must describe the same BAR tables.
    Expectations are derived from the model metadata and compared with what
    PostgreSQL reflects after `alembic upgrade head`; no schema is restated here.
    """
    from sqlalchemy.dialects import postgresql

    dialect = postgresql.dialect()

    def reflect(sync):
        inspector = inspect(sync)
        unique = {frozenset(u["column_names"]) for u in inspector.get_unique_constraints(table.name)}
        unique |= {frozenset(i["column_names"]) for i in inspector.get_indexes(table.name) if i["unique"]}
        return {
            "columns": {c["name"]: (c["type"].compile(dialect=dialect), c["nullable"]) for c in inspector.get_columns(table.name)},
            "primary_key": set(inspector.get_pk_constraint(table.name)["constrained_columns"]),
            "unique": unique,
            "foreign_keys": {
                (tuple(f["constrained_columns"]), f["referred_table"], tuple(f["referred_columns"]))
                for f in inspector.get_foreign_keys(table.name)
            },
            "checks": {c["name"] for c in inspector.get_check_constraints(table.name)},
        }

    engine = create_async_engine(URLS["migrated"])
    try:
        async with engine.connect() as conn:
            actual = await conn.run_sync(reflect)
    finally:
        await engine.dispose()

    assert actual["columns"] == {c.name: (c.type.compile(dialect=dialect), c.nullable) for c in table.columns}
    assert actual["primary_key"] == {c.name for c in table.primary_key.columns}
    expected_unique = {frozenset(c.name for c in u.columns) for u in table.constraints if isinstance(u, UniqueConstraint)}
    expected_unique |= {frozenset([c.name]) for c in table.columns if c.unique}
    expected_unique |= {frozenset(c.name for c in i.columns) for i in table.indexes if i.unique}
    assert expected_unique <= actual["unique"]
    assert actual["foreign_keys"] == {((fk.parent.name,), fk.column.table.name, (fk.column.name,)) for fk in table.foreign_keys}
    expected_checks = {str(c.name) for c in table.constraints if isinstance(c, CheckConstraint)}
    assert expected_checks <= actual["checks"]
