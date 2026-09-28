# VV-AUDIT-WP-23-AC — Verification & Validation Audit (Gate 2): Enterprise BAR Workstreams A–C

**Gate:** CLAUDE.md §19.7b Gate 2 (Verification & Validation Audit)
**Object under review:** WP-23 Workstreams A–C tranche. This covers Enterprise Business Activity Registry (BAR) identifier issuance (Workstream B) and registration (Workstream C). It also covers the BAR-INDEX.md governance catalogue (Workstream A), but only for the "no side effects / zero registration" checks.
**Date:** 2026-09-25
**Verdict:** **GATE 2 FAIL.** One High-severity data-integrity finding (VV-F-01) cannot be deferred under §19.8.5. §19.7b Gates 3–4 are required.

---

## 1. Independence Statement

A fresh-context reviewer wrote this audit. The reviewer had no role in implementing WP-23 A–C, in Gate 1 (Independent Certification) or in any other gate. Every probe listed below was written from scratch for this audit. The implementer's 22 tests (`tests/test_bar_identifier_service.py`, `tests/test_bar_registration_service.py`) were read only to understand the harness. They were **not** adapted into probes and are **not** counted as evidence for any conclusion. They were run once, for context only (22 passed). Governance documents were read for context, and their claims were not trusted.

## 2. Environment Used

| Item | Value |
|---|---|
| Database | **SQLite (file databases, `sqlite+aiosqlite`)**. **No PostgreSQL was available.** No local installation was found (`psql` and `pg_ctl` are absent). The Docker CLI is present but the daemon was not running (`docker info` failed). Per instruction, no services were started or installed |
| Python / libs | `Backend/Services/AuthService/venv` — SQLAlchemy 2.0.50, alembic 1.18.4, aiosqlite 0.22.1 |
| FK enforcement | `PRAGMA foreign_keys=ON` is issued on **every** DBAPI connection by a SQLAlchemy `connect` event listener on each probe engine (`make_engine()` in `probes.py`) |
| FK positive control (P0a/P0b) | `PRAGMA foreign_keys` = **1,1** on two concurrently-open pooled connections, and **1** inside the probe session. An orphan `bar_registration` insert was **rejected by the database**: `IntegrityError('FOREIGN KEY constraint failed')`. No other FK probe was counted before this control passed |
| FK negative control (P5) | On an identical engine with `PRAGMA foreign_keys=OFF` (pragma=0), the **same orphan insert was accepted**: `bar_registration=[('BA-424242',)]` with 0 ledger rows |
| Harness replica (P5b) | An engine configured exactly like `tests/conftest.py` (no listener) reports `PRAGMA foreign_keys = 0` |
| Schema source for probes | `golden_head.db`. Its BAR tables were created by the **real BAR migrations** (`a7b8c9d0e1f2`, `b8c9d0e1f2a3`) through `alembic upgrade head`, not by `create_all` (see §5) |
| Scratch location | `C:\Users\ashit\AppData\Local\Temp\claude\C--Ashit-corpstage-enterprise-operating-system\a7a13f8c-d9da-479f-b7b3-b6b4826d4e72\scratchpad\gate2\` (abbreviated `$S` below). Nothing was written into the repository except this file |
| Env vars | `JWT_SECRET_KEY=ci-test-secret-key-not-for-production JWT_ALGORITHM=HS256` (TD-010), `PYTHONDONTWRITEBYTECODE=1`, `DATABASE_URL=sqlite+aiosqlite:///<scratch db>` for alembic |

**NOT VERIFIED ON PRODUCTION DIALECT (PostgreSQL).** None of the following is claimed as passed:
- the `substr`/`CAST(... AS INTEGER)` allocator at runtime;
- `server_default` behaviour;
- CHECK and UNIQUE semantics under PostgreSQL;
- `VARCHAR(n)` length enforcement. On PostgreSQL an over-length field raises `DataError`/`StringDataRightTruncation`, which is *not* an `IntegrityError` and so takes a different exception path through `register()`;
- `DateTime(timezone=True)` round-trip. SQLite returned naive datetimes (P1c);
- row-level lock and concurrency semantics;
- full-chain `alembic upgrade head` from base.

Static PostgreSQL DDL was compiled offline for comparison only (§5.3).

## 3. Sources Read

- Code: `models/bar_identifier_ledger.py`, `models/bar_registration.py`, `repositories/bar_identifier_repository.py`, `repositories/bar_registration_repository.py`, `repositories/base_repository.py`, `services/bar_identifier_service.py`, `services/bar_registration_service.py`, `models/database.py`, `config.py` (DATABASE_URL override)
- Migrations: `alembic/versions/2026_09_22_0900-a7b8c9d0e1f2_bar_identifier_ledger.py`, `alembic/versions/2026_09_22_1000-b8c9d0e1f2a3_bar_registration.py`, `alembic/env.py`, `alembic.ini`
- Harness: `tests/conftest.py`
- Governance: `IRA-WP-23-AC_BAR_Workstreams_A-C_Closure_Readiness.md` §9.2 (G2-1..G2-13 and the parity checklist), `BAR-INDEX.md` (§1–§4, §8), `CLAUDE.md` §19.7b, §19.8.5, §19.8.7. The IMP-REPORT, the Charter, the ROD (RD-23-03 Option D: `bar_registration` = runtime execution registration) and the Design §4/§5/§16 were consulted for context only

## 4. Probe Table

Scripts: `$S/probes.py` (main suite), `$S/probe_batch_loss.py` (P6h), `$S/probe_batch_loss_control.py` (P6h control), `$S/make_base.py`, `$S/dump_schema.py`, `$S/parity.py`.
Main command (from `Backend/Services/AuthService`): `PYTHONPATH=. venv/Scripts/python.exe $S/probes.py` → output in `$S/probes_output.txt`. P6h output is in `$S/probe_batch_loss_output.txt`, and its control output in `$S/probe_batch_loss_control_output.txt`.

| ID (IRA map) | What | Observed result | Result |
|---|---|---|---|
| P0a/P0b | FK positive control | pragma 1,1 on two connections. Orphan raw-SQL insert → `FOREIGN KEY constraint failed` | PASS |
| P1 (req. 1) | Positive registration via `BarRegistrationService` on the migrated DB | 1 row with all 8 fields: `('BA-000001','Probe BA','C-999','WP-99','REGISTERED','VV-PROBE-ACT',<timestamp>,0)`. The identifier matches `^BA-\d{6}$`. A matching ledger row exists | PASS |
| P1b | Sequencing and retroactive flag | `BA-000001` → `BA-000002`. `is_retroactive=True` is stored as 1 | PASS |
| P1c | Timestamp round-trip | SQLite returns a naive datetime (`tzinfo=None`) | INFO (PG not verified) |
| P1d | Whitespace-only required fields | All four were rejected with `ValueError`, and no ledger row was consumed | PASS |
| P2a/P2b (G2-3) | Service duplicate `(wp, ref)` | `BarRegistrationAlreadyExists`. Ledger count was 1 before and 1 after, even after the caller committed | PASS |
| P2c/P2d (G2-3) | Duplicate on the race path (pre-check blinded once, so the database UNIQUE constraint fires) | UQ backstop → "raced" branch → `BarRegistrationAlreadyExists`. Ledger 1, registrations 1 | PASS |
| P2e (G2-3) | Direct-insert duplicate `(wp, ref)` | `UNIQUE constraint failed: bar_registration.owning_work_package, bar_registration.business_activity_reference` | PASS |
| P2f (G2-2) | Direct duplicate `identifier` in the ledger | `UNIQUE constraint failed: bar_identifier_ledger.identifier` | PASS |
| P2g (G2-2) | Direct duplicate `identifier` in the registration table | `UNIQUE constraint failed: bar_registration.identifier` | PASS |
| P2h | Reference normalization | `'Probe BA '` (trailing space) was accepted as distinct from `'Probe BA'` | INFO (see O-01) |
| P3a (G2-4) | CHECK constraint on status: `DRAFT`, `registered`, `NOT_REGISTERED`, `''` | All rejected: `CHECK constraint failed: ck_bar_registration_status` | PASS |
| P3b | Status omitted | The migration's `server_default` supplies `REGISTERED` (SQLite) | PASS (PG not verified) |
| P3c (G2-8) | Digit boundaries | Seeds `BA-000009`, `BA-000099`, `BA-099999` produced `BA-000010`, `BA-000100`, `BA-100000` | PASS |
| P3d (G2-8) | `BA-999999` + 1 | `issue_identifier()` returned **`'BA-1000000'`** (10 chars, **fails** `^BA-\d{6}$`). The next `register()` returned `'BA-1000001'`. There was no exception and no guard. `String(20)` does not constrain it | OBS → VV-F-05 |
| P3e (G2-8) | Reuse after a rolled-back issuance | A rolled-back `BA-000001` was re-issued as `BA-000001` (persisted once), then `BA-000002`. No duplicate | PASS |
| P3f | Non-numeric ledger value (direct write) | `'BA-XYZ'` was accepted (no format CHECK). SQLite `CAST` gives 0, so the allocator continued. On PostgreSQL `CAST('XYZ' AS INTEGER)` would raise | OBS → VV-F-06 (PG not verified) |
| P4/P4b/P4c (G2-1) | Orphan `bar_registration`, both raw SQL and ORM model, FK ON | Both rejected by the **database** (`FOREIGN KEY constraint failed`). 0 rows remain | PASS |
| P5 (G2-13) | Negative control, FK OFF | Identical orphan **accepted** | PASS (control behaves as expected) |
| P6a/P6b (G2-5) | Failure after the ledger add and before the flush completes (`is_retroactive=None` → NOT NULL violation) | Neither row survives (ledger 0, registration 0). **However**, the non-collision `IntegrityError` was treated as an identifier collision: it was retried 5×, surfaced as `BarRegistrationAllocationExhausted`, and emitted a DENIED audit with reason `"BA-NNNNNN allocation exhausted retries during registration"` | Atomicity PASS. Misclassification → VV-F-02 |
| P6c | Non-DB failure after the ledger add (injected `RuntimeError` in `registration_repo.create`) | The exception propagates with no cleanup. `session.new=['BarIdentifierLedger:BA-000001']`. A caller that catches the exception and commits persists an orphan issued identifier (ledger `['BA-000001']`, 0 registrations) | OBS → VV-F-07 |
| P6d-pending / P6d-flushed (G2-7) | Unrelated caller `Person`, pending or flushed, in the same session, then one lost identifier race inside `register()` | `register()` returned `BA-000002` normally. The Person was expunged from the session. **persons after caller commit = `[]`: caller work SILENTLY DISCARDED** in both modes. The service's query autoflushes the "pending" object first, so both modes end up the same | **FAIL → VV-F-01** |
| P6e (G2-7) | Same, duplicate race path | persons after caller commit = `[]`: discarded | **FAIL → VV-F-01** |
| P6f (G2-7) | Same, fast-path duplicate (no rollback) | The Person survived | PASS |
| P6g (G2-7) | Same, `issue_identifier()` with one lost race | Returned `BA-000002`. persons after caller commit = `[]`: discarded | **FAIL → VV-F-01** |
| **P6h** (G2-7, extended) | Two `register()` calls in one caller session. The first succeeds. The second loses one identifier race (genuine database UNIQUE violation via a stale MAX read) | The caller was handed **first=`BA-000002`** ("First BA") **and second=`BA-000002`** ("Second BA"). After the caller commits, the registrations are `[('BA-000002','Second BA')]`. **"First BA" was silently un-registered, and its already-returned identifier now belongs to a different Business Activity.** Duplicate-race variant: after the first succeeds and the second raises `AlreadyExists`, the caller's first registration is also gone | **FAIL → VV-F-01** |
| P6h-control | The same sequence with no forced collision | first=`BA-000002`, second=`BA-000003`. Both persisted. This proves the loss is caused by the rollback path | Control OK |
| P7a-register / P7a-issue (G2-6) | Two consecutive lost races (another connection commits the candidate after the service reads MAX) | Obtained `BA-000003`. Ledger `[BA-000001..3]`, unique. 3 allocator calls | PASS |
| P7b-register / P7b-issue (G2-6) | Exhaustion (every attempt loses) | `BarRegistrationAllocationExhausted` / `BarIdentifierAllocationExhausted` after 5 attempts. Ledger = 5 rows, all from the competing connection. 0 registrations. No partial rows | PASS |
| P8a (G2-9) | Two sessions (aiosqlite worker threads) registering distinct refs concurrently | Both read MAX=0. A flushed and committed. B was blocked by SQLite's write lock, collided, rolled back, re-read MAX=1 and got `BA-000002`. Ledger unique | PASS on SQLite. **NOT VERIFIABLE HERE for PostgreSQL row-level concurrency** |
| P8b (G2-9) | Two sessions racing the **same** ref | One got `BA-000003`. The other raised `BarRegistrationAlreadyExists` through the concurrent branch. 1 registration. No extra ledger row | PASS on SQLite. **NOT VERIFIABLE HERE for PG** |
| P11/P11b (G2-11) | Read surface | Hits returned, and absent keys → `None`. `count_*` correct. **0 flush/commit events. Only `SELECT` statements emitted.** Session new/dirty/deleted = 0. Empty tables → counts 0, max 0 | PASS |
| P9 / G2-12 | Zero unintended registration | See §7 | PASS |
| G2-10 | Migrations | See §5 | PASS for BAR revisions on SQLite. Full chain NOT VERIFIED |

## 5. Migration Evidence (G2-10 / G1-4 parity)

### 5.1 Full chain

On a clean scratch SQLite DB (`$S/mig_full.db`), `alembic upgrade head` **fails at revision `b3f7a1c9d2e4` (organization_lifecycle_profile_fields, the 2nd migration of the chain)**. The error is `NotImplementedError: No support for ALTER of constraints in SQLite dialect` (log: `$S/mig_full_upgrade.log`). This failure predates WP-23 and is not a BAR defect, but it means **full-chain application is NOT VERIFIED** in this environment.

### 5.2 What was done instead

1. `make_base.py` built every non-BAR table (28) with `create_all`.
2. `alembic stamp f6a7b8c9d0e1` (the BAR migrations' parent).
3. `alembic upgrade head`. This ran the real BAR migrations: `f6a7b8c9d0e1 → a7b8c9d0e1f2 → b8c9d0e1f2a3`. `current` = `b8c9d0e1f2a3 (head)`.
4. `downgrade -1` → `bar_registration` and its index were dropped (29+1 tables, version `a7b8c9d0e1f2`).
5. `downgrade -1` → `bar_identifier_ledger` and its index were dropped. No `bar_*` table, index or autoindex remained. Version `f6a7b8c9d0e1`.
6. `upgrade head` again. The schema dump is **byte-identical** to the first upgrade (`diff schema_up1.txt schema_up2.txt` → IDENTICAL).

**No residue.**

### 5.3 Model vs migration parity

Evidence: `$S/parity.txt`, `$S/schema_up1.txt`, and `$S/pg_offline_upgrade.sql` (the migrations compiled to PostgreSQL offline via `alembic upgrade f6a7b8c9d0e1:head --sql`; no server).

- **Equivalent (enforcement semantics):** column set, types, and nullability; `registration_status` `server_default 'REGISTERED'`; FK `identifier → bar_identifier_ledger.identifier`; UNIQUE(identifier) on both tables; UNIQUE(owning_work_package, business_activity_reference); CHECK `registration_status = 'REGISTERED'`.
- **Drift.** `alembic compare_metadata(models, migrated DB)` reports 6 BAR diffs:
  1. **Ledger:** the model (`unique=True, index=True`) produces a **UNIQUE INDEX `ix_bar_identifier_ledger_identifier`** and no named constraint. The migration produces a **UNIQUE CONSTRAINT `uq_bar_identifier_ledger_identifier` plus a non-unique `ix_bar_identifier_ledger_identifier`**. The same index name has different uniqueness, and the migrated DB carries a redundant second index.
  2. **Registration:** the migration adds a non-unique `ix_bar_registration_identifier` that the model does not declare. It is redundant with the UNIQUE constraint.
  3. **Constraint names:** the migration names `pk_*`, `fk_bar_registration_identifier` and `uq_bar_registration_identifier`. The model leaves the PK, FK and single-column UNIQUE unnamed (no naming convention on `Base.metadata`), so dialect-generated names will differ.
  4. **`id` type** (`UUID` vs `CHAR(32)`) is reported on SQLite only. This is a reflection artifact and is not meaningful on PostgreSQL, where both are `UUID`.

- **Does the create_all harness matter?** Yes, in two ways:
  - (a) FK is not enforced at all (§8).
  - (b) The harness schema differs from production in index and constraint shape and names. Any future test or code that relies on constraint *names* (for example, parsing `uq_bar_registration_wp_reference` from an error) would behave differently.

  Enforcement semantics are otherwise equal. See VV-F-03 and VV-F-04.

## 6. Negative Control Evidence

- **FK (G2-13):** the P4 orphan insert was rejected with FK ON and accepted with FK OFF (P5). The engine configured like `conftest.py` reports `foreign_keys=0` (P5b). The existing BAR tests therefore provide **no** FK evidence.
- **VV-F-01:** the P6h control (identical call sequence with no forced collision) persists both registrations with distinct identifiers. The loss in P6h is therefore caused specifically by the `session.rollback()` inside the collision and race branches.

## 7. Zero Unintended Registration (req. 9 / G2-12)

- The `BAR-INDEX.md` §3 Register contains only `*(no entries)*`. Its SHA-256 before and after all probes is `6f5307f8a2aae1b9b61f73f72395ee2825fefbf01a0c79cb70be301e441479f5`, and `cmp` confirms it is byte-identical. The services do not write it.
- **No code outside tests calls the BAR services.** Repository-wide grep, excluding `venv`, `node_modules`, `.git` and `.claude`, found `register()`/`issue_identifier()`/`BarRegistrationService`/`BarIdentifierService` only in `tests/test_bar_*.py` and in docstrings and comments of the BAR modules themselves. No router or `main.py` reference exists. `Backend/Runtime/BusinessActivityEngine/tests/test_package_boundary.py:60` explicitly asserts non-import. Other `.register(` hits are unrelated (`ResolverRegistry`, AIService `EventRegistry`/search).
- **Database files in the working tree:** `Backend/Services/AIService/aurex.db`, `Backend/Services/AuthService/dev_manual_check.db`, and three `.claude/worktrees/*/aurex.db`. All are untracked or ignored, and all were opened read-only (`mode=ro`). **None contains any `bar_*` table**, so they hold no registration rows. Any external PostgreSQL database configured in `Config/platform-config.yaml` was not accessible and is **NOT VERIFIED**.

## 8. Harness / Production-Parity Checklist (§19.7b)

1. **Does the test harness enforce every constraint production enforces?** **No.**
   - **FK:** not enforced. `tests/conftest.py` builds `sqlite+aiosqlite:///:memory:` with no `PRAGMA foreign_keys=ON` (P5b confirms 0). Only `tests/test_access_evaluation_service.py:243` enables it locally, and the BAR tests do not.
   - **CHECK and UNIQUE:** SQLite enforces them (P2/P3), so they are exercised.
   - **Schema:** built by `Base.metadata.create_all`, not by migrations, so constraint and index names and shapes differ from production (§5.3).

   **Is a harness change required before acceptance?** Gate 2 has independently established FK enforcement in an enforced environment (P4/P5), so the FK gap does not by itself block acceptance and can be recorded as Technical Debt (VV-F-03, Medium). However, the Gates 3–4 remediation of VV-F-01 should add its regression evidence under an FK-enforced session, because the defect involves the ledger and registration FK pair.
2. **Does any test need multi-tenant coverage?** **Not applicable.** The migrated DDL of both tables (§5.3, `schema_up1.txt`) has **no `organization_id` or tenant column**, and the migrations state that BAR is platform-global metadata. No tenant-isolation probe applies.

## 9. Findings

Severity follows the §19.8.7 rubric. §19.8.5 is applied: data-integrity defects cannot be deferred as debt.

| ID | Severity | Description | Evidence | Blocks acceptance |
|---|---|---|---|---|
| **VV-F-01** | **High** | **Session-wide `rollback()` inside the services silently destroys caller work, including prior BAR registrations, and can hand one identifier to two Business Activities.** `BarRegistrationService.register()` (collision and concurrent-duplicate branches) and `BarIdentifierService.issue_identifier()` (collision branch) call `session.rollback()` on the caller's session after an `IntegrityError`. This discards **all** pending *and* flushed-but-uncommitted work in that session, and then the service **returns normally**. The caller commits believing its earlier work persisted. In P6h, one caller registering two Business Activities in one session received `BA-000002` for "First BA" and then `BA-000002` again for "Second BA". After commit only "Second BA" exists, so "First BA" is silently unregistered and its returned identifier now denotes a different Business Activity. This defeats D2's "canonical identity" responsibility and SD-002-004's "globally unique, permanent identifier" for a subset of cases (any batch or multi-step caller, such as the future Workstream F retroactive cutover, that meets one identifier collision or duplicate race). It is a data-integrity defect under §19.8.5, so it **cannot be deferred as debt**. It is latent today, because no non-test caller exists (§7). The implementer's own docstring in `bar_registration_service.py` names this hazard as the reason for not calling `issue_identifier()` ("rolls back the *entire session* … unsafe to interleave"), yet `register()` has the same property toward its caller. None of the existing 22 tests detects it (they pass) | P6d-pending, P6d-flushed, P6e, P6g, P6h. Control P6h-control. Scripts `probes.py`, `probe_batch_loss.py`, `probe_batch_loss_control.py` | **Yes.** Gates 3–4 required |
| VV-F-02 | Medium | **Any `IntegrityError` is treated as an identifier collision.** A non-collision constraint failure (for example NOT NULL on `is_retroactive`) is retried 5×, surfaces as `BarRegistrationAllocationExhausted` ("retry"), and writes a DENIED audit record with the false reason "allocation exhausted retries". This is misleading for diagnostics and for the audit trail. Atomicity itself held (no rows survive) | P6a, P6a2 | No on its own (recordable as TD). The natural fix site is the same code as VV-F-01, so it is recommended to be resolved in the same remediation |
| VV-F-03 | Medium | **Harness parity gap:** the shared harness enforces no FKs and builds the schema via `create_all` rather than migrations. No existing BAR test yields FK evidence | P5, P5b. `conftest.py`. §5.3 | No. Record as TD. Remediation evidence for VV-F-01 should run FK-enforced |
| VV-F-04 | Low | **Model/migration drift:** ledger UNIQUE index vs UNIQUE constraint plus a redundant non-unique index with the same name `ix_bar_identifier_ledger_identifier`; an extra redundant `ix_bar_registration_identifier`; unnamed vs named PK/FK/UQ. Autogenerate reports 6 BAR diffs. Enforcement semantics are equivalent | `parity.txt`, `schema_up1.txt`, `pg_offline_upgrade.sql` | No |
| VV-F-05 | Low | **Width overflow:** after `BA-999999` the allocator silently issues `BA-1000000`, `BA-1000001`, which violate the `BA-NNNNNN` six-digit format (`^BA-\d{6}$`). There is no guard and no error. The capacity of 999,999 is far beyond the current population of 21 | P3d | No |
| VV-F-06 | Low | **No database-level format CHECK on `identifier`.** A non-conforming value written directly to the ledger (for example `BA-XYZ`) is accepted. On SQLite the allocator tolerates it (`CAST` → 0). On PostgreSQL, `CAST('XYZ' AS INTEGER)` would make `max_identifier_sequence()` raise, which would halt all issuance (**NOT VERIFIED ON PRODUCTION DIALECT**). Reachable only by writes that bypass the service | P3f | No |
| VV-F-07 | Low | **No cleanup on non-`IntegrityError` failure after the ledger add.** The pending ledger row stays in the session. A caller that catches the exception and commits persists an orphan issued identifier. The standard `get_session` dependency rolls back on exception, so the default path is safe | P6c | No |
| O-01 | Info | `business_activity_reference` is not normalized: a trailing-space variant is a distinct registration. No source defines normalization, so this is recorded only as an observation for the Repository Owner, not as a defect | P2h | No |

## 10. Overall Verdict

**GATE 2 FAIL.**

**What passed** (SQLite, FK-enforced):
- database-level FK, UNIQUE and CHECK enforcement, with positive and negative controls;
- duplicate-registration protection through the service, the race branch and direct insert;
- cross-table atomicity of a single `register()` call;
- collision retry and exhaustion;
- sequential and digit-boundary allocation;
- SQLite-level concurrency;
- the read-only read surface;
- BAR migration upgrade/downgrade/re-upgrade with no residue;
- zero unintended registration.

**What failed:** VV-F-01 (High) is a non-deferrable data-integrity defect under §19.8.5. §19.7b Gate 3 (remediation) and Gate 4 (independent verification of remediation, including a negative control that runs `probe_batch_loss.py` against the pre-fix code) are required before Repository Owner acceptance. VV-F-02 to VV-F-07 are non-blocking and may be remediated alongside VV-F-01 or recorded in `TECH-DEBT.md`.

**What was not verified:** everything specific to PostgreSQL (§2) and full-chain migration application (§5.1).

## 11. Integrity Statement

**What was run:**
- read-only inspection of the listed sources;
- `alembic heads/stamp/upgrade/downgrade/current` against scratch SQLite files only, with `DATABASE_URL` pointing into `$S`, and offline `--sql` compilation against a dummy PostgreSQL URL (no connection);
- the probe scripts listed in §4, all located in `$S`, run with the service directory on `PYTHONPATH` and `PYTHONDONTWRITEBYTECODE=1`;
- read-only (`mode=ro`) inspection of working-tree `.db` files;
- one context-only run of the existing BAR tests (`pytest -p no:cacheprovider`, 22 passed).

**What was not done:** no repository code, test, migration, configuration, governance document or database file was modified. No git state-changing command was used.

**Repository state:** `git status --short` before the audit file was written was identical to the pre-audit baseline (147 pre-existing entries, left untouched). `git diff --cached --name-only` was empty. The only change this reviewer introduced is this file.

The final `git status --short` also showed a second new untracked file, `architecture/06-Reviews/CERT-WP-23-AC_BAR_Workstreams_A-C.md`. It appeared after this reviewer's mid-audit baseline check. This reviewer did **not** create it; it is presumably the concurrently dispatched Gate 1 reviewer's artifact. This reviewer did not read it, and it did not inform this audit.
