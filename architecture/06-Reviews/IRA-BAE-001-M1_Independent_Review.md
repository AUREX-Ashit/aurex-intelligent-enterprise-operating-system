# IRA-BAE-001-M1 — Independent Review of the WP-BAE-001 M1 Skeleton Implementation

**Document ID:** IRA-BAE-001-M1-IR
**Work Package / Milestone:** `WP-BAE-001` (Business Activity Engine), M1 — Runtime Contract / Architecture Baseline (skeleton implementation)
**Review type:** `CLAUDE.md §19.7` Independent Review of a milestone reported "IMPLEMENTATION COMPLETE — awaiting independent review". It is not Independent Certification (Gate 1) or a V&V Audit (Gate 2) under `§19.7b`. Those apply at Work Package closure.
**Date:** 2026-09-24
**Overall disposition:** **PASS WITH CONDITIONS** (§10)
**M2 gate:** **M2 is NOT authorized by the evidence currently available** (§11)

---

## 1. Review Authority and Independence Statement

- The Repository Owner's "MANDATORY INDEPENDENT REVIEW — WP-BAE-001 M1" brief commissioned this review.
- The reviewer is a fresh-context agent. It did not write, design, or test any of the code or documents under review, and it did not take part in the M1 analysis (`IRA-BAE-001-M1`), `ADR-042`, or the M1 skeleton implementation.
- The implementation report's conclusions were not relied on. Every material claim below was checked by:
  - reading source and test code directly;
  - re-running the test suites;
  - running from-scratch runtime probes that were not adapted from the existing suite (§8.3);
  - running mutation-based negative controls on a disposable copy (§8.4).
- **Constraints observed:**
  - No repository file was modified except this new artifact.
  - Nothing was staged, committed, stashed, checked out, or pushed.
  - Probes and mutations ran only in the session scratchpad. The mutation copy was deleted after use.
  - Test runs used `PYTHONDONTWRITEBYTECODE=1` and `-p no:cacheprovider`.
  - Throwaway JWT values existed only in the test process environment and were never written to a file (`TD-010`).
- Where a finding needs a governance decision, this review records it for the Repository Owner (RO) and does not decide it (`CLAUDE.md §16`, §17).

## 2. Sources Examined

| # | Source | Extent |
|---|---|---|
| 1 | `architecture/05-Implementation/WP-BAE-001_Business_Activity_Engine_Charter.md` | Full |
| 2 | `architecture/06-Reviews/IRA-BAE-001-M1_Runtime_Contract_and_Gap_Analysis.md` | Full (§0–§17) |
| 3 | `architecture/07-Decisions/ADR-042_…_Manifest_Resolution_Ownership.md` | Full |
| 4 | `architecture/03-Engineering/IMP-001_Implementation_Playbook.md` | `§6.16.3`–`§6.16.7`, `§6.17.4`–`§6.17.8`, `§6.17.13`–`§6.17.15`, `§6.18.5`–`§6.18.6`, section index `§6.16`–`§6.19` |
| 5 | `architecture/02-Constitutional/RTA-001 - Runtime Architecture and Execution.md` (LOCKED) | `§6.6`, `§6.7`, `§11.5`–`§11.8`, `§11.13` |
| 6 | `CLAUDE.md` | `§16`–`§19.8.7`, `§21.4` |
| 7 | `architecture/05-Implementation/IMP-REPORT-WP-BAE-001_Business_Activity_Engine.md` | Full |
| 8 | `architecture/06-Reviews/TECH-DEBT.md` | `TD-165` row; `TD-071`; working-tree diff |
| 9 | `Backend/Runtime/AuthorizationEngine/` | `README.md` (and its working-tree diff), `adapters/authorization_adapter.py`, `authorization/models.py` |
| 10 | BAR A–C: `Backend/Services/AuthService/{models,repositories,services}/bar_*.py`, both `bar_*` Alembic migrations, `tests/test_bar_*.py`; `architecture/00-Governance/BAR-INDEX.md` | Timestamps; seeding grep; BAR-INDEX `§7` |
| 11 | `architecture/05-Implementation/WP-23_Enterprise_BAR_Mechanism_Implementation_Charter.md` | `§8`–`§12` |
| 12 | WP-RTA-001 material: `WP-RTA-001_Authorization_Runtime_Engine.md` (timestamp and status only); `Backend/Services/AuthService/dependencies.py::enforce_domain_permission`; `authz_integration/runtime_engine_path.py` | As cited |
| 13 | The RO's M1 skeleton implementation authorization | The verbatim scope items 5–8, required tests 5–7, and stop conditions supplied with the review brief. No repository file holds this text (§5.2) |

## 3. Implementation Examined

**Package** `Backend/Runtime/BusinessActivityEngine/`. All files are untracked, created 2026-09-24 13:08–13:11, and read in full:

- `business_activity_engine/__init__.py`, `identity.py`, `pipeline.py`, `context.py`, `state.py`, `ports.py`, `results.py`, `engine.py`
- `tests/test_contracts.py`, `tests/test_engine.py`, `tests/test_package_boundary.py`
- `pytest.ini`, `README.md`

**Other files attributed to M1 by the implementation report:**
- `TECH-DEBT.md` — `TD-165` row, file mtime 13:12
- `IMP-REPORT-WP-BAE-001` — mtime 13:28

**Timeline, from file timestamps.** Every file modified on 2026-09-24 falls into two groups:

| Group | Time | Files |
|---|---|---|
| (a) Pre-M1 | 11:54–12:37 | `RO-M1-12` corrections to the Charter, `WP-RTA-001`, and the AuthorizationEngine `README.md`; the `IRA-BAE-001-M1` revision; `ADR-042` |
| (b) M1 implementation | 13:08–13:28 | The BAE package, `TECH-DEBT.md`, the IMP-REPORT |

No other file in the working tree changed on 2026-09-24. This is consistent with the report's "Files Created/Modified" tables.

## 4. Evidence-Based Findings by Review Area

### A. Runtime placement — CONFORMS

- The package sits at `Backend/Runtime/BusinessActivityEngine/`, a peer of `Backend/Runtime/AuthorizationEngine/`.
- It is a plain in-process library. It has no server, no network client, and no entry point other than `BusinessActivityEngine.execute()`.
- This conforms to `ADR-042` / `RO-M1-01`.
- No host service imports it: a grep of `Backend/Services` and `Backend/Shared` for `business_activity_engine`/`BusinessActivityEngine` returned zero hits.

### B. Invocation boundary — CONFORMS, with one robustness gap (F-06)

- **One entry point.** The only public engine attribute is `execute` (probe P15). Its signature is `(self, invocation)` and it is async.
- **No FastAPI dependency.** The AST scan in the test and direct reading of every import agree: the runtime core imports no FastAPI, Starlette, httpx, requests, SQLAlchemy, Alembic, or asyncpg.
- **No database or session ownership.** No session, engine, or repository is created or accepted. `TransactionBoundary` is a `Protocol` that is never referenced by `engine.py`.
- **Result/error boundary.**
  - Collaborator exceptions are caught at stages 2 and 4 and returned as `EXECUTION_FAILED`.
  - Malformed collaborator *return values* are not contained, and `execute()` then raises (F-06):
    - a resolver returning `None`;
    - an authorizer returning `None`;
    - a decision given as a plain string.
  - Every such case still fails closed; none produces success.
  - `BaseException` (for example `CancelledError`) propagates, which is correct.

### C. Business Activity identity — CONFORMS

- `BusinessActivityIdentifier` validates the pattern `BA-\d{6}` with `fullmatch` and a `str` type check. It is frozen.
- Its only public attribute is `value`.
- No allocation, issuance, reservation, or BAR call exists anywhere in the package.
- `BusinessActivityInvocation` refuses a raw string identifier (`TypeError`).
- Tests use shape-valid literals only. No registration side effect is possible, because the package cannot reach BAR or any database.

### D. Pipeline — CONFORMS

- `PipelineStage` matches `IMP-001 §6.16.3` verbatim and in order. The reviewer compared it line by line against IMP-001 lines 2699–2736.
- `engine.py` walks stages 1 → 2 → 3 → 4 in that order.
- `_Run._append` raises if any stage is reported out of canonical order. Mutation M6, which consults authorization before registration, failed 5 tests.
- **Knowledge Graph Update** (`R-01`) is absent, and a test asserts its absence. Deferral is preserved.
- **Unimplemented stages cannot report success.**
  - `BusinessActivityExecutionResult.__post_init__` enforces three rules:
    - `COMPLETED` if and only if all sixteen stages are `COMPLETED`;
    - `terminated_at is None` if and only if `COMPLETED`;
    - canonical coverage and order of the stage reports.
  - The furthest any M1 path reaches is `NOT_IMPLEMENTED` at `INPUT_CONTRACT_VALIDATION`.
  - Probe P13 confirmed that an all-completed report set with a non-`COMPLETED` outcome is also rejected.
- **No hidden bypass path.** There is one public method, and the private `_run_pipeline` is the same pipeline. No stage 5+ logic exists to be reached.
- **Partial-completion semantics.** Stage 3 (and stage 4 on `ALLOW`) reports `COMPLETED` although only partially realised. See F-04.

### E. Activity Resolution — CONFORMS

- BAR is reached only through the injected `RegistrationSource.is_registered()` Protocol. No concrete BAR adapter ships.
- Nothing in the package imports AuthService, a BAR model, repository, or service, or any `register` symbol.
- There is no scanning, decorator, filesystem, route, or heuristic discovery: no `importlib`, `pkgutil`, `os`, `glob`, `sys`, `__import__`, or `__subclasses__`, confirmed by reading every import.
- The shipped `UnimplementedManifestResolver` always returns `NOT_IMPLEMENTED`. Mutation M2, which made it return `RESOLVED`, failed 2 tests.
- `ManifestResolution` carries only `status`/`reason`, so no manifest schema is invented. The Manifest Resolution boundary remains explicitly deferred to M2 (`RO-M1-03`).
- **Robustness gap.** The registration check uses truthiness (`if not registered`), so any truthy non-`bool` return is treated as "registered" (F-02).

### F. Authorization — CONFORMS, with a disclosed deferral (O-01)

- The engine uses the existing public contract unmodified:
  - `adapters.authorization_adapter.AuthorizationRequest`;
  - `authorization.models.AuthorizationDecision` / `EvaluationResult`;
  - structural `Authorizer` Protocol, satisfied by `AuthorizationAdapter`.
- There is no precedence logic, `ResolverRegistry` assembly, or tier resolver in the BAE.
- **ALLOW is the only path that proceeds.** The check is `evaluation.decision is not AuthorizationDecision.ALLOW`, an identity comparison.
  - DENY, CONDITIONAL, DELEGATED, and ESCALATED each yield `AUTHORIZATION_DENIED`.
  - A plain string `"ALLOW"` or a `MagicMock` result does not pass (probes P6, P7).
  - Mutation M5, which treated CONDITIONAL as ALLOW, was caught.
- **Engine exceptions never become success.** An authorizer raising yields `EXECUTION_FAILED`. Mutation M3, which converted an exception into ALLOW, was caught.
- **Real engine.** The unmodified real engine with an empty `ResolverRegistry` returns DENY through the BAE (re-run).
- **AuthorizationEngine unchanged.** The git diff for `Backend/Runtime/AuthorizationEngine/` is limited to `README.md`, the pre-M1 `RO-M1-12` correction at 11:55. All code is git-clean. The AuthorizationEngine suite passed 106/106.

### G. Context — PARTIALLY CONFORMS (F-04, F-05)

What conforms:
- The context is built once, by the engine, after Activity Resolution and before Authorization (C5, `§6.16.6`).
- It is frozen. Identity and organization come from the invocation's claim fields, never from the payload (probe P12).
- Nothing is fabricated. Six sections are reported as unavailable, both in `unavailable_sections` and in the stage-3 reason text.

What does not fully conform:
- **Sections are binary.** `AVAILABLE_SECTIONS` is a static class constant. ACTIVITY, IDENTITY, ORGANIZATION, and RUNTIME are declared "available" although each holds only one to three fields of the `§6.17.6`–`§6.17.15` content. For example, the Activity Context holds only the identifier, with no name, version, domain, activity type, invocation source, or execution mode.
- **No ten-section model.** The IRA-M1 §15 skeleton contract calls for "a ten-section context model". What is implemented is a flat seven-field dataclass plus a section-name enum.
- **No transaction-context shape.** The `§6.17.13` transaction-context shape, also required by §15, is not implemented.
- **Undisclosed.** The IMP-REPORT does not disclose these gaps (F-05).

### H. Result/error semantics — CONFORMS

`ExecutionOutcome` keeps the classes distinct. Each is produced at a distinct stage by a distinct cause, and each has a dedicated test.

| Outcome | Stage | Cause |
|---|---|---|
| `VALIDATION_FAILED` | Request Reception | Blank or non-`str` identity/organization |
| `ACTIVITY_NOT_REGISTERED` | Activity Resolution | Registration source reports not registered |
| `AUTHORIZATION_DENIED` | Authorization Evaluation | Any non-ALLOW decision |
| `NOT_IMPLEMENTED` | Activity Resolution or Input Contract Validation | Manifest not resolved, or first unbuilt stage reached |
| `EXECUTION_FAILED` | Stage 2 or stage 4 | A collaborator raised |

**Caveats:**
- The resolver-raises path has no test (mutation M9 survived).
- Exception text is copied into `result.reason` (F-08).

### I. Transaction boundary — CONFORMS

- `TransactionBoundary` declares `commit`/`rollback` only and is never called.
- The README and the module docstring state that the M1 engine opens no transaction.
- No commit, rollback, or session code exists.
- The implementation does not claim to own or execute commits in M1.

### J. State — CONFORMS

- `ExecutionState` holds the nine `§6.18.4` names verbatim.
- `AUTHORITATIVE_TRANSITIONS` holds exactly the ten `§6.18.6` pairs. The reviewer checked it against IMP-001 lines 3613–3639.
- `engine.py` never imports `state.py`: no state is assigned and no transition is performed.
- No U-01/U-02 or other unsupported transition is introduced (`RO-M1-08`).

### K. Observability — CONFORMS

- There is one JSON line per execution to the stdlib logger `business_activity_engine`, plus `logger.exception` on collaborator failure.
- A host-supplied correlation ID is carried. Otherwise a `uuid4` is generated (O-03).
- No Event Bus, Audit Engine, Notification Platform, Observability Platform, metrics, or telemetry sink is created or claimed.
- AuthService `observability.py` is not imported, consistent with `RO-M1-10` / IRA-M1 §6.
- No test covers the log record (mutation M11 survived; LOW, F-07).

### L. Tests — see §8

## 5. Charter / Authorization Reconciliation (Critical Governance Question #1)

### 5.1 What the Charter actually says

`WP-BAE-001` Charter §10 M1 says:

- **Objective:** a "skeleton pipeline structure … each honestly stubbed/reported", plus the `BusinessActivityContext`/`BusinessActivityState`/`BusinessActivityTransaction` model shapes, "with no concrete stage logic and no consumer wired".
- **Outputs:** "no live invocation path".
- **Verification:** "Structural tests only (model shape, pipeline stage enumeration) — no behavioral claim".
- ***Explicit exclusions:* "No BAR query, no Authorization invocation, no persistence, no real consumer."**

Related Charter text:
- Authorization Context construction and AuthorizationEngine invocation are **M4** scope (§10 M4).
- M3 explicitly excludes "Authorization Context construction yet (M4)".

`IRA-BAE-001-M1 §15` restates the M1 skeleton identically: "the sixteen … stages …, each reporting `NOT_IMPLEMENTED`; structural tests only". §16 Condition 3 requires separate RO authorization. The Charter's status lines still read "No milestone has begun" (a known stale item, IRA-M1 §16 Condition 2).

### 5.2 What the explicit M1 implementation authorization authorized

The RO's authorization was given in conversation. The verbatim text relevant here was supplied with the brief. The repository holds only a summary paraphrase, in the IMP-REPORT's "Authorization" section.

- **Item 5 — authorization boundary:** "integrate only with the existing AuthorizationEngine contract; BAE constructs/provides the required authorization context; AuthorizationEngine remains the sole authorization decision authority; fail closed for any non-ALLOW decision."
- **Item 6 — BAR boundary:** "establish a read-only integration abstraction/interface for obtaining authoritative registration information; do not duplicate BAR registration logic; do not modify BAR A–C; do not register any Business Activity."
- **Item 7 — Manifest boundary:** abstraction/interface only; no resolution, registry, scanning, or discovery.
- **Item 8 — Transaction boundary:** "define the BAE ownership contract"; no durable-state table.
- **Required tests:** "5. Authorization DENY prevents business execution. 6. Authorization non-ALLOW is fail-closed. 7. BAR integration is read-only from BAE."
- **Stop conditions:**
  - (5) the skeleton "would require implementing a deferred **M2/M5/M6** responsibility";
  - (4) "a new governance decision is required to choose between materially different implementation architectures".

### 5.3 Is the implementation's interpretation legitimate?

**Evidence for the implementation's reading:**
- The RO is the authority that approved the Charter (Charter §17). The Charter itself says no milestone may begin without a separate RO implementation authorization, so the milestone-level authorization is where M1's operative scope is fixed.
- Items 5–6 and required tests 5–7 cannot be met with "no behavioural claim" and no authorization or BAR interaction at all. Proving "DENY prevents business execution" needs an execution path that consumes a decision.
- The authorization's stop condition 5 names M2/M5/M6 only. Authorization integration is M4 and context construction is M3, so stop condition 5 was not literally triggered.
- The implementation kept the footprint minimal:
  - ports only;
  - no concrete BAR adapter;
  - no resolver wiring;
  - no host;
  - no BAR query or Authorization Engine invocation outside the test suite.
- The divergence is disclosed ("Design Decisions Requiring Disclosure", item 1) and the Charter was not silently amended.

**Evidence against, or unresolved:**
- The literal Charter M1 exclusions, verification method, and "no live invocation path" output are not what was built. `execute()` is a live, callable invocation path. The suite makes behavioural claims. One test (`test_real_authorization_engine_with_no_resolvers_denies`) invokes the real Authorization Engine pipeline, which is more than an "interface".
- Parts of M3 (context construction) and M4 (authorization request construction and invocation) were brought forward into M1. The Charter's M3 exclusion ("No Authorization Context construction yet (M4)") is now contradicted by delivered code.
- The implementer, not the RO, chose which source prevails ("the reading adopted to satisfy both instructions"). `CLAUDE.md §16` says conflicting canonical texts must not be resolved by assumption. Under the brief's instruction, newer does not win automatically.
- The authorization text that the implementation relies on is not in the repository. A future reviewer or M2 §19 checklist reading the Charter alone would find M1 non-conforming.

### 5.4 Conclusion

- **Classification: documentation inconsistency that requires RO disposition.** The later RO authorization explicitly required a fail-closed authorization boundary, a read-only BAR interface, and behavioural tests proving DENY stops execution. The delivered scope stays within those items and within its stop conditions.
- **Not an implementation deviation from the operative authorization, and not a governance violation.** The divergence was disclosed rather than hidden, and no code is used outside tests.
- **What remains open is for the RO alone:**
  - (a) whether the M1 authorization is confirmed as superseding Charter §10 M1's exclusions, verification method, and "no live invocation path", and IRA-M1 §15's "structural tests only / each reporting NOT_IMPLEMENTED";
  - (b) whether the M3/M4 elements brought forward are accepted as M1 deliverables;
  - (c) whether the authorization text is recorded verbatim in the repository and the Charter M1/M3/M4 text corrected.
- This review does not decide (a)–(c).

## 6. TD-165 Assessment (Critical Governance Question #2)

**What it represents.**
- Neither Runtime package is pip-installable.
- The BAE imports the AuthorizationEngine's public types as top-level packages, `adapters` and `authorization`.
- Every host must therefore put both package roots on `sys.path`.
- The BAE suite does this via `pytest.ini`. AuthService does it for the AuthorizationEngine via `authz_integration/runtime_engine_path.py`.
- The reviewer confirmed the claim that no prior register entry existed: `runtime_engine_path`/`pyproject`/`pip-installable` appear in `TECH-DEBT.md` only in `TD-165`.

**Does it block M1 certification?** No.
- It is packaging and deployability debt.
- Both suites run.
- No host consumes the BAE, so nothing is broken today.
- It is correctly outside `§19.8.5`'s non-deferrable list.
- The Medium rating matches the `§19.8.7` rubric.

**Does it affect M2?** Potentially yes, in design though not as a blocker.
- M2 delivers the concrete BAR-backed `RegistrationSource` (`RO-M1-04`).
- BAR lives in AuthService, and the BAE is forbidden from importing AuthService (boundary test). Any concrete adapter or integration test therefore lives host-side, and AuthService must then import `business_activity_engine`.
- That makes TD-165 live at M2, not M7. The same applies to the `RO-M1-11` cross-service question.
- TD-165's Planned Resolution ("no later than … M7") may be too late. M2's §19 checklist should address the import mechanism explicitly (IRA-M1 §10 already leaves it as `[DESIGN]`).

**Did M1 create an architectural dependency that should have been resolved in M1?** No.
- The dependency direction (BAE → AuthorizationEngine public contract types) is mandated by IRA-M1 C6/§10 ("builds an `AuthorizationRequest`, calls the existing `AuthorizationAdapter.evaluate()`, consumes the `EvaluationResult` unchanged").
- The import mechanism was explicitly left `[DESIGN]`.
- The dependency is on the public contract only (boundary test `test_only_the_existing_authorization_contract_is_imported`, confirmed by reading).
- **One latent packaging risk worth recording when TD-165 is resolved:** the top-level package names `authorization` and `adapters` are generic and could collide with host packages. None collides today; the reviewer searched `Backend/` for directories with those names.
- **Conclusion: packaging/operational debt only.** It is correctly recorded and non-blocking for M1. It should be re-examined at M2 start rather than left until M7.

## 7. M1 Scope-Leakage Assessment (Critical Governance Question #3)

| Item checked | Present? | Evidence |
|---|---|---|
| Manifest implementation / schema / registry | **No** | `ManifestResolution` has only `status`/`reason`; the only resolver shipped returns `NOT_IMPLEMENTED` |
| Durable execution state / table / migration | **No** | No persistence import; no Alembic file under the BAE; engine never assigns `ExecutionState` |
| State machine | **No** | Vocabulary plus a frozenset only; not consulted by the engine |
| Actual (concrete) BAR adapter | **No** | Protocol only; no AuthService or BAR import |
| Workstream E gate | **No** | `is_registered` port only; WP-23 Charter mtime 2026-09-22 |
| Real Business Activity registration / identifier assignment | **No** | No BAR access possible; BAR migrations contain no insert/seed; BAR-INDEX §7 still records C-024 BA-01 unregistered |
| Post-commit processing | **No** | Stages 11–16 are `NOT_REACHED` only |
| Audit persistence | **No** | Log line only |
| Event infrastructure | **No** | None |
| Notification integration | **No** | None |
| AI runtime | **No** | None |
| Capability business logic | **No** | No handler interface; Business Rule Execution unreachable |
| Host-service migration / wiring | **No** | Zero references from `Backend/Services` or `Backend/Shared`; no AuthService file modified on 2026-09-24 |
| **M3/M4 work brought forward** | **Yes, bounded** | Partial context construction (M3) and `AuthorizationRequest` construction plus `Authorizer` invocation (M4) — authorized by RO items 5–6 but excluded by Charter §10; see §5 (F-01) |

**Conclusion:**
- No M2/M5/M6 leakage was found.
- The only forward movement is the bounded M3/M4 elements discussed in §5. It is within the RO authorization's text and outside the Charter's.

## 8. Test-Quality Assessment

### 8.1 Reported results — independently reproduced

| Suite | Reported | Reproduced by this review |
|---|---|---|
| BAE (`Backend/Runtime/BusinessActivityEngine`) | 71 passed | **71 passed** (37 test functions; 71 collected cases) |
| AuthorizationEngine | 106 passed | **106 passed** |
| AuthService BAR A–C + WP-13 (`test_bar_identifier_service.py`, `test_bar_registration_service.py`, `test_authorization_integration.py`) | 33 passed | **33 passed** |
| AuthService full suite (throwaway JWT env, TD-010) | 972 passed | **972 passed** (71 warnings; 8 min 39 s) |

### 8.2 Meaningfulness

**Strong, behaviour-bearing tests**, several confirmed by mutation (§8.4):
- stage order;
- result invariants;
- fail-closed on every non-ALLOW decision;
- authorizer exception;
- registration gate;
- manifest boundary;
- claims-built authorization request;
- blank-claim validation;
- the real-engine DENY test.

**Tests that test mocks, or carry low evidential weight:**
- `test_no_m1_path_executes_business_rules_or_succeeds` makes up **20 of the 71** cases. Its assertions ("not succeeded", "Business Rule Execution not reached", all stages listed) are guaranteed by construction in M1: no code path to stage 9 exists, and the result invariant forbids success. It would still pass if stages 1–4 were badly broken, as long as the result invariants held. The headline count of 71 overstates distinct evidence.
- `test_executions_do_not_share_state` compares two DENY runs' reports. It would pass with shared state in several shapes. Isolation is actually protected by the per-call `_Run` design, which was read directly.
- `test_bar_is_only_ever_asked_whether_an_identifier_is_registered` uses `__getattr__`, which fires only for *missing* attributes. It proves the engine calls no other BAR method. It cannot prove "read-only" in the persistence sense, which is trivially true in M1 because no concrete adapter exists.
- The package-boundary tests are name and AST deny-lists. They are useful regression guards, but not proofs.

**Missing negative paths** (from-scratch probes and mutations):
- **Claims vs payload (tenant/identity source).** No test supplies a payload carrying `organization_id`/`identity_id`. Mutations M4 (organization taken from payload for authorization) and M10 (identity taken from payload in the context) both **survived** with all 71 tests passing. C5 and `CLAUDE.md §21.4` make "identity/organization from claims, never from the payload" a binding contract clause, and nothing guards it (F-03).
- **Manifest resolver raising.** Mutation M9, which removed the try/except around `resolve()`, **survived**. The `EXECUTION_FAILED` path at stage 2 for the resolver is untested (F-03).
- **Non-`bool` registration result.** Untested, and actually fail-open (F-02).
- **Malformed collaborator return values** (`None`, a plain-string decision). Untested; they raise out of `execute()` (F-06).
- **`membership_id=None` / `session_id=None`.** Not exercised through the engine (minor).
- **Log record.** Mutation M11 survived (F-07).

**False positives:** none found. Every test that was mutated against failed for the right reason.

**Tests encoding an unapproved architectural decision:**
- `test_context_names_the_ten_canonical_sections_and_partitions_them` fixes the four-available/six-unavailable partition as a contract.
- `test_allow_reaches_the_first_unimplemented_stage_and_does_not_succeed` fixes "Authorization Evaluation = COMPLETED on ALLOW" while the request is not yet activity-scoped (O-01).
- Both encode the stage-3/stage-4 "COMPLETED for partial realisation" semantics (F-04). That was an implementer `[DESIGN]` choice, not an RO or IRA decision.
- The transition-set and stage-order tests encode approved decisions (`§6.18.6`/`RO-M1-08`; `RO-M1-02`) and are appropriate.

### 8.3 From-scratch runtime probes (scratchpad only; not adapted from the suite)

| Probe | Input | Observed | Assessment |
|---|---|---|---|
| P1 | `is_registered` returns `"false"` (truthy string) | Proceeds past the gate to authorization; ends `NOT_IMPLEMENTED` at stage 5 | **Fail-open** (F-02) |
| P2 | `is_registered` returns `MagicMock()` | Same as P1 | **Fail-open** (F-02) |
| P9 | Registration source is a default `AsyncMock()` | Same as P1 | **Fail-open** (F-02) |
| P3 | `is_registered` returns `None` | `ACTIVITY_NOT_REGISTERED` | Correct |
| P4 | Resolver returns `None` | `AttributeError` raised out of `execute()` | Fail-closed, but breaks "never raised" (F-06) |
| P5 | Authorizer returns `None` | `AttributeError` raised out of `execute()` | Fail-closed, but breaks "never raised" (F-06) |
| P6 | Decision is the plain string `"ALLOW"` | Treated as non-ALLOW, then `AttributeError` building the reason | Fail-closed, but raises (F-06) |
| P7 | Authorizer returns `MagicMock()` | `AUTHORIZATION_DENIED` | Correct |
| P8 | `identity_id=None` | `VALIDATION_FAILED` | Correct |
| P10 | Authorizer raises `CancelledError` | Propagates | Correct |
| P11 | Resolver status is the plain string `"RESOLVED"` | `NOT_IMPLEMENTED` | Correct (strict) |
| P12 | Payload carries a spoofed `organization_id`/`identity_id` | Authorization request uses claim values | Correct (currently) |
| P13 | All-completed reports with `NOT_IMPLEMENTED` outcome | `ValueError` | Correct |
| P14 | Context frozen | `True` | Correct |
| P15 | Public engine surface | `['execute']` | Correct |

### 8.4 Mutation negative controls (disposable copy; deleted afterwards)

| Mutation | Suite result | Caught? |
|---|---|---|
| M1 registration gate removed | 1 failed / 70 passed | Yes |
| M2 default resolver returns `RESOLVED` | 2 failed | Yes |
| M3 authorizer exception converted to ALLOW | 1 failed | Yes |
| **M4 organization taken from payload for authorization** | **71 passed** | **No** |
| M5 CONDITIONAL treated as ALLOW | 1 failed | Yes (reproduces the IMP-REPORT's own control) |
| M6 authorization consulted before registration | 5 failed | Yes |
| M7 blank-identity check removed | 2 failed | Yes |
| M8 `membership_id` dropped from the authorization request | 1 failed | Yes |
| **M9 resolver exception no longer caught** | **71 passed** | **No** |
| **M10 identity taken from payload into the context** | **71 passed** | **No** |
| **M11 execution log record removed** | **71 passed** | **No** |

## 9. Findings by Severity

Severities follow `CLAUDE.md §19.8.7` wording where applicable.

### CRITICAL
None.

### HIGH
None.

### MEDIUM

**F-01 — Charter §10 M1 vs M1 implementation authorization (documentation inconsistency; RO disposition required).** See §5.
- Charter M1 excludes BAR query and Authorization invocation, requires structural tests only and no live invocation path, and places Authorization Context construction in M4.
- The RO's M1 authorization required a fail-closed authorization boundary, a read-only BAR interface, and behavioural DENY tests.
- The implementation followed the authorization and disclosed that choice. The operative authorization text is not recorded verbatim in the repository.
- Not an implementation defect.

**F-02 — The registration prerequisite gate fails open on a non-`bool` truthy return** (`engine.py:101`, `if not registered:`).
- Probes P1, P2, and P9: a string, a `MagicMock`, or a default `AsyncMock` registration source lets an unregistered identifier pass Activity Resolution and reach Authorization Evaluation.
- The authorization gate uses a strict identity comparison. The registration gate does not, which is inconsistent within the same engine.
- **Impact today:** none. No concrete `RegistrationSource` exists, no host wires the engine, and the authorization gate still follows.
- **Why it is not ordinary debt:** this is the runtime enforcement point for `RO-M1-04` ("unregistered cannot execute"). The concrete M2 adapter is exactly where a non-`bool` value (a row object, a status string) is likely to be returned.
- Under `§19.8.5` a gate that fails open must not be carried as ordinary Technical Debt once a concrete source is wired.

**F-03 — Contract-critical negative paths are untested.**
- (a) "Identity/Organization from claims, never from the payload" (C5; `CLAUDE.md §21.4`): mutations M4 and M10 survived.
- (b) Manifest resolver raising: mutation M9 survived.
- The behaviour is correct today (probe P12; code reading). Nothing prevents a regression.

**F-04 — "COMPLETED" is reported for partially realised stages; context sections are binary.**
- Stage 3 reports `COMPLETED` while six of ten `§6.17.5` sections are absent.
- Four sections are labelled "available" while holding only a fraction of their `§6.17.6`–`§6.17.15` content.
- Stage 4 reports `COMPLETED` on ALLOW, although the request carries no activity or operation scope (O-01).
- Nothing is fabricated, and the absent sections are named. However, `StageStatus` has no way to express "partially realised".
- IRA-M1 C14 ("An unbuilt stage reports `NOT_IMPLEMENTED`") and `§6.16.6` ("construct a complete execution context before business processing begins") make this a semantic choice that needs a recorded disposition before any path can pass stage 4 (M3).
- It is encoded in tests (§8.2).
- It does not create a false success in M1, because the result invariant forbids that.

**F-05 — M1 model-shape deliverables are thinner than the M1 skeleton contract, and this is undisclosed.**
- IRA-M1 §15 and Charter §10 M1 call for a ten-section context model and a transaction-context shape (`§6.17.13` / "BusinessActivityTransaction model shape").
- Delivered:
  - a flat seven-field `BusinessActivityContext`;
  - a section-name enum;
  - no transaction-context type (only the `TransactionBoundary` commit/rollback Protocol, which satisfies RO item 8's "ownership contract");
  - an `ExecutionState` enum that does satisfy the "state" shape.
- The IMP-REPORT does not mention the missing transaction-context shape or the absence of a sectioned model.
- This does not block M2, whose scope is resolution. It needs disclosure, or remediation, before M1 is accepted.

### LOW

**F-06 — `execute()` can raise despite the "never raised" result contract.**
- Malformed collaborator return values (`None` manifest, `None` evaluation, string decision) produce `AttributeError` outside the try blocks (probes P4–P6).
- Always fail-closed.

**F-07 — Low-evidential-weight tests and an untested log record.**
- The 20-case matrix is tautological in M1.
- The shared-state test is weak.
- No test covers the one observability record (mutation M11).
- The 71-case headline overstates distinct evidence.

**F-08 — Raw exception text is copied into `result.reason`** (`"{step} raised {type}: {exc}"`).
- Once an invoker maps `reason` to an HTTP body (M6), this can disclose internal details.
- Belongs to the M6 error contract (D-06).

### OBSERVATION

**O-01 — Authorization is not yet activity-scoped.**
- `AuthorizationRequest` carries identity, organization, membership, and session, but no Business Activity or requested operation.
- The engine takes one `Authorizer` at construction, while the governed request is bound through resolver construction (WP-13 pattern).
- ALLOW at stage 4 therefore means only what the injected authorizer means.
- This is disclosed and deferred (IRA-M1 C6/§10; IMP-REPORT deferral table: per-BA policy source M2, resolver binding M4).
- It must be resolved before stage 4 is relied upon for a real Business Activity. `§6.16.7` lists "Business Activity" and "Requested Operation" as authorization inputs.

**O-02 — The `EvaluationResult` is attached to the result only.**
- IRA-M1 §10 says it is also "attached unchanged to the Authorization Context section".
- The context is immutable and built before authorization, so this is an M3/M4 design point.

**O-03 — A correlation ID is generated when the host supplies none.**
- C5 says correlation is "reused from the hosting service's real correlation mechanism".
- Generation is a reasonable fallback (`§6.17.15`, "automatically populated"), but it is an unrecorded `[DESIGN]` choice.

**O-04 — TD-165 becomes live at M2 if the concrete BAR adapter is host-side** (§6).

**O-05 — Governance-document status staleness.** Once M1 is accepted, the following are stale:
- the Charter header, §10, and §17 ("No milestone has begun");
- IRA-M1's status ("BAE implementation has not begun");
- ADR-042's "Affected Code: … not created" (accurate at authoring time);
- the BAE README ("not been independently reviewed").

These are already partly tracked as IRA-M1 §16 Condition 2. They are a Release Readiness Audit concern (`§19.7b` Gate 5).

**O-06 — Request Reception performs structural claim validation (`VALIDATION_FAILED`).**
- `§6.16.4` gives Request Reception only "Accept invocation".
- Validation is otherwise a stage-5 concern.
- This is a reasonable `[DESIGN]` choice. It is recorded so that M3 keeps "invocation malformed" distinct from "input contract violated".

**O-07 — Other rows in the `TECH-DEBT.md` diff.** The working-tree diff also contains uncommitted `TD-161`–`TD-164`, which come from earlier Work Packages. Git cannot attribute rows within one untracked-change file. The report's claim that M1 added only `TD-165` is consistent with the row contents (`TD-165` alone cites WP-BAE-001).

## 10. Overall Disposition

**PASS WITH CONDITIONS.**

**What passes.** The M1 skeleton conforms to the authorized architecture on every point in scope:
- `ADR-042` placement and ordering (`RO-M1-01`/`RO-M1-02`);
- Manifest Resolution left as an explicit deferred boundary (`RO-M1-03`);
- a read-only, port-only BAR boundary with no registration logic (`RO-M1-04`);
- the existing AuthorizationEngine contract, unmodified, with ALLOW-only progression and fail-closed exception handling;
- no transaction ownership claimed;
- no lifecycle transition introduced (`RO-M1-08`);
- no fictitious platform service (`RO-M1-10`);
- no M2/M5/M6 leakage;
- no success reachable from any unimplemented stage.

**What the conditions cover.**
- One governance inconsistency that only the RO can dispose of (F-01).
- One fail-open robustness defect in the registration gate (F-02).
- Missing contract-critical tests (F-03).
- Two semantic and deliverable gaps that need remediation or recorded disposition (F-04, F-05).

**Conditions to be satisfied before M1 is accepted and committed** (`CLAUDE.md §19.7`: "review observations addressed; accepted through independent review; committed"):

1. **(RO)** Dispose of F-01 per §5.4 (a)–(c). This includes recording the verbatim M1 implementation authorization in the repository and directing any Charter §10 correction.
2. **Remediate F-02.** Make the registration gate fail closed on anything other than a real `True` (the same strictness the authorization gate already applies), and add a probe-style test. Under `§19.7b` gate 4 practice, a reviewer independent of the remediation should confirm the fix, including a negative control against the current code.
3. **Close F-03.** Add tests that fail if identity or organization is ever sourced from the payload (context and authorization request), and a test for resolver-raised `EXECUTION_FAILED`. Confirm each new test fails against the corresponding mutation (M4, M9, M10).
4. **Dispose of F-04 and F-05.** Either remediate, or record the decisions:
   - F-04: whether partially realised stages may report `COMPLETED`, or need a distinct status or explicit section-level `NOT_AVAILABLE` markers;
   - F-05: the missing transaction-context shape and sectioned context model.
   Record them in the IMP-REPORT and, where deferred, as `TECH-DEBT.md` entries under `§19.8.2`. These may be deferred to M3 as debt, since they are not `§19.8.5`-class.
5. **Update the IMP-REPORT** to reflect this review and the remediation. Then commit the accepted M1 with logical commits (no `git add -A`). F-06 may be remediated together with F-02, since it is the same code region.

## 11. M2 Gate Determination

**"Is WP-BAE-001 M2 authorized by the evidence currently available?" — No.**

**Exact blockers:**
1. **No M2 implementation authorization exists.**
   - The Charter §17 and §10 preamble require a separate RO authorization for each milestone.
   - `ADR-042` §0/§6 authorizes no implementation.
   - The M1 skeleton authorization is limited to M1, and its stop conditions forbid work beyond M1.
2. **The M1 Completion Gate (`§19.7`, applied per milestone by Charter §13) is not satisfied.**
   - M1 is still awaiting acceptance, has open conditions (§10), and is not committed.
   - `§19.7` prohibits beginning the next unit while the current one "requires remediation", "has not been accepted", or "has not been committed".
3. **M2's own `CLAUDE.md §19` Implementation Start Checklist does not exist.** IRA-M1 §15 and §16 Condition 4 require it to address, before any M2 code:
   - (1) the minimum manifest contract, and whether a new governed artifact is needed (`RO-M1-03`, D-09);
   - (2) the per-datum source analysis (`RO-M1-05`);
   - (3) the BAE ↔ Workstream E interface, including how M2 proceeds while Workstream E is unbuilt (`RO-M1-04`);
   - (4) the per-BA authorization-policy source;
   - (5) tenant-isolation placement (`X-15`).
   Item (1) may itself produce a `§19.4` STOP for a new governed artifact.

**Once all three are cleared,** M2 is subject only to normal implementation-start governance. It should additionally carry O-04 (TD-165 import mechanism for a host-side adapter) and O-01 into its checklist.

**Nothing in M1 itself structurally blocks M2.** The ports M2 needs (`RegistrationSource`, `ManifestResolver`) exist, and their shapes do not pre-decide the manifest contract.

## 12. Required Conditions and RO Decisions

**RO decisions genuinely required before M2:**
- **RO-D1 (F-01).**
  - Confirm, or not, that the 2026-09-24 M1 skeleton authorization governs M1's scope over Charter §10 M1's exclusions and verification method, and over IRA-M1 §15's "structural tests only / each reporting NOT_IMPLEMENTED".
  - Accept, or not, the bounded M3/M4 elements brought forward into M1.
  - Direct whether the authorization text is recorded verbatim in the repository and whether Charter §10 M1/M3/M4 is corrected.
- **RO-D2.** Authorize M2 implementation, once M1 is accepted and committed and M2's `§19` checklist exists. This is the normal milestone authorization and is listed because the brief asks for every decision that gates M2.

**RO decision recommended (not strictly gating M2):**
- **RO-D3 (F-04).** Whether a partially realised stage may report `COMPLETED`. If the RO prefers, the implementer may resolve this as a recorded `[DESIGN]` choice at M3. It must be settled before any path passes stage 4.

**Implementer conditions (no RO decision needed):** §10 conditions 2–5.

**Safely deferrable to M2/M5/M6** (not `§19.8.5`-class):
- F-05, if recorded as debt;
- F-06, if not fixed with F-02;
- F-07 (M6 for observability tests);
- F-08 (M6 error contract);
- O-01 (M2/M4);
- O-02 (M3/M4);
- O-03 (M3/M6);
- O-04 / TD-165 (reassess at M2 start);
- O-05 (Release Readiness);
- O-06 (M3);
- `R-01` (M5);
- U-01–U-10 (M5/M6).

**Not deferrable as ordinary debt beyond the point a concrete `RegistrationSource` is wired:** F-02.

## 13. Integrity Verification

| Check | Result | Evidence |
|---|---|---|
| No Business Activity registered | Confirmed | BAE cannot reach BAR (no AuthService, BAR, or DB import; no concrete adapter). Neither BAR migration contains insert/seed statements. BAE tests use literals only |
| No BA identifier assigned | Confirmed | No issuance symbol or BAR service referenced; the identifier type only validates |
| BAR A–C unchanged | Confirmed by timestamp (files untracked, so git cannot diff them) | All ten BAR model, repository, service, migration, and test files last modified 2026-09-22 15:24–16:19, before M1 (2026-09-24 13:08). BAR regression 33/33 passed |
| BAR-INDEX unchanged | Confirmed by timestamp (untracked) | mtime 2026-09-22 13:30; `§7` still records C-024 BA-01 unregistered |
| WP-23 Charter unchanged | Confirmed by timestamp (untracked) | mtime 2026-09-22 13:24 |
| C-024 BA-01 unregistered | Confirmed | BAR-INDEX `§7`; no seeding |
| AuthorizationEngine unchanged | **Code unchanged.** `README.md` carries the pre-M1 `RO-M1-12` factual correction (mtime 11:55, IRA-M1 §17 rows 5–6), not an M1 change | `git diff --stat Backend/Runtime/AuthorizationEngine` shows `README.md` only; no untracked files there; 106/106 passed |
| ADR-042 unchanged by M1 | Confirmed by timestamp (untracked) | mtime 12:37, before the first BAE file (13:08) |
| IMP-001 unchanged | Confirmed | git-clean (tracked, no diff); mtime 2026-08-07 |
| RTA-001 unchanged | Confirmed | git-clean (tracked, no diff); mtime 2026-08-09 |
| No unrelated implementation changes by M1 | Confirmed | Only the BAE package, `TECH-DEBT.md` (TD-165), and the IMP-REPORT changed after 12:37 on 2026-09-24. No AuthService or other service file changed that day |
| Git HEAD | `8323bf3976818ff463cf67e891bd2a0a953777fd` ("docs(WP-20): close C-021 offering definition") | `git rev-parse HEAD` |
| Staging state | Nothing staged | `git diff --cached --name-only` is empty |
| Commit / push state | M1 not committed. The branch `main` is **ahead of `origin/main` by 1** (`8323bf3`, a pre-existing unpushed WP-20 commit unrelated to M1). No stash entries. The working tree carries many uncommitted changes from earlier Work Packages (151 status entries) | `git status -sb`; `git log origin/main..HEAD` |
| This review's own footprint | This file is the only file created. No other file modified. No scratchpad artifacts left inside the repository | Probes and mutation copy under the session scratchpad; the mutation copy was deleted |

---

*End of IRA-BAE-001-M1 Independent Review.*
- Disposition: PASS WITH CONDITIONS.
- M2: not authorized by current evidence (§11).
- RO decisions required: RO-D1 (F-01), RO-D2 (M2 authorization); RO-D3 recommended.
- No file other than this one was created or modified. Nothing was staged, committed, or pushed.
