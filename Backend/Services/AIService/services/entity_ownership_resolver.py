# services/entity_ownership_resolver.py
"""
WP-14 BA-05 — Synchronize Enterprise Knowledge Graph. `EntityOwnershipResolver`
(`TDS-013 §9`/§11). Narrowed to BA-05's own currently-authorized minimum
scope (`RO-DEC-WP14-BA05-02`; `TDS-013 §9`'s own reconciliation note): only
the two load-bearing strategies for the one Knowledge Asset → Organization
relationship are implemented here — `KNOWLEDGE_ASSET` (source, queries
`knowledge_asset_registry.organization_id` directly, a fresh read per
resolution, never cached, per `SD-002-108`) and `ORGANIZATION` (target,
resolved trivially — a pure pass-through, no I/O — since `RO-DEC-WP14-
BA05-02` defines the target's own `organization_id` as identical to the
source Knowledge Asset's own persisted `organization_id`, never
independently looked up).

The broader five-strategy `RTA-001 §12.8` scope (`discovery_provider_
registry`, `unclassified_intelligence_registry`, `customer_metric_
registry`/`metric_registry`) is disclosed future scope (`TDS-013 §24`
item 7) — not implemented here. Any entity type outside the two above is
treated as an Entity Resolution failure (`found=False`), never a silent
default.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.knowledge_asset import KnowledgeAssetRegistryModel


@dataclass(frozen=True)
class EntityResolutionResult:
    """
    A resolved entity's own tenant boundary. `organization_id` may
    legitimately be `None` when `found=True` (confirmed-Global, BR-3,
    `TDS-013 §12`) — distinct from `found=False` (unresolved/ambiguous,
    an Entity Resolution failure, never a silent BR-3 default).
    """

    found: bool
    organization_id: uuid.UUID | None = None


class EntityOwnershipResolver:
    """`TDS-013 §9`/§11 — resolves `(entity_type, entity_id)` to its owning Organization boundary."""

    def __init__(self, db_session: AsyncSession) -> None:
        self.db = db_session

    async def resolve(self, entity_type: str, entity_id: uuid.UUID) -> EntityResolutionResult:
        if entity_type == "KNOWLEDGE_ASSET":
            return await self._resolve_knowledge_asset(entity_id)
        if entity_type == "ORGANIZATION":
            return self._resolve_organization(entity_id)
        # Outside this design's own minimum scope (TDS-013 §9's own
        # reconciliation note, §24 item 7) — an Entity Resolution failure,
        # never a silent BR-3 NULL default (TDS-013 §12).
        return EntityResolutionResult(found=False)

    async def _resolve_knowledge_asset(self, knowledge_asset_id: uuid.UUID) -> EntityResolutionResult:
        query = select(KnowledgeAssetRegistryModel.organization_id).where(
            KnowledgeAssetRegistryModel.knowledge_asset_id == knowledge_asset_id
        )
        row = (await self.db.execute(query)).scalar_one_or_none()
        if row is None:
            return EntityResolutionResult(found=False)
        return EntityResolutionResult(found=True, organization_id=row)

    def _resolve_organization(self, organization_id: uuid.UUID | None) -> EntityResolutionResult:
        """
        `RO-DEC-WP14-BA05-02`'s own decided target resolution — trivial by
        design, zero I/O: the target Organization's own boundary IS
        `organization_id` itself, never independently looked up against
        `AuthService`'s own `organization_master` table (a separate
        service database, `CLAUDE.md §8`). This design's only caller of
        this path (`RelationshipResolutionService`) always supplies the
        source Knowledge Asset's own already-resolved `organization_id` as
        this argument — never an event-payload-sourced value.
        """
        return EntityResolutionResult(found=True, organization_id=organization_id)
