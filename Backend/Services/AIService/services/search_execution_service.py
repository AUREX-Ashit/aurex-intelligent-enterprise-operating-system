# services/search_execution_service.py
"""
WP-11 BA-02 — Execute Enterprise Search (`IRA-011 §5`). Reuses
`RAGEngine.build_context()` literally, not re-implemented — its own
`embed -> search -> assemble` orchestration shape, re-wired to the real,
persisted `vector_index_registry` configuration (BA-01) and real,
tenant-scoped `document_chunk_registry` content (BA-03) via
`DocumentChunkRegistryVectorProvider`, instead of `AzureSearchStubProvider`'s
own hardcoded, query-independent fake results.

`index_name` is never accepted from the caller as a raw identifier to
search against directly — always resolved first, scoped to the caller's
own `organization_id` (`VectorIndexRegistryRepository`), per
`CLAUDE.md §21.4`(c). Structural resolution of that scoping is what
prevents Organization A from ever reaching Organization B's own
tenant-dedicated index or content, not a bolted-on check.
"""
from __future__ import annotations

import uuid

from fastapi import HTTPException, status

from repositories.search_repository import VectorIndexRegistryRepository
from schemas.search import ExecuteSearchRequest, SearchResponse, SearchResultItem
from services.rag_engine import RAGEngine


class SearchExecutionService:
    """Business Activity orchestrator for BA-02."""

    def __init__(self, index_repo: VectorIndexRegistryRepository, rag_engine: RAGEngine) -> None:
        self.index_repo = index_repo
        self.rag_engine = rag_engine

    async def execute(self, organization_id: uuid.UUID, request: ExecuteSearchRequest) -> SearchResponse:
        if request.index_name:
            index = await self.index_repo.get_by_name_for_caller(organization_id, request.index_name)
        else:
            index = await self.index_repo.get_default_for_caller(organization_id)

        if index is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    "No resolvable index configuration — name it explicitly, or establish exactly "
                    "one tenant-dedicated index first (BA-01), before querying without a name."
                ),
            )

        # Real orchestration, literally reused (IRA-011 §5): embed -> search -> assemble.
        # `index_name` here is the resolved, tenant-verified vector_index_id, not a raw
        # caller-supplied string — the provider's own second, independent tenant check
        # (services/vector_provider.py::DocumentChunkRegistryVectorProvider) still applies.
        await self.rag_engine.build_context(
            index_name=str(index.vector_index_id), query=request.query, top_k=request.top_k
        )

        # Structured items for the API response, from the same real, tenant-scoped query
        # `build_context()` just ran (TD candidate: two reads instead of one — `IRA-011`-class
        # disclosed inefficiency, not a correctness gap; see IMP-REPORT-WP-11).
        query_vector = await self.rag_engine.embedder.get_embedding(request.query)
        raw_results = await self.rag_engine.vector_db.search_index(
            index_name=str(index.vector_index_id), query_vector=query_vector, top_k=request.top_k
        )

        if not raw_results:
            return SearchResponse(
                vector_index_id=index.vector_index_id,
                results=[],
                message="No matching references found — no content has been registered under this index yet.",
            )

        results = [
            SearchResultItem(
                document_chunk_id=uuid.UUID(item["id"]),
                evidence_id=uuid.UUID(item["metadata"]["evidence_id"]),
                score=item["score"],
                citation=item["text"],
                metadata=item["metadata"],
            )
            for item in raw_results
        ]
        return SearchResponse(vector_index_id=index.vector_index_id, results=results)
