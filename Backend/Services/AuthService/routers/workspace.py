from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_current_claims
from models.database import db_manager
from repositories.membership_repository import MembershipRepository
from repositories.organization_node_repository import OrganizationNodeRepository
from schemas.workspace import WorkspaceCandidatesResponse, WorkspaceStatusResponse
from services.workspace_resolution_service import WorkspaceResolutionService
from services.workspace_status_service import WorkspaceStatusService

router = APIRouter()


# ---------------------------------------------------------------------------
# Dependency factories
# ---------------------------------------------------------------------------

async def get_membership_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> MembershipRepository:
    return MembershipRepository(session)


async def get_organization_node_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> OrganizationNodeRepository:
    return OrganizationNodeRepository(session)


async def get_workspace_resolution_service(
    membership_repo: Annotated[MembershipRepository, Depends(get_membership_repository)],
) -> WorkspaceResolutionService:
    return WorkspaceResolutionService(membership_repo)


async def get_workspace_status_service(
    membership_repo: Annotated[MembershipRepository, Depends(get_membership_repository)],
    organization_node_repo: Annotated[OrganizationNodeRepository, Depends(get_organization_node_repository)],
) -> WorkspaceStatusService:
    return WorkspaceStatusService(membership_repo, organization_node_repo)


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


@router.post(
    "/refresh-status",
    response_model=WorkspaceStatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Detect and resolve disrupted Workspace Context (WP-09 BA-02, EX-C008-10)",
    description=(
        "Re-confirms the caller's own current Workspace Context (the Membership "
        "and structural placement named by the session's own membership_id/"
        "organization_id claims) rather than trusting the last-known JWT claim "
        "state. Read-only — no audit record or domain event. Never a silent 200 "
        "with stale data: even a deactivated or removed Membership resolves to "
        "UNRESOLVED, not a 404."
    ),
)
async def refresh_workspace_status(
    claims: Annotated[dict, Depends(get_current_claims)],
    status_service: Annotated[WorkspaceStatusService, Depends(get_workspace_status_service)],
) -> WorkspaceStatusResponse:
    membership_id = UUID(claims["membership_id"])
    organization_id = UUID(claims["organization_id"])
    return await status_service.refresh(membership_id, organization_id)
