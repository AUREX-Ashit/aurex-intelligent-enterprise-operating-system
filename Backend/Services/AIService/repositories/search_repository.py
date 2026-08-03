# repositories/search_repository.py
"""
WP-11 — Enterprise Search (C-093) repositories. Every read is scoped to
`organization_id == caller's own claim OR organization_id IS NULL`
(platform-wide) — never an unscoped lookup by a caller-supplied
identifier, per `CLAUDE.md §21.4`(c). No repository method here accepts
a raw tenant identifier from the request body; every caller-facing
service method (`services/*.py`) passes the caller's own JWT-derived
`organization_id`, never a client-supplied one.
"""
from __future__ import annotations

import uuid

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.search import (
    DocumentChunkRegistryModel,
    EvidenceRegistryModel,
    VectorIndexRegistryModel,
)


class VectorIndexRegistryRepository:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db = db_session

    async def create(
        self,
        *,
        organization_id: uuid.UUID | None,
        index_name: str,
        embedding_model: str,
        embedding_dimension: int,
        retrieval_mode: str,
        refresh_cadence: str | None,
    ) -> VectorIndexRegistryModel:
        instance = VectorIndexRegistryModel(
            organization_id=organization_id,
            index_name=index_name,
            embedding_model=embedding_model,
            embedding_dimension=embedding_dimension,
            retrieval_mode=retrieval_mode,
            refresh_cadence=refresh_cadence,
            active_flag=True,
        )
        self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance

    async def list_visible(self, organization_id: uuid.UUID) -> list[VectorIndexRegistryModel]:
        """The caller's own tenant-dedicated rows plus every platform-wide row, active only."""
        query = select(VectorIndexRegistryModel).where(
            VectorIndexRegistryModel.active_flag.is_(True),
            or_(
                VectorIndexRegistryModel.organization_id == organization_id,
                VectorIndexRegistryModel.organization_id.is_(None),
            ),
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_active_by_exact_scope(
        self, organization_id: uuid.UUID | None, index_name: str
    ) -> VectorIndexRegistryModel | None:
        """
        Exact-scope lookup — `organization_id` matched precisely (including
        `NULL` for platform-wide), never the caller-visibility `OR NULL`
        fallback `get_by_name_for_caller` applies. Used by
        `SearchIndexConfigurationService.establish` to reject a duplicate
        `(organization_id, index_name)` pair before it can be created
        (`VV-AUDIT-WP-11` Finding 1 — no such constraint exists in AMD-012's
        own schema text, so this is an application-level guard, not a
        database-level one; `get_by_name_for_caller`'s own
        `.scalar_one_or_none()` would otherwise raise `MultipleResultsFound`
        once two rows share a scope, crashing BA-02/BA-03 with an unhandled
        500).
        """
        query = select(VectorIndexRegistryModel).where(
            VectorIndexRegistryModel.index_name == index_name,
            VectorIndexRegistryModel.active_flag.is_(True),
            VectorIndexRegistryModel.organization_id == organization_id
            if organization_id is not None
            else VectorIndexRegistryModel.organization_id.is_(None),
        )
        return (await self.db.execute(query)).scalar_one_or_none()

    async def get_by_name_for_caller(
        self, organization_id: uuid.UUID, index_name: str
    ) -> VectorIndexRegistryModel | None:
        """Scoped lookup — the caller's own tenant-dedicated row for this name if one exists, else a platform-wide row of the same name. Never any other tenant's row."""
        tenant_query = select(VectorIndexRegistryModel).where(
            VectorIndexRegistryModel.index_name == index_name,
            VectorIndexRegistryModel.organization_id == organization_id,
            VectorIndexRegistryModel.active_flag.is_(True),
        )
        tenant_row = (await self.db.execute(tenant_query)).scalar_one_or_none()
        if tenant_row is not None:
            return tenant_row

        platform_query = select(VectorIndexRegistryModel).where(
            VectorIndexRegistryModel.index_name == index_name,
            VectorIndexRegistryModel.organization_id.is_(None),
            VectorIndexRegistryModel.active_flag.is_(True),
        )
        return (await self.db.execute(platform_query)).scalar_one_or_none()

    async def get_default_for_caller(self, organization_id: uuid.UUID) -> VectorIndexRegistryModel | None:
        """Used when BA-02's own request omits `index_name` — the caller's own single tenant-dedicated active index, if exactly one exists."""
        query = select(VectorIndexRegistryModel).where(
            VectorIndexRegistryModel.organization_id == organization_id,
            VectorIndexRegistryModel.active_flag.is_(True),
        )
        rows = list((await self.db.execute(query)).scalars().all())
        return rows[0] if len(rows) == 1 else None

    async def get_by_id_for_caller(
        self, organization_id: uuid.UUID, vector_index_id: uuid.UUID
    ) -> VectorIndexRegistryModel | None:
        """Scoped by id — the caller's own tenant-dedicated row or a platform-wide row; never another tenant's row (`CLAUDE.md §21.4`(c))."""
        query = select(VectorIndexRegistryModel).where(
            VectorIndexRegistryModel.vector_index_id == vector_index_id,
            VectorIndexRegistryModel.active_flag.is_(True),
            or_(
                VectorIndexRegistryModel.organization_id == organization_id,
                VectorIndexRegistryModel.organization_id.is_(None),
            ),
        )
        return (await self.db.execute(query)).scalar_one_or_none()


class EvidenceRegistryRepository:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db = db_session

    async def create(
        self,
        *,
        organization_id: uuid.UUID,
        evidence_type: str | None,
        evidence_source: str | None,
        file_reference: str | None,
    ) -> EvidenceRegistryModel:
        instance = EvidenceRegistryModel(
            organization_id=organization_id,
            evidence_type=evidence_type,
            evidence_source=evidence_source,
            file_reference=file_reference,
            ai_extracted_flag=False,
            active_flag=True,
        )
        self.db.add(instance)
        await self.db.flush()
        return instance


class DocumentChunkRegistryRepository:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db = db_session

    async def create(
        self,
        *,
        organization_id: uuid.UUID,
        evidence_id: uuid.UUID,
        vector_index_id: uuid.UUID,
        chunk_sequence_number: int,
        chunk_locator: str | None,
        chunk_text_hash: str,
        embedding_reference: str,
        embedding_model_version: str,
    ) -> DocumentChunkRegistryModel:
        instance = DocumentChunkRegistryModel(
            organization_id=organization_id,
            evidence_id=evidence_id,
            vector_index_id=vector_index_id,
            chunk_sequence_number=chunk_sequence_number,
            chunk_locator=chunk_locator,
            chunk_text_hash=chunk_text_hash,
            embedding_reference=embedding_reference,
            embedding_model_version=embedding_model_version,
            active_flag=True,
        )
        self.db.add(instance)
        await self.db.flush()
        return instance

    async def list_for_index(
        self, *, vector_index_id: uuid.UUID, organization_id: uuid.UUID, top_k: int
    ) -> list[tuple[DocumentChunkRegistryModel, EvidenceRegistryModel]]:
        """
        Real, tenant-scoped retrieval — every chunk registered under this
        specific `vector_index_id` AND this caller's own `organization_id`
        (never another tenant's chunks, even if `vector_index_id` itself
        is a platform-wide index another tenant also registered content
        under — content registration is always organization-scoped,
        `services/content_registration_service.py`). Ordered by
        `created_at` descending — a real, if disclosed-primitive,
        ordering; no real embedding model is configured to rank by
        semantic relevance (`IRA-011 §4.6`).
        """
        query = (
            select(DocumentChunkRegistryModel, EvidenceRegistryModel)
            .join(EvidenceRegistryModel, DocumentChunkRegistryModel.evidence_id == EvidenceRegistryModel.evidence_id)
            .where(
                DocumentChunkRegistryModel.vector_index_id == vector_index_id,
                DocumentChunkRegistryModel.organization_id == organization_id,
                DocumentChunkRegistryModel.active_flag.is_(True),
            )
            .order_by(DocumentChunkRegistryModel.created_at.desc())
            .limit(top_k)
        )
        result = await self.db.execute(query)
        return [(row[0], row[1]) for row in result.all()]
