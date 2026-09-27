# IMP-REPORT-WP-21 — Establish Commercial Account (C-022, BA-01)

**Work Package:** WP-21 — Customer & Account Management (C-022), BA-01 "Establish Commercial Account"
**Governing chain:** `CAP-001` line 76 → `COM-001` §4/§7 (`COM-001-001`/`-002`/`-003`/`-005`/`-030`…`-036`/`-060`/`-061`, LOCKED) → `PE-001-C022` v1.2 (Active) → `ROD-C022` (D1–D6) → `IRA-C022` (🟢 GREEN-leaning readiness) → `TDS-C022` (prepared, independently reviewed; `[C-3]`/`[C-4]`/`[C-5]` remediated) → `IRA-TDS-C022_Independent_Review.md` (PASS WITH CONDITIONS) → `ROD-C022-A` (D7 classification, D8 read/list) → `ADR-038` (classification conflict, Accepted — Option A) → `ADR-039` (CBOR registration preparation) → `ROD-C022-B` (D9 lifecycle-pattern, D10 BAR) → `ADR-040` (CBOR registration executed — `CAC-000001`) → `WP-21_C022_BA-01_Establish_Commercial_Account_Business_Activity_Charter.md` (§25a Implementation Authorization) → this report.
**Status:** **IMPLEMENTATION COMPLETE — CBOR REGISTERED (`ADR-040` — `CAC-000001`) — BAR REGISTRATION: DEFERRED BY REPOSITORY OWNER DECISION (`ROD-C022-B` D10, Option A) — `CLAUDE.md §19.7b` GATE 1: ❌ FAIL (2026-09-15; `CERT-WP-21`; one Medium finding `G1-M-01` — this report's own prior absence; zero Critical/High; four Low, non-blocking) — this report is `G1-M-01`'s own remediation; a fresh Gate 1 re-dispatch to a further independent reviewer remains a separate, subsequent action, not performed by this report.** ~~WP-21 / C-022 BA-01 is **NOT** certified, **NOT** closed, **NOT** release-ready as of this report.~~

*(Superseded 2026-09-16 at Gate 5 formal closure — accurate when written, and preserved rather than deleted per this repository's strikethrough-preserve discipline. The gate sequence has since completed in full: **Gate 1 attempt #2 ✅ PASS WITH OBSERVATIONS** (`CERT-WP-21A`, 2026-09-15, a further fresh-context reviewer; `G1-M-01` — this report's own prior absence — independently found RESOLVED; 0 Critical/High/Medium, 4 Low, 7 Observations); **Gate 2 ✅ PASS WITH NON-MATERIAL OBSERVATIONS** (`VV-AUDIT-WP-21`, 2026-09-16; 0 Critical/High/Medium, 4 Low, 8 Observations, 34/34 RTM rows PASS); **Gates 3–4 NOT TRIGGERED** (no defect required remediation); **Gate 5 ✅ PASS — CERTIFIED — CLOSED — RELEASE-READY** (`RRA-WP-21`, 2026-09-16, a further fresh-context reviewer uninvolved in the implementation or any prior gate; 0 Critical/High/Medium). **Current status: WP-21 / C-022 BA-01 is CERTIFIED, CLOSED, and RELEASE-READY.** Technical Debt arising: `TD-164` (Testing, Medium per `§19.8.7`). Note on §5.7 below: its disclosure that the 950/950 full-regression figure had **not** been independently reproduced at Gate 1 attempt #1 was correct and transparent when written; that figure has since been independently reproduced three further times — at Gate 1 attempt #2, at Gate 2, and at Gate 5 — each an exact match. §5.7's own historical wording is deliberately left untouched as the record of what was true at the time.)*

---

## 1. Repository Owner Implementation Authorization (recorded)

Implementation Authorization is recorded in `WP-21_C022_BA-01_Establish_Commercial_Account_Business_Activity_Charter.md §25a` ("Implementation Authorization (Recorded 2026-09-15)"), per direct Repository Owner instruction ("Begin implementation of WP-21 / C-022 / BA-01 — Establish Commercial Account"). Key terms, recorded verbatim in substance:

- Authorization is scoped exactly to the Charter's own approved content — §1–§20 — and no further: the single `POST /commercial-accounts` establish endpoint, the conceptual schema of §8 (including the explicit absence of a `classification` column), the `PREFIX-NNNNNN` Account Reference requirement (§7), the declared-but-unexercised hierarchy column (§13), and the `active`-only status write (§14).
- `ROD-C022-B` D9 (Option A — accept the collapsed single-call lifecycle realization) and D10 (Option A — defer BAR mechanism) are explicitly preserved, not reopened, by this authorization.
- Every Charter exclusion (§20) is explicitly preserved — no Customer, Customer–Account Relationship, reclassification/retirement/reactivation, merge/split/transfer, Subscription/Billing/Contract/Entitlement, CRM, Organization equivalence, tenant isolation, Identity/Person wiring, read/list, or invented lifecycle policy.
- The `§20.3` backend-only determination (Charter §21) is preserved and binding — no frontend/UI implementation is required or authorized.
- `ADR-038`'s Option A (no classification attribute) and `ADR-040`'s CBOR registration (`CAC-000001`) are both preserved, unaltered, and unreopened.
- The authorization does not itself authorize implementation to begin merely by being recorded — a separate implementation task performed the work this report documents.
- Backend-only is binding; do not create frontend/UI implementation for C-022 BA-01.
- Reuse existing repository mechanisms (`require_platform_admin`, the `BaseRepository` pattern, `record_audit`/`publish_event`, the reference-allocator shape) where appropriate, but preserve C-022's own ownership and semantics — do not copy C-021 business semantics merely because its implementation is a precedent.
- Change control: do not stage, commit, or push; do not begin independent Gate review within the same task; do not modify unrelated working-tree changes; preserve all pre-existing modifications; STOP rather than invent a workaround if a migration/model/route conflict requires a governance decision.

## 2. Authorized Scope (implemented)

Per `ROD-C022 §H` / D1/D5, as constrained by `ROD-C022-A` D7 (no classification)/D8 (establish-only) and `ROD-C022-B` D9 (collapsed single-call accepted)/D10 (BAR deferred), and the WP-21 charter §2: establish exactly one standalone **Authoritative Commercial Account** in `status = 'active'` — canonical identity (`id` uuid); **system-assigned Account Reference** (`COM-001-001` `PREFIX-NNNNNN`); minimum canonical `account_name`; hierarchy column declared but always `NULL`; produce the first Authoritative Commercial Account Context and the stable Account Reference. **Platform-global** — no `organization_id`; `require_platform_admin`; `/commercial-accounts` tenant-middleware-exempt (D2).

## 3. Implementation-Time STOP-and-Report Events

**None.** Unlike `WP-20` (where the BAR STOP-and-report was raised and resolved during the same implementation pass, `IMP-REPORT-WP-20 §3`/`§3.1`), for WP-21 both governance prerequisites were already fully resolved **before** Implementation Authorization was granted:

- **CBOR registration** was executed in a prior, dedicated governance pass — `ADR-040_Commercial_Account_Canonical_Business_Object_Registration.md` (Accepted), registering Business Object `CAC-000001`, adopting `ADR-039`'s prior eligibility/preparation analysis. `CBOR-INDEX.md §3` already carries the `CAC-000001` row.
- **BAR treatment** was already decided by explicit Repository Owner instruction — `ROD-C022-B` D10 (Option A, recorded 2026-09-15): no BAR registry, mechanism, or Business Activity Identifier is created; the `COM-001-060` execution-time obligation is deferred to a future enterprise-level BAR-mechanism decision, mirroring `ADR-037`'s disposition for C-021.
- **Schema-shape** — no STOP-and-report triggered. `TDS-C022 §6` performed the `CLAUDE.md §18`/`§19.4` schema-shape STOP-and-report at the conceptual level and surfaced no further Repository Owner decision beyond the ones already recorded in `ROD-C022-A`/`ROD-C022-B`. The physical migration is purely additive (one `op.create_table` + one `op.create_index` + one `UNIQUE` + one `CheckConstraint` + one self-referential `ForeignKeyConstraint`; **no `ALTER`**, **no PostgreSQL `SEQUENCE`**). No new architectural object was introduced during implementation itself, and no further STOP-and-report condition (new service, new cross-capability dependency, new authority mechanism, tenant-scoped semantics, excluded scope) arose while implementing.

Because both governance prerequisites were resolved ahead of time, implementation proceeded directly from `TDS-C022` without needing to raise or resolve any STOP-and-report of its own.

## 4. Explicit Exclusions (NOT implemented)

Per `ROD-C022 §H`, `ROD-C022-A` D7/D8, `ROD-C022-B` D9/D10, and the WP-21 charter §20: Customer establishment of any kind; the Customer–Account Relationship (`COM-001-034` requires an existing Customer Anchor *and* Commercial Account Anchor — not a first-slice concern); reclassification, retirement, or reactivation of a Commercial Account (no transition endpoint); merge, split, or transfer (`ERB-C022-04`); any Subscription (C-020), Billing (C-024), Contract (C-025), or Entitlement (C-023) functionality; any CRM/sales-pipeline/case-management/ERP-Customer-Master functionality; any Organization (C-004) equivalence or reference; tenant isolation of any kind; Identity (C-001/URA-001) or Person (C-006) reference wiring; read, list, or retrieval of any established Commercial Account (`ROD-C022-A` D8); any lifecycle policy beyond what `PE-001-C022`/`COM-001 §7` already canonically define; any Commercial Account `classification` attribute (`ADR-038` Option A); CBOR actual re-registration or a second Business Object Identifier; BAR mechanism creation or Business Activity Identifier assignment; any frontend/Enterprise Experience delivery for this Business Activity (Charter §21, backend-only, binding). **No speculative table, column, API, field, service, relationship, or governance mechanism was introduced to "prepare for" any of the above.**

## 5. Implementation Evidence

### 5.1 Files created

| File | Purpose |
|---|---|
| `Backend/Services/AuthService/models/c022_commercial_account.py` | `C022CommercialAccount` ORM model — 8 columns; one `CheckConstraint` (`status`); `UNIQUE`+index on `account_reference`; self-referential FK on `parent_account_id`; **no `organization_id`, no `classification`**; hierarchy declared-not-exercised. |
| `Backend/Services/AuthService/alembic/versions/2026_09_15_0900-f6a7b8c9d0e1_c022_commercial_account.py` | Migration. `revision='f6a7b8c9d0e1'`, `down_revision='e5f6a7b8c9d0'`. Purely additive; no `ALTER`; no `SEQUENCE`. |
| `Backend/Services/AuthService/repositories/c022_commercial_account_repository.py` | `C022CommercialAccountRepository(BaseRepository[...])` — `get_by_account_reference()` (`TDS-C022 §14`'s own minimum-method list; not wired to any route), `max_reference_sequence()` (fixed-offset `substr` allocator, PostgreSQL-portable from the outset — the WP-20 Gate 5 remediation pattern applied directly, not discovered the hard way a second time). |
| `Backend/Services/AuthService/schemas/commercial_account.py` | `EstablishCommercialAccountRequest` (`account_name` only; a `field_validator` rejects blank strings), `CommercialAccountResponse` (`from_attributes=True`). **No `classification` field anywhere in this module.** |
| `Backend/Services/AuthService/services/commercial_account_service.py` | `CommercialAccountService` — `establish` only (allocate-and-retry against the `UNIQUE` constraint, `record_audit` + `publish_event`, actor-id coercion). **No list/read/transition method.** |
| `Backend/Services/AuthService/routers/commercial_account.py` | 1 route — `POST ""` (201) — `Depends(require_platform_admin)`. **No other route.** |
| `Backend/Services/AuthService/tests/test_commercial_account.py` | 21 tests (see §5.7). |
| `architecture/05-Implementation/WP-21_C022_BA-01_Establish_Commercial_Account_Business_Activity_Charter.md` | BA-01 charter (prepared in a prior governance pass; not created by this implementation pass, listed here for completeness of the WP-21 document set). |
| `architecture/07-Decisions/ADR-040_Commercial_Account_Canonical_Business_Object_Registration.md` | CBOR registration of `CAC-000001` (prepared in a prior governance pass; not created by this implementation pass). |
| `architecture/06-Reviews/CERT-WP-21_Establish_Commercial_Account.md` | Gate 1 Independent Certification record — FAIL on `G1-M-01` (this report's own prior absence); produced by an independent reviewer, not by this implementation pass. |
| `architecture/05-Implementation/IMP-REPORT-WP-21_Establish_Commercial_Account.md` | This report. |

**No frontend file was created** — Charter §21's `CLAUDE.md §20.3` backend-only determination is binding for this Business Activity. Confirmed by direct search: no file under `source/frontend/src` references `commercial-account`, `c022`, or `C-022`.

### 5.2 Files modified

| File | Change |
|---|---|
| `Backend/Services/AuthService/models/__init__.py` | `from .c022_commercial_account import C022CommercialAccount` + `"C022CommercialAccount"` added to `__all__`. |
| `Backend/Services/AuthService/main.py` | `commercial_account` added to `from routers import …`; `app.include_router(commercial_account.router, prefix="/commercial-accounts", tags=["Customer & Account Management"])`. |
| `Backend/Services/AuthService/middleware/tenant.py` | `/commercial-accounts` + `/commercial-accounts/` added to the tenant-exemption path check, with a rationale comment citing `ROD-C022` D2 (the `/roles`/`/offerings` platform-global basis). |

**`WPR-001` and `CBOR-INDEX.md`** already carry their respective WP-21 (§2 row) and `CAC-000001` (§3 row) entries from the prior CBOR/WP-registration governance pass — **not modified again by this implementation pass.** **`WP-REG-001` was not modified**, consistent with the unbroken `WP-16`→`WP-20` precedent of registering only in `WPR-001` (recorded explicitly in the WP-21 Charter's own header note). **`MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md`** was updated in the prior governance pass, not this one.

### 5.3 Schema — implemented exactly per `TDS-C022 §6.1`

`c022_commercial_account`: `id` (uuid PK), `account_reference` (String(30), NOT NULL, UNIQUE, indexed — the `COM-001-001` `PREFIX-NNNNNN` identity), `account_name` (String(255), NOT NULL, no uniqueness invariant per `COM-001-033`), `status` (String(20), NOT NULL, default `'active'`, CHECK `IN ('active','suspended','retired')`), `parent_account_id` (uuid, NULLABLE, self-FK — `COM-001-033`'s hierarchy-position fact, declared, never written non-NULL by BA-01), `created_by_actor_id` (uuid, NOT NULL, **not a FK** — audit citation), `created_at` (NOT NULL), `updated_at` (NULLABLE, `onupdate`). **No `organization_id`. No `classification`.** Index: `ix_c022_commercial_account_account_reference` (unique).

### 5.4 Account Reference generation — acceptance properties, not a mandated mechanism

`CommercialAccountService.establish` calls `_next_account_reference()` → `f"ACCOUNT-{max_reference_sequence()+1:06d}"`. The `UNIQUE` constraint on `account_reference` is the concurrency backstop; on `IntegrityError` the transaction is rolled back and the allocation retried (up to 5 attempts, then a clean 409). **No PostgreSQL `SEQUENCE`, no new DB object.** `max_reference_sequence()` uses `func.substr(account_reference, _REFERENCE_SUFFIX_OFFSET)` with `_REFERENCE_SUFFIX_OFFSET = len("ACCOUNT") + 2 = 9` — a fixed, compile-time-known character offset, with no runtime search function (`instr()`/`strpos()`/`position()`) at all, applying the `WP-20` Gate 5 PostgreSQL-portability remediation directly at design time rather than discovering the defect class a second time. Verified: `^ACCOUNT-\d{6}$`, system-assigned (caller-supplied `account_reference`/`id`/`status`/`parent_account_id` — and a probed `classification` field — in the request body are all ignored, since none is part of the request schema), monotonic and contiguous across successive establishes, unique. The prefix `ACCOUNT` is a spelled-out word chosen to mirror the certified `OFFERING_REFERENCE_PREFIX = "OFFERING"` precedent; it is not lexically aligned with the `CAC-000001` CBOR identifier, which `TDS-C022 §7` permits (the prefix token is `[IMPLEMENTATION-TIME]`) and which is explicitly disclosed in the model's own module docstring.

### 5.5 Status semantics — only to the extent already authorized

`status` writes exactly one literal, `'active'`, at establish time (`services/commercial_account_service.py`); no other write path exists in the module. The closed set `{active, suspended, retired}` is declared in the schema for constitutional-model correctness (`COM-001-033`'s "current status" concern) and future-increment readiness — mirroring `c021_offering_definition.state`'s "declare the full closed set, write one value" pattern — not because BA-01 itself exercises suspend/retire. No transition endpoint, method, or schema field exists.

### 5.6 Platform-global security model (D2) — reused, not reinvented

Every route (there is exactly one) is `Depends(require_platform_admin)` — the identical, byte-for-byte unmodified dependency every previously certified platform-global route uses (`dependencies.py`; confirmed unchanged by `git diff -- dependencies.py` returning empty). `/commercial-accounts` is in `middleware/tenant.py`'s exemption list on the `/roles`/`/offerings` basis — no `X-Tenant-ID` required. `CLAUDE.md §21.4`'s Mandatory Tenant-Isolation Test Checklist is **structurally not applicable** (the data model carries no organization/tenant boundary, D2); the **substitute assurance** (`TDS-C022 §11`, Charter §12) is provided by the test suite: (a) non-`PLATFORM_ADMIN` denied 403; (b) `PLATFORM_ADMIN` succeeds; (c) an automated assertion (live table introspection **and** ORM metadata) that `c022_commercial_account` has no `organization_id` (or any `tenant`) column.

### 5.7 Test evidence

`Backend/Services/AuthService/tests/test_commercial_account.py` — **21 tests, 21/21 passing** (`JWT_SECRET_KEY` env set), independently reproduced twice in this workstream (once during implementation, once again by the independent Gate 1 reviewer, `CERT-WP-21 §6`): `test_establish_happy_path_persists_active`, `test_account_reference_format_is_prefix_nnnnnn`, `test_account_reference_is_system_assigned_caller_cannot_override`, `test_account_reference_is_monotonic_and_unique`, `test_blank_account_name_is_422`, `test_missing_account_name_is_422`, `test_no_classification_field_in_response_or_schema`, `test_orm_model_declares_no_classification_column`, `test_no_state_transition_endpoint_exists`, `test_no_read_or_list_endpoint_exists`, `test_non_platform_admin_is_forbidden`, `test_no_role_claim_is_forbidden`, `test_missing_authorization_header_is_400`, `test_malformed_authorization_header_is_400`, `test_commercial_accounts_needs_no_tenant_header`, `test_c022_table_has_no_organization_id_or_classification_column`, `test_orm_model_declares_no_organization_id`, `test_establish_emits_success_audit`, `test_end_to_end_establish_probe`, `test_max_reference_sequence_query_has_no_sqlite_only_function`, `test_max_reference_sequence_runtime_sql_has_no_sqlite_only_function`.

**Full `AuthService` regression: 950 passed, 0 failed**, 71 pre-existing deprecation warnings (unrelated — Starlette's `HTTP_422_UNPROCESSABLE_ENTITY` rename), executed once during this implementation pass (runtime 561.00s / 9m21s) against this exact, unchanged code. This figure has **not** been independently reproduced by the Gate 1 reviewer — `CERT-WP-21 §6` explicitly declines to re-run it, on the stated basis that the C-022 change set is additive and modifies no shared code path, and defers full-regression re-verification to Gate 2 (V&V). This report records the 950/950 figure as previously executed and unchanged since, not as independently re-confirmed at Gate 1.

### 5.8 Audit evidence

`test_establish_emits_success_audit` monkeypatch-spies `services.commercial_account_service.record_audit` and asserts a `SUCCESS` record with `action == "ESTABLISH_COMMERCIAL_ACCOUNT"`, `actor_id == <person_id>`, `metadata.status == "active"`, and `metadata.account_reference` matching `^ACCOUNT-\d{6}$`. `publish_event("COMMERCIAL_ACCOUNT_ESTABLISHED", …)` is emitted alongside, using the existing structured-log stand-in — not a real event bus, consistent with `IRA-C021 §16`'s disclosure for the identical mechanism class. No new audit or event mechanism was introduced.

### 5.9 Migration-head evidence

`alembic heads` → `f6a7b8c9d0e1 (head)` — **single, non-branching head**, independently confirmed a second time by the Gate 1 reviewer (`CERT-WP-21 §3.1` row 28, §5). Chain is linear from `e5f6a7b8c9d0` (WP-20). No branch, no merge. The migration was not executed against a live PostgreSQL server (no reachable server in this environment); verification was by direct read, ORM-vs-migration comparison, and `alembic heads`/`alembic branches` — the same disposition recorded for every prior `AuthService` Work Package (`CERT-WP-20 §4` observation 4; `CERT-WP-21 §5`).

### 5.10 Frontend evidence — not applicable (backend-only, binding)

Per the WP-21 Charter §21 `CLAUDE.md §20.3` determination (backend-only), **no frontend/UI implementation exists or was created for this Business Activity.** Confirmed by direct repository search (`source/frontend/src`) returning zero files referencing `commercial-account`, `c022`, or `C-022` — independently re-confirmed by the Gate 1 reviewer (`CERT-WP-21 §3.2`, Charter §21 row: "HONORED"). `CLAUDE.md §20.7`'s Enterprise Experience completion-gate extension correctly does not apply, per §20.3's own charter-exception clause.

## 6. TDS / Charter Traceability

| Requirement | Source | Where implemented / verified |
|---|---|---|
| Establish standalone Authoritative Commercial Account, `active` | `ROD-C022 §H`/D1/D5 | `service.establish` (`status="active"`, `parent_account_id=None`); `test_establish_happy_path_persists_active` |
| System-assigned `PREFIX-NNNNNN` Account Reference, monotonic, unique, concurrency-safe | `COM-001-001` (inherited by §7), `TDS-C022 §7` (post-`[C-3]`) | `_next_account_reference` + `UNIQUE` + retry; `test_account_reference_*` (3 tests) |
| Canonical name | `COM-001-033` | `account_name` String(255) NOT NULL; `test_blank_account_name_is_422`, `test_missing_account_name_is_422` |
| **No `classification` attribute** | `ADR-038` Option A, `ROD-C022-A` D7 | No column/field/attribute anywhere in the module set; `test_no_classification_field_in_response_or_schema`, `test_orm_model_declares_no_classification_column` |
| `status = active` only; no transition | `ROD-C022-A` D8, `TDS-C022 §9` | no transition method/endpoint; `test_no_state_transition_endpoint_exists` |
| Hierarchy declared, not exercised | `COM-001-033`, `TDS-C022 §10` | `parent_account_id` nullable self-FK, hard-coded `None` on write |
| **No read/list endpoint** | `ROD-C022-A` D8 | router contains exactly one route; `test_no_read_or_list_endpoint_exists` |
| Collapsed single-call lifecycle realization accepted | `ROD-C022-B` D9 (Option A) | exactly one public service method (`establish`); no Anchor/Intent/Proposed/Assessment construct anywhere |
| Platform-global, no `organization_id`, `require_platform_admin` | `ROD-C022` D2 | no column; `Depends(require_platform_admin)`; `/commercial-accounts` middleware-exempt; `test_c022_table_has_no_organization_id_or_classification_column`, `test_orm_model_declares_no_organization_id`, `test_commercial_accounts_needs_no_tenant_header`, `test_non_platform_admin_is_forbidden` |
| Service host = `AuthService` | `ROD-C022` D3 | all backend files under `Backend/Services/AuthService`; `main.py` wiring |
| Migration `down_revision = e5f6a7b8c9d0`, additive, no `SEQUENCE` | `TDS-C022 §6.1` | `2026_09_15_0900-f6a7b8c9d0e1_…`; `alembic heads` single head |
| Audit / Evidence | `TDS-C022 §17` | `record_audit` + `publish_event` on establish; `test_establish_emits_success_audit` |
| CBOR registration | `COM-001-005`/`-061`, `IRA-C022 §11` | `ADR-040` (`CAC-000001`) + `CBOR-INDEX.md §3` row |
| BAR treatment | `COM-001-060` | `ROD-C022-B` D10 (Option A) — deferred, no mechanism/identifier created |
| `CLAUDE.md §20.3` backend-only | Charter §21 | no frontend file exists; `§20.7` extension inapplicable |
| Purpose-built end-to-end runtime probe (`CLAUDE.md §19.7b` method note) | Charter §19 | `test_end_to_end_establish_probe` |
| PostgreSQL-portable allocator (WP-20 Gate 5 lesson applied) | Repository precedent | `test_max_reference_sequence_*` (2 tests) |

## 7. Deferred Scope (disclosed, not implemented — unchanged from `ROD-C022`/`ROD-C022-A`/`ROD-C022-B`)

Customer establishment and the Customer–Account Relationship (`COM-001-034`); reclassification, retirement, and reactivation and their approval authority; merge/split/transfer (`ERB-C022-04`); read/list/retrieval of any established Commercial Account and the `COM-001-036` reference-distribution consequence this defers (`ROD-C022-A` D8's own accepted consequence: C-020 remains blocked from consuming a genuine, retrievable Commercial Account reference until a later C-022 Business Activity exists); a BAR mechanism (`ROD-C022-B` D10); the `COM-001-033`↔`PE-001-C022` classification conflict `ADR-038` identified but deliberately left unresolved as a separate future architecture-governance item; the lifecycle-pattern realization question `TDS-C022 §15.1` disclosed and `ROD-C022-B` D9 settled for BA-01 specifically (not a general ruling for every future C-022 Business Activity).

## 8. Known Limitations

Recorded as Gate 1 (`CERT-WP-21`) Low, non-blocking findings — explicitly **not** implementation defects, distinguished here from any correctness issue:

- **`G1-L-01`** — the allocate-and-retry concurrency backstop (`services/commercial_account_service.py`, `except IntegrityError` / the `for…else` 409 path) is not exercised by any test; no test pre-seeds a colliding `account_reference`. The design is sanctioned by `TDS-C022 §18` and mirrors the certified `OfferingDefinitionService.establish` pattern exactly, whose identical gap was carried through all five WP-20 gates without remediation. Candidate `CLAUDE.md §19.8` Technical Debt entry, Medium severity per §19.8.7 (internal robustness/completeness — no Business Intent or security boundary at stake).
- **`G1-L-02`** — the "persists" tests (`test_establish_happy_path_persists_active`, `test_end_to_end_establish_probe`) verify through the same uncommitted session the request used (`tests/conftest.py`'s `client` fixture overrides `get_session` with a non-committing generator), so they observe post-`flush`, in-transaction state rather than a true committed round-trip on a separate connection. Production `get_session` (`models/database.py`) does commit correctly. This is a pre-existing, repository-wide shared-harness property, unmodified by this Work Package and identical for every previously certified Work Package — not specific to C-022.
- **`G1-L-03`** — the test harness does not enable `PRAGMA foreign_keys=ON` for SQLite, so `fk_c022_commercial_account_parent_account_id` is unenforced in tests. No functional impact for BA-01, since `parent_account_id` is hard-coded `None` on every write and no route ever sets it. Identical to `CERT-WP-20 §4` observation 5.
- **`G1-L-04`** — the `WPR-001` WP-21 row and a `CBOR-INDEX.md` sentence, both written before implementation existed, now read as stale ("IMPLEMENTATION NOT YET STARTED", "no … table, model, migration, or API exists as of this entry"). `CLAUDE.md §19.7b` explicitly assigns this class of governance-documentation staleness to Gate 5 (Release Readiness Audit); it is **not** corrected by this report, per this report's own change-control instruction that governance-registry synchronization belongs to a later gate/pass, not this documentation remediation.

None of the above is a `CLAUDE.md §19.8.5`-class defect (no architectural, security, data-integrity, or tenant-isolation defect; no failing test; no build failure).

## 9. Explicit Confirmations

- ✅ Implementation is strictly within `ROD-C022 §H`, `ROD-C022-A` D7/D8, `ROD-C022-B` D9/D10, `ADR-038` Option A, and the WP-21 Charter §1–§20/§25a. No other C-022 Business Activity implemented.
- ✅ Host = `AuthService` (D3). No new service.
- ✅ Account Reference satisfied as a set of acceptance properties (system-assigned, monotonic, unique, concurrency-safe, `PREFIX-NNNNNN`); **no PostgreSQL `SEQUENCE`**; no new architectural/database object.
- ✅ **No `classification` attribute** anywhere — model, schema, migration, response, or request (`ADR-038` Option A).
- ✅ **No read/list/update/delete endpoint** exists (`ROD-C022-A` D8).
- ✅ **No** Customer, Customer–Account Relationship, Organization equivalence, Identity/Person wiring, Subscription, Billing, Contract, Entitlement, CRM behavior, reclassify, retire/reactivate, or merge/split/transfer entered the schema, API, service, or any file.
- ✅ D9 (`ROD-C022-B`, Option A) honored — exactly one public service method (`establish`); no separately-observable Anchor/Intent/Proposed/Assessment stage introduced.
- ✅ D10 (`ROD-C022-B`, Option A) honored — no BAR registry, mechanism, or Business Activity Identifier created anywhere.
- ✅ CBOR registered (`ADR-040` — `CAC-000001`); `CBOR-INDEX.md §3` row present, scoped strictly to the Commercial Account Business Object; not re-registered or altered by this implementation pass.
- ✅ Charter §21 `CLAUDE.md §20.3` backend-only determination honored — **no frontend/UI file created**.
- ✅ Migration additive; single non-branching Alembic head `f6a7b8c9d0e1`; `down_revision = e5f6a7b8c9d0`.
- ✅ Targeted C-022 suite 21/21 (reproduced twice — implementation pass and independent Gate 1 reviewer). Full `AuthService` regression 950/950 (implementation pass; not re-run at Gate 1, per `CERT-WP-21 §6`'s own stated, disclosed basis).
- ✅ The pre-existing modified/untracked working-tree content unrelated to WP-21 (the C-021/WP-20 implementation and frontend, the `ROD-C040-*`/`ROD-Meta-Governance-*` set, `ADR-027`…`ADR-035`, and others) was **not** touched by this implementation pass. No LOCKED constitutional document was modified.
- ✅ **Nothing was staged, committed, or pushed.** `git add -A`/`git add .` were not used.

## 10. Gate Readiness

WP-21 / BA-01 has already been submitted for, and has already completed, one `CLAUDE.md §19.7b` **Gate 1 (Independent Certification)** attempt — a fresh-context reviewer with no involvement in the implementation, recorded in `CERT-WP-21_Establish_Commercial_Account.md` (2026-09-15): **❌ FAIL**, on exactly one Medium finding, `G1-M-01` — this report's own prior absence. Zero Critical/High findings; four Low, non-blocking findings; the implementation code itself was found conformant on every technical dimension examined (§7 below records `CERT-WP-21`'s own result in full).

**This report is `G1-M-01`'s own required remediation.** Per `CERT-WP-21 §9`'s own stated path to PASS, a **fresh** Gate 1 re-dispatch — to a further independent reviewer uninvolved in the implementation and in the original `CERT-WP-21` review — remains a separate, subsequent action, **not performed by this report.** WP-21 / C-022 BA-01 is **NOT** certified, **NOT** closed, **NOT** release-ready as of this report. Gate 2 (V&V Audit), Gates 3–4 (if triggered), and Gate 5 (Release Readiness Audit) all remain unstarted.

## 11. Change Control

**Baseline at the start of this documentation-remediation pass:** `HEAD = 8323bf3976818ff463cf67e891bd2a0a953777fd`. The C-022 implementation files (§5.1/§5.2) and `CERT-WP-21` already existed, untouched by this pass. The large pre-existing modified/untracked batch (13 pre-existing modified tracked files; the `ROD-C040-*`/`ROD-Meta-Governance-*`/`ADR-027`…`035` set; the C-021/WP-20 implementation and frontend; `Master_Platform_Capability_Delivery_Map.xlsx`; `Sarika_consent.png`; and others) — **not touched** by this pass.

**File created by this pass:** exactly one — `architecture/05-Implementation/IMP-REPORT-WP-21_Establish_Commercial_Account.md` (this report).

**Not modified by this pass:** every implementation file (§5.1/§5.2 — all byte-untouched); the WP-21 Charter; `TDS-C022`; `ROD-C022`/`ROD-C022-A`/`ROD-C022-B`; `ADR-038`/`ADR-039`/`ADR-040`; `CBOR-INDEX.md`; `WPR-001`; `WP-REG-001`; `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md`; **`CERT-WP-21_Establish_Commercial_Account.md`** (the failed Gate 1 record remains intact, historical evidence, per direct instruction); any LOCKED constitutional document; any unrelated ADR, migration, test, or certified WP artifact; any pre-existing modified or untracked file.

**Nothing was staged, committed, or pushed.**

---

## 12. Gate 1 — Independent Certification: Result (2026-09-15) — ❌ FAIL

**Reviewer independence.** A fresh-context reviewer with **no** involvement in the WP-21/C-022 implementation, `ROD-C022`, `ROD-C022-A`, `ROD-C022-B`, `IRA-C022`, `TDS-C022`, the WP-21 Charter, `ADR-038`, `ADR-039`, or `ADR-040`. The reviewer re-derived every material claim from actual repository source, an independently executed targeted suite (**21/21**), `alembic heads`/`alembic branches` output, and direct `git` inspection. Full record: `architecture/06-Reviews/CERT-WP-21_Establish_Commercial_Account.md`.

**Verdict: ❌ FAIL.** Zero Critical, zero High findings. **One Medium finding, `G1-M-01` — blocking**: this Implementation Report did not exist at the time Gate 1 was dispatched, leaving the Implementation half of `CLAUDE.md §19.7`'s Business Activity Completion Gate unsatisfied. Four Low, non-blocking findings (`G1-L-01` through `G1-L-04`, recorded at §8 above). Five non-blocking observations.

**What the FAIL was not.** `CERT-WP-21`'s own decision (§9) states explicitly: *"It is not a defect in the delivered code. On every technical dimension examined … the implementation was found conformant, in-scope, and correct."* No `CLAUDE.md §19.8.5`-class defect (architectural, security, data-integrity, tenant-isolation, failing test, or build failure) was found.

**Remediation performed by this report.** This document is `G1-M-01`'s required remediation — authoring the missing `IMP-REPORT-WP-21`, per `CERT-WP-21 §7`'s own recorded remediation instruction: *"Author `architecture/05-Implementation/IMP-REPORT-WP-21_Establish_Commercial_Account.md` following the `IMP-REPORT-WP-20` structure, recording the BA-01 implementation, the governing-document basis, the evidence, the test results, the disclosed observations, and an Implementation Status of 'IMPLEMENTATION COMPLETE'. Then re-dispatch Gate 1 to a further fresh-context reviewer. No implementation file requires any change."* No implementation file was changed by this remediation, consistent with that instruction.

**Not performed by this report.** A fresh Gate 1 re-dispatch, per `CERT-WP-21`'s own stated path to PASS, is a separate, subsequent action. `G1-L-04`'s `WPR-001`/`CBOR-INDEX.md` staleness was explicitly left uncorrected here, per direct instruction, as belonging to a later gate/documentation-synchronization pass. `CERT-WP-21` itself was not modified — it remains intact as the historical record of the first Gate 1 attempt.

---

*End of IMP-REPORT-WP-21. Implementation Status: IMPLEMENTATION COMPLETE. Gate 1 (first attempt): FAIL on `G1-M-01` (this report's own prior absence), now remediated by this report's own creation. A fresh Gate 1 re-dispatch remains a separate, subsequent, explicitly-authorized action. WP-21 / C-022 BA-01 is NOT certified, NOT closed, NOT release-ready. Nothing staged, committed, or pushed.*
