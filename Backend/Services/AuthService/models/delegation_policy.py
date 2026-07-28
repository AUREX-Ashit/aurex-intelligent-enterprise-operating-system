import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, String, DateTime, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.database import Base

if TYPE_CHECKING:
    from models.organization import Organization
    from models.domain import Domain


class VersionStatus(str, Enum):
    """
    SD-002-011's Canonical Temporal Model Status property (WP-02 BA-07,
    ERB-C003-02/EX-C003-07). ACTIVE is the object's current, in-force
    version; SUPERSEDED is a preserved prior version (BR-C003-05 — never
    invalidated, deprecated, or retired by being superseded). Deprecated/
    Retired states belong to a future Business Activity (EX-C003-08) and
    are not added here.
    """
    ACTIVE = "ACTIVE"
    SUPERSEDED = "SUPERSEDED"


class DelegationScopeType(str, Enum):
    """
    URA-001-89's fixed four-value enumeration. Stored explicitly, never
    inferred from anchor presence — ORGANIZATION scope shares an
    identical (empty) anchor pattern with no other scope here, but would
    become ambiguous the same way BA-03's GLOBAL/COMPANY pair was without
    its own stored discriminator (PE-001-C003 Contract 5.2, Object
    Distinctness).
    """
    ORGANIZATION = "ORGANIZATION"
    DOMAIN = "DOMAIN"
    OBJECT = "OBJECT"
    EVENT = "EVENT"


class DelegationPolicy(Base):
    """
    Delegation Policy — a governed, reusable rule under which future
    delegation instances may occur (WP-02 BA-04, ERB-C003-01/EX-C003-04
    per PE-001-C003).

    Explicitly distinct from a delegation instance (Contract 5.2, Object
    Distinctness): this model never holds a specific delegator/delegatee
    pairing, a reason, or a concrete date window — those belong
    exclusively to the (not yet implemented in AuthService)
    delegation_registry, the operational act EX-C003-04 itself places
    outside this capability's boundary. Declares exactly one
    delegation_type and exactly one scope_type, the latter validated at
    the request layer (schemas/delegation_policy.py) and enforced again
    at the database layer via ck_delegation_policies_scope_consistency.
    Realizes Master Technical Architecture's canonical
    delegation_policy_registry (URA-001-88/89/90/92).
    """

    __tablename__ = "delegation_policies"
    __table_args__ = (
        CheckConstraint(
            "scope_type IN ('ORGANIZATION', 'DOMAIN', 'OBJECT', 'EVENT')",
            name="ck_delegation_policies_scope_type",
        ),
        CheckConstraint(
            "(scope_type = 'ORGANIZATION' AND domain_id IS NULL AND object_type IS NULL AND object_id IS NULL AND event_code IS NULL) OR "
            "(scope_type = 'DOMAIN' AND domain_id IS NOT NULL AND object_type IS NULL AND object_id IS NULL AND event_code IS NULL) OR "
            "(scope_type = 'OBJECT' AND domain_id IS NULL AND object_type IS NOT NULL AND object_id IS NOT NULL AND event_code IS NULL) OR "
            "(scope_type = 'EVENT' AND domain_id IS NULL AND object_type IS NULL AND object_id IS NULL AND event_code IS NOT NULL)",
            name="ck_delegation_policies_scope_consistency",
        ),
        CheckConstraint(
            "status IN ('ACTIVE', 'SUPERSEDED')",
            name="ck_delegation_policies_status",
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
    """Required for every scope, including ORGANIZATION."""

    policy_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    delegation_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    """TEMPORARY/OUT_OF_OFFICE/EMERGENCY/ACTING_ROLE/PROJECT_BASED, or a tenant-defined custom type (URA-001-90) — open-ended, no CHECK constraint."""

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

    event_code: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )
    """Populated only when scope_type = 'EVENT' — links to workflow_event_registry, no FK (same cross-registry-reference basis as runtime_assignment_registry.event_code)."""

    sub_delegation_allowed: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )
    """URA-001-92: organizations explicitly permit or prohibit further delegation of an already-delegated authority."""

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
    """WP-02 BA-07: SD-002-011 Approval Reference property. Free-text (Contract 5.3 — never a workflow C-003 executes itself)."""

    supersedes_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("delegation_policies.id"),
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
    organization: Mapped["Organization"] = relationship("Organization", foreign_keys=[organization_id])
    domain: Mapped["Domain | None"] = relationship("Domain", foreign_keys=[domain_id])
    supersedes: Mapped["DelegationPolicy | None"] = relationship(
        "DelegationPolicy", remote_side=[id], foreign_keys=[supersedes_id], backref="superseded_by_one"
    )
