import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, String, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.database import Base

if TYPE_CHECKING:
    from models.membership import Membership


class OrganizationStatus(str, Enum):
    """
    ADR-005 interim lifecycle model. Not metadata-driven (SD-002-051's
    target architecture) — a plain, fixed enum pending the Metadata Runtime.
    RETIRED (BA-07, ERB-C004-07 per PE-001-C004) is terminal: no code path
    in OrganizationService transitions a RETIRED organization to any
    other status.
    """
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    RETIRED = "RETIRED"


class Organization(Base):
    """
    Organization represents a company, supplier, customer,
    regulator, NGO, or any legal entity onboarded into CorpStage.
    """

    __tablename__ = "organizations"
    __table_args__ = (
        # Declared on the model to close TD-004 (model/migration drift) —
        # matches the CHECK constraint created in b3f7a1c9d2e4 and widened
        # in d2d840d224b6 (BA-07) to include RETIRED.
        CheckConstraint("status IN ('ACTIVE', 'SUSPENDED', 'RETIRED')", name="ck_organizations_status"),
    )

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
    Interim lifecycle state ('ACTIVE' / 'SUSPENDED' / 'RETIRED', the third
    value added in BA-07 per ERB-C004-07) per ADR-005 — a plain column,
    not the metadata-driven state machine SD-002-051 ultimately requires.
    This is the seam a future Metadata Runtime migration replaces.
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
