# IRA-C040 — Tenant Administration: Business-Function & Implementation Readiness Assessment

**Capability:** C-040 — Tenant Administration
**Domain:** D-003 — Enterprise Administration
**Status:** ~~Analysis / Readiness Exercise Only — no WP, BA, or implementation authorized by this document~~ *(historical, drafting-time statement for Part I, preserved per this repository's own no-silent-fix discipline — accurate on 2026-08-25, before Parts II/III existed and before formal acceptance.)* **ACCEPTED, 2026-08-26 — see Part III §20/§28 (result: GREEN — Implementation Ready) and `WP-16_C040_BA-01_Tenant_Establishment_Business_Activity_Charter.md §20`.** Acceptance is a governance act recognizing this assessment's own conclusion; it does not retroactively alter Part I's RED finding or Part II's AMBER finding, both preserved verbatim below as the historical record.
**Prepared:** 2026-08-25 (Part I); amended 2026-08-26 (Part II); amended 2026-08-26 (Part III); accepted 2026-08-26, WP-16 chartered
**Classification:** Implementation Readiness Assessment — **Accepted** (Parts I–III; governs WP-16 BA-01, Tenant Establishment)

**Filename note:** This document is named `IRA-C040_...`, not `IRA-001_C-040_...` as literally requested, because `IRA-001` already exists (`IRA-001_WP-01_Organization_Management_Implementation_Readiness_Assessment.md`, C-004). Reusing that identifier for an unrelated capability would collide with an existing governance artifact and would misleadingly suggest WP-01 ownership, exactly the failure mode this repository's own capability-first IRA-naming precedent (`IRA-C066`, `IRA-C114`) was established to prevent. No WP number exists for C-040 (confirmed below), so no `IRA-0NN` number is legitimately available either. This is a disclosed deviation from the literal instruction, not a silent one.

---

## 1. Executive Summary

C-040's Enterprise Experience is, on the documentary evidence, the most mature and internally rigorous specification examined for any not-yet-implemented capability in this repository to date — a Gold Standard Conformance Baseline with 8 ERBs, 17 EXs, 10 Experience Contracts, 15 Business Rules, 17 Invariants, 36 internal validation passes (all PASS), and a disciplined three-revision self-correction history (v1.0→1.1→1.2) that already removed its own unsupported assumptions rather than carrying them forward. This is a genuinely different starting position from either prior precedent examined this session: **C-066** had a thin business function but one populated, governed table to build against; **C-114** had a rich implementation surface but an undefined business function. **C-040 has neither problem** — the business function is unambiguous and the architecture (SD-002 §13) is sufficient and consistent — **and still cannot proceed**, because the one thing every candidate Business Activity's execution path depends on — a canonical Tenant object with identity-allocation authority — does not exist anywhere in this repository, canonical or implemented, and its own governing specification (`PE-001-C040` §5.4) states explicitly that no Tenant Administrative standing exists to observe until a provisioning Commit produces the first one.

**Overall Classification: 🔴 RED — Not Implementation Ready.** Confidence: **High**. This is not a borderline call — it is corroborated identically across four independent analysis passes this session (a capability-readiness pre-screen, a Primary-Specification/Tenant-binding decision analysis, a fresh-context independent verification, and this full-document readiness assessment) and by the specification's own self-declared "Pending Canonical Binding" markers at 15+ points in its own text.

---

## 2. Authoritative Baseline

Per the Repository Owner Decision recorded 2026-08-25 (`CAP-001` v1.6, "C-040 Repository Owner Confirmation" changelog entry) and this session's own prior analysis chain:

1. **C-040 Primary Specification = SD-002.** Already the assigned value since WP-2; independently reaffirmed. Treated as canonical architectural authority for C-040 throughout this assessment.
2. **`tenant_registry` remains DEFERRED** (`SER-001` SE-052, reaffirmed 2026-08-25). Not adopted as C-040's canonical Tenant binding. Not promoted, invented, or inferred as canonical anywhere in this document.
3. The prior task changed only `CAP-001_Enterprise_Capability_Registry.md` and `SER-001_Strategic_Enhancement_Register.md`. No implementation was authorized.
4. This assessment adds no new Repository Owner decision, no ADR, no WP, no BA, no migration, no code. `PE-001-C040.docx` is read-only for this task and was not modified.

---

## 3. C-040 Business Function Definition

**3.1 Business purpose.** C-040 solves the problem of administering a Tenant — the platform's administratively-governed infrastructure and data-isolation partition for an already-existing Organization — as a distinct concern from Organization business identity (C-004), enterprise structure (C-005), or configuration values (C-041). No other capability owns provisioning, isolation/resource-allocation confirmation, administrator designation, migration, offboarding, or cross-tenant-sharing governance for that partition (`PE-001-C040` §1.1).

**3.2 One-paragraph business-function definition.** C-040 is the Enterprise Experience through which the enterprise establishes, understands, deliberately changes, and continuously makes referenceable the administrative standing of a Tenant — the infrastructure/data-isolation partition underlying an already-valid Organization — covering provisioning, administrator designation, migration, offboarding, and governed cross-tenant sharing exceptions, while never originating Organization, Membership, Access, Workspace, Subscription, Customer/Account, Entitlement, Billing, Contract, Configuration, or Preference facts, and while explicitly declining to invent canonical Tenant identity, identifier-allocation authority, or Tenant–Organization cardinality where the supplied constitutional baseline does not establish them (`PE-001-C040` §1.2–§1.8, Business Rules BR-C040-01/03/10/15).

**3.3 Ownership boundary.**

| C-040 owns | C-040 does NOT own |
|---|---|
| Tenant provisioning, isolation/resource-allocation *confirmation* (not enforcement), administrator designation, migration, offboarding, cross-tenant sharing agreement governance, as Enterprise Experience (`PE-001-C040` Pre-Engineering Authority Pass, Table 1) | Organization business identity/existence/validity (C-004); Enterprise Structure (C-005); Identity/Auth (C-001/URA-001); Person (C-006); Membership (C-007); Access/Role/Permission (C-002/C-003/URA-001); Workspace resolution (PE-001-C008); Subscription (C-020); Customer/Account (C-022); Entitlement/License (C-023); Billing (C-024); Contract (C-025); Configuration (C-041); Preference (C-042); the physical/logical isolation *enforcement* mechanism itself (RTA-001/infrastructure); canonical Tenant identity/identifier-allocation authority; Tenant–Organization cardinality (BR-C040-01/03/10/15, §1.5 Out of Scope, exhaustive) |

- **Upstream capability:** C-004 (Organization existence/validity and the Organization activation trigger) — C-040 cannot begin provisioning without an already-valid Organization Anchor consumed exclusively from C-004 (§1.7 "Organization before Tenant").
- **Downstream capabilities:** C-020/C-022/C-023/C-024/C-025 (referenced only, advisory, for migration/offboarding impact assessment); every capability requiring Tenant effective standing consumes it exclusively through EX-C040-15 (Contract 5.3).
- **Shared platform services:** C-002 (Access Evaluation Outcome, consumed not granted); PE-001-C008 (Workspace anchor, contextual only).
- **External dependencies:** none identified; the physical isolation enforcement mechanism is out of scope by design (RTA-001/infrastructure).

**3.4 Candidate Business Activities.** **No canonical Business Activity or EAC identifier exists for C-040 anywhere in the supplied baseline** (`PE-001-C040` §1.15, explicit; confirmed independently — `WPR-001`/`WP-REG-001` grep to zero C-040 hits). Every item below is a **Candidate BA requiring future approval**, derived from the 8 ERBs without inventing scope. No official BA ID is assigned.

| Candidate BA (proposed name) | Business outcome | Actor | Trigger | Preconditions | Primary flow (ERB) | Dependencies | In C-040's boundary? |
|---|---|---|---|---|---|---|---|
| Anchor Tenant Administrative Context | Tenant Administrative Anchor Context established | Tenant Administration Steward / Observer | Enterprise/journey objective requires knowing which Organization's Tenant is relevant, or a C-004 activation trigger arrives | Resolvable candidate Organization Anchor | ERB-C040-01 | C-004 (Organization validity, trigger) | Yes |
| Understand Tenant Administrative Standing | Current standing understood | Standing Observer | Anchor exists | Tenant Administrative Anchor Context resolved | ERB-C040-02 | ERB-C040-01's output; **an Authoritative Tenant Context to observe, which does not exist before first Commit (Contract 5.4)** | Yes, but blocked — see §6 |
| Frame Tenant Administrative Intent (provisioning / redesignation / migration / offboarding / sharing agreement) | Change Intent Context established | Tenant Administration Steward | Business reason for one of five target actions arises | Anchor resolved | ERB-C040-03 | Same as above | Yes |
| Shape and Assess Proposed Tenant Administrative Change | Proposed change + advisory impact assessment | Steward + Decision Participant | Confirmed intent | Intent framed | ERB-C040-04 | C-020/C-022/C-023/C-024/C-025 references (advisory) | Yes |
| Commit Tenant Administrative Transition | Resulting Tenant Administrative Context produced | Steward (with governed authority, Pending Canonical Binding — BR-C040-13) | Assessed proposal ready | Shaped + assessed proposal | ERB-C040-05 | **Canonical Tenant identity/allocation authority — Pending Canonical Binding (BR-C040-15)**; provisioning/migration/offboarding/sharing approval authority — **Pending Canonical Binding (BR-C040-13)** | Yes, but blocked — see §6 |
| Resolve Effective Tenant Administrative State | Effective state resolved (continuous, recomputed) | Any dependent capability | Dependent capability needs current standing | **An Authoritative Tenant Context must already exist** | ERB-C040-06 | Depends on Commit having occurred at least once | Yes, but blocked — see §6 |
| Distribute Tenant Reference Downstream | Tenant Reference available to consumers | Any dependent capability | Resulting context requires downstream availability | Same as above | ERB-C040-07 | Same as above | Yes, but blocked — see §6 |
| Resolve Tenant Administrative Context Disruption | Condition classified, owned, resolved/escalated | Any | Interruption, disruption, Access rejection, unresolved binding, or reference conflict | — | ERB-C040-08 | — | Yes |

No candidate BA absorbs any excluded capability's domain semantics — independently re-verified against Table 1 (Pre-Engineering Authority Pass), §1.5 (Out of Scope), and the Separation Validation table (§8.4, 21/21 PASS) below.

---

## 4. Capability Boundary

Restated concisely from §3.3 and `PE-001-C040` §1.8: C-040's responsibility begins when an enterprise objective requires establishing, understanding, or changing a Tenant's administrative standing, and ends when a Resulting Tenant Administrative Context is produced and available for reference, or the experience exits without a completed transition. C-040 **never originates** Organization, Enterprise Structure, Person, Membership, Access, Workspace, Subscription, Customer/Account, Entitlement/License, Billing, Contract, Configuration, or Preference facts (BR-C040-01/10), and **never locally establishes canonical Tenant identity or identifier-allocation authority** (BR-C040-15) — this last exclusion is the specification's own explicit acknowledgment of the exact gap this assessment finds blocking.

---

## 5. Canonical Architecture Authority

**CANONICAL:** `CAP-001` assigns C-040 to **SD-002**, reaffirmed by explicit Repository Owner Decision, 2026-08-25 (`CAP-001` v1.6). This governs the assessment.

**DOCUMENTATION DRIFT (not re-litigated here — see §14):** `PE-001-C040`'s own masthead, CRB identity table (§2.1), Canonical Experience Identity table (§9.3), and Gold Standard self-validation Q4 (§8.5) all still assert `SD-001` as Primary Specification, unsynchronized with the Repository Owner's reaffirmation. This assessment treats **SD-002 as authoritative per the Repository Owner's own instruction**, independently of what the document's own masthead currently says.

---

## 6. SD-002 Conformance Analysis

**Which SD-002 requirements apply:** Section 2 (Universal Business Object Model, SD-002-004 through -020) applies to any future canonical Tenant object; Section 13 (Multi-Tenancy & Data Isolation, SD-002-108 through -112) applies directly and substantively to C-040's own experience content; Section 7 (Event/Audit, SD-002-051–054) and Section 8 (Governance, SD-002-055–058) apply to any future Commit implementation.

**Direct governance mapping (verified, no gaps found):**

| SD-002 principle | C-040 realization |
|---|---|
| SD-002-108 (explicit tenant boundary, non-optional identifier) | BR-C040-03, Contract 5.4 — Tenant Administrative Anchor keyed to its own anchor; no ambiguous boundary permitted |
| SD-002-109 (isolation by construction, not just access control) | Out of Scope §1.5 — C-040 engineers the *confirmation* experience; enforcement mechanics correctly deferred to RTA-001/infrastructure, not silently absorbed nor silently ignored |
| SD-002-110 (shared infrastructure ≠ shared performance risk) | Referenced in Authoritative Tenant Context's isolation/resource-allocation posture concern (§1.16); no contradiction found |
| SD-002-111 (only Global/Industry CIL shared; cross-tenant sharing requires explicit audited agreement) | BR-C040-07, INV-C040-12, ERB-C040-03/05 (EX-C040-08/14) — cross-tenant sharing engineered as its own explicit, additive, audited target action, never default |
| SD-002-112 (migration/offboarding preserve full historical integrity) | BR-C040-06, INV-C040-11, ERB-C040-05 (EX-C040-12/13) — engineered as distinct Commit outcomes specifically because they carry this obligation and provisioning/redesignation do not |

**No conflicts found.** C-040's ERBs, Business Rules, and Invariants map cleanly onto SD-002 §13 with no contradiction, no gap requiring an additional architectural decision beyond what §7/§9 of this document already name as Pending Canonical Binding. **C-040 can be designed within SD-002 without additional architectural decisions to SD-002 itself** — the blocking gaps (§9, §13 below) are canonical-object-existence and governance-authority gaps, not SD-002 insufficiency.

**Classification of every material SD-001 reference encountered (per the four-category scheme the governing task specifies):**

| # | Location | Content | Classification |
|---|---|---|---|
| 1 | Masthead (§Document Control) | "Primary Specification Reference: SD-001" | **2 — Actual C-040 primary-specification drift** |
| 2 | §Normative Position | "SD-001 remains authoritative for applicable presentation/administrative-experience principles... SD-002 Section 13 remains authoritative for multi-tenancy and data-isolation semantics" | **1 — Valid SD-001 reference** (accurate dual-authority statement, independent of which is "Primary") |
| 3 | §Pre-Engineering Authority Pass | "SD-001 (this capability's own Primary Specification) uses 'tenant' exclusively as an adjective..." | **4 — Document-maintenance issue only** (the parenthetical label is drift; the substantive linguistic analysis is accurate and, if anything, supports SD-002 as structural owner) |
| 4 | §1.5 Out of Scope | "Presentation Architecture, screen, widget, layout or navigation-menu design — SD-001 (referenced only where PE-001 requires)" | **1 — Valid** |
| 5 | §1.9 Dependencies table | "SD-001 \| Applicable administrative-experience principles, translated into experience architecture" | **1 — Valid** |
| 6 | §7.7 Discoverability Rules | "...consistent with the applicable SD-001 resolution-sequence principle..." | **1 — Valid** |
| 7 | §7.8 Explainability Rules | "...consistent with the applicable SD-001 explainability... principles" | **1 — Valid** |
| 8 | §7.13 Cross-Specification References table | "SD-001 \| Applicable administrative-experience principles... \| Translated into experience architecture; not reproduced as screen design" | **1 — Valid** |
| 9 | Revision History (v1.0 row) | "...established Tenant's canonical meaning from SD-001, SD-002 Section 13, CMD-001, and CLAUDE.md..." | **1 — Valid** (accurate historical record of sources consulted) |
| 10 | §2.1 CRB Identity table | "Primary Specification \| SD-001" | **2 — Drift** (masthead-mirror field) |
| 11 | §8.5 Internal Validation Passes, Q2 | "...Primary Specification SD-001 (Chapter 2.1, 9.3)" | **2 — Drift** (describes where the drifted value appears) |
| 12 | §8.5 Internal Validation Passes, Q4 | "Is the Primary Specification (SD-001) accurately represented, without inventing semantics SD-001 does not define?" + PASS disposition | **3 — Ambiguous, requires review** (this is a self-validation *check*, not a passive citation — correcting Primary Spec to SD-002 requires re-executing this check's own logic against the new value, not a text substitution) |
| 13 | §9.3 Canonical Experience Identity table | "Primary Specification \| SD-001" | **2 — Drift** (masthead-mirror field, Gold Standard chapter) |
| 14 | §9.6 Experience Decision Record | "SD-001-102 is the only canonical evidence of a 'tenant administrator' responsibility..." | **1 — Valid** (substantive, accurate finding, independent of labeling) |
| 15 | §9.6 Experience Decision Record, row 1 | "...triangulates Tenant's canonical meaning from CLAUDE.md §6, SD-002 Section 13, CMD-001 §12.6, and SD-001" | **1 — Valid** (methodological accuracy) |

**Tally: 9 valid, 4 drift, 1 document-maintenance-only, 1 ambiguous/requires-review.** The substantive architecture is sound; the drift is concentrated in four self-referential "Primary Specification" label fields plus one self-validation check that needs re-execution — see §14 for the full Document Synchronization Debt Register.

---

## 7. Tenant / Organization Analysis

Per the Repository Owner's explicit reaffirmation, `tenant_registry` = **DEFERRED**, not canonical. This section does not use it as such.

- **What currently defines Tenant?** Nothing canonically implemented. `PE-001-C040`'s own Pre-Engineering Authority Pass triangulates a *conceptual* definition from three non-implementing sources (CLAUDE.md §6, SD-002 §13, CMD-001's scope hierarchy) but explicitly states this triangulation does **not** resolve canonical identity or identifier-allocation authority (BR-C040-15). No CBOR (Canonical Business Object Register) entry exists for Tenant (independently verified this session — `CBOR-INDEX.md`'s 8 entries do not include one). No Backend model, repository, API, or migration exists anywhere (independently verified this session against both services' full Alembic chains).
- **Tenant ↔ Organization relationship:** **PENDING CANONICAL BINDING**, explicitly and repeatedly self-declared by the specification itself (§1.5, §1.7 "Organization before Tenant" as a *sequencing* principle only — not a cardinality statement, BR-C040-03, Contract 5.4, INV-C040-07, §9.6 Decision Record). The specification's own v1.1 corrective pass *removed* an earlier unsupported "exactly one Organization Anchor" assumption specifically because no canonical source resolves it — this is documented self-correction, not an oversight this assessment is newly discovering.
- **Does C-040 require Tenant context?** Yes — every ERB operates on Tenant Administrative context by definition. This is not itself a blocker; the blocker is that no canonical Tenant *object* exists for that context to attach to.
- **Is cardinality canonically decided?** **No — PENDING CANONICAL BINDING.** `organization_master.tenant_id` (nullable FK, `Master_Technical_Architecture.md` AMD-002) is schema-level *design intention* only — not implemented in the real, migrated `AuthService.Organization` model, and points at the deferred, non-canonical `tenant_registry`. Per this session's own prior independent verification, this schema comment does not itself constitute a ratified constitutional statement.
- **Unresolved tenant-binding questions, exhaustively, per the specification's own self-declaration:** (1) canonical Tenant identity/identifier-allocation authority (BR-C040-15, INV-C040-17); (2) Tenant–Organization cardinality (BR-C040-03, INV-C040-07); (3) provisioning approval authority; (4) migration approval authority; (5) offboarding approval authority; (6) cross-tenant sharing approval authority (all four: BR-C040-13). **All six: PENDING CANONICAL BINDING.**

---

## 8. Domain & Data Model

| Construct | Status | Basis |
|---|---|---|
| Tenant Administrative Anchor Context | **PROPOSED** (specification-defined, non-authoritative by design) | `PE-001-C040` §1.16, Table 6 |
| Organization Activation Trigger Reference Context | **PROPOSED** | Same |
| Authoritative Tenant Context | **PROPOSED / UNRESOLVED** — the specification's own central object, but it cannot exist until a first Commit, which cannot occur without canonical identity-allocation authority | §1.16–1.18, §5.4, §9.7 |
| Tenant Administrative Change Intent / Proposed / Impact Assessment Context | **PROPOSED** | §1.16 |
| Resulting Tenant Administrative Context | **PROPOSED / UNRESOLVED** (same dependency chain as Authoritative Tenant Context) | §1.16–1.18 |
| Effective Tenant Administrative State Context | **PROPOSED**, never persisted by design (SD-002-008/009-conformant: computed projection, not stored state) | §5.3, §9.7 |
| Tenant Reference Distribution Context | **PROPOSED** | §1.16 |
| Tenant Administrative Continuity Recovery Context | **PROPOSED**, exception-scoped only | §1.16 |
| `tenant_registry` (AMD-002) | **DERIVED / DEFERRED** — a candidate infrastructure schema, explicitly not canonical (Repository Owner Decision, 2026-08-25) | `Master_Technical_Architecture.md`; `SER-001` SE-052 |
| Canonical Tenant identity / identifier-allocation authority | **UNRESOLVED — PENDING CANONICAL BINDING** | BR-C040-15, INV-C040-17 |
| Tenant–Organization cardinality | **UNRESOLVED — PENDING CANONICAL BINDING** | BR-C040-03, INV-C040-07 |
| Authoritative system of record | **NONE EXISTS** | No canonical Business Object registration, no Backend implementation |
| Cross-capability references | Consumed-only from C-004 (Organization), conditionally from C-001/C-006/C-007 (administrator identity), advisory-only from C-020/C-022/C-023/C-024/C-025 | §1.9, §2.10, §5.9 (all fully specified, no gap) |
| Evidence/audit requirements | Governed by SD-002 §7 generally once a real object exists; no C-040-specific gap beyond the object's own nonexistence | SD-002-051–054 |
| Tenant/Organization scoping | Isolation is architecturally required (SD-002-108/109) but enforcement mechanics are correctly out of scope (RTA-001/infrastructure) | §1.5 |
| AI/data dependencies | Advisory-only (§5.7, BR-C040-12) — no gap | Chapter 5.7 |

No entity in this table is **CANONICAL**. This is the single most consequential finding of this section: C-040's *experience* architecture is exhaustively specified, but its *domain model* has zero canonical anchor.

---

## 9. Business Rules & Invariants

All 15 Business Rules (BR-C040-01 through -15) and all 17 Invariants (INV-C040-01 through -17) were read in full (`PE-001-C040` §7.2, §9.4). None were manufactured for this assessment — all are direct quotations/paraphrases of the specification's own text. Selected rules with direct implementation consequence:

| Rule | Source | Canonical status | Implementation consequence | Unresolved question |
|---|---|---|---|---|
| BR-C040-01/10 | §7.2 | **RATIFIED** (specification-internal) | No BA may absorb C-004/C-005/C-006/C-007/C-002/C-008/C-020/C-022/C-023/C-024/C-025/C-041/C-042 semantics | None |
| BR-C040-03 / INV-C040-07 | §7.2, §9.4 | **RATIFIED**, but content is itself "no cardinality assumed" | An implementer literally cannot write a Tenant↔Organization FK/relationship without first resolving cardinality | **PENDING CANONICAL BINDING** |
| BR-C040-05 | §7.2 (v1.1-corrected) | **RATIFIED** | Offboarded Tenant never reprovisioned to same anchor; C-040 has no authority over new Organization establishment | None (already corrected once, no residual gap) |
| BR-C040-07 / INV-C040-12 | §7.2, §9.4 | **RATIFIED** | Cross-tenant sharing requires an explicit, named, audited record — **no such mechanism exists anywhere in this repository** (`TECH-DEBT.md` TD-040) | Open, but non-blocking per TD-040's own Low severity — no sharing agreement currently exists to consult |
| BR-C040-09 | §7.2 | **RATIFIED** | Administrator designation never itself an Access/Role/Permission grant — governed by C-002/C-003/URA-001 | None |
| BR-C040-13 | §7.2 | **RATIFIED**, content is itself "no authority invented" | No implementer may invent who may approve provisioning/migration/offboarding/sharing | **PENDING CANONICAL BINDING** (four separate authorities) |
| BR-C040-15 / INV-C040-17 | §7.2, §9.4 (v1.1-added) | **RATIFIED**, content is itself "canonical identity not established" | Commit (ERB-C040-05) — the precondition for every other ERB's Business Activity — cannot be implemented without this authority existing | **PENDING CANONICAL BINDING** |

No business rule was manufactured to complete this analysis; where the specification itself declares a rule's content to be "Pending Canonical Binding," that status is preserved here, not resolved.

---

## 10. Candidate / Existing Business Activities

Restated from §3.4, with explicit A–E readiness classification per `IMP-001 §6.2b` (the canonical scale, formalized ADR-014/METH-001):

| Candidate BA | A–E Category | Rationale |
|---|---|---|
| Anchor Tenant Administrative Context (ERB-C040-01) | **D** | No constitutional blocker in the *anchor-resolution* logic itself, but the anchor's own completion condition ("does an Authoritative Tenant already exist") cannot be answered without a canonical Tenant object |
| Understand Tenant Administrative Standing (ERB-C040-02) | **D** | Nothing exists to "understand" before a first Commit (Contract 5.4) |
| Frame Tenant Administrative Intent (ERB-C040-03) | **D** | Framing intent is possible in isolation, but every one of the five target actions terminates at a Commit gated on BR-C040-15/-13 |
| Shape and Assess Proposed Change (ERB-C040-04) | **D** | Same dependency chain |
| Commit Tenant Administrative Transition (ERB-C040-05) | **D** | Directly blocked — requires canonical Tenant identity/allocation authority (BR-C040-15) and named approval authorities (BR-C040-13), neither established |
| Resolve Effective Tenant Administrative State (ERB-C040-06) | **D** | Requires an Authoritative Tenant Context to already exist |
| Distribute Tenant Reference Downstream (ERB-C040-07) | **D** | Same |
| Resolve Tenant Administrative Context Disruption (ERB-C040-08) | **D** | The recovery/exception logic itself is well-specified and largely self-contained (Chapter 6), but is only exercised once the other seven ERBs have something to recover from |

**All eight candidate BAs classify as Category D — Governance clarification required**, none reaches C (ordinary implementation-level design work remaining, no constitutional blocker) because every execution path terminates at the same unresolved constitutional gap (BR-C040-15/BR-C040-03/BR-C040-13), not at independent, per-BA implementation questions. This is a stronger, more precisely-evidenced version of the original capability-readiness pre-screen's own finding, now traced to the specification's own explicit rule numbers rather than inferred.

---

## 11. CBAIP Lifecycle Readiness

Applying `IMP-001 §6.3–6.7`'s mandatory lifecycle/component/contract structure to the Commit Business Activity (ERB-C040-05/EX-C040-11–14), as the representative case every other candidate BA ultimately depends on:

| CBAIP dimension | Status | Basis |
|---|---|---|
| Intent | **Defined** | §1.16 Tenant Administrative Change Intent Context, fully specified |
| Preconditions | **Partially Defined** | Anchor + assessed proposal defined; canonical Organization validity defined (consumed from C-004); canonical Tenant identity precondition **Undefined** |
| Trigger | **Defined** | §4 EX-C040-04 through -08 (five distinct target-action triggers) |
| Authorization | **Undefined** | BR-C040-13 — provisioning/migration/offboarding/sharing approval authority all Pending Canonical Binding; C-002 Access Evaluation Outcome consumption is defined, but *who* is authorized to hold that outcome for these specific actions is not |
| Validation | **Partially Defined** | Business-rule-level validation (BR-C040-01 through -15) fully specified; persistence-level validation cannot be designed without a schema |
| Execution | **Undefined** | No canonical Tenant object to execute against |
| State transition | **Defined** (conceptually) | §5.5 Tenant Lifecycle Contract fully specifies PROVISIONED/MIGRATING/OFFBOARDED semantics — but this is a *state machine specification*, not an implementable state, absent a canonical object to carry it |
| Persistence | **Undefined** | No canonical object, no CBOR registration, no migration |
| Events | **Partially Defined** | SD-002-009/052 mandates event-per-transition generically; C-040-specific event names are not enumerated anywhere in the specification (a genuine, disclosed absence — Enterprise Transitions in §6.1 name the *transition*, not an event payload/type) |
| Audit | **Partially Defined** | SD-002-054's seven-question standard applies generically; no C-040-specific audit design exists yet, appropriately deferred pending persistence design |
| Notifications | **Not Applicable** | Not named anywhere in the specification as a C-040 concern (workflow/notification mechanics belong to SD-003 per SD-002-037) |
| Postconditions | **Defined** | §1.17–1.18, §9.7 — exceptionally precisely specified, including the v1.2 per-concern authority-promotion clarification |
| Failure handling | **Defined** | Chapter 6, ERB-C040-08, six exception classifications, all specified |
| Idempotency | **Undefined** | `IMP-001 §6.7` requires every BAC to disclose guarded-vs-idempotent transition behavior; `PE-001-C040` does not address this at the implementation-mechanics level (correctly out of scope for a PE-001 Enterprise Experience document, but it means this dimension remains open for the eventual BAC, not resolved by anything examined here) |
| Observability | **Partially Defined** | §7.9 Experience KPIs (9 KPIs, fully named and defined) — strong basis once implementation exists |

**Overall: Partially Defined, tending toward Undefined for every dimension that depends on a persisted object existing.** The *experience*-layer dimensions (Intent, Trigger, Postconditions, Failure handling, Observability-definition) are exceptionally well defined. The *implementation*-layer dimensions (Authorization, Execution, Persistence, Events, Idempotency) cannot be defined without first resolving the canonical-object and authority gaps in §7/§9.

---

## 12. Dependencies

| Dependency | Type | Current Status | Canonical Source | Blocking? | Required Decision |
|---|---|---|---|---|---|
| C-004 Organization validity & activation trigger | Capability | **RATIFIED**, implemented, migrated | `AuthService.Organization`; ADR-003 | No | None — fully available |
| Canonical Tenant identity/identifier-allocation authority | Architectural | **PENDING CANONICAL BINDING** | None exists | **Yes — primary blocker** | Repository Owner / architecture decision: what allocates Tenant identity, and does `tenant_registry` (or another mechanism) ever become that authority |
| Tenant–Organization cardinality | Architectural | **PENDING CANONICAL BINDING** | None exists | **Yes** | Repository Owner decision (deliberately not resolved by this assessment, consistent with the Repository Owner's own 2026-08-25 instruction not to infer it from `organization_master.tenant_id`) |
| Provisioning approval authority | Governance | **PENDING CANONICAL BINDING** | None exists | **Yes** | Repository Owner decision naming an authority |
| Migration approval authority | Governance | **PENDING CANONICAL BINDING** | None exists | **Yes** | Same |
| Offboarding approval authority | Governance | **PENDING CANONICAL BINDING** | None exists | **Yes** | Same |
| Cross-tenant sharing approval authority | Governance | **PENDING CANONICAL BINDING**; mechanism itself absent platform-wide | None exists; `TECH-DEBT.md` TD-040 | Not currently (Low severity, no agreement exists to need one yet) | Future, separate capability/BA charter per TD-040's own Target Resolution |
| `tenant_registry` build authorization | Data | **DEFERRED** (Repository Owner Decision, 2026-08-25) | `SER-001` SE-052 | Not directly — deferred by design, not omitted | None pending; current instruction is explicit non-adoption |
| C-002 Access Evaluation Outcome | Identity/Authorization | **RATIFIED**, available | URA-001, implemented | No | None |
| `TenantService` scaffold reconciliation | Implementation substrate | **DEFERRED** | ADR-003 | Not directly (C-040 does not depend on `TenantService`) | Future, separately-scoped ADR per ADR-003's own §3 |
| Missing ARP-001 WP-2 implementation report | Governance evidence | **UNKNOWN / not discoverable** | Cited by `CAP-001`'s own WP-2 changelog | No (does not block C-040 specifically; a general repository evidentiary gap, independently reconfirmed this session) | None required for C-040 directly |
| PE-001-C040 document synchronization | Documentation | **DOCUMENTATION DRIFT** | See §6, §14 | Not for the *architecture* (SD-002 content is sound); yes for **publication-readiness re-certification** if the document is ever re-issued | Future, separately-scoped remediation pass |
| Event/audit type naming for C-040 transitions | Implementation | **UNDEFINED** | None yet | Would block Gate 7 (implementation) once other blockers clear | Ordinary implementation-level design (Category C), not a governance gap |

---

## 13. Governance & Decision Gaps

Consolidating §7, §9, §12: **four live, unresolved Repository-Owner-or-architecture-level gaps**, all self-declared by `PE-001-C040`'s own text (not discovered by inference):

1. Canonical Tenant identity/identifier-allocation authority (BR-C040-15/INV-C040-17).
2. Tenant–Organization cardinality (BR-C040-03/INV-C040-07).
3. Provisioning / migration / offboarding / cross-tenant-sharing approval authority (BR-C040-13) — four related but distinct authorities.
4. `PE-001-C040`'s own internal Primary Specification synchronization (masthead, §2.1, §9.3, §8.5 Q4) — a document-maintenance gap, not an architecture gap, since CAP-001/Repository Owner have already resolved the substantive question (§5, §6).

None of these is newly discovered by this assessment; all four are already self-labeled "Pending Canonical Binding" within the specification's own text, which this assessment treats as authoritative self-disclosure rather than a defect the specification's authors overlooked.

---

## 14. PE-001-C040 Document Synchronization Debt Register

Per §6's classification table (15 locations examined):

| Category | Count | Locations | Required treatment |
|---|---|---|---|
| 1 — Valid SD-001 reference | 9 | Normative Position; §1.5 (presentation exclusion); §1.9 Dependencies; §7.7/§7.8 (resolution-sequence/explainability principles); §7.13 Cross-Spec table; Revision History v1.0; §9.6 (SD-001-102 finding; triangulation record) | None — no correction needed |
| 2 — Actual C-040 primary-specification drift | 4 | Masthead; §2.1 CRB Identity table; §8.5 Q2; §9.3 Canonical Experience Identity table | Mechanical label correction (SD-001 → SD-002) once a document-maintenance pass is separately authorized |
| 3 — Ambiguous, requires review | 1 | §8.5 Q4 (Gold Standard self-validation check asserting "Primary Specification (SD-001) accurately represented") | Requires **re-execution** of the underlying validation logic against SD-002, not a text substitution — may surface new findings |
| 4 — Document-maintenance issue only | 1 | Pre-Engineering Authority Pass parenthetical ("SD-001 (this capability's own Primary Specification)") | Delete/update the parenthetical label; underlying linguistic analysis is accurate and unaffected |

**Conclusion, stated explicitly per the governing task's own requirement: no mechanical SD-001 → SD-002 replacement should be performed without semantic review.** Nine of fifteen locations must NOT be changed at all (they are accurate regardless of Primary Specification labeling); a mechanical find-replace across the document would corrupt those nine while only correctly fixing four, and would leave the one self-validation check (§8.5 Q4) asserting a conclusion its own logic was never re-run to support. This finding reproduces and further evidences the same conclusion this session's prior C-040 Repository Owner Decision task already reached and recorded in `CAP-001`'s own new changelog entry.

---

## 15. Implementation Readiness Matrix

| # | Category | Status | Evidence | Blocker? | Required action |
|---|---|---|---|---|---|
| 1 | Business-function clarity | **DEFINED** | §1.1–1.2, exceptionally precise, single verbatim CAP-001 Business Intent | No | None |
| 2 | Capability boundary | **DEFINED** | §1.5, §1.8, §2.10, 21/21 Separation Validation PASS | No | None |
| 3 | Architecture authority | **RATIFIED** (CAP-001/Repository Owner) but **DOCUMENTATION DRIFT** (PE-001-C040 self-reference) | §5, §6, §14 | Non-blocking for architecture; blocking for publication-readiness re-certification only | Future document-sync pass |
| 4 | Requirements completeness | **DEFINED** | 8 ERBs, 17 EXs, 10 Contracts, all seven-dimension context-engineered | No | None |
| 5 | Business Activity completeness | **PROPOSED**, zero canonical | §1.15, §10 | Yes (no canonical BA exists at all) | Repository Owner: authorize BA charter once §13's gaps close |
| 6 | Domain/data model completeness | **UNRESOLVED** | §8 — no entity is CANONICAL | **Yes — primary blocker** | Repository Owner/architecture decision (§13.1–13.3) |
| 7 | Identity/authorization readiness | **PARTIALLY DEFINED** | C-002 consumption defined; approval authorities Pending Canonical Binding | Yes | §13.3 |
| 8 | Tenant-context readiness | **PENDING CANONICAL BINDING** | §7 | **Yes** | §13.1–13.2 |
| 9 | Business-rule completeness | **DEFINED** | §9, 15/15 rules read, none manufactured | No | None |
| 10 | Event/audit requirements | **PARTIALLY DEFINED** | §11 — generic SD-002 obligation defined; C-040-specific event taxonomy undefined | Yes (implementation-level, Category C once other gaps close) | Ordinary design work, not governance |
| 11 | API/interaction readiness | **UNDEFINED** | Explicitly Out of Scope by the specification itself (§1.5, "Any API, database, event payload...") — correct for a PE-001 document, but means zero API design exists yet | Not blocking readiness *assessment*; blocking implementation start | TDS authoring, after §13 gaps close |
| 12 | Error/failure semantics | **DEFINED** | Chapter 6, six exception classifications, all specified | No | None |
| 13 | Migration requirements | **UNDEFINED** | No schema exists to migrate | Yes (downstream of §13.1) | Architecture decision first |
| 14 | Integration dependencies | **DEFINED** | §12 — fully enumerated, all either available (C-004/C-002) or explicitly advisory-only | No | None |
| 15 | Governance approvals | **PENDING CANONICAL BINDING** | §13 | **Yes** | Repository Owner decisions |
| 16 | Testability | **NOT ASSESSABLE YET** | No implementable object exists | Downstream | N/A until §13 resolved |
| 17 | Observability | **PARTIALLY DEFINED** | §7.9, 9 KPIs named | No (strong basis, not yet wired) | Implementation-level |
| 18 | Documentation consistency | **DOCUMENTATION DRIFT** | §14 | Non-blocking for this assessment; blocking for republication | Future sync pass |
| 19 | Outstanding canonical decisions | **4 live gaps** | §13 | **Yes** | Repository Owner |
| 20 | Implementation evidence | **NONE** | No code, no migration, no CBOR entry exists anywhere | **Yes** | N/A until authorized |

---

## 16. Readiness Gates

**Gate 1 — Business Function: ✅ PASS.** Unambiguous. §1.1–1.2, independently re-verified word-for-word against CAP-001's Business Intent; no ambiguity found anywhere in 902 paragraphs / 36 tables read.

**Gate 2 — Architecture: ⚠️ CONDITIONAL PASS.** SD-002 is sufficient and authoritative *as reaffirmed by the Repository Owner and CAP-001* (§5), and its §13 content maps onto C-040 with zero contradiction (§6). It fails to be an unconditional PASS only because `PE-001-C040`'s own self-validation apparatus has not yet been resynchronized to that reaffirmation (§14) — a document-maintenance gap, not an architectural insufficiency.

**Gate 3 — Domain: ❌ FAIL.** Core entities are not defined as canonical Business Objects anywhere. Zero CBOR registration, zero Backend model, zero migration (§8).

**Gate 4 — Tenant: ❌ FAIL.** Tenant context and cardinality are explicitly, repeatedly self-declared "Pending Canonical Binding" by the specification's own text (§7).

**Gate 5 — Business Activities: ❌ FAIL.** Zero canonical BAs exist; all eight candidates classify Category D under `IMP-001 §6.2b`'s own canonical scale, because every execution path terminates at the same unresolved constitutional gap (§10).

**Gate 6 — Governance: ❌ FAIL.** Four live, self-declared Repository-Owner-or-architecture-level decisions remain open (§13).

**Gate 7 — Implementation: ❌ FAIL.** An engineer could not implement C-040 today without inventing canonical Tenant identity/allocation semantics, cardinality, or approval authority — precisely what BR-C040-03/13/15 forbid inventing locally. No architectural assumption is required only for the exception/recovery path (ERB-C040-08) in isolation, which is insufficient to constitute implementation readiness for the capability.

**5 of 7 gates fail.** Gates 1 and 2(conditional) pass; Gates 3–7 do not.

---

## 17. Open Questions

1. What authority allocates canonical Tenant identity, and through what mechanism (BR-C040-15)?
2. What is the Tenant–Organization cardinality (BR-C040-03)?
3. Who may approve tenant provisioning (BR-C040-13)?
4. Who may approve tenant migration (BR-C040-13)?
5. Who may approve tenant offboarding (BR-C040-13)?
6. Who may approve a cross-tenant sharing agreement (BR-C040-13), and does a sharing-agreement mechanism (TD-040) get chartered before or after C-040 itself?
7. When, and through what mechanism, should `PE-001-C040`'s own Primary Specification self-references (§14) be resynchronized — as its own dedicated document-maintenance pass, or bundled into a future C-040 BA charter's own gap-closure work?

None of these is answered by this assessment. All are stated here exactly as the specification's own text states them.

---

## 18. Required Repository Owner Decisions

Maximum decisions actually required to move C-040 forward (not manufactured beyond what blocks progress):

1. **Canonical Tenant identity/identifier-allocation authority** — what mechanism, if any, allocates it, and does `tenant_registry` (currently deferred) ever become that mechanism, or does a different one apply?
2. **Tenant–Organization cardinality** — one-to-one, one-to-many, or genuinely undetermined pending more information?
3. **Provisioning / migration / offboarding / cross-tenant-sharing approval authority** — who (which role, persona, or governance body) holds each of these four authorities?
4. **PE-001-C040 document synchronization** — authorize a dedicated remediation pass (per §14's register) as its own scoped task, separate from any future BA charter?

These four decisions are the same four gaps named in §13, restated here in decision form per the governing task's own §18 requirement — no additional decision was manufactured to pad this section.

---

## 19. Recommended Next Steps

Recommended, **not performed by this assessment**:

1. Repository Owner decision on Question 1 (§18) — the single most consequential gap, since every other candidate BA's Commit path depends on it.
2. Repository Owner decision on Question 2 (§18), likely resolvable together with Question 1 if the same mechanism that allocates identity also fixes cardinality.
3. Repository Owner decision on Question 3 (§18) — the four approval authorities may be resolvable as a single governance decision (e.g., naming a Tenant Administration Steward persona's own authorization model) rather than four independent ones; that determination itself belongs to whoever drafts the eventual decision brief, not to this assessment.
4. Only after 1–3 (or an explicit Repository Owner decision to defer C-040 entirely, mirroring C-114's own GAP-4 deferral precedent) — reassess candidate BA readiness; several (e.g., ERB-C040-08 Recovery) may reclassify from D toward C once the others are resolved.
5. Independently, and not blocking 1–4: authorize a narrow, separately-scoped `PE-001-C040` document-synchronization remediation pass per §14's register, since it is a Repository-Owner-approved-content-vs-document-currency issue, not an architecture question.

---

## 20. Final Readiness Classification

### 🔴 RED — Not Implementation Ready

- **Confidence level:** High. Corroborated identically across four independent analysis passes this session (capability-readiness pre-screen, Primary-Specification/Tenant-binding decision analysis, fresh-context independent verification, and this full-document readiness assessment) and by the specification's own 15+ internal "Pending Canonical Binding" self-declarations — not a single inference manufactured by this document that the specification's own authors did not already flag themselves.
- **Principal blockers:** (1) no canonical Tenant identity/identifier-allocation authority exists (BR-C040-15); (2) Tenant–Organization cardinality unresolved (BR-C040-03); (3) four approval authorities unresolved (BR-C040-13); (4) zero canonical Business Activities exist, and all eight candidates classify Category D under the very execution-path dependency chain items 1–3 create.
- **Non-blocking debt:** `PE-001-C040`'s own internal Primary Specification self-references (masthead, §2.1, §9.3, §8.5 Q4) remain unsynchronized with the Repository Owner's 2026-08-25 reaffirmation — a disclosed, tracked document-maintenance gap (§14), not an architecture defect; TD-040 (cross-tenant sharing mechanism absent platform-wide, Low severity, no current impact); the missing ARP-001 WP-2 implementation report (general repository evidentiary gap, not C-040-specific).
- **Required Repository Owner decisions:** the four listed in §18.
- **Required architecture decisions:** decisions 1–2 in §18 are architecture-level, not merely administrative — they may warrant a formal ADR once resolved, per this repository's own established practice (mirroring, e.g., `ADR-003`'s own treatment of the analogous TenantService question).
- **Required document maintenance:** the four-location masthead/self-validation correction in §14, explicitly **not** a mechanical find-replace (§14's own conclusion).
- **Earliest point implementation could legitimately begin:** only after Repository Owner decisions 1–3 (§18) are made and a fresh, Business-Activity-specific implementation-readiness gap analysis is performed per `CLAUDE.md §19.7` and `IMP-001 §6.2b`'s own explicit requirement that a D→C reclassification does not, by itself, authorize implementation. This assessment does not estimate a date or WP number for that point — doing so would exceed this assessment's own read-only, analysis-only scope.

---

# PART II — FRESH RE-ASSESSMENT (2026-08-26)

## 21. Fresh Re-Assessment Authorization and Baseline

**Commissioned by:** explicit Repository Owner decision, 2026-08-26 ("C-040 — COMMISSION THE FRESH IRA"), pursuant to `CLAUDE.md §19.7`. This decision explicitly resolved the sequencing question raised by the same-day read-only "C-040 — Final IRA Prerequisite Reconciliation": the Repository Owner elected to commission this re-assessment now rather than wait for `AI-002`/`AI-004` accountability-point appointment, and explicitly accepted that this re-assessment may — and, as found below, does — continue to report `AI-002`'s unpopulated accountability point as an open finding. Commissioning this re-assessment does not itself constitute, and is not treated anywhere below as, appointment to `AI-002`.

**Method:** this is an in-place amendment of the existing `IRA-C040` document (Part I above, unmodified except for this appended Part II), per this repository's own established amend-in-place precedent (`TDS-017 §21`–`27`; `ADR-014`/METH-001) and the commissioning instruction's own explicit prohibition on creating a duplicate IRA. Part I is preserved verbatim as the historical record of the 2026-08-25 assessment; Part II re-applies the same methodology (`IMP-001 §6.2b`'s A–E scale; the seven Readiness Gates of §16) against the current repository baseline and states only where and why conclusions change.

**Baseline re-verified directly for this re-assessment, not assumed from prior-session memory:**
- `ROD-C040-Blocker-Closure-Assessment.md` (full re-read).
- `ADR-024` through `ADR-035` (existence and Accepted status confirmed).
- `AI-001`, `AI-002`, `AI-003` (full re-read).
- `TDS-016`, `TDS-017` (full re-read, including each document's own Non-Goals/Dependencies/Implementation Authorization Boundary sections).
- `TD-157`, `TD-158` (current text re-read directly from `TECH-DEBT.md`).
- `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md` (current C-040 row, §5, D-003).
- `CBOR-INDEX.md` (current register — 8 rows, no Tenant entry).
- `AuthService` source directly: `models/authority_holder.py`, `repositories/authority_holder_repository.py`, `dependencies.py` (`require_ai001_holder`/`require_ai002_holder`), `routers/auth.py` (`/auth/authority-login/*`, `/auth/authority-check/*`), `middleware/tenant.py` (exemption entries), `alembic/versions/...a1b2c3d4e5f6_authority_holders.py`.
- `tenant_registry`/`organization_master` implementation search: zero matches in `models/`, `repositories/`, `alembic/versions/` (re-confirmed this pass).
- Full `AuthService` regression suite: re-run fresh this pass — **810 passed, 0 failed**.

## 22. Baseline Changes Since the Original Assessment (2026-08-25 → 2026-08-26)

| Item | 2026-08-25 (Part I) | 2026-08-26 (current) | Source |
|---|---|---|---|
| Tenant–Organization cardinality | PENDING CANONICAL BINDING | **Resolved — 1:1** | `ADR-025` |
| Canonical Tenant system-of-record mechanism | Not addressed; `tenant_registry` DEFERRED, non-canonical | **`tenant_registry` adopted as implementation candidate**, conditional on remediation | `ADR-034` |
| `tenant_registry` remediation design | Did not exist | **Complete** — 20-section TDS, independently reviewed and corrected | `TDS-016` |
| Business Approval Authority (identity) | PENDING CANONICAL BINDING | **Constitutionally established**; accountability point appointed (Ashit Padhi) | `ADR-029 §10`, `AI-001`, `AI-003` |
| Infrastructure Allocation Authority (identity) | PENDING CANONICAL BINDING | **Constitutionally established**; accountability point **unpopulated** — 15 independent Key-2 cases, frozen | `ADR-029 §11`, `AI-002`, `TD-157` |
| Business Governance Authority membership structure | Not addressed | **Resolved** — minimum-membership structure defined | `ADR-035` |
| Two-Key/Key-2 appointment mechanism | Not addressed | **Ratified and twice-proven** (`AI-001`, `AI-003`) | `ADR-030`–`ADR-033` |
| Runtime mechanism for AI-001/AI-002 as enforceable authorization | Not addressed; not yet identified as a gap | **Design resolved and implemented**: pre-Organization authentication + live-lookup runtime authorization, independent of the five-tier `organization_id`-mandatory Authorization Engine | `TDS-017`, `authority_holders` table/model/repository/migration, `dependencies.py`, `routers/auth.py` |
| Runtime mechanism test coverage | Not addressed | **12 dedicated tests + full 810-test regression, 0 failures**, independently reviewed | `tests/test_authority_holder.py` |
| BA-charter scoping decision | Not addressed; all 8 candidate BAs treated as equally unscoped | **Resolved** — minimum scope is "Tenant Establishment only (Business Approval → Infrastructure Allocation)", explicitly excluding migration/offboarding/sharing/Technical Provisioning as disclosed future scope | `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md`, 2026-08-26 |
| CBOR registration | Not addressed (Part I §7 found no CBOR entry, treated as a general absence) | Tenant **preliminarily passes** the `CMD-001 §26.3a` eligibility test (ELIGIBLE); **actual registration (registering ADR) not yet performed** — explicitly deferred, not required to reach this point | `TDS-016 §13`, `CBOR-INDEX.md` (still 8 rows, unchanged) |
| `tenant_registry` schema/migration/code | Did not exist | **Still does not exist** — design-only | Verified directly, this pass |
| Tenant Establishment business transaction/API | Did not exist | **Still does not exist** | Verified directly, this pass |
| AI-001 runtime holder record | Did not exist (concept did not exist yet) | Mechanism exists; **record not populated** — no legitimate `Person` record for Ashit Padhi exists; not fabricated | Verified directly, this pass |
| Migration/offboarding/sharing approval authorities | PENDING CANONICAL BINDING | **Unchanged — still PENDING CANONICAL BINDING**, but now explicitly out of the chartered minimum scope, not silently dropped | `ROD-C040-Blocker-Closure-Assessment.md §3` item 16; Delivery Map |
| Technical Provisioning Authority | Not separately addressed in Part I | **Still undecided**, explicitly out of chartered minimum scope | `ADR-026 §13`; Delivery Map |
| `PE-001-C040` document synchronization debt (§14) | Open | **Unchanged — still open**, non-blocking | `IRA-C040 §14` (Part I) |

**Net effect:** three of Part I's four "live governance gaps" (§13) are now resolved for the chartered minimum scope (identity/allocation mechanism decided; cardinality decided; the *relevant subset* of BR-C040-13's four approval authorities — provisioning only — resolved). The fourth (document sync) is unchanged. Migration/offboarding/sharing approval authorities remain open but are no longer in scope for what is being assessed for implementation-readiness purposes — they are future-scope items, not blockers of the chartered BA, per the Repository Owner's own 2026-08-26 scoping decision.

## 23. Gate-by-Gate Re-Assessment

Re-applying §16's own seven gates, scoped to the chartered minimum-scope candidate BA ("Tenant Establishment") wherever a gate's original finding was scope-dependent; noted explicitly wherever a gate is scope-independent and therefore unchanged.

**Gate 1 — Business Function: ✅ PASS.** Unchanged — scope-independent; not re-examined.

**Gate 2 — Architecture: ✅ PASS (upgraded from ⚠️ CONDITIONAL PASS).** SD-002 remains sufficient and authoritative (unchanged). What was missing in Part I — a concrete technical design translating SD-002 §13 into an actual schema/transaction/authorization design for C-040 — now exists and has been independently reviewed twice (`TDS-016`, `TDS-017`). The `PE-001-C040` self-reference drift (§14) remains open but was already correctly classified as non-blocking for the *architecture* gate in Part I, and remains so.

**Gate 3 — Domain: ❌ FAIL (unchanged in outcome, narrowed in reason).** No canonical Business Object registration exists for Tenant; no Backend model, repository, or migration exists (re-verified directly, this pass, zero matches). This is no longer "no design exists to build against" (Part I's finding) — it is now "a complete, reviewed design exists (`TDS-016`) and has simply not been built or registered yet." This is a **Category B (implementation prerequisite)** finding now, not a Category A (governance/constitutional) finding — the distinction the commissioning decision explicitly asked this re-assessment to preserve. Per `ROD-C040-Blocker-Closure-Assessment.md §7`'s own explicit and uncontested disclaimer, this does not gate commissioning of this IRA and is not treated as a Gate-3-blocks-everything finding the way Part I's absence-of-any-design did.

**Gate 4 — Tenant: ✅ PASS (upgraded from ❌ FAIL).** Cardinality resolved 1:1 (`ADR-025`). System-of-record mechanism resolved at the decision level — `tenant_registry` adopted as implementation candidate (`ADR-034`), with a complete, reviewed remediation design (`TDS-016`) translating that decision into schema/constraints/lifecycle. Both of Part I's "Pending Canonical Binding" findings for this gate are closed.

**Gate 5 — Business Activities: ⚠️ CONDITIONAL PASS (upgraded from ❌ FAIL), scoped to the chartered candidate BA only.** Applying `IMP-001 §6.2b`'s A–E scale to "Tenant Establishment" specifically (§24 below): **reclassifies from Category D to Category C** — ordinary implementation-level design work remains, but no open constitutional or governance question blocks it. The other seven candidate BAs from Part I §10 (Understand Standing, Frame Intent for migration/offboarding/sharing, Commit for those actions, Resolve/Distribute Effective State, Recovery) remain Category D or are not yet re-examined, because they remain outside the chartered minimum scope — this gate is a conditional pass for the chartered scope, not a claim that all eight original candidates have been resolved.

**Gate 6 — Governance: ⚠️ CONDITIONAL PASS (upgraded from ❌ FAIL), scoped to the chartered candidate BA.** Of Part I §13's four live gaps: (1) Tenant identity/allocation authority — resolved (`ADR-034`/`TDS-016`); (2) cardinality — resolved (`ADR-025`); (3) approval authority — resolved for the provisioning/establishment subset in scope (`AI-001`, `AI-002` both constitutionally established; `AI-002`'s accountability point remains unpopulated — see §26 below, tracked as `TD-157`, a data/environment-readiness item, not a reopened governance question); migration/offboarding/sharing approval authority remains open but is explicitly out of chartered scope, not silently dropped (Delivery Map, `ROD-C040-Blocker-Closure-Assessment.md §3` item 16). (4) Document sync — unchanged, open, non-blocking. This is a conditional, not unconditional, pass because `AI-002`'s seat remaining empty is a genuine, disclosed, currently-unresolved fact that this re-assessment is required to keep surfacing, per the commissioning decision's own explicit instruction.

**Gate 7 — Implementation: ⚠️ CONDITIONAL PASS (upgraded from ❌ FAIL).** An engineer could now begin implementing the chartered minimum-scope BA today without inventing any canonical semantics — `TDS-016` supplies the schema/transaction design, `TDS-017` supplies the (already-built and tested) authorization mechanism. What remains is ordinary implementation work (build `tenant_registry`, wire the Establishment transaction/endpoint, populate `AI-001`'s runtime holder with a legitimate identity record) plus one disclosed, non-architectural dependency this re-assessment does not attempt to resolve: full end-to-end live execution of the Establishment transaction's Infrastructure Allocation half cannot occur until `AI-002` is populated. Implementation *can begin*; implementation *cannot be exercised end-to-end* yet. This is precisely the "implementation prerequisite vs. IRA gate" distinction the commissioning decision required this re-assessment to preserve, not collapse.

**Revised gate count: 2 unconditional PASS (Gates 1, 4), 3 conditional PASS (Gates 2, 6, 7 — Gate 2 arguably unconditional; kept as PASS above), 1 conditional PASS specific to the chartered scope (Gate 5), 1 FAIL (Gate 3, downgraded from a constitutional to an implementation-level finding).** Compare to Part I's 5-of-7 FAIL. This is a materially different position, not a reconfirmation of Part I's RED.

## 24. Minimum-Scope Candidate BA Reclassification

Re-applying `IMP-001 §6.2b`'s A–E scale to the one candidate BA now actually chartered — **"Tenant Establishment" (Business Approval → Infrastructure Allocation)**, `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md`, 2026-08-26 — as opposed to Part I §10's undifferentiated treatment of all eight ERB-derived candidates:

| Dimension | Part I (2026-08-25) | Part II (2026-08-26) |
|---|---|---|
| Canonical Tenant identity/allocation authority (BR-C040-15) | PENDING CANONICAL BINDING | Resolved — `ADR-034`, `TDS-016` |
| Cardinality (BR-C040-03) | PENDING CANONICAL BINDING | Resolved — `ADR-025`, 1:1 |
| Provisioning approval authority (BR-C040-13, provisioning subset) | PENDING CANONICAL BINDING | Resolved — `AI-001`/`AI-002` both constitutionally established |
| Runtime enforceability of that authority | Not yet identified as a distinct gap | Resolved and implemented — `TDS-017`, tested |
| Schema/transaction design | Did not exist | Complete — `TDS-016` §8/§9/§10 |
| Actual build | Did not exist | Still does not exist (Category B, disclosed) |
| Accountability-point population | N/A (authorities did not yet exist) | `AI-001` appointed; `AI-002` unpopulated (`TD-157`, frozen) |

**Classification: Category C — "Architecture requires completion (implementation-level). Ordinary implementation-level design work remains (persistence mechanism, endpoint shape, service/repository composition), but no open constitutional or governance question blocks it."** This is a genuine reclassification from Part I's Category D finding for this same underlying business need (there, framed as "Commit Tenant Administrative Transition," ERB-C040-05), not a relabeling — every constitutional/governance question that caused the original D classification (BR-C040-15, BR-C040-03, the provisioning subset of BR-C040-13) has a cited, ratified resolution. The disclosed, non-architectural dependency on `AI-002` population governs *live execution*, not the classification of this BA's *readiness for implementation design and build to begin* — the same distinction `TDS-016 §19` and `TDS-017`'s own Non-Goals sections already draw, restated here as the reclassification's own basis, not invented for this re-assessment.

The other seven Part I candidate BAs are unaffected by this reclassification and remain outside the chartered scope; this re-assessment does not re-examine them, consistent with the commissioning decision's own instruction not to resurrect scope the Repository Owner has not chartered.

## 25. Updated Implementation Readiness Matrix (Delta Only)

Restating only the rows of Part I §15 whose status changed; all other rows (1, 2, 4, 9, 12, 14, 17) are unchanged and not repeated.

| # | Category | Part I Status | Part II Status | Blocker? |
|---|---|---|---|---|
| 3 | Architecture authority | RATIFIED but documentation drift | **RATIFIED, with two independently-reviewed TDS artifacts now grounding it** (§22) | No |
| 5 | Business Activity completeness | PROPOSED, zero canonical | **One candidate BA chartered and reclassified to Category C** (§24); zero *formally chartered* (no WP/BA number assigned yet — a chartering action, not a readiness question) | Charter assignment: administrative, not a gap; Category C completion: implementation, Category B |
| 6 | Domain/data model completeness | UNRESOLVED | **Designed, reviewed, not yet built** (`TDS-016`) | Category B, not A |
| 7 | Identity/authorization readiness | PARTIALLY DEFINED | **Designed and implemented for the provisioning/establishment scope** (`TDS-017`, tested); accountability-point population for `AI-002` remains open (`TD-157`) | Category C (data readiness), not A |
| 8 | Tenant-context readiness | PENDING CANONICAL BINDING | **Resolved** (`ADR-025`, `ADR-034`) | No |
| 15 | Governance approvals | PENDING CANONICAL BINDING | **Resolved for chartered scope**; migration/offboarding/sharing remain open but out of scope | No, for chartered scope |
| 19 | Outstanding canonical decisions | 4 live gaps | **0 live gaps for chartered scope**; document-sync (§14) and out-of-scope migration/offboarding/sharing authorities remain open, disclosed | No, for chartered scope |
| 20 | Implementation evidence | NONE | **`TDS-017` implemented and tested (810/810); `TDS-016` designed, not built; zero CBOR registration; zero Tenant Establishment code** | Partial — see §26 |

## 26. Blocker Classification (A–F)

Per the commissioning decision's own required distinction — true governance blockers vs. implementation prerequisites vs. data/environment readiness vs. disclosed future scope vs. already-resolved decisions vs. tracked technical debt:

**A — True Category-A readiness blockers (constitutional/governance), for the chartered minimum scope:** **None found.** This is the headline finding of this re-assessment. (Migration/offboarding/sharing approval authorities remain genuine Category-A gaps, but only for scope the Repository Owner has explicitly not chartered — see D below.)

**B — Implementation prerequisites, not IRA gates:**
- `tenant_registry` schema, migration, Backend model/repository/service (`TDS-016`, unbuilt).
- Tenant Establishment business transaction/API/endpoint (does not exist).
- CBOR registration — a registering ADR for Tenant as a Canonical Business Object (`TDS-016 §13`; preliminarily ELIGIBLE, not yet registered).
- C-040-specific event/audit type naming (Part I §11/§12, still undefined).
- `AI-001`'s own runtime authorization dependency (mirroring `require_platform_admin`), per `TDS-016 §12`'s disclosed design-not-yet-built statement.

**C — Data/environment readiness:**
- `AI-001` runtime holder record — mechanism built and tested (`authority_holders`); no legitimate `Person` record exists for Ashit Padhi; not fabricated, per explicit standing instruction.
- `AI-002` accountability-point appointment — constitutionally established (`ADR-029 §11`, `AI-002`); accountability point unpopulated; 15 independent Key-2 cases completed across two candidates; Sarika Rath evidentiary path concluded and **permanently frozen** (`TD-157`, `ROD-C040-AI-002-Sarika-Rath-Inspected-WhatsApp-Screenshot-Case-Outcome.md`); no `AI-004` exists. **Per explicit instruction, this re-assessment draws no conclusion that Sarika Rath is ineligible, that she did not consent, that no suitable human exists, or that the Key-2 mechanism is defective — only that no case has yet succeeded.** No further evidence search was performed and none is authorized by this task.

**D — Future/disclosed scope, not blockers of the chartered BA:**
- Migration approval authority (BR-C040-13 subset) — PENDING CANONICAL BINDING, explicitly excluded from chartered minimum scope.
- Offboarding approval authority (BR-C040-13 subset) — same.
- Cross-tenant sharing approval authority (BR-C040-13 subset) — same; mechanism itself absent platform-wide (`TD-040`, Low severity).
- Technical Provisioning Authority (`ADR-026 §13`) — entirely undecided, explicitly out of chartered scope.
- `PE-001-C040` document synchronization debt (Part I §14) — four label-drift locations plus one self-validation check requiring re-execution; non-blocking, unchanged.

**E — Governance decisions already resolved (not re-litigated here):**
- Tenant–Organization cardinality — `ADR-025`.
- `tenant_registry` adoption as system-of-record implementation candidate — `ADR-034`.
- Business Approval Authority identity and architectural model — `ADR-029 §10`.
- Infrastructure Allocation Authority identity and architectural model — `ADR-029 §11`.
- Business Governance Authority minimum membership structure — `ADR-035`.
- Two-Key/per-case Key-2 appointment mechanism — `ADR-030`–`ADR-033`, twice-proven (`AI-001`, `AI-003`).
- BA-charter minimum-scope scoping decision — Delivery Map, 2026-08-26.
- Authority Runtime Enforcement design and implementation boundary — `TDS-017`.

**F — Technical debt (tracked, not blocking this re-assessment):**
- `TD-157` — `AI-002` accountability point unpopulated. Status: **Open — BLOCKED.** Severity: High. Sarika Rath path frozen after 15 cases; no further candidate search authorized by this or any prior task.
- `TD-158` — `AuthService` `TenantMiddleware`/`X-Tenant-ID` legacy Organization-scoped compatibility surface disclosure.
- `TD-040` — cross-tenant sharing mechanism absent platform-wide. Low severity; no current impact; out of chartered scope regardless.
- `PE-001-C040` document synchronization debt (Part I §14) — four locations plus one self-validation re-execution, not re-classified as a numbered TD entry by this re-assessment (outside this task's authorized scope: `TECH-DEBT.md` may not be modified by this task).

## 27. Final IRA Output — Required Answers

1. **Is C-040 Implementation Ready?** Not yet unconditionally — but no longer for the constitutional/governance reasons Part I found. **AMBER — Conditionally Ready**, for the chartered minimum-scope BA only (§28).
2. **What blockers remain?** Two Category-B implementation prerequisites (build `tenant_registry`; build the Tenant Establishment transaction) and two Category-C data/environment items (`AI-001` runtime holder population; `AI-002` accountability-point population, frozen).
3. **Which blockers are constitutional?** None, for the chartered scope (§26-A).
4. **Which are implementation gaps?** `tenant_registry` schema/migration/code; Tenant Establishment endpoint; CBOR registration; event/audit taxonomy (§26-B).
5. **Which are data/environment dependencies?** `AI-001` and `AI-002` runtime holder population (§26-C).
6. **Which are future scope rather than blockers?** Migration/offboarding/sharing approval authorities; Technical Provisioning Authority; document synchronization debt (§26-D).
7. **Which technical debts remain?** `TD-157`, `TD-158`, `TD-040`, and the unreclassified `PE-001-C040` document-sync debt (§26-F).
8. **What exact conditions must be satisfied to move C-040 to GREEN, for the chartered minimum-scope BA?**
   - Formally charter the BA (assign WP/BA identifier) — administrative, not a readiness gap.
   - Build `tenant_registry` schema/migration/Backend model per `TDS-016`.
   - Wire and test the actual Tenant Establishment transaction/endpoint.
   - Populate `AI-001`'s runtime holder record with a legitimate `Person` identity (no fabrication).
   - Author a CBOR registering ADR for Tenant, per `TDS-016 §13`.
   - Satisfy `CLAUDE.md §21.4`'s Mandatory Tenant-Isolation Test Checklist and `TDS-016 §16`'s own test strategy.
   - Complete Independent Certification / V&V / Release Readiness per `CLAUDE.md §19.7b`.
   - **Separately, and not owned by this BA's own implementation work:** `AI-002` accountability-point population remains required before the Infrastructure Allocation half of the Establishment transaction can be *exercised* end-to-end. This is not resolved, not waived, and not treated as resolved by this re-assessment — it remains `TD-157`, Open — BLOCKED, and no further candidate search is authorized here.

No new governance requirement is invented by this list; every item is either already named in `TDS-016`/`TDS-017`'s own Dependencies sections or is the ordinary completion of design work those documents already specify.

## 28. Updated Final Readiness Classification

### 🟡 AMBER — Conditionally Ready (upgraded from 🔴 RED, Part I, 2026-08-25)

**Scope of this classification:** the chartered minimum-scope candidate BA — Tenant Establishment (Business Approval → Infrastructure Allocation) — only. This classification does not extend to migration, offboarding, cross-tenant sharing, or Technical Provisioning, all of which remain explicitly out of scope and unassessed for readiness by this re-assessment.

**Confidence level:** High. Every upgrade cited above traces to a specific, ratified ADR, a specific Appointment Instrument, or a specific, independently-reviewed TDS — none is inferred or manufactured by this re-assessment.

**Why AMBER, not GREEN:** two genuine, disclosed, unresolved dependencies remain: (1) `tenant_registry` and the Tenant Establishment transaction itself are designed but not built (Category B); (2) `AI-002`'s accountability point remains unpopulated, blocking full end-to-end live execution of the transaction's Infrastructure Allocation half (Category C, `TD-157`, frozen). Neither is a constitutional or governance gap; both are ordinary, already-disclosed, already-tracked completion items.

**Why AMBER, not RED:** every constitutional/governance gap Part I found for this specific business need (canonical Tenant identity/allocation authority, cardinality, the provisioning subset of approval authority) has a cited, ratified resolution. An engineer could begin implementation today without inventing any canonical semantics — the defining condition of Part I's RED (§20, "precisely what BR-C040-03/13/15 forbid inventing locally") no longer holds for this scope.

**This re-assessment does not resolve `AI-002`.** Per the commissioning decision's own explicit instruction, `AI-002` remains constitutionally established but unpopulated; the Sarika Rath evidentiary path remains concluded and permanently frozen after 15 cases; no `AI-004` is created; no further candidate search is performed or recommended by this document.

---

## Change Control — Part II Amendment

**Files modified this pass:** this document only (`IRA-C040_...md`) — Part II (§21–28) appended; Part I preserved verbatim, unmodified.
**Files created:** none. **Files deleted:** none.
**Not modified, per explicit instruction:** any ADR; `AI-001`/`AI-002`/`AI-003`; no `AI-004` created; `TECH-DEBT.md`; the Delivery Map; `TDS-016`; `TDS-017`; `tenant_registry` code (none exists); `AuthService` code; schema; migrations; `CBOR-INDEX.md`; any runtime authority record.
**Not performed:** no Key-2 case; no AI-002 evidence search; no implementation of `tenant_registry` or Tenant Establishment; no CBOR registration.
**Regression evidence:** full `AuthService` test suite re-run fresh this pass — 810 passed, 0 failed.
**Commit/push:** none — not authorized for this task.

---

# PART III — POST-IMPLEMENTATION FINAL READINESS REASSESSMENT (2026-08-26)

## 29. Authorization and Baseline

**Commissioned by:** explicit Repository Owner instruction, 2026-08-26 ("C-040 — FINAL READINESS REASSESSMENT AFTER IMPLEMENTATION"), following completion of the TDS-016 implementation this same instruction's own baseline reports (Part II's own AMBER classification, then the separate, explicitly-authorized implementation pass). This is a read-only reassessment — no code, schema, migration, ADR, AI artifact, `TD-157`, Delivery Map, or `CBOR-INDEX.md` change is made by this Part.

**Every implementation claim was independently re-verified against the actual repository, not taken from the implementing pass's own report:**
- `models/tenant_registry.py`, `models/organization.py` (`tenant_id` column, line 97), `repositories/organization_repository.py` (`establish_tenant_if_unset`), `services/tenant_establishment_service.py`, `routers/tenant_establishment.py`, `schemas/tenant_establishment.py` — read directly, this pass.
- `alembic heads` — confirmed single head `b2c3d4e5f6a7`, revising `a1b2c3d4e5f6` (the `TDS-017` migration) — no branching, no orphaned head.
- `main.py` — confirmed `tenant_establishment` router imported and included at `prefix="/tenants"`.
- `middleware/tenant.py` — confirmed exactly one additive exemption line (`/tenants`), no change to any other path's own exemption or to `X-Tenant-ID`'s meaning.
- `routers/tenant_establishment.py` / `services/tenant_establishment_service.py` — confirmed `require_ai002_holder` (unmodified, `TDS-017`) is the sole authorization gate; no `PLATFORM_ADMIN`/`AUREX_ADMIN` reference exists in either file except in a docstring explicitly documenting their *non*-substitution.
- Full `AuthService` regression suite re-run fresh, independently, this pass: **823 passed, 0 failed** (810 pre-existing + 13 new `test_tenant_establishment.py` tests), confirming the implementing pass's own reported count rather than trusting it.

## 30. Reassessed Readiness Gates (Part II → Part III)

| Gate | Part II (pre-implementation) | Part III (post-implementation) | Why it changed |
|---|---|---|---|
| 1 — Business Function | PASS | **PASS** (unchanged) | Scope-independent |
| 2 — Architecture | PASS | **PASS** (unchanged) | Design docs now additionally corroborated by matching, tested code |
| 3 — Domain | FAIL (designed, not built) | **CONDITIONAL PASS** | `tenant_registry` table and `organizations.tenant_id` now exist, migrated, tested (§31 below). Still conditional: no `CMD-001 §26` registering ADR exists yet (`TDS-016 §13`'s own preliminarily-ELIGIBLE, not-yet-registered finding, unchanged) — a disclosed, non-blocking future action, not a rebuilt or newly-discovered gap |
| 4 — Tenant | PASS | **PASS** (unchanged) | Cardinality/system-of-record decisions unaffected by implementation |
| 5 — Business Activities | CONDITIONAL PASS (Category D→C reclassification) | **PASS** | The chartered BA's own "ordinary implementation-level work" (Category C's own defining content) is now complete, tested, and verified — advancing it to Category A/B on `IMP-001 §6.2b`'s own scale ("an existing implementation satisfies the Business Activity as-is" / "requires no new architectural or constitutional groundwork") |
| 6 — Governance | CONDITIONAL PASS | **PASS** | Re-examined precisely (§32 below): every governance *decision* this gate measures (cardinality, system-of-record mechanism, both authorities' identity and architectural model, BGA membership structure, BA-scope decision) is resolved. `AI-002`'s empty seat is a *data/appointment-execution* fact, not an open *decision* — reclassified to its own Runtime/Data Readiness dimension (§32), not carried as a Governance-gate failure |
| 7 — Implementation | CONDITIONAL PASS ("can begin, cannot be exercised end-to-end") | **PASS** | Implementation is not merely possible — it is done, tested (823/823), and independently re-verified this pass. The "cannot be exercised end-to-end in production" fact is a production-operational-readiness fact (§32), not an implementation-readiness fact — `IMP-001 §6.2b`'s own A–E scale does not measure real-world data population |

**Six gates now PASS, one Conditional Pass (Domain, on CBOR registration alone).** Compare Part II's 2 PASS / 4 conditional / 1 FAIL, and Part I's 5-of-7 FAIL.

## 31. Implementation Verification (Direct)

| Item | Verified | Evidence |
|---|---|---|
| `tenant_registry` exists | Yes | `models/tenant_registry.py`; migration `b2c3d4e5f6a7` creates it; `alembic upgrade ... --sql` DDL confirmed against PostgreSQL dialect |
| `organizations.tenant_id` exists | Yes | `models/organization.py` line 97; nullable, `UNIQUE`, FK to `tenant_registry.id` — matches `TDS-016 §5/§7` exactly (nullable preserved, no `NOT NULL` added) |
| Constraints/invariants | Yes | `ck_tenant_registry_lifecycle_state` (four-state CHECK); `uq_tenant_registry_tenant_code`; `uq_organizations_tenant_id`; atomicity/immutability enforced at the service layer per `TDS-016 §6` |
| Atomic Establishment transaction | Yes | `services/tenant_establishment_service.py::establish()` — pre-check, live `AI-001` lookup, INSERT, conditional `UPDATE ... WHERE tenant_id IS NULL`, rowcount-based rollback — matches `TDS-016 §8`'s six steps exactly |
| Four-state lifecycle, Establishment → PROVISIONED only | Yes | `TenantLifecycleState` enum; no `MIGRATING`/`OFFBOARDING` transition implemented (correctly out of scope) |
| Authorization (`AI-002` gate, no bypass) | Yes | `require_ai002_holder` (`TDS-017`, unmodified) is the sole gate; test suite confirms `PLATFORM_ADMIN`/`AUREX_ADMIN` do not substitute |
| Audit attribution | Yes | `approved_by_actor_id`/`approved_at` (live `AI-001` holder), `allocated_by_actor_id`/`allocated_at` (caller), both written in the one atomic transaction, plus `record_audit`/`publish_event` per this repository's own established convention |
| Duplicate/replay handling | Yes | Pre-check (404/409) + conditional-UPDATE rowcount guard; tested (`test_duplicate_establishment_rejected`) |
| Rollback | Yes | Explicit `session.rollback()` on lost-race; tested (`test_rejected_establishment_leaves_no_orphaned_tenant_row`) confirms zero orphaned rows |
| API | Yes | `POST /tenants`, wired in `main.py`, exempted in `middleware/tenant.py` (additive only) |
| Tests | Yes | 13 focused tests, covering the Repository Owner's own minimum list A–L (`tests/test_tenant_establishment.py`) |
| Regression | Yes | 823/823, independently re-run this pass |
| Scope confinement | Yes | No Technical Provisioning, migration, offboarding, or cross-tenant-sharing code exists anywhere in the new files; `Backend/Services/TenantService` (the separate, mocked scaffold, `ADR-003`) untouched |

## 32. Runtime Authority Holder Classification (Critical Question)

Distinguishing the five layers precisely, per the commissioning instruction's own requirement:

1. **Constitutional appointment** — `AI-001`: done (`AI-003`, Ashit Padhi). `AI-002`: not done (`TD-157`, frozen).
2. **Runtime holder population** (`authority_holders` table rows) — **neither** `AI-001` nor `AI-002` has a row. This is narrower than layer 1: even the constitutionally-appointed `AI-001` has no runtime row, because no legitimate `Person` record for Ashit Padhi exists and none was fabricated (explicit standing instruction, honored throughout).
3. **Implementation readiness** — fully satisfied. The mechanism is built, migrated, and tested; it correctly and universally denies every caller today, which is the *correct* behavior for an unpopulated authority, not a defect.
4. **Production operational readiness** — not satisfied. No real caller can successfully invoke `POST /tenants` today, because no real person occupies either seat. This is a fact about data, not about code.
5. **IRA GREEN status** — the classification this reassessment must determine.

**Classification: B — a Category-B/C implementation-and-data readiness item that prevents production operational readiness (layer 4) but does NOT prevent IRA GREEN / implementation-ready classification.**

**Exact canonical basis, cited, not invented:**
- `IMP-001 §6.2b`'s own A–E scale — the repository's own canonical rubric for exactly this classification question — measures whether "an existing implementation satisfies the Business Activity as-is" and whether "an open constitutional or governance question... must be resolved... before implementation-level design can proceed." Nothing in this rubric's own five category definitions references real-world data population; it measures architectural and governance completeness, both of which are satisfied here.
- `TDS-016 §19` and `TDS-017`'s own repeated, explicit, already-established distinction — restated, not newly invented, by this reassessment — between "blocks live execution" and "does not block design/implementation completeness." This reassessment extends that same distinction one further step, consistently: now that implementation itself (not merely design) is complete, the identical distinction separates "blocks production execution" from "blocks implementation-readiness classification."
- `ROD-C040-Blocker-Closure-Assessment.md §7`'s own express statement that "no code, API, migration, or Business Activity implementation is required before the fresh IRA — the IRA re-assesses readiness against the now-resolved governance baseline, it does not require implementation to already exist." If implementation need not even exist for the IRA to proceed, a fortiori a data/environment fact — a strictly narrower category than "implementation" — cannot be read as a harder gate than implementation itself was.
- `CLAUDE.md §19.8.1`/`§19.8.5` — Technical Debt's own governing definition includes items "intentionally deferred," and its prohibition list (architectural, security, data-integrity, tenant-isolation defects; failing tests; broken functionality) does not name a data-population gap for a constitutional authority. The functionality is not broken — it is verified, by 13 passing tests using isolated, disclosed test-only fixtures, to behave exactly as designed in both the populated and unpopulated case.

**Distinguished explicitly, per the commissioning instruction's own requirement:** this reassessment does **not** find that either `AI-001` or `AI-002` is now "populated," "activatable," or "live." It finds only that the *absence* of population does not, under this repository's own canonical rubric for implementation-readiness classification, belong in the same category as an unresolved constitutional or architectural gap. Production operational readiness (layer 4) and IRA GREEN status (layer 5) are not the same question — `CLAUDE.md §20.4`'s own Demonstrability standard ("a real persona, using the real frontend, exercising the real API, producing a real, persisted outcome") governs *Work Package completion* (§20.7, extending §19.7), a later, separate gate this capability has not yet reached because no WP/BA has been formally chartered — it does not govern IRA commissioning or classification, exactly as `ROD-C040-Blocker-Closure-Assessment.md §7` already established implementation itself need not precede the IRA.

## 33. AI-002 — Assessed Exactly As It Currently Exists (Not Reopened)

- Constitutionally established (`ADR-029 §11`, `AI-002`).
- Accountability point unpopulated.
- `TD-157` — Open — BLOCKED, High severity.
- Fifteen independent Key-2 cases completed across two candidates.
- The Sarika Rath evidentiary path is concluded and **permanently frozen** (`ROD-C040-AI-002-Sarika-Rath-Inspected-WhatsApp-Screenshot-Case-Outcome.md`).
- No `AI-004` exists. None is created by this reassessment.
- No further evidence search was performed or is recommended by this document.

**Per §32's own classification, this stands as an explicitly disclosed Category-C Runtime/Data Readiness finding.** The current IRA methodology (`IMP-001 §6.2b`, applied throughout this document) permits GREEN while a disclosed Category-C finding remains open, for the same reason it already permits GREEN while Technical Debt remains open generally (`CLAUDE.md §19.8`'s own "visible, justified, prioritised, planned, tracked, eventually resolved" standard, not "resolved before GREEN"). No new requirement is invented by this finding — `TD-157`'s own existing disposition (Open — BLOCKED) is restated, not altered.

## 34. Tenant Establishment — Business Capability Confirmation

Directly confirmed, this pass (§31): the business capability now exists as a real, callable API (`POST /tenants`), backed by a real atomic transaction, real persisted state (`tenant_registry`, `organizations.tenant_id`), real authorization (`AI-002` live lookup, no bypass), real audit attribution, real duplicate/rollback handling, and a real four-state lifecycle model (Establishment producing `PROVISIONED` only). Thirteen focused tests exercise all of this directly.

**This removes the previous Category-B/domain implementation failure (Part II Gate 3's "designed, not built" finding) in full.** What remains at Gate 3 is narrower and disclosed: formal `CMD-001 §26` CBOR registration, a future, non-blocking action per `TDS-016 §13`'s own already-established treatment.

## 35. No Scope Expansion — Confirmed

Consistent with the commissioning instruction's own list, none of the following is treated as a blocker by this reassessment, because the canonical minimum C-040 scope does not require them for the chartered BA: Technical Provisioning (`ADR-026 §13`); migration; offboarding; cross-tenant sharing; future lifecycle transitions beyond `(none) → PROVISIONED`; executor relationships beyond the disclosed v1 direct-execution choice (`ROD-C040-Blocker-Closure-Assessment.md §3` item 8); CBOR registration (§34); future Organization-scoped provisioning. All remain exactly where Part I/Part II left them — future, disclosed scope, not reopened, not silently absorbed, not newly gated.

## 36. Final Decision

### 🟢 GREEN — IMPLEMENTATION READY

**Scope:** the chartered minimum-scope candidate BA — Tenant Establishment (Business Approval → Infrastructure Allocation) — only. This classification does not extend to, and is not evidence for, readiness of migration, offboarding, cross-tenant sharing, or Technical Provisioning.

**What remains as disclosed/future scope but does NOT prevent GREEN:**

| Item | Classification | Why it does not block GREEN |
|---|---|---|
| `AI-001` runtime holder population | Data/environment readiness | §32 — blocks production execution only, not implementation-readiness classification |
| `AI-002` accountability-point population (`TD-157`) | Data/environment readiness, disclosed Technical Debt | §32/§33 — same; explicitly not reopened, no action authorized here |
| CBOR registration (registering ADR) | Disclosed future implementation action | `TDS-016 §13`'s own already-established, non-blocking treatment |
| Formal BA/WP chartering | Administrative | Not a readiness question — a subsequent Repository Owner act |
| Independent Certification / V&V Audit / Release Readiness Audit (`CLAUDE.md §19.7`/`§19.7b`) | Downstream Work Package closure gate | Governs closing a chartered WP, not commissioning or classifying an IRA |
| Frontend / Enterprise Experience / Vertical Slice (`CLAUDE.md §20.3`/`§20.7`) | Downstream Work Package closure gate | Same — applies once a WP is chartered; no WP exists yet for this scope |
| Technical Provisioning, migration, offboarding, cross-tenant sharing | Future, explicitly out-of-scope capability | Never part of the chartered minimum BA (§35) |
| `PE-001-C040` document synchronization debt (Part I §14) | Non-blocking document-maintenance item | Unaffected by implementation, unchanged since Part I |

**Why GREEN, not AMBER:** Part II's own two stated reasons for AMBER were (1) the implementation not yet existing, and (2) `AI-002` blocking end-to-end execution. Reason (1) is now fully resolved and independently verified (§31). Reason (2), examined rigorously and in isolation for the first time this pass (§32) rather than carried forward bundled with reason (1), does not itself meet the bar Part I's own RED and Part II's own AMBER were actually gated on — an open constitutional, architectural, or governance question. None remains for this chartered scope.

**Why GREEN, not RED:** not applicable at this stage of the assessment — RED was already superseded by Part II's own AMBER finding and nothing in this Part reopens any of Part I's four original governance gaps.

## Change Control — Part III Amendment

**Files modified this pass:** this document only (`IRA-C040_...md`) — Part III (§29–36) appended; Parts I and II preserved verbatim, unmodified.
**Files created:** none. **Files deleted:** none.
**Not modified, per explicit instruction:** any ADR; `AI-001`/`AI-002`/`AI-003`; no `AI-004` created; `TECH-DEBT.md`/`TD-157`; the Delivery Map; `TDS-016`; `TDS-017`; `CBOR-INDEX.md`; any application code, schema, or migration; any runtime authority record; no Person/Identity fabrication.
**Not performed:** no Key-2 case; no AI-002 evidence search; no implementation work of any kind.
**Regression evidence:** full `AuthService` test suite re-run fresh, independently, this pass — 823 passed, 0 failed.
**Commit/push:** none — not authorized for this task.
