import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.database import Base

if TYPE_CHECKING:
    from models.organization import Organization
    from models.domain import Domain


class ApprovalStrategy(str, Enum):
    """URA-001-42/62's fixed four-value enumeration."""
    ANY_ONE = "ANY_ONE"
    ALL = "ALL"
    MAJORITY = "MAJORITY"
    SEQUENTIAL = "SEQUENTIAL"


class ApprovalScopeType(str, Enum):
    """
    URA-001-61's fixed four-value enumeration. Stored explicitly, never
    inferred from which anchor column is populated: DOMAIN and OBJECT are
    distinguishable by their own anchor columns, but GLOBAL and COMPANY
    share an identical anchor pattern (organization_id set, domain_id/
    object_type/object_id all NULL) now that organization_id is required
    for every scope — the two would be genuinely indistinguishable
    without their own stored discriminator, exactly the "vague or
    dual-stated" scope PE-001-C003 EX-C003-03's Success Criteria forbids.
    """
    GLOBAL = "GLOBAL"
    COMPANY = "COMPANY"
    DOMAIN = "DOMAIN"
    OBJECT = "OBJECT"


class ApprovalAuthority(Base):
    """
    Approval Authority — a first-class authorization object independent of
    Business Role (WP-02 BA-03, ERB-C003-01/EX-C003-03 per PE-001-C003).

    Declares exactly one approval_strategy and exactly one scope_type, the
    latter validated at the request layer (schemas/approval_authority.py)
    and enforced again at the database layer via
    ck_approval_authorities_scope_consistency, matching the anchor
    populated (domain_id for DOMAIN, object_type/object_id for OBJECT,
    neither for GLOBAL/COMPANY) to the declared scope_type exactly.
    Realizes Master Technical Architecture's canonical
    approval_authority_registry (URA-001-04/41/42/61/82).
    """

    __tablename__ = "approval_authorities"
    __table_args__ = (
        CheckConstraint(
            "approval_strategy IN ('ANY_ONE', 'ALL', 'MAJORITY', 'SEQUENTIAL')",
            name="ck_approval_authorities_approval_strategy",
        ),
        CheckConstraint(
            "scope_type IN ('GLOBAL', 'COMPANY', 'DOMAIN', 'OBJECT')",
            name="ck_approval_authorities_scope_type",
        ),
        CheckConstraint(
            "(scope_type IN ('GLOBAL', 'COMPANY') AND domain_id IS NULL AND object_type IS NULL AND object_id IS NULL) OR "
            "(scope_type = 'DOMAIN' AND domain_id IS NOT NULL AND object_type IS NULL AND object_id IS NULL) OR "
            "(scope_type = 'OBJECT' AND domain_id IS NULL AND object_type IS NOT NULL AND object_id IS NOT NULL)",
            name="ck_approval_authorities_scope_consistency",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=False,
        index=True
    )
    """Required for every scope, including GLOBAL/COMPANY."""

    authority_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    approval_strategy: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    majority_threshold_pct: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    scope_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    domain_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("domains.id"),
        nullable=True,
        index=True
    )
    """Populated only when scope_type = 'DOMAIN'."""

    object_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )
    """Populated only when scope_type = 'OBJECT' (mirrors runtime_assignment_registry's own anchor pattern)."""

    object_id: Mapped[uuid.UUID | None] = mapped_column(
        nullable=True
    )
    """Populated only when scope_type = 'OBJECT' — polymorphic, no FK (same basis as runtime_assignment_registry.object_id)."""

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
    organization: Mapped["Organization"] = relationship("Organization", foreign_keys=[organization_id])
    domain: Mapped["Domain | None"] = relationship("Domain", foreign_keys=[domain_id])
