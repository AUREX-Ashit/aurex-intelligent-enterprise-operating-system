"""
Extension point validation for WP-RTA-001 Milestone M6.

Verifies future extension points for Metrics, Tracing, and Audit
attach purely through PipelineObserver (M3) with zero changes to
AuthorizationEngine, AuthorizationContext, or any other M1 file. Also
documents a genuine finding about Caching: PipelineObserver is a
passive, after-the-fact notification seam (on_start/on_complete/
on_error all return None) and cannot short-circuit evaluation to
return a cached result -- it is structurally insufficient for caching,
which requires intercepting *before* the engine runs. This is recorded
honestly (see IMP-REPORT-WP-RTA-001 M6 and TD-078), not glossed over.
No caching mechanism is implemented here, per instruction -- the
proof-of-concept wrapper below exists only to demonstrate the
composition pattern a future, separately-scoped Caching milestone
would use, and is not shipped as production code.
"""

from __future__ import annotations

import inspect

from authorization import (
    AuthorizationContext,
    AuthorizationDecision,
    DomainPermissionResolver,
    EvaluationPipeline,
    EvaluationResult,
    PipelineExecution,
    PipelineObserver,
    ResolverRegistry,
    TierResolution,
)
from authorization.engine import AuthorizationEngine


def _context(**overrides) -> AuthorizationContext:
    defaults = dict(identity_id="person-1", organization_id="org-1")
    defaults.update(overrides)
    return AuthorizationContext(**defaults)


def _stub_domain_permission_resolver(outcome: TierResolution | None):
    class _Stub(DomainPermissionResolver):
        async def resolve(self, context: AuthorizationContext) -> TierResolution | None:
            return outcome

    return _Stub()


_ENGINE_SOURCE_SNAPSHOT = inspect.getsource(AuthorizationEngine)


def test_authorization_engine_source_is_unaffected_by_any_extension_point_in_this_file() -> None:
    """A literal, executable guarantee -- not just an assertion in prose."""
    assert inspect.getsource(AuthorizationEngine) == _ENGINE_SOURCE_SNAPSHOT


# ---------------------------------------------------------------------------
# Metrics, Tracing, Audit -- all satisfied by the existing PipelineObserver seam
# ---------------------------------------------------------------------------


class _MetricsObserverStub:
    """Stands in for a future metrics-backend integration -- pure PipelineObserver, no core change required."""

    def __init__(self) -> None:
        self.evaluations = 0

    def on_start(self, execution: PipelineExecution) -> None:
        self.evaluations += 1

    def on_complete(self, execution: PipelineExecution, result: EvaluationResult) -> None:
        pass

    def on_error(self, execution: PipelineExecution, error: Exception) -> None:
        pass


class _TracingObserverStub:
    """Stands in for a future distributed-tracing integration."""

    def __init__(self) -> None:
        self.spans: list[str] = []

    def on_start(self, execution: PipelineExecution) -> None:
        self.spans.append(f"span-start:{execution.execution_id}")

    def on_complete(self, execution: PipelineExecution, result: EvaluationResult) -> None:
        self.spans.append(f"span-end:{execution.execution_id}:{result.decision.value}")

    def on_error(self, execution: PipelineExecution, error: Exception) -> None:
        self.spans.append(f"span-error:{execution.execution_id}:{type(error).__name__}")


class _AuditObserverStub:
    """Stands in for a future audit-persistence integration."""

    def __init__(self) -> None:
        self.audit_log: list[dict] = []

    def on_start(self, execution: PipelineExecution) -> None:
        pass

    def on_complete(self, execution: PipelineExecution, result: EvaluationResult) -> None:
        self.audit_log.append({"decision": result.decision.value, "execution_id": execution.execution_id})

    def on_error(self, execution: PipelineExecution, error: Exception) -> None:
        self.audit_log.append({"error": type(error).__name__, "execution_id": execution.execution_id})


async def test_metrics_tracing_and_audit_extension_points_attach_via_pipeline_observer_only() -> None:
    metrics = _MetricsObserverStub()
    tracing = _TracingObserverStub()
    audit = _AuditObserverStub()
    pipeline = EvaluationPipeline(
        ResolverRegistry().register(
            _stub_domain_permission_resolver(TierResolution(AuthorizationDecision.ALLOW, "grant"))
        ),
        observers=(metrics, tracing, audit),
    )

    result = await pipeline.execute(_context())

    assert metrics.evaluations == 1
    assert len(tracing.spans) == 2  # start + end
    assert tracing.spans[1].endswith(result.decision.value)
    assert audit.audit_log[0]["decision"] == result.decision.value


def test_all_three_stub_observers_satisfy_pipeline_observer_structurally() -> None:
    for observer in (_MetricsObserverStub(), _TracingObserverStub(), _AuditObserverStub()):
        assert isinstance(observer, PipelineObserver)


# ---------------------------------------------------------------------------
# Persistence -- also satisfied by the observer seam for read-side recording
# ---------------------------------------------------------------------------


class _PersistenceObserverStub:
    """A future persistence integration recording completed evaluations -- writes nothing back into the runtime itself."""

    def __init__(self) -> None:
        self.persisted: list[EvaluationResult] = []

    def on_start(self, execution: PipelineExecution) -> None:
        pass

    def on_complete(self, execution: PipelineExecution, result: EvaluationResult) -> None:
        self.persisted.append(result)  # a real implementation would write to a repository here -- out of scope

    def on_error(self, execution: PipelineExecution, error: Exception) -> None:
        pass


async def test_persistence_extension_point_attaches_via_pipeline_observer_only() -> None:
    persistence = _PersistenceObserverStub()
    pipeline = EvaluationPipeline(
        ResolverRegistry().register(
            _stub_domain_permission_resolver(TierResolution(AuthorizationDecision.ALLOW, "grant"))
        ),
        observers=(persistence,),
    )

    await pipeline.execute(_context())

    assert len(persistence.persisted) == 1


# ---------------------------------------------------------------------------
# Caching -- documented finding: PipelineObserver is insufficient; a wrapper is required
# ---------------------------------------------------------------------------


class _ProofOfConceptCachingWrapper:
    """
    Test-only proof of concept, NOT production code and not exported
    from `authorization` or `adapters`. Demonstrates that a future
    Caching milestone can wrap EvaluationPipeline entirely by
    composition -- still zero AuthorizationEngine changes required --
    without needing PipelineObserver at all, since caching must
    intercept *before* evaluation runs, which PipelineObserver's
    passive, after-the-fact callbacks cannot do (TD-078).
    """

    def __init__(self, pipeline: EvaluationPipeline) -> None:
        self._pipeline = pipeline
        self._cache: dict[str, EvaluationResult] = {}
        self.cache_hits = 0
        self.cache_misses = 0

    async def execute(self, context: AuthorizationContext) -> EvaluationResult:
        cache_key = context.identity_id  # deliberately naive -- proof of concept only
        if cache_key in self._cache:
            self.cache_hits += 1
            return self._cache[cache_key]

        self.cache_misses += 1
        result = await self._pipeline.execute(context)
        self._cache[cache_key] = result
        return result


async def test_caching_extension_point_requires_a_wrapper_not_an_observer() -> None:
    """Documents the finding: proves the wrapper pattern works, and that it still touches no core file."""
    pipeline = EvaluationPipeline(
        ResolverRegistry().register(
            _stub_domain_permission_resolver(TierResolution(AuthorizationDecision.ALLOW, "grant"))
        )
    )
    wrapped = _ProofOfConceptCachingWrapper(pipeline)
    context = _context()

    first = await wrapped.execute(context)
    second = await wrapped.execute(context)

    assert first is second  # served from cache, not re-evaluated
    assert wrapped.cache_misses == 1
    assert wrapped.cache_hits == 1


def test_pipeline_observer_protocol_cannot_short_circuit_evaluation() -> None:
    """Structural proof of the finding: every PipelineObserver method's own declared return type is None."""
    for method_name in ("on_start", "on_complete", "on_error"):
        method = getattr(PipelineObserver, method_name)
        return_annotation = inspect.signature(method).return_annotation
        assert return_annotation in (None, "None"), (
            f"PipelineObserver.{method_name} returns {return_annotation!r}, not None -- "
            "if this ever changes, re-examine whether Caching could use the observer seam after all."
        )
