import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime, Boolean, CheckConstraint, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.database import Base

if TYPE_CHECKING:
    from models.person import Person
    from models.organization import Organization
    from models.role import Role
    from models.organization_node import OrganizationNode


class MembershipType(str, Enum):
    """URA-001-106. WP-03 BA-01, ERB-C007-01/EX-C007-02 per PE-001-C007."""
    INTERNAL = "INTERNAL"
    EXTERNAL = "EXTERNAL"


class LicenseType(str, Enum):
    """URA-001-111. WP-03 BA-01, ERB-C007-01/EX-C007-02 per PE-001-C007."""
    FULL = "FULL"
    LIGHT = "LIGHT"


class Membership(Base):
    """
    Connects a Person to an Organization through a Role.

    Examples:

    Ashit -> ABC -> ESG_MANAGER

    Ashit -> XYZ -> SUPPLIER_ADMIN

    WP-03 BA-01 (Establish Membership Context, ERB-C007-01/EX-C007-01/02)
    extends this WP-00-era table with `home_node_id`, `membership_type`,
    `license_type`, `effective_from`, `effective_to` — the fields
    EX-C007-02's own Success Criteria requires ("anchored to a confirmed
    home node, with explicit license type, membership type and
    effective dates"). `role_id` (WP-00, NOT NULL) and `membership_status`
    (WP-00) are untouched — see TD-033 for the disclosed tension between
    this inherited requirement and PE-001-C007's own "C-007 does not
    assign or remove Roles or Permissions" boundary.
    """

    __tablename__ = "memberships"

    __table_args__ = (
        UniqueConstraint(
            "person_id",
            "organization_id",
            name="uq_membership_person_organization"
        ),
        CheckConstraint(
            "membership_type IN ('INTERNAL', 'EXTERNAL')",
            name="ck_memberships_membership_type",
        ),
        CheckConstraint(
            "license_type IN ('FULL', 'LIGHT')",
            name="ck_memberships_license_type",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    person_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("persons.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    role_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("roles.id"),
        nullable=False
    )

    membership_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="ACTIVE"
    )

    is_primary: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    home_node_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("organization_nodes.id"),
        nullable=True
    )
    """
    URA-001-17b / ERG-001-03's home-node anchor. Canonically NOT NULL,
    but deliberately nullable here (TD-032): no Business Activity
    anywhere establishes an OrganizationNode row today (MDP-001 excludes
    it from build-time seeding; C-005/Enterprise Structure Management,
    which would own that Business Activity, has no IRA yet), so a
    caller cannot always supply a valid candidate. When supplied, this
    method validates it references a real, active OrganizationNode
    (BR-C007-002/007) — it is never invented or defaulted.
    """

    membership_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=MembershipType.INTERNAL.value,
        server_default=MembershipType.INTERNAL.value,
    )
    """URA-001-106 (MembershipType). WP-03 BA-01."""

    license_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=LicenseType.FULL.value,
        server_default=LicenseType.FULL.value,
    )
    """URA-001-111 (LicenseType). WP-03 BA-01."""

    effective_from: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    """WP-03 BA-01: SD-002-011-style Effective From, per EX-C007-02's own Success Criteria. Establish-scoped only — no version/status/supersedes_id machinery, which belongs to a later Business Activity (Maintain Membership Terms), not BA-01."""

    effective_to: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    """WP-03 BA-01: Effective To. NULL while open-ended."""

    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

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
    person: Mapped["Person"] = relationship(
        "Person",
        back_populates="memberships"
    )

    organization: Mapped["Organization"] = relationship(
        "Organization",
        back_populates="memberships"
    )

    role: Mapped["Role"] = relationship(
        "Role",
        back_populates="memberships"
    )

    home_node: Mapped["OrganizationNode | None"] = relationship(
        "OrganizationNode",
        foreign_keys=[home_node_id],
    )
