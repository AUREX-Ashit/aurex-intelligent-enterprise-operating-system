# TDS-C021 — Product & Service Catalog (C-021) — Minimum Business Activity Technical Design

**Document status: PREPARED FOR INDEPENDENT REVIEW (O1/O2 correction pass applied).** Per direct Repository Owner authorization ("C-021 — REPOSITORY OWNER ACCEPTANCE + SERVICE-HOSTING DECISION + TDS PREPARATION"), the Repository Owner has (1) explicitly selected **Option A — `AuthService`** as the C-021 service host, and (2) **accepted** the `IRA-C021` 🟡 AMBER verdict as the governance basis for proceeding to Technical Design. Per a follow-on authorization ("C-021 — CORRECT THE TDS-C021 O1/O2 OBSERVATIONS"), two further Repository Owner decisions have been applied to this document:

- **O1 — Identity generation.** The Repository Owner **accepts the R-1 acceptance properties as the requirement** — the Offering Reference is system-assigned, monotonic, of the form `PREFIX-NNNNNN`, unique, and concurrency-safe. A PostgreSQL `SEQUENCE` is **NOT** made an architectural requirement; the concrete mechanism is left to implementation design provided those properties hold, and if implementation determines a new database object (e.g. `CREATE SEQUENCE`) is required, that is handled through the normal `CLAUDE.md §18`/`§19.4` change-control process. (§9.3, §9.11, §17, §21, §26, §27.)
- **O2 — `category_ref`.** The Repository Owner decides `category_ref` is **OPTIONAL / NULLABLE**. It remains an opaque reference only; no taxonomy governance, category management, or free-form taxonomy is created, and `ROD-C021` is not reopened. (§9.1, §9.8, §9.11, §13, §20, §23, §25, §27.)

This document is the resulting Technical Design for C-021's minimum-scope first Business Activity, strictly within the `ROD-C021` D1–D8 boundary. **No schema, migration, ORM model, repository, service, router, frontend, or test is created or authorized by this document** — this is a governance/design-completeness status, not an implementation authorization. **No WP is registered. No BA charter exists. No CBOR ADR is created. No BAR registration is performed.** The schema-shape STOP-and-report required by `CLAUDE.md §18`/`§19.4` is performed at the conceptual level in §9.

**Naming note (mirrors `TDS-C023`'s and `TDS-C132`'s own precedent):** capability-first, no WP number — none exists yet for C-021 (`WPR-001 §3` Maintenance Rule).

**Governing basis, in order:** `CAP-001` (C-021 registration, line 75) → `COM-001` §4/§6 (Universal Commercial Construct Model; Offering Definition / Product & Service Catalog canonical model — LOCKED, CR-3.0) → `PE-001-C021` v1.1 (Enterprise Experience Specification — Active) → `architecture/06-Reviews/ROD-C021-Product-and-Service-Catalog-Capability-Boundary-and-Minimum-Scope.md` (RO Decisions D1–D8) → `architecture/05-Implementation/IRA-C021_Product_and_Service_Catalog_Implementation_Readiness_Assessment.md` (🟡 AMBER — ready for Technical Design preparation; accepted by the Repository Owner) → the Repository Owner's service-hosting selection (Option A — `AuthService`) → this document.

**Classification key:** `[FACT]` — repository fact / verbatim from a LOCKED or Active source, or verified by direct code inspection. `[RO DECISION]` — a recorded Repository Owner decision (D1–D8, or the hosting selection). `[PRECEDENT]` — an existing, certified in-repo implementation pattern. `[DESIGN]` — a Technical Design decision this document makes within the approved boundary. `[FUTURE TDS QUESTION]` — deferred to a future C-021 increment's own TDS. `[IMPLEMENTATION-TIME]` — an ordinary implementation choice requiring no further TDS or RO decision.

---

## 1. Purpose

Design, at the level `IRA-C021`'s accepted AMBER verdict authorizes, the minimum-scope first Business Activity for C-021: a persisted, platform-global **Offering Definition** record supporting establish / list / read, per `ROD-C021` D4 (Option A + D). This document carries forward every design conclusion `IRA-C021` reached, applies the Repository Owner's `AuthService` hosting selection, and performs the `CLAUDE.md §18`/`§19.4` schema-shape STOP-and-report (§9) — recording whether any further Repository Owner decision surfaces from it.

## 2. Scope (design-level; carried forward from `ROD-C021` D4 / `IRA-C021 §9`, unchanged)

BA-01 — **"Establish / Manage Offering Definition"** — establishes and reads a **standalone Atomic Offering Definition**:

- **Establish** an Atomic Offering Definition with: canonical identity; canonical name; Product / Service classification; opaque category reference (optional / nullable per `[RO DECISION]` O2 — §9.8); optional opaque list-price reference; current state = `draft`.
- **List** Offering Definitions (platform-global — no tenant filter).
- **Read** one Offering Definition by id.
- Produce the first **Authoritative Offering Definition Context** (`COM-001-002`) and a stable **Offering Reference** (`ERB-C021-06`) for downstream consumption by C-020 / C-024 / C-025 (by reference only; those capabilities are unchartered).

## 3. Non-Goals (unchanged from `ROD-C021` D3/D5/D6/D7/D8 and `ROD-C021 §M` — restated, not reinterpreted)

Composition (Composite / Bundle / Package / Variant / Edition / Optional Component / Add-on); Offering Relationships (replaces / superseded-by / successor / predecessor / depends-on / bundled-with / optional-with / mutually-exclusive / complementary); the Digital / Physical secondary typology of `COM-001-021` (BA-01 classifies on the Product ↔ Service axis only, per D4's literal text); publication (`draft → published`); retirement (`published → retired`); revision of a published offering; pricing computation / rating / discounting / execution; a pricing engine; availability determination; Subscription (C-020); Customer / Account and Customer–Account relationships (C-022); segment-scoping; Entitlement / Feature Catalog / entitlement semantics (C-023 — **C-023 Decision 3 is not fired or reopened**, §10, §24); Billing (C-024); Contract (C-025); tenant-specific catalog overlays / per-tenant catalog (D8); catalog taxonomy governance authority; a canonical Catalog Governance Authority; offering approval authority; retirement-notice policy; order / inventory / fulfillment / provisioning / usage / metering / taxation; discovery / overlap detection (`EX-C021-13`); future-dated transitions; external product / marketplace / CRM / ERP integrations; any event-bus infrastructure or repair of `Backend/Shared/Events`; any new governance authority; any speculative future architecture.

## 4. Business Activity Being Designed

**BA-01 — "Establish / Manage Offering Definition."** One Business Activity, three operations (establish, list, read). "Manage" carries no meaning beyond these three for BA-01 — no edit or delete of an established Offering Definition's content is designed here (revision belongs to the future Version Management increment, `COM-001-025`). BA-01 writes an Offering Definition only in `state = 'draft'` and implements no state transition.

---

## 5. Selected Service Host — RECORDED

**`[RO DECISION]` — Option A: `AuthService`.** Recorded per direct Repository Owner instruction ("C-021 — REPOSITORY OWNER ACCEPTANCE + SERVICE-HOSTING DECISION + TDS PREPARATION").

- C-021 Offering Definition persistence, and the BA-01 backend (model, repository, service, router), shall be hosted in the existing **`AuthService`**.
- `[FACT]` Rationale of record (from `IRA-C021 §17`): consistency with `ADR-036`'s modular-monolith posture; co-location with the adjacent D-002 capability C-023 (`c023_license_context`, `c023_entitlement_context`, already in `AuthService`); the platform-global administrative-object precedent `C-003` Roles physically lives in `AuthService`; a single, direct `PLATFORM_ADMIN` writer with **no write-fan-in** (contrast `TDS-C132 §6` — C-021 has no cross-service trigger topology to solve).
- **This decision does NOT authorize:** cross-service database access (`CLAUDE.md §8` remains binding); any new service; an event bus; implementation of any kind. `AuthService` hosting is a design/architecture decision only.

---

## 6. Business Object Boundary

`[FACT]` / `[DESIGN]` The Offering Definition is a single, self-contained aggregate:

- **Aggregate root:** the Offering Definition record itself. No child entities in BA-01 (composition/relationships are excluded, §3).
- **It is not, and never becomes:** a Subscription (C-020), a Customer/Account (C-022), an Entitlement or Feature (C-023), a computed Price (C-024), a Contract (C-025), a Tenant (C-040), an Access grant (C-002), or a Workspace (C-008) — `PE-001-C021 §1.5`, restated `ROD-C021` D1/D2/D3.
- **Downstream consumers** (C-020 Subscription Anchor `COM-001-011`; C-024 Billing; C-025 Contract) consume the **Offering Reference** by identity, by reference only. BA-01 builds no integration to them (all unchartered). The Offering Reference is a stable, opaque string (§9.3) other capabilities may later store and resolve.
- **Opaque references out:** `category_ref` and `list_price_reference` are opaque strings the Offering Definition *cites*, never governed foreign keys it *owns* (§9.8, §9.9) — no taxonomy table, no price table, no FK.

---

## 7. Business Object Eligibility + CBOR / BAR Prerequisites (carried forward from `IRA-C021 §8` — not re-derived)

`[FACT]` **FINDING (already established, `IRA-C021 §8`):** the Offering Definition satisfies `CMD-001 §26.3a` — Step 1 (Independent Identity) ✓, Step 2 (Cross-Experience Reference — C-020/C-024/C-025 consume the Offering Reference by identity) ✓, Step 3 (Governed Lifecycle `draft → published → retired`, Historical Definitions retained) ✓. **Eligible for CBOR registration.**

- **`[FACT]` CBOR ADR — MANDATORY PREREQUISITE, NOT PERFORMED HERE.** Per `COM-001-005` (Registration Precedes Implementation), `COM-001-061` (an Offering Definition is a CBOR-registered Business Object once implemented), and `CMD-001 §26.4`, a dedicated ADR registering the Offering Definition Business Object in `CBOR-INDEX.md` (Business Object Identifier, Canonical Name, Owning Capability = C-021, Aggregate Root, Primary Data Category, Lifecycle Model) **must be created and accepted before implementation begins**, mirroring `ADR-019`'s registration of `CFG-000001` for WP-10. **This TDS does not create that ADR.** The Business Object Identifier is the ADR's to assign (candidate form `OFR-000001` / `OFD-000001`, not fixed here).
- **`[FACT]` BAR registration — MANDATORY PREREQUISITE, NOT PERFORMED HERE.** Per `COM-001-060`, the BA-01 Business Activity ("Establish / Manage Offering Definition") **must be registered in the Business Activity Registry before implementation begins**. **This TDS does not perform that registration.**

Both prerequisites gate *implementation authorization*, not this TDS's own preparation or its independent review.

---

## 8. Ownership Boundaries (restating `ROD-C021` D1/D2/D3 — not reinterpreted)

- **C-021 / C-020** (D1): C-021 owns the Offering Definition; C-020 owns Subscription. C-021 produces the Offering Reference C-020 consumes. BA-01 models no Subscription.
- **C-021 / C-022** (D2): an Offering Definition exists independently of Customer/Account. BA-01 models no Customer/Account; no segment-scoping.
- **C-021 / C-023** (D3): C-021 owns the commercial Offering Definition; C-023 owns Licensing & Entitlement. **No direct dependency.** BA-01 implements no entitlement/feature semantics. **C-023 Decision 3 is untouched and not fired** (§24).

---

## 9. Schema-Shape STOP-and-Report (`CLAUDE.md §18` / `§19.4`) — conceptual level only; NO migration / model / table created

Performed now that §5 resolves the host as `AuthService`. This is governance/Technical-Design work — **it creates no Alembic migration, ORM model, database table, repository, service, router, frontend, or test.** It records the conceptual schema shape the eventual physical design must satisfy, and states explicitly whether any further Repository Owner decision surfaces (§9.11). Reasoning applies `COM-001 §4`/`§6`, `CMD-001`, `CLAUDE.md §8`/`§18`/`§21.4`, and `AuthService`'s own existing persistence conventions — `models/role.py`, `models/c023_entitlement_context.py`, `models/c023_license_context.py`, `models/c132_notification.py` (all read directly for this report as the governing precedent set).

### 9.1 Proposed table (conceptual): `c021_offering_definition`

`[DESIGN]` Capability-prefixed name, mirroring `c023_entitlement_context` / `c132_notification`. The `String` lengths shown below are indicative; exact length bounds are `[IMPLEMENTATION-TIME]` per §9.6.

| Field | Conceptual type | Null? | Notes / precedent |
|---|---|---|---|
| `id` | UUID, PK, default `uuid4` | NOT NULL | Record identity + audit correlation id. Every `AuthService` model's own PK convention (`role.id`, `c023_*.id`, `c132_notification.id`). |
| `offering_reference` | String(30), UNIQUE | NOT NULL | The `COM-001-001` Universal Identity (`PREFIX-NNNNNN`) **and** the stable Offering Reference downstream capabilities consume (`ERB-C021-06`). System-assigned (§9.3). Distinct from the UUID PK, mirroring `role.role_code`'s "business key alongside the UUID PK" shape — but generated, not caller-supplied. |
| `offering_name` | String(255) | NOT NULL | Canonical name (D4). Precedent: `role.role_name`. No uniqueness invariant (§9.5). |
| `offering_kind` | String(20), `CheckConstraint "offering_kind IN ('PRODUCT','SERVICE')"` | NOT NULL | Product / Service classification (D4; the Product↔Service axis of `COM-001-021`). Digital/Physical secondary typology is **excluded** from BA-01 (§3). Closed-set CHECK mirrors `c132_notification.severity` / `c023_entitlement_context.status`. |
| `category_ref` | String(100) | **NULLABLE** | Opaque category reference (D4). **Optional / nullable per Repository Owner decision O2** — no governed `COM-001-024` taxonomy authority exists, and BA-01 must be able to establish a standalone Atomic Offering Definition without depending on an unresolved taxonomy authority. Free-text, non-authoritative — **not a FK**, no `c021_category` table, no category management (§9.8). Precedent: `c023_entitlement_context.entitlement_source_reference` (nullable, free-text, non-authoritative). |
| `list_price_reference` | String(100) | NULLABLE | Optional opaque list-price reference (D6). Reference attribute **only** — the `String` type is chosen precisely to make "becomes a numeric/computed price field" structurally impossible. **Never** a `Numeric`/`Decimal`/`Integer` column; never rated, discounted, or computed. Precedent: same opaque-string-citation shape as `entitlement_source_reference`. |
| `state` | String(20), `CheckConstraint "state IN ('draft','published','retired')"`, default `'draft'` | NOT NULL | `COM-001-020` offering-state model. **BA-01 writes only `'draft'`** and exposes no transition (D7). Full closed set declared for schema correctness even though a subset is written — precedent: `c023_entitlement_context` declares `ACTIVE/SUSPENDED/REVOKED`, BA-01 writes only `ACTIVE`; `c132_notification` declares `UNREAD/ACKNOWLEDGED`. |
| `version` | Integer, default `1`, server_default `'1'` | NOT NULL | `COM-001-025` Version Management. **Designed-for, not exercised** by BA-01 (no versioning endpoint). Precedent: `role.version`. |
| `supersedes_id` | UUID, FK → `c021_offering_definition.id` | NULLABLE | `COM-001-025` Historical Definition / lineage link. **Designed-for, not exercised** by BA-01 (always `NULL` in BA-01). Precedent: `role.supersedes_id` (self-referential FK, derived inverse via relationship, never a second stored column). |
| `created_by_actor_id` | UUID | NOT NULL | Point-in-time audit citation of the `PLATFORM_ADMIN` caller's `person_id`. **NOT a foreign key** — precedent: `c023_entitlement_context.committed_by_actor_id` ("a point-in-time audit citation"). |
| `created_at` | `DateTime(timezone=True)`, default now() | NOT NULL | Standard platform timestamp. |
| `updated_at` | `DateTime(timezone=True)`, `onupdate` now() | NULLABLE | Standard platform timestamp. |

**No `organization_id` column** — `[RO DECISION]` D8, platform-global catalog. Precedent: `roles` has no `organization_id`. This is a structural expression of D8, not an omission.

### 9.2 Ownership

`[DESIGN]` `AuthService` exclusively (§5). No other service reads or writes `c021_offering_definition`, consistent with `CLAUDE.md §8`. Downstream capabilities, when chartered, will consume the Offering Reference through C-021's own API, never by reaching into this table.

### 9.3 Identity generation

`[DESIGN]` Two identifiers, by deliberate design (mirroring `role.id` + `role.role_code`):
- `id` — `uuid4`, the database PK and internal handle (platform convention; used in the `GET /offerings/{id}` path).
- `offering_reference` — the `COM-001-001` `PREFIX-NNNNNN` Universal Identity **and** the stable Offering Reference downstream capabilities consume (`ERB-C021-06`). Exact prefix token (`OFFERING-` / `OFF-` / `OFR-` / `OFD-`) is `[IMPLEMENTATION-TIME]`, to align with the CBOR ADR's assigned Business Object Identifier; the numeric portion is 6-digit zero-padded (`NNNNNN`).

`[RO DECISION] (O1)` **The `offering_reference` generation is specified as a set of acceptance properties, not a mechanism.** Per Repository Owner decision O1, the Offering Reference SHALL be:
1. **system-assigned** (assigned by C-021 at establish time, never supplied or chosen by the caller);
2. **monotonic**;
3. of the form **`PREFIX-NNNNNN`** (`COM-001-001`);
4. **unique** (enforced by the `UNIQUE` constraint on the column, §9.1/§9.5);
5. **concurrency-safe** (two concurrent establishes never produce the same reference and never fail with an unhandled error — the standard `except IntegrityError → rollback → retry` discipline `role_service.establish` already demonstrates is one acceptable realization, §17).

`[RO DECISION] (O1)` **A PostgreSQL `SEQUENCE` is NOT an architectural requirement.** The concrete mechanism (a DB sequence, an in-transaction `MAX+1` with retry, an application-level allocator, or another approach) is **intentionally left to implementation design**, provided the five acceptance properties above are satisfied. `[FACT]` No existing `AuthService` model generates a per-row `PREFIX-NNNNNN` reference today — every model uses a `uuid4` PK and any business key (`role_code`) is caller-supplied — so realizing `COM-001-001`'s mandated format is new implementation work, but it introduces no new architectural concept, service boundary, or business rule. **If implementation determines that a new database object (for example `CREATE SEQUENCE`) is required, that object SHALL be introduced through the normal `CLAUDE.md §18`/`§19.4` change-control process** at implementation time — it is neither presupposed nor pre-authorized here.

`[DESIGN]` Options recorded for the implementation designer (none is mandated; none implies a schema commitment beyond §9.1): a dedicated DB sequence formatted by the service as `f"{PREFIX}-{n:06d}"`; an application-level allocator that derives the next number from the current maximum already-assigned `offering_reference` with the `UNIQUE` constraint as backstop and an `IntegrityError`-driven retry; or an equivalent monotonic allocator. A caller-supplied reference (the `role_code` shape) is **excluded** by O1 property 1; using the bare `uuid` PK as the reference is **excluded** by O1 property 3.

### 9.4 State representation

`[DESIGN]` A single `state` string column, CHECK-constrained to the full closed set `{draft, published, retired}` (`COM-001-020`), defaulting to and only ever written as `'draft'` in BA-01. No enum table. No transition method, endpoint, or history row in BA-01 (D7). Precedent: `c132_notification.status`, `c023_entitlement_context.status`.

### 9.5 Uniqueness / natural-key decisions

`[DESIGN]`
- `offering_reference` — **UNIQUE** (whole-table plain unique index). It is a system-assigned stable identity; a plain unique constraint is correct because BA-01 has no in-place versioning that would legitimately reuse it. `[FUTURE TDS QUESTION]`: if the Version Management increment (`COM-001-025`) later versions an offering in place while preserving `offering_reference` across versions, this may need to become a partial unique index scoped to the current version, mirroring `roles`' `ix_roles_role_code_active_unique` — out of scope for BA-01.
- `offering_name` — **NOT unique.** `COM-001 §6` names no uniqueness invariant on offering name; two `draft` offerings may legitimately share a name. This mirrors `c132_notification`'s "BA-01 imposes no uniqueness/idempotency invariant" disposition and bears on idempotency (§18).
- No composite natural key (e.g. `(offering_name, offering_kind)`) is governance-required.

### 9.6 Indexes — governance-required vs implementation-time

`[DESIGN]`
- **Governance-required:** the UNIQUE index on `offering_reference` (identity integrity); the two `CheckConstraint`s on `offering_kind` and `state` (closed-set integrity, mirroring `AccessEvaluationOutcome`'s discipline).
- **`[IMPLEMENTATION-TIME]`:** whether `ix_c021_offering_definition_state` is added to support the list view's "draft offerings" filter (precedent: `c132`'s composite `(membership_id, status)`); whether `ix_c021_offering_definition_offering_kind` is added; exact constraint/index naming; exact `String` length bounds for `offering_reference` / `offering_kind` / `state` / `category_ref` / `list_price_reference`.

### 9.7 Version / lineage representation

`[DESIGN]` `version` (Integer, default 1) and `supersedes_id` (self-referential nullable FK) are **declared in the BA-01 schema** so the future Version Management increment does not require an `ALTER`, mirroring how `roles` carried its full version/supersedes shape from WP-00/WP-02. **BA-01 never writes a non-default value** — `version` is always `1`, `supersedes_id` always `NULL`. This "declare the full lifecycle shape, exercise a subset" choice matches the `c023_*` precedent exactly.

### 9.8 Opaque `category_ref` semantics

`[DESIGN]` / `[RO DECISION] (O2)` `category_ref` is a free-text, opaque, non-authoritative string citing a catalog category (`COM-001-024`, `ROD-C021` D4). Per Repository Owner decision O2 it is **OPTIONAL / NULLABLE**:
- **Why nullable:** `ROD-C021` D4 approves *an opaque category reference*; no governed `COM-001-024` taxonomy or category authority currently exists; and BA-01 must be able to establish a standalone Atomic Offering Definition **without depending on an unresolved taxonomy authority**. A caller may omit `category_ref` entirely (the row persists with `NULL`); a supplied value is stored verbatim.
- **What O2 does NOT create:** no taxonomy governance; no category management (no CRUD for categories); no free-form taxonomy / category registry; no `c021_category` table; no foreign key. `ROD-C021` is **not** reopened.
- **Precedent:** `c023_entitlement_context.entitlement_source_reference` — a nullable, free-text, non-authoritative reference. `category_ref` "stores a REFERENCE, never a DEFINITION."
- `[FUTURE TDS QUESTION]` — if `COM-001-024` catalog taxonomy governance authority later binds, a future C-021 increment's own TDS may govern `category_ref`'s vocabulary. BA-01 introduces none of that machinery.

### 9.9 Opaque `list_price_reference` semantics

`[DESIGN]` `list_price_reference` is an **optional** (`NULLABLE`), opaque, non-authoritative `String` citing an externally-held list price (`COM-001-020`, `PE-001-C021 §1.5` — "a list-price reference attribute … only, and never computes or executes a price"). Enforcement of D6 is structural: the column is `String`, never numeric; the service performs no arithmetic on it; the response echoes it verbatim; there is no rate/discount/compute code path anywhere in BA-01. Pricing execution (C-024) is out of scope (§3).

### 9.10 What is deliberately absent from `c021_offering_definition`

`[DESIGN]` No `organization_id` (D8); no composition/child-component columns or table (D5); no relationship columns or table (D5); no `published_at` / `retired_at` / approval-reference columns (D7 — publication/retirement out of scope; approval authority Pending Canonical Binding must not be silently solved); no numeric price, rate, discount, or currency column (D6); no `effective_from` / `effective_to` (an Offering Definition in `draft` is not a time-bound fact like an entitlement — `COM-001 §6` has no effective-dating for `draft`); no customer/account/segment column (D2); no entitlement/feature column (D3); no tenant-overlay column (D8).

### 9.11 Does any further Repository Owner decision surface?

`[DESIGN]` **No further *blocking* Repository Owner decision surfaces from this schema-shape investigation.** Every field maps to an already-established `AuthService` persistence pattern (`uuid` PK; business-key-alongside-PK per `role_code`; closed-set `CheckConstraint`s per `severity`/`status`; opaque non-authoritative string citation per `entitlement_type_ref`/`entitlement_source_reference`/`committed_by_actor_id`; self-referential version/lineage per `roles`; no `organization_id` per `roles`).

The two items this schema-shape investigation originally disclosed for Repository Owner attention **have now been resolved by explicit Repository Owner decisions** (recorded in the status header and applied throughout this document):
1. **Reference generation (§9.3)** — `[RO DECISION] (O1)`: R-1's acceptance properties (system-assigned, monotonic, `PREFIX-NNNNNN`, unique, concurrency-safe) are the requirement; the mechanism is left to implementation design; a PostgreSQL `SEQUENCE` is not mandated; a new DB object, if any, goes through `CLAUDE.md §18`/`§19.4` at implementation time.
2. **`category_ref` nullability (§9.8)** — `[RO DECISION] (O2)`: `category_ref` is OPTIONAL / NULLABLE; it stays an opaque reference only; no taxonomy governance, category management, or free-form taxonomy is created; `ROD-C021` is not reopened.

This mirrors `TDS-C132 §6.6` item 11 ("none identified that requires further Repository Owner authority") — and the two items that were flagged have since been decided by the Repository Owner, not deferred.

---

## 10. Authority Model / `PLATFORM_ADMIN` Enforcement

`[DESIGN]` / `[PRECEDENT]`
- Every BA-01 route (`POST /offerings`, `GET /offerings`, `GET /offerings/{id}`) is gated by **`Depends(require_platform_admin)`** — the existing `AuthService` dependency (`dependencies.py`), a direct `claims["role_code"] == "PLATFORM_ADMIN"` check, no `AuthorizationContext`, no Runtime Engine.
- **Precedent:** `C-003` Roles — `routers/role.py` gates every operation with `Depends(require_platform_admin)`; `roles` has no `organization_id`; `models/role.py` verified directly. This is the platform-global-administrative-object pattern, exactly the shape `IRA-C021 §11`/`§12` identified.
- This is **not** the tenant-scoped `require_matching_tenant_or_platform_admin` gate used by C-041 Configuration and C-132 Notifications — `[RO DECISION]` D8 makes the C-021 catalog platform-global, so there is no caller-tenant-vs-header comparison to make.
- **No dedicated Approval / Commit Authority** is designed for `establish` — BA-01 establishes an offering only in `draft` (D7); the point where an approval authority matters (`draft → published`, `COM-001-026`) is out of scope. Keeping BA-01 to `draft` is precisely what avoids loading the approval-authority Pending Canonical Binding.
- `[FUTURE TDS QUESTION]` A canonical **Catalog Governance Authority** replacing the interim `require_platform_admin` gate — trigger: any C-021 increment past `draft` (publication, retirement, taxonomy governance, retirement-notice policy). Deferred with recorded trigger, mirroring `IRA-C023 §21.12`'s Decision-3 deferral discipline (`ROD-C021 §K`).

## 11. Tenant-Middleware Exemption Rationale

`[DESIGN]` / `[PRECEDENT]` The `/offerings` prefix shall be added to `middleware/tenant.py`'s exemption list, on the **same basis as `/roles`**: the `c021_offering_definition` model has no `organization_id` column — the catalog is platform-global (`[RO DECISION]` D8), not tenant-scoped, so there is no single tenant to which a request could be scoped, and `X-Tenant-ID` is not required. `[FACT]` The exemption list already carries `/roles`, `/organizations`, `/domains` on this exact rationale (verified: `middleware/tenant.py` lines ~33–34, 221–245). The exemption entry is purely additive and does not alter `X-Tenant-ID`'s meaning for any already-tenant-scoped endpoint (`/configuration`, `/entitlement-license-contexts`, `/notifications` remain unchanged). `[IMPLEMENTATION-TIME]`: prefix-match (`path == "/offerings" or path.startswith("/offerings/")`), mirroring every other entry.

## 12. Repository / Service / Router Boundaries

`[DESIGN]` / `[PRECEDENT]` Mirrors the established `AuthService` per-capability layering (`role.py` / `c132_notification` / `entitlement_license`):

| Layer | Component (conceptual) | Responsibility |
|---|---|---|
| Model | `models/c021_offering_definition.py` → `C021OfferingDefinition(Base)` | ORM mapping only (§9.1). Registered in `models/__init__.py`. |
| Repository | `repositories/c021_offering_definition_repository.py` → `C021OfferingDefinitionRepository(BaseRepository[C021OfferingDefinition])` | `create()`, `get_by_id()`, `list_all(limit=_LIST_HARD_CAP)` (newest-first), `next_offering_reference()` (§9.3). A hard list cap (e.g. `_LIST_HARD_CAP = 200`) mirroring `C132NotificationRepository`. |
| Service | `services/offering_definition_service.py` → `OfferingDefinitionService` | BA-01 orchestration: `establish(request, actor_id)` (assign `offering_reference`, insert `state='draft'`, `record_audit` + `publish_event`), `list()`, `get(offering_id)`. No transition methods. |
| Router | `routers/offering.py` → `router` | 3 routes (§13). `Depends(require_platform_admin)` on each. Registered in `main.py` as `app.include_router(offering.router, prefix="/offerings", tags=["Product & Service Catalog"])`. |
| Schema | `schemas/offering.py` | `EstablishOfferingDefinitionRequest`, `OfferingDefinitionResponse` (§13). |

## 13. API Contract (design-level)

`[DESIGN]` Prefix `/offerings` (kebab plural, per `main.py` convention). All routes `require_platform_admin`; prefix tenant-middleware-exempt (§11).

| Method / path | Operation | Request | Response | Codes |
|---|---|---|---|---|
| `POST /offerings` | Establish | `EstablishOfferingDefinitionRequest` = { `offering_name`: str (min_length 1), `offering_kind`: `Literal["PRODUCT","SERVICE"]`, `category_ref`: str \| None (optional per RO decision O2; if provided, min_length 1), `list_price_reference`: str \| None } | `OfferingDefinitionResponse` (all §9.1 columns, incl. `offering_reference`, `state="draft"`, `category_ref` possibly `null`), `from_attributes=True` | 201 established · 400 missing/malformed Authorization · 401 invalid token · 403 not `PLATFORM_ADMIN` · 422 invalid body (bad `offering_kind`, empty `offering_name`, empty-string `category_ref`) |
| `GET /offerings` | List | — | `list[OfferingDefinitionResponse]`, newest-first, hard-capped | 200 (possibly empty) · 400 · 401 · 403 |
| `GET /offerings/{offering_id}` | Read | path `offering_id`: UUID | `OfferingDefinitionResponse` | 200 · 400 · 401 · 403 · 404 no such offering |

`[DESIGN]` Notes: `state` is **not** a settable request field — always `'draft'` (D7). `offering_reference` is **not** a settable request field — system-assigned (§9.3). Read is by UUID `id` (consistent with every other `AuthService` read); `[IMPLEMENTATION-TIME]`: whether a secondary `GET /offerings/by-reference/{offering_reference}` lookup is also offered. No anti-enumeration 404-vs-403 nuance is needed (unlike `c132`/`c023`) — the catalog is platform-global and every row is visible to any `PLATFORM_ADMIN`, so a missing id is a plain 404.

## 14. Frontend Contract (design-level)

`[DESIGN]` `[RO DECISION]` D4 includes `list` and `read`, and C-021 (a future WP-20) falls under `CLAUDE.md §20`/`§21.3` — BA-01 delivers an operable, demonstrable frontend (not backend-only):

- **Feature folder** `source/frontend/src/features/offering-catalog/` (`components/*.tsx`, `state/useOfferingCatalog.ts`, `api/offering-api.ts`, `types/offering.ts`), mirroring the certified WP-17 `features/entitlement-license/` shape.
- **Screens:** (1) Offering Definition list (table — `offering_reference`, `offering_name`, `offering_kind`, `category_ref`, `state`); (2) Offering Definition detail (read one); (3) Establish Offering Definition form (name, kind select, category, optional list-price reference).
- **Navigation:** under the existing `subscriptions` nav parent (`source/frontend/src/config/admin-navigation.ts` — "Subscription & Commercial Management", `/platform-admin/subscriptions`), as a sibling of the C-023 `entitlement-license` screen. Candidate route `/platform-admin/subscriptions/offerings`. `[IMPLEMENTATION-TIME]`: exact slug/label, subject to DS-001 nav conventions.
- **Required UI states** (`CLAUDE.md §20.6`): loading, empty, validation, error, confirmation — against the real `/offerings` API, no mock. Plus the `IMP-001 §10.3` content-disclosure states (Summary / Details / Evidence / Audit History) where applicable to the detail screen.
- **Metadata-driven rendering** (`IMP-FE-001` `screen_registry`) and keyboard accessibility are mandatory per `CLAUDE.md §20.6` — restated here as a completion checkpoint, not a new rule.

## 15. DS-001 Compliance / Frontend Boundary

`[FACT]` / `[DESIGN]` BA-01's screens are standard enterprise list / detail / create archetypes. **No new DS-001 component, token, theme, colour, spacing value, motion, or interaction pattern is introduced.** Reused DS-001 primitives: data table, form field / select, detail panel, status chip (for `state`, of which BA-01 renders only `draft`), page shell. `[FACT]` Per the recall note, `DS-001` defines taxonomy only; `theme.css` is the concrete token source — no colour/icon/spacing is invented here. **No `CLAUDE.md §19.1` STOP-and-report is triggered on the DS-001 dimension.** `[IMPLEMENTATION-TIME]`: exact component selection per screen, against the DS-001 component catalogue.

## 16. Audit / Event Requirements (existing infrastructure only)

`[DESIGN]` / `[PRECEDENT]` `establish` calls, in-process, post-flush, mirroring `role_service.establish` exactly:
- `record_audit(action="ESTABLISH_OFFERING_DEFINITION", resource=f"offering:{row.id}", status=AuditStatus.SUCCESS, actor_id=actor_id or "SYSTEM", metadata={"offering_reference": row.offering_reference, "offering_kind": row.offering_kind, "state": row.state})` — and an `AuditStatus.DENIED` record on the validation-failure paths (bad `offering_kind`, etc.), matching `role_service`'s denied-path audit calls.
- `publish_event("OFFERING_DEFINITION_ESTABLISHED", {"offering_id": str(row.id), "offering_reference": row.offering_reference, "offering_kind": row.offering_kind, "offering_name": row.offering_name})`.
- `[FACT]` `publish_event()` is `AuthService`'s **structured-log stand-in**, not a real event bus (`IRA-C021 §16`; `observability.py`). No broker, no subscriber, no `Backend/Shared/Events` involvement. `list` / `read` are non-mutating and are not audited (consistent with `role`/`c132` read paths).
- `COM-001-063` confirms `SD-002 §6` Evidence applies to Offering Definition transitions — satisfied by the `record_audit` trail, no new mechanism.

## 17. Transaction Model

`[DESIGN]` / `[PRECEDENT]` Single-row insert in `AuthService`'s own request transaction: `repo.create({...})` → `session.flush()`, with commit deferred to the session dependency context (`BaseRepository` convention). The `offering_reference` **concurrency-safe** property (O1, §9.3) is satisfiable by the standard `except IntegrityError → session.rollback()` → retry discipline `role_service.establish` already demonstrates, against the `UNIQUE` constraint — one acceptable realization, not a mandated one (the mechanism is implementation-design's choice per O1). No cross-service transaction — there is no second writer (§5).

## 18. Idempotency / Concurrency

`[DESIGN]` No content-level idempotency: `(offering_name, offering_kind)` is not a natural key (§9.5), so a double-submitted establish creates two distinct `draft` offerings, each with its own `offering_reference` — `COM-001 §6` names no invariant forbidding this. This mirrors `c132_notification` / `TD-152`'s disposition: idempotency-mechanism selection is `[IMPLEMENTATION-TIME]`, requiring no RO decision unless a concrete concurrency risk is later identified. The only concurrency point requiring handling is `offering_reference` assignment (§17), covered by the `UNIQUE` backstop + retry.

## 19. Lifecycle and Temporal Semantics

`[DESIGN]` BA-01 lifecycle: establish → persists in `state='draft'`. No transition. `version=1`, `supersedes_id=NULL` always. `created_at` at establish; `updated_at` only if a future increment mutates the row. No `effective_from`/`effective_to` (§9.10). **Retention:** an Offering Definition is a permanent commercial record (`COM-001-025` — "never deletion"); no purge/archive mechanism is designed, and its absence weakens no audit, security, or tenant-isolation boundary. `[FUTURE TDS QUESTION]`: alignment with any general retention floor at the Version Management increment.

## 20. Security Considerations + Negative-Control Security Tests

`[DESIGN]` Standard bearer-token auth on every route; `require_platform_admin` gate (§10); tenant-middleware-exempt prefix (§11). No cross-service call, no internal-service-auth surface (contrast `TDS-C132 §18`). The eventual implementation's test suite SHALL include, before submission for Independent Certification:

1. **Authorization negative controls** — a caller **without** `PLATFORM_ADMIN` receives 403 on `POST /offerings`, `GET /offerings`, and `GET /offerings/{id}`; a caller **with** `PLATFORM_ADMIN` receives 201 / 200; a request with a missing/malformed `Authorization` header receives 400; an invalid/expired token receives 401.
2. **Platform-global schema assertion** — an automated assertion that `c021_offering_definition` has **no `organization_id` column** and no tenant-scoping column of any kind (the structural expression of D8).
3. **`list_price_reference` non-computation** — the response echoes the supplied reference string verbatim; no endpoint returns a numeric/derived price; the request schema rejects a JSON number for `list_price_reference` (Pydantic `str | None`).
4. **Closed-set enforcement** — `offering_kind` outside `{PRODUCT, SERVICE}` → 422; `state` is not acceptable as a request field (always `'draft'`).
4a. **Optional `category_ref` (O2)** — a `POST /offerings` body **omitting** `category_ref` → 201, row persisted with `category_ref = NULL`, BA-01 raises no error; a non-empty `category_ref` → persisted verbatim; an empty-string `category_ref` → 422. No taxonomy/category endpoint exists to call.
5. **Read isolation** — `GET /offerings/{random-uuid}` → 404 (no server error, no disclosure).
6. **Purpose-built runtime probe (per `CLAUDE.md §19.7b` method requirement for the later V&V gate)** — a from-scratch probe, not adapted from the suite above, exercising establish → list → read end-to-end against a real `AuthService` instance and asserting the persisted row shape, the `record_audit` trail, and the `draft` state. (A negative control against pre-fix code is N/A — BA-01 is greenfield, no remediation.)
7. **`CLAUDE.md §21.4` Mandatory Tenant-Isolation Test Checklist** — **structurally not applicable** (the data model carries no organization/tenant boundary, `[RO DECISION]` D8), the same disposition as `/roles`. Per `IRA-C021 §11` / `CLAUDE.md §19.4`, the **substitute assurance** is items 1 + 2 above (authorization gate + no-`organization_id` schema assertion), and this substitution SHALL be explicitly recorded in the WP-20 BA-01 charter and re-affirmed in the Implementation Report — not silently assumed.

## 21. Migration Considerations

`[DESIGN]` **No migration, ORM model, or table is created, drafted, or authorized by this document.** The eventual physical migration lives at `Backend/Services/AuthService/alembic/versions/<date>-<rev>_c021_offering_definition.py`, mirroring `2026_09_05_0900-d4e5f6a7b8c9_c132_notification.py`. `[FACT]` `down_revision = 'd4e5f6a7b8c9'` (the current `AuthService` head — the c132 notification migration; verified by direct `ls` of `alembic/versions/`). Purely additive: one `op.create_table` + the UNIQUE index + any implementation-time indexes. **If the chosen `offering_reference` generation mechanism (O1, §9.3) requires a new database object (e.g. a sequence), that object is introduced through the normal `CLAUDE.md §18`/`§19.4` change-control process at implementation time — it is neither presupposed nor pre-authorized here.** **No `ALTER` to any existing table.** Not created until a WP/BA charter and explicit Implementation Authorization exist.

## 22. CBOR ADR + BAR Registration Prerequisites (explicit)

`[FACT]` Restated from §7 for prominence, per the Repository Owner's instruction that these be explicitly identified:
1. **CBOR registration ADR** — a dedicated ADR registering the Offering Definition Business Object (`CMD-001 §26.4`, `COM-001-005`, `COM-001-061`), mirroring `ADR-019`. **MANDATORY before implementation. NOT created by this TDS.**
2. **BAR registration** — the BA-01 Business Activity registered in the Business Activity Registry (`COM-001-060`). **MANDATORY before implementation. NOT performed by this TDS.**

Neither blocks this TDS's preparation or its independent review; both gate Implementation Authorization.

## 23. Deferred Governance Questions (restated precisely, not reinterpreted)

- `[RO DECISION]` D7 — `draft → published` and `published → retired` transitions; the offering approval-authority Pending Canonical Binding (`COM-001-026`) — deferred to a future increment; **not silently solved** by BA-01 (which stays in `draft`).
- `[RO DECISION]` D8 — a future tenant-scoped catalog overlay; a canonical Catalog Governance Authority — each deferred with a recorded trigger (`ROD-C021 §K`).
- `[RO DECISION]` D5 — composition and relationships — future increments.
- `COM-001-024` catalog taxonomy governance authority — Pending Canonical Binding. `category_ref` is an **optional** opaque free-text reference (`[RO DECISION]` O2, §9.8); a future taxonomy binding may later govern its vocabulary in a subsequent C-021 increment, but BA-01 introduces **no** taxonomy authority, **no** category management, and **no** free-form taxonomy.
- Pricing Execution (C-024) — Pending Canonical Binding; out of scope (§3, §9.9).
- `PE-001-C021` masthead doc-sync debt ("Primary Specification Reference: SD-001" vs. the true `COM-001`) — non-blocking; **not corrected by this TDS** (no spec/locked document is modified here); for a future `PE-001` maintenance pass (`IRA-C021 §23`).

## 24. C-023 Decision 3 Preservation

`[FACT]` **C-023 Decision 3 is untouched and not fired by this TDS.** BA-01 (per D3/D4 and §3/§6/§9.10) models a commercial Offering Definition only — it creates, modifies, and governs **no** entitlement type or feature definition, and defines **no** cross-reference from an offering to an entitlement type. `IRA-C023 §21.12`'s Decision-3 trigger ("implementation need … for another formally chartered capability that requires creation, modification, or governance of global Entitlement Types/Feature definitions") is therefore not met. This TDS modifies no C-023 / WP-17 artifact and no C-023 Decision. **Disclosure (from `ROD-C021 §F`):** a *future* C-021 increment adding an "entitlement types conferred by this offering" cross-reference *would* fire C-023 Decision 3 — **BA-01 as designed does not.**

## 25. Requirements Traceability Matrix / Acceptance Criteria

| # | Requirement (source) | Design element (this TDS) | Acceptance criterion |
|---|---|---|---|
| 1 | Establish a standalone Atomic Offering Definition (D4) | `POST /offerings` → `OfferingDefinitionService.establish` → `c021_offering_definition` insert (§9, §12, §13) | A `PLATFORM_ADMIN` `POST /offerings` with valid body returns 201 and a persisted row with `state="draft"`, `version=1`, `supersedes_id=NULL`. |
| 2 | Canonical identity, `PREFIX-NNNNNN` (D4; `COM-001-001`; `[RO DECISION]` O1) | `offering_reference` String(≈30) UNIQUE, meeting the O1 acceptance properties — system-assigned, monotonic, `PREFIX-NNNNNN`, unique, concurrency-safe; mechanism is implementation-design's choice (§9.3) | Response carries a unique `offering_reference` matching `^[A-Z]+-\d{6}$` (exact prefix token aligns with the CBOR Business Object Identifier); the caller cannot supply or override it; two establishes yield distinct, increasing references; concurrent establishes never collide or error. |
| 3 | Canonical name (D4) | `offering_name` String(255) NOT NULL (§9.1) | Empty/whitespace name → 422; a valid name is persisted and echoed. |
| 4 | Product / Service classification (D4; `COM-001-021` Product↔Service axis) | `offering_kind` String(20) CHECK `IN ('PRODUCT','SERVICE')` (§9.1) | `offering_kind` outside the set → 422; `PRODUCT`/`SERVICE` persist. Digital/Physical not accepted (excluded, §3). |
| 5 | Opaque category reference (D4; `COM-001-024`; `[RO DECISION]` O2) | `category_ref` String(≈100) **NULLABLE**, optional, non-FK opaque string (§9.1, §9.8, §13) | Omitting `category_ref` → 201 with `category_ref = NULL`, BA-01 raises no error; a non-empty value persists verbatim; an empty-string value → 422; no taxonomy table, FK, or category-management endpoint exists. |
| 6 | Optional opaque list-price reference (D6) | `list_price_reference` String(100) NULLABLE, non-numeric, non-computed (§9.9) | Omitting it → row persists with `NULL`; supplying a string → echoed verbatim; a JSON number → 422; no endpoint returns a computed price. |
| 7 | Current state = draft (D7) | `state` String(20) CHECK `IN ('draft','published','retired')`, default+only `'draft'`; no transition endpoint (§9.4, §13) | Every established row has `state="draft"`; there is no route to change it; `state` is not a request field. |
| 8 | List Offering Definitions (D4) | `GET /offerings` → `repository.list_all(limit=_LIST_HARD_CAP)`, newest-first, no tenant filter (§12, §13) | A `PLATFORM_ADMIN` `GET /offerings` returns all rows (up to the cap), newest first, with no `X-Tenant-ID` required. |
| 9 | Read one Offering Definition (D4) | `GET /offerings/{offering_id}` by UUID (§13) | Valid id → 200 with the row; unknown id → 404; non-`PLATFORM_ADMIN` → 403. |
| 10 | First Authoritative Offering Definition Context + stable Offering Reference (D4; `COM-001-002`, `ERB-C021-06`) | The persisted row is the Authoritative Context; `offering_reference` is the stable, opaque, externally-citable reference (§6, §9.3) | `offering_reference` is stable across reads and unique; it is the value a future C-020/C-024/C-025 would store. |
| 11 | Platform-global catalog, no tenant anchor (D8) | No `organization_id` column; `require_platform_admin`; tenant-middleware exempt (§9.1, §10, §11) | Schema assertion: no `organization_id`. `GET /offerings` needs no `X-Tenant-ID`. Precedent parity with `/roles`. |
| 12 | Authorization (D8; `IRA-C021 §11`) | `Depends(require_platform_admin)` on all 3 routes (§10) | Non-admin → 403 on all routes; admin → success. |
| 13 | Audit / Evidence (`COM-001-063`, `SD-002 §6`) | `record_audit` + `publish_event` on establish, existing infra (§16) | An `ESTABLISH_OFFERING_DEFINITION` audit record is emitted on success and on denied validation paths. |
| 14 | BO eligibility → CBOR + BAR (`COM-001-005`/`-060`/`-061`) | Prerequisites recorded, not performed (§7, §22) | The WP-20 charter cannot pass Implementation Authorization without the CBOR ADR and BAR registration complete. |
| 15 | Frontend demonstrability (`CLAUDE.md §20.3`/`§20.4`) | `features/offering-catalog/` — list + detail + establish screens, real API, 5 UI states (§14) | A `PLATFORM_ADMIN` persona can establish, list, and read an Offering Definition through the running UI against the real API. |
| 16 | C-023 Decision 3 preserved (`ROD-C021 §F`/`§R`) | No entitlement/feature column, no offering→entitlement cross-reference (§9.10, §24) | No C-023 artifact is modified; no entitlement-type creation/governance path exists in BA-01. |

`[DESIGN]` No requirement above was manufactured — every row traces to a `ROD-C021` D-decision, a `COM-001`/`PE-001-C021` clause, or an `IRA-C021` finding.

## 26. Implementation Sequencing (informative — not authorized by this document)

If implementation is later authorized: (1) CBOR registration ADR + BAR registration (§22); (2) migration `c021_offering_definition` (plus any new database object the chosen `offering_reference` mechanism requires — via `CLAUDE.md §18`/`§19.4`, O1/§9.3/§21); (3) model → repository → service → router → `main.py` wiring + `middleware/tenant.py` exemption; (4) schema + Pydantic contracts; (5) tests per §20; (6) frontend feature folder + screens + nav; (7) IMP-REPORT-WP-20; (8) `CLAUDE.md §19.7b` five-gate closure. **None of this is authorized here.**

## 27. Implementation-Time vs TDS-Level Questions (explicit separation)

**Resolved at TDS level (this document):** scope/non-scope (§2/§3); host = `AuthService` (§5); BO boundary (§6); BO eligibility + CBOR/BAR prerequisites (§7, §22); conceptual schema shape (§9); `category_ref` OPTIONAL / NULLABLE per `[RO DECISION]` O2 (§9.1, §9.8); identity-generation **requirement** = the O1 acceptance properties — system-assigned, monotonic, `PREFIX-NNNNNN`, unique, concurrency-safe (§9.3); authority model = `require_platform_admin` (§10); tenant-middleware exemption (§11); layer boundaries (§12); API endpoint shape (§13); frontend shape (§14); DS-001 target (§15); audit pattern (§16); transaction posture (§17); idempotency posture (§18); lifecycle floor (§19); security-test requirements incl. the `§21.4` substitute assurance (§20); migration `down_revision` (§21); RTM (§25).

**Left to implementation time (no further TDS or RO decision):** the concrete `offering_reference` generation **mechanism**, provided it meets the O1 acceptance properties (§9.3) — a DB sequence, an in-transaction `MAX+1` with retry, an application allocator, or an equivalent; **any new database object that mechanism requires goes through `CLAUDE.md §18`/`§19.4`** (§21); exact prefix token (`OFFERING-`/`OFF-`/`OFR-`/`OFD-`, to align with the CBOR id); exact `String` length bounds and index/constraint naming (§9.6); whether `ix_c021_offering_definition_state`/`_offering_kind` are added; whether a `GET /offerings/by-reference/{ref}` lookup is added (§13); exact frontend component selection and nav slug/label (§14, §15); exact repository/service method signatures.

**`[FUTURE TDS QUESTION]` (a later C-021 increment's own TDS):** `draft → published` / `published → retired` transitions and their approval authority (§23); a partial-unique index on `offering_reference` if in-place versioning is added (§9.5); governance of `category_ref`'s vocabulary **if** `COM-001-024` catalog taxonomy authority later binds — BA-01 introduces no such machinery (§9.8, §23); composition and relationships (§3); a tenant-scoped catalog overlay and a canonical Catalog Governance Authority (§23).

**Requires the Repository Owner, not decidable at TDS or implementation time:** none remaining. The host is decided (§5); the schema-shape STOP-and-report surfaced no further blocking RO decision, and the two items it flagged for attention (identity generation, `category_ref` nullability) are now decided by Repository Owner decisions O1 and O2 (§9.11).

## 28. TDS Quality Gate (self-check before Independent Review)

Performed against `ROD-C021`, `IRA-C021`, `COM-001`, `PE-001-C021`, and `CLAUDE.md`'s governance rules, before submission for independent review:

| Check | Result |
|---|---|
| Every design decision verified against `ROD-C021` D1–D8 | ✅ §§2–27 each cite the controlling D-decision; no decision reinterpreted or extended |
| No excluded scope entered the TDS | ✅ §3 non-goals restated verbatim; §9.10 lists what is deliberately absent from the schema; no composition/relationship/publication/retirement/pricing-compute/subscription/customer/entitlement/tenant-overlay element appears in §9, §13, or §14 |
| Service-hosting decision matches the explicit RO decision | ✅ §5 records Option A — `AuthService`, verbatim |
| No schema designed beyond the approved BA-01 boundary | ✅ §9 fields map 1:1 to D4's in-scope list + audit/lifecycle-shape columns declared-not-exercised (`version`/`supersedes_id`) with the `c023_*`/`roles` precedent; no speculative column |
| CBOR + BAR prerequisites explicitly identified | ✅ §7, §22, §25 row 14 — recorded as mandatory-before-implementation, not performed here |
| No CBOR ADR created; no BAR registration performed | ✅ §7, §22 — explicitly not done |
| No locked/spec/governance document modified | ✅ §30 change-control — `COM-001`, `PE-001`, `PE-001-C021`, `CAP-001`, C-023 artifacts, `CBOR-INDEX.md`, `WPR-001`, `ADR-036` all read-only |
| No implementation, migration, model, code, frontend, or test created | ✅ §21, §26 — design-level only |
| `IRA-C021` remains 🟡 AMBER (not re-classified) | ✅ §29 |
| Tenant-isolation `§21.4` inapplicability disclosed + substitute assurance mandated | ✅ §20 item 7 |
| C-023 Decision 3 preserved | ✅ §24 |
| **O1 applied** — identity generation is a set of acceptance properties (system-assigned / monotonic / `PREFIX-NNNNNN` / unique / concurrency-safe), NOT a mandatory PostgreSQL `SEQUENCE`; a new DB object, if needed, via `CLAUDE.md §18`/`§19.4` | ✅ status header, §9.3, §9.11, §17, §21, §26, §27 |
| **O2 applied** — `category_ref` is OPTIONAL / NULLABLE; still an opaque reference only; no taxonomy governance, category management, or free-form taxonomy introduced; `ROD-C021` not reopened | ✅ status header, §9.1, §9.8, §9.11, §13, §20 item 4a, §23, §25 row 5, §27 |

## 29. Readiness Implications

`[DESIGN]` This TDS's preparation does not, by itself, change `IRA-C021`'s recorded classification. **`IRA-C021` remains 🟡 AMBER.** AMBER's TDS-preparation half is now satisfied (this document exists, within boundary, host resolved, schema-shape STOP-and-report performed with no further blocking RO decision). AMBER's Implementation-Authorization half is unaffected — **WP-20 registration, the BA-01 charter, the CBOR ADR, BAR registration, and a separate explicit Repository Owner Implementation Authorization all remain prerequisites this document does not perform.**

## 30. Change Control

**Files created by this pass:** this document only — `architecture/05-Implementation/TDS-C021_Product_and_Service_Catalog_Minimum_BA_Technical_Design.md`.

**Files read for cross-reference, not modified:** `CAP-001` (line 75), `COM-001` (§4, §6 [`COM-001-001`/`-002`/`-005`/`-020`…`-026`/`-060`/`-061`/`-063`]), `PE-001-C021` (v1.1 — §1.3/§1.5/§1.9/§1.11/§1.16/§1.24/§2.10, ERB/EX list), `ROD-C021-Product-and-Service-Catalog-Capability-Boundary-and-Minimum-Scope.md` (D1–D8), `IRA-C021_Product_and_Service_Catalog_Implementation_Readiness_Assessment.md` (§8/§9/§11/§16/§17/§22/§23), `CMD-001 §26.3a`/`§26.4`, `IRA-C023 §21.12`, `ADR-036`, `ADR-019`, `TDS-C132` / `TDS-C023` / `TDS-C023-A`, `CLAUDE.md §8`/`§18`/`§19.1`/`§19.4`/`§19.7b`/`§20`/`§21.3`/`§21.4`, and — by direct code inspection — `Backend/Services/AuthService/`: `models/role.py`, `models/c132_notification.py`, `models/c023_entitlement_context.py`, `dependencies.py`, `middleware/tenant.py`, `repositories/base_repository.py`, `services/role_service.py`, `routers/role.py`, `routers/entitlement_license.py`, `routers/notification.py`, `main.py`, `alembic/versions/` (head rev `d4e5f6a7b8c9`), and `source/frontend/src/config/admin-navigation.ts`.

**Not modified:** any LOCKED constitutional document (`COM-001`, `PE-001`, `PE-001-C021`, `CAP-001`, `SD-001`, `SD-002`, `SD-003`, `URA-001`, `CMD-001`, `GRC-001`, `PLT-001`, `RTA-001`, `EIA-001`, `DS-001`, `ARCH-000`, `ADR-002`/`003`/`016`/`023`/`036`); any C-023 / WP-17 artifact or C-023 Decision (Decision 3 untouched, §24); `CBOR-INDEX.md`; `SER-001`; `HISTORICAL-SCREEN-REALIZATION-MATRIX.md`; `EXECUTIVE-COGNITION-REALIZATION-STRATEGY.md`; `WPR-001`; `WP-REG-001`; `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md`; `ROD-C021`; `IRA-C021`; any `Backend/` or `source/frontend/` file, migration, or test; any unrelated pre-existing working-tree change. **No WP registered. No BA charter created. No CBOR ADR created. No BAR registration performed. No implementation of any kind.** Nothing was staged, committed, or pushed.

*End of TDS-C021 (PREPARED FOR INDEPENDENT REVIEW).*
