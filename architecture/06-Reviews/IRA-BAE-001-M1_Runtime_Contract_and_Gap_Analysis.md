# IRA-BAE-001-M1 — Business Activity Engine: Runtime Contract and Gap Analysis

**Document ID:** IRA-BAE-001-M1
**Work Package:** `WP-BAE-001` (Business Activity Engine) — registered, `WPR-001 §2a`
**Milestone:** M1 — Runtime Contract / Architecture Baseline — **analysis and design only**
**Document type:** Milestone-level `CLAUDE.md §19` Implementation Start Checklist (§19.1 governing assets, §19.2 existing-asset discovery, §19.3 gap analysis, §19.4 architectural impact assessment) for M1, plus the evidence baseline M2–M7 will each re-use and re-verify.
**Prepared:** 2026-09-23. **Revised:** 2026-09-24, to record the Repository Owner's M1 Architectural Disposition (`RO-M1-01`–`RO-M1-12`, §0), reconcile the runtime contract with it, and log the `RO-M1-12` documentation corrections (§17).
**Status:** **M1 — COMPLETE WITH CONDITIONS** (§16). The runtime contract is coherent after the §0 dispositions. The conditions are listed in §16. ~~**BAE implementation has not begun and is not authorized.** No code, schema, migration, API, route, test, manifest, or execution-state table exists.~~ *(Updated 2026-09-25: accurate when this analysis was written. The M1 skeleton was subsequently authorized, implemented, independently reviewed, remediated, and accepted — see `IMP-REPORT-WP-BAE-001`. M2 is not authorized. No manifest or execution-state table exists.)*

**Classification key used throughout:**
`[LOCKED]` verbatim from a LOCKED constitutional document · `[ACTIVE]` from an Active methodology document (`IMP-001`) · `[FACT]` directly verified repository fact (file/line cited) · `[RO]` a recorded Repository Owner decision · `[CONTRACT]` runtime-contract clause traceable to `[LOCKED]`/`[ACTIVE]`/`[RO]` text · `[DESIGN]` implementation-design choice deliberately left to the milestone that builds it · `[DEFERRED → Mn]` an open item the Repository Owner has explicitly assigned to a named later milestone.

---

## 0. Repository Owner Decision Record — M1 Architectural Disposition

**Recorded:** 2026-09-24, by direct Repository Owner instruction ("RO DECISION PACKAGE — WP-BAE-001 M1 ARCHITECTURAL DISPOSITION"), responding to the twelve decision questions raised in §14.2 of this document's 2026-09-23 version. Each decision below is recorded as stated and is not reinterpreted. The instruction reaffirms: **"Do NOT begin BAE implementation yet."**

| ID | Repository Owner decision (as recorded) | Status after this revision |
|---|---|---|
| **RO-M1-01** Module placement | **APPROVED.** `Backend/Runtime/BusinessActivityEngine/` is the canonical BAE runtime module. The BAE executes **in-process within the hosting service**, not as a standalone service. Rationale recorded: consistent with the AuthorizationEngine runtime precedent; lets the BAE own the hosting service's transaction boundary; avoids cross-service database transaction ownership; keeps the BAE a platform runtime rather than placing it inside AuthService. **Explicit RO architectural decision. The module is not to be created yet.** | **RESOLVED** (decision). The module is not created. |
| **RO-M1-02** Pipeline order | **`IMP-001 §6.16` is the canonical BAE execution-pipeline order.** Where `RTA-001` and `IMP-001` conflict on ordering, `IMP-001 §6.16` governs BAE execution semantics. `RTA-001` is not to be silently rewritten. Stale `RTA-001` wording that directly affects the BAE contract is to be identified for a later correction pass. | **RESOLVED** (decision). `RTA-001` corrections identified, not performed (§14.3). One residual stage-*membership* item recorded (`R-01`, §14.4) |
| **RO-M1-03** Manifest resolution / implementation mapping | **The BAE owns Manifest Resolution at runtime**: BAR-issued identifier → canonical Business Activity implementation/manifest. BAR remains the canonical registration and identifier authority and does **not** become the runtime owner of implementation-code resolution. **Prohibited discovery means:** filesystem scanning, decorators, arbitrary module scanning, FastAPI route discovery, implementation heuristics. The mapping must use an explicit governed manifest/registry contract. The manifest schema is not to be invented now. **M2 defines the minimum manifest contract and identifies whether a new governed artifact is required.** | **RESOLVED** (ownership) + **DEFERRED → M2** (manifest contract) |
| **RO-M1-04** Execution-time registration gate | **The BAE is the runtime consumer/enforcer of the registration prerequisite.** WP-23 Workstream E remains responsible for the BAR-side execution-gate mechanism/authority. The BAE must not duplicate BAR registration logic or become a second registration authority. Relationship: BAR (authoritative registration state) → the BAE queries/consumes it → unregistered cannot execute → registered proceeds. The exact API/repository/interface boundary is designed in M2. WP-23 Workstream E is not modified. | **RESOLVED** (ownership split) + **DEFERRED → M2** (interface boundary) |
| **RO-M1-05** Resolution verification | Activity Resolution verifies **only the minimum authoritative contract** required by `IMP-001 §6.16` and the BAE runtime contract. No invented validation rules. Where `IMP-001` requires version/status/invocation-method verification and BAR lacks the metadata, M2 identifies, **per datum**: the authoritative source, whether it exists, and whether a new manifest/metadata contract is required. BAR's scope is not silently expanded. | **RESOLVED** (principle) + **DEFERRED → M2** (per-datum source analysis) |
| **RO-M1-06** `IMP-001 §6.20`–`§6.29` scope | The Charter is **not** expanded merely because `§6.20`–`§6.29` exist. M1–M7 remain within existing Charter scope, unless M1 shows a specific `§6.20`–`§6.29` requirement is already mandatory for a Charter-included BAE responsibility. Such cases are documented as **dependencies**, not scope expansion. No Charter amendment. | **RESOLVED.** Dependencies documented (§14.5) |
| **RO-M1-07** Durable execution state | **APPROVED IN PRINCIPLE.** The BAE shall have durable execution state. M5/M6 define the minimum persistence model. The design must distinguish runtime/in-memory context, durable execution state, transaction state, and terminal/non-terminal lifecycle state. No table yet. | **RESOLVED** (principle) + **DEFERRED → M5/M6** (model) |
| **RO-M1-08** State transitions | The canonical transition set derives from (1) `IMP-001`'s state model, (2) the approved M1 runtime contract, (3) explicit lifecycle semantics established in M5/M6 design. Transitions are not invented to fill gaps. Any transition without authoritative support is identified as an unresolved RO decision. | **RESOLVED** (method) + **DEFERRED → M5/M6.** Authoritative vs. unsupported transitions inventoried (§11.2) |
| **RO-M1-09** Audit timing | Preserve the distinction between execution-time audit recording and post-commit finalization. The BAE must not invent a replacement Audit Engine. M5 identifies: audit information required before commit; what can only be finalized after commit; the existing authoritative audit mechanism, if any; what remains a platform dependency. If no authoritative persistent audit mechanism exists, the dependency is recorded rather than fabricated. | **RESOLVED** (principle) + **DEFERRED → M5** |
| **RO-M1-10** Platform services | **No fake** Event Bus, Audit Engine, Notification Platform, or Observability Platform built to satisfy the BAE. Where log/correlation mechanisms are real and already authoritative, the BAE may integrate with them **at their existing capability boundary**. Where a true platform service is absent: record it as a dependency, create no substitute under the BAE, and do not claim it exists. C-132 keeps ownership of enterprise notification capability. | **RESOLVED** |
| **RO-M1-11** Cross-service BAR access | **DEFERRED.** Becomes an architectural decision only once the first BAE consumer and its hosting boundary are known. Does not block M1 closure. | **DEFERRED → first-consumer selection (M7)** |
| **RO-M1-12** Stale documentation | **AUTHORIZED — narrow correction pass only.** (1) The Charter's stale "no production consumer" statement; (2) directly corresponding stale AuthorizationEngine README / WP-RTA-001 status wording making the same factual claim; (3) the Charter's stale statement that an Event Bus, Audit Engine and Observability Platform exist, replaced with an evidence-supported description. No change to scope, milestones, governance decisions, AuthorizationEngine design, event/audit/observability design, or `IMP-001`. Every corrected file and section recorded. | **RESOLVED — performed** (§17) |

---

## 1. Purpose and Authorization

**Authorization:** (1) Repository Owner decision, 2026-09-23: *"AUTHORIZE WP-BAE-001 M1 — RUNTIME CONTRACT / ARCHITECTURE BASELINE GAP ANALYSIS"*, limited to M1 analysis and design. (2) Repository Owner M1 Architectural Disposition, 2026-09-24 (§0), authorizing this revision and the `RO-M1-12` correction pass only. Neither authorizes BAE implementation, M2 or later, code, schema, API, migration, or runtime integration.

**Purpose:** establish, from repository evidence only, (A) what the repository already provides, (B) what `IMP-001 §6.15`–`§6.19` require, (C) what the BAE must own, (D) what it must integrate with, (E) what is missing, and (F) which architectural decisions are still required before any BAE code is written.

**Pre-analysis state reconfirmation (2026-09-23, before the first version; nothing altered):**

| Check | Result |
|---|---|
| `WP-BAE-001` registered | Yes — `WPR-001 §2a` line 132, "CHARTER APPROVED — REGISTERED. IMPLEMENTATION NOT YET AUTHORIZED." |
| M1 already started | No — no M1 artifact, gap analysis, or IMP-REPORT for `WP-BAE-001` existed |
| BAE implementation | None — zero hits for `BusinessActivityEngine`/`business_activity_engine`/`BusinessActivityContext` in any `.py` under `Backend/`; `Backend/Runtime/` contains only `AuthorizationEngine` |
| WP-23 Workstream D | Deferred, unamended (Charter file last modified 2026-09-22 13:24) |
| BAR Workstreams A–C | Intact (all ten files last modified 2026-09-22 15:24–16:19) |
| C-024 BA-01 | Unregistered (`BAR-INDEX.md §7`; no seeding in either BAR migration) |
| HEAD / staging | `8323bf3`; nothing staged |

## 2. Scope and Exclusions

**In scope:** requirement-to-repository mapping for the 21 responsibility areas the M1 authorization enumerates; the M1-level runtime contract (16 clauses), separated into contract / design / deferred; boundaries; BAR and AuthorizationEngine integration contracts; transaction/state implications; module placement; a governance cross-check; M2–M7 sequencing implications; the record of the §0 dispositions.

**Excluded:** any BAE code or stub; any change to `Backend/Runtime/AuthorizationEngine` code, BAR A–C, `BAR-INDEX.md`, the WP-23 Charter (incl. Workstreams D and E), `IMP-001`, `RTA-001`, `IRA-BAE-001`, or C-024; any Charter scope or milestone change; any Business Activity registration or identifier assignment; any migration, schema, API, route, test, manifest, or execution-state table; any M2+ work. The only documentation edits permitted are the `RO-M1-12` corrections (§17). **Contradictions are reported (§14), never silently reconciled** (`CLAUDE.md §16`).

## 3. Repository Evidence Examined

**Governing documents (read in full for the cited ranges):**
- `architecture/05-Implementation/WP-BAE-001_Business_Activity_Engine_Charter.md` (all)
- `architecture/05-Implementation/IRA-BAE-001_Business_Activity_Engine_Implementation_Readiness_Assessment.md` (all)
- `architecture/06-Reviews/BAR-WP23-WORKSTREAM-D-BUSINESS-ACTIVITY-ENGINE-PREREQUISITE-INVESTIGATION.md` (all)
- `architecture/03-Engineering/IMP-001_Implementation_Playbook.md`:
  - `§6.15`–`§6.19` (lines 2326–4234) in full
  - `§6.7` BAC and `§6.14` CBAM (2105–2140, 2283–2321)
  - `§6.20` (4236–4296 plus subsection headings)
  - `§6.21`, `§6.23`–`§6.28` purpose statements and subsection headings
  - `§6.22.1a`–`§6.22.14` (4935–5349)
  - `§6.28.4` (7346–7376)
  - `§6.29.1`–`§6.29.6`, `§6.29.11`–`§6.29.12` (7727–7850, 8105–8140)
- `architecture/02-Constitutional/RTA-001 - Runtime Architecture and Execution.md` `[LOCKED]` — `§3.5`, `§3.6`, `§6.4`–`§6.6`, `§11.5`, `§11.13`
- `architecture/00-Governance/WPR-001_Work_Package_Roadmap.md` — `§2a` (WP-23, WP-BAE-001, WP-RTA-001 rows); `WP-13` row (line 41)
- `architecture/05-Implementation/WP-23_Enterprise_BAR_Mechanism_Implementation_Charter.md` — `§7`–`§13`
- `architecture/06-Reviews/ROD-ENTERPRISE-BAR-Decision-Preparation.md` — `§0b` (D2), `§0c` (D3), `§0d` (D5), `§0e` (D6)
- `architecture/05-Implementation/WP-RTA-001_Authorization_Runtime_Engine.md` — status, Responsibility Boundary, Interfaces, Exit Criteria
- `architecture/06-Reviews/CERT-WP-RTA-001_Authorization_Runtime_Engine.md` — verdict ("CERTIFIED WITH CONDITIONS")
- `architecture/00-Governance/BAR-INDEX.md` (all)
- `architecture/06-Reviews/TECH-DEBT.md` — `TD-071`, `TD-076`, `TD-078`, `TD-105`, `TD-106`
- `architecture/07-Decisions/ADR-036_Licensing_and_Entitlement_Persistence_Implementation_Ownership.md` (header — "AuthService, Modular-Monolith Phase")

**Source code (read directly):**
- `Backend/Runtime/AuthorizationEngine/README.md`, `authorization/models.py`, `adapters/authorization_adapter.py`; package layout (26 git-tracked files, commit `7fac19c`)
- `Backend/Services/AuthService/authz_integration/domain_permission_resolver.py`, `authz_integration/runtime_engine_path.py`
- `Backend/Services/AuthService/dependencies.py` lines 95–175 (`enforce_domain_permission`, `require_domain_permission`) and its 7 call sites in `routers/approval_authority.py` (1), `routers/delegation_policy.py` (1), `routers/domain_permission.py` (5); WP-13 commits `a180ca4`, `d5004b2`, `909ba08`
- `Backend/Services/AuthService/models/bar_registration.py`, `models/bar_identifier_ledger.py`, `repositories/bar_registration_repository.py`, `services/bar_registration_service.py`
- `Backend/Services/AuthService/observability.py`; `middleware/logging.py` (correlation ID); `main.py` (middleware registration); `models/database.py` (`DatabaseSessionManager.get_session`)
- `Backend/Shared/Events/event_publisher.py`, `Backend/Shared/Logging/audit_logger.py` (headers/classes); `Backend/aurex/backend/shared/` shim (Release A1)
- Repository-wide `__tablename__` search for audit/event/notification/workflow/metadata/screen/execution/activity tables; `screen_registry` search; CBAM/manifest artifact search

## 4. Current-State Architecture

`[FACT]` The runtime today, as it actually executes:

```
Client ──HTTP──▶ FastAPI app (per service; AuthService hosts most capabilities — ADR-036 "Modular-Monolith Phase")
                   │  middleware: TenantMiddleware, LoggingMiddleware (X-Correlation-ID → observability.CorrelationContext)
                   ▼
                 Router handler  (30 entries under AuthService `routers/`; 105 mutating routes across Backend/Services/*/routers)
                   │  auth: require_platform_admin / enforce_domain_permission (WP-13) / require_authority_holder
                   │        └─ enforce_domain_permission ─▶ AuthorizationAdapter ─▶ EvaluationPipeline ─▶ AuthorizationEngine
                   ▼
                 Capability service (validation, business rules, repository calls, record_audit(), publish_event())
                   ▼
                 AsyncSession from db_manager.get_session  ── commit at end of request / rollback on exception
```

- **No Business Activity Engine exists.** Every Business Activity executes by direct FastAPI routing (investigation §7, re-confirmed).
- **BAR exists but nothing calls it at runtime.** `BarRegistrationService.register()` has no router and no caller outside its own tests. `bar_registration` has zero rows by construction.
- **The AuthorizationEngine already has a committed consumer.** `WP-13`'s `enforce_domain_permission` (`dependencies.py:95–154`) evaluates real Domain Permission grants through the engine at 7 call sites across 3 routers. `WP-13` is recorded in `WPR-001` as "Not yet certified — in progress."
- **Platform services are stand-ins, not engines.** Audit, events, and metrics are structured log lines (`observability.py`, self-described as an "explicitly temporary local substitute"). `Backend/Shared/Events` defines an `EventPublisher` abstraction whose `KafkaEventPublisher` carries no broker client (`event_publisher.py:71`). No Workflow Engine, Metadata Engine, Notification Engine, AI Runtime Engine, or Audit Engine exists as a platform service.

## 5. IMP-001 Requirement Mapping

Classification vocabulary as authorized: **IMPLEMENTED / REUSABLE**, **PARTIALLY IMPLEMENTED**, **SPECIFIED BUT NOT IMPLEMENTED**, **ARCHITECTURALLY UNDEFINED**, **EXTERNAL DEPENDENCY**, **GOVERNANCE DECISION REQUIRED**. No implementation is inferred from a specification describing it. The final column shows the effect of the §0 dispositions. The *repository-evidence* classification is unchanged by a decision: a decision assigns ownership; it does not build anything.

| # | Area | IMP-001 requirement (source) | Repository evidence | Classification | After §0 |
|---|---|---|---|---|---|
| 1 | Business Activity Resolution | "Locate the Business Activity implementation" (`§6.15.4`); verify Identifier, Version, Status, Invocation Method, Business Domain, Required Platform Version; unresolved ⇒ terminate (`§6.16.5`) | BAR gives identity + registration only. No version, lifecycle status, invocation method, domain, platform version, or implementation mapping (D2) | **PARTIALLY IMPLEMENTED** | Owner: BAE (`RO-M1-03`). Verification scope: minimum authoritative (`RO-M1-05`). Per-datum sources **DEFERRED → M2** |
| 2 | BAR-exclusive discovery | Exclusively through the Registry (`§6.22.8`); `RTA-001 §6.6` `[LOCKED]` | BAR query surface exists (by identifier / by WP+reference); no consumer | **PARTIALLY IMPLEMENTED** | Prohibited discovery means fixed (`RO-M1-03`). Governed manifest/registry contract **DEFERRED → M2** |
| 3 | Context Initialization | Once, before business processing; immutable except metrics/state (`§6.16.6`, `§6.17.2`–`§6.17.4`) | None; frozen-dataclass precedent (`AuthorizationContext`) | **SPECIFIED BUT NOT IMPLEMENTED** | M1 skeleton / M3 |
| 4 | Business Activity Context | Ten canonical sections (`§6.17.5`) + immutability + propagation. *"18-part" counts subsections, not parts* (`X-13`) | Partial value sources: JWT claims, `TenantMiddleware`, `CorrelationContext` | **SPECIFIED BUT NOT IMPLEMENTED** (model); inputs **PARTIALLY IMPLEMENTED** | M1 skeleton / M3 |
| 5 | Authorization Context construction | BAE constructs it (`RTA-001 §11.5` `[LOCKED]`) | `AuthorizationContext` + `AuthorizationAdapter.build_context` reusable unmodified | **IMPLEMENTED / REUSABLE** (model + adapter) | M4 |
| 6 | AuthorizationEngine invocation | Before any business processing (`§6.16.7`) | Invocation path real (WP-13). Only the Domain Permission tier has a real resolver. Per-BA authorization policy source undefined | **IMPLEMENTED / REUSABLE** + **ARCHITECTURALLY UNDEFINED** (per-BA policy) | Per-BA policy source: CBAM "Authorization Requirements" (`§6.14`/`§6.29.12`) is the documented candidate, assessed with the M2 manifest contract (§14.5, `D-09`) |
| 7 | Input Validation | Technical + Business validation (`§6.16.8`) | Pydantic per route; business validation inside capability services. No CBAM artifact exists | **PARTIALLY IMPLEMENTED** + **ARCHITECTURALLY UNDEFINED** (input-contract source) | Input Contract is a CBAM attribute (`§6.14`). Source assessed in M2 manifest contract. Business Validation via registered Custom Validators (`§6.15.8`) is `[DESIGN]`, M3 |
| 8 | Metadata Resolution | `§6.16.9`; Metadata Engine (`RTA-001 §3`) | No Metadata Engine; `screen_registry` absent from `Backend/`/`database/` | **EXTERNAL DEPENDENCY** | Dependency recorded; no substitute (`RO-M1-10`) |
| 9 | Workflow Coordination | `§6.16.10`; Workflow Context optional (`§6.17.11`) | No Workflow Engine | **EXTERNAL DEPENDENCY** | Standalone execution only; dependency recorded (`RO-M1-10`) |
| 10 | Business Rule Execution boundary | Only stage implemented by domains (`§6.16.11`) | Capability services also do auth/audit/events/rollback today | **SPECIFIED BUT NOT IMPLEMENTED** | Boundary fixed (C8). Migration excluded (Charter §5) |
| 11 | Persistence Coordination | `§6.16.12` | `AsyncSession` + `BaseRepository`; no verified optimistic-concurrency convention | **PARTIALLY IMPLEMENTED** | M5 |
| 12 | Transaction Management | `§6.19` | Request-scoped session commit/rollback in `get_session` | **PARTIALLY IMPLEMENTED** | In-process placement lets the BAE own the hosting-service transaction (`RO-M1-01`). M5 |
| 13 | State Model | Nine states (`§6.18.4`); BAE-owned; invalid transitions rejected; durable history (`§6.18.11`) | None | **SPECIFIED BUT NOT IMPLEMENTED** | Durable state approved in principle (`RO-M1-07`). Transition set **DEFERRED → M5/M6** (`RO-M1-08`, §11.2) |
| 14 | Post-Commit Processing | Only after commit (`§6.16.14`, `§6.19.14`) | Today events/audit are logged before commit | **SPECIFIED BUT NOT IMPLEMENTED** | M5 |
| 15 | Response Generation | Transport-independent (`§6.16.15`) | Per-route HTTP schemas | **SPECIFIED BUT NOT IMPLEMENTED** | M6 |
| 16 | Event Publication | Post-commit, reliable (`§6.16.16`); Event Bus (`RTA-001 §6.4`) | `publish_event` log line; `Shared/Events` abstraction, no broker | **EXTERNAL DEPENDENCY** | No fake Event Bus. Integration at existing capability boundary only (`RO-M1-10`) |
| 17 | Notification Integration | `§6.15.4` | C-132 capability-owned notification; no Notification Engine | **EXTERNAL DEPENDENCY** | C-132 ownership preserved; dependency recorded (`RO-M1-10`) |
| 18 | Audit Recording | Immutable trail; post-commit (`§6.16.14`) vs failure audit (`§6.18.9`) | `record_audit` / `AuditLogger` log-based; `ReportingService.audit_logs` capability-local. No Audit Engine | **EXTERNAL DEPENDENCY** | Execution-time vs. post-commit distinction preserved; no replacement Audit Engine (`RO-M1-09`). **DEFERRED → M5** |
| 19 | AI Assistance | Post-commit hooks (`§6.16.14`); AI Context (`§6.17.14`) | AIService features are capability-specific; `AgentOrchestrator` has zero code | **EXTERNAL DEPENDENCY** | M6, limited to what `IMP-001` names |
| 20 | Error Handling | "Canonical error management" (`§6.15.4`) | Per-route `HTTPException`; capability exceptions | **PARTIALLY IMPLEMENTED** | `§6.28.4` classification recorded as a **dependency** (`RO-M1-06`, §14.5) |
| 21 | Observability | `§6.15.4`, `§6.18.14`, `§6.19.15` | Correlation real per service; `record_metric` log line; `PipelineObserver` precedent (`TD-078`) | **PARTIALLY IMPLEMENTED** + **EXTERNAL DEPENDENCY** | Integrate with real correlation mechanism at its capability boundary; no fake Observability Platform (`RO-M1-10`). `§6.27` recorded as a **dependency** |

## 6. Gap Analysis (`CLAUDE.md §19.3`)

**Existing assets that satisfy a requirement as-is (Reuse):**
- `AuthorizationContext`, `AuthorizationRequest`, `AuthorizationAdapter`, `EvaluationPipeline` (areas 5–6)
- `BarRegistrationRepository.get_by_identifier`, read-only (area 1)
- `CorrelationContext` + `LoggingMiddleware` `X-Correlation-ID` handling (areas 4, 21)
- `DatabaseSessionManager` / `AsyncSession` / `BaseRepository` (areas 11–12)
- `PipelineObserver` pattern, as a design precedent only (area 21)

**Existing assets requiring extension (not performed):**
- Transaction ownership moves from `get_session` to the BAE for BAE-routed activities only, with no change to `get_session` itself (M5).
- Integration with log/correlation mechanisms happens at their existing capability boundary (`RO-M1-10`). The hosting service supplies its own mechanism through a BAE seam. The BAE does not import AuthService's `observability.py` directly, which would couple a platform runtime to one service (`§6.15.9`). `[DESIGN]`, M5/M6.

**Missing architecture — status after §0:**

| Gap | Status |
|---|---|
| Implementation binding (identifier → executable code) | Owner decided: BAE (`RO-M1-03`). Contract **DEFERRED → M2** |
| Manifest resolution | Owner decided: BAE (`RO-M1-03`). `IMP-001 §6.14`/`§6.29` already define the CBAM as the governed manifest concept. No CBAM instance exists, and CBAM attributes carry no implementation-code reference (`§6.29.6` read; none found). **DEFERRED → M2** |
| Per-BA authorization policy | Candidate source: CBAM "Authorization Requirements" (`§6.14`; `§6.29.12`). **DEFERRED → M2** (manifest) / M4 (binding) |
| Per-BA input contract | Candidate source: CBAM "Input Contract" (`§6.14`; BAC `§6.7`). **DEFERRED → M2/M3** |
| Transition table | **DEFERRED → M5/M6** (§11.2) |
| Execution-state persistence | Approved in principle. **DEFERRED → M5/M6** |

**Why creation is necessary (for M1, when authorized):**
- No existing module performs context construction, pipeline sequencing, or execution-state ownership.
- The AuthorizationEngine is excluded by its own Charter.
- `[RO]` Option B forbids assigning the BAE to an existing component.

The new Runtime Component's location is now fixed by `RO-M1-01`.

## 7. BAE Runtime Contract (M1 level, reconciled with §0)

Each clause is labelled **[CONTRACT]** (binding, traceable to source or `[RO]`), **[DESIGN]** (deliberately left to the building milestone), or **[DEFERRED → Mn]** (open, assigned by the Repository Owner to a named milestone).

**C1 — Invocation boundary.**
- [CONTRACT] One canonical entry, `execute(invocation) → response`, running **in-process within the hosting service** (`RO-M1-01`). It is the exclusive execution path for BAE-routed Business Activities (`§6.15.5`, `§6.15.10`).
- [CONTRACT] Responses are transport-independent (`§6.16.15`). FastAPI, event subscribers, schedulers, and AI callers are invokers (`§6.15.3`; Request Reception, `§6.16.4`).
- [CONTRACT] Callers never pass a pre-built context (`§6.16.6`).
- [DESIGN] Signature details; the shape of the invoker adapter.

**C2 — Business Activity identity.**
- [CONTRACT] The target is named by its BAR-issued `BA-NNNNNN` identifier (D5 `[RO]`). The BAE never mints or reformats identifiers.
- [DESIGN] Whether invokers may also address by `(owning_work_package, business_activity_reference)`.

**C3 — BAR lookup and Manifest Resolution.**
- [CONTRACT] **The BAE owns runtime Manifest Resolution:** BAR-issued identifier → canonical Business Activity manifest/implementation (`RO-M1-03`; consistent with `IMP-001 §6.29.3` "The Business Activity Engine consumes the CBAM" and `§6.29.12`).
- [CONTRACT] BAR is consulted **read-only** for registration state. It does not become the owner of implementation-code resolution, and it is never written, extended, or duplicated (`RO-M1-03`; Charter §7; D2).
- [CONTRACT] The binding **must not** be obtained by filesystem scanning, decorators, arbitrary module scanning, FastAPI route discovery, or implementation heuristics (`RO-M1-03`; `RTA-001 §6.6` `[LOCKED]`; `§6.22.8`; `§6.29.12` "never rely upon implementation-specific assumptions"). It must come from an explicit governed manifest/registry contract.
- [CONTRACT] An unresolvable identifier or manifest terminates execution before business processing (`§6.16.5`).
- [DEFERRED → M2] The minimum manifest contract, derived from the existing CBAM definition (`§6.14`/`§6.29`) rather than invented, and whether a new governed artifact is required (`RO-M1-03`).

**C4 — Activity registration precondition.**
- [CONTRACT] **The BAE is the runtime consumer/enforcer** of the registration prerequisite (`RO-M1-04`). BAR (via WP-23 Workstream E's gate mechanism/authority) holds the authoritative registration state.
- [CONTRACT] Unregistered ⇒ cannot execute. Registered ⇒ proceeds to the pipeline.
- [CONTRACT] The BAE contains no registration logic of its own and is not a second registration authority.
- [CONTRACT] Consistent with D8 `[RO]`: the 21 existing Business Activities are not routed through the BAE until their own D9 cutover, so the BAE never denies their current direct-routing execution.
- [DEFERRED → M2] The exact API/repository/interface boundary between the BAE and the Workstream E gate. WP-23 Workstream E is not modified by this document.

**C5 — Input / context construction.**
- [CONTRACT] Exactly once, by the BAE, before authorization (`§6.16.6`).
- [CONTRACT] Immutable apart from runtime metrics and execution state (`§6.17.16`).
- [CONTRACT] The ten canonical sections (`§6.17.5`). Workflow and AI Context are optional.
- [CONTRACT] Identity/Organization come from authenticated claims, never from the payload (`§6.17.7`; `CLAUDE.md §21.4`).
- [CONTRACT] Correlation is reused from the hosting service's real correlation mechanism (`§6.17.15`; `RO-M1-10`).
- [DESIGN] Concrete types. Sections without a source are marked `NOT_AVAILABLE`, never fabricated.

**C6 — Authorization interaction.**
- [CONTRACT] The BAE builds an `AuthorizationRequest`, calls the existing `AuthorizationAdapter.evaluate()`, and consumes the `EvaluationResult` unchanged (`RTA-001 §11.5`/`§11.13` `[LOCKED]`).
- [CONTRACT] It never evaluates precedence and never modifies the AuthorizationEngine.
- [CONTRACT] Authorization completes before business processing (`§6.16.7`).
- [CONTRACT] **Fail-closed:** any decision other than `ALLOW` terminates execution before business processing (WP-13 precedent; `CLAUDE.md §19.8.5`).
- [DEFERRED → M2/M4] The per-BA resolver binding source (candidate: CBAM "Authorization Requirements").
- [DEFERRED → M5/M6] Whether `ESCALATED`/`DELEGATED`/`CONDITIONAL` should map to `Waiting` rather than termination (`U-10`, §11.2). Until decided, fail-closed governs.

**C7 — Execution lifecycle and pipeline order.**
- [CONTRACT] **Pipeline order is `IMP-001 §6.16.3`** (`RO-M1-02`): Request Reception → Activity Resolution → Execution Context Initialization → Authorization Evaluation → Input Contract Validation → Business Validation → Metadata Resolution → Workflow Resolution → Business Rule Execution → Persistence Coordination → Transaction Commit → Domain Event Publication → Notification Processing → Audit Recording → AI Assistance Hooks → Response Generation.
- [CONTRACT] No stage is bypassed unless the Business Activity Contract designates it optional (`§6.16.3`).
- [CONTRACT] Manifest Resolution sits inside Activity Resolution (`RO-M1-03`; `§6.16.5` "Resolve the registered Business Activity"). Enterprise Context resolution sits inside Context Initialization (`§6.17.9`). Neither is an additional stage.
- [CONTRACT] The BAE exclusively owns execution state (`§6.18.5`). The nine canonical state names are used verbatim (`§6.18.4`).
- [CONTRACT] Only authoritatively supported transitions are permitted (§11.2). Anything else is rejected, not invented (`RO-M1-08`).
- [DEFERRED → M5] `RTA-001 §6.5`'s "Knowledge Graph Update" stage has no `§6.16.3` counterpart (`R-01`, §14.4).

**C8 — Business-rule delegation.**
- [CONTRACT] The capability supplies business logic only. It reads the context and never commits, rolls back, opens sessions, authorizes, publishes, audits, notifies, or invokes workflow (`§6.16.11`, `§6.19.3`).
- [CONTRACT] Its outcome (result + requested Domain Events) returns to the BAE.
- [CONTRACT] The BAE has no domain knowledge (`§6.15.9`).
- [DESIGN] Handler interface; extension-by-registration (`§6.15.8`), where registration is itself declared through the governed manifest contract (C3), never through decorators or scanning (`RO-M1-03`).

**C9 — Persistence / transaction boundary.**
- [CONTRACT] One Business Transaction per execution (`§6.19.5`), opened and committed or rolled back only by the BAE (`§6.19.3`), on the **hosting service's own database** (`RO-M1-01`; `CLAUDE.md §8`).
- [CONTRACT] Commit only after authorization, validation, business rules, persistence, and integrity verification succeed (`§6.19.10`). Pre-commit failure restores the pre-execution state (`§6.19.11`).
- [CONTRACT] No two-phase commit; cross-service effects use events/compensation (`§6.19.9`).
- [DESIGN] Savepoints, nested boundaries, optimistic concurrency (M5).

**C10 — State transitions and execution state.**
- [CONTRACT] Every transition emits an internal lifecycle event, distinct from Domain Events (`§6.18.13`). Failure carries reason, diagnostics, and correlation ID (`§6.18.9`).
- [CONTRACT] Execution history is never deleted (`§6.18.11`).
- [CONTRACT] Execution state is durable (`RO-M1-07`, approved in principle).
- [CONTRACT] Four concerns stay distinct (`RO-M1-07`): runtime/in-memory context, durable execution state, transaction state, and terminal/non-terminal lifecycle state.
- [DEFERRED → M5/M6] The minimum persistence model, which will be a new table under its own `CLAUDE.md §19.4` assessment. Also the transition-set completion (§11.2).

**C11 — Post-commit processing.**
- [CONTRACT] Domain Event publication, notification, workflow continuation, AI hooks, analytics, monitoring, and audit **finalization** occur only after a successful commit (`§6.16.14`, `§6.19.14`).
- [CONTRACT] Post-commit failures do not alter the commit decision and do not modify committed objects (`§6.19.10`, `§6.19.14`).
- [DESIGN] Reliability mechanism (M5). Any persisted form needs its own assessment.

**C12 — Event / notification / audit integration.**
- [CONTRACT] The BAE coordinates and never rebuilds. **No fake** Event Bus, Audit Engine, Notification Platform, or Observability Platform (`RO-M1-10`).
- [CONTRACT] Where a real mechanism exists (correlation; the per-service structured audit/event log calls that D2 `[RO]` names as the existing governing mechanism), the BAE integrates at that mechanism's existing capability boundary. Where a true platform service is absent, it is recorded as a dependency (§13) and never claimed.
- [CONTRACT] C-132 keeps ownership of enterprise notification capability.
- [CONTRACT] Execution-time audit recording and post-commit audit finalization remain distinct. The BAE does not invent a replacement Audit Engine (`RO-M1-09`).
- [DEFERRED → M5] Pre-commit vs. post-commit audit content; the authoritative audit mechanism, if any; the resulting platform dependency (`RO-M1-09`).

**C13 — Response contract.**
- [CONTRACT] Transport-independent response: outcome, final state, correlation ID, duration, event references, messages/warnings (`§6.16.15`), plus the Authorization Decision and Runtime Trace as returned.
- [CONTRACT] Never a fabricated success for a `NOT_IMPLEMENTED` stage.
- [DESIGN] Field names. HTTP mapping belongs to the invoker adapter.

**C14 — Error contract.**
- [CONTRACT] Every termination names the failing stage, reason, correlation ID, and resulting state. An unbuilt stage reports `NOT_IMPLEMENTED`.
- [CONTRACT] Error classification follows `IMP-001 §6.28.4`'s ten categories. This is recorded as a **dependency** of the Charter-included "canonical error management" responsibility, not as scope expansion (`RO-M1-06`, §14.5 `D-06`).
- [DESIGN] Exception types (M6).

**C15 — Observability contract.**
- [CONTRACT] Per execution: correlation ID, activity identifier, per-stage timing/outcome, state transitions (`§6.18.14`).
- [CONTRACT] Per transaction: the `§6.19.15` field set.
- [CONTRACT] An observer's failure never alters the result (AuthorizationEngine M5 precedent).
- [CONTRACT] Emission goes through the hosting service's real correlation/log mechanism at its capability boundary. There is no substitute Observability Platform (`RO-M1-10`).
- [DEFERRED → M6] Which `§6.27` requirements are dependencies of the Charter's Observability responsibility (§14.5 `D-05`).

**C16 — AI-assistance boundary.**
- [CONTRACT] AI hooks run post-commit, only where configured (`§6.16.14`). AI Context is optional.
- [CONTRACT] The BAE does not construct or host `AgentOrchestrator`, which is a future invoker (`§13.6c`).
- [CONTRACT] AI output never bypasses authorization or the transaction boundary.
- [DESIGN] Hook interface (M6), limited to what `IMP-001` names.

**Coherence check after §0:**
- Every clause now has either a contract statement or an explicit milestone assignment.
- No clause depends on an undecided *ownership* question.
- No clause requires expanding BAR, amending the Charter, or changing `IMP-001`.
- The one ordering conflict with LOCKED `RTA-001` is disposed by `RO-M1-02`. The one ownership conflict with LOCKED `RTA-001` is disposed by `RO-M1-03`.
- Both leave `RTA-001` text needing a later governed correction (§14.3). This is a documentation condition (§16), not an open decision.

## 8. BAE Architectural Boundaries

| Counterpart | BAE relationship | BAE must NOT |
|---|---|---|
| **BAR** (WP-23 A–C) | Read-only consumer of registration state; runtime enforcer of the registration prerequisite (`RO-M1-04`) | Own, write, extend, duplicate, or become a second registration/discovery authority; mint identifiers; populate `BAR-INDEX.md`; own implementation-code resolution inside BAR (`RO-M1-03`) |
| **WP-23 Workstream E** | Consumes the gate mechanism/authority Workstream E owns (`RO-M1-04`) | Re-implement it |
| **AuthorizationEngine** (WP-RTA-001) | Constructs `AuthorizationRequest`/`AuthorizationContext`; invokes via `AuthorizationAdapter`; consumes `EvaluationResult` | Evaluate precedence; modify any file under `Backend/Runtime/AuthorizationEngine`; fabricate `ALLOW` |
| **Capability services** | Invokes their business-rule handlers, bound through the governed manifest contract | Own their rules, Business Objects, or lifecycles; know domain semantics |
| **Business Objects** | Coordinates persistence inside the BAE-owned transaction | Own any |
| **Business Activities** | Executes them; owns *execution* state | Author or register them |
| **Existing FastAPI routing** | Remains the operative path for every existing BA until each capability separately migrates (Charter §5; D2) | Be retrofitted in bulk; discover activities from routes (`RO-M1-03`) |
| **Platform services** | Coordinates with real mechanisms at their capability boundary | Build substitutes (`RO-M1-10`) |
| **AgentOrchestrator** | Future invoker | Construct or host it |
| **AIService** | Future AI-hook provider | Absorb its capability-specific engines |
| **C-132 Notification** | Future notification-integration counterpart | Absorb or duplicate C-132 (`RO-M1-10`) |
| **WP-RTA-001** | Fulfils its "Authorization Context Construction — Business Activity Engine" boundary row | Re-scope or reopen WP-RTA-001 |

## 9. BAR Integration Contract

- **Surface consumed:** `BarRegistrationRepository.get_by_identifier(identifier) → BarRegistration | None` (read-only), or whatever Workstream E exposes as the gate interface. The choice is **DEFERRED → M2** (`RO-M1-04`). `BarRegistrationService.register()` is never called by the BAE.
- **Fields the BAE may rely on (exactly D2's eight):** `identifier`, `business_activity_reference`, `owning_capability`, `owning_work_package`, `registration_status` (always `REGISTERED`), `registering_act`, `registered_at`, `is_retroactive`.
- **Semantics:** a row exists ⇒ registered ⇒ may proceed. No row ⇒ cannot execute.
- **Not available from BAR (D2/D6 `[RO]`):** version, `§6.22.9` lifecycle status, invocation method, domain, platform version, implementation mapping, execution policy, authorization policy, manifest. `RO-M1-05` requires M2 to identify each datum's authoritative source without expanding BAR.
- **Tenant scope:** `bar_registration` has no organization column. `CLAUDE.md §21.4` attaches to M3/M4 context construction and authorization, not to the BAR lookup itself (`X-15`).
- **Service locality:** BAR is local to AuthService. Cross-service access is **DEFERRED** (`RO-M1-11`) until the first consumer's hosting boundary is known.

## 10. AuthorizationEngine Integration Contract

- **Surface consumed (unmodified):** `AuthorizationAdapter(pipeline).evaluate(AuthorizationRequest) → EvaluationResult`; `EvaluationPipeline`; `ResolverRegistry`; tier resolver ABCs.
- **Request mapping:** `identity_id` ← Identity Context; `organization_id` ← Organization Context. Remaining fields come from the corresponding context sections where a real source exists; otherwise they stay at their defaults and are never guessed.
- **Governed request:** carried by resolver construction (WP-13 pattern), not by `AuthorizationContext`. Per-BA binding source **DEFERRED → M2/M4** (candidate: CBAM "Authorization Requirements").
- **Decision handling:** fail-closed (C6). The `EvaluationResult` is attached unchanged to the Authorization Context section and to the response.
- **Import mechanism:** the existing interim `sys.path` approach (`runtime_engine_path.py`) or formal packaging. `[DESIGN]`, M4.
- **Record corrected:** the engine already has a committed consumer (WP-13). M4 will be the first consumer *through the BAE* (`X-06`, corrected under `RO-M1-12`, §17).

## 11. Transaction and State Model Implications

### 11.1 Transaction and state

- **Transaction owner shift.** For BAE-routed activities the BAE owns commit/rollback on the hosting service's session (`§6.19.3`; `RO-M1-01`). Handlers only flush through repositories. `[DESIGN]`, M5.
- **Existing services conflict with `§6.19.3`.** `BarRegistrationService.register()` rolls back internally. This is a migration concern only (Charter §5).
- **Pre-commit publication today.** For BAE-routed activities, `publish_event`/`record_audit` move to their correct side of the commit (C11/C12; `RO-M1-09`, M5).
- **Durable state (`RO-M1-07`).** The M5/M6 model must keep four concerns separate:
  - runtime/in-memory context (the immutable BACX, `§6.17`, not persisted as a Business Object, `§6.17.4`);
  - durable execution state (the current `§6.18.4` state + history, `§6.18.11`/`§6.18.12`);
  - transaction state (`§6.17.13`, `§6.19.4`);
  - terminal vs. non-terminal lifecycle classification (§11.2).
- **Idempotency.** Transaction Context carries an Idempotency Key (`§6.17.13`). `§6.20` is a dependency (§14.5 `D-01`). `§6.20.9`'s "Execution Registry" overlaps the durable state approved by `RO-M1-07`; M5/M6 must assess whether one model serves both, without assuming it.

### 11.2 State-transition inventory (`RO-M1-08`)

**Authoritatively supported (`§6.18.6` "Permitted examples", verbatim — 10):**
Created → Ready · Ready → Running · Running → Waiting · Waiting → Running · Running → Suspended · Suspended → Running · Running → Completed · Running → Failed · Running → Cancelled · Failed → Rolled Back.

**Not authoritatively supported — each an unresolved RO decision, DEFERRED → M5/M6.** None is permitted until decided.

| ID | Candidate transition | Why it arises | Source status |
|---|---|---|---|
| U-01 | Created → Failed / Created → Cancelled | Activity Resolution and registration-prerequisite failure occur before initialization completes (`§6.16.5`, C4) | Not listed in `§6.18.6`; not drawn in `§6.18.3` |
| U-02 | Ready → Failed / Ready → Cancelled | Whether Authorization Evaluation happens in `Ready` or `Running` is unspecified. A denial before `Running` needs an exit | Not listed; not drawn |
| U-03 | Waiting → Cancelled / Waiting → Failed | Cancelling or timing out while waiting (`§6.18.7`, `§6.18.10`) | Not listed |
| U-04 | Suspended → Cancelled / Suspended → Failed | Cancelling a paused activity (`§6.18.8`, `§6.18.10`) | Not listed |
| U-05 | Failed → Running (or Failed → Ready) | Domains may request "Retry" (`§6.18.5`); `§6.18.3` draws Failed merging back into Running | Drawn in `§6.18.3`, not listed in `§6.18.6` |
| U-06 | Completed → Rolled Back | Compensation after completion (`§6.18.11` "reversed through … compensation"; `§6.19.12`) | Drawn in `§6.18.3`, not listed |
| U-07 | Completed → Cancelled | Drawn in `§6.18.3` only | Drawn, not listed; no semantic source |
| U-08 | Running → Rolled Back (direct) | Pre-commit rollback (`§6.19.11`) — the listed path is Running → Failed → Rolled Back | Not listed |
| U-09 | Terminal classification of Completed and Failed | Cancelled and Rolled Back have no outbound transition in either source. Completed has one only in the diagram (U-06/U-07). Failed has a listed outbound transition | Needed for `RO-M1-07`'s terminal/non-terminal distinction |
| U-10 | `ESCALATED` / `DELEGATED` / `CONDITIONAL` authorization → `Waiting` | `RTA-001 §11.8` decisions that are neither allow nor deny | No mapping source; fail-closed until decided (C6) |

## 12. Module Placement

**Decided by `RO-M1-01`:** `Backend/Runtime/BusinessActivityEngine/`, executed in-process within the hosting service. **Not created.**

The comparison that supported it is retained for the record:

| Option | Evidence for | Evidence against |
|---|---|---|
| **P1 — `Backend/Runtime/BusinessActivityEngine/`, in-process** (**SELECTED**) | AuthorizationEngine precedent; `RTA-001 §3` Runtime component; domain independence (`§6.15.9`); only form that owns the hosting service's transaction without cross-service DB access; first consumers AuthService-hosted (ADR-036) | Not pip-installable; inherits the interim `sys.path` import pattern unless packaged; BAR lookup local only in AuthService (`RO-M1-11`, deferred) |
| P2 — embedded in AuthService | BAR and the real resolver are local | Contradicts `§6.15.9`/`§6.15.3`; unusable by other services |
| P3 — `Backend/Shared/` | Importable since Release A1 | Library layer, not Runtime Components; `TD-071` Open |
| P4 — standalone service | Clear process boundary | Cannot own another service's transaction; forces distributed transactions (`§6.19.9`); new service boundary |

## 13. Dependencies

| Dependency | Needed by | Status |
|---|---|---|
| BAR A–C read surface | M2 | Delivered; read-only *(C-4 annotation, 2026-09-28, `IRA-WP-23-AC §7` S-8: "Delivered" predated independent verification of WP-23 A–C; historical wording kept. The tranche is now accepted (`IRA-WP-23-AC §0.2`) and committed in `b0f5a12e84a9a3f7d9622bcbea4cee87b934be85`; not certified)* |
| WP-23 Workstream E gate mechanism/authority | M2 | **Not built** (WP-23 Charter §9). The BAE consumes it (`RO-M1-04`). The interface is designed in M2. Whether M2 can proceed against the raw BAR read surface before Workstream E exists is an M2 question |
| Governed manifest contract (CBAM instance or equivalent) | M2, M3, M4 | **None exists.** M2 defines the minimum contract (`RO-M1-03`) |
| `AuthorizationAdapter` / `EvaluationPipeline` | M4 | Delivered; consumed by WP-13; reusable unmodified |
| Real tier resolvers beyond Domain Permission | M4 (non-trivial BAs) | Only Domain Permission exists |
| Correlation mechanism | M3, M6 | Real, per service (AuthService `LoggingMiddleware`/`CorrelationContext`) |
| `AsyncSession` / repositories | M5 | Exists |
| **Event Bus** | M5 | **Absent** — dependency; no substitute (`RO-M1-10`) |
| **Audit Engine / authoritative persistent audit** | M5 | **Absent** — per-service structured log calls only; dependency recorded (`RO-M1-09`/`RO-M1-10`) |
| **Notification Engine** | M5 | **Absent** — C-132 is a capability, not a platform service |
| **Observability Platform** | M6 | **Absent** — log-based metrics only |
| **Metadata Engine / Workflow Engine / AI Runtime Engine** | M3, M6 | **Absent** |
| Durable execution-state persistence | M5/M6 | Approved in principle (`RO-M1-07`); model not designed |
| First real consumer BA and its hosting boundary | M7 | Not identified; triggers `RO-M1-11` |

## 14. Cross-Check Findings and Dispositions

### 14.1 Findings from the 2026-09-23 cross-check, with disposition

| ID | Finding (summary; full text in 2026-09-23 version) | Disposition |
|---|---|---|
| **X-01** | Four differing stage sequences (`IMP-001 §6.15.5`, `§6.16.3`, `RTA-001 §6.5` `[LOCKED]`, Charter §9/IRA §4) | **Disposed by `RO-M1-02`.** `§6.16.3` governs BAE order. `RTA-001 §6.5` correction identified (§14.3, `RC-01`). Charter §9 hybrid list noted (§14.3, `RC-04`), not corrected (outside `RO-M1-12`). Residual stage-membership item `R-01` (§14.4) |
| **X-02** | Manifest Resolution: BAR per `RTA-001 §3.6`/`§6.4` `[LOCKED]`; excluded by D2/D6; BAE per Charter | **Disposed by `RO-M1-03`** (BAE owns it at runtime). `RTA-001` corrections identified (`RC-02`, `RC-03`) |
| **X-03** | No source for identifier → implementation binding | **Ownership disposed by `RO-M1-03`**; contract **DEFERRED → M2** |
| **X-04** | `§6.16.5` verification fields absent from BAR; D6 addressed only `§6.22` | **Disposed by `RO-M1-05`** (minimum authoritative; per-datum source analysis in M2; BAR not expanded) |
| **X-05** | Execution gate claimed by both WP-23 Workstream E and BAE M2 | **Disposed by `RO-M1-04`** (Workstream E = BAR-side mechanism/authority; BAE = runtime consumer/enforcer) |
| **X-06** | Stale "no production consumer" claim (Charter, IRA, investigation, README, WP-RTA-001) | **Corrected under `RO-M1-12`** in the Charter, README, and WP-RTA-001 (§17). IRA-BAE-001 §6/§13 and the investigation §5/§6 carry the same claim but were not named in `RO-M1-12`, so they are left unchanged and recorded as a condition (§16). `CERT-WP-RTA-001` is a historical certification record and is correctly left unchanged |
| **X-07** | Charter §11 overstated existence of Event Bus / Audit Engine / Observability Platform | **Corrected under `RO-M1-12`** (Charter §11 and the §9 diagram; §17) |
| **X-08** | `§6.16.7` inputs vs `RTA-001 §11.5` context fields | No change; `RTA-001` field set governs the engine; governed request via resolver binding |
| **X-09** | Audit timing inconsistent within `IMP-001` | **Disposed by `RO-M1-09`** (distinction preserved; **DEFERRED → M5**) |
| **X-10** | Services roll back internally, contrary to `§6.19.3` | Migration concern only; Charter §5 |
| **X-11** | Durable history implies a new table | **Disposed by `RO-M1-07`** (approved in principle; **DEFERRED → M5/M6**) |
| **X-12** | `§6.18.3` diagram vs `§6.18.6` list | **Disposed by `RO-M1-08`** (method); inventory §11.2; **DEFERRED → M5/M6** |
| **X-13** | "18-part / 16-part" terminology | Not a stale *factual* statement of the kind `RO-M1-12` names. Left unchanged. This document uses the structural counts (ten sections, nine states). Noted for any future Charter maintenance |
| **X-14** | Charter range omits `§6.20`–`§6.29` | **Disposed by `RO-M1-06`**; dependencies §14.5 |
| **X-15** | M2 tenant-isolation expectation vs global BAR | Not a stale factual statement named in `RO-M1-12`. Left unchanged. §9 records where `§21.4` actually attaches |
| **X-16** | `§6.15.3` target vs D2 interim | Consistent; no action |

### 14.2 Repository Owner decisions

All twelve are recorded in §0. None remains unanswered. Items the Repository Owner explicitly assigned to later milestones are consolidated in §15.

### 14.3 `RTA-001` corrections identified (`RO-M1-02`/`RO-M1-03`) — NOT performed

`RTA-001` is LOCKED and was not modified. Per `CLAUDE.md §19` ("Architecture SHALL NOT evolve during implementation unless explicitly approved through the existing ADR process"), these corrections, and the `RO-M1-01`–`03` dispositions they reflect, should be formalized through an ADR before the later correction pass is applied (condition, §16).

| ID | Location | Current `[LOCKED]` text | Correction required to reflect §0 |
|---|---|---|---|
| **RC-01** | `RTA-001 §6.5` Runtime Execution Lifecycle | "Runtime Request │ Activity Discovery │ Manifest Resolution │ Business Activity Context │ Authorization │ Metadata Resolution │ Enterprise Context Resolution │ Business Rule Execution │ Business Object Persistence │ Transaction Commit │ Domain Event Publication │ Workflow Continuation │ Knowledge Graph Update │ Audit Recording │ Observability │ Response" | State that BAE execution order is governed by `IMP-001 §6.16.3` (`RO-M1-02`), or align the sequence to it. The alignment would need to: include Input Contract Validation and Business Validation after Authorization; include Notification Processing and AI Assistance Hooks; place Manifest Resolution within Activity Resolution and Enterprise Context resolution within Context Initialization; and record the disposition of Knowledge Graph Update (`R-01`) |
| **RC-02** | `RTA-001 §3.6` BAR primary responsibilities | "Activity discovery · Version resolution · **Manifest resolution** · Execution policy lookup · Dependency resolution · Registration governance" | Remove or re-qualify "Manifest resolution" as a runtime BAE responsibility (`RO-M1-03`). "Version resolution", "Execution policy lookup", and "Dependency resolution" also exceed D2's decided BAR scope and D6's reading of `IMP-001 §6.22`. Whether they are corrected in the same pass is for the Repository Owner (not decided here) |
| **RC-03** | `RTA-001 §6.4` Runtime Responsibilities table | "Manifest Resolution — Business Activity Registry" | "Manifest Resolution — Business Activity Engine" (`RO-M1-03`) |
| **RC-04** *(non-`RTA-001`, informational)* | WP-BAE-001 Charter §9 and IRA-BAE-001 §4 | A hybrid stage list attributed to `§6.16.3` that does not match it | Replace with the verbatim `§6.16.3` sequence (C7). Not performed: outside `RO-M1-12`'s three named statements |

### 14.4 Residual item after `RO-M1-02`

**R-01 — Knowledge Graph Update.**
- `RTA-001 §6.5` `[LOCKED]` includes a "Knowledge Graph Update" stage.
- `IMP-001 §6.16.3` has no counterpart. `§6.16.14` lists "Analytics Updates", not a knowledge-graph update. `§6.15.5` names the Knowledge Graph only as a resource below the engine.
- `RO-M1-02` settled *ordering* conflicts. Whether the BAE carries a post-commit Knowledge Graph Update obligation is a stage-*membership* question that `RO-M1-02` did not explicitly address.
- **This is part of `X-01` as originally reported, not a new conflict.** It does not affect M1: the skeleton enumerates `§6.16.3`'s sixteen stages.
- It is **DEFERRED → M5** (post-commit processing) as an unresolved RO sub-question. If left undecided, the BAE carries no Knowledge Graph Update stage, and that absence is disclosed. It is not silently added.

### 14.5 `IMP-001 §6.20`–`§6.29` — dependencies of Charter-included responsibilities (`RO-M1-06`)

Recorded as **dependencies only**. The Charter is not expanded. Each row names the Charter-included responsibility that already requires the later section.

| ID | `IMP-001` section | Charter-included responsibility that depends on it | Why mandatory | Milestone |
|---|---|---|---|---|
| **D-01** | `§6.20` Idempotency & Replay Protection | Transaction Management / Context (`§6.17.13` Transaction Context "Idempotency Key") | `§6.20.3` assigns idempotency management exclusively to the BAE; the in-scope context already carries the key | M3 (key), M5 |
| **D-02** | `§6.21` Compensation & Recovery | Transaction Management (`§6.19.12` Compensation Strategy, `§6.19.13` Recovery); State Model (`§6.18.11` Rolled Back via compensation, `§6.18.15` Recovery) | In-scope subsections defer the mechanism to "the Business Activity Contract" / compensation model | M5 |
| **D-03** | `§6.23` Versioning | Activity Resolution (`§6.16.5` "Activity Version") | Version verification is in-scope; the version model lives in `§6.23` (subject to `RO-M1-05`'s per-datum source analysis) | M2 |
| **D-04** | `§6.24` Composition | Transaction Management (`§6.19.8` Nested Business Activities); Context Propagation (`§6.17.17`) | Parent/child boundaries are in scope; composition semantics live in `§6.24` | M5 |
| **D-05** | `§6.27` Observability & Telemetry | Observability (`§6.15.4`); Transaction Observability (`§6.19.15`); State Monitoring (`§6.18.14`) | The Charter includes Observability; `§6.27` defines the canonical telemetry and correlation model (`§6.27.5`/`§6.27.6`) | M6 |
| **D-06** | `§6.28` Error Classification | Error Handling — "Apply canonical error management" (`§6.15.4`) | `§6.28.4`: "Error classification shall be mandatory" — the only definition of "canonical" error management | M6 |
| **D-07** | `§6.25` Execution Policies | Activity Context "Execution Mode" (`§6.17.6`); Recovery governed by "Retry Policy" / "Transaction Policy" (`§6.18.15`) | In-scope subsections consume policies defined in `§6.25` | M5/M6 |
| **D-08** | `§6.26` Performance, SLA & QoS | State Monitoring "SLA monitoring" (`§6.18.14`) | Monitoring of SLA only; SLA governance itself is not a Charter responsibility | M6 (monitoring only) |
| **D-09** | `§6.29` CBAM v2 (with `§6.14` CBAM, `§6.7` BAC) | Manifest Resolution (`RO-M1-03`); Input Validation (Input Contract); Authorization (Authorization Requirements); `§6.16.3` "optional by the Business Activity Contract" | `§6.29.3`: "The Business Activity Engine consumes the CBAM"; `§6.29.12` lists what the BAE determines from it. M2's minimum manifest contract must derive from this, not be invented | M2 |

## 15. M2–M7 Sequencing Implications and M2 Prerequisites

**M1 skeleton (not authorized).** When separately authorized, it is implementable at `Backend/Runtime/BusinessActivityEngine/` (`RO-M1-01`). It needs:
- a ten-section context model (`§6.17.5`);
- a nine-state enum (`§6.18.4`) with only the ten authoritative transitions (§11.2);
- a transaction-context shape (`§6.17.13`);
- the sixteen `§6.16.3` stages in canonical order (`RO-M1-02`), each reporting `NOT_IMPLEMENTED`;
- structural tests only.

No further decision is needed for the skeleton.

**M2 prerequisites** (each assigned to M2 by §0; M2's own `§19` checklist must address all of them before code):
1. **Minimum manifest contract** (`RO-M1-03`), derived from `IMP-001 §6.14`/`§6.29`/`§6.7` (`D-09`). Decide whether a new governed artifact is required, and how an identifier binds to executable code without scanning, decorators, or route discovery.
2. **Per-datum source analysis** (`RO-M1-05`) for Activity Version, Activity Status, Supported Invocation Method, Business Domain, and Required Platform Version (`§6.16.5`): the authoritative source, whether it exists, and whether a new manifest/metadata contract is required. BAR is not expanded. `D-03` for version.
3. **BAE ↔ Workstream E interface boundary** (`RO-M1-04`), including how M2 proceeds while Workstream E is unbuilt. WP-23 is not modified by M2 unless separately authorized.
4. **Per-BA authorization-policy source** (candidate: CBAM "Authorization Requirements"), as input to M4.
5. **Tenant-isolation placement** (`X-15`): confirm that the `§21.4` checklist applies at M3/M4 rather than to the global BAR lookup.

**Later milestones:**
- **M3:** Identity/Organization/Request/Runtime context are real. Enterprise/Workflow/AI context sections are `NOT_AVAILABLE` until their sources exist. Idempotency key (`D-01`).
- **M4:** technically ready (adapter reusable). Needs the per-BA binding source from M2. Fail-closed until U-10 is decided.
- **M5:** durable state model (`RO-M1-07`); audit timing (`RO-M1-09`); platform dependencies recorded, not substituted (`RO-M1-10`); `R-01`; `D-01`/`D-02`/`D-04`/`D-07`; transitions U-01–U-10 (`RO-M1-08`).
- **M6:** state model completion; `D-05`/`D-06`/`D-08`; AI hooks limited to `IMP-001`.
- **M7:** first-consumer selection triggers `RO-M1-11`. No candidate is selected here.

**Ordering observation (no change proposed):** M4 depends only on M1 and M3's Identity/Organization context. Any resequencing is the Repository Owner's decision.

## 16. M1 Conclusion and Readiness Statement

**Final status: M1 — COMPLETE WITH CONDITIONS.**

Basis:
- The runtime contract (§7) is coherent after the §0 dispositions. Every clause carries a contract statement or an explicit milestone assignment made by the Repository Owner.
- All twelve decision questions are answered (§0). No ownership question remains open.
- No genuinely new constitutional conflict was found in this revision. The one residual item (`R-01`, Knowledge Graph Update) was part of the originally reported `X-01`, does not affect M1, and is deferred to M5 with a stated non-fabrication default.

**Conditions:**
1. **ADR formalization.** `RO-M1-02` and `RO-M1-03` depart from LOCKED `RTA-001` text (`§6.5`; `§3.6`/`§6.4`), and `RO-M1-01` introduces a new Runtime Component location. Per `CLAUDE.md §19`, these should be formalized through the ADR process (`architecture/07-Decisions`). The `RTA-001` corrections RC-01–RC-03 should then be applied under that authority. Neither step was performed here, because this task authorized no additional governance document and no `RTA-001` edit.
2. **Residual stale statements outside `RO-M1-12`.** The "no production consumer" claim remains in `IRA-BAE-001` (§6 dependency table, §13) and in `BAR-WP23-WORKSTREAM-D-...-INVESTIGATION.md` (§5, §6). The hybrid stage list remains in Charter §9 / IRA §4 (`RC-04`). The Charter header/§10/§17 "No milestone has begun" wording predates this M1 analysis. A further narrow correction pass needs separate authorization.
3. **M1 skeleton implementation** requires separate Repository Owner authorization. It is not authorized by this document or by §0.
4. **M2 prerequisites** (§15, items 1–5) must be addressed in M2's own `CLAUDE.md §19` checklist before any M2 code.
5. **Deferred items** remain open and assigned: `RO-M1-07`/`08`/`09` (M5/M6), `R-01` (M5), U-01–U-10 (M5/M6), `RO-M1-11` (first-consumer selection).

**Integrity:**
- No BAE code, module directory, schema, migration, API, route, test, manifest, or execution-state table was created.
- No Business Activity was registered, and no identifier was assigned.
- Unaltered: BAR A–C, `BAR-INDEX.md`, the WP-23 Charter (Workstreams D and E), `IMP-001`, `RTA-001`, `IRA-BAE-001`, and C-024.
- The WP-BAE-001 Charter was changed only by the `RO-M1-12` factual corrections (§17). Its scope and milestones are unchanged.
- Nothing was staged, committed, or pushed.

## 17. `RO-M1-12` Documentation Correction Log (2026-09-24)

All corrections follow the repository's no-silent-fix convention: the original text is preserved struck through, followed by a dated *(Corrected … per `RO-M1-12`)* note. No scope, milestone, governance decision, design, or `IMP-001` requirement was altered.

| # | File | Exact location | Stale statement | Correction |
|---|---|---|---|---|
| 1 | `architecture/05-Implementation/WP-BAE-001_Business_Activity_Engine_Charter.md` | §8 AuthorizationEngine Relationship, final bullet | "Once built, this Engine would resolve `WP-RTA-001`'s … limitation that 'no Business Capability consumes this engine's decisions in production use'" | Records that WP-13 (commit `a180ca4`+) already invokes the engine at 7 call sites across 3 AuthService routers; WP-13 not yet certified per `WPR-001`; the BAE would be the first consumer *through the BAE* |
| 2 | same | §9 Target Runtime Flow diagram, "Platform Services" block | "… AI Runtime Engine — each existing, each coordinated with, none rebuilt by this Engine" | "coordinated with where they exist, none rebuilt by this Engine; see §11 for which exist today — corrected 2026-09-24, RO-M1-12" |
| 3 | same | §10 M4, "Outputs/deliverables" | "the first real consumer of `Backend/Runtime/AuthorizationEngine`'s own M4 adapter, resolving … 'no Business Capability consumes …' limitation as a byproduct" | "the first invocation … made **through the Business Activity Engine**"; notes the existing WP-13 consumer. Milestone objective, scope, dependencies, and exclusions unchanged |
| 4 | same | §11 Dependencies, "Already available", fourth bullet | "Existing platform services … independently verified to exist and already consumed directly by certified capabilities: Persistence Services, Event Bus, Audit Engine, Observability Platform." | Evidence-supported description: Persistence (real); correlation (real, per service); audit/events/metrics (log-based stand-ins: `observability.py`, `Shared/Logging.AuditLogger`, `Shared/Events.EventPublisher` without broker); absent as authoritative platform services: Event Bus, Audit Engine, Observability Platform, Notification Engine (C-132 is a capability), Metadata, Workflow, AI Runtime Engines |
| 5 | `Backend/Runtime/AuthorizationEngine/README.md` | Header `**Status:**` line | "Not committed. Not independently reviewed or certified. No Business Activity or WP-05 consumer wired." | Committed (`7fac19c`); CERTIFIED WITH CONDITIONS (`CERT-WP-RTA-001`; `WPR-001 §2a`); consumed by WP-13 (7 call sites / 3 routers; WP-13 not yet certified); no BAE consumer yet |
| 6 | same | "Known Limitations", second bullet | "No Business Activity or FastAPI endpoint consumes this runtime yet (`AuthorizationAdapter` has no real caller)." | One real caller, WP-13's `enforce_domain_permission`; only the Domain Permission tier bound; no caller through a BAE yet. **Documentation file only — no AuthorizationEngine code changed** |
| 7 | `architecture/05-Implementation/WP-RTA-001_Authorization_Runtime_Engine.md` | Header `**Status:**` line | "Not yet independently reviewed, certified, or committed — …" | Committed (`7fac19c`); CERTIFIED WITH CONDITIONS (`CERT-WP-RTA-001`; `WPR-001 §2a`) |
| 8 | same | §"Exit Criteria", third bullet | "… no Business Capability consumes this engine's decisions in production use." | Original **kept** (accurate at closure, preserved as the closure record). A dated factual-update note is appended recording the WP-13 consumer (and WP-13's uncertified status). **No exit criterion changed** |

---

*End of IRA-BAE-001-M1 (revised 2026-09-24). M1 — COMPLETE WITH CONDITIONS. This document records the Repository Owner's M1 Architectural Disposition and the RO-M1-12 correction pass. It authorizes no implementation.*
