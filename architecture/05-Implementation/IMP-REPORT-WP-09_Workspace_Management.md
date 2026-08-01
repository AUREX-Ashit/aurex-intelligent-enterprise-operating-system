# IMP-REPORT-WP-09 — Workspace Management (C-008)

**Work Package:** WP-09 — Workspace Management (C-008)
**Governing Readiness Assessment:** `IRA-009_WP-09_Workspace_Management_Implementation_Readiness_Assessment.md` (Accepted — READY, scoped: 3 Business Activities realizing `EX-C008-01`/`02`/`10`/`11`; `ERB-C008-02`/`03`/`04`/`05` — `EX-C008-03`–`09` — excluded, consolidated as `TD-111`).
**Governing Business Object:** None. All three authorized Business Activities are read-only queries/classifications against existing `Membership`/`Organization`/`Role` data (`IRA-009 §6` — not applicable, no new persisted construct proposed).
**Governing Capability Specification:** `PE-001-C008_Workspace_Management.docx` v1.3 (`ERB-C008-01` through `06`; `EX-C008-01` through `11`).
**Repository Owner Authorization:** Granted per Repository Owner Instruction "Release B – WP-09 Implementation Authorization," 2026-08-01.
**Scope of this report:** BA-01 and BA-02 (`EX-C008-01`/`02`/`10`). BA-03 is implemented one Business Activity at a time per the governing instruction's own methodology — it requires separate Repository Owner approval before proceeding. BA-01's own section below is unmodified from its own approved, committed state (`90544cb`) — not revisited by this pass.

---

## BA-01 — Resolve and Present Available Workspace Candidates (`EX-C008-01`/`02`)

### Business Activity Contract (`IMP-001 §6.7`)

- **Business Intent:** Resolve and present the Workspaces a Person may enter, from real Membership/structural data — replacing the static, identical-for-every-user candidate list every prior release has shown.
- **Disposition:** New. Read-only candidate discovery, distinct from governed Workspace entry (`ERB-C008-02`, excluded from this Work Package's scope per `IRA-009 §4.2`). Reuses `MembershipRepository.get_person_memberships()` — the same repository method `MembershipService.present_own_portfolio()` (WP-03 BA-08, an analogous cross-organization view) already uses — rather than duplicating it, per `CLAUDE.md §19.5`'s Reuse-first order.
- **Input Contract:** none (acts on the caller's own current Memberships, from JWT claims — `person_id`).
- **Output Contract:** `WorkspaceCandidatesResponse` (`candidates: WorkspaceCandidate[]`, each: `membership_id`, `organization_id`, `organization_name`, `role_code`, `role_name`, `home_node_id` nullable, `is_primary`).
- **Business Rules:** Only `ACTIVE`-status Memberships are candidates (inherited from `get_person_memberships()`'s own existing filter). Per `BR-C008-01a`, this Business Activity does not determine which `PE-001 §13.5` Workspace Type(s) a candidate's structural anchor may host (Pending Canonical Binding, disclosed in the WP-09 charter's own Out of Scope) — candidates are returned keyed to their structural anchor (`organization_id`, `home_node_id`) only.
- **Authorization Rules:** Authenticated only (`get_current_claims`) — a self-referential query, not an administrative action, consistent with `Contract 5.3`'s own scoping (only *governed* actions — entry, switch, re-entry, all excluded — require Access Evaluation).
- **Audit Requirements:** None — read-only, mirrors `MembershipService.present_own_portfolio()`'s own precedent.
- **Tests:** `test_resolve_candidates_returns_empty_list_when_no_memberships`, `test_resolve_candidates_returns_one_candidate_per_active_membership`, `test_resolve_candidates_spans_multiple_organizations`, `test_resolve_candidates_excludes_non_active_memberships`, `test_resolve_candidates_only_returns_the_supplied_persons_own_memberships`, `test_resolve_candidates_exposes_home_node_id_as_structural_anchor_only` (service — 6 tests); `test_get_candidates_returns_empty_list_when_no_memberships`, `test_get_candidates_returns_candidates_for_active_memberships`, `test_get_candidates_requires_authentication`, `test_get_candidates_does_not_require_tenant_header`, `test_get_candidates_only_returns_the_callers_own_memberships` (API — 5 tests).

---

## Frontend / Enterprise Experience (`CLAUDE.md §20`, Plan B — `IRA-009 §7`)

- **Extended, not created:** `source/frontend/src/components/layout/WorkspaceSwitcher.tsx` — the existing `Menu`-based dropdown, mounted in `GlobalHeader.tsx`, is unchanged in its navigable item set (no new screen, no new navigation entry). What changes: `GET /workspaces/candidates` is now called on mount, and its real result governs the loading/empty/error states below. The static `WORKSPACES` config (`config/workspaces.ts`) remains the actual switchable/navigable list, per `IRA-009 §7`'s own explicit design ("`config/workspaces.ts`'s static array becomes a fallback/seed only, not the sole source of truth") — no `PE-001 §13.5` Workspace Type binding exists yet to route per-candidate (Pending Canonical Binding, Out of Scope), so replacing the navigable items themselves with per-candidate entries would either invent that binding or regress working navigation (jumping between Platform/Enterprise Administration/Identity & Security admin sections) into a non-functional list of same-destination organization names — neither is authorized. Reconciliation classified below.
- **New:** `src/types/workspace.ts`, `src/services/workspace-api.ts`.
- **Reused, not invented:** `Menu`, `Spinner` (existing DS-001-aligned component library); `useNotifications()`/`apiClient`/`ApiError` (existing infrastructure).
- **States implemented (`CLAUDE.md §20.6`):** loading (`Spinner` replaces the trigger's static chevron while the candidate fetch is in flight), empty (zero candidates is real, new information the static config never had — surfaced via a one-time `notify(..., "warning")`, since `Menu`'s own `MenuItem` type defines no disabled-item treatment DS-001 does not already provide, and inventing one is out of scope), error (one-time `notify(..., "danger")`, existing static list continues to function unaffected — a safe fallback, not a broken switcher), confirmation/validation (not applicable — a read-only switcher, not a form, mirrors `IRA-008`'s own disposition for `WorkspaceSwitcher`-class components).
- **Verification:** `tsc --noEmit` — 0 errors. `eslint` (new/modified files) — 0 problems.

### Historical UI Concept Review (Enterprise Experience section, this turn's own instruction)

Direct search of `design/historical-concepts/` for "workspace" (case-insensitive) returns matches in `01-login.html`, `02-registration.html`, `03-payment-setup.html`, and `04-invite-team.html` — all colloquial, single-tenant onboarding-flow language ("Activate your workspace," "Sign in to your workspace," a "Workspace Owner" role badge in the invite-team table). None of these model a multi-organization Workspace *switcher* or candidate-resolution concept — they use "workspace" as informal shorthand for "your account," consistent with a pre-C-008, single-tenant signup flow. No historical concept models `ERB-C008-01`'s own governed candidate-discovery behavior. **Classification: RETIRE (as a source for this Business Activity)** — none of the four concepts is a KEEP/EVOLVE candidate for BA-01's own switcher work; their "workspace" language is superficially similar but semantically unrelated (single-tenant account activation, not multi-organization Membership-derived candidate resolution). No historical concept is reused, extended, or otherwise drawn upon here.

---

## BA-02 — Detect and Resolve Disrupted Workspace Context (`EX-C008-10`)

### Business Activity Contract (`IMP-001 §6.7`)

- **Business Intent:** Re-confirm that the caller's own current session Workspace Context (the Membership and structural placement named by the session's own `membership_id`/`organization_id` claims) remains valid — never inferring validity is preserved absent a freshly re-resolved, affirmative confirmation.
- **Disposition:** New. Read-only re-confirmation, no persistence — mirrors `IdentityStatusService.refresh()`'s own established precedent (WP-08 BA-01) exactly, per `IRA-009 §4.6`/`§5`.
- **Input Contract:** none (acts on the caller's own current session, from JWT claims — `membership_id`, `organization_id`).
- **Output Contract:** `WorkspaceStatusResponse` (`membership_id`, `organization_id`, `status`: `CURRENT`/`UNRESOLVED`, `checked_at`).
- **Business Rules:** `CURRENT` only if the named Membership exists, is `ACTIVE`, and (when a `home_node_id` anchor is present) its `OrganizationNode` exists and is `active_flag = true`; `UNRESOLVED` otherwise — including a removed/unknown `membership_id`, deliberately resolved as `UNRESOLVED` (200), never a 404, per `IRA-009 §5`'s own testing note ("deactivated/removed Membership → UNRESOLVED"), since detecting exactly that disruption is this Business Activity's own purpose. The `home_node_id`-absent branch is dormant in practice today (`TD-032`: no Business Activity anywhere establishes an `OrganizationNode` row), same disclosed class as `TD-104`'s own dormant check.
- **Authorization Rules:** Authenticated only (`get_current_claims`) — a self-referential check, not an administrative action.
- **Audit Requirements:** None — read-only, mirrors `IdentityStatusService.refresh()`'s own precedent.
- **Tests:** `test_refresh_status_current_for_active_membership`, `test_refresh_status_unresolved_for_suspended_membership`, `test_refresh_status_unresolved_for_removed_membership_not_404`, `test_refresh_status_current_when_home_node_absent`, `test_refresh_status_current_when_home_node_active`, `test_refresh_status_unresolved_when_home_node_inactive` (service — 6 tests); `test_refresh_status_returns_current`, `test_refresh_status_returns_unresolved_for_unknown_membership`, `test_refresh_status_requires_authentication`, `test_refresh_status_does_not_require_tenant_header` (API — 4 tests).

### Mandatory Guardrails — Verified

This Business Activity does **not**: implement governed Workspace entry, switching, or re-entry (no code path calls `C-002`/Access Evaluation; `home_node_id`/`membership_status` checks only, both already-available facts per `IRA-009 §4.6`); circumvent `TD-111` (the Access Evaluation resolver remains unconsulted, exactly as `TD-111` discloses as unavailable — this Business Activity's own scope was never gated by it); introduce a temporary workaround, mocked business logic, or fabricated business data (every check is a real query against `Membership`/`OrganizationNode`, identical in kind to `IdentityStatusService`'s own already-certified precedent).

---

## Frontend / Enterprise Experience — BA-02 (`CLAUDE.md §20`, Plan B — `IRA-009 §7`)

- **New:** `src/features/workspace/state/useWorkspaceStatus.ts` (first file under `src/features/workspace/`), `WorkspaceStatusResponse`/`WorkspaceContextStatus` types added to `src/types/workspace.ts`, `refreshWorkspaceStatus()` added to `src/services/workspace-api.ts`.
- **Not modified:** `src/components/layout/WorkspaceSwitcher.tsx` — BA-01's own already-completed, already-approved implementation (`90544cb`), per this pass's own explicit "Do NOT modify BA-01" guardrail.
- **No new screen, no forced UI placement invented:** `IRA-009 §7` characterizes `EX-C008-10` as "likely surfaced only diagnostically, not as a primary user-facing action," not as requiring a specific mandatory placement. The one existing Workspace UI surface (`WorkspaceSwitcher.tsx`) is BA-01's own completed work, off-limits this pass. No other Workspace-related screen exists anywhere in this repository to attach a diagnostic display to, and inventing one would exceed both this Business Activity's own disclosed scope ("no new screen," `IRA-009 §7`) and `CLAUDE.md §19`'s prohibition on inventing UI SD-001/DS-001 does not already define a location for. The hook is therefore delivered as a standalone, composable unit — the real backend integration is complete and tested — ready for a future Work Package or Business Activity to mount wherever a genuine diagnostic placement is authorized, rather than forcing an undisclosed one now.
- **Reused, not invented:** `useNotifications()`/`ApiError`/`apiClient` (existing infrastructure); the hook's own shape directly mirrors `useIdentityManagement.ts`'s own "checking-status" slice.
- **States implemented (`CLAUDE.md §20.6`):** loading (`"checking"` state, for a future consumer to render), confirmation/error (an `UNRESOLVED` result and a network failure each produce a one-time `notify(...)` — `"warning"` and `"danger"` respectively, mirroring BA-01's own one-time-notification pattern), empty/validation (not applicable — no list, no form).
- **Verification:** `tsc --noEmit` — 0 errors. `eslint` (new/modified files) — 0 problems.

### Historical UI Concept Review

Direct search of `design/historical-concepts/` for session/disruption-adjacent terms ("session," "expired," "reconnect," "disrupt," "stale," "re-confirm," case-insensitive) returns matches in 7 files, all confirmed false positives on inspection: font-loading `preconnect` links, `sessionStorage` theme-persistence calls (unrelated to Workspace Context), and an ESG metric label ("Operational Disruption Risk"). No historical concept models a disrupted-session/context re-confirmation UI pattern. **Classification: RETIRE (as a source for this Business Activity)** — same disposition as BA-01's own review; no historical concept is reused, extended, or otherwise drawn upon here.

---

## Strategic Enhancements

| Strategic Enhancement | Implemented in WP-09 | Deferred | Justification |
|---|---|---|---|
| Real, Membership-derived Workspace candidate list (replacing the static, identical-for-every-user config) | Yes (BA-01) | — | Directly realizes `EX-C008-01`/`02`, the capability this Work Package charters. |
| Workspace Context disruption self-check (real Membership/structural-placement re-confirmation, replacing implicit trust in stale JWT claims) | Yes (BA-02) | — | Directly realizes `EX-C008-10`, per `IRA-009 §4.6`/§5. |
| Governed Workspace entry/switch/re-entry | — | Yes | `ERB-C008-02`/`04`/`05` require an unconditional Access Evaluation Outcome, structurally unobtainable (`TD-111`). Not this Work Package's authorized scope (`IRA-009 §4.2`/`§4.4`/`§4.5`). |
| Configuration Profiles, Branding, Theme, Terminology, Localization, Accessibility Profiles | — | Yes | C-041/WP-10's own scope, per `PRODUCT-MILESTONE-ROADMAP.md` §3 (Milestone 1). Explicitly out of this Work Package's own charter. |
| Saved Views, Progressive Disclosure four-state widget contract | — | Yes | Not named in `PE-001-C008`'s own governed scope for BA-01/BA-02; `WorkspaceSwitcher` is a navigation menu, not a data-bearing widget in `IMP-001 §10.3`'s own sense (`IRA-009 §7`, already disclosed as Not Applicable). |
| A dedicated Workspace status/diagnostic screen or panel | — | Yes | `IRA-009 §7` characterizes `EX-C008-10` as diagnostic-only, "not a primary user-facing action" — no screen is authorized by Plan B; inventing a placement now would exceed this Business Activity's own disclosed scope. |

No strategic enhancement backlog item belonging to WP-10 or a later Release was implemented.

---

## Documents Updated

- `Backend/Services/AuthService/schemas/workspace.py` (new)
- `Backend/Services/AuthService/services/workspace_resolution_service.py` (new)
- `Backend/Services/AuthService/routers/workspace.py` (new)
- `Backend/Services/AuthService/main.py` (modified — imports and mounts `workspace.router` at `/workspaces`)
- `Backend/Services/AuthService/middleware/tenant.py` (modified — `/workspaces` prefix exemption)
- `Backend/Services/AuthService/tests/test_workspace_resolution_service.py` (new, 6 tests)
- `Backend/Services/AuthService/tests/test_workspace_api.py` (new, 5 tests)
- `source/frontend/src/types/workspace.ts` (new)
- `source/frontend/src/services/workspace-api.ts` (new)
- `source/frontend/src/components/layout/WorkspaceSwitcher.tsx` (modified, BA-01 only — `90544cb`)
- `architecture/05-Implementation/IMP-REPORT-WP-09_Workspace_Management.md` (this report)

**BA-02, this pass:**

- `Backend/Services/AuthService/schemas/workspace.py` (modified — `WorkspaceContextStatus`, `WorkspaceStatusResponse` added)
- `Backend/Services/AuthService/services/workspace_status_service.py` (new)
- `Backend/Services/AuthService/routers/workspace.py` (modified — `POST /workspaces/refresh-status` added)
- `Backend/Services/AuthService/tests/test_workspace_status_service.py` (new, 6 tests)
- `Backend/Services/AuthService/tests/test_workspace_status_api.py` (new, 4 tests)
- `source/frontend/src/types/workspace.ts` (modified — `WorkspaceContextStatus`, `WorkspaceStatusResponse` added)
- `source/frontend/src/services/workspace-api.ts` (modified — `refreshWorkspaceStatus()` added)
- `source/frontend/src/features/workspace/state/useWorkspaceStatus.ts` (new)

---

## Validation

### BA-01 (unchanged, `90544cb`)

- **Backend, BA-01 tests only:** `pytest tests/test_workspace_resolution_service.py tests/test_workspace_api.py -v` (with `JWT_SECRET_KEY` set, `TD-010`'s own pre-existing environment note) → **11 passed, 0 failed** (6 service-layer + 5 API).
- **Frontend:** `tsc --noEmit` — 0 errors. `eslint` — 0 problems.

### BA-02 (this pass)

- **Backend, BA-02 tests only:** `pytest tests/test_workspace_status_service.py tests/test_workspace_status_api.py -v` (with `JWT_SECRET_KEY` set, `TD-010`'s own pre-existing environment note) → **10 passed, 0 failed** (6 service-layer + 4 API).
- **Backend, full regression:** `pytest tests/ -q` → **708 passed, 0 failed** (698 prior + 10 new), zero regressions.
- **Migration:** `alembic heads` → single head, `b1d6f4c8a3e7` (unchanged — no new table, no migration this Business Activity).
- **Frontend:** `tsc --noEmit` → 0 errors. `eslint` (new/modified files) → 0 problems.
- **App wiring:** `main.py` unchanged this pass (no new router mount needed — `POST /workspaces/refresh-status` added to the already-mounted `workspace.router`); route present in the route table; `/workspaces` prefix exemption (added for BA-01) covers this endpoint unchanged.
- **Python linting:** no dedicated linting tool (ruff/flake8/pylint) is configured anywhere in this repository's own CI (`authservice-ci.yml` runs only `pytest`) or `venv` — same as every prior Work Package, including BA-01. Compliance verified via `py_compile` (syntax-clean) plus direct conformance to the existing codebase's own established style (mirrors `identity_status_service.py` exactly).

---

## Technical Debt Raised

None new, either pass. `ERB-C008-02`/`03`/`04`/`05`'s own exclusion was already consolidated as `TD-111` during Governance Consolidation, prior to BA-01. BA-02's own dormant `home_node_id`-absent branch is the same disclosed class as `TD-104` (dormant today, per `TD-032`) — not a new entry, cross-referenced in BA-02's own Business Activity Contract above rather than duplicated.

---

## Status (BA-01, BA-02)

BA-01: **Implementation Complete**, committed `90544cb`. BA-02: **Implementation Complete**, this pass. `EX-C008-03`–`09` (`ERB-C008-02`/`03`/`04`/`05`): **Excluded** (disclosed, `TD-111`). BA-03 not yet started — requires separate Repository Owner approval before proceeding, per the governing instruction's own one-Business-Activity-at-a-time methodology. Not yet submitted for Independent Certification — that occurs once all three authorized Business Activities (`IRA-009 §4.8`) are complete, per this Work Package's own precedent (`WP-08` submitted BA-01 through BA-03 together, not per-BA).

---

*End of IMP-REPORT-WP-09 (BA-01, BA-02). Awaiting Repository Owner approval before BA-03 begins.*
