# models/knowledge_graph.py
"""
WP-14 BA-05 — Synchronize Enterprise Knowledge Graph (C-092 Knowledge Graph
Management). Canonical, LOCKED physical schema per `Master_Technical_
Architecture.md` AMD-012 (`enterprise_knowledge_graph_registry`, line 3170)
and AMD-016 (the `organization_id` tenant-boundary amendment, line 3214) —
no column added, removed, or retyped beyond what AMD-012/AMD-016 together
specify. Hosting-service determination: `AIService`, per `RO-DEC-WP14-
BA05-03` (`TDS-013 §20`/`§26a`; independently recorded in
`WP-14_BA-04_Establish_Knowledge_Asset_Business_Activity_Charter.md`,
"BA-05 — Repository Owner Decision Recording").

`organization_id` is a plain, nullable UUID column, not a database-level
`ForeignKey` to `organization_master` — that table lives in `AuthService`'s
own database, a separate service boundary (`CLAUDE.md §8`). The FK AMD-016
documents is a logical reference, enforced entirely by application-layer
BR-1–BR-4 derivation (`TDS-013 §9`–`§13`), mirroring the identical,
already-shipped precedent `models/search.py`'s own `vector_index_registry.
organization_id` column establishes (nullable = platform-wide/Global, per
BR-3, not merely optional).

`confidence_rule_id` (→ `confidence_scoring_registry`, AMD-003) is declared
as a plain nullable column, no FK — that table is LOCKED at the
architecture-document level only, with no physical Backend model anywhere
in this repository, mirroring the identical precedent `models/knowledge_
asset.py`'s own `confidence_rule_id` column already establishes. Neither
table is created by this change.

`graph_engine_reference`, `relationship_weight`, `confidence_score`, and
`explainability_reference` are never populated by BA-05's own minimum
scope (`RO-DEC-WP14-BA05-02`) — no confidence-scoring or live-Neo4j input
exists at this trigger. Left `NULL`, not invented (`TDS-013 §1`/§8 step 7).

No `CREATE POLICY`/RLS is created by this migration — consistent with
every other AMD-012 sibling table's own migration in this service (index
on `organization_id` only; RLS remains a documented, architecture-level
policy — AMD-016's own text — not yet physically enforced by any AIService
migration in this repository, `discovery_provider_registry`/`knowledge_
asset_registry` included). Tenant isolation for BA-05's own write path is
enforced at the application/service layer (`RelationshipResolutionService`,
`TDS-013 §22` layer 1) — the two-layer design's own database/RLS layer
remains a disclosed, repository-wide infrastructure-maturity gap, not a
BA-05-specific omission.
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from models.database import Base


class EnterpriseKnowledgeGraphRegistryModel(Base):
    """
    `enterprise_knowledge_graph_registry` (AMD-012/AMD-016). The Postgres-
    side relational index and RLS-governed audit trail of the Enterprise
    Knowledge Graph (`RTA-001 §12`) — not the primary graph store (Neo4j
    Aura, out of scope here; `graph_engine_reference` always `NULL`).
    WP-14 BA-05 (Synchronize Enterprise Knowledge Graph) writes this table.
    """

    __tablename__ = "enterprise_knowledge_graph_registry"

    knowledge_graph_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    source_entity_type: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source_entity_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    relationship_type: Mapped[str | None] = mapped_column(String(255), nullable=True)
    """`RTA-001 §12.9`'s own closed 12-value vocabulary — membership validated at the application layer (Ontology Validation, `TDS-013 §16`/`services/relationship_resolution_service.py`), not a database CHECK constraint (AMD-012's own LOCKED schema declares none, unlike `knowledge_asset_registry.curation_status`)."""
    target_entity_type: Mapped[str | None] = mapped_column(String(255), nullable=True)
    target_entity_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True)

    relationship_weight: Mapped[str | None] = mapped_column(String(255), nullable=True)
    confidence_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    explainability_reference: Mapped[str | None] = mapped_column(String(255), nullable=True)

    active_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="0")
    """AMD-012's own LOCKED schema text states DEFAULT FALSE for this table specifically — preserved verbatim, not altered. No business rule anywhere in `TDS-013` states a newly-synchronized relationship should be `active_flag=True`; not overridden at insert."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    confidence_rule_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    """AMD-003. confidence_scoring_registry is unimplemented anywhere in this repository — no FK, logical or physical; not required by BA-05's own minimum scope."""

    graph_engine_reference: Mapped[str | None] = mapped_column(String(255), nullable=True)
    """Always NULL from BA-05 — the live Neo4j Aura write is out of scope (`TDS-013 §1`, `SE-025`)."""

    organization_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True, index=True)
    """AMD-016. Nullable: NULL = platform/global relationship (BR-3), non-NULL = organization-scoped (BR-1/BR-2) — never independently asserted, always derived per `TDS-013 §9`–`§13`. Logical, not physical, FK to organization_master — see module docstring."""
