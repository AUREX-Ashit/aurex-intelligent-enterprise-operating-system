from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import require_platform_admin
from models.database import db_manager
from repositories.structural_review_repository import StructuralReviewRepository
from repositories.structural_proposal_repository import StructuralProposalRepository
from schemas.structural_review import (
    CreateStructuralReviewRequest,
    ResolveStructuralReviewConcernsRequest,
    StructuralReviewResponse,
)
from services.structural_review_service import StructuralReviewService

router = APIRouter()


# ---------------------------------------------------------------------------
# Dependency factories
# ---------------------------------------------------------------------------

async def get_structural_review_service(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> StructuralReviewService:
    return StructuralReviewService(
        StructuralReviewRepository(session),
        StructuralProposalRepository(session),
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post(
    "",
    response_model=StructuralReviewResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Review a proposed structural outcome",
    description=(
        "WP-04 Business Activity: Review Proposed Structural Outcome "
        "(C-005, ERB-C005-06/EX-C005-08 per PE-001-C005; RVC-000001, "
        "ADR-011, IRA-004 §25). Requires the PLATFORM_ADMIN role. "
        "Creates a Review Context for one specific proposal revision."
    ),
    responses={
        201: {"description": "Structural review created."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "The referenced structural proposal does not exist."},
        422: {"description": "Invalid request (e.g., missing required field)."},
    },
)
async def create_structural_review(
    request: CreateStructuralReviewRequest,
    structural_review_service: Annotated[StructuralReviewService, Depends(get_structural_review_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> StructuralReviewResponse:
    """No tenant-scoping: StructuralReview carries no organization_id column (models/structural_review.py's own docstring)."""
    review = await structural_review_service.create_review(request, actor_id=claims.get("person_id"))
    return StructuralReviewResponse.model_validate(review)


@router.post(
    "/{review_id}/resolve-concerns",
    response_model=StructuralReviewResponse,
    status_code=status.HTTP_200_OK,
    summary="Resolve a structural review's concerns",
    description=(
        "WP-04 Business Activity: Resolve Structural Review Concerns "
        "(C-005, ERB-C005-06/EX-C005-09 per PE-001-C005). Requires the "
        "PLATFORM_ADMIN role. Updates this Review Context row only — "
        "does not create or modify any structural proposal revision "
        "(that remains BA-04's own scope, POST "
        "/structural-proposals/{proposal_id}/revisions)."
    ),
    responses={
        200: {"description": "Structural review concerns resolved."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "No structural review exists with this id."},
        409: {"description": "The structural review is not open for concern resolution."},
        422: {"description": "Invalid request."},
    },
)
async def resolve_structural_review_concerns(
    review_id: UUID,
    request: ResolveStructuralReviewConcernsRequest,
    structural_review_service: Annotated[StructuralReviewService, Depends(get_structural_review_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> StructuralReviewResponse:
    """No tenant-scoping, same basis as create_structural_review above."""
    review = await structural_review_service.resolve_concerns(
        review_id, request, actor_id=claims.get("person_id")
    )
    return StructuralReviewResponse.model_validate(review)
