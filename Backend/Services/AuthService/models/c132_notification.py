import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    UUID as SA_UUID,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.database import Base

if TYPE_CHECKING:
    from models.membership import Membership


# DS-001 Chapter 21 (Notification Styling, `DS-001-350`) — the closed
# four-value severity taxonomy. Enforced identically here and in the
# `ck_c132_notification_severity` CHECK, mirroring
# `AccessEvaluationOutcome`'s own closed-set discipline. No fifth value
# may be added without a DS-001 amendment (`DS-001` §22.4).
NOTIFICATION_SEVERITIES = ("success", "info", "warning", "danger")

# `TDS-C132 §10` / `§6.6` item 4 — the minimum lifecycle. One-directional;
# no third state (archive/expiry) is designed for BA-01 (`ROD-C132` RO
# Decision 3a — the full `SD-003-226` interruption-ceiling/digest regime is
# deferred, not implemented here).
NOTIFICATION_STATUSES = ("UNREAD", "ACKNOWLEDGED")


class C132Notification(Base):
    """
    Authoritative Notification record — a persisted, tenant-scoped,
    recipient-anchored, in-application notification (C-132 Enterprise
    Notifications, WP-19 BA-01, "Establish / Manage Enterprise Notification
    Context").

    Governing design: `TDS-C132 §6.6` (schema-shape STOP-and-report,
    performed at the conceptual level after the Repository Owner selected
    `AuthService` as the host, `TDS-C132 §6.5` H-1) and the `WP-19` BA-01
    charter. Realizes `SD-003` §8's Notification composition/severity laws
    (`DS-001-350`/`DS-001-351`) at the data layer only — no delivery,
    orchestration, event bus, or cross-service fan-in (`ROD-C132` RO
    Decision 3; `TDS-C132 §3`/`§6.4`). Cross-service triggering is
    explicitly deferred (`TDS-C132 §6.4`, Option 2) — every caller of the
    write path in this first increment is intra-`AuthService`.

    A Notification is NOT an Audit Event, a Domain Event, a Timeline Event,
    or a C-131 comment/mention (`ROD-C132` architectural clarification;
    `TDS-C132 §7`). The `record_audit()` trail on establish/acknowledge is
    separate and unaffected — `SE-051`'s retention floor binds that trail,
    not this row (`TDS-C132 §6.6` item 9).

    Recipient anchor and tenant anchor are one and the same: `membership_id`
    (`Membership` = Person x Organization), reusing
    `AccessEvaluationOutcome.membership_id`'s own precedent — no separate,
    duplicated `organization_id` column (`TDS-C132 §6.6` item 3). Tenant
    isolation is enforced at the service layer via the join through
    `membership_id -> Membership.organization_id` (`CLAUDE.md §21.4`;
    `TDS-C132 §11`), exactly as every prior AuthService Work Package does.

    BA-01 imposes no uniqueness/idempotency invariant — a recipient may
    legitimately receive multiple, distinct notifications from the same
    `source_type`/`source_id` over time (`TDS-C132 §6.6` item 8;
    `IRA-C132 §14`, carried forward).
    """

    __tablename__ = "c132_notification"
    __table_args__ = (
        CheckConstraint(
            "severity IN ('success', 'info', 'warning', 'danger')",
            name="ck_c132_notification_severity",
        ),
        CheckConstraint(
            "status IN ('UNREAD', 'ACKNOWLEDGED')",
            name="ck_c132_notification_status",
        ),
        # Governance-required index — the tenant/recipient-scoped list/read
        # predicate `CLAUDE.md §21.4` requires (`TDS-C132 §6.6` item 10).
        # `ix_c132_notification_membership_id` itself is produced by the
        # `index=True` on the `membership_id` column below (matching the
        # migration's own explicit index name), mirroring
        # `c023_entitlement_context.organization_id`'s own pattern.
        #
        # Natural list-filter index for the unread view (`TDS-C132 §6.6`
        # item 10 — a disclosed implementation-time choice, taken here).
        Index("ix_c132_notification_membership_status", "membership_id", "status"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    """Record identity and the audit correlation id (`TDS-C132 §6.6` item 1)."""

    membership_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("memberships.id"),
        nullable=False,
        index=True,
    )
    """
    Recipient anchor AND tenant anchor (`TDS-C132 §6.6` items 1/3). Hard
    intra-service FK to `memberships.id`, mirroring
    `AccessEvaluationOutcome.membership_id -> memberships.id`. The
    recipient's own `Membership.organization_id` is the tenant boundary —
    there is no duplicated `organization_id` column here.
    """

    severity: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    """One of DS-001's four closed values (`DS-001-350`): success / info / warning / danger."""

    what_happened: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    """`DS-001-351`'s mandatory composition element."""

    why_it_matters: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    """`DS-001-351`'s optional composition element."""

    what_happens_next: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    """`DS-001-351`'s optional composition element."""

    source_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    """
    Free-text, non-authoritative citation of the causing capability/table
    (e.g. `"C023_ENTITLEMENT_CONTEXT"`, `"MEMBERSHIP"`) — mirrors
    `entitlement_source_reference`'s own free-text, non-authoritative
    precedent (`TDS-C132 §6.6` item 1). Stores a REFERENCE, never a
    DEFINITION.
    """

    source_id: Mapped[uuid.UUID | None] = mapped_column(
        SA_UUID(),
        nullable=True,
    )
    """
    Point-in-time citation to the causing row's own id (`TDS-C132 §6.6`
    item 1). NOT a foreign key — mirrors `committed_by_actor_id`'s own
    established non-FK-citation precedent. A real FK is not used because
    the causing table varies by capability, and inventing a
    polymorphic-association mechanism to support one would be new
    architecture `CLAUDE.md §18` does not authorize here.
    """

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="UNREAD",
    )
    """`UNREAD` / `ACKNOWLEDGED` (`TDS-C132 §10`). BA-01 establishes `UNREAD` and transitions once to `ACKNOWLEDGED`."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    acknowledged_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    """NULL while `UNREAD`. Set exactly once, on the `UNREAD -> ACKNOWLEDGED` transition."""

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    membership: Mapped["Membership"] = relationship("Membership", foreign_keys=[membership_id])
