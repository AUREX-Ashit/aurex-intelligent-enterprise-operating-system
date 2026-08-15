# repositories/discovery_provider_repository.py
"""
WP-14 BA-01 — Establish Discovery Provider Configuration (C-090). Every
read is scoped to `organization_id == caller's own claim OR organization_id
IS NULL` (platform-wide) — never an unscoped lookup by a caller-supplied
identifier, per `CLAUDE.md §21.4`(c). Mirrors
`repositories/search_repository.py::VectorIndexRegistryRepository`'s own
established shape exactly (WP-11 BA-01, IRA-014's own named structural
twin for this Business Activity).
"""
from __future__ import annotations

import uuid

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.discovery_provider import DiscoveryProviderRegistryModel


class DiscoveryProviderRegistryRepository:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db = db_session

    async def create(
        self,
        *,
        organization_id: uuid.UUID | None,
        provider_name: str | None,
        provider_category: str,
        provider_type: str,
        connection_config_json: dict | None,
        credential_id: uuid.UUID | None,
        discovery_cadence: str,
        governing_policy_id: uuid.UUID | None,
    ) -> DiscoveryProviderRegistryModel:
        instance = DiscoveryProviderRegistryModel(
            organization_id=organization_id,
            provider_name=provider_name,
            provider_category=provider_category,
            provider_type=provider_type,
            connection_config_json=connection_config_json,
            credential_id=credential_id,
            discovery_cadence=discovery_cadence,
            governing_policy_id=governing_policy_id,
        )
        self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance

    async def list_visible(self, organization_id: uuid.UUID) -> list[DiscoveryProviderRegistryModel]:
        """The caller's own tenant-dedicated rows plus every platform-wide row — not filtered by `active_flag` (module docstring: no activation step exists for this Business Activity)."""
        query = select(DiscoveryProviderRegistryModel).where(
            or_(
                DiscoveryProviderRegistryModel.organization_id == organization_id,
                DiscoveryProviderRegistryModel.organization_id.is_(None),
            )
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())
