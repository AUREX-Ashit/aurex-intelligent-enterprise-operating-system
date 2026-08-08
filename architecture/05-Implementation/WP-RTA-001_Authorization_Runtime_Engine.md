# WP-RTA-001 — Authorization Runtime Engine

**Work Package ID:** WP-RTA-001
**Type:** Runtime (not a Business Capability Work Package)
**Parent Architecture:** Runtime Architecture (`RTA-001 §3.8`/`§11`)
**Capability:** None — a Runtime Component serves multiple Business Capabilities; it is not owned by one (`IRA-RTA-001 §9`)
**Status:** IMPLEMENTATION COMPLETE — Milestones M1–M6 implemented (106 passing unit tests at `Backend/Runtime/AuthorizationEngine/`). Not yet independently reviewed, certified, or committed — per `CLAUDE.md §19.7`, this Work Package is not considered *complete* until an independent, fresh-context reviewer performs that review and certification; this status marks implementation, not closure. The milestone sequence below has been updated twice to match what was actually delivered — see the note at the top of §"Deliverables."
**Governing IRA:** `IRA-RTA-001_Authorization_Runtime_Engine_Implementation_Readiness_Assessment.md`
**Governing Implementation Report:** `IMP-REPORT-WP-RTA-001_Authorization_Runtime_Engine.md` (M1–M4 detail: design decisions, files, tests, Technical Debt)
**This document defines milestones only. No implementation, API, schema, migration, or test is created by this document.**

---

## Purpose

Implement and operate the Authorization Engine Runtime Component specified by `RTA-001 §3.8`/`§11`, so that any Business Capability may obtain a centralized, deterministic, non-fabricating runtime authorization decision without implementing authorization logic itself (`RTA-001 §11.2`: *"Business Activities shall never implement authorization logic. The Authorization Engine is the sole authority for runtime authorization decisions."*).

## Objectives

1. Implement `URA-001-76`'s five-tier Authorization Resolution Precedence (Named User > Group > Approval Authority > Business Role > Domain Permission) as a real, structurally complete evaluator that never fabricates a match for a tier it cannot resolve.
2. Provide Enterprise Scope Validation per `RTA-001 §11.12` — authorization is never evaluated outside a resolved Enterprise Context.
3. Provide Assignment, Delegation, and Approval Authority evaluation once each tier's own owning data model exists elsewhere in the repository (`IRA-RTA-001 §6` — this Work Package does not build those data models itself).
4. Generate deterministic, reproducible Authorization Decisions (`RTA-001 §11.8`: Allow / Deny / Conditional / Delegated / Escalated) with a full Runtime Trace supporting explainability (`§11.15`; `PE-001-C002 Contract 5.7`'s own explainability standard).
5. Serve as the mandatory pre-execution gate (`IMP-001 §8`, `IMP-API-002`) for any Business Activity that adopts it — on that Business Activity's own, separately-scoped decision, never mandated in bulk by this Work Package.

## Scope

**In scope:** the Runtime evaluation mechanism itself — see §"Implementation Boundary" below for the exhaustive list.

**Out of scope:** anything belonging to a Business Capability's own Business Object or Business Activity lifecycle — see §"Implementation Boundary" below. Also out of scope: building the Group model, `runtime_assignment_registry`, or an Approval-Authority holder/membership linkage (`IRA-RTA-001 §6`/`§7`) — these are canonical data-model gaps belonging to whichever capability's own governance ultimately claims them, not to this Runtime Work Package.

## Runtime Responsibilities

Per `RTA-001 §11.4`:

| Responsibility | Runtime Capability |
|---|---|
| Permission Resolution | Authorization Engine |
| Role Resolution | Authorization Engine |
| Assignment Resolution | Authorization Engine |
| Delegation Resolution | Authorization Engine |
| Approval Authority Evaluation | Authorization Engine |
| Enterprise Scope Validation | Authorization Engine |
| Authorization Context Construction | Business Activity Engine (consumed by, not performed by, this Work Package) |
| Authorization Telemetry | Observability Platform (this Work Package emits into it, per `§11.15`) |

## Interfaces

**Input** (per `RTA-001 §11.5`, Authorization Context, constructed by the Business Activity Engine and handed to this engine — never assembled by the engine itself): Identity, Organization, Membership, Roles, Permissions, Assignments, Delegations, Approval Authorities, Enterprise Scope, Security Classification, Session Information, Effective Time. The Authorization Context is immutable throughout evaluation (`§11.5`).

**Output** (per `RTA-001 §11.8`): One Authorization Decision — Allow, Deny, Conditional, Delegated, or Escalated — plus a Runtime Trace (per-tier resolution result and reason, supporting `§11.15` Authorization Observability and `PE-001-C002 Contract 5.7`'s explainability requirement). The invoking Business Activity consumes this decision; it does not interpret authorization policy itself (`§11.8`: *"They do not interpret authorization policies."*).

**Collaboration** (per `RTA-001 §11.13`): Identity Service, Metadata Engine, Enterprise Relationship Engine, Business Activity Engine, Workflow Engine, Audit Engine, Observability Platform. Business Activities receive an Authorization Context rather than invoking this engine's own internals directly.

## Dependencies

See `IRA-RTA-001 §6` for the full table. Summarized: `RTA-001 §11` (specification), `URA-001-76` (algorithm), `AEO-000001`/`ADR-015` (the Business Object this engine's decision informs — consumed, never owned), Domain Permission (WP-02, the one precedence tier with real existing data), Approval Authority/Role/Permission (WP-02, partially usable), Group/Named-User-Assignment data models (do not exist; not built by this Work Package), and at least one real consuming Business Activity (most likely WP-05 BA-01's Permitted/Denied branches, once separately ready).

## Deliverables

**Note (charter updated to match reality — second pass):** M1–M5 below describe what was actually implemented. The first charter-synchronization pass already reconciled M1–M4 (original M2/Enterprise Scope Validation and M4/Runtime Observability were not delivered as their own milestones; actual M2 = Runtime Resolver Framework, M3 = Runtime Evaluation Pipeline, M4 = Runtime Integration Adapters) and consolidated the remainder into M5 (Runtime Completeness — Enterprise Scope Validation + Observability, both since implemented) and a planned M6 (Real Tier Resolution, First Consumer Integration & Caching). **M6 diverged again**: the repository owner closed this Work Package with a Production Readiness / Hardening / Closure milestone instead of the previously-planned Real Tier Resolution / First Consumer / Caching content. That content was never delivered under any milestone number and is **not part of this Work Package's own scope as closed** — it is recorded in `IMP-REPORT-WP-RTA-001` M6's own Closure Report as Remaining External Dependencies for a future, separately-scoped initiative (no such initiative is chartered by this document; per `CLAUDE.md §17`, none is invented here). This is consistent with this document's own original Exit Criteria, which always permitted the externally-blocked tiers to "remain permanently deferred and disclosed as such."

| Milestone | Description | Precondition | Status |
|---|---|---|---|
| M1 — Authorization Evaluation Core | The evaluation pipeline, `AuthorizationContext`/`EvaluationResult`/`TierEvaluation` models, and the precedence skeleton over `URA-001-76`'s five tiers — every tier honestly reported (`NOT_EVALUATED`/`NO_MATCH`/`MATCH`), never a fabricated match. No concrete tier resolution, no consumer. | This charter accepted | **Implemented** |
| M2 — Runtime Resolver Framework & Tier Resolution | A dedicated, canonically-verified interface per `URA-001-76` tier (`NamedUserResolver`, `GroupResolver`, `ApprovalAuthorityResolver`, `BusinessRoleResolver`, `DomainPermissionResolver`) and `ResolverRegistry`, the injectable, fail-fast assembly mechanism. | M1 | **Implemented** |
| M3 — Runtime Evaluation Pipeline & Resolver Orchestration | `ResolverOrchestrator` (resolver discovery/assembly/introspection) and `EvaluationPipeline` (the stable entry point, wrapping the still-unmodified M1 engine, with the `PipelineObserver` extension seam for future audit/persistence/metrics/tracing — Caching found in M6 to require a different, wrapper-based seam, `TD-078`). | M1, M2 | **Implemented** |
| M4 — Runtime Integration Adapters | `AuthorizationAdapter`/`AuthorizationRequest` in a new, separate `adapters/` package — the stable interface a future Business Activity depends on, structurally and test-enforced one-way dependent on the runtime, never the reverse. No Business Activity wired to it yet. | M1–M3 | **Implemented** |
| M5 — Runtime Completeness (Enterprise Scope Validation & Observability) | `EnterpriseScopeValidator` (`§11.12`, wired into `EvaluationPipeline` before evaluation begins — a disclosed placement simplification relative to `§11.7`'s literal step order, `TD-077`) and `RuntimeObservabilityCollector` (a concrete `PipelineObserver` realizing a first, self-contained slice of `§11.15`'s telemetry set, `TD-075`). | M1–M4 | **Implemented** |
| M6 — Production Readiness, Hardening & Work Package Closure | Runtime Contract Verification (18 new contract-stability tests), Performance Validation (5 benchmark tests, no optimization required), Concurrency/Thread-Safety Validation (6 tests), Extension Point Validation (found Caching requires a wrapper, not `PipelineObserver` — `TD-078`), Package Hardening (dead-code/unused-import audit — none found; one M4 test defect found and fixed in M5, re-verified here), and full Documentation Synchronization. **This Work Package's own closure — see `IMP-REPORT-WP-RTA-001` M6's Closure Report.** Real Tier Resolution, First Consumer Integration, and Caching (this row's own original content, per the first charter-synchronization pass) were **not** delivered under this or any milestone — recorded as Remaining External Dependencies, not silently dropped. | M1–M5 | **Implemented (as Hardening & Closure — not as originally planned; see note above)** |

## Acceptance Criteria

- All five `URA-001-76` tiers are evaluated in canonical order for every request; no tier is silently skipped.
- No tier ever produces a fabricated `ALLOW` for data it cannot actually resolve (`CLAUDE.md §19.8.5`).
- Enterprise Scope Validation is enforced (`§11.12`) before any decision is returned.
- The decision taxonomy matches `RTA-001 §11.8` exactly; unreachable values (`CONDITIONAL`/`DELEGATED`/`ESCALATED`, pending Delegation/Approval Authority runtime mechanics) are declared for structural completeness without fabricated behavior.
- At least one real Business Capability's Business Activity gates through this engine per `IMP-API-002` (not merely a standalone, uncalled endpoint).
- Independent Review and Independent Certification performed per `CLAUDE.md §19.7`, by a genuinely independent reviewer, before any milestone is considered complete.

## Exit Criteria

`WP-RTA-001` is complete when:
- Every milestone in §"Deliverables" has been implemented (M1–M6, all six ✓) and independently reviewed and certified (pending — see `IMP-REPORT-WP-RTA-001` M6's own Closure Report).
- Real tier resolution for Named User/Group/Approval-Authority/Business-Role (blocked on data models external to this Work Package), first real Business Activity consumer integration, and Authorization Caching **remain permanently deferred, disclosed as Remaining External Dependencies rather than silently dropped** — this Work Package's own closure does not require capabilities this repository has not yet chartered to build, per this Exit Criteria's own original permission. None of the three is scheduled under any current or future milestone of this Work Package; a future, separately-scoped initiative would take them up, not invented or chartered here.
- `RTA-001 §11.2`'s own principle that the engine exists to be consumed, not to exist in isolation, is **not yet satisfied** — no Business Capability consumes this engine's decisions in production use. This is disclosed as a known limitation of the closed Work Package, not a blocking Exit Criterion this document retroactively waives.

---

## Runtime Dependency Model

```
Business Capability
        │  (e.g., C-002 Access Management, C-003 Role & Permission Management)
        │  owns its own Business Objects and Business Activities
        ▼
Business Activity
        │  (e.g., WP-05 BA-01 — Evaluate Access for a Governed Request)
        │  constructs an Authorization Context (RTA-001 §11.5) and
        │  invokes the Runtime Engine; never implements authorization logic itself
        ▼
Authorization Runtime Engine  (WP-RTA-001)
        │  evaluates URA-001-76's five-tier precedence chain;
        │  returns one Authorization Decision + Runtime Trace;
        │  owns no Business Object, performs no Business Activity
        ▼
Repositories
        │  read-only access to each precedence tier's own data
        │  (Domain Permission, Role/Permission, Approval Authority, Group,
        │  Named User Assignment) — each owned by its own Business Capability,
        │  never by this engine
        ▼
Persistence
        │  Persistence Services (RTA-001 §3.18) — the underlying data store
        │  each Repository above reads from; this engine writes nothing to
        │  Business Object storage (AEO-000001 remains C-002's own write path)
        ▼
Audit
        │  Audit Engine (RTA-001 §3.15, §11.13) — every Authorization Decision
        │  is auditable; this engine emits to the Audit Engine, it does not
        │  implement its own separate audit mechanism
        ▼
Events
        │  Event Bus (RTA-001 §3.11) — authorization-relevant state changes
        │  (e.g., a Role or Domain Permission grant changing) are consumed
        │  by this engine's own cache-invalidation logic (§11.14) via events
        │  published by the owning capability, never authored by this engine
```

**Layer responsibilities, stated plainly:**
- **Business Capability** — owns identity, meaning, and lifecycle of its own Business Objects (e.g., `AEO-000001`, Role, Domain Permission).
- **Business Activity** — the business-meaningful unit of work that needs an authorization decision to proceed; constructs the Authorization Context and consumes the decision; never computes the decision itself.
- **Authorization Runtime Engine** (this Work Package) — the sole authority computing the decision; stateless with respect to Business Object ownership; every output is a decision plus a trace, never a Business Object write.
- **Repositories** — the existing, capability-owned data-access layer this engine reads through (reused, per `IRA-RTA-001 §11`'s Assumptions — never reimplemented by this engine).
- **Persistence** — the underlying store; this engine has no persistence layer of its own — M5 delivered Observability entirely in-memory (`TD-075`), and Caching (originally anticipated here) was not delivered under any milestone of this Work Package (see §"Deliverables" M6's own note) and remains subordinate to whichever future initiative eventually builds it.
- **Audit** — every decision is auditable via the existing Audit Engine, not a parallel logging mechanism this Work Package invents.
- **Events** — this engine reacts to authorization-relevant events (for cache invalidation, `§11.14`) published by the capabilities that own the underlying data; it does not publish Business Events of its own, since it produces no Business Object.

---

## Implementation Boundary

**WILL be implemented under `WP-RTA-001`** (future milestones, per §"Deliverables" above — not implemented by this document):

- Authorization evaluation (the overall decision-computation act)
- Resolution precedence (`URA-001-76`'s five-tier chain)
- Enterprise scope validation (`RTA-001 §11.12`)
- Assignment authority evaluation (once its data model exists elsewhere)
- Delegation evaluation (once its data model exists elsewhere)
- Approval authority evaluation (once its holder/membership linkage exists elsewhere, closing `TD-026`)
- Decision generation (`RTA-001 §11.8`'s five-value taxonomy)
- Runtime trace generation (`§11.15` Authorization Observability; explainability per `PE-001-C002 Contract 5.7`)

**WILL NOT be implemented under `WP-RTA-001`** — each belongs to its own Business Capability:

- Access Evaluation Outcome (`AEO-000001`) lifecycle — C-002/WP-05
- Business approvals — the owning capability's own Approval Authority mechanism (WP-02/C-003 policy; execution, if ever built, is a separate future capability concern)
- Access requests — whichever capability originates the governed request being evaluated
- Membership lifecycle — C-007/WP-03
- Role lifecycle — C-003/WP-02
- Business policy ownership — every precedence tier's own governing policy remains owned by its issuing capability; this engine only evaluates against it, never authors or amends it

---

*End of WP-RTA-001. This document defines Work Package scope and milestones only. No implementation begins as a result of this document.*
