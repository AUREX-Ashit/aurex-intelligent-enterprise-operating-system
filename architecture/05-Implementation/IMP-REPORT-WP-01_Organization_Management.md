# IMP-REPORT-WP-01 — Organization Management (C-004)

**Type:** Living Implementation Report (audit trail — not a duplicate of the codebase)
**Work Package:** WP-01 — Organization Management
**Governing documents:** IRA-001 (`architecture/05-Implementation/IRA-001_WP-01_Organization_Management_Implementation_Readiness_Assessment.md`), ADR-003, ADR-004, ADR-005 (`architecture/07-Decisions/`)
**Maintenance rule:** One report for all of WP-01. Append a new Business Activity section per completion; update the dashboard each time. Do not create per-Business-Activity report files.
**Technical Debt:** Per CLAUDE.md §19.8, non-blocking Independent Review observations are tracked in `architecture/06-Reviews/TECH-DEBT.md`, not repeatedly re-stated in full across Business Activity sections. Historical BA-01 through BA-04 review sections below predate this register and are left as originally written (this is an audit trail, not rewritten history) — their carried-forward items are backfilled into the register as TD-001 through TD-011. From BA-05 onward, Independent Review sections reference the relevant `TD-NNN` ID instead of repeating an already-recorded observation.

---

## WP-01 Progress Dashboard

**Overall Status:** 🟡 In Progress

**Business Activities** (revised per WP-01 Scope Reconciliation, below — 8 planned items corrected to 7, aligned with PE-001-C004's canonical ERBs)

- ✅ BA-01 Establish Organization Identity
- ✅ BA-02 Resolve Organization Details
- ✅ BA-03 Search & List Organizations
- ✅ BA-04 Steward Organization Identity
- ✅ BA-05 Reactivate Suspended Organization
- ✅ BA-06 Suspend Organization
- ✅ BA-07 Retire Organization & Preserve Continuity

**Progress**

- Total Business Activities: 7 (revised from 8 — Configure Organization and Audit History removed; neither is a canonical C-004 Business Activity per PE-001-C004. See WP-01 Scope Reconciliation, below.)
- Completed: 7 / 7 — all 7 Business Activities implementation-complete, developer-validated, and independently reviewed (ACCEPTED / ACCEPTED WITH OBSERVATIONS). WP-01 as a whole is not yet closed: Independent Certification per CLAUDE.md §19.7 remains a separate, later WP-level activity.
- Remaining: 0 Business Activities. WP-01 Certification remains outstanding.
- Progress: 100% (Business Activity implementation); WP-01 Closure gate (§19.7) still pending WP-level Independent Certification.
- Database migrations completed: 2 (`b3f7a1c9d2e4` — `organizations.status`/`description`; `d2d840d224b6` — widens `ck_organizations_status` to include `RETIRED`, BA-07)
- API endpoints delivered: 7 (`POST /organizations`, `GET /organizations/{organization_id}`, `GET /organizations`, `PUT /organizations/{organization_id}`, `POST /organizations/{organization_id}/activate`, `POST /organizations/{organization_id}/suspend`, `POST /organizations/{organization_id}/retire`)
- UI screens delivered: 1 (`/platform-admin/organizations` — unchanged by BA-05/BA-06/BA-07, all three implemented backend-only per their explicit scope; see their sections)
- Tests (running totals, not a per-BA delta): 33 unit, 61 integration, 2 dedicated middleware — 96 total across `test_organization_service.py`/`test_organization_api.py`/`test_tenant_middleware.py`; BA-07 itself added 20 (8/12/0) — see BA-07 section for the exact breakdown. Full repository suite: 125/125 passing.
- ADRs raised during implementation: 0 across BA-01 through BA-07 (ADR-003, ADR-004, ADR-005 were recorded during the WP-01 readiness assessment, prior to implementation start — see IRA-001). No ADR was raised for the WP-01 Scope Reconciliation or for BA-07 either — see below.

---

## Business Activity: BA-01 — Establish Organization

**Date Completed:** 2026-07-21

### Scope Delivered

Full vertical slice for creating a new Organization: database schema extension, domain model, repository, Business Activity service (validation, duplicate rejection, audit, domain event), authorization-gated REST API, Platform Administrator UI screen, unit tests, integration tests, and OpenAPI contract. Implements IRA-001 §2.2's first Business Activity, scoped per ADR-003 (AuthService ownership), ADR-004 (Organization Profile/CRUD/Lifecycle subset, not the full canonical `organization_master`), and ADR-005 (interim `ACTIVE`/`SUSPENDED` lifecycle model).

### Files Created

| File | Purpose |
|---|---|
| `Backend/Services/AuthService/alembic/versions/2026_07_20_1930-b3f7a1c9d2e4_organization_lifecycle_profile_fields.py` | Migration adding `status`, `description` to `organizations` |
| `Backend/Services/AuthService/repositories/organization_repository.py` | `OrganizationRepository.get_by_code()` |
| `Backend/Services/AuthService/schemas/organization.py` | `EstablishOrganizationRequest`, `OrganizationResponse` |
| `Backend/Services/AuthService/dependencies.py` | `get_current_claims`, `require_platform_admin` (shared authorization dependency) |
| `Backend/Services/AuthService/services/organization_service.py` | `OrganizationService.establish()` Business Activity orchestration |
| `Backend/Services/AuthService/routers/organization.py` | `POST /organizations` |
| `Backend/Services/AuthService/tests/test_organization_service.py` | Unit tests |
| `Backend/Services/AuthService/tests/test_organization_api.py` | Integration tests |
| `Backend/Services/AuthService/organization-api.yaml` | OpenAPI contract |
| `source/frontend/src/types/organization.ts` | TS types mirroring the backend schema |
| `source/frontend/src/services/organization-api.ts` | API wrapper |
| `source/frontend/src/features/organization/state/useEstablishOrganization.ts` | Form/business state hook |
| `source/frontend/src/features/organization/components/EstablishOrganizationForm.tsx` | Form component |
| `source/frontend/src/features/organization/components/OrganizationResultPanel.tsx` | Result display |
| `source/frontend/src/features/organization/components/OrganizationManagementScreen.tsx` | Screen composing the above |

### Files Modified

| File | Summary of Changes |
|---|---|
| `Backend/Services/AuthService/models/organization.py` | Added `OrganizationStatus` enum, `status`/`description` columns |
| `Backend/Services/AuthService/main.py` | Registered `organization` router |
| `Backend/Services/AuthService/routers/__init__.py` | Exported `organization_router` |
| `Backend/Services/AuthService/middleware/tenant.py` | Added `/organizations` to the tenant-exemption list |
| `Backend/Services/AuthService/services/auth_service.py` | Added module-level `decode_access_token()` |
| `Backend/Services/AuthService/README.md` | New "Organization Management (WP-01)" section; updated feature list and project-structure tree |
| `source/frontend/src/app/platform-admin/(workspace)/organizations/page.tsx` | Replaced placeholder with `OrganizationManagementScreen` |
| `source/frontend/src/features/README.md` | Documented the new `features/organization/` module |

### Database

- **Migration:** `8fac154e79e2` → `b3f7a1c9d2e4`, purely additive. Validated `upgrade`/`downgrade`/`upgrade` against a real Postgres 16 container (not SQLite-only), confirmed via `\d organizations`.
- **Schema changes:** `organizations.status` (VARCHAR(20), NOT NULL, default `'ACTIVE'`), `organizations.description` (VARCHAR(1000), nullable).
- **Constraints:** `ck_organizations_status` CHECK (`status IN ('ACTIVE','SUSPENDED')`).
- **Indexes:** None added (existing `organization_code` unique index already supports this Business Activity's lookup).

### APIs

- **Endpoint added:** `POST /organizations` (201/400/401/403/409/422).
- **Request/Response models:** `EstablishOrganizationRequest` → `OrganizationResponse` (`schemas/organization.py`; contract mirrored in `organization-api.yaml`).
- **Authorization:** Bearer access token required; caller must hold `role_code == PLATFORM_ADMIN` (`dependencies.require_platform_admin`). Domain Permission-level checks (URA-001 §4) are out of scope per IRA-001 §2.7 — tracked as a known limitation, not a silent gap.

### Frontend

- **Route:** `/platform-admin/organizations` (existing placeholder route, now live).
- **Screen:** `OrganizationManagementScreen` (form + result panel).
- **Components:** `EstablishOrganizationForm`, `OrganizationResultPanel` — composed entirely from existing DS-001-derived primitives (`Card`, `StatusBadge`, `Button`, `Input`, `Spinner`, `Form*`); no new design-system component invented.
- **API integration:** `services/organization-api.ts` → shared `apiClient` (automatic bearer-token injection).

### Testing

- **Unit Tests:** 3 (`test_organization_service.py`) — creation defaults, optional field omission, duplicate rejection with no extra row.
- **Integration Tests:** 8 (`test_organization_api.py`) — success, duplicate (409), missing/invalid/wrong-role auth (400/401/403), missing/empty required fields (422), tenant-header exemption.
- **API Tests:** covered by the integration suite above (same file, HTTP-level).
- **UI Tests:** none added — no frontend test harness exists yet in `source/frontend` (pre-existing gap, not introduced by this Business Activity); verified instead via `tsc --noEmit` (0 errors).
- **Overall test results:** 40/40 backend tests passing (11 new, 0 regressions). Frontend: 0 TypeScript errors.

### Manual Verification

1. `alembic upgrade head` against a Postgres instance; confirm `organizations` has `status`/`description` columns and the `ck_organizations_status` constraint.
2. Obtain a `PLATFORM_ADMIN` access token via `POST /auth/login` against a bootstrapped environment (WP-00's seeded `platform.admin@corpstage.com`).
3. `POST /organizations` with that token and a unique `organization_code` → expect `201` with `status: "ACTIVE"`.
4. Repeat the same request → expect `409`.
5. Repeat without the `Authorization` header → expect `400`; with a non-`PLATFORM_ADMIN` token → expect `403`.
6. In the frontend, sign in as the Platform Administrator, navigate to `/platform-admin/organizations`, submit the form → confirm the result panel renders the created organization.

### Known Limitations (intentionally deferred, per WP-01 scope)

- Domain Permission-level authorization (URA-001 §4 VIEW/EDIT/APPROVE) is not implemented — `PLATFORM_ADMIN`-only gating is a documented interim simplification (IRA-001 §2.7), pending the Role & Permission Management work package.
- Lifecycle is a plain `status` column, not SD-002-051's metadata-driven state machine — interim per ADR-005, pending a Metadata Runtime.
- Only the ADR-004-approved Profile subset (`organization_code`, `organization_name`, `organization_type`, `description`) is implemented; the full canonical `organization_master` shape (industry taxonomy, reporting framework, financials, etc.) is deferred to future work packages.
- RLS on the `organizations` table itself was not added — IRA-001 §11 flagged this as an open, non-blocking confirmation item; not resolved by this Business Activity.
- No frontend test harness exists yet — verification here relied on `tsc --noEmit` plus manual steps, not automated UI tests.
- View/Search/Update/Activate/Suspend/Configuration/Audit History Business Activities are not yet implemented (dashboard above).

### Architecture Compliance

- **ARCH-000:** No architecture redefinition; implementation only.
- **IMP-001:** Business Activity Lifecycle followed (§6.3) — validation → business rule → object update → domain event → audit → response. No raw CRUD exposed as the primary interface (§1.7) — the endpoint is named and contracted as a Business Activity.
- **ERG-001:** No EnterpriseNode/Relationship/View concepts implemented or altered (out of WP-01 scope); Organization remains the separate, higher-level concept ERG-001-03 assumes.
- **C-004:** Scope matches ADR-004's approved subset exactly.
- **URA-001:** No Role/Permission/Membership concept altered; `organizations.id` remains the FK target `Membership.organization_id` already depends on (unchanged, unbroken — full suite green).
- **Approved ADRs:** ADR-003, ADR-004, ADR-005 — all three implemented as recorded, none re-litigated. No new ADR was required during this Business Activity's implementation.

### Implementation Status

✅ IMPLEMENTATION COMPLETE

### Independent Review

**Independent Review: Accepted — ACCEPT WITH OBSERVATIONS** (2026-07-21, fresh-context subagent with no memory of the implementation session; ran the full test suite and `tsc --noEmit` independently rather than trusting this report's claims).

Observations recorded (none blocking, none require remediation before BA-02):

1. `ck_organizations_status` exists in the migration but is not declared on the ORM model (`models/organization.py`) — model/migration drift; no test currently exercises the constraint.
2. The `IntegrityError` concurrent-duplicate-race branch in `OrganizationService.establish()` is implemented but not covered by a dedicated test (only the sequential pre-check path is tested).
3. Audit/event emission happens after `flush()` but before the outer session commit — a post-flush commit failure would emit a false-success signal. Low severity given the interim, log-only observability mechanism.
4. ~~Nothing in the repository (WP-00 through BA-01) is committed yet~~ — **resolved 2026-07-21**: committed as `d5150ab` (WP-00 + IC-001 remediation + WP-00A), `56994ae` (WP-01 IRA-001 + ADR-003/004/005), `145acfe` (BA-01 Establish Organization). Working tree clean, all three §19.7 completion-gate conditions now satisfied.
5. `get_current_claims` returns 400 (not 401) for a missing Authorization header — deliberate and tested, flagged only as a design note.

Recommendation from review: pick up observations 1–2 opportunistically in a later BA rather than blocking.

### Certification

Certification Status: Pending (WP-level activity, performed only after WP-01 completes, per CLAUDE.md §19.7)

---

## Ready for Review — BA-01 Establish Organization

**Summary of what was implemented:** Full vertical slice for creating a new Organization — migration, model, repository, `OrganizationService.establish()` Business Activity, `POST /organizations` (PLATFORM_ADMIN-gated), `/platform-admin/organizations` UI screen, unit + integration tests, OpenAPI contract. Detail above.

**Evidence available:**
- Migration validated up/down/up against a real Postgres 16 container (`\d organizations` output on record with the implementer).
- 40/40 backend tests passing (11 new — `tests/test_organization_service.py`, `tests/test_organization_api.py`).
- `tsc --noEmit` — 0 TypeScript errors.
- `organization-api.yaml` and `auth-api.yaml` both YAML-validated.

**Known issues:** None outside the Known Limitations listed above (all are deliberate WP-01 scope deferrals, not defects).

**Recommended next Business Activity:** BA-02 View Organization (read-side; lowest-risk next step, per IRA-001 §9/§10's recommended sequence, and a dependency for BA-03 Search).

---

## Business Activity: BA-02 — View Organization Details

**Date Completed:** 2026-07-21

### Scope Delivered

Read-only vertical slice for fetching a single Organization by id: `GET /organizations/{organization_id}`, gated by the same `require_platform_admin` dependency BA-01 introduced, returning 404 for an unknown id. No database or model change was required — reused every existing layer (model, `OrganizationRepository.get_by_id()` via `BaseRepository`, `OrganizationResponse` schema) as-is. Extended `TenantMiddleware`'s exemption from an exact-match list entry to a prefix match (`/organizations` and `/organizations/*`) since BA-02 introduced the first path-parameterized Organization endpoint — this covers this and every future WP-01 endpoint under the same prefix without further middleware edits. No ADR was required.

### Files Created

| File | Purpose |
|---|---|
| `source/frontend/src/features/organization/components/OrganizationDetailsList.tsx` | Shared presentational definition-list, extracted from BA-01's `OrganizationResultPanel` so Establish and View render organization details identically instead of duplicating markup |
| `source/frontend/src/features/organization/state/useViewOrganization.ts` | View Organization Details state hook |
| `source/frontend/src/features/organization/components/ViewOrganizationSection.tsx` | ID input + result display |

### Files Modified

| File | Summary of Changes |
|---|---|
| `Backend/Services/AuthService/services/organization_service.py` | Added `OrganizationService.get_details()`; updated module docstring |
| `Backend/Services/AuthService/routers/organization.py` | Added `GET /{organization_id}` |
| `Backend/Services/AuthService/middleware/tenant.py` | Exemption list entry `"/organizations"` generalized to a prefix check covering `/organizations/*` |
| `Backend/Services/AuthService/organization-api.yaml` | Added the `GET /organizations/{organization_id}` path |
| `Backend/Services/AuthService/tests/test_organization_service.py` | Added BA-02 unit tests |
| `Backend/Services/AuthService/tests/test_organization_api.py` | Added BA-02 integration tests |
| `Backend/Services/AuthService/README.md` | Updated Organization Management section/tree for BA-02 files |
| `source/frontend/src/services/organization-api.ts` | Added `getOrganization()` |
| `source/frontend/src/features/organization/components/OrganizationResultPanel.tsx` | Refactored to reuse `OrganizationDetailsList` instead of inline markup |
| `source/frontend/src/features/organization/components/OrganizationManagementScreen.tsx` | Renders `ViewOrganizationSection` alongside the existing Establish flow |

### Database

- **Migration(s):** None — BA-02 required no schema change.
- **Schema changes / Constraints / Indexes:** None.

### APIs

- **Endpoint added:** `GET /organizations/{organization_id}` (200/400/401/403/404/422).
- **Request/Response models:** Path param `organization_id: UUID` (FastAPI-validated, 422 on malformed input) → existing `OrganizationResponse` (no new schema).
- **Authorization:** Same `require_platform_admin` dependency as BA-01 — no new authorization tier introduced (Domain Permission-level view/edit distinction remains deferred, per IRA-001 §2.7).

### Frontend

- **Route:** `/platform-admin/organizations` (unchanged — extended, not a new route).
- **Screen:** `OrganizationManagementScreen` now composes both the BA-01 Establish flow and the new `ViewOrganizationSection`.
- **Components:** `ViewOrganizationSection` (new), `OrganizationDetailsList` (new, shared with BA-01's result panel) — all built from existing `ui/` primitives; no new design-system component invented.
- **API integration:** `services/organization-api.ts`'s new `getOrganization()`, same `apiClient` pattern as BA-01.

### Testing

- **Unit Tests:** 2 new (`test_organization_service.py`, 5 total in that file) — fetch-by-id returns the created organization; unknown id raises 404.
- **Integration Tests:** 6 new (`test_organization_api.py`, 14 total in that file) — success, 404, missing/wrong-role auth (400/403), invalid UUID (422), tenant-header exemption.
- **API Tests:** covered by the integration suite above.
- **UI Tests:** none added — same pre-existing gap as BA-01 (no frontend test harness yet); verified via `tsc --noEmit` (0 errors).
- **Overall test results:** 48/48 backend tests passing (8 new this BA, 0 regressions). Frontend: 0 TypeScript errors.

### Manual Verification

1. Using a `PLATFORM_ADMIN` access token, `POST /organizations` to create one, capture its `id`.
2. `GET /organizations/{id}` with the same token → expect `200` with matching fields.
3. `GET /organizations/{random-uuid}` → expect `404`.
4. Repeat without `Authorization` → `400`; with a non-`PLATFORM_ADMIN` token → `403`; with a malformed id (e.g. `/organizations/not-a-uuid`) → `422`.
5. In the frontend, on `/platform-admin/organizations`, paste a valid organization id into the new "View Organization Details" section and confirm the detail list renders; try an unknown id and confirm the "No organization exists with this ID" banner appears.

### Known Limitations (intentionally deferred, per WP-01 scope)

- Same authorization/lifecycle/schema-scope/RLS/frontend-test-harness limitations as BA-01 (unchanged — see BA-01 section above); none are specific to BA-02.
- No listing/search capability yet — a caller must already know the organization's id (BA-03 Search Organizations addresses this).

### Architecture Compliance

- **ARCH-000:** No architecture redefinition; implementation only.
- **IMP-001:** Read-side Business Activity — no audit record or domain event, consistent with the existing precedent that `PersonRecognitionService.recognize` (a read) is not audited while `establish` (a write) is (§6.3 applies fully to writes; a pure query returns data without a state transition to record).
- **ERG-001:** Unaffected — no EnterpriseNode/Relationship/View concept touched.
- **C-004 / ADR-004:** No new fields exposed beyond the approved subset; `OrganizationResponse` is reused unchanged.
- **URA-001:** Unaffected.
- **Approved ADRs:** ADR-003, ADR-004, ADR-005 — all still honored; none re-litigated. No new ADR raised.

### Implementation Status

✅ IMPLEMENTATION COMPLETE

### Independent Review

**Independent Review: Accepted — CERTIFIED PASS WITH OBSERVATIONS** (2026-07-21, fresh-context subagent with no memory of the implementation session; ran the full test suite and `tsc --noEmit` independently, traced the authorization dependency chain by hand, and diffed the working tree itself rather than trusting this report's claims).

**Findings:** architecture unchanged, no duplicated business logic (`get_details()` reuses `BaseRepository.get_by_id()`; router reuses BA-01's `require_platform_admin` unmodified), no unnecessary schema change (confirmed no new migration and `models/organization.py`/`repositories/organization_repository.py` untouched), authorization unbypassable, `OrganizationDetailsList` extraction genuinely removed the duplicate markup from `OrganizationResultPanel`, no new DS-001 component invented, error handling in `useViewOrganization.ts` (not-found / network-error / generic) is complete, and the "read paths aren't audited" claim was verified true against `PersonRecognitionService.recognize`'s precedent, not just asserted.

**Defect found and corrected:** this report originally mis-stated BA-02's test counts (claimed 5 new unit / 11 new overall; actual is 2 new unit / 8 new overall, verified via `grep -c` against the test files). Corrected above — a report-accuracy issue only, not a code defect; the code and its 8 new tests were always correct.

**Risk recorded (non-blocking):** the `middleware/tenant.py` exemption now uses a prefix match (`/organizations/*`) rather than an exact-match list entry. Correct for BA-02, but means any future sub-resource under this prefix that should be tenant-scoped would be silently exempted unless revisited when added.

**Recommendation carried into BA-03:** add a dedicated `TenantMiddleware` test asserting the `/organizations/*` prefix behavior directly (currently only exercised incidentally via BA-02's own endpoint test).

### Certification

**Certification Status: PASS WITH OBSERVATIONS**

### Repository

Committed as `4d5c52a` — "feat(auth-service): WP-01 BA-02 - View Organization Details" (2026-07-21). Working tree clean at commit time; all three §19.7 completion-gate conditions satisfied.

---

## Ready for Review — BA-02 View Organization Details

**Summary of what was implemented:** `GET /organizations/{organization_id}`, PLATFORM_ADMIN-gated, 404 on unknown id, reusing BA-01's model/repository/schema/auth dependency unchanged. Frontend View Organization Details section added to the existing screen, sharing a newly-extracted `OrganizationDetailsList` component with BA-01's result panel. `TenantMiddleware`'s exemption generalized from exact-match to prefix-match to support the new path parameter.

**Evidence available:**
- 48/48 backend tests passing (8 new — 2 unit, 6 integration).
- `tsc --noEmit` — 0 TypeScript errors.
- `organization-api.yaml` YAML-validated with the new path.
- Manual verification steps above.

**Known issues:** None outside the Known Limitations listed (unchanged from BA-01, none BA-02-specific).

**Recommended next Business Activity:** BA-03 Search Organizations, per IRA-001's recommended sequence — natural follow-on now that both create and fetch-by-id exist.

---

## Business Activity: BA-03 — Search & List Organizations

**Date Completed:** 2026-07-21

### Scope Delivered

The primary Organization Management screen: `GET /organizations` with text search (name/code substring, case-insensitive), status filter, pagination (skip/limit, max 100/page), and whitelisted sort (name/code/created_at, asc/desc), returning a page plus a total count. Frontend: `/platform-admin/organizations` restructured so the search/list grid is the primary view, with Create Organization and View Details as modal actions reusing BA-01's and BA-02's existing forms/hooks unchanged. No database migration and no new authorization tier — reused BA-01/BA-02's model, `require_platform_admin`, and response schema throughout. No ADR required.

### Files Created

| File | Purpose |
|---|---|
| `source/frontend/src/features/organization/state/useSearchOrganizations.ts` | Search/filter/sort/pagination state hook |
| `source/frontend/src/features/organization/components/OrganizationSearchGrid.tsx` | The primary grid: search, status filter, sortable columns, table, pagination, empty/loading/error states |

### Files Modified

| File | Summary of Changes |
|---|---|
| `Backend/Services/AuthService/repositories/organization_repository.py` | Added `search()` — whitelisted sort columns, ILIKE text match, status filter, offset/limit, count query |
| `Backend/Services/AuthService/schemas/organization.py` | Added `OrganizationSortField`, `SortOrder` enums and `OrganizationListResponse` |
| `Backend/Services/AuthService/services/organization_service.py` | Added `OrganizationService.search()` (thin pass-through to the repository, consistent with the existing Business Activity orchestration layer) |
| `Backend/Services/AuthService/routers/organization.py` | Added `GET ""` (list/search) — coexists with the existing `POST ""` at the same path, differentiated by HTTP method; no route-ordering conflict with `GET /{organization_id}` since query params, not a path segment, carry the search criteria |
| `Backend/Services/AuthService/organization-api.yaml` | Added the `GET /organizations` path and `OrganizationListResponse` schema |
| `Backend/Services/AuthService/tests/test_organization_service.py` | Added BA-03 unit tests |
| `Backend/Services/AuthService/tests/test_organization_api.py` | Added BA-03 integration tests |
| `Backend/Services/AuthService/README.md` | Updated Organization Management section for BA-03 |
| `source/frontend/src/types/organization.ts` | Added `OrganizationSortField`, `SortOrder`, `SearchOrganizationsParams`, `OrganizationListResponse` |
| `source/frontend/src/services/organization-api.ts` | Added `searchOrganizations()` |
| `source/frontend/src/features/organization/components/OrganizationManagementScreen.tsx` | Restructured: grid is now primary; Create and View Details became `Modal`-based actions (reusing `EstablishOrganizationForm` and `useViewOrganization`/`OrganizationDetailsList` unchanged); a second, independent `useViewOrganization` instance keeps the grid's View modal from leaking state into the standalone by-ID lookup section |

### Files Removed

| File | Reason |
|---|---|
| `source/frontend/src/features/organization/components/OrganizationResultPanel.tsx` | Became dead code once the Create modal stopped needing a result panel (the modal closes and the grid refreshes immediately on success — a "no results yet" panel was never actually visible); confirmed zero remaining imports before deletion |

### Database

- **Migration(s):** None — BA-03 required no schema change.
- **Schema changes / Constraints / Indexes:** None. (`organization_code` already has a unique index from BA-00/BA-01, which also serves code-prefix searches reasonably; no new index added for the `ilike` name/code search since WP-01's data volumes don't yet warrant one — a candidate for a future performance pass, not this Business Activity.)

### APIs

- **Endpoint added:** `GET /organizations` (200/400/401/403/422).
- **Query parameters:** `q` (optional, ≤255 chars), `status` (optional, `ACTIVE`/`SUSPENDED`), `skip` (≥0, default 0), `limit` (1-100, default 20), `sort_by` (`organization_name`/`organization_code`/`created_at`, default `organization_name`), `sort_order` (`asc`/`desc`, default `asc`) — all FastAPI/Pydantic-validated (422 on out-of-range or invalid enum values).
- **Response model:** `OrganizationListResponse` (`items: OrganizationResponse[]`, `total`, `skip`, `limit`) — `items` reuses the existing `OrganizationResponse` unchanged.
- **Authorization:** Same `require_platform_admin` dependency as BA-01/BA-02 — no new tier.
- **OpenAPI:** `organization-api.yaml` updated with the new path, parameters, and `OrganizationListResponse` schema; validated.

### Frontend

- **Route:** `/platform-admin/organizations` (unchanged route, restructured content — grid is now primary).
- **Screen:** `OrganizationSearchGrid` — search input, status filter buttons (All/Active/Suspended), sortable column headers (click to toggle field/direction), results table, Previous/Next pagination, "Create Organization" action, per-row "View Details" action, empty state (with a contextual "create the first organization" prompt when no filters are active), loading state (`Spinner`), error state (`FormBanner` with retry).
- **Components:** `OrganizationSearchGrid` (new) — built entirely from existing `Table`/`TableHead`/`TableBody`/`TableRow`/`TableHeaderCell`/`TableCell`, `Card`, `Button`, `Input`, `StatusBadge`, `Spinner`, `FormBanner`. **No new DS-001 component was created** — sorting uses clickable table headers and status filtering uses a `Button` toggle group rather than introducing a `Select`/`Filter Bar`/`Pagination` primitive, since existing components fully covered BA-03's needs (per "do not create new DS-001 components unless absolutely required").
- **Navigation:** No new route — Create and View Details are `Modal`-based actions on the existing route, consistent with "provide the Platform Administrator with the primary Organization Management screen" rather than spreading the capability across multiple routes.
- **API integration:** `services/organization-api.ts`'s new `searchOrganizations()`, same `apiClient` pattern; `useSearchOrganizations.ts` re-fetches on every query-parameter change and exposes a `refresh()` used for error-state retry.

### Testing

- **Unit Tests:** 6 new (`test_organization_service.py`, 11 total in that file) — default paging, case-insensitive name match, code match, status filter, pagination correctness (page contents and total), descending sort.
- **Integration Tests:** 10 new (`test_organization_api.py`, 24 total in that file) — list with total, text-query filter, status filter, pagination params end-to-end, limit>100 rejected (422), negative skip rejected (422), invalid sort_by rejected (422), missing/wrong-role auth (400/403), tenant-header exemption.
- **API Tests:** covered by the integration suite above.
- **UI Tests:** none added — same pre-existing gap as BA-01/BA-02 (no frontend test harness yet); verified via `tsc --noEmit` (0 errors).
- **Overall test results:** 64/64 backend tests passing (16 new this BA, 0 regressions). Frontend: 0 TypeScript errors.

### Manual Verification

1. Seed a few organizations via the "Create Organization" modal.
2. On `/platform-admin/organizations`, confirm they appear in the grid with correct name/code/type/status.
3. Type a partial name or code into the search box → confirm the grid narrows to matches only.
4. Click "Active"/"Suspended"/"All" → confirm the grid filters accordingly (all seeded orgs are `ACTIVE`, so "Suspended" should show the empty state).
5. Click a sortable column header twice → confirm ascending then descending order; confirm the arrow indicator matches.
6. With more than one page of results (`limit` default 20 — seed 21+ to exercise this, or verify via the API directly with a small `limit`), confirm Previous/Next and the "Showing X–Y of Z" text are correct, and that Previous is disabled on the first page / Next disabled on the last.
7. Click "View Details" on a row → confirm the modal shows that organization's full details (via a real `GET /organizations/{id}` call, not just the row's already-loaded data).
8. Click "Create Organization", submit a valid new organization → confirm the modal closes and the new organization appears in the grid without a manual refresh.
9. Directly against the API: `GET /organizations?limit=101` → 422; `GET /organizations?skip=-1` → 422; `GET /organizations?sort_by=bogus` → 422; omit `Authorization` → 400; non-`PLATFORM_ADMIN` token → 403.

### Known Limitations (intentionally deferred, per WP-01 scope)

- Same authorization/lifecycle/schema-scope/RLS/frontend-test-harness limitations as BA-01/BA-02 (unchanged — see BA-01 section above); none are specific to BA-03.
- No index added for the `ilike` name/code search — acceptable at WP-01's current data volume; a candidate for a future performance-focused pass if/when organization counts grow large, not part of this Business Activity's scope.
- "View Details" from the grid makes a live API call rather than reusing the row's already-fetched data, by design (exercises the real BA-02 Business Activity uniformly regardless of entry point) — a deliberate consistency-over-micro-optimization choice, not an oversight.

### Architecture Compliance

- **ARCH-000:** No architecture redefinition; implementation only.
- **IMP-001:** Read-side Business Activity — no audit record or domain event, same precedent as BA-02 (`get_details`) and Person's `recognize`.
- **ERG-001:** Unaffected — no EnterpriseNode/Relationship/View concept touched.
- **C-004 / ADR-004:** No new fields exposed; `OrganizationListResponse.items` reuses the existing, unchanged `OrganizationResponse`.
- **URA-001:** Unaffected.
- **Approved ADRs:** ADR-003, ADR-004, ADR-005 — all still honored; none re-litigated. No new ADR raised.

### Implementation Status

✅ IMPLEMENTATION COMPLETE

### Independent Review

**Independent Review: Accepted — ACCEPT WITH OBSERVATIONS** (2026-07-21, fresh-context subagent with no memory of the implementation session; ran the full backend test suite and `tsc --noEmit` independently, diffed the working tree itself, and traced the SQL sort-whitelisting/count-query/authorization logic by hand rather than trusting this report's claims).

**Test results actually observed:** Backend `pytest -q` → **64 passed, 0 failed**. Confirmed via `grep -c` (not trusted from the report) that BA-03 added exactly 6 new unit tests (11 total in `test_organization_service.py`) and 10 new integration tests (24 total in `test_organization_api.py`) — unlike BA-02, this report's test-count claim was accurate on first read. Frontend `tsc --noEmit` → 0 errors.

**Findings:** `sort_by` is whitelisted twice — once at the Pydantic `OrganizationSortField` enum (422 on any other value before the repository is reached) and again via the repository's `_SORTABLE_COLUMNS` dict lookup (never string-interpolated or resolved via `getattr()`); no SQL injection surface. The total-count query is built and filtered independently of the paginated `stmt` and is correctly unaffected by `.offset()/.limit()` — verified against `test_search_pagination_returns_correct_page_and_total`. ILIKE matching against both `organization_name` and `organization_code` is correctly case-insensitive. Authorization uses `require_platform_admin` unmodified from BA-01/BA-02 — no new tier. `OrganizationService.search()` is a genuine thin pass-through with no duplicated query logic. `middleware/tenant.py` has zero diff — BA-02's prefix-match exemption already covers `GET /organizations` without further changes. `models/organization.py` and `alembic/` show zero diff — no schema change, as claimed. `OrganizationResultPanel.tsx`'s only remaining string match repo-wide is a historical code comment, not an import — its deletion is safe. `OrganizationSearchGrid.tsx` and the restructured screen import only pre-existing DS-001 primitives (`Table*`, `Card`, `Button`, `Input`, `StatusBadge`, `Spinner`, `FormBanner`, `Modal` — `Modal` confirmed to predate BA-01, introduced in the DS-001 v1.0 release commit `18d0396`); no new component invented.

**Defects found:** None.

**Risks recorded (non-blocking):**
1. `useSearchOrganizations.ts` fetches on every keystroke with no debounce and no `AbortController`/staleness guard — a slow, out-of-order network response could briefly overwrite the grid with stale results. Self-corrects on the next state change; a hardening candidate, not a defect.
2. BA-02's carried-forward recommendation (a dedicated `TenantMiddleware` test asserting the `/organizations/*` prefix behavior directly) was not actioned in BA-03 either — re-carried forward below.
3. The `SUSPENDED` status-filter tests (unit and integration) only assert an empty result, since no Activate/Suspend Business Activity exists yet to produce a `SUSPENDED` row — the filter's ACTIVE branch is proven, but true inclusion/exclusion against a mixed-status dataset is not yet provable. Expected to self-resolve once BA-05/BA-06 land.
4. The grid fully remounts (`key={gridRefreshKey}`) after a successful create, resetting the user's active search/filter/sort/page to defaults rather than preserving them. Functionally correct; a UX nuance, not a defect against BA-03's stated scope.
5. Backend tests require `JWT_SECRET_KEY` set out-of-band with no fixture/`.env.example` documenting it — pre-existing since BA-01, re-flagged so it doesn't keep tripping reviewers/CI.

**Recommendations carried into BA-04:**
- Add the dedicated `TenantMiddleware` prefix test (recommended after BA-02, still outstanding after BA-03).
- Consider a debounce + request-cancellation/staleness guard for `useSearchOrganizations` before more interactive filters are added.
- When BA-05/BA-06 land, add a true positive/negative status-filter test (an ACTIVE row that must not appear under a SUSPENDED filter and vice versa).
- Continue the established pattern (thin service pass-through, repository owns query logic, schema-level enum whitelisting) — it held up cleanly through BA-03.

### Certification

Certification Status: Pending (WP-level activity, performed only after WP-01 completes, per CLAUDE.md §19.7)

### Repository

Committed as `95fd4fe` — "feat(auth-service): WP-01 BA-03 - Search & List Organizations" (2026-07-21). Working tree clean at commit time; all three §19.7 completion-gate conditions satisfied.

---

## Ready for Review — BA-03 Search & List Organizations

**Summary of what was implemented:** `GET /organizations` — text search (name/code, case-insensitive), status filter, pagination (skip/limit, max 100/page), whitelisted sort (name/code/created_at, asc/desc), item count — reusing BA-01/BA-02's model, authorization dependency, and response schema unchanged. Frontend: `/platform-admin/organizations` restructured so `OrganizationSearchGrid` is the primary view, with Create and View Details as `Modal` actions reusing existing forms/hooks. `OrganizationResultPanel.tsx` removed as dead code once superseded.

**Evidence available:**
- 64/64 backend tests passing (16 new this BA — 6 unit, 10 integration), independently re-run by the reviewing subagent.
- `tsc --noEmit` — 0 TypeScript errors, independently re-run.
- `organization-api.yaml` updated and validated with the new path and `OrganizationListResponse` schema.
- Independent review completed: **ACCEPT WITH OBSERVATIONS**, zero defects found.

**Known issues:** None outside the Known Limitations and non-blocking risks listed above (all deliberate WP-01 scope deferrals or low-severity hardening candidates, not defects).

**Recommended next Business Activity:** BA-04 Update Organization, per IRA-001's recommended sequence, once this Business Activity is committed per the §19.7 completion gate.

---

## Business Activity: BA-04 — Update Organization Profile

**Date Completed:** 2026-07-21

### Governing Canonical Assets Reviewed

- `architecture/05-Implementation/IRA-001_WP-01_Organization_Management_Implementation_Readiness_Assessment.md` — §2.2 Business Activity Assessment (row: "Update Organization Profile | Update | Organization | `ORGANIZATION_PROFILE_UPDATED`"), §6 Backend Impact Matrix (flags `BaseRepository` as needing an `update()` method), §9 Implementation Plan (Phase 4).
- `architecture/07-Decisions/ADR-004_Organization_Canonical_Schema_Scope_for_WP-01.md` — confirms Profile (name, code, type, descriptive fields) is in WP-01's approved subset; no schema change needed since these columns already exist.
- `architecture/07-Decisions/ADR-003_*.md`, `ADR-005_*.md` — re-confirmed unaffected (ownership and lifecycle model untouched by this BA).
- `architecture/03-Engineering/IMP-001_Implementation_Playbook.md` §6.3–6.7 — Business Activity Lifecycle (Request → Authorization → Business Validation → Business Rule Execution → Business Object Update → Domain Event Publication → Audit Recording → Response) and the mandatory BAC components.
- Existing WP-01 source: `models/organization.py`, `repositories/organization_repository.py`, `repositories/base_repository.py`, `schemas/organization.py`, `services/organization_service.py`, `routers/organization.py`, `middleware/tenant.py`, and BA-01/BA-02/BA-03's frontend (`useEstablishOrganization.ts`, `EstablishOrganizationForm.tsx`, `OrganizationSearchGrid.tsx`, `OrganizationManagementScreen.tsx`) — reviewed to reuse established patterns, not invent new ones.

### Gap Analysis

- **Satisfied as-is (reused unchanged):** `Organization` model (`organization_name`, `organization_type`, `description` columns already exist from BA-01 — no migration needed); `require_platform_admin` authorization dependency; `OrganizationResponse` schema; `middleware/tenant.py`'s `/organizations/*` prefix exemption (path-based, method-agnostic — already covers a new `PUT` verb on the same path with zero changes); `observability.py`'s `record_audit`/`publish_event`; the Modal/Card/Input/Button/Spinner/FormBanner/FormField/FormLabel DS-001 primitives; the establish/get_details service-method shape as the template for a new `update_profile()` method.
- **Required extension:** `BaseRepository` had no `update()` method (IRA-001 §6 flagged this explicitly as a needed extension) — added, mirroring `create()`'s shape (fetch, mutate in place, defer commit to the session's existing Unit-of-Work). `OrganizationService` needed a new `update_profile()` orchestration method; `routers/organization.py` needed a new `PUT /{organization_id}` route; `schemas/organization.py` needed a new `UpdateOrganizationProfileRequest`; frontend needed a new state hook and form component for this distinct Business Activity flow (state shape and validation differ from Establish's), plus an "Edit" action wired into the existing grid and screen.
- **Missing architecture:** None. No new entity, table, column, service boundary, permission tier, or DS-001 component was required.
- **Potential conflict considered:** whether `organization_code` should be part of this Business Activity's Update surface. ADR-004 groups "code" under the Profile subset generally, but `organization_code` is also the natural key BA-01's uniqueness rule and BA-03's search are built against. IRA-001 §2.2 names the activity "Update Organization Profile" without enumerating exact fields, and no canonical document requires code renaming. Making the code editable here would require re-implementing BA-01's duplicate-check/race-handling logic inside Update — a materially larger, undocumented business rule, not a mechanical field addition. **Decision:** `organization_code` and lifecycle `status` are excluded from `UpdateOrganizationProfileRequest`; only `organization_name`, `organization_type`, and `description` are updatable. This is an implementation-level scope judgment (same category as BA-02's "reads aren't audited" and BA-03's "no new DS-001 component" calls), not an architectural decision — no ADR raised. Recorded here explicitly for independent review to scrutinize, per CLAUDE.md §17's canonical-authority-resolution discipline.
- **Why creation (not reuse) was necessary for the new files:** `useUpdateOrganization.ts` and `UpdateOrganizationForm.tsx` are new because Update Organization Profile is a distinct Business Activity Contract (different input shape, different state transitions — `updating`/`updated`/`error{isNotFound}` vs. Establish's `establishing`/`established`/`error{isConflict}`) that cannot be collapsed into `useEstablishOrganization`/`EstablishOrganizationForm` without conflating two different Business Activities' contracts into one component, which BA-02's `OrganizationDetailsList` extraction precedent already establishes as the wrong direction (extract shared *presentation*, keep distinct *business flows* separate).

### Scope Delivered

`PUT /organizations/{organization_id}` — Update Organization Profile. Updates `organization_name`, `organization_type`, and `description` on an existing organization; 404 if the id doesn't exist. Reuses BA-01/BA-02/BA-03's model, `require_platform_admin` authorization, `OrganizationResponse`, and `TenantMiddleware` exemption unchanged. Frontend: an "Edit" action added alongside each row's "View Details" action in `OrganizationSearchGrid`, opening a pre-filled `UpdateOrganizationForm` in a `Modal`; on success the modal closes and the grid refreshes, mirroring BA-01/BA-03's Create flow exactly. No database migration and no new authorization tier. No ADR required (see Gap Analysis above for the one scope judgment call made and its rationale).

### Files Created

| File | Purpose |
|---|---|
| `source/frontend/src/features/organization/state/useUpdateOrganization.ts` | Update Organization Profile state hook |
| `source/frontend/src/features/organization/components/UpdateOrganizationForm.tsx` | Pre-filled Edit form (name/type/description; code shown read-only) |

### Files Modified

| File | Summary of Changes |
|---|---|
| `Backend/Services/AuthService/repositories/base_repository.py` | Added `update()` — fetch by id, mutate in place, return `None` if not found; commit deferred, same as `create()` |
| `Backend/Services/AuthService/schemas/organization.py` | Added `UpdateOrganizationProfileRequest` |
| `Backend/Services/AuthService/services/organization_service.py` | Added `OrganizationService.update_profile()`; updated module docstring |
| `Backend/Services/AuthService/routers/organization.py` | Added `PUT /{organization_id}` |
| `Backend/Services/AuthService/organization-api.yaml` | Added the `PUT /organizations/{organization_id}` path and `UpdateOrganizationProfileRequest` schema |
| `Backend/Services/AuthService/tests/test_organization_service.py` | Added BA-04 unit tests |
| `Backend/Services/AuthService/tests/test_organization_api.py` | Added BA-04 integration tests |
| `Backend/Services/AuthService/README.md` | Updated Organization Management section for BA-04 |
| `source/frontend/src/types/organization.ts` | Added `UpdateOrganizationProfileRequest` |
| `source/frontend/src/services/organization-api.ts` | Added `updateOrganization()` |
| `source/frontend/src/features/organization/components/OrganizationSearchGrid.tsx` | Added an `onEditOrganization` prop and a per-row "Edit" action |
| `source/frontend/src/features/organization/components/OrganizationManagementScreen.tsx` | Wired `useUpdateOrganization` + `UpdateOrganizationForm` into a new Edit `Modal`, refreshing the grid on success (same pattern as the Create modal) |

### Database

- **Migration(s):** None — `organization_name`, `organization_type`, and `description` already exist on `organizations` from BA-01.
- **Schema changes / Constraints / Indexes:** None.

### APIs

- **Endpoint added:** `PUT /organizations/{organization_id}` (200/400/401/403/404/422).
- **Request/Response models:** `UpdateOrganizationProfileRequest` (`organization_name`, `organization_type` required; `description` optional) → existing `OrganizationResponse` (no new response schema).
- **Authorization:** Same `require_platform_admin` dependency as BA-01/02/03 — no new tier.
- **OpenAPI:** `organization-api.yaml` updated with the new path and request schema; YAML-validated.

### Frontend

- **Route:** `/platform-admin/organizations` (unchanged route, extended content).
- **Screen:** `OrganizationManagementScreen` now composes a third `Modal` (Edit) alongside Create and View Details.
- **Components:** `UpdateOrganizationForm` (new) — built from the same `Card`/`Input`/`Button`/`Spinner`/`FormField`/`FormLabel`/`FormBanner` primitives as `EstablishOrganizationForm`; the `organization_code` field is rendered as a `disabled` `Input` for context, not submitted. **No new DS-001 component was created.**
- **API integration:** `services/organization-api.ts`'s new `updateOrganization()`, same `apiClient.put` pattern already available in the shared client.

### Testing

- **Unit Tests:** 4 new (`test_organization_service.py`, 15 total in that file) — updates name/type/description; leaves `organization_code` and `status` untouched; allows `description` to be cleared by omission; 404 on unknown id.
- **Integration Tests:** 9 new (`test_organization_api.py`, 33 total in that file) — success, 404, missing/wrong-role auth (400/403), missing/empty required field (422), invalid UUID (422), tenant-header exemption, and an explicit test proving a submitted `organization_code` field is silently ignored (Pydantic drops unknown fields by default) rather than applied.
- **API Tests:** covered by the integration suite above.
- **UI Tests:** none added — same pre-existing gap as BA-01/02/03 (no frontend test harness yet); verified via `tsc --noEmit` (0 errors).
- **Overall test results:** 77/77 backend tests passing (13 new this BA, 0 regressions). Frontend: 0 TypeScript errors.

### Manual Verification

1. Using a `PLATFORM_ADMIN` access token, create an organization via `POST /organizations`, capture its `id`.
2. `PUT /organizations/{id}` with new `organization_name`/`organization_type`/`description` → expect `200` with the updated fields; `organization_code` and `status` unchanged.
3. `PUT /organizations/{random-uuid}` → expect `404`.
4. Repeat without `Authorization` → `400`; with a non-`PLATFORM_ADMIN` token → `403`; with an empty `organization_name` → `422`.
5. In the frontend, on `/platform-admin/organizations`, click "Edit" on a row → confirm the modal opens pre-filled with that organization's current values, the code field is visibly read-only, submitting valid changes closes the modal and the grid reflects the update without a manual refresh.

### Known Limitations (intentionally deferred, per WP-01 scope)

- Same authorization/lifecycle/schema-scope/RLS/frontend-test-harness limitations as BA-01/02/03 (unchanged — see BA-01 section above); none are specific to BA-04.
- `organization_code` and lifecycle `status` are not updatable through this Business Activity (see Gap Analysis's scope-judgment rationale above) — status changes are BA-05/BA-06's scope (Activate/Suspend); a future code-rename capability, if ever required, would need its own Business Activity Contract addressing re-validated uniqueness, not a silent extension of this one.
- No optimistic concurrency control (no version/`ETag` field) — a concurrent Update from two callers is last-write-wins, same implicit behavior as every other write path in WP-01 to date; not a regression introduced by this BA.
- BA-02's carried-forward recommendation (a dedicated `TenantMiddleware` prefix test) remains outstanding — not actioned in BA-04 either, per this BA's "only introduce changes strictly required" scope instruction; re-carried forward below.

### Architecture Compliance

- **ARCH-000:** No architecture redefinition; implementation only.
- **IMP-001:** Full Business Activity Lifecycle followed (§6.3) — precondition check (existence) → Business Object Update → Domain Event (`ORGANIZATION_PROFILE_UPDATED`) → Audit Recording → Response. Business Activity named and contracted, not raw CRUD (§1.7).
- **ERG-001:** Unaffected — no EnterpriseNode/Relationship/View concept touched.
- **C-004 / ADR-004:** No new fields exposed; `OrganizationResponse` reused unchanged; the fields touched (`organization_name`, `organization_type`, `description`) are already within ADR-004's approved Profile subset.
- **URA-001:** Unaffected.
- **Approved ADRs:** ADR-003, ADR-004, ADR-005 — all still honored; none re-litigated. No new ADR raised — the `organization_code`/`status` exclusion documented above is an implementation-level Business Activity scope decision, not an architectural one.

### Implementation Status

✅ IMPLEMENTATION COMPLETE

### Independent Review

**Independent Review: Accepted — ACCEPTED** (2026-07-21, fresh-context subagent with no memory of the implementation session; ran the full backend test suite and `tsc --noEmit` independently, validated `organization-api.yaml` by parsing it, verified Pydantic's default `extra="ignore"` behavior with a live interpreter check rather than assuming it, and diffed every changed file itself rather than trusting this report's claims).

**Review Result: ACCEPTED**

**Test results actually observed:** Backend `pytest -q` (with `JWT_SECRET_KEY`/`JWT_ALGORITHM` set) → **77 passed, 0 failed**. Test-count delta verified via `grep -c "def test_"` against `git show HEAD:...` (pre-BA-04 state): `test_organization_service.py` 11→15 (+4), `test_organization_api.py` 24→33 (+9) — 13 new tests total, matching this report's claim exactly, with only additive `+` diff lines in both test files (no existing test deleted or weakened). Frontend `tsc --noEmit` → 0 errors. `organization-api.yaml` parses cleanly via `yaml.safe_load`.

**Findings:** `models/organization.py` has zero diff — no migration, no schema change, confirming the Database Impact claim. `BaseRepository.update()` fetches by id, returns `None` if missing, mutates via `setattr`, defers commit — mirrors `create()`'s existing shape. `OrganizationService.update_profile()` follows IMP-001 §6.3's lifecycle exactly: existence check → 404 (audit DENIED) or repository update → `session.flush()` → audit SUCCESS → `publish_event("ORGANIZATION_PROFILE_UPDATED", ...)` → response — matching BA-01's `establish()` precedent. **Code immutability verified, not assumed**: `UpdateOrganizationProfileRequest` has no `organization_code` field, and this codebase's Pydantic models default to `extra="ignore"` (no `model_config = {"extra": "forbid"}` found anywhere in `schemas/`) — confirmed live rather than inferred — so a submitted `organization_code` is silently dropped before reaching the service; `test_update_organization_does_not_accept_organization_code_change` genuinely proves this end-to-end. **Status immutability verified**: `status` appears nowhere in the request schema or the repository update dict; `test_update_profile_does_not_change_code_or_status` asserts it directly. Validation (`min_length=1` on required fields), 404 exception handling (no partial write, no silent no-op), and authorization (`require_platform_admin` reused unmodified, confirmed via zero diff on `dependencies.py`) all check out. Frontend `UpdateOrganizationForm.tsx` is a structural match to `EstablishOrganizationForm.tsx`, built from DS-001 primitives confirmed to predate this change; the `organization_code` field renders `disabled` and is never submitted; `useUpdateOrganization.ts` correctly distinguishes loading/success/not-found/network-error states; the Edit modal reuses the same `gridRefreshKey` refresh-on-success pattern as Create.

**Defects found:** None. Specifically checked for race conditions (not applicable — no unique constraint on the fields this BA touches), silent data corruption (the service's explicit field whitelist prevents it), wrong HTTP status codes (all six responses correct and tested), and authorization bypass (tested with a non-admin role → 403).

**Risks recorded (non-blocking):**
1. Code/status immutability rests entirely on `OrganizationService.update_profile()`'s explicit whitelist dict — `BaseRepository.update()` itself will `setattr` whatever keys it's given. Correct today (dumb repository, smart service, same design as `create()`), but the guarantee is only as strong as future developers' discipline if this method is ever refactored to pass `request.model_dump()` directly instead of an explicit dict.
2. No test asserts `updated_at` actually advances post-update. Not required by any governing document; a reasonable minor addition for a future BA.
3. No optimistic concurrency control (no version/`ETag` field) — acknowledged as a pre-existing, WP-01-wide gap, not introduced by this BA.
4. BA-02's carried-forward `TenantMiddleware` prefix test recommendation remains outstanding — correctly re-carried forward rather than silently dropped, for the third consecutive BA.

**Recommendations carried into BA-05:**
- Add the dedicated `TenantMiddleware` prefix test (recommended after BA-02 and BA-03, still outstanding).
- Consider a test asserting `updated_at` changes post-update.
- Continue the established pattern (thin service orchestration, explicit field whitelists for mutation, DS-001 primitive reuse) — it held up cleanly through BA-04.

### Certification

Certification Status: Pending (WP-level activity, performed only after WP-01 completes, per CLAUDE.md §19.7)

### Repository

Committed as `e7b77f9` — "feat(auth-service): WP-01 BA-04 - Update Organization Profile" (2026-07-21). Working tree clean at commit time; all three §19.7 completion-gate conditions satisfied.

---

## Business Activity: BA-05 — Reactivate Suspended Organization

**Renamed per the WP-01 Scope Reconciliation** (see below): originally recorded as "Activate Organization." PE-001-C004 (the canonical Capability Specification, read in full during the reconciliation) defines a *distinct* "Activate Organization" (ERB-C004-03/EX-C004-04 — completing an Organization's first-ever establishment) from what this Business Activity actually implements: reversibly restoring an already-established, currently-`SUSPENDED` Organization back to `ACTIVE` (ERB-C004-06/EX-C004-09, "Reactivate Suspended Organization"). This is a documentation-only rename — the `activate()` method, `POST /organizations/{organization_id}/activate` endpoint, `ORGANIZATION_ACTIVATED` Domain Event, and `ACTIVATE_ORGANIZATION` audit action name are all unchanged in the codebase; nothing below describing the actual implementation was rewritten.

**Date Completed:** 2026-07-21

### Governing Canonical Assets Reviewed

- `architecture/05-Implementation/IRA-001_WP-01_Organization_Management_Implementation_Readiness_Assessment.md` — §2.2 (row: "Activate Organization | Update (state transition) | Organization | `ORGANIZATION_ACTIVATED`"), §9 Phase 3 ("Activate/Suspend Business Activities per ADR-005's interim model... audit-record verification tests").
- `architecture/07-Decisions/ADR-005_Organization_Lifecycle_Interim_Model.md` — the interim `ACTIVE`/`SUSPENDED` status column, application-level transition logic, mandatory Domain Event + audit record per transition, explicit interim-marker self-documentation requirement.
- `architecture/02-Constitutional/SD-002_Universal_Business_Object_Rules.md` — SD-002-054 (the audit trail's seven questions: Who, What, Why, When, How, Using Which Evidence, Under Which Policy) and SD-002-051/052 (target metadata-driven, event-driven lifecycle — confirmed still not built, ADR-005's interim model remains the correct implementation).
- `architecture/03-Engineering/IMP-001_Implementation_Playbook.md` §6 (CBAIP) — Business Activity Lifecycle, mandatory BAC components, Activity Types table (this BA is type "Update" / state transition).
- ADR-003, ADR-004 — re-confirmed unaffected (ownership and schema scope untouched).
- Existing WP-01 source: `models/organization.py`, `repositories/organization_repository.py`, `repositories/base_repository.py`, `services/organization_service.py`, `routers/organization.py`, `middleware/tenant.py`, `observability.py` — reviewed to reuse established patterns.
- `architecture/06-Reviews/TECH-DEBT.md` — TD-001 (`TenantMiddleware` prefix test, Planned Resolution: BA-05) and TD-008 (trivial `SUSPENDED` filter tests, Planned Resolution: BA-05/BA-06) reviewed for items due in this Business Activity.

### Gap Analysis

- **Satisfied as-is (reused unchanged):** `Organization` model's existing `status` column (no migration needed — BA-01 already added it); `require_platform_admin`; `OrganizationResponse`; `middleware/tenant.py`'s `/organizations/*` prefix exemption (already covers a new sub-path with zero changes — path-prefix, method-agnostic); `observability.py`'s `record_audit`/`publish_event`; `BaseRepository.update()` (added in BA-04, reused here verbatim — no repository change required for BA-05 at all); the establish/update_profile method shape as the template for `activate()`.
- **Required extension:** `OrganizationService` needed a new `activate()` orchestration method; `routers/organization.py` needed a new `POST /{organization_id}/activate` route. No repository, model, or schema change was required — the entire Business Activity is additive at the service and router layers only.
- **Missing architecture:** None. No new entity, table, column, service boundary, or permission tier.
- **Business rule judgment call (documented for review scrutiny, no ADR raised — implementation-level, same category as BA-04's code-immutability decision):** ADR-005 defines the `ACTIVE`/`SUSPENDED` state pair but does not specify what happens when Activate is called on an organization that is already `ACTIVE`. Two options existed: (a) silently no-op and return 200, or (b) reject as an invalid transition. **Decision: reject with 409** ("Organization is already ACTIVE"), mirroring `establish()`'s existing precedent of using 409 for "this business rule doesn't apply given current state" rather than a silent success. Rationale: an explicit state machine with deterministic, fail-fast transitions (CLAUDE.md §10) is more defensible for a governed lifecycle than an implicit idempotent-success convention with no canonical basis; this also gives BA-06 Suspend a consistent precedent to follow (reject "already SUSPENDED" the same way).
- **Scope boundary (backend-only, per this task's explicit instruction):** this Business Activity's requested scope enumerated backend/API/domain/service/repository/validation/authorization/audit/event/test/documentation items and did not include frontend work (unlike BA-01 through BA-04's requests, which explicitly asked for a UI vertical slice). IRA-001 §5's UI Impact Matrix names "Action Center" as the pattern for Activate/Suspend but explicitly flags it as "named, not yet built" — inventing it now, for Activate alone, ahead of Suspend (BA-06) needing the same pattern, risked exactly the kind of premature/unspecified component creation CLAUDE.md §19.1 prohibits ("Claude Code SHALL NEVER invent a component... If DS-001 does not define something a feature requires, Claude Code SHALL STOP"). No frontend files were created or modified by this Business Activity; the backend endpoint is fully usable via direct API calls today and is ready for a future Action Center-based UI once that component is built (naturally alongside BA-06, when both Activate and Suspend actions are needed together).
- **Technical debt closed:** TD-001 (dedicated `TenantMiddleware` prefix test) had "Planned Resolution: BA-05" already recorded in the register — resolved in this Business Activity (`tests/test_tenant_middleware.py`) rather than left to go stale a fourth time.
- **Technical debt introduced:** TD-012 — `Organization.is_active` (a WP-00 legacy boolean, never referenced by any business logic) is not touched by `activate()`; once BA-06 Suspend sets `status="SUSPENDED"`, `is_active` will keep reading `True`, a genuine (not hypothetical) two-column lifecycle inconsistency. Recorded in the Technical Debt Register with Planned Resolution: BA-06.

### Scope Delivered

`POST /organizations/{organization_id}/activate` — Activate Organization. Transitions an organization's `status` from `SUSPENDED` to `ACTIVE`; 404 if the id doesn't exist; 409 if already `ACTIVE`. Reuses BA-01–04's model, `require_platform_admin` authorization, `OrganizationResponse`, `BaseRepository.update()`, and `TenantMiddleware` exemption unchanged. No database migration, no new authorization tier, no new DS-001 component. Also closes out TD-001 (dedicated `TenantMiddleware` prefix test). No ADR required (see Gap Analysis for the one business-rule judgment call made and its rationale).

### Files Created

| File | Purpose |
|---|---|
| `Backend/Services/AuthService/tests/test_tenant_middleware.py` | Dedicated `TenantMiddleware` prefix-exemption tests (closes TD-001) |

### Files Modified

| File | Summary of Changes |
|---|---|
| `Backend/Services/AuthService/services/organization_service.py` | Added `OrganizationService.activate()`; updated module docstring |
| `Backend/Services/AuthService/routers/organization.py` | Added `POST /{organization_id}/activate` |
| `Backend/Services/AuthService/organization-api.yaml` | Added the `POST /organizations/{organization_id}/activate` path |
| `Backend/Services/AuthService/tests/test_organization_service.py` | Added BA-05 unit tests |
| `Backend/Services/AuthService/tests/test_organization_api.py` | Added BA-05 integration tests; added `Organization`/`AsyncSession` imports for direct DB seeding of a `SUSPENDED` starting state |
| `Backend/Services/AuthService/README.md` | Updated Organization Management section for BA-05 |
| `architecture/06-Reviews/TECH-DEBT.md` | Closed TD-001; added TD-012; updated TD-007's Planned Resolution to reflect BA-05's backend-only scope |

### Database

- **Migration(s):** None — `status` already exists on `organizations` from BA-01.
- **Schema changes / Constraints / Indexes:** None.

### APIs

- **Endpoint added:** `POST /organizations/{organization_id}/activate` (200/400/401/403/404/409/422).
- **Request/Response models:** No request body (the path parameter is the entire Input Contract, consistent with IMP-001 §6.4 — a minimal but legitimate contract, same basis as GET `/{organization_id}`) → existing `OrganizationResponse` (no new response schema).
- **Authorization:** Same `require_platform_admin` dependency as BA-01–04 — no new tier.
- **OpenAPI:** `organization-api.yaml` updated with the new path; YAML-validated.

### Frontend

Not in scope for this Business Activity (see Gap Analysis's "Scope boundary" note above). No frontend files created or modified.

### Testing

- **Unit Tests:** 4 new (`test_organization_service.py`, 19 total in that file) — SUSPENDED→ACTIVE transition; reject already-ACTIVE (409); 404 on unknown id; profile fields (name/type/description/code) unchanged after activation.
- **Integration Tests:** 7 new (`test_organization_api.py`, 40 total in that file) — success (seeding SUSPENDED directly via the shared `db_session` fixture, since no Suspend Business Activity exists yet to produce one through the API — same precedent as `test_health.py`'s `test_ready_reports_ready_after_bootstrap`, which already mixes `client`+`db_session`), reject-already-ACTIVE (409), 404, missing/wrong-role auth (400/403), invalid UUID (422), tenant-header exemption.
- **Dedicated Middleware Tests:** 2 new (`test_tenant_middleware.py`) — the `/organizations/*` prefix exemption asserted directly (including the new `/activate` sub-path) rather than only incidentally; a boundary test proving the prefix match doesn't over-match a similar-looking path (`/organizationsfoo` still requires `X-Tenant-ID`).
- **API Tests:** covered by the integration suite above.
- **UI Tests:** N/A — no frontend work in this Business Activity.
- **Overall test results:** 90/90 backend tests passing (13 new this BA — 4 unit, 7 integration, 2 middleware — 0 regressions). Verified by running the full suite twice (once immediately after implementation, once again in this report's testing pass).

### Manual Verification

1. Using a `PLATFORM_ADMIN` access token, create an organization via `POST /organizations` (defaults to `ACTIVE`).
2. Directly set its `status` to `SUSPENDED` (no Suspend endpoint exists yet — this step is a stand-in for BA-06).
3. `POST /organizations/{id}/activate` → expect `200` with `status: "ACTIVE"`.
4. Repeat the same call → expect `409` ("already ACTIVE").
5. `POST /organizations/{random-uuid}/activate` → expect `404`.
6. Repeat without `Authorization` → `400`; with a non-`PLATFORM_ADMIN` token → `403`; with a malformed id → `422`.
7. `GET /organizations/{id}/activate` (wrong method, no `X-Tenant-ID`) → confirm the response body has a `detail` key (reached the app) rather than the middleware's `message` key — proving tenant exemption directly.

### Known Limitations (intentionally deferred, per WP-01 scope)

- Same authorization/lifecycle/schema-scope/RLS/frontend-test-harness limitations as BA-01–04 (unchanged — see BA-01 section above); none are specific to BA-05.
- No frontend Activate action exists yet (see Gap Analysis's scope-boundary note) — deferred to land alongside BA-06 Suspend, when the Action Center UI pattern is built once for both actions rather than twice.
- `Organization.is_active` is not synchronized with `status` by this Business Activity (TD-012, tracked in the register) — a real, not hypothetical, inconsistency that becomes externally observable once BA-06 Suspend exists.
- No automated test asserts the audit record's payload literally answers all seven SD-002-054 questions (Who/What/Why/When/How/Evidence/Policy) — `record_audit()` is called with the same field mapping as BA-01/BA-04 (established, not newly invented, in this BA), and this gap is pre-existing across WP-00's bootstrap tests and every WP-01 Business Activity to date, not introduced or newly discovered by BA-05.

### Architecture Compliance

- **ARCH-000:** No architecture redefinition; implementation only.
- **IMP-001:** Full Business Activity Lifecycle followed (§6.3) — precondition checks (existence, current status) → Business Object Update → Domain Event (`ORGANIZATION_ACTIVATED`) → Audit Recording → Response. Business Activity named and contracted as a state transition (§6.6's "Update" type), not raw CRUD (§1.7).
- **ERG-001:** Unaffected — no EnterpriseNode/Relationship/View concept touched.
- **C-004 / ADR-004:** No new fields exposed; `OrganizationResponse` reused unchanged.
- **ADR-005:** Implemented exactly as recorded — interim `status` column, application-level transition logic, mandatory Domain Event + audit per transition, explicit interim-model docstring reference in `activate()`.
- **URA-001:** Unaffected.
- **Approved ADRs:** ADR-003, ADR-004, ADR-005 — all still honored; none re-litigated. No new ADR raised — the already-ACTIVE→409 rule is an implementation-level Business Activity decision, not an architectural one.

### Implementation Status

✅ IMPLEMENTATION COMPLETE

### Developer Validation

Performed by the implementation agent against this Business Activity's own acceptance criteria (IMP-001 §6.4/§6.7, ADR-005, IRA-001 §2.2/§9). This is **self-certification, not Independent Review** — CLAUDE.md §19.7's Business Activity Completion Gate still requires a separate, independently-run review (as performed for BA-01 through BA-04 by a fresh-context subagent) before this Business Activity is considered fully complete; that review has not yet been requested for BA-05.

| Acceptance Criterion | Status | Evidence |
|---|---|---|
| Business Intent defined | ✅ Met | Activate Organization: `SUSPENDED` → `ACTIVE` transition |
| Input Contract | ✅ Met | `organization_id` path parameter (UUID, FastAPI-validated) |
| Output Contract | ✅ Met | `OrganizationResponse`, reused unchanged |
| Business Rules enforced | ✅ Met | Existence required (404); already-`ACTIVE` rejected (409) |
| Validation Rules | ✅ Met | Invalid UUID → 422 (`test_activate_organization_rejects_invalid_uuid`) |
| Authorization Rules | ✅ Met | `require_platform_admin` reused unmodified; 400/403 tested |
| Domain Events | ✅ Met | `ORGANIZATION_ACTIVATED` published via `publish_event()` |
| Audit Requirements | ✅ Met | `record_audit()` SUCCESS/DENIED, same field mapping as BA-01/BA-04 |
| Error Handling | ✅ Met | 404/409/422/400/403 all explicit, no silent no-ops, no 500s |
| No architecture change | ✅ Met | Zero diff on `models/organization.py`, no new migration, no new entity/permission tier |
| Reuse over creation | ✅ Met | `BaseRepository.update()`, `OrganizationResponse`, `require_platform_admin`, `observability.py` all reused verbatim; only `activate()` (service) and one router function are new |
| Tests (unit/integration/regression) | ✅ Met | 90/90 passing, 13 new, 0 regressions |
| Documentation updated | ✅ Met | IMP-REPORT-WP-01 (this section), README.md, `organization-api.yaml` |
| Technical debt recorded | ✅ Met | TD-012 added; TD-001 closed; TD-007 updated for accuracy |

**Self-certification outcome: PASS.** All acceptance criteria met by the implementation agent's own assessment. Recommending this Business Activity for Independent Review.

### Independent Review

**Independent Review: Accepted — ACCEPTED WITH OBSERVATIONS** (2026-07-21, fresh-context subagent with no memory of the implementation session; ran the full backend test suite independently, diffed the actual commit `467d847` itself rather than trusting this report's claims, and cross-checked the Technical Debt Register against the code it describes).

**Review Result: ACCEPTED WITH OBSERVATIONS**

**Test results actually observed:** `pytest -q` (with `JWT_SECRET_KEY`/`JWT_ALGORITHM` set) → **90 passed, 0 failed**, 54.28s. Test-count deltas verified against the pre-BA-05 commit (`467d847^`): `test_organization_service.py` 15→19 (+4), `test_organization_api.py` 33→40 (+7), new `test_tenant_middleware.py` (+2) — 13 new tests total, matching this report's claim exactly, with all diffs to existing test files additive-only.

**Findings:** `git show 467d847 --stat` confirms the diff touches exactly the 9 files this report's Files Created/Modified tables list, with zero frontend files — corroborating the backend-only scope claim. `models/organization.py`, `dependencies.py`, `repositories/organization_repository.py`, and `schemas/organization.py` all show empty diffs in this commit — no architecture, authorization, or repository-layer change. `activate()`'s lifecycle sequence was traced directly: existence check (404) → already-ACTIVE check (409, verified to run strictly before any mutating call) → `BaseRepository.update()` (reused verbatim, no new repository method) → `session.flush()` → `record_audit(SUCCESS)` → `publish_event("ORGANIZATION_ACTIVATED", ...)` → response. Audit fires on both DENIED paths (not-found, already-active) and the SUCCESS path with a metadata shape consistent with BA-01/BA-04. `test_tenant_middleware.py` was read in full and confirmed to genuinely exercise `middleware/tenant.py`'s actual prefix-match logic (not incidentally) — a regression to an exact-match list, or a broader/narrower prefix, would flip its assertions. The SUSPENDED-seeding techniques in both the unit tests (direct repository manipulation) and the integration test (the shared `db_session` fixture, verified sound against `conftest.py`'s dependency-override wiring) genuinely exercise the transition under test, not a shortcut around it. **Technical Debt Register verified line-by-line**: TD-001's `Status`/`Planned Resolution` correctly show `Closed`/resolved-by-`test_tenant_middleware.py`, and that file genuinely satisfies TD-001's original description. TD-012 is a new, distinct entry (not a duplicate of TD-004 or TD-011) with all columns filled consistently; its premise was independently confirmed — `grep is_active` in `organization_service.py` returns zero matches. TD-007's `Planned Resolution` was reasonably updated to reflect BA-05's confirmed backend-only scope.

**Defects found:** None that block acceptance.

**Risks recorded (non-blocking):**
1. A concurrent-activation race (read-then-write on `status` with no row lock) exists in `activate()`, but this is the same class of risk already tracked as TD-003 (optimistic concurrency, open, Medium priority, WP-02) and is not a new or BA-05-specific regression — `establish()` and `update_profile()` already carry the same characteristic. No new tech-debt entry needed.
2. TD-012 is real but currently latent — it becomes externally observable once BA-06 Suspend lands; correctly scoped to Medium priority.

**Observations (non-blocking):**
1. The dashboard's "Tests added: 61 (19 unit, 40 integration, 2 dedicated middleware)" line reads ambiguously as if 61 tests were added in BA-05, when 19/40/2 are running totals in those files (the actual BA-05 delta, 4/7/2=13, is correctly stated in this section). Clarified below.
2. `record_audit()` is called before `publish_event()` in `activate()` (and in `establish()`/`update_profile()` before it), while IMP-001 §6.3 literally states the order as Business Object Update → Domain Event Publication → Audit Recording. This is inherited unchanged from already-accepted BA-01/BA-04 precedent, not introduced by BA-05, so it is not chargeable to this Business Activity — but the systemic divergence from the documented order is worth a single reconciling decision (amend IMP-001 to reflect the implemented order, or change the code) rather than continuing to carry it forward silently.

**Recommendations carried forward:**
- Resolve TD-012 when BA-06 Suspend is implemented, before further lifecycle transitions compound the `is_active`/`status` divergence.
- Reconcile the audit-before-event ordering across all Business Activities against IMP-001 §6.3's literal text (single decision, not urgent).

### Certification

Certification Status: Pending (WP-level activity, performed only after WP-01 completes, per CLAUDE.md §19.7)

---

## Business Activity: BA-06 — Suspend Organization

**Date Completed:** 2026-07-21

### Governing Canonical Assets Reviewed

- `architecture/05-Implementation/IRA-001_WP-01_Organization_Management_Implementation_Readiness_Assessment.md` — §2.2 (row: "Suspend Organization | Update (state transition) | Organization | `ORGANIZATION_SUSPENDED`"), §9 Phase 3 (Activate/Suspend Business Activities per ADR-005's interim model).
- `architecture/07-Decisions/ADR-005_Organization_Lifecycle_Interim_Model.md` — same interim `ACTIVE`/`SUSPENDED` model BA-05 implemented; Suspend is the model's other transition.
- `architecture/02-Constitutional/SD-002_Universal_Business_Object_Rules.md` — SD-002-054 (seven audit questions), reused via the same `observability.py` mechanism as every prior WP-01 Business Activity.
- `architecture/03-Engineering/IMP-001_Implementation_Playbook.md` §6 (CBAIP) — Business Activity Lifecycle, mandatory BAC components.
- ADR-003, ADR-004 — re-confirmed unaffected.
- Existing WP-01 source: `services/organization_service.py`'s `activate()` (BA-05, the direct precedent this Business Activity mirrors in the opposite direction), `routers/organization.py`, `repositories/base_repository.py`'s `update()` (BA-04), `middleware/tenant.py`.
- `architecture/06-Reviews/TECH-DEBT.md` — reviewed for items planned for BA-06: **TD-008** (Search/List's trivial `SUSPENDED`-filter tests, Planned Resolution: BA-05/BA-06) and **TD-012** (`Organization.is_active`/`status` divergence, Planned Resolution: BA-06).

### Gap Analysis

- **Satisfied as-is (reused unchanged):** `Organization` model's existing `status`/`is_active` columns (no migration); `require_platform_admin`; `OrganizationResponse`; `middleware/tenant.py`'s `/organizations/*` prefix exemption (already covers the new sub-path with zero changes); `observability.py`'s `record_audit`/`publish_event`; `BaseRepository.update()` (no repository change required); `activate()`'s method shape as the direct template for `suspend()` (same structure, reversed direction).
- **Required extension:** `OrganizationService` needed a new `suspend()` orchestration method; `routers/organization.py` needed a new `POST /{organization_id}/suspend` route. No repository, model, or schema change required.
- **Missing architecture:** None. No new entity, table, column, service boundary, or permission tier.
- **Business rule (already precedented by BA-05, not re-litigated):** suspending an already-`SUSPENDED` organization returns 409, mirroring `activate()`'s already-`ACTIVE`→409 rule exactly — BA-05's report explicitly named this as "a consistent precedent for BA-06 Suspend," so this is confirmation of an existing decision, not a new judgment call requiring fresh documentation.
- **Technical debt planned for this BA, resolved:**
  - **TD-008**: with `suspend()` now real, a true positive/negative status-filter test was added at both the service layer (`test_search_status_filter_correctly_includes_and_excludes_mixed_statuses`) and the API layer (`test_search_organizations_status_filter_includes_and_excludes_mixed_statuses`), proving the `ACTIVE`/`SUSPENDED` filter correctly includes and excludes against a real mixed-status dataset — previously only the trivial "SUSPENDED returns empty" case was provable. Closed.
  - **TD-012**: resolved by having both `activate()` and `suspend()` write `is_active` alongside `status` in the same repository call (`is_active: True` on activate, `is_active: False` on suspend) — `BaseRepository.update()` (generic, unchanged) accepts the extra key with no repository modification needed. Verified with a dedicated round-trip test at both layers (`test_suspend_and_activate_keep_is_active_in_sync_with_status`, `test_suspend_then_activate_round_trip_keeps_is_active_in_sync`). Closed. Note: `activate()`'s BA-05 code was touched to add `"is_active": True` to its existing `update()` call — a one-line addition to already-committed code, made under this Business Activity's explicit license to resolve TD-012 (which named `activate()`/`suspend()` symmetry as the fix), not a re-opening of BA-05's accepted scope.
- **Technical debt introduced:** None identified. The same concurrent-transition race already tracked as TD-003 (optimistic concurrency) applies symmetrically to `suspend()`, but this is the same pre-existing risk class already covered by that entry, not a new one.
- **Scope boundary (backend-only, consistent with BA-05):** no frontend files created or modified — same rationale as BA-05 (Action Center is a named-but-unbuilt DS-001 component; building it now for Suspend alone, without Activate's UI either, would still be premature. Both actions remain candidates for a single future Action Center UI pass).

### Scope Delivered

`POST /organizations/{organization_id}/suspend` — Suspend Organization. Transitions `status` from `ACTIVE` to `SUSPENDED` (and syncs `is_active` to `False`); 404 if the id doesn't exist; 409 if already `SUSPENDED`. Reuses BA-01–05's model, `require_platform_admin`, `OrganizationResponse`, `BaseRepository.update()`, and `TenantMiddleware` exemption unchanged. Also closes TD-008 and TD-012. No database migration, no new authorization tier, no new DS-001 component, no ADR required.

### Files Created

None — this Business Activity is additive at the service, router, and test layers only.

### Files Modified

| File | Summary of Changes |
|---|---|
| `Backend/Services/AuthService/services/organization_service.py` | Added `OrganizationService.suspend()`; added `"is_active": True` to `activate()`'s existing `update()` call (TD-012 resolution); updated module docstring |
| `Backend/Services/AuthService/routers/organization.py` | Added `POST /{organization_id}/suspend` |
| `Backend/Services/AuthService/organization-api.yaml` | Added the `POST /organizations/{organization_id}/suspend` path |
| `Backend/Services/AuthService/tests/test_organization_service.py` | Added BA-06 unit tests; added a TD-008 mixed-status search test |
| `Backend/Services/AuthService/tests/test_organization_api.py` | Added BA-06 integration tests; added a TD-008 mixed-status search test |
| `Backend/Services/AuthService/README.md` | Updated Organization Management section for BA-06 |
| `architecture/06-Reviews/TECH-DEBT.md` | Closed TD-008 and TD-012 with resolution notes |

### Database

- **Migration(s):** None — `status` and `is_active` already exist on `organizations`.
- **Schema changes / Constraints / Indexes:** None.

### APIs

- **Endpoint added:** `POST /organizations/{organization_id}/suspend` (200/400/401/403/404/409/422).
- **Request/Response models:** No request body (path parameter only, same basis as `/activate`) → existing `OrganizationResponse` (no new response schema).
- **Authorization:** Same `require_platform_admin` dependency as BA-01–05 — no new tier.
- **OpenAPI:** `organization-api.yaml` updated with the new path; YAML-validated.

### Frontend

Not in scope for this Business Activity (see Gap Analysis's "Scope boundary" note above). No frontend files created or modified.

### Testing

- **Unit Tests:** 6 new (`test_organization_service.py`, 25 total in that file) — ACTIVE→SUSPENDED transition; reject already-SUSPENDED (409); 404 on unknown id; profile fields unchanged; `is_active`/`status` sync round-trip; TD-008's mixed-status filter proof.
- **Integration Tests:** 9 new (`test_organization_api.py`, 49 total in that file) — success, reject-already-SUSPENDED (409), 404, missing/wrong-role auth (400/403), invalid UUID (422), tenant-header exemption, `is_active` sync round-trip through the HTTP API, TD-008's mixed-status filter proof through the HTTP API.
- **API Tests:** covered by the integration suite above.
- **UI Tests:** N/A — no frontend work in this Business Activity.
- **Overall test results:** 105/105 backend tests passing (15 new this BA — 6 unit, 9 integration — 0 regressions). Full suite run twice (immediately after implementation and again before this report update).

### Manual Verification

1. Using a `PLATFORM_ADMIN` access token, create an organization via `POST /organizations` (defaults to `ACTIVE`, `is_active: true`).
2. `POST /organizations/{id}/suspend` → expect `200` with `status: "SUSPENDED"`, `is_active: false`.
3. Repeat the same call → expect `409` ("already SUSPENDED").
4. `POST /organizations/{id}/activate` on the now-suspended organization → expect `200` with `status: "ACTIVE"`, `is_active: true` again.
5. `POST /organizations/{random-uuid}/suspend` → expect `404`.
6. Repeat without `Authorization` → `400`; with a non-`PLATFORM_ADMIN` token → `403`; with a malformed id → `422`.
7. `GET /organizations?status=SUSPENDED` and `GET /organizations?status=ACTIVE` against a mixed dataset → confirm each filter returns exactly the organizations in that state.

### Known Limitations (intentionally deferred, per WP-01 scope)

- Same authorization/lifecycle/schema-scope/RLS/frontend-test-harness limitations as BA-01–05 (unchanged — see BA-01 section above); none are specific to BA-06.
- No frontend Suspend action exists yet (see Gap Analysis's scope-boundary note) — deferred alongside BA-05's Activate action to a future Action Center UI pass covering both.
- No business rule prevents suspending an organization with active Memberships (e.g., cascading a suspension to member access) — this is explicitly out of WP-01's scope per IRA-001 (Membership/Role & Permission Management are separate work packages); not a gap in this Business Activity, a scope boundary already recorded at the WP level.

### Architecture Compliance

- **ARCH-000:** No architecture redefinition; implementation only.
- **IMP-001:** Full Business Activity Lifecycle followed (§6.3) — precondition checks (existence, current status) → Business Object Update → Domain Event (`ORGANIZATION_SUSPENDED`) → Audit Recording → Response. Business Activity named and contracted as a state transition (§6.6's "Update" type), not raw CRUD.
- **ERG-001:** Unaffected — no EnterpriseNode/Relationship/View concept touched.
- **C-004 / ADR-004:** No new fields exposed; `OrganizationResponse` reused unchanged.
- **ADR-005:** Implemented exactly as recorded — interim `status` column, application-level transition logic, mandatory Domain Event + audit per transition.
- **URA-001:** Unaffected.
- **Approved ADRs:** ADR-003, ADR-004, ADR-005 — all still honored; none re-litigated. No new ADR raised.

### Implementation Status

✅ IMPLEMENTATION COMPLETE

### Developer Validation

Performed by the implementing engineer against this Business Activity's own acceptance criteria (IMP-001 §6.4/§6.7, ADR-005, IRA-001 §2.2/§9), mirroring BA-05's Developer Validation checklist.

| Acceptance Criterion | Status | Evidence |
|---|---|---|
| Business Intent defined | ✅ Met | Suspend Organization: `ACTIVE` → `SUSPENDED` transition |
| Input Contract | ✅ Met | `organization_id` path parameter (UUID, FastAPI-validated) |
| Output Contract | ✅ Met | `OrganizationResponse`, reused unchanged |
| Business Rules enforced | ✅ Met | Existence required (404); already-`SUSPENDED` rejected (409) |
| Validation Rules | ✅ Met | Invalid UUID → 422 (`test_suspend_organization_rejects_invalid_uuid`) |
| Authorization Rules | ✅ Met | `require_platform_admin` reused unmodified; 400/403 tested |
| Domain Events | ✅ Met | `ORGANIZATION_SUSPENDED` published via `publish_event()` |
| Audit Requirements | ✅ Met | `record_audit()` SUCCESS/DENIED, same field mapping as BA-05 |
| Error Handling | ✅ Met | 404/409/422/400/403 all explicit, no silent no-ops, no 500s |
| No architecture change | ✅ Met | Zero diff on `models/organization.py`, no new migration, no new entity/permission tier |
| Reuse over creation | ✅ Met | `BaseRepository.update()`, `OrganizationResponse`, `require_platform_admin`, `observability.py`, and `activate()`'s method shape all reused; only `suspend()` (service) and one router function are new |
| Tests (unit/integration/regression) | ✅ Met | 105/105 passing, 15 new, 0 regressions |
| Documentation updated | ✅ Met | IMP-REPORT-WP-01 (this section), README.md, `organization-api.yaml` |
| Technical debt resolved/recorded | ✅ Met | TD-008 closed; TD-012 closed; no new debt introduced |

**Developer Validation outcome: PASS.** All acceptance criteria met by the implementing engineer's own assessment. This is developer validation, not Independent Review — CLAUDE.md §19.7's Business Activity Completion Gate still requires a separate, independently-run review before this Business Activity is considered fully complete; that review has not yet been requested for BA-06.

### Independent Review

**Independent Review: Accepted — ACCEPTED WITH OBSERVATIONS** (2026-07-21, fresh-context subagent with no memory of the implementation session; ran the full backend test suite independently, diffed the actual working tree itself rather than trusting this report's claims, and cross-checked the Technical Debt Register against the code and tests it describes).

**Review Result: ACCEPTED WITH OBSERVATIONS**

**Test results actually observed:** `pytest -q` (with `JWT_SECRET_KEY`/`JWT_ALGORITHM` set) → **105 passed, 0 failed**, 12.45s. Test-count deltas verified against the last committed state (`HEAD`): `test_organization_service.py` 19→25 (+6), `test_organization_api.py` 40→49 (+9) — 15 new tests total, matching this report's claim exactly, with all test-file diffs additive-only.

**Findings:** `git status`/`git diff` confirm the working tree touches exactly the files this report's Files Modified table lists (plus the pre-existing, unrelated `CLAUDE.md` change). Zero diff on `models/organization.py`, `dependencies.py`, `repositories/organization_repository.py`, `schemas/organization.py`, `middleware/tenant.py`, and all of `source/frontend/`. `suspend()` and `activate()` were read side by side and confirmed structurally and behaviorally symmetric: `get_by_id()` → 404 if missing (audit DENIED) → target-state check → 409 if already in that state (audit DENIED, confirmed to run strictly before any mutating call) → `BaseRepository.update()` with both `status` and `is_active` → `session.flush()` → `record_audit(SUCCESS)` → `publish_event(...)` → response. The modification to already-accepted `activate()` code was verified narrow and legitimate: `git diff` shows only a docstring addition and one dict key (`"is_active": True`) — its 404/409 logic, audit metadata, and event payload are byte-for-byte unchanged from BA-05's accepted version. `organization-api.yaml` parses cleanly and lists the new `/suspend` path with matching response codes. All 15 new tests were read in full and genuinely exercise what they claim — including the TD-008 mixed-status filter tests (real `suspend()` call seeding a genuine mixed dataset, asserting true inclusion and exclusion, not just "returns empty") and the TD-012 `is_active`/`status` round-trip tests at both service and API layers.

**Defects found:** None that block acceptance.

**Technical Debt Register verified:** TD-008 `Closed` with a resolution note naming the actual test functions — both exist and pass. TD-012 `Closed` with a resolution note describing the `is_active` sync — the code genuinely performs it (verified in the diff, not just claimed). TD-003 (optimistic concurrency) correctly remains `Open`, unmodified, not duplicated — the same TOCTOU race in `suspend()` is the same risk class already tracked there, not a new entry needed. No duplicate entries introduced.

**Risks recorded (non-blocking):**
1. The audit-before-event ordering discrepancy against IMP-001 §6.3's literal text is inherited from BA-01/BA-04/BA-05, not introduced or fixed by BA-06 — now spans 4+ Business Activities and is growing in surface area with each additional one that copies the pattern.
2. The Action Center UI deferral reasoning (from BA-05) is weaker now that both Activate and Suspend exist — the original "only half the actions exist" justification no longer fully holds, though deferring is still defensible this review (no regression, no architecture invented). Should not be indefinitely re-deferred.
3. `suspend()`/`activate()`'s copy-paste-with-reversal duplication is acceptable at two transitions; a shared `_transition()` helper is a reasonable candidate only if a third lifecycle transition is ever added — not required now.

**Recommendations carried forward:**
- Schedule a single reconciling decision for the audit/event ordering discrepancy (amend IMP-001 §6.3 or reorder the code) before WP-01 closure.
- Schedule the Action Center UI (covering both Activate and Suspend) explicitly before WP-01 closure rather than continuing to implicitly re-defer it BA-by-BA.
- Consider extracting a shared `_transition()` helper only if/when a third lifecycle transition is introduced.

### Certification

Certification Status: Pending (WP-level activity, performed only after WP-01 completes, per CLAUDE.md §19.7)

### Repository

Committed as `a264b86` — "feat(auth-service): WP-01 BA-06 - Suspend Organization" (2026-07-21). This Independent Review outcome recorded in a separate documentation commit per §19.7's completion-gate repository condition.

---

## WP-01 Scope Reconciliation

**Date:** 2026-07-21
**Trigger:** Before starting the originally-planned BA-07 (Configure Organization), a governing-canonical-asset review (CLAUDE.md §19.1) surfaced that `PE-001-C004_Organization_Management.docx` — the authoritative Capability Experience Specification for C-004 — had never actually been read; IRA-001 had logged it as unreadable (`.docx`-only) and flagged the gap as Risk #4 (Major, Open). It was extracted directly from the archive (a `.docx` is a zip container) and read in full before any further implementation proceeded.

**Findings:**

- `PE-001-C004` (Gold Standard, v1.1) became the authoritative capability specification for C-004 once read, superseding IRA-001 §2.2's originally-drafted Business Activity list wherever they conflict, per CLAUDE.md §16.
- IRA-001 originally contained 8 planned Business Activities, several self-labeled "proposed here for planning purposes only" — explicitly provisional, not themselves a canonical source.
- **Configure Organization** and **Audit History** were removed: no ERB, EX, or scope clause anywhere in `PE-001-C004` defines either (confirmed by full-text search of the extracted spec). ADR-004 had already, independently, deferred every configuration-flavored canonical field to future work packages pending a real consumer; Audit History's underlying concern is already satisfied cross-cuttingly by `observability.py`'s `record_audit()` calls across every implemented Business Activity (SD-002-054 / C-114 — a platform-wide concern, not a distinct C-004 Enterprise Experience).
- **ERB-C004-07 (Retire Organization & Preserve Continuity)** replaces the two removed Business Activities as the corrected **BA-07** — a real canonical ERB (with its own terminal `RETIRED` lifecycle state) that had no Business Activity anywhere in the original plan.
- BA-05 was renamed **Reactivate Suspended Organization** (from "Activate Organization") to disambiguate it from PE-001-C004's distinct, different "Activate Organization" (ERB-C004-03/EX-C004-04, first-time establishment completion) — see the note at the top of BA-05's section, above. BA-01, BA-02, and BA-04 were similarly aligned to canonical ERB terminology in the dashboard and in IRA-001 (Establish Organization Identity / Resolve Organization Details / Steward Organization Identity) without any change to implemented behavior, APIs, or Domain Event names.

**Resolution:**

- **No architecture changed.** No entity, table, column, service boundary, or permission tier was added, removed, or redefined.
- **No implementation was discarded.** BA-01 through BA-06 are unchanged in the codebase — same models, repositories, services, routers, endpoints, event names, and tests as already independently reviewed and committed. Only Business Activity names and canonical cross-references in planning/report documents were corrected.
- **No ADR was required.** This was IRA-001's own self-flagged provisional content being superseded by the canonical Capability Specification once read — exactly the outcome IRA-001's own Risk #4 anticipated — not a genuine conflict between two canonical authorities requiring a governance tradeoff decision.
- WP-01's total Business Activity count is corrected from 8 to **7**; 6 are complete, **1 remains: BA-07 Retire Organization & Preserve Continuity**.

**Cross-reference:** `architecture/05-Implementation/IRA-001_WP-01_Organization_Management_Implementation_Readiness_Assessment.md` §15 records the same reconciliation from the readiness-assessment side, including the full Business Activity → canonical ERB mapping.

---

## Business Activity: BA-07 — Retire Organization & Preserve Continuity

**Date Completed:** 2026-07-21
**This is the final Business Activity of WP-01**, per the WP-01 Scope Reconciliation (above).

### Governing Canonical Assets Reviewed

- `docs/Product/PE-001/capabilities/C-004/PE-001-C004_Organization_Management.docx` — read in full during the WP-01 Scope Reconciliation. §3.8 (ERB-C004-07 "Retire Organization & Preserve Continuity"): Entry Context ("Authoritative Organization Context in ACTIVE or SUSPENDED state, with a stated retirement intent"), Exit Context (RETIRED, terminal, optionally with a successor link), Context Engineering (Preserved: "The full Authoritative Organization Context and its identity history, permanently, in RETIRED state"; Invalidated: "The Organization's validity for any new dependent activity... retirement itself is never invalidated or reversed"). §4.9–4.12 (EX-C004-10 through -13). The lifecycle-state paragraph ("Once activated, an Organization SHALL exist in exactly one of ACTIVE, SUSPENDED, or RETIRED state... RETIRED SHALL NOT be reversible to any other state under any circumstance").
- `architecture/05-Implementation/IRA-001_WP-01_Organization_Management_Implementation_Readiness_Assessment.md` §2.2 (revised, per §15) and §15 (the Scope Reconciliation itself).
- `architecture/07-Decisions/ADR-005_Organization_Lifecycle_Interim_Model.md` — the interim `status` column model this Business Activity extends with a third value, not replaces.
- ADR-003, ADR-004 — re-confirmed unaffected.
- Existing WP-01 source: `services/organization_service.py`'s `activate()`/`suspend()` (BA-05/BA-06 — the direct precedent `retire()` mirrors, and the two methods requiring a correctness update), `routers/organization.py`, `models/organization.py`, `repositories/base_repository.py`'s `update()`.
- `architecture/06-Reviews/TECH-DEBT.md` — reviewed for items due in this Business Activity: **TD-004** (`ck_organizations_status` model/migration drift) was the only entry with a natural connection to this BA's own migration work.

### Gap Analysis

- **Satisfied as-is (reused unchanged):** `require_platform_admin`; `OrganizationResponse` (no new response schema); `middleware/tenant.py`'s `/organizations/*` prefix exemption (already covers the new sub-path with zero changes); `observability.py`'s `record_audit`/`publish_event`; `BaseRepository.update()` (no new repository method); `activate()`/`suspend()`'s method shape as the direct template for `retire()`.
- **Required extension:** `OrganizationService` needed a new `retire()` method; `routers/organization.py` needed a new `POST /{organization_id}/retire` route; `models/organization.py`'s `OrganizationStatus` enum needed a third value (`RETIRED`); the `ck_organizations_status` CHECK constraint needed widening via a new Alembic migration (`d2d840d224b6`) — the one genuine, minimal, additive database change this Business Activity required, explicitly anticipated by the task's own lifecycle-model description (ACTIVE/SUSPENDED/RETIRED) and pre-authorized by ADR-004's "purely additive" extension pattern.
- **Required correctness fix to already-accepted code (not scope creep — a necessary consequence of introducing RETIRED):** `activate()` and `suspend()` (BA-05/BA-06) had no RETIRED guard. Without adding one, introducing `RETIRED` as a new status value would have made a retired organization silently reactivatable or re-suspendable via the already-shipped `/activate`/`/suspend` endpoints — directly violating PE-001-C004's explicit, repeated invariant that retirement is never reversible "under any circumstance." Both methods now reject a RETIRED organization with 409 before any other check. This is the same category of narrow, necessary touch to already-committed code as BA-06's one-line addition to BA-05's `activate()` for the `is_active` sync.
- **Business rule (canonical, not invented):** Entry Context explicitly permits retirement from **either** ACTIVE or SUSPENDED — not only from SUSPENDED. The task's own lifecycle diagram (ACTIVE → SUSPENDED → RETIRED) was read as illustrating state severity/ordering, not a mandatory sequential FSM requiring suspension first — PE-001-C004's Entry Context is the authoritative, explicit statement on this point and was followed literally rather than inferring a stricter constraint from an ASCII diagram. `retire()` therefore accepts both starting states and rejects only an already-RETIRED organization (409), mirroring `activate()`/`suspend()`'s already-in-target-state pattern.
- **Missing architecture:** None beyond the one pre-authorized, minimal CHECK-constraint widening. No new entity, table, service boundary, or permission tier.
- **Technical debt closed:** TD-004 (`ck_organizations_status` model/migration drift) — resolved by declaring the constraint on the ORM model (`__table_args__`) in the same change that widens it in the migration, so the two can no longer drift from each other going forward.
- **Technical debt discovered and recorded (not fixed — out of this Business Activity's scope):**
  - **TD-013**: `update_profile()` (BA-04, Steward Organization Identity) has no status check, but PE-001-C004's ERB-C004-05 Entry Context restricts identity stewardship to **ACTIVE** organizations only. Discovered while reading ERB-C004-05 for context while implementing ERB-C004-07; not fixed here because it would change BA-04's already-accepted, already-independently-reviewed behavior — a decision requiring its own review, not a side effect of BA-07.
  - **TD-014**: PE-001-C004's optional Organization Continuity Context (successor-organization link, EX-C004-13) and a persisted retirement reason/authority record are not implemented — deliberately, consistent with ADR-004's incremental-implementation philosophy (no successor-organization concept exists anywhere in the schema; no current consumer needs one).
  - **TD-015**: Frontend `OrganizationStatus`/`StatusBadge` don't recognize `RETIRED` yet (a retired org would render with the same tone as `SUSPENDED`) — consistent with BA-07 being scoped backend-only, same precedent as BA-05/BA-06.
- **Scope boundary (backend-only, consistent with BA-05/BA-06):** no frontend files created or modified — same Action Center/premature-component rationale as the prior two lifecycle Business Activities.

### Scope Delivered

`POST /organizations/{organization_id}/retire` — Retire Organization & Preserve Continuity. Transitions `status` to `RETIRED` from either `ACTIVE` or `SUSPENDED` (and syncs `is_active` to `False`); 404 if the id doesn't exist; 409 if already `RETIRED`. `RETIRED` is terminal — `activate()`/`suspend()` were both updated to reject a RETIRED organization with 409, closing the reversibility gap that introducing the new state would otherwise have opened. Reuses BA-01–06's model, `require_platform_admin`, `OrganizationResponse`, `BaseRepository.update()`, and `TenantMiddleware` exemption unchanged. No row is ever deleted — `get_details()` and `search()` continue to return a retired organization's full data unchanged, satisfying PE-001-C004's continuity requirement via the existing repository layer as-is. Also closes TD-004. No ADR required (see Gap Analysis for the two judgment calls made — Entry Context's dual starting states, and the deliberate deferral of the continuity link/reason — and their rationale).

### Files Created

| File | Purpose |
|---|---|
| `Backend/Services/AuthService/alembic/versions/2026_07_21_2100-d2d840d224b6_organization_retired_lifecycle_state.py` | Widens `ck_organizations_status` to include `'RETIRED'` |

### Files Modified

| File | Summary of Changes |
|---|---|
| `Backend/Services/AuthService/models/organization.py` | Added `OrganizationStatus.RETIRED`; declared `ck_organizations_status` on the model via `__table_args__` (closes TD-004) |
| `Backend/Services/AuthService/services/organization_service.py` | Added `OrganizationService.retire()`; added a RETIRED guard to `activate()` and `suspend()` (409, correctness fix); updated module docstring |
| `Backend/Services/AuthService/routers/organization.py` | Added `POST /{organization_id}/retire` |
| `Backend/Services/AuthService/organization-api.yaml` | Added the `POST /organizations/{organization_id}/retire` path; widened the `status` enum (query param and `OrganizationResponse` schema) to include `RETIRED` |
| `Backend/Services/AuthService/tests/test_organization_service.py` | Added BA-07 unit tests |
| `Backend/Services/AuthService/tests/test_organization_api.py` | Added BA-07 integration tests |
| `Backend/Services/AuthService/README.md` | Updated Organization Management section for BA-07; corrected all Business Activity names per the Scope Reconciliation |
| `architecture/06-Reviews/TECH-DEBT.md` | Closed TD-004; added TD-013, TD-014, TD-015 |

### Database

- **Migration:** `b3f7a1c9d2e4` → `d2d840d224b6`. Widens `ck_organizations_status` from `IN ('ACTIVE', 'SUSPENDED')` to `IN ('ACTIVE', 'SUSPENDED', 'RETIRED')`. No column added, renamed, or dropped — purely a constraint change.
- **Schema changes:** None beyond the constraint widening above.
- **Constraints:** `ck_organizations_status` widened; now also declared on the ORM model (TD-004 resolution).
- **Indexes:** None added.

### APIs

- **Endpoint added:** `POST /organizations/{organization_id}/retire` (200/400/401/403/404/409/422).
- **Endpoints modified (behavior only — same request/response contracts):** `POST /organizations/{organization_id}/activate` and `POST /organizations/{organization_id}/suspend` now additionally return 409 when the target organization is `RETIRED` (previously only checked the "already in target state" case).
- **Request/Response models:** No request body (path parameter only, same basis as `/activate`/`/suspend`) → existing `OrganizationResponse` (status enum widened to include `RETIRED`, no new schema).
- **Authorization:** Same `require_platform_admin` dependency as BA-01–06 — no new tier.
- **OpenAPI:** `organization-api.yaml` updated with the new path and widened enums; YAML-validated.

### Frontend

Not in scope for this Business Activity (see Gap Analysis's "Scope boundary" note above; TD-015 records the resulting display gap). No frontend files created or modified.

### Testing

- **Unit Tests:** 8 new (`test_organization_service.py`, 33 total in that file) — ACTIVE→RETIRED transition; SUSPENDED→RETIRED transition (proving both canonical starting states); reject already-RETIRED (409); 404 on unknown id; profile-field/identity preservation (continuity); RETIRED organization still findable via `search()`'s status filter; `activate()` rejects a RETIRED organization (409, irreversibility); `suspend()` rejects a RETIRED organization (409, irreversibility).
- **Integration Tests:** 12 new (`test_organization_api.py`, 61 total in that file) — success from ACTIVE, success from SUSPENDED, reject-already-RETIRED (409), 404, missing/wrong-role auth (400/403), invalid UUID (422), tenant-header exemption, `/activate` rejects RETIRED (409, via API), `/suspend` rejects RETIRED (409, via API), `GET` still returns full details for a retired organization (continuity, via API), `GET /organizations?status=RETIRED` finds a retired organization (via API).
- **API Tests:** covered by the integration suite above.
- **UI Tests:** N/A — no frontend work in this Business Activity.
- **Overall test results:** 125/125 backend tests passing (20 new this BA — 8 unit, 12 integration — 0 regressions). Full suite run three times during implementation (after unit tests, after integration tests, and again before this report update).

### Manual Verification

1. Using a `PLATFORM_ADMIN` access token, create an organization via `POST /organizations` (defaults to `ACTIVE`).
2. `POST /organizations/{id}/retire` → expect `200` with `status: "RETIRED"`, `is_active: false`.
3. Repeat the same call → expect `409` ("already RETIRED").
4. `POST /organizations/{id}/activate` on the retired organization → expect `409` ("RETIRED and cannot be reactivated"); confirm via `GET /organizations/{id}` that `status` is still `RETIRED`.
5. `POST /organizations/{id}/suspend` on the retired organization → expect `409` ("RETIRED and cannot be suspended"); confirm status is still `RETIRED`.
6. `GET /organizations/{id}` on the retired organization → expect `200` with all profile fields intact (continuity — no data lost).
7. `GET /organizations?status=RETIRED` → confirm the retired organization appears.
8. Create a second organization, `POST .../suspend` it, then `POST .../retire` it → expect `200` with `status: "RETIRED"` (proving retirement directly from SUSPENDED, not only ACTIVE).
9. `POST /organizations/{random-uuid}/retire` → expect `404`.
10. Repeat without `Authorization` → `400`; with a non-`PLATFORM_ADMIN` token → `403`; with a malformed id → `422`.

### Known Limitations (intentionally deferred, per WP-01 scope)

- Same authorization/schema-scope/RLS/frontend-test-harness limitations as BA-01–06 (unchanged — see BA-01 section above); none are specific to BA-07.
- No Organization Continuity Context (successor-organization link, EX-C004-13) or persisted retirement reason/authority record — tracked as TD-014.
- No frontend Retire action, and the frontend doesn't yet visually distinguish `RETIRED` from `SUSPENDED` — tracked as TD-015.
- `update_profile()`'s missing ACTIVE-only status check (a pre-existing BA-04 gap, newly discovered while implementing this Business Activity's Entry Context) is not fixed here — tracked as TD-013.

### Architecture Compliance

- **ARCH-000:** No architecture redefinition; implementation only.
- **IMP-001:** Full Business Activity Lifecycle followed (§6.3) — precondition checks (existence, current status) → Business Object Update → Domain Event (`ORGANIZATION_RETIRED`) → Audit Recording → Response. Business Activity named and contracted as a terminal state transition (§6.6's "Update" type), not raw CRUD.
- **ERG-001:** Unaffected — no EnterpriseNode/Relationship/View concept touched.
- **C-004 / PE-001-C004:** Directly realizes ERB-C004-07, the last of the seven canonical ERBs this work package implements. WP-01's Business Activity scope is now fully aligned with PE-001-C004 (see the Scope Reconciliation, above).
- **ADR-005:** Extended, not violated — the interim `status` column now carries a third value, still a plain column with application-level transition logic, not the metadata-driven state machine SD-002-051 ultimately requires. The extension point ADR-005 anticipated ("a future Metadata Runtime migration replaces [this seam]") is unchanged.
- **URA-001:** Unaffected.
- **Approved ADRs:** ADR-003, ADR-004, ADR-005 — all still honored; none re-litigated. No new ADR raised — the CHECK-constraint widening is pre-authorized by ADR-004's additive-extension pattern, and the Entry Context / continuity-deferral decisions are implementation-level, not architectural.

### Implementation Status

✅ IMPLEMENTATION COMPLETE

### Developer Validation

Performed by the implementing engineer against this Business Activity's own acceptance criteria (IMP-001 §6.4/§6.7, ADR-005, PE-001-C004's ERB-C004-07), mirroring BA-05/BA-06's Developer Validation checklist.

| Acceptance Criterion | Status | Evidence |
|---|---|---|
| Business Intent defined | ✅ Met | Retire Organization & Preserve Continuity: terminal `ACTIVE`/`SUSPENDED` → `RETIRED` transition |
| Input Contract | ✅ Met | `organization_id` path parameter (UUID, FastAPI-validated) |
| Output Contract | ✅ Met | `OrganizationResponse`, reused, enum widened |
| Business Rules enforced | ✅ Met | Existence required (404); already-RETIRED rejected (409); valid from ACTIVE or SUSPENDED per canonical Entry Context |
| Lifecycle transition rules (irreversibility) | ✅ Met | `activate()`/`suspend()` both reject a RETIRED organization (409) — tested at unit and integration layers |
| Validation Rules | ✅ Met | Invalid UUID → 422 (`test_retire_organization_rejects_invalid_uuid`) |
| Authorization Rules | ✅ Met | `require_platform_admin` reused unmodified; 400/403 tested |
| Domain Events | ✅ Met | `ORGANIZATION_RETIRED` published via `publish_event()` |
| Audit Requirements | ✅ Met | `record_audit()` SUCCESS/DENIED, same field mapping as BA-05/BA-06 |
| Continuity preservation | ✅ Met | No row deleted; `get_details()`/`search()` return full data post-retirement — tested at unit and integration layers |
| Error Handling | ✅ Met | 404/409/422/400/403 all explicit, no silent no-ops, no 500s |
| No architecture change | ✅ Met | Only pre-authorized, additive CHECK-constraint widening; no new entity/table/permission tier |
| Reuse over creation | ✅ Met | `BaseRepository.update()`, `OrganizationResponse`, `require_platform_admin`, `observability.py`, and `activate()`/`suspend()`'s method shape all reused; only `retire()` (service), one router function, and the necessary `activate()`/`suspend()` guard additions are new |
| Tests (unit/integration/regression) | ✅ Met | 125/125 passing, 20 new, 0 regressions |
| Documentation updated | ✅ Met | IMP-REPORT-WP-01 (this section), IRA-001 (already reconciled), README.md, `organization-api.yaml` |
| Technical debt resolved/recorded | ✅ Met | TD-004 closed; TD-013/014/015 recorded; no duplicate entries |

**Developer Validation outcome: PASS.** All acceptance criteria met by the implementing engineer's own assessment. This is developer validation, not Independent Review — CLAUDE.md §19.7's Business Activity Completion Gate still requires a separate, independently-run review before this Business Activity — and WP-01 as a whole — is considered fully complete; that review has not yet been requested for BA-07.

### Independent Review

**Independent Review: Accepted — ACCEPTED WITH OBSERVATIONS** (2026-07-23, fresh-context subagent with no memory of the implementation session; extracted and read `PE-001-C004_Organization_Management.docx` in full itself rather than trusting this report's citations, ran the full backend test suite independently, and performed its own codebase-wide search for Organization/status consumers rather than accepting the Enterprise Lifecycle Consistency Check's findings at face value).

**Review Result: ACCEPTED WITH OBSERVATIONS**

**Test results actually observed:** `pytest -q` (with `JWT_SECRET_KEY`/`JWT_ALGORITHM` set) → **125 passed, 0 failed**, 12.73s. Test-count deltas verified against the last committed state (`HEAD`): `test_organization_service.py` 25→33 (+8), `test_organization_api.py` 49→61 (+12) — matching this report's claims exactly, with all test-file diffs additive-only.

**Findings:** `retire()`'s Entry Context was checked against the extracted canonical text of PE-001-C004 §3.8 directly — confirmed to accept both `ACTIVE` and `SUSPENDED` as valid starting states (not only `SUSPENDED`), exactly matching "Authoritative Organization Context in ACTIVE or SUSPENDED state." Already-RETIRED correctly rejected with 409 (not a no-op, not a 500). The irreversibility guards added to `activate()`/`suspend()` were read line-by-line and confirmed to run strictly before any mutating repository call in both methods; the relevant tests were confirmed to assert the stronger invariant (409 **and** a follow-up fetch proving the status did not change), not merely "an exception was raised." Historical continuity confirmed via direct search: no `DELETE` endpoint or call to `BaseRepository.delete()` is wired to Organization anywhere; `get_details()`/`search()` remain status-agnostic reads. The Alembic migration (`d2d840d224b6`) was confirmed to only widen the existing CHECK constraint (no column added/dropped/renamed), with `models/organization.py`'s `__table_args__` declaration verified character-for-character identical to the migration's constraint text; `alembic heads` resolves to exactly one head. `organization-api.yaml` parses cleanly and the previously-stale `/activate`/`/suspend` documentation (both the router decorators and the YAML) was confirmed genuinely updated to mention RETIRED-rejection, via direct diff inspection showing comment/description-only changes. **The Consistency Check's TD-016 finding was independently re-derived, not just accepted**: `services/auth_service.py`'s `authenticate_user()` was read directly and confirmed to never reference `Organization` or any status field — only `Membership.membership_status`/`is_active` gates login, meaning a person with an active Membership can today authenticate into a `SUSPENDED` or `RETIRED` organization's context. TD-004/013/014/015/016 in the Technical Debt Register were all confirmed accurate, non-duplicate, and consistent with the register's existing schema; no previously-`Closed` row was altered.

**Defects found:** None. No functional, security, or business-rule defect was found that would block acceptance.

**Test-coverage gap found (new — not caught by the original Consistency Check, recorded as TD-017 below):** `OrganizationRepository.get_by_code()` has no status filter, so `establish()`'s duplicate-code check correctly rejects reusing a RETIRED organization's `organization_code` for a new organization — architecturally correct continuity behavior — but **no test exercises this scenario** in either test file. A coverage gap, not a functional defect.

**Risks recorded (non-blocking):**
1. TD-016 is a real, currently-exploitable gap (not hypothetical) — a person can authenticate into a SUSPENDED/RETIRED organization's context today. Correctly out of C-004's capability boundary to fix (requires touching AuthService's core login flow, a different capability, C-001/URA-001), consistent with the same class of judgment call as TD-012/TD-013's precedent — but should not linger indefinitely at Medium priority given it directly undermines the "SUSPENDED/RETIRED are not valid for new dependent activity" invariant PE-001-C004 establishes.
2. TD-013 (`update_profile()` missing an ACTIVE-only status check) remains open for the same reasons as previously recorded — re-confirmed still correctly out of scope.
3. The untested retired-code-reuse path (new finding, TD-017) — low risk since the code path itself is correct, but any future refactor of `get_by_code()`/`establish()` could silently reintroduce a reuse bug with no test to catch it.

**Recommendations carried forward:**
- Add a test for retired-organization-code-reuse rejection (e.g. `test_establish_rejects_reusing_a_retired_organizations_code`) at the next convenient touch point — recorded as TD-017.
- Prioritize TD-016 as a near-term item for whatever work package next owns AuthService's login flow or Membership Management — the most consequential open item this review surfaced.
- Consider whether TD-013 and TD-016 together warrant a dedicated cross-cutting hardening pass once Role & Permission / Membership Management work packages begin.
- Nothing found in this review should block WP-01 Certification once BA-07 is committed.

### Certification

Certification Status: Pending (WP-level activity, performed only after WP-01 completes and BA-07's commit, per CLAUDE.md §19.7)

### Repository

Committed as `a63c62c` — "feat(auth-service): WP-01 BA-07 - Retire Organization & Preserve Continuity" (2026-07-23), which also carried IRA-001's previously-uncommitted WP-01 Scope Reconciliation (§15). This Independent Review outcome recorded in a separate documentation commit per §19.7's completion-gate repository condition.

---

## BA-07 — Enterprise Lifecycle Consistency Check

**Date:** 2026-07-22
**Trigger:** Before Independent Review, a full lifecycle consistency verification was performed across all BA-01 through BA-07 implementations to confirm that introducing the `RETIRED` state left no previously-implemented Business Activity in an inconsistent state. No redesign; no new functionality — verification only, per the task's explicit instructions.

**Method:** Every reference to `status`/`ACTIVE`/`SUSPENDED`/`RETIRED`/`OrganizationStatus` was located across `models/`, `services/`, `routers/`, `repositories/`, and `schemas/` and individually reviewed. The search was then widened beyond the Organization Management module itself to `middleware/tenant.py`, `services/auth_service.py`, `services/bootstrap_service.py`, and `repositories/membership_repository.py` — every other consumer of Organization or its lifecycle state in the codebase — to check for consequences outside BA-01–07's own files.

**Confirmed consistent (no defect):**

- **RETIRED cannot re-enter the lifecycle:** `activate()` and `suspend()` both reject a RETIRED organization with 409 before any mutating call — verified in code and already covered by `test_activate_rejects_retired_organization`/`test_suspend_rejects_retired_organization` (unit) and their API-layer equivalents (integration).
- **No physical-delete path exists:** `BaseRepository.delete()` is a generic, inherited method never wired to any Organization router or service method — retirement is the only "removal" concept exposed, and it never deletes a row.
- **Read-only operations continue to function:** `get_details()` and `search()` are status-agnostic by construction and were already confirmed (BA-07's own tests) to return full data for RETIRED organizations.
- **Search/List correctly exposes lifecycle state:** the status filter is a generic `Organization.status == status` comparison with no hardcoded two-value assumption; `RETIRED` flows through automatically (confirmed by `test_retire_is_findable_by_status_filter` and `test_search_organizations_can_filter_by_retired_status`).
- **Validation rules remain internally consistent:** `schemas/organization.py` has no hardcoded ACTIVE/SUSPENDED enum or validator that would reject `RETIRED`; `OrganizationResponse.status` is a plain `str`.
- **Domain Events remain consistent:** `ORGANIZATION_ESTABLISHED`/`_PROFILE_UPDATED`/`_ACTIVATED`/`_SUSPENDED`/`_RETIRED` all fire only on success, with a uniform payload shape (`organization_id`, `organization_code`, `previous_status` where applicable, `status`).
- **Audit behaviour remains consistent:** `record_audit()` is called with `DENIED` on every rejection path (not-found, already-in-target-state, RETIRED-guard) and `SUCCESS` on every write, with the same metadata shape, across all five write-path Business Activities.
- **WP-00's bootstrap seeding is unaffected:** `bootstrap_service.py` never sets `status` explicitly (relies on the model's `ACTIVE` default).
- **`middleware/tenant.py`'s exemption is unaffected:** it matches on path prefix only, never on status.

**Minor documentation defects found and corrected** (direct, narrow consequences of BA-07's own changes, corrected within BA-07's scope — no test or business-logic change required; regression suite re-run clean after each):

1. `models/organization.py`'s `status` column docstring still read "('ACTIVE' / 'SUSPENDED')" after `RETIRED` was added earlier in this same Business Activity — corrected.
2. `routers/organization.py`'s `/activate` and `/suspend` endpoint `description` and `409` response text documented only the "already in target state" rejection reason, omitting the RETIRED-rejection behavior BA-07 itself added to those two endpoints — corrected in both the route decorators and `organization-api.yaml` (all four locations).
3. `update_profile()`'s docstring said status "belongs to the Activate/Suspend Business Activities" (pre-BA-07 wording) — corrected to "Activate/Suspend/Retire," with a note cross-referencing TD-013 added directly at the point in the code the gap applies to.

**Broader finding, recorded as new technical debt, NOT implemented** (exceeds BA-07 scope, per the task's explicit instructions):

- **TD-016** (new): `services/auth_service.py`'s `authenticate_user()` never checks `Organization.status` — only `Membership.is_active` is consulted, meaning a person with an active Membership can still select and authenticate into a `SUSPENDED` or `RETIRED` organization's context. This gap pre-dates BA-07 (equally true since `SUSPENDED` was introduced by BA-06) and was only surfaced by this consistency check, not newly created by `RETIRED`. It cross-cuts AuthService's login flow and Membership/Role & Permission Management — both explicitly excluded from WP-01's scope per IRA-001 — so it was recorded, not fixed. See `architecture/06-Reviews/TECH-DEBT.md`.
- **TD-013** (recorded during BA-07's original implementation) was re-examined and re-confirmed correctly out of scope: it is a pre-existing gap since BA-04 (the ACTIVE-only Entry Context restriction canonically applies to SUSPENDED too, which predates BA-07), not a new consequence of `RETIRED` specifically, and fixing it would change BA-04's already-accepted, already-independently-reviewed behavior.

**Regression verification:** Full backend suite re-run after every corrective change — **125/125 passing, 0 regressions**, throughout.

**Outcome:** No functional or business-logic defects were found in BA-01 through BA-07's handling of `ACTIVE`/`SUSPENDED`/`RETIRED`. Three minor, in-scope documentation inconsistencies were corrected. One new, genuinely out-of-scope cross-service finding (TD-016) was recorded per the task's instructions, not implemented. This check's findings were subsequently validated, not merely accepted, by BA-07's Independent Review (above), which independently re-derived TD-016 and found one additional test-coverage gap (TD-017).

---

## WP-01 Implementation Freeze

**Date:** 2026-07-23
**Status:** All 7 Business Activities of WP-01 (per the canonical Business Activity list established by the WP-01 Scope Reconciliation, above) are now **implementation complete, developer-validated, independently reviewed, and committed**:

| Business Activity | Implementation | Developer Validation | Independent Review | Committed |
|---|---|---|---|---|
| BA-01 Establish Organization Identity | ✅ | ✅ | ✅ Accepted | ✅ `145acfe` |
| BA-02 Resolve Organization Details | ✅ | ✅ | ✅ Accepted with Observations | ✅ `4d5c52a` |
| BA-03 Search & List Organizations | ✅ | ✅ | ✅ Accepted with Observations | ✅ `95fd4fe` |
| BA-04 Steward Organization Identity | ✅ | ✅ | ✅ Accepted | ✅ `e7b77f9` |
| BA-05 Reactivate Suspended Organization | ✅ | ✅ | ✅ Accepted with Observations | ✅ `467d847` |
| BA-06 Suspend Organization | ✅ | ✅ | ✅ Accepted with Observations | ✅ `a264b86` |
| BA-07 Retire Organization & Preserve Continuity | ✅ | ✅ | ✅ Accepted with Observations | ✅ `a63c62c` |

**Implementation is now frozen.** No additional feature implementation shall occur within WP-01 beyond this point.

From this point forward, changes to WP-01's Organization Management implementation are permitted **only** through:

1. **Independent Certification findings** — the WP-level Certification (CLAUDE.md §19.7) that follows this freeze may identify items requiring remediation before WP-01 is considered formally complete.
2. **Approved remediation** — any remediation explicitly directed in response to Certification findings.
3. **Critical defect fixes** — a genuine, production-impacting defect discovered after this point, not a scope addition or enhancement.

No new Business Activity, no configuration/audit-history-style scope addition, and none of the open Technical Debt items (TD-002, TD-003, TD-005, TD-006, TD-007, TD-009, TD-010, TD-011, TD-013, TD-014, TD-015, TD-016, TD-017, TD-018, TD-019, TD-020 — all still `Open` in `architecture/06-Reviews/TECH-DEBT.md`) shall be implemented under this freeze. They remain correctly recorded, non-blocking, and explicitly deferred to their stated `Planned Resolution` (a later Business Activity slot, WP-01 Closure, WP-02, or a dedicated future work package) — resolving them now would itself violate this freeze.

**Register completeness audit (Step 3 of this task):** Before declaring the freeze, every Independent Review section in this report (BA-01 through BA-07) was re-read specifically to confirm no non-blocking observation exists only in review prose. Three were found to violate CLAUDE.md §19.8.2 this way, each carried across multiple reviews without ever being given its own entry: the audit-before-event ordering discrepancy (flagged at BA-05's and BA-06's reviews), the undelivered Action Center UI (flagged at the same two reviews), and a conditional refactoring recommendation (BA-06's review judged a shared `_transition()` helper warranted "only if a third lifecycle transition is ever added" — BA-07's `retire()` met that condition, but the recommendation was never revisited or registered). These are now **TD-018**, **TD-019**, and **TD-020**. All other carried-forward observations were confirmed already correctly registered (TD-001 through TD-017). The register is now complete: every outstanding non-blocking observation from every Independent Review to date has a `TD-NNN` entry.

**Next step:** WP-01 Independent Certification (CLAUDE.md §19.7), a separate WP-level governance activity performed independently of this implementation session, not yet begun.

---

*(WP-01's Business Activity implementation is complete and frozen as of this entry. The next entry in this report will be either WP-01 Certification's outcome or a remediation record responding to it.)*

---

## IRA-001A — Constitutional Correction: Organization Identity Establishment & Activation

**Trigger:** This repository's own constitutional-interpretation, behavioral-compliance-assessment, and historical-governance-validity investigation chain established that `OrganizationService.establish()` (BA-01) violated PE-001-C004's BR-C004-01 ("An Organization SHALL NOT be treated as valid before governed activation") and Contract 5.4 ("no Organization exists in this sense" prior to activation) — using code that existed at WP-01's own certification time (2026-07-23 self-reported, CERT-WP-01), not a documentation-accuracy gap as CERT-WP-01's own Finding A originally classified it. Full governing document: `architecture/05-Implementation/IRA-001A_WP-01_Organization_Establishment_Activation_Correction.md`.

**Note on WP-01's freeze (above):** this correction is exactly the class of change the freeze's own text anticipates permitting — a governance-directed remediation responding to a material finding about already-certified behavior, not a scope addition or enhancement. It does not reopen or re-litigate BA-02 through BA-07, none of which was found non-compliant.

### Business Activity Implemented

**BA-01 (amended) — Establish Organization Identity**, realizing ERB-C004-01's own Exit Context correctly for the first time: an Organization Anchor Context, not an Authoritative Organization Context. **BA-01B (new) — Verify Organization Domain Claim**, realizing ERB-C004-02. **BA-01C (new) — Activate Organization (first-time)**, realizing ERB-C004-03 — the first, distinct, governed act producing the first Authoritative Organization Context for a given establishment attempt.

### Architectural Realization

A separate, non-authoritative persistence construct (`organization_establishment_attempts`, the Organization Anchor Context per PE-001-C004 §1.16) — selected over three alternatives (a fourth lifecycle status value on `organizations`, constitutionally disqualified by PE-001-C004 §9.6's own drafting history; a single-table authority flag; a workflow-orchestrated single table) for satisfying BR-C004-08/Contract 5.4 by construction and reopening zero already-certified Business Activities. Full option analysis: see this repository's own architectural-decision investigation (incorporated into IRA-001A §4).

### Files Created

| File | Purpose |
|---|---|
| `Backend/Services/AuthService/models/organization_establishment_attempt.py` | `OrganizationEstablishmentAttempt` model, `DomainVerificationStatus` enum |
| `Backend/Services/AuthService/alembic/versions/2026_08_02_0900-e5c1a9f4b7d2_organization_establishment_attempt.py` | Migration: creates `organization_establishment_attempts` — purely additive, no existing table altered |
| `Backend/Services/AuthService/repositories/organization_establishment_attempt_repository.py` | `OrganizationEstablishmentAttemptRepository.get_by_code()` |
| `Backend/Services/AuthService/schemas/organization_establishment_attempt.py` | Request/response schemas for BA-01/BA-01B/BA-01C |
| `Backend/Services/AuthService/routers/organization_establishment_attempt.py` | `POST /organization-establishment-attempts`, `.../verify-domain`, `.../activate` |
| `Backend/Services/AuthService/organization-establishment-attempt-api.yaml` | OpenAPI contract for the three new endpoints |
| `architecture/05-Implementation/IRA-001A_WP-01_Organization_Establishment_Activation_Correction.md` | Governing IRA for this correction |

### Files Modified

| File | Summary of Changes |
|---|---|
| `Backend/Services/AuthService/services/organization_service.py` | `establish()` rewritten to write only to the new Anchor construct; added `verify_domain_claim()`, `activate_establishment()`. `get_details()`, `search()`, `update_profile()`, `activate()`, `suspend()`, `retire()` — **zero changes**, confirmed by diff. |
| `Backend/Services/AuthService/routers/organization.py` | Removed the `POST ""` (establish) handler — relocated, not repurposed. Every other endpoint unchanged. |
| `Backend/Services/AuthService/main.py` | Registered the new router at `/organization-establishment-attempts`. |
| `Backend/Services/AuthService/middleware/tenant.py` | Added `/organization-establishment-attempts` prefix exemption. |
| `Backend/Services/AuthService/models/__init__.py` | Registered `OrganizationEstablishmentAttempt` in the SQLAlchemy mapper-registry import list. |
| `Backend/Services/AuthService/schemas/organization.py` | Removed the now-dead `EstablishOrganizationRequest` class (superseded by `EstablishOrganizationAttemptRequest`); updated two docstrings. |
| `Backend/Services/AuthService/tests/test_organization_service.py` | BA-01's establish tests rewritten; BA-01B/BA-01C tests added; BA-02–BA-07 test setup code migrated to a new `_establish_and_activate` helper — their own assertions unchanged. |
| `Backend/Services/AuthService/tests/test_organization_api.py` | Same pattern, HTTP level. |
| `Backend/Services/AuthService/organization-api.yaml` | Removed the `POST /organizations` path and `EstablishOrganizationRequest` schema; version bumped to 1.1.0. |
| `architecture/06-Reviews/TECH-DEBT.md` | TD-046 through TD-049 added. |
| `architecture/00-Governance/WPR-001_Work_Package_Roadmap.md` | WP-01 row updated to reflect the correction. |

No other Work Package's files were touched — confirmed by `git diff --stat` (Independent Review, below).

### Validation

- Full AuthService suite: **469 passed**, zero regressions (441 pre-existing at WP-04's own baseline this session + 28 net from this correction and the same session's other work — re-run directly, not taken on faith).
- Confirmed a single Alembic head (`e5c1a9f4b7d2`) after the new migration.
- Confirmed `establish()` never writes to `organizations` (grep: `organization_repo.create` appears exactly once in the file, inside `activate_establishment`).
- Confirmed `get_details()`/`search()` (BA-02/BA-03) reference the new repository nowhere.
- Confirmed no file outside this change set references `organization_establishment_attempts`.
- OpenAPI schema generated successfully: 60 total paths (57 before), including the three new endpoints; `/organizations` retains only `GET`.
- Both `organization-api.yaml` and the new `organization-establishment-attempt-api.yaml` validated via `yaml.safe_load`.

### Status

**Implementation:** COMPLETE

**Developer Validation:** Complete (469/469 full suite passing)

**Independent Review:** APPROVED WITH OBSERVATIONS

**Repository Commit:** [recorded in commit-hash recording pass]

### Independent Review

**Review Result:** APPROVED WITH OBSERVATIONS

**Review Summary:** An independent reviewer, with no prior involvement in this correction, verified it against actual repository state rather than trusting IRA-001A's own narrative, and re-ran the full test suite directly. Confirmed by direct grep and full reads: `establish()` writes only to the new Anchor construct (`organization_repo.create` appears exactly once in `organization_service.py`, inside `activate_establishment`); `activate_establishment()`'s gate (VERIFIED domain or an explicit `no_domain_activation_reason`) has no bypass path, traced by hand; both repositories share the same request-scoped session, so the `IntegrityError` rollback on a concurrent-duplicate race correctly unwinds both tables together; `get_details()`/`search()` (BA-02/BA-03) were confirmed to reference the new repository nowhere, and their diffs are empty except docstring wording; `routers/organization.py` no longer has a `POST ""` handler (confirmed removed, not repurposed); a repository-wide grep found no stray reference to `organization_establishment_attempts` outside the expected new/modified files. Tests were re-read in full: BA-01's own tests now assert zero `organizations` rows exist after `establish()` alone; BA-01B/BA-01C have dedicated 404/409/precondition tests; BA-02 through BA-07's own test assertions were confirmed byte-for-byte unchanged (only their setup fixtures were migrated to a new helper). The reviewer re-ran the full suite directly (468 passed at that point) and confirmed `git status`/`git diff --stat` touched only the expected file set, no other Work Package.

Findings, all resolved in this same documentation/implementation pass:
1. **`no_domain_activation_reason` accepted whitespace-only strings**, technically satisfying the gate's truthiness check without recording a genuine decision (BR-C004-09's intent). **Fixed**: `activate_establishment()` now strips and treats an empty-after-strip reason as absent; a dedicated test (`test_activate_establishment_rejects_whitespace_only_no_domain_reason`) added. Suite re-run: 469/469.
2. **IRA-001A's own §9 prematurely claimed Independent Review was complete**, citing this very section before it existed. **Fixed**: corrected to accurately reflect that this review (the one being recorded here) is the first and satisfies the claim.
3. **An undisclosed, unrelated stray file** (`architecture/05-Implementation/_PE-001-C005_ba02_check.txt`, leftover scratch output from an earlier, separate investigation this same session) was found untracked in the working tree. Confirmed unrelated to this correction's diff; **left as-is, not committed with this change set** — disclosed in IRA-001A §8 for traceability.
4. Two cross-capability/architecture observations were raised and registered as Technical Debt rather than fixed inline, consistent with §19.8's discipline: **TD-047** (`MembershipService`, WP-03's own file, bypasses C-004's resolution authority — out of WP-01A's ownership) and **TD-048** (BA-02 doesn't realize EX-C004-05's typed validity contract — no current consumer needs it). **TD-046** (BA-01B has no real proof-of-control mechanism) and **TD-049** (frontend now calls a removed endpoint) were also registered, both disclosed in IRA-001A from the start, not review findings.

No defect was found in the core correction: no code path creates or exposes an Organization as valid outside `activate_establishment()`'s governed gate, and no code path lets a pre-activation attempt leak through BA-02/BA-03 or any other consumer.
