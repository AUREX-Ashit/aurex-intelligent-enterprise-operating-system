"""
WP-09 BA-01 — Resolve and Present Available Workspace Candidates
(EX-C008-01/02, PE-001-C008 v1.3/ERB-C008-01).
Service-layer tests for WorkspaceResolutionService.resolve_candidates()
— reuses MembershipRepository.get_person_memberships() (the same
repository method MembershipService.present_own_portfolio() already
uses), so the ACTIVE-only filter and cross-organization behavior are
inherited from that already-tested method, not re-derived here.
"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from models.organization import Organization
from models.person import Person
from models.role import Role
from repositories.membership_repository import MembershipRepository
from repositories.organization_node_repository import OrganizationNodeRepository
from repositories.organization_repository import OrganizationRepository
from repositories.person_repository import PersonRepository
from repositories.role_repository import RoleRepository
from schemas.membership import EstablishMembershipRequest
from services.membership_service import MembershipService
from services.workspace_resolution_service import WorkspaceResolutionService


@pytest.fixture
async def seeded_person_organization_role(db_session: AsyncSession) -> tuple[Person, Organization, Role]:
    person = Person(first_name="Wren", last_name="Okafor", display_name="Wren Okafor")
    organization = Organization(
        organization_code="WS_TEST_ORG", organization_name="Workspace Test Org", organization_type="CORPORATE",
    )
    role = Role(role_code="WS_TEST_ROLE", role_name="Workspace Test Role")
    db_session.add_all([person, organization, role])
    await db_session.flush()
    return person, organization, role


def _resolution_service(session: AsyncSession) -> WorkspaceResolutionService:
    return WorkspaceResolutionService(MembershipRepository(session))


def _membership_service(session: AsyncSession) -> MembershipService:
    return MembershipService(
        MembershipRepository(session),
        PersonRepository(session),
        OrganizationRepository(session),
        RoleRepository(session),
        OrganizationNodeRepository(session),
    )


async def test_resolve_candidates_returns_empty_list_when_no_memberships(
    db_session: AsyncSession, seeded_person_organization_role
) -> None:
    person, _organization, _role = seeded_person_organization_role
    service = _resolution_service(db_session)

    result = await service.resolve_candidates(person.id)

    assert result.candidates == []


async def test_resolve_candidates_returns_one_candidate_per_active_membership(
    db_session: AsyncSession, seeded_person_organization_role
) -> None:
    person, organization, role = seeded_person_organization_role
    membership_service = _membership_service(db_session)
    established = await membership_service.establish(
        EstablishMembershipRequest(
            person_id=person.id, organization_id=organization.id, role_id=role.id, is_primary=True
        )
    )

    result = await _resolution_service(db_session).resolve_candidates(person.id)

    assert len(result.candidates) == 1
    candidate = result.candidates[0]
    assert candidate.membership_id == established.id
    assert candidate.organization_id == organization.id
    assert candidate.organization_name == organization.organization_name
    assert candidate.role_code == role.role_code
    assert candidate.role_name == role.role_name
    assert candidate.is_primary is True


async def test_resolve_candidates_spans_multiple_organizations(
    db_session: AsyncSession, seeded_person_organization_role
) -> None:
    person, organization, role = seeded_person_organization_role
    other_organization = Organization(
        organization_code="WS_TEST_ORG_OTHER", organization_name="Workspace Test Org Other", organization_type="CORPORATE",
    )
    db_session.add(other_organization)
    await db_session.flush()
    membership_service = _membership_service(db_session)
    await membership_service.establish(
        EstablishMembershipRequest(person_id=person.id, organization_id=organization.id, role_id=role.id)
    )
    await membership_service.establish(
        EstablishMembershipRequest(person_id=person.id, organization_id=other_organization.id, role_id=role.id)
    )

    result = await _resolution_service(db_session).resolve_candidates(person.id)

    returned_org_ids = {c.organization_id for c in result.candidates}
    assert returned_org_ids == {organization.id, other_organization.id}


async def test_resolve_candidates_excludes_non_active_memberships(
    db_session: AsyncSession, seeded_person_organization_role
) -> None:
    person, organization, role = seeded_person_organization_role
    membership_service = _membership_service(db_session)
    established = await membership_service.establish(
        EstablishMembershipRequest(person_id=person.id, organization_id=organization.id, role_id=role.id)
    )
    established.membership_status = "SUSPENDED"
    await db_session.flush()

    result = await _resolution_service(db_session).resolve_candidates(person.id)

    assert result.candidates == []


async def test_resolve_candidates_only_returns_the_supplied_persons_own_memberships(
    db_session: AsyncSession, seeded_person_organization_role
) -> None:
    person, organization, role = seeded_person_organization_role
    other_person = Person(first_name="Other", last_name="Person", display_name="Other Person")
    db_session.add(other_person)
    await db_session.flush()
    membership_service = _membership_service(db_session)
    await membership_service.establish(
        EstablishMembershipRequest(person_id=person.id, organization_id=organization.id, role_id=role.id)
    )

    result = await _resolution_service(db_session).resolve_candidates(other_person.id)

    assert result.candidates == []


async def test_resolve_candidates_exposes_home_node_id_as_structural_anchor_only(
    db_session: AsyncSession, seeded_person_organization_role
) -> None:
    """
    BR-C008-01a: candidates are keyed to their structural anchor only —
    this service never determines which PE-001 §13.5 Workspace Type(s)
    the anchor may host. home_node_id is nullable per TD-032 (no
    Business Activity anywhere establishes an OrganizationNode row
    today), so it is expected to be None here, not fabricated.
    """
    person, organization, role = seeded_person_organization_role
    membership_service = _membership_service(db_session)
    await membership_service.establish(
        EstablishMembershipRequest(person_id=person.id, organization_id=organization.id, role_id=role.id)
    )

    result = await _resolution_service(db_session).resolve_candidates(person.id)

    assert result.candidates[0].home_node_id is None
