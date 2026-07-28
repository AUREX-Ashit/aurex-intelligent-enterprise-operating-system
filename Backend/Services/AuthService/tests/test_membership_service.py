"""
WP-03 BA-01 — Establish Membership Context (ERB-C007-01 / EX-C007-01 +
EX-C007-02 per PE-001-C007). Service-layer tests for
MembershipService.establish(), covering BR-C007-001 (recognition
before establishment), BR-C007-002/007 (home-node candidate validity),
and the referenced-object existence checks (Person/Organization/Role).
"""
import uuid

import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.organization import Organization
from models.organization_node import OrganizationNode
from models.person import Person
from models.role import Role
from repositories.membership_repository import MembershipRepository
from repositories.organization_node_repository import OrganizationNodeRepository
from repositories.organization_repository import OrganizationRepository
from repositories.person_repository import PersonRepository
from repositories.role_repository import RoleRepository
from schemas.membership import EstablishMembershipRequest
from services.membership_service import MembershipService


@pytest.fixture
async def seeded_person_organization_role(db_session: AsyncSession) -> tuple[Person, Organization, Role]:
    person = Person(first_name="Ada", last_name="Lovelace", display_name="Ada Lovelace")
    organization = Organization(
        organization_code="MEM_TEST_ORG", organization_name="Membership Test Org", organization_type="CORPORATE",
    )
    role = Role(role_code="MEM_TEST_ROLE", role_name="Membership Test Role")
    db_session.add_all([person, organization, role])
    await db_session.flush()
    return person, organization, role


def _service(session: AsyncSession) -> MembershipService:
    return MembershipService(
        MembershipRepository(session),
        PersonRepository(session),
        OrganizationRepository(session),
        RoleRepository(session),
        OrganizationNodeRepository(session),
    )


async def test_establish_creates_membership(
    db_session: AsyncSession, seeded_person_organization_role
) -> None:
    """BA-01/EX-C007-02: a first-time Establish call creates exactly one row, ACTIVE by default."""
    person, organization, role = seeded_person_organization_role
    service = _service(db_session)
    request = EstablishMembershipRequest(
        person_id=person.id, organization_id=organization.id, role_id=role.id,
    )

    membership = await service.establish(request, actor_id="platform-admin-1")

    assert membership.id is not None
    assert membership.person_id == person.id
    assert membership.organization_id == organization.id
    assert membership.role_id == role.id
    assert membership.home_node_id is None
    assert membership.membership_type == "INTERNAL"
    assert membership.license_type == "FULL"
    assert membership.membership_status == "ACTIVE"
    assert membership.effective_from is not None
    assert membership.effective_to is None


async def test_establish_rejects_duplicate_membership(
    db_session: AsyncSession, seeded_person_organization_role
) -> None:
    """BR-C007-001: a second establish for the same (person, organization) pair is rejected with 409."""
    person, organization, role = seeded_person_organization_role
    service = _service(db_session)
    request = EstablishMembershipRequest(person_id=person.id, organization_id=organization.id, role_id=role.id)
    await service.establish(request)

    with pytest.raises(HTTPException) as exc_info:
        await service.establish(request)
    assert exc_info.value.status_code == 409


async def test_establish_rejects_unknown_person(db_session: AsyncSession, seeded_person_organization_role) -> None:
    _person, organization, role = seeded_person_organization_role
    service = _service(db_session)
    request = EstablishMembershipRequest(person_id=uuid.uuid4(), organization_id=organization.id, role_id=role.id)

    with pytest.raises(HTTPException) as exc_info:
        await service.establish(request)
    assert exc_info.value.status_code == 404


async def test_establish_rejects_unknown_organization(db_session: AsyncSession, seeded_person_organization_role) -> None:
    person, _organization, role = seeded_person_organization_role
    service = _service(db_session)
    request = EstablishMembershipRequest(person_id=person.id, organization_id=uuid.uuid4(), role_id=role.id)

    with pytest.raises(HTTPException) as exc_info:
        await service.establish(request)
    assert exc_info.value.status_code == 404


async def test_establish_rejects_unknown_role(db_session: AsyncSession, seeded_person_organization_role) -> None:
    person, organization, _role = seeded_person_organization_role
    service = _service(db_session)
    request = EstablishMembershipRequest(person_id=person.id, organization_id=organization.id, role_id=uuid.uuid4())

    with pytest.raises(HTTPException) as exc_info:
        await service.establish(request)
    assert exc_info.value.status_code == 404


async def test_establish_accepts_confirmed_active_home_node(
    db_session: AsyncSession, seeded_person_organization_role
) -> None:
    """BR-C007-002/007: a supplied home_node_id that resolves to a real, active node is accepted and persisted."""
    person, organization, role = seeded_person_organization_role
    node = OrganizationNode(node_code="NODE-001", node_name="Test Node", node_type="entity")
    db_session.add(node)
    await db_session.flush()

    service = _service(db_session)
    request = EstablishMembershipRequest(
        person_id=person.id, organization_id=organization.id, role_id=role.id, home_node_id=node.id,
    )
    membership = await service.establish(request)

    assert membership.home_node_id == node.id


async def test_establish_rejects_unknown_home_node(db_session: AsyncSession, seeded_person_organization_role) -> None:
    person, organization, role = seeded_person_organization_role
    service = _service(db_session)
    request = EstablishMembershipRequest(
        person_id=person.id, organization_id=organization.id, role_id=role.id, home_node_id=uuid.uuid4(),
    )

    with pytest.raises(HTTPException) as exc_info:
        await service.establish(request)
    assert exc_info.value.status_code == 404


async def test_establish_rejects_inactive_home_node(db_session: AsyncSession, seeded_person_organization_role) -> None:
    """BR-C007-002: a candidate home-node context that is not active is not authoritative."""
    person, organization, role = seeded_person_organization_role
    node = OrganizationNode(node_code="NODE-INACTIVE", node_name="Inactive Node", node_type="entity", active_flag=False)
    db_session.add(node)
    await db_session.flush()

    service = _service(db_session)
    request = EstablishMembershipRequest(
        person_id=person.id, organization_id=organization.id, role_id=role.id, home_node_id=node.id,
    )

    with pytest.raises(HTTPException) as exc_info:
        await service.establish(request)
    assert exc_info.value.status_code == 409


async def test_establish_accepts_explicit_membership_and_license_type(
    db_session: AsyncSession, seeded_person_organization_role
) -> None:
    """EX-C007-02 Success Criteria: explicit membership_type and license_type are honored, not defaulted silently when supplied."""
    person, organization, role = seeded_person_organization_role
    service = _service(db_session)
    request = EstablishMembershipRequest(
        person_id=person.id, organization_id=organization.id, role_id=role.id,
        membership_type="EXTERNAL", license_type="LIGHT",
    )

    membership = await service.establish(request)

    assert membership.membership_type == "EXTERNAL"
    assert membership.license_type == "LIGHT"
