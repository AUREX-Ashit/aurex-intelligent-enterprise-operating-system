# IMP-REPORT-WP-05 — Access Management (C-002)

**Work Package:** WP-05 — Access Management (C-002)
**Governing Readiness Assessment:** `IRA-005_WP-05_Access_Management_Implementation_Readiness_Assessment.md` (Accepted — WP-05 authorized to begin at **minimum scope only**, per IRA-005 §12 and the repository owner's own authorization): BA-01 limited to its Unresolved/Deferred branches (Permitted/Denied explicitly excluded — no real `TierResolver` exists in `WP-RTA-001` yet, per that Work Package's own Closure Report §7), BA-02 and BA-04 in full, BA-03 limited to its classification/detection portion only.
**Governing Business Object:** `AEO-000001` (Access Evaluation Outcome), registered by `ADR-015_Access_Evaluation_Outcome_Canonical_Business_Object_Registration.md`. Lifecycle Model = Outcome Type (PERMITTED/DENIED/UNRESOLVED/DEFERRED, fixed at creation) × Validity Status (CREATED → PRESERVED → {SUPERSEDED | INVALIDATED | EXPIRED}).
**Governing Capability Specification:** `PE-001-C002_Access_Management` (ERB-C002-01 Evaluate Access for a Governed Request; EX-C002-03 through EX-C002-08).
**Scope of this report:** BA-01 (Unresolved/Deferred branches only) through BA-04 — **all four Business Activities authorized by IRA-005 §12, completing WP-05's minimum-scope charter.** Permitted/Denied determination and the "re-resolve to a fresh determination" portion of BA-03 remain explicitly out of scope, pending a future, separately gap-analyzed integration with `WP-RTA-001`'s own Authorization Engine once a real `TierResolver` exists.

---

## BA-01 — Evaluate Access for a Governed Request (Unresolved/Deferred branches only)

### Business Activity Contract (IMP-001 §6.7)

- **Business Intent:** Produce an Access Evaluation Outcome recording why a governed request's access could not yet be resolved to Permitted/Denied — CAP-001's C-002 Business Intent ("Govern access rights"), scoped to the Unresolved/Deferred subset only (IRA-005 §12).
- **Input Contract:** `membership_id` (UUID, required), `domain_id` (UUID, required), `permission_level` (one of `DomainPermissionLevel`'s eight values, required).
- **Output Contract:** The created `AccessEvaluationOutcome` (id, membership_id, domain_id, permission_level, outcome_type, validity_status, reason, approval_authority_id, created_at, updated_at), or an HTTP error naming the specific violated rule.
- **Business Rules:**
  - EX-C002-03 — a request whose Membership cannot be confirmed to be in ACTIVE standing (missing, or present but not ACTIVE) cannot be resolved — produces `UNRESOLVED`.
  - EX-C002-04 — a request against a Domain governed by an ACTIVE, DOMAIN-scoped Approval Authority requires approval before resolution can proceed — produces `DEFERRED`, with `approval_authority_id` populated.
  - CLAUDE.md §19.8.5 — a Permitted/Denied determination requires a real URA-001-76 precedence-chain resolver, which does not exist in this repository (`WP-RTA-001` Closure Report §7, "Not production ready"). Rather than approximate or silently decline, any request reaching neither the Unresolved nor the Deferred branch raises **HTTP 501**, naming IRA-005 §12 as the reason — a false Permitted outcome would be a security defect, not deferrable Technical Debt.
- **Validation Rules:** Target Domain must already exist (structural pre-check, 404 if not — mirrors `DomainPermissionService.establish()`'s own precedent).
- **Authorization Rules:** `PLATFORM_ADMIN` role required — the same interim gate WP-01 through WP-04 all used. No PE-001-C002 persona exists as an enforceable claim today (same class of gap as TD-021–025/031/042/043).
- **Domain Events:** `ACCESS_EVALUATION_OUTCOME_CREATED` (outcome_id, outcome_type).
- **Audit Requirements:** `record_audit("EVALUATE_ACCESS", ...)` on every path (unknown domain, Unresolved, Deferred, and the 501 decline), per SD-002-054's seven audit questions.
- **Tests:** covered in `tests/test_access_evaluation_service.py` (5 tests) and `tests/test_access_evaluation_api.py` (7 tests) — see full test list below.

---

## BA-02 — Preserve and Bound Access Evaluation Outcome Validity

### Business Activity Contract (IMP-001 §6.7)

- **Business Intent:** Realize EX-C002-05/EX-C002-06 — an Access Evaluation Outcome's Validity Status must be explicitly, observably transitioned, never silently assumed.
- **Input Contract:** `outcome_id` (UUID path parameter); empty request body for both actions.
- **Output Contract:** The updated `AccessEvaluationOutcome`.
- **Business Rules:**
  - EX-C002-05 — Preserve: `CREATED → PRESERVED` only. A non-`CREATED` outcome cannot be preserved (409).
  - EX-C002-06 — Expire: `PRESERVED → EXPIRED` only, explicit and caller-invoked. A non-`PRESERVED` outcome cannot be expired (409). No automatic/time-based expiry is implemented — that would require a scheduler, a new architectural component out of this Work Package's own scope.
- **Authorization Rules:** `PLATFORM_ADMIN`, same as BA-01.
- **Domain Events:** `ACCESS_EVALUATION_OUTCOME_PRESERVED`, `ACCESS_EVALUATION_OUTCOME_EXPIRED`.
- **Audit Requirements:** `record_audit()` on every path (not-found, wrong-state, success).
- **Tests:** covered in `tests/test_access_evaluation_service.py` (5 tests) and `tests/test_access_evaluation_api.py` (2 tests).

---

## BA-03 — Detect and Resolve Access Context Change (classification/detection portion only)

### Business Activity Contract (IMP-001 §6.7)

- **Business Intent:** Realize EX-C002-07's classification/detection portion — a reported governing-fact change against a still-live outcome (`CREATED` or `PRESERVED`) always invalidates it. The "re-resolve to a fresh determination" portion re-enters BA-01's own excluded Permitted/Denied branches and is explicitly out of scope (IRA-005 §12); the caller's own next step is a fresh BA-01 call, never auto-triggered here.
- **Input Contract:** `outcome_id` (UUID path parameter), `changed_fact` (str, 1–500 chars, required).
- **Output Contract:** `AccessContextChangeOutcome` (outcome_id, invalidated, changed_fact, checked_at, re_evaluation_required — always `true` when invalidated).
- **Business Rules:** Only a live outcome (`CREATED` or `PRESERVED`) may be invalidated by a context change; a non-live outcome is rejected (409).
- **Authorization Rules:** `PLATFORM_ADMIN`, same as BA-01/BA-02.
- **Domain Events:** `ACCESS_EVALUATION_OUTCOME_INVALIDATED`.
- **Audit Requirements:** `record_audit()` on every path.
- **Tests:** covered in `tests/test_access_evaluation_service.py` (2 tests) and `tests/test_access_evaluation_api.py` (1 test).

---

## BA-04 — Resolve Dependent Capability Access Hand-off Rejection

### Business Activity Contract (IMP-001 §6.7)

- **Business Intent:** Realize EX-C002-08. Mirrors WP-02 BA-10's own `HandoffRejectionClassification` pattern exactly, applied here to C-002's own Access Evaluation Outcome instead of C-003's authorization policy objects.
- **Input Contract:** `outcome_id` (UUID path parameter), `reporting_capability` (str, required), `stated_reason` (str, required).
- **Output Contract:** `AccessHandoffRejectionOutcome` (outcome_id, classification, object_preserved, explanation, routed_to, checked_at).
- **Business Rules (Contract 5.6/5.7 discipline, "a signal, not an authority"):** the outcome's own current `validity_status` is the sole classification basis — never the reporting capability's stated reason.
  - Live outcome (`CREATED`/`PRESERVED`) → `CAPABILITY_SCOPED_INSUFFICIENCY`, `object_preserved=true`, `routed_to=null`.
  - Non-live outcome → `INTEGRITY_SIGNAL`, `object_preserved=false`, `routed_to="BA-01 (Evaluate Access for a Governed Request)"`.
- **Authorization Rules:** `PLATFORM_ADMIN`, same as BA-01–BA-03.
- **Domain Events:** `ACCESS_HANDOFF_REJECTION_RESOLVED`.
- **Audit Requirements:** `record_audit()` recording `reporting_capability`, `stated_reason`, and the computed `classification`.
- **Tests:** covered in `tests/test_access_evaluation_service.py` (3 tests) and `tests/test_access_evaluation_api.py` (1 test).

---

## Governing Architecture Review (Step 1)

Reviewed (per IRA-005's own Documents Reviewed line, re-confirmed for this implementation pass): CLAUDE.md (§14, §16, §17, §19.1–§19.8), ARCH-000, CAP-001 (C-002 entry), PE-001-C002 (ERB-C002-01, EX-C002-03 through EX-C002-08), `ADR-015` (AEO-000001 registration), IRA-005 (§11 Lifecycle Model, §12 authorized minimum scope), IMP-001 (§6 CBAIP), WPR-001 (confirms WP-04 CLOSED — Certified; WP-RTA-001 CERTIFIED WITH CONDITIONS but not a usable Permitted/Denied consumer), WP-REG-001 (WP-05 row: initialization complete, 0/4 Business Activities in progress), the existing AuthService repository structure — `models/domain_permission.py`, `services/domain_permission_service.py`, `models/approval_authority.py`, `models/membership.py`, `schemas/authorization_policy_conflict.py`, `schemas/authorization_policy_handoff.py` (WP-02 BA-09/BA-10's own precedent, directly mirrored for BA-04).

**Key finding requiring disclosure:** no `access_evaluation_outcomes` table, model, or service existed anywhere in the repository prior to this Work Package — `AEO-000001` was registered by `ADR-015` as a canonical Business Object but had no Physical Implementation Mapping yet. This is a genuine Create (not an Extend), consistent with CLAUDE.md §19.5's Reuse → Configure → Extend → Compose → Create order — no existing table, model, or service could be extended to hold this Work Package's own Lifecycle Model, because none existed.

---

## Gap Analysis Summary (see IRA-005 §11–§12 for full detail)

- **Database:** One new table, `access_evaluation_outcomes` — the first Physical Implementation Mapping for `AEO-000001`. FKs to `memberships.id` (CASCADE), `domains.id`, and `approval_authorities.id` (nullable, populated only for DEFERRED outcomes) — all three already exist as of this migration's own `down_revision` (`e6c1b3a9d7f2`, WP-04's last migration). Single new migration (`f3a7c5e9b2d8`), confirmed a single Alembic head.
- **Business Activities:** BA-01 (Unresolved/Deferred branches only) through BA-04 are the four Business Activities authorized by IRA-005 §12. BA-01's Permitted/Denied branches and BA-03's re-resolution branch remain candidate-only, each requiring a future, separately-scoped gap analysis once a real `WP-RTA-001` `TierResolver` exists.
- **API Impact:** Five new endpoints under `/access-evaluations`, mirroring the established schema/repository/service/router layering already used by every prior WP.
- **UI Impact:** Out of scope (backend Business Activity implementation only, matching every prior WP's own BA-01 precedent).
- **Dependencies:** Membership (C-007, WP-03, closed), Domain (AMD-014, WP-02-era reference data), Approval Authority (C-003, WP-02, closed) — all three reused verbatim, none modified.
- **Explicitly out of scope (IRA-005 §12):** Permitted/Denied determination (requires a real URA-001-76 precedence-chain resolver — `WP-RTA-001` exists but has no production `TierResolver` for any tier); BA-03's re-resolution-to-fresh-determination path (inherits the same exclusion).
- **Technical Debt inherited:** none directly named this Work Package as its own resolution path; TD-021-class PLATFORM_ADMIN-only gating is inherited as a new instance, recorded below as `TD-079`.

---

## Documents Updated

**Architecture (new, planning only):**
- `architecture/05-Implementation/IRA-005_WP-05_Access_Management_Implementation_Readiness_Assessment.md` (already accepted; unchanged by this report, per that IRA's own instruction not to be modified)
- `architecture/05-Implementation/IMP-REPORT-WP-05_Access_Management.md` (this report)
- `architecture/06-Reviews/TECH-DEBT.md` (`TD-079`, `TD-080` added)
- `architecture/00-Governance/WP-REG-001_Enterprise_Work_Package_Register.md` (WP-05 execution-status rows updated: Business Activities In Progress, Work Package Status table, Lifecycle History) — `WPR-001` intentionally **not** touched at this point: per `WP-REG-001 §2`/`§3`'s own division of authority, WPR-001 updates only on roadmap-level governance changes (chartering, IRA acceptance, closure/certification), not per-Business-Activity execution status. It will be updated once Independent Review/Certification actually completes, mirroring WP-04's own precedent.
- `architecture/00-Governance/DOC-000_Documentation_Catalogue.md` (Implementation Reports index count updated: 5 → 6)

**Implementation (new):**
- `Backend/Services/AuthService/models/access_evaluation_outcome.py`
- `Backend/Services/AuthService/repositories/access_evaluation_outcome_repository.py`
- `Backend/Services/AuthService/schemas/access_evaluation.py`
- `Backend/Services/AuthService/services/access_evaluation_service.py`
- `Backend/Services/AuthService/routers/access_evaluation.py`
- `Backend/Services/AuthService/alembic/versions/2026_08_09_0900-f3a7c5e9b2d8_access_evaluation_outcome.py`
- `Backend/Services/AuthService/tests/test_access_evaluation_service.py` (15 tests)
- `Backend/Services/AuthService/tests/test_access_evaluation_api.py` (11 tests)

**Implementation (modified):**
- `Backend/Services/AuthService/main.py` — registered the new `access_evaluation` router at `/access-evaluations`.
- `Backend/Services/AuthService/middleware/tenant.py` — added `/access-evaluations` and `/access-evaluations/*` to the tenant-exemption list, with disclosure language mirroring `/domain-permissions`' own precedent (genuinely organization-scoped data, one hop via `membership_id`, exempted only because PLATFORM_ADMIN is the sole caller today).

No other existing model, repository, service, or router was modified.

---

## Validation

- 29 new tests (15 unit, 14 API — 3 API tests added post-certification closing `TD-081`), all passing.
- Full AuthService suite: **601 passed**, zero regressions (re-run directly via `pytest tests/ -v`, not taken on faith).
- Confirmed a single Alembic head (`f3a7c5e9b2d8`) after the new migration, chained onto `e6c1b3a9d7f2`.
- Confirmed BA-01's UNRESOLVED branch: missing membership and inactive (non-ACTIVE `membership_status`) membership both produce `UNRESOLVED`.
- Confirmed BA-01's DEFERRED branch: an ACTIVE, DOMAIN-scoped Approval Authority governing the target Domain produces `DEFERRED` with `approval_authority_id` populated.
- Confirmed BA-01's explicit exclusion: an ACTIVE membership with no governing Approval Authority returns HTTP 501, never a fabricated Permitted/Denied decision.
- Confirmed BA-02's `CREATED → PRESERVED → EXPIRED` transitions and both 409 guards (double-preserve, expire-without-preserve).
- Confirmed BA-03's context-change invalidation of a live outcome, and its 409 rejection of a second invalidation against an already-invalidated outcome.
- Confirmed BA-04's two-way classification: a live outcome classifies as `CAPABILITY_SCOPED_INSUFFICIENCY` (object preserved); an invalidated (non-live) outcome classifies as `INTEGRITY_SIGNAL` (object not preserved, routed to BA-01) — regardless of the reporting capability's own stated reason, confirmed by using an unrelated stated reason in both tests.
- Confirmed non-`PLATFORM_ADMIN` callers receive 403; missing Authorization header returns 400; invalid `permission_level` returns 422.
- Confirmed `POST /access-evaluations` and its sub-resource actions require no `X-Tenant-ID` header (tenant-exemption list), matching the disclosed rationale.
- Live Postgres `alembic upgrade`/`alembic check` was not exercised — no running Postgres instance is available in this environment, the same limitation every prior WP's own validation carried (SQLite in-memory is used for the test suite).

---

## Status (BA-01 through BA-04)

**Implementation:** COMPLETE

**Developer Validation:** Complete (601/601 full suite passing, re-run directly during this report's own preparation)

**Independent Review:** COMPLETE — performed by a fresh-context subagent per CLAUDE.md §19.7/ADR-014 (the implementing session did not certify its own work). Result: **CERTIFIED — PASS WITH OBSERVATIONS** (`CERT-WP-05_Access_Management.md`). Three Low-severity findings, none Blocking: `TD-079` and `TD-080` (pre-existing, confirmed accurate and non-overstated), and `TD-081` (newly raised by the reviewer — a narrow API-layer test-coverage gap, closed same-day by adding the three missing branch-level assertions the reviewer identified).

**Certification:** WP-05 is **CLOSED — CERTIFIED**. `WP-REG-001` and `WPR-001` updated accordingly.

**Repository Commit:** Not yet committed — git commits are only made on the repository owner's explicit instruction (see this session's own git safety protocol); all WP-05 implementation and documentation changes remain staged in the working tree, ready to commit on request.
