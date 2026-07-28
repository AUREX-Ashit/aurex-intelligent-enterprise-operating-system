import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.database import Base

if TYPE_CHECKING:
    from models.membership import Membership
    from models.domain import Domain


class VersionStatus(str, Enum):
    """
    SD-002-011's Canonical Temporal Model Status property (WP-02
    BA-07/BA-08, ERB-C003-02/EX-C003-07/EX-C003-08). ACTIVE is the
    object's current, in-force version; SUPERSEDED is a preserved prior
    version (BR-C003-05 — never invalidated, deprecated, or retired by
    being superseded). DEPRECATED and RETIRED (BA-08) realize URA-001-127's
    Hide/Archive distinction respectively — DEPRECATED is Hidden
    (invisible, restorable in a future Business Activity; not
    reactivated here), RETIRED is Archived (inactive, historically
    accessible, terminal — no code path transitions away from it, the
    same discipline WP-01's Organization.activate()/suspend() already
    established for its own RETIRED state).
    """
    ACTIVE = "ACTIVE"
    SUPERSEDED = "SUPERSEDED"
    DEPRECATED = "DEPRECATED"
    RETIRED = "RETIRED"


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
        CheckConstraint(
            "status IN ('ACTIVE', 'SUPERSEDED', 'DEPRECATED', 'RETIRED')",
            name="ck_domain_permissions_status",
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

    version: Mapped[int] = mapped_column(
        Integer,
        default=1,
        server_default="1"
    )
    """WP-02 BA-07: SD-002-011 Version property."""

    status: Mapped[str] = mapped_column(
        String(20),
        default=VersionStatus.ACTIVE.value,
        server_default=VersionStatus.ACTIVE.value,
    )
    """WP-02 BA-07: SD-002-011 Status property (VersionStatus)."""

    approval_reference: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )
    """WP-02 BA-07: SD-002-011 Approval Reference property. Free-text (Contract 5.3 — never a workflow C-003 executes itself)."""

    supersedes_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("domain_permissions.id"),
        nullable=True
    )
    """WP-02 BA-07: BR-C003-05's prior-version link. 'Superseded By' is the derived inverse relationship, never a second stored column."""

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
    supersedes: Mapped["DomainPermission | None"] = relationship(
        "DomainPermission", remote_side=[id], foreign_keys=[supersedes_id], backref="superseded_by_one"
    )
