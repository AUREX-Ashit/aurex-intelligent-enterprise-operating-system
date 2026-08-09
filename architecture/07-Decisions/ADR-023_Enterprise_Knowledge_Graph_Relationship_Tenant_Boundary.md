# ADR-023 — Enterprise Knowledge Graph Relationship Tenant Boundary

**Status:** Accepted
**Classification:** Architecture Governance / Data-Model Conformance (Multi-Tenancy)
**Decided by:** Repository owner (architecture governance authority), following a dedicated Architectural Decision Assessment (`enterprise_knowledge_graph_registry` tenant-boundary review, WP-14/BA-05, this session) — the same decision-authority pattern `ADR-016`/`ADR-019`/`ADR-020`–`022` already established.
**Affected Documents:** `Master_Technical_Architecture.md` (AMD-016, `enterprise_knowledge_graph_registry`'s own `CREATE TABLE`/RLS section) — amended alongside this ADR, not by it directly. `RTA-001 §12.9` (Relationship Resolution) — a one-sentence clarification, evaluated and applied alongside this ADR (see §5). `SD-002` is **not** amended — this decision conforms an existing physical table to a rule `SD-002` already states.
**Affected Code:** None. No migration, model, router, service, or test is created or modified by this ADR.

---

## 1. Context

`IRA-014_WP-14_Enterprise_Intelligence_Foundation_Implementation_Readiness_Assessment.md`'s own BA-05 (Synchronize Enterprise Knowledge Graph) was classified **C — STOP** during a focused authorization review: `enterprise_knowledge_graph_registry` (`Master_Technical_Architecture.md` AMD-012, LOCKED) carries no `organization_id`, no `domain_id`, and its own `source_entity_type`/`source_entity_id` and `target_entity_type`/`target_entity_id` are untyped polymorphic references with no declared foreign key. This is a tenant-isolation *representation* gap, not an authorization-persona gap — `PLATFORM_ADMIN` gates who may call an endpoint, not whether the underlying rows are safely scoped to one tenant.

A dedicated Architectural Decision Assessment then examined the repository's own existing constitutional evidence, tenant-boundary patterns, authorization precedents, sibling graph/entity models, and Domain-Event-triggered synchronization mechanics, and evaluated five candidate solutions before reaching the recommendation this ADR now formalizes.

## 2. Governing Constitutional Evidence

- **`SD-002-013` ("Universal Relationships and the Enterprise Knowledge Graph"):** *"Every object may participate in typed relationships... with any other object. Collectively, these relationships form Aurex's enterprise knowledge graph."* This is the constitutional definition `enterprise_knowledge_graph_registry` physically realizes — relationships are governed Business Objects, not exempt index rows.
- **`SD-002-108` ("Every Object Carries an Explicit Tenant Boundary"):** *"Every business object... carries an explicit, non-optional tenant identifier as part of its Universal Identity. An object with an ambiguous or inferred tenant boundary is an invalid object state, not an edge case to be resolved at query time."* This directly forecloses deriving tenant ownership only at query/runtime from the polymorphic entity references — the option this ADR rejects (§4).
- **`SD-002-109`** ("Company CIL and Workspace Objects Are Isolated by Construction"): *"Company-level and Workspace-level CIL objects (Sections 9) are isolated from every other tenant's objects at the data layer, not merely at the application or permissions layer."* Separately: *"isolation is a storage and retrieval guarantee, not solely an access-control feature."*
- **`SD-002-111`:** cross-tenant reference to another tenant's own Company-level object *"requires an explicit, named, audited cross-tenant sharing agreement — it is never a default or implicit capability."* No such mechanism exists in this repository today (the same disclosed gap `TD-040` already names for an unrelated capability) — cross-organization Knowledge Graph relationships are therefore correctly rejected by default, not silently permitted.

## 3. Why Query-Time/Transitive Tenant Inference Is Rejected

Deriving a relationship row's tenant ownership by resolving its polymorphic `source_entity_id`/`target_entity_id` against whichever table each happens to reference, at query or write time, without storing the result, is the literal shape `SD-002-108` names and prohibits ("not an edge case to be resolved at query time"). It is also, independently of the constitutional text, the same defect shape two prior, unrelated findings in this repository already confirmed in practice: `VV-AUDIT-WP-05`'s Finding F-02 (cross-tenant Approval Authority selection) and `WP-09`'s `TD-113` (cross-tenant Membership-status disclosure) — both produced by tenant scope being inferred rather than explicit. Rejected on both constitutional and empirical grounds, not preference.

## 4. Rejected Alternatives

| Option | Disposition | Reason |
|---|---|---|
| B — derive tenant ownership from source/target entities at query/runtime, no stored column | **Rejected** | Directly contradicts `SD-002-108`'s own text (§3); reproduces the `VV-AUDIT-WP-05`/`TD-113` defect shape |
| C — a new explicit graph/workspace/knowledge boundary object owning the relationship | **Rejected** | A new Business Object where an existing owner (Organization, via `SD-002-108`) already correctly owns the responsibility — fails the "no new concept unless an existing owner cannot correctly own it" test this repository already applies at every prior Work Package gate (`CLAUDE.md §19.5`, `ADR-014`'s own worked examples) |
| D — reuse `Domain`/`DomainPermission` (WP-13's Authorization Runtime), or `Workspace` (C-008) | **Rejected** | Category error — `Domain`/`DomainPermission` governs within-Organization delegation of authority, not which Organization owns a resource in the first place; no textual bridge exists anywhere in the repository connecting a Knowledge Graph relationship to a `domain_id`. `Workspace` is itself Organization-scoped and adds indirection with no isolation benefit over Organization directly |
| A-variant — a separate external "relationship → organization" index table, table itself left unchanged | **Rejected** | Still violates `SD-002-108`'s "as part of its Universal Identity" language (intrinsic to the object's own row) and `SD-002-109`'s data-layer guarantee (a bolt-on index still requires an application-level join) |

## 5. Approved Decision

1. **The tenant boundary of an Enterprise Knowledge Graph relationship is Organization** (`SD-002-108`/`SD-002-013`).
2. **`enterprise_knowledge_graph_registry` gains an explicit, nullable `organization_id`** (`Master_Technical_Architecture.md` AMD-016, amended alongside this ADR — see that document for the exact column/FK/index/RLS declaration).
3. **`organization_id` is never an independently asserted ownership claim.** It is derived from, and validated against, the authoritative ownership of the relationship's own two endpoints, per the following business rules:
   - **BR-1:** if both endpoints are Organization-scoped, their `organization_id` values MUST match; a mismatch MUST reject the relationship — never silently reconciled.
   - **BR-2:** if exactly one endpoint is Organization-scoped, the relationship inherits that endpoint's `organization_id`.
   - **BR-3:** if neither endpoint is Organization-scoped (both platform-wide/Global), `organization_id` remains `NULL`.
   - **BR-4:** cross-organization relationships are rejected unless and until an explicit, named, audited cross-tenant sharing mechanism exists (`SD-002-111`) — not built by this ADR, not authorized by it.
4. **Global objects remain legitimately usable in relationships** (BR-3) — this decision does not narrow what `metric_registry`'s own Global CDEs, Frameworks, or Regulations may participate in; it only makes the resulting relationship's own tenant scope explicit rather than absent.
5. **Authorization SHALL subsequently reuse the existing tenant-boundary enforcement pattern already certified at `WP-10`** (`require_matching_tenant_or_platform_admin`/`PLATFORM_ADMIN`) once the column exists. **WP-13's Authorization Runtime Engine (`enforce_domain_permission`, the ADMIN-level DomainPermission grant mechanism) is explicitly NOT used for this purpose** — this is an Organization-boundary question, not a within-Organization Domain-delegation question (§4, Option D).
6. **`RTA-001 §12.7`/`§12.9`** — evaluated for whether a clarification is genuinely necessary (§7, below), applied in the same governance pass as this ADR if so, without redesigning the Knowledge Graph Runtime.

## 6. This ADR Is NOT

- **Not a new Business Object, capability, or persona.** It conforms an existing, already-registered physical table to a rule `SD-002` already states; no `CMD-001 §26.3a` eligibility question arises (a relationship row does not become a newly-eligible independent Business Object by gaining a tenant-boundary column — it already is one, per `SD-002-013`).
- **Not a new authorization mechanism.** §5 item 5 reuses an already-certified pattern; it does not invent one.
- **Not an authorization to implement BA-05.** This ADR resolves the architectural question `IRA-014`'s own Classification C raised. It does not itself authorize Technical Design or implementation — `IRA-014` must still be amended (§9), and a subsequent, separate "WP-14 Implementation Authorization" instruction (the same two-step chartering-then-authorization precedent `WP-10`/`WP-11`/`WP-12` each established) remains required before any Business Activity code is written.
- **Not a decision about `cross_domain_relationship_registry`.** That table shares the identical polymorphic, no-`organization_id` shape (`Master_Technical_Architecture.md`, adjacent to `enterprise_knowledge_graph_registry` in the same document) but is explicitly out of scope for this ADR and for BA-05 — named here as a related, disclosed, **future** concern, not resolved or silently extended to by this decision.

## 7. RTA-001 Disposition

Evaluated directly against `§12.7` (Graph Synchronization Pipeline) and `§12.9` (Relationship Resolution): neither currently states or precludes a tenant-boundary validation step — a genuine silence, not a conflict, but one this ADR's own BR-1/BR-2/BR-3 need a citable runtime home in. A minimal, one-sentence clarification is applied to `§12.9` alongside this ADR (see `RTA-001`'s own amendment record) rather than left as an `AMD-016`-only fact with no Runtime-layer acknowledgment — the Knowledge Graph Runtime itself is not redesigned.

## 8. Consequences

- `IRA-014`'s own BA-05 (§6, §11, §17) is amended, in a subsequent, separate action, to reflect this decision: Classification C → B, with Technical Design (not immediate implementation) as the next gate.
- `Master_Technical_Architecture.md` gains AMD-016, documenting the column/FK/index/RLS declaration and BR-1–BR-4 as architecture notation, consistent with how AMD-004/005/012/013 each documented their own additions. No Alembic migration is created by this ADR or its accompanying AMD.
- `cross_domain_relationship_registry`'s own identical gap remains open, disclosed, out of scope.
- No code, test, migration, or IRA-014 change is performed by this ADR itself — each is a separate, subsequent action in the same governance pass, per the Repository Owner's own phased instruction.

## 9. Status

**Accepted.**
