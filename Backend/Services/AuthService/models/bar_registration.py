import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from models.database import Base

# D2 (`ROD-ENTERPRISE-BAR-Decision-Preparation.md §0b`): registration state is
# a two-state minimum (registered / not-registered), never `IMP-001
# §6.22.9`'s own six-state lifecycle. A row in this table always means
# "Registered" — there is no "not registered" row to represent, since a
# Business Activity that is not registered simply has no row here at all
# (mirroring `CBOR-INDEX.md`'s own "absence = not registered" convention,
# re-confirmed at `BAR-INDEX.md §3`/§4 for the Business Activity case).
# The literal, single legal value is declared as a CHECK constraint rather
# than an open-ended status column, so the schema itself cannot silently
# grow into the broader lifecycle D2/D6 already excluded.
REGISTRATION_STATUS_REGISTERED = "REGISTERED"


class BarRegistration(Base):
    """
    Enterprise BAR — WP-23 Workstream C, canonical Business Activity
    registration mechanism.

    Governance baseline (re-confirmed, not reopened):
      * D2 — the four LOCKED-minimum BAR responsibilities (cataloguing/
        registration, canonical identity, execution-time gate, discovery)
        bound this table's own column set; no broader `IMP-001 §6.22`
        attribute schema, validation checklist, or lifecycle is imported.
      * D5 — BAR is the canonical Business Activity Identifier authority;
        `identifier` here is a foreign key into the Workstream B ledger
        (`bar_identifier_ledger.identifier`), never independently minted —
        a Business Activity can only be registered with an identifier BAR
        itself has already issued, enforced by this table's own FK, not
        merely by application discipline.
      * D7 — BAR keeps its own registration record, separate from
        `WPR-001` and `CBOR-INDEX.md`.
      * RD-23-03 (layered authority model,
        `ROD-WP-23-AC-BAR-Registry-Authority-Decision-Preparation.md §0`):
        the registering act is the governance authority for a
        registration; this table is the execution-time runtime record
        that BAR logic consults ("is this Business Activity currently
        registered for execution?"); `BAR-INDEX.md` is the human
        governance catalogue. A row here does not, by itself, establish
        that the governance authorization exists — `registering_act` is a
        citation, not a verified link — and reconciliation between the
        governance record and this runtime record is required.
        `owning_capability`/`owning_work_package` are opaque reference
        strings only (no FK into any capability/WP table — neither exists
        as a database object; `CAP-001` and `WPR-001` are governance
        documents, per D7's own explicit "linked, not merged" boundary).

    Mandatory fields, exactly the eight already approved in
    `ENTERPRISE-BAR-MECHANISM-DESIGN-AND-IMPLEMENTATION-READINESS.md §4`
    / `BAR-INDEX.md §3` — no field is added or renamed here:
        Identifier, Reference, Owning Capability, Owning Work Package,
        Registration Status, Registering Act, Registration Date,
        Retroactive flag.

    `[IMPLEMENTATION DESIGN — not constitutional text]` decisions made by
    this table, disclosed rather than silently assumed:
      * Duplicate-registration protection is a UNIQUE constraint on
        `(owning_work_package, business_activity_reference)` — no source
        specifies a duplicate-detection key; this reuses two already-
        approved fields rather than inventing a new identity scheme
        (`ROD-ENTERPRISE-BAR §D5`'s own instruction not to invent
        identifier semantics beyond what governance already fixed, applied
        here by extension to the duplicate-key question, which no source
        settles either). This is a real database constraint, not an
        application-side "check then insert" — the constraint itself is
        the backstop; the service layer's own pre-check is a
        friendlier-error convenience only.
      * `registering_act` is a free-text governance-act citation (e.g. an
        ADR/ROD/WP reference), mirroring `CBOR-INDEX.md §3`'s own
        "Registering ADR" column, generalized per `ROD-ENTERPRISE-BAR
        §D5.7`'s own finding that BAR's registering act need not literally
        be an ADR. Never validated against a fixed enum — this table does
        not know, and does not need to know, what kinds of governance acts
        exist.
    """

    __tablename__ = "bar_registration"
    __table_args__ = (
        CheckConstraint(
            f"registration_status = '{REGISTRATION_STATUS_REGISTERED}'",
            name="ck_bar_registration_status",
        ),
        UniqueConstraint(
            "owning_work_package",
            "business_activity_reference",
            name="uq_bar_registration_wp_reference",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    """Record identity, internal handle only — never the Business Activity Identifier itself."""

    identifier: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("bar_identifier_ledger.identifier"),
        nullable=False,
        unique=True,
    )
    """
    The canonical `BA-NNNNNN` identifier this registration claims (D5).
    Foreign-keyed to `bar_identifier_ledger.identifier` — a registration
    can only ever exist for an identifier BAR itself has issued;
    `unique=True` additionally guarantees no two registrations ever share
    one identifier.
    """

    business_activity_reference: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    """
    Informal, human-readable Business Activity name/description
    (`[IMPLEMENTATION DESIGN]`, `ENTERPRISE-BAR-MECHANISM-DESIGN...md §4`).
    No standalone uniqueness invariant — uniqueness is scoped to
    `(owning_work_package, business_activity_reference)` together, per
    this table's own `uq_bar_registration_wp_reference` constraint.
    """

    owning_capability: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    """Opaque `C-XXX` reference for traceability to `CAP-001`. Not a foreign key — `CAP-001` is a governance document, not a database table."""

    owning_work_package: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    """Opaque `WP-NN` reference linking to (never merging with) `WPR-001`, per D7. Not a foreign key — `WPR-001` is a governance document."""

    registration_status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=REGISTRATION_STATUS_REGISTERED,
        server_default=REGISTRATION_STATUS_REGISTERED,
    )
    """Always `'REGISTERED'` (D2's own two-state minimum — the only state a persisted row can represent; "not registered" is the absence of a row)."""

    registering_act: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    """Free-text citation of the governance act that authorized this registration (e.g. an ADR/ROD/WP reference)."""

    registered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    """System-assigned registration timestamp — never caller-supplied."""

    is_retroactive: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )
    """True if this row entered via D3's own backfill population; False if prospectively registered. Caller-supplied, per `ENTERPRISE-BAR-MECHANISM-DESIGN...md §4`."""
