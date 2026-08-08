# CERT-WP-RTA-001 — Independent Certification

## Authorization Runtime Engine

**Certification Type:** Independent Work Package Certification (`CLAUDE.md §19.7`, "Independent Certification")
**Work Package:** WP-RTA-001 — Authorization Runtime Engine (Runtime; no PE-001 capability)
**Certifying party:** Fresh-context independent reviewer, no prior involvement in WP-RTA-001's implementation, per `CLAUDE.md §19.7`'s explicit prohibition on self-certification and `ADR-014`'s fresh-context reviewer requirement. Every material claim below was re-derived directly from source code, test execution, and primary governance documents — the implementer's own `IMP-REPORT-WP-RTA-001`, `WP-RTA-001_Closure_Report.md`, and `WP-RTA-001_Self_Verification_Audit.md` were read only as navigational aids and re-verified, never trusted.
**Date:** 2026-07-30
**Provenance note:** This document is reproduced verbatim from the independent reviewer's own output (a fresh-context subagent dispatched with no memory of WP-RTA-001's implementing conversation). No finding below has been edited by the implementing session. A Post-Certification Resolution addendum, clearly separated, was appended after this document's original text to record the resolution of Blocking Conditions — that addendum was not written or reviewed by the independent reviewer.

---

## 1. Executive Summary

`WP-RTA-001` delivers a Runtime Component (`RTA-001 §3.8`/`§11`) at `Backend/Runtime/AuthorizationEngine/` implementing `URA-001-76`'s five-tier Authorization Resolution Precedence (Named User > Group > Approval Authority > Business Role > Domain Permission) across six milestones (M1–M6). Independent re-verification confirms:

- **106/106 tests pass**, independently re-run in this pass (`cd Backend/Runtime/AuthorizationEngine && python -m pytest tests/ -v` → `106 passed in 0.70s`).
- The runtime package is architecturally clean: `AuthorizationEngine` (`engine.py`) contains no persistence/ORM/repository/FastAPI code (confirmed by full source read and independent grep of every import statement); dependency direction is one-way (`adapters/` → `authorization/`, never reversed — confirmed by an independent grep of every `import`/`from` line in every `authorization/*.py` file, which found exactly zero executable references to `adapters`, only two docstring mentions); the pipeline (`pipeline.py`) performs orchestration only, never inspecting or branching on the returned `AuthorizationDecision`; the adapter (`authorization_adapter.py`) performs translation only (zero references to `AuthorizationDecision` anywhere in the file); observers (`PipelineObserver`) cannot influence the returned decision (all three methods return `None`, discarded by `_notify_safely`). No circular dependency exists anywhere in the package (dependency graph independently reconstructed, §5 below).
- `TD-071` through `TD-078` were independently re-checked against `TECH-DEBT.md`'s live text and against the source files they describe — all eight are accurate, correctly scoped, and correctly non-blocking.
- Two Low-severity findings previously raised by the implementer's own (non-certifying) Self-Verification Audit were independently re-derived and **confirmed real**: stale "M4 Observability, M6 Caching" docstring references in `pipeline.py` (lines 8–9, 71, 83–84), and the absence of a formal ADR (`ADR-016` or later) recording the `IRA-RTA-001 §5` repository-owner decision, unlike every comparable precedent (`ADR-006`–`ADR-015`).

**One material, previously-undisclosed-as-current finding is the central item of this certification (§9, Non-Conformity 1):** the repository's working tree currently contains a **second, unauthorized, still-wired-in implementation of the same Authorization Engine capability**, sitting inside `Backend/Services/AuthService/{routers,schemas,services,tests}/authorization_engine*.py`, with real router registration in `main.py` (`app.include_router(authorization_engine.router, prefix="/authorization", ...)`) and a tenant-middleware exemption in `middleware/tenant.py`. This code predates `WP-RTA-001` — it is the exact "candidate implementation" that `architecture/06-Reviews/AUTHORIZATION_ENGINE_CONSTITUTIONAL_RESPONSE.md` already found **not constitutionally authorized** (Findings F-01/F-02, both classified Constitutional Violation, citing fabricated `WP-RTA-001`/`IRA-RTA-001` identities that, at the time that review was written, corresponded to no real chartered artifact). `WP-RTA-001` was subsequently chartered for real, and this certification confirms its own deliverable is sound. **But the original unauthorized candidate code was never removed, never reconciled with the newly-authorized `Backend/Runtime/AuthorizationEngine` package, and — critically — its continued presence in the working tree is disclosed by none of the five WP-RTA-001-series governance documents** (`IRA-RTA-001`, `WP-RTA-001`, `IMP-REPORT-WP-RTA-001`, the Closure Report, or the Self-Verification Audit), nor by `WPR-001`'s own WP-RTA-001 or WP-05 rows — despite all of them stating claims ("no file under `Backend/Services/*` was touched," "no Business Capability consumes this engine's decisions in production use") that a reader would reasonably, but incorrectly, take to mean the working tree's `Backend/Services/AuthService` is unaffected and no competing authorization mechanism exists. It duplicates `URA-001-76`'s precedence logic in a second, independent implementation (`CLAUDE.md §12`/§15 Golden Rule 4: "One business rule. One implementation"; "Avoid parallel implementations") and self-labels itself `"WP-RTA-001 Business Activity: BA-02 Implement Authorization Engine"` — a Business Activity identity `IRA-RTA-001 §9` explicitly states this Work Package does **not** have ("Performs no Business Activity of any capability").

This finding does not implicate the quality of `WP-RTA-001`'s own milestone deliverables, which are independently confirmed sound. It does mean the repository, as a whole, is **not** in a clean state for this Work Package to be declared closed without a corrective action.

## 2. Certification Decision

**CERTIFIED WITH CONDITIONS**

- The `Backend/Runtime/AuthorizationEngine` package itself (M1–M6, all six milestones) is certified on its own merits and may be frozen as-is; no further change to that package is required by this certification.
- The Work Package as a governance unit, and the repository's readiness to proceed to `WP-05`, are **conditioned** on resolving Blocking Condition 1 (§11) — the undisclosed, unresolved, still-wired parallel implementation in `Backend/Services/AuthService`.

---

## 3. Scope

**Governance documents reviewed (full, this pass):**
- `CLAUDE.md` (full, including §14, §16–§19, §19.7, §19.8)
- `CERT-WP-04_Enterprise_Structure_Management.md` (format/rigor reference only)
- `architecture/02-Constitutional/RTA-001 - Runtime Architecture and Execution.md` (§§1–3 skimmed for context; §11 "Authorization Runtime" read in full)
- `architecture/02-Constitutional/URA-001 - User, Role, Permission, Event and ssignment.md` (`URA-001-76` and surrounding context read directly, not assumed)
- `architecture/05-Implementation/IRA-RTA-001_Authorization_Runtime_Engine_Implementation_Readiness_Assessment.md` (full)
- `architecture/05-Implementation/WP-RTA-001_Authorization_Runtime_Engine.md` (full)
- `architecture/05-Implementation/IMP-REPORT-WP-RTA-001_Authorization_Runtime_Engine.md` (full, all six milestone sections)
- `architecture/06-Reviews/WP-RTA-001_Closure_Report.md` (full)
- `architecture/06-Reviews/WP-RTA-001_Self_Verification_Audit.md` (full — treated as a navigational aid only, every claim re-derived independently)
- `architecture/06-Reviews/AUTHORIZATION_ENGINE_CONSTITUTIONAL_RESPONSE.md` (full — discovered during this pass via independent search, not listed in the task's own document list; directly material to §9 Non-Conformity 1)
- `architecture/00-Governance/WPR-001_Work_Package_Roadmap.md` (WP-RTA-001 and WP-05 rows)
- `architecture/06-Reviews/TECH-DEBT.md` (`TD-071` through `TD-078`, full entries)
- `architecture/07-Decisions/ADR-015_Access_Evaluation_Outcome_Canonical_Business_Object_Registration.md` (full)
- `architecture/05-Implementation/IRA-005_WP-05_Access_Management_Implementation_Readiness_Assessment.md` (§9, §10.1–§10.5 read in full)

**Source code read in full (independent verification):**
- `Backend/Runtime/AuthorizationEngine/authorization/{models,resolvers,engine,tier_resolvers,registry,orchestrator,pipeline,scope_validator,observability,__init__}.py`
- `Backend/Runtime/AuthorizationEngine/adapters/{authorization_adapter,__init__}.py`
- `Backend/Runtime/AuthorizationEngine/README.md`, `pytest.ini`
- All 12 test files under `Backend/Runtime/AuthorizationEngine/tests/` (106 tests)
- `Backend/Services/AuthService/routers/authorization_engine.py`, `schemas/authorization_engine.py`, `services/authorization_engine_service.py`, `tests/test_authorization_engine_{api,service}.py`, and the `main.py`/`middleware/tenant.py` diffs (discovered via `git status`/`git diff`, read in full — not part of the task's original document list but material to certification)

**Test execution:** `cd Backend/Runtime/AuthorizationEngine && "../../Services/AuthService/venv/Scripts/python.exe" -m pytest tests/ -v` — run directly by this reviewer, not trusted from any report.

---

## 4. Repository Evidence

- **Fresh test run:** 106 passed, 0 failed, 0 skipped, 0 errors, in 0.70s.
- **`git status --short`** (independently run): confirms every `WP-RTA-001`-related path is untracked (`??`) or modified-uncommitted (`M`) — `Backend/Runtime/` is entirely untracked; `Backend/Services/AuthService/main.py`, `middleware/tenant.py` are modified-uncommitted; `WPR-001` and `TECH-DEBT.md` are modified-uncommitted; five new governance documents are untracked. **Also confirmed:** `Backend/Services/AuthService/routers/authorization_engine.py`, `schemas/authorization_engine.py`, `services/authorization_engine_service.py`, `tests/test_authorization_engine_api.py`, `tests/test_authorization_engine_service.py` are all untracked (`??`) — this is the candidate code discussed at §1 and §9.
- **`git log --oneline --all -- Backend/Runtime/`** and **`git log --oneline --all -- Backend/Services/AuthService/{routers,services,schemas}/authorization_engine*.py`**: both return zero commits. Neither the authorized runtime package nor the unauthorized candidate code has ever been committed. This confirms the implementer's own "not committed" claim, but does not change the fact that both exist, side by side, in the current working tree.
- **File inventory** (fresh `find`, not from any report): 10 production files under `authorization/`/`adapters/` + 12 test files = matches every prior claim exactly.
- **`grep -c "^| TD-07[1-8] "` on `TECH-DEBT.md`:** 8 — all eight entries exist as claimed.
- **`find architecture/07-Decisions -iname "ADR-01[6-9]*"`:** empty — confirmed no ADR beyond `ADR-015` exists.
- **Candidate-code discovery:** the parallel `Backend/Services/AuthService` authorization engine implementation was found via the initial `git status` (provided in this session's environment context, not something WP-RTA-001's own documents pointed to) and independently traced to `architecture/06-Reviews/AUTHORIZATION_ENGINE_CONSTITUTIONAL_RESPONSE.md` via a repository-wide grep for its own file paths — that document is the only governance artifact in the repository that acknowledges this code's existence, and it does so only as a historical review subject, never confirming or denying whether the code is still present at Work Package closure time.

---

## 5. Implementation Verification (M1–M6)

| Milestone | Status | Evidence |
|---|---|---|
| **M1 — Authorization Evaluation Core** | **Implemented** | `authorization/models.py` — `AuthorizationContext`, `EvaluationResult`, `TierEvaluation`, `AuthorizationTier`/`AuthorizationDecision`/`TierResult` enums, all `@dataclass(frozen=True)` (read directly, confirmed). `authorization/engine.py` — `AuthorizationEngine.evaluate()` (lines 62–119): iterates `PRECEDENCE_ORDER`, short-circuits on first `MATCH`, never fabricates `ALLOW` for an unbound tier (reports `NOT_EVALUATED`), defaults `DENY` with full trace if no tier resolves. `PRECEDENCE_ORDER` (lines 39–45) matches `URA-001-76`'s own text exactly (Named User > Group > Approval Authority > Business Role > Domain Permission), verified directly against `URA-001-76`'s primary-source text in this pass, not assumed. Tests: `tests/test_authorization_engine.py` (9 tests), all pass. |
| **M2 — Runtime Resolver Framework & Tier Resolution** | **Implemented** | `authorization/tier_resolvers.py` — five ABCs (`NamedUserResolver`, `GroupResolver`, `ApprovalAuthorityResolver`, `BusinessRoleResolver`, `DomainPermissionResolver`), each with exactly one abstract `resolve()` method and a fixed `TIER` class variable. `authorization/registry.py` — `ResolverRegistry` (fail-fast, `DuplicateResolverError` on re-registration, fluent `.register()`). Tests: `tests/test_resolver_framework.py` (14 tests), all pass. |
| **M3 — Runtime Evaluation Pipeline & Resolver Orchestration** | **Implemented** | `authorization/orchestrator.py` — `ResolverOrchestrator` (discovery: `configured_tiers`/`missing_tiers`, both computed against the same `PRECEDENCE_ORDER` imported — not redefined — from `engine.py`). `authorization/pipeline.py` — `EvaluationPipeline` (assembly + `PipelineObserver` extension seam). Tests: `tests/test_pipeline.py` (13 tests), all pass. |
| **M4 — Runtime Integration Adapters** | **Implemented** | `adapters/authorization_adapter.py` — `AuthorizationAdapter`/`AuthorizationRequest`, translation-only (`build_context()` is a direct field mapping plus two blank-string checks). Dependency direction independently re-verified (§6). Tests: `tests/test_adapter.py` (9 tests), all pass. |
| **M5 — Runtime Completeness** | **Implemented** | `authorization/scope_validator.py` — `EnterpriseScopeValidator` (structural-only presence/well-formedness checks, disclosed as such). `authorization/observability.py` — `RuntimeObservabilityCollector`, a concrete `PipelineObserver`. `pipeline.py`'s `execute()` extended with scope validation and `_notify_safely()` observer-failure isolation (lines 130–172, read directly). Tests: `tests/test_scope_validator.py` (6), `tests/test_observability.py` (5), `tests/test_pipeline_m5.py` (7) = 18 tests, all pass. |
| **M6 — Production Readiness, Hardening & Closure** | **Implemented** (scope redefined via two disclosed charter-synchronization passes; original M6 content — real tier resolution, first consumer integration, Caching — never delivered under any milestone, disclosed as Remaining External Dependencies, not silently dropped) | `tests/test_contract_stability.py` (18), `tests/test_performance.py` (5), `tests/test_concurrency.py` (6), `tests/test_extension_points.py` (6), `tests/test_package_integrity.py` (8) — 43 tests, all read in full and all pass. `README.md` exists, documents every public contract accurately (independently cross-checked against actual signatures). `WP-RTA-001_Closure_Report.md` exists. |

**Total: 106/106 passing, independently re-run.** All six milestones are Implemented against their own, twice-disclosed, twice-revised charter. No milestone claims something the source code does not support.

**Acceptance Criteria not fully met (honestly disclosed by the charter itself, not a contradiction):** `WP-RTA-001`'s own Acceptance Criteria requires *"At least one real Business Capability's Business Activity gates through this engine per `IMP-API-002`"*. This is **not met** by the authorized `Backend/Runtime/AuthorizationEngine` package — `AuthorizationAdapter` has no real caller anywhere in the repository. The charter's own Exit Criteria section explicitly permits this to remain unmet at closure, disclosed as a "Remaining External Dependency." This is internally consistent (the charter says what it does and doesn't require), but it does mean the deliverable, considered alone, is not yet usable — see §9 Non-Conformity 4.

---

## 6. Architecture Assessment

Independently re-verified, not merely re-stated from the Self-Verification Audit:

| Claim | Verified | Evidence |
|---|---|---|
| `AuthorizationEngine` contains no persistence/ORM/repository/FastAPI/Business Activity logic | **Confirmed** | Full read of `engine.py` (119 lines): a `dict` lookup, a `for` loop over `PRECEDENCE_ORDER`, dataclass construction. Only imports: `.models`, `.resolvers`. |
| Resolvers are isolated to their own tier | **Confirmed** | Each of the five `tier_resolvers.py` ABCs has exactly one abstract method scoped to its own `TIER`; no resolver-to-resolver call exists anywhere (grepped). |
| The pipeline performs orchestration only, not decision-making | **Confirmed** | `pipeline.py`'s `execute()` calls `scope_validator.validate()` then `engine.evaluate()`; never inspects or branches on the returned `AuthorizationDecision` (confirmed by reading the full method body). |
| The adapter performs translation only | **Confirmed** | `authorization_adapter.py` full read — `build_context()` is a field mapping plus two blank-string checks; `AuthorizationDecision` appears zero times in the file (grepped). |
| Observers cannot influence the returned decision | **Confirmed** | `PipelineObserver`'s three methods are all declared `-> None`; `_notify_safely()` (lines 159–172 of `pipeline.py`) discards every callback's return value and swallows exceptions via `except Exception: pass`. |
| Dependency direction is one-way: `adapters/` depends on `authorization/`, never the reverse | **Confirmed, independently** | My own `grep -n "^import\|^from" authorization/*.py adapters/*.py` (§ command run this pass) found exactly two matches of the string `adapters` inside `authorization/*.py` — both in `__init__.py`'s own docstring prose explaining the dependency-direction rule (line 19: "imports from `adapters`."), zero real `import`/`from` statements. `adapters/authorization_adapter.py` imports `from authorization import ...` and `from authorization.pipeline import EvaluationPipeline` — the only cross-package edge, running one way. |
| No circular dependency exists | **Confirmed** | Independently reconstructed dependency graph (below) — every edge points one direction; `models.py` and `resolvers.py` are true leaves with zero internal imports. |

**Dependency graph (independently reconstructed this pass, via direct source read, not copied from the Self-Verification Audit):**

```
adapters/authorization_adapter.py ──▶ authorization (package) , authorization.pipeline

authorization/models.py        (leaf — no internal imports)
authorization/resolvers.py     ──▶ models
authorization/tier_resolvers.py──▶ models, resolvers
authorization/registry.py      ──▶ models, resolvers, tier_resolvers
authorization/engine.py        ──▶ models, resolvers          (unmodified since M1 — confirmed: no import of registry/orchestrator/pipeline)
authorization/orchestrator.py  ──▶ engine (PRECEDENCE_ORDER only), models, registry, resolvers
authorization/scope_validator.py──▶ models
authorization/pipeline.py      ──▶ engine, models, orchestrator, registry, scope_validator
authorization/observability.py ──▶ models, pipeline
authorization/__init__.py      ──▶ every module above (re-export point only)
```

No file under `authorization/` imports from `adapters/`. No cycle exists. This matches `engine.py`'s own claim of being "unmodified since M1" structurally, not merely by assertion.

**No forbidden imports:** `test_package_integrity.py::test_no_file_imports_a_web_framework_or_orm` and this reviewer's own independent grep both confirm zero `fastapi`/`sqlalchemy`/`starlette`/`Backend.Services`/`Backend.Shared` imports anywhere in `authorization/`/`adapters/`.

---

## 7. Test Assessment

- **106/106 pass**, run twice during this certification (once standalone, once while cross-checking specific test bodies), identical results both times — no flakiness observed.
- Every one of the 12 test files was read in full (not sampled) by this reviewer. Assertions reference real, existing methods/properties; no test imports a nonexistent module; no test is trivially tautological.
- Coverage is not tool-measured (`pytest-cov` not installed) — confirmed absent again this pass. This is an honest, disclosed gap, not glossed over by the implementer's own documents either.
- Tests genuinely exercise the claimed guarantees, not merely happy paths: `test_evaluate_denies_when_no_resolvers_bound`, `test_higher_precedence_tier_wins_and_lower_tier_is_never_consulted`, `test_resolver_failure_propagates_and_is_never_silently_converted_to_a_decision`, `test_broken_on_error_does_not_mask_the_real_underlying_exception`, `test_concurrent_evaluations_with_different_outcomes_never_cross_contaminate` (200-way `asyncio.gather` with forced interleaving via `await asyncio.sleep(0)`), `test_authorization_engine_source_is_unaffected_by_any_extension_point_in_this_file` (a literal `inspect.getsource()` snapshot comparison, not just a prose claim).
- Extension-point validation (`test_extension_points.py`) is genuinely rigorous: it proves Metrics/Tracing/Audit/Persistence all attach via `PipelineObserver` alone, and — importantly — **honestly proves Caching does not**, via a structural check on the Protocol's own return-type annotations, not merely an assertion in a docstring.

No test defect was found beyond the one the implementer's own M5 pass already found and fixed (the M4 substring-based dependency check, replaced with AST-based detection — independently re-verified correct by this reviewer's own separate grep).

---

## 8. Documentation Assessment

Cross-checked `WP-RTA-001`, `IRA-RTA-001`, `IMP-REPORT-WP-RTA-001`, `WPR-001`, the Closure Report, the Self-Verification Audit, and `TECH-DEBT.md` against each other and against the repository.

**Internally consistent:** milestone statuses, test counts (106, stated identically everywhere), `TD-071`–`TD-078` (same descriptions everywhere), "not committed / not independently certified" (consistent across all documents, confirmed true by `git log`).

**Confirmed real, both previously-flagged findings:**
1. **Stale docstring references in `pipeline.py`.** Confirmed by direct read: line 8 ("...the extension seam future milestones (M4 Observability, M6 Caching, and..."), line 71 ("...M4's own tracing) has a stable correlation id..."), lines 83–84 ("...implements this to observe pipeline execution (e.g. M4 Observability, M6 Caching, or any future Audit/persistence...)"). These are stale from an M3-era draft, pre-dating two subsequent charter-renumbering passes (M4 became Integration Adapters; Observability shipped as M5; Caching was never delivered under any milestone). Cosmetic, no functional impact — confirmed nothing in `execute()`'s actual control flow depends on these comment lines.
2. **No ADR formalizes the `IRA-RTA-001 §5` repository-owner decision**, unlike every comparable precedent (`ADR-006` through `ADR-015`) — confirmed by direct directory listing (`architecture/07-Decisions/` contains no `ADR-016` or later).

**One inconsistency the implementer's own documents did not find, confirmed by this reviewer:** every WP-RTA-001-series governance document's claim of the form "no file under `Backend/Services/*` ... was touched" is **narrowly true but materially incomplete** — see §9 Non-Conformity 1. None of the five documents discloses that a competing, unauthorized implementation of the exact same capability is currently present, uncommitted, and wired into `Backend/Services/AuthService`'s own `main.py`/`middleware/tenant.py`.

---

## 9. Technical Debt Assessment

All eight entries independently re-checked against `TECH-DEBT.md`'s live text and against the source files/behavior they describe:

| ID | Accurately describes current state? | Severity/Priority correct? | Should be blocking? |
|---|---|---|---|
| `TD-071` (`Backend/Shared` `aurex` namespace breakage) | Yes — confirmed pre-existing, unrelated to this Work Package's own code quality | Medium, correct | No |
| `TD-072` (`AuthorizationContext` opaque field shapes) | Yes — confirmed, `tuple[str, ...]` fields verified in `models.py` | Low, correct | No |
| `TD-073` (`PipelineConfigurationError` guards only `None`) | Yes — confirmed by reading `orchestrator.py`/`pipeline.py` constructors | Low, correct | No |
| `TD-074` (`AuthorizationRequest` mirrors `AuthorizationContext`) | Yes — confirmed field-for-field identical, read directly | Low, correct | No |
| `TD-075` (observer-failure isolation has no visibility) | Yes — confirmed, `_notify_safely()` swallows silently | Medium, correct | No |
| `TD-076` (`EnterpriseScopeValidator` structural only) | Yes — confirmed, no persistence import in `scope_validator.py` | Low, correct | No |
| `TD-077` (scope validation runs pre-evaluation, not mid-pipeline per `§11.7`'s literal order) | Yes — confirmed against `§11.7`'s own text and `pipeline.py`'s actual call order | Low, correct — the substantive `§11.12` guarantee is preserved regardless of literal step position | No |
| `TD-078` (Caching requires a wrapper, not `PipelineObserver`) | Yes — confirmed and test-proven (`test_extension_points.py`) | Low, correct | No |

**No entry is Critical or High**, and correctly so — none defeats a stated guarantee (`CLAUDE.md §19.8.5`'s own governance list was checked against each: none is a deferred architectural, security, data-integrity, or tenant-isolation *defect*, nor a failing test).

**Additional Technical Debt found in this pass, not registered anywhere in `TECH-DEBT.md`:**
- The stale `pipeline.py` docstrings (§8, finding 1) — a genuine, findable Technical Debt item per `CLAUDE.md §19.8.2` ("Technical Debt shall not exist solely within... commit messages or chat history" — currently it exists only in the Self-Verification Audit and this certification, not in the register itself). **Recommend registering as `TD-079`.**
- The missing `ADR-016` (§8, finding 2) is better framed as a Governance Gap than ordinary Technical Debt (it already has a name in `AUTHORIZATION_ENGINE_CONSTITUTIONAL_RESPONSE.md` as Finding F-03), but if the repository owner prefers to track it in `TECH-DEBT.md` for visibility, that is a reasonable alternative to a standalone ADR action item.
- **The unresolved presence of the `Backend/Services/AuthService/authorization_engine*.py` candidate code (§9 below) is not tracked anywhere as Technical Debt, a Governance Backlog Item, or otherwise** — despite `AUTHORIZATION_ENGINE_CONSTITUTIONAL_RESPONSE.md` itself already having found it non-compliant seven months (in narrative time) before this certification. This is the most consequential untracked item found in this pass.

---

## 10. Non-Conformities

| # | Severity | Finding | Evidence | Impact | Recommendation |
|---|---|---|---|---|---|
| 1 | **High** | An unauthorized, pre-`WP-RTA-001` "candidate" Authorization Engine implementation remains present, uncommitted, and **actively wired into `Backend/Services/AuthService`'s own `main.py` (`app.include_router(authorization_engine.router, prefix="/authorization", ...)`) and `middleware/tenant.py`** (a tenant-isolation exemption). It duplicates `URA-001-76`'s precedence logic independently of the now-authorized `Backend/Runtime/AuthorizationEngine` package, self-labels as `"WP-RTA-001 Business Activity: BA-02"` (a Business Activity identity `IRA-RTA-001 §9` says this Work Package does not have), and its continued presence is disclosed by none of the five WP-RTA-001-series certification-facing documents or `WPR-001`. | `git status`/`git diff` (this pass); `Backend/Services/AuthService/routers/authorization_engine.py`, `services/authorization_engine_service.py`, `schemas/authorization_engine.py`; `architecture/06-Reviews/AUTHORIZATION_ENGINE_CONSTITUTIONAL_RESPONSE.md` Findings F-01/F-02 (already classified Constitutional Violation, "no constitutional standing," "do not commit under any identity") | If committed accidentally, or if a future implementer mistakes this for the authorized engine, the repository would ship two competing authorization mechanisms — one honestly `DENY`-by-default and adapter-based, one a self-contained duplicate that already resolves real Domain Permission grants against the live database and is exempted from tenant-isolation middleware. `CLAUDE.md §12`/§15 duplication rules are violated in substance, even though the duplicate is (correctly) uncommitted. | **Blocking.** Either (a) delete the candidate code and its wiring, since it has "no constitutional standing" per the repository's own prior finding, or (b) formally reconcile it — obtain the `ADR-016` decision, refactor it to consume `Backend/Runtime/AuthorizationEngine` via `AuthorizationAdapter` instead of reimplementing precedence logic, and register it as `WP-05`'s real `BA-01`. Do not leave it as-is, uncommitted and undocumented, going forward. |
| 2 | Low | No ADR formalizes the `IRA-RTA-001 §5` repository-owner decision, unlike `ADR-006`–`ADR-015`'s own precedent. | `architecture/07-Decisions/` directory listing (absence); already flagged by the Self-Verification Audit and `AUTHORIZATION_ENGINE_CONSTITUTIONAL_RESPONSE.md` F-03 | Weaker traceability than every prior governance decision of the same class; not fatal since `IRA-RTA-001 §5` does record the decision in prose. | Non-blocking. Author `ADR-016` at next convenient touch. |
| 3 | Low | Stale "M4 Observability, M6 Caching" docstring references in `pipeline.py` (lines 8–9, 71, 83–84), pre-dating two subsequent charter-renumbering passes. | Direct read of `pipeline.py`, confirmed this pass | Cosmetic only — confirmed no functional dependency on these comment lines. | Non-blocking. Update the four references; register as `TD-079` per `CLAUDE.md §19.8.2` so it does not persist only in review documents. |
| 4 | Medium | `WP-RTA-001`'s own Acceptance Criterion ("at least one real Business Capability's Business Activity gates through this engine") is unmet — `AuthorizationAdapter` has no real caller anywhere in the repository. | `WP-RTA-001_Authorization_Runtime_Engine.md` Acceptance/Exit Criteria; confirmed by repository-wide search — zero references to `AuthorizationAdapter` outside `Backend/Runtime/AuthorizationEngine/` itself | The deliverable, considered alone, is a well-tested foundation, not yet a usable authorization system — honestly and repeatedly disclosed by the implementer's own documents, so this is not a documentation-integrity problem. | Non-blocking for this certification's own narrow scope (the charter's own Exit Criteria explicitly permits deferring this). Blocking before any claim of "production ready" or before real consumption begins. |
| 5 | Low | No real production `TierResolver` exists for any of the five tiers, including Domain Permission — the one tier `IRA-RTA-001` itself identified as having real, existing data (`WP-02`'s `domain_permission_registry`). Notably, a working Domain Permission resolver (reusing `DomainPermissionRepository.get_active_grant()`) already exists in the unauthorized candidate code (Non-Conformity 1) but was never ported into the authorized package. | `Backend/Runtime/AuthorizationEngine/README.md` "Known Limitations"; Closure Report §5/§7; independently confirmed via source read — no concrete `TierResolver` subclass exists outside test files | Consistent with the charter's own disclosed scope; a missed reuse opportunity rather than a defect. | Non-blocking. When a future milestone or `WP-05` implements real Domain Permission resolution, evaluate porting the already-proven logic from the (to-be-resolved-per-Non-Conformity-1) candidate code rather than rewriting from scratch. |

---

## 11. Risk Assessment

1. **(Material) Non-Conformity 1 — undisclosed duplicate implementation.** The core risk is not that the candidate code produces a wrong decision today (it correctly fails closed — `DENY` by default, `ALLOW` only via the pre-existing `PLATFORM_ADMIN` override or a genuine Domain Permission grant, matching `AUTHORIZATION_ENGINE_CONSTITUTIONAL_RESPONSE.md`'s own Finding F-10). The risk is **governance and architectural drift**: two implementations of the same constitutionally-significant capability, one authorized and inert, one unauthorized and live-wired, coexisting silently. If `WP-05` begins under the assumption that "the Authorization Engine" means `Backend/Runtime/AuthorizationEngine` (the only one any current governance document names as authorized), while the candidate code remains present and functional, a future implementer has a 50/50 chance of extending the wrong one, or of the two silently diverging further.
2. Missing `ADR-016` (Non-Conformity 2) — Low risk, traceability gap only.
3. Stale docstrings (Non-Conformity 3) — negligible risk, cosmetic.
4. Unmet "real consumer" Acceptance Criterion (Non-Conformity 4) — expected and disclosed; the risk is only that a reader of `WPR-001`'s summary line alone (without reading the Closure Report) might overestimate readiness. Both documents are consistent with each other on this point, so the risk is one of a shallow read, not a documentation defect.
5. No security, data-integrity, or tenant-isolation defect was found in the authorized `Backend/Runtime/AuthorizationEngine` package itself. `EnterpriseScopeValidator`'s structural-only scope (`TD-076`) and the pre-evaluation placement (`TD-077`) are both correctly assessed as Low — neither defeats the substantive `§11.12` guarantee.

---

## 12. Certification Decision

**CERTIFIED WITH CONDITIONS.**

### Blocking (must be resolved before repository release / before proceeding to WP-05)

1. **Resolve Non-Conformity 1** — the unauthorized, undisclosed, still-wired `Backend/Services/AuthService/authorization_engine*.py` candidate implementation. Either remove it and its `main.py`/`tenant.py` wiring, or formally reconcile it (obtain `ADR-016`, refactor it onto `AuthorizationAdapter`, register it as `WP-05` `BA-01`). This must be resolved, and disclosed in whichever governance document closes it out, before this repository can be considered to have a single, unambiguous Authorization Engine.
2. **Author `ADR-016`** (or equivalent) formalizing the `IRA-RTA-001 §5` repository-owner decision, for traceability parity with `ADR-006`–`ADR-015`. (This may be satisfied jointly with Blocking Condition 1's own resolution, since both trace to the same underlying governance gap.)

### Non-Blocking (may be resolved at a future convenient touch)

3. Correct the four stale docstring references in `pipeline.py` (§10, Non-Conformity 3); register as `TD-079`.
4. `TD-071` through `TD-078` — confirmed accurate and correctly non-blocking; carry forward unchanged.
5. When real tier resolution is eventually built, evaluate reuse of the working Domain Permission resolver logic already present in the (to-be-resolved) candidate code (§10, Non-Conformity 5).

**The `Backend/Runtime/AuthorizationEngine` package itself (M1–M6) may be frozen as-is.** Nothing found in this certification requires any change to that package's own source code, tests, or documentation.

---

## 13. Recommended Next Steps

1. **Do not proceed to `WP-05` until Blocking Condition 1 (§12) is resolved.** `WP-05` is precisely the Work Package that would wire a real consumer to the Authorization Engine — beginning it while an unauthorized, functioning, uncommitted duplicate sits in the exact same territory (`Backend/Services/AuthService`) creates a concrete, avoidable risk that `WP-05`'s own implementer builds on, or is confused by, the wrong artifact. This is not a hypothetical: the candidate code already self-labels with `WP-RTA-001`/`BA-02` framing that a future reader could easily mistake for legitimate.
2. Once Blocking Condition 1 is resolved (either by removal or formal reconciliation), update `WPR-001`'s WP-RTA-001 row from "IMPLEMENTATION COMPLETE" to **"CLOSED — Certified, with Blocking Conditions Resolved"**, referencing this certification document and whatever follow-up action (deletion commit, or `ADR-016` + `WP-05` `BA-01` registration) resolved Condition 1.
3. If the repository owner elects to resolve Non-Conformity 1 via reconciliation (option b) rather than deletion, that reconciliation itself constitutes the beginning of `WP-05`'s real `BA-01` implementation and should be gap-analyzed fresh under `CLAUDE.md §19`, not treated as a mechanical port of the candidate code — Findings F-04 (not wired as a true pre-execution gate) and F-05 (no `AEO-000001` persistence) from `AUTHORIZATION_ENGINE_CONSTITUTIONAL_RESPONSE.md` still apply to the candidate code as written and must be addressed, not carried forward silently.
4. Register `TD-079` (stale `pipeline.py` docstrings) in `TECH-DEBT.md` at the next touch of that file, per `CLAUDE.md §19.8.2`'s prohibition on Technical Debt existing only in review documents.
5. Once Blocking Conditions are resolved, `WP-RTA-001` itself, as a Runtime Component delivering M1–M6, is sound and ready to serve as the seam a real `WP-05 BA-01` (or any other future Business Activity) integrates through.

---

*End of CERT-WP-RTA-001 (independent reviewer's original text).*

---

## Post-Certification Resolution

**Added by:** the implementing session, after the certification above was delivered, per explicit repository-owner instruction. **Not written or reviewed by the independent certifying reviewer** — this addendum records what was done in response to the certification, it does not re-certify it.

**Repository owner's decision:** Resolve Non-Conformity 1 / Blocking Condition 1 via **removal** (option (a) in §10/§12 above), not reconciliation.

**Actions taken:**
1. Removed `Backend/Services/AuthService/routers/authorization_engine.py`, `schemas/authorization_engine.py`, `services/authorization_engine_service.py`, `tests/test_authorization_engine_api.py`, `tests/test_authorization_engine_service.py`.
2. Reverted `Backend/Services/AuthService/main.py` and `Backend/Services/AuthService/middleware/tenant.py` to their pre-candidate, committed state — confirmed via `git diff --stat` showing zero remaining diff against `HEAD` for both files after the revert.
3. Confirmed via repository-wide grep: zero remaining references to `authorization_engine` anywhere in `Backend/Services/AuthService`.
4. Confirmed via `pytest --collect-only` against AuthService's own test suite: 572 tests collect cleanly, zero import errors, after the removal.
5. Created `architecture/07-Decisions/ADR-016_Authorization_Runtime_Consolidation.md`, formalizing the `IRA-RTA-001 §5` repository-owner decision (resolving Blocking Condition 2 in the same pass) and recording this removal action.

**Blocking Condition 1: RESOLVED — via removal, per `ADR-016`.**
**Blocking Condition 2: RESOLVED — `ADR-016` created.**

**Exactly one Authorization Engine / Authorization Runtime implementation now exists in this repository:** `Backend/Runtime/AuthorizationEngine/` (`WP-RTA-001`, certified above with these conditions now resolved). Nothing in the certified package itself (M1–M6) was modified by this resolution.

**Not re-certified.** This addendum records a factual resolution of the two Blocking Conditions; it is not, itself, an independent re-certification of the resolution action. Per the same `CLAUDE.md §19.7` discipline this whole certification exists to satisfy, if formal re-certification of the *consolidation action* is desired, that would itself require a fresh-context reviewer, not this same implementing session.

Non-Blocking items 3–5 (§12) remain open, unaffected by this resolution.
