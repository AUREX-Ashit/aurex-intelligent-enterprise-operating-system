# ADR-024 — Tenant Identity, Allocation, and Boundary Authority Belongs to the Infrastructure/Technical-Architecture Layer

**Status:** Accepted
**Classification:** Architecture Governance / Constitutional Authority Assignment (Multi-Tenancy)
**Decided by:** Repository Owner (architecture governance authority), 2026-08-25, selecting Option C of `ROD-C040-Tenant-Identity-Allocation-Authority.md` (`architecture/06-Reviews/`) following the completed `IRA-C040_Tenant_Administration_Business_Function_and_Implementation_Readiness_Assessment.md` readiness assessment.
**Affected Documents:** None amended by this ADR. This ADR resolves a constitutional-authority-assignment question that `CAP-001`, `SD-002`, and `CMD-001` leave open; it does not itself amend any of them. `PE-001-C040.docx` is unaffected — not modified by this ADR.
**Affected Code:** None. No migration, model, router, service, schema, or test is created or modified by this ADR.

---

## 1. ADR ID

`ADR-024`

## 2. Title

Tenant Identity, Allocation, and Boundary Authority Belongs to the Infrastructure/Technical-Architecture Layer

## 3. Status

**Accepted.** This decision has already been made by the Repository Owner (explicit selection of Option C, recorded in conversation 2026-08-25, following full review of `ROD-C040-Tenant-Identity-Allocation-Authority.md`). Per this repository's own established convention, "Proposed" is used only while a decision is still open for selection (see `ADR-023`'s identical usage, drafted after its own Architectural Decision Assessment concluded). This ADR is not drafted "Proposed" merely because it is being written after the decision was made — the decision itself was already accepted before drafting began.

## 4. Date

2026-08-25

## 5. Decision

**Tenant identity, Tenant allocation authority, and Tenant boundary authority belong to the technical/infrastructure-architecture layer of the platform (`RTA-001`/`Master_Technical_Architecture.md`'s own governing domain), not to the Organization business-identity layer (`ERG-001`/C-004).** This is the authority-model decision only — it establishes *which architectural layer owns the question*, not the concrete mechanism, schema, or service that will eventually answer it.

This decision:

- Is consistent with C-040's already-reaffirmed Primary Specification, **SD-002** (`CAP-001` v1.6, Repository Owner Decision, 2026-08-25).
- Directly follows `SD-002 §13`'s own structural framing of Tenant as an infrastructure/data-isolation partition, distinct from Organization's business-identity concern.
- Formalizes Option C as evaluated in `ROD-C040-Tenant-Identity-Allocation-Authority.md` §8, without adopting that brief's own flagged future implementation consequence (`tenant_registry`) as part of this decision (§15 below).

## 6. Context

`IRA-C040_Tenant_Administration_Business_Function_and_Implementation_Readiness_Assessment.md` (2026-08-25) classified C-040 — Tenant Administration **RED — Not Implementation Ready**, finding that all eight candidate Business Activities are blocked at Category D (`IMP-001 §6.2b`) because no canonical authority exists for Tenant identity, allocation, or boundary (`PE-001-C040` BR-C040-15/INV-C040-17, BR-C040-03/INV-C040-07, BR-C040-13). `ROD-C040-Tenant-Identity-Allocation-Authority.md` then presented the Repository Owner with four genuinely distinct architectural options (A: platform-level constitutional entity; B: Organization-owned authority; C: infrastructure-layer authority; D: defer) without recommending one. The Repository Owner reviewed that brief and explicitly selected **Option C**.

## 7. Problem

The repository has never assigned an authority for three related but distinct questions: (a) who/what creates and permanently assigns a Tenant's canonical identity; (b) who/what determines that a new Tenant should exist and allocates it; (c) what constitutes the authoritative Tenant boundary for isolation/governance purposes. `PE-001-C040`'s own text repeatedly and deliberately declines to answer these (its v1.1 corrective pass specifically *removed* an earlier unsupported cardinality assumption rather than let it stand unexamined) — this is disciplined non-invention, not an oversight, and this ADR exists to close exactly the gap that discipline correctly refused to close on its own authority.

## 8. Decision Drivers

1. Alignment with **SD-002** as C-040's own reaffirmed Primary Specification (`CAP-001` v1.6).
2. Preservation of separation between infrastructure tenancy and business Organization identity — `PE-001-C040` BR-C040-01 ("A Tenant SHALL NOT be treated as equivalent to... an Organization") and its own Guiding Architectural Question derivation (§1.3), which engineered C-040 separately from C-004 specifically because SD-002 §13 names a structural concern C-004 does not own.
3. Avoidance of prematurely constraining Tenant–Organization cardinality — an infrastructure-layer authority does not, by itself, force any particular cardinality, unlike Option B (which would have forced 1:1 by construction).
4. Compatibility with a multi-tenant SaaS architecture — `Master_Technical_Architecture.md`'s own already-designed `tenant_registry` schema (AMD-002, still deferred) names `deployment_model` (shared / dedicated_subscription / customer_tenant) as a first-class concern, evidencing that the platform's own technical architecture already anticipates deployment-model variability an Organization-only model would not naturally express.
5. Compatibility with multiple deployment/tenant isolation models — `SD-002-109`/`-110` frame isolation and resource-allocation as data-layer and infrastructure guarantees, not business-identity guarantees.
6. Avoidance of prematurely creating a new Layer-1 constitutional entity (Option A) when SD-002 §13 already provides sufficient constitutional grounding for an infrastructure-layer reading, without requiring new constitutional authorship at this time.
7. Avoidance of prematurely adopting `tenant_registry` — this decision is explicitly scoped to the authority *layer*, not the mechanism (§15).

These are stated here as the Repository Owner's decision rationale, as documented and evaluated in `ROD-C040` §7/§11; they are architectural rationale, not implementation facts, and are not overstated as such anywhere in this ADR.

## 9. Architectural Meaning of the Decision

**Tenant identity.** The infrastructure/technical-architecture layer owns the canonical concept and authority governing Tenant identity — i.e., whatever mechanism eventually assigns a Tenant its permanent identifier, that mechanism belongs within the infrastructure-architecture domain, not within `ERG-001`/C-004's own Organization-identity domain.

**Tenant allocation.** The infrastructure/technical-architecture layer owns the authority governing when a Tenant identity is allocated/established — the trigger, criteria, and process for bringing a new Tenant into existence belong to this layer, not to Organization Establishment (C-004) directly, though Organization establishment may remain a relevant upstream signal (as `PE-001-C040` §1.7's own "Organization before Tenant" sequencing principle already states, unaffected by this ADR).

**Tenant boundary.** The infrastructure/technical-architecture layer owns the Tenant boundary used for platform data-isolation and governance purposes — the authoritative answer to "which Tenant does this data/request belong to" is a question this layer answers, consistent with `SD-002-108`'s requirement that every business object carry an explicit, non-optional tenant identifier "as part of its Universal Identity," never inferred at query time.

**Organization.** Organization remains exclusively a business/enterprise identity concept, governed by `ERG-001`/C-004, unaffected by this ADR. **This ADR does not state that Tenant and Organization are 1:1. It does not state that multiple Organizations per Tenant are permitted.** Cardinality is explicitly and deliberately left open (§13).

## 10. Canonical Architectural Relationship

```
Infrastructure / Technical-Architecture Layer
    → Tenant identity            (this ADR)
    → Tenant allocation           (this ADR)
    → Tenant isolation/boundary   (this ADR)

Business / Enterprise Layer  (unaffected — ERG-001/C-004, unchanged)
    → Organization identity
    → Organization lifecycle
    → Organization business relationships
```

Conflating these two layers — as Option B would have done by construction — would permanently bind Tenant's own lifecycle to Organization's, foreclosing any future deployment model in which a single infrastructure/isolation partition legitimately spans more than one Organization, or in which an Organization's own infrastructure partition changes independently of its business identity (e.g., a technical migration between deployment models without any change to the Organization itself). Keeping the layers separate preserves the platform's own already-evidenced deployment-model variability (`tenant_registry.deployment_model`, `Master_Technical_Architecture.md` AMD-002) as a live future option rather than closing it off by an identity-modeling choice made now, for reasons unrelated to that variability.

## 11. Evidence

- **`SD-002 §13`** (`SD-002-108` through `SD-002-112`) — the constitutional grounding for treating Tenant as a structural, infrastructure/data-isolation concern; independently confirmed by this session's own full read of `SD-002` as containing five substantive, structural tenant rules, versus `SD-001`'s single, adjectival reference (`SD-001-102`).
- **`CAP-001` v1.6** — C-040's Primary Specification is SD-002, reaffirmed by explicit Repository Owner Decision, 2026-08-25 (the "C-040 Repository Owner Confirmation" changelog entry).
- **`ROD-C040-Tenant-Identity-Allocation-Authority.md`** — the decision brief this ADR formalizes; Option C's own full evaluation (§8), the Decision Matrix (§11), and the explicit `tenant_registry`-independence framing (§10) are all incorporated here by reference, not restated in full.
- **`IRA-C040_Tenant_Administration_Business_Function_and_Implementation_Readiness_Assessment.md`** — the readiness assessment that first surfaced this gap as the central blocker (§9, §13, §18).
- **`CMD-001 §12.6`** (Scope Hierarchy) — places Tenant above Enterprise in an illustrative configuration-resolution chain (Global Platform → Region → Country → Tenant → Enterprise → Business Domain → Business Object → User). This is cited here, as it was in `IRA-C040`/`ROD-C040`, strictly as *suggestive* evidence of a configuration-resolution scope relationship — it is not treated as resolving cardinality, and this ADR does not convert it into a cardinality decision (§13).
- **`Master_Technical_Architecture.md`** (AMD-002, `tenant_registry`) — the only existing, already-designed candidate schema for an infrastructure-layer Tenant mechanism; cited as evidence that the technical-architecture layer has already anticipated this kind of concern, not as evidence that this schema is now adopted (§15).
- **`Backend/Services/AuthService/models/organization.py`** — the real, migrated `Organization` model, independently re-verified for this ADR (as it was for `ROD-C040 §5`) to carry no tenant field, no tenant relationship, and no tenant concept of any kind. **Preserved distinction, per the ROD's own discipline:** `CLAUDE.md §6`'s constitutional text ("Organization defines the tenant boundary") is a statement about Organization's role in *defining* a tenant boundary conceptually; it is not evidence that Organization is, or has ever been, the *implemented system of record* for Tenant identity — no such implementation exists anywhere in this repository. This ADR does not read `CLAUDE.md §6` as contradicting the decision made here; it reads it as a boundary-definition statement consistent with Organization remaining the business-identity anchor an infrastructure-layer Tenant concept would still need to consume (`PE-001-C040` §1.7, "Organization before Tenant" sequencing, unaffected by this ADR).
- **`ADR-003`** — the precedent for resolving an implementation-ownership ambiguity `CAP-001`/`ARCH-000`/`ERG-001` do not themselves address, via a dedicated ADR rather than by silent inference; this ADR follows the same pattern for a comparably-scoped, comparably-unaddressed question.
- **`RTA-001`** — the runtime/infrastructure-architecture document this ADR names as the eventual home for Tenant identity/allocation/boundary authority; not itself amended by this ADR (§Affected Documents), and not searched for a pre-existing Tenant-authority statement it does not currently make, per this session's own prior independent findings that no general-purpose, implemented Tenant mechanism exists anywhere in this repository, including `RTA-001`.

No evidence cited above is claimed to state more than it actually states; where a source is suggestive rather than dispositive (`CMD-001 §12.6`, `Master_Technical_Architecture.md`'s schema comment), that is stated explicitly rather than silently upgraded to a ratified fact.

## 12. Options Considered

Restated from `ROD-C040` §8, with the Repository Owner's own reason for non-selection recorded for each, without disparagement:

### Option A — Tenant as a first-class constitutional platform entity
Not selected. Would have required authoring new Layer-1 constitutional architecture (mirroring `COM-001`/`GRC-001`/`PLT-001`'s own precedent) before any authority question could be resolved — the heaviest-weight option, and SD-002 §13 was judged to already provide sufficient constitutional grounding for an infrastructure-layer reading without new constitutional authorship at this time (Decision Driver 6).

### Option B — Organization-owned Tenant authority
Not selected. Architecturally viable and consistent with `CLAUDE.md §6`'s literal text, but would have forced Tenant–Organization cardinality to 1:1 by construction, directly foreclosing the deployment-model flexibility `Master_Technical_Architecture.md`'s own `tenant_registry` design already anticipates, and would have required reconciling substantial redundancy with `PE-001-C040`'s own existing 8-ERB architecture (particularly ERB-C040-01, engineered specifically to resolve a distinction Option B would collapse).

### Option C — Infrastructure-layer Tenant authority — **SELECTED**
Selected as the authority model most directly consistent with `SD-002 §13`'s own existing constitutional framing, requiring no new constitutional document and no forced cardinality, while remaining honest that its only existing candidate mechanism (`tenant_registry`) is separately, and remains, deferred (§15).

### Option D — Defer the decision
Not selected. Would have left all eight C-040 candidate Business Activities indefinitely blocked with no authority question resolved at all; the Repository Owner chose to resolve the authority-layer question now rather than defer it further, distinct from the separate, still-standing decision to keep `tenant_registry` itself deferred.

## 13. Decision Rationale

See Decision Drivers (§8) for the seven considerations documented as informing the Repository Owner's selection of Option C. These are recorded here as the rationale for *this* decision; they are not restated as claims about implementation readiness, which this ADR does not change (§18).

## 14. Architectural Consequences

### Positive consequences
- Clear architectural ownership of the Tenant identity/allocation/boundary question, ending the previously undecided state `IRA-C040` found blocking.
- Clean separation preserved between infrastructure tenancy (this ADR) and Organization business identity (`ERG-001`/C-004, unaffected).
- Future cardinality flexibility preserved — this ADR does not foreclose any Tenant–Organization relationship model.
- C-040 is now aligned, at the authority-layer level, with its own reaffirmed Primary Specification, SD-002.
- No premature implementation commitment is made — the mechanism, schema, and system of record all remain open questions (§15–§18).

### Negative / deferred consequences
- The physical Tenant system of record remains unresolved (§18).
- `tenant_registry` remains deferred — this ADR does not change that status (§15).
- Tenant–Organization cardinality remains unresolved (§16).
- Tenant creation/allocation approval authority remains unresolved (§17).
- **C-040 remains RED — Not Implementation Ready** (§20). This ADR does not, by itself, unblock any C-040 Business Activity.
- Additional constitutional/domain decisions remain necessary before implementation can begin (§21).

## 15. `tenant_registry` Status

**`tenant_registry` remains DEFERRED.**

This ADR:

- **Does not adopt** `tenant_registry`.
- **Does not reject** `tenant_registry`.
- **Does not authorize implementation** of `tenant_registry` (no migration, model, or schema build is authorized here or anywhere else by this decision).
- **Does not establish** `tenant_registry` as the Tenant system of record.

Selecting an infrastructure-layer authority *model* (this ADR) is independent of selecting a concrete infrastructure-layer *mechanism*. `tenant_registry` (`Master_Technical_Architecture.md` AMD-002) remains the only already-designed candidate mechanism consistent with this ADR's chosen layer, but its own standing deferral (`SER-001` SE-052, reaffirmed 2026-08-25) is unchanged by this ADR. **Any future adoption of `tenant_registry`, or of any alternative infrastructure-layer mechanism, must occur through a separate, explicit architectural/governance decision** — not implied, inferred, or silently authorized by this ADR.

## 16. Tenant–Organization Cardinality Status

**Tenant–Organization cardinality remains unresolved.**

This ADR does not infer or establish 1:1, 1:N, N:1, or N:N. The infrastructure-layer authority model selected here intentionally does not settle cardinality — `ROD-C040` presented cardinality as a distinct sub-question (§3, §14 sequence step 2) precisely because an authority-layer decision does not, by itself, answer it. `CMD-001 §12.6`'s scope-hierarchy placement of Tenant above Enterprise remains suggestive evidence only (§11), not converted into a ratified cardinality statement by this ADR.

## 17. Approval Authority Status

**Tenant creation/allocation approval authority remains unresolved — PENDING CANONICAL BINDING.**

This ADR does not assign approval authority to Platform Administrator, Corporate Administrator, an infrastructure/operations role, C-040 itself, or any other actor. No canonical source examined for this ADR (`SD-002`, `CAP-001`, `RTA-001`, `PE-001-C040`, any existing ADR) establishes such an authority. Per `PE-001-C040` BR-C040-13's own discipline, this remains explicitly recorded as Pending Canonical Binding rather than resolved by inference or convenience.

## 18. System-of-Record Status

**The canonical Tenant system-of-record mechanism remains unresolved.**

This ADR establishes the **authority layer** (infrastructure/technical-architecture) that will eventually own the system of record; it does not establish the concrete registry, database, table, or service itself. No CBOR (Canonical Business Object Register) entry exists for Tenant, and none is created by this ADR.

## 19. C-040 Impact

### Resolves
- The Tenant identity/allocation/boundary **authority layer** — this question, and only this question, is now settled: infrastructure/technical-architecture, not Organization business identity.

### Does NOT resolve
- Tenant–Organization cardinality (§16).
- Tenant creation/allocation approval authority (§17).
- The Tenant system-of-record mechanism (§18).
- `tenant_registry`'s own adoption status (§15).
- Any C-040 Business Activity's own implementation readiness.
- Any database schema, API design, migration, provisioning workflow, migration workflow, offboarding workflow, or cross-tenant sharing mechanism.
- Any Work Package (including WP-16, not created, reserved, or implied by this ADR).

**Therefore: C-040 remains RED — Not Implementation Ready until the remaining canonical decisions are resolved and the IRA is re-assessed.** This ADR's own acceptance does not, by itself, upgrade `IRA-C040`'s classification — that determination belongs exclusively to a fresh, dedicated IRA re-assessment (`CLAUDE.md §19.7`; `ROD-C040 §16` step 7), not to this ADR.

## 20. Explicit Non-Decisions

This ADR does **not** decide, and no part of it should be read as deciding:

- `tenant_registry` adoption (§15).
- The physical Tenant registry/system-of-record mechanism (§18).
- Tenant database schema.
- Tenant identifier implementation.
- Tenant–Organization cardinality (§16).
- Tenant creation/allocation approval authority (§17).
- Tenant provisioning workflow.
- Tenant migration.
- Tenant offboarding.
- Cross-tenant sharing.
- API design.
- Any C-040 Business Activity definition or charter.
- WP-16 or any Work Package.
- Implementation authorization of any kind.

## 21. Dependencies / Follow-on Decisions

The downstream dependency chain, none of it collapsed into this single decision:

**Infrastructure-layer Tenant authority** *(this ADR)*
→ **Tenant–Organization cardinality**
→ **Tenant approval/allocation authority**
→ **Tenant system-of-record decision**
→ **C-040 architectural reconciliation** (`PE-001-C040` reviewed against this ADR's own authority-layer decision)
→ **Business Activity ratification** (candidate BAs re-classified under `IMP-001 §6.2b`'s A–E scale; a D→C reclassification does not, by itself, authorize implementation, per `IMP-001 §6.2b`'s own explicit rule)
→ **IRA re-assessment** (`CLAUDE.md §19.7`)
→ **implementation authorization**

Each step remains a separate, subsequent Repository Owner action.

## 22. Related Artifacts

- `architecture/06-Reviews/ROD-C040-Tenant-Identity-Allocation-Authority.md` — the decision brief this ADR formalizes.
- `architecture/05-Implementation/IRA-C040_Tenant_Administration_Business_Function_and_Implementation_Readiness_Assessment.md` — the readiness assessment that surfaced the gap.
- `architecture/02-Constitutional/CAP-001_Enterprise_Capability_Registry.md` v1.6 — C-040's Primary Specification (SD-002) reaffirmation, this ADR's own Decision Driver 1.
- `architecture/06-Reviews/SER-001_Strategic_Enhancement_Register.md` (SE-052) — `tenant_registry`'s own standing deferral, unchanged by this ADR.
- `architecture/07-Decisions/ADR-003_Organization_Management_Implementation_Ownership.md` — the precedent this ADR's own structure follows for resolving an implementation-ownership ambiguity via dedicated ADR.
- `docs/Product/PE-001/capabilities/C-040/PE-001-C040_Tenant_Administration.docx` — the governed specification whose BR-C040-03/13/15 named the gap this ADR now begins to close; not modified by this ADR.

## 23. Approval / Repository Owner Record

| Field | Value |
|---|---|
| **Decision** | Option C — Infrastructure-Layer Tenant Authority |
| **Decision Authority** | Repository Owner |
| **Decision Date** | 2026-08-25 |
| **Source Decision Brief** | `ROD-C040-Tenant-Identity-Allocation-Authority.md` |
| **Status** | Accepted |

---

## 24. Consequences Summary (Repository State After This ADR)

| Item | Status |
|---|---|
| C-040 Primary Specification | SD-002 (unchanged, reaffirmed prior to this ADR) |
| Tenant identity/allocation/boundary authority layer | **Infrastructure/technical-architecture — decided by this ADR** |
| `tenant_registry` | DEFERRED (unchanged) |
| Tenant–Organization cardinality | UNRESOLVED (unchanged) |
| Tenant approval authority | UNRESOLVED — PENDING CANONICAL BINDING (unchanged) |
| Tenant system of record | UNRESOLVED (unchanged) |
| C-040 readiness classification | RED — Not Implementation Ready (unchanged; this ADR does not upgrade it) |
