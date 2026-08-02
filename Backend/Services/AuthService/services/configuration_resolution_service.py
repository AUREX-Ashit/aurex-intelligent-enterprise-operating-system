"""
WP-10 BA-01 — Resolve Enterprise Configuration (EX-C041-01,
PE-001/CMD-001 §12.6/§12.7).

Read-only resolution, walking the CMD-001 §12.6 Scope Hierarchy tiers
this repository can actually anchor today (IRA-010 §4.8/§6): User ->
Tenant -> Platform Default. Region/Country/Enterprise/Business Domain/
Business Object have no existing entity anywhere in this codebase to
anchor an override to (the same disclosed limitation IRA-009/TD-032
already found for OrganizationNode) and are not resolved here.

Platform Default is never a database row (models/configuration_entry.py's
own class docstring) — PLATFORM_DEFAULTS below is this resolution's own
hardcoded fallback, mirroring the values theme.css / GlobalHeader /
existing UI copy already render today, so introducing Configuration
Management does not change any screen's behaviour until an override is
actually established (BA-02).
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from models.configuration_entry import ConfigurationEntry, ConfigurationFacet
from repositories.configuration_entry_repository import ConfigurationEntryRepository
from schemas.configuration import ConfigurationSource, ResolvedConfigurationBundle, ResolvedConfigurationValue

# Facets with a small, fixed, known key set that always resolves to a
# definite value (a caller never needs to special-case "no override
# exists yet"). Terminology is deliberately absent — its key space is
# open-ended (any term an enterprise chooses to override), so it
# resolves to whatever overrides exist and nothing else; there is no
# single "platform default term" to synthesize per key.
PLATFORM_DEFAULTS: dict[str, dict[str, Any]] = {
    ConfigurationFacet.BRANDING.value: {"logo_url": None},
    ConfigurationFacet.THEME.value: {"theme_class": "LIGHT"},
    ConfigurationFacet.ACCESSIBILITY.value: {
        "high_contrast_enabled": False,
        "reduced_motion_enabled": False,
    },
    ConfigurationFacet.LOCALIZATION.value: {"default_language": "en"},
}

ALL_FACETS: list[str] = [f.value for f in ConfigurationFacet]


class ConfigurationResolutionService:
    """Business Activity orchestrator for Resolve Enterprise Configuration (WP-10 BA-01)."""

    def __init__(self, configuration_repo: ConfigurationEntryRepository) -> None:
        self.configuration_repo = configuration_repo

    async def resolve(
        self, organization_id: UUID, person_id: UUID, facets: list[str] | None
    ) -> ResolvedConfigurationBundle:
        requested_facets = facets or ALL_FACETS

        resolved: dict[str, list[ResolvedConfigurationValue]] = {}
        for facet in requested_facets:
            resolved[facet] = await self._resolve_facet(organization_id, person_id, facet)

        return ResolvedConfigurationBundle(
            organization_id=organization_id,
            facets=resolved,
            resolved_at=datetime.now(timezone.utc),
        )

    async def _resolve_facet(self, organization_id: UUID, person_id: UUID, facet: str) -> list[ResolvedConfigurationValue]:
        tenant_overrides = {
            entry.key: entry
            for entry in await self.configuration_repo.get_active_tenant_overrides_for_facet(organization_id, facet)
        }
        user_overrides = {
            entry.key: entry
            for entry in await self.configuration_repo.get_active_user_overrides_for_facet(organization_id, person_id, facet)
        }
        platform_defaults = PLATFORM_DEFAULTS.get(facet, {})

        known_keys = sorted(set(platform_defaults) | set(tenant_overrides) | set(user_overrides))

        resolved_values: list[ResolvedConfigurationValue] = []
        for key in known_keys:
            resolved_values.append(self._resolve_key(key, tenant_overrides, user_overrides, platform_defaults))
        return resolved_values

    @staticmethod
    def _resolve_key(
        key: str,
        tenant_overrides: dict[str, ConfigurationEntry],
        user_overrides: dict[str, ConfigurationEntry],
        platform_defaults: dict[str, Any],
    ) -> ResolvedConfigurationValue:
        if key in user_overrides:
            entry = user_overrides[key]
            return ResolvedConfigurationValue(
                key=key, value=entry.value, source=ConfigurationSource.USER, version=entry.version
            )
        if key in tenant_overrides:
            entry = tenant_overrides[key]
            return ResolvedConfigurationValue(
                key=key, value=entry.value, source=ConfigurationSource.TENANT, version=entry.version
            )
        return ResolvedConfigurationValue(
            key=key, value=platform_defaults[key], source=ConfigurationSource.PLATFORM_DEFAULT, version=None
        )
