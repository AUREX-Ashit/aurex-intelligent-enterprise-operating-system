# STOP-AND-REPORT WP-17-01 — C-023 Entitlement/License Registry Schema Shape

**Type:** Implementation-time STOP-and-report, per `IMP-REPORT-WP-17_Establish_Entitlement_License_Context.md §4(1)` and `CLAUDE.md §18` / `§19.4`.
**Raised by:** WP-17 / BA-01 implementation, Phase 1 (Implementation Discovery / Technical Design), 2026-09-01.
**Repository state:** commit `c2f93d5` (`main`), **at the time this STOP-and-report was raised** (Phase 1, 2026-09-01). ~~**No production code, model, schema, migration, or test was created or run. No Alembic migration exists or was executed.**~~ *(Accurate when raised; superseded 2026-09-01 — final pre-Gate-1 governance cleanup, per direct Repository Owner authorization. After the Repository Owner recorded the schema decision (`TDS-C023-A §19.1`, D-1…D-7), implementation resumed and is COMPLETE — models, the additive Alembic migration (single head `c3d4e5f6a7b8`), repositories, service, router, Pydantic schemas, 23 tests (full `AuthService` suite 876/876), and the two authorized frontend items all exist (`IMP-REPORT-WP-17 §11`) and were independently reviewed SOUND. This STOP-and-report's own content below (§A–§G) is preserved unchanged as the historical record of what was raised. **WP-17 / BA-01 = IMPLEMENTATION AUTHORIZED — IMPLEMENTATION COMPLETE — NOT YET CERTIFIED**; C-023 remains 🔴 RED — NOT IMPLEMENTATION READY; Decisions 1–6, Decision 3, and Decision 4 unchanged/deferred.)*
**Status:** ~~**AWAITING REPOSITORY OWNER / ARCHITECTURAL DECISION.** Implementation of the persistence layer and everything downstream of it is HALTED pending resolution. This document does not choose a schema and does not self-authorize one.~~ *(Resolved 2026-09-01 — the Repository Owner decided the schema, recorded verbatim at `TDS-C023-A §19.1` (D-1…D-7); implementation subsequently resumed and completed (`IMP-REPORT-WP-17 §11`), was independently reviewed SOUND, and `CLAUDE.md §19.7b` Gate 1 has been dispatched. This document's own content — the exact question, the canonical evidence, and the three options — is preserved unchanged below as the historical record of what was raised; it is superseded as a live blocker, not erased. Annotated 2026-09-01 per the R9 governance-reconciliation pass, `IMP-REPORT-WP-17 §14`/`CERT-WP-17` non-material observation O2 — no production code, schema, migration, or test was touched by this annotation.)*

---

## A. Exact unresolved question

**A.1 — What schema decision is required?**

BA-01 ("Establish Entitlement/License Context (Administrative)") must persist the **Authoritative Entitlement Context** and/or **Authoritative License Context** — "the current, single, canonical fact per anchor" (`TDS-C023 §5-A`). To create the SQLAlchemy model(s) and the Alembic migration, the following must be decided, and none is uniquely determined by the current canonical sources:

1. **One table or two.** `Master_Technical_Architecture.md` (MTA) defines **two separate canonical tables** — `license_registry` (per-Membership) and `entitlement_registry` (per-Organization), the `entitlement_registry` PURPOSE comment stating it is "explicitly separate from license_registry". `TDS-C023 §6.3` sketches **one** working-name table, `entitlement_license_registry` ("or equivalent", `§6.3` item 12).
2. **Lifecycle `status` column.** MTA's `license_registry` has **no** status column. BA-01 requires a persisted `status` — `ACTIVE` for the establish/continuing outcome, with the `ACTIVE`/`SUSPENDED`/`REVOKED` lifecycle overlay per `PE-001-C023 §5.5` / `TDS-C023 §10.1` (a future BA transitions it; BA-01 only ever writes `ACTIVE`). Adding a `status` column to a table modelled on `license_registry` is a **new database column** beyond the canonical definition — `CLAUDE.md §18`/`§19.4` territory.
3. **Effective dates on the License side.** MTA's `license_registry` has **no** `effective_from`/`effective_to` (only `entitlement_registry` does). `TDS-C023 §5-A`/`§10.1`/`§14`/`§17` require `effective_from`/`effective_to` on **both** the License and the Entitlement Authoritative Context. Adding them to a license table is a deviation from MTA's `license_registry`.
4. **Entitlement Source Reference column.** Required by `TDS-C023 §6.2`/`§6.3` item 10 and `§5-A`; **absent** from both MTA tables.
5. **Authority reference column.** `TDS-C023 §5-A` requires "a reference to the Commit Authority instance that authorized the transition" (the `approval_authorities` row id, and per `§16` the resolving actor). **Absent** from both MTA tables.
6. **`license_type` column vs Decision 6.** MTA's `license_registry` **has** a `license_type VARCHAR(50)` column. **Decision 6** (`IRA-C023 §18.13`, Split Ownership) and `TDS-C023 §6.3` item 11 ("the single most important design constraint") **forbid** any C-023 mechanism carrying its own copy of the `FULL`/`LIGHT` value — the C-023 record must reference `AuthService`'s `memberships.license_type` by value at read/establish time, never duplicate it. Implementing MTA's `license_registry` **verbatim** would therefore violate Decision 6.
7. **Reference style — hard FK vs referenced UUID.** MTA uses hard foreign keys (`membership_id UUID REFERENCES membership_registry(membership_id)`, `organization_id UUID REFERENCES organization_master(organization_id)`). `TDS-C023 §6.3` item 2 chose "a referenced UUID, **not a hard cross-service database foreign key**" (polymorphic-reference precedent, `approval_authorities.object_id`). `ADR-036` Consequences say co-location in `AuthService` *permits* — but does **not mandate** — simplifying that to a real intra-service FK ("a consequence permitted by this decision, not mandated by it, and it does not change `TDS-C023`'s accepted design intent"). Additionally the MTA canonical FK **target names** (`membership_registry`, `organization_master`) do not match `AuthService`'s actual table names (`memberships`, `organizations`) — a known MTA-vs-implementation naming gap.
8. **Uniqueness constraint shape.** `TDS-C023 §15` reuses `INV-C023-09`/`INV-C023-10` ("exactly one current Authoritative License Context per Membership Anchor" / "per Entitlement Anchor and entitlement type") as a **database-level `UniqueConstraint`**. MTA's tables carry only a surrogate PK — no such constraint. The exact column tuple and predicate (`membership_id` alone? `(membership_id) WHERE effective_to IS NULL`? `(organization_id, entitlement_code)`? `(organization_id, entitlement_code) WHERE effective_to IS NULL`?) is undesigned at the schema-column level.

**A.2 — Why the existing canonical sources do not uniquely resolve it**

- **The MTA's two tables are minimal and insufficient for BA-01 as chartered.** `license_registry` (3 columns: `license_id`, `membership_id`, `license_type`) and `entitlement_registry` (5 columns: `entitlement_id`, `organization_id`, `entitlement_code`, `effective_from`, `effective_to`) carry **no** lifecycle `status`, **no** Entitlement Source Reference, **no** authority reference, and **no** uniqueness constraint enforcing the single-current-context invariant. `TDS-C023 §5-A`/`§14`/`§16`/`§17` require all four.
- **Implementing the MTA tables verbatim would violate an already-recorded Repository Owner Decision.** `license_registry.license_type` directly conflicts with Decision 6's prohibition on C-023 duplicating the Full/Light value.
- **The TDS's richer alternative is explicitly non-final and explicitly deferred to this exact STOP-and-report.** `TDS-C023 §6.3` item 2 ("recommended design", "working name"), item 12 ("`entitlement_license_registry` or equivalent … new-schema territory requiring `CLAUDE.md §18`/`§19.4`'s own STOP-and-report discipline at the point of actual creation"), and `§23` all mark the table shape as an implementation-time design decision requiring STOP-and-report — not a settled design.
- **`ADR-036` deliberately did not decide it.** Decision item 8: "resolves the `WP-17 §8` (Persistence Target) `[D]` item and its mirror `TDS-C023 §24` item 1 — **and nothing else**." Consequences: "**The `license_registry` vs `entitlement_registry` vs `entitlement_license_registry` schema question is NOT decided by this ADR.**"
- **`IMP-REPORT-WP-17 §4(1)`** (the authorization itself) mandates: "The implementing session SHALL author an implementation-time Technical Design for the schema and SHALL perform a `CLAUDE.md §18` / `§19.4` **STOP-and-report** before running any migration … Any schema shape not directly supported by a canonical source requires an explicit Repository Owner decision obtained through that STOP-and-report — it SHALL NOT be assumed."

---

## B. Evidence

### B.1 — Canonical facts (verified against primary sources at `c2f93d5`)

| # | Canonical fact | Source |
|---|---|---|
| B-1 | `license_registry` — columns `license_id UUID PRIMARY KEY`, `membership_id UUID REFERENCES membership_registry(membership_id)`, `license_type VARCHAR(50)` (FULL/LIGHT). PURPOSE: "License grant record per membership." | `Master_Technical_Architecture.md` lines 1610–1619 |
| B-2 | `entitlement_registry` — columns `entitlement_id UUID PRIMARY KEY`, `organization_id UUID REFERENCES organization_master(organization_id)`, `entitlement_code VARCHAR(100)`, `effective_from TIMESTAMPTZ`, `effective_to TIMESTAMPTZ`. PURPOSE: "Feature/module entitlements at the organization level — explicitly separate from license_registry." | `Master_Technical_Architecture.md` lines 1621–1635 |
| B-3 | Schema-catalog listing: "`license_registry` — per-membership license grant (URA-001-111)"; "`entitlement_registry` — org-level feature entitlements, separate from licensing (URA-001-112)". | `Master_Technical_Architecture.md` lines 330–331 |
| B-4 | RLS: `entitlement_registry` org-isolated on `organization_id` directly (line 4777–4778); `license_registry` org-isolated via a join through `membership_registry` (line 4820–4822). | `Master_Technical_Architecture.md` Part D |
| B-5 | The MTA "does not specify … owning service" for its tables; service assignment is an implementation-ownership decision (resolved for C-023 by `ADR-036` = `AuthService`, modular-monolith phase). | MTA ~L5069; `ADR-036` Decision items 1, 8 |
| B-6 | **Decision 6 (Split Ownership):** `memberships.license_type` stays `C-007`/`WP-03`-owned; the C-023 record references it by value, **read-only**, never written/duplicated/migrated; "**never** … a column extension of `memberships`". | `IRA-C023 §18.13`; `TDS-C023 §6.1` / `§6.3` items 1, 3, 5, 9, 11 |
| B-7 | **Decision 1 (Reuse Approval Authority mechanism):** the C-023 Commit Authority is one `approval_authorities` row per Organization, `authority_name = "Entitlement/License Commit Authority"`, `scope_type = 'COMPANY'`, `approval_strategy = 'ANY_ONE'`. **This is data provisioning via the already-certified `ApprovalAuthorityService.establish()` — it needs no schema change** (`authority_name` is already free-text). | `TDS-C023 §7.1`–`§7.6`; `IRA-C023 §19.13`; `models/approval_authority.py` (`ApprovalScopeType.COMPANY`, `ApprovalStrategy.ANY_ONE` already exist) |
| B-8 | Lifecycle per `PE-001-C023`: `ACTIVE` / `SUSPENDED` (reversible) / `REVOKED` (terminal); `EXPIRED` is **never stored** — a read-time derived fact against `effective_from`/`effective_to` (reusing `C-007`'s `compute_membership_authority_consequence()` precedent). `effective_from`/`effective_to` are **independent Commit-time business dates**, not derived from any Subscription. | `TDS-C023 §10.1`; `PE-001-C023 §5.5`, `§1.16`/`§1.17` |
| B-9 | Runtime enforcement (`require_approval_authority()` / `enforce_approval_authority()` / `resolve_approval_authority()` / `membership_approval_authority` binding) is **implemented and certified** (WP-18, `TDS-018`, CLOSED — CERTIFIED — RELEASE-READY). BA-01 consumes it — **no schema work is needed for the authority mechanism itself.** | `dependencies.py` lines 233–307; `services/approval_authority_resolver.py`; `models/membership_approval_authority.py`; `CERT-WP-18` / `VV-AUDIT-WP-18` / `RRA-WP-18` |
| B-10 | Repository precedent for adding a **new registry table to `AuthService`** while deliberately **not** implementing every column the MTA draft lists: `tenant_registry` (`TDS-016 §5`, WP-16) — implemented only the columns the governing TDS actually specified; explicitly omitted the MTA-draft Technical-Provisioning columns; each such new table went through its own governing Technical Design and its own migration authorization. | `models/tenant_registry.py` (docstring); `TDS-016`; `TDS-017` (`authority_holders`) |

### B.2 — Implementation inference (NOT canonical — flagged as such)

| # | Inference | Why it is inference, not fact |
|---|---|---|
| I-1 | A single `entitlement_license_registry` (the TDS §6.3 sketch) would be simpler to consume from one repository/service than two tables. | An implementation-convenience judgement. `CLAUDE.md §18`/`§19.4` and `IMP-REPORT-WP-17 §4(1)` forbid choosing on this basis. The MTA's own text says the two concepts are "explicitly separate". |
| I-2 | Co-located in `AuthService`, an intra-service FK to `memberships.id` / `organizations.id` is available and would be cheaper than a polymorphic UUID reference. | `ADR-036` Consequences explicitly frame this as "a consequence **permitted** … not **mandated**" and "does not change `TDS-C023`'s accepted design intent." Choosing it silently is picking a schema shape. |
| I-3 | The single-current-context uniqueness constraint most naturally maps to a partial unique index `WHERE effective_to IS NULL`, mirroring `authority_holders` / `membership_approval_authority` precedent. | A pattern-match, not a canonical instruction. The invariant text (`INV-C023-09`/`-10`) does not specify the enforcement mechanism or column tuple. |
| I-4 | BA-01 only ever writes `status = 'ACTIVE'`, so a `CHECK (status IN ('ACTIVE','SUSPENDED','REVOKED'))` constraint could be added now for the full lifecycle even though only `ACTIVE` is exercised. | Reasonable, mirrors `approval_authority.py`'s own `VersionStatus` `CHECK`, but it is still a schema-column decision that presupposes the table shape. |

---

## C. Options

Three viable schema options are identified. **No fourth option is developed** — the evidence supports only these, consistent with `CLAUDE.md §19.4`'s caution.

### Option 1 — Two tables, mirroring the MTA canonical split, minimally extended

`license_registry` and `entitlement_registry` as **two** separate `AuthService`-hosted tables, each extended only with the columns BA-01's governing TDS actually requires and the MTA canonical table lacks.

- **`license_registry`** (Membership-anchored): `id` (surrogate PK), `membership_id` (reference to `memberships.id`), **`status`** (ACTIVE/SUSPENDED/REVOKED + CHECK), **`effective_from`** / **`effective_to`**, **`entitlement_source_reference`** (nullable), **`approval_authority_id`** (reference to the `approval_authorities` row that authorized it) + **`committed_by_actor_id`** / `committed_at`, `created_at` / `updated_at`. **No `license_type` column** — the FULL/LIGHT value is read from `memberships.license_type` at establish/resolve time (Decision 6). The `URA-001-115` specialized license types (`§6.2`) would be a nullable `c023_license_type` column **only if BA-01 must establish one** — see §F.
- **`entitlement_registry`** (Organization-anchored, optionally Domain-scoped): `id`, `organization_id` (reference to `organizations.id`), `domain_id` (nullable), `entitlement_type_ref` (an already-recognized type identifier only — no type-creation), `status`, `effective_from` / `effective_to`, `entitlement_source_reference` (nullable), `approval_authority_id` + `committed_by_actor_id` / `committed_at`, `created_at` / `updated_at`.

| Aspect | Assessment |
|---|---|
| **Advantages** | Preserves the MTA's own "explicitly separate" split; each table's RLS follows the MTA's own two distinct isolation patterns (B-4); the License/Entitlement independence `URA-001-112`/`-148` and `BR-C023-03` require is structural, not conventional; nearest to the canonical schema catalog. |
| **Disadvantages** | Two models, two repositories (or one repository with two entities), two migrations, two uniqueness constraints; a caller establishing "both" in one BA request touches two tables in one transaction (still single-service, single-transaction per `TDS-C023 §14`). Still adds `status` / source-ref / authority-ref columns the MTA `license_registry` lacks (§18/§19.4 new-columns). |
| **Impact on existing canonical tables** | None. Both are additive new tables. No `ALTER` to `memberships` / `organizations` / `approval_authorities` / `membership_approval_authority`. |
| **Migration implications** | One migration creating both tables (or two). `down_revision` chains onto the current single Alembic head `f9a3c7e1b5d2` (WP-18). Purely additive; clean `downgrade()`. |
| **FK / tenant-isolation** | If intra-service FKs to `memberships.id` / `organizations.id` are used: real referential integrity, RLS trivially follows the MTA patterns. If referenced UUIDs (per `TDS-C023 §6.3` item 2): service-layer existence checks at establish time (mirroring `ApprovalAuthorityService.establish()`), RLS enforced at establish time + resolution time (mirroring `TDS-018 §18`). **Either sub-choice is itself part of this decision.** |
| **Impact on WP-17 minimum BA scope** | None — scope unchanged; this is purely how the Authoritative Context is stored. |

### Option 2 — One table (`entitlement_license_registry`), per the `TDS-C023 §6.3` sketch

A single `AuthService`-hosted `entitlement_license_registry`: `id`, a discriminator (`context_kind` = LICENSE | ENTITLEMENT), `membership_id` (nullable — set for LICENSE), `organization_id` (nullable — set for ENTITLEMENT), `domain_id` (nullable), `entitlement_type_ref` (nullable — set for ENTITLEMENT), `c023_license_type` (nullable — the `URA-001-115` type, if in scope), `status`, `effective_from` / `effective_to`, `entitlement_source_reference` (nullable), `approval_authority_id` + `committed_by_actor_id` / `committed_at`, `created_at` / `updated_at`. `membership.license_type` is **never** copied here (Decision 6).

| Aspect | Assessment |
|---|---|
| **Advantages** | One model / one repository / one service / one migration / one uniqueness-constraint family; matches the `TDS-C023 §6.3` working name and item 2's polymorphic-reference recommendation directly; one audit/observability code path. |
| **Disadvantages** | Diverges from the MTA's "explicitly separate" two-table canonical definition — the largest departure from canonical of the three options. A nullable-column discriminator table conflates two constructs `URA-001-112`/`-148` and `BR-C023-03` deliberately keep independent; RLS must branch on `context_kind` (org-direct for ENTITLEMENT, membership-join for LICENSE) rather than following either MTA pattern cleanly. |
| **Impact on existing canonical tables** | None (additive new table). But it effectively supersedes two canonical MTA table definitions with one — a canonical-schema reconciliation that `CLAUDE.md §18` reserves to the Repository Owner / architectural authority. |
| **Migration implications** | One additive migration onto head `f9a3c7e1b5d2`; clean `downgrade()`. A future decision to split it back into two tables would then itself be a migration with data movement. |
| **FK / tenant-isolation** | Two nullable anchor columns → FKs can only be `ON DELETE`-guarded per-column and the "exactly one of `membership_id`/`organization_id` is set" rule needs a `CHECK`. RLS branches on the discriminator. More constraint logic than Option 1. |
| **Impact on WP-17 minimum BA scope** | None to scope; but the conflation risk is precisely what Decision 6's investigation (`IRA-C023 §15a`/`§18`) and `BR-C023-03` warn against — worth the Repository Owner weighing explicitly. |

### Option 3 — Defer the table; implement only the schema-independent slice now

Do not create any Entitlement/License persistence table in this pass. Author a dedicated implementation-time **Technical Design (TDS-C023-A or equivalent)** for the schema, submit it for the Repository Owner decision, and in the meantime implement only what is genuinely schema-independent (see §F).

| Aspect | Assessment |
|---|---|
| **Advantages** | Zero risk of an implicit schema commitment; matches `IMP-REPORT-WP-17 §4(1)` and `TDS-C023 §6.3` item 12 / `§23` exactly ("author an implementation-time Technical Design … STOP-and-report before running any migration"); mirrors the `TDS-016`/`TDS-017` → WP-16 precedent (a schema TD authored and accepted before the implementation migration). |
| **Disadvantages** | The schema-independent slice is thin (§F) — most of BA-01 waits. Adds a governance round-trip (author TD → RO decision) before substantive implementation resumes. |
| **Impact on existing canonical tables** | None. |
| **Migration implications** | None now. |
| **FK / tenant-isolation** | Deferred with the table. |
| **Impact on WP-17 minimum BA scope** | None. BA-01 stays exactly as chartered; only the sequencing changes. |

---

## D. Recommendation

**Recommended: Option 3 (author a dedicated implementation-time schema Technical Design, then a single Repository Owner decision), and within it, Option 1's two-table shape as the narrowest option supported by canonical evidence.**

Reasoning:
- **Option 3 is what the authorization itself mandates.** `IMP-REPORT-WP-17 §4(1)` says the implementing session "SHALL author an implementation-time Technical Design for the schema" and STOP-and-report before any migration. This is not optional and not a preference — it is the recorded condition of the grant.
- **Within that TD, Option 1 (two tables) is the narrowest canonically-supported shape.** The MTA canonically defines `license_registry` and `entitlement_registry` as two separate tables and states they are "explicitly separate"; `URA-001-112`/`-148` and `BR-C023-03` keep License and Entitlement independent. Option 1 adds only the columns BA-01's governing TDS demonstrably requires (`status`, `effective_from`/`effective_to` on the license side, `entitlement_source_reference`, `approval_authority_id` + actor) and omits the one canonical column that would violate Decision 6 (`license_type`). Option 2 (one table) is a larger departure — it supersedes two canonical definitions with one and reintroduces the exact License/Entitlement-conflation risk Decision 6's investigation warned against.
- **The reference-style sub-question (intra-service FK vs referenced UUID) and the `URA-001-115` `c023_license_type` sub-question should be settled inside the same TD**, not pre-judged here.

**This recommendation is NOT an approved architectural decision.** It is a recommendation offered per `CLAUDE.md §19.4`. The Repository Owner (or the architectural authority) must explicitly choose the option and the schema shape before any model or migration is written.

---

## E. Governance classification

**This requires an explicit Repository Owner / architectural approval under `CLAUDE.md §18` and `§19.4`.** It involves, at minimum:
- **new database tables** (one or two, per the option chosen);
- **new database columns** relative to the MTA canonical `license_registry` / `entitlement_registry` definitions (`status`, license-side `effective_from`/`effective_to`, `entitlement_source_reference`, `approval_authority_id`, `committed_by_actor_id`);
- a potential **canonical-schema reconciliation** (Option 2 would supersede two canonical table definitions with one);
- a **reference-integrity design choice** (hard FK vs referenced UUID) that `TDS-C023 §6.3` and `ADR-036` both left open.

`CLAUDE.md §19.4` is explicit: on encountering a need for new tables / new columns / new schema, "Claude Code SHALL STOP. Claude Code SHALL NOT implement the change. Instead Claude Code SHALL report … Wait for approval before continuing." `IMP-REPORT-WP-17 §4(1)` and `§7` reinforce this specifically for WP-17. **Claude Code has not chosen a schema and does not self-authorize one.** The recommended next governance step is a dedicated implementation-time Technical Design (e.g. `TDS-C023-A`) submitted for an explicit Repository Owner decision, mirroring the `TDS-016` / `TDS-017` precedent.

---

## F. Implementation boundary

### F.1 — What can safely proceed WITHOUT resolving the schema question

- **Nothing that persists an Authoritative Entitlement/License Context** — the model, repository, service `establish()` transaction, router, request/response Pydantic schemas (their field set is derived from the persistence model), the `require_approval_authority` wiring onto that router, all BA-01 tests, and the two frontend items are **all downstream of the table** and must wait.
- **C-023 `approval_authorities` instance provisioning is schema-independent** but not independently meaningful/testable: establishing the `"Entitlement/License Commit Authority"` row (`scope_type='COMPANY'`, `approval_strategy='ANY_ONE'`, one per participating Organization) uses the **already-certified** `ApprovalAuthorityService.establish()` (WP-02 BA-03) and needs no schema change (`authority_name` is free-text, `TDS-C023 §7.2`). This is data provisioning, exercised via the establish flow — which does not yet exist. It should be sequenced with the establish-flow implementation, not run ahead of it.
- **`membership_approval_authority` binding rows** are likewise data, created via the **already-certified** `MembershipApprovalAuthorityService.bind()` (WP-18) — sequenced with the same flow.
- **A dedicated implementation-time schema Technical Design (`TDS-C023-A` or equivalent)** can and should be authored now — that is the recommended next step (§D, §E). It is a design document, not implementation.

### F.2 — What MUST wait for the schema decision

- `models/…` for the Authoritative Entitlement/License Context.
- The Alembic migration (and therefore any change to the Alembic head).
- `repositories/…` for the new entity/entities.
- `services/…` — the `establish()` transaction (`TDS-C023 §14`).
- `routers/…` and `schemas/…` for the two frontend items and the establish endpoint.
- The `require_approval_authority("Entitlement/License Commit Authority")` dependency wired onto the establish route.
- All BA-01 tests, including the `CLAUDE.md §21.4` Mandatory Tenant-Isolation Test Checklist and the `TDS-C023 §21` V&V obligations.
- The two authorized frontend items (also subject to the separate `IMP-REPORT-WP-17 §4(2)` `§19.1`/`§20.5` STOP-and-report if `DS-001`/Workspace/Navigation coverage proves insufficient).

---

## G. Change control

**Files changed by this Phase-1 discovery / STOP-and-report pass:**

| File | Change |
|---|---|
| `architecture/05-Implementation/STOP-AND-REPORT-WP-17-01_Entitlement_License_Registry_Schema_Shape.md` | **Created** (this document). |

**No other file was created or modified by the original Phase-1 pass.**

**R9 governance-reconciliation annotation pass (2026-09-01), per direct Repository Owner authorization ("Repository Owner Authorization — WP-17 Gate 1 Governance Reconciliation"), resolving `CERT-WP-17` non-material observation O2:** the header `Status` line and the closing status/pointer lines — annotated (strikethrough-preserve, historically accurate for their own pass, not erased) with a dated note pointing to the current, authoritative status in `IMP-REPORT-WP-17 §11`/`§14`. No question, evidence, option, or recommendation content (§A–§F) was altered. No `Backend/` file, migration, model, or test touched. Not staged, committed, or pushed.

**Final pre-Gate-1 governance-cleanup follow-up (2026-09-02), per direct Repository Owner authorization ("Proceed with the final pre-Gate-1 governance cleanup exactly as follows"), resolving the borderline stale-status item the repository-wide sweep identified in this document's header:** the **Repository state** line (line 5) — the absolute clause "No production code, model, schema, migration, or test was created or run. No Alembic migration exists or was executed." struck (strikethrough-preserve) and superseded with a dated note recording that implementation has since resumed and is COMPLETE (Alembic head `c3d4e5f6a7b8`; `IMP-REPORT-WP-17 §11`), independently reviewed SOUND, and that this document's §A–§G content is preserved unchanged as historical record. The `commit c2f93d5` / "at the time this STOP-and-report was raised" scoping was retained. **Not altered:** §A (the exact question), §B (canonical evidence), §C (options), §D (recommendation), §E (governance classification), §F (implementation boundary), §G's own findings list; any `Backend/` file, migration, model, service, router, schema, or test; the C-023 🔴 RED classification; any C-023 Decision 1–6 / Decision 3 / Decision 4. No certification claimed. Not staged, committed, or pushed.

- ~~**No Alembic migration was created or run.** The Alembic head remains `f9a3c7e1b5d2` (WP-18), unchanged.~~
- ~~**No production model, repository, service, router, schema, or test code was created.** `git grep` for any C-023 Entitlement/License implementation symbol in `Backend/` returns zero hits.~~
- *(The two bullets immediately above are historical statements from this Phase-1 discovery / STOP-and-report pass, accurate at commit `c2f93d5`. Struck 2026-09-02 per a final residual-historical-assertion sweep (direct Repository Owner authorization). After the Repository Owner recorded the schema decision (`TDS-C023-A §19.1`, D-1…D-7), implementation resumed and is COMPLETE — the additive Alembic migration is the current single head `c3d4e5f6a7b8`, and the models / repositories / service / router / Pydantic schemas / tests exist (`IMP-REPORT-WP-17 §11`), independently reviewed SOUND. This sweep did not rewrite the historical ledger below; it only marks these two entries as superseded.)*
- **No C-023 Decision 1–6 was reopened or altered** — `IRA-C023 §18.13` / `§19.13` / `§20.12` / `§21.12` / `§22.13` / `§23.13` untouched.
- **WP-18 was untouched** — no change to `TDS-018`, `membership_approval_authority.py`, `approval_authority_resolver.py`, `dependencies.py`, `CERT-WP-18` / `VV-AUDIT-WP-18` / `RRA-WP-18`, or any migration.
- **No excluded WP-17 scope was implemented** — no Consumption, Allocation, Entitlement Catalog administration, Subscription semantics, Billing, C-020/C-025 hand-off, suspend/revoke/reactivate, new service boundary, Authorization Engine / AuthorityHolder / Group redesign.
- **`TDS-C023` and `IRA-C023` were NOT modified** to resolve the schema question — they were read only.
- **Nothing was staged, committed, or pushed** by this pass. `HEAD` = `c2f93d5`.

~~**WP-17 / BA-01 status:** IMPLEMENTATION AUTHORIZED, NOT YET COMPLETE, NOT CERTIFIED — **implementation HALTED at the schema-shape STOP-and-report point; no `CLAUDE.md §19.7b` gate dispatched.**~~
**C-023 capability-wide:** 🔴 RED — Not Implementation Ready (unchanged).
**WP-18:** CLOSED — CERTIFIED — RELEASE-READY (untouched).

*(Superseded 2026-09-01 — R9 governance-reconciliation, `CERT-WP-17` O2: the Repository Owner subsequently decided the schema-shape question (`TDS-C023-A §19.1`), implementation resumed and is now COMPLETE, independently reviewed SOUND, and `CLAUDE.md §19.7b` Gate 1 has been dispatched (NOT CERTIFIED — stale-status documentation only, since reconciled; no code/design defect). Current status: WP-17 / BA-01 = **IMPLEMENTATION AUTHORIZED — IMPLEMENTATION COMPLETE — NOT YET CERTIFIED** (`IMP-REPORT-WP-17 §11`/`§14`). C-023 capability-wide and WP-18 statuses above are unchanged and remain accurate as written.)*

---

~~*Awaiting Repository Owner direction on the schema-shape question (§A / §C / §D) before implementation of the WP-17 / BA-01 persistence layer or anything downstream of it resumes.*~~ *(Resolved — see the `§6`/G annotation above and `TDS-C023-A §19.1`.)*
