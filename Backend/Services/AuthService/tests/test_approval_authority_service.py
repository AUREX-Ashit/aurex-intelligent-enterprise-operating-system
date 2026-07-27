import uuid

import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.domain import Domain
from models.organization import Organization
from repositories.approval_authority_repository import ApprovalAuthorityRepository
from repositories.domain_repository import DomainRepository
from repositories.organization_repository import OrganizationRepository
from schemas.approval_authority import EstablishApprovalAuthorityRequest
from services.approval_authority_service import ApprovalAuthorityService


@pytest.fixture
async def seeded_organization_and_domain(db_session: AsyncSession) -> tuple[Organization, Domain]:
    organization = Organization(
        organization_code="AA-TEST-ORG",
        organization_name="Approval Authority Test Org",
        organization_type="CORPORATE",
    )
    domain = Domain(domain_name="Finance")
    db_session.add_all([organization, domain])
    await db_session.flush()
    return organization, domain


def _service(session: AsyncSession) -> ApprovalAuthorityService:
    return ApprovalAuthorityService(
        ApprovalAuthorityRepository(session),
        OrganizationRepository(session),
        DomainRepository(session),
    )


async def test_establish_global_scope(
    db_session: AsyncSession, seeded_organization_and_domain
) -> None:
    organization, _domain = seeded_organization_and_domain
    service = _service(db_session)
    request = EstablishApprovalAuthorityRequest(
        organization_id=organization.id,
        authority_name="Global Framework Approval",
        approval_strategy="ANY_ONE",
        scope_type="GLOBAL",
    )

    authority = await service.establish(request, actor_id="platform-admin-1")

    assert authority.scope_type == "GLOBAL"
    assert authority.domain_id is None
    assert authority.object_type is None
    assert authority.id is not None


async def test_establish_company_scope(
    db_session: AsyncSession, seeded_organization_and_domain
) -> None:
    organization, _domain = seeded_organization_and_domain
    service = _service(db_session)
    request = EstablishApprovalAuthorityRequest(
        organization_id=organization.id,
        authority_name="Annual Report Approver",
        approval_strategy="SEQUENTIAL",
        scope_type="COMPANY",
    )

    authority = await service.establish(request)

    assert authority.scope_type == "COMPANY"
    assert authority.organization_id == organization.id


async def test_establish_domain_scope(
    db_session: AsyncSession, seeded_organization_and_domain
) -> None:
    organization, domain = seeded_organization_and_domain
    service = _service(db_session)
    request = EstablishApprovalAuthorityRequest(
        organization_id=organization.id,
        authority_name="Revenue CDE Approval",
        approval_strategy="MAJORITY",
        majority_threshold_pct=66,
        scope_type="DOMAIN",
        domain_id=domain.id,
    )

    authority = await service.establish(request)

    assert authority.scope_type == "DOMAIN"
    assert authority.domain_id == domain.id
    assert authority.majority_threshold_pct == 66


async def test_establish_object_scope(
    db_session: AsyncSession, seeded_organization_and_domain
) -> None:
    organization, _domain = seeded_organization_and_domain
    service = _service(db_session)
    object_id = uuid.uuid4()
    request = EstablishApprovalAuthorityRequest(
        organization_id=organization.id,
        authority_name="Revenue CDE Approval",
        approval_strategy="ALL",
        scope_type="OBJECT",
        object_type="revenue_cde",
        object_id=object_id,
    )

    authority = await service.establish(request)

    assert authority.scope_type == "OBJECT"
    assert authority.object_type == "revenue_cde"
    assert authority.object_id == object_id
    assert authority.domain_id is None


async def test_establish_rejects_unknown_organization(db_session: AsyncSession) -> None:
    """EX-C003-03 Context Required: organization_id is required for every scope."""
    service = _service(db_session)
    request = EstablishApprovalAuthorityRequest(
        organization_id=uuid.uuid4(),
        authority_name="Global Framework Approval",
        approval_strategy="ANY_ONE",
        scope_type="GLOBAL",
    )

    with pytest.raises(HTTPException) as exc_info:
        await service.establish(request)

    assert exc_info.value.status_code == 404


async def test_establish_rejects_unknown_domain_for_domain_scope(
    db_session: AsyncSession, seeded_organization_and_domain
) -> None:
    organization, _domain = seeded_organization_and_domain
    service = _service(db_session)
    request = EstablishApprovalAuthorityRequest(
        organization_id=organization.id,
        authority_name="Revenue CDE Approval",
        approval_strategy="MAJORITY",
        scope_type="DOMAIN",
        domain_id=uuid.uuid4(),
    )

    with pytest.raises(HTTPException) as exc_info:
        await service.establish(request)

    assert exc_info.value.status_code == 404
