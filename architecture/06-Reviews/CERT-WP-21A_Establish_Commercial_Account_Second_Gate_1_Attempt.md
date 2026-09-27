# CERT-WP-21A — Gate 1 Independent Certification, **SECOND (FRESH) ATTEMPT** — Establish Commercial Account (C-022, WP-21 BA-01)

> **THIS IS A SECOND, FRESH GATE 1 ATTEMPT.**
> The **first** Gate 1 attempt — `architecture/06-Reviews/CERT-WP-21_Establish_Commercial_Account.md`, performed 2026-09-15 by a different independent reviewer — resulted in **❌ FAIL**, on exactly one Medium finding, `G1-M-01`: the mandatory `CLAUDE.md §19.7` Implementation Report `IMP-REPORT-WP-21` did not exist.
> **This reviewer independently finds `G1-M-01` RESOLVED** (§3 below).
> **This document does NOT replace, edit, supersede, or invalidate `CERT-WP-21`.** `CERT-WP-21` remains intact, unmodified, and authoritative as the historical record of the first Gate 1 attempt. It was not touched by this review.
> This is a complete, independent re-review of *everything* — not a spot-check of the single item that failed last time. Every dimension the first attempt recorded as PASS was independently re-derived from source here, and none of its conclusions was adopted on trust.

**Gate:** `CLAUDE.md §19.7b` Gate 1 — Independent Certification (second attempt).
**Work Package / BA:** WP-21 — C-022 Customer & Account Management, BA-01 "Establish Commercial Account".
**Governing chain (each artifact opened and read from disk by this reviewer):** `CAP-001` (C-022, line 76 — *"Manage customer relationships."*, Active, owning spec `COM-001`) → `COM-001 §4`/`§7`/`§10` (`COM-001-001`, `-002`, `-003`, `-033`, `-036`, `-060`, `-061`; LOCKED) → `PE-001-C022` v1.2 (`docs/Product/PE-001/capabilities/C-022/`) → `ROD-C022` (D1–D6, §H) → `IRA-C022` (§11) → `TDS-C022` (§4–§25) → `IRA-TDS-C022_Independent_Review.md` (PASS WITH CONDITIONS, `[C-1]`–`[C-7]`) → `ROD-C022-A` (D7, D8) → `ADR-038` (Accepted — Option A) → `ADR-039` (PROPOSED — preparation only) → `ROD-C022-B` (D9 = Option A, D10 = Option A) → `ADR-040` (Accepted — CBOR registration, `CAC-000001`) → `CBOR-INDEX.md §3` → `WPR-001` WP-21 row → `WP-21 … Charter` (§21, §25a) → implementation → `IMP-REPORT-WP-21` → `CERT-WP-21` (Gate 1 attempt #1, FAIL) → **this record (Gate 1 attempt #2)**.
**Date:** 2026-09-15.
**Repository HEAD at review:** `8323bf3976818ff463cf67e891bd2a0a953777fd` (verified by this reviewer via `git rev-parse HEAD`).

**Naming note.** Before choosing this filename, this reviewer enumerated `architecture/06-Reviews/CERT-*` for an existing re-certification precedent. The repository's own CERT-family precedent for a follow-on certification artifact is `CERT-WP-01A_Organization_Management_Correction.md` — a letter suffixed directly to the Work Package number. This document follows that CERT-family precedent (`CERT-WP-21A`) rather than the ROD-family `-A`/`-B` hyphenated pattern (`ROD-C022-A`/`ROD-C022-B`), which governs decision records, not certifications.

---

## CURRENT CERTIFICATION STATE

> ### ✅ **GATE 1 — INDEPENDENT CERTIFICATION (SECOND ATTEMPT): PASS WITH OBSERVATIONS**

- **Zero Critical findings. Zero High findings. Zero Medium findings.**
- **`G1-M-01` (the sole blocking finding of attempt #1): RESOLVED.** `IMP-REPORT-WP-21` now exists, satisfies every `CLAUDE.md §19.7` Implementation Report requirement, and every factual claim this reviewer sampled from it was independently confirmed against actual repository state.
- **Four Low, non-blocking findings**, all carried forward from `CERT-WP-21` and each **independently re-confirmed as still factually accurate** by this reviewer against current repository state (none was carried forward on trust). One of them (`G1-L-04`) is **extended** by two additional stale governance locations this reviewer found that attempt #1 did not name.
- **Seven non-blocking Observations.**
- **No `CLAUDE.md §19.8.5`-class defect** — no architectural, security, data-integrity, or tenant-isolation defect; no failing test; no build failure.
- **Tests: 21/21 targeted and 950/950 full regression, both executed by this reviewer personally**, not accepted from any prior report.

---

## 1. Reviewer independence (`CLAUDE.md §19.7` fresh-context requirement)

This reviewer had **no** involvement in, and **no** conversational memory of, the WP-21 / C-022 implementation, the authoring of `IMP-REPORT-WP-21`, the first Gate 1 review (`CERT-WP-21`), or any C-022 governance artifact (`ROD-C022`, `ROD-C022-A`, `ROD-C022-B`, `IRA-C022`, `TDS-C022`, `IRA-TDS-C022_Independent_Review.md`, the Charter, `ADR-038`, `ADR-039`, `ADR-040`).

Both `CERT-WP-21` and `IMP-REPORT-WP-21` were read **as evidence and as leads on where to look**, never as authority. Every material assertion in either was independently re-derived:

- every governance document was opened and read from disk;
- every implementation file was read in full;
- the targeted suite was executed by this reviewer;
- **the full ~950-test regression was executed by this reviewer** (attempt #1 explicitly declined to re-run it — this reviewer did not inherit that disposition);
- `alembic heads`, `alembic branches`, and `alembic history` were executed by this reviewer;
- `git rev-parse HEAD`, `git status --short`, `git diff --cached --name-only`, and targeted `git diff` were run by this reviewer;
- the live FastAPI application's **OpenAPI surface** was enumerated by this reviewer;
- a **purpose-built runtime probe, written from scratch and not adapted from the existing test suite**, was executed against the running application (§10.3).

Nothing below is synthesized from any implementing session's memory, and nothing is restated from `CERT-WP-21` without independent re-verification.

## 2. Scope of certification

WP-21 / C-022 BA-01 only — establish exactly one standalone Authoritative Commercial Account via `POST /commercial-accounts`, platform-global, `require_platform_admin`-gated, `AuthService`-hosted, per `ROD-C022 §H`/D1–D6 as constrained by `ROD-C022-A` D7/D8, `ROD-C022-B` D9/D10, `ADR-038` Option A, `ADR-040`, and the Charter §25a Implementation Authorization.

This record does **not** close C-022 as a capability, and does not advance, prejudge, or substitute for Gate 2 (V&V Audit), Gates 3–4 (Remediation and its Independent Verification), or Gate 5 (Release Readiness Audit).

---

## 3. STEP 1 (mandatory) — `G1-M-01` re-check and disposition

### 3.1 Existence

`architecture/05-Implementation/IMP-REPORT-WP-21_Establish_Commercial_Account.md` — **exists** (34,148 bytes, mtime `2026-09-15 22:16:18`, untracked/new; it postdates `CERT-WP-21`'s own mtime of `2026-09-15 21:35:16`, consistent with it having been authored as `G1-M-01`'s remediation). Read in full by this reviewer.

### 3.2 Conformance to `CLAUDE.md §19.7`'s Implementation Report requirements

| `§19.7` Implementation Report requirement | Where satisfied in `IMP-REPORT-WP-21` | Result |
|---|---|---|
| Governing chain identified | Header line 4 — full chain `CAP-001` → `COM-001` → `PE-001-C022` → `ROD-C022` → `IRA-C022` → `TDS-C022` → `IRA-TDS-C022` → `ROD-C022-A` → `ADR-038` → `ADR-039` → `ROD-C022-B` → `ADR-040` → Charter §25a. **Every cited artifact was confirmed by this reviewer to resolve to a real file.** | PASS |
| Repository Owner Implementation Authorization recorded | §1 — recorded, and verified by this reviewer against Charter §25a directly; the scope terms match | PASS |
| Authorized scope stated | §2 — matches Charter §25a / `ROD-C022 §H` | PASS |
| STOP-and-report events disclosed | §3 — "None," with the reason (both governance prerequisites resolved before authorization). Independently confirmed: `ADR-040` is Accepted and predates implementation; `ROD-C022-B` D10 is recorded | PASS |
| Explicit exclusions stated | §4 — full exclusion list, matching Charter §20 verbatim in substance | PASS |
| Files created / modified | §5.1 / §5.2 — **all 7 created and all 3 modified files independently confirmed** against `git status --short` and `git diff` | PASS |
| Implementation evidence | §5.3–§5.10 — schema, allocator, status semantics, security model, tests, audit, migration head, frontend N/A | PASS |
| Test results | §5.7 — 21 named tests, 21/21; full regression 950/950 with 71 warnings. **Both independently reproduced by this reviewer** (§10) | PASS |
| Traceability | §6 — a 16-row requirement→evidence matrix. This reviewer re-derived its own matrix (§4) independently and found no row unsupported | PASS |
| **Implementation Status marked "IMPLEMENTATION COMPLETE"** | Header line 5 and closing line 191 — both state `IMPLEMENTATION COMPLETE` | PASS |
| Known limitations | §8 — the four `CERT-WP-21` Low findings, each with impact and disposition | PASS |
| Explicit confirmations | §9 — 13 confirmations. Each was independently spot-checked by this reviewer; none was found false | PASS |
| Change control | §11 — baseline HEAD, one file created, nothing else touched, nothing staged/committed/pushed. **HEAD independently verified as `8323bf39…`** | PASS |
| Does not self-certify | §10 / §12 — explicitly states WP-21 is NOT certified, NOT closed, NOT release-ready, and that a fresh Gate 1 re-dispatch is a separate action not performed by the report. **This is the correct posture under `§19.7`'s no-self-certification clause** | PASS |

### 3.3 Independent verification of a sample of its factual claims

Claims sampled and checked against actual repository state — **not** accepted because the report looks complete:

| Claim in `IMP-REPORT-WP-21` | Independent verification | Result |
|---|---|---|
| Migration `revision='f6a7b8c9d0e1'`, `down_revision='e5f6a7b8c9d0'` (§5.1) | Read directly at migration L60–61 | ✅ accurate |
| Purely additive; no `ALTER`; no `SEQUENCE` (§3, §5.1) | Read the whole migration — one `create_table`, one `create_index`, `downgrade()` drops both. No `op.alter_*`, no `CREATE SEQUENCE` | ✅ accurate |
| Model has 8 columns; one `CheckConstraint`; self-FK on `parent_account_id`; no `organization_id`, no `classification` (§5.1, §5.3) | Runtime ORM introspection: exactly 8 columns `[id, account_reference, account_name, status, parent_account_id, created_by_actor_id, created_at, updated_at]`; `CheckConstraint:ck_c022_commercial_account_status`; `ForeignKeyConstraint`; `PrimaryKeyConstraint` | ✅ accurate |
| `_REFERENCE_SUFFIX_OFFSET = len("ACCOUNT") + 2 = 9` (§5.4) | Read repository L17; arithmetic verified (`ACCOUNT` occupies 1-based positions 1–7, `-` is 8, suffix starts at 9) | ✅ accurate |
| No `instr()`/`strpos()`/`position()` in the allocator (§5.4) | Read repository L59–63; and **executed** both portability tests, which compile under both dialects and intercept the actually-executed SQL | ✅ accurate |
| 21 test names, 21/21 passing (§5.7) | **Executed.** All 21 names match exactly; 21 passed, 0 failed | ✅ accurate |
| Full regression 950 passed, 0 failed, 71 deprecation warnings (§5.7) | **Executed by this reviewer: `950 passed, 71 warnings in 344.82s`.** Exact match on both figures | ✅ accurate |
| `alembic heads` → single non-branching head `f6a7b8c9d0e1` (§5.9) | **Executed.** `heads` → `f6a7b8c9d0e1 (head)`; `branches` → empty; `history` → 30 linear revisions | ✅ accurate |
| `git diff -- dependencies.py` returns empty (§5.6) | **Executed.** Empty | ✅ accurate |
| No file under `source/frontend/src` references `commercial-account`/`c022`/`C-022` (§5.1, §5.10) | **Executed** a case-insensitive recursive grep across `source/frontend/src` for all three tokens — zero hits | ✅ accurate |
| `CBOR-INDEX.md §3` carries the `CAC-000001` row (§5.2) | Read `CBOR-INDEX.md:40` — `\| CAC-000001 \| Commercial Account \| C-022 … \| ADR-040 \| IRA-C022 §11 \|` | ✅ accurate |
| `HEAD = 8323bf3976818ff463cf67e891bd2a0a953777fd` (§11) | **Executed** `git rev-parse HEAD` | ✅ accurate |
| `CERT-WP-21` not modified by the report's own pass (§11) | `CERT-WP-21` mtime `21:35:16` predates `IMP-REPORT-WP-21`'s `22:16:18` | ✅ consistent |

**One minor wording inaccuracy found** — recorded as Observation O-1 (§12), not as a finding: §5.3's closing sentence describes the index as *"`ix_c022_commercial_account_account_reference` (unique)"*. That is true of the **ORM** shape (`unique=True, index=True`, confirmed at runtime as `('ix_c022_commercial_account_account_reference', True)`) but not of the **migration** shape, where `op.create_index(...)` is non-unique and uniqueness is carried by a separate `sa.UniqueConstraint('account_reference', name='uq_c022_commercial_account_account_reference')`. The report's own §3 describes the migration correctly ("one `op.create_index` + one `UNIQUE`"), so this is loose phrasing in one sentence, not a materially misleading or fabricated claim. Uniqueness is enforced in both shapes, and the same ORM-versus-migration divergence exists verbatim in the already-certified C-021 precedent.

### 3.4 `G1-M-01` — explicit disposition

> ### ✅ **`G1-M-01`: RESOLVED.**

The artifact whose absence was the sole basis of attempt #1's FAIL now exists, satisfies every `CLAUDE.md §19.7` Implementation Report requirement enumerated at §3.2, carries an explicit Implementation Status of "IMPLEMENTATION COMPLETE", and is **usable as a certification input** — its factual claims were independently sampled and found accurate (§3.3), with one immaterial wording imprecision recorded as an Observation. It correctly refrains from self-certifying. `CERT-WP-21 §7`'s own recorded remediation instruction ("Author … following the `IMP-REPORT-WP-20` structure … Then re-dispatch Gate 1 to a further fresh-context reviewer. No implementation file requires any change.") was followed in full, and no implementation file was changed by that remediation — independently confirmed: every implementation file's mtime (`17:42`–`17:46`) predates both `CERT-WP-21` (`21:35`) and `IMP-REPORT-WP-21` (`22:16`).

---

## 4. Requirement / evidence matrix (independently re-derived)

Built by this reviewer from `ROD-C022 §H`/D1–D6, `ROD-C022-A` D7/D8, `ROD-C022-B` D9/D10, `ADR-038`, `ADR-040`, `TDS-C022 §6`–`§21`, and Charter §1–§21/§25a — read from source, not copied from any prior matrix. "Verified" means the construct was located in code and confirmed to do what the governing text requires.

| # | Requirement (source) | Evidence | Result |
|---|---|---|---|
| 1 | Table `c022_commercial_account` (`TDS §6.1`, Charter §8) | Migration L68 `op.create_table('c022_commercial_account', …)`; model L93 `__tablename__` | PASS |
| 2 | `id` UUID PK, default `uuid4` | Migration L69 + `PrimaryKeyConstraint('id', name='pk_c022_commercial_account')` L77; model L101–104 | PASS |
| 3 | `account_reference` String(30), NOT NULL, UNIQUE | Migration L70 + `UniqueConstraint(… name='uq_c022_commercial_account_account_reference')` L82; model L107–112 `unique=True, index=True`; runtime index `('ix_…', unique=True)` | PASS |
| 4 | `account_name` String(255), NOT NULL, **no** uniqueness invariant (`COM-001-033` states none; `TDS §6.1`) | Migration L71 — no unique constraint on the column anywhere in the file; model L119–122 | PASS |
| 5 | `status` String(20), CHECK `{active,suspended,retired}`, NOT NULL | Migration L72 + `CheckConstraint("status IN ('active','suspended','retired')", name='ck_…')` L83–86; model L94–99 identical; `ACCOUNT_STATUSES` L24 | PASS |
| 6 | BA-01 writes **only** `'active'` (`ROD-C022-A` D8, `TDS §9`, Charter §14) | Service L104 `"status": "active"` — the only `status` write in the module; no transition method exists. Empirically confirmed: 4/4 rows in this reviewer's own probe are `active` | PASS |
| 7 | `parent_account_id` nullable self-FK, declared, **never** written non-NULL (`TDS §10`, Charter §13) | Migration L73 + `ForeignKeyConstraint(['parent_account_id'], ['c022_commercial_account.id'], name='fk_…')` L78–81; model L132–135; service L105 `"parent_account_id": None` hard-coded. Probe: all rows `NULL` | PASS |
| 8 | `created_by_actor_id` UUID NOT NULL, **not** a FK (`TDS §6.1`) | Migration L74 — no `ForeignKeyConstraint` references it; model L138–140 has no `ForeignKey` | PASS |
| 9 | `created_at` NOT NULL / `updated_at` NULLABLE, `DateTime(timezone=True)` | Migration L75–76; model L147–157 | PASS |
| 10 | **No `organization_id`, no `tenant*` column** (`ROD-C022` D2, `TDS §6.1`/`§11`, Charter §12) | Absent from migration column list L69–76 and from ORM metadata (runtime-confirmed 8-column set). Executed `test_c022_table_has_no_organization_id_or_classification_column` (live `inspect()`) and `test_orm_model_declares_no_organization_id` (ORM metadata) | PASS |
| 11 | **No `classification` anywhere** (`ADR-038` Option A, `ROD-C022-A` D7, Charter §15) | Repo-wide grep over all six C-022 implementation files: **only** docstring/comment occurrences asserting its absence — zero code occurrences. Absent from migration, ORM, request schema, and response schema. Empirically confirmed: a body carrying `classification` is silently ignored and the 201 response has exactly 7 keys, none of them `classification` | PASS |
| 12 | `account_reference` SHALL be `PREFIX-NNNNNN` (`COM-001-001`, inherited by Section 7 per `COM-001` line 44 — re-verified verbatim by this reviewer) | Model L34 `ACCOUNT_REFERENCE_PREFIX = "ACCOUNT"`; service L158 `f"{PREFIX}-{current_max + 1:06d}"`. Observed live: `ACCOUNT-000043`, `ACCOUNT-000044`, `ACCOUNT-000045` | PASS |
| 13 | System-assigned; caller cannot supply or override (`TDS §8`/`§16`, Charter §6) | Request schema declares **exactly one** field, `account_name` (runtime-confirmed via OpenAPI). `account_reference`/`id`/`status`/`parent_account_id`/`created_by_actor_id`/`organization_id`/`tenant_id`/`classification` are structurally absent from the contract. Empirically confirmed by this reviewer's own injection probe (§10.3, PROBE 4) | PASS |
| 14 | Acceptance properties: system-assigned, monotonic, unique, concurrency-safe (`TDS §7`) | System-assigned (row 13); monotonic `MAX(suffix)+1` — **and independently probed against a pre-seeded non-zero base**: seeding `ACCOUNT-000042` yields `ACCOUNT-000043` then `ACCOUNT-000044` (§10.3, PROBE 1/2), which the existing suite never exercises; unique via UNIQUE constraint; concurrency-safe via UNIQUE backstop + allocate-and-retry (service L96–127) | PASS (see `G1-L-01` on retry-path coverage) |
| 15 | Allocator PostgreSQL-portable — fixed-offset `substr`, never `instr()`/`strpos()`/`position()` | Repository L17/L59–63 read directly. Verified **not** by the comment but by executing both guards: one compiles under PostgreSQL and SQLite dialects asserting all three functions absent and the two SQL strings byte-identical; the other attaches a `before_cursor_execute` listener and asserts the **actually executed** statement is clean | PASS |
| 16 | `POST /commercial-accounts`, 201, `Depends(require_platform_admin)` (`TDS §15`, Charter §10) | Router L26–29 + L57; `main.py:112` mounts at prefix `/commercial-accounts`. OpenAPI: `{'/commercial-accounts': ['post']}` | PASS |
| 17 | **No other route** (`ROD-C022-A` D8, Charter §20) | Router contains exactly one `@router.` decorator (L26). **OpenAPI enumeration of all 103 application paths** returns exactly one commercial-account path with exactly one method. Runtime-confirmed by the two absence tests (5 transition shapes + 2 read/list shapes, all 404/405) | PASS |
| 18 | Blank/missing `account_name` → 422 (`TDS §16`, Charter §7) | Schema `Field(..., min_length=1, max_length=255)` + `field_validator` rejecting whitespace-only. Both 422 tests executed and pass | PASS |
| 19 | Non-`PLATFORM_ADMIN` → 403; no-role → 403; missing/malformed `Authorization` → 400 (`TDS §19`) | Four tests executed and pass. **Extended by this reviewer's own probe**: six role variants (`ORG_ADMIN`, `TENANT_ADMIN`, `MEMBER`, `PLATFORM_ADMINX`, lowercase `platform_admin`, empty) **all 403** — no case-insensitive or near-miss bypass exists | PASS |
| 20 | Tenant-middleware exemption on the `/roles`/`/offerings` basis (`ROD-C022` D2, `TDS §12`, Charter §11) | `middleware/tenant.py` gains exactly one exemption line, `path == "/commercial-accounts" or path.startswith("/commercial-accounts/")` — exact-prefix-scoped (§8.3), plus a rationale comment citing `ROD-C022` D2 | PASS |
| 21 | Service host `AuthService`; no new service (`ROD-C022` D3, `TDS §5`/`§13`) | All files under `Backend/Services/AuthService`; file names match `TDS §13`'s prescribed layout exactly | PASS |
| 22 | Repository minimum methods (`TDS §14`) | `create()`/`get_by_id()` inherited from `BaseRepository`; `get_by_account_reference()` implemented (not route-wired, disclosed); `max_reference_sequence()` added for the allocator | PASS |
| 23 | Audit + event on establish (`TDS §17`) | Service L129–149 `record_audit(action="ESTABLISH_COMMERCIAL_ACCOUNT", status=SUCCESS, …)` + `publish_event("COMMERCIAL_ACCOUNT_ESTABLISHED", …)`, both existing mechanisms. Observed live in this reviewer's probe, including `"tenant_id": "PLATFORM"` | PASS |
| 24 | Migration additive, `down_revision = e5f6a7b8c9d0`, single non-branching head (`TDS §6.1`) | `alembic history` → 30 linear revisions; `heads` → `f6a7b8c9d0e1 (head)`; `branches` → empty | PASS |
| 25 | D9 — collapsed single-call lifecycle accepted (`ROD-C022-B` D9, Charter §16) | §6.1 below | PASS |
| 26 | D10 — BAR deferred, no mechanism/identifier (`ROD-C022-B` D10, Charter §18) | §6.2 below | PASS |
| 27 | CBOR registered `CAC-000001` (`ADR-040`, `COM-001-061`) | §11.1 below | PASS |
| 28 | `CLAUDE.md §20.3` backend-only honored (Charter §21) | §11.3 below | PASS |
| 29 | Purpose-built end-to-end runtime probe (`§19.7b` method note, Charter §19) | `test_end_to_end_establish_probe` exists and passes; **and this reviewer wrote and executed an additional, independent from-scratch probe** (§10.3) | PASS |

**No row was found unsupported, and no requirement in the governing set was found unimplemented.**

---

## 5. Scope control — absence verified by direct inspection

Each item below was confirmed absent by reading code and by runtime inspection — **not** by trusting any docstring that asserts its absence.

| Must be ABSENT | How verified | Result |
|---|---|---|
| Account `classification` (column / field / attribute) | Absent from migration DDL, ORM metadata (runtime 8-column set), request schema (OpenAPI: one property, `account_name`), response schema (7 fields). A body carrying `classification` is ignored; the 201 response has no such key | ABSENT |
| Customer; Customer–Account Relationship | No model, table, schema, service method, or route. No import of any Customer construct anywhere in the six C-022 files | ABSENT |
| Organization equivalence / wiring | No `organization_id` column; **zero imports** of `models.organization`, `organization_node`, or any C-004 construct in any C-022 file | ABSENT |
| Identity / Person wiring | **Zero imports** of `models.identity`, `models.person`, `models.membership`. `created_by_actor_id` is a bare UUID audit citation with **no** `ForeignKey` | ABSENT |
| Read / list / update / delete routes | OpenAPI enumeration of all 103 paths: only `POST /commercial-accounts`. Router has one decorator. `GET` collection, `GET` item, and `PATCH` all 404/405 at runtime | ABSENT |
| Lifecycle-transition operations (reclassify / retire / reactivate / transition) | No service method, no schema, no route. All four probed at runtime → 404/405. `status` has exactly one write site, the literal `"active"` | ABSENT |
| Merge / split / transfer (`ERB-C022-04`) | No construct of any kind | ABSENT |
| Subscription (C-020) / Billing (C-024) / Contract (C-025) / Entitlement (C-023) | **Zero imports** of any such module; no field, route, or service reference | ABSENT |
| CRM / sales-pipeline / case-management behavior | None | ABSENT |
| Frontend / UI | Recursive case-insensitive grep across `source/frontend/src` for `commercial-account`, `commercial_account`, `c022`, `C-022` → **zero files** | ABSENT |
| BAR mechanism / registry / Business Activity Identifier | Repository-wide `find` for `*BAR-INDEX*`, `*Business_Activity_Registry*`, `*BAR-REG*` → **no file exists**. No `business_activity*` / `activity_identifier` construct in any AuthService source file. No `BA-NNNNNN` identifier assigned to C-022 anywhere | ABSENT |

**Import-level confirmation (a check that cannot be defeated by a docstring):** the complete import set of all five C-022 modules is `uuid`, `datetime`, `typing`, `sqlalchemy`/`pydantic`/`fastapi`, `models.database`, `models.c022_commercial_account`, `repositories.base_repository`, `repositories.c022_commercial_account_repository`, `schemas.commercial_account`, `services.commercial_account_service`, `observability`, `dependencies`. **There is no coupling to any other domain whatsoever.**

---

## 6. D9 / D10

### 6.1 D9 — Collapsed single-call lifecycle (`ROD-C022-B` D9 = Option A) — HONORED

`ROD-C022-B:19` (read directly): *"D9 = Option A — ACCEPT COLLAPSED MINIMUM SLICE."* Anchor/Intent/Proposed/Assessment remain conceptually distinct roles per `COM-001-002`/`COM-001-003`; BA-01 may realize them internally within one externally invoked establish flow.

Implemented exactly so: **one** endpoint (`POST ""`), **one** public service method (`establish`). This reviewer searched the C-022 module set for any separately materialized Anchor, Intent, Proposed, or Assessment construct — **none exists** as a table, column, schema, service method, route, or enum. No implicit state machine and no hidden transition was introduced: `status` is written at exactly one site, as the fixed literal `"active"`, and no code path anywhere reads `status` to branch. **No unauthorized lifecycle policy was introduced.**

### 6.2 D10 — BAR deferred (`ROD-C022-B` D10 = Option A) — HONORED

`ROD-C022-B:20`/`:110` (read directly): no BAR registry, `BAR-INDEX`, database, or runtime mechanism is created; no Business Activity Identifier is assigned; the `COM-001-060` obligation remains **deferred**.

Repository-wide verification (not limited to the listed files) found **no BAR artifact of any kind**. No Business Activity Identifier is assigned to C-022 BA-01 anywhere.

`COM-001-060` was read verbatim by this reviewer: *"Every commercial action described in Sections 5–9 (establish, …) is a Business Activity per SD-002 §5, registered in the Business Activity Registry (IMP-001 §6.22) **once implemented**, per COM-001-005."* The execution-time obligation is **accurately described as deferred, never as satisfied**, in `IMP-REPORT-WP-21 §4`/`§6`/`§9`, the `WPR-001` WP-21 row, the `CBOR-INDEX.md §3` note, `ADR-040 §Decision item 5`, and Charter §18 — every one of which this reviewer read. This is visible, justified, recorded, and traceable, per `CLAUDE.md §19.8.6`. See Observation O-5 (§12) recording that the clause's own "once implemented" trigger has now actually fired, so the deferral must remain visible into Gates 2 and 5.

---

## 7. Data / migration

- **Revision id** `f6a7b8c9d0e1`; **`down_revision`** `e5f6a7b8c9d0` (WP-20 / `c021_offering_definition`) — read at migration L60–61.
- **`alembic heads`** (executed) → `f6a7b8c9d0e1 (head)` — exactly one head.
- **`alembic branches`** (executed) → **empty** — non-branching.
- **`alembic history`** (executed) → 30 revisions in a single linear chain, terminating at this migration.
- **Constraints:** `pk_c022_commercial_account` (PK on `id`); `uq_c022_commercial_account_account_reference` (UNIQUE); `ck_c022_commercial_account_status` (CHECK on the closed set); `fk_c022_commercial_account_parent_account_id` (self-referential FK).
- **Index:** `ix_c022_commercial_account_account_reference`.
- **Nullability / defaults:** `id`, `account_reference`, `account_name`, `status`, `created_by_actor_id`, `created_at` NOT NULL; `parent_account_id`, `updated_at` NULLABLE. Model carries `default='active'`, `default=uuid4`, `default=now()`, `onupdate=now()`.
- **ORM-versus-migration:** the column set, nullability, PK, CHECK, and self-FK match exactly. The one non-substantive divergence — ORM declares a *unique index*, migration declares a *unique constraint plus a plain index* — enforces identical uniqueness semantics and is byte-for-byte the same pattern as the already-certified `c021_offering_definition`. Recorded as Observation O-1.
- **Portability:** `func.substr(account_reference, 9)` — a fixed, compile-time-known offset. **No `instr()`, `strpos()`, or `position()` anywhere.** Verified by *running* the two portability guards: one compiles the query under both the PostgreSQL and SQLite dialects, asserts all three functions absent from both, and asserts the two SQL strings byte-identical; the other intercepts the **actually executed** statement via a `before_cursor_execute` listener. Reading the source comment alone was not treated as evidence.
- **Not executed against a live PostgreSQL server** — none is reachable in this environment. This is the same disposition recorded for every prior `AuthService` Work Package; verification was by direct read, ORM-versus-migration comparison, `alembic heads`/`branches`/`history`, and dual-dialect compilation.

---

## 8. Security

### 8.1 `require_platform_admin` unmodified

`git diff -- dependencies.py` (executed) → **empty**. The dependency is byte-for-byte the certified one: `dependencies.py:46–55`, raising 403 when `claims.get("role_code") != PLATFORM_ADMIN_ROLE_CODE`.

### 8.2 Router uses it; no weaker or alternate path exists

`routers/commercial_account.py:57` — `claims: Annotated[dict, Depends(require_platform_admin)]` on the single route. The router does **not** use `require_matching_tenant_or_platform_admin` or any bespoke check. `CommercialAccountService` is reachable **only** through `get_commercial_account_service`, which is itself reachable only through that one gated route. Empirically confirmed by this reviewer: six distinct non-`PLATFORM_ADMIN` role claims — including the lowercase variant `platform_admin` and the near-miss `PLATFORM_ADMINX` — **all returned 403**.

### 8.3 Tenant-middleware exemption is exact-prefix-scoped

The single added line is `or path == "/commercial-accounts" or path.startswith("/commercial-accounts/")`. It matches the exact path and its subtree only; it does **not** match `/commercial-accounts-anything` or any unrelated path, and it widens nothing else. The surrounding diff adds only a rationale comment block citing `ROD-C022` D2.

### 8.4 No cross-tenant leakage surface exists at all

There is **no** `organization_id` and **no** column whose name contains `tenant` — in the migration DDL *or* in the ORM metadata (both independently confirmed, the former by live `inspect()` introspection at runtime, the latter by metadata inspection). `CLAUDE.md §21.4`'s Mandatory Tenant-Isolation Test Checklist is therefore **structurally not applicable**, exactly as `ROD-C022` D2 / `TDS §11` / Charter §12 determine; the substitute assurance those documents require (non-admin denied; admin succeeds; automated dual-mechanism no-`organization_id` assertion) is present and was executed. There is no organization boundary to breach, so §21.4(a)/(b)/(c) have no object. Additionally, this reviewer probed injection of `organization_id` and `tenant_id` into the request body — both silently ignored, and neither reaches persistence (Observation O-2 notes the deliberate `ignore` policy this relies on, which `TDS §16` mandates).

---

## 9. API

- **Request validation:** `EstablishCommercialAccountRequest` declares exactly one field, `account_name: str`, `min_length=1`, `max_length=255`, plus a `field_validator` rejecting whitespace-only strings. Confirmed in the live OpenAPI schema (one property, one required entry).
- **Response contract:** `CommercialAccountResponse` (`from_attributes=True`) exposes `id`, `account_reference`, `account_name`, `status`, `parent_account_id`, `created_at`, `updated_at`. `created_by_actor_id` is correctly **excluded**. Live response keys observed: exactly those seven.
- **Declared responses:** 201, 400, 401, 403, 409, 422 — confirmed in the live OpenAPI document.
- **Duplicate / conflict handling (read directly, service L95–127):** a bounded `for … else` over `_REFERENCE_ALLOCATION_MAX_RETRIES = 5`; each iteration allocates a fresh reference, creates, and flushes; an `IntegrityError` triggers `session.rollback()` and a retry; exhaustion emits a `DENIED` audit record and raises a clean `409` chained from the last error. The logic is correct as written. **It is structurally present but not empirically tested** — the `except` block carries `# pragma: no cover - race backstop` and no test seeds a colliding `account_reference`. Recorded as `G1-L-01`.
- **Route registration:** `main.py:112` includes the router once, at prefix `/commercial-accounts`, tag `Customer & Account Management`. `grep -n "commercial_account" main.py` returns exactly two lines (the import extension and that one `include_router`) — **no double-registration**. OpenAPI enumeration across all 103 application paths confirms a single commercial-account path with a single method.

---

## 10. Test results — what this reviewer personally ran

### 10.1 Targeted suite — executed by this reviewer

```
py -3 -m pytest tests/test_commercial_account.py -v
=> 21 passed, 3 warnings in 8.94s
```

All 21 tests passed. All 21 names match `IMP-REPORT-WP-21 §5.7`'s list exactly. **No test file was modified; nothing was skipped or xfailed.**

**Per-test quality judgement (does each test actually exercise the claim its name makes?):**

- *Genuine, stronger than its name.* `test_account_reference_is_monotonic_and_unique` asserts full **contiguity** (`suffixes == list(range(suffixes[0], suffixes[0]+5))`), not merely uniqueness or sortedness — it genuinely exercises the `MAX+1` allocator.
- *Genuine, and specifically checked by this reviewer because a source comment would not have sufficed.* The two portability tests verify the property empirically — one by dual-dialect compilation with byte-equality assertion, one by intercepting the **actually executed** SQL.
- *Genuine.* The two absence-of-endpoint tests probe five transition shapes and two read/list shapes against the **running application**, requiring 404/405 — absence is proved behaviourally, not by reading the router.
- *Genuine.* The schema-absence tests use two independent mechanisms (live DB introspection *and* ORM metadata), satisfying `TDS §11`'s substitute-assurance clause (c) as written.
- *Genuine.* `test_establish_emits_success_audit` spies the real `record_audit` and asserts action, actor, status, and a regex-conformant reference — not merely that something was logged.
- *Weaker than its name.* `test_establish_happy_path_persists_active` and `test_end_to_end_establish_probe` read back through the **same** session the request used; `conftest.py`'s `client` fixture overrides `get_session` with a generator that never commits, whereas production `get_session` (`models/database.py:64–78`) does commit. They observe post-`flush`, in-transaction state. Recorded as `G1-L-02`.
- *Gap.* No test exercises the `IntegrityError` retry path or the 409 exhaustion path; no test negatively exercises the `status` CHECK constraint (unreachable via the API, since no field accepts a status). Recorded as `G1-L-01`.

### 10.2 Full regression — executed by this reviewer

This reviewer **did not** rely on the prior 950/950 result, and did not adopt attempt #1's disposition of deferring it. The full suite was re-run from scratch:

```
py -3 -m pytest tests/ -q
=> 950 passed, 71 warnings in 344.82s (0:05:44)
```

**950 passed, 0 failed, 71 warnings** — an exact match to `IMP-REPORT-WP-21 §5.7`'s claimed figures on both counts. The warnings are the pre-existing, unrelated Starlette `HTTP_422_UNPROCESSABLE_ENTITY` rename deprecations (spot-checked in the output across `routers/membership.py`, `routers/person.py`, `tests/test_membership_service.py`). No test file was modified; nothing was skipped or xfailed.

For completeness, the independent staleness check was also performed and agrees: no `AuthService` source or test file has an mtime later than `2026-09-15 17:46:34`; `conftest.py` (`2026-07-16`) and `dependencies.py` (`2026-08-29`) are untouched. The prior result would have been valid — but this reviewer re-ran it regardless rather than certify on inherited evidence.

### 10.3 Purpose-built runtime probe — written from scratch by this reviewer

Not adapted from the existing suite. Executed against the real application via `TestClient` on a fresh in-memory database:

| Probe | What it tests that the existing suite does not | Result |
|---|---|---|
| **P1** — pre-seed `ACCOUNT-000042`, then establish | The allocator's behaviour on a **non-empty, non-zero base**. Every existing test starts from an empty table, so the `substr`/`cast`/`MAX` path has never been exercised against a real prior maximum | ✅ `201 ACCOUNT-000043` — resumes correctly from the seeded maximum |
| **P2** — establish again | Contiguity continues from a seeded base | ✅ `201 ACCOUNT-000044` |
| **P3** — six role variants (`ORG_ADMIN`, `TENANT_ADMIN`, `MEMBER`, `PLATFORM_ADMINX`, `platform_admin`, `''`) | Whether any near-miss or case-variant role bypasses the gate. The existing suite tests two variants | ✅ **all six → 403**; no bypass |
| **P4** — body carrying `organization_id`, `tenant_id`, `classification`, `created_by_actor_id` | Whether a tenant-scoping or classification field can be injected through the ignore-policy | ✅ `201`, all injected fields ignored; response keys exactly the seven contracted ones; no `classification`, no `organization_id` |
| **P5** — read back all rows | Persisted state | ✅ 4 rows, all `status='active'`, all `parent_account_id=NULL` |

The live audit record emitted during P4 was observed directly and carries `"action": "ESTABLISH_COMMERCIAL_ACCOUNT"`, `"status": "SUCCESS"`, `"tenant_id": "PLATFORM"`, and a `PREFIX-NNNNNN`-conformant `account_reference` — confirming both the audit contract and the platform-global posture at runtime.

---

## 11. Governance

### 11.1 CBOR — `CAC-000001`

`CBOR-INDEX.md:40` carries `| CAC-000001 | Commercial Account | C-022 (Customer & Account Management) | ADR-040 | IRA-C022 §11 |`. Verified:
- **Correctly mapped** — object name, owning capability, registering ADR, and eligibility basis all correct.
- **Registering ADR resolves to a real file** — `architecture/07-Decisions/ADR-040_…md` exists (11,246 bytes), **Status: Accepted**, assigns `CAC-000001`, and explicitly states it performs **no** BAR registration.
- **Eligibility basis resolves** — `IRA-C022 §11` (line 140) does contain the `CMD-001 §26.3a` three-step eligibility analysis, so the citation is accurate.
- `ADR-039` remains **PROPOSED — REGISTRATION PREPARATION ONLY**, unaltered, as the historical preparation record. Correct: `ADR-040` is the execution record.
- No second Business Object Identifier was assigned and the index was not re-amended by the implementation pass.

### 11.2 `WPR-001` WP-21 row — present, **but still stale**

A WP-21 row exists at `WPR-001:74`. Its **current exact text** (read this pass, not assumed) still states:

> *"**IMPLEMENTATION AUTHORIZED (RO, 2026-09-15) — IMPLEMENTATION NOT YET STARTED.** No schema, migration, model, repository, service, router, frontend, or test exists."*

and its Gate column still states:

> *"**No Gate dispatched.** No implementation exists; `CLAUDE.md §19.7b`'s five-gate closure sequence has not begun."*

`WPR-001:76` similarly states *"Implementation itself has **not** begun — no schema, migration, code, or test exists."* **All of these are now false** — the implementation exists, Gate 1 has been dispatched twice, and this is the second Gate 1 record. `G1-L-04` has therefore **not** been corrected and is carried forward, extended (§12).

### 11.3 Charter §25a scope versus what the code does; §21 backend-only

- Charter §25a authorizes exactly: the single `POST /commercial-accounts` establish endpoint (§10), §8's schema **including the explicit absence of `classification`**, §7's `PREFIX-NNNNNN` reference, §13's declared-but-unexercised hierarchy column, and §14's `active`-only status write — *"No field, endpoint, or business rule beyond §1–§20 is authorized."* **The delivered code implements exactly that set and nothing beyond it** (§4, §5). Every §20 exclusion is preserved.
- Charter §21 (`CLAUDE.md §20.3` backend-only, binding) is **HONORED** — zero files under `source/frontend/src` reference C-022 in any form. `CLAUDE.md §20.7`'s Enterprise Experience completion-gate extension correctly does not apply, per §20.3's own charter-exception clause.

### 11.4 `CERT-WP-21` intact

`architecture/06-Reviews/CERT-WP-21_Establish_Commercial_Account.md` — present, 39,526 bytes, mtime `2026-09-15 21:35:16`, **unmodified**. It was read by this reviewer as historical evidence and as a source of leads, and **was not touched, edited, overwritten, or superseded**. It remains the authoritative record of the first Gate 1 attempt.

### 11.5 Other governance artifacts confirmed

`ROD-C022` D1–D6 (D2 platform-global, D3 `AuthService`, §H boundary), `ROD-C022-A` D7/D8 (both Option A), `ROD-C022-B` D9/D10 (both Option A), `ADR-038` (Accepted — Option A), `IRA-TDS-C022_Independent_Review.md` (PASS WITH CONDITIONS, all seven conditions resolved or deferred by recorded decision), `CAP-001:76` (C-022 Active, owning spec `COM-001`), and the `COM-001` clauses `-001`/`-002`/`-003`/`-033`/`-036`/`-060`/`-061` — **all read directly from source and all consistent with the delivered implementation.** No canonical conflict requiring `CLAUDE.md §16`'s STOP-and-report procedure was found.

---

## 12. Findings

### Critical — none
### High — none
### Medium — none

**`G1-M-01` (the sole blocking finding of Gate 1 attempt #1) is RESOLVED** — see §3.4.

### Low — non-blocking (all four carried forward from `CERT-WP-21`, each independently re-confirmed still accurate)

**`G1-L-01` — Allocate-and-retry concurrency backstop and 409 exhaustion path are untested.**
*File / location:* `Backend/Services/AuthService/services/commercial_account_service.py:112` (`except IntegrityError as exc:  # pragma: no cover - race backstop`) and L116–127 (the `for … else` 409 path); `Backend/Services/AuthService/tests/test_commercial_account.py` (whole file).
*Evidence (re-verified this pass):* this reviewer read the full test file — no test pre-seeds a colliding `account_reference`, so neither the retry branch nor the exhaustion branch is ever entered. The `status` CHECK constraint is likewise never negatively exercised (unreachable via the API, since no request field accepts a status).
*Impact:* Low. The concurrency property `TDS §7`/`§18` require is asserted **structurally** — the UNIQUE constraint and retry loop were read and confirmed correct by this reviewer, and the allocator was independently probed against a non-empty table (§10.3, P1/P2) — but the collision path itself is not demonstrated empirically. The design is sanctioned by `TDS §18` and mirrors the certified `OfferingDefinitionService.establish` pattern, whose identical `# pragma: no cover` gap was carried through all five WP-20 gates.
*Required remediation:* add a collision regression test at Gate 2 — pre-seed the reference the allocator is about to claim, then establish and assert recovery. Candidate `CLAUDE.md §19.8` Technical Debt entry; **Medium severity** per the `§19.8.7` rubric (internal robustness/completeness; no Business Intent and no security or tenant-isolation boundary at stake). Not a `§19.8.5`-class defect.

**`G1-L-02` — "Persists" tests verify through the request's own uncommitted session.**
*File / location:* `Backend/Services/AuthService/tests/conftest.py` (the `client` fixture, `override_get_session`) versus `Backend/Services/AuthService/models/database.py:64–78` (production `get_session`).
*Evidence (re-verified this pass):* this reviewer read `conftest.py` in full — `override_get_session` yields the same `db_session` the assertions later query and **never commits**; production `get_session` commits on successful exit. `test_establish_happy_path_persists_active` and `test_end_to_end_establish_probe` therefore observe post-`flush`, in-transaction state, not a committed round-trip on a separate connection.
*Impact:* Low. The production commit path is correct and unmodified. The tests' assurance is narrower than the word "persists" implies. This is a **pre-existing, repository-wide shared-harness property** — `conftest.py` is unmodified by this Work Package (mtime `2026-07-16`) and identical for every previously certified Work Package.
*Required remediation:* harness-parity item for Gate 2's `§19.7b` production-parity checklist. **No WP-21 implementation change.**

**`G1-L-03` — Test harness does not enable `PRAGMA foreign_keys=ON`.**
*File / location:* `Backend/Services/AuthService/tests/conftest.py` — no pragma and no `connect` event listener anywhere in the file.
*Evidence (re-verified this pass):* read in full; confirmed absent. SQLite disables FK enforcement by default, so `fk_c022_commercial_account_parent_account_id` is unenforced in tests.
*Impact:* **None functionally for BA-01** — `parent_account_id` is hard-coded `None` at the single write site and no route ever sets it (independently confirmed at runtime: all probe rows `NULL`). Low, and identical to `CERT-WP-20 §4` observation 5.
*Required remediation:* repository-wide harness-parity item for Gate 2's production-parity checklist, which `§19.7b` names explicitly as a root-cause class. **No WP-21 change.**

**`G1-L-04` — Governance documents describing WP-21 are factually stale. (EXTENDED by this reviewer.)**
*File / location — the two `CERT-WP-21` already named, re-confirmed still uncorrected:*
1. `architecture/00-Governance/WPR-001_Work_Package_Roadmap.md:74` — still reads *"IMPLEMENTATION NOT YET STARTED. No schema, migration, model, repository, service, router, frontend, or test exists"*, and its Gate column still reads *"**No Gate dispatched.** … the five-gate closure sequence has not begun."* Both false.
2. `architecture/00-Governance/CBOR-INDEX.md:23` — *"no `c022_commercial_account` table, model, migration, or API exists as of this entry."* Now false, though that line is explicitly time-scoped and already self-discloses that a follow-up correction will be required.
*Two additional locations this reviewer found that attempt #1 did not name:*
3. `architecture/00-Governance/WPR-001_Work_Package_Roadmap.md:76` — *"Implementation itself has **not** begun — no schema, migration, code, or test exists."* False.
4. `architecture/06-Reviews/MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md:40` **and** `:183` — both still read *"IMPLEMENTATION AUTHORIZED (RO, 2026-09-15) — IMPLEMENTATION NOT YET STARTED. No schema, migration, code, or test exists."* Both false.
*Impact:* Low, and **not independently blocking.** `CLAUDE.md §19.7b` assigns exactly this class of governance-documentation staleness to **Gate 5 (Release Readiness Audit)**, which *"exists specifically to catch governance-documentation staleness (e.g., a status field still describing a superseded or already-completed state)."* It is recorded here, extended, so the full set is visible entering Gate 2 rather than rediscovered piecemeal at Gate 5.
*Required remediation:* synchronize all four locations (plus `ADR-040`'s own Physical Implementation Mapping row, which `ADR-040:38` already anticipates requiring correction once implementation exists), strikethrough-preserved per repository convention, at the Gate 1 recording pass or **at the latest before Gate 5**. **No implementation change.**

### Observations (non-findings)

**O-1.** `IMP-REPORT-WP-21 §5.3` describes `ix_c022_commercial_account_account_reference` as *"(unique)"*. True of the ORM shape (runtime-confirmed `unique=True`); not true of the migration, where the index is plain and uniqueness is carried by `uq_c022_commercial_account_account_reference`. The report's own §3 describes the migration correctly. Uniqueness is enforced in both shapes, and the same divergence exists in the already-certified C-021 precedent. Cosmetic wording only; no correctness impact, and no implementation change warranted.

**O-2.** `EstablishCommercialAccountRequest` does not set `extra="forbid"`, so Pydantic's default `ignore` applies and unknown body fields are silently dropped. This is **exactly** what `TDS §16` specifies (*"ignored (not present in the schema at all) — mirrors `c021_offering_definition`'s own 'not in the schema' enforcement rather than a runtime override-and-reject check"*), and this reviewer confirmed it empirically (§10.3, P4). Conformant, not a finding.

**O-3.** `CommercialAccountResponse` includes `updated_at`, which `TDS §15` / Charter §10 do not enumerate in their response list. It is part of the persisted row per `TDS §6.1` / Charter §8, is always `null` at establish, and `created_by_actor_id` is correctly excluded. Non-material.

**O-4.** The runtime prefix `ACCOUNT-` is not lexically aligned with the CBOR identifier `CAC-000001`. Permitted by `TDS §7` (the prefix token is `[IMPLEMENTATION-TIME]`), explicitly disclosed at `models/c022_commercial_account.py:26–33`, and consistent with the certified `OFFERING-` / `OFR-000001` precedent. Cosmetic.

**O-5.** `COM-001-060`'s own trigger wording is *"once implemented."* Implementation now exists, so that clause's condition has, in fact, fired for BA-01. The obligation remains explicitly and correctly **deferred** by `ROD-C022-B` D10 (Option A) — an explicit Repository Owner decision — and is described as deferred, never as satisfied, in every governance location this reviewer checked. No BAR artifact exists anywhere in the repository. Recorded so the obligation stays visible into Gates 2 and 5; **not** a finding, since a recorded Repository Owner deferral is exactly the disposition `CLAUDE.md §19.8.6` contemplates.

**O-6.** `CommercialAccountService._coerce_actor_id` (service L160–179) returns **400** for an authenticated `PLATFORM_ADMIN` whose token lacks a `person_id` claim or whose claim is not a valid UUID. The behaviour is correct and fail-closed — it prevents writing a NULL or invalid `created_by_actor_id` — but the router's OpenAPI description for 400 reads *"Missing or malformed Authorization header"*, which does not describe this second 400 case. Documentation nuance only.

**O-7.** No C-022 / WP-21 entry exists in `architecture/06-Reviews/TECH-DEBT.md`. Consistent with Gate 1 not having previously concluded; `G1-L-01` is the candidate entry, to be created as part of the post-Gate-1 Technical Debt recording per `CLAUDE.md §19.8.2`.

---

## 13. Change-boundary confirmation (verified by this reviewer)

- `git rev-parse HEAD` → **`8323bf3976818ff463cf67e891bd2a0a953777fd`** — **matches the expected hash exactly.**
- `git diff --cached --name-only` → **empty.** Nothing is staged.
- **Nothing was committed or pushed by this review.**
- **C-022 implementation files (all untracked, all new):** `models/c022_commercial_account.py`, `repositories/c022_commercial_account_repository.py`, `services/commercial_account_service.py`, `schemas/commercial_account.py`, `routers/commercial_account.py`, `alembic/versions/2026_09_15_0900-f6a7b8c9d0e1_c022_commercial_account.py`, `tests/test_commercial_account.py`.
- **Additive edits to three tracked files, diffed line by line:** `main.py` (one import extension + one `include_router`), `middleware/tenant.py` (one rationale comment block + one exemption line pair), `models/__init__.py` (one import + one `__all__` entry). Each of these three also carries pre-existing, unrelated WP-20 / C-021 content in the same diff; that content was inspected only far enough to confirm it is not C-022's, and is not commented on here.
- **Governance files reflecting WP-21 content:** `architecture/05-Implementation/IMP-REPORT-WP-21_Establish_Commercial_Account.md` (the certification input for this review) and `architecture/06-Reviews/CERT-WP-21_Establish_Commercial_Account.md` (attempt #1's record, untouched), plus this document.
- **Every other modified or untracked path in the working tree was confirmed to carry no C-022 / commercial-account content** and was left exactly as found — the 13 pre-existing modified tracked files (`CLAUDE.md`, `CAP-001`, `SER-001`, `TECH-DEBT.md`, `ADR-002`, `admin-navigation.ts`, `WPR-001`, `CBOR-INDEX.md`, the delivery map, and others) and the large pre-existing untracked set (the C-021 / WP-20 implementation and frontend, the `ROD-C040-*` / `ROD-Meta-Governance-*` set, `ADR-027`…`ADR-035`, and others).
- **Files created by this review:** exactly one — this document, `architecture/06-Reviews/CERT-WP-21A_Establish_Commercial_Account_Second_Gate_1_Attempt.md`.
- **Files modified by this review: none.** No implementation file, no test file, no Charter, no TDS, no ROD, no ADR, no register, and — explicitly — **not `CERT-WP-21` and not `IMP-REPORT-WP-21`**. The implementation that was reviewed is byte-untouched.

---

## 14. Gate 1 decision

> ### ✅ **GATE 1 — INDEPENDENT CERTIFICATION (SECOND ATTEMPT): PASS WITH OBSERVATIONS**

**Basis.** Zero Critical, zero High, zero Medium findings. The single blocking finding of the first attempt, `G1-M-01`, is independently found **RESOLVED**: `IMP-REPORT-WP-21` exists, satisfies every `CLAUDE.md §19.7` Implementation Report requirement, carries an explicit Implementation Status of "IMPLEMENTATION COMPLETE", and every factual claim sampled from it was independently confirmed against actual repository state — including the two claims this review was specifically directed not to take at face value, **21/21** and **950/950**, both of which this reviewer reproduced exactly (`21 passed in 8.94s`; `950 passed, 71 warnings in 344.82s`).

On every technical dimension independently re-derived — requirement traceability against `ROD-C022 §H` / D1–D10 / `ADR-038` / `ADR-040` / Charter §25a; functional correctness of establish, the `PREFIX-NNNNNN` allocator, persistence, validation, and the 403/400/422/409 paths; scope control (classification, Customer, Relationship, Organization equivalence, Identity/Person wiring, read/list/update/delete, lifecycle transitions, merge/split/transfer, Subscription/Billing/Contract/Entitlement, CRM, frontend, BAR, Business Activity Identifier — **all confirmed absent by direct inspection, import-set analysis, and runtime probing, not by trusting docstrings**); D9's collapsed single-call realization and the absence of any unauthorized lifecycle policy; D10's BAR deferral and the accurate, non-satisfied description of `COM-001-060`; the data model, constraints, indexes, and the single non-branching Alembic head; the PostgreSQL-portable allocator, verified by execution rather than by comment; the unmodified `require_platform_admin` gate, the exact-prefix-scoped middleware exemption, and the structural absence of any tenant column and therefore of any cross-tenant leakage surface; the API contract, validation, and single-route registration confirmed against the live 103-path OpenAPI surface — **the implementation is conformant, in scope, and correct.**

`CLAUDE.md §19.8.5` is **not** engaged: no architectural, security, data-integrity, or tenant-isolation defect; no failing test; no build failure.

**Why "WITH OBSERVATIONS" and not a clean PASS.** Four Low findings remain open. Each was independently re-verified as still factually accurate rather than carried forward on trust; one (`G1-L-04`) is extended with two further stale governance locations this reviewer found. None is blocking: `G1-L-02` and `G1-L-03` are pre-existing repository-wide shared-harness properties unmodified by this Work Package and explicitly assigned by `§19.7b` to Gate 2's production-parity checklist; `G1-L-04` is governance-documentation staleness explicitly assigned by `§19.7b` to Gate 5; `G1-L-01` is a test-coverage gap on a structurally correct, `TDS §18`-sanctioned path that mirrors a certified precedent, and is the candidate `§19.8` Technical Debt entry (Medium severity per the `§19.8.7` rubric).

**Relationship to `CERT-WP-21`.** This record does not replace, edit, supersede, or invalidate `CERT-WP-21`. That document remains intact and authoritative as the record of the first Gate 1 attempt and its FAIL. This record is the second, separate attempt, and it is this record that satisfies `CLAUDE.md §19.7`'s Independent Review block for WP-21 / C-022 BA-01.

**`CLAUDE.md §19.7` Business Activity Completion Gate — status after this review:**

| §19.7 condition | Status |
|---|---|
| Production-quality implementation complete | ✅ |
| All required unit, integration and API tests pass | ✅ 21/21 targeted; 950/950 full regression (both executed by this reviewer) |
| Implementation Report (`IMP-REPORT-WP-XX`) updated | ✅ `IMP-REPORT-WP-21` exists and conforms |
| Implementation Status marked "IMPLEMENTATION COMPLETE" | ✅ |
| Submitted for independent review | ✅ twice |
| Review observations addressed | ✅ `G1-M-01` remediated; four Low findings are non-blocking Gate 2 / Gate 5 carry-forwards |
| Accepted through independent review | ✅ **by this record** |
| Committed to the repository | ⬜ **not yet** — commit remains a separate, later act, authorized only after the remaining `§19.7b` gates |

**Gates 2–5 have not been run.** This record does not advance, prejudge, or substitute for any of them.

## 15. Gate 2 eligibility

**Gate 2 (Verification & Validation Audit) is now ELIGIBLE to be dispatched**, per `CLAUDE.md §19.7b`'s sequence, to a **further fresh-context reviewer uninvolved in the implementation, in `CERT-WP-21`, in the authoring of `IMP-REPORT-WP-21`, and in this review**.

Carry-forward inputs for Gate 2: `G1-L-01` (collision-path coverage — and the `§19.7b` harness/fixture production-parity checklist it feeds), `G1-L-02` and `G1-L-03` (shared-harness production parity — both are named root-cause classes in `§19.7b`'s own checklist), `G1-L-04` (governance staleness across four locations, due at the latest before Gate 5), and Observations O-1 through O-7. Note for Gate 2's own method requirement: `§21.4`'s Mandatory Tenant-Isolation Test Checklist is structurally inapplicable here, since the data model carries no organization boundary at all (§8.4) — this should be re-derived independently by that reviewer rather than adopted from this record.

---

*End of CERT-WP-21A. Gate 1 — Independent Certification, second (fresh) attempt: **PASS WITH OBSERVATIONS** (zero Critical, zero High, zero Medium; four Low, seven Observations). `G1-M-01` — the sole blocking finding of the first attempt — independently found **RESOLVED**. Independently performed 2026-09-15 by a fresh-context reviewer with no involvement in the WP-21 / C-022 implementation, in any C-022 governance artifact, in the authoring of `IMP-REPORT-WP-21`, or in `CERT-WP-21`. `CERT-WP-21` was read as historical evidence and was **not** modified. No implementation file, test file, governance document, or register was modified. Nothing was staged, committed, or pushed. WP-21 / C-022 BA-01 is certified at Gate 1 only — it is **NOT** closed and **NOT** release-ready; Gates 2 and 5 (and Gates 3–4 if triggered) remain outstanding.*
