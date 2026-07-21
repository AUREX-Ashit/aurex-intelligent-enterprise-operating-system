import uuid

import pytest
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.organization import Organization, OrganizationStatus
from repositories.organization_repository import OrganizationRepository
from schemas.organization import EstablishOrganizationRequest
from services.organization_service import OrganizationService


def _service(session: AsyncSession) -> OrganizationService:
    return OrganizationService(OrganizationRepository(session))


async def test_establish_creates_organization_with_active_status(db_session: AsyncSession) -> None:
    """
    Business Activity Contract: a first-time Establish Organization call
    creates exactly one row, with status defaulted to ACTIVE per ADR-005's
    interim lifecycle model — never invented as some other value.
    """
    service = _service(db_session)
    request = EstablishOrganizationRequest(
        organization_code="ACME-001",
        organization_name="Acme Corporation",
        organization_type="CORPORATE",
        description="A test organization.",
    )

    organization = await service.establish(request, actor_id="platform-admin-1")

    assert organization.organization_code == "ACME-001"
    assert organization.organization_name == "Acme Corporation"
    assert organization.organization_type == "CORPORATE"
    assert organization.description == "A test organization."
    assert organization.status == OrganizationStatus.ACTIVE.value
    assert organization.is_active is True
    assert organization.id is not None


async def test_establish_allows_optional_description_to_be_omitted(db_session: AsyncSession) -> None:
    """description is the only optional field — establishment must not require it."""
    service = _service(db_session)
    request = EstablishOrganizationRequest(
        organization_code="ACME-002",
        organization_name="Acme Subsidiary",
        organization_type="SUBSIDIARY",
    )

    organization = await service.establish(request)

    assert organization.description is None


async def test_establish_rejects_duplicate_organization_code(db_session: AsyncSession) -> None:
    """
    Business Rule: organization_code is unique platform-wide. A second
    Establish Organization call for the same code is rejected (409), not
    silently deduplicated and not permitted to create a second row.
    """
    service = _service(db_session)
    request = EstablishOrganizationRequest(
        organization_code="ACME-003",
        organization_name="Acme Corporation",
        organization_type="CORPORATE",
    )
    await service.establish(request)

    with pytest.raises(HTTPException) as exc_info:
        await service.establish(request)

    assert exc_info.value.status_code == 409

    result = await db_session.execute(
        select(Organization).where(Organization.organization_code == "ACME-003")
    )
    assert len(result.scalars().all()) == 1


# ---------------------------------------------------------------------------
# BA-02 — View Organization Details
# ---------------------------------------------------------------------------

async def test_get_details_returns_the_established_organization(db_session: AsyncSession) -> None:
    """BA-02: fetching by id returns exactly the organization created by BA-01's establish()."""
    service = _service(db_session)
    request = EstablishOrganizationRequest(
        organization_code="ACME-004",
        organization_name="Acme Fourth",
        organization_type="CORPORATE",
        description="Fetched by id.",
    )
    created = await service.establish(request)

    fetched = await service.get_details(created.id)

    assert fetched.id == created.id
    assert fetched.organization_code == "ACME-004"
    assert fetched.organization_name == "Acme Fourth"
    assert fetched.description == "Fetched by id."
    assert fetched.status == OrganizationStatus.ACTIVE.value


async def test_get_details_raises_404_for_unknown_id(db_session: AsyncSession) -> None:
    """BA-02: a well-formed but non-existent id is a 404, not a 500 or an empty success."""
    service = _service(db_session)

    with pytest.raises(HTTPException) as exc_info:
        await service.get_details(uuid.uuid4())

    assert exc_info.value.status_code == 404
