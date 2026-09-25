# WP-23 Workstream D — Business Activity Engine Prerequisite Investigation

**Document type:** Architectural investigation / Repository Owner decision-preparation record — presents evidence and options; **selects nothing**. Same class as `BAR_ENTERPRISE_MECHANISM_DECISION_INVESTIGATION.md` and `ROD-ENTERPRISE-BAR-Decision-Preparation.md`'s own pre-decision content.

**Prepared:** 2026-09-23, per direct Repository Owner instruction, following WP-23 Workstream D's own STOP (no Business Activity Engine exists in this repository to rewire) — this document resolves, at the decision-preparation level only, the dependency that STOP surfaced.

**Classification key:** `[LOCKED]` — verbatim constitutional text. `[ACTIVE]` — verbatim from a Status: Active document (`IMP-001`, `RTA-001` is LOCKED). `[FACT]` — directly verified repository fact. `[PRECEDENT]` — a prior Work Package/decision, cited for comparison only. `[RO DECISION REQUIRED]` — an open question requiring Repository Owner resolution.

---

## 0. Repository Owner Decision — Option B Selected

**Decided:** 2026-09-23, by direct Repository Owner selection among the three neutral options presented in §10 above (no option had been ranked or recommended; the Repository Owner was first asked to supply a decision, an initial response arrived as the literal unfilled instruction placeholder `"RO DECISION: [ENTER A, B, OR C]"` and was correctly treated as not-an-answer per this repository's own established discipline of never inferring a Repository Owner decision, and the Repository Owner then explicitly selected in response to a direct re-ask: **"Option B — Separate BA Engine Work Package."**

**What this decision resolves:** §13's Required Repository Owner Decision. The Business Activity Engine specified at `IMP-001 §6.15`–`§6.19` SHALL be built, if and when it is built, under its own separately chartered, cross-cutting runtime Work Package — mirroring the `WP-RTA-001` procedural precedent (§6 above) — never as a byproduct of WP-23 Workstream D, and never by silently expanding the scope of an already-certified component.

**What this decision authorizes:**
- Preparation of the "next required governance artifact" §15's own Option B row identifies: a Work Package Charter + Implementation Readiness Assessment for the future Business Activity Engine Work Package, mirroring `IRA-RTA-001`'s own structure and constitutional weight (§6 above; `WP-RTA-001` precedent).
- This document's own §14 status is updated below to reflect that Option B, not "NOT SELECTED," is now the recorded outcome.

**What this decision does NOT authorize, per the selecting instruction's own explicit constraints:**
- **No Business Activity Engine implementation.** No code, service, module, or stub of any kind is created by this decision or by the governance artifact it authorizes preparing. The forthcoming IRA is a constitutional readiness assessment only, exactly as `IRA-RTA-001` itself was for `WP-RTA-001` (`IRA-RTA-001 §15`: "Constitutionally READY to exist as a Work Package. NOT READY for any implementation milestone").
- **No silent ownership assignment.** The Business Activity Engine is NOT assigned to `Backend/Runtime/AuthorizationEngine` (`WP-RTA-001`) — that component's own Charter already excludes Business Activity lifecycle work (§6 above) and remains, as before, a downstream consumer of the (still nonexistent) Business Activity Engine, never the Engine itself. It is NOT assigned to `AgentOrchestrator` — that remains an unbuilt specification (`IMP-001 §13.5`/`§13.6a`) that is itself a future consumer of the same Business Activity Engine (`§13.6c`: "a hard dependency, not a convention"), never its builder.
- **WP-23 Workstream D remains dependent, not resolved.** Per §10's own Option B text ("this option describes a *path to* resolution, not resolution itself"), Workstream D remains exactly where the original STOP left it — not-implemented, pending the future Business Activity Engine Work Package's own eventual completion. No WP-23 Charter amendment is performed by this decision; §10's own disclosure that a Workstream D Charter re-scoping "would follow, not precede, this option's own authorization" governs, and that re-scoping is deferred to when the future Engine Work Package is itself chartered and registered, not performed now.
- **D1–D9 are unaltered.** No enterprise BAR decision record (`ROD-ENTERPRISE-BAR-Decision-Preparation.md`) is touched by this decision.
- **BAR Workstreams A–C are unaltered.** No code, migration, test, or model file under `Backend/Services/AuthService/` created for Workstreams A–C is modified by this decision.
- **No Business Activity is registered.** Zero of the 21 existing Business Activities, and C-024 BA-01, remain unregistered in `bar_registration`; `BAR-INDEX.md` remains unpopulated.
- **No new Work Package is registered in `WPR-001 §2a` by this decision.** Per the established sequence this decision follows (`WP-RTA-001` precedent: IRA prepared and accepted first, Charter and `WPR-001` registration follow), registration is a later step this document does not itself perform.

---

## 1. Purpose

WP-23 Workstream D's own objective — "make the Business Activity Engine discover Business Activities exclusively through BAR" — cannot be implemented because no Business Activity Engine exists anywhere in this repository. This document investigates and prepares, without selecting, the Repository Owner decision needed to resolve that dependency: whether/how a Business Activity Engine is built, and what that means for WP-23 Workstream D specifically.

---

## 2. Executive Finding

**No Business Activity Engine — nor any functional equivalent — exists anywhere in this codebase.** This is not a partial or stubbed implementation; it is a complete absence, independently re-confirmed for this document (§3) and consistent with every prior finding in this Work Package's own governance chain. The authoritative source (`IMP-001 §6.15`–`§6.19`) specifies the Business Activity Engine as an extensive, foundational "Core Platform Service" — sixteen named architectural responsibilities (`§6.15.4`), a sixteen-stage canonical execution pipeline (`§6.16.3`), an eighteen-part context model (`§6.17`), a sixteen-part state model (`§6.18`), and a sixteen-part transaction-management model (`§6.19`) — spanning roughly 1,900 lines of specification. **No Work Package in this repository's history, including `WP-RTA-001`, has ever built any part of it**; `WP-RTA-001`'s own Charter explicitly and repeatedly disclaims doing so (§6 below). Building it is a separate, large engineering undertaking — comparable in scale to, or larger than, `WP-RTA-001`'s own six-milestone effort to build the narrower Authorization Engine alone — not something WP-23 Workstream D can or should absorb as a side effect of a discovery-integration task.

---

## 3. Existing Verified Evidence (re-confirmed, not rediscovered)

Reused directly from the immediately preceding Workstream D STOP report, plus one further citation newly verified for this document:

- No `BusinessActivityEngine` class, module, or directory exists anywhere in `Backend/` — confirmed by direct repository-wide search (`find`/`grep` across all `.py` files).
- `Backend/Runtime/AuthorizationEngine/` is the only Runtime Component actually built. Its own `engine.py` docstring states it is "the sole authority for runtime **authorization** decisions" (`RTA-001 §11.2`) and explicitly lists "Business Activity / pre-execution-gate integration (M3)" as a later milestone that was never delivered.
- Two disclosed code comments, re-verified unchanged: `Backend/Services/AIService/schemas/conversation.py:37` ("no Business Activity Engine integration exists in AIService yet"); `Backend/Runtime/AuthorizationEngine/authorization/models.py:51` (`AuthorizationContext` is "Constructed by the Business Activity Engine (never by this engine itself)").
- `AgentOrchestrator` (referenced in `IMP-001 §13.5`/`§13.6a`, an AI-orchestration domain service specified under the Enterprise Intelligence Engineering Architecture Enhancement, `AMD-013` Phase 3) does not exist as code anywhere — confirmed by direct search, zero hits in `Backend/`.
- **Newly verified for this document:** `IMP-001 §13.6c` states a sub-task resolving to a Business Activity "is dispatched through the existing `BusinessActivityEngine` interface (Section 6.15), **never through a path `AgentOrchestrator` maintains itself — this is a hard dependency, not a convention**." This confirms `IMP-001` itself treats the Business Activity Engine as a hard prerequisite for `AgentOrchestrator`'s own (also unbuilt) future work — not merely a Workstream-D-local dependency.
- Four unrelated "engine"-named classes exist in `AIService` (`extraction_engine.py`, `scoring_engine.py`, `validation_engine.py`, `rag_engine.py`) — content-processing pipelines for AI features, not Business Activity runtime components. `discovery_provider*` files implement C-090 Enterprise Discovery (external data-source configuration), an unrelated capability.

---

## 4. Authoritative Business Activity Engine Responsibilities

Re-read directly from `IMP-001 §6.15`–`§6.19` for this document (not assumed from the design document's own earlier, narrower citation of `§6.22`/`RTA-001 §3.5` alone):

| Category | Responsibility | Authoritative source | Intended owner | Exists today? | Belongs in WP-23? |
|---|---|---|---|---|---|
| **A. Business Activity discovery** | "Activity Resolution: Locate the Business Activity implementation" (`§6.15.4`); registry-exclusive discovery (`§6.22.8`, `RTA-001 §6.6`) | `IMP-001 §6.15.4`, `§6.22.8`; `RTA-001 §6.6` `[LOCKED]` | Business Activity Engine, querying BAR | **No** — no Engine exists to perform this lookup | **Partially** — BAR's own query surface (the "queried" side) is in scope and delivered (Workstreams A–C); the Engine's own "locate/resolve" side is not |
| **B. Identity/context resolution** | "Context Initialization: Build execution context" (`§6.15.4`); the full Business Activity Context model (`§6.17`, 18 subsections: Activity/Identity/Organization/Enterprise/Authorization/Workflow/Request/Transaction/AI/Runtime Context, immutability, propagation) | `IMP-001 §6.15.4`, `§6.17` | Business Activity Engine | **No** | **No** — this is Engine-internal machinery, not a BAR responsibility |
| **C. Pre-execution processing** | "Input Validation: Validate contracts" (`§6.15.4`); a dedicated Validation Pipeline stage (`§6.16.8`) | `IMP-001 §6.15.4`, `§6.16.8` | Business Activity Engine | **No** | **No** |
| **D. AuthorizationContext construction** | "Authorization: Invoke centralized authorization framework" (`§6.15.4`); Authorization Evaluation stage (`§6.16.7`); `AuthorizationContext` is explicitly "constructed by the Business Activity Engine" per `RTA-001 §11.5`, re-confirmed in `WP-RTA-001`'s own Charter (§6 below) | `IMP-001 §6.15.4`/`§6.16.7`; `RTA-001 §11.5` `[LOCKED]` | Business Activity Engine (construction) → Authorization Engine (evaluation) | **No** (construction side); the evaluation side (`AuthorizationEngine`) **exists**, per `WP-RTA-001` | **No** |
| **E. Authorization invocation** | The Engine invokes the (separately built) Authorization Engine, handing it the constructed context | `IMP-001 §6.15.4`, `§6.16.7`; `RTA-001 §11.13` | Business Activity Engine → Authorization Engine | Authorization Engine side exists (`WP-RTA-001`); invocation side does not | **No** |
| **F. Execution-time BAR gate** | "shall not be executable until successfully registered" (`IMP-001 §6.22.7`/`§6.22.15`); D8's own transitional policy | `IMP-001 §6.22.7`/`§6.22.15`; `ROD-ENTERPRISE-BAR §0g` | BAR (the rule) + Business Activity Engine (the enforcement point) | Rule exists (D2/D8, decided); enforcement point does not | **This is Workstream E**, explicitly out of Workstream D's own scope per the WP-23 Charter |
| **G. Business Activity execution/orchestration** | "canonical execution engine for all Business Activities" (`§6.15.1`); the full 16-stage Canonical Execution Pipeline (`§6.16.3`: Activity Resolution → Manifest Resolution → Context Construction → Authorization → Validation → Metadata Resolution → Workflow Resolution → Business Rule Execution → Persistence Coordination → Transaction Management → Post-Commit Processing → Response Generation) | `IMP-001 §6.15.1`, `§6.16.3` | Business Activity Engine | **No** | **No** |
| **H. Transaction/lifecycle responsibilities** | Full Transaction Management model (`§6.19`, 16 subsections: ownership, canonical lifecycle, scope, atomicity, isolation, nested activities, distributed transactions, commit/rollback/compensation policy, recovery, observability); full State Model (`§6.18`, 16 subsections: canonical states, transitions, Waiting/Suspended/Failed/Cancelled/Rolled-Back states, persistence, events, monitoring, recovery) | `IMP-001 §6.18`, `§6.19` | Business Activity Engine | **No** | **No** |
| **I. Other named responsibilities** | Metadata Resolution, Workflow Coordination, Persistence Coordination, Event Publication, Notification Integration, Audit Recording, AI Assistance, Response Generation, Error Handling, Observability (`§6.15.4`'s own remaining table rows) | `IMP-001 §6.15.4` | Business Activity Engine (each coordinating with an existing, separately-owned platform service — Event Bus, Persistence Services, Audit Engine, Observability Platform, per `RTA-001 §6.4`'s own Runtime Responsibilities table) | **No** (the Engine-side coordination); several of the underlying platform services it would coordinate with (audit, events) already exist and are consumed directly today, without an Engine, by every certified capability | **No** |

**Ownership is not inferred where sources are silent:** every row above cites an exact `IMP-001` subsection naming the Business Activity Engine as the intended owner — none is a guess. `§6.15.3`'s own "Platform Position" text ("a Core Platform Service... every executable operation... shall execute through the Business Activity Engine... No component shall bypass the engine") confirms this is intended as a single, mandatory, platform-wide component — not something any one capability-scoped or cross-cutting Work Package would incidentally build as a byproduct.

---

## 5. Current Runtime Components and Ownership

| Component | Actual scope | Built? | Relationship to Business Activity Engine |
|---|---|---|---|
| `Backend/Runtime/AuthorizationEngine` (`WP-RTA-001`) | "the sole authority for runtime authorization decisions" (`RTA-001 §11.2`) — a five-tier precedence evaluator | Yes, M1–M6 delivered, `CERTIFIED WITH CONDITIONS` (`WPR-001 §2a`) | A **downstream consumer**, not the Business Activity Engine itself — it receives an `AuthorizationContext` the (nonexistent) Business Activity Engine would construct; its own Charter states "no Business Activity wired to it yet" |
| `AgentOrchestrator` (`IMP-001 §13.5`/`§13.6a`) | An AI-orchestration domain service, specified but not built | No — zero code exists | Specified as a **downstream consumer** of the Business Activity Engine (`IMP-001 §13.6c`: "a hard dependency, not a convention") |
| `extraction_engine.py`/`scoring_engine.py`/`validation_engine.py`/`rag_engine.py` (AIService) | Content-processing pipelines for specific AI features | Yes, each independently | Unrelated — none is, or claims to be, a Business Activity Engine |
| `discovery_provider*` (AIService, C-090) | External data-source configuration registry | Yes | Unrelated — a different capability, a different meaning of "discovery" |
| Enterprise BAR (`WP-23`, Workstreams A–C) | Business Activity cataloguing/registration, canonical identity (D2) | Yes, Workstreams A–C | **The registry a future Business Activity Engine would query** — not the Engine itself |

**No competing runtime discovery authority exists.** This is not Phase 2's "Outcome C" (multiple competing authorities) — it is the absence of any runtime discovery authority at all. The only prior discovery-adjacent finding in this repository's own governance history is the investigation's own §7 finding (re-confirmed, unchanged): every certified Business Activity to date is invoked via direct FastAPI routing, never through any Engine-mediated discovery path — a fact consistent with, not contradicted by, today's finding.

---

## 6. Existing Work Package / Charter Authorization Analysis

**`WP-RTA-001` (Authorization Runtime Engine) — re-read directly for this document:**
- **Exact scope:** "Implement `URA-001-76`'s five-tier Authorization Resolution Precedence... as a real, structurally complete evaluator." (`§"Objectives"` item 1)
- **Exact runtime responsibilities:** Authorization decision evaluation only — its own "Responsibility Boundary" table explicitly rows "Authorization Context Construction | **Business Activity Engine (consumed by, not performed by, this Work Package)**."
- **Explicit scope exclusion, verbatim:** "**Out of scope:** anything belonging to a Business Capability's own Business Object or Business Activity lifecycle."
- **Implementation status:** M1–M6 delivered; `CERTIFIED WITH CONDITIONS` (`ADR-016`); its own Exit Criteria section discloses, as an accepted, non-waived limitation: "`RTA-001 §11.2`'s own principle that the engine exists to be consumed, not to exist in isolation, is **not yet satisfied** — no Business Capability consumes this engine's decisions in production use."
- **Does it authorize building the Business Activity Engine now?** **No.** `WP-RTA-001`'s own Charter both explicitly excludes Business Activity lifecycle work and explicitly frames the Business Activity Engine as something *external to it that it depends on*, not something it builds. Stretching this narrower authorization into authority over the Business Activity Engine would directly contradict the Charter's own text.

**`AgentOrchestrator` / `IMP-001 §13.5`–`§13.6c` (AMD-013 Phase 3):** This is a **specification**, not a Work Package — no `WP-NN` charters `AgentOrchestrator`'s own construction, and no code exists. It cannot authorize anything; it is itself a *future consumer* of the same unbuilt Business Activity Engine.

**Any other Runtime/Orchestration/Business Activity/Execution Work Package:** None found. `WPR-001 §2a` (Runtime Work Package Roadmap) contains exactly two entries: `WP-23` (this Work Package, Enterprise BAR) and `WP-RTA-001` (Authorization Engine, analyzed above). No entry anywhere authorizes building the general Business Activity Engine.

**Conclusion (Step 4's own required factual outcome): Outcome C.** No existing authorization covers the Business Activity Engine, even partially in a way WP-23 could extend — a new runtime Work Package would be required to build it, mirroring `WP-RTA-001`'s own precedent (its own Charter's "Capability: None — a Runtime Component serves multiple Business Capabilities; it is not owned by one," `IRA-RTA-001 §9`).

---

## 7. Exact Architectural Gap

`IMP-001 §6.15`–`§6.19` specify a mandatory, platform-wide Business Activity Engine — the sole intended execution path for every Business Activity in this repository, per `§6.15.3`'s own "no component shall bypass the engine" language. **This specification has never been built, in whole or in part, by any Work Package to date.** Every certified Business Activity (all 22 Work Packages' worth) executes today via direct FastAPI routing, entirely outside this specification — a pre-existing, disclosed condition this document does not newly create (the investigation's own §5/§7 findings already established that `RTA-001`'s broader Runtime Execution Architecture, of which the Business Activity Engine is a part, is "entirely unbuilt" for every Business Activity in this repository). WP-23 Workstream D's own objective — make an Engine discover through BAR — presupposes the Engine already exists or is being built concurrently; neither is true.

---

## 8. Relationship to WP-23 Workstream D

Workstream D, as chartered (`WP-23_Enterprise_BAR_Mechanism_Implementation_Charter.md §8`), describes "the (not-yet-built) Business Activity Engine... obtains its list of discoverable, executable Business Activities exclusively by querying the BAR registration record." The Charter's own language ("not-yet-built") already discloses this dependency — it does not claim Workstream D itself builds the Engine. Today's STOP is the first attempt to actually execute Workstream D's own implementation step, which is where the already-disclosed dependency became a concrete blocker rather than a footnoted risk.

---

## 9. What WP-23 Workstreams A–C Already Provide

Assessed directly against `IMP-001 §6.15.4`'s own "Activity Resolution" responsibility and the broader discovery-adjacent needs a future Engine would have:

- **Canonical BAR registration** — `bar_registration` table (Workstream C). **Provided.**
- **`BA-NNNNNN` identity** — `bar_identifier_ledger` + FK-enforced issuance (Workstreams B/C). **Provided.**
- **Registration status** — `registration_status` (CHECK-constrained to `'REGISTERED'`, D2's own two-state minimum). **Provided.**
- **BAR repository/service retrieval** — `BarRegistrationRepository.get_by_identifier`, `get_by_work_package_and_reference`; `BarRegistrationService.register`. **Provided** (a query/write surface exists and is tested).
- **Owning Capability / Owning Work Package / registration metadata** — all persisted, queryable columns. **Provided.**

**What is NOT provided, and cannot be provided by WP-23 alone:** the actual runtime consumer that would call this query surface. **The BAR-side discovery capability is complete and ready to be consumed. The Business Activity Engine runtime discovery *consumer* does not exist.** These are two distinct things — the first is data-and-query infrastructure (a "waiter"); the second is a running system component (a "diner") that has not yet been seated. No engine is invented here merely to close this distinction — per this task's own explicit instruction, doing so would fabricate the very component this investigation exists to flag as missing.

---

## 10. Options A–C (neutral, none selected, none ranked)

### OPTION A — Defer WP-23 Workstream D

**Engineering scope:** none — Workstream D remains not-implemented, exactly as the current STOP leaves it.

**Governance required:** a Repository Owner acknowledgment that Workstream D is deferred pending a future, independently governed Business Activity Engine — no new governance artifact is strictly required beyond recording this decision.

**Effect on existing WP-23:** Workstreams A–C remain delivered and usable; Workstreams E–H remain blocked or partially blocked by the same missing consumer (E explicitly depends on D per the WP-23 Charter's own Workstream sequencing; F/G/H do not strictly require D to exist first, but their own eventual completion still needs D/E to close the loop).

**Effect on BAR:** none — BAR's own decided scope (D1–D9) is fully delivered on the registration side regardless.

**Dependencies:** a future, separately-governed Business Activity Engine Work Package (Option B) or an equivalent future decision.

**What would remain unfinished:** Workstream D, E, and — practically — the enterprise BAR mechanism's own execution-time relevance (registration would exist, but nothing would yet consult it to gate or discover execution).

**WP-23 Charter modification required?** Not necessarily — the Charter's own existing "not-yet-built" language already accommodates this outcome.

**New Charter/IRA/registration sequence required?** No, under this option alone.

### OPTION B — Create a separate Business Activity Runtime Work Package

**Engineering scope:** build the Business Activity Engine per `IMP-001 §6.15`–`§6.19`'s own full specification (or a Repository-Owner-scoped subset of it, mirroring how `WP-RTA-001` itself delivered a scoped subset of `RTA-001 §11`) — Activity Resolution, Context Construction/`§6.17`, the Execution Pipeline/`§6.16`, State Model/`§6.18`, Transaction Management/`§6.19`, with BAR-exclusive discovery as one governed requirement among many others already specified.

**Governance required:** a new Work Package Charter, an Implementation Readiness Assessment analogous to `IRA-RTA-001`, and the full `CLAUDE.md §19.7b` five-gate closure sequence — the same weight of process `WP-RTA-001` itself required, likely larger given the BAE's own broader specification.

**Effect on existing WP-23:** Workstream D would then be re-scoped to "integrate with the now-existing Business Activity Engine" rather than "build discovery into a nonexistent engine" — a Charter amendment to WP-23 would follow, not precede, this option's own authorization.

**Effect on BAR:** BAR's own already-decided scope (D1–D9) is unaffected; a new Work Package would consume, not alter, it.

**Dependencies:** a Repository Owner decision to authorize a new cross-cutting runtime Work Package, mirroring the `WP-RTA-001` precedent's own procedural class.

**What would remain unfinished:** until that new Work Package completes, WP-23 Workstream D (and E) remain exactly where Option A leaves them — this option describes a *path to* resolution, not resolution itself.

**WP-23 Charter modification required?** Yes, eventually — once the new Engine exists, to re-scope Workstream D to integration rather than construction.

**New Charter/IRA/registration sequence required?** Yes — a new, separately chartered and registered Work Package.

### OPTION C — Narrow WP-23 Workstream D's own scope

**Engineering scope:** redefine Workstream D's own deliverable as "the BAR-side discovery contract/query surface a future Business Activity Engine will consume" — which, per §9 above, is already substantially delivered by Workstreams A–C — rather than "rewire an existing engine."

**Governance required:** a WP-23 Charter amendment narrowing Workstream D's own stated objective (`§8`) to match what is actually achievable without an Engine.

**Effect on existing WP-23:** Workstream D could be marked complete (or near-complete) without contradiction, since its own re-scoped deliverable already exists; this would not create new capability, only reconcile documentation with reality.

**Effect on BAR:** none beyond what Workstreams A–C already deliver.

**Dependencies:** none beyond the Charter amendment itself.

**What would remain unfinished:** the actual runtime discovery behavior `RTA-001 §6.6`/`IMP-001 §6.22.8` describe — no Business Activity would actually be discovered by anything at runtime under this option; the "exclusively through BAR" LOCKED requirement remains textually satisfied only in the trivial sense that *no* discovery mechanism exists to violate it.

**WP-23 Charter modification required?** Yes — this option's own text is a Charter amendment.

**New Charter/IRA/registration sequence required?** No new Work Package; an amendment to the existing one.

**No option is ranked, scored, or named as a winner.**

---

## 11. Governance Implications

- D1–D9 are unaffected by any of the three options — none touches enterprise BAR scope, identity authority, retroactivity, the `IMP-001` relationship, registration-record placement, or the transitional gate.
- `C-024 D10` is unaffected — BA-01 remains NOT STARTED and outside any of these options' own scope.
- Option B's own eventual Work Package would need its own full governance sequence (Charter → IRA → the five-gate closure), independent of and not shortcut by WP-23's own already-completed gates for Workstreams A–C.
- Option C's own Charter amendment would need to be weighed against `CLAUDE.md §19.7`'s own Business Activity Completion Gate discipline — amending a chartered Workstream's own objective after the fact is a disclosed, not silent, act if chosen.

## 12. Engineering Implications

- Option A: zero engineering effort now; the BAR-side query surface (Workstreams A–C) sits idle until a consumer exists.
- Option B: the largest engineering effort of the three — potentially exceeding `WP-RTA-001`'s own six-milestone scope, given `IMP-001 §6.15`–`§6.19`'s own broader specification surface (16 responsibilities, a 16-stage pipeline, an 18-part context model, two further 16-part models).
- Option C: minimal engineering effort (largely already done); the effort is documentation/governance, not code.

---

## 13. Required Repository Owner Decision

**The Repository Owner must decide:** given that no Business Activity Engine exists and no existing Work Package authorizes building one, does AUREX (1) defer WP-23 Workstream D indefinitely pending a future, independently governed Business Activity Engine (Option A); (2) authorize a new, separately chartered cross-cutting runtime Work Package to build the Business Activity Engine per `IMP-001 §6.15`–`§6.19` (Option B); or (3) narrow WP-23 Workstream D's own chartered objective to the BAR-side query surface alone, which Workstreams A–C already substantially deliver (Option C)?

No sub-decisions (scope of a future Engine Work Package, its own timeline, or the exact amended wording for Option C) are resolved here — each would follow from, not precede, this root decision.

---

## 14. Decision Status — OPTION B SELECTED

~~No option has been selected. This document presents evidence and options only, per its own stated Purpose (§1) and Document type (header).~~

*(Updated 2026-09-23, per §0 above.)* **Option B — Create a separate Business Activity Runtime Work Package — has been selected** by explicit Repository Owner decision, recorded in full at §0. This document's own Purpose (§1) and original Document type (header: "selects nothing") described its state at preparation time; §0 now supersedes that description of decision status only — every evidentiary finding (§2–§9), the neutral option analysis itself (§10), and the governance/engineering implications (§11–§12) remain unchanged and are not reopened by this update, consistent with this repository's own no-silent-fix convention.

---

## 15. Scope Exclusions

This document does **not**: implement a Business Activity Engine, a fake adapter, a source-code scanner, a static discovery registry, or any runtime execution code; modify the `WP-23` Charter; modify D1–D9 or any enterprise BAR decision record; modify `BAR-INDEX.md`; register any Business Activity; assign any Business Activity Identifier; modify `WPR-001` or `CBOR-INDEX.md`; or modify any constitutional document.

**Required document changes AFTER a decision is made (identified now, not performed):**
- **If Option A:** a brief recorded note (e.g., in `WPR-001 §2a`'s own WP-23 row or a future maintenance note) that Workstream D is formally deferred, pending a future Engine.
- **If Option B:** a new Work Package Charter + IRA for the Business Activity Engine; a subsequent WP-23 Charter amendment re-scoping Workstream D to integration.
- **If Option C:** a WP-23 Charter amendment to `§8` (Discovery Mechanism) narrowing its own stated objective, plus a corresponding update to `ENTERPRISE-BAR-MECHANISM-DESIGN-AND-IMPLEMENTATION-READINESS.md §9`/`§19`/`§22`.

None of these is performed by this document.

---

## 16. Source / Evidence References

`IMP-001_Implementation_Playbook.md §6.15`–`§6.19` (Business Activity Engine, Execution Pipeline, Context, State Model, Transaction Management — Active); `§13.5`/`§13.6a`–`§13.6c` (`AgentOrchestrator`, AMD-013 Phase 3 — specified, unbuilt); `§6.22` (Business Activity Registry — Active, already governing D1–D9); `RTA-001 §3.5`/`§6.1`–`§6.6`/`§11.2`/`§11.5`/`§11.13` (LOCKED); `WP-RTA-001_Authorization_Runtime_Engine.md` (Charter, `WPR-001 §2a`); `IRA-RTA-001_Authorization_Runtime_Engine_Implementation_Readiness_Assessment.md §6`/`§7`/`§9`; `WP-23_Enterprise_BAR_Mechanism_Implementation_Charter.md §8`; `ENTERPRISE-BAR-MECHANISM-DESIGN-AND-IMPLEMENTATION-READINESS.md §9`/`§19a`/`§22`; `ROD-ENTERPRISE-BAR-Decision-Preparation.md` (D1–D9); direct repository-wide code search across `Backend/` (this document and the immediately preceding Workstream D STOP report).

---

*End of investigation, as amended by §0/§14 on 2026-09-23. Option B selected — a separate, future Business Activity Engine Work Package is required; this document does not build it. No Business Activity Engine, adapter, or runtime code created. `WP-23` Charter, D1–D9, `BAR-INDEX.md`, `WPR-001`, and `CBOR-INDEX.md` were read, not modified. No Business Activity was registered. No Business Activity Identifier was assigned. C-024 BA-01 remains unregistered. Nothing staged, committed, or pushed.*
