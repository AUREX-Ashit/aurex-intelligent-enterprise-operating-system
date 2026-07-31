"""
WP-07 BA-04 — Distinguish Candidate Person Matches (EX-C006-04,
ERB-C006-03, PE-001-C006 §1.7).

Governs confirmation only. Per IRA-007 §7.3, candidate-GENERATION
(probabilistic/fuzzy matching) is out of this Work Package's authorized
scope — the same, already-disclosed boundary
PersonRecognitionService.recognize() (WP-07 BA-01) already states.
This service therefore operates on a caller-supplied candidate set
(one or more Person IDs) rather than one fed automatically by BA-01's
own recognition path.

Recognition Authority Rule (PE-001-C006 §1.7): applies identically
whether candidate_person_ids contains one entry or several — no
confidence-based auto-selection exists, and this method never
transitions to a decision without the caller's own explicit
decision_type/rationale.
"""

from __future__ import annotations

from fastapi import HTTPException, status

from repositories.person_distinction_decision_repository import PersonDistinctionDecisionRepository
from repositories.person_repository import PersonRepository
from schemas.person import DistinguishPersonRequest, PersonDistinctionDecisionResponse, PersonDistinctionDecisionType
from observability import record_audit, publish_event, AuditStatus


class PersonDistinctionService:
    """Business Activity orchestrator for Distinguish Candidate Person Matches (WP-07 BA-04)."""

    def __init__(
        self,
        distinction_repo: PersonDistinctionDecisionRepository,
        person_repo: PersonRepository,
    ) -> None:
        self.distinction_repo = distinction_repo
        self.person_repo = person_repo

    async def distinguish(
        self, request: DistinguishPersonRequest, actor_id: str | None = None
    ) -> PersonDistinctionDecisionResponse:
        """
        Structural rules (BR-C006-002/003):
        - Every candidate_person_id must resolve to an existing Person (404 if not).
        - SELECTED_EXISTING requires selected_person_id to be one of candidate_person_ids (422 if not).
        - NEW_PERSON requires selected_person_id to be absent.
        """
        for candidate_id in request.candidate_person_ids:
            candidate = await self.person_repo.get_by_id(candidate_id)
            if candidate is None:
                record_audit(
                    action="DISTINGUISH_PERSON",
                    resource=f"person:{candidate_id}",
                    status=AuditStatus.DENIED,
                    actor_id=actor_id or "SYSTEM",
                    metadata={"reason": "candidate person does not exist"},
                )
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No person found with id '{candidate_id}'.",
                )

        if request.decision_type == PersonDistinctionDecisionType.SELECTED_EXISTING:
            if request.selected_person_id is None or request.selected_person_id not in request.candidate_person_ids:
                record_audit(
                    action="DISTINGUISH_PERSON",
                    resource="person:distinguish",
                    status=AuditStatus.DENIED,
                    actor_id=actor_id or "SYSTEM",
                    metadata={"reason": "selected_person_id must be one of candidate_person_ids for SELECTED_EXISTING"},
                )
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="selected_person_id is required and must be one of candidate_person_ids when decision_type is SELECTED_EXISTING.",
                )
        elif request.selected_person_id is not None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="selected_person_id must be omitted when decision_type is NEW_PERSON.",
            )

        decision = await self.distinction_repo.create({
            "candidate_person_ids": [str(cid) for cid in request.candidate_person_ids],
            "decision_type": request.decision_type.value,
            "selected_person_id": request.selected_person_id,
            "rationale": request.rationale,
            "decided_by": actor_id,
        })
        await self.distinction_repo.session.flush()

        record_audit(
            action="DISTINGUISH_PERSON",
            resource=f"person_distinction_decision:{decision.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={
                "candidate_count": len(request.candidate_person_ids),
                "decision_type": decision.decision_type,
            },
        )
        publish_event(
            "PERSON_DISTINCTION_DECIDED",
            {
                "distinction_decision_id": str(decision.id),
                "decision_type": decision.decision_type,
                "selected_person_id": str(decision.selected_person_id) if decision.selected_person_id else None,
            },
        )

        return PersonDistinctionDecisionResponse.model_validate(decision)
