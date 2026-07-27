# AMD-014 — Domain Business Object: Architecture Completion Amendment

**Type:** Architecture Completion Amendment (not an Architecture Decision Record — no competing architectural alternative exists; see §1)
**Status:** Architecture completion required. Purely architectural — establishes that completion is required and where; does not perform it.
**Scope:** This amendment does not design a schema, does not invent columns, does not produce SQL, and does not give implementation guidance. Implementation occurs later, after the architecture named in §4 is completed, following this repository's normal Reuse → Configure → Extend → Compose → Create discipline at that time.
**Trigger:** Discovered during WP-02 (Role & Permission Management) BA-02 readiness analysis, when EX-C003-02's Entry Context ("the target Domain, already established") could not be traced to any actual entity in Master Technical Architecture.

---

## 1. Why an ADR Does Not Apply

An Architecture Decision Record exists to record a deliberate choice between competing architectural alternatives. This amendment records the opposite finding: no such choice was ever made. Domain — the business object URA-001 §4 defines (Finance, HR, Risk, Supply Chain, Cyber Security, Legal, Business Resilience, and organization-added equivalents) — has no registry anywhere in Master Technical Architecture, and no document anywhere states this as a deliberate omission. There is nothing to decide between; there is a gap to close. An amendment, not a decision record, is the correct instrument.

## 2. Why `domain_registry` Is a Missing Architectural Element

The determination that this is a completion gap, not a design choice, rests on convergent evidence already independently verified against the primary sources:

1. **The amendment that introduced the surrounding tables enumerates every URA-001 rule cluster it covered — and Domain-the-entity is the one cluster it silently skipped.** Master Technical Architecture's own AMD-011 CHANGELOG lists, one line per new table, exactly which URA-001 rule each realizes: URA-001-29 → `system_role_registry`, URA-001-38/40 → `business_role_registry`, URA-001-57/59 → `group_registry`, URA-001-47 → `domain_permission_registry`. URA-001-43/44/45/46 — the rules defining Domain itself, its hierarchy, and its owners/admins — appear nowhere in that list, even though every adjacent rule cluster in the same Section range produced a registry.
2. **The immediately preceding sibling table proves the necessary modeling pattern was available and in active use, one line earlier.** `group_registry` (built directly before `domain_permission_registry`, in the same amendment) already models self-referencing hierarchy: `parent_group_id UUID REFERENCES group_registry(group_id)`. URA-001-44 ("Domain Hierarchies Shall Be Supported") requires the identical pattern. The author had the tool in hand and used it for the adjacent concept, not for this one.
3. **`domain_permission_registry`'s own FK declaration is silently incomplete**, breaking a convention this document otherwise applies without exception. Its header comment states `FK: membership_id -> membership_registry` — one relationship — while the table body declares a second FK-shaped column, `domain_id UUID, -- references domain object (Finance, HR, Risk, etc.)`, with no `REFERENCES` clause and no corresponding entry in the FK line.
4. **No instance of this document's own "flagged, not silently resolved" convention exists for Domain.** Elsewhere, deliberate omissions are marked explicitly and consistently — "ASSUMPTION (flagged, not silently resolved)," "deliberately left configurable, not fixed," "a stated design choice, not an oversight" — each tied to a numbered Assumption a later amendment can cite back to ("AMD-011 Assumptions 1-6"). No assumption number, flag, or explanatory sentence exists anywhere for Domain or `domain_id`, and a direct search of the document for "known gap," "not yet modeled," or "domain...pending" returns nothing.
5. **Ownership notes are silent, not dismissive.** The Component/Service Ownership section names no service as owning, or explicitly excluding, Domain.

Each of these was independently verifiable before this amendment was drafted; none is asserted without the corresponding primary-source citation above.

## 3. Traceability

| Source | What it establishes | Status |
|---|---|---|
| **URA-001 §4** (URA-001-43 through URA-001-56) | Defines Domain as a first-class business object: organization-extensible (URA-001-43), hierarchical with configurable inheritance (URA-001-44), owned by a Domain Owner (URA-001-45) and administered by a Domain Admin (URA-001-46), the anchor for standing Domain Permissions (URA-001-47/48), and effective-dated (URA-001-53). This is the constitutional authority for Domain's existence and rules. **Complete — no change needed here.** |
| **Master Technical Architecture, `domain_permission_registry`** | Physically realizes URA-001-47 (the permission grant) and explicitly names its anchor: `domain_id UUID, -- references domain object (Finance, HR, Risk, etc.)`. This is the consuming table whose declared dependency is currently unfulfilled. |
| **Master Technical Architecture, `business_role_registry`** | The nearest existing registry to what Domain's own entity table would resemble in kind — tenant-extensible via a nullable `organization_id` (NULL = global default, set = tenant-specific), a plain descriptive name, and no complex lifecycle machinery beyond effective-dating. Established in the prior review as the closest structural precedent, cited here only as traceability evidence, not as a schema proposal. |
| **Master Technical Architecture, AMD-011 CHANGELOG** | The amendment record that added `system_role_registry`, `business_role_registry`, `group_registry`, and `domain_permission_registry` together, in one pass through URA-001 §§3–5 — and the artifact in which Domain-the-entity's absence is visible as an omission from an otherwise-complete enumeration (§2.1 above). |

## 4. Architectural Intent

Domain, per URA-001 §4, is intended to be:

- A **first-class business object** in its own right (URA-001-43), not merely an attribute or enumerated value on another table.
- **Organization-extensible**: every organization inherits a platform-default set (Finance, HR, Risk, Supply Chain, Cyber Security, Legal, Business Resilience) and may add its own (URA-001-43).
- **Hierarchical**, supporting sub-domains with configurable inheritance and overrides (URA-001-44) — e.g., Finance containing Accounting, Treasury, Taxation.
- **Owned and administered** by named roles distinct from its permission-holders: a Domain Owner for business accountability, a Domain Admin for operational management (URA-001-45/46).
- The **standing authority anchor** that `domain_permission_registry` grants permission against, and that `node_permission_assignment`-style resolution (per ERG-001's own description) ultimately resolves into, ahead of URA-001-76's precedence chain.

Domain is not intended to be a competing authorization mechanism, a duplicate of ERG-001's EnterpriseNode/organizational hierarchy, or a redefinition of Organization (C-004). It is intended to be exactly what URA-001 §4 already describes: a governed, hierarchical business-ownership classification that Domain Permission anchors to. This amendment does not alter that intent; it exists because the intent was never carried through to a corresponding registry.

## 5. Documents Requiring Completion

| Document | What requires completion | Why |
|---|---|---|
| **Master Technical Architecture** | The missing Domain entity registry, and completion of `domain_permission_registry.domain_id`'s currently-absent foreign key once that registry exists. | This is the document where every sibling object in the same rule range (`system_role_registry`, `business_role_registry`, `group_registry`) already has its registry; Domain is the one exception. |
| **URA-001** | No rule content requires change — §4 is already complete and internally consistent (§3 above). Only its status as "fully realized in the physical schema" is currently inaccurate and should be reconciled once Master Technical Architecture is completed. | URA-001 defines the business rule correctly; the gap is entirely on the physical-realization side. |
| **PE-001-C003** | EX-C003-02's Entry Context — *"the target Domain (already established, C-004/URA-001 Section 4)"* — currently cites an entity that has no physical registry to be "already established" in. Once Master Technical Architecture is completed, this citation becomes accurate as written; until then, it describes a precondition the schema cannot yet fulfill. | This is the capability specification whose Business Activity (BA-02) depends on Domain existing as queryable data. |
| **MDP-001** | Once a Domain registry exists, MDP-001's seed-population inventory will need a corresponding entry for it (the platform-default domain set URA-001-43 names), mirroring how `system_role_registry`'s five fixed rows are already specified there. | MDP-001 is this repository's authority for which platform-seeded reference data gets populated at build time, and currently has no entry for Domain because no registry exists to populate. |

No other document was found to make a claim about Domain requiring reconciliation — CAP-001, ERG-001, CMD-001, and PE-001-C005 were each checked directly in the prior analysis and found either silent on this specific object or referring to an unrelated homonym of "Domain."

## 6. Status

**Architecture completion required.** This amendment establishes the gap, its evidence, and the documents it touches. It does not schedule, design, or authorize implementation. No schema has been proposed, no column invented, no SQL written, and no implementation guidance given. Completion of Master Technical Architecture (and the consequential updates to URA-001's realization status, PE-001-C003's citation, and MDP-001's seed inventory) is a separate, later architectural effort.
