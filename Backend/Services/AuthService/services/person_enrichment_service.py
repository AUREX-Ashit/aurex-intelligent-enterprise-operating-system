"""
WP-07 BA-08 — Enrich Person Context (EX-C006-08, ERB-C006-06,
BR-C006-007, PE-001-C006 §5.1).

Additive only — never overwrites an existing fact. A candidate
enrichment that contradicts an existing fact belongs to EX-C006-05
(conflict classification), never treated as enrichment here (§3.7).
"""

from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException, status

from repositories.person_enrichment_repository import PersonEnrichmentRepository
from repositories.person_repository import PersonRepository
from schemas.person import EnrichPersonRequest, PersonEnrichmentResponse
from observability import record_audit, publish_event, AuditStatus


class PersonEnrichmentService:
    """Business Activity orchestrator for Enrich Person Context (WP-07 BA-08)."""

    def __init__(
        self,
        enrichment_repo: PersonEnrichmentRepository,
        person_repo: PersonRepository,
    ) -> None:
        self.enrichment_repo = enrichment_repo
        self.person_repo = person_repo

    async def enrich(
        self, person_id: UUID, request: EnrichPersonRequest, actor_id: str | None = None
    ) -> PersonEnrichmentResponse:
        person = await self.person_repo.get_by_id(person_id)
        if person is None:
            record_audit(
                action="ENRICH_PERSON",
                resource=f"person:{person_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "person does not exist"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No person found with id '{person_id}'.",
            )

        enrichment = await self.enrichment_repo.create({
            "person_id": person_id,
            "attribute_name": request.attribute_name,
            "attribute_value": request.attribute_value,
            "source": request.source,
            "sensitivity_classification": request.sensitivity_classification.value,
            "accepted_by": actor_id,
        })
        await self.enrichment_repo.session.flush()

        record_audit(
            action="ENRICH_PERSON",
            resource=f"person:{person_id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={
                "enrichment_id": str(enrichment.id),
                "attribute_name": request.attribute_name,
                "sensitivity_classification": request.sensitivity_classification.value,
            },
        )
        publish_event(
            "PERSON_CONTEXT_ENRICHED",
            {
                "person_id": str(person_id),
                "enrichment_id": str(enrichment.id),
                "attribute_name": request.attribute_name,
            },
        )

        return PersonEnrichmentResponse.model_validate(enrichment)
