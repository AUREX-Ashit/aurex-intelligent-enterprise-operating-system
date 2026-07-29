"""
WP-04 BA-05 — Assess Structural Consequence (ERB-C005-05 / EX-C005-07
per PE-001-C005). Realizes IMC-000001, the Impact Context Business
Object registered by ADR-009 / IRA-004 §23.

Follows IMP-001 §6.3's Business Activity Lifecycle. Mirrors
StructuralChangeIntentService's own create -> flush -> audit -> event
shape (no duplicate check — Impact Context has no natural business
key), with one existence check first: structural_proposal_id must
reference an existing StructuralProposal revision (reused directly
from BA-04's own StructuralProposalRepository, not a new lookup).

IRA-004 §4 types BA-05 as "Query (computed)" at the Business Activity
level (it reads a proposal and computes an assessment; it does not
mutate any existing structural data) — but the assessment itself is a
registered, persisted Business Object (IMC-000001), so the HTTP verb
this Business Activity's own router uses is POST (create), the same
verb BA-03's own Create-typed Business Activity used, not a
contradiction between "Query" typing and a write-shaped endpoint.

Deliberately does not implement INVALIDATED or ARCHIVED (IRA-004 §23's
own registered Lifecycle Model) — see models/impact_assessment.py's
own docstring and TD-057. Deliberately does not modify
StructuralProposal or trigger invalidation from BA-04's own
refine_proposal() — out of this Business Activity's own scope
("implement only what BA-05 owns").
"""

from __future__ import annotations

from fastapi import HTTPException, status

from models.impact_assessment import ImpactAssessment, ImpactAssessmentStatus
from repositories.impact_assessment_repository import ImpactAssessmentRepository
from repositories.structural_proposal_repository import StructuralProposalRepository
from schemas.impact_assessment import AssessStructuralConsequenceRequest
from observability import record_audit, publish_event, AuditStatus


class ImpactAssessmentService:
    """Business Activity orchestrator for Assess Structural Consequence (WP-04 BA-05)."""

    def __init__(
        self,
        impact_assessment_repo: ImpactAssessmentRepository,
        structural_proposal_repo: StructuralProposalRepository,
    ) -> None:
        self.impact_assessment_repo = impact_assessment_repo
        self.structural_proposal_repo = structural_proposal_repo

    async def assess_structural_consequence(
        self, request: AssessStructuralConsequenceRequest, actor_id: str | None = None
    ) -> ImpactAssessment:
        """
        Business Activity: Assess Structural Consequence (BA-05,
        EX-C005-07).

        Required Context (EX-C005-07, verbatim): "Coherent proposal and
        current authoritative structural context" — the proposal
        revision is existence-checked (404 if it does not exist); the
        current authoritative structural context is reached
        transitively through that revision's own
        target_organization_node_id, not separately validated here (it
        was already validated when the proposal itself was shaped,
        BA-04).

        Business Rule (BR-C005-008): downstream_implications records
        an identification only — no downstream capability action is
        triggered.
        """
        structural_proposal = await self.structural_proposal_repo.get_by_id(
            request.structural_proposal_id
        )
        if structural_proposal is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No structural proposal exists with id '{request.structural_proposal_id}'.",
            )

        impact_assessment = await self.impact_assessment_repo.create(
            {
                "structural_proposal_id": request.structural_proposal_id,
                "impact_description": request.impact_description,
                "uncertainty_notes": request.uncertainty_notes,
                "downstream_implications": request.downstream_implications,
                "status": ImpactAssessmentStatus.CREATED.value,
            }
        )
        await self.impact_assessment_repo.session.flush()

        record_audit(
            action="ASSESS_STRUCTURAL_CONSEQUENCE",
            resource=f"impact_assessment:{impact_assessment.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={"structural_proposal_id": str(impact_assessment.structural_proposal_id)},
        )
        publish_event(
            "STRUCTURAL_CONSEQUENCE_ASSESSED",
            {
                "impact_assessment_id": str(impact_assessment.id),
                "structural_proposal_id": str(impact_assessment.structural_proposal_id),
            },
        )
        return impact_assessment
