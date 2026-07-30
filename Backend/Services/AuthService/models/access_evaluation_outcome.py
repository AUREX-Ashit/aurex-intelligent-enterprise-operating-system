import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.database import Base

if TYPE_CHECKING:
    from models.membership import Membership
    from models.domain import Domain


class AccessEvaluationOutcomeType(str, Enum):
    """
    ADR-015 / IRA-005 S11's own Lifecycle Model: Outcome Type, fixed at
    creation, exactly one of four (BR-C002-02, the closed-set rule).

    WP-05's own authorized scope (IRA-005 S12) writes only UNRESOLVED and
    DEFERRED. PERMITTED/DENIED require a URA-001-76 precedence-chain
    determination this Work Package is explicitly not authorized to
    compute (no real TierResolver exists in WP-RTA-001 yet) -- the full
    four-value enum is declared here for schema correctness (mirroring
    TD-052/TD-057/TD-062/TD-065/TD-069's own identical precedent: the
    constraint allows the full registered Lifecycle Model even where a
    given Business Activity's own code writes only a subset), not
    because this Work Package's own code path can ever produce them.
    """
    PERMITTED = "PERMITTED"
    DENIED = "DENIED"
    UNRESOLVED = "UNRESOLVED"
    DEFERRED = "DEFERRED"


class AccessEvaluationValidityStatus(str, Enum):
    """ADR-015 / IRA-005 S11's own Lifecycle Model: Validity Status. CREATED (BA-01) -> PRESERVED (BA-02) -> {SUPERSEDED | INVALIDATED (BA-03) | EXPIRED (BA-02)}. SUPERSEDED is never written by WP-05 (would require a fresh BA-01 re-evaluation producing a new record, itself gated by the same Permitted/Denied exclusion) -- declared for schema completeness, same class of gap as the Outcome Type ones above."""
    CREATED = "CREATED"
    PRESERVED = "PRESERVED"
    SUPERSEDED = "SUPERSEDED"
    INVALIDATED = "INVALIDATED"
    EXPIRED = "EXPIRED"


class AccessEvaluationOutcome(Base):
    """
    Access Evaluation Outcome (AEO-000001, WP-05 / C-002, ADR-015).

    The scoped, temporally-bounded determination of whether a specific
    governed request is currently permitted -- never authoritative in
    itself (IRA-005 S11, PE-001-C002 S1.7), always derived from Identity,
    Membership, Role, Permission, Delegation, Runtime Assignment,
    Organization, and Enterprise Scope facts consumed from their owning
    authorities. This Work Package's own authorized scope (IRA-005 S12)
    produces this record only via BA-01's Unresolved/Deferred branches;
    BA-02/03/04 transition its Validity Status. Never PERMITTED/DENIED
    (see AccessEvaluationOutcomeType's own docstring).
    """

    __tablename__ = "access_evaluation_outcomes"
    __table_args__ = (
        CheckConstraint(
            "outcome_type IN ('PERMITTED', 'DENIED', 'UNRESOLVED', 'DEFERRED')",
            name="ck_access_evaluation_outcomes_outcome_type",
        ),
        CheckConstraint(
            "validity_status IN ('CREATED', 'PRESERVED', 'SUPERSEDED', 'INVALIDATED', 'EXPIRED')",
            name="ck_access_evaluation_outcomes_validity_status",
        ),
        CheckConstraint(
            "permission_level IN ('VIEW', 'ENTER', 'EDIT', 'REVIEW', 'APPROVE', 'ASSIGN', 'DELEGATE', 'ADMIN')",
            name="ck_access_evaluation_outcomes_permission_level",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    membership_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("memberships.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    domain_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("domains.id"),
        nullable=False,
        index=True,
    )

    permission_level: Mapped[str] = mapped_column(String(50), nullable=False)
    """One of DomainPermissionLevel's eight values (URA-001-47), reused verbatim -- not redefined."""

    outcome_type: Mapped[str] = mapped_column(String(20), nullable=False)
    """One of AccessEvaluationOutcomeType's four values -- fixed at creation, never amended (BR-C002-02)."""

    validity_status: Mapped[str] = mapped_column(
        String(20),
        default=AccessEvaluationValidityStatus.CREATED.value,
        server_default=AccessEvaluationValidityStatus.CREATED.value,
    )

    reason: Mapped[str] = mapped_column(Text, nullable=False)
    """The exact basis for outcome_type / the latest validity_status transition -- never a bare verdict (mirrors WP-02 BA-09/BA-10's own explainability discipline)."""

    approval_authority_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("approval_authorities.id"),
        nullable=True,
    )
    """Populated only for DEFERRED outcomes -- the specific Approval Authority this request is deferred to (EX-C002-04's own Context Consumed)."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    membership: Mapped["Membership"] = relationship("Membership")
    domain: Mapped["Domain"] = relationship("Domain")
