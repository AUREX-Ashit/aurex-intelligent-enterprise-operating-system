"""
WP-07 BA-07 — Correct Person Context (EX-C006-07, ERB-C006-05,
BR-C006-006, PE-001-C006 §5.1).

Preserves the pre-correction value permanently in traceability — a
correction is never a silent overwrite. Applies the corrected value to
the live Person row (the current authoritative fact) while recording a
PersonCorrection audit-trail row carrying the prior value, reason, and
optional approval_reference.
"""

from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException, status

from repositories.person_correction_repository import PersonCorrectionRepository
from repositories.person_repository import PersonRepository
from schemas.person import AuthoritativePersonContext, CorrectPersonRequest, PersonCorrectionResponse
from observability import record_audit, publish_event, AuditStatus


class PersonCorrectionService:
    """Business Activity orchestrator for Correct Person Context (WP-07 BA-07)."""

    def __init__(
        self,
        correction_repo: PersonCorrectionRepository,
        person_repo: PersonRepository,
    ) -> None:
        self.correction_repo = correction_repo
        self.person_repo = person_repo

    async def correct(
        self, person_id: UUID, request: CorrectPersonRequest, actor_id: str | None = None
    ) -> PersonCorrectionResponse:
        person = await self.person_repo.get_by_id(person_id)
        if person is None:
            record_audit(
                action="CORRECT_PERSON",
                resource=f"person:{person_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "person does not exist"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No person found with id '{person_id}'.",
            )

        prior_value = getattr(person, request.field_name)

        correction = await self.correction_repo.create({
            "person_id": person_id,
            "field_name": request.field_name,
            "prior_value": prior_value,
            "corrected_value": request.corrected_value,
            "reason": request.reason,
            "approval_reference": request.approval_reference,
            "corrected_by": actor_id,
        })

        setattr(person, request.field_name, request.corrected_value)
        await self.correction_repo.session.flush()

        record_audit(
            action="CORRECT_PERSON",
            resource=f"person:{person_id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={
                "correction_id": str(correction.id),
                "field_name": request.field_name,
                "prior_value": prior_value,
                "corrected_value": request.corrected_value,
            },
        )
        publish_event(
            "PERSON_CONTEXT_CORRECTED",
            {
                "person_id": str(person_id),
                "correction_id": str(correction.id),
                "field_name": request.field_name,
            },
        )

        return PersonCorrectionResponse(
            correction_id=correction.id,
            person=AuthoritativePersonContext(
                person_id=person.id,
                first_name=person.first_name,
                last_name=person.last_name,
                display_name=person.display_name,
            ),
            field_name=request.field_name,
            prior_value=prior_value,
            corrected_value=request.corrected_value,
            corrected_at=correction.corrected_at,
        )
