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
    from models.membership import Membership
    from models.approval_authority import ApprovalAuthority


class C023LicenseContext(Base):
    """
    Authoritative License Context — the current, single, canonical License
    governance-layer fact for one Membership Anchor (C-023 Licensing &
    Entitlement, WP-17 BA-01 — "Establish Entitlement/License Context
    (Administrative)").

    Governing design: `TDS-C023-A §3.1` (the schema shape approved by the
    Repository Owner at `TDS-C023-A §19.1`, D-1 Option A / D-2 hard
    intra-service FKs / D-3 nullable `c023_license_type` / D-5 full
    canonical `status` set / D-6 `c023_`-prefixed name). Realizes the
    Membership-anchored half of the Master Technical Architecture's
    canonical `license_registry` (MTA lines 1615-1619; `URA-001-111`),
    minimally extended with only the lifecycle/authority/audit columns
    `TDS-C023 §5-A`/`§14`/`§16` require.

    Decision 6 (`IRA-C023 §18.13`, Split Ownership) is complied with by
    construction: this table carries NO `FULL`/`LIGHT` value and no foreign
    key to `memberships.license_type`. `c023_license_type` holds the
    disjoint four-value `URA-001-115` specialized set only — never the
    `C-007`-owned base classification, which is read by value at
    establish/resolution time and never persisted here
    (`TDS-C023 §6.3` item 11 — "the single most important design
    constraint"; `TDS-C023-A §4`).

    BA-01 only ever writes `status = 'ACTIVE'` and never closes a context
    (`effective_to` stays NULL) — the `SUSPENDED`/`REVOKED` transitions and
    context soft-close belong to a future, separately-scoped Business
    Activity and are not implemented here (`TDS-C023 §4`; `TDS-C023-A §9.1`;
    Repository Owner D-5 instruction). The full canonical value set is in
    the CHECK so that future BA does not require an `ALTER ... DROP/ADD
    CONSTRAINT`, mirroring `approval_authority.py`'s own `VersionStatus`
    CHECK.
    """

    __tablename__ = "c023_license_context"
    __table_args__ = (
        CheckConstraint(
            "status IN ('ACTIVE', 'SUSPENDED', 'REVOKED')",
            name="ck_c023_license_context_status",
        ),
        CheckConstraint(
            "c023_license_type IS NULL OR "
            "c023_license_type IN ('SUPPLIER', 'AUDITOR', 'BOARD_MEMBER', 'CONSULTANT')",
            name="ck_c023_license_context_license_type",
        ),
        # INV-C023-10 (`TDS-C023 §15`, `PE-001-C023 §1.16`): exactly one
        # CURRENT (`effective_to IS NULL`) Authoritative License Context per
        # Membership Anchor. Partial unique index — the identical pattern
        # `ux_membership_approval_authority_active` (WP-18) and
        # `ux_authority_holders_active_authority` (TDS-017) already use, so
        # the SQLite test harness (`conftest.py`) builds it too.
        Index(
            "ux_c023_license_context_current",
            "membership_id",
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

    membership_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("memberships.id"),
        nullable=False,
        index=True,
    )
    """
    The Membership Anchor (`TDS-C023 §6.3` item 3). Hard intra-service FK
    to `memberships.id` (both tables AuthService-owned, `ADR-036`;
    Repository Owner D-2) — mirroring WP-18's own
    `membership_approval_authority.membership_id -> memberships.id`. The FK
    targets the row identity, NOT the `license_type` classification value.
    """

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    """`ACTIVE` / `SUSPENDED` / `REVOKED` (`PE-001-C023 §5.5`). BA-01 writes only `ACTIVE`."""

    effective_from: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    """Independent Commit-time business date (`TDS-C023 §10.1`) — never derived from any Subscription."""

    effective_to: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    """NULL while this context is the current one. Soft-close only (never hard-deleted); BA-01 never sets it (`TDS-C023-A §9.1`)."""

    entitlement_source_reference: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    """
    Free-text citation of the non-authoritative Entitlement Source
    Reference (Subscription id, Contract id, or `"ADMINISTRATIVE"` for a
    direct grant) — `TDS-C023 §6.2`/`§6.3` item 10, `BR-C023-02`. Never
    itself treated as an authoritative fact.
    """

    approval_authority_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("approval_authorities.id"),
        nullable=False,
        index=True,
    )
    """
    The `approval_authorities` row that authorized this Commit
    (`TDS-C023 §5-A` "Authority reference"). Hard intra-service FK
    (Repository Owner D-2), mirroring
    `membership_approval_authority.approval_authority_id`. Stores a
    pointer for audit/traceability; it does not participate in resolution
    (`resolve_approval_authority()` is consumed as-is — `TDS-C023-A §11`).
    """

    committed_by_actor_id: Mapped[uuid.UUID] = mapped_column(
        SA_UUID(),
        nullable=False,
    )
    """
    The `person_id` of the caller who satisfied the resolved Commit
    Authority (`TDS-C023 §16`). NOT a foreign key — a point-in-time audit
    citation, mirroring `tenant_registry.approved_by_actor_id` /
    `allocated_by_actor_id` (`TDS-016 §11`).
    """

    committed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    """When the Commit occurred."""

    c023_license_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )
    """
    Repository Owner D-3: the four `URA-001-115` specialized C-023 license
    types (`SUPPLIER` / `AUDITOR` / `BOARD_MEMBER` / `CONSULTANT`).
    Nullable. This is NOT a copy of `memberships.license_type` (which is
    `FULL`/`LIGHT` only) and never stores `FULL`/`LIGHT`. Decision 6
    remains unchanged.
    """

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
    membership: Mapped["Membership"] = relationship("Membership", foreign_keys=[membership_id])
    approval_authority: Mapped["ApprovalAuthority"] = relationship(
        "ApprovalAuthority", foreign_keys=[approval_authority_id]
    )
