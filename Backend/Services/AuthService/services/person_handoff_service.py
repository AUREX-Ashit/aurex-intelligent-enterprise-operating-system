"""
WP-07 BA-09/BA-10 — Hand Off Person Context to Identity Establishment
(EX-C006-10) / Membership Establishment (EX-C006-11), both ERB-C006-07,
BR-C006-009/010, PE-001-C006 §5.8 (Cross-Capability Hand-off Contract).

C-006 never calls into Identity Management's (C-001) or Membership
Management's (C-007) own API — neither is chartered as a real Work
Package with a real API to call, and PE-001-C006's own Out-of-Scope
(§1.4) excludes any cross-service coupling. The caller (acting on
behalf of the dependent capability) reports the outcome; this mirrors
WP-02 BA-10's own already-accepted "the caller reports the outcome"
hand-off precedent exactly.

No persistence (IRA-007 §5): BR-C006-009's "record an explicit accepted
or returned outcome" is satisfied by record_audit(), the same basis
every prior hand-off Business Activity in this repository already uses.
A downstream rejection never alters the underlying Authoritative Person
Context (BR-C006-010) — this service performs no write to the Person
row in either branch.
"""

from __future__ import annotations

from typing import Literal
from uuid import UUID

from fastapi import HTTPException, status

from repositories.person_repository import PersonRepository
from schemas.person import PersonHandoffOutcome, PersonHandoffRequest, PersonHandoffOutcomeType
from observability import record_audit, publish_event, AuditStatus

_EVENT_TYPE = {
    "C-001": "PERSON_HANDOFF_TO_IDENTITY_RECORDED",
    "C-007": "PERSON_HANDOFF_TO_MEMBERSHIP_RECORDED",
}


class PersonHandoffService:
    """Business Activity orchestrator for Hand Off Person Context to a dependent capability (WP-07 BA-09/BA-10)."""

    def __init__(self, person_repo: PersonRepository) -> None:
        self.person_repo = person_repo

    async def handoff(
        self,
        person_id: UUID,
        target_capability: Literal["C-001", "C-007"],
        request: PersonHandoffRequest,
        actor_id: str | None = None,
    ) -> PersonHandoffOutcome:
        person = await self.person_repo.get_by_id(person_id)
        if person is None:
            record_audit(
                action="HANDOFF_PERSON_CONTEXT",
                resource=f"person:{person_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "person does not exist", "target_capability": target_capability},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No person found with id '{person_id}'.",
            )

        if request.outcome == PersonHandoffOutcomeType.RETURNED and not request.reason:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="reason is required when outcome is RETURNED.",
            )

        record_audit(
            action="HANDOFF_PERSON_CONTEXT",
            resource=f"person:{person_id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={
                "target_capability": target_capability,
                "outcome": request.outcome.value,
                "reason": request.reason,
            },
        )
        publish_event(
            _EVENT_TYPE[target_capability],
            {
                "person_id": str(person_id),
                "outcome": request.outcome.value,
                "reason": request.reason,
            },
        )

        return PersonHandoffOutcome(
            person_id=person_id,
            target_capability=target_capability,
            outcome=request.outcome,
            reason=request.reason,
        )
