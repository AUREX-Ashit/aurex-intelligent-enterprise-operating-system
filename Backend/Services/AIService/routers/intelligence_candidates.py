# routers/intelligence_candidates.py
"""WP-14 BA-02/BA-03 — Register + Resolve Enterprise Intelligence Candidate (C-090 Enterprise Discovery).

No `GET`/list endpoint is built here — `IRA-014 §6` names only `POST
/intelligence-candidates` (BA-02) and `POST .../{id}/resolve` (BA-03) for
this resource, unlike BA-01/BA-04 which each also name a `GET`. BA-03's
own "resolution queue" frontend (`IRA-014 §9` Plan B) reads the candidate
directly from its own resolve response, mirroring BA-04's established
precedent — no separate listing surface is built.
"""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import require_platform_admin
from models.database import get_db
from repositories.customer_metric_repository import CustomerMetricRegistryRepository
from repositories.search_repository import EvidenceRegistryRepository
from repositories.unclassified_intelligence_repository import UnclassifiedIntelligenceRegistryRepository
from schemas.unclassified_intelligence import (
    IntelligenceCandidateResponse,
    RegisterIntelligenceCandidateRequest,
    ResolveIntelligenceCandidateRequest,
    ResolvedIntelligenceCandidateResponse,
)
from services.intelligence_candidate_resolution_service import IntelligenceCandidateResolutionService
from services.unclassified_intelligence_service import IntelligenceCandidateService

router = APIRouter(prefix="/intelligence-candidates", tags=["Intelligence Candidates"])


# ---------------------------------------------------------------------------
# Dependency factories
# ---------------------------------------------------------------------------

async def get_intelligence_candidate_repo(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> UnclassifiedIntelligenceRegistryRepository:
    return UnclassifiedIntelligenceRegistryRepository(session)


async def get_intelligence_candidate_service(
    repo: Annotated[UnclassifiedIntelligenceRegistryRepository, Depends(get_intelligence_candidate_repo)],
) -> IntelligenceCandidateService:
    return IntelligenceCandidateService(repo)


async def get_customer_metric_repo(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> CustomerMetricRegistryRepository:
    return CustomerMetricRegistryRepository(session)


async def get_evidence_repo(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> EvidenceRegistryRepository:
    return EvidenceRegistryRepository(session)


async def get_intelligence_candidate_resolution_service(
    session: Annotated[AsyncSession, Depends(get_db)],
    candidate_repo: Annotated[UnclassifiedIntelligenceRegistryRepository, Depends(get_intelligence_candidate_repo)],
    customer_metric_repo: Annotated[CustomerMetricRegistryRepository, Depends(get_customer_metric_repo)],
    evidence_repo: Annotated[EvidenceRegistryRepository, Depends(get_evidence_repo)],
) -> IntelligenceCandidateResolutionService:
    return IntelligenceCandidateResolutionService(session, candidate_repo, customer_metric_repo, evidence_repo)


# ---------------------------------------------------------------------------
# BA-02 — Register Enterprise Intelligence Candidate
# ---------------------------------------------------------------------------

@router.post(
    "",
    response_model=IntelligenceCandidateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register Enterprise Intelligence Candidate (WP-14 BA-02)",
    description=(
        "Writes a real, tenant-scoped unclassified_intelligence_registry row (AMD-005, LOCKED), "
        "resolution_status='PENDING'. extraction_method restricted to MANUAL_ENTRY/API_INGEST — "
        "any of the five automated values is rejected (422), per IRA-014 §5.2's own disclosed "
        "deferral (no live extraction pipeline exists). Gated by PLATFORM_ADMIN — no dedicated "
        "persona exists yet, same interim measure this repository already uses platform-wide."
    ),
)
async def register_intelligence_candidate(
    request: RegisterIntelligenceCandidateRequest,
    claims: Annotated[dict, Depends(require_platform_admin)],
    service: Annotated[IntelligenceCandidateService, Depends(get_intelligence_candidate_service)],
) -> IntelligenceCandidateResponse:
    organization_id = UUID(claims["organization_id"])
    actor_id = UUID(claims["person_id"])
    return await service.register(organization_id, actor_id, request)


# ---------------------------------------------------------------------------
# BA-03 — Resolve Enterprise Intelligence Candidate (Convergence Decision)
# ---------------------------------------------------------------------------

@router.post(
    "/{unclassified_id}/resolve",
    response_model=ResolvedIntelligenceCandidateResponse,
    status_code=status.HTTP_200_OK,
    summary="Resolve Enterprise Intelligence Candidate (WP-14 BA-03)",
    description=(
        "Resolves a PENDING candidate to exactly one of MAPPED_TO_EXISTING/NEW_CDE_CREATED/"
        "DISCARDED (Complete_Blueprint.md §5.0c Binding 5). Semantic Matching is always "
        "attempted before NEW_CDE_CREATED (a disclosed, non-AI placeholder — no real "
        "Reasoning Engine exists anywhere in this platform, TD-133). A net-new CDE writes "
        "customer_metric_registry (cde_tier='TENANT') and carries an Evidence reference "
        "(evidence_registry, SD-002-041). 409 if the candidate was already resolved. Gated "
        "by PLATFORM_ADMIN, same basis as BA-02's own register path."
    ),
)
async def resolve_intelligence_candidate(
    unclassified_id: UUID,
    request: ResolveIntelligenceCandidateRequest,
    claims: Annotated[dict, Depends(require_platform_admin)],
    service: Annotated[IntelligenceCandidateResolutionService, Depends(get_intelligence_candidate_resolution_service)],
) -> ResolvedIntelligenceCandidateResponse:
    organization_id = UUID(claims["organization_id"])
    actor_id = UUID(claims["person_id"])
    return await service.resolve(organization_id, actor_id, unclassified_id, request)
