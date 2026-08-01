from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_current_claims, require_platform_admin
from models.database import db_manager
from repositories.membership_repository import MembershipRepository
from repositories.organization_node_repository import OrganizationNodeRepository
from schemas.workspace import (
    ClassifyWorkspaceHandoffRejectionRequest,
    WorkspaceCandidatesResponse,
    WorkspaceHandoffRejectionOutcome,
    WorkspaceStatusResponse,
)
from services.workspace_handoff_classification_service import WorkspaceHandoffClassificationService
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


async def get_workspace_handoff_classification_service(
    status_service: Annotated[WorkspaceStatusService, Depends(get_workspace_status_service)],
) -> WorkspaceHandoffClassificationService:
    return WorkspaceHandoffClassificationService(status_service)


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


@router.post(
    "/classify-handoff-rejection",
    response_model=WorkspaceHandoffRejectionOutcome,
    status_code=status.HTTP_200_OK,
    summary="Resolve dependent capability Workspace hand-off rejection (WP-09 BA-03, EX-C008-11)",
    description=(
        "Classifies a dependent capability's Workspace Context hand-off rejection as "
        "either capability-scoped insufficiency (Workspace Context preserved) or a "
        "Workspace Context integrity signal (routed to BA-02 for re-resolution). "
        "Computed entirely from the Workspace Context's own independently-verifiable "
        "current state, never from the reporting capability's stated reason. Gated by "
        "PLATFORM_ADMIN — the caller-supplied membership_id is not verified against the "
        "caller's own claims (the endpoint's own purpose is to classify a hand-off "
        "reported by a dependent capability, not necessarily the caller's own "
        "Membership), so an unrestricted caller could otherwise learn another tenant's "
        "own Membership status. Same interim gate as /access-evaluations/"
        "/domain-permissions pending a real dependent-capability trust mechanism (TD-113)."
    ),
)
async def classify_handoff_rejection(
    request: ClassifyWorkspaceHandoffRejectionRequest,
    claims: Annotated[dict, Depends(require_platform_admin)],
    classification_service: Annotated[
        WorkspaceHandoffClassificationService, Depends(get_workspace_handoff_classification_service)
    ],
) -> WorkspaceHandoffRejectionOutcome:
    return await classification_service.classify(request, actor_id=claims.get("person_id"))
