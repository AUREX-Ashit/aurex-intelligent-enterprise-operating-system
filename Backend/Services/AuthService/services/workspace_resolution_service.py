"""
WP-09 BA-01 — Resolve and Present Available Workspace Candidates
(EX-C008-01/02, PE-001-C008 v1.3/ERB-C008-01).

Read-only candidate discovery, distinct from governed Workspace entry
(ERB-C008-02, excluded from this Work Package's scope per IRA-009 §4.2
— the unconditional Access Evaluation Outcome requirement in Contract
5.3 is scoped to entry/switch/re-entry only, not discovery, per Contract
5.3's own text and BR-C008-02's own confirmation that Membership
Authority Consequence Context is "a required... input to Workspace
availability resolution" but never independently determines it).

Reuses MembershipRepository.get_person_memberships() — the same
repository method MembershipService.present_own_portfolio() (WP-03
BA-08, an analogous cross-organization view) already uses — rather than
duplicating it, per CLAUDE.md §19.5's Reuse-first order (IRA-009 §3/§5).

Per BR-C008-01a, this service does not determine which PE-001 §13.5
Workspace Type(s) a candidate's structural anchor may host (Pending
Canonical Binding, disclosed in the WP-09 charter's own Out of Scope) —
candidates are returned keyed to their structural anchor
(organization_id, home_node_id) only.
"""

from __future__ import annotations

from uuid import UUID

from repositories.membership_repository import MembershipRepository
from schemas.workspace import WorkspaceCandidate, WorkspaceCandidatesResponse


class WorkspaceResolutionService:
    """Business Activity orchestrator for Resolve and Present Available Workspace Candidates (WP-09 BA-01)."""

    def __init__(self, membership_repo: MembershipRepository) -> None:
        self.membership_repo = membership_repo

    async def resolve_candidates(self, person_id: UUID) -> WorkspaceCandidatesResponse:
        memberships = await self.membership_repo.get_person_memberships(person_id)

        candidates = [
            WorkspaceCandidate(
                membership_id=membership.id,
                organization_id=membership.organization_id,
                organization_name=membership.organization.organization_name,
                role_code=membership.role.role_code,
                role_name=membership.role.role_name,
                home_node_id=membership.home_node_id,
                is_primary=membership.is_primary,
            )
            for membership in memberships
        ]

        return WorkspaceCandidatesResponse(candidates=candidates)
