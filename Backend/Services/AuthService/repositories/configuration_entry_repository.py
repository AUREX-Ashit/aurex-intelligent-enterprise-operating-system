import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.configuration_entry import ConfigurationEntry, ConfigurationLifecycleState
from repositories.base_repository import BaseRepository


class ConfigurationEntryRepository(BaseRepository[ConfigurationEntry]):
    """Repository for Configuration Entry records (CFG-000001, WP-10 / C-041)."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(ConfigurationEntry, session)

    async def get_active_tenant_override(
        self, organization_id: uuid.UUID, facet: str, key: str
    ) -> ConfigurationEntry | None:
        """
        BA-01's own Tenant-tier lookup: the currently-ACTIVE TENANT-scope
        override for one Facet + Key within one Organization, if any.
        `order_by` makes selection deterministic if more than one ACTIVE
        row were ever found (should not happen — BA-02 supersedes the
        prior ACTIVE row in the same transaction — but mirrors
        VV-AUDIT-WP-05 F-02's own "never rely on an undefined .first()"
        lesson defensively).
        """
        result = await self.session.execute(
            select(ConfigurationEntry)
            .where(
                ConfigurationEntry.organization_id == organization_id,
                ConfigurationEntry.person_id.is_(None),
                ConfigurationEntry.scope_level == "TENANT",
                ConfigurationEntry.facet == facet,
                ConfigurationEntry.key == key,
                ConfigurationEntry.lifecycle_state == ConfigurationLifecycleState.ACTIVE.value,
            )
            .order_by(ConfigurationEntry.created_at.desc(), ConfigurationEntry.id)
        )
        return result.scalars().first()

    async def get_active_tenant_overrides_for_facet(
        self, organization_id: uuid.UUID, facet: str
    ) -> list[ConfigurationEntry]:
        """BA-01's own bulk resolution path — every currently-ACTIVE TENANT-scope override for one Facet within one Organization, e.g. every Terminology term override at once."""
        result = await self.session.execute(
            select(ConfigurationEntry)
            .where(
                ConfigurationEntry.organization_id == organization_id,
                ConfigurationEntry.person_id.is_(None),
                ConfigurationEntry.scope_level == "TENANT",
                ConfigurationEntry.facet == facet,
                ConfigurationEntry.lifecycle_state == ConfigurationLifecycleState.ACTIVE.value,
            )
            .order_by(ConfigurationEntry.key)
        )
        return list(result.scalars().all())

    async def get_active_user_overrides_for_facet(
        self, organization_id: uuid.UUID, person_id: uuid.UUID, facet: str
    ) -> list[ConfigurationEntry]:
        """
        BA-01's own most-specific tier (CMD-001 §12.6 — User is the final,
        most specific rule in the Scope Hierarchy). Always returns an
        empty list in WP-10's own authorized scope today: BA-02
        (PLATFORM_ADMIN-gated establish/update) never writes a USER-scope
        row (no self-service, non-admin establish flow is chartered by
        IRA-010 §6) — implemented now, ahead of any writer, so a future
        self-service Business Activity only needs to add a write path,
        never a resolve-side change, mirroring RSC-000001's own
        precedent of registering a mechanism's read side ahead of its
        write side being fully authorized.
        """
        result = await self.session.execute(
            select(ConfigurationEntry)
            .where(
                ConfigurationEntry.organization_id == organization_id,
                ConfigurationEntry.person_id == person_id,
                ConfigurationEntry.scope_level == "USER",
                ConfigurationEntry.facet == facet,
                ConfigurationEntry.lifecycle_state == ConfigurationLifecycleState.ACTIVE.value,
            )
            .order_by(ConfigurationEntry.key)
        )
        return list(result.scalars().all())

    async def list_active_for_organization(self, organization_id: uuid.UUID) -> list[ConfigurationEntry]:
        """BA-02's own establish/update admin screen listing — every currently-ACTIVE TENANT-scope override across all facets for one Organization."""
        result = await self.session.execute(
            select(ConfigurationEntry)
            .where(
                ConfigurationEntry.organization_id == organization_id,
                ConfigurationEntry.person_id.is_(None),
                ConfigurationEntry.scope_level == "TENANT",
                ConfigurationEntry.lifecycle_state == ConfigurationLifecycleState.ACTIVE.value,
            )
            .order_by(ConfigurationEntry.facet, ConfigurationEntry.key)
        )
        return list(result.scalars().all())
