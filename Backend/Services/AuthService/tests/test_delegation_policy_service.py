import uuid

import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.domain import Domain
from models.organization import Organization
from repositories.delegation_policy_repository import DelegationPolicyRepository
from repositories.domain_repository import DomainRepository
from repositories.organization_repository import OrganizationRepository
from schemas.delegation_policy import EstablishDelegationPolicyRequest
from services.delegation_policy_service import DelegationPolicyService


@pytest.fixture
async def seeded_organization_and_domain(db_session: AsyncSession) -> tuple[Organization, Domain]:
    organization = Organization(
        organization_code="DP-POLICY-TEST-ORG",
        organization_name="Delegation Policy Test Org",
        organization_type="CORPORATE",
    )
    domain = Domain(domain_name="Finance")
    db_session.add_all([organization, domain])
    await db_session.flush()
    return organization, domain


def _service(session: AsyncSession) -> DelegationPolicyService:
    return DelegationPolicyService(
        DelegationPolicyRepository(session),
        OrganizationRepository(session),
        DomainRepository(session),
    )


async def test_establish_organization_scope(
    db_session: AsyncSession, seeded_organization_and_domain
) -> None:
    organization, _domain = seeded_organization_and_domain
    service = _service(db_session)
    request = EstablishDelegationPolicyRequest(
        organization_id=organization.id,
        policy_name="Emergency Financial Approval Delegation",
        delegation_type="EMERGENCY",
        scope_type="ORGANIZATION",
    )

    policy = await service.establish(request, actor_id="platform-admin-1")

    assert policy.scope_type == "ORGANIZATION"
    assert policy.domain_id is None
    assert policy.sub_delegation_allowed is False
    assert policy.id is not None


async def test_establish_domain_scope(
    db_session: AsyncSession, seeded_organization_and_domain
) -> None:
    organization, domain = seeded_organization_and_domain
    service = _service(db_session)
    request = EstablishDelegationPolicyRequest(
        organization_id=organization.id,
        policy_name="Finance Domain Out-of-Office Delegation",
        delegation_type="OUT_OF_OFFICE",
        scope_type="DOMAIN",
        domain_id=domain.id,
    )

    policy = await service.establish(request)

    assert policy.scope_type == "DOMAIN"
    assert policy.domain_id == domain.id


async def test_establish_object_scope(
    db_session: AsyncSession, seeded_organization_and_domain
) -> None:
    organization, _domain = seeded_organization_and_domain
    service = _service(db_session)
    object_id = uuid.uuid4()
    request = EstablishDelegationPolicyRequest(
        organization_id=organization.id,
        policy_name="Revenue CDE Acting-Role Delegation",
        delegation_type="ACTING_ROLE",
        scope_type="OBJECT",
        object_type="revenue_cde",
        object_id=object_id,
    )

    policy = await service.establish(request)

    assert policy.scope_type == "OBJECT"
    assert policy.object_type == "revenue_cde"
    assert policy.object_id == object_id


async def test_establish_event_scope(
    db_session: AsyncSession, seeded_organization_and_domain
) -> None:
    organization, _domain = seeded_organization_and_domain
    service = _service(db_session)
    request = EstablishDelegationPolicyRequest(
        organization_id=organization.id,
        policy_name="CFO Signoff Event Delegation",
        delegation_type="PROJECT_BASED",
        scope_type="EVENT",
        event_code="CFO_SIGNOFF",
        sub_delegation_allowed=True,
    )

    policy = await service.establish(request)

    assert policy.scope_type == "EVENT"
    assert policy.event_code == "CFO_SIGNOFF"
    assert policy.sub_delegation_allowed is True


async def test_establish_rejects_unknown_organization(db_session: AsyncSession) -> None:
    """EX-C003-04 Context Required: organization_id is required for every scope."""
    service = _service(db_session)
    request = EstablishDelegationPolicyRequest(
        organization_id=uuid.uuid4(),
        policy_name="Emergency Financial Approval Delegation",
        delegation_type="EMERGENCY",
        scope_type="ORGANIZATION",
    )

    with pytest.raises(HTTPException) as exc_info:
        await service.establish(request)

    assert exc_info.value.status_code == 404


async def test_establish_rejects_unknown_domain_for_domain_scope(
    db_session: AsyncSession, seeded_organization_and_domain
) -> None:
    organization, _domain = seeded_organization_and_domain
    service = _service(db_session)
    request = EstablishDelegationPolicyRequest(
        organization_id=organization.id,
        policy_name="Finance Domain Out-of-Office Delegation",
        delegation_type="OUT_OF_OFFICE",
        scope_type="DOMAIN",
        domain_id=uuid.uuid4(),
    )

    with pytest.raises(HTTPException) as exc_info:
        await service.establish(request)

    assert exc_info.value.status_code == 404
