from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import require_matching_tenant_or_platform_admin, require_platform_admin
from middleware.tenant import get_current_tenant
from models.configuration_entry import ConfigurationFacet
from models.database import db_manager
from repositories.configuration_entry_repository import ConfigurationEntryRepository
from schemas.configuration import (
    ConfigurationEntryListResponse,
    ConfigurationEntryResponse,
    EstablishConfigurationEntryRequest,
    ResolvedConfigurationBundle,
)
from services.configuration_management_service import ConfigurationManagementService
from services.configuration_resolution_service import ConfigurationResolutionService

router = APIRouter()


# ---------------------------------------------------------------------------
# Dependency factories
# ---------------------------------------------------------------------------

async def get_configuration_repository(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> ConfigurationEntryRepository:
    return ConfigurationEntryRepository(session)


async def get_configuration_resolution_service(
    configuration_repo: Annotated[ConfigurationEntryRepository, Depends(get_configuration_repository)],
) -> ConfigurationResolutionService:
    return ConfigurationResolutionService(configuration_repo)


async def get_configuration_management_service(
    configuration_repo: Annotated[ConfigurationEntryRepository, Depends(get_configuration_repository)],
) -> ConfigurationManagementService:
    return ConfigurationManagementService(configuration_repo)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get(
    "",
    response_model=ResolvedConfigurationBundle,
    status_code=status.HTTP_200_OK,
    summary="Resolve Enterprise Configuration (WP-10 BA-01, EX-C041-01)",
    description=(
        "Resolves the caller's own tenant Configuration, walking the CMD-001 "
        "§12.6 Scope Hierarchy tiers this repository can anchor today "
        "(User -> Tenant -> Platform Default). Genuinely tenant-scoped, not "
        "PLATFORM_ADMIN-only — but the caller's own X-Tenant-ID must match "
        "their own JWT organization_id claim unless they hold PLATFORM_ADMIN "
        "(require_matching_tenant_or_platform_admin) — never an arbitrary "
        "tenant named only by an unverified header (CERT-WP-10 Finding B-1). "
        "Never a silent gap: a key with no override still resolves, naming "
        "source=PLATFORM_DEFAULT explicitly."
    ),
)
async def resolve_configuration(
    claims: Annotated[dict, Depends(require_matching_tenant_or_platform_admin)],
    organization_id: Annotated[UUID, Depends(get_current_tenant)],
    resolution_service: Annotated[ConfigurationResolutionService, Depends(get_configuration_resolution_service)],
    facet: Annotated[list[ConfigurationFacet] | None, Query(description="Restrict resolution to specific facets; omit to resolve all.")] = None,
) -> ResolvedConfigurationBundle:
    person_id = UUID(claims["person_id"])
    facets = [f.value for f in facet] if facet else None
    return await resolution_service.resolve(organization_id, person_id, facets)


@router.post(
    "",
    response_model=ConfigurationEntryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Establish/Update Enterprise Configuration (WP-10 BA-02, EX-C041-02)",
    description=(
        "Establishes a new TENANT-scope Configuration override for the "
        "caller's own X-Tenant-ID, versioned per CMD-001 §12.5 — a prior "
        "ACTIVE row for the same facet+key is superseded, never overwritten "
        "in place. Gated by PLATFORM_ADMIN — no Tenant Admin authority model "
        "exists yet (same interim gate as /workspaces/classify-handoff-"
        "rejection, TD-113)."
    ),
)
async def establish_configuration(
    request: EstablishConfigurationEntryRequest,
    claims: Annotated[dict, Depends(require_platform_admin)],
    organization_id: Annotated[UUID, Depends(get_current_tenant)],
    management_service: Annotated[ConfigurationManagementService, Depends(get_configuration_management_service)],
) -> ConfigurationEntryResponse:
    established_by = UUID(claims["person_id"]) if claims.get("person_id") else None
    return await management_service.establish(organization_id, request, established_by)


@router.get(
    "/entries",
    response_model=ConfigurationEntryListResponse,
    status_code=status.HTTP_200_OK,
    summary="List established Enterprise Configuration overrides (WP-10 BA-02, EX-C041-02)",
    description=(
        "Lists every currently-ACTIVE TENANT-scope override for the caller's "
        "own X-Tenant-ID, across all facets — the establish/update admin "
        "screen's own listing. Gated by PLATFORM_ADMIN, same basis as the "
        "establish endpoint above."
    ),
)
async def list_configuration_entries(
    claims: Annotated[dict, Depends(require_platform_admin)],
    organization_id: Annotated[UUID, Depends(get_current_tenant)],
    management_service: Annotated[ConfigurationManagementService, Depends(get_configuration_management_service)],
) -> ConfigurationEntryListResponse:
    entries = await management_service.list_established(organization_id)
    return ConfigurationEntryListResponse(entries=entries)
