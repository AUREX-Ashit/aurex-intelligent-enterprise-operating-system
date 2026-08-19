# Master Capability → Feature → Business Activity → Work Package Delivery Map

**Type:** Governance analysis artifact — same class as `STRATEGIC-PLATFORM-CAPABILITY-TRACEABILITY-REPORT.md`/`HISTORICAL-SCREEN-REALIZATION-MATRIX.md`. **Not an IRA, not an ADR, not a Work Package, not a charter. Creates no capability. Modifies no architecture. Authorizes no implementation.**
**Prepared under:** direct Repository Owner instruction, 2026-08-10. **Corrected under:** direct Repository Owner instruction, 2026-08-19 — a governance/documentation-only synchronization pass against actual repository state, correcting statements that had gone stale since this document's original 2026-08-10 writing (principally: WP-14 BA-01/02/03/04 have since been implemented, independently certified, committed, and pushed — this document's original "zero WP-14 implementation exists" claim no longer holds; BA-05 remains genuinely not started). No capability, feature, Business Activity, or Work Package is added, removed, or redefined by this correction.
**Purpose:** a single, repository-grounded current-state map of Product → Capability → Feature → Business Activity → Work Package → Status, so future chartering decisions (including WP-14's own BA-04/BA-05) are made with the full delivery picture visible, not WP-by-WP in isolation.

**Method:** every row below is sourced directly from `CAP-001_Enterprise_Capability_Registry.md`, `WP-REG-001_Enterprise_Work_Package_Register.md`, `WPR-001_Work_Package_Roadmap.md`, `SER-001_Strategic_Enhancement_Register.md`, `TECH-DEBT.md`, and the `docs/Product/PE-001/capabilities/` directory, re-read directly for this document, not inferred or estimated. **Nothing below is invented.** Where the repository does not decompose a capability further, this is stated as `Not decomposed`, not filled in with a plausible-sounding guess. No Work Package beyond WP-14 is assigned a number anywhere in this document — `WPR-001 §2`'s own text is explicit: *"No Business Capability Work Package beyond WP-14 currently has constitutional ownership anywhere in this repository."*

---

## 0. Vocabulary Note (read before using the matrix)

This repository's own governing methodology (`CLAUDE.md §7`, `IMP-001`) does **not** define a distinct "Feature" layer between Capability and Business Activity. **Business Activities are the primary implementation unit** — a Capability decomposes directly into Business Activities (via an Implementation Readiness Assessment's own Gap Analysis), not through an intermediate, separately-governed "Feature" concept. This document was asked to include a Feature column; to do so without inventing a governance concept that does not exist, the **Feature ID/Name column below is populated from `SER-001`'s own `SE-XXX` Strategic Enhancement entries** — the closest thing this repository actually has to a named, granular, sub-capability deliverable — where one exists for that capability. Where no `SE-XXX` entry exists and no Business Activity exists either, the cell reads `Not decomposed`, honestly, not with an invented feature name. **Capability, Feature (`SE-XXX`), Business Activity, and Work Package are four distinct concepts in this map and are never conflated with each other**, per the governing instruction's own explicit requirement.

---

## 1. Master Capability → Feature → Business Activity → Work Package Matrix

**43 capabilities total** (`CAP-001`, independently re-counted directly against its own table — matches `WP-REG-001 §4`'s own independently-stated figure).

### Domain D-001 — Enterprise Foundation (C-001–C-008 registered)

| Capability ID | Capability Name | Feature (`SE-XXX`) / Name | Business Activity | WP | Status | Evidence / Source | Confidence |
|---|---|---|---|---|---|---|---|
| C-001 | Identity Management | Not decomposed below BA level | BA-01 Detect/Resolve Disrupted Identity Context; BA-02 Recover Inaccessible Identity Context (self-service only); BA-03 Classify Identity Hand-off Rejection | WP-08 | CLOSED — CERTIFIED | `WP-REG-001 §5`/§7, `WPR-001 §2` | High |
| C-002 | Access Management | `SE-019` (TierResolver production build, blocks full C-002) | BA-01 (Unresolved/Deferred branches only), BA-02, BA-03 (classification portion only), BA-04 | WP-05 | CLOSED — CERTIFIED (minimum scope; BA-01 Permitted/Denied and BA-03 re-resolution excluded, gated on `SE-019`) | `WP-REG-001 §5`, `SER-001 §3` | High |
| C-003 | Role & Permission Management | Not decomposed below BA level | WP-02: 9 BAs (full scope). WP-06: BA-01 Understand Domain Permission Context (scoped charter, "Domain Permission Read APIs"). WP-13: cross-cutting retrofit, not itself a BA. | WP-02, WP-06, WP-13 (retrofit) | WP-02 CLOSED — CERTIFIED; WP-06 CLOSED — CERTIFIED; WP-13 IN PROGRESS (retrofit only, no new BA) | `WP-REG-001 §5` | High |
| C-004 | Organization Management | Not decomposed below BA level | 9 BAs (BA-01/01B/01C + BA-02–BA-07, per `IRA-001A` correction) | WP-01 | CLOSED — Certified, with `IRA-001A` correction applied | `WP-REG-001 §5`/§7 | High |
| C-005 | Enterprise Structure Management | `SE-057` (real ERG-001 structural-mutation mechanism — Business Intent gap, `TD-070` High) | 9 BAs, named in full: Establish Organization Node, Understand Structural Position, Frame Structural Change Intent, Shape/Refine Proposed Structural Outcome, Assess Structural Consequence, Review Proposed Structural Outcome, Validate Transition Readiness, Complete Structural Transition, Continue from Resulting Structure | WP-04 | CLOSED — CERTIFIED (BA-08's own completion performs no real structural mutation, `TD-070`/`SE-057`, disclosed) | `WP-REG-001 §5`, `SER-001 §9` | High |
| C-006 | Person Management | `SE-060` (probabilistic/AI-assisted Person-recognition tier, unimplemented) | 10 BAs (BA-01–BA-10), full scope, covering all 12 EXs | WP-07 | CLOSED — CERTIFIED | `WP-REG-001 §5`, `SER-001 §9` | High |
| C-007 | Membership Management | `SE-023` (wire hand-off logic to WP-09's real endpoint) | 11 BAs planned; 9 complete (BA-01/02/03/06/07/08/09/10/11); **BA-04 formally BLOCKED** (external dependency on C-005); **BA-05 formally BLOCKED** (governance decision required) | WP-03 | CLOSED — CERTIFIED (BA-04/BA-05 disposition final, not outstanding work) | `WP-REG-001 §5`, `SER-001 §4` | High |
| C-008 | Workspace Management | `SE-020` (Governed Workspace Entry/Switch/Re-Entry — Critical business value, gated on `SE-019`) | BA-01 Resolve and Present Available Workspace Candidates; BA-02 Detect and Resolve Disrupted Workspace Context; BA-03 Classify Workspace Hand-off Rejection. **3 of 6 ERBs excluded** (`ERB-C008-02`/`03`/`04`/`05`) — largest proportional exclusion of any WP to date. | WP-09 | CLOSED — CERTIFIED (scoped) | `WP-REG-001 §5`, `SER-001 §4` | High |

### Domain D-002 — Commercial & Subscription (C-020–C-025 registered)

| Capability ID | Capability Name | Feature (`SE-XXX`) / Name | Business Activity | WP | Status | Evidence / Source | Confidence |
|---|---|---|---|---|---|---|---|
| C-020 | Subscription Management | Not decomposed | None | None | **WP not yet chartered.** `PE-001-C020` spec exists (`docs/Product/PE-001/capabilities/C-020`). | `CAP-001`, PE-001 directory listing | High |
| C-021 | Product & Service Catalog | Not decomposed | None | None | **WP not yet chartered.** `PE-001-C021` spec exists. | `CAP-001`, PE-001 directory listing | High |
| C-022 | Customer & Account Management | Not decomposed | None | None | **WP not yet chartered.** `PE-001-C022` spec exists. | `CAP-001`, PE-001 directory listing | High |
| C-023 | Licensing & Entitlement | Not decomposed | None | None | **WP not yet chartered.** `PE-001-C023` spec exists. | `CAP-001`, PE-001 directory listing | High |
| C-024 | Billing Management | `SE-043` (charter, Unscheduled, gated on COM-001 EARB certification) | None | None | **WP not yet chartered.** Planned status. `PE-001-C024` spec exists. | `CAP-001`, `SER-001 §6` | High |
| C-025 | Contract Management | `SE-044` (charter, Unscheduled, gated on COM-001 EARB certification) | None | None | **WP not yet chartered.** Planned status. **No `PE-001-C025` spec exists** (confirmed — absent from the PE-001 capabilities directory listing, unlike C-020–024). | `CAP-001`, `SER-001 §6`, PE-001 directory listing | High |

### Domain D-003 — Enterprise Administration (C-040–C-042 registered)

| Capability ID | Capability Name | Feature (`SE-XXX`) / Name | Business Activity | WP | Status | Evidence / Source | Confidence |
|---|---|---|---|---|---|---|---|
| C-040 | Tenant Administration | Not decomposed | None | None | **WP not yet chartered** — not present anywhere in `WP-REG-001`/`WPR-001`'s own WP tables, despite `PE-001-C040` spec existing and Primary Specification being `SD-002`. | `CAP-001`, `WPR-001`, PE-001 directory listing | High |
| C-041 | Configuration Management | `SE-011` umbrella (`SE-012`–`SE-016` sub-facets — see §5) | BA-01 Resolve Enterprise Configuration; BA-02 Establish/Update Enterprise Configuration (scoped: Terminology, Branding-core, Theme-core, Accessibility Profiles, Localization-narrow) | WP-10 | CLOSED — CERTIFIED (scoped; dual-logo Branding, White-label Theme, Configuration Profiles, AI Configuration excluded) | `WP-REG-001 §5`, `SER-001 §2` | High |
| C-042 | Preference & Personalization | `SE-036` (charter, Release D, Unassigned) | None | None | **WP not yet chartered.** Planned status. `TD-110` already determined C-041's own Scope Hierarchy structurally accommodates user-level AI preference without C-042 involvement — narrows, does not eliminate, C-042's own eventual scope. | `CAP-001`, `SER-001 §6`, `TECH-DEBT.md TD-110` | High |

### Domain D-004 — Enterprise Operations (C-060–C-067 registered)

| Capability ID | Capability Name | Feature (`SE-XXX`) / Name | Business Activity | WP | Status | Evidence / Source | Confidence |
|---|---|---|---|---|---|---|---|
| C-060 | Business Workflow Management | Not decomposed; no `SE-XXX` entry found | None | None | **WP not yet chartered.** No `SER-001` entry names this capability directly. | `CAP-001`, `SER-001` (absence confirmed by full read) | Medium — absence of an SE entry is not itself proof no informal planning exists |
| C-061 | Work Management | Not decomposed; no `SE-XXX` entry found | None | None | **WP not yet chartered.** | `CAP-001`, `SER-001` | Medium |
| C-062 | Case Management | `SE-045` (charter, Unscheduled) | None | None | **WP not yet chartered.** Planned status. | `CAP-001`, `SER-001 §6` | High |
| C-063 | Approval Management | `SE-046` (charter, Unscheduled) | None | None | **WP not yet chartered.** Planned status. | `CAP-001`, `SER-001 §6` | High |
| C-064 | Review Management | `SE-047` (charter, Unscheduled) | None | None | **WP not yet chartered.** Planned status. | `CAP-001`, `SER-001 §6` | High |
| C-065 | Decision Management | `SE-048` (charter, incl. general Decision Journal concept, Unscheduled) | None | None | **WP not yet chartered.** Planned status. | `CAP-001`, `SER-001 §6` | High |
| C-066 | Evidence Management | `SE-031` (AI Evidence Fusion table names C-066 as eventual home) | None chartered under C-066 itself — `evidence_registry` exists physically (AMD-012) but was built as a WP-11/C-093 supporting table, not under a C-066 charter | None | **WP not yet chartered as C-066.** A physical `evidence_registry` table exists and is in active use (WP-11, WP-14's own reuse inventory) without any Business Activity ever having been chartered directly against C-066 itself — flagged as a mapping gap (§6E below), not silently resolved. | `CAP-001`, `SER-001 §5`, direct schema evidence | High |
| C-067 | Enterprise Content Management | Not decomposed; no `SE-XXX` entry found | None | None | **WP not yet chartered.** | `CAP-001`, `SER-001` | Medium |

### Domain D-005 — Enterprise Intelligence (C-090–C-095 registered)

| Capability ID | Capability Name | Feature (`SE-XXX`) / Name | Business Activity | WP | Status | Evidence / Source | Confidence |
|---|---|---|---|---|---|---|---|
| C-090 | Enterprise Discovery | `SE-024` (WP-11 umbrella disclosed, "not selected this cycle" for WP-11; realized instead by WP-14) | BA-01 Establish Discovery Provider Configuration; BA-02 Register Enterprise Intelligence Candidate | WP-14 | BA-01 **CLOSED — CERTIFIED** (committed `9bbc117`, pushed); BA-02 **CLOSED — CERTIFIED** (committed `7bace8b`, pushed). WP-14 overall remains **IN PROGRESS** (BA-05 not started) | `WP-REG-001 §5`, `IRA-014 §6` | High |
| C-091 | Knowledge Management | Not decomposed below BA level | BA-04 Establish Knowledge Asset (+ BA-04 Increment F-01 — Lifecycle Transition + `ACCEPTED` Domain Event) | WP-14 | BA-04 **CLOSED — CERTIFIED** (charter accepted and committed; implementation committed `5d41175`/`a5e0c7a`, pushed). BA-04 Increment F-01 **CLOSED — CERTIFIED** (Gate 1 CERTIFIED, F-01 finding remediated/condition closure independently re-certified CLOSED, Gate 2 V&V PASS, Gate 5 Release Readiness READY WITH CONDITIONS — documentation-only; committed `4c86813`, pushed). WP-14 overall remains **IN PROGRESS** (BA-05 not started) | `WP-REG-001 §5`, `IRA-014 §6`, `TDS-014` | High |
| C-092 | Knowledge Graph Management | `SE-025` (Knowledge Graph real/Neo4j build — deferred, out of BA-05's own minimum scope) | BA-05 Synchronize Enterprise Knowledge Graph (relational registry only, live Neo4j write excluded) | WP-14 | **IN PROGRESS** — `IRA-014` Classification B, `ADR-023`/`AMD-016` resolve the tenant-boundary architecture, `TDS-013` (Technical Design, corrected, committed `2cbff08`) exists; BA-05 not yet implementation-authorized | `WP-REG-001 §5`, `IRA-014 §6`, `ADR-023`, `TDS-013` | High |
| C-093 | Enterprise Search | `SE-024`/`SE-026` (both marked Implemented at WP-11's authorized scope) | BA-01 Establish Enterprise Search Index Configuration; BA-02 Execute Enterprise Search; BA-03 Register Enterprise Search Content | WP-11 | CLOSED — CERTIFIED (real embedding/vector-search provider excluded, no credentials) | `WP-REG-001 §5`, `SER-001 §5` | High |
| C-094 | AI Conversation Management | `SE-037` (Partially Implemented) | BA-01 Establish and Manage Conversation Lifecycle; BA-02 Execute Interaction; BA-03 Retrieve Conversation | WP-12 | CLOSED — CERTIFIED (Cross-Lifecycle Agent Handoff, multi-agent visualization, Ask User Gate, streaming, real Reasoning Engine, `C-095` excluded) | `WP-REG-001 §5`, `SER-001 §6` | High — **see discrepancy below** |
| C-095 | Enterprise Memory | `SE-038` (charter, Unscheduled, gated on lifting `ARCH-000 §7c` deferral) | None | None | **WP not yet chartered.** Explicitly deferred by `ARCH-000 §7c`, no placeholder owner. | `CAP-001`, `SER-001 §6` | High |

**Discrepancy flagged, not silently resolved:** `CAP-001` lists **C-094's own Status as `Planned`**, yet `WP-REG-001`/`WPR-001` both record **WP-12 as CLOSED — CERTIFIED** for C-094 (all five `CLAUDE.md §19.7b` gates complete, committed across five commits). Every other capability this repository has fully delivered (C-001–C-008, C-041, C-093) carries a CAP-001 Status of `Active`, not `Planned` — C-094 is the sole exception, and appears to be a CAP-001 staleness gap (its own Status field was never updated after WP-12's closure), not a substantive claim that C-094 is not really delivered. Not corrected here — `CAP-001` is outside this document's edit scope and this pass's own governance rules.

### Domain D-006 — Governance, Risk & Compliance (C-110–C-115 registered)

| Capability ID | Capability Name | Feature (`SE-XXX`) / Name | Business Activity | WP | Status | Evidence / Source | Confidence |
|---|---|---|---|---|---|---|---|
| C-110 | KPI Management | `SE-053`/`SE-054`/`SE-055` (Enterprise Health Score, Goal Intelligence, OKR Intelligence — all "extend C-110") | None | None | **WP not yet chartered.** | `CAP-001`, `SER-001 §8` | High |
| C-111 | Risk Management | Not decomposed; no `SE-XXX` entry found | None | None | **WP not yet chartered.** | `CAP-001`, `SER-001` | Medium |
| C-112 | Compliance Management | Not decomposed; no `SE-XXX` entry found | None | None | **WP not yet chartered.** | `CAP-001`, `SER-001` | Medium |
| C-113 | Policy Management | `SE-039` (charter, Unscheduled — "general, non-authorization-scoped Policy-as-Code") | None | None | **WP not yet chartered.** Planned status. | `CAP-001`, `SER-001 §6` | High |
| C-114 | Audit & Assurance | `SE-035` (AI audit wiring names C-114 as eventual home; borderline TD-vs-SE classification, disclosed by SER-001 itself) | None chartered under C-114 itself | None | **WP not yet chartered.** `record_audit` primitive exists platform-wide (built pre-governance) and is used by every WP, but no Business Activity has ever been chartered directly against C-114. | `CAP-001`, `SER-001 §5` | High |
| C-115 | Reporting & Disclosure | Not decomposed; no `SE-XXX` entry found | None | None | **WP not yet chartered.** | `CAP-001`, `SER-001` | Medium |

### Domain D-007 — Collaboration & Engagement (C-130–C-133 registered)

| Capability ID | Capability Name | Feature (`SE-XXX`) / Name | Business Activity | WP | Status | Evidence / Source | Confidence |
|---|---|---|---|---|---|---|---|
| C-130 | Enterprise Collaboration | Not decomposed; no `SE-XXX` entry found | None | None | **WP not yet chartered.** | `CAP-001`, `SER-001` | Medium |
| C-131 | Enterprise Communication | Not decomposed; no `SE-XXX` entry found | None | None | **WP not yet chartered.** | `CAP-001`, `SER-001` | Medium |
| C-132 | Enterprise Notifications | `SE-018` (backend+frontend wiring; backend model/table/API does not exist at all) | None | None | **WP not yet chartered.** Active status, but genuinely zero implementation — frontend shell is an honest, self-disclosed empty state. | `CAP-001`, `SER-001 §2` | High |
| C-133 | Activity Stream & Timeline | `SE-040` (charter, Release C/D, absorbs the standalone "Timeline" gap) | None | None | **WP not yet chartered.** Planned status. | `CAP-001`, `SER-001 §6` | High |

### Domain D-008 — Enterprise Platform (C-150–C-151 registered)

| Capability ID | Capability Name | Feature (`SE-XXX`) / Name | Business Activity | WP | Status | Evidence / Source | Confidence |
|---|---|---|---|---|---|---|---|
| C-150 | Integration Management | `SE-041` (Connector Framework — `CMD-001 §23`, fully specified, zero implementation) | None | None | **WP not yet chartered.** Active status. | `CAP-001`, `SER-001 §6` | High |
| C-151 | Import & Export Management | `SE-049` (charter, Unscheduled, gated on PLT-001 EARB certification) | None | None | **WP not yet chartered.** Planned status. | `CAP-001`, `SER-001 §6` | High |

---

## 2. Work Package View

| WP | Capability | Business Activities | Impl. Status | Certification Status | Outstanding Items |
|---|---|---|---|---|---|
| WP-00/WP-00A | — (Platform Bootstrap) | N/A (pre-BA governance) | Closed | None (not required — predates process) | None |
| WP-01 | C-004 | 9 (BA-01/01B/01C + BA-02–BA-07) | Closed | `CERT-WP-01` PASS WITH OBS + `CERT-WP-01A` (correction) | None outstanding |
| WP-02 | C-003 | 9 | Closed | `CERT-WP-02` PASS WITH OBS | None outstanding |
| WP-03 | C-007 | 11 planned, 9 complete | Closed | `CERT-WP-03` PASS WITH OBS | BA-04/BA-05 formally BLOCKED (external dep. / governance decision) — final disposition, not outstanding |
| WP-04 | C-005 | 9/9 | Closed | `CERT-WP-04` PASS WITH OBS | `TD-070` (High) — no real structural mutation on completion, disclosed |
| WP-05 | C-002 | 4 (minimum scope) | Closed | `CERT-WP-05` superseded by `VV-AUDIT-WP-05` (2 High findings remediated, independently re-confirmed) | Full BA-01 Permitted/Denied and BA-03 re-resolution excluded pending `SE-019` (TierResolver) |
| WP-06 | C-003 (scoped) | 1 (BA-01) | Closed | All 5 `§19.7b` gates complete, no remediation required | `TD-091` (unbounded list endpoint), Low/Medium |
| WP-07 | C-006 | 10/10 | Closed | All 5 gates complete, no remediation required | `TD-092`–`TD-099` Open (Low/Medium) |
| WP-08 | C-001 | 3/3 | Closed | All 5 gates complete, no remediation required | `TD-100`–`TD-104` Open |
| WP-09 | C-008 | 3/3 | Closed | All 5 gates complete; 1 High/`§19.8.5`-class finding remediated + independently re-verified | `TD-111`/`TD-112` Open (root-cause TierResolver gap) |
| WP-10 | C-041 | 2/2 | Closed | All 5 gates complete; 1 High/`§19.8.5`-class finding (B-1) remediated + independently re-verified | `TD-115`–`TD-122` Open |
| WP-11 | C-093 | 3/3 | Closed | All 5 gates complete; 1 High/`§19.8.5`-class finding remediated + independently re-verified; **not yet committed** | `TD-124`–`TD-128` Open (Low/Medium) |
| WP-12 | C-094 | 3/3 | Closed | All 5 gates complete; 3 Medium/Low findings registered, none `§19.8.5`-class, no remediation required | `TD-133`–`TD-136` Open |
| WP-13 | — (Runtime, cross-cutting) | Not decomposed into formal BAs | **IN PROGRESS** — retrofittable scope under existing architecture exhausted | Not yet certified | See §3 below |
| WP-14 | C-090/091/092 | 5 (BA-01–BA-05) named in `IRA-014`; BA-01/02/03/04 CLOSED — CERTIFIED (BA-04 incl. Increment F-01); BA-05 not started | **IN PROGRESS** | Each closed BA independently certified via its own gate sequence; WP-14 as a whole not yet certified | See §4 below |
| WP-RTA-001 | — (Runtime, serves future capabilities) | N/A — 6 Milestones, not BAs | Complete (M1–M6) | Certified with conditions → resolved (`ADR-016`) | No production `TierResolver` for any tier — "Not production ready" (own Closure Report §7); `TD-071`–`TD-078` Open |

---

## 3. Current WP-13 View

**Chartered to accomplish** (per Repository Owner Instruction "Implementation Replanning Approval," `WPR-001 §2`, `WP-REG-001 §5`): integrate the already-committed, already-certified `Backend/Runtime/AuthorizationEngine` (`WP-RTA-001`, commit `7fac19c`) platform-wide, retiring the interim `PLATFORM_ADMIN`-only pattern every one of WP-01 through WP-12 carries (`TD-021`-class, ~15 open entries at chartering time). Deliver the integration surface first (consumable immediately by WP-14), then retrofit `AuthService`'s and `AIService`'s existing endpoints to consume it — without inventing new authorization architecture. Runs in parallel with WP-14, per explicit instruction.

**What was actually completed** (Increments 2–8, commits `fdc203a`, `4434e77`, `45c2e20`, `3e39d7c`, `5472ebd`, `d5004b2`, `909ba08`):
- Authorization Runtime integration surface delivered (`a180ca4`).
- `domain_permission.py` fully retrofitted: establish/list/get/version/deprecate/retire/dependency-check/resolve-dependency.
- `establish_approval_authority`'s `scope_type='DOMAIN'` subset retrofitted.
- `establish_delegation_policy`'s `scope_type='DOMAIN'` subset retrofitted.
- Each increment shipped with corresponding API-level tests and `CLAUDE.md §21.4` Mandatory Tenant-Isolation validation. Full `AuthService` suite at 798/798 passing (as of the last recorded increment), zero regressions.

**TDs resolved (Closed):** `TD-022`, `TD-090`, `TD-137`, `TD-138`, `TD-139`.
**TDs partially resolved (Open, DOMAIN-scope only):** `TD-023` (Approval Authority), `TD-024` (Delegation Policy) — ORGANIZATION/OBJECT/EVENT scopes remain `PLATFORM_ADMIN`-only.
**TDs remaining Open, confirmed BLOCKED pending Repository Owner architectural decision:** `TD-021` (Role), `TD-025` (Runtime Assignment Policy), `TD-113` (Workspace hand-off), `TD-124`/`TD-129` (AIService — additionally needs a cross-service authorization bridge), `TD-140` (Domain Permission `handoff-rejection`).

**Whether WP-13 is complete, blocked, or awaiting governance — stated exactly as `WP-REG-001` records it, not reinterpreted:** **IN PROGRESS.** Not formally closed. `WP-REG-001 §6`'s own words: *"WP-13's own retrofittable scope under the existing architecture is exhausted; its remaining `TD-021`-class items await a Repository Owner decision on `ADR-002` (AuthService Seed Role Catalog Reconciliation) and/or a dependent-capability/downstream-caller persona and trust model... before further retrofit is possible — WP-13 is not formally closed pending that decision."* No Business Activity decomposition, no Independent Certification, no V&V Audit, no Release Readiness Audit sequence has begun for WP-13 as a whole.

---

## 4. Current WP-14 View

**Capabilities:** C-090 Enterprise Discovery, C-091 Knowledge Management, C-092 Knowledge Graph Management (all `CAP-001` Status: Active), plus the foundational, non-ADR-requiring elements of the Enterprise Intelligence Convergence Lifecycle.

**Business Activities (`IRA-014 §6`):**
- BA-01 — Establish Discovery Provider Configuration (C-090) — **CLOSED — CERTIFIED**, one independent Gate 1 pass (PASS, no A/B findings), committed `9bbc117`, pushed to `origin/main`
- BA-02 — Register Enterprise Intelligence Candidate (C-090, narrowed to `MANUAL_ENTRY`/`API_INGEST`) — **CLOSED — CERTIFIED**, one independent Gate 1 pass (PASS, no A/B findings), committed `7bace8b`, pushed to `origin/main`
- BA-03 — Resolve Enterprise Intelligence Candidate / Convergence Decision (cross-cutting Convergence Lifecycle core) — **CLOSED — CERTIFIED**, all five `CLAUDE.md §19.7b` gates complete (Gate 1 CERTIFIED WITH CONDITIONS → remediated/condition-closed; Gate 2 V&V PASS WITH CONDITIONS → remediated/condition-closed; Gate 5 READY FOR RELEASE/GATE 5 PASSED), committed `10dfe53`, pushed to `origin/main`
- BA-04 — Establish Knowledge Asset (C-091) — **CLOSED — CERTIFIED**; the Business Activity Charter (drafted at this document's own original 2026-08-10 writing) has since been accepted and committed; implementation committed `5d41175`/`a5e0c7a`, pushed to `origin/main`. **BA-04 Increment F-01 — Lifecycle Transition + `ACCEPTED` Domain Event — also CLOSED — CERTIFIED**: Gate 1 CERTIFIED (the originally-found F-01 finding — SUCCESS audit `event_id` must equal the actual published event's `event_id`, `TDS-014 §11` — remediated, condition closure independently re-certified CLOSED); Gate 2 V&V Audit by a fresh, independent reviewer — PASS, all 14 verification objectives re-derived from source with file:line citations, no findings; Gate 5 Release Readiness Audit by a further independent reviewer — READY WITH CONDITIONS, three conditions all documentation-only/non-blocking. 35/35 BA-04 Increment tests, full `AIService` regression 145/145 passing. Committed `4c86813`, pushed to `origin/main`. See `TDS-014_WP-14_BA-04_Increment_Knowledge_Asset_Lifecycle_Transition_Technical_Design.md`.
- BA-05 — Synchronize Enterprise Knowledge Graph (C-092, relational registry only) — **NOT STARTED.** No implementation of any kind exists (independently re-confirmed by repository-wide grep for `enterprise_knowledge_graph`/`KnowledgeGraphSyncHandler`/`RelationshipResolutionService`/`EntityOwnershipResolver`/`Neo4j` during the BA-04 Increment F-01 Gate 2/Gate 5 audits — no hits beyond design-document disclosure text). `TDS-013` exists as its own Technical Design Specification (last committed `2cbff08`); not yet implementation-authorized.

**`IRA-014` classification/readiness:** All five BAs — **Classification B, architecturally unblocked**. `IRA-014` is now recorded as **Accepted** (`WP-REG-001 §5`/`WPR-001 §2`, both citing "`IRA-014_WP-14_Enterprise_Intelligence_Foundation_Implementation_Readiness_Assessment.md` (Accepted)") — superseding this document's own original 2026-08-10 statement that Acceptance was "Not yet granted." Of the three open items `IRA-014 §11` originally named: (1) the convergence-matching algorithm (BA-03 only) was resolved by BA-03's own implementation (CLOSED — CERTIFIED, above); (2) the hosting-service decision is resolved **for BA-01–04** as a matter of fact — all four are implemented and certified under `AIService` — whether it is formally, separately confirmed as the decision for BA-05 specifically is not re-derived here (BA-05 is out of this document's own edit scope); (3) BA-05's own BR-1–BR-4 enforcement mechanism remains resolved on paper only by `TDS-013`, not yet implementation-authorized — unchanged.

**`ADR-023`:** Accepted, committed (`ccb36af`), pushed. Resolves the `enterprise_knowledge_graph_registry` tenant-boundary architecture question (BR-1–BR-4) that had classified BA-05 as Classification C — STOP. Does not itself authorize BA-05 implementation (`ADR-023 §6`).

**`TDS-013`:** BA-05's own Technical Design Specification. Corrected twice this session (three narrowly-scoped design corrections at `d00c8b6`; one Events-infrastructure staleness correction at `2cbff08`), committed and pushed. Technically sound per the completed Repository Owner review. Hosting service remains explicitly OPEN pending Repository Owner concurrence.

**Current implementation readiness — corrected, this pass, against direct repository evidence (this statement was stale as of this document's own original 2026-08-10 writing and is the specific correction this governance pass exists to make):** BA-01, BA-02, BA-03, and BA-04 (including BA-04's own Increment F-01) have all been implemented, independently certified, committed, and pushed to `origin/main` — this is **not** a case of "zero WP-14 implementation exists." Real, tested, certified code exists in `Backend/Services/AIService/` for all four (`discovery_providers.py`/`intelligence_candidates.py`/`knowledge_asset.py` routers and their own services/repositories/schemas/models, plus BA-04 Increment F-01's own `events/knowledge_asset_events.py`). **BA-05 alone remains at zero implementation** — independently re-confirmed by repository-wide search during the BA-04 Increment F-01 Gate 2/Gate 5 audits, no hits beyond design-document disclosure text. WP-14 itself is **IN PROGRESS** per `WP-REG-001` — 4 of 5 Business Activities `IRA-014` names are now formally closed in the register's own execution-tracking sense; only BA-05 remains not started.

**Dependencies/blockers, consolidated and corrected this pass:**
- Hosting-service decision — **resolved for BA-01–04** as a matter of implemented, certified fact (all four hosted in `AIService`); BA-05's own hosting-service status is unchanged from this document's own prior statement, since re-deriving it is outside this pass's own edit scope (BA-05 implementation itself is out of scope for this correction).
- BA-04's own per-trigger-event-type mapping — **resolved**: `TDS-014` (BA-04 Increment F-01's own Technical Design) freezes the `KnowledgeAssetAcceptedEvent` contract (`event_name`/`event_version`/payload), now implemented and certified. BA-05's own *consumption* of that event (the `KnowledgeGraphSyncHandler` `TDS-013 §26a` names) remains unimplemented — unchanged, still a Repository Owner/implementation-time decision for BA-05's own future authorization.
- `Backend/Shared/Events` import blocker — **already resolved** (`TD-105` Closed, Release A1) — no longer a live blocker for BA-05's event-triggered path; BA-04 Increment F-01's own event class is the first concrete `BaseEvent` subclass anywhere in this repository to actually exercise this framework, per `TDS-014`.
- WP-13's own authorization integration surface is a stated dependency (`WPR-001 §2`: "Depends on WP-13's own integration-surface delivery for its own authorization gating") — the surface itself is delivered (§3 above), so this dependency is satisfied for the interim `PLATFORM_ADMIN` pattern BA-01–04 (and BA-04 Increment F-01, which reuses the identical `require_platform_admin` dependency verbatim) use; WP-13's own remaining `TD-021`-class blockers do not gate WP-14 (different resource shapes).

---

## 5. Future / Uncharted Feature Map

Grouped using this repository's own domain/capability terminology (`CAP-001` D-XXX), not invented categories. Each item is a real `SE-XXX` entry from `SER-001` or a capability with no `SE-XXX` entry at all (marked accordingly) — no capability or feature is invented here.

**D-001 Enterprise Foundation** — fully chartered (C-001–C-008 all have a WP). Remaining gaps are sub-capability, gated on `SE-019` (TierResolver): `SE-020` (Governed Workspace Entry/Switch/Re-Entry, Critical business value), `SE-021` (Governed Identity Establishment), `SE-022` (Administrator-initiated Identity recovery), `SE-023` (C-007→C-008 hand-off wiring).

**D-002 Commercial & Subscription** — C-020/021/022/023 (Active, PE-001 specs exist, no WP, no `SE-XXX` charter entry found); C-024 Billing (`SE-043`, gated on COM-001 EARB certification); C-025 Contract (`SE-044`, gated on COM-001 EARB certification, no PE-001 spec exists).

**D-003 Enterprise Administration** — C-040 Tenant Administration (Active, no WP, no `SE-XXX` entry — the most evidenced-but-unchartered capability in this domain, since a PE-001 spec exists); C-042 Preference & Personalization (`SE-036`, Release D).

**D-004 Enterprise Operations** — C-060/061 (Active, no `SE-XXX` entry at all); C-062/063/064/065 (each has its own `SE-04X` charter entry, all Unscheduled); C-066 Evidence Management (physical table exists via WP-11, never chartered directly); C-067 (Active, no `SE-XXX` entry).

**D-005 Enterprise Intelligence** — C-095 Enterprise Memory (`SE-038`, explicitly deferred by `ARCH-000 §7c`). The rest of this domain is chartered (WP-11/WP-12/WP-14).

**D-006 Governance, Risk & Compliance** — C-110 (`SE-053`/`054`/`055`, "extend C-110"); C-111/112/115 (Active, no `SE-XXX` entry); C-113 (`SE-039`, Unscheduled); C-114 (`SE-035`, borderline TD/SE classification, disclosed as such by `SER-001` itself).

**D-007 Collaboration & Engagement** — C-130/131 (Active, no `SE-XXX` entry); C-132 (`SE-018`, zero backend implementation); C-133 (`SE-040`, Release C/D).

**D-008 Enterprise Platform** — C-150 (`SE-041`, Connector Framework, fully specified, zero implementation); C-151 (`SE-049`, gated on PLT-001 EARB certification).

**Cross-cutting / Enterprise Experience** (not tied to one capability): `SE-004` (Saved Views), `SE-005`/`SE-006` (Universal Search/command palette), `SE-017` (feature-flag frontend wiring), `SE-028`–`SE-034` (AI Runtime build-out: prompt management, policy engine, real confidence computation, Evidence Fusion, cost tracking, tool governance, unified observability), `SE-041`/`SE-042`/`SE-063` (Connector Framework, Plugin architecture, Extensibility & Marketplace — deliberately sequenced to avoid mutual duplication), `SE-050` (Executive Cognition / Future Platform umbrella — Digital Twin, Simulation, Executive Copilot, Skills Graph, Prompt/Workflow Studio, AI Marketplace, Operating Manual, Autonomous BAs — gated cluster, Release D), `SE-051`/`SE-052` (retention policies, data residency), `SE-056` (Recommendation Engine, least-specified item in the register), `SE-061`/`SE-062` (Enterprise DNA & Adaptive Experience, Two-Layer Sacred 12 — both structural patterns, not yet populated by any capability).

---

## 6. Gap Analysis

**A. Capabilities with no feature decomposition at all (no `SE-XXX`, no BA, no WP):** C-060, C-061, C-067, C-111, C-112, C-115, C-130, C-131 — 8 capabilities. All `Active` status in `CAP-001`, none named anywhere in `SER-001`'s 66 entries. This does not mean no informal planning exists elsewhere in the repository — only that this pass found no `SE-XXX` entry or BA/WP evidence for them.

**B. Features (`SE-XXX`) with no Business Activity decomposition:** the large majority of `SER-001`'s 66 entries — every entry marked `Deferred`/`Open` and `Planned WP: Unassigned` (roughly 45 of 66). Not enumerated individually here; see §5 above and `SER-001` directly for the full list.

**C. Business Activities with no WP:** none found — every Business Activity this repository's governance documents name (across all closed WPs and WP-14) is already assigned to a WP. This is expected, since Business Activities are only formally named inside an IRA, which itself belongs to a specific WP.

**D. Capabilities/features awaiting an architectural decision before further progress:**
- C-002/C-001(partial)/C-008(partial) — gated on `SE-019` (TierResolver production implementation), the single highest-evidence platform dependency in `SER-001` (5 independent disclosures, consolidated as `TD-111`).
- C-090/091/092 (WP-14) — hosting-service decision (`IRA-014 §11` item 2) resolved for BA-01–04, all implemented and certified under `AIService`; BA-04's own event-trigger mapping resolved by `TDS-014`/BA-04 Increment F-01 (the `KnowledgeAssetAcceptedEvent` contract is now implemented and certified). What remains gated: BA-05's own implementation authorization and its own consumption of that event (not invented, Repository Owner/implementation-time decision).
- C-003 (WP-13's remaining scope) — gated on `ADR-002` (AuthService Seed Role Catalog Reconciliation) and/or a dependent-capability persona/trust model.
- C-042 — soft-gated on `TD-110`'s own already-made determination narrowing, not eliminating, its scope.
- C-024/C-025 — gated on COM-001 EARB constitutional certification.
- C-151 — gated on PLT-001 EARB constitutional certification.
- C-095 — gated on a Repository Owner decision to lift the `ARCH-000 §7c` deferral.

**E. Features/tables already implemented but not clearly mapped to a current capability/WP:**
- `evidence_registry` (physical, real, built by WP-11) — functionally serves C-066 Evidence Management, but no Business Activity was ever chartered against C-066 itself; it exists only as a WP-11/C-093 supporting table.
- `data_ingestion_registry` — LOCKED at the architecture-document level (`Master_Technical_Architecture.md`), referenced by `knowledge_asset_registry.source_ingestion_id`, but **has no physical Backend model anywhere** — a finding this session independently made while chartering BA-04, correcting `IRA-014`'s own claim that it is "pre-existing, real, built by WP-11." `IngestionService` instead built a differently-named, non-canonical pair of tables (`aurex_documents`/`aurex_upload_trackers`) using a non-standard tenant-representation pattern (`tenant_id: String`, not this repository's own standard `organization_id: UUID FK`).
- `record_audit` (platform-wide primitive, built pre-governance) — functionally serves C-114 Audit & Assurance, no Business Activity ever chartered directly against C-114.
- Feature-flag backend (`SE-017`) — fully built, zero capability/WP owns its frontend consumption.

---

## 7. Delivery Roadmap

### COMPLETED (formally completed/certified)
WP-00, WP-00A, WP-01, WP-02, WP-03, WP-04, WP-05, WP-06, WP-07, WP-08, WP-09, WP-10, WP-11, WP-12, WP-RTA-001 (Certified, conditions resolved) — covering C-001 through C-008, C-041, C-093, C-094.

### CURRENT (formally chartered / in progress)
WP-13 (Runtime, cross-cutting authorization retrofit — retrofittable scope exhausted, remaining items blocked pending Repository Owner decision) and WP-14 (C-090/C-091/C-092, Enterprise Intelligence Foundation — 5 BAs specified by `IRA-014`, now Accepted; BA-01/02/03/04 CLOSED — CERTIFIED and pushed to `origin/main` (BA-04 incl. Increment F-01); only BA-05 not yet started).

### KNOWN FUTURE (repository-supported, no WP chartered — no hypothetical WP number assigned)
Every capability/feature named in §5 above: C-020, C-021, C-022, C-023, C-024 (`SE-043`), C-025 (`SE-044`), C-040, C-042 (`SE-036`), C-060, C-061, C-062 (`SE-045`), C-063 (`SE-046`), C-064 (`SE-047`), C-065 (`SE-048`), C-066, C-067, C-095 (`SE-038`), C-110 (`SE-053`–`055`), C-111, C-112, C-113 (`SE-039`), C-114 (`SE-035`), C-115, C-130, C-131, C-132 (`SE-018`), C-133 (`SE-040`), C-150 (`SE-041`), C-151 (`SE-049`), plus the cross-cutting Enterprise Experience/AI-Runtime/Executive-Cognition enhancement set (`SE-001`/`004`–`006`/`017`/`028`–`034`/`041`/`042`/`050`–`056`/`061`–`063`).

---

## Final Counts

- **Total known capabilities (`CAP-001`):** 43
- **Total known features identified (`SER-001` `SE-XXX` entries):** 66 (`SE-001`–`SE-066`)
- **Total formally defined Business Activities identified:** 72 completed (`WP-REG-001 §4`'s own directly-cited figure — WP-01 through WP-12 inclusive, plus WP-14's own BA-01/02/03/04, all CLOSED — CERTIFIED; BA-04's own Increment F-01 is additive scope within already-counted BA-04, not a separate Business Activity) + 1 named by `IRA-014` for WP-14 not yet closed (BA-05) = **73 named**, of which 2 remain formally BLOCKED within an otherwise-closed WP (WP-03 BA-04/BA-05)
- **Total formally chartered Work Packages:** 16 Business-lifecycle entries (WP-00, WP-00A, WP-01–WP-14) + 1 Runtime (WP-RTA-001) = **17**
- **Completed WPs:** 14 (WP-00, WP-00A, WP-01–WP-12 — `WP-REG-001 §4`'s own directly-cited figure) — **plus WP-RTA-001, Certified with conditions resolved but not yet formally transitioned to "Closed" in `WPR-001`** (a known, disclosed staleness item `WP-REG-001 §4` itself flags — reported here, not corrected, per this document's own no-silent-fix rule)
- **Current WPs:** 2 (WP-13, WP-14)
- **Known-but-uncharted feature areas:** 29 capabilities with no WP (43 total − 14 chartered [C-001–008, C-041, C-090–094, C-093 counted once] = 29; cross-checked directly against §1's own per-capability rows)
- **Major decomposition gaps:** 8 capabilities with zero feature/BA/WP evidence of any kind (§6A); `SE-019` (TierResolver) as the single highest-leverage platform dependency, gating parts of 3 already-delivered capabilities; the `data_ingestion_registry` non-existence finding (§6E), directly relevant to WP-14 BA-04; C-066/C-114's own "supporting infrastructure exists, capability never formally chartered" pattern.

---

*End of this map. No implementation, migration, model, router, service, API, ADR, Technical Design, or Business Activity/Work Package charter was created by this document. `CAP-001`, `WP-REG-001`, `WPR-001`, `SER-001`, `TECH-DEBT.md`, `IRA-014`, `ADR-023`, `TDS-013`, and `CLAUDE.md` are unmodified by this pass. **Correction to this document's own original 2026-08-10 closing statement:** this document is in fact already registered in `DOC-000`'s own catalogue, as its own Governance row (added during the original Master Capability/Feature/BA/WP Delivery Map registration pass, 2026-08-10) — the prior claim that it was "not yet registered" was itself stale, found and corrected by this same governance-synchronization pass. `DOC-000`'s own "Last Updated" value for that row (still 2026-08-10) is not updated by this pass — updating `DOC-000` is explicitly out of this pass's own edit scope; disclosed as a known follow-up, not performed here.*
