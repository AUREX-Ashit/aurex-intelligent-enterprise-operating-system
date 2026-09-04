# TDS-C023-A — C-023 / WP-17 BA-01 Entitlement/License Registry Schema — Implementation-Time Technical Design

**Document ID:** TDS-C023-A (implementation-time schema Technical Design supplementing `TDS-C023`; the "dedicated implementation-time Technical Design for the schema" mandated by `IMP-REPORT-WP-17 §4(1)` and recommended by `STOP-AND-REPORT-WP-17-01 §D`/`§E`).
**Capability / Work Package:** C-023 Licensing & Entitlement / WP-17 BA-01 — Establish Entitlement/License Context (Administrative).
**Repository state:** commit `c2f93d5` (`main`).
**Type:** **DESIGN ONLY.** No production model, repository, service, router, Pydantic schema, or test is created by this document. **No Alembic migration is created or run by this document.** No existing governance document is modified. `TDS-C023`, `IRA-C023`, the `WP-17` charter, `WPR-001`, `TDS-018`, `WP-18`, and C-023 Decisions 1–6 are **read-only inputs** here and are **not** altered.
**Governing basis (cited, not restated):** `WP-17` charter; `IMP-REPORT-WP-17 §1`–`§8` (the recorded Implementation Authorization and its `§4(1)` STOP-and-report obligation); `TDS-C023` (accepted, twice independently reviewed) `§5`/`§6`/`§7`/`§10`/`§14`/`§15`/`§16`/`§17`; `IRA-C023 §18.13` (Decision 6), `§19.13` (Decision 1), `§20.12`/`§21.12`/`§22.13`/`§23.13` (Decisions 2/3/4/5); `ADR-036` (Accepted — `AuthService` host, modular-monolith phase); certified `WP-18`/`TDS-018` (`membership_approval_authority`, `resolve_approval_authority()`, `require_approval_authority()`); `Master_Technical_Architecture.md` (`license_registry`/`entitlement_registry` canonical definitions, lines 1610–1635; RLS lines 4777–4826; schema catalog lines 330–331); `URA-001-111`/`-112`/`-115`/`-116`/`-117`/`-118`/`-119`/`-148`; `CLAUDE.md §8`/`§18`/`§19.1`/`§19.4`/`§19.7b`/`§21.4`; AuthService precedents `models/{membership,approval_authority,membership_approval_authority,authority_holder,tenant_registry}.py`, `services/tenant_establishment_service.py`, `observability.py`, `middleware/tenant.py`.

> **NO SELF-AUTHORIZATION.** Creating this Technical Design does **not** authorize implementation, does **not** approve a schema, and does **not** create or run a migration. ~~The schema shape remains an open `CLAUDE.md §18`/`§19.4` decision requiring explicit Repository Owner / architectural approval — see `§19` (REPOSITORY OWNER / ARCHITECTURAL DECISION REQUIRED). Until that approval is recorded, WP-17 / BA-01 implementation of the persistence layer and everything downstream of it (`§16`) remains HALTED.~~ *(Superseded 2026-09-01 — final pre-Gate-1 governance cleanup, per direct Repository Owner authorization. The Repository Owner's schema decision (D-1…D-7) is **RECORDED** at `§19.1`; implementation subsequently resumed and is **COMPLETE**, independently reviewed **SOUND** (`IMP-REPORT-WP-17 §11`). The `§19` heading was renamed at that time — the "REQUIRED" suffix removed — see `§19` / `§19.1`. **Current status: WP-17 / BA-01 = IMPLEMENTATION AUTHORIZED — IMPLEMENTATION COMPLETE — NOT YET CERTIFIED** (certification pending a fresh `CLAUDE.md §19.7b` Gate 1). This note changes no D-1…D-7, `§19.1`/`§19.2`, or schema content, and does not itself certify WP-17.)*

---

## 1. The exact schema decision

BA-01 must persist the **Authoritative Entitlement Context** and/or **Authoritative License Context** — "the current, single, canonical fact per anchor; exactly one per Entitlement Anchor; exactly one per Membership Anchor" (`TDS-C023 §5-A`). To write the SQLAlchemy model(s) and the Alembic migration, exactly one of the following table shapes must be chosen, and the canonical sources do not uniquely determine it:

- **Option A — two tables** (`license_registry` + `entitlement_registry`), mirroring the MTA canonical split, each minimally extended with only the columns `TDS-C023 §5-A`/`§14`/`§16` demonstrably require.
- **Option B — one table** (`entitlement_license_registry`), per the `TDS-C023 §6.3` item 2 sketch, with a discriminator and two nullable anchor columns.
- **Option C — any other genuinely viable canonical option.** §17 examines whether one exists; conclusion: **no third canonical option is supported** (a `memberships`/`organizations` column extension is barred by Decision 6 and by `URA-001-112`/`-148`; an events-only or view-only representation cannot hold "the current single authoritative fact per anchor" the BA requires).

Coupled sub-decisions, each part of the same approval (§3, §7, §10):
- **S-1** hard intra-service foreign key vs referenced UUID (`§7`);
- **S-2** whether BA-01's schema includes a nullable `c023_license_type` column for the four `URA-001-115` specialized license types, or defers it (`§4.4`);
- **S-3** the precise database-level uniqueness enforcement for INV-C023-09 / INV-C023-10 (`§10`), including the `domain_id`-NULL handling on the Entitlement side.

---

## 2. Canonical evidence for each option

### 2.1 Evidence for a two-table shape (Option A)

| # | Canonical statement | Source |
|---|---|---|
| E-A1 | `license_registry` and `entitlement_registry` are defined as **two separate `CREATE TABLE` statements**. | `Master_Technical_Architecture.md` lines 1615–1619, 1629–1635 |
| E-A2 | `entitlement_registry`'s PURPOSE comment: "Feature/module entitlements at the organization level — **explicitly separate from license_registry**, which governs per-membership licensing rather than org-wide feature enablement." | MTA line 1622–1625 |
| E-A3 | Schema-catalog: "`license_registry` — per-membership license grant (URA-001-111)"; "`entitlement_registry` — org-level feature entitlements, **separate from licensing** (URA-001-112)". | MTA lines 330–331 |
| E-A4 | `URA-001-112`: "Entitlements Are Separate From Licenses — licenses define user counts; entitlements define capabilities." `URA-001-148`: "Entitlements Are Independent of Licenses — restated structurally." | `URA-001` lines 225, 281 |
| E-A5 | The two tables have **different anchors and different RLS**: `entitlement_registry` isolates directly on `organization_id`; `license_registry` isolates via a join through `membership_registry.organization_id`. | MTA lines 4777–4778, 4820–4826 |
| E-A6 | `TDS-C023 §11`: "Entitlement … and License … are independently authoritative, **never conflated**, per `URA-001-112`/`148` and `BR-C023-03`." | `TDS-C023 §11` |
| E-A7 | `BR-C023-03` (per `IRA-C023`/`TDS-C023`): Entitlement keyed to Organization (optionally Domain); License keyed to Membership — never conflated. | `IRA-C023 §4`; `TDS-C023 §11` |
| E-A8 | Precedent: `tenant_registry` (`TDS-016`) is a new AuthService registry table implementing **only** the columns its governing TDS specifies, explicitly omitting MTA-draft columns outside the chartered scope. Two focused tables extended minimally is the same discipline. | `models/tenant_registry.py` docstring; `TDS-016 §5` |

### 2.2 Evidence for a one-table shape (Option B)

| # | Canonical statement | Source |
|---|---|---|
| E-B1 | `TDS-C023 §6.3` item 2: "**recommended design**: a new C-023-owned record (**working name**: `entitlement_license_registry`) … keyed by `membership_id` (a referenced UUID, not a hard cross-service database foreign key)". | `TDS-C023 §6.3` item 2 |
| E-B2 | `TDS-C023 §6.3` item 12: "a new table (`entitlement_license_registry` **or equivalent**) … this document proposes the design; it does not create the table". | `TDS-C023 §6.3` item 12 |
| E-B3 | `TDS-C023 §6.3` items 5, 6, 10, 11, 13 describe **one** "C-023 License record" with a `status`, `effective_from`/`effective_to`, an Entitlement Source Reference, and a read-only reference to `membership.license_type`. | `TDS-C023 §6.3` |
| E-B4 | `TDS-C023 §24` item 1 (post-R7, `c2f93d5`): the service host is resolved (`ADR-036` — `AuthService`); the "schema-shape question (one table or two; exact columns, constraints, indexes)" is explicitly still open. | `TDS-C023 §24` item 1 |

### 2.3 Where the two bodies of evidence conflict — and why the MTA verbatim shape is not directly usable

- `TDS-C023 §6.3` sketches **one** record; the MTA defines **two** tables. `§6.3` item 2's own text hedges ("recommended", "working name", "or equivalent") and `§6.3` item 12 / `§23` route the **actual** shape to a `CLAUDE.md §18`/`§19.4` STOP-and-report — i.e. the TDS itself did not finalise this.
- **The MTA's `license_registry` cannot be implemented verbatim:** its `license_type VARCHAR(50)` column would be a C-023-owned copy of the `FULL`/`LIGHT` value, which **Decision 6** (`§4`) and `TDS-C023 §6.3` item 11 ("**the single most important design constraint**") forbid.
- **The MTA's tables are also insufficient for BA-01 as chartered:** neither carries a lifecycle `status`, an Entitlement Source Reference, an authority reference, an actor/accountability reference, or a uniqueness constraint for the single-current-context invariant — all required by `TDS-C023 §5-A`/`§14`/`§15`/`§16`.

Both options therefore add columns beyond the MTA canonical definitions and require the `CLAUDE.md §18`/`§19.4` decision this document exists to obtain.

---

## 3. Proposed logical data model — RECOMMENDED option (Option A, two tables)

> Presented as the **recommended** shape for the Repository Owner to approve, reject, or amend (`§18`, `§19`). Not built. Column types are the PostgreSQL production target (`CLAUDE.md §9`, `Master_Technical_Architecture.md` standard); the SQLite test harness (`conftest.py`) maps them as every existing AuthService model already does.

### 3.1 Table `c023_license_context` — Authoritative License Context (Membership-anchored)

| Column | Type | Null | Notes |
|---|---|---|---|
| `id` | `UUID` | NOT NULL | **PK**, `default uuid4` — the record's own canonical identity and the audit correlation id (`TDS-C023 §16`). Mirrors `memberships.id` / `approval_authorities.id`. |
| `membership_id` | `UUID` | NOT NULL | The Membership Anchor (`TDS-C023 §6.3` item 3). Reference strategy per **S-1** (`§7`): recommended a hard intra-service FK `REFERENCES memberships(id)` (both tables AuthService-owned, `ADR-036`) — mirroring WP-18's own `membership_approval_authority.membership_id → memberships.id`. Indexed. |
| `status` | `VARCHAR(20)` | NOT NULL | `ACTIVE` / `SUSPENDED` / `REVOKED` (`PE-001-C023 §5.5`; `TDS-C023 §6.3` item 6). **BA-01's service only ever writes `ACTIVE`** (`§9`). `CHECK (status IN ('ACTIVE','SUSPENDED','REVOKED'))` — the value set is canonically grounded, mirroring `approval_authority.py`'s own `VersionStatus` CHECK; the transitions that would produce `SUSPENDED`/`REVOKED` are **out of BA-01 scope** and not implemented. |
| `effective_from` | `TIMESTAMPTZ` | NOT NULL | Independent Commit-time business date (`TDS-C023 §10.1`), `default now()`; caller-supplied when provided, never derived from any Subscription. Mirrors `memberships.effective_from`. |
| `effective_to` | `TIMESTAMPTZ` | NULL | NULL while this context remains the current one. A context is closed by setting `effective_to` (soft-close), never hard-deleted — the same convention `membership_approval_authority` / `authority_holders` / `approval_authorities` already use. **BA-01 never closes a context** (`§9`); this column exists for the invariant in `§10` and for future lifecycle BAs. |
| `entitlement_source_reference` | `VARCHAR(255)` | NULL | Free-text citation of the non-authoritative Entitlement Source Reference (Subscription id, Contract id, or `"ADMINISTRATIVE"` for a direct grant) — `TDS-C023 §6.2`/`§6.3` item 10, `BR-C023-02`. Never itself treated as an authoritative fact. Free-text, mirroring `approval_authority.approval_reference`. |
| `approval_authority_id` | `UUID` | NOT NULL | The `approval_authorities` row that authorized this Commit (`TDS-C023 §5-A` "Authority reference", `§7`). Reference strategy per **S-1**: recommended a hard intra-service FK `REFERENCES approval_authorities(id)` (mirroring `membership_approval_authority.approval_authority_id → approval_authorities.id`). Indexed. |
| `committed_by_actor_id` | `UUID` | NOT NULL | The `person_id` of the caller who satisfied the resolved Commit Authority (`TDS-C023 §16`). **Not** a foreign key — a point-in-time audit citation, mirroring `tenant_registry.approved_by_actor_id` / `allocated_by_actor_id` (which `TDS-016 §11` deliberately made non-FK "point-in-time audit citations, not live references"). |
| `committed_at` | `TIMESTAMPTZ` | NOT NULL | When the Commit occurred, `default now()`. Mirrors `tenant_registry.approved_at`. |
| `c023_license_type` | `VARCHAR(50)` | NULL | **Sub-decision S-2** (`§4.4`): the four `URA-001-115` specialized license types (`SUPPLIER` / `AUDITOR` / `BOARD_MEMBER` / `CONSULTANT`). **This is NOT a copy of `memberships.license_type`** (which is `FULL`/`LIGHT` only — `§4`). Recommended: **include as nullable now**, `CHECK (c023_license_type IS NULL OR c023_license_type IN ('SUPPLIER','AUDITOR','BOARD_MEMBER','CONSULTANT'))`, since `URA-001-115` is canonical and `TDS-C023 §6.2` names it as C-023-owned; BA-01's establish path may set it or leave it NULL. Alternative: defer the column entirely to a later BA. **Requires explicit approval.** |
| `created_at` | `TIMESTAMPTZ` | NOT NULL | `default now()`. |
| `updated_at` | `TIMESTAMPTZ` | NULL | `onupdate now()`. |

**Primary key:** `(id)`.
**Foreign keys (recommended, S-1):** `membership_id → memberships(id)`; `approval_authority_id → approval_authorities(id)`. Both intra-service.
**Indexes:** btree on `membership_id`; btree on `approval_authority_id`.
**Uniqueness (S-3, `§10`):** partial unique index `ux_c023_license_context_current` on `(membership_id)` `WHERE effective_to IS NULL` — enforces INV-C023-10 ("exactly one current Authoritative License Context per Membership Anchor"). Cross-dialect (`postgresql_where` + `sqlite_where`), exactly as `ux_membership_approval_authority_active` and `ux_authority_holders_active_authority` already are.
**RLS (production):** `USING (membership_id IN (SELECT id FROM memberships WHERE organization_id = NULLIF(current_setting('app.organization_id', true), '')::uuid))` — the same one-hop-via-membership pattern the MTA specifies for `license_registry` (E-A5) and that `domain_permission_registry` already uses in AuthService.

### 3.2 Table `c023_entitlement_context` — Authoritative Entitlement Context (Organization-anchored, optionally Domain-scoped)

| Column | Type | Null | Notes |
|---|---|---|---|
| `id` | `UUID` | NOT NULL | **PK**, `default uuid4` — record identity + audit correlation id. |
| `organization_id` | `UUID` | NOT NULL | The Entitlement Anchor (`TDS-C023 §11`, `BR-C023-03`). Reference strategy per **S-1**: recommended hard intra-service FK `REFERENCES organizations(id)` (mirroring `approval_authority.organization_id → organizations.id`). Indexed. |
| `domain_id` | `UUID` | NULL | Optional Domain scoping (`TDS-C023 §11` "optionally Domain-scoped"). FK `REFERENCES domains(id)` when set — mirroring `approval_authority.domain_id`. NULL = organization-wide entitlement. |
| `entitlement_type_ref` | `VARCHAR(100)` | NOT NULL | An **already-recognized** Entitlement Type identifier only (`TDS-C023 §5-A`, `§19`; Decision 3 deferred — **no type-creation, no catalog write**). Free-text identifier of an existing recognized type (e.g. `IFRS_ENABLED`, `AI_DISCOVERY_ENABLED`, `SUPPLIER_PORTAL_ENABLED` — `URA-001-112` examples). **The recognition/lookup mechanism is a separate open item** (`TDS-C023 §19` / `§21.6`) — see `§9.3`. |
| `status` | `VARCHAR(20)` | NOT NULL | `ACTIVE` / `SUSPENDED` / `REVOKED`, `CHECK` as `§3.1`. BA-01 writes only `ACTIVE`. |
| `effective_from` | `TIMESTAMPTZ` | NOT NULL | Independent Commit-time business date (`URA-001-117`: entitlements are time-bound), `default now()`. **Present in the MTA `entitlement_registry` canonical definition already** (E-A1). |
| `effective_to` | `TIMESTAMPTZ` | NULL | NULL while current. Same soft-close convention as `§3.1`. **Present in the MTA definition already.** |
| `entitlement_source_reference` | `VARCHAR(255)` | NULL | As `§3.1`. |
| `approval_authority_id` | `UUID` | NOT NULL | As `§3.1` — FK `REFERENCES approval_authorities(id)`. Indexed. |
| `committed_by_actor_id` | `UUID` | NOT NULL | As `§3.1` — non-FK audit citation. |
| `committed_at` | `TIMESTAMPTZ` | NOT NULL | As `§3.1`. |
| `created_at` | `TIMESTAMPTZ` | NOT NULL | `default now()`. |
| `updated_at` | `TIMESTAMPTZ` | NULL | `onupdate now()`. |

**Primary key:** `(id)`.
**Foreign keys (recommended, S-1):** `organization_id → organizations(id)`; `domain_id → domains(id)` (nullable); `approval_authority_id → approval_authorities(id)`.
**Indexes:** btree on `organization_id`; btree on `(organization_id, entitlement_type_ref)`; btree on `approval_authority_id`.
**Uniqueness (S-3, `§10`):** partial unique index `ux_c023_entitlement_context_current` on `(organization_id, COALESCE(domain_id, '00000000-0000-0000-0000-000000000000'::uuid), entitlement_type_ref)` `WHERE effective_to IS NULL` — enforces INV-C023-09 ("exactly one current Authoritative Entitlement Context per Entitlement Anchor **and entitlement type**"). The `COALESCE` sentinel is required because PostgreSQL treats NULL `domain_id` values as distinct in a plain unique index, which would wrongly permit two concurrent organization-wide entitlements of the same type. Cross-dialect. **The exact NULL-handling technique (`COALESCE` sentinel vs `NULLS NOT DISTINCT` (PG 15+) vs a service-layer guard) is sub-decision S-3 and requires explicit approval.**
**RLS (production):** `USING (organization_id = NULLIF(current_setting('app.organization_id', true), '')::uuid)` — the same direct pattern the MTA specifies for `entitlement_registry` (E-A5).

### 3.3 What is deliberately absent from both tables

- **No `license_type` (`FULL`/`LIGHT`) column** — Decision 6 (`§4`). `c023_license_type` (`§3.1`, S-2) is a *different* concept (the `URA-001-115` specialized types), disjoint from the `memberships` two-value enum.
- **No `granted_capacity` / `consumption` / `available_capacity` / purchased-limit column** — Decision 4 deferred (`TDS-C023 §5-B` / `§6.3` item 7; `URA-001-116`).
- **No billing / commercial / price / currency / contract-line column** — out of scope (`TDS-C023 §5-D` / `§6.3` item 8).
- **No Subscription-alignment column** (`aligned_to_subscription_id`, `renews_with`, `expires_with_subscription`) — Pending Canonical Binding (`TDS-C023 §10.2`, `§9.4`).
- **No catalog / entitlement-type-definition table** — Decision 3 deferred (`TDS-C023 §5-C`); `entitlement_type_ref` is a reference to an *already-recognized* type, not a definition.
- **No `version` / `supersedes_id` column** — BA-01 is establish-only, no version machinery (`TDS-C023 §4`; mirrors `memberships`' own BA-01 "no version/status/supersedes_id machinery, which belongs to a later Business Activity"). A future "Maintain Entitlement/License Terms" BA would add it if needed.
- **No `organization_id` column on `c023_license_context`** — the governing Organization for a License is `memberships.organization_id`, reached one hop (`TDS-C023 §7.4`; mirrors `tenant_registry`'s deliberate omission of a back-reference).

---

## 4. Decision 6 compliance — `memberships.license_type` stays read-only and is not duplicated

`IRA-C023 §18.13` (Decision 6, Split Ownership): `AuthService` `memberships.license_type` (the base `FULL`/`LIGHT` classification) remains `C-007`/`WP-03`-owned; C-023 owns the *governance layer*. `TDS-C023 §6.1`/`§6.3` items 1, 3, 5, 9, 11, 13 design the mechanism. This TDS-C023-A schema complies as follows:

1. **Not modified.** No `ALTER TABLE memberships` of any kind. `memberships.license_type`, its `ck_memberships_license_type` CHECK, its default/server-default, `MembershipService.establish()`, and the certified `BA-03` term-change path are untouched. The migration (`§13`) touches only the two new tables.
2. **Not FK-referenced.** No column in `c023_license_context` or `c023_entitlement_context` is a foreign key to `memberships.license_type`. `c023_license_context.membership_id` references `memberships.id` (the row identity), not the classification value.
3. **Not duplicated.** **No column anywhere in this schema stores a `FULL`/`LIGHT` value.** `c023_license_type` (`§3.1`, S-2) holds the disjoint `URA-001-115` specialized-type set (`SUPPLIER`/`AUDITOR`/`BOARD_MEMBER`/`CONSULTANT`), never `FULL`/`LIGHT`. `TDS-C023 §6.3` item 11's "single most important design constraint" — "the C-023 License record does **not** carry its own copy of `FULL`/`LIGHT`" — is satisfied structurally by the absence of any such column.
4. **Read by value, at read time only.** The `FULL`/`LIGHT` value, where a resolution or an establish-time validation needs it, is read from `memberships.license_type` via `MembershipRepository` at the moment of the operation and used transiently — never persisted into a C-023 table. This is a *service-layer* behaviour (`§16` implementation), enforced by the schema simply not providing a place to store it.
5. **The License governance layer is what C-023 owns and this schema persists** — lifecycle `status`, `effective_from`/`effective_to`, `entitlement_source_reference`, the authority/actor references, and (if S-2 approved) the specialized type. `TDS-C023 §6.3` item 13's source-of-truth table maps exactly: `memberships.license_type` → C-007; License lifecycle/effective period/source reference → C-023, these new tables.

**Result:** Decision 6 is complied with by construction — there is no schema pathway by which C-023 could write, copy, or independently maintain the `FULL`/`LIGHT` classification.

---

## 5. License vs Entitlement separation — `URA-001-112` / `URA-001-148` / `BR-C023-03`

- `URA-001-112`: "Entitlements Are Separate From Licenses — licenses define user counts; entitlements define capabilities." `URA-001-148`: "Entitlements Are Independent of Licenses — restated structurally." `BR-C023-03` (via `IRA-C023`/`TDS-C023 §11`): Entitlement keyed to Organization (optionally Domain); License keyed to Membership; never conflated.
- **The recommended two-table shape (Option A) realizes this structurally:** `c023_license_context` is Membership-anchored (no `organization_id` column, no `entitlement_type_ref`, no `domain_id`); `c023_entitlement_context` is Organization-anchored (no `membership_id`, no `c023_license_type`). Neither table can hold the other's construct. There is no discriminator, no nullable-anchor ambiguity, and no row that is "both".
- Each table's RLS follows its own canonical isolation path (`§3.1` / `§3.2`, matching MTA E-A5) — a License context is org-scoped one hop through its Membership; an Entitlement context is org-scoped directly.
- **Option B (one table)** would place both constructs in one table distinguished only by a `context_kind` discriminator and nullable anchor columns — a structure `IRA-C023 §15a`/`§18`'s Decision-6 investigation and `BR-C023-03` specifically caution against (it recreates the conflation risk). Option B's compliance would rest on *convention* (the service never mixing them) rather than *structure*. This is the principal reason `§17`/`§18` recommend Option A.

---

## 6. Organization and Membership anchoring; tenant-isolation enforcement

- **Entitlement → Organization (direct):** `c023_entitlement_context.organization_id` is the authority key, optionally narrowed by `domain_id` (`TDS-C023 §11`). This is the same anchor `approval_authorities.organization_id` already uses, and the same anchor the MTA `entitlement_registry` uses (E-A1).
- **License → Membership → Organization (one hop):** `c023_license_context.membership_id` is the direct authority key; the *governing Organization* for isolation and for the Commit Authority lookup is `memberships.organization_id`, reached by joining `memberships` (`TDS-C023 §7.4`). No `organization_id` column is stored on `c023_license_context` — mirroring the MTA `license_registry` (which also stores only `membership_id`) and `tenant_registry`'s deliberate omission of redundant anchors.
- **Tenant isolation is enforced at three independent points** (mirroring `TDS-018 §18`'s own three-point model for `membership_approval_authority`):
  1. **Request boundary:** the establish endpoint is reached with an `X-Tenant-ID` header; `middleware/tenant.py` resolves it to `get_current_tenant` (the caller's target `organization_id`), which is a *separate* value from the caller's own claimed `organization_id` in the JWT.
  2. **Authority-verification step (before any write):** `require_approval_authority("Entitlement/License Commit Authority")` → `resolve_approval_authority(...)` compares the caller's claimed `organization_id` against the `X-Tenant-ID`-derived target (`TDS-018 §29.2` step 4) and requires an effective `membership_approval_authority` binding — a mismatch fails closed (403) before any row is inserted. For a License establish, the target Organization must equal `memberships.organization_id` for the supplied `membership_id`; for an Entitlement establish, the target Organization must equal the supplied `organization_id`. This equality is validated at the service layer (`§16`), mirroring `MembershipApprovalAuthorityService.bind()`'s own cross-Organization rejection.
  3. **Row-Level Security (production):** the two `org_isolation` policies in `§3.1`/`§3.2` (direct for Entitlement, one-hop-via-membership for License) — identical in kind to the MTA's own two policies (E-A5) and to `domain_permission_registry`'s existing AuthService policy.
- **`CLAUDE.md §21.4` Mandatory Tenant-Isolation Test Checklist** implications are in `§15`.

---

## 7. Reference-integrity choice — hard FK vs referenced UUID (sub-decision S-1)

| | Hard intra-service FK (recommended) | Referenced UUID, no FK |
|---|---|---|
| **What it means here** | `membership_id → memberships(id)`, `organization_id → organizations(id)`, `domain_id → domains(id)`, `approval_authority_id → approval_authorities(id)` — all targets AuthService-owned. | Plain `UUID` columns; existence validated only at the service layer at establish time. |
| **MTA convention** | The MTA `license_registry`/`entitlement_registry` use `REFERENCES membership_registry` / `organization_master` — i.e. the MTA canonically expresses these as **hard FKs** (E-A1). | — |
| **`ADR-036`** | Consequences: co-location in `AuthService` **permits** simplifying `TDS-C023 §6.3`'s polymorphic reference "to real intra-service foreign keys … a consequence **permitted** by this decision, not mandated by it". | `ADR-036` also does not forbid the polymorphic reference. |
| **`TDS-C023 §6.3` item 2** | — | Explicitly recommended a "referenced UUID, **not a hard cross-service database foreign key**", citing `CLAUDE.md §8` and the `approval_authorities.object_id` polymorphic precedent — **but that reasoning was written when the host was undecided and cross-service was possible.** |
| **`CLAUDE.md §8`** | "never access another service's database." With `ADR-036` fixing the host as `AuthService` and all four FK targets AuthService-owned, an intra-service FK **does not** cross a service boundary — `§8` is satisfied, not violated. | Also satisfies `§8` (no FK at all). |
| **Repository precedent** | **WP-18's own `membership_approval_authority`** uses hard intra-service FKs (`ForeignKey("memberships.id")`, `ForeignKey("approval_authorities.id")`) for exactly this class of AuthService-co-located binding — the closest precedent. `approval_authority.organization_id`/`domain_id` are hard FKs. | `approval_authority.object_id` is a no-FK polymorphic reference — but only because its target is *any* object type, not a single known table. `tenant_registry`'s `*_actor_id` columns are non-FK — but only because `authority_holders` is a "runtime projection that may later supersede" (`TDS-016 §11`), which is not the case for `memberships`/`organizations`/`approval_authorities`. |
| **Integrity** | Referential integrity enforced by the database; a dangling `membership_id` is structurally impossible. | Integrity depends entirely on the service layer; a race or a bug can orphan a row. |
| **Reconciliation** | `TDS-C023 §6.3` item 2's polymorphic recommendation was conditioned on host-uncertainty that `ADR-036` has since removed; `ADR-036` explicitly permits the FK; WP-18 set the precedent. Adopting the hard FK **does not change `TDS-C023`'s accepted design intent** (`ADR-036` Consequences say so in as many words). | Choosing the polymorphic reference despite the host now being fixed would be honouring the letter of a superseded premise. |

**Recommendation for S-1: hard intra-service foreign keys** to `memberships(id)`, `organizations(id)`, `domains(id)`, `approval_authorities(id)` — consistent with the MTA's own `REFERENCES` convention, explicitly permitted by `ADR-036`, precedented by WP-18, and stronger on integrity. **Requires explicit approval** (`§19`).

---

## 8. MTA table-name mismatch — `membership_registry` / `organization_master` vs `memberships` / `organizations`

- **The gap is pre-existing and repository-wide, not introduced here.** The `Master_Technical_Architecture.md` is an idealized single-logical-database schema using names like `membership_registry`, `organization_master`, `approval_authority_registry`. Every AuthService table since WP-00 implements the same concept under a shorter/plural name: `memberships`, `organizations`, `approval_authorities`, `domains`, `domain_permissions`, `roles`, etc. `models/membership.py`'s FK is `ForeignKey("organizations.id")`; `models/approval_authority.py`'s is `ForeignKey("organizations.id")`; `models/membership_approval_authority.py`'s are `ForeignKey("memberships.id")` / `ForeignKey("approval_authorities.id")`.
- **This TDS follows the established AuthService naming convention and does not change canonical architecture.** The recommended models reference `memberships(id)` / `organizations(id)` / `domains(id)` / `approval_authorities(id)` — the actual AuthService table names — exactly as WP-01 through WP-18 all did. The MTA's `license_registry` / `entitlement_registry` logical names map to the implementation names `c023_license_context` / `c023_entitlement_context` (a `c023_`-prefixed, purpose-descriptive name, mirroring how `TDS-016` named its table `tenant_registry` after the MTA concept while `tenant_establishment_service` etc. use AuthService conventions). **The MTA is not edited by this document.** If the Repository Owner prefers the implementation table names to match the MTA logical names exactly (`license_registry` / `entitlement_registry`), that is a naming sub-choice available within Option A — noted, not pre-decided.
- **No canonical document is altered.** Any future reconciliation of MTA logical names to AuthService implementation names is a separate, repository-wide documentation exercise outside this TDS's scope (the same disposition every prior WP took).

---

## 9. Current-state / effective-state semantics — only what C-023 canonical sources already support

### 9.1 Lifecycle status (canonically grounded, not invented)

`PE-001-C023 §5.5` / `TDS-C023 §10.1` establish exactly three stored states: `ACTIVE` (continuing), `SUSPENDED` (reversible), `REVOKED` (terminal). The `status` column's `CHECK (status IN ('ACTIVE','SUSPENDED','REVOKED'))` reflects this canonical set — it is **not** an invented lifecycle. **BA-01's service writes only `ACTIVE`** (`§4` of the charter: `(none) → ACTIVE` establish/continuing outcome only; `TDS-C023 §4`: "suspend/revoke/reactivate … are **not** in this minimum scope"). The suspend/revoke/reactivate *transitions* and their authority requirements are **not designed and not implemented** by TDS-C023-A — they remain a future, separately-scoped BA. Including the full value set in the CHECK (rather than `CHECK (status = 'ACTIVE')`) mirrors `approval_authority.py`'s own `VersionStatus` CHECK and avoids a later `ALTER … DROP CONSTRAINT … ADD CONSTRAINT` when that future BA arrives; **this is a minor sub-choice, flagged for approval** (`§19`) — restricting the CHECK to `'ACTIVE'` now is the strictly-narrowest alternative.

### 9.2 Derived `EXPIRED` (never stored)

`PE-001-C023 §1.17` / `TDS-C023 §10.1`: `EXPIRED` is **never a stored status** — it is a read-time-only derived fact computed against `effective_from`/`effective_to` at the moment of resolution, reusing `C-007`'s certified `compute_membership_authority_consequence()` pattern. **No `EXPIRED` value appears in the CHECK and no column stores it.** This is a `§16` service-layer read behaviour, not a schema element.

### 9.3 Entitlement-type recognition (Decision 3 boundary)

`entitlement_type_ref` holds an identifier of an **already-recognized** Entitlement Type. **BA-01 does not create, modify, or govern a global Entitlement Type or a catalog** (Decision 3 deferred, `TDS-C023 §5-C` / `§19` / `§21.6`). The "is this type recognized?" check is a `§16` service-layer validation against whatever recognized-type source exists; `TDS-C023 §19` / `§21.6` already disclose that if **no** Entitlement Type is recognized anywhere, the Entitlement half of BA-01 is *vacuously blocked* (the License half is fully exercisable) — and `IMP-REPORT-WP-17 §5` mandates a `§18`/`§19.4` STOP-and-report if demonstrating the Entitlement path end-to-end turns out to require the deferred catalog-governance mechanism. **This TDS does not resolve that; it only records that the schema stores a *reference*, never a *definition*.**

### 9.4 No Subscription/temporal semantics

`effective_from`/`effective_to` are independent Commit-time business dates (`TDS-C023 §10.1`). **No column aligns them to a Subscription, a renewal, or a termination** — every such question is Pending Canonical Binding (`TDS-C023 §10.2`) and `WP-17 §23` forbids inventing Subscription-aligned expiry. `URA-001-117` ("entitlements are time-bound and automatically deactivate on expiry") is satisfied by the derived-`EXPIRED` read (`§9.2`), not by a stored deactivation.

---

## 10. Uniqueness invariants — INV-C023-09 / INV-C023-10 (sub-decision S-3)

- **INV-C023-10** (`TDS-C023 §15`, `PE-001-C023 §1.16`): "exactly one **current** Authoritative License Context per Membership Anchor." "Current" ≡ `effective_to IS NULL` under the soft-close convention (`§3.1`). Enforcement: **partial unique index `ux_c023_license_context_current` on `(membership_id) WHERE effective_to IS NULL`.** Directly mirrors WP-18's `ux_membership_approval_authority_active` (`… WHERE effective_to IS NULL`) and TDS-017's `ux_authority_holders_active_authority` (`… WHERE status = 'ACTIVE'`).
- **INV-C023-09** (`TDS-C023 §15`): "exactly one current Authoritative Entitlement Context per Entitlement Anchor **and entitlement type**." Enforcement: **partial unique index `ux_c023_entitlement_context_current` on `(organization_id, <domain_id-normalized>, entitlement_type_ref) WHERE effective_to IS NULL`.**
- **The `domain_id`-NULL problem (S-3):** a plain multi-column unique index in PostgreSQL treats NULL `domain_id` as distinct from every other NULL — so two concurrent organization-wide (`domain_id IS NULL`) entitlements of the same type could both be inserted, violating the invariant. Three techniques, one must be chosen:
  1. **`COALESCE(domain_id, '<sentinel-uuid>')` index expression** — recommended; works on all supported PostgreSQL versions and (with an equivalent expression) on the SQLite test harness; the sentinel is a fixed all-zeros UUID that no real Domain can hold.
  2. **`NULLS NOT DISTINCT`** on the index — cleaner, but PostgreSQL 15+ only; needs a deployment-version confirmation and has no SQLite equivalent (`conftest.py` would need a fallback).
  3. **Service-layer guard only** — a pre-check under a transaction, no DB constraint for the NULL case — weakest; relies on the pre-check-then-create race window being covered, which the partial index is specifically meant to close.
- **Race handling** (`TDS-C023 §15`): the certified pattern — pre-check for a current context, then create, then catch `IntegrityError` from the partial unique index and translate to `409` — exactly as `MembershipService.establish()` and every prior WP-0X BA do.
- **Recommendation for S-3:** the `COALESCE` sentinel expression (technique 1), plus the pre-check-then-catch-`IntegrityError` service pattern. **Requires explicit approval** — the technique choice and the sentinel value are schema-visible.

---

## 11. Approval Authority — referencing the certified WP-18 mechanism without redesigning it

- **The `approval_authorities` policy row** ("Entitlement/License Commit Authority", `scope_type='COMPANY'`, `approval_strategy='ANY_ONE'`, one per participating Organization — `TDS-C023 §7.1`–`§7.6`) is created via the **already-certified** `ApprovalAuthorityService.establish()` (WP-02 BA-03). `authority_name` is already a free-text `VARCHAR(255)` column — **no schema change to `approval_authorities`** (`TDS-C023 §7.2`). This is data provisioning, not schema.
- **The binding** (`membership_approval_authority` rows linking the accountable Membership(s) to that authority) is created via the **already-certified** `MembershipApprovalAuthorityService.bind()` (WP-18). **No schema change to `membership_approval_authority`.**
- **Runtime enforcement** on the establish endpoint is `require_approval_authority("Entitlement/License Commit Authority")` → `enforce_approval_authority()` → `resolve_approval_authority()` — the certified WP-18 functions, consumed **as-is**. `resolve_approval_authority()`'s 8-step fail-closed algorithm (`ANY_ONE` authorizes; `MAJORITY`/`ALL`/`SEQUENTIAL` → `UNSUPPORTED_STRATEGY`; no admin bypass; Organization-match at step 4) is **not modified, extended, or reinterpreted**.
- **This schema's only touch-point** is the `approval_authority_id` column on each new table — a reference (FK per S-1, or plain UUID) to the `approval_authorities` row that authorized the Commit, recorded for audit and traceability (`TDS-C023 §5-A` "Authority reference", `§16`). It stores a pointer; it does not participate in resolution.
- **`TDS-018`, `WP-18`, and their certification artifacts are untouched.** WP-18 remains CLOSED — CERTIFIED — RELEASE-READY.

---

## 12. Audit — reusing existing observability infrastructure

- **Mechanism:** `observability.py`'s `record_audit(action, resource, status: AuditStatus, actor_id, tenant_id, metadata)` and `publish_event(...)` — the same functions `TenantEstablishmentService.establish()`, `MembershipService.establish()`, and `resolve_approval_authority()` already use. **No new audit subsystem** (`TDS-C023 §16`).
- **`AuditStatus`** vocabulary reused as-is: `SUCCESS` (established), `DENIED` (authority not satisfied / duplicate current context), `FAILED` (unexpected persistence error).
- **Recorded per `TDS-C023 §16`** on every establish attempt: initiating `person_id` (`actor_id`); the specific `approval_authorities` row id that authorized (in `metadata`); the affected `organization_id` and/or `membership_id`; the License/Entitlement anchor and `entitlement_type_ref` / `c023_license_type`; `effective_from`/`effective_to`; the resulting `status`; the new record's `id` as the correlation identifier; and, on failure, the specific rejection reason (`resolve_approval_authority()`'s returned `ApprovalAuthorityResolution` label, or `409`/`404` cause).
- **No secret material** (raw JWT, `Authorization` header, `JWT_SECRET_KEY`, password) is placed in `metadata` — the same discipline `VV-AUDIT-WP-18` verified for the resolver.
- **This is a `§16` service-layer behaviour** — TDS-C023-A adds no audit *column* to either table (the `committed_by_actor_id` / `committed_at` columns are the persisted audit *citation*, per the `tenant_registry` precedent; the append-only audit *log* is emitted by `record_audit`).

---

## 13. Migration strategy (described — NOT created)

- **Shape:** one **purely additive** Alembic migration creating `c023_license_context` and `c023_entitlement_context` (Option A) — two `op.create_table(...)` calls plus their indexes and partial unique indexes. **No `ALTER`** to any existing table. A clean `downgrade()` drops the two tables and their indexes, nothing else.
- **Chain:** `down_revision` = `f9a3c7e1b5d2` (the current single non-branching Alembic head, WP-18's `membership_approval_authority` migration). The new migration becomes the single head. No branch.
- **Cross-dialect:** the two partial unique indexes use `postgresql_where=text(...)` + `sqlite_where=text(...)`, exactly as `ux_membership_approval_authority_active` and `ux_authority_holders_active_authority` already do, so the SQLite test harness (`conftest.py`) creates them too. The `COALESCE`-expression index (S-3, technique 1) is expressed identically on both dialects.
- **RLS policies** (`§3.1`/`§3.2`) are PostgreSQL-only; per the existing AuthService pattern they are added in the migration's PostgreSQL branch and are inert under SQLite (where isolation is asserted at the service layer in tests — `TD-096`/`TD-159`, the known repository-wide harness limitation, applies here identically to every other AuthService table and introduces no new debt).
- **The migration is NOT written by this document.** It is written only after the Repository Owner approves the schema (`§19`), and — per `IMP-REPORT-WP-17 §4(1)` — a further `CLAUDE.md §18`/`§19.4` confirmation is performed at the point of actually creating it, mirroring how `TDS-016` preceded `tenant_registry`'s migration.

---

## 14. Compatibility — existing canonical tables / consumers that must remain untouched

| Artifact | Why untouched |
|---|---|
| `memberships` (table + model + `MembershipService` + `BA-03` path) | Decision 6 (`§4`). No `ALTER`, no FK to `license_type`, no write. |
| `organizations` | Only referenced (FK per S-1, or read). No `ALTER`. |
| `domains` | Only referenced (nullable FK). No `ALTER`. |
| `approval_authorities` (+ `ApprovalAuthorityService`, WP-02) | Only referenced and read via `resolve_approval_authority()`. `authority_name` already free-text — no schema change. Data provisioning of the C-023 instance uses the certified `establish()`. |
| `membership_approval_authority` (+ service + resolver, WP-18) | Consumed as-is. No schema change, no new column, no algorithm change. `TDS-018` / `CERT-WP-18` / `VV-AUDIT-WP-18` / `RRA-WP-18` unaffected. |
| `authority_holders` (C-040/TDS-017) | Not referenced at all by C-023. |
| `tenant_registry` (C-040/WP-16) | Not referenced (`TDS-C023 §13`: WP-16's minimal `(none)→PROVISIONED` scope suffices; no further Tenant work). |
| The Alembic head `f9a3c7e1b5d2` | Extended by chaining a new migration onto it; not rewritten or branched. |
| `Master_Technical_Architecture.md` | Not edited (`§8`). The MTA logical names are mapped to implementation names per the established AuthService convention. |
| `TDS-C023`, `IRA-C023`, `WP-17` charter, `WPR-001`, `IMP-REPORT-WP-17` | Read-only inputs. Not modified by this TDS. (If the Repository Owner approves a schema, a subsequent governance pass may add a one-line pointer from `TDS-C023 §24` item 1's schema-shape note to the approved decision — that is a separate, later change, not part of TDS-C023-A.) |
| C-023 Decisions 1–6 (`IRA-C023 §18.13`/`§19.13`/`§20.12`/`§21.12`/`§22.13`/`§23.13`) | Not reopened, altered, or reinterpreted. |

---

## 15. Security — `CLAUDE.md §21.4` tenant-isolation implications and fail-closed requirements

- **Fail-closed:** the establish service verifies the resolved Commit Authority **before any write** (`TDS-C023 §14` step 2); `resolve_approval_authority()` returns a non-`AUTHORIZED` label → `enforce_approval_authority()` raises `403` → no row is inserted. No default-allow path. No `PLATFORM_ADMIN`/`AUREX_ADMIN` bypass (inherited from WP-18; `TDS-C023 §22`).
- **`CLAUDE.md §21.4` Mandatory Tenant-Isolation Test Checklist** (implications for the eventual test suite, `§16`):
  - **(a)** seed two distinct, unrelated Organizations with no shared row — one `c023_license_context` / `c023_entitlement_context` per Organization, disjoint Memberships.
  - **(b)** a caller in Organization A cannot establish or read Organization B's Authoritative Context — verified at establish time (`403`/`404` on cross-Organization `membership_id` or `organization_id`) and at read time (RLS in production; service-layer Organization filter under the SQLite harness).
  - **(c)** an explicit probe of a **foreign-object identifier not derived from the caller's own claims** — supply another tenant's `membership_id` / `organization_id` / `approval_authority_id` and confirm it is rejected (not silently accepted). The `X-Tenant-ID`-derived target (`§6`) is the only attacker-influenceable value and is gated at resolver step 4.
  - **`c023_entitlement_context.entitlement_type_ref`** — a free-text identifier — must be validated as an already-recognized type (`§9.3`) and must not be usable to probe another tenant's data (it is not an object identifier, but the test suite should confirm a nonexistent type yields a clean rejection, not an inference).
- **RLS** (`§3.1`/`§3.2`) provides the production defense-in-depth layer; the service-layer Organization checks provide the primary enforcement and the only enforcement under the SQLite test harness — this is the identical posture WP-16 and WP-18 both certified under, and it introduces no new debt.

---

## 16. Implementation sequencing — what depends on the schema decision

**Blocked until the Repository Owner approves a schema (`§19`):**
1. `models/c023_license_context.py` (+ `c023_entitlement_context.py`, Option A) — or the single `models/entitlement_license_context.py` (Option B) — and their registration in `models/__init__.py`.
2. The additive Alembic migration (`§13`) and therefore any change to the Alembic head.
3. `repositories/…` for the new entity/entities (pre-check + create + effective-window queries).
4. `services/entitlement_license_establishment_service.py` — the `establish()` transaction (`TDS-C023 §14`): validate anchors → `enforce_approval_authority(...)` → establish inside one DB transaction → `record_audit` → `IntegrityError` → `rollback` → `409`.
5. `routers/…` + `schemas/…` (Pydantic request/response — field set derived from the model) for the establish endpoint and the two frontend items; `require_approval_authority("Entitlement/License Commit Authority")` wired onto the establish route; router registration in `main.py`; the `middleware/tenant.py` exemption entry if the establish endpoint names the target Organization in the body (mirroring `/tenants`).
6. All BA-01 tests — the `CLAUDE.md §21.4` checklist (`§15`), the `TDS-C023 §21` V&V obligations (a negative control proving the authority contract denies by default; a concurrent-establish race test), effective-window boundary cases, audit-content assertions, admin-bypass-absence tests.
7. The two authorized frontend items (`TDS-C023 §17`) — also subject to the separate `IMP-REPORT-WP-17 §4(2)` `CLAUDE.md §19.1`/`§20.5` STOP-and-report if `DS-001` / Workspace / Navigation coverage proves insufficient.
8. The full `CLAUDE.md §19.7b` five-gate closure.

**Genuinely schema-independent (may proceed only alongside step 4's flow, not ahead of it):**
- Provisioning the C-023 `approval_authorities` "Entitlement/License Commit Authority" instance per participating Organization (certified `ApprovalAuthorityService.establish()`) and its `membership_approval_authority` binding row(s) (certified `MembershipApprovalAuthorityService.bind()`). Data, not schema — but not independently exercisable/testable before the establish flow exists, so sequenced with step 4.

**Conclusion:** essentially the entire BA-01 implementation is downstream of the schema decision. Nothing of substance proceeds until `§19` is answered.

---

## 17. Alternatives — rigorous comparison

| Criterion | **A — two tables** (`c023_license_context` + `c023_entitlement_context`) | **B — one table** (`entitlement_license_context`, discriminator + nullable anchors) | **C — other viable canonical option** |
|---|---|---|---|
| **Canonical alignment** | **Strongest.** Mirrors the MTA's two separate `CREATE TABLE`s (E-A1), the "explicitly separate" PURPOSE text (E-A2), the catalog (E-A3), `URA-001-112`/`-148` (E-A4), and the two distinct RLS patterns (E-A5). | **Weaker.** Matches the `TDS-C023 §6.3` "working name / or equivalent" sketch (E-B1/E-B2) but supersedes two canonical MTA definitions with one; the TDS text itself is non-final on this point. | **None found.** A `memberships`/`organizations` column extension is barred by Decision 6 and `URA-001-112`/`-148`; an events-only (`URA-001-119`) or read-model-only representation cannot hold "the current single authoritative fact per anchor" (`TDS-C023 §5-A`). |
| **Complexity** | Two models, two repositories (or one repo, two entities), two partial unique indexes, one migration with two `create_table`s. A "both" establish request writes two rows in one transaction. | One model, one repository, one migration. But: a `context_kind` discriminator, a `CHECK` enforcing "exactly one of `membership_id` / `organization_id` set", branching RLS, branching uniqueness (two partial indexes anyway, or one complex expression). Net complexity is comparable, concentrated in constraints rather than table count. | — |
| **Integrity** | **Strongest.** Each table structurally cannot hold the other construct; each FK target is single and known; each uniqueness index is simple. | **Weaker.** Nullable anchor columns; correctness of "exactly one anchor" rests on a `CHECK`; a bug that sets both (or neither) is a data-integrity failure the structure does not prevent. | — |
| **Tenant isolation** | Clean: direct `org_isolation` for Entitlement, one-hop for License — each matching its MTA policy exactly (E-A5). | RLS must branch on `context_kind` (direct vs one-hop) — one policy with a `CASE`/`OR`, harder to audit and to match against the MTA's two separate policies. | — |
| **Future extensibility** | A future "Maintain Terms" BA, or Consumption/Allocation (Decision 4), or Catalog (Decision 3) extends whichever table it concerns without touching the other; License↔Entitlement independence stays structural. | Every future extension must consider both constructs in one table and re-check the discriminator/anchor invariants; the conflation risk `BR-C023-03` warns of grows with each column. | — |
| **Compatibility** | Purely additive; two new tables; no `ALTER` anywhere; head chains cleanly. | Purely additive; one new table; no `ALTER`. Slightly simpler migration, but a later decision to split back to two tables would require data movement. | — |
| **Decision 6 compliance** | By construction (`§4`) — no `FULL`/`LIGHT` column on either table. | Also compliant (no `FULL`/`LIGHT` column) — but relies more on convention, since License and Entitlement share a table. | — |
| **`URA-001-112`/`-148` / `BR-C023-03`** | Realized **structurally** (`§5`). | Realized by **convention** (the service never mixing kinds) — precisely the weaker posture `IRA-C023 §15a`/`§18` cautioned against. | — |

---

## 18. Recommendation (current — NOT an approved decision)

Consistent with `STOP-AND-REPORT-WP-17-01 §D`:

- **Adopt Option A — the two-table shape** (`c023_license_context` + `c023_entitlement_context`, `§3`), as the narrowest option supported by canonical evidence: the MTA canonically defines two separate tables and states they are "explicitly separate"; `URA-001-112`/`-148` and `BR-C023-03` keep License and Entitlement independent; Option A realizes that independence *structurally* rather than by convention; it adds only the columns `TDS-C023 §5-A`/`§14`/`§16` demonstrably require and omits the one canonical column that would violate Decision 6.
- **S-1 (reference integrity): hard intra-service foreign keys** to `memberships(id)` / `organizations(id)` / `domains(id)` / `approval_authorities(id)` — consistent with the MTA's own `REFERENCES` convention, explicitly permitted by `ADR-036`, precedented by WP-18, stronger on integrity (`§7`).
- **S-2 (`c023_license_type`): include the nullable specialized-type column now**, `CHECK` restricted to the four `URA-001-115` values, since `URA-001-115` is canonical and `TDS-C023 §6.2` names it C-023-owned — with the strictly-narrower alternative (defer the column to a later BA) available if the Repository Owner prefers minimal surface (`§3.1`, `§4.3`).
- **S-3 (uniqueness NULL-handling): the `COALESCE(domain_id, '<all-zeros UUID>')` partial-unique-index expression** plus the certified pre-check-then-catch-`IntegrityError` service pattern (`§10`).
- **Table naming:** `c023_`-prefixed implementation names (`§8`), with the option to instead use the MTA logical names (`license_registry` / `entitlement_registry`) if the Repository Owner prefers exact name parity — a sub-choice within Option A.

**This recommendation is offered per `CLAUDE.md §19.4`. It is NOT a Repository Owner decision and NOT an architectural approval.** No model, no migration, no code follows from this document alone.

---

## 19. REPOSITORY OWNER / ARCHITECTURAL DECISION

~~**Implementation of the WP-17 / BA-01 persistence layer and everything downstream of it (`§16`) remains HALTED until the Repository Owner explicitly answers the following. This document does not answer them and does not self-authorize any of them (`§20`).**~~ *(Superseded 2026-09-01 — the Repository Owner has answered every question below; see `§19.1` for the decision recorded verbatim and `§19.2` for the confirmed schema. The `§19.3` conditions on `§20` and the `CLAUDE.md §18`/`§19.4` STOP-and-report discipline remain in force.)*

### 19.0 The decision questions (as originally posed — preserved as the record of what was asked)

**D-1 — Table shape.** Approve **Option A** (two tables: `c023_license_context` + `c023_entitlement_context`), **Option B** (one table: `entitlement_license_context`), or direct a different shape. *(Recommendation: Option A — `§17`, `§18`.)*

**D-2 — Reference integrity (S-1).** For the anchor and authority references, approve **hard intra-service foreign keys** to `memberships(id)` / `organizations(id)` / `domains(id)` / `approval_authorities(id)`, or **referenced UUIDs with no FK** (the `TDS-C023 §6.3` item 2 style). *(Recommendation: hard intra-service FKs — `§7`.)*

**D-3 — Specialized license type column (S-2).** Approve including a **nullable `c023_license_type`** column now (CHECK: `SUPPLIER`/`AUDITOR`/`BOARD_MEMBER`/`CONSULTANT`, per `URA-001-115`), or **defer** it to a later BA. *(Recommendation: include now, nullable — `§3.1`, `§4.3`.)*

**D-4 — Uniqueness NULL-handling (S-3).** Approve the **`COALESCE`-sentinel partial-unique-index expression** for the Entitlement-side `domain_id`-NULL case, or direct **`NULLS NOT DISTINCT`** (requires PostgreSQL 15+ confirmation and a SQLite fallback), or **service-layer-only** enforcement for that case. *(Recommendation: `COALESCE` sentinel — `§10`.)*

**D-5 — `status` CHECK breadth.** Approve `CHECK (status IN ('ACTIVE','SUSPENDED','REVOKED'))` (the full canonical set, only `ACTIVE` ever written by BA-01), or restrict to `CHECK (status = 'ACTIVE')` now. *(Recommendation: full canonical set — `§9.1`.)*

**D-6 — Implementation table names.** Approve `c023_`-prefixed implementation names (`c023_license_context` / `c023_entitlement_context`), or direct exact MTA-logical-name parity (`license_registry` / `entitlement_registry`). *(Recommendation: `c023_`-prefixed, per established AuthService convention — `§8`; either is available within Option A.)*

**D-7 — Migration authorization.** Confirm that, once D-1…D-6 are decided, the implementing session is authorized to (a) write the additive Alembic migration described in `§13` after performing the further `CLAUDE.md §18`/`§19.4` confirmation `IMP-REPORT-WP-17 §4(1)` mandates at the point of creation, and (b) proceed with the `§16` implementation sequence — **without** a further Repository Owner decision, unless implementation encounters a *new* undocumented architectural question (in which case it STOPs and reports again). *(This is the "resume" authorization; it is not implied by approving D-1…D-6.)*

**Explicitly NOT in this decision:** Consumption/Allocation (Decision 4), Entitlement Catalog / type-definition governance (Decision 3), Subscription/temporal alignment (`TDS-C023 §10.2`), Billing, suspend/revoke/reactivate transitions, C-020/C-025 hand-off, a new service boundary, any change to `TDS-018`/WP-18, any change to `memberships`, and any change to C-023 Decisions 1–6.

### 19.1 Repository Owner / Architectural Decision — RECORDED, 2026-09-01 (verbatim)

The Repository Owner explicitly approved `§19.0` D-1 through D-6 and granted the D-7 resume authorization, subject to the stated governance boundaries. The decision text below is reproduced exactly as issued, with no wording, date, or scope added or altered:

> **I approve the recommendations in TDS-C023-A §19, D-1 through D-6, and I grant the D-7 resume authorization, subject to the stated governance boundaries.**
>
> **Repository Owner / Architectural Decision:**
>
> **D-1 — TABLE SHAPE**
> APPROVED: Option A — two tables:
> - c023_license_context
> - c023_entitlement_context
>
> Rationale: preserve the canonical License/Entitlement separation and align structurally with URA-001-112, URA-001-148 and BR-C023-03.
>
> **D-2 — REFERENCE INTEGRITY**
> APPROVED: Hard intra-Service foreign keys where applicable:
> - memberships
> - organizations
> - domains
> - approval_authorities
>
> Use the actual AuthService table names and existing repository conventions. Do not create cross-service FKs.
>
> **D-3 — c023_license_type**
> APPROVED: Include nullable c023_license_type now.
>
> It must contain only the four specialized C-023 license types defined by URA-001-115. It must NOT duplicate membership.license_type and must NOT alter memberships.license_type.
>
> Decision 6 remains completely unchanged.
>
> **D-4 — ENTITLEMENT UNIQUENESS NULL HANDLING**
> APPROVED: COALESCE-sentinel approach for the database-level uniqueness constraint, provided the implementation-time migration/design documents the exact expression and demonstrates cross-dialect correctness.
>
> **D-5 — STATUS**
> APPROVED: Full canonical status set:
> ACTIVE, SUSPENDED, REVOKED.
>
> For BA-01, only ACTIVE may be written.
>
> Do not introduce suspend/revoke/reactivate lifecycle behavior as part of WP-17/BA-01.
>
> **D-6 — TABLE NAMES**
> APPROVED: c023_-prefixed names:
> - c023_license_context
> - c023_entitlement_context
>
> **D-7 — RESUME AUTHORIZATION**
> APPROVED.
>
> Once D-1 through D-6 have been recorded, independently reviewed, and the resulting implementation-time design is reconciled, the implementation session may proceed with:
> - the additive Alembic migration,
> - models,
> - repositories,
> - service transaction,
> - router/Pydantic schemas,
> - approval-authority wiring,
> - audit wiring,
> - required tests,
> - the two authorized frontend items,
>
> without requiring another Repository Owner decision for these already-decided items.
>
> HOWEVER, the existing CLAUDE.md §18 / §19.4 STOP-and-report discipline remains in force.
>
> If implementation encounters ANY new architectural question, canonical contradiction, schema requirement not covered by D-1 through D-6, new service boundary, scope expansion, or change to any C-023 Decision 1–6, STOP immediately and report it. Do not infer or self-authorize a solution.
>
> **IMPLEMENTATION BOUNDARIES**
>
> Authorized:
> - WP-17 / BA-01 only: Establish Entitlement/License Context (Administrative).
> - AuthService hosting per accepted ADR-036.
> - The two-table schema approved above.
> - Certified WP-18 Approval Authority infrastructure.
> - Decision 6 read-only membership.license_type usage.
> - Existing observability/audit infrastructure.
> - Required tenant-isolation controls and tests.
> - The two explicitly authorized frontend items.
>
> Explicitly excluded:
> - broader C-023 implementation;
> - Consumption / Allocation;
> - Entitlement Catalog administration;
> - Subscription semantics;
> - Billing;
> - C-020 / C-025 integration;
> - migration/offboarding;
> - cross-tenant sharing;
> - Decision 3 or Decision 4 implementation;
> - Authorization Engine Option A / M2-M6 redesign;
> - AuthorityHolder replacement;
> - Group infrastructure;
> - new service boundary;
> - modifications to memberships;
> - changes to C-023 Decisions 1–6;
> - any schema not covered by the approved TDS-C023-A decision.
>
> **IMPORTANT SEQUENCING**
>
> Before creating or running the migration:
>
> 1. Update TDS-C023-A §19 to record these Repository Owner decisions verbatim.
> 2. Independently review the recorded decisions for fidelity and consistency with TDS-C023-A.
> 3. Update the appropriate implementation report / Change Control records.
> 4. Reconfirm that the approved schema exactly matches the decision.
> 5. Only then proceed to implementation.
>
> Do NOT implement in the same governance-recording step.
>
> After the decision is recorded and independently verified, resume implementation.
>
> At implementation completion:
> - produce IMP-REPORT evidence;
> - run the complete test suite;
> - run the required tenant-isolation tests;
> - verify migration head;
> - perform scope/change-control verification;
> - dispatch the independent implementation reviewer;
> - then proceed through the CLAUDE.md §19.7b certification gates.
>
> Do not claim certification merely because implementation succeeds.
>
> Current statuses remain:
> WP-17 / BA-01 = IMPLEMENTATION AUTHORIZED — IMPLEMENTATION HALTED pending schema decision
> C-023 = 🔴 RED — NOT IMPLEMENTATION READY
> WP-18 = CLOSED — CERTIFIED — RELEASE-READY
>
> STOP after recording and independently reviewing the decision. Do not implement until that verification is complete.

### 19.2 Confirmed schema (the decision applied to `§3`)

Each Repository Owner approval in `§19.1` maps to the corresponding element of `§3` as follows. **No element of `§3` is changed by this section** — `§3` was authored as the recommended shape and every recommendation was approved as recommended:

| Decision | Approved | Applies to |
|---|---|---|
| **D-1** | Option A — **two tables**: `c023_license_context` (Membership-anchored), `c023_entitlement_context` (Organization-anchored, optionally Domain-scoped) | `§3.1`, `§3.2` — unchanged |
| **D-2** | **Hard intra-service foreign keys**, using the actual AuthService table names: `c023_license_context.membership_id → memberships(id)`, `c023_license_context.approval_authority_id → approval_authorities(id)`, `c023_entitlement_context.organization_id → organizations(id)`, `c023_entitlement_context.domain_id → domains(id)` (nullable), `c023_entitlement_context.approval_authority_id → approval_authorities(id)`. **No cross-service FK.** `committed_by_actor_id` remains a **non-FK** point-in-time audit citation (the `tenant_registry` precedent, `§3.1`). | `§3.1`, `§3.2`, `§7` (S-1) — the "hard intra-service FK" pole selected |
| **D-3** | **Include `c023_license_type` nullable now** on `c023_license_context`, `CHECK (c023_license_type IS NULL OR c023_license_type IN ('SUPPLIER','AUDITOR','BOARD_MEMBER','CONSULTANT'))` — the four `URA-001-115` specialized types only. It **does not** store `FULL`/`LIGHT` and **does not** alter `memberships.license_type`. **Decision 6 unchanged** (`§4`). | `§3.1`, `§4` (S-2) — the "include now, nullable" pole selected |
| **D-4** | **`COALESCE`-sentinel** partial-unique-index expression for the Entitlement-side `domain_id`-NULL case: `ux_c023_entitlement_context_current` on `(organization_id, COALESCE(domain_id, '00000000-0000-0000-0000-000000000000'::uuid), entitlement_type_ref) WHERE effective_to IS NULL`. **The implementation-time migration/design SHALL document the exact expression and demonstrate cross-dialect (PostgreSQL + the SQLite test harness) correctness** — a Repository Owner condition on this approval. | `§3.2`, `§10` (S-3) — the `COALESCE`-sentinel pole selected, with the stated documentation/cross-dialect condition |
| **D-5** | **Full canonical `status` set**: `CHECK (status IN ('ACTIVE','SUSPENDED','REVOKED'))` on both tables. **BA-01 writes only `ACTIVE`.** **No suspend/revoke/reactivate lifecycle behaviour is implemented as part of WP-17/BA-01** — a Repository Owner instruction reaffirming `§9.1`. | `§3.1`, `§3.2`, `§9.1` — the "full canonical set" pole selected |
| **D-6** | **`c023_`-prefixed implementation table names**: `c023_license_context`, `c023_entitlement_context`. | `§3`, `§8` — the `c023_`-prefixed pole selected |
| **D-7** | **Resume authorization GRANTED**, subject to: (a) this recording (`§19.1`), its independent review, and the reconciliation of this TDS being complete first; (b) the `CLAUDE.md §18`/`§19.4` STOP-and-report discipline remaining in force — any *new* architectural question, canonical contradiction, uncovered schema requirement, new service boundary, scope expansion, or change to any C-023 Decision 1–6 triggers an immediate STOP-and-report; (c) the `IMPLEMENTATION BOUNDARIES` list in `§19.1` (Authorized / Explicitly excluded); (d) at implementation completion, the full evidence/test/tenant-isolation/migration-head/scope-verification/independent-review sequence and then the `CLAUDE.md §19.7b` five gates — certification is **not** implied by implementation succeeding. | `§13`, `§16` — implementation of the `§16` sequence is authorized to proceed for the D-1…D-6 items **after** the sequencing steps 1–5 in `§19.1` are complete |

**Nothing in `§3` was edited to fit this decision — the decision confirmed `§3` as written.**

### 19.3 Effect of this decision

- `§20` ("No self-authorization") is **partly superseded**: the Repository Owner — not this document — has now approved the schema shape, columns, constraints, indexes, and reference strategy for the D-1…D-6 items, and has granted the D-7 resume authorization. What remains true from `§20`: this **recording** pass creates no model, no migration, no code; it does not change the Alembic head; and the `CLAUDE.md §18`/`§19.4` STOP-and-report discipline is explicitly kept in force by `§19.1` for anything *not* covered by D-1…D-6.
- Per the `§19.1` `IMPORTANT SEQUENCING`, implementation does **not** begin in this recording pass. It resumes only after: (1) this recording is complete (done, `§19.1`/`§19.2`); (2) an independent review confirms the recording's fidelity and consistency with this TDS; (3) the implementation report / Change Control records are updated (`IMP-REPORT-WP-17 §9`); (4) the approved schema is reconfirmed against the decision (`§19.2`); then (5) implementation proceeds.
- **Statuses at the close of this recording pass** (per the Repository Owner's own statement, `§19.1`): ~~WP-17 / BA-01 = **IMPLEMENTATION AUTHORIZED — IMPLEMENTATION HALTED pending completion of the sequencing steps** (schema decision now made; implementation not yet resumed)~~ — *this is a HISTORICAL statement of the recording pass's own end-of-pass status; it is **NOT** the current implementation status. Struck to strikethrough-preserve format 2026-09-01 per the final pre-Gate-1 governance cleanup (direct Repository Owner authorization). The sequencing steps this statement describes have since completed. **Current factual status: WP-17 / BA-01 = IMPLEMENTATION AUTHORIZED — IMPLEMENTATION COMPLETE — NOT YET CERTIFIED** (`IMP-REPORT-WP-17 §11`/`§14`/`§16`); implementation was independently reviewed SOUND, and certification remains pending a fresh `CLAUDE.md §19.7b` Gate 1 (attempted twice, currently NOT CERTIFIED for stale-status documentation only — no code/design defect).* C-023 = **🔴 RED — NOT IMPLEMENTATION READY** (unchanged, still current); WP-18 = **CLOSED — CERTIFIED — RELEASE-READY** (unchanged, still current). *(Prior annotation retained: annotated 2026-09-01 per the R9 governance-reconciliation pass, `CERT-WP-17` non-material observation O3; no schema/code content, and no `§19.0`/`§19.1` verbatim Repository Owner quotation or D-1…D-7 decision text, was altered by that pass or this cleanup.)*

---

## 20. No self-authorization

~~Creating this Technical Design **does not**:~~ *(partly superseded 2026-09-01 by the Repository Owner decision at `§19.1` — see `§19.3`. The schema shape, columns, constraints, indexes, and reference strategy for D-1…D-6, and the D-7 resume authorization, were approved **by the Repository Owner**, not by this document. The statements below remain true of the **document itself** and of every pass that has touched it, including the `§19.1` recording pass.)*

- ~~authorize WP-17 / BA-01 implementation to resume~~ — *the Repository Owner granted the D-7 resume authorization at `§19.1`, subject to its stated conditions; this document did not self-authorize it;*
- ~~approve any schema shape, column, constraint, index, or reference strategy~~ — *the Repository Owner approved D-1…D-6 at `§19.1`; this document recommended, it did not approve;*
- create or run an Alembic migration, or change the Alembic head — **still true**: no migration was created or run by this document or by the `§19.1` recording pass; the Alembic head is unchanged at `f9a3c7e1b5d2`;
- create any production model, repository, service, router, Pydantic schema, or test — **still true**: none created by this document or the recording pass;
- modify `TDS-C023`, `IRA-C023`, the `WP-17` charter, `WPR-001`, `TDS-018`, `WP-18`, `Master_Technical_Architecture.md`, or any C-023 Decision 1–6 — **still true**: none modified by this document or the recording pass;
- change C-023's capability-wide 🔴 RED status or WP-17's status — C-023 remains 🔴 RED (**still true**, unchanged); ~~WP-17 remains IMPLEMENTATION AUTHORIZED — IMPLEMENTATION HALTED — NOT CERTIFIED (the halt now being the `§19.1` sequencing steps, not a missing schema decision).~~ *(Accurate at the close of the recording pass; superseded 2026-09-01 by the R9-completion governance-reconciliation pass, per direct Repository Owner authorization ("Repository Owner Authorization — Complete WP-17 R9 Governance Reconciliation"), resolving a residual Gate 1 M-1 finding: the `§19.1` sequencing steps completed, implementation resumed after the approved D-1…D-7 schema decision and is now **COMPLETE** for the License path end-to-end (Entitlement path vacuously blocked by design per Repository Owner Option A, `IMP-REPORT-WP-17 §12.1`), independently reviewed **SOUND**. **WP-17 / BA-01 = IMPLEMENTATION COMPLETE — NOT YET CERTIFIED** — certification remains pending a fresh `CLAUDE.md §19.7b` Gate 1 (attempted twice, currently NOT CERTIFIED for stale-status documentation only; `IMP-REPORT-WP-17 §14`/`§16`, `CERT-WP-17`). This note alters no D-1…D-7 or C-023 Decision 1–6 semantics.)*

This document was a design proposal produced under `CLAUDE.md §19.4`'s STOP-and-report discipline. The Repository Owner has since answered `§19` in full (`§19.1`). Per the `§19.1` `IMPORTANT SEQUENCING`, implementation does not begin in the recording pass — it resumes only after this recording is independently reviewed for fidelity, the implementation report is updated, and the approved schema is reconfirmed (`§19.3`). ~~Until then, WP-17 / BA-01 remains **IMPLEMENTATION AUTHORIZED — IMPLEMENTATION HALTED — NOT CERTIFIED**; C-023 remains **🔴 RED — Not Implementation Ready**; WP-18 remains **CLOSED — CERTIFIED — RELEASE-READY**.~~ *(Accurate at the close of the recording pass — preserved unchanged, not a live status. The sequencing steps have since completed and implementation is COMPLETE, independently reviewed SOUND, with `CLAUDE.md §19.7b` Gate 1 dispatched (NOT CERTIFIED — a stale-status documentation finding only, since reconciled — no code/design defect). Current, authoritative status: WP-17 / BA-01 = **IMPLEMENTATION AUTHORIZED — IMPLEMENTATION COMPLETE — NOT YET CERTIFIED** (`IMP-REPORT-WP-17 §11`/`§14`); C-023 = **🔴 RED — Not Implementation Ready** (unchanged); WP-18 = **CLOSED — CERTIFIED — RELEASE-READY** (unchanged). Annotated 2026-09-01 per the R9 governance-reconciliation pass, `CERT-WP-17` non-material observation O3.)* The `CLAUDE.md §18`/`§19.4` STOP-and-report discipline remains in force for anything not covered by D-1…D-6 (`§19.1`).

---

## Change Control

**File created (original pass, 2026-09-01):** this document — `architecture/05-Implementation/TDS-C023-A_Entitlement_License_Registry_Schema.md` (implementation-time schema Technical Design; design only). Independently reviewed — SOUND (design-only, no schema decided); non-material findings only.

**Decision-recording pass (2026-09-01, per the Repository Owner's own `IMPORTANT SEQUENCING` step 1 — "Update TDS-C023-A §19 to record these Repository Owner decisions verbatim"):** strikethrough-preserve, nothing erased.
- `§19` heading changed from "REPOSITORY OWNER / ARCHITECTURAL DECISION **REQUIRED**" to "REPOSITORY OWNER / ARCHITECTURAL DECISION"; its "remains HALTED until the Repository Owner explicitly answers" preamble struck and superseded.
- `§19.0` added as the header for the preserved (unchanged) D-1…D-7 question text.
- **`§19.1` added** — the Repository Owner's decision reproduced **verbatim** in a blockquote (D-1…D-7 approvals, the `IMPLEMENTATION BOUNDARIES` list, and the `IMPORTANT SEQUENCING`).
- **`§19.2` added** — a mapping table showing each approval applied to the corresponding `§3` element. **No element of `§3` was edited** — every recommendation in `§3`/`§18` was approved as recommended.
- **`§19.3` added** — the effect of the decision, including that implementation does not begin in this recording pass.
- `§20` ("No self-authorization") annotated strikethrough-preserve — the two bullets the Repository Owner's decision supersedes (resume authorization; schema approval) are struck with the reason; the remaining bullets (no migration/model/code created; no governance doc or `Backend/` file modified; C-023 stays RED / WP-17 status) are reaffirmed as still true of the document and the recording pass.
- This Change Control section updated.

**Not created — by the original pass or the decision-recording pass:** any Alembic migration; any production model / repository / service / router / Pydantic schema / test file. **The Alembic head is unchanged at `f9a3c7e1b5d2`.**
**Not modified — by the original pass or the decision-recording pass:** any `Backend/` file; `TDS-C023`; `IRA-C023`; the `WP-17` charter; `WPR-001`; `TDS-018`; `ADR-036`; any WP-18 certification artifact; `Master_Technical_Architecture.md`; `URA-001`; `CAP-001`; any C-040/WP-16 artifact; any C-023 Decision 1–6 record; `STOP-AND-REPORT-WP-17-01`. `IMP-REPORT-WP-17` is updated **separately** in the same recording pass (its own `§9` — per the Repository Owner's `IMPORTANT SEQUENCING` step 3).
**Nothing was staged, committed, or pushed.** Repository at `c2f93d5`.

**R9 governance-reconciliation annotation pass (2026-09-01), per direct Repository Owner authorization ("Repository Owner Authorization — WP-17 Gate 1 Governance Reconciliation"), resolving `CERT-WP-17` non-material observation O3:** `§19.3`'s "Statuses at the close of this recording pass" bullet and `§20`'s closing paragraph — both annotated (not struck; historically accurate for their own pass) with a dated note pointing to the current, authoritative status in `IMP-REPORT-WP-17 §11`/`§14`. No schema, decision text (`§19.1`/`§19.2`), or other content altered. This Change Control section updated. Not staged, committed, or pushed.

**R9-completion annotation pass (2026-09-01), per direct Repository Owner authorization ("Repository Owner Authorization — Complete WP-17 R9 Governance Reconciliation"), resolving the residual Gate 1 M-1 location the fresh Gate 1 re-attempt identified in this document:** the `§20` bullet parenthetical "…WP-17 remains … IMPLEMENTATION HALTED — NOT CERTIFIED …" — struck (strikethrough-preserve) and superseded with a dated note recording WP-17 / BA-01 = IMPLEMENTATION COMPLETE — NOT YET CERTIFIED (certification pending a fresh Gate 1). No schema, no D-1…D-7 or `§19.1`/`§19.2` decision text, and no other content was altered; "C-023 remains 🔴 RED" in the same bullet is preserved as still-true. This Change Control section updated. Not staged, committed, or pushed.

**Final pre-Gate-1 governance-cleanup pass (2026-09-01), per direct Repository Owner authorization ("Complete the final narrow governance cleanup before re-dispatching Gate 1"):** `§19.3`'s "Statuses at the close of this recording pass" bullet — the "WP-17 / BA-01 = IMPLEMENTATION AUTHORIZED — IMPLEMENTATION HALTED pending completion of the sequencing steps (schema decision now made; implementation not yet resumed)" clause converted from annotated-not-struck to full **strikethrough-preserve** format: the historical statement is struck and retained as historical record, with a dated superseding note stating the current factual status (**WP-17 / BA-01 = IMPLEMENTATION AUTHORIZED — IMPLEMENTATION COMPLETE — NOT YET CERTIFIED**; certification pending a fresh Gate 1). "C-023 = 🔴 RED — NOT IMPLEMENTATION READY" and "WP-18 = CLOSED — CERTIFIED — RELEASE-READY" in the same bullet are preserved as still-current. **The `§19.0`/`§19.1` verbatim Repository Owner quotation (including its "IMPLEMENTATION HALTED pending schema decision" line) was NOT touched — it is a protected verbatim historical record.** No schema (`§3`), no D-1…D-7 / `§19.1` / `§19.2` decision text, and no other content was altered. This Change Control section updated. Not staged, committed, or pushed.

**Final pre-Gate-1 governance-cleanup pass, follow-up (2026-09-02), per direct Repository Owner authorization ("Proceed with the final pre-Gate-1 governance cleanup exactly as follows"), resolving the residual M-1 and one borderline item the immediately-preceding independent review's repository-wide sweep identified in this document:** (1) the top-of-document **"NO SELF-AUTHORIZATION" callout (line 9)** — the "the schema shape remains an open … decision … remains HALTED" sentence struck (strikethrough-preserve) and superseded with a dated note recording that D-1…D-7 are RECORDED (`§19.1`) and implementation is COMPLETE — NOT YET CERTIFIED, and noting the `§19` heading rename; the first sentence ("Creating this Technical Design does **not** authorize implementation…", still true of the document itself) retained. (2) the **end-of-document italic note** — the "implementation resumes only after this recording is independently reviewed … it does NOT begin in this pass" clause struck and superseded with a dated note giving current status. **The `§19.0`/`§19.1` verbatim Repository Owner quotation was again NOT touched.** No schema (`§3`), no D-1…D-7 / `§19.1` / `§19.2` decision text, no Decision 1–6 / Decision 3 / Decision 4 semantics, and no C-023 🔴 RED classification were altered. No certification is claimed. Companion follow-up reconciliations in the same pass: `IMP-REPORT-WP-17 §7` (one bullet) and `STOP-AND-REPORT-WP-17-01` line 5 — both strikethrough-preserve. Not staged, committed, or pushed.

*End of Technical Design. The `§19` schema decision (D-1 … D-7) is RECORDED (`§19.1`).* ~~*Per the Repository Owner's `IMPORTANT SEQUENCING`, implementation resumes only after this recording is independently reviewed for fidelity and the approved schema is reconfirmed — it does NOT begin in this pass.*~~ *(Superseded 2026-09-01 — final pre-Gate-1 governance cleanup: the `IMPORTANT SEQUENCING` steps completed; implementation resumed and is COMPLETE, independently reviewed SOUND. **WP-17 / BA-01 = IMPLEMENTATION AUTHORIZED — IMPLEMENTATION COMPLETE — NOT YET CERTIFIED** — see `IMP-REPORT-WP-17 §11`/`§16`. C-023 remains 🔴 RED — NOT IMPLEMENTATION READY; D-1…D-7 and Decisions 1–6 unchanged.)*
