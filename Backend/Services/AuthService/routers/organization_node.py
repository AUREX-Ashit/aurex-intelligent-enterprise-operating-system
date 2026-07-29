from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import require_platform_admin
from models.database import db_manager
from repositories.organization_node_repository import OrganizationNodeRepository
from schemas.organization_node import EstablishOrganizationNodeRequest, OrganizationNodeResponse
from services.organization_node_service import OrganizationNodeService

router = APIRouter()


# ---------------------------------------------------------------------------
# Dependency factories
# ---------------------------------------------------------------------------

async def get_organization_node_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> OrganizationNodeRepository:
    return OrganizationNodeRepository(session)


async def get_organization_node_service(
    organization_node_repo: Annotated[OrganizationNodeRepository, Depends(get_organization_node_repository)],
) -> OrganizationNodeService:
    return OrganizationNodeService(organization_node_repo)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post(
    "",
    response_model=OrganizationNodeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Establish a new organization node",
    description=(
        "WP-04 Business Activity: Establish Organization Node (C-005, "
        "ERB-C005-01/EX-C005-01/02 per PE-001-C005; ERG-001-02/03; "
        "IRA-004 §9/§11). Requires the PLATFORM_ADMIN role (same interim "
        "gate WP-01/02/03 all used — Domain Permission checks are "
        "deferred to the Role & Permission Management work package). "
        "Rejects duplicate node_code with 409. Persists only the "
        "Structural Identity column subset IRA-004 scoped for BA-01; "
        "geography_id, hierarchy readiness, and the materiality/risk/"
        "scenario/passport scores are deferred (TD-043)."
    ),
    responses={
        201: {"description": "Organization node established."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        409: {"description": "An organization node with this node_code already exists."},
        422: {"description": "Invalid request (e.g., missing required field)."},
    },
)
async def establish_organization_node(
    request: EstablishOrganizationNodeRequest,
    organization_node_service: Annotated[OrganizationNodeService, Depends(get_organization_node_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> OrganizationNodeResponse:
    """
    No tenant-scoping: OrganizationNode carries no organization_id
    column anywhere in Master Technical Architecture's own canonical
    DDL or this table's current shape — there is no tenant to scope
    this request to, on the same basis routers/organization.py's
    establish_organization already documents for Organization. See also
    middleware/tenant.py's exemption list, which this path is added to.
    """
    organization_node = await organization_node_service.establish(
        request, actor_id=claims.get("person_id")
    )
    return OrganizationNodeResponse.model_validate(organization_node)
