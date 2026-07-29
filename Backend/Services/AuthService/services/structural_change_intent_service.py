"""
WP-04 BA-03 — Frame Structural Change Intent (ERB-C005-03 / EX-C005-04
per PE-001-C005). Realizes SCI-000001, the Structural Change Intent
Business Object registered by ADR-006 / IRA-004 §21.

Follows IMP-001 §6.3's Business Activity Lifecycle (Request ->
Validation -> Business Rule Execution -> Business Object Update ->
Domain Event Publication -> Audit Recording -> Response), reusing the
same create -> flush -> audit -> event shape every prior Establish-type
Business Activity in this repository has used.

Deliberate difference from OrganizationNodeService.establish() (BA-01):
no pre-flight duplicate check exists here, because EX-C005-04's own
text names no unique business key for a Change Intent Context (every
Frame Structural Change Intent call is a distinct decision record) —
disclosed, not silently omitted.

Deliberately does not implement MODIFIED / SUPERSEDED / ABANDONED /
WITHDRAWN / ARCHIVED lifecycle transitions (IRA-004 §21's own
registered Lifecycle Model) — only CREATED, mirroring BA-01's own
minimal-slice precedent (IRA-004 §5). Those transitions belong to
BA-04 through BA-08's own future gap analyses.
"""

from __future__ import annotations

from models.structural_change_intent import StructuralChangeIntent, StructuralChangeIntentStatus
from repositories.structural_change_intent_repository import StructuralChangeIntentRepository
from schemas.structural_change_intent import FrameStructuralChangeIntentRequest
from observability import record_audit, publish_event, AuditStatus


class StructuralChangeIntentService:
    """Business Activity orchestrator for Frame Structural Change Intent (WP-04 BA-03)."""

    def __init__(self, structural_change_intent_repo: StructuralChangeIntentRepository) -> None:
        self.structural_change_intent_repo = structural_change_intent_repo

    async def frame_change_intent(
        self, request: FrameStructuralChangeIntentRequest, actor_id: str | None = None
    ) -> StructuralChangeIntent:
        """
        Business Activity: Frame Structural Change Intent (BA-03).

        Business Rule (BR-C005-001): a governed structural change SHALL
        have explicit Change Intent Context — satisfied by construction:
        this is the only path that creates a StructuralChangeIntent row,
        and change_rationale/target_outcome are both required (schema
        validation, 422 if missing).

        status is always persisted as CREATED — this Business Activity
        implements no other lifecycle transition (see module docstring).
        """
        structural_change_intent = await self.structural_change_intent_repo.create(
            {
                "change_rationale": request.change_rationale,
                "target_outcome": request.target_outcome,
                "decision_boundary": request.decision_boundary,
                "status": StructuralChangeIntentStatus.CREATED.value,
            }
        )
        await self.structural_change_intent_repo.session.flush()

        record_audit(
            action="FRAME_STRUCTURAL_CHANGE_INTENT",
            resource=f"structural_change_intent:{structural_change_intent.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={"target_outcome": structural_change_intent.target_outcome},
        )
        publish_event(
            "STRUCTURAL_CHANGE_INTENT_FRAMED",
            {
                "structural_change_intent_id": str(structural_change_intent.id),
                "status": structural_change_intent.status,
            },
        )
        return structural_change_intent
