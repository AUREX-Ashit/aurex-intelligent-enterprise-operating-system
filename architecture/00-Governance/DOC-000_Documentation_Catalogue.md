# DOC-000 — Enterprise Documentation Register (EDR)

**Type:** Authoritative Enterprise Documentation Register — governs the repository's own document inventory, metadata, ownership, and navigation. (Sections 1–7 below retain this document's original role as the Repository Navigation Guide; that role is preserved unchanged, not replaced — see Section 8 onward for the Register itself.)
**Status:** Current as of Constitutional Baseline v2.0; evolved into the Enterprise Documentation Register per repository-owner governance decision (2026-07-30)
**Read time:** ~10 minutes (Sections 1–7); ~10 further minutes for the Register (Sections 8–12)
**Relationship to WP-REG-001:** Complementary, not overlapping. DOC-000 answers *"What governed documents exist within the Enterprise Operating System?"* — inventory, metadata, ownership, canonical status, navigation. `WP-REG-001` answers *"What is the current implementation state?"* — Work Package lifecycle, Business Activity progress, certification status. DOC-000 SHALL NOT contain implementation status; `WP-REG-001` SHALL NOT contain document inventory. Neither supersedes the other.

---

## 1. Purpose

This catalogue is the single entry point into the Aurex Enterprise Operating System repository. It exists because the repository now spans 20+ registered architecture documents across four layers, and no single document previously told a reader which one to open first.

**How to use it:** find your role in Section 6, or your task in Section 5's "If I want to..." table, and go straight to the named document. Section 3 is the full reference catalogue; consult it when Sections 5–6 don't cover your case. **For the complete, authoritative inventory of every governed document in the repository** (metadata, ownership, canonical/lifecycle status, update triggers) **see Section 8 onward — the Enterprise Documentation Register.**

**Who should read it:** every new architect, developer, reviewer, or AI coding agent, before opening any other file in this repository.

---

## 2. Repository Structure

```
Complete Blueprint          (Enterprise Philosophy, narrative vision)
        ↓
ARCH-000 / CAP-001          (Governance: the map, and capability identity)
        ↓
Constitutional Layer        (SD-001..003, URA-001, ERG-001, CMD-001, RTA-001,
                              EIA-001, COM-001, GRC-001, PLT-001, ONT-001, OPM-001)
        ↓
Experience Layer            (PE-001, PE-001-Cxxx)
        ↓
Engineering Layer           (IMP-001, Master Technical Architecture)
        ↓
Implementation              (MDP-001, source code, database, infrastructure)
```

Each layer consumes the layer above it and never redefines it. This mirrors ARCH-000 §3's own layering exactly.

---

## 3. Master Document Catalogue

### Governance

| Document | Owner | Purpose | Dependencies |
|---|---|---|---|
| **ARCH-000** | Chief Architecture Office | The authoritative entry point; defines every document's responsibility, ownership, and the Constitutional Document Standard. | None — read this first. |
| **DOC-000** (this document) | Chief Architecture Office | Navigation guide to the whole repository. | ARCH-000 |
| **WPR-001** | Repository Owner / Engineering Governance | The authoritative Work Package → Capability roadmap; the single source for which WP-NN implements which C-XXX. | CAP-001, ARCH-000 |

### Layer 1 — Constitutional Architecture

| Document | Owner | Purpose | Dependencies |
|---|---|---|---|
| **CAP-001** | Product Architecture | The immutable registry of every business capability, its domain, and its one Primary Specification. | ARCH-000 |
| **Complete Blueprint** | Product Architecture | Enterprise philosophy, the 39 Laws, and the IDAL (Discover-First) narrative vision. | ARCH-000 |
| **SD-001** | Product Architecture | What users see and how every screen is designed — presentation principles, Evidence/Confidence presentation, Guided Completion. | SD-002, SD-003 |
| **DS-001** | Design Authority | The AUREX visual design system — tokens, themes, components, accessibility. | SD-001 |
| **SD-002** | Product Architecture | The Universal Business Object model — every CDE, BQ, BA, Evidence, and lifecycle rule in the platform. | SD-001, SD-003 |
| **SD-003** | Product Architecture | Enterprise interaction laws — approvals, escalation, delegation, notifications, human/AI interaction sequencing. | SD-001, SD-002 |
| **URA-001** | Security Architecture | Identity, roles, permissions, approval authorities, and assignment/escalation authorization data model. | SD-002, SD-003, ERG-001 |
| **ERG-001** | Enterprise Architecture | Enterprise structure and relationship graph — how organizations, nodes, and entities connect. | URA-001 |
| **CMD-001** | Data Architecture | Canonical metadata, the Canonical Business Object Register (CBOR), and physical data-shape reference. | SD-002, ERG-001 |
| **RTA-001** | Chief Architecture Office | How the platform executes at runtime — Business Activity, Workflow, Knowledge Graph, and AI Runtime. | CMD-001, SD-002, SD-003 |
| **EIA-001** (Vol. I & II) | Enterprise Intelligence Architect | Enterprise Intelligence's business semantics — Discovery, Knowledge, Search, AI Conversation, Memory. | CMD-001, ERG-001, URA-001 |
| **COM-001** | Product Architecture | Commercial & Subscription business semantics — Subscription, Offering, Customer, Billing. | CAP-001, SD-002 |
| **GRC-001** | Product Architecture | Governance, Risk & Compliance business semantics — KPI, Risk, Compliance, Policy, Disclosure. | CAP-001, SD-002 |
| **PLT-001** | Product Architecture | Enterprise Platform business semantics — Integration and Data Exchange as governed business relationships. | CAP-001, CMD-001, RTA-001 |
| **ONT-001** | Chief Architecture Office | The constitutional vocabulary of semantic relationship kinds (Classification, Composition, Association, etc.). | SD-002, CMD-001 |
| **OPM-001** | Chief Architecture Office | How the constitutional domains coordinate with each other — orchestration only, owns nothing itself. | All Layer 1 documents |

### Layer 2 — Experience Architecture

| Document | Owner | Purpose | Dependencies |
|---|---|---|---|
| **PE-001** | Product Architecture | The canonical Enterprise Experience methodology — Journeys, Personas, Workspaces, Navigation; v1.1 adds AI/Decision/Search Experience. | CAP-001, all Layer 1 |
| **PE-001-Cxxx** | Product Architecture | Capability-specific experience blueprints conforming to PE-001. See Section 4. | PE-001 |

### Layer 3 — Engineering Architecture

| Document | Owner | Purpose | Dependencies |
|---|---|---|---|
| **IMP-001** | Engineering Architecture | The engineering playbook — coding standards, the Business Activity Registry (BAR), implementation patterns. | All Layer 1, RTA-001 |
| **Master Technical Architecture** | Engineering Architecture | The physical schema (136 tables), technology stack (PostgreSQL, Neo4j, Temporal, Azure), and RLS policies. | CMD-001, URA-001, ERG-001 |

### Layer 4 — Implementation Specifications

| Document | Owner | Purpose | Dependencies |
|---|---|---|---|
| **MDP-001** | Engineering Architecture | Master data population / seed data rules for a new tenant. | CMD-001, CAP-001 |

### Supporting Artifacts (not independently registered in ARCH-000)

| Artifact | Purpose |
|---|---|
| `architecture/07-Decisions/ADR-*` | Architecture Decision Records — formal, superseding changes to a Locked document. |
| `cil/Domain_*.xlsx`, `cil/industry-packs/*` | Canonical Intelligence Library — the enterprise vocabulary (entities, KPIs, metrics) to consult before naming anything new. |
| `docs/Product/Implementation/EIS-001` | Enterprise Intelligence Implementation Specification — engineering detail for the EI platform. |
| `CLAUDE.md` | AI coding agent operating instructions for this repository. |

---

## 4. PE-001 Capability Catalogue

| Capability | Name | Purpose |
|---|---|---|
| C-001 | Identity Management | Manage enterprise identities. |
| C-002 | Access Management | Govern access rights. |
| C-003 | Role & Permission Management | Manage authorization roles and permissions. |
| C-004 | Organization Management | Manage enterprise organizations. |
| C-005 | Enterprise Structure Management | Maintain enterprise structure. *(Gold Standard reference CRB.)* |
| C-006 | Person Management | Manage enterprise persons. |
| C-007 | Membership Management | Manage enterprise memberships. |
| C-008 | Workspace Management | Provide contextual workspaces. |
| C-020 | Subscription Management | Manage subscriptions. |
| C-021 | Product & Service Catalog | Manage offerings. |
| C-022 | Customer & Account Management | Manage customer relationships. |
| C-023 | Licensing & Entitlement | Manage entitlements. |
| C-024 | Billing Management | Manage billing. |
| C-040 | Tenant Administration | Administer tenants. |

*(All other CAP-001 capabilities — C-041 onward — have no PE-001-Cxxx specification yet; their business intent is defined directly in CAP-001.)*

---

## 5. Quick Reference

| If I want to... | Read first |
|---|---|
| Add or change a Business Object, CDE, or BQ | **SD-002** |
| Modify permissions, roles, or approval authorities | **URA-001** |
| Modify runtime execution, workflow, or the AI Runtime | **RTA-001** |
| Implement a new feature end-to-end | **CAP-001** → the capability's domain document → **PE-001** |
| Modify UX, screens, or presentation | **SD-001**, then **DS-001** for visual design |
| Add an ontology / semantic relationship concept | **ONT-001** |
| Modify metadata, canonical data shape, or the CBOR | **CMD-001** |
| Implement APIs, services, or the database schema | **IMP-001**, then **Master Technical Architecture** |
| Understand a commercial, governance, or platform business rule | **COM-001** / **GRC-001** / **PLT-001** (per domain) |
| Understand how domains coordinate with each other | **OPM-001** |
| Understand Enterprise Intelligence, Knowledge, or Search | **EIA-001** |

---

## 6. Recommended Reading Order

**New Architect:** ARCH-000 → CAP-001 → Complete Blueprint → SD-002 → OPM-001

**Developer:** ARCH-000 → CAP-001 → IMP-001 → Master Technical Architecture → SD-002

**AI Coding Agent:** ARCH-000 → CLAUDE.md → CAP-001 → the relevant domain document (Section 5) → IMP-001

**Reviewer:** ARCH-000 → CAP-001 → the document under review → its Freeze Statement / Full Principle Index → OPM-001 (for cross-domain impact)

**Enterprise Architect:** ARCH-000 → Complete Blueprint → CAP-001 → all Layer 1 documents → OPM-001

---

## 7. Architecture Map

```
                         Complete Blueprint
                                │
                             ARCH-000 ── CAP-001
                                │
   ┌───────┬────────┬─────────┼──────────┬──────────┬──────────┐
 SD-001  SD-002   SD-003   URA-001    ERG-001    CMD-001    RTA-001
   │        │        │         │          │          │          │
   └────────┴────────┴─────────┴──────────┴──────────┴──────────┘
                                │
              COM-001 · GRC-001 · PLT-001 · ONT-001 · OPM-001
                                │
                             EIA-001
                                │
                              PE-001 ── PE-001-Cxxx
                                │
                    IMP-001 ── Master Technical Architecture
                                │
                             MDP-001
                                │
                      source/ · Backend/ · database/
```

Read top to bottom. Every arrow is "consumes," never "redefines" — per ARCH-000 Architectural Principle 1, each concern has exactly one owner.

---

---

# PART II — ENTERPRISE DOCUMENTATION REGISTER

*(Sections 8–12. Sections 1–7 above are preserved unchanged as this document's original Repository Navigation Guide content. This Part is the new material governed by DOC-000's evolved role.)*

## 8. Enterprise Documentation Register

The master inventory. Every governed document appears exactly once. `Version`/`Last Updated` values not independently re-verified against `git log` in this pass are marked accordingly rather than estimated.

### Architecture (Layer 1 — Constitutional)

| Document ID | Document Name | Category | Repository Path | Owner | Canonical Status | Lifecycle Status | Current Version | Last Updated | Primary Audience |
|---|---|---|---|---|---|---|---|---|---|
| ARCH-000 | Enterprise Operating System Architecture Manifest | Architecture | `architecture/00-Governance/ARCH-000 – Enterprise Operating System Architecture Manifest.md` | Chief Architecture Office | Canonical, top-level authority | AUTHORITATIVE | 1.7 (§7c Knowledge Governance row corrected per Release A1 Foundation Repairs, `IRA-RELEASE-A`) | 2026-08-01 | All roles |
| SD-001 | Enterprise Presentation Architecture | Architecture | `architecture/02-Constitutional/SD-001 — Enterprise Presentation Architecture.md` | Product Architecture | Canonical | LOCKED | 2.0 (Gold Standard) | Not independently dated this pass | Architects, Frontend |
| SD-002 | Universal Business Object Rules | Architecture | `architecture/02-Constitutional/SD-002_Universal_Business_Object_Rules.md` | Product Architecture | Canonical | LOCKED | 2.2 (Gold Standard) | Not independently dated this pass | All engineering roles |
| SD-003 | Enterprise Interaction Laws | Architecture | `architecture/02-Constitutional/SD-003_Enterprise_Interaction_Laws.md` | Product Architecture | Canonical | LOCKED | 2.0 (Gold Standard) | Not independently dated this pass | Architects, Frontend |
| URA-001 | User, Role, Permission, Event and Assignment | Architecture | `architecture/02-Constitutional/URA-001 - User, Role, Permission, Event and ssignment.md` | Security Architecture | Canonical | LOCKED | 2.1 (Gold Standard) | Not independently dated this pass | Security, Backend |
| ERG-001 | Enterprise Structure & Relationship Management | Architecture | `architecture/02-Constitutional/ERG-001 Enterprise Structure & Relationship Management (ESRM).md` | Enterprise Architecture | Canonical | LOCKED | 2.0 (Gold Standard) | Not independently dated this pass | Architects, Backend |
| CMD-001 | Canonical Data Model | Architecture | `architecture/02-Constitutional/CMD-001_Canonical_Data_Model.md` | Data Architecture | Canonical | LOCKED | 1.3 (Gold Standard) | Not independently dated this pass | Data, Backend |
| RTA-001 | Runtime Architecture and Execution | Architecture | `architecture/02-Constitutional/RTA-001 - Runtime Architecture and Execution.md` | Chief Architecture Office | Canonical | LOCKED | 1.0 | Not independently dated this pass | Architects, Backend, Runtime engineers |
| EIA-001 | Enterprise Intelligence Architecture (Vol. I & II) | Architecture | `docs/Product/Implementation/EIS-001` region (per DOC-000 §3 Supporting Artifacts) — canonical volumes referenced, not re-verified this pass | Enterprise Intelligence Architect | Canonical | Frozen v1.0 | 1.0 | Not independently dated this pass | AI/Intelligence engineers |
| COM-001 | Commercial & Subscription Architecture | Architecture | `architecture/02-Constitutional/COM-001_Commercial_and_Subscription_Architecture.md` | Product Architecture | Canonical | LOCKED | 1.0 | Not independently dated this pass | Commercial domain engineers |
| GRC-001 | Governance, Risk & Compliance Architecture | Architecture | `architecture/02-Constitutional/GRC-001_Governance_Risk_and_Compliance_Architecture.md` | Product Architecture | Canonical | LOCKED | 1.0 | Not independently dated this pass | GRC domain engineers |
| PLT-001 | Enterprise Platform Architecture | Architecture | `architecture/02-Constitutional/PLT-001_Enterprise_Platform_Architecture.md` | Product Architecture | Canonical | LOCKED | 1.0 | Not independently dated this pass | Platform/Integration engineers |
| OPM-001 | Enterprise Operating Model Architecture | Architecture | `architecture/02-Constitutional/OPM-001_Enterprise_Operating_Model_Architecture.md` | Chief Architecture Office | Canonical | LOCKED | 1.0 | Not independently dated this pass | Cross-domain architects |
| ONT-001 | Enterprise Ontology Architecture | Architecture | `architecture/02-Constitutional/ONT-001_Enterprise_Ontology_Architecture.md` | Chief Architecture Office | Canonical | LOCKED | 1.0 | Not independently dated this pass | Data, Knowledge engineers |

### Experience (Layer 2)

| Document ID | Document Name | Category | Repository Path | Owner | Canonical Status | Lifecycle Status | Current Version | Last Updated | Primary Audience |
|---|---|---|---|---|---|---|---|---|---|
| PE-001 | Enterprise Experience Blueprint | Experience | `docs/Product/PE-001/PE-001_Enterprise_Experience_Blueprint.md` | Product Architecture | Canonical | LOCKED (evolving under ARCH-000 §12.6) | 1.1 | Not independently dated this pass | Experience/Product engineers |
| PE-001-Cxxx | Capability-specific Experience Blueprints (14 authored: C-001–008, C-020–024, C-040) | Experience | `docs/Product/PE-001/capabilities/C-0XX/` | Product Architecture | Canonical (per capability) | Varies — see §4 above for the full 14-entry catalogue | Varies | Not independently dated this pass | Capability implementers |

### Engineering (Layer 3)

| Document ID | Document Name | Category | Repository Path | Owner | Canonical Status | Lifecycle Status | Current Version | Last Updated | Primary Audience |
|---|---|---|---|---|---|---|---|---|---|
| IMP-001 | Implementation Playbook | Engineering | `architecture/03-Engineering/IMP-001_Implementation_Playbook.md` | Engineering Architecture | Canonical | Active (Controlled Evolution, `ARCH-000 §12.6`) | Not independently versioned this pass | Not independently dated this pass | All engineering roles |
| Master Technical Architecture | Master Technical Architecture | Engineering | `architecture/04-Technical/Master_Technical_Architecture.md` | Engineering Architecture | Canonical | Active, evolving via amendment log | 7.2 (AMD-015, Prompt/Model Configuration Reconciliation, per Release A2 — **note: this row was already stale at 6.9 before this pass; the document's own header had already reached v7.1 via AMD-014-adjacent completion amendments never reflected here — corrected to the true current version, not merely incremented**) | 2026-08-01 | Backend, Data, Platform |
| MDP-001 | Master Data Population Specification | Implementation | `architecture/05-Implementation/MDP-001_Master_Data_Population_Specification.md` | Engineering Architecture | Canonical | LOCKED | 1.2 (Gold Standard) | Not independently dated this pass | Backend, DevOps |
| METH-001 | Engineering Methodology Improvements (Post-WP-04 Retrospective) | Engineering | `architecture/03-Engineering/METH-001_Engineering_Methodology_Improvements.md` | Engineering Governance | Non-canonical (retrospective) | Adopted per `ADR-014` | N/A | 2026-07-30 (recovered) | Engineering Governance |
| METH-002 | Engineering Methodology Improvements (Post-WP-05 Retrospective) | Engineering | `architecture/03-Engineering/METH-002_WP-05_Engineering_Methodology_Improvements.md` | Engineering Governance | Non-canonical (retrospective) | Adopted per `ADR-017` | N/A | 2026-07-31 | Engineering Governance |
| METH-003 | Implementation Methodology v2.0 (Post-WP-09 Formalization) | Engineering | `architecture/03-Engineering/METH-003_Implementation_Methodology_v2.md` | Engineering Governance | Non-canonical (synthesis of existing canonical authority; no redefinition) | Adopted per `ADR-018` | N/A | 2026-08-02 | Engineering Governance |
| AMD-014 | Domain Business Object Architecture Completion | Engineering | `architecture/04-Technical/AMD-014_Domain_Business_Object_Architecture_Completion.md` | Engineering Architecture | Amendment (Master Technical Architecture) | Architecture completion required | N/A | Not independently dated this pass | Backend |

### Design

| Document ID | Document Name | Category | Repository Path | Owner | Canonical Status | Lifecycle Status | Current Version | Last Updated | Primary Audience |
|---|---|---|---|---|---|---|---|---|---|
| DS-001 | AUREX Design System | Design | `architecture/02-Constitutional/DS-001 — AUREX Design System.md` | Design Authority | Canonical | RELEASED | 1.0 | Not independently dated this pass | Frontend, Design |
| DS-001 (Release Record) | DS-001 — Version and Release Record | Design | `architecture/02-Constitutional/DS-001 — Version and Release Record.md` | Design Authority | Canonical (governing release record) | RELEASED | 1.0 | Not independently dated this pass | Design, Frontend |

### Governance

| Document ID | Document Name | Category | Repository Path | Owner | Canonical Status | Lifecycle Status | Current Version | Last Updated | Primary Audience |
|---|---|---|---|---|---|---|---|---|---|
| CAP-001 | Enterprise Capability Registry | Governance | `architecture/02-Constitutional/CAP-001_Enterprise_Capability_Registry.md` | Product Architecture | Canonical | Architecture Review Complete | 1.5 | Not independently dated this pass | All roles |
| WPR-001 | Work Package Roadmap | Governance | `architecture/00-Governance/WPR-001_Work_Package_Roadmap.md` | Repository Owner / Engineering Governance | Governance Registry (roadmap/definition authority) | Active | N/A (living registry) | 2026-08-01 | Engineering Governance, Implementers |
| WP-REG-001 | Enterprise Work Package Register | Governance | `architecture/00-Governance/WP-REG-001_Enterprise_Work_Package_Register.md` | Repository Owner / Engineering Governance | Governance Registry (execution-status authority) | Active | 1.0 | 2026-08-01 | Executives, Architects, Reviewers |
| DOC-000 | Enterprise Documentation Register (this document) | Governance | `architecture/00-Governance/DOC-000_Documentation_Catalogue.md` | Chief Architecture Office | Governance Registry (document-inventory authority) | Active | 2.0 (evolved from Navigation Guide) | 2026-08-01 | All roles |
| CBOR-INDEX | Canonical Business Object Register Index | Governance | `architecture/00-Governance/CBOR-INDEX.md` | Engineering Governance | Governance Registry | Active | N/A (living index) | Not independently dated this pass | Engineering |
| TECH-DEBT | Technical Debt Register | Governance | `architecture/06-Reviews/TECH-DEBT.md` | Repository-wide (per-entry ownership) | Governance Registry | Active | N/A (living register, 122 entries — recounted directly against the Register table during the WP-10 Gate 5 Release Readiness Audit, 2026-08-02; TD-115 through TD-122 confirmed well-formed, 8-column rows and non-duplicated) | 2026-08-02 (latest: TD-122, `ConfigurationLifecycleState.RETIRED` unreachable by any write path, found by `VV-AUDIT-WP-10`) | All engineering roles |
| ADR Index | Architecture Decision Records (ADR-001 through ADR-021; ADR-016 and ADR-021 not yet committed to the repository as of this row's own update — verified via `git status`, not assumed) | Governance | `architecture/07-Decisions/ADR-*.md` | Repository Owner (per-decision) | Governance (superseding-change authority) | 21 Accepted | N/A (index of 21 documents) | 2026-08-07 (latest: ADR-021, AI-Native Enterprise Experience Framework Constitutional Foundation; preceded by ADR-020, AI Session Management Conversation and Interaction Constitutional Foundation, committed) | Architects, Reviewers |
| IRA Reports | Implementation Readiness Assessments (IRA-001, IRA-001A, IRA-002 through IRA-009, IRA-RTA-001, IRA-010, IRA-011) | Governance | `architecture/05-Implementation/IRA-*.md` | Implementing session per WP | Governance (readiness gate) | 13 Accepted (`IRA-010` accepted per Repository Owner Instruction "WP-10 Implementation Authorization," committed `9865bac`; `IRA-011` accepted per Repository Owner Instruction "WP-11 Implementation Authorization," 2026-08-03, not yet committed) | N/A (index of 13 documents) | 2026-08-03 (latest: `IRA-011`, accepted, not yet committed) | Implementers, Reviewers |
| Independent Review / Certification Reports | CERT-WP-01, CERT-WP-01A, CERT-WP-02, CERT-WP-03, CERT-WP-04, CERT-WP-05, CERT-WP-06, CERT-WP-07, CERT-WP-08, CERT-WP-09, CERT-WP-10, CERT-WP-11, CERT-WP-RTA-001 | Governance | `architecture/06-Reviews/CERT-*.md` | Independent (fresh-context) reviewer, per `CLAUDE.md §19.7` | Governance (certification authority) | 13 issued (11 PASS/CERTIFIED WITH OBSERVATIONS, 2 CERTIFIED WITH CONDITIONS — both resolved) — CERT-WP-05's own PASS WITH OBSERVATIONS did not survive a subsequent independent V&V audit (`VV-AUDIT-WP-05`, two `CLAUDE.md §19.8.5`-class defects); both remediated and independently re-verified (`VV-AUDIT-WP-05_Remediation_Verification.md`, CONFIRMED WITH OBSERVATIONS) — WP-05 restored to CLOSED — Certified. CERT-WP-06's own V&V Audit and Release Readiness Audit have both since completed — WP-06 is CLOSED — Certified, committed `a82ff87`. CERT-WP-07 has since been followed by its own V&V Audit (`VV-AUDIT-WP-07`) and Release Readiness Audit (`RRA-WP-07`) — WP-07 is CLOSED — Certified, committed `6da647e`. CERT-WP-08 (first Work Package under `CLAUDE.md §20`) has since been followed by its own V&V Audit (`VV-AUDIT-WP-08`) and Release Readiness Audit (`RRA-WP-08`) — WP-08 is CLOSED — Certified, committed `808c06d`. CERT-WP-09's own V&V Audit found one High/`CLAUDE.md §19.8.5`-class defect (a cross-tenant Membership-status disclosure), remediated and independently re-verified (`VV-AUDIT-WP-09_Remediation_Verification.md`), followed by its own Release Readiness Audit (`RRA-WP-09`) — WP-09 is CLOSED — Certified, committed `90544cb`/`6ce9bd3`/`d648150`. **CERT-WP-10** (first Work Package under `CLAUDE.md §21`) found a High/`CLAUDE.md §19.8.5`-class blocking finding (Finding B-1 — cross-tenant Configuration disclosure via an unverified `X-Tenant-ID` header), remediated and independently re-verified (`CERT-WP-10_Remediation_Verification.md`), followed by its own V&V Audit (`VV-AUDIT-WP-10`, PASS WITH OBSERVATIONS) and Release Readiness Audit (`RRA-WP-10`) — WP-10 is **CLOSED — Certified**, all five gates complete, committed `ae50998`/`9865bac`. **CERT-WP-11** — CERTIFIED WITH OBSERVATIONS, no blocking finding — has since been followed by its own V&V Audit (`VV-AUDIT-WP-11`, one High/`CLAUDE.md §19.8.5`-class finding, remediated and independently confirmed by `VV-AUDIT-WP-11_Remediation_Verification.md`) and Release Readiness Audit (`RRA-WP-11`, RELEASE READY) — WP-11 is **CLOSED — Certified**, all five gates complete, not yet committed. | N/A (index of 13 documents) | 2026-08-03 (latest: CERT-WP-11, WP-11 CLOSED — Certified) | Executives, Reviewers, Auditors |
| VV-AUDIT-WP-11 | WP-11 Independent Verification & Validation Audit | Governance | `architecture/06-Reviews/VV-AUDIT-WP-11_Enterprise_Search.md` | Independent (fresh-context) reviewer, no prior WP-11 involvement (second reviewer, distinct from `CERT-WP-11`'s own reviewer) | Verification & Validation Audit — Gate 2 of `CLAUDE.md §19.7b`'s five-gate sequence, distinct from and more exhaustive than Independent Certification | **Remediation required before Gate 5** — Requirements Traceability Matrix against `IRA-011 §5`/§10; five from-scratch runtime probe scripts (not adapted from the shipped suite), including a two-organization identical-index-name adversarial probe and a harness FK-enforcement probe; found one High/`CLAUDE.md §19.8.5`-class blocking defect (Finding 1 — no uniqueness constraint on `(organization_id, index_name)`, causing `VectorIndexRegistryRepository.get_by_name_for_caller`'s own `.scalar_one_or_none()` to raise `MultipleResultsFound`, an unhandled 500 in both BA-02 and BA-03, fully reachable through ordinary sequential use) and one Low finding (`TD-127`, `active_flag` default value non-conformant with AMD-012) | N/A | 2026-08-03 | Executives, Reviewers, Auditors |
| VV-AUDIT-WP-11_Remediation_Verification | WP-11 Remediation Re-Verification | Governance | `architecture/06-Reviews/VV-AUDIT-WP-11_Remediation_Verification.md` | Independent (fresh-context) reviewer — third distinct reviewer, no involvement in the design, implementation, `CERT-WP-11`, or `VV-AUDIT-WP-11` | Independent re-verification of a correction, per `CLAUDE.md §19.7` and `§19.7b` (required regardless of the finding's own severity) | **REMEDIATION VERIFIED — CONFIRMED** — negative control reconstructed the pre-fix code, confirmed it reproduced both the original crash and a failing regression test, then confirmed the restored fix closes both; full suite re-run, 33/33 passing; independently assessed the fix's own scoping (platform-wide vs. tenant-dedicated correctly distinguished) and disclosed one further Medium residual risk (`TD-128`, a check-then-insert concurrency race, calibrated against this repository's own `TD-118` precedent) | N/A | 2026-08-03 | Executives, Reviewers, Auditors |
| RRA-WP-11 | WP-11 Release Readiness Audit | Governance | `architecture/06-Reviews/RRA-WP-11_Enterprise_Search_Release_Readiness_Audit.md` | Independent (fresh-context) reviewer, no prior WP-11 involvement (sixth reviewer, distinct from the implementation, `CERT-WP-11`, `VV-AUDIT-WP-11`, and `VV-AUDIT-WP-11_Remediation_Verification`) | Release Readiness Audit — Gate 5 of `CLAUDE.md §19.7b`'s five-gate sequence; verifies git status, repository-wide consistency, full regression results, and governance-document accuracy, not content correctness (already covered by Gates 1/2/4) | **RELEASE READY — authorized for commit (local commit only; no push).** Independently re-ran 33/33 full suite, `alembic heads` (single head, `d4a9c1e7f3b5`), a full upgrade/downgrade cycle against a disposable database, and `tsc`/`eslint`/`next build`; confirmed clean WP-11 change-set scoping, no scope creep, unrelated concurrent working-tree material (WP-RTA-001, `design/`) independently confirmed genuinely untouched; directed the WP-11 charter/`IRA-011`/`RELEASE-C-INITIATION-SUMMARY.md`/AIService Authentication Bootstrap prerequisite (never committed) into a two-commit closure sequence; directly corrected extensive governance-documentation staleness across `WP-REG-001`, `WPR-001`, `SER-001`, and this document (this row and two others added). | N/A | 2026-08-03 | Executives, Reviewers, Auditors |
| AAR-001 | Architecture Audit Remediation Register | Governance | `architecture/06-Reviews/AAR-001_Architecture_Audit_Remediation_Register.md` | Architecture Governance | Planning artifact (no architecture modified) | CERTIFIED WITH OBSERVATIONS | 2.1 | 2026-07-30 (recovered) | Architecture Governance |
| ARM-001 | Architecture Remediation Implementation Report (AR-001) | Governance | `architecture/06-Reviews/ARM-001_Implementation_Report.md` | Implementing session | Implementation Report | Complete (committed `770aaad`) | N/A | 2026-07-30 (corrected) | Architecture Governance |
| ENTERPRISE-AI-ARCHITECTURE-AUDIT | Enterprise AI Architecture Audit | Governance | `architecture/06-Reviews/ENTERPRISE-AI-ARCHITECTURE-AUDIT.md` | Independent architecture reviewer | Architecture Review (read-only) | Final: OPTION B | N/A | 2026-07-30 (recovered) | Architecture Governance, AI engineers |
| AUTHORIZATION_ENGINE_CONSTITUTIONAL_RESPONSE | Authorization Engine Constitutional Response | Governance | `architecture/06-Reviews/AUTHORIZATION_ENGINE_CONSTITUTIONAL_RESPONSE.md` | Implementing session (Constitutional Review) | Review artifact | Complete — recommendation PARTIAL REUSE | N/A | 2026-07-30 | Architecture Governance |
| BCGA-001 | Business Capability Gap Assessment — C-003 Domain Permission Query Access | Governance | `architecture/06-Reviews/BCGA-001_C003_Domain_Permission_Query_Access_Gap_Assessment.md` | Implementing session (fact-finding, per CLAUDE.md §17 STOP) | Advisory review artifact — not an IRA, not an ADR | **Accepted and acted upon.** `EX-C003-11` (Understand Domain Permission Context) was added to `PE-001-C003` (now Version 1.1) per this assessment's own recommendation — see `CAR-001_PE-001-C003_EX-C003-11_Capability_Amendment_Report.md` | N/A | 2026-07-31 | Repository Owner, Architecture Governance |
| CAR-001 | Capability Amendment Report — PE-001-C003 Version 1.1 (EX-C003-11) | Governance | `architecture/06-Reviews/CAR-001_PE-001-C003_EX-C003-11_Capability_Amendment_Report.md` | Implementing session (capability engineering activity, per repository-owner instruction) | Capability amendment record — not an IRA, not a Work Package implementation | Complete — `PE-001-C003` approved as governing authority for chartering WP-06 | N/A | 2026-07-31 | Repository Owner, Architecture Governance |
| WP-RTA-001_Closure_Report | WP-RTA-001 Closure Report | Governance | `architecture/06-Reviews/WP-RTA-001_Closure_Report.md` | Implementing session | Closure Report (not a certification) | Implementation Complete | N/A | 2026-07-30 | Architecture Governance, Reviewers |
| WP-RTA-001_Self_Verification_Audit | WP-RTA-001 Self-Verification Audit | Governance | `architecture/06-Reviews/WP-RTA-001_Self_Verification_Audit.md` | Implementing session | Self-verification (explicitly not a certification) | Complete | N/A | 2026-07-30 | Architecture Governance |
| VV-AUDIT-WP-05 | WP-05 Independent Verification & Validation Audit | Governance | `architecture/06-Reviews/VV-AUDIT-WP-05_Access_Management.md` | Independent (fresh-context) auditor, no prior WP-05 involvement | Verification & Validation Audit — distinct from, and more rigorous than, Independent Certification (`CLAUDE.md §19.7`); re-examines a Work Package already carrying a `CERT-WP-*` determination | PASS WITH MINOR REMEDIATION (2 High findings, non-`CLAUDE.md §19.8.5`-deferrable; remediated, see `VV-AUDIT-WP-05_Remediation_Verification` below) | N/A | 2026-07-31 | Executives, Reviewers, Auditors |
| VV-AUDIT-WP-05_Remediation_Verification | WP-05 Remediation Re-Verification | Governance | `architecture/06-Reviews/VV-AUDIT-WP-05_Remediation_Verification.md` | Independent (fresh-context) reviewer — third distinct reviewer, no involvement in the design, implementation, original certification, or the V&V audit that found F-01/F-02 | Independent re-verification of a correction, per `CLAUDE.md §19.7` and `VV-AUDIT-WP-05`'s own Finding F-06 (a prior self-attested remediation was criticized for lacking this step) | **CONFIRMED WITH OBSERVATIONS** — 24 from-scratch probe checks + 2 negative controls against pre-fix code; restored WP-05 to CLOSED — Certified | N/A | 2026-07-31 | Executives, Reviewers, Auditors |
| VV-AUDIT-WP-06 | WP-06 Independent Verification & Validation Audit | Governance | `architecture/06-Reviews/VV-AUDIT-WP-06_Domain_Permission_Read_APIs.md` | Independent (fresh-context) reviewer, no prior WP-06 involvement (second reviewer, distinct from `CERT-WP-06`'s own reviewer) | Verification & Validation Audit — Gate 2 of `CLAUDE.md §19.7b`'s five-gate sequence, distinct from and more exhaustive than Independent Certification | **PASS WITH OBSERVATIONS** — Requirements Traceability Matrix against `EX-C003-11`'s full primary-source text; purpose-built two-Organization probe; no `CLAUDE.md §19.8.5`-class defect found; two forward-looking findings (F-02, F-03) folded into `TD-090`/`TD-091`'s Resolution Criteria; no remediation required | N/A | 2026-07-31 | Executives, Reviewers, Auditors |
| VV-AUDIT-WP-07 | WP-07 Independent Verification & Validation Audit | Governance | `architecture/06-Reviews/VV-AUDIT-WP-07_Person_Management.md` | Independent (fresh-context) reviewer, no prior WP-07 involvement (second reviewer, distinct from `CERT-WP-07`'s own reviewer) | Verification & Validation Audit — Gate 2 of `CLAUDE.md §19.7b`'s five-gate sequence, distinct from and more exhaustive than Independent Certification | **PASS WITH OBSERVATIONS** — Requirements Traceability Matrix against all 12 EXs and Business Rule conformance table against all 12 BRs, both from `PE-001-C006`'s own primary-source text; two purpose-built runtime probes empirically confirmed `TD-093` (concurrency race) and `TD-096` (FK-enforcement gap); one new completeness finding (`TD-099`, `EX-C006-09`'s stale-context rule); no `CLAUDE.md §19.8.5`-class defect found; no remediation required | N/A | 2026-07-31 | Executives, Reviewers, Auditors |
| VV-AUDIT-WP-08 | WP-08 Independent Verification & Validation Audit | Governance | `architecture/06-Reviews/VV-AUDIT-WP-08_Identity_Management.md` | Independent (fresh-context) reviewer, no prior WP-08 involvement (second reviewer, distinct from `CERT-WP-08`'s own reviewer) | Verification & Validation Audit — Gate 2 of `CLAUDE.md §19.7b`'s five-gate sequence, distinct from and more exhaustive than Independent Certification | **PASS WITH OBSERVATIONS** — Requirements Traceability Matrix against all 8 EXs and Business Rule conformance table against all 9 BRs, both from `PE-001-C001`'s own primary-source text (independently re-extracted a second time); two purpose-built runtime probes (BA-02/`C-002` zero-interaction; `TD-096`-class FK-enforcement reproduction, not currently live); independently re-rated `TD-103`'s severity Medium (from `CERT-WP-08`'s own Medium-High) and found its proposed remediation path not achievable without inventing new architecture; no `CLAUDE.md §19.8.5`-class defect found; no remediation required | N/A | 2026-08-01 | Executives, Reviewers, Auditors |
| RRA-WP-06 | WP-06 Release Readiness Audit | Governance | `architecture/06-Reviews/RRA-WP-06_Domain_Permission_Read_APIs_Release_Readiness_Audit.md` | Independent (fresh-context) reviewer, no prior WP-06 involvement (fourth reviewer, distinct from the implementation, `CERT-WP-06`, and `VV-AUDIT-WP-06`) | Release Readiness Audit — Gate 5 of `CLAUDE.md §19.7b`'s five-gate sequence; verifies git status, repository-wide consistency, full regression results, and governance-document accuracy, not content correctness (already covered by Gates 1–2) | **RELEASE READY — authorized for commit/push.** Independently re-ran 622/622 full suite and `alembic heads`; confirmed clean WP-06 change-set scoping (flagged a staging caution re: co-resident, unrelated WP-RTA-001 untracked files); directly corrected three pre-existing/introduced governance-documentation staleness items in `WP-REG-001` and `DOC-000` (including this document's own total/category document-count arithmetic) | N/A | 2026-07-31 | Executives, Reviewers, Auditors |
| RRA-WP-07 | WP-07 Release Readiness Audit | Governance | `architecture/06-Reviews/RRA-WP-07_Person_Management_Release_Readiness_Audit.md` | Independent (fresh-context) reviewer, no prior WP-07 involvement (fourth reviewer, distinct from the implementation, `CERT-WP-07`, and `VV-AUDIT-WP-07`) | Release Readiness Audit — Gate 5 of `CLAUDE.md §19.7b`'s five-gate sequence; verifies git status, repository-wide consistency, full regression results, and governance-document accuracy, not content correctness (already covered by Gates 1–2) | **RELEASE READY — authorized for commit/push.** Independently re-ran 664/664 full suite and `alembic heads` (single head, `05f620c521e9`); confirmed clean WP-07 change-set scoping (flagged a staging caution re: co-resident, unrelated WP-RTA-001 untracked files); directly corrected six governance-documentation staleness items in `WP-REG-001` and `DOC-000` (gate-transition phrasing, a stale pre-WP-05 `HEAD` reference, document-count arithmetic, a stale TD-range example, stale `Last Updated` dates). **This row was itself missing from this register until identified and added by `RRA-WP-08`'s own Gate 5 review — a pre-existing, `RRA-WP-07`-introduced omission, not a new one this document creates.** | N/A | 2026-07-31 | Executives, Reviewers, Auditors |
| RRA-WP-08 | WP-08 Release Readiness Audit | Governance | `architecture/06-Reviews/RRA-WP-08_Identity_Management_Release_Readiness_Audit.md` | Independent (fresh-context) reviewer, no prior WP-08 involvement (fourth reviewer, distinct from the implementation, `CERT-WP-08`, and `VV-AUDIT-WP-08`) | Release Readiness Audit — Gate 5 of `CLAUDE.md §19.7b`'s five-gate sequence; verifies git status, repository-wide consistency, full regression results, and governance-document accuracy, not content correctness (already covered by Gates 1–2) | **RELEASE READY — authorized for commit/push.** Independently re-ran 687/687 full suite and `alembic heads` (single head, `b1d6f4c8a3e7`); confirmed clean WP-08 change-set scoping; found and corrected a two-commits-stale `HEAD`/"Repository Commit" self-reference in `WP-REG-001` (`6da647e` → the actual current `c9dd215`, the WP-08 charter commit) and this document's own missing `RRA-WP-07` row; independently confirmed `VV-AUDIT-WP-08`'s own flagged `WPR-001` staleness (Finding F-05) was actually corrected, not merely claimed; directly corrected seven further governance-documentation staleness items in `WP-REG-001` and `DOC-000` (gate-transition phrasing, document-count arithmetic, a stale TD-range example, stale `Last Updated` dates). | N/A | 2026-08-01 | Executives, Reviewers, Auditors |
| VV-AUDIT-WP-09 | WP-09 Independent Verification & Validation Audit | Governance | `architecture/06-Reviews/VV-AUDIT-WP-09_Workspace_Management.md` | Independent (fresh-context) reviewer, no prior WP-09 involvement (second reviewer, distinct from `CERT-WP-09`'s own reviewer) | Verification & Validation Audit — Gate 2 of `CLAUDE.md §19.7b`'s five-gate sequence, distinct from and more exhaustive than Independent Certification | **Remediation required before Gate 5** — Requirements Traceability Matrix against all 6 ERBs/11 EXs and Business Rule conformance table against all 7 BRs, both from `PE-001-C008`'s own primary-source text (independently re-extracted a second time); found one Medium/deferrable finding (`TD-112`, BA-02 never requests an Access Evaluation Outcome, via a from-scratch runtime probe with a seeded `DENIED` `AccessEvaluationOutcome`) and one High/`CLAUDE.md §19.8.5`-class finding (`TD-113`'s own subject — a cross-tenant Membership-status disclosure via `POST /workspaces/classify-handoff-rejection`, confirmed via a from-scratch, two-tenant runtime probe, and independently re-rated High against `VV-AUDIT-WP-05`'s own F-02 precedent, disagreeing with Gate 1's own recommendation to defer it) | N/A | 2026-08-02 | Executives, Reviewers, Auditors |
| VV-AUDIT-WP-09_Remediation_Verification | WP-09 Remediation Re-Verification | Governance | `architecture/06-Reviews/VV-AUDIT-WP-09_Remediation_Verification.md` | Independent (fresh-context) reviewer — fourth distinct reviewer, no involvement in the design, implementation, `CERT-WP-09`, or `VV-AUDIT-WP-09` | Independent re-verification of a correction, per `CLAUDE.md §19.7` and `§19.7b` (required regardless of the finding's own severity) | **REMEDIATION VERIFIED** — negative control reproduced the original defect against the pre-fix commit (`d648150`, restored via `git stash`, confirmed vulnerable, then reverted with no data loss); post-fix code confirmed to require `PLATFORM_ADMIN` and reject the identical two-tenant scenario with 403; full suite re-run, 718/718 passing; incidentally found the identical disclosure shape in the already-CLOSED WP-08's own `/identity/classify-handoff-rejection`, disclosed as `TD-114`, WP-08 not reopened per `CLAUDE.md §20.1` | N/A | 2026-08-02 | Executives, Reviewers, Auditors |
| RRA-WP-09 | WP-09 Release Readiness Audit | Governance | `architecture/06-Reviews/RRA-WP-09_Workspace_Management_Release_Readiness_Audit.md` | Independent (fresh-context) reviewer, no prior WP-09 involvement (fifth reviewer, distinct from the implementation, `CERT-WP-09`, `VV-AUDIT-WP-09`, and `VV-AUDIT-WP-09_Remediation_Verification`) | Release Readiness Audit — Gate 5 of `CLAUDE.md §19.7b`'s five-gate sequence; verifies git status, repository-wide consistency, full regression results, and governance-document accuracy, not content correctness (already covered by Gates 1/2/4) | **RELEASE READY — authorized for commit.** Independently re-ran 718/718 full suite and `alembic heads` (single head, `b1d6f4c8a3e7`); confirmed clean WP-09 change-set scoping, no scope creep; found WP-09's own governing charter/IRA and both business-value/platform-dependency review documents had never been committed to the repository despite being cited by already-committed documents, directing the closure commit to include all four; directly identified governance-documentation staleness items in `IMP-REPORT-WP-09`, `WP-REG-001`, `WPR-001`, and `DOC-000` (this document), corrected in this same closure pass. | N/A | 2026-08-02 | Executives, Reviewers, Auditors |
| CERT-WP-10_Remediation_Verification | WP-10 Remediation Re-Verification | Governance | `architecture/06-Reviews/CERT-WP-10_Remediation_Verification.md` | Independent (fresh-context) reviewer — second distinct reviewer, no involvement in the design, implementation, or `CERT-WP-10`'s own Gate 1 Certification | Independent re-verification of a correction, per `CLAUDE.md §19.7` and `§19.7b` (required regardless of the finding's own severity) — Gate 4 of the five-gate sequence | **REMEDIATION VERIFIED** — negative control confirmed both governing tests FAIL against the pre-fix code (via a temporary revert, one disclosing another Organization's actual `theme_class` override to an unrelated caller) and PASS against the restored fixed code; independently confirmed `require_matching_tenant_or_platform_admin`'s own logic has no bypass path, no import cycle, and no double-evaluation risk; full suite re-run, 743/743 passing; `POST /configuration`/`GET /configuration/entries` confirmed unaffected | N/A | 2026-08-02 | Executives, Reviewers, Auditors |
| VV-AUDIT-WP-10 | WP-10 Independent Verification & Validation Audit | Governance | `architecture/06-Reviews/VV-AUDIT-WP-10_Configuration_Management.md` | Independent (fresh-context) reviewer, no prior WP-10 involvement (third reviewer, distinct from `CERT-WP-10`'s own reviewer and `CERT-WP-10_Remediation_Verification`'s own reviewer) | Verification & Validation Audit — Gate 2 of `CLAUDE.md §19.7b`'s five-gate sequence, distinct from and more exhaustive than Independent Certification | **PASS WITH OBSERVATIONS** — Requirements Traceability Matrix against `CMD-001 §12`'s full mandatory-characteristics list and all five in-scope facets; four from-scratch runtime probes empirically confirmed `TD-118`'s concurrent-write race claim and `TD-115`'s USER-scope unreachability claim, and independently re-confirmed Finding B-1's own remediation has no bypass path; no `CLAUDE.md §19.8.5`-class defect found; four new, non-blocking findings registered as `TD-119` (High severity, non-blocking — Accessibility facet substitutes `high_contrast_enabled` for `DS-001-194`'s actual large-text requirement), `TD-120`/`TD-121` (Low — AI Discoverability/Approval Workflow applicability never explicitly recorded), `TD-122` (Low — `RETIRED` lifecycle state unreachable); no remediation required | N/A | 2026-08-02 | Executives, Reviewers, Auditors |
| RRA-WP-10 | WP-10 Release Readiness Audit | Governance | `architecture/06-Reviews/RRA-WP-10_Configuration_Management_Release_Readiness_Audit.md` | Independent (fresh-context) reviewer, no prior WP-10 involvement (fourth reviewer, distinct from the implementation, `CERT-WP-10`, `CERT-WP-10_Remediation_Verification`, and `VV-AUDIT-WP-10`) | Release Readiness Audit — Gate 5 of `CLAUDE.md §19.7b`'s five-gate sequence; verifies git status, repository-wide consistency, full regression results, and governance-document accuracy, not content correctness (already covered by Gates 1/2/4) | **RELEASE READY — authorized for commit.** Independently re-ran 743/743 full suite, `tsc`/`eslint`/`next build`, and confirmed via direct file inspection that `c7e2b5a9f1d4` is the sole leaf migration revision; confirmed clean WP-10 change-set scoping; found WP-10's own governing charter and `IRA-010` had never been committed to the repository despite being cited by already-committed documents, directing the closure commit to include both, mirroring `RRA-WP-09`'s own identical finding; directly corrected governance-documentation staleness in `WP-REG-001` and `DOC-000` (this document), including a pre-existing, WP-10-unrelated omission of WP-09 from `WP-REG-001 §4`/`§10`'s own aggregate counts dating from before WP-09's own closure. | N/A | 2026-08-02 | Executives, Reviewers, Auditors |
| RELEASE-B-INTEGRATION-SE009-EDR1-READINESS | Release B Integration, SE-009 Enterprise Experience Gate & EDR-1 Preparation | Governance | `architecture/06-Reviews/RELEASE-B-INTEGRATION-SE009-EDR1-READINESS.md` | Implementing session (Phases 1/2/5 of the Repository Owner's own "Release B Integration, Certification & EDR-1 Preparation" instruction) | Release-level validation artifact — not an IRA, not an ADR, not a Work Package; validates WP-09+WP-10 integration and executes `SE-009` for the first time | Complete — one real gap found and remediated (Theme establish now applies live); `SE-004`/`SE-003`/`SE-001` confirmed out of Release B's own chartered scope (Roadmap-description accuracy gap, not an implementation defect); no blocking issue | N/A | 2026-08-03 | Executives, Product, Repository Owner, Reviewers |
| RELEASE-C-INITIATION-SUMMARY | Release C Initiation & WP-11 Planning — Summary | Governance | `architecture/06-Reviews/RELEASE-C-INITIATION-SUMMARY.md` | Implementing session, per Repository Owner Instruction "Release C Initiation & WP-11 Planning" | Release-level planning artifact — not an IRA, not an ADR, not a Work Package; consolidates the WP-11 capability-selection evidence, charter status, `IRA-011` status, and SER-001/Enterprise-Experience/Executive-Experience allocation into one summary | Complete, planning-only — WP-11 charter reviewed/corrected, `IRA-011` drafted (READY at scope, pending acceptance); no implementation performed | N/A | 2026-08-03 | Executives, Product, Repository Owner, Reviewers |
| PRODUCT-MILESTONE-ROADMAP | Product Milestone Roadmap | Governance | `architecture/06-Reviews/PRODUCT-MILESTONE-ROADMAP.md` | Implementing session (Product Delivery Strategy exercise, per repository-owner instruction) | Planning artifact — reframes the Architecture Evolution Roadmap and Implementation Programme as a customer-facing delivery roadmap; not an IRA, not an ADR, not a Work Package, creates no capability | Active (refined into canonical form per repository-owner instruction; subject to further repository-owner-directed refinement) | 1.2 (Milestone 1's own "Enterprise Experience Delivered"/"Expected Demonstration Scenarios" corrected 2026-08-03 — an overclaim naming Saved Views/Discover-First parity/Progressive Disclosure as delivered, found by the Release B Independent Certification and Readiness Assessment) | 2026-08-03 | Executives, Product, Commercial, Architecture Governance |
| RELEASE-A2-AI-CONFIGURATION-GOVERNANCE-REVIEW | Release A2 — AI Configuration Governance Review | Governance | `architecture/06-Reviews/RELEASE-A2-AI-CONFIGURATION-GOVERNANCE-REVIEW.md` | Implementing session (focused architectural validation, per repository-owner instruction) | Advisory review artifact, same class as `ENTERPRISE-AI-ARCHITECTURE-AUDIT`/`BCGA-001` — not an IRA, not an ADR, not a Work Package, creates no capability, modifies no architecture | Complete — refines R4 (recommends `reasoning_engine_registry` as canonical over `llm_prompt_registry`), reaffirms R5 deferred, discloses one new related finding (`rag_configs` vs `vector_index_registry`) | N/A | 2026-08-01 | Repository Owner, Architecture Governance |
| AI-CONFIGURATION-TRACEABILITY-MATRIX | AI Configuration Traceability Matrix | Governance | `architecture/06-Reviews/AI-CONFIGURATION-TRACEABILITY-MATRIX.md` | Implementing session (architecture consistency validation, per repository-owner instruction) | Advisory review artifact, same class as `ENTERPRISE-AI-ARCHITECTURE-AUDIT`/`RELEASE-A2-AI-CONFIGURATION-GOVERNANCE-REVIEW` — not an IRA, not an ADR, not a Work Package, creates no capability, modifies no architecture | Complete — validated ~60 AI concepts against ownership; found 2 duplicate-ownership items (R4, and a new `rag_configs`/`vector_index_registry` finding), 1 new ambiguous-ownership item (AI Preferences, C-041 vs C-042), 0 circular ownership; Release A2 assessed Ready with Observations (governance-decision sense only, not implementation-closure) | N/A | 2026-08-01 | Repository Owner, Architecture Governance |
| WP-09-BUSINESS-VALUE-ASSESSMENT | WP-09 — Business Value & Scope Validation Assessment | Governance | `architecture/06-Reviews/WP-09-BUSINESS-VALUE-ASSESSMENT.md` | Implementing session (business value validation, per repository-owner instruction) | Advisory review artifact, same class as `RELEASE-A2-AI-CONFIGURATION-GOVERNANCE-REVIEW`/`AI-CONFIGURATION-TRACEABILITY-MATRIX` — not an IRA, not an ADR, not a Work Package, creates no capability, modifies no architecture | Complete — assessed `IRA-009`'s disclosed 3-of-6 ERB exclusion against `CAP-001`/`PRODUCT-MILESTONE-ROADMAP` business-value evidence; found both Critical-rated deliverables (Enter, Switch) fall in the excluded set; recommended proceeding at `IRA-009 §4.8`'s scope with explicit partial-realization disclosure, plus flagging the unscheduled Access Evaluation `TierResolver` gap (now blocking 3 Work Packages) as its own scheduling question | N/A | 2026-08-01 | Repository Owner, Architecture Governance |
| PLATFORM-DEPENDENCY-ASSESSMENT-TIERRESOLVER | Platform Dependency Assessment — Access Evaluation TierResolver | Governance | `architecture/06-Reviews/PLATFORM-DEPENDENCY-ASSESSMENT-TIERRESOLVER.md` | Implementing session (platform dependency validation, per repository-owner instruction) | Advisory review artifact, same class as `WP-09-BUSINESS-VALUE-ASSESSMENT`/`RELEASE-A2-AI-CONFIGURATION-GOVERNANCE-REVIEW` — not an IRA, not an ADR, not a Work Package, creates no capability, modifies no architecture, modifies no roadmap | Complete — traced the unresolved Access Evaluation `TierResolver` across WP-05, WP-RTA-001, WP-08, WP-09 (17 files); found the dependency systemic (root cause: incomplete implementation of already-approved RTA-001 architecture, with no Work Package/Release/roadmap item currently owning its resolution); no current Milestone/Release exit criterion blocked; recommended registering it as a single, named, roadmap-visible platform dependency (Option 3/5), resolution mechanism deferred to a separate future decision | N/A | 2026-08-01 | Repository Owner, Architecture Governance |
| SER-001 | Strategic Enhancement Register | Governance | `architecture/06-Reviews/SER-001_Strategic_Enhancement_Register.md` | Repository Owner / Engineering Governance | Governance Registry (same class as `TECH-DEBT.md`) | Active | N/A (living register, 63 entries — Status corrected 2026-08-03 for `SE-002`/`SE-009`/`SE-011`/`SE-012`/`SE-013` (stale after WP-10's own closure) and `SE-035` (classification note added — correctly out of both `IRA-009`/`IRA-010`'s own reviewed scope), found by the Release B Independent Certification and Readiness Assessment) | 2026-08-03 (corrected) | All engineering roles, Repository Owner |
| ENTERPRISE-EXPERIENCE-REALIZATION-STRATEGY | Enterprise Experience Realization Strategy | Governance | `architecture/06-Reviews/ENTERPRISE-EXPERIENCE-REALIZATION-STRATEGY.md` | Implementing session (Implementation Methodology v2.0 Establishment, per repository-owner instruction) | Implementation planning artifact — process document, not a canonical specification; synthesizes `PE-001`/`SD-001`/`DS-001`, redefines neither | Active | N/A | 2026-08-02 | Implementers, Reviewers |
| EXECUTIVE-COGNITION-REALIZATION-STRATEGY | Executive Cognition Realization Strategy | Governance | `architecture/06-Reviews/EXECUTIVE-COGNITION-REALIZATION-STRATEGY.md` | Implementing session (Implementation Methodology v2.0 Establishment, per repository-owner instruction) | Implementation planning artifact — process document; synthesizes `PE-001` Chapters 12/16/22-24, redefines neither | Active | N/A | 2026-08-02 | Implementers, Reviewers |
| HISTORICAL-SCREEN-REALIZATION-MATRIX | Historical Screen Realization Matrix | Governance | `architecture/06-Reviews/HISTORICAL-SCREEN-REALIZATION-MATRIX.md` | Implementing session (Implementation Methodology v2.0 Establishment, per repository-owner instruction) | Implementation planning artifact — classifies every historical UI concept KEEP CONCEPT/EVOLVE CONCEPT/MERGE CONCEPT/RETIRE CONCEPT against business intent and current canonical state | Complete — 14 historical concepts classified (0 KEEP, 7 EVOLVE, 1 MERGE, 6 RETIRE); no historical concept ignored. Remediated 2026-08-02 — 4 classifications corrected (`F1`, `G2`, `G3`, `I1`) per Independent Validation findings | N/A | 2026-08-02 (remediated) | Implementers, Reviewers |

### Implementation

| Document ID | Document Name | Category | Repository Path | Owner | Canonical Status | Lifecycle Status | Current Version | Last Updated | Primary Audience |
|---|---|---|---|---|---|---|---|---|---|
| Implementation Reports | IMP-REPORT-WP-01 through WP-11, IMP-REPORT-WP-RTA-001 | Implementation | `architecture/05-Implementation/IMP-REPORT-*.md` | Implementing session per WP | Implementation audit trail (not certification, per `CLAUDE.md §19` Implementation Reporting note) | 12 issued (10 Closed [WP-01 through WP-10], 1 Certified-conditions-resolved [WP-RTA-001], 1 Implementation Complete awaiting Gate 1 [WP-11]) | N/A (index of 12 documents) | 2026-08-03 (latest: WP-11, Implementation Complete, not yet committed) | Implementers, Reviewers |
| IMP-REPORT-RELEASE-A1 | Release A1 (Foundation Repairs) Implementation Report | Implementation | `architecture/05-Implementation/IMP-REPORT-RELEASE-A1_Foundation_Repairs.md` | Implementing session | Implementation audit trail (not certification, per `CLAUDE.md §19`) — **intentionally not part of the IMP-REPORT-WP-01…08/RTA-001 family above**, since Release A1 charters no Work Package (same non-WP precedent as `IRA-RELEASE-A`) | Implementation Complete — Certified With Observations, Release Ready | N/A | 2026-08-01 | Implementers, Reviewers, Architecture Governance |
| IMP-REPORT-RELEASE-A2 | Release A2 (Architecture Governance) Implementation Report | Implementation | `architecture/05-Implementation/IMP-REPORT-RELEASE-A2_Governance.md` | Implementing session | Implementation audit trail (not certification, per `CLAUDE.md §19`) — same non-WP precedent as `IMP-REPORT-RELEASE-A1`/`IRA-RELEASE-A`; Release A2 charters no Work Package | Implementation Complete — Certified With Observations, one finding remediated and independently verified per `CLAUDE.md §19.7b`, Release Ready | N/A | 2026-08-01 | Implementers, Reviewers, Architecture Governance |

**Total documents registered above: 70** (14 Architecture + 2 Experience-family entries + 7 Engineering + 2 Design + 42 Governance + 3 Implementation entries [the WP-01…09/RTA-001 family row, `IMP-REPORT-RELEASE-A1`, and `IMP-REPORT-RELEASE-A2`] — recounted directly against §8's own rows; the count reached 60/33 Governance following WP-09's own Gate 1/2/4/5 closure (full derivation retained in prior revisions of this line); the Implementation Methodology v2.0 Establishment / WP-10 Planning Authorization pass added `METH-003` (61, Engineering 6→7), `SER-001` (62/34 Governance), `ENTERPRISE-EXPERIENCE-REALIZATION-STRATEGY` (63/35), `EXECUTIVE-COGNITION-REALIZATION-STRATEGY` (64/36), and `HISTORICAL-SCREEN-REALIZATION-MATRIX` (65/37) — `ADR-018` folded into the existing `ADR Index` family row, `IRA-010` folded into the existing `IRA Reports` family row, and the WP-10 charter itself is **not** individually tracked here, per this repository's own established precedent that WP charter `.md` files are tracked via `WPR-001`'s own table only. The WP-10 Implementation Authorization pass kept the total at 65 — `ADR-019` and the now-12-Accepted `IRA-010` folded into their existing family rows, and `IMP-REPORT-WP-10` folded into the existing `Implementation Reports` family row (10→11 issued) — no new DOC-000 row added at that point, consistent with every prior WP's own mid-implementation precedent. The WP-10 Gate 5 Release Readiness Audit pass (2026-08-02) brought the total to 68 (65→68) — three new Governance rows: `CERT-WP-10_Remediation_Verification` (66/38 Governance), `VV-AUDIT-WP-10` (67/39), and `RRA-WP-10` (68/40) — `CERT-WP-10` itself folded into the existing `CERT-*` family row (11→12 issued). The Release B Phase 6 governance synchronization pass (2026-08-03) brought the total to 69 (68→69) — one new Governance row, `RELEASE-B-INTEGRATION-SE009-EDR1-READINESS` (69/41). `PRODUCT-MILESTONE-ROADMAP` and `SER-001` were content-corrected in that same pass (staleness/overclaim fixes found by the Release B Independent Certification and Readiness Assessment), not newly added — did not change that count. **Release C Initiation & WP-11 Planning pass (2026-08-03):** total reached 70 (69→70) — one new Governance row, `RELEASE-C-INITIATION-SUMMARY` (70/42). `IRA-011` folded into the existing `IRA Reports` family row; the WP-11 charter itself is **not** individually tracked here, per the same WP-charter-via-`WPR-001`-only precedent noted above. **WP-11 Implementation Authorization / Gate 1–5 closure pass (this update, 2026-08-03):** total is now 73 (70→73) — three new Governance rows: `VV-AUDIT-WP-11` (71/43), `VV-AUDIT-WP-11_Remediation_Verification` (72/44), `RRA-WP-11` (73/45). `CERT-WP-11` folded into the existing `Independent Review / Certification Reports` family row (13 issued); `IMP-REPORT-WP-11` folded into the existing `Implementation Reports` family row; `IRA-011`'s own Accepted status folded into the existing `IRA Reports` family row — none of these three counted as separate new rows, mirroring every prior WP's own identical precedent (e.g. `RRA-WP-10`'s pass folding `CERT-WP-10` the same way). `WP-REG-001`, `WPR-001`, and `SER-001` were content-corrected (WP-11 CLOSED — CERTIFIED status propagated) in the same pass, not newly added — does not change this count.

---

## 9. Document Ownership Matrix

| Document | Owns | Examples |
|---|---|---|
| ARCH-000 | Every document's own responsibility, ownership, and the Constitutional Document Standard itself | Layer assignment, "what document governs X" resolution |
| CAP-001 | Capability identity, business intent, domain, Primary Specification assignment | C-001–C-151 registry |
| SD-002 | Universal Business Object rules — CDE, BQ, BA, Evidence, lifecycle | Every canonical business object's own shape rules |
| URA-001 | Identity, roles, permissions, approval authorities, assignment/escalation model | `AuthorizationTier`, `URA-001-76` precedence |
| RTA-001 | Runtime execution — Business Activity Engine, Workflow, AI Runtime, Authorization Engine | `WP-RTA-001`'s own governing specification (`§3.8`/`§11`) |
| CMD-001 | Canonical metadata, CBOR, physical data-shape reference | `CBOR-INDEX.md` |
| IMP-001 | Engineering methodology, Business Activity Registry, coding/implementation patterns | Business Activity Contract template |
| WPR-001 | Work Package chartering, capability mapping, sequencing, dependencies, roadmap | `WP-01` → `C-004` assignment |
| WP-REG-001 | Work Package execution status, BA progress, certification status, lifecycle history | "Is WP-05 In Progress or Ready?" |
| DOC-000 | Document inventory, metadata, canonical status, navigation, reading order | "Where do I find the ADR index?" |
| TECH-DEBT | Every disclosed, non-blocking implementation gap | `TD-001`–`TD-104` |
| ADR Index | Every superseding change to a Locked document | `ADR-016` (Authorization Runtime Consolidation) |

Ownership boundaries are exclusive per `CLAUDE.md §15` Golden Rule 12 ("One entity, one definition") — no two documents above own the same concern.

---

## 10. Document Update Matrix

| Document | Updated When |
|---|---|
| CAP-001 | A Capability is added, changes status, or changes Primary Specification |
| PE-001 / PE-001-Cxxx | Enterprise Experience methodology or a capability's own experience blueprint changes |
| IMP-001 | Implementation methodology, coding standards, or the Business Activity Registry changes |
| WPR-001 | A Work Package is chartered, or roadmap/sequencing/dependency information changes |
| WP-REG-001 | A Business Activity completes/is added/removed, or any Work Package lifecycle state changes (see `WP-REG-001 §3`) |
| TECH-DEBT | Debt is introduced or resolved |
| ADR Index | A new Architecture Decision Record is Accepted |
| DOC-000 | A governed document is added, removed, renamed, retired, or changes canonical status; repository organization changes |
| CBOR-INDEX | A new Canonical Business Object is registered |
| Constitutional documents (SD-001–003, URA-001, ERG-001, CMD-001, RTA-001, EIA-001, COM-001, GRC-001, PLT-001, OPM-001, ONT-001) | Only via the Locked-document ADR process, or a certified recertification (per each document's own Freeze Statement) |

---

## 11. Repository Document Hierarchy

```
DOC-000 (Enterprise Documentation Register — this document)
        │
        ▼
   Architecture (ARCH-000, CAP-001, SD-001..003, URA-001, ERG-001,
                 CMD-001, RTA-001, EIA-001, COM-001, GRC-001,
                 PLT-001, OPM-001, ONT-001, DS-001)
        │
        ▼
   Experience (PE-001, PE-001-Cxxx)
        │
        ▼
   Engineering (IMP-001, Master Technical Architecture, METH-001)
        │
        ▼
   Implementation (MDP-001, IMP-REPORT-*, source code, database, infrastructure)
        │
        ▼
   Runtime (RTA-001-specified components — e.g. WP-RTA-001's Authorization Engine —
             consumed by, never redefining, the Architecture layer above)
        │
        ▼
   Governance (WPR-001, WP-REG-001, TECH-DEBT, ADR Index, IRA Reports,
                Independent Review / Certification Reports — tracks and gates
                every layer above; owns none of their content)
```

Each layer consumes the layer above it and never redefines it — this extends `§2`'s own structure diagram (preserved above) with the Runtime and Governance layers `WP-RTA-001`/`WP-REG-001` introduced, without altering `§2`'s own original diagram.

---

## 12. Repository Statistics

*(Recounted directly against §8's own register during the WP-06 Release Readiness Audit, `RRA-WP-06`, 2026-07-31 — the prior figures below (43/5/15/"5 individual reports"/"40 of 43") predated this recount and did not match a direct row count of §8 even before `VV-AUDIT-WP-06`'s row was added; not estimated. Re-recounted during the WP-07 Release Readiness Audit, 2026-07-31, following `VV-AUDIT-WP-07`'s own new row (§8 Governance) and `IMP-REPORT-WP-07`'s own addition to the existing Implementation family entry. Re-recounted again during the WP-08 Release Readiness Audit (`RRA-WP-08`), 2026-08-01: this pass found the prior "47/22 Governance/8 Implementation reports" figures below did not match a direct row count of §8 either — `VV-AUDIT-WP-08`'s own new row had already been added (bringing the true pre-this-pass count to 48/23) but §12 itself had not been updated to reflect it, and `RRA-WP-07`'s own row had never been added to §8 at all despite `RRA-WP-06`'s row existing as established precedent — both gaps corrected in that pass. Recounted again during the Product Milestone Roadmap Governance Synchronization pass, 2026-08-01, following the addition of the `PRODUCT-MILESTONE-ROADMAP` row to §8's Governance category, per repository-owner instruction — `WP-REG-001` and `WPR-001` were explicitly and intentionally left untouched in that same pass, since neither register's schema governs a product-delivery planning artifact. Recounted again during Release A1's own Governance Synchronization phase, 2026-08-01, following the addition of the `IMP-REPORT-RELEASE-A1` row as a second, distinct Implementation-category entry — `WP-REG-001` and `WPR-001` again intentionally left untouched, since Release A1 charters no Work Package. Recounted again following the Release A2 AI Configuration Governance Review, 2026-08-01, after adding `RELEASE-A2-AI-CONFIGURATION-GOVERNANCE-REVIEW` to §8's Governance category — same non-WP precedent, `WP-REG-001`/`WPR-001` again intentionally untouched. Recounted again following the AI Configuration Traceability Matrix validation, 2026-08-01, after adding `AI-CONFIGURATION-TRACEABILITY-MATRIX` to §8's Governance category — same non-WP precedent, `WP-REG-001`/`WPR-001` again intentionally untouched. Recounted again following Release A2's own closure, 2026-08-01, after adding `IMP-REPORT-RELEASE-A2` as a third, distinct Implementation-category entry — `WP-REG-001`/`WPR-001` again intentionally untouched, since Release A2 charters no Work Package. Recounted again following the WP-09 Business Value & Scope Validation Assessment, 2026-08-01, after adding `WP-09-BUSINESS-VALUE-ASSESSMENT` to §8's Governance category, same non-WP, non-IRA, non-ADR advisory-review-artifact class as `RELEASE-A2-AI-CONFIGURATION-GOVERNANCE-REVIEW`/`AI-CONFIGURATION-TRACEABILITY-MATRIX` — `WP-REG-001`/`WPR-001` again intentionally untouched, since this assessment charters no Work Package and modifies no architecture. Recounted again following the Platform Dependency Assessment — Access Evaluation TierResolver, 2026-08-01, after adding `PLATFORM-DEPENDENCY-ASSESSMENT-TIERRESOLVER` to §8's Governance category, same advisory-review-artifact class — `WP-REG-001`/`WPR-001` again intentionally untouched, since this assessment charters no Work Package, modifies no architecture, and modifies no roadmap (per its own explicit STOP condition). Recounted again during the WP-09 Release Readiness Audit (`RRA-WP-09`), 2026-08-02, following the addition of `VV-AUDIT-WP-09`, `VV-AUDIT-WP-09_Remediation_Verification`, and `RRA-WP-09` as three new §8 Governance-category rows (`CERT-WP-09` folded into the existing `CERT-*` family row; `IMP-REPORT-WP-09` folded into the existing Implementation Reports family row, per every prior WP's own established precedent) — `WP-REG-001` and `WPR-001` updated in the same pass, since WP-09 is a genuine Work Package closure, unlike the preceding several non-WP advisory-artifact passes above. Recounted again following Implementation Methodology v2.0 Establishment / WP-10 Planning Authorization, 2026-08-02, after adding `METH-003` (Engineering), `SER-001`, `ENTERPRISE-EXPERIENCE-REALIZATION-STRATEGY`, `EXECUTIVE-COGNITION-REALIZATION-STRATEGY`, and `HISTORICAL-SCREEN-REALIZATION-MATRIX` (four Governance rows) — `WP-REG-001` and `WPR-001` updated in the same pass for WP-10's own chartering, per the same WP-charter trigger `RRA-WP-09`'s own pass used for WP-09. Recounted again during the WP-10 Release Readiness Audit (`RRA-WP-10`), 2026-08-02, following the addition of `CERT-WP-10_Remediation_Verification`, `VV-AUDIT-WP-10`, and `RRA-WP-10` as three new §8 Governance-category rows (`CERT-WP-10` folded into the existing `CERT-*` family row; `IMP-REPORT-WP-10` already folded into the existing Implementation Reports family row during the prior pass) — this same pass also found and corrected a pre-existing, WP-10-unrelated staleness item in `WP-REG-001 §4`/`§10` (WP-09's own closure had never been reflected in that register's aggregate Completed/Certified/Business-Activity counts), not introduced by this pass but surfaced and corrected by it.)*

| Statistic | Value |
|---|---|
| Total Documents Registered | 73 (per §8's own count, including grouped family entries; 70 reflected the Release C Initiation & WP-11 Planning pass; +3 for the WP-11 Gate 1–5 closure pass's own three new rows — `VV-AUDIT-WP-11`, `VV-AUDIT-WP-11_Remediation_Verification`, `RRA-WP-11` (73, Governance 42→45) — `CERT-WP-11`/`IMP-REPORT-WP-11`/`IRA-011`'s own Accepted status each folded into their existing family rows, not counted separately. `WP-REG-001`/`WPR-001`/`SER-001` were content-corrected, not newly added, so neither changes this count.) |
| Architecture Documents | 14 |
| Experience Documents (entries; 14 individual capability blueprints beneath the PE-001-Cxxx family entry) | 2 family entries (16 including the 14 individually-authored blueprints) |
| Engineering Documents | 7 |
| Design Documents | 2 |
| Governance Documents | 41 |
| Implementation Documents (3 entries: the WP-01…09/RTA-001 family row [10 individual reports beneath it], `IMP-REPORT-RELEASE-A1`, and `IMP-REPORT-RELEASE-A2`) | 3 entries (12 individual reports total) |
| Active Documents (Status: Active/AUTHORITATIVE/RELEASED/LOCKED, currently governing) | Not re-derived this pass; denominator is 61 (58 + 3 new Governance rows). The numerator was already left undetermined by `RRA-WP-06`'s own recount (at 45) and is not guessed forward here for the further documents added since — this remains an arithmetic reconciliation, not a full content/canonical-status review |
| Deprecated / Retired Documents | 0 — none found in this pass |
| Canonical Documents (Layer 1 Constitutional, LOCKED or AUTHORITATIVE) | 14 |

---

---

# Enterprise Governance Framework

*(New section. Appended per repository-owner governance decision, 2026-07-30. Explains how the repository's governance registers work together; introduces no new register, renames nothing, and reassigns no existing ownership — every boundary stated below already exists in the register it names, established across `WPR-001`, `WP-REG-001 §2`, and Part II above.)*

## Section 1 — Enterprise Governance Registers

| Register | Governs | Primary Audience | Primary Question Answered |
|---|---|---|---|
| **DOC-000** | Enterprise Documentation Register — repository document inventory, metadata, ownership, canonical status, navigation | All roles | *"What governed documents exist?"* |
| **CAP-001** | Enterprise Capability Register — capability identity, business intent, domain, Primary Specification, status | Product Architecture, all implementers | *"What capabilities exist, and what defines them?"* |
| **WPR-001** | Enterprise Work Package Roadmap — Work Package chartering, capability→WP mapping, sequencing, dependencies, scope | Engineering Governance, Implementers | *"What Work Packages exist, and why?"* |
| **WP-REG-001** | Enterprise Work Package Register — Work Package execution status, Business Activity progress, certification status, lifecycle history | Executives, Architects, Reviewers | *"What is the current implementation state?"* |
| **TECH-DEBT** | Technical Debt Register — every disclosed, non-blocking implementation gap, its severity, and its planned resolution | All engineering roles | *"What engineering obligations remain outstanding, and how urgent are they?"* |
| **ADR Repository** | Architecture Decision Records — every superseding change to a Locked/Frozen document, or a governance decision requiring a formal, citable record | Architects, Reviewers | *"Why was this architectural or governance decision made, and under what authority?"* |
| **IRA Reports** | Implementation Readiness Assessments — whether a Work Package or Business Activity is constitutionally and practically ready to begin implementation | Implementers, Reviewers | *"Is this Work Package ready to be built?"* |
| **Independent Review Reports** | Per-Business-Activity independent review outcomes recorded within each Work Package's own `IMP-REPORT-WP-0X` | Implementers, Certifiers | *"Did this specific Business Activity's implementation pass independent review?"* |
| **Certification Reports** | Independent Work Package Certification — the formal `CERTIFIED` / `CERTIFIED WITH CONDITIONS` / `REJECTED` determination for a Work Package, issued only by a genuinely independent, fresh-context reviewer (`CLAUDE.md §19.7`) | Executives, Auditors | *"Is this Work Package certified, and under what conditions?"* |

**What each register owns, stated plainly (per the format requested):**

- **DOC-000** — Owns: repository documentation inventory and navigation. Question: *"What governed documents exist?"*
- **CAP-001** — Owns: capability identity and business intent. Question: *"What capabilities exist?"*
- **WPR-001** — Owns: Work Package definition, capability mapping, and sequencing. Question: *"What Work Packages exist, and why?"*
- **WP-REG-001** — Owns: Work Package and Business Activity execution status. Question: *"What is the current implementation state?"*
- **TECH-DEBT** — Owns: disclosed, non-blocking engineering gaps. Question: *"What remains outstanding?"*
- **ADR Repository** — Owns: the record of every decision that changed a Locked document or resolved a governance question. Question: *"Why was this decided?"*
- **IRA Reports** — Owns: the readiness gate before implementation begins. Question: *"Is this ready to build?"*
- **Independent Review Reports** — Owns: per-Business-Activity review outcomes. Question: *"Did this pass review?"*
- **Certification Reports** — Owns: the final, independent PASS/FAIL determination. Question: *"Is this certified?"*

## Section 2 — Governance Register Relationships

```
                          DOC-000
                             │
                 Enterprise Documentation
                             │
                             ▼

     CAP-001 ─────────── WPR-001 ─────────── WP-REG-001
        │                    │                    │
   Capabilities           Planning            Execution
        │                    │                    │
        │              (gated by IRA)      (gated by Independent
        │                    │               Review, then
        │                    │               Certification)
        │                    │                    │
        └────────────────────┴────────────────────┘
                             │
                        TECH-DEBT
                             │
                  Engineering Quality
                             │
                             ▼
                     ADR Repository
              (consulted, and written to,
               from any point above where a
               Locked document must change or
               a governance question must be
               formally decided)
```

**Responsibility of each register in this relationship:**

- **DOC-000** sits above the whole framework — it is how any reader (executive, architect, developer, reviewer, or AI coding agent) discovers that the other registers exist at all, and where each one lives.
- **CAP-001** is the root of the implementation side: nothing is built that isn't first a registered Capability.
- **WPR-001** takes a Capability and turns it into a chartered, sequenced Work Package — but only once an `IRA` (Implementation Readiness Assessment) accepts it as ready.
- **WP-REG-001** takes a chartered Work Package and tracks its actual execution — Business Activity by Business Activity — through Independent Review and, ultimately, Certification.
- **TECH-DEBT** sits beneath all three, because any Business Activity in any Work Package, at any stage, may disclose a non-blocking gap into it — it is the shared engineering-quality ledger every register's own execution feeds.
- **ADR Repository** is not a stage in the pipeline but a cross-cutting record consulted from any point in it — a Locked constitutional document changing, or a governance question needing a formal, citable decision (as `WPR-001`, `WP-REG-001`, and `DOC-000`'s own chartering each required one).

## Section 3 — Governance Ownership Matrix

| Governance Concern | Owning Register |
|---|---|
| Enterprise Documentation | → **DOC-000** |
| Capability Definition | → **CAP-001** |
| Work Package Definition | → **WPR-001** |
| Implementation Status | → **WP-REG-001** |
| Engineering Obligations | → **TECH-DEBT** |
| Architecture Decisions | → **ADR Repository** |
| Implementation Readiness | → **IRA Reports** |
| Business Activity Review Outcome | → **Independent Review Reports** |
| Certification | → **Certification Reports** |

No concern above appears twice — each row names exactly one owning register, per the Governance Principles below.

## Section 4 — Governance Principles

- **Every governance concern has exactly one authoritative owner.** (`CLAUDE.md §15` Golden Rule 12: "One entity, one definition.")
- **No governance register duplicates another register.** This is the same discipline applied when `WP-REG-001` was chartered specifically to avoid duplicating `WPR-001`'s own "single source of truth" claim (see `WP-REG-001 §2`) — extended here to the full register set.
- **Every register answers a distinct governance question.** Section 1's own rightmost column is the proof of this — no two rows share a question.
- **Cross-references are encouraged.** A register citing another by name (e.g., `WP-REG-001` citing an `IRA` acceptance, or a `CERT-WP-0X` citing the `ADR`s a Work Package registered) is expected and healthy; a register *restating* another's own content in its own words is not.
- **Duplicate ownership is prohibited.** If two registers ever appear to answer the same question, that is a defect to resolve — by clarifying or narrowing one register's own scope — not a basis for either register's authority to be diluted.
- **Governance updates shall occur as part of normal implementation.** A Work Package's own Business Activity completion, review, and certification are the events that trigger register updates (`WP-REG-001 §3`/`§11`, `DOC-000`'s own update-trigger list, `TECH-DEBT.md`'s own per-entry discipline) — governance bookkeeping is not a separate, deferred activity.
- **Repository governance shall evolve through controlled change.** Every register introduced or re-scoped in this framework was itself the product of an explicit repository-owner decision, several formalized as their own `ADR` (`ADR-016`) — this framework does not exempt itself from that discipline.

## Section 5 — Repository Governance Lifecycle

```
Business Capability
        │
        ▼
     CAP-001                    (Capability registered: identity, business
        │                        intent, domain, Primary Specification)
        ▼
Work Package Planned
        │
        ▼
     WPR-001                    (Work Package chartered: capability mapping,
        │                        sequencing, dependencies — gated by an
        │                        accepted IRA before this step is reached)
        ▼
  Implementation
        │
        ▼
   WP-REG-001                   (Execution tracked: Business Activity by
        │                        Business Activity, current status,
        │                        progress counts, active WP/BA)
        ▼
      Review                    (Per-Business-Activity Independent Review,
        │                        recorded in the Work Package's own
        │                        IMP-REPORT)
        │
        ├─────────────┐
        │             │
        ▼             ▼
   Certified     Technical Debt
        │               │
        │               ▼
        │        Future Resolution        (Tracked in TECH-DEBT until
        │                                   closed by a future Business
        │                                   Activity or Work Package)
        ▼
  WPR-001 / WP-REG-001 updated to Closed
```

**How each register participates:**

- **CAP-001** originates the lifecycle — a Business Capability must be a registered capability before any Work Package may target it.
- **WPR-001** charters the Work Package, recording why it exists and what it depends on, contingent on an **IRA** finding it ready.
- **WP-REG-001** owns the entire Implementation → Review arc — it is the register that answers, at any moment, which Business Activity is active and how many remain.
- **Review** produces two possible outputs per Business Activity or Work Package: a clean pass feeding toward **Certification**, or a disclosed, non-blocking gap feeding **TECH-DEBT** — both are legitimate, expected outcomes, not one being a failure state of the other (`CLAUDE.md §19.8`'s own Technical Debt Management discipline).
- **Certification Reports** close the loop — only a genuinely independent, fresh-context reviewer may issue one (`CLAUDE.md §19.7`), and only after certification does `WPR-001`/`WP-REG-001` record the Work Package as Closed.
- **TECH-DEBT** items that reach **Future Resolution** re-enter the lifecycle as scoped work within a future Business Activity or Work Package — the loop closes back into `WPR-001`'s own sequencing, not around it.

---

*End of DOC-000. For anything not covered here, start at ARCH-000. For the full document inventory, start at Section 8. For how the governance registers work together, start at the Enterprise Governance Framework above.*
