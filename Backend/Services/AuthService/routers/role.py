from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import require_platform_admin
from models.database import db_manager
from repositories.domain_repository import DomainRepository
from repositories.organization_repository import OrganizationRepository
from repositories.role_repository import RoleRepository
from schemas.authorization_policy_conflict import DependencyConflictReport, ResolveDependencyConflictRequest
from schemas.authorization_policy_handoff import HandoffRejectionOutcome, ReportHandoffRejectionRequest
from schemas.role import EstablishRoleRequest, RoleResponse, VersionRoleRequest
from services.authorization_policy_conflict_service import AuthorizationPolicyConflictService
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


async def get_organization_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> OrganizationRepository:
    return OrganizationRepository(session)


async def get_domain_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> DomainRepository:
    return DomainRepository(session)


async def get_authorization_policy_conflict_service(
    organization_repo: Annotated[OrganizationRepository, Depends(get_organization_repository)],
    domain_repo: Annotated[DomainRepository, Depends(get_domain_repository)],
) -> AuthorizationPolicyConflictService:
    return AuthorizationPolicyConflictService(organization_repo, domain_repo)


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


@router.post(
    "/{role_id}/deprecate",
    response_model=RoleResponse,
    status_code=status.HTTP_200_OK,
    summary="Deprecate (Hide) a Role",
    description=(
        "WP-02 Business Activity: Deprecate or Retire Authorization "
        "Policy Object (C-003) — BA-08, realizing PE-001-C003's "
        "ERB-C003-02 / EX-C003-08. Transitions the current ACTIVE "
        "version to DEPRECATED (Hidden, URA-001-127) in place — never a "
        "new version row, never a hard delete. Rejected (409, naming "
        "BR-C003-04) if any Membership is still actively assigned this "
        "Role. Requires the PLATFORM_ADMIN role."
    ),
    responses={
        200: {"description": "Role deprecated."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "The target Role does not exist."},
        409: {"description": "The target Role is not the current ACTIVE version, or has an active dependency remaining unresolved (BR-C003-04)."},
    },
)
async def deprecate_role(
    role_id: UUID,
    role_service: Annotated[RoleService, Depends(get_role_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> RoleResponse:
    role = await role_service.deprecate(role_id, actor_id=claims.get("person_id"))
    return RoleResponse.model_validate(role)


@router.post(
    "/{role_id}/retire",
    response_model=RoleResponse,
    status_code=status.HTTP_200_OK,
    summary="Retire (Archive) a Role",
    description=(
        "WP-02 Business Activity: Deprecate or Retire Authorization "
        "Policy Object (C-003) — BA-08, realizing PE-001-C003's "
        "ERB-C003-02 / EX-C003-08. Transitions the current ACTIVE "
        "version to RETIRED (Archived, URA-001-127) in place — terminal, "
        "never reversible, never a hard delete. Rejected (409, naming "
        "BR-C003-04) if any Membership is still actively assigned this "
        "Role. Requires the PLATFORM_ADMIN role."
    ),
    responses={
        200: {"description": "Role retired."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "The target Role does not exist."},
        409: {"description": "The target Role is not the current ACTIVE version, or has an active dependency remaining unresolved (BR-C003-04)."},
    },
)
async def retire_role(
    role_id: UUID,
    role_service: Annotated[RoleService, Depends(get_role_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> RoleResponse:
    role = await role_service.retire(role_id, actor_id=claims.get("person_id"))
    return RoleResponse.model_validate(role)


@router.post(
    "/{role_id}/dependency-check",
    response_model=DependencyConflictReport,
    status_code=status.HTTP_200_OK,
    summary="Detect Authorization Policy Dependency Conflict for a Role",
    description=(
        "WP-02 Business Activity: Detect and Resolve Authorization "
        "Policy Dependency Conflict (C-003) — BA-09, realizing "
        "PE-001-C003's ERB-C003-03 / EX-C003-09. Enumerates every "
        "currently-active dependent (Membership, BR-C003-04) and checks "
        "version-chain and temporal integrity, before a proposed "
        "deprecation, retirement, or breaking amendment proceeds. Does "
        "not itself deprecate or retire (BA-08's own capability, "
        "unchanged). Requires the PLATFORM_ADMIN role."
    ),
    responses={
        200: {"description": "Dependency conflict report produced (has_conflicts indicates whether the change may proceed)."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "The target Role does not exist."},
    },
)
async def check_role_dependencies(
    role_id: UUID,
    role_repo: Annotated[RoleRepository, Depends(get_role_repository)],
    conflict_service: Annotated[AuthorizationPolicyConflictService, Depends(get_authorization_policy_conflict_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> DependencyConflictReport:
    role = await role_repo.get_by_id(role_id)
    if role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No role found with id '{role_id}'.")
    return await conflict_service.detect_conflicts("role", role, role_repo)


@router.post(
    "/{role_id}/resolve-dependency",
    response_model=DependencyConflictReport,
    status_code=status.HTTP_200_OK,
    summary="Resolve an Authorization Policy Dependency Conflict for a Role",
    description=(
        "WP-02 Business Activity: Detect and Resolve Authorization "
        "Policy Dependency Conflict (C-003) — BA-09, realizing "
        "PE-001-C003's ERB-C003-03 / EX-C003-09. Records the proposing "
        "authority's explicit resolution statement (Contract 5.6 — "
        "reassignment, natural expiry, or an affirmative accepted "
        "break; never a silent default) and re-runs the dependency "
        "check. Never mutates a Membership's own record (Contract "
        "5.1's C-007 boundary). Requires the PLATFORM_ADMIN role."
    ),
    responses={
        200: {"description": "Resolution recorded; current dependency conflict report returned."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "The target Role, or the supplied replacement_target_id, does not exist."},
        409: {"description": "The supplied replacement_target_id is not the current ACTIVE version."},
        422: {"description": "REASSIGNMENT_CONFIRMED requires replacement_target_id, or it names the object being replaced."},
    },
)
async def resolve_role_dependency(
    role_id: UUID,
    request: ResolveDependencyConflictRequest,
    role_repo: Annotated[RoleRepository, Depends(get_role_repository)],
    conflict_service: Annotated[AuthorizationPolicyConflictService, Depends(get_authorization_policy_conflict_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> DependencyConflictReport:
    role = await role_repo.get_by_id(role_id)
    if role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No role found with id '{role_id}'.")
    return await conflict_service.resolve_conflict("role", role, role_repo, request, actor_id=claims.get("person_id"))


@router.post(
    "/{role_id}/handoff-rejection",
    response_model=HandoffRejectionOutcome,
    status_code=status.HTTP_200_OK,
    summary="Resolve a Dependent Capability Hand-off Rejection for a Role",
    description=(
        "WP-02 Business Activity: Resolve Dependent Capability "
        "Authorization Policy Hand-off Rejection (C-003) — BA-10, "
        "realizing PE-001-C003's ERB-C003-03 / EX-C003-10. Classifies a "
        "reported rejection (e.g. from C-002 Access Management) as "
        "CAPABILITY_SCOPED_INSUFFICIENCY (object preserved unchanged) "
        "or INTEGRITY_SIGNAL (routed for correction), computed entirely "
        "from this Role's own status and BA-09's dependency check — "
        "never from the reporting capability's stated reason alone "
        "(Contract 5.7 — a signal, not an authority). Requires the "
        "PLATFORM_ADMIN role."
    ),
    responses={
        200: {"description": "Hand-off rejection classified."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "The target Role does not exist."},
    },
)
async def report_role_handoff_rejection(
    role_id: UUID,
    request: ReportHandoffRejectionRequest,
    role_repo: Annotated[RoleRepository, Depends(get_role_repository)],
    conflict_service: Annotated[AuthorizationPolicyConflictService, Depends(get_authorization_policy_conflict_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> HandoffRejectionOutcome:
    role = await role_repo.get_by_id(role_id)
    if role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No role found with id '{role_id}'.")
    return await conflict_service.classify_handoff_rejection("role", role, role_repo, request, actor_id=claims.get("person_id"))
