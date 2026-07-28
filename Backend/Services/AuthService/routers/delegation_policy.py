from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import require_platform_admin
from models.database import db_manager
from repositories.delegation_policy_repository import DelegationPolicyRepository
from repositories.domain_repository import DomainRepository
from repositories.organization_repository import OrganizationRepository
from schemas.authorization_policy_conflict import DependencyConflictReport, ResolveDependencyConflictRequest
from schemas.delegation_policy import EstablishDelegationPolicyRequest, DelegationPolicyResponse, VersionDelegationPolicyRequest
from services.authorization_policy_conflict_service import AuthorizationPolicyConflictService
from services.delegation_policy_service import DelegationPolicyService

router = APIRouter()


# ---------------------------------------------------------------------------
# Dependency factories
# ---------------------------------------------------------------------------

async def get_delegation_policy_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> DelegationPolicyRepository:
    return DelegationPolicyRepository(session)


async def get_organization_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> OrganizationRepository:
    return OrganizationRepository(session)


async def get_domain_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> DomainRepository:
    return DomainRepository(session)


async def get_delegation_policy_service(
    delegation_policy_repo: Annotated[DelegationPolicyRepository, Depends(get_delegation_policy_repository)],
    organization_repo: Annotated[OrganizationRepository, Depends(get_organization_repository)],
    domain_repo: Annotated[DomainRepository, Depends(get_domain_repository)],
) -> DelegationPolicyService:
    return DelegationPolicyService(delegation_policy_repo, organization_repo, domain_repo)


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
    response_model=DelegationPolicyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Establish a new Delegation Policy",
    description=(
        "WP-02 Business Activity: Establish Delegation Policy (C-003), "
        "realizing PE-001-C003's ERB-C003-01 / EX-C003-04. Requires the "
        "PLATFORM_ADMIN role (interim gate, mirroring BA-01/BA-02/BA-03 — "
        "confirmed Corporate Admin/Domain Owner authority is not yet "
        "implementable, tracked as technical debt). Declares exactly one "
        "delegation_type and exactly one scope_type (ORGANIZATION/DOMAIN/"
        "OBJECT/EVENT, URA-001-89); an ambiguous, dual-stated, or "
        "incomplete scope is rejected with 422. Governs future delegation "
        "instances (out of this capability's own scope) — never "
        "establishes a specific delegator/delegatee pairing itself. "
        "Rejects an unknown Organization or Domain with 404."
    ),
    responses={
        201: {"description": "Delegation Policy established."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "The target Organization or Domain does not exist."},
        422: {"description": "Invalid request (e.g., scope_type's required anchor missing, or an anchor supplied for the wrong scope_type)."},
    },
)
async def establish_delegation_policy(
    request: EstablishDelegationPolicyRequest,
    delegation_policy_service: Annotated[DelegationPolicyService, Depends(get_delegation_policy_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> DelegationPolicyResponse:
    delegation_policy = await delegation_policy_service.establish(request, actor_id=claims.get("person_id"))
    return DelegationPolicyResponse.model_validate(delegation_policy)


@router.post(
    "/{delegation_policy_id}/versions",
    response_model=DelegationPolicyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Version and re-effective-date a Delegation Policy",
    description=(
        "WP-02 Business Activity: Version and Re-effective-Date "
        "Authorization Policy Object (C-003), realizing PE-001-C003's "
        "ERB-C003-02 / EX-C003-07. Amends policy_name/"
        "sub_delegation_allowed and/or the effective-date window without "
        "changing delegation_type or scope (outside this Business "
        "Activity's non-breaking scope). Preserves the prior version as "
        "an inspectable, SUPERSEDED historical record (BR-C003-05). "
        "Requires the PLATFORM_ADMIN role (same interim gate as BA-04)."
    ),
    responses={
        201: {"description": "New version established; prior version preserved as SUPERSEDED."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "The target Delegation Policy does not exist."},
        409: {"description": "The target Delegation Policy id does not name the current ACTIVE version."},
        422: {"description": "Invalid request."},
    },
)
async def version_delegation_policy(
    delegation_policy_id: UUID,
    request: VersionDelegationPolicyRequest,
    delegation_policy_service: Annotated[DelegationPolicyService, Depends(get_delegation_policy_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> DelegationPolicyResponse:
    delegation_policy = await delegation_policy_service.create_new_version(
        delegation_policy_id, request, actor_id=claims.get("person_id")
    )
    return DelegationPolicyResponse.model_validate(delegation_policy)


@router.post(
    "/{delegation_policy_id}/deprecate",
    response_model=DelegationPolicyResponse,
    status_code=status.HTTP_200_OK,
    summary="Deprecate (Hide) a Delegation Policy",
    description=(
        "WP-02 Business Activity: Deprecate or Retire Authorization "
        "Policy Object (C-003) — BA-08, realizing PE-001-C003's "
        "ERB-C003-02 / EX-C003-08. Transitions the current ACTIVE "
        "version to DEPRECATED (Hidden, URA-001-127) in place. "
        "Requires the PLATFORM_ADMIN role."
    ),
    responses={
        200: {"description": "Delegation policy deprecated."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "The target Delegation Policy does not exist."},
        409: {"description": "The target Delegation Policy is not the current ACTIVE version, has no resolvable owning organization, or has an active dependency remaining unresolved (BR-C003-04)."},
    },
)
async def deprecate_delegation_policy(
    delegation_policy_id: UUID,
    delegation_policy_service: Annotated[DelegationPolicyService, Depends(get_delegation_policy_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> DelegationPolicyResponse:
    delegation_policy = await delegation_policy_service.deprecate(delegation_policy_id, actor_id=claims.get("person_id"))
    return DelegationPolicyResponse.model_validate(delegation_policy)


@router.post(
    "/{delegation_policy_id}/retire",
    response_model=DelegationPolicyResponse,
    status_code=status.HTTP_200_OK,
    summary="Retire (Archive) a Delegation Policy",
    description=(
        "WP-02 Business Activity: Deprecate or Retire Authorization "
        "Policy Object (C-003) — BA-08, realizing PE-001-C003's "
        "ERB-C003-02 / EX-C003-08. Transitions the current ACTIVE "
        "version to RETIRED (Archived, URA-001-127) in place — terminal, "
        "never reversible. Requires the PLATFORM_ADMIN role."
    ),
    responses={
        200: {"description": "Delegation policy retired."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "The target Delegation Policy does not exist."},
        409: {"description": "The target Delegation Policy is not the current ACTIVE version, has no resolvable owning organization, or has an active dependency remaining unresolved (BR-C003-04)."},
    },
)
async def retire_delegation_policy(
    delegation_policy_id: UUID,
    delegation_policy_service: Annotated[DelegationPolicyService, Depends(get_delegation_policy_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> DelegationPolicyResponse:
    delegation_policy = await delegation_policy_service.retire(delegation_policy_id, actor_id=claims.get("person_id"))
    return DelegationPolicyResponse.model_validate(delegation_policy)


@router.post(
    "/{delegation_policy_id}/dependency-check",
    response_model=DependencyConflictReport,
    status_code=status.HTTP_200_OK,
    summary="Detect Authorization Policy Dependency Conflict for a Delegation Policy",
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
        404: {"description": "The target Delegation Policy does not exist."},
    },
)
async def check_delegation_policy_dependencies(
    delegation_policy_id: UUID,
    delegation_policy_repo: Annotated[DelegationPolicyRepository, Depends(get_delegation_policy_repository)],
    conflict_service: Annotated[AuthorizationPolicyConflictService, Depends(get_authorization_policy_conflict_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> DependencyConflictReport:
    policy = await delegation_policy_repo.get_by_id(delegation_policy_id)
    if policy is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No delegation policy found with id '{delegation_policy_id}'.")
    return await conflict_service.detect_conflicts("delegation_policy", policy, delegation_policy_repo)


@router.post(
    "/{delegation_policy_id}/resolve-dependency",
    response_model=DependencyConflictReport,
    status_code=status.HTTP_200_OK,
    summary="Resolve an Authorization Policy Dependency Conflict for a Delegation Policy",
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
        404: {"description": "The target Delegation Policy, or the supplied replacement_target_id, does not exist."},
        409: {"description": "The supplied replacement_target_id is not the current ACTIVE version."},
        422: {"description": "REASSIGNMENT_CONFIRMED requires replacement_target_id, or it names the object being replaced."},
    },
)
async def resolve_delegation_policy_dependency(
    delegation_policy_id: UUID,
    request: ResolveDependencyConflictRequest,
    delegation_policy_repo: Annotated[DelegationPolicyRepository, Depends(get_delegation_policy_repository)],
    conflict_service: Annotated[AuthorizationPolicyConflictService, Depends(get_authorization_policy_conflict_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> DependencyConflictReport:
    policy = await delegation_policy_repo.get_by_id(delegation_policy_id)
    if policy is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No delegation policy found with id '{delegation_policy_id}'.")
    return await conflict_service.resolve_conflict("delegation_policy", policy, delegation_policy_repo, request, actor_id=claims.get("person_id"))
