"""
Unit tests for WP-RTA-001 Milestone M3 -- Runtime Evaluation Pipeline & Resolver Orchestration.

Covers: successful pipeline execution, missing resolver (discovery),
duplicate resolver (inherited from M2's ResolverRegistry), resolver
failure, empty context, deterministic execution, canonical tier
ordering, engine invocation, and pipeline immutability. No database,
no FastAPI, no capability-specific dependency, no Business Activity
integration.
"""

from __future__ import annotations

import dataclasses

import pytest

from authorization import (
    ApprovalAuthorityResolver,
    AuthorizationContext,
    AuthorizationDecision,
    AuthorizationTier,
    DomainPermissionResolver,
    DuplicateResolverError,
    EvaluationPipeline,
    GroupResolver,
    NamedUserResolver,
    PipelineConfigurationError,
    PipelineExecution,
    ResolverOrchestrator,
    ResolverRegistry,
    TierResolution,
)
from authorization.engine import PRECEDENCE_ORDER


def _context(**overrides) -> AuthorizationContext:
    defaults = dict(identity_id="person-1", organization_id="org-1")
    defaults.update(overrides)
    return AuthorizationContext(**defaults)


def _stub(base_cls, *, outcome: TierResolution | None = None, error: Exception | None = None):
    class _Stub(base_cls):  # type: ignore[misc,valid-type]
        def __init__(self) -> None:
            self.calls = 0

        async def resolve(self, context: AuthorizationContext) -> TierResolution | None:
            self.calls += 1
            if error is not None:
                raise error
            return outcome

    return _Stub()


class _RecordingObserver:
    """Spy observer -- proves the pipeline actually notifies at each stage, and that it invoked the engine."""

    def __init__(self) -> None:
        self.started: list[PipelineExecution] = []
        self.completed: list[tuple[PipelineExecution, object]] = []
        self.errored: list[tuple[PipelineExecution, Exception]] = []

    def on_start(self, execution: PipelineExecution) -> None:
        self.started.append(execution)

    def on_complete(self, execution: PipelineExecution, result) -> None:
        self.completed.append((execution, result))

    def on_error(self, execution: PipelineExecution, error: Exception) -> None:
        self.errored.append((execution, error))


# ---------------------------------------------------------------------------
# ResolverOrchestrator -- discovery
# ---------------------------------------------------------------------------


def test_orchestrator_rejects_none_registry() -> None:
    with pytest.raises(PipelineConfigurationError):
        ResolverOrchestrator(None)  # type: ignore[arg-type]


def test_orchestrator_configured_and_missing_tiers_respect_canonical_order() -> None:
    registry = (
        ResolverRegistry()
        .register(_stub(DomainPermissionResolver))
        .register(_stub(NamedUserResolver))
    )
    orchestrator = ResolverOrchestrator(registry)

    # Canonical order is NAMED_USER > GROUP > APPROVAL_AUTHORITY > BUSINESS_ROLE > DOMAIN_PERMISSION,
    # not registration order (DOMAIN_PERMISSION was registered first, above).
    assert orchestrator.configured_tiers == (AuthorizationTier.NAMED_USER, AuthorizationTier.DOMAIN_PERMISSION)
    assert orchestrator.missing_tiers == (
        AuthorizationTier.GROUP,
        AuthorizationTier.APPROVAL_AUTHORITY,
        AuthorizationTier.BUSINESS_ROLE,
    )
    # Both tuples are exact-order subsequences of PRECEDENCE_ORDER, not registration order.
    assert list(orchestrator.configured_tiers) == [t for t in PRECEDENCE_ORDER if t in orchestrator.configured_tiers]
    assert list(orchestrator.missing_tiers) == [t for t in PRECEDENCE_ORDER if t in orchestrator.missing_tiers]


def test_orchestrator_resolvers_returns_independent_copy() -> None:
    registry = ResolverRegistry().register(_stub(DomainPermissionResolver))
    orchestrator = ResolverOrchestrator(registry)

    first = orchestrator.resolvers()
    second = orchestrator.resolvers()

    assert first == second
    assert first is not second


# ---------------------------------------------------------------------------
# EvaluationPipeline -- configuration and discovery
# ---------------------------------------------------------------------------


def test_pipeline_missing_resolver_is_discoverable_before_execution() -> None:
    """A caller can know a tier is unconfigured without running an evaluation at all."""
    pipeline = EvaluationPipeline(ResolverRegistry().register(_stub(DomainPermissionResolver)))

    assert AuthorizationTier.DOMAIN_PERMISSION in pipeline.configured_tiers
    assert AuthorizationTier.NAMED_USER in pipeline.missing_tiers
    assert AuthorizationTier.GROUP in pipeline.missing_tiers
    assert AuthorizationTier.APPROVAL_AUTHORITY in pipeline.missing_tiers
    assert AuthorizationTier.BUSINESS_ROLE in pipeline.missing_tiers


def test_pipeline_duplicate_resolver_still_rejected_by_the_underlying_registry() -> None:
    """M3 adds no new duplicate-registration path -- M2's ResolverRegistry.register() remains the sole gate."""
    registry = ResolverRegistry().register(_stub(DomainPermissionResolver))

    with pytest.raises(DuplicateResolverError):
        registry.register(_stub(DomainPermissionResolver))


def test_pipeline_rejects_none_registry() -> None:
    with pytest.raises(PipelineConfigurationError):
        EvaluationPipeline(None)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# EvaluationPipeline -- execution
# ---------------------------------------------------------------------------


async def test_successful_pipeline_execution_invokes_the_engine_and_returns_its_result() -> None:
    registry = ResolverRegistry().register(
        _stub(DomainPermissionResolver, outcome=TierResolution(AuthorizationDecision.ALLOW, "active grant"))
    )
    pipeline = EvaluationPipeline(registry)

    result = await pipeline.execute(_context())

    assert result.decision == AuthorizationDecision.ALLOW
    assert result.matched_tier == AuthorizationTier.DOMAIN_PERMISSION
    assert len(result.trace) == 5  # proves the real AuthorizationEngine ran the full canonical walk, not a stub


async def test_pipeline_notifies_observers_on_start_and_on_complete_in_order() -> None:
    observer = _RecordingObserver()
    registry = ResolverRegistry().register(
        _stub(DomainPermissionResolver, outcome=TierResolution(AuthorizationDecision.ALLOW, "grant"))
    )
    pipeline = EvaluationPipeline(registry, observers=(observer,))

    context = _context()
    result = await pipeline.execute(context)

    assert len(observer.started) == 1
    assert observer.started[0].context == context
    assert len(observer.completed) == 1
    completed_execution, completed_result = observer.completed[0]
    assert completed_execution.execution_id == observer.started[0].execution_id
    assert completed_result is result
    assert observer.errored == []


async def test_empty_authorization_context_denies_deterministically_through_the_pipeline() -> None:
    pipeline = EvaluationPipeline(ResolverRegistry())

    result = await pipeline.execute(_context())

    assert result.decision == AuthorizationDecision.DENY
    assert result.matched_tier is None
    assert len(result.trace) == 5


async def test_resolver_failure_propagates_through_the_pipeline_and_notifies_on_error() -> None:
    class _ResolverBlewUp(RuntimeError):
        pass

    observer = _RecordingObserver()
    registry = ResolverRegistry().register(_stub(DomainPermissionResolver, error=_ResolverBlewUp("boom")))
    pipeline = EvaluationPipeline(registry, observers=(observer,))

    with pytest.raises(_ResolverBlewUp):
        await pipeline.execute(_context())

    assert len(observer.errored) == 1
    assert isinstance(observer.errored[0][1], _ResolverBlewUp)
    assert observer.completed == []  # on_complete must never fire when the engine raised


async def test_pipeline_execution_is_deterministic_across_repeated_calls() -> None:
    registry = (
        ResolverRegistry()
        .register(_stub(GroupResolver, outcome=None))
        .register(_stub(ApprovalAuthorityResolver, outcome=TierResolution(AuthorizationDecision.CONDITIONAL, "needs approval")))
    )
    pipeline = EvaluationPipeline(registry)
    context = _context()

    first = await pipeline.execute(context)
    second = await pipeline.execute(context)

    assert first.decision == second.decision == AuthorizationDecision.CONDITIONAL
    assert first.matched_tier == second.matched_tier == AuthorizationTier.APPROVAL_AUTHORITY
    assert first.trace == second.trace


async def test_pipeline_respects_canonical_tier_ordering_end_to_end() -> None:
    """Named User (registered second, below) must still win over Domain Permission (registered first)."""
    registry = (
        ResolverRegistry()
        .register(_stub(DomainPermissionResolver, outcome=TierResolution(AuthorizationDecision.ALLOW, "would allow")))
        .register(_stub(NamedUserResolver, outcome=TierResolution(AuthorizationDecision.DENY, "explicit deny")))
    )
    pipeline = EvaluationPipeline(registry)

    result = await pipeline.execute(_context())

    assert result.decision == AuthorizationDecision.DENY
    assert result.matched_tier == AuthorizationTier.NAMED_USER
    assert len(result.trace) == 1  # Domain Permission was never even consulted


# ---------------------------------------------------------------------------
# Immutability
# ---------------------------------------------------------------------------


def test_pipeline_execution_is_immutable() -> None:
    execution = PipelineExecution(execution_id="exec-1", context=_context())

    with pytest.raises(dataclasses.FrozenInstanceError):
        execution.execution_id = "exec-2"  # type: ignore[misc]
