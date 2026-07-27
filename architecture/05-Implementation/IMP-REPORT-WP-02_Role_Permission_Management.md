# IMP-REPORT-WP-02 — Role & Permission Management (C-003)

**Work Package:** WP-02 — Role & Permission Management (C-003)
**Governing Readiness Assessment:** `IRA-002_WP-02_Role_Permission_Management_Implementation_Readiness_Assessment.md` (Approved — WP-02 READY, BA-01 only; BA-02 assessed inline below per IRA-002 §2.2's own instruction that BA-02 onward each require a fresh gap analysis before implementation)
**Governing Capability Specification:** `PE-001-C003_Role_Permission_Management.docx` v1.0 (three ERBs, ten Enterprise Experiences)
**Scope of this report:** BA-01, BA-02, and BA-03, per the Business Activity Completion Gate (CLAUDE.md §19.7), each completed and gated independently. BA-04 through BA-10 (mapped in IRA-002 §2.2) are not started.

---

## BA-01 — Establish Business or System Role

## Business Activity Implemented

**BA-01 — Establish Business or System Role**, realizing PE-001-C003's ERB-C003-01 (Define Authorization Policy Structure) / EX-C003-01 (Establish Business or System Role).

### Business Activity Contract (IMP-001 §6.7)

- **Business Intent:** Establish a new Business Role or System Role as a governed, metadata-driven authorization structure, per URA-001 Section 3 and CAP-001's C-003 Business Intent ("Manage authorization roles and permissions").
- **Input Contract:** `role_code` (unique, 1–100 chars), `role_name` (1–255 chars), `description` (optional, ≤1000 chars), `is_system_role` (boolean, defaults False).
- **Output Contract:** The established Role (id, role_code, role_name, description, is_system_role, created_at, updated_at), or an HTTP error naming the specific violated rule.
- **Business Rules:**
  - BR-C003-01 — established only where `role_code` is unique and the proposing Person's defining authority is confirmed.
  - BR-C003-02 — establishing a Role never automatically confers a Domain Permission, Approval Authority, or Runtime Assignment (satisfied by construction: `RoleService.establish()` never writes to `role_permissions`).
  - BR-C003-08 — restricted to confirmed human defining authorities. **Scoped simplification (IRA-002 §2.7):** gated on the existing `PLATFORM_ADMIN` role, since persona-specific authority (Corporate Admin / Security Admin / User Admin) cannot be implemented until ADR-002 resolves the canonical role catalog. Stated explicitly, not a silent gap.
- **Validation Rules:** `role_code` uniqueness enforced both at the service layer (pre-check, clean 409) and by the database's existing unique constraint (concurrent-duplicate race, same pattern as `OrganizationService.establish()`).
- **Authorization Rules:** `PLATFORM_ADMIN` role required (see BR-C003-08 above).
- **Domain Events:** `ROLE_ESTABLISHED` (role_id, role_code, role_name, is_system_role).
- **Audit Requirements:** `record_audit("ESTABLISH_ROLE", ...)` on both success and denial (duplicate), per SD-002-054's seven audit questions — same mechanism WP-01 established, reused as-is.
- **Tests:** `tests/test_role_service.py` (5 unit tests), `tests/test_role_api.py` (7 API/authorization tests) — 12 new tests, all passing; full suite (137 tests) passing with zero regressions.

---

## Governing Architecture Review (Step 1)

Reviewed: PE-001-C003 (extracted and read in full — Document Control, Chapters 1–9), URA-001 Sections 3–7, IMP-001 (Business Activity Registry — confirmed no canonical C-003 BA/EAC identifier exists), ADR-001 through ADR-005, RTA-001 §11 (boundary confirmation only, per PE-001-C003's own stated consultation scope), SD-002/SD-003 (Universal Business Object / Interaction principles, consulted for audit/explainability discipline, not duplicated locally). Enterprise Intelligence documents were **not** reviewed — C-003 does not depend on them, consistent with the instruction to review only C-003's governing assets.

**Key finding requiring disclosure:** ADR-002 (Reconcile AuthService Seed Role Catalog with MDP-001/URA-001) is **Proposed, not Accepted**, and directly touches the `roles` table this Business Activity uses. Full gap analysis in IRA-002 §2.1. Disposition: BA-01 builds the establishment *mechanism* only, reuses the existing `is_system_role` discriminator, and does not touch the seed catalog — this keeps BA-01 correct regardless of ADR-002's eventual resolution, and the report does not resolve ADR-002 itself (CLAUDE.md §18).

---

## Gap Analysis Summary (see IRA-002 for full detail)

- **Database:** No gap. `roles` table already exists (WP-00-era migration); BA-01 adds application-layer code only. Zero new tables, columns, or constraints — no architectural-impact escalation triggered (CLAUDE.md §19.4).
- **Business Activities:** No canonical BA identifier existed for C-003 anywhere in the repository (PE-001-C003 records every BA/EAC binding as Pending Canonical Binding). The ten-BA mapping in IRA-002 §2.2 was derived from PE-001-C003's ten Enterprise Experiences, following the same discipline WP-01 applied when it derived its own seven-BA list from PE-001-C004.
- **Database Impact:** None (§2.6).
- **API Impact:** One new endpoint, `POST /roles`, mirroring `POST /organizations`'s established shape exactly (schema/repository/service/router layering, duplicate-check-then-create, audit/event emission).
- **UI Impact:** Out of scope for BA-01 (Step 3 requested backend Business Activity implementation only).
- **Dependencies:** None blocking BA-01. `Membership.role_id` already FK-references `roles.id` (WP-00-era) — unaffected, since BA-01 only adds rows, never alters the table shape.
- **Risks:** See IRA-002 §3 (ADR-002 resolution timing; BA-01's authorization-gate simplification; no seed-catalog collision risk, since BA-01 neither seeds nor renames existing rows).
- **Technical Debt inherited from WP-01:** `dependencies.require_platform_admin`'s own docstring (written during WP-01) explicitly names Role & Permission Management as the work package expected to replace its interim, PLATFORM_ADMIN-only gate with real Domain Permission checks. BA-01 continues reusing that same interim gate — this is the exact debt WP-01 flagged in advance, not new debt introduced here (see IRA-002 §4).

---

## Documents Updated

**Architecture (new, planning only):**
- `architecture/05-Implementation/IRA-002_WP-02_Role_Permission_Management_Implementation_Readiness_Assessment.md`
- `architecture/05-Implementation/IMP-REPORT-WP-02_Role_Permission_Management.md` (this report)

**Implementation (new):**
- `Backend/Services/AuthService/schemas/role.py`
- `Backend/Services/AuthService/repositories/role_repository.py`
- `Backend/Services/AuthService/services/role_service.py`
- `Backend/Services/AuthService/routers/role.py`
- `Backend/Services/AuthService/role-api.yaml`
- `Backend/Services/AuthService/tests/test_role_service.py`
- `Backend/Services/AuthService/tests/test_role_api.py`

**Implementation (modified, minimal):**
- `Backend/Services/AuthService/main.py` — registered the new `role` router at `/roles`.
- `Backend/Services/AuthService/middleware/tenant.py` — added `/roles` and `/roles/*` to the tenant-exemption list (Roles are platform-global, same basis as `/organizations`).

No database migration was required. No existing model, repository, service, or router was modified beyond the two minimal registrations above.

---

## Validation

- 12 new tests (5 unit, 7 API), all passing.
- Full AuthService suite: **137 passed**, zero regressions.
- Confirmed `role_permissions` is never written by `RoleService.establish()` (BR-C003-02, tested explicitly in `test_establish_never_grants_a_permission`).
- Confirmed duplicate `role_code` is rejected with 409 both via pre-check and the database's own unique constraint path (mirroring `OrganizationService.establish()`'s concurrent-duplicate handling).
- Confirmed non-`PLATFORM_ADMIN` callers receive 403 (`test_establish_role_rejects_non_platform_admin`), consistent with IRA-002 §2.7's disclosed simplification.

---

## Status

**Implementation:** COMPLETE

**Developer Validation:** Pending

**Independent Review:** APPROVED WITH OBSERVATIONS

**Repository Commit:** Committed to `master` in three commits — `bca7f0b` (implementation: 9 files), `178d07b` (documentation: this report + TECH-DEBT.md TD-021), and `67e45c9` (IRA-002, committed unchanged after independent verification found no factual corrections required).

**Commit Hash:** `bca7f0b` (implementation), `178d07b` (documentation: implementation report + TECH-DEBT.md), `67e45c9` (IRA-002)

**Commit Date:** 2026-07-27 (all three commits)

**Current Repository Status:** All WP-02 BA-01 artifacts are committed to `master` — implementation (9 files), TECH-DEBT.md (TD-021), IMP-REPORT-WP-02 (this report), and IRA-002. The only remaining uncommitted change belonging to this update is this report's own Repository Commit/Commit Hash/Commit Date/Current Repository Status section, being committed now. Unrelated pre-existing working-tree changes (`CLAUDE.md`, `architecture/04-Technical/Master_Technical_Architecture.md`, `architecture/06-Reviews/ARM-001_Implementation_Report.md`, and several untracked Enterprise Intelligence remediation-program documents) remain outside WP-02's scope and are not part of this commit.

---

## Independent Review

**Review Result:** APPROVED WITH OBSERVATIONS

**Review Summary:** An independent reviewer, with no prior involvement, verified all seven required points against actual repository state and re-ran the test suite directly rather than trusting this report's claims. PE-001-C003 was re-extracted and re-read independently; BR-C003-01, BR-C003-02, and BR-C003-08 were each traced through the actual code paths (not docstrings), and Contract 5.5's "every rejection names the specific violated rule" requirement was confirmed against the real HTTP responses for duplicate `role_code` (409), missing `role_name` (422), and non-PLATFORM_ADMIN callers (403). `git status`/`git diff` confirmed only BA-01 was implemented (zero BA-02–BA-10 code found anywhere), zero database schema changes (no new migration, `models/role.py` byte-identical to its pre-WP-02 state), and correct reuse of WP-01's repository/service/router/audit/event patterns, verified side-by-side against `OrganizationService`/`OrganizationRepository`/`routers/organization.py`. ADR-002 compliance was independently reasoned through all three of its options (A/B/C) against the actual code (no role-code naming convention hardcoded in `schemas/role.py`, seed catalog files untouched) and confirmed BA-01 would require zero change under any of them. Tests were re-run directly: 12/12 new tests pass, 137/137 full suite passes, matching the report's claims exactly, and both new test files were read in full to confirm each test exercises genuinely distinct behavior. One Minor finding was recorded: the PLATFORM_ADMIN-only authorization-gate simplification (BR-C003-08's deferred persona-specific model) is genuinely and repeatedly disclosed in prose (dependencies.py docstring, IRA-001 §2.7, IRA-002 §2.7/§4) but has never been given its own entry in `architecture/06-Reviews/TECH-DEBT.md`, which CLAUDE.md §19.8.2 requires — a registration-hygiene gap, not a functional, security, or architectural defect, and not blocking. The reviewer also noted three unrelated pre-existing uncommitted changes (`CLAUDE.md`, Master Technical Architecture, `ARM-001_Implementation_Report.md`) that are confirmed unrelated to BA-01 and should not be mistaken for scope creep.

---

## BA-02 — Establish Domain Permission

Realizing PE-001-C003's ERB-C003-01 (Define Authorization Policy Structure) / EX-C003-02 (Establish Domain Permission).

### Business Activity Contract (IMP-001 §6.7)

- **Business Intent:** Establish a Domain Permission as standing authority within a Domain, independent of any Business Role (URA-001-47/48), per EX-C003-02's stated Business Goal ("grant permanent, domain-scoped access without tying it to a Business Role that may change independently").
- **Input Contract:** `membership_id` (UUID, required — the Membership the grant is anchored to), `domain_id` (UUID, required — the target Domain, already established per AMD-014's `domain_registry`), `permission_level` (one of URA-001-47's eight values: VIEW/ENTER/EDIT/REVIEW/APPROVE/ASSIGN/DELEGATE/ADMIN), `effective_from`/`effective_to` (optional, URA-001-53).
- **Output Contract:** The established Domain Permission (id, membership_id, domain_id, permission_level, effective_from, effective_to, created_at, updated_at), or an HTTP error naming the specific violated rule.
- **Business Rules:**
  - BR-C003-01 — established only where the target Domain exists (404), the target Membership exists (404), `permission_level` is one of the eight canonical values (422, enforced by `DomainPermissionLevel` before the service layer is reached), and no currently-active grant of the identical (membership, domain, permission_level) triple already exists (409).
  - BR-C003-02 — a Domain Permission is never an implicit consequence of a Business Role (satisfied by construction: `DomainPermissionService.establish()` never reads or writes `roles`/`role_permissions`).
  - EX-C003-02's Domain Owner/Domain Admin authority requirement (URA-001-45/46). **Scoped simplification, same class as BA-01's BR-C003-08 disposition (IRA-002 §2.7):** gated on the existing `PLATFORM_ADMIN` role. Unlike BA-01 (where the gap is ADR-002's pending resolution of an existing-but-mismatched catalog), here no Domain Owner/Domain Admin relationship exists anywhere in the schema at all — Domain (AMD-014) was deliberately implemented as ownership-free reference data, a decision this Business Activity does not reopen. Stated explicitly, not a silent gap; registered as TD-022.
- **Validation Rules:** Domain existence and Membership existence checked before creation (404 each); duplicate-active-grant checked both at the service layer (pre-check, clean 409) and via `IntegrityError` handling for the concurrent-creation race, same pattern as `RoleService.establish()`/`OrganizationService.establish()`.
- **Authorization Rules:** `PLATFORM_ADMIN` role required (see the Business Rules disposition above; TD-022).
- **Domain Events:** `DOMAIN_PERMISSION_ESTABLISHED` (domain_permission_id, membership_id, domain_id, permission_level).
- **Audit Requirements:** `record_audit("ESTABLISH_DOMAIN_PERMISSION", ...)` on success and on every denial path (unknown domain, unknown membership, duplicate grant), per SD-002-054's seven audit questions — same mechanism reused as-is.
- **Tests:** `tests/test_domain_permission_service.py` (6 unit tests), `tests/test_domain_permission_api.py` (6 API/authorization tests) — 12 new tests, all passing; full suite (160 tests) passing with zero regressions.

---

## Governing Architecture Review (BA-02)

Reviewed: PE-001-C003 (ERB-C003-01, EX-C003-02, Chapter 5 Contracts 5.1/5.2/5.4/5.5, Chapter 7 Business Rules BR-C003-01/02/04, extracted and read directly from the docx's `word/document.xml`), URA-001 Section 4 (URA-001-43 through -56, Domain Ownership & Domain Permissions), `architecture/04-Technical/Master_Technical_Architecture.md` (`domain_permission_registry`, its FK completed by AMD-014, and `domain_registry` itself), IRA-002 (§2.1's live ADR-002 question — confirmed not applicable to BA-02, since Domain Permission does not touch the `roles`/`permissions` seed-catalog dispute at all; §2.2's BA-02 mapping and its explicit instruction that this Business Activity needs its own gap analysis before implementation), `IMP-REPORT-WP-02`'s own BA-01 precedent (duplicate-check-then-create, audit/event pattern, PLATFORM_ADMIN interim gate).

**Key finding requiring disclosure:** EX-C003-02's Entry Context requires confirming the proposing Person's Domain Owner or Domain Admin authority (URA-001-45/46) for the specific target Domain. No such relationship exists anywhere in this codebase — a direct consequence of Domain (AMD-014) being deliberately built as ownership-free reference/master data, a decision this Business Activity does not reopen (Domain architecture is frozen). Disposition: BA-02 gates on the existing `PLATFORM_ADMIN` dependency, the same interim-simplification class BA-01 already established for BR-C003-08, disclosed explicitly rather than silently assumed, and registered as TD-022.

---

## Gap Analysis Summary (BA-02)

- **Database:** New table required — `domain_permissions` did not exist anywhere in AuthService prior to this Business Activity (unlike BA-01's `roles`, which pre-existed from WP-00). This is not an architectural-impact escalation under CLAUDE.md §19.4: the schema shape is not invented here — it directly realizes Master Technical Architecture's own canonical `domain_permission_registry` (AMD-011, URA-001-47), whose FK to Domain was completed by the already-approved AMD-014 amendment. One new, purely additive migration (`e7f2b4a9c3d5`).
- **Business Activities:** BA-02's mapping to ERB-C003-01/EX-C003-02 was already derived in IRA-002 §2.2; this report performs the fresh, BA-02-specific gap analysis IRA-002 §2.2 stated would be required before implementation.
- **API Impact:** One new endpoint, `POST /domain-permissions`, mirroring `POST /roles`'s established shape (schema/repository/service/router layering, duplicate-check-then-create, audit/event emission), plus two existence-check dependencies (Domain, Membership) neither BA-01 nor WP-01 needed.
- **UI Impact:** Out of scope (backend Business Activity only, consistent with BA-01's own scope decision).
- **Dependencies:** `domain_registry` (AMD-014, already committed) and `memberships` (WP-00-era) — both consumed as pre-existing, unaltered tables; BA-02 adds rows to a new table only, never alters either dependency's shape.
- **Risks:** Domain Owner/Domain Admin authority gap (TD-022, above) — Low severity, same risk profile as TD-021, no privilege beyond what `PLATFORM_ADMIN` already holds platform-wide. Tenant-scoping: `/domain-permissions` is tenant-exempt (`middleware/tenant.py`), but for a narrower reason than `/roles`/`/domains` — a Domain Permission grant genuinely is organization-scoped data in the canonical architecture (`domain_permission_registry`'s own RLS policy scopes it via `membership_id -> organization_id`); the exemption holds only because `PLATFORM_ADMIN` is the sole caller today and already operates across every organization boundary elsewhere in this codebase, and should be revisited once TD-022 is resolved.
- **Technical Debt registered:** TD-022 (`architecture/06-Reviews/TECH-DEBT.md`).

---

## Documents Updated (BA-02)

**Architecture:**
- `architecture/05-Implementation/IMP-REPORT-WP-02_Role_Permission_Management.md` (this report, extended)
- `architecture/06-Reviews/TECH-DEBT.md` (TD-022 added)

**Implementation (new):**
- `Backend/Services/AuthService/alembic/versions/2026_07_27_1400-e7f2b4a9c3d5_domain_permission_registry.py`
- `Backend/Services/AuthService/models/domain_permission.py`
- `Backend/Services/AuthService/repositories/domain_permission_repository.py`
- `Backend/Services/AuthService/services/domain_permission_service.py`
- `Backend/Services/AuthService/schemas/domain_permission.py`
- `Backend/Services/AuthService/routers/domain_permission.py`
- `Backend/Services/AuthService/domain-permission-api.yaml`
- `Backend/Services/AuthService/tests/test_domain_permission_service.py`
- `Backend/Services/AuthService/tests/test_domain_permission_api.py`

**Implementation (modified, minimal):**
- `Backend/Services/AuthService/main.py` — registered the new `domain_permission` router at `/domain-permissions`.
- `Backend/Services/AuthService/models/__init__.py` — registered `DomainPermission`.
- `Backend/Services/AuthService/middleware/tenant.py` — added `/domain-permissions` to the tenant-exemption list, with the narrower rationale stated above (not the same basis as `/roles`/`/domains`).

No existing model, repository, service, or router was modified beyond the registrations above.

---

## Validation (BA-02)

- 12 new tests (6 unit, 6 API), all passing.
- Full AuthService suite: **160 passed**, zero regressions.
- Single, linear Alembic head confirmed (`e7f2b4a9c3d5`), purely additive migration.
- `domain-permission-api.yaml` confirmed to parse cleanly via `yaml.safe_load`.
- Confirmed `DomainPermissionService.establish()` never reads or writes `roles`/`role_permissions` (BR-C003-02, tested explicitly in `test_establish_never_touches_role_permissions`).
- Confirmed unknown Domain and unknown Membership each independently produce 404 (`test_establish_rejects_unknown_domain`, `test_establish_rejects_unknown_membership`).
- Confirmed a duplicate active (membership, domain, permission_level) grant is rejected with 409, while two distinct permission levels for the same pair both succeed (`test_establish_rejects_duplicate_active_grant`, `test_establish_allows_different_permission_levels_on_same_domain`).
- Confirmed non-`PLATFORM_ADMIN` callers receive 403 and an invalid `permission_level` receives 422 (`test_establish_domain_permission_rejects_non_platform_admin`, `test_establish_domain_permission_rejects_invalid_permission_level`).

---

## Independent Review (BA-02)

**Review Result:** APPROVED WITH OBSERVATIONS

**Review Summary:** An independent reviewer, with no prior involvement, re-ran the full test suite directly (160/160 passing), re-extracted PE-001-C003's docx independently, and traced BR-C003-01/BR-C003-02 through the actual `services/domain_permission_service.py` code rather than its docstring. Confirmed the Domain Owner/Domain Admin authority gap (URA-001-45/46) is genuine — no such relationship exists anywhere in the codebase — and judged the PLATFORM_ADMIN interim-gate disposition defensible, the same class as BA-01's own accepted TD-021 simplification. Confirmed the Alembic migration is single-headed and purely additive, and the OpenAPI contract parses and matches the implemented endpoint. Three findings were raised and are disposed of as follows:
1. **(Resolved by this update)** This report had not yet been extended to cover BA-02 at the time of review, and no BA-02-specific gap analysis existed as a discoverable artifact — the reviewer correctly flagged that CLAUDE.md §19.7's Business Activity Completion Gate requires the implementation-report/gap-analysis artifact to exist, not only the code and tests. This section is that artifact.
2. **(Resolved by this update)** TD-022 did not yet exist in `TECH-DEBT.md` at the time of review, despite the service docstring already citing it — added above, mirroring TD-021's detailed-entry format.
3. **(Resolved by this update)** The original `middleware/tenant.py` comment claimed the same tenant-exemption basis as `/roles`/`/domains`; the reviewer correctly noted `domain_permission_registry` is canonically organization-scoped data (via `membership_id`), a narrower case than Role's/Domain's genuinely-global-or-nullable scoping. The comment has been corrected to state the actual, narrower rationale (PLATFORM_ADMIN-only caller, revisit at TD-022 resolution) rather than implying an equivalent precedent.

No data-integrity, tenant-isolation, security, or build-breaking defect was found. The three findings above are documentation/registration-hygiene gaps, all closed by this same update, consistent with how BA-01's own single Minor finding (TD-021's missing registration) was resolved.

---

## Status (Combined)

**BA-01 — Establish Business or System Role:** Implementation COMPLETE. Independent Review APPROVED WITH OBSERVATIONS. Committed (`bca7f0b`, `178d07b`, `67e45c9`, `0258d6c`).

**BA-02 — Establish Domain Permission:** Implementation COMPLETE. Independent Review APPROVED WITH OBSERVATIONS (all three findings resolved in this same update — see above). Repository Commit: Pending (this update, including code, tests, TECH-DEBT.md TD-022, and this report section, is being committed together).

**Current Repository Status:** BA-01 and BA-02 remain committed to `master` as previously recorded. BA-03's implementation, TECH-DEBT.md's TD-023 entry, and this report's BA-03 sections are new since BA-02's last commit and are being committed together as one unit. Unrelated pre-existing working-tree changes (`CLAUDE.md`, `architecture/06-Reviews/ARM-001_Implementation_Report.md`, and the frozen Enterprise-AI-Audit-remediation documents, including the frozen ARM-002 diff sitting inside `Master_Technical_Architecture.md` at its own, separate version-history entry) remain outside WP-02's scope and are not part of this commit.

---

## BA-03 — Establish Approval Authority

Realizing PE-001-C003's ERB-C003-01 (Define Authorization Policy Structure) / EX-C003-03 (Establish Approval Authority).

### Business Activity Contract (IMP-001 §6.7)

- **Business Intent:** Establish an Approval Authority as a first-class object independent of Business Role, declaring exactly one approval strategy and exactly one scope (URA-001-61/62), per EX-C003-03's stated Business Goal ("define who or what group must approve a class of decision, without conflating that authority with a business title").
- **Input Contract:** `organization_id` (UUID, required — for every scope, including GLOBAL/COMPANY), `authority_name` (required, 1–255 chars), `approval_strategy` (one of ANY_ONE/ALL/MAJORITY/SEQUENTIAL, URA-001-42/62), `majority_threshold_pct` (optional, 0–100, URA-001-82), `scope_type` (one of GLOBAL/COMPANY/DOMAIN/OBJECT, URA-001-61), `domain_id` (required iff scope_type=DOMAIN), `object_type`/`object_id` (required iff scope_type=OBJECT).
- **Output Contract:** The established Approval Authority (id, organization_id, authority_name, approval_strategy, majority_threshold_pct, scope_type, domain_id, object_type, object_id, created_at, updated_at), or an HTTP error naming the specific violated rule.
- **Business Rules:**
  - BR-C003-01 — established only where the target Organization exists (404), and where scope_type=DOMAIN, the target Domain exists (404); scope_type/domain_id/object_type/object_id's mutual consistency is validated before the service layer is ever reached (422).
  - EX-C003-03's Corporate Admin/Domain Owner authority requirement (URA-001-32/45). **Scoped simplification, same class as BA-01/BA-02's disposition:** gated on the existing `PLATFORM_ADMIN` role, since neither authority exists as a distinct, enforceable claim today. Stated explicitly, not a silent gap; registered as TD-023.
- **Validation Rules:** scope_type's anchor consistency enforced at three independent layers — Pydantic `model_validator` (422, `schemas/approval_authority.py`), a database CHECK constraint (`ck_approval_authorities_scope_consistency`), and existence checks for Organization/Domain (404). Exactly one of four combinations is ever valid: GLOBAL/COMPANY (organization_id only), DOMAIN (+ domain_id), OBJECT (+ object_type and object_id) — every other combination is rejected.
- **Authorization Rules:** `PLATFORM_ADMIN` role required (see the Business Rules disposition above; TD-023).
- **Domain Events:** `APPROVAL_AUTHORITY_ESTABLISHED` (approval_authority_id, organization_id, authority_name, approval_strategy, scope_type, domain_id, object_type, object_id).
- **Audit Requirements:** `record_audit("ESTABLISH_APPROVAL_AUTHORITY", ...)` on success and on every denial path (unknown organization, unknown domain), per SD-002-054's seven audit questions — same mechanism reused as-is.
- **Tests:** `tests/test_approval_authority_schema.py` (13 unit tests, scope-consistency matrix), `tests/test_approval_authority_service.py` (6 unit tests), `tests/test_approval_authority_api.py` (8 API/authorization tests) — 27 new tests, all passing; full suite (187 tests) passing with zero regressions.

---

## Governing Architecture Review (BA-03)

Reviewed: PE-001-C003 (ERB-C003-01, EX-C003-03, Chapter 7 BR-C003-01, extracted and read directly from the docx's `word/document.xml`), URA-001 Section 3 (URA-001-32, Corporate Admin) and Section 4 (URA-001-42, -45, -61, -62, -82), `architecture/04-Technical/Master_Technical_Architecture.md` (`approval_authority_registry`, already canonical from AMD-011), IRA-002 (§2.2's BA-03 mapping), `IMP-REPORT-WP-02`'s own BA-01/BA-02 precedent.

**Key finding requiring disclosure, verified before any implementation:** `approval_authority_registry` as it existed prior to this Business Activity had no `scope_type` column and no Domain/Object anchor at all, despite URA-001-61 and EX-C003-03 both requiring an Approval Authority to declare exactly one of GLOBAL/COMPANY/DOMAIN/OBJECT scope as an explicit attribute ("declaring exactly one approval strategy and one scope"; Success Criteria: "never... without exactly one declared strategy and exactly one declared scope"). This was surfaced as a genuine stop condition (schema change requiring architectural approval) before any code was written, verified against the primary canonical text with the user, and explicitly approved: scope_type is stored, never inferred, because GLOBAL and COMPANY share an identical anchor pattern (organization_id set, every other anchor NULL) once organization_id is required for every scope — the two would be genuinely indistinguishable without their own discriminator. `architecture/04-Technical/Master_Technical_Architecture.md` was updated (v6.9) to add `scope_type`, `domain_id`, `object_type`, `object_id`, and a scope-consistency CHECK constraint to the existing canonical table — reusing `approval_strategy`'s own enum-column convention, `domain_permission_registry`'s own FK convention, `runtime_assignment_registry`'s own polymorphic-anchor convention, and `industry_taxonomy_registry`'s own conditional-CHECK-constraint convention. No new architectural style was introduced.

---

## Gap Analysis Summary (BA-03)

- **Database:** New table required — `approval_authorities` did not exist anywhere in AuthService prior to this Business Activity. One new, purely additive migration (`b8d3f6a1c4e2`), plus the architecture completion above (four new columns + one CHECK constraint on the canonical `approval_authority_registry`, `organization_id` widened to NOT NULL — no existing table's data is affected, since no prior Business Activity had created any row in it).
- **Business Activities:** BA-03's mapping to ERB-C003-01/EX-C003-03 was already derived in IRA-002 §2.2; this report performs the fresh, BA-03-specific gap analysis IRA-002 §2.2 stated would be required.
- **API Impact:** One new endpoint, `POST /approval-authorities`, mirroring `POST /domain-permissions`'s established shape (schema/repository/service/router layering, existence-check-then-create, audit/event emission), plus request-layer scope-consistency validation as a new (but pattern-reusing) validation concern.
- **UI Impact:** Out of scope (backend Business Activity only, consistent with BA-01/BA-02's own scope decision).
- **Dependencies:** `organizations` (WP-00-era) and `domains` (AMD-014) — both consumed as pre-existing, unaltered tables; BA-03 adds rows to a new table only.
- **Risks:** Corporate Admin/Domain Owner authority gap (TD-023) — Low severity, same risk profile as TD-021/TD-022. Tenant-scoping: `/approval-authorities` is tenant-exempt (`middleware/tenant.py`), same narrower rationale as `/domain-permissions` — `organization_id` is genuinely required/real data, but `PLATFORM_ADMIN` is the sole caller today and already operates across every organization boundary elsewhere in this codebase.
- **Latent defect found and fixed (not a new feature):** `main.py`'s `validation_exception_handler` failed with an unhandled `TypeError` when a Pydantic `@model_validator` raises a plain `ValueError` (a completely standard Pydantic idiom), because `exc.errors()` embeds the raw, non-JSON-serializable exception instance in each error's `ctx` field. This was a pre-existing bug in shared code, never triggered before because no prior schema used a custom `model_validator`. Fixed by stripping `ctx` from each error dict before serialization (the human-readable `msg` field is unaffected). Confirmed no existing test asserts on `ctx`'s presence in a 422 response body.
- **Technical Debt registered:** TD-023 (`architecture/06-Reviews/TECH-DEBT.md`).

---

## Documents Updated (BA-03)

**Architecture:**
- `architecture/04-Technical/Master_Technical_Architecture.md` (v6.8 → v6.9: `approval_authority_registry` scope completion)
- `architecture/05-Implementation/IMP-REPORT-WP-02_Role_Permission_Management.md` (this report, extended)
- `architecture/06-Reviews/TECH-DEBT.md` (TD-023 added)

**Implementation (new):**
- `Backend/Services/AuthService/alembic/versions/2026_07_27_1600-b8d3f6a1c4e2_approval_authority_registry.py`
- `Backend/Services/AuthService/models/approval_authority.py`
- `Backend/Services/AuthService/repositories/approval_authority_repository.py`
- `Backend/Services/AuthService/services/approval_authority_service.py`
- `Backend/Services/AuthService/schemas/approval_authority.py`
- `Backend/Services/AuthService/routers/approval_authority.py`
- `Backend/Services/AuthService/approval-authority-api.yaml`
- `Backend/Services/AuthService/tests/test_approval_authority_schema.py`
- `Backend/Services/AuthService/tests/test_approval_authority_service.py`
- `Backend/Services/AuthService/tests/test_approval_authority_api.py`

**Implementation (modified, minimal):**
- `Backend/Services/AuthService/main.py` — registered the new `approval_authority` router at `/approval-authorities`; fixed the pre-existing `validation_exception_handler` `ctx`-serialization defect (see Gap Analysis above).
- `Backend/Services/AuthService/models/__init__.py` — registered `ApprovalAuthority`.
- `Backend/Services/AuthService/middleware/tenant.py` — added `/approval-authorities` to the tenant-exemption list, same narrower rationale as `/domain-permissions`.

No existing model, repository, service, or router was modified beyond the registrations and the one bug fix above.

---

## Validation (BA-03)

- 27 new tests (13 schema, 6 service, 8 API), all passing.
- Full AuthService suite: **187 passed**, zero regressions.
- Single, linear Alembic head confirmed (`b8d3f6a1c4e2`), purely additive migration (creates one new table only).
- `approval-authority-api.yaml` confirmed to parse cleanly.
- Confirmed all four valid scope combinations (GLOBAL, COMPANY, DOMAIN, OBJECT) establish correctly (`test_establish_global_scope`, `test_establish_company_scope`, `test_establish_domain_scope`, `test_establish_object_scope`).
- Confirmed every invalid combination is rejected: missing required anchor (DOMAIN without domain_id, OBJECT without object_type/object_id), and dual-stated/ambiguous anchors (GLOBAL or COMPANY with any anchor set, DOMAIN or OBJECT with the other scope's anchor also set) — all at the schema layer (422) and re-enforced by the database CHECK constraint.
- Confirmed unknown Organization and unknown Domain (for DOMAIN scope) each independently produce 404.
- Confirmed non-`PLATFORM_ADMIN` callers receive 403.

---

## Independent Review (BA-03)

**Review Result:** APPROVED WITH OBSERVATIONS

**Review Summary:** An independent reviewer, with no prior involvement, re-ran the full test suite directly (187/187 passing), re-extracted PE-001-C003's docx independently, and manually traced the `ck_approval_authorities_scope_consistency` CHECK constraint's boolean logic against all four scope_type values, confirming it is exhaustive (no combination falls through to satisfying none or multiple branches) and matches the Pydantic `model_validator` exactly. Independently re-derived the scope_type-must-be-explicit conclusion against EX-C003-03's own text and confirmed it holds. Confirmed the `main.py` ctx-stripping fix addresses a real, pre-existing latent bug, with no existing test depending on `ctx`'s presence. Confirmed no Corporate Admin/Domain Owner authority model exists anywhere in the codebase, and the PLATFORM_ADMIN interim gate is disclosed, not silent. Three findings were raised and are disposed of as follows:
1. **(Resolved by this update)** A leftover scratch docx-extraction file (`_pe001c003_scope_check.txt`) was left in the working tree, contrary to this repository's own scratch-file-cleanup convention — deleted.
2. **(Resolved by this update)** The scope_type rationale, as originally worded in three places (`models/approval_authority.py`, the migration docstring, and Master Technical Architecture's v6.9 entry), overstated the source of ambiguity — it attributed it to "a Domain-scoped authority still belongs to one organization_id," when DOMAIN is in fact trivially distinguishable from GLOBAL/COMPANY by `domain_id`'s own presence. The genuine ambiguity is GLOBAL vs. COMPANY specifically, which share an identical anchor pattern once `organization_id` is required for every scope. The conclusion (explicit `scope_type` column required) was correct throughout; only the stated reasoning was imprecise. Corrected in all three locations.
3. **(Informational, not actioned)** `majority_threshold_pct` has no conditional tie to `approval_strategy == MAJORITY` — a pre-existing gap in the canonical registry that predates this Business Activity and is outside its purely-additive scope; not registered as new technical debt, consistent with the instruction to register only genuine debt this Business Activity itself introduces or discovers as blocking, not speculative future enhancements.

No data-integrity, tenant-isolation, security, or build-breaking defect was found.

---

## Status (Combined)

**BA-01 — Establish Business or System Role:** Implementation COMPLETE. Independent Review APPROVED WITH OBSERVATIONS. Committed (`bca7f0b`, `178d07b`, `67e45c9`, `0258d6c`).

**BA-02 — Establish Domain Permission:** Implementation COMPLETE. Independent Review APPROVED WITH OBSERVATIONS (all findings resolved). Committed (`31ed253`, `5655b2f`).

**BA-03 — Establish Approval Authority:** Implementation COMPLETE. Independent Review APPROVED WITH OBSERVATIONS (all three findings resolved in this same update — see above). Repository Commit: Pending (implementation and documentation being committed separately, per instruction).

**Current Repository Status:** BA-01 and BA-02 remain committed to `master`. BA-03's implementation (10 new files, 3 minimally-modified files, one architecture completion to `Master_Technical_Architecture.md`), TECH-DEBT.md's TD-023 entry, and this report's BA-03 sections are new since BA-02's last commit. Unrelated pre-existing working-tree changes (`CLAUDE.md`, `architecture/06-Reviews/ARM-001_Implementation_Report.md`, the frozen Enterprise-AI-Audit-remediation documents, and the frozen ARM-002 diff sitting inside `Master_Technical_Architecture.md` at its own separate version-history entry) remain outside WP-02's scope and are not part of this commit.

---

*Per instruction: BA-04 has not been started. Awaiting explicit approval before proceeding.*
