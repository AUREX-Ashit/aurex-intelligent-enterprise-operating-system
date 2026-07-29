# ERG-001: Enterprise Structure & Relationship Management (ESRM)
### Version 2.0 — GOLD STANDARD (Supersedes v1.0 Draft)

**Status:** LOCKED
**Scope:** Defines the canonical Enterprise Relationship Graph (ERG) — nodes, relationships, views, financial consolidation, and node-based authorization — within Aurex.
**Companion documents:** SD-001, SD-002, SD-003, URA-001 (all v2.0/v2.1, locked)
**Governing framework:** Aurex Blueprint v2.1 — 39 Laws, 39 Screens, Two Journeys, Three Layers, One Platform

---

## Changelog from v1.0 Draft

| Fix | Detail |
|---|---|
| **ESG generalized out of the foundational architecture** | v1.0 embedded ESG as one of five permanent view types in the canonical model diagram itself, in two formal Architectural Decision Records (AD-004, AD-005), and as the canonical worked example for an entire permission-scope category. This was not fixable by renaming — the whole "Enterprise Views" taxonomy is now genuinely generalized: any tenant may configure any number of named reporting views (Legal, Financial, Operating, Management, Customer, and any custom view including a Regulatory & Resilience Reporting View) with **none hardcoded into the canonical model**. |
| **Precedence conflict with URA-001 resolved** | v1.0's Node Permission Assignment (five inheritance scopes) had no stated relationship to URA-001-76's Authorization Resolution Precedence. Resolved jointly in both documents: node-based access always resolves to an effective Domain Permission that feeds URA-001-76's existing chain — it is never a parallel authority. |
| **EnterpriseView reconciled with SD-002-014** | v1.0 reinvented One Truth, Multiple Views specifically for the graph without stating its relationship to SD-002's generic multi-view consumption principle. EnterpriseView is now stated explicitly as a graph-specific *specialization* of SD-002-014, not a parallel mechanism. |
| **Consolidation method decoupled from ownership relationship** | v1.0 stored financial consolidation method as an attribute of the OWNS relationship, coupling two facts that change on independent timelines under independent authorities. Consolidation method is now its own temporal, policy-governed object. |
| **Graph cycle detection added** | New principle requiring configuration-time rejection of ownership cycles, consistent with URA-001-94a's escalation cycle-detection precedent. |
| **Membership-to-Node linkage added (joint fix with URA-001 v2.1)** | URA-001's Membership object had no reference to EnterpriseNode. URA-001-17b now requires every Membership to declare a home node; ERG-001 states the corresponding graph-side contract below. |
| **TraversalPolicy separated from RelationshipType** | A customer defining a new relationship type no longer simultaneously commits to its access-propagation behavior — these are now independently governed, matching the Domain Admin/Security Admin separation already established in URA-001. |
| Language purge | All remaining ESG/CSRD/BRSR/ISSB/GRI/Carbon examples replaced per the binding substitution table, beyond the structural fix above. |
| Format | Compact prose per section, full treatment for fixed/new content — matching the efficient format used for SD-003 and URA-001. |

---

## SECTION 1: Purpose & Universal Design Principles

ESRM provides the canonical foundation for representing, governing, and evolving enterprise structures within Aurex as a metadata-driven Enterprise Relationship Graph (ERG) — modeling any organizational ecosystem (legal structures, operating models, financial consolidation, management hierarchies, supply chains, shared services, brands, joint ventures, franchises, alliances, regulatory boundaries, geographic structures, and future constructs not yet known) without future schema redesign.

**ERG-001-01 [amended]: The ERG Is Enterprise Infrastructure, Not an Application Feature**

*(Amended — v1.0's purpose statement listed "ESG Reporting Scopes" as a named platform capability alongside Financial Consolidation and Workflow Routing. Corrected to describe the capability generically.)*

All platform capabilities consume enterprise context through the ERG rather than implementing their own structural models — this includes User Access & Authorization (URA-001), Regulatory & Resilience Reporting, Financial Consolidation, Materiality Assessments, KPI Management, Evidence Collection, Workflow Routing, Benchmarking, AI Discovery, and Analytics. No specific reporting framework, including any single regulatory or voluntary disclosure regime, is named as a foundational capability — every reporting boundary is a configured instance of the generic Enterprise View mechanism (Section 6), never a hardcoded platform feature.

**Foundational Principles (V1–V8, retained from v1.0):** one canonical graph exists (V1); views are projections, never independent structures (V2); views are metadata-driven and customer-configurable (V3); multiple views coexist simultaneously (V4); views support effective dating and versioning (V5); authorization may be view-specific (V6); views support graph traversal constraints (V7); adding a new view never requires schema redesign (V8).

---

## SECTION 2: Canonical Enterprise Relationship Graph — Conceptual Model

The ERG is a directed graph of EnterpriseNodes connected by EnterpriseRelationships, with no assumed hierarchy. **AD-001 (Everything Is a Node):** no hardcoded entity types (ParentCompany, Subsidiary, Plant, BusinessUnit, CountryOffice) exist in the schema — every enterprise construct is an EnterpriseNode carrying a metadata-driven NodeType. This was chosen over hardcoded entity classes specifically to avoid schema proliferation, industry-specific assumptions, and the recurring cost of future redesign as new organizational constructs emerge.

**AD-002 (Relationships Are First-Class Business Objects):** relationships exist as independent EnterpriseRelationship objects, never as `parent_id` columns — this is what makes multiple parents, joint ventures, and shared services representable at all. **AD-003 (Graphs Over Trees):** the enterprise model is a directed graph, not a hierarchical tree, because real structures (e.g., a 60/40 joint venture with two parent nodes) cannot be represented by a single-parent tree.

---

## SECTION 3: Canonical Domain Model & Core Business Objects

EnterpriseNode, EnterpriseRelationship, and EnterpriseView are the three core business objects defined by this document, each inheriting SD-002's Universal Business Object Model (Identity, Ownership, Lifecycle, Events, Versioning, Evidence, Relationships, Explainability, Search, Bulk Operations, Human-Governed/AI-Assisted, Extensibility — SD-002 Section 2) in full, per SD-002-002 ("No Object Is a Special Case").

**ERG-001-02 [new]: Bounded Context Separation Within EnterpriseNode**

*(New — closes a DDD boundary concern identified in review: v1.0 asked EnterpriseNode to simultaneously serve as MDM golden record, authorization boundary, financial consolidation participant, and reporting-view member — four distinct bounded contexts collapsed into one aggregate.)*

EnterpriseNode carries a stable, shared identity reference consumed by four independently-governed extension contexts: **Structural Identity** (NodeType, hierarchy position, lifecycle — governed by Corporate Admin/Company Steward), **Authorization** (NodePermissionAssignment — governed by Security Admin per URA-001), **Financial Consolidation** (consolidation method — governed by Finance per Section 7 below), and **Reporting Views** (view membership — governed by Domain Admins per view). A change driven by one context's need (e.g., a new authorization requirement) must never require a corresponding change to another context's data (e.g., financial consolidation) purely because they share the same node — each context extends the node through its own metadata namespace, never through shared mutable fields.

---

## SECTION 4: Enterprise Node Architecture

Every EnterpriseNode carries: node identity, NodeType (metadata-driven — Subsidiary, Plant, Business Unit, Cost Center, Brand, Joint Venture, Shared Service Center, or any customer-defined type), lifecycle state, effective dates, version history, and audit trail — per SD-002's universal object model. NodeTypes are customer-extensible without code change, consistent with URA-001-11 (Everything Is Metadata Driven).

**ERG-001-03 [new]: Node-to-Membership Linkage — the ERG Side of URA-001-17b**

*(New — the graph-side half of the joint fix with URA-001 v2.1. URA-001-17b requires every Membership to declare a `home_node_id`; this principle states ERG-001's corresponding obligation.)*

Every EnterpriseNode that can serve as a membership's organizational home must be addressable and resolvable at the time a Membership is created — the ERG exposes a lookup capability returning valid candidate home nodes for a given Organization, and rejects a Membership creation request that references a node outside that organization's graph or a node in a non-ACTIVE lifecycle state. Home node assignment is distinct from, and evaluated independently of, any NodePermissionAssignment the same membership may separately hold (Section 9) — a person's organizational home (where they sit) and their granted access (what they can see or do) are two different facts about the same membership, never conflated into one field.

---

## SECTION 5: Enterprise Relationship Architecture

EnterpriseRelationship connects two or more EnterpriseNodes with a typed, metadata-driven relationship (OWNS, PARTIALLY_OWNS, JOINT_VENTURE_WITH, REPORTS_TO, SUPPORTS, MANAGES, SUPPLIES_TO, SHARES_SERVICES_WITH, or any customer-defined type), each carrying effective dates, ownership percentage where applicable, and full audit history.

**ERG-001-04 [new]: TraversalPolicy Is Independently Governed From RelationshipType**

*(New — closes a gap identified in review: v1.0 coupled a relationship type's business meaning to its authorization-propagation behavior, forcing whoever defines a new relationship type to simultaneously decide access rules — a different governance decision requiring a different authority.)*

Defining a new RelationshipType (a Domain Admin or Corporate Admin action, describing business meaning) is independent of defining its TraversalPolicy (a Security Admin action, describing whether and how the relationship propagates authorization, per Section 9). A RelationshipType may exist with no TraversalPolicy defined yet, defaulting to NODE_ONLY (no propagation) until a Security Admin explicitly configures otherwise — new business relationships are never accidentally access-propagating by default.

**ERG-001-05 [new]: Ownership Cycle Detection Is Mandatory at Configuration Time**

*(New — closes a gap identified in review: v1.0 permitted multi-parent structures with no stated safeguard against a genuine ownership cycle, e.g., A owns 30% of B, B owns 40% of C, C owns 20% of A.)*

Before an OWNS or PARTIALLY_OWNS relationship is activated, the platform validates that adding it does not create a cycle in the ownership sub-graph. A cyclical ownership configuration is rejected at creation time with the specific cycle path shown to the requesting Domain Admin — it is never discovered later as a traversal or consolidation calculation failure. This is the ERG-specific instance of the same class of safeguard URA-001-94a requires for escalation chains.

---

## SECTION 6: Enterprise Views & Contextual Projections

**ERG-001-06 [substantially amended]: Enterprise Views Are Fully Generic — No View Type Is Hardcoded**

*(Substantially amended. This is the core structural fix. v1.0's canonical model diagram named five permanent view types including ESG View as a structural sibling of Legal, Financial, Operating, and Management views — embedded in the model itself, not left as configuration. Corrected below.)*

The canonical model is: **Enterprise Relationship Graph → [customer-configured Enterprise Views]** — no specific view is named in the canonical model. A tenant configures whichever views their reporting and operational needs require. Common configured views include Legal, Financial, Operating, Management, Customer, and — as one configurable instance among many, never a named architectural citizen — a **Regulatory & Resilience Reporting View**, which a tenant may populate with whatever regulatory or voluntary disclosure scope applies to them (financial regulatory reporting, safety and environmental compliance reporting, or any other externally-mandated or voluntarily-adopted reporting boundary). **This principle is falsifiable and testable: if any future version of this document, or any implementation built from it, hardcodes a specific named view type into a diagram, a database enum, or a canonical example, that is a violation of this principle regardless of which view type is hardcoded.**

**ERG-001-07 [amended]: EnterpriseView Is a Graph-Specific Specialization of SD-002's One Truth, Multiple Views**

*(Amended — closes a gap identified in review: v1.0 reinvented SD-002-014 specifically for the graph without stating the relationship between the two.)*

EnterpriseView is not a parallel mechanism to SD-002-014 (One Truth, Multiple Views) — it is that same universal principle specialized for graph traversal: where SD-002-014 governs how any business object is projected into different consumption contexts (Finance View, Board Dashboard, Annual Report), EnterpriseView governs specifically how the *graph's traversal rules* differ per context (which relationships participate, which nodes are visible, per view). An implementation must use one underlying view-projection engine for both — SD-002-014's general mechanism, with EnterpriseView supplying the graph-specific traversal-constraint parameters, never two separately-built projection systems.

EnterpriseView (retained from v1.0) specifies: which relationships participate, which nodes are visible, traversal rules, and business semantics — as a business object inheriting SD-002's universal model in full, supporting effective dating, versioning, and view-specific authorization (V5, V6 above).

---

## SECTION 7: Financial Consolidation Architecture

Ownership and financial consolidation are separate concepts. Supported consolidation methods: FULL_CONSOLIDATION, PROPORTIONAL_CONSOLIDATION, EQUITY_METHOD, EXCLUDE.

**ERG-001-08 [amended]: Consolidation Method Is Its Own Temporal Object, Not a Relationship Attribute**

*(Amended — closes CDF-3 from review: v1.0 stored consolidation method as an attribute of the OWNS relationship, coupling two facts — ownership structure and consolidation treatment — that change on independent timelines under independent authorities. A company can cross a control threshold and move from equity method to full consolidation with zero change to the underlying ownership percentage.)*

Consolidation method is modeled as its own effective-dated, versioned business object — `ConsolidationDetermination` — referencing the relevant OWNS or PARTIALLY_OWNS relationship but carrying its own lifecycle, effective dates, and approval history, governed by Finance (Domain Owner) rather than whoever manages the underlying ownership relationship. This supports IFRS, local GAAP equivalents, and any other consolidation framework simultaneously, each potentially reaching a different consolidation determination for the same ownership relationship at the same point in time — a legitimate, common real-world scenario v1.0's coupled model could not represent.

Regulatory and voluntary reporting scope (e.g., a Regulatory & Resilience Reporting View's boundary, per Section 6) is likewise independent of both ownership and consolidation method, and must never be automatically inferred from either — it is its own explicit business decision, configured through the same Enterprise View mechanism.

---

## SECTION 8: Temporal Model, Versioning & Auditability

Every ERG object (Node, Relationship, View, ConsolidationDetermination, NodePermissionAssignment) supports effective dates, version numbers, lifecycle states, audit trails, and historical reconstruction, per SD-002's universal temporal model (SD-002-011).

**ERG-001-09 [new]: Retroactive Correction Is Distinct From Prospective Change**

*(New — closes a gap identified in review: v1.0's temporal model addressed only prospective change — e.g., ownership changing going forward from today — with no stated treatment for retroactive correction, e.g., discovering that a recorded ownership percentage was wrong as of a past date.)*

A prospective change creates a new effective-dated version starting today or a future date, leaving history untouched. A retroactive correction is a distinct, explicitly-flagged operation that amends what was true as of a past date — it requires a stated reason, an approval per Section 9's governance model, and produces an audit record showing both the original (now-corrected) historical value and the corrected value, with both remaining permanently visible. Historical reports generated before a retroactive correction are never silently altered; they carry a flag indicating a subsequent correction exists and is reachable on demand, consistent with SD-002's explainability principle.

---

## SECTION 9: URA-001 Integration — Node-Based Access Control & Inheritance

The ERG serves as the canonical authorization boundary for Aurex, extending — never replacing — URA-001's identity and role model. Node-Based Authorization principles U1–U10 (retained from v1.0): EnterpriseNode is the fundamental authorization boundary; permissions are granted against nodes, not organizational trees; inheritance policies are metadata-driven; access propagation is view-aware; multiple-parent structures are supported; temporal states reconstruct historical permissions; authorization decisions are fully auditable; customer-specific inheritance requires no code change; relationship semantics influence propagation (now governed independently per ERG-001-04); access control supports both graph traversal and explicit assignment.

**ERG-001-10 [amended]: Node Permission Assignment Resolves Into URA-001's Existing Precedence Chain**

*(Amended — this is the resolution to CDF-1, the critical precedence conflict identified in review, fixed jointly with URA-001 v2.1's amended URA-001-76.)*

NodePermissionAssignment (membership → role → node → permission scope) is not a fourth, competing authorization system. A node-based grant — resolved through NODE_ONLY, INCLUDE_DESCENDANTS, INCLUDE_ANCESTORS, VIEW_CONSTRAINED, or CUSTOM_TRAVERSAL — always resolves to an **effective Domain Permission** for the object in question before URA-001-76's precedence chain (Named User > Group > Approval Authority > Business Role > Domain Permission) is evaluated. A Named User's direct object-level assignment therefore always overrides an inherited node-based grant, exactly as it would override any other Domain Permission — node-based access is the weakest, most-easily-overridden layer of the same single precedence chain, never a parallel authority requiring separate reconciliation logic.

Permission Scope Model (retained from v1.0, generalized examples): NODE_ONLY (access limited to the assigned node only — e.g., a Plant Manager assigned to Plant A); INCLUDE_DESCENDANTS (access to the assigned node and all its descendants — e.g., a Global CFO assigned to the Global Enterprise node); INCLUDE_ANCESTORS (access to the assigned node plus its reporting chain — e.g., a Regional Auditor); VIEW_CONSTRAINED (access limited to nodes visible within a specific Enterprise View — e.g., a Domain-specific reporting lead scoped to their configured view); CUSTOM_TRAVERSAL (customer-defined traversal semantics, e.g., following only SUPPORTS relationships for a shared-services team).

---

## SECTION 10: Metadata Extension Framework & Customer Configurability

NodeTypes, RelationshipTypes, TraversalPolicies (now independently configurable per ERG-001-04), Enterprise Views (now fully generic per ERG-001-06), and validation rules are all metadata-driven, extensible without code change, and subject to the same Customer Extensions Without Global Pollution rule SD-002-006 establishes for every business object.

---

## SECTION 11: Technical Architecture, Storage Model & Graph Query Patterns

PostgreSQL serves as the system of record, using recursive CTEs for graph traversal, materialized views for performance-sensitive aggregate queries, Redis for caching, and event-driven integration with the rest of the platform. Graph database projections remain an explicitly optional future evolution path.

**ERG-001-11 [new]: A Stated Trigger for Graph Database Migration**

*(New — closes a gap identified in review: v1.0's "optional future graph database" had no stated trigger, and "optional future" without a trigger tends to never happen until a production incident forces it.)*

The platform monitors three concrete thresholds against the current PostgreSQL-based implementation: average traversal depth exceeding 6 hops in production queries, total node count exceeding 500,000 per tenant, or P95 traversal query latency exceeding a stated performance budget (consistent with SD-001-083's performance budget principle) for two consecutive review periods. Crossing any threshold triggers a mandatory architecture review of graph database migration — this is a scheduled decision point, not an indefinitely deferred option.

---

## SECTION 12: Design Decisions, Architectural Trade-offs & Future Evolution

**Architectural Decision Records AD-001 through AD-003 (retained, see Sections 2 above).**

**AD-004 [amended]: One Truth, Multiple Views — Generic, Not Enumerated**

*(Amended — see ERG-001-06. The decision itself remains correct; only the earlier draft's enumeration of specific view types, including ESG Views, as permanent architectural elements is removed.)* The platform maintains one canonical Enterprise Graph with any number of customer-configured views, rejecting separate organizational structures per view (data duplication, governance conflicts, reconciliation effort, inconsistent enterprise truths) in favor of unified governance, traceability, and consistency — with no specific view type named as foundational.

**AD-005 [amended]: Ownership, Control, Management, Consolidation, and Reporting Scope Remain Independent Concepts**

*(Amended — see ERG-001-08. "ESG Reporting Scope" as a named concept is replaced with the generic principle it was a special case of.)* Ownership, control, management, financial consolidation method, and reporting scope (of any kind — financial regulatory, safety, environmental, or any other externally-mandated or voluntary disclosure boundary) are five independently-governed concepts. None is inferred from another. This supports IFRS, local GAAP equivalents, and any current or future reporting framework simultaneously, without the platform ever assuming that a company's consolidation treatment, control structure, or reporting scope for one framework determines its treatment under another.

---

## Full Principle Index

| Range | Section |
|---|---|
| ERG-001-01 (amended) | Section 1 — Purpose & Universal Design Principles |
| — | Section 2 — Canonical ERG Conceptual Model (AD-001–003, unchanged) |
| ERG-001-02 (new) | Section 3 — Canonical Domain Model & Core Business Objects |
| ERG-001-03 (new) | Section 4 — Enterprise Node Architecture |
| ERG-001-04, 05 (new) | Section 5 — Enterprise Relationship Architecture |
| ERG-001-06, 07 (amended) | Section 6 — Enterprise Views & Contextual Projections |
| ERG-001-08 (amended) | Section 7 — Financial Consolidation Architecture |
| ERG-001-09 (new) | Section 8 — Temporal Model, Versioning & Auditability |
| ERG-001-10 (amended) | Section 9 — URA-001 Integration |
| — | Section 10 — Metadata Extension Framework (unchanged) |
| ERG-001-11 (new) | Section 11 — Technical Architecture & Storage Model |
| AD-004, AD-005 (amended) | Section 12 — Design Decisions & Trade-offs |

**Total: 11 numbered fixes/additions across 9 of 12 sections. 3 sections (2, 10, and the retained AD-001–003) required no change.**

---

## Freeze Statement

ERG-001 v2.0 is ready for lock. The structural ESG-embedding problem — the most severe finding across every Aurex architecture document reviewed to date — is resolved at the root: Enterprise Views are now fully generic, with no view type named in the canonical model, and the falsifiable test in ERG-001-06 is designed to prevent this class of defect from recurring in any future version. The precedence conflict with URA-001 is resolved jointly in both documents — node-based access is confirmed to feed URA-001-76's existing chain, never to compete with it. The EnterpriseView/SD-002-014 relationship is now explicit. Consolidation method is decoupled from ownership. Cycle detection, retroactive-correction handling, TraversalPolicy independence, and a concrete graph-database migration trigger are all newly stated.

**The membership-to-node linkage identified during this joint review is fixed in both documents simultaneously** — URA-001 v2.1's URA-001-17b and this document's ERG-001-03 are two halves of one integration contract and must be read together.

**All five foundational documents — SD-001, SD-002, SD-003, URA-001 v2.1, and ERG-001 v2.0 — are now mutually consistent and ready to freeze as a coherent architecture.**
