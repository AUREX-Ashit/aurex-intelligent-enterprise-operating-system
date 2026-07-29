from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import require_platform_admin
from models.database import db_manager
from repositories.structural_change_intent_repository import StructuralChangeIntentRepository
from schemas.structural_change_intent import FrameStructuralChangeIntentRequest, StructuralChangeIntentResponse
from services.structural_change_intent_service import StructuralChangeIntentService

router = APIRouter()


# ---------------------------------------------------------------------------
# Dependency factories
# ---------------------------------------------------------------------------

async def get_structural_change_intent_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> StructuralChangeIntentRepository:
    return StructuralChangeIntentRepository(session)


async def get_structural_change_intent_service(
    structural_change_intent_repo: Annotated[
        StructuralChangeIntentRepository, Depends(get_structural_change_intent_repository)
    ],
) -> StructuralChangeIntentService:
    return StructuralChangeIntentService(structural_change_intent_repo)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post(
    "",
    response_model=StructuralChangeIntentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Frame a new structural change intent",
    description=(
        "WP-04 Business Activity: Frame Structural Change Intent (C-005, "
        "ERB-C005-03/EX-C005-04 per PE-001-C005; SCI-000001, ADR-006, "
        "IRA-004 §21). Requires the PLATFORM_ADMIN role (same interim "
        "gate WP-01/02/03/WP-04 BA-01/BA-02 all used). Persists a new "
        "Structural Change Intent in the CREATED lifecycle state only — "
        "no structural target binding (BA-04's own future scope) is "
        "accepted or persisted here."
    ),
    responses={
        201: {"description": "Structural change intent framed."},
        400: {"description": "Missing or malformed Authorization header."},
        401: {"description": "Access token invalid or expired."},
        403: {"description": "Caller does not hold the PLATFORM_ADMIN role."},
        422: {"description": "Invalid request (e.g., missing required field)."},
    },
)
async def frame_structural_change_intent(
    request: FrameStructuralChangeIntentRequest,
    structural_change_intent_service: Annotated[
        StructuralChangeIntentService, Depends(get_structural_change_intent_service)
    ],
    claims: Annotated[dict, Depends(require_platform_admin)],
) -> StructuralChangeIntentResponse:
    """
    No tenant-scoping: StructuralChangeIntent carries no organization_id
    column (models/structural_change_intent.py's own docstring) — an
    enterprise-structure-level construct, the same basis
    routers/organization_node.py documents for OrganizationNode. See
    also middleware/tenant.py's exemption list, which this path is
    added to.
    """
    structural_change_intent = await structural_change_intent_service.frame_change_intent(
        request, actor_id=claims.get("person_id")
    )
    return StructuralChangeIntentResponse.model_validate(structural_change_intent)
