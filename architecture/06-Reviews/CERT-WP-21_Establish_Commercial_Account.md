# CERT-WP-21 — Gate 1 Independent Certification — Establish Commercial Account (C-022, WP-21 BA-01)

**Gate:** `CLAUDE.md §19.7b` Gate 1 — Independent Certification.
**Work Package / BA:** WP-21 — C-022 Customer & Account Management, BA-01 "Establish Commercial Account".
**Governing chain:** `CAP-001` (C-022, line 76) → `COM-001 §4`/`§7` (`COM-001-001`/`-002`/`-003`/`-033`/`-036`/`-060`, LOCKED) → `PE-001-C022` v1.2 → `ROD-C022` (D1–D6) → `IRA-C022` → `TDS-C022` (incl. `[C-3]`/`[C-4]`/`[C-5]` remediation) → `IRA-TDS-C022_Independent_Review.md` (PASS WITH CONDITIONS) → `ROD-C022-A` (D7, D8) → `ADR-038` (Option A) → `ROD-C022-B` (D9, D10) → `ADR-039` (CBOR preparation) → `ADR-040` (CBOR execution, `CAC-000001`) → `WP-21` BA-01 Charter (§25a Implementation Authorization) → implementation → this Gate 1 record.
**Date:** 2026-09-15.
**Repository HEAD at review:** `8323bf3976818ff463cf67e891bd2a0a953777fd`.

---

## CURRENT CERTIFICATION STATE

**Gate 1 — Independent Certification: ❌ FAIL** (2026-09-15, fresh-context independent reviewer).

- **Zero Critical findings. Zero High findings.**
- **One Medium finding (`G1-M-01`) — blocking.** The mandatory `CLAUDE.md §19.7` Implementation Report (`IMP-REPORT-WP-21`) does not exist anywhere in the repository. Under `§19.7`'s own Business Activity Completion Gate, that artifact is an Implementation-stage prerequisite sequenced **before** submission for Independent Review, and `§19.7`'s "Implementation Reporting & Independent Certification" clause names implementation reports as a required certification input. The Implementation half of the completion gate is therefore unsatisfied at the point Gate 1 was dispatched.
- **Four Low, non-material observations** — none is a `§19.8.5`-class defect; none requires an implementation change.
- **The implementation code itself passed every technical check performed in this review.** The FAIL is a governance/audit-trail defect, not a defect in the shipped code. Remediation is narrow, purely additive, and requires **no** change to any implementation file.

---

## 1. Reviewer independence

This is an **INDEPENDENT CERTIFICATION**, not an implementation report and not a self-certification.

The reviewer had **no** involvement in — and no conversational memory of — the WP-21 / C-022 implementation, `ROD-C022`, `ROD-C022-A`, `ROD-C022-B`, `IRA-C022`, `TDS-C022`, `IRA-TDS-C022_Independent_Review.md`, the WP-21 BA-01 Charter, `ADR-038`, `ADR-039`, or `ADR-040`. Every material claim below was re-derived directly from actual repository source: the governance documents were read in full from disk; every implementation file was read in full; the targeted test suite was executed by this reviewer; `alembic heads` / `alembic branches` were executed by this reviewer; `git rev-parse HEAD`, `git status --short`, `git diff --cached --name-only`, and targeted `git diff` output were inspected directly. No factual claim in this document is carried forward from any prior session's assertion.

Per `CLAUDE.md §19.7`'s fresh-context reviewer requirement, nothing below is synthesized from the implementing session's own conversational memory.

## 2. Scope of certification

WP-21 / C-022 BA-01 only — establish exactly one standalone Authoritative Commercial Account, `POST /commercial-accounts`, platform-global, `require_platform_admin`-gated, `AuthService`-hosted, per `ROD-C022` §H/D1–D5 as constrained by `ROD-C022-A` D7/D8, `ROD-C022-B` D9/D10, `ADR-038` Option A, and the Charter's §25a Implementation Authorization.

This Gate 1 record does **not** close C-022 as a capability. C-022 capability-wide status is as `IRA-C022` records it, unchanged. This record does not proceed to, prejudge, or substitute for Gate 2 (V&V Audit), Gates 3–4 (Remediation and its Independent Verification), or Gate 5 (Release Readiness Audit).

## 3. Requirement / evidence matrix

Every row was verified against the cited file directly. "Verified" means the reviewer located the construct and confirmed it does what the governing text requires — not that the design document restates it.

### 3.1 TDS-C022 §6–§21 and Charter §1–§20 — normative requirements

| # | Requirement (source) | Implementation evidence | Result |
|---|---|---|---|
| 1 | Conceptual table `c022_commercial_account` (`TDS §6.1`, Charter §8) | `alembic/versions/2026_09_15_0900-f6a7b8c9d0e1_c022_commercial_account.py:68` `op.create_table('c022_commercial_account', ...)`; ORM `models/c022_commercial_account.py:93` `__tablename__` | PASS |
| 2 | `id` UUID PK, default `uuid4` | Migration L69 + `sa.PrimaryKeyConstraint('id', name='pk_c022_commercial_account')` L77; model L101–104 `primary_key=True, default=uuid.uuid4` | PASS |
| 3 | `account_reference` String(30), NOT NULL, UNIQUE | Migration L70 + `sa.UniqueConstraint('account_reference', name='uq_c022_commercial_account_account_reference')` L82; model L107–112 `String(30), nullable=False, unique=True, index=True` | PASS |
| 4 | `account_name` String(255), NOT NULL, **no** uniqueness invariant (`TDS §6.1`) | Migration L71 (no unique constraint on this column anywhere in the file); model L119–122 | PASS |
| 5 | `status` String(20), CHECK `{active,suspended,retired}`, NOT NULL (`TDS §6.1`/`§9`) | Migration L72 + `sa.CheckConstraint("status IN ('active', 'suspended', 'retired')", name='ck_c022_commercial_account_status')` L83–86; model L94–99 identical `CheckConstraint`; `ACCOUNT_STATUSES` L24 | PASS |
| 6 | BA-01 writes **only** `'active'` (`TDS §9`, Charter §14) | `services/commercial_account_service.py:104` `"status": "active"` — the sole literal; no other write path exists in the module | PASS |
| 7 | `parent_account_id` nullable self-referential FK, declared, **never** written non-NULL (`TDS §10`, Charter §13) | Migration L73 + `sa.ForeignKeyConstraint(['parent_account_id'], ['c022_commercial_account.id'], name='fk_c022_commercial_account_parent_account_id')` L78–81; model L132–135; service L105 `"parent_account_id": None` — hard-coded, not caller-derived | PASS |
| 8 | `created_by_actor_id` UUID NOT NULL, **not** a FK (`TDS §6.1`) | Migration L74 `sa.Column('created_by_actor_id', sa.UUID(), nullable=False)` — no `ForeignKeyConstraint` references it; model L138–140 has no `ForeignKey` | PASS |
| 9 | `created_at` NOT NULL / `updated_at` NULLABLE, `DateTime(timezone=True)` | Migration L75–76; model L147–157 | PASS |
| 10 | **No `organization_id` column** (`TDS §6.1`/`§11`, `ROD-C022` D2, Charter §12) | Migration column list L69–76 contains no such column; model column set contains none. Independently re-confirmed at runtime by `test_c022_table_has_no_organization_id_or_classification_column` (live `inspect()` introspection) and `test_orm_model_declares_no_organization_id` (ORM metadata), both of which this reviewer executed. Also confirmed no column name contains `tenant`. | PASS |
| 11 | **No `classification` column/field anywhere** (`ADR-038` Option A, `ROD-C022-A` D7, `TDS §4`/`§6.1`, Charter §15) | Repo-wide grep across all six C-022 implementation files returns **only** docstring/comment occurrences asserting its absence — zero code occurrences. Migration has no such column; ORM has no such attribute; `schemas/commercial_account.py` has no such field in either model. Runtime-confirmed by `test_orm_model_declares_no_classification_column` and `test_no_classification_field_in_response_or_schema` | PASS |
| 12 | `account_reference` SHALL be `PREFIX-NNNNNN` (`COM-001-001` inherited by §7; `TDS §7` post-`[C-3]`; Charter §7) | `models/c022_commercial_account.py:34` `ACCOUNT_REFERENCE_PREFIX = "ACCOUNT"`; `services/commercial_account_service.py:158` `f"{_ACCOUNT_REFERENCE_PREFIX}-{current_max + 1:06d}"` → `ACCOUNT-000001`. Six-digit zero-padded suffix confirmed. Prefix token is `[IMPLEMENTATION-TIME]` per `TDS §7`; the spelled-out-word choice mirrors the certified `OFFERING_REFERENCE_PREFIX = "OFFERING"` / `OFR-000001` precedent and is explicitly disclosed at model L26–33 | PASS |
| 13 | `account_reference` system-assigned; caller cannot supply or override (`TDS §8`, Charter §6) | `schemas/commercial_account.py:21–49` — `EstablishCommercialAccountRequest` declares **exactly one** field, `account_name`. `account_reference`/`id`/`status`/`parent_account_id`/`created_by_actor_id` are structurally absent from the request contract, matching `TDS §16`'s "not present in the schema at all" enforcement rather than a runtime reject. Runtime-confirmed by `test_account_reference_is_system_assigned_caller_cannot_override` | PASS |
| 14 | Acceptance properties: system-assigned, monotonic, unique, concurrency-safe (`TDS §7`) | System-assigned — row 13. Monotonic — `_next_account_reference` (service L156–158) = `MAX(suffix)+1`; runtime-confirmed contiguous by `test_account_reference_is_monotonic_and_unique` (L138 asserts `suffixes == list(range(suffixes[0], suffixes[0]+5))`, i.e. genuine contiguity, not merely uniqueness). Unique — UNIQUE constraint (row 3). Concurrency-safe — UNIQUE constraint as backstop + allocate-and-retry (service L96–127) | PASS (see `G1-L-01` on retry-path test coverage) |
| 15 | Allocator must be PostgreSQL-portable — fixed-offset `substr`, never `instr()` (WP-20 Gate 5 remediation) | `repositories/c022_commercial_account_repository.py:17` `_REFERENCE_SUFFIX_OFFSET = len(ACCOUNT_REFERENCE_PREFIX) + 2` (= 9; verified correct: `ACCOUNT` occupies 1-based positions 1–7, `-` is 8, suffix starts at 9). L59–63 uses `func.substr(col, _REFERENCE_SUFFIX_OFFSET)` with no search function. Verified **not** by reading the comment but by the two tests this reviewer executed: `test_max_reference_sequence_query_has_no_sqlite_only_function` compiles the query under both the PostgreSQL and SQLite dialects and asserts `instr(`/`strpos(`/`position(` absent and the two SQL strings byte-identical; `test_max_reference_sequence_runtime_sql_has_no_sqlite_only_function` attaches a `before_cursor_execute` listener and asserts the **actually executed** statement contains no `instr(` | PASS |
| 16 | `POST /commercial-accounts`, 201, `Depends(require_platform_admin)` (`TDS §15`, Charter §10) | `routers/commercial_account.py:26–29` `@router.post("", response_model=CommercialAccountResponse, status_code=status.HTTP_201_CREATED)`; L57 `claims: Annotated[dict, Depends(require_platform_admin)]`; `main.py` mounts `commercial_account.router` at prefix `/commercial-accounts` | PASS |
| 17 | **No other route** is registered (`TDS §15`, `ROD-C022-A` D8, Charter §20) | `routers/commercial_account.py` contains exactly one `@router.` decorator (L26). Runtime-confirmed by `test_no_read_or_list_endpoint_exists` (GET collection and GET item both 404/405) and `test_no_state_transition_endpoint_exists` (reclassify / retire / reactivate / transition / PATCH all 404/405) | PASS |
| 18 | Blank `account_name` → 422 (`TDS §16`, Charter §19) | `schemas/commercial_account.py:29–41` — `min_length=1` plus a `field_validator` rejecting `v.strip() == ""`. Runtime-confirmed by `test_blank_account_name_is_422` and `test_missing_account_name_is_422` | PASS |
| 19 | Non-`PLATFORM_ADMIN` → 403; no role → 403; missing/malformed `Authorization` → 400 (`TDS §19`) | Enforced by the unmodified `dependencies.require_platform_admin` / `get_current_claims` chain. Runtime-confirmed by four tests: `test_non_platform_admin_is_forbidden`, `test_no_role_claim_is_forbidden`, `test_missing_authorization_header_is_400`, `test_malformed_authorization_header_is_400` | PASS |
| 20 | `middleware/tenant.py` gains one exemption prefix pair (`TDS §12`, Charter §11) | `middleware/tenant.py` diff adds exactly `or path == "/commercial-accounts" or path.startswith("/commercial-accounts/")` plus a rationale comment citing `ROD-C022` D2. Scoping verified correct — see §4.3 | PASS |
| 21 | Audit: `record_audit(action="ESTABLISH_COMMERCIAL_ACCOUNT", ..., status=SUCCESS, metadata={account_reference, account_name})` (`TDS §17`) | `services/commercial_account_service.py:129–140`. Runtime-confirmed by `test_establish_emits_success_audit`, which asserts action, `actor_id` equals the caller's `person_id` claim, `metadata["status"] == "active"`, and the reference matches `^ACCOUNT-\d{6}$` | PASS |
| 22 | `publish_event("COMMERCIAL_ACCOUNT_ESTABLISHED", ...)` via the existing structured-log stand-in; no new mechanism (`TDS §17`) | Service L141–149; imported from the existing `observability` module. No new event infrastructure introduced | PASS |
| 23 | Allocate-and-retry on `IntegrityError` → rollback → retry (`TDS §18`) | Service L96–127 — 5-attempt loop; `except IntegrityError` → `session.rollback()` → `continue`; `for…else` raises 409 with a DENIED audit record on exhaustion | PASS structurally; see `G1-L-01` |
| 24 | Module placement mirrors `c021_offering_definition`'s layout (`TDS §13`, Charter §9) | All five files present at the exact designed paths: `models/c022_commercial_account.py`, `repositories/c022_commercial_account_repository.py`, `services/commercial_account_service.py`, `routers/commercial_account.py`, `schemas/commercial_account.py`. No new service created | PASS |
| 25 | Repository: `BaseRepository`-derived; `create()`, `get_by_id()`, `get_by_account_reference()` (`TDS §14`) | `C022CommercialAccountRepository(BaseRepository[C022CommercialAccount])` L20; `get_by_account_reference` L37–44; `get_by_id` inherited from `BaseRepository`; `create` inherited. `get_by_account_reference` exists but is **not** wired to any route — correctly disclosed at repository L28–31 as internal/future-readiness, not a retrieval surface | PASS |
| 26 | `AuthService` hosting, no new service (`ROD-C022` D3, `TDS §5`) | All files under `Backend/Services/AuthService/`; `main.py` change is two `include_router` lines (one of which is pre-existing C-021 content) plus the import | PASS |
| 27 | Migration purely additive, no `ALTER` (`CLAUDE.md §18`/`§19.4`) | Migration contains exactly one `op.create_table` and one `op.create_index`; no `op.alter_*`, no `op.add_column` anywhere in the file | PASS |
| 28 | Migration chains from the actual head; single non-branching head today | `down_revision = 'e5f6a7b8c9d0'` (L61). Independently executed by this reviewer: `alembic heads` → `f6a7b8c9d0e1 (head)` (exactly one); `alembic branches` → empty | PASS |
| 29 | Test set per `TDS §20` / Charter §19 | 21 tests present and executed — see §6 | PASS |

### 3.2 Charter §15–§21 — settled governance determinations

| Determination | Requirement | Evidence | Result |
|---|---|---|---|
| Charter §15 / `ADR-038` / D7 | No classification attribute | Matrix row 11 | HONORED |
| Charter §16 / `ROD-C022-B` D9 | Collapsed single-call lifecycle accepted; **no** separately-observable Anchor / Intent / Proposed / Assessment stage introduced | Exactly one endpoint; `CommercialAccountService` exposes exactly one public method, `establish` (L75); no anchor/intent/proposal/assessment table, column, route, schema, or method exists anywhere in the C-022 files. The single-call realization is explicitly disclosed at model L84–90 and service L30–33 | HONORED |
| Charter §17 / `ADR-040` | CBOR registered as `CAC-000001`, mapped to C-022 | `CBOR-INDEX.md:40` — `` | `CAC-000001` | Commercial Account | C-022 (Customer & Account Management) | ADR-040 | IRA-C022 §11 | ``. Registering ADR reference resolves: `architecture/07-Decisions/ADR-040_Commercial_Account_Canonical_Business_Object_Registration.md` exists | VERIFIED |
| Charter §18 / `ROD-C022-B` D10 | BAR deferred — no registry, no mechanism, no Business Activity Identifier | Repository-wide search: no `BAR-INDEX` or equivalent file exists anywhere; no `BAR` / `business_activity_registry` / `business_activity_id` construct appears in any C-022 implementation file. CBOR and BAR are **not** conflated — model L26–33 explicitly distinguishes the `ACCOUNT` reference prefix from "the short CBOR code", and `CBOR-INDEX.md:23` records the BAR obligation as a separate, still-deferred item that is not a dependency of the `CAC-000001` registration | HONORED |
| Charter §20 | Out-of-scope boundaries | No Customer entity/table/route; no Customer–Account Relationship; no Organization reference or equivalence; no Identity/Person wiring; no Subscription/Billing/Contract/Entitlement construct; no reclassify/retire/reactivate; no merge/split/transfer; no CRM construct; no read/list route; no invented lifecycle policy. Each independently confirmed by direct file inspection and, where an endpoint could exist, by executed runtime probe (tests at L172–191) | HONORED |
| Charter §21 | `CLAUDE.md §20.3` backend-only determination | `grep -rilE "commercial.?account\|c022\|C-022" source/frontend/src` returns **zero** files. No frontend artifact for this Business Activity exists. `§20.7`'s Enterprise Experience completion-gate extension correctly does not apply, per `§20.3`'s own charter-exception clause | HONORED |
| Charter §25a | Implementation Authorization scope | The authorization is bounded to Charter §1–§20 and explicitly excludes classification, read/list, BAR, frontend, and every §20 item. Cross-checked against what the code actually does: the code implements exactly the §10 endpoint over the §8 schema with the §7 reference rule, the §13 unexercised hierarchy column, and the §14 `active`-only write — and implements **none** of the excluded items. No field, endpoint, or business rule beyond §1–§20 was found | CONFORMANT |

## 4. Security and authorization

### 4.1 `require_platform_admin` is unmodified

`git diff -- dependencies.py` returns **empty** — the file is byte-identical to HEAD (`8323bf3`), i.e. byte-for-byte the same gate every previously certified route uses. Its definition (`dependencies.py:47–56`) rejects any caller whose `role_code` claim is not `PLATFORM_ADMIN` with 403, and its upstream `get_current_claims` returns 400 on a missing/malformed `Authorization` header.

### 4.2 No alternate or weaker auth path

`routers/commercial_account.py` contains one route, and that route declares `Depends(require_platform_admin)`. No route in the module uses `require_matching_tenant_or_platform_admin`, `get_current_claims` alone, or no dependency. `get_commercial_account_service` (L20–23) is a session-wiring dependency only and performs no authorization decision. There is no second registration of this router anywhere in `main.py`.

### 4.3 Tenant-middleware exemption scoping

The added exemption is `path == "/commercial-accounts" or path.startswith("/commercial-accounts/")`. This is the exact-prefix pair pattern already used for `/roles` and `/organizations`. It is correctly scoped: it matches the collection path and its subtree only, and does **not** match a differently-named sibling such as `/commercial-accounts-export` (which `startswith("/commercial-accounts")` alone would have wrongly matched). No pre-existing exemption entry was modified, broadened, or removed — the diff is a pure two-line insertion into the existing chain.

### 4.4 Cross-tenant / scope-leakage risk

Structurally none, and this was verified rather than assumed. There is no tenant or organization column in the migration (columns are exactly `id`, `account_reference`, `account_name`, `status`, `parent_account_id`, `created_by_actor_id`, `created_at`, `updated_at`) and none in the ORM model. Both facts are asserted at runtime by executed tests — one via live `inspect()` table introspection against the actual created table, one via ORM metadata — and both also assert no column name contains `tenant`. With no tenant column, no tenant predicate, and a `PLATFORM_ADMIN`-only gate, there is no per-tenant data boundary for a caller to cross. `CLAUDE.md §21.4`'s Mandatory Tenant-Isolation Test Checklist is structurally inapplicable, exactly as `TDS §11` and Charter §12 disclose, and the prescribed substitute assurance (a, b, c) is present in full.

No request field accepts a foreign-object identifier of any kind, so `§21.4(c)`'s unrelated-identifier probe has no applicable surface.

## 5. Data model and migration

Column types, nullability, and constraints are enumerated in §3.1 rows 2–10 and were read directly from the migration file, not inferred from the ORM. Constraint coverage is complete against `TDS §6.1`: PK (`pk_c022_commercial_account`), UNIQUE (`uq_c022_commercial_account_account_reference`), CHECK on `status` (`ck_c022_commercial_account_status`), self-referential FK (`fk_c022_commercial_account_parent_account_id`), plus one index (`ix_c022_commercial_account_account_reference`). All constraints are explicitly named. `downgrade()` correctly reverses both objects.

The ORM model's `CheckConstraint` string is byte-identical to the migration's, so the two cannot silently diverge on the status vocabulary.

Alembic chain: `down_revision = 'e5f6a7b8c9d0'` chains from the WP-20 / C-021 migration. This reviewer executed `alembic heads` and observed exactly one head, `f6a7b8c9d0e1` — this migration — and `alembic branches` returned empty. No branch, no multiple heads.

The migration was **not** executed against a live PostgreSQL server in this pass (`alembic/env.py` requires a reachable server); verification was by direct read, ORM comparison, and `alembic heads`. This matches the disposition recorded for every prior `AuthService` Work Package, including `CERT-WP-20 §4` observation 4, and is carried forward as `G1-L-04`.

## 6. Test results — independently reproduced

Executed by this reviewer, from `Backend/Services/AuthService`, with `JWT_SECRET_KEY` set:

```
py -3 -m pytest tests/test_commercial_account.py -v
...
======================= 21 passed, 3 warnings in 11.72s =======================
```

**21 collected, 21 passed, 0 failed, 0 errors** — independently reproduced, not cited from any prior claim. (The three warnings are pre-existing third-party deprecation notices — Starlette/httpx and `HTTP_422_UNPROCESSABLE_ENTITY` — unrelated to this Business Activity.)

**Full regression suite:** this reviewer did **not** execute the full `AuthService` regression suite, and this document makes **no** claim about its result. No prior full-regression figure is relied upon or restated here as a finding. This is justified on the basis that the C-022 change set is additive — six new files plus three additive edits (`main.py` import + one `include_router` line; `middleware/tenant.py` comment + one exemption line; `models/__init__.py` import + `__all__` entry) — and modifies no shared code path. Executing the full regression is appropriately a Gate 2 (V&V) activity.

**Test-quality assessment (judged per test, not by count):**

- *Genuine, well-targeted.* `test_account_reference_is_monotonic_and_unique` does more than its name's weakest reading — beyond asserting 5 distinct references and sorted order, L138 asserts full contiguity (`suffixes == list(range(suffixes[0], suffixes[0]+5))`), which actually exercises the `MAX+1` allocator rather than merely uniqueness.
- *Genuine.* The two portability tests (L300–356) verify the WP-20 Gate 5 property empirically — one by dual-dialect compilation, one by intercepting the **actually executed** SQL via a `before_cursor_execute` listener — rather than by trusting the source comment. This reviewer specifically checked this, as the comment alone would not have been acceptable evidence.
- *Genuine.* The two absence-of-endpoint tests probe five state-transition shapes and two read/list shapes against the running app and require 404/405, rather than asserting absence by reading the router.
- *Genuine.* The schema-absence tests use two independent mechanisms (live DB introspection and ORM metadata), satisfying `TDS §11`'s substitute-assurance requirement (c) as written.
- *Weaker than its name suggests.* `test_establish_happy_path_persists_active` and `test_end_to_end_establish_probe` verify persistence through the **same** session object the request used: the shared `conftest.py` `client` fixture overrides `db_manager.get_session` with a generator that yields `db_session` and never commits, whereas production `get_session` (`models/database.py:70–78`) commits on successful exit. The row is therefore observed post-`flush`, in-transaction, not after a committed round-trip on a separate connection. The production commit path is correct; the test's assurance is narrower than "persisted". Recorded as `G1-L-02`. This is a property of the pre-existing shared harness (unmodified by this Work Package), identical for every previously certified Work Package.
- *Gap.* No test exercises the `IntegrityError` allocate-and-retry path or the 409 retry-exhaustion path. The `except IntegrityError` block carries `# pragma: no cover - race backstop` (service L112). A colliding `account_reference` is never pre-seeded. Recorded as `G1-L-01`.
- *Gap.* No test attempts an out-of-vocabulary `status` write, so the CHECK constraint is never negatively exercised. Not reachable through the API (no field accepts it), so no functional exposure. Folded into `G1-L-01`.

## 7. Findings

### Medium — blocking

---

**`G1-M-01` — The mandatory Implementation Report `IMP-REPORT-WP-21` does not exist.**

- **Severity:** Medium (materially affects governance).
- **File / location:** `architecture/05-Implementation/` — expected `IMP-REPORT-WP-21_Establish_Commercial_Account.md`; absent.
- **Evidence:** `ls architecture/05-Implementation/ | grep "^IMP-REPORT"` returns reports for WP-01 through WP-12, WP-14 through WP-20, and WP-RTA-001 — an unbroken convention across every Work Package that has an implementation. There is no WP-21 entry. `grep -rl "IMP-REPORT-WP-21" --include=*.md .` returns **nothing** — the artifact is not referenced anywhere in the repository, let alone present. The only WP-21 document in `architecture/05-Implementation/` is the Charter.
- **Governing requirement:** `CLAUDE.md §19.7`'s Business Activity Completion Gate lists, under **Implementation** and therefore sequenced *before* the **Independent Review** block: *"✓ The Work Package Implementation Report (IMP-REPORT-WP-XX) has been updated. ✓ Implementation Status is marked 'IMPLEMENTATION COMPLETE'."* The same section's "Implementation Reporting & Independent Certification" clause further states that certification *"SHALL be performed independently using the approved architecture, implementation reports, source code, tests, APIs, database migrations, and other implementation evidence"* — naming implementation reports as a required certification input. `CERT-WP-20` confirms this is the established practice: `IMP-REPORT-WP-20` appears in that record's own governing chain (§5 header line) and in its change-control section (§5).
- **Impact:** The Implementation half of `§19.7`'s completion gate is unsatisfied at the point Gate 1 was dispatched, so Gate 1 cannot properly pass. Downstream, the audit trail that Gate 2 (V&V) and Gate 5 (Release Readiness) are each required to work from is missing its central implementation-evidence document; Gate 2's own Requirements Traceability Matrix and Gate 5's source-versus-governance consistency check both have no implementation report to reconcile against. There is **no** effect on code correctness, security, tenant isolation, or delivered scope.
- **Required remediation:** Author `architecture/05-Implementation/IMP-REPORT-WP-21_Establish_Commercial_Account.md` following the `IMP-REPORT-WP-20` structure, recording the BA-01 implementation, the governing-document basis, the evidence, the test results, the disclosed observations, and an Implementation Status of "IMPLEMENTATION COMPLETE". Then re-dispatch Gate 1 to a further fresh-context reviewer. **No implementation file requires any change.**

---

### Low — non-blocking

**`G1-L-01` — Allocate-and-retry concurrency backstop is untested.**
*File/location:* `services/commercial_account_service.py:112` (`except IntegrityError as exc:  # pragma: no cover - race backstop`) and L116–127 (the `for…else` 409 path); `tests/test_commercial_account.py` (no test pre-seeds a colliding `account_reference`).
*Evidence:* No test in the file creates a UNIQUE collision on `account_reference`; the retry and exhaustion branches are never entered. The CHECK constraint on `status` is likewise never negatively exercised.
*Impact:* The concurrency property `TDS §7`/`§18` require is asserted structurally (UNIQUE constraint + retry loop, read and confirmed correct by this reviewer) but not demonstrated empirically. Low: the design is sanctioned by `TDS §18`, and the code is a faithful mirror of the certified `OfferingDefinitionService.establish` pattern, whose identical `# pragma: no cover` block was carried as `CERT-WP-20 §4` observation 1 through all five WP-20 gates.
*Remediation:* Add a concurrency/collision regression test at Gate 2 (e.g. pre-seed `ACCOUNT-000001` directly, then establish and assert the allocator recovers). Candidate `CLAUDE.md §19.8` Technical Debt entry, Medium severity per `§19.8.7` (internal robustness/completeness, no Business Intent or security boundary at stake).

**`G1-L-02` — Persistence tests verify through the request's own uncommitted session.**
*File/location:* `tests/conftest.py:46–57` (`client` fixture overrides `db_manager.get_session` with a non-committing generator yielding the same `db_session`), versus `models/database.py:70–78` (production `get_session` commits).
*Evidence:* `test_establish_happy_path_persists_active` (L93–98) and `test_end_to_end_establish_probe` (L285–291) query `db_session` — the identical session the route used — so they observe post-`flush`, in-transaction state, not a committed round-trip.
*Impact:* Low. The production commit path is correct and unmodified; the tests' assurance is simply narrower than the word "persists" implies. This is a pre-existing, repository-wide shared-harness property — `conftest.py` is unmodified by this Work Package and identical for every previously certified Work Package.
*Remediation:* A harness-parity item for Gate 2's `§19.7b` production-parity checklist, not a WP-21 implementation change.

**`G1-L-03` — Test harness does not enable `PRAGMA foreign_keys=ON`.**
*File/location:* `tests/conftest.py` (no pragma or `connect` event listener anywhere in the file).
*Evidence:* SQLite disables foreign-key enforcement by default; the harness never enables it, so `fk_c022_commercial_account_parent_account_id` is unenforced in tests.
*Impact:* **None functionally for BA-01** — `parent_account_id` is hard-coded `None` on every write and no route ever sets it. Low, and identical to `CERT-WP-20 §4` observation 5.
*Remediation:* Repository-wide harness-parity item for Gate 2's production-parity checklist; explicitly named by `§19.7b` as a root-cause class. No WP-21 change.

**`G1-L-04` — Governance documents describing WP-21 are now factually stale.**
*File/location:* `architecture/00-Governance/WPR-001_Work_Package_Roadmap.md:74` (WP-21 row) and `architecture/00-Governance/CBOR-INDEX.md:23`.
*Evidence:* The `WPR-001` WP-21 row still states *"IMPLEMENTATION AUTHORIZED (RO, 2026-09-15) — IMPLEMENTATION NOT YET STARTED. No schema, migration, model, repository, service, router, frontend, or test exists"*, and its Gate column states *"**No Gate dispatched.** No implementation exists; `CLAUDE.md §19.7b`'s five-gate closure sequence has not begun."* Both are now false: the implementation exists and Gate 1 has been dispatched. `CBOR-INDEX.md:23` similarly records *"no `c022_commercial_account` table, model, migration, or API exists as of this entry"* — though that line is explicitly time-stamped and already self-discloses that *"`ADR-040`'s own Physical Implementation Mapping row is explicitly conceptual/planned and will require a follow-up correction once implementation exists"*, so its staleness was anticipated rather than overlooked. The Charter's own header and §25a carry equivalent as-of-that-pass statements; per this review's change-control constraints the Charter was not modified, and its statements are correctly read as scoped to the governance pass that recorded them.
*Impact:* Low, and **not** independently blocking. `CLAUDE.md §19.7b` assigns exactly this class of governance-documentation staleness to Gate 5 (Release Readiness Audit), which *"exists specifically to catch governance-documentation staleness (e.g., a status field still describing a superseded or already-completed state)"*. It is recorded here so it is visible from the start of the gate sequence rather than discovered at Gate 5.
*Remediation:* Synchronize the `WPR-001` WP-21 row (status + Gate column) and the `ADR-040` / `CBOR-INDEX` Physical Implementation Mapping row as part of the Gate 1 recording pass or, at the latest, before Gate 5. Strikethrough-preserve per repository convention.

### Observations (non-findings)

1. `CommercialAccountResponse` (`schemas/commercial_account.py:52–63`) includes `updated_at`, which `TDS §15` / Charter §10 do not enumerate in their response list (`id`, `account_reference`, `account_name`, `status`, `parent_account_id`, `created_at`). `updated_at` is part of the persisted row per `TDS §6.1` and is always `null` at establish. No new semantic, no prohibited data, and `created_by_actor_id` is correctly **excluded** from the response. Non-material.
2. The request schema does not set `extra="forbid"`, so Pydantic's default `ignore` applies and unknown body fields are silently dropped. This is exactly what `TDS §16` specifies (*"ignored (not present in the schema at all) — mirrors `c021_offering_definition`'s own 'not in the schema' enforcement rather than a runtime override-and-reject check"*), and is confirmed at runtime by `test_account_reference_is_system_assigned_caller_cannot_override`. Conformant, not a finding.
3. The runtime reference prefix `ACCOUNT-` is not lexically aligned with the CBOR identifier `CAC-000001`. Permitted by `TDS §7` (prefix token is `[IMPLEMENTATION-TIME]`), explicitly disclosed at `models/c022_commercial_account.py:26–33`, and consistent with the certified `OFFERING-` / `OFR-000001` precedent (`CERT-WP-20 §4` observation 2). Cosmetic.
4. On a non-uniqueness `IntegrityError` (e.g. a CHECK or FK violation), the retry loop would exhaust and return a 409 whose message names Account Reference allocation, which would be misleading. Structurally unreachable at BA-01 scope — every constrained value the service writes is a fixed literal. Identical to the certified C-021 precedent. Non-material.
5. No C-022 or WP-21 entry exists in `architecture/06-Reviews/TECH-DEBT.md`. Consistent with Gate 1 not yet having concluded; `G1-L-01` is the candidate entry.

## 8. Change-boundary confirmation (verified by this reviewer)

- `git rev-parse HEAD` → **`8323bf3976818ff463cf67e891bd2a0a953777fd`** — matches the expected hash exactly.
- `git diff --cached --name-only` → **empty**. Nothing is staged.
- Nothing was committed or pushed by this review.
- **C-022 implementation files (all untracked, all new):** `models/c022_commercial_account.py`, `repositories/c022_commercial_account_repository.py`, `services/commercial_account_service.py`, `schemas/commercial_account.py`, `routers/commercial_account.py`, `alembic/versions/2026_09_15_0900-f6a7b8c9d0e1_c022_commercial_account.py`, `tests/test_commercial_account.py`.
- **Additive edits to three tracked files, diffed line by line:** `main.py` (one import extension + one `include_router` line for `commercial_account`), `middleware/tenant.py` (one rationale comment block + one exemption line pair), `models/__init__.py` (one import + one `__all__` entry). Every one of these three files also carries pre-existing, unrelated WP-20 / C-021 content in the same diff; that content was reviewed only enough to confirm it is not C-022's, and is not commented on here.
- **Every other modified or untracked path in the working tree was confirmed to carry no C-022 / commercial-account content** and was left exactly as found. This includes the ~13 pre-existing modified tracked files (`CLAUDE.md`, `CAP-001`, `SER-001`, `TECH-DEBT.md`, `ADR-002`, `admin-navigation.ts`, and others) and the large set of pre-existing untracked files (the C-021 / WP-20 implementation and frontend, the `ROD-C040-*` / `ROD-Meta-Governance-*` governance set, `ADR-027`…`ADR-035`, and others).
- **Files created by this review:** exactly one — this document, `architecture/06-Reviews/CERT-WP-21_Establish_Commercial_Account.md`.
- **Files modified by this review:** **none.** No implementation file, no Charter, no TDS, no ROD, no ADR, no register was touched. The implementation that was reviewed is byte-untouched.

## 9. Gate 1 decision

> ### ❌ **GATE 1 — INDEPENDENT CERTIFICATION: FAIL**

**Basis.** One Medium finding (`G1-M-01`) that materially affects governance: the `CLAUDE.md §19.7`-mandated Implementation Report `IMP-REPORT-WP-21` does not exist. `§19.7` sequences that artifact within the Implementation block, *before* submission for Independent Review, and names implementation reports as a required certification input. The Implementation half of the Business Activity Completion Gate is therefore unsatisfied, and Gate 1 cannot pass over it.

**What this FAIL is not.** It is not a defect in the delivered code. On every technical dimension examined — scope fidelity against `ROD-C022` §H / D1–D10 / `ADR-038` / `ADR-040` / the Charter's §25a authorization; the absence of classification, Customer, Relationship, Organization equivalence, Identity/Person wiring, read/list, state transitions, BAR constructs, and frontend artifacts; the platform-global security model and the unmodified `require_platform_admin` gate; the correctly-scoped tenant-middleware exemption; the data model, constraints, and single non-branching Alembic head; the `COM-001-001` `PREFIX-NNNNNN` reference contract and its PostgreSQL-portable allocator; the API contract and validation behavior; and 21/21 independently reproduced tests — the implementation was found **conformant**, in-scope, and correct. `§19.8.5` is not engaged: no architectural, security, data-integrity, or tenant-isolation defect, no failing test, and no build failure was found.

**Path to PASS.** Author `IMP-REPORT-WP-21` per §7's `G1-M-01` remediation, optionally synchronize the `G1-L-04` governance-document staleness in the same pass, and re-dispatch Gate 1 to a further fresh-context reviewer uninvolved in the implementation and in this review. No implementation change is required or recommended by this record. The four Low findings are Gate 2 carry-forward inputs; none requires remediation before Gate 2, and `G1-L-01` is a candidate `§19.8` Technical Debt entry (Medium severity per the `§19.8.7` rubric).

**Gates 2–5 have not been run.** This record does not advance, prejudge, or substitute for any of them.

---

*End of CERT-WP-21. Gate 1 — Independent Certification: FAIL (one Medium, four Low, five Observations; zero Critical, zero High). Independently performed 2026-09-15 by a fresh-context reviewer with no involvement in the WP-21 / C-022 implementation or in any C-022 governance artifact. No implementation file, governance document, or register was modified. Nothing was staged, committed, or pushed.*
