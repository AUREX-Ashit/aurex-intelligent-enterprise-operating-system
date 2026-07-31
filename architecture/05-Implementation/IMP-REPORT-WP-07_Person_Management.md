# IMP-REPORT-WP-07 — Person Management (C-006)

**Work Package:** WP-07 — Person Management (C-006)
**Governing Readiness Assessment:** `IRA-007_WP-07_Person_Management_Implementation_Readiness_Assessment.md` (Accepted — READY, full scope: 10 Business Activities covering all 12 EXs, two EXs satisfied by construction).
**Governing Business Object:** None newly registered. `Person`/`Identity` (WP-00-era, pre-governance) reused unchanged. Four new audit/traceability tables (`PersonDistinctionDecision`, `PersonReconciliationDecision`, `PersonCorrection`, `PersonEnrichment`) fail `CMD-001 §26.3a`'s eligibility test — not registered canonical Business Objects (IRA-007 §5/§9).
**Governing Capability Specification:** `PE-001-C006_Person_Management.docx` v1.1 (`CRB-C006`; `ERB-C006-01` through `07`; `EX-C006-01` through `12`).
**Scope of this report:** BA-01 through BA-10 — all ten Business Activities authorized by `IRA-007 §12` at full scope.

---

## BA-01 — Recognize Incoming Person Reference (EX-C006-01, deterministic tier only)

### Business Activity Contract (IMP-001 §6.7)

- **Business Intent:** Determine, via deterministic recognition, whether an Authoritative Person already exists for an incoming reference.
- **Disposition:** **REUSE & CERTIFY**, no modification. Pre-existing implementation (`PersonRecognitionService`, committed `34cf7fe`, before `WP-00`) independently verified to conform to `PE-001-C006` v1.1's Recognition Authority Rule (§1.7) — see `IRA-007 §8` for the full conformance finding.
- **Input Contract:** `email` (EmailStr, required).
- **Output Contract:** `PersonRecognitionResponse` (`outcome`: `MATCHED`/`NO_CANDIDATE`, `person`: populated only on `MATCHED`).
- **Business Rules:** Deterministic lookup only, via `Identity.email` — a probabilistic tier is out of scope (`TD-095`).
- **Authorization Rules:** None — bootstrap-safe design (`URA-001-15`), pre-existing, unchanged.
- **Tests:** `test_recognize_deterministic_match`, `test_recognize_no_candidate`, `test_recognize_invalid_email_format`, `test_recognize_does_not_require_tenant_header` (pre-existing, re-verified).

## BA-02 — Establish New Person Context (EX-C006-02)

- **Disposition:** **REUSE & CERTIFY**, no modification. Re-runs recognition as a runtime precondition (not trusting the caller's own claim). Disclosed race condition inherited, formally registered as `TD-093`. Dangling `FC-IB-001` citation formally registered as `TD-094`.
- **Tests:** 5 pre-existing tests, re-verified.

## BA-03 — Understand Authoritative Person Context (EX-C006-03)

- **Business Intent:** A privacy-respecting, provenance-aware view of a Person's authoritative context, without exposing Identity's or Membership's own data.
- **Input Contract:** `person_id` (UUID path parameter).
- **Output Contract:** `PersonUnderstandingContext` (person fields + `has_identity`/`has_active_membership` boolean existence signals only).
- **Business Rules:** Read-only — no mutation. Also structurally satisfies `EX-C006-09` (Preserve Context) and, indirectly, `EX-C006-12` (Continue) — `IRA-007 §7.1`/`§7.2`.
- **Authorization Rules:** `PLATFORM_ADMIN` (`TD-092`).
- **Audit Requirements:** None — read-only, mirroring `OrganizationService.get_details()`'s own precedent.
- **Tests:** `test_understand_person_returns_full_context`, `test_understand_person_without_identity_or_membership`, `test_understand_person_rejects_unknown_id`, `test_understand_person_requires_authorization_header`, `test_understand_person_rejects_non_platform_admin`.

## BA-04 — Distinguish Candidate Person Matches (EX-C006-04)

- **Business Intent:** Resolve a Candidate Person Context (of any size, including exactly one) to exactly one Authoritative Person Context or an explicit new-Person decision, by governed human confirmation — never auto-selected.
- **Input Contract:** `candidate_person_ids` (list[UUID], min 1), `decision_type` (`SELECTED_EXISTING`/`NEW_PERSON`), `selected_person_id` (conditional), `rationale` (required).
- **Business Rules:** Every candidate must exist (404 otherwise). `SELECTED_EXISTING` requires `selected_person_id` to be one of the candidates (422 otherwise). Operates on a caller-supplied candidate set — `EX-C006-01`'s probabilistic tier does not feed this automatically (`TD-095`).
- **Persistence:** `PersonDistinctionDecision` (audit-trail table, not a registered Business Object).
- **Authorization Rules:** `PLATFORM_ADMIN` (`TD-092`).
- **Tests:** 7 tests covering both decision types, single- and multi-candidate sets, unknown-candidate rejection, invalid-selection rejection, and authorization.

## BA-05 — Resolve Conflicting Person Context (EX-C006-05)

- **Business Intent:** Classify a conflict between incoming and authoritative Person context as an ambiguity or a correction need, and route accordingly — never resolved through the same path.
- **Input Contract:** `person_id` (path), `conflicting_reference` (str), `classification` (`AMBIGUITY`/`CORRECTION_NEEDED`, human-made).
- **Output Contract:** Classification + `routed_to` (naming `EX-C006-04` or `EX-C006-07`).
- **Persistence:** None (`IRA-007 §5`) — `record_audit()` only.
- **Authorization Rules:** `PLATFORM_ADMIN` (`TD-092`).
- **Tests:** 5 tests covering both classifications, unknown-person rejection, authorization.

## BA-06 — Review Potential Duplicate Person Indication (EX-C006-06)

- **Business Intent:** A governed Reconciliation Decision for two Person contexts suspected of representing the same human — never a silent merge.
- **Input Contract:** `person_id_a`, `person_id_b`, `decision` (`CONFIRMED_DUPLICATE`/`CONFIRMED_DISTINCT`/`ESCALATED`), `rationale`.
- **Business Rules:** Both persons must exist (404). The two IDs must differ (422). Technical consolidation following a confirmed duplicate is explicitly out of scope — this service never merges records.
- **Persistence:** `PersonReconciliationDecision` (audit-trail table).
- **Authorization Rules:** `PLATFORM_ADMIN` (`TD-092`).
- **Tests:** 6 tests covering both terminal decisions, same-person rejection, unknown-person rejection, authorization.

## BA-07 — Correct Person Context (EX-C006-07)

- **Business Intent:** Correct an inaccurate authoritative fact while preserving the prior value permanently — never a silent overwrite.
- **Input Contract:** `person_id` (path), `field_name` (`first_name`/`last_name`/`display_name`), `corrected_value`, `reason`, `approval_reference` (optional).
- **Business Rules:** Prior value captured before mutation; `Person` row updated in place; `PersonCorrection` row preserves the prior value permanently.
- **Persistence:** `PersonCorrection` (audit-trail table).
- **Authorization Rules:** `PLATFORM_ADMIN` (`TD-092`).
- **Tests:** 4 tests, including explicit prior-value-preservation assertion.

## BA-08 — Enrich Person Context (EX-C006-08)

- **Business Intent:** Add legitimate new detail to a Person's authoritative context — additive only, sourced, sensitivity-classified.
- **Input Contract:** `person_id` (path), `attribute_name`, `attribute_value`, `source` (required provenance), `sensitivity_classification` (`PUBLIC`/`INTERNAL`/`CONFIDENTIAL`/`RESTRICTED`, reusing `CMD-001 §26.4`'s own vocabulary).
- **Persistence:** `PersonEnrichment` (audit-trail table). `Person`'s own fixed schema is never mutated by enrichment.
- **Authorization Rules:** `PLATFORM_ADMIN` (`TD-092`).
- **Tests:** 4 tests.

## BA-09 — Hand Off Person Context to Identity Establishment (EX-C006-10)

- **Business Intent:** Transfer bounded Person context to Identity Management and record the outcome — C-006 never calls C-001's own API (unchartered).
- **Input Contract:** `person_id` (path), `outcome` (`ACCEPTED`/`RETURNED`), `reason` (required if `RETURNED`, 422 otherwise).
- **Business Rules:** The underlying `Person` row is never mutated by either outcome (`BR-C006-010`).
- **Persistence:** None (`IRA-007 §5`) — `record_audit()`/`publish_event()` only, mirroring `WP-02 BA-10`'s own hand-off precedent.
- **Authorization Rules:** `PLATFORM_ADMIN` (`TD-092`).
- **Tests:** 6 tests.

## BA-10 — Hand Off Person Context to Membership Establishment (EX-C006-11)

- Identical shape to BA-09, targeting `C-007`. 5 tests.

---

## EX-C006-09 / EX-C006-12 — Satisfied by Construction (No Dedicated BA)

Per `IRA-007 §7.1`/`§7.2`: neither EX produces a distinct resource of its own for a dedicated endpoint to expose — `BA-03`'s `GET /person/{id}` and every other BA's own already-returned response together satisfy both EXs' stated Business Value. Disclosed explicitly, not silently folded in, mirroring `WP-04`'s own precedent for Comparison Context and Downstream Continuation Context.

---

## Governing Architecture Review (Step 1)

Reviewed: `CLAUDE.md` (§14, §16, §17, §18, §19.1–§19.8), `METH-002`, `ADR-017`, `IMP-001` (§6 CBAIP), `CMD-001 §26.3a`, `PE-001-C006` v1.1 in full (Chapters 1–9, read directly from `word/document.xml`), `URA-001` (§2, clauses 13/15/16/17a/17b/28 — independently confirmed against the actual document text, not assumed), `WPR-001`/`WP-REG-001` (WP-07 chartered row), `IRA-007` (full), the existing AuthService repository structure.

**Key finding:** two EXs (`EX-C006-01`/`02`) already had real, tested implementation predating this repository's entire governance discipline (committed `34cf7fe`, one day before `WP-00`) — never through an IRA, Certification, or V&V. Independent review (`IRA-007 §8`) determined this code **conforms** to `PE-001-C006` v1.1, not the pre-1.1 draft's disclosed confidence-based contradiction, and certified it for reuse rather than modifying or replacing it.

---

## Gap Analysis Summary (see IRA-007 §4–§10 for full detail)

- **Database:** Four new tables (`person_distinction_decisions`, `person_reconciliation_decisions`, `person_corrections`, `person_enrichments`), none a registered canonical Business Object. FKs to `persons.id`, already existing as of this migration's own `down_revision` (`f3a7c5e9b2d8`, WP-05's last migration). Single new migration (`05f620c521e9`), confirmed a single Alembic head.
- **Business Activities:** BA-01 through BA-10 are the ten Business Activities `IRA-007 §3`/`§12` authorized, at full scope — no minimum-scope narrowing (unlike WP-05), since no external blocker exists.
- **API Impact:** Eight new endpoints under the existing `/person` prefix, two endpoints (`/recognize`, `/establish`) reused unchanged.
- **UI Impact:** Out of scope (backend Business Activity implementation only, matching every prior WP's own precedent).
- **Dependencies:** `Person`/`Identity` (pre-`WP-00`, reused unchanged, no schema modification). `Membership` (WP-03, closed) reused read-only for BA-03's existence signal, no modification.
- **Explicitly out of scope:** `EX-C006-01`'s probabilistic tier (`TD-095`); Identity, Membership, Access, Role/Permission, Structure, and Workspace's own internal semantics (`PE-001-C006 §1.4`).
- **Technical Debt raised:** `TD-092` (PLATFORM_ADMIN-only gate, BA-03–10), `TD-093` (disclosed pre-existing race condition in `establish()`), `TD-094` (dangling `FC-IB-001` citation), `TD-095` (probabilistic tier / BA-04 candidate-generation dependency).

---

## Documents Updated

**Architecture:**
- `architecture/05-Implementation/IRA-007_WP-07_Person_Management_Implementation_Readiness_Assessment.md` (new)
- `architecture/05-Implementation/IMP-REPORT-WP-07_Person_Management.md` (this report)
- `architecture/06-Reviews/TECH-DEBT.md` (`TD-092` through `TD-095` added, with Detailed Entries)

**Implementation (new):**
- `Backend/Services/AuthService/models/person_distinction_decision.py`
- `Backend/Services/AuthService/models/person_reconciliation_decision.py`
- `Backend/Services/AuthService/models/person_correction.py`
- `Backend/Services/AuthService/models/person_enrichment.py`
- `Backend/Services/AuthService/repositories/person_distinction_decision_repository.py`
- `Backend/Services/AuthService/repositories/person_reconciliation_decision_repository.py`
- `Backend/Services/AuthService/repositories/person_correction_repository.py`
- `Backend/Services/AuthService/repositories/person_enrichment_repository.py`
- `Backend/Services/AuthService/services/person_understanding_service.py`
- `Backend/Services/AuthService/services/person_distinction_service.py`
- `Backend/Services/AuthService/services/person_conflict_service.py`
- `Backend/Services/AuthService/services/person_reconciliation_service.py`
- `Backend/Services/AuthService/services/person_correction_service.py`
- `Backend/Services/AuthService/services/person_enrichment_service.py`
- `Backend/Services/AuthService/services/person_handoff_service.py`
- `Backend/Services/AuthService/alembic/versions/2026_08_10_0900-05f620c521e9_person_management.py`

**Implementation (modified):**
- `Backend/Services/AuthService/models/__init__.py` — registered the four new models.
- `Backend/Services/AuthService/schemas/person.py` — added request/response schemas for BA-03 through BA-10.
- `Backend/Services/AuthService/routers/person.py` — added eight new endpoints, all gated by `require_platform_admin` except the two pre-existing, unmodified `/recognize`/`/establish` endpoints.
- `Backend/Services/AuthService/middleware/tenant.py` — exemption widened from an exact two-entry list (`/person/recognize`, `/person/establish`) to a full `/person`/`/person/*` prefix match, on the stronger basis that `Person` has no `organization_id` column anywhere in its own model or any of the four new tables (`URA-001-15`).
- `Backend/Services/AuthService/tests/test_person.py` — 42 new tests (51 total in the file).

No other existing model, repository, service, or router was modified. `BA-01`/`BA-02`'s own pre-existing code (`services/person_recognition_service.py`, `services/establish_person_context_service.py`, `repositories/identity_repository.py`, `repositories/person_repository.py`, `routers/person.py`'s original two endpoints) is byte-for-byte unchanged — certified, not touched.

---

## Validation

- 42 new tests (all in `tests/test_person.py`, alongside the 9 pre-existing), 51/51 passing in the file.
- Full AuthService suite: **664 passed**, zero regressions (`pytest tests/ -q`, re-run directly) — up from 622 at WP-06's own closure (622 + 42 = 664, exact).
- Confirmed a single Alembic head (`05f620c521e9`) after the new migration, chained onto `f3a7c5e9b2d8`.
- Confirmed BA-01/BA-02's own pre-existing tests (9) still pass unmodified — certification, not silent regression risk.
- Confirmed every new endpoint's authorization (400/401/403), 404-on-unknown, and 422-on-invalid-input paths.
- Confirmed BA-07's prior-value preservation directly (`test_correct_person_updates_field_and_preserves_prior_value`).
- Confirmed BA-09/10 never mutate the underlying `Person` row on either outcome (implicit in the service's own read-only-on-`Person` code path, no write call exists in `PersonHandoffService`).
- Live Postgres `alembic upgrade`/`alembic check` was not exercised — no running Postgres instance is available in this environment, the same limitation every prior WP's own validation carried.

---

## Status (BA-01 through BA-10)

**Implementation:** COMPLETE

**Developer Validation:** Complete (664/664 full suite passing, re-run directly during this report's own preparation)

**Independent Review:** Pending — to be performed by a fresh-context subagent per `CLAUDE.md §19.7`/`ADR-014` (self-certification prohibited).

**Verification & Validation Audit:** Pending — mandatory for every Work Package per `CLAUDE.md §19.7b`.

**Remediation:** Not yet applicable — pending V&V Audit outcome.

**Release Readiness Audit:** Pending.

**Certification status:** NOT YET CERTIFIED. `WP-REG-001`/`WPR-001` to be updated to "Implementation Complete — Pending Independent Review" as the next repository-synchronization step.

**Repository Commit:** Not yet committed — git commits are only made on the repository owner's explicit instruction; all WP-07 implementation and documentation changes remain staged in the working tree, ready to commit on request.
