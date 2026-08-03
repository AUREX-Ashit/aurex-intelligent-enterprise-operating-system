# models/search.py
"""
WP-11 — Enterprise Search (C-093). Canonical, LOCKED physical schema per
`Master_Technical_Architecture.md` AMD-012 (the "Retrieval Service"
component boundary) — no column added, removed, or retyped beyond what
AMD-012 itself already specifies (`IRA-011 §5`/§6).

`organization_id` on every model below is a plain UUID column, not a
database-level `ForeignKey` to `organization_master`/`organizations` —
that table lives in `AuthService`'s own database, a separate service
boundary (`CLAUDE.md §8`: never access another service's database). The
FK AMD-012 documents is a logical reference, enforced by the caller's own
verified JWT `organization_id` claim (`dependencies.get_current_claims`),
not a physical constraint AIService's own database can express. The same
reasoning applies to `evidence_registry.confidence_rule_id`
(`confidence_scoring_registry` is unimplemented anywhere in this
repository, out of WP-11's own scope) — declared as a plain nullable
column, no FK.

Supersedes `models/rag.py`'s `RAGConfigModel`/`rag_configs` per `TD-109` —
that model is retained, unmigrated, per its own entry's "no runtime data
affected" disclosure; no new code writes to it.
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from models.database import Base


class VectorIndexRegistryModel(Base):
    """
    `vector_index_registry` (AMD-012). Configuration of a Vector Database
    index (Azure AI Search, per the frozen technology stack). One row per
    index; `DocumentChunkRegistryModel` rows reference the index their
    embedding lives in. Configuration/design only — retrieval mechanics
    are RTA-001's own runtime scope, not this table's.

    WP-11 BA-01 (Establish Enterprise Search Index Configuration) writes
    this table.
    """

    __tablename__ = "vector_index_registry"
    __table_args__ = (
        CheckConstraint(
            "retrieval_mode IN ('SEMANTIC', 'LEXICAL', 'HYBRID')",
            name="ck_vector_index_registry_retrieval_mode",
        ),
    )

    vector_index_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    index_name: Mapped[str] = mapped_column(String(255), nullable=False)
    embedding_model: Mapped[str] = mapped_column(String(255), nullable=False)
    embedding_dimension: Mapped[int] = mapped_column(Integer, nullable=False)
    retrieval_mode: Mapped[str] = mapped_column(String(50), nullable=False, default="HYBRID", server_default="HYBRID")
    refresh_cadence: Mapped[str | None] = mapped_column(String(255), nullable=True)
    active_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="1")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    organization_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True, index=True)
    """NULL for a platform-wide shared index; set for a tenant-dedicated one (AMD-012). See module docstring — logical, not physical, FK."""


class EvidenceRegistryModel(Base):
    """
    `evidence_registry` (Master Technical Architecture). Stores evidence
    supporting intelligence — the source document/passage a
    `DocumentChunkRegistryModel` row is chunked from.

    WP-11 BA-03 (Register Enterprise Search Content) writes this table —
    narrowly: a caller-supplied text passage's own evidence record, not a
    real document-ingestion/discovery pipeline (`IRA-011 §4.2`, C-090's
    own future domain).
    """

    __tablename__ = "evidence_registry"

    evidence_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    evidence_type: Mapped[str | None] = mapped_column(String(255), nullable=True)
    linked_entity_type: Mapped[str | None] = mapped_column(String(255), nullable=True)
    linked_entity_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    evidence_source: Mapped[str | None] = mapped_column(String(255), nullable=True)
    file_reference: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source_timestamp: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    confidence_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    externally_verified_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="0")
    legal_defensibility_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="0")
    retention_policy: Mapped[str | None] = mapped_column(String(255), nullable=True)
    document_hash_signature: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ai_extracted_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="0")
    active_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="1")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    organization_id: Mapped[uuid.UUID] = mapped_column(nullable=False, index=True)
    """AMD-001. Logical, not physical, FK to organization_master — see module docstring."""

    confidence_rule_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    """AMD-003. confidence_scoring_registry is unimplemented anywhere in this repository — no FK, logical or physical; out of WP-11's own scope."""


class DocumentChunkRegistryModel(Base):
    """
    `document_chunk_registry` (AMD-012). The physical unit of a source
    document once split for retrieval — the schema gap between
    `evidence_registry` (whole document/passage) and a Vector Database
    entry (one retrievable unit). Chunking strategy itself is
    intentionally not specified by this table (AMD-012's own comment) —
    WP-11 BA-03 applies a single, deliberately simple fixed-size pass,
    not a configurable strategy (`IRA-011 §5`).

    WP-11 BA-03 writes this table; BA-02 (Execute Enterprise Search)
    reads it via the Vector Database (`embedding_reference` — the vector
    itself is not stored here, per AMD-012).
    """

    __tablename__ = "document_chunk_registry"

    document_chunk_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    evidence_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("evidence_registry.evidence_id", ondelete="CASCADE"), nullable=False, index=True
    )
    chunk_sequence_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    chunk_locator: Mapped[str | None] = mapped_column(String(255), nullable=True)
    chunk_text_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)

    vector_index_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("vector_index_registry.vector_index_id", ondelete="SET NULL"), nullable=True, index=True
    )
    embedding_reference: Mapped[str | None] = mapped_column(String(255), nullable=True)
    embedding_model_version: Mapped[str | None] = mapped_column(String(255), nullable=True)
    active_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="1")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    organization_id: Mapped[uuid.UUID] = mapped_column(nullable=False, index=True)
    """AMD-001. Logical, not physical, FK to organization_master — see module docstring."""
