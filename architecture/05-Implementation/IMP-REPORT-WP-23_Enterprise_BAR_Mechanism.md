# IMP-REPORT-WP-23 — Enterprise Business Activity Registry (BAR) Mechanism

**Work Package:** WP-23 — Enterprise BAR Mechanism (Runtime / cross-cutting platform infrastructure; no `CAP-001` capability; no PE-001 Enterprise Experience)
**Governing Work Package Charter:** `WP-23_Enterprise_BAR_Mechanism_Implementation_Charter.md` (Workstreams A–H). **This report covers the A–C tranche only.**
**Governing Design:** `architecture/06-Reviews/ENTERPRISE-BAR-MECHANISM-DESIGN-AND-IMPLEMENTATION-READINESS.md` (§4 registration model, §5 identifier model, §6 index model, §14–§16, §18, §19a.6)
**Governing Decisions:** `ROD-ENTERPRISE-BAR-Decision-Preparation.md` D1–D8; design §19a (D9); tranche decisions RD-23-01 and RD-23-02 (`architecture/06-Reviews/IRA-WP-23-AC_BAR_Workstreams_A-C_Closure_Readiness.md §0`)
~~**Open decision affecting this report:** **RD-23-03 — registry authority** (`architecture/06-Reviews/ROD-WP-23-AC-BAR-Registry-Authority-Decision-Preparation.md`)~~
**Registry authority (updated 2026-09-25):** **RD-23-03 decided, Option D — Layered Authority Model** (`architecture/06-Reviews/ROD-WP-23-AC-BAR-Registry-Authority-Decision-Preparation.md §0`).
- **Registering act:** governance authority.
- **`bar_registration`:** runtime execution registration. A row is not proof of authorization.
- **`BAR-INDEX.md`:** governance catalogue only.
- **Reconciliation:** must stay traceable; no mechanism is decided yet.
**Scope of this report:** **Workstreams A (BAR index), B (identifier issuance) and C (registration mechanism).** Workstreams D, E, F, G and H are not implemented and not started. **WP-23 remains OPEN.** *(2026-09-30: this report also carries the governance status of the TD-171 remediation tranche, Charter §21a; see "TD-171 Remediation Tranche (Charter §21a): Governance Status" below. No tranche implementation evidence exists yet.)*

**Implementation Status:** ~~***IMPLEMENTATION COMPLETE — AWAITING INDEPENDENT VERIFICATION*** (A–C tranche).~~
- ~~Not independently verified, not accepted, not certified and not committed.~~
- Written 2026-09-25, after implementation (2026-09-22), per `IRA-WP-23-AC` P-5.

*(Synchronized 2026-09-28, Gate 5 condition C-2, `RRA-WP-23-AC` ST-7.)* ***IMPLEMENTATION COMPLETE — INDEPENDENTLY VERIFIED — GATE 5 PASS WITH CONDITIONS*** (A–C tranche).
- **Gate 1** (`CERT-WP-23-AC`): STOP. Its governance blocker CERT-F-01 was resolved by Repository Owner decision **RD-23-04**, which ratified the B/C runtime construction and corrected the Charter and design. CERT-F-02 was resolved by the WP-20 and WP-21 commits (`355ebbe`, `203bed1`). The verdict was not re-issued (Gate 5 C-3).
- **Gate 2** (`VV-AUDIT-WP-23-AC`): FAIL on VV-F-01 (High). The **Gate 3** remediation followed (this report), and **Gate 4** (`VV-AUDIT-WP-23-AC_…_Gate-4`) passed.
- **Gate 5** (`RRA-WP-23-AC_…_Release_Readiness_Audit`): PASS WITH CONDITIONS. ~~C-1 and C-2 are being remediated (2026-09-28).~~ *(C-3 addendum, 2026-09-28: C-1 and C-2 completed; C-3 satisfied by the Repository Owner Acceptance Record, `IRA-WP-23-AC §0.2`; C-4 outstanding.)*
- ~~**NOT ACCEPTED, NOT CERTIFIED, NOT COMMITTED. WP-23 remains OPEN.**~~ *(C-3 addendum, 2026-09-28.)* **ACCEPTED** (A–C tranche; RD-23-02 terminal state) and committed together with the acceptance record. **NOT CERTIFIED, NOT CLOSED. WP-23 remains OPEN; Workstreams D–H are not implemented.** TD-171's execution-eligibility condition remains open.

---

## A–C Tranche

### Authorization

- **Implementation authority:** WP-23 Charter §20. "WP-23 is authorized to implement the enterprise BAR mechanism strictly within Workstreams A–G (§21), as specified in `ENTERPRISE-BAR-MECHANISM-DESIGN-AND-IMPLEMENTATION-READINESS.md` and this Charter", subject to the §19.7b five-gate sequence before release.
- **No separate per-workstream RO authorization record for B or C was found** in the repository (searched 2026-09-25). This report records that absence; it does not supply one.
- **Tranche closure unit:** RD-23-02 (RO, 2026-09-25). A–C may reach IMPLEMENTED → INDEPENDENTLY VERIFIED → ACCEPTED as a tranche. WP-23 stays OPEN, and the tranche's acceptance does not make WP-23 complete, closed or certified.

**Scope question disclosed, not resolved.** Charter §21 row C describes Workstream C as a "registering-act convention … **Low risk — governance-only, no runtime**". The implementation built a runtime table (`bar_registration`), a service and a migration. The design §6 left the existence of a runtime store undecided and named it the "most likely eventual shape"; it did not decide it. Whether the runtime store is within the Charter §20 authorization depends on **RD-23-03**. That question is Gate 1 check G1-2 (`IRA-WP-23-AC §9.1`).

### Governing Architecture Review

Sources re-read for this report: the WP-23 Charter (§3–§7, §14–§16, §19–§22); the design (§4, §5, §6, §10, §14–§18, §19a.6); `ROD-ENTERPRISE-BAR` D2, D5 and D7; `BAR-INDEX.md` in full; the implementation files below; `CLAUDE.md` §18, §19.7, §19.7b, §19.8.5 and §21.4.

### Files Created (all untracked; paths under `Backend/Services/AuthService/` unless stated)

| Workstream | File | Purpose |
|---|---|---|
| A | `architecture/00-Governance/BAR-INDEX.md` | BAR Registration Index. Structure per design §6; zero registrations; illustrative example (§6 of the index) kept outside the Register |
| B | `models/bar_identifier_ledger.py` | `BarIdentifierLedger`: `id` (UUID PK), `identifier` (`String(20)`, UNIQUE, indexed), `issued_at`. `BAR_IDENTIFIER_PREFIX = "BA"` |
| B | `repositories/bar_identifier_repository.py` | `max_identifier_sequence()` (fixed-offset `substr` + `CAST`, `MAX`, `COALESCE 0`); `count_issued()` |
| B | `services/bar_identifier_service.py` | `BarIdentifierService.issue_identifier()`: `MAX+1` → `BA-NNNNNN`, UNIQUE backstop, up to 5 allocate-and-retry attempts, `BarIdentifierAllocationExhausted`; `record_audit` / `publish_event` |
| B | `alembic/versions/2026_09_22_0900-a7b8c9d0e1f2_bar_identifier_ledger.py` | Additive: creates `bar_identifier_ledger` plus `ix_bar_identifier_ledger_identifier`. `down_revision = f6a7b8c9d0e1` |
| B | `tests/test_bar_identifier_service.py` | 9 tests |
| C | `models/bar_registration.py` | `BarRegistration`: the eight design-§4 fields. `identifier` FK to `bar_identifier_ledger.identifier`, UNIQUE. `ck_bar_registration_status` (`= 'REGISTERED'`). `uq_bar_registration_wp_reference` (`owning_work_package`, `business_activity_reference`) |
| C | `repositories/bar_registration_repository.py` | `get_by_work_package_and_reference`, `get_by_identifier`, `count_registered` (read-only) |
| C | `services/bar_registration_service.py` | `BarRegistrationService.register()`: required-field validation, duplicate pre-check, then ledger insert plus registration insert in **one flush** (atomic), with retry and race discrimination; `BarRegistrationAlreadyExists` / `BarRegistrationAllocationExhausted`; shared-session enforcement; audit and event |
| C | `alembic/versions/2026_09_22_1000-b8c9d0e1f2a3_bar_registration.py` | Additive: creates `bar_registration` with named PK, FK, unique and check constraints plus `ix_bar_registration_identifier`. `down_revision = a7b8c9d0e1f2` |
| C | `tests/test_bar_registration_service.py` | 13 tests |

### Files Modified

| File | Change | Note |
|---|---|---|
| `models/__init__.py` | +2 imports and +2 `__all__` entries (`BarIdentifierLedger`, `BarRegistration`) | Shares one diff hunk with WP-20's `C021OfferingDefinition` and WP-21's `C022CommercialAccount` lines (uncommitted). The WP-23 commit must stage only the BAR lines (`IRA-WP-23-AC §0`) |

**No router, schema (Pydantic), API, endpoint, frontend, adapter or `main.py` change belongs to A–C.** No Workstream D, E, F or H code exists.

### Implementation Summary

- **A.** A governance index mirroring `CBOR-INDEX.md`, with the eight design-§4 columns, a two-state Registration Status, the D2/D5/D8/D9 baseline, the §4 state model, the C-024 relationship and an amendment procedure. It contains zero registrations.
- **B.** A persistent issuance ledger (`bar_identifier_ledger`) and service. Identifiers are `BA-` plus six zero-padded digits, sequential from `BA-000001`. The format is `[IMPLEMENTATION DESIGN — not constitutional text]` (design §5; Charter §6). Allocation reuses the application-level monotonic-allocator pattern certified for `c021_offering_definition.offering_reference` (O1). There is no PostgreSQL SEQUENCE.
- **C.** A persistent registration table and service. `register()` issues the identifier and registers it atomically, so D5's "assigned at registration" holds structurally for this path.
  - Two-state status is enforced by a CHECK constraint.
  - Duplicate protection is a database UNIQUE constraint on `(owning_work_package, business_activity_reference)`.
  - The service does **not** write `BAR-INDEX.md`.

### Design Decisions Requiring Disclosure

| # | Decision | Status |
|---|---|---|
| DD-1 | A runtime store (both tables) was built for Workstreams B and C, where Charter §21 row C reads "governance-only, no runtime" | ~~Open: RD-23-03 / G1-2~~ *(2026-09-25)* RD-23-03 (Option D) assigns the table the runtime-registration role. ~~**Whether building it was within the Charter's authorization remains Gate 1's determination (G1-2)**; the RD-23-03 decision does not settle it~~ *(Synchronized 2026-09-28, ST-9.)* Gate 1 classified the conflict as a governance problem (CERT-F-01). **Resolved by Repository Owner decision RD-23-04** (`IRA-WP-23-AC §0`): it ratified the B/C runtime construction as within the WP-23 design boundary (past construction only; no D/E/M2 authority) and applied dated corrections to Charter §21 rows C/D and design §19 rows C/D |
| DD-2 | The `bar_registration` docstring claims the table is "the authoritative persisted record of Business Activity registration", while `BAR-INDEX.md §1` claims the index is authoritative | ~~Open: RD-23-03~~ *(2026-09-25)* `BAR-INDEX.md §1` is updated to Option D. ~~**The runtime docstrings are not updated** (no runtime-code change is authorized): GAP-23-03-3~~ *(Synchronized 2026-09-28, ST-9.)* The runtime docstrings were corrected under the RO-authorized Gate 3 remediation (CERT-F-03; see "Gate 3 Remediation" below) and verified at Gate 4. GAP-23-03-3 is closed |
| DD-3 | `BarRegistrationService` does not write `BAR-INDEX.md`, so the two can diverge; no reconciliation mechanism exists | ~~Open: RD-23-03~~ *(2026-09-25)* Option D requires the two to stay traceably related, and leaves the mechanism undecided: GAP-23-03-2, for independent review |
| DD-4 | `register()` enforces no caller authority: no router, no permission check, optional `actor_id`. Governance authority (K-4: RO-authorized registering act) is not enforced in code | *(2026-09-25)* Under Option D a runtime row is not proof of authorization, and no enforcement links the act to the row: GAP-23-03-1, for independent review. No caller exists in the repository today |
| DD-5 | `register()` does not call `BarIdentifierService.issue_identifier()`. It reuses the same repository, allocator and prefix, and inserts both rows in one flush, for atomicity | `[IMPLEMENTATION DESIGN]`, documented in the service docstring |
| DD-6 | `issue_identifier()` used standalone can produce a committed identifier never attached to a registration ("issued but orphaned") | Disclosed in `bar_identifier_service.py`. No caller exists in the repository |
| DD-7 | On an `IntegrityError`, both services call `session.rollback()`, which discards the **whole** session, including any unrelated pending work of the caller | ~~Documented for the issuance service only. To be probed at Gate 2 (G2-7)~~ *(Synchronized 2026-09-28, ST-9.)* Gate 2 classified it as defect VV-F-01 (High). It was **remediated at Gate 3** (a savepoint per attempt; no whole-session rollback) and **verified at Gate 4: PASS**. The related VV-F-07 (orphaned pending ledger row) is closed by later evidence (Gate 4 G4-O-04; Gate 5 probe G5-P1) |
| DD-8 | The duplicate key `(owning_work_package, business_activity_reference)` has no governing source; it reuses two approved fields | `[IMPLEMENTATION DESIGN]`, documented in the model docstring |
| DD-9 | Sequence width: `BA-999999` + 1 would format as seven digits, contrary to `^BA-\d{6}$` (design §5); no guard exists | Disclosed here for the first time. To be probed at Gate 2 (G2-8). No realistic near-term exposure |
| DD-10 | Tenant isolation: neither table has an organization column; BAR is platform-global (design §18; Charter §16 flagged confirmation) | `§21.4` (a)–(c) do not attach (no endpoint; no tenant-owned data). To be confirmed at G1-9 |

### Test Execution

Implementer-run, 2026-09-25, AuthService `venv`. **This is implementer evidence only; it is not independent verification.**

| Suite | Result |
|---|---|
| `tests/test_bar_identifier_service.py` + `tests/test_bar_registration_service.py` | **22 passed** (9 + 13) |
| AuthService full suite (regression; `JWT_SECRET_KEY`/`JWT_ALGORITHM` set to the CI test values, per `TD-010`) | **972 passed**, 0 failed. This matches the M1 baseline of 972. A first run without those variables set gave 502 failed / 470 passed, all failing with `JWT_SECRET_KEY … not defined`; that is the known `TD-010` environment requirement, not a regression |
| `alembic heads` | Single head `b8c9d0e1f2a3`; chain `d4e5f6a7b8c9 → e5f6a7b8c9d0 → f6a7b8c9d0e1 → a7b8c9d0e1f2 → b8c9d0e1f2a3` |

**Known limitation of this evidence (disclosed, not waived):**
- **Foreign keys are not enforced.** The harness (`tests/conftest.py`) uses in-memory SQLite without `PRAGMA foreign_keys=ON`, so the `bar_registration → bar_identifier_ledger` FK is **not enforced in any of the 22 tests**. No FK-integrity claim is made from them. Gate 2 must probe it under genuine enforcement (`IRA-WP-23-AC §9.2`, G2-1 and G2-13).
- **The migrations are untested.** The harness builds the schema with `Base.metadata.create_all`, not with the migrations, so no test exercises `upgrade` or `downgrade`.
- **Concurrency is not tested.** Two tests (`test_true_concurrent_sessions_not_reliably_testable_on_this_harness`) concede that true concurrency cannot be tested on this harness.

### Technical Debt

~~**No new Technical Debt item is recorded by this report.**~~ *(Synchronized 2026-09-28, ST-9; Gate 5 condition C-1.)* The Technical Debt the gates identified is registered in `architecture/06-Reviews/TECH-DEBT.md`:
- **TD-171:** CERT-F-04 / GAP-23-03-1 and 2 (no act-to-row enforcement, no reconciliation). It must close before `bar_registration` is used to decide execution eligibility.
- **TD-172:** CERT-F-05 / F-13 (non-evidential or misnamed tests).
- **TD-173:** CERT-F-08 / VV-F-04 (model/migration drift).
- **TD-174:** CERT-F-14 / VV-F-05 (duplicated allocator; six-digit overflow; DD-5, DD-9).
- **TD-175:** VV-F-06 (no database format CHECK).
- **TD-176:** PostgreSQL/asyncpg verification (Gate 5 G5-07).
- **TD-096:** extended with CERT-F-06 / VV-F-03 and Gate 4 G4-O-01.

The following earlier bullets are preserved as written:
- ~~DD-1 to DD-4 await RD-23-03.~~ *(2026-09-25)* DD-1 to DD-4 and GAP-23-03-1 to 3 await classification by the independent reviewers.
- DD-7 and DD-9 await Gate 2 classification.
- Under `CLAUDE.md §19.8.5`, any data-integrity defect found at Gate 2 must be remediated before acceptance and may not be deferred as debt.

### Independent Review

~~**Not performed.** The Gate 1 and Gate 2 scope is prepared in `IRA-WP-23-AC §9`. Dispatch conditions are in `IRA-WP-23-AC §10`: RD-23-03 decided, or an explicit RO ruling to proceed with it open.~~ *(Updated 2026-09-25.)* Gate 1 and Gate 2 were dispatched to separate fresh-context reviewers on Repository Owner instruction, after RD-23-03 was decided. Their artifacts are `architecture/06-Reviews/CERT-WP-23-AC_BAR_Workstreams_A-C.md` and `architecture/06-Reviews/VV-AUDIT-WP-23-AC_BAR_Workstreams_A-C.md`. This report does not restate their results.

### Certification Status

~~**NOT CERTIFIED. NOT ACCEPTED.**~~ *(C-3 addendum, 2026-09-28.)* **NOT CERTIFIED. ACCEPTED** (2026-09-28, Repository Owner Acceptance Record, `IRA-WP-23-AC §0.2`). Under RD-23-02 the tranche's terminal state ~~will be~~ is **ACCEPTED**, not certified: WP-level certification remains at WP-23 completion (Charter §22).

### Repository Commit

~~**Not committed; commit currently blocked** (RD-23-01).~~
- ~~The WP-23 A–C migrations descend from `e5f6a7b8c9d0` (WP-20 / C-021) and `f6a7b8c9d0e1` (WP-21 / C-022), which are both untracked.~~
- ~~The WP-20 and WP-21 implementation commits must exist first, each under its own Work Package's authority (`IRA-WP-23-AC §0`).~~

*(Synchronized 2026-09-28, ST-8.)* ~~**Not committed.**~~ *(C-3 addendum, 2026-09-28: **committed** as one WP-23 A–C commit, together with the acceptance record, using the `RRA-WP-23-AC §7` boundary; not pushed. ~~The commit hash is recorded at C-4.~~ *(C-4, 2026-09-28: commit `b0f5a12e84a9a3f7d9622bcbea4cee87b934be85`, parent `203bed15cdcb963e98266e89391399fb607611f4`.)*)* The migration-ancestry blocker (RD-23-01) is resolved: WP-20 was committed as `355ebbe` and WP-21 as `203bed1`, each under its own Repository Owner authorization, and the committed head is `f6a7b8c9d0e1`. ~~The commit now awaits Gate 5 conditions C-1 and C-2 (being remediated) and the Repository Owner's acceptance (C-3).~~ *(C-3 addendum, 2026-09-28: C-1 and C-2 completed; C-3 satisfied, `IRA-WP-23-AC §0.2`.)* The boundary is in `RRA-WP-23-AC §7`.
- The WP-23 governance documents are also uncommitted: the Charter, the design, `ROD-ENTERPRISE-BAR`, the investigation, `BAR-INDEX.md` and the `WPR-001` WP-23 row.

### Not Implemented (outside the A–C tranche)

| Workstream | State |
|---|---|
| D — discovery integration | Not started. Depends on WP-BAE-001, per the committed Workstream D investigation |
| E — execution gate | Not started. Remains the BAR-side execution-gate authority (RD-M2-04) |
| F — 21-BA retroactive registration/cutover | Not started. **No Business Activity is registered. No identifier is issued or assigned outside test databases** |
| G — WP-level five-gate verification | Not started |
| H — C-024 integration readiness | No action (`C-024 D10` unchanged) |

---

## A–C Tranche — Gate 3 Remediation (2026-09-26)

**Authorization:** Repository Owner, 2026-09-26: "Proceed with Gate 3 remediation for WP-23 A–C … narrowly authorized."
- **Authorized:** VV-F-01 (High), CERT-F-03 (Medium) and VV-F-02 (Medium), plus the tests and documentation strictly required to prove them.
- **Not authorized:** any other Gate 1 or Gate 2 finding, schema change, M2, or Workstream D or E.

**Status:** ~~***GATE 3 REMEDIATION APPLIED — AWAITING GATE 4 (fresh-context independent verification of remediation).***~~ *(Synchronized 2026-09-28, ST-7.)* ***GATE 3 REMEDIATION APPLIED — GATE 4 PASS*** (`VV-AUDIT-WP-23-AC_BAR_Workstreams_A-C_Gate-4.md`, 2026-09-26). ~~Not accepted, not certified, not committed.~~ *(C-3 addendum, 2026-09-28: accepted (`IRA-WP-23-AC §0.2`) and committed; not certified.)*

### VV-F-01 — Session-safe collision handling

**Root cause.** On an `IntegrityError` inside the allocation loop, both `BarIdentifierService.issue_identifier()` and `BarRegistrationService.register()` called `session.rollback()`. That rolled back the caller's **entire** transaction, including unrelated pending work and earlier flushed registrations in the same session. The service then retried and returned normally. A caller registering two Business Activities in one session could lose the first silently, and its identifier would be handed out again (Gate 2 probe P6h).

**Remediation.**
- **Transaction ownership:** the caller owns the transaction. The services never commit and no longer roll back the caller's session.
- **Caller's pending work:** it is flushed once before allocation, outside the collision handler.
- **Isolating each attempt:** each attempt runs inside `session.begin_nested()`, SQLAlchemy's standard SAVEPOINT API. For registration, an attempt is the ledger insert plus the registration insert. A failed attempt rolls back only to its savepoint, and the objects it added are expunged. The caller's pending and flushed work stays in the outer transaction. On success the savepoint is released into the caller's transaction, and the caller's own commit or rollback decides the outcome, as before.
- **Unchanged:** allocation (`MAX+1`, `BA-NNNNNN`, the UNIQUE backstop, retry, exhaustion), schema, constraints and the authority model.
- **Precedent:** `begin_nested()` is not used elsewhere in the repository. It is the stock SQLAlchemy mechanism, not a new transaction framework. Other services' whole-session rollbacks (request-scoped handlers that own their session) are out of scope and were not changed.

### VV-F-02 — Integrity-error classification

After a failed attempt the failure is classified; the check does not depend on the database dialect:
- **`register()` only:** if the `(owning_work_package, business_activity_reference)` pair now exists, the service raises `BarRegistrationAlreadyExists`, as before.
- **Genuine collision:** if the candidate identifier is now issued (new read method `BarIdentifierRepository.is_issued`), the service retries.
- **Anything else:** the original `IntegrityError` is **re-raised unchanged**. It is not retried, not reported as allocation exhaustion, and is audited as `FAILED` ("integrity failure that is not an identifier collision"), where it was previously a false `DENIED`/"exhausted".

### CERT-F-03 — Docstrings (documentation only; no behaviour change)

- **`models/bar_registration.py`:** the D7 bullet no longer calls the table "the authoritative persisted record". A new RD-23-03 bullet states:
  - the registering act is the governance authority;
  - this table is the execution-time runtime record that BAR logic consults;
  - `BAR-INDEX.md` is the human governance catalogue;
  - a row does not by itself establish governance authorization (`registering_act` is a citation, not a verified link);
  - reconciliation is required.
- **`services/bar_registration_service.py`:**
  - the module docstring's D7 bullet ("the authoritative registration act") is replaced by the same layered statement;
  - the `BAR-INDEX.md` bullet is restated for Option D;
  - the class docstring no longer calls the service the "registration authority";
  - the atomicity paragraph is rewritten, because it described the removed whole-session rollback.

### Files changed

| File | Change |
|---|---|
| `services/bar_identifier_service.py` | Savepoint per attempt; up-front flush; classification (VV-F-01, VV-F-02) |
| `services/bar_registration_service.py` | Same, plus docstrings (VV-F-01, VV-F-02, CERT-F-03) |
| `repositories/bar_identifier_repository.py` | New read-only `is_issued(identifier)` (VV-F-02 classification) |
| `models/bar_registration.py` | Class docstring only (CERT-F-03); no column, constraint or schema change |
| `tests/test_bar_transaction_safety.py` *(new)* | 10 tests (below) |

No migration, schema or `conftest.py` change. The existing 22 BAR tests are unchanged.

### Tests and evidence (implementer-run; not independent verification)

**New tests.** `tests/test_bar_transaction_safety.py` runs on its own file-backed SQLite engine. Every connection sets `PRAGMA foreign_keys=ON`, and the engine applies SQLAlchemy's documented pysqlite/aiosqlite recipe for correct SAVEPOINT semantics (driver autocommit off, explicit `BEGIN`). Collisions are forced as **genuine database UNIQUE violations**, confirmed by a `rollback_savepoint` event counter.

The tests:
1. `test_harness_enforces_foreign_keys` — positive control;
2. `test_first_registration_survives_collision_on_second` — the exact VV-F-01 scenario;
3. `test_unrelated_pending_caller_work_survives_registration_collision`;
4. `test_unrelated_pending_caller_work_survives_issuance_collision`;
5. `test_first_registration_survives_duplicate_race_on_second`;
6. `test_caller_still_owns_the_transaction` — no hidden commit;
7. `test_genuine_collision_exhaustion_still_raises_without_partial_rows`;
8. `test_non_collision_integrity_error_is_not_retried_in_register` — VV-F-02;
9. `test_non_collision_integrity_error_is_not_retried_in_issuance` — VV-F-02;
10. `test_caller_pending_work_failure_is_not_classified_as_collision`.

| Run | Result |
|---|---|
| New tests, post-fix | **10 passed** |
| **Negative control:** new tests against the **pre-fix** services, loaded from a byte-identical scratch snapshot via a preload plugin; repository files untouched | **7 failed, 3 passed.** The 7 defect-targeting tests (2, 3, 4, 5, 7, 8, 9) fail. Tests 1 and 6 are invariants that pass by design. Test 10 also passes pre-fix, because the pre-fix duplicate pre-check already autoflushed the caller's bad data before allocation; it is a regression guard, not a discriminating test |
| **Gate 2 probe `probe_batch_loss.py`, pre-fix** (a copy run in a separate scratch directory; the Gate 2 artifacts are unaltered) | Reproduced VV-F-01 exactly. The collision variant handed out `BA-000002` twice, and only "Second BA" survived the commit. The duplicate-race variant lost "New BA" |
| Same probe, **post-fix** | Collision variant: `BA-000002` "First BA" **and** `BA-000003` "Second BA" survive; no identifier handed out twice. Duplicate-race variant: `BarRegistrationAlreadyExists` raised, **and** "New BA" survives |
| BAR suite (22 existing + 10 new) | **32 passed** |
| AuthService full suite (`JWT_SECRET_KEY`/`JWT_ALGORITHM` set, TD-010) | **982 passed**, 0 failed (972 baseline + 10 new) |

### Known limitations (disclosed, not waived)

- **No PostgreSQL run.** No true concurrent PostgreSQL race was performed, because PostgreSQL is unavailable here. Collisions were forced deterministically on SQLite with enforced foreign keys. SAVEPOINT behaviour under asyncpg (the production driver) is standard but **not exercised here**.
- **SQLite legacy mode in the shared harness.** The shared `db_session` harness uses pysqlite's legacy transaction mode. There, a SAVEPOINT that is the first statement of a transaction is not nested inside a real transaction, and its release commits. This affects only that SQLite harness, not PostgreSQL, and is why the new tests use their own correctly-configured engine. The harness itself is unchanged (TD-096 / VV-F-03 remain open).
- **Upfront flush.** `issue_identifier()`/`register()` now flush the caller's pending work before allocation. The previous code also flushed the whole session (at its single `flush()`), so this changes timing, not scope.

### Gate 2 / Gate 1 findings NOT remediated (out of the authorized scope)

- **Gate 2:** VV-F-03 (harness FK and migration parity, TD-096), VV-F-04 (model/migration drift), VV-F-05 (six-digit overflow), VV-F-06 (no database format check), VV-F-07 (a pending ledger row after a non-database error), O-01.
- **Gate 1:** CERT-F-02 (RD-23-01 prerequisite commits), CERT-F-04 (no act↔row enforcement or reconciliation), CERT-F-05 (the pre-existing "forced collision" tests still do not collide; the new tests do), and CERT-F-08 to F-14.


---

## TD-171 Remediation Tranche (Charter §21a): Governance Status (synchronized 2026-09-30)

*Governance synchronization of already-recorded decisions. It records **no implementation evidence**, because none exists. The A–C tranche content above is unchanged.*

| Item | State | Record |
|---|---|---|
| Charter §21a amendment | **ACCEPTED / IN FORCE** (Gate R1 SATISFIED) | Charter §21a, Repository Owner Acceptance Record (`7f479bd`) |
| Tranche authorization | **AUTHORIZED** (Gate R2 SATISFIED, Option A) | `ROD-WP23-TD-171-Remediation-Tranche-Authorization-Decision-Preparation.md` §19 (`d2aaade`) |
| Authorization conditions | **All 14 conditions in the ROD §19.2 are binding** | Same |
| R3: design/readiness | **NOT SATISFIED** | — |
| R4: implementation and controlled deployment verification | **NOT SATISFIED** | — |
| R5: independent verification/review | **NOT SATISFIED** | — |
| R6: closure evidence and governance synchronization | **NOT SATISFIED** | — |
| Implementation | **Not started. No implementation, tests, commits, migrations or deployment evidence exist for this tranche** | — |
| TD-171 | **OPEN**, remediation required. Closes only at R6 (§21a.8) | `TECH-DEBT.md` (unchanged) |

**Outstanding under the conditions** (not satisfied by authorization):
- R3 design/readiness, including the machine-verifiable act-citation rule;
- canonical production environment designation;
- database-role separation (design and provisioning);
- controlled read-only reconciliation access;
- TD-176 PostgreSQL verification before closure.

**Boundaries:**
- Workstreams A–C remain **ACCEPTED** and are **not reopened**.
- WP-23 remains **OPEN**, not certified or closed.
- TD-172 to TD-175 are **not** authorized.
- WP-BAE-001 **M2 NOT AUTHORIZED / NOT STARTED**; **M2-P CHARTERED / NOT AUTHORIZED / NOT STARTED**.

**R3 Design Decisions (synchronized 2026-09-30).**
- *This synchronizes design decisions already established in `architecture/06-Reviews/TDS-WP23-TD-171-R3-Remediation-Design-and-Readiness.md` §17.1 (`fa93fc7`), and already synchronized into Charter §21a.6 and `ROD-WP23-TD-171-Remediation-Decision-Preparation.md` §19.7 (`649f55a`).*
- **It is not a new decision.** It records **design decisions only**: nothing is implemented, verified or satisfied by them.

| OD | Design decision | State |
|---|---|---|
| OD-1 | **Two-part governed act.** An authorization component establishes the governed registration intent before identifier issuance. An execution/registration addendum records the BAR Business Activity Identifier actually issued at registration. D5 is unchanged, and no identifier is pre-created to satisfy the act. Until the execution evidence exists, the registration is not treated as governed, and the OD-5 block applies | **DESIGN DECIDED** (not implemented) |
| OD-2 | **Both canonical BAR write paths are governed:** `issue_identifier()` and `register()`. The AuthService runtime database role is **intended** to have no INSERT, UPDATE or DELETE on either BAR table. The governed deployment-time operation is the controlled production write path. Static caller verification is **intended** to cover both methods. A design decision within the TD-171 tranche, not a Workstream B/C scope expansion | **DESIGN DECIDED** (role restriction and caller verification not implemented or verified) |
| OD-3 | **Structured governed-act metadata convention**, using the repository's existing Field/Value metadata-table style, not YAML front matter. **No act registry.** It separates the human-readable governance record, machine-verifiable metadata/citation, and runtime validation inputs. The field convention is defined in the R3 TDS §17.1.3 | **DESIGN DECIDED** (no runtime validation exists yet) |
| OD-4 | Canonical-environment identity check. No environment name, database identity, connection identifier or deployment designation is recorded or inferred | **OPEN / EXTERNAL PREREQUISITE** |
| OD-5 | **Deployment-level integrity block** for ungoverned or unverifiable BAR rows. It detects, blocks, reports and preserves the evidence, and requires separately governed remediation. **No new BAR registration status.** M2 does not compensate for invalid BAR governance | **DESIGN DECIDED** (control not implemented or tested) |

**Status distinction.** DESIGN DECIDED is not IMPLEMENTED, VERIFIED or R3 SATISFIED. The R3 checklist states are unchanged:
- **C-05, C-06 and C-11:** designed, decision resolved. **Not implemented; no PASS.**
- **C-07** (database-role provisioning), **C-09** (reconciliation access) and **C-10** (canonical environment designation): **not satisfied**, external.

**R3: NOT SATISFIED; NOT READY FOR R3 ACCEPTANCE REVIEW.**

**External prerequisites outstanding:**
- canonical production environment designation;
- database-role provisioning;
- controlled read-only reconciliation access;
- a target PostgreSQL environment.

**R3 External Prerequisites Request (synchronized 2026-09-30).**
- *Status synchronization of the committed request package `architecture/06-Reviews/TDS-WP23-TD-171-R3-External-Prerequisites-Request.md` (`7a3b639`).*
- The package was issued to **Platform Engineering**: the ownership **role** defined by responsibility in `Backend/Services/AuthService/docs/OPERATIONAL_OWNERSHIP.md` ("Deployment and release"; "Database ownership"). No individual is named.
- **The request package is committed. The prerequisites themselves remain outstanding.** This records the issuance of a **request**, not delivery, and **does not change the R3 gate state**.

| EP | Request | Status |
|---|---|---|
| EP-01 | Canonical production environment designation: an authoritative designation of the actual canonical production environment and database for enterprise-global BAR identifiers. `ENVIRONMENT=production` is **not** itself treated as that designation. No environment or database identity has been invented | **REQUESTED / NOT PROVIDED** |
| EP-02 | Database-role separation: an evidenced PostgreSQL privilege boundary under which the AuthService runtime cannot INSERT, UPDATE or DELETE either BAR table, and the governed deployment-time operation is the controlled BAR write authority. **Evidence finding (not a completed prerequisite):** `scripts/run_bootstrap.py` uses the same `db_manager` / `DATABASE_URL` connection pattern as the runtime, so a separate write-capable deployment connection does not yet exist. No role provisioning is claimed | **REQUESTED / NOT PROVIDED** |
| EP-03 | Controlled read-only reconciliation access: environment-scoped, controlled read-only access sufficient for reconciliation, with no write capability. No access is claimed to exist | **REQUESTED / NOT PROVIDED** |
| EP-04 | PostgreSQL verification environment: a PostgreSQL-capable environment or fixture sufficient for the R4 verification plan, using the existing CI PostgreSQL capability where appropriate. **CI/test PostgreSQL is distinct from canonical production PostgreSQL** and does not satisfy EP-01/C-10 | **REQUESTED / NOT PROVIDED** |

**Boundary:**
- These are external-prerequisite **requests**. None has been provided, and no infrastructure has been provisioned through the repository.
- **C-07, C-09 and C-10 remain not satisfied (no PASS).** No R3 criterion is satisfied by issuing a request.
- **R3: NOT SATISFIED; NOT READY FOR R3 ACCEPTANCE REVIEW. TD-171: OPEN.**

---

~~*End of IMP-REPORT-WP-23 (A–C tranche). IMPLEMENTATION COMPLETE — AWAITING INDEPENDENT VERIFICATION. WP-23 OPEN. Nothing staged, committed or pushed.*~~

~~*End of IMP-REPORT-WP-23 (A–C tranche). Synchronized 2026-09-28 (ST-7): IMPLEMENTATION COMPLETE — INDEPENDENTLY VERIFIED (Gates 1, 2 and 4) — GATE 5 PASS WITH CONDITIONS (C-1 and C-2 being remediated). NOT ACCEPTED, NOT CERTIFIED, NOT COMMITTED. WP-23 OPEN. WP-BAE-001 M2 NOT AUTHORIZED and NOT STARTED.*~~

*End of IMP-REPORT-WP-23 (A–C tranche). C-3 addendum 2026-09-28: IMPLEMENTATION COMPLETE — INDEPENDENTLY VERIFIED (Gates 1, 2 and 4) — GATE 5 PASS WITH CONDITIONS (C-1 and C-2 completed, C-3 satisfied, C-4 outstanding) — **ACCEPTED** (`IRA-WP-23-AC §0.2`) and committed with that record. NOT CERTIFIED, NOT CLOSED. WP-23 OPEN; Workstreams D–H not implemented. WP-BAE-001 M2 NOT AUTHORIZED and NOT STARTED.*

*(2026-09-30 addendum.) TD-171 remediation tranche (Charter §21a): ACCEPTED (R1); AUTHORIZED (R2, `d2aaade`); R3–R6 NOT SATISFIED; implementation not started; TD-171 OPEN. M2 NOT AUTHORIZED / NOT STARTED; M2-P CHARTERED / NOT AUTHORIZED / NOT STARTED.*

*(2026-09-30 addendum, R3 design synchronization.) OD-1, OD-2, OD-3 and OD-5 DESIGN DECIDED (`fa93fc7`, `649f55a`); OD-4 OPEN / EXTERNAL. R3 NOT SATISFIED / NOT READY FOR R3 ACCEPTANCE REVIEW. Nothing implemented. TD-171 OPEN.*

*(2026-09-30 addendum, external prerequisites.) Request package issued to Platform Engineering (`7a3b639`). EP-01 to EP-04 REQUESTED / NOT PROVIDED. R3 NOT SATISFIED / NOT READY FOR R3 ACCEPTANCE REVIEW. TD-171 OPEN.*
