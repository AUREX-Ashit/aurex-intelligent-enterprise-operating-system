# ADR-001 — Canonical Authority Alignment for CAP-001 and PE-001

**Status:** Accepted
**Classification:** Architecture Governance
**Affected Documents:** CAP-001 (Enterprise Capability Registry), ARCH-000 (Enterprise Operating System Architecture Manifest)

---

## Context

A repository architecture-orientation and authority-resolution review identified the following facts, drawn only from canonical documents already present in this repository:

1. **CAP-001** (`architecture/02-Constitutional/CAP-001_Enterprise_Capability_Registry.docx`) assigns capability **C-006 — Person Management** ("Manage enterprise persons.") a Primary Specification of **ERG-001**.
2. **URA-001** (`architecture/02-Constitutional/URA-001 - User, Role, Permission, Event and ssignment.md`), Section 2, is the sole canonical treatment of the Person concept in the repository: URA-001-15 ("Person Is the Master Human Entity"), URA-001-16 (Identity), and URA-001-17/17a/17b (Organization Membership) define Person, Identity and Membership as a coherent, adjacent semantic group. CAP-001 already assigns the adjacent capabilities C-001 (Identity Management) and C-007 (Membership Management) to URA-001.
3. **ERG-001** (`architecture/02-Constitutional/ERG-001 Enterprise Structure & Relationship Management (ESRM).md`) defines exactly three canonical objects — EnterpriseNode, EnterpriseRelationship, EnterpriseView — and contains no definition of Person anywhere in its text. Its only connection to person-related data is the joint URA-001-17b / ERG-001-03 principle, which anchors a **Membership** (not a Person) to a `home_node_id` — a Membership-management and structural-placement concern, not a Person-identity concern.
4. **CLAUDE.md** Section 6 ("Enterprise Modeling Rules") states that Organization, Person, Identity, Membership, Role and Permission are canonical concepts that "must remain independent" and must never be merged or duplicated. Person sitting on ERG-001's Primary Specification while Identity and Membership sit on URA-001 breaks this stated grouping's internal consistency.
5. **PE-001** (`docs/Product/PE-001/PE-001_Enterprise_Experience_Blueprint.docx`) and **PE-001-C005** (`docs/Product/PE-001/capabilities/C-005/PE-001-C005_Enterprise_Structure_Management.docx`) both establish that capability identity and business intent are authoritatively sourced from **CAP-001**, and that a capability's structural/domain semantics are sourced from that capability's Primary Specification. PE-001-C005 states explicitly: *"CAP-001 remains authoritative for capability identity and business intent. ERG-001 remains authoritative for enterprise structure semantics and relationships... This specification does not redefine those concerns."* No equivalent PE-001-C006 exists yet, so this ADR establishes the correct Primary Specification before that engineering begins.
6. No embedded architecture decision in ERG-001 (AD-001 through AD-005), URA-001 (URA-001-01a, 17a, 17b, 31, 76, 94a, 108a, 123, 145, 150a), or PE-001 (ADR-PE-001-001 through 012) assigns or explains Person Management's placement on ERG-001. The current CAP-001 entry has no supporting rationale anywhere in the canonical document set — it is an unreconciled registry allocation, not a considered architectural decision.
7. Separately, **ARCH-000** (`architecture/00-Governance/ARCH-000 – Enterprise Operating System Architecture Manifest.md`), the designated authoritative entry point, has drifted from the current canonical repository model: it does not list CAP-001 anywhere; it marks PE-001 as *"(Under Development)"* although PE-001's own header declares itself a *"Canonical Enterprise Experience Specification"* with twelve frozen ADRs and a completed Gold Standard capability specification (PE-001-C005) built on it; it does not describe the PE-001-Cxxx capability-specification pattern; and it does not acknowledge EIA-001, which is cited as a locked, referenced companion authority by PE-001, PE-001-C005, and CAP-001 (as owner of capabilities C-090–C-095) but does not exist as an authored document anywhere in the repository.

## Decision

1. Correct **C-006 — Person Management**'s Primary Specification in CAP-001 from **ERG-001** to **URA-001**.
2. Retain **ERG-001** as a cross-specification dependency for C-006 wherever enterprise structural or relationship context is relevant (e.g., a person's placement within the Enterprise Relationship Graph via Membership), without altering CAP-001's registry meta-model to add a formal "Related Specification" field.
3. Recognize **CAP-001** as the canonical authority for capability identity, canonical capability name, and business intent across the Enterprise Operating System.
4. Recognize **PE-001** as the canonical Enterprise Experience foundation and methodology specification.
5. Recognize **PE-001-Cxxx** as the document model for capability-specific Enterprise Experience specifications, each conforming to PE-001's methodology while deriving capability identity and business intent from CAP-001.
6. Recognize **PE-001-C005** as the current Gold Standard reference for capability-level Enterprise Experience engineering quality and method — not as a content template for other capabilities.
7. Record **EIA-001** as a referenced canonical specification that is currently missing / not yet authored, so that ARCH-000 no longer silently omits a document other canonical specifications already depend on.
8. Correct the stale PE-001 status recorded in ARCH-000 to reflect PE-001's actual canonical state.

## Rationale

This decision is based exclusively on the canonical documents already present in this repository: CAP-001, URA-001, ERG-001, PE-001, PE-001-C005, CLAUDE.md, ARCHITECTURE.md, ARCH-000, and the architecture decisions embedded within URA-001 and ERG-001. No external or implementation-repository evidence was used to reach or support this decision.

C-006's business intent — "Manage enterprise persons" — is definitionally about the Person entity. URA-001 is the only canonical specification in this repository that defines Person, and it does so adjacent to Identity (C-001) and Membership (C-007), both of which CAP-001 already correctly assigns to URA-001. ERG-001 owns a structurally and semantically distinct concern (the Enterprise Relationship Graph: nodes, relationships, views) and defines no Person concept at all. Assigning C-006 to URA-001 aligns CAP-001 with the substantive content of the specifications it references, aligns C-006 with its immediately adjacent capabilities C-001 and C-007, and satisfies CLAUDE.md's requirement that Person, Identity, and Membership remain independently but consistently modeled canonical concepts. ERG-001 remains relevant only insofar as a Person's Membership carries structural placement (per URA-001-17b/ERG-001-03) — a dependency, not a primary ownership relationship.

The ARCH-000 corrections follow directly from documents that already exist and already assert these facts about themselves (PE-001's own status header, PE-001's own governance chapters establishing the PE-001-Cxxx pattern, CAP-001's own self-declared scope, and PE-001/PE-001-C005/CAP-001's mutual citation of EIA-001). No new architecture is invented by this ADR — it brings the manifest into agreement with what the referenced documents already state about themselves.

## Consequences

- C-006's capability identity does not change: it remains **C-006 — Person Management**.
- C-006's business intent does not change: it remains **"Manage enterprise persons."**
- No capability identifier changes anywhere in CAP-001.
- No change is made to the CAP-001 registry meta-model, its columns, or its structure.
- No implementation, schema, or migration change is required by this decision — this is a documentation and governance correction only.
- Future Enterprise Experience engineering for C-006 (PE-001-C006) will treat **URA-001** as its primary semantic authority for Person, Identity, and Membership concerns.
- **ERG-001** may still be referenced by PE-001-C006 wherever enterprise structural or relationship context is relevant, as a dependency rather than the primary authority.
- **ARCH-000** becomes aligned with the actual current canonical authority model of the repository: CAP-001 is recognized as capability-identity authority, PE-001's canonical (not "under development") status is reflected, the PE-001-Cxxx pattern and PE-001-C005's Gold Standard role are made explicit, and EIA-001's referenced-but-missing status is now visible rather than silently absent.

## Status

**Accepted**
