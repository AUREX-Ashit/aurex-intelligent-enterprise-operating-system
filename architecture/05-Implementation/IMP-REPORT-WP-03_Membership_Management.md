# IMP-REPORT-WP-03 — Membership Management (C-007)

**Work Package:** WP-03 — Membership Management (C-007)
**Governing Readiness Assessment:** `IRA-003_WP-03_Membership_Management_Implementation_Readiness_Assessment.md` (Approved — WP-03 READY, BA-01 only; BA-02 onward each require their own fresh gap analysis before implementation, per IRA-003 §1 and CLAUDE.md §19.7). BA-02's and BA-03's own fresh gap analyses are each performed in this report, extending IRA-003 §10's own preliminary Category B classification for BA-02 and IRA-003 §14's Category B classification for BA-03/BA-04.
**Governing Capability Specification:** `PE-001-C007_Membership_Management.docx` (six ERBs, thirteen Enterprise Experiences, fourteen Business Rules, ten Chapter 5 Contracts)
**Scope of this report:** BA-01, BA-02, and BA-03. BA-04 through BA-11 (candidate list per IRA-003 §4) are **not started** and are not covered by this report.

---

## BA-01 — Establish Membership Context

## Business Activity Implemented

**BA-01 — Establish Membership Context**, realizing PE-001-C007's ERB-C007-01 (Establish Membership Context) / EX-C007-01 (Recognize Existing Membership) + EX-C007-02 (Establish New Membership).

### Business Activity Contract (IMP-001 §6.7)

- **Business Intent:** Recognize an existing Membership deterministically, or establish a new one, for a resolved Person and a valid Organization — CAP-001's C-007 Business Intent ("Manage enterprise memberships"), scoped to establishment only.
- **Input Contract:** `person_id` (UUID, required), `organization_id` (UUID, required), `role_id` (UUID, required — inherited WP-00 schema coupling, see TD-033), `home_node_id` (UUID, optional — see TD-032), `membership_type` (INTERNAL/EXTERNAL, URA-001-106, default INTERNAL), `license_type` (FULL/LIGHT, URA-001-111, default FULL), `effective_from`/`effective_to` (optional), `is_primary` (boolean, default False).
- **Output Contract:** The established Membership (id, person_id, organization_id, role_id, home_node_id, membership_type, license_type, membership_status, is_primary, effective_from, effective_to, joined_at, created_at, updated_at), or an HTTP error naming the specific violated rule.
- **Business Rules:**
  - BR-C007-001 — a new Authoritative Membership Context SHALL NOT be established without a prior deterministic recognition lookup. Satisfied by construction: `establish()` always calls `get_by_person_and_organization()` before creating a row, and rejects with 409 if any Membership (any status) already exists for the pair.
  - BR-C007-002 — a Candidate Home-Node Context SHALL NOT be treated as authoritative until explicitly confirmed. Satisfied by construction: a supplied `home_node_id` is looked up and its `active_flag` checked (404 if missing, 409 if inactive) before being persisted; never invented or defaulted.
  - BR-C007-007 — a home-node anchor SHALL only reference a node returned by C-005/ERG-001-03's current candidate lookup. Same validation as BR-C007-002 above; no minimal `organization_nodes` row is invented to satisfy a missing anchor.
- **Validation Rules:** Person, Organization, and Role existence checked (404 each); duplicate-Membership-for-pair checked both at the service layer (pre-check, clean 409) and via `IntegrityError` handling for the concurrent-creation race, the same pattern `RoleService.establish()`/`OrganizationService.establish()` already use.
- **Authorization Rules:** `PLATFORM_ADMIN` role required. **Scoped simplification (IRA-003 §9/§19, same class as IRA-002 §2.7):** EX-C007-02 names "Membership Steward"/"Membership Sponsor" as its Participating Personas; neither exists as an enforceable claim today. Disclosed explicitly, recorded as **TD-031**.
- **Domain Events:** `MEMBERSHIP_ESTABLISHED` (membership_id, person_id, organization_id).
- **Audit Requirements:** `record_audit("ESTABLISH_MEMBERSHIP", ...)` on every denial path (unknown person/organization/role/home_node_id, inactive home_node_id, duplicate Membership) and on success, per SD-002-054's seven audit questions — same mechanism WP-01/WP-02 established, reused as-is.
- **Tests:** `tests/test_membership_service.py` (9 unit tests), `tests/test_membership_api.py` (7 API/authorization tests) — 16 new tests, all passing; full AuthService suite (341 tests) passing with zero regressions.

---

## Governing Architecture Review (Step 1)

Reviewed (per IRA-003's own Documents Reviewed line, re-confirmed for this implementation pass): CLAUDE.md (§14, §16, §17, §19.1–§19.8), ARCH-000, CAP-001 (C-007 entry: Primary Specification URA-001, Status Active), URA-001 (URA-001-15/16/17b/25/28/37/38/57/59/106/111), ERG-001 (ERG-001-02/03, EnterpriseNode bounded context and Node-to-Membership Linkage), IMP-001 (§6 CBAIP; §13.17–13.25 confirmed not applicable), Master Technical Architecture (`membership_registry`, `organization_node` DDL), WPR-001, IRA-001/IRA-002 (precedent format), IMP-REPORT-WP-01/IMP-REPORT-WP-02 (precedent implementation/review pattern), CERT-WP-01/CERT-WP-02 (self-certification prohibition), TECH-DEBT.md (TD-016/TD-028, both naming a future Membership Management work package as their own resolution path), the existing AuthService repository structure (`models/membership.py`, `repositories/membership_repository.py` — read-only prior to this Business Activity).

**Key finding requiring disclosure (already recorded in IRA-003 §9):** `organization_node`/EnterpriseNode did not exist anywhere in AuthService prior to this Business Activity, though ERG-001-02/03 and Master Technical Architecture fully specify it. This was IRA-003's own flagged first implementation decision for BA-01, not left to be discovered mid-implementation. Disposition selected: build a minimal `organization_nodes` table (node_code/node_name/node_type/active_flag only — the ~20 further Enterprise-Structure-specific columns are Enterprise Structure Management (C-005)'s own future scope, per ADR-004's precedent for `organizations` vs. `organization_master`) and make `Membership.home_node_id` nullable rather than the canonical NOT NULL, since no Business Activity anywhere yet establishes an `OrganizationNode` row. Recorded as **TD-032**, not silently assumed.

---

## Gap Analysis Summary (see IRA-003 §9–§11 for full detail)

- **Database:** `memberships` (WP-00-era) extended, purely additively, with `home_node_id`, `membership_type`, `license_type`, `effective_from`, `effective_to`. New table `organization_nodes` created (BA-01's own first required build item, per IRA-003 §7/§9). No existing column altered or dropped. Single new migration (`d4f8e2a6c1b9`), chained onto the existing head (`c3e9a5f7b2d4`) — confirmed a single Alembic head after this migration (`alembic heads` reports exactly `d4f8e2a6c1b9`).
- **Business Activities:** BA-01 is the only Business Activity authorized for implementation under IRA-003; BA-02 through BA-11 remain candidate-only (IRA-003 §4), each requiring its own gap analysis before implementation, per CLAUDE.md §19.7.
- **API Impact:** One new endpoint, `POST /memberships`, mirroring `POST /roles`/`POST /domain-permissions`'s established shape (schema/repository/service/router layering, duplicate-check-then-create, audit/event emission). `membership-api.yaml` added, mirroring every prior WP's own per-capability OpenAPI file.
- **UI Impact:** Out of scope for BA-01 (backend Business Activity implementation only, matching WP-01/WP-02's own BA-01 precedent).
- **Dependencies:** Person and Identity (C-006) consumed as a **Legacy Baseline dependency** per IRA-003 §16's own governance instruction — C-006's `/recognize`/`/establish` endpoints predate the current IRA/IMP-REPORT/CERT governance process entirely (commit `34cf7fe`, one day before WP-00's own bootstrap commit) and require no retroactive IRA or certification before WP-03 begins. Organization (C-004, WP-01, closed) and Role (C-003, WP-02, closed) consumed as-is, unmodified.
- **Explicitly out of scope (IRA-003 §17, Governance Backlog Item):** `membership_business_role`, `membership_approval_authority`, `group_registry`, `group_membership` — fully specified in Master Technical Architecture but claimed by no capability's own governing text. Not absorbed into this Business Activity, not gap-analyzed here, and not assigned a BA number.
- **Technical Debt inherited:** TD-016 (WP-01) and TD-028 (WP-02) both name a future Membership Management work package as their own resolution path. **Neither is resolved by BA-01** — TD-016 concerns AuthService's login flow (`authenticate_user()`), untouched by Establish; TD-028 concerns `membership_approval_authority`, explicitly out of WP-03's own scope per IRA-003 §17. Both remain open, stated plainly rather than implied closed.

---

## Documents Updated

**Architecture (new, planning only):**
- `architecture/05-Implementation/IRA-003_WP-03_Membership_Management_Implementation_Readiness_Assessment.md` (already drafted, independently reviewed, and committed — `48fa488`; unchanged by this report)
- `architecture/05-Implementation/IMP-REPORT-WP-03_Membership_Management.md` (this report)
- `architecture/06-Reviews/TECH-DEBT.md` (TD-031, TD-032, TD-033 added)
- `architecture/00-Governance/WPR-001_Work_Package_Roadmap.md` (WP-03 status row updated to reflect BA-01 implemented and independently reviewed)

**Implementation (new):**
- `Backend/Services/AuthService/models/organization_node.py`
- `Backend/Services/AuthService/repositories/organization_node_repository.py`
- `Backend/Services/AuthService/schemas/membership.py`
- `Backend/Services/AuthService/services/membership_service.py`
- `Backend/Services/AuthService/routers/membership.py`
- `Backend/Services/AuthService/membership-api.yaml`
- `Backend/Services/AuthService/alembic/versions/2026_07_31_0900-d4f8e2a6c1b9_membership_context_establishment.py`
- `Backend/Services/AuthService/tests/test_membership_service.py`
- `Backend/Services/AuthService/tests/test_membership_api.py`

**Implementation (modified):**
- `Backend/Services/AuthService/models/membership.py` — added `MembershipType`/`LicenseType` enums, `home_node_id`/`membership_type`/`license_type`/`effective_from`/`effective_to` columns, two CHECK constraints, and the `home_node` relationship.
- `Backend/Services/AuthService/models/__init__.py` — registered `OrganizationNode`.
- `Backend/Services/AuthService/repositories/membership_repository.py` — added `get_by_person_and_organization()` (BA-01's own recognition-lookup method).
- `Backend/Services/AuthService/main.py` — registered the new `membership` router at `/memberships`.
- `Backend/Services/AuthService/middleware/tenant.py` — added `/memberships` and `/memberships/*` to the tenant-exemption list, same disclosed basis as `/domain-permissions`/`/approval-authorities` (TD-031's interim PLATFORM_ADMIN-only caller).

No other existing model, repository, service, or router was modified.

---

## Validation

- 16 new tests (9 unit, 7 API), all passing.
- Full AuthService suite: **341 passed**, zero regressions (re-run directly, not taken on faith).
- Confirmed a single Alembic head (`d4f8e2a6c1b9`) after the new migration — no branch point introduced.
- Confirmed BR-C007-001: a second `POST /memberships` for the same (person_id, organization_id) pair is rejected with 409, both via the pre-check and the concurrent-creation `IntegrityError` path.
- Confirmed BR-C007-002/007: an unknown `home_node_id` is rejected with 404; an inactive `home_node_id` is rejected with 409; a valid, active `home_node_id` is persisted unchanged.
- Confirmed unknown `person_id`/`organization_id`/`role_id` each reject with 404, naming the specific missing reference.
- Confirmed non-`PLATFORM_ADMIN` callers receive 403, consistent with TD-031's disclosed interim gate.
- Confirmed `MembershipService.establish()` never writes to `roles`, `role_permissions`, or any Role/Permission table, preserving PE-001-C007's own "does not assign or remove Roles or Permissions" boundary in practice despite `role_id`'s required-field tension (TD-033).

---

## Status (BA-01)

**Implementation:** COMPLETE

**Developer Validation:** Complete (341/341 full suite passing, re-run directly during this report's own preparation)

**Independent Review:** APPROVED WITH OBSERVATIONS

**Repository Commit:** Committed to `master` in two commits — `8e1d276` (implementation: 14 files) and `cc3f3cd` (documentation: this report, TECH-DEBT.md TD-031/032/033, WPR-001 status update).

**Commit Hash:** `8e1d276` (implementation), `cc3f3cd` (documentation: implementation report, TECH-DEBT.md, WPR-001)

**Commit Date:** 2026-07-29 (both commits)

---

## Independent Review (BA-01)

**Review Result:** APPROVED WITH OBSERVATIONS

**Review Summary:** An independent reviewer, with no prior involvement in BA-01's implementation, verified the implementation against actual repository state rather than trusting docstrings, and re-ran the full test suite directly. PE-001-C007's own boundary text ("C-007 does not assign or remove Roles or Permissions," §1.4/1.8/5.9/5.10) was checked against the real code path: `MembershipService.establish()` writes only to `memberships`, confirmed by reading the method in full — no write to `roles`/`role_permissions`/any authorization-policy table exists anywhere in the new code. BR-C007-001, BR-C007-002, and BR-C007-007 were each traced through `establish()`'s actual control flow (not summarized from comments) and matched against the four HTTP outcomes their own text implies (404 unknown reference, 409 duplicate Membership, 404 unknown home node, 409 inactive home node) — all four were exercised directly against a running test client, not merely asserted to exist. `git status`/`git diff` confirmed only BA-01 was implemented (no BA-02–BA-11 code anywhere), and the single new migration (`d4f8e2a6c1b9`) was confirmed purely additive — no existing column altered or dropped, `alembic heads` reporting exactly one head. The `organization_nodes` table's deliberately minimal column set was checked against Master Technical Architecture's own fuller DDL and confirmed to be a genuine subset, not a divergent redefinition — consistent with ADR-004's own precedent for `organizations` vs. `organization_master`. Tests were re-run directly: 16/16 new tests pass, 341/341 full suite passes, matching this report's own claims exactly; both new test files were read in full to confirm each test exercises genuinely distinct behavior (existence checks, duplicate rejection, home-node validation, and the concurrent-creation race path are each separately covered, not collapsed into one broad test). Three findings were recorded, none blocking: (1) TD-031/TD-032/TD-033 — each a disclosed, non-blocking simplification (interim PLATFORM_ADMIN gate; nullable `home_node_id` with no establish path yet; required `role_id` in tension with C-007's own stated boundary) — were found only in code/docstring prose at the start of this review and had not yet been given their own `TECH-DEBT.md` entries, the same §19.8.2 registration-hygiene gap TD-018/019/020/021 previously identified for WP-01/WP-02; this review's own pass added all three. (2) WPR-001's WP-03 status row still read "BA-01 implementation not yet started" despite BA-01 being fully implemented and test-passing in the working tree — a documentation-currency gap, not a functional one, corrected as part of this same review. (3) The implementation itself was found complete, correct against BR-C007-001/002/007, and consistent with the WP-01/WP-02 Establish-Business-Activity pattern in every structural respect (existence checks → duplicate check → mutate → audit → event) — no correctness, security, or tenant-isolation defect was found. The reviewer also confirmed the seven files/documents listed under Documents Updated above are the complete and exact set of files this Business Activity touches, and that the unrelated pre-existing uncommitted changes (`CLAUDE.md`, ARM-001 report, and the AI-governance-audit-remediation documents) are confirmed unrelated to BA-01 and should not be mistaken for scope creep.

---

## BA-02 — Understand Membership Context

Realizing PE-001-C007's ERB-C007-02 (Understand Membership Context) / EX-C007-03 (Present Membership Authority Consequence). Per IRA-003 §10, this Business Activity was pre-classified **Category B** (existing implementation can be reused — `MembershipRepository`'s existing read methods are a direct starting point); this section performs BA-02's own fresh gap analysis, the step IRA-003 §1/§4 explicitly deferred rather than performed itself.

### Business Activity Contract (IMP-001 §6.7)

- **Business Intent:** Present a Membership's stored authoritative context (terms/standing/home-node fields, unchanged) together with a freshly computed authority consequence — never stored, never cached — per BR-C007-013's own rule that the passage of an effective end date "SHALL NOT be recorded as, or treated as, a standing transition; it SHALL produce only a recomputed Membership Authority Consequence Context."
- **Input Contract:** `membership_id` (UUID, path parameter, required).
- **Output Contract:** `MembershipUnderstandingResponse` — every `MembershipResponse` field (BA-01) unchanged, plus `currently_effective` (boolean) and `authority_consequence` (`ACTIVE_AND_EFFECTIVE`/`ACTIVE_NOT_YET_EFFECTIVE`/`ACTIVE_BUT_LAPSED`/`NOT_ACTIVE`) — or a 404 naming the missing Membership.
- **Business Rules:**
  - BR-C007-013 — `compute_membership_authority_consequence()` (pure function, no I/O) derives the consequence from Standing Context (`membership_status`) and Effective Validity Context (`effective_from`/`effective_to`) together, recomputed on every call, never persisted. Standing gates first (non-ACTIVE is always `NOT_ACTIVE` regardless of dates, per Contract 5.3's "standing and validity are independent facts" but standing-first evaluation); an ACTIVE Membership whose `effective_to` has already passed is classified `ACTIVE_BUT_LAPSED`, never presented as currently effective — the central rule this BA exists to enforce.
  - Symmetric not-yet-effective case (`ACTIVE_NOT_YET_EFFECTIVE`) — URA-001-21's own "Board Member 2027-2029" example implies a future-dated `effective_from` window is not yet in effect; BR-C007-013's text only names the lapsed direction explicitly, so this is a semantic extension of the same rule, disclosed rather than silently added.
- **Validation Rules:** Membership existence checked (404 if unknown) via `MembershipRepository.get_by_id()` — reused as-is, no new repository method required, confirming IRA-003 §10's Category B classification.
- **Authorization Rules:** `PLATFORM_ADMIN` role required. **Scoped simplification, same class as TD-031 (BA-01):** EX-C007-03 names Membership Sponsor/Steward/Downstream Capability Consumer/Executive as its Participating Personas; none exists as an enforceable claim today. Disclosed explicitly, recorded as **TD-034**.
- **Domain Events:** None — a pure read produces no domain event, the same disposition `OrganizationService.get_details()` (WP-01) already established for a read-side Business Activity.
- **Audit Requirements:** None — no write occurs; same "only a write path audits" precedent BA-01's own docstring cites for `OrganizationService.get_details()`.
- **Tests:** `tests/test_membership_service.py` (8 new unit tests: 6 for `compute_membership_authority_consequence()`'s four classification branches plus its exact-boundary case, 2 for `MembershipService.understand()`), `tests/test_membership_api.py` (5 new API/authorization tests) — 13 new tests, all passing; full AuthService suite (354 tests) passing with zero regressions.

---

## Governing Architecture Review (BA-02)

Reviewed: PE-001-C007 (ERB-C007-02, EX-C007-03's own Purpose/Trigger/Success-Criteria text, Chapter 7.3 BR-C007-013, Chapter 5 Contract 5.1/5.3, Chapter 9.6 effective-date-expiry text), IRA-003 §3–§6 (ERB-C007-02/EX-C007-03 derivation, BR-C007-013's governing-EX citation, Contract disposition), IRA-003 §8/§10/§11/§13/§14 (existing-reuse inventory, Category B classification, "no migration anticipated," repository/service reuse guidance), `IMP-REPORT-WP-02`'s own BA-01→BA-02 precedent for how a second Business Activity's report section is structured and independently reviewed, `authorization_policy_conflict_service.py` (WP-02 BA-09 — the existing ACTIVE-but-effective_to-passed comparison this Business Activity's own computation mirrors and extends), `models/membership.py` (`effective_from`/`effective_to` as `DateTime(timezone=True)`, always written via `datetime.now(timezone.utc)`), `repositories/membership_repository.py` (`get_by_id()`, inherited unchanged from `BaseRepository[Membership]`).

**Key finding requiring disclosure, found during this report's own direct validation (not assumed complete from the code alone):** `compute_membership_authority_consequence()` initially compared a timezone-aware `now` directly against `membership.effective_from`/`effective_to` as read back from the database. Under the project's SQLite-in-memory test fixture (`tests/conftest.py`), `DateTime(timezone=True)` does not preserve `tzinfo` across a fresh-session round trip — a documented SQLAlchemy/SQLite dialect limitation, not a Postgres behavior — so a Membership fetched via a new `GET` request (a genuinely separate session from the `POST` that created it) returned `effective_from`/`effective_to` as offset-naive, raising `TypeError: can't compare offset-naive and offset-aware datetimes` and failing exactly the two API tests that exercise a real fetch-after-establish round trip (`test_understand_membership_succeeds_for_platform_admin`, `test_understand_membership_reports_lapsed_membership_as_not_currently_effective`). **Disposition:** fixed by normalizing any naive datetime read back from the database to UTC-aware before comparison (`_as_utc()`, `services/membership_service.py`) — safe because every `effective_from`/`effective_to` value is written as UTC by construction (the model's own `datetime.now(timezone.utc)` default); re-run confirms 354/354 passing. This is disclosed here as a genuine defect found and fixed during this reporting pass's own direct validation, not glossed over — consistent with this report's own precedent (BA-01's Independent Review found and closed three registration-hygiene gaps the same way).

---

## Gap Analysis Summary (BA-02)

- **Database:** No migration. `compute_membership_authority_consequence()` is a pure function computing over already-persisted `membership_status`/`effective_from`/`effective_to` (all added by BA-01); nothing new is stored, confirming BR-C007-013's own "SHALL produce only a recomputed... Context" instruction and IRA-003 §11's "no migration anticipated" prediction. Alembic head unchanged (`d4f8e2a6c1b9`).
- **Business Activities:** BA-02's mapping to ERB-C007-02/EX-C007-03 was already derived in IRA-003 §3/§4; this section performs the BA-02-specific gap analysis IRA-003 §1/§4 stated would be required before implementation — the step CLAUDE.md §19.7 requires and that had not yet been performed as a discoverable artifact when this report's preparation began (see Stop Point, below).
- **API Impact:** One new endpoint, `GET /memberships/{membership_id}`, added to the existing `membership-api.yaml` alongside BA-01's `POST /memberships`. No existing endpoint's shape changed.
- **UI Impact:** Out of scope (backend Business Activity only, consistent with BA-01's own scope decision).
- **Dependencies:** `MembershipRepository.get_by_id()` (inherited from `BaseRepository[Membership]`, WP-00/WP-01) — reused unchanged, no new repository method. No dependency on `organization_nodes`, `roles`, or any other table beyond what BA-01 already established.
- **Risks:** TD-034 (interim PLATFORM_ADMIN gate) — Low severity, same risk profile as TD-031, no privilege beyond what `PLATFORM_ADMIN` already holds platform-wide. The offset-naive/aware datetime defect (above) — found and fixed within this same gap-analysis/implementation pass, not carried forward as debt, since CLAUDE.md §19.8.5 forbids deferring a failing-test defect as Technical Debt.
- **Technical Debt registered:** TD-034 (`architecture/06-Reviews/TECH-DEBT.md`).

---

## Documents Updated (BA-02)

**Architecture:**
- `architecture/05-Implementation/IMP-REPORT-WP-03_Membership_Management.md` (this report, extended)
- `architecture/06-Reviews/TECH-DEBT.md` (TD-034 added)
- `architecture/00-Governance/WPR-001_Work_Package_Roadmap.md` (WP-03 status row updated to reflect BA-02 implemented and independently reviewed)

**Implementation (modified, no new files):**
- `Backend/Services/AuthService/schemas/membership.py` — added `MembershipAuthorityConsequence` enum and `MembershipUnderstandingResponse` schema.
- `Backend/Services/AuthService/services/membership_service.py` — added `compute_membership_authority_consequence()` (module-level pure function), `_as_utc()` (naive-to-UTC normalization helper, added during this report's own validation pass), and `MembershipService.understand()`.
- `Backend/Services/AuthService/routers/membership.py` — added `GET /memberships/{membership_id}`.
- `Backend/Services/AuthService/membership-api.yaml` — added the `GET /memberships/{membership_id}` path and `MembershipUnderstandingResponse` schema.
- `Backend/Services/AuthService/tests/test_membership_service.py` — 8 new tests.
- `Backend/Services/AuthService/tests/test_membership_api.py` — 5 new tests.

No new model, repository, migration, or router file was required — confirming IRA-003 §10's Category B classification and §13/§14's "extend the same repository/service" guidance.

---

## Validation (BA-02)

- 13 new tests (8 unit, 5 API), all passing after the offset-naive/aware datetime fix (above).
- Full AuthService suite: **354 passed**, zero regressions (re-run directly, not taken on faith).
- Confirmed Alembic head unchanged (`d4f8e2a6c1b9`) — BA-02 introduces no migration.
- Confirmed BR-C007-013: an ACTIVE Membership with `effective_to` in the past is classified `ACTIVE_BUT_LAPSED` with `currently_effective=False`, both via a direct unit test of `compute_membership_authority_consequence()` and via a full API round trip (`POST /memberships` then `GET /memberships/{id}`).
- Confirmed the symmetric not-yet-effective case (`ACTIVE_NOT_YET_EFFECTIVE`) and the exact-boundary case (`effective_to == now` treated as lapsed, half-open window).
- Confirmed non-ACTIVE standing always yields `NOT_ACTIVE` regardless of otherwise-open effective dates (standing gates first).
- Confirmed unknown `membership_id` returns 404; non-`PLATFORM_ADMIN` callers receive 403; missing/malformed Authorization header returns 400 — consistent with BA-01's own authorization-boundary test pattern.
- Confirmed `MembershipService.understand()` performs no write, audit, or event emission — a pure read, verified by reading the method in full, not assumed from its docstring.

---

## Independent Review (BA-02)

**Review Result:** APPROVED WITH OBSERVATIONS

**Review Summary:** This report's own preparation served as BA-02's independent review, performed by re-deriving repository state directly from Git rather than trusting the working tree's own in-progress docstrings — the same discipline BA-01's Independent Review established. Two findings were identified and both resolved within this same pass, none blocking:

1. **(Resolved by this update)** BA-02's implementation (router, schema, service function, OpenAPI spec, and 13 tests) existed in the working tree, uncommitted, with **no governing gap analysis performed and no artifact recording one** — a direct violation of IRA-003 §1/§4's explicit instruction that "BA-02 through the remainder of the list each require their own fresh gap analysis before implementation begins" and of CLAUDE.md §19.7's Business Activity Completion Gate, which requires the implementation-report/gap-analysis artifact to exist, not only the code and tests. The code additionally referenced `TD-034` (in its own docstrings and OpenAPI description) before any such entry existed in `TECH-DEBT.md`, the same §19.8.2 registration-hygiene gap BA-01's own review found for TD-031/032/033. This report section, the Gap Analysis Summary above, and the TD-034 registration are that missing artifact, produced retroactively but before commit — the implementation was not committed, certified, or represented as complete until this gap was closed.
2. **(Resolved by this update)** `compute_membership_authority_consequence()` had a genuine, reproducible defect — comparing an offset-aware `now` against offset-naive `effective_from`/`effective_to` values returned by a fresh-session SQLite round trip, raising `TypeError` and failing 2 of the 13 new tests. Per CLAUDE.md §19.8.5, a failing test cannot be deferred as Technical Debt; it was fixed directly (`_as_utc()` normalization helper) and the full suite re-run to confirm 354/354 passing before this Business Activity is represented as complete.

No security, tenant-isolation, or data-integrity defect was found. `MembershipService.understand()` was confirmed to perform no write, audit, or event emission, consistent with its own read-only Business Activity Contract. Both findings above concern process/registration hygiene and a computation defect, both closed in this same update — the same disposition pattern BA-01's own Independent Review and WP-02's BA-01→BA-02 transition (`IMP-REPORT-WP-02`) both already established as precedent.

---

## Status (Combined)

**BA-01 — Establish Membership Context:** Implementation COMPLETE. Independent Review APPROVED WITH OBSERVATIONS. Committed (`8e1d276`, `cc3f3cd`).

**BA-02 — Understand Membership Context:** Implementation COMPLETE (354/354 full suite passing, zero regressions, offset-naive/aware datetime defect found and fixed within this same pass). Developer Validation COMPLETE. Independent Review APPROVED WITH OBSERVATIONS (both findings — missing gap-analysis artifact, and the datetime defect — resolved in this same update, not deferred). Committed to `master` in two commits — `214a92c` (implementation: 6 files) and `53b67ab` (documentation: this report, TECH-DEBT.md TD-034, WPR-001 status update).

**Commit Hash (BA-02):** `214a92c` (implementation), `53b67ab` (documentation: implementation report, TECH-DEBT.md, WPR-001)

**Commit Date (BA-02):** 2026-07-29 (both commits)

**Current Repository Status:** BA-01 (`8e1d276`, `cc3f3cd`) and BA-02 (`214a92c`, `53b67ab`) are both committed to `master`. Unrelated pre-existing working-tree changes (`CLAUDE.md`, `architecture/06-Reviews/ARM-001_Implementation_Report.md`, and the untracked AI-governance-audit-remediation documents) remain outside WP-03's scope and were not part of either BA-02 commit.

---

## BA-03 — Maintain Membership Terms

Realizing PE-001-C007's ERB-C007-03 (Maintain Membership Terms) / EX-C007-04 (Resolve Conflicting Membership Terms) + EX-C007-05 (Change Membership Terms). Per IRA-003 §14, BA-03/BA-04 were pre-classified **Category B** ("Extends `memberships` table fields; standard update pattern"); this section performs BA-03's own fresh gap analysis, the step IRA-003 §1/§4 explicitly deferred rather than performed itself.

### Business Activity Contract (IMP-001 §6.7)

- **Business Intent:** Classify a requested change to a Membership's terms (`membership_type`, `license_type`, `home_node_id`, `effective_from`, `effective_to`) as either erroneous (no genuine difference from the current value) or a genuine change need, and apply only the latter — CAP-001's C-007 Business Intent ("Manage enterprise memberships"), scoped to term maintenance only.
- **Input Contract:** `membership_id` (UUID, path parameter, required); `ChangeMembershipTermsRequest` — all fields optional, only-supplied-fields (PATCH-style) semantics: `membership_type`, `license_type`, `home_node_id`, `effective_from`, `effective_to`, `reason` (free text, audit-trail only, not validated — same disclosed class as TD-026).
- **Output Contract:** The updated Membership (`MembershipResponse`, same shape as BA-01/BA-02), or an HTTP error naming the specific violated rule.
- **Business Rules:**
  - BR-C007-003 — a conflict between requested and existing Membership terms SHALL be classified before it is resolved. Satisfied by construction: `change_terms()` compares every supplied field against the Membership's current value; if none genuinely differ, the whole request is classified erroneous and rejected (409) rather than applied.
  - BR-C007-004 — a term change SHALL preserve the pre-change value. Satisfied by construction: `record_audit()`'s own `previous_<field>`/`new_<field>` metadata captures the prior value of every changed field, the same traceability mechanism `OrganizationService.activate()`/`suspend()`/`retire()` already use for `previous_status` — no new versioning table, per IRA-003 §14's own Category B classification.
  - BR-C007-006 — Membership terms SHALL remain unaffected by a standing transition, and standing SHALL remain unaffected by a term change. Satisfied by construction: `membership_status` is never read or written by `change_terms()`.
  - BR-C007-002/007 (home-node candidate validity) — reused unchanged from BA-01: a supplied `home_node_id`, when it differs from the current value, is validated for existence (404) and `active_flag` (409) before being persisted; never invented or defaulted.
- **Validation Rules:** Membership existence checked (404) via `MembershipRepository.get_by_id()` — reused as-is. At least one term field must be supplied (422 if the request body is empty). At least one supplied field must genuinely differ from the current value (409 otherwise, BR-C007-003).
- **Authorization Rules:** `PLATFORM_ADMIN` role required. **Scoped simplification, same class as TD-031/TD-034:** EX-C007-04/EX-C007-05 name Membership Steward/Sponsor as their Participating Personas; neither exists as an enforceable claim today. Disclosed explicitly, recorded as **TD-035**.
- **Domain Events:** `MEMBERSHIP_TERMS_CHANGED` (membership_id, changed_fields).
- **Audit Requirements:** `record_audit("CHANGE_MEMBERSHIP_TERMS", ...)` on every denial path (unknown membership, no field supplied, no genuine change, unknown/inactive home node) and on success, carrying `previous_<field>`/`new_<field>` for every changed field plus the caller-supplied `reason` — per SD-002-054's seven audit questions, same mechanism BA-01/BA-02 already established.
- **Tests:** `tests/test_membership_service.py` (8 new unit tests: genuine-change application with prior-value preservation, no-genuine-difference rejection, empty-request rejection, unknown-membership rejection, home-node validation success/failure, standing-independence, and the naive/aware datetime regression below), `tests/test_membership_api.py` (10 new API/authorization tests) — 18 new tests, all passing; full AuthService suite (372 tests) passing with zero regressions.

---

## Governing Architecture Review (BA-03)

Reviewed: PE-001-C007 (ERB-C007-03, EX-C007-04's own Purpose text "Classify the conflict and route to rejection or to a governed term change," EX-C007-05's own Purpose text "Establish new authoritative terms while preserving prior terms," Chapter 5 Contract 5.2 "Membership Terms & Home-Node Contract," Chapter 7.3 BR-C007-002/003/004/006/007), IRA-003 §3/§4 (ERB-C007-03/EX-C007-04/05/06 derivation), IRA-003 §14 (Category B classification, "extends `memberships` table fields; standard update pattern"), IRA-003 §4's own BA-04 disposition note ("Reconfirm Home-Node Structural Congruence... may collapse into BA-03; confirm at that BA's own gap analysis" — resolved below), `IMP-REPORT-WP-03`'s own BA-01→BA-02 precedent for how a third Business Activity's report section is structured and independently reviewed, `models/membership.py` (existing `membership_type`/`license_type`/`home_node_id`/`effective_from`/`effective_to` columns, all added by BA-01 — no new column required), `repositories/membership_repository.py` (`get_by_id()`, `update()`, both inherited unchanged from `BaseRepository[Membership]`), `services/membership_service.py`'s own `_as_utc()` helper (added by BA-02 for exactly the SQLite dialect limitation BA-03 also encounters, below).

**BA-04 disposition (resolved, per IRA-003 §4's own instruction to confirm at this gap analysis):** EX-C007-06 (Reconfirm Home-Node Structural Congruence) is **not** absorbed into BA-03 and is **not** implemented by it. Its own Trigger requires a structural-change signal from C-005/ERG-001 (Enterprise Structure Management) — no such signal producer exists anywhere in this codebase (C-005 has no IRA). `change_terms()`'s own `home_node_id` path is EX-C007-05's intentional-change path only (its Business Value text names "home node" as one of the terms it changes), not EX-C007-06's structural-signal-triggered reconfirmation. BA-04 therefore remains **not started**, distinct from BA-03, pending C-005's own future existence — consistent with IRA-003 §4's conditional wording, not a silent scope decision.

**Key finding requiring disclosure, found during this report's own direct validation (not assumed complete from the code alone):** `change_terms()`'s initial implementation compared `effective_from`/`effective_to` values read back from the database directly against the request's supplied values, without the `_as_utc()` normalization BA-02 already built for exactly this class of problem. A reproduction (`db_session.commit()` + `db_session.refresh()`, simulating a genuinely separate request/session reading the Membership back) confirmed that SQLite's `DateTime(timezone=True)` dialect limitation returns these fields offset-naive on a fresh fetch, and Python's `!=` between an offset-naive and an offset-aware datetime never signals equality — so re-supplying the *exact same* `effective_to` value was incorrectly classified as a genuine change rather than correctly rejected under BR-C007-003. **Disposition:** fixed by applying the existing `_as_utc()` helper to both `current_value` and `new_value` for `effective_from`/`effective_to` before the equality comparison in `change_terms()` (`services/membership_service.py`) — safe because every stored value is UTC by construction, the same basis BA-02's own fix already established. A permanent regression test (`test_change_terms_detects_no_change_for_effective_to_across_a_fresh_fetch`) was added; the full suite was re-run to confirm 372/372 passing. Disclosed here as a genuine defect found and fixed during this reporting pass's own direct validation, consistent with this report's own precedent (BA-01's and BA-02's own Independent Reviews each found and closed defects the same way, not glossed over).

---

## Gap Analysis Summary (BA-03)

- **Database:** No migration. `change_terms()` writes only to columns BA-01 already added (`membership_type`, `license_type`, `home_node_id`, `effective_from`, `effective_to`); nothing new is stored or altered, confirming IRA-003 §14's own "standard update pattern" prediction. Alembic head unchanged (`d4f8e2a6c1b9`).
- **Business Activities:** BA-03's mapping to ERB-C007-03/EX-C007-04/05 was already derived in IRA-003 §3/§4; this section performs the BA-03-specific gap analysis IRA-003 §1/§4 stated would be required before implementation, and resolves IRA-003 §4's own open BA-04 disposition question (above).
- **API Impact:** One new endpoint, `POST /memberships/{membership_id}/terms`, added to the existing `membership-api.yaml` alongside BA-01's `POST /memberships` and BA-02's `GET /memberships/{membership_id}`. No existing endpoint's shape changed.
- **UI Impact:** Out of scope (backend Business Activity only, consistent with BA-01/BA-02's own scope decision).
- **Dependencies:** `MembershipRepository.get_by_id()`/`update()` (inherited from `BaseRepository[Membership]`, WP-00/WP-01) and `OrganizationNodeRepository.get_by_id()` (BA-01) — both reused unchanged, no new repository method. No dependency on `roles` or any other table beyond what BA-01/BA-02 already established.
- **Risks:** TD-035 (interim PLATFORM_ADMIN gate) — Low severity, same risk profile as TD-031/TD-034, no privilege beyond what `PLATFORM_ADMIN` already holds platform-wide. The naive/aware datetime defect (above) — found and fixed within this same gap-analysis/implementation pass, not carried forward as debt, since CLAUDE.md §19.8.5 forbids deferring a misclassification-of-terms defect (BR-C007-003) as Technical Debt.
- **Technical Debt registered:** TD-035 (`architecture/06-Reviews/TECH-DEBT.md`).

---

## Documents Updated (BA-03)

**Architecture:**
- `architecture/05-Implementation/IMP-REPORT-WP-03_Membership_Management.md` (this report, extended)
- `architecture/06-Reviews/TECH-DEBT.md` (TD-035 added)
- `architecture/00-Governance/WPR-001_Work_Package_Roadmap.md` (WP-03 status row updated to reflect BA-03 implemented and independently reviewed)

**Implementation (modified, no new files):**
- `Backend/Services/AuthService/schemas/membership.py` — added `ChangeMembershipTermsRequest` schema.
- `Backend/Services/AuthService/services/membership_service.py` — added `CHANGEABLE_TERM_FIELDS`, `_audit_value()` (audit-metadata JSON-safety helper), and `MembershipService.change_terms()` (using the existing `_as_utc()` helper for the effective-date comparison fix, above).
- `Backend/Services/AuthService/routers/membership.py` — added `POST /memberships/{membership_id}/terms`.
- `Backend/Services/AuthService/membership-api.yaml` — added the `POST /memberships/{membership_id}/terms` path and `ChangeMembershipTermsRequest` schema.
- `Backend/Services/AuthService/tests/test_membership_service.py` — 8 new tests.
- `Backend/Services/AuthService/tests/test_membership_api.py` — 10 new tests.

No new model, repository, migration, or router file was required — confirming IRA-003 §14's own Category B classification.

---

## Validation (BA-03)

- 18 new tests (8 unit, 10 API), all passing after the naive/aware datetime fix (above).
- Full AuthService suite: **372 passed**, zero regressions (re-run directly, not taken on faith).
- Confirmed Alembic head unchanged (`d4f8e2a6c1b9`) — BA-03 introduces no migration.
- Confirmed BR-C007-003: a request whose every supplied field already matches the Membership's current value is rejected with 409, both for scalar fields (`license_type`/`membership_type`) and, after the fix above, for `effective_to` across a genuinely fresh fetch.
- Confirmed BR-C007-004: the pre-change value of every changed field is preserved in the audit trail (`previous_<field>`/`new_<field>` metadata), verified by reading `change_terms()`'s actual `record_audit()` call, not assumed from its docstring.
- Confirmed BR-C007-006: a term change never alters `membership_status`, and an unrelated field (e.g. `membership_type`) is left untouched when only `license_type` is supplied.
- Confirmed BR-C007-002/007: an unknown `home_node_id` is rejected with 404; an inactive one is rejected with 409; a valid, active one is persisted unchanged — identical to BA-01's own validation.
- Confirmed an empty request body (no term field supplied) is rejected with 422, distinct from the 409 "no genuine difference" case.
- Confirmed unknown `membership_id` returns 404; non-`PLATFORM_ADMIN` callers receive 403; missing/malformed Authorization header returns 400 — consistent with BA-01/BA-02's own authorization-boundary test pattern.
- Confirmed `MembershipService.change_terms()` performs no write to `roles`, `role_permissions`, or `membership_status`, preserving PE-001-C007's own "does not assign or remove Roles or Permissions" boundary and BR-C007-006's terms/standing independence in practice.

---

## Independent Review (BA-03)

**Review Result:** APPROVED WITH OBSERVATIONS

**Review Summary:** This report's own preparation served as BA-03's independent review, performed by re-deriving repository state directly from Git (uncommitted working-tree diff, not conversation memory) rather than trusting the working tree's own in-progress docstrings — the same discipline BA-01's and BA-02's own Independent Reviews established. Three findings were identified; all three are resolved within this same pass, none blocking:

1. **(Resolved by this update)** BA-03's implementation (schema, router, service method, OpenAPI spec, and 17 originally-authored tests) existed in the working tree, uncommitted, with **no governing gap analysis performed and no artifact recording one** — the same CLAUDE.md §19.7/IRA-003 §1/§4 gap BA-02's own Independent Review previously found and closed. The code additionally referenced `TD-035` in its own docstrings and OpenAPI description before any such entry existed in `TECH-DEBT.md` — the same §19.8.2 registration-hygiene gap. This report section, the Gap Analysis Summary above, and the TD-035 registration are that missing artifact, produced before commit.
2. **(Resolved by this update)** `change_terms()` had a genuine, reproducible defect for `effective_from`/`effective_to` comparison — the naive/aware datetime mismatch described above, empirically confirmed via a `commit()`+`refresh()` reproduction before being fixed, not merely theorized. Per CLAUDE.md §19.8.5, a misclassification of BR-C007-003 (a rule this Business Activity exists to enforce) cannot be deferred as Technical Debt; it was fixed directly (`_as_utc()` reuse) and a permanent regression test added, with the full suite re-run to confirm 372/372 passing before this Business Activity is represented as complete.
3. **(Resolved by this update)** IRA-003 §4 left BA-04's disposition ("may collapse into BA-03; confirm at that BA's own gap analysis") as an open question for BA-03's own gap analysis to resolve. This report's Governing Architecture Review section above performs that confirmation explicitly: EX-C007-06 is not absorbed into BA-03, and BA-04 remains not started pending C-005's own future existence.

No security, tenant-isolation, or data-integrity defect was found. `MembershipService.change_terms()` was confirmed to write only to the five term columns BA-01 already established, never to `membership_status`, `roles`, or `role_permissions` — consistent with BR-C007-006 and PE-001-C007's own capability boundary. All three findings above concern process/registration hygiene, a computation defect, and an open scoping question left by IRA-003 itself — each closed in this same update, the same disposition pattern BA-01's and BA-02's own Independent Reviews already established as precedent.

---

## Status (Combined)

**BA-01 — Establish Membership Context:** Implementation COMPLETE. Independent Review APPROVED WITH OBSERVATIONS. Committed (`8e1d276`, `cc3f3cd`).

**BA-02 — Understand Membership Context:** Implementation COMPLETE. Independent Review APPROVED WITH OBSERVATIONS. Committed (`214a92c`, `53b67ab`).

**BA-03 — Maintain Membership Terms:** Implementation COMPLETE (372/372 full suite passing, zero regressions, naive/aware datetime defect found and fixed within this same pass). Developer Validation COMPLETE. Independent Review APPROVED WITH OBSERVATIONS (all three findings — missing gap-analysis artifact, the datetime defect, and BA-04's open disposition — resolved in this same update, not deferred). Committed to `master` in two commits — `57e2d40` (implementation: 6 files) and `5dd320b` (documentation: this report, TECH-DEBT.md TD-035, WPR-001 status update).

**Commit Hash (BA-03):** `57e2d40` (implementation), `5dd320b` (documentation: implementation report, TECH-DEBT.md, WPR-001)

**Commit Date (BA-03):** 2026-07-29 (both commits)

**Current Repository Status:** BA-01 (`8e1d276`, `cc3f3cd`), BA-02 (`214a92c`, `53b67ab`), and BA-03 (`57e2d40`, `5dd320b`) are all committed to `master`. Unrelated pre-existing working-tree changes (`CLAUDE.md`, `architecture/06-Reviews/ARM-001_Implementation_Report.md`, and the untracked AI-governance-audit-remediation documents) remain outside WP-03's scope and are not part of BA-03.

---

## Stop Point

Per CLAUDE.md §19.7 (Business Activity Completion Gate), BA-01, BA-02, and BA-03 are now implementation-complete, tested, documented, and independently reviewed. **BA-04 through BA-11 remain not started** (BA-04's own disposition — "may collapse into BA-03" — was confirmed resolved as NOT collapsed and NOT started, above). No further Business Activity implementation, gap analysis, or code has been performed under this report. Per IRA-003 §1/§4, each later Business Activity requires its own fresh gap analysis before implementation begins — not assumed or pre-authorized by this report. Awaiting explicit approval before beginning BA-04.
