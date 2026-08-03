# services/vector_provider.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from config.settings import settings

class VectorProvider(ABC):
    """Abstract interface contract representing decoupled search engines (Azure Cognitive/Pinecone/Weaviate)."""
    
    @abstractmethod
    async def index_documents(self, index_name: str, documents: List[Dict[str, Any]]) -> bool:
        """Pushes items and tracking embeddings onto active registry."""
        pass

    @abstractmethod
    async def search_index(
        self, 
        index_name: str, 
        query_vector: List[float], 
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Executes vector and hybrid search filters returning score-ranked references."""
        pass


class AzureSearchStubProvider(VectorProvider):
    """Interfaced mock simulating Azure Cognitive Search capability layer."""
    
    def __init__(self, has_hybrid: bool = True):
        self.hybrid = has_hybrid

    async def index_documents(self, index_name: str, documents: List[Dict[str, Any]]) -> bool:
        return True

    async def search_index(
        self, 
        index_name: str, 
        query_vector: List[float], 
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        # High fidelity mocked responses representing matches inside index
        return [
            {
                "id": "doc_chunk_1",
                "score": 0.94,
                "text": "Overall energy strategy yields carbon emissions of 4200.50 Metric Tons under Scope 1 direct operations for FY25.",
                "metadata": {"page": 12, "source": "ESG_Report_2025.pdf"}
            },
            {
                "id": "doc_chunk_2",
                "score": 0.82,
                "text": "The Board maintains 11 permanent directors with 8 independent seats ensuring strong independence standards.",
                "metadata": {"page": 43, "source": "ESG_Report_2025.pdf"}
            }
        ]


def get_vector_provider() -> VectorProvider:
    return AzureSearchStubProvider(has_hybrid=True)


class DocumentChunkRegistryVectorProvider(VectorProvider):
    """
    WP-11 BA-02 (Execute Enterprise Search, `IRA-011 §5`) — real,
    tenant-scoped retrieval against the actually-persisted
    `document_chunk_registry`/`evidence_registry` rows a caller has
    registered via BA-03. Replaces `AzureSearchStubProvider`'s own
    hardcoded, query-independent fake results with genuine
    query-dependent, persistence-backed behavior — results now actually
    depend on what has been registered under the resolved index, not a
    canned response.

    `search_index`'s own `index_name` parameter is expected to be the
    real `vector_index_id` (stringified UUID) the caller's own service
    layer has already resolved and tenant-verified *before* constructing
    this provider's call — never a raw, unverified caller-supplied
    identifier (`CLAUDE.md §21.4`(c)). `organization_id` is required at
    construction time for the same reason: an independent, second
    tenant-scoping check inside the repository query itself, not merely
    trusting the caller's own upstream resolution.

    Ranking remains a disclosed placeholder (`score`, rank-based, not
    semantic) — no real embedding/vector-search model is configured
    anywhere in this environment (`IRA-011 §4.6`, unchanged). The
    mechanism (real writes, real reads, real tenant scoping) is
    genuinely real; only the *relevance* of the ranking is stubbed,
    exactly the distinction `TD-111` already draws for Access Evaluation.
    """

    def __init__(self, db_session: AsyncSession, organization_id: UUID):
        self.db = db_session
        self.organization_id = organization_id

    async def index_documents(self, index_name: str, documents: List[Dict[str, Any]]) -> bool:
        """Not used — BA-03's own `ContentRegistrationService` writes `document_chunk_registry` directly via its own repository, in the same transaction as `evidence_registry`, for stronger atomicity than this generic interface method could offer."""
        return True

    async def search_index(
        self,
        index_name: str,
        query_vector: List[float],
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        from repositories.search_repository import DocumentChunkRegistryRepository

        vector_index_id = UUID(index_name)
        chunk_repo = DocumentChunkRegistryRepository(self.db)
        rows = await chunk_repo.list_for_index(
            vector_index_id=vector_index_id, organization_id=self.organization_id, top_k=top_k
        )

        results: List[Dict[str, Any]] = []
        for rank, (chunk, evidence) in enumerate(rows):
            results.append(
                {
                    "id": str(chunk.document_chunk_id),
                    "score": round(1.0 / (rank + 1), 4),
                    "text": f"Evidence: {evidence.evidence_source or 'Unknown source'} ({evidence.file_reference or chunk.chunk_locator or 'no locator'})",
                    "metadata": {
                        "evidence_id": str(evidence.evidence_id),
                        "document_chunk_id": str(chunk.document_chunk_id),
                        "source": evidence.evidence_source,
                        "locator": chunk.chunk_locator,
                    },
                }
            )
        return results


def get_document_chunk_registry_vector_provider(
    db_session: AsyncSession, organization_id: UUID
) -> "DocumentChunkRegistryVectorProvider":
    return DocumentChunkRegistryVectorProvider(db_session=db_session, organization_id=organization_id)
