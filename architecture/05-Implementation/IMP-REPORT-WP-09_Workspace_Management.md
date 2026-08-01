# IMP-REPORT-WP-09 — Workspace Management (C-008)

**Work Package:** WP-09 — Workspace Management (C-008)
**Governing Readiness Assessment:** `IRA-009_WP-09_Workspace_Management_Implementation_Readiness_Assessment.md` (Accepted — READY, scoped: 3 Business Activities realizing `EX-C008-01`/`02`/`10`/`11`; `ERB-C008-02`/`03`/`04`/`05` — `EX-C008-03`–`09` — excluded, consolidated as `TD-111`).
**Governing Business Object:** None. All three authorized Business Activities are read-only queries/classifications against existing `Membership`/`Organization`/`Role` data (`IRA-009 §6` — not applicable, no new persisted construct proposed).
**Governing Capability Specification:** `PE-001-C008_Workspace_Management.docx` v1.3 (`ERB-C008-01` through `06`; `EX-C008-01` through `11`).
**Repository Owner Authorization:** Granted per Repository Owner Instruction "Release B – WP-09 Implementation Authorization," 2026-08-01.
**Scope of this report:** BA-01 only (`EX-C008-01`/`02`). BA-02 and BA-03 are implemented one Business Activity at a time per the governing instruction's own methodology — each requires separate Repository Owner approval before proceeding.

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

## Strategic Enhancements

| Strategic Enhancement | Implemented in WP-09 | Deferred | Justification |
|---|---|---|---|
| Real, Membership-derived Workspace candidate list (replacing the static, identical-for-every-user config) | Yes (BA-01) | — | Directly realizes `EX-C008-01`/`02`, the capability this Work Package charters. |
| Governed Workspace entry/switch/re-entry | — | Yes | `ERB-C008-02`/`04`/`05` require an unconditional Access Evaluation Outcome, structurally unobtainable (`TD-111`). Not this Work Package's authorized scope (`IRA-009 §4.2`/`§4.4`/`§4.5`). |
| Configuration Profiles, Branding, Theme, Terminology, Localization, Accessibility Profiles | — | Yes | C-041/WP-10's own scope, per `PRODUCT-MILESTONE-ROADMAP.md` §3 (Milestone 1). Explicitly out of this Work Package's own charter. |
| Saved Views, Progressive Disclosure four-state widget contract | — | Yes | Not named in `PE-001-C008`'s own governed scope for BA-01; `WorkspaceSwitcher` is a navigation menu, not a data-bearing widget in `IMP-001 §10.3`'s own sense (`IRA-009 §7`, already disclosed as Not Applicable). |

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
- `source/frontend/src/components/layout/WorkspaceSwitcher.tsx` (modified)
- `architecture/05-Implementation/IMP-REPORT-WP-09_Workspace_Management.md` (this report, new)

---

## Validation

- **Backend, BA-01 tests only:** `pytest tests/test_workspace_resolution_service.py tests/test_workspace_api.py -v` (with `JWT_SECRET_KEY` set, `TD-010`'s own pre-existing environment note) → **11 passed, 0 failed** (6 service-layer + 5 API).
- **Backend, full regression:** `pytest tests/ -q` → **698 passed, 0 failed** (687 prior + 11 new), 605.95s, zero regressions.
- **Migration:** `alembic heads` → single head, `b1d6f4c8a3e7` (unchanged — no new table, no migration this Business Activity).
- **Frontend:** `tsc --noEmit` → 0 errors. `eslint` (new/modified files) → 0 problems.
- **App wiring:** `main.py` imports cleanly; `GET /workspaces/candidates` present in the route table; `/workspaces` prefix exempted from `TenantMiddleware`.
- **Python linting:** no dedicated linting tool (ruff/flake8/pylint) is configured anywhere in this repository's own CI (`authservice-ci.yml` runs only `pytest`) or `venv` — same as every prior Work Package. Compliance verified via `py_compile` (syntax-clean) plus direct conformance to the existing codebase's own established style (mirrors `identity_status_service.py`/`routers/identity.py` exactly).

---

## Technical Debt Raised

None new. `ERB-C008-02`/`03`/`04`/`05`'s own exclusion was already consolidated as `TD-111` during Governance Consolidation, prior to this implementation pass — no duplicate entry raised here.

---

## Status (BA-01)

BA-01: **Implementation Complete**. `EX-C008-03`–`09` (`ERB-C008-02`/`03`/`04`/`05`): **Excluded** (disclosed, `TD-111`). BA-02 and BA-03 not yet started — each requires separate Repository Owner approval before proceeding, per the governing instruction's own one-Business-Activity-at-a-time methodology. Not yet submitted for Independent Certification — that occurs once all three authorized Business Activities (`IRA-009 §4.8`) are complete, per this Work Package's own precedent (`WP-08` submitted BA-01 through BA-03 together, not per-BA).

---

*End of IMP-REPORT-WP-09 (BA-01). Awaiting Repository Owner approval before BA-02 begins.*
