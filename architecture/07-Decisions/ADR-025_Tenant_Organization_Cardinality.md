# ADR-025 — Tenant–Organization Cardinality Is 1:1

**Status:** Accepted
**Classification:** Architecture Governance / Constitutional Data-Model Relationship (Multi-Tenancy)
**Decided by:** Repository Owner (architecture governance authority), 2026-08-25, selecting Option A of `ROD-C040-Tenant-Organization-Cardinality.md` (`architecture/06-Reviews/`) following `ADR-024`'s own explicit deferral of this question.
**Affected Documents:** None amended by this ADR. This ADR resolves a cardinality question `ADR-024`, `SD-002`, `CMD-001`, and `PE-001-C040` each explicitly and deliberately left open. It does not itself amend any of them.
**Affected Code:** None. No migration, model, router, service, schema, or test is created or modified by this ADR.

---

## 1. ADR ID

`ADR-025`

## 2. Title

Tenant–Organization Cardinality Is 1:1

## 3. Status

**Accepted.** The Repository Owner explicitly selected Option A of `ROD-C040-Tenant-Organization-Cardinality.md` (recorded in conversation, 2026-08-25). Per this repository's own established convention (`ADR-023`, `ADR-024`), this ADR is drafted "Accepted" directly, not "Proposed," because the decision was already made before drafting began.

## 4. Date

2026-08-25

## 5. Decision Authority

Repository Owner.

## 6. Context

`ADR-024` (Accepted, 2026-08-25) established that Tenant identity, allocation, and boundary authority belong to the infrastructure/technical-architecture layer, distinct from Organization's business-identity layer (`ERG-001`/C-004) — but explicitly left Tenant–Organization cardinality unresolved, naming it as the next decision in its own dependency sequence (`ADR-024 §21`). `ROD-C040-Tenant-Organization-Cardinality.md` then presented the Repository Owner with three genuine cardinality models (A: 1:1; B: 1 Tenant:Many Organizations; C: Many Tenants:1 Organization) and one explicitly excluded model (D: many-to-many, unevidenced), without deciding among them, and identified Option A as the architecturally strongest candidate on current evidence while making clear the Repository Owner retained full authority to select differently. The Repository Owner reviewed that brief and explicitly selected **Option A**.

## 7. Problem

`PE-001-C040`'s own Business Rule BR-C040-03 and Invariant INV-C040-07 record that the specification "SHALL NOT assume one-to-one, one-to-many, many-to-one, or many-to-many Tenant–Organization semantics" until cardinality is canonically established — a deliberate, disciplined non-invention (its v1.1 corrective pass specifically *removed* an earlier unsupported "exactly one Organization Anchor" assumption for this exact reason). `IRA-C040` identified this unresolved cardinality as one of the constitutional blockers preventing any C-040 Business Activity from advancing past Category D (`IMP-001 §6.2b`). This ADR exists to resolve exactly that gap, and only that gap.

## 8. Decision Drivers

1. `PE-001-C040`'s own Pre-Engineering Authority Pass — the specification's own mandatory, disciplined analysis step performed before any experience architecture was derived — found that "in the supplied baseline's common and only-evidenced case, one Organization corresponds to one Tenant." This is the single most direct piece of textual evidence available anywhere in the canonical baseline on this question (`ROD-C040-Tenant-Organization-Cardinality.md §2`, §15).
2. No canonical source establishes a 1:N requirement. `CMD-001 §12.6`'s scope-hierarchy placement of Tenant above Enterprise is suggestive of configuration-resolution scope only, and is explicitly disclaimed as non-dispositive by `PE-001-C040`'s own Decision Record (§9.6): "could suggest a one-to-many relationship, but no canonical document confirms this."
3. No canonical source establishes an N:1 requirement. `tenant_registry`'s own deferred schema design (`Master_Technical_Architecture.md` AMD-002) names `deployment_model` and `data_residency_country` as per-Tenant fields, which is suggestive of future deployment/residency variability, but — as `ROD-C040-Tenant-Organization-Cardinality.md §15` specifically clarifies — describes *how* a single Tenant's infrastructure is provisioned, not *how many* Tenants one Organization may span; it is not evidence of an N:1 requirement.
4. The existing, real, migrated `Organization` model (`Backend/Services/AuthService/models/organization.py`) is fully compatible with 1:1 cardinality as-is — it requires no structural change to accommodate this decision, unlike Options B or C, each of which would require inventing a new intra-Tenant or cross-Tenant mechanism not currently architected anywhere.
5. No C-040 requirement conflicts with 1:1. Direct re-examination of `PE-001-C040`'s own text (BR-C040-03, INV-C040-07, §1.7 "Organization before Tenant," §1.16 Tenant Administrative Anchor Context, ERB-C040-01) found every cardinality-adjacent reference either explicitly disclaiming an assumption (BR-C040-03/INV-C040-07) or describing single-experience-thread anchoring (§1.16, ERB-C040-01) compatible with any of the three genuine options, never a statement requiring 1:N or N:1 (`ROD-C040-Tenant-Organization-Cardinality.md §10`).
6. Selecting 1:1 preserves, rather than collapses, the conceptual separation `ADR-024` established between infrastructure Tenant and business Organization — 1:1 cardinality is a statement about *how many* of each concept correspond to the other, not a statement that the two concepts are the same entity (§10 below).
7. Selecting 1:1 avoids introducing an unsupported multi-Organization tenancy model (Option B) or multi-Tenant-per-Organization model (Option C) merely because either is technically possible — no repository evidence (a signed contract, an active sales conversation, or a `SER-001` entry) names an actual current need for either, and `ROD-C040-Tenant-Organization-Cardinality.md §8` found Option D (many-to-many) unsupported by any evidence whatsoever.

## 9. Decision

**The canonical Tenant–Organization cardinality is 1:1: exactly one Tenant corresponds to exactly one Organization, and exactly one Organization corresponds to exactly one Tenant.**

Architectural relationship, restated per the Repository Owner's own framing:

```
Infrastructure / Technical Architecture
    → Tenant
        → 1:1
    → Organization
Business / Enterprise Architecture
```

## 10. Critical Architectural Qualification

**Tenant and Organization remain distinct concepts. This ADR does not state or imply they are the same entity.**

- **Tenant** = infrastructure/data-isolation boundary, owned by the infrastructure/technical-architecture layer (`ADR-024`).
- **Organization** = business/enterprise identity and lifecycle concept, owned by `ERG-001`/C-004, unaffected by this ADR.

This ADR establishes **cardinality only** — a statement of how many of one concept correspond to how many of the other. It does **not** infer, require, or authorize that Tenant and Organization share: a lifecycle implementation; a database table; an identifier; a service; an API; a system of record; or an approval authority. Each of those remains a separate decision, resolved only where a canonical source already establishes it (none currently does — §16).

## 11. Options Considered

Restated from `ROD-C040-Tenant-Organization-Cardinality.md §8`, with the Repository Owner's own basis for non-selection of B and C recorded, without disparagement:

### Option A — 1 Tenant : 1 Organization — **SELECTED**
The only cardinality with direct evidentiary support (Decision Driver 1); requires no new architecture; fully compatible with the existing, real `Organization` model.

### Option B — 1 Tenant : Many Organizations
Not selected. Would require inventing an intra-Tenant Organization-isolation mechanism not currently architected anywhere, and a new billing/approval-authority question beyond what `ADR-024` already left open — none of which is evidenced as a current need.

### Option C — Many Tenants : 1 Organization
Not selected. Would require an Organization-lifecycle-to-multiple-Tenant-lifecycles reconciliation mechanism not currently architected anywhere; matches `tenant_registry`'s own anticipated deployment/residency variability more closely than Option B, but remains, per `ROD-C040-Tenant-Organization-Cardinality.md §9`, a plausible future scenario rather than a demonstrated current requirement.

### Option D — Many-to-Many
Not considered a genuine candidate at any stage — `ROD-C040-Tenant-Organization-Cardinality.md §8` found no repository evidence supporting it, and it was excluded from selection rather than evaluated as an equal alternative.

## 12. Rationale

See Decision Drivers (§8). The rationale rests specifically on `PE-001-C040`'s own disciplined Pre-Engineering Authority Pass finding, not on convenience or implementation simplicity — though 1:1 is also, independently, the simplest of the three genuine options to implement, this ADR's own basis for selection is the evidentiary one, consistent with `ROD-C040-Tenant-Organization-Cardinality.md §15`'s own recommendation discipline. No evidence is overstated here beyond what that brief already established: the "only evidenced case" finding is treated as exactly that — the only evidenced case — not as proof that alternative cardinalities are impossible or undesirable in the future (§14).

## 13. Architectural Consequences

- `PE-001-C040` BR-C040-03/INV-C040-07's own "SHALL NOT assume" language is now superseded for the 1:1 case specifically — the specification may now assume 1:1 cardinality where relevant, though this ADR does not itself amend `PE-001-C040`'s text (that remains a separate, future document-reconciliation action, per `IRA-C040 §14`'s own Document Synchronization Debt discipline, not performed by this ADR).
- `PE-001-C040`'s own experience-anchoring language (§1.16 Tenant Administrative Anchor Context, ERB-C040-01) is now confirmed consistent with the canonical cardinality — no re-architecture is required, only an optional future clarifying note.
- No change to `ERG-001`, `ADR-024`, or the real `Organization` model is required as a direct consequence of this ADR.
- The Organization-lifecycle-to-Tenant-lifecycle coupling risk that `ROD-C040-Tenant-Organization-Cardinality.md §11` identified as strongest under 1:1 cardinality remains a live, unresolved risk this ADR does not close — whether suspending or retiring an Organization automatically affects its (now-guaranteed-unique) Tenant is not decided here.

## 14. C-040 Impact

**Resolves:** the Tenant–Organization cardinality blocker specifically (§6 of `ROD-C040-Tenant-Organization-Cardinality.md`'s own downstream-sequence framing) — one of the constitutional gaps `IRA-C040` identified.

**Does NOT resolve:** any other C-040 blocker.

**Therefore: C-040 remains RED — Not Implementation Ready.** This ADR resolves only one constitutional blocker among several `IRA-C040` identified. Tenant creation/allocation approval authority and the Tenant system-of-record mechanism must still be separately resolved, followed by a `PE-001-C040` architectural reconciliation pass and a fresh, dedicated IRA re-assessment (`CLAUDE.md §19.7`), before any C-040 Business Activity's own readiness classification can be revisited. This ADR's own acceptance does not, by itself, upgrade any candidate Business Activity's Category D classification (`IMP-001 §6.2b`).

## 15. Future Change Condition

**A future requirement for multiple Organizations per Tenant, or multiple Tenants per Organization, must trigger a new explicit architectural decision and impact assessment. Such a relationship must not be introduced implicitly during implementation.** Any future deviation from 1:1 cardinality requires the same class of dedicated, evidence-first Repository Owner decision process this ADR and `ADR-024` themselves followed — not a silent schema change, not an implementation-time assumption, and not an inference from a future feature request alone.

## 16. Explicit Non-Decisions

This ADR does **not** decide, and no part of it should be read as deciding:

- `tenant_registry` adoption — **remains DEFERRED**, unchanged. This ADR does not adopt, activate, design, or authorize it.
- Tenant system-of-record mechanism — remains UNRESOLVED (`ADR-024 §18`).
- Tenant creation/allocation approval authority — remains UNRESOLVED / PENDING CANONICAL BINDING (`ADR-024 §17`).
- Tenant provisioning implementation.
- Tenant migration implementation.
- Tenant offboarding implementation.
- Cross-tenant sharing implementation.
- Any C-040 Business Activity definition, charter, or ratification.
- WP-16 or any Work Package.
- API design.
- Database schema.
- Any implementation authorization of any kind.
- Whether Tenant and Organization share a lifecycle implementation, database table, identifier, service, API, system of record, or approval authority (§10).

## 17. Remaining Open Decisions

Restated from `ADR-024 §21`'s own dependency sequence, now with cardinality closed:

**ADR-024 — Tenant authority layer** *(Accepted)*
→ **Tenant–Organization cardinality** *(this ADR — Accepted)*
→ **Tenant approval/allocation authority** *(still open)*
→ **Tenant system-of-record decision** *(still open)*
→ **C-040 architectural reconciliation**
→ **Business Activity ratification**
→ **IRA re-assessment**
→ **implementation authorization**

## 18. Related Artifacts

- `architecture/06-Reviews/ROD-C040-Tenant-Organization-Cardinality.md` — the decision brief this ADR formalizes.
- `architecture/07-Decisions/ADR-024_Tenant_Infrastructure_Layer_Authority.md` — the prior, related decision this ADR follows and does not amend.
- `architecture/06-Reviews/ROD-C040-Tenant-Identity-Allocation-Authority.md` — the decision brief `ADR-024` itself formalized.
- `architecture/05-Implementation/IRA-C040_Tenant_Administration_Business_Function_and_Implementation_Readiness_Assessment.md` — the readiness assessment that first surfaced this gap.
- `architecture/02-Constitutional/CAP-001_Enterprise_Capability_Registry.md` v1.6 — C-040's Primary Specification (SD-002), unaffected by this ADR.
- `architecture/06-Reviews/SER-001_Strategic_Enhancement_Register.md` (SE-052) — `tenant_registry`'s own standing deferral, unaffected by this ADR.
- `docs/Product/PE-001/capabilities/C-040/PE-001-C040_Tenant_Administration.docx` — the governed specification whose BR-C040-03/INV-C040-07 named this gap; not modified by this ADR.

## 19. Approval Record

| Field | Value |
|---|---|
| **Decision** | Option A — 1 Tenant : 1 Organization |
| **Decision Authority** | Repository Owner |
| **Decision Date** | 2026-08-25 |
| **Source Decision Brief** | `ROD-C040-Tenant-Organization-Cardinality.md` |
| **Status** | Accepted |

---

## 20. Consequences Summary (Repository State After This ADR)

| Item | Status |
|---|---|
| C-040 Primary Specification | SD-002 (unchanged) |
| Tenant identity/allocation/boundary authority layer | Infrastructure/technical-architecture (unchanged, `ADR-024`) |
| Tenant–Organization cardinality | **1:1 — decided by this ADR** |
| `tenant_registry` | DEFERRED (unchanged) |
| Tenant approval authority | UNRESOLVED — PENDING CANONICAL BINDING (unchanged) |
| Tenant system of record | UNRESOLVED (unchanged) |
| C-040 readiness classification | RED — Not Implementation Ready (unchanged; this ADR does not upgrade it) |
