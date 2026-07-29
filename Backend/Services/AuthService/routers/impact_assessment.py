from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import require_platform_admin
from models.database import db_manager
from repositories.impact_assessment_repository import ImpactAssessmentRepository
from repositories.structural_proposal_repository import StructuralProposalRepository
from schemas.impact_assessment import AssessStructuralConsequenceRequest, ImpactAssessmentResponse
from services.impact_assessment_service import ImpactAssessmentService

router = APIRouter()


# ---------------------------------------------------------------------------
# Dependency factories
# ---------------------------------------------------------------------------

async def get_impact_assessment_service(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> ImpactAssessmentService:
    return ImpactAssessmentService(
        ImpactAssessmentRepository(session),
        StructuralProposalRepository(session),
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post(
    "",
    response_model=ImpactAssessmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Assess the structural consequence of a proposal revision",
    description=(
        "WP-04 Business Activity: Assess Structural Consequence (C-005, "
        "ERB-C005-05/EX-C005-07 per PE-001-C005; IMC-000001, ADR-009, "
        "IRA-004 §23). Requires the PLATFORM_ADMIN role. Computes and "
        "persists Impact Context for one specific proposal revision. "
        "Identifies downstream capability implications only — does not "
        "execute or trigger any downstream capability action "
        "(BR-C005-008)."
    ),
    responses={
        201: {"description": "Impact assessment created."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "The referenced structural proposal does not exist."},
        422: {"description": "Invalid request (e.g., missing required field)."},
    },
)
async def assess_structural_consequence(
    request: AssessStructuralConsequenceRequest,
    impact_assessment_service: Annotated[ImpactAssessmentService, Depends(get_impact_assessment_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> ImpactAssessmentResponse:
    """No tenant-scoping: ImpactAssessment carries no organization_id column (models/impact_assessment.py's own docstring)."""
    impact_assessment = await impact_assessment_service.assess_structural_consequence(
        request, actor_id=claims.get("person_id")
    )
    return ImpactAssessmentResponse.model_validate(impact_assessment)
