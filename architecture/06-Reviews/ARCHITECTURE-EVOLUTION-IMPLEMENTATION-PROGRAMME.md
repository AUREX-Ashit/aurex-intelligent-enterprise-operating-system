# Architecture Evolution Implementation Programme

**Type:** Architecture Planning exercise (read-only; no repository, architecture, or governance artifact other than this report was modified in the course of this review)

**Input:** `architecture/06-Reviews/ARCHITECTURE-EVOLUTION-STRATEGIC-ROADMAP.md`, treated as the authoritative planning input per Repository Owner instruction. This report transforms that roadmap's recommendations into a structured implementation programme — classification, capability mapping, document mapping, Work Package mapping, dependency graph, and release plan. No new repository research was performed; all classifications below trace to evidence already established in the roadmap and its own underlying research passes, with one correction identified during this pass (§3, R14).

**Constraints observed:** nothing in this report was implemented, no code was modified, no document was updated, no Work Package was created. Every "Work Package" reference below is a recommendation for Repository Owner approval, not an act of chartering.

---

## Contents

1. [Executive Summary](#1-executive-summary)
2. [Recommendation Classification Matrix](#2-recommendation-classification-matrix)
3. [Capability Mapping](#3-capability-mapping)
4. [Document Update Plan](#4-document-update-plan)
5. [Work Package Mapping](#5-work-package-mapping)
6. [Dependency Graph](#6-dependency-graph)
7. [Release Plan](#7-release-plan)
8. [Critical Path](#8-critical-path)
9. [Risks](#9-risks)
10. [Repository Owner Decisions](#10-repository-owner-decisions)
11. [Recommended Implementation Sequence](#11-recommended-implementation-sequence)
12. [Items That Should NOT Be Implemented Yet](#12-items-that-should-not-be-implemented-yet)

---

## 1. Executive Summary

The roadmap's recommendations resolve into 36 discrete items (R1–R36). Eight are pure documentation reconciliations with zero code impact and zero dependencies on each other — the cheapest, safest, highest-leverage work in the entire programme, and the natural first release. One infrastructure repair (`Backend/Shared` import defect) unblocks two further items (AI audit wiring, Observability build-out) and should happen alongside the documentation release. A cluster of frontend/configuration work is independent of the AI/Knowledge track and can proceed in parallel. The single hard gate in the whole programme is that Enterprise Intelligence (D-005) has never been chartered before in this repository — everything downstream of it (Executive Cognition-branded work) is sequenced behind one deliberately narrow proving Work Package, not behind a generic "AI work" label.

One correction was identified while building the capability mapping in §3: the roadmap's Notification framework gap was previously described as having no CAP-001 owner. It does — **C-132 Enterprise Notifications is already Active.** This changes its classification from "new capability territory" to the same tier as C-041 or C-066: an Active, specified-by-reference, simply-unimplemented capability. This is noted here rather than silently corrected, consistent with the review discipline this entire exercise has followed.

**Reclassification (Release A Reclassification & Execution Strategy pass, this update):** `IRA-RELEASE-A_Foundation_Repair_Implementation_Readiness_Assessment.md` found that "Release A," as originally scoped in §7 below, is not a single executable unit — its nine items require three genuinely different governance processes before implementation, not one. Release A is accordingly split into **A1 (Foundation Repairs)**, **A2 (Architecture Governance)**, and **A3 (Locked Architecture Evolution)** — see §5, §6, §7, §8, §10, §11 below, each updated only where this split changes their content. Releases B, C, and D are unchanged by this pass.

---

## 2. Recommendation Classification Matrix

| # | Recommendation | Classification | Justification |
|---|---|---|---|
| R1 | Repair `Backend/Shared/Logging`/`Events` import defect | Infrastructure improvement | Fully built, currently unreachable by any service; not a design gap, a wiring defect |
| R2 | Correct CLAUDE.md §3 repository navigation map | Documentation reconciliation | Stated paths (`source/backend`, `source/database`) don't match actual layout |
| R3 | Reconcile ARCH-000 §7c / RTA-001 §12.16 (Knowledge Governance) | Documentation reconciliation | Two constitutional-tier documents disagree; no code involved |
| R4 | Reconcile `llm_prompt_registry` vs `reasoning_engine_registry` | Documentation reconciliation | Duplicate schema-level concept, neither migrated; a decision, not a build |
| R5 | Reconcile "Enterprise Operating System" vs "Intelligent Enterprise Operating Center" naming | Documentation reconciliation | Platform-identity naming variance across ARCH-000 and Complete_Blueprint |
| R6 | Update CMD-001 §24 to reference AMD-012/013 registries | Documentation reconciliation | Pre-existing, unretracted finding; data-model documentation is stale, not wrong |
| R7 | Ratify or retire SD-001's two unratified extensibility candidates | Documentation reconciliation | Governance decision on already-drafted candidate text |
| R8 | Add Explainability as an explicit owned row in ARCH-000 §7c | Documentation reconciliation | Closes an acknowledged ownership gap in an existing table |
| R9 | Decide fate of the duplicate Tenant model | Architecture enhancement | Touches a canonical-model boundary (CLAUDE.md §6); requires a decision before any dependent code change |
| R10 | Build the Progressive Disclosure four-state widget contract | Existing capability implementation + Frontend enhancement | IMP-001 §10.3/IMP-FE-004 already mandates this; nothing new is being designed |
| R11 | Build Theme High-Contrast / reduced-motion / large-text modes | Existing capability implementation + Frontend enhancement + Enterprise Experience enhancement | DS-001 Ch.11's five-class model and SD-001-063 already specify this |
| R12 | Extend Discover-First to Membership/Organization Node establish forms | Existing capability extension + Frontend enhancement | A working precedent (Person Management, WP-07) already exists; this replicates it |
| R13 | Build Saved Views against DataGrid | Existing capability implementation + Frontend enhancement | SD-001-052 already specifies the exact behavior |
| R14 | Build Notification backend | **Existing capability implementation** (corrected — see §3) + Backend enhancement | Realizes Active capability C-132 Enterprise Notifications; frontend shell already exists as a self-disclosed placeholder |
| R15 | Charter WP-09 (C-008 Workspace Management) | Existing capability implementation | C-008 is Active and specified; simply next in WP-REG-001's own queue |
| R16 | Charter WP-10 (C-041 Configuration Management, consolidated scope) | Existing capability implementation | Consolidates Terminology/Branding/Theme/Config Profiles/Localization/Accessibility/AI Configuration under one already-Active capability |
| R17 | Charter WP-11 (first D-005 capability, C-090 or C-093) | Existing capability implementation | Both are Active and registered; this is proving an unchartered domain, not inventing one |
| R18 | Wire existing `record_audit` into AIService | Backend enhancement + AI Governance enhancement + Technical debt | Closes a disclosed, already-built-elsewhere gap; not new architecture |
| R19 | Build out Observability Runtime (RTA-001 §17 / Law 14) | Infrastructure improvement + Backend enhancement | Fully specified as a canonical Runtime Law; currently fragmented per-service due to R1 |
| R20 | Build Connector Framework (CMD-001 §23) | Existing capability implementation + Backend enhancement | Realizes Active capability C-150 Integration Management |
| R21 | Fold Plugin architecture into C-150, sequenced after R20 | New capability (contingent) / Future roadmap only | No CAP-001 registration exists yet; explicitly sequenced, not immediate |
| R22 | Charter C-042 Preference & Personalization | Existing capability implementation | Planned capability, registered, unspec'd |
| R23 | Charter C-094 AI Conversation Management | Existing capability implementation (gated) | Planned capability; gated behind R17 succeeding |
| R24 | Charter C-095 Enterprise Memory | Existing capability implementation (gated) | Planned capability; gated behind R17 **and** a Repository Owner decision to lift ARCH-000 §7c's deferral |
| R25 | Charter C-113 Policy Management (general Policy-as-Code) | Existing capability implementation | Planned capability; distinct from the already-Active narrow authorization case under C-003 |
| R26 | Charter C-133 Activity Stream & Timeline | Existing capability implementation | Planned capability; realizes the "Timeline" gap |
| R27 | Build Multi-Agent orchestration runtime | Architecture enhancement + Infrastructure improvement | Cross-cutting RTA-001 §13.6d/e runtime capability, not itself a CAP-001 capability — supports D-005 capabilities rather than being one |
| R28 | Build real Semantic Search implementation (replace hardcoded stub) | Existing capability implementation + AI Governance enhancement + Backend enhancement | Realizes C-093/C-092; the interface layer already exists and matches spec |
| R29 | Log the `Backend/Shared` defect in the Technical Debt Register | Technical debt | Governance action itself — zero code, should happen regardless of R1's timing |
| R30 | Decide whether to formally define a lighter-weight "Sprint" category | Future roadmap only | No governance status exists today; a pure Repository Owner process decision |
| R31 | Decide whether to retroactively document the recent frontend refinement work | Future roadmap only | Same as R30 — a disclosed gap, not an implementation item |
| R32–R36 | Executive Cognition / Future Platform items (Executive Copilot, Digital Twin, Simulation, Organizational Learning, Skills Graph, Workflow Studio, AI Marketplace, Operating Manual, Autonomous Business Activities, Prompt Studio, standalone MCP Selection, "Cognitive Design Language") | Future roadmap only | No CAP-001 registration for most; explicitly excluded from this programme per §12 |

---

## 3. Capability Mapping

`[EVIDENCE]`/`[RECOMMENDATION]` notation as used in the source roadmap. Mapping against CAP-001 v1.5's actual 43-row registry.

| Recommendation | Existing CAP-001 capability | New capability required? | No capability required |
|---|---|---|---|
| R10 Progressive disclosure | Cross-cutting — governed by IMP-001 §10.3, not a single capability | No | — |
| R11 Theme High-Contrast | **C-041 Configuration Management** (Active) | No | — |
| R12 Discover-First parity | C-007 Membership Management / C-005 Enterprise Structure Management (both already chartered, WP-03/WP-04) | No | — |
| R13 Saved Views | Cross-cutting — governed by SD-001-052, applies to any capability's list screens | No | — |
| **R14 Notification backend** | **C-132 Enterprise Notifications — already Active** *(correction: the source roadmap described this gap as ownerless; it is not — see Executive Summary)* | No | — |
| R15 WP-09 | **C-008 Workspace Management** (Active) | No | — |
| R16 WP-10 | **C-041 Configuration Management** (Active) — covers Terminology, Branding, Theme, Configuration Profiles, Localization, Accessibility Profiles, **and AI Configuration** (`[EVIDENCE]` CMD-001 §12's Configuration Categories explicitly include an "AI Configuration" category — Embedding Model, LLM Selection, Prompt Strategy — resolved through the same Tenant/Enterprise scope hierarchy as every other C-041 facet, per CMD-001:5966-5980. This corrects a soft mis-mapping in the source roadmap, which grouped AI Provider/Embedding/Tool Selection under D-005 (C-090–093) — the CMD-001 data model places *which AI vendor an enterprise configures* under C-041, while *what Enterprise Discovery/Knowledge/Search/Graph capabilities do with that configured AI* stays under D-005. Both mappings now stand, distinguished by concern.) | No | — |
| R17 WP-11 | **C-090 Enterprise Discovery** or **C-093 Enterprise Search** (both Active) | No | — |
| R18 AI audit wiring | C-114 Audit & Assurance (Active) as the eventual governance home; near-term this is pure backend wiring, not a capability build | No | No — pure implementation of an existing primitive |
| R19 Observability build-out | Cross-cutting — RTA-001 §17 is platform infrastructure, not a CAP-001 capability | No | Yes — infrastructure, not a capability |
| R20 Connector Framework | **C-150 Integration Management** (Active) | No | — |
| R21 Plugin architecture | None currently | **Yes, if pursued** — would require a new ID within D-008's reserved range (C-150–C-169), a Repository-Owner-level decision | — |
| R22 C-042 | **C-042 Preference & Personalization** (Planned) | No | — |
| R23 C-094 | **C-094 AI Conversation Management** (Planned) | No | — |
| R24 C-095 | **C-095 Enterprise Memory** (Planned, currently deferred at governance level) | No | — |
| R25 C-113 | **C-113 Policy Management** (Planned) | No | — |
| R26 C-133 | **C-133 Activity Stream & Timeline** (Planned) | No | — |
| R27 Multi-Agent orchestration | Cross-cutting — RTA-001 §13.6d/e | No | Yes — runtime infrastructure supporting D-005, not itself a capability |
| R28 Semantic Search | **C-093 Enterprise Search** / **C-092 Knowledge Graph Management** (both Active) | No | — |
| R9 Tenant model decision | Touches the canonical model boundary itself (CLAUDE.md §6), not a specific capability | No | Yes — an architecture-level decision |
| R32–R36 | None registered (except R35's MCP-neutrality, which is a deliberate non-capability) | Would each require new registration | — |

**Governance rule observed throughout:** per CAP-001 §3, "new capabilities shall be appended within reserved domain ranges" — no recommendation above proposes appending a new ID except where explicitly marked, and even those are flagged as Repository-Owner decisions, not proposals this report is making unilaterally.

---

## 4. Document Update Plan

*(Restated from the source roadmap's §7, unchanged except where R14's correction affects framing — see the note under CLAUDE.md.)*

| Document | Why | Sections | Impact | Dependencies |
|---|---|---|---|---|
| CLAUDE.md | Repository navigation map (§3) doesn't match actual layout | §3 Repository Intelligence | Low functional risk; high onboarding-accuracy value | None |
| ARCH-000 | Knowledge Governance deferral doesn't address RTA-001 §12.16's substantive content | §7c AI Governance Ownership Map | Medium — affects Knowledge Governance work, gates part of R17/R23/R24 | RTA-001 §12.16 (referenced) |
| ARCH-000 | Explainability has no explicit owned row | §7c AI Governance Ownership Map | Low-Medium — closes an acknowledged gap | SD-002-016 (referenced) |
| Master Technical Architecture | `llm_prompt_registry` / `reasoning_engine_registry` unreconciled | The two registry definitions | High for any future AI prompt/model work; gates part of R17 | None |
| ARCH-000 §2 / Complete_Blueprint | "Enterprise Operating System" vs. "Intelligent Enterprise Operating Center" naming variance | ARCH-000 §2; Complete_Blueprint Executive Summary | Low functional risk; onboarding/external-consistency value | None |
| CMD-001 | §24 predates AMD-012/013 physical registries | §24.3–24.5 | Medium — documentation-currency gap | Master Technical Architecture |
| SD-001 | Two unratified extensibility candidates (`SD-002-CANDIDATE-016`/`026`) | The candidate list | Medium, contingent on R16 (C-041 charter) | R16 |

---

## 5. Work Package Mapping

| Recommendation | Mapping |
|---|---|
| R1, R2, R3, R8, R29 *(Release A1)* | **No Work Package** — ready to implement directly; touches no Locked document and requires no Repository Owner decision, per `IRA-RELEASE-A` |
| R4, R5 *(Release A2)* | **No Work Package** — blocked on a Repository Owner decision only (no Locked document involved), per `IRA-RELEASE-A` |
| R6, R7 *(Release A3)* | **No Work Package** — blocked on the formal Locked-document ADR/recertification process (`CMD-001`, `SD-001` are both LOCKED per `DOC-000` §8), and, for R7, additionally on a Repository Owner ratify/retire decision, per `IRA-RELEASE-A` |
| R9 | **Repository Owner decision**, then either Infrastructure remediation or Technical Debt depending on the outcome |
| R1 *(see A1 above)* | **Infrastructure remediation** |
| R19 | **Infrastructure remediation**, contingent on R1 |
| R18, R29 | **Technical Debt** |
| R10, R11, R12, R13 | **Product refinement** — bounded, precedented (matches this session's own recent Enterprise Shell refinement pattern), not WP-shaped |
| R15 | **Future Work Package** (WP-09) |
| R16 | **Future Work Package** (WP-10) |
| R17 | **Future Work Package** (WP-11) |
| R14, R20, R22, R23, R24, R25, R26 | **Future Work Package**, each against its own CAP-001 capability |
| R21 | **Future capability** (contingent on a Repository Owner registration decision, then Future Work Package) |
| R27, R28 | Scoped **inside** WP-11's own charter, not separate Work Packages |
| R30, R31 | **Repository Owner decision** — no Work Package possible until the process question itself is settled |
| R32–R36 | **Future capability** / explicitly out of this programme (§12) |

---

## 6. Dependency Graph

**Refined this pass, per `IRA-RELEASE-A`:** Release A's own items are no longer treated as one undifferentiated group in the graph below — A1 items are unblocked now, A2/A3 items carry their own distinct blockers, and one new soft dependency (R6 → R17) was identified by re-examining what WP-11 will actually need from CMD-001, not previously called out in the original graph.

**Prerequisites (hard blocks):**
- R18, R19 depend on **R1** *(Release A1 — unblocked, ready now)*
- R17 depends on **R3 and R4** — R3 is Release A1 (unblocked, ready now); R4 is Release A2, blocked on a Repository Owner decision (§10) — this repository's own precedent (ADR-014/017 methodology) is not to build against unreconciled documents
- R23, R24 depend on **R17 succeeding** (proving the D-005 charter pattern)
- R24 additionally depends on a **Repository Owner decision** to lift ARCH-000 §7c's Enterprise Memory deferral
- R21 depends on **R20 completing** (avoids duplicating Connector/Plugin extension mechanisms)
- R16's AI Configuration facet has a **soft dependency** on R9 (if AI configuration data ultimately needs Tenant-model fields, the model's fate should be settled first)
- **New this pass:** R16's Configuration Profiles facet specifically (not its other five facets) has a **soft dependency** on R7 *(Release A3)* — WP-10 can charter and build Terminology/Branding/Theme/Locale/Accessibility/AI Configuration regardless, but Configuration Profiles has no ratified spec to build against until R7 resolves.
- **New this pass:** R17 has a **soft dependency** on R6 *(Release A3)* — WP-11 builds against C-090/092/093, part of CMD-001 §24's own Knowledge & AI Domain; §24 not yet referencing the AMD-012/013 registries those capabilities actually use is a real risk that WP-11's own IRA re-surfaces the same staleness this programme already found, not a proven hard block. Recommended to resolve before WP-11's IRA is drafted, not required before WP-11 is chartered.

**Parallel work (no dependency on each other or on the above):**
- R2, R3, R8, R29 *(Release A1 — unblocked, ready now)*
- R15 (WP-09)
- R20 (Connector Framework)
- R25, R26 (C-113, C-133)
- R10, R11, R12, R13 (frontend/product refinement track)

**Blocked work:** R18, R19 (on R1 — unblocked, so effectively ready once A1 lands); R17, R27, R28 (on R3 [unblocked] + R4 [Release A2, decision-blocked], and soft-blocked on R6 [Release A3]); R23, R24 (on R17); R21 (on R20); R4, R5 (Release A2 — on a Repository Owner decision only); R6, R7 (Release A3 — on the Locked-document process, and R7 additionally on a decision).

**Independent work:** everything in the parallel list above, plus all of Release A1 — the largest single bucket in the programme, and the safest place to start.

**Critical path:** see §8.

---

## 7. Release Plan

**Release A is reclassified into three waves this pass, per `IRA-RELEASE-A`'s finding that it is not one executable unit:**

**Release A1 — Foundation Repairs.** R1, R2, R3, R8, R29. Ready to implement now — touches no Locked document, requires no Repository Owner decision. One infrastructure repair (R1, a wiring fix, not new logic), one CLAUDE.md correction (R2, a non-governed document), two ARCH-000-only table corrections following the repository's own established remediation precedent (R3, R8), one Technical Debt Register entry (R29, a living register). Zero code risk beyond R1.

**Release A2 — Architecture Governance.** R4, R5. Blocked on a Repository Owner decision each (which AI-configuration registry governs; which platform-identity name is canonical) — neither touches a Locked document, so once decided, each can be implemented immediately without a separate ADR. Not scheduled to a date; unblocks the moment its decision is made.

**Release A3 — Locked Architecture Evolution.** R6, R7. Blocked on the formal Locked-document ADR/recertification process (`CMD-001` and `SD-001` are both `LOCKED` per `DOC-000` §8), the heaviest-process wave in Release A. R7 additionally requires a Repository Owner ratify/retire decision as part of that process. Recommended to begin only once A1 has demonstrated the reclassification holds up in practice, though nothing structurally prevents starting the ADR drafting in parallel.

**Release B — Enterprise Experience & Configuration Completion.** R15 (WP-09), R16 (WP-10, includes R11), R14, R13, R10, R12. Groups every frontend-facing, already-specified, D-005-independent item into one coherent release. Matches this session's own precedent of Enterprise Shell refinement work.

**Release C — Enterprise Intelligence Foundation.** R17 (WP-11, includes R27, R28), R18, R19, R20, R9 resolution. This is the release where the AI/Knowledge/Platform-infrastructure track is proven end-to-end for the first time in this repository. Gated on Release A's R3/R4 completing first.

**Release D — Executive Cognition & Extended Platform.** R22, R23, R24, R25, R26, R21 (if R20 has completed). Gated on Release C's R17 succeeding. This release should not be scheduled with a fixed date — it starts only once its gate condition is actually met, not on a calendar assumption.

**Not a release — Future Vision.** R30, R31 (Repository Owner process decisions, can happen anytime independent of the above) and R32–R36 (explicitly excluded, see §12).

---

## 8. Critical Path

The longest true dependency chain in the programme, and the one sequence that cannot be compressed by adding parallel effort:

**R3 (Release A1, unblocked) + R4 (Release A2, decision-blocked) → R17 / WP-11 (first D-005 charter, closes successfully through the full five-gate process) → R23 / R24 (C-094, C-095 charters) → R32+ (Executive Cognition work becomes chartering-eligible).**

Only **R4** now sits on the hard critical path as an open blocker — R3 is Release A1 and can close immediately. R4 is therefore the single highest-leverage Repository Owner decision in the entire programme: resolving it is the one action that shortens the path to Executive Cognition work, and nothing else does.

**R6 (Release A3) is a recommended risk-reduction step alongside the critical path, not a proven hard block on it** — see §6's own new finding. Resolving R6 before WP-11's own IRA is drafted avoids that IRA re-discovering the same CMD-001 §24 staleness this programme already found, but WP-11 could technically be chartered without it.

Every other recommendation in this programme sits off this path — Release A1's remaining items, Release B in its entirety, and R20/R25/R26/R29 can all proceed without waiting on it. `[RECOMMENDATION]` the practical implication: there is no reason to delay Release A1 or Release B while the critical path is being worked — they are genuinely independent — but there is also no way to shorten the path to Executive Cognition work by working harder on anything else. Time spent elsewhere doesn't substitute for R4 being decided and R17 actually closing.

---

## 9. Risks

- **Compressing the critical path risk:** attempting to charter C-094/C-095 before R17 (WP-11) has closed would repeat this repository's own WP-05 lesson — a correctly-run process can still miss defects a domain's first real attempt surfaces. The critical path exists specifically to prevent this.
- **Release A under-prioritization risk:** documentation reconciliations are low-drama and easy to defer indefinitely in favor of visible feature work; R3 (A1) and R4 (A2) sit on the critical path, so deferring either silently delays Release C and D as well.
- **Release A fragmentation risk (new this pass):** now that Release A is three waves instead of one, there's a real risk A2 and A3 get treated as indefinitely deferred simply because A1 shipped and "Release A" reads as done. Only R4 is actually on the hard critical path — A3 (R6, R7) can wait safely, but A2's R4 cannot wait indefinitely without stalling Release C.
- **R9 (Tenant model) ambiguity risk:** every release that touches AI/Tenant-adjacent configuration (part of R16, all of Release C) carries latent risk until this decision is made explicitly.
- **Release D calendar-pressure risk:** because Release D has a real, evidence-based gate (R17 success) rather than a fixed date, there will be pressure to schedule it anyway; recommend resisting this pressure per §8.
- **Scope-widening risk within Release B:** R16 bundles six facets (Terminology, Branding, Theme, Config Profiles, Localization, Accessibility, AI Configuration) into one Work Package; if the charter isn't disciplined about the "Reuse → Extend" boundary, this could grow into a redesign rather than an extension of C-041.

---

## 10. Repository Owner Decisions

The following cannot be scheduled without an explicit decision first:

1. **R4** *(Release A2)* — which AI-configuration registry should govern, `llm_prompt_registry` or `reasoning_engine_registry`, or should they be explicitly scoped apart? **Highest-leverage decision in the programme** — the only remaining hard blocker on the critical path to Executive Cognition (§8).
2. **R5** *(Release A2)* — canonical platform-identity name: "Enterprise Operating System" or "Intelligent Enterprise Operating Center," or explicitly synonymous.
3. **R7** *(Release A3)* — ratify or retire the two SD-001 extensibility candidates, in addition to authorizing whichever outcome through the Locked-document ADR process.
4. **R9** — retire or explicitly scope-apart the non-canonical Tenant model.
5. **R24's gate** — lift or maintain ARCH-000 §7c's deferral of Enterprise Memory (C-095) governance ownership.
6. **R30** — formally define a lighter-weight governance category below Work Package, or continue routing everything through the five-gate process.
7. **R31** — retroactively document the recent frontend refinement work, or leave it informal.
8. **R21's premise** — whether Plugin architecture should ever receive a new CAP-001 ID (D-008 range), independent of when.
9. **This programme's own release structure** — approval of the reclassified Releases A1/A2/A3, B, C, D as scoped, or a different grouping/sequencing preference.
10. **R15/R16/R17 sequencing** — confirm WP-09 → WP-10 → WP-11 as the intended charter order, since this programme assumes but does not itself decide that order.

---

## 11. Recommended Implementation Sequence

1. **Release A1** (Foundation Repairs) — start immediately; internally parallel, no gating, no decision required.
2. **Release B** (Enterprise Experience & Configuration) — start immediately in parallel with A1; fully independent of it. WP-09 has no relationship to any Release A wave. WP-10 can charter and build five of its six facets regardless of A2/A3; only its Configuration Profiles facet should wait on R7 (A3).
3. **Release A2** (Architecture Governance) — resolve R4 and R5 as soon as the Repository Owner is available to decide; R4 is the single highest-leverage action in the programme (§8). Not gated on A1 or B, but should not be left indefinitely open (§9).
4. **Release A3** (Locked Architecture Evolution) — begin the ADR process for R6/R7 once A1 has demonstrated the reclassification in practice; not gated on A2, but R7 shares a decision-maker with A2 so scheduling them together may be efficient.
5. **Release C** (Enterprise Intelligence Foundation) — start once R3 (A1) and R4 (A2) have closed; do not start R17 before then. R6 (A3) is recommended but not required to close first (§6, §8).
6. **Release D** (Executive Cognition & Extended Platform) — start only once R17 (part of Release C) has closed successfully through the full five-gate process; do not schedule by calendar.
7. **R30/R31** (process decisions) — can be resolved at any point; recommend resolving early since they're cheap and inform how all releases get tracked.

---

## 12. Items That Should NOT Be Implemented Yet

- **R21 Plugin architecture** — no CAP-001 registration; sequenced after Connector Framework (R20) at minimum, and gated on a Repository Owner registration decision beyond that.
- **R23 C-094 / R24 C-095** — gated on R17 (WP-11) succeeding; attempting either before then works against the entire reason WP-11 was scoped narrowly.
- **R32 Executive Copilot, Enterprise Digital Twin, Enterprise Simulation** — depend entirely on R23/R24; doubly gated.
- **R33 Organizational Learning, Enterprise Skills Graph** — no CAP-001 registration at all; would require a net-new capability decision this programme does not make.
- **R34 Workflow Studio, AI Marketplace, Enterprise Operating Manual, Autonomous Business Activities, Prompt Studio** — same as R33.
- **R35 A standalone Enterprise MCP Selection capability** — the architecture's considered position is deliberate vendor neutrality; building this now would be building ahead of an intentional non-decision, not filling a gap.
- **R36 Anything under a "Cognitive Design Language" banner** — the term does not exist anywhere in this repository; nothing should be built or charted under it.
- **Any Work Package outside Release A/B** before this programme's release structure itself is approved (§10, decision 7).

---

*Read-only architecture planning exercise · no repository files were modified other than this report · no Work Package was created · no document was updated · Aurex Enterprise Operating System*
