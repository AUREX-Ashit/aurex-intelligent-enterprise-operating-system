"""
WP-07 BA-05 — Resolve Conflicting Person Context (EX-C006-05,
ERB-C006-03, BR-C006-004).

Classification only — routes to EX-C006-04 (ambiguity) or EX-C006-07
(correction need); this Business Activity never itself resolves the
conflict, per PE-001-C006 §5.7 ("AI SHALL NOT resolve the conflict
itself" — extended here to mean this endpoint records and routes an
already-made human classification, it does not compute one).

No new table (IRA-007 §5/§9): the classification decision is recorded
via record_audit only, mirroring every other "detect and classify"
Business Activity's own precedent in this repository (e.g. WP-02 BA-09's
dependency-conflict detection).
"""

from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException, status

from repositories.person_repository import PersonRepository
from schemas.person import PersonConflictClassification, PersonConflictClassificationResponse, ResolvePersonConflictRequest
from observability import record_audit, AuditStatus

_ROUTING = {
    PersonConflictClassification.AMBIGUITY: "EX-C006-04 (Distinguish Candidate Person Matches)",
    PersonConflictClassification.CORRECTION_NEEDED: "EX-C006-07 (Correct Person Context)",
}


class PersonConflictService:
    """Business Activity orchestrator for Resolve Conflicting Person Context (WP-07 BA-05)."""

    def __init__(self, person_repo: PersonRepository) -> None:
        self.person_repo = person_repo

    async def resolve_conflict(
        self, person_id: UUID, request: ResolvePersonConflictRequest, actor_id: str | None = None
    ) -> PersonConflictClassificationResponse:
        person = await self.person_repo.get_by_id(person_id)
        if person is None:
            record_audit(
                action="CLASSIFY_PERSON_CONFLICT",
                resource=f"person:{person_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "person does not exist"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No person found with id '{person_id}'.",
            )

        record_audit(
            action="CLASSIFY_PERSON_CONFLICT",
            resource=f"person:{person_id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={"classification": request.classification.value},
        )

        return PersonConflictClassificationResponse(
            person_id=person_id,
            classification=request.classification,
            routed_to=_ROUTING[request.classification],
        )
