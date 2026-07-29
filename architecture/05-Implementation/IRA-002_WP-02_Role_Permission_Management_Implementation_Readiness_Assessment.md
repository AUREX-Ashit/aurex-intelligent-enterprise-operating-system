# IRA-002 — WP-02 Implementation Readiness Assessment
### Role & Permission Management (C-003)

**Status:** Approved — WP-02 READY (BA-01 only; BA-02 onward re-assessed per Business Activity, per the Business Activity Completion Gate, CLAUDE.md §19.7)
**Classification:** Implementation Readiness Assessment (canonical IRA template, per IRA-001)
**Work Package:** WP-02 — Role & Permission Management (C-003)
**Governing capability specification:** `PE-001-C003_Role_Permission_Management.docx` (extracted and reviewed in full — Version 1.0, Initial Gold Standard Engineering Pass). Three canonical ERBs: ERB-C003-01 (Define Authorization Policy Structure), ERB-C003-02 (Govern Authorization Policy Lifecycle), ERB-C003-03 (Resolve Authorization Policy Dependency Conflict and Cross-Capability Hand-off). Ten Enterprise Experiences (EX-C003-01 through 10). Every Business Activity/EAC binding in PE-001-C003 is recorded as Pending Canonical Binding — no canonical BA identifier exists yet; this document derives the Business Activity list, following the same discipline WP-01 applied for PE-001-C004.
**Documents reviewed:** CLAUDE.md, ARCH-000, CAP-001 (§2 Registry, C-003 entry), URA-001 (Sections 3–7: System/Business Roles, Domain Ownership & Domain Permissions, Groups & Approval Authorities, Event Architecture & Runtime Assignment Model, Delegation/Escalation/Exception Management), RTA-001 §11 (Authorization Runtime — 11.2 Authorization Engine sole runtime authority, 11.16 Authorization Governance, 11.17 URA-001/RTA-001 division of labor), IMP-001 (Business Activity Registry — no canonical C-003 BA/EAC identifier found, confirmed Pending Canonical Binding), SD-002 / SD-003 (Universal Business Object and Interaction principles, URA-001-01a boundary), ADR-001 through ADR-005 (all reviewed; ADR-002 is directly relevant — see §2.1 below), IRA-001 (precedent format and explicit exclusion of C-003 from WP-01's scope), IMP-REPORT-WP-01 (precedent Business Activity implementation pattern), current AuthService repository structure (`models/role.py`, `models/permission.py`, `models/role_permission.py` — already exist; no repository/service/router/schema/tests yet).

---

## 1. Executive Summary

WP-02 is **READY** to begin implementation, for **BA-01 only**.

One live, unresolved architectural question — **ADR-002 (Proposed, not Accepted)** — directly touches the `roles`/`permissions` schema this Business Activity will use. It does not block BA-01 as scoped below (establishing a governed Role structure, independent of any specific seed-catalog naming decision), but it **does** constrain BA-01's authorization gate (see §2.1 and §2.7) and will need resolution before later Business Activities (Domain Permission, Approval Authority, Delegation Policy establishment) can fully realize PE-001-C003's persona-specific defining-authority model (BR-C003-08).

Per the Business Activity Completion Gate (CLAUDE.md §19.7), only BA-01 is implemented under this IRA. BA-02 through BA-10 (mapped in §2.2) each require their own gap check before implementation begins, consistent with how WP-01 proceeded one Business Activity at a time.

---

## 2. Readiness Assessment

### 2.1 Capability Assessment

- **Primary Capability:** C-003 Role & Permission Management (CAP-001) — Primary Specification **URA-001** (Sections 3–7), Business Intent "Manage authorization roles and permissions." (verbatim).
- **Runtime Execution Boundary Authority:** RTA-001 §11 (Authorization Engine) — consulted only to confirm C-003 never crosses into runtime decision execution (RTA-001-11.2: "the Authorization Engine is the sole authority for runtime authorization decisions"). C-003 defines authorization *structure*; it never evaluates whether a specific request is currently permitted.
- **Upstream Dependencies (consumed, never redefined):** C-001 (Identity Context), C-007 (Membership Context and defining authority), C-004 (Organization/Domain anchor, referenced only), C-008 (Workspace, referenced only).
- **Principal Downstream Capability:** C-002 (Access Management) — the sole consumer of every authorization policy object C-003 produces; C-002's own Access Evaluation Outcome and evaluation logic are never redefined here.
- **Excluded from this capability (PE-001-C003 §1.5, Out of Scope):** Identity, Person, Membership, Organization, Workspace ownership; whether any specific request is currently permitted; the Authorization Engine's own runtime decision logic, policy language, claims format, or token structure; any specific runtime instance of a delegation/assignment (an operational act under URA-001 §§6–7, not an Enterprise Experience this capability hosts).

#### Live Architectural Question Requiring Disclosure (ADR-002)

**ADR-002 — Reconcile AuthService Seed Role Catalog with MDP-001/URA-001** is **Proposed, not Accepted**. It records a genuine, unresolved conflict:

- The existing `roles` table (already in the schema, seeded by WP-00) is a single, undifferentiated catalog: `PLATFORM_ADMIN, ORG_ADMIN, ESG_MANAGER, AUDITOR, SUPPLIER_ADMIN, BOARD_MEMBER`, distinguished only by an `is_system_role` boolean column.
- URA-001/MDP-001's canonical model specifies two **separate** registries — `system_role_registry` (5 fixed rows: `AUREX_ADMIN, CORPORATE_ADMIN, USER_ADMIN, SECURITY_ADMIN, DOMAIN_ADMIN`) and `business_role_registry` (named examples: `CEO, CFO, COO, CHRO, CSO, CISO, Company Secretary, Finance Manager, Plant Head, Board Member`) — and the seeded catalog's actual codes do not match either registry's names.
- This ADR explicitly states the decision is "outside an AuthService implementation task's authority (CLAUDE.md §18/§19.4)" and has not been made.

**Disposition for BA-01:** BA-01 (Establish Business or System Role) is scoped to build the *mechanism* — a governed, validated act of creating a new Role row of a stated type — not to decide, seed, or rename any specific canonical role. It reuses the existing `roles` table's `is_system_role` discriminator as-is (already a defensible, minimal realization of URA-001-03's "System Roles and Business Roles remain independent" at the schema level) and does **not** touch the seed catalog (`scripts/03_seed_r001_data.sql`, `scripts/bootstrap_data.py`) — modifying that would itself be resolving ADR-002, which this implementation task is not authorized to do. This scoping keeps BA-01 correct today regardless of which ADR-002 option governance eventually selects. See §8 (Risks) and §12 (Technical Debt) for what this means for later Business Activities.

### 2.2 Business Activity Assessment

Per IMP-001 §1.7 ("Business Activities Over CRUD") and following the same ERB→EX→BA derivation discipline WP-01 applied for PE-001-C004 (no canonical BA identifier exists in PE-001-C003 — every reference is "Pending Canonical Binding"), the ten Enterprise Experiences map to ten proposed Business Activities:

| Business Activity | Type | Business Object | Governing ERB / EX | Status |
|---|---|---|---|---|
| **BA-01 — Establish Business or System Role** | Create | Role | ERB-C003-01 / EX-C003-01 | ✅ **Implemented under this IRA** |
| BA-02 — Establish Domain Permission | Create | Permission (Domain-anchored) | ERB-C003-01 / EX-C003-02 | ⏳ Not started |
| BA-03 — Establish Approval Authority | Create | (new object type — no existing model) | ERB-C003-01 / EX-C003-03 | ⏳ Not started |
| BA-04 — Establish Delegation Policy | Create | (new object type — no existing model) | ERB-C003-01 / EX-C003-04 | ⏳ Not started |
| BA-05 — Establish Runtime Assignment Policy | Create | (new object type — no existing model) | ERB-C003-01 / EX-C003-05 | ⏳ Not started |
| BA-06 — Produce Rejected/Unresolved Definition Outcome | Cross-cutting (realized inline by BA-01–05, not a standalone endpoint) | n/a | ERB-C003-01 / EX-C003-06 | ⏳ Realized inline in BA-01 (see §2.9) |
| BA-07 — Version and Re-effective-Date Authorization Policy Object | Update | Role / Permission / etc. | ERB-C003-02 / EX-C003-07 | ⏳ Not started |
| BA-08 — Deprecate or Retire Authorization Policy Object | Update (state transition) | Role / Permission / etc. | ERB-C003-02 / EX-C003-08 | ⏳ Not started |
| BA-09 — Detect and Resolve Authorization Policy Dependency Conflict | Query + Update | Role / Permission / etc. | ERB-C003-03 / EX-C003-09 | ⏳ Not started |
| BA-10 — Resolve Dependent Capability Hand-off Rejection | Update (classification) | n/a | ERB-C003-03 / EX-C003-10 | ⏳ Not started |

**Only BA-01 is implemented under this IRA**, per the explicit Step 3 instruction and the Business Activity Completion Gate (CLAUDE.md §19.7). BA-02 through BA-10 each require Domain Permission, Approval Authority, Delegation Policy, and Runtime Assignment Policy object types — none of which have an existing database model (`role.py`/`permission.py`/`role_permission.py` cover only Role and a flat Permission concept, not URA-001's fuller Domain Permission/Approval Authority/Delegation Policy/Runtime Assignment Policy shapes) — each will need its own gap analysis before implementation, likely surfacing its own architectural-impact questions (new tables/columns), which CLAUDE.md §18/§19.4 would require to be raised explicitly at that time, not assumed now.

### 2.3 Architecture Impact

**None for BA-01.** No new entity, table, column, API contract shape, or business rule beyond what URA-001/PE-001-C003 already establish. `roles` table already exists (WP-00-era migration `8fac154e79e2_initial_r001_schema.py`); BA-01 adds only application-layer code (schema, repository, service, router, tests) consuming it as-is. This satisfies BR-C003-01 (structural rule + defining-authority confirmation before establishment) and BR-C003-02 (no automatic permission grant — trivially true, since `establish()` never touches `role_permissions`).

### 2.4 Backend Impact

New files only, mirroring WP-01's Organization Management pattern exactly (Reuse before Create — no new pattern invented):
- `schemas/role.py` (`EstablishRoleRequest`, `RoleResponse`)
- `repositories/role_repository.py` (`RoleRepository(BaseRepository[Role])`, `get_by_code()`)
- `services/role_service.py` (`RoleService.establish()`)
- `routers/role.py` (`POST /roles`)
- `main.py` — register the new router
- `middleware/tenant.py` — add `/roles` to the tenant-exemption list (Roles are platform-global, no `organization_id` column, same basis as `/organizations`)

### 2.5 Frontend Impact

Out of scope for BA-01 per the Step 3 instruction ("Implement ONLY BA-01" — backend Business Activity only, no UI deliverable requested). No DS-001/SD-001 gap identified in principle (an "Establish Role" form is the same Guided Completion pattern WP-01 already used for Establish Organization) — deferred to a future frontend-scoped pass.

### 2.6 Database Impact

**None.** `roles` table already exists with the exact columns BA-01 needs (`role_code`, `role_name`, `description`, `is_system_role`, `created_at`, `updated_at`). No migration required.

### 2.7 Security Assessment

- **Authentication:** N/A — rides on AuthService's existing JWT bearer auth (unchanged).
- **Authorization:** BR-C003-08 requires confirmed, type-specific defining authority (Corporate Admin for Business Roles; Security Admin or User Admin for System Roles). **No such differentiated authority is implementable today** — only `PLATFORM_ADMIN` exists as an enforced role claim (`dependencies.require_platform_admin`), and ADR-002 (§2.1) has not resolved whether/how `CORPORATE_ADMIN`/`SECURITY_ADMIN`/`USER_ADMIN` map onto the actual seed catalog. **Disposition, mirroring IRA-001 §2.7's precedent exactly:** BA-01 gates both Business Role and System Role establishment on the existing `require_platform_admin` dependency, as a stated, deliberate simplification — not a silent gap — pending ADR-002's resolution and the persona-specific authority model it would unlock.
- **Roles/Permissions:** BA-01 creates Role rows; it does not touch `role_permissions` (Permission assignment is a separate, later Business Activity — BA-02 realizes Domain Permission establishment, and Permission *assignment* to a Role is not part of any ERB-C003-01 EX at all — it is a distinct, not-yet-mapped concern).
- **Audit:** `observability.py`'s `record_audit`/`publish_event` (WP-00/WP-01's established mechanism) — reused as-is, no new mechanism.
- **Encryption:** No field requires field-level encryption beyond standard transport/at-rest DB encryption (unchanged from AuthService baseline).

### 2.8 Integration Assessment

- **Internal Services:** `Membership.role_id` already FK-references `roles.id` (WP-00-era) — BA-01 must not break this; it only adds new rows, never alters the table shape.
- **External Systems / Events / Notifications:** None identified for BA-01.

### 2.9 Vertical Slice Assessment

Complete slice achievable: DB (existing) → Repository → Service → Router → Tests → Observability, mirroring WP-01's Establish Organization slice exactly. The Rejected/Unresolved outcome (EX-C003-06, BA-06 in §2.2) is realized *inline* within BA-01's own service method (a 409 on duplicate `role_code`), not as a separate endpoint — consistent with how WP-01 realized rejection outcomes inline within `establish()` rather than as a standalone Business Activity.

### 2.10 Testing Strategy

Same as IRA-001 §2.10: IMP-TEST-001 (Business Activity Contract tests) as primary layer, IMP-TEST-002 (Authorization Boundary tests, constrained by §2.7's simplification). Unit tests (`test_role_service.py`) and API/integration tests (`test_role_api.py`), using the existing `tests/conftest.py` SQLite-in-memory pattern — no new test infrastructure.

### 2.11 Deployment Assessment

- **Migration:** None (§2.6).
- **Rollback:** N/A — no schema change.
- **Backward Compatibility:** No existing column, constraint, or relationship is altered; `Membership.role_id`'s FK target is untouched.

### 2.12 Risks

See Risk Register (§8).

### 2.13 Implementation Plan

BA-01 only, this IRA. BA-02 onward each require a fresh gap analysis before implementation (§2.2).

### 2.14 Success Criteria

- BA-01 has a full Business Activity Contract per IMP-001 §6.7 (Business Intent, Input/Output Contract, Business Rules, Validation Rules, Authorization Rules, Domain Events, Audit Requirements, Tests).
- BR-C003-01, BR-C003-02, and BR-C003-08 (as scoped by §2.7's stated simplification) are satisfied and tested.
- No new database table, column, or architecture invented — Reuse-before-Create fully honored.
- ADR-002's live status and BA-01's specific disposition relative to it are disclosed, not silently assumed resolved.

---

## 3. Risk Register

| Risk | Severity | Mitigation |
|---|---|---|
| ADR-002 remains unresolved indefinitely, and a later Business Activity (e.g., BA-02 Domain Permission) needs the System/Business Role split BA-01 deliberately avoided deciding | Medium | Flagged explicitly in this IRA (§2.1); recommend escalating ADR-002 for architecture governance decision before BA-02 begins, not before BA-01 (BA-01 does not need it resolved) |
| BA-01's authorization gate (`PLATFORM_ADMIN`, not persona-specific) does not yet realize BR-C003-08's full defining-authority model | Low (documented simplification, same class as IRA-001 §2.7's precedent) | Same disposition WP-01 already used successfully; revisit once ADR-002 resolves and real `CORPORATE_ADMIN`/`SECURITY_ADMIN`/`USER_ADMIN` claims exist |
| `role_code`/`role_name` collision with an eventual ADR-002 rename (e.g., if `PLATFORM_ADMIN` is renamed `AUREX_ADMIN` under ADR-002 Option A) | Low | BA-01 does not seed or rename any row; new roles established via BA-01 use whatever codes their proposing admin supplies, unaffected by a future rename of the pre-existing seed catalog |

---

## 4. Technical Debt Inherited from WP-01

- **`dependencies.require_platform_admin`'s own docstring** (written during WP-01) explicitly anticipates this work package: *"This checks only the existing, WP-00-seeded PLATFORM_ADMIN role_code claim — not Domain Permissions (URA-001 §4 VIEW/EDIT/APPROVE/etc.), which belong to the separate, not-yet-built Role & Permission Management work package."* BA-01 continues reusing this same interim gate rather than resolving it, since resolving it requires the persona-specific authority model that itself depends on ADR-002 (§2.1) — this is not new debt BA-01 introduces, it is the exact debt WP-01 flagged in advance, now confirmed still open at the start of the work package meant to close it.
- **ADR-002** (§2.1) is unchanged technical debt from before WP-01 — not created by this IRA, but directly relevant to this work package's later Business Activities.

---

**Governing document status:** This IRA does not create any ADR, does not modify architecture, and does not resolve ADR-002. It records BA-01's scope as not requiring that resolution, and flags the point at which a future Business Activity will.
