# RRA-WP-23-AC — Gate 5 Release Readiness Audit — Enterprise BAR Workstreams A–C Tranche

**Gate:** `CLAUDE.md §19.7b` Gate 5 — Release Readiness Audit.
**Object:** WP-23 (Enterprise Business Activity Registry Mechanism), Workstreams **A** (`BAR-INDEX.md` governance catalogue), **B** (Business Activity identifier issuance ledger) and **C** (runtime BAR registration record and mechanism), treated as a separately closable tranche under RD-23-02.
**Date:** 2026-09-28.
**Repository HEAD at audit:** `203bed15cdcb963e98266e89391399fb607611f4` (verified with `git rev-parse HEAD`). Nothing staged (`git diff --cached --name-only` empty).

---

## VERDICT: **GATE 5 — PASS WITH CONDITIONS**

- **No Critical, High or Medium defect remains open in the A–C code.** VV-F-01 (High) and VV-F-02 (Medium) are remediated. Gate 4 verified them, and this gate spot-checked them again with its own probe and a working negative control. No `§19.8.5`-class defect is open.
- **CERT-F-02 is RESOLVED.** Commits `355ebbe` (WP-20/C-021) and `203bed1` (WP-21/C-022) now hold the parent migrations. The committed Alembic head is `f6a7b8c9d0e1`. The WP-23 migrations chain onto it cleanly.
- **Tests I ran myself:**
  - BAR tests: **32 passed** (9 + 13 + 10).
  - Full AuthService suite on the working tree: **982 passed, 0 failed**.
  - Full suite on a scratch tree built from `git archive HEAD` plus exactly the WP-23 A–C file set: **982 passed, 0 failed**.
- **The conditions (§9) are governance conditions, not code conditions.** Two must be met before the WP-23 A–C commit:
  1. **C-1:** record in `TECH-DEBT.md` the Technical Debt that Gate 1 and Gate 2 said must be registered. None of it is registered today, and `§19.8.2` requires it.
  2. **C-2:** synchronize the WP-23 status text that this gate found stale. Several WP-23 documents still say the commit is blocked, Gate 4 is not started, and A–C is not independently verified.

  C-3 (the basis of the acceptance record) and C-4 (post-commit reconciliation of committed stale statements) are also listed in §9.
- **This gate does not accept, certify, close, commit or push anything.** WP-23 as a whole remains **OPEN**. Acceptance of A–C is a Repository Owner act that follows this audit.

---

## 1. Independence Statement

I am a fresh-context reviewer. I had no part in any of the following:
- the WP-23 A–C implementation or its Gate 3 remediation;
- `IMP-REPORT-WP-23`, `IRA-WP-23-AC`, `ROD-WP-23-AC`, the Charter or the design;
- Gate 1 (`CERT-WP-23-AC`), Gate 2 (`VV-AUDIT-WP-23-AC`) or Gate 4 (`VV-AUDIT-WP-23-AC_…_Gate-4`);
- the WP-20 and WP-21 commits.

Every governance document and gate record was read as a lead, never as evidence. I re-derived each material claim from git, the source, command output and my own probe. The stale statements S-1 to S-12 (`IRA-WP-23-AC §7`) played no part in any conclusion.

## 2. Scope

**In scope:**
- release readiness of the A–C tranche: git state, commit prerequisites, the commit boundary and separability;
- consistency across source, tests, migrations and governance documents, and the accuracy and staleness of those documents (the specific purpose of Gate 5);
- a full regression run;
- disposition of every open Gate 1, Gate 2 and Gate 4 item for release.

**Out of scope:**
- Workstreams D to H;
- WP-BAE-001 M2, which is NOT AUTHORIZED and NOT STARTED (`IRA-BAE-001-M2:9`);
- any Business Activity registration or identifier assignment;
- re-adjudicating Gate 4's findings.

## 3. Sources Read

- **Governance:**
  - WP-23 Charter (§1, §20, §21 with the RD-23-04 correction note, §22 with the RD-23-02 note, §23);
  - `ENTERPRISE-BAR-MECHANISM-DESIGN-AND-IMPLEMENTATION-READINESS.md` §19 rows A–H and the RD-23-04 correction note;
  - `IRA-WP-23-AC_BAR_Workstreams_A-C_Closure_Readiness.md`, in full;
  - `ROD-WP-23-AC-BAR-Registry-Authority-Decision-Preparation.md` header and §0 (RD-23-03);
  - `BAR-INDEX.md` and `IMP-REPORT-WP-23_Enterprise_BAR_Mechanism.md`, both in full (including the Gate 3 section);
  - `WPR-001` WP-23 row and note (working tree), and the WP-23-related hunks of the working-tree diff;
  - `TECH-DEBT.md` (register rows, TD-096, TD-162, TD-170);
  - `IRA-BAE-001-M2 §0` and the `ROD-BAE-001-M2` header, for boundary confirmation only;
  - `RRA-WP-21` and `VV-AUDIT-WP-21`, for how earlier Work Packages handled the PostgreSQL limitation;
  - `CLAUDE.md` §16–§19 (§19.7, §19.7b, §19.8.2, §19.8.5, §19.8.7) and §21.4.
- **Gate records:** `CERT-WP-23-AC_BAR_Workstreams_A-C.md` (Gate 1), `VV-AUDIT-WP-23-AC_BAR_Workstreams_A-C.md` (Gate 2) and `VV-AUDIT-WP-23-AC_BAR_Workstreams_A-C_Gate-4.md` (Gate 4), all in full.
- **Code** (`Backend/Services/AuthService/`): `services/bar_registration_service.py` in full; `services/bar_identifier_service.py` module docstring; `models/bar_registration.py` and `models/bar_identifier_ledger.py` docstrings; both BAR migrations (headers, columns, constraints, revision ids); the BAR test files (names, counts, and the assertion lines Gate 1 cited); the `models/__init__.py` diff.

## 4. Method

1. **Read-only git.**
   - `rev-parse`, `log`, `show --stat` of `355ebbe` and `203bed1`, `merge-base --is-ancestor`, `ls-files`.
   - `status --porcelain --untracked-files=all`, compared against `status-before-gate5.txt` (identical), `commits/status-after-C2.txt` (identical) and `status-after-gate4.txt`.
   - `diff` and `diff --cached`.
   - `git grep` on `HEAD` for committed stale statements.
2. **Scratch trees** (under `…\scratchpad\gate5\`):
   - `head_tree` = `git archive HEAD` (AuthService and Runtime);
   - `wp23_tree` = `git archive HEAD` plus exactly the WP-23 A–C file set (11 untracked files, `models/__init__.py`, `BAR-INDEX.md`). `diff -rq --strip-trailing-cr` against the working-tree AuthService (excluding venv, caches and the ignored dev DB) returned **no differences**;
   - `prefix_tree` = `wp23_tree` with the SHA-verified pre-fix snapshot (`prefix_snapshot/`, digests `84eb665d…`, `4241233a…`, `b7258437…`) overlaid, used for a negative control.
3. **Alembic.**
   - `alembic heads` on `head_tree`, the working tree and `wp23_tree`, plus `alembic history`.
   - Offline PostgreSQL rendering (`--sql`, dummy URL, no connection) of `upgrade f6a7b8c9d0e1:head` and `downgrade b8c9d0e1f2a3:f6a7b8c9d0e1`.
4. **Tests.**
   - The three BAR test files in-repo.
   - The full AuthService suite in-repo and in `wp23_tree`, with `JWT_SECRET_KEY`/`JWT_ALGORITHM` set to the CI values (TD-010) and `-p no:cacheprovider`.
5. **Purpose-built probe** `gate5/probe_g5.py`, written from scratch, not adapted from the suite or from earlier gates' probes.
   - **Engine:** file DB; `PRAGMA foreign_keys=ON` on every connection; the pysqlite SAVEPOINT recipe.
   - **G5-P1:** VV-F-07. A non-`IntegrityError` is injected after the ledger add, and the caller catches it and commits.
   - **G5-P2:** VV-F-01. Two registrations in one caller transaction; the second meets a genuine UNIQUE collision through a stale MAX read.
   - **G5-P3:** no hidden commit. An independent `sqlite3` reader checks what is visible before the caller commits or rolls back.
   - The probe was run against the current code and, as a negative control, against the pre-fix snapshot.
6. **Hashes** of every WP-23 code file, both migrations and `BAR-INDEX.md` (`gate5/wp23_sha256.txt`), compared with the Gate 2 and Gate 4 records.

## 5. Checklist Results

### 5.1 Commit and migration prerequisite (CERT-F-02) — **RESOLVED**

| Check | Evidence | Result |
|---|---|---|
| `355ebbe` exists (WP-20/C-021) | `355ebbebbb9cc98e…`, "feat(WP-20): commit C-021 offering definition implementation", 23 files, including migration `e5f6a7b8c9d0` and the C-021 model, repository, service, router, schema, tests and frontend | PASS |
| `203bed1` exists (WP-21/C-022) | `203bed15cdcb963e…`, "feat(WP-21): close C-022 commercial account", 29 files, including migration `f6a7b8c9d0e1`, the C-022 code and the WP-21 gate artifacts | PASS |
| C1 is an ancestor of C2; C2's parent is C1 | `git merge-base --is-ancestor 355ebbe 203bed1` → true. `git rev-parse 203bed1^` = `355ebbe…` | PASS |
| Committed head after C2 | `alembic heads` on `git archive HEAD` → **`f6a7b8c9d0e1 (head)`** | PASS |
| WP-23 migrations only in the working tree | `a7b8c9d0e1f2` and `b8c9d0e1f2a3` are `??` (untracked). `git log --all` has no history for any `*bar_*` AuthService path. `git ls-files` lists both parent migrations as tracked | PASS |
| Chain | Working tree and `wp23_tree`: single head `b8c9d0e1f2a3`. History: `d4e5f6a7b8c9 → e5f6a7b8c9d0 → f6a7b8c9d0e1 → a7b8c9d0e1f2 → b8c9d0e1f2a3`. `down_revision` values are `f6a7b8c9d0e1` and `a7b8c9d0e1f2` | PASS |
| WP-23 not committed | No commit touches any BAR file or WP-23 governance document | PASS |
| `models/__init__.py` | After C1 and C2, the working-tree diff is **only** the two BAR imports and the two BAR `__all__` entries (+4 lines). The C-021 and C-022 lines are committed. **The IRA's "hunk-selective staging" constraint (`IRA-WP-23-AC:67`) is now moot:** the whole-file diff is WP-23-only | PASS |

**CERT-F-02: RESOLVED.** The RD-23-01 order (WP-20 commit, then WP-21 commit, then WP-23 A–C) is now satisfiable. A WP-23 A–C commit would leave `alembic upgrade` working on a clean checkout.

### 5.2 Gate 1 status

| Item | Status now | Blocks release of A–C? |
|---|---|---|
| Gate 1 verdict | **STOP** (`CERT-WP-23-AC:5`). Gate 1 was never re-run or resumed; its §6 allows "re-run, or narrowly resumed" | See condition C-3 |
| CERT-F-01 (High, governance) | **Resolved by Repository Owner act RD-23-04** (`IRA-WP-23-AC:26`). The correction notes exist, with the old text struck through, at Charter §21 rows C/D (`Charter:168-169`) and the note below (`:175-185`), and at design §19 rows C/D and the note below. The ratification is limited to construction already performed, is expressly "not an expansion of WP-23 scope", and does not authorize D, E, M2, registration, gating or new runtime behaviour | No |
| CERT-F-02 (High) | **Resolved** (§5.1) | No |
| CERT-F-03 (Medium) | **Remediated at Gate 3 and verified at Gate 4.** Re-read here: `models/bar_registration.py:40-54` and `services/bar_registration_service.py:15-26, 99` state the RD-23-03 layered model and claim no registration or governance authority | No |
| CERT-F-04 (Medium; GAP-23-03-1/2) | Open, by design: RD-23-03 §0.2 forbids fixing it now. Gate 1's condition was "No, **if registered as TD** with the condition that it closes before any execution-eligibility consumer is built". **Not registered** | **Yes, through C-1** (register it) |
| CERT-F-05 (Medium) | Open. The two misnamed "forced collision" tests are unchanged (`test_bar_identifier_service.py:111`, `test_bar_registration_service.py:238`). Real-collision coverage now exists in `test_bar_transaction_safety.py`. Gate 1 required it to be recorded as TD. **Not recorded** | Through C-1 |
| CERT-F-06 (Medium) | Tracked as TD-096 (Open) | No |
| CERT-F-07 (Medium) | Same defect as VV-F-01. **Remediated and verified at Gate 4**; re-probed here (§5.4) | No |
| CERT-F-08 (Low) | Open (model/migration drift). Gate 1 required TD. **Not recorded** | Through C-1 |
| CERT-F-09 (Low) | **Still open.** The unsupported "§19a.6" quotation remains at `models/bar_identifier_ledger.py:36-40` and migration `a7b8c9d0e1f2:34-37`. Gate 1 said to fix it "in the CERT-F-03 docstring pass"; Gate 3 did not | No (B) |
| CERT-F-10 (Low) | Still open: `BAR-INDEX.md:18`, `:60`, `:98` | No (B; see C-2) |
| CERT-F-11 (Low) | Still open (the committed text at `BAR-WP23-WORKSTREAM-D-…:198` is outside the S-inventory) | No (C-4) |
| CERT-F-12 (Low) | Still open. The Charter cites a nonexistent §29/§31 (`Charter:5, 11, 21`). The IRA header is stale (worse now; see §5.5) | No (C-2) |
| CERT-F-13 (Low) | Still open. Non-evidential tests remain (`test_bar_identifier_service.py:193`, `test_bar_registration_service.py:362`) | No (B) |
| CERT-F-14 (Low) | Open (duplicated allocator; no overflow guard). Gate 1 required TD. **Not recorded** | Through C-1 |

**No unauthorized scope expansion.**
- A repository-wide search of `Backend/` finds BAR symbols only in the 11 WP-23 files and in the BAE negative boundary test (`Backend/Runtime/BusinessActivityEngine/tests/test_package_boundary.py`).
- No `main.py`, router, schema, `dependencies.py` or `authz_integration` file references BAR.
- No `bae_integration*` path exists.
- `git status -- Backend/Runtime` is empty.

### 5.3 Gate 2 residual findings — classification

`§19.8.5` test applied to each: is it an architectural, security, data-integrity or tenant-isolation defect, a failing test, a build failure, broken functionality, or a mandatory-compliance item?

| Finding | Classification | `§19.8.5` test | TD recorded? |
|---|---|---|---|
| VV-F-01 (High) | **Addressed by later evidence:** remediated at Gate 3, PASS at Gate 4, re-probed here with a negative control (§5.4) | Was data integrity, and is now fixed. Not deferred | n/a |
| VV-F-02 (Medium) | **Addressed by later evidence:** remediated at Gate 3, PASS at Gate 4 | Fixed | n/a |
| VV-F-03 (Medium): harness has no FK pragma and uses `create_all` | **Deferred technical debt**, already TD-096 (Open). Gate 4 recommended folding its G4-O-01 (the SQLite legacy-transaction `RELEASE`-commits artifact) into TD-096. **That was not done** | Not a product defect: a test-infrastructure parity gap, and FK enforcement was proven independently at Gates 2 and 4 and here. Deferrable | Partly (TD-096 exists; G4-O-01 is not appended) → C-1 |
| VV-F-04 (Low): model/migration drift | **Deferred TD.** Enforcement semantics are equivalent. The offline PostgreSQL DDL is byte-identical to Gates 2 and 4 (§5.6) | Not a defect class listed in `§19.8.5`. Deferrable | **No** → C-1 (TD-162 covers C-021 only) |
| VV-F-05 (Low): `BA-999999`+1 overflows to seven digits | **Deferred TD.** Reachable only after 999,999 registrations, against a known population of 21 | A latent format-integrity limit, not reachable in practice. Gate 2 classed it Low and non-blocking. I concur that it is deferrable if tracked | **No** → C-1 |
| VV-F-06 (Low): no DB format CHECK on `identifier` | **Deferred TD.** Reachable only by writes that bypass the service. On PostgreSQL a non-numeric value would make `max_identifier_sequence()` raise and halt issuance (unverified) | Fails closed. No row corruption through the service. Deferrable | **No** → C-1 |
| VV-F-07 (Low): orphan pending ledger row after a non-`IntegrityError` | **Addressed by later evidence.** The savepoint remediation rolls back the attempt's inserts on any exception. My probe G5-P1: current code `session.new=[]`, ledger after the caller's commit `[]`; pre-fix control: `session.new=['BarIdentifierLedger']`, ledger `['BA-000001']` (orphan reproduced). Consistent with G4-O-04 | Resolved | n/a (record its closure in the IMP-REPORT under C-2) |
| O-01 (Info): `business_activity_reference` is not normalized | **Observation for Repository Owner visibility.** No governing source defines normalization, and inventing a rule would breach `§18`. Not TD | n/a | n/a |

**None of the residual Gate 2 items is a `§19.8.5` non-deferrable defect.** Deferral is still conditional on actually recording the items (`§19.8.2`: Technical Debt "SHALL NOT exist solely within Independent Review reports"). The register has **no** WP-23 or BAR entry today: its only BAR-related row is TD-170, which belongs to WP-BAE-001 M2. That gap is condition **C-1**.

### 5.4 Gate 3/4 status — **PASS confirmed**

- **Gate 4 record:**
  - verdict "GATE 4 — PASS, subject only to any separately identified Gate 1 prerequisites or closure conditions";
  - negative control valid (pre-fix reproduces VV-F-01 and VV-F-02; current code does not);
  - no hidden commit under the recipe configuration;
  - savepoint behaviour traced;
  - VV-F-02 classification proven with three non-collision classes;
  - CERT-F-03 PASS.

  I do not re-adjudicate any of this.
- **Code unchanged since Gate 4:**
  - service SHA-256 values `2939bc04…` and `99ae6677…` equal Gate 4's "current" digests;
  - migrations `975acda8…` and `86cbeb42…` equal Gate 4's digests;
  - `BAR-INDEX.md` `6f5307f8…` equals the Gate 2 and Gate 4 value;
  - file mtimes (latest 2026-09-26 00:05) precede Gate 4.
- **Spot-check of my own** (`gate5/probe_g5_output.txt`; negative control in `gate5/probe_g5_prefix_output.txt`):

| Probe | Current code | Pre-fix snapshot (negative control) |
|---|---|---|
| G5-P2, commit: 2nd registration collides with the 1st's uncommitted ledger row (allocator called twice) | `('BA-000001','BA-000002')`; both rows persist after commit | `('BA-000001','BA-000001')`; only "G5 Second" survives: **VV-F-01 reproduced** |
| G5-P3: independent reader before the caller ends | Sees nothing new before commit. After the caller's rollback, nothing from that transaction persists | Pre-fix rows were visible before the caller ended |
| G5-P1: VV-F-07 | No orphan | Orphan `BA-000001` committed |

- **FK positive control:** `PRAGMA foreign_keys` = 1 inside each session.
- **Gate 4 observations and release impact:**
  - **G4-O-01 (Low):** the artifact affects SQLite legacy mode only, and no non-test caller exists. Not release-blocking. It should be appended to TD-096 (C-1).
  - **G4-O-02 (Info):** none.
  - **G4-O-03 (Low):** IRA staleness; confirmed and widened in §5.5 (C-2).
  - **G4-O-04 (Info):** confirms VV-F-07 closure (above).
  - **G4-O-05 (Info):** bounded extra retries; none.
  - **G4-O-06 (Info):** cosmetic.

### 5.5 Release-artifact completeness and cross-document consistency

**Completeness: every required artifact exists.**
- Charter
- IMP-REPORT, including the Gate 3 remediation record
- `BAR-INDEX.md`
- Gate 1 record (CERT)
- Gate 2 record (VV-AUDIT)
- Gate 4 record (VV-AUDIT Gate-4)
- RD-23-01 to RD-23-04 (`IRA-WP-23-AC §0`), with RD-23-03 also in `ROD-WP-23-AC §0`
- the design and readiness package, `ROD-ENTERPRISE-BAR` and the BAR investigation
- 8 implementation files, 2 migrations, 3 test files
- this RRA

Nothing is missing.

**Staleness: the specific purpose of Gate 5.** The following statements no longer match the repository as verified in §5.1 to §5.4.

| # | Document:line | Stale statement | Actual state |
|---|---|---|---|
| ST-1 | `IRA-WP-23-AC:8` | "The commit is blocked by missing prerequisite commits … Gate 1 cannot be dispatched" | Prerequisites committed (`355ebbe`, `203bed1`); Gate 1 ran |
| ST-2 | `IRA-WP-23-AC:11` | "VV-F-01 (High) remains OPEN. Remediation (Gate 3) and … (Gate 4) are outstanding and not started" | Gate 3 applied; Gate 4 PASS |
| ST-3 | `IRA-WP-23-AC:22` (RD-23-01 status) | "Prerequisite NOT MET: STOP condition reached for the commit" | Met |
| ST-4 | `IRA-WP-23-AC:42, 44` (§0.1 Gate 2 and Gate 4 rows) | "pending Gate 4"; "Gate 4 … REQUIRED — not started" | Gate 4 PASS (2026-09-26) |
| ST-5 | `IRA-WP-23-AC:105-113` (§2) | "`IMP-REPORT` … Does not exist"; "Gate 1–5 artifacts … None exist"; `models/__init__.py` "in the same diff hunk as WP-20 … WP-21" | All exist; the hunk is BAR-only |
| ST-6 | `IRA-WP-23-AC:193, 198-199, 356` (§5.1 P-2, P-7, P-8; §10) | P-2 "NOT MET — blocks P-10"; P-7 "NOT STARTED"; "the commit (P-10) remains blocked until P-2 is met" | P-2 met; P-7 and P-8 done |
| ST-7 | `IMP-REPORT-WP-23:15-16`, `:138`, `:222` | "AWAITING INDEPENDENT VERIFICATION"; "AWAITING GATE 4" | Gates 1, 2 and 4 recorded; Gate 5 this record |
| ST-8 | `IMP-REPORT-WP-23:115-118` | "Not committed; commit currently blocked (RD-23-01) … both untracked" | Parents committed |
| ST-9 | `IMP-REPORT-WP-23:72-73, 78, 100` | DD-1: "remains Gate 1's determination"; DD-2: "runtime docstrings are not updated"; DD-7: whole-session rollback; "No new Technical Debt item is recorded" | RD-23-04 resolved DD-1 (the report never mentions RD-23-04); Gate 3 fixed DD-2 and DD-7; TD registration still owed (C-1) |
| ST-10 | `BAR-INDEX.md:42, 76, 119` | A–C "not yet independently verified" | Independently verified at Gates 1, 2 and 4 (not yet accepted) |
| ST-11 | `WPR-001:133` (WP-23 row, working tree) and note `:125` | Row status "CHARTERED — IMPLEMENTATION NOT YET COMPLETED"; note "does not create `BAR-INDEX.md` or any runtime artifact" (true at registration time) | The row does not reflect the A–C tranche state (P-10 row synchronization, `IRA-WP-23-AC:185`) |
| ST-12 | `ROD-WP-23-AC:7` | "No change is made to the `bar_registration` docstring, the BAR services …"; GAP-23-03-3 open | Historical at decision time; GAP-23-03-3 is closed by the CERT-F-03 remediation, but there is no annotation |
| ST-13 | Design §19 rows B/C (`ENTERPRISE-BAR-…:342-343`) | "READY FOR INDEPENDENT VERIFICATION"; atomicity "proven deterministically via the forced-collision test" | Those tests do not collide (CERT-F-05) |
| ST-14 | `models/bar_identifier_ledger.py:36-45`; migration `a7b8c9d0e1f2:34-37`; `services/bar_identifier_service.py:31-34` | "Workstream C, not yet built"; "Workstream C will call `issue_identifier()`" | C is built and deliberately does **not** call `issue_identifier()` (DD-5) |

**Consistent and correct on authority (RD-23-03):**
- `BAR-INDEX.md §1` (`:16-21`), §2 D8 (`:35`) and §4 (`:70`);
- IMP-REPORT header (`:8-12`);
- Charter correction note (`:180-184`);
- design correction note;
- `models/bar_registration.py:40-54`;
- `services/bar_registration_service.py:15-26, 39-44, 99`.

Each states: the registering act is the governance authority; `bar_registration` is the runtime execution-time record, and a row is not proof of authorization; `BAR-INDEX.md` is the governance catalogue and "must not become a second runtime authority"; reconciliation is required and its mechanism is undecided. **No release-blocking contradiction.** The residual Low items are `BAR-INDEX.md` header `:4` ("authoritative … registration record", D7 wording), §8 `:98` (collision-check "against this index", CERT-F-10) and ST-14. None of them assigns runtime authority to the index.

### 5.6 A–C scope — **PASS**

- A–C provide the catalogue (A), issuance (B) and the runtime record and `register()` (C).
- There is no router, endpoint, adapter, `bae_integration` package, discovery query, execution gate, cutover, registration of an existing Business Activity, Business Activity execution or M2 code.
- The only non-BAR reference is the negative boundary test in BAE.
- **No non-test caller** of `BarRegistrationService`, `BarIdentifierService` or either repository exists (Grep over `Backend/`, excluding venv).
- `BAR-INDEX.md §3` contains only `*(no entries)*`. `BA-000089` appears only in §6, outside the Register.
- **`§21.4` does not attach:** the tables have no organization or tenant column (migration `a7b8c9d0e1f2:39-40`, `b8c9d0e1f2a3:52-53`), and no endpoint exists.

### 5.7 Tests and migrations — measured by this reviewer

| Run | Result |
|---|---|
| `tests/test_bar_identifier_service.py` + `test_bar_registration_service.py` + `test_bar_transaction_safety.py` (in-repo) | **32 passed** (9 + 13 + 10), 14.4 s |
| Full AuthService suite, working tree | **982 passed, 0 failed**, 71 warnings, 507 s (`gate5/full-suite-worktree.log`) |
| Full AuthService suite, `wp23_tree` (= `git archive HEAD` + the WP-23 A–C file set) | **982 passed, 0 failed**, 71 warnings, 468 s (`gate5/full-suite-wp23tree.log`). **The proposed commit boundary is self-consistent** |
| `alembic heads`: HEAD extract / working tree / `wp23_tree` | `f6a7b8c9d0e1` / `b8c9d0e1f2a3` / `b8c9d0e1f2a3`, each a single head |
| Offline PostgreSQL `upgrade f6a7b8c9d0e1:head --sql` | Additive only (2 × `CREATE TABLE` + `CREATE INDEX`). **Byte-identical** to Gate 2's `pg_offline_upgrade.sql` and Gate 4's `pg_offline_upgrade_g4.sql` |
| Offline PostgreSQL `downgrade b8c9d0e1f2a3:f6a7b8c9d0e1 --sql` | The exact reverse (drop index, drop table, for C then B) |

**Environmental limitation (category C).** PostgreSQL is not installed and the Docker daemon is not running. The following remain **UNVERIFIED**, as at Gates 2 and 4:
- real PostgreSQL/asyncpg savepoint semantics;
- a genuine concurrent `MAX+1` race reaching the retry path;
- `is_issued` visibility under non-default isolation levels;
- `DataError` on over-length strings;
- the `CAST` behaviour behind VV-F-06;
- full-chain `alembic upgrade head` from base (the pre-existing SQLite `ALTER` limitation at `b3f7a1c9d2e4`, Gate 2 §5.1).

**Does this block the tranche?**

No existing governance rule makes a PostgreSQL run a release criterion. The directly comparable precedent is WP-21 (`RRA-WP-21`, `VV-AUDIT-WP-21:58, 110-111`). It was CERTIFIED, CLOSED and RELEASE-READY on SQLite with FK enforcement, offline dialect compilation, and a forced-collision probe, with no PostgreSQL concurrency run.

The same treatment applies here, with two aggravating notes:
- `begin_nested()` is used for the first time in the repository (`IMP-REPORT:149`);
- no production caller exists yet.

The limitation therefore does **not** block acceptance or commit of A–C. I recommend recording it as a Medium TD item, with the planned resolution "verified on PostgreSQL/asyncpg before the first real registering act or the first execution-eligibility consumer (Workstream E / M2)" (C-1). I do not claim any of it as passed.

### 5.8 Working tree, commit safety and separability — **PASS**

- **Status baseline.** `git status --porcelain --untracked-files=all` at the start of this audit was **identical** to `status-before-gate5.txt` (114 entries) and to `commits/status-after-C2.txt`.
- **Differences from `status-after-gate4.txt`:** only removals of WP-20/WP-21 paths now committed in `355ebbe`/`203bed1` (`main.py`, `middleware/tenant.py`, `admin-navigation.ts`, the C-021/C-022 code and migrations, and WP-21 governance files). The only other difference is that `architecture/04-Requirements/` is listed per file rather than as a directory. **There are no additions.**
- **WP-23 file hashes** match Gate 4 (§5.4).
- The two full-suite runs and the probe **left the working tree unchanged** (status re-diffed after the runs: identical).
- **Separability of the tracked modified files:**
  - `models/__init__.py` is WP-23-only.
  - `WPR-001` holds three hunks: a WP-22 row and note (`@@ -74,0 +75,3`), which are not WP-23; the WP-23 note (`@@ -121,0 +125,2`); and the WP-23 row (`@@ -127,0 +133`). The WP-23 hunks are separable with a prepared partial patch (`git apply --cached`).
  - `TECH-DEBT.md`'s only hunk is TD-170. It belongs to WP-BAE-001 M2 (raised in `IRA-BAE-001-M2` RD-M2-03) and **must stay out** of the WP-23 commit.
  - `CBOR-INDEX.md` and `SER-001` (C-024/WP-22), and `CAP-001`, `ADR-002`, `CANONICAL-ENTERPRISE-SEARCH-…` and the delivery map (C-040/D-002, C-020–C-025 lines) contain **no** BAR or WP-23 content (diff token scan). They stay out.
  - `CLAUDE.md` is not WP-23 work and stays out.
- **M2 and BAE:** there is no `bae_integration` path, `Backend/Runtime` has no working-tree changes, and `IRA-BAE-001-M2:9` still reads "M2 remains NOT AUTHORIZED and NOT STARTED".
- **Zero real registrations.**

## 6. Findings

Categories: **A** = blocker to acceptance or commit; **B** = non-blocking observation or deferred Technical Debt; **C** = environmental limitation; **D** = a future Workstream D/E or M2 concern outside this tranche. Severity follows `§19.8.7`.

| ID | Cat. | Severity | Description | Evidence | Blocks commit? |
|---|---|---|---|---|---|
| G5-01 | **A** | Medium | **Required Technical Debt is not registered.** Gate 1 said CERT-F-04, -05, -06, -08 and -14 "must be recorded in the Technical Debt Register (or cross-referenced to TD-096) before acceptance". Gate 2 said VV-F-03 to VV-F-07 may be recorded in `TECH-DEBT.md`. Gate 4 recommended folding G4-O-01 into TD-096. `TECH-DEBT.md` has **no** WP-23/BAR entry, and the IMP-REPORT says "No new Technical Debt item is recorded". `§19.8.2` makes registration mandatory | `CERT-WP-23-AC:113-123, 141`; `VV-AUDIT-WP-23-AC:151-155, 173`; Gate-4 `:181`; `TECH-DEBT.md` (rows TD-001 to TD-170); `IMP-REPORT-WP-23:100` | **Yes** (acceptance prerequisite → condition C-1) |
| G5-02 | **A** | Low | **WP-23 governance status is stale** against the verified repository state (ST-1 to ST-13 in §5.5). The WP-23 documents say the commit is blocked, the prerequisites are unmet, Gate 4 is not started, A–C is not independently verified, no IMP-REPORT or gate artifacts exist, and TD is not recorded. Committing and pushing them unchanged would publish false status. Detecting exactly this is Gate 5's purpose (`§19.7b` item 5) | §5.5 table | **Yes**: sync before or in the WP-23 commit (condition C-2) |
| G5-03 | B | Low | Code docstrings are stale or unsupported: "Workstream C, not yet built" and "Workstream C will call `issue_identifier()`" (ST-14), and CERT-F-09's unsupported §19a.6 quotation, which was not corrected in the Gate 3 docstring pass. There is no behaviour impact, and it does not contradict RD-23-03. Correcting it would be a code-file change after Gate 4, so it needs its own authorization (and any further verification the Repository Owner requires). It is therefore recorded here rather than made a commit condition | `models/bar_identifier_ledger.py:36-45`; migration `a7b8c9d0e1f2:34-37`; `services/bar_identifier_service.py:31-34` | No |
| G5-04 | B | Low | Gate 1 findings CERT-F-10, -12 and -13 remain open (`BAR-INDEX.md` §4 "reproduced exactly" and §8 collision-check wording, and the line 18 pointer; Charter §29/§31 citations; placeholder tests) | §5.2 | No (may be folded into C-2 or C-1) |
| G5-05 | B | Info | **Forward references to uncommitted, non-WP-23 documents.** WP-23 governance documents cite `ADR-041`, `ROD-C024-BAR_Treatment_Decision_Preparation.md`, the `WP-22` Charter and `CBOR-INDEX` `BIA-000001`, all uncommitted C-024/WP-22 material (`BIA-000001` appears 0× at HEAD and 2× in the working tree). They also cite `IRA-BAE-001-M2` and `ROD-BAE-001-M2`, uncommitted M2 readiness material. A WP-23-only commit would carry dangling references until those are committed under their own authority. This does not break the build | grep of the WP-23 document set (§5.8); `git show HEAD:…/CBOR-INDEX.md` | No. Repository Owner to decide the sequencing, or accept forward references |
| G5-06 | B | Info | Gate 1's verdict remains formally **STOP** and was never re-issued. Every item it named as blocking acceptance is now resolved: CERT-F-01 (RD-23-04), CERT-F-02 (§5.1), and CERT-F-03 and F-07 (Gate 4). Under RD-23-02 the tranche's terminal state is ACCEPTED, not CERTIFIED | `CERT-WP-23-AC:5, 127-142`; §5.2 | No (condition C-3: acceptance record states the basis) |
| G5-07 | C | — | PostgreSQL/asyncpg savepoint, concurrency, isolation, `DataError`, and full-chain migration are **UNVERIFIED**. This is consistent with the WP-21 precedent, and no rule makes it a release criterion | §5.7 | No (recommend registering as a TD item under C-1) |
| G5-08 | D | (per C-1 entry) | CERT-F-04 / GAP-23-03-1 and 2: no act-to-row enforcement and no index-to-table reconciliation. It is latent while nothing consumes `bar_registration`. It becomes a governance-authority, fail-open boundary once Workstream E or M2 reads the table for eligibility. The C-1 TD entry must carry a hard precondition that it closes before any such consumer is built, and its severity must be assessed against `§19.8.7`'s High criterion ("weakens a security … boundary") at that point | `services/bar_registration_service.py:22-26, 118-145`; `ROD-WP-23-AC §0.4` | No (for A–C) |
| G5-09 | D | Info | S-1 to S-12 plus CERT-F-11: committed documents still say BAR A–C is "delivered" or "certified" (for example `WP-BAE-001` Charter `:131`, `:170`; the investigation `:142`). Per `IRA-WP-23-AC §7.1` these are correctable only after acceptance and commit (P-11) | `git grep` on HEAD | No (condition C-4, post-commit) |

**No Critical, High or Medium code defect. No `§19.8.5`-class defect open.**

## 7. Proposed WP-23 A–C Commit Boundary

**Include** (explicit paths; `git add -A` and `git add .` are prohibited):

1. **Code, all under `Backend/Services/AuthService/`**, 12 paths:
   - `alembic/versions/2026_09_22_0900-a7b8c9d0e1f2_bar_identifier_ledger.py`
   - `alembic/versions/2026_09_22_1000-b8c9d0e1f2a3_bar_registration.py`
   - `models/bar_identifier_ledger.py`, `models/bar_registration.py`
   - `repositories/bar_identifier_repository.py`, `repositories/bar_registration_repository.py`
   - `services/bar_identifier_service.py`, `services/bar_registration_service.py`
   - `tests/test_bar_identifier_service.py`, `tests/test_bar_registration_service.py`, `tests/test_bar_transaction_safety.py`
   - `models/__init__.py` (the whole-file diff is BAR-only)
2. **WP-23 governance documents:**
   - `architecture/00-Governance/BAR-INDEX.md`
   - `architecture/05-Implementation/WP-23_Enterprise_BAR_Mechanism_Implementation_Charter.md`
   - `architecture/05-Implementation/IMP-REPORT-WP-23_Enterprise_BAR_Mechanism.md`
   - `architecture/06-Reviews/ENTERPRISE-BAR-MECHANISM-DESIGN-AND-IMPLEMENTATION-READINESS.md`
   - `architecture/06-Reviews/ROD-ENTERPRISE-BAR-Decision-Preparation.md`
   - `architecture/06-Reviews/BAR_ENTERPRISE_MECHANISM_DECISION_INVESTIGATION.md`
   - `architecture/06-Reviews/IRA-WP-23-AC_BAR_Workstreams_A-C_Closure_Readiness.md`
   - `architecture/06-Reviews/ROD-WP-23-AC-BAR-Registry-Authority-Decision-Preparation.md`
   - `architecture/06-Reviews/CERT-WP-23-AC_BAR_Workstreams_A-C.md`
   - `architecture/06-Reviews/VV-AUDIT-WP-23-AC_BAR_Workstreams_A-C.md`
   - `architecture/06-Reviews/VV-AUDIT-WP-23-AC_BAR_Workstreams_A-C_Gate-4.md`
   - `architecture/06-Reviews/RRA-WP-23-AC_BAR_Workstreams_A-C_Release_Readiness_Audit.md` (this file)
3. **Partial hunks** (a prepared patch applied with `git apply --cached`):
   - `architecture/00-Governance/WPR-001_Work_Package_Roadmap.md`: **only** the WP-23 note (`+125-126`) and the WP-23 row (`+133`), after C-2 synchronization. **Exclude** the WP-22 row and note.
   - `architecture/06-Reviews/TECH-DEBT.md`: **only** the new WP-23 A–C entries created under C-1. **Exclude TD-170.**

**Exclude**, because it belongs to other Work Packages or other authority:
- **WP-BAE-001 M2:** TD-170, `IRA-BAE-001-M2_…`, `ROD-BAE-001-M2-…`.
- **WP-22/C-024:** the Charter, `IRA-C024*`, `TDS-C024*`, `C-024_…Investigation`, `ROD-C024-*`, `ADR-041`, and the `CBOR-INDEX.md` and `SER-001` hunks.
- **C-040/D-002, SD-002 and meta-governance:** `ROD-C040-*`, `ROD-Meta-*`, `ROD-SD002-*`, `ADR-027` to `ADR-035`, the `CAP-001`, `ADR-002`, `CANONICAL-ENTERPRISE-SEARCH-…` and delivery-map hunks, `ROD-ADR-002-*`.
- **Other:** `CLAUDE.md`, `IRA-C114_…`, `*.xlsx`, `AUREX_ENTERPRISE_FEATURE_CAPABILITY_COVERAGE_MATRIX.md`, `Sarika_consent.png`.

**Evidence that the boundary is self-consistent:** `wp23_tree` (HEAD plus exactly item 1 and `BAR-INDEX.md`) produced a single head `b8c9d0e1f2a3` and **982/982** passing. The governance files do not affect the build.

## 8. What Remains Before WP-23 A–C Can Be Accepted and Committed

1. **C-1** (before acceptance): register the Technical Debt (G5-01).
2. **C-2** (before or in the commit): synchronize the WP-23 governance status (G5-02).
3. **Repository Owner acceptance** of the A–C tranche under RD-23-02, on the basis stated under **C-3**.
4. **The WP-23 A–C commit**, with the §7 boundary.
5. **Post-commit:** the P-11 / C-4 stale-statement reconciliation. Only after that is RD-M2-01's precondition for M2 satisfied, and M2 itself still needs its own authorization and RD-M2-02.

## 9. Conditions

| ID | Condition | Blocks commit? |
|---|---|---|
| **C-1** | Add `TECH-DEBT.md` entries (with ID, Description, Raised In, Priority, Planned Resolution, Status and a `§19.8.7` severity) for the following, or cross-reference them to existing IDs where `§19.8.3` allows: CERT-F-04 / GAP-23-03-1 and 2 (with the hard "before any execution-eligibility consumer" precondition; see G5-08); CERT-F-05 and F-13 (non-evidential or misnamed tests); CERT-F-08 / VV-F-04 (drift); CERT-F-14 / VV-F-05 (allocator duplication and overflow); VV-F-06 (no format CHECK); G4-O-01 (append to TD-096); and G5-07 (PostgreSQL/asyncpg verification before the first real registering act). O-01 goes to Repository Owner visibility, not to TD | **Yes.** Gate 1 made it an acceptance prerequisite, and `§19.8.2` requires it |
| **C-2** | A dated, strikethrough-preserving status synchronization of ST-1 to ST-13 in the WP-23 documents (IRA-WP-23-AC, IMP-REPORT, `BAR-INDEX.md`, the `WPR-001` WP-23 row, the ROD-WP-23-AC note and design §19 rows B/C). It records: `355ebbe`/`203bed1`; Gate 1 STOP with its blockers resolved; Gate 2 FAIL → Gate 3 → Gate 4 PASS; this Gate 5 result; VV-F-07 closed by later evidence; and the TD IDs from C-1. It must not claim WP-23 COMPLETE, CLOSED or CERTIFIED | **Yes**, as a closure sync. It can be made in the same commit or immediately before it |
| **C-3** | The Repository Owner's acceptance record for A–C states its basis: Gate 1 STOP was not re-issued, but every Gate 1 blocker is resolved (G5-06); Gate 2 FAIL was remediated and Gate 4 PASS; this Gate 5 PASS WITH CONDITIONS; terminal state ACCEPTED (RD-23-02); WP-23 remains OPEN. The Repository Owner may alternatively order a narrow Gate 1 resumption | It is the acceptance act itself, which precedes the commit |
| **C-4** | P-11: reconcile S-1 to S-12 and CERT-F-11 in committed documents per `IRA-WP-23-AC §7.1` | No. It follows the commit |

G5-03 to G5-05 are non-blocking and are recorded for Repository Owner visibility.

## 10. Integrity Statement

**What I ran:**
- read-only git (`rev-parse`, `log`, `show --stat`, `merge-base --is-ancestor`, `ls-files`, `status`, `diff`, `diff --cached`, `grep`, and `archive` into scratch);
- `alembic heads`/`history` and offline `--sql` rendering against a dummy PostgreSQL URL (no connection);
- pytest on the three BAR files and on the full AuthService suite, in-repo and in `wp23_tree`;
- my from-scratch probe `probe_g5.py` against the current code and the pre-fix snapshot;
- SHA-256 hashing.

**Scratch:** all scratch material is under `…\scratchpad\gate5\`: `head_tree/`, `wp23_tree/`, `prefix_tree/`, `probe_g5.py`, `probe_g5_output.txt`, `probe_g5_prefix_output.txt`, `pg_offline_*_g5.sql`, `full-suite-*.log`, `wp23_sha256.txt`, `gate5-status-start.txt`. The `prefix_snapshot/`, `gate1` to `gate4` and `commits/` directories were read only.

**What I did not do:**
- no code, migration, test, governance document, decision record or configuration was modified;
- no Business Activity was registered and no identifier was assigned;
- no M2, Workstream D or Workstream E work was done;
- no git state-changing command (add, commit, stash, checkout, reset or push) was run.

**Repository state:**
- `git status --porcelain --untracked-files=all` at the start was identical to `status-before-gate5.txt` (114 entries), and it was unchanged after all test and probe runs.
- The only change this audit introduces is this file, `architecture/06-Reviews/RRA-WP-23-AC_BAR_Workstreams_A-C_Release_Readiness_Audit.md`.
- `git diff --cached --name-only` is empty. Nothing is staged, committed or pushed.
