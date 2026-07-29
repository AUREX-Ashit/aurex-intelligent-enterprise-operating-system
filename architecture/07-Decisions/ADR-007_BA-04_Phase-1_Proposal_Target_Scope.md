# ADR-007 — BA-04 Phase-1 Implementation Scope: EnterpriseNode-Only Structural Proposals

**Status:** Accepted
**Classification:** Architecture Governance / Implementation Scope
**Decided by:** Repository owner (architecture governance authority), during WP-04's own BA-04 readiness assessment — the same decision-authority pattern ADR-004/005/006 already established during a Work Package's own readiness-assessment review.
**Affected Documents:** `architecture/05-Implementation/IRA-004_WP-04_Enterprise_Structure_Management_Implementation_Readiness_Assessment.md` (§4 BA-04 candidate row and §10 gap-analysis disposition updated to reference this ADR) — no other document amended. **ERG-001 is not amended.** **IRA-004 §21 (SCI-000001's own CBOR registration entry) is not amended.**

---

## Context

The BA-04 readiness assessment (this Work Package's own prior turn) confirmed BA-04 ("Shape / Refine Proposed Structural Outcome", ERB-C005-04/EX-C005-05/-06) remained blocked at IRA-004 §4/§10's own recorded Category D: *"Depends on §4's disclosed ambiguity (which ERG-001 object a 'proposal' attaches to) — not resolved here."* ADR-006 (which registered SCI-000001) explicitly declined to resolve this: *"This ADR does not resolve BA-04's own disclosed ambiguity... Structural Change Intent's own `DERIVED_FROM` relationship to a specific ERG-001 object remains explicitly Pending Canonical Binding."*

The ambiguity: EX-C005-05's Produced Context ("Proposed Outcome Context") could, per PE-001-C005's own generic, target-agnostic experience text (§42.16: C-005's ERBs are "the reference for depth... not a content template to be mechanically duplicated"), be shaped against any of ERG-001's structural objects — EnterpriseNode, EnterpriseRelationship, or ConsolidationDetermination. Of these three, only **EnterpriseNode** (`organization_nodes`) exists in this repository today (WP-04 BA-01/BA-02). **EnterpriseRelationship** (`organization_hierarchy`) and **ConsolidationDetermination** do not exist anywhere — confirmed by direct grep, zero matches beyond comments/docstrings noting their future, not-yet-built status (IRA-004 §7).

This is distinct in kind from the question ADR-006 resolved. ADR-006 answered a *constitutional* question (does Structural Change Intent qualify for CBOR registration at all) using a test independent of any table (SD-002 §2). This ADR answers a *scope-phasing* question — which of several already-canonical ERG-001 targets a first implementation slice of BA-04 supports — the same class of decision ADR-004 already made for WP-01's own `organizations`/`organization_master` column scope, and IRA-004 §9 made for BA-01's own Structural Identity column subset.

## Analysis

**Is narrowing BA-04 v1 to EnterpriseNode-only proposals constitutionally valid?** Tested against CLAUDE.md §18/§19.4's prohibition on introducing new entities/tables/APIs/service boundaries/business rules without approval:

- No new entity is introduced. EnterpriseNode, EnterpriseRelationship, and ConsolidationDetermination are all **already** canonically specified in ERG-001 (§5, §7, §9) — none is invented by this decision, and none is redefined, removed, or narrowed *within ERG-001 itself*. ERG-001 remains entirely unamended.
- No new business rule is invented. BR-C005-003 (current structural context SHALL remain distinguishable from Proposed Outcome Context) and BR-C005-004 (traceability to the originating Change Intent) apply identically regardless of which ERG-001 object a proposal targets — this decision does not touch either rule's substance.
- SCI-000001's own CBOR registration (IRA-004 §21) is not touched. Its `DERIVED_FROM` relationship was already recorded as generic/Pending Canonical Binding — this decision does not resolve, bind, or narrow that relationship; it only decides what BA-04's own **first implementation slice** supports, which is a distinct question from what SCI-000001 itself is permitted to relate to.
- This mirrors ADR-004's own precedent exactly (deliberately implement a validated subset of an already-canonical shape now, defer the rest as a known, tracked gap, not a silent omission) and IRA-004 §9's identical disposition for BA-01's own column subset — an established, already-accepted engineering discipline in this repository, not a novel exception carved out for BA-04.

**Conclusion: constitutionally valid.** This is an implementation-phasing decision, not an architectural one. It requires an ADR (rather than a disclosed IRA note alone) only because IRA-004 §10 itself already classified the underlying ambiguity as Category D ("governance clarification required"), the same threshold ADR-006 crossed for BA-03 — not because the decision itself redefines any canonical concept.

## Decision

1. **BA-04 Version 1 is intentionally scoped to EnterpriseNode-targeted structural proposals only.** A Proposed Outcome Context shaped by BA-04 v1 (EX-C005-05/-06) references an existing `organization_nodes` row as its structural target.
2. **This is explicitly a phased implementation decision, not an architectural one.** ERG-001's own definition of EnterpriseNode, EnterpriseRelationship, and ConsolidationDetermination is unchanged; this ADR scopes BA-04's first implementation slice against ERG-001, it does not redefine ERG-001 (the identical relationship ADR-004 already established between WP-01's implementation scope and Master Technical Architecture's canonical `organization_master`).
3. **EnterpriseRelationship-targeted and ConsolidationDetermination-targeted proposal types remain deferred**, not eliminated — real, tracked, future work, blocked only on their own respective ERG-001 objects being built (`organization_hierarchy`: BA-08 candidate per IRA-004 §4; ConsolidationDetermination: no candidate BA assigned yet). Each requires its own future implementation-readiness gap analysis before being added to BA-04's scope, per CLAUDE.md §19.7 — not authorized by this ADR.
4. **SCI-000001 remains generic and is not permanently bound to EnterpriseNode.** IRA-004 §21's own registration entry (`DERIVED_FROM` → EnterpriseNode/EnterpriseRelationship, Pending Canonical Binding) is unchanged by this ADR. A Structural Change Intent framed by BA-03 carries no target-type commitment of its own; BA-04 v1's own EnterpriseNode-only scope is a property of BA-04's implementation, not of SCI-000001's own definition.
5. **Future Business Activities may extend the proposal target without invalidating BA-04 v1.** When EnterpriseRelationship or ConsolidationDetermination proposal support is later added (by a future BA-04 extension or a distinct future Business Activity), no BA-04 v1 data, endpoint, or business rule requires retraction or redefinition — the extension is strictly additive, the same additive-extension discipline ADR-004's own Consequences section already pre-authorizes for `organizations`.

## Rationale

Building proposal-target support for EnterpriseRelationship and ConsolidationDetermination now would require inventing schema for two objects (`organization_hierarchy`, `consolidation_determination`) that do not yet exist and have no current owning Business Activity — exactly the speculative, premature schema design ADR-004's own Rationale already rejected for WP-01. Scoping BA-04 v1 to the one ERG-001 object that already exists (EnterpriseNode) lets BA-04 proceed on validated ground, consistent with CLAUDE.md §19.5's Reuse → Configure → Extend → Compose → Create discipline, while leaving the door open — explicitly, not by silent omission — for the other two target types once their own owning Business Activities (BA-08 candidate and beyond) build the objects they require.

## Consequences

- BA-04's own future implementation-readiness gap analysis may now proceed against a resolved scope question — the target-type ambiguity is no longer Category D. This ADR does not itself authorize BA-04's implementation; a fresh gap analysis (persistence mechanism, endpoint shape, service/repository design, and the item disclosed below) remains required per CLAUDE.md §19.7.
- IRA-004 §4 (BA-04 candidate row) and §10 (gap-analysis disposition) are updated to reference this ADR and record the EnterpriseNode-only v1 scope. IRA-004 §21 (SCI-000001's own registration) is **not** amended.
- **Disclosed, not resolved by this ADR:** whether "Proposed Outcome Context" (the object BA-04 itself would create) is, by the same SD-002 §2 Cross-Experience Reference Test used to register SCI-000001, itself a canonical Business Object requiring its own CBOR registration before implementation — EX-C005-05's Produced Context is plausibly consumed by name at BA-05 (EX-C005-07), BA-06 (EX-C005-08/-09), and BA-07 (EX-C005-10), the same cross-Business-Activity reference pattern that triggered SCI-000001's own registration. This ADR resolves only the target-type scope question; it does not perform that eligibility test. BA-04's own future gap analysis must address this before implementation, not assume it away.
- No existing table, model, service, or API is modified by this ADR. No implementation, schema, migration, or code exists or is authorized as a result of it.

## Status

**Accepted**
