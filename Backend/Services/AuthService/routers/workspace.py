from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_current_claims
from models.database import db_manager
from repositories.membership_repository import MembershipRepository
from schemas.workspace import WorkspaceCandidatesResponse
from services.workspace_resolution_service import WorkspaceResolutionService

router = APIRouter()


# ---------------------------------------------------------------------------
# Dependency factories
# ---------------------------------------------------------------------------

async def get_membership_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> MembershipRepository:
    return MembershipRepository(session)


async def get_workspace_resolution_service(
    membership_repo: Annotated[MembershipRepository, Depends(get_membership_repository)],
) -> WorkspaceResolutionService:
    return WorkspaceResolutionService(membership_repo)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get(
    "/candidates",
    response_model=WorkspaceCandidatesResponse,
    status_code=status.HTTP_200_OK,
    summary="Resolve and present available Workspace candidates (WP-09 BA-01, EX-C008-01/02)",
    description=(
        "Resolves the caller's own candidate Workspace Contexts from their current "
        "active Memberships, keyed to structural anchors only. Read-only discovery — "
        "distinct from governed Workspace entry (ERB-C008-02), excluded from this "
        "Work Package's scope pending a production Access Evaluation resolver "
        "(IRA-009 §4.2)."
    ),
)
async def get_workspace_candidates(
    claims: Annotated[dict, Depends(get_current_claims)],
    resolution_service: Annotated[WorkspaceResolutionService, Depends(get_workspace_resolution_service)],
) -> WorkspaceCandidatesResponse:
    person_id = UUID(claims["person_id"])
    return await resolution_service.resolve_candidates(person_id)
