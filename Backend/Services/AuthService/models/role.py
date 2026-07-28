import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Index, String, DateTime, Boolean, Integer, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.database import Base

if TYPE_CHECKING:
    from models.membership import Membership
    from models.role_permission import RolePermission


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


class Role(Base):
    """
    Role assigned to a Membership.

    Examples:
    - PLATFORM_ADMIN
    - ORG_ADMIN
    - ESG_MANAGER
    - AUDITOR
    - SUPPLIER_ADMIN
    - BOARD_MEMBER
    """

    __tablename__ = "roles"
    __table_args__ = (
        CheckConstraint(
            "status IN ('ACTIVE', 'SUPERSEDED', 'DEPRECATED', 'RETIRED')",
            name="ck_roles_status",
        ),
        # WP-02 BA-07: role_code identifies the governed Role across its
        # full version history (BR-C003-05) — a SUPERSEDED row legitimately
        # shares role_code with its current ACTIVE successor. Uniqueness
        # is therefore scoped to ACTIVE rows only, replacing WP-00's plain
        # (whole-table) unique constraint, which predates versioning and
        # would otherwise reject every version amendment outright.
        Index(
            "ix_roles_role_code_active_unique",
            "role_code",
            unique=True,
            sqlite_where=text("status = 'ACTIVE'"),
            postgresql_where=text("status = 'ACTIVE'"),
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    role_code: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    """
    WP-02 BA-07: uniqueness is no longer declared inline (unique=True)
    since versioning requires it scoped to ACTIVE rows only — see the
    partial unique index in __table_args__ above.
    """

    role_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True
    )

    is_system_role: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    version: Mapped[int] = mapped_column(
        Integer,
        default=1,
        server_default="1"
    )
    """WP-02 BA-07: SD-002-011 Version property. Starts at 1; incremented by each Version and Re-effective-Date amendment."""

    status: Mapped[str] = mapped_column(
        String(20),
        default=VersionStatus.ACTIVE.value,
        server_default=VersionStatus.ACTIVE.value,
    )
    """WP-02 BA-07: SD-002-011 Status property. ACTIVE or SUPERSEDED (VersionStatus)."""

    effective_from: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    """WP-02 BA-07: SD-002-011 Effective From property."""

    effective_to: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    """WP-02 BA-07: SD-002-011 Effective To property. NULL while this version remains current."""

    approval_reference: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )
    """WP-02 BA-07: SD-002-011 Approval Reference property. Free-text; not a FK to approval_authorities (Contract 5.3 — C-003 never executes an approval workflow, only records a reference to one)."""

    supersedes_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("roles.id"),
        nullable=True
    )
    """WP-02 BA-07: BR-C003-05's prior-version link. Points to the version this row replaces. 'Superseded By' is the derived inverse (superseded_by relationship below), never a second stored column."""

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
    memberships: Mapped[list["Membership"]] = relationship(
        "Membership",
        back_populates="role"
    )

    role_permissions: Mapped[list["RolePermission"]] = relationship(
        "RolePermission",
        back_populates="role"
    )

    supersedes: Mapped["Role | None"] = relationship(
        "Role", remote_side=[id], foreign_keys=[supersedes_id], backref="superseded_by_one"
    )
