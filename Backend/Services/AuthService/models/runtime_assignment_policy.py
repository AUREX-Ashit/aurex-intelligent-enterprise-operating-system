import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, String, DateTime, Integer, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.database import Base

if TYPE_CHECKING:
    from models.organization import Organization


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


class AssignmentTargetType(str, Enum):
    """
    URA-001-75's fixed four-value enumeration (Named User, Business Role,
    Group, or External User). Stored explicitly as the policy's declared
    target-type rule — mirrors approval_strategy's/delegation_type's own
    single-required-discriminator convention, not scope_type's
    anchor-consistency pattern, since a target-type declaration has no
    varying anchor column to keep consistent with it.
    """
    NAMED_USER = "NAMED_USER"
    BUSINESS_ROLE = "BUSINESS_ROLE"
    GROUP = "GROUP"
    EXTERNAL_USER = "EXTERNAL_USER"


class RuntimeAssignmentPolicy(Base):
    """
    Runtime Assignment Policy — a governed, reusable rule under which
    future Runtime Assignment instances may occur (WP-02 BA-05,
    ERB-C003-01/EX-C003-04 per PE-001-C003).

    Explicitly distinct from a Runtime Assignment instance (Contract 5.2,
    Object Distinctness — "a Runtime Assignment grants a new,
    object-scoped authority independent of any transfer, URA-001-74"):
    this model never holds a specific object_type/object_id anchor or
    assignee — those belong exclusively to the (not yet implemented in
    AuthService) runtime_assignment_registry, the operational act
    EX-C003-05 itself places outside this capability's boundary ("the
    specific act of assigning a Person to an object/event remains an
    operational act outside this capability"). status/effective_from/
    effective_to (added WP-02 BA-07) describe this Policy's own version
    window — when this particular version of the governed rule is in
    force — never a Runtime Assignment instance's own operational window.

    Declares exactly one assignment_target_type (URA-001-75), a
    configured lifecycle-states set (URA-001-78, defaulting to the nine
    canonical states and tenant-extensible), and an optional reference to
    an existing Escalation Policy (URA-001-80/94/94a). escalation_policy_id
    is a cross-registry reference with no declared FK — the same
    convention already established for object_id/event_code elsewhere in
    this capability — since escalation_policy_registry, though canonical,
    is not yet implemented in AuthService either. Realizes Master
    Technical Architecture's canonical runtime_assignment_policy_registry
    (URA-001-75/77/78/80/94/94a).
    """

    __tablename__ = "runtime_assignment_policies"
    __table_args__ = (
        CheckConstraint(
            "assignment_target_type IN ('NAMED_USER', 'BUSINESS_ROLE', 'GROUP', 'EXTERNAL_USER')",
            name="ck_runtime_assignment_policies_target_type",
        ),
        CheckConstraint(
            "status IN ('ACTIVE', 'SUPERSEDED', 'DEPRECATED', 'RETIRED')",
            name="ck_runtime_assignment_policies_status",
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

    policy_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    assignment_target_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    """NAMED_USER/BUSINESS_ROLE/GROUP/EXTERNAL_USER (URA-001-75) — exactly one per policy."""

    configured_lifecycle_states: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False
    )
    """
    URA-001-78: CREATED/ASSIGNED/ACCEPTED/IN_PROGRESS/COMPLETED/REJECTED/
    ESCALATED/EXPIRED/ARCHIVED are the default states; companies may add
    states such as BOARD_APPROVED. Defaulted to the nine canonical states
    by the service layer when the caller supplies none.
    """

    escalation_policy_id: Mapped[uuid.UUID | None] = mapped_column(
        nullable=True
    )
    """
    Populated only where escalation is configured (URA-001-80/94/94a's
    "where escalation is configured" — not mandatory on every policy).
    Cross-registry reference to escalation_policy_registry — no FK
    declared, same basis as this capability's own object_id/event_code
    convention, since escalation_policy_registry is not yet implemented
    in AuthService. escalation_policy_registry's own NOT NULL max_depth
    (DEFAULT 5) already guarantees the mandatory depth limit whenever a
    real escalation policy is referenced.
    """

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
    """WP-02 BA-07: SD-002-011 Status property (VersionStatus) — this Policy version's own status, never a Runtime Assignment instance's."""

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
        ForeignKey("runtime_assignment_policies.id"),
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
    supersedes: Mapped["RuntimeAssignmentPolicy | None"] = relationship(
        "RuntimeAssignmentPolicy", remote_side=[id], foreign_keys=[supersedes_id], backref="superseded_by_one"
    )
