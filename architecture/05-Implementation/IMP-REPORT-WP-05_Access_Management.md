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
  - EX-C002-03 — a request against a Membership that is present but not in ACTIVE standing cannot be resolved — produces `UNRESOLVED`. A Membership that does not exist at all is a **structural precondition failure (404)**, not an UNRESOLVED business outcome — see the VV-AUDIT-WP-05 Correction below.
  - EX-C002-04 — a request against a Domain governed by an ACTIVE, DOMAIN-scoped Approval Authority **within the requesting Membership's own Organization** requires approval before resolution can proceed — produces `DEFERRED`, with `approval_authority_id` populated. The Approval Authority lookup is organization-scoped, not merely domain-scoped — see the VV-AUDIT-WP-05 Correction below.
  - CLAUDE.md §19.8.5 — a Permitted/Denied determination requires a real URA-001-76 precedence-chain resolver, which does not exist in this repository (`WP-RTA-001` Closure Report §7, "Not production ready"). Rather than approximate or silently decline, any request reaching neither the Unresolved nor the Deferred branch raises **HTTP 501**, naming IRA-005 §12 as the reason — a false Permitted outcome would be a security defect, not deferrable Technical Debt.
- **Validation Rules:** Target Domain must already exist (structural pre-check, 404 if not — mirrors `DomainPermissionService.establish()`'s own precedent). Target Membership must also already exist (structural pre-check, 404 if not — identical basis; corrected per VV-AUDIT-WP-05 F-01, `membership_id` is a non-nullable foreign key and cannot anchor a persisted outcome to a nonexistent row).
- **Authorization Rules:** `PLATFORM_ADMIN` role required — the same interim gate WP-01 through WP-04 all used. No PE-001-C002 persona exists as an enforceable claim today (same class of gap as TD-021–025/031/042/043, tracked as `TD-079`).
- **Idempotency:** `POST /access-evaluations` is **not idempotent** — no uniqueness constraint exists on `(membership_id, domain_id, permission_level)`, so calling it twice with identical inputs creates two distinct outcome rows. Disclosed, not silently omitted (VV-AUDIT-WP-05 F-04); tracked for future resolution via the same class of gap already open for other WPs' create endpoints.
- **AI Assistance:** None implemented. This Business Activity contains no AI/LLM invocation of any kind, consistent with Contract 5.7's prohibitions (AI SHALL NOT grant, deny, override, invent, or infer authorization) — verified by reading all source; recorded explicitly per VV-AUDIT-WP-05 F-04.
- **Domain Events:** `ACCESS_EVALUATION_OUTCOME_CREATED` (outcome_id, outcome_type).
- **Audit Requirements:** `record_audit("EVALUATE_ACCESS", ...)` on every path (unknown domain, unknown membership, Unresolved, Deferred, and the 501 decline), attributed to the authenticated caller's own `person_id` (corrected per VV-AUDIT-WP-05 F-03 — previously always `"SYSTEM"`), per SD-002-054's seven audit questions.
- **Tests:** covered in `tests/test_access_evaluation_service.py` (7 tests) and `tests/test_access_evaluation_api.py` (9 tests) — see full test list below.

---

## BA-02 — Preserve and Bound Access Evaluation Outcome Validity

### Business Activity Contract (IMP-001 §6.7)

- **Business Intent:** Realize EX-C002-05/EX-C002-06 — an Access Evaluation Outcome's Validity Status must be explicitly, observably transitioned, never silently assumed.
- **Input Contract:** `outcome_id` (UUID path parameter); empty request body for both actions.
- **Output Contract:** The updated `AccessEvaluationOutcome`.
- **Business Rules:**
  - EX-C002-05 — Preserve: `CREATED → PRESERVED` only. A non-`CREATED` outcome cannot be preserved (409).
  - EX-C002-06 — Expire: `PRESERVED → EXPIRED` only, explicit and caller-invoked. A non-`PRESERVED` outcome cannot be expired (409). No automatic/time-based expiry is implemented — that would require a scheduler, a new architectural component out of this Work Package's own scope. **Disclosed limitation:** EX-C002-06's own "at Scope Boundary" language and IRA-005 §11's Object/Event/Time scoping are not modelled at all (no scope identifier, no time bound) — recorded as `TD-082` (VV-AUDIT-WP-05 F-08), not silently assumed complete.
- **Authorization Rules:** `PLATFORM_ADMIN`, same as BA-01.
- **Idempotency:** Both endpoints are naturally idempotent against repeated calls with the same effect — a second `preserve`/`expire` call against an already-transitioned outcome returns 409 rather than silently repeating the transition. No explicit BAC disclosure previously existed for this; recorded per VV-AUDIT-WP-05 F-04.
- **AI Assistance:** None implemented — verified by reading all source.
- **Domain Events:** `ACCESS_EVALUATION_OUTCOME_PRESERVED`, `ACCESS_EVALUATION_OUTCOME_EXPIRED`.
- **Audit Requirements:** `record_audit()` on every path (not-found, wrong-state, success), attributed to the authenticated caller's own `person_id` (corrected per VV-AUDIT-WP-05 F-03).
- **Tests:** covered in `tests/test_access_evaluation_service.py` (5 tests) and `tests/test_access_evaluation_api.py` (4 tests).

---

## BA-03 — Detect and Resolve Access Context Change (classification/detection portion only)

### Business Activity Contract (IMP-001 §6.7)

- **Business Intent:** Realize EX-C002-07's classification/detection portion — a reported governing-fact change against a still-live outcome (`CREATED` or `PRESERVED`) always invalidates it. The "re-resolve to a fresh determination" portion re-enters BA-01's own excluded Permitted/Denied branches and is explicitly out of scope (IRA-005 §12); the caller's own next step is a fresh BA-01 call, never auto-triggered here.
- **Input Contract:** `outcome_id` (UUID path parameter), `changed_fact` (str, 1–500 chars, required).
- **Output Contract:** `AccessContextChangeOutcome` (outcome_id, invalidated, changed_fact, checked_at, re_evaluation_required — always `true` when invalidated).
- **Business Rules:** Only a live outcome (`CREATED` or `PRESERVED`) may be invalidated by a context change; a non-live outcome is rejected (409). **Disclosed limitation:** no actual *detection* occurs — `changed_fact` is validated only for length and is never re-checked against Membership/Domain/Approval Authority state; the endpoint trusts the caller's own assertion. Recorded as `TD-083` (VV-AUDIT-WP-05 F-09), not silently assumed to be fact-verified.
- **Authorization Rules:** `PLATFORM_ADMIN`, same as BA-01/BA-02.
- **Idempotency:** Not idempotent in effect (each call appends to `reason`), but naturally guarded — a second call against an already-invalidated outcome returns 409 rather than double-appending. Recorded per VV-AUDIT-WP-05 F-04.
- **AI Assistance:** None implemented — verified by reading all source.
- **Domain Events:** `ACCESS_EVALUATION_OUTCOME_INVALIDATED`.
- **Audit Requirements:** `record_audit()` on every path, attributed to the authenticated caller's own `person_id` (corrected per VV-AUDIT-WP-05 F-03).
- **Tests:** covered in `tests/test_access_evaluation_service.py` (2 tests) and `tests/test_access_evaluation_api.py` (3 tests).

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
- **Idempotency:** Naturally idempotent — a pure read-and-classify operation; repeated identical calls against the same outcome return the same classification with no state change. **Disclosed limitation:** the rejection itself is never persisted — no queryable record of any hand-off rejection exists beyond the audit log and the synchronous response. Recorded as `TD-087` (VV-AUDIT-WP-05 F-15).
- **AI Assistance:** None implemented — verified by reading all source.
- **Domain Events:** `ACCESS_HANDOFF_REJECTION_RESOLVED`.
- **Audit Requirements:** `record_audit()` recording `reporting_capability`, `stated_reason`, and the computed `classification`, attributed to the authenticated caller's own `person_id` (corrected per VV-AUDIT-WP-05 F-03).
- **Tests:** covered in `tests/test_access_evaluation_service.py` (3 tests) and `tests/test_access_evaluation_api.py` (3 tests).

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

## Correction (VV-AUDIT-WP-05, 2026-07-31)

**What happened.** After `CERT-WP-05` certified WP-05 `PASS WITH OBSERVATIONS` and the Work Package was recorded `CLOSED — CERTIFIED`, a separate, more rigorous **Verification & Validation audit** (`VV-AUDIT-WP-05_Access_Management.md`) was performed by a fresh-context auditor with no prior involvement in WP-05's design, implementation, review, or certification — the same `CLAUDE.md §19.7`/`ADR-014` independence discipline this Work Package's own certification was supposed to have satisfied, applied a second time at greater depth. That audit found **two High-severity defects** `CERT-WP-05` did not identify, both falling inside `CLAUDE.md §19.8.5`'s explicit list of categories Technical Debt SHALL NOT be used to defer:

- **F-01 (data integrity / broken functionality).** BA-01's `UNRESOLVED`-for-unknown-Membership branch persisted an `AccessEvaluationOutcome` row whose non-nullable `membership_id` foreign key referenced a Membership that did not exist. This succeeded only because the shared test harness (`tests/conftest.py`) runs SQLite with foreign-key enforcement off; on any FK-enforcing database (including this repository's declared production database, PostgreSQL, per `CLAUDE.md §9`), the identical call raised an unhandled `IntegrityError`, returning HTTP 500 instead of the specified `201` + `UNRESOLVED`. The audit demonstrated this empirically with a purpose-built probe, not merely by reasoning about it.
- **F-02 (tenant isolation / security).** `AccessEvaluationOutcomeRepository.get_active_domain_approval_authority()` selected an ACTIVE, DOMAIN-scoped Approval Authority by `domain_id` alone, never filtering by organization. Because `Domain` is platform-shared reference data (`Domain.organization_id` nullable) while `ApprovalAuthority.organization_id` is required for every scope, a Membership in one Organization could be `DEFERRED` to a different Organization's Approval Authority — disclosing that authority's name and id into a persisted, API-returned record. The audit demonstrated this empirically with a two-organization probe.

Neither defect was disclosed in `TECH-DEBT.md`, this report, or `CERT-WP-05` prior to the audit. Per `CLAUDE.md §19.7`, WP-05's Business Activity Completion Gate was therefore **not actually satisfied** at the point of its original certification, notwithstanding its recorded status.

**What was remediated, by whom, and how verified.** Both defects were remediated by the implementing session (this report's own author), following the audit's own recommended fix shape (Recommendation R-01 option (a); R-02):

- **F-01 fix:** `AccessEvaluationService.evaluate()` now treats an unknown `membership_id` as a structural precondition failure — **404**, mirroring the pre-existing Domain-not-found precedent exactly — rather than attempting to persist an outcome anchored to a nonexistent row. The UNRESOLVED branch now fires only for a Membership that genuinely exists but is not in ACTIVE standing, which always has a valid foreign key. A regression test running against a **separately-configured engine with SQLite foreign-key enforcement turned ON** (`test_evaluate_unknown_membership_writes_no_row_under_foreign_key_enforcement`) confirms the fix directly, per the audit's own Recommendation R-01.
- **F-02 fix:** `get_active_domain_approval_authority()` now requires and filters on `organization_id` (the requesting Membership's own), and adds a deterministic `ORDER BY (created_at, id)` in place of the previous unordered `.first()`. Two regression tests (unit and API layer) seed a second Organization's Approval Authority against the same shared Domain and assert it is never selected — instead correctly falling through to the 501 out-of-scope path.
- Per `CLAUDE.md §19.8.5`, neither F-01 nor F-02 was recorded in `TECH-DEBT.md` — both were ineligible for deferral and were remediated directly.

**This remediation was not self-certified.** Consistent with the audit's own Finding F-06 (which criticized `TD-081`'s remediation for having been self-attested by the implementing session without independent re-review before the Work Package's status was allowed to stand), this correction was not treated as closing WP-05's completion gate on the implementing session's own say-so. A fresh, independent reviewer (with no involvement in this correction) was dispatched and independently confirmed the remediation (`VV-AUDIT-WP-05_Remediation_Verification.md`, CONFIRMED WITH OBSERVATIONS) before WP-05's `CLOSED — CERTIFIED` status was restored in `WP-REG-001`/`WPR-001`, per the audit's own Recommendation R-03.

**Additional findings addressed in this same pass (non-blocking, all previously either undisclosed-in-register or missing a required field):**

- **F-03** (every audit record attributed the action to `"SYSTEM"`, never the real actor) — fixed: all five router handlers now pass `actor_id=claims.get("person_id")`, matching the 51 existing occurrences across the service's other 15 routers. A test using `caplog` now asserts the authenticated actor's own `person_id` reaches the audit record.
- **F-05** (`DOC-000`'s Certification Reports index omitted `CERT-WP-05` entirely) — fixed: `CERT-WP-05` and `VV-AUDIT-WP-05` are now both indexed in `DOC-000`.
- **F-06 / F-07** (`CERT-WP-05` and this report's own prior test counts/commit-state assertions were stale or self-contradictory) — corrected in this revision (see Documents Updated / Validation below); `CERT-WP-05` itself is left as the historical record of the original (superseded) certification pass, per this section's own disclosure, rather than edited after the fact.
- **F-10** (`TD-081` lacked a Detailed Entry and an explicit `CLAUDE.md §19.8.7` severity) — fixed: a Detailed Entry with `Severity: Low` now exists.
- **F-04, F-08, F-09, F-11, F-12, F-13, F-15, F-19, F-21** (the BA Contracts above now carry Idempotency/AI Assistance disclosures for the substantive items; the remaining previously-undocumented limitations, most of which existed only in code docstrings in violation of `CLAUDE.md §19.8.2`, are now individually registered as `TD-082` through `TD-089`).

---

## Documents Updated

**Architecture (new, planning only):**
- `architecture/05-Implementation/IRA-005_WP-05_Access_Management_Implementation_Readiness_Assessment.md` (already accepted; unchanged by this report, per that IRA's own instruction not to be modified)
- `architecture/05-Implementation/IMP-REPORT-WP-05_Access_Management.md` (this report — includes the Correction section above)
- `architecture/06-Reviews/VV-AUDIT-WP-05_Access_Management.md` (new — the independent V&V audit that found F-01/F-02)
- `architecture/06-Reviews/TECH-DEBT.md` (`TD-079`, `TD-080` from the original pass; `TD-081` given a Detailed Entry with severity; `TD-082` through `TD-089` added for previously-undocumented limitations)
- `architecture/00-Governance/WP-REG-001_Enterprise_Work_Package_Register.md` (WP-05 status qualified to CERTIFIED — REMEDIATION APPLIED, RE-VERIFICATION PENDING, then restored to CLOSED — CERTIFIED once `VV-AUDIT-WP-05_Remediation_Verification.md` confirmed the correction)
- `architecture/00-Governance/DOC-000_Documentation_Catalogue.md` (Certification Reports index: `CERT-WP-05` added, 6 → 7; new `VV-AUDIT-WP-05` row added; Implementation Reports row corrected)

**Implementation (new):**
- `Backend/Services/AuthService/models/access_evaluation_outcome.py`
- `Backend/Services/AuthService/repositories/access_evaluation_outcome_repository.py` (corrected: `get_active_domain_approval_authority()` now organization-scoped with deterministic ordering — F-02 fix)
- `Backend/Services/AuthService/schemas/access_evaluation.py`
- `Backend/Services/AuthService/services/access_evaluation_service.py` (corrected: `evaluate()` now 404s on unknown Membership rather than persisting an invalid FK — F-01 fix; actor_id now threaded through)
- `Backend/Services/AuthService/routers/access_evaluation.py` (corrected: all five handlers now pass `actor_id=claims.get("person_id")` — F-03 fix)
- `Backend/Services/AuthService/alembic/versions/2026_08_09_0900-f3a7c5e9b2d8_access_evaluation_outcome.py`
- `Backend/Services/AuthService/tests/test_access_evaluation_service.py` (17 tests — rewritten fixtures, F-01/F-02 regressions, FK-enforcement probe)
- `Backend/Services/AuthService/tests/test_access_evaluation_api.py` (19 tests — rewritten fixtures, F-01/F-02/F-03 regressions, additional 404 coverage)

**Implementation (modified):**
- `Backend/Services/AuthService/main.py` — registered the new `access_evaluation` router at `/access-evaluations`.
- `Backend/Services/AuthService/middleware/tenant.py` — added `/access-evaluations` and `/access-evaluations/*` to the tenant-exemption list, with disclosure language mirroring `/domain-permissions`' own precedent (genuinely organization-scoped data, one hop via `membership_id`, exempted only because PLATFORM_ADMIN is the sole caller today).

No other existing model, repository, service, or router was modified.

---

## Validation

- 36 new tests (17 unit, 19 API), all passing — up from 29 at original certification; +7 net (2 F-01/F-02 unit regressions, 1 FK-enforcement probe, 2 F-01/F-02 API regressions, 1 F-03 audit-actor assertion, 1 additional API 404 case beyond the three TD-081 already closed).
- Full AuthService suite: **608 passed**, zero regressions (re-run directly via `pytest tests/ -q`, not taken on faith).
- Confirmed a single Alembic head (`f3a7c5e9b2d8`) after the new migration, chained onto `e6c1b3a9d7f2` — unchanged by this correction (no new migration was required for either fix).
- Confirmed BA-01's UNRESOLVED branch: an inactive (non-ACTIVE `membership_status`), but genuinely existing, Membership produces `UNRESOLVED`. Confirmed BA-01 now rejects an unknown `membership_id` with **404** (corrected from the pre-fix `201`/`UNRESOLVED` behavior, per F-01).
- Confirmed BA-01's DEFERRED branch: an ACTIVE, DOMAIN-scoped Approval Authority governing the target Domain **within the requesting Membership's own Organization** produces `DEFERRED` with `approval_authority_id` populated. Confirmed a **different** Organization's Approval Authority against the same shared Domain is never selected (falls through to 501 instead) — both at the unit and API layers, per F-02.
- Confirmed BA-01's explicit exclusion: an ACTIVE membership with no governing Approval Authority (in its own organization) returns HTTP 501, never a fabricated Permitted/Denied decision.
- Confirmed BA-02's `CREATED → PRESERVED → EXPIRED` transitions and both 409 guards (double-preserve, expire-without-preserve) — now also confirmed at the API layer for the unknown-outcome 404 case on both endpoints.
- Confirmed BA-03's context-change invalidation of a live outcome, its 409 rejection of a second invalidation against an already-invalidated outcome, and (newly) its 404 for an unknown outcome at the API layer.
- Confirmed BA-04's two-way classification: a live outcome classifies as `CAPABILITY_SCOPED_INSUFFICIENCY` (object preserved); an invalidated (non-live) outcome classifies as `INTEGRITY_SIGNAL` (object not preserved, routed to BA-01) — regardless of the reporting capability's own stated reason, confirmed by using an unrelated stated reason in both tests. Its own unknown-outcome 404 is now also confirmed at the API layer.
- Confirmed non-`PLATFORM_ADMIN` callers receive 403; missing Authorization header returns 400; invalid `permission_level` returns 422.
- Confirmed `POST /access-evaluations` and its sub-resource actions require no `X-Tenant-ID` header (tenant-exemption list), matching the disclosed rationale.
- Confirmed (new, F-03) the authenticated caller's own `person_id` — not `"SYSTEM"` — reaches every audit record, via a `caplog`-based assertion on the real emitted log record.
- Confirmed (new, F-01) the unknown-Membership 404 path writes no row and raises no `IntegrityError`, under a dedicated engine with SQLite foreign-key enforcement turned on — the exact condition the original defect required to manifest.
- Live Postgres `alembic upgrade`/`alembic check` was not exercised — no running Postgres instance is available in this environment, the same limitation every prior WP's own validation carried (SQLite in-memory is used for the test suite).

---

## Status (BA-01 through BA-04)

**Implementation:** COMPLETE (including the VV-AUDIT-WP-05 correction)

**Developer Validation:** Complete (608/608 full suite passing, re-run directly during this report's own preparation)

**Independent Review (original pass):** COMPLETE — performed by a fresh-context subagent per CLAUDE.md §19.7/ADR-014. Result: **CERTIFIED — PASS WITH OBSERVATIONS** (`CERT-WP-05_Access_Management.md`). This determination **did not survive** a subsequent, more rigorous Verification & Validation audit (`VV-AUDIT-WP-05_Access_Management.md`) performed by a second, independent fresh-context reviewer, which found two High-severity, `CLAUDE.md §19.8.5`-class defects (F-01, F-02) `CERT-WP-05` had not identified. See the Correction section above.

**Remediation:** COMPLETE — F-01 and F-02 fixed per the audit's own recommended approach; both confirmed by dedicated regression tests (including an FK-enforced probe and a two-organization probe) and by a full-suite re-run (608/608).

**Re-verification of remediation:** COMPLETE — performed by a third, independent fresh-context reviewer (uninvolved in the design, implementation, original certification, or `VV-AUDIT-WP-05` itself), per `CLAUDE.md §19.7` and per that audit's own Finding F-06 (which specifically criticized `TD-081`'s prior remediation for being accepted without independent re-review). Result: **CONFIRMED WITH OBSERVATIONS** (`VV-AUDIT-WP-05_Remediation_Verification.md`) — both defects independently re-verified via structural code review, 24 from-scratch probe checks, and 2 negative controls (the same probes run against pre-fix `HEAD` code, which independently reproduced both original defects, proving the probes are meaningful rather than tautological). No over-narrowing found in either fix; no new defect found in the diff. Four non-blocking documentation-level observations recorded; two (a stale `TECH-DEBT.md` cross-reference and an incomplete OpenAPI 404 description) were corrected in this same governance pass.

**Certification status:** **CLOSED — CERTIFIED.** `WP-REG-001` and `WPR-001` both restored accordingly.

**Repository Commit:** Not yet committed — git commits are only made on the repository owner's explicit instruction (see this session's own git safety protocol); all WP-05 implementation and documentation changes, including this correction, remain staged in the working tree, ready to commit on request.
