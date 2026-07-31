import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.database import Base

if TYPE_CHECKING:
    from models.person import Person

SENSITIVITY_CLASSIFICATIONS = ("PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED")
"""CMD-001 §26.4's own Security Classification vocabulary, reused verbatim rather than inventing a capability-local one."""


class PersonEnrichment(Base):
    """
    Enrichment Context — legitimate new detail added to a Person's
    Authoritative Person Context (WP-07 BA-08, EX-C006-08, BR-C006-007).
    Additive only; never overwrites an existing fact (a contradicting
    candidate is redirected to correction, not treated as enrichment,
    per PE-001-C006 §3.7/§5.1).

    A generic attribute_name/attribute_value pair, not a fixed new
    column on Person: Person's own schema (first_name/last_name/
    display_name) has no other structured field for a specific
    enrichment to target, and this Work Package does not extend that
    schema speculatively ahead of a real, concrete consumer (IRA-007
    §10, item 5 — mirrors ADR-004's own incremental-implementation
    precedent).

    Audit/traceability record only — not a registered canonical Business
    Object (IRA-007 §5/§9).
    """

    __tablename__ = "person_enrichments"
    __table_args__ = (
        CheckConstraint(
            "sensitivity_classification IN ('PUBLIC', 'INTERNAL', 'CONFIDENTIAL', 'RESTRICTED')",
            name="ck_person_enrichments_sensitivity_classification",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    person_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("persons.id", ondelete="CASCADE"), nullable=False, index=True)

    attribute_name: Mapped[str] = mapped_column(String(255), nullable=False)

    attribute_value: Mapped[str] = mapped_column(Text, nullable=False)

    source: Mapped[str] = mapped_column(String(255), nullable=False)
    """Attributable provenance — required (PE-001-C006 §5.1: "an enrichment SHALL be additive and attributable to a source")."""

    sensitivity_classification: Mapped[str] = mapped_column(String(20), nullable=False)

    accepted_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    """Explicit human acceptance — EX-C006-08 completes only on explicit acceptance, never silently."""

    accepted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    person: Mapped["Person"] = relationship("Person")
