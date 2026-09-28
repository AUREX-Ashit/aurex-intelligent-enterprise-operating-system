# IRA-BAE-001 — Business Activity Engine Implementation Readiness Assessment

**Document ID:** IRA-BAE-001
**Work Package:** Not yet registered (this document is the constitutional readiness assessment that precedes registration — see §16)
**Constitutional Subject:** The Business Activity Engine, `IMP-001 §6.15`–`§6.19`
**Methodology Applied:** `ADR-014`/`WP-METH-001` (`IMP-001 §6.2a` Mandatory Context Discovery, `§6.2b` Gap Analysis Category Scheme), applied to a Runtime Component per the `IRA-RTA-001` precedent (the first IRA in this repository to do so) — this document is the second, and follows `IRA-RTA-001`'s own structure directly rather than re-deriving a shape for it.
**Status:** Assessment and constitutional charter-preparation only. No implementation, no code, no API, no schema, no migration, no test is authorized by this document. This document does not itself charter a Work Package or register one in `WPR-001 §2a` — it prepares the readiness assessment a future Charter would rest on, per the Repository Owner's own Option B decision (`BAR-WP23-WORKSTREAM-D-BUSINESS-ACTIVITY-ENGINE-PREREQUISITE-INVESTIGATION.md §0`).

Treat the Git repository as the ONLY source of truth. Every claim below is sourced from `architecture/03-Engineering/IMP-001_Implementation_Playbook.md` (`§6.15`–`§6.19`, `§13.5`/`§13.6a`–`§13.6c`, `§6.22`, read in full), `architecture/02-Constitutional/RTA-001 - Runtime Architecture and Execution.md` (`§3.5`, `§6.1`–`§6.6`, `§11.2`, `§11.5`, `§11.13`), `architecture/05-Implementation/WP-RTA-001_Authorization_Runtime_Engine.md`, `architecture/05-Implementation/IRA-RTA-001_Authorization_Runtime_Engine_Implementation_Readiness_Assessment.md`, `architecture/06-Reviews/BAR-WP23-WORKSTREAM-D-BUSINESS-ACTIVITY-ENGINE-PREREQUISITE-INVESTIGATION.md` (§0, §2–§13), `architecture/05-Implementation/WP-23_Enterprise_BAR_Mechanism_Implementation_Charter.md`, `architecture/00-Governance/WPR-001_Work_Package_Roadmap.md`, and `architecture/06-Reviews/TECH-DEBT.md`. No claim is drawn from conversational memory.

---

## 1. Executive Summary

`BAR-WP23-WORKSTREAM-D-BUSINESS-ACTIVITY-ENGINE-PREREQUISITE-INVESTIGATION.md` found, when WP-23 Workstream D attempted to rewire "the Business Activity Engine" to discover Business Activities exclusively through the newly built Enterprise BAR, that no such Engine — nor any functional equivalent — exists anywhere in this repository. The investigation's own §10 disclosed three neutral, unranked options for resolving this and selected none, escalating the choice to the Repository Owner per `CLAUDE.md §18`'s STOP-and-report discipline, in the same procedural shape `IRA-005 §10.2 item 3` used for the Authorization Engine gap that produced `IRA-RTA-001`/`WP-RTA-001`.

**The Repository Owner has now made that decision** (`BAR-WP23-WORKSTREAM-D-BUSINESS-ACTIVITY-ENGINE-PREREQUISITE-INVESTIGATION.md §0`): Option B — the Business Activity Engine, if and when built, is chartered as its own separate, cross-cutting runtime Work Package, never as a byproduct of WP-23 Workstream D and never by silently expanding `Backend/Runtime/AuthorizationEngine`'s or any other existing component's scope. This document is the constitutional readiness assessment for that future charter, mirroring `IRA-RTA-001`'s own role for `WP-RTA-001`. It establishes the boundary of what the future Business Activity Engine Work Package is and is not, records the Repository Owner decision that authorizes its eventual existence, and identifies what must still be resolved before real implementation milestones may begin. **It does not itself charter, register, or begin implementing anything.**

## 2. Purpose

To establish the constitutional foundation required before any Business Activity Engine implementation may proceed: a stated boundary distinguishing this future Runtime Component's responsibilities from every existing Business Capability's and every existing Runtime Component's own responsibilities, an explicit record of the Repository Owner decision resolving `BAR-WP23-WORKSTREAM-D-...-INVESTIGATION.md §13`, and a disclosure of what remains open before a Charter and `WPR-001 §2a` registration may follow.

## 3. Scope

**In scope for this IRA:** the constitutional groundwork itself — responsibility boundary (Runtime vs. Business, and vs. every existing Runtime Component), dependency identification, risk disclosure, and readiness assessment for a future Charter to be prepared.

**Out of scope for this IRA:** any implementation detail (service placement, pipeline-stage implementation, persistence mechanism, algorithm implementation, milestone sequencing). Those remain for the future Work Package's own separately-scoped, milestone-level gap analyses, each subject to its own `CLAUDE.md §19` Implementation Start Checklist before code is written — exactly as `IRA-RTA-001 §3` reserved them for `WP-RTA-001`. Also out of scope: registering the future Work Package in `WPR-001 §2a` (that follows a Charter, which follows Repository Owner acceptance of this IRA — see §16) and re-scoping WP-23 Workstream D's own chartered text (disclosed as a later, following action in the investigation's own §0/§10/§15, not performed here).

## 4. Constitutional Authority

| Authority | Role |
|---|---|
| `IMP-001 §6.15` | Names the Business Activity Engine as a "Core Platform Service" and states its Platform Position: "every executable operation... shall execute through the Business Activity Engine... No component shall bypass the engine." |
| `IMP-001 §6.15.4` | Sixteen named architectural responsibilities (Activity Resolution, Context Initialization, Input Validation, Authorization invocation, Metadata Resolution, Workflow Coordination, Business Rule Execution, Persistence Coordination, Transaction Management, Post-Commit Processing, Response Generation, Event Publication, Notification Integration, Audit Recording, AI Assistance, Error Handling/Observability). |
| `IMP-001 §6.16.3` | The sixteen-stage canonical execution pipeline (Activity Resolution → Manifest Resolution → Context Construction → Authorization → Validation → Metadata Resolution → Workflow Resolution → Business Rule Execution → Persistence Coordination → Transaction Management → Post-Commit Processing → Response Generation). |
| `IMP-001 §6.17` | The eighteen-part Business Activity Context model (Activity/Identity/Organization/Enterprise/Authorization/Workflow/Request/Transaction/AI/Runtime Context, immutability, propagation). |
| `IMP-001 §6.18` | The sixteen-part canonical State Model. |
| `IMP-001 §6.19` | The sixteen-part Transaction Management model. |
| `IMP-001 §6.22.7`/`§6.22.15`/`§6.22.8` | "Shall not be executable until successfully registered" (execution gate); registry-exclusive discovery — already governs enterprise BAR's own D2/D8/D9, and names the Business Activity Engine as this rule's own enforcement point. |
| `RTA-001 §6.6` `[LOCKED]` | "Business Activities shall never be discovered through implementation-specific mechanisms" — the same discovery-exclusivity principle, stated at the Runtime Architecture layer. |
| `RTA-001 §11.2`/`§11.5`/`§11.13` `[LOCKED]` | Names the Business Activity Engine as the constructor of `AuthorizationContext` and the invoker of the (separately built) Authorization Engine — never the reverse. |
| `IMP-001 §13.6c` | States a further, independent hard dependency: `AgentOrchestrator`'s own future work dispatches through "the existing `BusinessActivityEngine` interface (Section 6.15), never through a path `AgentOrchestrator` maintains itself — this is a hard dependency, not a convention." |
| `WP-RTA-001_Authorization_Runtime_Engine.md` | Its own Responsibility Boundary table rows "Authorization Context Construction \| Business Activity Engine (consumed by, not performed by, this Work Package)" and its own Scope excludes "anything belonging to a Business Capability's own Business Object or Business Activity lifecycle" — confirmed, not assumed, that this existing, already-certified Work Package does not and cannot be read to cover the Business Activity Engine. |
| `IRA-RTA-001` (in full) | The direct structural and procedural precedent this document mirrors — the first IRA in this repository chartering a Runtime Component rather than a Business Capability. |
| `BAR-WP23-WORKSTREAM-D-BUSINESS-ACTIVITY-ENGINE-PREREQUISITE-INVESTIGATION.md §0`/`§2`–`§13` | First identified the gap (re-confirming zero code exists anywhere), disclosed the three resolution options, and now records the Repository Owner's Option B selection this IRA exists to act on. |
| `ARCH-000` Layer model | Places the Business Activity Engine's governing specification (`IMP-001`, Layer 3/4 methodology and implementation-specification material) as requiring its own chartering before implementation, per the same reasoning `IRA-RTA-001 §4` applied to `RTA-001`. |
| `CLAUDE.md §18`/`§19.4` | The STOP-and-report discipline this entire document exists to satisfy. |

## 5. Repository Owner Decision

The Repository Owner has accepted the following decision, recorded in full at `BAR-WP23-WORKSTREAM-D-BUSINESS-ACTIVITY-ENGINE-PREREQUISITE-INVESTIGATION.md §0`, resolving that investigation's own §13 Required Repository Owner Decision as **Option B**:

> "Option B — Separate BA Engine Work Package."

This decision:
- Rejects Option A (indefinite deferral with no forward path) as the *sole* disposition — WP-23 Workstream D remains deferred in the interim (§6 below), but a forward path is now authorized to exist.
- Rejects Option C (narrowing WP-23 Workstream D's own chartered objective to the BAR-side query surface alone) — the investigation's own §10 discloses Option C would leave "no Business Activity... actually discovered by anything at runtime," which the Repository Owner did not select as sufficient.
- Selects Option B — a dedicated, separately chartered, cross-cutting runtime Work Package for the Business Activity Engine, mirroring the `WP-RTA-001` precedent's own procedural class (§4 above).
- **Does not itself authorize any implementation**, mirroring `IRA-RTA-001 §5`'s own identical discipline: this decision authorizes the future Work Package's eventual constitutional existence once a Charter is prepared and this IRA is accepted (§16) — it is not itself readiness for any specific deliverable.
- **Does not assign ownership to any existing component.** `Backend/Runtime/AuthorizationEngine` (`WP-RTA-001`) and `AgentOrchestrator` (`IMP-001 §13.5`/`§13.6a`, unbuilt) each remain, as before, downstream *consumers* of the Business Activity Engine's future output — never the Engine itself, and never expanded in scope to absorb it (§9 below).
- **Leaves WP-23 Workstream D dependent, not resolved.** Workstream D remains not-implemented pending this future Work Package's own eventual completion (§6 below); no WP-23 Charter amendment is performed by this document.

## 6. Dependencies

| Dependency | Nature | Status |
|---|---|---|
| `IMP-001 §6.15`–`§6.19` | Governing specification the Engine must conform to | Exists, Active |
| `RTA-001 §6.6`/`§11.2`/`§11.5`/`§11.13` | Discovery-exclusivity and Authorization-invocation principles the Engine must conform to | Exists, LOCKED |
| Enterprise BAR (`WP-23` Workstreams A–C: `bar_identifier_ledger`, `bar_registration`) | The registry the Engine's own Activity Resolution responsibility (`§6.15.4`) would query — **consumed, never owned or duplicated** | ~~Delivered, certified, and directly reusable as-is~~ *(C-4 correction, 2026-09-28, `IRA-WP-23-AC §7` S-1: the WP-23 A–C tranche is implemented, independently verified (Gates 1–5) and **accepted** (`IRA-WP-23-AC §0.2`), committed in `b0f5a12e84a9a3f7d9622bcbea4cee87b934be85`; **not certified**; WP-23 remains OPEN. It was not delivered or certified when this was written.)* Reusable as-is; no BAR schema change is anticipated by this document |
| `Backend/Runtime/AuthorizationEngine` (`WP-RTA-001`) | The separately built, already-certified consumer the future Engine would invoke (`RTA-001 §11.13`), handing it a constructed `AuthorizationContext` | Exists, `CERTIFIED WITH CONDITIONS`; its own disclosed condition ("no Business Capability consumes this engine's decisions in production use," `IRA-RTA-001 §15`) would be resolved once, and only once, a real Business Activity Engine actually invokes it — a future milestone-level fact, not decided here |
| `AgentOrchestrator` (`IMP-001 §13.5`/`§13.6a`) | A second, independent future consumer with "a hard dependency, not a convention" on the Engine (`§13.6c`) | Specified only; zero code exists; not built by this document or by the future Engine Work Package itself |
| WP-23 Workstream D (discovery integration) | The originating blocked task this future Work Package exists to unblock | Deferred, pending this future Work Package (§0 above) |
| At least one real, willing Business Capability to migrate its execution path onto the Engine once built | `IMP-001 §6.15.3`'s own "no component shall bypass the engine" language is a target-state principle; every certified Business Activity to date executes via direct FastAPI routing (investigation's own §7 finding), a pre-existing condition this document does not resolve | Not yet identified; a future Work Package's own milestone-level concern, mirroring how `IRA-RTA-001 §6`'s own final row flagged the identical open question for the Authorization Engine |

**A note on scale, mirroring `IRA-RTA-001 §6`'s own disclosure pattern:** the Business Activity Engine's governing specification (16 responsibilities, a 16-stage pipeline, an 18-part context model, two further 16-part models — roughly 1,900 lines of `IMP-001` text) is, on its face, comparable to or larger than `RTA-001 §11`'s own specification for the narrower Authorization Engine, which itself required six milestones (`WP-RTA-001` M1–M6) to deliver a five-tier precedence evaluator alone. This IRA does not scope milestones (§3 above) — it discloses that the future Work Package's own eventual Charter should expect a comparable or larger milestone count, not assume a single-pass delivery.

## 7. Out of Scope

- Any Business Activity of any capability (C-002 through C-132 and beyond) — the future Engine invokes; it does not own or re-implement any capability's own Business Object or Business Activity lifecycle.
- `Backend/Runtime/AuthorizationEngine`'s own decision-evaluation logic — remains `WP-RTA-001`'s exclusive concern; the future Engine only invokes it (§11.13) and constructs the context it consumes (§11.5) — it never re-implements precedence evaluation itself.
- `AgentOrchestrator`'s own construction — remains a separate, independently future-chartered concern; the future Engine is a dependency `AgentOrchestrator` would consume, not a component that builds `AgentOrchestrator`.
- Enterprise BAR's own registration/identifier mechanism (`WP-23` Workstreams A–C) — remains BAR's exclusive concern; the future Engine only queries it (§6 above), per `IMP-001 §6.22.8`/`RTA-001 §6.6`'s own registry-exclusive-discovery principle.
- WP-23 Workstream D's own Charter text — not amended by this document (§5 above); any future re-scoping is a distinct, later act.
- Migrating any existing, already-certified Business Activity's execution path from direct FastAPI routing onto the future Engine — each capability's own future, separately-scoped decision, exactly as `IRA-RTA-001 §7`'s own final bullet disclosed for the Authorization Engine.
- Any UI, frontend, or presentation-layer work.
- Registering a Work Package number in `WPR-001 §2a` — a later step, following Charter preparation and Repository Owner acceptance of this IRA (§16).

## 8. Business Activity Engine — Responsibilities (restated as future scope)

Per `IMP-001 §6.15.4`/`§6.16.3`/`§6.17`–`§6.19`, restated as this future Work Package's own eventual scope (implementation deferred to its own future milestones, not defined here):

- Activity Resolution (querying BAR — the one responsibility with a delivered, reusable dependency today, per §6 above) *(C-4 annotation, 2026-09-28, `IRA-WP-23-AC §7` S-6: "delivered" predated independent verification of WP-23 A–C. The tranche is now accepted (`IRA-WP-23-AC §0.2`) and committed in `b0f5a12e84a9a3f7d9622bcbea4cee87b934be85`; not certified.)*
- Context Initialization / the full 18-part Business Activity Context model
- Input Validation
- Authorization invocation (constructing `AuthorizationContext`, invoking the existing Authorization Engine — never re-implementing its evaluation)
- Metadata Resolution, Workflow Coordination
- Business Rule Execution (capability-owned rules, invoked not owned)
- Persistence Coordination, Transaction Management (16-part model)
- Post-Commit Processing, Response Generation
- Event Publication, Notification Integration, Audit Recording (each coordinating with an already-existing, separately-owned platform service, per the investigation's own §4 row I finding — not rebuilt by the Engine)
- AI Assistance, Error Handling, Observability
- The full 16-part State Model (canonical states, transitions, Waiting/Suspended/Failed/Cancelled/Rolled-Back)

## 9. Business Responsibilities

**None.** Mirroring `IRA-RTA-001 §9`'s own central constitutional fact, restated here for the Business Activity Engine:
- Owns no Business Object anywhere in `CMD-001`'s registry.
- Performs no Business Activity of any capability — it executes them on each capability's own behalf; it never becomes their owner.
- Is invoked by nothing upstream of it in the model `IMP-001 §6.15.3` describes ("no component shall bypass the engine") — every certified Business Activity would, in the Engine's own target state, execute *through* it; the Engine itself has no upstream Business Capability caller of its own.
- Does not own BAR's own registration data (`bar_identifier_ledger`/`bar_registration` remain AuthService/BAR's own tables, per `WP-23`'s own Workstream C design) — the Engine queries them; it never writes to them, never duplicates them, and never becomes a second discovery authority alongside them (`IMP-001 §6.22.8`/`RTA-001 §6.6`).
- Does not own the Authorization Engine's own decision logic (`RTA-001 §11.2`: "the Authorization Engine is the sole authority for runtime authorization decisions") — the future Business Activity Engine constructs context and invokes; it never decides.

## 10. Constitutional Principles

Restated from `IRA-RTA-001 §10`, confirmed to apply identically to this second Runtime Work Package by the same reasoning that document itself declared binding on "any future Runtime Work Package":

1. **Runtime Engines are shared infrastructure.** `RTA-001 §2.3`/`§3.3` names the Business Activity Engine as one of a fixed set of Runtime Execution Platform components, not capability-specific by design.
2. **Runtime Engines own no Business Objects.** Confirmed directly (§9 above) — no Runtime Component appears anywhere in `CMD-001`'s Business Object registry, and this document introduces none.
3. **Runtime Engines implement no Business Activities.** The Engine *executes* Business Activities on each capability's own behalf; it does not become their owner or re-implement their business rules.
4. **Runtime Engines execute runtime policies.** The Engine enforces the already-decided BAR execution gate (D2/D8) and discovery-exclusivity rule (`IMP-001 §6.22.8`); it does not author these policies itself.
5. **Business Capabilities remain the owners of Business Objects and Business Activity lifecycles.** No capability's own ownership is reassigned by this document's existence.
6. **Runtime Engines may be reused by multiple Business Capabilities.** The future Business Activity Engine is, by its own governing specification (`§6.15.3`), the single mandatory execution path for every Business Activity in this repository — one Engine, every capability, never rebuilt per capability.
7. **Runtime Engines require explicit constitutional authorization before implementation.** This is exactly the gap the prerequisite investigation found and this document begins to close — `CLAUDE.md §18`/`§19.4`'s STOP-and-report discipline applies identically here as it did for `WP-RTA-001`.

## 11. Assumptions

- `IMP-001 §6.15`–`§6.19`'s own specification is assumed correct and complete as the target specification to (eventually) implement — it is canonical text, not a design choice this IRA introduces.
- The future Engine's eventual service/module placement (embedded, standalone, or shared-library) is **not** assumed here and is explicitly deferred to the future Work Package's own milestone-level design, informed by `CLAUDE.md §8`'s service-boundary rules at that time — mirroring `IRA-RTA-001 §11`'s identical deferral for the Authorization Engine.
- Existing certified Business Activities' direct-FastAPI-routing execution path is assumed to remain operative until each capability separately decides to migrate onto the future Engine — this document does not assume a mandatory, repository-wide cutover, mirroring `IRA-RTA-001 §11`'s own identical disclosure for `PLATFORM_ADMIN` gating.
- BAR's own already-delivered query surface *(C-4 annotation, 2026-09-28, S-7: "already-delivered" predated independent verification; WP-23 A–C are now accepted, `IRA-WP-23-AC §0.2`, and committed in `b0f5a12e84a9a3f7d9622bcbea4cee87b934be85`; not certified)* (`BarRegistrationRepository.get_by_identifier`, `get_by_work_package_and_reference`) is assumed sufficient, unmodified, for the future Engine's own Activity Resolution responsibility — no BAR schema change is anticipated by this document; any actual gap discovered during future milestone-level design would be its own disclosed finding at that time, not assumed away here.

## 12. Risks

| Risk | Description | Disposition |
|---|---|---|
| Scale risk | The governing specification's own scope (16 responsibilities, 16-stage pipeline, 18-part context model, two further 16-part models) exceeds `RTA-001 §11`'s own narrower Authorization Engine specification, which itself required six milestones | Future Charter should scope milestones deliberately, not assume single-pass delivery (§6 above) |
| Scope-creep into existing certified components | Temptation to satisfy Workstream D's own original objective faster by expanding `AuthorizationEngine`'s or `AgentOrchestrator`'s own scope instead of building a genuinely separate Engine | Explicitly foreclosed by §0/§5's own Repository Owner decision text ("does not assign ownership to any existing component") — any future attempt to do so would contradict this recorded decision, not merely be inadvisable |
| Migration risk | If/when existing certified Business Activities adopt the future Engine as their execution path, that is a cross-cutting change touching already-certified code across every prior Work Package | Explicitly out of this document's scope (§7); each capability's own future, separately-scoped decision, mirroring `IRA-RTA-001 §12`'s identical disposition for its own analogous risk |
| Indefinite deferral risk | Nothing in this document or in §0's own decision compels the future Work Package to actually be chartered on any timeline | Disclosed, not resolved — `BAR-WP23-...-INVESTIGATION.md §10`'s own Option B text already states "this option describes a path to resolution, not resolution itself"; WP-23 Workstream D remains formally deferred (§5 above) until that future Charter is actually prepared and accepted |
| False-progress risk on WP-23 Workstream D | A future reader could mistake this IRA's existence for Workstream D having been unblocked | This document explicitly states (§5, §13) that Workstream D remains dependent, not resolved, by this IRA alone |

## 13. Technical Debt

This IRA creates no new Technical Debt (it authorizes no implementation). It references the relevant existing disclosures:
- The investigation's own finding that every certified Business Activity to date executes via direct FastAPI routing, entirely outside any Runtime Execution Architecture Engine-mediated path — a pre-existing, already-disclosed condition (`BAR-WP23-...-INVESTIGATION.md §7`), not newly created here.
- `WP-RTA-001`'s own disclosed, accepted limitation that no Business Capability yet consumes its decisions in production (`IRA-RTA-001 §15`) — this document does not resolve that; it remains open until a real Business Activity Engine exists and actually invokes it.
- WP-23 Workstream D's own deferred status (§0/§5 above) — not itself a new Technical Debt entry (it is a disclosed dependency, tracked in the investigation document and this IRA, not the Technical Debt Register per `CLAUDE.md §19.8.1`'s own definition, since it is not "a normal outcome of iterative development" so much as an explicit cross-Work-Package dependency already fully disclosed by name in both governing documents).

## 14. Success Criteria

This IRA (plus its eventual acceptance) is successful when:
- The Runtime/Business responsibility boundary for the future Business Activity Engine is stated unambiguously (§9 above) and does not contradict `RTA-001`, `WP-RTA-001`'s own Charter, or the prerequisite investigation.
- No implementation, schema, API, or code exists as a result of this document (verified: this document alone is the only artifact created by it).
- A future implementer can begin Charter preparation and milestone-level planning without needing to re-derive the ownership question this document and its predecessor (`BAR-WP23-...-INVESTIGATION.md`) already resolved.
- WP-23 Workstream D's own dependency on this future Work Package remains explicit and traceable (§5, §6 above), not silently dropped.

## 15. Implementation Readiness Assessment

**This document does not itself make any specific deliverable implementation-ready**, mirroring `IRA-RTA-001 §15`'s own identical discipline. Per `IMP-001 §6.2b`'s Gap Analysis category scheme, applied here to a second Runtime Work Package by direct analogy:
- The **constitutional** question (who owns this, under what future charter) — **now resolved** by §5's Repository Owner decision. This was the gap the prerequisite investigation's own §13 identified; it is closed by this document.
- Every **implementation-level** question (milestone sequencing, service placement, which capability first migrates onto the Engine, exact pipeline-stage implementation) remains open and is deliberately **not** resolved here — each requires its own future, milestone-scoped gap analysis before code is written, per `CLAUDE.md §19`'s Implementation Start Checklist, applied fresh at that time.
- A further, prior step this document does not itself perform: a Work Package Charter must still be prepared and the Work Package registered in `WPR-001 §2a` before any milestone-level gap analysis could even begin — mirroring exactly how `IRA-RTA-001` preceded, rather than replaced, `WP-RTA-001`'s own Charter document.

**Readiness Decision: Constitutionally READY for a future Charter to be prepared. NOT READY for `WPR-001 §2a` registration or for any implementation milestone** — a Charter document must be authored and accepted first (§16), exactly as `WP-RTA-001_Authorization_Runtime_Engine.md` followed `IRA-RTA-001`.

## 16. Recommendation

Prepare a future Work Package Charter (working title: `WP-BAE-001_Business_Activity_Engine.md`, or a Repository-Owner-chosen equivalent, mirroring `WP-RTA-001_Authorization_Runtime_Engine.md`'s own document shape) only once the Repository Owner separately authorizes that next step — this document does not create that Charter, and does not assume the Repository Owner wishes to proceed immediately. Once such a Charter is accepted, register the resulting Work Package in `WPR-001 §2a` (mirroring `WP-RTA-001`'s own row), and only then begin milestone-level gap analyses, each individually gated under `CLAUDE.md §19` before any code is written — consistent with `IRA-RTA-001 §16`'s own identical recommendation sequence for the Authorization Engine. The most natural first milestone to gap-analyze, once such a Charter is accepted, is Activity Resolution against BAR (§6, §8 above) — the one responsibility this document finds already has a real, delivered, reusable dependency (`WP-23` Workstreams A–C) to build against, mirroring how `IRA-RTA-001 §16` identified the one Authorization precedence tier (Domain Permission) that already had real, resolvable data as the Authorization Engine's own most natural first milestone.

Until that future Charter is prepared and accepted, WP-23 Workstream D remains formally deferred (§0/§5 above), and no further action on it is authorized by this document.

---

*End of IRA-BAE-001. This document records the Repository Owner's Option B decision and assesses constitutional readiness for a future Business Activity Engine Work Package. It does not charter that Work Package, does not register it in `WPR-001 §2a`, and does not authorize implementation of any deliverable. WP-23 Workstream D remains dependent on that future, not-yet-chartered Work Package. D1–D9 and BAR Workstreams A–C are unmodified by this document. No Business Activity was registered. C-024 BA-01 remains unregistered. Nothing staged, committed, or pushed.*
