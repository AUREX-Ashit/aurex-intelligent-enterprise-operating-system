# Authorization Runtime Engine (WP-RTA-001)

Implements the Authorization Engine Runtime Component specified by `RTA-001 §3.8`/`§11`. Owns no Business Object, performs no Business Activity — see `architecture/05-Implementation/IRA-RTA-001_...md` for the full constitutional charter and `architecture/05-Implementation/WP-RTA-001_...md` for the Work Package definition. This file documents the package's own public contracts (Milestone M6, "Document all public contracts") — it does not restate the governance record.

**Status:** M1–M6 implemented (see `architecture/05-Implementation/IMP-REPORT-WP-RTA-001_...md`). Not committed. Not independently reviewed or certified. No Business Activity or WP-05 consumer wired.

## Package Structure

```
Backend/Runtime/AuthorizationEngine/
├── authorization/          The runtime itself. Never imports from adapters/.
│   ├── models.py           M1 — AuthorizationContext, EvaluationResult, TierEvaluation, and the three enums
│   ├── resolvers.py        M1 — the generic TierResolver Protocol, TierResolution
│   ├── engine.py           M1 — AuthorizationEngine (decision authority; unmodified since M1)
│   ├── tier_resolvers.py   M2 — the five URA-001-76 tier-specific resolver interfaces
│   ├── registry.py         M2 — ResolverRegistry (injectable resolver assembly)
│   ├── orchestrator.py     M3 — ResolverOrchestrator (discovery/introspection)
│   ├── pipeline.py         M3, extended M5 — EvaluationPipeline (the stable entry point)
│   ├── scope_validator.py  M5 — EnterpriseScopeValidator
│   └── observability.py    M5 — RuntimeObservabilityCollector (a concrete PipelineObserver)
├── adapters/                The integration layer. May import from authorization/; never the reverse.
│   └── authorization_adapter.py   M4 — AuthorizationAdapter, AuthorizationRequest
├── tests/                   106 unit tests across all six milestones
└── pytest.ini
```

## Quick Start

```python
from authorization import (
    AuthorizationDecision,
    EvaluationPipeline,
    ResolverRegistry,
    RuntimeObservabilityCollector,
    TierResolution,
)
from authorization.tier_resolvers import DomainPermissionResolver
from adapters import AuthorizationAdapter, AuthorizationRequest

class MyDomainPermissionResolver(DomainPermissionResolver):
    async def resolve(self, context):
        # look up a real grant here (M5's own scope, not yet built) and
        # return TierResolution(AuthorizationDecision.ALLOW, "...") or None
        ...

registry = ResolverRegistry().register(MyDomainPermissionResolver())
collector = RuntimeObservabilityCollector()
pipeline = EvaluationPipeline(registry, observers=(collector,))
adapter = AuthorizationAdapter(pipeline)

result = await adapter.evaluate(
    AuthorizationRequest(identity_id="person-1", organization_id="org-1")
)
print(result.decision, result.matched_tier, result.trace)
```

## Public Contracts

### `AuthorizationEngine` (M1 — unmodified since introduction)

```python
AuthorizationEngine(resolvers: dict[AuthorizationTier, TierResolver] | None = None)
async def evaluate(self, context: AuthorizationContext) -> EvaluationResult
```

The sole decision authority (`RTA-001 §11.2`). Never queries a database, calls an API, or accesses a repository. Never fabricates `ALLOW`. Deterministic and reproducible.

### `EvaluationPipeline` (M3, extended M5)

```python
EvaluationPipeline(
    registry: ResolverRegistry,
    observers: tuple[PipelineObserver, ...] = (),
    scope_validator: EnterpriseScopeValidator | None = None,
)
async def execute(self, context: AuthorizationContext) -> EvaluationResult
configured_tiers: tuple[AuthorizationTier, ...]   # property
missing_tiers: tuple[AuthorizationTier, ...]      # property
```

Validates Enterprise Scope, invokes `AuthorizationEngine`, notifies every `PipelineObserver` at each stage. An observer's own failure is isolated (M5) and never affects the real result or masks the real exception.

### `AuthorizationAdapter` (M4)

```python
AuthorizationAdapter(pipeline: EvaluationPipeline)
def build_context(self, request: AuthorizationRequest) -> AuthorizationContext
async def evaluate(self, request: AuthorizationRequest) -> EvaluationResult
```

Translation only. Raises `InvalidAuthorizationRequestError` on a blank `identity_id`/`organization_id`, before the pipeline is ever invoked.

### `ResolverRegistry` (M2)

```python
ResolverRegistry()
def register(self, resolver: BaseTierResolver) -> "ResolverRegistry"   # fluent
def build(self) -> dict[AuthorizationTier, TierResolver]
```

Raises `DuplicateResolverError` on a second registration for an already-bound tier.

### Tier resolver interfaces (M2)

`NamedUserResolver`, `GroupResolver`, `ApprovalAuthorityResolver`, `BusinessRoleResolver`, `DomainPermissionResolver` — each an ABC with a single abstract method:

```python
async def resolve(self, context: AuthorizationContext) -> TierResolution | None
```

Return a `TierResolution` if the tier reaches a determination; `None` if checked and found nothing (`NO_MATCH`, distinct from an unbound tier, which the engine reports as `NOT_EVALUATED` without ever calling `resolve()`).

### `PipelineObserver` (M3) — the extension point

```python
def on_start(self, execution: PipelineExecution) -> None
def on_complete(self, execution: PipelineExecution, result: EvaluationResult) -> None
def on_error(self, execution: PipelineExecution, error: Exception) -> None
```

A structural `Protocol` — no inheritance required. All three methods return `None`; an observer can never influence the returned decision. **Sufficient for:** Metrics, Tracing, Audit, read-side Persistence recording (all proven in `tests/test_extension_points.py`). **Not sufficient for:** Caching — caching must intercept *before* evaluation runs, which this passive, after-the-fact seam cannot do. A future Caching milestone wraps `EvaluationPipeline` by composition instead (see `test_extension_points.py`'s own proof-of-concept for the pattern; `TD-078`).

### `EnterpriseScopeValidator` (M5)

```python
def validate(self, context: AuthorizationContext) -> None   # raises EnterpriseScopeValidationError
```

Structural validation only (`organization_id`/`enterprise_scope` presence and well-formedness) — never a real ERG-001 lookup (`TD-076`, requires persistence, out of scope).

### `RuntimeObservabilityCollector` (M5) — a concrete `PipelineObserver`

```python
RuntimeObservabilityCollector()
events: tuple[ObservabilityEvent, ...]   # property, in-memory only
evaluation_count / completed_count / failure_count: int   # properties
```

## Known Limitations (see `architecture/06-Reviews/TECH-DEBT.md` for the full register)

- Four of five precedence tiers (Named User, Group, Approval Authority, Business Role) have no real, bound resolver anywhere yet — their owning data models (`Group`, `runtime_assignment_registry`, an Approval-Authority holder linkage, Business-Role domain-scoping) do not exist in this repository (`TD-071`, `IRA-RTA-001 §6`).
- No Business Activity or FastAPI endpoint consumes this runtime yet (`AuthorizationAdapter` has no real caller).
- Enterprise Scope Validation runs once, before evaluation, rather than at `RTA-001 §11.7`'s own literal mid-pipeline position (`TD-077`).
- Observer-failure isolation has no visibility mechanism of its own (`TD-075`).
- Caching is not implemented; the extension point requires a wrapper, not an observer (`TD-078`).

## Testing

```
cd Backend/Runtime/AuthorizationEngine
python -m pytest tests/ -v
```

106 tests, zero database, zero network, zero FastAPI dependency. Runs in under 1.5 seconds.
