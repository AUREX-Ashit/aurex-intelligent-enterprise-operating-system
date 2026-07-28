import uuid

import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.organization import Organization
from repositories.runtime_assignment_policy_repository import RuntimeAssignmentPolicyRepository
from repositories.organization_repository import OrganizationRepository
from schemas.runtime_assignment_policy import EstablishRuntimeAssignmentPolicyRequest, DEFAULT_LIFECYCLE_STATES
from services.runtime_assignment_policy_service import RuntimeAssignmentPolicyService


@pytest.fixture
async def seeded_organization(db_session: AsyncSession) -> Organization:
    organization = Organization(
        organization_code="RAP-POLICY-TEST-ORG",
        organization_name="Runtime Assignment Policy Test Org",
        organization_type="CORPORATE",
    )
    db_session.add(organization)
    await db_session.flush()
    return organization


def _service(session: AsyncSession) -> RuntimeAssignmentPolicyService:
    return RuntimeAssignmentPolicyService(
        RuntimeAssignmentPolicyRepository(session),
        OrganizationRepository(session),
    )


async def test_establish_defaults_lifecycle_states_when_none_supplied(
    db_session: AsyncSession, seeded_organization: Organization
) -> None:
    service = _service(db_session)
    request = EstablishRuntimeAssignmentPolicyRequest(
        organization_id=seeded_organization.id,
        policy_name="Revenue CDE Review Assignment Policy",
        assignment_target_type="BUSINESS_ROLE",
    )

    policy = await service.establish(request, actor_id="platform-admin-1")

    assert policy.id is not None
    assert policy.assignment_target_type == "BUSINESS_ROLE"
    assert policy.configured_lifecycle_states == DEFAULT_LIFECYCLE_STATES
    assert policy.escalation_policy_id is None


async def test_establish_named_user_target(
    db_session: AsyncSession, seeded_organization: Organization
) -> None:
    service = _service(db_session)
    request = EstablishRuntimeAssignmentPolicyRequest(
        organization_id=seeded_organization.id,
        policy_name="Ad Hoc Named-User Assignment Policy",
        assignment_target_type="NAMED_USER",
    )

    policy = await service.establish(request)

    assert policy.assignment_target_type == "NAMED_USER"


async def test_establish_group_target(
    db_session: AsyncSession, seeded_organization: Organization
) -> None:
    service = _service(db_session)
    request = EstablishRuntimeAssignmentPolicyRequest(
        organization_id=seeded_organization.id,
        policy_name="Board Committee Group Assignment Policy",
        assignment_target_type="GROUP",
    )

    policy = await service.establish(request)

    assert policy.assignment_target_type == "GROUP"


async def test_establish_external_user_target(
    db_session: AsyncSession, seeded_organization: Organization
) -> None:
    service = _service(db_session)
    request = EstablishRuntimeAssignmentPolicyRequest(
        organization_id=seeded_organization.id,
        policy_name="External Auditor Assignment Policy",
        assignment_target_type="EXTERNAL_USER",
    )

    policy = await service.establish(request)

    assert policy.assignment_target_type == "EXTERNAL_USER"


async def test_establish_preserves_custom_lifecycle_states(
    db_session: AsyncSession, seeded_organization: Organization
) -> None:
    """URA-001-78: companies may add states such as BOARD_APPROVED."""
    service = _service(db_session)
    custom_states = DEFAULT_LIFECYCLE_STATES + ["BOARD_APPROVED"]
    request = EstablishRuntimeAssignmentPolicyRequest(
        organization_id=seeded_organization.id,
        policy_name="Board Approval Assignment Policy",
        assignment_target_type="GROUP",
        configured_lifecycle_states=custom_states,
    )

    policy = await service.establish(request)

    assert policy.configured_lifecycle_states == custom_states


async def test_establish_stores_escalation_policy_reference(
    db_session: AsyncSession, seeded_organization: Organization
) -> None:
    service = _service(db_session)
    escalation_policy_id = uuid.uuid4()
    request = EstablishRuntimeAssignmentPolicyRequest(
        organization_id=seeded_organization.id,
        policy_name="Escalating Review Assignment Policy",
        assignment_target_type="BUSINESS_ROLE",
        escalation_policy_id=escalation_policy_id,
    )

    policy = await service.establish(request)

    assert policy.escalation_policy_id == escalation_policy_id


async def test_establish_rejects_unknown_organization(db_session: AsyncSession) -> None:
    """EX-C003-05 Context Required: the target Organization must already exist."""
    service = _service(db_session)
    request = EstablishRuntimeAssignmentPolicyRequest(
        organization_id=uuid.uuid4(),
        policy_name="Revenue CDE Review Assignment Policy",
        assignment_target_type="BUSINESS_ROLE",
    )

    with pytest.raises(HTTPException) as exc_info:
        await service.establish(request)

    assert exc_info.value.status_code == 404
