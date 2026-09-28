# VV-AUDIT-WP-23-AC (Gate 4) — Independent Verification of Remediation: Enterprise BAR Workstreams A–C

**Gate:** CLAUDE.md §19.7b Gate 4 (Independent Verification of Remediation)
**Object under review:** the WP-23 A–C Gate 3 remediation of **VV-F-01** (High), **VV-F-02** (Medium) and **CERT-F-03** (Medium), as described in `IMP-REPORT-WP-23_Enterprise_BAR_Mechanism.md` § "A–C Tranche — Gate 3 Remediation".
**Date:** 2026-09-26
**Verdict:** **GATE 4 — PASS, subject only to any separately identified Gate 1 prerequisites or closure conditions.**

Gate 4 is not the acceptance authority. This record does **not** accept, certify or close WP-23 A–C. Gate 1 items outside the Gate 3 scope (for example CERT-F-02, the RD-23-01 prerequisite commits) remain as recorded by Gate 1, and §19.7b Gate 5 (Release Readiness Audit) is still required.

---

## 1. Independence Statement

A fresh-context reviewer wrote this record. The reviewer took no part in implementing WP-23 A–C, in Gate 1 (Certification), in Gate 2 (V&V Audit) or in the Gate 3 remediation.

No document was treated as evidence because of what it says, including the Gate 3 section of the IMP-REPORT. Every material claim was re-derived from source and from runtime probes written from scratch for this gate (`probes_g4.py`, `probe_p3e_g4.py`, `probe_conc_g4.py`). The negative-control loader (`run_in.py`) is independent of the implementer's `gate3/prefix_preload.py`; that helper was read but not used. The implementer's 10 new tests were read to understand them, run for regression counts, and run once against the pre-fix code as a second negative control. They were **not** adapted into probes and do not carry any conclusion here.

## 2. Environment and Engine Configurations

| Item | Value |
|---|---|
| Python / libraries | `Backend/Services/AuthService/venv`: CPython 3.14.5, SQLAlchemy 2.0.50, aiosqlite 0.22.1, SQLite 3.50.4 |
| PostgreSQL | **Not available.** `psql` and `pg_ctl` are absent, and `docker info` failed: `failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine`. No service was installed or started. **All PostgreSQL/asyncpg behaviour is UNVERIFIED (§8).** |
| Scratch location (`$G`) | `C:\Users\ashit\AppData\Local\Temp\claude\C--Ashit-corpstage-enterprise-operating-system\a7a13f8c-d9da-479f-b7b3-b6b4826d4e72\scratchpad\gate4\` |
| Schema for file-DB probes | `$G/golden_head.db`, copied from Gate 2. Its SHA-256 (`6d21a1e6…e8ba509`) matches Gate 2's copy. Its BAR tables were built by the real BAR migrations |
| Env vars | `PYTHONDONTWRITEBYTECODE=1`. For pytest, `JWT_SECRET_KEY=ci-test-secret-key-not-for-production JWT_ALGORITHM=HS256` (TD-010) |

Every probe was run under three engine configurations. The results differ between them in one respect, which matters (G4-O-01).

| Config | Definition | FK positive control |
|---|---|---|
| **recipe** | File DB with `PRAGMA foreign_keys=ON` on every connection. Applies SQLAlchemy's documented pysqlite SAVEPOINT recipe: `dbapi_conn.isolation_level = None`, plus `BEGIN` emitted on the SQLAlchemy `begin` event. **This is the configuration whose transactional evidence is trustworthy.** It matches how SQLAlchemy drives PostgreSQL: an explicit `BEGIN` precedes any `SAVEPOINT` | `PRAGMA foreign_keys=1`. An orphan `bar_registration` insert was **REJECTED: FOREIGN KEY constraint failed** (probe FK0). Each file-DB probe also asserts `fk=1` inside its own session |
| **legacy** | Same file DB and FK=ON, but pysqlite's default legacy implicit-`BEGIN` handling. This is the shape of Gate 2's `probe_batch_loss.py` and of the implementer's post-fix run of it | `PRAGMA foreign_keys=1`; orphan insert REJECTED |
| **harness** | Exact replica of `tests/conftest.py`: `sqlite+aiosqlite:///:memory:`, `create_all`, no FK pragma, legacy transactions. Used **only** to compare transaction behaviour. It is not FK evidence | `PRAGMA foreign_keys=0`; orphan insert **ACCEPTED**. This confirms TD-096 / VV-F-03 still stand |

**Why the configuration matters.** In the legacy and harness configurations, pysqlite does not open a transaction for `SELECT`. As a result, a `SAVEPOINT` that is the first write-related statement of a caller's transaction *starts* an SQLite transaction, and the matching `RELEASE` **commits** it. The recipe configuration does not have this distortion. See §5 and G4-O-01.

## 3. Sources Read

- **Code** (`Backend/Services/AuthService/`):
  - services: `bar_identifier_service.py`, `bar_registration_service.py`;
  - repositories: `bar_identifier_repository.py`, `bar_registration_repository.py`, `base_repository.py`;
  - models: `bar_registration.py`, `bar_identifier_ledger.py`, `database.py`, and the `config.py` DB-URL handling;
  - migrations: `alembic/versions/2026_09_22_0900-a7b8c9d0e1f2_bar_identifier_ledger.py`, `…1000-b8c9d0e1f2a3_bar_registration.py`;
  - tests: `test_bar_identifier_service.py`, `test_bar_registration_service.py`, `test_bar_transaction_safety.py`, `conftest.py`.
- **Findings and claims:**
  - `VV-AUDIT-WP-23-AC_BAR_Workstreams_A-C.md` (Gate 2);
  - `CERT-WP-23-AC_BAR_Workstreams_A-C.md` (Gate 1: CERT-F-03, F-05 and F-09 rows, criterion 4);
  - `IMP-REPORT-WP-23_Enterprise_BAR_Mechanism.md` (Gate 3 section).
- **Authority model:**
  - `ROD-WP-23-AC-BAR-Registry-Authority-Decision-Preparation.md` §0 (RD-23-03, Option D);
  - `IRA-WP-23-AC_BAR_Workstreams_A-C_Closure_Readiness.md` header, §0 and §0.1 (RD-23-04);
  - `WP-23_Enterprise_BAR_Mechanism_Implementation_Charter.md` (existence and mtime only);
  - `BAR-INDEX.md` §3.
- **Governance:** CLAUDE.md §19.7b, §19.8.5, §19.8.7.
- **Scratch evidence** (read-only): `prefix_snapshot/` with `SHA256SUMS`; `gate2/probe_batch_loss.py`, `probes.py`, `probes_output.txt`, `pg_offline_upgrade.sql`, `BAR-INDEX.before.md`; `gate3/prefix_preload.py`, `run_probe.py` (inspected, not used); `status-before-gate4.txt`, `status-after-gate3.txt`.

## 4. Negative-Control Evidence (pre-fix vs current)

### 4.1 Establishing the pre-fix code

- **Git cannot supply it.** All BAR files are **untracked** (`git status`: `??`), so git history holds no pre-fix version.
- **Snapshot integrity.** Recomputed SHA-256 of the three files in `prefix_snapshot/`:
  - `bar_identifier_service.py` = `84eb665d…f17f`
  - `bar_registration_service.py` = `4241233a…6853`
  - `models/bar_registration.py` = `b7258437…e2dc`

  All three equal the values in `SHA256SUMS`, which were recorded against the repository paths. The snapshot mtime (2026-09-26 00:01:20) precedes every Gate 3 edit to the repository files (00:03:00 to 00:03:55).
- **Content matches the Gate 1 and Gate 2 descriptions of the defective code.**
  - The snapshot has `await self.identifier_repo.session.rollback()` (identifier service line 112) and `await self.registration_repo.session.rollback()` (registration service line 169). These are the whole-session rollbacks that Gate 2 identifies as the VV-F-01 cause.
  - `models/bar_registration.py:38-39` reads "this table … is the authoritative persisted record". The registration service at lines 13-14 reads "is the authoritative registration act", and at line 81 "Canonical Business Activity registration authority". These are exactly the lines CERT-F-03 cites.
- **Behavioural fingerprint.** Gate 2's own `probes.py` was run against the snapshot services (`$G/g2fp_prefix/out.txt`) and normalized for UUIDs and timestamps. The output is **identical** to Gate 2's recorded `probes_output.txt` except P8a/P8b, whose interleaving of two concurrent threads is nondeterministic (the same outcomes, in swapped order). This is strong evidence that the snapshot is the code Gate 2 tested.
- **Diff snapshot → current.** The differences are exactly:
  - both services: an up-front `session.flush()`; `session.rollback()` replaced by `async with session.begin_nested()`; the `is_issued` classification with a `FAILED` audit and a bare `raise`;
  - docstring and comment text in the three files.

  `models/bar_registration.py` is identical except for docstring text: an AST comparison with string expressions stripped was **identical**, and the compiled DDL (PostgreSQL and SQLite, 48 lines) was **identical**.
- **Gap (G4-O-02).** `repositories/bar_identifier_repository.py` was also modified by Gate 3 (mtime 00:03:00; new `is_issued()`), but it was **not snapshotted**, so no byte-level pre-fix copy exists. The pre-fix services never call `is_issued`. The fingerprint run above used the *current* repository with the pre-fix services and reproduced Gate 2's output exactly. The repository change is therefore behaviour-neutral for everything Gate 2 exercised. The remaining methods (`max_identifier_sequence`, `count_issued`) match Gate 2's description (fixed-offset `substr`).

### 4.2 Loader

`$G/run_in.py` puts a full scratch copy of the AuthService source first on `sys.path`: `$G/prefix_tree` has the three snapshot files overlaid, and `$G/current_tree` is a byte-identical copy of the repository, confirmed by `diff -r`. Before running each probe, the loader prints the loaded file path, its SHA-256 and marker strings.
- **Pre-fix run:** `sha256=84eb665d…` and `4241233a…`, `session.rollback()=True`, `begin_nested=False`.
- **Current run:** `2939bc04…` and `99ae6677…`, `session.rollback()=False`, `begin_nested=True`.

### 4.3 Results

| Scenario | PRE-FIX | CURRENT |
|---|---|---|
| Gate 2 `probe_batch_loss.py`, collision variant (legacy config, as authored) | **Reproduced.** first=`BA-000002`, second=`BA-000002`, "same identifier handed out twice: True". After commit only `('BA-000002','Second BA')` survives | first=`BA-000002`, second=`BA-000003`. Both survive; not handed out twice |
| Same probe, duplicate-race variant | **Reproduced.** "New BA" lost; only `('BA-000001','Existing BA')` remains | `AlreadyExists` raised, and "New BA" (`BA-000002`) survives |
| G4 A2: 2nd registration collides with the 1st registration's own *uncommitted* ledger row (recipe) | **FAIL.** first=`BA-000001`, second=`BA-000001`, same_id_twice=True. After commit `[('BA-000001','G4 Second')]`; the first object is no longer persistent | **PASS.** `BA-000001` / `BA-000002`. Both committed |
| G4 A1: flushed and pending unrelated caller work, then a collision (recipe) | **FAIL.** domains after commit = `[]` | **PASS.** Both domains survive |
| G4 C2-check: non-collision CHECK violation (recipe) | **FAIL.** 5 attempts, then `BarRegistrationAllocationExhausted`, audit DENIED "exhausted" | **PASS.** 1 attempt; original `IntegrityError` re-raised; audit FAILED |
| Implementer's 10 new tests (run from the scratch trees) | 7 of the 10 new tests failed (defect-targeting tests 2, 3, 4, 5, 7, 8, 9); 3 passed | 10 of 10 passed |

The negative control is **valid**: the pre-fix code reproduces the historical VV-F-01 and VV-F-02 failures under every configuration (recipe, legacy and harness), and the current code does not. In the tree runs, 2 other tests also failed, identically for both trees: `test_*_does_not_touch_bar_index_md`. They fail only because they resolve `BAR-INDEX.md` relative to the relocated scratch tree, and they pass in-repo (§6).

## 5. Probe Table

Command form (from `$G`): `venv/Scripts/python.exe run_in.py <prefix_tree|current_tree> <script> [args]`. Outputs: `$G/out_<tree>_<config>.txt`, `$G/nc_batch_{prefix,current}.txt`, `$G/out_p3e.txt`, `$G/g2fp_{prefix,current}/out.txt`.

Every forced collision is a **genuine database UNIQUE violation**. Its error text was captured from the engine's `handle_error` event, for example `UNIQUE constraint failed: bar_identifier_ledger.identifier`. The emitted `SAVEPOINT` / `ROLLBACK TO SAVEPOINT` / `RELEASE SAVEPOINT` / `BEGIN` statements and DBAPI commits and rollbacks were captured by `before_cursor_execute`, `commit` and `rollback` listeners. "No hidden commit" was checked with an **independent `sqlite3` connection**, which can see only committed data.

| ID | Purpose (req.) | Script / args | Observed (CURRENT, recipe) | Classification |
|---|---|---|---|---|
| FK0 | FK positive control | `probes_g4.py <cfg>` | recipe and legacy: fk=1, orphan REJECTED. harness: fk=0, ACCEPTED | PASS (control) |
| A1 | Unrelated flushed **and** pending caller work survives a registration collision; no hidden commit; commit persists (A.1, A.4, A.5, A.7) | `probes_g4.py recipe` | SQL `INSERT domains → SAVEPOINT sa_savepoint_1 → INSERT bar_identifier_ledger → ROLLBACK TO SAVEPOINT → SAVEPOINT sa_savepoint_2 → INSERT ledger → INSERT bar_registration → RELEASE SAVEPOINT sa_savepoint_2`. DB error: UNIQUE on `ledger.identifier`. After `register()`: `in_transaction=True`, `in_nested_transaction=False`, both domains persistent and not expired. The external reader sees (regs, domains, ledger) = (0, 0, 1), i.e. only the seed. After commit: registration `BA-000002`, both domains present, ledger `[BA-000001, BA-000002]`. Audit: SUCCESS only | **PASS** |
| A2 | An earlier registration in the same caller transaction survives a later collision, which here is against its **own uncommitted** ledger row; the retry does not re-issue the identifier (A.2, A.3, A.8) | same | first=`BA-000001`, second=`BA-000002`, `same_id_twice=False`. 2nd call: `SAVEPOINT_2 … ROLLBACK TO SAVEPOINT … SAVEPOINT_3 … RELEASE`. The first object stays persistent with 0 expired attributes. The external reader sees 0 registrations before commit. After commit both rows are present | **PASS** |
| A3-collision | Caller rollback after a collision-then-success discards everything (A.6) | same | After caller rollback: regs 0, domains 0, ledger = seed only | **PASS** |
| A3-first-write | Caller rollback when `register()` is the **first write** in the transaction (A.5, A.6) | same | recipe: `BEGIN → SAVEPOINT → INSERTs → RELEASE`. The external reader sees 0 registrations. After rollback: regs 0, ledger empty | **PASS (recipe)**. **Differs in legacy/harness**: G4-O-01 |
| P3e-G4 | Issuance as the first write, then caller rollback | `probe_p3e_g4.py` | recipe: ledger `[]`, PASS. Legacy: ledger `['BA-000001']`, a **HIDDEN COMMIT** at `RELEASE`. Pre-fix in legacy: `[]` | recipe PASS. Legacy: G4-O-01 |
| A5 | `issue_identifier()`: flushed caller work survives a collision (A.1) | `probes_g4.py` | `SAVEPOINT_1 … ROLLBACK TO … SAVEPOINT_2 … RELEASE`. Issued `BA-000002`. The domain survives commit. The external reader sees 0 domains before commit | **PASS** |
| A9 | Exhaustion: rollbacks confined to savepoints; caller work kept | same | 5 genuine UNIQUE violations and 5 `ROLLBACK TO SAVEPOINT`. `BarRegistrationAllocationExhausted`, audit DENIED "exhausted". The caller's domain survives commit. 0 registrations | **PASS** |
| C1 | Genuine collisions enter the retry path (C.1) | same | 2 genuine UNIQUE violations, 3 allocator calls → `BA-000003`. Audits: SUCCESS only (no FAILED or DENIED) | **PASS** |
| C2-check | **Own design:** non-collision CHECK violation (`registration_status` mutated after `create`) (C.2–C.5) | same | 1 attempt. `IntegrityError` with orig `CHECK constraint failed: ck_bar_registration_status`, identical to the DB error captured by the engine. Not `AllocationExhausted`. Audit: one **FAILED** "integrity failure that is not an identifier collision"; no DENIED; no event published. The session is still in its transaction. The caller's domain survives commit. 0 ledger and 0 registration rows | **PASS** |
| C3-fk | **Own design:** non-collision FK violation (the registration identifier is switched to an un-issued `BA-777777`) | same | Same pattern: orig `FOREIGN KEY constraint failed`, 1 attempt, FAILED audit, caller work kept | **PASS** |
| C4-issuance-pk | **Own design, edge case:** a UNIQUE violation that is **not** the identifier. The ledger **primary key** reuses an existing row's `id`, and the ledger is non-empty | same | orig `UNIQUE constraint failed: bar_identifier_ledger.id`. 1 attempt; re-raised unchanged; FAILED audit. Ledger = seed only. `is_issued(candidate)` correctly reports False, although a UNIQUE constraint fired | **PASS** |
| C6 | Duplicate behaviour: fast path; race path against a committed row; race path against a **same-session uncommitted** row (C.6) | same | Fast: `AlreadyExists`, DENIED "already registered", 0 SQL writes. Race paths: 2× UNIQUE on `(owning_work_package, business_activity_reference)`, 2× `AlreadyExists`, DENIED "(concurrent)". After commit: registrations `G4 Dup` and `G4 Kept` (no duplicate), ledger 2 rows, both caller domains present. Pre-fix: the same-session race **re-registered "G4 Kept"** after its own rollback | **PASS** |
| CONC | Genuine two-session concurrency (barrier after both MAX reads) | `probe_conc_g4.py` | current: A → `OperationalError: database is locked`, B → `BA-000001`. Pre-fix: the mirror image. SQLite serializes writers with a lock error, so the UNIQUE-collision retry path is **not reachable** under genuine SQLite concurrency. No duplicate identifier in either case | INFO. The real race is **UNVERIFIED** (§8) |
| G2-fingerprint | Gate 2 `probes.py` against the current code | `run_in.py current_tree g2fp_current/probes.py` | P6d/P6e/P6g: caller work **SURVIVED**. P6a: the original `IntegrityError` is re-raised. P6c: `session.new=[]`, ledger `[]` (see G4-O-04). P3e: FAIL, the legacy-config hidden commit (G4-O-01). P7 "racing allocator": `database is locked`, because the probe's second SQLite writer cannot commit while the service keeps its transaction open (by design, to preserve caller work). The stale-read probes above cover this path | INFO. Consistent with the table above |

**Results across configurations (current code).** Recipe: every probe PASS. Legacy and harness: every probe PASS **except A3-first-write** (the registration is visible to the external reader before rollback and persists after it) and the P3e analogue. In the legacy A2 run the external reader also saw the *first* registration before the caller committed, which is the same RELEASE-commit artifact. This means the post-fix run of `probe_batch_loss.py` in its authored legacy configuration shows "First BA survives" partly **because it was already committed at RELEASE**. That run alone is therefore not trustworthy transactional evidence. The recipe runs (A1, A2, A3, A5), with an independent reader and the SAVEPOINT trace, are the evidence relied on here.

## 6. Regression Counts (measured by this reviewer, in-repo)

| Run | Command (from `Backend/Services/AuthService`, env as §2, `-p no:cacheprovider`) | Result |
|---|---|---|
| New transaction-safety tests | `pytest tests/test_bar_transaction_safety.py` | **10 passed** |
| Full BAR suite | `pytest tests/test_bar_identifier_service.py tests/test_bar_registration_service.py tests/test_bar_transaction_safety.py` | **32 passed** |
| Full AuthService suite | `pytest tests` | **982 passed, 0 failed** (71 warnings, 616 s). Output: `$G/pytest_full.txt` |

**Test-infrastructure limitations:**
- **The shared harness** (`tests/conftest.py`) uses `sqlite+aiosqlite:///:memory:` with no FK pragma (fk=0, reconfirmed), a schema from `create_all`, and pysqlite legacy transactions. The 22 pre-existing BAR tests run there. Under the new code, a `SAVEPOINT` that opens a transaction commits at `RELEASE` (G4-O-01), so that harness cannot give valid caller-rollback evidence for BAR.
- **The new test file** uses its own file-backed engine with FK=ON and the recipe. This is the correct configuration, and it matches this reviewer's recipe results.
- **No PostgreSQL** is available (§8).

## 7. Scope and Governance Check (§G)

| Check | Evidence | Result |
|---|---|---|
| No M2 work | `git status --short -- Backend/Runtime` is empty: BusinessActivityEngine and AuthorizationEngine are unchanged and have no untracked files. No `bae_integration` directory exists under `Backend/`. `test_package_boundary.py:60` still asserts non-import of the BAR services | PASS |
| No Workstream D/E code, no BA registration | `BAR-INDEX.md` SHA-256 `6f5307f8…79f5` equals Gate 2's pre-audit copy. Its §3 contains only `*(no entries)*`. A repository-wide grep (excluding venv, node_modules, `.claude`, `architecture`) finds `BarRegistrationService`/`BarIdentifierService` only in `tests/test_bar_*.py`, in BAR docstrings and comments, and in the boundary test's non-import assertion. **No non-test caller exists** | PASS |
| No schema/migration change | Both BAR migrations have mtime 2026-09-22, before Gates 1–3. Hashes: `975acda8…`, `86cbeb42…`. `alembic upgrade f6a7b8c9d0e1:head --sql`, regenerated offline with a dummy PG URL and no connection, is **identical** to Gate 2's `pg_offline_upgrade.sql`. Model DDL pre-fix vs current is identical (§4.1) | PASS |
| No Charter / RD-23-03 / RD-23-04 change | The Charter mtime (25-09 23:49) and the ROD mtime (25-09 23:28) both precede Gate 3. The IRA (mtime 26-09 00:15, by Gate 3) was edited only in its gate-status rows (§0.1, Gate 2/3/4 rows dated 2026-09-26). The RD-23-04 row is dated 2026-09-25 and carries no 2026-09-26 text. No git history exists (untracked), so this is established by content and mtime, not by diff | PASS, with G4-O-03 |
| No AuthorizationEngine change | Covered by the `Backend/Runtime` status above | PASS |
| The four pre-existing tracked modifications were not touched | mtimes: `main.py` and `middleware/tenant.py` 2026-09-15; `models/__init__.py` 2026-09-22; `admin-navigation.ts` 2026-09-08. All precede Gate 3. `git diff models/__init__.py` shows only the pre-existing `C021…`, `C022…`, `BarIdentifierLedger` and `BarRegistration` import and `__all__` lines | PASS |
| Only authorized files changed by Gate 3 | Files with a Gate 3-window mtime: the two services, `bar_identifier_repository.py`, `models/bar_registration.py`, the new `tests/test_bar_transaction_safety.py`, the IMP-REPORT and the IRA. `status-after-gate3.txt` equals `status-before-gate4.txt`. `conftest.py` is unchanged (mtime 2026-07-16) | PASS |

## 8. What is proven, what is not, what blocks

**(i) Transaction safety proven under the tested SQLite/SQLAlchemy environment** (recipe config, FK=ON, genuine UNIQUE violations, independent-reader checks):
- caller work survives a collision, whether pending or flushed;
- an earlier registration survives a later collision, including a collision against its own uncommitted ledger row;
- rollback is confined to the failed savepoint (`ROLLBACK TO SAVEPOINT` traced);
- success is released into the outer transaction (`in_nested_transaction()=False`, `in_transaction()=True` after return);
- no hidden commit: no DBAPI commit is emitted by the services, and the external reader sees nothing before the caller commits;
- caller rollback discards the registration;
- caller commit persists it;
- the retry path does not issue the same identifier twice.

VV-F-02 classification was proven with three independent non-collision failure classes: CHECK, FK, and a PK-UNIQUE violation.

**(ii) UNVERIFIED: true PostgreSQL/asyncpg behaviour.** Specifically:
- savepoint semantics on asyncpg (SQLAlchemy emits an explicit `BEGIN` there, so the legacy-SQLite artifact G4-O-01 should not arise, but this was not exercised);
- a genuine concurrent MAX+1 race reaching the retry path. SQLite serializes writers, and the CONC probe produced lock errors, not collisions;
- `is_issued` visibility of a concurrently committed identifier. The classification relies on `READ COMMITTED` statement-level visibility, which is PostgreSQL's default; `models/database.py` sets no isolation level. Under `REPEATABLE READ` or `SERIALIZABLE`, a genuine concurrent collision would be invisible to `is_issued` and would be re-raised as a non-collision `IntegrityError`. That fails closed: no duplicate is created and no caller work is lost, but it is misclassified;
- `DataError` (over-length strings) on PostgreSQL.

None of these is claimed as passed.

**(iii) Remaining defects that independently block acceptance:** **none within the Gate 3 scope.** The High and Medium findings under remediation are verified as fixed (§9). The observations in §9 are Low or Info and non-blocking. Gate 1 findings outside the Gate 3 scope remain as Gate 1 recorded them, notably CERT-F-02, the RD-23-01 prerequisite commits, which Gate 1 marked as blocking acceptance. So do the non-remediated Gate 2 findings (VV-F-03 to VV-F-07, O-01). This gate does not re-adjudicate any of them.

## 9. Findings

| ID | Item | Classification | Severity (§19.8.7) | Evidence | Blocks acceptance |
|---|---|---|---|---|---|
| **VV-F-01** | Session-wide rollback destroys caller work and re-issues identifiers | **PASS — remediated and independently verified** | (was High) | A1, A2, A3-collision, A3-first-write (recipe), A5, A9, C6; negative control §4.3 | No |
| **VV-F-02** | Any `IntegrityError` treated as a collision | **PASS — remediated and independently verified** | (was Medium) | C1, C2-check, C3-fk, C4-issuance-pk, A9; pre-fix C2/C3/C4 show 5 attempts and exhaustion | No |
| **CERT-F-03** | Docstrings contradict RD-23-03 | **PASS — remediated and independently verified.** Both files now state all five points: the registering act is the governance authority; `bar_registration` is the execution-time runtime record; `BAR-INDEX.md` is the human governance catalogue; a row alone does not establish authorization; the records must stay traceable and reconcilable. The service's class docstring now reads "Writes … runtime … registration record … the registering act, not this service, is the governance authority". The remaining uses of "authority" in the BAR files are D5 *identifier* authority (decided) or the DB constraint as "authoritative backstop"; none claims registration or governance authority. `models/bar_registration.py` has no behaviour change (AST and DDL identical) | (was Medium) | §4.1; grep of the snapshot vs the current files | No |
| G4-O-01 | **SQLite legacy-transaction artifact introduced by the fix.** Under pysqlite's default (legacy) handling, which the shared `conftest.py` harness and Gate 2's probe both use, a `begin_nested()` that is the first write in the caller's transaction starts the SQLite transaction, and its `RELEASE` **commits** the registration or issuance. Caller rollback then does not undo it (A3-first-write and P3e in legacy/harness; the pre-fix code did not have this behaviour). Not applicable to the production dialect: `postgresql+asyncpg`, where SQLAlchemy begins transactions explicitly (UNVERIFIED here). The implementer disclosed it (IMP-REPORT "Known limitations"). Consequence: BAR transactional evidence from the shared harness, or from any legacy-config probe, is not trustworthy. Any SQLite-backed runtime use (such as a local dev DB via `DATABASE_URL`) would need the recipe. No non-test caller exists today | OBSERVATION | Low | `out_current_legacy.txt`, `out_current_harness.txt`, `out_p3e.txt` | No. Recommend folding it into TD-096 / VV-F-03 (harness parity) |
| G4-O-02 | The pre-fix snapshot omits `repositories/bar_identifier_repository.py`, which Gate 3 changed (`is_issued` added). No byte-level pre-fix copy exists. The change was shown to be behaviour-neutral for the pre-fix paths by the Gate 2 fingerprint (§4.1) | OBSERVATION | Info | §4.1 | No |
| G4-O-03 | Governance staleness: the IRA header line 11 still reads "VV-F-01 (High) remains OPEN. Remediation (Gate 3) and its independent verification (Gate 4) are outstanding and not started", although the §0.1 table beneath it records Gate 3 as applied. It is for the Gate 5 Release Readiness Audit to reconcile. It was not edited here | OBSERVATION | Low | IRA lines 11 and 42–44 | No |
| G4-O-04 | Incidental effect: because an exception inside `begin_nested()` rolls back the savepoint, a non-`IntegrityError` raised after the ledger add no longer leaves a pending orphan ledger row (Gate 2 P6c now gives `session.new=[]`, ledger `[]`). This bears on VV-F-07, which was **not** in the Gate 3 scope. VV-F-07's status is left to the owning gate; it is not closed by this record | OBSERVATION | Info | `g2fp_current/out.txt` P6c | No |
| G4-O-05 | Residual classification window: if a non-collision failure occurs and a concurrent transaction commits the same candidate before `is_issued` runs, the failure is treated as a collision and retried. The next attempt fails again and is then re-raised, so the effect is bounded to extra attempts. Only a pathological run of such coincidences could end in "exhausted". The same class of risk applies to the isolation-level dependency in §8(ii) | OBSERVATION | Info | Code review, `bar_*_service.py` classification block | No |
| G4-O-06 | Cosmetic: in `models/bar_registration.py` the sentence "`owning_capability`/`owning_work_package` are opaque reference strings …", formerly part of the D7 bullet, now trails the RD-23-03 bullet | OBSERVATION | Info | Lines 40–54 | No |

**Savepoint and transaction implementation review (§D).**
- Both services obtain the session from the repository.
- Neither service calls `commit()` or `rollback()` on the session. The only rollback left is the savepoint rollback performed by the `begin_nested()` context manager on exception.
- Each attempt is an isolated `begin_nested()`. On success the savepoint is released and `in_nested_transaction()` returns to False inside the caller's transaction.
- The up-front `session.flush()` surfaces the caller's own invalid work unchanged, before any attempt. It is not audited as FAILED, and that is correct because it is not a BAR failure.
- After a savepoint rollback, the objects added in that attempt are expunged. Outer objects are neither expired nor expunged (A1, A2).
- `BarRegistrationService.__init__` still enforces a shared session between the two repositories.

No new defect was found in this review. Residual risks are listed in §8(ii), G4-O-01 and G4-O-05.

## 10. Verdict

All three authorized remediations are independently verified. Each has a from-scratch probe per defect class and a valid pre-fix negative control. No Critical, High or Medium defect remains within the Gate 3 scope.

**GATE 4 — PASS, subject only to any separately identified Gate 1 prerequisites or closure conditions.**

This record does not declare WP-23 A–C accepted, certified or closed. PostgreSQL/asyncpg concurrency and savepoint behaviour remain **UNVERIFIED** (§8(ii)). §19.7b Gate 5 remains required.

## 11. Integrity Statement

**What was run:**
- read-only inspection of the listed sources;
- SHA-256 and `diff` of the snapshot, the current files and the scratch trees;
- the probe scripts in `$G`, using scratch copies of `golden_head.db` and in-memory SQLite only;
- offline `alembic upgrade --sql` against a dummy PostgreSQL URL (no connection made);
- pytest in-repo with `-p no:cacheprovider` and `PYTHONDONTWRITEBYTECODE=1`;
- pytest in the scratch trees.

**What was not done:**
- no repository code, test, migration, configuration or governance document was modified;
- no database file was created in the repository;
- no git state-changing command was used;
- `prefix_snapshot/`, `gate2/` and `gate3/` were not written to (the needed files were copied into `$G`).

**Repository state:**
- `status-after-gate3.txt` is identical to `status-before-gate4.txt` (150 entries).
- The final `git status --short` differs from that baseline by exactly one line: `?? architecture/06-Reviews/VV-AUDIT-WP-23-AC_BAR_Workstreams_A-C_Gate-4.md`.
- `git diff --cached --name-only` is empty.
- The only change this reviewer introduced is this file.
