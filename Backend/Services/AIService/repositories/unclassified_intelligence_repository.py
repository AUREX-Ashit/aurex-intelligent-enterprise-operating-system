# repositories/unclassified_intelligence_repository.py
"""
WP-14 BA-02 — Register Enterprise Intelligence Candidate (C-090). Writes
are strictly tenant-scoped — `organization_id` is always the caller's own
JWT-derived claim, never a caller-supplied identifier, per
`CLAUDE.md §21.4`(c).
"""
from __future__ import annotations

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from models.unclassified_intelligence import UnclassifiedIntelligenceRegistryModel


class UnclassifiedIntelligenceRegistryRepository:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db = db_session

    async def create(
        self,
        *,
        organization_id: uuid.UUID,
        raw_extracted_value: str,
        source_document_reference: str,
        source_page_section: str | None,
        extraction_method: str,
    ) -> UnclassifiedIntelligenceRegistryModel:
        instance = UnclassifiedIntelligenceRegistryModel(
            organization_id=organization_id,
            raw_extracted_value=raw_extracted_value,
            source_document_reference=source_document_reference,
            source_page_section=source_page_section,
            extraction_method=extraction_method,
        )
        self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance
