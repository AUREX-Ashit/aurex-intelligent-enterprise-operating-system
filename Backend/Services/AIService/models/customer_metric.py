# models/customer_metric.py
"""WP-14 BA-03 — Resolve Enterprise Intelligence Candidate (Convergence Decision). Physical schema per `Master_Technical_Architecture.md` — `customer_metric_registry`'s own base definition (line 4263, part of the Custom CDE tables governed by `Complete_Blueprint.md §5.0c` Binding 3 and AMD-004) combined with that same table's own later Binding-3 "rework" (line 5410, adding `cde_tier`/`semantic_match_*`/`convergence_count`/`promotion_*`) AND its own AMD-007 "Hide/Purge governance columns" rework (line 5541, adding `is_hidden_flag`/`is_purged_flag`/`purge_*`) — all three DDL blocks read directly and combined here (corrected per the Gate 1 independent certification's own Finding 4, which found the model had combined only the first two); no column added, removed, or retyped beyond what those three LOCKED blocks together specify. `purge_audit_log` (the separate table AMD-007 also introduces, line 5551) is a distinct table this Business Activity does not write to and is not created here — Hide/Purge are entirely future, unchartered actions no WP-14 Business Activity performs; only `customer_metric_registry`'s own passive columns are added for schema completeness, per the same "verbatim" fidelity requirement already applied to the other two blocks. `ck_customer_metric_registry_semantic_match_score` (`CHECK (semantic_match_score BETWEEN 0 AND 1)`, Master_Technical_Architecture.md:5418-5419) was added in Gate 2 V&V remediation (Finding 3) — the Binding-3 rework block's own `semantic_match_score` `CHECK` was previously omitted from this model despite the rest of that block being represented; written verbatim from the LOCKED DDL text, with no added `IS NULL OR` guard, since a bare `CHECK` already passes a `NULL` value under standard SQL semantics (both Postgres and SQLite) — preserving this column's own "NULL, never populated" disposition in this implementation without inventing stricter text than the LOCKED DDL states.

`organization_id` is a plain, non-nullable UUID column, not a
database-level `ForeignKey` to `organization_master` — mirroring every
other AIService model's own identical precedent (`CLAUDE.md §8`, separate
service boundary). RLS policy is unqualified (`organization_id =
current_setting(...)`, `Master_Technical_Architecture.md:4289-4291`) —
strictly tenant-scoped, no platform-wide sharing, the same shape BA-02's
own table already uses.

`requested_by_user_id`/`approved_by_user_id`/`promotion_requested_by`/
`promotion_decided_by` carry no FK, logical or physical — `user_registry`
does not exist under that name
anywhere in this repository's actual implementation (this repo's real
canonical actor model is Person/Identity per `CLAUDE.md §6`); BA-03
populates this column with the caller's own JWT `person_id` claim, the
same actor-identity resolution every prior WP-14 Business Activity already
uses, not a new interpretation invented here.

`semantic_match_result_metric_id` is a logical FK to `metric_registry`
specifically — its own `COMMENT ON COLUMN` (`Master_Technical_
Architecture.md:5433-5437`) states verbatim: "The **Global** CDE the
semantic engine believes this Tenant CDE duplicates." `metric_registry`
has zero physical rows and no physical Backend model anywhere in this
repository (the "2356 locked CIL CDEs" it should contain do not exist as
data), so this column is always `NULL` in this implementation — an
honest rendering of its own documented "NULL if no match found"
semantics, since a Global match can never actually occur here (corrected
per the Gate 1 independent certification's own Finding 2, which found an
earlier version of this code wrote a Tenant `customer_metric_id` into
this Global-reserved column — a column-semantics violation, not merely
an unvalidatable reference). The same-organization Tenant-CDE duplicate
heuristic (`TD-145`) still runs and is still surfaced to the caller, but
only via the resolve response's own `same_organization_duplicate_
customer_metric_id` field — never persisted into this LOCKED,
Global-only column, since the schema provides no column for a Tenant-CDE
match record. See `services/intelligence_candidate_resolution_service.py`
for the full disclosure.

`customer_domain_id` remains unpopulated (always `NULL`) — no document
governing BA-03 names a customer-domain input, and building
`customer_domain_registry` support would be new, unauthorized scope.

Convergence/promotion columns (`convergence_count`, `promotion_*`) are
declared for schema completeness but never written beyond their own
column defaults by this Business Activity — cross-tenant convergence
matching is explicitly flagged, not resolved, by `IRA-014 §6`/§8 itself
("a genuine Technical Design-phase open item"), and Global promotion is
explicitly "a separate, later, Aurex-Admin-only act... never automatic"
(`IRA-014 §6` Business Rules) — neither is BA-03's own scope.
"""
import uuid
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import Boolean, CheckConstraint, DateTime, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from models.database import Base


class CustomerMetricRegistryModel(Base):
    """
    `customer_metric_registry`. A customer-defined Canonical Data Element,
    tenant-scoped and invisible to every other customer — mirrors
    `metric_registry`'s own column shape (Master_Technical_Architecture.md
    comment, line 4258-4261).

    WP-14 BA-03 (Resolve Enterprise Intelligence Candidate) writes this
    table on the `NEW_CDE_CREATED` resolution path only.
    """

    __tablename__ = "customer_metric_registry"
    __table_args__ = (
        CheckConstraint(
            "approval_status IN ('pending', 'approved', 'rejected')",
            name="ck_customer_metric_registry_approval_status",
        ),
        CheckConstraint(
            "cde_tier IN ('TENANT', 'TEMPORARY')",
            name="ck_customer_metric_registry_cde_tier",
        ),
        CheckConstraint(
            "promotion_decision IS NULL OR promotion_decision IN ('PENDING', 'APPROVED', 'REJECTED')",
            name="ck_customer_metric_registry_promotion_decision",
        ),
        CheckConstraint(
            "semantic_match_score BETWEEN 0 AND 1",
            name="ck_customer_metric_registry_semantic_match_score",
        ),
        UniqueConstraint("organization_id", "metric_code", name="uq_customer_metric_registry_org_code"),
    )

    customer_metric_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(nullable=False, index=True)
    """AMD-001. Logical, not physical, FK to organization_master — see module docstring."""

    customer_domain_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    """Never populated by BA-03 — see module docstring."""

    metric_name: Mapped[str] = mapped_column(String(255), nullable=False)
    metric_code: Mapped[str] = mapped_column(String(100), nullable=False)
    metric_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    unit_of_measure: Mapped[str | None] = mapped_column(String(50), nullable=True)
    formula_logic: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_type: Mapped[str | None] = mapped_column(String(50), nullable=True)

    requested_by_user_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    """NOT NULL per the LOCKED schema. Logical only, no FK — always populated with the caller's own JWT person_id claim; see module docstring."""
    approval_status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending", server_default="pending")
    approved_by_user_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    evidence_required_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="1")
    ai_extractable_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="0")
    active_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="1")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    cde_tier: Mapped[str] = mapped_column(String(20), nullable=False, default="TENANT", server_default="TENANT")
    semantic_match_attempted_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="0")
    semantic_match_result_metric_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    """Logical FK to metric_registry — no physical model anywhere in this repository; see module docstring."""
    semantic_match_score: Mapped[Decimal | None] = mapped_column(nullable=True)
    """NUMERIC(4,3), CHECK (semantic_match_score BETWEEN 0 AND 1) per the LOCKED DDL
    (Master_Technical_Architecture.md:5418-5419) — see ck_customer_metric_registry_semantic_match_score
    in __table_args__ (Gate 2 V&V remediation, Finding 3; missing in the original implementation).
    Always NULL in this implementation — see semantic_match_result_metric_id's own docstring."""
    semantic_match_rejected_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    convergence_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1, server_default="1")
    promotion_requested_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="0")
    promotion_requested_by: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    promotion_requested_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    promotion_decision: Mapped[str | None] = mapped_column(String(20), nullable=True)
    promotion_decided_by: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    promotion_decided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # AMD-007 Hide/Purge governance columns (line 5541) — never written by
    # BA-03 (which only ever inserts new rows); present for schema
    # completeness against the LOCKED definition. Hide/Purge actions
    # themselves are unchartered — no WP-14 Business Activity performs
    # them (Gate 1 Finding 4 remediation).
    is_hidden_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="0")
    hidden_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    is_purged_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="0")
    purge_requested_by: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    purge_requested_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    purge_approved_by: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    purge_approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    purge_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
