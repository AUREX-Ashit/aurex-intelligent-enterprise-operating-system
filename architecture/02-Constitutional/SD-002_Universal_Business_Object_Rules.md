# SD-002: Universal Business Object Rules
### Version 2.2 — GOLD STANDARD (Supersedes v2.1)

**Status:** LOCKED
**Scope:** Defines what business objects are and their universal behaviors across the Aurex Enterprise Intelligence Platform.
**Companion documents:** SD-001 (Screen Design Principles, v2.0 GOLD STANDARD), SD-003 (Interaction Laws)
**Governing framework:** Aurex Blueprint v2.1 — 39 Laws, 39 Screens, Two Journeys, Three Layers, One Platform

---

## Changelog from v2.1

| Fix | Detail |
|---|---|
| Enterprise Intelligence / AI governance cross-reference added (ARP-001 WP-5) | Section 6 (Evidence & Source Intelligence Rules) now explicitly notes that EIA-001 Vol. II §12's Knowledge Asset model (Provenance, Confidence, Freshness, Authority, Lineage) extends this section's Evidence rules into the Enterprise Intelligence domain, and that reasoning provenance and confidence scoring for AI-assisted output are owned by EIA-001 under this section's authority. No existing Evidence rule redefined. |

## Changelog from v2.0

| Fix | Detail |
|---|---|
| BAR/CBOR cross-references added (ARP-001 WP-3) | SD-002-004 (Universal Identity) and SD-002-034/035 (Business Activities) now cite the Business Activity Registry (BAR, IMP-001 §6.22) and Canonical Business Object Register (CBOR, CMD-001 §26) as the registries that operationalize this rule, formalizing an already-anticipated relationship without redefining SD-002's own content. |

## Changelog from v1.0 Draft

| Fix | Detail |
|---|---|
| 11 rule-ID collisions resolved | v1.0 had 222 rule definitions sharing only 211 unique IDs — SD-002-100 through SD-002-110 each named two different rules, because Evidence (Section 6) and Governance/CIL (Sections 7–9) were numbered by independent counters that overlapped. Renumbered sequentially, single counter, zero collisions. |
| Systemic redundancy consolidated | v1.0 stated the same ~15 universal capabilities (Identity, Ownership, Lifecycle, Events, Versioning, Evidence, Relationships, Explainability, Search, Bulk Operations, Human-Governed/AI-Assisted, Extensibility, Future-Proofing) once generically (Section 1), again as "every business object" (Section 2), and again separately for CDEs, BQs, and BAs (Sections 3–5). This is the actual root cause of the ID collisions — independent per-type restatement invites independent per-type numbering. Consolidated into one inheritance contract (Section 2); Sections 3–5 now state only what is genuinely distinctive to CDEs, BQs, and BAs. Total principle count reduced from 182 to 121 with zero loss of substance. |
| Multi-Tenancy & Data Isolation added | v1.0 used the word "tenant" twice in the entire document, with no explicit isolation principle for a platform whose business model is many enterprises on shared infrastructure. New Section 13. |
| SD-001 boundary violation removed | v1.0's "Navigation Structures Are Metadata" (menus, landing pages, quick actions, default views) duplicated SD-001-018. Relocated to SD-001; only the bare configuration-record concept remains here, stripped of screen language. |
| Language purge completed | Removed: "ESG Reports," "Head Of Sustainability," "ABC Manufacturing ESG Team," "ESG Lead," "CSRD" (×2) — replaced per the binding substitution table. |
| Temporal model consolidated | Effective dating was referenced six times across different sections with no single canonical statement. Consolidated into one principle in Section 2, cross-referenced everywhere else. |
| Cross-object data lineage added | Evidence lineage was well-covered within a single object; a new principle extends it explicitly across derived chains (CDE → Report, Activity → CDE → Framework). |
| Retention floor stated | "Governed" and "permanent" retention now carries an explicit stated minimum, configurable upward, never downward without governance approval. |
| CIL conflict-precedence rule added | v1.0 had no rule for what happens when a Company CIL extension and an incoming Industry CIL promotion define the same concept differently. New principle added, and cross-referenced against SD-001 v2.0's identical open item (config-hierarchy precedence) — this is one architectural decision, now resolved once and referenced from both documents. |
| Event sourcing and MDM named explicitly | The underlying concepts existed correctly (SD-002-168 in v1.0 was textbook event sourcing; the canonical/golden-record model was a genuine MDM pattern) but neither term was ever used, making the document harder to find via standard architecture search terms. Now named directly where each concept is defined. |
| Numbering cleaned | Sequential, zero gaps, zero collisions: SD-002-001 through SD-002-121, plus 6 Universal Object Blueprints retained as structural diagrams. |
| Format compressed | v1.0's one-word-per-line list style replaced with compact prose and tables — same substance, roughly 55% shorter. |

---

## SECTION 1: Purpose & Philosophy

SD-002 defines what a business object is, and the behaviors every business object in Aurex must support regardless of its type, industry, customer, or the screen that eventually renders it.

**SD-002-001: Everything Important Is a Business Object**

Traditional enterprise systems model users, tables, forms, and workflows. Aurex models Business Activities, Canonical Data Elements, Evidence, Approvals, Assignments, Reports, Frameworks, Departments, and Events — every one of them a first-class business object, not an application artifact. This is what makes consistency, traceability, reuse, and governance possible across the entire platform rather than per-module.

**SD-002-002: No Object Is a Special Case**

Every business object — a CDE, a Business Question, a Business Activity, an Evidence record, a Report, a Framework — inherits the same universal capabilities defined in Section 2. There is no object type in Aurex that is exempt from identity, ownership, evidence, versioning, events, audit, or governance. Object-type sections (3, 4, 5) define only what is *additional and distinctive* to that type — never a restatement of what Section 2 already guarantees.

**SD-002-003: Objects Must Be Future-Proof**

Every object must support new frameworks, new industries, new AI models, and new workflows without redesign. The standing test: if adding a new industry, framework, or AI provider requires a code change to an existing object's structure, that object's design has failed this principle.

---

## SECTION 2: The Universal Business Object Model

This section is the single inheritance contract for every business object in Aurex. It is stated exactly once. Sections 3–5 (CDE, BQ, BA) do not repeat any capability defined here — they declare inheritance from this contract and add only what is genuinely distinctive to their type.

**SD-002-004: Universal Identity**

Every business object possesses a globally unique, permanent identity (`CDE-000001`, `BQ-000025`, `BA-000089`, `REP-000014`, `EVD-000112`) alongside a canonical name, business name, description, and version. Business names and labels may change per tenant; the canonical identity never does.

*(Formalized per ARP-001 WP-3: this identity is assigned and catalogued, not merely declared. Business Objects are registered in the Canonical Business Object Register — CBOR, CMD-001 §26; Business Activities are registered in the Business Activity Registry — BAR, IMP-001 §6.22. Both registries operationalize this rule; neither redefines it.)*

**SD-002-005: Canonical Definition, Independent of Presentation**

Every object maintains a global definition independent of any customer's terminology. *Example: canonically "Revenue"; a customer may label it "Net Sales" in their Sales department view. The underlying object remains Revenue.* This is the foundation of MDM (Master Data Management) discipline within Aurex: one golden record, unlimited local labels.

**SD-002-006: Metadata Extensions Without Canonical Pollution**

Customers may extend any object with custom labels, additional attributes, custom categories, or industry classifications — at Global, Industry, Company, Department, or User scope — without ever altering the canonical definition itself. Extension Without Pollution is the governing rule.

**SD-002-007: Universal Ownership**

Every object requires a named Owner and optionally supports Reviewer, Approver, Assignee, and Delegate roles. The specific ownership model is configurable per enterprise; the capability itself is universal and non-optional.

**SD-002-008: Universal Lifecycle**

Every object supports a configurable lifecycle. Default: `CREATED → DISCOVERED → EXTRACTED → ENTERED → VALIDATED → REVIEWED → APPROVED → SUPERSEDED → ARCHIVED`. Organizations may add, remove, or rename states (e.g., `LEGAL_REVIEW`, `BOARD_APPROVED`) — the lifecycle *engine* remains metadata-driven regardless of how any tenant configures its states.

**SD-002-009: Every State Transition Is an Event — Nothing Is Overwritten**

No lifecycle transition occurs silently. Every state change generates an immutable business event (`DISCOVERED`, `REVIEWED`, `APPROVED`, `REJECTED`, `ASSIGNED`, `SUPERSEDED`, `ARCHIVED`). **This is Aurex's event-sourcing model, stated explicitly by name:** the current state of any object is not stored as ground truth — it is a computed projection of that object's full historical event stream. History is the source of truth; current state is a view of it.

**SD-002-010: Universal Versioning**

Every object preserves its full historical state across versions, supporting comparison, restoration, audit, and effective-dated reconstruction of "what was true as of any given date." Nothing is ever permanently overwritten.

**SD-002-011: The Canonical Temporal Model**

*(Consolidates six scattered v1.0 references into one statement.)* Every business object supports **Effective From**, **Effective To**, **Version**, **Status**, and **Approval Reference** as universal temporal properties. This is the single mechanism by which Aurex answers "what did this look like on any past date" for any object of any type — CDEs, organizational structures, governance policies, and reports all use this same temporal model, not type-specific variants of it.

**SD-002-012: Universal Evidence Support**

Every object may attach evidence — documents, web sources, ERP exports, user inputs, AI discoveries, or manual entries — carrying source, page/location reference, confidence, discovery method, and owner. Evidence is itself a first-class business object (Section 6) and is reusable across every object that references it.

**SD-002-013: Universal Relationships and the Enterprise Knowledge Graph**

Every object may participate in typed relationships (`DEPENDS_ON`, `USES`, `REQUIRES`, `SUPPORTS`, `DERIVED_FROM`, `PART_OF`, `MAPS_TO`) with any other object. Collectively, these relationships form Aurex's enterprise knowledge graph — this is named explicitly here as the platform's knowledge-graph architecture, not merely "relationships between records."

**SD-002-014: One Truth, Multiple Views — Multi-View Consumption**

An object exists exactly once. It may be consumed differently by a Finance view, a CFO view, an Annual Report, and a Board Dashboard without duplication, independent ownership, or the risk of conflicting versions. Truth is canonical; every view is a projection of it.

**SD-002-015: Configurable Visibility — Show, Hide, Archive, Promote**

Organizations may show, hide, archive, or promote any object without destroying it. Hidden and archived objects remain fully auditable, traceable, and recoverable. Hard deletion is never a default operation — it requires the governance process defined in Section 8.

**SD-002-016: Universal Explainability**

Every object must answer, on demand: What is it? Why does it exist? Who owns it? Who changed it? Where did it come from? What evidence supports it? This is a mandatory capability of the object itself — not a screen feature layered on top of it (SD-001 governs how the answer is *displayed*; this principle governs that the object must be *able* to answer).

**SD-002-017: Universal Enterprise Search**

Every object is discoverable by business meaning — keywords, tags, relationships, owners, departments, frameworks, evidence sources — never by database structure. A user searches for "delivery cost," not for a table name.

**SD-002-018: Universal Bulk Operations**

Every object type supports bulk assign, bulk approve, bulk review, bulk hide, and bulk export. Enterprise productivity at scale is a first-class requirement of the object model, not an interface afterthought (SD-001 governs how bulk actions render on screen; this principle governs that the underlying object model must support them).

**SD-002-019: Human Governed, AI Assisted**

AI may discover, extract, infer, recommend, classify, summarize, and detect patterns on any object. Humans alone may approve, reject, override, promote, archive, and purge. This authority boundary is universal and does not vary by object type, tenant configuration, or AI capability improvement.

**SD-002-020: Universal Extensibility**

Every object supports safe, versioned, upgradeable, and portable extension by customers and partners — fields, labels, relationships, categories, and workflows may all be extended without modifying canonical definitions or fragmenting the object model.

**The Universal Business Object Blueprint**

```
UniversalBusinessObject
├── Identity          (SD-002-004)
├── Canonical Definition (SD-002-005)
├── Ownership          (SD-002-007)
├── Lifecycle & Events (SD-002-008, SD-002-009)
├── Versioning & Temporal Model (SD-002-010, SD-002-011)
├── Evidence           (SD-002-012)
├── Relationships       (SD-002-013)
├── Multi-View Projection (SD-002-014)
├── Visibility & Governance States (SD-002-015)
├── Explainability      (SD-002-016)
├── Search & Bulk Operations (SD-002-017, SD-002-018)
├── Governance Authority (SD-002-019)
└── Extensibility        (SD-002-020)
```

Every subtype defined in Sections 3, 4, and 5 inherits this blueprint in full. What follows in those sections is additive only.

---

## SECTION 3: Canonical Data Elements (CDE) Rules

*(Inherits Section 2 in full. States only what is distinctive to CDEs.)*

**SD-002-021: One Business Fact, One CDE**

A business fact exists once, never once per framework. *Bad: "IFRS Revenue," "Regulatory Revenue," "Annual Report Revenue" as three separate objects. Good: one Revenue CDE, mapped to IFRS, the Annual Report, and Board Reports as metadata.* One Truth, Multiple Consumers.

**SD-002-022: CDEs Are Framework-Independent**

A CDE never belongs to a framework. *Bad: "Regulatory Employee Count." Good: "Employee Count," used by the applicable regulatory framework, IFRS, the Annual Report, and internal resilience reporting as separate mapping metadata.* Framework mappings are metadata layered onto the CDE; they are never part of its identity.

**SD-002-023: CDEs Belong to Business Domains**

Every CDE belongs to a primary domain (Finance, HR, Supply Chain, Risk) that may be extended by company or industry. Domain assignment is what makes enterprise search and role-based consumption (Section 2) meaningful for data elements specifically.

**SD-002-024: CDE Discovery Method Is Always Visible**

A CDE's value may originate from Discovery, Extraction, Manual Entry, Inference, or Import — and whichever method produced the current value must remain visible on the object, not just in an audit log. This is the CDE-specific expression of SD-001's Discover-First sequencing (SD-001-004): the object records *which* step in that sequence actually resolved it.

**SD-002-025: CDE Confidence Composition**

Every CDE maintains a confidence score computed from source reliability, human review status, evidence quality, document recency, and cross-validation — the specific formula is governed jointly with SD-001-011 (screen-facing disclosure requirement); this principle governs that the CDE object itself must carry the score and its contributing factors, not just a final number.

**SD-002-026: CDE Coverage Is Dynamic — Known and Unknown CDEs**

The platform distinguishes discovered-and-known CDEs (Revenue, Employee Count) from industry- or customer-specific metrics not yet in any canonical layer (e.g., a plant-specific efficiency index). Unknown CDEs may be added to the canonical library, kept company-specific, or archived — this dynamic is what allows the CIL (Section 9) to grow without every possible metric being pre-defined at platform launch.

**SD-002-027: CDEs Relate to Business Questions and Business Activities**

A CDE is populated or validated through one or more Business Questions (Section 4), which are in turn grouped into Business Activities (Section 5). The relationship chain — Business Questions → CDE → Frameworks — is a CDE-specific structural rule, distinct from the generic relationship capability in SD-002-013.

**SD-002-028: Customer-Defined CDEs Are First-Class Citizens**

A customer-created CDE (e.g., "Plant Safety Score," "Customer Happiness Index") inherits the full Section 2 blueprint identically to a globally-canonical CDE. Custom, but never second-class.

---

## SECTION 4: Business Questions (BQ) Rules

*(Inherits Section 2 in full. States only what is distinctive to BQs.)*

**SD-002-029: Business Questions Use Business Language Only**

A Business Question is phrased in business language, never in framework codes or regulatory citations. *Bad: "Reg-L3-P5-Q2." Good: "How many women employees worked during the reporting period?"* A user answering a question should never need to know which framework, report, or regulation is consuming the answer. This is the object-level enforcement of L3 (Business Language Only).

**SD-002-030: One BQ May Support Multiple CDEs; One CDE May Require Multiple BQs**

A single question ("What was total cost of delivery?") may populate several CDEs (Transportation Cost, Packaging Cost, Distribution Cost). Conversely, one complex CDE may require several distinct questions to fully resolve. Ask Once, Reuse Everywhere.

**SD-002-031: BQs Are Framework-Independent**

Identical to the CDE rule (SD-002-022), applied to questions: a BQ is never named after the framework that consumes it, and the same BQ may feed multiple frameworks' reporting requirements simultaneously.

**SD-002-032: BQs Belong to Business Activities, Never to Standalone Questionnaires**

A user never answers an isolated, numbered question. Every BQ belongs to a named Business Activity (Section 5). This is the object-model enforcement of L22 (One Primary Question Per Screen) and the platform's core "Business Activities, Not Questionnaires" law — a BQ with no parent Activity is a modeling error, not a valid object state.

**SD-002-033: Every BQ Supports Multiple Input Methods**

A BQ may be resolved via Discover, Upload, Enter, Import, or Skip — mirroring the CDE discovery-method rule (SD-002-024) at the question level, since a single BQ's answer may itself be sourced from any of these methods independently of how its parent CDE was resolved.

---

## SECTION 5: Business Activities (BA) Rules

*(Inherits Section 2 in full. States only what is distinctive to BAs.)*

**SD-002-034: Every Activity Represents Real Business Work**

An Activity is named for the business work it represents, not the data it collects. *Bad: "Financial Data Entry." Good: "Cost of Delivery Assessment."* An Activity must be understandable to a business user with no platform training.

*(Formalized per ARP-001 WP-3: every Activity satisfying SD-002-034 is catalogued in the Business Activity Registry — BAR, IMP-001 §6.22 — per SD-002-004's Universal Identity rule.)*

**SD-002-035: Activities Aggregate Questions Into Coherent Work**

One Activity contains many Business Questions, which in turn populate many CDEs. This aggregation is what allows SD-001's Guided Completion screens (SD-001-009) to present one named piece of work rather than a list of disconnected questions.

**SD-002-036: Activities Must Communicate Effort and Business Value Before Starting**

Every Activity states its input count, estimated time, and which reports or CDEs it improves, before the user begins. *Example: "Cost of Delivery — 10 inputs, 3 minutes, improves the Annual Report, IFRS readiness, and the Resilience P&L."* Business Value Before Data Collection.

**SD-002-037: Activities Support Progressive and Collaborative Completion**

An Activity may be started, saved as a draft, delegated to another owner for part of its inputs, and resumed — with multiple contributors completing different sections of the same Activity object. *Workflow execution mechanics (notifications, routing) belong to SD-003; the object's capacity to hold partial, multi-owner state belongs here.*

**SD-002-038: Activities Generate Measurable Business Outcomes**

Completing an Activity is measured by CDEs improved, reports updated, and risk or coverage change — not merely by "submitted" status. An Activity's value is its downstream effect on the object graph, not the act of completion itself.

**SD-002-039: Customer-Defined Activities Are First-Class Citizens**

Identical in spirit to SD-002-028 for CDEs: a customer-created Activity inherits the full Section 2 blueprint and may be promoted through the CIL (Section 9) exactly as a canonical Activity would be.

---

## SECTION 6: Evidence & Source Intelligence Rules

*(Formalized per ARP-001 WP-5: this section's Evidence, confidence, and source rules are the foundation Enterprise Intelligence reasoning builds on. EIA-001 Vol. II §12's Knowledge Asset model — Provenance, Confidence, Freshness, Authority, Lineage — extends these rules into the Enterprise Intelligence domain specifically; it does not define a competing Evidence concept. Reasoning provenance and confidence scoring for AI-assisted output are owned by EIA-001 under this section's authority, per ARCH-000 §7c.)*

**SD-002-040: Evidence Is a First-Class Business Object, Not an Attachment**

Evidence is not a file attached to a record — it is itself a governed object with identity, ownership, versioning, relationships, confidence, events, audit, and lifecycle, inheriting Section 2 in full.

**SD-002-041: No CDE Exists Without Evidence Capability**

Every CDE must support an evidence relationship, even if a specific value is currently unresolved. No Evidence, No Trust is the governing rule — this does not mean every CDE has evidence attached at all times, only that the capability is universal and unresolved CDEs must be visibly distinguishable from evidenced ones.

**SD-002-042: Evidence May Originate From Any Recognized Source Class**

Document sources (PDF, Excel, Word, images), enterprise sources (SAP, Oracle, Workday, Salesforce), public sources (national registries, regulators, company websites), human sources (manual input, approvals, board decisions), and AI sources (LLM discoveries, inferences) are all valid evidence origins, each carrying its own reliability weighting (Section 4 of SD-001 v2.0 governs how that weighting composes into a displayed confidence score).

**SD-002-043: Evidence Supports Granular, Precise References**

Evidence traceability extends to document, page, section, table, and cell level where the source format permits it. Trust Requires Precision.

**SD-002-044: Evidence Is Reusable Across Objects**

One evidence record (e.g., a single annual filing) may support many CDEs simultaneously. Duplicating the same evidence record per CDE is a modeling error.

**SD-002-045: Evidence Confidence Is Independently Scored**

Evidence itself carries a confidence score, independent of and contributing to the confidence of any CDE it supports — an audited financial statement and a human-entered estimate do not carry the same evidential weight even if they produce the same numeric value.

**SD-002-046: Evidence Preserves Immutable Original Sources**

AI may enrich evidence — classify it, extract entities from it, summarize it — but the original source evidence is never altered or destroyed by that enrichment. Enrichment is always additive metadata alongside an immutable original.

**SD-002-047: Evidence Supports Multi-Modal Formats**

Documents, images, audio (board recordings), video (plant audits), and structured data (ERP exports, JSON, CSV, XML) are all valid evidence formats, each inheriting the same Section 2 blueprint regardless of format.

**SD-002-048: Evidence Retention Has a Governed Floor**

*(New — closes a v1.0 gap.)* Evidence retention is configurable per tenant and per data category, but never below a stated constitutional floor: audit-relevant evidence is retained for a minimum of seven years or the applicable statutory minimum, whichever is longer, and this floor may be raised by tenant policy but never lowered without documented governance approval (see Section 8).

**SD-002-049: Cross-Object Data Lineage Is Explicit**

*(New — closes a v1.0 gap.)* Beyond within-object evidence traceability (SD-002-043), the platform maintains an explicit lineage chain across derived objects: a number appearing in a published Report traces backward through the Activity that produced it, the CDEs it aggregated, and each CDE's individual evidence — as one continuous, queryable chain, not four separately-traceable hops a user must manually assemble.

**SD-002-050: Evidence Is Human Governed**

AI may discover, classify, summarize, and recommend evidence classification. Humans alone approve, reject, override, and archive evidence records — identical authority boundary to SD-002-019, restated here because evidence governance failures carry outsized legal and audit consequence.

**The Universal Evidence Blueprint**

```
Evidence
├── Identity          (Evidence ID, Type, Version)
├── Source             (System, Document, URL, Origin)
├── References          (Page, Section, Table, Cell)
├── Confidence          (Score, Contributing Factors)
├── Lineage            (Cross-object chain, SD-002-049)
└── Governance          (Owner, Retention Floor, Lifecycle)
```

---

## SECTION 7: Event, Lifecycle & Audit Rules

**SD-002-051: No Object Exists Outside a Defined Lifecycle**

Every business object's lifecycle is metadata-driven, tenant-configurable, version-controlled, extensible without code change, and governed through permissions — with no exceptions for any object type.

**SD-002-052: State Transitions Are Always Event-Driven**

No lifecycle transition occurs silently. Every transition generates an immutable event (`CDE_DISCOVERED`, `CDE_REVIEW_REQUESTED`, `CDE_APPROVED`, `EVIDENCE_VERIFIED`, `ACTIVITY_COMPLETED`, `REPORT_PUBLISHED`). Restated here at the general lifecycle-engine level (see SD-002-009 for the object-level statement of the same event-sourcing principle).

**SD-002-053: Event Types Are Tenant-Configurable Metadata**

Every event carries a configurable code, name, category, severity, visibility, retention period, escalation rule, notification policy, and stated business consequence. New event types require no application deployment — only a metadata record.

**SD-002-054: The Audit Trail Answers Seven Questions, Always**

Every audited action must answer: Who, What, Why, When, How, Using Which Evidence, and Under Which Policy. Audit is immutable, exportable, legally defensible, and historically reconstructable — an architectural guarantee, not an operational feature that can be disabled per tenant.

---

## SECTION 8: Ownership, Responsibility & Governance Rules

**SD-002-055: Ownership Memory Is Preserved, Not Just Current Ownership**

The platform preserves who owned, reviewed, approved, delegated, escalated, and overrode an object across its entire history — not merely who owns it today. Knowledge without ownership history is incomplete knowledge.

**SD-002-056: Governance Actions Are Always Evidence-First**

No approval exists without a referenced evidence basis, a stated business justification, an audit record, and a named responsible individual. Governance without evidence is opinion; Aurex governs evidence-backed truth only.

**SD-002-057: Governance Intensity Reflects Materiality, Not Object Type**

Not every object requires equal governance. Materiality — not the object's type or category — determines the required intensity of approval, review, retention, escalation, and audit. A low-materiality customer-specific metric and a high-materiality board-reported figure are governed proportionally to their actual business impact, and the materiality threshold itself is a governed, auditable configuration (closing the "who sets materiality" gap flagged in review).

**SD-002-058: Retention Floors Are Governed, Never Silently Lowered**

*(Cross-references SD-002-048.)* Any request to reduce a stated retention floor below its constitutional minimum requires Corporate Administrator approval, legal validation, and an audit record — retention reduction is never a routine configuration change.

---

## SECTION 9: Canonical Intelligence Library (CIL) Evolution Rules

**SD-002-059: The CIL Is a Four-Layer Intelligence System**

Global CIL → Industry CIL → Company CIL → Workspace Extensions. Each layer inherits from its parent while permitting controlled local evolution. Knowledge created at a lower layer never automatically alters a higher layer without the explicit governance defined below.

**SD-002-060: The Global CIL Is Immutable to Customers — Stewardship Is Named**

Customers may consume, extend, hide locally, override labels on, and add company-specific metadata to Global CIL objects. Customers may never delete, modify, or purge them directly. **Authority to change the Global CIL itself rests with the Aurex Governance Board** (see the stewardship table in SD-002-066) — this closes a gap in v1.0, where "immutable to customers" was stated without stating who *could* change it.

**SD-002-061: Industry CIL Enables Sector Intelligence**

Industry CILs (Manufacturing, Healthcare, Banking, Telecommunications, Retail, Energy, Pharmaceuticals, and others) extend the Global CIL with sector-specific CDEs, Business Questions, Activities, benchmarks, evidence types, and regulatory mappings, while preserving full inheritance from the Global layer.

**SD-002-062: Company CIL Represents Private Organizational Knowledge**

A company's canonical extensions (custom cost metrics, internal activities, internal terminology) remain private to that organization unless explicitly promoted. Unlimited company-level extension is supported without affecting global standards.

**SD-002-063: Workspace Extensions Enable Local Experimentation Without Risk**

Workspaces are the lowest tier — temporary CDEs, experimental Activities, pilot questions — supporting promotion, archiving, hiding, and retirement, and explicitly guaranteed to never compromise enterprise-wide canonical truth regardless of what is experimented with locally.

**SD-002-064: Discovery Creates Candidates, Never Automatic Canonical Changes**

AI discovery produces a candidate object — with discovery method, evidence, confidence, similarity analysis, suggested domain, suggested ownership, and business rationale attached — for human review and promotion decision. AI discovers. Humans govern. This is non-negotiable regardless of AI confidence level.

**SD-002-065: Promotion Is a Named, Governed Lifecycle With Stated Authority**

| Promotion | Authority |
|---|---|
| Workspace → Company | Company Steward |
| Company → Industry | Industry Council |
| Industry → Global | Aurex Governance Board |

Each promotion level requires its own explicit approval; no object skips a tier.

**SD-002-066: CIL Stewardship Is Multi-Tier and Explicitly Named**

| Layer | Steward |
|---|---|
| Global | Aurex Governance Board |
| Industry | Industry Intelligence Council |
| Company | Enterprise Data Council |
| Workspace | Workspace Administrator |

**SD-002-067: Similarity Detection Prevents Canonical Fragmentation**

Before any new CIL object is created, the platform performs similarity analysis against existing objects (*"New CDE: Employee Satisfaction — 94% similar to Employee Engagement Score"*) and recommends reuse, merge, extension, or — only if genuinely distinct — creation of a new object. One truth, minimal duplication, maximum semantic consistency.

**SD-002-068: Canonical Identity Survives Label Changes**

Labels may change; canonical meaning may not. Every CIL object retains a stable canonical ID, global identifier, version number, and alias list (*"CDE_001245, labeled 'Employees,' aliased as 'Associates,' 'Team Members,' 'Workforce'"*) regardless of how many customers relabel it.

**SD-002-069: Hide Is Local and Non-Destructive**

A hidden canonical object continues to exist globally, retains its relationships and dependencies, and remains fully recoverable. Hide never destroys canonical intelligence.

**SD-002-070: Archive Preserves History; Purge Requires Constitutional Governance**

Archiving indicates historical irrelevance, not deletion — archived objects remain auditable, support historical reports, and preserve evidence and relationships. Purging is the sole exception process: it requires Corporate Administrator approval, retention validation, audit recording, and legal validation, is always a soft, recoverable, auditable operation, and Global CIL objects may never be purged by customer action under any circumstance.

**SD-002-071: AI May Recommend Evolution; It May Never Enforce It**

AI may recommend new CDEs, Activities, Questions, merges, retirements, promotions, or relationship updates. Approval, publication, promotion, archiving, purging, and every governance exception remain exclusively human. This is a constitutional principle of the platform, restated here at the CIL-evolution level because it is the point of highest AI-autonomy temptation.

**SD-002-072: CIL Evolution Preserves Backward Compatibility**

Canonical changes never invalidate historical intelligence — historical reports continue functioning, evidence chains remain intact, and older references remain resolvable, even as canonical labels or structures evolve.

**SD-002-073: Relationships Evolve Independently of Labels**

A CIL object's relationship graph is a canonical asset in its own right. Relabeling or re-owning an object never destroys its dependency graph — the semantic knowledge network must remain stable across organizational change.

**SD-002-074: CIL Conflict Precedence — Company Override vs. Incoming Industry Promotion**

*(New — closes a v1.0 gap, and resolves the same open question flagged in SD-001 v2.0's freeze statement.)* When a Company CIL extension and a newly-promoted Industry CIL update define the same underlying concept differently, the **Company override takes precedence for that tenant** until the tenant's Enterprise Data Council explicitly reviews and accepts the incoming Industry definition. The incoming definition is never silently applied over an existing customer override. This is the single resolution to the configuration-conflict question that appeared three times across SD-001 and SD-002 in review — stated once, here, as the canonical answer; SD-001's Configuration Hierarchy candidate principles should reference this rule rather than re-deciding it.

**SD-002-075: The CIL Is the Enterprise Memory System**

The CIL functions as enterprise memory, organizational learning, AI knowledge base, historical truth repository, and cross-period intelligence layer simultaneously. Its value compounds — every discovery, approval, correction, override, relationship, and evidence pattern strengthens it. This is Living Memory (L37), stated at the architectural level.

**SD-002-076: Canonical Evolution Prioritizes Truth Over Convenience**

The platform prefers reuse, merge, extend, and govern over duplicate, fork, delete, and recreate. Truth fragmentation is a governance failure, not a minor inconsistency; canonical evolution is a strategic capability of the platform, not administrative overhead.

---

## SECTION 10: Metadata, Configuration & Extensibility Rules

**SD-002-077: Everything Business-Facing Is Metadata**

Domains, departments, roles, lifecycle states, event types, Business Questions, Business Activities, frameworks, reports, labels, visibility rules, approval models, and retention policies are all metadata records. Adding or changing a business concept never requires software deployment.

**SD-002-078: Canonical Identity Is Independent of Presentation**

Restated here at the metadata-architecture level (see SD-002-005 for the object-level statement): business meaning is canonical; labels are metadata; the two never conflate.

**SD-002-079: Domains, Departments, and Roles Are Tenant-Configurable Metadata**

No business domain, department structure, or role name is hardcoded. Organizations define, rename, merge, and archive these freely; role metadata governs visibility, ownership rights, approval rights, delegation rights, and escalation authority, while security implementation consumes — but never defines — the business role itself.

**SD-002-080: Reports and Frameworks Are Metadata, Rendered Not Hardcoded**

Reports (Annual Report, Board Pack, statutory filings) are metadata definitions of sections, dependencies, evidence requirements, and publication rules; the reporting engine renders these definitions rather than executing hardcoded templates. Frameworks (the applicable regulatory and voluntary standards a tenant operates under) exist as invisible metadata mapping layers — never as objects an executive is shown directly. The executive experience remains business-first; framework compliance is invisible by design (L25).

**SD-002-081: Visibility and Retention Are Metadata-Driven, Never Hardcoded**

Visibility rules (who sees what, by role, department, hierarchy, geography, or materiality) and retention rules (how long evidence, events, and reports persist, subject to the floor in SD-002-048) are both tenant-configurable metadata. Visibility governs access to views; it never alters canonical truth.

**SD-002-082: Enterprise DNA Is a Tenant Metadata Record**

*(The raw data model referenced by SD-001 v2.0 Section 6.)* Decision style, risk appetite, approval culture, AI trust model, and management style are stored as a single tenant configuration record that Enterprise DNA screens (SD-001 v2.0) render from. This record influences approval models, escalation policies, and visibility rules — never by forking the platform, only by parameterizing the same universal engine.

**SD-002-083: Navigation Configuration Exists as a Metadata Record**

*(Corrected from v1.0's "Navigation Structures Are Metadata," which improperly defined menus, landing pages, and quick actions — screen concerns now owned exclusively by SD-001-018.)* The underlying navigation configuration object — which named navigation entries exist for a tenant, and their target screen references — is a metadata record like any other. How that record renders as menus, workspaces, or quick actions on screen is entirely SD-001's concern; this principle governs only that the record itself exists as configurable metadata rather than hardcoded routes.

**SD-002-084: Metadata Changes Are Themselves Audited Business Events**

Every metadata change (`ROLE_CREATED`, `DOMAIN_ARCHIVED`, `QUESTION_UPDATED`, `ACTIVITY_PROMOTED`) generates an audit event capturing who changed it, why, when, and the before/after definition. Configuration history is organizational memory, not a side effect.

**SD-002-085: Extensibility Preserves Canonical Integrity**

Every customer or partner extension must remain safe (cannot alter global definitions), versioned, upgradeable, and portable across tenants — extensibility that fragments canonical truth is, by definition, not extensibility Aurex supports.

---

## SECTION 11: Relationships, Dependencies & One Truth Multiple Views Rules

**SD-002-086: Relationships Are Governed Enterprise Assets**

Relationships (`DEPENDS_ON`, `GENERATES`, `SUPPORTS`, `INFLUENCES`, `APPROVES`) are governed with the same rigor as the business facts they connect. A broken relationship represents broken intelligence, not a cosmetic data-quality issue.

**SD-002-087: Dependency Graphs Are First-Class, Queryable Structures**

Complex objects (a Report requiring 250 CDEs; an Activity using 10 CDEs) maintain explicit, queryable dependency graphs — not implicit relationships a user must reconstruct manually from separate records.

**SD-002-088: One Truth, Multiple Views, Applied at the Relationship Level**

The same underlying object participates in Executive Views, Department Views, Role Views, Framework Views, Reports, and Activities without duplication, independent ownership, or conflicting versions at any of those consumption points.

**SD-002-089: Enterprise Intelligence Is a Connected Knowledge System, Not a Record Collection**

Enterprise understanding emerges from the combination of Objects + Relationships + Evidence + Events + Ownership + Business Consequences functioning together — Aurex is architected as a connected intelligence network, and any feature that treats objects as independent records rather than nodes in this network is a design deviation from this principle.

---

## SECTION 12: Universal Business Object Constitutional Principles

This section crystallizes the non-negotiable constitutional laws governing every business object, present and future. These are permanent architectural constraints, not implementation recommendations, and they intentionally restate — in compressed, canonical form — principles already established in Sections 2–11. This is deliberate: a constitution crystallizes, it does not introduce. It explicitly excludes screen behavior (SD-001), user interactions, workflow experiences, notification mechanics, and collaboration models (all SD-003).

**SD-002-090: Business Truth Is Evidence First** — no business fact exists without evidence; facts without evidence are opinions.

**SD-002-091: Discover First, Ask Later Is Constitutional** — `Discover → Extract → Retrieve → Infer → Confirm → Route → Ask`; human input is the final mechanism, never the primary one; the burden of understanding belongs to the platform before it belongs to the user.

**SD-002-092: Human Governed, AI Assisted** — restated as constitutional law: human judgment is the final authority on organizational truth, without exception, regardless of AI capability.

**SD-002-093: Everything Is Event-Driven** — current state is a projection of historical events; history creates truth.

**SD-002-094: Everything Is Versioned** — updates create new versions; they never overwrite history.

**SD-002-095: Everything Is Explainable** — black-box truth does not exist; explainability is a prerequisite for enterprise trust.

**SD-002-096: Everything Is Auditable** — immutable, exportable, legally defensible, historically reconstructable; audit is architecture, not a feature toggle.

**SD-002-097: Everything Is Metadata** — application code implements engines; metadata implements business semantics.

**SD-002-098: One Truth, Multiple Views** — truth is canonical; views are projections; never duplicated, never independently owned.

**SD-002-099: Relationships Are Enterprise Assets** — governed as carefully as the facts they connect.

**SD-002-100: Organizational Memory Is Permanent** — Aurex is a living organizational memory, not a transactional application.

**SD-002-101: Governance Intensity Reflects Materiality** — governance effort remains proportional to business impact, never uniform.

**SD-002-102: Canonical Evolution Prioritizes Reuse Over Duplication** — enterprise truth compounds through reuse; duplication destroys semantic integrity.

**SD-002-103: Backward Compatibility Is Mandatory** — historical reports, evidence chains, relationships, and audit histories remain reconstructable across decades of platform evolution.

**SD-002-104: Business Language Always Wins** — the platform exposes Cost of Delivery, Workforce Readiness, and Strategic Commitments, never framework terminology or regulatory codes; canonical semantics may be complex, but the business experience is always simple.

**SD-002-105: Enterprise Intelligence Is a Connected Knowledge System** — knowledge creates intelligence; context creates meaning; the platform is a network, not a record collection.

**SD-002-106: The Platform Is a Living System** — it becomes more intelligent with time, not more complicated; memory, knowledge, and trust all compound.

**SD-002-107: Truth Over Convenience Is the Supreme Principle**

When any architectural tradeoff arises, the platform always prefers evidence over assumption, history over deletion, reuse over duplication, governance over speed, explainability over automation, and human authority over AI autonomy. This principle supersedes every implementation shortcut. The integrity of enterprise truth is the platform's highest constitutional responsibility — higher than delivery speed, feature velocity, or AI capability.

---

## SECTION 13: Multi-Tenancy & Data Isolation

*(New in v2.0 — this section did not exist in v1.0, which used the word "tenant" exactly twice in the entire document with no explicit isolation guarantee.)*

**SD-002-108: Every Object Carries an Explicit Tenant Boundary**

Every business object — CDE, BQ, BA, Evidence, Report, Event — carries an explicit, non-optional tenant identifier as part of its Universal Identity (SD-002-004). An object with an ambiguous or inferred tenant boundary is an invalid object state, not an edge case to be resolved at query time.

**SD-002-109: Company CIL and Workspace Objects Are Isolated by Construction**

Company-level and Workspace-level CIL objects (Sections 9) are isolated from every other tenant's objects at the data layer, not merely at the application or permissions layer. A permissions bug must never be capable of exposing one tenant's Company CIL to another tenant — isolation is a storage and retrieval guarantee, not solely an access-control feature.

**SD-002-110: Shared Infrastructure Never Implies Shared Performance Risk**

One tenant's discovery volume, evidence processing load, or CIL extension size must never degrade another tenant's platform performance. Resource allocation across tenants is a governed, monitored architectural guarantee, not an operational best-effort.

**SD-002-111: Only the Global and Industry CIL Layers Are Legitimately Shared**

The only business-object content legitimately shared across tenant boundaries is the Global CIL and the relevant Industry CIL (Section 9) — both are explicitly designed for cross-tenant reuse. Every other layer (Company, Workspace) is tenant-exclusive by default, and any mechanism for one tenant to reference another tenant's Company-level object requires an explicit, named, audited cross-tenant sharing agreement — it is never a default or implicit capability.

**SD-002-112: Tenant Migration and Offboarding Preserve Full Historical Integrity**

When a tenant migrates infrastructure or offboards from the platform, that tenant's full object graph — including event history, evidence, relationships, and audit trails — must export as a complete, self-consistent, historically-reconstructable package. Organizational memory (SD-002-100) belongs to the tenant, not to the platform, and must be portable on request.

**Cross-Reference** *(added per `ADR-020`, Repository Owner Constitutional Design Workshop, 2026-08-07 — references this Section's existing guarantee; adds no new principle number)*: the tenant boundary and isolation guarantees `SD-002-108` through `SD-002-112` establish apply without exception to Conversation and Interaction, the AI Session Management constructs `RTA-001 §13.15a` defines.

---

## Full Principle Index

| Range | Section |
|---|---|
| SD-002-001 – 003 | Section 1 — Purpose & Philosophy |
| SD-002-004 – 020 | Section 2 — The Universal Business Object Model |
| SD-002-021 – 028 | Section 3 — Canonical Data Elements (CDE) Rules |
| SD-002-029 – 033 | Section 4 — Business Questions (BQ) Rules |
| SD-002-034 – 039 | Section 5 — Business Activities (BA) Rules |
| SD-002-040 – 050 | Section 6 — Evidence & Source Intelligence Rules |
| SD-002-051 – 054 | Section 7 — Event, Lifecycle & Audit Rules |
| SD-002-055 – 058 | Section 8 — Ownership, Responsibility & Governance Rules |
| SD-002-059 – 076 | Section 9 — Canonical Intelligence Library (CIL) Evolution Rules |
| SD-002-077 – 085 | Section 10 — Metadata, Configuration & Extensibility Rules |
| SD-002-086 – 089 | Section 11 — Relationships, Dependencies & One Truth Multiple Views |
| SD-002-090 – 107 | Section 12 — Universal Business Object Constitutional Principles |
| SD-002-108 – 112 | Section 13 — Multi-Tenancy & Data Isolation |

**Total SD-002 principles: 112 (renumbered, zero gaps, zero collisions).**
**v1.0 had 182 numbered slots for 222 actual rule definitions across 11 colliding IDs; v2.0 has 112 unique, non-overlapping principles covering the same substantive ground with the systemic Section 1–5 redundancy removed.**

---

## Freeze Statement

SD-002 v2.0 is ready for lock. The 11 rule-ID collisions are resolved through consolidation, not just renumbering — the redundant per-type restatement that caused them (Sections 1–5 each independently asserting the same universal capabilities) has been replaced with a single inheritance contract (Section 2) that CDE, BQ, and BA rules now build on rather than duplicate. Multi-tenancy is now an explicit, five-principle section rather than two passing references. The SD-001 boundary violation (Navigation Structures) is corrected. The language purge is complete. The CIL conflict-precedence gap is resolved with a stated rule (SD-002-074), and that resolution is the canonical answer to the same question flagged three times across SD-001 v2.0 and this document — SD-001's corresponding candidate principle should now reference SD-002-074 rather than re-deciding it independently.

One item is intentionally left open rather than silently resolved: **SD-002-057** states that materiality governs governance intensity, and that the materiality threshold is itself a governed configuration — but this document does not yet state a default materiality threshold or the specific council authorized to set one per tenant. This is appropriately an SD-003 (interaction/workflow) or implementation-level decision rather than an object-rules decision, and is flagged here so it is not lost in the handoff to whichever document resolves it.
