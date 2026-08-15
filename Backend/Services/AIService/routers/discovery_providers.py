# routers/discovery_providers.py
"""WP-14 BA-01 — Establish Discovery Provider Configuration (C-090 Enterprise Discovery)."""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_current_claims, require_platform_admin
from models.database import get_db
from repositories.discovery_provider_repository import DiscoveryProviderRegistryRepository
from schemas.discovery_provider import (
    DiscoveryProviderListResponse,
    DiscoveryProviderResponse,
    EstablishDiscoveryProviderRequest,
)
from services.discovery_provider_service import DiscoveryProviderService

router = APIRouter(prefix="/discovery-providers", tags=["Discovery Providers"])


# ---------------------------------------------------------------------------
# Dependency factories
# ---------------------------------------------------------------------------

async def get_discovery_provider_repo(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> DiscoveryProviderRegistryRepository:
    return DiscoveryProviderRegistryRepository(session)


async def get_discovery_provider_service(
    repo: Annotated[DiscoveryProviderRegistryRepository, Depends(get_discovery_provider_repo)],
) -> DiscoveryProviderService:
    return DiscoveryProviderService(repo)


# ---------------------------------------------------------------------------
# BA-01 — Establish Discovery Provider Configuration
# ---------------------------------------------------------------------------

@router.post(
    "",
    response_model=DiscoveryProviderResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Establish Discovery Provider Configuration (WP-14 BA-01)",
    description=(
        "Writes a real, tenant-scoped discovery_provider_registry row (AMD-013, LOCKED). "
        "Gated by PLATFORM_ADMIN — no dedicated persona exists yet (IRA-014 §10), same "
        "interim measure this repository already uses platform-wide. platform_wide=True "
        "establishes a platform-wide shared provider (organization_id NULL) instead, "
        "mirroring WP-11 BA-01's own identical precedent."
    ),
)
async def establish_discovery_provider(
    request: EstablishDiscoveryProviderRequest,
    claims: Annotated[dict, Depends(require_platform_admin)],
    service: Annotated[DiscoveryProviderService, Depends(get_discovery_provider_service)],
) -> DiscoveryProviderResponse:
    organization_id = UUID(claims["organization_id"])
    actor_id = UUID(claims["person_id"])
    return await service.establish(organization_id, actor_id, request)


@router.get(
    "",
    response_model=DiscoveryProviderListResponse,
    status_code=status.HTTP_200_OK,
    summary="List visible Discovery Provider Configurations (WP-14 BA-01)",
    description=(
        "Lists the caller's own tenant-dedicated Discovery Provider configurations plus "
        "every platform-wide one. Any authenticated caller — genuinely tenant-scoped, not "
        "PLATFORM_ADMIN-only, mirroring WP-11 BA-01's own identical precedent (establish "
        "is gated, list is not)."
    ),
)
async def list_discovery_providers(
    claims: Annotated[dict, Depends(get_current_claims)],
    service: Annotated[DiscoveryProviderService, Depends(get_discovery_provider_service)],
) -> DiscoveryProviderListResponse:
    organization_id = UUID(claims["organization_id"])
    return await service.list_visible(organization_id)
