# routers/search.py
"""WP-11 — Enterprise Search (C-093). BA-01/02/03 endpoints (`IRA-011 §5`)."""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_current_claims, require_platform_admin
from models.database import get_db
from repositories.search_repository import (
    DocumentChunkRegistryRepository,
    EvidenceRegistryRepository,
    VectorIndexRegistryRepository,
)
from schemas.search import (
    EstablishIndexConfigurationRequest,
    ExecuteSearchRequest,
    IndexConfigurationListResponse,
    IndexConfigurationResponse,
    RegisterContentRequest,
    RegisteredContentResponse,
    SearchResponse,
)
from services.content_registration_service import ContentRegistrationService
from services.embedding_provider import EmbeddingProvider, get_embedding_provider
from services.rag_engine import RAGEngine
from services.search_execution_service import SearchExecutionService
from services.search_index_service import SearchIndexConfigurationService
from services.vector_provider import DocumentChunkRegistryVectorProvider

router = APIRouter(prefix="/search", tags=["Enterprise Search"])


# ---------------------------------------------------------------------------
# Dependency factories
# ---------------------------------------------------------------------------

async def get_vector_index_repo(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> VectorIndexRegistryRepository:
    return VectorIndexRegistryRepository(session)


async def get_evidence_repo(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> EvidenceRegistryRepository:
    return EvidenceRegistryRepository(session)


async def get_chunk_repo(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> DocumentChunkRegistryRepository:
    return DocumentChunkRegistryRepository(session)


async def get_index_service(
    index_repo: Annotated[VectorIndexRegistryRepository, Depends(get_vector_index_repo)],
) -> SearchIndexConfigurationService:
    return SearchIndexConfigurationService(index_repo)


async def get_content_service(
    session: Annotated[AsyncSession, Depends(get_db)],
    index_repo: Annotated[VectorIndexRegistryRepository, Depends(get_vector_index_repo)],
    evidence_repo: Annotated[EvidenceRegistryRepository, Depends(get_evidence_repo)],
    chunk_repo: Annotated[DocumentChunkRegistryRepository, Depends(get_chunk_repo)],
) -> ContentRegistrationService:
    return ContentRegistrationService(session, index_repo, evidence_repo, chunk_repo)


async def get_search_service(
    session: Annotated[AsyncSession, Depends(get_db)],
    index_repo: Annotated[VectorIndexRegistryRepository, Depends(get_vector_index_repo)],
    embedding_provider: Annotated[EmbeddingProvider, Depends(get_embedding_provider)],
    claims: Annotated[dict, Depends(get_current_claims)],
) -> SearchExecutionService:
    organization_id = UUID(claims["organization_id"])
    vector_db = DocumentChunkRegistryVectorProvider(db_session=session, organization_id=organization_id)
    rag_engine = RAGEngine(embedder=embedding_provider, vector_db=vector_db)
    return SearchExecutionService(index_repo, rag_engine)


# ---------------------------------------------------------------------------
# BA-01 — Establish Enterprise Search Index Configuration
# ---------------------------------------------------------------------------

@router.post(
    "/index-configurations",
    response_model=IndexConfigurationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Establish Enterprise Search Index Configuration (WP-11 BA-01)",
    description=(
        "Writes a real, tenant-scoped vector_index_registry row (AMD-012, LOCKED). "
        "Gated by PLATFORM_ADMIN — no dedicated persona exists yet (IRA-011 §5), same "
        "interim measure this repository already uses platform-wide. platform_wide=True "
        "establishes a platform-wide shared index (organization_id NULL) instead."
    ),
)
async def establish_index_configuration(
    request: EstablishIndexConfigurationRequest,
    claims: Annotated[dict, Depends(require_platform_admin)],
    service: Annotated[SearchIndexConfigurationService, Depends(get_index_service)],
) -> IndexConfigurationResponse:
    organization_id = UUID(claims["organization_id"])
    return await service.establish(organization_id, request)


@router.get(
    "/index-configurations",
    response_model=IndexConfigurationListResponse,
    status_code=status.HTTP_200_OK,
    summary="List visible Enterprise Search Index Configurations (WP-11 BA-01)",
    description=(
        "Lists the caller's own tenant-dedicated index configurations plus every "
        "platform-wide one. Any authenticated caller — genuinely tenant-scoped, not "
        "PLATFORM_ADMIN-only, mirroring IRA-010's own BA-01 (resolve) precedent."
    ),
)
async def list_index_configurations(
    claims: Annotated[dict, Depends(get_current_claims)],
    service: Annotated[SearchIndexConfigurationService, Depends(get_index_service)],
) -> IndexConfigurationListResponse:
    organization_id = UUID(claims["organization_id"])
    return await service.list_visible(organization_id)


# ---------------------------------------------------------------------------
# BA-03 — Register Enterprise Search Content
# ---------------------------------------------------------------------------

@router.post(
    "/content",
    response_model=RegisteredContentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register Enterprise Search Content (WP-11 BA-03)",
    description=(
        "Writes evidence_registry + document_chunk_registry rows (AMD-012, LOCKED) for a "
        "caller-supplied text passage — no file upload, no Discovery Provider connection, "
        "no configurable chunking (IRA-011 §4.2, deliberately narrow). Gated by "
        "PLATFORM_ADMIN, same basis as BA-01's own establish path."
    ),
)
async def register_content(
    request: RegisterContentRequest,
    claims: Annotated[dict, Depends(require_platform_admin)],
    service: Annotated[ContentRegistrationService, Depends(get_content_service)],
) -> RegisteredContentResponse:
    organization_id = UUID(claims["organization_id"])
    return await service.register(organization_id, request)


# ---------------------------------------------------------------------------
# BA-02 — Execute Enterprise Search
# ---------------------------------------------------------------------------

@router.post(
    "/query",
    response_model=SearchResponse,
    status_code=status.HTTP_200_OK,
    summary="Execute Enterprise Search (WP-11 BA-02)",
    description=(
        "Embeds the query, resolves the caller's own tenant-scoped (or a named "
        "platform-wide) index, and returns real, evidence-cited results from content "
        "registered via BA-03 — reuses RAGEngine.build_context()'s own orchestration "
        "shape (IRA-011 §5). Any authenticated caller may search their own scope; an "
        "honest empty-state message is returned when no content has been registered."
    ),
)
async def execute_search(
    request: ExecuteSearchRequest,
    claims: Annotated[dict, Depends(get_current_claims)],
    service: Annotated[SearchExecutionService, Depends(get_search_service)],
) -> SearchResponse:
    organization_id = UUID(claims["organization_id"])
    return await service.execute(organization_id, request)
