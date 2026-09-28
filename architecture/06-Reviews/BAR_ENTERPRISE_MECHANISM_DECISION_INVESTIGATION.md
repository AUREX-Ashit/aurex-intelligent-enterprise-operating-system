# BAR Enterprise Mechanism Decision Investigation

**Document type:** Enterprise governance investigation / Repository Owner decision preparation. Same class as `IRA-C024_CBOR_Eligibility.md` and the ROD-preparation artifacts in this repository — presents evidence and options; **selects nothing**.

**Prepared:** 2026-09-19, per direct Repository Owner instruction, following C-024 BA-01's own D10 (BAR treatment deferred, `ROD-C024-BAR_Treatment_Decision_Preparation.md §0`).

**Scope:** Enterprise-wide. Not limited to C-024. This investigation does not reopen, alter, or reinterpret D10, or any prior C-021/C-022/C-024 BAR disposition — each is examined only as evidence of precedent.

**Classification key:** `[LOCKED]` — verbatim constitutional text (SD-002, COM-001, CMD-001, RTA-001, PLT-001, GRC-001, OPM-001, ONT-001 — all Status: LOCKED). `[ACTIVE]` — verbatim from a Status: Active document (IMP-001). `[FACT]` — directly verified repository fact (file exists / does not exist, code inspected). `[PRECEDENT]` — a prior Repository Owner decision or ADR, cited for procedure/comparison only, never as enterprise policy. `[INFERENCE]` — a conclusion drawn from combining sources, explicitly flagged as such. `[OBSERVATION]` — a descriptive note, not a requirement. `[RO DECISION REQUIRED]` — an open question this investigation identifies as requiring Repository Owner resolution.

---

## 1. Executive Summary

AUREX's constitutional architecture (`SD-002-004`, `SD-002-034`, `COM-001-005`/`-060`, and identical "Registration Precedes Implementation"/"BAR Integration" clauses independently repeated in `PLT-001`, `GRC-001`, and cross-referenced in `OPM-001`/`ONT-001`) establishes a **genuine, LOCKED, enterprise-wide obligation**: every Business Activity satisfying `SD-002-034` is to be catalogued in a Business Activity Registry (BAR), and no commercial Business Activity is to be **executed** until so registered. This obligation is **not** commercial-specific (`COM-001-060`'s own scope) — `PLT-001-030` and `GRC-001-070` impose the identical obligation on platform and governance-domain Business Activities respectively, and `OPM-001-050`/`-083` treat BAR as a universal, cross-domain mechanism.

**No BAR mechanism exists anywhere in this repository** — no registry file, no database table, no identifier ever assigned, no runtime lookup, no validation, no `Business Activity Engine`. This is not a documentation gap: two independent source files (`Backend/Services/AIService/schemas/conversation.py:37`, `Backend/Runtime/AuthorizationEngine/authorization/models.py:51`) explicitly disclose, in code comments, that "no Business Activity Engine integration exists... yet." IMP-001 §6.22 and RTA-001 §3.6/§6/§11 describe a large, detailed target runtime architecture (registry + engine + manifest + execution policy + monitoring) that has never been built, in whole or in part, for any capability.

**Every Business Activity implemented in this repository to date — including at least nine Work Packages formally `CLOSED — CERTIFIED — RELEASE-READY` (WP-01 through WP-19, selectively) — has been certified, closed, and (in several cases) executed in production-shaped form with zero BAR registration and zero Business Activity Identifier.** This is not a C-024-specific or even a commercial-capability-specific condition. Only three Work Packages (WP-20/C-021, WP-21/C-022, WP-22/C-024) have ever explicitly raised the BAR question at all; in every one of those three, the Repository Owner's own decision was to defer, and none was blocked or delayed by that deferral at any subsequent gate.

**C-024 BA-01's own D10 (BAR deferred) is unaffected by this investigation and creates no conflict with any LOCKED requirement found here** — see §11. No hard blocker was discovered. This investigation makes no substantive recommendation and selects no option; it prepares the enterprise-level decision set for the Repository Owner (§14).

---

## 2. Investigation Objective

Determine whether AUREX requires a canonical enterprise Business Activity Registry (BAR) mechanism and governance model, and — if so — what the Repository Owner must decide before future Business Activities are implemented. This is broader than C-024: C-024's own D10 decision governs only C-024 BA-01 and does not resolve, and was never claimed to resolve, this enterprise question (`ROD-C024-BAR_Treatment_Decision_Preparation.md §0`, explicit non-transferability statement, re-verified §11 below).

---

## 3. Current Authoritative Governance State (as of 2026-09-19)

C-024 Billing Management: D1–D6 recorded/validated; D7 IRA accepted; D8 TDS preparation authorized; TDS-C024 prepared, independently reviewed (`IRA-TDS-C024_Independent_Review.md`, PASS WITH CONDITIONS), remediation complete; D9 accepted (`ROD-C024-D9_Lifecycle_Decision_Preparation.md §0`, Option A, collapsed lifecycle, BA-01 only); Charter prepared (`WP-22_C024_BA-01_Establish_Billing_Arrangement_Charter.md`); WP-22 registered (`WPR-001`); CBOR eligibility ELIGIBLE (`IRA-C024_CBOR_Eligibility.md`); CBOR registration COMPLETE, identifier `BIA-000001` (`ADR-041`); D10 accepted (`ROD-C024-BAR_Treatment_Decision_Preparation.md §0`, Option A — BAR treatment deferred for C-024 BA-01, not registered, no BAR identifier, no enterprise exemption created); implementation NOT STARTED.

**D10 is a C-024 BA-01 decision only.** It does not establish a repository-wide BAR exemption and does not resolve the enterprise BAR architecture/governance question this document investigates.

---

## 4. Source Inventory

Read directly for this investigation (not from summary):

- `SD-002_Universal_Business_Object_Rules.md` — `SD-002-004` (Universal Identity), `SD-002-034`/`-035` (Business Activities Rules). **Status: LOCKED.**
- `COM-001_Commercial_and_Subscription_Architecture.md` — `COM-001-001`/`-005`, `COM-001-060`/`-061`. **Status: LOCKED — Certified, CR-3.0.**
- `CMD-001_Canonical_Data_Model.md` — `§26.3`/`§26.3a`/`§26.4`/`§26.4a`/`§26.4b` (CBOR, cited for the CBOR/BAR distinction). **Status: LOCKED.**
- `PLT-001_Enterprise_Platform_Architecture.md` — `PLT-001-004`, `PLT-001-030`/`-031`. **Status: LOCKED** (confirmed among "all locked or current" companion set; own text uses identical "Registration Precedes Implementation"/"BAR Integration" formula to COM-001).
- `GRC-001_Governance_Risk_and_Compliance_Architecture.md` — `GRC-001-008`, `GRC-001-070`/`-071`. **Status: LOCKED** (same formula).
- `OPM-001_Enterprise_Operating_Model_Architecture.md` — `OPM-001-004`, `OPM-001-013`, `OPM-001-050`, `OPM-001-083`. **Status: LOCKED** — explicitly frames BAR as a universal coordination point, not a domain-specific rule ("OPM-001 adds no registration obligation beyond what SD-002-004/034/035 already establish").
- `ONT-001_Enterprise_Ontology_Architecture.md` — `ONT-001-051` (No BAR/CBOR Impact — disclaims any BA/BO of its own) and `ONT-001 §2` (Domain Ownership & Explicit Boundaries — confirms BAR/CBOR are "the registries of instances," owned by IMP-001/CMD-001 respectively).
- `RTA-001 - Runtime Architecture and Execution.md` — §3.6 (Business Activity Registry), §6 (Business Activity Runtime), §11 (Runtime Component inventory), §1.2/§1.4 (Runtime Philosophy/Scope). **Status: LOCKED** (corrected from an original "Draft" mislabel per `CERT-010`).
- `IMP-001_Implementation_Playbook.md` — §6.7 (BAC), §6.7a, §6.8–§6.13, §6.14 (CBAM), §6.22 (BAR, all subsections 6.22.1–6.22.15), §6.23 (Versioning), §6.29 (CBAM v2), §12049/§12059/§12129/§12133/§12139/§12251 (registry-specialization pattern). **Status: Active** — "governs current engineering practice; evolves via Controlled Evolution (`ARCH-000 §12.6`)," i.e. governed but not frozen, distinct from the LOCKED constitutional layer above.
- `CAP-001_Enterprise_Capability_Registry.md` — searched for BAR/Business Activity Registry references. **Zero hits.** CAP-001 does not mention BAR at all.
- `CLAUDE.md` (current, checked into this repository) — searched in full for `BAR`/`Business Activity Registry`. **Zero hits.** CLAUDE.md's own §19.7/§19.7b/§20/§21 govern Business Activity **completion gates** (Certification, V&V, Release Readiness) but never mention BAR by name.
- `WPR-001_Work_Package_Roadmap.md` — full WP-00 through WP-22 inventory (§3 table). No "BA Identifier" or "BAR" column exists in this register's own structure.
- `CBOR-INDEX.md` — confirmed this indexes Business **Objects**, not Business Activities (§1: "this Index registers Business Objects, not Business Activities"). Ten registered entries; none is a Business Activity.
- `architecture/00-Governance/AUREX_Master_Capability_Feature_Register.xlsx`, sheet `4_Business_Activity_Register` — 12 data rows. Column headers: `Capability, Domain, WP, BA, BA Name, Business Function, Authorization, Implementation, Testing, Gate 1–5, Certification, Release, Dependencies, Evidence, Last Updated, Notes`. **No "BA Identifier" or "BAR" column exists.** The `BA` column holds informal, per-charter ordinal labels (`BA-01`, `BA-01..08`), not `PREFIX-NNNNNN` Business Activity Identifiers.
- `ADR-037` (Offering Definition CBOR registration, C-021/WP-20) §Decision item 5 and its 2026-09-13 Correction note.
- `ADR-040` (Commercial Account CBOR registration, C-022/WP-21) §Decision item 5.
- `ADR-039` (Commercial Account CBOR preparation, C-022) — identifier-timing precedent only.
- `ADR-041` (Billing Arrangement CBOR registration, C-024/WP-22) §Decision item 5.
- `ROD-C022-B_Lifecycle_and_BAR_Decisions.md` — D10 (C-022's own BAR disposition, Option A, deferred).
- `ROD-C024-BAR_Treatment_Decision_Preparation.md` — full document, §0 decision record.
- `ADR-015` (Access Evaluation Outcome, C-002/WP-05) and `ADR-019` (Configuration Entry, C-041/WP-10) — searched for BAR references. **Zero hits in either** — BAR was never raised as a question for WP-05 or WP-10.
- Repository-wide grep for `BAR`, `Business Activity Registry`, `Business Activity Identifier`, `BAR registration`, `BAR mechanism`, `execution-time BAR`, `activity registry`, `activity identity`, `BAR validation`, `BA-0000NN`, `BAR-INDEX`/`BAR_INDEX`/`Business_Activity_Registry` (as filenames), `CBAM` (as filenames), `BusinessActivityEngine`/`business_activity_registry` (as code identifiers) — performed across `architecture/`, `Backend/`, `source/`.

---

## 5. BAR Requirement Extraction (Part A)

| Requirement | Exact source | What it requires | Scope | Lifecycle point | Current repository treatment |
|---|---|---|---|---|---|
| Universal Identity extends to Business Activities | `SD-002-004` `[LOCKED]` | Every business object (explicitly including BAs, example `BA-000089`) possesses a globally unique, permanent `PREFIX-NNNNNN` identity | Universal — all Business Activities, all domains | Identity assignment (timing not stated here) | **Not satisfied anywhere.** `BA-000089` appears only as an illustrative example in three constitutional files; zero actual `BA-NNNNNN` identifiers exist in this repository. |
| Every BA is catalogued in BAR | `SD-002-034` formalization note `[LOCKED]` | "Every Activity satisfying `SD-002-034` is catalogued in the Business Activity Registry — BAR, `IMP-001 §6.22`" | Universal — every Business Activity, not commercial-specific | Cataloguing (timing not stated here; see `COM-001-005` for the commercial-domain timing rule) | **Not satisfied.** No BAR exists to catalogue anything into. |
| Registration precedes implementation (Objects) / execution (Activities) — commercial domain | `COM-001-005` `[LOCKED]` | "No persistent commercial Business Object shall be **implemented** until registered in the CBOR. No commercial Business Activity shall be **executed** until registered in the BAR." | C-020–C-025 (COM-001 Sections 5–9) | CBOR: before implementation. BAR: before **execution**, a later gate than implementation | CBOR: satisfied for C-021 (`OFR-000001`), C-022 (`CAC-000001`), C-024 (`BIA-000001`). BAR: not satisfied for any — but none of C-021/C-022/C-024 has been executed yet either (none is implemented), so the execution-gate has not yet been triggered for any of them. |
| BAR Integration — commercial domain | `COM-001-060` `[LOCKED]` | Every commercial action (establish, change, renew, terminate, etc., Sections 5–9) is a Business Activity per `SD-002 §5`, registered in BAR **once implemented** | C-020–C-025 | Once implemented (i.e., an obligation that matures at implementation, discharged before execution per `COM-001-005`) | Not satisfied for any C-020–C-025 Business Activity; none has reached "implemented" status that would trigger this clause except arguably none — C-021/C-022/C-024 are all still pre-implementation. |
| Registration precedes implementation/execution — platform domain | `PLT-001-004` `[LOCKED]` | Identical formula to `COM-001-005`, applied to platform Business Objects/Activities | Enterprise Integration / Data Exchange domain | Same two-gate structure | Not applicable to any currently implemented capability in this repository (no PLT-001 Business Activity yet implemented, per this investigation's search). |
| BAR Integration — platform domain | `PLT-001-030` `[LOCKED]` | Every platform action (propose/authorize/suspend/retire an Integration; request/authorize/execute/complete an Exchange) is a Business Activity, registered in BAR once implemented | Platform Integration/Exchange domain | Once implemented | Not applicable — no such capability yet implemented. |
| Registration precedes implementation/execution — governance domain | `GRC-001-008` `[LOCKED]` | Identical formula, applied to governance Business Objects/Activities | KPI/Risk/Compliance/Policy/Disclosure domain | Same two-gate structure | Not applicable — no such capability yet implemented in this repository per this search. |
| BAR Integration — governance domain | `GRC-001-070` `[LOCKED]` | Every governance action is a Business Activity, registered in BAR once implemented | Same domain | Once implemented | Not applicable. |
| BAR is universal, not domain-specific | `OPM-001-013`, `OPM-001-050` `[LOCKED]` | "Every domain document's own constructs remain individually responsible for their own BAR/CBOR registration... OPM-001 adds no registration obligation beyond what `SD-002-004/034/035` already establish." A Business Activity's flow is "catalogued in the BAR (`IMP-001 §6.22`)" — stated as a cross-cutting coordination fact, not a new rule | All domains | N/A (coordination statement) | Confirms the obligation's cross-domain reach; does not itself create or discharge any obligation. |
| BAR/CBOR relationship to Ontology | `ONT-001 §2` `[LOCKED]` | BAR and CBOR are "the registries of instances (`IMP-001 §6.22`, `CMD-001 §26`)" | N/A — definitional cross-reference | N/A | Confirms BAR and CBOR are two distinct registries, neither a subset of the other. |
| BAR purpose/architecture (engineering layer) | `IMP-001 §6.22.1`–`§6.22.15` `[ACTIVE]` | Full registry specification: identity, classification, ownership, execution policy, security, workflow, events, AI configuration, runtime mapping (11 attribute categories, `§6.22.6`); registration validation (`§6.22.7`); discovery exclusively through the registry (`§6.22.8`); explicit status lifecycle Draft→Registered→Active→Suspended→Deprecated→Retired (`§6.22.9`); version management (`§6.22.10`); dependency management (`§6.22.11`); governance workflow (`§6.22.12`); observability (`§6.22.13`) | Universal — "all Business Activities within the Aurex Intelligent Operating Center" | Registration before execution (`§6.22.7`: "shall not be executable until successfully registered") | **Entirely unbuilt.** This is a target engineering design, not a currently-binding minimum — see §9 (IMP-001 distinction analysis) for why this is a materially larger scope than the LOCKED minimum above. |
| BAR as one node of the Runtime Execution Architecture | `RTA-001 §3.6`, §6, §11 `[LOCKED]` | "Every executable business operation within the Aurex Intelligent Operating Center shall execute through the Business Activity Runtime" (a Business Activity Engine + BAR + CBAM collaboration) | Universal — all runtime execution | Execution time | **Entirely unbuilt, LOCKED text notwithstanding.** No Business Activity in this repository executes through any such runtime; a dedicated Work Package (`WP-RTA-001`, status per `WPR-001`: scoped narrowly to the Authorization Engine, `RTA-001 §3.8`/`§11`) indicates RTA-001 is understood, in actual repository practice, as an incrementally-realized target architecture, not a precondition already met or immediately required for every Business Activity's own certification. |
| CBAM defines "what," BAR defines "how the platform manages it" | `IMP-001 §6.22.14` `[ACTIVE]`, `RTA-001 §6.6` `[LOCKED]` | Distinguishes the design-time contract (BAC/CBAM) from the runtime registry (BAR) | Universal | N/A — definitional | Neither BAC nor CBAM exists as a physical artifact for any Business Activity either (see §10). |

**On `COM-001-005` vs `COM-001-060` specifically:** these establish **two distinct obligations at two distinct lifecycle points**, not one restated twice. `COM-001-005` is the **prerequisite/gate rule** — it fixes *when* registration must occur relative to implementation (CBOR) and execution (BAR). `COM-001-060` is the **classification rule** — it establishes *which* actions are Business Activities subject to that gate at all (every Section 5–9 commercial action), and states the obligation matures "once implemented." Read together: CBOR must be satisfied **before implementation begins**; BAR must be satisfied **before execution occurs**, a later point than implementation completion. This is the same asymmetry `COM-001-005`'s own verbatim text already draws (`[LOCKED]`, re-confirmed directly from source for this investigation, not carried forward from any prior session's summary).

---

## 6. Current BAR Repository-State Inventory (Part B)

| Item | Status | Evidence |
|---|---|---|
| 1. BAR registry/index | **ABSENT** | Repository-wide search for `BAR-INDEX`, `BAR_INDEX`, `Business_Activity_Registry` (as a filename) returns nothing. `CBOR-INDEX.md §1` itself confirms it "registers Business Objects, not Business Activities." |
| 2. Business Activity identifier namespace | **ABSENT** | `BA-000089` appears only as an illustrative example in `CMD-001 §26.4a`, `IMP-001 §6.22.1b`, `SD-002-004` — three constitutional citations, zero actual assignments. No `BA-NNNNNN` token appears anywhere else in the repository. |
| 3. Business Activity registration artifacts | **ABSENT** | No ADR, RO decision, or file registers a Business Activity anywhere (contrast: ten CBOR registrations exist for Business Objects). |
| 4. Runtime registration lookup | **ABSENT** | No `Business Activity Engine`, no discovery-by-registry code. Confirmed by explicit code-comment disclosure at `Backend/Services/AIService/schemas/conversation.py:37` ("no Business Activity Engine integration exists in AIService yet") and `Backend/Runtime/AuthorizationEngine/authorization/models.py:51` ("Business Activity Engine (never by this engine itself)"). |
| 5. BAR validation | **ABSENT** | No registration-validation code exists; `IMP-001 §6.22.7`'s validation list (Contract/Manifest/Version/Dependency/Authorization/Event/Workflow) has no implementation. |
| 6. BAR-to-capability linkage | **ABSENT** | No linkage mechanism exists; nothing to link. |
| 7. BAR-to-WP linkage | **ABSENT** | `WPR-001`'s own table structure (`WP \| Capability \| Capability Name \| Status \| Governing IRA \| Certification`) has no BAR column. |
| 8. BAR-to-Charter linkage | **ABSENT** | Charters (`WP-20`/`21`/`22`) each *narrate* BAR as an outstanding prerequisite in prose (§24/§26 of the respective Charter) — a documentation reference, not a linkage mechanism. |
| 9. BAR-to-CBOR linkage | **ABSENT** | `ONT-001-051` confirms these are two independent registries by design; no cross-registry field exists in `CBOR-INDEX.md`'s own table structure, and none should be expected to, per that same design separation. |
| 10. BAR-to-authorization linkage | **ABSENT** | `IMP-001 §6.22.3`/`§6.22.6` describe an "Authorization Resolution" registry function; no implementation exists. Actual authorization in every implemented BA (`require_platform_admin` and peers) is a direct FastAPI dependency, not registry-resolved. |
| 11. BAR-to-execution/audit linkage | **ABSENT** | No such linkage exists; audit (`record_audit`/`publish_event`) in every implemented BA is direct, not registry-mediated. |
| 12. BAR lifecycle/status model | **ABSENT (specified, not built)** | `IMP-001 §6.22.9` fully specifies a Draft/Registered/Active/Suspended/Deprecated/Retired model. Zero Business Activities carry any such status field anywhere in this repository. |
| 13. BAR versioning | **ABSENT (specified, not built)** | `IMP-001 §6.22.10`/`§6.23` fully specify version management. Not implemented. |
| 14. BAR uniqueness enforcement | **ABSENT** | No identifier exists to enforce uniqueness over. |
| 15. BAR governance workflow | **ABSENT (specified, not built)** | `IMP-001 §6.22.12` specifies Registration Approval/Activation/Suspension/etc. as governed Business Activities in their own right. Not implemented. |

**No item classifies as FOUND, PARTIAL, or STUB/PLACEHOLDER.** Every item is **ABSENT** — a documentation-only specification with zero physical realization, confirmed independently at the code level (not merely inferred from the absence of a governance artifact).

---

## 7. Business Activity Inventory (Part C)

Built from `WPR-001` §3 and `AUREX_Master_Capability_Feature_Register.xlsx` sheet `4_Business_Activity_Register` (12 rows) plus direct WP-16–22 text. No identifier is invented for any row lacking one.

| Capability | WP | BA | BA Identifier | Charter | Implementation state | Certification | BAR state | Evidence |
|---|---|---|---|---|---|---|---|---|
| C-004 (Organization Mgmt) | WP-01 | BA-01..08 (informal) | **None** | Predates formal Charter convention | IMPLEMENTED (BA-01 corrected per `IRA-001A`) | CLOSED — CERTIFIED | Not raised/not registered | `IMP-REPORT-WP-01` |
| C-003 (Role & Permission) | WP-02, WP-06, WP-18 | Various (informal) | **None** | Charter for WP-18 only | IMPLEMENTED (WP-18: runtime binding) | CLOSED — CERTIFIED (WP-18: — RELEASE-READY) | Not raised/not registered | `IMP-REPORT-WP-18`, `CERT-WP-18`, `RRA-WP-18` |
| C-007 (Membership Mgmt) | WP-03 | BA-01,02,03,06–11 (9 of 11) | **None** | Predates formal Charter convention | PARTIAL (BA-04 BLOCKED, external dependency) | CERTIFIED (partial) | Not raised/not registered | `IMP-REPORT-WP-03` |
| C-005 (Enterprise Structure) | WP-04 | BA-01..09 (informal) | **None** (6 Business **Objects** registered: `SCI/POC/IMC/RVC/VLC/RSC`-000001 — not BAs) | Predates formal Charter convention | IMPLEMENTED (9/9) | CLOSED — CERTIFIED | Not raised/not registered | `IMP-REPORT-WP-04`; `ADR-006/008/009/011/012/013` (CBOR only) |
| C-002 (Access Mgmt) | WP-05 | BA-01..06 (informal) | **None** (1 Business Object registered: `AEO-000001`) | Predates formal Charter convention | IMPLEMENTED (Minimum Scope/Option A) | CLOSED — CERTIFIED | Not raised/not registered (`ADR-015` — zero BAR mentions) | `IMP-REPORT-WP-05`; `ADR-015` |
| C-006 | WP-07 | (informal) | **None** | Predates formal Charter convention | IMPLEMENTED | CLOSED — CERTIFIED | Not raised/not registered | `WPR-001` WP-07 row |
| C-001 | WP-08 | (informal) | **None** | Predates formal Charter convention | IMPLEMENTED | CLOSED — CERTIFIED | Not raised/not registered | `WPR-001` WP-08 row |
| C-008 | WP-09 | (informal) | **None** | Predates formal Charter convention | IMPLEMENTED | CLOSED — CERTIFIED | Not raised/not registered | `WPR-001` WP-09 row |
| C-041 (Configuration Mgmt) | WP-10 | (informal) | **None** (1 Business Object registered: `CFG-000001`) | Predates formal Charter convention | IMPLEMENTED | CLOSED — CERTIFIED | Not raised/not registered (`ADR-019` — zero BAR mentions) | `IMP-REPORT-WP-10`; `ADR-019` |
| C-093 (Enterprise Search) | WP-11 | BA-01/02/03 | **None** | Predates formal Charter convention | IMPLEMENTED — PARTIAL (stub backing) | CLOSED — CERTIFIED | Not raised/not registered | `IMP-REPORT-WP-11` |
| C-094 (AI Conversation Mgmt) | WP-12 | BA-01/02/03 | **None** | Predates formal Charter convention | IMPLEMENTED — PARTIAL (stub backing) | CLOSED — CERTIFIED WITH FINDINGS | Not raised/not registered | `IMP-REPORT-WP-12` |
| — (Runtime) | WP-13 | N/A | **None** | N/A | IN PROGRESS | Not certified | Not raised/not registered | `WPR-001` WP-13 row |
| C-090/091/092 (Enterprise Intelligence Foundation) | WP-14 | BA-01..05 | **None** | Predates formal Charter convention | IMPLEMENTED | CLOSED — CERTIFIED | Not raised/not registered | `IMP-REPORT-WP-14` |
| C-066 (Evidence Mgmt) | WP-15 | BA-01 | **None** | Predates formal Charter convention | IMPLEMENTED | CLOSED — CERTIFIED | Not raised/not registered | `IMP-REPORT-WP-15` |
| C-040 (Tenant Administration) | WP-16 | BA-01 | **None** | `WP-16` Charter | IMPLEMENTATION COMPLETE | CLOSED — CERTIFIED | Not raised/not registered (not a COM-001 construct) | `IMP-REPORT-WP-16`; `CERT-WP-16`; `RRA-WP-16` |
| C-023 (Licensing & Entitlement) | WP-17 | BA-01 | **None** | `WP-17` Charter | IMPLEMENTED (per R9 governance-reconciliation) | Gate 1 PASSED (per R9); full 5-gate closure text not independently re-verified by this investigation beyond the R9 note | Not raised/not registered (not a COM-001 construct) | `WPR-001` WP-17 row |
| C-003 (Approval Authority runtime binding) | WP-18 | (repository-wide infra, backend-only) | **None** | `WP-18` Charter | IMPLEMENTATION COMPLETE | CLOSED — CERTIFIED — RELEASE-READY | Not raised/not registered | `IMP-REPORT-WP-18`; `CERT-WP-18`; `VV-AUDIT-WP-18`; `RRA-WP-18` |
| C-132 (Enterprise Notifications) | WP-19 | BA-01 | **None** | `WP-19` Charter | IMPLEMENTATION COMPLETE | FORMALLY CLOSED — CERTIFIED — RELEASE-READY | Not raised/not registered (not a COM-001 construct; C-132 is D-007) | `WPR-001` WP-19 row |
| C-021 (Product & Service Catalog) | WP-20 | BA-01 | **None** | `WP-20` Charter | IMPLEMENTATION AUTHORIZED / CLOSED — CERTIFIED — RELEASE-READY (per `WPR-001`) | CLOSED — CERTIFIED — RELEASE-READY | **Explicitly raised and deferred** — RO decision 2026-09-08, no BAR mechanism created (`ADR-037 §Decision item 5`) | `ADR-037`; `IMP-REPORT-WP-20 §3.1` |
| C-022 (Customer & Account Mgmt) | WP-21 | BA-01 | **None** | `WP-21` Charter | IMPLEMENTATION COMPLETE | CLOSED — CERTIFIED — RELEASE-READY | **Explicitly raised and deferred** — `ROD-C022-B` D10, Option A (`ADR-040 §Decision item 5`) | `ADR-040`; `ROD-C022-B` |
| C-024 (Billing Management) | WP-22 | BA-01 | **None** | `WP-22` Charter | NOT STARTED | Not certified | **Explicitly raised and deferred** — `ROD-C024-BAR_Treatment_Decision_Preparation.md §0`, D10, Option A | `ROD-C024-BAR...md` |

**Findings:**
- **Zero Business Activities, across every Work Package in this repository's history, carry a `BA-NNNNNN` Business Activity Identifier.** The `BA` column in every register (`WPR-001`, `4_Business_Activity_Register`) holds an informal, per-Charter ordinal label (e.g. "BA-01"), never the `SD-002-004` Universal Identity form.
- **Zero Business Activities carry a BAR registration.**
- **The BAR question was explicitly raised, analyzed, and deferred for exactly three Work Packages — WP-20/C-021, WP-21/C-022, WP-22/C-024 — and was never raised at all for any of the other nineteen.** This is not because those nineteen are exempt under any located LOCKED text; `SD-002-034`'s formalization note and `OPM-001-013` both state the cataloguing obligation is universal, not commercial-domain-specific. The three-WP pattern coincides exactly with the three Work Packages whose owning capabilities happen to fall under `COM-001` Sections 5–9, where `COM-001-060` gave the obligation a concrete, capability-specific citation to discover during CBOR-registration investigation. `[INFERENCE]` The other nineteen Work Packages' own BAR obligation under `SD-002-034`/`PLT-001-030`/`GRC-001-070` (whichever applies to each) appears to have gone **undiscovered**, not **satisfied** or **exempted** — no artifact anywhere disclaims or resolves it for those nineteen.

---

## 8. IMP-001 Distinction Analysis (Part D)

**What IMP-001 already requires for a Business Activity, independent of BAR:**
- `§6.7` **Business Activity Contract (BAC)** — a design-time specification (Activity Identifier, Domain, Object, Type, Intent, Input/Output Contract, Pre/Postconditions, Authorization, Events, Workflow, Audit, AI Assistance, Definition of Done, Idempotency). In current practice, every Charter (`WP-16` through `WP-22`) narrates the substance of a BAC in prose, without using that name or a discrete machine-readable artifact.
- `§6.14`/`§6.29` **Canonical Business Activity Manifest (CBAM)** — a machine-readable version of the same information, stated to be "the implementation contract for Business Activities" that "Claude Code shall use." No physical CBAM file (of any format) exists anywhere in this repository for any Business Activity.
- `§6.8`–`§6.13` — granularity, workflow/event/authorization/AI integration principles, and testing requirements. These are satisfied in substance by every certified Work Package's own implementation (authorization via `require_platform_admin` and peers, events via `publish_event`, testing per `CLAUDE.md §11`/`§19.7b`), without any registry.

**What BAR (`§6.22`) adds beyond this:** a **runtime, queryable, centrally-owned metadata store** consumed by a **Business Activity Engine** that is stated to be the platform's *exclusive* discovery mechanism (`§6.22.8` "Activity Discovery": "The Business Activity Engine shall discover Business Activities exclusively through the Registry.") and *exclusive* execution gate (`§6.22.7`: "shall not be executable until successfully registered"). This is categorically different from a BAC/CBAM, which are design-time documents describing one Activity; BAR is described as live infrastructure spanning every Activity, with its own lifecycle-status enforcement (`§6.22.9`), version resolution (`§6.22.10`), dependency-impact analysis (`§6.22.11`), and governance workflow (`§6.22.12`).

**Is BAR "simply a registry of metadata IMP-001 already governs"?** `[FINDING]` **No, not simply.** IMP-001 §6.7/§6.14 already govern the *content* of what a BA is (the BAC/CBAM). BAR's own distinguishing addition is the **runtime enforcement layer** — the claim that no Activity may execute without passing through this registry, and that discovery/authorization/monitoring are centrally mediated by it rather than by each service's own code. That is an execution-time obligation IMP-001's design-time sections (§6.7–§6.14) do not, and structurally cannot, discharge on their own — a BAC/CBAM sitting in a repository is not itself a runtime gate.

**Is this a documentation registry, canonical identity source, runtime governance mechanism, execution control, or multiple layers?** `[FINDING]` As specified, BAR is described as **all of these at once** — canonical identity source (`§6.22.6` Identity block, tied to `SD-002-004`), documentation/metadata registry (`§6.22.5`/`§6.22.6` full attribute set), runtime execution control (`§6.22.7`/`§6.22.8`, gates executability and discovery), and governance mechanism (`§6.22.12`). The specification does not distinguish a minimal subset from the full set — it describes one integrated mechanism. **Ambiguity, disclosed rather than resolved:** whether the *LOCKED minimum* (`SD-002-004`/`-034`, `COM-001-005`/`-060` and their `PLT-001`/`GRC-001` counterparts — "catalogue every BA with an identity; gate commercial-domain execution on that catalogue entry") requires building the *entire* `IMP-001 §6.22` engineering design (Business Activity Engine, execution-policy resolution, AI configuration, monitoring) or could be satisfied by a materially smaller mechanism that still discharges the LOCKED text, is **not answered by any source examined**. `IMP-001` is Status: Active (evolvable via Controlled Evolution), not LOCKED — its own elaborated §6.22 design is engineering methodology, not frozen constitutional law, meaning a smaller LOCKED-compliant mechanism is not obviously foreclosed, but no source affirmatively states this either. This ambiguity is material to Part G's Option A scope and is carried there undecided.

---

## 9. Existing Precedent Analysis

Three precedents exist, all in this repository's `COM-001` commercial-capability line, all deferring: `ADR-037 §Decision item 5` (C-021/WP-20, RO decision 2026-09-08 — "do NOT create any BAR registry / `BAR-INDEX` / BAR file / database or runtime mechanism as part of WP-20... a future enterprise-level decision may establish the canonical BAR mechanism"); `ROD-C022-B D10` (C-022/WP-21, Option A, 2026-09-15, `ADR-040 §Decision item 5` executing it); `ROD-C024-BAR_Treatment_Decision_Preparation.md §0` (C-024/WP-22, D10, Option A, 2026-09-19). **Each decision is explicit that it does not create a repository-wide policy and does not bind any other capability** — `ROD-C022-B D10` and `ROD-C024-BAR §0` both state this in their own text, independently, not by cross-reference to each other. **This investigation does not treat any of the three as enterprise policy**, consistent with that self-limitation and with the governing instruction for this task. Their evidentiary value here is solely: (a) confirmation that the "no BAR mechanism exists" finding is stable across three separate investigations conducted at three different times (2026-09-08, -15, -19); (b) confirmation that deferral has, in fact, never blocked a subsequent gate — WP-20 and WP-21 both reached `CLOSED — CERTIFIED — RELEASE-READY` after their own BAR deferral, with no gate (Certification, V&V, Release Readiness) treating the undischarged BAR obligation as a release blocker.

---

## 10. Enterprise Impact Analysis (Part E)

| Process | Current state | BAR dependency | Consequence of no BAR mechanism | Blocking / Deferred / Advisory / Unknown |
|---|---|---|---|---|
| Business Activity creation | Ad hoc, per-Charter, no registry consulted | `SD-002-034` (cataloguing) | New BAs continue to be created without a central catalogue check for duplication/collision | **Deferred** — no source treats this as blocking creation |
| Chartering | Charter documents narrate BAC-equivalent content in prose; no CBAM artifact created | `IMP-001 §6.7`/`§6.14` (design-time, distinct from BAR) | None specific to BAR — Charters have proceeded without CBAM for every WP to date | **Advisory** (CBAM gap, not a BAR-specific consequence) |
| WP registration (`WPR-001`) | No BAR column; registration proceeds on Charter/IRA evidence alone | None found — `WPR-001`'s own structure never required a BAR field | None | **Not applicable** — `WPR-001` is source-of-truth-independent of BAR by its own design |
| Business Activity Identifier assignment | Never performed for any BA in this repository's history | `SD-002-004` | Every BA remains identified only by informal, per-Charter ordinal labels, not a globally unique, cross-capability-referenceable identity | **Deferred** (structurally unresolved, not yet treated as blocking any gate) |
| Implementation authorization | Granted per-WP by direct Repository Owner decision, independent of BAR | `COM-001-005` ties BAR to **execution**, not implementation | Implementation has proceeded for 19+ WPs without BAR; `COM-001-005`'s own text supports this — CBOR (not BAR) is the implementation-gate | **Not blocking** — source-confirmed (`COM-001-005`) |
| Execution-time activity invocation | Every certified BA is invoked directly via its own FastAPI route; no registry-mediated discovery | `COM-001-005` ("no commercial Business Activity shall be **executed** until registered in the BAR"); `IMP-001 §6.22.7`/`§6.22.8` | For C-020–C-025 constructs specifically, this is a **LOCKED, currently-undischarged execution-gate obligation** for any Business Activity that reaches actual execution (i.e., is called in a running system) — not yet triggered for C-021/C-022 (implemented but investigation did not confirm live execution beyond certification test-suite runs) or C-024 (not implemented). For the other nineteen WPs, this obligation traces instead to `SD-002-034`/`PLT-001-030`/`GRC-001-070` depending on domain, and — per §7's finding — was never raised, so its status there is **unknown**, not resolved. | **Blocking, by LOCKED text, once execution actually occurs** for C-020–C-025 constructs — but no source in this repository states that "execution" has yet occurred for any of them in a sense distinct from "implemented and certified." This is a genuinely unresolved reading, flagged, not resolved, here. |
| Audit/events | `record_audit`/`publish_event`, direct calls, no registry mediation | `IMP-001 §6.22.6` Events category (registry-tracked) | None observed — audit/events function correctly today without BAR | **Advisory** |
| Authorization | Direct FastAPI dependency injection (`require_platform_admin` and peers) | `IMP-001 §6.22.3`/`§6.22.6` (Authorization Resolution as a registry function) | None observed — authorization functions correctly today without BAR | **Advisory** |
| Traceability | Achieved today via Charter/ROD/IRA/TDS cross-references and the census artifacts, not via BAR | `IMP-001 §6.22.1` ("authoritative source for... discovery, execution, governance, monitoring") | Traceability exists today through a documentation-based mechanism, not BAR | **Advisory** — an alternative mechanism is already in active, working use |
| Reporting / assurance | Achieved via the census artifacts (`AUREX_ENTERPRISE_FEATURE_CAPABILITY_COVERAGE_MATRIX.md`, the XLSX register) | None found tying reporting specifically to BAR | None observed | **Advisory** |
| Capability dependency management | Achieved via each Charter's own Dependencies section (e.g. `WP-22 Charter §16`) | `IMP-001 §6.22.11` (Dependency Management as a registry function) | Dependency tracking exists today through Charter prose, not a queryable registry | **Advisory** |
| Cross-capability activity references | Achieved via direct citation in governing text (e.g. C-024's Bill-To reference to C-022's own produced Account Reference) | None found requiring BAR specifically for this | None observed | **Advisory** |
| Future agent execution / orchestration | `[FACT]` No authoritative source examined ties BAR to AI agent execution/orchestration specifically, beyond `IMP-001 §6.22.6`'s "AI" attribute category (AI Assistance Enabled / Human Review Required / Confidence Threshold / AI Policy) and `IMP-001 §6.12` (AI may assist but "shall not execute Business Activities autonomously unless explicitly permitted by governance") | `IMP-001 §6.22.6`, `§6.12` | If a future Business Activity is intended to be invoked by an AI agent/orchestrator, `§6.22`'s AI-configuration and human-review-gating fields would need a home; none currently exists outside the unbuilt BAR | **Unknown** — no source states this is currently blocking anything, since no such agent-invoked Business Activity exists yet in this repository |

---

## 11. C-024 D10 Position (Part F)

D10 (`ROD-C024-BAR_Treatment_Decision_Preparation.md §0`): BAR treatment for C-024 BA-01 is deferred — not registered, no BAR identifier assigned, no enterprise exemption created, decision scoped to C-024 BA-01 only.

**Effect of this investigation on D10: none.** Specifically:

- **Does this investigation change D10?** No. D10 remains exactly as recorded; this document does not edit, strike through, or supersede any part of `ROD-C024-BAR_Treatment_Decision_Preparation.md`.
- **Does it reveal a future dependency?** Yes, already disclosed by D10 itself (§0: "the `COM-001-060` execution-time obligation remains outstanding... deferred pending a future enterprise-level BAR-mechanism decision"). This investigation confirms, with a much wider evidentiary base (§5–§10 above), that the future dependency is real and enterprise-wide, not C-024-specific — it does not newly create the dependency.
- **Does it create a new enterprise-level governance requirement that may affect future C-024 implementation?** Not a *new* one — `COM-001-005`'s BAR clause already required this before this investigation began. What this investigation adds is **evidentiary breadth**: the obligation is confirmed to arise from `SD-002-034` (universal) and `COM-001-060` (commercial-specific) simultaneously for C-024, and from precedent (`ADR-037`, `ROD-C022-B`) that deferral has not historically blocked subsequent gates for structurally identical decisions.
- **Does it require any fresh RO decision specifically for C-024?** No. C-024's own decision is complete and internally coherent (see conflict-check below). Any future decision C-024 requires is the same one every other deferred capability requires: the enterprise-level Option A/B choice in §12 below, which is not C-024-specific.
- **Conflict check — does D10 coexist with every LOCKED requirement found in this investigation?** `[FINDING]` **Yes, no conflict found.** `COM-001-005`'s BAR clause gates **execution**, not implementation or Charter/decision-recording. C-024 BA-01 has not been implemented and has certainly not been executed. D10's own deferral is therefore not in tension with `COM-001-005` — it defers a decision about a gate (execution) that has not yet been reached. `COM-001-060`'s "once implemented" maturation clause has likewise not yet triggered, since C-024 is not implemented. **No STOP condition applies.** This finding was independently re-derived from `COM-001-005`/`COM-001-060`'s own verbatim text (§5 above) specifically to check for this conflict, not assumed from D10's own self-description.

---

## 12. Enterprise Decision Options (Part G)

**No option is selected below.**

### OPTION A — Establish a canonical enterprise BAR mechanism now

**Authoritative evidence:** `SD-002-004`/`-034`, `COM-001-005`/`-060`, `PLT-001-004`/`-030`, `GRC-001-008`/`-070`, `OPM-001-013`/`-050` (the LOCKED obligation this option would discharge); `IMP-001 §6.22` (the existing, if unbuilt, engineering design to draw from); `RTA-001 §3.6`/§6` (the LOCKED runtime-architecture context BAR sits within).

**Scope:** Could range, per §9's disclosed ambiguity, from (a) a minimal LOCKED-compliant catalogue (identifier + name + owning capability + status, mirroring `CBOR-INDEX.md`'s own adapted nine/ten-attribute table shape) to (b) the full `IMP-001 §6.22` Business Activity Engine (registry + runtime discovery + execution-policy resolution + AI configuration + monitoring). This investigation does not resolve which; that is itself part of what Option A would need to settle.

**What would be decided:** That AUREX establishes a BAR; its scope (minimal vs. full `§6.22` design); Business Activity Identifier assignment authority and timing; registration lifecycle/status model; ownership; relationship to `WPR-001`/CBOR/`IMP-001`.

**What would remain undecided:** Concrete engineering design and implementation timeline (this investigation is explicitly barred from design-in-detail); whether retroactive registration is required for the nineteen already-certified Work Packages found in §7 to have never raised the question, or only prospective from the decision date forward.

**Impact on existing BAs:** All 20+ already-certified/implemented Business Activities (§7) would face a retroactive-registration question the Repository Owner has not yet been asked. Depending on scope chosen, some or all could require identifier backfill.

**Impact on future BAs:** Every future Business Activity (including C-024 BA-01, once implementation is authorized) would need to satisfy whatever registration timing is decided before it may execute (`COM-001-005`), and — if `IMP-001 §6.22`'s full scope is adopted — before it may even be *discovered* by any Business Activity Engine (`§6.22.8`).

**Impact on implementation governance:** A new mandatory step would enter the `CLAUDE.md §21.3` Standard Work Package Lifecycle and/or the `CLAUDE.md §19.7b` gate sequence, requiring a `CLAUDE.md`/`IMP-001` cross-reference this investigation is not authorized to make.

**Impact on C-024:** BA-01 could proceed to implementation without further BAR-specific delay only if the new mechanism's registration timing is satisfied before execution, exactly as `COM-001-005` already requires; D10 would need no reopening either way, since D10 only deferred the *decision*, not a specific registration timeline.

**New artifacts required:** A `BAR-INDEX.md` (or equivalent) mirroring `CBOR-INDEX.md`'s own Amendment Procedure; a registering-ADR pattern for each Business Activity; potentially a `CLAUDE.md`/`IMP-001` amendment stating this is now mandatory (a constitutional-document change this investigation cannot make).

**Would an enterprise architecture/governance initiative be triggered?** Yes — `[FINDING]` given the retroactive-registration question for 20+ already-certified Work Packages and the design-scope ambiguity in §9, Option A as fully realized (`IMP-001 §6.22`'s complete design) would very likely require a dedicated Work Package or enterprise initiative of its own, comparable in scope to `WP-RTA-001`'s own narrower (Authorization Engine only) undertaking.

### OPTION B — Continue without an enterprise BAR mechanism; formally defer until a future enterprise governance initiative

**Authoritative evidence:** The unbroken precedent of §9 (three prior deferrals, zero subsequent gate blockage); `COM-001-005`'s own execution-gate (not implementation-gate) framing, which permits continued implementation/certification work while the execution-time obligation remains outstanding; the fact that 19 of 22 Work Packages have already, in effect, operated this way without any decision ever being recorded for them.

**Scope:** Formalizes, at enterprise level, what has so far happened by omission for nineteen Work Packages and by explicit case-by-case decision for three.

**What would be decided:** That AUREX does not establish an enterprise BAR mechanism at this time; that the `COM-001-005`/`COM-001-060` (and `PLT-001`/`GRC-001` counterparts) BAR obligation remains a disclosed, outstanding, unsatisfied constitutional obligation enterprise-wide, deferred to a named future initiative (or left unnamed, if the Repository Owner does not wish to commit to one yet).

**What would remain undecided:** The same design-scope question as Option A (deferred indefinitely rather than resolved); whether any future Business Activity approaching actual **execution** (as opposed to mere implementation/certification) would need case-by-case treatment before that specific gate, given `COM-001-005`'s own text.

**Impact on existing BAs:** None — no change to any already-certified Work Package's status.

**Impact on future BAs:** Each future commercial-domain (`COM-001` Sections 5–9) Business Activity would need its own case-by-case BAR-deferral decision before implementation/Charter conclusion, mirroring the `ADR-037`/`ROD-C022-B`/`ROD-C024-BAR` pattern, **unless** this option's own recording is drafted broadly enough to cover future cases without a fresh decision each time — a choice this investigation flags but does not resolve, since it borders on "does this option, itself, create the repository-wide policy §9's precedents each individually disclaimed creating." Non-commercial-domain Business Activities (the pattern found for 19 of 22 existing WPs) would continue to proceed without the question being raised at all, unless this option's own recording explicitly extends to them.

**Impact on implementation governance:** None — no new gate, no new artifact type, no `CLAUDE.md`/`IMP-001` change.

**Impact on C-024:** No change — D10 already reflects this option's own logic for C-024 BA-01 specifically.

**New artifacts required:** None beyond this investigation's own record of the decision, if made.

**Would an enterprise architecture/governance initiative be triggered?** Not immediately — the decision is explicitly to defer such an initiative. It could be reframed later as a planned, named future initiative without contradicting this option.

**No third, materially distinct alternative was found in the sources examined.** A middle path (e.g., "build only the minimal LOCKED-compliant catalogue now, defer the full `IMP-001 §6.22` engine") is not a separate option — it is Option A with its own scope question (§9's disclosed ambiguity) resolved toward the minimal end; it is noted here rather than manufactured as an "Option C" for symmetry.

---

## 13. Decision Implications (Part I)

- **Can future Business Activities be implemented without BAR?** `[Source-backed: yes]` — `COM-001-005` gates **execution**, not implementation, for commercial-domain Activities; CBOR (not BAR) is the implementation-gate. Non-commercial-domain Activities have never had this question raised (§7), so this remains **unknown** for them specifically, though eighteen have already been implemented without it being raised.
- **Can they be chartered without BAR?** `[Source-backed: yes]` — every Charter examined (WP-16 through WP-22) either narrates BAR as a future prerequisite (WP-20/21/22) or does not mention it at all (WP-16 through WP-19), and none was blocked at Charter stage.
- **Can they be registered in `WPR-001` without BAR?** `[Source-backed: yes]` — `WPR-001`'s own table structure carries no BAR field; every WP examined registered without one.
- **Is CBOR independent of BAR?** `[Source-backed: yes]` — `ONT-001-051` and `CBOR-INDEX.md §1` both confirm these are two separate registries (Business Objects vs. Business Activities); `COM-001-005` states two independent gates (implementation vs. execution) for two independent things.
- **Does BAR affect Business Activity identity?** `[Source-backed: yes]` — `SD-002-004`/`IMP-001 §6.22.1b` tie the Activity Identifier's assignment/cataloguing to BAR; absent BAR, no BA in this repository has ever received one (§7).
- **Does BAR affect execution-time governance?** `[Source-backed: yes, for commercial-domain Activities]` — `COM-001-005`'s own execution-gate is the direct mechanism; §10 above flags that whether any commercial Activity has yet reached "execution" in the sense this gate contemplates is itself unresolved.
- **Does BAR affect audit/assurance?** `[Unresolved / not source-confirmed as currently blocking]` — `IMP-001 §6.22.6` names Events/Audit as registry-tracked categories, but every implemented Activity's actual audit/event mechanism (`record_audit`/`publish_event`) functions today without registry mediation; no source states audit/assurance is degraded by BAR's absence.
- **Does BAR affect agent orchestration?** `[Unresolved]` — see §10's row on this; no authoritative source ties BAR to a currently-existing agent-orchestration mechanism, since none exists yet in this repository.

---

## 14. Required Repository Owner Decision(s) (Part H)

**Repository Owner Decision Required:**

1. **Does AUREX establish a canonical enterprise Business Activity Registry (BAR) mechanism now, or does it formally defer this to a future enterprise governance initiative?** (Option A vs. Option B, §12.)
2. **If established (Option A): what scope?** — a minimal LOCKED-compliant catalogue (identity, name, owning capability, status), or the full `IMP-001 §6.22` Business Activity Engine design (registry + runtime discovery + execution-policy resolution + AI configuration + monitoring)?
3. **If established: does registration apply retroactively to the twenty-plus already-certified/implemented Business Activities found in §7 to have never raised the question, or only prospectively from a stated future date?**
4. **If deferred (Option B): does the deferral apply enterprise-wide (covering the nineteen Work Packages that have never raised the question, as well as future non-commercial-domain Business Activities), or only to the specific capabilities that have already raised it case-by-case (C-021/C-022/C-024)?** — i.e., does this decision itself constitute the "repository-wide policy" that `ADR-037`/`ROD-C022-B`/`ROD-C024-BAR` each individually disclaimed creating, or does it leave that question open for the next capability to raise again?
5. **Business Activity Identifier authority:** if BAR is established, who assigns `BA-NNNNNN` identifiers, and at what governance point (mirroring the CBOR identifier-timing precedent already established — at registration, never earlier)?
6. **Relationship to `IMP-001`:** does establishing BAR require amending `IMP-001 §6.22` (an Active, evolvable document) to fix the minimal-vs-full scope ambiguity §9 disclosed, or is that left to a future engineering decision within whatever scope is chosen in Decision 2?
7. **Relationship to `WPR-001`:** does `WPR-001`'s own table structure gain a BAR-status column, or does BAR remain a separately-tracked register exactly as `CBOR-INDEX.md` is separate from `WPR-001` today?

Only decisions genuinely required by the evidence above are listed; no decision is manufactured for completeness.

---

## 15. Open Questions / Unresolved Governance

- Whether "execution" (`COM-001-005`'s BAR trigger) has a repository-recognized meaning distinct from "implemented and certified" — no source examined defines this boundary precisely (§10, §13).
- Whether the eighteen-Work-Package pattern of never raising the BAR question (§7) itself requires remediation, independent of whatever the Repository Owner decides about a future mechanism — this investigation surfaces the pattern but does not judge it, since judging it would exceed this task's decision-preparation-only scope.
- The minimal-vs-full `IMP-001 §6.22` scope ambiguity (§9), which Decision 2 above must resolve if Option A is ever selected.
- Whether a future enterprise BAR mechanism, once built, would also need to retroactively examine the non-`COM-001` domains (`PLT-001`, `GRC-001`) for their own not-yet-implemented Business Activities, or whether this investigation's commercial-domain-heavy evidence base under-represents those domains (none currently has an implemented Business Activity to test against, per this search).

---

## 16. Recommended Next Governed Stage

**Process recommendation only, not a substantive option recommendation:** A Repository Owner decision on the question in §14 Decision 1 (and, if Option A, Decisions 2–7) is required before any BAR mechanism design, implementation, or registration may proceed. No further investigation artifact is needed before that decision is made — the evidentiary record above is source-complete for the decisions listed.

---

## 17. Evidence Matrix

| Assertion | Source | File/Section | Evidence type |
|---|---|---|---|
| BAR obligation is universal, not commercial-only | `SD-002-034` formalization; `OPM-001-013` | `SD-002_Universal_Business_Object_Rules.md:229`; `OPM-001...md` §OPM-001-013 | `[LOCKED]` |
| CBOR gates implementation, BAR gates execution | `COM-001-005` | `COM-001...md:59-60` | `[LOCKED]`, verbatim |
| Identical BAR clause exists in Platform/Governance domains | `PLT-001-004`/`-030`; `GRC-001-008`/`-070` | Respective files | `[LOCKED]`, verbatim |
| No BAR mechanism exists in code | Code comments | `Backend/Services/AIService/schemas/conversation.py:37`; `Backend/Runtime/AuthorizationEngine/authorization/models.py:51` | `[FACT]`, direct code inspection |
| Zero `BA-NNNNNN` identifiers ever assigned | Repository-wide search | grep result, 3 files, all illustrative-only | `[FACT]` |
| BAR raised/deferred only for C-021/C-022/C-024 | `ADR-037`, `ROD-C022-B`, `ROD-C024-BAR` vs. absence in `ADR-015`/`ADR-019`/other WP artifacts | Cited files | `[FACT]` + `[PRECEDENT]` |
| WPR-001/CBOR-INDEX/4_Business_Activity_Register carry no BAR field | Direct structural inspection | `WPR-001` §3 header row; `CBOR-INDEX.md §3`; XLSX sheet headers | `[FACT]` |
| IMP-001 §6.22 is Active, not LOCKED | Document header | `IMP-001_Implementation_Playbook.md:6` | `[FACT]` |
| RTA-001's BAR/BAE runtime model is LOCKED but unbuilt | Document header + code absence | `RTA-001...md:7`; cross-checked against Backend/ absence | `[LOCKED]` + `[FACT]` |
| D10 does not conflict with any LOCKED requirement found | Independent re-derivation | `COM-001-005`/`-060` verbatim, §11 above | `[INFERENCE]`, disclosed |

---

## 18. Self-Review

- **No BAR mechanism, registry, or identifier was created by this investigation.** Confirmed — this document only reads and reports. **Confirmed.**
- **No Business Activity was registered.** Confirmed. **Confirmed.**
- **D10 was not reopened, altered, or reinterpreted** — §11 restates it verbatim and only checks it for conflict (finding: none). `ROD-C024-BAR_Treatment_Decision_Preparation.md` itself was read, not modified. **Confirmed.**
- **COM-001 and PE-001 were not modified.** Confirmed — neither file was opened for editing. **Confirmed.**
- **CMD-001, IMP-001, and CLAUDE.md were not modified.** Confirmed. **Confirmed.**
- **No option was selected in §12; no substantive recommendation appears in §16** — only a process statement ("a decision is required"). **Confirmed.**
- **No RO decision was manufactured** — all seven items in §14 trace directly to an ambiguity or gap identified in §5–§11, not invented for completeness. **Confirmed.**
- **C-021/C-022/C-024's own D10-class decisions were treated as precedent only** (§9), never as enterprise policy. **Confirmed.**
- **Every significant assertion carries a source citation and evidence-type tag** (§5–§10, §17). **Confirmed.**
- **No lifecycle state, runtime semantic, or Business Activity Identifier was invented** — §7's inventory explicitly marks every missing identifier as "None," not a placeholder value. **Confirmed.**

---

*End of BAR Enterprise Mechanism Decision Investigation. No BAR mechanism created. No Business Activity registered or identified. D10 unchanged. `COM-001`, `PE-001`, `CMD-001`, `IMP-001`, `CLAUDE.md`, `WPR-001`, `CBOR-INDEX.md`, and every C-024 ROD/IRA/TDS/Charter were read, not modified.*
