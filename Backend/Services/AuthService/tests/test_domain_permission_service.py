import uuid

import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.domain import Domain
from models.membership import Membership
from models.organization import Organization
from models.person import Person
from models.role import Role
from repositories.domain_permission_repository import DomainPermissionRepository
from repositories.domain_repository import DomainRepository
from repositories.membership_repository import MembershipRepository
from schemas.domain_permission import EstablishDomainPermissionRequest
from services.domain_permission_service import DomainPermissionService


@pytest.fixture
async def seeded_membership_and_domain(db_session: AsyncSession) -> tuple[Membership, Domain, Role]:
    """Seeds one Person -> Organization -> Role -> Membership chain, plus one Domain."""
    person = Person(first_name="Dom", last_name="Owner", display_name="Dom Owner")
    organization = Organization(
        organization_code="DP-TEST-ORG",
        organization_name="Domain Permission Test Org",
        organization_type="CORPORATE",
    )
    role = Role(role_code="DP_TEST_ROLE", role_name="Domain Permission Test Role")
    db_session.add_all([person, organization, role])
    await db_session.flush()

    membership = Membership(
        person_id=person.id,
        organization_id=organization.id,
        role_id=role.id,
    )
    domain = Domain(domain_name="Finance")
    db_session.add_all([membership, domain])
    await db_session.flush()

    return membership, domain, role


def _service(session: AsyncSession) -> DomainPermissionService:
    return DomainPermissionService(
        DomainPermissionRepository(session),
        DomainRepository(session),
        MembershipRepository(session),
    )


async def test_establish_creates_domain_permission(
    db_session: AsyncSession, seeded_membership_and_domain
) -> None:
    """BA-02/EX-C003-02: a first-time Establish Domain Permission call creates exactly one row."""
    membership, domain, _role = seeded_membership_and_domain
    service = _service(db_session)
    request = EstablishDomainPermissionRequest(
        membership_id=membership.id,
        domain_id=domain.id,
        permission_level="APPROVE",
    )

    grant = await service.establish(request, actor_id="platform-admin-1")

    assert grant.membership_id == membership.id
    assert grant.domain_id == domain.id
    assert grant.permission_level == "APPROVE"
    assert grant.effective_to is None
    assert grant.id is not None


async def test_establish_rejects_unknown_domain(
    db_session: AsyncSession, seeded_membership_and_domain
) -> None:
    """EX-C003-02 Entry Context: the target Domain must already be established."""
    membership, _domain, _role = seeded_membership_and_domain
    service = _service(db_session)
    request = EstablishDomainPermissionRequest(
        membership_id=membership.id,
        domain_id=uuid.uuid4(),
        permission_level="VIEW",
    )

    with pytest.raises(HTTPException) as exc_info:
        await service.establish(request)

    assert exc_info.value.status_code == 404


async def test_establish_rejects_unknown_membership(
    db_session: AsyncSession, seeded_membership_and_domain
) -> None:
    _membership, domain, _role = seeded_membership_and_domain
    service = _service(db_session)
    request = EstablishDomainPermissionRequest(
        membership_id=uuid.uuid4(),
        domain_id=domain.id,
        permission_level="VIEW",
    )

    with pytest.raises(HTTPException) as exc_info:
        await service.establish(request)

    assert exc_info.value.status_code == 404


async def test_establish_rejects_duplicate_active_grant(
    db_session: AsyncSession, seeded_membership_and_domain
) -> None:
    """
    BR-C003-01's structural-rule discipline: establishing the same
    (membership, domain, permission_level) triple twice while the first
    grant is still active is rejected (409), naming the specific
    violated rule, mirroring OrganizationService.establish()'s and
    RoleService.establish()'s duplicate-prevention precedent.
    """
    membership, domain, _role = seeded_membership_and_domain
    service = _service(db_session)
    request = EstablishDomainPermissionRequest(
        membership_id=membership.id,
        domain_id=domain.id,
        permission_level="EDIT",
    )

    await service.establish(request)

    with pytest.raises(HTTPException) as exc_info:
        await service.establish(request)

    assert exc_info.value.status_code == 409


async def test_establish_allows_different_permission_levels_on_same_domain(
    db_session: AsyncSession, seeded_membership_and_domain
) -> None:
    """Two distinct permission_level grants for the same membership/domain pair are both valid."""
    membership, domain, _role = seeded_membership_and_domain
    service = _service(db_session)

    view_grant = await service.establish(
        EstablishDomainPermissionRequest(
            membership_id=membership.id, domain_id=domain.id, permission_level="VIEW"
        )
    )
    approve_grant = await service.establish(
        EstablishDomainPermissionRequest(
            membership_id=membership.id, domain_id=domain.id, permission_level="APPROVE"
        )
    )

    assert view_grant.id != approve_grant.id


async def test_establish_never_touches_role_permissions(
    db_session: AsyncSession, seeded_membership_and_domain
) -> None:
    """
    BR-C003-02: a Domain Permission is never an implicit consequence of a
    Business Role — establishing one must not create or modify any
    role_permissions row.
    """
    membership, domain, role = seeded_membership_and_domain
    service = _service(db_session)
    request = EstablishDomainPermissionRequest(
        membership_id=membership.id, domain_id=domain.id, permission_level="ADMIN"
    )

    await service.establish(request)
    await db_session.refresh(role, attribute_names=["role_permissions"])

    assert role.role_permissions == []
