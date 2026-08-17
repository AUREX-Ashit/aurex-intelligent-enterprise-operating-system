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

from sqlalchemy import select, update
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

    async def claim_transition(
        self,
        organization_id: uuid.UUID,
        knowledge_asset_id: uuid.UUID,
        *,
        target_status: str,
    ) -> bool:
        """
        WP-14 BA-04 Increment (`TDS-014 §6`, `BA04-INC-DEC-004`). Atomically
        transitions a `PROPOSED` Knowledge Asset to `target_status`, guarded
        by a `WHERE curation_status = 'PROPOSED'` clause the database
        re-evaluates at the moment this `UPDATE` actually executes — never a
        `get_by_id_for_caller()`-then-attribute-assignment sequence, which
        `TDS-014 §6` explicitly rejects (the same unsafe pattern
        `OrganizationService.activate()`/`suspend()` uses, and the same
        pattern class BA-03's own Gate 1 Finding 1 already found unsafe).
        Mirrors `UnclassifiedIntelligenceRegistryRepository.claim_for_
        resolution` exactly: an `UPDATE` statement takes a write lock on the
        row(s) it matches, held until this call's own `commit()` below — a
        second, genuinely concurrent call against the same row blocks on
        that lock, then re-evaluates its own `WHERE` clause against the
        now-committed row and finds zero matches, since `curation_status`
        is no longer `'PROPOSED'`. Returns `True` only to the exactly-one
        caller whose `UPDATE` actually matched a row.

        Commits internally (mirroring `create()`'s own single-step
        transaction shape, not `claim_for_resolution`'s own multi-step
        deferred-commit shape) — this Increment's own transition is a
        single atomic operation with no further write to sequence after
        it, so the same commit-per-call shape `create()` already
        establishes for this repository applies here too. This also
        directly satisfies `TDS-014 §9`'s own `DATABASE COMMIT → DOMAIN
        EVENT PUBLISH ATTEMPT` ordering invariant: by the time this
        coroutine returns, the transition (if any) is already committed,
        so the caller may safely proceed to a publish attempt only after
        awaiting this call.
        """
        result = await self.db.execute(
            update(KnowledgeAssetRegistryModel)
            .where(
                KnowledgeAssetRegistryModel.knowledge_asset_id == knowledge_asset_id,
                KnowledgeAssetRegistryModel.organization_id == organization_id,
                KnowledgeAssetRegistryModel.curation_status == "PROPOSED",
            )
            .values(curation_status=target_status)
        )
        await self.db.commit()
        return result.rowcount == 1
