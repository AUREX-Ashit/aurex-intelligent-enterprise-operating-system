"""
WP-18 (C-003, TDS-018 §29.2) — Approval Authority Runtime Resolver tests.

Realizes TDS-018 §29.6's own minimum test obligations (also restated at
WP-18 §18) plus CLAUDE.md §21.4's Mandatory Tenant-Isolation Test
Checklist: two distinct, unrelated Organizations with no shared row; an
explicit cross-Organization denial; and an explicit probe of a foreign
Approval Authority identifier (belonging to an unrelated Organization)
not derived from the caller's own claims.

Every test exercises `resolve_approval_authority()` directly (the plain,
testable function TDS-018 §29.2 designs) and, where the admin-bypass-
absence and tenant-mismatch behavior specifically depend on it, the
`enforce_approval_authority()` FastAPI-facing wrapper in `dependencies.py`
— no HTTP router exists for this Work Package (WP-18's own charter
authorizes no such endpoint; a future consumer, e.g. C-023, would wire
`require_approval_authority()` into its own route).
"""

import uuid
from datetime import datetime, timedelta, timezone

import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import enforce_approval_authority
from models.approval_authority import ApprovalAuthority
from models.membership import Membership
from models.membership_approval_authority import MembershipApprovalAuthority
from models.organization import Organization
from models.person import Person
from models.role import Role
from services.approval_authority_resolver import ApprovalAuthorityResolution, resolve_approval_authority

AUTHORITY_NAME = "Test Commit Authority"


async def _make_org_membership(
    db_session: AsyncSession, org_code: str, person_name: str, role_code: str
) -> tuple[Organization, Membership]:
    role = Role(role_code=role_code, role_name=f"{role_code} Role")
    org = Organization(organization_code=org_code, organization_name=org_code, organization_type="CORPORATE")
    person = Person(first_name=person_name, last_name="Test", display_name=f"{person_name} Test")
    db_session.add_all([role, org, person])
    await db_session.flush()

    membership = Membership(person_id=person.id, organization_id=org.id, role_id=role.id)
    db_session.add(membership)
    await db_session.flush()
    return org, membership


async def _make_authority(
    db_session: AsyncSession,
    organization_id: uuid.UUID,
    approval_strategy: str = "ANY_ONE",
    majority_threshold_pct: int | None = None,
    status: str = "ACTIVE",
    authority_name: str = AUTHORITY_NAME,
) -> ApprovalAuthority:
    authority = ApprovalAuthority(
        organization_id=organization_id,
        authority_name=authority_name,
        approval_strategy=approval_strategy,
        majority_threshold_pct=majority_threshold_pct,
        scope_type="COMPANY",
        status=status,
    )
    db_session.add(authority)
    await db_session.flush()
    return authority


async def _bind(
    db_session: AsyncSession,
    membership_id: uuid.UUID,
    approval_authority_id: uuid.UUID,
    effective_from: datetime | None = None,
    effective_to: datetime | None = None,
) -> MembershipApprovalAuthority:
    binding = MembershipApprovalAuthority(
        membership_id=membership_id,
        approval_authority_id=approval_authority_id,
        effective_to=effective_to,
    )
    if effective_from is not None:
        binding.effective_from = effective_from
    db_session.add(binding)
    await db_session.flush()
    return binding


@pytest.fixture
async def org_a(db_session: AsyncSession):
    org, membership = await _make_org_membership(db_session, "RESOLVER-ORG-A", "Alice", "RESOLVER_TEST_ROLE_A")
    return org, membership


@pytest.fixture
async def org_b(db_session: AsyncSession):
    org, membership = await _make_org_membership(db_session, "RESOLVER-ORG-B", "Bob", "RESOLVER_TEST_ROLE_B")
    return org, membership


# ---------------------------------------------------------------------------
# 1. ANY_ONE + valid binding -> AUTHORIZED
# ---------------------------------------------------------------------------

async def test_any_one_with_valid_binding_authorizes(db_session: AsyncSession, org_a) -> None:
    org, membership = org_a
    authority = await _make_authority(db_session, org.id, approval_strategy="ANY_ONE")
    await _bind(db_session, membership.id, authority.id)

    result = await resolve_approval_authority(
        db_session, org.id, AUTHORITY_NAME, org.id, membership.id
    )
    assert result == ApprovalAuthorityResolution.AUTHORIZED


# ---------------------------------------------------------------------------
# 2. missing authority -> NO_AUTHORITY_CONFIGURED
# ---------------------------------------------------------------------------

async def test_missing_authority_denies(db_session: AsyncSession, org_a) -> None:
    org, membership = org_a
    result = await resolve_approval_authority(
        db_session, org.id, "Nonexistent Authority", org.id, membership.id
    )
    assert result == ApprovalAuthorityResolution.NO_AUTHORITY_CONFIGURED


# ---------------------------------------------------------------------------
# 3. inactive (SUPERSEDED/DEPRECATED/RETIRED) authority -> INACTIVE_AUTHORITY
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("stale_status", ["SUPERSEDED", "DEPRECATED", "RETIRED"])
async def test_inactive_authority_denies(db_session: AsyncSession, org_a, stale_status: str) -> None:
    org, membership = org_a
    authority = await _make_authority(db_session, org.id, status=stale_status)
    await _bind(db_session, membership.id, authority.id)

    result = await resolve_approval_authority(
        db_session, org.id, AUTHORITY_NAME, org.id, membership.id
    )
    assert result == ApprovalAuthorityResolution.INACTIVE_AUTHORITY


# ---------------------------------------------------------------------------
# 4. malformed configuration (MAJORITY, no threshold) -> INVALID_CONFIGURATION,
#    unreachable via a qualifying binding
# ---------------------------------------------------------------------------

async def test_malformed_majority_configuration_denies_before_binding_check(
    db_session: AsyncSession, org_a
) -> None:
    org, membership = org_a
    authority = await _make_authority(
        db_session, org.id, approval_strategy="MAJORITY", majority_threshold_pct=None
    )
    await _bind(db_session, membership.id, authority.id)

    result = await resolve_approval_authority(
        db_session, org.id, AUTHORITY_NAME, org.id, membership.id
    )
    assert result == ApprovalAuthorityResolution.INVALID_CONFIGURATION


# ---------------------------------------------------------------------------
# 5/6/7. MAJORITY / ALL / SEQUENTIAL + valid binding -> UNSUPPORTED_STRATEGY,
#    never AUTHORIZED -- the core false-ALLOW-prevention regression test
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("strategy,threshold", [("MAJORITY", 60), ("ALL", None), ("SEQUENTIAL", None)])
async def test_unsupported_strategy_with_valid_binding_never_authorizes(
    db_session: AsyncSession, org_a, strategy: str, threshold: int | None
) -> None:
    org, membership = org_a
    authority = await _make_authority(
        db_session, org.id, approval_strategy=strategy, majority_threshold_pct=threshold
    )
    await _bind(db_session, membership.id, authority.id)

    result = await resolve_approval_authority(
        db_session, org.id, AUTHORITY_NAME, org.id, membership.id
    )
    assert result == ApprovalAuthorityResolution.UNSUPPORTED_STRATEGY
    assert result != ApprovalAuthorityResolution.AUTHORIZED


# ---------------------------------------------------------------------------
# 8. Organization mismatch -> INVALID_SCOPE (CLAUDE.md §21.4(b))
# ---------------------------------------------------------------------------

async def test_organization_mismatch_denies(db_session: AsyncSession, org_a, org_b) -> None:
    org_a_row, _membership_a = org_a
    org_b_row, membership_b = org_b
    authority = await _make_authority(db_session, org_a_row.id, approval_strategy="ANY_ONE")
    # membership_b is bound to org_a's own authority (hypothetically) -- but
    # the caller's own claimed organization is org_b, which must not match
    # org_a's target -- denied at step 4, before the binding is even consulted.
    await _bind(db_session, membership_b.id, authority.id)

    result = await resolve_approval_authority(
        db_session, org_a_row.id, AUTHORITY_NAME, org_b_row.id, membership_b.id
    )
    assert result == ApprovalAuthorityResolution.INVALID_SCOPE


# ---------------------------------------------------------------------------
# 9. inactive Membership -> INACTIVE_MEMBERSHIP
# ---------------------------------------------------------------------------

async def test_inactive_membership_denies(db_session: AsyncSession, org_a) -> None:
    org, membership = org_a
    membership.membership_status = "SUSPENDED"
    await db_session.flush()
    authority = await _make_authority(db_session, org.id, approval_strategy="ANY_ONE")
    await _bind(db_session, membership.id, authority.id)

    result = await resolve_approval_authority(
        db_session, org.id, AUTHORITY_NAME, org.id, membership.id
    )
    assert result == ApprovalAuthorityResolution.INACTIVE_MEMBERSHIP


# ---------------------------------------------------------------------------
# 10. missing effective binding -> NO_ELIGIBLE_ACTOR
# ---------------------------------------------------------------------------

async def test_missing_binding_denies(db_session: AsyncSession, org_a) -> None:
    org, membership = org_a
    await _make_authority(db_session, org.id, approval_strategy="ANY_ONE")
    # No binding ever created for this membership.
    authority = await _make_authority(
        db_session, org.id, approval_strategy="ANY_ONE", authority_name="Another Authority"
    )

    result = await resolve_approval_authority(
        db_session, org.id, "Another Authority", org.id, membership.id
    )
    assert result == ApprovalAuthorityResolution.NO_ELIGIBLE_ACTOR


# ---------------------------------------------------------------------------
# 11. cross-Organization binding attempt (foreign identifier probe,
#     CLAUDE.md §21.4(c)) -- a membership from Org A cannot resolve an
#     authority belonging to Org B even when the resolver is explicitly
#     asked to resolve against Org B's own id as target
# ---------------------------------------------------------------------------

async def test_cross_organization_binding_attempt_rejected(db_session: AsyncSession, org_a, org_b) -> None:
    org_a_row, membership_a = org_a
    org_b_row, _membership_b = org_b
    authority_b = await _make_authority(db_session, org_b_row.id, approval_strategy="ANY_ONE")

    # membership_a claims org_a as its own organization -- targeting org_b's
    # authority as the caller's own org must be denied at step 4 (INVALID_SCOPE),
    # never reaching a binding lookup that could leak org_b's own data.
    result = await resolve_approval_authority(
        db_session, org_b_row.id, AUTHORITY_NAME, org_a_row.id, membership_a.id
    )
    assert result == ApprovalAuthorityResolution.INVALID_SCOPE


# ---------------------------------------------------------------------------
# 12. effective-date boundary cases
# ---------------------------------------------------------------------------

async def test_binding_not_yet_effective_denies(db_session: AsyncSession, org_a) -> None:
    org, membership = org_a
    authority = await _make_authority(db_session, org.id, approval_strategy="ANY_ONE")
    future = datetime.now(timezone.utc) + timedelta(days=1)
    await _bind(db_session, membership.id, authority.id, effective_from=future)

    result = await resolve_approval_authority(
        db_session, org.id, AUTHORITY_NAME, org.id, membership.id
    )
    assert result == ApprovalAuthorityResolution.NO_ELIGIBLE_ACTOR


async def test_binding_already_expired_denies(db_session: AsyncSession, org_a) -> None:
    org, membership = org_a
    authority = await _make_authority(db_session, org.id, approval_strategy="ANY_ONE")
    past_start = datetime.now(timezone.utc) - timedelta(days=10)
    past_end = datetime.now(timezone.utc) - timedelta(days=1)
    await _bind(db_session, membership.id, authority.id, effective_from=past_start, effective_to=past_end)

    result = await resolve_approval_authority(
        db_session, org.id, AUTHORITY_NAME, org.id, membership.id
    )
    assert result == ApprovalAuthorityResolution.NO_ELIGIBLE_ACTOR


async def test_binding_open_ended_and_currently_effective_authorizes(db_session: AsyncSession, org_a) -> None:
    org, membership = org_a
    authority = await _make_authority(db_session, org.id, approval_strategy="ANY_ONE")
    past_start = datetime.now(timezone.utc) - timedelta(days=1)
    await _bind(db_session, membership.id, authority.id, effective_from=past_start, effective_to=None)

    result = await resolve_approval_authority(
        db_session, org.id, AUTHORITY_NAME, org.id, membership.id
    )
    assert result == ApprovalAuthorityResolution.AUTHORIZED


# ---------------------------------------------------------------------------
# 13. no eligible actor at all (authority exists, ACTIVE, but zero bindings
#     anywhere) is distinct from "no authority configured"
# ---------------------------------------------------------------------------

async def test_authority_exists_but_zero_bindings_is_no_eligible_actor_not_no_authority(
    db_session: AsyncSession, org_a
) -> None:
    org, membership = org_a
    await _make_authority(db_session, org.id, approval_strategy="ANY_ONE")

    result = await resolve_approval_authority(
        db_session, org.id, AUTHORITY_NAME, org.id, membership.id
    )
    assert result == ApprovalAuthorityResolution.NO_ELIGIBLE_ACTOR


# ---------------------------------------------------------------------------
# 14. audit behavior -- every outcome (ALLOW and DENY) is audited
# ---------------------------------------------------------------------------

async def test_authorized_outcome_is_audited(db_session: AsyncSession, org_a, monkeypatch) -> None:
    org, membership = org_a
    authority = await _make_authority(db_session, org.id, approval_strategy="ANY_ONE")
    await _bind(db_session, membership.id, authority.id)

    calls = []
    monkeypatch.setattr(
        "services.approval_authority_resolver.record_audit",
        lambda **kwargs: calls.append(kwargs),
    )

    result = await resolve_approval_authority(db_session, org.id, AUTHORITY_NAME, org.id, membership.id)

    assert result == ApprovalAuthorityResolution.AUTHORIZED
    assert len(calls) == 1
    assert calls[0]["action"] == "RESOLVE_APPROVAL_AUTHORITY"
    assert calls[0]["status"].value == "SUCCESS"


async def test_denied_outcome_is_audited_with_reason(db_session: AsyncSession, org_a, monkeypatch) -> None:
    org, membership = org_a

    calls = []
    monkeypatch.setattr(
        "services.approval_authority_resolver.record_audit",
        lambda **kwargs: calls.append(kwargs),
    )

    result = await resolve_approval_authority(db_session, org.id, AUTHORITY_NAME, org.id, membership.id)

    assert result == ApprovalAuthorityResolution.NO_AUTHORITY_CONFIGURED
    assert len(calls) == 1
    assert calls[0]["status"].value == "DENIED"
    assert calls[0]["metadata"]["reason"] == "NO_AUTHORITY_CONFIGURED"


# ---------------------------------------------------------------------------
# 15. PLATFORM_ADMIN / AUREX_ADMIN are not implicit substitutes at the
#     dependency layer (mirrors test_authority_holder.py's own precedent)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("role_code", ["PLATFORM_ADMIN", "AUREX_ADMIN"])
async def test_admin_role_does_not_bypass_approval_authority_gate(
    db_session: AsyncSession, org_a, role_code: str
) -> None:
    org, membership = org_a
    await _make_authority(db_session, org.id, approval_strategy="ANY_ONE")
    # No binding created for this caller -- an admin role must not substitute for one.

    claims = {
        "person_id": str(uuid.uuid4()),
        "organization_id": str(org.id),
        "membership_id": str(membership.id),
        "role_code": role_code,
    }
    with pytest.raises(HTTPException) as exc_info:
        await enforce_approval_authority(claims, db_session, org.id, AUTHORITY_NAME)
    assert exc_info.value.status_code == 403


async def test_missing_claims_denies_closed(db_session: AsyncSession, org_a) -> None:
    """No person_id/organization_id/membership_id in claims -- fails closed, never simulated."""
    org, _membership = org_a
    await _make_authority(db_session, org.id, approval_strategy="ANY_ONE")

    claims: dict = {}
    with pytest.raises(HTTPException) as exc_info:
        await enforce_approval_authority(claims, db_session, org.id, AUTHORITY_NAME)
    assert exc_info.value.status_code == 403
