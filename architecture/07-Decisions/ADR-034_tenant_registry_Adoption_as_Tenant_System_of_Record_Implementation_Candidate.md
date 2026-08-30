# ADR-034 — `tenant_registry` Adoption as the Tenant System-of-Record Implementation, Conditional on Disclosed Remediation

**Status:** Accepted
**Classification:** Architecture Governance / Tenant System-of-Record Implementation Selection (Multi-Tenancy)
**Decided by:** Repository Owner (architecture governance authority), 2026-08-25, selecting `tenant_registry` as the concrete implementation of the first-class Tenant domain `ADR-027` already established as the architectural model, following `ROD-C040-Tenant-System-of-Record.md §9`'s own evidentiary analysis and `ROD-C040-Blocker-Closure-Assessment.md`'s own closure-plan identification of this decision as the single remaining Category-A architectural gap.
**Affected Documents:** None amended by this ADR. `ADR-027`, `ADR-025`, `ADR-024`, `ADR-026`, `ADR-029`, `AI-001`, `AI-002`, `ROD-C040-Tenant-System-of-Record.md`, `ROD-C040-Blocker-Closure-Assessment.md`, `SD-002`, and `Master_Technical_Architecture.md` are read-only evidentiary sources this ADR builds upon; none is modified (§16).
**Affected Code:** None. No migration, model, router, service, schema, or test is created or modified by this ADR. `tenant_registry`'s own draft `CREATE TABLE` definition in `Master_Technical_Architecture.md` is not edited by this ADR.

---

## 1. Context

`ADR-027` established the *architectural model* for the Tenant system of record: a first-class, dedicated infrastructure domain, distinct from Organization, with `tenant_registry` named as "an implementation candidate for the first-class Tenant domain this ADR establishes — not the approved system of record, not adopted, not activated" (`ADR-027 §13.3`). `ADR-027 §13.4` explicitly named the next required step: **"Adoption of the existing `tenant_registry` draft... requires a separate, explicit architectural/design decision, covering at minimum: architectural conformance to `SD-002 §2`; schema/domain-model reconciliation; 1:1 enforcement (§13.1); lifecycle model; versioning; event model; identity semantics; migration; integration impact on other capabilities currently scoping only by `organization_id`; and C-040 reconciliation. None of this work is performed by this ADR."** `ROD-C040-Blocker-Closure-Assessment.md §3` (item 5) subsequently identified this exact adoption decision as the single Category-A blocker remaining in the entire C-040 closure path — the one gap not already resolved by `ADR-024`–`ADR-033`/`AI-001`/`AI-002`. This ADR performs that separate, explicitly-anticipated decision, and only that decision.

## 2. Problem

`IRA-C040 §8` found C-040's Gate 3 (Domain) an unconditional FAIL: "Core entities are not defined as canonical Business Objects anywhere. Zero CBOR registration, zero Backend model, zero migration." Without a canonically-selected concrete system-of-record mechanism, `AI-001`'s and `AI-002`'s own constituted authorities have nothing to allocate an identity *into* — the Infrastructure Allocation Authority's own MAY list (`ADR-029 §11`, `AI-002 §6`) permits it to "establish the Tenant identity/boundary allocation itself," but no canonical mechanism exists anywhere for that allocation to be recorded. This ADR resolves *which* mechanism is the selected candidate — it does not resolve *whether that mechanism is yet fit for production use*, which remains explicitly conditional (§7–§9).

## 3. Decision

**`tenant_registry` (`Master_Technical_Architecture.md`, AMD-002) is ADOPTED as the concrete implementation candidate for the Tenant system of record `ADR-027` already established as the architectural model.**

This adoption is **explicitly and entirely conditional** on the remediation scope enumerated in §7, drawn without addition from `ADR-027 §13.1`/`§13.2`/`§13.4` and `ROD-C040-Tenant-System-of-Record.md §9`/`§13`. **The current draft schema is NOT declared `SD-002`-conformant by this ADR merely because it is adopted as the selected candidate.** No implementation, migration, code, API, Business Activity, or production use of `tenant_registry` is authorized by this ADR (§10).

## 4. Three Distinct Layers — Kept Explicit

Per the assigning task's own required distinction:

- **ARCHITECTURAL ADOPTION** (this ADR's own effect): `tenant_registry` is selected as the concrete mechanism implementing `ADR-027`'s already-established model. Nothing more.
- **CONFORMANCE REMEDIATION** (required, not performed): `tenant_registry`'s own draft must be brought into conformity with the already-established canonical requirements enumerated in §7 before any production or implementation use.
- **IMPLEMENTATION AUTHORIZATION**: **NOT granted by this ADR**, under any circumstance, for any purpose (§10).

## 5. ADR-027's Architectural Model Remains Authoritative

`ADR-027`'s own decision — Tenant as a first-class infrastructure/domain concept requiring a dedicated authoritative system of record, distinct from Organization — is not reopened, reinterpreted, or narrowed by this ADR. This ADR does not select `tenant_registry` "as-is" — it selects it as the *candidate mechanism*, exactly as `ADR-027 §13.3`/`§13.4` already anticipated this exact follow-on decision would eventually do, subject to the remediation `ADR-027` itself already disclosed as required (§13.1/§13.2, restated in full at §7 below, not reopened or narrowed).

## 6. Preserved, Unaffected by This ADR

- **`ADR-025`'s 1:1 Tenant–Organization cardinality** remains authoritative, unmodified. §7 item 1 below exists specifically to bring `tenant_registry` into conformance with it, not to reopen it.
- **`ADR-024`, `ADR-026`, `ADR-029`, `AI-001`, `AI-002`** — the entire authority-separation architecture — remain authoritative, unmodified. §8 below restates, not narrows, this separation.
- **`AI-001`/`AI-002`'s own boundaries** (membership, quorum, voting, chair, tenure for the Business Governance Authority; accountability point, executor for the Infrastructure Allocation Authority) remain exactly as those Instruments left them — not touched, resolved, or narrowed by this ADR.
- **`ADR-002`'s bypass-scope follow-on question** — unaffected, not addressed here, consistent with `ROD-C040-Blocker-Closure-Assessment.md §3` item 15's own finding that it does not gate C-040.
- **Migration, offboarding, and cross-tenant-sharing approval authority** — unaddressed by this ADR, consistent with `ROD-C040-Blocker-Closure-Assessment.md §3` item 16's own finding that these remain out of scope for the establishment-only closure path this ADR is part of.

## 7. Required Conformance Remediation Scope — Enumerated From Existing Evidence, Nothing Added

Drawn exactly from `ADR-027 §13.1`/`§13.2`, `ROD-C040-Tenant-System-of-Record.md §4`/`§9`/`§13`, and re-confirmed by direct inspection of `Master_Technical_Architecture.md`'s own `tenant_registry`/`organization_master` `CREATE TABLE` definitions. **No additional defect is invented beyond what these sources already disclosed.**

1. **1:1 cardinality enforcement (`ADR-025`).** The current draft's `organization_master.tenant_id` is a nullable FK to `tenant_registry.tenant_id` with **no uniqueness constraint** — nothing in the schema itself prevents two `organization_master` rows from referencing the same Tenant, contradicting `ADR-025`'s own accepted 1:1 cardinality (`ADR-027 §13.1`, `ROD-C040-Tenant-System-of-Record.md §4`'s own new finding at the time). Remediation requires a uniqueness constraint (or equivalent enforcement) on the referencing side.
2. **`SD-002 §2` Universal Business Object Model conformance (`ADR-027 §13.2`).** The current draft lacks: **versioning** (`SD-002-010`); an **event-sourced, configurable lifecycle** (`SD-002-008`/`-009`) — `active_flag` is a bare boolean, not a lifecycle; and **CBOR registration** (`SD-002-004`'s own operationalizing registry — `CBOR-INDEX.md` carries no Tenant entry, independently reconfirmed across this decision sequence).
3. **Actor-reference fields.** The current draft carries no `allocated_by`, `approved_by`, or `created_by`-equivalent column of any kind (`ROD-C040-Infrastructure-Allocation-Authority-Resolution.md §11`, `ROD-Meta-Governance-Stage-3-Appointment-Authority.md §5`, both independently re-confirmed earlier in this decision sequence, restated here without re-deriving). Remediation requires adding reference fields sufficient to record the Business Approval decision reference, the Infrastructure Allocation decision reference, and — once appointed — the actual appointer/accountability-point identity (per `AI-001 §11`/`AI-002 §11`'s own Appointment Instrument field specification), consistent with `SD-002-056`'s "no approval exists without an audit record" requirement.
4. **`organization_master.tenant_id` FK-direction and referential-integrity reconciliation.** Beyond the uniqueness constraint (item 1), the eventual schema/domain-model reconciliation `ADR-027 §13.4` itself lists must confirm this FK direction remains architecturally correct (Organization referencing Tenant, per `ROD-C040-Tenant-System-of-Record.md §10`'s own finding) before any implementation.
5. **CMD-001 §26.3a Business Object eligibility analysis**, per `ROD-C040-Tenant-System-of-Record.md §9` item 4(a) and `ADR-027 §16` — required before formal CBOR registration, not performed by this ADR.
6. **Integration-impact review** for any capability currently scoping only by `organization_id`, to evaluate whether `tenant_id` scoping is also required — per `ROD-C040-Tenant-System-of-Record.md §9` item 5, restated, not performed here.

**This enumeration is exhaustive of what the cited sources already disclosed. No new defect is asserted beyond it.**

## 8. Authority Separation — Restated, Not Narrowed

Consistent with `ADR-024`, `ADR-026`, `ADR-029`, `AI-001`, and `AI-002`, all unmodified:

- **`tenant_registry` does not itself constitute, become, or substitute for the Business Approval Authority, the Infrastructure Allocation Authority, or the Technical Provisioning Authority.** A system of record is a persistence mechanism; it is not, and cannot become, a constitutional decision-making authority merely by being selected as the record those authorities' own decisions are written into.
- **Tenant identity allocation, once implemented, must be performed by the Infrastructure Allocation Authority** (`ADR-024`, `ADR-026`, `ADR-029 §11`, `AI-002`) — `tenant_registry`, once remediated, is the record that allocation is written *into*, never the actor performing the allocation itself.
- **No provisioning behavior is authorized by this decision.** Technical Provisioning Authority remains entirely unresolved (`ADR-026 §13`, `ROD-C040-Blocker-Closure-Assessment.md §3` item 3), and this ADR does not touch it, narrow it, or imply an answer to it.

## 9. Tenant System-of-Record Custodianship — Not Resolved, Except Where Inseparable

**This ADR does not resolve System-of-Record custodianship as a governance question** (`AI-001 §10`, `AI-002 §10`, `ADR-027 §11`'s own "not assumed to travel with either authority") — that remains open, exactly as every prior artifact in this sequence left it. The one narrow point this ADR necessarily touches, because it is inseparable from *which mechanism* is selected: `tenant_registry` is a `Master_Technical_Architecture.md`-hosted schema, not itself an organizational custodian — selecting it as the mechanism does not, by itself, name which team, service, or role is operationally responsible for it. That remains a separate, future decision.

## 10. Implementation Authorization — Explicitly Not Granted

This ADR does **not** authorize: any code, migration, schema change, or API touching `tenant_registry`; production deployment of any kind; Business Activity creation; `WP-16` or any Work Package; or `tenant_registry`'s own transition out of its current DEFERRED status as recorded in `SER-001` SE-052. **`tenant_registry`'s DEFERRED status in `SER-001` is unaffected by this ADR** — this ADR selects it as the *architectural candidate*, consistent with `ADR-024 §15`'s own framing that adoption-as-candidate and adoption-as-implementation-authorized are two separate acts; only the former is performed here.

## 11. Consequences

**Positive:**
- Closes the single Category-A architectural gap `ROD-C040-Blocker-Closure-Assessment.md §3`/§5 identified as the last remaining constitutional blocker in the C-040 closure path.
- Gives `AI-001`'s and `AI-002`'s own constituted authorities a named target mechanism their eventual decisions will be recorded into, once remediated.
- Provides a concrete, bounded remediation scope (§7) for any future implementation work, rather than an open-ended "fix `tenant_registry`" instruction.

**Negative / deferred:**
- `tenant_registry` remains non-conformant as drafted — this ADR does not close that gap, only names it precisely.
- System-of-Record custodianship remains open (§9).
- Technical Provisioning Authority remains open (`ADR-026 §13`).
- Migration, offboarding, and cross-tenant-sharing approval authority remain open (`ROD-C040-Blocker-Closure-Assessment.md §3` item 16).
- No implementation timeline is established or implied.

## 12. C-040 Impact

Per `ROD-C040-Blocker-Closure-Assessment.md §3` item 5, this ADR resolves the system-of-record *mechanism selection* half of that item — the *remediation work itself* (§7) and *actual CBOR registration/schema build* remain outstanding, unauthorized, future implementation work. **C-040 remains RED — Not Implementation Ready.** The closure plan's own remaining steps (`ROD-C040-Blocker-Closure-Assessment.md §4`) — Business Governance Authority membership-structure decision, further Key-2 appointments (`AI-003`/`AI-004`), minimum-scope BA-charter scoping decision, and a fresh IRA re-assessment — are all unaffected and unperformed by this ADR.

## 13. Explicit Non-Decisions

This ADR does **not**:

- Declare `tenant_registry`'s current draft `SD-002`-compliant.
- Authorize any code, migration, schema change, or API.
- Authorize production deployment of `tenant_registry`.
- Create any Business Activity.
- Authorize `WP-16` or any Work Package.
- Resolve Technical Provisioning Authority.
- Resolve Tenant System-of-Record custodianship, except the narrow point named in §9.
- Resolve executor relationships for either C-040 authority.
- Resolve request-intake mechanics.
- Resolve membership, quorum, voting, chair, or tenure for `AI-001`, or the accountability point/executor for `AI-002`.
- Resolve migration, offboarding, or cross-tenant-sharing approval authority.
- Resolve `ADR-002`'s own bypass-scope follow-on question.
- Modify `SD-002`, `PE-001-C040`, `URA-001`, `RTA-001`, `ARCH-000`, `CMD-001`, `CLAUDE.md`, `ADR-024`–`ADR-033`, `AI-001`, or `AI-002`.
- Change `tenant_registry`'s own DEFERRED status in `SER-001`.
- Change C-040's implementation-readiness status — remains RED.

## 14. Decision History

| Date | Event | Status After |
|---|---|---|
| 2026-08-25 | `ADR-027` establishes the Tenant system-of-record architectural model; names `tenant_registry` as a candidate mechanism only, explicitly deferring its own adoption to a separate decision (`§13.3`/`§13.4`). | Model accepted; mechanism selection deferred |
| 2026-08-25 | `AI-001`/`AI-002` constitute both C-040 authorities via the Two-Key mechanism; neither touches system-of-record adoption. | Authorities exist; mechanism still unselected |
| 2026-08-25 | `ROD-C040-Blocker-Closure-Assessment.md` identifies `tenant_registry` adoption as the single remaining Category-A architectural gap in the C-040 closure path. | Gap precisely scoped |
| 2026-08-25 | Repository Owner selects `tenant_registry` as the concrete implementation candidate, conditional on disclosed remediation. | This ADR drafted |
| 2026-08-25 | This ADR accepted. | **Accepted** |

## 15. Approval Record

| Field | Value |
|---|---|
| Decision | `tenant_registry` adopted as the concrete Tenant System-of-Record implementation candidate, conditional on disclosed remediation |
| Decision Authority | Repository Owner |
| Decision Date | 2026-08-25 |
| Source Decision Briefs | `ROD-C040-Tenant-System-of-Record.md`; `ROD-C040-Blocker-Closure-Assessment.md` |
| Status | Accepted |
| Remediation performed | None — enumerated only (§7) |
| Implementation authorized | None |
| C-040 impact | System-of-record mechanism selected; remediation and build remain outstanding; C-040 remains RED |

---

## Change Control

**Files created:** this document only — `architecture/07-Decisions/ADR-034_tenant_registry_Adoption_as_Tenant_System_of_Record_Implementation_Candidate.md`.

**Files NOT modified:** `ADR-024`–`ADR-033`, `AI-001`, `AI-002`, `SD-002`, `PE-001-C040`, `URA-001`, `RTA-001`, `ARCH-000`, `CMD-001`, `CLAUDE.md`, `Master_Technical_Architecture.md` (including `tenant_registry`'s own `CREATE TABLE` definition — inspected, not edited), `SER-001`, `CAP-001`, every prior `ROD-*` brief, and any backend/frontend code.

**No implementation performed:** no code, migration, API, schema change, or Business Activity was created or modified; `WP-16` was not created or authorized; `tenant_registry` was not built, deployed, or removed from its DEFERRED status in `SER-001`; no authority members were appointed; no Technical Provisioning, custodianship, executor, or request-intake question was resolved. `ADR-024`–`ADR-033` remain Accepted, unchanged. C-040 remains RED — Not Implementation Ready.
