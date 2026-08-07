# models/conversation.py
"""
WP-12 — AI Conversation Management (C-094). Physical schema per `TDS-012 §4`,
instantiating the Business Object relationship `ADR-020` Clarifications 1-2
already decided: `ConversationModel` realizes the registered "AI Conversation"
Business Object (`CMD-001 §24.4`); `InteractionModel` is its decomposition
element, not a separately registered Business Object, mirroring how
`AI Recommendation` decomposes into `recommendation`/`recommendation_context`/
`recommendation_feedback`/`recommendation_audit`.

`organization_id` is a plain UUID column, not a database-level `ForeignKey` —
same reasoning as `models/search.py`'s own module docstring: the owning table
lives in `AuthService`'s own database, a separate service boundary
(`CLAUDE.md §8`). Enforced by the caller's own verified JWT `organization_id`
claim (`dependencies.get_current_claims`), not a physical constraint this
service's own database can express.
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from models.database import Base


class ConversationModel(Base):
    """
    `conversation_registry`. Realizes the registered "AI Conversation"
    Business Object (`CMD-001 §24.4`) and the Conversation construct
    (`RTA-001 §13.15a`, `ADR-020` Decisions 1-2). Durable business context;
    owns no presentation contract of its own (`ADR-022`/`SD-001-121`).

    WP-12 BA-01 (Establish and Manage Conversation Lifecycle) writes this
    table.
    """

    __tablename__ = "conversation_registry"
    __table_args__ = (
        CheckConstraint(
            "state IN ('OPEN', 'CLOSED')",
            name="ck_conversation_registry_state",
        ),
        CheckConstraint(
            "state_transition_reason IN ('EXPLICIT_ACTION', 'RUNTIME_POLICY') OR state_transition_reason IS NULL",
            name="ck_conversation_registry_state_transition_reason",
        ),
    )

    conversation_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    organization_id: Mapped[uuid.UUID] = mapped_column(nullable=False, index=True)
    """Logical, not physical, FK to organization_master — see module docstring."""

    established_by: Mapped[uuid.UUID] = mapped_column(nullable=False)
    """person_id — the accountability anchor's own originating caller, per RTA-001 §13.2/§13.3. Logical FK, same reasoning as organization_id."""

    state: Mapped[str] = mapped_column(String(10), nullable=False, default="OPEN", server_default="OPEN")
    """RTA-001 §13.15a Conversation State Model. Transitions only via ConversationStateResolver (ADR-020 Decision 2) — never a default."""

    state_transitioned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    state_transition_reason: Mapped[str | None] = mapped_column(String(20), nullable=True)
    """Populated only on transition to CLOSED — EXPLICIT_ACTION or RUNTIME_POLICY (ADR-020 Decision 2). NULL while OPEN (initial state, no transition yet)."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class InteractionModel(Base):
    """
    `interaction_registry`. Decomposition element of the Conversation
    Business Object (`ADR-020` Clarification 1) — not independently
    registered. Realizes Interaction (`RTA-001 §13.15a`) — one bounded AI
    Request Lifecycle. Identity, ordering, and accountability preserved
    per `ADR-022` Decision 1/`SD-001-119`.

    WP-12 BA-02 (Execute Interaction) writes this table; BA-03 (Retrieve
    Conversation) reads it, ordered by `sequence_number`.
    """

    __tablename__ = "interaction_registry"
    __table_args__ = (
        UniqueConstraint("conversation_id", "sequence_number", name="uq_interaction_registry_conversation_sequence"),
        CheckConstraint(
            "status IN ('PENDING', 'COMPLETE', 'FAILED')",
            name="ck_interaction_registry_status",
        ),
    )

    interaction_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    conversation_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("conversation_registry.conversation_id", ondelete="CASCADE"), nullable=False, index=True
    )
    sequence_number: Mapped[int] = mapped_column(Integer, nullable=False)
    """Per-Conversation ordering (ADR-022 Decision 1). Structural uniqueness enforced via the table's own UniqueConstraint, not application convention alone — mirrors the (organization_id, index_name) precedent TD-128 recommended for WP-11, applied here from the start."""

    business_activity_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    """Accountability anchor, per SD-001-114/ADR-021 Decision 2 — Business Activity accountability, never the Conversation's own."""

    status: Mapped[str] = mapped_column(String(10), nullable=False, default="PENDING", server_default="PENDING")

    input_reference: Mapped[str] = mapped_column(String(4000), nullable=False)
    output_reference: Mapped[str | None] = mapped_column(String(8000), nullable=True)

    confidence_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    """Evidence Panel input (IMP-001 §10.4), populated once status=COMPLETE. Real, not stub, per IRA-012 §4.4's own first-implementation finding."""
    evidence_reference: Mapped[str | None] = mapped_column(String(2000), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    organization_id: Mapped[uuid.UUID] = mapped_column(nullable=False, index=True)
    """Denormalized from the parent Conversation for direct tenant-isolation filtering without a join on every read (CLAUDE.md §21.4)."""


class InteractionPromptExecutionModel(Base):
    """
    `interaction_prompt_execution`. Join table realizing the containment
    relationship `ADR-020` Clarification 2 already decided: an Interaction
    may invoke a Reasoning Engine more than once (`RTA-001 §13.9b`,
    "Multi-LLM delegation within one execution"), each producing its own
    Prompt Execution record (`CMD-001 §24.4`, already registered).

    No FK to a `prompt_execution` table is declared here — Prompt
    Execution's own physical schema is not part of WP-12's own scope
    (it belongs to whichever Work Package first implements `RTA-001
    §13.8`/`§13.9c` for real); `prompt_execution_id` is recorded as a
    plain identifier, logical reference only, the same pattern
    `models/search.py`'s own `confidence_rule_id` already establishes for
    an out-of-scope sibling construct.
    """

    __tablename__ = "interaction_prompt_execution"

    interaction_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("interaction_registry.interaction_id", ondelete="CASCADE"), primary_key=True
    )
    prompt_execution_id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
