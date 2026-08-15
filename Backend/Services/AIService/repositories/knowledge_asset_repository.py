# repositories/knowledge_asset_repository.py
"""
WP-14 BA-04 — Establish Knowledge Asset (C-091) repository. Every read is
scoped to `organization_id == caller's own claim` — never an unscoped
lookup by a caller-supplied identifier, per `CLAUDE.md §21.4`(c). No
method here accepts a raw tenant identifier from the request body; the
router passes the caller's own JWT-derived `organization_id`, never a
client-supplied one — mirrors `repositories/search_repository.py`'s own
established convention exactly.
"""
from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.knowledge_asset import KnowledgeAssetRegistryModel


class KnowledgeAssetRegistryRepository:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db = db_session

    async def create(
        self,
        *,
        organization_id: uuid.UUID,
        knowledge_asset_name: str | None,
        knowledge_asset_type: str | None,
        provenance_reference: str,
        source_ingestion_id: uuid.UUID | None,
        confidence_rule_id: uuid.UUID | None,
    ) -> KnowledgeAssetRegistryModel:
        instance = KnowledgeAssetRegistryModel(
            organization_id=organization_id,
            knowledge_asset_name=knowledge_asset_name,
            knowledge_asset_type=knowledge_asset_type,
            provenance_reference=provenance_reference,
            source_ingestion_id=source_ingestion_id,
            confidence_rule_id=confidence_rule_id,
            # curation_status: model-level default("PROPOSED") applies — not
            # overridden here (BA-04 Charter §7: establishment always begins
            # PROPOSED).
            # active_flag: AMD-012's own LOCKED schema states DEFAULT FALSE
            # for this table specifically — not overridden here, per the
            # governing instruction's own "preserve the authorized schema
            # semantics" condition; no business rule anywhere states a newly
            # established Knowledge Asset should be active=True.
        )
        self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance

    async def get_by_id_for_caller(
        self, organization_id: uuid.UUID, knowledge_asset_id: uuid.UUID
    ) -> KnowledgeAssetRegistryModel | None:
        """Scoped by id — the caller's own tenant-owned row only; never another tenant's row (`CLAUDE.md §21.4`(c))."""
        query = select(KnowledgeAssetRegistryModel).where(
            KnowledgeAssetRegistryModel.knowledge_asset_id == knowledge_asset_id,
            KnowledgeAssetRegistryModel.organization_id == organization_id,
        )
        return (await self.db.execute(query)).scalar_one_or_none()
