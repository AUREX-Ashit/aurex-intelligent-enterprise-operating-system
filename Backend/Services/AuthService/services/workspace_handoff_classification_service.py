"""
WP-09 BA-03 — Classify Workspace Hand-off Rejection (EX-C008-11,
PE-001-C008 v1.3/ERB-C008-06/BR-C008-06).

Mirrors WP-08 BA-03's own established precedent
(IdentityHandoffClassificationService, itself mirroring WP-02 BA-10's
AuthorizationPolicyConflictService.classify_handoff_rejection()) exactly:
the classification is computed entirely from the Workspace Context's own
independently-verifiable current state — re-resolved via
WorkspaceStatusService.resolve_status() (WP-09 BA-02, unmodified) — never
from the reporting capability's own stated_reason, which is recorded for
audit traceability only, per BR-C008-06's own "a signal, not an
authority" shape.

Closes the gap Backend/Services/AuthService/schemas/membership.py's own
DependentCapability.WORKSPACE_MANAGEMENT enum value has been disclosing
since WP-03 BA-10: a real endpoint now exists for a dependent
capability's own hand-off rejection to be classified against. Wiring a
caller into this endpoint remains that dependent capability's own future
work, not this Work Package's (IRA-009 §5).
"""

from __future__ import annotations

from datetime import datetime, timezone

from observability import record_audit, AuditStatus
from schemas.workspace import (
    ClassifyWorkspaceHandoffRejectionRequest,
    WorkspaceContextStatus,
    WorkspaceHandoffClassification,
    WorkspaceHandoffRejectionOutcome,
)
from services.workspace_status_service import WorkspaceStatusService


class WorkspaceHandoffClassificationService:
    """Business Activity orchestrator for Classify Workspace Hand-off Rejection (WP-09 BA-03)."""

    def __init__(self, status_service: WorkspaceStatusService) -> None:
        self.status_service = status_service

    async def classify(
        self,
        request: ClassifyWorkspaceHandoffRejectionRequest,
        actor_id: str | None = None,
    ) -> WorkspaceHandoffRejectionOutcome:
        resolved_status = await self.status_service.resolve_status(request.membership_id)

        if resolved_status == WorkspaceContextStatus.CURRENT:
            classification = WorkspaceHandoffClassification.CAPABILITY_SCOPED_INSUFFICIENCY
            context_preserved = True
            routed_to = None
            explanation = (
                "The Workspace Context re-resolves CURRENT against the underlying Membership "
                "and structural placement — the underlying association is not in question; "
                "the rejection is scoped to the reporting capability's own attempted use only "
                "(BR-C008-06 — the Workspace Context is preserved unchanged)."
            )
        else:
            classification = WorkspaceHandoffClassification.INTEGRITY_SIGNAL
            context_preserved = False
            routed_to = "EX-C008-10 (POST /workspaces/refresh-status) — re-resolution against source-of-truth facts, never auto-corrected here per BR-C008-06."
            explanation = (
                "The Workspace Context re-resolves UNRESOLVED against the underlying Membership "
                "and structural placement — the underlying association itself is genuinely in "
                "question, independent of the reporting capability's stated reason."
            )

        checked_at = datetime.now(timezone.utc)

        record_audit(
            action="CLASSIFY_WORKSPACE_HANDOFF_REJECTION",
            resource=f"membership:{request.membership_id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={
                "rejecting_capability": request.rejecting_capability,
                "stated_reason": request.stated_reason,
                "classification": classification.value,
            },
        )

        return WorkspaceHandoffRejectionOutcome(
            membership_id=request.membership_id,
            classification=classification,
            context_preserved=context_preserved,
            routed_to=routed_to,
            explanation=explanation,
            checked_at=checked_at,
        )
