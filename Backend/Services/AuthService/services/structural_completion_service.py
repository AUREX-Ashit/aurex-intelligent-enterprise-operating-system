"""
WP-04 BA-08 — Complete Structural Transition (ERB-C005-08 / EX-C005-11
per PE-001-C005). Realizes RSC-000001, the Resulting Structural
Context Business Object registered by ADR-013 / IRA-004 §27.

Follows IMP-001 §6.3's Business Activity Lifecycle. Mirrors
ImpactAssessmentService/StructuralValidationService's own single-check
create -> flush -> audit -> event shape.

**Option A scope (mandatory, per BA-08's own readiness assessment and
this task's own explicit instruction):** this service creates the
C-005 experience-layer completion record only. It never writes to
`organization_nodes`, never creates `organization_hierarchy` or
`consolidation_determination`, and never attempts to infer a
structural change from a proposal's own free-text
`proposed_outcome_description`. No canonical document in this
repository specifies a structured representation from which such a
mutation could be deterministically derived (PE-001-C005 §38.4 places
database/mutation mechanics outside C-005's own scope) — building one
here would be an unauthorized architectural addition, not an
implementation detail. The deferred mutation mechanism is recorded as
TD-070, not silently omitted.

**Completion idempotency (this Business Activity's own first disclosed
decision, documented per this task's own instruction):** completion is
a guarded transition, not idempotent. A second completion attempt
against the same structural_validation_id is rejected with 409 —
mirroring BA-06's own already-resolved-review guard
(StructuralReviewService.resolve_concerns()) and BA-07's own
unresolved-concerns guard (StructuralValidationService). Completion is
a one-time terminal event closing a governed decision (BR-C005-009/
BR-C005-010), not a revision chain like BA-04's own deliberately
append-only StructuralProposal — allowing multiple completions per
validation would let the same governed decision be "completed" more
than once, which BR-C005-010 ("Exiting without completion SHALL not
represent a proposal as resulting enterprise structure") argues
against by implication: completion is meant to be a single, decisive
closure, not a repeatable action. Enforced both in the service layer
(pre-check, clean 409) and via the model's own
`structural_validation_id` unique constraint (a second line of defense
against the concurrent-completion race, the same pattern
OrganizationService.establish() already documents for
`organization_code`).

Deliberately does not implement ARCHIVED (IRA-004 §27's own registered
Lifecycle Model) — see TD-069.

WP-04 BA-09 ("Continue from Resulting Structure", EX-C005-12) adds
get_details() — a pure read, mirroring
OrganizationNodeService.get_details()'s (WP-04 BA-01/BA-02) own
identical shape: get_by_id() -> 404-if-None -> return, no audit, no
domain event (read-only Business Activities do not audit or emit
events in this repository's established pattern). Reuses the existing
StructuralCompletionResponse verbatim — no payload enrichment, no
embedded upstream chain, no new "downstream continuation" object
(BA-09's own readiness assessment: "Downstream continuation context"
does not qualify as a canonical Business Object — EX-C005-12's own
Invalidated Context explicitly describes it as "C-005-only transient
context not required downstream").
"""

from __future__ import annotations

from uuid import UUID

from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from models.structural_completion import StructuralCompletion, StructuralCompletionStatus
from repositories.structural_completion_repository import StructuralCompletionRepository
from repositories.structural_validation_repository import StructuralValidationRepository
from schemas.structural_completion import CompleteStructuralTransitionRequest
from observability import record_audit, publish_event, AuditStatus


class StructuralCompletionService:
    """Business Activity orchestrator for Complete Structural Transition (WP-04 BA-08)."""

    def __init__(
        self,
        structural_completion_repo: StructuralCompletionRepository,
        structural_validation_repo: StructuralValidationRepository,
    ) -> None:
        self.structural_completion_repo = structural_completion_repo
        self.structural_validation_repo = structural_validation_repo

    async def complete_structural_transition(
        self, request: CompleteStructuralTransitionRequest, actor_id: str | None = None
    ) -> StructuralCompletion:
        structural_validation = await self.structural_validation_repo.get_by_id(
            request.structural_validation_id
        )
        if structural_validation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No structural validation exists with id '{request.structural_validation_id}'.",
            )

        existing_completion = await self.structural_completion_repo.get_by_structural_validation_id(
            request.structural_validation_id
        )
        if existing_completion is not None:
            record_audit(
                action="COMPLETE_STRUCTURAL_TRANSITION",
                resource=f"structural_validation:{request.structural_validation_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "structural transition already completed"},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"Structural validation '{request.structural_validation_id}' has already "
                    f"been completed."
                ),
            )

        try:
            completion = await self.structural_completion_repo.create(
                {
                    "structural_validation_id": request.structural_validation_id,
                    "completion_notes": request.completion_notes,
                    "status": StructuralCompletionStatus.CREATED.value,
                }
            )
            await self.structural_completion_repo.session.flush()
        except IntegrityError:
            # Closes the race window between the pre-check above and this
            # insert, the identical concurrent-duplicate defense
            # OrganizationService.establish() (WP-01) already documents.
            await self.structural_completion_repo.session.rollback()
            record_audit(
                action="COMPLETE_STRUCTURAL_TRANSITION",
                resource=f"structural_validation:{request.structural_validation_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "structural transition already completed (concurrent completion)"},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"Structural validation '{request.structural_validation_id}' has already "
                    f"been completed."
                ),
            )

        record_audit(
            action="COMPLETE_STRUCTURAL_TRANSITION",
            resource=f"structural_completion:{completion.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={"structural_validation_id": str(completion.structural_validation_id)},
        )
        publish_event(
            "STRUCTURAL_TRANSITION_COMPLETED",
            {
                "structural_completion_id": str(completion.id),
                "structural_validation_id": str(completion.structural_validation_id),
            },
        )
        return completion

    async def get_details(self, structural_completion_id: UUID) -> StructuralCompletion:
        """
        Business Activity: Continue from Resulting Structure (BA-09,
        EX-C005-12).

        Realizes EX-C005-12's own Required Context ("Resulting
        Structural Context") as a direct read of the completion record
        already produced by BA-08 — no new object, no embellishment.
        """
        completion = await self.structural_completion_repo.get_by_id(structural_completion_id)
        if completion is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No structural completion exists with id '{structural_completion_id}'.",
            )
        return completion
