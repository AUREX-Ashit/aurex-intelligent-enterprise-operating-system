# WP-09 — Workspace Management (C-008)

**Work Package ID:** WP-09
**Type:** Business Capability
**Capability ID / Name:** C-008 — Workspace Management
**Governing Capability Specification:** `PE-001-C008_Workspace_Management.docx`, Version 1.3 (Chapter 9.16: "APPROVED for publication as a Canonical Capability Experience Specification")
**Status:** **CLOSED — CERTIFIED** (2026-08-02). Implementation authorized per Repository Owner Instruction "Release B – WP-09 Implementation Authorization," committed `90544cb`/`6ce9bd3`/`d648150`; full five-gate closure sequence complete (`CLAUDE.md §19.7b`) — see `IMP-REPORT-WP-09_Workspace_Management.md` and `RRA-WP-09_Workspace_Management_Release_Readiness_Audit.md`.
**Chartered By:** Repository Owner instruction ("Release B Initiation"), 2026-08-01
**Chartering Date:** 2026-08-01
**Governing IRA:** `IRA-009_WP-09_Workspace_Management_Implementation_Readiness_Assessment.md` — **Accepted, 2026-08-01**, per Repository Owner Instruction "Governance Consolidation & Transition to WP-09," following consistent review conclusions in `WP-09-BUSINESS-VALUE-ASSESSMENT.md` and `PLATFORM-DEPENDENCY-ASSESSMENT-TIERRESOLVER.md`

**This charter originally authorized progression to the Implementation Readiness Assessment stage only; it did not itself authorize implementation.** Per this repository's own established precedent (WP-01 through WP-08's own charter documents), full-lifecycle implementation authority required a separate, subsequent Repository Owner authorization after the IRA was reviewed and accepted — **granted 2026-08-01** ("Release B – WP-09 Implementation Authorization"). WP-09 is now CLOSED — CERTIFIED, per the Status line above.

---

## 1. Purpose / Business Objective

Per CAP-001's own Business Intent for C-008, verbatim: **"Provide contextual workspaces."** PE-001-C008 §1.2 restates this without expansion or redefinition — the capability's Primary Specification is PE-001 itself (Chapter 13, Workspace Model), since no separate Constitutional-layer document owns Workspace semantics anywhere in this repository (confirmed: no reference to Workspace as a data object, domain entity, or technical construct exists in CMD-001, ERG-001, URA-001, RTA-001, or Master Technical Architecture).

## 2. Scope

Per PE-001-C008 v1.3, six Enterprise Relationship Boundaries (ERBs), eleven Enterprise Experiences (EXs):

| ERB | Title | Realizing EX(s) |
|---|---|---|
| ERB-C008-01 | Resolve Available Workspace Context | EX-C008-01, EX-C008-02 |
| ERB-C008-02 | Enter Workspace Context | EX-C008-03, EX-C008-04 |
| ERB-C008-03 | Continue Enterprise Journey Within Workspace Context | EX-C008-05 |
| ERB-C008-04 | Switch Workspace Context | EX-C008-06, EX-C008-07 |
| ERB-C008-05 | Re-enter Previously Participating Workspace Context | EX-C008-08, EX-C008-09 |
| ERB-C008-06 | Resolve Workspace Context Disruption | EX-C008-10, EX-C008-11 |

Seven Business Rules (BR-C008-01 through 07) and ten numbered Experience Contracts (5.1–5.10) govern realization — full text reviewed and cited in `IRA-009`. **Which of these ERBs/EXs this Work Package is actually authorized to implement is determined by the accompanying IRA's own Gap Analysis (`IRA-009 §4`), not pre-decided here** — per this repository's own established charter/IRA separation of concerns (WP-01 through WP-08 precedent: the charter states the capability's full governed scope; the IRA determines what of that scope is presently buildable).

**Disclosed at chartering time, not deferred to IRA discovery:** PE-001-C008's own Contract 5.3 states C-008 "SHALL request, and SHALL NOT compute, an Access Evaluation Outcome" for every Workspace entry, switch, and re-entry (ERB-C008-02, -04, -05 — the majority of this capability's governed scope). C-002's own Access Evaluation resolver remains minimum-scope only, with no production `TierResolver` for any tier (`WP-RTA-001` Closure Report §7, unchanged since WP-08's own closure). This is the identical structural blocker WP-08's own chartering decision (`WP-REG-001` §9, 2026-07-31) already evaluated and used as the explicit reason to charter C-001 over C-008 at the same decision point this charter now revisits. See §9 (Risks) and `IRA-009 §4` for the full, disclosed impact on this Work Package's actually-buildable scope.

## 3. Business Activities

Not pre-specified in this charter. Per this repository's own established convention (IRA-005 §12, IRA-007, IRA-008 §5 — Business Activities are determined during Gap Analysis, not chartered in advance), the Business Activities this Work Package will realize are determined by `IRA-009 §5` (Plan A), against whichever EXs that Gap Analysis finds in scope.

## 4. Out of Scope

Per PE-001-C008 §1.5, verbatim:

> Membership existence, standing, or effective validity (C-007); Access evaluation and authorization decisions (C-002); Role and Permission definition or assignment (C-003); Organization identity, existence, or validity (C-004); Enterprise Structure, EnterpriseNode, EnterpriseRelationship, or EnterpriseView definition (ERG-001/C-005); Presentation Architecture, screen or widget design (SD-001); Universal Business Object rules (SD-002); Enterprise Interaction mechanics (SD-003); Runtime orchestration (RTA-001); Business Activity implementation (IMP-001); Canonical Data Model ownership (CMD-001); any API, database, microservice, frontend component, or technical state machine; determination of which PE-001 §13.5 Workspace Type(s) a given Membership/Organization/structural anchor may host (**Pending Canonical Binding** — no canonical authority in the current repository establishes this determination, and this capability does not invent one).

## 5. Dependencies

Per PE-001-C008 §1.9 / Document Control: C-002 (Access Evaluation Outcome — consumed, never computed; **the blocking dependency**, §2 above), C-003/URA-001 (Role/Permission — referenced only), C-004 (Organization existence/validity — consumed, never redefined), C-005/ERG-001 (structural placement, Home Node — consumed, never redefined), C-006 (Authoritative Person Context — consumed, never redefined), C-007 (Membership Authority Consequence Context, Home Node — consumed, never redefined), URA-001 (overall authorization model), PE-001 Chapters 11/13/14/15. **No dependency on RTA-001 is stated in the specification itself**, though the Access Evaluation blocker's own root cause traces to RTA-001/`WP-RTA-001`'s TierResolver.

All named upstream capabilities (C-002 through C-007) are already Closed and Certified (WP-01 through WP-07). The one live dependency risk is not a missing capability — it is C-002's own disclosed minimum-scope limitation.

## 6. Enterprise Experience Requirement (`CLAUDE.md §20`)

This Work Package is chartered under the Enterprise Experience Standard (`CLAUDE.md §20`), governing WP-08 onward. Per §20.7, Independent Certification shall not pass until backend capability, Enterprise Experience, navigation, and end-to-end demonstrability are all complete for whatever scope the IRA determines is in bounds — the accompanying IRA must therefore produce both a Plan A (Business Capability Implementation) and a Plan B (Enterprise Experience Implementation), per the same dual-plan requirement WP-08's own charter established.

## 7. Deliverables / Acceptance Criteria

Deliverables and acceptance criteria are scope-dependent and therefore determined by `IRA-009`'s own Readiness Decision (§8), not fixed here in advance of that determination — consistent with §3 above. At minimum, whatever scope is authorized shall meet every element of `CLAUDE.md §14`'s Definition of Done, including Independent Certification, Verification & Validation, and Release Readiness per `§19.7`/`§19.7b`, extended by `§20.7`.

## 8. Risks

- **Primary, disclosed risk:** the majority of C-008's governed scope (ERB-C008-02, -04, -05 — Enter, Switch, and Re-enter Workspace Context) requires a currently-unavailable Access Evaluation Outcome. This risk is not new — it is the same risk WP-08's own chartering decision weighed and used to prefer C-001. Charting WP-09 now does not resolve this risk; it proceeds with it disclosed.
- **Scope-narrowing risk:** if the IRA's Gap Analysis excludes most of ERB-C008-02/-04/-05 (as the evidence strongly suggests it must, absent a change in C-002's own production readiness), the resulting Work Package may deliver substantially less of what "Workspace Management" colloquially implies than its name suggests — a perception risk for stakeholders expecting a full workspace-switching capability.
- **No new architectural risk identified** — C-008 introduces no new canonical entity, no new database table, no new API surface beyond what its own governed EXs require, per §1.5's Out of Scope.

## 9. Technical Assumptions

- C-002's Access Evaluation resolver remains minimum-scope for the duration of this Work Package's own implementation window (per `WP-RTA-001` Closure Report §7, unchanged since 2026-08-01).
- No existing frontend Workspace-adjacent code (`config/workspaces.ts`, `WorkspaceSwitcher.tsx`) implements any PE-001-C008 ERB/EX — both are WP-08-era navigation scaffolding, confirmed via direct code review (`IRA-009 §3`), and are available to extend, not replace.
- No backend Workspace Management code exists anywhere in this repository today (confirmed via repository-wide search, `IRA-009 §3`) — this Work Package's own backend implementation, whatever its final IRA-determined scope, begins from zero existing service code, not a partial one.

## 10. Architecture Impact

None. This Work Package introduces no new capability, no new canonical Business Object (subject to `IRA-009 §6`'s own eligibility analysis for any new persisted construct), no new architectural pattern, and no redesign of any existing subsystem. Every element of its own governed scope (per PE-001-C008 §1.5) explicitly excludes ownership of Presentation Architecture, the Canonical Data Model, Runtime orchestration, and Business Activity implementation methodology — those remain SD-001/CMD-001/RTA-001/IMP-001's own exclusive scope, consumed not redefined.

## 11. Testing Strategy

Per `IMP-001 §11`, applied to whatever scope `IRA-009 §5` authorizes: Business Activity Contract tests (unit, service-layer) for each in-scope Business Activity; Authorization Boundary tests (401/403 as applicable); API tests for every endpoint and status branch the IRA's own Plan A specifies. Full AuthService regression suite re-run before closure, per every prior Work Package's own precedent.

## 12. Exit Criteria

Per `CLAUDE.md §19.7`/`§19.7b`/`§20.7`: Business Activities realized (per the IRA's own final scope) marked Implementation Complete; Independent Certification passed; Verification & Validation Audit passed (or any finding remediated and independently re-verified); Release Readiness Audit passed; end-to-end demonstrability confirmed for whatever scope was authorized; repository committed. Only after all of the above may WP-09 be marked CLOSED.

## 13. Repository Authority

Implementation authority does not exist under this charter alone. Per this repository's own established process, full-lifecycle execution requires the accompanying IRA to be accepted, followed by a separate, explicit Repository Owner authorization.

## 14. Governing Documents

- `PE-001-C008_Workspace_Management.docx` v1.3 (Primary Specification)
- `PE-001_Enterprise_Experience_Blueprint.md` Chapters 11, 13, 14, 15 (Workspace Model, referenced not redefined)
- `CAP-001_Enterprise_Capability_Registry.md` (C-008 registration)
- `CLAUDE.md §16–§20` (canonical authority resolution, architectural change control, implementation checklist, Enterprise Experience Standard)
- `WP-RTA-001_Closure_Report.md §7` (Access Evaluation resolver production-readiness finding — the governing constraint on this Work Package's own achievable scope)
- `IRA-008_WP-08_Identity_Management_Implementation_Readiness_Assessment.md` (precedent methodology for scoping around the same class of blocker)
- `WP-REG-001_Enterprise_Work_Package_Register.md` §9 (WP-08's own chartering-decision record, the origin of this blocker's disclosure)

---

*This charter records that WP-09 exists and is authorized to proceed to the Implementation Readiness Assessment stage. It does not itself authorize implementation.*
