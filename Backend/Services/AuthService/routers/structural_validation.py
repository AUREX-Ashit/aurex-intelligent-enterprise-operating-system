from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import require_platform_admin
from models.database import db_manager
from repositories.structural_validation_repository import StructuralValidationRepository
from repositories.structural_proposal_repository import StructuralProposalRepository
from repositories.structural_review_repository import StructuralReviewRepository
from schemas.structural_validation import ValidateTransitionReadinessRequest, StructuralValidationResponse
from services.structural_validation_service import StructuralValidationService

router = APIRouter()


# ---------------------------------------------------------------------------
# Dependency factories
# ---------------------------------------------------------------------------

async def get_structural_validation_service(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> StructuralValidationService:
    return StructuralValidationService(
        StructuralValidationRepository(session),
        StructuralProposalRepository(session),
        StructuralReviewRepository(session),
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post(
    "",
    response_model=StructuralValidationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Validate structural transition readiness",
    description=(
        "WP-04 Business Activity: Validate Transition Readiness (C-005, "
        "ERB-C005-07/EX-C005-10 per PE-001-C005; VLC-000001, ADR-012, "
        "IRA-004 §26). Requires the PLATFORM_ADMIN role. Hard-enforces "
        "BR-C005-007: rejects (409) if the referenced review's concerns "
        "are not CONCERNS_RESOLVED, or if the review does not belong to "
        "the referenced proposal. Every successfully created row "
        "represents a 'ready' validation by construction — the "
        "'return-to-resolution' outcome is realized as a 409 rejection, "
        "never as a persisted row."
    ),
    responses={
        201: {"description": "Structural transition readiness validated."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "The referenced structural proposal or structural review does not exist."},
        409: {"description": "The review does not belong to the proposal, or its concerns are not yet resolved (BR-C005-007)."},
        422: {"description": "Invalid request (e.g., missing required field)."},
    },
)
async def validate_transition_readiness(
    request: ValidateTransitionReadinessRequest,
    structural_validation_service: Annotated[StructuralValidationService, Depends(get_structural_validation_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> StructuralValidationResponse:
    """No tenant-scoping: StructuralValidation carries no organization_id column (models/structural_validation.py's own docstring)."""
    validation = await structural_validation_service.validate_transition_readiness(
        request, actor_id=claims.get("person_id")
    )
    return StructuralValidationResponse.model_validate(validation)
