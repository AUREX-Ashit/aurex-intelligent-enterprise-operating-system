# VV-AUDIT-WP-05 — Independent Verification & Validation Audit

## Work Package WP-05 — Access Management (Capability C-002), Authorized Minimum Scope

**Document ID:** VV-AUDIT-WP-05
**Document Type:** Independent Verification & Validation (V&V) Audit — **not** an Implementation Review, **not** a repeat of `CERT-WP-05_Access_Management.md`
**Work Package audited:** WP-05 — Access Management (C-002), minimum scope per `IRA-005 §12`
**Audited commits:** `84b095b` (implementation) and `2ff1002` (governance/closure), branch `master`
**Audit date:** 2026-07-31
**Auditor posture:** Independent Enterprise Software Auditor. No involvement in WP-05's design, implementation, review, or certification. Every claim in `IMP-REPORT-WP-05_Access_Management.md` and `CERT-WP-05_Access_Management.md` was treated as an unproven hypothesis and independently re-derived against actual source code, actual test execution, actual database behaviour, and the actual governing documents.

**Certification Recommendation (Section 16): PASS WITH MINOR REMEDIATION.**

---

## 1. Executive Summary

### 1.1 What was audited

WP-05 implements Capability C-002 (Access Management) at the deliberately narrow scope authorized by `IRA-005 §12`: BA-01 (Evaluate Access for a Governed Request) limited to its **Unresolved** and **Deferred** outcome branches; BA-02 (Preserve and Bound Validity) in full; BA-03 (Detect and Resolve Access Context Change) limited to its classification/detection portion; BA-04 (Resolve Dependent Capability Access Hand-off Rejection) in full. Permitted and Denied outcome branches, and BA-03's re-resolution path, are explicitly **not** authorized and must **not** exist.

The implementation comprises 8 new source files, 1 Alembic migration, 2 modified files, and 29 tests, all committed in `84b095b`; governance closure was committed in `2ff1002`.

### 1.2 What the audit confirms

The single most important constitutional requirement of this Work Package holds, and was verified exhaustively rather than by reading the one obvious method:

- **No code path anywhere in WP-05 can produce a `PERMITTED` or `DENIED` Access Evaluation Outcome.** Verified four independent ways (Section 8.9): full trace of every branch of `evaluate()`; repository-wide grep confirming the only `DENIED` tokens in the service are `AuditStatus.DENIED` (an audit-log vocabulary value, not an outcome type); confirmation that `outcome_type` is written from a literal enum member at exactly two call sites, both `UNRESOLVED`/`DEFERRED`; and confirmation that no update path anywhere mutates `outcome_type` after creation. This satisfies `CLAUDE.md §19.8.5`'s prohibition on deferring a security defect and `BR-C002-02`'s closed-set rule.
- **Scope conformance is exact.** No Business Activity exceeds `IRA-005 §12`'s authorization, and no authorized behaviour was silently dropped. BA-03 never re-resolves; BA-04 classifies on `validity_status` alone.
- **601/601 tests pass** and **exactly one Alembic head** (`f3a7c5e9b2d8`) exists — both independently re-executed by this audit, not taken from any report.
- **Model/migration parity is exact** for all three `CheckConstraint`s.
- **No unauthorized architecture** was introduced: one table, five endpoints, no new entity beyond `AEO-000001`, no new service boundary, no new technology.

### 1.3 What the audit found that prior review did not

Two **High**-severity defects were found that `CERT-WP-05` did not identify, both of which fall squarely inside `CLAUDE.md §19.8.5`'s list of categories that **SHALL NOT** be deferred as Technical Debt:

- **F-01 (High, data integrity).** BA-01's `UNRESOLVED`-for-unknown-Membership branch persists a row whose non-nullable `membership_id` foreign key deliberately references a Membership that does not exist. It succeeds only because the test harness uses SQLite with foreign-key enforcement **off**. Under PostgreSQL — this repository's declared production database (`CLAUDE.md §9`) — the identical call raises `IntegrityError`, which is not caught, and returns **HTTP 500** instead of a `201 UNRESOLVED` outcome. Empirically demonstrated (Section 9.6). Consequence: half of `EX-C002-03` is not implemented in production, and **16 of WP-05's 29 tests** are seeded through this production-impossible path.
- **F-02 (High, tenant isolation).** `AccessEvaluationOutcomeRepository.get_active_domain_approval_authority()` filters on `domain_id`, `scope_type`, and `status` only — **never on organization**. Because `Domain.organization_id` is nullable ("platform-seeded, visible to every tenant"), a Membership in Organization A can be `DEFERRED` to Organization B's Approval Authority, whose `authority_name` is then written into the persisted `reason` column and returned in the API response body. Empirically demonstrated (Section 8.6). This is a cross-tenant information disclosure and a materially wrong business determination.

A further **four Medium** and **eight Low** findings are recorded in Section 14, including: audit records that never identify the actual actor (F-03); a Business Activity Contract missing 10 of `IMP-001 §6.7`'s 16 mandatory attributes including the explicitly-mandatory Idempotency disclosure (F-04); `DOC-000`'s Certification Reports index omitting `CERT-WP-05` entirely (F-05); and `CERT-WP-05` certifying test evidence (598 tests, 11 API tests) that does not match the code committed alongside it (601 tests, 14 API tests) (F-06).

### 1.4 Bottom line

WP-05 is architecturally sound, scope-conformant, and constitutionally correct on the one issue it could not afford to get wrong. It is **not** free of defects, and two of those defects are of a class `CLAUDE.md §19.8.5` forbids deferring. Neither requires redesign or reimplementation — F-01 and F-02 are each a small, localized change. Accordingly the recommendation is **PASS WITH MINOR REMEDIATION**, with the explicit qualification that WP-05's current `CLOSED — CERTIFIED` status in `WP-REG-001` and `WPR-001` is **not presently supportable** and should be qualified until F-01 and F-02 are closed.

---

## 2. Scope

### 2.1 In scope

**Governing documents read in full and used as the audit standard:**

| Document | Path | Role in this audit |
|---|---|---|
| CLAUDE.md | `CLAUDE.md` | §14 Definition of Done, §16 Canonical Authority Resolution, §17 Canonical Document Compliance, §18 Architectural Change Control, §19.1–§19.8 (esp. §19.5 Reuse→Create order, §19.7 Completion Gate, §19.8.5 non-deferrable defect classes, §19.8.7 severity rubric) |
| IRA-005 | `architecture/05-Implementation/IRA-005_WP-05_Access_Management_Implementation_Readiness_Assessment.md` | Read in full (lines 1–316). §3 candidate Business Activities, §5 Business Object eligibility, §7 Gap Analysis, §9 readiness decision, §11 `AEO-000001` registration and Lifecycle Model, **§12 the authorized minimum scope — the scope boundary this audit measures against** |
| ADR-015 | `architecture/07-Decisions/ADR-015_Access_Evaluation_Outcome_Canonical_Business_Object_Registration.md` | Registers `AEO-000001`; Decision items 1–5 (lines 26–30) |
| CAP-001 | `architecture/02-Constitutional/CAP-001_Enterprise_Capability_Registry.md` line 53 | C-002 identity and Business Intent ("Govern access rights.") |
| IMP-001 | `architecture/03-Engineering/IMP-001_Implementation_Playbook.md` | §6.7 Business Activity Contract (lines 2049–2094), §6.16.7 Authorization Evaluation (lines 2757–2791), §8 API Standards IMP-API-001/002/004 (lines 11669–11683) |
| ADR repository | `architecture/07-Decisions/` (ADR-001 … ADR-016) | Searched in full for any other ADR touching C-002 or Access Evaluation Outcome |

**Implementation audited (all committed):**

`Backend/Services/AuthService/` — `models/access_evaluation_outcome.py`, `repositories/access_evaluation_outcome_repository.py`, `schemas/access_evaluation.py`, `services/access_evaluation_service.py`, `routers/access_evaluation.py`, `alembic/versions/2026_08_09_0900-f3a7c5e9b2d8_access_evaluation_outcome.py`, `tests/test_access_evaluation_service.py`, `tests/test_access_evaluation_api.py`, plus the two modified files `main.py` and `middleware/tenant.py`.

**Reused-not-modified dependencies read to verify correct reuse:** `models/membership.py`, `models/domain.py`, `models/approval_authority.py`, `models/domain_permission.py`, `models/database.py`, `repositories/base_repository.py`, `dependencies.py`, `observability.py`, `tests/conftest.py`, and — as convention comparators — `routers/structural_completion.py` and `services/structural_completion_service.py`.

**Inputs re-verified rather than trusted:** `IMP-REPORT-WP-05_Access_Management.md`, `CERT-WP-05_Access_Management.md`, `TECH-DEBT.md` (TD-079/TD-080/TD-081), `WP-REG-001`, `WPR-001`, `DOC-000`.

### 2.2 Out of scope

- **`WP-RTA-001` / `Backend/Runtime/`** — a separate Work Package with substantial pre-existing uncommitted work. Not audited. `git show --stat 84b095b` and `git show --stat 2ff1002` were used to establish WP-05's actual change set independently of the working tree's unrelated contents.
- **`architecture/05-Implementation/*RTA-001*` and `architecture/06-Reviews/*RTA-001*`** — same basis.
- **BA-01's Permitted/Denied branches and BA-03's re-resolution path** — explicitly **not authorized** by `IRA-005 §12`. This audit verifies they are **absent**; it does not assess them as missing functionality.
- **`docs/Product/PE-001/capabilities/C-002/PE-001-C002_Access_Management.docx`** — the capability specification exists at this path as a binary `.docx`. It could not be read as text in this environment. **This audit therefore relies on `IRA-005`'s own extensive verbatim quotations from it** (`IRA-005` lines 42, 49–66, 107–126, 253–265) rather than on the source document. Where a conformance judgment depends on PE-001-C002 text not quoted in `IRA-005`, this audit says so explicitly rather than inferring. See Finding F-16.

### 2.3 Audit boundaries observed

No implementation, test, or governance document was modified. Nothing was committed. No destructive git command was run. Two read-only probe scripts were written to a scratchpad directory outside the repository (Sections 8.6 and 9.6); neither touches repository files.

---

## 3. Verification Methodology

1. **Establish the true change set.** `git show --stat 84b095b` / `git show --stat 2ff1002` were used to enumerate exactly which files WP-05 touched, rather than reading `git status` (which is polluted by unrelated WP-RTA-001 work).
2. **Derive requirements from governing documents only.** Requirements were extracted from `IRA-005` (§3, §7, §11, §12), `ADR-015` (Decision items), `CAP-001` (C-002 row), `IMP-001` (§6.7, §6.16.7, §8), and `CLAUDE.md` (§14, §18, §19). No requirement was invented, and no behaviour was assumed to be "probably intended."
3. **Read every WP-05 source file in full**, then read every reused dependency in full to check the reuse claims rather than accept them.
4. **Independently execute.** Full suite (`pytest tests/`), targeted suite (`pytest tests/test_access_evaluation_*.py -v`), and `alembic heads` were run directly in this audit.
5. **Probe behaviour that tests do not cover.** Two purpose-built read-only probes were written to test hypotheses the existing suite structurally cannot detect: (a) foreign-key behaviour under enforcement, (b) cross-organization Approval Authority selection. Both hypotheses were confirmed.
6. **Cross-check every governance document against the actual repository state** (file counts, test counts, commit state, status fields), rather than against each other.
7. **Apply the "absence of evidence is absence of implementation" rule.** Where a requirement has no code, no test, and no document, it is recorded as Missing — never as "probably fine."

**Commands executed (verbatim), with output summarized in the relevant sections:**

```
git show --stat 84b095b
git show --stat 2ff1002
JWT_SECRET_KEY=ci-test-secret-key-not-for-production venv/Scripts/python.exe -m pytest tests/ -q      -> 601 passed, 47 warnings in 255.92s
JWT_SECRET_KEY=ci-test-secret-key-not-for-production venv/Scripts/python.exe -m pytest tests/test_access_evaluation_service.py tests/test_access_evaluation_api.py -v   -> 29 passed
JWT_SECRET_KEY=ci-test-secret-key-not-for-production venv/Scripts/python.exe -m alembic heads          -> f3a7c5e9b2d8 (head)
JWT_SECRET_KEY=ci-test-secret-key-not-for-production venv/Scripts/python.exe -m alembic history        -> e6c1b3a9d7f2 -> f3a7c5e9b2d8 (head), access_evaluation_outcome
```

The `JWT_SECRET_KEY` value was independently confirmed against `.github/workflows/authservice-ci.yml` (line 34: `JWT_SECRET_KEY: ci-test-secret-key-not-for-production`; line 35: `run: python -m pytest tests/ -v`) — it is the project's own CI value, not an invented one.

---

## 4. Requirements Traceability Matrix

Requirement IDs below are assigned **by this audit** for traceability; they are not canonical repository identifiers. Each is anchored to the governing document text it derives from.

### 4.1 Capability and Business Object requirements

| Req ID | Requirement (source) | BA | Implementation | API | Database | Tests | Docs | Status |
|---|---|---|---|---|---|---|---|---|
| R-01 | `AEO-000001` shall exist as a persisted Business Object with `IRA-005 §11`'s Lifecycle Model (ADR-015 Decision 1; IRA-005 §11 lines 249–266) | All | `models/access_evaluation_outcome.py:46-125` | n/a | `access_evaluation_outcomes` | 29 (indirect) | IMP-REPORT §Gap Analysis | **Implemented** |
| R-02 | Outcome Type shall be the closed set PERMITTED/DENIED/UNRESOLVED/DEFERRED, fixed at creation (BR-C002-02; IRA-005 §11 line 260) | BA-01 | `models/access_evaluation_outcome.py:16-34`, CheckConstraint `:63-66` | n/a | `ck_access_evaluation_outcomes_outcome_type` | migration/model parity verified | ADR-015 | **Implemented** |
| R-03 | Validity Status shall be CREATED → PRESERVED → {SUPERSEDED \| INVALIDATED \| EXPIRED} (IRA-005 §11 line 260) | BA-02/03 | `models/access_evaluation_outcome.py:37-43`, CheckConstraint `:67-70` | n/a | `ck_access_evaluation_outcomes_validity_status` | 8 lifecycle tests | IMP-REPORT | **Partially Implemented** — SUPERSEDED is declared but unreachable by design (correct per scope; disclosed in the model docstring line 38, **but not recorded in TECH-DEBT.md** — see F-11) |
| R-04 | Versioning Policy: full history retained for audit and traceability (IRA-005 §11 line 261) | BA-02/03 | Rows are never deleted; `validity_status` mutates in place | n/a | no delete path | — | IRA-005 §11 | **Partially Implemented** — history of *the row* is retained, but the pre-transition `validity_status` is overwritten, not versioned. No prior-state record exists. See F-12 |
| R-05 | Registration shall not authorize implementation without a fresh §19.7 gap analysis (ADR-015 Decision 3) | All | IMP-REPORT §"Governing Architecture Review", §"Gap Analysis Summary" | n/a | n/a | n/a | IMP-REPORT lines 79–95 | **Implemented** |
| R-06 | Physical Implementation Mapping was Pending at ADR-015; WP-05 supplies it (ADR-015 "Explicitly Not Decided"; IRA-005 line 289) | All | migration `f3a7c5e9b2d8` | 5 endpoints | 1 table, 2 indexes, 3 FKs, 3 CHECKs | migration verified | IMP-REPORT | **Implemented** — but `CMD-001 §26.7` itself is **not updated** to record the now-known Physical Tables/APIs/Events. See F-13 |

### 4.2 BA-01 requirements (`IRA-005 §12` bullet 1)

| Req ID | Requirement | Implementation | API | Tests | Status |
|---|---|---|---|---|---|
| R-07 | BA-01 shall produce an `UNRESOLVED` outcome where Membership standing cannot be confirmed (EX-C002-03) | `services/access_evaluation_service.py:103-131` | `POST /access-evaluations` → 201 | `test_evaluate_produces_unresolved_outcome_for_unknown_membership`, `test_evaluate_produces_unresolved_outcome_for_inactive_membership`, `test_evaluate_access_returns_201_and_unresolved_for_unknown_membership` | **Partially Implemented** — the *non-ACTIVE Membership* sub-branch works; the *missing Membership* sub-branch raises `IntegrityError` → HTTP 500 on any FK-enforcing database. **F-01** |
| R-08 | BA-01 shall produce a `DEFERRED` outcome where an ACTIVE, DOMAIN-scoped Approval Authority governs the Domain (EX-C002-04) | `services/access_evaluation_service.py:133-157`; `repositories/access_evaluation_outcome_repository.py:17-33` | `POST /access-evaluations` → 201 | `test_evaluate_produces_deferred_outcome_when_approval_authority_governs_domain`, `test_evaluate_access_returns_deferred_when_approval_authority_governs_domain` | **Partially Implemented** — produces DEFERRED correctly within one organization, but selects Approval Authorities across organization boundaries. **F-02** |
| R-09 | BA-01 shall **never** produce PERMITTED or DENIED (`IRA-005 §12`; `CLAUDE.md §19.8.5`) | `services/access_evaluation_service.py:159-173` (explicit 501) | `POST /access-evaluations` → 501 | `test_evaluate_raises_501_when_no_approval_authority_governs_domain`, `test_evaluate_access_returns_501_when_no_approval_authority_governs_domain` | **Implemented** — verified exhaustively, Section 8.9 |
| R-10 | The target Domain must exist (structural pre-check) | `services/access_evaluation_service.py:89-101` | → 404 | `test_evaluate_rejects_unknown_domain`, `test_evaluate_access_rejects_unknown_domain` | **Implemented** |
| R-11 | `permission_level` shall be one of `DomainPermissionLevel`'s eight URA-001-47 values, reused not redefined | `schemas/access_evaluation.py:7,24`; CheckConstraint `models/...:71-74` | → 422 | `test_evaluate_access_rejects_invalid_permission_level` | **Implemented** |
| R-12 | BA-01 shall emit `ACCESS_EVALUATION_OUTCOME_CREATED` | `services/access_evaluation_service.py:127-130,153-156` | n/a | **none** | **Implemented, untested** — no test asserts any event is published. See F-14 |
| R-13 | BA-01 shall audit every path (IMP-REPORT line 25) | `:91-97, :120-126, :146-152, :159-165` | n/a | **none** | **Implemented, untested, and defective** — actor is always `"SYSTEM"`. **F-03** |

### 4.3 BA-02 requirements (`IRA-005 §12` bullet 2 — full scope)

| Req ID | Requirement | Implementation | API | Tests | Status |
|---|---|---|---|---|---|
| R-14 | Preserve: CREATED → PRESERVED only (EX-C002-05) | `services/access_evaluation_service.py:179-208` | `POST /{id}/preserve` → 200 | `test_preserve_transitions_created_to_preserved`, `test_preserve_and_expire_lifecycle` | **Implemented** |
| R-15 | Preserve shall reject a non-CREATED outcome (409) | `:185-196` | → 409 | `test_preserve_rejects_non_created_outcome`, API duplicate-preserve assertion | **Implemented** |
| R-16 | Expire: PRESERVED → EXPIRED only, explicit and caller-invoked (EX-C002-06) | `:210-242` | `POST /{id}/expire` → 200 | `test_expire_transitions_preserved_to_expired`, `test_preserve_and_expire_lifecycle` | **Implemented** |
| R-17 | Expire shall reject a non-PRESERVED outcome (409) | `:219-230` | → 409 | `test_expire_rejects_non_preserved_outcome`, `test_expire_rejects_outcome_that_was_never_preserved` | **Implemented** |
| R-18 | Expiry at scope boundary (EX-C002-06 "Expire ... at Scope Boundary") | — | — | — | **Missing / Deferred** — no scope boundary is modelled at all. There is no execution-scope identifier, no time bound, and no automatic expiry. `IRA-005 §11` line 262 states validity is "Object Scoped, Event Scoped, and Time Scoped to the single governed execution it was produced for" — **none of these three scopings exists in the schema**. Disclosed only obliquely in a code docstring (`:213-217`). **F-08** |
| R-19 | BA-02 shall emit PRESERVED/EXPIRED events | `:207, :241` | n/a | **none** | **Implemented, untested** |

### 4.4 BA-03 requirements (`IRA-005 §12` bullet 3 — classification/detection portion only)

| Req ID | Requirement | Implementation | API | Tests | Status |
|---|---|---|---|---|---|
| R-20 | BA-03 shall classify/detect a governing-fact change and invalidate a live outcome (EX-C002-07) | `services/access_evaluation_service.py:248-302` | `POST /{id}/context-change` → 200 | `test_detect_context_change_invalidates_live_outcome`, `test_context_change_invalidates_outcome` | **Partially Implemented** — invalidation works, but no *detection* occurs: the decision is driven entirely by an unvalidated free-text `changed_fact` string. **F-09** |
| R-21 | BA-03 shall reject a non-live outcome (409) | `:263-274` | → 409 | `test_detect_context_change_rejects_non_live_outcome`, `test_context_change_rejects_non_live_outcome` | **Implemented** |
| R-22 | BA-03 shall **never** re-resolve to a fresh determination (`IRA-005 §12`) | `:248-302` contains no call to `evaluate()`, no `AccessEvaluationOutcome` construction, no `AccessEvaluationOutcomeType` reference | n/a | implied by the 409/200 assertions | **Implemented** — independently verified |
| R-23 | BA-03 shall emit `ACCESS_EVALUATION_OUTCOME_INVALIDATED` | `:292-295` | n/a | **none** | **Implemented, untested** |

### 4.5 BA-04 requirements (`IRA-005 §12` bullet 4 — full scope)

| Req ID | Requirement | Implementation | API | Tests | Status |
|---|---|---|---|---|---|
| R-24 | BA-04 shall classify a dependent capability's rejection into exactly two classes (BR-C002-05, Contract 5.6) | `schemas/access_evaluation.py:112-122`; `services/...:322-337` | `POST /{id}/handoff-rejection` → 200 | 2 unit + 2 API tests | **Implemented** |
| R-25 | Classification shall derive from the outcome's own `validity_status`, never from the reporting capability's stated reason | `services/...:322` — the `if` reads only `outcome.validity_status`; `request.stated_reason` appears only in `record_audit` metadata `:345` | n/a | both classification tests pass an unrelated `stated_reason` | **Implemented** — independently verified |
| R-26 | INTEGRITY_SIGNAL shall route to BA-01 | `:337` | n/a | `test_resolve_handoff_rejection_classifies_invalidated_outcome_as_integrity_signal` | **Implemented** — routing is a *string label* only; no actual routing occurs. Accurate to the schema's own description (`schemas:158`), so not a defect, but noted |
| R-27 | BA-04 shall emit `ACCESS_HANDOFF_REJECTION_RESOLVED` | `:350-353` | n/a | **none** | **Implemented, untested** |
| R-28 | The hand-off rejection shall be recorded | `record_audit` `:339-349` only | n/a | none | **Partially Implemented** — the rejection is logged, never persisted. No queryable record of any hand-off rejection exists. Not required by `IRA-005`; recorded as an observation (F-15) |

### 4.6 Cross-cutting governance requirements

| Req ID | Requirement (source) | Evidence | Status |
|---|---|---|---|
| R-29 | Every Business Activity shall have a Business Activity Contract with `IMP-001 §6.7`'s 16 attributes | IMP-REPORT-WP-05 lines 13–26, 32–43, 49–58, 64–75 | **Partially Implemented** — 6 of 16 present. **F-04** |
| R-30 | Tenant isolation shall be preserved (`CLAUDE.md §14`, §11) | `middleware/tenant.py:132-139,161`; repository query `:26-32` | **Not satisfied** — **F-02** |
| R-31 | No new architecture without approval (`CLAUDE.md §18`) | `git show --stat 84b095b`: one table, five endpoints, no new service boundary | **Implemented** |
| R-32 | Reuse → Configure → Extend → Compose → Create order (`CLAUDE.md §19.5`) | `DomainPermissionLevel`, `ApprovalAuthority`, `Membership`, `Domain`, `BaseRepository`, `require_platform_admin`, `record_audit` all reused verbatim; `AccessEvaluationOutcome` justified as a genuine Create (IMP-REPORT line 83) | **Implemented** |
| R-33 | Technical Debt shall be visible, traceable, prioritised (`CLAUDE.md §19.8`) | TECH-DEBT.md lines 109–111, 948–978 | **Partially Implemented** — TD-081 lacks a Detailed Entry and a §19.8.7 severity assignment (F-10); at least four real limitations are undocumented (F-08, F-11, F-12, F-15) |
| R-34 | Independent Certification shall be performed by a genuinely independent fresh-context reviewer (`CLAUDE.md §19.7`, ADR-014) | `CERT-WP-05` line 7 asserts this | **Implemented in form** — but the certification's evidence does not match the certified artifact (**F-06**) |

### 4.7 Implementation without a traceable requirement

Every implemented behaviour traces to a governing document, with these exceptions:

| Implemented behaviour | Traceability |
|---|---|
| `PreserveAccessEvaluationOutcomeRequest` / `ExpireAccessEvaluationOutcomeRequest` — empty request bodies, required on the wire (`schemas:57-64`; `routers:110,132`) | No governing document requires a request body for a pure state transition. Forces every caller to send `{}`. Harmless but unrequired. Recorded as F-17 (Low) |
| HTTP **501 Not Implemented** as the out-of-scope signal (`services:166-173`) | First and only use of 501 anywhere in this service (verified: `grep -rn "501\|NOT_IMPLEMENTED" routers/ services/` matches nothing outside `access_evaluation`). Not enumerated by any repository API standard. **Justified** — it is the honest, semantically correct code and satisfies `IMP-API-004`'s "errors are explained" rule better than any alternative. Recorded as an observation, not a defect |
| `routed_to = "BA-01 (Evaluate Access for a Governed Request)"` — a human-readable string, not an identifier (`services:337`) | No document specifies the shape. Accurately described by `schemas:158`. Observation only |

**No implemented behaviour was found that contradicts a governing document, and no unauthorized capability was found.**

---

## 5. Specification Conformance Audit

Every mandatory (MUST/SHALL/REQUIRED/MANDATORY/explicitly-prohibited) statement bearing on WP-05 was extracted and individually verified.

### 5.1 IRA-005 §12 — the authorization boundary (the controlling scope statement)

| # | Mandatory statement (IRA-005 §12, verbatim in relevant part) | Implemented? | Evidence | Pass/Fail |
|---|---|---|---|---|
| S-01 | "BA-01 ... Unresolved and Deferred outcome branches only (`EX-C002-03`/`EX-C002-04`)" | Yes | `services/access_evaluation_service.py:110-118` writes `UNRESOLVED`; `:135-144` writes `DEFERRED`; no other creation site exists | **PASS** (with F-01 qualifying the Unresolved branch's production viability) |
| S-02 | "Permitted and Denied branches ... SHALL NOT be implemented as part of this authorization" | Yes — absent | No executable statement references `.PERMITTED` or `.DENIED`; `grep` over the service returns only `AuditStatus.DENIED` at 6 sites (audit-log status vocabulary, not outcome type) | **PASS** |
| S-03 | "reaching them requires a separate, future, gap-analyzed integration with `WP-RTA-001` ... not assumed here" | Yes | `services:166-173` raises 501 with a detail naming `IRA-005 S12` and `CLAUDE.md S19.8.5`; no import of, or reference to, `Backend/Runtime/` anywhere in WP-05 | **PASS** |
| S-04 | "BA-02 ... full scope, no blocker" | Yes | `preserve()` `:179-208`, `expire()` `:210-242`, both guards enforced pre-mutation | **PASS on the transitions; PARTIAL on "full scope"** — EX-C002-06's *scope boundary* is not modelled at all (R-18 / F-08) |
| S-05 | "BA-03 ... classification/detection portion only. The 're-resolve to a fresh Permitted/Denied determination' path ... is out of this authorization" | Yes — the excluded path is absent | `detect_context_change()` `:248-302` contains no `evaluate()` call, no outcome creation, no `AccessEvaluationOutcomeType` reference | **PASS on the exclusion; PARTIAL on "detection"** — see F-09 |
| S-06 | "BA-04 ... full scope, no blocker" | Yes | `resolve_handoff_rejection()` `:308-361`, both classification branches present | **PASS** |
| S-07 | "`WPR-001`'s own WP-05 row and `WP-REG-001`'s own WP-05 row are updated in the same governance pass" (§12 line 311) | Yes | `WPR-001:30`, `WP-REG-001:92` both updated | **PASS** |

### 5.2 ADR-015 — the registration decision

| # | Mandatory statement | Implemented? | Evidence | Pass/Fail |
|---|---|---|---|---|
| S-08 | Decision 1 — register `AEO-000001` with the `IRA-005 §11` entry adopted by reference | Yes | `IRA-005:249-266`; model docstring `models/...:46-59` cites `AEO-000001`, `ADR-015` | **PASS** |
| S-09 | Decision 2 — **do not** register Governed Request Context or the four Preserved/Superseded/Invalidated/Deferred constructs | Yes | Exactly one model, one table. The four labels appear only as `AccessEvaluationValidityStatus` enum values (`models/...:37-43`), never as separate objects | **PASS** |
| S-10 | Decision 3 — "This ADR does not authorize any Business Activity's implementation ... still requires its own fresh implementation-readiness gap analysis per CLAUDE.md §19.7" | Yes | `IRA-005 §12` supplies the authorization; IMP-REPORT lines 79–95 record the gap analysis | **PASS** |
| S-11 | Decision 4 — this ADR does not resolve the Authorization Engine governance question | Yes | Resolved separately by `IRA-005 §12` (Option 2) and `ADR-016:22`; WP-05 builds no engine | **PASS** |
| S-12 | Decision 5 — no pattern-level ADR; single-object lifecycle | Yes | One table, one aggregate root, no chain | **PASS** |
| S-13 | "`CMD-001 §26.7` (Physical Implementation Mapping) remains entirely unset for `AEO-000001`" — implying WP-05, having supplied it, should record it | **No** | No update to `CMD-001 §26.7` or any equivalent register was made recording the now-known Physical Table, APIs, and Events | **FAIL (Low)** — **F-13** |

### 5.3 CLAUDE.md §19.8.5 — the non-deferrable defect classes (the prohibition that defines this Work Package)

`CLAUDE.md §19.8.5` states Technical Debt SHALL NOT be used to defer: architectural defects, **security defects**, **data integrity defects**, **tenant isolation defects**, failing tests, build failures, broken functionality, or mandatory compliance requirements.

| # | Prohibition | Verified? | Evidence | Pass/Fail |
|---|---|---|---|---|
| S-14 | No fabricated `PERMITTED` outcome may be deferred as Technical Debt | Yes, and honoured | Four-way verification, Section 8.9. The 501 path is the *correct* handling: it neither fabricates nor silently declines | **PASS** — this is the requirement WP-05 most needed to satisfy, and it does |
| S-15 | No **data integrity** defect may be deferred | **No — violated** | F-01: the `UNRESOLVED` branch writes an orphan FK. Empirically reproduced (Section 9.6). Not disclosed in `TECH-DEBT.md`, `IMP-REPORT-WP-05`, or `CERT-WP-05` | **FAIL (High)** |
| S-16 | No **tenant isolation** defect may be deferred | **No — violated** | F-02: cross-organization Approval Authority selection with cross-tenant name disclosure. Empirically reproduced (Section 8.6). Not disclosed anywhere | **FAIL (High)** |
| S-17 | No failing tests / build failures | Yes | 601/601 pass; single Alembic head | **PASS** |

### 5.4 CLAUDE.md §18 / §19.4 — Architectural Change Control

| # | Prohibition | Verified? | Evidence | Pass/Fail |
|---|---|---|---|---|
| S-18 | No new entity/table/column/API/service boundary/workflow/permission/event beyond what is documented | Conformant | One table (`AEO-000001`'s own, authorized by ADR-015 + IRA-005 §12 + IMP-REPORT's gap analysis); five endpoints, all named by IMP-REPORT; four events, all named by IMP-REPORT; no new permission (reuses `PLATFORM_ADMIN`) | **PASS** |
| S-19 | No new technology | Conformant | FastAPI/SQLAlchemy/Alembic/Pydantic only, per `CLAUDE.md §9` | **PASS** |
| S-20 | No new background job or scheduled process | Conformant, and explicitly declined | `services:213-217` states expiry is caller-invoked because a scheduler "would require ... a new architectural component out of this Work Package's own scope" — a correct §18 STOP applied in the small | **PASS** — commendable |

### 5.5 IMP-001 mandatory statements

| # | Statement | Implemented? | Evidence | Pass/Fail |
|---|---|---|---|---|
| S-21 | §6.7 — "Every Business Activity **shall** have a Business Activity Contract" including 16 named attributes | Partially | IMP-REPORT supplies Business Intent, Input Contract, Output Contract, Business Rules, Authorization, Events, Audit (7 of 16 fields, one of them — Business Rules/Validation Rules — not in §6.7's own list). **Absent for all four BAs:** Activity Identifier, Business Domain, Business Object, Activity Type, Preconditions, Postconditions, Workflow, AI Assistance, Definition of Done, **Idempotency** | **FAIL (Medium)** — **F-04** |
| S-22 | §6.7 — "Idempotency ... **required** for any write endpoint callable twice against the same target" | **No** | Five write endpoints exist; none has an Idempotency disclosure. BA-02/BA-03 are in fact guarded (409). **BA-01 is genuinely non-idempotent**: `POST /access-evaluations` creates an unbounded number of duplicate outcomes for the same `(membership_id, domain_id, permission_level)` triple — no uniqueness check in `evaluate()`, and `grep -n "UniqueConstraint"` over both the model and the migration returns **nothing** | **FAIL (Medium)** — **F-04** |
| S-23 | §6.16.7 — "Authorization **shall** invoke the centralized authorization framework defined by URA-001" | No | `require_platform_admin` is a single role-claim equality check (`dependencies.py:45-49`), not URA-001-76's precedence chain | **FAIL, but fully disclosed** — TD-079 covers this exactly; identical class to TD-021–025/031/034–036/039/042 across every prior WP. **Accepted as pre-existing, repository-wide.** TD-079 would be improved by citing `IMP-API-002` explicitly (recommendation R-10) |
| S-24 | §6.16.7 — "Business Activities **shall never** implement authorization logic internally" | Yes | The service contains no endpoint-authorization logic; the gate is a router-level `Depends` | **PASS** |
| S-25 | IMP-API-001 — "the URL names the Business Activity, not the underlying object" | No | `POST /access-evaluations` names the object | **FAIL, pre-existing and repository-wide** — identical to `POST /organizations`, `POST /memberships`, `POST /structural-completions` and every other endpoint in this service. **Not a WP-05 defect**; WP-05 correctly followed the established convention rather than inventing a divergent one. Recorded as an observation for the repository, not a finding against WP-05 |
| S-26 | IMP-API-004 — a business-rule rejection "**shall** state ... which specific rule was violated, by reference to its principle ID" | Partially | The **501** detail cites `IRA-005 S12` and `CLAUDE.md S19.8.5` — conformant and exemplary. The **409** details (`services:195, :229, :273`) and **404** details (`:100, :379`) cite no rule ID. Comparator: `services/structural_completion_service.py:112-116` also cites none | **FAIL, pre-existing and repository-wide** — recorded as an observation, not a WP-05-specific finding |

### 5.6 CLAUDE.md §14 — Definition of Done

| Criterion | Verdict | Evidence |
|---|---|---|
| Implementation complete | Yes, within authorized scope | Section 4 |
| Architecture respected | Yes | S-18–S-20 |
| DS-001 respected | N/A | Backend-only; no UI |
| Governing Capability Specification respected | Substantially, with F-09 qualifying BA-03 | Section 5.1 |
| Tests pass | Yes — 601/601 | Section 3 |
| Security verified | **No** | F-02 (tenant leak), F-03 (no actor attribution) |
| Accessibility verified | N/A | No UI |
| Performance acceptable | Not assessed by anyone | No benchmark, no index-plan review. Queries are trivial and indexed; no concern identified, but no evidence either |
| **Tenant isolation preserved** | **No** | **F-02** |
| Traceable to governing canonical documents | Yes — exemplary | Every file cites `IRA-005 §12`, `ADR-015`, `AEO-000001`, and the governing EX |
| Maintainable | Yes | Section 7.9 |
| Documentation updated | Partially | F-05, F-06, F-07, F-08, F-13 |
| Build succeeds | Yes | Section 3 |

**§14 is not fully satisfied**, on the "security verified" and "tenant isolation preserved" criteria specifically.

---

## 6. Business Activity Audit

### 6.1 A note on Acceptance Criteria

`IRA-005` — the governing readiness assessment — **contains no per-Business-Activity Acceptance Criteria section.** §3 (lines 72–85) gives each candidate BA a one-line "Business-Meaningful Action"; §7 (lines 154–163) gives each a Gap Analysis category; §12 (lines 302–309) gives each a scope authorization. Nothing in `IRA-005` states testable acceptance criteria.

Per this audit's own rule, this is reported rather than filled in: **Acceptance Criteria for BA-01 through BA-04 do not exist in the governing document.** The closest approximation is the Business Activity Contract in `IMP-REPORT-WP-05`, which is an *implementation* artifact, not a governing one — and which per F-04 is itself incomplete against `IMP-001 §6.7`. Conformance below is therefore assessed against `IRA-005 §12`'s scope statements and `IRA-005 §11`'s Lifecycle Model, the only governing statements that exist.

### 6.2 BA-01 — Evaluate Access for a Governed Request

| Dimension | Finding | Evidence |
|---|---|---|
| **Business Objective** | Produce exactly one Access Evaluation Outcome for a specific governed request, limited to Unresolved/Deferred | `services:66-88` docstring; `IRA-005:78` |
| **Inputs** | `membership_id: UUID`, `domain_id: UUID`, `permission_level: DomainPermissionLevel` — all required, no defaults | `schemas:15-34` |
| **Outputs** | `AccessEvaluationOutcomeResponse` (10 fields), HTTP 201 | `schemas:37-50`; `routers:61-64` |
| **Validation** | Domain existence (404). `permission_level` validated by Pydantic enum → 422. **No validation that `membership_id` references a real Membership** — this is deliberate (it is the UNRESOLVED trigger) and is precisely the cause of **F-01** | `services:89-101, :103-108` |
| **Authorization** | `require_platform_admin` (`routers:86`). 400 missing header, 401 bad token, 403 wrong role | `dependencies.py:28-50` |
| **Persistence** | `outcome_repo.create()` + `session.flush()`; transaction commit deferred to `db_manager.get_session()` (`models/database.py:70-78`) | `services:110-119, :135-145` |
| **Events** | `ACCESS_EVALUATION_OUTCOME_CREATED` on both success branches. **Not emitted on the 501 path** — correct, no state change occurred | `services:127-130, :153-156` |
| **Audit Logging** | All four paths audited. **Actor is always `"SYSTEM"`** (F-03) | `services:91, :120, :146, :159` |
| **Error Handling** | 404/501 via `HTTPException`. **No `IntegrityError` handling** despite `services/structural_completion_service.py:118-144` establishing exactly that pattern in WP-04 | **F-01 aggravating factor** |
| **Business Rules** | BR-C002-02 (closed set) honoured; the ordering — Domain → Membership → Approval Authority → 501 — is deterministic and documented (`services:77-87`) | Verified |
| **Acceptance Criteria** | **Do not exist in IRA-005** (§6.1) | — |
| **Automated Tests** | 5 unit + 7 API. Cover: 404, UNRESOLVED×2, DEFERRED, 501, 400, 403, 422 | Verified by execution |
| **Runtime behaviour (traced)** | Section 6.6.1. **Diverges from tested behaviour on PostgreSQL** for the missing-Membership case | **F-01** |
| **Missing** | Idempotency guard/disclosure (F-04); organization scoping on the Approval Authority lookup (F-02); FK-safe handling of the missing-Membership case (F-01); event and audit assertions (F-14, F-03) | — |

### 6.3 BA-02 — Preserve and Bound Access Evaluation Outcome Validity

| Dimension | Finding | Evidence |
|---|---|---|
| **Business Objective** | Hold an outcome valid for its governed execution and expire it at that boundary | `IRA-005:79` |
| **Inputs** | `outcome_id` path param; empty request bodies (required on the wire — F-17) | `schemas:57-64`; `routers:109-110, :131-132` |
| **Outputs** | Updated `AccessEvaluationOutcomeResponse`, HTTP 200 | `routers:98-99, :120-121` |
| **Validation** | Existence (404 via `_get_or_404`); state guard (409) checked **before** mutation in both methods | `services:184-196, :218-230` |
| **Authorization** | `require_platform_admin` on both endpoints | `routers:112, :134` |
| **Persistence** | `update()` + `flush()`; `updated_at` set by the model's `onupdate` | `services:198-199, :232-233` |
| **Events** | `..._PRESERVED`, `..._EXPIRED` | `services:207, :241` |
| **Audit Logging** | 404, 409, and success paths all audited; actor always `"SYSTEM"` (F-03) | `services:186, :200, :220, :234` |
| **Error Handling** | Consistent 404/409 with descriptive detail naming the current status | Verified |
| **Business Rules** | CREATED→PRESERVED→EXPIRED strictly enforced; no path allows PRESERVED→PRESERVED, CREATED→EXPIRED, or any transition out of EXPIRED/INVALIDATED | Verified by reading both guards |
| **Acceptance Criteria** | Do not exist in IRA-005 | — |
| **Automated Tests** | 5 unit + 3 API. Both transitions, both 409 guards, 404 | Verified by execution |
| **Runtime behaviour** | Section 6.6.2 — fully demonstrable | — |
| **Missing** | **The "Bound" half of this BA's own name.** `EX-C002-06` is "Expire ... **at Scope Boundary**" and `IRA-005:262` states validity is Object/Event/Time Scoped. **No scope identifier, no time bound, and no automatic expiry exist in the schema or the code.** What is implemented is a manually-invoked status flip, which is a valid Option-A-style minimum, but the omission is disclosed only in a code docstring and **appears in no Technical Debt entry.** **F-08** |

### 6.4 BA-03 — Detect and Resolve Access Context Change (classification portion)

| Dimension | Finding | Evidence |
|---|---|---|
| **Business Objective** | Re-resolve — here, classify — an outcome when a governing fact changes | `IRA-005:80, :306` |
| **Inputs** | `outcome_id` path param; `changed_fact: str` (1–500 chars) | `schemas:73-91` |
| **Outputs** | `AccessContextChangeOutcome` (5 fields), HTTP 200 | `schemas:94-104` |
| **Validation** | Existence (404); liveness guard `_LIVE_VALIDITY_STATUSES` = {CREATED, PRESERVED} (409). **`changed_fact` is validated only for length** — never checked against any authority | `services:262-274, :43-46` |
| **Authorization** | `require_platform_admin` | `routers:164` |
| **Persistence** | `validity_status` → INVALIDATED; `reason` appended as `"{old} | Invalidated: {changed_fact}"` | `services:277-284` |
| **Events** | `ACCESS_EVALUATION_OUTCOME_INVALIDATED` with `changed_fact` | `services:292-295` |
| **Audit Logging** | 404, 409, success; actor `"SYSTEM"` (F-03) | `services:264, :285` |
| **Error Handling** | Consistent | Verified |
| **Business Rules** | The **exclusion** (never re-resolve) is correctly and verifiably honoured — R-22 | Verified |
| **Acceptance Criteria** | Do not exist in IRA-005 | — |
| **Automated Tests** | 2 unit + 2 API | Verified |
| **Runtime behaviour** | Section 6.6.3 — demonstrable |
| **Missing / questionable** | **No detection occurs.** The Business Activity is named "**Detect** and Resolve Access Context Change" and `IRA-005:158` describes "Re-resolving a changed fact and determining 'same or different determination'". What is implemented unconditionally trusts a caller-supplied free-text assertion and always invalidates. `BR-C002-01` (per `IRA-005:66`, "exclusive derivation from owning authorities") is the relevant rule: the invalidation basis is a client string, never a fact re-read from Membership, Domain, or Approval Authority. The service's own docstring is honest about this (`:256-260`), and it is arguably inside "classification/detection portion only" — but the gap between the BA's name and its behaviour is disclosed nowhere in `TECH-DEBT.md`. **F-09** |
| **Also missing** | `reason` is mutated by concatenation, overwriting the sole record of the pre-invalidation reasoning shape. Combined with the absence of any prior-state record, `IRA-005:261`'s "Full history retained for audit and traceability" is only partially met. **F-12** |

### 6.5 BA-04 — Resolve Dependent Capability Access Hand-off Rejection

| Dimension | Finding | Evidence |
|---|---|---|
| **Business Objective** | Classify and route a dependent capability's rejection of a produced outcome | `IRA-005:81` |
| **Inputs** | `outcome_id`; `reporting_capability` (1–50), `stated_reason` (1–1000) | `schemas:125-149` |
| **Outputs** | `AccessHandoffRejectionOutcome` (6 fields), HTTP 200 | `schemas:152-161` |
| **Validation** | Existence (404) only. **No state guard** — deliberate and correct: both live and non-live outcomes are valid inputs, each yielding a different classification | `services:319-337` |
| **Authorization** | `require_platform_admin` | `routers:188` |
| **Persistence** | **None.** No row is created or mutated | `services:308-361` |
| **Events** | `ACCESS_HANDOFF_REJECTION_RESOLVED` | `services:350-353` |
| **Audit Logging** | 404 and success; records `reporting_capability`, `stated_reason`, computed `classification` | `services:339-349` |
| **Error Handling** | 404 only; consistent | Verified |
| **Business Rules** | `BR-C002-05` / Contract 5.6's "signal, not an authority" discipline is **genuinely** implemented: `services:322` branches on `outcome.validity_status` alone; `request.stated_reason` appears only at `:346` inside audit metadata. Independently re-verified, and independently corroborated by tests that pass an unrelated `stated_reason` in both branches | Verified |
| **Acceptance Criteria** | Do not exist in IRA-005 | — |
| **Automated Tests** | 3 unit + 2 API — both classifications plus 404 at the unit layer; both classifications at the API layer (404 not covered at the API layer) | Verified |
| **Runtime behaviour** | Section 6.6.4 — demonstrable |
| **Missing** | No persisted record of the rejection (R-28 / F-15). API-layer 404 test absent (F-14). `routed_to` is a label, not a mechanism — accurately documented, not a defect |

### 6.6 Implementation Demonstration — end-to-end code-path traces

For each Business Activity the full chain **Request → Validation → Authorization → Execution → Persistence → Audit → API Response → Database State → Completion** was traced through actual code. Where a step cannot be demonstrated, that is stated explicitly.

#### 6.6.1 BA-01 — `POST /access-evaluations`

| Step | Traced code | Demonstrable? |
|---|---|---|
| **Request** | `TenantMiddleware.dispatch` (`middleware/tenant.py:140-162`) matches `path == "/access-evaluations"` at `:161` → `call_next` without requiring `X-Tenant-ID`. `LoggingMiddleware` runs. FastAPI binds `EvaluateAccessRequest` (`routers:84`) | ✔ |
| **Validation (syntactic)** | Pydantic validates 3 required fields; `permission_level` against `DomainPermissionLevel`. Failure → `RequestValidationError` → `main.py:56-70` → **422** | ✔ (tested) |
| **Authorization** | `Depends(require_platform_admin)` (`routers:86`) → `get_current_claims` (`dependencies.py:28-38`): missing/malformed header → **400**; `decode_access_token` failure → **401**; then `role_code != "PLATFORM_ADMIN"` → **403** (`:45-49`). Resolves **before** the handler body executes | ✔ (400/403 tested; 401 untested — U-09) |
| **Validation (structural)** | `domain_repo.get_by_id()` (`services:89`); `None` → audit DENIED (`:91-97`) → **404** (`:98-101`) | ✔ (tested) |
| **Execution — branch 1** | `membership_repo.get_by_id()` (`:103`); `None` **or** `membership_status != "ACTIVE"` → `reason` composed at `:105-109` → `outcome_type = UNRESOLVED` | ✔ for non-ACTIVE; **✘ for missing Membership on PostgreSQL — F-01** |
| **Execution — branch 2** | `get_active_domain_approval_authority()` (`:133`); non-`None` → `outcome_type = DEFERRED`, `approval_authority_id` set (`:135-144`) | ✔ — but crosses organizations, **F-02** |
| **Execution — branch 3** | Neither branch → audit DENIED (`:159-165`) → **501** (`:166-173`). **No row is written** | ✔ (tested) |
| **Persistence** | `outcome_repo.create()` → `session.add` (`base_repository.py:36-38`); `session.flush()` (`services:119`/`:145`) issues the INSERT; commit deferred to `db_manager.get_session()` (`models/database.py:73`) | ✔ for DEFERRED; **✘ for missing-Membership UNRESOLVED — F-01** |
| **Audit** | `record_audit("EVALUATE_ACCESS", …)` on all four paths | ✔ coverage; **actor always `"SYSTEM"` — F-03** |
| **Event** | `publish_event("ACCESS_EVALUATION_OUTCOME_CREATED", …)` (`:127`/`:153`) | ✔ emitted; **no test asserts it — F-14** |
| **API Response** | `AccessEvaluationOutcomeResponse.model_validate(outcome)` (`routers:89`) → **201** with 10 fields | ✔ (tested) |
| **Database state** | One `access_evaluation_outcomes` row: `validity_status='CREATED'` (server_default), `outcome_type` UNRESOLVED\|DEFERRED, `created_at` set, `updated_at` NULL | ✔ |
| **Completion** | Session commits on clean handler exit; rolls back on any exception (`models/database.py:73-76`) | ✔ |

#### 6.6.2 BA-02 — `POST /{id}/preserve` and `POST /{id}/expire`

| Step | Traced code | Demonstrable? |
|---|---|---|
| Request / Authorization | Same middleware exemption (prefix match, `tenant.py:161`); `require_platform_admin` (`routers:112`/`:134`); `outcome_id` coerced to `UUID` → 422 if malformed | ✔ (auth not tested at these endpoints — U-08) |
| Validation | `_get_or_404` (`services:367-381`) → audit DENIED → **404**. Then the state guard: `!= CREATED` (`:185`) / `!= PRESERVED` (`:219`) → audit DENIED → **409**. Both guards precede any mutation | ✔ (all four cases tested) |
| Execution / Persistence | `outcome_repo.update()` (`base_repository.py:41-52`) sets `validity_status`; `flush()` issues the UPDATE; SQLAlchemy's `onupdate` sets `updated_at` (`models:117-121`) | ✔ |
| Audit / Event | `record_audit` + `publish_event` on success (`:200-207`, `:234-241`) | ✔ / **F-14** |
| API Response | Full updated outcome, **200** | ✔ |
| Database state | Same row; `validity_status` = PRESERVED then EXPIRED; `updated_at` populated. **Prior value not retained — F-12** | ✔ |
| Completion | Commit on exit | ✔ |

#### 6.6.3 BA-03 — `POST /{id}/context-change`

| Step | Traced code | Demonstrable? |
|---|---|---|
| Request / Authorization | As above (`routers:164`); body `changed_fact` validated 1–500 chars | ✔ (length boundaries untested — U-11) |
| Validation | `_get_or_404` → **404**; liveness check against `_LIVE_VALIDITY_STATUSES` (`services:263`, constant at `:43-46`) → **409**. **No verification of `changed_fact` against any authority — F-09** | ✔ / partial |
| Execution / Persistence | `update()` sets `validity_status='INVALIDATED'` and rewrites `reason` as `"{old} \| Invalidated: {changed_fact}"` (`:277-283`); `flush()` | ✔ |
| Audit / Event | `record_audit` + `publish_event("...INVALIDATED", {changed_fact})` (`:285-295`) | ✔ / **F-14** |
| API Response | `AccessContextChangeOutcome` — `invalidated=True`, `re_evaluation_required=True`, `checked_at`, **200** | ✔ |
| Database state | `validity_status='INVALIDATED'`; `reason` appended; `updated_at` set | ✔ |
| Completion | Commit; **no follow-on evaluation is triggered** — verified, `evaluate()` is never called | ✔ |

#### 6.6.4 BA-04 — `POST /{id}/handoff-rejection`

| Step | Traced code | Demonstrable? |
|---|---|---|
| Request / Authorization | As above (`routers:188`); `reporting_capability` 1–50, `stated_reason` 1–1000 | ✔ (boundaries untested — U-12) |
| Validation | `_get_or_404` → **404**. No state guard — both live and non-live are valid inputs | ✔ (404 at unit layer only — U-07) |
| Execution | Single branch on `outcome.validity_status in _LIVE_VALIDITY_STATUSES` (`:322`) → CAPABILITY_SCOPED_INSUFFICIENCY / INTEGRITY_SIGNAL, with `object_preserved`, `explanation`, `routed_to` derived (`:322-337`) | ✔ (both branches tested) |
| **Persistence** | **None — no row is created or mutated.** This step **cannot be demonstrated because it does not exist** (F-15) | **✘ by design** |
| Audit / Event | `record_audit` recording `reporting_capability`, `stated_reason`, computed `classification` (`:339-349`); `publish_event("ACCESS_HANDOFF_REJECTION_RESOLVED", …)` (`:350-353`) | ✔ / **F-14** |
| API Response | `AccessHandoffRejectionOutcome` (6 fields), **200** | ✔ |
| Database state | **Unchanged** — correct for CAPABILITY_SCOPED_INSUFFICIENCY (`object_preserved=True`); for INTEGRITY_SIGNAL the response says `object_preserved=False` and `routed_to="BA-01 …"`, but **no state change and no routing actually occur** — the schema documents this accurately (`schemas:158`), so it is disclosed, not concealed | ✔ with caveat |
| Completion | Commit (no changes to flush) | ✔ |

#### 6.6.5 Steps that cannot be demonstrated

| Step | Reason |
|---|---|
| BA-01's missing-Membership persistence on PostgreSQL | Raises `IntegrityError` → HTTP 500. **F-01** |
| BA-04's persistence | No persistence exists. **F-15** |
| BA-02's expiry *at a scope boundary* | No scope, no time bound, no scheduler exists. **F-08** |
| BA-03's *detection* of a context change | No authority is re-read; the caller's assertion is trusted. **F-09** |
| Any live-PostgreSQL migration application | No PostgreSQL instance available. **F-20** |
| Audit attribution of a real actor | Always `"SYSTEM"`. **F-03** |

---

## 7. Architecture Compliance Review

### 7.1 Layering and dependency direction

The implementation follows the service's established five-layer shape exactly:

```
routers/access_evaluation.py      →  services/access_evaluation_service.py
                                   →  repositories/access_evaluation_outcome_repository.py
                                   →  models/access_evaluation_outcome.py
schemas/access_evaluation.py      (contract layer, imported by router + service)
```

Verified by import inspection: the model imports only `models.database` and SQLAlchemy; the repository imports only models + `BaseRepository`; the service imports models, repositories, schemas, `observability`, and `fastapi` (for `HTTPException`); the router imports the service, repositories, schemas, `dependencies`, and `models.database`. **No inward dependency inversion** (no model importing a service, no repository importing a router). **PASS.**

### 7.2 FastAPI leakage into the business layer

`services/access_evaluation_service.py:27` imports `from fastapi import HTTPException, status`, and every rejection is raised as an `HTTPException`. This means the business layer is not framework-independent, contrary to `CLAUDE.md §2` ("Keep business logic framework-independent").

**However:** this is the established convention of every service in this repository (verified against `services/structural_completion_service.py:110-116`, `services/structural_validation_service.py:75-120`). WP-05 following it is the correct choice under `CLAUDE.md §12`'s Extend→Refactor→Reuse ordering; diverging would have created a parallel error-handling convention. **Recorded as a pre-existing repository-wide observation, not a WP-05 finding.**

### 7.3 Repository pattern usage

`AccessEvaluationOutcomeRepository` extends `BaseRepository[AccessEvaluationOutcome]` and adds exactly one domain-specific query (`get_active_domain_approval_authority`). It correctly reuses `BaseRepository.get_by_id/create/update` rather than reimplementing them (`repositories/access_evaluation_outcome_repository.py:11-15`). **PASS on pattern; FAIL on that one query's correctness — F-02.**

One structural observation: `get_active_domain_approval_authority()` queries the **`ApprovalAuthority`** table from the **`AccessEvaluationOutcome`** repository. An `ApprovalAuthorityRepository` exists in this service. Placing a foreign-aggregate query on this repository is a mild cohesion smell — and is very likely the proximate reason the organization filter was overlooked, since the canonical owner of that query would naturally have carried the organization-scoping convention with it. Recorded as F-18 (Low), with F-02 as its consequence.

### 7.4 Service pattern usage

Constructor injection of three repositories (`services:52-60`); no global state; no direct session construction; one public method per Business Activity plus one shared private helper (`_get_or_404`). Method-level docstrings cite the governing EX and the authorizing IRA section. **PASS — this is high-quality service design.**

### 7.5 API / router pattern

Dependency factories (`routers:31-54`) mirror the established pattern. Every route declares `response_model`, `status_code`, `summary`, `description`, and a `responses` map. **PASS.** One defect: the injected `claims` is bound but never used (`routers:86, 112, 134, 164, 188`) — the direct cause of **F-03**.

### 7.6 Database design

One table, three FKs, two indexes, three CHECK constraints. Column types are appropriate (`Uuid`, `String(20)`/`String(50)` sized to the constrained vocabularies, `Text` for the unbounded `reason`, `DateTime(timezone=True)` throughout). Naming follows the repository's `ck_<table>_<column>` and `ix_<table>_<column>` conventions exactly. **PASS** — see Section 10 for full detail.

### 7.7 Transaction boundaries

`session.flush()` is called after every mutation (`services:119, 145, 199, 233, 284`); `commit()` is never called by the service. The commit is owned by `db_manager.get_session()` (`models/database.py:70-78`), which commits on clean exit and rolls back on exception. This is correct Unit-of-Work discipline and matches `BaseRepository`'s own documented contract (`base_repository.py:38`). **PASS.**

**One consequence worth stating:** because rollback is global to the request, F-01's `IntegrityError` correctly discards the partial write — it does not corrupt data. F-01 is an availability/functional defect (HTTP 500 where 201 is specified), and a data-*integrity*-class defect in the §19.8.5 sense that the code **attempts** to write referentially invalid data, not a defect that leaves bad rows behind.

### 7.8 Tenant isolation

`/access-evaluations` and `/access-evaluations/*` are added to the tenant-exemption list (`middleware/tenant.py:161`) with a 8-line rationale comment (`:132-139`) that is accurate and appropriately narrow — it explicitly states the data **is** organization-scoped and that the exemption exists only because `PLATFORM_ADMIN` is the sole caller. This mirrors `/domain-permissions`' own precedent exactly and is disclosed as TD-079.

**The exemption itself is defensible and correctly disclosed. What is not defensible is F-02**, which is a separate matter: even accepting a PLATFORM_ADMIN-only, tenant-header-exempt endpoint, the *business logic* still crosses an organization boundary and discloses one tenant's Approval Authority name to a record anchored in another tenant. The middleware exemption governs request routing; it does not license the query in `repositories/access_evaluation_outcome_repository.py:26-32`. **FAIL — F-02.**

### 7.9 Async usage correctness

All five service methods and all repository methods are `async def` and are correctly `await`ed at every call site. No blocking I/O, no `time.sleep`, no synchronous DB driver. `datetime.now(timezone.utc)` is used (never naive `utcnow()`), consistent with the timezone-aware columns. **PASS.**

### 7.10 Error handling consistency

Status codes are used consistently and correctly across the five endpoints: 201 for creation, 200 for state transitions and classifications, 404 for missing referents, 409 for state-guard violations, 422 for Pydantic validation, 400/401/403 from the shared auth dependency, and 501 for the explicitly-out-of-scope determination. Every `detail` string names the specific entity and, for 409s, the current status. **PASS** — with the `IMP-API-004` principle-ID gap noted at S-26 as a pre-existing repository-wide pattern.

### 7.11 CLAUDE.md §19.5 Reuse → Configure → Extend → Compose → Create

| Asset | Disposition | Verified |
|---|---|---|
| `DomainPermissionLevel` (8 URA-001-47 values) | **Reused** verbatim as the `permission_level` vocabulary | `schemas:7,24` — imported, not redeclared |
| `ApprovalAuthority` (WP-02) | **Reused** verbatim | `repositories/...:7,18` |
| `Membership`, `Domain` (WP-03/WP-02) | **Reused** verbatim | `services:31-32` via their own repositories |
| `BaseRepository` | **Extended** | `repositories/...:11` |
| `require_platform_admin` | **Reused** | `routers:7` |
| `record_audit`/`publish_event`/`AuditStatus` | **Reused** | `services:41` |
| WP-02 BA-10's `HandoffRejectionClassification` pattern | **Composed** — the pattern is mirrored for a different object, correctly, rather than the class being force-reused across capability boundaries | `schemas:112-122` |
| `AccessEvaluationOutcome` | **Created** — justified: no existing table could hold `AEO-000001`'s Lifecycle Model (IMP-REPORT line 83) | Verified: no pre-existing table has both an Outcome Type and a Validity Status dimension |

**PASS — the Reuse→Create order was genuinely applied, and the single Create is genuinely justified.**

---

## 8. Security Review

### 8.1 Authentication

All five endpoints depend transitively on `get_current_claims` (`dependencies.py:28-38`), which requires a `Bearer` header (400 if absent/malformed) and verifies the token via `decode_access_token` (401 on failure). **PASS.**

### 8.2 Authorization

`require_platform_admin` (`dependencies.py:41-50`) performs `claims.get("role_code") != "PLATFORM_ADMIN"` → 403. This is a single string-equality check, not URA-001-76's precedence chain (S-23). It is applied to all five endpoints (`routers:86, 112, 134, 164, 188` — each verified individually, not grepped). **PASS as implemented; disclosed gap correctly tracked as TD-079.**

### 8.3 Permission enforcement

There is no per-object, per-organization, or per-domain permission check anywhere in WP-05. Any `PLATFORM_ADMIN` may evaluate, preserve, expire, invalidate, or classify **any** outcome belonging to **any** organization. TD-079 describes this accurately and non-overstatedly. **Accepted as disclosed.**

### 8.4 Injection risk

Every query is constructed through SQLAlchemy Core/ORM expressions — `session.get()` (`base_repository.py:22`) and `select(...).where(Model.col == value)` (`repositories/access_evaluation_outcome_repository.py:26-32`). **No raw SQL, no string interpolation into a query, no `text()` construct anywhere in WP-05.** Verified by reading all query-bearing code.

The `reason` column is built by f-string interpolation of `approval_authority.authority_name` and `request.changed_fact` (`services:141, :281`), but these are bound as **parameters**, not concatenated into SQL — SQLAlchemy parameterizes the INSERT/UPDATE. No SQL injection risk. Note that this content is echoed back in API responses; there is no HTML escaping, but the response is `application/json` and no UI consumes it yet. **PASS on injection.**

### 8.5 Input validation

| Field | Constraint | Verified |
|---|---|---|
| `membership_id`, `domain_id`, `outcome_id` | Pydantic/FastAPI `UUID` → 422 on malformed | `schemas:22-23`; `routers:109,131,161,185` |
| `permission_level` | `DomainPermissionLevel` enum → 422 | `schemas:24`; tested |
| `changed_fact` | `min_length=1, max_length=500` | `schemas:82-85` |
| `reporting_capability` | `min_length=1, max_length=50` | `schemas:133-136` |
| `stated_reason` | `min_length=1, max_length=1000` | `schemas:137-140` |

All bounded, all required, no field accepts unbounded input. The `reason` DB column is `Text` (unbounded) but is only ever written from bounded inputs plus fixed templates. **PASS.**

### 8.6 Tenant isolation — **FAILING (F-02)**

**Hypothesis tested:** does BA-01's DEFERRED branch select an Approval Authority belonging to a different organization than the Membership being evaluated?

**Why it is plausible:** `Domain.organization_id` is `nullable=True` and documented as "NULL = platform-default domain, **visible to every tenant** (URA-001-43)" (`models/domain.py:38-43`). `ApprovalAuthority.organization_id` is `nullable=False`, "Required for every scope" (`models/approval_authority.py:103-108`). The lookup filters on `domain_id`, `scope_type`, `status` only (`repositories/access_evaluation_outcome_repository.py:26-32`) — **organization appears nowhere in the query.**

**Probe executed** (read-only, scratchpad): seeded Organization A and Organization B; a platform Domain (`organization_id=None`); a Membership in Org A; an ACTIVE, DOMAIN-scoped `ApprovalAuthority` named `"TENANT-B CONFIDENTIAL APPROVAL BOARD"` owned by **Org B**; then called `evaluate()` for Org A's Membership.

**Result:**

```
Membership organization_id : 58a6e84c-945f-4950-a2ec-1b45e231db28 (Tenant A)
Selected AA organization_id: 1a1db6bd-8a05-41ed-9445-bee864e752ab (Tenant B)
outcome_type               : DEFERRED
approval_authority_id      : cf25da1d-ac71-46f6-8487-829770170c5f
reason (persisted+returned): Governed by Approval Authority 'TENANT-B CONFIDENTIAL APPROVAL BOARD'
                             (cf25da1d-ac71-46f6-8487-829770170c5f); resolution pending approval.
CROSS-TENANT LEAK: True
```

**Three distinct defects follow:**

1. **Cross-tenant information disclosure.** Organization B's Approval Authority *name* and *id* are written into a persisted row anchored to Organization A's Membership, and returned verbatim in the API response body (`AccessEvaluationOutcomeResponse.reason`, `schemas:45`).
2. **Materially wrong business determination.** The request is DEFERRED to an authority with no jurisdiction over the requesting Membership's organization. `IRA-005:265` quotes Contract 5.7's prohibition on inferring authority; deferring to an unrelated tenant's authority is exactly such an inference.
3. **Nondeterminism.** `result.scalars().first()` (`:33`) has **no `ORDER BY`**. Where multiple organizations hold ACTIVE DOMAIN-scoped Approval Authorities on the same platform Domain, which one is selected is database-plan-dependent and may vary between calls.

**Why the existing tests cannot detect this:** both the unit fixture (`test_access_evaluation_service.py:111-118`) and the API fixture (`test_access_evaluation_api.py:60-67`) create the Approval Authority in the **same** organization as the Membership. No test exercises a second organization.

**Severity: High** under `CLAUDE.md §19.8.7` — it "weakens a security or tenant-isolation boundary, even if no exploit is currently known." **Non-deferrable** under `§19.8.5`.

### 8.7 Sensitive data handling

The table stores no credentials, no PII beyond foreign keys, and no secrets. `reason` is free text and may embed an Approval Authority name (see F-02). `Security Classification` for `AEO-000001` is "Internal" per `IRA-005:264`, and that document correctly discloses this as a default assumption rather than a citation. No hardcoded secrets exist in any WP-05 file. **PASS, with F-02 as the exception.**

### 8.8 Audit logging completeness — **PARTIALLY FAILING (F-03)**

**What is right:** `record_audit()` is called on every one of the 11 exit paths across the four Business Activities — the 404-domain path, both success creations, the 501 decline, both `_get_or_404` failures, both 409 guards in BA-02, BA-03's 409 and success, and BA-04's success. Independently verified by reading each method. This matches `CERT-WP-05 §4.6`'s claim.

**What is wrong, and what `CERT-WP-05 §4.6` did not check:** every one of those calls passes `actor_id=actor_id or "SYSTEM"`, and **`actor_id` is never supplied.** The five router handlers call the service without it (`routers:88, 114, 136, 166, 190`), even though each has an authenticated `claims` dict in scope containing `person_id`.

**Result:** 100% of WP-05 audit records attribute the action to `"SYSTEM"`. Confirmed by probe output:

```
INFO:authservice.audit:{"audit": true, "action": "EVALUATE_ACCESS", ...,
 "status": "SUCCESS", "actor_id": "SYSTEM", "tenant_id": "PLATFORM", ...}
```

`observability.py:74-79` states this function exists to answer SD-002-054's seven questions, of which **"Who"** is the first. WP-05's audit trail cannot answer it.

**This is a deviation from the repository's own universal convention, not a repository-wide gap.** `grep -rn "actor_id=claims\.get" routers/` returns **51 occurrences across 15 router files** — including `structural_completion.py:69`, `membership.py`, `role.py`, `organization.py`, `domain_permission.py`, `approval_authority.py`, and every other WP-01–WP-04 router. `routers/access_evaluation.py` is the **only** router in the service that omits it.

**Severity: Medium** (§19.8.7: an internal completeness/robustness concern touching observability, not itself a security-boundary weakening — the *control* works, only its record is anonymised).

### 8.9 The critical question: can any caller obtain PERMITTED or DENIED?

This is the single most important security question for this Work Package, and it was verified four independent ways rather than by reading `evaluate()` alone.

**Verification 1 — every creation site.** `AccessEvaluationOutcome` rows are created at exactly two locations in the entire repository: `services/access_evaluation_service.py:110-118` (literal `AccessEvaluationOutcomeType.UNRESOLVED.value`) and `:135-144` (literal `AccessEvaluationOutcomeType.DEFERRED.value`). Both are hard-coded enum members, neither is derived from any input. There is no other `AccessEvaluationOutcomeRepository.create()` call anywhere.

**Verification 2 — every mutation site.** `outcome_repo.update()` is called at three locations (`:198`, `:232`, `:277`). Their payload dicts contain only `validity_status` and (at `:277`) `reason`. **`outcome_type` is never in any update payload.** Therefore an outcome's type cannot change after creation — satisfying `IRA-005:260`'s "fixed at creation" and `BR-C002-02`.

**Verification 3 — token search.** `grep -rn "PERMITTED\|DENIED"` over the service, router, repository, and schema files returns **six matches, all `AuditStatus.DENIED`** (`services:94, 162, 189, 223, 267, 373`) — an audit-log status vocabulary value from `observability.py:62`, entirely unrelated to `AccessEvaluationOutcomeType`. **Zero occurrences of `PERMITTED` in any executable code.**

**Verification 4 — no external write path.** No `GET`/`PUT`/`PATCH`/`DELETE` endpoint exists (TD-080), so there is no API surface through which `outcome_type` could be supplied by a caller. `EvaluateAccessRequest` (`schemas:15-34`) has three fields, none of them `outcome_type`. There is no bulk-import, no admin override, no seed script writing this table.

**Conclusion: it is not possible for any caller, through any code path, to obtain a `PERMITTED` or `DENIED` Access Evaluation Outcome from WP-05.** `PERMITTED`/`DENIED` exist only in the enum (`models:31-32`) and the CHECK constraint (`models:64`, migration `:50`), both correctly declared to match `ADR-015`'s full registered Lifecycle Model rather than a narrowed non-conforming subset — the same discipline TD-052/TD-057/TD-062/TD-065/TD-069 established at WP-04.

**PASS — and this is the requirement WP-05 could least afford to fail.**

### 8.10 Privilege escalation

No path allows a caller to acquire authority they did not have. The 403 gate precedes all business logic. `AccessEvaluationOutcome` grants nothing — it is a determination record with no downstream enforcement consumer in this repository. Even F-02, while a disclosure and correctness defect, does not escalate privilege: it defers a request (denying immediate resolution) rather than permitting anything. **PASS.**

---

## 9. Test Coverage Review

### 9.1 Execution evidence

```
$ JWT_SECRET_KEY=ci-test-secret-key-not-for-production venv/Scripts/python.exe -m pytest tests/ -q
601 passed, 47 warnings in 255.92s (0:04:15)

$ ... -m pytest tests/test_access_evaluation_service.py tests/test_access_evaluation_api.py -v
29 passed, 2 warnings in 17.64s
```

All 15 unit tests and all 14 API tests were individually observed to pass (full `-v` listing captured). Actual counts confirmed: `test_access_evaluation_service.py` = **15**, `test_access_evaluation_api.py` = **14**.

### 9.2 Coverage by Business Activity

| BA | Unit | API | Positive | Negative | Boundary | Validation | AuthZ | Persistence-failure | Exception |
|---|---|---|---|---|---|---|---|---|---|
| BA-01 | 5 | 7 | ✔ (UNRESOLVED×2, DEFERRED) | ✔ (404, 501) | ✔ (501 is the boundary of authorized scope) | ✔ (422) | ✔ (400, 403) | **✘** | **✘** |
| BA-02 | 5 | 3 | ✔ (both transitions) | ✔ (both 409s, 404) | ✔ | n/a | **✘ (no 403/400 at BA-02 endpoints)** | **✘** | **✘** |
| BA-03 | 2 | 2 | ✔ | ✔ (409) | ✔ | **✘ (no empty/501-char `changed_fact` test)** | **✘** | **✘** | **✘** |
| BA-04 | 3 | 2 | ✔ (both classifications) | ✔ (404 unit only) | ✔ | **✘** | **✘** | **✘** | **✘** |

### 9.3 Assertion quality

Assertions are genuinely substantive, not status-code-only: `outcome_type`, `validity_status`, `approval_authority_id`, `reason` substring, `classification`, `object_preserved`, `routed_to`, `invalidated`, `re_evaluation_required` are all asserted. `test_evaluate_produces_unresolved_outcome_for_inactive_membership:104` asserts `"SUSPENDED" in outcome.reason` — a real content check. Both BA-04 tests deliberately pass an unrelated `stated_reason` to prove the classification does not depend on it. **This is above-average test quality for this repository.**

### 9.4 Specific untested branches (named precisely, not generically)

| # | Untested behaviour | Location | Layer |
|---|---|---|---|
| U-01 | **No test asserts any Domain Event is published.** Four event types (`..._CREATED`, `..._PRESERVED`, `..._EXPIRED`, `..._INVALIDATED`, `ACCESS_HANDOFF_REJECTION_RESOLVED`) are emitted; zero assertions exist on any of them | `services:127, 153, 207, 241, 292, 350` | both |
| U-02 | **No test asserts any audit record's content**, in particular `actor_id`. Had one existed, F-03 would have been caught | `services:91, 120, 146, 159, 186, 200, 220, 234, 264, 285, 339, 370` | both |
| U-03 | **No test exercises a second organization.** Directly conceals F-02 | fixtures `test_..._service.py:26-43`, `test_..._api.py:36-71` | both |
| U-04 | **No test runs with foreign-key enforcement on.** Directly conceals F-01 | `tests/conftest.py:19-36` — no `PRAGMA foreign_keys=ON` listener | both |
| U-05 | API 404 for `POST /{id}/expire` (only the unit layer covers `_get_or_404` for expire) | `routers:130` | API |
| U-06 | API 404 for `POST /{id}/context-change` | `routers:160` | API |
| U-07 | API 404 for `POST /{id}/handoff-rejection` (covered at unit layer only) | `routers:184` | API |
| U-08 | API 400/401/403 for all four sub-resource endpoints — auth is tested only on `POST /access-evaluations` | `routers:112, 134, 164, 188` | API |
| U-09 | Invalid/expired Bearer token → 401 (any endpoint). Noted by `CERT-WP-05 §4.4` as a repository-wide pattern | `dependencies.py:38` | API |
| U-10 | UNRESOLVED via **inactive** membership at the API layer (unit-only) | `services:104-108` | API |
| U-11 | `changed_fact` boundary: empty string and 501-character string → 422 | `schemas:82-85` | API |
| U-12 | `reporting_capability` / `stated_reason` length boundaries → 422 | `schemas:133-140` | API |
| U-13 | Transition out of `EXPIRED` (e.g. `expire` then `context-change`) — only the INVALIDATED-then-context-change path is tested | `services:263, 219` | both |
| U-14 | BA-04 classification of an **EXPIRED** outcome (only CREATED and INVALIDATED are tested; EXPIRED also yields INTEGRITY_SIGNAL) | `services:322` | both |
| U-15 | Concurrent duplicate `POST /access-evaluations` — no idempotency behaviour is tested because none exists (F-04) | `services:66` | both |
| U-16 | `_LIVE_VALIDITY_STATUSES` never tested against `SUPERSEDED` (unreachable, but the constant admits it) | `services:43-46` | both |

### 9.5 The structural problem with the test suite

**16 of the 29 WP-05 tests seed their fixture by calling `evaluate()` with `membership_id=uuid.uuid4()`** — a deliberately nonexistent Membership — to obtain an UNRESOLVED outcome cheaply.

Unit (9): `test_evaluate_produces_unresolved_outcome_for_unknown_membership`, `test_preserve_transitions_created_to_preserved`, `test_preserve_rejects_non_created_outcome`, `test_expire_transitions_preserved_to_expired`, `test_expire_rejects_non_preserved_outcome`, `test_detect_context_change_invalidates_live_outcome`, `test_detect_context_change_rejects_non_live_outcome`, `test_resolve_handoff_rejection_classifies_live_outcome_as_capability_scoped_insufficiency`, `test_resolve_handoff_rejection_classifies_invalidated_outcome_as_integrity_signal`.

API (7): `test_evaluate_access_returns_201_and_unresolved_for_unknown_membership`, `test_preserve_and_expire_lifecycle`, `test_expire_rejects_outcome_that_was_never_preserved`, `test_context_change_invalidates_outcome`, `test_context_change_rejects_non_live_outcome`, `test_handoff_rejection_classifies_live_outcome`, `test_handoff_rejection_classifies_invalidated_outcome_as_integrity_signal`.

Per F-01, **this seeding path cannot execute on PostgreSQL.** Consequently, on the production database, BA-02, BA-03, and BA-04 currently have **no test at all** that exercises them against an outcome record obtainable in production — the only production-obtainable outcome is the DEFERRED one, and neither DEFERRED test proceeds to preserve, expire, invalidate, or classify. This is a coverage illusion, not merely a coverage gap.

### 9.6 Probe: foreign-key enforcement (evidence for F-01)

**Hypothesis:** `evaluate()`'s UNRESOLVED branch writes `membership_id` referencing a nonexistent Membership into a `nullable=False` FK column (`models/access_evaluation_outcome.py:79-83`; migration `:61`), which must fail on any FK-enforcing database.

**Why the suite does not catch it:** `tests/conftest.py:11` uses `sqlite+aiosqlite:///:memory:` and `:19-36` registers no `PRAGMA foreign_keys=ON` listener. SQLite defaults to FK enforcement **off**.

**Probe executed** (read-only, scratchpad) — identical code path, run twice, differing only in the pragma:

```
PROBE 2 — FK enforcement on BA-01 UNRESOLVED branch
  foreign_keys=OFF -> WROTE outcome id=70df6971-... type=UNRESOLVED
                      membership_id=0bec3b50-... (orphan FK)
  foreign_keys=ON  -> RAISED IntegrityError: (sqlite3.IntegrityError)
                      FOREIGN KEY constraint failed
                      [SQL: INSERT INTO access_evaluation_outcomes (id, membership_id, ...
```

**Production consequence.** `CLAUDE.md §9` declares PostgreSQL the platform database; PostgreSQL enforces foreign keys unconditionally and non-deferrably for a non-`DEFERRABLE` constraint (which this is — migration `:61` declares no deferral). `evaluate()` contains no `try/except IntegrityError` — unlike `services/structural_completion_service.py:118-144`, which establishes exactly that defensive pattern in WP-04. The exception therefore propagates to `main.py:72-78`'s global handler and the caller receives:

```
HTTP 500 {"message": "An internal server error occurred."}
```

instead of the specified `201` + `UNRESOLVED`.

**Severity: High** under `§19.8.7` — the gap "defeats the governing capability's own stated Business Intent" for a whole class of requests (`EX-C002-03`'s missing-Membership case), and the subset is **undisclosed** rather than disclosed. **Non-deferrable** under `§19.8.5` (data integrity, broken functionality).

### 9.7 Test coverage verdict

Quality of the tests that exist: **good**. Breadth: **inadequate** — no event assertion, no audit assertion, no multi-organization case, no FK-enforced case, and eight named API-layer gaps. Two of the gaps (U-03, U-04) are not incidental: they are the exact blind spots that allowed both High-severity findings to reach a certified, committed state.

---

## 10. Database Review

### 10.1 Model ↔ migration parity

| Element | Model (`models/access_evaluation_outcome.py`) | Migration (`...f3a7c5e9b2d8...`) | Match |
|---|---|---|---|
| Table name | `access_evaluation_outcomes` (`:61`) | `'access_evaluation_outcomes'` (`:38`) | ✔ |
| `id` | `Mapped[uuid.UUID]`, PK, `default=uuid.uuid4` (`:77`) | `sa.Uuid()`, `nullable=False`, `PrimaryKeyConstraint` (`:39, :64`) | ✔ |
| `membership_id` | FK `memberships.id` CASCADE, `nullable=False`, indexed (`:79-83`) | `sa.Uuid()` NOT NULL, FK CASCADE, index (`:40, :61, :66`) | ✔ |
| `domain_id` | FK `domains.id`, `nullable=False`, indexed (`:85-89`) | `sa.Uuid()` NOT NULL, FK, index (`:41, :62, :67`) | ✔ |
| `permission_level` | `String(50)`, `nullable=False` (`:91`) | `sa.String(50)`, NOT NULL (`:42`) | ✔ |
| `outcome_type` | `String(20)`, `nullable=False` (`:94`) | `sa.String(20)`, NOT NULL (`:43`) | ✔ |
| `validity_status` | `String(20)`, `default`+`server_default='CREATED'` (`:97-101`) | `sa.String(20)`, NOT NULL, `server_default='CREATED'` (`:44`) | ✔ |
| `reason` | `Text`, `nullable=False` (`:103`) | `sa.Text()`, NOT NULL (`:45`) | ✔ |
| `approval_authority_id` | FK `approval_authorities.id`, nullable (`:106-109`) | `sa.Uuid()` nullable, FK (`:46, :63`) | ✔ |
| `created_at` | `DateTime(timezone=True)`, Python `default` (`:112-115`) | `sa.DateTime(timezone=True)`, NOT NULL, **no `server_default`** (`:47`) | ✔ (see 10.4) |
| `updated_at` | `DateTime(timezone=True)`, nullable, `onupdate` (`:117-121`) | `sa.DateTime(timezone=True)`, nullable (`:48`) | ✔ |
| CHECK `outcome_type` | `:63-66` | `:49-52` | ✔ **character-identical** |
| CHECK `validity_status` | `:67-70` | `:53-56` | ✔ **character-identical** |
| CHECK `permission_level` | `:71-74` | `:57-60` | ✔ **character-identical** |

**No model/migration drift.** The TD-004-class defect found at WP-01 is not repeated. This confirms `CERT-WP-05 §4.3`'s claim independently.

### 10.2 Indexes

`ix_access_evaluation_outcomes_membership_id` and `ix_access_evaluation_outcomes_domain_id` are created (migration `:66-67`) and declared on the model (`index=True` at `:82, :88`). `approval_authority_id` carries a foreign key but **no index** — PostgreSQL does not auto-index FK child columns, so a `DELETE`/`UPDATE` on `approval_authorities` performs a sequential scan of this table. Immaterial at current volumes. Recorded as F-19 (Low).

### 10.3 Foreign keys

All three targets (`memberships`, `domains`, `approval_authorities`) exist as of `down_revision = 'e6c1b3a9d7f2'` (WP-04's final migration) — verified via `alembic history`. No forward reference. `ON DELETE CASCADE` on `membership_id` is appropriate (the outcome is meaningless without its Membership); the other two have no delete rule, i.e. `NO ACTION` — meaning a `Domain` or `ApprovalAuthority` referenced by any outcome cannot be deleted. That is the correct conservative choice for a record whose Versioning Policy is "full history retained" (`IRA-005:261`). **PASS.**

### 10.4 Nullability and defaults

`created_at` is `NOT NULL` in the migration with **no `server_default`**, relying entirely on the ORM's Python-side `default`. Any non-ORM insert (a data-fix script, a bulk load, a psql statement) fails. This is the same pattern used by `models/membership.py:150-153` and `models/approval_authority.py:186-189`, so it is the repository's convention, not a WP-05 deviation. Recorded as an observation only.

### 10.5 Naming conventions

`ck_<table>_<column>` and `ix_<table>_<column>` throughout, matching `ck_approval_authorities_status`, `ck_memberships_membership_type`, etc. Table name is plural snake_case, matching every sibling. Revision file name follows the repository's `YYYY_MM_DD_HHMM-<rev>_<slug>.py` convention. **PASS.**

### 10.6 Upgrade / downgrade correctness

```python
def upgrade():            # :36-67
    op.create_table('access_evaluation_outcomes', ...10 columns, 3 CHECKs, 3 FKs, 1 PK)
    op.create_index('ix_..._membership_id', ...)
    op.create_index('ix_..._domain_id', ...)

def downgrade():          # :70-73
    op.drop_index('ix_..._domain_id', table_name='access_evaluation_outcomes')
    op.drop_index('ix_..._membership_id', table_name='access_evaluation_outcomes')
    op.drop_table('access_evaluation_outcomes')
```

`downgrade()` reverses `upgrade()` exactly and in correct reverse order (indexes before table). No other schema object is created by `upgrade()`, so nothing is left behind. `downgrade()` is idempotent-safe in the sense that it will fail loudly rather than silently on a partially-applied state. **PASS.**

**Not verified:** neither `upgrade()` nor `downgrade()` was executed against a live PostgreSQL instance — no PostgreSQL is available in this environment. `IMP-REPORT-WP-05:139` discloses this same limitation honestly. This audit therefore **cannot certify** that the migration applies cleanly to PostgreSQL; it certifies only that its declared DDL matches the model exactly and is syntactically well-formed Alembic. Recorded as F-20 (Low, informational).

### 10.7 Uniqueness

**No `UniqueConstraint` exists** on the model or in the migration (verified by `grep -n "UniqueConstraint"` on both files → no matches). Nothing prevents unbounded duplicate outcomes for the same `(membership_id, domain_id, permission_level)`. See F-04.

---

## 11. API Review

### 11.1 Endpoint inventory and OpenAPI generation

`app.openapi()` was invoked directly and succeeded without error. All five endpoints are present:

```
  /access-evaluations                            ['post']
  /access-evaluations/{outcome_id}/context-change ['post']
  /access-evaluations/{outcome_id}/expire         ['post']
  /access-evaluations/{outcome_id}/handoff-rejection ['post']
  /access-evaluations/{outcome_id}/preserve       ['post']
total /access-evaluations operations: 5
```

Router registration (`main.py:11, 104`) uses `prefix="/access-evaluations"`, `tags=["Access Evaluation"]` — consistent with all 18 sibling routers. **PASS.**

### 11.2 Status codes

| Code | Used at | Correct? | Consistent with WP-01–WP-04? |
|---|---|---|---|
| 201 | `POST /access-evaluations` (`routers:64`) | ✔ resource created | ✔ matches `POST /structural-completions`, `POST /memberships` |
| 200 | all four sub-resource actions (`routers:99, 121, 147, 176`) | ✔ state transition / computation, no new resource | ✔ |
| 400 | missing/malformed Authorization header (`dependencies.py:33-36`) | Unconventional (401 would be the RFC-correct code for a missing credential) but **repository-wide and consistent** | ✔ every prior WP behaves identically |
| 401 | invalid/expired token (`decode_access_token`) | ✔ | ✔ |
| 403 | non-PLATFORM_ADMIN (`dependencies.py:46-49`) | ✔ | ✔ |
| 404 | unknown Domain, unknown outcome (`services:98, 377`) | ✔ | ✔ |
| 409 | state-guard violations (`services:193, 227, 271`) | ✔ | ✔ matches `structural_completion_service.py:110` |
| 422 | Pydantic validation (`main.py:56-70`) | ✔ | ✔ |
| **501** | Permitted/Denied out of scope (`services:166`) | ✔ semantically exact — the server recognizes the request and does not support the functionality | **First and only use in this repository.** Verified: `grep -rn "501\|NOT_IMPLEMENTED" routers/ services/` matches nothing outside `access_evaluation` |

The 501 introduces a new convention. This audit finds it **correct and well-justified**: it is the only code that is neither a lie (200/201 with a fabricated outcome), nor a misattribution of fault to the caller (4xx), nor a concealment (500). Its `detail` names `IRA-005 S12` and `CLAUDE.md S19.8.5` explicitly, satisfying `IMP-API-004` better than any other WP-05 error message. Recommendation R-11 suggests recording it as an intentional repository convention.

### 11.3 Validation and error-response shape

Validation errors are shaped by the global handler at `main.py:56-70` → `{"detail": [...], "message": "Validation failed for request data."}`. `HTTPException` errors use FastAPI's default `{"detail": "..."}`. **These two shapes differ**, which is a pre-existing repository-wide inconsistency (every WP behaves this way), not a WP-05 defect. Recorded as an observation.

Every `HTTPException` detail names the specific entity and, for 409s, the current status — e.g. `"Access Evaluation Outcome '{id}' is not CREATED (current: 'PRESERVED'); only a newly-created outcome may be preserved."` This is genuinely explanatory. Only the 501 cites a principle ID (S-26).

### 11.4 OpenAPI documentation quality

Each route declares `summary`, a multi-sentence `description` citing the governing BA/ERB/EX and `IRA-005 §12`, and a `responses` map. `POST /access-evaluations` documents all seven of its status codes including 501 (`routers:73-81`). The two sub-resource BA-02 routes document 200/404/409 but **omit 400/401/403** from their `responses` maps (`routers:102-106, 124-128`), as do BA-03's and BA-04's (`:154-158, :179-182`) — even though those codes are reachable on all five endpoints. Minor OpenAPI incompleteness; recorded as F-21 (Low).

### 11.5 Idempotency

| Endpoint | Repeatable against the same target? | Guarded? | Disclosed? |
|---|---|---|---|
| `POST /access-evaluations` | **Yes — unbounded duplicates** | **No** — no uniqueness check, no unique constraint | **No** |
| `POST /{id}/preserve` | Yes | ✔ 409 on second call | Not in a BAC Idempotency field, but behaviourally correct |
| `POST /{id}/expire` | Yes | ✔ 409 | same |
| `POST /{id}/context-change` | Yes | ✔ 409 | same |
| `POST /{id}/handoff-rejection` | Yes | Naturally idempotent (read-only classification, no state change) | **No** |

`IMP-001 §6.7` makes the Idempotency disclosure **required** for exactly this situation. None of the four BACs contains it. **F-04.**

### 11.6 Consistency with WP-01 – WP-04 conventions

| Convention | WP-05 | Verdict |
|---|---|---|
| Router → dependency factories → service → repository | ✔ identical | PASS |
| `Annotated[..., Depends(require_platform_admin)]` on every write route | ✔ | PASS |
| Sub-resource action verbs (`/{id}/preserve`) | ✔ matches `/{id}/activate`, `/{id}/hand-off` etc. | PASS |
| `response_model` + `responses` map on every route | ✔ | PASS |
| Tenant-exemption entry with a written rationale comment | ✔ (`tenant.py:132-139`) | PASS — the rationale is the most carefully qualified of the 16 entries |
| **`actor_id=claims.get("person_id")` passed to the service** | **✘ — the only router of 16 that omits it** | **FAIL — F-03** |
| `GET /{id}` read endpoint | ✘ — absent | Disclosed as TD-080; matches TD-051/055/058/061/064 precedent. Accepted |
| `try/except IntegrityError` around create+flush | ✘ — absent | Contributes to F-01 |

---

## 12. Repository Consistency Review

Every WP-05-bearing document was cross-checked against the **actual repository state**, not against each other.

### 12.1 Test-count consistency

| Source | Claim | Actual | Consistent? |
|---|---|---|---|
| Actual execution | — | **601 total; 15 unit + 14 API = 29 WP-05** | (ground truth) |
| `IMP-REPORT-WP-05:115` | `test_access_evaluation_service.py` (15 tests) | 15 | ✔ |
| `IMP-REPORT-WP-05:116` | `test_access_evaluation_api.py` (**11 tests**) | **14** | **✘ F-07** |
| `IMP-REPORT-WP-05:128` | "29 new tests (15 unit, **14** API…)" | 29 / 14 | ✔ — **and contradicts line 116 in the same document** |
| `IMP-REPORT-WP-05:129` | "601 passed" | 601 | ✔ |
| `IMP-REPORT-WP-05:26` | BA-01: 5 unit + 7 API | 5 + 7 | ✔ |
| `IMP-REPORT-WP-05:43` | BA-02: 5 unit + **2** API | 5 + **3** | **✘ F-07** |
| `IMP-REPORT-WP-05:58` | BA-03: 2 unit + **1** API | 2 + **2** | **✘ F-07** |
| `IMP-REPORT-WP-05:75` | BA-04: 3 unit + **1** API | 3 + **2** | **✘ F-07** |
| `CERT-WP-05:19` | "**598/598** backend tests pass" | **601** | **✘ F-06** |
| `CERT-WP-05:57` | `test_access_evaluation_api.py` (**11 tests**) | **14** | **✘ F-06** |
| `CERT-WP-05:95` | "**598/598** tests pass" | **601** | **✘ F-06** |
| `CERT-WP-05:97` | "`test_access_evaluation_api.py` (**11 tests**) exercises only one branch of…" — the three named gaps | All three now closed | **✘ F-06** |
| `WP-REG-001:74` | "601/601 full AuthService suite passing" | 601 | ✔ |
| `WP-REG-001:92` | "29 new tests (15 unit + 14 API), 601/601" | ✔ | ✔ |
| `WPR-001:30` | "29 new tests … 601/601" | ✔ | ✔ |
| `TECH-DEBT:111` | "14/14 API tests pass, 601/601 full suite passes" | ✔ | ✔ |

**Analysis.** The three TD-081 remediation tests were added **inside commit `84b095b`**, i.e. before commit, but **after** `CERT-WP-05` was written. `CERT-WP-05` was then committed unchanged in `2ff1002`. The result is that the repository's certifying artifact describes a code state that does not exist in the same commit that contains it, and the three remediation tests were **never independently re-verified by any reviewer** — they were added by the implementing session in response to the review and self-attested. This is a §19.7 process gap, not merely a stale number. **F-06.**

### 12.2 Commit-state consistency

WP-05 **is** committed: `84b095b` (implementation) and `2ff1002` (governance). Yet:

| Document | Stale claim |
|---|---|
| `IMP-REPORT-WP-05:153` | "**Repository Commit: Not yet committed** — … all WP-05 implementation and documentation changes remain staged in the working tree" |
| `WP-REG-001:92` | Git-committed column: "**Not committed**" |
| `WP-REG-001:123` | "\| WP-05 \| 2026-07-30 \| 2026-07-30 (`CERT-WP-05`) \| **Not committed** \|" |
| `WP-REG-001:151-154` | All four lifecycle-history rows: "**Not committed**" |
| `CERT-WP-05:25` | "`git status` confirms only WP-05's own eight new source files … **are uncommitted**" |

Six statements across three documents assert an uncommitted state that is false at the audited commits. `WP-REG-001:151-154` are lifecycle-history rows (point-in-time records) and are defensible as historical; `WP-REG-001:92`, `:123` and `IMP-REPORT:153` are current-state assertions and are simply wrong. **F-07.**

Note the governance tension: these documents were committed *by* `2ff1002`, so a document asserting "not committed" was necessarily false the instant it was written to the repository. `CLAUDE.md §19.7` makes repository commit a completion-gate condition — a register that records "Not committed" against a Certified/Closed Work Package is internally contradictory about whether the gate is met.

### 12.3 `DOC-000` index consistency

| `DOC-000` line | Claim | Actual | Consistent? |
|---|---|---|---|
| `:252` | Certification Reports: "**CERT-WP-01, CERT-WP-01A, CERT-WP-02, CERT-WP-03, CERT-WP-04, CERT-WP-RTA-001** … **6 issued** … 2026-07-30 (latest: CERT-WP-RTA-001)" | **7 files on disk**; `CERT-WP-05_Access_Management.md` exists and is **absent from the list, the count, and the "latest" field** | **✘ F-05 — the certifying artifact for WP-05 is not indexed at all** |
| `:264` | Implementation Reports: "6 issued (4 Closed, 1 Certified-conditions-resolved, **1 Implementation Complete — Independent Review pending**)" | WP-05 is Certified/Closed; the "Review pending" slot is stale | **✘ F-05** |
| `:251` | IRA Reports: "7 Accepted", latest IRA-RTA-001 | 7 IRA files on disk (IRA-001, 001A, 002, 003, 004, 005, RTA-001) | ✔ |
| `:250` | ADR Index: "ADR-001 through ADR-016 … 16 Accepted" | 16 ADR files | ✔ |

Commit `2ff1002`'s own message states "DOC-000 Implementation Reports index count updated" — the Implementation Reports row was touched, but the **Certification Reports** row, which is the one that must record the new `CERT-WP-05`, was not. **F-05.**

### 12.4 TECH-DEBT register consistency

| Check | Result |
|---|---|
| TD-079 summary row (`:109`) vs Detailed Entry (`:948-961`) | ✔ consistent; Severity **Low** assigned per §19.8.7 |
| TD-080 summary row (`:110`) vs Detailed Entry (`:965-978`) | ✔ consistent; Severity **Low** assigned |
| **TD-081** summary row (`:111`) | **No Detailed Entry exists.** The register's own maintenance convention (every other WP-05-era entry has one) is broken, and **no §19.8.7 severity is assigned anywhere** — the table row carries "Low" in the Priority column, which §19.8.7 explicitly states is a *different* field from Severity ("Severity is independent of Priority … Neither field substitutes for the other") | **✘ F-10** |
| TD-081 status | `TECH-DEBT:111` = **Closed** | ✔ **Genuinely closed — independently verified** (Section 13.3) |
| TD-081 status per `CERT-WP-05:146` | "**Open**" | ✘ stale (F-06) |
| `CERT-WP-05:155` recommendation 2 | "At the next convenient touch … add the three missing branch-level API assertions" | ✘ already done (F-06) |
| Undocumented limitations | At least four: EX-C002-06's scope boundary (F-08); BA-03's non-detection (F-09); SUPERSEDED unreachable (F-11); no prior-state history (F-12); no persisted hand-off rejection (F-15) | **✘** |
| Undisclosed defects | F-01, F-02 — both §19.8.5-class and therefore not eligible for the register at all; they require remediation | **✘** |

### 12.5 `WP-REG-001` / `WPR-001` internal consistency

- `WP-REG-001:69` and `:169` both state "Certified | 6 (WP-01, WP-02, WP-03, WP-04, WP-05, WP-RTA-001)". `WPR-001:42`'s WP-RTA-001 entry both opens with "**CERTIFIED WITH CONDITIONS** … (`CERT-WP-RTA-001`, `ADR-016`)" and closes with "**Not yet independently reviewed or certified; not committed**". These contradict each other. **This is a WP-RTA-001 defect, outside this audit's scope**, but it does mean `WP-REG-001`'s "Certified: 6" figure rests on a contested premise. Recorded as an out-of-scope observation.
- `WP-REG-001 §10` (`:161-177`) is **no longer stale** — `CERT-WP-05 §4.7`'s "BA-01 implementation not yet begun" observation was correctly addressed. §10's arithmetic (40 completed / 42 planned = 95.2%) is internally consistent with §5's own rows. ✔
- `WPR-001:30` and `WP-REG-001:92` describe WP-05's scope, certification, and TD position consistently with `IRA-005 §12`, `CERT-WP-05`, and `TECH-DEBT`. ✔ (apart from the "Not committed" column).

### 12.6 Source-code ↔ documentation consistency

| Check | Result |
|---|---|
| `IMP-REPORT:109-114` file list vs `git show --stat 84b095b` | ✔ exact match (6 source + 2 test files + migration) |
| `IMP-REPORT:119-120` modified-file claims vs actual diff | ✔ exact — `main.py` +1 import entry +1 `include_router`; `tenant.py` +1 comment block +1 clause |
| `IMP-REPORT:24, 41, 56, 73` event names vs `services:128, 207, 241, 293, 351` | ✔ all five match verbatim |
| `IMP-REPORT:16-17` BA-01 input/output contract vs `schemas:15-50` | ✔ exact |
| `IMP-REPORT:130` "single Alembic head `f3a7c5e9b2d8`, chained onto `e6c1b3a9d7f2`" | ✔ independently re-verified |
| `IRA-005 §11` Lifecycle Model vs the two enums + two CHECK constraints | ✔ exact — all 4 Outcome Types, all 5 Validity Statuses |
| `TD-079:952` names all five endpoint functions | ✔ all five exist with exactly those names |
| `TD-080:969` "no `GET /access-evaluations/{id}` exists" | ✔ confirmed via OpenAPI (5 POST operations, 0 GET) |

**Source-to-documentation traceability is excellent.** The inconsistencies are confined to counts, status fields, and index entries — never to substantive claims about what the code does, with the exception of `CERT-WP-05 §4.6`'s audit-completeness claim, which is true as to *coverage* and silent as to *actor attribution* (F-03).

---

## 13. Technical Debt Review

### 13.1 Source-code scan for undisclosed compromise

```
grep -rn "TODO\|FIXME\|XXX\|HACK" <all 7 WP-05 source and test files>
  -> no matches
```

**No TODO/FIXME/XXX/HACK markers exist anywhere in WP-05.** Every acknowledged limitation is instead expressed in a prose docstring citing the governing document — a materially better practice. Examples: `models/access_evaluation_outcome.py:17-30` (why PERMITTED/DENIED are declared but unwritten), `:38` (why SUPERSEDED is unreachable), `services:12-20` (the module-level statement of the §19.8.5 reasoning), `services:213-217` (why no scheduler was built).

### 13.2 Are all real limitations documented?

| Limitation | In TECH-DEBT? | Assessment |
|---|---|---|
| PLATFORM_ADMIN-only gate | ✔ TD-079 | Accurate, non-overstated, correctly Low |
| No `GET` read endpoint | ✔ TD-080 | Accurate, correctly Low |
| API-layer branch coverage gap | ✔ TD-081 (Closed) | Genuinely closed — §13.3 |
| **No execution-scope / time bound; expiry is manual only** | **✘** | Disclosed only in `services:213-217`. `IRA-005:262` explicitly requires Object/Event/Time scoping. **F-08 (Medium)** |
| **BA-03 performs no actual detection** | **✘** | Disclosed only in `services:256-260`. **F-09 (Medium)** |
| **SUPERSEDED unreachable** | **✘** | Disclosed only in `models:38`. WP-04's equivalents (TD-052/057/062/065/069) each got a register entry; WP-05's did not. **F-11 (Low)** |
| **No prior-state history despite "full history retained"** | **✘** | **F-12 (Low)** |
| **Hand-off rejection never persisted** | **✘** | **F-15 (Low)** |
| **`CMD-001 §26.7` never updated** | **✘** | **F-13 (Low)** |
| **F-01 (orphan FK)** | **✘** | §19.8.5-class — **not eligible for the register**; requires remediation |
| **F-02 (cross-tenant AA)** | **✘** | §19.8.5-class — **not eligible for the register**; requires remediation |
| **F-03 (no actor in audit)** | **✘** | **F-03 (Medium)** |
| **F-04 (BAC incompleteness / undisclosed non-idempotency)** | **✘** | **F-04 (Medium)** |

**Verdict:** the three registered entries are accurate and honestly scoped. But **five to seven further real limitations are documented only in code comments**, which `CLAUDE.md §19.8.2` explicitly forbids: "Technical Debt SHALL NOT exist solely within Independent Review reports, implementation reports, commit messages, or chat history." A docstring is a closer cousin of those than of the register.

### 13.3 Verification that TD-081's "Closed" status is genuine

TD-081 (`TECH-DEBT:111`) names three specific remediation tests. Each was located and executed individually:

```
tests/test_access_evaluation_api.py::test_expire_rejects_outcome_that_was_never_preserved       PASSED
tests/test_access_evaluation_api.py::test_context_change_rejects_non_live_outcome               PASSED
tests/test_access_evaluation_api.py::test_handoff_rejection_classifies_invalidated_outcome_as_integrity_signal PASSED
```

All three exist at `test_access_evaluation_api.py:223-239`, `:269-292`, and `:322-349` respectively, each carrying a `"""TD-081: …"""` docstring, and all three pass. The API suite is 14/14 and the full suite 601/601, exactly as TD-081's Planned Resolution field claims.

**TD-081's Closed status is genuine and independently confirmed.** Two caveats: (a) the closure lacks a §19.8.7 severity assignment and a Detailed Entry (F-10); (b) the three tests were authored by the implementing session after certification and were never independently reviewed (F-06).

### 13.4 §19.8.7 severity-rubric compliance

TD-079 and TD-080 each carry an explicit `Severity:` field in their Detailed Entries, correctly reasoned against the rubric (both "no effect on correctness, security, or another capability's ability to depend on this one" → Low). TD-081 carries none. Applying the rubric independently to the undisclosed items:

- **F-01, F-02** → would be **High** ("defeats the governing capability's own stated Business Intent for a subset"; "weakens a security or tenant-isolation boundary") — but §19.8.5 makes both **ineligible** for the register: they must be remediated, not tracked.
- **F-03, F-04, F-08, F-09** → **Medium** ("internal completeness or robustness … expected to require resolution before the capability is exercised at production scale or by a downstream capability that depends on it").
- **F-11, F-12, F-13, F-15** → **Low**.

---

## 14. Findings (consolidated, ranked by severity)

### 14.1 High

---

**F-01 — BA-01's UNRESOLVED branch writes a referentially invalid foreign key; fails with HTTP 500 on PostgreSQL**

- **Category:** Data integrity / Broken functionality (`CLAUDE.md §19.8.5` — non-deferrable)
- **Severity:** **High** (§19.8.7: defeats the governing capability's stated Business Intent for an undisclosed subset)
- **Location:** `Backend/Services/AuthService/services/access_evaluation_service.py:103-119`; schema at `Backend/Services/AuthService/models/access_evaluation_outcome.py:79-83`; migration at `...f3a7c5e9b2d8...:40, :61`
- **Description:** When `membership_repo.get_by_id()` returns `None`, the service nonetheless persists an `AccessEvaluationOutcome` whose `membership_id` — a `nullable=False` FK to `memberships.id` — references a row that does not exist. `session.flush()` at `:119` issues the INSERT immediately.
- **Evidence:** Probe, Section 9.6. With `PRAGMA foreign_keys=OFF` (the test-harness default, `tests/conftest.py:11,19-36`) the row is written. With `foreign_keys=ON` the identical call raises `sqlite3.IntegrityError: FOREIGN KEY constraint failed`. PostgreSQL enforces unconditionally; the constraint is not declared `DEFERRABLE`.
- **Impact:** `POST /access-evaluations` with an unknown `membership_id` returns **HTTP 500** (via `main.py:72-78`) instead of the specified `201` + `UNRESOLVED`. Half of `EX-C002-03` is unimplemented in production. Additionally, **16 of 29 WP-05 tests** seed through this path (Section 9.5), so BA-02/BA-03/BA-04 have no production-viable test coverage.
- **Aggravating factor:** `services/structural_completion_service.py:118-144` already establishes the `try/except IntegrityError` + rollback + mapped-status pattern in this codebase. WP-05 neither applied it nor avoided the invalid write.
- **Why prior review missed it:** `CERT-WP-05` verified test execution but did not question whether the harness's database semantics match production.
- **Not disclosed** in `TECH-DEBT.md`, `IMP-REPORT-WP-05`, or `CERT-WP-05`.

---

**F-02 — Deferred-branch Approval Authority lookup crosses organization boundaries, disclosing one tenant's data into another's record**

- **Category:** Tenant isolation / Security (`CLAUDE.md §19.8.5` — non-deferrable)
- **Severity:** **High** (§19.8.7: weakens a tenant-isolation boundary, even if no exploit is currently known)
- **Location:** `Backend/Services/AuthService/repositories/access_evaluation_outcome_repository.py:17-33` (the query); consumed at `services/access_evaluation_service.py:133-157`
- **Description:** The query filters on `ApprovalAuthority.domain_id`, `.scope_type == "DOMAIN"`, and `.status == "ACTIVE"` only. `ApprovalAuthority.organization_id` is `nullable=False` (`models/approval_authority.py:103-108`) and `Domain.organization_id` is nullable — platform Domains are "visible to every tenant" (`models/domain.py:38-43`). Nothing constrains the selected authority to the Membership's own organization.
- **Evidence:** Probe, Section 8.6. A Membership in Tenant A was DEFERRED to Tenant B's `"TENANT-B CONFIDENTIAL APPROVAL BOARD"`, whose name and id were persisted into `reason`/`approval_authority_id` and returned in the API response.
- **Impact:** (1) cross-tenant information disclosure of an Approval Authority's name and identifier; (2) a materially wrong business determination — deferral to an authority with no jurisdiction; (3) nondeterministic selection, since `.first()` at `:33` has no `ORDER BY`.
- **Why prior review and tests missed it:** every test fixture places the Approval Authority in the same organization as the Membership (`test_..._service.py:111-118`, `test_..._api.py:60-67`). No multi-organization test exists anywhere in WP-05.
- **Contributing structural cause:** the query lives on `AccessEvaluationOutcomeRepository` rather than on the `ApprovalAuthority` aggregate's own repository (F-18), so it did not inherit that aggregate's organization-scoping conventions.
- **Not disclosed** anywhere.

### 14.2 Medium

---

**F-03 — Every WP-05 audit record attributes the action to `"SYSTEM"`; the actual actor is never recorded**

- **Category:** Security observability / Repository consistency
- **Severity:** Medium
- **Location:** `Backend/Services/AuthService/routers/access_evaluation.py:88, 114, 136, 166, 190`
- **Description:** All five handlers inject `claims: Annotated[dict, Depends(require_platform_admin)]` but never use it. The service's `actor_id` parameter defaults to `None`, and every `record_audit()` call resolves `actor_id or "SYSTEM"`.
- **Evidence:** Probe output, Section 8.8: `"actor_id": "SYSTEM"`. `observability.py:74-79` names "Who" as the first of SD-002-054's seven audit questions.
- **Repository deviation:** `grep -rn "actor_id=claims\.get" routers/` → **51 occurrences across 15 files**. `access_evaluation.py` is the only router of 16 that omits it. `structural_completion.py:69` is the direct comparator.
- **Impact:** 12 audit call sites × every request produce forensically unusable records. Not a control failure — authorization still works — but the audit trail cannot answer who acted.
- **Fix:** one argument per handler.

---

**F-04 — Business Activity Contracts omit 10 of `IMP-001 §6.7`'s 16 mandatory attributes, including the explicitly-required Idempotency disclosure; BA-01 is in fact non-idempotent**

- **Category:** Specification conformance / Architecture governance
- **Severity:** Medium
- **Location:** `architecture/05-Implementation/IMP-REPORT-WP-05_Access_Management.md:13-26, 32-43, 49-58, 64-75`; behaviour at `services/access_evaluation_service.py:66-173`
- **Description:** `IMP-001 §6.7` (lines 2049–2094) mandates 16 BAC attributes. All four WP-05 BACs supply approximately 6: Business Intent, Input Contract, Output Contract, Authorization, Events, Audit. **Absent from all four:** Activity Identifier, Business Domain, Business Object, Activity Type, Preconditions, Postconditions, Workflow, AI Assistance, Definition of Done, **Idempotency**.
- **Aggravating substance:** §6.7's Idempotency attribute is explicitly "**required** for any write endpoint callable twice against the same target." WP-05 has five such endpoints. `POST /access-evaluations` creates unbounded duplicate outcomes for the same `(membership_id, domain_id, permission_level)` — verified: no uniqueness logic in `evaluate()`, and `grep -n "UniqueConstraint"` over the model and migration returns nothing. This real non-idempotency is disclosed in no document.
- **Note on AI Assistance specifically:** `IRA-005:265` reproduces Contract 5.7's AI prohibitions verbatim (AI SHALL NOT grant, deny, override, invent, infer…). No BAC records an AI Assistance disposition, so there is no artifact stating that WP-05 implements no AI behaviour. It does not — verified by reading all source — but the absence is undocumented.

---

**F-05 — `DOC-000`'s Certification Reports index omits `CERT-WP-05` entirely**

- **Category:** Repository governance / Documentation
- **Severity:** Medium
- **Location:** `architecture/00-Governance/DOC-000_Documentation_Catalogue.md:252` (and `:264`)
- **Description:** Line 252 lists six certification reports and states "6 issued", with "latest: CERT-WP-RTA-001". `architecture/06-Reviews/` contains **seven** `CERT-*.md` files; `CERT-WP-05_Access_Management.md` appears in neither the list, the count, nor the latest-date field. Line 264's Implementation Reports status breakdown still carries "1 Implementation Complete — Independent Review pending", stale now that WP-05 is certified.
- **Evidence:** `ls architecture/06-Reviews/CERT-*.md | wc -l` → 7.
- **Why it matters:** commit `2ff1002`'s own message claims DOC-000 was updated. It was — but the Implementation Reports row, not the Certification Reports row. `DOC-000` is the repository's documentation catalogue; a certifying artifact absent from it is invisible to any consumer navigating by the catalogue.

---

**F-06 — `CERT-WP-05`'s evidence does not match the code committed alongside it, and its remediation tests were never independently verified**

- **Category:** Governance / Certification integrity
- **Severity:** Medium
- **Location:** `architecture/06-Reviews/CERT-WP-05_Access_Management.md:19, 25, 57, 95, 97, 146, 155`
- **Description:** `CERT-WP-05` certifies "**598/598**" tests (lines 19, 95) and an "**11 tests**" API suite (lines 57, 97). The commit that contains it (`2ff1002`) sits atop `84b095b`, which contains **601** tests and a **14-test** API suite. Line 146 lists TD-081 as **Open**; `TECH-DEBT:111` records it **Closed**. Line 155 recommends adding three tests that already exist. Line 25 asserts the change set is uncommitted.
- **Substantive consequence, beyond staleness:** the three TD-081 remediation tests were authored by the **implementing** session after certification, folded into the implementation commit, and never re-reviewed. `CLAUDE.md §19.7` requires that "the implementation agent SHALL NOT certify its own work" and that review observations be addressed *and re-accepted*. The remediation was self-attested. This audit independently verifies the three tests are correct and passing (Section 13.3) — closing the substance — but the process gap stands.

### 14.3 Low

---

**F-07 — `IMP-REPORT-WP-05` contradicts itself on test counts, and asserts an uncommitted state**

- **Severity:** Low
- **Location:** `IMP-REPORT-WP-05:116` ("11 tests") vs `:128` ("14 API") in the same document; `:43` ("2 API"), `:58` ("1 API"), `:75` ("1 API") vs actual 3/2/2; `:153` ("Not yet committed").
- **Related:** `WP-REG-001:92, :123` also carry "Not committed" as a current-state assertion (Section 12.2).

---

**F-08 — `EX-C002-06`'s scope boundary is not modelled at all, and the omission is in no Technical Debt entry**

- **Severity:** Medium-to-Low (recorded Low on impact today, Medium on governance)
- **Location:** `models/access_evaluation_outcome.py` (no scope column); `services/access_evaluation_service.py:210-217`
- **Description:** BA-02's own name is "Preserve and **Bound**"; `EX-C002-06` is "Expire … **at Scope Boundary**"; `IRA-005:262` states validity is "Object Scoped, Event Scoped, and Time Scoped to the single governed execution it was produced for." **No execution-scope identifier, no expiry timestamp, and no automatic expiry exist.** An outcome remains PRESERVED indefinitely until a caller explicitly expires it. Declining to build a scheduler is a correct §18 STOP (`services:213-217`), but the resulting gap belongs in the register.

---

**F-09 — BA-03 performs no detection: invalidation is driven entirely by an unvalidated caller-supplied string**

- **Severity:** Low (within authorized scope) / Medium (as an undisclosed conformance gap)
- **Location:** `services/access_evaluation_service.py:248-302`; `schemas/access_evaluation.py:82-85`
- **Description:** The Business Activity is "**Detect** and Resolve Access Context Change." `changed_fact` is validated only for length (1–500) and is never checked against Membership, Domain, or Approval Authority state. Any live outcome is invalidated on assertion alone. `BR-C002-01` (per `IRA-005:66`) governs "exclusive derivation from owning authorities." The docstring (`:256-260`) is honest; the register is silent.

---

**F-10 — TD-081 lacks a Detailed Entry and a §19.8.7 severity assignment**

- **Severity:** Low
- **Location:** `TECH-DEBT.md:111`
- **Description:** TD-079 (`:948-961`) and TD-080 (`:965-978`) each have a Detailed Entry with an explicit `Severity:` field. TD-081 has neither. Its table row carries "Low" in the **Priority** column; `CLAUDE.md §19.8.7` states plainly that "Severity is independent of Priority … Neither field substitutes for the other."

---

**F-11 — `SUPERSEDED` is permanently unreachable and undisclosed in the register**

- **Severity:** Low
- **Location:** `models/access_evaluation_outcome.py:37-43` (docstring at `:38`)
- **Description:** No code path writes `SUPERSEDED`. This is correct given the scope, and the docstring says so — but WP-04's five equivalent cases each received a register entry (TD-052/057/062/065/069). WP-05's did not.

---

**F-12 — "Full history retained for audit and traceability" is only partially met**

- **Severity:** Low
- **Location:** `services/access_evaluation_service.py:198, 232, 277-283`
- **Description:** `IRA-005:261` states the Versioning Policy is "Full history retained for audit and traceability." Transitions overwrite `validity_status` in place, and BA-03 additionally rewrites `reason` by concatenation. No prior-state row, version column, or transition table exists. The audit log is the only history, and it is anonymised by F-03.

---

**F-13 — `CMD-001 §26.7` Physical Implementation Mapping for `AEO-000001` was never updated**

- **Severity:** Low
- **Location:** `IRA-005:289`; `ADR-015` "Explicitly Not Decided"
- **Description:** Both documents record Physical Tables/APIs/Events as **Pending**. WP-05 has now supplied all three. No document was updated to record them, so `AEO-000001`'s registration still reads as having no physical realisation.

---

**F-14 — No test asserts that any Domain Event is published**

- **Severity:** Low
- **Location:** `services:127, 153, 207, 241, 292, 350`; both test files
- **Description:** Five event types are emitted; zero assertions exist. A regression removing every `publish_event` call would leave 601/601 green.

---

**F-15 — Hand-off rejections are never persisted**

- **Severity:** Low
- **Location:** `services/access_evaluation_service.py:308-361`
- **Description:** BA-04 mutates nothing and creates nothing. The rejection exists only as a log line. No governing document requires persistence, so this is an observation — but it means no queryable record of any dependent capability's rejection exists.

---

**F-16 — `PE-001-C002` could not be read directly; conformance rests on `IRA-005`'s quotations**

- **Severity:** Low (audit limitation, disclosed rather than concealed)
- **Location:** `docs/Product/PE-001/capabilities/C-002/PE-001-C002_Access_Management.docx`
- **Description:** The governing capability specification exists only as a binary `.docx`, unreadable as text in this environment. `IRA-005` quotes it extensively and appears scrupulous, but this audit **cannot independently verify** BR-C002-01…08, Contracts 5.1–5.7, or any EX Success Criteria against their source. Any conformance judgment in Sections 5 and 6 that depends on un-quoted PE-001-C002 text is therefore **unverified, not verified-positive**.

---

**F-17 — Empty request bodies are required on the wire for `preserve` and `expire`**

- **Severity:** Low
- **Location:** `schemas/access_evaluation.py:57-64`; `routers:110, 132`
- **Description:** Both schemas define zero fields, yet are declared as required body parameters, forcing every caller to send `{}`. No governing document requires a body for a pure state transition.

---

**F-18 — A foreign-aggregate query is placed on `AccessEvaluationOutcomeRepository`**

- **Severity:** Low (but the proximate structural cause of F-02)
- **Location:** `repositories/access_evaluation_outcome_repository.py:17-33`
- **Description:** `get_active_domain_approval_authority()` queries `ApprovalAuthority` from the outcome's own repository, while an `ApprovalAuthorityRepository` exists in the same service. Had the query lived on its own aggregate's repository, it would more plausibly have carried that aggregate's organization-scoping conventions.

---

**F-19 — `approval_authority_id` foreign key is not indexed**

- **Severity:** Low
- **Location:** migration `:46, :63`
- **Description:** PostgreSQL does not auto-index FK child columns; deletes/updates on `approval_authorities` will sequentially scan this table. Immaterial at current volumes.

---

**F-20 — The migration has never been executed against PostgreSQL**

- **Severity:** Low (informational)
- **Location:** `IMP-REPORT-WP-05:139` (honestly disclosed)
- **Description:** No PostgreSQL instance is available; `alembic upgrade`/`alembic check` were not run against the production engine by the implementer, the certifier, or this audit. DDL/model parity is verified statically; live application is not certified by anyone.

---

**F-21 — Four of five routes omit 400/401/403 from their OpenAPI `responses` maps**

- **Severity:** Low
- **Location:** `routers:102-106, 124-128, 154-158, 179-182`
- **Description:** All five endpoints can return 400/401/403 via the shared auth dependency; only `POST /access-evaluations` (`:73-81`) documents them.

### 14.4 Findings summary

| Severity | Count | IDs |
|---|---|---|
| **High** | **2** | F-01, F-02 |
| **Medium** | **4** | F-03, F-04, F-05, F-06 |
| **Low** | **15** | F-07 … F-21 |
| **Total** | **21** | |

**Blocking / FAIL-level:** F-01 and F-02 are each of a class `CLAUDE.md §19.8.5` explicitly prohibits deferring as Technical Debt (data integrity; tenant isolation). Under `CLAUDE.md §19.7`, such issues "SHALL be remediated before the Business Activity Completion Gate … is satisfied." **WP-05's completion gate is therefore not presently satisfied**, notwithstanding its recorded `CLOSED — CERTIFIED` status. Neither finding requires redesign or reimplementation.

### 14.5 Implementation Completeness — categorization of every requirement

Every requirement identified in Section 4, categorized.

| Category | Count | Requirements |
|---|---|---|
| **Implemented** | 22 | R-01, R-02, R-05, R-06, R-09, R-10, R-11, R-12, R-14, R-15, R-16, R-17, R-19, R-21, R-22, R-23, R-24, R-25, R-26, R-27, R-31, R-32 — of which **R-12, R-19, R-23, R-27** (all four event requirements) are implemented-but-untested (F-14) |
| **Partially Implemented** | 10 | **R-07** (missing-Membership sub-branch fails in production — F-01) · **R-08** (crosses organizations — F-02) · **R-03** (SUPERSEDED unreachable, undisclosed — F-11) · **R-04** (history retained only at row level — F-12) · **R-13** (audit present, actor absent — F-03) · **R-20** (invalidates but does not detect — F-09) · **R-28** (logged, never persisted — F-15) · **R-29** (6 of 16 BAC attributes — F-04) · **R-33** (3 registered, 5+ undocumented) · **R-34** (independent certification performed in form; evidence does not match the certified artifact — F-06) |
| **Missing / Not Satisfied** | 2 | **R-18** (expiry at scope boundary — no scope, no time bound, no scheduler — F-08) · **R-30** (tenant isolation preserved — F-02). *Additionally, S-13's `CMD-001 §26.7` Physical Implementation Mapping was never recorded — F-13* |
| **Deferred (properly disclosed)** | 3 | TD-079 (PLATFORM_ADMIN-only gate) · TD-080 (no `GET` endpoint) · TD-081 (API branch coverage — **Closed**, independently verified §13.3) |
| **Outside Scope (correctly absent)** | 3 | BA-01's PERMITTED branch · BA-01's DENIED branch · BA-03's re-resolution path — all three verified **absent**, per `IRA-005 §12` |
| **Unexpected Implementation** | 3 | Empty required request bodies for preserve/expire (F-17) · HTTP 501 as the out-of-scope signal (unprecedented in this repository, but **justified**) · `routed_to` as a human-readable label rather than an identifier (documented in-schema) |
| **Not verifiable by this audit** | 2 | `PE-001-C002`'s own BR/Contract/Success-Criteria text (binary `.docx` — F-16) · live PostgreSQL migration application (F-20) |

**Net position.** No authorized requirement is entirely absent except R-18. No unauthorized capability was built. The dominant failure mode is **partial implementation with undisclosed partiality** — nine requirements are less complete than the governance record states, and only three of those nine gaps appear in `TECH-DEBT.md`.

### 14.6 Quality Scoring

Scores are evidence-backed; every deduction cites a specific finding and a specific location.

| Dimension | Score | Basis and deductions |
|---|---|---|
| **Requirements Coverage** | **80 / 100** | All four authorized Business Activities present; both excluded branches verifiably absent; scope conformance exact (S-01 – S-07). **−8** R-07: `EX-C002-03`'s missing-Membership case unimplemented in production (F-01). **−6** R-18: `EX-C002-06`'s scope boundary entirely absent (F-08). **−4** R-20: BA-03 performs no detection (F-09). **−2** R-28/R-04/R-03: hand-off rejection unpersisted, no prior-state history, SUPERSEDED unreachable |
| **Architecture Compliance** | **86 / 100** | Layering, dependency direction, Repository/Service/Router patterns, transaction discipline, and `§19.5` Reuse→Create order all verified correct (§7.1–7.11); `§18` honoured, including a correct STOP on the scheduler (`services:213-217`). **−8** `IMP-001 §6.7`: 10 of 16 BAC attributes absent (F-04). **−4** F-18: foreign-aggregate query misplaced on `AccessEvaluationOutcomeRepository`. **−2** F-13: `CMD-001 §26.7` never updated |
| **Business Rule Compliance** | **76 / 100** | `BR-C002-02`'s closed set is honoured absolutely and the Permitted/Denied prohibition holds (§8.9, verified four ways) — the single most important rule. `BR-C002-05`'s "signal, not authority" discipline genuinely implemented (R-25). **−14** `BR-C002-01` (exclusive derivation from owning authorities) is not met twice: F-02 selects an authority outside the Membership's organization, and F-09 derives an invalidation from a client string rather than an authority. **−6** `IRA-005:262`'s Object/Event/Time scoping unimplemented (F-08). **−4** `IRA-005:261`'s "full history retained" only partially met (F-12) |
| **Security** | **58 / 100** | The headline requirement holds and was verified exhaustively, not assumed (§8.9); authentication, authorization gating on all five endpoints, injection resistance, and input bounding all verified (§8.1–8.5). **−25** F-02: cross-tenant information disclosure and jurisdictionally-wrong determination, empirically demonstrated (§8.6) — `CLAUDE.md §14`'s "tenant isolation is preserved" is not met. **−12** F-03: 100% of audit records anonymised to `"SYSTEM"`, defeating SD-002-054's first question. **−5** F-01's 500-on-500-class failure surface. Note: TD-079's PLATFORM_ADMIN-only gate is **not** deducted — it is correctly disclosed and repository-wide |
| **Testing** | **60 / 100** | 601/601 pass, independently re-executed; assertion quality is genuinely good — body-field assertions throughout, and both BA-04 tests deliberately prove independence from `stated_reason`. **−18** F-01's structural consequence: 16 of 29 tests seed via a production-impossible path, so BA-02/03/04 have no production-viable coverage (§9.5). **−10** U-03: no multi-organization test anywhere — the exact blind spot concealing F-02. **−6** U-01/U-02: zero event assertions and zero audit assertions across five event types and twelve audit sites. **−6** U-05 – U-12: eight named API-layer gaps (404s on three endpoints, auth codes on four, input boundaries) |
| **Documentation** | **72 / 100** | Traceability from code to governing document is exemplary — every file, class, and method cites `IRA-005 §12`, `ADR-015`, `AEO-000001`, and its governing EX; the tenant-exemption rationale (`tenant.py:132-139`) is the most carefully qualified of the sixteen. **−10** F-05: `CERT-WP-05` absent from `DOC-000`'s Certification Reports index entirely. **−8** F-06: certification evidence (598/11) contradicts the code committed with it (601/14). **−6** F-07: `IMP-REPORT` self-contradiction on test counts plus false "Not committed". **−4** F-04: no AI Assistance / Definition of Done / Idempotency disposition recorded anywhere |
| **Repository Governance** | **62 / 100** | The `§19.7` fresh-context reviewer requirement was honoured in form; `WP-REG-001`/`WPR-001`/`IRA-005 §12` are substantively consistent; `WP-REG-001 §10`'s previously-stale statistic was correctly fixed. **−20** the `§19.7` completion gate is not actually satisfied: two `§19.8.5`-class defects (F-01, F-02) exist undisclosed in a Work Package recorded `CLOSED — CERTIFIED`. **−8** F-06: the TD-081 remediation was self-attested by the implementing session post-certification and never re-reviewed. **−6** `§19.8.2` breach: five-plus real limitations documented only in docstrings (F-08, F-09, F-11, F-12, F-15). **−4** F-10: TD-081 has no Detailed Entry and no `§19.8.7` severity |
| **Maintainability** | **88 / 100** | Small, cohesive modules; one public method per Business Activity; constructor injection; no global state; strong typing throughout; zero TODO/FIXME/XXX markers; docstrings that explain *why* with document citations rather than restating *what*. **−6** F-18: misplaced foreign-aggregate query. **−4** F-03's root cause — an injected `claims` bound and unused in five handlers is dead weight that reads as an oversight. **−2** F-17: pointless required empty bodies |
| **Overall Implementation Quality** | **73 / 100** | Weighted across the above. The Work Package is well-engineered, honestly documented at the code level, and constitutionally correct on the point that mattered most. It is held back by two undisclosed `§19.8.5`-class defects that a single-tenant, FK-disabled test harness could not surface, and by a governance record that overstates the completeness of what was delivered |

---

## 15. Recommendations

### 15.1 Mandatory before WP-05's `CLOSED — CERTIFIED` status can stand

**R-01 — Remediate F-01 (orphan foreign key).** Three options, in `CLAUDE.md §19.5` order; the choice is a governance decision, not an implementation preference, because each changes a documented behaviour:
  - **(a) Preferred — do not persist a row for an unresolvable anchor.** Return `404` for an unknown `membership_id`, exactly as the Domain pre-check already does (`services:89-101`). Rationale: a governed request naming a nonexistent Membership is a malformed request, not a business outcome — the identical reasoning `services:71-76` already applies to Domain. Narrows `EX-C002-03` to the "Membership present but not confirmable" case, which must be disclosed.
  - **(b) Make `membership_id` nullable** and record the unresolvable identifier in `reason`. Requires a new migration and an `ADR`-level decision, since `AEO-000001`'s anchor would become optional.
  - **(c) Wrap create+flush in `try/except IntegrityError`** mirroring `structural_completion_service.py:118-144`, mapping to a defined status. Weakest option — it converts a 500 into a handled error but still leaves `EX-C002-03`'s missing-Membership case unimplemented.
  In all cases, **add a test that runs with foreign-key enforcement enabled** (a `PRAGMA foreign_keys=ON` connect listener on the test engine), and re-examine the 16 tests that seed via this path.

**R-02 — Remediate F-02 (cross-organization Approval Authority).** Add an organization constraint to `get_active_domain_approval_authority()`, scoping the lookup to the Membership's own `organization_id`, and add a deterministic `ORDER BY` to replace the bare `.first()`. Add a regression test seeding two organizations and asserting Tenant B's authority is never selected for Tenant A's Membership. Consider relocating the query to `ApprovalAuthorityRepository` (F-18).

**R-03 — Qualify WP-05's governance status until R-01 and R-02 land.** `WP-REG-001:92` and `WPR-001:30` currently read `CLOSED — CERTIFIED`. Because F-01 and F-02 are §19.8.5-class, that status is not presently supportable. Recommended interim state: **`CERTIFIED — REMEDIATION REQUIRED`**, citing this audit, reverting to `CLOSED — CERTIFIED` once both close. Do **not** record F-01/F-02 in `TECH-DEBT.md` — §19.8.5 makes them ineligible for deferral.

### 15.2 High-value, low-cost

**R-04 — Fix F-03.** Pass `actor_id=claims.get("person_id")` in all five handlers (`routers:88, 114, 136, 166, 190`), matching the 51 existing occurrences across 15 sibling routers. Add one test asserting a non-`"SYSTEM"` `actor_id` reaches `record_audit`.

**R-05 — Fix F-05.** Add `CERT-WP-05_Access_Management.md` to `DOC-000:252`'s Certification Reports list, update the count 6 → 7 and the "latest" field, and refresh `:264`'s Implementation Reports status breakdown.

**R-06 — Fix F-07 and the "Not committed" assertions.** Correct `IMP-REPORT-WP-05:116` (11 → 14) and the per-BA API counts at `:43, :58, :75`; update `:153`, `WP-REG-001:92` and `:123` to record `84b095b` / `2ff1002`.

**R-07 — Reconcile F-06.** Either append a dated addendum to `CERT-WP-05` recording the post-certification test additions and the corrected figures (601, 14), or supersede it. Note in `WP-REG-001`'s lifecycle history that the TD-081 remediation was self-attested, and that this audit independently confirmed the three tests exist and pass.

**R-08 — Fix F-10.** Add a TD-081 Detailed Entry with an explicit §19.8.7 `Severity:` field, matching TD-079/TD-080's format.

### 15.3 Technical Debt register hygiene

**R-09 — Register the undisclosed limitations** currently living only in docstrings, per `CLAUDE.md §19.8.2`: F-08 (no scope boundary / no automatic expiry — Medium), F-09 (BA-03 performs no detection — Medium), F-11 (SUPERSEDED unreachable — Low), F-12 (no prior-state history — Low), F-13 (`CMD-001 §26.7` unset — Low), F-15 (hand-off rejection not persisted — Low), F-19 (FK unindexed — Low), F-21 (OpenAPI responses incomplete — Low). Each with a §19.8.7 severity.

**R-10 — Strengthen TD-079** by citing `IMP-001 IMP-API-002` (line 11675) as the specific standard the `PLATFORM_ADMIN`-only gate deviates from. TD-079 is otherwise accurate.

### 15.4 Test-suite integrity

**R-11 — Enable foreign-key enforcement in `tests/conftest.py`** via a `PRAGMA foreign_keys=ON` connect listener on the test engine. This is a **repository-wide** change with repository-wide benefit: it is what would have caught F-01 automatically, and it aligns the harness with the production database's semantics. It may surface latent issues in other Work Packages and should therefore be undertaken as its own scoped change, not folded into WP-05's remediation.

**R-12 — Add the specific missing tests** named in Section 9.4: U-01 (event assertions), U-02 (audit `actor_id` assertion), U-03 (multi-organization), U-05 – U-08 (API-layer 404s and auth codes on the four sub-resource endpoints), U-11/U-12 (input boundaries), U-14 (BA-04 classification of an EXPIRED outcome).

### 15.5 Documentation and process

**R-13 — Complete the four Business Activity Contracts** against `IMP-001 §6.7`'s 16 attributes (F-04), prioritising **Idempotency** — and, in doing so, state explicitly that `POST /access-evaluations` is non-idempotent and creates duplicate outcomes, or add a uniqueness rule if that is the intended behaviour. Record an explicit "AI Assistance: none implemented" disposition against Contract 5.7.

**R-14 — Convert `PE-001-C002` to a text-readable form** (or publish a Markdown extract alongside the `.docx`) so that future audits can verify BR-C002-01…08 and Contracts 5.1–5.7 against the source rather than through `IRA-005`'s quotations (F-16). This applies to every `PE-001-Cxxx` and is a repository-level recommendation.

**R-15 — Adopt "verify the harness, not just the tests" as a certification step.** Both High findings were invisible to a review that read all the code and re-ran all the tests, because both are hidden by properties of the *test environment* (FK enforcement off) and the *test fixtures* (single organization). A short standing checklist — does the test database enforce what production enforces? does any test exercise a second tenant? does any test assert audit and event emission? — would have surfaced F-01, F-02, F-03, and F-14.

---

## 16. Certification Recommendation

### 16.1 Determination

# PASS WITH MINOR REMEDIATION

### 16.2 Basis for the determination

**Why not FAIL or FAIL — REIMPLEMENTATION REQUIRED.** Nothing in WP-05 requires redesign. The layering, repository and service patterns, dependency direction, transaction discipline, model/migration parity, reuse decisions, and scope conformance are all correct and independently verified (Sections 7, 10, 5.1, 5.4). No unauthorized architecture was introduced (S-18 – S-20). Critically, **the one requirement this Work Package could least afford to fail — that no caller may ever obtain a `PERMITTED` or `DENIED` outcome — holds absolutely**, verified four independent ways (Section 8.9): every creation site writes a literal `UNRESOLVED`/`DEFERRED`; no update path touches `outcome_type`; the only `DENIED` tokens in the service are `AuditStatus.DENIED`; and no API surface accepts an `outcome_type`. `CLAUDE.md §19.8.5`'s central prohibition is honoured, and the 501 decline (`services:166-173`) is a genuinely exemplary piece of engineering honesty. Both High findings are localized: F-02 is one `WHERE` clause and one `ORDER BY`; F-01 is a branch-handling decision plus, at most, one migration.

**Why not PASS or PASS WITH OBSERVATIONS.** `PASS WITH OBSERVATIONS` is what `CERT-WP-05` concluded, and that conclusion did not survive independent re-verification. Two defects exist that `CLAUDE.md §19.8.5` places on its explicit non-deferrable list:

- **F-01** is a data-integrity and broken-functionality defect. `POST /access-evaluations` with an unknown `membership_id` returns HTTP 500 on PostgreSQL — demonstrated, not theorised (Section 9.6) — where the specification requires 201 + UNRESOLVED. It further means 16 of 29 WP-05 tests exercise a path that cannot run in production, so BA-02, BA-03, and BA-04 currently have **no production-viable test coverage at all**.
- **F-02** is a tenant-isolation defect with cross-tenant information disclosure — demonstrated, not theorised (Section 8.6). `CLAUDE.md §14`'s "tenant isolation is preserved" criterion is not met.

`CLAUDE.md §19.7` states such issues "SHALL be remediated before the Business Activity Completion Gate … is satisfied." Neither was disclosed in `TECH-DEBT.md`, `IMP-REPORT-WP-05`, or `CERT-WP-05`. **WP-05's completion gate is therefore not currently satisfied**, and its recorded `CLOSED — CERTIFIED` status in `WP-REG-001:92` and `WPR-001:30` overstates the evidence.

**Why `PASS WITH MINOR REMEDIATION` is the proportionate call.** The Work Package is substantively sound and constitutionally correct; the defects are real, non-deferrable, and undisclosed, but each is a bounded code change with a clear fix. The correct response is targeted remediation and a status qualification — not rejection, and not acceptance as-is. The quality scoring in Section 14.6 (Overall Implementation Quality **73/100**, with Security **58** and Repository Governance **62** as the two dimensions carrying the material deductions, against Maintainability **88** and Architecture Compliance **86**) reflects exactly this shape: well-built, honestly commented, incompletely governed.

### 16.3 Conditions

| # | Condition | Finding | Blocking? |
|---|---|---|---|
| C-01 | Remediate the orphan-FK write in BA-01's UNRESOLVED branch; add an FK-enforced test | F-01 | **Yes** |
| C-02 | Scope the Approval Authority lookup to the Membership's organization; make selection deterministic; add a two-organization regression test | F-02 | **Yes** |
| C-03 | Qualify WP-05's status in `WP-REG-001` / `WPR-001` until C-01 and C-02 close | F-01, F-02 | **Yes** |
| C-04 | Pass the authenticated actor into all five service calls | F-03 | No — expected before the next Work Package |
| C-05 | Complete the four BACs against `IMP-001 §6.7`, especially Idempotency | F-04 | No |
| C-06 | Index `CERT-WP-05` in `DOC-000`; correct the stale counts and commit-state assertions | F-05, F-06, F-07 | No |
| C-07 | Register the seven-plus undisclosed limitations with §19.8.7 severities | F-08 – F-15, F-19, F-21 | No |

### 16.4 Statement of independence

This audit was performed with no prior involvement in WP-05's design, implementation, review, or certification. Every material claim in `IMP-REPORT-WP-05_Access_Management.md` and `CERT-WP-05_Access_Management.md` was treated as an unproven hypothesis and re-derived against actual source, actual test execution, actual database behaviour, and the actual governing documents. Two purpose-built read-only probes were used to test hypotheses the existing suite structurally cannot detect; both hypotheses were confirmed. No implementation, test, or governance document was modified, and nothing was committed.

Where this audit could not verify a claim — most importantly the `PE-001-C002` capability specification itself (F-16) and live PostgreSQL migration application (F-20) — that limitation is stated rather than papered over, and the affected conclusions are marked **unverified** rather than **verified-positive**.

---

*End of VV-AUDIT-WP-05.*
