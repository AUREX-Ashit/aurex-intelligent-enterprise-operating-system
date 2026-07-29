import uuid
from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from models.database import Base


class StructuralValidationStatus(str, Enum):
    """
    IRA-004 §26's own registered Lifecycle Model for VLC-000001
    (Validation Context): CREATED (EX-C005-10) -> INVALIDATED (material
    proposal revision, EX-C005-10's own Invalidated Context / BR-C005-005
    / GS-INV-007) -> ARCHIVED (SD-002-008's terminal state).

    WP-04 BA-07 ("Validate Transition Readiness") realizes only
    CREATED, mirroring BA-03/BA-04/BA-05/BA-06's own disclosed
    minimal-slice precedent (TD-052/053/057/062). INVALIDATED would
    require reaching into BA-04's own refine_proposal() flow, the same
    disclosed limitation already recorded for Impact Context (TD-057)
    and Review Context (TD-062) — see TD-065.
    """
    CREATED = "CREATED"
    INVALIDATED = "INVALIDATED"
    ARCHIVED = "ARCHIVED"


class StructuralValidation(Base):
    """
    Validation Context — the canonical Business Object VLC-000001
    (ADR-012; IRA-004 §26, CMD-001 §26.3/§26.4), realizing PE-001-C005's
    ERB-C005-07 ("Validate Transition Readiness") / EX-C005-10.

    Aggregate Root in its own right (IRA-004 §26's own "Aggregate Root"
    attribute) — not merged with Proposed Outcome Context (POC-000001),
    Impact Context (IMC-000001), or Review Context (RVC-000001), per
    ADR-010 point 5.

    Implementation class name is `StructuralValidation` /
    `structural_validations`, distinct from the canonical CBOR name
    "Validation Context" — the same implementation-name-vs-canonical-
    name disclosed choice already made for `StructuralProposal`,
    `ImpactAssessment`, and `StructuralReview`.

    **Readiness-result representation (IRA-004 §26's own explicitly
    undecided question, resolved here as this Business Activity's own
    first disclosed implementation decision):** EX-C005-10's own Exit
    Context (PE-001-C005 §40.8) offers two outcomes — "Validated
    Transition Context or explicit return-to-resolution context." This
    implementation realizes "return-to-resolution" as an HTTP 409
    rejection at the service layer (BR-C005-007's own hard enforcement
    — see services/structural_validation_service.py) rather than as a
    persisted row carrying a "not ready" state. Consequently, every row
    that exists in this table represents a successful ("ready")
    validation by construction — there is no `readiness_result` column,
    because the not-ready outcome never reaches persistence.

    References one specific `structural_proposals.id` (one revision,
    not a `proposal_id` lineage — BR-C005-006/GS-INV-006) and one
    specific `structural_reviews.id` — the review whose
    `CONCERNS_RESOLVED` status this Business Activity's own service
    layer hard-enforces before a row is ever created (BR-C005-007).
    Structural Change Intent (SCI-000001) is reached transitively
    through the referenced proposal's own `structural_change_intent_id`,
    the same design already used by `ImpactAssessment`/`StructuralReview`.

    No `organization_id` column: like every other C-005 experience-layer
    construct in this Work Package, this is enterprise-structure-level
    data, not organization-scoped (see `middleware/tenant.py`'s
    exemption for this router's own prefix).
    """

    __tablename__ = "structural_validations"
    __table_args__ = (
        CheckConstraint(
            "status IN ('CREATED', 'INVALIDATED', 'ARCHIVED')",
            name="ck_structural_validations_status",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    structural_proposal_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("structural_proposals.id"), nullable=False
    )
    """References one specific proposal revision (structural_proposals.id), not a proposal_id lineage."""

    structural_review_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("structural_reviews.id"), nullable=False
    )
    """The specific review whose CONCERNS_RESOLVED status this Business Activity's own service layer hard-enforces (BR-C005-007) before creating this row."""

    readiness_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    """Optional caller-supplied notes about the validation outcome — EX-C005-10's own "readiness result" narrative, distinct from the boolean fact of this row's own existence."""

    status: Mapped[str] = mapped_column(
        String(20),
        default=StructuralValidationStatus.CREATED.value,
        server_default=StructuralValidationStatus.CREATED.value,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, onupdate=lambda: datetime.now(timezone.utc)
    )
