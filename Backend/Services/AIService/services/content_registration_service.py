# services/content_registration_service.py
"""
WP-11 BA-03 — Register Enterprise Search Content (`IRA-011 §4.2`/§5, new
Business Activity — required because `document_chunk_registry.evidence_id`
is a `NOT NULL` FK to `evidence_registry`, wholly unimplemented anywhere
in this repository before this Work Package).

Deliberately narrow: accepts a caller-supplied text passage only. No
file upload, no Discovery Provider connection (`discovery_provider_
registry`, AMD-013 — C-090's own future domain), no configurable
chunking strategy — a single, fixed-size chunking pass, per AMD-012's
own comment that "chunking strategy itself... is intentionally not
specified by this table." Gated by `PLATFORM_ADMIN` at the router, same
basis as BA-01's own establish path.
"""
from __future__ import annotations

import hashlib
import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.search_repository import (
    DocumentChunkRegistryRepository,
    EvidenceRegistryRepository,
    VectorIndexRegistryRepository,
)
from schemas.search import RegisterContentRequest, RegisteredContentResponse
from services.embedding_provider import AzureEmbeddingStubProvider

_CHUNK_SIZE_CHARS = 1000


def _fixed_size_chunks(text: str, chunk_size: int = _CHUNK_SIZE_CHARS) -> list[str]:
    """A single, deliberately simple fixed-size chunking pass — not a configurable strategy (see module docstring)."""
    stripped = text.strip()
    if not stripped:
        return []
    return [stripped[i : i + chunk_size] for i in range(0, len(stripped), chunk_size)]


class ContentRegistrationService:
    """Business Activity orchestrator for BA-03."""

    def __init__(
        self,
        db_session: AsyncSession,
        index_repo: VectorIndexRegistryRepository,
        evidence_repo: EvidenceRegistryRepository,
        chunk_repo: DocumentChunkRegistryRepository,
    ) -> None:
        self.db = db_session
        self.index_repo = index_repo
        self.evidence_repo = evidence_repo
        self.chunk_repo = chunk_repo

    async def register(
        self, organization_id: uuid.UUID, request: RegisterContentRequest
    ) -> RegisteredContentResponse:
        index = await self.index_repo.get_by_name_for_caller(organization_id, request.index_name)
        if index is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No visible index configuration named '{request.index_name}' — establish one first (BA-01).",
            )

        chunks = _fixed_size_chunks(request.text)
        if not chunks:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="text must contain non-whitespace content.")

        # Embeds using a provider sized to *this* index's own configured
        # embedding_dimension, not a platform-wide default — CERT-WP-11
        # Observation 2: the prior generic (always-1536) provider made
        # BA-03 fail for any index established at a different dimension.
        # The mismatch check below remains a genuine safety net for a
        # future real provider swap; it is no longer reachable against
        # the current stub, which is the correct outcome, not merely a
        # suppressed check.
        embedding_provider = AzureEmbeddingStubProvider(
            model_name=index.embedding_model, dimensions=index.embedding_dimension
        )

        evidence = await self.evidence_repo.create(
            organization_id=organization_id,
            evidence_type=request.evidence_type,
            evidence_source=request.evidence_source,
            file_reference=request.file_reference,
        )

        document_chunk_ids: list[uuid.UUID] = []
        for sequence_number, chunk_text in enumerate(chunks):
            embedding_vector = await embedding_provider.get_embedding(chunk_text)
            if len(embedding_vector) != index.embedding_dimension:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=(
                        f"Embedding provider produced a {len(embedding_vector)}-dimension vector, "
                        f"but index '{index.index_name}' is configured for {index.embedding_dimension} "
                        "dimensions (vector_index_registry.embedding_dimension)."
                    ),
                )

            chunk_text_hash = hashlib.sha256(chunk_text.encode("utf-8")).hexdigest()
            chunk = await self.chunk_repo.create(
                organization_id=organization_id,
                evidence_id=evidence.evidence_id,
                vector_index_id=index.vector_index_id,
                chunk_sequence_number=sequence_number,
                chunk_locator=f"{request.file_reference or evidence.evidence_id}#chunk={sequence_number}",
                chunk_text_hash=chunk_text_hash,
                embedding_reference=f"local-chunk-{chunk_text_hash[:16]}",
                embedding_model_version=index.embedding_model,
            )
            document_chunk_ids.append(chunk.document_chunk_id)

        await self.db.commit()
        await self.db.refresh(evidence)

        return RegisteredContentResponse(
            evidence_id=evidence.evidence_id,
            vector_index_id=index.vector_index_id,
            chunk_count=len(document_chunk_ids),
            document_chunk_ids=document_chunk_ids,
            created_at=evidence.created_at,
        )
