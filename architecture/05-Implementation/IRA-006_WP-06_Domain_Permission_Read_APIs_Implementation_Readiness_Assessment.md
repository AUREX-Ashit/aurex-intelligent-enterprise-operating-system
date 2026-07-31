# IRA-006 — WP-06 Implementation Readiness Assessment

**Document ID:** IRA-006
**Work Package:** WP-06
**Capability:** C-003 — Role & Permission Management, scoped per repository-owner charter to "Domain Permission Read APIs"
**Governing Specification:** `docs/Product/PE-001/capabilities/C-003/PE-001-C003_Role_Permission_Management.docx` (**Version 1.1**, amended per `CAR-001` to add `EX-C003-11`)
**Methodology Applied:** `METH-002`/`ADR-017` (`CLAUDE.md §19.7b` five-gate closure sequence), `IMP-001 §6.2a` Context Discovery, `IMP-001 §6.2b` Gap Analysis, `CMD-001 §26.3a` Business Object Eligibility Test — applied in full.
**Status:** Assessment only. No implementation, no code, no migration is performed by this document.

Treat the Git repository as the ONLY source of truth. Every claim below is sourced from `PE-001-C003_Role_Permission_Management.docx` Version 1.1 (extracted and read directly), `BCGA-001`, `CAR-001`, `architecture/02-Constitutional/CAP-001_Enterprise_Capability_Registry.md`, `architecture/06-Reviews/TECH-DEBT.md`, and a direct search of `Backend/Services/AuthService`. No claim is drawn from conversational memory.

---

## 1. Executive Summary

C-003 (Role & Permission Management) is `CLOSED — Certified` via WP-02, which implemented all ten of `PE-001-C003`'s original Enterprise Experiences. `PE-001-C003` was amended to Version 1.1 (`CAR-001`) to add an eleventh, `EX-C003-11` ("Understand Domain Permission Context"), closing a gap `BCGA-001` identified: no Enterprise Experience previously realized `ERB-C003-01`'s own declared *Discover/Understand* lifecycle stages for any authorization policy object type. WP-06 is chartered to implement exactly this one Enterprise Experience, for Domain Permission only, per the repository owner's own explicit charter.

This assessment finds:

- **The governing Business Object already exists and is fully reusable.** `DomainPermission` (`models/domain_permission.py`) was established by WP-02 BA-02 and requires no new registration, no schema change, and no migration — `EX-C003-11` only reads what WP-02 already writes.
- **No Canonical Business Object eligibility question arises.** `EX-C003-11` produces no new context construct of its own (its own Context Created field, authored in `CAR-001`, states "None") — there is nothing to test against `CMD-001 §26.3a`.
- **No constitutional blocker exists.** Unlike WP-05's own Authorization Engine gap, this Work Package requires no new architectural component, no new entity, and no new dependency that does not already exist in this repository.
- **A single Business Activity is proposed**, realizing `EX-C003-11` in full (both its single-item and list/query branches, which share one Trigger, one Contract, and one Context Engineering block in the governing specification's own text).

**Overall Readiness Decision: READY, full scope, no blocker.**

---

## 2. Capability Analysis

| Attribute | Value |
|---|---|
| Capability | C-003 — Role & Permission Management |
| Business Intent (CAP-001, verbatim) | "Manage authorization roles and permissions." |
| Governing Specification Version | PE-001-C003 **Version 1.1** (`CAR-001`) |
| ERB Count | 3 (unchanged by the amendment) |
| EX Count | **11** (ten original + `EX-C003-11`) |
| Experience Contract Count | 8 (unchanged — `EX-C003-11` extends Contract 5.1 rather than adding a ninth) |
| Governing ERB for this Work Package | `ERB-C003-01` (Define Authorization Policy Structure) |
| Governing EX for this Work Package | `EX-C003-11` — Understand Domain Permission Context |
| Governing Contract | `Contract 5.1` (Authorization Policy Definition Authority), as extended by `CAR-001` §2.3 |
| WP-06's own charter scope | **Domain Permission only** — the identical gap for Role, Approval Authority, Delegation Policy, and Runtime Assignment Policy (`BCGA-001 §6.3`) is explicitly out of scope; this Work Package does not extend the capability beyond its charter. |

**`EX-C003-11`, verbatim (from `PE-001-C003` v1.1, authored per `CAR-001 §2.2`):**

- **Trigger:** A Corporate Admin, Domain Admin, or Domain Owner needs to confirm the current state of a specific Domain Permission, or to determine which Domain Permissions currently exist for a given Domain or Membership, before proposing a new grant, a lifecycle change, or reviewing a reported dependency.
- **Purpose:** Retrieves the current governed state of a specific Domain Permission by its own identity, or a filtered list of Domain Permissions matching a stated Domain, Membership, or status criterion, without establishing, versioning, deprecating, retiring, or otherwise altering any object it returns.
- **Participating Personas:** Corporate Admin (`URA-001-32`); Domain Owner (`URA-001-45`); Domain Admin (`URA-001-46`).
- **Lifecycle Participation:** Discover, Understand.

---

## 3. Business Activities (candidate proposal — Pending Canonical Binding, per `PE-001-C003`'s own disposition for every EX)

| Candidate BA | Realizes | Business-Meaningful Action |
|---|---|---|
| BA-01 — Understand Domain Permission Context | `ERB-C003-01` (`EX-C003-11`, in full) | Retrieve a specific Domain Permission's current state by identity, or a filtered list matching a Domain/Membership/status criterion |

**Single Business Activity, not two.** `EX-C003-11`'s own text (§2 above) states one Trigger, one Purpose, and one Context Engineering block covering both its single-item and list/query outcomes — mirroring `WP-05` BA-01's own precedent of one Business Activity producing multiple outcome branches from one governing EX (there, `UNRESOLVED`/`DEFERRED`/`501`; here, single-item/list), rather than WP-01's own View/Search split, which was justified there by two *separate* Enterprise Experiences (not evidenced here — `PE-001-C003` v1.1 authors exactly one EX for this capability). Splitting this into two Business Activities now would invent structure `EX-C003-11`'s own text does not itself draw a line for.

**This numbering is a candidate proposal only.** No Business Activity or canonical identifier is created or bound by this IRA, per `PE-001-C003`'s own Pending Canonical Binding disposition (`Chapter 4`, every EX's own Business Activity References field).

---

## 4. Context Discovery (IMP-001 §6.2a, Bounded Scan)

`PE-001-C003`'s own table-of-contents structure was already fully scanned during `BCGA-001`'s own drafting (its own direct `.docx` extraction, `Chapter 1.9`'s Context Model equivalent). No new Context Model section was introduced by the Version 1.1 amendment — `EX-C003-11` was added under the existing `ERB-C003-01`, consuming context constructs (`Access Evaluation Outcome`'s own class of already-registered state, here: `DomainPermission`'s own already-established state) rather than declaring any new one. This scan requires no re-derivation: `BCGA-001 §4` already performed it for the entire capability, and the amendment did not add a Context Model section requiring a fresh pass.

**Secondary trigger (generic-journey ERB shape):** Not applicable — `ERB-C003-01` remains an object-definition ERB (Establish/Understand verbs for six typed objects), not a generic multi-stage journey shape like `PE-001-C005`'s own `ERB-C005-01`.

---

## 5. Business Object Eligibility Analysis (CMD-001 §26.3a)

**No new candidate construct exists to test.** `EX-C003-11`'s own Context Created field (`CAR-001 §2.2`) states explicitly: *"None. This experience creates no new context of its own."* Its Context Consumed field names the object it reads: *"The Domain Permission's own current governed state, as produced by `EX-C003-02` (establishment), `EX-C003-07` (versioning), or `EX-C003-08` (deprecation/retirement)."*

`DomainPermission` itself was not re-assessed for eligibility here because it is **already a registered, implemented Business Object** (established by WP-02 BA-02, `IRA-002`) — `CMD-001 §26.3`'s own registration-precedes-implementation principle was already satisfied at WP-02's own chartering time. Re-deriving its eligibility now would be redundant, not diligent.

**Determination: No registration required. `EX-C003-11` is purely a read-side realization of an already-registered object.**

---

## 6. Context Lifecycle

Not applicable in the WP-04/WP-05 sense (a multi-stage object lifecycle spanning several Business Activities). `EX-C003-11` neither creates nor transitions `DomainPermission`'s own existing lifecycle (`ACTIVE → SUPERSEDED/DEPRECATED/RETIRED`, per `models/domain_permission.py`'s own `VersionStatus` enum, established by WP-02 BA-07/BA-08) — it only reads whichever state that lifecycle currently holds. No pattern-level ADR is warranted, for the same reason none was warranted by WP-05's own single-object case (`IRA-005 §6`): this is not even a new object, let alone a new multi-object chain.

---

## 7. Gap Analysis (IMP-001 §6.2b, category A–E)

| Candidate BA | Category | Reasoning |
|---|---|---|
| BA-01 — Understand Domain Permission Context | **C** (Architecture requires completion — implementation-level) | No governance question, no missing Business Object, no missing dependency. `DomainPermission`, `BaseRepository.get_by_id()`, `DomainPermissionResponse`, and `require_platform_admin` all already exist and are directly reusable. The only implementation-level design decision (how to shape the list/query filters) is an ordinary API design question, not a constitutional one. |

**Constitutional-vs-Implementation blocker distinction applied:** No question here determines Business Object eligibility or requires a new entity, table, API, service boundary, or business rule not already authorized (`CLAUDE.md §18`'s own list) — every question is "how much of the already-authorized read access to build now," an Implementation Blocker class question, not a Constitutional one (`IMP-001`'s own distinction, formalized per `ADR-014`/`METH-001`).

---

## 8. Existing Reusable Implementation

Confirmed by direct repository search (`Backend/Services/AuthService`):

**Exists and directly reusable, no modification required:**
- `models/domain_permission.py` — `DomainPermission`, `VersionStatus`, `DomainPermissionLevel`. No new column, no new migration.
- `repositories/base_repository.py` — `BaseRepository.get_by_id()`, already inherited by `DomainPermissionRepository`, directly reusable for the single-item branch (mirroring `OrganizationService.get_details()`'s own precedent exactly: *"Reuses BaseRepository.get_by_id via OrganizationRepository as-is — no new repository method required"*).
- `schemas/domain_permission.py` — `DomainPermissionResponse` already exists (WP-02's own Establish response schema) and is directly reusable, unmodified, as the response shape for both new endpoints.
- `dependencies.require_platform_admin` — the same repository-wide interim gate every prior Work Package's endpoints use.
- `middleware/tenant.py` — `/domain-permissions` and `/domain-permissions/*` are **already** in the tenant-exemption list (added at WP-02, `TD-022`'s own disclosed basis). The two new endpoints share this exact path prefix — **no `middleware/tenant.py` change is required.**
- `main.py` — `domain_permission.router` is already registered at `/domain-permissions`. **No `main.py` change is required** — the new endpoints are added to the existing router file.

**Requires one small, additive extension:**
- `repositories/domain_permission_repository.py` — no existing method performs an unfiltered or multi-criterion query; one new method (`search()`) is required for the list/query branch. This is an Extend, not a Create, per `CLAUDE.md §19.5`.
- `services/domain_permission_service.py` — two new methods (`get_by_id()`, `search()`) added to the existing `DomainPermissionService` class.
- `routers/domain_permission.py` — two new `GET` endpoints added to the existing router.

**Does not exist and is not needed:** no new model, no new schema class (query filters are declared as native FastAPI `Query()` parameters, not a request body — there is no request body for a `GET`), no new migration, no new Alembic revision.

---

## 9. Readiness Decision

**WP-06 is READY, full scope, no blocker.** Every dependency this Work Package needs already exists, correctly, in this repository. The single Business Activity (§3) requires only an additive extension of two already-established, already-certified files (`repositories/domain_permission_repository.py`, `services/domain_permission_service.py`) and one router file — no new database object, no new schema, no new middleware entry, no new registration.

---

## 10. Recommendations

### 10.1 Implementation Order

1. `repositories/domain_permission_repository.py` — add `search()`.
2. `services/domain_permission_service.py` — add `get_by_id()`, `search()`.
3. `routers/domain_permission.py` — add `GET /domain-permissions/{id}` and `GET /domain-permissions`.
4. Tests — extend `tests/test_domain_permission_service.py` and `tests/test_domain_permission_api.py` (the same files WP-02 already established for this object, per `CLAUDE.md §12`'s Extend-before-Create discipline — this is not a new domain concept warranting new test files).

### 10.2 Technical Debt Anticipated

The two new endpoints will be gated on `PLATFORM_ADMIN` only, the same interim authorization gap `TD-022` already discloses for `POST /domain-permissions` (Establish) — `PE-001-C003`'s own `EX-C003-11` Participating Personas (Corporate Admin, Domain Owner, Domain Admin) have no distinct, enforceable claim in this repository's seeded role catalog today, the same root cause as `TD-021` through `TD-025`/`031`/`034`–`036`/`039`/`042`/`079`. A new Technical Debt entry (next sequential ID) will be raised at implementation time, mirroring this exact precedent — not treated as a blocker (`CLAUDE.md §19.8.5` does not apply; this is a disclosed, non-security-boundary-weakening authorization-granularity gap, the same class already accepted repository-wide).

### 10.3 No Governance Backlog Item

Unlike `IRA-005 §10.3`, this assessment records no unresolved ownership or architecture question. WP-06's own scope is fully bounded by already-existing, already-reusable implementation.

---

## 11. Business Object Registration

**Not applicable.** No new Canonical Business Object is produced by this Work Package (§5). `DomainPermission` remains owned by its original registration under WP-02.

---

## 12. Repository-Owner Authorization to Begin

**Repository-owner decision, recorded here:** WP-06 is chartered and authorized to begin at **full scope**, per the repository owner's own explicit charter (2026-07-31):

- **BA-01 — Understand Domain Permission Context**: full scope (`EX-C003-11`, both single-item and list/query branches) — no blocker, no minimum-scope narrowing required.

**Explicitly excluded from this authorization, per the repository owner's own charter:** extending this capability beyond `EX-C003-11`; implementing the identical Understand/Query gap for Role, Approval Authority, Delegation Policy, or Runtime Assignment Policy (`BCGA-001 §6.3`); altering `PE-001-C003` further; implementing any unrelated authorization feature.

**Governing update:** `WPR-001`'s own WP-06 row and `WP-REG-001`'s own WP-06 row are added/updated in the same governance pass as this section.

---

*End of IRA-006.*
