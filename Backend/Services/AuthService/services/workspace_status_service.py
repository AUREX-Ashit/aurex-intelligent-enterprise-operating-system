"""
WP-09 BA-02 — Detect and Resolve Disrupted Workspace Context (EX-C008-10,
PE-001-C008 v1.3/ERB-C008-06).

Read-only re-confirmation — no audit record or domain event, mirroring
WP-08's own IdentityStatusService.refresh() shape exactly (IRA-009 §4.6/
§5): a status check, not a governed action. Unlike Identity's own
refresh (which always has an identity_id to resolve against, from the
JWT's own identity_id claim), Workspace has no equivalent persisted
"currently held Workspace Context" today — the caller's own JWT
membership_id/organization_id claims are the closest available signal
for "which Workspace the Person is currently operating under," per
IRA-009 §4.6's own reasoning about the existing route-derived notion of
current Workspace. RTA-001's own runtime Access-Evaluation signal is
named only "where relevant" (conditional) for this EX, not the
unconditional Contract 5.3 requirement ERB-C008-02/04/05 name
(TD-111) — this service re-resolves the two signals that are available
and sufficient: current Membership standing and structural placement.
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from models.membership import Membership
from repositories.membership_repository import MembershipRepository
from repositories.organization_node_repository import OrganizationNodeRepository
from schemas.workspace import WorkspaceContextStatus, WorkspaceStatusResponse


class WorkspaceStatusService:
    """Business Activity orchestrator for Detect and Resolve Disrupted Workspace Context (WP-09 BA-02)."""

    def __init__(
        self, membership_repo: MembershipRepository, organization_node_repo: OrganizationNodeRepository
    ) -> None:
        self.membership_repo = membership_repo
        self.organization_node_repo = organization_node_repo

    async def refresh(self, membership_id: UUID, organization_id: UUID) -> WorkspaceStatusResponse:
        membership = await self.membership_repo.get_by_id(membership_id)

        resolved_status = await self._resolve_status(membership)

        return WorkspaceStatusResponse(
            membership_id=membership_id,
            organization_id=organization_id,
            status=resolved_status,
            checked_at=datetime.now(timezone.utc),
        )

    async def resolve_status(self, membership_id: UUID) -> WorkspaceContextStatus:
        """
        WP-09 BA-03 (Classify Workspace Hand-off Rejection, EX-C008-11)
        reuse entry point — the same status-determination core refresh()
        (BA-02, unmodified above) already uses, without requiring an
        organization_id echo value BA-03's own caller has no canonical
        source for when reporting an arbitrary handed-off membership_id.
        Added per CLAUDE.md §19.5's Reuse-first order, per IRA-009 §5's
        own instruction that BA-03 classify via "BA-02's own refresh()
        logic" — not a duplicate implementation of the classification
        rule itself.
        """
        membership = await self.membership_repo.get_by_id(membership_id)
        return await self._resolve_status(membership)

    async def _resolve_status(self, membership: Membership | None) -> WorkspaceContextStatus:
        if membership is None or membership.membership_status != "ACTIVE":
            return WorkspaceContextStatus.UNRESOLVED

        if membership.home_node_id is None:
            # BR-C007-002/007's own structural-placement anchor is optional
            # (TD-032 — no Business Activity anywhere establishes an
            # OrganizationNode row today). Nothing to re-confirm.
            return WorkspaceContextStatus.CURRENT

        home_node = await self.organization_node_repo.get_by_id(membership.home_node_id)
        if home_node is not None and home_node.active_flag:
            return WorkspaceContextStatus.CURRENT

        return WorkspaceContextStatus.UNRESOLVED
