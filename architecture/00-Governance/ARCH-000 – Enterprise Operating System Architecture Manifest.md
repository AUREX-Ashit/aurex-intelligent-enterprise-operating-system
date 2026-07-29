# ARCH-000 – Enterprise Operating System (EOS) Architecture Manifest

**Version:** 1.6  
**Status:** AUTHORITATIVE  
**Classification:** Architecture Governance  
**Audience:** Enterprise Architects, Product Architects, Solution Architects, Developers, AI Coding Agents (Claude Code, GitHub Copilot, Cursor, ChatGPT, etc.)

---

# 1. Purpose

This document is the **authoritative entry point** to the Aurex Enterprise Operating System (EOS) architecture.

It establishes the constitutional map of the architecture by defining:

- the architecture documents that govern the platform
- the responsibility of each document
- the relationship between documents
- the recommended reading sequence
- the ownership boundaries for every architectural concern
- the structural, lifecycle and evolution standard every constitutional document must satisfy (Section 12)

This document **does not define architecture**.

Instead, it defines **where architecture is defined**.

Every human contributor and every AI coding agent **must read this document before consuming any other architecture document.**

---

# 2. Enterprise Operating System Philosophy

The Enterprise Operating System is governed through a collection of **constitutional architecture documents**.

Each document owns **exactly one architectural concern**.

No architecture document may redefine or duplicate another document's responsibility.

Engineering documents consume constitutional architecture.

Implementation documents consume engineering architecture.

---

# 3. Architecture Classification

The Enterprise Operating System documentation is organized into four architecture layers.

---

## Layer 1 — Enterprise Constitutional Architecture

These documents define the Enterprise Operating System.

| Document | Architectural Responsibility |
|------------|--------------------------------------------|
| CAP-001 | Capability Identity, Canonical Capability Name and Business Intent |
| Complete Blueprint | Enterprise Philosophy, Enterprise Operating Model, Enterprise Intelligence Vision and Constitutional Principles |
| SD-001 | Enterprise Presentation Architecture |
| DS-001 | AUREX Design System — Enterprise Visual Design Architecture |
| SD-002 | Canonical Business Object Architecture |
| SD-003 | Enterprise Interaction Architecture |
| URA-001 | Enterprise Identity, Authorization and Assignment Architecture |
| ERG-001 | Enterprise Structure and Relationship Architecture |
| CMD-001 | Canonical Metadata Architecture |
| RTA-001 | Runtime Architecture and Enterprise Execution |
| EIA-001 | Enterprise Intelligence Architecture |
| COM-001 | Commercial & Subscription Architecture |
| GRC-001 | Governance, Risk & Compliance Architecture |
| ONT-001 | Enterprise Ontology Architecture — semantic relationship taxonomy only; not a capability domain |
| PLT-001 | Enterprise Platform Architecture |
| OPM-001 | Enterprise Operating Model Architecture — constitutional cross-domain collaboration only; not a capability domain |

---

## 3a. Note on Enterprise Operating Model Terminology (ARP-001 WP-1D)

Complete Blueprint's row above lists "Enterprise Operating Model" among its architectural responsibilities, referring to its own narrative content (§14.0 "Two-Tier Sacred 12 Architecture & Operating Model," and the Operating Model dimension of the Enterprise DNA profile). That narrative content is not redefined, restated, or superseded by OPM-001. Per the certified pattern already applied throughout this program (formalizing rich, undecomposed Blueprint narrative into constitutional-grade principles without altering the Blueprint itself), OPM-001 is the constitutional-grade formalization of a different, related concept: how the Enterprise Operating System's already-owned constitutional domains collaborate, not the Blueprint's screen architecture or DNA-profile dimension. This is an observation about existing terminology, not a change to Complete Blueprint's own content — no responsibility is reassigned by this note.

---

## Layer 2 — Enterprise Experience Architecture

These documents define how enterprises experience the Enterprise Operating System.

| Document | Architectural Responsibility |
|------------|--------------------------------------------|
| PE-001 | Canonical — Enterprise Experience Foundation & Methodology |
| PE-001-Cxxx | Capability-Specific Enterprise Experience Specifications |

PE-001-Cxxx specifications conform to PE-001's Enterprise Experience methodology and derive capability identity and business intent from CAP-001, never redefining either. PE-001-C005 (Enterprise Structure Management) is the current Gold Standard reference for capability-level Enterprise Experience engineering.

---

## Layer 3 — Enterprise Engineering Architecture

These documents define how constitutional architecture is engineered.

| Document | Architectural Responsibility |
|------------|--------------------------------------------|
| IMP-001 | Enterprise Engineering & Implementation Playbook |
| Master Technical Architecture | Physical Platform Architecture, Services, Database, APIs and Deployment |

---

## Layer 4 — Implementation Specifications

These documents define engineering execution.

| Document | Architectural Responsibility |
|------------|--------------------------------------------|
| MDP-001 | Master Data Population Specification |

---

# 4. Recommended Reading Order

Architecture should always be read in the following sequence.

| Order | Document |
|--------|----------|
| 1 | CAP-001 – Enterprise Capability Registry |
| 2 | Complete Blueprint |
| 3 | SD-001 – Enterprise Presentation Architecture |
| 4 | DS-001 – AUREX Design System |
| 5 | SD-002 – Canonical Business Object Architecture |
| 6 | SD-003 – Enterprise Interaction Architecture |
| 7 | URA-001 – Universal Role Architecture |
| 8 | ERG-001 – Enterprise Relationship Graph |
| 9 | CMD-001 – Canonical Metadata Architecture |
| 10 | RTA-001 – Runtime Architecture & Execution |
| 11 | EIA-001 – Enterprise Intelligence Architecture |
| 12 | IMP-001 – Implementation Playbook |
| 13 | Master Technical Architecture |
| 14 | MDP-001 – Master Data Population Specification |

---

# 5. Architecture Navigation Matrix

Use this table to identify the authoritative document for any architectural concern.

| If you need to know... | Read... |
|--------------------------|--------------------------------|
| What capabilities exist and their business intent | CAP-001 |
| Why the Enterprise Operating System exists | Complete Blueprint |
| Enterprise Philosophy and Constitutional Principles | Complete Blueprint |
| How enterprise information is presented | SD-001 |
| How the platform's visual language, design tokens, themes, and components are governed | DS-001 |
| What Business Objects exist | SD-002 |
| How enterprise interactions work | SD-003 |
| Identity, Roles and Permissions | URA-001 |
| Enterprise Structure and Relationships | ERG-001 |
| Metadata definitions | CMD-001 |
| Runtime orchestration | RTA-001 |
| Engineering implementation standards | IMP-001 |
| Physical technical implementation | Master Technical Architecture |
| Master data population rules | MDP-001 |
| Enterprise user experience | PE-001 |

---

# 6. Architectural Ownership

Each architectural concern has **one and only one owner**.

| Architectural Concern | Authoritative Document |
|----------------------------|------------------------|
| Capability Identity & Business Intent | CAP-001 |
| Enterprise Philosophy | Complete Blueprint |
| Enterprise Presentation | SD-001 |
| Enterprise Visual Design (AUREX Design System) | DS-001 |
| Enterprise Business Objects | SD-002 |
| Enterprise Interaction | SD-003 |
| Enterprise Identity & Authority | URA-001 |
| Enterprise Context | ERG-001 |
| Enterprise Metadata | CMD-001 |
| Enterprise Runtime | RTA-001 |
| Enterprise Intelligence | EIA-001 |
| Commercial & Subscription | COM-001 |
| Governance, Risk & Compliance | GRC-001 |
| Enterprise Platform | PLT-001 |
| Enterprise Semantic Relationship Taxonomy | ONT-001 |
| Enterprise Operating Model Coordination | OPM-001 |
| Enterprise Experience | PE-001 |
| Enterprise Engineering | IMP-001 |
| Enterprise Technical Implementation | Master Technical Architecture |
| Enterprise Seed Data | MDP-001 |

*(Rows for COM-001, GRC-001, PLT-001, ONT-001, and OPM-001 added under WP-7, Repository Quality & Hygiene, closing the table-completeness observation carried forward from CR-3.0 §3. Each row records ownership already certified under CR-3.0; no ownership is reassigned or newly decided by this addition.)*

---

# 7. Architectural Principles

The Enterprise Operating System is governed by the following architectural principles.

1. Every architectural concern has exactly one owner.

2. Architecture must never be duplicated.

3. Engineering must implement architecture.

4. Implementation must never redefine architecture.

5. Metadata governs platform behavior.

6. Business Activities are the fundamental execution unit of the Enterprise Operating System.

7. Business Objects are the canonical representation of enterprise truth.

8. Runtime orchestration is governed exclusively by RTA-001.

9. Presentation architecture is governed exclusively by SD-001.

10. Constitutional architecture always takes precedence over engineering implementation.

11. Constitutional document structure, lifecycle and evolution are governed exclusively by Section 12 (Constitutional Document Standard).

12. AI remains subordinate to enterprise governance. No AI-generated output is authoritative on its own; it is authoritative only insofar as it carries the Evidence, Provenance, and Confidence properties SD-002 and EIA-001 already require, and remains subject to the human approval and override rules already established by URA-001 and SD-003. Evidence is the foundation of enterprise reasoning, not a downstream justification for it.

---

## 7a. Note on Domain Typology (CAP-001)

CAP-001's eight Business Domains are not architecturally uniform. Some (Enterprise Foundation, Enterprise Intelligence) are vertical, self-contained business territories with their own dedicated constitutional owner (URA-001/ERG-001; EIA-001, respectively). Others (Enterprise Operations, Governance/Risk/Compliance, Collaboration & Engagement) are better understood as groupings of largely cross-cutting behaviors whose constitutional grounding lives in the horizontal rules documents (SD-002, SD-003) rather than in a domain-specific specification. This is an observation about CAP-001's existing structure, not a change to it — no capability, domain, or ownership assignment is altered by this note.

---

## 7b. AI Actor Vocabulary *(formalized per ARP-001 WP-5)*

Four terms are already in constitutional and technical use for AI-related actors. This section reconciles them; it does not rename, merge, or redefine any of them.

| Term | Owning Document | What It Denotes |
|---|---|---|
| **AI Coding Agent** | ARCH-000 §9 | A development-time actor (Claude Code, GitHub Copilot, Cursor, ChatGPT, etc.) that builds or modifies the platform's own repository. Not a runtime or in-product concept. |
| **AI Assistant** | SD-003 §10 ("AI Assistant & Human Interaction Laws") | The in-product AI's interaction behavior toward enterprise users — the constitutional, business-semantics layer definition. |
| **Autonomous Agent Persona** | PE-001 (Persona Model) | The Experience-layer design classification for an autonomous-agent-class user PE-001-Cxxx specifications design experiences for. |
| **AI Runtime Engine** | RTA-001 §13 (AI Runtime) | The runtime component that executes AI processing — consumed by, and never a competing authority over, the business-semantics layer that orchestrates it (the same consumed-runtime relationship RTA-001 already holds with URA-001 for authorization, per ARCH-000 §6 and established certification precedent). |

AI Assistant, Autonomous Agent Persona, and AI Runtime Engine describe **the same underlying in-product AI actor at three architectural layers** — Constitutional/Interaction, Experience, and Runtime, respectively — the same pattern already formalized for Business Object / Enterprise Information Object / CBOR (CMD-001 §26.4b). AI Coding Agent is a distinct, unrelated, development-time-only actor and does not participate in this relationship.

---

## 7c. Enterprise Intelligence & AI Governance Ownership Map *(formalized per ARP-001 WP-5; corrected per ARM-001/AR-001, Architecture Audit Remediation)*

Every AI governance dimension already has either a certified constitutional owner or an explicit, certified deferral. This section assigns ownership; it does not create new governance rules.

| Governance Dimension | Owner | Status |
|---|---|---|
| Evidence-first reasoning | SD-002 §6 (Evidence & Source Intelligence Rules) | Owned |
| Reasoning provenance | EIA-001 Vol. II §12 (Knowledge Asset — Provenance property) | Owned |
| Confidence scoring | EIA-001 Vol. II §12 (Knowledge Asset — Confidence property) | Owned |
| Human approval | URA-001 (Approval Authorities) and SD-003 §6 (Review, Approval & Human Governance Laws) | Owned |
| Human override | SD-003 §6 | Owned |
| Auditability | SD-002 §7 (Event, Lifecycle & Audit Rules) | Owned |
| AI policy boundaries | SD-003 §10 (AI Assistant & Human Interaction Laws) | Partially owned — interaction-level boundaries only |
| Prompt governance | RTA-001 §13.15 (AI Governance) | **Owned** — corrected per ARM-001/AR-001. RTA-001 §13.15 already states the AI Runtime shall support Prompt Governance operationally; this table previously recorded this dimension as Deferred, contradicting RTA-001. RTA-001 §13.15 is unmodified; this table is corrected to match it. |
| Knowledge governance | — | **Deferred.** EIA-001 Vol. I §8.4 explicitly reserves this for a future volume; not established here. RTA-001 §13.15 makes no claim over this dimension, so no contradiction exists here. |
| Memory governance | — | **Deferred.** Same reservation; also consistent with Enterprise Memory's mechanics being deliberately unbuilt (EIA-001 Vol. II). RTA-001 §13.15 makes no claim over this dimension, so no contradiction exists here. |
| Model governance | RTA-001 §13.15 (AI Governance) | **Owned** — corrected per ARM-001/AR-001, same reasoning as Prompt Governance above. |
| Explainability | SD-002-016 (Universal Explainability); SD-001 LAW-26 ("Explainability Is One Click Away") | **Owned** — added per ARM-001/AR-001. RTA-001 §13.15 lists Explainability among the AI Runtime's governance guarantees but is not itself the substantive source; SD-002-016 and SD-001 LAW-26 are the owning definitions this table now cites. |
| Agent-specific governance (distinct from generic AI Governance) | RTA-001 §13.15 (AI Governance) | **Owned — subsumed.** Added per ARM-001/AR-001. No governance dimension distinct from the general AI Governance guarantee above exists for agents specifically; `agent_registry.governing_policy_id` reuses the platform's general governance/confidence mechanism rather than a separate agent-specific policy. This is a clarification of scope, not a new governance rule. |

Deferred dimensions remain open Future Intelligence Capabilities. No placeholder owner has been assigned to Knowledge Governance or Memory Governance.

---

# 8. Architectural Dependency Model

```
Capability Identity & Business Intent (CAP-001)
        │
        ▼
Enterprise Constitution
        │
        ▼
Complete Blueprint
        │
──────────────────────────────────────────────
Enterprise Presentation (SD-001)

Enterprise Visual Design (DS-001)

Enterprise Business Objects (SD-002)

Enterprise Interaction (SD-003)

Enterprise Authority (URA-001)

Enterprise Context (ERG-001)

Enterprise Metadata (CMD-001)

Enterprise Runtime (RTA-001)
──────────────────────────────────────────────
        │
        ▼
Enterprise Experience (PE-001)
        │
        ▼
Capability-Specific Enterprise Experience (PE-001-Cxxx)
        │
        ▼
Implementation Playbook (IMP-001)
        │
        ▼
Master Technical Architecture
        │
        ▼
Implementation Specifications (MDP-001)
        │
        ▼
Engineering Implementation
```

---

# 9. AI Coding Agent Instructions

Every AI coding agent shall follow the process below before generating or modifying code.

## Step 1

Read this Architecture Manifest.

---

## Step 2

Identify the Business Activity being implemented.

---

## Step 3

Identify the required Business Objects.

---

## Step 4

Identify:

- Enterprise Context
- Enterprise Authority
- Enterprise Runtime
- Enterprise Presentation
- Enterprise Interaction

using the appropriate constitutional documents.

---

## Step 5

Generate implementation that conforms to:

- Blueprint
- Constitutional Architecture
- Engineering Standards
- Technical Architecture

---

## Step 6

Never invent architecture.

Never redefine architecture.

Never duplicate architecture.

Always extend the Enterprise Operating System using the constitutional architecture.

---

# 10. Constitutional Documents

The following documents are considered constitutional architecture.

- Complete Blueprint
- SD-001
- DS-001
- SD-002
- SD-003
- URA-001
- ERG-001
- CMD-001
- RTA-001
- EIA-001
- COM-001
- GRC-001
- PLT-001
- ONT-001
- OPM-001

These documents shall not be modified except through formal architectural governance.

All engineering and implementation work must conform to these documents.

The structural standard every document above must satisfy is defined in Section 12 (Constitutional Document Standard).

---

## 10a. Constitutional Baseline Certification Record

**Enterprise Operating System Constitutional Architecture — Baseline v2.0** was certified under **Constitutional Recertification CR-3.0** (Independent Enterprise Architecture Certification Authority / EARB / Chief Enterprise Architect), decision: **CERTIFIED WITH OBSERVATIONS**. This certification transitioned COM-001, GRC-001, PLT-001, ONT-001, and OPM-001 from Draft to LOCKED (ARCH-000 §12.4), completing their entry into Section 10's list above and, for COM-001/GRC-001/PLT-001, satisfying ARCH-000 §12.7(1)'s Locked/Released eligibility requirement for the Primary Specification assignments CAP-001 already recorded for them (CAP-001 CR-3.0 Changelog, Version 1.4 → 1.5). CR-3.0 carried forward four non-blocking observations (ARCH-000 §6 table completeness, legacy Companion-documents convention variance, IMP-001's duplicate §6.22 heading, RTA-001's missing Companion-documents field) — each classified Documentation, Editorial, or Repository Hygiene, none an Architectural Defect, none required to sustain this certification. This record documents the certification event; it does not itself constitute Constitutional Evolution (§12.6) of any cited document's content.

---

# 11. Manifest Governance

This manifest shall be updated whenever:

- a constitutional architecture document is added
- a constitutional architecture document is superseded
- a constitutional architecture document is retired
- a new engineering architecture document is introduced
- a new implementation specification becomes authoritative

The Architecture Manifest shall always remain the first document read by every architect, engineer and AI coding agent.

---

# 12. Constitutional Document Standard

This section defines the structure, lifecycle and evolution standard every document in Section 3 (Layer 1) and Section 10 (Constitutional Documents) already follows. It documents an existing convention; it does not introduce new architecture, terminology, or governance layers.

---

## 12.1 What Is a Constitutional Document

A Constitutional Document is a Layer 1 document (Section 3) that holds sole, non-duplicated authority over exactly one Architectural Concern (Section 6), per Architectural Principle 1 (Section 7).

---

## 12.2 Purpose of a Constitutional Document

A Constitutional Document exists to give one Architectural Concern a single authoritative source of business-domain truth. Engineering documents (Layer 3) implement it; implementation documents (Layer 4) execute it; neither may redefine it (Principles 3, 4 and 10, Section 7).

---

## 12.3 Mandatory Characteristics

Every Constitutional Document shall declare:

- **Document ID**
- **Status** — see 12.4
- **Scope** — one authoritative statement of what the document owns, including an explicit disclaimer of what it does not
- **Purpose** — stated first, before any domain content
- **Domain ownership** — the single Architectural Concern (Section 6) it authoritatively owns
- **Explicit ownership boundaries** — citations to the adjacent documents whose concerns it consumes but never redefines
- **Constitutional principles** — individually addressable, numbered statements (`DOC-ID-NNN`); a document whose domain model spans a large number of top-level sections may rely on structural section numbering alone instead
- **Cross-document references** — explicit citations to every other constitutional document whose concern is touched
- **Freeze Statement** — a closing declaration that the document is ratified and changeable only through Constitutional Evolution (12.6)

This is the pattern already in consistent use across Complete Blueprint, SD-001, DS-001, SD-002, SD-003, URA-001, ERG-001, CMD-001 and RTA-001.

---

## 12.4 Constitutional Lifecycle

- **Referenced** — the document's identifier and Architectural Concern are reserved in this manifest, but the document has not yet been authored (e.g., EIA-001, Section 3).
- **Draft** — authored, not yet ratified.
- **Locked / Released** — ratified and immutable except through Constitutional Evolution (12.6). Both terms denote the same terminal state; "Locked" is used by URA-001, ERG-001, SD-001, SD-002, SD-003, CMD-001 and RTA-001, "Released" by DS-001.
- **Superseded / Retired** — the states already defined in Section 11 for a document that is replaced or withdrawn.

---

## 12.5 Constitutional Ownership

One constitutional concern, one constitutional owner. This is Architectural Principle 1 (Section 7) and the Architectural Ownership table (Section 6), applied to constitutional documents specifically: no constitutional document may describe, redefine, or duplicate an Architectural Concern owned by another.

---

## 12.6 Constitutional Evolution

A Locked/Released Constitutional Document changes only by:

- **CERT correction** — an inline, point-of-fix annotation correcting an error without altering the document's ratified decisions or Freeze Statement (e.g., RTA-001's CERT-010, CMD-001's CERT-007).
- **ADR** (Architecture Decision Record, `architecture/07-Decisions`) — for a substantive change to a document's decisions, ownership, or scope (e.g., ADR-001).
- **Architecture Board approval** — required for both of the above, per Section 10's existing requirement that constitutional documents "shall not be modified except through formal architectural governance."
- **Versioning** — every change increments the document's version and is recorded in its own changelog.

---

## 12.7 Primary Specification Eligibility

A document may serve as a capability's Primary Specification (Section 6, "Capability Identity & Business Intent"; CAP-001) only if it is:

1. a Constitutional Document under this section, in Locked/Released status (12.4) — not Draft or Referenced;
2. the Architectural Concern owner (Section 6) of the business domain in question; and
3. a document that defines that domain's business semantics directly, not one that merely depends on, presents, or implements it.

Per the Layer boundaries already established in Section 3: a Layer 2 Experience document, a Layer 3 Engineering document, or a Layer 4 Implementation document does not become a business domain's Primary Specification by being cited for it. Presentation architecture governs how a domain is displayed, not what the domain is. Engineering architecture governs how a domain is built, not what the domain is. Technical implementation architecture governs where a domain is physically stored, not what the domain is.

---

## 12.8 Guidance for Future Constitutional Documents

A new constitutional document shall follow the pattern already established by Complete Blueprint, SD-001, DS-001, SD-002, SD-003, URA-001, ERG-001, CMD-001 and RTA-001: the mandatory characteristics of 12.3, ownership of exactly one Architectural Concern (Section 6, 12.5), and the lifecycle and evolution mechanisms of 12.4 and 12.6 once ratified. This section names the structure those documents already share; it does not modify or reinterpret the content of any of them.

---

# End of Document

**Document ID:** ARCH-000  
**Document Name:** Enterprise Operating System Architecture Manifest  
**Status:** Authoritative Entry Point