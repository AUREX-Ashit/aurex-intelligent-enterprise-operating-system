import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Index, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.database import Base

if TYPE_CHECKING:
    from models.membership import Membership
    from models.approval_authority import ApprovalAuthority


class MembershipApprovalAuthority(Base):
    """
    Membership <-> Approval Authority binding (WP-18, C-003, TDS-018
    §5-§7/§19/§29.2), realizing Master Technical Architecture's canonical
    `membership_approval_authority` join table — previously disclosed as
    canonical-but-unimplemented (`approval_authority_repository.py`'s own
    `get_active_dependents()` docstring, TD-023/TD-028).

    Exact canonical column set (`Master_Technical_Architecture.md` lines
    1318-1329) — no column added beyond what is canonically specified.
    Deliberately carries no `organization_id` column of its own, mirroring
    the canonical definition exactly; Organization isolation is enforced
    at two other points instead (TDS-018 §18): a service-layer
    existence-and-match check at bind time
    (`MembershipApprovalAuthorityService.bind()`, TDS-018 §7/§19's own
    disclosed requirement, mirroring `ApprovalAuthorityService.establish()`'s
    own FK-existence-validation pattern), and the resolver's own explicit
    caller-Organization-vs-target-Organization check at resolution time
    (`services/approval_authority_resolver.py`, TDS-018 §29.2 step 4).

    Records one Membership's own time-bounded eligibility to satisfy one
    Approval Authority under the `ANY_ONE` strategy (TDS-018 §8) — never
    itself a workflow execution or a vote, and never itself the source of
    `ALL`/`MAJORITY`/`SEQUENTIAL` semantics, which remain unresolved
    (TDS-018 §9/§29.5).
    """

    __tablename__ = "membership_approval_authority"
    __table_args__ = (
        # Active-binding uniqueness/concurrency protection (TDS-018 §19):
        # at most one currently-open (effective_to IS NULL) binding per
        # (membership_id, approval_authority_id) pair — the same
        # partial-unique-index pattern `authority_holders` already
        # establishes for its own "at most one ACTIVE row" invariant,
        # applied here to this table's own effective_to-based openness
        # concept (this table has no separate status column).
        Index(
            "ux_membership_approval_authority_active",
            "membership_id",
            "approval_authority_id",
            unique=True,
            postgresql_where=text("effective_to IS NULL"),
            sqlite_where=text("effective_to IS NULL"),
        ),
    )

    membership_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("memberships.id"),
        primary_key=True,
        nullable=False,
    )

    approval_authority_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("approval_authorities.id"),
        primary_key=True,
        nullable=False,
    )

    effective_from: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        primary_key=True,
        default=lambda: datetime.now(timezone.utc),
    )
    """Third element of the composite PK, per the canonical schema exactly."""

    effective_to: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    """NULL while this binding remains open. Closed via `MembershipApprovalAuthorityService.close()` — never hard-deleted (TDS-018 §9's own soft-close convention, mirrored from `ApprovalAuthority`/`DelegationPolicy`/`RuntimeAssignmentPolicy`/`AuthorityHolder`)."""

    # Relationships
    membership: Mapped["Membership"] = relationship("Membership", foreign_keys=[membership_id])
    approval_authority: Mapped["ApprovalAuthority"] = relationship("ApprovalAuthority", foreign_keys=[approval_authority_id])
