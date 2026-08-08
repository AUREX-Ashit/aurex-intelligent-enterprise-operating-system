# IRA-RTA-001 — Authorization Runtime Engine Implementation Readiness Assessment

**Document ID:** IRA-RTA-001
**Work Package:** WP-RTA-001 (Runtime — no PE-001 capability)
**Constitutional Subject:** The Authorization Engine, `RTA-001 §3.8`/`§11`
**Methodology Applied:** `ADR-014`/`WP-METH-001` (`IMP-001 §6.2a` Mandatory Context Discovery, `§6.2b` Gap Analysis Category Scheme) — applied to a Runtime Component rather than a Business Capability, the first IRA in this repository to do so; deviations from the Business-Capability IRA shape are stated explicitly where they occur.
**Status:** Assessment and constitutional charter only. No implementation, no code, no API, no schema, no migration, no test is authorized by this document. This document authorizes **future** implementation planning (`WP-RTA-001`) — it does not itself constitute implementation readiness for any specific deliverable within that Work Package.

Treat the Git repository as the ONLY source of truth. Every claim below is sourced from `architecture/02-Constitutional/RTA-001 - Runtime Architecture and Execution.md` (§§1–3, 11, read in full), `architecture/02-Constitutional/URA-001 - User, Role, Permission, Event and ssignment.md` (URA-001-76), `architecture/07-Decisions/ADR-015_Access_Evaluation_Outcome_Canonical_Business_Object_Registration.md`, `architecture/05-Implementation/IRA-005_WP-05_Access_Management_Implementation_Readiness_Assessment.md`, `architecture/06-Reviews/AUTHORIZATION_ENGINE_CONSTITUTIONAL_RESPONSE.md`, `architecture/00-Governance/WPR-001_Work_Package_Roadmap.md`, `architecture/00-Governance/ARCH-000 – Enterprise Operating System Architecture Manifest.md`, and `architecture/06-Reviews/TECH-DEBT.md`. No claim is drawn from conversational memory.

---

## 1. Executive Summary

`IRA-005` (WP-05, C-002 Access Management) found, during its own readiness assessment, that C-002's central purpose (producing Permitted/Denied Access Evaluation Outcomes) depends on a URA-001-76 precedence-chain resolver — `RTA-001`'s own Authorization Engine — that exists nowhere in this repository and that no capability or Work Package claimed ownership of building. `IRA-005 §10.2 item 3` disclosed three options for resolving this and declined to choose among them, escalating the choice to the repository owner per `CLAUDE.md §18`'s STOP-and-report discipline. A subsequent Constitutional Review (`architecture/06-Reviews/AUTHORIZATION_ENGINE_CONSTITUTIONAL_RESPONSE.md`) of a candidate, unauthorized implementation independently reached the same conclusion and recommended Option 2 (a dedicated Runtime Work Package) on the evidence that `PE-001-C002 §1.5` affirmatively places the engine outside C-002's own scope and that the engine is a genuinely cross-capability dependency.

**The repository owner has now made that decision** (§5 below): the Authorization Engine is chartered as its own Runtime Work Package, `WP-RTA-001`, separate from any Business Capability Work Package. This IRA is the constitutional readiness assessment for that charter. It establishes the boundary of what `WP-RTA-001` is and is not, records the repository-owner decision, and identifies what must still be resolved before real implementation milestones (defined in `WP-RTA-001` itself) may begin — it does not begin implementation.

## 2. Purpose

To establish the constitutional foundation required before any Authorization Engine implementation may proceed: a chartered Work Package, a stated boundary distinguishing Runtime responsibilities from Business Capability responsibilities, and an explicit record of the repository-owner decision resolving `IRA-005 §10.2 item 3`.

## 3. Scope

**In scope for this IRA:** the constitutional charter itself — Work Package registration, Runtime/Business responsibility boundary, dependency identification, risk disclosure, and readiness assessment for beginning `WP-RTA-001`'s own future milestone-level planning.

**Out of scope for this IRA:** any implementation detail (service placement, endpoint shape, persistence mechanism, algorithm implementation). Those remain for `WP-RTA-001`'s own future, separately-scoped, milestone-level gap analyses, each subject to its own `CLAUDE.md §19` Implementation Start Checklist before code is written.

## 4. Constitutional Authority

| Authority | Role |
|---|---|
| `RTA-001 §3.8` | Names the Authorization Engine as a canonical Runtime Component. |
| `RTA-001 §11` (Authorization Runtime) | The full governing specification: purpose, architectural principle, runtime position, responsibilities, authorization context, resolution pipeline, decision taxonomy, assignment/delegation/approval-authority resolution, enterprise scope validation, collaboration, caching, observability, governance, and relationship to `URA-001`. |
| `URA-001-76` | Authorization Resolution Precedence — the five-tier order (Named User > Group > Approval Authority > Business Role > Domain Permission) the engine must implement. |
| `ADR-015` | Registers `AEO-000001` (Access Evaluation Outcome) as C-002's own Business Object; explicitly declines to resolve the Authorization Engine ownership question, leaving it to this decision. |
| `IRA-005 §9`/`§10.2` | First identified the ownership gap and disclosed the three resolution options. |
| `AUTHORIZATION_ENGINE_CONSTITUTIONAL_RESPONSE.md` | Independent Constitutional Review of the candidate implementation; recommended Option 2 (this charter) on repository evidence. |
| `ARCH-000` Layer model | Places `RTA-001` in Layer 1 (Enterprise Constitutional Architecture — defines) and implementation in Layer 4 (Implementation Specifications — requires its own chartering); `RTA-001`'s own text contains no self-authorizing "Work Package"/"charter" language (confirmed by direct search), consistent with implementation requiring a separate charter such as this one. |
| `CLAUDE.md §18`/`§19.4` | The STOP-and-report discipline this entire charter exists to satisfy. |

## 5. Repository Owner Decision

The repository owner has accepted the following constitutional decision, resolving `IRA-005 §10.2 item 3` as **Option 2**:

> "The Authorization Engine is a shared Runtime Engine. It is specified by RTA-001, owns no Business Objects, performs no Business Activities, and provides runtime authorization services to multiple Business Capabilities. Its implementation requires its own constitutional charter."

This decision:
- Rejects Option 1 (charter inside WP-05/C-002) — consistent with `PE-001-C002 §1.5`'s own explicit exclusion of the engine's decision-computation logic from C-002's scope.
- Selects Option 2 (a dedicated Runtime Work Package) — `WP-RTA-001`, registered in `WPR-001 §2a` (see §"Update WPR-001" in the accompanying Work Package document).
- Does not select Option 3 (WP-05 minimum scope only) as the *sole* path — WP-05's own already-unblocked minimum scope (BA-02, BA-04, BA-03's classification portion, BA-01's Unresolved/Deferred branches) remains independently available and is not foreclosed by this decision; it simply is not what resolves the Authorization Engine question.
- **Does not itself authorize any implementation.** Per `ADR-015`'s own precedent (registration does not imply readiness), this decision authorizes `WP-RTA-001`'s constitutional existence, not any specific deliverable's readiness to be built.

## 6. Dependencies

| Dependency | Nature | Status |
|---|---|---|
| `RTA-001 §11` | Governing specification the engine must conform to | Exists, LOCKED |
| `URA-001-76` | The precedence algorithm to implement | Exists |
| `AEO-000001` (`ADR-015`, C-002) | The Business Object whose Outcome Type the engine's decision populates — **consumed, never owned** | Registered; no Physical Implementation Mapping yet (`CMD-001 §26.7` Pending) |
| Domain Permission (WP-02, `domain_permission_registry`) | One precedence tier's real, existing data source | Exists and reusable |
| Approval Authority (WP-02) | Another precedence tier's data source — **no holder/membership linkage exists yet** (`TD-026`) | Exists as policy/catalog only; not resolvable end-to-end |
| Role/Permission (WP-02) | Business Role tier's partial data source — **no domain-scoping exists** (`BR-C003-02`, by design) | Exists but insufficient for this tier alone |
| Group / Group Membership | Named User tier's and Group tier's own precedence-chain input | **Does not exist anywhere in this repository** (`IRA-005 §8`; `IRA-003 §17` Governance Backlog Item) |
| `runtime_assignment_registry` | Named User tier's runtime-assignment *instance* data (distinct from `RuntimeAssignmentPolicy`, the governed policy, WP-02) | **Does not exist anywhere in this repository** |
| At least one real consuming Business Activity | `WP-RTA-001` produces decisions Business Activities consume (`RTA-001 §11.2`); it has no purpose evaluated in isolation | The most likely first consumer is WP-05 BA-01's Permitted/Denied branches, once WP-05's own scope is separately ready |

**A note on the Group/Named-User/Approval-Authority-linkage gaps:** these are canonical **data models**, not Runtime logic. Per Constitutional Principle 2 (§10 below — Runtime Engines own no Business Objects), `WP-RTA-001` does **not** charter itself to build these missing registries. Whichever capability's own governance ultimately owns them (most plausibly a future `URA-001`/C-003 extension, not decided here) must charter that separately. `WP-RTA-001` evaluates against these registries once they exist; it does not create them. This is stated explicitly, not assumed, per `CLAUDE.md §17`.

## 7. Out of Scope

- `AEO-000001`'s own lifecycle (Created → Preserved → {Superseded|Invalidated|Expired}) — owned by C-002/WP-05, never by `WP-RTA-001`.
- Any Business Activity of any capability (C-002, C-003, C-004, C-007, or any other).
- Business approvals, access requests, membership lifecycle, role lifecycle — each remains its owning capability's own concern.
- Building the Group model, `runtime_assignment_registry`, or an Approval-Authority holder/membership linkage (see §6 note above) — these are Business/canonical data model gaps belonging elsewhere.
- Any UI, frontend, or presentation-layer work.
- Migrating every existing WP-01–04 endpoint off the interim `PLATFORM_ADMIN` gate onto this engine in one pass — that migration, if and when it happens, is each endpoint's own capability's future decision, informed by this engine's existence, not mandated by this charter.

## 8. Runtime Responsibilities

Per `RTA-001 §11.4`, restated as this Work Package's own future scope (implementation deferred to `WP-RTA-001`'s own milestones — see the accompanying Work Package document):

- Permission Resolution
- Role Resolution
- Assignment Resolution
- Delegation Resolution
- Approval Authority Evaluation
- Enterprise Scope Validation
- Authorization Decision generation (`RTA-001 §11.8`: Allow / Deny / Conditional / Delegated / Escalated)
- Runtime Trace / Authorization Telemetry generation (`§11.15`)

## 9. Business Responsibilities

**None.** This is the central constitutional fact this charter exists to state plainly. The Authorization Engine:
- Owns no Business Object anywhere in `CMD-001`'s registry, including `AEO-000001` — that remains C-002's own.
- Performs no Business Activity of any capability.
- Is invoked by Business Capabilities (via their own Business Activities, per `RTA-001 §11.2`: *"Business Activities consume authorization decisions... Business Activities shall never implement authorization logic"*) — the relationship is strictly Business Capability → invokes → Runtime Engine, never the reverse.
- Access Evaluation Outcomes remain owned, created, preserved, superseded, invalidated, and expired exclusively by C-002 (`ADR-015`, `IRA-005 §11`) — `WP-RTA-001` computes the value that C-002's own Business Activity (BA-01) writes into its own record; `WP-RTA-001` never writes that record itself.

## 10. Constitutional Principles

These principles govern every Runtime Engine in this repository, not only the Authorization Engine — stated here because this is the first Runtime Work Package chartered under them, but binding on any future Runtime Work Package by the same reasoning.

1. **Runtime Engines are shared infrastructure.** `RTA-001 §2.3`/`§3.3` define a fixed set of Runtime Execution Platform components (Business Activity Engine, Workflow Engine, Authorization Engine, Metadata Engine, Enterprise Relationship Engine, Event Bus, Knowledge Graph Engine, AI Runtime Engine, Notification Engine, Audit Engine, Observability Platform, Integration Gateway, Persistence Services, Caching Services) — none is capability-specific by design.
2. **Runtime Engines own no Business Objects.** Confirmed directly for the Authorization Engine: `AEO-000001` belongs to C-002, not to `RTA-001 §11`. No Runtime Component appears anywhere in `CMD-001`'s Business Object registry.
3. **Runtime Engines implement no Business Activities.** `RTA-001 §11.2`: *"Business Activities shall never implement authorization logic... The Authorization Engine is the sole authority for runtime authorization decisions."* The inverse holds equally: the Authorization Engine never performs a Business Activity.
4. **Runtime Engines execute runtime policies.** `RTA-001 §11.16`: *"Only authorization artifacts governed under URA-001 may participate in runtime execution."* The engine executes policy; it does not author policy.
5. **Business Capabilities remain the owners of Business Objects and Business Activity lifecycles.** C-002 owns `AEO-000001`'s full lifecycle; C-003 owns Role/Permission; C-004 owns Organization; C-007 owns Membership — none of this is reassigned by `WP-RTA-001`'s existence.
6. **Runtime Engines may be reused by multiple Business Capabilities.** `IRA-005 §11`'s own Relationship Mapping already anticipates C-003, C-004, and C-008 will each eventually consume `AEO-000001` (and, transitively, this engine's decisions) as an Entry Context precondition (Contract 5.6) — one engine, many future consumers, never rebuilt per capability.
7. **Runtime Engines require explicit constitutional authorization before implementation.** This is exactly the gap `IRA-005` found and this charter closes — `CLAUDE.md §18`/`§19.4`'s STOP-and-report discipline applies identically to Runtime Components as to Business Capabilities; no exception exists in `RTA-001`'s own text for self-authorizing implementation (confirmed by the zero "Work Package"/"charter" references noted in §4 above).

## 11. Assumptions

- URA-001-76's five-tier precedence order is assumed correct and complete as the algorithm to implement — it is canonical text, not a design choice this IRA introduces.
- The engine's eventual service/module placement (embedded within an existing service, a standalone microservice, or a shared library) is **not** assumed here and is explicitly deferred to `WP-RTA-001`'s own future milestone-level design, informed by `CLAUDE.md §8`'s service-boundary rules at that time.
- Existing interim `PLATFORM_ADMIN`-only gating (WP-00 convention, reused by every WP-01–04 write endpoint) is assumed to remain the operative gate for those endpoints until each capability separately decides to adopt this engine — `WP-RTA-001` does not assume a mandatory, repository-wide cutover.

## 12. Risks

| Risk | Description | Disposition |
|---|---|---|
| Precedence-tier data gaps | Four of five tiers (Named User, Group, Approval Authority, Business Role) have no resolvable data source anywhere in this repository today (§6) | Engine must report each honestly as unresolved rather than fabricating a match — mirrors the disclosure discipline the discarded candidate code already demonstrated correctly |
| False-Permitted security defect | A stubbed or approximated decision risks a false `ALLOW`, which `CLAUDE.md §19.8.5` prohibits deferring as ordinary Technical Debt | Every milestone gap analysis must explicitly verify no tier can produce a fabricated match |
| Service-boundary ambiguity | `RTA-001` does not specify where the engine physically lives | Deferred explicitly to future milestone design, not decided by this charter (§11) |
| Enterprise Scope Validation complexity | `RTA-001 §11.12` requires the engine never evaluate outside Enterprise Context; no existing precedent in this repository implements cross-tenant scope validation at this layer | Flagged as its own future milestone (see `WP-RTA-001` Deliverables) |
| Broad migration risk | If/when existing WP-01–04 endpoints adopt this engine as their `IMP-API-002` gate, that is a cross-cutting change touching already-certified code | Explicitly out of this charter's scope (§7); each capability's own future, separately-scoped decision |

## 13. Technical Debt

This IRA creates no new Technical Debt (it authorizes no implementation). It references existing, already-tracked entries relevant to `WP-RTA-001`'s eventual work:

- `TD-021` through `TD-025`, `TD-031`, `TD-034`–`TD-036`, `TD-039`, `TD-042` — the repository-wide interim `PLATFORM_ADMIN`-only gate class every prior Work Package's write endpoints use; relevant background for any future decision on migrating a capability's endpoint onto this engine.
- `TD-026` — Approval Authority carries no holder/membership linkage; blocks that precedence tier.
- `IRA-003 §17` / `IRA-005 §8` Governance Backlog Item — the Group/Group Membership model gap; blocks that precedence tier.

## 14. Success Criteria

`WP-RTA-001`'s constitutional charter (this IRA plus the accompanying Work Package document plus the `WPR-001` registration) is successful when:

- The Work Package is registered in `WPR-001 §2a` with Status = Planned.
- The Runtime/Business responsibility boundary is stated unambiguously (§9 above) and does not contradict `ADR-015`, `IRA-005`, or `RTA-001 §11.2`.
- No implementation, schema, API, or code exists as a result of this charter (verified: this document, `WP-RTA-001`, and the `WPR-001` update are the only artifacts created).
- A future implementer can begin milestone-level planning without needing to re-derive the ownership question this IRA and its predecessor documents already resolved.

## 15. Implementation Readiness Assessment

**This charter does not itself make any specific deliverable implementation-ready.** Per `IMP-001 §6.2b`'s Gap Analysis category scheme (applied here to a Runtime Work Package rather than a Business Activity, by direct analogy):

- The **constitutional** question (who owns this, under what charter) — **now resolved** by §5's repository-owner decision. This was the Category D/bordering-E blocker `IRA-005 §7` identified; it is closed by this document.
- Every **implementation-level** question (service placement, precedence-tier data availability, gate-wiring strategy, persistence for observability/trace data) remains open and is deliberately **not** resolved here — each requires its own future, milestone-scoped gap analysis before code is written, per `CLAUDE.md §19`'s Implementation Start Checklist, applied fresh at that time.

**Readiness Decision: Constitutionally READY to exist as a Work Package. NOT READY for any implementation milestone** — each milestone in `WP-RTA-001`'s own Deliverables section requires its own separate readiness gate.

## 16. Recommendation

Register `WP-RTA-001` in `WPR-001 §2a` per §5's decision, using the accompanying Work Package document (`WP-RTA-001_Authorization_Runtime_Engine.md`) to define milestones only. Do not begin implementation of any milestone until that milestone has its own gap analysis, consistent with every prior Work Package's own precedent (WP-01 through WP-04, each gated Business-Activity-by-Business-Activity under `CLAUDE.md §19.7`). The most natural first milestone to gap-analyze, once this charter is accepted, is the precedence evaluator against the one precedence tier that already has real, resolvable data (Domain Permission) — mirroring how the discarded candidate code's own structure (honestly reported `NOT_EVALUATED` tiers, real Domain Permission resolution) already demonstrated the correct shape, without carrying forward its fabricated `WP-RTA-001`/`IRA-RTA-001` identity or its lack of authorization.

---

*End of IRA-RTA-001. This document charters `WP-RTA-001`'s constitutional existence. It does not authorize implementation of any deliverable within it.*
