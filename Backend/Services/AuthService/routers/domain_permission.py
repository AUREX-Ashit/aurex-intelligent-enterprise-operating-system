from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import require_platform_admin
from models.database import db_manager
from repositories.domain_permission_repository import DomainPermissionRepository
from repositories.domain_repository import DomainRepository
from repositories.membership_repository import MembershipRepository
from schemas.domain_permission import EstablishDomainPermissionRequest, DomainPermissionResponse, VersionDomainPermissionRequest
from services.domain_permission_service import DomainPermissionService

router = APIRouter()


# ---------------------------------------------------------------------------
# Dependency factories
# ---------------------------------------------------------------------------

async def get_domain_permission_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> DomainPermissionRepository:
    return DomainPermissionRepository(session)


async def get_domain_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> DomainRepository:
    return DomainRepository(session)


async def get_membership_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> MembershipRepository:
    return MembershipRepository(session)


async def get_domain_permission_service(
    domain_permission_repo: Annotated[DomainPermissionRepository, Depends(get_domain_permission_repository)],
    domain_repo: Annotated[DomainRepository, Depends(get_domain_repository)],
    membership_repo: Annotated[MembershipRepository, Depends(get_membership_repository)],
) -> DomainPermissionService:
    return DomainPermissionService(domain_permission_repo, domain_repo, membership_repo)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post(
    "",
    response_model=DomainPermissionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Establish a new Domain Permission",
    description=(
        "WP-02 Business Activity: Establish Domain Permission (C-003), "
        "realizing PE-001-C003's ERB-C003-01 / EX-C003-02. Requires the "
        "PLATFORM_ADMIN role (interim gate, mirroring BA-01 — confirmed "
        "Domain Owner/Domain Admin authority per URA-001-45/-46 is not yet "
        "implementable, tracked as technical debt). Independent of any "
        "Business Role (BR-C003-02). Rejects an unknown Domain or "
        "Membership with 404, and a duplicate active grant with 409."
    ),
    responses={
        201: {"description": "Domain Permission established."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "The target Domain or Membership does not exist."},
        409: {"description": "An active grant of this permission level already exists for this membership/domain pair."},
        422: {"description": "Invalid request (e.g., permission_level not one of URA-001-47's eight values)."},
    },
)
async def establish_domain_permission(
    request: EstablishDomainPermissionRequest,
    domain_permission_service: Annotated[DomainPermissionService, Depends(get_domain_permission_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> DomainPermissionResponse:
    domain_permission = await domain_permission_service.establish(request, actor_id=claims.get("person_id"))
    return DomainPermissionResponse.model_validate(domain_permission)


@router.post(
    "/{domain_permission_id}/versions",
    response_model=DomainPermissionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Version and re-effective-date a Domain Permission",
    description=(
        "WP-02 Business Activity: Version and Re-effective-Date "
        "Authorization Policy Object (C-003), realizing PE-001-C003's "
        "ERB-C003-02 / EX-C003-07. Domain Permission has no metadata "
        "field distinct from its structural grant, so this endpoint "
        "amends only the effective-date window (membership_id, "
        "domain_id, and permission_level are outside this Business "
        "Activity's non-breaking scope). Preserves the prior version as "
        "an inspectable, SUPERSEDED historical record (BR-C003-05). "
        "Requires the PLATFORM_ADMIN role (same interim gate as BA-02)."
    ),
    responses={
        201: {"description": "New version established; prior version preserved as SUPERSEDED."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "The target Domain Permission does not exist."},
        409: {"description": "The target Domain Permission id does not name the current ACTIVE version."},
        422: {"description": "Invalid request."},
    },
)
async def version_domain_permission(
    domain_permission_id: UUID,
    request: VersionDomainPermissionRequest,
    domain_permission_service: Annotated[DomainPermissionService, Depends(get_domain_permission_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> DomainPermissionResponse:
    domain_permission = await domain_permission_service.create_new_version(
        domain_permission_id, request, actor_id=claims.get("person_id")
    )
    return DomainPermissionResponse.model_validate(domain_permission)
