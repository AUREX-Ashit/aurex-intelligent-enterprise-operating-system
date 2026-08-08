"""
Runtime Observability (WP-RTA-001 M5).

A concrete PipelineObserver (M3's own extension seam,
`authorization.pipeline.PipelineObserver`) recording
evaluation-started / evaluation-completed / evaluation-failed events.
In-memory only -- no persistence, no metrics backend, no tracing
backend (explicitly out of this milestone's scope; a real backend
integration is a future, separately-scoped concern).

Realizes a first, self-contained slice of RTA-001 S11.15's own
telemetry set: Authorization Resolution Time (per-event duration),
Permission Evaluation Count (`evaluation_count`), Authorization
Failures (`failure_count`). The remaining S11.15 metrics (Assignment
Resolution Time, Delegation Usage, Approval Authority Evaluations,
Cache Hit Ratio, Policy Evaluation Time) require data this Work
Package does not yet produce -- real Assignment/Delegation/
Approval-Authority resolution and Caching are both M6.

Never influences an AuthorizationDecision -- PipelineObserver's own
method signatures return None, and this class only ever appends to its
own private, internal event list. Observability is passive by
construction, not by convention alone.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from enum import Enum

from .models import EvaluationResult
from .pipeline import PipelineExecution


class ObservabilityEventType(str, Enum):
    EVALUATION_STARTED = "EVALUATION_STARTED"
    EVALUATION_COMPLETED = "EVALUATION_COMPLETED"
    EVALUATION_FAILED = "EVALUATION_FAILED"


@dataclass(frozen=True)
class ObservabilityEvent:
    """One recorded runtime event. Immutable, in-memory only, never persisted."""

    event_type: ObservabilityEventType
    execution_id: str
    duration_seconds: float | None = None
    decision: str | None = None
    error_type: str | None = None


class RuntimeObservabilityCollector:
    """
    Concrete PipelineObserver realizing Runtime Observability.
    Constructor-free (no dependencies) -- a caller simply passes an
    instance to `EvaluationPipeline(registry, observers=(collector,))`.
    """

    def __init__(self) -> None:
        self._events: list[ObservabilityEvent] = []
        self._started_at: dict[str, float] = {}

    @property
    def events(self) -> tuple[ObservabilityEvent, ...]:
        return tuple(self._events)

    @property
    def evaluation_count(self) -> int:
        return sum(1 for e in self._events if e.event_type == ObservabilityEventType.EVALUATION_STARTED)

    @property
    def completed_count(self) -> int:
        return sum(1 for e in self._events if e.event_type == ObservabilityEventType.EVALUATION_COMPLETED)

    @property
    def failure_count(self) -> int:
        return sum(1 for e in self._events if e.event_type == ObservabilityEventType.EVALUATION_FAILED)

    # -- PipelineObserver protocol ------------------------------------

    def on_start(self, execution: PipelineExecution) -> None:
        self._started_at[execution.execution_id] = time.monotonic()
        self._events.append(
            ObservabilityEvent(ObservabilityEventType.EVALUATION_STARTED, execution.execution_id)
        )

    def on_complete(self, execution: PipelineExecution, result: EvaluationResult) -> None:
        self._events.append(
            ObservabilityEvent(
                ObservabilityEventType.EVALUATION_COMPLETED,
                execution.execution_id,
                duration_seconds=self._duration_since_start(execution.execution_id),
                decision=result.decision.value,
            )
        )

    def on_error(self, execution: PipelineExecution, error: Exception) -> None:
        self._events.append(
            ObservabilityEvent(
                ObservabilityEventType.EVALUATION_FAILED,
                execution.execution_id,
                duration_seconds=self._duration_since_start(execution.execution_id),
                error_type=type(error).__name__,
            )
        )

    def _duration_since_start(self, execution_id: str) -> float | None:
        started = self._started_at.pop(execution_id, None)
        if started is None:
            return None
        return time.monotonic() - started
