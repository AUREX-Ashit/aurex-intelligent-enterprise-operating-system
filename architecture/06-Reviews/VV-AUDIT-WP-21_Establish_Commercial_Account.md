# VV-AUDIT-WP-21 — Gate 2 Verification & Validation Audit — Establish Commercial Account (C-022, WP-21 BA-01)

**Gate:** `CLAUDE.md §19.7b` Gate 2 — Verification & Validation Audit.
**Work Package / BA:** WP-21 — C-022 Customer & Account Management, BA-01 "Establish Commercial Account".
**Predecessor gates:** Gate 1 Independent Certification, attempt #1 — ❌ FAIL on one Medium (`G1-M-01`, `CERT-WP-21`); attempt #2 — ✅ PASS WITH OBSERVATIONS (`CERT-WP-21A`; 0 Critical/High/Medium, 4 Low, 7 Observations).
**Date:** 2026-09-16.
**Repository HEAD at audit:** `8323bf3976818ff463cf67e891bd2a0a953777fd` (verified by this reviewer via `git rev-parse HEAD`). Nothing staged (`git diff --cached --name-only` empty).

---

## VERDICT: ✅ PASS WITH NON-MATERIAL OBSERVATIONS

**Zero Critical. Zero High. Zero Medium.** No `CLAUDE.md §19.8.5`-class defect — no architectural, security, data-integrity, tenant-isolation, failing-test, build-failure, or broken-functionality issue. **All 34 rows of this reviewer's independently-derived Requirements Traceability Matrix verified PASS.** Four Low / non-material findings (`V2-L-01`…`V2-L-04`), each a reassessment of a Gate 1 carry-forward, and eight Observations. **Gate 3 and Gate 4 NOT TRIGGERED** — no defect requiring remediation was found.

**Two of the four Gate 1 Low findings are materially advanced by this audit.** `G1-L-01` (collision-retry path never demonstrated) and `G1-L-02` (persistence never verified across a commit boundary) were both *verification* gaps, not defect claims. This audit closed both empirically with purpose-built, from-scratch probes carrying working negative controls — the underlying behaviour is now **proven correct**, and only the absence of *permanent regression coverage* remains (a Technical Debt candidate, not a defect).

**Tests executed personally by this reviewer:** targeted `21/21`; full `AuthService` regression `950 passed, 0 failed, 71 warnings in 236.98s`. Both figures independently reproduced, not inherited.

---

## 1. Reviewer independence (`CLAUDE.md §19.7b` fresh-context requirement)

This reviewer had **no** involvement in, and no conversational memory of: the WP-21 / C-022 implementation; the authoring of `IMP-REPORT-WP-21`; Gate 1 attempt #1 (`CERT-WP-21`); Gate 1 attempt #2 (`CERT-WP-21A`); or any C-022 governance artifact (`ROD-C022`, `ROD-C022-A`, `ROD-C022-B`, `IRA-C022`, `TDS-C022`, `IRA-TDS-C022_Independent_Review.md`, the Charter, `ADR-038`, `ADR-039`, `ADR-040`).

All three predecessor artifacts were read **as evidence and as leads on where to look, never as authority.** Gate 2 was deliberately **not** a re-run of Gate 1's method. This audit built its own Requirements Traceability Matrix from the governing texts, performed exhaustive specification-conformance checking, and — per `§19.7b`'s explicit method requirement — authored and executed **four purpose-built runtime probe programs from scratch**, none adapted from `tests/test_commercial_account.py`, each targeting a defect class the existing suite was never designed to catch:

| Probe | Defect class targeted | Why the existing suite cannot catch it |
|---|---|---|
| **A** — migration DDL execution + constraint enforcement | Schema drift between the ORM and the *actually shipped* migration; unenforced constraints | The suite builds its schema from `Base.metadata.create_all` (ORM), so it **never executes the Alembic migration DDL at all**; and it runs SQLite with FKs off |
| **B** — committed round-trip via the real, unoverridden `get_session` | Persistence that exists only inside an uncommitted transaction | `conftest.py` overrides `get_session` with a generator that never commits, and the "persists" assertions read back through that same session (`G1-L-02`) |
| **C** — genuine `account_reference` UNIQUE collision + negative control | The `# pragma: no cover` allocate-and-retry backstop and the 409 exhaustion branch | No test seeds a colliding reference; both branches are unreachable from the suite (`G1-L-01`) |
| **D** — ORM-vs-migration parity under the production dialect; event emission | Silent divergence that only manifests on PostgreSQL; unverified `publish_event` contract | The suite never compares the two schema shapes and never asserts the event payload |

Probes were authored and executed **outside the repository**, under the scratchpad directory. No repository file was created, modified, staged, committed, or pushed by this audit other than this document.

---

## 2. Scope of this audit

WP-21 / C-022 BA-01 only: establish exactly one standalone Authoritative Commercial Account via `POST /commercial-accounts` — platform-global, `require_platform_admin`-gated, `AuthService`-hosted — per `ROD-C022 §H`/D1–D6 as constrained by `ROD-C022-A` D7/D8, `ROD-C022-B` D9/D10, `ADR-038` Option A, `ADR-040` (`CAC-000001`), `TDS-C022 §6`–`§21`, and Charter §25a.

This record does not close C-022 as a capability, and does not advance, prejudge, or substitute for Gate 5 (Release Readiness Audit). Gates 3–4 are not triggered.

**Governing documents read directly from disk by this reviewer:** the WP-21 Charter (§1–§26a); `TDS-C022` (§1–§25); `ROD-C022` §H/D1–D6; `ROD-C022-A` D7/D8; `ROD-C022-B` D9/D10; `ADR-038`, `ADR-039`, `ADR-040`; `CBOR-INDEX.md` §3; `WPR-001` (WP-21 rows 74/76); `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md` (lines 40/183); `COM-001` (Section 4 preamble line 44, `COM-001-001`, `-002`, `-003`, `-032`, `-033`, `-034`, `-035`, `-036`, `-060`, `-061`, all quoted verbatim below where relied upon); `CLAUDE.md §19.7`/`§19.7b`/`§19.8`/`§20`/`§21.4`; `IMP-REPORT-WP-21`; `CERT-WP-21`; `CERT-WP-21A`; `TECH-DEBT.md`.

---

## 3. `CLAUDE.md §19.7b` harness / fixture production-parity checklist

`§19.7b` assigns this checklist specifically to the Gate 2 audit. Both questions are answered explicitly, as required.

### Q1 — Does the test harness enforce every constraint the declared production database enforces unconditionally (foreign keys, check constraints, uniqueness)?

> ### ❌ **NO — and this is a harness limitation, not a product defect.** The distinction is proven, not asserted.

`tests/conftest.py` (mtime `2026-07-16`, **unmodified by this Work Package**) creates its schema with `Base.metadata.create_all` against `sqlite+aiosqlite:///:memory:` and sets **no** `PRAGMA foreign_keys=ON` and no `connect` event listener. SQLite therefore leaves foreign keys unenforced for the entire suite. This is `G1-L-03`, independently re-confirmed by reading the file in full.

**Probe A establishes that the product schema itself is fully correct.** The probe executed the *actual* migration `f6a7b8c9d0e1`'s `upgrade()` against a real connection with `PRAGMA foreign_keys=ON` — i.e. at production parity, since PostgreSQL enforces all three constraint classes unconditionally — and then empirically attacked every declared constraint:

| Constraint attacked | Result under production parity |
|---|---|
| `CHECK` — `status='bogus'` | **REJECTED** (`IntegrityError`) |
| `CHECK` — `status='ACTIVE'` (case variant) | **REJECTED** (`IntegrityError`) |
| `CHECK` — `status` ∈ {`suspended`,`retired`} | **ACCEPTED** (the declared closed set is exactly right) |
| `UNIQUE` — duplicate `account_reference` | **REJECTED** (`IntegrityError`) |
| `FK` — `parent_account_id` pointing at a non-existent row | **REJECTED** (`IntegrityError`) |
| `FK` — `parent_account_id` pointing at a real row | **ACCEPTED** |
| `NOT NULL` — `account_name` / `account_reference` / `created_by_actor_id` | **REJECTED** in all three cases |

**Conclusion.** Every constraint the migration declares is real and is enforced by a production-parity database. The harness's inability to enforce them is a pre-existing, repository-wide property of `conftest.py`, unrelated to and unmodified by WP-21. It is recorded as `V2-L-04`, **not** as a WP-21 defect. Additionally, for BA-01 specifically the unenforced FK has **zero** functional exposure: `parent_account_id` is hard-coded `None` at the single write site (`commercial_account_service.py:105`), and every row produced by every probe in this audit was confirmed `NULL`.

### Q2 — Does at least one test exercise more than one tenant/organization for any capability whose data model includes an organization boundary?

> ### ⬛ **STRUCTURALLY NOT APPLICABLE — independently re-derived, not adopted from `CERT-WP-21A`.**

This was verified by four independent mechanisms rather than assumed:

1. **Live introspection of the migration-created table** (Probe A): the column set is exactly `{id, account_reference, account_name, status, parent_account_id, created_by_actor_id, created_at, updated_at}`. No `organization_id`; no column whose name contains `tenant`.
2. **ORM metadata**: identical 8-column set.
3. **Runtime persistence check** (Probe B): a `PLATFORM_ADMIN` token carrying a foreign `organization_id` claim establishes successfully, and the committed row carries no organization attribute of any kind — there is nothing for the claim to bind to.
4. **Injection** (Probe B3): `organization_id` and `tenant_id` supplied in the request body are silently dropped and reach neither the ORM nor the database.

`CLAUDE.md §21.4`'s Mandatory Tenant-Isolation Test Checklist has **no object here**: (a) seeding two Organizations is impossible — no row can belong to one; (b) cross-Organization retrieval is impossible — there is no read endpoint *and* no organization attribute; (c) there is no foreign-object identifier accepted from the request at all (the contract has exactly one field, `account_name`). This is the structural expression of `ROD-C022` D2 (platform-global), matching `TDS-C022 §11` and Charter §12, and identical in kind to the certified C-021 disposition. The substitute assurance those documents require — non-admin denied, admin succeeds, dual-mechanism no-`organization_id` assertion — is present in the suite **and** was independently re-executed here.

**There is no tenant-isolation boundary in this data model to breach, and therefore no tenant-isolation defect is possible.**

---

## 4. Independent Requirements Traceability Matrix

Derived by this reviewer from `TDS-C022 §6`–`§21`, `ROD-C022 §H`/D1–D6, `ROD-C022-A` D7/D8, `ROD-C022-B` D9/D10, `ADR-038`, `ADR-040`, and Charter §1–§21/§25a — read from source, not copied from `CERT-WP-21A`'s matrix or `IMP-REPORT-WP-21 §6`.

Verification method legend: **[R]** source read · **[I]** live database introspection · **[M]** migration DDL executed · **[X]** existing test executed · **[P]** this reviewer's own from-scratch runtime probe · **[O]** live OpenAPI enumeration.

| # | Requirement (source) | Expected behaviour | Actual behaviour | Method | Result |
|---|---|---|---|---|---|
| 1 | Table `c022_commercial_account` (`TDS §6.1`, Charter §8) | Single C-022-owned table | Migration `upgrade()` executed live → exactly one table, correctly named | M, I | **PASS** |
| 2 | `id` UUID PK (`TDS §6.1`) | PK on `id`, `uuid4` default | `pk_c022_commercial_account` PRIMARY KEY (id); model `default=uuid.uuid4`; live rows carry distinct UUIDs | M, I, P | **PASS** |
| 3 | `account_reference` String(30) NOT NULL UNIQUE (`TDS §6.1`) | Unique, non-null | `VARCHAR(30) NOT NULL`; `uq_…_account_reference` UNIQUE; duplicate insert **rejected** at production parity | M, I, P | **PASS** |
| 4 | `account_name` String(255) NOT NULL, **no** uniqueness invariant (`COM-001-033` states none) | No unique constraint on the column | No UNIQUE on `account_name` anywhere in the executed DDL; two accounts with the same name both established successfully | M, I, P | **PASS** |
| 5 | `status` String(20), CHECK `{active,suspended,retired}`, NOT NULL (`TDS §6.1`) | Closed set enforced | `ck_…_status` present; `'bogus'` and `'ACTIVE'` **rejected**; `'suspended'`/`'retired'` accepted | M, I, P | **PASS** |
| 6 | BA-01 writes **only** `'active'` (`ROD-C022-A` D8, `TDS §9`, Charter §14) | Every established row `active` | Service L104 is the only `status` write, the literal `"active"`; **every** committed row across all probes is `active`, including when `status:"retired"` was injected | R, P | **PASS** |
| 7 | `parent_account_id` nullable self-FK, declared, never written non-NULL (`TDS §10`, Charter §13) | Always NULL from BA-01; FK real | `fk_…_parent_account_id` → `c022_commercial_account.id`; FK **enforced** at production parity; service L105 hard-codes `None`; every committed row NULL, including when a parent UUID was injected | M, I, R, P | **PASS** |
| 8 | `created_by_actor_id` UUID NOT NULL, **not** a FK (`TDS §6.1`) | Bare audit citation | Present, NOT NULL; the executed DDL declares exactly one FK and it is not this column | M, I | **PASS** |
| 9 | `created_at` NOT NULL / `updated_at` NULLABLE, tz-aware (`TDS §6.1`) | Correct nullability | Confirmed by live introspection; both render `TIMESTAMP WITH TIME ZONE` under the PostgreSQL dialect | M, I | **PASS** |
| 10 | **No `organization_id`, no `tenant*`** (`ROD-C022` D2, `TDS §6.1`/`§11`, Charter §12) | Structurally absent | Absent from migration DDL, ORM metadata, request contract, response contract, and every committed row | M, I, O, P | **PASS** |
| 11 | **No `classification` anywhere** (`ADR-038` Option A, `ROD-C022-A` D7, Charter §15) | Absent at every layer | Absent from migration DDL, ORM metadata, request schema, response schema; injected `classification:"STRATEGIC"` silently dropped, never persisted | M, I, O, P | **PASS** |
| 12 | `account_reference` SHALL be `PREFIX-NNNNNN` (`COM-001-001`, inherited by Section 7 per `COM-001` line 44 — re-read verbatim by this reviewer) | `^[A-Z]+-\d{6}$` | `ACCOUNT_REFERENCE_PREFIX="ACCOUNT"`; `f"{PREFIX}-{n:06d}"`; observed live `ACCOUNT-000001`…`ACCOUNT-000009` | R, P | **PASS** |
| 13 | System-assigned; caller cannot supply or override (`TDS §8`/`§16`, Charter §6) | Contract exposes one field only | Live OpenAPI: `EstablishCommercialAccountRequest` has exactly one property, `account_name`. A body carrying `id`, `account_reference`, `status`, `parent_account_id`, `created_by_actor_id`, `created_at`, `updated_at`, `classification`, `organization_id`, `tenant_id` → 201, **all ten ignored, verified against the committed database row** | O, P | **PASS** |
| 14 | Allocator acceptance properties: system-assigned, monotonic, unique, **concurrency-safe** (`TDS §7`/`§18`) | `MAX+1`; UNIQUE backstop; allocate-and-retry recovers | Monotonic and contiguous across four **separately committed** transactions (`ACCOUNT-000001`→`000004`). **A real UNIQUE collision was forced and the retry loop demonstrably recovered** — see §5 | R, P | **PASS** |
| 15 | Allocator PostgreSQL-portable — fixed-offset `substr`, never `instr()`/`strpos()`/`position()` | Identical SQL on both dialects | `_REFERENCE_SUFFIX_OFFSET = len("ACCOUNT")+2 = 9`; both portability guards executed; dual-dialect compile byte-identical | R, X | **PASS** |
| 16 | `POST /commercial-accounts` → 201, `Depends(require_platform_admin)` (`TDS §15`, Charter §10) | One gated route | Router L26–29/L57; `main.py:112` includes it once; live OpenAPI `{'/commercial-accounts': ['post']}` | R, O, P | **PASS** |
| 17 | **No other route** (`ROD-C022-A` D8, Charter §20) | Establish only | OpenAPI enumeration of all **103** application paths → exactly one commercial-account path, one method. 13 further shapes probed at runtime (GET collection, GET item, PUT, PATCH, DELETE, retire, reactivate, reclassify, transition, merge, split, transfer, search) → all 404/405. `GET` returns 405 with no listing body | O, P | **PASS** |
| 18 | Blank/missing `account_name` → 422 (`TDS §16`, Charter §7) | Reject non-substantive names | Blank, empty, missing, `null`, non-string, 256-char, and tab/newline-only → all **422**; 255-char accepted; **no invalid row persisted** in any case | P | **PASS** |
| 19 | Non-`PLATFORM_ADMIN` → 403; no-role → 403; missing/malformed `Authorization` → 400 (`TDS §19`) | Fail closed | 15 negative auth variants probed → exactly the specified codes; **and zero rows written by any rejected caller**, verified on a separate connection | P | **PASS** |
| 20 | Tenant-middleware exemption on the `/roles`/`/offerings` basis (`ROD-C022` D2, `TDS §12`, Charter §11) | Exact-prefix scope, widens nothing | One added line pair, `path == "/commercial-accounts" or path.startswith("/commercial-accounts/")`; establish succeeds with no `X-Tenant-ID`, and an explicitly-supplied `X-Tenant-ID` is ignored rather than honoured | R, P | **PASS** |
| 21 | Service host `AuthService`; no new service (`ROD-C022` D3, `TDS §5`/`§13`) | Five files at the prescribed paths | All present under `Backend/Services/AuthService/`, names matching `TDS §13` exactly | R | **PASS** |
| 22 | Repository minimum methods (`TDS §14`) | `create`/`get_by_id`/`get_by_account_reference` | `create`/`get_by_id` inherited from `BaseRepository`; `get_by_account_reference` implemented; `max_reference_sequence` added for the allocator | R | **PASS** |
| 23 | Audit on establish (`TDS §17`) | SUCCESS record, correct actor + metadata | `record_audit(action="ESTABLISH_COMMERCIAL_ACCOUNT", status=SUCCESS, …)`; observed live, actor matching the caller's `person_id` claim. **DENIED record on allocation exhaustion also observed live** (§5) | R, X, P | **PASS** |
| 24 | Event on establish (`TDS §17`) | `publish_event("COMMERCIAL_ACCOUNT_ESTABLISHED", …)` | Emitted; payload is exactly `{account_id, account_reference, account_name, status}` — no actor, tenant, organization, or classification leakage | P | **PASS** |
| 25 | Migration additive, `down_revision=e5f6a7b8c9d0`, single non-branching head (`TDS §6.1`) | Linear chain | `alembic heads` → `f6a7b8c9d0e1 (head)` (one); `alembic branches` → empty; `alembic history` → 30 linear revisions. No `ALTER`, no `CREATE SEQUENCE` | R | **PASS** |
| 26 | Migration `downgrade()` correctness | Clean reversal | `downgrade()` executed live → index and table both dropped, database returns to empty | M | **PASS** |
| 27 | ORM ↔ migration schema parity | No drift | Column names, nullability, PK, FK, CHECK, and index all identical. Under the **PostgreSQL** dialect both shapes render byte-equivalent column types (`UUID`, `TIMESTAMP WITH TIME ZONE`). Uniqueness enforced under both shapes (duplicate rejected in each) | M, I, P | **PASS** (see `Obs-1`) |
| 28 | **Committed** persistence of reference / status / parent / name / actor | Survives the commit boundary | Established through the **real, unoverridden** `get_session` (which commits) against the **migration-built** table, then read on a **brand-new engine and connection**: all seven persisted values correct; `updated_at` NULL at establish. **This closes `G1-L-02`'s verification gap empirically** | P | **PASS** |
| 29 | D7 — no classification (`ROD-C022-A` D7, `ADR-038` Option A) | Settled, absent | Row 11. `ADR-038` re-read: **Accepted — Option A selected** | R, M, I, O, P | **PASS** |
| 30 | D8 — establish-only (`ROD-C022-A` D8) | No read/list/update/delete | Row 17. `get_by_account_reference` exists as a repository method per `TDS §14` but is wired to **no** route or service method (see `Obs-4`) | R, O, P | **PASS** |
| 31 | D9 — collapsed single-call lifecycle (`ROD-C022-B` D9 Option A, Charter §16) | No separately-observable Anchor/Intent/Proposed/Assessment stage | `ROD-C022-B:19` re-read verbatim. Searched the whole C-022 module set: **no** Anchor, Intent, Proposed, or Assessment construct exists as a table, column, enum, schema, service method, or route. One endpoint, one public service method. `status` has exactly one write site and no code path branches on it — no implicit state machine was introduced | R, I, O | **PASS** |
| 32 | D10 — BAR deferred, no mechanism, no identifier (`ROD-C022-B` D10 Option A, Charter §18) | Nothing created | Repository-wide glob for `*BAR-INDEX*` / `*Business_Activity_Registry*` / `*BAR-REG*` → **no file exists**. No `business_activity_registry` / `BA-NNNNNN` construct in any `Backend/` source. Deferral described as deferred — never as satisfied — in Charter §18, `WPR-001`, `CBOR-INDEX.md:23`, `ADR-040`, and `IMP-REPORT-WP-21` | R | **PASS** |
| 33 | CBOR registered `CAC-000001` (`ADR-040`, `COM-001-061`) | Chain resolves | `CBOR-INDEX.md:40` → `\| CAC-000001 \| Commercial Account \| C-022 (Customer & Account Management) \| ADR-040 \| IRA-C022 §11 \|`. `ADR-040` exists, **Status: Accepted**, assigns `CAC-000001`. `ADR-039` remains `PROPOSED — REGISTRATION PREPARATION ONLY`, correctly unaltered as the historical record. Full chain `CAC-000001 → Commercial Account → C-022 → WP-21 → ADR-040` **resolves correctly** | R | **PASS** |
| 34 | `CLAUDE.md §20.3` backend-only honoured (Charter §21) | No frontend for this BA | Recursive case-insensitive search across `source/frontend/` for `commercial-account`, `commercial_account`, `CommercialAccount`, `c022`, `C-022` → **zero files**. `§20.7`'s Enterprise Experience completion-gate extension correctly does not apply, per `§20.3`'s own charter-exception clause | R | **PASS** |

**No row was found unsupported. No requirement in the governing set was found unimplemented, and no behaviour was found that the governing set does not authorize.**

---

## 5. Purpose-built runtime probes — `CLAUDE.md §19.7b` method requirement

### 5.1 Probe C — the collision-retry backstop, **with a working negative control**

This is the audit's most significant result. `commercial_account_service.py:112` marks the `except IntegrityError` branch `# pragma: no cover - race backstop`, and `CERT-WP-21A` recorded (`G1-L-01`) that neither the retry branch nor the 409 exhaustion branch had ever been demonstrated. **Reading the code is not evidence that it works** — that is precisely the gap `§19.7b`'s method requirement exists to close.

**Method.** A file-backed database whose table was created by the **real migration DDL**. A genuinely separate session/connection commits the row the allocator is about to claim — a real concurrent establisher. The allocator's `MAX` read is made stale for exactly one call, which is precisely what happens in production when two callers read `MAX(suffix)` before either commits. **Only the timing is simulated**: the UNIQUE constraint, the `IntegrityError`, the `session.rollback()`, the retry, and the re-allocation are all unmodified production code, reached through the real HTTP route.

| Probe | Result |
|---|---|
| **C1 — positive.** Racer commits `ACCOUNT-000001`; establish then claims the same number | ✅ **HTTP 201.** The allocator was re-entered (2 calls — the retry loop demonstrably ran). Recovered to `ACCOUNT-000002`, the next free number. Both rows committed; **no duplicate, no data loss**; the racer's row was untouched by the rollback; the recovered row is `active` |
| **C2 — NEGATIVE CONTROL.** Identical setup, retry budget reduced to 1 | ✅ **HTTP 409** — the collision is **not** survived without the retry loop. This proves the probe genuinely reproduces a collision and that recovery in C1 was the retry loop, not luck. Had C2 returned 201, C1's result would have been meaningless |
| **C2b — exhaustion behaviour** | ✅ `409 Conflict` with a clean message; a **DENIED** audit record emitted (`action="ESTABLISH_COMMERCIAL_ACCOUNT"`, `reason="account_reference allocation exhausted retries"`); **no partial or garbage row committed** |
| **C3 — recovery after exhaustion** | ✅ The next establish succeeds normally at `ACCOUNT-000004` — no poisoned session state survives the rollback |

> **Finding: the allocate-and-retry concurrency backstop and the 409 exhaustion path are CORRECT, and are now empirically demonstrated for the first time.** `G1-L-01`'s correctness risk is discharged. What remains is only the absence of a *permanent* regression test — a Technical Debt item, not a defect (`V2-L-02`).

### 5.2 Probe B — committed persistence on a genuinely separate connection

Established through the **real, unoverridden** `db_manager.get_session` (which commits, `models/database.py:73`) against the **migration-built** table, then read back on a **brand-new engine and connection opened after the request completed**. All persisted values correct (§4 row 28). The allocator was additionally shown monotonic and contiguous **across four separately committed transactions** — something the shared-session harness structurally cannot demonstrate.

> **Finding: persistence is genuinely durable across the commit boundary.** `G1-L-02`'s verification gap is closed empirically.

### 5.3 Probe B — security negative controls (15 variants, all verified non-persisting)

| Variant | Expected | Actual |
|---|---|---|
| No `Authorization` header | 400 | ✅ 400 |
| Malformed header (`NotBearer x`) | 400 | ✅ 400 |
| Empty Bearer / garbage token | 401 | ✅ 401 |
| **Token signed with a different secret** | 401 | ✅ 401 |
| **Expired `PLATFORM_ADMIN` token** | 401 | ✅ 401 |
| **`refresh`-type token** | not 201 | ✅ 401 |
| Roles `ORG_ADMIN`, `TENANT_ADMIN`, `MEMBER`, `None`, `''` | 403 | ✅ 403 each |
| Near-misses `platform_admin`, `PLATFORM_ADMINX`, `' PLATFORM_ADMIN'`, `PLATFORM-ADMIN` | 403 | ✅ 403 each — **no case-insensitive, padded, or near-miss bypass exists** |
| `PLATFORM_ADMIN` with no `person_id` claim | fail closed | ✅ 400, **no row written** |
| `PLATFORM_ADMIN` with a non-UUID `person_id` | fail closed | ✅ 400, **no row written** |

**Crucially, the committed row count was re-read on a separate connection before and after the entire negative battery and was unchanged** — no rejected caller wrote anything. `git diff -- dependencies.py` is empty: `require_platform_admin` is byte-for-byte the certified dependency; no authorization path was widened.

### 5.4 Coupling analysis — a check no docstring can defeat

The complete import set of all five C-022 modules is: `uuid`, `datetime`, `typing`, `sqlalchemy`, `pydantic`, `fastapi`, `models.database`, `models.c022_commercial_account`, `repositories.base_repository`, `repositories.c022_commercial_account_repository`, `schemas.commercial_account`, `services.commercial_account_service`, `observability`, `dependencies`.

**Zero imports** of any Customer, Organization, `organization_node`, Identity, Person, Membership, Subscription (C-020), Billing (C-024), Contract (C-025), or Entitlement (C-023) construct. In the reverse direction, the only references to C-022 modules anywhere in `Backend/` are the three wiring lines already disclosed (`main.py:11`/`:112`, `models/__init__.py:33`/`:65`) plus a comment in `middleware/tenant.py`. **There is no coupling to any other domain in either direction.** Live OpenAPI confirms no `/customers` or `/customer-account-relationships` path exists (the `400` these return is the pre-existing global `TenantMiddleware` response for any unknown non-exempt path, not evidence of a route — verified against the full 103-path enumeration).

---

## 6. Negative scope testing — `§20`/`ROD-C022 §H` exclusions

Each verified absent by code inspection **and** runtime probe, not by absence-of-route alone.

| Must be ABSENT | Verification | Result |
|---|---|---|
| Account `classification` | Absent from executed migration DDL, ORM metadata, request contract (OpenAPI: one property), response contract (7 fields); injected value dropped and never persisted | **ABSENT** |
| Customer creation | No model, table, schema, service method, or route; zero imports; `/customers` absent from the 103-path OpenAPI surface | **ABSENT** |
| Customer–Account Relationship | Same; `/customer-account-relationships` absent | **ABSENT** |
| Organization creation / linkage / equivalence | No `organization_id` column; zero imports of any C-004 construct; an `organization_id` JWT claim has nothing to bind to | **ABSENT** |
| Identity / Person linkage | Zero imports of `models.identity`, `models.person`, `models.membership`; `created_by_actor_id` carries **no** `ForeignKey` in the executed DDL | **ABSENT** |
| Account classification operation | No route, no service method, no field | **ABSENT** |
| Subscription / Billing / Contract / Entitlement | Zero imports; no field, route, or reference | **ABSENT** |
| Read / list | `GET` collection → 405 with no body; `GET` item → 404; `HEAD`/`OPTIONS` expose no account data | **ABSENT** |
| Update / delete | `PUT`/`PATCH`/`DELETE` → 404 | **ABSENT** |
| Lifecycle transitions (retire/reactivate/reclassify/transition) | All → 404; `status` has exactly one write site, the literal `"active"`; no code path branches on `status` | **ABSENT** |
| Merge / split / transfer (`ERB-C022-04`) | All → 404; no construct of any kind | **ABSENT** |
| BAR registration / mechanism / identifier | Repository-wide: no `BAR-INDEX` or equivalent file exists; no `BA-NNNNNN` identifier assigned to C-022 anywhere | **ABSENT** |
| Frontend / Enterprise Experience (`§20.3` backend-only) | Zero files under `source/frontend/` reference C-022 in any form | **ABSENT** |

---

## 7. Regression V&V — executed by this reviewer

**Staleness check first.** Every `AuthService` implementation and test file carries an mtime no later than `2026-09-15 17:46:34`; `conftest.py` (`2026-07-16`) and `dependencies.py` (`2026-08-29`) are untouched; HEAD is unchanged at `8323bf39…`; nothing is staged. The code is byte-identical to what `CERT-WP-21A` ran.

**This reviewer re-ran both suites anyway**, because Gate 2's mandate is broader than Gate 1's and because `§19.7b` is explicit that inherited evidence is not evidence:

```
py -3 -m pytest tests/test_commercial_account.py -v   =>  21 passed, 3 warnings in 4.18s
py -3 -m pytest tests/ -q                             =>  950 passed, 71 warnings in 236.98s
```

**21/21 targeted and 950/950 full regression — both independently reproduced, exact match to the figures claimed in `IMP-REPORT-WP-21 §5.7`.** Zero failures, zero skips, zero xfails. **No test file was modified to obtain a pass.** The 71 warnings are the pre-existing, WP-21-unrelated Starlette `HTTP_422_UNPROCESSABLE_ENTITY` rename deprecations.

Note for the record: `IMP-REPORT-WP-21 §5.7` correctly and transparently disclosed that the 950/950 figure had **not** been independently reproduced at Gate 1 attempt #1 and deferred that re-verification to Gate 2. It was subsequently reproduced at Gate 1 attempt #2, and **again independently here.** The claim is accurate.

---

## 8. Findings

### Critical — none
### High — none
### Medium — none

**No `CLAUDE.md §19.8.5`-class defect exists.** No architectural defect; no security defect; no data-integrity defect; no tenant-isolation defect (structurally impossible — §3 Q2); no failing test; no build failure; no broken functionality.

### Low / non-material (no remediation performed — Gate 3/4 not triggered)

| # | Finding | Independent assessment | Materially affects V&V correctness? | Disposition |
|---|---|---|---|---|
| **`V2-L-01`** | **Governance documents describing WP-21 are factually stale.** Confirmed still uncorrected at: `WPR-001:74` (status column — *"IMPLEMENTATION AUTHORIZED … IMPLEMENTATION NOT YET STARTED. No schema, migration, model, repository, service, router, frontend, or test exists"*; **and** its Gate column — *"No Gate dispatched. … the five-gate closure sequence has not begun"*), `WPR-001:76`, `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md:40` and `:183`, and `CBOR-INDEX.md:23`. All are now false: the implementation exists, Gate 1 has been dispatched twice, and this is Gate 2. `ADR-040`'s Physical Implementation Mapping row likewise still reads conceptual/planned — though `ADR-040` itself already anticipates requiring that correction. | **Confirmed accurate.** Re-verified by reading each location's current exact text this pass; not carried forward on trust. `CBOR-INDEX.md:23` is explicitly time-scoped (*"as of this entry"*) and self-discloses the follow-up, so it is the least misleading of the set. | **No.** Documentation state, not product behaviour. | `§19.7b` assigns this class **explicitly to Gate 5** (*"exists specifically to catch governance-documentation staleness (e.g., a status field still describing a superseded or already-completed state)"*). Recorded here so the complete six-location set enters Gate 5 visible, rather than being rediscovered piecemeal. **Not blocking Gate 2.** |
| **`V2-L-02`** | **No permanent regression test covers the collision-retry or 409 exhaustion path.** `services/commercial_account_service.py:112` still carries `# pragma: no cover - race backstop`; `tests/test_commercial_account.py` still seeds no colliding `account_reference`. The `status` CHECK constraint is likewise never negatively exercised by the suite (structurally unreachable through the API — no request field accepts a status). | **Confirmed accurate as a coverage statement — but its correctness premise is now discharged.** This audit forced a real UNIQUE collision through the real route and proved recovery, with a working negative control (§5.1), and separately proved the CHECK constraint real and enforced at production parity (§3 Q1). The behaviour is **correct**; only permanent coverage is absent. | **No.** Correctness is now empirically established. | **Technical Debt candidate** — Testing, **Medium severity** per the `§19.8.7` rubric (internal completeness; no Business Intent, security, or tenant-isolation boundary at stake). No `TECH-DEBT.md` entry exists for C-022/WP-21 yet (highest current id `TD-163`). This audit is **not authorized to write tests or amend the register**; recorded for the post-gate Technical Debt recording per `§19.8.2`. |
| **`V2-L-03`** | **The shared harness verifies persistence through the request's own uncommitted session.** `conftest.py`'s `client` fixture overrides `get_session` with a generator that never commits, and the assertions read back through that same session; production `get_session` (`models/database.py:73`) commits. `test_establish_happy_path_persists_active` and `test_end_to_end_establish_probe` therefore observe post-`flush`, in-transaction state. | **Confirmed accurate** by reading `conftest.py` in full. **The verification gap it describes is now closed** by Probe B, which used the real committing `get_session` and read back on a brand-new connection (§5.2). The production commit path is correct and unmodified. | **No.** Pre-existing, repository-wide harness property; `conftest.py` (mtime `2026-07-16`) is **unmodified by this Work Package** and identical for every previously certified WP. | `§19.7b` production-parity checklist item — answered at §3 Q1. **No WP-21 implementation change.** |
| **`V2-L-04`** | **Test harness does not enable `PRAGMA foreign_keys=ON`.** No pragma and no `connect` listener anywhere in `conftest.py`, so `fk_c022_commercial_account_parent_account_id` is unenforced throughout the suite. | **Confirmed accurate.** **And proven to be a harness limitation only**: Probe A executed the real migration DDL with FKs on and the constraint **rejected** an unknown parent while **accepting** a valid one (§3 Q1). Zero functional exposure for BA-01 — `parent_account_id` is hard-coded `None` and every probed row is NULL. | **No.** Harness property, not a product defect — the distinction is now proven rather than asserted. | Repository-wide harness-parity item, which `§19.7b` names as a root-cause class. **No WP-21 change.** |

### Observations (non-findings)

**`Obs-1` — ORM/migration uniqueness *shape* divergence.** The ORM declares `unique=True, index=True` (→ a unique index); the migration declares a plain index **plus** a separate `uq_c022_commercial_account_account_reference`. Independently probed: a duplicate `account_reference` is **rejected under both shapes**, and under the **PostgreSQL** dialect both render byte-equivalent column types. The only real-world effect is `alembic autogenerate` drift noise. Identical to the already-certified C-021 precedent (tracked there as `TD-162`). Non-material. *(This also disposes of `CERT-WP-21A`'s `O-1`: `IMP-REPORT-WP-21 §5.3`'s description of the index as "(unique)" is true of the ORM shape and loose about the migration shape; the report's own §3 describes the migration correctly. Cosmetic wording only.)*

**`Obs-2` — `COM-001-001`'s "and version" clause is not realized.** `COM-001-001` reads verbatim: *"Every commercial object possesses a globally unique, permanent identity in `PREFIX-NNNNNN` form, per SD-002-004, **alongside a canonical name and version**."* `c022_commercial_account` has `account_name` (the canonical name) but **no `version` column**, whereas the certified `c021_offering_definition` does carry one. **This is not an implementation defect and no implementation change is warranted or permitted:** `TDS-C022 §7` states the position explicitly (*"No in-place versioning exists at BA-01 scope"*); `IRA-TDS-C022_Independent_Review.md:132` quoted `COM-001-001` in full — including this clause — and raised only the `PREFIX-NNNNNN` format as `[C-3]`; the certified `c023_entitlement_context` (WP-17) likewise carries no version column under the same inherited Section 4; and Charter §25a is explicit that *"No field, endpoint, or business rule beyond §1–§20 is authorized"*, so adding one would itself violate `CLAUDE.md §18`. Recorded here for visibility as a **governance-level** item for a future C-022 increment, not as a WP-21 finding.

**`Obs-3` — the status closed set is expressed twice.** `models/c022_commercial_account.py:24` declares `ACCOUNT_STATUSES = ("active", "suspended", "retired")`, but the constant is **referenced nowhere** — the `CheckConstraint` at L95–98 repeats the set as a string literal, and the migration repeats it a third time. All three currently agree (verified), but they could drift independently. Cosmetic / maintainability only; mirrors the C-021 precedent.

**`Obs-4` — `get_by_account_reference` is wired to nothing.** Implemented in the repository but called by no service method and reachable from no route. This is **required** by `TDS-C022 §14`'s minimum repository method list and is explicitly disclosed in the repository docstring as existing for internal use and future-increment readiness, "not to imply a retrieval route exists." Conformant with the TDS; does **not** create a read surface (independently confirmed — §6). Not a `CLAUDE.md §10` dead-code violation, since the governing design mandates it.

**`Obs-5` — the router's documented 400 does not describe both 400 cases.** The OpenAPI `responses` entry reads *"Missing or malformed Authorization header"*, but `CommercialAccountService._coerce_actor_id` also returns 400 for an authenticated `PLATFORM_ADMIN` whose token lacks a `person_id` claim or carries a non-UUID one. Both behaviours are **correct and fail-closed** — this reviewer confirmed both empirically and confirmed **no row is written** in either case (§5.3). Documentation nuance only.

**`Obs-6` — runtime prefix `ACCOUNT-` is not lexically aligned with the CBOR identifier `CAC-000001`.** Explicitly permitted by `TDS-C022 §7` (the prefix token is `[IMPLEMENTATION-TIME]`), disclosed at `models/c022_commercial_account.py:26–33`, and consistent with the certified `OFFERING-` / `OFR-000001` precedent. Cosmetic.

**`Obs-7` — `COM-001-060`'s "once implemented" trigger has now fired.** Implementation exists, so the BAR obligation's own condition is met. It remains correctly **deferred** by an explicit Repository Owner decision (`ROD-C022-B` D10, Option A) and is described as deferred — never as satisfied — in every governance location this reviewer checked. No BAR artifact exists anywhere in the repository. This is exactly the disposition `CLAUDE.md §19.8.6` contemplates. Recorded so the obligation remains visible into Gate 5.

**`Obs-8` — `POST /commercial-accounts/` (trailing slash) returns 307 to the canonical path.** Verified with redirects disabled: `307 → /commercial-accounts`. **Byte-identical to the certified `/offerings/` precedent**, verified side by side in the same probe run. Standard FastAPI `redirect_slashes` behaviour; the tenant-middleware exemption covers both forms deliberately. Not a finding.

---

## 9. Treatment of the four carried-forward Gate 1 Low findings

Per instruction, each was **independently investigated, not auto-converted**:

| Gate 1 | Still factually accurate? | Materially affects V&V correctness? | Gate 2 disposition |
|---|---|---|---|
| `G1-L-01` — collision-retry path untested | **Yes**, as a *coverage* statement — the `pragma` and the test gap both confirmed by direct reading | **No** — and its correctness premise is now **discharged**: this audit forced a real collision through the real route and proved recovery, with a working negative control | → `V2-L-02`. Correctness **verified**; permanent coverage remains a Technical Debt candidate |
| `G1-L-02` — persistence tests share the request's uncommitted session | **Yes** — confirmed by reading `conftest.py` in full | **No** — the verification gap is now **closed** by Probe B's committed round-trip on a separate connection | → `V2-L-03`. Harness property, unmodified by WP-21 |
| `G1-L-03` — no SQLite FK pragma in the harness | **Yes** — confirmed absent | **No** — and now **proven** to be a harness limitation, not a product defect: the FK is real and is enforced at production parity | → `V2-L-04`. Answered in the §3 Q1 production-parity checklist |
| `G1-L-04` — stale WP-21 governance wording | **Yes** — all four locations `CERT-WP-21A` named re-verified stale this pass, plus `CBOR-INDEX.md:23` and `ADR-040`'s mapping row (six in total) | **No** — documentation state, not product behaviour | → `V2-L-01`. `§19.7b` assigns this class **explicitly to Gate 5** |

**None was escalated.** Gate 1's own severity classification is independently confirmed correct in all four cases. Two are now substantively *stronger* than Gate 1 could record, because this audit supplied the empirical evidence Gate 1 said was missing.

---

## 10. Change-boundary confirmation

- `git rev-parse HEAD` → **`8323bf3976818ff463cf67e891bd2a0a953777fd`**, unchanged.
- `git diff --cached --name-only` → **empty.** Nothing staged. Nothing committed. Nothing pushed.
- **Files modified by this audit: none.** No implementation file, no test file, no Charter, no TDS, no ROD, no ADR, no `CBOR-INDEX.md`, no `WPR-001`, no delivery map, no `TECH-DEBT.md`, and — explicitly — **not `IMP-REPORT-WP-21`, not `CERT-WP-21`, and not `CERT-WP-21A`.** All three remain intact as historical evidence. The implementation under review is byte-untouched.
- **Files created by this audit: exactly one** — this document.
- Probe programs were authored and executed under the session scratchpad, **outside the repository**, and no probe artifact was left in the working tree.
- Every other modified or untracked path in the working tree (the large pre-existing C-021/WP-20, `ROD-C040-*`, `ROD-Meta-Governance-*`, and `ADR-027`…`ADR-035` sets, and the 13 pre-existing modified tracked files) was confirmed to carry no C-022 content and was left exactly as found.
- **No finding was fixed.** Gate 3 (Remediation) and Gate 4 (Independent Verification of Remediation) are **not triggered**, because no defect requiring remediation was found.

---

## 11. Gate 2 decision

> ### ✅ **GATE 2 — VERIFICATION & VALIDATION AUDIT: PASS WITH NON-MATERIAL OBSERVATIONS**

**Basis.** Zero Critical, zero High, zero Medium findings. All 34 independently-derived RTM rows PASS. WP-21 / C-022 BA-01 is independently determined to be **functionally correct** (establish, `PREFIX-NNNNNN` allocation, validation, and every error path verified at runtime); **behaviourally compliant** (every `TDS-C022 §6`–`§15` normative behaviour traced and confirmed); **correctly integrated** (Router → Schema → Service → Repository → Model → Database and Authentication → Authorization → Middleware → Business Activity both verified end to end, with zero coupling to any other domain in either direction); **secure** (`require_platform_admin` byte-unchanged and enforced against 15 negative variants with no bypass and no row written; no injectable field reaches persistence; no authorization path widened); **persistent** (proven durable across a real commit boundary, read on a separate connection, against the migration-built table); **deterministic where required** (`active`-only status, always-NULL hierarchy, monotonic contiguous references across committed transactions, and a collision-recovery path now empirically proven with a working negative control); **correctly scoped** (every `§20` exclusion verified absent by code inspection *and* runtime probe, including D7, D8, D9, D10, and `§20.3` backend-only); **correctly authorized** (delivered content matches Charter §25a exactly, with nothing beyond §1–§20); **regression-safe** (950/950 independently reproduced); and **faithful to its approved Charter and TDS**.

`CLAUDE.md §19.8.5` is **not** engaged.

**Why "WITH NON-MATERIAL OBSERVATIONS" and not a clean PASS.** Four Low findings remain open, each a reassessment of a Gate 1 carry-forward and none blocking: `V2-L-01` is governance-documentation staleness that `§19.7b` assigns **by name** to Gate 5; `V2-L-03` and `V2-L-04` are pre-existing, repository-wide shared-harness properties unmodified by this Work Package, now explicitly answered in the `§19.7b` production-parity checklist and **proven** to be harness limitations rather than product defects; `V2-L-02` is a permanent-regression-coverage gap on a path this audit has now **proven correct**. Eight non-blocking Observations are recorded, of which only `Obs-2` touches a constitutional clause — and it is a governance-level item for a future increment that the implementation is **prohibited** from addressing under `CLAUDE.md §18` and Charter §25a.

**Gate 3 / Gate 4: NOT TRIGGERED.** No defect requiring remediation was found, so no remediation occurred and none requires independent re-verification.

### Gate eligibility

**WP-21 / C-022 BA-01 is now ELIGIBLE for Gate 5 — Release Readiness Audit**, per `CLAUDE.md §19.7b`'s sequence (Gates 3–4 skipped, correctly, because Gate 2 found nothing requiring remediation), to be dispatched to a **further fresh-context reviewer uninvolved in the implementation, in `CERT-WP-21`, in `CERT-WP-21A`, in the authoring of `IMP-REPORT-WP-21`, and in this audit**.

**Mandatory carry-forward inputs for Gate 5:**

1. **`V2-L-01` — six stale governance locations**, which Gate 5 exists specifically to catch and which must be synchronized (strikethrough-preserved per repository convention) before any push: `WPR-001:74` (**both** the status column and the Gate column), `WPR-001:76`, `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md:40`, `:183`, `CBOR-INDEX.md:23`, and `ADR-040`'s Physical Implementation Mapping row.
2. **`V2-L-02` — the `TECH-DEBT.md` entry**, which does not yet exist for C-022/WP-21 (highest current id `TD-163`). `CLAUDE.md §19.8.2` requires every accepted Technical Debt item to be recorded in the register, and `§19.8.2`'s own prohibition is explicit that Technical Debt *"SHALL NOT exist solely within Independent Review reports."* This audit is not authorized to amend the register.
3. **`Obs-7`** — the `COM-001-060` BAR deferral, whose "once implemented" trigger has now fired and which must remain visibly deferred rather than quietly dropped.
4. **`Obs-2`** — the unrealized `COM-001-001` "and version" clause, for Repository Owner visibility as a future-increment governance item, explicitly **not** remediable within WP-21's authorized scope.
5. **`§21.4`'s tenant-isolation checklist is structurally inapplicable** (§3 Q2) — this should be re-derived independently by the Gate 5 reviewer rather than adopted from this record.

---

*End of VV-AUDIT-WP-21. Gate 2 — Verification & Validation Audit: **✅ PASS WITH NON-MATERIAL OBSERVATIONS** (zero Critical, zero High, zero Medium; four Low, eight Observations). Gate 3 and Gate 4 NOT TRIGGERED. Independently performed 2026-09-16 by a fresh-context reviewer with no involvement in the WP-21 / C-022 implementation, in any C-022 governance artifact, in the authoring of `IMP-REPORT-WP-21`, or in either Gate 1 attempt. Four purpose-built runtime probes were authored from scratch and executed, including a genuine `account_reference` UNIQUE collision with a working negative control and a committed round-trip on a separate connection — closing, empirically, the two verification gaps Gate 1 recorded as `G1-L-01` and `G1-L-02`. Tests independently reproduced: 21/21 targeted, 950/950 full regression. `IMP-REPORT-WP-21`, `CERT-WP-21`, and `CERT-WP-21A` were read as evidence and were **not** modified. No implementation file, test file, governance document, or register was modified. No finding was fixed. Nothing was staged, committed, or pushed. WP-21 / C-022 BA-01 is certified at Gates 1 and 2 only — it is **NOT** closed and **NOT** release-ready; Gate 5 remains outstanding.*
