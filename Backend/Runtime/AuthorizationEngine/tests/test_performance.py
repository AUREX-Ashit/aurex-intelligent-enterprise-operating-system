"""
Performance validation for WP-RTA-001 Milestone M6.

Sanity benchmarks with deliberately generous thresholds -- this is
pure in-memory Python logic with no I/O, so even a heavily-loaded CI
machine should clear these by a wide margin. The purpose is regression
detection (something becoming pathologically slow), not micro-
optimization; "No optimization is required unless a genuine issue is
found" (instruction), and none was found -- see measured results in
IMP-REPORT-WP-RTA-001 M6.
"""

from __future__ import annotations

import time

from authorization import (
    AuthorizationContext,
    AuthorizationDecision,
    DomainPermissionResolver,
    EvaluationPipeline,
    ResolverRegistry,
    TierResolution,
)


def _context(**overrides) -> AuthorizationContext:
    defaults = dict(identity_id="person-1", organization_id="org-1")
    defaults.update(overrides)
    return AuthorizationContext(**defaults)


def _stub_domain_permission_resolver(outcome: TierResolution | None):
    class _Stub(DomainPermissionResolver):
        async def resolve(self, context: AuthorizationContext) -> TierResolution | None:
            return outcome

    return _Stub()


async def test_single_evaluation_completes_quickly() -> None:
    pipeline = EvaluationPipeline(
        ResolverRegistry().register(
            _stub_domain_permission_resolver(TierResolution(AuthorizationDecision.ALLOW, "grant"))
        )
    )

    started = time.perf_counter()
    result = await pipeline.execute(_context())
    elapsed = time.perf_counter() - started

    assert result.decision == AuthorizationDecision.ALLOW
    assert elapsed < 0.5, f"single evaluation took {elapsed:.4f}s -- unexpectedly slow for pure in-memory logic"


async def test_repeated_sequential_evaluations_stay_fast() -> None:
    pipeline = EvaluationPipeline(
        ResolverRegistry().register(
            _stub_domain_permission_resolver(TierResolution(AuthorizationDecision.ALLOW, "grant"))
        )
    )
    context = _context()
    iterations = 2000

    started = time.perf_counter()
    for _ in range(iterations):
        await pipeline.execute(context)
    elapsed = time.perf_counter() - started

    per_call = elapsed / iterations
    assert elapsed < 3.0, f"{iterations} sequential evaluations took {elapsed:.4f}s ({per_call * 1000:.4f}ms/call)"


async def test_pipeline_construction_is_cheap() -> None:
    """Assembly (ResolverOrchestrator + AuthorizationEngine construction) should not be a bottleneck."""
    registry = ResolverRegistry().register(
        _stub_domain_permission_resolver(TierResolution(AuthorizationDecision.ALLOW, "grant"))
    )

    started = time.perf_counter()
    for _ in range(1000):
        EvaluationPipeline(registry)
    elapsed = time.perf_counter() - started

    assert elapsed < 1.0, f"1000 pipeline constructions took {elapsed:.4f}s"


async def test_worst_case_all_five_tiers_not_evaluated_stays_fast() -> None:
    """The zero-resolver-bound path walks all five tiers with no work per tier -- the cheapest possible evaluation, sanity-checked for overhead."""
    pipeline = EvaluationPipeline(ResolverRegistry())
    context = _context()

    started = time.perf_counter()
    for _ in range(5000):
        await pipeline.execute(context)
    elapsed = time.perf_counter() - started

    assert elapsed < 3.0, f"5000 empty-registry evaluations took {elapsed:.4f}s"


async def test_resolver_execution_overhead_is_negligible() -> None:
    """Isolates a single resolver's own call overhead from the rest of the pipeline."""
    resolver = _stub_domain_permission_resolver(TierResolution(AuthorizationDecision.ALLOW, "grant"))
    context = _context()

    started = time.perf_counter()
    for _ in range(5000):
        await resolver.resolve(context)
    elapsed = time.perf_counter() - started

    assert elapsed < 1.0, f"5000 direct resolver calls took {elapsed:.4f}s"
