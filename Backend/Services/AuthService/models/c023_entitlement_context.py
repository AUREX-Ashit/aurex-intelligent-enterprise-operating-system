import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    String,
    UUID as SA_UUID,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.database import Base

if TYPE_CHECKING:
    from models.organization import Organization
    from models.domain import Domain
    from models.approval_authority import ApprovalAuthority


# The fixed all-zeros UUID used as the COALESCE sentinel for the
# `domain_id`-NULL case of `ux_c023_entitlement_context_current`
# (Repository Owner D-4). `uuid.uuid4()` never produces this value, and no
# Business Activity establishes a Domain with it, so it is safe as a
# "no domain" stand-in that a plain multi-column unique index cannot
# express (PostgreSQL treats each NULL as distinct). Documented here and in
# the Alembic migration, per the Repository Owner's D-4 condition.
DOMAIN_ID_NULL_SENTINEL = "00000000-0000-0000-0000-000000000000"

# Identical SQL text on PostgreSQL and on the SQLite test harness
# (`TDS-C023-A §13` — "expressed identically on both dialects"):
#   - PostgreSQL: `domain_id` is `uuid`; the string literal is implicitly
#     cast to `uuid` inside COALESCE (its other argument is `uuid`), so no
#     explicit `::uuid` cast is needed and the expression is dialect-neutral.
#   - SQLite: `domain_id` round-trips as a hex string; COALESCE returns
#     either that value or the 36-char dashed sentinel — always distinct.
_CURRENT_ENTITLEMENT_UNIQUE_EXPR = f"COALESCE(domain_id, '{DOMAIN_ID_NULL_SENTINEL}')"


class C023EntitlementContext(Base):
    """
    Authoritative Entitlement Context — the current, single, canonical
    Entitlement fact for one Entitlement Anchor (Organization, optionally
    Domain-scoped) and entitlement type (C-023 Licensing & Entitlement,
    WP-17 BA-01).

    Governing design: `TDS-C023-A §3.2` (approved by the Repository Owner
    at `TDS-C023-A §19.1`). Realizes the Organization-anchored half of the
    Master Technical Architecture's canonical `entitlement_registry` (MTA
    lines 1622-1635), which is "explicitly separate from license_registry"
    (MTA line 1622-1625; `URA-001-112`/`-148`; `BR-C023-03`). Neither this
    table nor `c023_license_context` can hold the other's construct —
    License↔Entitlement independence is structural, not conventional
    (`TDS-C023-A §5`).

    `entitlement_type_ref` is a reference to an ALREADY-RECOGNIZED
    Entitlement Type identifier only. BA-01 does NOT create, modify, or
    govern a global Entitlement Type or a catalog — Decision 3
    (`IRA-C023 §21.12`) is deferred and not reopened (`TDS-C023-A §9.3`).
    No `granted_capacity` / consumption column exists — Decision 4
    (`IRA-C023 §22.13`) is deferred (`TDS-C023-A §3.3`).

    BA-01 only ever writes `status = 'ACTIVE'` and never closes a context
    (`TDS-C023-A §9.1`; Repository Owner D-5).
    """

    __tablename__ = "c023_entitlement_context"
    __table_args__ = (
        CheckConstraint(
            "status IN ('ACTIVE', 'SUSPENDED', 'REVOKED')",
            name="ck_c023_entitlement_context_status",
        ),
        # Non-unique lookup index (`TDS-C023-A §3.2` Indexes list).
        Index(
            "ix_c023_entitlement_context_org_type",
            "organization_id",
            "entitlement_type_ref",
        ),
        # INV-C023-09 (`TDS-C023 §15`): exactly one CURRENT Authoritative
        # Entitlement Context per Entitlement Anchor AND entitlement type.
        # The COALESCE sentinel (Repository Owner D-4) is required because a
        # plain unique index treats NULL `domain_id` as distinct, which
        # would wrongly permit two concurrent organization-wide entitlements
        # of the same type.
        Index(
            "ux_c023_entitlement_context_current",
            "organization_id",
            text(_CURRENT_ENTITLEMENT_UNIQUE_EXPR),
            "entitlement_type_ref",
            unique=True,
            postgresql_where=text("effective_to IS NULL"),
            sqlite_where=text("effective_to IS NULL"),
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    """Record identity and the audit correlation id (`TDS-C023 §16`)."""

    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=False,
        index=True,
    )
    """
    The Entitlement Anchor (`TDS-C023 §11`, `BR-C023-03`). Hard
    intra-service FK to `organizations.id` (Repository Owner D-2),
    mirroring `approval_authority.organization_id -> organizations.id`.
    """

    domain_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("domains.id"),
        nullable=True,
    )
    """Optional Domain scoping (`TDS-C023 §11`). NULL = organization-wide entitlement. FK to `domains.id`, mirroring `approval_authority.domain_id`."""

    entitlement_type_ref: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    """
    An ALREADY-RECOGNIZED Entitlement Type identifier only (`TDS-C023 §5-A`;
    Decision 3 deferred — no type-creation, no catalog write). The
    recognition/lookup mechanism is a separate open item
    (`TDS-C023-A §9.3`); this column stores a REFERENCE, never a DEFINITION.
    """

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    """`ACTIVE` / `SUSPENDED` / `REVOKED`. BA-01 writes only `ACTIVE`."""

    effective_from: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    """Independent Commit-time business date (`URA-001-117`: entitlements are time-bound). Present in the MTA `entitlement_registry` definition already."""

    effective_to: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    """NULL while current. Soft-close only; BA-01 never sets it."""

    entitlement_source_reference: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    """As `c023_license_context` — free-text, non-authoritative (`BR-C023-02`)."""

    approval_authority_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("approval_authorities.id"),
        nullable=False,
        index=True,
    )
    """The `approval_authorities` row that authorized this Commit (Repository Owner D-2 — hard intra-service FK). Recorded for audit; does not participate in resolution."""

    committed_by_actor_id: Mapped[uuid.UUID] = mapped_column(
        SA_UUID(),
        nullable=False,
    )
    """The `person_id` of the committing caller (`TDS-C023 §16`). NOT a foreign key — a point-in-time audit citation (`tenant_registry` precedent)."""

    committed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    organization: Mapped["Organization"] = relationship("Organization", foreign_keys=[organization_id])
    domain: Mapped["Domain | None"] = relationship("Domain", foreign_keys=[domain_id])
    approval_authority: Mapped["ApprovalAuthority"] = relationship(
        "ApprovalAuthority", foreign_keys=[approval_authority_id]
    )
