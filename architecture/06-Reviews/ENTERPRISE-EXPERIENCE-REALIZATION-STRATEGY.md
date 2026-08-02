# Enterprise Experience Realization Strategy

**Document ID:** EE-REALIZATION-STRATEGY
**Type:** Implementation planning artifact (process document, not a canonical specification) — companion to `METH-003_Implementation_Methodology_v2.md`
**Established by:** Repository Owner Instruction "Implementation Methodology v2.0 Establishment / WP-10 Planning Authorization," 2026-08-02
**Canonical authority preserved, not redefined (`CLAUDE.md §16`):** every principle this document applies is already owned by `PE-001` (Chapters 5–8, 11–17, 22–24), `SD-001`, or `DS-001`. This document is the practical, per-Business-Activity worksheet those chapters do not themselves provide — a repeatable question set, not a new experience model.

---

## 1. Purpose

`CLAUDE.md §21.3`'s own Standard Work Package Lifecycle names "Enterprise Experience" as a mandatory step between Business Activity definition and Backend/Frontend implementation. This document defines the worksheet every future Work Package's own IRA (Plan B) SHALL complete for every Business Activity, per the establishing instruction's own Phase 3.

## 2. The Per-Business-Activity Worksheet

For every Business Activity, the IRA's own Plan B SHALL answer:

| Question | Owning Canonical Source | WP-09 Worked Example |
|---|---|---|
| **What does the user see?** | `PE-001 §5.1` (Experience First — outcomes, not screens) | BA-01: a real, Membership-derived candidate list in the existing `WorkspaceSwitcher`, replacing a static 3-entry array. |
| **What does the Executive see?** | `PE-001` Chapter 12 (Persona Model, Executive Personas) | Not applicable to any WP-09 BA — none realizes an Executive Persona's own responsibility (§12.6). Stated explicitly, not silently omitted, per this worksheet's own §3 below. |
| **What workflow changes?** | `PE-001` Chapter 16 (Enterprise Experience Lifecycle — Discover/Enter/Understand/Decide/Execute/Validate/Transition/Complete) | BA-02: the Discover stage of "is my current context still valid" moves from implicit trust in a stale JWT claim to an explicit, real re-confirmation. |
| **Which Experience Contracts are realized?** | The governing `PE-001-Cxxx`'s own Chapter 5 Contracts | BA-03 realizes `EX-C008-11`'s own Context Produced per `BR-C008-06`. |
| **Which Screens are realized?** | `SD-001 §5`/`§7` (Screen Composition, Standard Screen Anatomy) | BA-01/02: no new screen — `WorkspaceSwitcher.tsx` extended, per `IRA-009 §7`'s own explicit "no new screen" design. |
| **Which Design System components are used?** | `DS-001` | `Menu`, `Spinner` (both pre-existing, reused per `CLAUDE.md §19.5`). |
| **Which Enterprise Shell areas are affected?** | `PE-001` Chapter 13 (Workspace Model), Chapter 14 (Navigation) | `GlobalHeader.tsx`'s own mounted `WorkspaceSwitcher` — no new navigation entry, per `CLAUDE.md §20.5`'s own "do not regress into an administration console." |

## 3. Architectural Justification When No Enterprise Experience Is Required

Per `CLAUDE.md §20.4`, a Business Activity satisfied only by a test suite, with no operable screen, does not meet the Enterprise Experience Standard **unless** the Work Package's own charter designates it infrastructure/backend-only, or the specific Business Activity is system-facing per its own governing specification. Where this applies, the worksheet's own "What does the user see?" row SHALL be answered with the specific citation, not left blank — WP-09's own BA-03 precedent: *"No frontend deliverable. `IRA-009 §7` explicitly characterizes `EX-C008-11` as 'system-facing — no dedicated screen, mirrors `IRA-008`'s own treatment of `EX-C001-08`'... `IMP-REPORT-WP-08`'s own Frontend section confirms that precedent built no UI section for the identical-shaped `EX-C001-08` either."*

**A justification that merely asserts "not applicable" without a specification citation and a same-shape precedent does not satisfy this section.**

## 4. Reuse-First Discipline for Enterprise Experience

Before any new screen, component, or navigation entry is proposed, the implementing session SHALL confirm, per `CLAUDE.md §19.5`:

1. Does an existing screen already own this capability's own navigational area (`admin-navigation.ts`, `config/workspaces.ts`, or their successors)? Extend it — WP-08's own `IdentityAccessScreen.tsx` and WP-09's own `WorkspaceSwitcher.tsx` extensions are the established precedent.
2. Does an existing DS-001-aligned component already provide the interaction pattern needed (`Menu`, `Spinner`, `Card`, `Button`, `Form`, `StatusBadge`, `useOverlay`)? Reuse it. Inventing a new component requires the explicit STOP-and-clarify discipline `CLAUDE.md §19.1`/`§20.5` already require when DS-001 does not define something a feature needs.
3. Does an existing state-machine hook pattern already establish the shape needed (`useIdentityManagement.ts`, `useMembershipManagement.ts`, `useOrganizationStructure.ts`)? Mirror its own discriminated-union `status` shape rather than inventing a new state-management convention.

## 5. World-Class Enterprise Experience Evaluation

Applied at Independent Certification, per `METH-003 §9` (Simplicity, Discoverability, Progressive Disclosure, Executive-first usability where applicable, Explainability, Accessibility, Keyboard-first productivity, Enterprise consistency, Responsive experience) — not restated here a second time. `CLAUDE.md §20.5`'s own constraint stands: interaction-quality reference only, never visual imitation of any named product.

## 6. States Checklist (unchanged, restated as a pointer)

Every screen/widget SHALL implement loading, empty, validation, error, and confirmation states against real API integration, per `CLAUDE.md §20.6` — not restated here; see that section directly.

---

## 7. Application to WP-10 (C-041, Configuration Management)

Per `PRODUCT-MILESTONE-ROADMAP.md §3` (Milestone 1), WP-10's own Enterprise Experience is not incidental — it is the primary carrier of Milestone 1's own stated Business Objective ("prove the platform reflects this specific enterprise... not a generic template"). WP-10's own IRA (`IRA-010`) SHALL apply this worksheet to every Business Activity it charters, with particular attention to the "What does the Executive see?" row — Configuration Management (branding, terminology, theme) is one of the few C-041-adjacent capabilities where an Executive Persona's own experience (a branded, enterprise-consistent platform, per `PE-001 §5.9`) is directly, not incidentally, affected.

---

*End of Enterprise Experience Realization Strategy. Governs Business Activity Plan B drafting from WP-10 onward, per `CLAUDE.md §21.3`.*
