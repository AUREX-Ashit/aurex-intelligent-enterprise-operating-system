# CERT-WP-23-AC — Gate 1 Independent Certification: Enterprise BAR Workstreams A–C Tranche

**Gate:** `CLAUDE.md §19.7` / `§19.7b` Gate 1 (Independent Certification), for the WP-23 Workstreams A–C tranche under RD-23-02.
**Date:** 2026-09-25
**Verdict:** **GATE 1 STOP — a governance blocker requires a Repository Owner decision (CERT-F-01).** Other findings are listed in §5. Two of them (CERT-F-02 and CERT-F-03) also block acceptance independently of the STOP.

---

## 1. Reviewer Independence

I am a fresh-context reviewer. I had no role in implementing Workstreams A–C, in writing `IMP-REPORT-WP-23`, `IRA-WP-23-AC`, `ROD-WP-23-AC` or any other WP-23 governance document, or in any earlier gate. I re-derived every material claim from source, from command output and from my own probes. I did not accept any claim in the implementation report, the closure-readiness assessment or the decision records as evidence. The stale statements S-1 to S-12 (`IRA-WP-23-AC §7`) played no part in any conclusion.

## 2. Sources Actually Read

- **Code** (under `Backend/Services/AuthService/`), read in full:
  - `models/bar_identifier_ledger.py`, `repositories/bar_identifier_repository.py`, `services/bar_identifier_service.py`, `alembic/versions/2026_09_22_0900-a7b8c9d0e1f2_bar_identifier_ledger.py`, `tests/test_bar_identifier_service.py`;
  - `models/bar_registration.py`, `repositories/bar_registration_repository.py`, `services/bar_registration_service.py`, `alembic/versions/2026_09_22_1000-b8c9d0e1f2a3_bar_registration.py`, `tests/test_bar_registration_service.py`;
  - `models/__init__.py` (working-tree diff) and `tests/conftest.py`.
- **Governance:**
  - `BAR-INDEX.md` and `IMP-REPORT-WP-23_Enterprise_BAR_Mechanism.md`, both in full;
  - WP-23 Charter, in full (including §7, §20, §21 and the §22 RD-23-02 note);
  - `IRA-WP-23-AC` §0–§10, in full;
  - `ROD-WP-23-AC-BAR-Registry-Authority-Decision-Preparation.md`, in full;
  - `ENTERPRISE-BAR-MECHANISM-DESIGN-AND-IMPLEMENTATION-READINESS.md` §4–§10, §14–§19 and §19a.6;
  - `ROD-ENTERPRISE-BAR-Decision-Preparation.md` §0b (D2), §0d (D5) and §0f (D7);
  - `IRA-BAE-001-M2` §0 header and decision table;
  - `TECH-DEBT.md` (TD-096 entry);
  - the WP-23 row of `WPR-001`;
  - `CLAUDE.md` §16–§21.
- **Leakage check:** `Backend/Runtime/BusinessActivityEngine/` (package listing, `tests/test_package_boundary.py`).

## 3. Method

1. **Git state.** `git status --short`, `git ls-files` and `git log` for every object-list file and for both parent migrations. I also inspected commit `8323bf3` with `git show --stat`.
2. **Alembic.** Read-only `alembic heads` and `alembic history`. I rendered offline SQL with `alembic upgrade f6a7b8c9d0e1:head --sql` and `alembic downgrade head:f6a7b8c9d0e1 --sql`; this needs no database. I compared that SQL with the model DDL, compiled for the PostgreSQL dialect in a scratch script.
3. **Tests.** I re-ran both BAR test files myself, then the full AuthService suite (with `JWT_SECRET_KEY`/`JWT_ALGORITHM` set to the CI test values, per TD-010).
4. **Probes.** I wrote five purpose-built probes of my own, not adapted from the suite: collision-path instrumentation, retry-then-succeed, FK with and without `PRAGMA foreign_keys=ON`, the CHECK constraint, and caller pending-work loss. They ran against fresh in-memory SQLite engines. Probe scripts are kept in the session scratchpad only.
5. **Repository-wide searches.** For BAR symbols, `bae_integration`, `BA-NNNNNN` tokens, and WP-23 status labels.

## 4. Gate 1 Checklist

| # | Item | Evidence | Result |
|---|---|---|---|
| 1 | Scope matches authorization | **What is absent.** No router, schema, endpoint or adapter references BAR: repository-wide grep of `Backend/` finds BAR symbols only in the ten object-list files, `models/__init__.py`, and a negative boundary test in BAE. There is no discovery query, execution gate, cutover or C-024 code. `bar_registration` has exactly the eight design-§4 fields plus `id`. **What is present.** Runtime tables, services and migrations were built for B and C, while Charter §21 row C reads "governance-only, no runtime" | **STOP**: see §4.1 and CERT-F-01. D/E/F/H exclusions: PASS |
| 2 | RD-23-01 commit order | **Committed:** the last committed migration is `d4e5f6a7b8c9` (c132). **Untracked:** `e5f6a7b8c9d0` (c021, WP-20) and `f6a7b8c9d0e1` (c022, WP-21), plus their models and repositories. Commit `8323bf3` ("close C-021") contains governance docs only. **Chain:** `d4e5f6a7b8c9 → e5f6a7b8c9d0 → f6a7b8c9d0e1 → a7b8c9d0e1f2 → b8c9d0e1f2a3` | **FAIL** (prerequisite not met): CERT-F-02 |
| 3 | RD-23-02 closure-unit treatment | No artifact labels WP-23 as a whole COMPLETE, CLOSED or CERTIFIED. `BAR-INDEX.md:106-117`, the IMP-REPORT (lines 13, 111) and Charter §22 note (lines 181-184) all state WP-23 OPEN, D and E not implemented, and a terminal state of ACCEPTED. The `WPR-001` WP-23 row reads "CHARTERED — IMPLEMENTATION NOT YET COMPLETED". The Charter is untracked, so git cannot prove that the §22 note left other text unaltered. The note is self-contained and I found no contradiction with other Charter text | **PASS with observation.** Committed text "WP-23's own already-completed gates for Workstreams A–C" at `BAR-WP23-WORKSTREAM-D-…-INVESTIGATION.md:198` is outside the S-inventory: CERT-F-11 |
| 4 | RD-23-03 layered model represented | `BAR-INDEX.md §1` (lines 16-21), §2 D8, §3 and §4 correctly reflect Option D. The IMP-REPORT (lines 8-12) and `IRA-WP-23-AC §0` do too. The runtime docstrings contradict it: `models/bar_registration.py:38-39` and `services/bar_registration_service.py:12-14` both claim authority. `BAR-INDEX.md §8` still describes the index row as the act that assigns the identifier and is collision-checked against the index | **FAIL**: CERT-F-03 (docstrings). Low: CERT-F-10 (§8) |
| 5 | Report completeness and accuracy | Every object-list file is listed in IMP-REPORT lines 35-55. Its claims re-verified: field list, allocator, one-flush atomicity, test counts, 972 regression, single head, and DD-1 to DD-10 match source. The DD-7 and DD-9 behaviours were confirmed by probe. Inaccuracies: design §19 row B/C annotations (cited by the report's evidence trail) claim a "forced UNIQUE-collision retry" test, but that test produces no collision (CERT-F-05). IMP-REPORT line 43 omits the UNIQUE constraint the migration creates | **PASS with observations** |
| 6 | Migrations and ancestry | `alembic heads` returns a single head, `b8c9d0e1f2a3`. The chain is intact. Both upgrades are `create_table` plus `create_index` only; there is no ALTER. Each downgrade drops the index and then the table, the exact reverse. Model-to-migration parity is covered item by item in §4.2 | **PASS**. Parity: functional match, structural drift (CERT-F-08) |
| 7 | Tests and evidence | My run: BAR files **22 passed** (9 + 13) in 7.7 s. Full AuthService suite: **972 passed, 0 failed** (481 s). The harness uses SQLite `:memory:`, builds the schema with `create_all` (so migrations are not exercised), and has no FK pragma (`tests/conftest.py:30-32`, TD-096). The assertion audit found two "forced collision" tests that never collide (probe P1: 0 rollbacks), two placeholder tests that assert only `test_engine is not None`, and one static-constant test | **PASS (green)** with CERT-F-05, CERT-F-06 and CERT-F-13 |
| 8 | BAR-INDEX status, Register, identifiers | §3 Register holds one placeholder row, `*(no entries)*`. The `BA-000089` example sits in §6, outside the Register. A repository-wide `BA-0\d{5}` search finds only illustrative constitutional examples, tests, BAE contract tests and governance prose. No real Business Activity is registered and no identifier is assigned. Status table lines 108-119 are accurate | **PASS** (Low: CERT-F-10) |
| 9 | No Workstream D/E leakage | No discovery, query surface consumer, gate or feature flag exists. `get_by_identifier` is a plain repository read with no caller | **PASS** |
| 10 | No WP-BAE-001 M2 leakage | There is no `bae_integration` directory or module. `business_activity_engine/` contains M1 files only and has no working-tree changes. The BAE's only BAR reference is the negative boundary test `test_package_boundary.py:52-60`. No BAR→BAE adapter exists | **PASS** |
| 11 | Stale-statement non-reliance | No conclusion here cites S-1 to S-12 | **PASS** |
| 12 | Tenant isolation (§21.4) | Neither table has an organization or tenant column (rendered DDL, §4.2). Both hold platform-global metadata. No router or endpoint exists. §21.4 (a)–(c) attach only to "a new endpoint whose underlying data model carries an organization/tenant boundary". Neither condition holds, so the checklist does not attach | **PASS** |

### 4.1 Mandatory special inspection: Charter §21, Workstream C

**The Charter says:**
- **§7:** Workstream C is "a registering-act convention mirroring the CBOR-ADR pattern — a discrete, Repository-Owner-authorized act per Business Activity … This Charter authorizes **building** this mechanism".
- **§21 row C** (line 168): "Registering-act convention (design §7)"; test expectation "Governance-artifact review per act"; containment "**Low risk — governance-only, no runtime**".
- **§21 row D** (line 169): "Moderate — **first runtime component**". This implies that no workstream before D, including B, is a runtime component.
- **§20:** authorizes Workstreams A–G "as specified in `ENTERPRISE-BAR-…-READINESS.md` and this Charter".

**The design says:**
- **§6** leaves the existence of a database-backed runtime store "**not decided here** … a downstream engineering decision within **Workstream C/D** (§18), not fixed now".
- **§18** lists the runtime store as "not yet built", with the registration flow ending in "(optionally) propagate to a runtime store".
- **§19 row C** carries the same "governance-only, no runtime" wording. It now sits beside the implementer's own "IMPLEMENTED … migration `b8c9d0e1f2a3`" annotation in the same cell, so that cell contradicts itself.
- **D5** (`ROD-ENTERPRISE-BAR §0d`): BAR "creates and controls the identifier internally". This is consistent with, but does not mandate, a runtime issuer.

**What RD-23-03 decides** (`ROD-WP-23-AC §0`):
- It assigns "the persistent `bar_registration` table" the Layer-2 runtime-registration role.
- It forbids schema changes (§0.2).
- It states: "**The decision establishes the authority model only.**"
- It does not state that building the table under Workstream C was authorized, and it does not amend or annotate Charter §21 row C or row D.
- The preparation analysis in the same document (§6, Option D, "Needs an ADR" row) says Option D requires "settling the Charter §21 row C wording". §0.3 rejects the ADR requirement but does not settle that wording.
- The implementer's own report agrees: "the RD-23-03 decision does not settle it" (IMP-REPORT line 72), and "No separate per-workstream RO authorization record for B or C was found" (line 26).

**Classification: (c) — a genuine governance problem requiring a Repository Owner decision.**

Reasoning:
- **Not (b).** The implementation does not plainly exceed authorization. Design §6, which Charter §20 incorporates, expressly delegated the runtime-store question to Workstream C/D. RD-23-03 later placed the built table in the authority model.
- **Not (a).** Classifying it as a mere documentation inaccuracy would require me to rule that design §6's delegation overrides the Charter's more specific row C, and implicitly row D. That means resolving a conflict between two governing texts by interpretation, which `CLAUDE.md §16`/`§17` prohibit.
- **RD-23-03 assigns a role; it does not authorize past construction.** It says it "establishes the authority model only". The step its own analysis identified for Option D, settling the row C wording, was never taken.

The open question is therefore narrow, but it is real: was building runtime persistence under Workstreams B and C authorized? It needs an explicit Repository Owner act, for example ratification of the construction plus an authorized, dated correction note on Charter §21 rows C and D and design §19 row C. Gate 1 cannot certify checklist item 1 without that act.

### 4.2 Model ↔ Migration Parity (item by item)

| Object | Model (`create_all`, PostgreSQL-compiled) | Migration (offline SQL) | Result |
|---|---|---|---|
| Ledger columns: `id` UUID NN, `identifier` VARCHAR(20) NN, `issued_at` TIMESTAMPTZ NN | Same | Same | Parity |
| Ledger defaults | Python-side only (`uuid4`, `now(utc)`); no server default | None | Parity |
| Ledger PK | Unnamed | `pk_bar_identifier_ledger` | Name drift |
| Ledger uniqueness on `identifier` | `unique=True, index=True` compiles to one `CREATE UNIQUE INDEX ix_bar_identifier_ledger_identifier` | A named `UNIQUE` constraint `uq_bar_identifier_ledger_identifier` plus a separate non-unique index `ix_bar_identifier_ledger_identifier` | Structural drift, semantically equivalent; the migration has a redundant index |
| Registration columns (9), types, nullability | Same | Same | Parity |
| `registration_status` server default `'REGISTERED'` | Present | Present | Parity |
| `ck_bar_registration_status` | `registration_status = 'REGISTERED'` | Same | Parity |
| `uq_bar_registration_wp_reference` | `(owning_work_package, business_activity_reference)` | Same | Parity |
| Registration UNIQUE `identifier` | Unnamed | `uq_bar_registration_identifier` | Name drift |
| Registration FK → `bar_identifier_ledger.identifier` | Unnamed | `fk_bar_registration_identifier` | Name drift |
| `ix_bar_registration_identifier` | **Absent** | Present (redundant with the UNIQUE constraint) | Drift |

## 5. Findings

The rubric is `CLAUDE.md §19.8.7` together with `§19.8.5`. "Blocks acceptance" refers to RO acceptance of the A–C tranche (P-9).

| ID | Severity | Description | Evidence | Blocks acceptance |
|---|---|---|---|---|
| CERT-F-01 | **High** (governance) | The authorization status of runtime persistence (tables, services, migrations) built under Workstreams B and C is unresolved. Charter §21 row C says "governance-only, no runtime" and row D says D is the "first runtime component". Design §6 delegated the runtime store to C/D. RD-23-03 assigns a role but "establishes the authority model only", and the row C wording remains unsettled. Classification (c) | Charter lines 7, 20, 168-169; design §6, §19 row C; `ROD-WP-23-AC` §0, §0.2, §6; IMP-REPORT lines 26, 72 | **Yes — STOP. RO decision required** |
| CERT-F-02 | **High** | RD-23-01 prerequisite not met. Parent migrations `e5f6a7b8c9d0` and `f6a7b8c9d0e1`, with their C-021 and C-022 code, are untracked. Committing BAR now would leave `alembic upgrade` broken on a clean checkout. All WP-23 governance documents are untracked as well. This blocks the commit (P-10) and therefore §19.7 completion, but not this review | `git ls-files` / `git status`; `alembic history`; `git show --stat 8323bf3` | **Yes** (commit and acceptance chain) |
| CERT-F-03 | **Medium** | Runtime docstrings contradict the decided RD-23-03 layered model. The table claims to be "the authoritative persisted record of Business Activity registration". The service claims "this mechanism … is the authoritative registration act". This is an architecture-conformance defect inside the object under review (§19.8.5: not deferrable). The ROD's own analysis (§7) says closure requires the chosen option's text corrections | `models/bar_registration.py:38-39`; `services/bar_registration_service.py:12-14` | **Yes** |
| CERT-F-04 | **Medium** | GAP-23-03-1 and GAP-23-03-2 are confirmed. `register()` accepts any non-blank free-text `registering_act`. It performs no caller-authority check, and `actor_id` is optional. No reconciliation exists between the table and `BAR-INDEX.md`. RD-23-03 §0.2 expressly does not authorize fixing this now, and nothing consumes the table today. It becomes a security and authority boundary (fail-open for governance) once Workstream E or BAE M2 reads `bar_registration` for eligibility. It must be entered in `TECH-DEBT.md`; it is currently unrecorded (IMP-REPORT line 100) | `services/bar_registration_service.py:100-134, 229-244` | No, if registered as TD with the condition that it closes before any execution-eligibility consumer is built |
| CERT-F-05 | **Medium** | Two tests do not test what their names claim. `test_forced_collision_is_retried_not_duplicated` and `test_forced_identifier_collision_is_retried_without_duplicate_or_half_registration` pre-seed `BA-000001`, but the allocator computes `MAX+1` = `BA-000002`, so no collision occurs. Probe P1 measured 0 rollbacks in both. The retry-then-succeed branch is therefore untested by the suite; only the exhaustion path exercises `except IntegrityError`. My probe P2, with a real collision, showed issuance retries correctly (`BA-000005` pre-seeded and forced, `BA-000006` issued). The registration-path equivalent is left to Gate 2 | `tests/test_bar_identifier_service.py:111-131`; `tests/test_bar_registration_service.py:238-262` | No (TD). The evidence claims in the report and design annotations should be corrected |
| CERT-F-06 | **Medium** | The harness does not enforce FKs and does not exercise the migrations. Tracked as **TD-096** (Open). Probe P3: an orphan `bar_registration` row is **accepted** without the pragma and **rejected** with `PRAGMA foreign_keys=ON`, so the FK itself is correct. Probe P4: the CHECK constraint rejects `PENDING` | `tests/conftest.py:30-32`; TD-096 | No (tracked as TD-096). Gate 2 must still probe under enforcement |
| CERT-F-07 | **Medium** | On `IntegrityError`, both services call `session.rollback()`, which silently discards the caller's unrelated pending work. Probe P5: a pending caller object (`BA-000777`) vanished and no error was raised. The issuance docstring does not state this consequence for callers. There is no caller today. Must be dispositioned at Gate 2 (G2-7). If it is classified as a data-integrity defect, §19.8.5 forbids deferral | `services/bar_identifier_service.py:110-113`; `services/bar_registration_service.py:167-169` | **Yes, pending Gate 2 disposition** |
| CERT-F-08 | **Low** | Model/migration structural drift: constraint names, a redundant non-unique index on the ledger, and an extra `ix_bar_registration_identifier` that is not in the model (§4.2). Functionally equivalent, but Alembic autogenerate would report drift | §4.2 | No (TD) |
| CERT-F-09 | **Low** | Unsupported citation. The model docstring quotes design §19a.6: "issuance is an internal capability of the registration mechanism, not an independent registration event". That text exists nowhere in the repository except this docstring. The migration docstring repeats the attribution (`§19a.6`) | `models/bar_identifier_ledger.py:36-40`; migration `a7b8c9d0e1f2` lines 34-37 | No. Correct it in the CERT-F-03 docstring pass |
| CERT-F-10 | **Low** | `BAR-INDEX.md` accuracy. §4 claims to reproduce design §19a.6 "exactly", but §19a.6 is a three-state table and §4 lists five concepts. §8 (amendment procedure) is not updated for Option D. The line 18 parenthetical "unchanged from the paragraph above" points at the struck-through paragraph | `BAR-INDEX.md:18, 60-62, 98` | No |
| CERT-F-11 | **Low** | The stale-statement inventory is incomplete. Committed text says "WP-23's own already-completed gates for Workstreams A–C", which is not among S-1 to S-12 | `BAR-WP23-WORKSTREAM-D-BUSINESS-ACTIVITY-ENGINE-PREREQUISITE-INVESTIGATION.md:198` | No. Add it to the P-11 reconciliation |
| CERT-F-12 | **Low** | Governance text defects. The Charter cites §29 and §31, which do not exist (it has 23 sections). The `IRA-WP-23-AC` header (lines 5, 8) still says Gate 1 "cannot be dispatched", while §10 records dispatch | Charter lines 11, 21, 202; `IRA-WP-23-AC:5-8` vs `:325` | No |
| CERT-F-13 | **Low** | Non-evidential tests are counted in the "9/9" and "13/13" totals. Two tests assert only `test_engine is not None`; one asserts only module constants | `test_bar_identifier_service.py:164-193`; `test_bar_registration_service.py:333-362, 388-399` | No |
| CERT-F-14 | **Low** | The allocator is duplicated in two services (DD-5, disclosed; "one business rule, one implementation"). There is no guard against width overflow at `BA-999999` (DD-9, disclosed) | `bar_identifier_service.py:139-141`; `bar_registration_service.py:225-227` | No (TD) |

## 6. Overall Verdict

**GATE 1 STOP — a governance blocker requires a Repository Owner decision.**

- **Clean results:**
  - The tranche is functionally green: 22/22 BAR tests and 972/972 in the full suite, on my own re-run.
  - The migrations form a single additive head and each reverses cleanly.
  - No Workstream D, E, F or H code and no M2 or BAE leakage exists.
  - No real Business Activity is registered and no identifier is assigned.
  - §21.4 does not attach.
- **What blocks certification:**
  - Scope conformance (item 1) cannot be certified while CERT-F-01 is unresolved.
  - Independently of that STOP, acceptance also requires three things:
    - CERT-F-02: the RD-23-01 prerequisite commits;
    - CERT-F-03: docstring conformance to RD-23-03, which is remediation under §19.7b gates 3–4;
    - CERT-F-07: the Gate 2 disposition.
  - CERT-F-04, -05, -06, -08 and -14 must be recorded in the Technical Debt Register (or cross-referenced to TD-096) before acceptance.
- **Re-submission:** Gate 1 can be re-run, or narrowly resumed, once the Repository Owner resolves CERT-F-01.

## 7. Integrity Statement

- **What I ran:**
  - `git status`, `ls-files`, `log` and `show --stat`, all read-only;
  - `alembic heads`, `history` and offline `--sql` renders, which need no database connection;
  - `pytest` on the two BAR files and on the full AuthService suite;
  - a model-DDL compile script and a from-scratch probe script (P1–P5) against private in-memory SQLite engines.
- **Where scratch files are:** under the session scratchpad `…\scratchpad\gate1\` only (`model_ddl.py`, `probe_g1.py`, `full_suite.txt`).
- **What I changed:** only this file, `architecture/06-Reviews/CERT-WP-23-AC_BAR_Workstreams_A-C.md`. No code, test, migration or governance document was modified. Nothing was staged, committed, stashed or pushed.
- **Git check:** `git status --short` was checked before and after. The only new entry is this file, and `git diff --cached --name-only` is empty.
