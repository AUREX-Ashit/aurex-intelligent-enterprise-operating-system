from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import require_platform_admin
from models.database import db_manager
from repositories.domain_repository import DomainRepository
from schemas.domain import DomainResponse
from services.domain_service import DomainService

router = APIRouter()


# ---------------------------------------------------------------------------
# Dependency factories
# ---------------------------------------------------------------------------

async def get_domain_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> DomainRepository:
    return DomainRepository(session)


async def get_domain_service(
    domain_repo: Annotated[DomainRepository, Depends(get_domain_repository)],
) -> DomainService:
    return DomainService(domain_repo)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get(
    "",
    response_model=list[DomainResponse],
    summary="List the Domain reference catalog",
    description=(
        "AMD-014 reference/master-data lookup: every platform-default "
        "Domain (URA-001-43: Finance, HR, Risk, Supply Chain, Cyber "
        "Security, Legal, Business Resilience), plus the given "
        "organization's own added domains if organization_id is supplied. "
        "Read-only — Domain rows are seeded (MDP-001 §B2a), not created "
        "through this API."
    ),
    responses={
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
    },
)
async def list_domains(
    domain_service: Annotated[DomainService, Depends(get_domain_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
    organization_id: UUID | None = Query(
        None,
        description="Include this organization's own added domains alongside the platform defaults.",
    ),
) -> list[DomainResponse]:
    domains = await domain_service.list_domains(organization_id)
    return [DomainResponse.model_validate(d) for d in domains]


@router.get(
    "/{domain_id}",
    response_model=DomainResponse,
    summary="Resolve a single Domain by id",
    description=(
        "AMD-014 reference/master-data lookup, realizing PE-001-C003's "
        "EX-C003-02 Entry Context precondition ('the target Domain, "
        "already established'). Read-only."
    ),
    responses={
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "No domain found with this id."},
    },
)
async def get_domain(
    domain_id: UUID,
    domain_service: Annotated[DomainService, Depends(get_domain_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> DomainResponse:
    domain = await domain_service.get_details(domain_id)
    return DomainResponse.model_validate(domain)
