"""
WP-09 BA-03 — Classify Workspace Hand-off Rejection (EX-C008-11,
PE-001-C008 v1.3/ERB-C008-06/BR-C008-06).
Service-layer tests for WorkspaceHandoffClassificationService.classify()
— mirrors test_identity_service.py's own BA-03 test shape exactly.
"""
import uuid

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
from schemas.workspace import ClassifyWorkspaceHandoffRejectionRequest, WorkspaceHandoffClassification
from services.membership_service import MembershipService
from services.workspace_handoff_classification_service import WorkspaceHandoffClassificationService
from services.workspace_status_service import WorkspaceStatusService


@pytest.fixture
async def seeded_person_organization_role(db_session: AsyncSession) -> tuple[Person, Organization, Role]:
    person = Person(first_name="Tomas", last_name="Rivera", display_name="Tomas Rivera")
    organization = Organization(
        organization_code="WS_HANDOFF_TEST_ORG", organization_name="Workspace Handoff Test Org", organization_type="CORPORATE",
    )
    role = Role(role_code="WS_HANDOFF_TEST_ROLE", role_name="Workspace Handoff Test Role")
    db_session.add_all([person, organization, role])
    await db_session.flush()
    return person, organization, role


def _classification_service(session: AsyncSession) -> WorkspaceHandoffClassificationService:
    status_service = WorkspaceStatusService(MembershipRepository(session), OrganizationNodeRepository(session))
    return WorkspaceHandoffClassificationService(status_service)


def _membership_service(session: AsyncSession) -> MembershipService:
    return MembershipService(
        MembershipRepository(session),
        PersonRepository(session),
        OrganizationRepository(session),
        RoleRepository(session),
        OrganizationNodeRepository(session),
    )


async def test_classify_capability_scoped_when_workspace_current(
    db_session: AsyncSession, seeded_person_organization_role
) -> None:
    person, organization, role = seeded_person_organization_role
    membership_service = _membership_service(db_session)
    established = await membership_service.establish(
        EstablishMembershipRequest(person_id=person.id, organization_id=organization.id, role_id=role.id)
    )
    service = _classification_service(db_session)

    result = await service.classify(
        ClassifyWorkspaceHandoffRejectionRequest(
            membership_id=established.id,
            rejecting_capability="C-007",
            stated_reason="Membership hand-off could not confirm the presented Workspace Context.",
        )
    )

    assert result.classification == WorkspaceHandoffClassification.CAPABILITY_SCOPED_INSUFFICIENCY
    assert result.context_preserved is True
    assert result.routed_to is None
    assert result.membership_id == established.id


async def test_classify_integrity_signal_when_workspace_unresolved(
    db_session: AsyncSession, seeded_person_organization_role
) -> None:
    person, organization, role = seeded_person_organization_role
    membership_service = _membership_service(db_session)
    established = await membership_service.establish(
        EstablishMembershipRequest(person_id=person.id, organization_id=organization.id, role_id=role.id)
    )
    established.membership_status = "SUSPENDED"
    await db_session.flush()
    service = _classification_service(db_session)

    result = await service.classify(
        ClassifyWorkspaceHandoffRejectionRequest(
            membership_id=established.id,
            rejecting_capability="C-007",
            stated_reason="Workspace hand-off rejected this context.",
        )
    )

    assert result.classification == WorkspaceHandoffClassification.INTEGRITY_SIGNAL
    assert result.context_preserved is False
    assert result.routed_to is not None


async def test_classify_integrity_signal_for_unknown_membership(db_session: AsyncSession) -> None:
    service = _classification_service(db_session)

    result = await service.classify(
        ClassifyWorkspaceHandoffRejectionRequest(
            membership_id=uuid.uuid4(),
            rejecting_capability="C-007",
            stated_reason="Membership no longer resolves.",
        )
    )

    assert result.classification == WorkspaceHandoffClassification.INTEGRITY_SIGNAL
    assert result.context_preserved is False


async def test_classify_never_uses_stated_reason_as_basis(
    db_session: AsyncSession, seeded_person_organization_role
) -> None:
    """
    BR-C008-06: 'a signal, not an authority.' Even a stated_reason that
    claims an integrity problem must not change the classification when
    the Workspace Context's own independently-verifiable state is
    CURRENT.
    """
    person, organization, role = seeded_person_organization_role
    membership_service = _membership_service(db_session)
    established = await membership_service.establish(
        EstablishMembershipRequest(person_id=person.id, organization_id=organization.id, role_id=role.id)
    )
    service = _classification_service(db_session)

    result = await service.classify(
        ClassifyWorkspaceHandoffRejectionRequest(
            membership_id=established.id,
            rejecting_capability="C-007",
            stated_reason="This Workspace Context is definitely invalid and corrupted.",
        )
    )

    assert result.classification == WorkspaceHandoffClassification.CAPABILITY_SCOPED_INSUFFICIENCY
