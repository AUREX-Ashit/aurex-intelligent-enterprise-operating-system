# VV-AUDIT-WP-18 — Independent Verification & Validation Audit: Bind and Resolve Approval Authority (C-003)

**Work Package:** WP-18 — C-003 (Role & Permission Management) — Bind and Resolve Approval Authority (repository-wide Approval Authority runtime-binding infrastructure)
**Business Activity:** BA — Bind and Resolve Approval Authority (working title, per the charter §1 disclosure — no closer canonical term exists in `URA-001` or repository precedent)
**State audited:** working tree at time of review — commit `e86192f95a1ef3534513f9fcee9418bbecb21baf` (`main`) plus the **same uncommitted WP-18 change set `CERT-WP-18_Approval_Authority_Runtime_Binding.md` was certified against; no new commit since Gate 1.** The working tree simultaneously carries uncommitted WP-16 (C-040) work certified/audited separately (`CERT-WP-16`, `VV-AUDIT-WP-16`, `RRA-WP-16`); this audit isolates and audits the WP-18 change set only. `git status --short` / `git diff --check` / `git diff --cached --stat` reproduced in full at §12, before and after.
**Reviewer:** Genuinely independent, fresh-context reviewer. No access to any prior session's conversation; no prior involvement in WP-18's implementation, in the drafting of `TDS-018` / the WP-18 charter / `IMP-REPORT-WP-18`, in `TDS-018 §28`/`§30`/`§31`'s prior independent reviews, in the prior Gate 1 attempt that returned NOT CERTIFIED for "M-1", or in `CERT-WP-18`'s own drafting. `CERT-WP-18` was read as a **map of what Gate 1 checked, not as a source of trusted conclusions** — every material claim below was independently re-derived from primary sources: actual files opened, actual commands run, purpose-built runtime probes written and executed.
**Gate:** 2 of 5 (`CLAUDE.md §19.7b`) — a broader, more exhaustive mandate than Gate 1: from-scratch runtime probes per defect class (none adapted from the existing test suite), a negative control reproducing the pre-fix defect, the harness/fixture production-parity checklist, the `CLAUDE.md §21.4` checklist re-applied independently, and an adversarial re-examination of Gate 1's four observations.
**Determination:** **PASS WITH OBSERVATIONS.** No `CLAUDE.md §19.8.5`-class defect found — no architectural, security, data-integrity, or tenant-isolation defect; no false `ALLOW`; no failing test; no build failure; no migration failure; no design non-conformance to `TDS-018 §29.2` that changes behaviour; no out-of-scope implementation; no evidence Gate 1 certification was materially incorrect. Five non-material observations are recorded (four carried forward from Gate 1 and independently re-examined; one new Low-severity defense-in-depth hardening observation, `VV-O5`, which does **not** require correction and does **not** trigger Gates 3–4). WP-18 may proceed to Gate 5 (Release Readiness Audit) in this reviewer's judgment.

---

## 1. Scope and Method

Re-reading source and re-running the existing suite were treated as **necessary but insufficient**, per `CLAUDE.md §19.7b`'s method requirement. In addition:

**Primary documents read in full:** `TDS-018_C003_Approval_Authority_Runtime_Binding_Technical_Design.md` (all 409 lines — §§1–31, including §29.2–§29.6 corrected resolver algorithm, §29 amendment, §30 amendment review, §31 M-1 reconciliation, both Change Control blocks); `WP-18_C003_BA-XX_Approval_Authority_Runtime_Binding_Business_Activity_Charter.md` (full); `IMP-REPORT-WP-18_Approval_Authority_Runtime_Binding.md` (full); `CERT-WP-18_Approval_Authority_Runtime_Binding.md` (full — map only); `WPR-001_Work_Package_Roadmap.md` (WP-18 row + diff + WP-13 precedent); `CLAUDE.md §16`/`§17`/`§18`/`§19` (all subsections, incl. `§19.7`/`§19.7b`/`§19.8.5`/`§19.8.7`)/`§20`/`§21` (`§21.3`/`§21.4`); `TECH-DEBT.md` entries `TD-028`/`TD-096`/`TD-159`/`TD-160` (table rows + detailed entries).

**Every WP-18 implementation file read in full:** `models/membership_approval_authority.py`; `alembic/versions/2026_08_29_1100-f9a3c7e1b5d2_membership_approval_authority.py`; `repositories/membership_approval_authority_repository.py`; `services/membership_approval_authority_service.py`; `services/approval_authority_resolver.py`; `tests/test_approval_authority_resolver.py` (all 22 tests); `tests/test_membership_approval_authority_service.py` (all 8 tests).

**Every modified tracked file inspected via `git diff`:** `dependencies.py`, `models/__init__.py`, `repositories/approval_authority_repository.py`, `middleware/tenant.py`.

**Supporting files read:** `models/approval_authority.py` (`ApprovalStrategy`/`VersionStatus` enums, `majority_threshold_pct`, four `CheckConstraint`s), `models/membership.py` (`membership_status` default `ACTIVE`, `effective_from`/`effective_to`), `middleware/tenant.py` (`get_current_tenant` / `tenant_context` ContextVar derivation), `Backend/Runtime/AuthorizationEngine/authorization/tier_resolvers.py` (`ApprovalAuthorityResolver` stub), `observability.py` (`record_audit`/`publish_event` bodies), `tests/conftest.py` (SQLite/StaticPool harness).

**Commands run (venv `./venv/Scripts/python.exe`, `JWT_SECRET_KEY` set in env, from `Backend/Services/AuthService`):**

| Command | Purpose |
|---|---|
| `git rev-parse HEAD` / `git status --short` / `git diff --check` / `git diff --cached --stat` (repo root, before + after) | Change control |
| `python -m alembic heads` | Single-head verification |
| `python -m alembic history` | Linear-chain verification |
| `DATABASE_URL=sqlite… python -m alembic upgrade b2c3d4e5f6a7:f9a3c7e1b5d2 --sql` | Offline SQLite DDL for the WP-18 migration in isolation |
| `DATABASE_URL=postgresql… python -m alembic upgrade b2c3d4e5f6a7:f9a3c7e1b5d2 --sql` | Offline **PostgreSQL** DDL for the WP-18 migration |
| `DATABASE_URL=postgresql… python -m alembic downgrade f9a3c7e1b5d2:b2c3d4e5f6a7 --sql` | Offline PostgreSQL DDL for `downgrade()` |
| `python -m pytest tests/test_approval_authority_resolver.py tests/test_membership_approval_authority_service.py -v` | Dedicated-suite re-run |
| `python -m pytest -q` | Full AuthService regression re-run |
| `grep -rn "MembershipApprovalAuthority(\|\.bind(\|binding_repo.create\|MembershipApprovalAuthorityService" --include=*.py` | Enumerate every binding-row creation path in the codebase |
| `grep -rniE "license\|entitlement\|subscription\|billing\|c-023\|group_registry\|group_membership\|group_approval"` over the 7 WP-18 files | Scope containment |

**From-scratch runtime probes** (two throwaway scripts placed temporarily in `Backend/Services/AuthService/` for relative imports, run against a throwaway `sqlite+aiosqlite:///:memory:` engine mirroring `conftest.py`'s construction, **deleted immediately after use** — not repository deliverables, absent from the final `git status`, §12). **None adapted from `tests/test_approval_authority_resolver.py` or `tests/test_membership_approval_authority_service.py`** — all seed their own Organization/Person/Role/Membership graphs and assert against resolver return values, DB row counts, raised exceptions, and captured audit kwargs. All ORM inserts used real `uuid.UUID` objects, avoiding the raw-SQL dashed-string-vs-`CHAR(32)` pitfall `VV-AUDIT-WP-16 §3` documented. Probes P1–P10 (script 1) and the TD-028 trace + audit-content deep check (script 2) are written up at §4.

**Environment limitation (stated, not worked around):** no PostgreSQL, no Docker, and no local PG cluster are available in this environment (`which psql` / `docker ps` / `pg_lsclusters` all negative). Runtime probes therefore ran on SQLite/StaticPool only; PostgreSQL parity was verified at the **DDL-generation level** (`alembic … --sql` for the `postgresql+asyncpg` dialect) but **not** by executing against a live PostgreSQL engine. Residual confidence limit recorded at §6 and §10.

---

## 2. Verification — Implementation vs. `TDS-018 §29.2`–`§29.6` / Charter / Canonical Schema

| # | Requirement (authoritative source) | Independently verified against | Result |
|---|---|---|---|
| V1 | Resolver step order **exactly** `TDS-018 §29.2`'s 8 steps, no step skippable/reorderable | `services/approval_authority_resolver.py::resolve_approval_authority()` lines 60–169, traced line-by-line | ✓ Match — step 1 resolve authority; step 2 config validation; step 3 strategy gate; step 4 org mismatch; step 5 eligible binding; step 6 membership validity; steps 7–8 `AUTHORIZED` |
| V2 | Step 1 distinguishes `NO_AUTHORITY_CONFIGURED` (no row) from `INACTIVE_AUTHORITY` (row exists, non-`ACTIVE`) | `get_active_by_organization_and_name` → if `None`, `get_any_by_organization_and_name` → non-`ACTIVE` ⇒ `INACTIVE_AUTHORITY` else `NO_AUTHORITY_CONFIGURED` | ✓ Match; `get_active_…` filters `status == VersionStatus.ACTIVE.value` |
| V3 | Step 2 (config validation) evaluated **before** step 3 and **before any caller-specific step** — cannot be bypassed by a qualifying binding (`§29.2` step 2 ordering fix) | Code order + in-code comment citing `§29.2` step 2; **Probe P2** (malformed `MAJORITY` + mismatched org + nonexistent membership ⇒ `INVALID_CONFIGURATION`) | ✓ Empirically confirmed — the caller-specific inputs never reached |
| V4 | Step 3 (`approval_strategy != ANY_ONE` ⇒ `UNSUPPORTED_STRATEGY`) evaluated **before any caller-specific step**; `ALL`/`MAJORITY`/`SEQUENTIAL` never counted/simulated/approximated | Full-module read (no counting/quorum/sequencing logic anywhere); **Probe P1** (MAJORITY + mismatched org + nonexistent membership ⇒ `UNSUPPORTED_STRATEGY`, not `INVALID_SCOPE`/`NO_ELIGIBLE_ACTOR`); **Probe P3** (fully-qualifying caller + MAJORITY/ALL/SEQUENTIAL ⇒ `UNSUPPORTED_STRATEGY`, never `AUTHORIZED`) | ✓ Empirically confirmed for all three strategies |
| V5 | Step 4 organization mismatch ⇒ `INVALID_SCOPE`; `caller_organization_id is None` also ⇒ `INVALID_SCOPE` | Code lines 122–124; **Probe P5** (caller Org A → target Org B ⇒ `INVALID_SCOPE`) | ✓ Match |
| V6 | Step 5 missing/ineffective binding ⇒ `NO_ELIGIBLE_ACTOR`; `caller_membership_id is None` also ⇒ `NO_ELIGIBLE_ACTOR`; effective window = `effective_from <= now AND (effective_to IS NULL OR effective_to > now)` | Code lines 126–131; `get_effective_binding` query lines 51–64; existing tests `test_binding_not_yet_effective_denies` / `test_binding_already_expired_denies` re-run | ✓ Match |
| V7 | Step 6 membership validity: `membership_status == "ACTIVE"` AND effective window covers now; otherwise `INACTIVE_MEMBERSHIP` | Code lines 133–143 | ✓ Match — see `VV-O5` (§13) for a defense-in-depth note on what step 6 does **not** additionally re-check |
| V8 | Steps 7–8: `AUTHORIZED` reached only when steps 1–6 all pass; emits `record_audit(SUCCESS)` + `publish_event("APPROVAL_AUTHORITY_RESOLVED")` | Code lines 145–169; **Probe P3/P10** | ✓ Match |
| V9 | Reason taxonomy = `TDS-018 §29.4`'s exactly 8 labels, no more, no fewer | `ApprovalAuthorityResolution(str, Enum)` lines 36–54 | ✓ Exactly: `NO_AUTHORITY_CONFIGURED`, `INACTIVE_AUTHORITY`, `INVALID_CONFIGURATION`, `UNSUPPORTED_STRATEGY`, `INVALID_SCOPE`, `NO_ELIGIBLE_ACTOR`, `INACTIVE_MEMBERSHIP`, `AUTHORIZED` |
| V10 | Fail-closed (`§29.3`): every non-`AUTHORIZED` branch denies; no branch simulates/infers/defaults; no `PLATFORM_ADMIN`/`AUREX_ADMIN`/Role/Group fallback | Full-module read (`_deny` on every branch; only admin strings are in the docstring documenting deliberate non-bypass); **Probe P3–P7**, existing `test_admin_role_does_not_bypass…[PLATFORM_ADMIN\|AUREX_ADMIN]`, `test_missing_claims_denies_closed` | ✓ Match |
| V11 | `enforce_approval_authority` / `require_approval_authority` (Option B, `TDS-018 §12`): direct claims comparison + one live DB resolution; no `AuthorizationContext`, no Engine; **no admin bypass**; `target_organization_id` from `X-Tenant-ID` via `get_current_tenant`, independent of caller JWT claims | `git diff` of `dependencies.py` (purely appended); `middleware/tenant.py::get_current_tenant` reads `tenant_context` ContextVar set by `TenantMiddleware` from the `X-Tenant-ID` header | ✓ Match — step-4 comparison is genuinely meaningful (target ≠ a self-comparison of one claim) |
| V12 | `membership_approval_authority` model = canonical column set (`Master_Technical_Architecture.md` 1318–1329), composite PK `(membership_id, approval_authority_id, effective_from)`, nullable `effective_to`, no `organization_id` column | `models/membership_approval_authority.py` full read; migration `--sql` output (both dialects) | ✓ Match, column-by-column |
| V13 | One disclosed additive hardening: partial unique index `ux_membership_approval_authority_active` on `(membership_id, approval_authority_id) WHERE effective_to IS NULL` (`TDS-018 §19`, mirrors `authority_holders`) | Model `__table_args__` (cross-dialect `postgresql_where` + `sqlite_where`); migration `op.create_index`; **Probe P8** (two open rows for one pair ⇒ `IntegrityError`); **Probe P9** negative control (re-open after close ⇒ allowed) | ✓ Present, cross-dialect, and empirically enforced under SQLite |
| V14 | `bind()` (`TDS-018 §5`–§7): Membership existence (404) → Approval Authority existence (404) → cross-Organization rejection (409) → duplicate open-binding rejection (409) → create + audit + event | `services/membership_approval_authority_service.py::bind()` full read; existing service tests re-run | ✓ Match |
| V15 | `close()` (`TDS-018 §9`): locate open binding (404 if none) → set `effective_to = now` → audit + event; **never a hard delete** | `close()` full read; existing `test_close_deactivates_binding_without_deleting` re-run (asserts row still present) | ✓ Match |
| V16 | Migration purely additive: one `CREATE TABLE` + one `CREATE INDEX`; no `ALTER` to `approval_authorities`/`memberships`; `downgrade()` = clean drop index + drop table | Migration full read; `--sql` output both dialects | ✓ Match |
| V17 | Modified tracked files purely additive | `git diff` of `dependencies.py` (appended `enforce_approval_authority`/`require_approval_authority` only), `models/__init__.py` (added import + `__all__` entry), `repositories/approval_authority_repository.py` (added `select` import, extended `VersionStatus` import, two new read-only methods; `get_active_dependents`/`has_active_dependents` byte-for-byte unchanged) | ✓ No existing symbol altered |

**Note on `middleware/tenant.py`:** its `git diff` (new `/auth/authority-*` and `/tenants` exemptions, plus `require_authority_holder`/`require_ai001_holder`/`require_ai002_holder` in the `dependencies.py` diff) is **pre-existing WP-16 / C-040 (TDS-017) work, not WP-18** — `IMP-REPORT-WP-18 §2` lists only the two WP-18 `dependencies.py` functions, both appended after existing content. Independently confirmed by diff inspection.

**Verification conclusion:** the implementation faithfully realizes `TDS-018 §29.2`–`§29.6`, the charter, and the canonical schema, with no undisclosed deviation and no behaviour-changing discrepancy. This independently re-derives — it does not merely repeat — Gate 1's identical conclusion.

---

## 3. Validation — From-Scratch Runtime Probes (per defect class, none from the existing suite)

| Probe | Method | Result |
|---|---|---|
| **P1 — step-order: strategy gate precedes caller steps** | `MAJORITY` authority; call resolver with a **mismatched** `caller_organization_id` (random UUID) **and** a nonexistent `caller_membership_id`. If a caller step fired first ⇒ `INVALID_SCOPE` or `NO_ELIGIBLE_ACTOR`. | **`UNSUPPORTED_STRATEGY`** — step 3 fires before steps 4/5. **PASS** |
| **P2 — step-order: config gate precedes strategy gate + caller steps** | `MAJORITY` with `majority_threshold_pct = None`; same mismatched org + nonexistent membership. | **`INVALID_CONFIGURATION`** — step 2 fires before step 3 and before caller steps. **PASS** |
| **P3 — false-`ALLOW`: fully-qualifying caller vs. non-`ANY_ONE`** | For each of `MAJORITY`(thr 60) / `ALL` / `SEQUENTIAL`: same-Org authority + genuine currently-effective same-Org binding + `ACTIVE` membership + matching `caller_organization_id`. A single qualifying binding present in every case. | **`UNSUPPORTED_STRATEGY`** in all three; **never `AUTHORIZED`**. **PASS** |
| **P4 — negative control (reproduces the pre-fix defect)** | Reconstructed the original `TDS-018 §10` algorithm (no config gate, no strategy gate) as a standalone function; ran P3's `MAJORITY` scenario against it. | **`AUTHORIZED`** — the pre-fix algorithm **does** false-`ALLOW` a `MAJORITY` row with one qualifying binding. Confirms P1–P3 exercise a real defect class, and that `§29.2`'s step 3 is what eliminates it. **PASS** |
| **P5 — tenant isolation: caller Org A cannot resolve Org B's authority** | Two independent Organizations, no shared row; `ANY_ONE` authority + binding in Org B; caller genuinely in Org A (`caller_organization_id = OrgA`) targets Org B. | **`INVALID_SCOPE`** at step 4, before any binding lookup that could infer Org B data. **PASS** |
| **P6 — foreign membership id, no binding** | `target = OrgB`, `caller_organization_id = OrgB`, `caller_membership_id` = an Org-A membership id; no binding row. | **`NO_ELIGIBLE_ACTOR`** — no crash, no `AUTHORIZED`. **PASS** |
| **P7 — defense-in-depth: directly-inserted cross-Organization binding row** | Simulates a `membership_approval_authority` row that bypassed the `bind()` guard (direct DB insert): Org-A `ACTIVE` membership ↔ Org-B authority. Call with `target = OrgB`, `caller_organization_id = OrgB` (i.e. claims internally inconsistent with the membership's real Org), `caller_membership_id` = the Org-A membership. | **`AUTHORIZED`.** The resolver does **not** independently re-verify `membership.organization_id == target_organization_id` at step 6 — it relies on step-4 (claim vs. target) + the bind-time guard + JWT claim internal consistency. **See `VV-O5` (§13): non-material** — no WP-18 code path can create such a row (§3.1), conforms to `TDS-018 §29.2` as written, and the JWT is the trust anchor for claim consistency. Recorded as a Low hardening observation, **not a defect, Gates 3–4 not triggered.** |
| **P8 — partial unique index actually blocks two open bindings** | Insert open binding row 1 (default `effective_from`), then open binding row 2 for the same pair with a later `effective_from` (distinct composite PK, both `effective_to IS NULL`). | **`IntegrityError`** — the partial unique index, not the composite PK, blocks it (PKs differ). **PASS** |
| **P9 — negative control for P8** | Close row 1 (`effective_to = now`), then insert a new open row for the same pair. | **Allowed** — the partial index is correctly scoped to open rows only. **PASS** |
| **P10 — audit: every branch audited; no secret material** | Monkeypatch `record_audit`; drive one DENY (`NO_AUTHORITY_CONFIGURED`) and one `AUTHORIZED`. Inspect captured kwargs. | DENY ⇒ one `record_audit(status=DENIED, metadata={"reason": "NO_AUTHORITY_CONFIGURED"})`; `AUTHORIZED` ⇒ one `record_audit(status=SUCCESS, …)`. No `bearer `, `jwt_secret`, `secret_key`, `password`, or raw `authorization` string in any metadata. **PASS** |
| **P-TD028 — retired authority + open binding + valid membership** | `status="RETIRED"` authority + genuine open binding + `ACTIVE` membership + matching org. | **`INACTIVE_AUTHORITY`** (DENY) — fail-closed. `get_active_dependents()` still returns `[]` / `has_active_dependents()` still `False` (WP-18 deliberately did not extend them), but the resolver's step 1 covers the risk. **PASS** — see §9 (TD-028). |
| **P-audit-content — full audit kwargs inspection** | Capture full kwargs for a DENY and an `AUTHORIZED` with `actor_id="person-123"`. | DENY metadata = `{"reason": "NO_AUTHORITY_CONFIGURED"}`; `AUTHORIZED` metadata = `{approval_authority_id, membership_id, authority_name, organization_id}`, `actor_id="person-123"`. Only identifiers/names/reason — no claim blob, no token, no secret. **PASS** |

**Validation conclusion:** the corrected `§29.2` algorithm genuinely eliminates the pre-fix false-`ALLOW` (P3 vs. negative control P4); step ordering is empirically enforced, not merely asserted (P1, P2); the partial unique index is a real, DB-enforced guard under SQLite (P8, P9); every outcome is audited with no secret leakage (P10, P-audit-content).

### 3.1 Enumeration of every binding-row creation path

`grep -rn` across `--include=*.py` (excluding tests/probes/venv) for `MembershipApprovalAuthority(` / `.bind(` / `binding_repo.create` / `MembershipApprovalAuthorityService`: the **only** row-creation path is `MembershipApprovalAuthorityService.bind()`, which enforces the cross-Organization 409 guard and the duplicate-open 409 guard. **No FastAPI router wires binding management** (WP-18 is infrastructure-only). Therefore the P7 precondition (a cross-Organization binding row) is **unreachable through any WP-18 code path** — it would require direct DB write access (⇒ the trust boundary is already lost) or a future, differently-authored binding path that omits the guard.

---

## 4. `CLAUDE.md §21.4` Mandatory Tenant-Isolation Test Checklist — Independently Re-Applied

| §21.4 clause | Bind-time | Resolution-time |
|---|---|---|
| **(a) two distinct, unrelated Organizations with no shared row** | `test_bind_cross_organization_rejected` + Probe P5/P7 seed fully separate Organization + Person + Role + Membership graphs | idem — resolver probes P5, P6, P7 |
| **(b) a caller in one Organization cannot retrieve/infer another Organization's data** | `bind()` compares `membership.organization_id` vs `authority.organization_id` ⇒ 409, and asserts **no row created** (`get_open_binding(...) is None`) — re-run, passing; Probe P7 confirms the guard | resolver step 4 compares `caller_organization_id` (JWT claim) vs `target_organization_id` (`X-Tenant-ID`-derived) ⇒ `INVALID_SCOPE` **before** any binding lookup — Probe P5 (`INVALID_SCOPE`), existing `test_organization_mismatch_denies` / `test_cross_organization_binding_attempt_rejected` re-run, passing |
| **(c) explicit probe of a foreign-object identifier not derived from the caller's claims** | `bind()` accepts `membership_id` + `approval_authority_id` as parameters (no HTTP surface); cross-Org pair ⇒ 409, no row — Probe P7 | the resolver **never accepts a caller-supplied `approval_authority_id`** — the authority is looked up by `(target_organization_id, authority_name)`. `target_organization_id` is `X-Tenant-ID`-derived and gated at step 4 against the JWT `organization_id`. `caller_membership_id` **is** claim-derived (from the signed JWT), not a free request parameter. Probe P6 (foreign membership id, no binding ⇒ `NO_ELIGIBLE_ACTOR`); Probe P7 (foreign membership id **with** a directly-inserted cross-Org binding ⇒ `AUTHORIZED`, see `VV-O5`) |

**Checklist conclusion:** at the actual request boundary (`enforce_approval_authority` / `require_approval_authority`), the only attacker-controlled value is `X-Tenant-ID`, gated at resolver step 4 against the signed JWT `organization_id`. No foreign, non-claim-derived object identifier is accepted there. §21.4(a)/(b)/(c) are satisfied at both bind-time and resolution-time. `VV-O5` records a defense-in-depth gap that is **only** reachable given both a corrupt cross-Org binding row (no code path creates one) **and** an internally-inconsistent signed JWT (outside the resolver's trust model) — non-material.

---

## 5. Persistence / Database Results

- **`alembic heads`** → `f9a3c7e1b5d2 (head)` — **single, non-branching head.**
- **`alembic history`** → linear chain: `b2c3d4e5f6a7 -> f9a3c7e1b5d2 (membership_approval_authority)`, `a1b2c3d4e5f6 -> b2c3d4e5f6a7 (tenant_registry)`, `c7e2b5a9f1d4 -> a1b2c3d4e5f6 (authority_holders)`, … `<base> -> 8fac154e79e2 (initial_r001_schema)`. No branch, no orphan. `b2c3d4e5f6a7` / `a1b2c3d4e5f6` are the uncommitted WP-16 migrations; the WP-18 migration correctly chains off the most recent (`b2c3d4e5f6a7`).
- **WP-18 migration, SQLite dialect (`alembic upgrade b2c3d4e5f6a7:f9a3c7e1b5d2 --sql`):**
  ```sql
  CREATE TABLE membership_approval_authority (
      membership_id UUID NOT NULL,
      approval_authority_id UUID NOT NULL,
      effective_from DATETIME NOT NULL,
      effective_to DATETIME,
      CONSTRAINT pk_membership_approval_authority PRIMARY KEY (membership_id, approval_authority_id, effective_from),
      CONSTRAINT fk_membership_approval_authority_membership_id FOREIGN KEY(membership_id) REFERENCES memberships (id),
      CONSTRAINT fk_membership_approval_authority_approval_authority_id FOREIGN KEY(approval_authority_id) REFERENCES approval_authorities (id)
  );
  CREATE UNIQUE INDEX ux_membership_approval_authority_active ON membership_approval_authority (membership_id, approval_authority_id) WHERE effective_to IS NULL;
  ```
- **WP-18 migration, PostgreSQL dialect (`postgresql+asyncpg`):** identical structure, `effective_from TIMESTAMP WITH TIME ZONE NOT NULL`, `effective_to TIMESTAMP WITH TIME ZONE` — **matches the canonical `Master_Technical_Architecture.md` schema (lines 1318–1329) exactly** (`TIMESTAMP WITH TIME ZONE`, composite PK on the first three columns, nullable `effective_to`). The partial unique index emits `... WHERE effective_to IS NULL` — valid PostgreSQL partial-index syntax.
- **`downgrade()`, PostgreSQL dialect:** `DROP INDEX ux_membership_approval_authority_active;` then `DROP TABLE membership_approval_authority;` — clean, additive-only reversal, no data migration, nothing destructive to `approval_authorities` / `memberships`.
- **Full-chain `alembic upgrade head` against SQLite fails at the *first* migration** (`8fac154e79e2 initial_r001_schema` — a `create_check_constraint` ALTER unsupported by SQLite's dialect). This is a **pre-existing, chain-wide limitation** (the test harness uses `Base.metadata.create_all`, not migrations); it is **not** WP-18's migration, which uses only `create_table` + `create_index` and generates cleanly in isolation for both dialects (above). `downgrade` of the WP-18 revision in isolation was verified via `--sql`.
- **Composite PK** `(membership_id, approval_authority_id, effective_from)` — correct, canonical; permits multiple distinct time-windows per pair. **`effective_to` semantics:** `NULL` = open (Probe P8/P9, `get_open_binding` filters `effective_to.is_(None)`); past value = closed/ineffective (`get_effective_binding` requires `effective_to IS NULL OR effective_to > now`; existing `test_binding_already_expired_denies` re-run, passing).
- **Partial unique index `ux_membership_approval_authority_active`** genuinely prevents two simultaneously-open bindings for the same pair — **Probe P8** (`IntegrityError`), **Probe P9** negative control (re-open after close allowed).
- **No unintended schema mutation** to `approval_authorities` / `memberships` — migration read + `git diff` of `models/__init__.py` (import + `__all__` only) + `git diff` of `repositories/approval_authority_repository.py` (two new read-only methods; `get_active_dependents`/`has_active_dependents` unchanged).
- **PostgreSQL parity:** verified at DDL-generation level for both `upgrade()` and `downgrade()`; **not** executed against a live PostgreSQL engine (none available — §1). Residual SQLite-only confidence limit for runtime FK enforcement and true-concurrency behaviour of the partial index (§6, §10).

---

## 6. Audit Results

- **Resolver:** `_deny(...)` emits exactly one `record_audit(action="RESOLVE_APPROVAL_AUTHORITY", status=AuditStatus.DENIED, actor_id=<person_id or "SYSTEM">, metadata={"reason": <label>, **extra})` for **every** denial branch (`NO_AUTHORITY_CONFIGURED`, `INACTIVE_AUTHORITY` [+`{"status": …}`], `INVALID_CONFIGURATION`, `UNSUPPORTED_STRATEGY` [+`{"approval_strategy": …}`], `INVALID_SCOPE`, `NO_ELIGIBLE_ACTOR`, `INACTIVE_MEMBERSHIP`). The `AUTHORIZED` path emits `record_audit(status=SUCCESS, …)` + `publish_event("APPROVAL_AUTHORITY_RESOLVED", {…, "decision": "AUTHORIZED"})`. Confirmed by full-module read + **Probe P10** + **Probe P-audit-content** + existing `test_authorized_outcome_is_audited` / `test_denied_outcome_is_audited_with_reason` re-run.
- **Bind service:** `bind()` audits `BIND_APPROVAL_AUTHORITY` on missing membership (DENIED), missing authority (DENIED), cross-Org (DENIED, with both `organization_id`s in metadata), duplicate open (DENIED), and success (SUCCESS) + `publish_event("MEMBERSHIP_APPROVAL_AUTHORITY_BOUND")`. `close()` audits `CLOSE_APPROVAL_AUTHORITY_BINDING` on missing open binding (DENIED) and success (SUCCESS) + `publish_event("MEMBERSHIP_APPROVAL_AUTHORITY_CLOSED")`. Confirmed by full-module read.
- **No sensitive claim material persisted:** audit metadata across all branches carries only UUIDs, `authority_name`, `reason`, and `approval_strategy` / `status` strings. `actor_id` is `claims.get("person_id")` (a UUID string) or `"SYSTEM"`. No raw JWT, `Authorization` header, `JWT_SECRET_KEY`, or password appears in any `record_audit`/`publish_event` call (grep + Probe P10 + Probe P-audit-content). Uses the existing `observability.py` convention — no new audit subsystem.

**Audit conclusion:** every outcome (bind success/failure, close success/failure, resolution success + all seven denial reasons) is audited with the expected status and reason context, and no sensitive material is improperly persisted.

---

## 7. Regression Results — Independently Re-Run, Fresh

**Command:** `./venv/Scripts/python.exe -m pytest tests/test_approval_authority_resolver.py tests/test_membership_approval_authority_service.py -v`
**Actual output (tail):** `30 passed, 1 warning in 5.48s` — exit code 0. 22 in `test_approval_authority_resolver.py` + 8 in `test_membership_approval_authority_service.py`, every named test PASSED. The one warning is a pre-existing `StarletteDeprecationWarning` (`httpx` / `starlette.testclient`), unrelated.

**Command:** `./venv/Scripts/python.exe -m pytest -q` (full AuthService suite)
**Actual output (tail):** `853 passed, 52 warnings in 241.90s (0:04:01)` — **exit code 0.** Independently reproduces the `IMP-REPORT-WP-18 §4` and `CERT-WP-18 §F` figure of 853 (823 pre-existing + 30 new). All 52 warnings are pre-existing deprecation warnings (`HTTP_422_UNPROCESSABLE_ENTITY`, `StarletteDeprecationWarning`) — none WP-18-related, none a failure.

**`TDS-018 §29.6` minimum obligations — each exercised by a real passing test** (independently re-run): `ANY_ONE` + valid binding ⇒ `AUTHORIZED` (`test_any_one_with_valid_binding_authorizes`, `test_binding_open_ended_and_currently_effective_authorizes`); `MAJORITY`/`ALL`/`SEQUENTIAL` + valid binding ⇒ `UNSUPPORTED_STRATEGY`, never `AUTHORIZED` (`test_unsupported_strategy_with_valid_binding_never_authorizes[MAJORITY-60 | ALL-None | SEQUENTIAL-None]`); malformed `MAJORITY` (NULL threshold) ⇒ `INVALID_CONFIGURATION`, unreachable via a qualifying binding (`test_malformed_majority_configuration_denies_before_binding_check`); `NO_AUTHORITY_CONFIGURED`, `INACTIVE_AUTHORITY` (×3 SUPERSEDED/DEPRECATED/RETIRED), `INVALID_SCOPE`, `NO_ELIGIBLE_ACTOR`, `INACTIVE_MEMBERSHIP` each dedicated.

**Regression conclusion:** 30/30 dedicated + 853/853 full regression pass, exit code 0, independently re-run this session.

---

## 8. Scope-Containment Result

- **No C-023 implementation** — `grep -rniE "license|entitlement|subscription|billing|c-023"` over the 7 WP-18 files returns exactly **one** hit: a comment in `test_approval_authority_resolver.py` naming C-023 as a hypothetical future consumer. Zero implementing code.
- **No WP-17 implementation** — no `WP-17` / Entitlement-Context file in the WP-18 change set.
- **No frontend / UI** — none in the file set (charter §21 designates the WP backend-only / infrastructure-only).
- **No Group infrastructure** — `grep` for `group_registry|group_membership|group_approval` over the 7 WP-18 files: zero hits.
- **`AuthorityHolder` not replaced or modified** — `models/authority_holder.py` is a pre-existing untracked WP-16 file, not in the WP-18 set; its `CheckConstraint("authority_identity IN ('AI-001', 'AI-002')")` is intact and unreferenced by any WP-18 file.
- **Runtime Engine untouched** — `git status --short Backend/Runtime/` returns nothing. `authorization/tier_resolvers.py::ApprovalAuthorityResolver` is `class ApprovalAuthorityResolver(BaseTierResolver)` with only a `TIER` ClassVar, **no `resolve()` override**; `BaseTierResolver.resolve` is `@abstractmethod` raising `NotImplementedError` ⇒ **uninstantiable abstract stub.** No Option A / M2–M6 work.
- **No `PLATFORM_ADMIN` / `AUREX_ADMIN` redesign** — the two WP-18 `dependencies.py` functions grant these no bypass; no existing admin dependency modified (`git diff`).
- **No unrelated authorization redesign** — `require_platform_admin`, `require_matching_tenant_or_platform_admin`, `require_domain_permission` unchanged in the diff.

**Scope conclusion:** the WP-18 change set is confined to C-003 Approval Authority runtime-binding infrastructure.

---

## 9. Assessment of TD-028 / TD-096 / TD-159 / TD-160

**TD-028 (retirement-dependency handling does not incorporate `membership_approval_authority`) — ACCEPTED FOLLOW-UP, NOT a WP-18 defect.**
`ApprovalAuthorityRepository.get_active_dependents()` / `has_active_dependents()` still do not query the new table, so `ApprovalAuthorityService`'s `BR-C003-04` retirement path can retire an authority that has open bindings. Traced empirically (**Probe P-TD028**): a `RETIRED` authority + a genuine open binding + an `ACTIVE` membership + matching org ⇒ resolver returns **`INACTIVE_AUTHORITY` (DENY)** at step 1 (which only accepts `status == ACTIVE`). **No wrong `ALLOW` is producible.** Orphaned-pointing binding rows simply resolve to DENY — no false authorization, no data-integrity violation. The charter §19 explicitly lists "Modification of certified Approval Authority CRUD behavior" as out of scope, so leaving `ApprovalAuthorityService` untouched is **correct scope confinement.** `TD-028` is a pre-existing register entry (raised in WP-02 BA-08, Medium, Data Integrity, Open) whose stale docstring ("not yet implemented anywhere in AuthService") is now factually inaccurate — a documentation-cleanliness item for a future Work Package that touches `ApprovalAuthorityService`. Same conclusion as `CERT-WP-18` Observation 2, independently re-derived.

**TD-096 (harness does not enforce `PRAGMA foreign_keys=ON`) — MATERIAL CONFIDENCE LIMIT DISCLOSED, does not undermine WP-18.**
The two WP-18 FKs (`memberships.id`, `approval_authorities.id`) are present in the generated DDL for both dialects (§5) and would be enforced in production (PostgreSQL). Under the SQLite harness they are not exercised at the constraint level. However: (a) `bind()` performs explicit application-layer existence checks (404) for both FK targets — tested and re-run; (b) the resolver looks authority up by `(org, name)` and binding by `(membership_id, authority_id)` — no reliance on FK enforcement; (c) the **most important new constraint** — the partial unique index `ux_membership_approval_authority_active` — is a `UNIQUE` index, **not** FK-dependent, and **is** genuinely enforced by SQLite (Probe P8/P9). No FK-dependent invariant is load-bearing for WP-18's chartered scope. Residual limit: FK behaviour and partial-index behaviour under a production-parity engine (PostgreSQL) could not be executed here (no PG available). Same class of gap every Work Package since WP-07 faces; **not introduced or worsened by WP-18.**

**TD-159 (StaticPool — single shared connection) — CONFIDENCE LIMIT, not a WP-18 defect.**
`create_async_engine("sqlite+aiosqlite:///:memory:")` auto-selects `StaticPool`; two `AsyncSession`s share one physical connection, so a genuine two-connection race on the `bind()` check-then-insert (`get_open_binding` → 409, else `create` + `flush`) cannot be reproduced here. Mitigation already in the implementation: the partial unique index is the DB-level backstop — under real concurrency, a racing second open insert raises `IntegrityError` at `flush()` (fail-closed: no double binding, a 500 rather than a graceful 409, which is acceptable for a should-never-happen race). Not worsened by WP-18; the backstop constraint is present in both dialects' DDL.

**TD-160 (session override skips production commit/rollback wrapping) — CONFIDENCE LIMIT, not a WP-18 defect.**
`conftest.py`'s `override_get_session` yields the session without the production `commit`/`rollback`/`close` wrapping. WP-18's `bind()`/`close()` call `session.flush()` (not `commit()`), consistent with the rest of the codebase's service layer, and the resolver performs no writes. No WP-18-specific defect is masked. Pre-existing, repository-wide, inherited unchanged.

**Overall:** none of TD-028 / TD-096 / TD-159 / TD-160 is a WP-18 defect or a Gate 2 blocker. TD-028's practical risk is empirically neutralised by the resolver's fail-closed step 1. TD-096 leaves a genuine SQLite-only residual confidence limit for FK / partial-index behaviour under PostgreSQL (§10). See §13 `VV-O3` for the `CLAUDE.md §19.8.2` register-hygiene observation.

---

## 10. PostgreSQL Parity Check — Not Executable Here

No PostgreSQL engine, Docker daemon, or local PG cluster is available in this environment (`which psql`, `docker ps`, `pg_lsclusters` all negative). PostgreSQL parity was therefore verified **only** at the DDL-generation level (`alembic … --sql` for the `postgresql+asyncpg` dialect, §5), which confirms the WP-18 migration emits canonical-conformant PostgreSQL DDL for both `upgrade()` and `downgrade()`, including a syntactically valid partial index. **Residual SQLite-only confidence limit:** the runtime behaviour of the two foreign keys (blocked under `TD-096`) and the concurrency behaviour of `ux_membership_approval_authority_active` under genuinely separate connections (blocked under `TD-159`) were not exercised against a production-parity engine. This is the same limit every prior Work Package's V&V Audit has recorded; it is not specific to, introduced by, or worsened by WP-18. Recommend the eventual `TD-096` / `TD-159` remediation pass re-confirm WP-18's constraints specifically.

---

## 11. Gate 1's Four Observations — Independently Re-Examined

| Gate 1 obs. | Independent re-examination | Disposition |
|---|---|---|
| **Obs. 1 (Low)** — two non-struck design-rationale phrases in `TDS-018`'s frozen `§§1–28` (`§1`: "does not exist anywhere in this codebase today"; `§4.2`: "Not implemented anywhere in `AuthService`") are factually stale post-implementation | Confirmed present and stale. They sit inside the `§29`/`§31.1`-declared "preserved unchanged" historical body; they are design-motivation narrative, **not** status-of-record assertions. The three current-status locations (corrected header block, `§29.9` superseding note, `§31.3` table) are all correct. A reader cannot conclude WP-18 is unauthorised/uncertified. **Does not recreate M-1.** | Carried forward as **`VV-O1`** (§13). Low, non-blocking. |
| **Obs. 2 (Low)** — certified `ApprovalAuthorityService` retirement path does not see `membership_approval_authority` bindings (`TD-028`) | Independently traced (Probe P-TD028, §9): resolver step 1 yields `INACTIVE_AUTHORITY` for a retired authority regardless of bindings ⇒ no wrong `ALLOW`, no data-integrity violation. Correct scope confinement (charter §19). | Carried forward as **`VV-O2`** (§13). Low, non-blocking. |
| **Obs. 3 (Low)** — the two `IMP-REPORT-WP-18 §5` follow-ups (`TD-028` stale docstring; `TD-096`) are recorded only in the Implementation Report, not cross-referenced in `TECH-DEBT.md` (`CLAUDE.md §19.8.2`) | Confirmed: `TECH-DEBT.md`'s `TD-028` and `TD-096` entries carry no WP-18 cross-reference. Both are pre-existing entries; the substantive debt is already registered. A one-line cross-reference on each would satisfy `§19.8.2` hygiene. | Carried forward as **`VV-O3`** (§13). Low, non-blocking; recommend the Gate 5 / a future pass add the cross-references. |
| **Obs. 4 (informational)** — repository-wide harness fidelity (`TD-096`/`TD-159`/`TD-160`) leaves WP-18's FKs and partial unique index not fully exercised at the DB-constraint level; earmarked for this Gate 2 checklist | Re-applied (§9, §10). The partial unique index **is** enforced under SQLite (Probe P8/P9); the FKs are not (`TD-096`) and true concurrency is not reproducible (`TD-159`); no PostgreSQL available for parity execution. No load-bearing WP-18 invariant depends on the unexercised behaviour. | Carried forward as **`VV-O4`** (§13). Informational; residual SQLite-only limit stated. |

**None of Gate 1's four observations is upgraded to a material finding on re-examination.** No evidence that Gate 1 certification was materially incorrect.

---

## 12. Change-Control Verification

**Before this audit (repo root):**
```
git rev-parse HEAD        -> e86192f95a1ef3534513f9fcee9418bbecb21baf
git status --short        -> 126 entries (10 modified tracked files under Backend/Services/AuthService;
                             8 modified tracked governance/CLAUDE files; remainder untracked —
                             WP-16/C-040 + WP-18 backend + governance artifacts)
git diff --check          -> only "LF will be replaced by CRLF" informational warnings; no whitespace/conflict errors
git diff --cached --stat  -> (empty — nothing staged)
```

**After this audit (repo root):**
```
git rev-parse HEAD        -> e86192f95a1ef3534513f9fcee9418bbecb21baf   (unchanged)
git status --short        -> 127 entries (identical set; the one added line is this V&V audit file,
                             architecture/06-Reviews/VV-AUDIT-WP-18_Approval_Authority_Runtime_Binding.md,
                             a new untracked file)
git diff --check          -> only "LF will be replaced by CRLF" informational warnings; no whitespace/conflict errors
git diff --cached --stat  -> (empty — nothing staged)
```

**Probe scripts** (`_vv_wp18_probe.py`, `_vv_wp18_probe2.py`) were created temporarily inside `Backend/Services/AuthService/` and **deleted immediately after use** — confirmed absent from the post-audit `git status`. Throwaway SQLite files (`/tmp/x.db`, `/tmp/wp18_vv_probe.db`) removed.

**Files changed by this audit:** exactly one — the creation of this file (`architecture/06-Reviews/VV-AUDIT-WP-18_Approval_Authority_Runtime_Binding.md`). **No implementation file, migration, test, `TDS-018`, the WP-18 charter, `IMP-REPORT-WP-18`, `WPR-001`, `TECH-DEBT.md`, `CERT-WP-18`, `IRA-C023`, `TDS-C023`, or the `WP-17` charter was modified.** Nothing staged, committed, or pushed. This file is left uncommitted, matching the `VV-AUDIT-WP-16` convention.

---

## 13. Material Findings and Non-Material Observations

### Material Findings

**None.** No `CLAUDE.md §19.8.5`-class defect (architectural / security / data-integrity / tenant-isolation defect; failing test; build failure; broken functionality; mandatory-compliance failure). No false `ALLOW`. No behaviour-changing discrepancy from `TDS-018 §29.2`. No out-of-scope implementation. No evidence Gate 1 certification was materially incorrect. **Gates 3–4 (remediation and its independent verification) are NOT triggered.**

### Non-Material Observations (non-blocking)

- **`VV-O1` (Low)** — `TDS-018 §1` and `§4.2` carry non-struck, now-stale "does not exist / not implemented" design-rationale phrases inside the frozen `§§1–28` historical body. Not status-of-record; does not recreate M-1. Recommend a brief forward-pointing note at a convenient future documentation pass (mirrors `CERT-WP-18` Obs. 1). Not a Gate 2 blocker.
- **`VV-O2` (Low)** — `ApprovalAuthorityService.get_active_dependents()` / `has_active_dependents()` do not query `membership_approval_authority` (`TD-028`); a retired authority with open bindings resolves to `INACTIVE_AUTHORITY` (DENY, empirically verified) so no wrong `ALLOW` results. Correct scope confinement; reconcile the stale `TD-028` docstring in a future Work Package touching `ApprovalAuthorityService`. Not a Gate 2 blocker.
- **`VV-O3` (Low)** — the `IMP-REPORT-WP-18 §5` follow-ups are not cross-referenced in `TECH-DEBT.md`'s `TD-028` / `TD-096` entries (`CLAUDE.md §19.8.2` hygiene). Recommend a one-line cross-reference on each entry at the Gate 5 pass or a convenient future pass. Not a Gate 2 blocker.
- **`VV-O4` (informational)** — SQLite/StaticPool harness (`TD-096` / `TD-159` / `TD-160`) does not enforce FKs or reproduce true cross-connection concurrency; no PostgreSQL available in this environment for parity execution. The partial unique index **is** enforced under SQLite (Probe P8/P9). Residual SQLite-only confidence limit for WP-18's FKs and partial-index concurrency behaviour under PostgreSQL. Not introduced or worsened by WP-18; recommend the eventual `TD-096`/`TD-159` remediation re-confirm WP-18's constraints specifically.
- **`VV-O5` (Low — NEW this Gate; does NOT require correction)** — **defense-in-depth:** the resolver's step 6 (membership validity) verifies `membership_status == "ACTIVE"` and the membership's effective window, but does **not** independently re-verify `membership.organization_id == target_organization_id`. Tenant isolation at resolution-time rests on step 4 (caller-claim `organization_id` vs. `target_organization_id`) **plus** the bind-time cross-Organization 409 guard **plus** the signed JWT's internal consistency (its `organization_id` and `membership_id` refer to the same membership). **Probe P7** shows that if a cross-Organization `membership_approval_authority` row somehow exists *and* the caller presents claims where `organization_id` equals the target but `membership_id` points to a foreign-Organization `ACTIVE` membership, the resolver returns `AUTHORIZED`. This is **non-material** because: (1) **no WP-18 code path can create a cross-Organization binding row** — the sole creation path (`MembershipApprovalAuthorityService.bind()`) rejects it with 409, and no router wires binding management (§3.1); (2) the implementation **conforms to `TDS-018 §29.2` as written** — step 4 is the designated Organization check, and step 6 as specified requires only membership validity; (3) the signed JWT is the trust anchor for claim internal consistency — forging `organization_id`≠`membership_id`-origin would be an AuthService token-issuance defect, outside this resolver's trust boundary. **Recommendation (hardening, optional):** add a cheap `membership.organization_id == target_organization_id` assertion at step 6 so resolution-time isolation does not depend on the bind-time guard never having been bypassed. This is a strengthening suggestion, **not** a defect requiring remediation — Gates 3–4 are not triggered.

---

## 14. Final Determination

### PASS WITH OBSERVATIONS

WP-18 (Bind and Resolve Approval Authority, C-003) **passes the Gate 2 Verification & Validation Audit.** The implementation faithfully realizes `TDS-018 §29.2`'s corrected 8-step resolver algorithm in exact, empirically-verified order — configuration validation (step 2) and the `approval_strategy` gate (step 3) both fire **before any caller-specific step** (Probes P1, P2), so a qualifying Membership binding cannot bypass them; `MAJORITY` / `ALL` / `SEQUENTIAL` terminate at step 3 with `DENY` / `UNSUPPORTED_STRATEGY` and are never counted, simulated, or approximated (Probe P3), while a reconstruction of the pre-fix `§10` algorithm does false-`ALLOW` the identical scenario (negative control P4), confirming the corrected gate is what closes the defect. Every branch is fail-closed with no `PLATFORM_ADMIN` / `AUREX_ADMIN` / Role / Group fallback. The `§29.4` 8-label reason taxonomy is exact. Tenant isolation is enforced at bind time (service-layer 409, no row created — Probe P7) and at resolution time (step-4 scope check against an `X-Tenant-ID`-derived target independent of caller JWT claims — Probe P5); the `CLAUDE.md §21.4` checklist is satisfied at both layers. The `membership_approval_authority` model and migration match the canonical `Master_Technical_Architecture.md` schema exactly for both SQLite and PostgreSQL DDL, are strictly additive (clean `downgrade()`), and yield a single non-branching Alembic head `f9a3c7e1b5d2`. The partial unique index `ux_membership_approval_authority_active` genuinely prevents two simultaneously-open bindings (Probe P8) and correctly permits re-open after close (Probe P9). Every resolution and binding outcome is audited via the existing `observability.py` convention with no sensitive claim material persisted (Probes P10, P-audit-content). 30/30 dedicated tests and 853/853 full AuthService regression pass, independently re-run this session (exit code 0). Scope is confined to C-003 Approval Authority runtime-binding infrastructure — no C-023, no WP-17, no frontend, no Group infrastructure, no `AuthorityHolder` modification, no Runtime Engine M2–M6 work (`ApprovalAuthorityResolver` remains an uninstantiable abstract stub), no admin redesign. TD-028's practical risk is empirically neutralised by the resolver's fail-closed step 1 (Probe P-TD028). Five non-material observations are recorded (`VV-O1`–`VV-O5`); none is a `CLAUDE.md §19.8.5`-class defect and none requires remediation.

**No `CLAUDE.md §19.8.5`-class defect was found. Gate 1 certification is not shown to be materially incorrect.**

### Gate scope and residual status

- **This is Gate 2 only** (Verification & Validation Audit, `CLAUDE.md §19.7b`). **Gates 3–4 (remediation and its independent verification) are triggered only if Gate 2 finds a defect requiring remediation — it did not, so they do not apply.** **Gate 5 (Release Readiness Audit) was NOT performed and is NOT passed.**
- **WP-18 is NOT fully released.** The five-gate sequence is not complete; nothing is committed or pushed.
- **C-023 remains 🔴 RED — NOT IMPLEMENTATION READY.** Unchanged by WP-18 or by this audit.
- **WP-17 remains CHARTERED — NOT IMPLEMENTED, NOT CERTIFIED.** Unchanged by WP-18 or by this audit.
- `IRA-C023`, `TDS-C023`, and the `WP-17` charter were confirmed untouched by the WP-18 change set.

---

## Change Control

**Files read (not modified) in preparing this audit:** every governing document and every backend/test file listed under §1.

**Files created by this audit:** this document only — `architecture/06-Reviews/VV-AUDIT-WP-18_Approval_Authority_Runtime_Binding.md` (left uncommitted, matching the `VV-AUDIT-WP-16` convention).

**Files modified:** none. No application code, schema, migration, ADR, `TDS-018`, the WP-18 charter, `IMP-REPORT-WP-18`, `WPR-001`, `TECH-DEBT.md`, `CERT-WP-18`, `CAP-001`, `IRA-C023`, `TDS-C023`, the `WP-17` charter, or any other governance document was modified.

**Temporary artifacts:** `_vv_wp18_probe.py`, `_vv_wp18_probe2.py` (in `Backend/Services/AuthService/`) and throwaway SQLite DB files — all deleted; confirmed absent from the post-audit `git status`.

**Not performed:** no Release Readiness Audit; no WP-18 closure; no remediation; no `membership_approval_authority` row created outside throwaway in-memory probe databases; no commit; no push.
