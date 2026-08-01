# IRA-009 — WP-09 Workspace Management (C-008) — Implementation Readiness Assessment

**Document ID:** IRA-009
**Work Package:** WP-09
**Capability:** C-008 — Workspace Management
**Governing Specification:** `PE-001-C008_Workspace_Management.docx`, Version 1.3
**Status:** ACCEPTED — READY (at the scope determined in §4). **IRA Acceptance granted 2026-08-01** per Repository Owner Instruction "Governance Consolidation & Transition to WP-09," following consistent review conclusions in `WP-09-BUSINESS-VALUE-ASSESSMENT.md` and `PLATFORM-DEPENDENCY-ASSESSMENT-TIERRESOLVER.md` (both found no Release B/Milestone 1 blocker at this IRA's own §4.8 scope). **Implementation subsequently authorized 2026-08-01 and completed: WP-09 is CLOSED — CERTIFIED (2026-08-02), committed `90544cb`/`6ce9bd3`/`d648150`, per `IMP-REPORT-WP-09_Workspace_Management.md` and the full five-gate closure sequence (`CLAUDE.md §19.7b`).**
**Prepared By:** Engineering Governance session (Claude Code), under Repository Owner instruction
**Date:** 2026-08-01 (drafted); 2026-08-01 (accepted)

---

## 1. Purpose

Determines whether, and at what scope, WP-09 (chartered `WP-09_Workspace_Management.md`) may proceed to implementation, per `CLAUDE.md §19`/`§20`. Per the charter's own §6 (Enterprise Experience Requirement), this IRA produces **two** implementation plans — **Plan A** (Business Capability Implementation, §5) and **Plan B** (Enterprise Experience Implementation, §7) — neither of which designs screens or writes code; both are planning determinations only.

**This IRA's central finding, stated up front rather than buried:** three of C-008's six ERBs are excluded from this Work Package's authorized scope, for the same structural reason WP-08's own chartering decision already used to prefer C-001 over C-008 — an unconditional dependency on a currently-unavailable Access Evaluation Outcome. This is a larger exclusion, proportionally, than any prior Work Package's own disclosed narrowing (WP-08 excluded 1 of 4 ERBs; this excludes 3 of 6). The excluded ERBs are the ones a reader would most associate with "Workspace Management" in the colloquial sense — entering, switching, and re-entering a workspace. See §4 for the full, EX-by-EX reasoning.

---

## 2. Governing Documents Reviewed

- `PE-001-C008_Workspace_Management.docx` v1.3 — full text extracted directly from `word/document.xml` (Chapters 1–9, Appendices A–C; not summarized).
- `WP-09_Workspace_Management.md` (charter).
- `CLAUDE.md` §16–§20 (canonical authority resolution, architectural change control, implementation checklist, Enterprise Experience Standard).
- `CAP-001_Enterprise_Capability_Registry.md` (C-008 registration, verbatim).
- `WP-REG-001_Enterprise_Work_Package_Register.md` §4/§6/§8/§9 (Executive Dashboard; confirms no WP currently In Progress; confirms WP-08's own chartering-decision record naming C-008's identical blocker).
- `WPR-001_Work_Package_Roadmap.md` (confirms no prior C-008 charter exists).
- `WP-RTA-001_Closure_Report.md §7` (Access Evaluation resolver production-readiness finding — unchanged since WP-08's own closure).
- `IRA-005_WP-05_Access_Management_Implementation_Readiness_Assessment.md §12` (precedent: the original disclosure of the Access Evaluation resolver's minimum-scope limitation).
- `IRA-008_WP-08_Identity_Management_Implementation_Readiness_Assessment.md` (precedent methodology: an analogous capability's own scoping around the identical blocker, and the "satisfied by construction" / classification-only Business Activity patterns reused below).
- Existing repository source: `source/frontend/src/config/workspaces.ts`, `source/frontend/src/components/layout/WorkspaceSwitcher.tsx`, `Backend/Services/AuthService/schemas/membership.py` (`DependentCapability.WORKSPACE_MANAGEMENT`), and a repository-wide search for any other Workspace-related backend code.

---

## 3. Existing Asset Discovery (Reuse Before Creating, `CLAUDE.md §19.2`)

Direct repository search, not assumption, found the following pre-existing assets bearing on C-008:

| Asset | Location | Status |
|---|---|---|
| `WORKSPACES` config | `source/frontend/src/config/workspaces.ts` | Exists (WP-08 era). `Workspace { id, label, description, homeHref, navItems }`, 3 static entries (`platform`, `enterprise-administration`, `identity-security`). Its own header comment explicitly states this is a regrouping of existing navigation, not a C-008 realization — "the remaining categories... are not realized by any chartered capability yet and are not invented here." No Membership/Access re-confirmation, no availability resolution, no disruption handling — a navigation construct, not a governed Workspace Context. |
| `WorkspaceSwitcher.tsx` | `source/frontend/src/components/layout/` | Exists. Thin `Menu`-based dropdown; `router.push(workspace.homeHref)` against the 3 static entries above. No Access Evaluation call, no governed entry/switch semantics. |
| `DependentCapability.WORKSPACE_MANAGEMENT` | `Backend/Services/AuthService/schemas/membership.py:222-224` | Exists (WP-03 BA-10, C-007's own hand-off-rejection enum). Its own docstring states: *"C-002 (Access Management) and C-008 (Workspace Management) are both registered Active in CAP-001 but have no Work Package... C-007 never calls into any dependent capability's own API for this Business Activity."* A **real, existing caller-in-waiting** for a future C-008 classification endpoint — unlike WP-08's own `EX-C001-08`, which had no caller anywhere (`TD-101`). |
| Backend Workspace implementation | — | **NOT FOUND anywhere.** No model, router, service, or database table named `workspace` exists in any service, migration, or `.sql` file repository-wide. Confirmed by direct repository-wide search, not assumption — consistent with PE-001-C008 §9.6's own decision record that Workspace has no data-model footprint. |

**Conclusion:** per `CLAUDE.md §2`/`§19.5` (Reuse → Configure → Extend → Compose → Create), WP-09's own Plan B extends the existing `config/workspaces.ts`/`WorkspaceSwitcher.tsx`/navigation pattern; Plan A begins backend implementation from zero existing Workspace-specific code, following the same established feature pattern (`services/*.py`, `repositories/*.py`, `routers/*.py`) every prior Work Package has used.

---

## 4. Gap Analysis — Scope Determination Per Enterprise Experience

Each of the 11 EXs is evaluated against real repository evidence, per `PE-001-C008`'s own governing text, its Business Rules, and its ten Experience Contracts.

### 4.1 `EX-C008-01`/`02` (`ERB-C008-01`, Resolve Available Workspace Context) — **IN SCOPE**

`EX-C008-01`'s own Trigger: "A Person authenticates or returns to the platform without a currently established Participating Workspace Context." Its Context Required draws on Membership (`C-007`) and structural placement/Home Node (`C-005`) — both already established, both Closed capabilities. Critically, **Contract 5.3's own unconditional Access Evaluation requirement is scoped explicitly to "every Workspace entry, switch, or re-entry"** — discovery and presentation of *candidates* is a distinct, earlier step this contract does not name. `BR-C008-02` reinforces this: Membership Authority Consequence Context is "a required... input to Workspace availability resolution but SHALL NOT independently determine Workspace availability or participation eligibility" — availability resolution is a Membership/structural-data query, not an authorization decision.

**Disposition:** in scope, buildable now, without a production Access Evaluation resolver. Realized as **BA-01 — Resolve and Present Available Workspace Candidates**, per §5 below.

### 4.2 `EX-C008-03`/`04` (`ERB-C008-02`, Enter Workspace Context) — **EXCLUDED**

`EX-C008-03`'s own Context Required: "a current Access Evaluation Outcome for the candidate's Home Node scope." Contract 5.3, verbatim: "C-008 SHALL request, and SHALL NOT compute, an Access Evaluation Outcome" for entry. `C-002` (Access Management, `WP-05`) was authorized only at minimum scope (`IRA-005 §12`): a genuine, affirmative Permitted/Denied determination requires a real, production `TierResolver`, which `WP-RTA-001`'s own Closure Report §7 states does not exist for any tier. An affirmative Access Evaluation Outcome is therefore structurally unobtainable from this repository's own running code today — the identical root cause `IRA-005 §12` and `IRA-008 §4.1` already disclosed, now recurring a third time.

`EX-C008-04` (the rejection/unresolved-outcome branch of the same entry attempt) is entangled with `EX-C008-03`: a genuine rejection outcome requires a genuine attempt to have occurred first. Building `EX-C008-04` alone, without `EX-C008-03`, would mean either fabricating a rejection with no real evaluation behind it, or building a pass-through that always reports "unresolved" — neither is a real Enterprise Experience realization.

**Disposition, mirroring `IRA-005 §12`/`IRA-008 §4.1`'s own precedent exactly:** `EX-C008-03`/`04` (and therefore `ERB-C008-02` in full) are **excluded from this Work Package's authorized scope**. This is the same class of scope exclusion those two prior IRAs already disclosed, not a new or worse kind of gap — but it is the *central* transition of this specific capability, which those two prior exclusions were not for their own capabilities.

### 4.3 `EX-C008-05` (`ERB-C008-03`, Continue Enterprise Journey Within Workspace Context) — **EXCLUDED**

Unlike `IRA-008`'s own `EX-C001-05` (satisfied by construction via the pre-existing, unconditional `POST /auth/refresh`), no mechanism anywhere in this repository currently establishes "an established Participating Workspace Context" for this EX to preserve continuity *of*. Its own Trigger presupposes `ERB-C008-02` has already occurred. With `ERB-C008-02` excluded (§4.2), this EX has no reachable trigger condition in the resulting system — not satisfied by construction (nothing already does this), and not independently buildable (there is nothing yet to continue).

**Disposition:** excluded, same root cause as §4.2, transitively.

### 4.4 `EX-C008-06`/`07` (`ERB-C008-04`, Switch Workspace Context) — **EXCLUDED**

`BR-C008-03`, verbatim: "Every Workspace entry, switch, **and re-entry** SHALL request a current Access Evaluation Outcome from C-002; none SHALL be computed by C-008." Switch is explicitly, unconditionally named alongside Entry. Same root cause as §4.2.

**Disposition:** excluded.

### 4.5 `EX-C008-08`/`09` (`ERB-C008-05`, Re-enter Previously Participating Workspace Context) — **EXCLUDED**

`BR-C008-05`: a historical Participating Workspace Context record "SHALL NOT be restored without re-confirming current Membership and Access standing" — Access standing again names the same blocked dependency. Additionally, re-entry presupposes a prior entry to re-enter, which `§4.2`'s own exclusion means never occurs in this Work Package's own scope — doubly blocked.

**Disposition:** excluded, same root cause as §4.2 and §4.4.

### 4.6 `EX-C008-10` (`ERB-C008-06`, Detect and Resolve Disrupted Workspace Context) — **IN SCOPE**

Directly analogous in shape to `IRA-008`'s own `EX-C001-06` (in scope, realized as `BA-01`): a read-only re-confirmation that a currently-held context remains valid, consulting only already-available Membership/Organization facts, with the runtime Access-Evaluation signal named only "where relevant" (conditional, not mandatory) in the governing text — not the unconditional requirement §4.2/§4.4/§4.5 name. Unlike `EX-C001-06` (which operates against the JWT-based Identity Context every authenticated user already holds regardless of `C-008`'s own gate), `C-008` has no equivalent persisted "currently held Workspace Context" today — but the existing, already-real `config/workspaces.ts`/`workspaceForPathname()` mechanism (§3) provides a lightweight, route-derived notion of "which workspace the Person is currently navigated to." Re-confirming that the Person's underlying Membership and structural placement remain valid for that route is a genuine, buildable re-confirmation, independent of `ERB-C008-02`'s own excluded governed-entry mechanics.

**Disposition:** in scope, buildable now. Realized as **BA-02 — Detect and Resolve Disrupted Workspace Context**, per §5 below, mirroring `IRA-008`'s own `BA-01` pattern (read-only, no persistence).

### 4.7 `EX-C008-11` (`ERB-C008-06`, Resolve Dependent Capability Hand-off Rejection) — **IN SCOPE**

Purely a classification Business Activity, per `BR-C008-06`: classify as Dependent Capability Context Insufficiency or Potential Workspace Context Integrity Disruption, routing accordingly. Directly mirrors `IRA-008`'s own `BA-03` (`EX-C001-08`), already proven buildable for the structurally analogous C-001 case. **Unlike `EX-C001-08` (no caller anywhere, `TD-101`), this EX already has a real, existing caller-in-waiting**: `Backend/Services/AuthService/schemas/membership.py`'s own `DependentCapability.WORKSPACE_MANAGEMENT` enum value, registered by `C-007`'s own WP-03 BA-10, whose docstring explicitly discloses it names C-008 "but has no Work Package" to call into yet.

**Disposition:** in scope, no blocker, and — unusually — closes a gap another already-Closed Work Package explicitly disclosed. Realized as **BA-03 — Classify Workspace Hand-off Rejection**, per §5 below.

### 4.8 Summary

| EX | ERB | Disposition | Realization |
|---|---|---|---|
| `EX-C008-01`/`02` | `ERB-C008-01` | In scope | BA-01 |
| `EX-C008-03`/`04` | `ERB-C008-02` | Excluded (Access Evaluation blocker, identical to `IRA-005 §12`) | None this WP |
| `EX-C008-05` | `ERB-C008-03` | Excluded (no reachable trigger, transitive) | None this WP |
| `EX-C008-06`/`07` | `ERB-C008-04` | Excluded (Access Evaluation blocker, `BR-C008-03` explicit) | None this WP |
| `EX-C008-08`/`09` | `ERB-C008-05` | Excluded (Access Evaluation blocker + depends on excluded entry) | None this WP |
| `EX-C008-10` | `ERB-C008-06` | In scope | BA-02 |
| `EX-C008-11` | `ERB-C008-06` | In scope | BA-03 |

**Three of six ERBs excluded (50%), covering five of eleven EXs.** This Work Package, at this scope, does not deliver governed workspace entry, switching, or re-entry — the existing, ungoverned `WorkspaceSwitcher.tsx` navigation remains the only way a user moves between workspaces after this Work Package closes, exactly as before it. What this Work Package *does* deliver: a real availability/candidate-resolution service, a disruption self-check, and closure of a gap `C-007` already disclosed waiting on.

---

## 5. PLAN A — Business Capability Implementation

### BA-01 — Resolve and Present Available Workspace Candidates (`EX-C008-01`/`02`)

- **Domain Model:** None new (subject to `CMD-001 §26.3a` eligibility confirmation, §6 below — likely no new persisted construct, since this is a query/projection over existing Membership/Structure data).
- **Database:** No migration anticipated.
- **Repository:** New thin repository method(s) querying existing `Membership`/`OrganizationNode` tables (both `C-007`/`C-005`, already governed elsewhere) — reuse, not duplicate, their own existing repositories.
- **Service:** New `services/workspace_resolution_service.py` — resolves the caller's own candidate Workspace set from their current Memberships and Home Nodes; per `BR-C008-01a`, does **not** determine which `PE-001 §13.5` Workspace Type(s) an anchor may host (Pending Canonical Binding, disclosed in the charter's own Out of Scope) — returns candidates keyed to structural anchors only.
- **API:** `GET /workspaces/candidates` — no request body; response: a list of candidate Workspace Context summaries. Gated by authentication only.
- **Events:** None (read-only resolution).
- **Testing:** Unit (service: correct candidate set for a Person with N active Memberships; empty set for none) + API (200 with candidates, 200 empty, 401 unauthenticated).

### BA-02 — Detect and Resolve Disrupted Workspace Context (`EX-C008-10`)

- **Domain Model:** None new.
- **Database:** No migration.
- **Repository:** Reuses `MembershipRepository`/structural-placement repositories.
- **Service:** New `services/workspace_status_service.py` — `refresh(workspace_route_context)`: re-confirms the Membership and structural placement underlying the Person's currently-navigated-to workspace remain valid; mirrors `IRA-008`'s own `IdentityStatusService.refresh()` shape exactly (read-only, no persistence, no audit record).
- **API:** `POST /workspaces/refresh-status` — request: `{}` (acts on caller's own current session/route context); response: refreshed status (`CURRENT`/`UNRESOLVED`) with an explicit unresolved outcome, never a silent 200 with stale data.
- **Events:** None.
- **Testing:** Unit (current Membership → `CURRENT`; deactivated/removed Membership → `UNRESOLVED`) + API (200 both branches, 401 unauthenticated).

### BA-03 — Classify Workspace Hand-off Rejection (`EX-C008-11`)

- **Domain Model:** None (classification-only, no persistence).
- **Database:** No migration.
- **Service:** New `services/workspace_handoff_classification_service.py` — `classify(context, rejecting_capability, stated_reason)`. Mirrors `IRA-008`'s own `BA-03` pattern (itself mirroring `WP-02 BA-10`'s `AuthorizationPolicyConflictService.classify_handoff_rejection()`), per `BR-C008-06`: classification computed from the Workspace Context's own independently-verifiable current state (via BA-02's own `refresh()` logic), never from `stated_reason`, which is recorded for audit traceability only.
- **API:** `POST /workspaces/classify-handoff-rejection` — request: `{context, rejecting_capability, stated_reason}`; response: `{classification, context_preserved: bool, routed_to, explanation}`. Gated by authentication only. **This closes the gap `Backend/Services/AuthService/schemas/membership.py`'s own `DependentCapability.WORKSPACE_MANAGEMENT` enum value has been disclosing since WP-03 BA-10** — `C-007`'s own hand-off logic may now call a real endpoint, though wiring that caller is `C-007`'s own future work, not this Work Package's.
- **Events:** None.
- **Testing:** Unit (current → `CAPABILITY_SCOPED_INSUFFICIENCY`; unresolved → `INTEGRITY_SIGNAL`, routed to BA-02) + API (200 both branches, 401 unauthenticated).

### Cross-cutting

- **`middleware/tenant.py`:** a `/workspaces` prefix exemption decision is deferred to implementation time, following whichever precedent (`/person`'s unconditional exemption vs. `/domain-permissions`'s interim gate) the actual query shape at implementation time warrants — not pre-decided here.
- **Authorization:** none of BA-01/02/03 is gated by `require_platform_admin` — each is a self-referential action against the caller's own Membership/context, consistent with `Contract 5.3`'s own scoping (only *governed* actions — entry, switch, re-entry, all excluded — require Access Evaluation).
- **Migration:** none anticipated for this scope.

---

## 6. Business Object Eligibility Analysis (`CMD-001 §26.3a`)

No new persisted construct is proposed at this scope (BA-01/02/03 are all read-only query/classification services against existing Membership/Structure data). **Result: not applicable — no new Business Object to evaluate.** If implementation discovers a genuine need for a new persisted construct (e.g., a Workspace-candidate cache), the eligibility test shall be applied at that time, not assumed here.

---

## 7. PLAN B — Enterprise Experience Implementation

Derived only from `PE-001`, `PE-001-C008`, `SD-001`, `DS-001`, `IMP-001 §10` — per the charter's own §6, this plan identifies what is built; it does not itself design a screen.

- **Enterprise Experiences realized:** `EX-C008-01`/`02` (candidate presentation), `EX-C008-10` (disruption self-check, likely surfaced only diagnostically, not as a primary user-facing action), `EX-C008-11` (system-facing — no dedicated screen, mirrors `IRA-008`'s own treatment of `EX-C001-08`).
- **User Personas:** any authenticated Person with at least one active Membership.
- **User Journey:** an authenticated user's existing `WorkspaceSwitcher.tsx` dropdown, currently backed by the static `WORKSPACES` config, is extended to source its candidate list from BA-01's own `GET /workspaces/candidates` endpoint instead — the same UI surface, a real backend behind it, not a new screen.
- **Workspace placement:** the existing `WorkspaceSwitcher.tsx`, mounted in `GlobalHeader.tsx` — no new navigation entry.
- **Screens/Views:** no new screen. `WorkspaceSwitcher.tsx` extended to call the real candidate-resolution API; `config/workspaces.ts`'s static array becomes a fallback/seed only, not the sole source of truth, once BA-01 lands.
- **States implemented (`CLAUDE.md §20.6`):** loading (candidate fetch in flight), empty (no candidates — a Person with zero Memberships), error (network/API failure via existing `useNotifications()` pattern), validation (not applicable — no form), confirmation (not applicable — a switcher, not a submission).
- **Not applicable, disclosed rather than silently omitted:** Progressive Disclosure's four-state widget contract (`IMP-001 §10.3`/`IMP-FE-004`) — `WorkspaceSwitcher` is a navigation menu, not a data-bearing widget in that contract's own sense; Guided Completion, Confidence/Evidence panels, DNA-adaptive rendering, Sacred 12 tiering — none apply, consistent with every prior Work Package's own precedent for administrative navigation surfaces.
- **Accessibility, Responsive behaviour, State management:** inherited from the existing `Menu`/`WorkspaceSwitcher` component and its already-established `useOverlay` focus-trap/keyboard-navigation pattern (confirmed this session's own recent Enterprise Shell refinement work) — no new pattern invented.

---

## 8. Readiness Decision

**READY**, at the scope determined in §4.8: BA-01, BA-02, BA-03, backend and frontend, per Plan A (§5) and Plan B (§7). `ERB-C008-02`, `-03`, `-04`, `-05` (in full) excluded — the majority of this capability's colloquially-expected scope. This is a materially narrower Work Package than "Workspace Management" suggests, and the Repository Owner should weigh this explicitly before authorizing implementation — see the accompanying charter's own §8 (Risks) and this report's own §1.

No constitutional blocker for the scope that IS in bounds. No new canonical Business Object (§6). No new architectural component beyond the service/router files listed in §5 and their frontend counterparts in §7 — all following established, precedented patterns (directly mirroring `IRA-008`'s own BA-01/BA-03 shapes), none inventing a new one.

---

## 9. Anticipated Technical Debt

- **TD-candidate-A** (Medium — same severity class as `TD-102`, `IRA-008`'s own analogous exclusion): `ERB-C008-02`/`-04`/`-05` excluded in full, pending the same Access Evaluation resolver `§4.2` discloses as unavailable. This is the largest single exclusion any Work Package in this repository has disclosed to date, proportionally.
- **TD-candidate-B** (Low): BA-03's classification endpoint has a real caller-in-waiting (`C-007`'s own `DependentCapability.WORKSPACE_MANAGEMENT`) but wiring that caller is `C-007`'s own future work, not performed here.
- **TD-candidate-C** (Low): `config/workspaces.ts`'s static `WORKSPACES` array is not removed when BA-01 lands — recommend a future pass migrate it to a pure fallback/seed role once the real API is proven, rather than maintaining two sources of workspace-candidate truth indefinitely.

(Final Technical Debt IDs assigned at implementation time, per `CLAUDE.md §19.8.2`.)

---

## 10. Testing Strategy

Per `IMP-001 §11`: Business Activity Contract tests for BA-01/02/03 (unit, service-layer); Authorization Boundary tests (401 unauthenticated for all three) — no 403 branch anticipated, since none is gated beyond authentication; API tests for every endpoint and status branch listed in §5. Full AuthService regression suite re-run before closure, per every prior Work Package's own precedent.

---

## 11. Entry Criteria

This IRA itself is the entry-criteria gate. Satisfied: charter exists (`WP-09_Workspace_Management.md`), governing specification reviewed in full, existing assets discovered, Gap Analysis complete, no constitutional blocker for the in-scope portion.

## 12. Exit Criteria

Per `CLAUDE.md §19.7`/`§19.7b`/`§20.7`, applied to the scope in §4.8/§8: BA-01/02/03 Implementation Complete; Independent Certification; V&V Audit (remediated and re-verified if any finding); Release Readiness Audit; end-to-end demonstrability for the in-scope EXs only (not the excluded ones); committed.

---

## 13. Repository-Owner Authorization

**IRA Acceptance: GRANTED, 2026-08-01**, per Repository Owner Instruction "Governance Consolidation & Transition to WP-09" — this IRA's own §4.8 scope determination has now been reviewed via two Repository-Owner-commissioned assessments (`WP-09-BUSINESS-VALUE-ASSESSMENT.md`, `PLATFORM-DEPENDENCY-ASSESSMENT-TIERRESOLVER.md`), both reaching a consistent conclusion: no Release B/Milestone 1 exit criterion is blocked at this scope, and the excluded ERBs' root cause is understood and not an implementation-time surprise.

**Full-lifecycle implementation authority: GRANTED, 2026-08-01**, per Repository Owner Instruction "Release B – WP-09 Implementation Authorization" — the separate, distinct decision this section originally identified as outstanding. All three Business Activities `§4.8` authorized (BA-01, BA-02, BA-03) were subsequently implemented, committed (`90544cb`/`6ce9bd3`/`d648150`), and closed through the full five-gate sequence (`CLAUDE.md §19.7b`) — WP-09 is **CLOSED — CERTIFIED**, per `IMP-REPORT-WP-09_Workspace_Management.md`.

---

*End of IRA-009. Accepted, 2026-08-01, at the scope determined in §4.8. Implementation authorized 2026-08-01 and completed — WP-09 CLOSED — CERTIFIED, 2026-08-02.*
