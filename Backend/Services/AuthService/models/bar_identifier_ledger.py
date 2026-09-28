import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from models.database import Base

# `SD-002-004` Universal Identity prefix for the Business Activity
# namespace — not invented: the same prefix appears as the illustrative
# worked example (`BA-000089`) in `SD-002-004`, `CMD-001 §26.4a`, and
# `IMP-001 §6.22.1b`. Adopting `BA` as the actual prefix is the lowest-
# invention reading of that already-telegraphed convention
# (`ENTERPRISE-BAR-MECHANISM-DESIGN-AND-IMPLEMENTATION-READINESS.md §5`).
# `[IMPLEMENTATION DESIGN]` — this constant and the `PREFIX-NNNNNN` shape
# it participates in are an engineering choice, not constitutional text.
BAR_IDENTIFIER_PREFIX = "BA"


class BarIdentifierLedger(Base):
    """
    Enterprise BAR — WP-23 Workstream B, Business Activity Identifier
    issuance ledger.

    D5 (`ROD-ENTERPRISE-BAR-Decision-Preparation.md §0d`): BAR is the
    canonical Business Activity Identifier authority; the identifier is
    assigned at BAR registration, never earlier. This table is that
    issuing authority's own persistence: every row is one issued
    `BA-NNNNNN` value, inserted atomically (UNIQUE constraint backstop,
    allocate-and-retry on collision — the same application-level
    monotonic-allocator pattern already certified for
    `c021_offering_definition.offering_reference`, `[RO DECISION]` O1,
    reused here as the established repository convention rather than
    inventing a new one).

    Deliberately NOT a Business Activity registration table (Workstream C,
    not yet built) — per the approved design's own explicit separation
    (`ENTERPRISE-BAR-MECHANISM-DESIGN-AND-IMPLEMENTATION-READINESS.md
    §19a.6`): "issuance is an internal capability of the registration
    mechanism, not an independent registration event." This table carries
    no Business Activity name, capability, Work Package, or registration-
    status field — only the fact that an identifier was issued, and when.
    A future Workstream C will consume this ledger (via
    `BarIdentifierService.issue_identifier`) as one step inside its own
    fuller registration transaction; it does not duplicate this table's
    own responsibility.

    Does not import any part of `IMP-001 §6.22`'s broader attribute
    schema, status lifecycle, version/dependency management, or
    governance-workflow metadata (D2/D6) — exactly the four LOCKED-minimum
    responsibilities decided by D2, and no more.
    """

    __tablename__ = "bar_identifier_ledger"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    """Record identity, internal handle only — never the Business Activity Identifier itself."""

    identifier: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True,
        index=True,
    )
    """
    The canonical, permanent `BA-NNNNNN` value (`SD-002-004`, D5).
    System-assigned by `BarIdentifierService`; never caller-supplied.
    Never reused once issued, mirroring `SD-002-004`'s own "globally
    unique, permanent identifier" requirement.
    """

    issued_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    """Governance/audit traceability — when this identifier was issued."""
