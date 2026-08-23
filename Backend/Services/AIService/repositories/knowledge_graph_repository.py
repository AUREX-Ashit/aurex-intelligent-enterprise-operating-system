# repositories/knowledge_graph_repository.py
"""
WP-14 BA-05 — Synchronize Enterprise Knowledge Graph. `EnterpriseKnowledgeGraphRepository`
(`TDS-013 §15`). Thin persistence layer only — no BR-1–BR-4 derivation, no
Entity Resolution, no Ontology Validation (`services/relationship_
resolution_service.py`'s own responsibility). `insert()` adds and flushes
only — it never commits; one relationship-resolution attempt = one
transaction, owned by the caller that opened the session (`TDS-013 §15`),
mirroring `KnowledgeAssetRegistryRepository`'s own read methods (this
repository's own single write path is analogous to that repository's
`create()`, adapted to a non-HTTP, non-`Depends()` call site).
"""
from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.knowledge_graph import EnterpriseKnowledgeGraphRegistryModel


class EnterpriseKnowledgeGraphRepository:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db = db_session

    async def find_by_natural_key(
        self,
        *,
        source_entity_type: str,
        source_entity_id: uuid.UUID,
        relationship_type: str,
        target_entity_type: str,
        target_entity_id: uuid.UUID,
    ) -> EnterpriseKnowledgeGraphRegistryModel | None:
        """
        `TDS-013 §17`'s own natural key —
        `(source_entity_type, source_entity_id, relationship_type,
        target_entity_type, target_entity_id)`. `organization_id` is
        deliberately excluded (`TDS-013 §17`: BR-1–BR-3 are deterministic
        derivations, so two attempts against the same natural key always
        derive the same `organization_id`).
        """
        query = select(EnterpriseKnowledgeGraphRegistryModel).where(
            EnterpriseKnowledgeGraphRegistryModel.source_entity_type == source_entity_type,
            EnterpriseKnowledgeGraphRegistryModel.source_entity_id == source_entity_id,
            EnterpriseKnowledgeGraphRegistryModel.relationship_type == relationship_type,
            EnterpriseKnowledgeGraphRegistryModel.target_entity_type == target_entity_type,
            EnterpriseKnowledgeGraphRegistryModel.target_entity_id == target_entity_id,
        )
        return (await self.db.execute(query)).scalar_one_or_none()

    async def insert(
        self,
        *,
        source_entity_type: str,
        source_entity_id: uuid.UUID,
        relationship_type: str,
        target_entity_type: str,
        target_entity_id: uuid.UUID,
        organization_id: uuid.UUID | None,
    ) -> EnterpriseKnowledgeGraphRegistryModel:
        instance = EnterpriseKnowledgeGraphRegistryModel(
            source_entity_type=source_entity_type,
            source_entity_id=source_entity_id,
            relationship_type=relationship_type,
            target_entity_type=target_entity_type,
            target_entity_id=target_entity_id,
            organization_id=organization_id,
            # graph_engine_reference / relationship_weight / confidence_score /
            # explainability_reference: model-level default (NULL) applies —
            # not overridden here (TDS-013 §1/§8 step 7: no live Neo4j write,
            # no confidence-scoring input, at BA-05's own minimum scope).
            # active_flag: AMD-012's own LOCKED schema states DEFAULT FALSE —
            # not overridden here, mirroring knowledge_asset_registry's own
            # established precedent (models/knowledge_asset.py).
        )
        self.db.add(instance)
        await self.db.flush()
        return instance
