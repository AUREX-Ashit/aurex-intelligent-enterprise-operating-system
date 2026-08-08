"""
Unit tests for WP-RTA-001 Milestone M6 -- Runtime Contract Verification.

Asserts the exact public signature and shape of every public runtime
interface (AuthorizationEngine, EvaluationPipeline, AuthorizationAdapter,
ResolverRegistry, the tier resolver interfaces, and the two observer
Protocols). A future accidental signature change breaks these tests
before it breaks a real caller -- this is the executable form of
"Document all public contracts."
"""

from __future__ import annotations

import dataclasses
import inspect

from adapters import AuthorizationAdapter, AuthorizationRequest
from authorization import (
    AuthorizationContext,
    AuthorizationDecision,
    AuthorizationEngine,
    AuthorizationTier,
    BaseTierResolver,
    EnterpriseScopeValidator,
    EvaluationPipeline,
    EvaluationResult,
    PipelineExecution,
    PipelineObserver,
    ResolverOrchestrator,
    ResolverRegistry,
    RuntimeObservabilityCollector,
    TierEvaluation,
    TierResolution,
    TierResolver,
    TierResult,
)


# ---------------------------------------------------------------------------
# AuthorizationEngine (M1)
# ---------------------------------------------------------------------------


def test_authorization_engine_constructor_contract() -> None:
    params = inspect.signature(AuthorizationEngine.__init__).parameters
    assert list(params) == ["self", "resolvers"]
    assert params["resolvers"].default is None


def test_authorization_engine_evaluate_contract() -> None:
    sig = inspect.signature(AuthorizationEngine.evaluate)
    assert list(sig.parameters) == ["self", "context"]
    assert inspect.iscoroutinefunction(AuthorizationEngine.evaluate)


# ---------------------------------------------------------------------------
# EvaluationPipeline (M3, extended M5)
# ---------------------------------------------------------------------------


def test_evaluation_pipeline_constructor_contract() -> None:
    params = inspect.signature(EvaluationPipeline.__init__).parameters
    assert list(params) == ["self", "registry", "observers", "scope_validator"]
    assert params["observers"].default == ()
    assert params["scope_validator"].default is None


def test_evaluation_pipeline_execute_contract() -> None:
    sig = inspect.signature(EvaluationPipeline.execute)
    assert list(sig.parameters) == ["self", "context"]
    assert inspect.iscoroutinefunction(EvaluationPipeline.execute)


def test_evaluation_pipeline_exposes_discovery_properties() -> None:
    assert isinstance(EvaluationPipeline.configured_tiers, property)
    assert isinstance(EvaluationPipeline.missing_tiers, property)


# ---------------------------------------------------------------------------
# AuthorizationAdapter (M4)
# ---------------------------------------------------------------------------


def test_authorization_adapter_constructor_contract() -> None:
    params = inspect.signature(AuthorizationAdapter.__init__).parameters
    assert list(params) == ["self", "pipeline"]


def test_authorization_adapter_evaluate_contract() -> None:
    sig = inspect.signature(AuthorizationAdapter.evaluate)
    assert list(sig.parameters) == ["self", "request"]
    assert inspect.iscoroutinefunction(AuthorizationAdapter.evaluate)


def test_authorization_adapter_build_context_contract() -> None:
    sig = inspect.signature(AuthorizationAdapter.build_context)
    assert list(sig.parameters) == ["self", "request"]
    assert not inspect.iscoroutinefunction(AuthorizationAdapter.build_context)  # synchronous, by design


def test_authorization_request_required_fields() -> None:
    """A field only counts as required if it has neither a default nor a default_factory (tuple-typed fields use the latter)."""
    required = [
        f.name
        for f in dataclasses.fields(AuthorizationRequest)
        if f.default is dataclasses.MISSING and f.default_factory is dataclasses.MISSING
    ]
    assert required == ["identity_id", "organization_id"]


# ---------------------------------------------------------------------------
# ResolverRegistry / ResolverOrchestrator (M2/M3)
# ---------------------------------------------------------------------------


def test_resolver_registry_contract() -> None:
    assert list(inspect.signature(ResolverRegistry.__init__).parameters) == ["self"]
    assert list(inspect.signature(ResolverRegistry.register).parameters) == ["self", "resolver"]
    assert list(inspect.signature(ResolverRegistry.build).parameters) == ["self"]


def test_resolver_orchestrator_contract() -> None:
    assert list(inspect.signature(ResolverOrchestrator.__init__).parameters) == ["self", "registry"]
    assert isinstance(ResolverOrchestrator.configured_tiers, property)
    assert isinstance(ResolverOrchestrator.missing_tiers, property)


# ---------------------------------------------------------------------------
# Tier resolver interfaces (M2)
# ---------------------------------------------------------------------------


def test_base_tier_resolver_is_abstract_with_a_single_resolve_method() -> None:
    assert inspect.isabstract(BaseTierResolver)
    assert "resolve" in BaseTierResolver.__abstractmethods__
    assert inspect.iscoroutinefunction(BaseTierResolver.resolve)


def test_tier_resolver_protocol_matches_base_tier_resolver_shape() -> None:
    sig_protocol = inspect.signature(TierResolver.resolve)
    sig_base = inspect.signature(BaseTierResolver.resolve)
    assert list(sig_protocol.parameters) == list(sig_base.parameters) == ["self", "context"]


# ---------------------------------------------------------------------------
# Observer Protocols (M3, M5's concrete implementation)
# ---------------------------------------------------------------------------


def test_pipeline_observer_protocol_contract() -> None:
    assert list(inspect.signature(PipelineObserver.on_start).parameters) == ["self", "execution"]
    assert list(inspect.signature(PipelineObserver.on_complete).parameters) == ["self", "execution", "result"]
    assert list(inspect.signature(PipelineObserver.on_error).parameters) == ["self", "execution", "error"]


def test_runtime_observability_collector_implements_pipeline_observer_shape() -> None:
    collector = RuntimeObservabilityCollector()
    assert isinstance(collector, PipelineObserver)  # runtime_checkable Protocol -- structural conformance


def test_enterprise_scope_validator_contract() -> None:
    sig = inspect.signature(EnterpriseScopeValidator.validate)
    assert list(sig.parameters) == ["self", "context"]
    assert not inspect.iscoroutinefunction(EnterpriseScopeValidator.validate)  # synchronous, by design


# ---------------------------------------------------------------------------
# Immutable models -- every advertised-immutable type really is one
# ---------------------------------------------------------------------------


def test_every_advertised_immutable_model_is_a_frozen_dataclass() -> None:
    for cls in (AuthorizationContext, TierEvaluation, EvaluationResult, TierResolution, PipelineExecution):
        assert dataclasses.is_dataclass(cls), f"{cls.__name__} is not a dataclass"
        assert cls.__dataclass_params__.frozen, f"{cls.__name__} is not frozen"


def test_enum_decision_and_tier_and_result_members_are_stable() -> None:
    assert {d.value for d in AuthorizationDecision} == {"ALLOW", "DENY", "CONDITIONAL", "DELEGATED", "ESCALATED"}
    assert {t.value for t in AuthorizationTier} == {
        "NAMED_USER",
        "GROUP",
        "APPROVAL_AUTHORITY",
        "BUSINESS_ROLE",
        "DOMAIN_PERMISSION",
    }
    assert {r.value for r in TierResult} == {"MATCH", "NO_MATCH", "NOT_EVALUATED"}
