# CERT-WP-05 — Independent Certification

## Access Management (C-002), Minimum Scope

**Certification Type:** Independent Work Package Certification (CLAUDE.md §19.7, "Independent Certification")
**Work Package:** WP-05 — Access Management (C-002), authorized minimum scope (`IRA-005 §12`)
**Certifying party:** Independent certification pass performed by a fresh-context reviewer with no prior involvement in WP-05's implementation, per CLAUDE.md §19.7 / ADR-014's explicit prohibition on self-certification. Every material claim below was re-derived directly against source code, migrations, and test execution — none is taken on faith from `IMP-REPORT-WP-05_Access_Management.md` or any other implementation-session document.
**Date:** 2026-07-30
**Inputs certified against:** `CLAUDE.md` (§14, §16, §17, §19.1–§19.8), `IRA-005_WP-05_Access_Management_Implementation_Readiness_Assessment.md` (full, including §11 Lifecycle Model and §12 authorized minimum scope), `ADR-015_Access_Evaluation_Outcome_Canonical_Business_Object_Registration.md`, `IMP-REPORT-WP-05_Access_Management.md`, `TECH-DEBT.md` (TD-079, TD-080, and the §19.8.7 severity rubric), `WP-REG-001_Enterprise_Work_Package_Register.md` (§5, §6, §9), `CERT-WP-04_Enterprise_Structure_Management.md` and `CERT-WP-RTA-001_Authorization_Runtime_Engine.md` (precedent for review rigor and structure), and direct inspection of all eight WP-05 source files, the migration, both test files, `git diff`/`git status`, an independent full-suite test run, and an independent `alembic heads` run.

---

## 1. Executive Summary

WP-05 implements Access Management (C-002) at the explicitly authorized minimum scope recorded in `IRA-005 §12`: BA-01 (Evaluate Access for a Governed Request) limited to its Unresolved/Deferred branches; BA-02 (Preserve/Expire) and BA-04 (Hand-off Rejection Classification) in full; BA-03 (Detect and Resolve Access Context Change) limited to its classification/detection portion. Permitted/Denied determination is deliberately excluded — `WP-RTA-001` has no production `TierResolver` yet — and this is the single hard security requirement CLAUDE.md §19.8.5 makes non-negotiable: a false Permitted outcome would be a security defect, not deferrable Technical Debt.

Independent re-verification confirms:

- **598/598 backend tests pass**, re-run independently (not taken from the Implementation Report) via `JWT_SECRET_KEY=ci-test-secret-key-not-for-production venv/Scripts/python.exe -m pytest tests/ -v`, matching the Report's own claimed figure exactly.
- **Exactly one Alembic head** (`f3a7c5e9b2d8`), independently re-run via `alembic heads`, chained onto WP-04's own last migration (`e6c1b3a9d7f2`).
- **`AccessEvaluationService.evaluate()` was traced line by line and contains no code path that returns, creates, or otherwise produces an outcome of type `PERMITTED` or `DENIED`.** Its only three exit paths are: (1) 404 if the target Domain does not exist; (2) a created `UNRESOLVED` outcome if the Membership is missing or not `ACTIVE`; (3) a created `DEFERRED` outcome if an `ACTIVE`, `DOMAIN`-scoped Approval Authority governs the Domain; (4) `HTTPException(status_code=501)` for every remaining case, with a detail message naming IRA-005 §12 as the reason. `AccessEvaluationOutcomeType.PERMITTED`/`.DENIED` are declared on the enum and the CheckConstraint (schema completeness, matching the TD-052-class precedent already established at WP-04) but are never referenced by any executable statement in `services/access_evaluation_service.py`, confirmed by direct search.
- **`BA-03`'s `detect_context_change()` never calls `evaluate()` or anything resembling a fresh re-resolution.** It only transitions `validity_status` to `INVALIDATED` for a live (`CREATED`/`PRESERVED`) outcome and returns `re_evaluation_required=True`; the caller's own next step (a fresh BA-01 call) is never auto-triggered.
- **`BA-04`'s classification genuinely bases its decision on the outcome's own `validity_status` alone.** `request.stated_reason` and `request.reporting_capability` are recorded into `record_audit()`'s metadata for traceability but are never read by the `if outcome.validity_status in _LIVE_VALIDITY_STATUSES` branch that determines `CAPABILITY_SCOPED_INSUFFICIENCY` vs. `INTEGRITY_SIGNAL` — confirmed by reading the method body, and independently confirmed by the unit test that passes an unrelated `stated_reason` string in both branches and gets the validity-status-determined classification back regardless.
- **The `CheckConstraint` strings on the model's `__table_args__` and the migration's `op.create_table()` are character-for-character identical** for `outcome_type`, `validity_status`, and `permission_level` — no model/migration drift (the TD-004-class defect from WP-01 is not repeated here).
- **`git diff` on `main.py`/`middleware/tenant.py` confirms only the `access_evaluation` router registration and the `/access-evaluations` tenant-exemption entry were added** — no other route, middleware behavior, or unrelated line was touched. `git status` confirms only WP-05's own eight new source files, the migration, two test files, and IRA-005/IMP-REPORT-WP-05/TECH-DEBT/WP-REG-001 documentation changes are uncommitted; no unrelated file is part of this Work Package's own change set (the separately-disclosed pre-existing WP-RTA-001 uncommitted work in `Backend/Runtime/` is out of this Work Package's scope and was not touched).
- **All five `/access-evaluations` endpoints are gated by `require_platform_admin`**, confirmed by direct inspection of every route decorator in `routers/access_evaluation.py`. `TD-079` accurately and non-overstatedly describes this as the same class of interim gate already accepted at TD-021 through TD-025/TD-031/TD-034/TD-035/TD-036/TD-039/TD-042 — no privilege-escalation risk beyond what `PLATFORM_ADMIN` already holds platform-wide.
- **Audit trail completeness confirmed**: every branch of every one of the four Business Activities — including both `_get_or_404` failure paths, the 404-domain and 409-wrong-state paths, and every success path — calls `record_audit()` before returning or raising.

**One newly-identified, non-blocking finding** (§4.4, now `TD-081`): the API-level test suite (`test_access_evaluation_api.py`) exercises only one branch of several two-branch service behaviors (BA-04's `INTEGRITY_SIGNAL` classification, BA-02's expire-without-preserve 409, BA-03's non-live-outcome 409 are each covered at the unit layer only, not the API layer). This mirrors the identical, already-accepted disposition CERT-WP-04 recorded for three of its own seven API suites missing an invalid-token 401 test — a narrow test-completeness gap, not an untested code path or a missing control.

None of the findings below is a data-integrity, tenant-isolation, security, or build-breaking defect within C-002's own authorized minimum-scope boundary, and none fabricates or approximates a Permitted/Denied outcome.

## 2. Certification Decision

**CERTIFIED — PASS WITH OBSERVATIONS**

---

## 3. Scope Reviewed

**Governance documents:**
- `CLAUDE.md` (§14 Definition of Done, §16 Canonical Authority Resolution, §17 Canonical Document Compliance, §19.1–§19.8, especially §19.7 Business Activity Completion Gate and §19.8.5's security-defect-cannot-be-Technical-Debt rule)
- `architecture/05-Implementation/IRA-005_WP-05_Access_Management_Implementation_Readiness_Assessment.md` (full — §1–§12, including §5's Business Object eligibility analysis, §7's Gap Analysis, §9's readiness decision, §11's `AEO-000001` registration entry, and §12's repository-owner authorization to begin at minimum scope)
- `architecture/07-Decisions/ADR-015_Access_Evaluation_Outcome_Canonical_Business_Object_Registration.md`
- `architecture/05-Implementation/IMP-REPORT-WP-05_Access_Management.md` (full — every claim independently re-verified, not taken on faith)
- `architecture/06-Reviews/TECH-DEBT.md` (TD-079, TD-080 detailed entries, and the §19.8.7 severity rubric they were judged against)
- `architecture/00-Governance/WP-REG-001_Enterprise_Work_Package_Register.md` (§5 WP-05 row, §6 Current Active Work Package, §9 Change History)
- `architecture/06-Reviews/CERT-WP-04_Enterprise_Structure_Management.md` and `architecture/06-Reviews/CERT-WP-RTA-001_Authorization_Runtime_Engine.md` (precedent for review structure and rigor)

**Source code read in full (independent verification):**
- `Backend/Services/AuthService/models/access_evaluation_outcome.py`
- `Backend/Services/AuthService/repositories/access_evaluation_outcome_repository.py`
- `Backend/Services/AuthService/schemas/access_evaluation.py`
- `Backend/Services/AuthService/services/access_evaluation_service.py` (every method, traced line by line for BA-01's own outcome-branch completeness)
- `Backend/Services/AuthService/routers/access_evaluation.py` (every endpoint decorator)
- `Backend/Services/AuthService/alembic/versions/2026_08_09_0900-f3a7c5e9b2d8_access_evaluation_outcome.py`
- `Backend/Services/AuthService/tests/test_access_evaluation_service.py` (15 tests) and `Backend/Services/AuthService/tests/test_access_evaluation_api.py` (11 tests)
- `Backend/Services/AuthService/dependencies.py` (`require_platform_admin`/`get_current_claims`, to confirm the authorization gate's actual behavior, not just its name)
- `Backend/Services/AuthService/observability.py` (`record_audit`/`publish_event`/`AuditStatus` signatures, to confirm every call site in the new service matches)
- `git diff Backend/Services/AuthService/main.py Backend/Services/AuthService/middleware/tenant.py` and `git status --porcelain` (full repository, to confirm WP-05's own change set is scoped as claimed)
- Actual `pytest tests/ -v` execution (598 passed, independently re-run) and actual `alembic heads` execution (single head `f3a7c5e9b2d8`, independently re-run)

---

## 4. Findings

### 4.1 Architecture / Scope Conformance

- BA-01's `evaluate()` was read in full. Its only code paths are: 404 (unknown Domain) → `UNRESOLVED` (unknown or non-ACTIVE Membership) → `DEFERRED` (ACTIVE DOMAIN-scoped Approval Authority governs the Domain) → `HTTPException(501)` (every remaining case). No branch constructs an `AccessEvaluationOutcome` with `outcome_type="PERMITTED"` or `"DENIED"`, and no branch returns any value approximating a decision. The 501 path's `detail` message explicitly cites IRA-005 §12 and CLAUDE.md §19.8.5, matching the disclosure the IRA itself requires.
- `AccessEvaluationOutcomeType.PERMITTED`/`.DENIED` and `AccessEvaluationValidityStatus.SUPERSEDED` are declared on their respective enums and included in the database `CheckConstraint`s, but a direct search of `services/access_evaluation_service.py` confirms neither `.PERMITTED`, `.DENIED`, nor `.SUPERSEDED` is referenced anywhere in executable code — only in docstrings explaining why they are declared but unused. This is the same "declare the full registered Lifecycle Model, write only the authorized subset" discipline already established at WP-04 (TD-052/TD-057/TD-062/TD-065/TD-069), correctly mirrored here rather than narrowed to a non-conforming partial enum.
- BA-03's `detect_context_change()` contains no call to `evaluate()`, no construction of a new `AccessEvaluationOutcome`, and no reference to `AccessEvaluationOutcomeType` at all — it only reads and writes `validity_status`/`reason` on the existing row. `re_evaluation_required` is a static `True` on the response schema, description text confirming the caller (not this method) performs the next evaluation.
- BA-04's `resolve_handoff_rejection()` branches solely on `outcome.validity_status in _LIVE_VALIDITY_STATUSES`. `request.stated_reason` and `request.reporting_capability` appear only inside the `record_audit()` metadata dict on both branches — never in the `if` condition, never in `explanation`'s classification-determining logic (only in the fixed english template). This is a genuine mirror of WP-02 BA-10's own "signal, not authority" discipline, not merely a claimed one.
- `git diff` of `main.py` shows exactly one added import-list entry (`access_evaluation`) and one added `app.include_router(...)` line. `git diff` of `middleware/tenant.py` shows exactly one added comment block and one added `or path == "/access-evaluations" or path.startswith("/access-evaluations/")` clause appended to the existing exemption `if`. No other line in either file changed. No new architectural component, entity, table, or service boundary beyond `AEO-000001`'s own single table was introduced.
- `git status --porcelain` at the repository root shows the WP-05 change set is exactly: the eight new/modified `Backend/Services/AuthService` implementation and test files listed in IMP-REPORT-WP-05's own "Documents Updated" section, plus `IRA-005` (§12's authorization addendum), `IMP-REPORT-WP-05`, and `TECH-DEBT.md`. The pre-existing uncommitted `Backend/Runtime/` (WP-RTA-001) and several architecture-audit documents are present but untouched by any WP-05 file — confirmed by diffing only the files WP-05 claims, not by assuming the broader working tree is WP-05's own.

### 4.2 Business Activities (BA-01 through BA-04)

| BA | Claim | Independent finding |
|---|---|---|
| BA-01 | Unresolved/Deferred only; 501 for anything else; never fabricates Permitted/Denied | Confirmed by full line-by-line trace (§4.1). Structural 404 pre-check on Domain existence confirmed to mirror `DomainPermissionService.establish()`'s own precedent (`domain_repo.get_by_id()` called first, before any Membership check). |
| BA-02 | `CREATED → PRESERVED → EXPIRED`, each transition guarded by 409 | Confirmed — `preserve()` rejects any non-`CREATED` outcome with 409 before mutating; `expire()` rejects any non-`PRESERVED` outcome with 409 before mutating. Both guards checked before the `outcome_repo.update()` call, not after. |
| BA-03 | Classification/detection only; never re-resolves | Confirmed (§4.1) — no `evaluate()` call, no new outcome created, only `validity_status`/`reason` mutated on the existing row, gated by `_LIVE_VALIDITY_STATUSES` membership with 409 otherwise. |
| BA-04 | Classifies on `validity_status` alone, never on `stated_reason` | Confirmed (§4.1) and confirmed by test (`test_resolve_handoff_rejection_classifies_invalidated_outcome_as_integrity_signal` passes an unrelated `stated_reason` and still gets `INTEGRITY_SIGNAL`). |

No Business Activity was found to exceed its own IRA-005 §12-authorized scope, and none was found to fall short of it (i.e., no Unresolved/Deferred/Preserve/Expire/classification behavior required by IRA-005 §12 is missing).

### 4.3 Data Model / Migration

- Model `__table_args__` and migration `op.create_table()` CheckConstraints for `outcome_type`, `validity_status`, and `permission_level` are textually identical (confirmed by direct side-by-side comparison of the two files) — no model/migration drift of the kind TD-004 previously found at WP-01.
- Foreign keys (`membership_id` → `memberships.id` CASCADE, `domain_id` → `domains.id`, `approval_authority_id` → `approval_authorities.id`, nullable) all target tables that already existed as of this migration's own `down_revision` (`e6c1b3a9d7f2`) — confirmed no forward-reference to a not-yet-existing table.
- `alembic heads` independently re-run: exactly one head, `f3a7c5e9b2d8`.

### 4.4 Testing

- **598/598 tests pass**, independently re-run in this certification pass (`JWT_SECRET_KEY=ci-test-secret-key-not-for-production venv/Scripts/python.exe -m pytest tests/ -v`) — matches IMP-REPORT-WP-05's own claimed figure exactly; not taken on faith.
- 15 unit tests (`test_access_evaluation_service.py`) independently confirmed to cover: 404 unknown domain, UNRESOLVED for unknown membership, UNRESOLVED for inactive membership, DEFERRED with populated `approval_authority_id`, 501 for the remaining case; both BA-02 transitions plus both their 409 guards; both BA-03 outcomes (invalidate, and reject a second invalidation with 409); both BA-04 classifications plus the 404 case.
- **New finding (non-blocking, recorded as `TD-081`):** `test_access_evaluation_api.py` (11 tests) exercises only one branch of several two-branch behaviors already fully covered at the unit layer: BA-04's `handoff-rejection` endpoint is tested only for the live-outcome (`CAPABILITY_SCOPED_INSUFFICIENCY`) path, not the invalidated-outcome (`INTEGRITY_SIGNAL`) path; BA-02's `expire` endpoint's own 409 is tested only for double-preserve, not for expire-without-preserve; BA-03's `context-change` endpoint is tested only for its invalidating path, not its own 409 rejection of a non-live outcome. This is a narrow API-layer coverage gap — every branch it omits is independently proven correct at the unit layer — and mirrors the identical, already-certified-as-non-blocking disposition CERT-WP-04 recorded for three of its own seven API suites missing an invalid-token 401 test.
- Separately, `test_access_evaluation_api.py` itself has no explicit invalid-Bearer-token 401 test (only the 400 missing-header and 403 wrong-role cases). This is consistent with the majority of this repository's own API test files (only 8 of the full suite's API test modules include this specific case) — a pre-existing, repository-wide pattern, not a WP-05-specific regression, and not severe enough on its own to warrant a new register entry distinct from the already-established precedent.
- Test assertions were spot-checked for weakness (e.g., status-code-only assertions masking a wrong response shape): both API and unit tests consistently assert on response body fields (`outcome_type`, `validity_status`, `approval_authority_id`, `classification`, `object_preserved`, `routed_to`) in addition to status codes, not status codes alone.

### 4.5 Tenant Isolation and Security

- All five `/access-evaluations` endpoints (`POST /access-evaluations`, `POST /{id}/preserve`, `POST /{id}/expire`, `POST /{id}/context-change`, `POST /{id}/handoff-rejection`) carry `claims: Annotated[dict, Depends(require_platform_admin)]` — confirmed by direct inspection of every route decorator in `routers/access_evaluation.py`, not merely grepped for the string.
- `require_platform_admin`/`get_current_claims` (`dependencies.py`) were read directly: 400 for a missing/malformed `Authorization` header, 401 implicitly via `decode_access_token()` for an invalid/expired token (not separately tested for this router, §4.4), 403 for a valid, non-`PLATFORM_ADMIN` claim. No bypass path exists.
- The `/access-evaluations` tenant-exemption entry is accurately disclosed in both `middleware/tenant.py`'s own comment and `TD-079`: this data is genuinely organization-scoped (one hop via `membership_id`), and the exemption exists only because `PLATFORM_ADMIN` is the sole caller today — the same interim disclosure already accepted for `/domain-permissions` and every other prior WP's PLATFORM_ADMIN-only endpoint. No new tenant-isolation weakening beyond the already-accepted precedent was found.
- Audit-trail completeness (§4.6) closes the observability half of the security posture — every decision, including every rejection, is recorded.

### 4.6 Audit Trail Completeness

Every code path in `services/access_evaluation_service.py` was checked for a `record_audit()` call before returning or raising:

- `evaluate()`: unknown-domain 404, UNRESOLVED success, DEFERRED success, and the 501 decline — all four call `record_audit()`.
- `preserve()`/`expire()`: the shared `_get_or_404()` helper calls `record_audit()` on 404; each method additionally calls it on its own 409-guard rejection and on success.
- `detect_context_change()`: 404 (via `_get_or_404()`), 409 rejection, and success all call `record_audit()`.
- `resolve_handoff_rejection()`: 404 (via `_get_or_404()`) and the single success path (covering both classification branches) call `record_audit()`, recording `reporting_capability`, `stated_reason`, and the computed `classification`.

No code path was found that mutates state or returns a decision without a corresponding audit record.

### 4.7 Documentation

- IMP-REPORT-WP-05's "Documents Updated," "Validation," and "Status" sections were checked claim-by-claim against actual source, actual test output, and actual `alembic heads` output — every claim independently confirmed accurate, including the specific 598/598 figure.
- `TD-079` and `TD-080`'s detailed entries were checked against the actual router/test code they describe and found accurate and non-overstated — `TD-079` correctly scopes the gap to "no distinct, enforceable persona claim exists," not a broken control; `TD-080` correctly scopes the missing-`GET`-endpoint gap to "no current consumer needs it."
- **Minor observation (non-blocking, documentation only):** `WP-REG-001 §10` ("Repository Statistics") still reads "WP-05 ... BA-01 implementation not yet begun," stale relative to the same document's own `§6`/`§9` rows, which correctly state all four Business Activities are implementation-complete pending Independent Review. This is an internal staleness within the governance register itself (not an implementation defect), naturally correctable in the same governance pass that will record this certification's outcome — noted here for completeness rather than left for a future reviewer to rediscover.

---

## 5. Risks

None of the following is a data-integrity, tenant-isolation, security, or build-breaking defect, and none fabricates or approximates a Permitted/Denied determination:

1. `TD-079` (Low) — all five `/access-evaluations` endpoints gate on `PLATFORM_ADMIN` only, no C-002-specific persona claim exists yet. Same accepted class as nine prior TD entries across WP-02/WP-03.
2. `TD-080` (Low) — no `GET /access-evaluations/{id}` read endpoint exists yet. Same accepted class as five prior TD entries across WP-04.
3. `TD-081` (Low, newly raised by this certification) — API-level test suite exercises only one branch of several two-branch behaviors already fully proven at the unit layer. Narrow, non-blocking, same class CERT-WP-04 already accepted for its own API suites' 401-test gap.
4. `WP-REG-001 §10`'s stale "BA-01 implementation not yet begun" statistic (documentation-only, §4.7) — to be corrected in the same governance pass that records this certification.

**The one item this Work Package was constitutionally required to get right — never fabricating or approximating a Permitted/Denied Access Evaluation Outcome — was independently verified true by direct code trace, not merely by trusting the Implementation Report's own claim.**

---

## 6. Technical Debt Summary

| TD | Theme | Severity | Status |
|---|---|---|---|
| TD-079 | PLATFORM_ADMIN-only gate on all five `/access-evaluations` endpoints | Low | Open |
| TD-080 | No `GET` read endpoint for Access Evaluation Outcome | Low | Open |
| TD-081 (new, this certification) | API-layer test coverage narrower than unit-layer for several two-branch behaviors | Low | Open |

All three carry an owning Work Package, a related Business Activity, and an explicit resolution criterion in `TECH-DEBT.md`.

---

## 7. Recommendations

1. No action required to certify. The three open Low-severity Technical Debt items above are appropriately deferred, not blocking.
2. At the next convenient touch of `test_access_evaluation_api.py`, add the three missing branch-level API assertions described in `TD-081` — low cost, closes a real (if narrow) coverage gap, mirroring CERT-WP-04's own precedent recommendation for its own analogous gap.
3. Correct `WP-REG-001 §10`'s stale "BA-01 implementation not yet begun" line in the same governance pass that records this certification's outcome.
4. When a future Business Activity or governance decision eventually integrates a real `WP-RTA-001` `TierResolver`, BA-01's Permitted/Denied branches and BA-03's re-resolution path should each receive their own fresh, separately-scoped gap analysis (per `IRA-005 §12`'s own instruction) — not be silently added as an unreviewed extension of this Work Package's already-certified code.

---

## 8. Whether WP-05 May Be Marked "CLOSED — CERTIFIED"

**Yes.** This certification's decision is PASS WITH OBSERVATIONS. WP-05's own status in `WP-REG-001` (and `WPR-001`, if that document tracks WP-05) may now be updated from "Implementation Complete — Independent Review Pending" to **"CLOSED — Certified"**, with this document (`CERT-WP-05_Access_Management.md`) as the certifying artifact, and `TD-079`/`TD-080`/`TD-081` carried forward as this Work Package's own open Technical Debt — not resolved by closure, per CLAUDE.md §19.8.

*(Note: updating `WP-REG-001`'s and `WPR-001`'s own status lines and cross-reference columns, and committing this Work Package's own change set to git, are separate governance/repository actions this certification licenses but does not itself perform.)*

---

*End of CERT-WP-05.*
