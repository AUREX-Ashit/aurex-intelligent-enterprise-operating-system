# DOC-000 — Enterprise Operating System Documentation Catalogue

**Type:** Repository Navigation Guide (not an architecture, design, or governance specification)
**Status:** Current as of Constitutional Baseline v2.0
**Read time:** ~10 minutes

---

## 1. Purpose

This catalogue is the single entry point into the CorpStage Enterprise Operating System repository. It exists because the repository now spans 20+ registered architecture documents across four layers, and no single document previously told a reader which one to open first.

**How to use it:** find your role in Section 6, or your task in Section 5's "If I want to..." table, and go straight to the named document. Section 3 is the full reference catalogue; consult it when Sections 5–6 don't cover your case.

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

*End of DOC-000. For anything not covered here, start at ARCH-000.*
