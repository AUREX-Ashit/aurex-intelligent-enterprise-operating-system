# Platform Dependency Assessment — Access Evaluation TierResolver

**Document ID:** PLATFORM-DEPENDENCY-ASSESSMENT-TIERRESOLVER
**Subject:** Whether the unresolved Access Evaluation `TierResolver` has become a platform-level dependency, rather than a per-Work-Package scoping detail, per Repository Owner Instruction "Platform Dependency Assessment — Access Evaluation TierResolver," 2026-08-01.
**Type:** Advisory review artifact — not an IRA, not an ADR, not a Work Package, creates no capability, modifies no architecture, modifies no roadmap.
**Prepared By:** Engineering Governance session (Claude Code), under Repository Owner instruction
**Date:** 2026-08-01

**This is not an implementation exercise, not a redesign exercise, and not a Work Package planning exercise.** It answers one question: has the same, repeatedly-disclosed dependency now crossed from "a scoping detail three Work Packages happened to share" into "a platform dependency the roadmap itself should represent."

---

## Governing Documents Reviewed

- `WP-08_Identity_Management.md`, `IRA-008_...md` §4.1/§4.5
- `WP-RTA-001_Closure_Report.md` §4, §7, §9
- `WP-09_Workspace_Management.md`, `IRA-009_...md` §4
- `WP-09-BUSINESS-VALUE-ASSESSMENT.md` (Phase 4)
- `CAP-001_Enterprise_Capability_Registry.md` (C-002, C-008 registrations)
- `PRODUCT-MILESTONE-ROADMAP.md` §3 (Milestones 0–3), §5 (EDR-1/EDR-2)
- `ARCHITECTURE-EVOLUTION-IMPLEMENTATION-PROGRAMME.md` (Release B/R15 definition)
- `WP-REG-001_Enterprise_Work_Package_Register.md` §5 (WP-05, WP-08, WP-09, WP-RTA-001 rows), §9 (WP-08 chartering-decision record)
- `WPR-001_Work_Package_Roadmap.md`
- `TECH-DEBT.md` (TD-072, TD-079, TD-080, TD-100, TD-102, TD-103, and their detailed entries)
- `IRA-005_WP-05_...md` §12
- `CLAUDE.md` §16–§20 (Release Governance discipline as applied by every prior release/WP in this repository)

No repository-wide review was performed; the search below is a targeted traceability sweep for the exact terms "TierResolver" / "Access Evaluation Outcome" / "Access Evaluation resolver," which is what Phase 1 itself requires, not a new audit. No background agent was launched.

---

## Phase 1 — Evidence Traceability

A direct repository search for "TierResolver" returns matches in **17 files**. Every substantive occurrence is enumerated below, in chronological order of first disclosure.

| # | Document | Context | Capability | Work Package | Release | Architectural Impact |
|---|---|---|---|---|---|---|
| 1 | `IRA-005_WP-05_...md` §12 | Original disclosure: a genuine, affirmative Permitted/Denied Access Evaluation Outcome requires a real, production `TierResolver`. None existed. Repository Owner authorized WP-05 at **minimum scope only** — BA-01 Unresolved/Deferred branches only, BA-03's classification portion only. | C-002 | WP-05 | Milestone 0 (Foundation) | None — scoping decision only, no architecture changed. |
| 2 | `TD-079`/`TD-080`, `TECH-DEBT.md` | Downstream symptoms of the WP-05 exclusion: no persona-specific gate exists for C-002 endpoints; no `GET` read endpoint for Access Evaluation Outcome (scope never exercised the read path). | C-002 | WP-05 | Milestone 0 | None. |
| 3 | `WP-RTA-001_Closure_Report.md` §7 | **"Not production ready."** Verbatim: "Zero real data connections exist. No production resolver has been written for any of the five tiers, including Domain Permission." Runtime scaffolding (Protocol, registry, orchestrator, pipeline) is complete and tested (106 passing tests) — the architecture for a `TierResolver` exists and is approved; no concrete implementation of it exists for any tier. | C-002 (runtime foundation, owns no Business Object itself) | WP-RTA-001 | Milestone 0 | None — RTA-001's own architecture is unchanged; this is an implementation-completeness finding against already-approved architecture. |
| 4 | `WP-RTA-001_Closure_Report.md` §9 | **"Real tier data resolution"** listed explicitly among items "not scheduled under any current or future milestone." Concrete `TierResolver` implementations for all five tiers — including Domain Permission, which "has real data available (WP-02) but no implementation written" — remain unbuilt. Named User/Group/Approval-Authority-linkage/Business-Role-domain-scoping tiers additionally require data models that do not exist anywhere in the repository. | C-002 and, by extension, every tier URA-001-76 defines | WP-RTA-001 | Milestone 0 | None — confirms the gap is implementation, not specification. |
| 5 | `TD-072`, `TECH-DEBT.md` | `AuthorizationContext` models Roles/Permissions/Assignments as opaque identifier tuples rather than richer typed objects — "a deliberate M1 simplification, since no concrete `TierResolver` exists yet." | Runtime | WP-RTA-001 | Milestone 0 | None — a downstream design simplification caused by the same absence. |
| 6 | `IRA-008_...md` §4.1, `WP-REG-001` §9 (WP-08 chartering row) | `ERB-C001-01` (`EX-C001-01`/`02`, Establish New Identity Context) excluded in full — an unconditional Access Evaluation Outcome requirement, "structurally unobtainable," identical root cause to `IRA-005 §12`. This is also the record of the **chartering-level decision**: the same blocker was weighed when choosing C-001 over C-008 as WP-08's own charter target. | C-001 | WP-08 | Milestone 0 | None. |
| 7 | `TD-100`, `TD-102`, `TECH-DEBT.md` | `TD-102`: `ERB-C001-01` excluded in full. `TD-100`: administrator-initiated Identity recovery branch excluded, same blocker. | C-001 | WP-08 | Milestone 0 | None. |
| 8 | `TD-103`, `TECH-DEBT.md`, found by `VV-AUDIT-WP-08` (Gate 2) | **A materially different manifestation, not merely another exclusion:** BA-02 (already built, already shipped) silently never requests an Access Evaluation Outcome at all, in tension with `PE-001-C001`'s own unconditional `BR-C001-03`. This is a Business Rule non-conformance inside code that *is* running, discovered independently, not disclosed at chartering time — evidence that the same absence produces defects, not only disclosed exclusions, once a Work Package's own scoping analysis relies on a weaker textual basis than the strongest applicable rule. | C-001 | WP-08 | Milestone 0 | None directly, but is the first evidence this gap can produce a silent conformance defect rather than only a disclosed scope reduction. |
| 9 | `WP-09_Workspace_Management.md` §2/§8, `IRA-009_...md` §4.2/§4.4/§4.5 | 3 of 6 ERBs excluded (`ERB-C008-02`/`03`/`04`/`05`) — governed workspace entry, continuation, switch, and re-entry all require the same unconditional Access Evaluation Outcome. Largest proportional exclusion of any Work Package to date. | C-008 | WP-09 | Release B (Milestone 1) | None. |
| 10 | `WP-09-BUSINESS-VALUE-ASSESSMENT.md` Phase 4 | Independently concluded this is "a real, currently-unscheduled gap" and "now the root cause narrowing a third Work Package... with no chartered path to resolve it." | C-008 | WP-09 | Release B (Milestone 1) | None — advisory finding only. |

**Determination: the dependency is now systemic.** It has recurred across every Work Package to date that charters a governed action requiring an affirmative authorization decision (WP-05, WP-08, WP-09), across the Work Package that built the runtime foundation itself (WP-RTA-001), and has begun producing not only disclosed scope reductions but at least one independently-discovered conformance defect in already-shipped code (`TD-103`). No Work Package chartered since `WP-RTA-001`'s own closure has been exempt from this pattern when its own governed scope required an affirmative Permitted/Denied determination.

---

## Phase 2 — Dependency Analysis

| Item | Blocked? | Evidence |
|---|---|---|
| **C-002** (Access Management) | **Yes, partially** — already CLOSED at minimum scope; BA-01's Permitted/Denied branches and BA-03's re-resolution path remain excluded from WP-05's own scope entirely, per `WP-REG-001` §47 ("Relationship to WP-05"): "resolving them requires WP-05's own future, separately-scoped gap analysis... once a real, production `TierResolver` exists." |
| **C-008** (Workspace Management) | **Yes, majority scope** — 3 of 6 ERBs (`IRA-009 §4.8`). |
| **Future Workspace capabilities** | **Indeterminate from current evidence, but at risk.** No future C-008-adjacent capability is currently chartered or specified beyond `PE-001-C008` itself; the risk is structural (any future governed-transition EX will recur the same pattern), not evidenced against a named, not-yet-existing capability. Stated as risk, not fact, since no such capability exists in `CAP-001` today. |
| **Enterprise Experience** (`CLAUDE.md §20`) | **Not blocked as a standard.** §20 governs interaction quality, demonstrability, and completeness of *whatever scope* a Work Package is authorized to deliver — it does not itself require governed Access Evaluation flows to be built. WP-08 and (pending) WP-09 both satisfy §20 at their own disclosed, reduced scope. |
| **Release B** (Milestone 1) | **Not blocked.** `PRODUCT-MILESTONE-ROADMAP.md` §3's own Exit Criteria for Milestone 1 is "WP-09 and WP-10 both Closed and Certified" — a status achievable at `IRA-009`'s own disclosed scope, per `WP-09-BUSINESS-VALUE-ASSESSMENT.md`. WP-10 (C-041) has no dependency on Access Evaluation anywhere in its own scope evidence gathered this session. |
| **EDR-1** | **Not blocked from occurring; one named demo scenario weakened.** `PRODUCT-MILESTONE-ROADMAP.md` §3 lists "Switch workspaces" as Milestone 1's first Expected Demonstration Scenario — achievable at EDR-1 only via the pre-existing, ungoverned `WorkspaceSwitcher.tsx`, not via any new WP-09 deliverable (`WP-09-BUSINESS-VALUE-ASSESSMENT.md` Phase 3/4). EDR-1's own Demonstration Readiness Criteria (§5) does not itself require governed switching — only "WP-09 and WP-10 both Closed and Certified." |
| **Release C** (Milestone 2, WP-11) | **No evidence of blockage found.** `PRODUCT-MILESTONE-ROADMAP.md` §3's own Milestone 2 Capabilities (C-090/C-092/C-093, Enterprise Discovery/Knowledge Graph/Search) are not cited anywhere in `PE-001` or `CAP-001` as depending on an Access Evaluation Outcome. No document reviewed for this assessment ties Milestone 2 to `TierResolver`. Absence of evidence is reported as such, not extrapolated into a finding. |
| **Additional capabilities affected** | `WP-RTA-001_Closure_Report.md §9` names the underlying gap as spanning **all five URA-001-76 tiers**, not only the Domain Permission tier C-002/C-008 have exercised so far: Named User, Group, Approval-Authority-linkage, and Business-Role-domain-scoping tiers "additionally require data models that do not exist anywhere in this repository." This means the dependency's own footprint is wider than the three Work Packages that have hit it so far — it is bounded by URA-001's own five-tier model, not by C-002/C-008 specifically. |

**Conclusion:** the dependency currently blocks real, disclosed scope within C-002 and C-008 only. It does not currently block any Milestone/Release exit criterion, because every affected Work Package to date has scoped around it and disclosed the reduction rather than being prevented from closing. Its risk is forward-looking and structural: any future governed-transition Enterprise Experience, in any capability, that requires an affirmative Permitted/Denied decision will recur this same pattern, per the five-tier scope `WP-RTA-001 §9` itself already defines.

---

## Phase 3 — Root Cause Analysis

Evaluated directly against the classifications the Repository Owner's own instruction lists, with repository evidence, not speculation:

- **Missing architecture — NO.** `RTA-001`'s own `TierResolver` Protocol, `ResolverRegistry`, and `ResolverOrchestrator` already exist, are approved, and are tested (106 passing tests, `WP-RTA-001_Closure_Report.md §4`). The interface every future tier resolver must implement is fully specified. This is not an architecture gap.
- **Incomplete implementation — YES, primary classification.** `WP-RTA-001_Closure_Report.md §7`, verbatim: "No production resolver has been written for any of the five tiers, including Domain Permission [which] has real data available... but no implementation written." The architecture that defines *how* to build a `TierResolver` is complete; no concrete tier implementation was ever built against it, by any Work Package to date.
- **Missing Work Package — YES, contributing classification.** `WP-REG-001` §45 (WP-RTA-001 row), verbatim: "no successor Work Package is chartered by this entry." `WP-RTA-001_Closure_Report.md §9` lists "Real tier data resolution" among items explicitly excluded from that Work Package's own delivered scope and "not scheduled under any current or future milestone." No Work Package in `WPR-001` or `WP-REG-001` today owns building a real `TierResolver`.
- **Missing roadmap item — YES, contributing classification.** Neither `PRODUCT-MILESTONE-ROADMAP.md` nor `ARCHITECTURE-EVOLUTION-IMPLEMENTATION-PROGRAMME.md` names this dependency as a scheduled item at any Milestone or Release. It appears only as a recurring, per-Work-Package disclosure (Technical Debt entries), never as a roadmap-level line.
- **Technical Debt — PARTIALLY, but insufficient as the sole classification.** Individual manifestations are correctly recorded as Technical Debt (`TD-072`, `TD-079`, `TD-080`, `TD-100`, `TD-102`, `TD-103`, `TD-070`-class entries per `IRA-005 §12`). But Technical Debt entries are, by `CLAUDE.md §19.8`'s own design, per-Work-Package, non-blocking observations — they record symptoms at the point each Work Package encounters them. None of them, individually or collectively, constitutes a plan to resolve the shared root cause; each simply re-discloses it. Treating this purely as "more Technical Debt" is the classification least supported by the evidence, precisely because the same cause has now generated Technical Debt in three separate registers' worth of entries without the underlying gap narrowing at all.
- **Missing Release activity — YES, contributing classification.** No Release (A, B, or currently-planned C/D) charters closing this gap as one of its own objectives, per direct review of `ARCHITECTURE-EVOLUTION-IMPLEMENTATION-PROGRAMME.md`'s Release Plan and `PRODUCT-MILESTONE-ROADMAP.md`'s own Milestone definitions.

**Root cause, stated precisely:** this is **incomplete implementation of already-approved architecture (RTA-001), for which no Work Package, Release, or roadmap item currently exists to complete it.** It is not a defect, not a design gap, and not resolvable by writing more Technical Debt entries — each of which has, so far, only recorded the same absence again.

---

## Phase 4 — Implementation Options

Repository-supported options only. None requires new architecture (RTA-001's own Protocol already defines the shape a `TierResolver` must take) or redesign of any Work Package already Closed.

| Option | Architectural Impact | Repository Impact | Governance Impact | Release Impact | Work Package Impact | Business Impact |
|---|---|---|---|---|---|---|
| **1 — Leave as Technical Debt (status quo)** | None. | None — no new document. | None — continues the existing per-WP disclosure pattern. | None to Release B; every future release recurs the same disclosure per affected Work Package. | Any future WP touching a governed transition (C-002, C-008 residual scope, or any new capability with an affirmative-authorization EX) will re-disclose the identical blocker, as WP-05/08/09 already have three times. | Continued deferral of governed workspace/identity transitions and any future capability with the same shape; no new business value unlocked, none lost beyond what is already excluded. |
| **2 — Small standalone implementation activity** (e.g., a minimal, real Domain Permission `TierResolver`, the tier `WP-RTA-001 §9` itself identifies as nearest to buildable — "real data available (WP-02) but no implementation written") | None — implements RTA-001's existing Protocol, does not extend it. | New code in `Backend/Runtime/AuthorizationEngine/`, first real consumer integration via the existing `AuthorizationAdapter` seam (`WP-RTA-001` M4). | Requires its own IRA-style readiness check (proportionate to its size), but not a full capability-owning Work Package charter. | Could unblock WP-05's own excluded BA-01 Permitted/Denied branches and WP-08/WP-09's excluded ERBs for the Domain Permission tier specifically — other tiers remain blocked (Named User/Group/Approval-Authority/Business-Role tiers still lack the underlying data models per `WP-RTA-001 §9`). | Reopens WP-05 (already Closed — Certified) for a scope extension, or requires a new, narrowly-scoped Work Package — either has real governance overhead disproportionate to "small." | Meaningfully unblocks the single most business-value-critical excluded item found in `WP-09-BUSINESS-VALUE-ASSESSMENT.md` Phase 2 (governed workspace entry) for at least one tier. |
| **3 — Create a dedicated, roadmap-visible platform dependency work item** (a named entry in `WPR-001`/`ARCHITECTURE-EVOLUTION-IMPLEMENTATION-PROGRAMME.md`, distinct from a per-WP Technical Debt line, that makes the dependency itself visible and schedulable — without yet building anything or committing to Option 2 vs. Option 4's specific mechanism) | None. | None yet — this option is disclosure/scheduling only; a subsequent Repository Owner decision selects the actual resolution mechanism. | Converts a repeatedly-rediscovered, per-WP-buried finding into a single, roadmap-level, Repository-Owner-visible item — directly addressing the systemic pattern Phase 1/3 establish, without prematurely committing engineering effort. | None to current Release B; positions the dependency for deliberate scheduling ahead of whichever future release first requires a governed Permitted/Denied action. | None to any existing Work Package. | Lowest-cost option that stops the pattern of the same finding being independently re-discovered by every future Work Package's own IRA — directly reduces repeated governance overhead. |
| **4 — Introduce a new, full-lifecycle Work Package** dedicated to real `TierResolver` implementation across one or more tiers, plus first consumer integration | None — implements RTA-001's existing Protocol. | Full charter, IRA, implementation, and five-gate closure per `CLAUDE.md §19.7`/§19.7b. | Highest governance cost of any option — a full Work Package lifecycle. | Directly resolves the root cause at whatever tier(s) are scoped; could unblock C-002/C-008's own excluded ERBs for those tiers specifically. | Largest option; does not itself modify any existing Closed Work Package, but sequencing it (before/after Release B, C) is a roadmap decision this assessment does not make. | Highest potential business value recovered (unblocks governed Enter/Switch/Re-enter for Workspace, and Permitted/Denied for Access Management), at the highest one-time governance/engineering cost. |
| **5 — Combination: Option 3 now, Option 2 or 4 as a subsequent, separately-scoped decision** | None. | Same as Option 3 initially; Option 2/4's own impact applies only once and if selected later. | Matches this repository's own established two-step discipline (e.g., `IRA-005 §10.2 item 3` was first recorded as a governance question, then separately resolved as Option 2/WP-RTA-001 in a later, distinct decision) — disclosure and scheduling first, resolution-mechanism decision second. | Same as Option 3. | Same as Option 3, with the resolution-mechanism Work Package (if any) chartered only after a deliberate, separate Repository Owner decision. | Preserves all of Option 3's low-cost visibility benefit while keeping the door open to Option 2 or Option 4 without committing to either prematurely. |

---

## Phase 5 — Roadmap Impact

**The current roadmap remains valid.** Reasoning, evidence-based:

- No Milestone or Release exit criterion currently defined in `PRODUCT-MILESTONE-ROADMAP.md` or `ARCHITECTURE-EVOLUTION-IMPLEMENTATION-PROGRAMME.md` requires the excluded scope. Milestone 1's own Exit Criteria is "WP-09 and WP-10 both Closed and Certified" — a status reachable at each Work Package's own disclosed, reduced scope, as WP-08 already proved by closing successfully under the identical pattern.
- Milestone 2 (Release C, WP-11) shows no evidenced dependency on Access Evaluation or `TierResolver` anywhere reviewed for this assessment.
- Every Work Package affected so far (WP-05, WP-08, WP-09) scoped around the gap through its own IRA, per this repository's own established Reuse→Configure→Extend→Compose→Create discipline (`CLAUDE.md §19.5`) — the roadmap's sequencing and milestone structure did not need to change to accommodate any of them.

**The roadmap does have one gap, not a defect:** it contains no item, at any point in Release A through the currently-defined Release D, that closes this dependency. Per Phase 3's own root cause finding, this is a missing roadmap item, not evidence the existing sequence is wrong.

**Minimum change, if the Repository Owner elects to correct this now (not performed by this assessment):** add a single, explicitly-named platform dependency entry to `WPR-001`/`ARCHITECTURE-EVOLUTION-IMPLEMENTATION-PROGRAMME.md` (Option 3/5, Phase 4) naming the Access Evaluation `TierResolver` production-readiness gap and its own resolution trigger. This does not require reordering any Milestone, renaming any Release, or altering any current Work Package's own scope — it is an addition, not a restructuring, consistent with "smallest possible correction."

---

## Phase 6 — Repository Owner Recommendation

**Recommendation: Option 3/5 — register the Access Evaluation `TierResolver` production-readiness gap as a single, named, roadmap-visible platform dependency, without yet selecting Option 2 or Option 4 as its resolution mechanism.**

This is the lowest-risk, highest-value path forward, for reasons directly grounded in the evidence above:

1. **It matches this repository's own established precedent for exactly this kind of decision.** `IRA-005 §10.2 item 3` was first recorded as an open governance question, then separately resolved later as Option 2 (chartering `WP-RTA-001`) — disclosure and scheduling preceded the resolution-mechanism decision, not the reverse. This recommendation repeats that same, already-proven two-step pattern.
2. **It directly addresses the finding this assessment exists to make:** the dependency is now systemic (Phase 1), has produced not only disclosed exclusions but at least one independently-discovered conformance defect in shipped code (`TD-103`, Phase 1 item 8), and currently has no home anywhere in the roadmap (Phase 3). A visible, named roadmap entry is the smallest change that stops each future Work Package from independently re-discovering the same absence.
3. **It carries zero architectural, Work Package, or Release risk.** No Milestone/Release exit criterion is currently blocked (Phase 2), so there is no urgency requiring the heavier Option 2 or Option 4 today — and committing to either prematurely, before a deliberate scoping decision, risks exactly the kind of under-scoped, expedient fix `CLAUDE.md §18`/§19.4 caution against.
4. **It preserves optionality.** Once visible on the roadmap, the Repository Owner can select Option 2 (a narrow Domain Permission resolver, the nearest-to-buildable tier per `WP-RTA-001 §9`) or Option 4 (a full Work Package across more tiers) at the point it actually needs to be resolved — informed by which future capability first requires it, rather than guessed now.

---

*End of PLATFORM-DEPENDENCY-ASSESSMENT-TIERRESOLVER. No implementation performed. No architecture modified. No Work Package (including WP-09) begun or redesigned. No roadmap document modified — Phase 5's own minimum change is a recommendation only. Awaiting Repository Owner decision.*
