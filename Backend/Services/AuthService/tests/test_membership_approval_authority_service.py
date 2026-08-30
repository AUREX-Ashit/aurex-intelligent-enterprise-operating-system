"""
WP-18 (C-003, TDS-018 §5-§7/§19) — `MembershipApprovalAuthorityService`
bind/close tests, including the cross-Organization bind-time guard
(TDS-018 §7's own disclosed gap, closed here at the service layer) and
idempotent-conflict behavior for a duplicate bind attempt.
"""

import uuid

import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.approval_authority import ApprovalAuthority
from models.membership import Membership
from models.organization import Organization
from models.person import Person
from models.role import Role
from repositories.approval_authority_repository import ApprovalAuthorityRepository
from repositories.membership_approval_authority_repository import MembershipApprovalAuthorityRepository
from repositories.membership_repository import MembershipRepository
from services.membership_approval_authority_service import MembershipApprovalAuthorityService


def _service(session: AsyncSession) -> MembershipApprovalAuthorityService:
    return MembershipApprovalAuthorityService(
        MembershipApprovalAuthorityRepository(session),
        MembershipRepository(session),
        ApprovalAuthorityRepository(session),
    )


async def _make_org_membership(db_session: AsyncSession, org_code: str) -> tuple[Organization, Membership]:
    role = Role(role_code=f"{org_code}_ROLE", role_name=f"{org_code} Role")
    org = Organization(organization_code=org_code, organization_name=org_code, organization_type="CORPORATE")
    person = Person(first_name=org_code, last_name="Test", display_name=f"{org_code} Test")
    db_session.add_all([role, org, person])
    await db_session.flush()

    membership = Membership(person_id=person.id, organization_id=org.id, role_id=role.id)
    db_session.add(membership)
    await db_session.flush()
    return org, membership


async def _make_authority(db_session: AsyncSession, organization_id: uuid.UUID) -> ApprovalAuthority:
    authority = ApprovalAuthority(
        organization_id=organization_id,
        authority_name="Bind Test Authority",
        approval_strategy="ANY_ONE",
        scope_type="COMPANY",
    )
    db_session.add(authority)
    await db_session.flush()
    return authority


@pytest.fixture
async def org_a(db_session: AsyncSession):
    return await _make_org_membership(db_session, "BIND-ORG-A")


@pytest.fixture
async def org_b(db_session: AsyncSession):
    return await _make_org_membership(db_session, "BIND-ORG-B")


# ---------------------------------------------------------------------------
# bind() success
# ---------------------------------------------------------------------------

async def test_bind_succeeds_same_organization(db_session: AsyncSession, org_a) -> None:
    org, membership = org_a
    authority = await _make_authority(db_session, org.id)
    service = _service(db_session)

    binding = await service.bind(membership.id, authority.id, actor_id="test-actor")

    assert binding.membership_id == membership.id
    assert binding.approval_authority_id == authority.id
    assert binding.effective_to is None


# ---------------------------------------------------------------------------
# bind() -- missing Membership / missing Approval Authority
# ---------------------------------------------------------------------------

async def test_bind_missing_membership_404(db_session: AsyncSession, org_a) -> None:
    org, _membership = org_a
    authority = await _make_authority(db_session, org.id)
    service = _service(db_session)

    with pytest.raises(HTTPException) as exc_info:
        await service.bind(uuid.uuid4(), authority.id)
    assert exc_info.value.status_code == 404


async def test_bind_missing_authority_404(db_session: AsyncSession, org_a) -> None:
    _org, membership = org_a
    service = _service(db_session)

    with pytest.raises(HTTPException) as exc_info:
        await service.bind(membership.id, uuid.uuid4())
    assert exc_info.value.status_code == 404


# ---------------------------------------------------------------------------
# bind() -- cross-Organization rejection (TDS-018 §7/§19's own disclosed gap,
# closed here; CLAUDE.md §21.4's own foreign-identifier probe)
# ---------------------------------------------------------------------------

async def test_bind_cross_organization_rejected(db_session: AsyncSession, org_a, org_b) -> None:
    org_a_row, membership_a = org_a
    org_b_row, _membership_b = org_b
    authority_b = await _make_authority(db_session, org_b_row.id)
    service = _service(db_session)

    with pytest.raises(HTTPException) as exc_info:
        await service.bind(membership_a.id, authority_b.id)
    assert exc_info.value.status_code == 409

    # Confirm no row was actually created despite the attempt.
    binding_repo = MembershipApprovalAuthorityRepository(db_session)
    assert await binding_repo.get_open_binding(membership_a.id, authority_b.id) is None


# ---------------------------------------------------------------------------
# bind() -- idempotent-conflict: a second bind for an already-open pair is
# rejected (409), never silently duplicated
# ---------------------------------------------------------------------------

async def test_bind_duplicate_pair_rejected_not_silently_duplicated(db_session: AsyncSession, org_a) -> None:
    org, membership = org_a
    authority = await _make_authority(db_session, org.id)
    service = _service(db_session)

    first = await service.bind(membership.id, authority.id)
    assert first is not None

    with pytest.raises(HTTPException) as exc_info:
        await service.bind(membership.id, authority.id)
    assert exc_info.value.status_code == 409


# ---------------------------------------------------------------------------
# close() success and re-bind after close
# ---------------------------------------------------------------------------

async def test_close_deactivates_binding_without_deleting(db_session: AsyncSession, org_a) -> None:
    org, membership = org_a
    authority = await _make_authority(db_session, org.id)
    service = _service(db_session)

    await service.bind(membership.id, authority.id)
    closed = await service.close(membership.id, authority.id)

    assert closed.effective_to is not None

    binding_repo = MembershipApprovalAuthorityRepository(db_session)
    assert await binding_repo.get_open_binding(membership.id, authority.id) is None

    # The row itself still exists (soft-close, never a hard delete).
    from sqlalchemy import select
    from models.membership_approval_authority import MembershipApprovalAuthority

    result = await db_session.execute(
        select(MembershipApprovalAuthority).where(
            MembershipApprovalAuthority.membership_id == membership.id,
            MembershipApprovalAuthority.approval_authority_id == authority.id,
        )
    )
    assert result.scalars().first() is not None


async def test_close_missing_open_binding_404(db_session: AsyncSession, org_a) -> None:
    org, membership = org_a
    authority = await _make_authority(db_session, org.id)
    service = _service(db_session)

    with pytest.raises(HTTPException) as exc_info:
        await service.close(membership.id, authority.id)
    assert exc_info.value.status_code == 404


async def test_rebind_after_close_succeeds(db_session: AsyncSession, org_a) -> None:
    org, membership = org_a
    authority = await _make_authority(db_session, org.id)
    service = _service(db_session)

    await service.bind(membership.id, authority.id)
    await service.close(membership.id, authority.id)

    second = await service.bind(membership.id, authority.id)
    assert second.effective_to is None
