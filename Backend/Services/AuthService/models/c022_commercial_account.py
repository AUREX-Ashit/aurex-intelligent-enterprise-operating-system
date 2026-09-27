import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.database import Base

if TYPE_CHECKING:  # pragma: no cover
    pass


# `COM-001-033` Account status. `ROD-C022-A` D8 / `TDS-C022 §9`: BA-01
# establishes and only ever writes `active`; suspend/retire/reactivate are a
# future C-022 increment. The full closed set is declared for schema
# correctness even though BA-01 writes a subset — mirroring
# `c021_offering_definition.state` / `c023_entitlement_context`.
ACCOUNT_STATUSES = ("active", "suspended", "retired")

# `COM-001-001` Universal Identity prefix for the Commercial Account Business
# Object (`ADR-040` CBOR registration `CAC-000001`). The `PREFIX-NNNNNN` shape
# is mandated by `COM-001-001` (inherited in full by Section 7, `TDS-C022 §7`
# post-`[C-3]`-remediation); the exact token is a spelled-out word, mirroring
# `OFFERING_REFERENCE_PREFIX = "OFFERING"`'s own precedent rather than the
# short CBOR code. Single source of truth for both `CommercialAccountService`
# (formats new references) and `C022CommercialAccountRepository` (derives the
# fixed offset at which the numeric suffix starts).
ACCOUNT_REFERENCE_PREFIX = "ACCOUNT"


class C022CommercialAccount(Base):
    """
    Authoritative Commercial Account Context — the enterprise's single,
    continuously authoritative commercial-container fact for one Commercial
    Account (C-022 Customer & Account Management, WP-21 BA-01, "Establish
    Commercial Account").

    Governing design: `TDS-C022 §6` (schema-shape STOP-and-report, conceptual
    level, `AuthService`-hosted per `ROD-C022` D3) and the WP-21 BA-01
    charter. Realizes `COM-001 §7` (`COM-001-030`…`-036`) at the data layer
    only, for the minimum first increment — establish of exactly one
    standalone Commercial Account.

    Platform-global (`ROD-C022` D2 — `[RO DECISION]`): there is NO
    `organization_id` column. The authority boundary is
    `require_platform_admin`, mirroring the certified `/roles`/`/offerings`
    precedent.

    **No `classification` column** (`ADR-038`, Option A; `ROD-C022-A` D7).
    `COM-001-033` governs Account as written — identity, hierarchy position,
    and status only. The `COM-001-033` ↔ `PE-001-C022` conflict `ADR-038`
    identified remains a separate, later architecture-governance item, not
    resolved by this model.

    Excluded from BA-01 (`ROD-C022 §H`, `ROD-C022-A` D8): Customer
    establishment, the Customer–Account Relationship, reclassification,
    retirement/reactivation, merge/split/transfer, Subscription (C-020),
    Billing (C-024), Contract (C-025), Entitlement (C-023), Organization
    (C-004) equivalence, tenant isolation, Identity/Person wiring, read/list
    of any established Commercial Account.

    `account_reference` is the `COM-001-001` Universal Identity
    (`PREFIX-NNNNNN`) and the stable Account Reference `COM-001-036` names as
    consumable by downstream capabilities. It is system-assigned, monotonic,
    unique, and concurrency-safe, mirroring `offering_reference`'s own O1
    acceptance properties — see
    `CommercialAccountService._next_account_reference`.

    `parent_account_id` is `COM-001-033`'s own "Account-to-Account hierarchy
    position" fact, glossed by `PE-001-C022 §1.16` as "(parent Account
    reference, where applicable)". Declared here so a future structural
    increment (`ERB-C022-04`) needs no `ALTER`; BA-01 establishes exactly one
    standalone account with no counterparty, so every BA-01-established row
    has `parent_account_id = NULL` (`TDS-C022 §10`, `ROD-C022-B` D9 — single-
    call establish accepted; this column is not part of any observable
    lifecycle stage BA-01 exercises).

    Single-call establish realization of `COM-001-002`/`COM-001-003`'s
    Anchor/Intent/Proposed/Assessment lifecycle pattern is accepted for BA-01
    per `ROD-C022-B` D9 (Option A) — Anchor, Intent, Proposed, and Assessment
    remain conceptually distinct architectural roles; this table stores only
    the resulting Authoritative Commercial Account Context, exactly as
    `c021_offering_definition` stores only the resulting Authoritative
    Offering Definition Context for its own certified single-call precedent.
    """

    __tablename__ = "c022_commercial_account"
    __table_args__ = (
        CheckConstraint(
            "status IN ('active', 'suspended', 'retired')",
            name="ck_c022_commercial_account_status",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    """Record identity, internal handle, and audit correlation id (`TDS-C022 §6.1`)."""

    account_reference: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        unique=True,
        index=True,
    )
    """
    `COM-001-001` Universal Identity (`PREFIX-NNNNNN`) and the stable Account
    Reference (`COM-001-036`). System-assigned, monotonic, unique,
    concurrency-safe. Never caller-supplied.
    """

    account_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    """Minimum canonical identity (`COM-001-033`: "its own identity"). No uniqueness invariant (`TDS-C022 §6.1`)."""

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="active",
    )
    """`COM-001-033` Account status. BA-01 establishes and only ever writes `active` (`ROD-C022-A` D8)."""

    parent_account_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("c022_commercial_account.id"),
        nullable=True,
    )
    """`COM-001-033`'s Account-to-Account hierarchy position. Declared for a future increment; BA-01 always writes NULL."""

    created_by_actor_id: Mapped[uuid.UUID] = mapped_column(
        nullable=False,
    )
    """
    Point-in-time audit citation of the `PLATFORM_ADMIN` caller's `person_id`
    (`TDS-C022 §6.1`). NOT a foreign key — mirrors
    `c021_offering_definition.created_by_actor_id`.
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

    # Relationship: the parent Account this row's hierarchy position refers
    # to (derived inverse only). Declared, never populated by BA-01.
    parent_account: Mapped["C022CommercialAccount | None"] = relationship(
        "C022CommercialAccount",
        remote_side=[id],
        foreign_keys=[parent_account_id],
        backref="child_accounts",
    )
