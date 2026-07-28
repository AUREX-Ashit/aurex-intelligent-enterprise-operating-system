from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import require_platform_admin
from models.database import db_manager
from repositories.runtime_assignment_policy_repository import RuntimeAssignmentPolicyRepository
from repositories.organization_repository import OrganizationRepository
from schemas.runtime_assignment_policy import (
    EstablishRuntimeAssignmentPolicyRequest,
    RuntimeAssignmentPolicyResponse,
    VersionRuntimeAssignmentPolicyRequest,
)
from services.runtime_assignment_policy_service import RuntimeAssignmentPolicyService

router = APIRouter()


# ---------------------------------------------------------------------------
# Dependency factories
# ---------------------------------------------------------------------------

async def get_runtime_assignment_policy_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> RuntimeAssignmentPolicyRepository:
    return RuntimeAssignmentPolicyRepository(session)


async def get_organization_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> OrganizationRepository:
    return OrganizationRepository(session)


async def get_runtime_assignment_policy_service(
    runtime_assignment_policy_repo: Annotated[RuntimeAssignmentPolicyRepository, Depends(get_runtime_assignment_policy_repository)],
    organization_repo: Annotated[OrganizationRepository, Depends(get_organization_repository)],
) -> RuntimeAssignmentPolicyService:
    return RuntimeAssignmentPolicyService(runtime_assignment_policy_repo, organization_repo)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post(
    "",
    response_model=RuntimeAssignmentPolicyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Establish a new Runtime Assignment Policy",
    description=(
        "WP-02 Business Activity: Establish Runtime Assignment Policy (C-003), "
        "realizing PE-001-C003's ERB-C003-01 / EX-C003-05. Requires the "
        "PLATFORM_ADMIN role (interim gate, mirroring BA-01/BA-02/BA-03/BA-04 — "
        "confirmed Corporate Admin/Domain Admin authority is not yet "
        "implementable, tracked as technical debt). Declares exactly one "
        "assignment_target_type (NAMED_USER/BUSINESS_ROLE/GROUP/EXTERNAL_USER, "
        "URA-001-75) and a configured lifecycle-states set (URA-001-78, "
        "defaulting to the nine canonical states). Governs future Runtime "
        "Assignment instances (out of this capability's own scope) — never "
        "establishes a specific assignment instance itself. Rejects an "
        "unknown Organization with 404."
    ),
    responses={
        201: {"description": "Runtime Assignment Policy established."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "The target Organization does not exist."},
        422: {"description": "Invalid request (e.g., an unrecognized assignment_target_type, or an empty configured_lifecycle_states list)."},
    },
)
async def establish_runtime_assignment_policy(
    request: EstablishRuntimeAssignmentPolicyRequest,
    runtime_assignment_policy_service: Annotated[RuntimeAssignmentPolicyService, Depends(get_runtime_assignment_policy_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> RuntimeAssignmentPolicyResponse:
    runtime_assignment_policy = await runtime_assignment_policy_service.establish(request, actor_id=claims.get("person_id"))
    return RuntimeAssignmentPolicyResponse.model_validate(runtime_assignment_policy)


@router.post(
    "/{runtime_assignment_policy_id}/versions",
    response_model=RuntimeAssignmentPolicyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Version and re-effective-date a Runtime Assignment Policy",
    description=(
        "WP-02 Business Activity: Version and Re-effective-Date "
        "Authorization Policy Object (C-003), realizing PE-001-C003's "
        "ERB-C003-02 / EX-C003-07. Amends policy_name/"
        "configured_lifecycle_states/escalation_policy_id and/or the "
        "effective-date window without changing assignment_target_type "
        "(outside this Business Activity's non-breaking scope). "
        "Preserves the prior version as an inspectable, SUPERSEDED "
        "historical record (BR-C003-05). Requires the PLATFORM_ADMIN "
        "role (same interim gate as BA-05)."
    ),
    responses={
        201: {"description": "New version established; prior version preserved as SUPERSEDED."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "The target Runtime Assignment Policy does not exist."},
        409: {"description": "The target Runtime Assignment Policy id does not name the current ACTIVE version."},
        422: {"description": "Invalid request."},
    },
)
async def version_runtime_assignment_policy(
    runtime_assignment_policy_id: UUID,
    request: VersionRuntimeAssignmentPolicyRequest,
    runtime_assignment_policy_service: Annotated[RuntimeAssignmentPolicyService, Depends(get_runtime_assignment_policy_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> RuntimeAssignmentPolicyResponse:
    runtime_assignment_policy = await runtime_assignment_policy_service.create_new_version(
        runtime_assignment_policy_id, request, actor_id=claims.get("person_id")
    )
    return RuntimeAssignmentPolicyResponse.model_validate(runtime_assignment_policy)


@router.post(
    "/{runtime_assignment_policy_id}/deprecate",
    response_model=RuntimeAssignmentPolicyResponse,
    status_code=status.HTTP_200_OK,
    summary="Deprecate (Hide) a Runtime Assignment Policy",
    description=(
        "WP-02 Business Activity: Deprecate or Retire Authorization "
        "Policy Object (C-003) — BA-08, realizing PE-001-C003's "
        "ERB-C003-02 / EX-C003-08. Transitions the current ACTIVE "
        "version to DEPRECATED (Hidden, URA-001-127) in place. "
        "Requires the PLATFORM_ADMIN role."
    ),
    responses={
        200: {"description": "Runtime assignment policy deprecated."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "The target Runtime Assignment Policy does not exist."},
        409: {"description": "The target Runtime Assignment Policy is not the current ACTIVE version, has no resolvable owning organization, or has an active dependency remaining unresolved (BR-C003-04)."},
    },
)
async def deprecate_runtime_assignment_policy(
    runtime_assignment_policy_id: UUID,
    runtime_assignment_policy_service: Annotated[RuntimeAssignmentPolicyService, Depends(get_runtime_assignment_policy_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> RuntimeAssignmentPolicyResponse:
    runtime_assignment_policy = await runtime_assignment_policy_service.deprecate(
        runtime_assignment_policy_id, actor_id=claims.get("person_id")
    )
    return RuntimeAssignmentPolicyResponse.model_validate(runtime_assignment_policy)


@router.post(
    "/{runtime_assignment_policy_id}/retire",
    response_model=RuntimeAssignmentPolicyResponse,
    status_code=status.HTTP_200_OK,
    summary="Retire (Archive) a Runtime Assignment Policy",
    description=(
        "WP-02 Business Activity: Deprecate or Retire Authorization "
        "Policy Object (C-003) — BA-08, realizing PE-001-C003's "
        "ERB-C003-02 / EX-C003-08. Transitions the current ACTIVE "
        "version to RETIRED (Archived, URA-001-127) in place — terminal, "
        "never reversible. Requires the PLATFORM_ADMIN role."
    ),
    responses={
        200: {"description": "Runtime assignment policy retired."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "The target Runtime Assignment Policy does not exist."},
        409: {"description": "The target Runtime Assignment Policy is not the current ACTIVE version, has no resolvable owning organization, or has an active dependency remaining unresolved (BR-C003-04)."},
    },
)
async def retire_runtime_assignment_policy(
    runtime_assignment_policy_id: UUID,
    runtime_assignment_policy_service: Annotated[RuntimeAssignmentPolicyService, Depends(get_runtime_assignment_policy_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> RuntimeAssignmentPolicyResponse:
    runtime_assignment_policy = await runtime_assignment_policy_service.retire(
        runtime_assignment_policy_id, actor_id=claims.get("person_id")
    )
    return RuntimeAssignmentPolicyResponse.model_validate(runtime_assignment_policy)
