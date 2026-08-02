"""
WP-10 BA-02 — Establish/Update Enterprise Configuration (EX-C041-02,
CMD-001 §12.5).

Writes a TENANT-scope override only — USER-scope establishment is not
chartered (models/configuration_entry.py's own ConfigurationScopeLevel
docstring). PLATFORM_ADMIN-gated at the router (dependencies.
require_platform_admin), the same interim gate TD-021 through TD-025 and
TD-113 already established: no Tenant Admin/Corporate Admin authority
model exists yet to scope this more tightly than "any PLATFORM_ADMIN may
establish any tenant's Configuration."

Versioned per CMD-001 §12.5's mandatory Versioning/Effective Dating: the
prior ACTIVE row (if any) is superseded, never overwritten in place, in
the same transaction as the new row's own insert.
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from models.configuration_entry import ConfigurationEntry, ConfigurationLifecycleState
from repositories.configuration_entry_repository import ConfigurationEntryRepository
from schemas.configuration import ConfigurationEntryResponse, EstablishConfigurationEntryRequest


class ConfigurationManagementService:
    """Business Activity orchestrator for Establish/Update Enterprise Configuration (WP-10 BA-02)."""

    def __init__(self, configuration_repo: ConfigurationEntryRepository) -> None:
        self.configuration_repo = configuration_repo

    async def establish(
        self, organization_id: UUID, request: EstablishConfigurationEntryRequest, established_by_person_id: UUID | None
    ) -> ConfigurationEntryResponse:
        now = datetime.now(timezone.utc)

        existing = await self.configuration_repo.get_active_tenant_override(
            organization_id, request.facet.value, request.key
        )

        next_version = 1
        if existing is not None:
            existing.lifecycle_state = ConfigurationLifecycleState.SUPERSEDED.value
            existing.effective_to = now
            next_version = existing.version + 1

        new_entry = ConfigurationEntry(
            organization_id=organization_id,
            person_id=None,
            scope_level="TENANT",
            facet=request.facet.value,
            key=request.key,
            value=request.value,
            version=next_version,
            lifecycle_state=ConfigurationLifecycleState.ACTIVE.value,
            effective_from=now,
            established_by_person_id=established_by_person_id,
        )
        self.configuration_repo.session.add(new_entry)
        await self.configuration_repo.session.flush()

        return ConfigurationEntryResponse.model_validate(new_entry)

    async def list_established(self, organization_id: UUID) -> list[ConfigurationEntryResponse]:
        entries = await self.configuration_repo.list_active_for_organization(organization_id)
        return [ConfigurationEntryResponse.model_validate(entry) for entry in entries]
