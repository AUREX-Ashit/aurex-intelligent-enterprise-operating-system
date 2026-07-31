"""
WP-08 BA-03 — Resolve Dependent Capability Identity Hand-off Rejection
(EX-C001-08, PE-001-C001 v1.1/ERB-C001-04/Contract 5.7).

Mirrors the closer, more authoritative precedent found during IRA
drafting: WP-02 BA-10's AuthorizationPolicyConflictService.classify_
handoff_rejection() (EX-C003-10, Contract 5.7's C-003 analogue,
committed ffaaec6) — not the more generic static-routing-table
pattern IRA-007 BA-05 used. Per that precedent's own governing
principle, the classification is computed entirely from the Identity
Context's own independently-verifiable current state (re-resolved via
IdentityStatusService.refresh(), the same check BA-01 performs) —
never from the reporting capability's own stated_reason, which is
recorded for audit traceability only: Contract 5.7's own text is
explicit that "the dependent capability's stated rejection reason is a
signal, not an authority."
"""

from __future__ import annotations

from uuid import UUID

from observability import record_audit, AuditStatus
from schemas.identity import (
    ClassifyHandoffRejectionRequest,
    HandoffRejectionOutcome,
    IdentityContextStatus,
    IdentityHandoffClassification,
)
from services.identity_status_service import IdentityStatusService


class IdentityHandoffClassificationService:
    """Business Activity orchestrator for Resolve Dependent Capability Identity Hand-off Rejection (WP-08 BA-03)."""

    def __init__(self, status_service: IdentityStatusService) -> None:
        self.status_service = status_service

    async def classify(
        self,
        request: ClassifyHandoffRejectionRequest,
        actor_id: str | None = None,
    ) -> HandoffRejectionOutcome:
        refreshed = await self.status_service.refresh(request.identity_id)

        if refreshed.status == IdentityContextStatus.CURRENT:
            classification = IdentityHandoffClassification.CAPABILITY_SCOPED_INSUFFICIENCY
            identity_context_preserved = True
            routed_to = None
            explanation = (
                "The Identity Context re-resolves CURRENT against C-006 — the underlying "
                "association is not in question; the rejection is scoped to the reporting "
                "capability's own attempted use only (Contract 5.7 — the Identity Context "
                "is preserved unchanged)."
            )
        else:
            classification = IdentityHandoffClassification.INTEGRITY_SIGNAL
            identity_context_preserved = False
            routed_to = "EX-C001-06 (POST /identity/refresh-status) — re-resolution against source-of-truth facts, never auto-corrected here per Contract 5.7."
            explanation = (
                "The Identity Context re-resolves UNRESOLVED against C-006 — the underlying "
                "association itself is genuinely in question, independent of the reporting "
                "capability's stated reason."
            )

        record_audit(
            action="CLASSIFY_IDENTITY_HANDOFF_REJECTION",
            resource=f"identity:{request.identity_id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={
                "rejecting_capability": request.rejecting_capability,
                "stated_reason": request.stated_reason,
                "classification": classification.value,
            },
        )

        return HandoffRejectionOutcome(
            identity_id=request.identity_id,
            classification=classification,
            identity_context_preserved=identity_context_preserved,
            routed_to=routed_to,
            explanation=explanation,
            checked_at=refreshed.checked_at,
        )
