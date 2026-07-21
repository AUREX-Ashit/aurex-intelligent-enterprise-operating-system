from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import require_platform_admin
from models.database import db_manager
from repositories.organization_repository import OrganizationRepository
from schemas.organization import EstablishOrganizationRequest, OrganizationResponse
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
