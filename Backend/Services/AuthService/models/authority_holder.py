import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, String, DateTime, Integer, ForeignKey, Index, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.database import Base

if TYPE_CHECKING:
    from models.person import Person


class AuthorityHolderStatus(str, Enum):
    """
    TDS-017 §23's own minimum lifecycle — ACTIVE (the current accountability
    point) or SUPERSEDED (a preserved prior version, never deleted). No
    DEPRECATED/RETIRED value is added here — TDS-017 §23 specifies only
    these two, and constitutional tenure/revocation rules that might
    warrant a richer state set remain explicitly future governance work
    (TDS-017 §25), not invented by this implementation.
    """
    ACTIVE = "ACTIVE"
    SUPERSEDED = "SUPERSEDED"


class AuthorityHolder(Base):
    """
    Runtime holder record for a C-040 constitutional authority (AI-001,
    AI-002), realizing TDS-017 §23's own design exactly.

    Deliberately carries NO organization_id column of any kind — this is
    the entire point of this table's own existence (TDS-017 §5/§8/§23):
    approval_authorities and runtime_assignment_policies both require
    organization_id NOT NULL, structurally incompatible with a platform-
    wide, pre-Organization authority (ADR-031 §8). This table is a runtime
    implementation source of truth; it is not, and does not replace, the
    Appointment Instrument that authorizes each row's own creation
    (TDS-017 §24) — appointment_instrument_ref cites that document, it
    never embeds or supersedes it.

    No constitutional tenure, succession, or revocation rule is invented
    by this model's own existence — it records who currently holds an
    already-appointed authority; it does not decide when a change should
    occur (TDS-017 §25, ADR-031 §13, AI-001 §10, both left explicitly
    open and not touched here).
    """

    __tablename__ = "authority_holders"
    __table_args__ = (
        CheckConstraint(
            "authority_identity IN ('AI-001', 'AI-002')",
            name="ck_authority_holders_authority_identity",
        ),
        CheckConstraint(
            "status IN ('ACTIVE', 'SUPERSEDED')",
            name="ck_authority_holders_status",
        ),
        # Active-holder uniqueness/concurrency protection (TDS-017 §23):
        # at most one ACTIVE row per authority_identity at any time.
        # Cross-dialect partial unique index — postgresql_where for the
        # real target platform (Master_Technical_Architecture.md's own
        # PostgreSQL standard, CLAUDE.md §9), sqlite_where for this
        # repository's own in-memory SQLite test harness (conftest.py).
        Index(
            "ux_authority_holders_active_authority",
            "authority_identity",
            unique=True,
            postgresql_where=text("status = 'ACTIVE'"),
            sqlite_where=text("status = 'ACTIVE'"),
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    authority_identity: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True
    )
    """'AI-001' or 'AI-002' — which constitutional authority this row concerns."""

    holder_person_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("persons.id"),
        nullable=False,
        index=True
    )
    """The appointed accountability point's own Person identity (AuthService.persons.id)."""

    appointment_instrument_ref: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    """
    Citation only (e.g. "AI-003") — the governance document that
    authorized this row. Never embeds or restates the Instrument's own
    content; this table remains the runtime source of truth, the
    Instrument remains the governance source of truth (TDS-017 §24).
    """

    version: Mapped[int] = mapped_column(
        Integer,
        default=1,
        server_default="1"
    )
    """SD-002-011 Version property."""

    status: Mapped[str] = mapped_column(
        String(20),
        default=AuthorityHolderStatus.ACTIVE.value,
        server_default=AuthorityHolderStatus.ACTIVE.value,
    )
    """SD-002-011 Status property (AuthorityHolderStatus)."""

    effective_from: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    """SD-002-011 Effective From property."""

    effective_to: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    """SD-002-011 Effective To property. NULL while this version remains current."""

    supersedes_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("authority_holders.id"),
        nullable=True
    )
    """Prior-version link, mirroring approval_authorities's own established pattern."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    holder_person: Mapped["Person"] = relationship("Person", foreign_keys=[holder_person_id])
    supersedes: Mapped["AuthorityHolder | None"] = relationship(
        "AuthorityHolder", remote_side=[id], foreign_keys=[supersedes_id], backref="superseded_by_one"
    )
