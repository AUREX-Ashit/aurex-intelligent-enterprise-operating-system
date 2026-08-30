# TDS-018 — C-003 (Role & Permission Management) — Approval Authority Runtime Binding — Technical Design Specification

**Document ID:** TDS-018
**Capability:** C-003 — Role & Permission Management (owns `approval_authority_registry`/`membership_registry`, both hosted in `AuthService`, `WP-02`/`WP-03`)
**Scope:** the reusable, repository-wide runtime mechanism that binds an existing, Organization-scoped `approval_authorities` record to the actor(s)/caller(s) permitted to satisfy it. **Not C-023-specific** — C-023's own Decision 1 (`IRA-C023 §19.13`) is the trigger that surfaced this gap, but the mechanism designed here serves any capability that establishes an Approval Authority, exactly as `approval_authority_registry` itself already does.
**Basis:** direct Repository Owner instruction ("C-003 / Repository-Wide — Technical Design for Approval Authority Binding"), issued after `TDS-C023 §29`'s own investigation (`architecture/05-Implementation/TDS-C023_Licensing_and_Entitlement_Minimum_BA.md`) concluded that `membership_approval_authority` is the only canonically-supported binding mechanism identified, that it is specified in `Master_Technical_Architecture.md` but unimplemented, and that this is repository-wide infrastructure, not C-023-specific work — independently verified twice more in this document (§4).
**Governing constitutional authority (cited, not restated):** `URA-001-04`/`-08`/`-23`/`-38`/`-41`/`-42`/`-54`/`-57`–`-62`/`-66`/`-70`/`-71`/`-74`–`-82`; `Master_Technical_Architecture.md` (schema catalog, `approval_authority_registry`/`membership_approval_authority`/`group_registry`/`group_membership`/`runtime_assignment_registry` definitions and RLS policies); `RTA-001 §11` (Authorization Engine, Context, Decision, Trace); `ADR-016` (five-tier model authority); `ADR-002 §17a`/`§18` (`PLATFORM_ADMIN`/`AUREX_ADMIN` bypass scope, unresolved, untouched here); `TDS-017` (structural precedent, the `approval_authorities`/`authority_holders` distinction); `TDS-C023 §7`/`§9`/`§24`/`§29` (the triggering investigation).

**Document-naming note:** next number in the flat, sequential TDS series after `TDS-017`; capability-owned (`C-003`), not tied to any one Work Package — identical basis to `TDS-015`/`-016`/`-017`'s own precedent of capability-first, WP-independent numbering. No WPR-001 row is created or modified by this document — established repository convention (`TDS-016`, `TDS-017` precedent) registers a TDS only within its eventual governing Work Package's own row, not as a standalone governance-index entry; no such Work Package exists yet for this repository-wide infrastructure.

**Status (as originally issued — preserved per this repository's own no-silent-fix convention, mirroring `§10`/`§11`/`§20`'s own supersession handling):** ~~Technical Design — implementation NOT authorized. No schema, migration, model, repository, service, router, resolver, or test is created by this document. No Repository Owner decision is made by this document (§27). No authority holder or `approval_authorities`/`membership_approval_authority` row is created or populated.~~

**Status (current — updated 2026-08-29, Gate 1 M-1 governance-traceability reconciliation; see §31):** This is, and remains, a **governing Technical Design**. It never itself granted implementation authorization, it still creates no schema, migration, model, repository, service, router, resolver, or test, and it still makes no Repository Owner decision (§24, §27). **Since this document was issued, the Repository Owner has separately and explicitly granted Implementation Authorization for WP-18 (2026-08-29), and implementation against this design has been completed** — both recorded in full in `IMP-REPORT-WP-18_Approval_Authority_Runtime_Binding.md §1`/`§2`, and reflected consistently in the `WP-18` charter header and the `WPR-001` WP-18 row. That authorization came from the Repository Owner, recorded in `IMP-REPORT-WP-18`, **not from this document**. **WP-18 remains NOT YET CERTIFIED** — no `CLAUDE.md §19.7b` gate (Gate 1, Gate 2, or Gate 5) has yet passed. This status block does not itself certify WP-18, does not authorize anything, and does not re-dispatch Gate 1.

---

## 1. Purpose

Design the reusable, repository-wide runtime mechanism by which an existing, certified `approval_authorities` (`ApprovalAuthority`, WP-02 BA-03) record — which stores an authorization *policy* (strategy, scope) — is resolved at runtime against a specific caller, to determine whether that caller is one of the actors permitted to satisfy it. This mechanism does not exist anywhere in this codebase today, for any capability (`TDS-C023 §7.7`/`§19.4-A`, independently re-confirmed at `§4` below).

## 2. Scope

**In scope:** the canonical binding object between `approval_authorities` and an accountable actor; its cardinality and Organization-scoping properties; the runtime resolver contract (input/output/failure shape); the resolver's relationship to `Backend/Runtime/AuthorizationEngine`; its relationship to `AuthorityHolder` and to Group constructs; security/fail-closed requirements; a conceptual (not physical) data model; audit requirements; migration/compatibility implications for the certified `approval_authorities` table; a future implementation sequence; and an explicit determination of whether any Repository Owner decision or new ADR is required.

**Out of scope:** any implementation — no model, migration, repository, service, resolver, router, or test is created; `ALL`/`MAJORITY`/`SEQUENTIAL` strategy vote-counting/sequencing algorithms (named as a future item, §12); C-023 itself (no License/Entitlement record, no C-023 authority holder, no `ERB-C023-05`); `AI-002` population; `TenantMiddleware`/`X-Tenant-ID`; any modification to `approval_authorities`, `memberships`, `authority_holders`, `dependencies.py`, or `Backend/Runtime/AuthorizationEngine`; `PLATFORM_ADMIN`/`AUREX_ADMIN`'s own separate, unresolved bypass-scope question (`ADR-002 §17a`, untouched).

## 3. Constitutional Baseline

`URA-001-41` ("Approval Authorities Are First-Class Objects") and `URA-001-42`/`-62` (four configurable strategies: `ANY_ONE`/`ALL`/`MAJORITY`/`SEQUENTIAL`) govern `approval_authorities` itself — certified, unchanged, not reopened here. `URA-001-61` governs its four scopes (`GLOBAL`/`COMPANY`/`DOMAIN`/`OBJECT`), each requiring `organization_id` (`ADR-031 §8`, independently re-confirmed at `TDS-017 §5`: *"GLOBAL' here means global within one Organization's own approval structure, not platform-wide across Organizations"*). None of this is reinterpreted or narrowed by this document — it is the fixed input this design binds an actor to, never redefined.

## 4. Existing Machinery — Full Trace (Independently Re-Verified This Pass)

**4.1 `approval_authority_registry`/`approval_authorities` — real, certified, WP-02 BA-03/07/08.** Stores strategy + scope, never a holder — confirmed directly (`models/approval_authority.py`, no holder/actor column of any kind).

**4.2 `membership_approval_authority` — canonical, unimplemented.** `Master_Technical_Architecture.md` lines 1318–1329:

```sql
CREATE TABLE membership_approval_authority (
    membership_id UUID REFERENCES membership_registry(membership_id),
    approval_authority_id UUID REFERENCES approval_authority_registry(approval_authority_id),
    effective_from TIMESTAMP WITH TIME ZONE,
    effective_to TIMESTAMP WITH TIME ZONE,
    PRIMARY KEY (membership_id, approval_authority_id, effective_from)
);
```

Row-Level-Security policy (lines 4798–4803) scopes it to Organization via a join through `membership_registry.organization_id` — no `organization_id` column of its own, the identical indirect-scoping pattern `ApprovalAuthority.domain_id → Domain`'s own Organization anchor already uses in this codebase. Schema-catalog listing (line 323): *"membership_approval_authority — assigns approval authorities to memberships."* Independently corroborated by a pre-existing citation already in this codebase, predating both this document and `TDS-C023 §29`: `approval_authority_repository.py::get_active_dependents()`'s own docstring names this exact table as *"Master Technical Architecture's canonical `membership_approval_authority` join table... the real dependent of an Approval Authority."* **Not implemented anywhere in `AuthService`** — absent from `models/__init__.py`'s complete import list; no Alembic migration references it (repository-wide search, zero hits).

**4.3 `group_registry`/`group_membership` — canonical, unimplemented, and NOT bound to Approval Authority.** Both fully specified in `Master_Technical_Architecture.md` (lines 1331–1356, own RLS policies), matching `URA-001-08`/`-57`–`-59`. Not implemented in `AuthService` (absent from `models/__init__.py`). A direct search for any `group_approval_authority`-shaped table returns **zero results**. `group_registry`'s own documented consumers are its self-referencing `parent_group_id` (line 1342, hierarchy), `group_membership.group_id` (line 1351, membership), and `runtime_assignment_registry.assigned_to_group_id` (line 1430, the Named User/Group Runtime Assignment tier) — none targets `approval_authority_registry`. **This confirms, independently re-verified a third time (after `TDS-C023 §29.3`'s original text and its own subsequent correction), that no canonical Group-to-Approval-Authority binding exists.**

**4.4 `Backend/Runtime/AuthorizationEngine` — M1 skeleton only.** `ApprovalAuthorityResolver` (`authorization/tier_resolvers.py`) inherits `BaseTierResolver.resolve()` as `@abstractmethod`, never overridden — not instantiable. `engine.py`'s own docstring: *"No concrete TierResolver is bound by this module... every tier is NOT_EVALUATED"* until a future milestone (M5, "Assignment/Delegation/Approval Authority real resolution") binds one; M1 ships with zero resolvers bound by default. `AuthorizationContext` (`models.py`) already carries an `approval_authorities: tuple[str, ...]` field and a mandatory `organization_id: str` — structurally compatible with an Organization-scoped mechanism, unlike `TDS-017`'s own finding for the platform-wide `AI-001`/`AI-002` case (§10, contrast).

**4.5 `AuthorityHolder`/`require_authority_holder` — a different, deliberately incompatible mechanism.** Re-verified directly (`models/authority_holder.py`, `dependencies.py`): `CheckConstraint("authority_identity IN ('AI-001', 'AI-002')")` — closed to exactly two values; **deliberately carries no `organization_id` column** (`TDS-017 §23`: *"the entire point of this table's own existence"*). Built for a platform-wide, pre-Organization accountability point — structurally the opposite shape from the Organization-scoped `approval_authorities` mechanism (§9 below).

**4.6 `dependencies.py` — no `require_approval_authority`-shaped function exists.** Re-read in full: `require_platform_admin`, `require_matching_tenant_or_platform_admin`, `require_domain_permission`, `require_authority_holder` (+ `require_ai001_holder`/`require_ai002_holder`) — no fifth function targeting `approval_authorities`.

## 5. Design Question 1 — What Is the Canonical Binding Object?

**`membership_approval_authority`** (§4.2). It is the only construct in canonical architecture that directly relates an accountable actor (via Membership) to a specific `approval_authorities` row. This is a finding, not an invention — the table is already fully specified in `Master_Technical_Architecture.md`; this document identifies and designs around it, it does not create it.

## 6. Design Question 2 — Is `membership_approval_authority` the Correct Mechanism?

**Yes**, on the evidence at §4.2–§4.3: it is canonical (explicit `CREATE TABLE`, explicit RLS, catalog listing, independent pre-existing corroboration), Organization-scoped by construction, and identifies the accountable actor with the most precision available in this codebase (`membership_id`, not a Role or Group pool). The only competing candidate with any canonical textual proximity — Group (§4.3) — has no binding to `approval_authority_registry` anywhere in the canonical schema. `AuthorityHolder` (§4.5) and the Runtime Authorization Engine (§4.4) are each independently confirmed as the wrong shape or not yet buildable-from (§9, §10). No other candidate was found in a repository-wide search for actor/accountability/authority-assignment constructs (`Role`/`RolePermission` — wrong precision, cannot bind to one specific individual per `TDS-017 §5`'s own independent finding; `DomainPermission` — different tier; `Person`/`Identity` — identity primitives only; `OrganizationNode`, `ConfigurationEntry`, `TenantRegistry`, `DelegationPolicy` — each a distinct, unrelated concern).

## 7. Design Question 3 — Cardinality

Per the canonical `CREATE TABLE` definition (§4.2), `membership_approval_authority` is a **many-to-many, time-versioned join**:

- **One Membership → many Approval Authorities:** supported — a Membership row may appear against multiple `approval_authority_id` values.
- **One Approval Authority → many Memberships:** supported — the same `approval_authority_id` may appear against multiple `membership_id` values, which is what makes `ALL`/`MAJORITY`/`SEQUENTIAL` strategies representable at all (a "pool" of accountable people), even though the counting/sequencing logic that would consume that pool is not yet designed (§12).
- **Organization boundary — implicit, not structurally enforced.** The table carries no `organization_id` column of its own; RLS (§4.2) scopes read access via `membership_registry.organization_id`, but **nothing in the canonical schema as specified prevents a `membership_approval_authority` row from binding a Membership in Organization X to an `approval_authorities` row scoped to Organization Y.** This is a genuine, disclosed gap, investigated rather than assumed — the two FKs (`membership_registry`, `approval_authority_registry`) are independent; no `CHECK` constraint or cross-table trigger enforces their own respective `organization_id`s must match. **A future implementation MUST add this enforcement at the service layer** (mirroring how `ApprovalAuthorityService.establish()` already validates its own FK targets' existence before insert, §17) — not assumed safe by this design, and not built here.
- **Cross-Organization bindings are therefore not canonically prohibited by schema alone — they must be prohibited by service-layer validation, an implementation requirement this document names but does not build.**

## 8. Design Question 4 — What Does `ANY_ONE` Mean Operationally?

Derived mechanically from two already-canonical facts, not invented: `URA-001-42`'s own definition (*"ANY_ONE (any one member approves)"*) plus `membership_approval_authority`'s own schema (each row is one Membership's own individual binding to one Approval Authority). **Operational meaning: a caller's own currently-effective Membership satisfies an `ANY_ONE`-strategy `approval_authorities` row if, and only if, at least one currently-effective `membership_approval_authority` row exists linking that Membership to that row.** This is Category B (mechanical consequence of two already-certified constructs combined), not a fresh interpretive choice requiring Repository Owner adjudication — restated precisely at §11's resolver algorithm.

## 9. Design Question 5 — Other Strategies Already Specified

`URA-001-42`/`-62` name all four: `ANY_ONE`, `ALL`, `MAJORITY` (configurable threshold, `majority_threshold_pct`), `SEQUENTIAL` (predefined order). All four are already represented in `ApprovalAuthority.approval_strategy`'s own `CheckConstraint` (certified, unchanged). **Only `ANY_ONE`'s resolution semantics are designed by this document** (§8, §11) — consistent with `TDS-C023 §7.6`'s own recommendation that C-023's first consumer use `ANY_ONE` only. `ALL`/`MAJORITY`/`SEQUENTIAL` require vote-counting or sequencing logic with no canonical precedent anywhere in this codebase (`ApprovalAuthorityService`'s own docstring: *"Approval authority shall remain metadata-driven"*, `RTA-001 S11.11` — a policy/catalog record, never itself a workflow execution) — genuinely open, named as a future item (§12, §26), not resolved or invented here.

## 10. Design Question 6 — Resolver Determination Logic

**Superseded by §29's own corrected algorithm — preserved here unchanged as the historical record of the original design, per this repository's own no-silent-fix convention (mirroring `TDS-017 §21`'s identical practice).** An independent WP-18 implementation-readiness review found the sequence below contains no explicit gate on `approval_strategy`, creating a High-severity false-`ALLOW` risk (a `MAJORITY`/`ALL`/`SEQUENTIAL`-configured row could be satisfied by a single qualifying binding) and found step 6's malformed-configuration check is not actually wired into the gating order. **§29 is the corrected, operative algorithm; this section's own text is not.**

Given `(target_organization_id, authority_name, caller_membership_id)`, the resolver must determine, in this order, each condition sourced to an already-certified field (none invented):

1. **Missing/inactive/superseded authority.** Query `approval_authorities` for `organization_id = target_organization_id AND authority_name = authority_name AND status = 'ACTIVE'`. Zero rows → **no authority configured**, deny. `SUPERSEDED`/`DEPRECATED`/`RETIRED` rows are never considered — only the current `ACTIVE` version governs (`ApprovalAuthority.status`, `VersionStatus`, already certified, mirrors `TDS-C023 §7.8`).
2. **Organization mismatch.** The caller's own claimed `organization_id` (from verified claims, mirroring `require_matching_tenant_or_platform_admin`'s own existing claim-vs-target comparison pattern) must equal `target_organization_id`. Mismatch → deny, never resolved further — this is a structural rejection, the same "cannot match a real UUID" property `TDS-017 §22` already relies on elsewhere in this codebase.
3. **Eligible actor / missing binding.** Query `membership_approval_authority` for `approval_authority_id = <the row found in step 1> AND membership_id = caller_membership_id`, filtered to rows currently effective (`effective_from <= now < effective_to OR effective_to IS NULL`). Zero rows → **no eligible binding for this caller**, deny — distinct from step 1's "no authority configured" (the authority exists; this caller specifically is not bound to it).
4. **Active/inactive actor.** The caller's own `Membership` must itself be currently valid: `membership_status = 'ACTIVE'` (or whichever active-equivalent states a future Membership-lifecycle Business Activity certifies — not narrowed here) AND the Membership's own `effective_from`/`effective_to` window (`WP-03 BA-01`, certified) covers "now." A structurally-bound but no-longer-active Membership must not satisfy the authority — fail closed.
5. **Multiple bindings.** Not an error condition — for `ANY_ONE`, any one qualifying row (steps 1–4 all satisfied) is sufficient; for `ALL`/`MAJORITY`/`SEQUENTIAL`, multiple bindings define the pool the (not-yet-designed, §9) counting/sequencing logic would consume.
6. **Invalid configuration.** E.g., `approval_strategy = 'MAJORITY'` with `majority_threshold_pct IS NULL` — **not currently prevented by any `CheckConstraint`** on `approval_authorities` (independently re-verified against the model, §4.1) — a genuine, disclosed gap. The resolver must treat this as **fail-closed deny**, never simulate, infer, or default a threshold.

## 11. Design Question 7 — Fail-Closed Behavior

**Superseded by §29 — the "steps 1–4" reference below is the same defect §10's own superseding note names (steps 1–4 were never actually gated on `approval_strategy`); §29 restates this section's own principle correctly against the corrected algorithm.** Preserved unchanged as the historical record.

Every branch at §10 above denies by default; only the single, fully-satisfied `ANY_ONE` path (steps 1–4 all pass) authorizes. No branch simulates, infers, or defaults an authorization outcome — mirrors `require_authority_holder`'s own certified failure semantics exactly (*"this dependency never simulates, infers, or defaults a holder"*) and `AuthorizationEngine.evaluate()`'s own certified behavior (*"this engine never defaults to ALLOW"*, `engine.py`). No `PLATFORM_ADMIN`/`AUREX_ADMIN` fallback exists at any branch — `ADR-002 §17a`'s own separate, unresolved bypass-scope question is neither invoked nor narrowed here (§20).

## 12. Design Question 8 — Runtime Authorization Engine Integration

Two integration paths exist, genuinely competing, presented as an Options Analysis (mirroring `TDS-017 §14`'s own established method for the structurally analogous C-040 question) rather than decided unilaterally:

| | **Option A — Concrete M5 `ApprovalAuthorityResolver`** | **Option B — Direct FastAPI dependency (`require_approval_authority`-shaped)** |
|---|---|---|
| Architectural fit | **Correct long-term home** — `URA-001-76` names Approval Authority as Engine tier 3; `AuthorizationContext` already carries `organization_id`/`approval_authorities` fields structurally compatible with this mechanism (§4.4) — unlike `TDS-017`'s own AI-001/AI-002 case, no structural incompatibility blocks this route | Bypasses the Engine entirely — same pattern `require_authority_holder`/`require_platform_admin` already use, and the one `TDS-C023 §7.7` already conceptually sketched |
| Scope required | Also requires M2 (Enterprise Scope Validation), M3 (Business Activity/pre-execution-gate integration) — a real caller must construct an `AuthorizationContext` and invoke `AuthorizationEngine.evaluate()`, and no such caller exists yet anywhere in this codebase (`engine.py`'s own M1-only docstring) | None of M2–M4 required; deployable as soon as `membership_approval_authority` exists |
| Consistency with existing precedent | No precedent yet — would be the first real tier resolver built | Directly mirrors `require_authority_holder`'s own already-certified shape |
| Creates a second, parallel authorization pathway? | No — the canonical, single pathway `URA-001-76` describes | **Yes, in effect** — a second entry point querying the same canonical data (`approval_authorities`/`membership_approval_authority`) without routing through the Engine's own pipeline; an honestly-disclosed compromise, not hidden |
| Proportionate to unblocking C-023's minimum `ANY_ONE` need now? | No — disproportionate; would require building M2–M4 first, well beyond this gap | Yes — proportionate, immediately deployable |

**Recommendation, not a decision:** **Option B for the near term**, explicitly as an interim measure, not a permanent architectural substitute for Option A — mirroring exactly how `TDS-017 §15` framed its own analogous recommendation (*"a technical recommendation only, not self-executing"*). **Option A remains the architecturally correct long-term home** and should be revisited once M2–M4 exist and a real Business Activity Engine caller exists to construct `AuthorizationContext`s in production. This tension is disclosed here precisely so it is not silently resolved either way.

## 13. Design Question 9 — Should `ApprovalAuthorityResolver` Become a Concrete Resolver?

**Not by this document, and not now, per §12's own Option B recommendation.** Building it now would be disproportionate to the actual near-term need (unblocking C-023's `ANY_ONE` case) and would require also building the still-unbuilt M2–M4 milestones — a materially larger scope than this repository-wide gap alone requires. It remains the correct eventual target (§12), named as a future item (§26), not built or scaffolded here.

## 14. Design Question 10 — Relationship to `AuthorityHolder`

**Coexist, never merge or conflate — confirmed, not assumed.** `AuthorityHolder` exists for a structurally different purpose: a closed, two-value (`AI-001`/`AI-002`), platform-wide, pre-Organization accountability point (`TDS-017 §6`/`§7`/`§23`), deliberately carrying no `organization_id`. `membership_approval_authority` is the opposite shape by design: open-ended (any `approval_authorities` row), Organization-scoped, many-to-many. **`AuthorityHolder` must not be reused for this purpose** — doing so would require either weakening its own certified `CheckConstraint` (violating "preserve existing certified behavior") or conflating two constructs `TDS-017 §5`/`§8`/`§23` deliberately kept separate. Both mechanisms may exist permanently, side by side, serving different classes of authority — this is not a transitional state to be resolved later.

## 15. Design Question 11 — Relationship to Group Membership

**Not canonical for this purpose — investigated, not assumed, stated explicitly, per the governing instruction's own requirement.** `Group` (`group_registry`/`group_membership`) is itself a canonical, currently-unimplemented construct (§4.3), but no canonical source binds a Group *to* an Approval Authority — `group_registry`'s only documented consumers are its own hierarchy, its own membership, and the unrelated Named User/Group Runtime Assignment tier (§4.3). **This document does not create Group infrastructure, does not invent a Group-to-Authority binding, and does not treat Group membership as satisfying an Approval Authority.** Should a future, separate governance/design act establish a canonical Group-to-Authority binding, it would be additive to — not a replacement for — `membership_approval_authority`, since the two are not mutually exclusive; that act is not performed, scheduled, or implied here.

## 16. Design Question 12 — Reusability

**Yes, by design — this is the entire point of designing it at C-003, not at C-023.** Any capability that establishes an `approval_authorities` row (present or future) may depend on this same mechanism once built: C-023 (§17, the triggering case); any future Organization-scoped approval workflow that adopts `approval_authorities` per `URA-001-41`'s own general-purpose framing. This document creates no C-023-specific, or any other capability-specific, authorization framework — the design is capability-agnostic throughout (§2, §17).

## 17. Authorization Model — Five Layers, Not Conflated

```text
Approval Authority definition        (approval_authorities — WP-02 BA-03, certified, unchanged)
        │
        ▼
Authority-to-actor binding           (membership_approval_authority — §5–§7, this document's own subject)
        │
        ▼
Runtime resolution                   (§10–§13 — the resolver algorithm/contract, not yet built)
        │
        ▼
Authorization decision               (ALLOW/DENY, reusing RTA-001 S11.8's own AuthorizationDecision taxonomy, §19)
        │
        ▼
Business operation                   (e.g. a future ERB-C023-05 Commit — §22, explicitly NOT built here)
```

Each layer is independently governed and independently versioned; no layer is merged into another anywhere in this design. The Definition layer is already certified and untouched. The Binding layer is this document's own central subject (§5–§7). The Resolution layer is designed (§10–§13) but not built. The Decision layer reuses an already-certified taxonomy (§19), not a new one. The Business Operation layer is explicitly out of scope (§2, §22).

## 18. Security Requirements

- **Organization isolation:** enforced at three points — RLS on `membership_approval_authority` itself (§4.2, canonical); the resolver's own explicit organization-match check (§10 step 2); and the service-layer cross-Organization-binding guard this document names as required but does not build (§7). No point relies on a single layer alone.
- **Fail-closed authorization:** every resolver branch defaults to deny (§11); no branch authorizes on absence of information.
- **No implicit administrative bypass:** neither `PLATFORM_ADMIN` nor `AUREX_ADMIN` nor any Role/claim is treated as automatically satisfying an Approval Authority anywhere in this design (§11, §20) — `ADR-002 §17a`'s own separate, unresolved bypass-scope question is untouched, not narrowed, not invoked.
- **Deterministic resolution:** the ordered, exhaustive branch sequence at §10 always reaches exactly one outcome for a given input at a given instant — no ambiguous or partially-resolved state.
- **Stale/inactive authority handling:** `SUPERSEDED`/`DEPRECATED`/`RETIRED` `approval_authorities` rows, and no-longer-effective `membership_approval_authority`/`Membership` windows, are each independently checked and each independently deny (§10 steps 1, 3, 4) — no cached or trusted-from-token authorization state (mirrors `TDS-017 §22`'s own "live lookup... never trusting a claim embedded in the JWT" principle, reused here as the same design discipline, not copied code).
- **Auditability:** §21.
- **Prevention of cross-tenant authority leakage:** §7's disclosed schema gap plus §10 step 2's resolver-level check together close this at two independent layers; §7's own service-layer guard remains a named, not-yet-built requirement.
- **Explicit handling of conflicting bindings:** "conflicting" is not itself an error state under this design — multiple qualifying bindings are the expected `ALL`/`MAJORITY`/`SEQUENTIAL` case (§10 step 5); a genuinely malformed row (§10 step 6) fails closed, never guessed.

## 19. Data Model (Conceptual Only — No Schema or Migration Created)

Reusing exactly the columns `Master_Technical_Architecture.md` already specifies (§4.2), with implementation-time hardening items named, not built:

| Field | Purpose | Note |
|---|---|---|
| `membership_id` | FK → `memberships.id` | Half of the composite PK |
| `approval_authority_id` | FK → `approval_authorities.id` | Half of the composite PK |
| `effective_from` | SD-002-011-style temporal bound | Third element of the composite PK, per the canonical schema |
| `effective_to` | SD-002-011-style temporal bound, NULL = open-ended | |

**Primary key:** `(membership_id, approval_authority_id, effective_from)`, exactly as canonically specified — permits multiple, distinct time-windows for the same pair.

**Uniqueness/concurrency hardening (named, not built):** the canonical schema as specified has no constraint preventing two *overlapping* effective windows for the same `(membership_id, approval_authority_id)` pair — a future implementation should add either a partial unique index (mirroring `authority_holders`'s own `ux_authority_holders_active_authority` precedent, §4.5) or an application-level guard at bind-time, to prevent ambiguous double-binding.

**Organization consistency (named, not built):** §7's disclosed gap — a future implementation must validate, at bind-time, that the target Membership's own `organization_id` equals the target `approval_authorities` row's own `organization_id`, mirroring `ApprovalAuthorityService.establish()`'s own existing FK-target-existence validation pattern (§4.1).

**Lifecycle/activation/deactivation:** governed entirely by `effective_from`/`effective_to`, no separate status column — consistent with the canonical schema's own minimal shape; a binding is "deactivated" by setting `effective_to`, never deleted (§ deletion behavior, below).

**Audit requirements:** §21.

**Deletion behavior:** the canonical schema names no soft-delete/status column, implying (Category C, implementation-time confirmation needed, not decided here) that a binding's own historical record should be preserved and closed via `effective_to`, not hard-deleted — mirroring every other SD-002-011-shaped table in this codebase (`ApprovalAuthority`, `DelegationPolicy`, `RuntimeAssignmentPolicy`, `AuthorityHolder`, all preserve history via status/effective_to rather than deletion). Not a constitutional requirement stated anywhere for this specific table — a recommended consistency choice, disclosed as such.

**Referential integrity:** two `NOT NULL`-implied FKs (`membership_id`, `approval_authority_id`) — the canonical `CREATE TABLE` does not explicitly mark them `NOT NULL`, but a binding row without both is meaningless; a future implementation should add `NOT NULL` explicitly (implementation-time precision, not a canonical-schema deviation).

## 20. Runtime Contract

**The seven-label reason list below is superseded by §29's own eight-label list (adding `UNSUPPORTED_STRATEGY`) — preserved unchanged as the historical record.**

**Input (minimum):** the target Organization identifier; the required `authority_name`; the caller's own verified claims (`person_id`, `organization_id`) and resolved `membership_id` for the target Organization — mirrors `TDS-C023 §7.7`'s own already-sketched input shape exactly.

**Output — reuses the existing `AuthorizationDecision` taxonomy (`RTA-001 S11.8`, `authorization/models.py`), rather than inventing a new status enum, per the governing instruction's own explicit preference for reuse over invention:** `ALLOW` or `DENY` as the outer decision (`CONDITIONAL`/`DELEGATED`/`ESCALATED` are not applicable to this binary `ANY_ONE` case and are not used here, not removed from the taxonomy). Alongside the decision, a `reason` string (mirroring `TierEvaluation.reason`'s own existing shape in the same module, and `HTTPException.detail`'s own existing shape in `dependencies.py`) carries the specific diagnostic category for callers and audit:

- `NO_AUTHORITY_CONFIGURED` — no `ACTIVE` `approval_authorities` row for the Organization/name (§10 step 1).
- `INACTIVE_AUTHORITY` — a row exists but is `SUPERSEDED`/`DEPRECATED`/`RETIRED` (§10 step 1).
- `INVALID_SCOPE` — caller's own Organization does not match the target (§10 step 2).
- `NO_ELIGIBLE_ACTOR` — the authority exists and is ACTIVE, but no currently-effective `membership_approval_authority` binds this caller to it (§10 step 3).
- `INACTIVE_MEMBERSHIP` — the caller's own Membership is not currently valid (§10 step 4).
- `INVALID_CONFIGURATION` — a structurally malformed authority row, e.g. `MAJORITY` with no threshold (§10 step 6).
- `AUTHORIZED` — all conditions satisfied (the sole `ALLOW` path).

These seven labels are documentation/diagnostic content for the `reason` string, not a second, competing enum — the task's own explicit "do not invent unnecessary status categories" is honored by reusing `AuthorizationDecision` as the actual returned type.

**Failure semantics:** every non-`AUTHORIZED` reason denies (§11) — no partial or conditional success path exists in this minimum design.

## 21. Audit / Observability

Reuses this codebase's own existing convention exactly (`observability.py`'s `record_audit`/`publish_event`/`AuditStatus`, already used by `ApprovalAuthorityService` itself, §4.1) — no new audit subsystem is invented. What should be auditable, once built:

- **Authority resolved (`AUTHORIZED`):** `record_audit(action="RESOLVE_APPROVAL_AUTHORITY", status=AuditStatus.SUCCESS, ...)`, metadata including `approval_authority_id`, `membership_id`, `authority_name`, `organization_id`.
- **Authority denied:** `record_audit(..., status=AuditStatus.DENIED, ...)`, metadata including the specific `reason` (§20) — mirrors every existing `ApprovalAuthorityService` method's own denial-audit pattern exactly.
- **Authority configuration missing/invalid:** audited as a `DENIED` outcome with `reason` = `NO_AUTHORITY_CONFIGURED`/`INVALID_CONFIGURATION` — not a distinct audit category, consistent with treating every denial uniformly.
- **Binding changed (a future `membership_approval_authority` create/supersede/close action):** would itself need its own `record_audit`/`publish_event` pair, mirroring `ApprovalAuthorityService.establish()`/`create_new_version()`'s own existing pattern exactly — not designed in further detail here, since binding *management* (as opposed to binding *resolution*) is a further future implementation concern (§26) this document does not scope in detail.

## 22. C-023 Relationship (Informative — No C-023 Implementation Performed)

Once built, C-023's own `ERB-C023-05` (Commit) would depend on this infrastructure exactly as `TDS-C023 §7.7` already conceptually sketched: a future `require_approval_authority("Entitlement/License Commit Authority", minimum_strategy=ANY_ONE)`-shaped dependency (§12 Option B), attached to whichever endpoint implements the Commit action, resolving whether the caller satisfies the currently-`ACTIVE` `approval_authorities` row named `"Entitlement/License Commit Authority"` for the target Organization. C-023 would say, in effect, *"this operation requires Approval Authority X"*; this mechanism determines whether caller Y satisfies X — the same separation of concerns §17's own five-layer model states structurally. **Not performed here:** any C-023 code, any C-023 authority holder, any C-023 License/Entitlement record, any `ERB-C023-05` implementation, any `WP-17` change.

## 23. Migration / Compatibility

`membership_approval_authority` is strictly **additive** — a new table with FKs to two already-certified tables (`approval_authorities`, `memberships`), no column added to either, no constraint of either touched. Existing `approval_authorities` records are entirely unaffected: they remain valid, queryable, and CRUD-manageable via the already-certified `ApprovalAuthorityService` exactly as today, whether or not any `membership_approval_authority` row references them yet (an `approval_authorities` row with zero bindings is not an error state — it is simply an authority no one yet fulfills, correctly denying every caller per §10 step 3/§11). Existing consumers (the certified `ApprovalAuthorityService`/`ApprovalAuthorityRepository`/router/schema, `WP-02` BA-03/07/08) require no change of any kind. Future consumers (this document's own resolver, §10–§13; C-023 or any later capability, §16/§22) are strictly additive on top.

## 24. Governance / Repository Owner Decision Determination

**No new Repository Owner decision is required by this document, and no new ADR is required.** Every classification below was checked explicitly, per this repository's own `CLAUDE.md §19.8.7`-style discipline (applied here to governance classification generally, not only Technical Debt):

| Item | Classification | Basis |
|---|---|---|
| Selecting `membership_approval_authority` as the binding mechanism | **A** — already determined | `IRA-C023 §19.13` Decision 1 already named "reuse the existing Approval Authority mechanism"; this table is that mechanism's own canonical completion, not a competing choice |
| `ANY_ONE` operational semantics | **B** — repository precedent, mechanical consequence | `URA-001-42` + the table's own schema, combined (§8) |
| `ALL`/`MAJORITY`/`SEQUENTIAL` resolution algorithm | **C** — ordinary future implementation design | No canonical precedent anywhere in this codebase; not needed for the minimum `ANY_ONE` scope (§9, §12) |
| Engine-tier (Option A) vs. direct-dependency (Option B) integration | **C** — ordinary implementation-design choice, with a technical recommendation offered, not decided | Mirrors `TDS-017 §14`/`§15`'s own identical treatment of its own analogous choice (§12) |
| Cross-Organization binding enforcement mechanism (service-layer guard vs. trigger) | **C** — ordinary implementation-design choice | §7, §19 |
| `PLATFORM_ADMIN`/`AUREX_ADMIN` bypass scope | **Pre-existing, separately unresolved (`ADR-002 §17a`)** — not reopened, not touched, not required to be resolved by this document | §18, §11 |

**No item above is classified D (requires a fresh Repository Owner decision) or E (requires a new ADR).** This mirrors `TDS-017 §19`'s own identical conclusion for its structurally analogous C-040 gap ("No item is classified D or E").

## 25. Open Questions (Disclosed, Not Resolved)

1. `ALL`/`MAJORITY`/`SEQUENTIAL` vote-counting/sequencing algorithm (§9, §12) — genuinely undesigned, Category C.
2. Engine-tier (Option A) vs. direct-dependency (Option B) as the actual build path (§12) — a technical recommendation is offered (Option B, near term), not a decision.
3. Overlapping-window uniqueness hardening for `membership_approval_authority` (§7, §19) — a recommended pattern is named, not built.
4. Cross-Organization binding enforcement's exact mechanism — service-layer validation vs. database trigger (§7, §19) — not chosen here.
5. Binding-management endpoints (create/supersede/close a `membership_approval_authority` row) — not designed in this document at all; only binding *resolution* is designed (§26 names this as a future implementation-sequence item).

## 26. Implementation Sequencing (Derived — FUTURE IMPLEMENTATION, Not Performed Here)

```text
A. membership_approval_authority model + migration (§19)         ──┐
                                                                     ├──► D. Runtime resolver / dependency (§10–§13, §20)
B. Cross-Organization binding-creation guard (§7)               ──┘        │
                                                                             ▼
C. Binding-management repository/service (create/supersede/close) ────► E. Audit wiring (§21)
                                                                             │
                                                                             ▼
                                                                   F. Tests (positive/negative, tenant-isolation,
                                                                      fail-closed, per §10's own exhaustive branch set)
                                                                             │
                                                                             ▼
                                                                   G. Consumer integration (e.g. a future C-023
                                                                      require_approval_authority dependency, §22)
                                                                             │
                                                                             ▼
                                                                   H. Explicit Implementation Authorization (separate,
                                                                      future, explicit Repository Owner act)
```

**A and B are independent and may proceed in parallel.** **C depends on A.** **D depends on A and B.** **E depends on D.** **F depends on A–E existing to test against.** **G depends on D–F.** **H is the separate, explicit gate — not self-authorized by this document, per `CLAUDE.md §19.1`, mirroring `TDS-017 §20`'s own identical discipline.**

## 27. Explicit Non-Goals

This document does not: implement the `membership_approval_authority` model, migration, repository, service, resolver, or dependency; modify `approval_authorities`, `memberships`, `authority_holders`, `dependencies.py`, or `Backend/Runtime/AuthorizationEngine`; create a new ADR; make a Repository Owner decision; implement C-023 in any way, create a C-023 authority holder, or create a C-023 License/Entitlement record; modify `WP-17`, `IRA-C023`, or `TDS-C023`; resolve `ALL`/`MAJORITY`/`SEQUENTIAL` semantics; build Group infrastructure; touch `ADR-002 §17a`'s own separate bypass-scope question; change C-023's RED classification; or authorize its own eventual implementation.

---

## 28. Independent Review

**Dispatched as a genuinely independent, fresh-context review, no access to the drafting session's own conversation.** Every load-bearing citation in this document was independently re-derived from primary sources, not trusted from the document's own quotes.

**Central claim: CONFIRMED.** The reviewer independently re-opened `Master_Technical_Architecture.md` and confirmed, line-for-line: the `membership_approval_authority` `CREATE TABLE` (lines 1323–1329, exact match), its RLS policy (lines 4798–4803), its schema-catalog listing (line 323), and — via an exhaustive `grep` for `REFERENCES approval_authority_registry` returning exactly one hit (`membership_approval_authority` itself, line 1325) — the complete absence of any `group_approval_authority`-shaped table. `group_registry`'s three FK consumers (`parent_group_id` self-reference, `group_membership.group_id`, `runtime_assignment_registry.assigned_to_group_id`) were independently re-confirmed, none targeting `approval_authority_registry`. The implementation gap was independently re-confirmed: `membership_approval_authority` appears only in `approval_authority_repository.py`'s own pre-existing docstring (lines 21, 28), absent from `models/__init__.py`'s import list and `__all__`, absent from every migration.

**Cross-Organization-binding gap (§7/§19): CONFIRMED.** The reviewer independently read the actual `CREATE TABLE` definitions of `membership_registry`, `approval_authority_registry`, and `membership_approval_authority` and confirmed no `CHECK`/trigger ties the two referenced tables' own `organization_id`s together — this document's own disclosure (a genuine gap requiring future service-layer enforcement, not claimed safe) was independently verified as accurate, not overstated or understated.

**`AuthorityHolder`, Runtime Authorization Engine, and `dependencies.py` claims: all independently confirmed exactly**, including verbatim re-verification of `authority_holder.py`'s `CheckConstraint` (line 52–55), `tier_resolvers.py`'s unoverridden abstract `resolve()` (line 47–50/77), `engine.py`'s "no resolvers bound"/"never defaults to ALLOW" docstring language (lines 11–23, 68–70), `models.py`'s `AuthorizationContext.organization_id`/`approval_authorities` fields (lines 68, 74), and the exact five-function inventory of `dependencies.py` (zero `approval_authorit`-named function beyond this document's own proposed, not-yet-built, `require_approval_authority`).

**No prohibited silent assumption found** — the reviewer read §8, §10, §11, §14, §15, §18 closely and confirmed none treats Organization Admin, `PLATFORM_ADMIN`/`AUREX_ADMIN`, Group membership, or blanket Membership as automatically satisfying an Approval Authority, and confirmed `AuthorityHolder`/Approval Authority are kept explicitly distinct throughout.

**§24's governance classification independently assessed as defensible** — the Option A/B choice (§12) left as a named recommendation rather than an executed decision was found correctly classified Category C, not D, for a design-only document that authorizes no implementation.

**§17's five-layer model independently confirmed internally consistent** — Definition/Binding/Resolution/Decision/Business-Operation remain separated throughout, no place merges Binding into Resolution or Decision into Business Operation.

**Scope-creep / unauthorized implementation: none found.** The reviewer cross-checked `git status --short`/`git diff --stat` against the session's own pre-existing baseline and confirmed every already-modified/untracked file (`dependencies.py`, `WPR-001`, the WP-16/C-040 artifacts, etc.) predates this document's creation and contains zero mention of `TDS-018`, `C-003`, or `membership_approval_authority` in its own diff content — this document is the only file this pass added. A repository-wide `grep` for `membership_approval_authority`/`group_approval_authority` found no model, migration, or schema file implementing either, and no concrete `ApprovalAuthorityResolver` anywhere.

**Two non-material issues disclosed, not requiring correction:** (1) §4.4's Engine-docstring quotation bridges two source lines with an ellipsis — faithful in substance, not byte-exact; (2) the reviewer did not independently re-verify `TDS-017`'s own internal citations (out of this review's assigned scope) — only the codebase facts this document itself attributes to `TDS-017` were checked, and those held up exactly.

**Overall verdict, quoted:** *"a well-sourced, honest, non-implementing technical design document — every load-bearing citation I independently re-derived from primary sources... matched exactly, the disclosed gaps... are genuine and correctly characterized as unenforced rather than falsely claimed safe, no prohibited silent assumption was made, and `git status`/`git diff` confirm no implementation artifact or out-of-scope file was created or modified in this pass — I found no material defect."*

---

## 29. Amendment — §10 Resolver Algorithm Correction (Approval-Strategy Gate)

**Provenance note, mirroring `TDS-017 §21`'s own established convention:** this amendment records a correction to `§10`/`§11`/`§20`'s own operative resolver algorithm, found necessary by an independent WP-18 implementation-readiness review (a separate, later governance pass than `§28`'s own original design review). **`§§1–28` above are preserved unchanged, not rewritten** — this amendment corrects the defect at the design level without erasing the record of how it was found. This amendment was performed by the same session that authored `§§1–28`; it is independently re-reviewed at `§30` below, not self-certified.

**29.1 The defect, restated precisely.** The original `§10` algorithm never conditioned on `approval_authorities.approval_strategy` before reaching `AUTHORIZED` — once an `ACTIVE` row existed, the caller's Organization matched, a currently-effective `membership_approval_authority` binding existed, and the caller's Membership was valid, the algorithm authorized regardless of whether the row's own strategy was `ANY_ONE`, `ALL`, `MAJORITY`, or `SEQUENTIAL`. Since `§9` explicitly leaves `ALL`/`MAJORITY`/`SEQUENTIAL` resolution logic undesigned, the practical consequence — independently confirmed by the WP-18 readiness reviewer — was a **High-severity false-`ALLOW`**: an authority an administrator configured as `MAJORITY` (e.g., 3-of-5) or `ALL` could be satisfied by a single qualifying binding, silently downgrading a stronger configured governance control with no error and a clean `SUCCESS` audit record. `§19.8.5`'s own prohibition on deferring security defects as ordinary Technical Debt applies directly — this is corrected here, not logged and deferred. A second, related flaw was found in the same review: the original `§10` step 6 (malformed-configuration denial) was never actually wired into the algorithm's own gating order, and could in principle be bypassed the same way.

**29.2 Corrected resolver algorithm (operative — supersedes `§10` in full).** Given `(target_organization_id, authority_name, caller_membership_id)`, in this exact order, no step skippable or reorderable:

1. **Resolve the authority.** Query `approval_authorities` for `organization_id = target_organization_id AND authority_name = authority_name AND status = 'ACTIVE'`. Zero rows → deny, `NO_AUTHORITY_CONFIGURED`. A `SUPERSEDED`/`DEPRECATED`/`RETIRED` row is not considered a match at this step (only `ACTIVE` rows are queried) — if the only matching row for the name is non-`ACTIVE`, this is reported as `INACTIVE_AUTHORITY`, not `NO_AUTHORITY_CONFIGURED`, mirroring the original `§10` step 1's own distinction, now made an explicit, separately-checked condition rather than folded into one step.
2. **Validate configuration.** Inspect the resolved row's own structural well-formedness for its declared `approval_strategy` (e.g., `MAJORITY`/`ALL`/`SEQUENTIAL` declared without a value `majority_threshold_pct` would structurally require, where applicable — not currently prevented by any `CheckConstraint`, §4.1, unchanged finding). Malformed → deny, `INVALID_CONFIGURATION`. **This check occurs before any caller-specific step and before the strategy-support check (29.2.3) — it cannot be bypassed by a qualifying Membership binding, correcting the original step 6's own unwired ordering.**
3. **Inspect `approval_strategy` — the new gate.** If `approval_strategy != 'ANY_ONE'`: deny, `UNSUPPORTED_STRATEGY`. **This is the corrected design's own central addition.** `ALL`/`MAJORITY`/`SEQUENTIAL` remain exactly as undesigned and unresolved as `§9` already states — this gate does not design their resolution; it makes the existing, already-decided `ANY_ONE`-only scope boundary (`§9`, `§24`) structurally enforced rather than merely asserted in prose. No semantics for `ALL`/`MAJORITY`/`SEQUENTIAL` are invented by this gate — it denies, it does not attempt to resolve them.
4. **Organization mismatch.** (Unchanged in substance from original `§10` step 2, renumbered.) The caller's own claimed `organization_id` must equal `target_organization_id`. Mismatch → deny, `INVALID_SCOPE`.
5. **Eligible actor / missing binding.** (Unchanged in substance from original `§10` step 3, renumbered.) Query `membership_approval_authority` for a currently-effective row binding `caller_membership_id` to the resolved authority. Zero rows → deny, `NO_ELIGIBLE_ACTOR`.
6. **Active/inactive actor.** (Unchanged in substance from original `§10` step 4, renumbered.) The caller's own Membership must itself be currently valid (`membership_status = 'ACTIVE'`, effective window covers "now"). Not valid → deny, `INACTIVE_MEMBERSHIP`.
7. **Multiple bindings — not an error, now correctly scoped.** Since step 3 already excludes every non-`ANY_ONE` row, this step is reached only for `ANY_ONE` rows: any one qualifying binding (steps 4–6 all satisfied) is sufficient; additional bindings beyond the first are surplus, not an error, and never trigger `ALL`/`MAJORITY`/`SEQUENTIAL`-shaped counting, since those rows were already denied at step 3.
8. **`AUTHORIZED`.** Reached only when steps 1–7 all pass — not steps 1–4 as the original `§11` incorrectly stated.

**29.3 Corrected Fail-Closed Behavior (supersedes `§11`).** Every branch at `§29.2` above denies by default; only the single, fully-satisfied path — an `ACTIVE`, well-formed, `ANY_ONE`-strategy authority (steps 1–3), matched Organization (step 4), an eligible current binding (step 5), and a valid Membership (step 6) — authorizes (step 8). No branch simulates, infers, or defaults an outcome; this restates `§11`'s own original principle, now true of the algorithm as actually specified, not merely asserted of it. No `PLATFORM_ADMIN`/`AUREX_ADMIN` fallback exists at any branch, unchanged from `§11`.

**29.4 Corrected Runtime Contract reason taxonomy (supersedes `§20`'s seven-label list — adds one label, changes no other).** Eight labels, still documentation/diagnostic content for the `reason` string, still not a competing enum (`§20`'s own reuse-over-invention discipline, unchanged):

- `NO_AUTHORITY_CONFIGURED` — no `ACTIVE` row for the Organization/name (step 1).
- `INACTIVE_AUTHORITY` — a row exists but is `SUPERSEDED`/`DEPRECATED`/`RETIRED` (step 1).
- `INVALID_CONFIGURATION` — structurally malformed authority row (step 2).
- **`UNSUPPORTED_STRATEGY` (new) — `approval_strategy` is not `ANY_ONE` (step 3).**
- `INVALID_SCOPE` — caller's Organization does not match the target (step 4).
- `NO_ELIGIBLE_ACTOR` — no currently-effective binding for this caller (step 5).
- `INACTIVE_MEMBERSHIP` — the caller's Membership is not currently valid (step 6).
- `AUTHORIZED` — all conditions satisfied (step 8, the sole `ALLOW` path).

**29.5 `ALL`/`MAJORITY`/`SEQUENTIAL` remain unresolved — not silently implemented.** This amendment adds a gate that denies these strategies; it does not design, simulate, or approximate their eventual resolution. `§9`'s own disclosure stands exactly as before: their vote-counting/sequencing semantics are genuinely open, Category C, a future item (`§12`, `§26`), not resolved here or by this amendment.

**29.6 Corrected minimum test obligations (informative — no test is written by this document).** A future implementation must, at minimum, prove:
- `ANY_ONE` + one valid, currently-effective binding → `AUTHORIZED`.
- `MAJORITY` + one valid binding → `DENY` (`UNSUPPORTED_STRATEGY`), never `AUTHORIZED`.
- `ALL` + one valid binding → `DENY` (`UNSUPPORTED_STRATEGY`), never `AUTHORIZED`.
- `SEQUENTIAL` + one valid binding → `DENY` (`UNSUPPORTED_STRATEGY`), never `AUTHORIZED`.
- A malformed configuration (e.g., `MAJORITY` with a NULL threshold) → `DENY` (`INVALID_CONFIGURATION`), never reachable via a qualifying binding.
- Every other branch (`NO_AUTHORITY_CONFIGURED`, `INACTIVE_AUTHORITY`, `INVALID_SCOPE`, `NO_ELIGIBLE_ACTOR`, `INACTIVE_MEMBERSHIP`) as already named at `§20`/`29.4`.
These negative tests establish only that unsupported strategies and malformed rows cannot accidentally authorize — they do not, and must not, define how `ALL`/`MAJORITY`/`SEQUENTIAL` would eventually operate (`29.5`).

**29.7 C-023 impact — none.** `IRA-C023 §19.13` Decision 1 (Option B — Reuse the Existing Approval Authority Mechanism) is not reopened, altered, or reinterpreted by this amendment. This amendment corrects the mechanism's own internal resolver logic; it does not touch which mechanism was selected, C-023's own scope, or any of Decisions 1–6. **C-023 remains RED — Not Implementation Ready. `WP-17` remains CHARTERED — implementation not yet complete, not yet certified.**

**29.8 Everything else, explicitly unaffected by this amendment:** `membership_approval_authority`'s own design (`§5`–`§7`, `§19`); the Organization-scoping model (`§18`); the `AuthorityHolder` distinction (`§14`); the Group exclusion (`§15`); the Option A/B integration recommendation (`§12` — Option B remains the near-term recommendation, unchanged, still not a decision); the audit model (`§21`); the migration/compatibility analysis (`§23`); `TDS-018`'s own C-003 ownership; `WP-18`'s own scope (not itself edited by this amendment — see `§29.9`).

**29.9 Note on `WP-18`'s own charter — alignment subsequently completed (updated).** This section originally disclosed, without correcting, that `WP-18_C003_BA-XX_Approval_Authority_Runtime_Binding_Business_Activity_Charter.md §7`/`§13` restated the original, now-superseded `§10`/`§11`/`§20` algorithm "verbatim, not reinterpreted," and recommended that the charter's own restatement be brought into alignment with `§29.2`–`§29.4` in a future, separate pass, before implementation begins against it. **That alignment has since been completed, in a separate, subsequent governance pass:** `WP-18`'s own `§7`, `§13`, and `§18` now cite and restate the current, authoritative `§29.2`/`§29.3`/`§29.4`/`§29.6` algorithm — configuration validation and the `approval_strategy` gate both preceding any caller-specific check, the eight-label reason taxonomy including `UNSUPPORTED_STRATEGY`, and the corresponding test obligations — and `WP-18`'s own Change Control section records that alignment pass explicitly. **The alignment gap this section originally named is therefore CLOSED as a traceability matter.** This update to `§29.9` is documentation-only: it does not alter `§29.2`'s own resolver algorithm and does not imply `WP-18` is certified. ~~It does not imply the underlying Approval Authority runtime mechanism has been implemented, and does not imply `WP-18` is certified or implementation-authorized — `WP-18` remains **CHARTERED — IMPLEMENTATION NOT YET AUTHORIZED, NOT YET COMPLETE, NOT CERTIFIED**, unchanged by this correction.~~

**Superseded 2026-08-29 (Gate 1 M-1 governance-traceability reconciliation — see §31 below).** The struck-through clause immediately above was accurate on the date `§29.9` was written, but is no longer accurate and is preserved only as the historical record. Since it was written, the Repository Owner has explicitly granted Implementation Authorization for WP-18 (2026-08-29), and implementation against this design has been completed — both recorded in full in `IMP-REPORT-WP-18_Approval_Authority_Runtime_Binding.md §1`/`§2`, and reflected consistently in the `WP-18` charter header and the `WPR-001` WP-18 row. **The current, accurate status is: WP-18 — IMPLEMENTATION AUTHORIZED (by the Repository Owner, recorded in `IMP-REPORT-WP-18`, not by this document); IMPLEMENTATION COMPLETE; NOT YET CERTIFIED.** No `CLAUDE.md §19.7b` gate has yet passed. See §31.

**No implementation, code, schema, migration, model, repository, service, resolver, or test was created or modified by this amendment.**

---

## 30. Independent Review of the Amendment

**Dispatched as a genuinely independent, fresh-context review, no access to the drafting session's own conversation.** The reviewer traced the exact failure scenario the original defect described through the corrected algorithm step by step, rather than trusting `§29`'s own claims.

**False-`ALLOW` defect: CONFIRMED ELIMINATED.** The reviewer's own trace: a `MAJORITY`-configured row with one valid, currently-effective binding for the caller reaches step 3 (*"Inspect `approval_strategy`"*) — `MAJORITY != 'ANY_ONE'` — and **terminates there with `DENY`/`UNSUPPORTED_STRATEGY`, before step 4 (Organization match) or step 5 (binding eligibility) are ever evaluated.** The caller's own valid binding is never consulted. The reviewer independently re-confirmed the original `§10`/`§11` (six steps, no strategy check; *"only... steps 1–4 all pass... authorizes"*, steps 1–4 containing no strategy check) would have let this exact scenario reach `AUTHORIZED`.

**Malformed-configuration ordering fix: CONFIRMED CORRECT.** Traced a `MAJORITY`-with-NULL-threshold row: step 2 (*"Validate configuration"*) denies with `INVALID_CONFIGURATION` before step 3 or any caller-specific step — the reviewer confirmed this ordering is explicitly stated in `§29.2`'s own text, not merely implied, and directly fixes the original step 6's unwired-ordering flaw (confirmed against the original `§10`/`§11`, which never referenced step 6 in `§11`'s own gating statement).

**`ALL`/`MAJORITY`/`SEQUENTIAL`: CONFIRMED still genuinely unresolved, not silently implemented.** No vote-counting or sequencing semantics are defined anywhere in `§29`; `§29.5`'s own disclaimer ("adds a gate that denies these strategies; it does not design, simulate, or approximate their eventual resolution") was independently verified accurate, and `§9` (re-read directly, unchanged) still states these are "genuinely open... not resolved or invented here" with no contradiction from `§29`.

**No material defect found.** Independently confirmed: `IRA-C023 §19.13` Decision 1 is accurately characterized and untouched; a repository-wide grep for `UNSUPPORTED_STRATEGY`, `membership_approval_authority`, `ApprovalAuthorityResolver`, `require_approval_authority` found zero new implementation anywhere in `Backend/` (`ApprovalAuthorityResolver` independently re-confirmed still an uninstantiable abstract stub); `git status` confirmed only `TDS-018...md` carries new content from this pass; `§29.9`'s own disclosure about `WP-18`'s charter was independently verified accurate — the charter's own `§7`/`§13` were read directly and confirmed to still restate exactly the old seven-condition/seven-label design, genuinely needing the disclosed future alignment pass; `§12` (Option A/B) and `§21` (audit model) were spot-checked and confirmed unaffected, still reading exactly as before; no unrelated editorial change was found in Decision 6, C-023 scope, the migration model, or the audit model.

**Non-material observations:** `§30` was confirmed a genuine, previously-unfilled placeholder before this review, not pre-populated with fabricated findings; `TDS-018` has never been committed, so file-level `git diff` isolation relies on content inspection rather than commit history — a lifecycle artifact of this document, not a defect of the amendment.

**Overall verdict, quoted:** *"The amendment is sound — the corrected 8-step algorithm in §29.2 genuinely eliminates the original false-`ALLOW` defect... and the malformed-configuration bypass... without expanding scope into `ALL`/`MAJORITY`/`SEQUENTIAL` resolution semantics, without reopening any `IRA-C023` decision, and without any implementation side effect anywhere in `Backend/`."*

---

## 31. Amendment — Gate 1 M-1 Governance-Traceability Reconciliation (Status Synchronization Only)

**Provenance note, mirroring `§29`'s own convention and `TDS-017 §21`'s.** This section records a **narrow governance-documentation correction** to this document's own status statements only. `§§1–30` above — including `§29.2`'s corrected resolver algorithm, `§29.3` fail-closed behavior, `§29.4` reason taxonomy, `§29.6` test obligations, `§24` governance classifications, and every `IRA-C023` characterization — are **not altered by this section in any way**. No resolver logic, no design decision, and no C-023 decision is touched.

**31.1 The finding this section closes.** A fresh, independent Gate 1 Independent Certification review of WP-18 returned **NOT CERTIFIED** on a single material governance-traceability defect ("M-1"): this document still carried stale, present-tense statements that WP-18 implementation was *"NOT YET AUTHORIZED, NOT YET COMPLETE"* —

- the original header **Status** line (*"Technical Design — implementation NOT authorized…"*), and
- `§29.9`'s closing clause (*"…`WP-18` remains **CHARTERED — IMPLEMENTATION NOT YET AUTHORIZED, NOT YET COMPLETE, NOT CERTIFIED**…"*)

— while the `WP-18` charter, `WPR-001`'s WP-18 row, and `IMP-REPORT-WP-18` had already been reconciled to the actual repository state. The Gate 1 reviewer found **no code, security, resolver-ordering, tenant-isolation, migration, or scope-containment defect** — the implementation itself passed Gate 1's technical and security review (853/853 regression independently reproduced; every negative control — `MAJORITY`/`ALL`/`SEQUENTIAL` → `UNSUPPORTED_STRATEGY`, malformed → `INVALID_CONFIGURATION`, cross-Organization → denied, no admin bypass — independently confirmed). The defect was **solely** the un-synchronized status wording in this document.

**31.2 What this section corrects.** Using the strikethrough-preserve convention (nothing erased):

- The header **Status** line is preserved as *"Status (as originally issued …)"* with its original text struck through, and a new *"Status (current — updated 2026-08-29 …)"* block added, stating that this remains a **governing Technical Design** that never itself granted authorization; that the Repository Owner has **since separately and explicitly granted Implementation Authorization for WP-18 on 2026-08-29** and implementation has been **completed**, both recorded in `IMP-REPORT-WP-18 §1`/`§2` and reflected in the charter and `WPR-001`; and that **WP-18 remains NOT YET CERTIFIED**.
- `§29.9`'s closing clause is preserved struck-through, with a *"Superseded 2026-08-29"* note giving the same corrected status.

**31.3 Current, accurate governing-document chain (for the avoidance of doubt).**

| Artifact | Records |
|---|---|
| `TDS-018` (this document) | Governing Technical Design; `§29.2` resolver algorithm is authoritative. Implementation Authorization was **not** granted by this document — it was granted by the Repository Owner on **2026-08-29** and is recorded in `IMP-REPORT-WP-18`. Implementation is **complete**. **WP-18 NOT YET CERTIFIED.** |
| `WP-18` charter | CHARTERED — IMPLEMENTATION AUTHORIZED / IMPLEMENTATION COMPLETE / NOT YET CERTIFIED. |
| `IMP-REPORT-WP-18` | RO Implementation Authorization recorded verbatim (2026-08-29); IMPLEMENTATION COMPLETE; explicitly does **not** constitute certification. |
| `WPR-001` WP-18 row | IMPLEMENTATION AUTHORIZED / IMPLEMENTATION COMPLETE / NOT YET CERTIFIED. |

**31.4 Explicitly NOT done by this section.** No new Repository Owner decision is made or implied (the authorization it points to already exists, in `IMP-REPORT-WP-18 §1`). This section does not certify WP-18, does not authorize anything, does not re-dispatch Gate 1, does not alter `§29.2`–`§29.6` or `§24`, does not reopen or modify any `IRA-C023` decision, and does not touch `WP-18`, `WPR-001`, `IMP-REPORT-WP-18`, `IRA-C023`, `TDS-C023`, `WP-17`, or any `Backend/` file. **C-023 remains 🔴 RED — Not Implementation Ready. `WP-17` remains CHARTERED — implementation not yet complete, not yet certified.** Nothing was staged, committed, or pushed.

---

## Change Control

**Files created:** `architecture/05-Implementation/TDS-018_C003_Approval_Authority_Runtime_Binding_Technical_Design.md` (this document, new; amended once — `§29`/`§30` appended, correcting `§10`/`§11`/`§20`'s own resolver algorithm; `§10`/`§11`/`§20` themselves preserved unchanged as the historical record, with forward-pointing supersession notes added).

**Status-synchronization pass (2026-08-29, Gate 1 M-1 governance-traceability reconciliation):** this document only. Three edits, strikethrough-preserve, nothing erased: (1) the header **Status** line — original struck through, a *"Status (current — updated 2026-08-29 …)"* block added; (2) `§29.9`'s closing clause — struck through, a *"Superseded 2026-08-29"* note added; (3) `§31` appended, recording the reconciliation in full. Purpose: bring this document's own status statements into agreement with the already-recorded Repository Owner Implementation Authorization (2026-08-29, `IMP-REPORT-WP-18 §1`) and completed implementation, so that no governing artifact still falsely states WP-18 implementation is unauthorized or incomplete. **`§29.2`'s resolver algorithm, `§29.3`/`§29.4`/`§29.6`, `§24`'s governance classifications, and every `IRA-C023` characterization were NOT changed.** No new Repository Owner decision was made or implied; no certification is claimed or implied; Gate 1 is not re-dispatched by this pass. `WP-18`, `WPR-001`, `IMP-REPORT-WP-18`, `IRA-C023`, `TDS-C023`, `WP-17`, and every `Backend/` file were read for cross-reference, not modified.

**Files modified:** none other. `Master_Technical_Architecture.md`, `approval_authority.py`, `approval_authority_repository.py`, `approval_authority_service.py`, `membership.py`, `authority_holder.py`, `dependencies.py`, `Backend/Runtime/AuthorizationEngine/authorization/{engine,models,tier_resolvers}.py`, `TDS-017`, `IRA-C023`, `TDS-C023`, `WP-17_C023_BA-01...md`, `WP-18_C003_BA-XX_...md`, `WPR-001`, `URA-001` were read, not modified, in preparing this amendment.
**No production code, schema, migration, router, service, repository, model, resolver, or test was created or modified. No `membership_approval_authority` row was created. No authority holder was created or modified. No Group infrastructure was created. No Repository Owner decision was made. No new ADR was created. No `IRA-C023` decision was reopened.** **C-023 remains RED — Not Implementation Ready. `WP-17` remains CHARTERED — implementation not yet complete, not yet certified. C-040/`WP-16` and `AI-002`/`TD-157` are untouched by this document.**
