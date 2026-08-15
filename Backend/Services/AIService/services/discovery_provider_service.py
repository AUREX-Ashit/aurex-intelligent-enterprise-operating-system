# services/discovery_provider_service.py
"""
WP-14 BA-01 — Establish Discovery Provider Configuration (C-090). Writes/
lists `discovery_provider_registry` (AMD-013, LOCKED). Gated by
`PLATFORM_ADMIN` at the router (establish) — no dedicated persona exists
yet (`PE-001-C090` names none), same interim measure this repository
already uses platform-wide (`IRA-014 §10`, `TD-021`-class).
"""
from __future__ import annotations

import uuid

from observability import AuditStatus, record_audit
from repositories.discovery_provider_repository import DiscoveryProviderRegistryRepository
from schemas.discovery_provider import (
    DiscoveryProviderListResponse,
    DiscoveryProviderResponse,
    EstablishDiscoveryProviderRequest,
)


class DiscoveryProviderService:
    """Business Activity orchestrator for BA-01."""

    def __init__(self, repo: DiscoveryProviderRegistryRepository) -> None:
        self.repo = repo

    async def establish(
        self, organization_id: uuid.UUID, actor_id: uuid.UUID, request: EstablishDiscoveryProviderRequest
    ) -> DiscoveryProviderResponse:
        target_organization_id = None if request.platform_wide else organization_id

        instance = await self.repo.create(
            organization_id=target_organization_id,
            provider_name=request.provider_name,
            provider_category=request.provider_category,
            provider_type=request.provider_type,
            connection_config_json=request.connection_config_json,
            credential_id=request.credential_id,
            discovery_cadence=request.discovery_cadence,
            governing_policy_id=request.governing_policy_id,
        )

        record_audit(
            action="ESTABLISH_DISCOVERY_PROVIDER",
            resource=f"discovery_provider:{instance.discovery_provider_id}",
            status=AuditStatus.SUCCESS,
            actor_id=str(actor_id),
            tenant_id=str(organization_id),
        )
        return DiscoveryProviderResponse.model_validate(instance)

    async def list_visible(self, organization_id: uuid.UUID) -> DiscoveryProviderListResponse:
        rows = await self.repo.list_visible(organization_id)
        return DiscoveryProviderListResponse(
            discovery_providers=[DiscoveryProviderResponse.model_validate(row) for row in rows]
        )
