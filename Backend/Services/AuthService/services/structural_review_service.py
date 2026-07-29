"""
WP-04 BA-06 — Review Proposed Structural Outcome / Resolve Structural
Review Concerns (ERB-C005-06 / EX-C005-08, -09 per PE-001-C005).
Realizes RVC-000001, the Review Context Business Object registered by
ADR-011 / IRA-004 §25.

Follows IMP-001 §6.3's Business Activity Lifecycle. create_review()
mirrors StructuralChangeIntentService's own create -> flush -> audit ->
event shape (no duplicate check — Review Context has no natural
business key), with one existence check first: structural_proposal_id
must reference an existing StructuralProposal revision (reused
directly from BA-04's own StructuralProposalRepository).

resolve_concerns() mirrors BA-04's own refine_proposal() shape in one
respect only — it is a status transition on an existing row, not a
new-row-per-revision append — but, unlike refine_proposal(), it never
creates a new StructuralProposal row and never touches
structural_proposals at all. "Resolve concerns" updates this same
Review Context row's own status (CREATED -> CONCERNS_RESOLVED) and,
optionally, appends resolution rationale to its own concerns field —
it never overwrites the original concerns text (SS41.16: "Proposal
revision SHALL not erase the rationale of earlier concerns," applied
here to concerns themselves). Resolving an already-resolved review is
rejected (409), not treated as idempotent — the same guarded-transition
discipline every other state-changing endpoint in this repository
uses (e.g. Establish Organization Node's own duplicate-node_code 409),
documented here as this Business Activity's own explicit choice.

Deliberately does not implement INVALIDATED or ARCHIVED (IRA-004 §25's
own registered Lifecycle Model) — see models/structural_review.py's
own docstring and TD-062. Deliberately does not create or refine any
StructuralProposal row — producing a revised proposal remains
exclusively BA-04's own scope (EX-C005-09's own disclosed "or revised
proposal context" alternative is realized by calling BA-04's existing
Refine endpoint directly, not by this Business Activity).
"""

from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException, status

from models.structural_review import StructuralReview, StructuralReviewStatus
from repositories.structural_review_repository import StructuralReviewRepository
from repositories.structural_proposal_repository import StructuralProposalRepository
from schemas.structural_review import CreateStructuralReviewRequest, ResolveStructuralReviewConcernsRequest
from observability import record_audit, publish_event, AuditStatus


class StructuralReviewService:
    """Business Activity orchestrator for Review / Resolve Structural Review Concerns (WP-04 BA-06)."""

    def __init__(
        self,
        structural_review_repo: StructuralReviewRepository,
        structural_proposal_repo: StructuralProposalRepository,
    ) -> None:
        self.structural_review_repo = structural_review_repo
        self.structural_proposal_repo = structural_proposal_repo

    async def create_review(
        self, request: CreateStructuralReviewRequest, actor_id: str | None = None
    ) -> StructuralReview:
        """
        Business Activity: Review Proposed Structural Outcome (BA-06,
        EX-C005-08).

        Required Context (EX-C005-08, verbatim): "Proposal, Impact
        Context and review purpose" — the proposal revision is
        existence-checked (404 if it does not exist); Impact Context is
        not separately validated as a hard precondition, the same
        disclosed-not-enforced disposition already established for
        PE-001-C005's experience-layer Required Context statements
        since BA-03 (IMP-REPORT-WP-04's own BR-C005-002 disposition).
        """
        structural_proposal = await self.structural_proposal_repo.get_by_id(
            request.structural_proposal_id
        )
        if structural_proposal is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No structural proposal exists with id '{request.structural_proposal_id}'.",
            )

        review = await self.structural_review_repo.create(
            {
                "structural_proposal_id": request.structural_proposal_id,
                "review_position": request.review_position,
                "concerns": request.concerns,
                "status": StructuralReviewStatus.CREATED.value,
            }
        )
        await self.structural_review_repo.session.flush()

        record_audit(
            action="REVIEW_PROPOSED_STRUCTURAL_OUTCOME",
            resource=f"structural_review:{review.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={"structural_proposal_id": str(review.structural_proposal_id)},
        )
        publish_event(
            "STRUCTURAL_REVIEW_CREATED",
            {
                "structural_review_id": str(review.id),
                "structural_proposal_id": str(review.structural_proposal_id),
            },
        )
        return review

    async def resolve_concerns(
        self, review_id: UUID, request: ResolveStructuralReviewConcernsRequest, actor_id: str | None = None
    ) -> StructuralReview:
        """
        Business Activity: Resolve Structural Review Concerns (BA-06,
        EX-C005-09).

        Required Context (EX-C005-09, verbatim): "Review Context with
        unresolved concerns" — 404 if no such review exists; 409 if the
        review is not currently CREATED (already resolved, or in a
        future, not-yet-implemented state) — a deliberate,
        documented guarded-transition choice, not an idempotent no-op.
        """
        review = await self.structural_review_repo.get_by_id(review_id)
        if review is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No structural review exists with id '{review_id}'.",
            )
        if review.status != StructuralReviewStatus.CREATED.value:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Structural review '{review_id}' is not open for concern resolution (status: {review.status}).",
            )

        if request.resolution_notes:
            existing = review.concerns or ""
            separator = "\n\n" if existing else ""
            review.concerns = f"{existing}{separator}Resolution: {request.resolution_notes}"
        review.status = StructuralReviewStatus.CONCERNS_RESOLVED.value
        await self.structural_review_repo.session.flush()

        record_audit(
            action="RESOLVE_STRUCTURAL_REVIEW_CONCERNS",
            resource=f"structural_review:{review.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={"structural_proposal_id": str(review.structural_proposal_id)},
        )
        publish_event(
            "STRUCTURAL_REVIEW_CONCERNS_RESOLVED",
            {
                "structural_review_id": str(review.id),
                "structural_proposal_id": str(review.structural_proposal_id),
            },
        )
        return review
