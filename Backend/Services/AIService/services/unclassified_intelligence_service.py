# services/unclassified_intelligence_service.py
"""
WP-14 BA-02 — Register Enterprise Intelligence Candidate (C-090). Writes
`unclassified_intelligence_registry` (AMD-005, LOCKED). Gated by
`PLATFORM_ADMIN` at the router — no dedicated persona exists yet
(`PE-001-C090` names none), same interim measure this repository already
uses platform-wide (`IRA-014 §10`, `TD-021`-class).
"""
from __future__ import annotations

import uuid

from observability import AuditStatus, record_audit
from repositories.unclassified_intelligence_repository import UnclassifiedIntelligenceRegistryRepository
from schemas.unclassified_intelligence import IntelligenceCandidateResponse, RegisterIntelligenceCandidateRequest


class IntelligenceCandidateService:
    """Business Activity orchestrator for BA-02."""

    def __init__(self, repo: UnclassifiedIntelligenceRegistryRepository) -> None:
        self.repo = repo

    async def register(
        self, organization_id: uuid.UUID, actor_id: uuid.UUID, request: RegisterIntelligenceCandidateRequest
    ) -> IntelligenceCandidateResponse:
        instance = await self.repo.create(
            organization_id=organization_id,
            raw_extracted_value=request.raw_extracted_value,
            source_document_reference=request.source_document_reference,
            source_page_section=request.source_page_section,
            extraction_method=request.extraction_method,
        )

        record_audit(
            action="REGISTER_INTELLIGENCE_CANDIDATE",
            resource=f"unclassified_intelligence:{instance.unclassified_id}",
            status=AuditStatus.SUCCESS,
            actor_id=str(actor_id),
            tenant_id=str(organization_id),
        )
        return IntelligenceCandidateResponse.model_validate(instance)
