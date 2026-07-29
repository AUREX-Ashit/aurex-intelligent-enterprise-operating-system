import uuid
from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from models.database import Base


class StructuralCompletionStatus(str, Enum):
    """
    IRA-004 §27's own registered Lifecycle Model for RSC-000001
    (Resulting Structural Context): CREATED (EX-C005-11) -> ARCHIVED
    (SD-002-008's terminal state). Deliberately no INVALIDATED
    transition — unlike every earlier Structural Context Lifecycle
    stage, this object represents a terminal, successfully-completed
    outcome; PE-001-C005's own text gives it no revision-invalidation
    semantics (IRA-004 §27's own disclosed difference from its five
    siblings).

    WP-04 BA-08 ("Complete Structural Transition") realizes only
    CREATED, mirroring every prior Business Activity's own disclosed
    minimal-slice precedent (TD-052/053/057/062/065) — see TD-069.
    """
    CREATED = "CREATED"
    ARCHIVED = "ARCHIVED"


class StructuralCompletion(Base):
    """
    Resulting Structural Context — the canonical Business Object
    RSC-000001 (ADR-013; IRA-004 §27, CMD-001 §26.3/§26.4), realizing
    PE-001-C005's ERB-C005-08 ("Complete Structural Transition") /
    EX-C005-11.

    Aggregate Root in its own right (IRA-004 §27's own "Aggregate Root"
    attribute) — not merged with Validation Context (VLC-000001) or any
    earlier stage, per ADR-010 point 5.

    Implementation class name is `StructuralCompletion` /
    `structural_completions`, distinct from the canonical CBOR name
    "Resulting Structural Context" — the same implementation-name-vs-
    canonical-name disclosed choice already made for every prior
    Structural Context Lifecycle member.

    **Option A scope (BA-08's own readiness assessment; mandatory per
    this task's own instruction):** this Business Activity records
    that a governed structural transition has been completed — it does
    NOT mutate `organization_nodes`, and does NOT create
    `organization_hierarchy` or `consolidation_determination`. PE-001-
    C005 §38.4 explicitly places database/mutation mechanics outside
    C-005's own scope; every `StructuralProposal` carries only free
    text (`proposed_outcome_description`), and no canonical document
    anywhere in this repository specifies a structured representation
    from which a real ERG-001 mutation could be deterministically
    derived. Inventing one here would be an unauthorized architectural
    addition (CLAUDE.md §18/§19.4), not an implementation detail.
    Deferred — see TD-070.

    References one specific `structural_validations.id` (GS-INV-012:
    "Completion SHALL identify the exact validated proposal revision
    from which Resulting Structural Context was produced" — reached
    via the referenced validation's own chain, the same design already
    used by every prior Structural Context Lifecycle member).
    Structural Change Intent, Proposed Outcome Context, Impact Context,
    and Review Context are all reached transitively through that same
    validation, never duplicated as separate FKs here.

    **Completion is a guarded transition, not idempotent** (this
    Business Activity's own first disclosed implementation decision,
    per this task's own instruction): a second completion attempt
    against the same `structural_validation_id` is rejected with 409,
    mirroring BA-06's own already-resolved-review guard and BA-07's own
    unresolved-concerns guard — completion is a one-time terminal
    event, not a revision chain (unlike BA-04's own deliberately
    append-only `StructuralProposal`).

    No `organization_id` column: like every other C-005 experience-layer
    construct in this Work Package, this is enterprise-structure-level
    data, not organization-scoped (see `middleware/tenant.py`'s
    exemption for this router's own prefix).
    """

    __tablename__ = "structural_completions"
    __table_args__ = (
        CheckConstraint(
            "status IN ('CREATED', 'ARCHIVED')",
            name="ck_structural_completions_status",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    structural_validation_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("structural_validations.id"), nullable=False, unique=True
    )
    """
    One specific validation (GS-INV-012). `unique=True` enforces the
    guarded-transition decision above at the database level, not only
    in the service layer's own pre-check — the same second-line-of-
    defense discipline `OrganizationService.establish()` already
    established for `organization_code`.
    """

    completion_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    """Optional caller-supplied notes about the completion outcome — EX-C005-11's own "completion outcome" narrative."""

    status: Mapped[str] = mapped_column(
        String(20),
        default=StructuralCompletionStatus.CREATED.value,
        server_default=StructuralCompletionStatus.CREATED.value,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, onupdate=lambda: datetime.now(timezone.utc)
    )
