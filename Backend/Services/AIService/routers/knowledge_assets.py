# routers/knowledge_assets.py
"""WP-14 BA-04 — Establish Knowledge Asset (C-091 Knowledge Management)."""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import require_platform_admin
from models.database import get_db
from repositories.knowledge_asset_repository import KnowledgeAssetRegistryRepository
from schemas.knowledge_asset import (
    EstablishKnowledgeAssetRequest,
    KnowledgeAssetResponse,
    TransitionKnowledgeAssetRequest,
)
from services.knowledge_asset_service import KnowledgeAssetService

router = APIRouter(prefix="/knowledge-assets", tags=["Knowledge Assets"])


# ---------------------------------------------------------------------------
# Dependency factories
# ---------------------------------------------------------------------------

async def get_knowledge_asset_repo(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> KnowledgeAssetRegistryRepository:
    return KnowledgeAssetRegistryRepository(session)


async def get_knowledge_asset_service(
    repo: Annotated[KnowledgeAssetRegistryRepository, Depends(get_knowledge_asset_repo)],
) -> KnowledgeAssetService:
    return KnowledgeAssetService(repo)


# ---------------------------------------------------------------------------
# BA-04 — Establish Knowledge Asset
# ---------------------------------------------------------------------------

@router.post(
    "",
    response_model=KnowledgeAssetResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Establish Knowledge Asset (WP-14 BA-04)",
    description=(
        "Writes a real, tenant-scoped knowledge_asset_registry row (AMD-012, LOCKED), "
        "curation_status='PROPOSED'. Mandatory Provenance (EIA-001 Vol. I §7.3) rejected "
        "with 422 if missing. Gated by PLATFORM_ADMIN — no dedicated persona exists yet "
        "for C-091 (Charter §4/§10), same interim measure this repository already uses "
        "platform-wide."
    ),
)
async def establish_knowledge_asset(
    request: EstablishKnowledgeAssetRequest,
    claims: Annotated[dict, Depends(require_platform_admin)],
    service: Annotated[KnowledgeAssetService, Depends(get_knowledge_asset_service)],
) -> KnowledgeAssetResponse:
    organization_id = UUID(claims["organization_id"])
    actor_id = UUID(claims["person_id"])
    return await service.establish(organization_id, actor_id, request)


@router.get(
    "/{knowledge_asset_id}",
    response_model=KnowledgeAssetResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve Knowledge Asset by id (WP-14 BA-04)",
    description=(
        "Scoped strictly to the caller's own Organization (404 for any other tenant's "
        "row, never a cross-tenant disclosure). Gated by PLATFORM_ADMIN, same basis as "
        "the establish path — the Charter treats BA-04 as a single, undifferentiated "
        "interim-authorization Business Activity (Charter §4/§10), not split by "
        "read/write."
    ),
)
async def get_knowledge_asset(
    knowledge_asset_id: UUID,
    claims: Annotated[dict, Depends(require_platform_admin)],
    service: Annotated[KnowledgeAssetService, Depends(get_knowledge_asset_service)],
) -> KnowledgeAssetResponse:
    organization_id = UUID(claims["organization_id"])
    return await service.get_by_id(organization_id, knowledge_asset_id)


# ---------------------------------------------------------------------------
# BA-04 Increment — Knowledge Asset Lifecycle Transition + ACCEPTED Domain
# Event (TDS-014, implementation authorized 2026-08-16)
# ---------------------------------------------------------------------------

@router.post(
    "/{knowledge_asset_id}/transition",
    response_model=KnowledgeAssetResponse,
    status_code=status.HTTP_200_OK,
    summary="Transition Knowledge Asset lifecycle status (WP-14 BA-04 Increment)",
    description=(
        "Transitions a PROPOSED Knowledge Asset to VALIDATED/ACCEPTED/REJECTED "
        "(TDS-014 §2) — no other transition edge is authorized. 409 if the asset "
        "is not currently PROPOSED (already transitioned or invalid state). On a "
        "successful transition to ACCEPTED, attempts a best-effort publication of "
        "aurex.aiservice.knowledge_asset.accepted v1.0.0 (RO-DEC-BA04-INC-007) — "
        "publication failure does not affect the already-committed ACCEPTED state. "
        "Gated by PLATFORM_ADMIN, same basis as establish/get_by_id."
    ),
)
async def transition_knowledge_asset(
    knowledge_asset_id: UUID,
    request: TransitionKnowledgeAssetRequest,
    claims: Annotated[dict, Depends(require_platform_admin)],
    service: Annotated[KnowledgeAssetService, Depends(get_knowledge_asset_service)],
) -> KnowledgeAssetResponse:
    organization_id = UUID(claims["organization_id"])
    actor_id = UUID(claims["person_id"])
    return await service.transition(organization_id, actor_id, knowledge_asset_id, request)
