# ROD-C022 — Customer & Account Management: Capability-Boundary and Minimum-Scope Decision

**Document type:** Repository Owner Decision record — a decision brief followed by recorded Repository Owner decisions, preceding the formal governance artifact (`IRA-C022`, a future, separately-authorized pass) that will cite it. Same class and structure as `ROD-C021-Product-and-Service-Catalog-Capability-Boundary-and-Minimum-Scope.md` and `ROD-C132-Enterprise-Notifications-Capability-Boundary-and-Minimum-Scope.md`.

**Capability:** C-022 Customer & Account Management (`CAP-001` line 76 — Active, Domain D-002 Commercial & Subscription, owning specification **`COM-001`** — Commercial & Subscription Architecture, certified LOCKED under EARB Constitutional Recertification CR-3.0).

**Recorded:** 2026-09-15, per direct Repository Owner instruction ("AUREX — C-022 REPOSITORY OWNER DECISION"), following two prior read-only investigations (this same session): "AUREX — C-020 SUBSCRIPTION MANAGEMENT — CAPABILITY-BOUNDARY & DELIVERY-READINESS INVESTIGATION" (which established that C-020 cannot proceed without a genuine Customer/Account reference, and that `COM-001-033` prohibits substituting Organization for it) and "AUREX — C-022 CUSTOMER & ACCOUNT MANAGEMENT — CAPABILITY-BOUNDARY & DELIVERY-READINESS INVESTIGATION" (which read `PE-001-C022_Customer_and_Account_Management.docx` v1.2 in full — 1 CRB / 8 ERBs / 17 EXs — `COM-001 §7`, `CAP-001`, the delivery map, and performed a repository-wide implementation-readiness search).

**Authority:** Repository Owner (same decision-authority pattern established for `C-021`'s own pre-IRA decisions recorded in `ROD-C021`, `C-132`'s own pre-IRA decisions recorded in `ROD-C132`, and `C-040`'s pre-IRA decisions recorded in the delivery map).

**Classification key:** `[FACT]` — repository fact / verbatim from a LOCKED or Active source. `[RO DECISION]` — a Repository Owner decision, now made. `[PRECEDENT]` — established by a completed, certified Work Package. `[FUTURE IRA QUESTION]` — deferred to `IRA-C022`. `[FUTURE TDS QUESTION]` — deferred to a finalized `TDS-C022`.

---

## A. Executive Decision Summary

`[FACT]` C-022 has no hard dependency on any unbuilt capability. Unlike C-020 (whose Anchor step structurally requires a Customer/Account reference that does not yet exist, per the prior investigation), C-022's own establishment path (`ERB-C022-01`) lists its dependencies as "PE-001 Context Preservation Model" only. `[FACT]` `COM-001-033` (LOCKED) explicitly forecloses the one shortcut that could otherwise have made C-022 unnecessary: a Commercial Account is *"never equivalent to a Workspace, Organization, Identity, Membership, ERP company code, CRM account record, or Billing Account."* `[FACT]` C-022 has **zero implementation** anywhere in the repository (confirmed by repository-wide search).

The Repository Owner **decides** six bounded items:

- **D1** — first delivery slice: **Option A** — Establish Commercial Account (not Customer, not both in parallel).
- **D2** — scope model: **Option A — Platform-global.** Explicitly *not* inferred from C-021; recorded on C-022's own basis (see §E).
- **D3** — service hosting: **Option A — `AuthService`.**
- **D4** — Identity/Person references: **Option A** — deferred entirely from BA-01.
- **D5** — BA-01 boundary: authorized **exactly and only** "Establish Commercial Account," per the exclusion list in §H.
- **D6** — next governance step: **`IRA-C022` preparation authorized. TDS, Charter, and implementation are explicitly NOT authorized by this decision.**

**This document advances the C-022 governance sequence exactly one step: capability-boundary + minimum-scope decided. It does not authorize `IRA-C022` acceptance, `TDS-C022`, a WP registration, a BA-01 charter, implementation, schema, migration, API, frontend, CBOR registration, an ADR, a commit, or a push. It does not reopen C-020's own unresolved decisions, does not alter C-021 or WP-20, and does not reconcile the outstanding `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md` changes.**

---

## B. C-022 Definition

- `[FACT]` `CAP-001` line 76: `| C-022 | Customer & Account Management | Manage customer relationships. | COM-001 | Active |`. Domain **D-002 Commercial & Subscription**.
- `[FACT]` Business Intent, verbatim (`PE-001-C022 §1.2`, "not paraphrased, not expanded, not redefined"): **"Manage customer relationships."**
- `[FACT]` C-022 is a **dual-construct capability** (`PE-001-C022 §1.3`): it maintains two related but independently-keyed authoritative facts — Customer identity and Commercial Account — plus a third, the Customer–Account Relationship, corrected into an independent authority in v1.1 specifically to remove an earlier many-to-many ambiguity.
- `[FACT]` `PE-001-C022` Guiding Architectural Question: the enterprise's single, continuously authoritative representation of *"who its Customer is and which Commercial Account that Customer's relationship is organized through,"* without that representation ever becoming, or being derived from, Identity (C-001/URA-001), Organization (C-004), Person (C-006), Workspace (C-008), Subscription (C-020), Offering (C-021), Entitlement (C-023), Billing (C-024), Contract (C-025), Tenant (C-040), Access (C-002), or a CRM/ERP system-of-engagement record.

---

## C. Constitutional / PE-001 Basis

| Source | Status | Relevance |
|---|---|---|
| `COM-001` — Commercial & Subscription Architecture | **LOCKED** (EARB, CR-3.0) | Primary Specification. §4 Universal Commercial Construct Model; §7 (`COM-001-030`–`036`) the Customer / Commercial Account (C-022) canonical model. |
| `PE-001-C022_Customer_and_Account_Management.docx` | v1.2, **Active** | Enterprise Experience Specification. 1 CRB-C022; 8 ERBs (Establish / Understand / Frame Lifecycle Intent / Frame Structural Intent / Shape & Assess / Commit / Distribute Reference / Resolve Disruption); 17 EXs. |
| `COM-001-033` | LOCKED | *"Authoritative Account Context... Never equivalent to a Workspace, Organization, Identity, Membership, or Billing Account."* The load-bearing clause ruling out an Organization-reuse shortcut. |
| `COM-001-036` | LOCKED | The Customer Reference, Commercial Account Reference, and/or Customer–Account Relationship Reference are each independently available for downstream consumption — establishes that C-020 may anchor on *either* reference, not only a combined one. |
| `ROD-C021` §E (D2 — C-021↔C-022 Boundary) | Prior RO decision | Already confirmed C-021 has no dependency on C-022 in the reverse direction; consistent with this document's own findings. |

---

## D. D1 — First Delivery Slice

`[FACT]` `PE-001-C022 §1.16`/`ERB-C022-01` permit anchoring on *"a partial candidate Customer or Account reference"* — either construct alone is a valid, non-contradictory starting state. `[FACT]` `COM-001-036` confirms downstream capabilities may consume *"the Customer Reference, Commercial Account Reference, and/or..."* — C-020's own Anchor (`COM-001-011`) does not require both.

`[RO DECISION — D1]` **Option A: Establish Commercial Account as the first C-022 Business Activity.** Not Customer (Option B); not both as parallel BAs (Option C). Rationale, per the Repository Owner's own instruction: Commercial Account carries marginally greater downstream dependency leverage — it is the construct both C-020 (Subscription Anchor) and C-024 (bill-to hierarchy) most directly reference — and establishing it alone, rather than in parallel with Customer, avoids inventing a combined-scope BA broader than either construct strictly requires.

---

## E. D2 — Scope Model

`PE-001-C022 §1.9`/`§2.10` record the tenant-container reference as **Pending Canonical Binding** — *"where detailed semantics are unavailable in the supplied baseline."* This decision resolves that binding for BA-01 specifically, on C-022's own evidentiary basis, **not by inference from `ROD-C021` D8**.

`[RO DECISION — D2]` **Option A: Platform-global.** No `organization_id`/tenant anchor on the Commercial Account model for BA-01; no tenant overlay; no segment-scoping. Rationale, per the Repository Owner's own recorded instruction:
- Commercial Account is a distinct canonical commercial-container authority (`COM-001-033`), not itself a tenant construct.
- `§1.9`/`§2.10` explicitly record C-004 Organization as *"not a dependency of substance"* and forbid using it as the Customer/Account representation — introducing `organization_id`/tenant isolation now would construct architecture `PE-001-C022` has not itself established.
- C-022 has no hard dependency on C-040 Tenant Administration; that dependency remains Pending Canonical Binding.
- Platform-global is therefore the minimum non-invented scope available for BA-01.
- **This is not a permanent foreclosure of a future tenant relationship.** Any future move to tenant-scoped Commercial Accounts requires its own explicit, separate Repository Owner decision — this decision governs BA-01 only.

---

## F. D3 — Service Hosting

`[RO DECISION — D3]` **Option A: `AuthService`.** Rationale: reuse of existing architecture and the unbroken precedent of every commercial-adjacent Work Package to date (C-021/WP-20, C-023/WP-17) hosting in `AuthService`, per the Repository Owner's own stated criterion — *"use existing architecture where appropriate; do not create a new service merely for conceptual purity."* No demonstrated need for a dedicated service exists at BA-01's own minimum scope.

---

## G. D4 — Identity/Person References

`[FACT]` `PE-001-C022 §1.9`/`§2.10` record both the Identity (C-001/URA-001) and Person (C-006) references as optional and conditional — *"consumed only where an individual Customer's identity is also [a principal/a known Person] — Pending Canonical Binding where unavailable."*

`[RO DECISION — D4]` **Option A: defer optional Identity/Person references entirely; establish the minimum Account authority only.** Consistent with D1 (Account-first, not Customer-first) — Identity/Person references attach to Customer identity (`COM-001-032`), not to Commercial Account (`COM-001-033`), so this decision is a natural consequence of D1, not an independent scope reduction.

---

## H. Approved BA-01 Governance Definition (D5 — BA Boundary)

**Authorized, and only:** **"Establish Commercial Account."**

**In scope:**
- Establish one Authoritative Commercial Account.
- A system-assigned, stable Account Reference.
- Minimum canonical Account identity, classification, and status (`COM-001-033`).
- Platform-global scope (§E), `AuthService` hosting (§F), the existing `require_platform_admin`-shaped authorization pattern.

**Explicitly out of scope for BA-01** (consolidated from the Repository Owner's own instruction):
- Customer creation of any kind.
- Customer–Account Relationship establishment (`COM-001-034` requires an existing Customer Anchor *and* an existing Commercial Account Anchor — structurally not a first-slice concern; deferred).
- Reclassification, retirement, or reactivation of a Commercial Account.
- Merge, split, or transfer (`ERB-C022-04`, structural/multi-party transitions).
- Any Subscription (C-020), Billing (C-024), Contract (C-025), or Entitlement (C-023) functionality.
- Any CRM/sales-pipeline/case-management/ERP-Customer-Master functionality — each already recorded in `PE-001-C022 §1.5` as Pending Canonical Binding, no canonical owning capability identified.
- Any Organization (C-004) equivalence or reference of any kind (`COM-001-033`; `§1.9`).
- Tenant isolation of any kind (§E).
- Identity (C-001/URA-001) or Person (C-006) reference wiring (§G).
- Any lifecycle policy (merge/split approval, hierarchy governance, reclassification approval) beyond what `PE-001-C022`/`COM-001 §7` already canonically define — none may be invented locally (`PE-001-C022 §1.5` closing bullets).

**This scope SHALL NOT be expanded except by an explicit, separately-recorded Repository Owner decision.**

---

## I. Dependencies (BA-01, as scoped)

| Authority | BA-01 Dependency | Disposition |
|---|---|---|
| `CAP-001` | Capability identity and Business Intent. | Satisfied. |
| `COM-001` §7 | Customer/Commercial Account canonical model. | Satisfied — `COM-001-033` fully specifies the Account construct BA-01 establishes. |
| `C-002`/`URA-001` | Access Evaluation Outcome for the establish operation. | Satisfied — reusable `require_platform_admin` pattern. |
| `C-004` Organization | **Not consumed, not referenced, not equivalent** (§E, `COM-001-033`). | N/A by explicit decision. |
| `C-001`/`URA-001` Identity, `C-006` Person | Deferred (§G). | Pending Canonical Binding, not exercised by BA-01. |
| `C-040` Tenant Administration | Deferred (§E). | Pending Canonical Binding, not exercised by BA-01. |
| `C-020`/`C-023`/`C-024`/`C-025` | Downstream consumers of the Account Reference BA-01 produces. | Not a BA-01 dependency in either direction — BA-01 does not require any of them to exist. |

---

## J. Authority Model

Every BA-01 operation is gated by the existing `require_platform_admin` dependency, per the platform-global scope decision (§E) and mirroring the `C-003` Roles / `C-021` precedent — no new authorization mechanism, no `AuthorizationContext`, no Runtime Engine dependency. This is a `[FUTURE TDS QUESTION]` to confirm at `TDS-C022` time, not re-litigated here.

---

## K. What This Decision Does NOT Authorize

Recording D1–D6 **does not authorize**:
- `IRA-C022` acceptance (only its *preparation* is authorized, §L);
- `TDS-C022` creation;
- a WP registration or BA-01 charter;
- Implementation Authorization of any kind;
- any schema / migration / ORM model / repository / service / router / test;
- any frontend implementation;
- CBOR registration or a CBOR ADR;
- any edit to `COM-001`, `PE-001`, `PE-001-C022`, `CAP-001`, or any other LOCKED/Active constitutional document;
- reopening C-020's own unresolved decisions;
- any edit to C-021, `WP-20`, or their governance artifacts;
- reconciling the outstanding `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md` changes;
- a commit;
- a push.

It authorizes exactly: **C-022 capability-boundary + minimum-BA-01 governance definition (D1–D5), and authorization to prepare `IRA-C022` (D6).**

---

## L. Next Governance Sequence (D6)

`[RO DECISION — D6]` This ROD → **`IRA-C022` preparation is authorized as the next step**, scoped to the "Establish Commercial Account" BA-01 boundary recorded in §H. `IRA-C022` preparation does not itself constitute IRA acceptance — that remains a separate, future Repository Owner act, per every prior capability's own governance sequence (`ROD-C021 §T`, `ROD-C132`). **`TDS-C022`, WP registration, a BA-01 charter, and implementation are explicitly NOT authorized by this decision** and each require their own separate, explicit Repository Owner authorization in turn.

---

*End of ROD-C022 (capability-boundary and minimum-BA-01 scope decided: D1 Establish Commercial Account; D2 platform-global; D3 `AuthService`; D4 Identity/Person deferred; D5 BA-01 boundary as recorded in §H; D6 `IRA-C022` preparation authorized, no further step authorized). Nothing implemented. Nothing staged, committed, or pushed.*
