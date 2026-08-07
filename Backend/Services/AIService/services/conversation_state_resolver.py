# services/conversation_state_resolver.py
"""
WP-12 — AI Conversation Management (C-094). Implements `ConversationStateResolver`
(`IMP-001 §13.29`), realizing `RTA-001 §13.15a`'s Conversation State Model and
`ADR-020` Decision 2's own separation: the state model and its transition
triggers are two independently injected concerns, never merged into one class.

This resolver decides WHETHER a transition is valid given a trigger. It never
originates a transition itself, and it never performs the write (`repositories
/conversation_repository.py::transition_state` does that, only after this
resolver has approved the transition).
"""
from __future__ import annotations

from enum import Enum


class ConversationTransitionTrigger(str, Enum):
    """The only two trigger kinds `ADR-020` Decision 2 permits — never a default."""
    EXPLICIT_ACTION = "EXPLICIT_ACTION"
    RUNTIME_POLICY = "RUNTIME_POLICY"


class InvalidConversationTransition(Exception):
    """Raised when a requested transition has no valid trigger, or the Conversation is already in the target state."""


class ConversationStateResolver:
    """
    `resolve(current_state, trigger) -> new_state`. Stateless — takes the
    Conversation's own current state and an explicit trigger, returns the
    resulting state. Never reads or writes the database itself.
    """

    _VALID_TRANSITIONS: dict[str, set[str]] = {
        "OPEN": {"CLOSED"},
        "CLOSED": set(),  # terminal for this Work Package's own scope (TDS-012 §2) — no reopen path
    }

    def resolve(self, current_state: str, target_state: str, trigger: ConversationTransitionTrigger) -> str:
        if trigger not in ConversationTransitionTrigger:
            raise InvalidConversationTransition(
                f"Transition rejected: '{trigger}' is not a recognized trigger. "
                "A Conversation state transition SHALL originate only from an explicit action "
                "or an evaluated Runtime Policy (ADR-020 Decision 2) — never a default."
            )
        allowed_targets = self._VALID_TRANSITIONS.get(current_state, set())
        if target_state not in allowed_targets:
            raise InvalidConversationTransition(
                f"Transition rejected: '{current_state}' -> '{target_state}' is not a valid "
                f"Conversation state transition (RTA-001 §13.15a Conversation State Model)."
            )
        return target_state
