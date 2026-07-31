import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.database import Base

if TYPE_CHECKING:
    from models.person import Person

CORRECTABLE_FIELDS = ("first_name", "last_name", "display_name")


class PersonCorrection(Base):
    """
    Correction Context for an inaccurate Authoritative Person fact (WP-07
    BA-07, EX-C006-07, BR-C006-006). Preserves the pre-correction value
    permanently in traceability — a correction is never a silent
    overwrite (PE-001-C006 §5.1).

    Audit/traceability record only — not a registered canonical Business
    Object (IRA-007 §5/§9).
    """

    __tablename__ = "person_corrections"
    __table_args__ = (
        CheckConstraint(
            "field_name IN ('first_name', 'last_name', 'display_name')",
            name="ck_person_corrections_field_name",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    person_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("persons.id", ondelete="CASCADE"), nullable=False, index=True)

    field_name: Mapped[str] = mapped_column(String(50), nullable=False)

    prior_value: Mapped[str] = mapped_column(Text, nullable=False)
    """The pre-correction value, preserved permanently even though it is simultaneously superseded (PE-001-C006 §3.6 — the two are not mutually exclusive)."""

    corrected_value: Mapped[str] = mapped_column(Text, nullable=False)

    reason: Mapped[str] = mapped_column(Text, nullable=False)

    approval_reference: Mapped[str | None] = mapped_column(String(255), nullable=True)
    """Free-text, mirroring every other authorization-policy object's own approval_reference field in this codebase (Contract 5.3-class runtime-execution boundary — this capability never executes an approval workflow itself)."""

    corrected_by: Mapped[str | None] = mapped_column(String(255), nullable=True)

    corrected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    person: Mapped["Person"] = relationship("Person")
