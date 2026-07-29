from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import require_platform_admin
from models.database import db_manager
from repositories.structural_completion_repository import StructuralCompletionRepository
from repositories.structural_validation_repository import StructuralValidationRepository
from schemas.structural_completion import CompleteStructuralTransitionRequest, StructuralCompletionResponse
from services.structural_completion_service import StructuralCompletionService

router = APIRouter()


# ---------------------------------------------------------------------------
# Dependency factories
# ---------------------------------------------------------------------------

async def get_structural_completion_service(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> StructuralCompletionService:
    return StructuralCompletionService(
        StructuralCompletionRepository(session),
        StructuralValidationRepository(session),
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post(
    "",
    response_model=StructuralCompletionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Complete a validated structural transition",
    description=(
        "WP-04 Business Activity: Complete Structural Transition (C-005, "
        "ERB-C005-08/EX-C005-11 per PE-001-C005; RSC-000001, ADR-013, "
        "IRA-004 §27). Requires the PLATFORM_ADMIN role. **Option A "
        "scope:** records completion of the governed structural "
        "transition only — does not modify organization_nodes, does "
        "not create organization_hierarchy or "
        "consolidation_determination, and does not infer a structural "
        "change from the proposal's own free text (TD-070). "
        "Completion is a guarded transition: a second completion "
        "attempt for the same structural_validation_id is rejected "
        "with 409."
    ),
    responses={
        201: {"description": "Structural transition completed."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "The referenced structural validation does not exist."},
        409: {"description": "The structural validation has already been completed."},
        422: {"description": "Invalid request (e.g., missing required field)."},
    },
)
async def complete_structural_transition(
    request: CompleteStructuralTransitionRequest,
    structural_completion_service: Annotated[StructuralCompletionService, Depends(get_structural_completion_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> StructuralCompletionResponse:
    """No tenant-scoping: StructuralCompletion carries no organization_id column (models/structural_completion.py's own docstring)."""
    completion = await structural_completion_service.complete_structural_transition(
        request, actor_id=claims.get("person_id")
    )
    return StructuralCompletionResponse.model_validate(completion)


@router.get(
    "/{completion_id}",
    response_model=StructuralCompletionResponse,
    status_code=status.HTTP_200_OK,
    summary="View a completed structural transition",
    description=(
        "WP-04 Business Activity: Continue from Resulting Structure "
        "(C-005, ERB-C005-08/EX-C005-12 per PE-001-C005). Requires the "
        "PLATFORM_ADMIN role. Returns the completion's own fields "
        "verbatim — the existing StructuralCompletionResponse shape, "
        "not enriched with the upstream Structural Change Intent / "
        "Proposal / Review / Validation chain, and no separate "
        "\"downstream continuation\" object (BA-09's own readiness "
        "assessment: not a canonical Business Object, per EX-C005-12's "
        "own Invalidated Context: \"C-005-only transient context not "
        "required downstream\")."
    ),
    responses={
        200: {"description": "Structural completion found."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "No structural completion exists with this id."},
        422: {"description": "completion_id is not a valid UUID."},
    },
)
async def get_structural_completion(
    completion_id: UUID,
    structural_completion_service: Annotated[StructuralCompletionService, Depends(get_structural_completion_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> StructuralCompletionResponse:
    """No tenant-scoping, same basis as complete_structural_transition above."""
    completion = await structural_completion_service.get_details(completion_id)
    return StructuralCompletionResponse.model_validate(completion)
