import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.database import Base

if TYPE_CHECKING:
    from models.organization import Organization


class Domain(Base):
    """
    Domain — reference/master-data catalog per URA-001 §4 (AMD-014).

    Describes the Domain only (Finance, HR, Risk, Supply Chain, Cyber
    Security, Legal, Business Resilience, or a tenant-added equivalent).
    Platform-seeded (organization_id NULL), tenant-extensible
    (URA-001-43), hierarchical via parent_domain_id (URA-001-44).

    No lifecycle state machine and no Domain Owner/Domain Admin
    relationship is modeled here (URA-001-45/-46 remain open, not
    silently resolved — AMD-014 §4/§6): this table exists to support
    WP-02 BA-02's lookup requirement (PE-001-C003 EX-C003-02's Entry
    Context, "the target Domain, already established"), not to
    introduce a new Business Activity or governance surface.
    """

    __tablename__ = "domains"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    organization_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=True,
        index=True
    )
    """NULL = platform-default domain, visible to every tenant (URA-001-43)."""

    domain_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    parent_domain_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("domains.id"),
        nullable=True
    )
    """Sub-domain hierarchy (URA-001-44), e.g. Finance -> Accounting, Treasury, Taxation."""

    active_flag: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    organization: Mapped["Organization | None"] = relationship(
        "Organization",
        foreign_keys=[organization_id],
    )

    parent_domain: Mapped["Domain | None"] = relationship(
        "Domain",
        remote_side=[id],
    )
