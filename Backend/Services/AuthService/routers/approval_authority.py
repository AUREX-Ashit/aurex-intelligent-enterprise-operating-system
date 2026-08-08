from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import enforce_domain_permission, get_current_claims, require_platform_admin
from models.approval_authority import ApprovalScopeType
from models.database import db_manager
from models.domain_permission import DomainPermissionLevel
from repositories.approval_authority_repository import ApprovalAuthorityRepository
from repositories.domain_repository import DomainRepository
from repositories.organization_repository import OrganizationRepository
from schemas.approval_authority import EstablishApprovalAuthorityRequest, ApprovalAuthorityResponse, VersionApprovalAuthorityRequest
from schemas.authorization_policy_conflict import DependencyConflictReport, ResolveDependencyConflictRequest
from schemas.authorization_policy_handoff import HandoffRejectionOutcome, ReportHandoffRejectionRequest
from services.approval_authority_service import ApprovalAuthorityService
from services.authorization_policy_conflict_service import AuthorizationPolicyConflictService

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
    response_model=ApprovalAuthorityResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Establish a new Approval Authority",
    description=(
        "WP-02 Business Activity: Establish Approval Authority (C-003), "
        "realizing PE-001-C003's ERB-C003-01 / EX-C003-03. For a DOMAIN-"
        "scoped Approval Authority, requires an active DomainPermission "
        "grant of ADMIN on the target Domain (URA-001-45 Domain Owner "
        "authority, realized via the Authorization Runtime Engine per "
        "WP-13 — the same mechanism `establish_domain_permission` uses; "
        "`TD-023`'s own interim PLATFORM_ADMIN-only gate remains a "
        "bypass, never narrowed). For GLOBAL, COMPANY, or OBJECT scope, "
        "the interim PLATFORM_ADMIN-only gate is unchanged — URA-001-32 "
        "Corporate Admin authority remains unmodeled (`TD-023`, `TD-021`'s "
        "own ADR-002 root cause), and no authority is named anywhere for "
        "OBJECT scope. Declares exactly one approval_strategy and "
        "exactly one scope_type (GLOBAL/COMPANY/DOMAIN/OBJECT, "
        "URA-001-61); an ambiguous, dual-stated, or incomplete scope is "
        "rejected with 422. Rejects an unknown Organization or Domain "
        "with 404."
    ),
    responses={
        201: {"description": "Approval Authority established."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold PLATFORM_ADMIN; for DOMAIN scope, an active ADMIN-level DomainPermission grant on the target Domain also satisfies this."},
        404: {"description": "The target Organization or Domain does not exist."},
        422: {"description": "Invalid request (e.g., scope_type's required anchor missing, or an anchor supplied for the wrong scope_type)."},
    },
)
async def establish_approval_authority(
    request: EstablishApprovalAuthorityRequest,
    approval_authority_service: Annotated[ApprovalAuthorityService, Depends(get_approval_authority_service)],
    claims: Annotated[dict, Depends(get_current_claims)],
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> ApprovalAuthorityResponse:
    if request.scope_type == ApprovalScopeType.DOMAIN:
        await enforce_domain_permission(claims, session, request.domain_id, DomainPermissionLevel.ADMIN)
    elif claims.get("role_code") != "PLATFORM_ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Establishing a GLOBAL, COMPANY, or OBJECT-scoped Approval Authority requires the PLATFORM_ADMIN role.",
        )
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


@router.post(
    "/{approval_authority_id}/deprecate",
    response_model=ApprovalAuthorityResponse,
    status_code=status.HTTP_200_OK,
    summary="Deprecate (Hide) an Approval Authority",
    description=(
        "WP-02 Business Activity: Deprecate or Retire Authorization "
        "Policy Object (C-003) — BA-08, realizing PE-001-C003's "
        "ERB-C003-02 / EX-C003-08. Transitions the current ACTIVE "
        "version to DEPRECATED (Hidden, URA-001-127) in place. "
        "Requires the PLATFORM_ADMIN role."
    ),
    responses={
        200: {"description": "Approval authority deprecated."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "The target Approval Authority does not exist."},
        409: {"description": "The target Approval Authority is not the current ACTIVE version, has no resolvable owning organization, or has an active dependency remaining unresolved (BR-C003-04)."},
    },
)
async def deprecate_approval_authority(
    approval_authority_id: UUID,
    approval_authority_service: Annotated[ApprovalAuthorityService, Depends(get_approval_authority_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> ApprovalAuthorityResponse:
    approval_authority = await approval_authority_service.deprecate(approval_authority_id, actor_id=claims.get("person_id"))
    return ApprovalAuthorityResponse.model_validate(approval_authority)


@router.post(
    "/{approval_authority_id}/retire",
    response_model=ApprovalAuthorityResponse,
    status_code=status.HTTP_200_OK,
    summary="Retire (Archive) an Approval Authority",
    description=(
        "WP-02 Business Activity: Deprecate or Retire Authorization "
        "Policy Object (C-003) — BA-08, realizing PE-001-C003's "
        "ERB-C003-02 / EX-C003-08. Transitions the current ACTIVE "
        "version to RETIRED (Archived, URA-001-127) in place — terminal, "
        "never reversible. Requires the PLATFORM_ADMIN role."
    ),
    responses={
        200: {"description": "Approval authority retired."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "The target Approval Authority does not exist."},
        409: {"description": "The target Approval Authority is not the current ACTIVE version, has no resolvable owning organization, or has an active dependency remaining unresolved (BR-C003-04)."},
    },
)
async def retire_approval_authority(
    approval_authority_id: UUID,
    approval_authority_service: Annotated[ApprovalAuthorityService, Depends(get_approval_authority_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> ApprovalAuthorityResponse:
    approval_authority = await approval_authority_service.retire(approval_authority_id, actor_id=claims.get("person_id"))
    return ApprovalAuthorityResponse.model_validate(approval_authority)


@router.post(
    "/{approval_authority_id}/dependency-check",
    response_model=DependencyConflictReport,
    status_code=status.HTTP_200_OK,
    summary="Detect Authorization Policy Dependency Conflict for an Approval Authority",
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
        404: {"description": "The target Approval Authority does not exist."},
    },
)
async def check_approval_authority_dependencies(
    approval_authority_id: UUID,
    approval_authority_repo: Annotated[ApprovalAuthorityRepository, Depends(get_approval_authority_repository)],
    conflict_service: Annotated[AuthorizationPolicyConflictService, Depends(get_authorization_policy_conflict_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> DependencyConflictReport:
    authority = await approval_authority_repo.get_by_id(approval_authority_id)
    if authority is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No approval authority found with id '{approval_authority_id}'.")
    return await conflict_service.detect_conflicts("approval_authority", authority, approval_authority_repo)


@router.post(
    "/{approval_authority_id}/resolve-dependency",
    response_model=DependencyConflictReport,
    status_code=status.HTTP_200_OK,
    summary="Resolve an Authorization Policy Dependency Conflict for an Approval Authority",
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
        404: {"description": "The target Approval Authority, or the supplied replacement_target_id, does not exist."},
        409: {"description": "The supplied replacement_target_id is not the current ACTIVE version."},
        422: {"description": "REASSIGNMENT_CONFIRMED requires replacement_target_id, or it names the object being replaced."},
    },
)
async def resolve_approval_authority_dependency(
    approval_authority_id: UUID,
    request: ResolveDependencyConflictRequest,
    approval_authority_repo: Annotated[ApprovalAuthorityRepository, Depends(get_approval_authority_repository)],
    conflict_service: Annotated[AuthorizationPolicyConflictService, Depends(get_authorization_policy_conflict_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> DependencyConflictReport:
    authority = await approval_authority_repo.get_by_id(approval_authority_id)
    if authority is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No approval authority found with id '{approval_authority_id}'.")
    return await conflict_service.resolve_conflict("approval_authority", authority, approval_authority_repo, request, actor_id=claims.get("person_id"))


@router.post(
    "/{approval_authority_id}/handoff-rejection",
    response_model=HandoffRejectionOutcome,
    status_code=status.HTTP_200_OK,
    summary="Resolve a Dependent Capability Hand-off Rejection for an Approval Authority",
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
        404: {"description": "The target Approval Authority does not exist."},
    },
)
async def report_approval_authority_handoff_rejection(
    approval_authority_id: UUID,
    request: ReportHandoffRejectionRequest,
    approval_authority_repo: Annotated[ApprovalAuthorityRepository, Depends(get_approval_authority_repository)],
    conflict_service: Annotated[AuthorizationPolicyConflictService, Depends(get_authorization_policy_conflict_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> HandoffRejectionOutcome:
    authority = await approval_authority_repo.get_by_id(approval_authority_id)
    if authority is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No approval authority found with id '{approval_authority_id}'.")
    return await conflict_service.classify_handoff_rejection("approval_authority", authority, approval_authority_repo, request, actor_id=claims.get("person_id"))
