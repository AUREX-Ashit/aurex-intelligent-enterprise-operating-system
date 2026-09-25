# IMP-REPORT-WP-BAE-001 — Business Activity Engine

**Work Package:** WP-BAE-001 — Business Activity Engine (Runtime; no PE-001 capability)
**Governing Readiness Assessment:** `IRA-BAE-001_Business_Activity_Engine_Implementation_Readiness_Assessment.md`
**Governing Work Package Charter:** `WP-BAE-001_Business_Activity_Engine_Charter.md` (milestones M1–M7; this report covers M1 only)
**Governing M1 Analysis:** `architecture/06-Reviews/IRA-BAE-001-M1_Runtime_Contract_and_Gap_Analysis.md` (M1 — COMPLETE WITH CONDITIONS; runtime contract §7)
**Governing Decision:** `ADR-042` — `RO-M1-01` placement, `RO-M1-02` pipeline ordering, `RO-M1-03` Manifest Resolution ownership
**Governing Specification:** `IMP-001 §6.15`–`§6.19`; `RTA-001 §6.6`/`§11.2`/`§11.5`/`§11.13` (LOCKED)
**Scope of this report:** **Milestone M1 — Runtime Contract / Architecture Baseline (skeleton) only.** M2–M7 remain unimplemented and unstarted.

---

## M1 — Runtime Contract / Architecture Baseline

### Authorization

Repository Owner, 2026-09-24: *"RO DECISION: AUTHORIZE WP-BAE-001 M1 SKELETON IMPLEMENTATION."* This authorizes the M1 skeleton only: the package, the transport-independent entry point, BAR-issued identity, the `IMP-001 §6.16` pipeline skeleton, the authorization boundary (existing contract, fail-closed), the read-only BAR boundary, the Manifest Resolution boundary (unimplemented), the transaction-ownership contract, result/error semantics, and observability through existing mechanisms only.

### Milestone Contract

- **Milestone Intent:** establish the BAE Runtime Component and its contracts so that later milestones build on them without redefining the architecture. It does not execute any Business Activity.
- **Input Contract:** `BusinessActivityInvocation`:
  - `identifier`: a `BusinessActivityIdentifier`, i.e. BAR-issued `BA-NNNNNN`, shape-validated;
  - `identity_id` and `organization_id`, derived from caller claims and non-blank;
  - optional `membership_id`, `session_id`, `correlation_id`;
  - a read-only `payload`.
- **Output Contract:** `BusinessActivityExecutionResult`. It carries an `ExecutionOutcome`, the terminating stage, a reason, one `StageReport` per canonical stage in order, and the Authorization Engine's `EvaluationResult` unchanged when authorization was evaluated. A `COMPLETED` outcome is structurally impossible unless all sixteen stages completed.
- **Collaborators (injected):**
  - `RegistrationSource` (BAR, read-only);
  - `ManifestResolver` (default `UnimplementedManifestResolver`);
  - `Authorizer` (structurally satisfied by the existing `AuthorizationAdapter`).

  `TransactionBoundary` is defined as the ownership contract but is not used in M1.

### Governing Architecture Review

`WP-BAE-001` Charter §4–§10, §17; `IRA-BAE-001-M1` §0, §7–§12, §14–§16; `ADR-042`; `IMP-001 §6.15`–`§6.19`; `RTA-001` (§6.5 read for the conflicting order, not followed per `ADR-042`); `Backend/Runtime/AuthorizationEngine` (README, `models.py`, `adapters/authorization_adapter.py`, `engine.py`, `pipeline.py`, test conventions); BAR A–C (`bar_registration` model/repository/service); `BAR-INDEX.md`; AuthService `observability.py`, `middleware/logging.py`, `models/database.py`.

### Files Created

| File | Purpose |
|---|---|
| `Backend/Runtime/BusinessActivityEngine/business_activity_engine/__init__.py` | Public exports |
| `…/business_activity_engine/identity.py` | `BusinessActivityIdentifier`, `InvalidBusinessActivityIdentifierError` |
| `…/business_activity_engine/pipeline.py` | `PipelineStage` (`§6.16.3`, canonical order), `CANONICAL_ORDER`, `StageStatus`, `StageReport` |
| `…/business_activity_engine/context.py` | `BusinessActivityInvocation`, `BusinessActivityContext`, `ContextSection` (`§6.17.5`) |
| `…/business_activity_engine/state.py` | `ExecutionState` (`§6.18.4`), `AUTHORITATIVE_TRANSITIONS` (`§6.18.6`) — vocabulary only |
| `…/business_activity_engine/ports.py` | `RegistrationSource`, `ManifestResolver`/`ManifestResolution`/`UnimplementedManifestResolver`, `Authorizer`, `TransactionBoundary` |
| `…/business_activity_engine/results.py` | `ExecutionOutcome`, `BusinessActivityExecutionResult` |
| `…/business_activity_engine/engine.py` | `BusinessActivityEngine.execute()` |
| `Backend/Runtime/BusinessActivityEngine/tests/test_contracts.py` | Structural contract tests (identity, order, states, sections, result invariants) |
| `…/tests/test_engine.py` | Behavioural tests |
| `…/tests/test_package_boundary.py` | Static AST boundary tests |
| `Backend/Runtime/BusinessActivityEngine/pytest.ini` | `asyncio_mode = auto`; `pythonpath = . ../AuthorizationEngine` |
| `Backend/Runtime/BusinessActivityEngine/README.md` | Public contracts |
| `architecture/05-Implementation/IMP-REPORT-WP-BAE-001_Business_Activity_Engine.md` | This report |

### Files Modified

| File | Change |
|---|---|
| `architecture/06-Reviews/TECH-DEBT.md` | `TD-165` added (packaging/import-path dependency, §19.8.2). No other row changed |

No other file was modified. The AuthorizationEngine, BAR A–C, `BAR-INDEX.md`, the WP-23 Charter, C-024, `IMP-001`, `RTA-001`, `ADR-042`, and ~~the WP-BAE-001 Charter~~ are unchanged. *(Corrected 2026-09-25: this was accurate at M1 implementation time. The WP-BAE-001 Charter was later changed by the F-01 disposition note and the M1-acceptance status updates; see the remediation and acceptance sections below.)*

### Implementation Summary

| Stage (`§6.16.3` order) | M1 behaviour |
|---|---|
| 1 Request Reception | Structural validation. A blank `identity_id`/`organization_id` gives `VALIDATION_FAILED` |
| 2 Activity Resolution | `RegistrationSource.is_registered()` (read-only). Unregistered gives `ACTIVITY_NOT_REGISTERED` (`RO-M1-04`). Then `ManifestResolver.resolve()`; the shipped resolver returns `NOT_IMPLEMENTED` (`RO-M1-03`, contract is M2) |
| 3 Execution Context Initialization | Immutable context built once from the invocation. Activity/Identity/Organization/Runtime populated; Enterprise/Authorization/Workflow/Request/Transaction/AI reported unavailable |
| 4 Authorization Evaluation | `AuthorizationRequest(identity_id, organization_id, membership_id, session_id)` passed to the `Authorizer`. Anything but `ALLOW` gives `AUTHORIZATION_DENIED`; an exception gives `EXECUTION_FAILED` (fail-closed) |
| 5 Input Contract Validation | `NOT_IMPLEMENTED`: execution ends here even on `ALLOW` |
| 6–16 | `NOT_REACHED`. No business rule, persistence, commit, event, notification, audit, or AI hook runs |

Collaborator exceptions are caught at the stage that raised them and reported as `EXECUTION_FAILED`. One structured record per execution goes to the stdlib logger `business_activity_engine`, with the host-supplied or generated correlation ID. No Observability Platform is created.

### Design Decisions Requiring Disclosure

1. **Authorization and BAR boundaries are exercised in M1 through injected ports.**
   - The Charter's M1 exclusions read "No BAR query, no Authorization invocation." The M1 skeleton authorization explicitly requires an authorization boundary with fail-closed behaviour, a read-only BAR boundary, and tests proving DENY prevents business execution.
   - Both are therefore implemented **as injected interfaces only**. The package ships **no concrete BAR adapter**: no BAR table is queried, and the concrete adapter is M2 (`RO-M1-04`). It builds **no Authorization Engine wiring**: no `ResolverRegistry`/resolver is assembled by the BAE, and the host injects an `Authorizer`.
   - No host injects either today, so no BAR query and no Authorization Engine invocation occurs outside the test suite.
   - This is recorded here as the reading adopted to satisfy both instructions. The Charter text is not amended.
2. **Manifest Resolution outcome without schema.** `ManifestResolution` carries only `status` and `reason`, never manifest content, so no manifest schema is invented (`RO-M1-03`). A test double returning `RESOLVED` is used only to exercise stages 3–4.
3. **Execution state is vocabulary only.** The engine does not assign `ExecutionState`. A pre-`Running` termination would need a transition no authoritative source defines (`IRA-BAE-001-M1 §11.2`, U-01/U-02), and `RO-M1-08` forbids inventing one. The outcome is carried by `ExecutionOutcome` instead.
4. *(See the F-04 disposition in the remediation section below.)* **Stage 3 reports COMPLETED for a partial context.** The context is genuinely constructed once from real invocation data. The six sections without a source are named in the stage reason and in `unavailable_sections`, never fabricated (`IRA-BAE-001-M1 §7`, C5). Full context construction remains M3.
5. **Invocation type check fails fast.** A non-`BusinessActivityIdentifier` identifier raises `TypeError` when `BusinessActivityInvocation` is constructed. It is a programming error, not a runtime outcome.

### Test Execution

Interpreter: `Backend/Services/AuthService/venv` (Python 3.14.5, pytest 9.0.3, pytest-asyncio 1.4.0).

| Suite | Result |
|---|---|
| `Backend/Runtime/BusinessActivityEngine` (new) | **71 passed** |
| `Backend/Runtime/AuthorizationEngine` (regression) | **106 passed**, identical to the pre-change baseline |
| AuthService `test_bar_identifier_service.py`, `test_bar_registration_service.py`, `test_authorization_integration.py` (BAR A–C + WP-13) | **33 passed**, identical to the pre-change baseline |
| AuthService full suite | **972 passed**, with `JWT_SECRET_KEY`/`JWT_ALGORITHM` set to throwaway test-only values in the shell (`TD-010`). Without them: 502 failed / 470 passed, every failure confirmed as the `TD-010` "JWT_SECRET_KEY environment variable is not defined" error, unrelated to this change (no AuthService file was touched) |

**Coverage of the ten required proofs:**

| # | Required proof | Tests |
|---|---|---|
| 1 | Entry point exists | `test_entry_point_is_a_single_async_execute_taking_only_an_invocation` |
| 2 | BA identity | `test_bar_issued_identifier_shape_is_accepted`, `test_malformed_identifier_is_rejected`, `test_identity_module_offers_no_way_to_issue_an_identifier`, `test_invocation_requires_a_typed_identifier` |
| 3 | `§6.16` order | `test_pipeline_is_imp_001_6_16_3_in_canonical_order`, `test_pipeline_adds_no_stage_outside_imp_001_6_16_3`, `test_authorization_precedes_every_business_stage` |
| 4 | Unimplemented stage cannot succeed | `test_allow_reaches_the_first_unimplemented_stage_and_does_not_succeed`, `test_no_m1_path_executes_business_rules_or_succeeds` (20 parameter combinations), `test_result_cannot_claim_success_while_any_stage_is_not_completed` |
| 5 | DENY prevents business execution | `test_deny_prevents_business_execution`, `test_real_authorization_engine_with_no_resolvers_denies` (real, unmodified Authorization Engine) |
| 6 | Non-ALLOW fail-closed | `test_every_non_allow_decision_fails_closed` (DENY/CONDITIONAL/DELEGATED/ESCALATED), `test_authorizer_exception_fails_closed` |
| 7 | BAR read-only | `test_bar_is_only_ever_asked_whether_an_identifier_is_registered` (strict double fails on any other access), `test_no_capability_service_or_bar_module_is_imported` |
| 8 | No registration | `test_no_registration_or_identifier_issuance_is_referenced`, `test_unregistered_activity_cannot_execute_and_authorization_is_not_consulted` |
| 9 | Manifest boundary unimplemented | `test_default_manifest_resolution_is_not_implemented_and_stops_execution`, `test_unimplemented_manifest_resolver_never_resolves`, `test_no_discovery_mechanism_is_used` |
| 10 | Failure classes distinct | `test_failure_classes_are_distinct`, plus the per-class tests above and `test_blank_identity_or_organization_is_a_validation_failure`, `test_registration_lookup_failure_fails_closed` |

**Negative control:** a scratch copy of the package, with the authorization check mutated to treat `CONDITIONAL` as `ALLOW`, failed `test_every_non_allow_decision_fails_closed[CONDITIONAL]` (1 failed / 70 passed). This confirms the suite detects a fail-open defect. The copy was deleted, and the repository was never modified by the control.

### Developer Validation

- **Registrations:** none. No Business Activity was registered, no `BA-NNNNNN` identifier was assigned, and `bar_registration`/`bar_identifier_ledger` were not written. The identifier values in the tests are shape-valid literals only.
- **Unchanged:** BAR A–C source and `BAR-INDEX.md` (hash-verified); WP-23 Charter, including Workstream D (deferred) and Workstream E; C-024 BA-01 (unregistered).

### Technical Debt

- **`TD-165` (new, Medium):** the Runtime packages are not pip-installable, so a host must place both package roots on its import path.
- **Pre-existing, referenced:** `TD-010` (AuthService test environment variables).

### Independent Review

~~Not performed. Per `CLAUDE.md §19.7`, M1 must be submitted for independent review before M2 begins.~~ *(Updated 2026-09-25.)* Performed by a fresh-context reviewer: **PASS WITH CONDITIONS** (`architecture/06-Reviews/IRA-BAE-001-M1_Independent_Review.md`). Its conditions and their remediation are recorded in §"M1 — Independent Review Remediation" below. The remediation is itself subject to a further fresh-context review.

### Certification Status

~~Not certified. Implementation Status: **IMPLEMENTATION COMPLETE — awaiting independent review.**~~ *(Updated 2026-09-25.)* ~~Implementation Status: **REMEDIATION APPLIED — awaiting independent verification of remediation.** M1 is **not accepted** and **not committed**; the `CLAUDE.md §19.7` completion gate is not yet satisfied.~~ *(Updated 2026-09-25 — M1 accepted by the Repository Owner.)* Implementation Status: **M1 ACCEPTED — COMPLETE.** See §"M1 — Acceptance and Closure". Work Package certification under `§19.7b` has not occurred.

### Repository Commit

~~Not committed. Nothing staged or pushed.~~ *(Updated 2026-09-25 — M1 accepted by the Repository Owner.)* Committed in the WP-BAE-001 M1 acceptance/closure commit (see `git log`). Not pushed.

### Deferred to Later Milestones

| Milestone | Deferred items |
|---|---|
| M2 | Minimum manifest contract and identifier-to-implementation binding (`RO-M1-03`); per-datum resolution sources (`RO-M1-05`); BAE ↔ Workstream E interface and concrete BAR adapter (`RO-M1-04`); per-BA authorization-policy source |
| M3 | Full context construction; Input Contract/Business Validation |
| M4 | Per-BA resolver binding; host wiring of the real Authorization Engine; non-`ALLOW` → `Waiting` mapping (U-10) |
| M5 | Persistence Coordination; Transaction Commit through `TransactionBoundary`; post-commit processing; audit timing (`RO-M1-09`); `R-01` |
| M5/M6 | Durable execution state (`RO-M1-07`); transition set U-01–U-10 (`RO-M1-08`) |
| M6 | Response generation; `§6.28` error classification (D-06); `§6.27` telemetry (D-05); AI hooks |
| M7 | First real consumer; `RO-M1-11`; ~~`TD-165` resolution~~ *(TD-165 re-targeted to M2, 2026-09-25 — see remediation section)* |

---

## M1 — Independent Review Remediation (2026-09-25)

**Input:** `architecture/06-Reviews/IRA-BAE-001-M1_Independent_Review.md` — **PASS WITH CONDITIONS**, findings F-01–F-08.
**Authorization:** Repository Owner remediation instruction, 2026-09-25. It covers remediation of F-01–F-08 only and explicitly excludes M2 and any later-milestone work.
**Status:** ~~remediation applied; **awaiting independent verification of remediation** (`CLAUDE.md §19.7b` gate 4 practice). M1 is not accepted and not committed.~~ *(Updated 2026-09-25 — M1 accepted by the Repository Owner.)* Remediation **independently verified** (`architecture/06-Reviews/IRA-BAE-001-M1_Remediation_Independent_Review.md`, VERIFIED). M1 accepted.

### Repository Owner Disposition — F-01

Recorded as given by the Repository Owner:

> The explicit M1 implementation authorization given in the current session authorized the M1 skeleton to include a read-only BAR registration boundary/check, and invocation of the existing AuthorizationEngine boundary, despite the earlier Charter wording that excluded BAR queries and authorization invocation from M1.
>
> This later explicit M1 authorization supersedes those two earlier M1 exclusions ONLY for this narrow M1 skeleton boundary.
>
> It does NOT authorize: a concrete BAR adapter, BAR registration, Business Activity Identifier issuance, Workstream E execution gating, manifest implementation, discovery, host-service integration, capability implementation, durable execution state, M2 work, M3/M4/M5/M6 work beyond what was explicitly required for the M1 skeleton.

**Classification:** documentation/governance-record inconsistency, **not** an implementation governance violation.

**Where recorded:**
- here;
- a disposition note under Charter §10 M1. The original Charter exclusion text is preserved unchanged; no milestone scope is otherwise amended.

**The M1 implementation authorization items this disposition refers to (2026-09-24, given in conversation), verbatim:**
- "5. Authorization boundary: integrate only with the existing AuthorizationEngine contract; BAE constructs/provides the required authorization context; AuthorizationEngine remains the sole authorization decision authority; fail closed for any non-ALLOW decision."
- "6. BAR boundary: establish a read-only integration abstraction/interface for obtaining authoritative registration information; do not duplicate BAR registration logic; do not modify BAR A–C; do not register any Business Activity."
- "7. Manifest boundary: define the M1-level abstraction/interface for Manifest Resolution; do NOT implement actual identifier-to-code resolution; do NOT create a manifest registry; do NOT use scanning, decorators, filesystem discovery, FastAPI route discovery, or heuristics."
- "8. Transaction boundary: define the BAE ownership contract established by M1; do not create the durable execution-state table yet; do not redesign the existing session manager."
- Required tests: "5. Authorization DENY prevents business execution. 6. Authorization non-ALLOW is fail-closed. 7. BAR integration is read-only from BAE."

### F-02 — Registration prerequisite now fails closed

- **Change:** `engine.py`, Activity Resolution.
  - `if not registered:` (truthiness) is replaced by strict identity checks.
  - `registered is False` → `ACTIVITY_NOT_REGISTERED`.
  - Any value that `is not True` → `EXECUTION_FAILED`. The reason names the returned type only, never its value.
  - Only a real `True` proceeds.
- **Docstrings updated:** `engine.py`, `ports.py` (`RegistrationSource`), `results.py` (`EXECUTION_FAILED`).
- **Outcome class for non-bool answers:** `EXECUTION_FAILED`, not `ACTIVITY_NOT_REGISTERED`. A malformed answer is a failure of the registration source, not a statement from BAR that the activity is unregistered. This includes `None` and an implicit no-return; both are fail-closed.
- **Not changed:** the BAR boundary remains a read-only Protocol. No BAR adapter was built, WP-23 Workstream C was not touched, and nothing was registered.

**Tests added** (`tests/test_engine.py`):

| Test | Covers |
|---|---|
| `test_registration_true_proceeds_past_activity_resolution` | True proceeds |
| `test_registration_false_stops_with_activity_not_registered` | False stops with `ACTIVITY_NOT_REGISTERED` |
| `test_non_boolean_registration_result_fails_closed` (13 cases) | `None`, `"false"`, `"False"`, `"0"`, `"true"`, `""`, `1`, `0`, `{}`, `[]`, a truthy dict, `object()`, `MagicMock()` — each gives `EXECUTION_FAILED` at Activity Resolution, with the authorizer never consulted |
| `test_missing_registration_result_fails_closed` | A lookup that returns nothing |
| `test_default_async_mock_registration_source_fails_closed` | Default `AsyncMock` source |
| `test_registration_source_without_the_lookup_method_fails_closed` | Missing method |

**Negative control** (run against a scratch copy of the pre-fix package, never the repository): **15 failed / 78 passed**.
- Fail-open cases that the pre-fix engine let through to Authorization: `"false"`, `"False"`, `"0"`, `"true"`, `1`, a truthy dict, `object()`, `MagicMock`, default `AsyncMock`.
- Cases where the pre-fix engine stopped, but reported `ACTIVITY_NOT_REGISTERED` rather than a malformed-answer failure: `None`, implicit no-return, `0`, `""`, `{}`, `[]`.
- Reverting only the fix in a scratch copy of the fixed code reproduced the same 15 failures.

### F-03 — Mutation-catching tests

**Tests added** (`tests/test_engine.py`):
- `test_identity_and_organization_come_from_the_invocation_claims_never_the_payload`: a payload carrying spoofed `identity_id`/`organization_id`/`membership_id`/`session_id` must not change the `AuthorizationRequest`, which is built from the context.
- `test_payload_never_fills_in_a_blank_claim` (2 cases): a blank claim with the value present in the payload is still `VALIDATION_FAILED`, and neither BAR nor the authorizer is consulted.
- `test_manifest_resolver_exception_fails_closed_without_escaping`: a raising resolver gives `EXECUTION_FAILED` at Activity Resolution (stage `TERMINATED`, reason names Manifest Resolution), the exception does not escape, and the authorizer is not consulted.

**Mutation experiments** (scratch copies only, each deleted after its run):

| Mutation | Against pre-fix code (plus new suite) | Against fixed code | Catching test |
|---|---|---|---|
| M4 — organization taken from the payload for the authorization request | caught | 1 failed / 92 passed | `test_identity_and_organization_come_from_…` |
| M10 — identity taken from the payload into the context | caught | 1 failed / 92 passed | `test_identity_and_organization_come_from_…` |
| M9 — try/except around Manifest Resolution removed | caught | 1 failed / 92 passed | `test_manifest_resolver_exception_fails_closed_without_escaping` |

M11 (log record) is not in the F-03 scope; see F-07 below.

### F-04 — Stage-status semantics (clarified, not redesigned)

- A stage's `COMPLETED` means **the step M1 implements for that stage executed successfully**. It does not mean the stage's full `IMP-001` capability is complete.
  - Stage 3 builds four of the ten `§6.17.5` sections.
  - Stage 4 is not yet activity-scoped (review O-01).
- An execution can never report successful Business Activity completion until every required stage is actually implemented. `BusinessActivityExecutionResult` rejects a `COMPLETED` outcome unless all sixteen stage reports are `COMPLETED`, and no M1 path reaches that.
- M1 skeleton behaviour is retained unchanged. No new status value and no lifecycle transition was introduced.
- The same clarification is recorded in the package `README.md`.

### F-05 — Context-model disclosure

**Actually implemented:** `BusinessActivityContext` has seven fields:

| Field | Source |
|---|---|
| `identifier` | Activity |
| `identity_id`, `membership_id`, `session_id` | Identity |
| `organization_id` | Organization |
| `correlation_id`, `started_at` | Runtime |

It also has a `ContextSection` enum naming all ten `§6.17.5` sections, an `AVAILABLE_SECTIONS` constant (Activity, Identity, Organization, Runtime), and an `unavailable_sections` property.
- Each "available" section holds only part of its `§6.17.6`–`§6.17.15` content (e.g. Identity has no Business Roles, Approval Authorities, Delegations or Authentication Method; Runtime has no Trace ID or performance metrics).

**Unavailable in M1:**
- the Enterprise, Authorization, Workflow, Request, Transaction and AI sections;
- a sectioned (nested) context model;
- a transaction-context type (`§6.17.13`).

Only the `TransactionBoundary` commit/rollback ownership Protocol exists, and it satisfies authorization item 8's "ownership contract" only.

**Deferred:**
- the full context model to M3 (Context Construction);
- the transaction-context type to the milestone that implements transaction semantics (M5).

Recorded as `TD-166`. **The M1 context model is not complete and is not claimed to be.**

### F-06 – F-08 — Low findings (no separate remediation)

Recorded as deferred improvements. No code changed for them.

| Finding | Register entry | Planned resolution |
|---|---|---|
| F-06 — `execute()` can raise on malformed collaborator return values; always fail-closed | `TD-167` | M2/M4 |
| F-07 — low-evidential-weight tests; log record untested (M11) | `TD-168` | M6 for the log test |
| F-08 — raw exception text in `result.reason` | `TD-169` | M6 error contract, before any invoker exposes `reason` |

These are recorded in the register as well as here per `CLAUDE.md §19.8.2`. None triggers M2 work.

### TD-165

Planned Resolution corrected from "no later than … M7's first-consumer integration" to **M2**, per review §6/O-04: a host-side concrete BAR adapter would first need to import the BAE. The original wording is quoted in the entry. No other part of TD-165 changed.

### Files Changed by This Remediation

| File | Change |
|---|---|
| `Backend/Runtime/BusinessActivityEngine/business_activity_engine/engine.py` | F-02 strict registration check; docstring |
| `…/business_activity_engine/ports.py` | `RegistrationSource` docstring |
| `…/business_activity_engine/results.py` | `EXECUTION_FAILED` docstring |
| `…/tests/test_engine.py` | F-02 and F-03 tests (22 new cases) |
| `Backend/Runtime/BusinessActivityEngine/README.md` | Status; F-02 semantics; F-04 clarification |
| `architecture/05-Implementation/WP-BAE-001_Business_Activity_Engine_Charter.md` | F-01 disposition note under §10 M1; original text preserved |
| `architecture/05-Implementation/IMP-REPORT-WP-BAE-001_Business_Activity_Engine.md` | This section; status updates |
| `architecture/06-Reviews/TECH-DEBT.md` | TD-165 Planned Resolution corrected; `TD-166`–`TD-169` added |

### Test Execution (after remediation)

| Suite | Result |
|---|---|
| BAE | **93 passed** (71 original + 22 new) |
| AuthorizationEngine | **106 passed** |
| AuthService BAR A–C + WP-13 | **33 passed** |
| AuthService full suite | **972 passed**, with throwaway test-only `JWT_SECRET_KEY`/`JWT_ALGORITHM` in the test process only (`TD-010`) |

All runs used `PYTHONDONTWRITEBYTECODE=1` and `-p no:cacheprovider`. No mutation or probe artifact exists in the repository.

### Scope Protection

- No M2 work was started. No Manifest Resolution design or implementation, BAR adapter, registration, identifier assignment, Workstream D/E work, durable state, state machine, host integration, migration, events, notifications, audit infrastructure or AI assistance was added.
- Unchanged: AuthorizationEngine, `IMP-001`, `ADR-042`, the WP-23 Charter, C-024, BAR A–C, `BAR-INDEX.md`.

---

## M1 — Acceptance and Closure (2026-09-25)

**Repository Owner decision, 2026-09-25:** *"I ACCEPT WP-BAE-001 M1."*

| Item | Status |
|---|---|
| M1 — Runtime Contract / Architecture Baseline (skeleton) | **ACCEPTED — COMPLETE** |
| Independent review | `architecture/06-Reviews/IRA-BAE-001-M1_Independent_Review.md` — PASS WITH CONDITIONS (unchanged) |
| Independent verification of remediation | `architecture/06-Reviews/IRA-BAE-001-M1_Remediation_Independent_Review.md` — **VERIFIED**; zero Critical/High/Medium/Low findings (unchanged) |
| Open Critical/High/Medium/Low review findings | **None.** F-01 dispositioned; F-02 and F-03 remediated and verified; F-04 and F-05 disclosed, with F-05 deferred as `TD-166`; F-06–F-08 deferred as Low debt `TD-167`–`TD-169` |
| Evidence relied upon | BAE 93 passed; AuthorizationEngine 106; AuthService BAR A–C + WP-13 33; AuthService full suite 972. Each was reproduced by the remediation reviewer. The closure changes are status/documentation only; the BAE suite was re-run at closure |
| **M2** | **NOT AUTHORIZED. NOT STARTED.** |
| M3–M7 | Not started |
| Business Activity Engine as a whole | **Not complete.** Only M1 is complete |
| Work Package `§19.7b` closure gates (Certification, V&V Audit, Release Readiness) | Not performed; they apply at Work Package closure |

**Status updates made at closure** (historical wording preserved, struck through):
- this report;
- `WP-BAE-001` Charter (header Status, §10 closing line, §17 authorization/milestone/verification lines);
- the package `README.md` Status line;
- `IRA-BAE-001-M1` Status line.

Unchanged at closure: both independent review artifacts, the F-01 disposition, `ADR-042`, `IMP-001`, `RTA-001`, the WP-23 Charter, C-024, BAR A–C, and `BAR-INDEX.md` (zero registrations).

**Not updated:** the `WPR-001 §2a` WP-BAE-001 row still reads "IMPLEMENTATION NOT YET AUTHORIZED". `WPR-001` also carries uncommitted changes from other Work Packages and was not named in the closure instruction, so it is left for a separate roadmap update.
