import uuid
from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from models.database import Base


class StructuralProposalStatus(str, Enum):
    """
    IRA-004 §22's own registered Lifecycle Model for POC-000001
    (Proposed Outcome Context): CREATED (EX-C005-05) -> REVISED
    (EX-C005-06) -> SUPERSEDED on revision -> a distinct, revocable
    readiness marker, VALIDATED (BR-C005-005) -> ARCHIVED (SD-002-008's
    terminal state).

    REVISED is not modeled as a row-level status here: this
    implementation realizes "a coherent proposal revision" (EX-C005-06)
    structurally, as a new immutable row sharing the same `proposal_id`
    with an incremented `revision_number` (POC-000001's own registered
    append-only Versioning Policy), not as a status transition of an
    existing row. A row's own status is therefore either the revision
    that was created (CREATED) or the revision a later one superseded
    (SUPERSEDED) — never REVISED.

    WP-04 BA-04 ("Shape / Refine Proposed Structural Outcome") realizes
    only CREATED and SUPERSEDED, mirroring BA-03's own disclosed
    minimal-slice precedent (TD-052): VALIDATED is BA-07's own future
    "Validate Transition Readiness" concern (not yet implemented, its
    own representation - separate column vs. separate table - is not
    decided here) and ARCHIVED is not reachable by any Business Activity
    implemented so far. Declared here, not invented, per POC-000001's
    own registered Lifecycle Model (IRA-004 §22) - see TD-053.
    """
    CREATED = "CREATED"
    SUPERSEDED = "SUPERSEDED"
    VALIDATED = "VALIDATED"
    ARCHIVED = "ARCHIVED"


class StructuralProposal(Base):
    """
    Proposed Outcome Context — the canonical Business Object POC-000001
    (ADR-008; IRA-004 §22, CMD-001 §26.3/§26.4), realizing PE-001-C005's
    ERB-C005-04 ("Shape Proposed Structural Outcome") / EX-C005-05
    (Shape) and EX-C005-06 (Refine).

    Aggregate Root in its own right (IRA-004 §22's own "Aggregate Root"
    attribute) — related to, but not a sub-object of, Structural Change
    Intent (SCI-000001) or the EnterpriseNode it targets.

    **Append-only revision model** (POC-000001's own registered
    Versioning Policy: "Full version history retained; superseded
    revisions preserved in traceability, never physically deleted"):
    each row is one immutable revision. `proposal_id` is the stable
    identity of the logical proposal across its full revision history
    (equal to `id` for a proposal's first/CREATED revision — no
    separate "header" table is introduced); `revision_number`
    distinguishes revisions within that lineage. Shaping a proposal
    (BA-04, EX-C005-05) inserts revision 1. Refining it (BA-04,
    EX-C005-06) inserts a new row (revision N+1) and transitions the
    prior current row's own `status` to SUPERSEDED — a status
    transition, not a content mutation: `proposed_outcome_description`
    on an existing row is never altered after insert.

    Carries `structural_change_intent_id` (EX-C005-05's own Required
    Context: "Change Intent Context") and, per `ADR-007`'s own
    EnterpriseNode-only BA-04 v1 scope decision,
    `target_organization_node_id` — bound for v1 only; a future BA-04
    extension (ADR-007 point 5) would add an EnterpriseRelationship or
    ConsolidationDetermination target column, not repurpose this one.
    Both are immutable across a proposal's own revisions (BR-C005-004:
    "every proposal revision SHALL remain traceable to the change
    intent that produced it") — Refine may change only
    `proposed_outcome_description`.

    No `organization_id` column: like `organization_nodes` and
    `structural_change_intents`, this is an enterprise-structure-level
    construct, not organization-scoped data (see
    `middleware/tenant.py`'s exemption for this router's own prefix).

    "Initial Comparison Context" (EX-C005-05's own Produced Context,
    alongside Proposed Outcome Context) is deliberately not persisted
    here — it fails the Cross-Experience Reference Test (named only
    within EX-C005-05's own text, never required by a later Enterprise
    Experience) and is therefore not itself a registered Business
    Object; implementing a structural diff/comparison representation
    without any PE-001-C005 text specifying what is compared would be
    architecture invention beyond this Business Activity's own scope.
    Deferred, not silently omitted — see TD-054.
    """

    __tablename__ = "structural_proposals"
    __table_args__ = (
        CheckConstraint(
            "status IN ('CREATED', 'SUPERSEDED', 'VALIDATED', 'ARCHIVED')",
            name="ck_structural_proposals_status",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    proposal_id: Mapped[uuid.UUID] = mapped_column(nullable=False, index=True)
    """Stable identity of the logical proposal across all its revisions — equals `id` for revision 1."""

    revision_number: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    structural_change_intent_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("structural_change_intents.id"), nullable=False
    )

    target_organization_node_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organization_nodes.id"), nullable=False
    )
    """EnterpriseNode-only v1 scope (ADR-007) — the sole proposal-target column this Business Activity implements."""

    proposed_outcome_description: Mapped[str] = mapped_column(Text, nullable=False)
    """EX-C005-05's own Purpose: "Create a proposed structural outcome". The only field a Refine (EX-C005-06) revision may change."""

    status: Mapped[str] = mapped_column(
        String(20),
        default=StructuralProposalStatus.CREATED.value,
        server_default=StructuralProposalStatus.CREATED.value,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, onupdate=lambda: datetime.now(timezone.utc)
    )
