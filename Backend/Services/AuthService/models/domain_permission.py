import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.database import Base

if TYPE_CHECKING:
    from models.membership import Membership
    from models.domain import Domain


class DomainPermissionLevel(str, Enum):
    """URA-001-47's fixed eight-value enumeration. Not metadata-driven — a
    plain, fixed enum, consistent with Organization's own interim-model
    precedent (ADR-005) pending the Metadata Runtime SD-002-051 requires."""
    VIEW = "VIEW"
    ENTER = "ENTER"
    EDIT = "EDIT"
    REVIEW = "REVIEW"
    APPROVE = "APPROVE"
    ASSIGN = "ASSIGN"
    DELEGATE = "DELEGATE"
    ADMIN = "ADMIN"


class DomainPermission(Base):
    """
    Domain Permission — a standing, Domain-anchored authorization grant to
    a Membership (WP-02 BA-02, ERB-C003-01/EX-C003-02 per PE-001-C003).

    Independent of any Business Role (URA-001-48, BR-C003-02): establishing
    one never touches `roles`/`role_permissions`. Realizes Master Technical
    Architecture's canonical `domain_permission_registry` (URA-001-47).
    """

    __tablename__ = "domain_permissions"
    __table_args__ = (
        CheckConstraint(
            "permission_level IN ('VIEW', 'ENTER', 'EDIT', 'REVIEW', 'APPROVE', 'ASSIGN', 'DELEGATE', 'ADMIN')",
            name="ck_domain_permissions_permission_level",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    membership_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("memberships.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    domain_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("domains.id"),
        nullable=False,
        index=True
    )

    permission_level: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    """One of DomainPermissionLevel's eight values (URA-001-47)."""

    effective_from: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    effective_to: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    """NULL = open-ended, currently active (URA-001-53: permissions may be time-bound, not always)."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        onupdate=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    membership: Mapped["Membership"] = relationship("Membership")
    domain: Mapped["Domain"] = relationship("Domain")
