from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import require_platform_admin
from models.database import db_manager
from repositories.approval_authority_repository import ApprovalAuthorityRepository
from repositories.domain_repository import DomainRepository
from repositories.organization_repository import OrganizationRepository
from schemas.approval_authority import EstablishApprovalAuthorityRequest, ApprovalAuthorityResponse, VersionApprovalAuthorityRequest
from services.approval_authority_service import ApprovalAuthorityService

router = APIRouter()


# ---------------------------------------------------------------------------
# Dependency factories
# ---------------------------------------------------------------------------

async def get_approval_authority_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> ApprovalAuthorityRepository:
    return ApprovalAuthorityRepository(session)


async def get_organization_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> OrganizationRepository:
    return OrganizationRepository(session)


async def get_domain_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> DomainRepository:
    return DomainRepository(session)


async def get_approval_authority_service(
    approval_authority_repo: Annotated[ApprovalAuthorityRepository, Depends(get_approval_authority_repository)],
    organization_repo: Annotated[OrganizationRepository, Depends(get_organization_repository)],
    domain_repo: Annotated[DomainRepository, Depends(get_domain_repository)],
) -> ApprovalAuthorityService:
    return ApprovalAuthorityService(approval_authority_repo, organization_repo, domain_repo)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post(
    "",
    response_model=ApprovalAuthorityResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Establish a new Approval Authority",
    description=(
        "WP-02 Business Activity: Establish Approval Authority (C-003), "
        "realizing PE-001-C003's ERB-C003-01 / EX-C003-03. Requires the "
        "PLATFORM_ADMIN role (interim gate, mirroring BA-01/BA-02 — "
        "confirmed Corporate Admin/Domain Owner authority is not yet "
        "implementable, tracked as technical debt). Declares exactly one "
        "approval_strategy and exactly one scope_type (GLOBAL/COMPANY/"
        "DOMAIN/OBJECT, URA-001-61); an ambiguous, dual-stated, or "
        "incomplete scope is rejected with 422. Rejects an unknown "
        "Organization or Domain with 404."
    ),
    responses={
        201: {"description": "Approval Authority established."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "The target Organization or Domain does not exist."},
        422: {"description": "Invalid request (e.g., scope_type's required anchor missing, or an anchor supplied for the wrong scope_type)."},
    },
)
async def establish_approval_authority(
    request: EstablishApprovalAuthorityRequest,
    approval_authority_service: Annotated[ApprovalAuthorityService, Depends(get_approval_authority_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> ApprovalAuthorityResponse:
    approval_authority = await approval_authority_service.establish(request, actor_id=claims.get("person_id"))
    return ApprovalAuthorityResponse.model_validate(approval_authority)


@router.post(
    "/{approval_authority_id}/versions",
    response_model=ApprovalAuthorityResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Version and re-effective-date an Approval Authority",
    description=(
        "WP-02 Business Activity: Version and Re-effective-Date "
        "Authorization Policy Object (C-003), realizing PE-001-C003's "
        "ERB-C003-02 / EX-C003-07. Amends authority_name/"
        "majority_threshold_pct and/or the effective-date window without "
        "changing approval_strategy or scope (outside this Business "
        "Activity's non-breaking scope). Preserves the prior version as "
        "an inspectable, SUPERSEDED historical record (BR-C003-05). "
        "Requires the PLATFORM_ADMIN role (same interim gate as BA-03)."
    ),
    responses={
        201: {"description": "New version established; prior version preserved as SUPERSEDED."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "The target Approval Authority does not exist."},
        409: {"description": "The target Approval Authority id does not name the current ACTIVE version."},
        422: {"description": "Invalid request."},
    },
)
async def version_approval_authority(
    approval_authority_id: UUID,
    request: VersionApprovalAuthorityRequest,
    approval_authority_service: Annotated[ApprovalAuthorityService, Depends(get_approval_authority_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> ApprovalAuthorityResponse:
    approval_authority = await approval_authority_service.create_new_version(
        approval_authority_id, request, actor_id=claims.get("person_id")
    )
    return ApprovalAuthorityResponse.model_validate(approval_authority)
