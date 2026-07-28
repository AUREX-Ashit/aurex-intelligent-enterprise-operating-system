from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import require_platform_admin
from models.database import db_manager
from repositories.role_repository import RoleRepository
from schemas.role import EstablishRoleRequest, RoleResponse, VersionRoleRequest
from services.role_service import RoleService

router = APIRouter()


# ---------------------------------------------------------------------------
# Dependency factories
# ---------------------------------------------------------------------------

async def get_role_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> RoleRepository:
    return RoleRepository(session)


async def get_role_service(
    role_repo: Annotated[RoleRepository, Depends(get_role_repository)],
) -> RoleService:
    return RoleService(role_repo)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post(
    "",
    response_model=RoleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Establish a new Business or System Role",
    description=(
        "WP-02 Business Activity: Establish Business or System Role (C-003), "
        "realizing PE-001-C003's ERB-C003-01 / EX-C003-01. Requires the "
        "PLATFORM_ADMIN role (IRA-002 §2.7 — persona-specific defining "
        "authority per BR-C003-08 is deferred pending ADR-002's resolution "
        "of the canonical role catalog). Establishing a Role never "
        "automatically grants a Domain Permission, Approval Authority, or "
        "Runtime Assignment (BR-C003-02). Rejects duplicate role_code with 409."
    ),
    responses={
        201: {"description": "Role established."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        409: {"description": "A role with this role_code already exists."},
        422: {"description": "Invalid request (e.g., missing required field)."},
    },
)
async def establish_role(
    request: EstablishRoleRequest,
    role_service: Annotated[RoleService, Depends(get_role_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> RoleResponse:
    """
    No tenant-scoping: Roles are platform-global (no organization_id
    column on the Role model), the same basis routers/organization.py
    documents for establish_organization — see also
    middleware/tenant.py's exemption list, which this path is added to.
    """
    role = await role_service.establish(request, actor_id=claims.get("person_id"))
    return RoleResponse.model_validate(role)


@router.post(
    "/{role_id}/versions",
    response_model=RoleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Version and re-effective-date a Role",
    description=(
        "WP-02 Business Activity: Version and Re-effective-Date "
        "Authorization Policy Object (C-003), realizing PE-001-C003's "
        "ERB-C003-02 / EX-C003-07. Amends role_name/description and/or "
        "the effective-date window without changing role_code or "
        "is_system_role (outside this Business Activity's non-breaking "
        "scope). Preserves the prior version as an inspectable, "
        "SUPERSEDED historical record (BR-C003-05) — never mutated in "
        "place. Requires the PLATFORM_ADMIN role (same interim gate as "
        "BA-01)."
    ),
    responses={
        201: {"description": "New version established; prior version preserved as SUPERSEDED."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "The target Role does not exist."},
        409: {"description": "The target Role id does not name the current ACTIVE version."},
        422: {"description": "Invalid request."},
    },
)
async def version_role(
    role_id: UUID,
    request: VersionRoleRequest,
    role_service: Annotated[RoleService, Depends(get_role_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> RoleResponse:
    role = await role_service.create_new_version(role_id, request, actor_id=claims.get("person_id"))
    return RoleResponse.model_validate(role)
