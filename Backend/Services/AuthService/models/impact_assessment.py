import uuid
from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from models.database import Base


class ImpactAssessmentStatus(str, Enum):
    """
    IRA-004 §23's own registered Lifecycle Model for IMC-000001 (Impact
    Context): CREATED (EX-C005-07) -> INVALIDATED (material proposal
    revision, EX-C005-07's own Invalidated Context) -> ARCHIVED
    (SD-002-008's terminal state).

    WP-04 BA-05 ("Assess Structural Consequence") realizes only
    CREATED, mirroring BA-03/BA-04's own disclosed minimal-slice
    precedent (TD-052/TD-053). Setting INVALIDATED would require
    reaching into BA-04's own refine_proposal() flow (the event that
    triggers invalidation) — out of BA-05's own scope ("implement only
    what BA-05 owns"), deferred rather than invented here — see TD-057.
    """
    CREATED = "CREATED"
    INVALIDATED = "INVALIDATED"
    ARCHIVED = "ARCHIVED"


class ImpactAssessment(Base):
    """
    Impact Context — the canonical Business Object IMC-000001 (ADR-009;
    IRA-004 §23, CMD-001 §26.3/§26.4), realizing PE-001-C005's
    ERB-C005-05 ("Assess Structural Consequence") / EX-C005-07.

    Aggregate Root in its own right (IRA-004 §23's own "Aggregate Root"
    attribute) — computed *about* a specific `StructuralProposal`
    revision but independently identified, retrieved, and invalidated
    across BA-06/BA-07's own later experience stages, not a sub-object
    of Proposed Outcome Context (POC-000001).

    Implementation class name is `ImpactAssessment` /
    `impact_assessments`, distinct from the canonical CBOR name
    "Impact Context" — the same implementation-name-vs-canonical-name
    disclosed choice already made for `StructuralProposal` (POC-000001)
    and `StructuralChangeIntent` (SCI-000001).

    References a specific `structural_proposals.id` (one revision, not
    a `proposal_id` lineage) — EX-C005-07's own Required Context is "A
    coherent proposed structural outcome", i.e. one specific revision;
    "current authoritative structural context" (the other half of that
    Required Context) is reached transitively via that revision's own
    `target_organization_node_id`, not duplicated as a separate FK here.

    No `organization_id` column: like every other C-005 experience-layer
    construct in this Work Package, this is enterprise-structure-level
    data, not organization-scoped (see `middleware/tenant.py`'s
    exemption for this router's own prefix).
    """

    __tablename__ = "impact_assessments"
    __table_args__ = (
        CheckConstraint(
            "status IN ('CREATED', 'INVALIDATED', 'ARCHIVED')",
            name="ck_impact_assessments_status",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    structural_proposal_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("structural_proposals.id"), nullable=False
    )
    """References one specific proposal revision (structural_proposals.id), not a proposal_id lineage."""

    impact_description: Mapped[str] = mapped_column(Text, nullable=False)
    """EX-C005-07's own Produced Context: known consequence context — affected structural areas."""

    uncertainty_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    """EX-C005-07's own Produced Context: uncertain consequence context. Optional — not every assessment carries unresolved uncertainty."""

    downstream_implications: Mapped[str | None] = mapped_column(Text, nullable=True)
    """
    BR-C005-008: C-005 SHALL identify downstream capability implications
    but SHALL not execute outcomes owned by those capabilities. This
    field records the identification only — no downstream capability
    action is triggered by this Business Activity. Optional — not every
    assessment identifies a downstream implication.
    """

    status: Mapped[str] = mapped_column(
        String(20),
        default=ImpactAssessmentStatus.CREATED.value,
        server_default=ImpactAssessmentStatus.CREATED.value,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, onupdate=lambda: datetime.now(timezone.utc)
    )
