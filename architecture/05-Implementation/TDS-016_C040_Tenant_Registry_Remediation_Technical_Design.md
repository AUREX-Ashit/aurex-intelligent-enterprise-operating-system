# TDS-016 — C-040 (Tenant Administration) — `tenant_registry`/`organization_master` Remediation — Technical Design Specification

**Document ID:** TDS-016
**Capability:** C-040 — Tenant Administration (`CAP-001` line 80: Domain D-003 Enterprise Administration, owning specification `SD-002`, Status Active)
**Business Activity (candidate, scope decided, not yet chartered):** BA-01 — "Tenant Establishment only — Business Approval → Infrastructure Allocation" (Repository Owner Decision, recorded in conversation, 2026-08-26, `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md` C-040 row)
**Basis:** `ROD-C040-Tenant-Registry-Remediation-Design.md` (design baseline), the subsequent Independent Implementation-Readiness Review of that document (this session, conversational — determination: **READY FOR IMPLEMENTATION DESIGN**), `ADR-034 §7` (remediation scope authorized)
**Governing constitutional authority (cited, not restated):** `ADR-024` (authority layer), `ADR-025` (1:1 cardinality), `ADR-026` (dual authority, three-step process), `ADR-027` (system-of-record model), `ADR-029` (authority boundaries), `ADR-034` (adoption + remediation scope), `ADR-035`/`AI-001`/`AI-003` (Business Governance Authority, populated), `AI-002`/`TD-157` (Infrastructure Allocation Authority, unpopulated), `SD-002 §2` (`SD-002-004`–`020`) and `§7` (`SD-002-051`–`058`), `CMD-001 §26.3a`/`§26.4`, `PE-001-C040 §5.5`/Contract 5.4/`EX-C040-11`/`ERB-C040-05` (directly re-extracted from the source `.docx` during the readiness review, not taken on any intermediate paraphrase), `TD-158`.

**Document-naming note (mirrors `IRA-C040`'s and `TDS-015`'s own established precedent, not a silent departure):** numbered `TDS-016` — the next number in the flat, sequential Technical Design series (`TDS-012`→WP-12, `TDS-013`/`TDS-014`→WP-14, `TDS-015`→C-066, no WP). No WP number exists for C-040 (confirmed: absent from `WP-REG-001`/`WPR-001`), so this document is titled capability-first, exactly mirroring `TDS-015`'s own identical situation. No WP number appears anywhere in this document's title, filename, or body.

**Status:** Technical Design — implementation NOT authorized by this document. This document determines a mechanism for a candidate Business Activity that has not yet been chartered under any Work Package; it does not charter one, assign one, or authorize building anything (§20).

**Corrections from the readiness review, incorporated throughout this document, not restated as caveats:**
1. Tenant lifecycle is the **four**-state model — PROVISIONED, MIGRATING, OFFBOARDING, OFFBOARDED — per `PE-001-C040 §5.5`'s own verbatim text, not the three-state shorthand the design baseline inherited from `ROD-C040-Tenant-System-of-Record.md`.
2. `ERB-C040-05` ("Commit... Tenant Administrative Transition," `EX-C040-11`) is the Business Approval + Infrastructure Allocation Commit (`ADR-026` Steps 1+2) — **not** `ADR-026`'s separate, still entirely undecided Step 3 (Technical Provisioning). Tenant Establishment and the Authoritative Tenant Context's first existence are **not** made dependent on Technical Provisioning completing anywhere in this design.

---

## 1. Purpose and Scope

Determines **how** the `ADR-034 §7` remediation would be built, given the design baseline (`ROD-C040-Tenant-Registry-Remediation-Design.md`) and the two corrections above — the mechanism, not the chartering decision, not the migration itself.

**In scope:** schema remediation design for `tenant_registry`/`organization_master` (items 1–3 of `ADR-034 §7`); the Tenant Establishment transaction (atomicity, ordering, failure handling, idempotency — all confirmed by the readiness review to be unaddressed by canonical text, and therefore designed here as implementation-level decisions); the corrected four-state lifecycle machine; actor/audit field design; the `CMD-001 §26.3a` eligibility boundary; the runtime-authorization design needed to enforce `ADR-029`'s own already-decided authority boundaries.

**Out of scope, explicitly:**
- Technical Provisioning Authority (`ADR-026 §13`) — entirely undecided, no model, boundaries, or accountable actor exists; not designed here.
- Migration, offboarding, and cross-tenant-sharing approval authority (`ROD-C040-Blocker-Closure-Assessment.md §3` item 16) — the lifecycle *state shapes* for MIGRATING/OFFBOARDING are named per `PE-001-C040 §5.5` (§10 below), but the authorities that trigger those transitions remain Pending Canonical Binding, unaffected by this document.
- Any modification to `AuthService/middleware/tenant.py`, `dependencies.py`, or `routers/configuration.py` — `TD-158`'s disposition is preserved unchanged (§14).
- CBOR registration itself, and any registering ADR (§13).
- `AI-002` population, the Sarika Rath evidence loop, `AI-004`.
- BA chartering, WP assignment, the fresh IRA, and any code, schema, or migration authorship (§20).

## 2. Canonical Authority

Restated as a flat reference list, not re-derived: `ADR-024`–`ADR-035`, `AI-001`–`AI-003`, `ADR-034 §7` (the six remediation items this TDS designs against), `SD-002-004`/`-008`/`-009`/`-010`/`-011`/`-054`/`-056`, `CMD-001 §26.3a`/`§26.4`, `PE-001-C040 §5.5` (Tenant Lifecycle Contract, directly re-extracted, §10), `ERG-001-05`'s service-layer-validation precedent (`Master_Technical_Architecture.md` lines 952–960, cited by analogy for §7's own invariant design), `TD-096` (repository-wide FK-enforcement test-harness gap, cited for §16), `WP-07`/`WP-08`'s own `CMD-001 §26.3a` negative-eligibility precedent for audit-trail-style constructs (`WP-REG-001`, cited for §13), `TD-158`, `TD-157`, the Delivery Map's two 2026-08-26 Repository Owner Decisions.

## 3. Current State

Directly re-verified, not assumed: the real, migrated `AuthService.Organization` model (`models/organization.py`) carries no `tenant_id` column of any kind. `tenant_registry`/`organization_master` exist only as an unimplemented draft in `Master_Technical_Architecture.md`. Zero Alembic migration anywhere creates either table (the initial schema migration's own comment: *"Legacy tables (tenants, users) are intentionally excluded"*). Zero real data exists. `AuthService`'s certified `TenantMiddleware`/`X-Tenant-ID`/`get_current_tenant()` mechanism operationally means `organization_id` (`TD-158`), confirmed by direct code trace. `AI-001` is populated (Ashit Padhi, via `AI-003`); `AI-002` is not (`TD-157`, Open — BLOCKED). C-040 is RED.

## 4. Target State

A dedicated, first-class Tenant domain (`ADR-027`), 1:1 with Organization (`ADR-025`), infrastructure-layer-owned (`ADR-024`), populated only via the dual-authority process (`ADR-026`/`ADR-029`), `SD-002 §2`-conformant, carrying the corrected four-state lifecycle, with `tenant_id` populated exactly once, atomically, at the Business-Approval-plus-Infrastructure-Allocation Commit — never gated on Technical Provisioning (correction 2, §above) — and structurally independent of `AuthService`'s existing legacy `X-Tenant-ID` surface (`TD-158`, preserved unchanged).

## 5. Schema Changes (Design Only — Not Implemented)

**`tenant_registry` (additions to the existing draft):**

| Column | Type | Purpose |
|---|---|---|
| `version` | `INTEGER NOT NULL DEFAULT 1` | `SD-002-010` Universal Versioning |
| `lifecycle_state` | `VARCHAR(20) NOT NULL CHECK (lifecycle_state IN ('PROVISIONED','MIGRATING','OFFBOARDING','OFFBOARDED'))` | Replaces `active_flag`; corrected four-state set (§10) |
| `effective_from` | `TIMESTAMPTZ NOT NULL` | `SD-002-011` Canonical Temporal Model |
| `effective_to` | `TIMESTAMPTZ NULL` | Same |
| `updated_at` | `TIMESTAMPTZ NULL` | Standard audit timestamp, mirrors `organization_master`'s own existing pattern |
| `approved_by_actor_id` | `UUID NOT NULL` | The Business Approval Authority's accountability-point identity (`ADR-034 §7` item 3) |
| `approved_at` | `TIMESTAMPTZ NOT NULL` | |
| `allocated_by_actor_id` | `UUID NOT NULL` | The Infrastructure Allocation Authority's accountability-point identity |
| `allocated_at` | `TIMESTAMPTZ NOT NULL` | Same moment as `created_at` (§8) |

**`organization_master`:** `UNIQUE(tenant_id)` added (already authorized, `ADR-034 §7` item 1); no other column change. `tenant_id` remains nullable (§7).

**Explicitly not added — a design choice, not an oversight:** a back-reference `organization_id` column on `tenant_registry`. The remediation design baseline (§5 of `ROD-C040-Tenant-Registry-Remediation-Design.md`) flagged the absence of a reverse reference as a gap. This TDS resolves it **without a redundant column**: the Tenant→Organization "exactly one" invariant is enforced by the atomic transaction design (§8), not by a second FK. A reverse lookup ("given a Tenant, find its Organization") is already efficiently answerable via `organization_master.tenant_id`'s own `UNIQUE` index — no denormalized column is required. This is the minimal-footprint design, consistent with `CLAUDE.md §19.5`'s Reuse-before-Create ordering; a future convenience denormalization remains available but is not proposed here.

## 6. Constraints / Invariants

1. `UNIQUE(organization_master.tenant_id)` — prevents two Organizations referencing the same Tenant (`ADR-034 §7` item 1). NULL-safe under standard PostgreSQL semantics — any number of Organizations may simultaneously hold `NULL` (§7).
2. `tenant_registry.lifecycle_state` `CHECK` constraint — the corrected four-state set (§10), no fifth/invented state.
3. **Atomicity invariant (service-layer, not a single DB constraint — mirrors the existing `ERG-001-05` service-layer-validation pattern in `Master_Technical_Architecture.md`, the same "a database constraint alone cannot express this" precedent already used elsewhere in this same schema document):** no code path may create a `tenant_registry` row except as part of the single atomic transaction defined in §8, which also writes the `organization_master.tenant_id` association. This is what enforces "exactly one Organization per Tenant" — not a second FK column.
4. **Immutability invariant (service-layer):** once `organization_master.tenant_id` is populated for an Organization, no code path may change it to a different value — identity is never reassigned (`ROD-C040-Tenant-System-of-Record.md §13` invariant 2). Whether this is additionally enforced by a database trigger is an implementation-time choice, not decided here.

## 7. Tenant/Organization Cardinality — Precision Restated

`organization_master.tenant_id` remains **nullable**. NULL means Tenant Establishment has not yet completed for that Organization (Decision 1, 2026-08-26) — never that the Organization is itself the Tenant. `tenant_id` becomes mandatory (non-NULL) for a given Organization **only** at the moment the atomic Establishment transaction (§8) commits for it — never before, never inferred, never defaulted. `NOT NULL` is not proposed as a table-level constraint (no canonical text requires it, and a genuine pre-establishment window is architecturally required by `ADR-026`'s own phased process).

## 8. Tenant Establishment Transaction

**Design principle, stated once and applied throughout:** canonical sources establish *who* may act and *what* the two-step sequence is (`ADR-026`, `ADR-029`); they establish nothing about atomicity, ordering mechanics, or failure handling (confirmed by direct full-text search of `PE-001-C040` during the readiness review — zero occurrences of "atomic," "idempotent," "rollback," "concurrent," "retry"). **Everything below is therefore an implementation-level design decision, not a constitutional requirement.** It does not require, and is not authorized by, a new ADR.

```text
BEGIN TRANSACTION
  1. Verify caller is the currently-appointed Infrastructure Allocation
     Authority accountability point (§12) — reject otherwise.
  2. Verify a valid, referenced Business Approval decision exists for
     this Organization (ADR-029 §11 MAY: "confirm... prerequisites").
  3. Verify organization_master.tenant_id IS NULL for this Organization
     — the idempotency/duplicate-establishment guard.
  4. INSERT INTO tenant_registry (tenant_id = gen_random_uuid(),
     tenant_code = ..., lifecycle_state = 'PROVISIONED', version = 1,
     approved_by_actor_id, approved_at, allocated_by_actor_id,
     allocated_at = now(), created_at = now()).
  5. UPDATE organization_master SET tenant_id = <new tenant_id>
     WHERE organization_id = <this Organization> AND tenant_id IS NULL.
  6. If step 5 affects zero rows (a concurrent transaction already
     populated tenant_id first) → ROLLBACK the entire transaction,
     including step 4's INSERT.
COMMIT (or ROLLBACK on any failure at any step).
```

- **Which authority creates the Tenant:** the Infrastructure Allocation Authority (`AI-002`, currently unpopulated), per `ADR-029 §11`'s own MAY grant — the *decision* is authorized by canonical text; the transaction mechanics above are this TDS's own implementation design.
- **When `tenant_registry` becomes authoritative / when `organization_master.tenant_id` is populated:** the same moment — the single transaction's own `COMMIT` — consistent with `PE-001-C040`'s own text: *"the first Authoritative Tenant Context for that anchor is produced only through successful provisioning Commit (`ERB-C040-05`)"* (correction 2, above — this is the Approval+Allocation Commit, not Technical Provisioning).
- **What must be atomic:** the `tenant_registry` INSERT and the `organization_master.tenant_id` UPDATE — one database transaction, standard ACID guarantees, no custom crash-recovery mechanism invented.
- **Decision/execution split (`ADR-029 §11`'s own MAY: "delegate the technical execution... to an automated mechanism"):** the Infrastructure Allocation Authority's accountable Person authorizes a specific allocation; an automated service executes the transaction above on that authorization's behalf. The service itself enforces step 1 — it does not accept an unauthenticated or self-asserted "I am the Infrastructure Allocation Authority" claim (§12).

## 9. Idempotency / Retry / Failure Handling

Explicitly labeled: **implementation/TDS-level design, not a constitutional requirement**, per the readiness review's own direct-evidence finding.

- **Duplicate establishment request:** step 3/6 of §8 guarantees only the first successful transaction populates `tenant_id`; any subsequent attempt for the same Organization observes `tenant_id IS NOT NULL` at step 3 and is rejected as already-established — **no second Tenant identity can ever be created for one Organization.**
- **Partial creation:** impossible under the single-transaction design — standard PostgreSQL crash-recovery guarantees all-or-nothing commit; no custom mechanism is invented.
- **Transaction failure:** full rollback, no `tenant_registry` row and no `organization_master` change persist; whether a caller/UI automatically retries is a UX-level decision, not addressed here (canonical text is silent, per the readiness review).
- **Replay** (a stale or duplicate message replayed via any future retry-queue mechanism): the same step-3/6 guard makes replay-after-success a safe no-op and replay-before-success a safe re-attempt.

## 10. Lifecycle State Machine (Corrected — Four States)

Per `PE-001-C040 §5.5`, directly re-extracted, verbatim: *"A provisioned Tenant SHALL exist in exactly one of PROVISIONED, MIGRATING, or OFFBOARDING/OFFBOARDED state at any point in time... Only PROVISIONED SHALL be treated as valid for new dependent capability reliance... MIGRATING SHALL be a transient, self-resolving state that returns to PROVISIONED upon completion."* Elsewhere the spec enumerates four discrete values: `PROVISIONED, MIGRATING, OFFBOARDING, OFFBOARDED` (plus the non-persisted meta-state `NOT_FOUND` for "no Authoritative Context exists yet").

```text
(no row exists)
      │  Establishment transaction commits (§8)
      ▼
  PROVISIONED ──────────────┐
      │  ▲                  │
      │  │ (self-resolving) │
      ▼  │                  ▼
  MIGRATING            OFFBOARDING
                              │
                              ▼
                         OFFBOARDED  (terminal)
```

**Transitions supported by canonical text:** `(none) → PROVISIONED` (§8); `PROVISIONED → MIGRATING`; `MIGRATING → PROVISIONED` ("self-resolving... returns to PROVISIONED"); `PROVISIONED → OFFBOARDING`; `OFFBOARDING → OFFBOARDED`. `OFFBOARDED` is terminal — `BR-C040-05` (`IRA-C040 §9`) confirms an offboarded Tenant is never reprovisioned to the same anchor.

**Not invented, explicitly:** no `MIGRATING → OFFBOARDING` transition, no `OFFBOARDED → PROVISIONED` transition, and no fifth "pending"/pre-provisioned state — none is supported by any canonical text examined, and none is added here.

**Caveat, not new, cross-referenced not restated:** the state *shapes* above are canonical (`PE-001-C040 §5.5`); the *authorities* that trigger `→ MIGRATING` and `→ OFFBOARDING` specifically remain Pending Canonical Binding (`ROD-C040-Blocker-Closure-Assessment.md §3` item 16) — this design does not name, invent, or assume one. Only the `(none) → PROVISIONED` transition has a fully resolved triggering authority today (`AI-001`/`AI-002`).

## 11. Actor / Audit Requirements

- **Tenant creation:** `approved_by_actor_id`/`approved_at` (Business Approval, `AI-001`) and `allocated_by_actor_id`/`allocated_at` (Infrastructure Allocation, `AI-002`) — both written in the same atomic transaction (§8), satisfying `SD-002-056` ("no approval exists without an audit record").
- **Organization↔Tenant association:** no separate audit record is needed beyond the above — the association is written in the same transaction, sharing the same actor/timestamp context.
- **Lifecycle transitions (Migrating/Offboarding):** `SD-002-009` requires every transition to generate an event; each transition should carry its own actor and timestamp. **Whether this is a dedicated audit-trail table or an event stream is not decided here** — this repository's own established precedent (`WP-07`/`WP-08`, `WP-REG-001`) consistently finds newly-proposed audit-trail-style tables **not independently `CMD-001 §26.3a`-eligible** for CBOR registration ("none of the four new persisted constructs eligible for canonical registration"); a Tenant lifecycle audit construct would plausibly follow the same disposition, but this is an eligibility determination for actual implementation time, not asserted here.

## 12. Security / Authorization

**Only the currently-appointed accountability point of each authority may act** — `ADR-029 §10`/`§11`'s own exclusive MAY grants, with explicit self-approval and `PLATFORM_ADMIN`-bypass-semantics prohibitions (`ADR-029 §10`/`§11`, `ADR-002 §17a`). This is fully resolved by canonical text — no new constitutional authority is invented here.

**A concrete, previously-unaddressed implementation gap, surfaced by this design:** `AI-001`/`AI-002`/`AI-003` are governance *documents* — none creates a runtime-enforceable claim. The runtime authorization mechanism by which the constitutionally established `AI-001`/`AI-002` authorities become enforceable runtime authorization is **not determined by this TDS**. The existing `approval_authority_registry` mechanism is organization-scoped (`organization_id NOT NULL`, `Backend/Services/AuthService/models/approval_authority.py`) and therefore cannot directly represent these platform-wide, pre-Organization authorities, **as already established by `ADR-031 §8`** ("`organization_id` (`approval_authority_registry`'s own `NOT NULL` constraint, structurally incompatible)") — cited here, not rediscovered or reinterpreted. Selection of the appropriate existing Authorization Runtime mechanism (`ADR-016`), or any required implementation adaptation, is a separate, future authority-runtime-enforcement workstream and is explicitly **OUT OF SCOPE** for this `tenant_registry` remediation TDS. This is not a new constitutional gap created by this document; this TDS does not select the runtime mechanism, does not create a new authority, does not modify `ADR-016`, and does not authorize creation of any runtime authority object. The equivalent step for Infrastructure Allocation Authority cannot even be reached yet, since `AI-002` has no appointed human at all (`TD-157`).

**Design (once both prerequisites are met):** an authorization dependency, mirroring the shape of `AuthService`'s already-certified `require_platform_admin`/`require_matching_tenant_or_platform_admin` pattern, checking the caller's identity against the specific Approval Authority holder — never against a generic role/claim, consistent with `ADR-029`'s own prohibition on inheriting `PLATFORM_ADMIN` bypass semantics.

## 13. CBOR / Registry Boundary

Restated from the design baseline, not re-derived: Tenant preliminarily passes `CMD-001 §26.3a`'s three-step eligibility test (independent identity; cross-Business-Activity reference via `EX-C040-15`/Contract 5.3; governed lifecycle per §10 above) — **ELIGIBLE**, preliminarily. Actual registration requires its own future registering ADR (`CBOR-INDEX.md`'s own Amendment Procedure) — **not created, not invented, not performed here.** A lifecycle-transition audit-trail construct, if built as a separate table, would require its own, likely negative, eligibility determination at that time (§11).

## 14. WP-10 Compatibility Boundary

Decision 2 (2026-08-26) and `TD-158` are preserved unchanged in full. `AuthService/middleware/tenant.py`, `dependencies.py`, and `routers/configuration.py` are not modified, referenced for modification, or redesigned by any part of this TDS. Nothing in §§5–13 above creates any code path connecting `tenant_registry`/`organization_master` to the existing `X-Tenant-ID` surface. Any future genuine-Tenant-identity integration into that surface remains a separate, explicitly out-of-scope workstream requiring its own design and certified-behavior compatibility analysis, per `TD-158`'s own Target Resolution.

## 15. Migration / Bootstrap Considerations

Per the readiness review's own confirmed finding: **this is a new implementation, not a repair or backfill of existing data** — zero rows, zero prior migration, zero prior implementation exist anywhere for `tenant_registry` or `organization_master.tenant_id`. No data-migration/backfill script is required for existing rows, because none exist. The only "migration" in the Alembic sense is the schema-creation work itself, not performed here. **Left open, correctly, not blocking this design's own completeness:** how already-certified, pre-existing Organizations (WP-01 through WP-15's own rows) relate to Tenant Establishment retroactively — a future bulk pass, individual future Establishment, or permanently-NULL-until-touched — an implementation-time or Repository-Owner-adjacent question that does not change the schema or transaction design above.

## 16. Test / Validation Strategy

Mirroring `CLAUDE.md §21.4`'s Mandatory Tenant-Isolation Test Checklist and this repository's own established CBAIP test conventions:
- **Two-Organizations test:** two Organizations independently complete Establishment; confirm each receives a distinct `tenant_id`; confirm no cross-Organization `tenant_id` leakage.
- **Idempotency/race test:** concurrent Establishment attempts for the same Organization; confirm exactly one `tenant_registry` row results (exercises §8 step 3/6).
- **Foreign-tenant-identifier probe** (`CLAUDE.md §21.4`(c)): confirm an arbitrary/unrelated `tenant_id` supplied by a caller is never silently accepted or associated.
- **Authorization probe:** confirm a caller who is not the currently-appointed accountability point (once runtime-enforceable, §12) is rejected.
- **Lifecycle-transition tests:** `PROVISIONED→MIGRATING→PROVISIONED`; `PROVISIONED→OFFBOARDING→OFFBOARDED`; confirm `OFFBOARDED` accepts no further transition; confirm an unsupported transition (e.g., `OFFBOARDED→PROVISIONED`, `MIGRATING→OFFBOARDING`) is rejected.
- **`UNIQUE` constraint enforcement test:** confirm the database itself (not only application logic) rejects a duplicate `organization_master.tenant_id` — this future implementation would otherwise inherit the same class of gap `TD-096` already discloses repository-wide (the shared SQLite test harness does not enable `PRAGMA foreign_keys=ON`); not a new finding, flagged here so it is not silently repeated.

## 17. Rollback Strategy

**Schema-level (once actually implemented, not performed here):** a standard Alembic `downgrade()` dropping the new columns/constraints. **Transaction-level:** covered fully by §8/§9 — standard database `ROLLBACK`, no custom mechanism. **Data-migration-level:** not applicable — §15 confirms no data migration/backfill occurs, since no existing data exists to migrate.

## 18. Explicit Non-Goals

This document does not: implement code, schema, or a migration; create a CBOR entry or a registering ADR; resolve Technical Provisioning Authority; resolve migration/offboarding/cross-tenant-sharing approval authority (only their already-canonical state *shapes* are named, §10); modify `TenantMiddleware`, `dependencies.py`, or `routers/configuration.py`; populate `AI-002`, reopen the Sarika Rath evidence loop, or create `AI-004`; create the `approval_authority_registry` runtime object flagged in §12 (identifies the need, does not perform it); charter a Business Activity or Work Package; run the fresh IRA; change C-040's readiness status.

## 19. Dependencies

- `AI-002` population (`TD-157`, frozen) — blocks *live execution* of the Infrastructure Allocation half of §8's transaction; does not block this design's own completeness.
- Runtime realization of `AI-001` as an enforceable Approval Authority object (§12, newly flagged) — blocks live execution of the Business Approval half.
- BA chartering (separate, outstanding — Delivery Map, 2026-08-26).
- The fresh IRA (`CLAUDE.md §19.7`, outstanding).
- A future CBOR registering ADR (§13, not pursued here).

## 20. Implementation Authorization Boundary

**This document does not authorize implementation.** Per `CLAUDE.md §19.1`'s own no-self-authorization discipline (the same discipline `TDS-015`'s own precedent already applied): BA chartering, WP assignment, and Implementation Authorization each remain separate, subsequent, explicit Repository Owner actions, not performed or implied by this TDS.

**Explicitly preserved, unchanged by this document:**
- `AI-002` remains unpopulated. `TD-157` remains Open — BLOCKED.
- C-040 remains RED — Not Implementation Ready.
- The BA charter remains a separate, outstanding step.
- The fresh IRA remains outstanding.
- `TD-158` and the Delivery Map's two 2026-08-26 Repository Owner Decisions are unchanged, not re-recorded, and not modified by this document — no update to `TECH-DEBT.md` or the Delivery Map was found to be required by this repository's own TDS convention (`TDS-015`'s own precedent shows no such cross-update performed at TDS-authoring time; such updates occur at actual WP-chartering time).

---

*End of TDS-016. No implementation, migration, model, repository method, router, service, schema, or test file has been created or modified by this document. No WP number has been assigned or implied. No other governance document (`CAP-001`, `SD-002`, `SER-001`, `TECH-DEBT.md`, `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md`, `Master_Technical_Architecture.md`, `ADR-024`–`035`, `AI-001`–`003`, `CLAUDE.md`) was modified in the preparation of this design. No CBOR entry was created. `AI-002` was not touched. C-040 remains RED — Not Implementation Ready.*
