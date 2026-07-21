import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.database import Base

if TYPE_CHECKING:
    from models.membership import Membership


class OrganizationStatus(str, Enum):
    """
    ADR-005 interim lifecycle model. Not metadata-driven (SD-002-051's
    target architecture) — a plain, fixed enum pending the Metadata Runtime.
    """
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"


class Organization(Base):
    """
    Organization represents a company, supplier, customer,
    regulator, NGO, or any legal entity onboarded into CorpStage.
    """

    __tablename__ = "organizations"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    organization_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    organization_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    organization_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default=OrganizationStatus.ACTIVE.value,
        server_default=OrganizationStatus.ACTIVE.value,
    )
    """
    Interim lifecycle state ('ACTIVE' / 'SUSPENDED') per ADR-005 — a plain
    column, not the metadata-driven state machine SD-002-051 ultimately
    requires. This is the seam a future Metadata Runtime migration replaces.
    """

    description: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
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
    memberships: Mapped[list["Membership"]] = relationship(
        "Membership",
        back_populates="organization"
    )
