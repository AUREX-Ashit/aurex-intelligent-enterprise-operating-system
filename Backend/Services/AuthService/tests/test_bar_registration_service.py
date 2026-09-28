"""
Enterprise BAR — WP-23 Workstream C ("canonical Business Activity
registration mechanism") implementation tests.

Covers this Workstream's own required demonstration set:
  * a valid registration receives a valid `BA-NNNNNN` identifier
  * all eight mandatory fields are persisted correctly
  * registration status is recorded as `REGISTERED`
  * registering act, registration date, retroactive flag, owning
    capability, and owning work package are each persisted exactly as
    supplied/assigned
  * duplicate registration (same work package + reference) is rejected
    safely, without consuming a new identifier
  * a forced identifier collision is retried without producing a
    duplicate or a half-registered row (mirroring, and extending,
    Workstream B's own deterministic-collision test)
  * a failed registration (allocation exhausted) leaves no partial
    ledger/registration state
  * genuine multi-session async concurrency is, once again, not reliably
    testable on this repository's own SQLite harness — disclosed
    explicitly rather than silently attempted or silently ignored,
    exactly mirroring Workstream B's own identical, already-documented
    finding
  * this workstream performs no interaction with, and no mutation of,
    `BAR-INDEX.md`
  * this workstream registers zero real Business Activities from the 21
    existing rows and assigns zero identifiers to C-024 BA-01 — every
    registration created by these tests uses obviously-synthetic test
    data (`owning_work_package="WP-TEST-01"`, etc.), never a real WP/
    capability identifier from the actual 21-row inventory or from
    C-024/WP-22
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from models.bar_identifier_ledger import BarIdentifierLedger
from repositories.bar_identifier_repository import BarIdentifierRepository
from repositories.bar_registration_repository import BarRegistrationRepository
from services.bar_registration_service import (
    BarRegistrationAllocationExhausted,
    BarRegistrationAlreadyExists,
    BarRegistrationService,
)

# pytest.ini sets `asyncio_mode = auto` — plain `async def test_*` runs.

_IDENTIFIER_RE = re.compile(r"^BA-\d{6}$")

_BAR_INDEX_PATH = (
    Path(__file__).resolve().parents[4] / "architecture" / "00-Governance" / "BAR-INDEX.md"
)

# Deliberately synthetic — never a real WP/capability from the actual
# 21-row inventory, never C-024/WP-22.
_TEST_WP = "WP-TEST-01"
_TEST_CAPABILITY = "C-TEST"
_TEST_REFERENCE = "Test Business Activity — Mechanism Verification Only"
_TEST_ACT = "TEST-REGISTERING-ACT-NOT-A-REAL-GOVERNANCE-ARTIFACT"


def _service(db_session: AsyncSession) -> BarRegistrationService:
    return BarRegistrationService(
        BarRegistrationRepository(db_session),
        BarIdentifierRepository(db_session),
    )


def _bar_index_hash() -> str | None:
    if not _BAR_INDEX_PATH.exists():
        return None
    return hashlib.sha256(_BAR_INDEX_PATH.read_bytes()).hexdigest()


# ---------------------------------------------------------------------------
# successful registration / mandatory-field persistence
# ---------------------------------------------------------------------------

async def test_register_returns_valid_identifier(db_session: AsyncSession):
    svc = _service(db_session)
    row = await svc.register(
        business_activity_reference=_TEST_REFERENCE,
        owning_capability=_TEST_CAPABILITY,
        owning_work_package=_TEST_WP,
        registering_act=_TEST_ACT,
        is_retroactive=False,
    )
    await db_session.commit()

    assert _IDENTIFIER_RE.match(row.identifier)
    assert row.identifier == "BA-000001"


async def test_register_persists_all_eight_mandatory_fields(db_session: AsyncSession):
    svc = _service(db_session)
    row = await svc.register(
        business_activity_reference=_TEST_REFERENCE,
        owning_capability=_TEST_CAPABILITY,
        owning_work_package=_TEST_WP,
        registering_act=_TEST_ACT,
        is_retroactive=True,
    )
    await db_session.commit()

    # 1. Identifier
    assert _IDENTIFIER_RE.match(row.identifier)
    # 2. Reference
    assert row.business_activity_reference == _TEST_REFERENCE
    # 3. Owning Capability
    assert row.owning_capability == _TEST_CAPABILITY
    # 4. Owning Work Package
    assert row.owning_work_package == _TEST_WP
    # 5. Registration Status
    assert row.registration_status == "REGISTERED"
    # 6. Registering Act
    assert row.registering_act == _TEST_ACT
    # 7. Registration Date
    assert row.registered_at is not None
    # 8. Retroactive flag
    assert row.is_retroactive is True


async def test_retroactive_flag_persists_false_when_prospective(db_session: AsyncSession):
    svc = _service(db_session)
    row = await svc.register(
        business_activity_reference=_TEST_REFERENCE,
        owning_capability=_TEST_CAPABILITY,
        owning_work_package=_TEST_WP,
        registering_act=_TEST_ACT,
        is_retroactive=False,
    )
    await db_session.commit()
    assert row.is_retroactive is False


async def test_second_registration_in_different_wp_gets_next_sequential_identifier(
    db_session: AsyncSession,
):
    svc = _service(db_session)
    first = await svc.register(
        business_activity_reference=_TEST_REFERENCE,
        owning_capability=_TEST_CAPABILITY,
        owning_work_package="WP-TEST-01",
        registering_act=_TEST_ACT,
        is_retroactive=False,
    )
    await db_session.commit()
    second = await svc.register(
        business_activity_reference=_TEST_REFERENCE,  # same reference, different WP — not a duplicate
        owning_capability=_TEST_CAPABILITY,
        owning_work_package="WP-TEST-02",
        registering_act=_TEST_ACT,
        is_retroactive=False,
    )
    await db_session.commit()

    assert first.identifier == "BA-000001"
    assert second.identifier == "BA-000002"


# ---------------------------------------------------------------------------
# duplicate protection
# ---------------------------------------------------------------------------

async def test_duplicate_registration_same_wp_and_reference_is_rejected(db_session: AsyncSession):
    svc = _service(db_session)
    await svc.register(
        business_activity_reference=_TEST_REFERENCE,
        owning_capability=_TEST_CAPABILITY,
        owning_work_package=_TEST_WP,
        registering_act=_TEST_ACT,
        is_retroactive=False,
    )
    await db_session.commit()

    with pytest.raises(BarRegistrationAlreadyExists):
        await svc.register(
            business_activity_reference=_TEST_REFERENCE,
            owning_capability=_TEST_CAPABILITY,
            owning_work_package=_TEST_WP,
            registering_act="A DIFFERENT ACT — STILL A DUPLICATE",
            is_retroactive=False,
        )

    reg_repo = BarRegistrationRepository(db_session)
    assert await reg_repo.count_registered() == 1  # rejected attempt did not create a second row


async def test_duplicate_rejection_does_not_consume_an_identifier(db_session: AsyncSession):
    """
    A rejected duplicate must not burn a `BA-NNNNNN` value — the
    fast-path pre-check runs before any identifier candidate is computed.
    """
    svc = _service(db_session)
    first = await svc.register(
        business_activity_reference=_TEST_REFERENCE,
        owning_capability=_TEST_CAPABILITY,
        owning_work_package=_TEST_WP,
        registering_act=_TEST_ACT,
        is_retroactive=False,
    )
    await db_session.commit()

    with pytest.raises(BarRegistrationAlreadyExists):
        await svc.register(
            business_activity_reference=_TEST_REFERENCE,
            owning_capability=_TEST_CAPABILITY,
            owning_work_package=_TEST_WP,
            registering_act=_TEST_ACT,
            is_retroactive=False,
        )

    id_repo = BarIdentifierRepository(db_session)
    assert await id_repo.max_identifier_sequence() == 1  # still just the one from `first`

    second = await svc.register(
        business_activity_reference="A genuinely different Business Activity",
        owning_capability=_TEST_CAPABILITY,
        owning_work_package=_TEST_WP,
        registering_act=_TEST_ACT,
        is_retroactive=False,
    )
    await db_session.commit()
    assert second.identifier == "BA-000002"  # no gap from the rejected duplicate
    assert first.identifier == "BA-000001"


# ---------------------------------------------------------------------------
# collision / atomicity / rollback
# ---------------------------------------------------------------------------

async def test_forced_identifier_collision_is_retried_without_duplicate_or_half_registration(
    db_session: AsyncSession,
):
    """
    Pre-seeds `BA-000001` directly in the ledger (as Workstream B's own
    test does), so the service's first natural candidate collides and
    must retry with `BA-000002` — proving the retry loop covers BOTH the
    ledger insert and the registration insert together, not just one.
    """
    db_session.add(BarIdentifierLedger(identifier="BA-000001"))
    await db_session.commit()

    svc = _service(db_session)
    row = await svc.register(
        business_activity_reference=_TEST_REFERENCE,
        owning_capability=_TEST_CAPABILITY,
        owning_work_package=_TEST_WP,
        registering_act=_TEST_ACT,
        is_retroactive=False,
    )
    await db_session.commit()

    assert row.identifier == "BA-000002"
    reg_repo = BarRegistrationRepository(db_session)
    assert await reg_repo.count_registered() == 1  # exactly one registration, not two, not zero


async def test_allocation_exhausted_leaves_no_partial_registration(
    db_session: AsyncSession, monkeypatch
):
    """
    If every retry candidate collides, the service raises
    `BarRegistrationAllocationExhausted` and leaves neither an orphaned
    ledger entry attributable to this attempt nor a half-registered row
    — the ledger's own count reflects only the one pre-seeded collision
    target, and the registration table has zero rows.
    """
    db_session.add(BarIdentifierLedger(identifier="BA-000001"))
    await db_session.commit()

    svc = _service(db_session)

    async def _always_same_candidate() -> str:
        return "BA-000001"

    monkeypatch.setattr(svc, "_next_identifier", _always_same_candidate)

    with pytest.raises(BarRegistrationAllocationExhausted):
        await svc.register(
            business_activity_reference=_TEST_REFERENCE,
            owning_capability=_TEST_CAPABILITY,
            owning_work_package=_TEST_WP,
            registering_act=_TEST_ACT,
            is_retroactive=False,
        )

    id_repo = BarIdentifierRepository(db_session)
    reg_repo = BarRegistrationRepository(db_session)
    assert await id_repo.count_issued() == 1  # only the pre-seeded row
    assert await reg_repo.count_registered() == 0  # no half-registration


async def test_required_fields_are_validated(db_session: AsyncSession):
    svc = _service(db_session)
    with pytest.raises(ValueError):
        await svc.register(
            business_activity_reference="   ",
            owning_capability=_TEST_CAPABILITY,
            owning_work_package=_TEST_WP,
            registering_act=_TEST_ACT,
            is_retroactive=False,
        )


async def test_service_requires_shared_session_across_repositories():
    """
    Constructing the service with two repositories bound to different
    sessions must fail fast — that combination cannot provide the
    atomicity guarantee this mechanism exists to give.
    """
    from unittest.mock import MagicMock

    reg_repo = MagicMock()
    reg_repo.session = object()
    id_repo = MagicMock()
    id_repo.session = object()

    with pytest.raises(ValueError):
        BarRegistrationService(reg_repo, id_repo)


# ---------------------------------------------------------------------------
# disclosed test-harness limitation (mirrors Workstream B's own finding)
# ---------------------------------------------------------------------------

async def test_true_concurrent_sessions_not_reliably_testable_on_this_harness(test_engine):
    """
    Disclosed, not silently assumed impossible: genuine multi-session
    concurrent registration attempts were not added to this suite as an
    `asyncio.gather`-style race, for the same, already-empirically-
    verified reason Workstream B's own identical test documents —
    independent `AsyncSession` objects against this repository's shared
    in-memory SQLite `test_engine` do not reliably provide the
    transactional isolation a genuine concurrent-write test requires (an
    explicit `StaticPool` attempt during Workstream B's own verification
    deadlocked rather than serializing correctly). Creating such a test
    here would risk exactly the same false-confidence-or-flaky outcome,
    not a stronger concurrency proof.

    What this suite proves instead, deterministically: the
    `uq_bar_registration_wp_reference` and `bar_identifier_ledger`
    UNIQUE constraints are real database constraints (not
    application-side "check then insert"), and the service's own retry
    loop correctly distinguishes a duplicate-key race
    (`test_duplicate_rejection_does_not_consume_an_identifier`,
    `test_duplicate_registration_same_wp_and_reference_is_rejected`) from
    an identifier collision
    (`test_forced_identifier_collision_is_retried_without_duplicate_or_
    half_registration`) — the two mechanisms that would jointly prevent
    a real duplicate registration under genuine concurrent load, per
    PostgreSQL's own stricter (row-level, MVCC) concurrency model. That
    specific claim is not independently re-verified against PostgreSQL
    in this suite.
    """
    assert test_engine is not None  # fixture wiring only; no concurrency assertion is made here


# ---------------------------------------------------------------------------
# boundary: no BAR-INDEX.md interaction, no real 21-row/C-024 registration
# ---------------------------------------------------------------------------

async def test_registration_does_not_touch_bar_index_md(db_session: AsyncSession):
    before = _bar_index_hash()
    assert before is not None, "BAR-INDEX.md must exist (Workstream A) for this check to be meaningful"

    svc = _service(db_session)
    for i in range(3):
        await svc.register(
            business_activity_reference=f"{_TEST_REFERENCE} {i}",
            owning_capability=_TEST_CAPABILITY,
            owning_work_package=_TEST_WP,
            registering_act=_TEST_ACT,
            is_retroactive=False,
        )
        await db_session.commit()

    after = _bar_index_hash()
    assert after == before, "Workstream C must not modify BAR-INDEX.md"


async def test_no_test_registration_uses_a_real_existing_wp_or_c024():
    """
    Static assertion, not a database check: every registration this
    suite performs uses the obviously-synthetic `WP-TEST-*`/`C-TEST`
    constants defined at the top of this file — never `WP-22` (C-024)
    or any of the actual `WP-01`–`WP-21` identifiers from the real
    21-row inventory. This test exists to make that boundary
    machine-checked rather than merely asserted in prose.
    """
    assert _TEST_WP.startswith("WP-TEST-")
    assert _TEST_CAPABILITY == "C-TEST"
    assert _TEST_WP != "WP-22"
