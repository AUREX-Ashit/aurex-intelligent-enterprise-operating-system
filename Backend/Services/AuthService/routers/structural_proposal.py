from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import require_platform_admin
from models.database import db_manager
from repositories.structural_proposal_repository import StructuralProposalRepository
from repositories.structural_change_intent_repository import StructuralChangeIntentRepository
from repositories.organization_node_repository import OrganizationNodeRepository
from schemas.structural_proposal import (
    ShapeStructuralProposalRequest,
    RefineStructuralProposalRequest,
    StructuralProposalResponse,
)
from services.structural_proposal_service import StructuralProposalService

router = APIRouter()


# ---------------------------------------------------------------------------
# Dependency factories
# ---------------------------------------------------------------------------

async def get_structural_proposal_service(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> StructuralProposalService:
    return StructuralProposalService(
        StructuralProposalRepository(session),
        StructuralChangeIntentRepository(session),
        OrganizationNodeRepository(session),
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post(
    "",
    response_model=StructuralProposalResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Shape a new structural proposal (revision 1)",
    description=(
        "WP-04 Business Activity: Shape Structural Proposal (C-005, "
        "ERB-C005-04/EX-C005-05 per PE-001-C005; POC-000001, ADR-008, "
        "IRA-004 §22). Requires the PLATFORM_ADMIN role. "
        "EnterpriseNode-only proposal target (ADR-007 v1 scope). "
        "Creates revision 1 of a new proposal."
    ),
    responses={
        201: {"description": "Structural proposal shaped (revision 1)."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "The referenced structural change intent or organization node does not exist."},
        422: {"description": "Invalid request (e.g., missing required field)."},
    },
)
async def shape_structural_proposal(
    request: ShapeStructuralProposalRequest,
    structural_proposal_service: Annotated[StructuralProposalService, Depends(get_structural_proposal_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> StructuralProposalResponse:
    """No tenant-scoping: StructuralProposal carries no organization_id column (models/structural_proposal.py's own docstring)."""
    proposal = await structural_proposal_service.shape_proposal(request, actor_id=claims.get("person_id"))
    return StructuralProposalResponse.model_validate(proposal)


@router.post(
    "/{proposal_id}/revisions",
    response_model=StructuralProposalResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Refine an existing structural proposal (next revision)",
    description=(
        "WP-04 Business Activity: Refine Structural Proposal (C-005, "
        "ERB-C005-04/EX-C005-06 per PE-001-C005). Requires the "
        "PLATFORM_ADMIN role. Append-only: inserts the next revision and "
        "marks the current revision SUPERSEDED — no revision's own "
        "content is ever overwritten."
    ),
    responses={
        201: {"description": "Structural proposal refined (next revision)."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        404: {"description": "No structural proposal exists with this proposal_id."},
        422: {"description": "Invalid request (e.g., missing required field)."},
    },
)
async def refine_structural_proposal(
    proposal_id: UUID,
    request: RefineStructuralProposalRequest,
    structural_proposal_service: Annotated[StructuralProposalService, Depends(get_structural_proposal_service)],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> StructuralProposalResponse:
    """No tenant-scoping, same basis as shape_structural_proposal above."""
    proposal = await structural_proposal_service.refine_proposal(
        proposal_id, request, actor_id=claims.get("person_id")
    )
    return StructuralProposalResponse.model_validate(proposal)
