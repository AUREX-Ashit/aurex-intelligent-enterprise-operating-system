# CERT-WP-18 — Independent Certification: Bind and Resolve Approval Authority (C-003)

**Work Package:** WP-18 — C-003 (Role & Permission Management) — Bind and Resolve Approval Authority
**Business Activity:** BA — Bind and Resolve Approval Authority (working title, per the charter §1 disclosure — no closer canonical term exists in `URA-001` or repository precedent)
**State certified:** working tree at the time of this review — commit `e86192f95a1ef3534513f9fcee9418bbecb21baf` (`main`) plus uncommitted WP-18 changes (`git status --short` / `git diff --stat` / `git diff --cached --stat` reproduced in full at the end of this report). The working tree simultaneously carries uncommitted WP-16 (C-040 Tenant Establishment) work certified separately in `CERT-WP-16_Tenant_Establishment.md`; this certification isolates and certifies the WP-18 change set only, exactly as `CERT-WP-16` certified an uncommitted working tree for its own scope.
**Reviewer:** Genuinely independent, fresh-context reviewer — no access to any prior session's conversation, no prior involvement in WP-18's implementation, in the drafting of `TDS-018` / the WP-18 charter / `IMP-REPORT-WP-18`, in `TDS-018 §28`/`§30`/`§31`'s prior independent reviews, or in the prior Gate 1 attempt that returned NOT CERTIFIED for finding "M-1". Every material claim below was re-derived from primary sources — actual files opened, actual commands run.
**Gate:** 1 of 5 (`CLAUDE.md §19.7b`)
**Determination:** **CERTIFIED — PASS WITH OBSERVATIONS** — no `CLAUDE.md §19.8.5`-class defect found (no architectural, security, data-integrity, tenant-isolation defect; no failing test; no build failure; no broken functionality; no live non-struck stale-status contradiction re-creating M-1; no design non-conformance to `TDS-018 §29.2`; no out-of-scope implementation). Four non-material observations recorded, none blocking.

---

## Scope and Method

This certification re-derives every material claim in the WP-18 charter, `IMP-REPORT-WP-18`, and `TDS-018` from primary sources — no claim accepted on trust, no prior certification conclusion relied upon. Specifically performed:

- Full read, in order: `WP-18_C003_BA-XX_Approval_Authority_Runtime_Binding_Business_Activity_Charter.md`; `IMP-REPORT-WP-18_Approval_Authority_Runtime_Binding.md`; `TDS-018_C003_Approval_Authority_Runtime_Binding_Technical_Design.md` (all 409 lines — §§1–31, including §29.2–§29.6 corrected resolver algorithm, §29 amendment, §30 amendment review, §31 M-1 reconciliation, and both Change Control blocks); `WPR-001_Work_Package_Roadmap.md` (WP-18 row and its diff; WP-13 precedent row); `CERT-WP-16_Tenant_Establishment.md` (format/rigor precedent); `CLAUDE.md §16`, `§17`, `§18`, `§19` (all subsections, incl. `§19.7`, `§19.7b`, `§19.8.5`, `§19.8.7`), `§20`, `§21` (`§21.3`, `§21.4`).
- Full read of every new WP-18 backend file: `models/membership_approval_authority.py`; `alembic/versions/2026_08_29_1100-f9a3c7e1b5d2_membership_approval_authority.py`; `repositories/membership_approval_authority_repository.py`; `services/membership_approval_authority_service.py`; `services/approval_authority_resolver.py`; `tests/test_approval_authority_resolver.py` (all 22 tests); `tests/test_membership_approval_authority_service.py` (all 8 tests).
- Direct `git diff` inspection of every modified tracked WP-18 file: `dependencies.py`, `models/__init__.py`, `repositories/approval_authority_repository.py` — each confirmed purely additive.
- Direct read of `models/approval_authority.py` (`ApprovalStrategy` / `VersionStatus` enums, `majority_threshold_pct`), `models/authority_holder.py` (`CheckConstraint`), `middleware/tenant.py` (`get_current_tenant` derivation), `Backend/Runtime/AuthorizationEngine/authorization/tier_resolvers.py` (`ApprovalAuthorityResolver` stub).
- Independent line-for-line comparison of the model/migration against the canonical `CREATE TABLE membership_approval_authority` in `Master_Technical_Architecture.md` (lines 1319–1329).
- Independent fresh re-run of `tests/test_approval_authority_resolver.py tests/test_membership_approval_authority_service.py -v` (30 tests).
- Independent fresh re-run of the full `AuthService` regression suite (`python -m pytest -q`) — not the figure reported by any prior report.
- Independent re-run of `alembic heads` and `alembic history` against the actual repository.
- `git rev-parse HEAD`, `git status --short`, `git diff --check`, `git diff --cached --stat` at the repository root, before and after this review.
- Direct grep of every WP-18 implementation file for License/Entitlement/Subscription/Billing/C-023/Group implementing terminology, to independently verify scope confinement.
- Targeted grep of `TDS-018` for any non-struck present-tense claim that WP-18 implementation is unauthorized / incomplete / nonexistent (the former "M-1" blocker).

## Governing Documents Reviewed

`WP-18_C003_BA-XX_Approval_Authority_Runtime_Binding_Business_Activity_Charter.md` (full); `IMP-REPORT-WP-18_Approval_Authority_Runtime_Binding.md` (full); `TDS-018_C003_Approval_Authority_Runtime_Binding_Technical_Design.md` (full, §§1–31 + both Change Control blocks); `WPR-001_Work_Package_Roadmap.md` (WP-18 row + WP-13 precedent); `Master_Technical_Architecture.md` (canonical `membership_approval_authority` schema, lines 1319–1329, and schema-catalog listing line ~1318); `CLAUDE.md §16`, `§17`, `§18`, `§19` (all subsections), `§20`, `§21` (`§21.3`/`§21.4`); `CERT-WP-16_Tenant_Establishment.md` (format/rigor precedent). Cross-check only, not certified, confirmed untouched by the WP-18 change set: `IRA-C023_Licensing_and_Entitlement_Implementation_Readiness_Assessment.md`, `TDS-C023_Licensing_and_Entitlement_Minimum_BA.md`, `WP-17_C023_BA-01_Establish_Entitlement_License_Context_Business_Activity_Charter.md`.

---

## Point-by-Point Findings

### A. Governance Traceability — including the former "M-1" blocker

**Checked:** direct read of `IMP-REPORT-WP-18 §1`/`§2`/`§6`, the WP-18 charter header Status line and §24/Final Determinations, the `WPR-001` WP-18 row and its diff, and a targeted grep of the whole of `TDS-018` for stale WP-18 status wording.

**Result:**
- **Repository Owner Implementation Authorization** is recorded verbatim in `IMP-REPORT-WP-18 §1`, in a block-quote reproduced "exactly as recorded", dated **2026-08-29**, "direct instruction", with an explicit **Scope authorized** list (the `membership_approval_authority` model/migration; repository/service; the resolver implementing `TDS-018 §29.2`'s corrected 8-step algorithm — `ANY_ONE` only, `MAJORITY`/`ALL`/`SEQUENTIAL` denied as `UNSUPPORTED_STRATEGY`, malformed configuration denied as `INVALID_CONFIGURATION`; Option B FastAPI-dependency integration; the cross-Organization bind guard; audit wiring; the `§18`/`§29.6`/`§21.4` test suite) and an explicit **"Explicitly NOT authorized"** exclusion list (C-023 of any kind; `WP-17`; License/Entitlement; License Consumption/Allocation; Entitlement Catalog; Subscription semantics; Billing; frontend/UI; `AuthorityHolder` replacement/modification; Group infrastructure; `PLATFORM_ADMIN`/`AUREX_ADMIN` redesign; any Engine work beyond `§12` Option B). The final sentence states verbatim: *"Authorization to implement WP-18 does not constitute certification. Certification remains subject to the applicable implementation, testing, independent-review, and certification gates (`CLAUDE.md §19.7`/`§19.7b`), none of which have yet been dispatched."*
- `IMP-REPORT-WP-18 §6` states **"Implementation Status: IMPLEMENTATION COMPLETE"** and explicitly **"This report does NOT certify WP-18."** `§2` lists the file set.
- WP-18 **charter** header Status line reads: **"CHARTERED — IMPLEMENTATION AUTHORIZED, IMPLEMENTATION COMPLETE, NOT YET CERTIFIED."** with the historical drafting-time wording preserved struck-through and dated. `§24` and the "Final Determinations" / "Final state" lines agree, again strikethrough-preserve, nothing erased.
- `WPR-001` WP-18 row current text: **"CHARTERED — IMPLEMENTATION AUTHORIZED, IMPLEMENTATION COMPLETE, NOT YET CERTIFIED."** with the prior drafting-time cell struck-through and annotated. Agrees with the charter and `IMP-REPORT`. The row also records the disclosed `WP-13`-precedent basis (no accepted IRA) and that the prior Gate 1 attempt returned NOT CERTIFIED for a governance-documentation gap only.
- **Former "M-1" blocker — eliminated.** `TDS-018`'s two status-of-record locations the prior Gate 1 finding named are both remediated with the strikethrough-preserve convention: (1) the header **Status** line — original struck (`~~Technical Design — implementation NOT authorized …~~`), a new *"Status (current — updated 2026-08-29 …)"* block added stating this remains a governing Technical Design that never itself granted authorization, that the Repository Owner has since separately and explicitly granted Implementation Authorization (2026-08-29, recorded in `IMP-REPORT-WP-18`), that implementation is complete, and that **WP-18 remains NOT YET CERTIFIED**; (2) `§29.9`'s closing clause — struck-through, with a *"Superseded 2026-08-29"* note giving the same corrected status. `§31` is appended recording the reconciliation in full, with a `§31.3` current-status table. `grep -niE "not yet authorized|not authorized|not yet complete|does not exist"` over `TDS-018` returns no **non-struck present-tense statement asserting WP-18 implementation is unauthorized, incomplete, or nonexistent as a status of record**. (Two non-struck design-rationale phrases in the explicitly-frozen `§§1–28` historical body are discussed at Observation 1 — they are not status assertions and do not recreate M-1.)

**Conclusion: Pass.** Governance chain (`TDS-018` → charter → `IMP-REPORT-WP-18` → `WPR-001`) is internally consistent and consistent with the actual repository state. The M-1 stale-status contradiction is genuinely eliminated, not merely relabelled.

### B. Design Conformance — `TDS-018 §29.2` authoritative resolver algorithm

**Checked:** line-by-line trace of `services/approval_authority_resolver.py::resolve_approval_authority()` against `TDS-018 §29.2`'s 8 ordered steps, `§29.3` fail-closed behavior, and `§29.4`'s 8-label reason taxonomy. `§10`/`§11`/`§20` confirmed superseded per `§29`'s own notes and not used.

**Result — the implemented order is exactly `§29.2`'s, no step skippable or reorderable:**
1. **Resolve the authority** — `get_active_by_organization_and_name(target_organization_id, authority_name)`; if `None`, `get_any_by_organization_and_name(...)` → if a non-`ACTIVE` row exists, `_deny(INACTIVE_AUTHORITY)`, else `_deny(NO_AUTHORITY_CONFIGURED)`. Distinction made an explicit separately-checked condition, per `§29.2` step 1.
2. **Validate configuration** — `approval_strategy == MAJORITY and majority_threshold_pct is None` → `_deny(INVALID_CONFIGURATION)`. Placed **before** the strategy gate and **before any caller-specific step**, with an in-code comment citing `§29.2` step 2's ordering fix. Independently confirmed unreachable-via-binding by `test_malformed_majority_configuration_denies_before_binding_check` (a valid binding is created, yet the outcome is `INVALID_CONFIGURATION`).
3. **Inspect `approval_strategy`** — `approval_strategy != ApprovalStrategy.ANY_ONE.value` → `_deny(UNSUPPORTED_STRATEGY, {"approval_strategy": ...})`. Placed **before** any caller-specific step. `MAJORITY`/`ALL`/`SEQUENTIAL` terminate here; no counting, quorum, or sequencing semantics are computed, simulated, or approximated anywhere in the module (confirmed by full read).
4. **Organization mismatch** — `caller_organization_id is None or caller_organization_id != target_organization_id` → `_deny(INVALID_SCOPE)`.
5. **Eligible actor / missing binding** — `caller_membership_id is None` → `NO_ELIGIBLE_ACTOR`; else `binding_repo.get_effective_binding(caller_membership_id, authority.id)` (`effective_from <= now` AND (`effective_to IS NULL` OR `effective_to > now`)); `None` → `_deny(NO_ELIGIBLE_ACTOR)`.
6. **Active/inactive actor** — `membership_repo.get_by_id(...)`; requires `membership_status == "ACTIVE"` AND `effective_from <= now` AND (`effective_to IS NULL` OR `effective_to > now`); otherwise `_deny(INACTIVE_MEMBERSHIP)`.
7–8. **`AUTHORIZED`** — reached only when steps 1–6 all pass; emits `record_audit(SUCCESS)` + `publish_event("APPROVAL_AUTHORITY_RESOLVED")` and returns `ApprovalAuthorityResolution.AUTHORIZED`.

- **Configuration validation precedes the strategy gate and precedes ALL caller-specific steps** — confirmed (step 2 before step 3 before steps 4–6).
- **`approval_strategy != ANY_ONE` terminates with DENY/UNSUPPORTED_STRATEGY before any caller-specific evaluation** — confirmed (step 3, before steps 4–6). `test_unsupported_strategy_with_valid_binding_never_authorizes[MAJORITY-60 | ALL-None | SEQUENTIAL-None]` asserts both `== UNSUPPORTED_STRATEGY` and `!= AUTHORIZED`, each with a real valid binding present.
- **ALL / MAJORITY / SEQUENTIAL vote-counting/sequencing is NOT invented, simulated, or approximated** — confirmed by full-module read; they are denied, not resolved.
- **Fail-closed (`§29.3`)** — every branch calls `_deny(...)` and returns the reason; the only non-deny path is the single fully-satisfied `ANY_ONE` path. No `PLATFORM_ADMIN` / `AUREX_ADMIN` / Role / Group fallback exists at any branch (confirmed by read and by grep — the only admin strings in the module are in the docstring documenting the deliberate non-bypass).
- **Reason taxonomy (`§29.4`)** — `ApprovalAuthorityResolution` is a `str, Enum` with exactly the 8 labels: `NO_AUTHORITY_CONFIGURED`, `INACTIVE_AUTHORITY`, `INVALID_CONFIGURATION`, `UNSUPPORTED_STRATEGY`, `INVALID_SCOPE`, `NO_ELIGIBLE_ACTOR`, `INACTIVE_MEMBERSHIP`, `AUTHORIZED` — no more, no fewer.

**Conclusion: Pass.** The implementation faithfully realizes `TDS-018 §29.2` in exact order, with `§29.3` fail-closed behavior and the `§29.4` taxonomy exact.

### C. Implementation — file-by-file, additive-change verification

**Checked:** full read of the 5 new source files + 2 new test files; `git diff` of the 3 modified tracked files.

**Result:**
- `models/membership_approval_authority.py` — canonical columns `membership_id` / `approval_authority_id` / `effective_from` (composite PK) / `effective_to` (nullable). One disclosed additive hardening: partial unique index `ux_membership_approval_authority_active` on `(membership_id, approval_authority_id) WHERE effective_to IS NULL` — exactly the hardening `TDS-018 §19` names, mirroring `authority_holders`'s own precedent. No `organization_id` column (matches canonical; isolation enforced at two other layers). Soft-close via `effective_to`, no status column.
- `alembic/.../f9a3c7e1b5d2_membership_approval_authority.py` — `down_revision = 'b2c3d4e5f6a7'`. `upgrade()` = one `op.create_table` + one `op.create_index` (the partial unique index). `downgrade()` drops both. No `ALTER` to `approval_authorities` or `memberships`; no data migration; nothing destructive.
- `repositories/membership_approval_authority_repository.py` — `get_open_binding()` (used by the bind-time uniqueness guard and by `close()`) and `get_effective_binding()` (resolver step 5). Read-only queries; extends `BaseRepository`.
- `services/membership_approval_authority_service.py` — `bind()`: Membership existence (404) → Approval Authority existence (404) → **cross-Organization rejection** `membership.organization_id != authority.organization_id` → HTTP **409** → duplicate open-binding rejection (**409**) → create + `record_audit(SUCCESS)` + `publish_event`. `close()`: locate open binding (404 if none) → set `effective_to = now` → audit + event. Never a hard delete.
- `services/approval_authority_resolver.py` — as traced in Finding B. Audits every outcome (`_deny` emits `record_audit(DENIED, {"reason": ...})`; the `AUTHORIZED` path emits `record_audit(SUCCESS)` + `publish_event`).
- `models/__init__.py` — `git diff` shows only added lines: `from .membership_approval_authority import MembershipApprovalAuthority` + `"MembershipApprovalAuthority"` in `__all__` (WP-18), alongside the separate WP-16 `TenantRegistry` addition. No existing line altered.
- `repositories/approval_authority_repository.py` — `git diff` shows only an added `from sqlalchemy import select`, an extended import (`ApprovalAuthority, VersionStatus`), and two new read-only methods `get_active_by_organization_and_name` / `get_any_by_organization_and_name`. `get_active_dependents()` / `has_active_dependents()` and every other existing method are byte-for-byte unchanged.
- `dependencies.py` — `git diff` shows the WP-18 hunk is purely appended: `enforce_approval_authority()` (plain async function; raises `HTTPException(403)` on any non-`AUTHORIZED` outcome) and `require_approval_authority()` (dependency factory; `authority_name` fixed at registration, target Organization = `Depends(get_current_tenant)`). The `require_authority_holder` / `require_ai001_holder` / `require_ai002_holder` block also present in the same diff is pre-existing WP-16/C-040 (TDS-017) work, not WP-18 — `IMP-REPORT-WP-18 §2` lists only the two WP-18 functions, and both are appended after existing content with no existing function modified.

**Conclusion: Pass.** Every modified file's WP-18 change is purely additive; no existing function, method, or migration was altered.

### D. Security

**Checked:** direct code read of `enforce_approval_authority` / `require_approval_authority`, `resolve_approval_authority`, `MembershipApprovalAuthorityService.bind()`, `middleware/tenant.py::get_current_tenant`, plus the dedicated security tests.

**Result:**
- **No admin bypass.** `enforce_approval_authority` / `require_approval_authority` grant no pass to `PLATFORM_ADMIN` or `AUREX_ADMIN` — a deliberate, documented divergence from `enforce_domain_permission`'s universal-bypass precedent (`TDS-018 §11`/`§18` prohibit any such fallback). `test_admin_role_does_not_bypass_approval_authority_gate[PLATFORM_ADMIN | AUREX_ADMIN]` seeds claims carrying the admin `role_code`, no binding, and asserts `HTTPException(403)`. Independently re-run, passing.
- **Tenant isolation at bind time.** `bind()` compares `membership.organization_id` against `authority.organization_id` and raises **409** on mismatch. `test_bind_cross_organization_rejected` binds a Membership in Org A to an Approval Authority in Org B, asserts 409, and then asserts `get_open_binding(...) is None` (no row created). Independently re-run, passing.
- **Tenant isolation at resolution time.** Resolver step 4 compares `caller_organization_id` (from JWT claims) against `target_organization_id`. In `require_approval_authority`, `target_organization_id` is `Depends(get_current_tenant)`, which returns the `tenant_context` ContextVar set by `TenantMiddleware` **from the `X-Tenant-ID` header** — independent of the caller's JWT claims. The mismatch check is therefore meaningful (not comparing a claim to itself). `test_organization_mismatch_denies` and `test_cross_organization_binding_attempt_rejected` (caller in Org A, target = Org B's id, Org B's authority) both assert `INVALID_SCOPE` — denied at step 4, before any binding lookup that could infer Org B data. Independently re-run, passing.
- **Malformed configuration.** `MAJORITY` with `NULL` threshold → `INVALID_CONFIGURATION` at step 2, unreachable via a qualifying binding (`test_malformed_majority_configuration_denies_before_binding_check`, passing).
- **Missing / invalid claims → fail closed.** `test_missing_claims_denies_closed` passes empty claims to `enforce_approval_authority` and asserts `HTTPException(403)`. The resolver treats `caller_organization_id is None` as `INVALID_SCOPE` and `caller_membership_id is None` as `NO_ELIGIBLE_ACTOR`. Passing.
- **Unsupported strategies → fail closed** (`UNSUPPORTED_STRATEGY`) — Finding B.
- **Duplicate open binding → 409, never silently duplicated; `close()` soft-closes.** `test_bind_duplicate_pair_rejected_not_silently_duplicated`, `test_close_deactivates_binding_without_deleting` (asserts the row still exists after close), `test_rebind_after_close_succeeds`. All passing.

**Conclusion: Pass.** No admin bypass; tenant isolation independently enforced at bind time and resolution time; all failure modes fail closed.

### E. Data / Migration

**Checked:** column-by-column comparison against `Master_Technical_Architecture.md` lines 1319–1329; migration content read; `alembic heads` / `alembic history` re-run.

**Result:**
- Canonical schema (`Master_Technical_Architecture.md`):
  ```sql
  CREATE TABLE membership_approval_authority (
      membership_id UUID REFERENCES membership_registry(membership_id),
      approval_authority_id UUID REFERENCES approval_authority_registry(approval_authority_id),
      effective_from TIMESTAMP WITH TIME ZONE,
      effective_to TIMESTAMP WITH TIME ZONE,
      PRIMARY KEY (membership_id, approval_authority_id, effective_from)
  );
  ```
  The model and migration match exactly: the three-column composite PK `(membership_id, approval_authority_id, effective_from)`, nullable `effective_to`, FKs to the AuthService-convention table names `memberships.id` / `approval_authorities.id` (the established WP-02/WP-03 physical names for `membership_registry` / `approval_authority_registry`). The additive partial unique index `ux_membership_approval_authority_active` is the `TDS-018 §19` hardening, not a canonical-schema deviation.
- Migration is **purely additive**: one new table, one new index; no `ALTER` to `approval_authorities` or `memberships`; no data migration; `downgrade()` is a clean drop.
- `alembic heads` → **`f9a3c7e1b5d2 (head)`** — a **single, non-branching head**. `alembic history` shows a linear chain: `b2c3d4e5f6a7 -> f9a3c7e1b5d2 (membership_approval_authority)`, `a1b2c3d4e5f6 -> b2c3d4e5f6a7 (tenant_registry)`, `c7e2b5a9f1d4 -> a1b2c3d4e5f6 (authority_holders)`, … No branch, no orphan. (`b2c3d4e5f6a7` / `a1b2c3d4e5f6` are the uncommitted WP-16 migrations; the WP-18 migration correctly chains off the most recent.)
- No regression to any WP-02 / WP-03 certified schema — no such object is referenced by the migration except as an unmodified FK target.

**Conclusion: Pass.** Canonical-schema conformant; strictly additive; single non-branching Alembic head `f9a3c7e1b5d2`.

### F. Testing — run for real

**Checked:** independent fresh runs, `JWT_SECRET_KEY` set in the environment as `CERT-WP-16` did.

**Command:** `./venv/Scripts/python.exe -m pytest tests/test_approval_authority_resolver.py tests/test_membership_approval_authority_service.py -v`
**Actual output:** `30 passed, 1 warning in 13.66s` — 22 in `test_approval_authority_resolver.py`, 8 in `test_membership_approval_authority_service.py`, every named test PASSED. (The one warning is a pre-existing `StarletteDeprecationWarning` about `httpx`, unrelated.)

**Command:** `./venv/Scripts/python.exe -m pytest -q` (full AuthService suite)
**Actual output:** `853 passed, 52 warnings in 356.95s (0:05:56)` — exit code 0. Independently reproduces the `IMP-REPORT-WP-18 §4` figure of 853 (823 pre-existing + 30 new). All 52 warnings are pre-existing deprecation warnings (`HTTP_422_UNPROCESSABLE_ENTITY`, `StarletteDeprecationWarning`), none WP-18-related, none a failure.

**`TDS-018 §29.6` minimum obligations — each exercised by a real, passing test:**
- `ANY_ONE` + valid, currently-effective binding → `AUTHORIZED` — `test_any_one_with_valid_binding_authorizes`, `test_binding_open_ended_and_currently_effective_authorizes`.
- `MAJORITY` + valid binding → `UNSUPPORTED_STRATEGY`, never `AUTHORIZED` — `test_unsupported_strategy_with_valid_binding_never_authorizes[MAJORITY-60]`.
- `ALL` + valid binding → `UNSUPPORTED_STRATEGY`, never `AUTHORIZED` — `[ALL-None]`.
- `SEQUENTIAL` + valid binding → `UNSUPPORTED_STRATEGY`, never `AUTHORIZED` — `[SEQUENTIAL-None]`.
- Malformed config (`MAJORITY`, NULL threshold) → `INVALID_CONFIGURATION`, unreachable via a qualifying binding — `test_malformed_majority_configuration_denies_before_binding_check`.
- `NO_AUTHORITY_CONFIGURED`, `INACTIVE_AUTHORITY` (×3: SUPERSEDED/DEPRECATED/RETIRED), `INVALID_SCOPE`, `NO_ELIGIBLE_ACTOR`, `INACTIVE_MEMBERSHIP` — each has a dedicated passing test; plus `NO_ELIGIBLE_ACTOR` vs `NO_AUTHORITY_CONFIGURED` distinction, effective-date boundary cases (not-yet-effective, expired, open-ended), and audit-content assertions for both `SUCCESS` and `DENIED`.

**`CLAUDE.md §21.4` Mandatory Tenant-Isolation Test Checklist:**
- **(a) two distinct, unrelated Organizations with no shared row** — the `org_a` / `org_b` fixtures in both test files create fully separate Organization + Membership + Person + Role graphs.
- **(b) a caller in one Organization cannot retrieve or infer another Organization's data** — `test_organization_mismatch_denies` and `test_cross_organization_binding_attempt_rejected` (resolution time); `test_bind_cross_organization_rejected` (bind time), which additionally asserts no row was created.
- **(c) explicit probe of a foreign-object identifier not derived from the caller's own claims** — `test_cross_organization_binding_attempt_rejected` passes Org B's `organization_id` as `target_organization_id` while the caller claims Org A → `INVALID_SCOPE`, never reaching a binding lookup; `test_bind_cross_organization_rejected` passes Org B's `approval_authority_id` to `bind()` for an Org A Membership → 409, no row. The resolver never accepts a caller-supplied `approval_authority_id` at all — the authority is looked up by `(target_organization_id, authority_name)`.

WP-18 charters no HTTP endpoint (Option B, infrastructure-only, backend-only per charter §21), so `§21.4`'s endpoint-oriented checklist is satisfied at the resolver and service layer instead — a reasonable adaptation, consistent with the charter §18 and mirroring `CERT-WP-16`'s own treatment of the same situation.

**Conclusion: Pass.** 30/30 dedicated tests and 853/853 full regression pass, independently re-run. Every `§29.6` and `§21.4` obligation is exercised by a real, passing test.

### G. Scope Containment

**Checked:** grep of every WP-18 implementation file for License/Entitlement/Subscription/Billing/C-023/Group terminology; `git status` for the presence of any out-of-scope object; direct read of the `AuthorityHolder` `CheckConstraint` and the Runtime Engine `ApprovalAuthorityResolver` stub.

**Result:**
- **No C-023 implementation** — grep of the 7 WP-18 files for `license|entitlement|subscription|billing|C-023` returns exactly one hit: a code comment in `test_approval_authority_resolver.py` naming C-023 as a hypothetical future consumer. Zero implementing code.
- **No WP-17 implementation** — no `WP-17` / Entitlement-Context file appears in the WP-18 change set.
- **No frontend / UI** — none in the file set (charter §21 designates the WP backend-only).
- **No Group infrastructure** — grep for `group_registry|group_membership|group_approval` in the WP-18 files: zero hits.
- **`AuthorityHolder` untouched** — `models/authority_holder.py` is not in the WP-18 file set (it is a pre-existing untracked WP-16 file); its `CheckConstraint("authority_identity IN ('AI-001', 'AI-002')")` is intact and unreferenced by any WP-18 file.
- **Runtime Authorization Engine untouched** — `git status --short Backend/Runtime/AuthorizationEngine/` returns nothing (no change). `authorization/tier_resolvers.py::ApprovalAuthorityResolver` remains `class ApprovalAuthorityResolver(BaseTierResolver)` with only a `TIER` ClassVar and no `resolve()` override — `BaseTierResolver.resolve` is `@abstractmethod` raising `NotImplementedError`, so the class remains an uninstantiable abstract stub. No M2–M6 work.
- **No `PLATFORM_ADMIN` / `AUREX_ADMIN` redesign** — the WP-18 dependency functions deliberately grant these no bypass; no existing admin dependency is modified (Finding C).
- **No unrelated capability change** — the WP-16 / C-040 tenant work, the `ROD-C040-*` / `ADR-024`–`035` / `AI-00x` artifacts, `CLAUDE.md`, `CAP-001`, `TECH-DEBT.md` (TD-157/158/159/160), and the other modified governance docs present in the working tree are all pre-existing uncommitted WP-16-and-earlier work — none is part of the WP-18 change set, and `IMP-REPORT-WP-18 §7` confirms WP-18's governance pass modified only the charter status lines and the `WPR-001` WP-18 row.

**Conclusion: Pass.** The WP-18 change set is confined to exactly the C-003 Approval Authority runtime-binding infrastructure.

### H. Change Control

**Checked:** `git rev-parse HEAD`, `git status --short`, `git diff --check`, `git diff --cached --stat` at repo root, before and after this review.

**Result:** HEAD unchanged at `e86192f95a1ef3534513f9fcee9418bbecb21baf` throughout. Nothing staged (`git diff --cached --stat` empty) before or after. `git diff --check` reports only pre-existing `LF will be replaced by CRLF` informational warnings — no whitespace errors, no conflict markers. This review modified no file except the creation of this certification artifact. The WP-18 implementation files and the `TDS-018` / charter / `IMP-REPORT-WP-18` / `WPR-001` changes are present in the working tree, uncommitted — the exact state being certified, per the `CERT-WP-16` precedent.

**Conclusion: Pass.**

---

## Material Findings

**None.** No `CLAUDE.md §19.8.5`-class defect (architectural / security / data-integrity / tenant-isolation defect; failing test; build failure; broken functionality; mandatory-compliance failure); no live non-struck stale-status contradiction re-creating M-1; no design non-conformance to `TDS-018 §29.2`; no out-of-scope implementation.

---

## Non-Material Observations (Non-Blocking)

**Observation 1 (Low) — two non-struck design-rationale phrases in `TDS-018`'s frozen historical body are now factually stale.** `§1` (Purpose) contains *"This mechanism does not exist anywhere in this codebase today, for any capability"* and `§4.2` contains *"Not implemented anywhere in `AuthService`"* (of `membership_approval_authority`) — both non-struck, both literally stale post-implementation. They sit inside `§§1–28`, which `§29`'s amendment note and `§31.1` both explicitly declare "preserved unchanged" / "not altered … in any way" as the historical record of the original design. They are design-motivation narrative, **not status-of-record assertions**, and the document's three current-status locations (the corrected header block, `§29.9`'s superseding note, and `§31.3`'s status table) are all correct and unambiguous — a reader cannot come away believing WP-18 is unauthorized or uncertified. This does **not** recreate M-1 (which was specifically about the header Status line and `§29.9`'s closing clause as status of record, both now fixed). Recommendation: at a convenient future documentation pass, add a brief forward-pointing note to the `§1` / `§4` headers (*"design-time snapshot; see `§31.3` for current status"*), mirroring the supersession notes `§10` / `§11` / `§20` already carry. Not required for Gate 1.

**Observation 2 (Low) — certified `ApprovalAuthorityService` retirement path does not yet see `membership_approval_authority` bindings as an active dependency.** Disclosed in `IMP-REPORT-WP-18 §5`: `ApprovalAuthorityRepository.get_active_dependents()` / `has_active_dependents()` still carry a docstring stating the join table "is not yet implemented anywhere in AuthService" (now stale), and neither method was extended to query the new table — so an Approval Authority with open bindings can currently be retired without that check catching it. This is **correct scope confinement**: the charter §19 lists "Modification of certified Approval Authority CRUD behavior" as explicitly out of scope, WP-18 correctly left `ApprovalAuthorityService` untouched, and the resolver handles the resulting state safely — a `RETIRED` / `SUPERSEDED` / `DEPRECATED` authority yields `INACTIVE_AUTHORITY` (DENY) at step 1, so no false authorization and no data-integrity violation results (orphaned-pointing binding rows simply resolve to DENY). It is a completeness gap in a certified adjacent capability, not a WP-18 defect. Recommendation: reconcile the stale `TD-028` docstring / register note in a future Work Package that touches `ApprovalAuthorityService`. Not blocking.

**Observation 3 (Low) — the two `IMP-REPORT-WP-18 §5` follow-up items are recorded only in the Implementation Report, not in `TECH-DEBT.md`** (`CLAUDE.md §19.8.2`: Technical Debt "SHALL NOT exist solely within … implementation reports"). Both relate to pre-existing register entries — `TD-028` (the stale retirement-dependency docstring, Observation 2) and `TD-096` (the shared SQLite harness not enforcing `PRAGMA foreign_keys=ON`). The third `§5` item (the config-validation check covers only the `MAJORITY`-with-NULL-threshold shape `TDS-018 §19` itself names as the example) is already covered by `TDS-018 §9`/`§29.5`'s standing disclosure that `ALL`/`SEQUENTIAL` semantics are genuinely undesigned. Recommendation: add a one-line cross-reference to the `TD-028` and `TD-096` register entries noting WP-18's interaction, at a convenient pass. Low; not blocking.

**Observation 4 (informational) — repository-wide test-harness fidelity limits (`TD-096` / `TD-159` / `TD-160`).** The in-memory SQLite harness used by `conftest.py` does not enforce foreign keys by default, auto-selects `StaticPool` (a single shared connection, so true cross-connection concurrency is not reproduced), and the session override skips production commit/rollback wrapping. WP-18's new foreign keys and its partial unique index `ux_membership_approval_authority_active` are therefore not fully exercised at the database-constraint level under this harness — the same limitation every prior Work Package's tables face. This is a known, tracked, repository-wide item (explicitly earmarked for the Gate 2 V&V Audit's harness/fixture production-parity checklist per `CLAUDE.md §19.7b`), **not introduced or worsened by WP-18**, and not a Gate 1 blocker. Noted here so the Gate 2 reviewer picks it up for WP-18's constraints specifically.

---

## Governing Documents Cross-Check Summary

| Item | Charter / IMP-REPORT claim | Independently verified | Result |
|---|---|---|---|
| Dedicated tests | 30 (22 resolver + 8 service) | 30 passed, re-run fresh (`13.66s`) | Match |
| Full regression | 853 (823 + 30) | `853 passed, 52 warnings in 356.95s`, re-run fresh | Match |
| Alembic head | Single, `f9a3c7e1b5d2`, down_revision `b2c3d4e5f6a7` | Single non-branching head `f9a3c7e1b5d2`; history linear | Match |
| Resolver algorithm | `TDS-018 §29.2` 8-step, exact order | Traced line-by-line; config validation before strategy gate before caller steps | Match |
| Reason taxonomy | `TDS-018 §29.4` 8 labels | Enum carries exactly those 8 | Match |
| `MAJORITY`/`ALL`/`SEQUENTIAL` | Denied `UNSUPPORTED_STRATEGY`, never resolved | Confirmed by code read + parametrized tests | Match |
| Admin bypass | None (deliberate divergence from `enforce_domain_permission`) | Confirmed by code read + `PLATFORM_ADMIN`/`AUREX_ADMIN` tests | Match |
| Cross-Org bind | Rejected 409, no row created | Confirmed by service read + `test_bind_cross_organization_rejected` | Match |
| Cross-Org resolution | `INVALID_SCOPE` at step 4; target from `X-Tenant-ID`, not claims | Confirmed via `get_current_tenant` read + tests | Match |
| Modified files additive | `models/__init__.py`, `approval_authority_repository.py`, `dependencies.py` | `git diff` — all additive, no existing symbol changed | Match |
| Canonical schema | `Master_Technical_Architecture.md` 1319–1329, composite PK | Column-by-column match | Match |
| Scope containment | No C-023 / WP-17 / frontend / Group / Engine / AuthorityHolder change | Confirmed by grep + `git status` + stub read | Match |
| M-1 stale status | Eliminated (strikethrough-preserve + `§31`) | grep — no non-struck status-of-record contradiction | Match |

No discrepancy was found between what the charter / `IMP-REPORT-WP-18` claim and what the actual repository state shows.

---

## Change-Control Verification

**Before this review:**
```
git rev-parse HEAD        -> e86192f95a1ef3534513f9fcee9418bbecb21baf
git status --short        -> 126 entries (10 modified tracked files under Backend/Services/AuthService;
                             8 modified tracked governance/CLAUDE files; remainder untracked —
                             WP-16/C-040 governance artifacts, WP-18 backend + governance files, etc.)
git diff --check          -> only "LF will be replaced by CRLF" informational warnings; no whitespace/conflict errors
git diff --cached --stat  -> (empty — nothing staged)
```

**After this review:**
```
git rev-parse HEAD        -> e86192f95a1ef3534513f9fcee9418bbecb21baf   (unchanged)
git status --short        -> 127 entries (identical set; the one added line is this certification
                             file itself, a new untracked file)
git diff --check          -> only "LF will be replaced by CRLF" informational warnings; no whitespace/conflict errors
git diff --cached --stat  -> (empty — nothing staged)
```

Nothing was staged, committed, or pushed. The only repository change made by this certification is the creation of this file. No `Backend/` implementation file, migration, test, `TDS-018`, the WP-18 charter, `IMP-REPORT-WP-18`, `WPR-001`, `IRA-C023`, `TDS-C023`, or the `WP-17` charter was modified by this review.

---

## Final Determination

### CERTIFIED — PASS WITH OBSERVATIONS

WP-18 (Bind and Resolve Approval Authority, C-003) is **CERTIFIED at Gate 1**. The implementation faithfully realizes `TDS-018 §29.2`'s corrected 8-step resolver algorithm in exact order — configuration validation before the strategy gate before all caller-specific steps; `approval_strategy != ANY_ONE` terminating with `DENY`/`UNSUPPORTED_STRATEGY` before any caller-specific evaluation; `ALL`/`MAJORITY`/`SEQUENTIAL` denied, never counted, simulated, or approximated; every branch fail-closed with no `PLATFORM_ADMIN`/`AUREX_ADMIN` fallback; the `§29.4` 8-label reason taxonomy exact. Tenant isolation is independently enforced at bind time (service-layer 409) and at resolution time (step-4 scope check against an `X-Tenant-ID`-derived target independent of caller claims). The `membership_approval_authority` model and migration match the canonical `Master_Technical_Architecture.md` schema exactly, are strictly additive, and yield a single non-branching Alembic head `f9a3c7e1b5d2`. Every modified tracked file's WP-18 change is purely additive. All 30 dedicated tests and the full 853-test AuthService regression pass, independently re-run (`13.66s` and `356.95s` respectively), and every `TDS-018 §29.6` and `CLAUDE.md §21.4` obligation is exercised by a real passing test. The former "M-1" governance-traceability blocker is genuinely eliminated: `TDS-018`'s status-of-record locations are reconciled with strikethrough-preserve + a new `§31`, and the charter, `IMP-REPORT-WP-18`, and `WPR-001` all consistently state IMPLEMENTATION AUTHORIZED / IMPLEMENTATION COMPLETE / NOT YET CERTIFIED. Scope is confined to C-003 Approval Authority runtime-binding infrastructure — no C-023, no WP-17, no frontend, no Group infrastructure, no `AuthorityHolder` modification, no Runtime Engine M2–M6 work, no admin redesign. Four Low-severity / informational non-material observations are recorded, none blocking.

**No `CLAUDE.md §19.8.5`-class defect was found.** WP-18 may proceed to Gate 2 (V&V Audit) in this reviewer's judgment.

### Gate scope and residual status

- **This is Gate 1 only** (Independent Certification, `CLAUDE.md §19.7`/`§19.7b`). **Gate 2 (V&V Audit) and Gate 5 (Release Readiness Audit) were NOT performed and are NOT passed.** Gates 3–4 (remediation and its independent verification) are triggered only if Gate 2 finds a defect.
- **WP-18 is NOT fully released.** Certification of the full five-gate sequence is not complete; nothing is committed or pushed.
- **C-023 remains 🔴 RED — NOT IMPLEMENTATION READY.** Unchanged by WP-18 or by this certification.
- **WP-17 remains CHARTERED — NOT IMPLEMENTED, NOT CERTIFIED.** Unchanged by WP-18 or by this certification.
- `IRA-C023`, `TDS-C023`, and the `WP-17` charter were confirmed untouched by the WP-18 change set.

---

## Change Control

**Files read (not modified) in preparing this certification:** every governing document and every backend/test file listed under "Scope and Method" and "Governing Documents Reviewed".

**Files created by this certification:** this document only — `architecture/06-Reviews/CERT-WP-18_Approval_Authority_Runtime_Binding.md`.

**Files modified:** none. No application code, schema, migration, ADR, `TDS-018`, the WP-18 charter, `IMP-REPORT-WP-18`, `WPR-001`, `TECH-DEBT.md`, `CAP-001`, `IRA-C023`, `TDS-C023`, the `WP-17` charter, or any other governance document was modified.

**Not performed:** no V&V Audit; no Release Readiness Audit; no WP-18 closure; no remediation; no `membership_approval_authority` row created; no `authority_holders` row created or modified; no Group infrastructure created; no C-023 / WP-17 work; no commit; no push.
