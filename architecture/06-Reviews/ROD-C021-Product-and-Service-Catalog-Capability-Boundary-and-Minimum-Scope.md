# ROD-C021 — Product & Service Catalog: Capability-Boundary and Minimum-Scope Decision

**Document type:** Repository Owner Decision record — a decision brief followed by recorded Repository Owner decisions, preceding the formal governance artifact (`IRA-C021`, prepared in the same pass) that cites it. Same class and structure as `ROD-C132-Enterprise-Notifications-Capability-Boundary-and-Minimum-Scope.md`.

**Capability:** C-021 Product & Service Catalog (`CAP-001` line 75 — Active, Domain D-002 Commercial & Subscription, owning specification **`COM-001`** — Commercial & Subscription Architecture, certified LOCKED under EARB Constitutional Recertification CR-3.0).

**Recorded:** 2026-09-09, per direct Repository Owner instruction ("REPOSITORY OWNER DECISION + GOVERNANCE AUTHORIZATION — C-021 PRODUCT & SERVICE CATALOG — ROD-C021 RECORDING + IRA-C021 PREPARATION — NO TDS / NO IMPLEMENTATION"), following a prior read-only "C-021 Capability-Boundary Decision Brief" (this same session) that investigated `CAP-001` (D-002 rows), `COM-001` (§2, §4 Universal Commercial Construct Model, §5 Subscription, §6 Offering Definition / Product & Service Catalog, §7 Customer & Commercial Account, §10 Cross-Document Integration, Freeze Statement), `PE-001-C021_Product_and_Service_Catalog.docx` in full (v1.1, Active — 1 CRB / 7 ERB / 13 EX / 11 INV), `PE-001-C023 §1.5`, `IRA-C023 §21` (Decision 3 formal investigation), `IRA-C132`/`ROD-C132`/`WP-19` and `IRA-C023`/`TDS-C023`/`WP-17` as minimum-scope precedents, `CMD-001 §26.3a`, `SER-001` (no C-021 entry found), `HISTORICAL-SCREEN-REALIZATION-MATRIX.md`, `EXECUTIVE-COGNITION-REALIZATION-STRATEGY.md`, the `C-003` Roles model/router/middleware as the platform-global-business-object precedent, and a repository-wide `Backend/` / `source/frontend/` scan (zero Offering / Product / Catalog / Plan / Pricing implementation of any kind).

**Authority:** Repository Owner (same decision-authority pattern established for `C-132`'s own pre-IRA decisions recorded in `ROD-C132`, `C-040`'s pre-IRA decisions recorded in `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md`, and `ADR-002`'s two `ROD-*` decision briefs).

**Classification key:** `[FACT]` — repository fact / verbatim from a LOCKED or Active source. `[RO DECISION]` — a Repository Owner decision, now made. `[PRECEDENT]` — established by a completed, certified Work Package. `[FUTURE TDS QUESTION]` — deferred to a finalized `TDS-C021`. `[FUTURE IMPLEMENTATION QUESTION]` — deferred to implementation time.

---

## A. Executive Decision Summary

C-021 has the cleanest governance path of any currently-unchartered Active capability: `[FACT]` its Primary Specification `COM-001` is certified LOCKED; its Enterprise Experience Specification `PE-001-C021` is v1.1, Active, engineered to the `PE-001-C005` Gold-Standard discipline; and it has **zero implementation** anywhere in the repository.

The three cross-capability boundary questions (C-021↔C-020, C-021↔C-022, C-021↔C-023) are **already settled by the LOCKED/Active specifications** (`PE-001-C021 §1.5`/`§2.10`, `COM-001 §2`/`§5`/`§6`, `PE-001-C023 §1.5`). The Repository Owner **confirms** them (D1–D3) and does not treat them as open decisions.

The Repository Owner **decides** five bounded items:
- **D4** — minimum first Business Activity scope: **Option A + D** (establish/manage a standalone Atomic Offering Definition; identity, name, Product/Service classification, opaque category reference, optional opaque `list_price_reference`, `draft` state, list, read).
- **D5** — Offering Composition and Offering Relationships: **EXCLUDED from BA-01** (future increments).
- **D6** — pricing: include the optional opaque `list_price_reference` **reference attribute only**; no computation / rating / discounting / execution.
- **D7** — lifecycle: BA-01 establishes an Offering Definition in **`draft`** only; **no** `draft → published` and **no** `published → retired` transition; publication/retirement are future increments; the approval-authority Pending Canonical Binding must not be silently solved by implementation.
- **D8** — catalog tenant scope: **Option A — platform-global catalog**; no `organization_id` tenant anchor; no tenant overlay; no segment-scoping; interim authorization gate = **`require_platform_admin`** (per the `C-003` Roles precedent); a future tenant-scoped overlay and a future canonical Catalog Governance Authority are each explicitly deferred with a recorded trigger.

C-023 Decision 3 (Global Entitlement Type / Feature Catalog governance-authority mechanism) is **preserved untouched** — chartering C-021 scoped to the commercial Offering Definition does not fire or reopen it (§R below).

**This document advances the C-021 governance sequence exactly one step: capability-boundary + minimum-scope decided. It does not authorize `TDS-C021`, `WP-20` registration, a BA-01 charter, implementation, schema, migration, API, frontend, CBOR registration, an ADR, a service-hosting decision, a commit, or a push.**

---

## B. C-021 Definition

- `[FACT]` `CAP-001` line 75: `| C-021 | Product & Service Catalog | Manage offerings. | COM-001 | Active |`. Domain **D-002 Commercial & Subscription** (`CAP-001 §D-002`: C-020–C-039).
- `[FACT]` Business Intent, verbatim (`PE-001-C021 §1.2`, "not paraphrased, not expanded, not redefined"): **"Manage offerings."**
- `[FACT]` C-021 is a **definitional, reference-producing capability upstream of commitment** (`PE-001-C021 §1.3`): *"it exists upstream of the commitment C-020 records, not downstream of it."*
- `[FACT]` `PE-001-C021` Guiding Architectural Question: the enterprise's *"single, continuously authoritative definition of what may currently be offered — its identity, composition, and current offering state — … as a stable fact other capabilities can reference,"* without that definition ever becoming the customer's commitment (C-020), the customer (C-022), the entitlement/feature availability (C-023), the price (C-024), the contract (C-025), the tenant (C-040), the access grant (C-002), or the workspace (C-008).

---

## C. Constitutional / PE-001 Basis

| Source | Status | Relevance |
|---|---|---|
| `COM-001` — Commercial & Subscription Architecture | **LOCKED** (EARB, CR-3.0) | Primary Specification. §2 Domain Ownership & Explicit Boundaries; §4 Universal Commercial Construct Model; §6 (COM-001-020…026) the Offering Definition / Product & Service Catalog (C-021) canonical model; §10 CBOR/BAR integration. |
| `PE-001-C021_Product_and_Service_Catalog.docx` | v1.1, **Active** | Enterprise Experience Specification. 1 CRB-C021; 7 ERBs (Establish Offering Context / Understand Offering Definition / Frame Offering Definition Intent / Shape & Assess Proposed Offering Definition / Commit Offering Definition Transition / Distribute Offering Reference Downstream / Resolve Offering Context Disruption); 13 EXs; 11 INVs. Masthead "Primary Specification Reference: SD-001" is stale doc-sync debt (same class `CAP-001` line 17 flags for `PE-001-C040`) — content authoritative. |
| `PE-001-C023 §1.5` | LOCKED-adjacent | Records the Global Entitlement Type / Feature Catalog governance authority as **Pending Canonical Binding** — "rather than assuming C-023, C-021, or any other capability owns it." |
| `IRA-C023 §21` | Accepted governance artifact | Decision 3 formal investigation — concluded the entitlement-type-catalog *domain* question is not C-021's (`PE-001-C021 §1.5` places entitlement definition / feature availability in C-023); C-023's own Decision 3 deferral concerns only C-023's internal authority mechanism. "No Global Entitlement Type/Feature Catalog exists anywhere in this repository, confirmed directly." |
| `CMD-001 §26.3a` | LOCKED | Canonical Business Object Eligibility Test (Step 1 Independent Identity + at least one of Step 2 Cross-Experience Reference / Step 3 Governed Lifecycle). |
| `C-003` Roles (`models/role.py`, `routers/role.py`, `middleware/tenant.py`) | CLOSED — CERTIFIED (WP-02) | Precedent for a **platform-global business object**: no `organization_id`, `require_platform_admin`-gated, tenant-middleware-exempt, with a version/status/effective-dating/supersedes lifecycle. |

---

## D. D1 — C-021 ↔ C-020 Boundary

**`[RO DECISION]` — CONFIRMED / SETTLED.**

- `[FACT]` `PE-001-C021 §2.10`: *"C-021 produces the Offering Reference C-020 consumes to anchor and shape a Subscription; C-021 never establishes, changes, or terminates a Subscription."*
- `[FACT]` `COM-001-010`/`011`: a Subscription "references an Offering Definition"; the Subscription Anchor is "consumed, never recomputed, from … the Offering."
- `[FACT]` `PE-001-C021 §1.3`: C-021 "exists upstream of the commitment C-020 records, not downstream of it."

**Decision:** C-021 owns the Offering Definition. C-020 owns Subscription / customer commitment. C-021 produces the Offering Reference consumed by C-020. **BA-01 shall not model, establish, modify, or terminate a Subscription.** A first C-021 BA has no dependency on C-020 (C-020 is unchartered; C-021 is its upstream producer).

---

## E. D2 — C-021 ↔ C-022 Boundary

**`[RO DECISION]` — CONFIRMED / SETTLED.**

- `[FACT]` `COM-001-033`: an Authoritative Account Context is "Never equivalent to a Workspace, Organization, Identity, Membership, or Billing Account." `COM-001-034`: "never redefines C-004 Organization, C-006 Person."
- `[FACT]` `PE-001-C021 §2.10`/`§1.9`: C-021 consumes a customer/account "segment reference **only where a canonical authority establishes segment-scoped offerings — Pending Canonical Binding; never assumed.**"

**Decision:** An Offering Definition exists independently of any Customer/Account. **BA-01 shall not require or model Customer/Account relationships. Segment-scoped offerings are excluded.** A first C-021 BA has no dependency on C-022; C-022 is unchartered and BA-01 does not need it.

---

## F. D3 — C-021 ↔ C-023 Catalog / Entitlement Boundary

**`[RO DECISION]` — CONFIRMED / SETTLED. C-023 Decision 3 preserved untouched (§R).**

- `[FACT]` `PE-001-C021 §1.5`: *"Licensing & Entitlement — entitlement definition, feature/capability availability and entitlement generation rules — **C-023**. C-021 never becomes Licensing & Entitlement, and an Offering Definition is never treated as equivalent to an Entitlement."*
- `[FACT]` `PE-001-C021 §2.10`: C-021 ↔ C-023 = "**No direct dependency**. C-023 may consume the Offering Reference indirectly via C-020's Subscription hand-off; C-021 never creates entitlement semantics."
- `[FACT]` `COM-001 §2`: C-023 Licensing & Entitlement is owned by URA-001; COM-001 "does not redefine License, Entitlement."
- `[FACT]` `IRA-C023 §21.12`: C-023 Decision 3 defers only the *governance-authority mechanism* for adding a global entitlement type — entirely within C-023's own domain.

**Decision:** C-021 owns the commercial Offering Definition. C-023 owns Licensing & Entitlement, including entitlement definition and feature/capability availability. **C-021 BA-01 has NO direct dependency on C-023. BA-01 shall NOT implement entitlement/feature semantics.** C-023 Decision 3 remains untouched and remains a C-023-internal deferred governance item; chartering C-021 (scoped to the commercial Offering Definition per D4) does **not** fire C-023 Decision 3's recorded trigger.

**Disclosure:** a *future* C-021 increment that adds an "entitlement types conferred by this offering" cross-reference would be C-023's domain to define and would fire C-023 Decision 3's own trigger — **BA-01 as decided does not.**

---

## G. D4 — Minimum BA-01 Scope

**`[RO DECISION]` — DECIDED: OPTION A + D.**

BA-01 shall establish / manage a **standalone Atomic Offering Definition** with:
- canonical identity (`PREFIX-NNNNNN` form, per `COM-001-001`);
- canonical name;
- Product / Service classification (`COM-001-021` — a Product is an Offering Definition realized through a standalone deliverable; a Service through enterprise activity on a customer's behalf);
- opaque **category reference** (`COM-001-024` — catalog organization; enterprise-wide taxonomy governance authority is Pending Canonical Binding, so the value is a reference, not a governed FK);
- optional opaque **`list_price_reference`** (`COM-001-020` / `PE-001-C021 §1.5` — reference attribute only; see D6);
- current offering **state = `draft`** (`COM-001-020`);
- **list** Offering Definitions;
- **read** one Offering Definition by id.

BA-01 must produce the first **Authoritative Offering Definition Context** (`COM-001-002`) and a stable **Offering Reference** (`ERB-C021-06` — for future consumption by C-020, C-024, C-025).

`[FACT]` This is the smallest slice delivering Business Outcome `C021-O01` ("Authoritative Offering Definition") with zero cross-capability dependency, and is a strict subset of every richer C-021 model (`[FUTURE IMPLEMENTATION QUESTION]`: none of the excluded scope creates a deprecation obligation).

---

## H. D5 — Composition / Relationships

**`[RO DECISION]` — DECIDED: EXCLUDE from BA-01.**

Excluded from BA-01, each a `[FUTURE IMPLEMENTATION QUESTION]` for a future C-021 increment:
- Composition (`COM-001-022` / `PE-001-C021 §1.21`): **Composite Offering, Bundle, Package, Variant, Edition, Optional Component, Add-on**.
- Relationships (`COM-001-023` / `PE-001-C021 §1.22`): **replaces / superseded-by, successor / predecessor, depends-on, bundled-with, optional-with, mutually-exclusive, complementary**.

`[FACT]` Rationale: composition/relationships are a distinct catalog-definitional concern (a self-referential graph), whose *evaluation/enforcement* at a customer commitment is explicitly C-020's — not needed for a base Atomic Offering Definition.

---

## I. D6 — `list_price_reference` / Pricing

**`[RO DECISION]` — DECIDED: include the optional opaque `list_price_reference` as a reference attribute ONLY.**

- `[FACT]` `PE-001-C021 §1.5`: C-021 "exposes a list-price reference attribute of an offering definition only, and **never computes or executes a price**."
- The attribute must never: calculate price; rate; discount; execute pricing; become a numeric / computed price field. Any downstream integrity constraint (`[FUTURE TDS QUESTION]`) shall enforce reference-only, non-computational semantics — recommended shape mirrors `c132_notification.source_id` / `source_type` (an opaque, non-authoritative citation).
- `[FACT]` Pricing Execution (dynamic pricing computation, rating, discounting) remains **Pending Canonical Binding** (no canonical Pricing Engine authority) and outside C-021 BA-01; the eventual computed price is C-024's (Billing) concern (`COM-001-022`).

---

## J. D7 — Lifecycle

**`[RO DECISION]` — DECIDED: BA-01 establishes an Offering Definition in `draft` only.**

- BA-01 does **NOT** implement `draft → published` or `published → retired`.
- `[FACT]` Publication and Retirement are future increments (`COM-001-025`/`026`, `ERB-C021-05`, `EX-C021-09`/`10`).
- `[FACT]` The **approval-authority Pending Canonical Binding** (`PE-001-C021 §1.5`, `COM-001-026`: "Approval … where a canonical approval authority exists — otherwise Pending Canonical Binding") **must not be silently solved by implementation.** Keeping BA-01 to `draft` avoids that load-bearing gap.
- `[FUTURE TDS QUESTION]`: whether the `state` column is CHECK-constrained to the full closed set (`draft`/`published`/`retired`) for schema correctness even though BA-01 only ever writes `draft` (mirrors the `access_evaluation_outcome` / `c023_*` precedent of declaring the full lifecycle enum while a first BA writes a subset).

---

## K. D8 — Catalog Tenant Scope

**`[RO DECISION]` — DECIDED: OPTION A — PLATFORM-GLOBAL CATALOG.**

- `[FACT]` `PE-001-C021 §1.9`/`§2.10` record catalog tenant-scope semantics as **Pending Canonical Binding**; `COM-001 §1` frames the catalog as "what is being commercially offered" by "the enterprise" (singular).
- **Decision:** the C-021 catalog for BA-01 is **platform-global**. Therefore:
  - **no `organization_id` tenant anchor** on the Offering Definition;
  - **no tenant-specific catalog overlay** in BA-01;
  - **no segment-scoped catalog**;
  - a **platform-global authority gate** applies — interim mechanism = **`require_platform_admin`**, per the existing repository precedent.
- `[PRECEDENT]` `C-003` Roles (`models/role.py`) is a platform-global business object with **no `organization_id`**, gated by **`require_platform_admin`**, tenant-middleware-exempt (`/roles` "tenant-agnostic … Roles are platform-global, URA-001 Section 3, no organization_id column"), with a `version` / `status` / `effective_from`/`effective_to` / `approval_reference` / `supersedes_id` version-managed lifecycle that maps closely to `COM-001-025`'s Current / Future / Historical Definition model. This is the direct D8 precedent.
- **Deferred, each with a recorded trigger:**
  - a future **tenant-scoped catalog overlay** (`[FUTURE IMPLEMENTATION QUESTION]` — trigger: a chartered capability that genuinely requires per-tenant catalog curation or segment-scoped offerings);
  - a canonical **Catalog Governance Authority** replacing the interim `require_platform_admin` gate (`[FUTURE IMPLEMENTATION QUESTION]` — trigger: implementation need for offering *approval*, taxonomy *governance*, or retirement *notice* policy in a C-021 BA — i.e. anything past `draft`, per D7; mirrors `IRA-C023 §21.12`'s Decision-3 deferral pattern).

---

## L. Approved BA-01 Governance Definition

**BA-01 — Establish / Manage Offering Definition.**

**Purpose:** Create the enterprise's authoritative definition of a standalone Atomic Offering that may subsequently be referenced by downstream commercial capabilities.

**In scope:** establish an Atomic Offering Definition; canonical identity; canonical name; Product / Service classification; opaque category reference; optional opaque `list_price_reference`; `draft` state; list; read; produce the Authoritative Offering Definition Context and the stable Offering Reference.

**Out of scope:** composition; relationships; publication; retirement; pricing computation; rating; discounting; availability; Subscription; Customer / Account; Entitlement; Feature Catalog; Billing; Contract; segment-scoping; tenant-specific overlays; taxonomy governance authority; Catalog Governance Authority; order; inventory; fulfillment; provisioning; usage; metering; taxation; discovery / overlap detection (`EX-C021-13`); future-dated transitions; external product integrations; marketplace / CRM / ERP functionality; any API / schema / event / service / workflow-engine implementation (that is `IRA` → `TDS` → charter work).

---

## M. Explicit Exclusions (consolidated)

`[RO DECISION]` — BA-01 explicitly excludes, each with an evidence basis:

| Excluded | Basis |
|---|---|
| Offering Composition (Composite / Bundle / Package / Variant / Edition / Optional Component / Add-on) | `COM-001-022`; D5 |
| Offering Relationships (replaces / superseded-by / successor / predecessor / depends-on / bundled-with / optional-with / mutually-exclusive / complementary) | `COM-001-023`; D5 |
| Publication (`draft → published`) and Retirement (`published → retired`), revision of a published offering | `COM-001-025`/`026`; D7 |
| Pricing computation / rating / discounting / execution | `PE-001-C021 §1.5`; Pending Canonical Binding; D6 |
| Availability determination (whether a specific customer may commit) | `COM-001-026` — the consuming capability's (C-020) concern |
| Subscription | `PE-001-C021 §1.5`/`§2.10`; D1 |
| Customer / Account, Customer–Account relationship, segment-scoping | `PE-001-C021 §1.5`/`§2.10`; D2 |
| Entitlement, Feature Catalog, entitlement generation | `PE-001-C021 §1.5`/`§2.10`; D3 |
| Billing, invoicing, payment | `PE-001-C021 §1.5`; `COM-001 §8` = C-024 |
| Contract instruments | `PE-001-C021 §1.5`; `COM-001 §9` = C-025 |
| Tenant-specific overlays; per-tenant catalog | D8 (platform-global) |
| Catalog taxonomy governance authority; offering approval authority; retirement notice policy | `PE-001-C021 §1.5`; Pending Canonical Binding |
| Order / inventory / fulfillment / provisioning / usage / metering / taxation | `COM-001 §2`; `PE-001-C021 §1.5`; Pending Canonical Binding |
| Discovery / overlap detection (`EX-C021-13`) | richer downstream experience; not needed for establish |
| Future-dated commit scheduling | `PE-001-C021 §1.24`; Pending Canonical Binding |
| External product integrations; marketplace / CRM / ERP | `PE-001-C021 §1.5` |

---

## N. Dependencies

`[FACT]` / `[RO DECISION]`:

| Dependency | Classification for BA-01 | Basis |
|---|---|---|
| C-004 Organization | **NOT REQUIRED** | D8 platform-global — no `organization_id` anchor |
| C-020 Subscription Management | **NOT REQUIRED** | D1 — C-021 is upstream; C-020 unchartered |
| C-022 Customer & Account Management | **NOT REQUIRED** | D2 — segment-scoping excluded; C-022 unchartered |
| C-023 Licensing & Entitlement | **NOT REQUIRED** | D3 — "No direct dependency" |
| C-003 Approval Authority (WP-02 / WP-18) | **NOT REQUIRED for BA-01** (interim `require_platform_admin` gate); a canonical Catalog Governance Authority is a `[FUTURE IMPLEMENTATION QUESTION]` | D7 / D8 |
| C-040 Tenant Administration / tenant infra | **NOT REQUIRED for BA-01** (platform-global); `[FUTURE IMPLEMENTATION QUESTION]` for a tenant overlay | D8 |
| Audit infrastructure (`record_audit` / `AuditLogger`) | **AVAILABLE — reuse** | Used by every prior WP; `COM-001-063` confirms SD-002 §6 Evidence applies |
| Event / broker infrastructure | **NOT REQUIRED** | BA-01 produces a reference consumed *by reference*; no cross-service trigger; no concrete `EventSubscriber` exists (`TD-151`) |
| D-002 service host | **`[FUTURE TDS QUESTION]` — requires an RO decision at IRA/TDS stage** | No D-002 service exists; see §P |

---

## O. Authority Model

- `[FACT]` `PE-001-C021` provides **no canonical approval/commit authority** for establishing an Offering Definition — `§1.5` records offering approval authority as Pending Canonical Binding; `§1.11` personas "do not define authorization roles"; `§1.9` names only the generic `C-002 / URA-001` Access Evaluation Outcome mechanism.
- `[RO DECISION]` (D8): BA-01's interim authorization gate is **`require_platform_admin`**.
- `[PRECEDENT]` This is the established repository pattern for a platform-global business object (`C-003` Roles, WP-02 — every `/roles` mutation is `require_platform_admin`-gated). It is **not** the tenant-scoped `require_matching_tenant_or_platform_admin` pattern used for C-041 Configuration or C-132 Notifications, because D8 makes the C-021 catalog platform-global, not tenant-scoped.
- `[FUTURE IMPLEMENTATION QUESTION]` A canonical **Catalog Governance Authority** (who may approve/publish/retire an offering, govern taxonomy, set retirement notice policy) is deferred with a recorded trigger (implementation need for any C-021 BA past `draft`), mirroring `IRA-C023 §21.12`'s Decision-3 deferral discipline.
- `[FACT]` Audit evidence: `record_audit()` on establish (the universal platform pattern); the actor is the `PLATFORM_ADMIN` caller's `person_id`; the resource is the Offering Definition id; `SD-002 §6` Evidence applies per `COM-001-063`.

---

## P. Service Hosting — Explicitly a Future Decision

- `[FACT]` The five physical services are `AuthService`, `AIService`, `IngestionService`, `ReportingService`, `TenantService`. **No D-002 / commercial service exists.**
- `[PRECEDENT]` `ADR-036` established the modular-monolith posture — a new dedicated service is disfavored in the current phase; `C-023` (the adjacent D-002 capability) is hosted in **`AuthService`**.
- `[FUTURE TDS QUESTION]` A formal service-hosting decision is required at the `IRA-C021` / `TDS-C021` stage (mirroring `TDS-C132 §6.5` H-1). Candidate hosts: **`AuthService`** (co-location with C-023, consistent with `ADR-036`'s modular-monolith trend) or a **new `CommercialService`** (cleaner single-owner but triggers a `CLAUDE.md §18`/`§19.4` new-service STOP-and-report and runs against the modular-monolith preference). **This ROD does not decide it.**
- `[FACT]` BA-01 can be implemented with **no new infrastructure** — a single additive table + router in an existing service; no event bus; no cross-service call.

---

## Q. Persistence / Business Object Governance

- `[FACT]` An Offering Definition **is a genuine persistent Business Object** — `COM-001-020`/`061` state it explicitly; `PE-001-C021 §1.16`/`§1.24` require an Authoritative Context with retained Historical lineage.
- `[FACT]` `CMD-001 §26.3a` Business Object Eligibility Test applied:
  - **Step 1 — Independent Identity:** satisfied — `PREFIX-NNNNNN` identity persisting as the Authoritative Offering Definition Context beyond any request (`COM-001-001`/`020`).
  - **Step 2 — Cross-Experience Reference Test:** satisfied — the Offering Reference is explicitly named as Consumed Context, retrieved by identity, by C-020 (Subscription Anchor, `COM-001-011` — "consumed, never recomputed, from … the Offering"), C-024 (Billing), and C-025 (Contract) — capabilities other than the one that produces it (`PE-001-C021 §1.4`/`§2.10`, "Produced for reference").
  - **Step 3 — Governed Lifecycle:** satisfied — `draft → published → retired`, Historical Definitions retained in lineage (`COM-001-025`).
  - → **ELIGIBLE for CBOR registration** (Step 1 + Step 2 + Step 3).
- `[FACT]` `COM-001-005` (Registration Precedes Implementation) + `CMD-001 §26.3`: **CBOR registration is required before implementation**, via a dedicated ADR (mirroring `ADR-019`'s registration of `CFG-000001` for WP-10). BAR registration of the BA-01 Business Activity is likewise required (`COM-001-060`).
- `[FUTURE TDS QUESTION]` Exact table name, column set, the anchor key (platform-global — no `organization_id`, per D8), whether `category` and `list_price_reference` are opaque `String` references (recommended) or FKs, `state` CHECK constraint set, index set, versioning/`supersedes` columns, and the schema-shape `CLAUDE.md §18`/`§19.4` STOP-and-report — all deferred to a finalized `TDS-C021`.
- `[FUTURE IMPLEMENTATION QUESTION]` Idempotency mechanism for establish (natural-key / double-submit), unless a concrete concurrency risk is identified (mirrors `TD-152` disposition).

---

## R. C-023 Decision 3 Preservation

**`[FACT]` C-023 Decision 3 (Global Entitlement Type / Feature Catalog governance-authority mechanism) is untouched by this ROD and by chartering C-021.**

- `IRA-C023 §21.12` recorded Decision 3 as **DEFERRED (Option A — Defer with a Recorded Trigger)**. That deferral concerns *what mechanism or accountability point may add a new global entitlement type*, **within C-023's own already-attributed domain** — not which capability owns the catalog.
- `PE-001-C021 §1.5` places "entitlement definition, feature/capability availability and entitlement generation rules" in **C-023**, not C-021. `PE-001-C021 §2.10` records C-021 ↔ C-023 as "**No direct dependency**."
- C-023 Decision 3's own recorded trigger — "implementation need … for another formally chartered capability that requires creation, modification, or governance of global Entitlement Types/Feature definitions" — is **not fired** by C-021 BA-01, because BA-01 (per D3/D4/M) does not create, modify, or govern any entitlement type or feature definition.
- This ROD does **not** modify `IRA-C023`, `TDS-C023`, `TDS-C023-A`, any `WP-17` artifact, `CERT-WP-17`, or any C-023 Decision (1–6). C-023 capability-wide status (**🔴 RED — Not Implementation Ready**, `IRA-C023 §16`) is unchanged.
- Disclosure (repeated from §F): a *future* C-021 increment adding an "entitlement types conferred" cross-reference would fire C-023 Decision 3's trigger — **BA-01 as decided does not.**

---

## S. What This Decision Does NOT Authorize

Recording D1–D8 and preparing `IRA-C021` **does not authorize**:

- `TDS-C021` creation;
- `WP-20` registration;
- a BA-01 charter;
- Implementation Authorization of any kind;
- any schema / migration / ORM model / repository / service / router / test;
- any frontend implementation or modification;
- a service-hosting decision;
- CBOR registration or the CBOR ADR;
- BAR registration;
- any edit to `COM-001`, `PE-001`, `PE-001-C021`, `CAP-001`, `SD-001`, `SD-002`, `SD-003`, `URA-001`, `CMD-001`, `GRC-001`, `PLT-001`, `RTA-001`, `EIA-001`, `DS-001`, `ARCH-000`, `ADR-002`, `ADR-003`, `ADR-016`, `ADR-023`, `ADR-036`;
- any edit to C-023 governance (`IRA-C023`, `TDS-C023`, `TDS-C023-A`, `WP-17`, `CERT-WP-17`) or any C-023 Decision;
- reopening C-020 / C-022 / C-040 / C-114 / WP-13 scope;
- firing C-023 Decision 3;
- a commit;
- a push.

It authorizes exactly: **C-021 capability-boundary + minimum-BA-01 governance definition (D1–D8), followed by `IRA-C021` readiness assessment against that definition.**

---

## T. Next Governance Sequence

`[FACT]` This ROD → **`IRA-C021`** (prepared in this same pass) → Strategic Enhancement Review (no C-021 `SE-XXX` entry exists in `SER-001` — Not Applicable) → Historical Screen Review (`HISTORICAL-SCREEN-REALIZATION-MATRIX.md` row 6 `06-admin-dashboard.html` is marked RETIRE CONCEPT — the old vendor-console manual-approve/price-calculator workflow explicitly conflicts with `COM-001`'s Offering/Approval-as-fitness-to-publish model; no C-021 historical screen is to be realized) → Executive Cognition Review (`EXECUTIVE-COGNITION-REALIZATION-STRATEGY.md` does not name C-021 — Not Applicable) → existing-asset discovery (zero Offering/Product/Catalog implementation) → `CMD-001 §26.3a` Business Object eligibility (ELIGIBLE, §Q) → DS-001 conformance check → **service-hosting RO decision** (`AuthService` vs. `CommercialService`) → **`IRA-C021` acceptance** → **`TDS-C021`** (with the mandatory schema-shape `CLAUDE.md §18`/`§19.4` STOP-and-report) → **`WP-20` registration** (`WPR-001 §3` Maintenance Rule (b)) + **`WP-20` BA-01 charter** → **separate, explicit Repository Owner Implementation Authorization** → implementation → `CLAUDE.md §19.7b` five-gate closure (Gate 1 Independent Certification, Gate 2 V&V Audit, Gates 3/4 if triggered, Gate 5 Release Readiness Audit) → formal closure → controlled explicit-path commit → push. **This document does not advance past "capability-boundary and minimum-scope decided" in that sequence; the pass it belongs to also prepares and independently reviews `IRA-C021` and stops there.**

---

## Change Control

**Files created by the pass this ROD belongs to:** this document — `architecture/06-Reviews/ROD-C021-Product-and-Service-Catalog-Capability-Boundary-and-Minimum-Scope.md` — and `architecture/05-Implementation/IRA-C021_Product_and_Service_Catalog_Implementation_Readiness_Assessment.md`.
**Files read for cross-reference, not modified:** `CAP-001`, `COM-001`, `PE-001-C021_Product_and_Service_Catalog.docx`, `PE-001-C023`, `IRA-C023` (§16, §21), `TDS-C023`/`TDS-C023-A` (read only), `CMD-001 §26.3a`/`§26.3`/`§26.4`, `SER-001`, `HISTORICAL-SCREEN-REALIZATION-MATRIX.md`, `EXECUTIVE-COGNITION-REALIZATION-STRATEGY.md`, `ADR-036`, `ADR-019`, `ROD-C132`, `IRA-C132`, `TDS-C132`, `WP-19` charter, `Backend/Services/AuthService/models/role.py`, `routers/role.py`, `middleware/tenant.py`, `dependencies.py`, `WPR-001`, `WP-REG-001`.
**Not modified:** any LOCKED constitutional document (`COM-001`, `PE-001`, `CAP-001`, `SD-001`, `SD-002`, `SD-003`, `URA-001`, `CMD-001`, `GRC-001`, `PLT-001`, `RTA-001`, `EIA-001`, `DS-001`, `ARCH-000`, `ADR-002`/`003`/`016`/`023`/`036`); any C-023 / WP-17 artifact or C-023 Decision; any `Backend/` or `source/frontend/` file, migration, or test; `WPR-001`, `WP-REG-001`, `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md`, `SER-001` (no additive C-021 status row is created by this pass — `WP-20` is not registered and no `WPR-001 §3` Maintenance-Rule trigger has fired); any unrelated pre-existing working-tree change. Nothing staged, committed, or pushed.

*End of ROD-C021.*
