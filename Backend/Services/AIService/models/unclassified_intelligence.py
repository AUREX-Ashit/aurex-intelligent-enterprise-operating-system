# models/unclassified_intelligence.py
"""WP-14 BA-02 — Register Enterprise Intelligence Candidate (C-090 Enterprise Discovery). Physical schema per `Master_Technical_Architecture.md` AMD-005 (`unclassified_intelligence_registry`, line 5453, LOCKED) — no column added, removed, or retyped beyond what AMD-005 itself specifies (`IRA-014 §6` BA-02 row).

`organization_id` is a plain, non-nullable UUID column, not a database-level
`ForeignKey` to `organization_master` — that table lives in `AuthService`'s
own database, a separate service boundary (`CLAUDE.md §8`), mirroring
`models/knowledge_asset.py`'s own identical precedent. Unlike
`discovery_provider_registry` (BA-01), this table's own RLS policy is
unqualified (`organization_id = current_setting(...)`, no `OR NULL`
clause, `Master_Technical_Architecture.md:5487-5488`) — every row is
strictly tenant-scoped, no platform-wide sharing.

`resolved_by_user_id`/`resolved_metric_id`/`resolved_customer_metric_id`
are declared nullable with no FK, logical or physical —
`user_registry`/`metric_registry`/`customer_metric_registry` have no
physical Backend model anywhere in this repository, the identical
disposition already established for BA-01's/BA-04's own optional FKs.
These three columns, `resolved_at`, and `convergence_signal_raised_flag`
are BA-03's own resolution-time fields — this Business Activity (BA-02,
establish only) never writes to them; they remain at their schema
defaults (`NULL`/`FALSE`) on every row this Business Activity creates.

`llm_label_suggestion`/`llm_confidence_score`/`probable_domain`/
`probable_bq_id` are AI-suggested fields with no live extraction pipeline
anywhere in this repository (`IRA-014 §5.2`'s own disclosed deferral) —
not exposed as caller inputs, remain `NULL` on every BA-02-created row,
mirroring `knowledge_asset_registry.source_ingestion_id`'s own identical
"physically real, not yet populated by this Business Activity" precedent.
"""
import uuid
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import Boolean, CheckConstraint, DateTime, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from models.database import Base


class UnclassifiedIntelligenceRegistryModel(Base):
    """
    `unclassified_intelligence_registry` (AMD-005). One row per extracted
    fact with no matching Canonical Data Element, held per
    `Complete_Blueprint.md §5.0c` Binding 5's own guarantee: "An extracted
    fact with no matching CDE is never discarded."

    WP-14 BA-02 (Register Enterprise Intelligence Candidate) writes this
    table, restricted to `extraction_method IN ('MANUAL_ENTRY',
    'API_INGEST')` only (`IRA-014 §5.2`) — the DB's own CHECK constraint
    permits all seven values; the narrower restriction is this Business
    Activity's own application-layer scope decision, not a schema fact.
    """

    __tablename__ = "unclassified_intelligence_registry"
    __table_args__ = (
        CheckConstraint(
            "extraction_method IN ("
            "'OCR', 'NLP_PARSE', 'TABLE_EXTRACT', 'ENTITY_EXTRACT', "
            "'SEMANTIC_PARSE', 'MANUAL_ENTRY', 'API_INGEST'"
            ")",
            name="ck_unclassified_intelligence_registry_extraction_method",
        ),
        CheckConstraint(
            "resolution_status IN ("
            "'PENDING', 'MAPPED_TO_EXISTING', 'NEW_CDE_CREATED', "
            "'DISCARDED', 'PROMOTED_CONVERGENCE'"
            ")",
            name="ck_unclassified_intelligence_registry_resolution_status",
        ),
    )

    unclassified_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    organization_id: Mapped[uuid.UUID] = mapped_column(nullable=False, index=True)
    """AMD-001. Logical, not physical, FK to organization_master — see module docstring."""

    raw_extracted_value: Mapped[str] = mapped_column(Text, nullable=False)
    source_document_reference: Mapped[str] = mapped_column(Text, nullable=False)
    source_page_section: Mapped[str | None] = mapped_column(String(500), nullable=True)
    extraction_method: Mapped[str] = mapped_column(String(100), nullable=False)

    llm_label_suggestion: Mapped[str | None] = mapped_column(String(255), nullable=True)
    llm_confidence_score: Mapped[Decimal | None] = mapped_column(Numeric(4, 3), nullable=True)
    probable_domain: Mapped[str | None] = mapped_column(String(100), nullable=True)
    probable_bq_id: Mapped[str | None] = mapped_column(String(50), nullable=True)

    resolution_status: Mapped[str] = mapped_column(
        String(30), nullable=False, default="PENDING", server_default="PENDING"
    )
    resolved_by_user_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    """AMD-005 logical FK to `user_registry` — no physical model anywhere in this repository."""
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    resolved_metric_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    """AMD-005 logical FK to `metric_registry` — no physical model anywhere in this repository."""
    resolved_customer_metric_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    """AMD-005 logical FK to `customer_metric_registry` — no physical model anywhere in this repository."""

    convergence_signal_raised_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="0")
    active_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="1")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )
