# ADR-026 — Tenant Establishment Uses Dual Business-Approval and Infrastructure-Allocation Authority

**Status:** Accepted
**Classification:** Architecture Governance / Constitutional Authority Model (Multi-Tenancy)
**Decided by:** Repository Owner (architecture governance authority), 2026-08-25, selecting Option D of `ROD-C040-Tenant-Approval-Allocation-Authority.md` (`architecture/06-Reviews/`) following `ADR-024` and `ADR-025`.
**Affected Documents:** None amended by this ADR. This ADR resolves an authority-model question `ADR-024`, `ADR-025`, `URA-001`, and `PE-001-C040` (BR-C040-13/BR-C040-15) each explicitly leave open. It does not itself amend any of them.
**Affected Code:** None. No migration, model, router, service, schema, or test is created or modified by this ADR.

---

## 1. ADR ID

`ADR-026`

## 2. Title

Tenant Establishment Uses Dual Business-Approval and Infrastructure-Allocation Authority

## 3. Status

**Accepted.** The Repository Owner explicitly selected Option D of `ROD-C040-Tenant-Approval-Allocation-Authority.md` (recorded in conversation, 2026-08-25). Per this repository's own established convention (`ADR-023`, `ADR-024`, `ADR-025`), this ADR is drafted "Accepted" directly, not "Proposed," because the decision was already made before drafting began.

## 4. Date

2026-08-25

## 5. Decision Authority

Repository Owner.

## 6. Context

`ADR-024` (Accepted) established that Tenant identity, allocation, and boundary authority belong to the infrastructure/technical-architecture layer. `ADR-025` (Accepted) established that Tenant–Organization cardinality is 1:1. Neither resolved *who* approves a Tenant's establishment or *who* allocates its canonical identity. `ROD-C040-Tenant-Approval-Allocation-Authority.md` then presented four genuine authority models (A: Platform Administrator/Governance Authority; B: Organization Establishment Authority; C: Infrastructure/Technical-Architecture Authority; D: Dual/Two-Step Authority), keeping Approval, Allocation, and Provisioning explicitly distinct throughout, and identified Option D as the architecturally strongest candidate on current evidence without deciding among them. The Repository Owner reviewed that brief and explicitly selected **Option D**.

## 7. Problem

`PE-001-C040` BR-C040-13 records that "provisioning authority, migration approval authority, offboarding approval authority, and cross-tenant sharing approval authority" must not be invented locally and remain Pending Canonical Binding where no canonical authority exists in the supplied baseline. `URA-001-29`'s canonical System Role catalog governs platform administration broadly but names no authority over Tenant specifically. `ROD-C040-Tenant-Approval-Allocation-Authority.md §7` confirmed this directly: no canonical document anywhere in this repository names a Tenant approval or allocation authority. This ADR resolves the provisioning-approval clause of BR-C040-13's own gap — and only that clause — by establishing the authority *model*, not the specific role.

## 8. Decision Drivers

1. It preserves the business/infrastructure separation `ADR-024` itself established as its own core rationale — a single-actor model (Options A or C) would collapse two of the four distinct authority types (Request/Approval/Allocation/Provisioning, `ROD-C040-Tenant-Approval-Allocation-Authority.md §6`) into one, while a business-derived model (Option B) would collapse three.
2. It separates authorization from execution, rather than treating Tenant establishment as a single undifferentiated act.
3. It is structurally consistent with `IMP-001 §6.3`'s already-canonical, universal Business Activity Lifecycle (`Request → Authorization → Business Validation → Business Rule Execution → ...`), which already separates authorization from execution as a platform-wide pattern — this decision applies an existing structural pattern to Tenant establishment rather than inventing a novel governance shape.
4. It provides stronger separation of duties than any single-authority option — no one actor both approves and allocates (`ROD-C040-Tenant-Approval-Allocation-Authority.md §10`, Governance Principle 3).
5. It reduces the risk of unauthorized Tenant allocation by requiring two independent gates rather than one (`ROD-C040-Tenant-Approval-Allocation-Authority.md §13`, "Unauthorized Tenant prevention" row).
6. It avoids giving either a business administrator or an infrastructure authority inappropriate powers over the other's own concern — a business authority cannot unilaterally allocate infrastructure-layer Tenant identity, and an infrastructure authority cannot unilaterally approve a business need for a Tenant to exist.
7. It preserves future implementation flexibility — the two-step shape does not itself commit to any specific role, service, or mechanism for either step, leaving that determination to the separate, subsequent decisions this ADR explicitly does not make (§16, §20).

These are recorded as the Repository Owner's own decision rationale, as evaluated in `ROD-C040-Tenant-Approval-Allocation-Authority.md §8`–`§14`. The ROD's own recommendation is not read here as proof that any specific role must perform either step — only that the two-step *model* is the architecturally strongest shape on current evidence.

## 9. Decision

**Tenant establishment uses a two-step authority model: a business/platform authority approves the need for a Tenant, and the infrastructure/technical-architecture authority subsequently allocates/establishes the canonical Tenant identity and boundary.**

This decision establishes **separation between approval and allocation**. It does **not** establish the specific canonical role, person, or claim responsible for either authority, except where an existing canonical source already establishes it — and, per the evidence gathered for the source ROD, none currently does (§11, §12).

## 10. Authority Model

```
Step 1 — Business Approval
    "This Tenant should be established."
    Business/platform authority — role identity: PENDING CANONICAL BINDING

           ↓

Step 2 — Infrastructure Allocation
    "This Tenant identity is now officially allocated/established."
    Infrastructure/technical-architecture authority (per ADR-024) — role identity: PENDING CANONICAL BINDING

           ↓

Step 3 — Technical Provisioning
    Downstream execution concern — NOT decided by this ADR
```

**Approval ≠ Allocation ≠ Provisioning.** These remain three distinct concerns throughout this ADR, exactly as `ROD-C040-Tenant-Approval-Allocation-Authority.md §6` established them.

## 11. Approval Authority

**Model:** a separate business/platform approval authority, distinct from the infrastructure-layer allocation authority.

**Specific canonical role:** unresolved. `URA-001-29`'s System Role catalog (Aurex Admin, Corporate Admin, User Admin, Security Admin, Domain Admin) governs platform administration generally but names no Tenant-specific authority. The code-level `PLATFORM_ADMIN` claim currently gates the closest existing analogue (Organization Establishment) but is explicitly documented, in the code's own comments, as an interim gate, and `ADR-002` (still Proposed, unresolved) records that `PLATFORM_ADMIN` is only "conceptually adjacent to," not identical with, the canonical `AUREX_ADMIN` System Role.

**Status: PENDING CANONICAL BINDING.**

## 12. Allocation Authority

**Model:** the infrastructure/technical-architecture authority, per `ADR-024`'s own already-accepted layer assignment.

**Specific canonical role:** unresolved. No role, service-level authority, or system-level claim is currently named anywhere in `RTA-001`, `Master_Technical_Architecture.md`, or any other canonical source as holding this authority.

**Status: PENDING CANONICAL BINDING.**

## 13. Provisioning Boundary

**Not decided by this ADR.** Technical provisioning of infrastructure for an allocated Tenant remains a downstream implementation/architecture decision, separate from both the approval and allocation authorities this ADR addresses. No provisioning mechanism, service, or authority is named, implied, or authorized here.

## 14. Options Considered

Restated from `ROD-C040-Tenant-Approval-Allocation-Authority.md §8`, with the Repository Owner's own basis for non-selection recorded as architectural trade-offs, not as invalidation:

### Option A — Platform Administrator / Platform Governance Authority
Not selected. Architecturally reasonable and consistent with `URA-001-29`'s own platform-administration scope, but concentrates approval and allocation in a single actor, weakening separation of duties relative to Option D, and inherits `ADR-002`'s own unresolved `PLATFORM_ADMIN`/`AUREX_ADMIN` naming question directly, without the benefit of a second, independent gate to offset that risk.

### Option B — Organization Establishment Authority
Not selected. `ADR-025`'s own 1:1 cardinality makes this option operationally more plausible than it would otherwise be, but selecting it would have collapsed Organization establishment (a business-layer act) into Tenant allocation authority (an infrastructure-layer act) merely because the two now always co-occur — exactly the conflation `ROD-C040-Tenant-Approval-Allocation-Authority.md §8` warned against, and the weakest of the four options on separation-of-duties and approval-traceability grounds.

### Option C — Infrastructure / Technical-Architecture Authority
Not selected. Highest single-option consistency with `ADR-024`'s own layer assignment, but collapses approval into the same layer as allocation — the inverse conflation from Option B — and no canonical role currently exists within the infrastructure layer with a human-facing approval mandate.

### Option D — Dual / Two-Step Authority — **SELECTED**
Selected as the only option preserving `ADR-024`'s own business/infrastructure separation on both sides of the Tenant-establishment decision, structurally consistent with `IMP-001 §6.3`'s own Authorization→Execution lifecycle, at the acknowledged cost of requiring two distinct authorities to eventually be named rather than one.

## 15. Rationale

See Decision Drivers (§8). The rationale rests on architectural separation-of-concerns evidence (`ADR-024`'s own rationale, `IMP-001 §6.3`'s own lifecycle structure, and the governance-principle comparison in `ROD-C040-Tenant-Approval-Allocation-Authority.md §10`/`§13`), not on a canonical source naming Option D directly — none does, since no canonical source addresses Tenant approval/allocation authority at all prior to this ADR. The ROD's own recommendation is treated here as advisory input the Repository Owner weighed and accepted, not as independent proof.

## 16. CBAIP Alignment

`IMP-001 §6.3`'s universal Business Activity Lifecycle is: `Request → Authorization → Business Validation → Business Rule Execution → Metadata Resolution → Workflow Evaluation → Business Object Update → Domain Event Publication → Audit Recording → Response`. This ADR's own two-step model maps onto that lifecycle's existing structure without prescribing implementation:

- **Authorization** (`IMP-001 §6.3`) ↔ **Business Approval** (this ADR, §10 Step 1).
- **Business Rule Execution / Business Object Update** (`IMP-001 §6.3`) ↔ **Infrastructure Allocation** (this ADR, §10 Step 2).
- **Provisioning** (this ADR, §10 Step 3) sits downstream of the lifecycle's own "Business Object Update," as a separate technical-execution concern this ADR does not address.

This alignment is stated as **structural consistency**, not as a Technical Design or an implementation prescription — no Business Activity, endpoint, or service is authorized, created, or designed by this ADR (§17, §19).

## 17. Architectural Consequences

### Positive
- Clear separation of business authorization and infrastructure allocation.
- Stronger separation of duties than any single-authority alternative.
- Better auditability — two independently recorded decisions rather than one undifferentiated act.
- Reduced risk of unauthorized Tenant creation.
- Alignment with `ADR-024`.
- Alignment with `ADR-025`.
- Alignment with `IMP-001 §6.3`'s own Authorization→Execution structure.
- Preserves future implementation flexibility — neither step's own role is committed to by this ADR.

### Negative / unresolved
- Introduces an additional governance step relative to a single-authority model.
- Exact role identities for both Approval and Allocation remain unresolved (§11, §12 — PENDING CANONICAL BINDING).
- Tenant system-of-record mechanism remains unresolved (unchanged from `ADR-024`).
- Provisioning architecture remains unresolved (§13).
- Additional architectural decisions remain necessary before C-040 can proceed (§18, §20).
- C-040 remains RED — Not Implementation Ready (§18).

## 18. C-040 Impact

**This decision resolves:** the constitutional question of *what type* of authority approves versus allocates a Tenant — the provisioning-approval-model clause of `PE-001-C040` BR-C040-13, complementing `ADR-024`'s own resolution of *which layer* owns allocation (BR-C040-15/INV-C040-17).

**This decision does NOT make C-040 implementation-ready.** **C-040 remains RED — Not Implementation Ready**, because the following remain unresolved:

- Canonical identity of the approval authority (§11).
- Canonical identity of the allocation authority (§12).
- Tenant system-of-record mechanism.
- `tenant_registry`'s own adoption status (unchanged — DEFERRED).
- `PE-001-C040`'s own document synchronization (`IRA-C040 §14`'s Document Synchronization Debt Register, untouched by this ADR).
- Subsequent C-040 architectural reconciliation.
- Business Activity ratification.
- A fresh IRA/readiness assessment (`CLAUDE.md §19.7`).

## 19. Explicit Non-Decisions

This ADR does **not** decide:

- `PLATFORM_ADMIN` vs. `AUREX_ADMIN` — not resolved, not conflated, not canonized as the Tenant approval authority.
- `ADR-002` — remains Proposed and unresolved, untouched by this ADR.
- Tenant system of record — remains UNRESOLVED (unchanged from `ADR-024`).
- `tenant_registry` — **remains DEFERRED.** This ADR does not adopt, reject, activate, authorize building, or establish it as the Tenant system of record.
- Tenant database schema.
- API design.
- Provisioning architecture (§13).
- Tenant migration.
- Tenant offboarding.
- Cross-tenant sharing.
- Any C-040 Business Activity definition, charter, or ratification.
- WP-16 or any Work Package.
- Implementation authorization of any kind.

## 20. Remaining Open Decisions

**ADR-024 — Tenant authority layer** *(Accepted)*
→ **ADR-025 — 1:1 Tenant–Organization** *(Accepted)*
→ **ADR-026 — Dual approval/allocation authority model** *(this ADR — Accepted)*
→ **Specific role identity for Business Approval Authority** *(still open — PENDING CANONICAL BINDING)*
→ **Specific role identity for Infrastructure Allocation Authority** *(still open — PENDING CANONICAL BINDING)*
→ **Tenant system-of-record decision** *(still open)*
→ **C-040 architectural reconciliation**
→ **Business Activity ratification**
→ **IRA re-assessment**
→ **implementation authorization**

## 21. Related Artifacts

- `architecture/06-Reviews/ROD-C040-Tenant-Approval-Allocation-Authority.md` — the decision brief this ADR formalizes.
- `architecture/07-Decisions/ADR-024_Tenant_Infrastructure_Layer_Authority.md` — the prior decision this ADR builds on.
- `architecture/07-Decisions/ADR-025_Tenant_Organization_Cardinality.md` — the prior decision this ADR builds on.
- `architecture/07-Decisions/ADR-002_AuthService_Seed_Role_Catalog_Reconciliation.md` — the unresolved `PLATFORM_ADMIN`/`AUREX_ADMIN` naming question this ADR explicitly declines to resolve.
- `architecture/05-Implementation/IRA-C040_Tenant_Administration_Business_Function_and_Implementation_Readiness_Assessment.md` — the readiness assessment that first surfaced this gap.
- `docs/Product/PE-001/capabilities/C-040/PE-001-C040_Tenant_Administration.docx` — the governed specification whose BR-C040-13/BR-C040-15 named this gap; not modified by this ADR.

## 22. Approval Record

| Field | Value |
|---|---|
| **Decision** | Option D — Dual / Two-Step Authority |
| **Decision Authority** | Repository Owner |
| **Decision Date** | 2026-08-25 |
| **Source Decision Brief** | `ROD-C040-Tenant-Approval-Allocation-Authority.md` |
| **Status** | Accepted |

---

## 23. Consequences Summary (Repository State After This ADR)

| Item | Status |
|---|---|
| C-040 Primary Specification | SD-002 (unchanged) |
| Tenant identity/allocation/boundary authority layer | Infrastructure/technical-architecture (unchanged, `ADR-024`) |
| Tenant–Organization cardinality | 1:1 (unchanged, `ADR-025`) |
| Tenant approval/allocation authority model | **Dual/two-step (business approval + infrastructure allocation) — decided by this ADR** |
| Business Approval Authority role identity | PENDING CANONICAL BINDING |
| Infrastructure Allocation Authority role identity | PENDING CANONICAL BINDING |
| `tenant_registry` | DEFERRED (unchanged) |
| Tenant system of record | UNRESOLVED (unchanged) |
| `PLATFORM_ADMIN` / `AUREX_ADMIN` (`ADR-002`) | Proposed, unresolved (unchanged, untouched) |
| C-040 readiness classification | RED — Not Implementation Ready (unchanged; this ADR does not upgrade it) |
