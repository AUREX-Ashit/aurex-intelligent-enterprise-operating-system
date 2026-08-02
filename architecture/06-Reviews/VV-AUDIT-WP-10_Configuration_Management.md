# VV-AUDIT-WP-10 — Independent Verification & Validation Audit: Configuration Management (C-041)

**Work Package:** WP-10 — Configuration Management (C-041)
**State audited:** working tree at time of review (BA-01/BA-02 "Implementation Complete," remediated, Gate-4-verified — not yet committed, per `IMP-REPORT-WP-10`)
**Reviewer:** Independent, fresh-context reviewer — no prior involvement in WP-10's implementation, `CERT-WP-10`'s own Gate 1 Certification, the remediation, or `CERT-WP-10_Remediation_Verification`'s own Gate 4
**Gate:** 2 of 5 (`CLAUDE.md §19.7b`) — a broader, more exhaustive mandate than Gate 1/Gate 4, per this document's own method requirement (a Requirements Traceability Matrix, exhaustive specification-conformance checking, and from-scratch runtime probes per defect class, not adapted from the existing test suite)
**Determination:** **PASS WITH OBSERVATIONS** — no `CLAUDE.md §19.8.5`-class defect found (security, tenant-isolation, data-integrity, failing test, build failure, or broken functionality). Four new, previously-undetected, non-blocking findings registered as Technical Debt below.

---

## Governing Documents Reviewed (Primary Text, Independently)

`IRA-010_WP-10_...md` (full); `CMD-001_Canonical_Data_Model.md` §12.1–§12.12 (Configuration & Policy Data Architecture, full text) and §26.3a/§26.4 (Eligibility Test, Registration Structure, full text); `ADR-019`; `IMP-REPORT-WP-10_Configuration_Management.md`; `CERT-WP-10_Configuration_Management.md` (Gate 1); `CERT-WP-10_Remediation_Verification.md` (Gate 4); `TECH-DEBT.md` `TD-115`–`TD-118` and (for the FK-parity checklist) `TD-096`; `DS-001 — AUREX Design System.md` Chapter 11 (§11.3, §11.7 — `DS-001-183`–`197`, full text, not summarized); `SD-001 — Enterprise Presentation Architecture.md` `SD-001-063`; `SD-002_Universal_Business_Object_Rules.md` §10 (`SD-002-077`–`085`, full text); `CLAUDE.md` §12–§21, specifically §19.8.5, §19.8.7, §20, §21.4; `CBOR-INDEX.md` §3; `WP-REG-001`, `DOC-000` (WP-10 rows).

All backend source files under WP-10's own change surface read in full (`models/configuration_entry.py`, `repositories/configuration_entry_repository.py`, `services/configuration_management_service.py`, `services/configuration_resolution_service.py`, `routers/configuration.py`, `schemas/configuration.py`, `dependencies.py`, `middleware/tenant.py`, the Alembic migration, all three test files) and every frontend file under the same surface (`useResolvedTheme.ts`, `useConfigurationManagement.ts`, `ConfigurationManagementScreen.tsx`, `EstablishConfigurationSection.tsx`, `ConfigurationEntriesSection.tsx`, `configuration-api.ts`, `api-client.ts`, `providers.tsx`, `AdminShell.tsx`, `theme.css`).

---

## Independent Re-Verification

- **Full backend regression suite**, re-run from scratch: `JWT_SECRET_KEY=test-secret ./venv/Scripts/python.exe -m pytest tests/ -q` → **743 passed, 0 failed** (509s). Matches `CERT-WP-10_Remediation_Verification`'s own claimed 743/743 exactly.
- **Frontend:** `npx tsc --noEmit` → 0 errors. `npx eslint src` → 5 problems (4 errors, 1 warning) — none in WP-10's own `src/features/configuration/**` or any WP-10-modified file; confirmed via `git status --short` that both affected directories (`src/features/organization/**`, `src/features/domain-permission/**`) have zero pending WP-10 changes. **Minor accuracy footnote (no action required, mirrors `CERT-WP-10`'s own G2-2 footnote discipline):** `CERT-WP-10` characterized all 5 problems as being in `src/features/organization/**`; one of the four errors (`useSearchDomainPermissions.ts:61`) is actually in `src/features/domain-permission/**`. Does not change the conclusion (still 0 problems introduced by WP-10, still all pre-existing/untouched).
- **Business Object Eligibility (`CMD-001 §26.3a`)**, re-derived independently from the primary text: Step 1 (Independent Identity) — satisfied, a `ConfigurationEntry` row is written by one BA-02 call and read by identity in an unrelated BA-01 call. Step 2 (Cross-Experience Reference Test) — satisfied, BA-01 is "a construct retrieved, by identity, from a separately-invoked later Business Activity," the exact satisfying language. Step 3 (Governed Lifecycle) — satisfied, `ACTIVE → SUPERSEDED` with `effective_to` set and the prior row retained is a real, persisting, later-invalidated lifecycle. Result: eligible, matching `IRA-010 §6`/`ADR-019`. The "one family, not five" registration shape is sound — the five in-scope facets share identical identity structure (Scope+Facet+Key), lifecycle mechanics, and resolution algorithm.
- **`CBOR-INDEX.md`**: `CFG-000001` row present, correctly attributed. `AEO-000001`'s incidental correction is correctly attributed and does not reopen `ADR-015`.

---

## Requirements Traceability Matrix

| Requirement (source) | Traced to | Status |
|---|---|---|
| Versioning (`CMD-001 §12.5`) | `ConfigurationEntry.version`, monotonic increment in `establish()` | ✓ Implemented, tested (`test_establish_again_supersedes_prior_active_version`) |
| Effective Dating (`§12.5`) | `effective_from`/`effective_to` | ✓ Implemented, tested |
| Lifecycle State (`§12.5`) | `ConfigurationLifecycleState` (ACTIVE/SUPERSEDED/RETIRED) | ⚠ **Partially reachable** — only ACTIVE→SUPERSEDED (via re-establishment) is reachable by any write path; RETIRED is declared and check-constrained but no Business Activity ever sets it — see Finding D |
| Audit Trail (`§12.5`) | `established_by_person_id`, `created_at` | ✓ Implemented, tested. "Why" (a reason/justification) is not captured — consistent with every other `establish`-shaped endpoint in this codebase (`EstablishMembershipRequest` etc. carry no reason field either); not a WP-10-specific gap |
| Metadata (`§12.5`) | `value: JSON`, facet+key-shaped payload | ✓ Implemented |
| Tenant Scope (`§12.5`) | `organization_id` FK, NOT NULL, filtered in every repository query | ✓ Implemented, tested, independently re-probed (Probe 1 below) |
| AI Discoverability (`§12.5`, mandatory ✓) | — | ⚠ **Never addressed** in any WP-10 governing document — see Finding B |
| Approval Workflow (`§12.5`, "where applicable") | — | ⚠ **Applicability never explicitly determined** — see Finding C |
| Scope Hierarchy (`§12.6`) — Tenant/User anchored, 5 of 8 tiers unanchored | `ConfigurationScopeLevel` (TENANT, USER only) | ✓ Accurately disclosed (`TD-116`); re-confirmed 8 named tiers in `§12.6` primary text, matching `TD-116`'s own count |
| Resolution Rules (`§12.7`) — most-specific wins | `ConfigurationResolutionService._resolve_key` (User → Tenant → Platform Default) | ✓ Implemented, tested |
| Terminology facet (`SD-002-079`, IRA-010 §4.1) | Open-ended key space, no synthetic platform default | ✓ Implemented, tested |
| Branding-core (`CMD-001 §12.3` example) | `logo_url` key | ✓ Implemented, tested. Dual-logo correctly excluded, undisturbed |
| Theme-core (`DS-001-183`, four of five classes) | `theme_class` key, `theme.css` `[data-theme]` blocks | ✓ Implemented, tested, consumed platform-wide via `AdminShell`/`useResolvedTheme` — verified the real WP-01–WP-09 screens (Membership, Organization Structure, etc.) all render under `platform-admin/(workspace)/**`, which `AdminShell` wraps; the `(app)/**` route group contains only placeholder pages today, so "platform-wide" is accurate for every screen that actually exists |
| Accessibility Profiles (`DS-001-194`/`SD-001-063`, IRA-010 §4.4) | `high_contrast_enabled`, `reduced_motion_enabled` | ✗ **Non-conforming** — see Finding A |
| Localization-narrow (`CMD-001 §12.3` example) | `default_language` key | ✓ Implemented, tested |
| BA-01 Authorization (own tenant only, or PLATFORM_ADMIN) | `require_matching_tenant_or_platform_admin` | ✓ Implemented, tested, independently re-probed (below) |
| BA-02 Authorization (`PLATFORM_ADMIN`-gated) | `require_platform_admin` | ✓ Implemented, tested — correctly disclosed as the same interim `TD-021`-class gate |
| Mandatory Tenant-Isolation Checklist (`CLAUDE.md §21.4`) | `TestConfigurationTenantIsolation` (3 tests) + service-layer equivalent | ✓ Implemented — re-probed independently at the repository layer (below), no gap found |
| Five mandatory UI states (`CLAUDE.md §20.6`) | `ConfigurationEntriesSection`/`EstablishConfigurationSection` | ✓ Loading, empty, validation, error, confirmation all independently confirmed wired to real state (`useConfigurationManagement.ts`), not hardcoded |

---

## Empirical Probes (From-Scratch, Not Adapted From the Shipped Suite)

### Probe 1 — Repository-Layer Two-Tenant Isolation + FK Production-Parity

A new, standalone script instantiated two Organizations and interleaved writes/reads directly against `ConfigurationEntryRepository`, bypassing the router/authorization layer entirely (the shipped `TestConfigurationTenantIsolation` class and `CERT-WP-10`'s own probe both go through the API; this probe targets the query layer in isolation, and also probes a random, never-seeded `organization_id`).

**Result: no isolation defect found.** Every repository method (`get_active_tenant_override`, `get_active_tenant_overrides_for_facet`, `list_active_for_organization`) returned exactly the calling organization's own rows; a lookup for a random, non-existent `organization_id` returned nothing (not an error, not another organization's row).

**Harness/fixture production-parity finding (required checklist item):** the same script inserted a `ConfigurationEntry` with a non-existent `organization_id` directly against the SQLite in-memory test harness — **it succeeded with no foreign-key error**, despite `organization_id` being declared `NOT NULL` + `ForeignKey("organizations.id")` in both the model and the Postgres migration. Root cause: `tests/conftest.py`'s `create_async_engine(SQLITE_TEST_URL, ...)` has no `PRAGMA foreign_keys=ON` connect-event listener, and SQLite does not enforce FK constraints by default. **This is not a new finding** — it is the exact, already-registered, repository-wide gap `TD-096` (Open, Medium, first found by `CERT-WP-07`) describes. WP-10 adds three more FK columns to the same already-disclosed harness gap (`organization_id`, `person_id`, `established_by_person_id`) — `TD-096` continues to apply to them; no new Technical Debt entry is warranted for this alone.

### Probe 2 — Concurrent-Write Race (`TD-118`'s Own Claim, Empirically Confirmed)

`TD-118` (raised by `CERT-WP-10` Gate 1, escalated as non-blocking) claims two concurrent `POST /configuration` calls for the same `(organization_id, facet, key)` can both land `ACTIVE`, since `establish()`'s read-then-write sequence holds no row lock and the Postgres migration creates only a non-unique index. A new, standalone script opened two independent `AsyncSession`s (simulating two concurrent HTTP requests), had both read "no prior ACTIVE row" before either wrote (the exact interleaving `TD-118` describes), then had both insert and commit.

**Result: TD-118's claim is empirically CONFIRMED.** Both commits succeeded with no error; the final state held **two simultaneously-ACTIVE rows** for the identical `(organization_id, THEME, theme_class)` key (`DARK` version 1 and `HIGH_CONTRAST` version 1, both `ACTIVE`). `TD-118`'s Medium severity rating is reasonable and unchanged — `PLATFORM_ADMIN`-only, low-concurrency establish traffic makes this an unlikely-to-trigger-today, not a currently-exploited, gap, and it is not a tenant-isolation or security defect (only one organization's own data is affected by its own admin's own race). No escalation to blocking is warranted.

### Probe 3 — USER-Scope Resolution Path Reachability (`TD-115`'s Own Claim)

`TD-115` claims `ConfigurationScopeLevel.USER` is declared for schema completeness with no writer anywhere. Verified by exhaustive `grep` across the entire `Backend/` tree (not only `AuthService`, and not only the files WP-10 itself touched) for `ConfigurationEntry(` constructor calls, `scope_level.*USER` literals, and any `configuration_entries` reference outside WP-10's own known file set. **Result: confirmed accurate.** The only two places `ConfigurationEntry(` is constructed anywhere in the codebase are the model's own class definition and `ConfigurationManagementService.establish()`, which hardcodes `scope_level="TENANT"`, `person_id=None` unconditionally — there is no router, script, seed path, or migration data-load anywhere that writes a `USER`-scope row, directly or indirectly. `ConfigurationResolutionService`'s own USER-tier read (`get_active_user_overrides_for_facet`) is genuinely dead code today, exactly as disclosed.

### Probe 4 — Cross-Tenant Disclosure Remediation (Finding B-1), Independent Re-Confirmation

Read `require_matching_tenant_or_platform_admin` and its wiring directly; independently traced every code path reaching `resolution_service.resolve(...)` in `routers/configuration.py` and confirmed only one exists, gated by the fixed dependency. Ran the existing `TestConfigurationTenantIsolation::test_outsider_with_no_relationship_to_org_cannot_resolve_its_configuration` and `test_resolve_rejects_mismatched_tenant_for_non_admin` as part of the full-suite run above (both pass). No new bypass path found. `CERT-WP-10_Remediation_Verification`'s own negative control (probe fails against pre-fix code, passes against post-fix code) is independently credible on the evidence presented and consistent with the code read directly in this audit.

---

## Finding A (Medium–High, non-blocking, registered as `TD-119`) — Accessibility Profile Facet Does Not Match Its Own Governing Provision (`DS-001-194`)

`IRA-010 §4.4` scoped the Accessibility Profiles facet explicitly and only in terms of "reduced-motion and large-text accessibility modes as orthogonal to theme class" — this is a direct (if slightly mis-cited: IRA-010 cites "`DS-001-570`", which does not exist as a provision ID; the correct citation, confirmed by direct read of DS-001 §11.7, is **`DS-001-194`**) paraphrase of `DS-001-194`: "Reduced-motion and large-text accessibility modes (`SD-001-063`) are supported identically across all five theme classes... Accessibility mode and theme class are independent, orthogonal selections." `DS-001-193` separately establishes that **High-Contrast is already realized by the Theme System itself** (the `HIGH_CONTRAST` theme class), not by a separate Accessibility flag — so `DS-001-194`'s own two orthogonal-to-Theme modes are specifically reduced-motion and large-text, not high-contrast.

The shipped implementation built `high_contrast_enabled` and `reduced_motion_enabled` (`PLATFORM_DEFAULTS` in `services/configuration_resolution_service.py`; `ACCESSIBILITY_KEYS` in `EstablishConfigurationSection.tsx`) — **large-text mode is entirely absent** from the platform (no backend key, no frontend control, no `theme.css` support anywhere), and `high_contrast_enabled` duplicates a mode the Theme facet already provides, undisclosed anywhere as an intentional substitution. `SD-001-063`'s own mandate ("high-contrast, reduced-motion, and large-text modes are tenant- and user-configurable") is therefore genuinely unmet for large-text — no mechanism anywhere in this platform makes it tenant- or user-configurable.

This was not found by `CERT-WP-10` (Gate 1) — confirmed by direct search of both certification documents for "large-text," "`DS-001-194`," and "`DS-001-570`": no match in either.

**Severity:** rated High per `CLAUDE.md §19.8.7`'s own rubric language ("the gap defeats the governing capability's own stated Business Intent, even if only for a disclosed subset of cases") — `IRA-010 §4.4`'s own stated basis for taking Accessibility Profiles in scope (large-text, orthogonal to Theme) was not delivered, and an undisclosed substitute was delivered in its place. **This is not, however, a `CLAUDE.md §19.8.5`-class defect** — it is not a security, tenant-isolation, or data-integrity gap, no test fails, and no functionality is broken (what was built works correctly for the two keys it does implement); it does not require remediation before Gate 5, mirroring `TD-070`'s own precedent (High severity, disclosed, deferred, not blocking).

**Proposed `TD-119`:** Description as above. Raised in: `VV-AUDIT-WP-10` (Gate 2). Category: Enterprise Experience / Specification Conformance. Severity: High. Target Resolution: replace `high_contrast_enabled` with `large_text_enabled` in `PLATFORM_DEFAULTS`, `ACCESSIBILITY_KEYS`, and any consuming frontend logic; retain `reduced_motion_enabled` unchanged; do not remove the Theme facet's own `HIGH_CONTRAST` class. Status: Open.

---

## Finding B (Low, non-blocking, registered as `TD-120`) — "AI Discoverability" (`CMD-001 §12.5`, Mandatory) Never Addressed

`CMD-001 §12.5` marks AI Discoverability mandatory (✓) for every Configuration or Policy object, the same table row as Versioning/Effective Dating/Lifecycle State/Audit Trail — all four of which `IMP-REPORT-WP-10`'s own Business Activity Contracts explicitly reason through. AI Discoverability is not mentioned once in `IRA-010`, `ADR-019`, `IMP-REPORT-WP-10`, or either `CERT-WP-10` document — confirmed by direct search of all four. This is **not unique to WP-10**: the identical search across every `IMP-REPORT-*`, `CERT-*`, and `ADR-*` document in the repository finds zero prior mentions either — a repository-wide silence on this specific mandatory characteristic, first surfaced by this audit, not a WP-10-specific omission. `CFG-000001`'s own `§26.4` "AI Context" registration field (present in `IRA-010 §6`: "The effective platform/tenant/user configuration value...") plausibly satisfies the intent at the Business-Object-type level, but no document anywhere states this reasoning explicitly.

**Proposed `TD-120`:** Description as above. Raised in: `VV-AUDIT-WP-10`. Category: Governance / Documentation Completeness. Severity: Low (a reasoning-completeness gap, not a functional one; a plausible satisfying mechanism already exists via `§26.4`'s AI Context field). Target Resolution: future IRAs/Implementation Reports should explicitly state how each mandatory `§12.5` characteristic, including AI Discoverability, is satisfied — for WP-10 specifically, add one sentence to `IMP-REPORT-WP-10` or a governance addendum noting `CFG-000001`'s own AI Context field as the satisfying mechanism. Status: Open.

---

## Finding C (Low, non-blocking, registered as `TD-121`) — "Approval Workflow — Where Applicable" (`CMD-001 §12.5`) Applicability Never Explicitly Determined

`CMD-001 §12.5` lists Approval Workflow as mandatory "where applicable." Neither `IRA-010` nor `IMP-REPORT-WP-10` ever states whether Approval Workflow is applicable to `CFG-000001` and, if not, why — BA-02's direct-write, `PLATFORM_ADMIN`-gated-only design is never justified against this specific characteristic. Independent review finds inapplicability is the defensible conclusion (the five in-scope facets — Terminology labels, single-logo branding, Theme class, Accessibility flags, default language — are low-stakes presentation configuration, not the kind of business-policy decision `§12.4`'s own "Approval Policies" category addresses; no generic approval-workflow-gating mechanism exists anywhere in this platform today for any object, `Configuration` or otherwise), but this determination was never actually made and recorded — it was silently skipped, not reasoned through and found inapplicable.

**Proposed `TD-121`:** Description as above. Raised in: `VV-AUDIT-WP-10`. Category: Governance / Documentation Completeness. Severity: Low (the likely-correct conclusion — not applicable — was probably reached implicitly, but was never recorded, so a future reviewer cannot distinguish "considered and found inapplicable" from "overlooked"). Target Resolution: add one sentence to `IMP-REPORT-WP-10` (or a governance addendum) recording that Approval Workflow was considered and found not applicable to WP-10's own in-scope facets, with the rationale above. Status: Open.

---

## Finding D (Low, non-blocking, registered as `TD-122`) — `RETIRED` Lifecycle State Is Declared but Unreachable by Any Write Path

`ConfigurationLifecycleState.RETIRED` is declared in the model, permitted by the `CheckConstraint` in both the model and the Postgres migration, and documented in the model's own docstring ("RETIRED (explicitly withdrawn, no replacement)") — but no Business Activity, router, or service method anywhere transitions any row to `RETIRED`. The only reachable transition is `ACTIVE → SUPERSEDED`, via re-establishing a new value for the same key (`ConfigurationManagementService.establish()`). An enterprise administrator can therefore **replace** an override but cannot **withdraw** one back to the Platform Default — there is no "reset to default" mechanism. This mirrors the exact disclosure discipline `TD-115` already applies to the unreachable `USER` scope level, but was not itself disclosed anywhere.

**Proposed `TD-122`:** Description as above. Raised in: `VV-AUDIT-WP-10`. Category: Enterprise Experience / Completeness. Severity: Low (no capability currently depends on retiring a Configuration override; the gap is a missing convenience operation, not a correctness or compliance defect — an administrator can still achieve the same effect for fixed-key facets, other than Terminology, by re-establishing the known platform-default value). Target Resolution: a future, separately-scoped BA-02 extension (e.g. `DELETE /configuration` or a `retire` action) that transitions the current `ACTIVE` row to `RETIRED` with `effective_to` set, restoring Platform Default resolution for that key. Status: Open.

---

## Harness/Fixture Production-Parity Checklist (Mandatory)

- **Does the harness enforce every constraint the declared production database enforces unconditionally (FK, check, uniqueness)?** No — confirmed by Probe 1 (FK) and Probe 2 (uniqueness/race). FK non-enforcement is the pre-existing, repository-wide `TD-096` (still Open, still Medium) — WP-10's own three new FK columns are simply three more instances of an already-tracked gap, not a new one. Uniqueness non-enforcement is `TD-118` (already registered by Gate 1), now empirically confirmed rather than merely inferred.
- **Does at least one test exercise more than one tenant/organization for `CFG-000001` (which has an organization boundary)?** Yes — `TestConfigurationTenantIsolation` (3 API-level tests) and `test_resolve_never_leaks_a_different_organizations_override` (1 service-level test), all genuine two-organization negative controls (not single-tenant absence-of-counter-evidence tests) — independently confirmed by direct read and by this audit's own from-scratch Probe 1, which found no isolation defect at the repository layer either.

---

## Determination

**PASS WITH OBSERVATIONS.** No `CLAUDE.md §19.8.5`-class defect (security, tenant-isolation, data-integrity, failing test, build failure, or broken functionality) was found. Finding B-1's remediation (Gate 3/4) is independently re-confirmed sound. Four new, non-blocking findings (A–D) are registered as proposed `TD-119` through `TD-122` above — the coordinating session should add these to `TECH-DEBT.md`; this audit does not edit that file itself. WP-10 may proceed to Gate 5 (Release Readiness Audit).

**Note for the Gate 5 (Release Readiness Audit) reviewer:** `WP-REG-001` and `DOC-000` currently state the pre-remediation test count (740/740) and "not yet committed" — accurate as of Gate 1, stale as of Gate 4's own 743/743. This is expected at this point in the sequence (Gate 5 is the gate `CLAUDE.md §19.7b` specifically assigns to catch governance-document staleness) and is noted here only so Gate 5 does not need to rediscover it independently.

---

*End of VV-AUDIT-WP-10. See a future `RRA-WP-10_Configuration_Management_Release_Readiness_Audit.md` (Gate 5) for final governance-document reconciliation and commit authorization.*
