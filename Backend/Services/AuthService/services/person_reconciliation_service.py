"""
WP-07 BA-06 — Review Potential Duplicate Person Indication (EX-C006-06,
ERB-C006-04, BR-C006-005, PE-001-C006 §5.3).

Records a governed Reconciliation Decision. Never a silent merge — any
technical consolidation following a CONFIRMED_DUPLICATE decision is a
downstream data-governance action outside this Enterprise Experience's
own scope (§5.3), and is never performed by this service.
"""

from __future__ import annotations

from fastapi import HTTPException, status

from repositories.person_reconciliation_decision_repository import PersonReconciliationDecisionRepository
from repositories.person_repository import PersonRepository
from schemas.person import ReconcilePersonRequest, PersonReconciliationDecisionResponse
from observability import record_audit, publish_event, AuditStatus


class PersonReconciliationService:
    """Business Activity orchestrator for Review Potential Duplicate Person Indication (WP-07 BA-06)."""

    def __init__(
        self,
        reconciliation_repo: PersonReconciliationDecisionRepository,
        person_repo: PersonRepository,
    ) -> None:
        self.reconciliation_repo = reconciliation_repo
        self.person_repo = person_repo

    async def reconcile(
        self, request: ReconcilePersonRequest, actor_id: str | None = None
    ) -> PersonReconciliationDecisionResponse:
        if request.person_id_a == request.person_id_b:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="person_id_a and person_id_b must be two distinct persons.",
            )

        for candidate_id in (request.person_id_a, request.person_id_b):
            person = await self.person_repo.get_by_id(candidate_id)
            if person is None:
                record_audit(
                    action="RECONCILE_PERSON",
                    resource=f"person:{candidate_id}",
                    status=AuditStatus.DENIED,
                    actor_id=actor_id or "SYSTEM",
                    metadata={"reason": "person does not exist"},
                )
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No person found with id '{candidate_id}'.",
                )

        decision = await self.reconciliation_repo.create({
            "person_id_a": request.person_id_a,
            "person_id_b": request.person_id_b,
            "decision": request.decision.value,
            "rationale": request.rationale,
            "reviewed_by": actor_id,
        })
        await self.reconciliation_repo.session.flush()

        record_audit(
            action="RECONCILE_PERSON",
            resource=f"person_reconciliation_decision:{decision.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={
                "person_id_a": str(request.person_id_a),
                "person_id_b": str(request.person_id_b),
                "decision": decision.decision,
            },
        )
        publish_event(
            "PERSON_RECONCILIATION_DECIDED",
            {
                "reconciliation_decision_id": str(decision.id),
                "person_id_a": str(request.person_id_a),
                "person_id_b": str(request.person_id_b),
                "decision": decision.decision,
            },
        )

        return PersonReconciliationDecisionResponse.model_validate(decision)
