# IMP-REPORT-WP-01 — Organization Management (C-004)

**Type:** Living Implementation Report (audit trail — not a duplicate of the codebase)
**Work Package:** WP-01 — Organization Management
**Governing documents:** IRA-001 (`architecture/05-Implementation/IRA-001_WP-01_Organization_Management_Implementation_Readiness_Assessment.md`), ADR-003, ADR-004, ADR-005 (`architecture/07-Decisions/`)
**Maintenance rule:** One report for all of WP-01. Append a new Business Activity section per completion; update the dashboard each time. Do not create per-Business-Activity report files.

---

## WP-01 Progress Dashboard

**Overall Status:** 🟡 In Progress

**Business Activities**

- ✅ BA-01 Establish Organization
- ✅ BA-02 View Organization
- ✅ BA-03 Search Organizations
- ✅ BA-04 Update Organization Profile
- ⏳ BA-05 Activate Organization
- ⏳ BA-06 Suspend Organization
- ⏳ BA-07 Organization Configuration
- ⏳ BA-08 Audit History

**Progress**

- Completed: 4 / 8
- Progress: 50%
- Database migrations completed: 1 (`b3f7a1c9d2e4` — `organizations.status`/`description`; neither BA-02, BA-03, nor BA-04 required schema changes)
- API endpoints delivered: 4 (`POST /organizations`, `GET /organizations/{organization_id}`, `GET /organizations`, `PUT /organizations/{organization_id}`)
- UI screens delivered: 1 (`/platform-admin/organizations`, now the primary Search/List grid with Create, View Details, and Edit as modal actions, plus the standalone by-ID lookup section)
- Tests added: 48 (15 unit, 33 integration)
- ADRs raised during implementation: 0 across BA-01 through BA-04 (ADR-003, ADR-004, ADR-005 were recorded during the WP-01 readiness assessment, prior to implementation start — see IRA-001)

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

*(Further Business Activity sections are appended below as WP-01 progresses. Dashboard above is updated with each entry. Final WP-01 Summary is added when BA-08 completes.)*
