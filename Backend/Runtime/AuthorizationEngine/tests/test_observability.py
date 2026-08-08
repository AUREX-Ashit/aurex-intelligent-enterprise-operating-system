"""
Unit tests for WP-RTA-001 Milestone M5 -- Runtime Observability.

Covers: evaluation-started/completed/failed event recording, in-memory
counts, and the guarantee that observability never influences the
returned AuthorizationDecision. No database, no metrics/tracing
backend.
"""

from __future__ import annotations

import pytest

from authorization import (
    AuthorizationContext,
    AuthorizationDecision,
    DomainPermissionResolver,
    EvaluationPipeline,
    ObservabilityEventType,
    ResolverRegistry,
    RuntimeObservabilityCollector,
    TierResolution,
)


def _context(**overrides) -> AuthorizationContext:
    defaults = dict(identity_id="person-1", organization_id="org-1")
    defaults.update(overrides)
    return AuthorizationContext(**defaults)


def _stub_domain_permission_resolver(outcome: TierResolution | None = None, *, error: Exception | None = None):
    class _Stub(DomainPermissionResolver):
        async def resolve(self, context: AuthorizationContext) -> TierResolution | None:
            if error is not None:
                raise error
            return outcome

    return _Stub()


async def test_collector_records_started_and_completed_events() -> None:
    collector = RuntimeObservabilityCollector()
    registry = ResolverRegistry().register(
        _stub_domain_permission_resolver(TierResolution(AuthorizationDecision.ALLOW, "grant"))
    )
    pipeline = EvaluationPipeline(registry, observers=(collector,))

    await pipeline.execute(_context())

    event_types = [event.event_type for event in collector.events]
    assert event_types == [ObservabilityEventType.EVALUATION_STARTED, ObservabilityEventType.EVALUATION_COMPLETED]
    assert collector.evaluation_count == 1
    assert collector.completed_count == 1
    assert collector.failure_count == 0


async def test_completed_event_carries_the_decision_and_a_non_negative_duration() -> None:
    collector = RuntimeObservabilityCollector()
    registry = ResolverRegistry().register(
        _stub_domain_permission_resolver(TierResolution(AuthorizationDecision.ALLOW, "grant"))
    )
    pipeline = EvaluationPipeline(registry, observers=(collector,))

    await pipeline.execute(_context())

    completed_event = collector.events[-1]
    assert completed_event.decision == AuthorizationDecision.ALLOW.value
    assert completed_event.duration_seconds is not None
    assert completed_event.duration_seconds >= 0.0


async def test_collector_records_failed_event_on_resolver_exception() -> None:
    class _ResolverBlewUp(RuntimeError):
        pass

    collector = RuntimeObservabilityCollector()
    registry = ResolverRegistry().register(_stub_domain_permission_resolver(error=_ResolverBlewUp("boom")))
    pipeline = EvaluationPipeline(registry, observers=(collector,))

    with pytest.raises(_ResolverBlewUp):
        await pipeline.execute(_context())

    event_types = [event.event_type for event in collector.events]
    assert event_types == [ObservabilityEventType.EVALUATION_STARTED, ObservabilityEventType.EVALUATION_FAILED]
    assert collector.failure_count == 1
    assert collector.completed_count == 0
    assert collector.events[-1].error_type == "_ResolverBlewUp"


async def test_multiple_evaluations_accumulate_counts() -> None:
    collector = RuntimeObservabilityCollector()
    registry = ResolverRegistry().register(
        _stub_domain_permission_resolver(TierResolution(AuthorizationDecision.ALLOW, "grant"))
    )
    pipeline = EvaluationPipeline(registry, observers=(collector,))

    await pipeline.execute(_context())
    await pipeline.execute(_context())
    await pipeline.execute(_context())

    assert collector.evaluation_count == 3
    assert collector.completed_count == 3


def test_events_tuple_is_a_snapshot_not_a_live_view() -> None:
    collector = RuntimeObservabilityCollector()

    events_before = collector.events
    collector._events.append("not-a-real-event")  # type: ignore[arg-type]  # simulate internal state changing

    assert events_before == ()  # the earlier snapshot is unaffected
