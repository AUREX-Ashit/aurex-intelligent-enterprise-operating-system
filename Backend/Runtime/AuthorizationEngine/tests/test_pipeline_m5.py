"""
Unit tests for WP-RTA-001 Milestone M5 -- EvaluationPipeline integration.

Covers: Enterprise Scope Validation wired into EvaluationPipeline
before AuthorizationEngine is ever invoked, observer failure
isolation, and deterministic execution with both M5 features active.
"""

from __future__ import annotations

import pytest

from authorization import (
    AuthorizationContext,
    AuthorizationDecision,
    AuthorizationTier,
    DomainPermissionResolver,
    EnterpriseScopeValidationError,
    EnterpriseScopeValidator,
    EvaluationPipeline,
    PipelineExecution,
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


class _CountingResolver(DomainPermissionResolver):
    """Proves the engine is never even reached when scope validation fails."""

    def __init__(self) -> None:
        self.calls = 0

    async def resolve(self, context: AuthorizationContext) -> TierResolution | None:
        self.calls += 1
        return TierResolution(AuthorizationDecision.ALLOW, "should never be reached")


# ---------------------------------------------------------------------------
# Scope validation wired into the pipeline
# ---------------------------------------------------------------------------


async def test_pipeline_rejects_invalid_scope_before_reaching_any_resolver() -> None:
    resolver = _CountingResolver()
    pipeline = EvaluationPipeline(ResolverRegistry().register(resolver))

    with pytest.raises(EnterpriseScopeValidationError):
        await pipeline.execute(_context(organization_id=""))

    assert resolver.calls == 0


async def test_pipeline_accepts_valid_scope() -> None:
    pipeline = EvaluationPipeline(
        ResolverRegistry().register(
            _stub_domain_permission_resolver(TierResolution(AuthorizationDecision.ALLOW, "grant"))
        )
    )

    result = await pipeline.execute(_context(organization_id="org-1", enterprise_scope="node-1"))

    assert result.decision == AuthorizationDecision.ALLOW


async def test_pipeline_accepts_a_custom_injected_scope_validator() -> None:
    """DI, consistent with M2/M3's own design: a caller may supply its own validator."""

    class _AlwaysPasses(EnterpriseScopeValidator):
        def validate(self, context: AuthorizationContext) -> None:
            return None  # deliberately permissive, for this test only

    pipeline = EvaluationPipeline(
        ResolverRegistry().register(
            _stub_domain_permission_resolver(TierResolution(AuthorizationDecision.ALLOW, "grant"))
        ),
        scope_validator=_AlwaysPasses(),
    )

    result = await pipeline.execute(_context(organization_id=""))  # would fail the default validator

    assert result.decision == AuthorizationDecision.ALLOW


# ---------------------------------------------------------------------------
# Observer failure isolation
# ---------------------------------------------------------------------------


class _BrokenObserver:
    def on_start(self, execution: PipelineExecution) -> None:
        raise RuntimeError("on_start is broken")

    def on_complete(self, execution: PipelineExecution, result) -> None:
        raise RuntimeError("on_complete is broken")

    def on_error(self, execution: PipelineExecution, error: Exception) -> None:
        raise RuntimeError("on_error is broken")


class _RecordingObserver:
    def __init__(self) -> None:
        self.completed = []
        self.errored = []

    def on_start(self, execution: PipelineExecution) -> None:
        pass

    def on_complete(self, execution: PipelineExecution, result) -> None:
        self.completed.append(result)

    def on_error(self, execution: PipelineExecution, error: Exception) -> None:
        self.errored.append(error)


async def test_broken_on_start_does_not_prevent_evaluation() -> None:
    pipeline = EvaluationPipeline(
        ResolverRegistry().register(
            _stub_domain_permission_resolver(TierResolution(AuthorizationDecision.ALLOW, "grant"))
        ),
        observers=(_BrokenObserver(),),
    )

    result = await pipeline.execute(_context())  # must not raise the observer's own RuntimeError

    assert result.decision == AuthorizationDecision.ALLOW


async def test_broken_on_complete_does_not_prevent_the_real_result_from_being_returned() -> None:
    recorder = _RecordingObserver()
    pipeline = EvaluationPipeline(
        ResolverRegistry().register(
            _stub_domain_permission_resolver(TierResolution(AuthorizationDecision.ALLOW, "grant"))
        ),
        observers=(_BrokenObserver(), recorder),
    )

    result = await pipeline.execute(_context())

    assert result.decision == AuthorizationDecision.ALLOW  # returned despite the first observer's own failure
    assert len(recorder.completed) == 1  # the second observer still got notified


async def test_broken_on_error_does_not_mask_the_real_underlying_exception() -> None:
    class _ResolverBlewUp(RuntimeError):
        pass

    class _AlwaysRaisingResolver(DomainPermissionResolver):
        async def resolve(self, context: AuthorizationContext) -> TierResolution | None:
            raise _ResolverBlewUp("the real failure")

    recorder = _RecordingObserver()
    pipeline = EvaluationPipeline(
        ResolverRegistry().register(_AlwaysRaisingResolver()),
        observers=(_BrokenObserver(), recorder),
    )

    with pytest.raises(_ResolverBlewUp):  # the real error, not the observer's RuntimeError
        await pipeline.execute(_context())

    assert len(recorder.errored) == 1
    assert isinstance(recorder.errored[0], _ResolverBlewUp)


# ---------------------------------------------------------------------------
# Deterministic execution with both M5 features active
# ---------------------------------------------------------------------------


async def test_deterministic_execution_with_scope_validation_and_observability_active() -> None:
    from authorization import RuntimeObservabilityCollector

    collector = RuntimeObservabilityCollector()
    pipeline = EvaluationPipeline(
        ResolverRegistry().register(
            _stub_domain_permission_resolver(TierResolution(AuthorizationDecision.ALLOW, "grant"))
        ),
        observers=(collector,),
    )
    context = _context(enterprise_scope="node-1")

    first = await pipeline.execute(context)
    second = await pipeline.execute(context)

    assert first.decision == second.decision == AuthorizationDecision.ALLOW
    assert first.matched_tier == second.matched_tier == AuthorizationTier.DOMAIN_PERMISSION
    assert collector.evaluation_count == 2
    assert collector.completed_count == 2
