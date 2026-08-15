# models/knowledge_asset.py
"""
WP-14 BA-04 — Establish Knowledge Asset (C-091 Knowledge Management).
Canonical, LOCKED physical schema per `Master_Technical_Architecture.md`
AMD-012 (`knowledge_asset_registry`, line 3226) — no column added, removed,
or retyped beyond what AMD-012 itself already specifies. Hosting-service
determination per `WP-14_BA-04_Establish_Knowledge_Asset_Business_Activity_
Charter.md §8` (corrected update): `AIService` is the evidenced physical
host; the broader, formal WP-14-wide hosting decision (BA-05's own
architectural matter) remains separately open and is not resolved here.

`organization_id` is a plain UUID column, not a database-level `ForeignKey`
to `organization_master` — that table lives in `AuthService`'s own
database, a separate service boundary (`CLAUDE.md §8`). The FK AMD-012
documents is a logical reference, enforced by the caller's own verified JWT
`organization_id` claim, exactly the same precedent already established in
`models/search.py` for `evidence_registry`/`document_chunk_registry`.

`source_ingestion_id` (→ `data_ingestion_registry`) and `confidence_rule_id`
(→ `confidence_scoring_registry`) are both declared as plain nullable
columns, no FK — both target tables are LOCKED at the architecture-document
level only, with no physical Backend model anywhere in this repository
(independently re-verified during the BA-04 dependency review; charter
§15/§16). Mirrors the identical, already-shipped precedent
`models/search.py` already established for `evidence_registry.
confidence_rule_id`. Neither table is created by this change.
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, CheckConstraint, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from models.database import Base


class KnowledgeAssetRegistryModel(Base):
    """
    `knowledge_asset_registry` (AMD-012). Physical realization of the
    Enterprise Knowledge Model's Knowledge Asset concept (`EIA-001 Vol. I
    §7`: "a curated, governed unit of knowledge produced from one or more
    Signals"). WP-14 BA-04 (Establish Knowledge Asset) writes this table.
    """

    __tablename__ = "knowledge_asset_registry"
    __table_args__ = (
        CheckConstraint(
            "curation_status IN ('PROPOSED', 'VALIDATED', 'ACCEPTED', 'REJECTED', 'SUPERSEDED')",
            name="ck_knowledge_asset_registry_curation_status",
        ),
    )

    knowledge_asset_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    knowledge_asset_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    knowledge_asset_type: Mapped[str | None] = mapped_column(String(255), nullable=True)

    source_ingestion_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    """AMD-012. data_ingestion_registry is unimplemented anywhere in this repository — no FK, logical or physical; not required at establishment (BA-04 Charter §16)."""

    curation_status: Mapped[str] = mapped_column(
        String(50), nullable=False, default="PROPOSED", server_default="PROPOSED"
    )
    provenance_reference: Mapped[str | None] = mapped_column(String(255), nullable=True)
    """Schema-level nullable; application-layer mandatory at establishment per EIA-001 Vol. I §7.3 (BA-04 Charter §6/§7)."""

    freshness_last_confirmed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    graph_engine_reference: Mapped[str | None] = mapped_column(String(255), nullable=True)
    """BA-05's own scope (live Neo4j write) — always NULL from BA-04 (Charter §19)."""

    confidence_rule_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    """AMD-003. confidence_scoring_registry is unimplemented anywhere in this repository — no FK, logical or physical; not required at establishment (BA-04 Charter §15/§16)."""

    active_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="0")
    """AMD-012's own LOCKED schema text states DEFAULT FALSE for this table specifically (unlike sibling AMD-012 tables' DEFAULT TRUE) — preserved verbatim, not altered."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    organization_id: Mapped[uuid.UUID] = mapped_column(nullable=False, index=True)
    """AMD-001. Logical, not physical, FK to organization_master — see module docstring."""
