"""
WP-09 BA-02 — Detect and Resolve Disrupted Workspace Context
(EX-C008-10, PE-001-C008 v1.3/ERB-C008-06).
Service-layer tests for WorkspaceStatusService.refresh() — mirrors
test_identity_service.py's own BA-01 (IdentityStatusService.refresh())
test shape exactly.
"""
import uuid

import pytest
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
from schemas.workspace import WorkspaceContextStatus
from services.membership_service import MembershipService
from services.workspace_status_service import WorkspaceStatusService


@pytest.fixture
async def seeded_person_organization_role(db_session: AsyncSession) -> tuple[Person, Organization, Role]:
    person = Person(first_name="Priya", last_name="Menon", display_name="Priya Menon")
    organization = Organization(
        organization_code="WS_STATUS_TEST_ORG", organization_name="Workspace Status Test Org", organization_type="CORPORATE",
    )
    role = Role(role_code="WS_STATUS_TEST_ROLE", role_name="Workspace Status Test Role")
    db_session.add_all([person, organization, role])
    await db_session.flush()
    return person, organization, role


def _status_service(session: AsyncSession) -> WorkspaceStatusService:
    return WorkspaceStatusService(MembershipRepository(session), OrganizationNodeRepository(session))


def _membership_service(session: AsyncSession) -> MembershipService:
    return MembershipService(
        MembershipRepository(session),
        PersonRepository(session),
        OrganizationRepository(session),
        RoleRepository(session),
        OrganizationNodeRepository(session),
    )


async def test_refresh_status_current_for_active_membership(
    db_session: AsyncSession, seeded_person_organization_role
) -> None:
    person, organization, role = seeded_person_organization_role
    membership_service = _membership_service(db_session)
    established = await membership_service.establish(
        EstablishMembershipRequest(person_id=person.id, organization_id=organization.id, role_id=role.id)
    )

    result = await _status_service(db_session).refresh(established.id, organization.id)

    assert result.status == WorkspaceContextStatus.CURRENT
    assert result.membership_id == established.id
    assert result.organization_id == organization.id


async def test_refresh_status_unresolved_for_suspended_membership(
    db_session: AsyncSession, seeded_person_organization_role
) -> None:
    person, organization, role = seeded_person_organization_role
    membership_service = _membership_service(db_session)
    established = await membership_service.establish(
        EstablishMembershipRequest(person_id=person.id, organization_id=organization.id, role_id=role.id)
    )
    established.membership_status = "SUSPENDED"
    await db_session.flush()

    result = await _status_service(db_session).refresh(established.id, organization.id)

    assert result.status == WorkspaceContextStatus.UNRESOLVED


async def test_refresh_status_unresolved_for_removed_membership_not_404(
    db_session: AsyncSession, seeded_person_organization_role
) -> None:
    """
    IRA-009 §5's own testing note: 'deactivated/removed Membership ->
    UNRESOLVED', distinct from IdentityStatusService.refresh()'s own
    404-on-unknown-id precedent — detecting exactly this disruption is
    this Business Activity's own purpose, not an exceptional case.
    """
    _person, organization, _role = seeded_person_organization_role
    unknown_membership_id = uuid.uuid4()

    result = await _status_service(db_session).refresh(unknown_membership_id, organization.id)

    assert result.status == WorkspaceContextStatus.UNRESOLVED
    assert result.membership_id == unknown_membership_id
    assert result.organization_id == organization.id


async def test_refresh_status_current_when_home_node_absent(
    db_session: AsyncSession, seeded_person_organization_role
) -> None:
    """TD-032: home_node_id is optional and, in practice, always None today — nothing to invalidate."""
    person, organization, role = seeded_person_organization_role
    membership_service = _membership_service(db_session)
    established = await membership_service.establish(
        EstablishMembershipRequest(person_id=person.id, organization_id=organization.id, role_id=role.id)
    )

    result = await _status_service(db_session).refresh(established.id, organization.id)

    assert result.status == WorkspaceContextStatus.CURRENT


async def test_refresh_status_current_when_home_node_active(
    db_session: AsyncSession, seeded_person_organization_role
) -> None:
    person, organization, role = seeded_person_organization_role
    node = OrganizationNode(
        node_code="WS_STATUS_NODE_ACTIVE", node_name="Active Node", node_type="ENTITY", active_flag=True,
    )
    db_session.add(node)
    await db_session.flush()
    membership_service = _membership_service(db_session)
    established = await membership_service.establish(
        EstablishMembershipRequest(
            person_id=person.id, organization_id=organization.id, role_id=role.id, home_node_id=node.id
        )
    )

    result = await _status_service(db_session).refresh(established.id, organization.id)

    assert result.status == WorkspaceContextStatus.CURRENT


async def test_refresh_status_unresolved_when_home_node_inactive(
    db_session: AsyncSession, seeded_person_organization_role
) -> None:
    person, organization, role = seeded_person_organization_role
    node = OrganizationNode(
        node_code="WS_STATUS_NODE_INACTIVE", node_name="Inactive Node", node_type="ENTITY", active_flag=True,
    )
    db_session.add(node)
    await db_session.flush()
    membership_service = _membership_service(db_session)
    established = await membership_service.establish(
        EstablishMembershipRequest(
            person_id=person.id, organization_id=organization.id, role_id=role.id, home_node_id=node.id
        )
    )
    node.active_flag = False
    await db_session.flush()

    result = await _status_service(db_session).refresh(established.id, organization.id)

    assert result.status == WorkspaceContextStatus.UNRESOLVED
