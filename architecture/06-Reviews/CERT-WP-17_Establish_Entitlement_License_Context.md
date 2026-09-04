# CERT-WP-17 — Independent Certification (Gate 1 of 5) — Establish Entitlement/License Context (Administrative) (C-023, BA-01)

**Work Package:** WP-17
**Capability:** C-023 — Licensing & Entitlement (`CAP-001` line 77, Domain D-002 "Commercial & Subscription", `URA-001`, Active — capability-wide status **🔴 RED — Not Implementation Ready**, `IRA-C023 §16`, unchanged)
**Business Activity:** BA-01 — Establish Entitlement/License Context (Administrative)
**Gate:** `CLAUDE.md §19.7b` **Gate 1 — Independent Certification** (gate 1 of 5). Gate 2 (V&V Audit) and Gate 5 (Release Readiness Audit) are separate, later, independently-staffed gates and are **not** performed here. Gates 3–4 are triggered only if a later gate finds a defect requiring remediation.

**State certified:**
- `git rev-parse HEAD` → `c2f93d55daa6806939d98c389f5edcd73993ac60` (`main`)
- All WP-17 work is uncommitted in the working tree (nothing staged, nothing committed). This certification isolates and certifies the **WP-17 change set only**, exactly as `CERT-WP-18` / `CERT-WP-16` certified an uncommitted working tree for their own scope. The working tree also carries a large body of pre-existing, unrelated C-040 / ROD / ADR-027…035 / `IRA-C114` / `Sarika_consent.png` / `Master_Platform_Capability_Delivery_Map.xlsx` noise that is **not** part of WP-17 and was verified (item 12) to carry no WP-17 content.
- `git status --short` at certification time is reproduced verbatim in the appendix ("Before").
- `git diff --check` → no whitespace errors, no conflict markers (only CRLF-normalisation `warning:` lines, pre-existing repo behaviour).

**Reviewer independence statement:** This certification was produced by a genuinely independent, fresh-context reviewer with **no** access to any prior session's conversation and **no** prior involvement in WP-17's implementation, in drafting `TDS-C023` / `TDS-C023-A` / `STOP-AND-REPORT-WP-17-01` / the `WP-17` charter / `IMP-REPORT-WP-17`, in the prior fidelity review of the D-1…D-7 schema-decision recording, or in the prior implementation readiness review. Every material claim below was **re-derived from primary sources** — actual files opened, actual commands run, purpose-built runtime probes written from scratch. No prior report's conclusion was accepted on trust.

---

## CURRENT CERTIFICATION STATE (2026-09-02) — ✅ GATE 1 CERTIFIED (third attempt)

**This document records three Gate 1 Independent Certification attempts.** The first two — the `## DETERMINATION` / Findings sections immediately below (2026-09-01), and the `## Gate 1 Re-Certification (fresh independent reviewer, post-R9)` section (2026-09-01) — each returned **❌ NOT CERTIFIED**, in both cases for **one M-1-class finding only**: a live, non-struck, stale-status self-contradiction in the WP-17 status-of-record governance documents. **Neither attempt ever found a `CLAUDE.md §19.8.5`-class code, security, data-integrity, tenant-isolation, test, build, design-conformance, or scope defect** — the technical implementation passed every other checklist item at both attempts.

After the M-1 stale-status documentation was fully reconciled (`IMP-REPORT-WP-17 §16.1`/`§16.2`/`§16.3`), a **third, fresh-context independent Gate 1 reviewer** — with no involvement in WP-17's implementation, in any R2–R9 / R9-completion / final-cleanup reconciliation pass, or in either prior Gate 1 attempt — was dispatched (2026-09-02) per direct Repository Owner authorization and returned **✅ GATE 1 PASSED**. That determination is recorded in the section **"Gate 1 Re-Certification (Third Attempt) — 2026-09-02 — ✅ CERTIFIED"** appended at the end of this document, and is the **current** Gate 1 state of record. A fresh-context independent **Gate 2 V&V Audit** was subsequently dispatched and **PASSED on the technical merits** (`IMP-REPORT-WP-17 §17`).

The two `❌ NOT CERTIFIED` sections below are **preserved unchanged as the historical record** of the first and second attempts.

**Current status:** WP-17 / BA-01 = IMPLEMENTATION AUTHORIZED — IMPLEMENTATION COMPLETE — **GATE 1 PASSED** — **GATE 2 V&V PASSED** — Gates 3/4 not triggered — **GATE 5 RELEASE READINESS PASSED** — ~~**GATE 5 (Release Readiness) PENDING; NOT YET RELEASE-READY.**~~ *(Superseded 2026-09-02 — Gate 5 Release Readiness Audit PASSED by a fresh independent reviewer; see `IMP-REPORT-WP-17 §18`.)* **FORMALLY CLOSED — CERTIFIED — RELEASE-READY** (all five `CLAUDE.md §19.7b` gates complete; governance-recording complete; repository commit outstanding — a separate, explicitly-authorized action, mirroring `WP-16`/`WP-18`'s own recorded closure state). C-023 capability-wide remains **🔴 RED — Not Implementation Ready** (`IRA-C023 §16`, unchanged); Decisions 1–6 untouched; Decision 3 and Decision 4 remain DEFERRED.

---

## DETERMINATION (first attempt — 2026-09-01 — historical; superseded, see "CURRENT CERTIFICATION STATE" above)

### ❌ NOT CERTIFIED (first attempt — historical)

**One MATERIAL DEFECT** was found — an **M-1-class live, non-struck, stale-status self-contradiction** in the Work Package's status-of-record governance documents. It is **not** a code, security, design-conformance, test, build, or scope defect (none of those was found — the technical implementation is sound and every other checklist item passed). It is materially identical in kind to the governance-documentation contradiction that returned **NOT CERTIFIED** at WP-18's first Gate 1 attempt.

Per this gate's own STOP conditions ("*a live non-struck stale-status self-contradiction (M-1 class): the determination is NOT CERTIFIED*"), the determination is **NOT CERTIFIED**. The defect is fully described in **Finding 13 / Material Findings** below. It is remediable by a governance-reconciliation pass (strikethrough-preserve + a new reconciliation section) that brings the `WP-17` charter, the `WPR-001` WP-17 row, and the stale clauses of `IRA-C023 §16` into agreement with `IMP-REPORT-WP-17`'s own current "IMPLEMENTATION COMPLETE — NOT YET CERTIFIED — entering `CLAUDE.md §19.7b`" status, after which Gate 1 may be re-dispatched. **No code change is required.** The reviewer did not modify any file other than creating this artifact.

---

## SCOPE AND METHOD

### Commands run (all from `C:\Ashit\corpstage-enterprise-operating-system`, or `Backend/Services/AuthService` where noted)

| # | Command | Purpose |
|---|---|---|
| 1 | `git rev-parse HEAD` ; `git status --short` ; `git diff --check` ; `git diff --stat` | Capture certified state |
| 2 | `git diff -- Backend/Services/AuthService/main.py models/__init__.py source/frontend/src/config/admin-navigation.ts` | Verify the three tracked-file backend/nav edits |
| 3 | `git diff -- architecture/05-Implementation/IMP-REPORT-WP-17_*.md` | Verify Implementation Report changes |
| 4 | `git diff --stat HEAD -- services/approval_authority_resolver.py dependencies.py models/membership_approval_authority.py repositories/membership_approval_authority_repository.py repositories/approval_authority_repository.py middleware/tenant.py` | Confirm WP-18 consumed-unchanged (zero diff) |
| 5 | `git status --short` on `TDS-018_*`, `CERT-WP-18`, `VV-AUDIT-WP-18`, `RRA-WP-18` | Confirm byte-unchanged |
| 6 | `./venv/Scripts/python.exe -m pytest tests/test_entitlement_license_establishment.py -q` | Re-run targeted suite |
| 7 | `./venv/Scripts/python.exe -m pytest -q` (full AuthService regression, background) | Re-run full suite |
| 8 | `./venv/Scripts/python.exe ./_d4_probe.py` (purpose-built, SQLite `:memory:`, `Base.metadata.create_all`) | D-4 COALESCE-sentinel partial-unique-index probe |
| 9 | `./venv/Scripts/python.exe -m alembic heads` ; `alembic history` | Migration head / linearity |
| 10 | `DATABASE_URL=postgresql+asyncpg://… alembic upgrade --sql f9a3c7e1b5d2:c3d4e5f6a7b8` ; `alembic downgrade --sql c3d4e5f6a7b8:f9a3c7e1b5d2` | Offline PostgreSQL DDL, both directions |
| 11 | `./venv/Scripts/python.exe -m pytest tests/_cert_wp17_probe.py -q -s` (purpose-built, uses repo `conftest.py` `client` / `db_session` fixtures) | Independent tenant-isolation runtime probe |
| 12 | `grep -rniE "granted_capacity\|consumption\|allocation\|catalog\|billing\|subscription\|supersedes_id\|version\|FULL\|LIGHT\|revoke\|suspend" <WP-17 backend change set>` | Excluded-capability scan |
| 13 | `git diff -- <6 unrelated modified governance docs>` piped to `grep -iE "c-023\|wp-17\|entitlement\|licens"` | Scope-containment check |
| 14 | `cd source/frontend && npx tsc --noEmit` ; `npx eslint src/features/entitlement-license src/services/entitlement-license-api.ts src/types/entitlement-license.ts src/config/admin-navigation.ts` | Frontend type/lint |
| 15 | `grep -n` over `middleware/tenant.py` exemption block; `grep -rn "def get_active_by_organization_and_name"` | Tenant-header mandatory; consumed repo method pre-existing |
| 16 | `git log --oneline -3 -- WPR-001` ; `git status --short WPR-001` | Confirm `WPR-001` unmodified in working tree |

The purpose-built probe scripts (`_d4_probe.py`, `tests/_cert_wp17_probe.py`) were created for this certification, run, and **deleted** — they are not part of the repository. Their full source and verbatim output are reproduced in Findings 3 and 8.

### Files read in full (or the cited sections)

- `architecture/05-Implementation/WP-17_C023_BA-01_Establish_Entitlement_License_Context_Business_Activity_Charter.md` — entire charter (194 lines incl. all Change Control R3/R7/R8 entries).
- `architecture/05-Implementation/TDS-C023_Licensing_and_Entitlement_Minimum_BA.md` — §7 (authority model, incl. §7.2 authority name), §14/§15/§16 (transaction / idempotency / audit), §17 (frontend — exactly two items), §18 (dependency matrix), §19 (Decisions 3/4 deferred), §22 (security).
- `architecture/05-Implementation/TDS-C023-A_Entitlement_License_Registry_Schema.md` — intro/type, §3.1/§3.2 (approved schema), §3.3 (deliberate absences), §4 (Decision 6 compliance), §19.0 (D-1…D-7 questions), §19.1 (verbatim Repository Owner decision), §19.2 (confirmed-schema mapping), §19.3 (effect), §20 (no self-authorization), Change Control.
- `architecture/05-Implementation/IMP-REPORT-WP-17_Establish_Entitlement_License_Context.md` — entire report incl. §1 (verbatim Implementation Authorization), §2 (authorized scope), §3 (explicit exclusions), §4 (STOP-and-report obligations), §5, §6 (status), §9 (schema-decision chain), §11 (implementation evidence), §12 + §12.1 (recognized-Entitlement-Type STOP-and-report + Repository Owner Option A decision, verbatim), §13 (Change Control).
- `architecture/05-Implementation/STOP-AND-REPORT-WP-17-01_Entitlement_License_Registry_Schema_Shape.md` — §A (exact question), status line.
- `architecture/07-Decisions/ADR-036_Licensing_and_Entitlement_Persistence_Implementation_Ownership.md` — Status (Accepted), Decision, Consequences.
- `architecture/05-Implementation/IRA-C023_Licensing_and_Entitlement_Implementation_Readiness_Assessment.md` — §16 (Final Readiness Classification + R7/R8 addenda), §15a/G (Decision 6 conflict), Decisions table.
- `architecture/00-Governance/WPR-001_Work_Package_Roadmap.md` — WP-17 row (line 55) + maintenance notes (lines 57–63); WP-18 row + notes (for M-1 precedent).
- `architecture/06-Reviews/CERT-WP-18_Approval_Authority_Runtime_Binding.md` — format/rigor precedent + the "M-1" prior-Gate-1 finding it records as eliminated.
- `CLAUDE.md` — §8, §16, §17, §18, §19 (all subsections incl. §19.7, §19.7b, §19.8.5, §19.8.7), §20 (§20.3–§20.6), §21 (§21.3, §21.4).
- Backend change set: `models/c023_license_context.py`, `models/c023_entitlement_context.py`, `alembic/versions/2026_09_01_0900-c3d4e5f6a7b8_c023_license_entitlement_context.py`, `repositories/c023_license_context_repository.py`, `repositories/c023_entitlement_context_repository.py`, `services/entitlement_license_establishment_service.py`, `schemas/entitlement_license.py`, `routers/entitlement_license.py`, `tests/test_entitlement_license_establishment.py`, plus the `main.py` / `models/__init__.py` diffs.
- Frontend change set: `types/entitlement-license.ts`, `services/entitlement-license-api.ts`, `features/entitlement-license/state/useEntitlementLicense.ts`, `features/entitlement-license/components/{EstablishEntitlementLicenseSection,EntitlementLicenseOutcomeSection,EntitlementLicenseManagementScreen}.tsx`, `app/platform-admin/(workspace)/subscriptions/entitlement-license/page.tsx`, `config/admin-navigation.ts` diff.
- Consumed-unchanged infrastructure: `middleware/tenant.py` (exemption block), `repositories/approval_authority_repository.py` (`get_active_by_organization_and_name`).

---

## GOVERNING DOCUMENTS REVIEWED

`WP-17` charter · `TDS-C023` (§7/§14/§15/§16/§17/§18/§19/§22) · `TDS-C023-A` (§3/§4/§19/§20) · `IMP-REPORT-WP-17` (§1–§13) · `STOP-AND-REPORT-WP-17-01` · `ADR-036` · `IRA-C023 §16` + Decisions 1–6 · `WPR-001` WP-17 row · `TDS-018` / `CERT-WP-18` / `VV-AUDIT-WP-18` / `RRA-WP-18` (cross-reference) · `CLAUDE.md` §8/§16/§17/§18/§19/§20/§21 · `Master_Technical_Architecture.md` `license_registry` / `entitlement_registry` canonical definitions (cross-reference).

---

## POINT-BY-POINT FINDINGS

### 1. Governance traceability — PASS (with the Finding 13 material defect noted separately)

- **Implementation Authorization (`IMP-REPORT-WP-17 §1`)** is reproduced verbatim as issued: authorized scope (AuthService hosting per ADR-036; persistence/model/migration/repository/service/router/schema; WP-18 Approval Authority enforcement; Decision 6 read-only reference; exactly two frontend items; existing audit infra; fail-closed + tenant isolation; §21.4 testing; full §19.7b closure) and explicit exclusions (broader C-023; Consumption/Allocation; Entitlement Catalog; Subscription; Billing; C-020/C-025; migration/offboarding; cross-tenant sharing; Authorization Engine M2–M6; AuthorityHolder replacement; Group infra; any Decision 3/4 implementation; any new service boundary; any unsupported schema decision). The as-built implementation conforms to every clause — see Findings 2–12.
- **D-1…D-7 schema decision (`TDS-C023-A §19.1`)** is reproduced verbatim in a blockquote; `§19.2` maps each approval onto the `§3` element it confirms, stating "*No element of `§3` was edited*". The as-built model + migration match `§3.1`/`§3.2` column-for-column (Finding 2).
- **Option A decision (`IMP-REPORT-WP-17 §12.1`)** is reproduced verbatim: "I choose OPTION A … Do NOT create, infer, seed, or introduce an interim recognized-Entitlement-Type set … the already-designed clean 422 … identifying Decision 3 …". The as-built `_RECOGNIZED_ENTITLEMENT_TYPE_REFS = frozenset()` is exactly this (Finding 6).
- **Grep for contradicting non-struck present-tense claims in `TDS-C023-A` and `IMP-REPORT-WP-17`:** `IMP-REPORT-WP-17 §6` carries the current, unambiguous, non-struck status "**IMPLEMENTATION COMPLETE … NOT CERTIFIED**" with the two earlier "IMPLEMENTATION NOT STARTED" lines struck-through and annotated. `§11.4` records "876 passed"; `§12`/`§12.1` record the Entitlement path blocked **solely** by Decision 3's absent recognized-type source, matching the code. No non-struck claim inside these two documents contradicts "IMPLEMENTATION COMPLETE". `TDS-C023-A`'s own status lines (`§19.3`, `§20`) are framed "at the close of this recording pass" and describe the schema-recording pass's end state (IMPLEMENTATION HALTED pending the sequencing steps) — historical to that pass, superseded by `IMP-REPORT-WP-17 §11`; a reconciliation pass should annotate them but they are not a Work-Package status-of-record the way the charter / `WPR-001` row are (see Finding 13, Observation O2-adjacent).
- **`IMP-REPORT-WP-17` accuracy:** `§11.1`/`§11.2` file lists match the actual working tree exactly; `§11.3` D-1…D-6 mapping matches the model/migration; `§11.4` test description matches `tests/test_entitlement_license_establishment.py`; `§11.5` migration evidence matches `alembic heads`/`history` and the offline SQL; `§11.6`–`§11.8` match the router/service/audit code. **The Implementation Report is an accurate record of what was built.**

### 2. Design conformance — schema to `TDS-C023-A §3.1`/`§3.2` (D-1…D-6) — PASS

Column-by-column, verified in **both** the SQLAlchemy model **and** the Alembic migration:

**`c023_license_context`** (`models/c023_license_context.py`, migration lines 77–118)

| Element | TDS-C023-A §3.1 | Model | Migration | Match |
|---|---|---|---|---|
| `id` | `UUID` PK, `default uuid4` | line 84–87, `primary_key=True, default=uuid.uuid4` | `sa.Column('id', sa.UUID(), nullable=False)` + `PrimaryKeyConstraint('id', name='pk_c023_license_context')` | ✓ |
| `membership_id` | `UUID` NOT NULL, **FK `memberships(id)`**, indexed | line 90–94, `ForeignKey("memberships.id"), nullable=False, index=True` | col + `ForeignKeyConstraint(['membership_id'],['memberships.id'])` + `create_index('ix_c023_license_context_membership_id')` | ✓ |
| `status` | `VARCHAR(20)` NOT NULL, `CHECK IN ('ACTIVE','SUSPENDED','REVOKED')` | line 103–106 `String(20)` + `CheckConstraint("status IN ('ACTIVE','SUSPENDED','REVOKED')", name="ck_c023_license_context_status")` | `sa.String(20)` + identical `CheckConstraint` | ✓ |
| `effective_from` | `TIMESTAMPTZ` NOT NULL, `default now()` | `DateTime(timezone=True), nullable=False, default=…utcnow` | `sa.DateTime(timezone=True), nullable=False` | ✓ |
| `effective_to` | `TIMESTAMPTZ` NULL | `nullable=True` | `nullable=True` | ✓ |
| `entitlement_source_reference` | `VARCHAR(255)` NULL | `String(255), nullable=True` | `sa.String(255), nullable=True` | ✓ |
| `approval_authority_id` | `UUID` NOT NULL, **FK `approval_authorities(id)`**, indexed | `ForeignKey("approval_authorities.id"), nullable=False, index=True` | col + `ForeignKeyConstraint(['approval_authority_id'],['approval_authorities.id'])` + `create_index('ix_c023_license_context_approval_authority_id')` | ✓ |
| `committed_by_actor_id` | `UUID` NOT NULL, **NON-FK** (audit citation) | line 147–150, `SA_UUID(), nullable=False` — **no `ForeignKey`** | `sa.Column('committed_by_actor_id', sa.UUID(), nullable=False)` — **no `ForeignKeyConstraint`** | ✓ |
| `committed_at` | `TIMESTAMPTZ` NOT NULL | `nullable=False` | `nullable=False` | ✓ |
| `c023_license_type` | `VARCHAR(50)` NULL, `CHECK (NULL OR IN ('SUPPLIER','AUDITOR','BOARD_MEMBER','CONSULTANT'))` | line 165–168 `String(50), nullable=True` + `CheckConstraint("c023_license_type IS NULL OR c023_license_type IN ('SUPPLIER','AUDITOR','BOARD_MEMBER','CONSULTANT')", name="ck_c023_license_context_license_type")` | `sa.String(50)` + identical `CheckConstraint` | ✓ |
| `created_at` / `updated_at` | `TIMESTAMPTZ` NOT NULL / NULL `onupdate` | `nullable=False` / `nullable=True, onupdate=…` | `nullable=False` / `nullable=True` | ✓ |
| **PK** | `(id)` | ✓ | `pk_c023_license_context` | ✓ |
| **Partial unique** | `ux_c023_license_context_current` on `(membership_id) WHERE effective_to IS NULL`, cross-dialect | `Index(..., unique=True, postgresql_where=text("effective_to IS NULL"), sqlite_where=text("effective_to IS NULL"))` | identical `create_index(..., unique=True, postgresql_where=…, sqlite_where=…)` | ✓ |

**`c023_entitlement_context`** (`models/c023_entitlement_context.py`, migration lines 120–163)

| Element | TDS-C023-A §3.2 | Model | Migration | Match |
|---|---|---|---|---|
| `id` | `UUID` PK `default uuid4` | ✓ | `PrimaryKeyConstraint('id', name='pk_c023_entitlement_context')` | ✓ |
| `organization_id` | `UUID` NOT NULL, **FK `organizations(id)`**, indexed | `ForeignKey("organizations.id"), nullable=False, index=True` | `ForeignKeyConstraint(['organization_id'],['organizations.id'])` + `create_index('ix_c023_entitlement_context_organization_id')` | ✓ |
| `domain_id` | `UUID` NULL, **FK `domains(id)`** | `ForeignKey("domains.id"), nullable=True` | `ForeignKeyConstraint(['domain_id'],['domains.id'])` | ✓ |
| `entitlement_type_ref` | `VARCHAR(100)` NOT NULL | `String(100), nullable=False` | `sa.String(100), nullable=False` | ✓ |
| `status` | `VARCHAR(20)` NOT NULL, same CHECK | `String(20)` + `CheckConstraint("status IN ('ACTIVE','SUSPENDED','REVOKED')", name="ck_c023_entitlement_context_status")` | identical | ✓ |
| `effective_from` / `effective_to` | `TIMESTAMPTZ` NOT NULL / NULL | ✓ | ✓ | ✓ |
| `entitlement_source_reference` | `VARCHAR(255)` NULL | ✓ | ✓ | ✓ |
| `approval_authority_id` | `UUID` NOT NULL, **FK `approval_authorities(id)`**, indexed | ✓ + `index=True` | `ForeignKeyConstraint([...],['approval_authorities.id'])` + `create_index('ix_c023_entitlement_context_approval_authority_id')` | ✓ |
| `committed_by_actor_id` | `UUID` NOT NULL, **NON-FK** | `SA_UUID(), nullable=False` — no FK | no `ForeignKeyConstraint` | ✓ |
| `committed_at` / `created_at` / `updated_at` | as `§3.1` | ✓ | ✓ | ✓ |
| **Non-unique lookup** | `ix_c023_entitlement_context_org_type` on `(organization_id, entitlement_type_ref)` | `Index("ix_c023_entitlement_context_org_type", "organization_id", "entitlement_type_ref")` | `create_index('ix_c023_entitlement_context_org_type', [...,'organization_id','entitlement_type_ref'])` | ✓ |
| **Partial unique** | `ux_c023_entitlement_context_current` on `(organization_id, COALESCE(domain_id, '00000000-0000-0000-0000-000000000000'), entitlement_type_ref) WHERE effective_to IS NULL`, cross-dialect | `Index(..., text("COALESCE(domain_id, '00000000-0000-0000-0000-000000000000')"), ..., unique=True, postgresql_where/sqlite_where)` | identical `create_index` | ✓ |

**Deliberate absences (`TDS-C023-A §3.3`) — all confirmed absent** in the model, migration, schema, service, and router (grep item 12): **no** `FULL`/`LIGHT` column or value (only the `URA-001-115` four-value CHECK on the disjoint `c023_license_type`); **no** FK to `memberships.license_type`; **no** `version` / `supersedes_id` / `granted_capacity` / `consumption` / `available_capacity` / billing / price / currency / contract-line / `aligned_to_subscription_id` / catalog-definition column. Every grep hit for those tokens was in a docstring, comment, CHECK-constraint value list (D-5-approved), or a user-facing rejection message explaining what is *not* done.

**One non-material deviation — see Observation O1** (D-4 expression omits the explicit `::uuid` cast that `TDS-C023-A §19.2` shows; the migration docstring documents the exact expression and the reason, satisfying the Repository Owner's D-4 condition).

### 3. D-4 cross-dialect condition — PASS

- **Documented:** the exact expression `COALESCE(domain_id, '00000000-0000-0000-0000-000000000000')` appears in `models/c023_entitlement_context.py` (module constant `_CURRENT_ENTITLEMENT_UNIQUE_EXPR`, lines 24–40, with a paragraph explaining PostgreSQL implicit-cast-inside-COALESCE vs SQLite string round-trip) **and** in the migration docstring (lines 29–48, "D-4 cross-dialect note").
- **From-scratch SQLite probe** (`_d4_probe.py` — SQLite `:memory:`, `Base.metadata.create_all`, run via `./venv/Scripts/python.exe` from `Backend/Services/AuthService`):

```python
# seed Organization + ApprovalAuthority, then:
s.add(mk("X")); await s.flush()          # row1: domain_id=None, entitlement_type_ref='X', effective_to=None
s.add(mk("X"))                            # row2: identical
try:    await s.flush()                   # expect IntegrityError
except IntegrityError: await s.rollback()
s.add(mk("Y")); await s.flush()          # row3: entitlement_type_ref='Y' -> expect OK
```

Verbatim output:

```
row1 (domain_id=None, ref=X): inserted OK
row2 (identical): IntegrityError as expected -> UNIQUE constraint failed: index 'ux_c023_entitlement_context_current'
row3 (domain_id=None, ref=Y): inserted OK
```

- **PostgreSQL offline DDL** (`DATABASE_URL=postgresql+asyncpg://… alembic upgrade --sql f9a3c7e1b5d2:c3d4e5f6a7b8`) — the index DDL emitted is syntactically valid PostgreSQL:

```sql
CREATE UNIQUE INDEX ux_c023_entitlement_context_current
  ON c023_entitlement_context
  (organization_id, COALESCE(domain_id, '00000000-0000-0000-0000-000000000000'), entitlement_type_ref)
  WHERE effective_to IS NULL;
```

The all-zeros string literal is implicitly cast to `uuid` inside `COALESCE` (its sibling argument `domain_id` is `uuid`), so no explicit `::uuid` is required — the migration docstring's stated rationale is correct.

### 4. Migration — PASS

- `alembic heads` → `c3d4e5f6a7b8 (head)` — **single head**.
- `alembic history` → `f9a3c7e1b5d2 -> c3d4e5f6a7b8 (head), c023_license_context + c023_entitlement_context` ; prior link `b2c3d4e5f6a7 -> f9a3c7e1b5d2, membership_approval_authority` — **linear, no branch**.
- Migration file: `revision = 'c3d4e5f6a7b8'`, `down_revision = 'f9a3c7e1b5d2'`, `branch_labels = None`, `depends_on = None`.
- **Offline upgrade SQL (PostgreSQL):** `BEGIN;` → two `CREATE TABLE` (`c023_license_context`, `c023_entitlement_context`) → 3 + 4 `CREATE INDEX` (incl. the two partial-unique) → `UPDATE alembic_version` → `COMMIT;`. **No `ALTER` to any existing table.** `memberships` / `organizations` / `domains` / `approval_authorities` / `membership_approval_authority` are referenced by FK only, never modified — Decision 6 complied with by construction.
- **Offline downgrade SQL:** drops only the 4 entitlement indexes + `c023_entitlement_context`, then the 3 license indexes + `c023_license_context`, then reverts `alembic_version`. Nothing else touched.
- `models/__init__.py` diff registers `C023LicenseContext` and `C023EntitlementContext` (import + `__all__`). `main.py` diff registers `entitlement_license.router` at `/entitlement-license-contexts`.

### 5. Business logic / transaction (`TDS-C023 §14`/`§15`, `WP-17 §7`/`§9`) — PASS

`services/entitlement_license_establishment_service.py` read end-to-end:

- **Authority before any write.** The route (`routers/entitlement_license.py` line 87) gates with `Depends(require_approval_authority(COMMIT_AUTHORITY_NAME))` — the certified WP-18 dependency runs before the handler body. Inside `establish()`, the authorizing `approval_authorities` row is re-read (line 146, `get_active_by_organization_and_name`) **before** any anchor read or write; if it is gone → `_audit_denied` + 403 (fail closed on the race). The comment at lines 141–145 explicitly orders this before anchor reads "*before any read of the anchors that would let a caller probe existence*".
- **Anchors validated, 404 on missing.** `_validate_license_anchor` → `membership_repo.get_by_id`; `None` → `_audit_denied` + 404. `_validate_entitlement_anchor` → `organization_repo.get_by_id` / `domain_repo.get_by_id`; `None` → 404.
- **`status` always `'ACTIVE'`.** Hard-coded string literal at line 192 (license) and line 209 (entitlement). The request schema has **no** `status` field — a caller cannot supply it.
- **INV-C023-09 / -10 pre-check → create → `flush` → catch `IntegrityError` → `rollback` → 409.** `_validate_*_anchor` calls `get_current_for_membership` / `get_current_for_anchor` and raises 409 (`INV-C023-10` / `INV-C023-09` cited in the message) if a current row exists; the `try` block (lines 187–236) creates the row(s), `await self.license_repo.session.flush()`, and `except IntegrityError` → `await …rollback()` → `_audit_denied` → 409 with a "(concurrent establishment)" message. Exactly the `MembershipService.establish()` shape.
- **`approval_authority_id` from a re-read of the ACTIVE row; resolver not re-implemented.** `authority.id` (from `get_active_by_organization_and_name`) is stored on each context. `resolve_approval_authority()` is **not** called or re-implemented here — the route dependency owns the authorization decision; this service only records the id. Comment lines 143–145 and docstring lines 11–15 state this explicitly.
- **`committed_by_actor_id` = verified `person_id`.** Router passes `actor_id=claims.get("person_id")`; service writes `UUID(actor_id)`.
- **No suspend / revoke / reactivate path.** Grep (item 12) — those words appear only in the D-5 CHECK-constraint value list and in docstrings/messages stating they are out of scope. No code branch sets `status` to anything but `'ACTIVE'`, and `effective_to` is only ever the caller-supplied open-ended value or `None` — never set by a close operation.
- **`effective_to <= effective_from` → 422** (lines 134–138). Test `test_effective_to_must_be_after_effective_from` passes.
- **Dates never derived from a Subscription.** `effective_from = effective_from or now`; `effective_to` passed through as-is. No Subscription lookup anywhere in the service.

### 6. Entitlement path — Option A conformance — PASS

- `_RECOGNIZED_ENTITLEMENT_TYPE_REFS: frozenset[str] = frozenset()` (line 76) — a **genuinely empty** `frozenset()`. Not populated, not a disguised allowlist, not seeded from `URA-001-112` prose, not read from any table or config. The 14-line comment above it (lines 56–75) states it is the deliberate Decision 3 seam.
- Every Entitlement establish reaches `_validate_entitlement_anchor` line 388: `if entitlement_type_ref not in _RECOGNIZED_ENTITLEMENT_TYPE_REFS` → **always true** → `_audit_denied` + `HTTP_422_UNPROCESSABLE_ENTITY` whose message names "*the Global Entitlement Type / Feature Catalog (URA-001-113; IRA-C023 Decision 3) is deferred and not implemented … the Entitlement half of this Business Activity is vacuously blocked*". Test `test_entitlement_establish_is_vacuously_blocked` asserts 422 + `"Decision 3" in detail` + zero `c023_entitlement_context` rows — passes.
- **No** Entitlement Catalog table, no recognized-type-creation code, no Decision 3 or Decision 4 code anywhere in the change set (grep item 12; migration creates no catalog table; `TDS-C023-A §3.3` absences confirmed).

### 7. Approval Authority — WP-18 consumed unchanged — PASS

- `git diff HEAD` of `services/approval_authority_resolver.py`, `dependencies.py`, `models/membership_approval_authority.py`, `repositories/membership_approval_authority_repository.py`, `repositories/approval_authority_repository.py`, `middleware/tenant.py` → **empty** (`git diff --stat` returned nothing for all six).
- `git status --short` for `TDS-018_C003_Approval_Authority_Runtime_Binding_Technical_Design.md`, `CERT-WP-18_*.md`, `VV-AUDIT-WP-18_*.md`, `RRA-WP-18_*.md` → **not listed** (byte-unchanged).
- Router gates with `require_approval_authority("Entitlement/License Commit Authority")` (via `COMMIT_AUTHORITY_NAME` constant, service line 42). This string matches `TDS-C023 §7.2` ("*Working name: `"Entitlement/License Commit Authority"`*") exactly.
- **No `PLATFORM_ADMIN` / `AUREX_ADMIN` bypass.** Not present in the router, service, or the consumed dependency. Test `test_admin_role_claim_does_not_bypass` (parametrized `PLATFORM_ADMIN`, `AUREX_ADMIN`) asserts 403 — passes.
- `get_active_by_organization_and_name` is a **pre-existing** method on the tracked `repositories/approval_authority_repository.py` (`git ls-files` confirms the file is tracked; the method is not in the WP-17 diff) — consumed, not added.

### 8. Security — fail-closed + tenant isolation (`CLAUDE.md §21.4`, `TDS-C023 §22`, `TDS-C023-A §6`) — PASS

**In code:**
- Authority verified before any write; deny-by-default at the route dependency and again on the service's authority re-read (Finding 5).
- License establish: `_validate_license_anchor` line 343 — `if membership.organization_id != target_organization_id` → `_audit_denied` + **403**. (`target_organization_id` = the `X-Tenant-ID`-derived tenant from `get_current_tenant`, independent of caller claims.)
- Entitlement establish: `_validate_entitlement_anchor` line 380 — `if organization_id != target_organization_id` → `_audit_denied` + **403**.
- Outcome `GET` (`get_context_for_tenant`, lines 282–306): a context whose governing Organization ≠ `target_organization_id` → **404** ("No such context."), never 403 — verified for both the license branch (via `membership.organization_id`) and the entitlement branch (via `organization_id`), and for the not-found case.
- The establish/GET routes are **not** in `middleware/tenant.py`'s exemption list (read in full, lines 220–247) — `/entitlement-license-contexts` is absent, so `X-Tenant-ID` is mandatory; a missing header → 400 (`test_missing_tenant_header_is_400` passes).
- **No secret material in audit `metadata`.** `_audit_denied` metadata = `{"reason": <string>}`; `_audit_established` metadata = kind / context_id / approval_authority_id / organization_id / anchor ids / effective dates / status / source reference. No raw JWT, `Authorization` header, JWT secret, or password. `test_establish_emits_success_audit` asserts the metadata shape.

**From-scratch runtime probe** (`tests/_cert_wp17_probe.py` — written for this certification, uses the repo's `conftest.py` `client` / `db_session` fixtures, run with `JWT_SECRET_KEY=test-secret-key-not-for-production DATABASE_URL=postgresql+asyncpg://u:p@localhost/db ./venv/Scripts/python.exe -m pytest`; then deleted):

```python
async def _org(db, code):
    # Role + Organization + Person + Membership(FULL) + ApprovalAuthority(ANY_ONE, ACTIVE)
    # + MembershipApprovalAuthority binding, all committed
    ...
async def test_cert_probe_cross_org_establish_and_read(client, db_session):
    oa, pa, ma, aa = await _org(db_session, "CERT-A")
    ob, pb, mb, ab = await _org(db_session, "CERT-B")
    # establish a License in Org A (baseline) -> 201
    r  = client.post("/entitlement-license-contexts", json={"membership_id": str(ma.id)},
                     headers={"Authorization": f"Bearer {_tok(pa,oa,ma)}", "X-Tenant-ID": str(oa.id)})
    assert r.status_code == 201
    a_ctx = r.json()["license"]["id"]
    # Org-A caller, X-Tenant-ID=A, supplies Org B's membership_id -> 403, zero Org-B rows
    r2 = client.post("/entitlement-license-contexts", json={"membership_id": str(mb.id)},
                     headers={"Authorization": f"Bearer {_tok(pa,oa,ma)}", "X-Tenant-ID": str(oa.id)})
    assert r2.status_code == 403
    assert (rows for mb.id) == []
    # Org-B caller GETs Org A's context id -> 404 (not 403)
    r3 = client.get(f"/entitlement-license-contexts/{a_ctx}",
                    headers={"Authorization": f"Bearer {_tok(pb,ob,mb)}", "X-Tenant-ID": str(ob.id)})
    assert r3.status_code == 404
    assert total license rows == 1
```

Verbatim result:

```
cross-org establish status: 403 {"detail":"Membership '56eacb36-…' belongs to a different Organization than the X-Tenant-ID this request is scoped to."}
cross-org read status: 404 {"detail":"No such context."}
PROBE PASS: 403 on cross-org establish, 0 Org-B rows; 404 on cross-org read; 1 total row
1 passed
```

The audit log emitted during the probe shows the WP-17 `DENIED` record with `tenant_id` = the Org-A UUID and `metadata.reason = "membership belongs to a different Organization"` — no secret material.

### 9. Testing (`WP-17 §18`, `TDS-C023 §21`, `CLAUDE.md §21.4`) — PASS

`tests/test_entitlement_license_establishment.py` read in full — **23 tests**:

- **§21.4 checklist:** `test_two_unrelated_orgs_have_no_shared_row` (two distinct unrelated Organizations, each own authority/binding/membership, no shared row; distinct authority ids asserted); `test_caller_cannot_read_foreign_org_context` (cross-Organization visibility probe → 404, not 403); `test_caller_cannot_establish_license_for_foreign_membership` (explicit foreign-`membership_id` probe — caller bound in Org A supplies Org B's `membership_id`; clears the dependency, then service rejects the cross-Org anchor → 403, zero rows).
- **Negative control — Approval Authority denies by default:** `test_denied_when_no_authority_configured` (no `approval_authorities` row → 403); `test_denied_when_caller_has_no_binding` (no `membership_approval_authority` → 403); `test_denied_for_unsupported_majority_strategy` (`MAJORITY` → 403 + `"UNSUPPORTED_STRATEGY"`); `test_admin_role_claim_does_not_bypass` (parametrized `PLATFORM_ADMIN` / `AUREX_ADMIN` → 403); `test_missing_authorization_header_is_400`; `test_missing_tenant_header_is_400`.
- **Concurrent-establish race test exercising the partial unique index:** `test_partial_unique_index_is_the_race_backstop` — commits a current row, monkeypatches the pre-check to return `None` (the race window), establishes again through the real API → 409, one row remains (the raced insert rolled back).
- Plus: happy path, default `effective_from`, open-ended `effective_to`, resulting-outcome `GET`, unknown-context `GET` → 404, `INV-C023-10` duplicate → 409, `effective_to <= effective_from` → 422, `c023_license_type ∈ {FULL, LIGHT, junk}` → 422, Decision 6 (`memberships.license_type` still `FULL`; no C-023 attribute holds `FULL`/`LIGHT`), Entitlement vacuously blocked → 422 citing Decision 3, Entitlement `organization_id ≠ X-Tenant-ID` rejected, success audit emitted.

**Targeted re-run** (`./venv/Scripts/python.exe -m pytest tests/test_entitlement_license_establishment.py -q`): **`23 passed, 6 warnings in 7.85s`**.

**Full AuthService regression re-run** (`./venv/Scripts/python.exe -m pytest -q`, ~4 min): **`876 passed, 57 warnings in 235.23s` — 0 failed**. Matches the `IMP-REPORT-WP-17 §11.4` claim of "876 passed" (853 pre-existing + 23 new). The 57 warnings are pre-existing `HTTP_422_UNPROCESSABLE_ENTITY` deprecation notices consistent with the rest of the codebase's current style — not introduced by WP-17 as failures.

### 10. Frontend — exactly the two authorized items (`TDS-C023 §17`, `IRA-C023` Decision 5, `WP-17 §21`, `CLAUDE.md §20.3`–`§20.6`) — PASS

- `EntitlementLicenseManagementScreen.tsx` composes exactly **(1)** `EstablishEntitlementLicenseSection` and **(2)** `EntitlementLicenseOutcomeSection`. **No** admin console, **no** Consumption / Allocation / Catalog / Billing / Subscription UI, **no** list/search view. `entitlement-license-api.ts` exposes only `establishEntitlementLicenseContext` (POST) and `getEntitlementLicenseOutcome` (GET `/{id}`) — its own comment states "*WP-17 BA-01 charters no list/search endpoint, so none is called here*".
- Only existing `@/components/ui/*` primitives are imported (`Button`, `Input`, `Spinner`, `StatusBadge`, `Card`, `Form*`, `PageHeader`). **No new DS-001 component / token / theme** — so no `IMP-REPORT-WP-17 §4(2)` STOP-and-report was owed.
- `§20.6` states present: **loading** (`Spinner` + `isLoading` disabling fieldsets/buttons; "Loading…" text on the outcome section), **empty** (`state.status === "idle"` → "Enter a Context ID to see its outcome."; the "Enter a Membership ID … or both" helper when no anchor is entered), **validation** (`entitlementIncomplete` + `aria-invalid` + inline "Required when an Organization ID is provided."; `canSubmit` gating; `required` on the Context ID input), **error** (`FormBanner tone="danger"`; distinct auth-denied / conflict / generic messages driven by HTTP 403 / 409 / other), **confirmation** (`state.status === "established"` → `FormBanner tone="success"` "Establishment committed." + an `EstablishedRow` summary with status badge). Real API integration via the shared `apiClient` (attaches `Authorization` + `X-Tenant-ID`) — no mocked response, no stubbed call.
- `types/entitlement-license.ts` mirrors `schemas/entitlement_license.py` field-for-field: `EstablishEntitlementLicenseRequest` (8 fields, all optional-nullable, same names), `LicenseContextResponse` (11 fields), `EntitlementContextResponse` (11 fields), `EstablishEntitlementLicenseResponse` (`license` / `entitlement`), `ContextOutcomeResponse` (`kind` / `license` / `entitlement`). No field added, renamed, or omitted.
- `cd source/frontend && npx tsc --noEmit` → **exit 0, no output**. `npx eslint src/features/entitlement-license src/services/entitlement-license-api.ts src/types/entitlement-license.ts src/config/admin-navigation.ts` → **exit 0, no output**.
- `admin-navigation.ts` diff = **one additive** `AdminNavItem` (`slug: "entitlement-license"`, `href: "/platform-admin/subscriptions/entitlement-license"`), no existing item changed. The route file `app/platform-admin/(workspace)/subscriptions/entitlement-license/page.tsx` resolves (via the `(workspace)` route group) to URL path `/platform-admin/subscriptions/entitlement-license` — matches the nav `href`.

### 11. Demonstrability (`CLAUDE.md §20.4`) — PASS

BA-01 is demonstrable through the running application via the **License path**: a real persona (a caller who satisfies the `"Entitlement/License Commit Authority"` for their `X-Tenant-ID` Organization via a real `membership_approval_authority` binding) uses the real `EstablishEntitlementLicenseSection` form → real `POST /entitlement-license-contexts` → a real persisted `ACTIVE` `c023_license_context` row → the real `EntitlementLicenseOutcomeSection` renders the outcome from a real `GET /entitlement-license-contexts/{id}`. The independent runtime probe (Finding 8) exercised this end to end (201 + persisted row + retrievable outcome). The **Entitlement path**'s 422-citing-Decision-3 is the disclosed, Repository-Owner-approved (Option A, `IMP-REPORT-WP-17 §12.1`) scope boundary — a documented, sanctioned rejection, not a hidden gap.

### 12. Scope containment / no Decision 1–6 change / no excluded capability — PASS

- `git status --short` + `git diff --stat`: the only added/modified files carrying WP-17 content are exactly the declared change set — `models/c023_{license,entitlement}_context.py`, `repositories/c023_{license,entitlement}_context_repository.py`, `services/entitlement_license_establishment_service.py`, `schemas/entitlement_license.py`, `routers/entitlement_license.py`, `alembic/versions/2026_09_01_0900-c3d4e5f6a7b8_*.py`, `tests/test_entitlement_license_establishment.py`, `models/__init__.py`, `main.py`, `TDS-C023-A_*.md`, `STOP-AND-REPORT-WP-17-01_*.md`, `IMP-REPORT-WP-17_*.md`, `source/frontend/src/types/entitlement-license.ts`, `.../services/entitlement-license-api.ts`, `.../features/entitlement-license/**`, `.../app/platform-admin/(workspace)/subscriptions/entitlement-license/page.tsx`, `.../config/admin-navigation.ts`.
- The other 9 modified tracked files (`CLAUDE.md`, `CAP-001`, `SER-001`, `ADR-002`, `CANONICAL-ENTERPRISE-SEARCH…`, `MASTER-CAPABILITY…MAP`, and the untracked `ROD-*` / `ADR-027…035` / `IRA-C114` / `.xlsx` / `.png`) — `git diff | grep -iE "c-023|wp-17|entitlement|licens"` returned **nothing** for each. Confirmed unrelated C-040 / ROD / ADR working-tree noise, correctly outside this certification's scope.
- WP-17 did **not** modify: the `memberships` model/table/service (no `ALTER memberships`, confirmed by the offline upgrade SQL); `TDS-C023`; `IRA-C023` Decisions §18.13/§19.13/§20.12/§21.12/§22.13/§23.13 (unchanged); the `WP-17` charter *since R8* (see Finding 13); `WPR-001` (unmodified in the working tree — `git status --short` blank); `TDS-C023-A §19.1` decision text (byte-unchanged per `IMP-REPORT-WP-17 §13`); `ADR-036` (unmodified, Status: Accepted); `Master_Technical_Architecture.md`; `URA-001`; any C-040/WP-16/WP-18 artifact.
- **No new service boundary** — all code in `AuthService` per `ADR-036`. **No** Consumption/Allocation/Catalog/Billing/Subscription/cross-tenant-sharing/offboarding/C-020–C-025 code; **no** Authorization-Engine tier resolver; **no** Group infrastructure; **no** `AuthorityHolder` change; **no** `ALTER memberships`.

### 13. Governance-document currency — **MATERIAL DEFECT (M-1 class)**

The task instruction for this item is: check whether the `WP-17` charter Status line, `WPR-001`'s WP-17 row, `IRA-C023 §16`, and `IMP-REPORT-WP-17`'s own status lines are consistent with "IMPLEMENTATION COMPLETE, entering §19.7b certification"; report any non-struck present-tense staleness; and treat it as a certification failure **only if it is a live self-contradiction of the kind that failed WP-18's first Gate 1 ("M-1")**. It is.

**`IMP-REPORT-WP-17`** — consistent. `§6` carries the current non-struck status "**IMPLEMENTATION COMPLETE … NOT CERTIFIED. No `CLAUDE.md §19.7b` gate has been dispatched.**" with the two earlier "NOT STARTED" lines struck. `§11`–`§13` record the completed implementation and its evidence. *(Minor: `§6`/`§12` say "No `CLAUDE.md §19.7b` gate has been dispatched" and "before Gate 1" — technically now superseded by this Gate 1 running, but this is expected drafting-time phrasing in the report that *initiates* the gate, not a status-of-record contradiction; not part of the material finding.)*

**`WP-17` charter** (`architecture/05-Implementation/WP-17_C023_BA-01_Establish_Entitlement_License_Context_Business_Activity_Charter.md`) — **STALE, non-struck, present-tense:**
- **Line 6 (the header `**Status:**` field — the Work Package's primary status of record):** after the R8 supersession it reads "**CHARTERED — IMPLEMENTATION AUTHORIZED (2026-09-01 …), NOT YET COMPLETE, NOT CERTIFIED.**" followed by the non-struck parenthetical "*(updated 2026-09-01: Implementation Authorization has now occurred …; **implementation itself has not started**, and no `CLAUDE.md §19.7b` gate has been dispatched.)*"
- **Line 179 ("Final state"):** non-struck — "**BA CHARTERED. IMPLEMENTATION AUTHORIZED … NOT YET COMPLETE. NOT CERTIFIED.** **Implementation has not started; no `CLAUDE.md §19.7b` gate has been dispatched.**"

**`WPR-001` WP-17 row** (`architecture/00-Governance/WPR-001_Work_Package_Roadmap.md` line 55 — **unmodified in the working tree**, `git status --short` blank; last touched by commit `c2f93d5`, the R8 authorization-recording pass) — **STALE, non-struck, bolded, present-tense:**
- "**CHARTERED — IMPLEMENTATION AUTHORIZED (2026-09-01 …), NOT YET COMPLETE, NOT CERTIFIED.** … **Implementation has NOT started; no `CLAUDE.md §19.7b` gate has been dispatched.**"
- "**No implementation code, schema, migration, router, service, repository, model, test, or frontend component exists for C-023. Not started; not implementation-complete; no C-023 Gate 1/2/5 has been dispatched or passed.**"
- Final column: "**None — no Gate 1/2/5 has been dispatched.**"

**`IRA-C023 §16`** — the R8 addendum (non-struck): "**WP-17 is authorized but NOT implemented and NOT certified — no `CLAUDE.md §19.7b` gate has been dispatched; implementation has not started.**" *(The §16 capability-wide **🔴 RED** classification itself is correctly unchanged and is **not** part of this finding — BA-01 passing gates does not change C-023's capability-wide readiness. Only the "not implemented / no gate" clause is stale.)*

**Why this is M-1 class, not a mere observation.** `IMP-REPORT-WP-17 §13` explicitly lists "*the `WP-17` charter; `WPR-001`*" under **"Not modified"** for the D-7 implementation-resume pass — i.e. the Work Package's status-of-record documents were deliberately **not** reconciled with completed implementation before Gate 1 was dispatched. The result is a set of flat, bolded, present-tense factual assertions in the **Work Package Roadmap** and the **Business Activity Charter** ("*No implementation code, schema, migration, router, service, repository, model, test, or frontend component exists*"; "*Implementation has not started*"; "*no … gate has been dispatched*") that are **directly, presently false**: every one of those components exists in the working tree (Findings 2–10), `IMP-REPORT-WP-17` itself says "IMPLEMENTATION COMPLETE", and Gate 1 is running. This is materially identical to the finding that returned **NOT CERTIFIED** at WP-18's first Gate 1 attempt, recorded at `CERT-WP-18` line 6 / `WPR-001` line 69: "*this row and the charter had not yet been reconciled with the granted authorization and completed implementation at the time of that attempt — a governance-documentation contradiction, not a code defect (the certifier found none)*". The prior WP-18 pattern is the governing precedent: reconcile the charter + `WPR-001` row (strikethrough-preserve + a new reconciliation section) to "IMPLEMENTATION COMPLETE — NOT YET CERTIFIED — entering `CLAUDE.md §19.7b`", **then** re-dispatch Gate 1.

Per this gate's STOP conditions, this is a **live non-struck stale-status self-contradiction (M-1 class)** → **NOT CERTIFIED**. The reviewer did **not** modify these documents (the Repository Owner instruction: do not silently modify governance documents to make a gate pass). **A separate governance-reconciliation pass is required** before Gate 1 can be re-attempted.

---

## MATERIAL vs NON-MATERIAL FINDINGS

### Material findings

**M-1 (this gate) — Live, non-struck, stale-status self-contradiction in the WP-17 status-of-record governance documents.** The `WP-17` charter header **Status:** line and "Final state" line, the `WPR-001` WP-17 row (all non-struck, present-tense, one bolded as an absolute: "*No implementation code, schema, migration, router, service, repository, model, test, or frontend component exists for C-023*"), and the `IRA-C023 §16` R8 addendum clause "*implementation has not started; no `CLAUDE.md §19.7b` gate has been dispatched*" all assert that WP-17 implementation has not started and is not complete, while (a) the full BA-01 implementation exists in the working tree, (b) `IMP-REPORT-WP-17 §6`/`§11`/`§13` records "IMPLEMENTATION COMPLETE", and (c) Gate 1 has been dispatched. `IMP-REPORT-WP-17 §13` confirms the charter and `WPR-001` were deliberately left un-reconciled. This is the same class of governance-documentation contradiction that returned NOT CERTIFIED at WP-18's first Gate 1 ("M-1"). **No code, security, design-conformance, test, build, tenant-isolation, or scope defect underlies it** — the technical implementation passed every other checklist item. **Remediation:** a governance-reconciliation pass (strikethrough-preserve + a new reconciliation section) bringing the charter Status/Final-state lines, the `WPR-001` WP-17 row, and the stale `IRA-C023 §16` clause into agreement with `IMP-REPORT-WP-17`'s "IMPLEMENTATION COMPLETE — NOT YET CERTIFIED — entering `CLAUDE.md §19.7b`" status (the **🔴 RED** capability-wide classification and Decisions 1–6 explicitly unchanged), then re-dispatch Gate 1.

No other material finding. Specifically, **no `CLAUDE.md §19.8.5`-class defect** was found: no architectural defect, no security defect, no data-integrity defect, no tenant-isolation defect, no failing test, no build failure, no broken functionality; **no design non-conformance to the approved D-1…D-6 or `TDS-C023 §14`**; **no out-of-scope implementation** (no excluded capability, no Decision 1–6 change, no new service boundary, no interim recognized-type set — `_RECOGNIZED_ENTITLEMENT_TYPE_REFS` is a genuinely empty `frozenset()`).

### Non-material observations

**O1 (Low) — D-4 partial-unique-index expression omits the explicit `::uuid` cast shown in `TDS-C023-A §19.2`.** `§19.2` records the approved expression as `COALESCE(domain_id, '00000000-0000-0000-0000-000000000000'::uuid)`; the implemented `models/c023_entitlement_context.py` and the migration use `COALESCE(domain_id, '00000000-0000-0000-0000-000000000000')` (no cast). The migration docstring (lines 29–48) and the model module comment (lines 24–40) both document the **exact** implemented expression and the rationale (PostgreSQL implicitly casts the string literal to `uuid` inside `COALESCE` because the sibling argument is `uuid`; SQLite round-trips `domain_id` as a hex string and the 36-char sentinel is always distinct). The Repository Owner's D-4 condition — "*the implementation-time migration/design documents the exact expression and demonstrates cross-dialect correctness*" — is met: documented in two places, PostgreSQL offline DDL is syntactically valid (Finding 3), SQLite behaviour empirically verified by the reviewer's from-scratch probe (Finding 3). Functionally equivalent; not a defect. Recommendation: at a convenient documentation pass, either add the `::uuid` cast to match `§19.2` verbatim, or annotate `§19.2` that the implemented form deliberately relies on the documented implicit cast.

**O2 (Low) — `STOP-AND-REPORT-WP-17-01` header still reads "Status: AWAITING REPOSITORY OWNER / ARCHITECTURAL DECISION".** The schema-shape question it raised was answered at `TDS-C023-A §19.1` and recorded at `IMP-REPORT-WP-17 §9`. `IMP-REPORT-WP-17 §10`/`§13` lists the STOP-and-report under "Not modified" across every subsequent pass, so it is referenced as a historical point-in-time artifact and the resolution is unambiguous elsewhere. It is not a Work-Package status-of-record the way the charter and `WPR-001` row are, so it does not by itself constitute the M-1 finding — but the same reconciliation pass that fixes M-1 should annotate this header (strikethrough-preserve) as resolved.

**O3 (Low) — `TDS-C023-A §19.3`/`§20` status lines describe the schema-recording pass's end state.** They state "WP-17 / BA-01 = IMPLEMENTATION AUTHORIZED — IMPLEMENTATION HALTED" as the status "at the close of this recording pass". They are explicitly time-boxed to that pass and are superseded by `IMP-REPORT-WP-17 §11`, but a reader landing on `TDS-C023-A` first sees a stale-looking status. Recommendation: the M-1 reconciliation pass should add a one-line forward pointer from `TDS-C023-A §19.3` to `IMP-REPORT-WP-17 §11`–§13.

**O4 (informational) — `HTTP_422_UNPROCESSABLE_ENTITY` deprecation warnings.** The service and router use `status.HTTP_422_UNPROCESSABLE_ENTITY`, which Starlette now deprecates in favour of `HTTP_422_UNPROCESSABLE_CONTENT`. This matches the current style throughout the AuthService codebase (57 identical warnings across the full regression run, the vast majority pre-existing) and is not a WP-17-introduced regression. Cosmetic; a codebase-wide cleanup item, not a WP-17 gate concern.

---

## DETERMINATION LINE

**NOT CERTIFIED** — Gate 1 of 5 (`CLAUDE.md §19.7b`). One MATERIAL DEFECT: **M-1 — a live, non-struck, stale-status self-contradiction** between the WP-17 status-of-record governance documents (`WP-17` charter Status/Final-state lines; `WPR-001` WP-17 row, including the absolute "*no implementation code … exists for C-023*"; the stale clause of `IRA-C023 §16`) and the actual repository state (`IMP-REPORT-WP-17 §6`/`§11`/`§13` = "IMPLEMENTATION COMPLETE"; the full BA-01 change set present in the working tree; Gate 1 dispatched). This is the same class of governance-documentation contradiction that returned NOT CERTIFIED at WP-18's first Gate 1 attempt. **No `CLAUDE.md §19.8.5`-class code / security / data-integrity / tenant-isolation defect, no failing test, no build failure, no broken functionality, no D-1…D-6 or `TDS-C023 §14` design non-conformance, and no out-of-scope implementation was found** — the technical implementation of WP-17 / BA-01 is sound and passed every other certification-checklist item (Findings 1–12). Remediation is a governance-reconciliation pass (no code change), after which Gate 1 may be re-dispatched.

---

## APPENDIX — `git status --short` / `git diff --check`

### Before (certification start) and After (certification end) — identical; the reviewer created only this one file

`git rev-parse HEAD` → `c2f93d55daa6806939d98c389f5edcd73993ac60` (unchanged).

`git diff --check` → no whitespace errors, no conflict markers (only pre-existing CRLF-normalisation `warning:` lines).

`git status --short` **before** (WP-17 change set + pre-existing unrelated noise; the pre-existing `ROD-*` / `ADR-027…035` / `IRA-C114` / `.xlsx` / `.png` untracked entries are elided here for length and are not part of WP-17):

```
 M Backend/Services/AuthService/main.py
 M Backend/Services/AuthService/models/__init__.py
 M CLAUDE.md                                                        (pre-existing, unrelated)
 M architecture/02-Constitutional/CAP-001_Enterprise_Capability_Registry.md          (pre-existing, unrelated)
 M architecture/05-Implementation/IMP-REPORT-WP-17_Establish_Entitlement_License_Context.md
 M architecture/06-Reviews/CANONICAL-ENTERPRISE-SEARCH-ARCHITECTURE-SPECIFICATION.md (pre-existing, unrelated)
 M architecture/06-Reviews/MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md           (pre-existing, unrelated)
 M architecture/06-Reviews/SER-001_Strategic_Enhancement_Register.md                 (pre-existing, unrelated)
 M architecture/07-Decisions/ADR-002_AuthService_Seed_Role_Catalog_Reconciliation.md (pre-existing, unrelated)
 M source/frontend/src/config/admin-navigation.ts
?? Backend/Services/AuthService/alembic/versions/2026_09_01_0900-c3d4e5f6a7b8_c023_license_entitlement_context.py
?? Backend/Services/AuthService/models/c023_entitlement_context.py
?? Backend/Services/AuthService/models/c023_license_context.py
?? Backend/Services/AuthService/repositories/c023_entitlement_context_repository.py
?? Backend/Services/AuthService/repositories/c023_license_context_repository.py
?? Backend/Services/AuthService/routers/entitlement_license.py
?? Backend/Services/AuthService/schemas/entitlement_license.py
?? Backend/Services/AuthService/services/entitlement_license_establishment_service.py
?? Backend/Services/AuthService/tests/test_entitlement_license_establishment.py
?? architecture/05-Implementation/STOP-AND-REPORT-WP-17-01_Entitlement_License_Registry_Schema_Shape.md
?? architecture/05-Implementation/TDS-C023-A_Entitlement_License_Registry_Schema.md
?? source/frontend/src/app/platform-admin/(workspace)/subscriptions/entitlement-license/
?? source/frontend/src/features/entitlement-license/
?? source/frontend/src/services/entitlement-license-api.ts
?? source/frontend/src/types/entitlement-license.ts
   … plus pre-existing unrelated untracked C-040 / ROD-* / ADR-027…035 / IRA-C114 / .xlsx / .png entries (not WP-17)
```

`git status --short` **after**: identical to the above **plus** this one new untracked file:

```
?? architecture/06-Reviews/CERT-WP-17_Establish_Entitlement_License_Context.md
```

Nothing was staged, committed, or pushed. No file other than this artifact was created or modified. Gate 2 was not started.

---

*End of Gate 1 certification. Determination: **NOT CERTIFIED** — one material defect (M-1 governance-documentation staleness); technical implementation sound and otherwise passing. Independent, fresh-context reviewer; every material claim re-derived from primary sources; two purpose-built runtime probes written from scratch, run, and deleted.*

---
---

## Gate 1 Re-Certification (fresh independent reviewer, post-R9) — 2026-09-01

### Reviewer independence statement

This re-certification was produced by a **second, genuinely independent, fresh-context reviewer** with **no** access to any prior session's conversation and **no** involvement in: WP-17's implementation; the drafting of `TDS-C023` / `TDS-C023-A` / `STOP-AND-REPORT-WP-17-01` / the `WP-17` charter / `IMP-REPORT-WP-17`; the **first Gate 1 attempt** recorded above; the **R9 governance-documentation reconciliation pass**; or R9's own independent review. Every material claim below was **re-derived from primary sources** — actual files opened, actual commands run, purpose-built runtime probes written from scratch and executed. No prior report's conclusion (including the first Gate 1 attempt above and the R9 reconciliation result) was accepted on trust. The **current** working-tree state was assessed.

### State certified

- `git rev-parse HEAD` → `c2f93d55daa6806939d98c389f5edcd73993ac60` (`main`) — unchanged from the first attempt.
- All WP-17 work (implementation + the R9 governance edits) is **uncommitted in the working tree** — nothing staged, nothing committed. This re-certification isolates and certifies the **WP-17 change set only**, exactly as `CERT-WP-18` / `CERT-WP-16` certified an uncommitted working tree. The working tree also carries a large body of pre-existing, unrelated C-040 / ROD / `ADR-027…035` / `IRA-C114` / `Sarika_consent.png` / `Master_Platform_Capability_Delivery_Map.xlsx` noise — verified (item 16) to carry **zero** WP-17 / C-023 content.
- `git status --short` → 96 entries before this appendix (WP-17 change set + the pre-existing unrelated noise); 96 after (this file was already untracked from the first attempt — editing it adds no new entry).
- `git diff --check` → no whitespace errors, no conflict markers (only pre-existing CRLF-normalisation `warning:` lines).

### Scope and Method

**Commands run** (from `C:\Ashit\corpstage-enterprise-operating-system`, or `Backend/Services/AuthService` where noted):

| # | Command | Purpose |
|---|---|---|
| 1 | `git rev-parse HEAD`; `git status --short`; `git diff --check` | Capture certified state |
| 2 | `git diff -- Backend/.../main.py models/__init__.py source/frontend/.../admin-navigation.ts` | Verify the three tracked-file backend/nav edits (all additive) |
| 3 | `git diff --stat HEAD -- <6 WP-18 consumed files>` | Confirm WP-18 consumed-unchanged (empty) |
| 4 | `git status --short -- <TDS-018/CERT/VV-AUDIT/RRA-WP-18>` | Confirm byte-unchanged (empty) |
| 5 | `./venv/Scripts/python.exe -m alembic heads` ; `alembic history` | Single head `c3d4e5f6a7b8`; linear `f9a3c7e1b5d2 -> c3d4e5f6a7b8` |
| 6 | `DATABASE_URL=postgresql+asyncpg://… alembic upgrade --sql f9a3c7e1b5d2:c3d4e5f6a7b8` ; `downgrade --sql …` | Offline PostgreSQL DDL, both directions |
| 7 | `./venv/Scripts/python.exe -m pytest tests/test_entitlement_license_establishment.py -q` | Targeted suite → **23 passed** |
| 8 | `./venv/Scripts/python.exe -m pytest -q` (full AuthService regression) | **876 passed, 0 failed, 57 warnings in 305.72s** |
| 9 | `./venv/Scripts/python.exe -m pytest tests/zz_cert_wp17_reattempt_probe.py -q -s` (purpose-built, uses repo `conftest.py` `client`/`db_session` fixtures; created, run, **deleted**) | Independent cross-tenant + D-4 runtime probe |
| 10 | `cd source/frontend && npx tsc --noEmit` ; `npx eslint <entitlement-license change set>` | Frontend type/lint — both exit 0, no output |
| 11 | `grep -rniE "<excluded-capability tokens>" <WP-17 backend change set>` | Excluded-capability / interim-recognized-type scan |
| 12 | `grep -nE "<stale-status phrases>" <WP-17 charter, WPR-001, IRA-C023, IMP-REPORT-WP-17, TDS-C023-A, STOP-AND-REPORT-WP-17-01>` | Item 20 residual-M-1 sweep |
| 13 | `git diff -- IRA-C023…md \| grep '^@@\|^[+-]'` | Confirm only the §16 R9 addendum area changed; Decision sections absent from every hunk |
| 14 | `git diff -- <6 unrelated modified governance docs> \| grep -icE "wp-17\|c-023\|entitlement.licen\|c023_"` | Scope-containment → **0** |

**Files read in full (or the cited sections):** the entire `CERT-WP-17` first-attempt section above; `WP-17` charter (all 196 lines, incl. §24 and every R3/R7/R8/R9 Change Control entry); `TDS-C023-A` (all 536 lines, incl. §3.1/§3.2, §19.0/§19.1/§19.2/§19.3, §20, Change Control incl. the R9 annotation); `IMP-REPORT-WP-17` (all 352 lines, incl. §1 verbatim authorization, §3 exclusions, §6, §11, §12+§12.1 verbatim Option A, §13, §14 first Gate 1 result, §15 R9 result); `STOP-AND-REPORT-WP-17-01` (header + tail, R9-annotated); `IRA-C023` §16 + the top Overall Classification + the R8/R9 addenda + the six Decision-section headers; `ADR-036` (Status: Accepted, Decision items 1/3/5/6/7); `WPR-001` WP-17 row + all five maintenance notes + the WP-18 row; backend change set (`models/c023_license_context.py`, `models/c023_entitlement_context.py`, the migration, both repositories, the service end-to-end, `schemas/entitlement_license.py`, `routers/entitlement_license.py`, `tests/test_entitlement_license_establishment.py`, the `main.py`/`models/__init__.py` diffs); frontend change set (`types/entitlement-license.ts`, `services/entitlement-license-api.ts`, `state/useEntitlementLicense.ts`, the three components, `page.tsx`, the `admin-navigation.ts` diff); `middleware/tenant.py` exemption block (read in full); `CLAUDE.md` §8/§16/§17/§18/§19 (incl. §19.7/§19.7b/§19.8.5/§19.8.7)/§20/§21.

**Purpose-built probe** (`tests/zz_cert_wp17_reattempt_probe.py` — created for this re-certification, run, then **deleted**; not added to the suite; `git status` for `tests/` shows only `test_entitlement_license_establishment.py` after deletion). Full source and verbatim output in Finding 7 below.

### Point-by-Point Findings (checklist items 1–20)

#### 1. BA-01 implementation complete — PASS

Model + migration + repositories + service + router + schemas + 23 tests + the two frontend items all present and wired. `models/__init__.py` diff registers `C023LicenseContext` + `C023EntitlementContext` (import + `__all__`). `main.py` diff registers `entitlement_license.router` at `prefix="/entitlement-license-contexts"`. Frontend: `types/`, `services/`, `features/entitlement-license/{state,components}/`, `app/platform-admin/(workspace)/subscriptions/entitlement-license/page.tsx`, and one additive `admin-navigation.ts` item — all present on disk.

#### 2. Approved two-table schema implemented EXACTLY (`TDS-C023-A §3.1`/`§3.2`/`§19.1` D-1…D-6) — PASS

Verified column-by-column in **both** the SQLAlchemy model and the Alembic migration, and cross-checked against the offline PostgreSQL DDL (Finding 3):

**`c023_license_context`** — `id` UUID PK (`pk_c023_license_context`, `default uuid4`); `membership_id` UUID NOT NULL, FK `memberships.id` (`fk_c023_license_context_membership_id`), indexed; `status` VARCHAR(20) NOT NULL + `CHECK (status IN ('ACTIVE','SUSPENDED','REVOKED'))`; `effective_from` TIMESTAMPTZ NOT NULL; `effective_to` TIMESTAMPTZ NULL; `entitlement_source_reference` VARCHAR(255) NULL; `approval_authority_id` UUID NOT NULL, FK `approval_authorities.id`, indexed; `committed_by_actor_id` UUID NOT NULL, **non-FK** (no `ForeignKeyConstraint`); `committed_at` TIMESTAMPTZ NOT NULL; `c023_license_type` VARCHAR(50) NULL + `CHECK (c023_license_type IS NULL OR c023_license_type IN ('SUPPLIER','AUDITOR','BOARD_MEMBER','CONSULTANT'))`; `created_at` NOT NULL / `updated_at` NULL `onupdate`; partial unique `ux_c023_license_context_current` on `(membership_id) WHERE effective_to IS NULL` (cross-dialect `postgresql_where` + `sqlite_where`).

**`c023_entitlement_context`** — `id` UUID PK; `organization_id` UUID NOT NULL, FK `organizations.id`, indexed; `domain_id` UUID NULL, FK `domains.id`; `entitlement_type_ref` VARCHAR(100) NOT NULL; `status` VARCHAR(20) NOT NULL + same CHECK; `effective_from` NOT NULL / `effective_to` NULL; `entitlement_source_reference` VARCHAR(255) NULL; `approval_authority_id` UUID NOT NULL, FK `approval_authorities.id`, indexed; `committed_by_actor_id` UUID NOT NULL **non-FK**; `committed_at` / `created_at` NOT NULL / `updated_at` NULL; non-unique `ix_c023_entitlement_context_org_type` on `(organization_id, entitlement_type_ref)`; partial unique `ux_c023_entitlement_context_current` on `(organization_id, COALESCE(domain_id, '00000000-0000-0000-0000-000000000000'), entitlement_type_ref) WHERE effective_to IS NULL` (cross-dialect).

The four hard intra-service FKs are exactly `memberships.id` / `approval_authorities.id` / `organizations.id` / `domains.id`; `committed_by_actor_id` is **non-FK** on both tables. Both `status` CHECKs and the `c023_license_type` CHECK are byte-identical model-vs-migration. **No `FULL`/`LIGHT` column or value anywhere** (every `FULL`/`LIGHT` grep hit is in a docstring, the disjoint `URA-001-115` four-value CHECK, or a rejection message); **no FK to `memberships.license_type`** (the `membership_id` FK targets row identity); **no** `version` / `supersedes_id` / `granted_capacity` / `consumption` / `available_capacity` / billing / price / currency / `aligned_to_subscription_id` / catalog-definition column (`TDS-C023-A §3.3`). **No deviation from D-1…D-6 found.** (One prior non-material observation — **O1**, the D-4 expression omits the `::uuid` cast shown in `TDS-C023-A §19.2` — is re-confirmed non-material below; the RO's D-4 condition, "documents the exact expression and demonstrates cross-dialect correctness", is met.)

#### 3. Migration integrity + single Alembic head — PASS

- `alembic heads` → `c3d4e5f6a7b8 (head)` — **single head**.
- `alembic history` → `f9a3c7e1b5d2 -> c3d4e5f6a7b8 (head), c023_license_context + c023_entitlement_context`; prior link `b2c3d4e5f6a7 -> f9a3c7e1b5d2` — **linear, no branch**.
- Migration file: `revision = 'c3d4e5f6a7b8'`, `down_revision = 'f9a3c7e1b5d2'`, `branch_labels = None`, `depends_on = None`.
- **Offline upgrade SQL (PostgreSQL dialect):** `BEGIN;` → `CREATE TABLE c023_license_context` → `ix_…_membership_id`, `ix_…_approval_authority_id`, `CREATE UNIQUE INDEX ux_c023_license_context_current … WHERE effective_to IS NULL` → `CREATE TABLE c023_entitlement_context` → `ix_…_organization_id`, `ix_…_approval_authority_id`, `ix_c023_entitlement_context_org_type`, `CREATE UNIQUE INDEX ux_c023_entitlement_context_current ON c023_entitlement_context (organization_id, COALESCE(domain_id, '00000000-0000-0000-0000-000000000000'), entitlement_type_ref) WHERE effective_to IS NULL` → `UPDATE alembic_version` → `COMMIT;`. **`TIMESTAMP WITH TIME ZONE`**, native **`UUID`**, the partial `WHERE` clauses, and the valid `COALESCE(...)` expression index are all present. **No `ALTER` to any existing table** — `memberships` / `organizations` / `domains` / `approval_authorities` are referenced by FK only.
- **Offline downgrade SQL:** drops the four entitlement indexes + `c023_entitlement_context`, then the three license indexes + `c023_license_context`, then reverts `alembic_version`. Nothing else.

#### 4. Repository / service / router — PASS (`TDS-C023 §14`/`§15`, `WP-17 §7`/`§9`)

`services/entitlement_license_establishment_service.py` read end to end:
- **Authority before any write.** Route (`routers/entitlement_license.py` line 87) gates with `Depends(require_approval_authority(COMMIT_AUTHORITY_NAME))`. Inside `establish()`, the authorizing `approval_authorities` row is re-read (`get_active_by_organization_and_name`, line 146) **before** any anchor read or write; if gone → `_audit_denied` + 403 (fail-closed on the race). The comment explicitly orders this "before any read of the anchors that would let a caller probe existence".
- **Anchors validated, 404 on missing.** `_validate_license_anchor` → `membership_repo.get_by_id`; `None` → 404. `_validate_entitlement_anchor` → `organization_repo.get_by_id` / `domain_repo.get_by_id`; `None` → 404.
- **`status` always `'ACTIVE'`.** Hard-coded string literal at service lines 192 (license) and 209 (entitlement). The request schema has **no** `status` field.
- **INV-C023-09/-10 pre-check → create → `flush` → catch `IntegrityError` → `rollback` → 409.** `_validate_*_anchor` calls `get_current_for_membership` / `get_current_for_anchor` and raises 409 (citing `INV-C023-10` / `INV-C023-09`) if a current row exists; the `try` block creates the row(s), `await self.license_repo.session.flush()`, `except _integrity_errors()` (= `sqlalchemy.exc.IntegrityError`) → `await …rollback()` → `_audit_denied` → 409 "(concurrent establishment)". Exactly the `MembershipService.establish()` shape.
- **`approval_authority_id` from the re-read ACTIVE row; resolver not re-implemented.** `authority.id` is stored on each context; `resolve_approval_authority()` is **not** called or re-implemented here — the route dependency owns the decision, the service only records the id (docstring lines 11–15).
- **`committed_by_actor_id` = verified `person_id`.** Router passes `actor_id=claims.get("person_id")`; service writes `UUID(actor_id)`.
- **No suspend/revoke/reactivate path** anywhere; `effective_to` is only ever the caller-supplied value or `None`.
- **`effective_to <= effective_from` → 422** (service lines 134–138); `test_effective_to_must_be_after_effective_from` passes.
- **Dates never derived from a Subscription** — `effective_from = effective_from or now`; `effective_to` passed through. No Subscription lookup.
- Repositories provide **only** the NULL-aware pre-check lookups (`get_current_for_membership`, `get_current_for_anchor`), each a plain `select … where … effective_to IS NULL`.

#### 5. Approval Authority enforcement through certified WP-18 — PASS

- `git diff --stat HEAD` for `services/approval_authority_resolver.py`, `dependencies.py`, `models/membership_approval_authority.py`, `repositories/membership_approval_authority_repository.py`, `repositories/approval_authority_repository.py`, `middleware/tenant.py` → **empty (zero changes)**.
- `git status --short` for `TDS-018_*`, `CERT-WP-18_*`, `VV-AUDIT-WP-18_*`, `RRA-WP-18_*` → **not listed (byte-unchanged)**.
- Router gates with `require_approval_authority("Entitlement/License Commit Authority")` via `COMMIT_AUTHORITY_NAME` (service line 42). This string matches `TDS-C023 §7.2` exactly.

#### 6. Fail-closed behavior — PASS

No default-allow path; authority verified before any write (route dependency + the service's own authority re-read). **No `PLATFORM_ADMIN` / `AUREX_ADMIN` bypass** in the router, service, or consumed dependency. Deny-by-default negative controls exist in the suite: `test_denied_when_no_authority_configured` (403), `test_denied_when_caller_has_no_binding` (403), `test_denied_for_unsupported_majority_strategy` (403 + `UNSUPPORTED_STRATEGY`), `test_admin_role_claim_does_not_bypass` (parametrized `PLATFORM_ADMIN` / `AUREX_ADMIN` → 403).

#### 7. Tenant isolation — bind-time AND read-time — PASS

**In code:** `/entitlement-license-contexts` is **absent** from `middleware/tenant.py`'s exemption list (read in full, lines 220–246) — `X-Tenant-ID` is mandatory; missing → 400 (`test_missing_tenant_header_is_400`). License establish: `_validate_license_anchor` line 343 — `membership.organization_id != target_organization_id` → `_audit_denied` + **403** (`target_organization_id` = the `X-Tenant-ID`-derived tenant from `get_current_tenant`, independent of caller claims). Entitlement establish: `_validate_entitlement_anchor` line 380 — body `organization_id != target_organization_id` → **403**. Outcome `GET` (`get_context_for_tenant`): a context whose governing Organization ≠ `target_organization_id` → **404** ("No such context."), never 403 — verified for both branches and the not-found case. `_audit_denied` metadata = `{"reason": <string>}` only; `_audit_established` metadata = kind / context_id / approval_authority_id / organization_id / anchor ids / effective dates / status / source reference — **no raw JWT, `Authorization` header, JWT secret, or password**.

**From-scratch runtime probe** (`tests/zz_cert_wp17_reattempt_probe.py`, run with `JWT_SECRET_KEY=test-secret-key-not-for-production DATABASE_URL=postgresql+asyncpg://u:p@localhost/db ./venv/Scripts/python.exe -m pytest`, then deleted). Probe body:

```python
async def test_probe_cross_tenant_and_d4(client, db_session):
    oa, pa, ma, aa = await _org(db_session, "PRB-A")   # Org + Person + Membership(FULL)
    ob, pb, mb, ab = await _org(db_session, "PRB-B")    # + ApprovalAuthority(ANY_ONE) + binding
    # 1. baseline: establish a License in Org A
    r = client.post("/entitlement-license-contexts", json={"membership_id": str(ma.id)},
                    headers={"Authorization": f"Bearer {_tok(str(pa.id), str(oa.id), str(ma.id))}",
                             "X-Tenant-ID": str(oa.id)})
    assert r.status_code == 201
    a_ctx = r.json()["license"]["id"]
    # 2. Org-A caller, X-Tenant-ID=A, supplies Org B's membership_id -> 403, no Org-B row
    r2 = client.post("/entitlement-license-contexts", json={"membership_id": str(mb.id)},
                     headers={"Authorization": f"Bearer {_tok(str(pa.id), str(oa.id), str(ma.id))}",
                              "X-Tenant-ID": str(oa.id)})
    assert r2.status_code == 403
    assert (await db_session.execute(select(C023LicenseContext)
            .where(C023LicenseContext.membership_id == mb.id))).scalars().all() == []
    # 3. Org-B caller GETs Org A's context id -> 404, not 403
    r3 = client.get(f"/entitlement-license-contexts/{a_ctx}",
                    headers={"Authorization": f"Bearer {_tok(str(pb.id), str(ob.id), str(mb.id))}",
                             "X-Tenant-ID": str(ob.id)})
    assert r3.status_code == 404
    assert len((await db_session.execute(select(C023LicenseContext))).scalars().all()) == 1
    # 4. D-4: two org-wide (domain_id NULL) entitlement rows, same type -> partial unique index collides
    # (two C023EntitlementContext(domain_id=None, entitlement_type_ref="PRB_TYPE", effective_to=None)
    #  flushed in sequence; second flush must raise IntegrityError)
```

Verbatim output (noise-filtered):

```
baseline establish: 201 {"license":{"id":"43ecfe21-…","membership_id":"cf759206-…","status":"ACTIVE", …
cross-org establish: 403 {"detail":"Membership '915a99d4-…' belongs to a different Organization than the X-Tenant-ID this request is scoped to."}
cross-org read: 404 {"detail":"No such context."}
D-4 collision: (sqlite3.IntegrityError) UNIQUE constraint failed: index 'ux_c023_entitlement_context_current'
PROBE PASS: 403 cross-org establish + 0 Org-B rows; 404 cross-org read; 1 total row; D-4 index collides on NULL domain
1 passed
```

The audit line emitted during the probe: `"status": "DENIED", … "metadata": {"reason": "membership belongs to a different Organization"}` — no secret material.

#### 8. Audit / observability — PASS

Every establish path calls `observability.record_audit(action="ESTABLISH_ENTITLEMENT_LICENSE_CONTEXT", …)` — `AuditStatus.SUCCESS` per established context (metadata: `kind`, `context_id`, `approval_authority_id`, `organization_id`, `anchor`, effective dates, `status`, `entitlement_source_reference`) + `publish_event("ENTITLEMENT_LICENSE_CONTEXT_ESTABLISHED", …)`; `AuditStatus.DENIED` on every rejection with a specific `reason`. No new audit subsystem. `test_establish_emits_success_audit` asserts the metadata shape; the probe (Finding 7) confirms the DENIED record carries no secret material.

#### 9. License path end-to-end demonstrability (`CLAUDE.md §20.4`) — PASS

The probe (Finding 7) exercised the full License path through the running app: a caller satisfying the `"Entitlement/License Commit Authority"` for their `X-Tenant-ID` Organization via a real `membership_approval_authority` binding → real `POST /entitlement-license-contexts` → **201** + a real persisted `ACTIVE` `c023_license_context` row → real `GET /entitlement-license-contexts/{id}` → **200** with the outcome. Frontend: `cd source/frontend && npx tsc --noEmit` → **exit 0, no output**; `npx eslint src/features/entitlement-license src/services/entitlement-license-api.ts src/types/entitlement-license.ts src/config/admin-navigation.ts` → **exit 0, no output**. The route file resolves (via the `(workspace)` route group) to `/platform-admin/subscriptions/entitlement-license`, matching the nav `href`.

#### 10. Entitlement path correctly vacuously blocked (Repository Owner Option A) — PASS

`services/entitlement_license_establishment_service.py` line 76: `_RECOGNIZED_ENTITLEMENT_TYPE_REFS: frozenset[str] = frozenset()` — a **genuinely empty** `frozenset()`, not populated, not seeded from `URA-001-112` prose, not read from any table or config (the 20-line comment above it, lines 56–75, states it is the deliberate Decision 3 seam). Every Entitlement establish reaches `_validate_entitlement_anchor` line 388: `if entitlement_type_ref not in _RECOGNIZED_ENTITLEMENT_TYPE_REFS` → **always true** → `_audit_denied` + `HTTP_422_UNPROCESSABLE_ENTITY` whose message names "*the Global Entitlement Type / Feature Catalog (URA-001-113; IRA-C023 Decision 3) is deferred and not implemented … the Entitlement half of this Business Activity is vacuously blocked*". `test_entitlement_establish_is_vacuously_blocked` asserts **422** + `"Decision 3" in detail` + **zero** `c023_entitlement_context` rows — passes.

#### 11. No interim recognized Entitlement Type set was invented — PASS

`grep -rniE "IFRS_ENABLED|ENTITLEMENT_ENABLED|AI_DISCOVERY|SUPPLIER_PORTAL|consumption|allocation|catalog|billing|subscription|supersedes|version|revoke|suspend|aligned_to" <WP-17 backend change set>` filtered to executable lines: **every** hit is a docstring, comment, the D-5-approved `status` CHECK value list, a field-description string, or a user-facing rejection message. No allowlist, seed file, config entry, or DB seed of entitlement-type identifiers exists anywhere in the change set.

#### 12. The two authorized frontend items ONLY — PASS

`EntitlementLicenseManagementScreen.tsx` composes exactly **(1)** `EstablishEntitlementLicenseSection` and **(2)** `EntitlementLicenseOutcomeSection` — no admin console, no Consumption / Allocation / Catalog / Billing / Subscription UI, no list/search. `entitlement-license-api.ts` exposes only `establishEntitlementLicenseContext` (POST) and `getEntitlementLicenseOutcome` (GET `/{id}`); its own comment: "*WP-17 BA-01 charters no list/search endpoint, so none is called here*". Only existing `@/components/ui/*` primitives imported (`Button`, `Input`, `Spinner`, `StatusBadge`, `Card`, `Form*`, `PageHeader`) — no new DS-001 component/token/theme. `§20.6` states present: **loading** (`Spinner` + `isLoading` disabling inputs/buttons), **empty** (`state.status === "idle"` → helper text), **validation** (`entitlementIncomplete` + `aria-invalid` + inline "Required when an Organization ID is provided."; `canSubmit` gating; `required` inputs), **error** (`FormBanner tone="danger"`, distinct 403/409/other messages), **confirmation** (`state.status === "established"` → `FormBanner tone="success"` "Establishment committed." + an `EstablishedRow` with `StatusBadge`). `types/entitlement-license.ts` mirrors `schemas/entitlement_license.py` field-for-field (`EstablishEntitlementLicenseRequest` 8 fields; `LicenseContextResponse` 11; `EntitlementContextResponse` 11; `EstablishEntitlementLicenseResponse`; `ContextOutcomeResponse`). `admin-navigation.ts` diff = **one additive** item (`slug: "entitlement-license"`, `href: "/platform-admin/subscriptions/entitlement-license"`), no existing item changed.

#### 13. Full test evidence, including the regression suite — PASS

- **Targeted:** `./venv/Scripts/python.exe -m pytest tests/test_entitlement_license_establishment.py -q` → **`23 passed, 6 warnings in 17.51s`** (expected 23).
- **Full AuthService regression:** `./venv/Scripts/python.exe -m pytest -q` → **`876 passed, 57 warnings in 305.72s (0:05:05)` — 0 failed**. Matches `IMP-REPORT-WP-17 §11.4` (853 pre-existing + 23 new). The 57 warnings are pre-existing `HTTP_422_UNPROCESSABLE_ENTITY` deprecation notices matching the codebase-wide style — not WP-17-introduced failures (**O4**, informational, re-confirmed).

#### 14. `TDS-C023 §21` V&V obligations applicable to BA-01 — PASS

`tests/test_entitlement_license_establishment.py` includes: **(a)** `CLAUDE.md §21.4` checklist — `test_two_unrelated_orgs_have_no_shared_row` (two distinct unrelated Organizations, each own authority/binding/membership, distinct authority ids, two independent rows); `test_caller_cannot_read_foreign_org_context` (cross-Organization visibility probe → 404, not 403); `test_caller_cannot_establish_license_for_foreign_membership` (explicit foreign-`membership_id` probe not derived from the caller's claims — clears the dependency, then the service rejects the cross-Org anchor → 403, zero rows). **(b)** negative control — deny-by-default (Finding 6). **(c)** concurrent-establish race — `test_partial_unique_index_is_the_race_backstop` (commits a current row, monkeypatches the pre-check to return `None` (the race window), establishes again through the real API → 409, one row remains). All pass.

#### 15. No Decision 1–6 modified or implicitly resolved — PASS

`git diff -- architecture/05-Implementation/IRA-C023_…md` produces **exactly one hunk** — `@@ -288,7 +288,9 @@`, inside `§16`: the R8 addendum's "WP-17 is authorized but NOT implemented and NOT certified … implementation has not started" clause wrapped in `~~…~~` with a dated superseding note, plus a new **R9 addendum**. The six Decision sections (`§18.13`/`§19.13`/`§20.12`/`§21.12`/`§22.13`/`§23.13`) do **not** appear in the diff. Independently re-read: their substantive content is unchanged. Nothing in the WP-17 change set implicitly resolves any Decision — the Entitlement path's empty recognized-type set (Finding 10) keeps Decision 3 as the sole trigger; no Consumption/Allocation code touches Decision 4.

#### 16. No excluded C-023 capability implemented — PASS

No Consumption/Allocation code or column; no Entitlement Catalog table or governance operation; no Subscription/temporal-alignment column; no Billing; no C-020/C-025 interface; no migration/offboarding; no cross-tenant sharing; no suspend/revoke/reactivate; no Authorization-Engine tier resolver; no `AuthorityHolder` change; no Group infrastructure; **no new service boundary** (all code in `AuthService`, `ADR-036` Status: Accepted); no `ALTER memberships` (confirmed by the offline upgrade SQL). `git diff -- <6 unrelated modified governance docs> | grep -icE "wp-17|c-023|entitlement.licen|c023_"` → **0** — the pre-existing C-040/ROD/ADR/C-114 working-tree noise carries no WP-17 content.

#### 17. WP-18 remains untouched — PASS

`git diff --stat HEAD` for every WP-18 code file → empty; `TDS-018` / `CERT-WP-18` / `VV-AUDIT-WP-18` / `RRA-WP-18` → not in `git status` (byte-unchanged). `WPR-001` WP-18 row is unchanged and still reads **CLOSED — CERTIFIED — RELEASE-READY** through all five gates.

#### 18. C-023 capability-wide remains 🔴 RED — NOT IMPLEMENTATION READY — PASS

`IRA-C023` line 19: "**Overall Classification: 🔴 RED — Not Implementation Ready.**" and line 269 heading "### 🔴 RED — Not Implementation Ready" — both **absent from the diff** (unchanged). The `§16` R8 addendum (now struck) and the new R9 addendum each explicitly restate "*this §16 **🔴 RED — Not Implementation Ready** capability-wide classification (unchanged)*". `IMP-REPORT-WP-17` §4/§7/§11.3/§13 and the `WP-17` charter's reconciled Status/Final-state lines all restate C-023 = 🔴 RED, unchanged.

#### 19. WP-17 governance documents now state IMPLEMENTATION COMPLETE / NOT YET CERTIFIED — PASS (with the item-20 exception below)

Current (post-R9) **live, non-struck** text:
- `WP-17` charter **header `Status:` line** → "**CHARTERED — IMPLEMENTATION AUTHORIZED — IMPLEMENTATION COMPLETE — NOT YET CERTIFIED**" (`IMP-REPORT-WP-17 §11`/`§14`); the R8-era "NOT YET COMPLETE / implementation itself has not started" text is struck with a dated R9 note.
- `WP-17` charter **"Final state" line** → "**BA CHARTERED. IMPLEMENTATION AUTHORIZED. IMPLEMENTATION COMPLETE … Independently reviewed SOUND. `CLAUDE.md §19.7b` Gate 1 has been dispatched and returned NOT CERTIFIED solely for the stale-status documentation this R9 pass reconciles … NOT YET CERTIFIED.**" — no claim of certification or of Gate 1 passing.
- `WPR-001` WP-17 row **main cell** → "**CHARTERED — IMPLEMENTATION AUTHORIZED — IMPLEMENTATION COMPLETE — NOT YET CERTIFIED.**"; **Gate column** → "**Gate 1 dispatched — NOT CERTIFIED (finding M-1 …). Gate 1 not yet re-dispatched. Gates 2/5 not dispatched.**"
- `IRA-C023 §16` **R9 addendum** → "**Current accurate status: WP-17 / BA-01 is IMPLEMENTATION AUTHORIZED — IMPLEMENTATION COMPLETE … — NOT YET CERTIFIED — entering the `CLAUDE.md §19.7b` certification sequence.** … This addendum does not itself certify WP-17."
- `IMP-REPORT-WP-17 §11` (line 305) / `§13` → "**IMPLEMENTATION AUTHORIZED — IMPLEMENTATION COMPLETE … INDEPENDENTLY REVIEWED SOUND — ENTERING `CLAUDE.md §19.7b` CERTIFICATION — NOT YET CERTIFIED.**"; `§15` records the R9 result and "**This pass does not itself certify WP-17.**"

None of these claims certification or that Gate 1 has passed. **However — see item 20: two of these same documents carry a *further*, un-reconciled stale assertion that R9 did not reach.**

#### 20. No stale "implementation has not started" status remains in ANY governing WP-17 document — **FAIL — RESIDUAL LIVE M-1**

Grep of the `WP-17` charter, `WPR-001`, `IRA-C023`, `IMP-REPORT-WP-17`, `TDS-C023-A`, `STOP-AND-REPORT-WP-17-01` for non-struck present-tense "implementation not started / not complete / no gate dispatched" assertions finds the following **still live (not inside `~~…~~`, no dated superseding note)**:

- **`WP-17` charter §24 (line 154), section titled "## 24. Implementation Status and Sequencing Disclosure":**
  > "**No implementation exists.** No production code, schema, migration, router, service, repository, model, or frontend component has been created for C-023 at any point, in this charter or any prior C-023 governance artifact. **Gates 1, 2, and 5 (`CLAUDE.md §19.7b`) have not been dispatched.**"

  Both bolded assertions are **directly, presently false**: the full BA-01 change set (models, migration, repositories, service, router, schemas, 23 tests, two frontend items) exists in the working tree (Findings 1–14), and Gate 1 has been dispatched **twice** (the first attempt above; this re-attempt). This is **materially identical in kind** to the first attempt's M-1 finding — indeed identical in wording to the `WPR-001` clause the first attempt quoted verbatim as its exemplar ("*No implementation code, schema, migration, router, service, repository, model, test, or frontend component exists for C-023*"). The R9 pass reconciled the charter's **header `Status` line and "Final state" line** (its own Change Control entry, line 195, lists only those two) and **did not reach §24**.

- **`WP-17` charter line 11 ("Governing basis for BA-01"):** "**No implementation exists at any point in this chain.**" — non-struck, present-tense, now false. Same finding, secondary instance (narrative context rather than a status field, but still a flat present-tense falsehood in the charter).

- **`TDS-C023-A §20 (line 510), bullet:** "*change C-023's capability-wide 🔴 RED status or WP-17's status* — **still true**: … **WP-17 remains IMPLEMENTATION AUTHORIZED — IMPLEMENTATION HALTED — NOT CERTIFIED**". Non-struck. The **closing paragraph of the same §20** (line 512) *was* reconciled by R9 with a struck old-status line and a dated "Current, authoritative status: … IMPLEMENTATION COMPLETE — NOT YET CERTIFIED" note — but this bullet's parenthetical "IMPLEMENTATION HALTED" was left live. Lesser weight (it appears in a "what this design document itself did not change" list), but it is a live present-tense "HALTED" status claim R9's own companion-reconciliation list (charter R9 entry, line 195: "`TDS-C023-A §19.3`/`§20` (O3)") asserts it addressed.

- **`IMP-REPORT-WP-17 §6 (line 110), non-struck:** "**… NOT CERTIFIED. No `CLAUDE.md §19.7b` gate has been dispatched.** One implementation-time STOP-and-report is open and requires Repository Owner direction before Gate 1 — `§12`." — both tails are now false (`§12.1` records the STOP-and-report **RESOLVED** via the Repository Owner's Option A; `§14` records Gate 1 **dispatched**). The first Gate 1 attempt's Finding 13 expressly treated the `IMP-REPORT`'s own "no gate dispatched / before Gate 1" phrasing as **non-material** ("expected drafting-time phrasing in the report that *initiates* the gate, not a status-of-record contradiction"), and `§11`/`§13`/`§14`/`§15` supersede it. This reviewer concurs it is **non-material** on that established basis — recorded here only so the reconciliation pass sweeps it for tidiness.

The `WP-17` charter §24 finding alone triggers this gate's STOP condition: "*any remaining live M-1-class stale-status self-contradiction: the determination is **NOT CERTIFIED***" and checklist item 20's "*Flag ANY that is still live — that would be a repeat M-1 and an automatic NOT CERTIFIED*".

### Material vs non-material findings

**Material findings**

**M-1 (repeat) — Residual live, non-struck, present-tense stale-status self-contradiction in the `WP-17` charter.** Charter **§24** ("Implementation Status and Sequencing Disclosure", line 154) asserts, bolded and present-tense, "**No implementation exists**" and "**Gates 1, 2, and 5 (`CLAUDE.md §19.7b`) have not been dispatched**"; charter **line 11** asserts "**No implementation exists at any point in this chain.**" Both are directly false against the current working tree (full BA-01 implementation present; Gate 1 dispatched twice). This is the **same class** of governance-documentation contradiction that returned NOT CERTIFIED at the first Gate 1 attempt and at WP-18's first Gate 1 — and, in §24's case, near-verbatim the exemplar clause the first attempt quoted. The R9 reconciliation pass corrected the charter's header `Status` line and "Final state" line but **did not reach §24 or line 11**. Lesser same-class instance: `TDS-C023-A §20` line 510's non-struck "WP-17 remains … IMPLEMENTATION HALTED" bullet parenthetical (the closing paragraph of that same section *was* reconciled).

**No `CLAUDE.md §19.8.5`-class defect underlies this** — no architectural, security, data-integrity, or tenant-isolation defect; no failing test; no build failure; no broken functionality; no D-1…D-6 or `TDS-C023 §14` design non-conformance; no out-of-scope implementation; no Decision 1–6 change; no interim recognized-type set (`_RECOGNIZED_ENTITLEMENT_TYPE_REFS` is a genuinely empty `frozenset()`). **The technical implementation of WP-17 / BA-01 is sound and passed every other certification-checklist item (Findings 1–18).**

**Remediation:** a further narrow governance-documentation reconciliation pass (strikethrough-preserve + dated superseding note), extending R9's own method to: `WP-17` charter §24 and line 11; `TDS-C023-A §20` line 510's bullet parenthetical; and (for tidiness, though non-material) `IMP-REPORT-WP-17 §6` line 110's "no gate dispatched / STOP-and-report open before Gate 1" tail — reconciling each to "IMPLEMENTATION COMPLETE — NOT YET CERTIFIED — Gate 1 dispatched (NOT CERTIFIED, M-1), entering `CLAUDE.md §19.7b`". The 🔴 RED capability-wide classification, Decisions 1–6, and Decision 3/4's deferred status remain explicitly untouched. **No code change is required or permitted.** Then Gate 1 SHALL be re-dispatched to a fresh reviewer.

**Non-material observations** (carried forward from the first attempt, all re-confirmed non-material against the current tree)

- **O1 (Low)** — the D-4 partial-unique-index expression omits the explicit `::uuid` cast shown in `TDS-C023-A §19.2` (`COALESCE(domain_id, '00000000-0000-0000-0000-000000000000')` vs `…::uuid`). The migration docstring (lines 29–48) and `models/c023_entitlement_context.py` (lines 24–40) both document the exact implemented expression and the rationale; the PostgreSQL offline DDL is syntactically valid (Finding 3); SQLite behaviour was empirically verified by this reviewer's own probe (Finding 7, "D-4 index collides on NULL domain"). The Repository Owner's D-4 condition ("documents the exact expression and demonstrates cross-dialect correctness") is met. Functionally equivalent; not a defect.
- **O2 (Low)** — resolved by R9: `STOP-AND-REPORT-WP-17-01`'s header `Status` line and closing lines are now struck with dated superseding notes.
- **O3 (Low)** — partially resolved by R9: `TDS-C023-A §19.3` and `§20`'s closing paragraph now carry dated forward pointers to `IMP-REPORT-WP-17 §11`/`§14`. `§20` line 510's *bullet* parenthetical was missed — folded into M-1 above as a lesser instance.
- **O4 (informational)** — `HTTP_422_UNPROCESSABLE_ENTITY` deprecation warnings match codebase-wide style (57 across the full run, the vast majority pre-existing); not a WP-17 regression.
- **O5 (Low, new)** — `IMP-REPORT-WP-17 §15` closes with "*Independent review: dispatched immediately following this pass — see `§16`*", but the report contains **no §16** (it ends at §15 + the closing paragraph). A dangling forward reference; the R9 pass's own independent review is asserted (task background) but not recorded in this report. Documentation-tidiness only; not a status-of-record contradiction and not part of M-1.

### Determination line

**NOT CERTIFIED** — Gate 1 of 5 (`CLAUDE.md §19.7b`), re-attempt. **One MATERIAL DEFECT: M-1 (repeat) — a residual live, non-struck, present-tense stale-status self-contradiction** in the `WP-17` charter (§24 "Implementation Status and Sequencing Disclosure": "**No implementation exists**" / "**Gates 1, 2, and 5 … have not been dispatched**"; and line 11: "**No implementation exists at any point in this chain**"), plus a lesser same-class instance in `TDS-C023-A §20` (line 510). The R9 reconciliation pass corrected the charter's header `Status` and "Final state" lines but did not reach these locations. **No `CLAUDE.md §19.8.5`-class code / security / data-integrity / tenant-isolation defect, no failing test (targeted 23/23; full AuthService 876/876), no build failure, no D-1…D-6 or `TDS-C023 §14` design non-conformance, and no out-of-scope implementation was found** — the technical implementation of WP-17 / BA-01 is sound and passed every other checklist item (Findings 1–18), including this reviewer's own from-scratch cross-tenant and D-4 runtime probes. Remediation is a further narrow governance-documentation reconciliation pass (no code change), after which Gate 1 may be re-dispatched to a fresh reviewer.

### Appendix — `git status --short` / `git diff --check` (before and after)

`git rev-parse HEAD` → `c2f93d55daa6806939d98c389f5edcd73993ac60` (unchanged, before and after).

`git diff --check` → no whitespace errors, no conflict markers (only pre-existing CRLF-normalisation `warning:` lines), before and after.

`git status --short` → **96 entries before this appendix** (the WP-17 change set + the pre-existing unrelated C-040 / ROD / `ADR-027…035` / `IRA-C114` / `.xlsx` / `.png` noise), including `?? architecture/06-Reviews/CERT-WP-17_Establish_Entitlement_License_Context.md` (already untracked from the first attempt). **96 entries after** — editing this already-untracked file adds no new `git status` entry. The purpose-built probe `tests/zz_cert_wp17_reattempt_probe.py` was created, run, and **deleted**; `git status` for `tests/` shows only `?? tests/test_entitlement_license_establishment.py` (the WP-17 suite) afterward. **Nothing was staged, committed, or pushed. No file other than this one (`CERT-WP-17_Establish_Entitlement_License_Context.md`, this appended section) was created or modified. Gates 2 and 5 were not dispatched.**

---

*End of Gate 1 re-certification (post-R9). Determination: **NOT CERTIFIED** — one material defect: **M-1 (repeat)**, a residual live stale-governance-status self-contradiction (`WP-17` charter §24 + line 11; `TDS-C023-A §20` line 510) that the R9 pass did not reach. **No code, security, data-integrity, tenant-isolation, test, build, design-conformance, or scope defect** — the technical implementation is sound and passed every other checklist item, including this reviewer's own from-scratch runtime probes and the full 876-test regression. Remediation is a further documentation-reconciliation pass, then Gate 1 re-dispatch. The first-attempt NOT CERTIFIED section above is preserved unchanged.*

---

## Gate 1 Re-Certification (Third Attempt) — 2026-09-02 — ✅ CERTIFIED

**Gate:** `CLAUDE.md §19.7b` **Gate 1 — Independent Certification** (gate 1 of 5), third attempt. Dispatched per direct Repository Owner authorization ("Repository Owner Authorization — Fresh Independent Gate 1 for WP-17 / BA-01"). Verdict recorded here per "Repository Owner Authorization — Record Gate 1 + Gate 2 Verdicts for WP-17 / BA-01" (2026-09-02).

**State certified:** `git rev-parse HEAD` → `c2f93d55daa6806939d98c389f5edcd73993ac60` (`main`); all WP-17 work uncommitted in the working tree; nothing staged, committed, or pushed. This certification isolates the **WP-17 change set only** (tracked modifications + untracked new files), exactly as the first two attempts did.

**Reviewer independence:** a genuinely independent, fresh-context reviewer with **no** access to any prior session's conversation and **no** involvement in: WP-17's implementation; drafting `TDS-C023` / `TDS-C023-A` / `STOP-AND-REPORT-WP-17-01` / the `WP-17` charter / `IMP-REPORT-WP-17`; the R2–R9 / R9-completion / final-cleanup governance-reconciliation passes; or **either the first (`## DETERMINATION` above) or second (`## Gate 1 Re-Certification (fresh independent reviewer, post-R9)` above) Gate 1 attempt**. Every material claim below was re-derived from primary sources — files opened, commands run, purpose-built runtime probes written from scratch and executed.

### Determination

### ✅ CERTIFIED — GATE 1 PASSED

**No `CLAUDE.md §19.8.5`-class defect was found** (no code / security / data-integrity / tenant-isolation defect; no failing test; no build failure; no broken functionality; no D-1…D-6 or `TDS-C023 §14` design non-conformance; no out-of-scope implementation). The M-1-class stale-status self-contradiction that failed the first two attempts has been fully reconciled — no live, non-struck, present-tense stale-status assertion remains in any WP-17 primary status-of-record document (`WP-17` charter Status + `§24` + Final-state lines; `WPR-001` WP-17 row + Gate column; `IRA-C023 §16`).

### Verification summary (each re-derived independently)

1. **Governance authorization** — RO Implementation Authorization reproduced verbatim at `IMP-REPORT-WP-17 §1` (committed `c2f93d5`, 2026-09-01 13:58 +0530); implementation file mtimes hours later → authorization predates implementation; implementation within the authorized WP-17 / BA-01 scope; no scope creep.
2. **WP-17 charter** — Status line, `§24`, and Final-state line all read the current status with the stale "not started / not complete / Gate 1 NOT CERTIFIED" clauses struck (strikethrough-preserve) and dated superseding notes; scope, exclusions, acceptance criteria coherent.
3. **C-023 governance** — `IRA-C023 §16` remains 🔴 RED — Not Implementation Ready; Decisions 1–6 byte-unchanged vs `git show HEAD:`; Decision 3 = DEFERRED; Decision 4 = DEFERRED; nothing reads C-023 capability-wide as implementation-ready.
4. **Implementation traceability** — models, migration, repositories, service, router, schemas, tests, and the two frontend items each map to authorized scope (charter / `TDS-C023` minimum BA / `TDS-C023-A` D-1…D-7).
5. **Approval Authority** — `POST /entitlement-license-contexts` gated by the certified WP-18 `require_approval_authority(...)` factory (`dependencies.py` unmodified); fail-closed; `ANY_ONE` only; no `PLATFORM_ADMIN` / `AUREX_ADMIN` bypass; the service records the ACTIVE row's id and never re-decides; 6 WP-18 files byte-unchanged vs HEAD.
6. **Membership `license_type` / Decision 6** — no write to `memberships`; `c023_license_type` is the disjoint `SUPPLIER/AUDITOR/BOARD_MEMBER/CONSULTANT` set; dedicated test confirms `memberships.license_type` untouched.
7. **Frontend boundary** — exactly Establish + Display-outcome, one additive nav item; real `apiClient` integration, no mocked response / stubbed service call; `§20.6` states present; `tsc` / `eslint` clean.
8. **Tenant isolation / integrity / transaction / audit** — `§21.4` checklist satisfied (two unrelated orgs, no shared row; cross-org read → 404; foreign `membership_id` / `organization_id` in the request body → 403, zero rows); deny-by-default negative controls; atomic transaction with rollback → 409; partial-unique-index race backstop; audit + event on every establish and rejection, no secret material in metadata.
9. **Schema & migration** — conforms to D-1…D-7; `upgrade()` additive only (2 `CREATE TABLE` + 7 `CREATE INDEX`, no `ALTER`); `alembic heads` → single head `c3d4e5f6a7b8`; chains linearly onto WP-18's `f9a3c7e1b5d2`.
10. **Tests & quality (executed by the reviewer)** — targeted suite **23 passed / 0 failed**; full `AuthService` regression **876 passed / 0 failed**; frontend `tsc --noEmit` / `eslint` clean; the reviewer's own from-scratch D-4 partial-unique-index probe passed.
11. **Change control** — `HEAD` `c2f93d5`; `git diff --cached --name-only` empty; WP-17 tracked modifications minimal and additive (`main.py` +1 router include; `models/__init__.py` +2 exports; `admin-navigation.ts` +1 item); all untracked new files are WP-17 artifacts.

**Completion-gate extension (`CLAUDE.md §20.7`)** — met: backend capability complete; Enterprise Experience complete; navigation complete; the end-to-end License workflow is demonstrable through the running application; frontend and backend fully integrated with no mocked API response or stubbed service call. The Entitlement establish-success path is the RO-approved Option A disclosed scope boundary (Decision 3 deferred), not an unmet condition.

### Non-material observations (non-blocking — do NOT fail Gate 1)

O1 D-4 index omits an illustrative `::uuid` cast (functionally equivalent; documented; cross-dialect proven). O2 one loose `in (403, 422)` test assertion (path is deterministically 403). O3 static-config screen rather than `screen_registry`-driven — pre-existing repo-wide pattern, not WP-17-introduced. O4 pre-existing `HTTP_422_UNPROCESSABLE_ENTITY` deprecation warnings, codebase-wide. O5 the suite requires `JWT_SECRET_KEY` / a parseable `DATABASE_URL` in the environment. O6 the working tree carries unrelated uncommitted C-040 / ROD / ADR / `CLAUDE.md` governance artifacts — verified to contain zero WP-17/C-023 content; a Release Readiness (Gate 5) concern, not a Gate 1 blocker.

### Determination line

**✅ CERTIFIED — Gate 1 of 5 (`CLAUDE.md §19.7b`), third attempt.** The technical implementation of WP-17 / BA-01 is sound and conforms to its governing charter, `TDS-C023`, `TDS-C023-A` D-1…D-7, `ADR-036`, and the Repository Owner authorization; it consumes the certified WP-18 Approval Authority infrastructure unchanged; it honours Decision 6; the frontend is exactly the two authorized items with real backend integration; the `§21.4` tenant-isolation checklist is satisfied; the migration is additive with a single head; the full 876-test `AuthService` regression passes; and the M-1 stale-status documentation that failed the first two attempts is reconciled. **C-023 capability-wide remains 🔴 RED — Not Implementation Ready; Decisions 1–6 unchanged; Decision 3 and Decision 4 remain DEFERRED.** Gate 2 (V&V Audit) has since also **PASSED on the technical merits** (`IMP-REPORT-WP-17 §17`); Gates 3–4 were not triggered; ~~Gate 5 (Release Readiness Audit) is **PENDING** — not dispatched.~~ *(Superseded 2026-09-02 — Gate 5 Release Readiness Audit has since **PASSED** by a fresh independent reviewer (`IMP-REPORT-WP-17 §18`), and WP-17 / BA-01 is now **FORMALLY CLOSED — CERTIFIED — RELEASE-READY** (all five `CLAUDE.md §19.7b` gates complete; repository commit outstanding).)* Nothing was staged, committed, or pushed. No file other than this one (this appended section) and its companion recording edits (`IMP-REPORT-WP-17`, `WPR-001` WP-17 row, `WP-17` charter, and — at formal closure — `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP` C-023 row, plus minimal closure forward-pointers in `IRA-C023 §16` and `TDS-C023`) was modified. The first- and second-attempt NOT CERTIFIED sections above are preserved unchanged.

*End of Gate 1 re-certification (third attempt). Determination: **✅ CERTIFIED — GATE 1 PASSED.***
