# WP-09 — Business Value & Scope Validation Assessment

**Document ID:** WP-09-BUSINESS-VALUE-ASSESSMENT
**Subject:** WP-09 (C-008 — Workspace Management), as scoped by `IRA-009`
**Purpose:** Determine whether WP-09's currently-authorized-for-review scope (per `IRA-009 §4.8`) delivers sufficient business value to justify implementation, or whether the Repository Owner should select a different path, per Repository Owner Instruction "WP-09 Architecture Review — Business Value & Scope Validation," 2026-08-01.
**Type:** Advisory review artifact — not an IRA, not an ADR, not a Work Package, creates no capability, modifies no architecture. Same class as `RELEASE-A2-AI-CONFIGURATION-GOVERNANCE-REVIEW` / `AI-CONFIGURATION-TRACEABILITY-MATRIX`.
**Prepared By:** Engineering Governance session (Claude Code), under Repository Owner instruction
**Date:** 2026-08-01

**This is not an implementation exercise and not a redesign exercise.** No code, API, architecture, or approved roadmap is modified by this document. It answers one question: given the dependency `IRA-009` already disclosed (not introduced by WP-09), is WP-09's remaining executable scope still worth building.

---

## Governing Documents Reviewed

- `WP-09_Workspace_Management.md` (charter)
- `IRA-009_WP-09_Workspace_Management_Implementation_Readiness_Assessment.md` (Gap Analysis, Plan A, Plan B, Readiness Decision)
- `PE-001-C008_Workspace_Management.docx` v1.3 (via `IRA-009`'s own full-text extraction, §2/§4)
- `CAP-001_Enterprise_Capability_Registry.md` (C-008 registration, verbatim: "Provide contextual workspaces," Active, PE-001-governed)
- `WP-RTA-001_Closure_Report.md` §7 ("Not production ready" — zero real `TierResolver` implementations, zero real consumers), §9 (real tier-resolver work "not scheduled under any current or future milestone")
- `PRODUCT-MILESTONE-ROADMAP.md` §3 (Milestone 1 — "The Configured Enterprise"), §5 (EDR-1)
- `ARCHITECTURE-EVOLUTION-IMPLEMENTATION-PROGRAMME.md` (R15/Release B definition)
- `CLAUDE.md` §16–§20 (canonical authority resolution; Release Governance discipline applied throughout this repository's own prior releases)

No repository-wide review was performed. No background agent was launched. All findings below trace to the documents listed above, already produced or already existing before this exercise began.

---

## Phase 1 — Deliverable Analysis

Every EX in C-008's governed scope (`PE-001-C008` v1.3, 6 ERBs / 11 EXs) is listed below as a candidate deliverable, whether or not `IRA-009` found it in scope. This is the full universe WP-09 was chartered against, not only what survived the Gap Analysis — required to make Phase 2's percentage estimate auditable against the whole, not just the remainder.

| # | EX(s) / ERB | Business Purpose | Business Activity | Dependency | Depends on Access Evaluation? | Implementable Today? |
|---|---|---|---|---|---|---|
| 1 | `EX-C008-01`/`02` (`ERB-C008-01`) | Resolve and present the Workspaces a Person may enter, from real Membership/structural data | **BA-01** — Resolve and Present Available Workspace Candidates | C-005, C-007 (consumed, both Closed) | **No** — `Contract 5.3`'s Access Evaluation requirement is scoped to entry/switch/re-entry only, not discovery (`IRA-009 §4.1`) | **Yes** |
| 2 | `EX-C008-03`/`04` (`ERB-C008-02`) | Govern the actual transition into a Workspace Context | *(would-be)* Enter Workspace Context | C-002 Access Evaluation Outcome, unconditional (`Contract 5.3`, verbatim) | **Yes** | **No** — no production `TierResolver` exists for any tier (`WP-RTA-001 §7`) |
| 3 | `EX-C008-05` (`ERB-C008-03`) | Preserve continuity of an already-entered Workspace Context | *(would-be)* Continue Enterprise Journey Within Workspace Context | Presupposes `ERB-C008-02` has occurred | **Yes**, transitively | **No** — no reachable trigger; nothing to continue (`IRA-009 §4.3`) |
| 4 | `EX-C008-06`/`07` (`ERB-C008-04`) | Govern switching from one entered Workspace Context to another | *(would-be)* Switch Workspace Context | C-002 Access Evaluation Outcome, unconditional (`BR-C008-03`, verbatim, names "switch" explicitly) | **Yes** | **No** |
| 5 | `EX-C008-08`/`09` (`ERB-C008-05`) | Govern re-entry into a previously-participating Workspace Context | *(would-be)* Re-enter Previously Participating Workspace Context | C-002 Access Evaluation Outcome (`BR-C008-05`) + presupposes `ERB-C008-02` | **Yes**, doubly | **No** |
| 6 | `EX-C008-10` (`ERB-C008-06`) | Detect whether a currently-navigated-to Workspace Context remains valid (Membership/structure re-confirmation) | **BA-02** — Detect and Resolve Disrupted Workspace Context | C-005, C-007 (consumed) | **No** — Access Evaluation is named only "where relevant," conditional, not the unconditional Contract 5.3 requirement (`IRA-009 §4.6`) | **Yes** |
| 7 | `EX-C008-11` (`ERB-C008-06`) | Classify a rejection signal from a dependent capability's own hand-off attempt | **BA-03** — Classify Workspace Hand-off Rejection | `BR-C008-06`; real caller-in-waiting: `Backend/Services/AuthService/schemas/membership.py:222-224` (`DependentCapability.WORKSPACE_MANAGEMENT`, C-007 WP-03 BA-10) | **No** | **Yes** |

**Repository fact, not estimate:** 3 of 7 candidate deliverables (rows 1, 6, 7) are implementable today without Access Evaluation. 4 of 7 (rows 2–5) are not. At the ERB level this is `IRA-009 §4.8`'s own already-disclosed 3-of-6 (50%) exclusion; at the EX level, 5 of 11.

---

## Phase 2 — Business Value Analysis

No repository-native, numeric value-weighting model exists for capability deliverables. The classification below is derived directly from citable sources — `CAP-001`'s own Business Intent statement for C-008, and `PRODUCT-MILESTONE-ROADMAP.md`'s own stated Business Objective and Expected Demonstration Scenarios for the milestone C-008 belongs to — not invented.

| Deliverable | Value Classification | Basis (repository evidence) |
|---|---|---|
| Row 2 — Enter Workspace Context | **Critical** | This is the literal realization of CAP-001's own Business Intent for C-008: "Provide contextual workspaces." Entry is the moment a Workspace Context is provided. Excluded. |
| Row 4 — Switch Workspace Context | **Critical** | `PRODUCT-MILESTONE-ROADMAP.md` §3, Milestone 1's own Expected Demonstration Scenarios, first-listed: **"Switch workspaces."** This is not an inferred priority — it is the roadmap's own named customer-facing demo moment for the milestone C-008 belongs to. Excluded. |
| Row 5 — Re-enter Previously Participating Workspace Context | **Medium-High** | Governs a common enterprise return-to-context workflow; not separately named in the roadmap's demo scenarios, but doubly gated by the same unresolved dependency as row 2. Excluded. |
| Row 3 — Continue Enterprise Journey Within Workspace Context | **Medium** | Continuity/session-quality concern; not a standalone demo moment. Excluded (transitively — no reachable trigger). |
| Row 1 — Resolve and Present Available Workspace Candidates (BA-01) | **High** | Real, evidenced defect closure: today, every authenticated Person sees the same 3 hardcoded entries in `config/workspaces.ts` regardless of actual Membership (`IRA-009 §3`). BA-01 replaces this with real Membership-derived candidates — a genuine correctness improvement, and the data behind the roadmap's own "Switch workspaces" demo becoming credible rather than static. In scope. |
| Row 6 — Detect and Resolve Disrupted Workspace Context (BA-02) | **Medium** | Defensive/reliability capability; strengthens platform trustworthiness but is not itself named in any roadmap demonstration scenario. In scope. |
| Row 7 — Classify Workspace Hand-off Rejection (BA-03) | **Low-Medium** | System-facing, no dedicated screen (`IRA-009 §7`). Real value: closes a gap `C-007`'s own WP-03 BA-10 has been disclosing since that Work Package closed (`DependentCapability.WORKSPACE_MANAGEMENT`'s own docstring). In scope. |

**Estimated business value deliverable today:** substantially less than the 50%-by-ERB-count figure `IRA-009 §4.8` already discloses. Both deliverables independently rated **Critical** against citable evidence — Enter (CAP-001's own Business Intent) and Switch (the roadmap's own named demo scenario) — fall in the excluded set. Every deliverable that remains in scope (BA-01/02/03) is rated High or below, and the single High-rated item (BA-01) earns that rating primarily by making an *existing* mechanism (the ungoverned `WorkspaceSwitcher.tsx`) more correct, not by delivering new governed capability.

This is a qualitative, evidence-grounded judgment, not a fabricated percentage. No repository document defines a formula to convert ERB/EX counts into a value percentage; stating one here would be exactly the kind of guess `CLAUDE.md §17` prohibits. What is defensible, and stated plainly: **the exclusion is more severe in business-value terms than in ERB-count terms**, because the two Critical items are both excluded and no in-scope item reaches that rating.

---

## Phase 3 — Capability Coherence

**Question:** can an enterprise derive meaningful value from WP-09 without governed workspace entry, switching, and re-entry?

**Answer: partially yes, but not as "Workspace Management" in the sense C-008's own name and Business Intent describe.**

Evidence for "yes, partially":
- `IRA-009 §4.8`, verbatim: "What this Work Package *does* deliver: a real availability/candidate-resolution service, a disruption self-check, and closure of a gap `C-007` already disclosed waiting on." All three are real, cited, non-trivial improvements.
- The enterprise loses nothing: the existing, ungoverned `WorkspaceSwitcher.tsx` (`router.push(workspace.homeHref)`) is untouched and remains fully functional before and after WP-09 (`IRA-009 §3`). Users can navigate between workspaces exactly as they can today.
- BA-01 closes a real, evidenced defect: today's static 3-entry config shows every user the same candidates regardless of actual Membership. That is not a cosmetic gap — it is a correctness gap in what should already be a per-user, data-driven list.
- BA-03 closes a gap `C-007`'s own prior Work Package (WP-03) explicitly disclosed and left waiting for — a rare case where WP-09 resolves debt another, already-Closed Work Package named in advance.

Evidence for "not as C-008's own name promises":
- CAP-001's own Business Intent for C-008 is "Provide contextual workspaces" — and per `PE-001-C008`'s own Contract 5.3, "contextual" is realized specifically through the Access-Evaluation-gated entry transition, which is excluded. What ships is workspace *discovery*, not workspace *provision* in the governed sense the capability's own name and specification describe.
- The roadmap's own "Switch workspaces" demonstration scenario (Phase 2, above) is achievable at Milestone 1 only through the pre-existing, ungoverned `WorkspaceSwitcher.tsx` mechanism — which predates WP-09 and is not itself a WP-09 deliverable. WP-09 makes the candidate list behind that switcher accurate; it does not create the ability to switch, govern the switch, or add anything new to what "switch workspaces" can demonstrate.

**Coherence verdict:** WP-09 at this scope is a coherent, evidence-grounded **foundation-and-discovery layer** for C-008 — real, useful, zero architectural cost, and it closes disclosed debt. It is not a coherent standalone implementation of "Workspace Management" as CAP-001 and PE-001-C008 define the capability, because the transitions that make a workspace *contextual* (entry, switch, re-entry) are precisely what remains excluded.

---

## Phase 4 — Roadmap Impact

| Dimension | Assessment | Evidence |
|---|---|---|
| Architectural integrity | **Preserved.** | `IRA-009 §6`/`§8`: no new canonical Business Object, no new entity, no new pattern. Charter §10: "Architecture Impact: None." |
| Capability integrity | **At risk of a status/reality mismatch, not of technical harm.** | If WP-09 closes as "CLOSED — Certified" under the C-008 name without an explicit scope annotation, a reader of `WP-REG-001`/`CAP-001` could reasonably infer "Workspace Management" is complete when 3 of 6 ERBs — including both Critical-rated deliverables — remain unbuilt. This is a disclosure risk, not an architecture risk. |
| Release B objectives | **Preserved, and not solely dependent on WP-09.** | `PRODUCT-MILESTONE-ROADMAP.md` §3 frames Milestone 1's own Business/Customer Value around branding, terminology, and theme ("this looks and speaks like my company") — `C-041`/WP-10's own scope, not C-008's. WP-09's reduced scope does not defeat Milestone 1's stated objective; it does defeat one of the milestone's four named demonstration scenarios in its fullest sense (see below). |
| Future WP-10 | **No impact.** | WP-10 (C-041) is independently scoped; per `IRA-RELEASE-A`/Implementation Programme evidence already established this session, five of six C-041 facets have no dependency on WP-09 or Release A. |
| Future WP-11 | **No impact.** | WP-11 (Milestone 2) is gated on Milestone 1's exit criteria (both WP-09 and WP-10 Closed/Certified) and is otherwise unrelated to C-008's internal ERB scope. |
| EDR-1 (Milestone 1 demo checkpoint) | **Named demo scenario weakened, not eliminated.** | `PRODUCT-MILESTONE-ROADMAP.md` §3 lists "Switch workspaces" as the first Expected Demonstration Scenario for Milestone 1; §5 sets EDR-1's own Demonstration Readiness Criteria as "WP-09 and WP-10 both Closed and Certified." Under WP-09's disclosed scope, that criterion can be met while "switch workspaces" is demoed using pre-existing, ungoverned code unchanged by WP-09 — the demo remains possible, but WP-09 contributes nothing new to it beyond more credible candidate data. |
| Downstream roadmap risk | **A real, currently-unscheduled gap.** | `WP-RTA-001_Closure_Report.md §9` already discloses that real `TierResolver` implementation work is "not scheduled under any current or future milestone." This is now the root cause narrowing a third Work Package (`WP-05`, `WP-08`'s `ERB-C001-01`, now `WP-09`'s majority scope), and the roadmap contains no chartered path to resolve it. Absent a Repository Owner scheduling decision, C-008's excluded ERBs have no future Work Package to land in. |

---

## Phase 5 — Repository Owner Options

Only options directly supported by the evidence above are presented. None requires redesigning WP-09, C-002, or the approved roadmap.

**Option 1 — Proceed with WP-09 exactly as scoped in `IRA-009` (BA-01/02/03).**
Matches the precedent already set by WP-08 (which proceeded with `ERB-C001-01` excluded, disclosed as `TD-102`, and closed successfully). Delivers real value now (candidate-accuracy defect closure, C-007 gap closure, disruption detection) at zero architectural cost, with no dependency on an unscheduled resolver. Risk: the capability's colloquial "Workspace Management" expectation is not met, and — absent explicit disclosure at closure — could be perceived as met.

**Option 2 — Proceed with the same technical scope, under an explicitly relabeled delivery increment.**
Same BA-01/02/03 content as Option 1, but the closure documentation (`WP-REG-001`, `CAP-001`-facing status) explicitly states C-008 is *partially* realized, not fully realized, after WP-09 closes — preventing the status/reality mismatch flagged in Phase 4 without reworking the already-produced charter/IRA. Distinguishes itself from Option 1 only in disclosure discipline, not in scope.

**Option 3 — Defer WP-09 until the Access Evaluation dependency (a production `TierResolver`) is resolved.**
Would deliver C-008 in full, ungapped form. Cost, per evidence: `WP-RTA-001_Closure_Report.md §9` states this work is currently unscheduled on any milestone — deferring on it has no evidence-based timeline. Because Milestone 1's own Exit Criteria requires *both* WP-09 and WP-10 Closed/Certified (`PRODUCT-MILESTONE-ROADMAP.md §3`), and WP-10 has no dependency on WP-09, this option stalls all of Milestone 1 and EDR-1 — not just C-008 — for a dependency with no scheduled resolution.

**Option 4 — Proceed with WP-09 as scoped (Option 1's content) and concurrently flag the Access Evaluation production-readiness gap as a named, unscheduled roadmap risk requiring a Repository Owner scheduling decision.**
Combines Option 1's pragmatic progress with Option 2's transparency: no rework of `WP-09`/`IRA-009`, but an explicit acknowledgment — separate from Technical Debt, since `TD-102`-class entries already exist for the underlying cause — that three Work Packages have now been narrowed by the same unscheduled gap, and the roadmap itself currently has no answer for when that changes.

---

## Final Recommendation

**Option 4.** Evidence-based reasoning:

1. Precedent already exists and succeeded: WP-08 proceeded on an analogous, disclosed exclusion and closed cleanly through the full five-gate sequence. Nothing about WP-09's situation is structurally different — it is a larger proportion of the same, already-accepted class of gap.
2. The in-scope deliverables are real, not filler: BA-01 fixes an existing correctness defect (hardcoded candidates shown to every user regardless of Membership), and BA-03 closes debt another, already-Closed Work Package explicitly disclosed waiting on.
3. Deferral (Option 3) has no evidence-based endpoint — the blocking dependency is unscheduled on any milestone — and would stall Milestone 1 and EDR-1 in their entirety, not only C-008, since WP-10's own independent readiness cannot substitute for WP-09 under the roadmap's own stated Exit Criteria.
4. The genuine risk this review surfaces is not technical but reputational/governance: a "Workspace Management — Closed, Certified" status that a reader could mistake for the full, colloquial capability. That risk is addressed by disclosure, not by redesign or delay — hence Option 4 over silent Option 1.
5. This is the third Work Package the same unscheduled resolver gap has narrowed. That pattern itself is now repository evidence the Repository Owner has not yet seen assembled in one place, and belongs in front of them as its own scheduling question — independent of whether WP-09 proceeds.

**Recommendation to the Repository Owner:** authorize WP-09 implementation at the scope `IRA-009 §4.8` already determined, with the closure documentation explicitly stating partial C-008 realization (Option 4); and separately decide whether to schedule the underlying Access Evaluation `TierResolver` production work on the roadmap, since it now blocks three Work Packages and appears on none.

---

*End of WP-09-BUSINESS-VALUE-ASSESSMENT. No implementation performed. No architecture modified. No WP-09/C-002 redesign proposed. Awaiting Repository Owner decision on Phase 5.*
