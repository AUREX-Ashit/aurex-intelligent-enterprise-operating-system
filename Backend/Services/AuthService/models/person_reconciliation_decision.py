import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.database import Base

if TYPE_CHECKING:
    from models.person import Person


class PersonReconciliationOutcome(str, Enum):
    """WP-07 BA-06 (EX-C006-06). PE-001-C006 §5.3 Potential Duplicate Context Contract."""
    CONFIRMED_DUPLICATE = "CONFIRMED_DUPLICATE"
    CONFIRMED_DISTINCT = "CONFIRMED_DISTINCT"
    ESCALATED = "ESCALATED"


class PersonReconciliationDecision(Base):
    """
    Governed Reconciliation Decision for two Person contexts suspected of
    representing the same physical human (WP-07 BA-06, EX-C006-06,
    BR-C006-005). Never a silent merge — this record is the decision
    itself; any technical consolidation following a confirmed-duplicate
    decision is a downstream data-governance action outside this
    Enterprise Experience's own scope (PE-001-C006 §5.3).

    Audit/traceability record only — not a registered canonical Business
    Object (IRA-007 §5/§9), same disposition as PersonDistinctionDecision.
    """

    __tablename__ = "person_reconciliation_decisions"
    __table_args__ = (
        CheckConstraint(
            "decision IN ('CONFIRMED_DUPLICATE', 'CONFIRMED_DISTINCT', 'ESCALATED')",
            name="ck_person_reconciliation_decisions_decision",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    person_id_a: Mapped[uuid.UUID] = mapped_column(ForeignKey("persons.id"), nullable=False, index=True)
    person_id_b: Mapped[uuid.UUID] = mapped_column(ForeignKey("persons.id"), nullable=False, index=True)

    decision: Mapped[str] = mapped_column(String(30), nullable=False)

    rationale: Mapped[str] = mapped_column(Text, nullable=False)

    reviewed_by: Mapped[str | None] = mapped_column(String(255), nullable=True)

    reviewed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    person_a: Mapped["Person"] = relationship("Person", foreign_keys=[person_id_a])
    person_b: Mapped["Person"] = relationship("Person", foreign_keys=[person_id_b])
