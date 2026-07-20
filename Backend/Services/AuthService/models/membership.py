import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.database import Base

if TYPE_CHECKING:
    from models.person import Person
    from models.organization import Organization
    from models.role import Role


class Membership(Base):
    """
    Connects a Person to an Organization through a Role.

    Examples:

    Ashit -> ABC -> ESG_MANAGER

    Ashit -> XYZ -> SUPPLIER_ADMIN
    """

    __tablename__ = "memberships"

    __table_args__ = (
        UniqueConstraint(
            "person_id",
            "organization_id",
            name="uq_membership_person_organization"
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
