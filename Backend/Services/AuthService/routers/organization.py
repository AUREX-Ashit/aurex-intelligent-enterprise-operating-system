from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import require_platform_admin
from models.database import db_manager
from models.organization import OrganizationStatus
from repositories.organization_repository import OrganizationRepository
from schemas.organization import (
    EstablishOrganizationRequest,
    OrganizationListResponse,
    OrganizationResponse,
    OrganizationSortField,
    SortOrder,
    UpdateOrganizationProfileRequest,
)
from services.organization_service import OrganizationService

router = APIRouter()


# ---------------------------------------------------------------------------
# Dependency factories
# ---------------------------------------------------------------------------

async def get_organization_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> OrganizationRepository:
    return OrganizationRepository(session)


async def get_organization_service(
    organization_repo: Annotated[OrganizationRepository, Depends(get_organization_repository)],
) -> OrganizationService:
    return OrganizationService(organization_repo)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post(
    "",
    response_model=OrganizationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Establish a new organization",
    description=(
        "WP-01 Business Activity: Establish Organization (C-004). Requires the "
        "PLATFORM_ADMIN role (IRA-001 §2.7 — Domain Permission checks are "
        "deferred to the Role & Permission Management work package). Rejects "
        "duplicate organization_code with 409."
    ),
    responses={
        201: {"description": "Organization established."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        409: {"description": "An organization with this organization_code already exists."},
        422: {"description": "Invalid request (e.g., missing required field)."},
    },
)
async def establish_organization(
    request: EstablishOrganizationRequest,
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> OrganizationResponse:
    """
    No tenant-scoping: establishing a brand-new Organization has no
    existing tenant to scope to, on the same basis routers/person.py's
    establish_person already documents for Person — see also
    middleware/tenant.py's exemption list, which this path is added to.
    """
    organization = await organization_service.establish(
        request, actor_id=claims.get("person_id")
    )
    return OrganizationResponse.model_validate(organization)


@router.get(
    "",
    response_model=OrganizationListResponse,
    status_code=status.HTTP_200_OK,
    summary="Search and list organizations",
    description=(
        "WP-01 Business Activity: Search & List Organizations (C-004) — BA-03. "
        "Requires the PLATFORM_ADMIN role, same interim gate as the other "
        "Organization Management endpoints (IRA-001 §2.7). q matches "
        "organization_name or organization_code, case-insensitive, substring."
    ),
    responses={
        200: {"description": "A page of matching organizations, with a total count for pagination."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        422: {"description": "Invalid query parameters."},
    },
)
async def search_organizations(
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
    q: Annotated[str | None, Query(max_length=255, description="Search text against name or code")] = None,
    status_filter: Annotated[OrganizationStatus | None, Query(alias="status", description="Filter by lifecycle status")] = None,
    skip: Annotated[int, Query(ge=0, description="Rows to skip (pagination offset)")] = 0,
    limit: Annotated[int, Query(ge=1, le=100, description="Max rows to return (1-100)")] = 20,
    sort_by: Annotated[OrganizationSortField, Query(description="Field to sort by")] = OrganizationSortField.organization_name,
    sort_order: Annotated[SortOrder, Query(description="Sort direction")] = SortOrder.asc,
) -> OrganizationListResponse:
    """
    No tenant-scoping, same basis as the other Organization Management
    endpoints — PLATFORM_ADMIN operates across every organization, so
    listing is inherently a cross-tenant operation.
    """
    items, total = await organization_service.search(
        query=q,
        status_filter=status_filter.value if status_filter else None,
        skip=skip,
        limit=limit,
        sort_by=sort_by.value,
        sort_order=sort_order.value,
    )
    return OrganizationListResponse(
        items=[OrganizationResponse.model_validate(item) for item in items],
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{organization_id}",
    response_model=OrganizationResponse,
    status_code=status.HTTP_200_OK,
    summary="View organization details",
    description=(
        "WP-01 Business Activity: View Organization Details (C-004). Requires the "
        "PLATFORM_ADMIN role, same interim gate as Establish Organization "
        "(IRA-001 §2.7)."
    ),
    responses={
        200: {"description": "Organization found."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "No organization exists with this id."},
        422: {"description": "organization_id is not a valid UUID."},
    },
)
async def get_organization(
    organization_id: UUID,
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> OrganizationResponse:
    """
    No tenant-scoping, same basis as establish_organization above:
    PLATFORM_ADMIN operates across organization boundaries, so a
    per-request tenant header is not applicable here — see
    middleware/tenant.py's exemption for the /organizations prefix.
    """
    organization = await organization_service.get_details(organization_id)
    return OrganizationResponse.model_validate(organization)


@router.put(
    "/{organization_id}",
    response_model=OrganizationResponse,
    status_code=status.HTTP_200_OK,
    summary="Update organization profile",
    description=(
        "WP-01 Business Activity: Update Organization Profile (C-004) — BA-04. "
        "Requires the PLATFORM_ADMIN role, same interim gate as the other "
        "Organization Management endpoints (IRA-001 §2.7). Updates "
        "organization_name, organization_type, and description; "
        "organization_code and lifecycle status are not part of this "
        "Business Activity's scope."
    ),
    responses={
        200: {"description": "Organization profile updated."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "No organization exists with this id."},
        422: {"description": "Invalid request (e.g., missing required field)."},
    },
)
async def update_organization(
    organization_id: UUID,
    request: UpdateOrganizationProfileRequest,
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> OrganizationResponse:
    """
    No tenant-scoping, same basis as get_organization above: PLATFORM_ADMIN
    operates across organization boundaries — see middleware/tenant.py's
    /organizations/* prefix exemption, already covering this path.
    """
    organization = await organization_service.update_profile(
        organization_id, request, actor_id=claims.get("person_id")
    )
    return OrganizationResponse.model_validate(organization)


@router.post(
    "/{organization_id}/activate",
    response_model=OrganizationResponse,
    status_code=status.HTTP_200_OK,
    summary="Activate organization",
    description=(
        "WP-01 Business Activity: Activate Organization (C-004) — BA-05. "
        "Requires the PLATFORM_ADMIN role, same interim gate as the other "
        "Organization Management endpoints (IRA-001 §2.7). Transitions "
        "status from SUSPENDED to ACTIVE per ADR-005's interim lifecycle "
        "model. Rejects an already-ACTIVE organization with 409 rather "
        "than a silent no-op."
    ),
    responses={
        200: {"description": "Organization activated."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "No organization exists with this id."},
        409: {"description": "Organization is already ACTIVE."},
        422: {"description": "organization_id is not a valid UUID."},
    },
)
async def activate_organization(
    organization_id: UUID,
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> OrganizationResponse:
    """
    No tenant-scoping, same basis as the other path-parameterized
    Organization Management endpoints — see middleware/tenant.py's
    /organizations/* prefix exemption, already covering this path.
    """
    organization = await organization_service.activate(
        organization_id, actor_id=claims.get("person_id")
    )
    return OrganizationResponse.model_validate(organization)


@router.post(
    "/{organization_id}/suspend",
    response_model=OrganizationResponse,
    status_code=status.HTTP_200_OK,
    summary="Suspend organization",
    description=(
        "WP-01 Business Activity: Suspend Organization (C-004) — BA-06. "
        "Requires the PLATFORM_ADMIN role, same interim gate as the other "
        "Organization Management endpoints (IRA-001 §2.7). Transitions "
        "status from ACTIVE to SUSPENDED per ADR-005's interim lifecycle "
        "model. Rejects an already-SUSPENDED organization with 409 rather "
        "than a silent no-op."
    ),
    responses={
        200: {"description": "Organization suspended."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "No organization exists with this id."},
        409: {"description": "Organization is already SUSPENDED."},
        422: {"description": "organization_id is not a valid UUID."},
    },
)
async def suspend_organization(
    organization_id: UUID,
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> OrganizationResponse:
    """
    No tenant-scoping, same basis as the other path-parameterized
    Organization Management endpoints — see middleware/tenant.py's
    /organizations/* prefix exemption, already covering this path.
    """
    organization = await organization_service.suspend(
        organization_id, actor_id=claims.get("person_id")
    )
    return OrganizationResponse.model_validate(organization)
