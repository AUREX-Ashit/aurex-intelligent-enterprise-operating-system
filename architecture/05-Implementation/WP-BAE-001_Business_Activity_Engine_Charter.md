# WP-BAE-001 — Business Activity Engine

**Work Package ID:** WP-BAE-001
**Type:** Runtime (not a Business Capability Work Package)
**Parent Architecture:** `IMP-001 §6.15`–`§6.19` (Business Activity Engine, Execution Pipeline, Context Model, State Model, Transaction Management); `RTA-001 §3.5`/`§6.1`–`§6.6`/`§11.2`/`§11.5`/`§11.13`
**Capability:** None — a Runtime Component serves every Business Capability; it is not owned by one (mirrors `WP-RTA-001`'s own identical "Capability: None" determination, `IRA-RTA-001 §9`; confirmed identically for this Engine at `IRA-BAE-001 §9`)
**Status:** ~~CHARTER PREPARED. NOT YET REGISTERED in `WPR-001 §2a`.~~ *(Updated 2026-09-23 — Repository Owner approved this Charter for formal registration; registered in `WPR-001 §2a`.)* **CHARTER APPROVED — REGISTERED.** ~~Implementation NOT authorized. No milestone has begun, none is complete. No independent verification has occurred. No closure or certification has occurred.~~ *(Updated 2026-09-25 — WP-BAE-001 M1 accepted by the Repository Owner.)* **M1 ACCEPTED — COMPLETE** (independent review `IRA-BAE-001-M1_Independent_Review.md`; remediation verified by `IRA-BAE-001-M1_Remediation_Independent_Review.md`). **M2 NOT AUTHORIZED and NOT STARTED.** M3–M7 not started. The Business Activity Engine as a whole is not complete. Closure and certification of the Work Package have not occurred.
**Governing IRA:** `IRA-BAE-001_Business_Activity_Engine_Implementation_Readiness_Assessment.md`
**Governing Repository Owner Decisions:** (1) `BAR-WP23-WORKSTREAM-D-BUSINESS-ACTIVITY-ENGINE-PREREQUISITE-INVESTIGATION.md §0` — Option B, "Separate BA Engine Work Package," recorded 2026-09-23. (2) Direct Repository Owner approval of this Charter for formal `WPR-001 §2a` registration, recorded 2026-09-23 — see §17 below.
**This document defines Work Package scope and milestones only. No implementation, API, schema, migration, or test is created by this document.**

---

## 1. Purpose

Implement and operate the Business Activity Engine Runtime Component specified by `IMP-001 §6.15`–`§6.19`, so that Business Activities across every Business Capability execute through one canonical, platform-wide runtime path — resolving each Business Activity exclusively through the Enterprise Business Activity Registry (BAR), constructing its execution context, invoking centralized authorization, coordinating validation/metadata/workflow/persistence/transaction/event/audit/observability concerns, and returning a response — rather than each capability separately implementing this machinery, per `§6.15.3`'s own Platform Position: *"every executable operation... shall execute through the Business Activity Engine... No component shall bypass the engine."*

## 2. Governance / Authority Basis

| Authority | Role |
|---|---|
| `IMP-001 §6.15` | Names the Business Activity Engine as a "Core Platform Service" and states its mandatory Platform Position. |
| `IMP-001 §6.15.4` | The sixteen named architectural responsibilities this Charter's §6 restates as future scope. |
| `IMP-001 §6.16.3` | The sixteen-stage canonical execution pipeline. |
| `IMP-001 §6.17` | The eighteen-part Business Activity Context model. |
| `IMP-001 §6.18` | The sixteen-part canonical State Model. |
| `IMP-001 §6.19` | The sixteen-part Transaction Management model. |
| `IMP-001 §6.22.7`/`§6.22.15`/`§6.22.8` | The execution-time BAR gate and registry-exclusive discovery rule this Engine is the intended enforcement point for. |
| `RTA-001 §6.6` `[LOCKED]` | "Business Activities shall never be discovered through implementation-specific mechanisms." |
| `RTA-001 §11.2`/`§11.5`/`§11.13` `[LOCKED]` | Names this Engine as the constructor of `AuthorizationContext` and the invoker of the (separately built, separately owned) Authorization Engine. |
| `IMP-001 §13.6c` | A second, independent hard dependency: `AgentOrchestrator`'s own future work dispatches exclusively through this Engine's interface — "a hard dependency, not a convention." |
| `WP-RTA-001_Authorization_Runtime_Engine.md` | The direct procedural and structural precedent for chartering a cross-cutting Runtime Work Package; its own Responsibility Boundary table and Scope explicitly exclude Business Activity Engine construction, confirming no existing Work Package already covers this scope. |
| `IRA-RTA-001` | The first Runtime-Component IRA in this repository; `IRA-BAE-001` mirrors its structure directly. |
| `IRA-BAE-001_Business_Activity_Engine_Implementation_Readiness_Assessment.md` | The constitutional readiness assessment this Charter is built on — every scope, dependency, risk, and exclusion below traces to it. |
| `BAR-WP23-WORKSTREAM-D-BUSINESS-ACTIVITY-ENGINE-PREREQUISITE-INVESTIGATION.md §0`/`§2`–`§13` | First identified the gap; records the Repository Owner's Option B decision this Charter exists to act on. |
| `CLAUDE.md §18`/`§19.4`/`§19.7`/`§19.7b` | The STOP-and-report discipline this Charter satisfies, and the closure-gate sequence this Work Package will be subject to once implementation begins. |

## 3. Architectural Need

`IMP-001 §6.15`–`§6.19` specify a mandatory, platform-wide Business Activity Engine as the sole intended execution path for every Business Activity in this repository. No Work Package to date — including `WP-RTA-001`, whose own Charter explicitly excludes "anything belonging to a Business Capability's own Business Object or Business Activity lifecycle" — has built any part of it (`IRA-BAE-001 §4`, `§6`; investigation document §2–§7). Every certified Business Activity today executes via direct FastAPI routing, entirely outside this specification (investigation document §7) — a pre-existing, disclosed condition this Charter does not newly create and does not, by itself, resolve. WP-23 Workstream D's own objective (rewire Business Activity discovery to be BAR-exclusive) cannot be implemented without this Engine, or a functional equivalent, existing — the architectural need this Charter exists to address.

## 4. Scope

**In scope (future milestones only — see §10; nothing below is implemented by this document):** the Runtime Component itself, per `IMP-001 §6.15`–`§6.19` — Activity Resolution against BAR, Context Initialization/the 18-part Context model, Input Validation, Authorization Context construction and invocation of the existing Authorization Engine, Metadata Resolution, Workflow Coordination, Business Rule Execution (invoked, not owned), Persistence Coordination, the 16-part Transaction Management model, Post-Commit Processing, Response Generation, Event Publication, Notification Integration, Audit Recording, AI Assistance, Error Handling, and Observability — each coordinating with its own already-existing, separately-owned platform service where one exists, never rebuilt by this Engine.

**Out of scope:** see §5.

## 5. Explicit Exclusions

- Any Business Capability's own Business Object or Business Activity lifecycle, business rule authorship, or Business Object ownership — this Engine invokes and executes on each capability's own behalf; it never becomes their owner (`IRA-BAE-001 §7`/`§9`).
- `Backend/Runtime/AuthorizationEngine`'s own decision-evaluation logic (`WP-RTA-001`) — this Engine constructs the `AuthorizationContext` and invokes that engine; it never re-implements precedence evaluation (§8 below).
- `AgentOrchestrator`'s own construction (`IMP-001 §13.5`/`§13.6a`) — a separate, independently future-chartered concern; this Engine is a dependency `AgentOrchestrator` would consume, not a component that builds `AgentOrchestrator`.
- Enterprise BAR's own registration/identifier mechanism (`WP-23` Workstreams A–C, `bar_identifier_ledger`, `bar_registration`) — this Engine only queries BAR; it never owns, duplicates, or becomes a second discovery authority alongside it (§7 below).
- WP-23 Workstream D's own Charter text — not amended by this document. WP-23 Workstream D remains a future integration/dependency item; **creation of this Charter does not complete, unblock, or resolve WP-23 Workstream D.**
- Migrating any existing, already-certified Business Activity's execution path from direct FastAPI routing onto this Engine — each capability's own future, separately-scoped decision, never mandated in bulk by this Charter (mirrors `WP-RTA-001 §"Objectives" item 5`'s identical discipline).
- Any UI, frontend, or presentation-layer work.
- Registering this Work Package in `WPR-001 §2a` — not performed by this document (§17 below).
- Any implementation, code, API, schema, migration, or test of any kind — this document is a Charter only.

## 6. Runtime Responsibilities

Per `IMP-001 §6.15.4`, restated as this Work Package's own future scope (implementation deferred to the milestones in §10 — none delivered by this document):

| Responsibility | Runtime Capability |
|---|---|
| Business Activity Resolution (querying BAR exclusively) | Business Activity Engine |
| Context Initialization (18-part Context model, `§6.17`) | Business Activity Engine |
| Input Validation | Business Activity Engine |
| Authorization Context Construction | Business Activity Engine (constructs); invokes, never re-implements, the Authorization Engine's own evaluation (`RTA-001 §11.5`/`§11.13`) |
| Metadata Resolution | Business Activity Engine, coordinating with the Metadata Engine (`RTA-001 §3`) |
| Workflow Coordination | Business Activity Engine, coordinating with the Workflow Engine |
| Business Rule Execution | Business Activity Engine, invoking each capability's own owned business rules — never authoring them |
| Persistence Coordination | Business Activity Engine, coordinating with Persistence Services |
| Transaction Management (16-part model, `§6.19`) | Business Activity Engine |
| Post-Commit Processing / Response Generation | Business Activity Engine |
| Event Publication | Business Activity Engine, coordinating with the Event Bus |
| Notification Integration | Business Activity Engine, coordinating with the Notification Engine |
| Audit Recording | Business Activity Engine, coordinating with the Audit Engine |
| AI Assistance | Business Activity Engine, coordinating with the AI Runtime Engine, where `IMP-001` names this as in-scope |
| Error Handling / Observability | Business Activity Engine, coordinating with the Observability Platform |
| Runtime State Model (16-part, `§6.18`) | Business Activity Engine |

## 7. BAR Relationship

- Enterprise BAR (`WP-23`) is the canonical Business Activity registration authority and the canonical Business Activity Identifier authority (D2, D5) — unaffected and unaltered by this Charter.
- Business Activity discovery must ultimately be BAR-exclusive, per `IMP-001 §6.22.8` and `RTA-001 §6.6` `[LOCKED]` — this Engine, once built, is the intended enforcement point of that already-decided rule; this Charter does not create or amend the rule itself.
- `WP-23` Workstreams A–C already provide the BAR-side registration and identity mechanism (`bar_identifier_ledger`, `bar_registration`, and their repository/service query surface) this Engine's own future Activity Resolution responsibility would consume (`IRA-BAE-001 §6`/§9 finding).
- This Engine, once built, will consume BAR for Business Activity resolution/discovery — it will query BAR's existing surface; it will not duplicate, extend, or bypass it.
- WP-23 Workstream D remains a future dependency/integration item for this Engine, not the reverse — **this Charter's creation does not complete WP-23 Workstream D.** Workstream D remains exactly where its own STOP and the subsequent investigation left it: deferred, pending this future Work Package's own eventual completion.
- BAR's own decided scope (D1–D9, `ROD-ENTERPRISE-BAR-Decision-Preparation.md`) is not altered, referenced for amendment, or reopened anywhere in this document.

## 8. AuthorizationEngine Relationship

The existing, already-certified relationship is preserved exactly as `RTA-001`/`WP-RTA-001` define it and is not altered by this Charter:

```
Business Activity Engine   (this Charter — WP-BAE-001, future)
        │  constructs AuthorizationContext (RTA-001 §11.5)
        ▼
Authorization Engine       (WP-RTA-001, already delivered, CERTIFIED WITH CONDITIONS)
        │  evaluates URA-001-76's five-tier precedence chain
        ▼
Authorization Decision     (RTA-001 §11.8: Allow / Deny / Conditional / Delegated / Escalated)
```

- The Business Activity Engine is **not** the Authorization Engine, and this Charter does not make it one. `Backend/Runtime/AuthorizationEngine` remains its own, separately chartered and already-certified component.
- This Charter does **not** absorb, re-scope, or extend `WP-RTA-001`'s own existing authority. Authorization precedence evaluation (`URA-001-76`'s five tiers), decision generation, and Runtime Trace generation remain exclusively `WP-RTA-001`'s own delivered responsibility.
- Per `WP-RTA-001`'s own Responsibility Boundary table, Authorization Context Construction is already documented as "Business Activity Engine (consumed by, not performed by, this Work Package)" — this Charter is that documented future counterpart; it does not introduce a new relationship, it fulfills one `WP-RTA-001` already disclosed as pending.
- ~~Once built, this Engine would resolve `WP-RTA-001`'s own disclosed, accepted limitation that "no Business Capability consumes this engine's decisions in production use" (`IRA-RTA-001 §15`) — but that resolution is a future milestone-level fact (§10 below), not something this Charter itself achieves or claims.~~ *(Corrected 2026-09-24, per `RO-M1-12`, factual correction only — `IRA-BAE-001-M1 §14`, `X-06`.)* That `WP-RTA-001` limitation is no longer current: `WP-13` (Authorization Runtime Integration, commit `a180ca4` and successors) already invokes the Authorization Engine from committed AuthService code — `dependencies.py::enforce_domain_permission`, via `AuthorizationAdapter` → `EvaluationPipeline` → `AuthorizationEngine`, at 7 call sites across 3 routers (`approval_authority.py`, `delegation_policy.py`, `domain_permission.py`). `WP-13` itself is recorded in `WPR-001` as not yet certified. This Engine, once built, would be the first consumer that reaches the Authorization Engine **through the Business Activity Engine**, not its first consumer.

## 9. Target Runtime Flow

Per `IMP-001 §6.16.3`'s sixteen-stage canonical execution pipeline, restated at Charter level (no implementation detail; milestone-level design is deferred to §10):

```
Business Capability
        │  owns its own Business Objects and Business Activities
        ▼
Business Activity Invocation
        │  (a request to execute a specific, BAR-registered Business Activity)
        ▼
Business Activity Engine   (this Charter, future)
        │  Activity Resolution (query BAR — exclusive discovery)
        │  → Manifest Resolution → Context Construction (18-part Context model)
        │  → Authorization (construct AuthorizationContext, invoke Authorization Engine)
        │  → Validation → Metadata Resolution → Workflow Resolution
        │  → Business Rule Execution (capability-owned, invoked not owned)
        │  → Persistence Coordination → Transaction Management
        │  → Post-Commit Processing → Response Generation
        ▼
Enterprise BAR              (WP-23, already delivered — queried, never owned or duplicated)
        │  [C-4 note 2026-09-28, IRA-WP-23-AC §7 S-4: "already delivered" predated
        │   verification; WP-23 A–C accepted and committed b0f5a12 (not certified;
        │   WP-23 OPEN, D–H not implemented)]
        │  registration/identity lookup only
        ▼
Authorization Engine        (WP-RTA-001, already delivered — invoked, never re-implemented)
        │  returns one Authorization Decision + Runtime Trace
        ▼
Platform Services           (Persistence, Event Bus, Audit Engine, Observability Platform,
        │                    Notification Engine, AI Runtime Engine — coordinated with
        │                    where they exist, none rebuilt by this Engine; see §11 for
        │                    which exist today — corrected 2026-09-24, RO-M1-12)
        ▼
Response to Business Capability
```

This flow is descriptive of the target state `IMP-001 §6.15`–`§6.19` specify; it is not implemented, wired, or tested by this document.

## 10. Milestones / Workstreams

No milestone below is authorized to begin by this document (§17). No dates are stated. Each milestone requires its own future, separately-scoped `CLAUDE.md §19` gap analysis before any code is written — mirroring `WP-RTA-001`'s own identical discipline (its Deliverables table: "This charter accepted" as M1's own precondition, never implementation authorization by the Charter itself).

**M1 — Runtime Contract / Architecture Baseline**
- *Objective:* Establish the Engine's own stable module boundary, its skeleton pipeline structure (`§6.16.3`'s sixteen named stages, each honestly stubbed/reported rather than fabricated), and the `BusinessActivityContext`/`BusinessActivityState`/`BusinessActivityTransaction` model shapes (`§6.17`–`§6.19`), with no concrete stage logic and no consumer wired.
- *Major scope:* Module/package placement decision (deferred design question per `IRA-BAE-001 §11`); context/state/transaction model skeletons; pipeline stage skeleton, each stage honestly reporting `NOT_IMPLEMENTED` rather than a fabricated result.
- *Outputs/deliverables:* The Engine's own foundational module structure and model definitions; no live invocation path.
- *Dependencies:* This Charter accepted; `IRA-BAE-001` accepted.
- *Verification expectations:* Structural tests only (model shape, pipeline stage enumeration) — no behavioral claim, no fabricated tier/stage result, mirroring `WP-RTA-001 M1`'s own "every tier honestly reported... never a fabricated match" discipline.
- *Explicit exclusions:* No BAR query, no Authorization invocation, no persistence, no real consumer.
- *Repository Owner disposition (recorded 2026-09-25; F-01 of `IRA-BAE-001-M1_Independent_Review.md`). The text above is preserved as originally chartered.*
  - The later, explicit M1 implementation authorization (2026-09-24) authorized the M1 skeleton to include a **read-only BAR registration boundary/check** and **invocation of the existing AuthorizationEngine boundary**.
  - It supersedes the two exclusions "No BAR query" and "no Authorization invocation" **only for that narrow M1 skeleton boundary**.
  - It does **not** authorize a concrete BAR adapter; BAR registration; Business Activity Identifier issuance; Workstream E execution gating; manifest implementation; discovery; host-service integration; capability implementation; durable execution state; any M2 work; or any M3/M4/M5/M6 work beyond what the M1 skeleton explicitly required.
  - The divergence is classified as a documentation/governance-record inconsistency, not an implementation governance violation.
  - The authorization text is recorded in `IMP-REPORT-WP-BAE-001 §"Repository Owner Disposition — F-01"`.
  - No milestone scope is otherwise amended by this note.

**M2 — Business Activity Resolution & BAR Integration**
- *Objective:* Implement Activity Resolution (`§6.15.4`) as a real, structurally complete query against BAR's own existing, delivered surface (`BarRegistrationRepository.get_by_identifier`/`get_by_work_package_and_reference`) — the one responsibility already having a real, reusable dependency (`IRA-BAE-001 §16`). *(C-4 annotation, 2026-09-28, `IRA-WP-23-AC §7` S-5, first clause only: "existing, delivered surface" predated independent verification of WP-23 A–C. The tranche is now accepted (`IRA-WP-23-AC §0.2`) and committed in `b0f5a12e84a9a3f7d9622bcbea4cee87b934be85`; not certified. The M2-scope point about `get_by_work_package_and_reference` (S-5 second clause, group G-C) is intentionally not addressed here and stays for M2 authorization.)*
- *Major scope:* Manifest Resolution; enforcement of the already-decided execution-time BAR gate (D2/D8) and registry-exclusive discovery rule (`IMP-001 §6.22.8`/`RTA-001 §6.6`).
- *Outputs/deliverables:* A real, tested Activity Resolution stage consuming BAR read-only.
- *Dependencies:* M1; BAR (`WP-23` Workstreams A–C, already delivered) — read-only, no BAR schema change. *(C-4 annotation, 2026-09-28, S-3: "already delivered" predated independent verification. WP-23 A–C are now accepted (`IRA-WP-23-AC §0.2`) and committed in `b0f5a12e84a9a3f7d9622bcbea4cee87b934be85`; not certified. M2 remains NOT AUTHORIZED and NOT STARTED.)*
- *Verification expectations:* Tenant-isolation and gate-enforcement tests per `CLAUDE.md §21.4`'s Mandatory Tenant-Isolation Test Checklist, applied fresh at this milestone; no fabricated resolution for an unregistered Business Activity.
- *Explicit exclusions:* No write to BAR; no change to BAR's own schema, service, or repository code.

**M3 — Context Construction & Execution Pipeline**
- *Objective:* Implement Context Initialization (the full 18-part Context model, `§6.17`) and the remaining structural pipeline stages (Validation, Metadata Resolution, Workflow Resolution) as real, tested logic.
- *Major scope:* `§6.17`'s Activity/Identity/Organization/Enterprise/Authorization/Workflow/Request/Transaction/AI/Runtime Context sub-models, immutability and propagation rules; Input Validation against each Business Activity's own declared contract.
- *Outputs/deliverables:* A real, immutable Context object per invocation; real Validation/Metadata/Workflow pipeline stages.
- *Dependencies:* M1, M2.
- *Verification expectations:* Context immutability tests; contract-violation rejection tests.
- *Explicit exclusions:* No Authorization Context construction yet (M4); no Business Rule Execution yet.

**M4 — Authorization Integration**
- *Objective:* Implement Authorization Context construction (`RTA-001 §11.5`) and invocation of the existing, already-certified Authorization Engine (`RTA-001 §11.13`) — never re-implementing its evaluation logic (§8 above).
- *Major scope:* `AuthorizationContext` assembly from the M3 Context; invocation of `Backend/Runtime/AuthorizationEngine`'s own existing adapter interface (`WP-RTA-001` M4, "the stable interface a future Business Activity depends on"); consumption of the returned Authorization Decision.
- *Outputs/deliverables:* ~~A real, tested Authorization stage; the first real consumer of `Backend/Runtime/AuthorizationEngine`'s own M4 adapter, resolving `WP-RTA-001`'s own disclosed "no Business Capability consumes this engine's decisions in production use" limitation as a byproduct — not this milestone's own stated objective, disclosed as an effect, not claimed prematurely.~~ *(Corrected 2026-09-24, per `RO-M1-12`, factual correction only — `IRA-BAE-001-M1 §14`, `X-06`.)* A real, tested Authorization stage — the first invocation of `Backend/Runtime/AuthorizationEngine`'s own M4 adapter **made through the Business Activity Engine**. The adapter already has a committed consumer outside this Engine (`WP-13`'s `enforce_domain_permission`, 7 call sites across 3 AuthService routers; see §8).
- *Dependencies:* M1–M3; `Backend/Runtime/AuthorizationEngine` (`WP-RTA-001`, already delivered — consumed read-only, never modified).
- *Verification expectations:* No fabricated `ALLOW`; every decision traceable to a real Authorization Engine invocation and Runtime Trace.
- *Explicit exclusions:* No modification to `Backend/Runtime/AuthorizationEngine`'s own code; no re-implementation of precedence evaluation.

**M5 — Execution, Transaction, Persistence, Event & Audit Integration**
- *Objective:* Implement Business Rule Execution invocation, Persistence Coordination, the 16-part Transaction Management model (`§6.19`), Post-Commit Processing, Event Publication, and Audit Recording — each coordinating with its own existing platform service.
- *Major scope:* Transaction lifecycle/scope/atomicity/isolation (per `§6.19`'s subsections); coordination with Persistence Services, the Event Bus, and the Audit Engine — none rebuilt by this Engine.
- *Outputs/deliverables:* A real, tested end-to-end pipeline capable of executing a Business Activity's own business rules within a managed transaction, publishing events, and recording audit entries.
- *Dependencies:* M1–M4.
- *Verification expectations:* Transaction atomicity/rollback tests; audit-completeness tests; no direct database or event-bus access bypassing the coordinated path.
- *Explicit exclusions:* No new Business Object; no new capability-owned business rule authored by this Engine.

**M6 — Response Generation, Error Handling, Observability & AI Assistance**
- *Objective:* Implement Response Generation, Error Handling, the 16-part State Model (`§6.18`), Observability integration, and AI Assistance where `IMP-001` names it as this Engine's own responsibility.
- *Major scope:* Canonical states/transitions (Waiting/Suspended/Failed/Cancelled/Rolled-Back, per `§6.18`); Observability Platform integration (telemetry, per the same discipline `WP-RTA-001 M5`'s `RuntimeObservabilityCollector` already demonstrated for the Authorization Engine); AI Assistance integration, scoped only to what `IMP-001` explicitly names.
- *Outputs/deliverables:* Full State Model implementation; observable, traceable execution; documented AI Assistance touchpoints, if and only if explicitly named in `IMP-001`.
- *Dependencies:* M1–M5.
- *Verification expectations:* State-transition completeness tests; no fabricated state; Observability output verified against `IMP-001`'s own named telemetry set.
- *Explicit exclusions:* No AI capability invented beyond what `IMP-001` explicitly specifies for this Engine.

**M7 — Integrated Verification & Production Readiness**
- *Objective:* End-to-end verification of the full pipeline (M1–M6) against at least one real, willing Business Capability's Business Activity (mirroring `WP-RTA-001`'s own Acceptance Criteria requiring "at least one real Business Capability's Business Activity gates through this engine"), plus contract-stability, performance, and concurrency validation mirroring `WP-RTA-001 M6`'s own discipline.
- *Major scope:* First real consumer integration; Runtime Contract Verification; Performance Validation; Concurrency/Thread-Safety Validation; full documentation synchronization; Work Package closure per `CLAUDE.md §19.7b`'s five-gate sequence.
- *Outputs/deliverables:* At least one certified Business Activity actually executing through this Engine end-to-end; the Implementation Report and Closure Report.
- *Dependencies:* M1–M6; identification of at least one real, willing Business Capability to migrate onto this Engine (`IRA-BAE-001 §6`'s own disclosed open dependency — not yet identified).
- *Verification expectations:* Independent Certification, Verification & Validation Audit, and Release Readiness Audit per `CLAUDE.md §19.7b`, in full.
- *Explicit exclusions:* Bulk migration of every existing certified Business Activity onto this Engine — remains each capability's own future, separately-scoped decision (§5 above).

~~No milestone above is marked complete. No milestone has begun.~~ *(Updated 2026-09-25 — WP-BAE-001 M1 accepted by the Repository Owner.)* M1 is ACCEPTED and COMPLETE (`IMP-REPORT-WP-BAE-001`). M2–M7 are not authorized and not started.

## 11. Dependencies

**Already available (delivered, certified, reusable as-is):**
- ~~Enterprise BAR (`WP-23` Workstreams A–C) — `bar_identifier_ledger`, `bar_registration`, and their repository/service query surface. No BAR schema change is anticipated by this Charter.~~ *(C-4 correction, 2026-09-28, `IRA-WP-23-AC §7` S-12: this bullet wrongly sat under "delivered, certified". The item is restated below as a dated note. The heading and the Authorization Engine bullet are unchanged.)*
- *(C-4 note, 2026-09-28.)* Enterprise BAR (`WP-23` Workstreams A–C) — `bar_identifier_ledger`, `bar_registration`, and their repository/service query surface. It is implemented, independently verified (Gates 1–5) and **accepted** (`IRA-WP-23-AC §0.2`), committed in `b0f5a12e84a9a3f7d9622bcbea4cee87b934be85`. It is **not certified**, and WP-23 remains OPEN (Workstreams D–H not implemented). No BAR schema change is anticipated by this Charter.
- `Backend/Runtime/AuthorizationEngine` (`WP-RTA-001`) — M1–M6 delivered, `CERTIFIED WITH CONDITIONS`; its own M4 adapter interface is the intended integration point for future M4 (§10 above).
- `IMP-001 §6.15`–`§6.19`, `RTA-001 §6.6`/`§11.2`/`§11.5`/`§11.13` — the governing specifications, Active/LOCKED.
- ~~Existing platform services this Engine would coordinate with, where independently verified to exist and already consumed directly by certified capabilities: Persistence Services, Event Bus, Audit Engine, Observability Platform.~~ *(Corrected 2026-09-24, per `RO-M1-12`, factual correction only — `IRA-BAE-001-M1 §4`/`§14`, `X-07`.)* Existing mechanisms this Engine could coordinate with, as they actually exist today:
  - **Persistence:** real. The per-service `AsyncSession` (`DatabaseSessionManager.get_session`) and repositories (`BaseRepository`).
  - **Correlation:** real, per service. `LoggingMiddleware` assigns or propagates `X-Correlation-ID` into `CorrelationContext`.
  - **Audit, events and metrics:** log-based stand-ins only. AuthService's `observability.py` (`record_audit`/`publish_event`/`record_metric`) describes itself as an "explicitly temporary local substitute". `Backend/Shared/Logging.AuditLogger` is also log-based. `Backend/Shared/Events.EventPublisher` is an abstraction whose Kafka publisher carries no broker client.
  - **Absent as authoritative platform services:** no Event Bus, Audit Engine, or Observability Platform exists. Likewise no Notification Engine (C-132 notification is a capability-owned Business Object, not a platform service), no Metadata Engine, no Workflow Engine, and no AI Runtime Engine.

**Future / external (not yet implemented; require their own governed increment):**
- At least one real, willing Business Capability to migrate its execution path onto this Engine once built (`IRA-BAE-001 §6`'s own disclosed open dependency — not identified by this Charter).
- `AgentOrchestrator` (`IMP-001 §13.5`/`§13.6a`) — unbuilt; a future consumer of this Engine, not a dependency this Engine requires to exist first.
- Any precedence-tier data-model gaps `WP-RTA-001`'s own IRA already disclosed (Group/Named-User-Assignment, Approval-Authority holder/membership linkage) — these remain `WP-RTA-001`'s own, or another future capability's own, disclosed gaps; this Charter does not newly depend on them and does not charter closing them.
- A future WP-23 Charter amendment to Workstream D, re-scoping it to integration once this Engine exists — disclosed as following, not preceding, this Charter's own eventual implementation (mirrors the investigation document's own §10 Option B disclosure).

No advisory dependency above is treated as mandatory beyond what `IRA-BAE-001` or the investigation document already states.

## 12. Inputs / Outputs / Interfaces

**Input (future, per `§6.16.3`/`§6.17`):** a Business Activity invocation request, identifying the target Business Activity (by its BAR-issued `BA-NNNNNN` identifier or equivalent reference), Identity, Organization, and Request context. Assembled into an immutable Business Activity Context (18 parts, `§6.17`) — this Engine constructs it; it is not supplied pre-built by the caller.

**Output (future, per `§6.16.3`):** a Response object (Response Generation stage) plus the applicable Runtime State (per `§6.18`) and Transaction outcome (per `§6.19`); where authorization was evaluated, the Authorization Decision and Runtime Trace the Authorization Engine returned (consumed, not re-generated, by this Engine).

**Collaboration (future, per `§6.15.4`, mirroring `WP-RTA-001 §"Interfaces"`'s own "Collaboration" discipline):** Enterprise BAR (Activity Resolution, read-only), `Backend/Runtime/AuthorizationEngine` (Authorization invocation), Metadata Engine, Workflow Engine, Persistence Services, Event Bus, Audit Engine, Observability Platform, Notification Engine, AI Runtime Engine — each an existing or separately-owned collaborator, none rebuilt by this Engine.

No interface above is implemented, exposed, or callable as a result of this Charter.

## 13. Verification and Gate Model

Once implementation begins (not authorized by this document), this Work Package is subject to the full `CLAUDE.md §19.7`/`§19.7b` closure-gate sequence, identical in kind to `WP-RTA-001`'s own:
- Each milestone (§10) requires its own `CLAUDE.md §19` Implementation Start Checklist (Gap Analysis, Architectural Impact Assessment) before code is written.
- `CLAUDE.md §19.7`'s Business Activity Completion Gate applies per milestone, mirroring how `WP-RTA-001`'s own milestone table gated M1 through M6 individually.
- Work Package closure requires the full five-gate sequence: Independent Certification, Verification & Validation Audit, Remediation (if needed), Independent Verification of Remediation (if remediation occurred), and Release Readiness Audit — each performed by a reviewer independent of every gate before it, per `CLAUDE.md §19.7b`.
- `CLAUDE.md §19.8.5`'s prohibition on deferring a false-`ALLOW`/security defect as ordinary Technical Debt applies with particular force to M4 (Authorization Integration) — mirrors `WP-RTA-001`'s own identical, already-accepted discipline.
- `CLAUDE.md §21.4`'s Mandatory Tenant-Isolation Test Checklist applies to M2 (BAR-backed Activity Resolution) and any other future milestone whose data model carries an organization/tenant boundary.

None of these gates has been entered. This Charter document is not itself subject to `§19.7b` (it authorizes no implementation); it records that the future Work Package will be, once chartered work begins.

## 14. Risks / Open Issues

Carried forward from `IRA-BAE-001 §12` (not re-derived, not newly invented):

| Risk | Description | Disposition |
|---|---|---|
| Scale risk | Governing specification (16 responsibilities, 16-stage pipeline, 18-part context model, two further 16-part models) is comparable to or larger than `RTA-001 §11`'s own narrower specification, which itself required six milestones | Charter scopes seven milestones (§10); no single-pass delivery assumed |
| Scope-creep into existing certified components | Temptation to satisfy WP-23 Workstream D faster by expanding `AuthorizationEngine`'s or `AgentOrchestrator`'s own scope instead of building a genuinely separate Engine | Explicitly foreclosed by §8/§5 above and by the underlying Repository Owner decision text |
| Migration risk | Adoption by existing certified Business Activities is a cross-cutting change touching already-certified code | Explicitly out of scope (§5); each capability's own future, separately-scoped decision |
| Indefinite deferral risk | Nothing compels this Work Package to actually be registered or implemented on any timeline | Disclosed, not resolved — WP-23 Workstream D remains formally deferred until implementation actually proceeds |
| No identified first consumer | `IRA-BAE-001 §6`'s own final dependency row — no real Business Capability has yet committed to migrating onto this Engine | Carried as an open dependency for M7 (§10); not resolved by this Charter |
| False-progress risk | A future reader could mistake this Charter's existence for WP-23 Workstream D being unblocked, or for any milestone having begun | This document explicitly states (header Status, §5, §17) that nothing is implemented, registered, or authorized by it |

## 15. Deliverables

This Charter itself delivers exactly one artifact: this document. No milestone deliverable listed in §10 is produced by this Charter. Future deliverables, once implementation is separately authorized, are as enumerated per-milestone in §10 (context/pipeline skeleton; BAR-integrated Activity Resolution; full Context Construction; Authorization integration; transaction/persistence/event/audit integration; state/observability/AI Assistance integration; integrated verification and closure artifacts).

## 16. Completion / Closure Criteria

This Charter is complete when accepted by the Repository Owner for the purpose of enabling future `WPR-001 §2a` registration (§17). The Work Package it charters is complete only when, per `CLAUDE.md §19.7b`, every milestone in §10 has been implemented, independently certified, V&V-audited, remediated where required (with independent verification of that remediation), and passed a Release Readiness Audit — mirroring `WP-RTA-001`'s own Exit Criteria discipline. At minimum, closure requires:
- All seven milestones (§10) implemented and independently reviewed and certified.
- At least one real Business Capability's Business Activity gating through this Engine end-to-end (mirrors `WP-RTA-001`'s own identical Acceptance Criterion).
- No tier, stage, or decision ever fabricated (`CLAUDE.md §19.8.5`).
- WP-23 Workstream D's own Charter formally re-scoped to integration (a distinct, later act — not performed by this Charter, see §5/§7 above) as part of, or immediately following, this Work Package's own closure.

None of the above has occurred. This Charter records the boundary; it does not satisfy it.

## 17. Approval / Registration Status

- Repository Owner decision for a separate Business Activity Engine Work Package: **RECORDED** (`BAR-WP23-WORKSTREAM-D-BUSINESS-ACTIVITY-ENGINE-PREREQUISITE-INVESTIGATION.md §0`, Option B).
- Governing Implementation Readiness Assessment: **PREPARED AND EXISTING** (`IRA-BAE-001`).
- This Charter: ~~**PREPARED**, pending Repository Owner review/approval.~~ *(Updated 2026-09-23.)* **APPROVED** by direct Repository Owner decision for formal `WPR-001 §2a` registration.
- `WP-BAE-001` registration in `WPR-001 §2a`: ~~**NOT YET REGISTERED.** This document does not perform that registration.~~ *(Updated 2026-09-23.)* **REGISTERED** — see `WPR-001_Work_Package_Roadmap.md §2a`. **Charter approval and registration authorize this Work Package's own constitutional existence only — they do NOT authorize implementation of M1 or any other milestone.**
- Implementation authorization: ~~**NOT YET GRANTED.**~~ *(Updated 2026-09-25 — WP-BAE-001 M1 accepted by the Repository Owner.)* Granted for **M1 only** (the M1 skeleton authorization of 2026-09-24; see the §10 M1 disposition note). **Not granted for M2–M7.** No milestone in §10 may begin under this Charter or this registration alone.
- Milestone status: ~~**No milestone has passed. No milestone has begun.**~~ *(Updated 2026-09-25 — WP-BAE-001 M1 accepted by the Repository Owner.)* **M1 ACCEPTED — COMPLETE.** M2–M7 not started.
- Independent verification (Certification, V&V Audit, Release Readiness Audit, per `CLAUDE.md §19.7b`): ~~**NOT PERFORMED** — none applies yet, as no implementation exists.~~ *(Updated 2026-09-25 — WP-BAE-001 M1 accepted by the Repository Owner.)* M1 was independently reviewed (`IRA-BAE-001-M1_Independent_Review.md`, PASS WITH CONDITIONS), and its remediation was independently verified (`IRA-BAE-001-M1_Remediation_Independent_Review.md`, VERIFIED), per the `§19.7` milestone gate. The Work Package–level `§19.7b` closure gates have **not** been performed.
- Closure/certification of this Work Package: **NOT PERFORMED.**
- WP-23 Workstream D: **remains dependent on this future Work Package; unaffected and unresolved by this Charter's own preparation.**
- BAR D1–D9 and WP-23 Workstreams A–C: **unaltered.**
- Zero real Business Activities registered in BAR as a result of this document; C-024 BA-01 remains unregistered; `BAR-INDEX.md` remains unchanged.

## 18. References

`IMP-001_Implementation_Playbook.md §6.15`–`§6.19` (Business Activity Engine, Execution Pipeline, Context, State Model, Transaction Management — Active); `§13.5`/`§13.6a`–`§13.6c` (`AgentOrchestrator` — specified, unbuilt); `§6.22` (Business Activity Registry — Active, governing D1–D9); `RTA-001 §3.5`/`§6.1`–`§6.6`/`§11.2`/`§11.5`/`§11.13` (LOCKED); `WP-RTA-001_Authorization_Runtime_Engine.md` (Charter, procedural precedent); `IRA-RTA-001_Authorization_Runtime_Engine_Implementation_Readiness_Assessment.md` (structural precedent); `IRA-BAE-001_Business_Activity_Engine_Implementation_Readiness_Assessment.md` (this Charter's own direct governing input); `BAR-WP23-WORKSTREAM-D-BUSINESS-ACTIVITY-ENGINE-PREREQUISITE-INVESTIGATION.md` (§0, §2–§13 — the Repository Owner decision and its underlying evidence); `WP-23_Enterprise_BAR_Mechanism_Implementation_Charter.md §8` (Workstream D's own original text); `ROD-ENTERPRISE-BAR-Decision-Preparation.md` (D1–D9, unaltered); `WPR-001_Work_Package_Roadmap.md §2a` (the future registration point, not performed here); `CLAUDE.md §18`/`§19`/`§19.7`/`§19.7b`/`§21.4`.

---

*End of WP-BAE-001. This document defines Work Package scope and milestones only. No implementation, API, schema, migration, or test is created by this document. `WP-BAE-001` is registered in `WPR-001 §2a` (2026-09-23, per direct Repository Owner approval) — registration authorizes this Work Package's constitutional existence only. Implementation is not authorized. WP-23 Workstream D remains dependent on this future Work Package, unresolved by this Charter's own preparation. D1–D9 and WP-23 Workstreams A–C are unaltered. No Business Activity was registered. C-024 BA-01 remains unregistered. `BAR-INDEX.md` is unchanged. Nothing staged, committed, or pushed.*
