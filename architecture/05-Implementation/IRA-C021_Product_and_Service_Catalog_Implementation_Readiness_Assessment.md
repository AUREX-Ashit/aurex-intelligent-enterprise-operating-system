# IRA-C021 — Product & Service Catalog (C-021) — Implementation Readiness Assessment

**Document ID naming note (established fact, mirrors `IRA-C132`'s, `IRA-C066`'s and `IRA-C114`'s own precedent):** this document is named capability-first, with no WP number. No WP number exists for C-021 anywhere in `WP-REG-001` or `WPR-001` as of this drafting (`WPR-001 §3` Maintenance Rule: "No future WP may be added speculatively… until it is properly assigned"). Capability-first naming avoids misrepresenting this document as governing an already-numbered Work Package.

**Repository Owner authorization basis for this document:** a sequence of explicit Repository Owner instructions, this session — (1) a "C-021 Product & Service Catalog — Capability-Boundary Decision Brief" (read-only investigation); (2) the Repository Owner's own recorded capability-boundary and minimum-scope decisions D1–D8, `architecture/06-Reviews/ROD-C021-Product-and-Service-Catalog-Capability-Boundary-and-Minimum-Scope.md` (created in this same pass); (3) the Repository Owner's explicit instruction: *"PART B — prepare and execute the C-021 Implementation Readiness Assessment (IRA-C021)… The governance sequence must stop after the IRA is prepared and independently reviewed."* This document runs the governed IRA process against the already-decided boundary and scope D1–D8 — it does not reopen, reinterpret, or re-derive them.

**This IRA does not grant IRA acceptance.** Per this repository's own no-self-authorization discipline (`CLAUDE.md §19.1`) and the explicit precedent of `IRA-C132 §19`/`§21`, `IRA-C066 §18`, `IRA-C114 §18`, and `IRA-C023`, acceptance is a separate, future Repository Owner review. This document also does not authorize `TDS-C021`, `WP-20` registration, a BA-01 charter, implementation, schema, migration, API, frontend, a CBOR ADR, a service-hosting decision, a commit, or a push.

**On "TDS may proceed" language later in this document (§22):** where §22 states that `TDS-C021` *drafting* "MAY begin," that is a readiness characterization of the assessment outcome — the same distinction `IRA-C132 §21` draws for its own AMBER verdict — not an authorization. `TDS-C021` drafting is authorized only by a future, separate Repository Owner instruction that first accepts this IRA; and `TDS-C021` may not be *finalized*, nor any implementation artifact created, until the service-hosting Repository Owner decision (§17), the CBOR registration ADR, and BAR registration (§8) are complete.

---

## 1. Executive Summary

**(Established fact.)** C-021 Product & Service Catalog is `CAP-001`-registered (line 75 — **Active**, Domain **D-002 Commercial & Subscription**, owning specification **`COM-001`**, certified LOCKED under EARB Constitutional Recertification CR-3.0). No Business Activity has ever been chartered against C-021. No IRA has ever existed for it before this document. **Unlike C-132, C-021 has a dedicated, Active Enterprise Experience Specification** — `PE-001-C021_Product_and_Service_Catalog.docx`, v1.1, engineered to the `PE-001-C005` Gold-Standard discipline (1 CRB, 7 ERBs, 13 EXs, 11 INVs). C-021's governance substrate is therefore *more* complete than any recently-chartered capability's.

**(Repository Owner decisions, recorded, not re-derived by this document — `ROD-C021…md` D1–D8.)**
- **D1 — C-021 ↔ C-020:** CONFIRMED/SETTLED. C-021 owns the Offering Definition; C-020 owns Subscription/commitment; C-021 produces the Offering Reference C-020 consumes. BA-01 shall not model a Subscription.
- **D2 — C-021 ↔ C-022:** CONFIRMED/SETTLED. Offering Definition exists independently of Customer/Account. BA-01 shall not model Customer/Account; segment-scoped offerings excluded.
- **D3 — C-021 ↔ C-023:** CONFIRMED/SETTLED. C-021 owns the commercial Offering Definition; C-023 owns Licensing & Entitlement. **No direct dependency.** BA-01 shall not implement entitlement/feature semantics. C-023 Decision 3 untouched.
- **D4 — minimum BA-01 scope:** OPTION A + D — a standalone Atomic Offering Definition (identity, name, Product/Service classification, opaque category reference, optional opaque `list_price_reference`, `draft` state), list, read; produce the first Authoritative Offering Definition Context and a stable Offering Reference.
- **D5 — composition/relationships:** EXCLUDED from BA-01.
- **D6 — pricing:** optional opaque `list_price_reference` reference attribute ONLY; no computation/rating/discounting/execution.
- **D7 — lifecycle:** BA-01 establishes in `draft` only; no `draft → published`, no `published → retired`; approval-authority Pending Canonical Binding must not be silently solved.
- **D8 — catalog tenant scope:** OPTION A — PLATFORM-GLOBAL. No `organization_id`; no tenant overlay; no segment-scoping; interim authority gate = `require_platform_admin` per the `C-003` Roles precedent; future tenant overlay and future canonical Catalog Governance Authority each deferred with a recorded trigger.

**Readiness verdict (§22): 🟡 AMBER — READY FOR TECHNICAL DESIGN PREPARATION, CONDITIONAL ON ONE OUTSTANDING REPOSITORY OWNER DECISION (service hosting).** No capability-defeating blocker exists. The one substantive open item is which service hosts the C-021 Offering Definition persistence (`AuthService`, co-located with the adjacent D-002 capability C-023 and consistent with `ADR-036`'s modular-monolith posture — or a new `CommercialService`, which would itself trigger a `CLAUDE.md §18`/`§19.4` new-service STOP-and-report). **Critically, C-021 does *not* carry C-132's own write-fan-in complication** — a Notification had to be written by many other services' transactions; an Offering Definition is established by a single, direct, authenticated `PLATFORM_ADMIN` action against C-021's own host, with no cross-service write path and no event bus involved.

---

## 2. Capability Analysis

**(Established fact, `CAP-001` line 75, direct read.)**

| Field | Value |
|---|---|
| Capability ID | C-021 |
| Capability Name | Product & Service Catalog |
| Business Intent | "Manage offerings." |
| Domain | D-002 — Commercial & Subscription (C-020–C-039) |
| Owning Specification | `COM-001` (Commercial & Subscription Architecture) — **LOCKED** (EARB, CR-3.0) |
| Status | Active |

**(Established fact, `COM-001 §6`, direct read.)** `COM-001-020` through `COM-001-026` are the canonical Offering Definition / Product & Service Catalog model: identity, category, composition, key attributes (incl. a list-price *reference* attribute), and a `draft → published → retired` state model (`-020`); Product / Service / Digital / Physical typology (`-021`); Composition (`-022`); Relationships (`-023`); Taxonomy (`-024`, enterprise-wide governance authority **Pending Canonical Binding**); Version Management (`-025`, Retirement terminal — "never deletion"); Publication ≠ Availability (`-026`, approval authority **Pending Canonical Binding**). `COM-001-061`: an Offering Definition is a **CBOR-registered Business Object** once implemented. `COM-001-005`: **Registration Precedes Implementation**.

**(Established fact, `PE-001-C021`, direct read, v1.1 Active.)** Guiding Architectural Question: the enterprise's *single, continuously authoritative definition of what may currently be offered — identity, composition, current offering state — as a stable fact other capabilities can reference*, without ever becoming the commitment (C-020), the customer (C-022), the entitlement (C-023), the price (C-024), the contract (C-025), the tenant (C-040), the access grant (C-002), or the workspace (C-008). 7 ERBs: Establish Offering Context / Understand Offering Definition / Frame Offering Definition Intent / Shape & Assess Proposed Offering Definition / Commit Offering Definition Transition / Distribute Offering Reference Downstream / Resolve Offering Context Disruption. **Masthead "Primary Specification Reference: SD-001" is stale doc-sync debt** (same class `CAP-001` line 17 flags for `PE-001-C040`) — content is authoritative; `COM-001` is the true Primary Specification per `CAP-001` line 75. Carried forward as a non-blocking open item (§23).

---

## 3. Existing Asset Discovery (`CLAUDE.md §19.2`, `IMP-001 §6.2a`)

**(Established fact, direct repository inspection this session.)**

### 3.1 Backend — genuinely zero footprint

A repository-wide, case-insensitive search of `Backend/` (excluding `venv`/`__pycache__`) for `offering`, `catalog`, `product`, `pricing`, `list_price`, `plan` (commercial sense) returns **zero domain hits**. No model, repository, service, router, schema, or migration for an Offering Definition, Product, Catalog, or any `COM-001 §6` construct exists anywhere in any of the five physical services. `AuthService/models/__init__.py` was read directly — nothing offering-shaped is registered. **No D-002 commercial capability has any physical footprint** other than C-023's own tables (`c023_license_context`, `c023_entitlement_context`), which are Licensing & Entitlement, not catalog.

### 3.2 Frontend — zero catalog footprint; one structural precedent

- No Offering / Product / Catalog / Plan component, page, type, or API client exists in `source/frontend/`.
- `source/frontend/src/config/admin-navigation.ts` has a nav parent `slug: "subscriptions"` ("Subscription & Commercial Management", route `/platform-admin/subscriptions`) with one child today — the C-023 entitlement-license screen at `/platform-admin/subscriptions/entitlement-license` (WP-17). This is the natural nav home for a future C-021 catalog screen (**not decided here** — a TDS/charter-time disposition).
- **Structural precedent:** `source/frontend/src/features/entitlement-license/{components/*.tsx, state/useEntitlementLicense.ts}` (WP-17, C-023) is the established per-capability frontend pattern this repository would likely mirror for C-021's own establish/list/read screens — cited as precedent, not prescribed.

### 3.3 Platform-global business object — a directly applicable, certified precedent exists

**(Established fact, direct read of `Backend/Services/AuthService/models/role.py`, `routers/role.py`, `middleware/tenant.py`.)** The `C-003` Roles object (WP-02, CLOSED — CERTIFIED) is a **platform-global business object**:
- `roles` table has **no `organization_id` column** — columns are `id`, `role_code`, `role_name`, `description`, `is_system_role`, `version`, `status`, `effective_from`, `effective_to`, `approval_reference`, `supersedes_id`, `created_at`, `updated_at`.
- Every `/roles` mutation is gated by `Depends(require_platform_admin)`.
- `/roles` is in the `middleware/tenant.py` exemption list — tenant-agnostic, `X-Tenant-ID` not required ("Roles are platform-global, URA-001 Section 3, no organization_id column").
- Its `version` / `status` / `effective_from`/`effective_to` / `approval_reference` / `supersedes_id` shape is a **version-managed lifecycle** that maps closely to `COM-001-025`'s Current / Future / Historical Definition model and `PE-001-C021 §1.24`.

This is the direct D8 (platform-global) precedent for C-021's Offering Definition. **No new authorization or persistence mechanism is required** — the pattern exists, is certified, and is in production use.

### 3.4 Audit and event infrastructure — reuse audit; no event bus needed

- `record_audit()` / `publish_event()` (structured-log audit + structured-log event stand-in) are the universal cross-cutting pattern every closed WP uses. **Directly reusable** for C-021 establish. `COM-001-063` confirms `SD-002 §6` Evidence applies to Offering Definition transitions.
- `Backend/Shared/Events` `EventPublisher`/`EventSubscriber` remain abstract with no production concrete subscriber (`TD-151`). **C-021 BA-01 needs none of this** — an Offering Definition is consumed *by reference* (a downstream capability reads it by identity when it needs it), not delivered through a broker. No infrastructure gap.

### 3.5 No prior IRA/BA/WP/charter for C-021

Confirmed by direct inspection of `WPR-001` (WP-00 through WP-19) and `WP-REG-001` — no C-021 entry anywhere.

---

## 4. RO Decision History (recorded, not re-derived)

Reproduced in substance from `ROD-C021-Product-and-Service-Catalog-Capability-Boundary-and-Minimum-Scope.md` (see that document for the full text and evidence basis; this section is a pointer, not a re-decision):

1. **D1 — C-021 ↔ C-020 = CONFIRMED/SETTLED.** C-021 owns the Offering Definition; C-020 owns Subscription; C-021 produces the Offering Reference; BA-01 shall not model/establish/modify/terminate a Subscription.
2. **D2 — C-021 ↔ C-022 = CONFIRMED/SETTLED.** Offering Definition independent of Customer/Account; BA-01 shall not require/model Customer/Account; segment-scoped offerings excluded.
3. **D3 — C-021 ↔ C-023 = CONFIRMED/SETTLED.** C-021 owns commercial Offering Definition; C-023 owns Licensing & Entitlement; no direct dependency; BA-01 shall not implement entitlement/feature semantics; C-023 Decision 3 untouched, remains C-023-internal deferred.
4. **D4 — minimum BA-01 scope = OPTION A + D.** Standalone Atomic Offering Definition: identity, name, Product/Service classification, opaque category reference, optional opaque `list_price_reference`, `draft` state, list, read; produce first Authoritative Offering Definition Context + stable Offering Reference.
5. **D5 — composition/relationships = EXCLUDE from BA-01.**
6. **D6 — pricing = include the optional opaque `list_price_reference` reference attribute ONLY;** never calculate/rate/discount/execute; never a numeric/computed field.
7. **D7 — lifecycle = establish in `draft` only;** no `draft → published`, no `published → retired`; approval-authority Pending Canonical Binding not to be silently solved.
8. **D8 — catalog tenant scope = OPTION A, PLATFORM-GLOBAL.** No `organization_id`; no tenant overlay; no segment-scoping; interim gate `require_platform_admin`; future tenant overlay + future canonical Catalog Governance Authority each deferred with a recorded trigger.

**This IRA does not reopen, reinterpret, or add to D1–D8.**

---

## 5. Strategic Enhancement Disposition (`CLAUDE.md §21.3`)

**(Established fact.)** `SER-001` (Strategic Enhancement Register) contains **no C-021, catalog, offering, or product/service `SE-XXX` entry** — confirmed by direct search. No Strategic Enhancement has ever been registered against C-021.

**Disposition recorded by this IRA: Strategic Enhancement Review is NOT APPLICABLE to C-021 BA-01** — there is no relevant registered enhancement to classify Implemented / Partially Implemented / Deferred / Not Applicable. This is the same "genuinely nothing registered" disposition, not a gap. Should a future C-021 increment (composition, publication, pricing execution) warrant a Strategic Enhancement entry, that is a future `SER-001` maintenance action, not a precondition for BA-01.

Adjacent entries reviewed and found not to require reclassification: none link to C-021 in `SER-001` itself.

---

## 6. Historical Screen Review (`CLAUDE.md §21.3`)

**(Established fact.)** `HISTORICAL-SCREEN-REALIZATION-MATRIX.md`'s classification table names no Offering, Catalog, Product, Pricing, or Plan screen concept. The one incidentally commercial item — **row 6, `06-admin-dashboard.html`, classified `RETIRE CONCEPT`** — is a historical vendor-console mock (CorpStage's own operator visibility into customer accounts, with a "manual approval + live price calculator" workflow). It is explicitly retired because *"the underlying manual-approve/price-calculator workflow conflicts with `COM-001`'s own actual Offering / Approval-as-fitness-to-publish model."*

**Disposition recorded by this IRA: no C-021 historical screen is to be realized.** The one commercial historical screen is a deliberately-retired concept whose workflow contradicts the LOCKED `COM-001` model. C-021's real experience follows `PE-001-C021`'s ERB/EX model, not the retired mock. This is the identical "genuinely nothing to realize, not a blocker" disposition `IRA-C132 §6`, `IRA-C066 §6b`, and `IRA-C114 §6b` each reached.

---

## 7. Executive Cognition Review (`CLAUDE.md §21.3`)

**(Established fact.)** `EXECUTIVE-COGNITION-REALIZATION-STRATEGY.md` never names C-021, offerings, or the catalog, and places no direct constraint on C-021.

**Disposition recorded by this IRA: Executive Cognition Review is NOT APPLICABLE to C-021 BA-01.** C-021 BA-01 delivers a Layer-1 administrative catalog surface (establish / list / read an Offering Definition, `PLATFORM_ADMIN`-operated), not a Sacred 12 executive-cognition surface. **(Inference, non-binding, carried forward not decided — §23.)** If a future capability ever surfaces an offering-portfolio view on an executive screen, `SD-001-054`/`056`/`057` would apply (consume-not-discover; no notification-styled noise; pair any count with a stated consequence) — not required for, and not a blocker to, BA-01.

**Reusable governance pattern:** `IRA-C132 §7` names the "charter off the owning constitutional spec" pattern; C-021 is *stronger* — it has both the owning constitutional spec (`COM-001`) **and** a dedicated Active Enterprise Experience Spec (`PE-001-C021`).

---

## 8. Business Object / Persistence Eligibility Analysis (`CMD-001 §26.3a`) + CBOR + BAR

**(Established fact — the applicable test, `CMD-001 §26.3a`, verbatim structure.)** A candidate is eligible for canonical registration if it satisfies **Step 1 (Independent Identity)** and at least one of **Step 2 (Cross-Experience Reference Test)** or **Step 3 (Governed Lifecycle)**.

**Applying the test to "Offering Definition," per the RO-authorized minimum scope D4 (establish / list / read, `draft` only):**

- **Step 1 — Independent Identity: SATISFIED.** `COM-001-001`/`-020` establish a `PREFIX-NNNNNN` identity that persists as the Authoritative Offering Definition Context beyond any single request. D4 explicitly authorizes `list`/`read` as distinct later actions against a previously-established record. It is not a value existing only for one request/response cycle.
- **Step 2 — Cross-Experience Reference Test: SATISFIED.** The Offering Reference is explicitly named as Consumed Context, retrieved *by identity*, by capabilities **other than** C-021's own producing BA: C-020 consumes it to anchor and shape a Subscription (`COM-001-011` — the Subscription Anchor is "consumed, never recomputed, from … the Offering"); `PE-001-C021 §2.10`/`ERB-C021-06` name C-024 (Billing) and C-025 (Contract) as downstream consumers of the Offering Reference. Per `CMD-001 §26.3a`, retrieval-by-identity from a separately-invoked later capability satisfies Step 2. **This is stronger than C-132's own Step 2 finding** (`IRA-C132 §8` found Step 2 "not satisfied today" for Notification — no other experience consumed it yet; for an Offering Definition, downstream consumption is the entire point of the capability, `PE-001-C021 §1.3`).
- **Step 3 — Governed Lifecycle: SATISFIED.** `COM-001-025` (Version Management) and `COM-001-020` describe a real `draft → published → retired` lifecycle with Retirement terminal and Historical Definitions retained in lineage ("never deletion"). A persisted `draft` state is later invalidated by a subsequent publication event. `PE-001-C021 §1.16`/`§1.24` require an Authoritative Context with retained Historical lineage.

**Composite finding: Step 1 (yes) + Step 2 (yes) + Step 3 (yes) → Offering Definition satisfies `CMD-001 §26.3a` and is ELIGIBLE for canonical CBOR registration.** All three steps pass (the test requires Step 1 and at least one of 2/3 — here all three hold).

**CBOR registration requirement (Assessment 4).** `COM-001-005` (Registration Precedes Implementation) and `COM-001-061` (an Offering Definition is a CBOR-registered Business Object once implemented), together with `CMD-001 §26.3`/`§26.4` and `CBOR-INDEX.md`'s Amendment Procedure, establish that **CBOR registration is required before implementation, via a dedicated ADR** (mirroring `ADR-019`'s registration of `CFG-000001` for WP-10). **This IRA does NOT perform that registration and does NOT create the ADR.** It records: *a CBOR registration ADR for the Offering Definition Business Object is a mandatory prerequisite to `TDS-C021` finalization / implementation authorization* — to be raised at TDS time or immediately after IRA acceptance, at Repository Owner discretion. The ADR would perform the actual `CMD-001 §26.4` registration (Business Object Identifier, Canonical Name, Owning Capability = C-021, Aggregate Root, Primary Data Category, etc.) and add the `CBOR-INDEX.md` row.

**BAR registration requirement (Assessment 5).** `COM-001-060` requires the BA-01 Business Activity ("Establish / Manage Offering Definition") to be **BAR-registered before implementation**. Same disposition: **this IRA records the requirement; it does not perform the registration.** BAR registration is a prerequisite to be satisfied at charter/TDS time, consistent with `COM-001-005`.

**STOP-and-report finding (`CLAUDE.md §18`/`§19.4`), independent of the above.** A new `offering`-shaped database table is, regardless of its `§26.3a` outcome, unambiguously the class of artifact `CLAUDE.md §18`/`§19.4` requires be justified via schema-shape STOP-and-report before any migration runs. **This IRA does not resolve it and does not design the schema** — per every recent precedent (`TDS-C023-A §19`, `TDS-016`, `TDS-C132 §22`), this is satisfied by the future `TDS-C021`'s own schema-decision section (see §13, §20 Assessment 3).

---

## 9. Candidate First Business Activity — Definition and Scope

**(Recorded per `ROD-C021 §L` — a governance definition for a future charter, not itself a charter.)**

**BA-01 name:** Establish / Manage Offering Definition.

**Purpose:** Create the enterprise's authoritative definition of a standalone Atomic Offering that may subsequently be referenced by downstream commercial capabilities.

**In scope, per D4 (Option A + D):**
- **Establish** an Atomic Offering Definition: canonical identity (`PREFIX-NNNNNN`, `COM-001-001`); canonical name; **Product / Service classification** (`COM-001-021`); opaque **category reference** (`COM-001-024`); optional opaque **`list_price_reference`** (`COM-001-020`, D6 — reference attribute only); current offering **state = `draft`** (`COM-001-020`).
- **List** Offering Definitions (`PLATFORM_ADMIN`, platform-global — no tenant filter, D8).
- **Read** one Offering Definition by id.
- Produce the first **Authoritative Offering Definition Context** (`COM-001-002`) and a stable **Offering Reference** (`ERB-C021-06`).

**Explicitly excluded (per D3/D5/D6/D7/D8 and `ROD-C021 §M`):** composition; relationships; publication (`draft → published`); retirement (`published → retired`); revision of a published offering; pricing computation / rating / discounting / execution; availability determination; Subscription; Customer / Account; segment-scoping; Entitlement; Feature Catalog; Billing; Contract; tenant-specific overlays; per-tenant catalog; catalog taxonomy governance authority; offering approval authority; retirement notice policy; order / inventory / fulfillment / provisioning / usage / metering / taxation; discovery / overlap detection (`EX-C021-13`); future-dated transitions; external product integrations; marketplace / CRM / ERP functionality.

**Trigger mechanism (finding).** Direct, synchronous, authenticated `PLATFORM_ADMIN` action against C-021's own host — `POST` to a C-021 router, in C-021's own transaction. **No cross-service write path, no write-fan-in, no event bus.** This is materially simpler than C-132's own trigger analysis (`IRA-C132 §17` had to solve write-fan-in from many services; C-021 has none).

**Deferred, disclosed (per D7/D8):** publication/retirement transitions; the approval-authority Pending Canonical Binding (`COM-001-026`); a canonical Catalog Governance Authority; a future tenant-scoped catalog overlay. Any `TDS-C021`/charter describing BA-01 must carry an explicit, dated deferral note for each, mirroring `IRA-C023`'s Decision 3/4 deferral-disclosure convention.

---

## 10. DS-001 Compliance (Assessment 16)

**(Finding.)** `PE-001-C021` engineers the C-021 experience to the `PE-001-C005` Gold-Standard discipline; its EXs (Establish Offering Context, Understand Offering Definition, Frame Offering Definition Intent, Shape & Assess) describe **standard enterprise CRUD-plus-lifecycle screens** — a list/table surface, a detail surface, a create/edit form surface. These are exactly the screen archetypes `DS-001` and the `IMP-001 §10` frontend standard already govern with existing components; the WP-17 `entitlement-license` feature is a working in-repo realization of the same archetype set.

**Reuse assessment:** the DS-001 table, form-field, detail-panel, status-chip (for the four-value offering `state` model, of which BA-01 uses only `draft`), and page-shell primitives are directly reusable. No C-021-specific component is required by BA-01.

**Gap check:** BA-01 introduces no new visual element `DS-001` does not already define. **No `CLAUDE.md §19.1` STOP-and-report is warranted on the DS-001 dimension** — but a routine DS-001 conformance pass (which specific components realize the list / detail / create surfaces) is ordinary TDS/frontend-engineering work, to be recorded in `TDS-C021`. `[FUTURE TDS QUESTION]`: exact component selection per screen.

---

## 11. Platform-Global Scope, Ownership & Security Model (Assessments 7, 23; `ROD-C021 §K`/`§O`)

**This section deliberately does NOT apply C-132's tenant-scoped authorization semantics.** `IRA-C132 §11`/`§12` reasoned from a tenant-scoped Notification record (`organization_id`, `require_matching_tenant_or_platform_admin`, anti-enumeration 404s). **D8 makes the C-021 catalog platform-global** — the correct precedent is different.

**(Established fact + `[RO DECISION]` D8.)**
- The Offering Definition carries **no `organization_id` tenant anchor**. There is **no tenant boundary** on the object — the catalog is one enterprise-wide catalog (`COM-001 §1` frames it as what "the enterprise" offers, singular).
- The ownership/authority boundary is therefore **not tenant isolation** — it is **platform-administrative authority**. The interim gate is **`require_platform_admin`** on every mutating and (per D4's platform-global list/read) reading route.
- **Precedent (verified against actual repo, §3.3):** `C-003` Roles — `roles` has no `organization_id`; every `/roles` mutation is `require_platform_admin`-gated; `/roles` is tenant-middleware-exempt (`X-Tenant-ID` not required). **C-021's routes should follow the same shape** — tenant-middleware-exempt, `require_platform_admin`-gated. `[FUTURE TDS QUESTION]`: confirm the exact middleware-exemption registration and whether read (`GET`) is also `require_platform_admin` or a broader authenticated-internal role (D4 as written implies `PLATFORM_ADMIN` for the whole BA-01 surface).

**Why tenant isolation is not the BA-01 ownership boundary (explicit, per the RO's instruction).** `CLAUDE.md §21.4`'s Mandatory Tenant-Isolation Test Checklist applies "for every new endpoint whose underlying data model carries an organization/tenant boundary." **The C-021 Offering Definition data model, per D8, carries no such boundary.** The checklist's tenant-seeding / cross-tenant-denial / foreign-tenant-identifier probes are therefore **structurally not applicable** to BA-01 — not skipped, not deferred, but inapplicable by the object's decided design, exactly as they are inapplicable to `/roles`. **The substitute assurance BA-01's test suite SHALL provide instead:** (a) a caller *without* `PLATFORM_ADMIN` is denied establish/list/read; (b) a caller *with* `PLATFORM_ADMIN` succeeds; (c) no `organization_id` / tenant column exists on the table (a schema-level assertion). This substitution SHALL be explicitly recorded in the BA-01 charter and `TDS-C021`, per `CLAUDE.md §19.4`'s STOP-and-report discipline for a scope decision — it is disclosed here, not silently assumed.

**Deferred with recorded trigger (D8):** a future tenant-scoped catalog overlay (trigger: a chartered capability genuinely requiring per-tenant catalog curation or segment-scoped offerings); a canonical Catalog Governance Authority replacing `require_platform_admin` (trigger: implementation need for offering approval, taxonomy governance, or retirement-notice policy — i.e. anything past `draft`, per D7).

---

## 12. Authority / Accountability (Assessment 8)

**(Finding.)** `PE-001-C021` provides **no canonical approval/commit authority** for establishing an Offering Definition — `§1.5` records offering approval authority as **Pending Canonical Binding**; `§1.11` states personas "do not define authorization roles"; `§1.9` names only the generic `C-002 / URA-001` Access Evaluation Outcome mechanism.

- BA-01's interim authorization gate is **`require_platform_admin`** (D8, §11).
- **This is the established platform pattern for a platform-global business object** (`C-003` Roles, WP-02) — it is **not** the tenant-scoped `require_matching_tenant_or_platform_admin` used for C-041 Configuration or C-132 Notifications, because D8 makes the catalog platform-global.
- **No dedicated Approval / Commit Authority is needed for BA-01**, because BA-01 establishes an offering only in `draft` (D7) — the point at which an approval authority would matter (`draft → published`, `COM-001-026`) is explicitly out of scope. Keeping BA-01 to `draft` is precisely what avoids loading the Pending Canonical Binding.
- **Audit / accountability:** `record_audit()` + `publish_event()` on establish (universal pattern, §3.4); actor = the `PLATFORM_ADMIN` caller's `person_id`; resource = the Offering Definition id; `SD-002 §6` Evidence applies per `COM-001-063`. **No RO decision required for the audit dimension.**
- `[FUTURE IMPLEMENTATION QUESTION]` A canonical **Catalog Governance Authority** (who may approve/publish/retire, govern taxonomy, set retirement-notice policy) is deferred with a recorded trigger, mirroring `IRA-C023 §21.12`'s Decision-3 deferral discipline.

---

## 13. Lifecycle, Temporal & Schema/TDS Boundary (Assessments 9, 13; `CLAUDE.md §13` schema/TDS boundary)

**(Finding, per D7.)**
- **Minimum lifecycle for BA-01:** established → (persists in `draft`). BA-01 implements **no** transition out of `draft`. `draft → published` and `published → retired` (`COM-001-025`) are future increments.
- **Temporal semantics:** `COM-001-025` requires Historical Definitions retained in lineage on version change ("never deletion"). BA-01 does not perform version changes, so the lineage mechanism (`supersedes_id`-style, mirroring `roles.supersedes_id`) is **designed for but not exercised** by BA-01. `[FUTURE TDS QUESTION]`: whether BA-01's table declares the `version`/`supersedes_id`/`effective_from`/`effective_to` columns up front (recommended — mirrors `roles` and the `c023_*` "declare the full lifecycle, write a subset" precedent) or adds them in the publication increment.
- **`state` column:** `[FUTURE TDS QUESTION]` — whether `state` is CHECK-constrained to the full closed set `{draft, published, retired}` (recommended for schema correctness, mirroring `c132_notification.status`'s CHECK) even though BA-01 only ever writes `draft`.
- **Retention:** an Offering Definition is a permanent commercial record (`COM-001-025` "never deletion"); no expiry. `[FUTURE TDS QUESTION]`: alignment with any general retention floor.

**Schema / TDS boundary — explicitly not crossed by this IRA.** This IRA does **not** design the schema and does **not** create a `TDS-C021`. The following are all marked `[FUTURE TDS QUESTION]` for a finalized `TDS-C021` with its own `CLAUDE.md §18`/`§19.4` schema-shape STOP-and-report:
1. Exact table name.
2. Full column set and types.
3. Whether `category` and `list_price_reference` are opaque `String` reference columns (recommended — mirrors `c132_notification.source_type`/`source_id` opaque non-FK citation) or FKs to a governed table (disfavoured — taxonomy authority is Pending Canonical Binding, D6).
4. `state` CHECK-constraint set.
5. Identity generation (`PREFIX-NNNNNN` sequence mechanism).
6. Index set.
7. Version/lineage columns.
8. Natural-key / uniqueness constraint (e.g. on canonical name) — bears on idempotency (§14).
9. The service that owns the table (§17).

---

## 14. Transaction / Idempotency (Assessments 10, 11)

**(Finding.)**
- **Transaction semantics:** BA-01 establish is a single-row insert in C-021's own host transaction, with the standard flush/rollback discipline every closed WP demonstrates (`EntitlementLicenseEstablishmentService` is the nearest in-repo shape). No distributed transaction, no cross-service write, no saga. **No RO decision required.**
- **Idempotency:** `[FUTURE IMPLEMENTATION QUESTION]` — whether establish needs duplicate-suppression (e.g. a natural key on canonical name, or a client idempotency token). This repository's precedent (`TD-141`-class findings, `TD-152`'s disposition for WP-14 BA-05) treats idempotency-mechanism selection as a routine implementation-time choice **not requiring a Repository Owner decision**, unless a specific natural key is later found to carry a genuine concurrency risk. Recorded as a TDS/implementation-time item, not a blocker.

---

## 15. Audit (Assessment 12)

**(Finding, universal platform precedent.)** BA-01's establish action SHALL call `record_audit()` / `publish_event()` exactly as every other Business Activity does (§3.4). `COM-001-063` confirms `SD-002 §6` Evidence applies to Offering Definition transitions. This is the standard cross-cutting pattern, structurally distinct from the Offering Definition record itself. **No RO decision required for this dimension.** `[FUTURE TDS QUESTION]`: the exact audit action name and evidence payload shape.

---

## 16. Event / Dependency & Cross-Capability Implications (Assessments 21, 22, 24, 25)

**(Established fact.)**
- **Infrastructure dependency (Assessment 21):** none. No live event bus exists (`Backend/Shared/Events` abstract, `TD-151`); BA-01 needs none — an Offering Definition is consumed by reference (read by identity when a downstream capability needs it), not delivered through a broker. BA-01 is implementable with **one additive table + one router in an existing service, zero new infrastructure**.
- **Cross-capability dependencies (Assessment 22):**

| Capability | BA-01 classification | Basis |
|---|---|---|
| C-004 Organization | NOT REQUIRED | D8 platform-global — no `organization_id` |
| C-020 Subscription Management | NOT REQUIRED (C-021 is its upstream producer; C-020 unchartered) | D1 |
| C-022 Customer & Account Management | NOT REQUIRED (segment-scoping excluded; C-022 unchartered) | D2 |
| C-023 Licensing & Entitlement | NOT REQUIRED ("No direct dependency") | D3 |
| C-003 Approval Authority (WP-02/WP-18) | NOT REQUIRED for BA-01 (interim `require_platform_admin`); canonical Catalog Governance Authority deferred | D7/D8 |
| C-040 Tenant Administration / tenant infra | NOT REQUIRED for BA-01 (platform-global); future tenant overlay deferred | D8 |
| Audit infra (`record_audit`/`publish_event`) | AVAILABLE — reuse | §3.4 |
| Event / broker infra | NOT REQUIRED | §3.4 |
| D-002 service host | **REQUIRES RO DECISION** at IRA/TDS stage | §17 |

- **C-020 / C-022 / C-023 boundary compliance (Assessment 24):** BA-01 as scoped (D1–D5) models **only** the Offering Definition — no Subscription, no Customer/Account, no Entitlement/Feature. Each boundary is `CONFIRMED/SETTLED` by the LOCKED/Active specifications (`COM-001 §2`/`§5`/`§6`, `PE-001-C021 §1.5`/`§2.10`, `PE-001-C023 §1.5`) and by RO decisions D1/D2/D3. **No boundary violation is introduced.**
- **C-023 Decision 3 preservation (Assessment 25):** **preserved untouched.** `IRA-C023 §21.12` deferred Decision 3 (the governance-authority mechanism for adding a global entitlement type) as Option A — *within C-023's own domain*. `PE-001-C021 §1.5` places entitlement definition / feature availability in C-023, not C-021; `PE-001-C021 §2.10` records C-021 ↔ C-023 as "No direct dependency." C-023 Decision 3's own recorded trigger ("implementation need … for another formally chartered capability that requires creation, modification, or governance of global Entitlement Types/Feature definitions") is **not fired** by C-021 BA-01, because BA-01 (D3/D4/§9) creates, modifies, and governs **no** entitlement type or feature definition. This IRA modifies **no** C-023 / WP-17 artifact and **no** C-023 Decision. **Disclosure:** a *future* C-021 increment adding an "entitlement types conferred by this offering" cross-reference would fire C-023 Decision 3's trigger — **BA-01 as decided does not.**

---

## 17. Service Hosting (Assessment 20; `ROD-C021 §P`)

**(Finding — status: 🔴 REQUIRES RO DECISION, but materially less complex than C-132's.)**

- **(Established fact.)** The five physical services are `AuthService`, `AIService`, `IngestionService`, `ReportingService`, `TenantService`. **No D-002 / commercial service exists.** No logical "Catalog Service" or "Commercial Service" is named in `Master_Technical_Architecture.md`'s service catalog.
- **(Precedent.)** `ADR-036` established the modular-monolith posture — a new dedicated service is disfavoured in the current phase; the adjacent D-002 capability **C-023 is hosted in `AuthService`** (`c023_license_context`, `c023_entitlement_context`).
- **Candidate hosts:**
  - **`AuthService`** — co-location with C-023 (the only other D-002 capability with a physical footprint), consistent with `ADR-036`'s modular-monolith trend, zero new-service STOP-and-report. The `C-003` Roles platform-global precedent (§3.3) also physically lives in `AuthService`, so the platform-global-object pattern C-021 would follow is already resident there.
  - **A new `CommercialService`** — cleaner single-owner boundary for the whole D-002 domain, but triggers a `CLAUDE.md §18`/`§19.4` new-service-boundary STOP-and-report and runs against the modular-monolith preference; disproportionate for a single additive table.
- **C-021 has NO write-fan-in complication.** `IRA-C132 §17`'s blocking novelty was that many unrelated services' transactions had to cause a Notification write with no cross-service DB access and no event bus. **C-021's Offering Definition is established by one direct, authenticated `PLATFORM_ADMIN` action against C-021's own host** — there is no second writer, so `CLAUDE.md §8`'s "never access another service's database" rule is not stressed and no write-fan-in mechanism decision is needed.
- **Classification:**
  - **DECIDED** — no cross-service database access regardless of host (`CLAUDE.md §8`); `TenantService` is not a viable host (`ADR-036 §Decision(5)` — mocked scaffolding).
  - **🔴 RO DECISION REQUIRED** — which service hosts the C-021 Offering Definition persistence: `AuthService` (recommended by precedent) or a new `CommercialService` (subject to its own STOP-and-report).
  - **IMPLEMENTATION-TIME** — exact schema shape, once hosting is resolved (§13).

**This IRA does not select a host.** Per the `TDS-013 §26a` / `RO-DEC-WP14-BA05-03` precedent (and `TDS-C132 §6.5`'s own H-1 decision), the hosting question should be resolved via a dedicated Repository Owner Decision **during `TDS-C021` drafting** — `TDS-C021` drafting may begin; `TDS-C021` may not be finalized, and no schema/migration may be authorized, until this decision is obtained. **Service-hosting status: REQUIRES RO DECISION (CONDITIONAL — a clear recommended default of `AuthService` exists on precedent, so this is not an open-ended blocker).**

---

## 18. API / Frontend Implications (Assessments 15, 12-frontend-readiness; `ROD-C021` §L)

**(Finding.)**
- **Backend:** one router on the C-021 host exposing `POST ""` (establish, 201), `GET ""` (list, platform-global — no tenant filter), `GET "/{id}"` (read) — mirroring `entitlement_license.py`'s shape (Pydantic request/response schemas, DI-composed service, repository). Every route `require_platform_admin`-gated; router tenant-middleware-exempt (§11, `/roles` precedent). `[FUTURE TDS QUESTION]`: exact route prefix (`/offerings` / `/catalog/offerings` / under `/platform-admin/...`).
- **Frontend — establish + list + read, NOT backend-only.** D4 explicitly includes `list` and `read`, and C-021 (as a future WP-20) falls under `CLAUDE.md §20` (Enterprise Experience Standard, WP-08 onward) and `§21.3`'s vertical-slice lifecycle — **a demonstrable operable screen is required unless the WP-20 charter explicitly designates BA-01 backend-only via `§19.4` STOP-and-report.** This IRA's determination: **BA-01 should deliver a frontend** — a catalog list surface + a detail (read) surface + a create (establish) form, `PLATFORM_ADMIN`-operated, homed under the existing `subscriptions` nav parent (`admin-navigation.ts`, §3.2), realized with the WP-17 `entitlement-license` feature-folder pattern and existing DS-001 primitives (§10). No new DS-001 component/token/pattern is required — no `CLAUDE.md §19.1` STOP-and-report on this dimension.
- **Frontend readiness (Assessment 15):** the panel/shell/table/form primitives and the per-capability feature-folder pattern all exist and are certified in-repo (WP-17). Readiness is **GREEN on the frontend dimension** — ordinary engineering, no missing capability.

---

## 19. Implementation Feasibility (Assessment 26)

**(Finding, consolidating §3, §16, §17.)** Technically feasible with **no missing infrastructure** for the RO-authorized minimum scope:
- trigger mechanism (direct synchronous `PLATFORM_ADMIN` establish) — trivial, single-writer, no fan-in, no bus;
- persistence — one additive table, `CLAUDE.md §18` schema-shape STOP-and-report deferred to `TDS-C021` (standard);
- authority — `require_platform_admin`, an existing certified pattern (`C-003` Roles);
- audit — existing `record_audit()`/`publish_event()` pattern;
- DS-001 — existing primitives, no new component;
- frontend — existing feature-folder + component pattern (WP-17).

**The one substantive open item between this IRA and a fully-scopable `TDS-C021` is the service-hosting decision (§17)** — and even that has a clear recommended default (`AuthService`) on precedent, making it a decision to *confirm* rather than an open architectural gap. **Two mandatory pre-implementation registrations** (CBOR ADR for the Business Object; BAR registration for the BA) are recorded as prerequisites (§8) — neither blocks `TDS-C021` drafting.

---

## 20. The 28-Point Readiness Assessment Matrix

Every assessment the Repository Owner's instruction enumerated, with its finding and pointer:

| # | Assessment | Finding | Where |
|---|---|---|---|
| 1 | Capability activation | C-021 is `CAP-001`-Active (line 75); owning spec `COM-001` LOCKED; `PE-001-C021` v1.1 Active. Activation substrate complete — stronger than any recently-chartered capability. | §2 |
| 2 | BA boundary | BA-01 = "Establish / Manage Offering Definition", scope per D4 (Option A + D); exclusions per D3/D5/D6/D7/D8. Coherent, bounded, RO-authorized. | §9 |
| 3 | BO eligibility (`CMD-001 §26.3a`) | **ELIGIBLE** — Step 1 (Independent Identity) ✓ + Step 2 (Cross-Experience Reference — C-020/C-024/C-025 consume the Offering Reference by identity) ✓ + Step 3 (Governed Lifecycle `draft→published→retired`) ✓. | §8 |
| 4 | CBOR requirement | **REQUIRED before implementation**, via a dedicated ADR (mirrors `ADR-019`). This IRA records the requirement; does **not** create the ADR. Prerequisite to `TDS-C021` finalization. | §8 |
| 5 | BAR requirement | **REQUIRED before implementation** (`COM-001-060`). Recorded; not performed. Prerequisite at charter/TDS time. | §8 |
| 6 | Offering identity | `PREFIX-NNNNNN` (`COM-001-001`), persisted as the Authoritative Offering Definition Context. Generation mechanism = `[FUTURE TDS QUESTION]`. | §8, §13 |
| 7 | Platform-global scope | **CONFIRMED (D8)** — no `organization_id`; one enterprise-wide catalog; precedent `C-003` Roles (verified in repo). | §11 |
| 8 | Authority model | Interim `require_platform_admin` on all routes; router tenant-middleware-exempt (`/roles` precedent). No dedicated Approval Authority needed (BA-01 is `draft`-only). Canonical Catalog Governance Authority deferred with trigger. | §11, §12 |
| 9 | Lifecycle | BA-01 establishes `draft` only; no transitions. `state` CHECK set + lineage columns = `[FUTURE TDS QUESTION]`. | §13 |
| 10 | Transaction semantics | Single-row insert in C-021's own host transaction; standard flush/rollback. No RO decision needed. | §14 |
| 11 | Idempotency | `[FUTURE IMPLEMENTATION QUESTION]` — routine implementation-time choice (`TD-152` precedent); no RO decision needed unless a natural key carries concurrency risk. | §14 |
| 12 | Audit | `record_audit()` + `publish_event()` on establish (universal pattern); `SD-002 §6` Evidence applies (`COM-001-063`). No RO decision needed. | §15 |
| 13 | Temporal semantics | Historical Definitions retained in lineage on version change (`COM-001-025`, "never deletion") — designed-for, not exercised by BA-01. Permanent record, no expiry. | §13 |
| 14 | Existing asset reuse | Backend: zero catalog footprint (reuse audit infra + `C-003` platform-global pattern). Frontend: zero catalog footprint (reuse WP-17 `entitlement-license` feature pattern + DS-001 primitives). | §3, §10, §18 |
| 15 | Frontend readiness | **GREEN** — panel/table/form primitives + per-capability feature-folder pattern exist and are certified (WP-17). Ordinary engineering. | §18 |
| 16 | DS-001 conformance | No new component/token/pattern required; standard list/detail/form archetypes. Component selection per screen = `[FUTURE TDS QUESTION]`. No `§19.1` STOP-and-report. | §10 |
| 17 | Historical screen review | **NOT APPLICABLE** — no C-021 historical screen; the one commercial mock (`06-admin-dashboard.html`) is `RETIRE CONCEPT`, its workflow conflicts with LOCKED `COM-001`. | §6 |
| 18 | Executive cognition review | **NOT APPLICABLE** — `EXECUTIVE-COGNITION-REALIZATION-STRATEGY.md` does not name C-021; BA-01 is a Layer-1 admin surface, not Sacred 12. | §7 |
| 19 | Strategic Enhancement Register review | **NOT APPLICABLE** — no C-021 / catalog / offering `SE-XXX` entry exists in `SER-001` (confirmed by direct search). Nothing to classify. | §5 |
| 20 | Service-hosting requirement | **🔴 REQUIRES RO DECISION** (`AuthService` recommended on precedent, or new `CommercialService` subject to its own STOP-and-report). Resolve during `TDS-C021` drafting (`TDS-013 §26a` precedent). No write-fan-in complication (unlike C-132). | §17 |
| 21 | Infrastructure dependency | **NONE** — no event bus needed; one additive table + router in an existing service. | §16 |
| 22 | Cross-capability dependencies | None required for BA-01 (C-004/C-020/C-022/C-023/C-040 all NOT REQUIRED). Audit infra reused. | §16 |
| 23 | Tenant isolation implications | `CLAUDE.md §21.4` checklist **structurally not applicable** — the object carries no tenant boundary by decided design (D8), same as `/roles`. Substitute assurance: `PLATFORM_ADMIN`-required tests + a schema assertion that no `organization_id` column exists; to be recorded in the charter/TDS per `§19.4`. | §11 |
| 24 | C-020/C-022/C-023 boundary compliance | **COMPLIANT** — BA-01 models only the Offering Definition; each boundary `CONFIRMED/SETTLED` by LOCKED/Active specs + D1/D2/D3. No violation introduced. | §16 |
| 25 | C-023 Decision 3 preservation | **PRESERVED UNTOUCHED** — BA-01 creates/modifies/governs no entitlement type or feature definition; C-023 Decision 3's trigger is not fired; no C-023/WP-17 artifact modified. | §16 |
| 26 | Implementation feasibility | Feasible with no missing infrastructure for the authorized minimum scope; the one open item is the service-hosting confirmation (§17). | §19 |
| 27 | Gate readiness | 5 of 7 gates PASS, 1 CONDITIONAL, 1 FAIL (Gate 6 — the single service-hosting item). See §21. | §21 |
| 28 | Governance completeness | ROD-C021 records D1–D8; this IRA runs the full readiness assessment; the remaining governed steps (Strategic Enhancement / Historical Screen / Executive Cognition reviews) are performed above (§5–§7) and each returns NOT APPLICABLE with basis. Two pre-implementation registrations (CBOR ADR, BAR) recorded as prerequisites. No governance step is skipped or assumed. | §5–§8, §23 |

---

## 21. Gate Assessment (mirroring `IRA-C040`'s / `IRA-C132`'s seven-gate framework, for comparability)

| Gate | Result |
|---|---|
| Gate 1 — Business Function | ✅ PASS — unambiguous Business Intent (`CAP-001` line 75); `COM-001 §6` governs it with material specificity; `PE-001-C021` v1.1 Active adds a full Enterprise Experience model. |
| Gate 2 — Architecture | ✅ PASS — `COM-001` is LOCKED (CR-3.0); `PE-001-C021` is Active/Gold-Standard; `DS-001` covers the presentation archetypes. No architecture gap. |
| Gate 3 — Data Model | 🟡 CONDITIONAL PASS — `CMD-001 §26.3a` eligibility resolved affirmatively (§8, all three steps); exact schema shape is ordinary TDS-stage work with a mandatory `§18` STOP-and-report; CBOR ADR + BAR registration are recorded prerequisites. |
| Gate 4 — Authority / Security | ✅ PASS — platform-global authority model (`require_platform_admin`) is an existing certified pattern (`C-003` Roles); no dedicated Approval Authority needed for a `draft`-only BA; tenant-isolation checklist inapplicability is disclosed and substituted, not skipped. |
| Gate 5 — Business Activities | ✅ PASS — coherent, narrowly-scoped, RO-authorized BA-01 (§9), with explicit disclosed exclusions (composition, relationships, publication, retirement, pricing execution, tenant overlay). |
| Gate 6 — Governance | 🔴 FAIL (single item) — service hosting is unresolved (§17). Unlike `IRA-C132`'s own Gate 6, there is **no** second unresolved item (no write-fan-in mechanism to decide) and a clear recommended default (`AuthService`) exists on precedent — a decision to confirm, not an open architectural question. |
| Gate 7 — Implementation | 🟡 CONDITIONAL PASS — no missing infrastructure for the authorized minimum scope (§19); full implementation planning waits on Gate 6's hosting confirmation. |

**5 of 7 gates PASS, 1 CONDITIONAL, 1 FAIL (Gate 6 — a single, precisely-named, low-risk, precedent-resolvable item).** This is at least as ready as `IRA-C132`'s own AMBER finding and arguably readier — C-132 had two Gate-6 items (host + write-fan-in) and a weaker Step-2 BO finding; C-021 has one Gate-6 item, a clear recommended host, and a three-of-three `§26.3a` pass.

---

## 22. Readiness Decision (`GREEN` / `AMBER` / `RED`)

**C-021 / candidate BA-01 is 🟡 AMBER — READY FOR TECHNICAL DESIGN PREPARATION, NOT YET READY FOR TDS FINALIZATION OR IMPLEMENTATION AUTHORIZATION.**

**Not RED:** no capability-defeating blocker. The governance substrate is unusually complete (LOCKED `COM-001` + Active Gold-Standard `PE-001-C021`); the RO-authorized minimum scope (D4) is coherent, bounded, and technically feasible with existing infrastructure; `CMD-001 §26.3a` resolves affirmatively on all three steps; the platform-global authority model has a certified in-repo precedent (`C-003` Roles); DS-001 conformance, audit, transaction semantics, and the frontend all follow proven, low-risk patterns; C-020/C-022/C-023 boundary compliance is `CONFIRMED/SETTLED` and C-023 Decision 3 is preserved untouched.

**Not GREEN:** one genuine, disclosed, precisely-named Repository Owner decision remains outstanding — **service hosting** (`AuthService` vs. a new `CommercialService`, §17) — and this repository's own discipline (`CLAUDE.md §18`) prohibits proceeding to a finalized schema/migration without it. In addition, **two mandatory pre-implementation registrations are recorded as prerequisites** — a CBOR registration ADR for the Offering Definition Business Object (§8, Assessment 4) and BAR registration for BA-01 (§8, Assessment 5) — neither of which this IRA performs.

**May TDS proceed?** **`TDS-C021` drafting MAY begin** — it should incorporate, as a first-order task, a dedicated Repository Owner Decision resolving §17's hosting question (mirroring `TDS-013 §26a` / `RO-DEC-WP14-BA05-03` and `TDS-C132 §6.5`'s own H-1), and it must contain the `CLAUDE.md §18`/`§19.4` schema-shape STOP-and-report for the new `offering`-shaped table. **`TDS-C021` may NOT be finalized, and no schema, migration, model, repository, service, router, or test may be authorized or created, until (a) the service-hosting Repository Owner decision is obtained and (b) the CBOR registration ADR and BAR registration are completed.**

**Is any additional Repository Owner decision required?** **Yes — exactly one, precisely named:** the C-021 service-hosting decision (§17). Every other dimension investigated (§§10–16, 18–20) is either already governed by an existing binding rule/precedent or is an explicitly-identified ordinary TDS-time / implementation-time choice this IRA has flagged rather than silently decided.

**IRA acceptance is NOT granted by this document** — per `CLAUDE.md §19.1` and the `IRA-C132` / `IRA-C066` / `IRA-C114` / `IRA-C023` precedent, acceptance is a separate, future Repository Owner review.

---

## 23. Explicit Statement of What Remains Unresolved (not decided by this IRA)

- **RO DECISION REQUIRED** — C-021 service hosting: `AuthService` (recommended on `ADR-036` + C-023 co-location + `C-003` precedent) vs. a new `CommercialService` (subject to its own `CLAUDE.md §18`/`§19.4` STOP-and-report). **This is the sole blocking item (§17).**
- **MANDATORY PRE-IMPLEMENTATION REGISTRATIONS (recorded, not performed here)** — (a) a CBOR registration ADR for the Offering Definition Business Object (`COM-001-005`/`-061`, `CMD-001 §26.4`); (b) BAR registration for BA-01 (`COM-001-060`). Neither blocks `TDS-C021` drafting; both block `TDS-C021` finalization / implementation authorization (§8).
- **`[FUTURE TDS QUESTION]` — all schema-shape decisions** — table name, column set/types, opaque-reference-vs-FK for `category` / `list_price_reference`, `state` CHECK set, identity-generation mechanism, index set, version/lineage columns, natural-key/uniqueness constraint, and the `§18`/`§19.4` schema STOP-and-report (§13).
- **`[FUTURE TDS QUESTION]` — DS-001 component selection per screen** (§10); exact route prefix and whether `GET` is `require_platform_admin` or a broader authenticated role (§11, §18).
- **`[FUTURE IMPLEMENTATION QUESTION]` — idempotency mechanism** for establish (§14) — routine, no RO decision unless a concurrency risk surfaces.
- **DEFERRED with recorded trigger (per D7/D8, `ROD-C021 §K`)** — `draft → published` and `published → retired` transitions; the offering approval-authority Pending Canonical Binding (`COM-001-026`); a canonical Catalog Governance Authority; a future tenant-scoped catalog overlay; catalog taxonomy governance authority (`COM-001-024`). None blocks BA-01; each must be carried as an explicit dated deferral note in `TDS-C021` and the charter.
- **UNRESOLVED, non-blocking — doc-sync debt** — `PE-001-C021` masthead reads "Primary Specification Reference: SD-001"; the true Primary Specification is `COM-001` (`CAP-001` line 75). Same class as the `PE-001-C040` masthead debt `CAP-001` line 17 flags. Not corrected by this IRA (no locked/spec document is modified here); to be reconciled by a future `PE-001` maintenance pass.
- **UNRESOLVED, non-blocking — inference only (§7)** — whether/how a future offering-portfolio view is ever surfaced on a Sacred 12 executive screen. Not required for, and not a blocker to, BA-01's Layer-1 admin surface.

---

## 24. Change Control

**Files created by the pass this IRA belongs to:** this document — `architecture/05-Implementation/IRA-C021_Product_and_Service_Catalog_Implementation_Readiness_Assessment.md` — and `architecture/06-Reviews/ROD-C021-Product-and-Service-Catalog-Capability-Boundary-and-Minimum-Scope.md`.

**Files read for cross-reference, not modified:** `CAP-001` (line 75, D-002 rows, line 17), `COM-001` (§2, §4, §5, §6 [`COM-001-020…026`], §7, §10, Freeze Statement), `PE-001-C021_Product_and_Service_Catalog.docx` (v1.1 — §1.2/§1.3/§1.5/§1.9/§1.11/§1.16/§1.21/§1.22/§1.24/§2.10, ERB/EX list), `PE-001-C023 §1.5`, `IRA-C023` (§16, §21 — Decision 3), `TDS-C023` / `TDS-C023-A` (read only), `CMD-001 §26.3a`/`§26.3`/`§26.4`, `CBOR-INDEX.md`, `SER-001` (no C-021 entry), `HISTORICAL-SCREEN-REALIZATION-MATRIX.md` (row 6), `EXECUTIVE-COGNITION-REALIZATION-STRATEGY.md`, `ADR-036`, `ADR-019`, `ROD-C132`, `IRA-C132`, `TDS-C132` (§6.5), `WP-19` charter, `TDS-013 §26a`, `TECH-DEBT.md` (`TD-151`, `TD-152`), `WPR-001`, `WP-REG-001`, `Backend/Services/AuthService/models/role.py`, `routers/role.py`, `middleware/tenant.py`, `models/__init__.py`, `source/frontend/src/config/admin-navigation.ts`, and the `features/entitlement-license/` frontend files named in §3.

**Not modified:** any LOCKED constitutional document (`COM-001`, `PE-001`, `PE-001-C021`, `CAP-001`, `SD-001`, `SD-002`, `SD-003`, `URA-001`, `CMD-001`, `GRC-001`, `PLT-001`, `RTA-001`, `EIA-001`, `DS-001`, `ARCH-000`, `ADR-002`/`003`/`016`/`023`/`036`); any C-023 / WP-17 artifact or C-023 Decision (1–6); `CBOR-INDEX.md`; `SER-001`; `HISTORICAL-SCREEN-REALIZATION-MATRIX.md`; `EXECUTIVE-COGNITION-REALIZATION-STRATEGY.md`; `WPR-001`; `WP-REG-001`; `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md`; any `Backend/` or `source/frontend/` file, migration, or test. **No minimal additive status registration was performed** — `WP-20` is not registered, and no `WPR-001 §3` Maintenance-Rule trigger has fired (a WP number is assigned only when a Work Package is properly authorized, which has not occurred). No implementation of any kind was performed. **No IRA acceptance is granted by this document.** Nothing was staged, committed, or pushed.

*End of IRA-C021.*
