import uuid
from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import CheckConstraint, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from models.database import Base


class StructuralChangeIntentStatus(str, Enum):
    """
    IRA-004 §21's own registered Lifecycle Model for SCI-000001
    (Structural Change Intent): CREATED (EX-C005-04) -> MODIFIED ->
    SUPERSEDED or ABANDONED (EX-C005-04's own Invalidated Context) ->
    WITHDRAWN (PE-001-C005 §43.3's distinct exception-semantics path)
    -> ARCHIVED (SD-002-008's terminal state).

    WP-04 BA-03 ("Frame Structural Change Intent") realizes only the
    CREATED transition, mirroring BA-01's own disclosed minimal-slice
    precedent (IRA-004 §5: BA-01 did not implement BR-C005-001-010's
    full governed-transition workflow either). The full enum is
    declared here — not invented, but read directly off IRA-004 §21's
    own registration entry — so the column's constraint reflects
    SCI-000001's actual registered lifecycle; no code path in this
    Business Activity ever sets a value other than CREATED (TD, see
    IMP-REPORT-WP-04).
    """
    CREATED = "CREATED"
    MODIFIED = "MODIFIED"
    SUPERSEDED = "SUPERSEDED"
    ABANDONED = "ABANDONED"
    WITHDRAWN = "WITHDRAWN"
    ARCHIVED = "ARCHIVED"


class StructuralChangeIntent(Base):
    """
    Structural Change Intent — the canonical Business Object SCI-000001
    (ADR-006; IRA-004 §21, CMD-001 §26.3/§26.4), realizing PE-001-C005's
    ERB-C005-03 ("Frame Structural Change Intent") / EX-C005-04.

    Aggregate Root in its own right (IRA-004 §21's own "Aggregate Root"
    attribute) — not a sub-object of EnterpriseNode/EnterpriseRelationship.
    Deliberately carries no FK to `organization_nodes` or any future
    `organization_hierarchy` row: EX-C005-04's own Required Context is
    "Structural Understanding Context and recognized change need", not a
    bound structural target — the `DERIVED_FROM` EnterpriseNode/
    EnterpriseRelationship relationship (IRA-004 §21's Relationship
    Mapping) is explicit Pending Canonical Binding, resolved (if at all)
    by a future BA-04 ("Shape Structural Proposal", EX-C005-05, whose own
    Required Context is "Change Intent Context AND current structural
    context" — the structural target is supplied at that later stage,
    not carried forward from this one). Binding a structural target here
    would absorb BA-04's own scope, which this Business Activity does
    not do.

    Also carries no `organization_id`: like `organization_nodes`
    (IRA-004 §9), this is an enterprise-structure-level construct, not
    organization-scoped data (see `middleware/tenant.py`'s exemption for
    this router's own prefix).
    """

    __tablename__ = "structural_change_intents"
    __table_args__ = (
        CheckConstraint(
            "status IN ('CREATED', 'MODIFIED', 'SUPERSEDED', 'ABANDONED', 'WITHDRAWN', 'ARCHIVED')",
            name="ck_structural_change_intents_status",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    change_rationale: Mapped[str] = mapped_column(Text, nullable=False)
    """EX-C005-04's own Required/Consumed Context: "recognized change need" — the business rationale for the structural change, in the persona's own words."""

    target_outcome: Mapped[str] = mapped_column(Text, nullable=False)
    """EX-C005-04's own Produced Context: "target outcome" — the intended structural result, expressed as enterprise intent, not yet a Proposed Outcome Context (BA-04's own scope)."""

    decision_boundary: Mapped[str | None] = mapped_column(Text, nullable=True)
    """EX-C005-04's own Produced Context: "decision boundary" — optional constraints/limits on the change (e.g. what must NOT change). Optional: EX-C005-04's text does not mark this a mandatory input, unlike change_rationale/target_outcome."""

    status: Mapped[str] = mapped_column(
        String(20),
        default=StructuralChangeIntentStatus.CREATED.value,
        server_default=StructuralChangeIntentStatus.CREATED.value,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, onupdate=lambda: datetime.now(timezone.utc)
    )
