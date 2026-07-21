import uuid

import pytest
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.organization import Organization, OrganizationStatus
from repositories.organization_repository import OrganizationRepository
from schemas.organization import EstablishOrganizationRequest, UpdateOrganizationProfileRequest
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


# ---------------------------------------------------------------------------
# BA-04 — Update Organization Profile
# ---------------------------------------------------------------------------

async def test_update_profile_updates_name_type_and_description(db_session: AsyncSession) -> None:
    """
    Business Activity Contract: Update Organization Profile persists the
    new organization_name, organization_type, and description.
    """
    service = _service(db_session)
    created = await service.establish(
        EstablishOrganizationRequest(
            organization_code="UPD-001",
            organization_name="Original Name",
            organization_type="CORPORATE",
            description="Original description.",
        )
    )

    updated = await service.update_profile(
        created.id,
        UpdateOrganizationProfileRequest(
            organization_name="Renamed Corporation",
            organization_type="SUBSIDIARY",
            description="Updated description.",
        ),
        actor_id="platform-admin-1",
    )

    assert updated.id == created.id
    assert updated.organization_name == "Renamed Corporation"
    assert updated.organization_type == "SUBSIDIARY"
    assert updated.description == "Updated description."


async def test_update_profile_does_not_change_code_or_status(db_session: AsyncSession) -> None:
    """
    Business Rule: organization_code (immutable natural key) and status
    (owned by the Activate/Suspend Business Activities, ADR-005) are not
    touched by Update Organization Profile.
    """
    service = _service(db_session)
    created = await service.establish(
        EstablishOrganizationRequest(
            organization_code="UPD-002",
            organization_name="Untouched Code Org",
            organization_type="CORPORATE",
        )
    )

    updated = await service.update_profile(
        created.id,
        UpdateOrganizationProfileRequest(organization_name="New Name", organization_type="CORPORATE"),
    )

    assert updated.organization_code == "UPD-002"
    assert updated.status == OrganizationStatus.ACTIVE.value


async def test_update_profile_allows_optional_description_to_be_cleared(db_session: AsyncSession) -> None:
    """description is optional on Update, same as Establish — omitting it clears any existing value."""
    service = _service(db_session)
    created = await service.establish(
        EstablishOrganizationRequest(
            organization_code="UPD-003",
            organization_name="Has Description",
            organization_type="CORPORATE",
            description="Will be cleared.",
        )
    )

    updated = await service.update_profile(
        created.id,
        UpdateOrganizationProfileRequest(organization_name="Has Description", organization_type="CORPORATE"),
    )

    assert updated.description is None


async def test_update_profile_raises_404_for_unknown_id(db_session: AsyncSession) -> None:
    """A well-formed but non-existent id is a 404, not a 500 or a silent no-op, same as get_details."""
    service = _service(db_session)

    with pytest.raises(HTTPException) as exc_info:
        await service.update_profile(
            uuid.uuid4(),
            UpdateOrganizationProfileRequest(organization_name="Ghost Org", organization_type="CORPORATE"),
        )

    assert exc_info.value.status_code == 404


# ---------------------------------------------------------------------------
# BA-03 — Search & List Organizations
# ---------------------------------------------------------------------------

async def _seed(service: OrganizationService, code: str, name: str, org_type: str = "CORPORATE") -> Organization:
    return await service.establish(
        EstablishOrganizationRequest(organization_code=code, organization_name=name, organization_type=org_type)
    )


async def test_search_returns_all_organizations_with_default_paging(db_session: AsyncSession) -> None:
    service = _service(db_session)
    await _seed(service, "SRCH-001", "Alpha Corp")
    await _seed(service, "SRCH-002", "Beta Corp")
    await _seed(service, "SRCH-003", "Gamma Corp")

    items, total = await service.search(
        query=None, status_filter=None, skip=0, limit=20, sort_by="organization_name", sort_order="asc"
    )

    assert total == 3
    assert [i.organization_name for i in items] == ["Alpha Corp", "Beta Corp", "Gamma Corp"]


async def test_search_matches_organization_name_case_insensitively(db_session: AsyncSession) -> None:
    service = _service(db_session)
    await _seed(service, "SRCH-010", "Northwind Traders")
    await _seed(service, "SRCH-011", "Contoso Ltd")

    items, total = await service.search(
        query="north", status_filter=None, skip=0, limit=20, sort_by="organization_name", sort_order="asc"
    )

    assert total == 1
    assert items[0].organization_code == "SRCH-010"


async def test_search_matches_organization_code(db_session: AsyncSession) -> None:
    service = _service(db_session)
    await _seed(service, "UNIQUE-CODE-042", "Some Company")
    await _seed(service, "OTHER-099", "Another Company")

    items, total = await service.search(
        query="unique-code", status_filter=None, skip=0, limit=20, sort_by="organization_name", sort_order="asc"
    )

    assert total == 1
    assert items[0].organization_code == "UNIQUE-CODE-042"


async def test_search_filters_by_status(db_session: AsyncSession) -> None:
    service = _service(db_session)
    await _seed(service, "SRCH-020", "Active One")
    await _seed(service, "SRCH-021", "Active Two")

    active_items, active_total = await service.search(
        query=None, status_filter="ACTIVE", skip=0, limit=20, sort_by="organization_name", sort_order="asc"
    )
    suspended_items, suspended_total = await service.search(
        query=None, status_filter="SUSPENDED", skip=0, limit=20, sort_by="organization_name", sort_order="asc"
    )

    assert active_total == 2
    assert suspended_total == 0
    assert suspended_items == []


async def test_search_pagination_returns_correct_page_and_total(db_session: AsyncSession) -> None:
    service = _service(db_session)
    for i in range(5):
        await _seed(service, f"PAGE-{i:03d}", f"Page Org {i}")

    page_1, total_1 = await service.search(
        query=None, status_filter=None, skip=0, limit=2, sort_by="organization_code", sort_order="asc"
    )
    page_2, total_2 = await service.search(
        query=None, status_filter=None, skip=2, limit=2, sort_by="organization_code", sort_order="asc"
    )

    assert total_1 == 5 and total_2 == 5
    assert len(page_1) == 2 and len(page_2) == 2
    assert [o.organization_code for o in page_1] == ["PAGE-000", "PAGE-001"]
    assert [o.organization_code for o in page_2] == ["PAGE-002", "PAGE-003"]


async def test_search_sort_order_descending(db_session: AsyncSession) -> None:
    service = _service(db_session)
    await _seed(service, "SORT-001", "Zeta Corp")
    await _seed(service, "SORT-002", "Alpha Corp")

    items, _total = await service.search(
        query=None, status_filter=None, skip=0, limit=20, sort_by="organization_name", sort_order="desc"
    )

    assert [i.organization_name for i in items] == ["Zeta Corp", "Alpha Corp"]
