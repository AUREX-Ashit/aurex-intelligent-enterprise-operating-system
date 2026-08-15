# routers/intelligence_candidates.py
"""WP-14 BA-02 — Register Enterprise Intelligence Candidate (C-090 Enterprise Discovery).

Only `POST /intelligence-candidates` is built here — `IRA-014 §6` BA-02's
own "APIs/services required" row names only the register path, unlike
BA-01/BA-04 which each also name a `GET`. A resolution/listing surface
(BA-03's own "resolution queue," `IRA-014 §9` Plan B) is deliberately not
built by this router.
"""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import require_platform_admin
from models.database import get_db
from repositories.unclassified_intelligence_repository import UnclassifiedIntelligenceRegistryRepository
from schemas.unclassified_intelligence import IntelligenceCandidateResponse, RegisterIntelligenceCandidateRequest
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
