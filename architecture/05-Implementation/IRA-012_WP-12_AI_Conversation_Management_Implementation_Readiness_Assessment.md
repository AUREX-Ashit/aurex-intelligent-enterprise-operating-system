# IRA-012 — WP-12 AI Conversation Management (C-094) — Implementation Readiness Assessment

**Document ID:** IRA-012
**Work Package:** WP-12
**Capability:** C-094 — AI Conversation Management ("Manage AI interactions," `CAP-001`, Planned, D-005)
**Governing Specification:** No dedicated `PE-001-C094` capability specification exists (`docs/Product/PE-001/capabilities/` contains specifications through C-040 only, confirmed by `IRA-011 §0`'s own identical finding for C-093, unchanged since). This IRA is grounded directly in `RTA-001 §13.15a` (AI Session Management — Conversation, Interaction, Handoff), `SD-001 §16` (AI-Native Enterprise Experience Framework), `ADR-020`, `ADR-021`, and `ADR-022` (Conversational Experience) — mirroring `IRA-011`'s own precedent of grounding a Gap Analysis in Locked/Active constitutional text when no dedicated capability docx exists.
**Status:** DRAFTED — pending Repository Owner review and a separate implementation authorization, per the two-step chartering-then-authorization precedent `WP-10`/`WP-11` each established. **No Business Activity code, API, or architecture change is authorized by this document.**
**Prepared By:** Engineering Governance session (Claude Code), under Repository Owner Instruction "Release D — WP-12 Implementation Charter (Execution Mode)"
**Date:** 2026-08-07

---

## 1. Purpose

Determines whether, and at what scope, WP-12 (C-094 AI Conversation Management) may proceed to implementation, per `CLAUDE.md §19`/`§20`/`§21`. This IRA produces **two** implementation plans — **Plan A** (Business Capability Implementation, §5) and **Plan B** (Enterprise Experience Implementation, §7) — neither of which designs screens or writes code; both are planning determinations only. This IRA also performs the three pre-Business-Activity reviews `CLAUDE.md §21.3` requires: Strategic Enhancement Review (§4a), Historical Screen Review (§4b), Executive Cognition Review (§4c).

**This IRA's central finding, stated up front:** the constitutional foundation for C-094 (`ADR-020`, `ADR-021`, `ADR-022`) is complete and internally consistent, independently re-verified against `RTA-001 §13.15a` and `IMP-001 §13.26–53` in this pass, not accepted on trust. Two of the three governing ADRs are not yet migrated into their own canonical host documents (`SD-001 §16` currently ends at `SD-001-118`; `ADR-022`'s own three decisions exist only as an approved, uncommitted ADR) — classified as Repository Completion Work, not an implementation blocker, per Repository Owner direction, and cited directly from the ADRs themselves throughout this document. **One previously-undisclosed gap materially affects Plan B's own scope**, found independently during this pass: `SER-001 SE-001` and `SE-007` already disclose that Progressive Disclosure and the Evidence Panel — the exact `SD-001` contracts `ADR-021`/`ADR-022` require Conversational Experience to compose rather than reinvent — have **zero conforming frontend implementation anywhere in this repository**. See §4.4.

---

## 2. Governing Documents Reviewed

- `CAP-001_Enterprise_Capability_Registry.md` (C-094 registration, verbatim: "Manage AI interactions," Planned, D-005).
- `RTA-001 §13.15a` (AI Session Management) — Conversation/Interaction definition, Conversation Boundary/State Model, System of Record, Interaction State and Continuity, Cross-Lifecycle Agent Handoff; `§13.12a` (Ask User Gate); `§13.6a`/`§13.6e` (Agent Execution Lifecycle, Capability Delegation) — all read directly.
- `SD-001 §16` (AI-Native Enterprise Experience Framework, `SD-001-113`–`118`) — Definition/Scope, Accountability Boundary, Workspace relationship, Composition Model, Contract-reuse discipline, Capability-layer adoption model.
- `ADR-020`, `ADR-021`, `ADR-022` — full text of each read directly; every Decision and Constitutional Principle cited below traces to a specific one of the three, not restated from memory.
- `IMP-001 §§13.26–53` (AI Session Management Engineering, AI-Native Enterprise Experience Engineering) — `ConversationService`/`InteractionService`, `ConversationStateResolver`, `SessionRecordRepository`, `InteractionStateAssembler`, `SessionHandoffResolver`, `ExperienceCompositionResolver`, `ExperienceAccountabilityGuard`, `ExistingContractRegistry`, `ExperienceWorkspaceBinding` — engineering patterns only, zero code, confirmed by repository-wide search.
- `SER-001_Strategic_Enhancement_Register.md` (`SE-001`, `SE-007`, `SE-008`, `SE-037`, `SE-064`, `SE-065`).
- `IRA-011_WP-11_Enterprise_Search_Implementation_Readiness_Assessment.md` — the direct structural and evidentiary precedent this IRA follows; every reused asset below (`AIService` authentication, Alembic chain, existing router pattern) traces to WP-11's own implementation record, not re-derived.
- Existing repository source, read directly: `Backend/Services/AIService/` in full — `dependencies.py` (WP-11's own real JWT verification, the reuse target for WP-12's own authorization), `alembic/` (the existing chain WP-12 extends, not bootstraps a second time), `services/search_execution_service.py` (the nearest existing precedent for a service composing `RAGEngine`-adjacent orchestration against real persistence); `source/frontend/src/config/admin-navigation.ts` (nav slot survey).

---

## 3. Existing Asset Discovery (Reuse Before Creating, `CLAUDE.md §19.2`)

| Asset | Location | Status |
|---|---|---|
| `RTA-001 §13.15a` (Conversation, Interaction, Boundary, System of Record, Continuity, Handoff) | `RTA-001` | Fully specified, constitutional. Zero code — this Work Package is the first to implement any of it. |
| `SD-001 §16` / `ADR-021`/`ADR-022` (Composition Model, Conversational Experience turn model, contract-reuse obligation) | `SD-001` / two ADRs | Fully specified, constitutional. Zero code. |
| `ConversationService`/`InteractionService`, `ConversationStateResolver`, `SessionRecordRepository`, `InteractionStateAssembler`, `SessionHandoffResolver` | `IMP-001 §13.26–38` | Engineering patterns fully specified (conceptual interfaces, dependency-injection shape). Zero implementation — no class, no file, confirmed by repository-wide search of `Backend/Services/AIService`. This is the real target Plan A builds against. |
| `ExperienceCompositionResolver`, `ExperienceAccountabilityGuard`, `ExistingContractRegistry`, `ExperienceWorkspaceBinding` | `IMP-001 §13.39–53` | Same — fully specified, zero implementation. |
| `AIService` real authentication (`get_current_claims`-equivalent JWT verification) | `Backend/Services/AIService/dependencies.py` | **Exists, real, already built by WP-11.** Directly reused — no second bootstrap required. |
| `AIService` Alembic chain | `Backend/Services/AIService/alembic/` | **Exists, real, already built by WP-11** (`d4a9c1e7f3b5`, first-ever migration). WP-12 adds new migrations to this existing chain; does not bootstrap a second one. |
| `RAGEngine`, `DocumentChunkRegistryVectorProvider` | `Backend/Services/AIService/services/` | Exist, real (WP-11). Not directly reused by WP-12's own core loop (Conversation/Interaction execution is a distinct concern from Search's own retrieval), but the *pattern* — a domain service composing an existing Reasoning Engine resolution against real persistence — is the direct structural precedent for `InteractionService`'s own implementation. |
| Ask User Gate (`RTA-001 §13.12a`) | `RTA-001` | Fully specified, constitutional. Zero code anywhere in the repository — no Work Package has implemented it yet. |
| Progressive Disclosure (`SD-001-021`/`IMP-001 §10.3`), Evidence Panel (`SD-001-020`/`IMP-001 §10.4`), Confidence | `SD-001` / `IMP-001` | Fully specified, mandatory-reuse component contracts (`SD-001-117`, `ADR-021` Decision 5/`ADR-022` Decision 3). **`SER-001 SE-001`/`SE-007` confirm zero conforming implementation exists repository-wide.** WP-12 cannot compose what has never been built. See §4.4. |
| `source/frontend/src/config/admin-navigation.ts` | `source/frontend/src/config/` | Exists. No `AI Conversation`/`C-094`-related nav slot found by direct search — unlike WP-11's own `enterprise-intelligence` placeholder, no existing slot exists for this capability at all. |

**Conclusion:** per `CLAUDE.md §2`/`§19.5` (Reuse → Configure → Extend → Compose → Create), Plan A implements the `IMP-001 §13.26–53` patterns for the first time — necessary and expected, since Session Management and Experience Framework engineering exist specifically to be implemented by the first capability that needs them, per `IMP-001 §13.17`'s own extension-point design. `AIService`'s own authentication and Alembic infrastructure are reused wholesale from WP-11, zero rebuild. Plan B cannot reuse Progressive Disclosure/Evidence Panel because neither has ever been built — WP-12 becomes their first real implementation, addressed in §4.4 as a disclosed, in-scope prerequisite, not new architecture (both are already fully specified contracts).

---

## 4. Gap Analysis

### 4a. Strategic Enhancement Review (`CLAUDE.md §21.3`)

| SE | Enhancement | Disposition for WP-12 |
|---|---|---|
| `SE-001` | Progressive Disclosure four-state widget contract | **Partially Implemented by this Work Package** — WP-12 is the first capability to build a conforming instance, scoped to Conversational Experience turns specifically (§4.4); the cross-cutting rollout to every existing WP-01–WP-11 screen remains separately tracked, unchanged |
| `SE-007` | AI Explainability components — Evidence Panel, Confidence Indicator, Source Citation | **Partially Implemented by this Work Package**, same reasoning — first real instance, scoped to Interaction outputs within a Conversation |
| `SE-008` | AI transparency interaction sequencing | **Not Applicable to this Work Package's own minimum scope** — sequencing beyond a single Interaction's own Evidence display is not required for WP-12's own BA-01/02/03; remains Deferred |
| `SE-037` | C-094 AI Conversation Management charter | **Implemented by this Work Package** — this IRA is that charter's own realization, per its own dependency ("WP-11 succeeding," already met) |
| `SE-064` | AI Session Management constitutional foundation | Consumed, not re-implemented — `RTA-001 §13.15a`/`IMP-001 §13.26–38`, engineered for the first time by this Work Package's own Plan A |
| `SE-065` | AI-Native Enterprise Experience Framework | Consumed, not re-implemented — `SD-001 §16`/`IMP-001 §13.39–53`, same reasoning |

No `SER-001` item names a C-094-specific deliverable this Gap Analysis has not already accounted for.

### 4b. Historical Screen Review (`CLAUDE.md §21.3`)

No entry in `HISTORICAL-SCREEN-REALIZATION-MATRIX.md` names a C-094-owned or Conversation-specific historical screen concept (confirmed by direct search — the two entries touching D-005, `F1`/`I1`, are C-090/C-090-092-093-owned respectively, both already excluded from WP-11's own scope per `IRA-011 §4b`, neither maps to Conversation Management). Plan B (§7) is therefore not constrained or informed by historical precedent, only by `DS-001`/`SD-001 §16`/`PE-001` directly — the same conclusion `IRA-011 §4b` reached for Search.

### 4c. Executive Cognition Review (`CLAUDE.md §21.3`)

Per `PRODUCT-MILESTONE-ROADMAP.md §3` (Milestone 3, "Executive Cognition") and `EIA-001 Volume I`'s own Access → Converse layering (cited directly in `IRA-011 §4c` and the Release C Initiation Summary): C-094 is the first capability in the "Converse" layer, gated behind — and now unblocked by — WP-11's own successful closure (the "Access" layer's proving Work Package). This is a genuine, first-of-kind advance: an Executive persona sustaining a multi-turn exchange, not a single query/response. `C-095` (Enterprise Memory) remains correctly excluded and gated behind its own separate `ARCH-000 §7c` deferral-lift decision, unaffected by this IRA.

### 4.1 Establish and Manage Conversation Lifecycle — **IN SCOPE**

`RTA-001 §13.15a`'s Conversation construct and Conversation State Model (`ADR-020` Decisions 1–2) are fully specified; `IMP-001 §13.28`'s `ConversationService` and `§13.29`'s `ConversationStateResolver` give the exact engineering shape. A real, buildable target with zero existing conflicting implementation.

**Disposition:** in scope, buildable now — realized as **BA-01**.

### 4.2 Execute Interaction — **IN SCOPE**

`RTA-001 §13.15a`'s Interaction construct (one bounded AI Request Lifecycle, `§13.6`) and Interaction State/Continuity (`ADR-020` Decision 4) are fully specified; `IMP-001 §13.30`'s `InteractionStateAssembler` gives the exact composition shape, explicitly barred from any `MemoryRepository` dependency (structural, not runtime-checked). This is C-094's own core deliverable — the actual "converse" loop.

**Disposition:** in scope, buildable now — realized as **BA-02**.

### 4.3 Retrieve Conversation — **IN SCOPE (new, added by this IRA)**

Neither the charter-equivalent constitutional decisions (`ADR-020`/`ADR-021`/`ADR-022`) nor `IMP-001 §13.26–53` name a distinct "retrieve" operation, but `ADR-022` Decision 1's own preservation obligation ("identity, ordering, and accountability") has no way to be demonstrated without one — a Conversation with no way to list its own Interactions in order cannot show continuity at all. This mirrors `IRA-011 §4.2`'s own reasoning for adding BA-03 there: the smallest addition that makes the other two Business Activities genuinely demonstrable rather than write-only.

**Disposition:** in scope, narrow — realized as **BA-03** (new). Excluded: any cross-Conversation search, filtering, or aggregation (`ADR-022` Decision 3 explicitly forbids Conversation-level aggregation) — this BA lists one Conversation's own Interactions, in order, nothing more.

### 4.4 Progressive Disclosure / Evidence Panel First Implementation — **IN SCOPE, mandatory, narrow prerequisite**

`SER-001 SE-001` and `SE-007` already disclose, platform-wide, that neither Progressive Disclosure nor the Evidence Panel has ever been built as a conforming frontend component — `SE-001`'s own text: "zero conforming components exist repo-wide." `ADR-021` Decision 5/`ADR-022` Decision 3 both require Conversational Experience to compose these contracts, never reinvent them. WP-12 is therefore the first Work Package for which this gap is load-bearing, not merely disclosed — the same shape of finding `IRA-011 §4.4` made for `AIService`'s own missing authentication (a pre-existing, service/platform-wide gap this Work Package is the first to actually need closed).

**Resolution path (Reuse → Extend, not invent):** `IMP-001 §10.3`/`§10.4` already fully specify both contracts' own shape (four-state widget contract; confidence-score-plus-evidence-reference Reference Component). No new component contract is proposed — this is a first, real implementation of an already-fully-specified contract, exactly as `IRA-011 §4.5` (AIService's Alembic chain) was Extend-class work applying an already-proven platform pattern to a service that had never adopted it.

**Scope narrowing, mirroring `IRA-011 §4.2`'s own "narrowest slice" discipline:** WP-12 builds Progressive Disclosure and the Evidence Panel only as far as Conversational Experience's own turn presentation requires — not the full cross-cutting rollout `SE-001`/`SE-007` describe platform-wide (retrofitting every existing WP-01–WP-11 screen). That broader rollout remains separately tracked in `SER-001`, unaffected by this Work Package, mirroring `TD-117`'s own precedent of a disclosed, narrower-than-the-full-enhancement consumption boundary.

**Disposition:** in scope, mandatory, narrow — realized as a cross-cutting concern within **BA-02**/**BA-03** (the two Business Activities that actually render Interaction output), not a separate Business Activity — `CMD-001 §26.3a` Step 1 would fail for it as a standalone candidate (no independent business identity of its own), the same reasoning `IRA-011 §4.7` already applied to its own Alembic-chain prerequisite.

### 4.5 Cross-Lifecycle Agent Handoff / Multi-Agent Visualization — **EXCLUDED**

`ADR-020` Decision 5 and `ADR-022` Decision 2 both specify the reuse obligation *if* Handoff/multi-agent visualization is presented, but neither requires it to be. `SER-001 SE-027` confirms Multi-Agent orchestration remains "architecturally complete, zero code" platform-wide, unaffected by WP-11 and unaffected here. Building it now would exceed C-094's own minimum viable scope with no demonstrated near-term need.

**Disposition:** excluded — unchanged from the constitutional workshop's own explicit exclusions (`ADR-022 §5`).

### 4.6 Ask User Gate Integration — **EXCLUDED**

`ADR-022` Decision 2 requires that *if* a human-approval pause is presented, it composes the existing Ask User Gate (`RTA-001 §13.12a`) rather than a parallel mechanism — it does not require WP-12 to build an approval-pause experience at all. No governing specification (no `PE-001-C094`) names human-approval pausing as part of C-094's own minimum scope, and `RTA-001 §13.12a` itself has zero implementation anywhere to extend. Building it now would be speculative, not evidenced.

**Disposition:** excluded — deferred to a future Work Package or extension of WP-12, if and when a genuine need is demonstrated.

### 4.7 Summary

| Item | Disposition | Realization |
|---|---|---|
| Establish and Manage Conversation Lifecycle | In scope | BA-01 |
| Execute Interaction | In scope | BA-02 |
| Retrieve Conversation (new) | In scope, narrow | BA-03 |
| Progressive Disclosure / Evidence Panel first implementation | In scope, mandatory, narrow | Within BA-02/BA-03 |
| Cross-Lifecycle Agent Handoff / multi-agent visualization | Excluded | None this WP |
| Ask User Gate integration | Excluded | None this WP |
| `AIService` authentication / Alembic chain | Reused from WP-11 | No new prerequisite |

**Three Business Activities**, mirroring `IRA-011`'s own three-BA shape. Unlike WP-11, no mandatory platform prerequisite sits *outside* the Business Activity layer this time — `AIService`'s own authentication and Alembic infrastructure are already built and simply reused; the one genuinely new cross-cutting concern (§4.4) is folded into the two Business Activities that need it, the same way WP-11 folded its own Alembic-chain prerequisite into BA-01.

---

## 5. PLAN A — Business Capability Implementation

### BA-01 — Establish and Manage Conversation Lifecycle

- **Domain Model:** `ConversationService` (`IMP-001 §13.28`), backed by `SessionRecordRepository` (`§13.29`) for durable persistence and `ConversationStateResolver` (`§13.29`) for boundary transitions — no new domain construct beyond what `RTA-001 §13.15a`/`IMP-001 §13.26–38` already specify.
- **Service:** Creates a tenant-scoped Conversation record (Open state); exposes an explicit close transition (per `ADR-020` Decision 2, triggered by explicit action or Runtime Policy, never by the state model itself).
- **API:** `POST /conversations` (establish); `POST /conversations/{id}/close` (explicit close transition). Gated by `AIService`'s own existing authentication dependency (WP-11, reused unchanged).
- **Cross-cutting:** one new Alembic migration, extending `AIService`'s existing chain (not bootstrapping a second one), introducing the Conversation System of Record — exact schema determined at implementation time, per `ADR-020` Decision 3's own explicit deferral of persistence-technology decisions.
- **Testing:** Unit (Conversation created in Open state; close transition only reachable via an explicit trigger, never a default) + API (200/201; 401/403) + the Mandatory Tenant-Isolation Test Checklist (§10).

### BA-02 — Execute Interaction

- **Domain Model:** `InteractionService` (`§13.28`), composing `InteractionStateAssembler` (`§13.30`) for continuity and the existing Reasoning Engine/Execution Capability Selection resolvers (`RTA-001 §13.9b`/`IMP-001 §13.9`) for the underlying AI Request Lifecycle execution.
- **Service:** Accepts a user turn against an Open Conversation; assembles Interaction State from prior Interactions in the same Conversation (never from any other Conversation, never from `MemoryRepository`); executes one bounded AI Request Lifecycle; persists the resulting Interaction, preserving identity, ordering, and accountability per `ADR-022` Decision 1.
- **API:** `POST /conversations/{id}/interactions` — request: turn input; response: the Interaction's own output, composed with the (first real implementation of the) Evidence Panel/Confidence contract per §4.4.
- **Cross-cutting (this BA, shared with BA-03):** first real Progressive Disclosure/Evidence Panel component build, scoped to Interaction output rendering only (§4.4).
- **Testing:** Unit (Interaction correctly scoped to its own Conversation; continuity assembled only from prior same-Conversation Interactions) + API (200/201; 401/403; a request against a Closed Conversation rejected) + the Mandatory Tenant-Isolation Test Checklist (§10) — a caller in Organization A must never retrieve or influence Organization B's own Conversation.

### BA-03 — Retrieve Conversation

- **Service:** Lists a Conversation's own Interactions, in order, by identity — `ADR-022` Decision 1's preservation obligation realized as a read path.
- **API:** `GET /conversations/{id}/interactions` — response: ordered Interaction list, each composing the same Progressive Disclosure/Evidence Panel contract as BA-02's own live response.
- **Explicitly excluded:** cross-Conversation listing, search, filtering, or any aggregate/summary view (`ADR-022` Decision 3, explicit prohibition).
- **Testing:** Unit (ordering preserved; no cross-Conversation leakage) + API (200; empty state for a Conversation with zero Interactions yet) + the Mandatory Tenant-Isolation Test Checklist (§10).

### Cross-cutting

- **Migration:** one new Alembic migration extending `AIService`'s existing chain (Conversation/Interaction System of Record — exact table shape determined at implementation time, per `ADR-020`'s own deferral of persistence technology).
- **Authentication/tenant isolation:** reused unchanged from WP-11's own `AIService` Authentication Bootstrap — no new prerequisite, no new dependency.

---

## 6. Business Object Eligibility Analysis (`CMD-001 §26.3a`)

**Required, unresolved by this IRA — flagged for Repository Owner decision before Technical Design.** Unlike WP-11 (which built against already-LOCKED `Master_Technical_Architecture.md` tables), Conversation and Interaction have no equivalent LOCKED physical schema anywhere yet — `ADR-020` Decision 3 established only that a canonical System of Record must exist, deliberately deferring its physical shape. This means, unlike `IRA-011 §6`'s finding that eligibility analysis was unnecessary, **WP-12 may require a genuine `CMD-001 §26.3a` eligibility determination and registration for Conversation/Interaction as canonical Business Objects**, mirroring `ADR-019`'s own `CFG-000001` precedent (registration required specifically because no canonical table existed before that Work Package). This is a Technical Design-phase determination, not resolved here — noted as an open item, not silently assumed either way.

---

## 7. PLAN B — Enterprise Experience Implementation

Derived only from `SD-001 §16`, `PE-001`, `DS-001`, `IMP-001 §§13.39–53` — per `CLAUDE.md §20.3`, this plan identifies what is built; it does not itself design a screen.

- **What the user sees:** a Conversational Experience surface — submit a turn, see the response composed with evidence/confidence (first real Progressive Disclosure/Evidence Panel instance, §4.4), see prior turns in order (BA-03).
- **What the Executive sees:** the platform's first sustained "converse" experience — narrow (single-Conversation, no cross-Conversation aggregation, no multi-agent visualization), disclosed as narrow, not oversold as a general-purpose copilot.
- **Screens realized:** **no existing nav slot exists for C-094** (confirmed by direct search, §3) — unlike WP-11's own reused `enterprise-intelligence` placeholder, a new, minimal nav entry is required. Exact placement (which of `PE-001 §13.5`'s six Workspace types, or a new capability-specific slot within one of them) is **not decided by this IRA** — determined at implementation time against `SD-001-115`'s own confirmation that this remains each capability's own CRB/ERB decision, per `PE-001 §13.5`'s existing delegation.
- **Design System components used:** existing `Form`, `Card`, `Button`, `Spinner` (reused, same set `IRA-010`/`IRA-011` already used); Progressive Disclosure and the Evidence Panel **built for the first time** (§4.4), following `IMP-001 §10.3`/`§10.4`'s own already-specified contract exactly — no new component contract invented.
- **Conversation turn presentation:** per `ADR-022` Decision 1, visual turn representation (including any streaming or progressive-rendering choice) is not constitutionally fixed — determined at implementation time, provided Interaction identity, ordering, and accountability are preserved.
- **States implemented (`CLAUDE.md §20.6`):** loading, empty (a newly-established Conversation with zero Interactions yet — an honest, disclosed empty state), validation, error, confirmation.

---

## 8. Readiness Decision

**READY, with one open item requiring Repository Owner input before Technical Design begins (§6).** C-094's own minimum viable Business Capability scope is three Business Activities — BA-01 (Establish and Manage Conversation Lifecycle), BA-02 (Execute Interaction, the core deliverable), BA-03 (Retrieve Conversation, new — the minimum addition making BA-01/02 genuinely demonstrable rather than write-only). The Progressive Disclosure/Evidence Panel first-implementation gap (§4.4) is in scope, narrow, and folded into BA-02/BA-03 rather than treated as a separate mandatory prerequisite outside the Business Activity layer — unlike WP-11's own authentication gap, this one is genuinely produced by, not merely consumed by, C-094's own Business Activities, since no other capability has needed it yet either.

No constitutional blocker for the scope that IS in bounds — `ADR-020`/`ADR-021`/`ADR-022` are each independently re-verified consistent and complete for what this scope requires (§1, §2). Cross-Lifecycle Agent Handoff, multi-agent visualization, and Ask User Gate integration excluded, each for a distinct, disclosed, evidence-grounded reason (§4.5/§4.6), not a blanket exclusion.

**One item requires explicit Repository Owner decision before Technical Design (§6):** whether Conversation/Interaction require a formal `CMD-001 §26.3a` Business Object eligibility determination and registration (mirroring `ADR-019`'s `CFG-000001` precedent) before their own physical schema is designed, since — unlike WP-11's own already-LOCKED tables — no canonical physical shape for either construct exists anywhere yet.

---

## 9. Anticipated Technical Debt

- **TD-candidate-E** (Medium): the exact write-path/read-path persona gate for BA-01/02/03 is undetermined — no `PE-001-C094` exists to name one, same root cause as `TD-021`-class entries across every prior Work Package.
- **TD-candidate-F** (Low): Progressive Disclosure/Evidence Panel's own first implementation (§4.4) is scoped narrowly to Conversational Experience turns; the full cross-cutting rollout to every existing WP-01–WP-11 screen (`SE-001`/`SE-007`'s own broader scope) remains open, disclosed, not this Work Package's obligation to close in full.
- **TD-candidate-G** (Medium): no real streaming/progressive-rendering mechanism is designed by this IRA (`ADR-022` Decision 1 leaves it open) — Technical Design will need to make this determination; deferring it here is intentional, not an oversight.
- **TD-candidate-H** (Low): Interaction State/Continuity's own structural exclusion of `MemoryRepository` (`IMP-001 §13.30`) means long conversations have no compaction/summarization strategy yet — acceptable for a first, narrow implementation; worth tracking once `C-095` Enterprise Memory is eventually chartered.

(Final Technical Debt IDs assigned at implementation time, per `CLAUDE.md §19.8.2`.)

---

## 10. Testing Strategy

Per `IMP-001 §11`, extended by `IMP-001 §13.36`'s own AI Session boundary tests and `§13.51`'s own AI-Native Experience boundary tests, and `CLAUDE.md §21.4`'s Mandatory Tenant-Isolation Test Checklist: Conversation and Interaction each carry an organization-level tenant boundary (per `ADR-020`'s own confirmed cross-reference to `SD-002 §13`). BA-01/02/03's own test suites SHALL each include, as a submission gate: (a) at least one test seeding two distinct, unrelated Organizations with no shared row; (b) at least one test confirming a caller in one Organization cannot retrieve or infer another Organization's own Conversation or Interaction records through any of the three endpoints; (c) an explicit probe of whether an unrelated tenant's own Conversation identifier is accepted by BA-02/BA-03 (a caller-supplied, not claims-derived, parameter) — if accepted, the endpoint SHALL be gated before submission. In addition, per `IMP-001 §13.36`/`§13.51`'s own named boundary tests: `ConversationStateResolver` transitions verified reachable only from an actual trigger, never a default; `InteractionStateAssembler` verified to have no reachable `MemoryRepository` dependency; `ExperienceCompositionResolver` verified to never resolve by hardcoded capability identity. Full `AIService` regression suite re-run before closure.

---

## 11. Entry Criteria

This IRA itself is the entry-criteria gate for chartering. Satisfied: governing constitutional documents reviewed in full (`RTA-001 §13.15a`, `SD-001 §16`, `ADR-020`/`021`/`022`, all read directly), existing assets discovered (§3), Gap Analysis complete including the three `§21.3` reviews and the one previously-undisclosed gap (§4.4), no constitutional blocker for the in-scope portion. **Not yet satisfied, and required before Technical Design specifically:** the `CMD-001 §26.3a` eligibility determination (§6) remains an open Repository Owner decision, not resolved by this IRA.

## 12. Exit Criteria

Per `CLAUDE.md §19.7`/`§19.7b`/`§20.7`/`§21`, applied to the scope in §4.7/§8: BA-01/02/03 Implementation Complete; Independent Certification; V&V Audit (including mandatory tenant-isolation verification per `§21.4`); Release Readiness Audit; end-to-end demonstrability for the in-scope facets only (a persona can open a Conversation, exchange turns, and retrieve the ordered history, with evidence/confidence genuinely rendered, not stubbed). Per `§21.5`, one Repository Owner authorization executes the entire Work Package.

---

## 13. Repository-Owner Authorization

**IRA Acceptance: Not yet granted — awaiting Repository Owner review**, including explicit resolution of the one open item this IRA surfaces (§6, `CMD-001 §26.3a` eligibility). Per the two-step chartering-then-authorization precedent `WP-10`/`WP-11` each established, a separate, future "WP-12 Implementation Authorization" instruction remains required before BA-01/02/03 implementation begins.
