import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime, CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.database import Base

if TYPE_CHECKING:
    pass


class IdentityRecoveryRequest(Base):
    """
    WP-08 BA-02 — Recover Inaccessible Identity Context (EX-C001-07,
    self-service scope, PE-001-C001 v1.1).

    Records a governed recovery request and its routing determination
    (toward ERB-C001-01 new-Identity establishment, or ERB-C001-02
    re-resolution of a recoverable existing Identity) — never the
    technical credential-recovery mechanism itself, which EX-C001-07's
    own text states remains owned by the applicable canonical or
    implementation authority. Lifecycle ends at creation
    (status=PENDING); this Work Package does not execute the routed-to
    action (ERB-C001-01 is excluded from WP-08's own scope, IRA-008
    §4.1). Fails CMD-001 §26.3a's Business Object Eligibility Test
    (IRA-008 §6) — same disposition as WP-07's four audit-trail tables.
    """

    __tablename__ = "identity_recovery_requests"
    __table_args__ = (
        CheckConstraint(
            "routed_path IN ('NEW_IDENTITY', 'RE_RESOLUTION')",
            name="ck_identity_recovery_request_routed_path",
        ),
        CheckConstraint(
            "status IN ('PENDING')",
            name="ck_identity_recovery_request_status",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    person_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("persons.id", ondelete="CASCADE"),
        nullable=False,
    )

    requested_by_identity_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("identities.id", ondelete="SET NULL"),
        nullable=True,
    )

    reason: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )

    routed_path: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="PENDING",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
