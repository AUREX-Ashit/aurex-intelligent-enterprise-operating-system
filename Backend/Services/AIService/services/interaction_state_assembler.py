# services/interaction_state_assembler.py
"""
WP-12 BA-02 — Execute Interaction. Implements `InteractionStateAssembler`
(`IMP-001 §13.30`), realizing `RTA-001 §13.15a`'s Interaction State and
Continuity and `ADR-020` Decision 4.

Structural exclusion, not a runtime check: this module has no import of,
and no reference to, any Memory-related repository or model anywhere in
its own source. `SD-001-121`/`ADR-022` Decision 3's own principle —
Conversation Continuity never depends on Enterprise Memory — is enforced
by this file's own dependency graph being unable to reach one, the same
"structural, not runtime-checked" discipline `IMP-001 §13.41`'s
`ExperienceAccountabilityGuard` already establishes for a different
concern. `tests/test_conversation.py::test_state_assembler_has_no_memory_dependency`
verifies this by import-graph inspection, not by exercising a code path.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass

from repositories.conversation_repository import InteractionRepository


@dataclass(frozen=True)
class AssembledInteractionState:
    """Bounded, structured continuity object — never a raw transcript (`ADR-020` Decision 1, as amended)."""
    conversation_id: uuid.UUID
    prior_turn_count: int
    prior_inputs: list[str]
    prior_outputs: list[str]


class InteractionStateAssembler:
    def __init__(self, interaction_repo: InteractionRepository) -> None:
        self.interaction_repo = interaction_repo

    async def assemble(self, *, conversation_id: uuid.UUID, organization_id: uuid.UUID) -> AssembledInteractionState:
        """
        Assembles continuity from prior Interactions in this Conversation only —
        never from any other Conversation, per `ADR-022` Decision 1's Conversation
        boundary. Only COMPLETE prior Interactions contribute; a PENDING or
        FAILED Interaction contributes nothing (its own output is not yet, or
        never, real).
        """
        prior = await self.interaction_repo.list_for_conversation(
            conversation_id=conversation_id, organization_id=organization_id
        )
        complete_prior = [row for row in prior if row.status == "COMPLETE"]
        return AssembledInteractionState(
            conversation_id=conversation_id,
            prior_turn_count=len(complete_prior),
            prior_inputs=[row.input_reference for row in complete_prior],
            prior_outputs=[row.output_reference for row in complete_prior if row.output_reference is not None],
        )
