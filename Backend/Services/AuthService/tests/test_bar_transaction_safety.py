"""
Enterprise BAR — WP-23 A–C Gate 3 remediation tests (VV-F-01, VV-F-02).

VV-F-01: an identifier collision or duplicate race inside
`BarRegistrationService.register()` / `BarIdentifierService.issue_identifier()`
used to roll back the caller's WHOLE session and then return normally,
silently discarding the caller's other pending/flushed work (including an
earlier registration in the same session). The services now isolate each
allocation attempt in a SAVEPOINT (`session.begin_nested()`).

VV-F-02: any `IntegrityError` used to be treated as an identifier collision
(retried, then reported as "allocation exhausted"). Only a genuine collision
is now retried; any other integrity failure is re-raised unchanged.

Harness note: these tests deliberately do NOT use the shared `db_session`
fixture. That fixture's SQLite engine enforces no foreign keys (TD-096) and
uses pysqlite's legacy transaction handling, under which a SAVEPOINT that is
the first statement of a transaction is not nested in a real transaction.
Each test here gets its own file-backed SQLite engine with
`PRAGMA foreign_keys=ON` on every connection and SQLAlchemy's documented
pysqlite/aiosqlite recipe for correct SAVEPOINT semantics (driver-level
autocommit off, explicit `BEGIN` on transaction start), so the transaction
behaviour under test matches a real transactional database. True concurrent
PostgreSQL races are NOT exercised here; collisions are forced
deterministically with a genuine database UNIQUE violation.

All data is synthetic (`WP-TEST-*`, `C-TEST`); no real Business Activity is
registered and no real identifier is assigned.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from sqlalchemy import event, func, select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from models.bar_identifier_ledger import BarIdentifierLedger
from models.bar_registration import BarRegistration
from models.database import Base
from models.domain import Domain
from repositories.bar_identifier_repository import BarIdentifierRepository
from repositories.bar_registration_repository import BarRegistrationRepository
from services.bar_identifier_service import BarIdentifierAllocationExhausted, BarIdentifierService
from services.bar_registration_service import (
    BarRegistrationAllocationExhausted,
    BarRegistrationAlreadyExists,
    BarRegistrationService,
)

_KW = dict(
    owning_capability="C-TEST",
    owning_work_package="WP-TEST-TXN",
    registering_act="TEST-REGISTERING-ACT-NOT-A-REAL-GOVERNANCE-ARTIFACT",
    is_retroactive=False,
)


@pytest.fixture
async def txn_engine(tmp_path):
    engine = create_async_engine(f"sqlite+aiosqlite:///{tmp_path / 'bar_txn.db'}")
    savepoint_rollbacks: list[str] = []

    @event.listens_for(engine.sync_engine, "connect")
    def _connect(dbapi_connection, _record):
        dbapi_connection.isolation_level = None  # SQLAlchemy emits BEGIN itself
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    @event.listens_for(engine.sync_engine, "begin")
    def _begin(conn):
        conn.exec_driver_sql("BEGIN")

    @event.listens_for(engine.sync_engine, "rollback_savepoint")
    def _rollback_savepoint(_conn, name, _context):
        savepoint_rollbacks.append(name)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield SimpleNamespace(engine=engine, savepoint_rollbacks=savepoint_rollbacks)
    await engine.dispose()


@pytest.fixture
def sessions(txn_engine):
    return async_sessionmaker(txn_engine.engine, class_=AsyncSession, expire_on_commit=False)


def _registration_service(session: AsyncSession) -> BarRegistrationService:
    return BarRegistrationService(BarRegistrationRepository(session), BarIdentifierRepository(session))


async def _seed_ledger(sessions, identifier: str) -> None:
    async with sessions() as s:
        s.add(BarIdentifierLedger(identifier=identifier))
        await s.commit()


def _force_one_stale_max_read(repo: BarIdentifierRepository) -> dict:
    """Make the next MAX read return 0 once, so the candidate collides with a
    committed `BA-000001` — a genuine database UNIQUE violation, the same shape
    as a lost race against another transaction."""
    real = repo.max_identifier_sequence
    calls = {"n": 0}

    async def stale_once() -> int:
        calls["n"] += 1
        return 0 if calls["n"] == 1 else await real()

    repo.max_identifier_sequence = stale_once
    return calls


async def _all(sessions, stmt):
    async with sessions() as s:
        return (await s.execute(stmt)).all()


# ---------------------------------------------------------------------------
# harness positive control
# ---------------------------------------------------------------------------

async def test_harness_enforces_foreign_keys(sessions):
    async with sessions() as s:
        assert (await s.execute(text("PRAGMA foreign_keys"))).scalar_one() == 1
        s.add(
            BarRegistration(
                identifier="BA-424242",  # not in the ledger
                business_activity_reference="orphan",
                **_KW,
            )
        )
        with pytest.raises(IntegrityError):
            await s.flush()


# ---------------------------------------------------------------------------
# VV-F-01 — caller work survives a collision / duplicate race
# ---------------------------------------------------------------------------

async def test_first_registration_survives_collision_on_second(sessions, txn_engine):
    """The exact Gate 2 VV-F-01 scenario: two registrations in one caller
    session; the second loses an identifier race. Pre-fix, the first was
    silently lost and its identifier was handed out again."""
    await _seed_ledger(sessions, "BA-000001")

    async with sessions() as s:
        svc = _registration_service(s)
        first = await svc.register(business_activity_reference="First BA", **_KW)
        calls = _force_one_stale_max_read(svc.identifier_repo)
        second = await svc.register(business_activity_reference="Second BA", **_KW)
        await s.commit()

    assert calls["n"] == 2  # the stale candidate was tried, then a fresh one
    assert txn_engine.savepoint_rollbacks  # a real collision was rolled back
    assert first.identifier == "BA-000002"
    assert second.identifier == "BA-000003"
    rows = await _all(
        sessions,
        select(BarRegistration.identifier, BarRegistration.business_activity_reference).order_by(
            BarRegistration.identifier
        ),
    )
    assert rows == [("BA-000002", "First BA"), ("BA-000003", "Second BA")]


async def test_unrelated_pending_caller_work_survives_registration_collision(sessions):
    await _seed_ledger(sessions, "BA-000001")

    async with sessions() as s:
        s.add(Domain(domain_name="Unrelated caller work (pending)"))
        svc = _registration_service(s)
        _force_one_stale_max_read(svc.identifier_repo)
        row = await svc.register(business_activity_reference="Registered after a collision", **_KW)
        await s.commit()

    assert row.identifier == "BA-000002"
    assert await _all(sessions, select(Domain.domain_name)) == [("Unrelated caller work (pending)",)]


async def test_unrelated_pending_caller_work_survives_issuance_collision(sessions, txn_engine):
    await _seed_ledger(sessions, "BA-000001")

    async with sessions() as s:
        s.add(Domain(domain_name="Unrelated caller work (pending)"))
        repo = BarIdentifierRepository(s)
        _force_one_stale_max_read(repo)
        identifier = await BarIdentifierService(repo).issue_identifier()
        await s.commit()

    assert txn_engine.savepoint_rollbacks
    assert identifier == "BA-000002"
    assert await _all(sessions, select(Domain.domain_name)) == [("Unrelated caller work (pending)",)]


async def test_first_registration_survives_duplicate_race_on_second(sessions):
    """Gate 2's second variant: the second call loses a duplicate race
    (pre-check blinded once); it must raise, and the first must survive."""
    async with sessions() as s:
        await _registration_service(s).register(business_activity_reference="Existing BA", **_KW)
        await s.commit()

    async with sessions() as s:
        svc = _registration_service(s)
        first = await svc.register(business_activity_reference="New BA", **_KW)
        real = svc.registration_repo.get_by_work_package_and_reference
        calls = {"n": 0}

        async def blind_once(wp, ref):
            calls["n"] += 1
            return None if calls["n"] == 1 else await real(wp, ref)

        svc.registration_repo.get_by_work_package_and_reference = blind_once
        with pytest.raises(BarRegistrationAlreadyExists):
            await svc.register(business_activity_reference="Existing BA", **_KW)
        await s.commit()

    rows = await _all(
        sessions,
        select(BarRegistration.identifier, BarRegistration.business_activity_reference).order_by(
            BarRegistration.identifier
        ),
    )
    assert rows == [("BA-000001", "Existing BA"), (first.identifier, "New BA")]


async def test_caller_still_owns_the_transaction(sessions):
    """No hidden commit: if the caller rolls back, the registration and the
    caller's own work are both discarded, collision or not."""
    await _seed_ledger(sessions, "BA-000001")

    async with sessions() as s:
        s.add(Domain(domain_name="Caller work to be rolled back"))
        svc = _registration_service(s)
        _force_one_stale_max_read(svc.identifier_repo)
        await svc.register(business_activity_reference="Rolled back BA", **_KW)
        await s.rollback()

    assert await _all(sessions, select(func.count()).select_from(BarRegistration)) == [(0,)]
    assert await _all(sessions, select(func.count()).select_from(Domain)) == [(0,)]
    assert await _all(sessions, select(BarIdentifierLedger.identifier)) == [("BA-000001",)]


# ---------------------------------------------------------------------------
# genuine collision retry and exhaustion (unchanged semantics)
# ---------------------------------------------------------------------------

async def test_genuine_collision_exhaustion_still_raises_without_partial_rows(sessions, monkeypatch):
    await _seed_ledger(sessions, "BA-000001")

    async with sessions() as s:
        s.add(Domain(domain_name="Unrelated caller work (pending)"))
        svc = _registration_service(s)

        async def always_colliding() -> str:
            return "BA-000001"

        monkeypatch.setattr(svc, "_next_identifier", always_colliding)
        with pytest.raises(BarRegistrationAllocationExhausted):
            await svc.register(business_activity_reference="Never registered", **_KW)
        await s.commit()

    assert await _all(sessions, select(func.count()).select_from(BarRegistration)) == [(0,)]
    assert await _all(sessions, select(BarIdentifierLedger.identifier)) == [("BA-000001",)]
    assert await _all(sessions, select(Domain.domain_name)) == [("Unrelated caller work (pending)",)]


# ---------------------------------------------------------------------------
# VV-F-02 — a non-collision integrity failure is not a collision
# ---------------------------------------------------------------------------

async def test_non_collision_integrity_error_is_not_retried_in_register(sessions):
    async with sessions() as s:
        svc = _registration_service(s)
        first = await svc.register(business_activity_reference="Kept BA", **_KW)
        attempts = {"n": 0}
        real_next = svc._next_identifier

        async def counting_next() -> str:
            attempts["n"] += 1
            return await real_next()

        svc._next_identifier = counting_next
        with pytest.raises(IntegrityError) as caught:
            # `is_retroactive` is NOT NULL: a genuine, non-collision failure.
            await svc.register(
                business_activity_reference="Invalid BA",
                owning_capability="C-TEST",
                owning_work_package="WP-TEST-TXN",
                registering_act="TEST-REGISTERING-ACT-NOT-A-REAL-GOVERNANCE-ARTIFACT",
                is_retroactive=None,
            )
        assert not isinstance(caught.value, BarRegistrationAllocationExhausted)
        assert attempts["n"] == 1  # never entered the collision retry path
        await s.commit()

    assert await _all(
        sessions, select(BarRegistration.identifier, BarRegistration.business_activity_reference)
    ) == [(first.identifier, "Kept BA")]
    assert await _all(sessions, select(BarIdentifierLedger.identifier)) == [(first.identifier,)]


async def test_non_collision_integrity_error_is_not_retried_in_issuance(sessions):
    async with sessions() as s:
        s.add(Domain(domain_name="Unrelated caller work (pending)"))
        svc = BarIdentifierService(BarIdentifierRepository(s))
        attempts = {"n": 0}

        async def null_candidate():
            attempts["n"] += 1
            return None  # `identifier` is NOT NULL: a non-collision failure

        svc._next_identifier = null_candidate
        with pytest.raises(IntegrityError) as caught:
            await svc.issue_identifier()
        assert not isinstance(caught.value, BarIdentifierAllocationExhausted)
        assert attempts["n"] == 1
        await s.commit()

    assert await _all(sessions, select(func.count()).select_from(BarIdentifierLedger)) == [(0,)]
    assert await _all(sessions, select(Domain.domain_name)) == [("Unrelated caller work (pending)",)]


async def test_caller_pending_work_failure_is_not_classified_as_collision(sessions):
    """An invalid object the CALLER left pending fails at the service's
    initial flush, as itself — before any allocation attempt."""
    async with sessions() as s:
        s.add(Domain(domain_name=None))  # caller's own invalid work
        svc = _registration_service(s)
        attempts = {"n": 0}

        async def counting_next() -> str:
            attempts["n"] += 1
            return "BA-000001"

        svc._next_identifier = counting_next
        with pytest.raises(IntegrityError):
            await svc.register(business_activity_reference="Never attempted", **_KW)
        assert attempts["n"] == 0
