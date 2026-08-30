# ADR-029 — Tenant Business Approval Authority and Infrastructure Allocation Authority: Architectural Model and Authority Boundaries

**Status:** Accepted
**Classification:** Architecture Governance / Constitutional Authority-Model Specification (Multi-Tenancy)
**Decided by:** Repository Owner (architecture governance authority), 2026-08-25, formalizing the architectural model and authority boundaries developed across `ROD-C040-Tenant-Authority-Governance-Gap.md`, `ROD-C040-Business-Governance-Authority-Definition.md`, `ROD-C040-Infrastructure-Allocation-Authority-Resolution.md`, and `ROD-C040-Infrastructure-Allocation-Authority-Definition.md` (`architecture/06-Reviews/`).
**Affected Documents:** None amended by this ADR. `ADR-026` (which this ADR specializes, not supersedes), `URA-001`, `SD-002`, `RTA-001`, and `Master_Technical_Architecture.md` are read-only evidentiary sources; none is modified (§18).
**Affected Code:** None. No migration, model, router, service, schema, or test is created or modified by this ADR.

---

## 1. ADR ID

`ADR-029`

## 2. Title

Tenant Business Approval Authority and Infrastructure Allocation Authority: Architectural Model and Authority Boundaries

## 3. Status

**Accepted.** The Repository Owner directed this joint ADR be drafted to formalize the architectural model and authority boundaries the four cited decision-support briefs already developed — explicitly instructing that neither authority's institutional identity, actor type, or executor be invented, created, or canonized by it. Per this repository's own established convention (`ADR-024` through `ADR-028`), this ADR is drafted "Accepted" directly.

## 4. Date

2026-08-25.

## 5. Decision Authority

Repository Owner.

## 6. Context

`ADR-026` (Accepted) established that Tenant establishment uses a dual/two-step authority model — Business Approval, then Infrastructure Allocation, then a separate downstream Technical Provisioning concern — without naming either authority's specific role identity, both left **PENDING CANONICAL BINDING**. Four subsequent decision-support briefs then investigated this gap in depth: `ROD-C040-Tenant-Authority-Governance-Gap.md` confirmed no existing System Role, governance board, or approval mechanism cleanly satisfies either requirement; `ROD-C040-Business-Governance-Authority-Definition.md` proposed a candidate constitutional shape for Business Approval Authority; `ROD-C040-Infrastructure-Allocation-Authority-Resolution.md` confirmed, on an exhaustive evidentiary sweep, that no canonical Infrastructure Allocation actor exists anywhere in the repository; `ROD-C040-Infrastructure-Allocation-Authority-Definition.md` proposed a candidate constitutional shape for Infrastructure Allocation Authority. Each brief was explicit that it proposed a shape only, selected no actor, and created nothing. This ADR formalizes what those four briefs, taken together, actually established as reusable architectural pattern — the model and the boundaries — while preserving, unchanged, the standing position that both specific authority identities remain Repository Owner decisions not yet made.

## 7. Problem

`ADR-026`'s own two-step model is a decision-shape only; it does not itself state what either step's authority may do, must not do, how the two steps relate to each other (beyond sequence), or how either relates to `AUREX_ADMIN`, Organization, Technical Provisioning, or the Tenant System of Record. Without this, any future selection of a specific actor for either role would have to re-derive these boundaries from scratch, and would risk inconsistency between the two steps or with the decision-support work already completed. This ADR closes that gap — formalizing the *rules any eventual actor must operate within*, without selecting who that actor is.

## 8. Evidence

Restated from the four cited briefs, re-verified against primary canonical text where each brief itself did so:

- **`ADR-026 §9`–`§13`**: the dual model itself — "a business/platform authority approves the need for a Tenant to exist," then "the infrastructure/technical-architecture authority subsequently allocates/establishes the canonical Tenant identity and boundary" — both **PENDING CANONICAL BINDING** (`ADR-026 §11`/`§12`).
- **`ROD-C040-Tenant-Authority-Governance-Gap.md §5`–`§11`**: no existing named body (Aurex Governance Board, Industry Intelligence Council, `AUREX_ADMIN`, Corporate Administrator) cleanly fits either authority; the governance-body naming vocabulary itself is unreconciled across `SD-002`, `IMP-001`, `ARCH-000`, `CMD-001`.
- **`URA-001-31`**: the one canonical decide/execute precedent — Aurex Governance Board/Industry Intelligence Council decide, `AUREX_ADMIN` executes — used by the source briefs as a structural analogy, not as a literal grant of Tenant authority to any of the three.
- **`ROD-C040-Infrastructure-Allocation-Authority-Resolution.md §6`–`§11`**: `AUREX_ADMIN` checked directly against five specific infrastructure-allocation powers (Tenant identity, allocation, infrastructure-partition allocation, boundary establishment, resource assignment) and found to hold none of them; `RTA-001` searched in full for any infrastructure-administration terminology, zero matches; `tenant_registry`'s own draft schema (`Master_Technical_Architecture.md`, line 3688) carries no actor-reference column of any kind.
- **`ROD-C040-Business-Governance-Authority-Definition.md §17`** and **`ROD-C040-Infrastructure-Allocation-Authority-Definition.md §12`**: the two proposed authority definitions this ADR formalizes the boundaries of (§9–§10 below), each independently labeled `PROPOSED — NOT CANONICAL` by its own source brief.
- **`ROD-SD002-Enterprise-Data-Council-Resolution.md`**, formalized by `ADR-028`: confirms `AUREX_ADMIN`, Corporate Admin, and Enterprise Data Council are each distinct, and none is established as either C-040 authority — restated here as unaffected context, not reopened.

No evidence beyond what is cited above, or already formalized by `ADR-024`–`ADR-028`, is relied upon for the decision in §9–§14.

## 9. Decision — Architectural Model

**The Tenant establishment lifecycle `ADR-026` already established is formalized, with the first two stages now specified at the boundary level, as follows:**

```text
Tenant Establishment Request
          │
          ▼
┌────────────────────────────────────┐
│ Business Approval Authority         │
│ (identity: PENDING CANONICAL        │
│  BINDING — not selected by this     │
│  ADR, §16)                          │
│                                      │
│ Decides: "Should this Tenant        │
│ exist?"                             │
└──────────────────┬───────────────────┘
                   │ APPROVED
                   │ (a discrete, auditable,
                   │  attributable decision
                   │  record referencing the
                   │  specific request)
                   ▼
┌────────────────────────────────────┐
│ Infrastructure Allocation Authority │
│ (identity: PENDING CANONICAL        │
│  BINDING — not selected by this     │
│  ADR, §16)                          │
│                                      │
│ Decides: "Allocate the canonical    │
│ Tenant identity/boundary."          │
└──────────────────┬───────────────────┘
                   │ ALLOCATED
                   │ (a discrete, auditable,
                   │  attributable decision
                   │  record referencing the
                   │  specific approval it
                   │  allocates against)
                   ▼
┌────────────────────────────────────┐
│ Technical Provisioning              │
│ (authority: entirely undecided —    │
│  ADR-026 §13, not addressed here)   │
│                                      │
│ Provisions required infrastructure  │
│ / resources.                        │
└──────────────────────────────────────┘
```

**This diagram formalizes sequence, decision content, and record-keeping discipline for the first two stages. It does not name, select, or imply any specific actor for either box** — both remain exactly as `ADR-026` left them: **PENDING CANONICAL BINDING** (§16).

## 10. Business Approval Authority — Architectural Boundaries

Formalized from `ROD-C040-Business-Governance-Authority-Definition.md §17`, unchanged in substance:

**Purpose:** to decide whether a specific proposed Tenant should be established.

**Scope:** platform-wide; limited exclusively to the Tenant-establishment admission decision.

**MAY:**
- Decide whether a proposed Tenant should be established.
- Approve or reject a Tenant establishment request, with a stated rationale.
- Produce a discrete, auditable Business Approval decision record referencing the specific request it resolves.
- Delegate execution of an approved decision to a designated execution actor, without thereby transferring the decision authority itself.

**MUST NOT, automatically or by implication:**
- Allocate the Tenant identity (a separate authority, §11).
- Provision infrastructure.
- Modify `tenant_registry` or any Tenant system-of-record table.
- Establish database records directly.
- Administer Organization data.
- Bypass any authorization control, including the certified five-tier Authorization Runtime Engine (`ADR-016`) or `DomainPermission` resolution.
- Perform technical provisioning of any kind.
- Inherit `PLATFORM_ADMIN`'s historical universal-bypass semantics (`ADR-002 §17a`, separately unresolved).
- Be, or be delegated to, a role internal to the Organization whose Tenant is under consideration (self-approval prohibition, §12).

## 11. Infrastructure Allocation Authority — Architectural Boundaries

Formalized from `ROD-C040-Infrastructure-Allocation-Authority-Definition.md §12`, unchanged in substance:

**Purpose:** to allocate the canonical Tenant identity after a valid Business Approval decision and before Technical Provisioning.

**Scope:** infrastructure/technical-architecture layer (`ADR-024`); narrow in function — limited exclusively to the allocation decision itself, not general infrastructure administration.

**MAY:**
- Allocate a canonical Tenant identity for an approved Tenant establishment request.
- Confirm that the request satisfies allocation prerequisites (a valid, referenced Business Approval decision exists).
- Establish the Tenant identity/boundary allocation itself, consistent with `SD-002-108`'s Universal Identity requirement and `ADR-025`'s 1:1 cardinality.
- Record the allocation decision as a discrete, auditable, attributable act referencing the specific Business Approval decision it allocates against.
- Reject an allocation request that lacks a valid, referenced Business Approval decision.
- Delegate the technical execution of the allocation operation to an automated mechanism, where decision and execution are split.

**MUST NOT, automatically or by implication:**
- Decide whether a Tenant should exist in the first place (`ADR-026`'s own Business Approval step, §10).
- Override, second-guess, or substitute its own judgment for a Business Approval decision.
- Approve its own allocation request.
- Create or provision infrastructure resources (Technical Provisioning, a separate, still entirely undecided authority).
- Modify Organization identity or administer Organization data.
- Change Tenant–Organization cardinality (`ADR-025`, Accepted, unaffected).
- Bypass any authorization control, including the certified five-tier Authorization Runtime Engine (`ADR-016`) or `DomainPermission` resolution.
- Inherit `PLATFORM_ADMIN`'s historical universal-bypass semantics (`ADR-002 §17a`, separately unresolved).
- Arbitrarily change an already-allocated Tenant's boundary once established.
- Implement, adopt, or modify `tenant_registry` — remains DEFERRED (§14).
- Change the Tenant schema or any physical implementation detail.
- Migrate existing data of any kind.

## 12. Relationship Between the Two Authorities

**Separation of duties is formalized as a structural requirement, not left to implementation-time convenience.** Restated from `ADR-026 §8` Decision Driver 4 and reinforced by both source definition briefs' own prohibitions (§10, §11 above):

- **No single actor may hold both Business Approval Authority and Infrastructure Allocation Authority for the same Tenant establishment request.** If the same identity performed both, `ADR-026`'s own separation-of-duties rationale would be undermined even while nominally satisfying the two-step *process* shape (two recorded events, but not two independent checks) — this ADR closes that residual risk by formalizing the prohibition directly, rather than leaving it as an inference from `ADR-026`'s own rationale alone.
- **Infrastructure Allocation Authority's decision is strictly gated on receiving a valid, referenced Business Approval decision** (§11's own "MAY... confirm that the request satisfies allocation prerequisites" and "MUST NOT... decide whether a Tenant should exist in the first place"). An allocation record with no referenced Business Approval decision is an invalid state, not a valid shortcut — the same discipline `URA-001-123` already requires for CIL-promotion execution records, applied here by structural analogy.
- **Neither authority may perform Technical Provisioning** — both §10 and §11 prohibit it explicitly. Whether the same actor eventually performs both Infrastructure Allocation and Technical Provisioning remains an open question `ADR-026 §13` already left unresolved and this ADR does not close (§16).

## 13. Relationship to AUREX_ADMIN

**No new relationship is established.** `ADR-002` remains unchanged and unaffected: `AUREX_ADMIN` is the canonical System Role identity; `PLATFORM_ADMIN` remains legacy/interim implementation evidence; the `PLATFORM_ADMIN` universal-bypass semantics remain a separate, unresolved follow-on decision (`ADR-002 §17a`).

This ADR does **not** state that `AUREX_ADMIN` is the Business Approval Authority. This ADR does **not** state that `AUREX_ADMIN` is the Infrastructure Allocation Authority — `ROD-C040-Infrastructure-Allocation-Authority-Resolution.md §6` already checked `AUREX_ADMIN` against the five specific powers Infrastructure Allocation would require and found none granted; this ADR does not overturn that finding. Where `URA-001-31`'s own decide/execute precedent is used as a structural analogy in the source briefs (a governance authority decides, `AUREX_ADMIN` executes), that remains an analogy offered for a *future* Repository Owner decision to accept or reject when the actual authority identities are selected (§16) — this ADR does not itself assign `AUREX_ADMIN` any execution role for either authority.

## 14. Relationship to Technical Provisioning and Tenant System of Record

**Technical Provisioning Authority remains entirely undecided**, exactly as `ADR-026 §13` left it. This ADR does not name, imply, or authorize any actor for it.

**`tenant_registry` remains DEFERRED**, exactly as `ADR-027 §13` left it. This ADR does not adopt, reject, redesign, or otherwise modify it. Both authorities' own boundaries (§10, §11) explicitly prohibit touching it.

**Tenant System-of-Record custodianship is not assumed to travel with either authority.** Per `ROD-C040-Infrastructure-Allocation-Authority-Definition.md §13`'s own explicit distinction, "maintaining the authoritative allocation state" (a Business Approval or Infrastructure Allocation Authority's own recorded decision) is not the same concern as the ongoing stewardship of the Tenant domain's full lifecycle state (`ADR-027`'s own first-class Tenant domain). This ADR preserves that distinction as open, not resolved.

## 15. Consequences

**Positive:**
- Any future Repository Owner selection of either authority's specific identity now has a settled, formalized set of boundaries to conform to, rather than needing to re-derive them from four separate decision-support briefs.
- The separation-of-duties requirement (§12) is now a structural constitutional rule, not merely an inference from `ADR-026`'s own rationale.
- The relationship (or, more precisely, the deliberate absence of a relationship) to `AUREX_ADMIN`, Technical Provisioning, and the Tenant System of Record is now explicit, preventing a future implementation from silently assuming any of these by default.

**Negative / deferred:**
- Neither authority's specific identity is selected — both remain **PENDING CANONICAL BINDING**.
- Neither authority's actor type (System Role, Business Role, Group, Governance Body, technical/system-level mechanism) is selected.
- Neither authority's executor (if decision and execution are split) is selected.
- Technical Provisioning Authority remains entirely undecided.
- Tenant System-of-Record custodianship remains undecided.
- C-040 remains RED — Not Implementation Ready (§16). This ADR does not, by itself, unblock any C-040 Business Activity.

## 16. C-040 Relationship

**This ADR does NOT resolve either C-040 Tenant authority decision.** It does not select, name, or imply an actor for Business Approval Authority. It does not select, name, or imply an actor for Infrastructure Allocation Authority. It does not infer `AUREX_ADMIN`, `PLATFORM_ADMIN`, Corporate Admin, or Enterprise Data Council holds either authority. It does not resolve Technical Provisioning Authority or Tenant System-of-Record custodianship.

**Both Decision 1 (Business Approval Authority) and Decision 2 (Infrastructure Allocation Authority) remain PENDING CANONICAL BINDING**, exactly as `ADR-026 §11`/`§12` left them — this ADR specializes the *boundaries* those pending authorities will operate within; it does not narrow the field of who they might be, and does not upgrade either decision's own status from pending to resolved.

**C-040 remains RED — Not Implementation Ready.** `ADR-024`, `ADR-025`, `ADR-026`, `ADR-027`, and `ADR-028` all remain Accepted, unchanged, and unaffected by this ADR.

## 17. Explicit Non-Decisions

This ADR does **not**:

- Select, name, or create the Business Approval Authority.
- Select, name, or create the Infrastructure Allocation Authority.
- Determine either authority's actor type (System Role, Business Role, Group, Governance Body, technical/system-level mechanism, or any other construct).
- Assign an executor to either authority.
- Assign Tenant System-of-Record custodianship to any actor.
- Resolve Technical Provisioning Authority.
- Modify `AUREX_ADMIN`'s canonical definition or authorization scope.
- Modify `PLATFORM_ADMIN`'s status.
- Modify `URA-001`, `SD-002`, `ERG-001`, or `RTA-001`.
- Modify `ADR-002`, `ADR-024`, `ADR-025`, `ADR-026`, `ADR-027`, or `ADR-028`.
- Modify the Authorization Runtime Engine or `DomainPermission`.
- Adopt, reject, or modify `tenant_registry`.
- Create a System Role, Business Role, Group, Governance Body, or any other role/authority construct.
- Create code, migrations, or APIs.
- Create any Business Activity.
- Authorize `WP-16` or any Work Package.
- Authorize implementation of any kind.

## 18. Future Canonicalization

The following remain open, separate constitutional decisions, not performed by this ADR:

1. **Business Approval Authority identity selection** — among the options `ROD-C040-Tenant-Authority-Role-Identity-Decision.md` and `ROD-C040-Business-Governance-Authority-Definition.md` already evaluated (a new dedicated governance body being the best-evidenced shape, per the latter brief's own §16, not selected).
2. **Infrastructure Allocation Authority identity selection** — among the options `ROD-C040-Infrastructure-Allocation-Authority-Definition.md §7`–`§10` already evaluated (a new technical/system-level authority being the best-evidenced shape, not selected).
3. **Executor selection for either authority**, if decision and execution are split.
4. **Tenant System-of-Record custodianship** (§14).
5. **Technical Provisioning Authority** (§14, `ADR-026 §13`).
6. **The broader governance-vocabulary reconciliation** (`Aurex Governance Board` / `Aurex Architecture Governance Board` / `Architecture Board` / `Enterprise Architecture Board`, disclosed by `ROD-C040-Business-Governance-Authority-Definition.md §4`) — unaffected by, and not required as a precondition for, either of the above selections, since both proposed authority shapes were deliberately defined independent of it.

## 19. Decision History

| Date | Event | Status After |
|---|---|---|
| 2026-08-25 | `ADR-026` establishes the dual/two-step model; both role identities left PENDING CANONICAL BINDING. | Model accepted; actors pending |
| 2026-08-25 | `ROD-C040-Tenant-Authority-Governance-Gap.md` confirms no existing actor cleanly fits either role. | Governance gap confirmed |
| 2026-08-25 | `ROD-C040-Business-Governance-Authority-Definition.md` proposes a candidate shape for Business Approval Authority (PROPOSED — NOT CANONICAL). | Shape proposed, not selected |
| 2026-08-25 | `ROD-C040-Infrastructure-Allocation-Authority-Resolution.md` confirms no existing actor for Infrastructure Allocation Authority. | Governance gap confirmed |
| 2026-08-25 | `ROD-C040-Infrastructure-Allocation-Authority-Definition.md` proposes a candidate shape for Infrastructure Allocation Authority (PROPOSED — NOT CANONICAL). | Shape proposed, not selected |
| 2026-08-25 | Repository Owner directs a joint ADR formalizing the architectural model and boundaries only, explicitly excluding actor selection. | This ADR drafted |
| 2026-08-25 | This ADR accepted. | **Accepted** |

## 20. Approval Record

| Field | Value |
|---|---|
| Decision formalized | Architectural model and authority boundaries for Business Approval Authority and Infrastructure Allocation Authority, per `ADR-026`'s own dual model |
| Decision Authority | Repository Owner |
| Decision Date | 2026-08-25 |
| Source Decision Briefs | `ROD-C040-Tenant-Authority-Governance-Gap.md`; `ROD-C040-Business-Governance-Authority-Definition.md`; `ROD-C040-Infrastructure-Allocation-Authority-Resolution.md`; `ROD-C040-Infrastructure-Allocation-Authority-Definition.md` |
| Status | Accepted |
| Business Approval Authority identity | PENDING CANONICAL BINDING — not selected by this ADR |
| Infrastructure Allocation Authority identity | PENDING CANONICAL BINDING — not selected by this ADR |
| C-040 impact | None — C-040 remains RED |

---

## Change Control

**Files created:** this document only — `architecture/07-Decisions/ADR-029_Tenant_Business_Approval_and_Infrastructure_Allocation_Authority_Architectural_Model.md`.

**Files NOT modified:** `URA-001`, `SD-002`, `ERG-001`, `RTA-001`, `Master_Technical_Architecture.md`, `IMP-001`, `ADR-002`, `ADR-016`, `ADR-024`, `ADR-025`, `ADR-026`, `ADR-027`, `ADR-028`, every prior `ROD-*` brief, `tenant_registry`, the Authorization Runtime Engine, `DomainPermission`, `CAP-001`, `SER-001`, `CLAUDE.md`, and any backend/frontend code.

**No implementation performed:** no System Role, Business Role, Group, Board, Committee, or Council was created; no executor was assigned; no Tenant authority was assigned to any specific actor; no database schema, migration, or API was created or modified; no Business Activity was created; `WP-16` was not created or authorized; `tenant_registry` was not adopted.

**Status transition:** N/A — this is a new ADR, drafted and accepted in the same action, per the same convention `ADR-024`–`ADR-028` already established.
