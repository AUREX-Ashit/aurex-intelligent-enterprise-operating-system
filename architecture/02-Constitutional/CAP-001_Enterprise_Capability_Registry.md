# CAP-001 — Enterprise Capability Registry

**Version:** 1.5
**Status:** Architecture Review Complete
**Classification:** Canonical Reference Specification

**Format note:** This document was converted from the original `CAP-001_Enterprise_Capability_Registry.docx` to Markdown as part of ARP-001 Work Package 2 (Capability Ownership Resolution), to enable direct correction of the Primary Specification field for capabilities whose ownership was certified incorrect during the Enterprise Architecture Certification Program (Stage I Batch 2A; Stage I D-004 Methodology extension; Stage I Constitutional Governance Refinement — CMD-001 Ownership Model; EA-2.9 Final Certification Report, §5). Content is preserved verbatim from the source docx except for the Primary Specification corrections documented in the changelogs below; no capability ID, capability name, business intent, domain, or status was altered. The original `.docx` is retained unchanged alongside this file.

---

## CR-3.0 Changelog (Version 1.4 → 1.5)

No Primary Specification reassignment. COM-001, GRC-001, and PLT-001 were certified LOCKED under Constitutional Recertification CR-3.0 (Enterprise Operating System Constitutional Architecture Baseline v2.0). Per ARCH-000 §12.7(1), Primary Specification eligibility requires Locked/Released status, not Draft — the C-020/021/022/024/025 (COM-001), C-110/111/112/113/115 (GRC-001), and C-150/151 (PLT-001) assignments recorded under WP-1A/WP-1B/WP-1C were, until this recertification, prepared and intended but not yet fully eligible. They are now fully eligible; this changelog entry and the bold-entries footnote below record that transition. No capability ID, name, business intent, domain, status, or Primary Specification target changes as a result.

## WP-1C Changelog (Version 1.3 → 1.4)

Two Primary Specification corrections applied: C-150 and C-151 now reference **PLT-001** (Enterprise Platform Architecture), the newly-authored Layer 1 constitutional document these two capabilities' Class C "Constitutional Gap" status was deferred pending (WP-2 Deferred Capabilities). Both capabilities were previously, only tentatively, associated with CMD-001 §23 before the certified CMD-001 Ownership Model Refinement explicitly reverted that association to CMD-001 serving as Constitutional Information Reference only, pending exactly this document. PLT-001 remains in Draft status pending EARB constitutional certification (see PLT-001's Freeze Statement) — this registry correction records the intended, prepared ownership.

## WP-1B Changelog (Version 1.2 → 1.3)

Five Primary Specification corrections applied: C-110, C-111, C-112, C-113, and C-115 now reference **GRC-001** (Governance, Risk & Compliance Architecture), the newly-authored Layer 1 constitutional document these five capabilities' Class C "Constitutional Gap" status was deferred pending (WP-2 Deferred Capabilities). GRC-001 remains in Draft status pending EARB constitutional certification (see GRC-001's Freeze Statement) — this registry correction records the intended, prepared ownership. C-114 was verified unchanged, remaining correctly owned by SD-002, per this work package's explicit instruction not to modify previously certified ownership decisions.

## WP-1A Changelog (Version 1.1 → 1.2)

Five Primary Specification corrections applied: C-020, C-021, C-022, C-024, and C-025 now reference **COM-001** (Commercial & Subscription Architecture), the newly-authored Layer 1 constitutional document these five capabilities' Class C "Constitutional Gap" status was deferred pending (WP-2 Deferred Capabilities). This correction is applied concurrently with COM-001's own authoring; COM-001 remains in Draft status pending EARB constitutional certification (see COM-001's Freeze Statement) — this registry correction records the intended, prepared ownership, consistent with COM-001 already being the document PE-001-C020/021/022/024's own "Primary Specification Reference" fields describe as the missing reference now supplied. C-023 was verified unchanged, remaining correctly owned by URA-001, per this work package's explicit instruction not to modify previously certified ownership decisions.

## WP-2 Changelog (Version 1.0 → 1.1)

Nine Primary Specification corrections applied, each already certified as a Category A (Mechanical Registry Correction) or Category B (Direct Constitutional Repointing) finding — no ADR required, no new constitutional document created, no placeholder owner introduced. Full rationale and evidence for each correction is recorded in the Traceability Matrix of the ARP-001 WP-2 implementation report. Two previously-tentative corrections (C-115, C-150) are explicitly **not** applied here — see that report's Deferred Capabilities section.

---

## 1. Canonical Capability Domains

| ID | Domain | Reserved IDs |
|---|---|---|
| D-001 | Enterprise Foundation | C-001–C-019 |
| D-002 | Commercial & Subscription | C-020–C-039 |
| D-003 | Enterprise Administration | C-040–C-059 |
| D-004 | Enterprise Operations | C-060–C-089 |
| D-005 | Enterprise Intelligence | C-090–C-109 |
| D-006 | Governance, Risk & Compliance | C-110–C-129 |
| D-007 | Collaboration & Engagement | C-130–C-149 |
| D-008 | Enterprise Platform | C-150–C-169 |

---

## 2. Canonical Enterprise Capability Registry

| ID | Capability | Business Intent | Primary Specification | Status |
|---|---|---|---|---|
| C-001 | Identity Management | Manage enterprise identities. | URA-001 | Active |
| C-002 | Access Management | Govern access rights. | URA-001 | Active |
| C-003 | Role & Permission Management | Manage authorization roles and permissions. | URA-001 | Active |
| C-004 | Organization Management | Manage enterprise organizations. | ERG-001 | Active |
| C-005 | Enterprise Structure Management | Maintain enterprise structure. | ERG-001 | Active |
| C-006 | Person Management | Manage enterprise persons. | URA-001 | Active |
| C-007 | Membership Management | Manage enterprise memberships. | URA-001 | Active |
| C-008 | Workspace Management | Provide contextual workspaces. | PE-001 | Active |
| C-020 | Subscription Management | Manage subscriptions. | **COM-001** | Active |
| C-021 | Product & Service Catalog | Manage offerings. | **COM-001** | Active |
| C-022 | Customer & Account Management | Manage customer relationships. | **COM-001** | Active |
| C-023 | Licensing & Entitlement | Manage entitlements. | URA-001 | Active |
| C-024 | Billing Management | Manage billing. | **COM-001** | Planned |
| C-025 | Contract Management | Manage commercial contracts. | **COM-001** | Planned |
| C-040 | Tenant Administration | Administer tenants. | **SD-002** | Active |
| C-041 | Configuration Management | Manage enterprise configuration. | **SD-002** | Active |
| C-042 | Preference & Personalization | Manage enterprise preferences. | PE-001 | Planned |
| C-060 | Business Workflow Management | Coordinate business workflows. | IMP-001 | Active |
| C-061 | Work Management | Manage enterprise work. | **SD-003** | Active |
| C-062 | Case Management | Manage business cases. | IMP-001 | Planned |
| C-063 | Approval Management | Govern approvals. | **SD-003** | Planned |
| C-064 | Review Management | Coordinate reviews. | **SD-003** | Planned |
| C-065 | Decision Management | Support business decisions. | IMP-001 | Planned |
| C-066 | Evidence Management | Manage enterprise evidence. | **SD-002** | Active |
| C-067 | Enterprise Content Management | Manage enterprise content. | SD-001 | Active |
| C-090 | Enterprise Discovery | Understand enterprise context. | EIA-001 | Active |
| C-091 | Knowledge Management | Curate enterprise knowledge. | EIA-001 | Active |
| C-092 | Knowledge Graph Management | Maintain semantic relationships. | EIA-001 | Active |
| C-093 | Enterprise Search | Discover enterprise information. | EIA-001 | Active |
| C-094 | AI Conversation Management | Manage AI interactions. | EIA-001 | Planned |
| C-095 | Enterprise Memory | Maintain enterprise memory. | EIA-001 | Planned |
| C-110 | KPI Management | Manage enterprise KPIs. | **GRC-001** | Active |
| C-111 | Risk Management | Manage enterprise risks. | **GRC-001** | Active |
| C-112 | Compliance Management | Manage compliance. | **GRC-001** | Active |
| C-113 | Policy Management | Govern enterprise policies. | **GRC-001** | Planned |
| C-114 | Audit & Assurance | Manage audits and assurance. | **SD-002** | Active |
| C-115 | Reporting & Disclosure | Publish enterprise reporting. | **GRC-001** | Active |
| C-130 | Enterprise Collaboration | Enable collaboration. | **SD-003** | Active |
| C-131 | Enterprise Communication | Enable communication. | PE-001 | Active |
| C-132 | Enterprise Notifications | Deliver notifications. | **SD-003** | Active |
| C-133 | Activity Stream & Timeline | Provide enterprise activity visibility. | PE-001 | Planned |
| C-150 | Integration Management | Enable interoperability. | **PLT-001** | Active |
| C-151 | Import & Export Management | Exchange enterprise data. | **PLT-001** | Planned |

*(Entries in **bold** were corrected under ARP-001 WP-2, WP-1A, WP-1B, or WP-1C. C-020/021/022/024/025's COM-001 assignment, C-110/111/112/113/115's GRC-001 assignment, and C-150/151's PLT-001 assignment are fully eligible Primary Specification assignments per ARCH-000 §12.7(1), COM-001/GRC-001/PLT-001 each having been certified LOCKED under Constitutional Recertification CR-3.0. All other entries are unchanged from Version 1.0 and either already Confirmed or intentionally deferred — see the WP-2 implementation report's Deferred Capabilities section.)*

---

## 3. Governance

Capability identifiers are immutable. Each capability belongs to one primary domain. New capabilities shall be appended within reserved domain ranges. Deprecated capabilities remain in the registry.

## 4. Conformance

All canonical specifications shall reference CAP-001 for capability identity. Capability names and identifiers shall not be redefined elsewhere.
