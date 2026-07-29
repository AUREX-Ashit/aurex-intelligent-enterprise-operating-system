"""
WP-04 BA-07 — Validate Transition Readiness (ERB-C005-07 / EX-C005-10
per PE-001-C005). Realizes VLC-000001, the Validation Context Business
Object registered by ADR-012 / IRA-004 §26.

Follows IMP-001 §6.3's Business Activity Lifecycle. Mirrors
StructuralChangeIntentService's own create -> flush -> audit -> event
shape (no duplicate check — Validation Context has no natural business
key), with three checks first: the referenced proposal must exist, the
referenced review must exist, the review must actually be a review of
that same proposal (BR-C005-006/GS-INV-006's own "exact proposal
revision" discipline), and — the mandatory business rule this Business
Activity hard-enforces — the review must be CONCERNS_RESOLVED
(BR-C005-007: "Unresolved review concerns SHALL prevent completion
unless the governing decision mechanism records an accepted
exception"). No accepted-exception mechanism exists anywhere in this
repository, so this Business Activity enforces the rule
unconditionally — see TD-066.

API response behaviour (documented, per this task's own instruction):
- Unknown structural_proposal_id or structural_review_id -> 404.
- structural_review_id does not belong to structural_proposal_id -> 409.
- structural_review_id exists but is not CONCERNS_RESOLVED -> 409
  (this is EX-C005-10's own "explicit return-to-resolution" outcome,
  realized as a rejection rather than a persisted row — see
  models/structural_validation.py's own docstring). Both 409 paths are
  audited as DENIED, mirroring OrganizationNodeService.establish()'s
  own duplicate-denial audit precedent.
- Otherwise -> 201, a new StructuralValidation row (always CREATED,
  always "ready" by construction).

Deliberately does not implement INVALIDATED or ARCHIVED (IRA-004 §26's
own registered Lifecycle Model) — see TD-065. Deliberately enforces
only BR-C005-007 as a readiness gate — EX-C005-10's own AI Assistance
clause ("AI MAY identify missing context or apparent inconsistencies")
alludes to further readiness criteria this Business Activity does not
implement — see TD-066.
"""

from __future__ import annotations

from fastapi import HTTPException, status

from models.structural_validation import StructuralValidation, StructuralValidationStatus
from models.structural_review import StructuralReviewStatus
from repositories.structural_validation_repository import StructuralValidationRepository
from repositories.structural_proposal_repository import StructuralProposalRepository
from repositories.structural_review_repository import StructuralReviewRepository
from schemas.structural_validation import ValidateTransitionReadinessRequest
from observability import record_audit, publish_event, AuditStatus


class StructuralValidationService:
    """Business Activity orchestrator for Validate Transition Readiness (WP-04 BA-07)."""

    def __init__(
        self,
        structural_validation_repo: StructuralValidationRepository,
        structural_proposal_repo: StructuralProposalRepository,
        structural_review_repo: StructuralReviewRepository,
    ) -> None:
        self.structural_validation_repo = structural_validation_repo
        self.structural_proposal_repo = structural_proposal_repo
        self.structural_review_repo = structural_review_repo

    async def validate_transition_readiness(
        self, request: ValidateTransitionReadinessRequest, actor_id: str | None = None
    ) -> StructuralValidation:
        structural_proposal = await self.structural_proposal_repo.get_by_id(
            request.structural_proposal_id
        )
        if structural_proposal is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No structural proposal exists with id '{request.structural_proposal_id}'.",
            )

        structural_review = await self.structural_review_repo.get_by_id(
            request.structural_review_id
        )
        if structural_review is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No structural review exists with id '{request.structural_review_id}'.",
            )

        if structural_review.structural_proposal_id != request.structural_proposal_id:
            record_audit(
                action="VALIDATE_TRANSITION_READINESS",
                resource=f"structural_proposal:{request.structural_proposal_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={
                    "reason": "structural_review_id does not belong to structural_proposal_id",
                    "structural_review_id": str(request.structural_review_id),
                },
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"Structural review '{request.structural_review_id}' is not a review of "
                    f"proposal '{request.structural_proposal_id}'."
                ),
            )

        if structural_review.status != StructuralReviewStatus.CONCERNS_RESOLVED.value:
            record_audit(
                action="VALIDATE_TRANSITION_READINESS",
                resource=f"structural_proposal:{request.structural_proposal_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={
                    "reason": "review concerns not resolved (BR-C005-007)",
                    "structural_review_id": str(request.structural_review_id),
                    "structural_review_status": structural_review.status,
                },
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"Structural review '{request.structural_review_id}' is not CONCERNS_RESOLVED "
                    f"(current status: {structural_review.status}). Unresolved review concerns "
                    f"SHALL prevent completion (BR-C005-007)."
                ),
            )

        validation = await self.structural_validation_repo.create(
            {
                "structural_proposal_id": request.structural_proposal_id,
                "structural_review_id": request.structural_review_id,
                "readiness_notes": request.readiness_notes,
                "status": StructuralValidationStatus.CREATED.value,
            }
        )
        await self.structural_validation_repo.session.flush()

        record_audit(
            action="VALIDATE_TRANSITION_READINESS",
            resource=f"structural_validation:{validation.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={"structural_proposal_id": str(validation.structural_proposal_id)},
        )
        publish_event(
            "STRUCTURAL_TRANSITION_VALIDATED",
            {
                "structural_validation_id": str(validation.id),
                "structural_proposal_id": str(validation.structural_proposal_id),
                "structural_review_id": str(validation.structural_review_id),
            },
        )
        return validation
