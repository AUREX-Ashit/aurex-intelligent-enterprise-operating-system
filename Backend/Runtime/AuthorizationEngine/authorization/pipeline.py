"""
Runtime Evaluation Pipeline (WP-RTA-001 M3).

The single, stable entry point a future caller invokes: assembles
resolvers via ResolverOrchestrator (this milestone) and
AuthorizationEngine (M1, unchanged, unmodified), executes one
evaluation, and notifies any registered PipelineObserver -- the
extension seam future milestones (M4 Observability, M6 Caching, and
any future Audit/persistence integration) attach to, so that none of
them ever needs to modify AuthorizationEngine itself.

Design note (boundary between this module and AuthorizationEngine,
disclosed per this milestone's own instruction to state design
decisions plainly): AuthorizationEngine's own internal iteration over
`engine.PRECEDENCE_ORDER` (M1, unchanged) is URA-001-76's precedence
*rule application* over a resolver set it was handed at construction
-- RTA-001 S11.2's own "sole authority for runtime authorization
decisions." It is not "orchestration" in this milestone's sense:
AuthorizationEngine performs no resolver *discovery* (it never reads a
registry or config source), no dependency-injection *assembly* (it is
handed a finished mapping), no configuration *introspection* (no
`configured_tiers`/`missing_tiers` equivalent exists on it), and
exposes no extension seam of its own. Those four responsibilities --
discovery, assembly, introspection, extension -- are exactly what this
module and `orchestrator.py` add, entirely outside `engine.py`, which
remains byte-for-byte unchanged from M2.

Never fabricates, overrides, or influences the AuthorizationDecision
AuthorizationEngine returns (CLAUDE.md S19.8.5) -- observers are
notified of the outcome, never consulted to help produce it.

M5 additions (WP-RTA-001 Milestone M5 -- Runtime Completeness),
disclosed here since they change this file's own `execute()`:
- Enterprise Scope Validation (`scope_validator.EnterpriseScopeValidator`)
  now runs before AuthorizationEngine is invoked -- see that module's
  own docstring for the disclosed placement-simplification rationale.
- Observer notification is now failure-isolated: an exception raised
  by one observer's own callback can never prevent the real
  EvaluationResult (or the real underlying exception) from reaching
  the caller, and can never prevent other observers from also being
  notified. See `_notify_safely` below.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Protocol, runtime_checkable
from uuid import uuid4

from .engine import AuthorizationEngine
from .models import AuthorizationContext, AuthorizationTier, EvaluationResult
from .orchestrator import PipelineConfigurationError, ResolverOrchestrator
from .registry import ResolverRegistry
from .scope_validator import EnterpriseScopeValidator

__all__ = [
    "EvaluationPipeline",
    "PipelineExecution",
    "PipelineObserver",
    "PipelineConfigurationError",
]


@dataclass(frozen=True)
class PipelineExecution:
    """
    Immutable, runtime-only record of one pipeline invocation.
    Correlation only -- never persisted (no ORM, no repository, no
    Business Activity integration; explicitly out of M3 scope). Given
    to every PipelineObserver callback so a future extension (e.g.
    M4's own tracing) has a stable correlation id without this module
    inventing a persistence mechanism to provide one.
    """

    execution_id: str
    context: AuthorizationContext


@runtime_checkable
class PipelineObserver(Protocol):
    """
    The Extension Point this milestone introduces. A future milestone
    implements this to observe pipeline execution (e.g. M4
    Observability, M6 Caching, or any future Audit/persistence
    integration) without AuthorizationEngine ever being modified. No
    observer method returns a value the pipeline consumes -- an
    observer may never influence the returned EvaluationResult, only
    react to it, preserving CLAUDE.md S19.8.5's prohibition on
    anything resembling a fabricated or externally-influenced
    authorization decision.
    """

    def on_start(self, execution: PipelineExecution) -> None: ...

    def on_complete(self, execution: PipelineExecution, result: EvaluationResult) -> None: ...

    def on_error(self, execution: PipelineExecution, error: Exception) -> None: ...


class EvaluationPipeline:
    """
    Runtime Evaluation Pipeline: accepts an AuthorizationContext,
    obtains the configured tier resolvers (via ResolverOrchestrator),
    invokes AuthorizationEngine, and returns its EvaluationResult --
    notifying any registered PipelineObserver along the way. Performs
    no resolver invocation, no precedence evaluation, and no decision
    -making of its own; all three remain exclusively
    AuthorizationEngine's job (M1, unmodified).
    """

    def __init__(
        self,
        registry: ResolverRegistry,
        observers: tuple[PipelineObserver, ...] = (),
        scope_validator: EnterpriseScopeValidator | None = None,
    ) -> None:
        self._orchestrator = ResolverOrchestrator(registry)
        self._engine = AuthorizationEngine(self._orchestrator.resolvers())
        self._observers: tuple[PipelineObserver, ...] = tuple(observers)
        self._scope_validator: EnterpriseScopeValidator = scope_validator or EnterpriseScopeValidator()

    @property
    def configured_tiers(self) -> tuple[AuthorizationTier, ...]:
        return self._orchestrator.configured_tiers

    @property
    def missing_tiers(self) -> tuple[AuthorizationTier, ...]:
        return self._orchestrator.missing_tiers

    async def execute(self, context: AuthorizationContext) -> EvaluationResult:
        """
        Validate Enterprise Scope, then run one evaluation. Never
        catches a scope-validation/resolver/engine exception to
        convert it into a decision -- it is reported to every
        observer's `on_error` and then always re-raised (fail fast,
        CLAUDE.md coding standards; never fabricate a decision,
        CLAUDE.md S19.8.5). An observer's own failure while being
        notified is isolated (M5) and never allowed to replace or
        suppress the real result or the real exception.
        """
        execution = PipelineExecution(execution_id=str(uuid4()), context=context)

        for observer in self._observers:
            self._notify_safely(observer.on_start, execution)

        try:
            self._scope_validator.validate(context)
            result = await self._engine.evaluate(context)
        except Exception as error:
            for observer in self._observers:
                self._notify_safely(observer.on_error, execution, error)
            raise

        for observer in self._observers:
            self._notify_safely(observer.on_complete, execution, result)

        return result

    @staticmethod
    def _notify_safely(callback: Callable[..., None], *args: object) -> None:
        """
        Isolate one observer callback's own failure (M5) -- caught and
        discarded, never allowed to affect the real evaluation outcome
        or prevent other observers from being notified. Deliberately
        has no visibility mechanism of its own (no logging/metrics
        backend is available this milestone, per instruction); see
        TD-075 for this disclosed limitation.
        """
        try:
            callback(*args)
        except Exception:
            pass
