from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import require_platform_admin
from models.database import db_manager
from models.domain_permission import VersionStatus
from repositories.domain_permission_repository import DomainPermissionRepository
from repositories.domain_repository import DomainRepository
from repositories.membership_repository import MembershipRepository
from repositories.organization_repository import OrganizationRepository
from schemas.authorization_policy_conflict import DependencyConflictReport, ResolveDependencyConflictRequest
from schemas.authorization_policy_handoff import HandoffRejectionOutcome, ReportHandoffRejectionRequest
from schemas.domain_permission import EstablishDomainPermissionRequest, DomainPermissionResponse, VersionDomainPermissionRequest
from services.authorization_policy_conflict_service import AuthorizationPolicyConflictService
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


async def get_organization_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> OrganizationRepository:
    return OrganizationRepository(session)


async def get_domain_permission_service(
    domain_permission_repo: Annotated[DomainPermissionRepository, Depends(get_domain_permission_repository)],
    domain_repo: Annotated[DomainRepository, Depends(get_domain_repository)],
    membership_repo: Annotated[MembershipRepository, Depends(get_membership_repository)],
) -> DomainPermissionService:
    return DomainPermissionService(domain_permission_repo, domain_repo, membership_repo)


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


@router.post(
    "/{domain_permission_id}/deprecate",
    response_model=DomainPermissionResponse,
    status_code=status.HTTP_200_OK,
    summary="Deprecate (Hide) a Domain Permission",
    description=(
        "WP-02 Business Activity: Deprecate or Retire Authorization "
        "Policy Object (C-003) — BA-08, realizing PE-001-C003's "
        "ERB-C003-02 / EX-C003-08. Transitions the current ACTIVE "
        "version to DEPRECATED (Hidden, URA-001-127) in place. "
        "Requires the PLATFORM_ADMIN role."
    ),
    responses={
        200: {"description": "Domain permission deprecated."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "The target Domain Permission does not exist."},
        409: {"description": "The target Domain Permission is not the current ACTIVE version, or has an active dependency remaining unresolved (BR-C003-04)."},
    },
)
async def deprecate_domain_permission(
    domain_permission_id: UUID,
    domain_permission_service: Annotated[DomainPermissionService, Depends(get_domain_permission_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> DomainPermissionResponse:
    domain_permission = await domain_permission_service.deprecate(domain_permission_id, actor_id=claims.get("person_id"))
    return DomainPermissionResponse.model_validate(domain_permission)


@router.post(
    "/{domain_permission_id}/retire",
    response_model=DomainPermissionResponse,
    status_code=status.HTTP_200_OK,
    summary="Retire (Archive) a Domain Permission",
    description=(
        "WP-02 Business Activity: Deprecate or Retire Authorization "
        "Policy Object (C-003) — BA-08, realizing PE-001-C003's "
        "ERB-C003-02 / EX-C003-08. Transitions the current ACTIVE "
        "version to RETIRED (Archived, URA-001-127) in place — terminal, "
        "never reversible. Requires the PLATFORM_ADMIN role."
    ),
    responses={
        200: {"description": "Domain permission retired."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "The target Domain Permission does not exist."},
        409: {"description": "The target Domain Permission is not the current ACTIVE version, or has an active dependency remaining unresolved (BR-C003-04)."},
    },
)
async def retire_domain_permission(
    domain_permission_id: UUID,
    domain_permission_service: Annotated[DomainPermissionService, Depends(get_domain_permission_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> DomainPermissionResponse:
    domain_permission = await domain_permission_service.retire(domain_permission_id, actor_id=claims.get("person_id"))
    return DomainPermissionResponse.model_validate(domain_permission)


@router.post(
    "/{domain_permission_id}/dependency-check",
    response_model=DependencyConflictReport,
    status_code=status.HTTP_200_OK,
    summary="Detect Authorization Policy Dependency Conflict for a Domain Permission",
    description=(
        "WP-02 Business Activity: Detect and Resolve Authorization "
        "Policy Dependency Conflict (C-003) — BA-09, realizing "
        "PE-001-C003's ERB-C003-03 / EX-C003-09. Requires the "
        "PLATFORM_ADMIN role."
    ),
    responses={
        200: {"description": "Dependency conflict report produced."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "The target Domain Permission does not exist."},
    },
)
async def check_domain_permission_dependencies(
    domain_permission_id: UUID,
    domain_permission_repo: Annotated[DomainPermissionRepository, Depends(get_domain_permission_repository)],
    conflict_service: Annotated[AuthorizationPolicyConflictService, Depends(get_authorization_policy_conflict_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> DependencyConflictReport:
    grant = await domain_permission_repo.get_by_id(domain_permission_id)
    if grant is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No domain permission found with id '{domain_permission_id}'.")
    return await conflict_service.detect_conflicts("domain_permission", grant, domain_permission_repo)


@router.post(
    "/{domain_permission_id}/resolve-dependency",
    response_model=DependencyConflictReport,
    status_code=status.HTTP_200_OK,
    summary="Resolve an Authorization Policy Dependency Conflict for a Domain Permission",
    description=(
        "WP-02 Business Activity: Detect and Resolve Authorization "
        "Policy Dependency Conflict (C-003) — BA-09, realizing "
        "PE-001-C003's ERB-C003-03 / EX-C003-09. Requires the "
        "PLATFORM_ADMIN role."
    ),
    responses={
        200: {"description": "Resolution recorded; current dependency conflict report returned."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "The target Domain Permission, or the supplied replacement_target_id, does not exist."},
        409: {"description": "The supplied replacement_target_id is not the current ACTIVE version."},
        422: {"description": "REASSIGNMENT_CONFIRMED requires replacement_target_id, or it names the object being replaced."},
    },
)
async def resolve_domain_permission_dependency(
    domain_permission_id: UUID,
    request: ResolveDependencyConflictRequest,
    domain_permission_repo: Annotated[DomainPermissionRepository, Depends(get_domain_permission_repository)],
    conflict_service: Annotated[AuthorizationPolicyConflictService, Depends(get_authorization_policy_conflict_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> DependencyConflictReport:
    grant = await domain_permission_repo.get_by_id(domain_permission_id)
    if grant is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No domain permission found with id '{domain_permission_id}'.")
    return await conflict_service.resolve_conflict("domain_permission", grant, domain_permission_repo, request, actor_id=claims.get("person_id"))


@router.post(
    "/{domain_permission_id}/handoff-rejection",
    response_model=HandoffRejectionOutcome,
    status_code=status.HTTP_200_OK,
    summary="Resolve a Dependent Capability Hand-off Rejection for a Domain Permission",
    description=(
        "WP-02 Business Activity: Resolve Dependent Capability "
        "Authorization Policy Hand-off Rejection (C-003) — BA-10, "
        "realizing PE-001-C003's ERB-C003-03 / EX-C003-10. Requires the "
        "PLATFORM_ADMIN role."
    ),
    responses={
        200: {"description": "Hand-off rejection classified."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "The target Domain Permission does not exist."},
    },
)
async def report_domain_permission_handoff_rejection(
    domain_permission_id: UUID,
    request: ReportHandoffRejectionRequest,
    domain_permission_repo: Annotated[DomainPermissionRepository, Depends(get_domain_permission_repository)],
    conflict_service: Annotated[AuthorizationPolicyConflictService, Depends(get_authorization_policy_conflict_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> HandoffRejectionOutcome:
    grant = await domain_permission_repo.get_by_id(domain_permission_id)
    if grant is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No domain permission found with id '{domain_permission_id}'.")
    return await conflict_service.classify_handoff_rejection("domain_permission", grant, domain_permission_repo, request, actor_id=claims.get("person_id"))


@router.get(
    "",
    response_model=list[DomainPermissionResponse],
    status_code=status.HTTP_200_OK,
    summary="List Domain Permissions matching an optional Domain, Membership, or status criterion",
    description=(
        "WP-06 Business Activity: Understand Domain Permission Context "
        "(C-003) — BA-01, realizing PE-001-C003 v1.1's EX-C003-11 "
        "filtered-list branch. Read-only — establishes, versions, "
        "deprecates, or retires nothing. domain_id, membership_id, and "
        "status are each independently optional; omitting all three "
        "returns every Domain Permission. Requires the PLATFORM_ADMIN "
        "role (same interim gate as BA-02, TD-022)."
    ),
    responses={
        200: {"description": "Matching Domain Permissions (possibly empty)."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
    },
)
async def list_domain_permissions(
    domain_permission_service: Annotated[DomainPermissionService, Depends(get_domain_permission_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
    domain_id: UUID | None = Query(None, description="Filter to Domain Permissions granted on this Domain."),
    membership_id: UUID | None = Query(None, description="Filter to Domain Permissions granted to this Membership."),
    status_filter: VersionStatus | None = Query(None, alias="status", description="Filter to Domain Permissions in this Status."),
) -> list[DomainPermissionResponse]:
    domain_permissions = await domain_permission_service.search(
        domain_id=domain_id,
        membership_id=membership_id,
        status_filter=status_filter.value if status_filter is not None else None,
    )
    return [DomainPermissionResponse.model_validate(dp) for dp in domain_permissions]


@router.get(
    "/{domain_permission_id}",
    response_model=DomainPermissionResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a Domain Permission's current governed state",
    description=(
        "WP-06 Business Activity: Understand Domain Permission Context "
        "(C-003) — BA-01, realizing PE-001-C003 v1.1's EX-C003-11 "
        "single-item branch. Read-only — establishes, versions, "
        "deprecates, or retires nothing. Requires the PLATFORM_ADMIN "
        "role (same interim gate as BA-02, TD-022)."
    ),
    responses={
        200: {"description": "The Domain Permission's current governed state."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "No Domain Permission exists with the given id."},
    },
)
async def get_domain_permission(
    domain_permission_id: UUID,
    domain_permission_service: Annotated[DomainPermissionService, Depends(get_domain_permission_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> DomainPermissionResponse:
    domain_permission = await domain_permission_service.get_by_id(domain_permission_id)
    return DomainPermissionResponse.model_validate(domain_permission)
