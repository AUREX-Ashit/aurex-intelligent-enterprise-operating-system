import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.database import Base

if TYPE_CHECKING:  # pragma: no cover
    pass


# `COM-001-021` — the Product ↔ Service classification axis. `ROD-C021` D4
# scopes BA-01 to this axis only; the Digital / Physical secondary typology
# of `COM-001-021` is excluded (`TDS-C021 §3`). Closed set, enforced here and
# in the `ck_c021_offering_definition_kind` CHECK.
OFFERING_KINDS = ("PRODUCT", "SERVICE")

# `COM-001-020` — the offering-state model. `ROD-C021` D7 / `TDS-C021 §9.4`:
# BA-01 establishes and only ever writes `draft`; `published` / `retired` and
# every transition between states are a future C-021 increment. The full
# closed set is declared for schema correctness even though BA-01 writes a
# subset — mirroring `c023_entitlement_context` (declares ACTIVE/SUSPENDED/
# REVOKED, writes only ACTIVE) and `c132_notification`.
OFFERING_STATES = ("draft", "published", "retired")

# `COM-001-001` Universal Identity prefix for the Offering Definition Business
# Object (`ADR-037` CBOR registration). Single source of truth for both
# `OfferingDefinitionService` (formats new references) and
# `C021OfferingDefinitionRepository` (derives the fixed offset at which the
# numeric suffix starts, `Gate 5 remediation` — see the repository's own
# `max_reference_sequence` docstring).
OFFERING_REFERENCE_PREFIX = "OFFERING"


class C021OfferingDefinition(Base):
    """
    Authoritative Offering Definition — the enterprise's single, continuously
    authoritative definition of one standalone Atomic Offering (C-021 Product
    & Service Catalog, WP-20 BA-01, "Establish / Manage Offering Definition").

    Governing design: `TDS-C021 §9` (schema-shape STOP-and-report, performed
    at the conceptual level after the Repository Owner selected `AuthService`
    as the host, `TDS-C021 §5`) and the WP-20 BA-01 charter. Realizes the
    `COM-001 §6` (`COM-001-020`…`-026`) canonical Offering Definition model at
    the data layer only, for the minimum first increment — establish / list /
    read of a `draft` Atomic Offering Definition.

    Platform-global (`ROD-C021` D8 — `[RO DECISION]`): there is NO
    `organization_id` column. The C-021 catalog is one enterprise-wide
    catalog; the authority boundary is platform-administrative
    (`require_platform_admin`), not tenant isolation — mirroring the
    certified `C-003` Roles precedent (`roles` has no `organization_id`,
    `/roles` is tenant-middleware-exempt).

    Excluded from BA-01 (`ROD-C021` D3/D5/D6/D7/D8, `TDS-C021 §3`/`§9.10`):
    composition, offering relationships, publication, retirement, any state
    transition, pricing computation / rating / discounting, availability,
    Subscription (C-020), Customer / Account (C-022), Entitlement / Feature
    Catalog (C-023 — Decision 3 untouched and not fired), Billing (C-024),
    Contract (C-025), tenant overlays, taxonomy governance authority.

    `offering_reference` is the `COM-001-001` Universal Identity
    (`PREFIX-NNNNNN`) AND the stable Offering Reference downstream commercial
    capabilities (C-020 / C-024 / C-025) consume by identity. It is
    system-assigned, monotonic, unique, and concurrency-safe
    (`[RO DECISION]` O1); the concrete allocation mechanism is left to
    implementation — see `OfferingDefinitionService._next_offering_reference`.
    A PostgreSQL SEQUENCE is NOT mandated (`[RO DECISION]` O1).

    `category_ref` is an OPTIONAL / NULLABLE, opaque, non-authoritative
    reference (`[RO DECISION]` O2) — no taxonomy authority, category
    management, `c021_category` table, or FK is created. `list_price_reference`
    is an optional opaque `String` reference only (`ROD-C021` D6) — never a
    numeric / computed price field, never rated or discounted.

    `version` and `supersedes_id` are declared for the future Version
    Management increment (`COM-001-025`) so it needs no `ALTER`; BA-01 never
    writes a non-default value (`version` always 1, `supersedes_id` always
    NULL).
    """

    __tablename__ = "c021_offering_definition"
    __table_args__ = (
        CheckConstraint(
            "offering_kind IN ('PRODUCT', 'SERVICE')",
            name="ck_c021_offering_definition_kind",
        ),
        CheckConstraint(
            "state IN ('draft', 'published', 'retired')",
            name="ck_c021_offering_definition_state",
        ),
        # Supports the list view's state filter (`GET /offerings`). A
        # disclosed implementation-time index choice (`TDS-C021 §9.6`).
        Index("ix_c021_offering_definition_state", "state"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    """Record identity, internal handle, and audit correlation id (`TDS-C021 §9.3`)."""

    offering_reference: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        unique=True,
        index=True,
    )
    """
    `COM-001-001` Universal Identity (`PREFIX-NNNNNN`) and the stable Offering
    Reference (`ERB-C021-06`). System-assigned, monotonic, unique,
    concurrency-safe (`[RO DECISION]` O1). Never caller-supplied.
    """

    offering_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    """Canonical name (`ROD-C021` D4). No uniqueness invariant (`TDS-C021 §9.5`)."""

    offering_kind: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    """`PRODUCT` or `SERVICE` (`COM-001-021` Product↔Service axis; `TDS-C021 §9.1`)."""

    category_ref: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    """
    OPTIONAL / NULLABLE opaque category reference (`[RO DECISION]` O2,
    `COM-001-024`). Free-text, non-authoritative — not a FK, no taxonomy
    table, no category management. When supplied it must be non-empty
    (validated in the request schema). Mirrors
    `c023_entitlement_context.entitlement_source_reference`'s nullable,
    free-text, non-authoritative precedent.
    """

    list_price_reference: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    """
    Optional opaque list-price reference (`ROD-C021` D6). The `String` type is
    deliberate — this is a REFERENCE attribute only; C-021 never computes,
    rates, discounts, or executes a price. Never a Numeric/Decimal column.
    """

    state: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="draft",
    )
    """`COM-001-020` offering state. BA-01 establishes and only ever writes `draft` (`ROD-C021` D7)."""

    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
        server_default="1",
    )
    """`COM-001-025` Version Management. Declared for the future increment; BA-01 always writes 1."""

    supersedes_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("c021_offering_definition.id"),
        nullable=True,
    )
    """`COM-001-025` Historical Definition / lineage link. Declared for the future increment; BA-01 always NULL."""

    created_by_actor_id: Mapped[uuid.UUID] = mapped_column(
        nullable=False,
    )
    """
    Point-in-time audit citation of the `PLATFORM_ADMIN` caller's `person_id`
    (`TDS-C021 §9.1`). NOT a foreign key — mirrors
    `c023_entitlement_context.committed_by_actor_id`.
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

    # Relationship: the version this row supersedes (derived inverse only).
    supersedes: Mapped["C021OfferingDefinition | None"] = relationship(
        "C021OfferingDefinition",
        remote_side=[id],
        foreign_keys=[supersedes_id],
        backref="superseded_by_one",
    )
