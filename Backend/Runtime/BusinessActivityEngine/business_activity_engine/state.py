"""
Business Activity Engine -- canonical execution-state vocabulary (WP-BAE-001 M1).

The nine canonical states (`IMP-001 §6.18.4`, names verbatim) and the
ten transitions `§6.18.6` lists. Nothing else.

This is vocabulary, not a state machine. The M1 engine does not drive
execution state: a pre-`Running` termination (unregistered activity,
authorization denial) would need a transition no authoritative source
defines (`IRA-BAE-001-M1 §11.2`, U-01/U-02). The full transition set,
terminal classification, and durable execution state are deferred to
M5/M6 (`RO-M1-07`, `RO-M1-08`) -- no transition is invented here.
"""

from __future__ import annotations

from enum import Enum


class ExecutionState(str, Enum):
    """`IMP-001 §6.18.4` canonical execution states."""

    CREATED = "CREATED"
    READY = "READY"
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    SUSPENDED = "SUSPENDED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    ROLLED_BACK = "ROLLED_BACK"


AUTHORITATIVE_TRANSITIONS: frozenset[tuple[ExecutionState, ExecutionState]] = frozenset(
    {
        (ExecutionState.CREATED, ExecutionState.READY),
        (ExecutionState.READY, ExecutionState.RUNNING),
        (ExecutionState.RUNNING, ExecutionState.WAITING),
        (ExecutionState.WAITING, ExecutionState.RUNNING),
        (ExecutionState.RUNNING, ExecutionState.SUSPENDED),
        (ExecutionState.SUSPENDED, ExecutionState.RUNNING),
        (ExecutionState.RUNNING, ExecutionState.COMPLETED),
        (ExecutionState.RUNNING, ExecutionState.FAILED),
        (ExecutionState.RUNNING, ExecutionState.CANCELLED),
        (ExecutionState.FAILED, ExecutionState.ROLLED_BACK),
    }
)
"""`IMP-001 §6.18.6` "Permitted examples", verbatim. Any other pair is unsupported until decided (U-01–U-10)."""
