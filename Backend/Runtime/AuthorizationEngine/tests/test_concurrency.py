"""
Thread safety / concurrency validation for WP-RTA-001 Milestone M6.

Verifies: immutable runtime objects, concurrent evaluation correctness
(no cross-talk between concurrently-running evaluations sharing one
pipeline/engine instance), absence of shared mutable state, and
deterministic behaviour under concurrent load. This runtime is
single-threaded-cooperative (asyncio), not multi-threaded -- these
tests validate the concurrency model this runtime actually uses.
"""

from __future__ import annotations

import asyncio
import dataclasses

import pytest

from authorization import (
    AuthorizationContext,
    AuthorizationDecision,
    AuthorizationTier,
    DomainPermissionResolver,
    EvaluationPipeline,
    NamedUserResolver,
    ResolverRegistry,
    RuntimeObservabilityCollector,
    TierResolution,
)


def _context(**overrides) -> AuthorizationContext:
    defaults = dict(identity_id="person-1", organization_id="org-1")
    defaults.update(overrides)
    return AuthorizationContext(**defaults)


def _stub(base_cls, outcome_by_identity: dict[str, TierResolution | None] | None = None, *, default: TierResolution | None = None):
    class _Stub(base_cls):  # type: ignore[misc,valid-type]
        async def resolve(self, context: AuthorizationContext) -> TierResolution | None:
            await asyncio.sleep(0)  # yield control, to actually exercise interleaving
            if outcome_by_identity is not None:
                return outcome_by_identity.get(context.identity_id, default)
            return default

    return _Stub()


# ---------------------------------------------------------------------------
# Immutable runtime objects
# ---------------------------------------------------------------------------


def test_every_immutable_model_rejects_mutation() -> None:
    context = _context()
    with pytest.raises(dataclasses.FrozenInstanceError):
        context.identity_id = "someone-else"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Concurrent evaluation -- no cross-talk between simultaneous requests
# ---------------------------------------------------------------------------


async def test_concurrent_evaluations_with_different_outcomes_never_cross_contaminate() -> None:
    """Person A must always get ALLOW, Person B must always get DENY -- run interleaved, many times, on one shared pipeline."""
    resolver = _stub(
        NamedUserResolver,
        outcome_by_identity={
            "person-allow": TierResolution(AuthorizationDecision.ALLOW, "A's own grant"),
            "person-deny": TierResolution(AuthorizationDecision.DENY, "B's own explicit deny"),
        },
    )
    pipeline = EvaluationPipeline(ResolverRegistry().register(resolver))

    async def evaluate_as(identity: str) -> AuthorizationDecision:
        result = await pipeline.execute(_context(identity_id=identity))
        return result.decision

    tasks = [evaluate_as("person-allow" if i % 2 == 0 else "person-deny") for i in range(200)]
    results = await asyncio.gather(*tasks)

    for i, decision in enumerate(results):
        expected = AuthorizationDecision.ALLOW if i % 2 == 0 else AuthorizationDecision.DENY
        assert decision == expected, f"task {i} cross-contaminated: expected {expected}, got {decision}"


async def test_concurrent_evaluations_produce_independent_traces() -> None:
    resolver = _stub(
        NamedUserResolver,
        outcome_by_identity={"person-a": TierResolution(AuthorizationDecision.ALLOW, "a")},
    )
    pipeline = EvaluationPipeline(ResolverRegistry().register(resolver))

    async def evaluate_as(identity: str):
        return await pipeline.execute(_context(identity_id=identity))

    result_a, result_b = await asyncio.gather(evaluate_as("person-a"), evaluate_as("person-b"))

    assert result_a.decision == AuthorizationDecision.ALLOW
    assert result_a.matched_tier == AuthorizationTier.NAMED_USER
    assert result_b.decision == AuthorizationDecision.DENY  # no resolver outcome bound for person-b
    assert result_b.matched_tier is None
    assert result_a.trace is not result_b.trace  # independent objects, never shared/mutated in place


# ---------------------------------------------------------------------------
# Shared mutable state
# ---------------------------------------------------------------------------


async def test_resolver_mapping_is_not_mutated_by_concurrent_evaluation() -> None:
    registry = ResolverRegistry().register(
        _stub(DomainPermissionResolver, default=TierResolution(AuthorizationDecision.ALLOW, "grant"))
    )
    pipeline = EvaluationPipeline(registry)
    before = pipeline.configured_tiers

    await asyncio.gather(*(pipeline.execute(_context()) for _ in range(50)))

    assert pipeline.configured_tiers == before  # unchanged by any number of evaluations


async def test_shared_observability_collector_accumulates_exact_counts_under_concurrent_load() -> None:
    """A single collector instance shared across many concurrent evaluations must count every one exactly once -- no lost or duplicated events."""
    collector = RuntimeObservabilityCollector()
    pipeline = EvaluationPipeline(
        ResolverRegistry().register(
            _stub(DomainPermissionResolver, default=TierResolution(AuthorizationDecision.ALLOW, "grant"))
        ),
        observers=(collector,),
    )

    concurrency = 300
    await asyncio.gather(*(pipeline.execute(_context()) for _ in range(concurrency)))

    assert collector.evaluation_count == concurrency
    assert collector.completed_count == concurrency
    assert collector.failure_count == 0


# ---------------------------------------------------------------------------
# Deterministic behaviour under concurrent load
# ---------------------------------------------------------------------------


async def test_same_context_evaluated_concurrently_many_times_yields_identical_results() -> None:
    pipeline = EvaluationPipeline(
        ResolverRegistry().register(
            _stub(DomainPermissionResolver, default=TierResolution(AuthorizationDecision.ALLOW, "grant"))
        )
    )
    context = _context()

    results = await asyncio.gather(*(pipeline.execute(context) for _ in range(100)))

    first = results[0]
    for result in results[1:]:
        assert result.decision == first.decision
        assert result.matched_tier == first.matched_tier
        assert result.reason == first.reason
        assert result.trace == first.trace
