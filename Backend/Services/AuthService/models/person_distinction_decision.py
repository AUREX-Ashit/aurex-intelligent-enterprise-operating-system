import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, String, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.database import Base

if TYPE_CHECKING:
    from models.person import Person


class PersonDistinctionDecisionType(str, Enum):
    """WP-07 BA-04 (EX-C006-04). Recognition Authority Rule (PE-001-C006 §1.7)."""
    SELECTED_EXISTING = "SELECTED_EXISTING"
    NEW_PERSON = "NEW_PERSON"


class PersonDistinctionDecision(Base):
    """
    Governed human decision resolving a Candidate Person Context (of any
    size, including exactly one candidate) to exactly one Authoritative
    Person Context or an explicit new-Person decision (WP-07 BA-04,
    EX-C006-04, PE-001-C006 §1.7 / BR-C006-003).

    Audit/traceability record only — not a registered canonical Business
    Object (IRA-007 §5/§9: fails CMD-001 §26.3a's Cross-Experience
    Reference Test and Governed Lifecycle test, the same disposition
    WP-04's own Comparison Context and Downstream Continuation Context
    already established precedent for).
    """

    __tablename__ = "person_distinction_decisions"
    __table_args__ = (
        CheckConstraint(
            "decision_type IN ('SELECTED_EXISTING', 'NEW_PERSON')",
            name="ck_person_distinction_decisions_decision_type",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    candidate_person_ids: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    """The candidate set under consideration, of any size — including exactly one, per the Recognition Authority Rule."""

    decision_type: Mapped[str] = mapped_column(String(20), nullable=False)

    selected_person_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("persons.id"),
        nullable=True,
    )
    """Populated only when decision_type is SELECTED_EXISTING."""

    rationale: Mapped[str] = mapped_column(Text, nullable=False)
    """BR-C006-003: every distinguish decision SHALL record why one candidate was selected, or why none were."""

    decided_by: Mapped[str | None] = mapped_column(String(255), nullable=True)

    decided_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    selected_person: Mapped["Person | None"] = relationship("Person", foreign_keys=[selected_person_id])
