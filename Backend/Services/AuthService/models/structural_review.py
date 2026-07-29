import uuid
from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from models.database import Base


class StructuralReviewStatus(str, Enum):
    """
    IRA-004 §25's own registered Lifecycle Model for RVC-000001 (Review
    Context): CREATED (EX-C005-08) -> CONCERNS_RESOLVED (EX-C005-09) ->
    INVALIDATED (material proposal revision, EX-C005-08's own
    Invalidated Context / GS-INV-007) -> ARCHIVED (SD-002-008's
    terminal state).

    WP-04 BA-06 ("Review Proposed Structural Outcome / Resolve
    Structural Review Concerns") realizes only CREATED and
    CONCERNS_RESOLVED, mirroring BA-03/BA-04/BA-05's own disclosed
    minimal-slice precedent (TD-052/053/057). INVALIDATED would require
    reaching into BA-04's own refine_proposal() flow (the event that
    triggers invalidation), the same disclosed limitation already
    recorded for Impact Context (TD-057) — see TD-062.
    """
    CREATED = "CREATED"
    CONCERNS_RESOLVED = "CONCERNS_RESOLVED"
    INVALIDATED = "INVALIDATED"
    ARCHIVED = "ARCHIVED"


class StructuralReview(Base):
    """
    Review Context — the canonical Business Object RVC-000001 (ADR-011;
    IRA-004 §25, CMD-001 §26.3/§26.4), realizing PE-001-C005's
    ERB-C005-06 ("Review Structural Outcome") / EX-C005-08 (Review) and
    EX-C005-09 (Resolve Concerns).

    Aggregate Root in its own right (IRA-004 §25's own "Aggregate Root"
    attribute) — not merged with Proposed Outcome Context (POC-000001)
    or Impact Context (IMC-000001), per ADR-010 point 5.

    Implementation class name is `StructuralReview` /
    `structural_reviews`, distinct from the canonical CBOR name "Review
    Context" — the same implementation-name-vs-canonical-name disclosed
    choice already made for `StructuralProposal` (POC-000001) and
    `ImpactAssessment` (IMC-000001).

    References one specific `structural_proposals.id` (one revision,
    not a `proposal_id` lineage) — BR-C005-006/GS-INV-006: "Review SHALL
    identify the exact proposal revision under review." Structural
    Change Intent (SCI-000001) is reached transitively through that
    revision's own `structural_change_intent_id`, not duplicated as a
    separate FK here — the same design already used by
    `ImpactAssessment`.

    Review Context owns its own concerns (`concerns`, a single Text
    field for this Business Activity's own v1 scope) — no separate
    "Concern" Business Object is registered or introduced. §41.16's own
    Collaboration Contract text ("Review concerns SHALL preserve
    author, decision context and unresolved/resolved status") arguably
    implies structured, per-concern tracking; that richness is
    deliberately deferred, not silently omitted — see TD-060.

    "Resolve concerns" (EX-C005-09) updates this same Review Context
    row's own `status` and, optionally, appends resolution rationale to
    `concerns` — it never creates or mutates a `StructuralProposal` row.
    Producing a revised proposal (EX-C005-09's own disclosed
    alternative Produced Context) remains exclusively BA-04's own
    `refine_proposal()` / `POST /structural-proposals/{id}/revisions`
    — a deliberate scope boundary, not an oversight.

    No `organization_id` column: like every other C-005 experience-layer
    construct in this Work Package, this is enterprise-structure-level
    data, not organization-scoped (see `middleware/tenant.py`'s
    exemption for this router's own prefix).
    """

    __tablename__ = "structural_reviews"
    __table_args__ = (
        CheckConstraint(
            "status IN ('CREATED', 'CONCERNS_RESOLVED', 'INVALIDATED', 'ARCHIVED')",
            name="ck_structural_reviews_status",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    structural_proposal_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("structural_proposals.id"), nullable=False
    )
    """References one specific proposal revision (structural_proposals.id), not a proposal_id lineage."""

    review_position: Mapped[str] = mapped_column(Text, nullable=False)
    """EX-C005-08's own Produced Context: "review position" — the reviewer's overall stance."""

    concerns: Mapped[str | None] = mapped_column(Text, nullable=True)
    """
    EX-C005-08's own Produced Context: "contextual concerns". Single
    Text field for BA-06's own v1 scope — deliberately deferred,
    structured per-concern author/status tracking (TD-060), not
    invented ahead of a real consumer needing it. Appended to, never
    overwritten, by resolve_concerns() (SS41.16: "Proposal revision
    SHALL not erase the rationale of earlier concerns" — applied here
    to concerns themselves).
    """

    status: Mapped[str] = mapped_column(
        String(20),
        default=StructuralReviewStatus.CREATED.value,
        server_default=StructuralReviewStatus.CREATED.value,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, onupdate=lambda: datetime.now(timezone.utc)
    )
