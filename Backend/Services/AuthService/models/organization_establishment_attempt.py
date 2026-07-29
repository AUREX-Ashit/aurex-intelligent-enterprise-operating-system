import uuid
from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import CheckConstraint, ForeignKey, String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from models.database import Base


class DomainVerificationStatus(str, Enum):
    """
    IRA-001A — BR-C004-02/BR-C004-09 (PE-001-C004): whether a claimed
    primary domain has been independently verified. NOT_CLAIMED is the
    default when no primary_domain is supplied at all (the governed
    no-domain path, ERB-C004-03) and is deliberately distinct from
    UNVERIFIED (a domain was claimed but verification has not
    succeeded) — BR-C004-09 requires this be a recorded fact, never a
    silent default or an inferred state.
    """
    NOT_CLAIMED = "NOT_CLAIMED"
    UNVERIFIED = "UNVERIFIED"
    VERIFIED = "VERIFIED"


class OrganizationEstablishmentAttempt(Base):
    """
    IRA-001A — Organization Anchor Context (PE-001-C004 §1.16),
    realizing ERB-C004-01's own Exit Context: a stable, explicitly
    non-authoritative construct correlating one establishment thread
    (candidate identity capture, domain verification, activation)
    until BA-01C (Activate Organization, first-time) produces the
    first Authoritative Organization Context for it (§1.17).

    Never queried by, or exposed through, any Organization-facing read
    path (get_details()/search(), BA-02/BA-03) — this is the
    structural mechanism that satisfies BR-C004-08 ("An Organization
    Anchor Context SHALL NOT be treated as, or represented as, an
    Authoritative Organization Context or Organization Validity
    Context, under any circumstance") and Contract 5.4's "resolve as
    NOT_FOUND" requirement: a row that lives only in this table is
    trivially NOT_FOUND to anything that only ever queries
    `organizations` (BA-02/BA-03 do, and continue to do, exactly that
    — neither was modified by this correction).
    """

    __tablename__ = "organization_establishment_attempts"
    __table_args__ = (
        CheckConstraint(
            "domain_verification_status IN ('NOT_CLAIMED', 'UNVERIFIED', 'VERIFIED')",
            name="ck_organization_establishment_attempts_domain_verification_status",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    organization_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    organization_name: Mapped[str] = mapped_column(String(255), nullable=False)
    organization_type: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    primary_domain: Mapped[str | None] = mapped_column(String(255), nullable=True)
    domain_verification_status: Mapped[str] = mapped_column(
        String(20),
        default=DomainVerificationStatus.NOT_CLAIMED.value,
        server_default=DomainVerificationStatus.NOT_CLAIMED.value,
    )
    no_domain_activation_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    """
    Populated only when BA-01C (Activate) proceeds without a VERIFIED
    domain claim — the governed no-domain activation decision itself,
    recorded as a fact rather than a silent default (BR-C004-09).
    """

    activated_organization_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("organizations.id"), nullable=True
    )
    """
    Set only by BA-01C (Activate). Per PE-001-C004 §1.17, the Anchor
    "remains preserved in lineage" once activation produces the first
    Authoritative Organization Context — this row is never deleted at
    activation, only linked forward. This column is a traceability
    reference only: it is never consulted by any existence/validity
    resolution path (get_details()/search()/EX-C004-05-style checks
    all query `organizations` directly, never this table), so its
    presence does not become a second, informal route by which a
    caller could infer Organization existence from this table — which
    would reintroduce the exact BR-C004-08 violation this construct
    exists to prevent.
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, onupdate=lambda: datetime.now(timezone.utc)
    )
