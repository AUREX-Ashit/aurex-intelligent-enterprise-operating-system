# Business Activity Engine (WP-BAE-001)

Implements the Business Activity Engine Runtime Component specified by `IMP-001 §6.15`–`§6.19`. It owns no Business Object and performs no Business Activity of its own (`IRA-BAE-001 §9`). Its placement, pipeline ordering, and Manifest Resolution ownership are fixed by `architecture/07-Decisions/ADR-042_...md`. Its runtime contract is `architecture/06-Reviews/IRA-BAE-001-M1_Runtime_Contract_and_Gap_Analysis.md §7`. This file documents the package's public contracts; it does not restate the governance record.

**Status:** M1 (Runtime Contract / Architecture Baseline) skeleton implemented. Independently reviewed: PASS WITH CONDITIONS (`architecture/06-Reviews/IRA-BAE-001-M1_Independent_Review.md`). Its remediation was independently verified (`architecture/06-Reviews/IRA-BAE-001-M1_Remediation_Independent_Review.md`). **M1 ACCEPTED — COMPLETE** (2026-09-25). This is M1 only: the Business Activity Engine as a whole is not complete, and M2 is not authorized. No host service consumes it. No Business Activity is registered or routed through it.

## Package Structure

```
Backend/Runtime/BusinessActivityEngine/
├── business_activity_engine/
│   ├── identity.py    BusinessActivityIdentifier — BAR-issued BA-NNNNNN, shape-validated, never issued here
│   ├── pipeline.py    PipelineStage — IMP-001 §6.16.3's sixteen stages, canonical order (ADR-042 / RO-M1-02)
│   ├── context.py     BusinessActivityInvocation (input), BusinessActivityContext (immutable), ContextSection
│   ├── state.py       ExecutionState (§6.18.4) + AUTHORITATIVE_TRANSITIONS (§6.18.6) — vocabulary only
│   ├── ports.py       RegistrationSource, ManifestResolver, Authorizer, TransactionBoundary
│   ├── results.py     BusinessActivityExecutionResult, ExecutionOutcome
│   └── engine.py      BusinessActivityEngine — the single entry point
├── tests/             structural, behavioural, and static package-boundary tests
└── pytest.ini
```

## Public Contract

```python
BusinessActivityEngine(
    registration_source: RegistrationSource,          # BAR, read-only
    authorizer: Authorizer,                           # e.g. the existing adapters.AuthorizationAdapter
    manifest_resolver: ManifestResolver | None = None,  # default: UnimplementedManifestResolver
)
async def execute(self, invocation: BusinessActivityInvocation) -> BusinessActivityExecutionResult
```

- **Transport-independent.** Failures are returned as an `ExecutionOutcome`, never raised. Mapping an outcome to HTTP belongs to the invoker.
- **In-process.** It runs within the hosting service (ADR-042 / RO-M1-01).
- **Every result reports all sixteen stages in canonical order.** A result cannot be `COMPLETED` unless every stage completed, and in M1 no path completes.
- **A stage's `COMPLETED` means that the step M1 implements for that stage ran successfully.** It does not mean the stage's full `IMP-001` capability exists. For example, Execution Context Initialization builds only four of ten sections, and Authorization Evaluation is not yet activity-scoped. Overall success needs every required stage to be actually implemented; the result invariant enforces this.

| Outcome | Meaning |
|---|---|
| `NOT_IMPLEMENTED` | Execution reached a stage M1 does not build |
| `ACTIVITY_NOT_REGISTERED` | The registration source answered exactly `False` |
| `AUTHORIZATION_DENIED` | The Authorization Engine returned anything other than `ALLOW` (fail-closed) |
| `VALIDATION_FAILED` | The invocation is structurally invalid (blank identity/organization) |
| `EXECUTION_FAILED` | A collaborator raised, or the registration source answered anything other than a real `bool`; execution failed closed |
| `COMPLETED` | Every stage completed — unreachable in M1 |

## What M1 Does and Does Not Do

| Stage | M1 behaviour |
|---|---|
| Request Reception | Structural validation of the invocation |
| Activity Resolution | `RegistrationSource.is_registered()` (read-only; only a real `True` proceeds, never truthiness), then `ManifestResolver.resolve()`. **The shipped resolver reports `NOT_IMPLEMENTED`**, so real executions end here (Manifest contract: M2) |
| Execution Context Initialization | Builds the immutable context once from the invocation. Activity/Identity/Organization/Runtime are populated; the other six sections are reported unavailable (full context: M3) |
| Authorization Evaluation | Builds an `AuthorizationRequest` and invokes the `Authorizer`. Non-`ALLOW` or an exception fails closed |
| Input Contract Validation … Response Generation | `NOT_IMPLEMENTED` / `NOT_REACHED`. No business rule runs, and no transaction is opened, committed, or rolled back |

Not provided by this package, and never substituted:
- a concrete BAR adapter (M2, `RO-M1-04`);
- Manifest Resolution itself, or any identifier-to-code mapping (M2, `RO-M1-03`);
- durable execution state (M5/M6, `RO-M1-07`);
- an Event Bus, Audit Engine, Notification Platform, Metadata/Workflow Engine, AI Runtime, or Observability Platform (`RO-M1-10`).

There is no scanning, decorator registration, or route discovery of any kind.

## Dependencies

- **Authorization Runtime Engine** (`Backend/Runtime/AuthorizationEngine`): the public contract only (`adapters.authorization_adapter.AuthorizationRequest`, `authorization.models.EvaluationResult` / `AuthorizationDecision`). It is unmodified. Neither package is pip-installable, so a host must make both importable (`TD-165`). This suite uses `pytest.ini`'s `pythonpath`.
- **Correlation:** a host passes its own correlation ID (e.g. AuthService's `CorrelationContext`) as `invocation.correlation_id`. Otherwise one is generated. One structured log record per execution goes to the stdlib logger `business_activity_engine`.

## Running the Tests

```
cd Backend/Runtime/BusinessActivityEngine
python -m pytest
```
