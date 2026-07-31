**IMP-001**

**Aurex Implementation Playbook**

**Classification:** Enterprise Engineering Architecture (Layer 3, per ARCH-000)
**Status:** Active — governs current engineering practice; evolves via Controlled Evolution (ARCH-000 §12.6)
**Governing framework:** ARCH-000

**Purpose**

IMP-001 defines the mandatory engineering standards, implementation
methodology, coding patterns, quality gates, and delivery lifecycle for
implementing the Aurex Intelligent Operating Center.

It translates the Enterprise Architecture into a consistent, repeatable
engineering process, ensuring every Business Domain, Business Object,
API, workflow, event, screen, and AI capability is implemented in
accordance with the approved architecture.

IMP-001 is the authoritative engineering implementation standard for
Aurex.

**Design Philosophy**

IMP-001 is built upon the principles established by:

-   Aurex Enterprise Blueprint

-   Master Technical Architecture

-   SD-001 -- Screen Design Principles

-   SD-002 -- Universal Business Object Rules

-   SD-003 -- Enterprise Interaction Laws

-   URA-001 -- User, Role, Permission, Event & Assignment

-   ERG-001 -- Enterprise Structure & Relationship Management

-   CMD-001 -- Canonical Data Model & Master Data Governance Architecture

-   RTA-001 -- Runtime Architecture and Execution *(added under the Enterprise Intelligence Engineering Architecture Enhancement, Phase 3 — Section 13 implements RTA-001's Sections 12, 13, 21, and 22, including AMD-013 Phase 2's Execution Strategy, Execution Capability Selection, Evidence Fusion, and Evidence Sufficiency Gate extensions; extended under the Runtime Engineering Methodology governance determination (WP-02) to implement RTA-001's remaining Runtime Components — Sections 6-11 and 14-19 — as Section 13's second engineering specialization, §§13.17-13.25)*

It does **not redefine architecture**. It operationalizes it.

**Structure (Gold Standard v1.1 — Corrected)**

*(This replaces an earlier planning outline that proposed 20 sections but was superseded during drafting by a different, 7-section structure plus Appendix A. That outline was never updated to match, creating a genuine internal-consistency defect identified during the Version 1.0 constitutional validation and corrected here. The list below is the actual, final structure of this document.)*

Section 1 — Purpose & Guiding Principles. Section 2 — Canonical Implementation Lifecycle (CIL) *(§2.13a, Work Package Closure & Release Gate Sequence, added per ADR-017 — METH-002)*. Section 3 — Canonical Implementation Unit (CIU). Section 4 — Repository Architecture & Project Structure. Section 5 — Canonical Business Object Implementation Pattern. Section 6 — Canonical Business Activity Implementation Pattern (CBAIP). Section 7 — Architectural Alignment & Implementation Guidance. Section 8 — API Standards. Section 9 — Event Implementation Standards. Section 10 — Frontend Standards. Section 11 — Testing Strategy. Section 12 — CI/CD & DevOps. Section 13 — Enterprise Intelligence Implementation Patterns *(added under the Enterprise Intelligence Engineering Architecture Enhancement, Phase 3; extended under AMD-013 Phase 3 with Planner, Execution Capability/Discovery Provider/Reasoning Engine Resolver, Execution Strategy, Multi-Agent, Evidence Fusion, Knowledge & Memory, and Discovery Pipeline patterns)*. Appendix A — Canonical Reference Implementation. Appendix B — WP-05 Reference Pointer *(added per ADR-017 — METH-002; points to METH-002 as the sole source for retrospective detail, not a restatement)*.


**Section 1 — Purpose & Guiding Principles**

**1.1 Objectives**

IMP-001 defines the mandatory engineering standard for implementing the Aurex Intelligent Operating Center. It exists so that any engineering team, or any AI coding platform, produces the same architecturally-compliant result from the same starting specification — the Business Object, Interaction, Authorization, and Structure principles already locked in SD-002, SD-003, URA-001, and ERG-001.

**1.2 Scope**

IMP-001 governs *how* the platform is built: repository structure, the Business Object and Business Activity implementation patterns, database standards, API standards, event handling, frontend implementation, testing, and deployment. It does not govern *what* is built — that is the constitutional documents' authority, and IMP-001 neither redefines nor duplicates them (Section 7 states this boundary explicitly for each).

**1.3 Engineering Philosophy**

Implementation follows the same discipline the constitutional architecture already establishes: metadata over hardcoding, canonical patterns over ad-hoc solutions, and explicit contracts (the Business Activity Contract, Appendix A.5) over implicit convention. An engineer or AI tool implementing any Business Object or Business Activity should be able to do so correctly from the pattern alone, without needing to ask a human what "the Aurex way" is for a case not yet built.

**1.4 Relationship with Architecture Documents**

IMP-001 sits downstream of, and is constrained by, the ten constitutional documents (Section 7.1's table). It translates their principles into engineering practice; it does not have authority to alter them. Where an engineering constraint appears to conflict with a constitutional principle, the constitutional principle governs, and the conflict is raised for architectural review rather than resolved by implementation convenience.

**1.5 Human Governed, AI Assisted**

Per L18 and URA-001's authorization model, AI-assisted implementation (code generation, test generation, migration scripts) is fully permitted and expected — but every generated artifact is reviewed and approved by a human engineer before merge. An AI coding tool may propose a Business Activity implementation; it does not merge its own code.

**1.6 Configuration Over Customization**

Per SD-002's Everything Is Metadata principle, an implementation need that appears to require a code change should first be checked against whether it is actually a configuration gap — a missing NodeType, a missing Business Role, a missing Event definition — before a code change is written. Code changes extend the engine; configuration changes extend what the engine does for a given tenant. Confusing the two is the single most common implementation anti-pattern this document exists to prevent.

**1.7 Business Activities Over CRUD**

Per Section 1's own downstream consequence in Section 8 (API Standards, IMP-API-001): no part of the implementation — database, API, or frontend — exposes raw create/read/update/delete operations against a Business Object as its primary interface. Every operation is a named Business Activity with a Business Activity Contract, consistent with Business Activities Over Questionnaires already established at the platform level.

**One Major Enhancement**

I recommend adding something that is rarely found in implementation
guides but would be extremely valuable for Aurex:

**Implementation Contract**

Every Business Object must have an **Implementation Contract** before
coding begins.

For example:

  -----------------------------------------------------------------------
  **Attribute**             **Value**
  ------------------------- ---------------------------------------------
  Business Domain           Identity

  Business Object           Person

  Aggregate Root            Person

  Primary Master Table      person_registry

  Supporting Tables         identity_registry, membership_registry

  APIs                      8

  Events                    5

  Business Activities       12

  Permissions               14

  Screens                   6

  AI Capabilities           3

  Seed Strategy             Tenant

  Definition of Done        Complete
  -----------------------------------------------------------------------

Claude Code would implement from this contract rather than inferring
behavior from scattered documents.

**My Recommendation**

I believe **IMP-001 should be the final foundational document** before
implementation begins.

Once IMP-001 is completed, I would stop producing architecture
documentation and switch entirely to execution. Claude Code should use
the architecture documents as the source of business intent and IMP-001
as the engineering playbook. Every implementation task should begin with
an **Implementation Contract**, ensuring consistency across all domains
and preventing architectural drift as the platform grows.

I also recommend that IMP-001 be treated as a **living engineering
standard**: updates should be made only when implementation experience
reveals a repeatable pattern worth standardizing, rather than
documenting one-off decisions. This keeps the playbook concise,
practical, and directly aligned with real engineering practices.

**Section 2 --- Canonical Implementation Lifecycle (CIL)**

This is **not** a software development lifecycle.

It is the **Aurex implementation lifecycle**.

**IMP-001**

**Section 2 --- Canonical Implementation Lifecycle (CIL)**

**2.1 Purpose**

The Canonical Implementation Lifecycle (CIL) defines the mandatory
engineering sequence for implementing every capability within the
Aurex Intelligent Operating Center.

Its purpose is to ensure that all implementations:

-   Follow the approved enterprise architecture.

-   Preserve canonical business semantics.

-   Maintain consistency across domains.

-   Eliminate implementation ambiguity.

-   Prevent architecture drift.

-   Enable AI-assisted software development.

The lifecycle is mandatory for every implementation regardless of
technology, team, or deployment model.

**2.2 Core Principle**

Aurex shall never be implemented using a traditional CRUD-first
methodology.

Instead, implementation shall always proceed from business intent to
technical realization.

The mandatory implementation sequence is:

Business Intent\
│\
Business Domain\
│\
Business Object\
│\
Business Activity\
│\
Business Rules\
│\
Metadata\
│\
Persistence\
│\
API\
│\
Events\
│\
Authorization\
│\
User Experience\
│\
Testing\
│\
Deployment

Implementation shall never begin with database tables or user interface
screens.

**2.3 Canonical Engineering Stages**

Every implementation shall progress through the following stages.

  -----------------------------------------------------------------------
  **Stage**                  **Objective**
  -------------------------- --------------------------------------------
  Architecture Validation    Confirm alignment with approved architecture

  Business Domain Definition Identify the owning domain

  Business Object Definition Define the canonical Business Object

  Business Activity          Define supported business activities
  Definition                 

  Metadata Definition        Configure behavior through metadata

  Data Model Definition      Define persistence requirements

  Event Definition           Define business events

  Authorization Definition   Define access control

  API Definition             Define service contracts

  User Experience            Implement screens and interactions

  Testing                    Validate behavior

  Deployment                 Release into production
  -----------------------------------------------------------------------

No stage may be skipped without formal architecture approval.

**2.4 Implementation Dependency Rules**

Implementation shall follow dependency order rather than feature order.

The dependency hierarchy is:

Enterprise Platform\
│\
Enterprise Domain\
│\
Business Object\
│\
Business Activity\
│\
Workflow\
│\
API\
│\
Screen

For example, a screen shall not be implemented until its underlying
Business Activities, APIs, authorization rules, and Business Objects
have been completed.

**2.5 Canonical Implementation Unit (CIU)**

The smallest independently implementable unit within Aurex is the
**Canonical Implementation Unit (CIU)**.

A CIU consists of:

-   One Business Object

-   One Aggregate Root

-   One Primary Master Table

-   Associated supporting tables

-   Business Activities

-   Events

-   APIs

-   Permissions

-   Metadata

-   Tests

A CIU is considered complete only when all required implementation
artifacts have been delivered.

**2.6 Implementation Contracts**

Before development begins, every CIU shall have an **Implementation
Contract**.

The contract shall contain:

  -----------------------------------------------------------------------
  **Attribute**               **Description**
  --------------------------- -------------------------------------------
  Business Domain             Owning domain

  Business Object             Canonical Business Object

  Aggregate Root              Aggregate owner

  Primary Master Table        System of Record

  Supporting Tables           Additional persistence

  Business Activities         Supported activities

  Events                      Published and consumed events

  APIs                        Service endpoints

  Permissions                 Required authorizations

  Screens                     Consuming user interfaces

  Seed Strategy               Platform, Tenant, Runtime

  Dependencies                Upstream/downstream CIUs

  Definition of Done          Completion criteria
  -----------------------------------------------------------------------

The Implementation Contract becomes the authoritative specification for
development.

**2.7 Architecture Validation Gate**

Every CIU shall pass an architecture validation before implementation
begins.

The validation confirms:

-   Alignment with CMD-001.

-   Compliance with SD-002.

-   Compliance with SD-003.

-   Compliance with URA-001.

-   Compliance with ERG-001.

-   Alignment with the Blueprint.

-   Consistency with the Master Technical Architecture.

Implementation may proceed only after successful validation.

**2.8 Metadata-First Implementation**

Business behavior shall be implemented through metadata wherever
feasible.

Examples include:

-   Validation rules

-   Form layouts

-   Workflow definitions

-   Approval chains

-   Display labels

-   Business rules

-   AI prompts

Hardcoding business behavior is prohibited unless explicitly approved
through architecture governance.

**2.9 Activity-Driven Development**

Implementation shall be organized around **Business Activities**, not
CRUD operations.

For example:

Instead of:

-   Create Metric

-   Update Metric

-   Delete Metric

The implementation should expose business activities such as:

-   Define Metric

-   Publish Metric

-   Retire Metric

-   Assign Metric Owner

-   Map Metric to Framework

-   Review Metric Quality

This aligns software behavior with business intent.

**2.10 Progressive Implementation**

Implementation shall progress from reusable platform capabilities toward
business-specific functionality.

Recommended sequence:

Platform Foundation\
│\
Metadata Engine\
│\
Enterprise Graph\
│\
Identity & Authorization\
│\
Master Data\
│\
Business Activities\
│\
Workflow\
│\
Reporting\
│\
AI Intelligence\
│\
Screens

This ensures that business functionality is built on stable platform
services.

**2.11 Continuous Architecture Compliance**

Architecture compliance shall be continuously evaluated throughout
implementation.

Compliance checks shall occur:

-   Before coding

-   During code review

-   Before merging

-   Before deployment

-   During release validation

Any deviation from approved architecture shall require formal review and
approval.

**2.12 AI-Assisted Development**

AI tools, including Claude Code, may assist with:

-   Code generation

-   Test generation

-   API scaffolding

-   Documentation

-   Refactoring

-   Static analysis

-   Migration generation

However:

-   AI shall not make architectural decisions.

-   AI shall not redefine Business Objects.

-   AI shall not introduce new business semantics.

-   AI-generated code shall be reviewed by a human before acceptance.

This preserves the Aurex principle of **Human Governed, AI
Assisted**.

**2.13 Completion Criteria**

A Canonical Implementation Unit is complete only when:

-   Architecture validation has passed.

-   Business Objects are implemented.

-   Metadata is configured.

-   Persistence is complete.

-   APIs are published.

-   Events are implemented.

-   Authorization is enforced.

-   Tests have passed.

-   Documentation has been updated.

-   The Definition of Done has been satisfied.

No implementation shall be considered complete based solely on
successful coding.

**2.13a Work Package Closure & Release Gate Sequence (validated per WP-05, ADR-017)**

Section 2.13's own Completion Criteria state that a Canonical
Implementation Unit is complete only when "Tests have passed" and "the
Definition of Done has been satisfied," without further detail on what
satisfying those two criteria requires at Work Package closure. WP-05
(Access Management, C-002) validated the concrete sequence this
subsection now states explicitly.

The governing rule lives in **CLAUDE.md §19.7 and §19.7b** — this
subsection presents the same, validated sequence at the engineering
methodology level and does not restate or duplicate CLAUDE.md's own
governing text; where the two differ, CLAUDE.md governs.

A Work Package's Business Activities each follow their own
implementation lifecycle (Section 6.3). Once every authorized Business
Activity is implemented and unit-tested, and the repository is
synchronized (documentation, governance registers, and Technical Debt
entries all reflect the current implementation state), the Work
Package as a whole closes through:

Business Activity Analysis\
│\
Solution Design\
│\
Implementation\
│\
Unit Testing\
│\
Repository Synchronization\
│\
Independent Review (Certification)\
│\
Verification & Validation (V&V) Audit\
│\
Remediation *(only if the V&V Audit finds anything)*\
│\
Independent Verification of Remediation *(only if Remediation occurred)*\
│\
Regression Testing\
│\
Release Readiness Audit\
│\
Certification (restored/confirmed)\
│\
Git Commit\
│\
Git Push\
│\
Repository Baseline Updated

Every gate from Independent Review onward is performed by a reviewer
independent of every gate before it, per `CLAUDE.md §19.7`/`§19.7b`.
No Work Package may be pushed to the remote repository until every
gate this sequence requires has completed.

**Architectural Enhancement (Recommended)**

I recommend introducing a **Canonical Implementation Register (CIR)**.

The CIR would become the operational counterpart to CMD-001.

Each CIU would have one record containing:

-   CIU Identifier

-   Business Domain

-   Business Object

-   Implementation Status

-   Dependencies

-   Assigned Engineer or AI Agent

-   Architecture Approval

-   Test Status

-   Deployment Status

-   Version

-   Release

This would provide complete visibility into implementation progress and
allow Claude Code and human developers to work from a single governed
backlog rather than disconnected tasks.

**My Assessment**

I believe this section is one of the most important documents in the
entire Aurex framework because it defines **how implementation
happens**, not just **what should be built**. It ensures that Claude
Code remains architecture-driven rather than database-driven or
UI-driven, minimizes architectural drift, and establishes a repeatable
implementation pattern that can be applied consistently across every
Business Domain and Business Object. It also lays the foundation for
parallel development by multiple engineers or AI agents while preserving
a single canonical architecture.

**IMP-001**

**Section 3 --- Canonical Implementation Unit (CIU)**

**3.1 Purpose**

The Canonical Implementation Unit (CIU) is the smallest independently
implementable, testable, deployable, and governable unit within the
Aurex Intelligent Operating Center.

A CIU is not a database table, API, screen, microservice, or user story.

A CIU represents the complete implementation of a single Canonical
Business Object together with all supporting architectural artifacts
required to deliver business value.

The CIU establishes the standard implementation pattern for all platform
capabilities.

**3.2 Architectural Principle**

Aurex follows the principle:

**One Canonical Business Object = One Canonical Implementation Unit**

Implementation shall always be organized around Business Objects.

Implementation shall never be organized around:

-   Database tables

-   UI screens

-   CRUD operations

-   Individual APIs

-   Technology layers

These are implementation artifacts, not implementation units.

**3.3 CIU Composition**

Every CIU shall consist of the following mandatory components.

  -----------------------------------------------------------------------
  **Layer**                                **Mandatory**
  ---------------------------------------- ------------------------------
  Business Domain                          ✓

  Aggregate Root                           ✓

  Canonical Business Object                ✓

  Metadata Definition                      ✓

  Business Rules                           ✓

  Validation Rules                         ✓

  Primary Master Table                     ✓

  Supporting Tables                        ✓ (if required)

  Business Activities                      ✓

  APIs                                     ✓

  Domain Events                            ✓

  Authorization Rules                      ✓

  Audit Rules                              ✓

  Versioning Rules                         ✓

  Effective Dating                         ✓ (where applicable)

  UI Metadata                              ✓

  Tests                                    ✓

  Documentation                            ✓
  -----------------------------------------------------------------------

No CIU shall omit any mandatory component without architecture approval.

**3.4 CIU Layer Model**

Every CIU shall follow the same implementation hierarchy.

Business Domain\
│\
Aggregate Root\
│\
Business Object\
│\
Business Rules\
│\
Metadata\
│\
Persistence\
│\
Repository\
│\
Service\
│\
Business Activities\
│\
Events\
│\
Authorization\
│\
API\
│\
UI Metadata\
│\
Screen\
│\
Testing

This order is mandatory.

**3.5 Example CIU**

Example:

**Business Object:** EnterpriseNode

Business Domain\
Enterprise\
\
↓\
\
Aggregate Root\
EnterpriseNode\
\
↓\
\
Primary Table\
organization_node\
\
↓\
\
Supporting Tables\
\
organization_hierarchy\
\
enterprise_view_registry\
\
↓\
\
Business Activities\
\
Create Enterprise Node\
\
Update Enterprise Node\
\
Deactivate Enterprise Node\
\
Move Enterprise Node\
\
Merge Enterprise Nodes\
\
↓\
\
Events\
\
Enterprise Node Created\
\
Enterprise Node Updated\
\
Enterprise Node Archived\
\
↓\
\
APIs\
\
POST /enterprise-nodes\
\
GET /enterprise-nodes\
\
PUT /enterprise-nodes\
\
↓\
\
Screens\
\
Enterprise Explorer\
\
Enterprise Details\
\
Enterprise Hierarchy

The CIU groups all related implementation artifacts into a single
governed unit.

**3.6 CIU Dependency Rules**

A CIU may depend only on approved upstream CIUs.

Dependency categories include:

-   Parent Aggregate

-   Shared Business Object

-   Metadata Registry

-   Reference Data

-   Identity & Authorization

-   Enterprise Graph

-   Event Framework

Circular dependencies are prohibited.

**3.7 CIU Lifecycle**

Each CIU progresses through the following lifecycle.

Proposed\
│\
Architecture Approved\
│\
Implementation Planned\
│\
Development\
│\
Testing\
│\
Validated\
│\
Released\
│\
Operational\
│\
Deprecated\
│\
Retired

Lifecycle transitions shall be governed and auditable.

**3.8 CIU Ownership**

Every CIU shall have clearly defined ownership.

  -----------------------------------------------------------------------
  **Responsibility**               **Owner**
  -------------------------------- --------------------------------------
  Business Semantics               Business Domain Owner

  Architecture                     Enterprise Architect

  Implementation                   Development Team

  Metadata                         Data Steward

  Security                         Security Architect

  Testing                          QA Team

  AI Behaviour                     AI Governance Owner
  -----------------------------------------------------------------------

Ownership shall be explicit and documented.

**3.9 CIU Definition of Ready**

Implementation shall not begin until the CIU satisfies the following
criteria:

-   Business Domain approved.

-   Business Object registered.

-   Aggregate Root identified.

-   Metadata defined.

-   Business Activities approved.

-   Permissions defined.

-   Events identified.

-   API requirements approved.

-   Seed strategy determined.

-   Dependencies resolved.

This ensures implementation begins with a complete architectural
specification.

**3.10 CIU Definition of Done**

A CIU shall be considered complete only when:

-   Database schema implemented.

-   Migrations completed.

-   Metadata registered.

-   Seed data available (where applicable).

-   Business logic implemented.

-   APIs published.

-   Events implemented.

-   Authorization enforced.

-   Audit enabled.

-   Tests passed.

-   Documentation updated.

-   Architecture compliance validated.

Completion is based on architectural completeness rather than coding
completion.

**3.11 CIU Reuse Principle**

A CIU shall be reusable across multiple business capabilities.

Examples:

-   Person supports Identity, Workflow, Reporting, and Collaboration.

-   EnterpriseNode supports Business Resilience, Risk, Finance, Human Capital, and
    Operations.

-   Metric supports Reporting, Benchmarking, AI, and Analytics.

A CIU shall never be duplicated to satisfy domain-specific requirements.

**3.12 CIU Quality Gates**

Every CIU shall pass the following quality gates before release.

  -----------------------------------------------------------------------
  **Gate**             **Validation**
  -------------------- --------------------------------------------------
  Architecture         Alignment with Blueprint and architecture
                       standards

  Business             Business rules verified

  Data                 CMD-001 compliance

  Security             URA-001 compliance

  Enterprise Structure ERG-001 compliance

  Interaction          SD-003 compliance

  Metadata             Metadata completeness

  Testing              All automated tests passed

  Documentation        Documentation complete
  -----------------------------------------------------------------------

Failure of any mandatory gate shall prevent deployment.

**3.13 Architectural Enhancement (Major Recommendation)**

**Canonical Implementation Manifest (CIM)**

Every CIU should have a **Canonical Implementation Manifest**.

The manifest becomes the single implementation contract for Claude Code.

It should include:

-   Business Domain

-   Aggregate Root

-   Business Object

-   Primary Master Table

-   Supporting Tables

-   Reference Tables

-   Configuration Tables

-   Business Activities

-   Domain Events

-   APIs

-   Permissions

-   Metadata

-   UI Metadata

-   Seed Strategy

-   Test Requirements

-   Definition of Ready

-   Definition of Done

-   Dependencies

Claude Code should generate code **only from an approved Canonical
Implementation Manifest**, not by interpreting multiple architecture
documents independently.

**My Assessment**

I believe this section is one of the defining innovations of the
Aurex engineering methodology. By making the **Canonical
Implementation Unit (CIU)** the fundamental unit of implementation, the
platform becomes architecture-centric rather than technology-centric.
Every Business Object is implemented using a consistent, repeatable
pattern, making it easier for multiple development teams and AI coding
agents to work in parallel while preserving architectural integrity.

**IMP-001**

**Section 4 --- Repository Architecture & Project Structure**

**4.1 Purpose**

The Aurex repository structure shall organize source code according
to **Business Domains** and **Canonical Business Objects**, ensuring
that the physical implementation reflects the enterprise architecture.

The repository structure shall:

-   Preserve business ownership.

-   Minimize coupling.

-   Maximize reuse.

-   Support parallel development.

-   Enable AI-assisted implementation.

-   Prevent technology-driven decomposition.

The repository is therefore an implementation of the Business
Architecture.

**4.2 Architectural Principles**

The repository shall follow these principles:

**IMP-PS-001 --- Business Domain First**

Top-level organization shall be by Business Domain, never by technical
layer.

Examples:

-   Enterprise

-   Identity

-   Intelligence

-   Workflow

-   Reporting

-   AI

-   Platform

**IMP-PS-002 --- One Business Object, One Home**

Every Canonical Business Object shall exist in exactly one location.

Duplicate implementations are prohibited.

**IMP-PS-003 --- Shared Platform Services**

Cross-cutting capabilities shall reside only in the Platform layer.

Examples:

-   Metadata Engine

-   Audit

-   Event Bus

-   Authorization Framework

-   Notification Framework

-   AI Services

Business Domains consume these services but do not implement them
independently.

**IMP-PS-004 --- No Layer-Based Repositories**

The following structures are prohibited:

/controllers\
/services\
/repositories\
/models

at the repository root.

Instead, each Business Domain encapsulates its own implementation.

**4.3 Monorepo Structure**

Aurex shall use a single governed monorepository.

aurex/\
│\
├── platform/\
├── enterprise/\
├── identity/\
├── intelligence/\
├── workflow/\
├── reporting/\
├── ai/\
├── integrations/\
├── shared/\
├── infrastructure/\
├── ui/\
├── tests/\
├── tools/\
└── docs/

Each top-level folder represents either:

-   a Business Domain, or

-   a shared platform capability.

**4.4 Business Domain Structure**

Every Business Domain shall follow the same internal structure.

Example:

enterprise/\
│\
├── business_objects/\
├── activities/\
├── metadata/\
├── persistence/\
├── services/\
├── events/\
├── api/\
├── ui/\
├── tests/\
└── docs/

This standardization enables developers and AI agents to navigate any
domain consistently.

**4.5 Business Object Structure**

Each Business Object shall have its own dedicated module.

Example:

enterprise/\
└── business_objects/\
└── enterprise_node/\
├── aggregate.py\
├── entity.py\
├── repository.py\
├── service.py\
├── validator.py\
├── metadata.py\
├── permissions.py\
├── events.py\
├── api.py\
├── tests/\
└── README.md

The module is the physical realization of the Canonical Implementation
Unit.

**4.6 Platform Services**

Platform capabilities shall be centralized.

Examples:

platform/\
│\
├── metadata_engine/\
├── event_bus/\
├── authorization/\
├── audit/\
├── versioning/\
├── effective_dating/\
├── notification/\
├── ai_gateway/\
├── search/\
└── observability/

These services are reusable across all Business Domains.

**4.7 Shared Components**

The shared module shall contain only technology-neutral reusable assets.

Examples:

-   Value Objects

-   Common Enumerations

-   Error Models

-   Utility Libraries

-   Canonical DTOs

-   Common Validation Components

Business logic shall not be placed in the shared module.

**4.8 Infrastructure Layer**

The infrastructure layer provides technical capabilities.

Examples:

infrastructure/\
│\
├── database/\
├── messaging/\
├── storage/\
├── cache/\
├── identity_provider/\
├── configuration/\
├── monitoring/\
└── deployment/

No business rules shall be implemented in this layer.

**4.9 User Interface Structure**

The UI shall mirror the Business Domains.

Example:

ui/\
│\
├── enterprise/\
├── identity/\
├── intelligence/\
├── workflow/\
├── reporting/\
├── ai/\
└── shared/

Screens consume Business Activities and APIs; they never access
persistence directly.

**4.10 Documentation Structure**

Each Business Domain shall maintain its own implementation
documentation.

Minimum artifacts:

-   Overview

-   Business Object catalog

-   API reference

-   Event catalog

-   Activity catalog

-   Configuration guide

-   Test guide

This keeps documentation aligned with implementation.

**4.11 Dependency Rules**

Dependencies shall always flow inward toward shared platform
capabilities.

UI\
↓\
Business Domain\
↓\
Platform Services\
↓\
Infrastructure

Forbidden dependencies include:

-   Business Domain → Another Business Domain (direct database access)

-   UI → Database

-   UI → Repository

-   Infrastructure → Business Logic

All cross-domain communication shall occur through APIs, events, or
approved shared services.

**4.12 Naming Standards**

To ensure consistency:

-   Folders: snake_case

-   Python modules: snake_case

-   Classes: PascalCase

-   Functions: snake_case

-   Constants: UPPER_SNAKE_CASE

-   Business Object identifiers: singular nouns (e.g., metric, person,
    enterprise_node)

-   Business Activity modules: verb-noun (e.g., publish_report,
    assign_role)

Naming must reflect business semantics rather than technical
implementation.

**4.13 AI-Friendly Repository Design**

The repository shall be organized to optimize AI-assisted development.

Every Business Object module should contain:

-   A concise README.md describing the Business Object.

-   References to the governing architecture documents.

-   The Canonical Implementation Manifest (CIM).

-   Public API definitions.

-   Event definitions.

-   Metadata definitions.

-   Test coverage summary.

This enables AI tools such as Claude Code to understand context without
scanning unrelated parts of the repository.

**Architectural Enhancement (Recommended)**

**Canonical Implementation Manifest (CIM) File**

In addition to code, each Business Object should include a
machine-readable manifest (for example, YAML or JSON) containing:

-   Business Domain

-   Business Object

-   Aggregate Root

-   Primary Master Table

-   Supporting Tables

-   APIs

-   Business Activities

-   Events

-   Permissions

-   Dependencies

-   Seed Strategy

-   Definition of Done

Claude Code can use this manifest as the authoritative implementation
contract, ensuring consistent generation across all Business Objects.

**My Assessment**

I believe this repository structure is significantly stronger than a
conventional layer-based organization because it mirrors the enterprise
architecture rather than the technology stack. It encourages high
cohesion within Business Domains, reduces coupling, and gives both human
developers and AI coding agents a predictable, repeatable implementation
pattern.

**One important refinement before we continue**

Before writing **Section 5 -- Business Domain Implementation Pattern**,
I recommend we make one strategic decision that will influence the
entire implementation:

**Should Aurex be implemented as:**

1.  **A Modular Monolith** (one deployable application composed of
    well-defined Business Domain modules), with the option to extract
    services later.

**or**

2.  **Microservices from Day One**, where each Business Domain is a
    separate deployable service.

Based on everything we\'ve designed---metadata-driven architecture,
shared registries, enterprise graph, AI, and the current scope---my
recommendation is **Modular Monolith first**.

It aligns with the architecture, simplifies development and testing,
reduces operational complexity, and still allows individual Business
Domains to be extracted into microservices in the future if scale or
organizational needs require it. I believe this approach offers the best
balance between architectural purity and practical execution for
Aurex Version 1.0.

**IMP-001**

**Section 5 --- Canonical Business Object Implementation Pattern
(CBIP)**

**5.1 Purpose**

The Canonical Business Object Implementation Pattern (CBIP) defines the
mandatory engineering blueprint for implementing every Canonical
Business Object within the Aurex Intelligent Operating Center.

The objective is to ensure that every Business Object:

-   Is implemented consistently.

-   Is architecture compliant.

-   Is independently testable.

-   Supports metadata-driven behavior.

-   Integrates with Enterprise Graph, Authorization, Workflow and AI.

-   Can be implemented by either human developers or AI coding agents
    using the same repeatable methodology.

The CBIP is mandatory for all Business Objects.

**5.2 Fundamental Principle**

Every Business Object shall be implemented using the same canonical
engineering pattern.

No Business Object may introduce its own implementation model.

The Business Object is the primary engineering unit.

Database tables, APIs, workflows and screens are implementation
artifacts derived from the Business Object.

**5.3 Canonical Business Object Stack**

Every Business Object shall contain the following mandatory layers.

Business Object\
│\
Aggregate Root\
│\
Metadata\
│\
Business Rules\
│\
Validation\
│\
Persistence\
│\
Repository\
│\
Domain Service\
│\
Business Activities\
│\
Events\
│\
Authorization\
│\
API\
│\
UI Metadata\
│\
Screen\
│\
Testing

The order is mandatory.

No downstream layer shall redefine upstream business semantics.

**5.4 Business Object Template**

Every Business Object shall include the following implementation
artifacts.

  -----------------------------------------------------------------------
  **Artifact**                                **Mandatory**
  ------------------------------------------- ---------------------------
  Aggregate Root                              ✓

  Entity Model                                ✓

  Value Objects                               ✓ (if applicable)

  Metadata Definition                         ✓

  Business Rule Specification                 ✓

  Validation Rules                            ✓

  Repository                                  ✓

  Domain Service                              ✓

  Business Activity Handlers                  ✓

  Event Definitions                           ✓

  Authorization Policy                        ✓

  API Contract                                ✓

  UI Metadata                                 ✓

  Seed Data Definition                        Where applicable

  Test Suite                                  ✓

  Documentation                               ✓
  -----------------------------------------------------------------------

**5.4a Canonical Name vs. Implementation Name** *(formalized per ADR-014 — METH-001)*

A registered Canonical Business Object's own CMD-001 §26.4 Canonical Name is not required to be the name of its implementing class. An implementation MAY use a more code-idiomatic class name, provided the model's own docstring discloses both names and cross-references the Business Object's own CMD-001 identifier.

This is an established, already-proven practice, not a new obligation: every WP-04 Structural Context Lifecycle object (`StructuralChangeIntent` for Structural Change Intent/SCI-000001, `StructuralProposal` for Proposed Outcome Context/POC-000001, `ImpactAssessment` for Impact Context/IMC-000001, `StructuralReview` for Review Context/RVC-000001, `StructuralValidation` for Validation Context/VLC-000001, `StructuralCompletion` for Resulting Structural Context/RSC-000001) already follows this pattern. This subsection formalizes it rather than introducing it.

**5.5 Aggregate Root**

Every Business Object shall identify exactly one Aggregate Root.

The Aggregate Root:

-   owns consistency

-   enforces invariants

-   manages lifecycle

-   coordinates related entities

External components shall interact only through the Aggregate Root.

**5.6 Metadata-Driven Behavior**

Business behavior shall be externalized into metadata wherever feasible.

Examples:

-   Validation

-   Display

-   Search

-   Workflow

-   Approval

-   Visibility

-   Localization

-   AI Prompts

Implementation code shall consume metadata rather than hardcoding
behavior.

**5.7 Business Activities**

Business Objects shall expose Business Activities instead of CRUD
operations.

Example:

**Metric**

Instead of:

-   Create

-   Update

-   Delete

Expose:

-   Define Metric

-   Publish Metric

-   Archive Metric

-   Assign Owner

-   Map Framework

-   Review Quality

Business Activities express business intent.

**5.8 Persistence Pattern**

Every Business Object shall designate:

-   One Primary Master Table

-   Zero or more Supporting Tables

-   Reference Tables

-   Relationship Tables

-   Transaction Tables

The Business Object shall not expose physical storage details to
consuming layers.

**5.9 Event Pattern**

Every Business Object shall publish meaningful domain events.

Examples:

Metric Defined\
Metric Published\
Metric Retired\
Metric Ownership Changed\
Framework Mapping Updated

Events shall describe business facts rather than technical operations.

**5.10 Authorization Pattern**

Every Business Activity shall define:

-   Required Permission

-   Node Scope

-   Role Requirements

-   Delegation Rules

-   Approval Requirements

Authorization shall be evaluated before execution of business logic.

**5.11 API Pattern**

APIs are façades over Business Activities.

APIs shall never manipulate persistence directly.

Example:

POST /metrics/{id}/publish

rather than

PUT /metric

The API expresses the business action.

**5.12 UI Pattern**

Screens consume:

-   Business Activities

-   Metadata

-   Authorization

-   APIs

Screens shall never:

-   contain business rules

-   access repositories

-   manipulate database tables directly

The UI is a presentation layer only.

**5.13 Testing Pattern**

Every Business Object shall include:

-   Unit Tests

-   Business Rule Tests

-   Validation Tests

-   Authorization Tests

-   API Tests

-   Event Tests

-   Integration Tests

Testing shall focus on business behavior rather than implementation
details.

**5.14 Definition of Complete**

A Business Object is complete only when:

-   Aggregate implemented.

-   Metadata registered.

-   Validation complete.

-   Repository implemented.

-   Business Activities implemented.

-   Events published.

-   Authorization enforced.

-   APIs documented.

-   UI metadata available.

-   Seed data defined (where applicable).

-   Tests passing.

-   Documentation complete.

No Business Object is complete based solely on successful compilation.

**5.15 Canonical Business Object Manifest (CBOM)**

Every Business Object shall include a machine-readable **Canonical
Business Object Manifest**.

The CBOM shall contain:

  -----------------------------------------------------------------------
  **Attribute**                  **Description**
  ------------------------------ ----------------------------------------
  Business Domain                Owning domain

  Business Object                Canonical name

  Aggregate Root                 Aggregate

  Primary Master Table           System of Record

  Supporting Tables              Related persistence

  Reference Tables               Lookup dependencies

  Business Activities            Supported actions

  Events                         Published and consumed

  Permissions                    Required authorizations

  APIs                           Service contracts

  UI Components                  Consuming screens

  Seed Strategy                  Platform, Tenant or Runtime

  Dependencies                   Upstream/downstream

  Version                        Manifest version
  -----------------------------------------------------------------------

The CBOM is the single implementation contract consumed by Claude Code.

**5.16 Architectural Enhancement (Major Recommendation)**

**Business Object Generator (BOG)**

Rather than asking Claude Code to interpret multiple architecture
documents, I recommend introducing a **Business Object Generator
(BOG)**.

The generator would read the **CBOM** and automatically scaffold:

-   Database migrations

-   SQLAlchemy models

-   Repositories

-   Domain services

-   FastAPI routers

-   OpenAPI definitions

-   Event classes

-   Authorization policies

-   UI metadata

-   Test skeletons

-   Documentation

Developers would then complete the business logic rather than creating
boilerplate from scratch.

This keeps implementation consistent and dramatically accelerates
delivery.

**My Assessment**

I believe this is the **single most valuable section of IMP-001**
because it defines the universal engineering pattern for every Business
Object in Aurex. If every implementation follows this Canonical
Business Object Implementation Pattern and is driven by a **Canonical
Business Object Manifest**, Claude Code can generate highly consistent,
architecture-compliant code across the entire platform with minimal
interpretation. It also creates a clear separation between business
semantics (defined by the architecture) and implementation mechanics
(defined by IMP-001), which is essential for maintaining architectural
integrity as the platform grows.

**Section 6 --- Canonical Business Activity Implementation Pattern
(CBAIP)**

**IMP-001**

**Section 6 --- Canonical Business Activity Implementation Pattern
(CBAIP)**

**6.1 Purpose**

The Canonical Business Activity Implementation Pattern (CBAIP) defines
the mandatory engineering methodology for implementing every Business
Activity within the Aurex Intelligent Operating Center.

Business Activities are the executable realization of business intent.

They encapsulate:

-   Business rules

-   Authorization

-   Validation

-   Workflow

-   Event publication

-   Audit

-   AI assistance

-   Persistence

Every user interaction, API request, workflow step, integration, or AI
recommendation shall ultimately execute one or more Business Activities.

**6.2 Architectural Principle**

Aurex is an **Activity-Driven Platform**.

Implementation shall be organized around Business Activities rather than
CRUD operations.

The platform executes business intent.

It does not execute database operations.

**6.2a Business Activity Readiness Discovery** *(formalized per ADR-014 — METH-001)*

Before a Business Activity's own Implementation Readiness Assessment (IRA) begins implementation planning, it shall perform a bounded Context Discovery scan of the governing Enterprise Experience specification.

**Scan procedure.** Read the specification's own table of contents / section-header list only (not a full-text re-read) and identify any chapter analogous to a named, cross-cutting Context/Object/Data Model declaration — a section that declares, in one place, the full set of Business Objects, Contexts, or data constructs a capability's Enterprise Experiences produce and consume across their lifecycle (for example, PE-001-C005 §38.15's "C-005 Context Model"). If such a section exists, every construct it names shall be tested against CMD-001 §26.3a's eligibility procedure in this one pass, before the first Business Activity of the Work Package begins implementation — not discovered piecemeal, one Business Activity at a time, as each construct is separately encountered.

**Secondary trigger.** Where no such named section exists, the same scan is still required if the capability's own Enterprise Requirement Breakdown (ERB) analysis describes a generic, multi-stage journey shape (e.g., propose → assess → review → validate → complete) rather than a set of independent lifecycle verbs. A generic journey shape is itself evidence that intermediate stage outputs are likely to be Business Objects consumed downstream, and the same upfront scan applies.

This is a bounded procedure, not an open-ended architectural review: it identifies candidate constructs for CMD-001 §26.3a's own eligibility test to evaluate; it does not itself decide eligibility, and it does not substitute for the Work Package's own per-Business-Activity Implementation Readiness Assessment.

**6.2b Gap Analysis Category Scheme (A–E)** *(canonicalized per ADR-014 — METH-001)*

Every Implementation Readiness Assessment (IRA-001 through IRA-004) has classified each Business Activity's own readiness against a five-point A–E scale, by convention, since IRA-001. This scale was never itself defined in a canonical document; this subsection canonicalizes it as observed and applied, without changing its meaning.

The scale is ordered from least to most blocking, mirroring CLAUDE.md §19.5's own Reuse → Configure → Extend → Compose → Create ordering:

-   **A — Reuse.** No gap. An existing implementation satisfies the Business Activity as-is.
-   **B — Existing implementation can be reused.** A direct extension point exists (e.g., an existing repository's inherited method, an existing response model) and requires no new architectural or constitutional groundwork.
-   **C — Architecture requires completion (implementation-level).** Ordinary implementation-level design work remains (persistence mechanism, endpoint shape, service/repository composition), but no open constitutional or governance question blocks it.
-   **D — Governance clarification required.** An open constitutional or architectural question (e.g., an undetermined Canonical Business Object eligibility question, an undetermined target-type scope) must be resolved — typically via an Architecture Decision Record — before implementation-level design can proceed with confidence.
-   **E — Genuine STOP condition.** No path forward exists without further approval; implementation shall not proceed. (No Business Activity across WP-01 through WP-04 has yet met this category.)

**Constitutional-vs-Implementation blocker distinction.** Categories D and C are distinguished by the *kind* of open question, not merely its difficulty. A category **D** finding is a constitutional blocker: it requires a governance decision (an ADR, a Business Object registration, a canonical scope decision) because the answer is not yet architecturally determined. A category **C** finding is an implementation blocker: the architecture is already determined, and what remains is ordinary engineering design. WP-04's own six Business Activities (BA-03 through BA-08) each began at category D pending a Business Object registration or scope decision and were reclassified to C once the relevant ADR was adopted. **This reclassification does not by itself authorize implementation.** A fresh, Business-Activity-specific implementation-readiness gap analysis is still required after any D→C reclassification, per CLAUDE.md §19.7.

**6.3 Business Activity Lifecycle**

Every Business Activity follows the same execution lifecycle.

Request\
│\
Authorization\
│\
Business Validation\
│\
Business Rule Execution\
│\
Metadata Resolution\
│\
Workflow Evaluation\
│\
Business Object Update\
│\
Domain Event Publication\
│\
Audit Recording\
│\
Response

This lifecycle is mandatory.

**6.4 Business Activity Components**

Every Business Activity shall include the following components.

  -----------------------------------------------------------------------
  **Component**                                     **Mandatory**
  ------------------------------------------------- ---------------------
  Business Activity Definition                      ✓

  Business Intent                                   ✓

  Input Contract                                    ✓

  Output Contract                                   ✓

  Business Rules                                    ✓

  Validation Rules                                  ✓

  Authorization Rules                               ✓

  Metadata Dependencies                             ✓

  Workflow Dependencies                             ✓

  Domain Events                                     ✓

  Audit Requirements                                ✓

  AI Assistance Points                              Optional

  Error Handling                                    ✓

  Tests                                             ✓
  -----------------------------------------------------------------------

**6.5 Business Activity Template**

Every Business Activity shall follow a standard implementation template.

Business Activity\
│\
Business Intent\
│\
Input Validation\
│\
Authorization\
│\
Business Rules\
│\
Metadata Evaluation\
│\
Workflow Coordination\
│\
Business Object Changes\
│\
Event Publication\
│\
Audit Recording\
│\
Response Generation

This template is universal.

**6.6 Business Activity Types**

Business Activities fall into one of the following categories.

  -----------------------------------------------------------------------
  **Type**             **Description**
  -------------------- --------------------------------------------------
  Create               Establish a new business entity

  Update               Modify business state

  Approve              Human approval

  Reject               Human rejection

  Assign               Responsibility assignment

  Review               Governance review

  Publish              Release business information

  Calculate            Execute business calculations

  Synchronize          External integration

  Analyze              AI or analytics processing

  Archive              Controlled retirement

  Restore              Reinstatement

  Monitor              Continuous observation

  Notify               Communication
  -----------------------------------------------------------------------

Additional activity types may be introduced through governance.

**6.7 Business Activity Contract (BAC)**

Every Business Activity shall have a Business Activity Contract.

The contract shall include:

  -----------------------------------------------------------------------
  **Attribute**                    **Description**
  -------------------------------- --------------------------------------
  Activity Identifier              Unique ID

  Business Domain                  Owning domain

  Business Object                  Target object

  Activity Type                    Category

  Business Intent                  Purpose

  Input Contract                   Required inputs

  Output Contract                  Expected outputs

  Preconditions                    Required state

  Postconditions                   Expected state

  Authorization                    Required permissions

  Events                           Published events

  Workflow                         Related workflow

  Audit                            Required audit trail

  AI Assistance                    Optional AI behavior

  Definition of Done               Completion criteria

  Idempotency                      Guarded or idempotent transition
                                    disclosure (required for any write
                                    endpoint callable twice against the
                                    same target — see §6.7a)
  -----------------------------------------------------------------------

The BAC is the authoritative specification for implementation.

**6.7a Business Activity Resume Protocol (Informative)** *(formalized per ADR-014 — METH-001)*

This subsection is informative, not normative. It documents an already-proven practice from WP-04; its absence does not by itself produce an incorrect implementation, so it is not a mandatory gate.

For a write endpoint callable twice against the same target, the BAC's own Idempotency attribute shall disclose which of two patterns the Business Activity uses:

-   **Guarded transition.** The second call is rejected (e.g., an already-resolved `StructuralReview`'s concerns cannot be resolved again). Enforced by both a service-layer pre-check and a database-level uniqueness constraint, so that a race between two concurrent calls still fails safely at the database if the service-layer check is bypassed. WP-04's `StructuralReview.resolve_concerns` and `StructuralCompletion.complete_structural_transition` both use this pattern.
-   **Idempotent transition.** The second call returns the same outcome as the first without error (e.g., re-requesting an already-generated read-only response).

A Business Activity that resumes after an interruption (per CLAUDE.md §19's own Repository Reconstruction / Interruption Analysis phases) shall re-derive its own current state from the repository before continuing, and its own write path's guarded-or-idempotent disclosure determines whether a resumed call that partially succeeded before the interruption is safe to simply retry.

**6.8 Business Activity Granularity**

Business Activities shall be business-meaningful.

Preferred examples:

-   Publish Intelligence Foundation Document

-   Assign Metric Owner

-   Approve Evidence

-   Link Enterprise Node

-   Evaluate Material Topic

-   Consolidate Financial Results

Avoid technical activities such as:

-   Update Row

-   Save Record

-   Delete Entry

Business Activities express business value.

**6.9 Workflow Integration**

Business Activities may participate in workflows.

Workflow engines coordinate activities.

Business Activities remain independently executable.

Workflows orchestrate.

Activities execute.

**6.10 Event Integration**

Every successful Business Activity shall publish one or more Domain
Events.

Examples:

Evidence Approved\
\
↓\
\
EvidenceApprovalCompleted

Events communicate business outcomes rather than technical operations.

**6.11 Authorization Integration**

Authorization shall be evaluated before business execution.

Authorization considers:

-   User

-   Role

-   Permission

-   Enterprise Node

-   Assignment

-   Delegation

-   Approval Authority

Business Activities shall not embed authorization logic directly.

They shall invoke the centralized authorization framework.

**6.12 AI Assistance**

AI may assist Business Activities by:

-   Extracting information

-   Recommending actions

-   Identifying anomalies

-   Drafting narratives

-   Suggesting approvals

-   Predicting outcomes

AI shall not execute Business Activities autonomously unless explicitly
permitted by governance.

**6.13 Testing Requirements**

Every Business Activity shall include:

-   Positive path tests

-   Negative path tests

-   Authorization tests

-   Workflow tests

-   Event publication tests

-   Audit verification tests

-   Performance tests

-   AI validation tests (where applicable)

Testing shall validate business outcomes rather than code paths.

**6.14 Canonical Business Activity Manifest (CBAM)**

Every Business Activity shall include a machine-readable manifest.

The manifest shall contain:

-   Business Domain

-   Business Object

-   Activity Name

-   Activity Type

-   Business Intent

-   Input Contract

-   Output Contract

-   Business Rules

-   Authorization Requirements

-   Workflow Integration

-   Events

-   Metadata Dependencies

-   AI Assistance

-   Test Requirements

-   Version

Claude Code shall use the CBAM as the implementation contract for
Business Activities.

**Editorial Note (WP-7 Repository Hygiene):** Sections 6.15 through 6.30 originally appeared twice in this document — first as an architect's restructuring recommendation and outline summary, then again as the fully detailed specification. The two copies shared section numbers (6.15–6.30), which CR-3.0 identified as a duplicate-numbering defect. The recommendation was accepted and fully realized in the detailed sections below; the outline copy added no content beyond what the detailed sections already state in full, and has been removed here as superseded scaffolding. The recommendation's original rationale is preserved below.

*Rationale (originally recorded alongside the recommendation to introduce the Business Activity Engine as a core platform capability, rather than having each domain implement activity execution independently): this is one of the defining differentiators of Aurex. Most enterprise systems are entity-centric or CRUD-centric; Aurex is Business Activity-centric. Standardizing every executable operation through the Canonical Business Activity Implementation Pattern and the Business Activity Engine gives the platform consistent behavior, centralized governance, and a predictable execution model aligned with SD-002, SD-003, URA-001, ERG-001, and CMD-001. SD-002 defines what the platform manages (Business Objects); URA-001 defines who can perform operations; ERG-001 defines where operations occur; CMD-001 defines what data is manipulated; IMP-001 defines how business intent is executed — completing the architectural foundation.*

**6.15 Business Activity Engine (BAE)**

**6.15.1 Purpose**

The **Business Activity Engine (BAE)** is the canonical execution engine
for all Business Activities within the Aurex Intelligent Operating
Center.

The BAE provides a standardized execution pipeline that ensures every
Business Activity behaves consistently regardless of the owning Business
Domain.

Rather than each domain independently implementing authorization,
validation, workflow coordination, event publication, auditing,
transaction management, or AI integration, these capabilities shall be
provided centrally by the Business Activity Engine.

Business Domains shall implement only their domain-specific business
logic.

The Business Activity Engine shall manage the complete execution
lifecycle.

**6.15.2 Architectural Principle**

Business Activities represent business intent.

The Business Activity Engine executes business intent.

Business Domains supply business rules.

The engine supplies execution.

This separation establishes a consistent execution model across the
entire platform.

**6.15.3 Platform Position**

The Business Activity Engine is a Core Platform Service.

Every executable operation initiated by:

-   User Interface

-   REST APIs

-   Internal Services

-   Workflow Engine

-   Event Subscribers

-   AI Services

-   Scheduled Jobs

-   Integration Connectors

-   Batch Processes

shall execute through the Business Activity Engine.

No component shall bypass the engine to directly modify Business
Objects.

**6.15.4 Architectural Responsibilities**

The Business Activity Engine shall provide the following platform
capabilities.

  -----------------------------------------------------------------------
  **Capability**             **Responsibility**
  -------------------------- --------------------------------------------
  Activity Resolution        Locate the Business Activity implementation

  Context Initialization     Build execution context

  Authorization              Invoke centralized authorization framework

  Input Validation           Validate contracts

  Metadata Resolution        Resolve metadata dependencies

  Workflow Coordination      Invoke workflow engine

  Transaction Management     Manage transaction lifecycle

  Business Rule Execution    Execute domain logic

  Persistence Coordination   Persist Business Object changes

  Event Publication          Publish Domain Events

  Notification Integration   Trigger notifications where applicable

  Audit Recording            Create immutable audit trail

  AI Assistance              Invoke AI assistance hooks

  Response Generation        Produce standardized responses

  Error Handling             Apply canonical error management

  Observability              Capture metrics, tracing and logs
  -----------------------------------------------------------------------

**6.15.5 Architectural Model**

User Interface\
│\
REST API\
│\
Integration Services\
│\
Workflow Engine\
│\
AI Services\
│\
Scheduled Jobs\
│\
──────────────────────────────────────\
Business Activity Engine\
──────────────────────────────────────\
\
Context Resolution\
\
↓\
\
Authorization\
\
↓\
\
Validation\
\
↓\
\
Metadata Resolution\
\
↓\
\
Workflow Coordination\
\
↓\
\
Business Rule Execution\
\
↓\
\
Persistence\
\
↓\
\
Transaction Management\
\
↓\
\
Event Publication\
\
↓\
\
Notification\
\
↓\
\
Audit Recording\
\
↓\
\
AI Assistance\
\
↓\
\
Response Generation\
──────────────────────────────────────\
\
Business Objects\
\
Metadata\
\
Workflows\
\
Events\
\
Audit\
\
Knowledge Graph

The Business Activity Engine shall be the exclusive execution path for
Business Activities.

**6.15.6 Business Domain Responsibility**

Business Domains shall implement only business-specific logic.

They shall not independently implement:

-   Authorization

-   Workflow execution

-   Audit recording

-   Event publication

-   Metadata resolution

-   Transaction management

-   Notification dispatch

-   AI orchestration

-   Logging

-   Correlation management

These capabilities belong exclusively to the Business Activity Engine.

**6.15.7 Execution Consistency**

Every Business Activity shall execute through the same execution
pipeline irrespective of:

-   Business Domain

-   Business Object

-   Activity Type

-   Deployment Model

-   Invocation Method

-   User Interface

-   API Version

-   Integration Source

Execution consistency is a constitutional architectural principle.

**6.15.8 Extension Model**

The Business Activity Engine shall expose extension points without
requiring modification of the engine itself.

Supported extension points include:

-   Custom Validators

-   Business Rule Processors

-   Metadata Providers

-   Workflow Adapters

-   Event Publishers

-   Notification Providers

-   AI Assistants

-   Audit Enrichers

-   Monitoring Extensions

Platform capabilities shall be extensible through registration rather
than engine customization.

**6.15.9 Domain Independence**

The Business Activity Engine shall remain independent of individual
Business Domains.

It shall have no knowledge of:

-   Business Resilience

-   Finance

-   Risk

-   Legal

-   Human Capital

-   Supply Chain

-   Enterprise Structure

-   Reporting

Domain knowledge shall exist exclusively within Business Activity
implementations.

The engine shall execute Business Activities without understanding their
business semantics.

**6.15.10 Governance Principle**

The Business Activity Engine is a constitutional platform component.

All executable business operations shall be governed through the engine.

No Business Domain, API, Workflow, AI Service, Integration Connector, or
User Interface shall directly manipulate Business Objects outside the
execution pipeline managed by the Business Activity Engine.

This guarantees:

-   Consistent authorization

-   Uniform validation

-   Standardized auditing

-   Predictable event publication

-   Controlled workflow execution

-   Complete observability

-   Platform-wide governance

-   Uniform business behavior

The Business Activity Engine establishes the canonical execution model
for the Aurex Intelligent Operating Center and is mandatory for
every Business Activity implementation.

**6.16 Business Activity Execution Pipeline**

**6.16.1 Purpose**

The Business Activity Execution Pipeline defines the mandatory runtime
sequence executed by the Business Activity Engine for every Business
Activity.

The pipeline establishes a single, predictable execution model across
the entire platform, ensuring that every Business Activity executes with
consistent governance, security, observability, auditability, and
business behavior.

Regardless of the Business Domain, Business Object, Activity Type, or
invocation mechanism, every Business Activity shall execute through the
canonical execution pipeline.

**6.16.2 Architectural Principle**

Business Activities execute through a standardized pipeline.

The pipeline owns execution.

Business Activities contribute only business-specific decision logic.

The execution sequence shall remain independent of:

-   Business Domain

-   User Interface

-   API implementation

-   Workflow definition

-   Integration technology

-   AI provider

-   Deployment architecture

Execution order is a constitutional platform standard.

**6.16.3 Canonical Execution Pipeline**

Every Business Activity shall execute through the following sequence.

Request Reception\
│\
Activity Resolution\
│\
Execution Context Initialization\
│\
Authorization Evaluation\
│\
Input Contract Validation\
│\
Business Validation\
│\
Metadata Resolution\
│\
Workflow Resolution\
│\
Business Rule Execution\
│\
Persistence Coordination\
│\
Transaction Commit\
│\
Domain Event Publication\
│\
Notification Processing\
│\
Audit Recording\
│\
AI Assistance Hooks\
│\
Response Generation

No stage may be bypassed unless explicitly designated as optional by the
Business Activity Contract.

**6.16.4 Stage Responsibilities**

  -----------------------------------------------------------------------
  **Stage**               **Responsibility**
  ----------------------- -----------------------------------------------
  Request Reception       Accept invocation from any supported channel

  Activity Resolution     Resolve the registered Business Activity

  Context Initialization  Build execution context

  Authorization           Validate access rights

  Input Validation        Validate request contract

  Business Validation     Validate business state and preconditions

  Metadata Resolution     Resolve configuration, reference and policy
                          metadata

  Workflow Resolution     Determine workflow participation

  Business Rule Execution Execute domain-specific business logic

  Persistence             Apply Business Object updates
  Coordination            

  Transaction Commit      Commit successful transaction

  Domain Event            Publish business outcome events
  Publication             

  Notification Processing Trigger user or system notifications

  Audit Recording         Persist immutable audit record

  AI Assistance Hooks     Invoke AI assistance where configured

  Response Generation     Produce standardized response
  -----------------------------------------------------------------------

**6.16.5 Activity Resolution**

The Business Activity Engine shall resolve the requested Business
Activity using the Business Activity Registry.

Resolution shall verify:

-   Activity Identifier

-   Activity Version

-   Activity Status

-   Supported Invocation Method

-   Business Domain

-   Required Platform Version

Activities that cannot be resolved shall terminate before execution
begins.

**6.16.6 Context Initialization**

The Business Activity Engine shall construct a complete execution
context before business processing begins.

The execution context shall be immutable throughout the Business
Activity lifecycle except for runtime metrics and execution state.

Context construction shall occur exactly once.

No Business Activity shall independently create execution context.

**6.16.7 Authorization Evaluation**

Authorization shall be completed before any business processing.

Authorization shall invoke the centralized authorization framework
defined by URA-001.

Authorization decisions may consider:

-   Person

-   Identity

-   Membership

-   Business Role

-   Approval Authority

-   Enterprise Node

-   Delegation

-   Runtime Assignment

-   Organization

-   Business Object

-   Business Activity

-   Requested Operation

Business Activities shall never implement authorization logic
internally.

**6.16.8 Validation Pipeline**

Validation consists of two distinct phases.

**Technical Validation**

Verifies:

-   Input Contract

-   Required fields

-   Data types

-   Format rules

-   Mandatory attributes

-   Schema compliance

**Business Validation**

Verifies:

-   Business Preconditions

-   Business State

-   Policy Constraints

-   Regulatory Rules

-   Configuration Rules

-   Workflow Requirements

Technical validation verifies correctness.

Business validation verifies legitimacy.

**6.16.9 Metadata Resolution**

Before business logic executes, the engine shall resolve all required
metadata.

Examples include:

-   Configuration Values

-   Business Rules

-   Approval Policies

-   Enterprise Policies

-   Reference Data

-   Canonical Definitions

-   Thresholds

-   Feature Flags

-   AI Policies

-   Notification Policies

Business Activities shall consume metadata.

They shall not own metadata.

**6.16.10 Workflow Resolution**

The engine shall determine whether the Business Activity participates in
a workflow.

Possible outcomes include:

-   Standalone execution

-   Workflow initiation

-   Workflow continuation

-   Approval step

-   Escalation

-   Parallel execution

-   Workflow completion

Business Activities remain independently executable regardless of
workflow participation.

**6.16.11 Business Rule Execution**

Business Rule Execution is the only stage implemented by Business
Domains.

Business logic shall:

-   Evaluate business rules

-   Modify Business Objects

-   Produce business outcomes

-   Request AI assistance where permitted

-   Produce Domain Events

Business logic shall not:

-   Perform authorization

-   Manage transactions

-   Publish events directly

-   Write audit records

-   Invoke workflow engines

-   Send notifications

These responsibilities remain with the Business Activity Engine.

**6.16.12 Persistence Coordination**

The engine shall coordinate persistence of all Business Object changes.

Persistence responsibilities include:

-   Business Object updates

-   Version management

-   Optimistic concurrency

-   State transitions

-   Metadata updates

-   Relationship updates

-   Integrity validation

Business Activities manipulate Business Objects.

The engine persists them.

**6.16.13 Transaction Management**

All persistence operations shall execute within a controlled business
transaction.

The engine shall guarantee:

-   Atomic execution

-   Consistent state

-   Isolation

-   Durability

Partial updates shall not be committed.

If execution fails before transaction completion, all Business Object
modifications shall be rolled back unless a defined compensation
strategy applies.

**6.16.14 Post-Commit Processing**

The following activities shall occur only after successful transaction
commitment:

-   Domain Event Publication

-   Notification Processing

-   Audit Recording

-   AI Assistance Hooks

-   Analytics Updates

-   Monitoring Updates

Business outcomes shall never be communicated before successful
commitment.

**6.16.15 Response Generation**

The Business Activity Engine shall produce a standardized response.

Responses may include:

-   Activity Result

-   Updated Business Object

-   Workflow Status

-   Generated Events

-   Messages

-   Warnings

-   AI Recommendations

-   Correlation Identifier

-   Execution Duration

Responses shall remain independent of transport protocols.

**6.16.16 Execution Guarantees**

The Business Activity Execution Pipeline guarantees:

-   Consistent execution order

-   Uniform authorization

-   Standardized validation

-   Centralized transaction management

-   Reliable event publication

-   Immutable audit recording

-   Controlled AI integration

-   Complete observability

-   Platform-wide governance

Every Business Activity executed within the Aurex Intelligent
Operating Center shall follow this canonical execution pipeline without
exception.

**6.17 Business Activity Context (BACX)**

**6.17.1 Purpose**

Every Business Activity shall execute within a standardized **Business
Activity Context (BACX)**.

The Business Activity Context represents the complete runtime
environment required to execute a Business Activity consistently across
the platform.

Rather than each Business Activity independently discovering user
identity, organization, permissions, workflow state, enterprise context,
configuration, or runtime metadata, the Business Activity Engine shall
construct and inject a fully populated Business Activity Context before
execution begins.

The Business Activity Context becomes the authoritative runtime context
for the duration of the Business Activity.

**6.17.2 Architectural Principle**

Business Activities shall consume context.

They shall not construct context.

The Business Activity Engine owns context creation.

Business Activities remain stateless with respect to execution
environment.

**6.17.3 Context Ownership**

The Business Activity Engine is solely responsible for:

-   Creating the Business Activity Context

-   Validating context integrity

-   Populating runtime information

-   Maintaining execution metadata

-   Passing context to Business Activities

-   Managing correlation across services

Business Domains shall never construct or modify execution context.

**6.17.4 Context Lifecycle**

The Business Activity Context follows the lifecycle below.

Incoming Request\
│\
Business Activity Engine\
│\
Context Construction\
│\
Context Validation\
│\
Business Activity Execution\
│\
Context Enrichment\
(Runtime Metrics Only)\
│\
Execution Complete\
│\
Context Archived

The Business Activity Context exists only for the lifetime of the
Business Activity execution.

It is not persisted as a Business Object unless explicitly required for
audit or diagnostic purposes.

**6.17.5 Canonical Context Structure**

Every Business Activity Context shall include the following logical
sections.

  -----------------------------------------------------------------------
  **Section**                      **Purpose**
  -------------------------------- --------------------------------------
  Activity Context                 Activity metadata

  Identity Context                 User identity

  Organization Context             Organizational scope

  Enterprise Context               Enterprise node scope

  Authorization Context            Runtime permissions

  Workflow Context                 Workflow execution state

  Request Context                  Request metadata

  Transaction Context              Transaction metadata

  AI Context                       AI execution information

  Runtime Context                  Observability information
  -----------------------------------------------------------------------

The exact implementation may evolve without altering the canonical
structure.

**6.17.6 Activity Context**

The Activity Context identifies the Business Activity being executed.

Typical information includes:

-   Activity Identifier

-   Activity Name

-   Activity Version

-   Business Domain

-   Business Object

-   Activity Type

-   Invocation Source

-   Execution Mode

-   Correlation Identifier

This information uniquely identifies the execution instance.

**6.17.7 Identity Context**

The Identity Context identifies the person responsible for the
execution.

It may include:

-   Person

-   Identity

-   Membership

-   Business Roles

-   Approval Authorities

-   Delegations

-   Runtime Assignments

-   Authentication Method

-   Session Identifier

Identity information shall be derived from the centralized identity
framework.

**6.17.8 Organization Context**

The Organization Context identifies the organizational scope of
execution.

Typical information includes:

-   Organization

-   Workspace

-   Tenant

-   Organization Settings

-   Organization Configuration

-   Organization Policies

Organization Context determines the organizational boundary for
execution.

**6.17.9 Enterprise Context**

The Enterprise Context identifies the operational scope within the
Enterprise Relationship Graph.

Typical information includes:

-   Enterprise Node

-   Parent Node

-   Hierarchy

-   Enterprise View

-   Relationship Scope

-   Consolidation Scope

-   Geographic Scope

Enterprise Context shall be resolved using the canonical Enterprise
Relationship Graph.

**6.17.10 Authorization Context**

Authorization Context contains the resolved authorization decision.

Typical information includes:

-   Granted Permissions

-   Effective Business Roles

-   Approval Authorities

-   Runtime Assignments

-   Delegations

-   Policy Decisions

-   Access Constraints

Business Activities consume authorization outcomes.

They do not evaluate authorization.

**6.17.11 Workflow Context**

Workflow Context describes workflow participation.

It may include:

-   Workflow Instance

-   Current Step

-   Previous Step

-   Next Step

-   Assigned Participants

-   Escalation State

-   Approval State

-   Due Dates

Business Activities remain executable outside workflows.

Workflow Context shall therefore be optional.

**6.17.12 Request Context**

The Request Context captures request-specific information.

Typical information includes:

-   Request Identifier

-   Request Timestamp

-   Request Source

-   API Version

-   Client Application

-   Device Information

-   Locale

-   Time Zone

-   Preferred Language

Request Context supports localization, diagnostics, and observability.

**6.17.13 Transaction Context**

Transaction Context captures transaction-related information.

It may include:

-   Transaction Identifier

-   Transaction Start Time

-   Transaction State

-   Retry Count

-   Idempotency Key

-   Isolation Level

-   Rollback Status

The Transaction Context is managed exclusively by the Business Activity
Engine.

**6.17.14 AI Context**

Where AI participates in execution, the Business Activity Context shall
include AI Context.

Typical information includes:

-   AI Assistant

-   AI Session Identifier

-   Prompt Template

-   Model Version

-   Confidence Threshold

-   Human Review Requirement

-   AI Policy

-   AI Execution Status

AI Context enables consistent governance of AI-assisted execution.

**6.17.15 Runtime Context**

Runtime Context supports monitoring and observability.

Typical information includes:

-   Correlation Identifier

-   Trace Identifier

-   Execution Start Time

-   Execution Duration

-   Service Instance

-   Deployment Environment

-   Performance Metrics

Runtime Context shall be automatically populated by the Business
Activity Engine.

**6.17.16 Context Immutability**

The Business Activity Context shall be immutable during Business
Activity execution except for runtime execution metadata.

Business Activities may read context.

Business Activities shall not modify context.

Only the Business Activity Engine may enrich runtime metrics during
execution.

This guarantees deterministic execution and simplifies auditing.

**6.17.17 Context Propagation**

Where a Business Activity invokes another Business Activity, initiates a
Workflow, publishes Domain Events, calls external services, or invokes
AI capabilities, the Business Activity Context shall be propagated as
required to maintain end-to-end traceability.

Context propagation shall preserve:

-   Correlation Identifier

-   Identity

-   Organization

-   Enterprise Scope

-   Authorization Decisions

-   Transaction Information

-   Audit References

This enables complete observability across distributed execution.

**6.17.18 Architectural Guarantee**

Every Business Activity within the Aurex Intelligent Operating
Center shall execute with a complete, validated, and standardized
Business Activity Context.

The Business Activity Context establishes a uniform execution
environment across all Business Domains, ensuring consistent
authorization, enterprise scoping, workflow participation, auditability,
AI governance, and end-to-end observability throughout the platform.

**6.18 Business Activity State Model**

**6.18.1 Purpose**

The Business Activity State Model defines the canonical lifecycle
through which every Business Activity progresses from initiation to
completion.

A standardized lifecycle enables consistent execution management,
monitoring, workflow coordination, recovery, auditing, and operational
observability across all Business Domains.

Every Business Activity executed by the Business Activity Engine shall
maintain an explicit execution state throughout its lifecycle.

**6.18.2 Architectural Principle**

Business Activities are stateful executions.

Business Objects represent business state.

Business Activity States represent execution state.

These concepts are independent and shall never be conflated.

A Business Activity may complete without changing a Business Object.

Likewise, a Business Object may participate in multiple Business
Activities during its lifecycle.

**6.18.3 Canonical State Model**

Every Business Activity shall transition through one or more of the
following execution states.

Created\
│\
Ready\
│\
Running\
│\
──────────────────────────────\
│ │ │\
│ │ │\
Waiting Suspended Failed\
│ │ │\
│ │ │\
─────────────┼──────────────\
│\
Running\
│\
Completed\
│\
─────────────┼──────────────\
│ │\
Cancelled Rolled Back

Not every Business Activity shall traverse every state.

The state model defines the complete execution vocabulary available to
the platform.

**6.18.4 State Definitions**

  ------------------------------------------------------------------------
  **State**   **Description**
  ----------- ------------------------------------------------------------
  Created     Activity instance has been created but not yet validated for
              execution

  Ready       Activity has passed initialization and is eligible for
              execution

  Running     Activity is currently executing

  Waiting     Activity is waiting for an external dependency or
              asynchronous completion

  Suspended   Execution has been intentionally paused

  Completed   Activity completed successfully

  Failed      Activity terminated due to an unrecoverable error

  Cancelled   Activity terminated before successful completion by an
              authorized action

  Rolled Back Activity execution has been reversed through transaction
              rollback or compensation
  ------------------------------------------------------------------------

State names are canonical across the platform.

**6.18.5 State Ownership**

The Business Activity Engine exclusively owns execution state.

Business Domains shall not directly manipulate lifecycle states.

Business Domains may request:

-   Pause

-   Resume

-   Cancel

-   Retry

-   Complete

The Business Activity Engine determines whether the requested transition
is valid.

**6.18.6 State Transition Rules**

State transitions shall follow the canonical lifecycle.

Permitted examples include:

Created → Ready\
\
Ready → Running\
\
Running → Waiting\
\
Waiting → Running\
\
Running → Suspended\
\
Suspended → Running\
\
Running → Completed\
\
Running → Failed\
\
Running → Cancelled\
\
Failed → Rolled Back

Invalid transitions shall be rejected by the Business Activity Engine.

**6.18.7 Waiting State**

The Waiting state represents temporary suspension pending completion of
an external dependency.

Examples include:

-   Human approval

-   External API response

-   Workflow continuation

-   Scheduled execution window

-   Batch processing

-   AI inference completion

-   Document ingestion

-   Event arrival

Waiting is not a failure state.

Execution may resume without creating a new Business Activity.

**6.18.8 Suspended State**

Suspended represents an intentional administrative or operational pause.

Typical reasons include:

-   Manual intervention

-   Governance review

-   Compliance hold

-   Operational maintenance

-   Investigation

-   Policy enforcement

A Suspended activity retains its execution context and may later resume.

**6.18.9 Failed State**

A Business Activity enters the Failed state when execution cannot
continue.

Typical causes include:

-   Business rule violation

-   Infrastructure failure

-   Integration failure

-   AI service failure

-   Data corruption

-   Unexpected system exception

Failure shall always generate:

-   Audit record

-   Failure reason

-   Diagnostic information

-   Correlation Identifier

Failure does not necessarily imply transaction rollback.

Rollback depends on transaction policy.

**6.18.10 Cancelled State**

Cancellation represents intentional termination before successful
completion.

Cancellation may occur because of:

-   User request

-   Workflow cancellation

-   Administrative action

-   Duplicate execution

-   Superseded request

-   Policy decision

Only authorized actors may cancel Business Activities.

Cancellation shall be auditable.

**6.18.11 Rolled Back State**

Rollback restores the platform to a consistent business state after
unsuccessful execution.

Rollback may occur through:

-   Database transaction rollback

-   Compensation Activity

-   Distributed transaction recovery

-   Manual recovery process

Rollback shall preserve the complete execution history.

Historical execution records shall never be deleted.

**6.18.12 State Persistence**

Execution state shall be maintained independently from Business Objects.

Execution state may be persisted for:

-   Long-running activities

-   Workflow coordination

-   Monitoring

-   Recovery

-   Operational dashboards

-   Audit

-   Analytics

State persistence enables Business Activities to survive service
restarts and distributed execution.

**6.18.13 State Events**

Every execution state transition shall generate a corresponding internal
lifecycle event.

Examples include:

-   ActivityCreated

-   ActivityReady

-   ActivityStarted

-   ActivityWaiting

-   ActivitySuspended

-   ActivityResumed

-   ActivityCompleted

-   ActivityFailed

-   ActivityCancelled

-   ActivityRolledBack

These are execution events generated by the Business Activity Engine.

They are distinct from Domain Events, which communicate business
outcomes.

**6.18.14 Monitoring & Observability**

The Business Activity Engine shall continuously monitor execution state
transitions.

Monitoring shall support:

-   Active execution tracking

-   Queue monitoring

-   Bottleneck detection

-   Long-running activity detection

-   Failure analysis

-   Retry analysis

-   SLA monitoring

-   Operational dashboards

Execution state provides the foundation for platform observability.

**6.18.15 Recovery**

Business Activities that terminate unexpectedly may be resumed from the
last persisted execution state where supported by the Business Activity
Contract.

Recovery behavior shall be governed by:

-   Activity Type

-   Transaction Policy

-   Retry Policy

-   Compensation Strategy

-   Workflow State

Recovery shall never compromise business consistency or audit integrity.

**6.18.16 Architectural Guarantee**

Every Business Activity executed within the Aurex Intelligent
Operating Center shall follow the canonical Business Activity State
Model.

The Business Activity Engine shall exclusively manage execution states,
validate all state transitions, maintain complete execution history, and
provide deterministic lifecycle management across all Business Domains.

This standardized state model ensures consistent execution control,
operational resilience, recoverability, workflow coordination,
auditability, and platform-wide observability.

**6.19 Business Activity Transaction Management**

**6.19.1 Purpose**

The Business Activity Transaction Management model defines the canonical
approach for maintaining business consistency, data integrity, and
execution reliability throughout the lifecycle of every Business
Activity.

The Business Activity Engine shall manage transaction boundaries for all
Business Activities, ensuring that business operations execute as
complete, atomic, and auditable units of work.

Business Domains shall not directly manage transactions.

**6.19.2 Architectural Principle**

Business Activities own business intent.

The Business Activity Engine owns transaction execution.

Transactions protect business consistency.

Business logic shall remain independent of transaction implementation.

**6.19.3 Transaction Ownership**

The Business Activity Engine shall exclusively manage:

-   Transaction creation

-   Transaction boundaries

-   Transaction propagation

-   Commit operations

-   Rollback operations

-   Savepoints

-   Compensation coordination

-   Transaction completion

Business Activities shall never:

-   Open transactions

-   Commit transactions

-   Roll back transactions

-   Manage database sessions

-   Control persistence mechanisms

These responsibilities belong exclusively to the Business Activity
Engine.

**6.19.4 Canonical Transaction Lifecycle**

Every Business Activity shall execute within a controlled transaction
lifecycle.

Business Activity Request\
│\
Transaction Initialization\
│\
Business Activity Execution\
│\
Business Object Changes\
│\
Validation Complete\
│\
Commit Decision\
┌─┴──────────────┐\
│ │\
Commit Rollback / Compensation\
│ │\
Post-Commit Recovery\
Processing\
│\
Activity Complete

The transaction lifecycle shall be deterministic and fully auditable.

**6.19.5 Transaction Scope**

A Business Transaction represents the complete execution scope of a
single Business Activity.

A transaction may include:

-   Business Object updates

-   Relationship updates

-   Metadata updates

-   Workflow state changes

-   Assignment changes

-   Configuration updates

-   Audit preparation

-   Domain Event preparation

The transaction boundary shall encompass all business changes required
to complete the Business Activity.

**6.19.6 Atomicity**

A Business Activity shall execute as a single logical unit of work.

Either:

-   All required business changes succeed,

or

-   None of the business changes are committed.

Partial business completion is prohibited unless explicitly defined by a
Compensation Strategy.

**6.19.7 Transaction Isolation**

Concurrent Business Activities shall execute without compromising
business consistency.

The Business Activity Engine shall support:

-   Optimistic concurrency control

-   Version validation

-   Conflict detection

-   Concurrent update resolution

Business Activities shall not implement concurrency management.

**6.19.8 Nested Business Activities**

A Business Activity may invoke one or more subordinate Business
Activities.

Example:

Publish Intelligence Report\
│\
├── Validate Report\
├── Freeze Metrics\
├── Generate Report\
├── Publish Disclosure\
└── Notify Stakeholders

The parent Business Activity remains responsible for overall business
completion.

Child Business Activities shall execute within controlled transactional
boundaries defined by the Business Activity Contract.

**6.19.9 Distributed Transactions**

Where execution spans multiple services or external systems, the
Business Activity Engine shall avoid distributed database transactions.

Instead, the platform shall employ:

-   Domain Events

-   Compensation Activities

-   Reliable messaging

-   Eventual consistency

-   Workflow coordination

Two-phase commit protocols shall not be the preferred architectural
pattern.

**6.19.10 Commit Policy**

A transaction may be committed only when all mandatory execution stages
have successfully completed, including:

-   Authorization

-   Validation

-   Business Rule Execution

-   Persistence

-   Integrity Verification

Post-commit activities shall not influence the commit decision.

**6.19.11 Rollback Policy**

Rollback shall occur when execution cannot successfully complete before
transaction commitment.

Typical rollback conditions include:

-   Authorization failure

-   Validation failure

-   Business rule violation

-   Persistence failure

-   Integrity violation

-   System exception

-   Infrastructure failure

Rollback shall restore all affected Business Objects to their
pre-execution state.

**6.19.12 Compensation Strategy**

Certain Business Activities interact with external systems that cannot
participate in database rollback.

Examples include:

-   Email delivery

-   External API invocation

-   ERP synchronization

-   Third-party notifications

-   Document publication

In such cases, the Business Activity Contract shall define a
Compensation Activity.

Example:

Publish Intelligence Report\
│\
Report Published\
│\
ERP Updated\
│\
Email Delivered\
│\
Failure Detected\
│\
Compensation Activity\
│\
Withdraw Report\
Notify Stakeholders\
Create Audit Entry

Compensation restores business consistency without reversing immutable
external actions.

**6.19.13 Transaction Recovery**

If execution terminates unexpectedly before transaction completion, the
Business Activity Engine shall determine whether recovery is possible.

Recovery options include:

-   Resume execution

-   Retry execution

-   Rollback transaction

-   Execute Compensation Activity

-   Escalate for manual intervention

Recovery strategy shall be defined by the Business Activity Contract.

**6.19.14 Post-Commit Processing**

The following activities shall occur only after successful transaction
commitment:

-   Domain Event Publication

-   Notification Delivery

-   Workflow Continuation

-   Analytics Updates

-   AI Assistance

-   Monitoring Updates

-   Audit Finalization

Post-commit processing shall not modify committed Business Objects.

**6.19.15 Transaction Observability**

Every transaction shall generate operational telemetry.

Captured information shall include:

-   Transaction Identifier

-   Correlation Identifier

-   Activity Identifier

-   Execution Duration

-   Commit Status

-   Rollback Status

-   Retry Count

-   Compensation Status

-   Failure Reason

Transaction telemetry supports operational monitoring and diagnostics.

**6.19.16 Architectural Guarantees**

The Business Activity Transaction Management model guarantees:

-   Atomic business execution

-   Consistent business state

-   Reliable transaction boundaries

-   Controlled rollback

-   Support for distributed execution through compensation

-   Deterministic commit behavior

-   Complete transaction traceability

-   Platform-wide consistency

All Business Activities within the Aurex Intelligent Operating
Center shall execute under the governance of the Business Activity
Engine\'s transaction management framework, ensuring reliable,
auditable, and resilient execution across all Business Domains.

**6.20 Business Activity Idempotency & Replay Protection**

**6.20.1 Purpose**

The Business Activity Idempotency and Replay Protection model ensures
that every Business Activity executes safely in the presence of retries,
duplicate requests, network failures, asynchronous messaging, and
distributed processing.

The Business Activity Engine shall guarantee that a Business Activity is
executed exactly once from a business perspective, even when the
underlying request is received multiple times.

This protects the integrity of Business Objects, Business Workflows,
Domain Events, and Audit Records.

**6.20.2 Architectural Principle**

Business intent shall execute once.

Requests may be received multiple times.

The Business Activity Engine shall distinguish between duplicate
requests and legitimate new Business Activities.

Business Domains shall not implement duplicate detection logic.

**6.20.3 Idempotency Responsibility**

The Business Activity Engine shall exclusively manage:

-   Idempotency Keys

-   Duplicate Detection

-   Replay Detection

-   Safe Retry Handling

-   Request Correlation

-   Execution History

-   Response Reuse

Business Activities consume idempotency decisions.

They shall not manage idempotency.

**6.20.4 Idempotency Lifecycle**

Every Business Activity shall follow the canonical idempotent execution
lifecycle.

Incoming Request\
│\
Generate / Validate Idempotency Key\
│\
Search Execution Registry\
│\
──────────────┬────────────────\
│\
Existing Execution?\
│\
┌───────┴────────┐\
│ │\
No Yes\
│ │\
Execute Activity Return Existing Result\
│\
Persist Execution Record\
│\
Return Response

The same business request shall never produce duplicate business
outcomes.

**6.20.5 Idempotency Key**

Every Business Activity capable of external invocation shall support an
Idempotency Key.

The key uniquely identifies the intended business operation rather than
the transport request.

The Idempotency Key may be supplied by:

-   Client Applications

-   API Gateways

-   Integration Connectors

-   Workflow Engine

-   Business Activity Engine

Where one is not provided, the Business Activity Engine may generate one
according to platform policy.

**6.20.6 Duplicate Detection**

Before execution begins, the Business Activity Engine shall determine
whether an equivalent Business Activity has already been executed.

Duplicate detection may consider:

-   Idempotency Key

-   Business Object

-   Activity Type

-   Organization

-   Enterprise Node

-   Person

-   Workflow Instance

-   Request Time Window

-   Activity Status

Duplicate detection shall occur before Business Rule Execution.

**6.20.7 Safe Retry**

Retries are expected in distributed systems.

The Business Activity Engine shall support retries caused by:

-   Network interruption

-   Client timeout

-   Service restart

-   Message redelivery

-   Queue processing

-   External integration retry

-   AI timeout

Safe retries shall never create duplicate Business Objects, duplicate
approvals, duplicate notifications, or duplicate Domain Events.

**6.20.8 Replay Protection**

Replay protection prevents previously completed Business Activities from
being executed again without authorization.

Replay protection shall detect:

-   Replayed API requests

-   Duplicate workflow messages

-   Reprocessed integration events

-   Queue redelivery

-   Event replay

-   AI re-execution requests

Replay detection shall use execution history maintained by the Business
Activity Engine.

**6.20.9 Execution Registry**

The Business Activity Engine shall maintain an immutable execution
registry for idempotency management.

Typical execution metadata includes:

-   Activity Identifier

-   Activity Version

-   Idempotency Key

-   Correlation Identifier

-   Organization

-   Enterprise Node

-   Business Object

-   Request Timestamp

-   Execution Status

-   Response Reference

-   Completion Timestamp

The execution registry serves as the authoritative source for duplicate
detection and replay protection.

**6.20.10 Response Reuse**

When a duplicate request is detected and the original Business Activity
completed successfully, the Business Activity Engine shall return the
original Business Activity result rather than re-executing the Business
Activity.

Response reuse guarantees consistent business outcomes while avoiding
unnecessary processing.

**6.20.11 Event Idempotency**

Domain Events shall also be idempotent.

The Business Activity Engine shall ensure that duplicate execution
attempts do not publish duplicate Domain Events.

Event consumers shall be capable of safely processing duplicate
deliveries where required by the messaging infrastructure.

Business outcome uniqueness shall be guaranteed even when message
delivery is at-least-once.

**6.20.12 Workflow Idempotency**

Workflow transitions shall execute only once for a given Business
Activity state transition.

Duplicate workflow messages shall not:

-   Advance workflow state multiple times

-   Create duplicate approvals

-   Generate duplicate assignments

-   Trigger duplicate escalations

Workflow integrity shall be preserved through Business Activity
idempotency.

**6.20.13 Integration Idempotency**

External integrations shall execute under controlled idempotency
policies.

The Business Activity Engine shall support:

-   Request deduplication

-   Integration correlation identifiers

-   Retry-safe outbound requests

-   Duplicate response handling

-   External acknowledgement tracking

Where external systems do not support idempotency, the Business Activity
Contract shall define the appropriate compensation or reconciliation
strategy.

**6.20.14 Idempotency Expiration**

Idempotency records need not be retained indefinitely.

The platform shall define configurable retention policies based on:

-   Activity Type

-   Regulatory Requirements

-   Audit Requirements

-   Business Criticality

-   Integration Requirements

Expired idempotency records shall remain subject to platform archival
and audit policies.

**6.20.15 Observability**

The Business Activity Engine shall capture idempotency metrics
including:

-   Duplicate Request Count

-   Replay Attempts

-   Retry Count

-   Successful Response Reuse

-   Duplicate Event Prevention

-   Duplicate Workflow Prevention

-   Duplicate Integration Prevention

These metrics support operational monitoring and reliability analysis.

**6.20.16 Architectural Guarantees**

The Business Activity Idempotency and Replay Protection model
guarantees:

-   Exactly-once business execution semantics

-   Safe retry handling

-   Duplicate request prevention

-   Replay attack protection

-   Consistent workflow execution

-   Reliable event publication

-   Integration resilience

-   Complete execution traceability

Every externally invocable Business Activity within the Aurex
Intelligent Operating Center shall execute under the governance of the
Business Activity Engine\'s idempotency framework, ensuring reliable and
deterministic business outcomes across all interfaces, workflows,
integrations, and distributed execution environments.

**6.21 Business Activity Compensation & Recovery**

**6.21.1 Purpose**

The Business Activity Compensation and Recovery model defines the
canonical mechanisms for restoring business consistency when a Business
Activity cannot be completed successfully.

While database transactions provide atomicity within a single
persistence boundary, many Business Activities interact with external
systems, asynchronous workflows, AI services, notifications, and
third-party integrations that cannot participate in traditional
transaction rollback.

The Business Activity Engine shall provide standardized compensation and
recovery mechanisms that preserve business integrity across distributed
execution environments.

**6.21.2 Architectural Principle**

Rollback restores technical consistency.

Compensation restores business consistency.

Recovery restores execution continuity.

These mechanisms are complementary and shall be selected according to
the characteristics of the Business Activity.

**6.21.3 Compensation Responsibility**

The Business Activity Engine shall exclusively coordinate:

-   Compensation execution

-   Recovery strategy selection

-   Retry orchestration

-   Recovery state management

-   Failure escalation

-   Recovery auditing

-   Execution resumption

Business Domains define compensation logic.

The Business Activity Engine governs its execution.

**6.21.4 Recovery Decision Model**

Following execution failure, the Business Activity Engine shall
determine the appropriate recovery strategy.

Business Activity Failure\
│\
Failure Classification\
│\
────────────────────────────────────────\
│ │ │ │\
Retry Rollback Compensation Manual Recovery\
│ │ │ │\
Resume Restore Business Administrative\
Execution Database Consistency Intervention

The selected recovery strategy shall be determined by the Business
Activity Contract.

**6.21.5 Rollback**

Rollback shall be used when all affected resources remain within the
managed transaction boundary.

Rollback restores:

-   Business Objects

-   Relationships

-   Metadata

-   Assignments

-   Workflow state (where transactional)

-   Configuration changes

Rollback shall occur automatically before transaction commitment.

**6.21.6 Compensation Activities**

Where rollback is impossible or insufficient, the Business Activity
Contract shall define one or more Compensation Activities.

A Compensation Activity is itself a Business Activity executed through
the Business Activity Engine.

Examples include:

  -----------------------------------------------------------------------
  **Original Activity**              **Compensation Activity**
  ---------------------------------- ------------------------------------
  Publish Intelligence Report        Withdraw Published Report

  Assign Business Owner              Remove Assignment

  Approve Evidence                   Revoke Approval

  Synchronize ERP                    Reverse ERP Transaction

  Create Enterprise Node             Retire Enterprise Node

  Notify Stakeholders                Issue Correction Notification
  -----------------------------------------------------------------------

Compensation Activities shall follow the same architectural standards as
all other Business Activities.

**6.21.7 Compensation Principles**

Compensation shall:

-   Restore business consistency

-   Preserve audit history

-   Never erase historical execution

-   Create compensating business outcomes

-   Publish corresponding Domain Events

-   Maintain regulatory traceability

Compensation is not deletion.

Compensation creates a new business outcome that offsets a previous
outcome.

**6.21.8 Retry Strategy**

Certain failures are transient and may safely be retried.

Examples include:

-   Temporary network failures

-   External service unavailability

-   Database connection interruptions

-   AI inference timeout

-   Message broker unavailability

Retry behavior shall be governed by the Business Activity Contract.

Retry policies may specify:

-   Maximum Retry Count

-   Retry Interval

-   Exponential Backoff

-   Retry Timeout

-   Failure Threshold

-   Escalation Policy

Retries shall execute under the Business Activity Engine.

**6.21.9 Resume Execution**

Long-running Business Activities may resume from the last successfully
completed execution stage.

Resume execution shall be supported only where:

-   Execution state has been persisted

-   Business consistency can be guaranteed

-   Activity Contract explicitly permits resumption

Resume execution shall preserve:

-   Business Activity Context

-   Correlation Identifier

-   Workflow State

-   Transaction History

-   Audit References

**6.21.10 Failure Classification**

The Business Activity Engine shall classify execution failures before
selecting a recovery strategy.

Typical failure categories include:

  -----------------------------------------------------------------------
  **Failure Type**                    **Typical Recovery**
  ----------------------------------- -----------------------------------
  Validation Failure                  Reject Request

  Authorization Failure               Reject Request

  Business Rule Failure               Reject Request

  Infrastructure Failure              Retry

  Integration Failure                 Retry or Compensation

  AI Service Failure                  Retry or Manual Review

  Workflow Failure                    Resume

  Persistence Failure                 Rollback

  External System Failure             Compensation or Retry
  -----------------------------------------------------------------------

Failure classification enables deterministic recovery behavior.

**6.21.11 Manual Recovery**

Certain failures require human intervention.

Examples include:

-   Regulatory exceptions

-   Governance review

-   Legal restrictions

-   Data integrity investigation

-   Irrecoverable external failures

The Business Activity Engine shall support administrative recovery
without compromising audit integrity.

Manual recovery actions shall themselves be executed as governed
Business Activities where applicable.

**6.21.12 Recovery Audit**

Every recovery action shall generate immutable audit records.

Recovery audit information shall include:

-   Original Activity

-   Failure Reason

-   Recovery Strategy

-   Recovery Initiator

-   Recovery Timestamp

-   Compensation Activity

-   Retry Attempts

-   Final Outcome

Recovery history shall remain permanently linked to the originating
Business Activity.

**6.21.13 Recovery Events**

Recovery operations shall publish execution events where appropriate.

Examples include:

-   ActivityRetried

-   ActivityRecovered

-   ActivityCompensated

-   ActivityResumed

-   ActivityRollbackCompleted

-   ManualRecoveryCompleted

These execution events are distinct from Domain Events representing
business outcomes.

**6.21.14 Recovery Observability**

The Business Activity Engine shall continuously monitor recovery
operations.

Operational metrics shall include:

-   Recovery Success Rate

-   Retry Success Rate

-   Compensation Count

-   Resume Count

-   Rollback Count

-   Manual Recovery Count

-   Mean Recovery Time

-   Failure Recurrence Rate

These metrics support operational resilience and continuous improvement.

**6.21.15 Architectural Guarantees**

The Business Activity Compensation and Recovery model guarantees:

-   Controlled recovery from execution failures

-   Consistent compensation for distributed business operations

-   Reliable retry and resume mechanisms

-   Preservation of business integrity

-   Complete auditability of recovery actions

-   Deterministic recovery behavior

-   Platform-wide operational resilience

Every Business Activity executed within the Aurex Intelligent
Operating Center shall be recoverable through standardized rollback,
compensation, retry, resume, or manual recovery strategies governed
exclusively by the Business Activity Engine, ensuring consistent and
resilient business execution across all Business Domains.

**6.22 Business Activity Registry**

**6.22.1 Purpose**

The Business Activity Registry (BAR) is the canonical metadata
repository for all Business Activities within the Aurex Intelligent
Operating Center.

Rather than discovering Business Activities through application code,
configuration files, or service implementations, the platform shall
maintain a centralized registry describing every Business Activity, its
capabilities, execution characteristics, governance requirements, and
implementation metadata.

The Business Activity Registry is the authoritative source for Business
Activity discovery, execution, governance, monitoring, and lifecycle
management.

**6.22.1a Constitutional Authority** *(formalized per ARP-001 WP-3)*

The Business Activity Registry operationalizes, at the engineering layer, the identity and rules SD-002 §5 (Business Activities Rules) already establishes at the constitutional layer. SD-002 defines what a Business Activity is and the rules it must satisfy; the Registry catalogs the identified instances. IMP-001 does not redefine Business Activity semantics here — per §1.2, it governs how the platform is built, not what is built.

**6.22.1b Identifier Strategy** *(formalized per ARP-001 WP-3)*

The Activity Identifier referenced throughout this section is governed by SD-002-004 (Universal Identity): a globally unique, permanent identifier in `PREFIX-NNNNNN` form (e.g. `BA-000089`), matching the format SD-002-004 already establishes for every business object type. This section does not define a competing identifier format.

**6.22.2 Architectural Principle**

Business Activities are platform assets.

Platform assets shall be registered.

The Business Activity Registry shall contain the complete metadata
required for the Business Activity Engine to discover, validate,
execute, monitor, and govern Business Activities.

Implementation code is not the source of truth.

The Registry is the source of truth.

**6.22.3 Registry Ownership**

The Business Activity Registry shall be managed by the platform.

The Business Activity Engine shall use the Registry for:

-   Activity Discovery

-   Version Resolution

-   Contract Validation

-   Execution Policy Resolution

-   Authorization Resolution

-   Workflow Integration

-   Event Configuration

-   AI Integration

-   Monitoring

-   Lifecycle Governance

Business Domains register Business Activities.

The Business Activity Engine executes them.

**6.22.4 Registry Architecture**

Business Domains\
│\
Register Activities\
│\
───────────────────────────────────────────────────\
Business Activity Registry\
───────────────────────────────────────────────────\
\
Activity Metadata\
\
Business Contracts\
\
Execution Policies\
\
Authorization Rules\
\
Workflow Definitions\
\
Event Configuration\
\
AI Configuration\
\
Monitoring Configuration\
\
Version Information\
\
Implementation Mapping\
───────────────────────────────────────────────────\
│\
Business Activity Engine\
│\
Execute Activity

The Registry shall serve as the single discovery mechanism for Business
Activity execution.

**6.22.5 Registry Contents**

Every Business Activity shall be represented by a registry entry.

The registry shall maintain metadata including:

  -----------------------------------------------------------------------
  **Category**                 **Description**
  ---------------------------- ------------------------------------------
  Activity Identity            Unique identification

  Business Classification      Domain, Object, Activity Type

  Execution Contract           Input and Output Contracts

  Authorization                Required permissions

  Workflow                     Workflow participation

  Events                       Published Domain Events

  AI                           AI assistance configuration

  Execution Policy             Runtime behavior

  Monitoring                   Observability configuration

  Versioning                   Activity versions

  Implementation               Runtime implementation mapping
  -----------------------------------------------------------------------

The Registry defines execution metadata, not business data.

**6.22.6 Canonical Registry Attributes**

Every registered Business Activity shall include, at minimum:

**Identity**

-   Activity Identifier

-   Activity Name

-   Activity Code

-   Version

-   Status

**Classification**

-   Business Domain

-   Business Object

-   Activity Type

-   Business Capability

-   Functional Area

**Ownership**

-   Domain Owner

-   Technical Owner

-   Steward

-   Approval Authority

**Execution**

-   Execution Mode

-   Transaction Policy

-   Retry Policy

-   Timeout

-   Compensation Strategy

-   Idempotency Policy

**Security**

-   Authorization Policy

-   Required Permissions

-   Security Classification

-   Data Classification

**Workflow**

-   Workflow Integration

-   Workflow Trigger

-   Approval Requirements

-   Escalation Policy

**Events**

-   Published Domain Events

-   Consumed Events

-   Notification Policies

**AI**

-   AI Assistance Enabled

-   Human Review Required

-   Confidence Threshold

-   AI Policy

**Runtime**

-   Implementation Class

-   Service Endpoint

-   Runtime Environment

-   Deployment Version

**6.22.7 Activity Registration**

A Business Activity shall not be executable until successfully
registered.

Registration shall validate:

-   Business Activity Contract

-   Manifest Completeness

-   Version Compatibility

-   Dependency Resolution

-   Authorization Configuration

-   Event Definitions

-   Workflow References

-   AI Configuration

Incomplete registrations shall be rejected.

**6.22.8 Activity Discovery**

The Business Activity Engine shall discover Business Activities
exclusively through the Registry.

Discovery shall support:

-   Activity Identifier

-   Business Domain

-   Business Object

-   Activity Type

-   Event Trigger

-   Workflow Step

-   API Endpoint

-   Scheduled Job

-   Integration Mapping

Business Activities shall never be discovered through implementation
scanning or naming conventions.

**6.22.9 Activity Status**

Each Business Activity shall have an explicit lifecycle status.

Supported statuses include:

-   Draft

-   Registered

-   Active

-   Suspended

-   Deprecated

-   Retired

Only Active Business Activities may be executed.

Deprecated Business Activities remain executable only under approved
compatibility policies.

Retired Business Activities shall not accept new executions.

**6.22.10 Registry Version Management**

The Registry shall maintain version history for every Business Activity.

Each version shall include:

-   Version Number

-   Effective Date

-   Deprecation Date

-   Compatibility Rules

-   Migration Strategy

-   Change History

Multiple compatible versions may coexist where required for backward
compatibility.

**6.22.11 Dependency Management**

The Registry shall maintain explicit dependencies between Business
Activities and platform capabilities.

Dependencies may include:

-   Business Objects

-   Metadata

-   Reference Data

-   Workflows

-   Domain Events

-   AI Models

-   External Integrations

-   Feature Flags

Dependency management enables impact analysis and controlled deployment.

**6.22.12 Registry Governance**

The Business Activity Registry shall support governance throughout the
Business Activity lifecycle.

Governance capabilities include:

-   Registration Approval

-   Version Approval

-   Activation

-   Suspension

-   Deprecation

-   Retirement

-   Ownership Transfer

-   Audit Review

Registry modifications shall themselves be governed Business Activities.

**6.22.13 Registry Observability**

The Registry shall support operational monitoring.

Typical metrics include:

-   Registered Activities

-   Active Activities

-   Deprecated Activities

-   Version Distribution

-   Execution Frequency

-   Failure Rate

-   Average Execution Duration

-   AI Utilization

-   Workflow Participation

These metrics provide insight into platform behavior and Business
Activity adoption.

**6.22.14 Relationship with the Canonical Business Activity Manifest
(CBAM)**

The Canonical Business Activity Manifest (CBAM) defines the
implementation contract for a Business Activity.

The Business Activity Registry maintains the operational metadata
required to discover, govern, and execute that Business Activity.

The CBAM describes **what** the Business Activity is.

The Registry describes **how** the platform manages it.

Together they form the complete execution metadata model.

**6.22.15 Architectural Guarantees**

The Business Activity Registry guarantees:

-   Centralized Business Activity discovery

-   Standardized execution metadata

-   Controlled lifecycle management

-   Version governance

-   Dependency transparency

-   Consistent execution policies

-   Platform-wide observability

-   Complete auditability

Every executable Business Activity within the Aurex Intelligent
Operating Center shall be registered in the Business Activity Registry
before becoming available for execution, ensuring consistent governance,
discoverability, lifecycle management, and operational control across
all Business Domains.

**6.23 Business Activity Versioning**

**6.23.1 Purpose**

The Business Activity Versioning model defines the canonical approach
for evolving Business Activities while preserving platform stability,
backward compatibility, auditability, and operational continuity.

Business Activities will evolve over time as business policies,
regulations, workflows, authorization rules, AI capabilities, and
platform functionality change.

The platform shall support controlled evolution without disrupting
existing Business Processes or compromising historical audit integrity.

**6.23.2 Architectural Principle**

Business intent evolves.

Business execution must remain stable.

Versioning enables continuous evolution while preserving deterministic
execution.

Business Activity versions shall be explicitly governed.

They shall never be implicitly replaced.

**6.23.3 Version Ownership**

The Business Activity Engine shall resolve the appropriate Business
Activity version during execution.

The Business Activity Registry shall maintain version metadata.

Business Domains own business logic changes.

The platform owns version governance.

**6.23.4 Version Lifecycle**

Every Business Activity Version shall follow a governed lifecycle.

Draft\
│\
Registered\
│\
Approved\
│\
Active\
│\
────────────────────────────\
│ │\
│ │\
Deprecated Suspended\
│ │\
│ │\
──────────────┬─────────────\
│\
Retired

Only Approved and Active versions shall be available for execution.

**6.23.5 Canonical Version Model**

Each Business Activity Version shall include:

  -----------------------------------------------------------------------
  **Attribute**                 **Description**
  ----------------------------- -----------------------------------------
  Activity Identifier           Canonical Activity

  Version Number                Semantic version

  Effective Date                Activation date

  Deprecation Date              Planned deprecation

  Retirement Date               End of execution support

  Status                        Lifecycle state

  Change Summary                Description of changes

  Compatibility Level           Compatibility classification

  Migration Strategy            Upgrade guidance
  -----------------------------------------------------------------------

Every version shall be immutable after approval.

**6.23.6 Version Compatibility**

Business Activity changes shall be classified according to
compatibility.

  -----------------------------------------------------------------------
  **Compatibility**         **Description**
  ------------------------- ---------------------------------------------
  Fully Compatible          Existing consumers require no changes

  Backward Compatible       Older clients continue to function

  Forward Compatible        Supports future enhancements

  Breaking Change           Requires coordinated migration
  -----------------------------------------------------------------------

Compatibility classification shall be declared before activation.

**6.23.7 Semantic Versioning**

Business Activities should follow semantic versioning principles.

Example:

Major.Minor.Patch\
\
1.0.0\
\
1.1.0\
\
1.2.3\
\
2.0.0

Where:

-   Major versions introduce breaking business behavior.

-   Minor versions introduce compatible business capabilities.

-   Patch versions correct implementation defects without altering
    business behavior.

Alternative versioning strategies may be adopted where required by
governance.

**6.23.8 Version Resolution**

The Business Activity Engine shall determine the version to execute
using:

-   Explicit Version Request

-   Workflow Definition

-   API Contract

-   Effective Date

-   Business Policy

-   Compatibility Rules

-   Platform Configuration

Version resolution shall be deterministic.

Ambiguous version selection shall be rejected.

**6.23.9 Concurrent Versions**

Multiple Business Activity versions may execute concurrently.

Examples include:

-   Long-running workflows

-   Regulatory transition periods

-   API compatibility

-   Customer-specific rollout

-   Controlled migration

Concurrent execution shall be governed through the Business Activity
Registry.

**6.23.10 Historical Integrity**

Historical Business Activity executions shall always reference the exact
Business Activity Version used during execution.

Audit records shall never be reassigned to newer versions.

Historical execution must remain reproducible.

**6.23.11 Version Migration**

When a new version becomes Active, migration shall be governed.

Migration strategies may include:

-   Immediate Replacement

-   Scheduled Migration

-   Parallel Execution

-   Controlled Rollout

-   Tenant-based Rollout

-   Enterprise-specific Rollout

-   Feature Flag Activation

Migration shall not interrupt executing Business Activities.

**6.23.12 Workflow Version Consistency**

Business Activities participating in a Workflow shall preserve execution
consistency.

A Workflow Instance shall normally continue executing using the Business
Activity Version active when the Workflow began unless the Workflow
Definition explicitly permits version migration.

This prevents inconsistent behavior within a single business process.

**6.23.13 Business Contract Evolution**

Changes affecting the Business Activity Contract shall be versioned.

Examples include:

-   Input Contract

-   Output Contract

-   Authorization Requirements

-   Business Rules

-   Validation Rules

-   Workflow Integration

-   Published Events

-   AI Policies

Contract evolution shall remain explicit and traceable.

**6.23.14 Version Governance**

Business Activity Versions shall be subject to governance.

Governance activities include:

-   Version Registration

-   Technical Review

-   Business Approval

-   Security Review

-   AI Governance Review

-   Release Approval

-   Deprecation Approval

-   Retirement Approval

Version changes shall themselves be auditable Business Activities.

**6.23.15 Version Observability**

The platform shall monitor Business Activity versions.

Metrics include:

-   Active Version Distribution

-   Deprecated Version Usage

-   Migration Progress

-   Compatibility Issues

-   Execution Success by Version

-   Failure Rate by Version

-   Performance by Version

Version observability supports controlled platform evolution.

**6.23.16 Relationship with CBAM and BAR**

The **Canonical Business Activity Manifest (CBAM)** defines the
implementation details of a specific Business Activity Version.

The **Business Activity Registry (BAR)** maintains the lifecycle and
governance of all Business Activity Versions.

The Business Activity Engine resolves the appropriate version during
execution.

Together they provide complete version governance across the platform.

**6.23.17 Architectural Guarantees**

The Business Activity Versioning model guarantees:

-   Controlled Business Activity evolution

-   Explicit version governance

-   Deterministic version resolution

-   Historical execution integrity

-   Backward compatibility where required

-   Safe migration strategies

-   Complete auditability

-   Platform-wide operational stability

Every Business Activity within the Aurex Intelligent Operating
Center shall be versioned, governed, and executed through an explicitly
managed lifecycle, ensuring that business capabilities evolve
predictably without compromising execution consistency, historical
integrity, or enterprise governance.

**6.24 Business Activity Composition**

**6.24.1 Purpose**

The Business Activity Composition model defines how multiple Business
Activities collaborate to accomplish a larger business objective while
preserving modularity, reusability, governance, and execution
consistency.

Business Activities shall remain individually executable, independently
testable, and independently governed.

More complex business capabilities shall be realized through the
composition of Business Activities rather than the creation of
monolithic implementations.

**6.24.2 Architectural Principle**

Business Activities represent atomic business intent.

Business Processes represent composed business intent.

Composition coordinates Business Activities.

Business Activities remain autonomous.

The Business Activity Engine shall execute each participating Business
Activity independently while preserving overall business consistency.

**6.24.3 Composition Hierarchy**

Business execution shall follow the canonical hierarchy.

Business Capability\
│\
Business Process\
│\
Composite Business Activity\
│\
──────────────────────────────────\
│ │ │ │\
Business Business Business Business\
Activity Activity Activity Activity\
│\
Business Objects

Composition exists above individual Business Activities.

Business Activities shall never become tightly coupled.

**6.24.4 Composition Types**

The platform shall support multiple composition patterns.

  ------------------------------------------------------------------------
  **Composition Type**    **Description**
  ----------------------- ------------------------------------------------
  Sequential              Activities execute in defined order

  Parallel                Activities execute concurrently

  Conditional             Activity execution depends on business
                          conditions

  Event-Driven            Activities execute in response to Domain Events

  Workflow-Orchestrated   Workflow engine coordinates execution

  Composite Activity      Parent Business Activity coordinates child
                          activities

  Recursive               A Business Activity invokes another Business
                          Activity
  ------------------------------------------------------------------------

Composition type shall be defined by the Business Activity Contract.

**6.24.5 Composite Business Activity**

A Composite Business Activity coordinates the execution of one or more
subordinate Business Activities.

The Composite Activity:

-   owns the business objective;

-   coordinates execution;

-   aggregates outcomes;

-   manages overall success or failure;

-   does not duplicate the business logic of child activities.

Each child Business Activity shall remain independently executable.

**6.24.6 Example Composition**

Example:

Publish Intelligence Report\
│\
──────────────────────────────────────\
│\
├── Validate Report\
│\
├── Freeze Metrics\
│\
├── Generate Executive Report\
│\
├── Publish Report\
│\
├── Notify Stakeholders\
│\
└── Archive Report Snapshot

Each child remains a fully independent Business Activity.

The parent coordinates business intent.

**6.24.7 Composition Responsibilities**

The Composite Business Activity may coordinate:

-   execution sequence;

-   dependency resolution;

-   result aggregation;

-   error propagation;

-   compensation coordination;

-   workflow progression;

-   completion evaluation.

Child Business Activities remain responsible only for their own business
logic.

**6.24.8 Activity Dependencies**

Business Activity dependencies shall be explicit.

Dependency relationships may include:

-   Requires Completion

-   Requires Approval

-   Requires Event

-   Requires Business Object State

-   Requires External Confirmation

-   Requires Workflow Stage

Hidden implementation dependencies are prohibited.

**6.24.9 Execution Independence**

Every Business Activity shall remain executable independently of any
Composite Business Activity.

Composition shall not introduce hidden assumptions regarding:

-   caller;

-   workflow;

-   user interface;

-   API;

-   integration.

Business Activities shall remain reusable platform capabilities.

**6.24.10 Nested Composition**

Composite Business Activities may invoke other Composite Business
Activities.

Example:

Enterprise Onboarding\
│\
──────────────────────────\
│\
├── Organization Setup\
│ │\
│ ├── Create Organization\
│ ├── Configure Workspace\
│ └── Create Enterprise Nodes\
│\
├── Identity Setup\
│\
├── Configuration Setup\
│\
└── Initial Assessment

The composition hierarchy may span multiple levels while maintaining
execution clarity.

**6.24.11 Failure Handling**

Failure of a child Business Activity shall not automatically imply
failure of the Composite Business Activity.

The Business Activity Contract shall define the failure policy.

Typical policies include:

-   Fail Fast

-   Continue Processing

-   Retry Child Activity

-   Execute Compensation

-   Escalate for Review

-   Manual Intervention

Failure behavior shall be deterministic.

**6.24.12 Transaction Coordination**

Composite Business Activities shall coordinate transactional behavior.

Possible transaction models include:

  -----------------------------------------------------------------------
  **Model**               **Description**
  ----------------------- -----------------------------------------------
  Single Transaction      All child activities execute within one
                          transaction

  Independent             Each child activity manages its own transaction
  Transactions            

  Compensating            Distributed consistency through Compensation
  Transactions            Activities

  Hybrid                  Combination determined by Business Activity
                          Contract
  -----------------------------------------------------------------------

Transaction strategy shall be explicitly defined.

**6.24.13 Event Coordination**

Each child Business Activity may publish Domain Events independently.

The Composite Business Activity may additionally publish higher-level
business outcome events.

Example:

Evidence Approved\
\
↓\
\
Report Published\
\
↓\
\
Stakeholders Notified\
\
↓\
\
Enterprise Report Published

Composite events communicate overall business outcomes rather than
implementation details.

**6.24.14 Monitoring & Observability**

The Business Activity Engine shall monitor composed execution.

Monitoring shall include:

-   Parent Activity

-   Child Activities

-   Execution Sequence

-   Execution Duration

-   Dependency Resolution

-   Retry Activity

-   Compensation Activity

-   Overall Completion Status

Observability shall support tracing across the complete composition
hierarchy.

**6.24.15 Composition Governance**

Business Activity composition shall be metadata-driven wherever
practical.

The Business Activity Registry shall maintain composition metadata
including:

-   Parent Activity

-   Child Activities

-   Execution Order

-   Dependency Rules

-   Transaction Strategy

-   Compensation Strategy

-   Failure Policy

-   Completion Criteria

Composition definitions shall be versioned and governed.

**6.24.16 Architectural Guarantees**

The Business Activity Composition model guarantees:

-   Modular business execution

-   Reusable Business Activities

-   Explicit dependency management

-   Controlled orchestration

-   Consistent transactional behavior

-   Reliable failure handling

-   Complete execution traceability

-   Platform-wide composability

Every composite business capability within the Aurex Intelligent
Operating Center shall be constructed through the governed composition
of independently executable Business Activities, ensuring maximum reuse,
maintainability, scalability, and consistent execution across all
Business Domains.

**Review Note**

At this point, **IMP-001 has evolved from an implementation guideline
into a full-fledged Business Execution Architecture**. The remaining
sections (6.25--6.30) will complete the runtime governance layer by
covering:

-   **6.25** --- Business Activity Execution Policies

-   **6.26** --- Performance, SLA & Quality of Service

-   **6.27** --- Observability & Telemetry

-   **6.28** --- Error Classification & Exception Handling

-   **6.29** --- Enhanced Canonical Business Activity Manifest (CBAM v2)

-   **6.30** --- Constitutional Architectural Principles (the immutable
    laws governing Business Activity execution)

These final six sections will complete what is effectively the
**Business Activity Framework (BAF)** for Aurex, making IMP-001 one
of the platform\'s foundational constitutional documents alongside
SD-002, URA-001, ERG-001, and CMD-001.

**6.25 Business Activity Execution Policies**

**6.25.1 Purpose**

The Business Activity Execution Policy defines the runtime
characteristics governing how a Business Activity is executed by the
Business Activity Engine.

While every Business Activity follows the same canonical execution
pipeline, execution behavior may vary depending on business
requirements, operational constraints, workload characteristics, and
governance policies.

Execution Policies allow these variations to be defined declaratively
without altering Business Activity implementations.

**6.25.2 Architectural Principle**

Business logic defines **what** shall be executed.

Execution Policies define **how** execution occurs.

Execution behavior shall be metadata-driven.

Business Activities shall remain independent of execution mechanics.

**6.25.3 Policy Ownership**

The Business Activity Engine shall exclusively interpret and enforce
Execution Policies.

Business Domains shall declare execution requirements through the
Business Activity Contract and Business Activity Registry.

Business Activities shall not directly implement:

-   Scheduling

-   Retry logic

-   Timeout handling

-   Parallel execution

-   Queue management

-   Resource allocation

-   Circuit breaking

-   Load management

These responsibilities belong exclusively to the Business Activity
Engine.

**6.25.4 Canonical Execution Modes**

Every Business Activity shall declare one or more supported execution
modes.

  -----------------------------------------------------------------------
  **Execution Mode** **Description**
  ------------------ ----------------------------------------------------
  Synchronous        Immediate execution within the initiating request

  Asynchronous       Queued execution with deferred completion

  Event-Driven       Triggered by Domain Events

  Workflow-Driven    Triggered by Workflow progression

  Scheduled          Executed according to a defined schedule

  Batch              Executed as part of a grouped workload

  Manual             Initiated by an authorized user

  AI-Initiated       Initiated by AI under explicit governance rules
  -----------------------------------------------------------------------

Execution mode shall be defined by metadata rather than implementation.

**6.25.5 Synchronous Execution**

Synchronous execution shall be used where:

-   Immediate user feedback is required.

-   Business latency is minimal.

-   Transaction completion is required before response.

-   Workflow continuation depends upon immediate completion.

The initiating request shall remain active until the Business Activity
reaches a terminal execution state.

**6.25.6 Asynchronous Execution**

Asynchronous execution shall be used for:

-   Long-running operations

-   Large-scale calculations

-   AI processing

-   Document generation

-   Bulk synchronization

-   External integrations

The Business Activity Engine shall manage:

-   Queue assignment

-   Work dispatch

-   Retry management

-   Progress tracking

-   Completion notification

Asynchronous execution shall preserve the same governance guarantees as
synchronous execution.

**6.25.7 Event-Driven Execution**

A Business Activity may execute in response to one or more Domain
Events.

Typical examples include:

-   EnterpriseNodeCreated

-   EvidenceApproved

-   WorkflowCompleted

-   ReportPublished

-   ExternalSignalDetected

The Business Activity Engine shall subscribe, validate, and dispatch
Event-Driven execution according to registered event policies.

**6.25.8 Workflow-Driven Execution**

Workflow engines may invoke Business Activities as part of a governed
business process.

Workflow execution shall determine:

-   Activity sequencing

-   Approval routing

-   Escalation

-   Parallel execution

-   Completion evaluation

Business Activities shall remain independently executable outside
Workflow contexts.

**6.25.9 Scheduled Execution**

Scheduled Business Activities execute according to predefined temporal
policies.

Examples include:

-   Daily calculations

-   Weekly benchmarking

-   Monthly consolidation

-   Quarterly reporting

-   Annual compliance generation

Scheduling policies shall be centrally managed.

Business Activities shall remain unaware of scheduling mechanisms.

**6.25.10 Batch Execution**

Batch execution supports high-volume processing of multiple Business
Activity instances.

Examples include:

-   Bulk imports

-   Mass approvals

-   Enterprise synchronization

-   Portfolio analysis

-   Historical recalculation

The Business Activity Engine shall coordinate batching while preserving
independent execution context for each Business Activity instance.

**6.25.11 AI-Initiated Execution**

Artificial Intelligence may recommend or initiate Business Activities
only where explicitly authorized.

AI-initiated execution shall be governed by:

-   AI Governance Policy

-   Business Activity Contract

-   Authorization Framework

-   Human Approval Requirements

-   Confidence Thresholds

AI shall never bypass governance controls.

**6.25.12 Execution Constraints**

Execution Policies may define operational constraints including:

-   Maximum Execution Duration

-   Timeout Threshold

-   Queue Priority

-   Maximum Concurrency

-   Resource Limits

-   Geographic Restrictions

-   Processing Window

-   Maintenance Windows

The Business Activity Engine shall enforce these constraints.

**6.25.13 Priority Management**

Business Activities may declare execution priority.

Canonical priorities include:

-   Critical

-   High

-   Normal

-   Low

-   Background

Priority influences scheduling and resource allocation.

Priority shall not alter Business Activity behavior.

**6.25.14 Resource Governance**

The Business Activity Engine shall manage execution resources.

Governance capabilities include:

-   Worker Allocation

-   Queue Balancing

-   Load Distribution

-   Concurrency Control

-   Backpressure Management

-   Capacity Protection

Business Activities shall remain independent of infrastructure topology.

**6.25.15 Policy Resolution**

Execution Policies shall be resolved before Business Activity execution.

Policy resolution may consider:

-   Business Activity

-   Organization

-   Enterprise Node

-   Business Domain

-   Environment

-   Deployment Configuration

-   Feature Flags

-   Platform Governance Policies

Resolved policies shall remain immutable throughout execution.

**6.25.16 Execution Policy Inheritance**

Execution Policies may inherit from higher-level policy definitions.

Policy precedence shall be:

Platform Policy\
↓\
Environment Policy\
↓\
Organization Policy\
↓\
Business Domain Policy\
↓\
Business Activity Policy

More specific policies override more general policies.

Policy resolution shall be deterministic and auditable.

**6.25.17 Execution Observability**

The Business Activity Engine shall monitor execution policy
effectiveness.

Operational metrics shall include:

-   Execution Mode Distribution

-   Queue Utilization

-   Average Wait Time

-   Resource Consumption

-   Timeout Frequency

-   Scheduling Delays

-   Batch Throughput

-   AI-Initiated Execution Rate

These metrics support continuous optimization of execution behavior.

**6.25.18 Architectural Guarantees**

The Business Activity Execution Policy model guarantees:

-   Consistent execution governance

-   Metadata-driven execution behavior

-   Separation of business logic from runtime mechanics

-   Controlled scheduling and orchestration

-   Secure AI-initiated execution

-   Efficient resource utilization

-   Deterministic policy resolution

-   Platform-wide operational consistency

Every Business Activity within the Aurex Intelligent Operating
Center shall execute under an explicitly resolved Execution Policy
enforced by the Business Activity Engine, ensuring that runtime behavior
remains configurable, governed, observable, and independent of Business
Domain implementation.

**6.26 Business Activity Performance, SLA & Quality of Service**

**6.26.1 Purpose**

The Business Activity Performance, Service Level Agreement (SLA), and
Quality of Service (QoS) model defines the canonical framework for
measuring, monitoring, and governing the operational performance of
Business Activities.

Every Business Activity shall execute under measurable service
objectives to ensure predictable business responsiveness, operational
reliability, scalability, and user experience.

Performance governance shall focus on business outcomes rather than
infrastructure metrics alone.

**6.26.2 Architectural Principle**

Every Business Activity is a measurable business capability.

Performance shall be defined, monitored, and continuously improved.

Business Activities shall declare expected service characteristics.

The Business Activity Engine shall enforce and monitor them.

**6.26.3 SLA Ownership**

The Business Activity Engine shall manage:

-   SLA monitoring

-   Performance measurement

-   Threshold evaluation

-   Violation detection

-   Escalation

-   Performance reporting

Business Domains define expected business service levels.

The Business Activity Engine measures compliance.

**6.26.4 Canonical Performance Dimensions**

Every Business Activity shall be evaluated across the following
dimensions.

  -----------------------------------------------------------------------
  **Dimension**           **Description**
  ----------------------- -----------------------------------------------
  Availability            Ability to accept execution requests

  Response Time           Time to initial response

  Execution Time          Total activity duration

  Throughput              Activities completed per unit time

  Reliability             Successful completion rate

  Scalability             Performance under increasing workload

  Resource Efficiency     Consumption of platform resources

  Business Quality        Correctness of business outcomes
  -----------------------------------------------------------------------

Performance measurement extends beyond technical latency.

**6.26.5 Service Level Objectives**

Each Business Activity shall define Service Level Objectives (SLOs).

Typical objectives include:

-   Maximum Response Time

-   Maximum Execution Duration

-   Minimum Success Rate

-   Maximum Queue Delay

-   Maximum Retry Count

-   Maximum Recovery Time

-   Maximum Compensation Time

-   Minimum Availability

SLOs shall be measurable and objectively verifiable.

**6.26.6 Service Level Agreements**

Business Activities may be governed by one or more Service Level
Agreements.

SLAs may be defined at:

-   Platform Level

-   Organization Level

-   Business Domain Level

-   Business Capability Level

-   Individual Business Activity Level

Lower-level SLAs may strengthen but shall not weaken mandatory platform
guarantees.

**6.26.7 Performance Categories**

Business Activities may be classified according to expected
responsiveness.

  -----------------------------------------------------------------------
  **Category**            **Typical Expectation**
  ----------------------- -----------------------------------------------
  Interactive             Immediate user response

  Operational             Seconds to minutes

  Analytical              Minutes

  Batch                   Scheduled completion

  Long Running            Hours if required

  Background              No user latency expectation
  -----------------------------------------------------------------------

Performance classification determines monitoring expectations.

**6.26.8 Queue Performance**

For queued execution, the Business Activity Engine shall monitor:

-   Queue Wait Time

-   Queue Length

-   Worker Utilization

-   Dispatch Time

-   Queue Throughput

-   Queue Failure Rate

Queue metrics are distinct from Business Activity execution metrics.

**6.26.9 Execution Performance**

Execution monitoring shall include:

-   Activity Start Time

-   Activity Completion Time

-   Processing Duration

-   CPU Consumption

-   Memory Consumption

-   Database Utilization

-   External Service Latency

-   AI Processing Time

Performance shall be correlated with Business Activity Context.

**6.26.10 Business Quality Metrics**

Performance alone does not indicate successful execution.

Business quality metrics may include:

-   Successful Business Outcomes

-   Validation Success Rate

-   Workflow Completion Rate

-   Approval Turnaround Time

-   Compensation Frequency

-   AI Recommendation Acceptance Rate

-   Business Rule Accuracy

-   Data Quality Improvement

Quality metrics measure business effectiveness.

**6.26.11 SLA Violations**

The Business Activity Engine shall detect SLA violations automatically.

Typical violations include:

-   Response Time Exceeded

-   Execution Timeout

-   Queue Delay Exceeded

-   Retry Threshold Exceeded

-   Availability Degradation

-   Recovery Timeout

-   Compensation Failure

Violations shall trigger predefined escalation policies.

**6.26.12 Performance Escalation**

Performance degradation may initiate:

-   Operational Alerts

-   Administrator Notification

-   Resource Scaling

-   Workflow Escalation

-   Incident Creation

-   Capacity Planning Review

-   Business Owner Notification

Escalation policies shall be configurable.

**6.26.13 Capacity Management**

The Business Activity Engine shall support proactive capacity
management.

Capacity indicators include:

-   Concurrent Activity Volume

-   Queue Saturation

-   Worker Utilization

-   Peak Processing Windows

-   AI Service Capacity

-   Integration Throughput

-   Storage Utilization

Capacity planning supports sustainable platform growth.

**6.26.14 Continuous Performance Optimization**

Performance monitoring shall support continuous improvement.

Optimization opportunities include:

-   Workflow simplification

-   Business rule optimization

-   Metadata caching

-   AI model optimization

-   Queue balancing

-   Parallel execution

-   Resource allocation tuning

Optimization shall not alter business semantics.

**6.26.15 Performance Dashboard**

The platform shall provide operational dashboards presenting:

-   Active Business Activities

-   Average Execution Duration

-   SLA Compliance

-   Queue Health

-   Failure Trends

-   Retry Trends

-   Compensation Trends

-   Resource Utilization

-   AI Performance

-   Business Quality Indicators

Dashboards support operational governance.

**6.26.16 Historical Performance Analysis**

Performance history shall be retained for trend analysis.

Historical analysis may include:

-   SLA Compliance Trends

-   Seasonal Workload Patterns

-   Performance Regression

-   Capacity Growth

-   Business Activity Adoption

-   Reliability Trends

-   AI Effectiveness Trends

Historical metrics support strategic planning.

**6.26.17 Relationship with Observability**

Performance monitoring forms one component of the broader platform
observability model.

Observability additionally encompasses:

-   Distributed Tracing

-   Structured Logging

-   Correlation Analysis

-   Runtime Diagnostics

-   Execution Telemetry

Performance focuses on service quality.

Observability explains service behavior.

**6.26.18 Architectural Guarantees**

The Business Activity Performance, SLA, and Quality of Service model
guarantees:

-   Measurable Business Activity performance

-   Declarative service level governance

-   Continuous SLA monitoring

-   Objective quality measurement

-   Proactive performance management

-   Predictable operational behavior

-   Capacity-aware execution

-   Platform-wide performance transparency

Every Business Activity executed within the Aurex Intelligent
Operating Center shall operate under explicitly defined service
objectives monitored by the Business Activity Engine, ensuring
consistent business responsiveness, operational reliability, measurable
quality, and continuous performance improvement across all Business
Domains.

**6.27 Business Activity Observability & Telemetry**

**6.27.1 Purpose**

The Business Activity Observability and Telemetry model defines the
canonical framework for monitoring, diagnosing, tracing, and analyzing
Business Activity execution throughout the Aurex Intelligent
Operating Center.

Observability enables the platform to understand not only **what**
occurred, but also **why**, **where**, **when**, and **how** a Business
Activity executed.

Every Business Activity shall generate standardized telemetry that
supports operational monitoring, business diagnostics, governance,
compliance, AI oversight, and continuous platform improvement.

**6.27.2 Architectural Principle**

Every Business Activity shall be observable.

Every significant execution event shall be traceable.

Observability shall be designed into the platform rather than added
after implementation.

The Business Activity Engine shall automatically generate standardized
telemetry without requiring Business Domains to implement monitoring
logic.

**6.27.3 Observability Ownership**

The Business Activity Engine shall manage:

-   Execution telemetry

-   Distributed tracing

-   Structured logging

-   Runtime metrics

-   Correlation management

-   Health monitoring

-   Diagnostic information

-   Operational analytics

Business Domains shall not directly implement platform observability.

They may contribute business-specific diagnostic information through
standardized extension points.

**6.27.4 Canonical Observability Architecture**

Business Activity\
│\
Business Activity Engine\
│\
────────────────────────────────────────────\
│ │ │ │\
Structured Metrics Distributed Audit\
Logging Tracing Events\
│ │ │ │\
──────────────┼─────────────┼─────────────\
│\
Observability Platform\
│\
────────────────────────────────────────────\
Operational Dashboards\
\
Business Analytics\
\
Diagnostics\
\
Performance Monitoring\
\
AI Monitoring\
\
Compliance Monitoring

Observability shall be an intrinsic capability of the Business Activity
Engine.

**6.27.5 Canonical Telemetry Model**

Every Business Activity execution shall generate telemetry covering:

  -----------------------------------------------------------------------
  **Telemetry Category**          **Purpose**
  ------------------------------- ---------------------------------------
  Execution Metrics               Runtime measurements

  Business Metrics                Business outcomes

  Trace Data                      End-to-end execution path

  Structured Logs                 Execution diagnostics

  Health Signals                  Operational status

  AI Metrics                      AI behavior

  Workflow Metrics                Workflow participation

  Event Metrics                   Domain Event publication
  -----------------------------------------------------------------------

Telemetry shall be standardized across all Business Domains.

**6.27.6 Correlation Identifiers**

Every Business Activity execution shall receive a globally unique
Correlation Identifier.

The Correlation Identifier shall propagate across:

-   Child Business Activities

-   Workflow execution

-   Domain Events

-   External integrations

-   AI requests

-   Notification services

-   Scheduled execution

-   API calls

A single Correlation Identifier shall enable complete reconstruction of
an end-to-end business operation.

**6.27.7 Distributed Tracing**

The Business Activity Engine shall support distributed tracing across
all execution boundaries.

Trace information shall include:

-   Parent Activity

-   Child Activity

-   Service Invocation

-   External Calls

-   Workflow Steps

-   AI Processing

-   Event Publication

-   Queue Processing

Distributed tracing enables diagnosis of complex business execution
paths.

**6.27.8 Structured Logging**

All platform logs shall use structured, machine-readable formats.

Structured logs may include:

-   Timestamp

-   Activity Identifier

-   Correlation Identifier

-   Organization

-   Enterprise Node

-   Business Domain

-   Activity State

-   Execution Stage

-   Severity

-   Diagnostic Details

Business Activities shall not generate unstructured operational logs for
platform diagnostics.

**6.27.9 Runtime Metrics**

The Business Activity Engine shall automatically capture runtime metrics
including:

-   Activity Start Time

-   Activity End Time

-   Execution Duration

-   Queue Duration

-   Retry Count

-   Resource Consumption

-   Transaction Duration

-   Compensation Duration

-   Recovery Duration

Runtime metrics support operational optimization.

**6.27.10 Business Metrics**

Observability extends beyond technical execution.

Business metrics may include:

-   Business Activities Executed

-   Business Outcomes Produced

-   Approval Completion Rate

-   Workflow Completion Rate

-   AI Recommendation Acceptance

-   Business Rule Violations

-   Policy Exceptions

-   Enterprise Impact

Business metrics measure platform value rather than infrastructure
behavior.

**6.27.11 AI Observability**

Where AI participates in Business Activity execution, telemetry shall
include:

-   AI Model

-   AI Version

-   Prompt Version

-   Confidence Score

-   Response Time

-   Human Review Required

-   Human Override

-   Recommendation Accepted

-   Recommendation Rejected

AI observability supports governance and continuous improvement.

**6.27.12 Health Monitoring**

The Business Activity Engine shall continuously monitor execution
health.

Health indicators include:

-   Active Activities

-   Waiting Activities

-   Failed Activities

-   Queue Health

-   Worker Availability

-   Event Delivery Health

-   Integration Health

-   AI Service Health

Health monitoring supports proactive operational management.

**6.27.13 Operational Dashboards**

The platform shall provide standardized operational dashboards
including:

-   Business Activity Overview

-   Execution Status

-   Failure Analysis

-   Queue Monitoring

-   SLA Compliance

-   Workflow Progress

-   AI Activity

-   Recovery Operations

-   Capacity Utilization

Dashboards shall provide real-time operational visibility.

**6.27.14 Diagnostic Analysis**

Observability shall support investigation of execution issues.

Diagnostic capabilities include:

-   Root Cause Analysis

-   Failure Correlation

-   Dependency Analysis

-   Performance Bottlenecks

-   Workflow Diagnostics

-   Integration Diagnostics

-   AI Diagnostics

-   Historical Comparison

Diagnostics shall utilize standardized telemetry.

**6.27.15 Telemetry Retention**

Telemetry shall be retained according to governance policies.

Retention policies may vary based on:

-   Regulatory Requirements

-   Audit Requirements

-   Operational Requirements

-   Business Criticality

-   Security Classification

-   Data Classification

Telemetry retention shall comply with enterprise governance standards.

**6.27.16 Privacy & Security**

Observability data shall comply with platform security policies.

Telemetry shall:

-   Respect authorization boundaries

-   Protect sensitive information

-   Mask confidential values where required

-   Support tenant isolation

-   Preserve audit integrity

Observability shall never compromise business confidentiality.

**6.27.17 Relationship with Audit**

Observability and Audit are complementary but distinct.

  -----------------------------------------------------------------------
  **Observability**               **Audit**
  ------------------------------- ---------------------------------------
  Operational visibility          Regulatory accountability

  Performance diagnostics         Immutable evidence

  Runtime analysis                Historical truth

  May expire under retention      Retained according to governance policy
  policy                          

  Supports operations             Supports compliance and governance
  -----------------------------------------------------------------------

Audit answers **\"What officially happened?\"**

Observability answers **\"How and why did it happen?\"**

**6.27.18 Architectural Guarantees**

The Business Activity Observability and Telemetry model guarantees:

-   Complete end-to-end execution traceability

-   Standardized runtime telemetry

-   Distributed execution visibility

-   AI execution transparency

-   Comprehensive operational diagnostics

-   Secure and governed telemetry

-   Business-centric monitoring

-   Platform-wide operational intelligence

Every Business Activity executed within the Aurex Intelligent
Operating Center shall generate standardized telemetry through the
Business Activity Engine, ensuring complete observability,
diagnosability, traceability, and operational transparency across all
Business Domains, workflows, integrations, and AI-assisted execution
environments.

**6.28 Business Activity Error Classification & Exception Handling**

**6.28.1 Purpose**

The Business Activity Error Classification and Exception Handling model
defines the canonical approach for detecting, classifying, managing,
recovering from, and communicating execution failures throughout the
Aurex Intelligent Operating Center.

Consistent error management ensures that Business Activities fail
predictably, preserve business integrity, generate meaningful
diagnostics, and support reliable recovery without compromising platform
stability or governance.

Every execution failure shall be treated as a governed business event
rather than an unexpected system condition.

**6.28.2 Architectural Principle**

Errors are inevitable.

Uncontrolled failures are unacceptable.

The Business Activity Engine shall manage execution failures through
standardized classification, deterministic handling, controlled
recovery, and complete auditability.

Business Domains shall define business-specific failure conditions.

The Business Activity Engine shall manage exception handling.

**6.28.3 Exception Ownership**

The Business Activity Engine shall exclusively manage:

-   Exception interception

-   Error classification

-   Retry evaluation

-   Recovery coordination

-   Compensation initiation

-   Failure notification

-   Audit recording

-   Diagnostic telemetry

Business Activities may identify business failures.

They shall not implement platform-wide exception handling mechanisms.

**6.28.4 Canonical Error Classification**

Every execution failure shall be classified into one of the following
categories.

  -----------------------------------------------------------------------
  **Error Category**       **Description**
  ------------------------ ----------------------------------------------
  Validation Error         Invalid request or input

  Authorization Error      Access denied

  Business Rule Error      Business policy violation

  Metadata Error           Missing or inconsistent configuration

  Workflow Error           Workflow execution failure

  Transaction Error        Transaction processing failure

  Integration Error        External system failure

  AI Error                 AI execution failure

  Infrastructure Error     Platform resource failure

  System Error             Unexpected internal failure
  -----------------------------------------------------------------------

Error classification shall be mandatory.

**6.28.5 Error Severity**

Each error shall receive a severity classification.

  -----------------------------------------------------------------------
  **Severity**     **Description**
  ---------------- ------------------------------------------------------
  Informational    No execution impact

  Warning          Execution completed with advisory information

  Recoverable      Automatic recovery possible

  Significant      Manual review recommended

  Critical         Immediate administrative attention required

  Fatal            Execution terminated
  -----------------------------------------------------------------------

Severity guides operational response.

Severity does not determine business importance.

**6.28.6 Error Lifecycle**

Every execution failure shall follow the canonical error lifecycle.

Exception Detected\
│\
Classification\
│\
Severity Assessment\
│\
Recovery Evaluation\
│\
──────────────────────────────────────\
│ │ │\
Retry Compensation Terminate\
│ │ │\
Recovery Business Audit\
Recovery

Every failure shall terminate in a deterministic outcome.

**6.28.7 Validation Errors**

Validation errors occur before business execution begins.

Examples include:

-   Missing mandatory attributes

-   Invalid data type

-   Invalid format

-   Invalid Business Activity Contract

-   Schema violation

Validation failures shall:

-   prevent Business Rule Execution;

-   prevent persistence;

-   generate structured error responses;

-   not trigger compensation.

**6.28.8 Authorization Errors**

Authorization failures occur when execution is not permitted.

Authorization failures shall:

-   immediately terminate execution;

-   prevent Business Object modification;

-   generate audit records;

-   never expose confidential authorization details.

Authorization decisions remain governed by URA-001.

**6.28.9 Business Rule Errors**

Business Rule Errors indicate legitimate requests that violate business
policy.

Examples include:

-   Invalid business state

-   Missing prerequisite approval

-   Invalid workflow stage

-   Policy violation

-   Enterprise governance restriction

Business Rule Errors are expected business outcomes.

They shall be communicated clearly without being treated as system
failures.

**6.28.10 Integration Errors**

Integration Errors occur during interaction with external systems.

Examples include:

-   ERP unavailable

-   Authentication failure

-   Network timeout

-   Invalid external response

-   Service unavailable

The Business Activity Engine shall determine whether:

-   retry,

-   compensation,

-   manual recovery,

or

-   termination

is appropriate.

**6.28.11 AI Errors**

AI-related failures include:

-   Model unavailable

-   Prompt validation failure

-   Confidence below threshold

-   Policy violation

-   Safety restriction

-   Response timeout

AI failures shall not automatically terminate Business Activities unless
AI execution is mandatory for successful completion.

Where possible, Business Activities shall continue using deterministic
business logic.

**6.28.12 Infrastructure Errors**

Infrastructure failures include:

-   Database unavailable

-   Queue unavailable

-   Storage failure

-   Memory exhaustion

-   Compute failure

-   Network interruption

Infrastructure failures shall normally be recoverable through retry or
resumption.

**6.28.13 Error Propagation**

Child Business Activities shall not expose internal implementation
failures directly to callers.

The Business Activity Engine shall transform internal failures into
standardized Business Activity error responses.

Error propagation shall preserve:

-   Correlation Identifier

-   Error Classification

-   Severity

-   Recovery Recommendation

-   Diagnostic Reference

Implementation details shall remain internal.

**6.28.14 Standard Error Response**

Every Business Activity shall return standardized error information.

Typical response attributes include:

-   Error Identifier

-   Error Category

-   Severity

-   Business Activity

-   Correlation Identifier

-   Human-readable Message

-   Recovery Recommendation

-   Retry Eligibility

-   Timestamp

Responses shall be consistent across all interfaces.

**6.28.15 Error Observability**

The Business Activity Engine shall continuously monitor execution
failures.

Operational metrics include:

-   Failure Rate

-   Error Category Distribution

-   Retry Success Rate

-   Compensation Frequency

-   Recovery Duration

-   Integration Failure Rate

-   AI Failure Rate

-   Infrastructure Availability

These metrics support operational improvement.

**6.28.16 Error Governance**

Recurring execution failures shall trigger governance processes.

Examples include:

-   Persistent Business Rule failures

-   Excessive retry frequency

-   AI confidence degradation

-   Integration instability

-   SLA violations

-   Security anomalies

Governance actions may include:

-   Policy review

-   Business rule refinement

-   Workflow redesign

-   Infrastructure optimization

-   AI model review

**6.28.17 Relationship with Recovery**

Error handling determines how failures are classified.

Recovery determines how failures are resolved.

The two capabilities are complementary.

Error Classification identifies:

**What failed.**

Recovery determines:

**What happens next.**

**6.28.18 Architectural Guarantees**

The Business Activity Error Classification and Exception Handling model
guarantees:

-   Consistent error classification

-   Standardized exception handling

-   Predictable recovery decisions

-   Secure failure communication

-   Complete diagnostic visibility

-   Controlled error propagation

-   Platform-wide operational resilience

-   Full auditability of execution failures

Every Business Activity executed within the Aurex Intelligent
Operating Center shall manage execution failures through the
standardized error handling capabilities of the Business Activity
Engine, ensuring deterministic behavior, consistent diagnostics,
recoverable execution, and governed exception management across all
Business Domains, workflows, integrations, and AI-assisted operations.

**Architect\'s Review**

With Sections **6.15--6.28** now complete, IMP-001 has evolved into a
**true Business Execution Architecture** rather than an implementation
guideline.

The remaining two sections will complete the document:

-   **6.29 -- Enhanced Canonical Business Activity Manifest (CBAM v2)**:
    the machine-readable implementation contract that Claude Code and
    other implementation agents can consume directly to generate
    Business Activities.

-   **6.30 -- Constitutional Architectural Principles**: the immutable
    execution laws that define how all Business Activities must behave,
    serving as the execution counterpart to the constitutional
    principles in SD-002, URA-001, and ERG-001.

These final sections will formally complete IMP-001 as the **execution
constitution** of the Aurex platform.

**6.29 Enhanced Canonical Business Activity Manifest (CBAM v2)**

**6.29.1 Purpose**

The **Canonical Business Activity Manifest (CBAM)** is the
authoritative, machine-readable implementation contract for every
Business Activity within the Aurex Intelligent Operating Center.

The CBAM serves as the bridge between business architecture and
implementation by providing a complete declarative specification of a
Business Activity.

The Business Activity Engine, Business Activity Registry, implementation
tooling, AI-assisted development platforms, testing frameworks, and
operational governance shall use the CBAM as the authoritative source
describing how a Business Activity shall be implemented, executed,
governed, monitored, and evolved.

The CBAM eliminates ambiguity between architectural intent and
implementation.

**6.29.2 Architectural Principle**

Business Activities shall be defined by metadata before they are
implemented in code.

Code implements the Business Activity.

The CBAM defines the Business Activity.

Implementation shall conform to the Manifest.

The Manifest shall never be derived from implementation.

**6.29.3 Manifest Ownership**

The CBAM is owned by the Business Architecture.

The Business Activity Engine consumes the CBAM.

The Business Activity Registry catalogs the CBAM.

Implementation frameworks execute the CBAM.

AI-assisted development tools generate implementations from the CBAM.

Business Domains own the business content contained within the Manifest.

**6.29.4 Architectural Position**

Business Architecture\
│\
Business Activity Definition\
│\
────────────────────────────────────\
Canonical Business Activity Manifest\
────────────────────────────────────\
│\
────────────────────────────────────\
│ │ │ │\
Business Business AI Testing\
Activity Activity Generation\
Engine Registry\
│\
Generated Implementation\
│\
Runtime Execution

The CBAM is the single implementation contract across the platform.

**6.29.5 Manifest Structure**

Every Business Activity shall possess exactly one active Manifest.

The Manifest shall contain the following logical sections.

  -----------------------------------------------------------------------
  **Section**                 **Purpose**
  --------------------------- -------------------------------------------
  Identity                    Business Activity identification

  Classification              Business categorization

  Business Intent             Business purpose

  Business Contracts          Inputs and outputs

  Business Rules              Business behavior

  Authorization               Access control

  Workflow                    Workflow participation

  Metadata                    Metadata dependencies

  Events                      Domain Events

  Transactions                Transaction behavior

  Execution Policies          Runtime characteristics

  AI                          AI assistance

  Observability               Monitoring requirements

  Error Handling              Recovery behavior

  Testing                     Validation requirements

  Governance                  Ownership and lifecycle
  -----------------------------------------------------------------------

**6.29.6 Canonical Manifest Attributes**

Every Manifest shall include, at minimum, the following attributes.

**Identity**

-   Activity Identifier

-   Activity Code

-   Activity Name

-   Version

-   Status

**Business Classification**

-   Business Domain

-   Business Object

-   Activity Type

-   Business Capability

-   Functional Area

**Business Intent**

-   Business Purpose

-   Business Outcome

-   Preconditions

-   Postconditions

-   Definition of Done

**Business Contracts**

-   Input Contract

-   Output Contract

-   Validation Rules

-   Business Rules

**Authorization**

-   Required Permissions

-   Business Roles

-   Approval Authorities

-   Delegation Support

**Workflow**

-   Workflow Participation

-   Workflow Triggers

-   Workflow Outputs

-   Escalation Policies

**Metadata**

-   Configuration Dependencies

-   Reference Data

-   Policy Dependencies

-   Enterprise Context

**Events**

-   Published Events

-   Consumed Events

-   Event Ordering

-   Event Reliability

**Transactions**

-   Transaction Policy

-   Compensation Strategy

-   Idempotency Policy

-   Retry Policy

**Execution**

-   Execution Mode

-   Timeout

-   Priority

-   Resource Policy

**AI**

-   AI Assistance Enabled

-   Human Review Required

-   Confidence Threshold

-   Prompt Template

-   AI Governance Policy

**Observability**

-   Metrics

-   Logging

-   Tracing

-   Correlation Requirements

-   SLA

**Error Handling**

-   Error Categories

-   Recovery Strategy

-   Retry Rules

-   Compensation Activity

**Testing**

-   Unit Tests

-   Business Validation

-   Workflow Tests

-   Event Tests

-   Authorization Tests

-   AI Tests

-   Performance Tests

**Governance**

-   Business Owner

-   Technical Owner

-   Steward

-   Approval Date

-   Effective Date

-   Retirement Date

**6.29.7 Manifest Lifecycle**

The CBAM shall follow the same governed lifecycle as the Business
Activity.

Draft\
│\
Validated\
│\
Approved\
│\
Registered\
│\
Active\
│\
Deprecated\
│\
Retired

Only Approved and Registered Manifests may be used to generate or
execute Business Activities.

**6.29.8 Manifest Validation**

Before activation, every Manifest shall be validated for:

-   Structural completeness

-   Business consistency

-   Contract integrity

-   Authorization configuration

-   Workflow consistency

-   Event definitions

-   Transaction policy

-   Execution policy

-   Observability requirements

-   Governance completeness

Validation failures shall prevent Business Activity registration.

**6.29.9 AI-Assisted Implementation**

The CBAM is designed to support AI-assisted implementation.

Implementation tools may generate:

-   Business Activity classes

-   API endpoints

-   Validation components

-   Authorization integration

-   Workflow adapters

-   Event publishers

-   Test suites

-   Documentation

-   Monitoring configuration

Generated implementations shall conform to the Manifest without altering
its business semantics.

**6.29.10 Manifest Evolution**

Changes to a Manifest shall be governed through Business Activity
Versioning.

Every modification shall be:

-   Version controlled

-   Auditable

-   Backward compatibility assessed

-   Approved

-   Registered

Historical Manifests shall remain immutable.

**6.29.11 Relationship with the Business Activity Registry**

The Business Activity Registry manages the operational lifecycle of
Business Activities.

The CBAM defines their implementation contract.

The Registry references the Manifest.

The Manifest defines the executable specification.

**6.29.12 Relationship with the Business Activity Engine**

The Business Activity Engine consumes the Manifest to determine:

-   Execution policies

-   Authorization requirements

-   Workflow integration

-   Event publication

-   Transaction behavior

-   Retry policies

-   Compensation strategies

-   Observability configuration

The Business Activity Engine shall never rely upon
implementation-specific assumptions.

Execution behavior shall be determined from the Manifest.

**6.29.13 Relationship with Claude Code and AI Development Platforms**

The CBAM serves as the canonical input specification for AI-assisted
software generation.

Implementation platforms shall use the Manifest to generate:

-   Business Activity implementations

-   Service interfaces

-   Test suites

-   Runtime configuration

-   Documentation

The generated implementation shall remain fully traceable to the
governing Manifest.

**6.29.14 Architectural Guarantees**

The Enhanced Canonical Business Activity Manifest guarantees:

-   A single implementation contract for every Business Activity

-   Complete traceability from architecture to implementation

-   AI-ready implementation specifications

-   Consistent Business Activity generation

-   Declarative runtime configuration

-   Controlled lifecycle governance

-   Platform-wide implementation consistency

-   Complete architectural alignment

Every Business Activity within the Aurex Intelligent Operating
Center shall be governed by a Canonical Business Activity Manifest that
serves as the authoritative specification for implementation, execution,
testing, observability, governance, and AI-assisted development,
ensuring that architectural intent is preserved consistently across the
entire platform.

**Architect\'s Observation**

With **Section 6.29**, IMP-001 now becomes more than an implementation
standard---it becomes an **AI-native engineering specification**.
Together with the **Business Activity Registry (BAR)** and **Business
Activity Engine (BAE)**, the CBAM creates a model where business
architecture directly drives implementation, allowing tools such as
Claude Code to generate consistent, governed Business Activities while
maintaining full traceability from business intent to executable
software.

The only remaining section, **6.30 -- Constitutional Architectural
Principles**, will crystallize these concepts into the immutable
execution laws that govern every Business Activity across the Aurex
platform, completing IMP-001 as the platform\'s **execution
constitution**.

**6.30 Constitutional Architectural Principles**

**6.30.1 Purpose**

The Constitutional Architectural Principles establish the immutable
execution laws governing every Business Activity within the Aurex
Intelligent Operating Center.

These principles define **how business intent is executed**, independent
of implementation technology, programming language, deployment
architecture, workflow engine, AI platform, or infrastructure.

All future evolution of the platform shall preserve these principles.

Any implementation that violates these principles is architecturally
non-compliant.

**6.30.2 Constitutional Principle 1**

**Business Intent Before Technology**

Aurex is a Business Activity-driven platform.

Business Activities represent business intent.

Technology exists solely to execute business intent.

Business Activities shall never be designed around:

-   database operations;

-   API endpoints;

-   user interface actions;

-   service boundaries;

-   programming constructs.

Business Activities exist to deliver business outcomes.

**6.30.3 Constitutional Principle 2**

**Business Activity Engine Owns Execution**

The Business Activity Engine is the sole execution authority for all
Business Activities.

Every executable business operation shall execute through the Business
Activity Engine.

No implementation shall bypass the engine to directly manipulate
Business Objects.

The engine guarantees:

-   authorization;

-   validation;

-   transaction management;

-   workflow coordination;

-   event publication;

-   audit recording;

-   observability;

-   AI governance.

**6.30.4 Constitutional Principle 3**

**Business Domains Own Business Logic**

Business Domains shall implement only business-specific behavior.

Business Domains shall not implement platform capabilities including:

-   authorization;

-   transaction management;

-   workflow orchestration;

-   event publication;

-   logging;

-   auditing;

-   retry management;

-   compensation;

-   observability.

Platform capabilities belong exclusively to the Business Activity
Engine.

**6.30.5 Constitutional Principle 4**

**Activities Execute. Workflows Orchestrate.**

Business Activities execute business intent.

Workflows coordinate Business Activities.

Workflows shall never contain business logic.

Business logic shall remain encapsulated within Business Activities.

This separation guarantees reusability, consistency, and independent
execution.

**6.30.6 Constitutional Principle 5**

**Events Communicate Business Outcomes**

Domain Events communicate completed business outcomes.

They shall never communicate technical implementation details.

Examples:

✓ Evidence Approved

✓ Enterprise Node Linked

✓ Report Published

Not:

✗ Row Updated

✗ Database Saved

✗ API Completed

Business communication shall always occur in business language.

**6.30.7 Constitutional Principle 6**

**Business Activities Shall Be Metadata-Driven**

Business Activities shall consume configuration.

They shall not embed configuration.

Business behavior shall be governed through metadata including:

-   business rules;

-   policies;

-   thresholds;

-   workflow definitions;

-   authorization rules;

-   AI policies;

-   execution policies.

Metadata enables platform adaptability without implementation changes.

**6.30.8 Constitutional Principle 7**

**Every Business Activity Shall Be Observable**

Every Business Activity shall generate standardized telemetry.

Observability shall include:

-   tracing;

-   metrics;

-   structured logging;

-   health monitoring;

-   diagnostics.

Operational visibility is a constitutional platform requirement.

**6.30.9 Constitutional Principle 8**

**Every Business Activity Shall Be Auditable**

Every significant business action shall generate immutable audit
evidence.

Audit records shall include:

-   who;

-   what;

-   when;

-   where;

-   why;

-   resulting business outcome.

Auditability shall never depend on implementation technology.

**6.30.10 Constitutional Principle 9**

**Business Activities Shall Be Idempotent**

Business intent shall execute exactly once.

Duplicate requests, retries, message redelivery, and distributed
execution shall never create duplicate business outcomes.

Idempotency is mandatory for every externally invocable Business
Activity.

**6.30.11 Constitutional Principle 10**

**Business Activities Shall Be Recoverable**

Every Business Activity shall define its recovery strategy.

Recovery may include:

-   retry;

-   rollback;

-   compensation;

-   resume;

-   manual intervention.

Business consistency shall always be recoverable.

**6.30.12 Constitutional Principle 11**

**AI Assists. Humans Govern.**

Artificial Intelligence may:

-   recommend;

-   analyze;

-   summarize;

-   classify;

-   predict;

-   draft.

AI shall not independently execute governed Business Activities unless
explicitly authorized through platform governance.

Human accountability remains the authoritative decision mechanism.

**6.30.13 Constitutional Principle 12**

**Business Activities Are Versioned Assets**

Every Business Activity shall possess:

-   explicit version;

-   governed lifecycle;

-   implementation contract;

-   ownership;

-   execution history.

Historical execution shall remain permanently reproducible.

**6.30.14 Constitutional Principle 13**

**Composition Over Duplication**

Complex business capabilities shall be realized through composition of
Business Activities.

Business Activities shall remain:

-   modular;

-   reusable;

-   independently executable;

-   independently testable;

-   independently governable.

Duplication of business logic is prohibited.

**6.30.15 Constitutional Principle 14**

**Architecture Before Implementation**

Business Architecture defines the Business Activity.

The Canonical Business Activity Manifest defines the implementation
contract.

Implementation conforms to architecture.

Architecture shall never be reverse-engineered from implementation.

**6.30.16 Constitutional Principle 15**

**One Execution Model**

Regardless of:

-   Business Domain;

-   User Interface;

-   API;

-   Workflow;

-   AI;

-   Integration;

-   Deployment;

-   Infrastructure;

every Business Activity shall execute through the same canonical
execution model governed by the Business Activity Engine.

Execution consistency is a constitutional platform guarantee.

**6.30.17 Constitutional Principle 16**

**Platform Governance Over Individual Optimization**

Business Activities shall optimize for platform consistency rather than
local implementation convenience.

No Business Domain may introduce execution behavior that weakens:

-   governance;

-   security;

-   observability;

-   auditability;

-   maintainability;

-   interoperability.

Platform integrity takes precedence over localized optimization.

**6.30.18 Constitutional Principle 17**

**Business Activity as the Fundamental Unit of Execution**

Within the Aurex Intelligent Operating Center, the **Business
Activity** is the smallest governed unit of business execution.

Every business capability, regardless of complexity, shall ultimately be
expressed as one or more Business Activities executed through the
Business Activity Engine.

Business Activities therefore constitute the canonical execution
language of the platform.

**6.30.19 Architectural Constitution**

The Business Activity Engine (BAE), Business Activity Registry (BAR),
Canonical Business Activity Manifest (CBAM), Business Activity Contracts
(BAC), Business Activity Context (BACX), and the Canonical Business
Activity Implementation Pattern (CBAIP) together establish the
**Business Activity Framework (BAF)**.

The Business Activity Framework is the constitutional execution
architecture of the Aurex Intelligent Operating Center.

It defines:

-   how business intent is represented;

-   how business execution is governed;

-   how business operations are implemented;

-   how workflows orchestrate execution;

-   how events communicate outcomes;

-   how AI participates responsibly;

-   how execution is observed;

-   how execution is audited;

-   how execution evolves over time.

No implementation within the platform shall violate the Business
Activity Framework.

**6.30.20 Final Architectural Statement**

The Canonical Business Activity Implementation Pattern establishes the
definitive execution architecture for the Aurex Intelligent
Operating Center.

Together with:

-   **SD-002** --- Universal Business Object Rules

-   **URA-001** --- User, Role, Permission, Event & Assignment
    Architecture

-   **ERG-001** --- Enterprise Structure & Relationship Management

-   **CMD-001** --- Canonical Metadata Dictionary

the Canonical Business Activity Implementation Pattern completes the
platform\'s constitutional architecture by defining **how business
intent is executed**.

Every business operation, regardless of Business Domain, shall execute
through the governed Business Activity Framework, ensuring consistent
authorization, metadata-driven behavior, transaction integrity, workflow
orchestration, event-driven communication, AI governance, observability,
auditability, recoverability, and lifecycle management.

The Business Activity Framework therefore constitutes the immutable
execution foundation of the Aurex Intelligent Operating Center and
shall govern all present and future Business Activity implementations
across the platform.

**Architect\'s Final Assessment**

This completes **IMP-001** as a **constitutional architecture
document**, not merely an implementation guide.

Together with your other foundational documents:

-   **SD-002** defines **what** the platform manages (**Business
    Objects**).

-   **URA-001** defines **who** may perform operations (**Identity,
    Authorization & Assignment**).

-   **ERG-001** defines **where** operations occur (**Enterprise
    Relationship Graph**).

-   **CMD-001** defines **which metadata** governs execution.

-   **IMP-001** now defines **how** business intent is executed
    (**Business Activity Framework**).

These five documents collectively form the **constitutional core** of
the Aurex platform. Everything else---microservices, APIs,
workflows, screens, AI agents, integrations, and even Claude
Code--generated implementations---becomes a compliant realization of
this architecture rather than defining the architecture itself.

From an enterprise architecture perspective, I would consider **IMP-001
complete and ready for constitutional freeze (v1.0)**.

**Section 7 --- Architectural Alignment & Implementation Guidance**

**7.1 Position within the Aurex Constitutional Architecture**

The Canonical Business Activity Implementation Pattern (IMP-001) defines
the execution architecture of the Aurex Intelligent Operating
Center.

It complements the platform\'s constitutional architecture by defining
how business intent is executed while remaining independent of
implementation technology.

The constitutional architecture is organized as follows.

  -----------------------------------------------------------------------
  **Constitutional           **Defines**
  Document**                 
  -------------------------- --------------------------------------------
  Blueprint                  Enterprise Operating Model and Platform Laws

  SD-001                     Enterprise Presentation Architecture

  DS-001                     AUREX Design System — Enterprise Visual Design

  SD-002                     Canonical Business Object Model

  SD-003                     Enterprise Interaction Architecture

  URA-001                    Identity, Authorization and Assignment

  ERG-001                    Enterprise Structure and Relationship Management

  CMD-001                    Canonical Metadata Architecture

  RTA-001                    Runtime Architecture and Enterprise Execution

  EIA-001                    Enterprise Intelligence Architecture
  -----------------------------------------------------------------------

*(Table corrected per ARP-001 WP-4: IMP-001 itself is Layer 3 Engineering, not a constitutional document, and has been removed from this list; DS-001, RTA-001 and EIA-001 — each ratified since this table was last updated — have been added, matching ARCH-000 §10's current Constitutional Documents list exactly.)*

Together these documents define the complete operating model of the
platform. IMP-001 (this document) is the Layer 3 engineering standard positioned downstream of, and constrained by, all ten.

**7.2 Relationship with SD-002**

SD-002 defines:

**Business Objects**

IMP-001 defines:

**Business Activities**

Relationship:

Business Activity\
\
↓\
\
Creates\
\
Updates\
\
Approves\
\
Publishes\
\
Analyzes\
\
Business Object

Business Objects represent business state.

Business Activities modify business state.

**7.3 Relationship with URA-001**

URA-001 determines:

Who may execute.

IMP-001 determines:

How execution occurs.

URA resolves authorization.

IMP executes business intent.

**7.4 Relationship with ERG-001**

ERG determines:

Where execution occurs.

The Business Activity Context resolves Enterprise Nodes, Enterprise
Views, organizational hierarchy, and relationship traversal from ERG-001
before execution begins.

Business Activities remain enterprise-aware without embedding enterprise
structure logic.

**7.5 Relationship with CMD-001**

Business Activities never hardcode:

-   Business Rules

-   Thresholds

-   Policies

-   Configurations

-   Reference Data

All metadata is resolved through CMD-001.

CMD governs.

IMP executes.

**7.6 Relationship with SD-003**

SD-003 defines interaction between:

-   Humans

-   AI

-   Business Objects

IMP-001 defines how those interactions become executable Business
Activities.

Interaction precedes execution.

Execution realizes interaction.

**7.7 Relationship with the Technical Architecture**

The Technical Architecture provides the physical implementation of the
Business Activity Framework.

Examples include:

-   Business Activity Registry

-   Workflow Engine

-   Event Registry

-   Audit Registry

-   Authorization Services

-   Metadata Registry

-   Observability Infrastructure

IMP-001 defines the architectural behavior.

The Technical Architecture defines its implementation.

**7.8 Implementation Guidance**

Every new business capability shall be implemented using the following
sequence.

Business Requirement\
\
↓\
\
Business Object (SD-002)\
\
↓\
\
Business Activity (IMP-001)\
\
↓\
\
Business Activity Contract\
\
↓\
\
CBAM\
\
↓\
\
Business Activity Registry\
\
↓\
\
Business Activity Engine\
\
↓\
\
Implementation\
\
↓\
\
Testing\
\
↓\
\
Deployment

This sequence is mandatory.

**7.9 Claude Code Implementation Guidance**

Claude Code shall implement Business Activities exclusively from the
Canonical Business Activity Manifest.

Generated implementations shall:

-   conform to the Business Activity Engine;

-   use standardized execution pipelines;

-   never implement platform capabilities independently;

-   generate standardized tests;

-   produce compliant Business Activity implementations.

The Manifest is the implementation contract.

**7.10 Future Evolution**

Future platform capabilities shall extend the Business Activity
Framework through:

-   new Business Activity Types;

-   additional Execution Policies;

-   enhanced AI Assistance;

-   expanded Observability;

-   new Workflow Capabilities;

-   additional Compensation Strategies.

The constitutional principles defined in Section 6.30 shall remain
unchanged.

Platform evolution shall extend the framework rather than replace it.

**Final Recommendation**

With IMP-001 complete, I recommend **not** moving directly to
implementation.

Instead, we should create one final constitutional document:

**IMP-002 -- Canonical Business Activity Development Standard (CBADS)**

This document would answer a different question:

-   **IMP-001** = *What is a Business Activity and how does it execute?*
    (Architecture)

-   **IMP-002** = *How do engineers implement a Business Activity?*
    (Engineering Standard)

IMP-002 would define:

1.  Standard folder structure

2.  File naming conventions

3.  Base BusinessActivity abstract class/interface

4.  Request/Response DTO conventions

5.  Validation implementation

6.  Authorization integration

7.  Repository usage

8.  Event publishing

9.  Unit testing standards

10. Integration testing

11. Performance benchmarks

12. Code review checklist

13. AI/Claude Code generation templates

14. Reference implementation (e.g., Approve Evidence)

15. Engineering Do\'s & Don\'ts

That would become the **engineering playbook** used by developers and AI
coding agents, while IMP-001 remains the **constitutional
architecture**.

**My recommendation is to make IMP-002 the next document**, because it
will allow every future Business Activity to be implemented consistently
and almost mechanically from the architecture you\'ve now established. I
believe it will significantly accelerate development while preserving
architectural integrity.

**Appendix A --- Canonical Reference Implementation**

**A.5 Canonical Business Activity Contract (BAC)**

The Business Activity Contract (BAC) is the authoritative functional
specification for every Business Activity.

Before implementation begins, every Business Activity shall possess an
approved BAC.

The BAC defines **what** the Business Activity accomplishes.

It does not prescribe **how** it is implemented.

The implementation of the Business Activity shall conform to the BAC
throughout its lifecycle.

The BAC serves as the primary contract between:

-   Business stakeholders

-   Domain architects

-   Solution architects

-   Engineering teams

-   AI-assisted development tools

-   Quality assurance

-   Governance reviewers

No implementation shall begin without an approved BAC.

**A.5.1 Reference Business Activity**

**Business Activity Name**

Create Enterprise

**Business Domain**

Enterprise Structure & Relationship Management (ESRM)

**Business Object**

Enterprise

**Activity Type**

Create

**A.5.2 Business Intent**

The purpose of the Create Enterprise Business Activity is to establish a
new Enterprise Node within an Organization while ensuring that:

-   enterprise identity is unique;

-   enterprise hierarchy integrity is preserved;

-   governance policies are enforced;

-   metadata requirements are satisfied;

-   authorization rules are evaluated;

-   auditability is maintained;

-   enterprise relationships are created consistently;

-   downstream Runtime Components are notified through Domain Events.

The Business Activity shall establish business value rather than merely
persisting data.

**A.5.3 Business Preconditions**

Before execution begins, the following preconditions shall be satisfied.

  -----------------------------------------------------------------------
  **Preconditions**        **Description**
  ------------------------ ----------------------------------------------
  Organization exists      Enterprise must belong to an existing
                           Organization

  User authenticated       Identity resolved through URA-001

  Authorization granted    Create Enterprise permission assigned

  Enterprise Context       Parent context identified where applicable
  resolved                 

  Metadata available       Required metadata successfully resolved

  Required reference data  Enterprise types, legal forms, jurisdictions
  available                and classifications resolved

  Business Activity        Business Activity exists in the Business
  registered               Activity Registry
  -----------------------------------------------------------------------

Failure of any mandatory precondition shall terminate execution before
Business Rule evaluation.

**A.5.4 Business Inputs**

The Business Activity consumes a canonical request.

Typical inputs include:

  -----------------------------------------------------------------------
  **Input**               **Description**
  ----------------------- -----------------------------------------------
  Organization Identifier Owning Organization

  Enterprise Name         Official enterprise name

  Enterprise Code         Business identifier

  Enterprise Type         Legal Entity, Business Unit, Site, Facility,
                          etc.

  Parent Enterprise       Optional parent node

  Legal Jurisdiction      Country / State

  Effective Date          Enterprise activation date

  Additional Metadata     Configurable enterprise attributes
  -----------------------------------------------------------------------

Input validation occurs before authorization and Business Rule
execution.

**A.5.5 Business Outputs**

Upon successful completion, the Business Activity shall produce:

  -----------------------------------------------------------------------
  **Output**                     **Description**
  ------------------------------ ----------------------------------------
  Enterprise Identifier          Newly created Enterprise Node

  Enterprise Version             Initial version

  Enterprise Context             Resolved execution context

  Business Activity Status       Completed

  Audit Identifier               Audit reference

  Domain Events                  Published events

  Correlation Identifier         Runtime traceability
  -----------------------------------------------------------------------

Outputs represent business outcomes rather than persistence results.

**A.5.6 Business Rules**

The Create Enterprise Business Activity shall enforce business rules
including, but not limited to:

1.  Enterprise Name shall be unique within the permitted scope.

2.  Enterprise Code shall be unique according to organizational policy.

3.  Parent Enterprise shall exist when specified.

4.  Circular enterprise hierarchies shall be prohibited.

5.  Enterprise Type shall be a valid metadata value.

6.  Effective Date shall satisfy organizational policy.

7.  Mandatory metadata shall be present.

8.  Enterprise relationships shall conform to ERG-001.

9.  Organization policies shall be satisfied before creation.

Business Rules shall be metadata-driven wherever configuration is
permitted.

**A.5.7 Business Postconditions**

Successful completion guarantees:

-   Enterprise Business Object created.

-   Enterprise registered within the Enterprise Relationship Graph.

-   Enterprise Context established.

-   Audit successfully recorded.

-   Domain Events published.

-   Transaction committed.

-   Runtime telemetry generated.

-   Business Activity completed successfully.

If any mandatory postcondition cannot be satisfied, the Business
Activity shall not be considered complete.

**A.5.8 Definition of Done**

The Business Activity shall be considered complete only when all of the
following have been satisfied:

-   Business validation completed.

-   Authorization approved.

-   Metadata resolved.

-   Enterprise Context established.

-   Business Rules satisfied.

-   Business Object persisted.

-   Transaction committed.

-   Domain Events published.

-   Audit recorded.

-   Observability telemetry generated.

-   Response successfully returned.

Partial completion shall not constitute successful execution.

**Architectural Note**

This BAC is intentionally **business-oriented** rather than
technology-oriented.

It contains **no references** to:

-   REST APIs

-   SQL

-   ORM frameworks

-   Programming languages

-   Message brokers

-   Cloud services

-   Databases

Those belong to the Technical Architecture.

The BAC remains a **technology-neutral constitutional contract**,
ensuring that every implementation---whether produced by human
developers or AI coding agents---begins from the same authoritative
business specification. I believe this separation is one of the
strongest aspects of the Aurex architecture because it keeps
business intent independent from implementation technology.

**A.6 Canonical Business Activity Manifest (CBAM) — Superseded, Retained for Historical Record**

*(CERT-014 correction: this Appendix defines a 20-section CBAM structure that is structurally different from, and unreconciled with, the 16-section structure at Section 6.29, "Enhanced Canonical Business Activity Manifest (CBAM v2)." Section 6.29 is the authoritative, current CBAM structure: it is body text registered in this document's own Table of Contents, and its own name ("CBAM v2") already identifies it as superseding the structure below. This Appendix is retained for historical record and is not the implementation contract; Section 6.29 is. No content from either structure has been merged or rewritten — this correction only resolves which one governs.)*

**A.6.1 Purpose**

The Canonical Business Activity Manifest (CBAM) is the machine-readable
implementation contract for every Business Activity within the Aurex
Intelligent Operating Center.

Where the Business Activity Contract (BAC) serves as the authoritative
specification for business stakeholders and architects, the CBAM serves
as the authoritative specification for engineering platforms,
AI-assisted development tools, automation pipelines, runtime
infrastructure, and implementation governance.

Every Business Activity shall possess exactly one CBAM.

The CBAM shall remain synchronized with the corresponding Business
Activity Contract throughout its lifecycle.

**A.6.2 Architectural Principle**

The BAC defines business intent.

The CBAM defines implementation intent.

Both describe the same Business Activity.

Neither may contradict the other.

The CBAM shall never introduce business behavior not defined within the
BAC.

**A.6.3 Objectives**

The CBAM enables:

-   deterministic code generation;

-   standardized Business Activity registration;

-   runtime discovery;

-   validation automation;

-   implementation consistency;

-   deployment automation;

-   documentation generation;

-   governance validation;

-   AI-assisted software engineering.

The CBAM shall be the single implementation contract consumed by Claude
Code and future AI engineering assistants.

**A.6.4 Canonical Manifest Structure**

Every CBAM shall contain the following sections.

  -----------------------------------------------------------------------
  **Section**                                          **Mandatory**
  ---------------------------------------------------- ------------------
  Manifest Metadata                                    ✓

  Business Activity Identity                           ✓

  Business Intent                                      ✓

  Business Object References                           ✓

  Business Rules                                       ✓

  Input Contract                                       ✓

  Output Contract                                      ✓

  Validation Rules                                     ✓

  Authorization Requirements                           ✓

  Enterprise Context Requirements                      ✓

  Metadata Dependencies                                ✓

  Workflow Integration                                 ✓

  Transaction Policy                                   ✓

  Execution Policy                                     ✓

  Domain Events                                        ✓

  Audit Requirements                                   ✓

  Observability Requirements                           ✓

  AI Assistance                                        Optional

  Test Requirements                                    ✓

  Version Information                                  ✓
  -----------------------------------------------------------------------

No mandatory section may be omitted.

**A.6.5 Reference CBAM**

The following illustrates the canonical structure for the **Create
Enterprise** Business Activity.

manifestVersion: \"1.0\"\
\
businessActivity:\
\
id: BA-ESRM-001\
\
name: Create Enterprise\
\
domain: Enterprise Structure & Relationship Management\
\
activityType: CREATE\
\
businessObject: Enterprise\
\
businessIntent: \>\
Create a new Enterprise within an Organization while preserving\
enterprise hierarchy integrity, governance, metadata compliance,\
authorization, auditability and event publication.\
\
inputContract:\
\
required:\
- organizationId\
- enterpriseName\
- enterpriseType\
- jurisdiction\
\
validation:\
\
metadataDriven: true\
\
authorization:\
\
permission:\
CREATE_ENTERPRISE\
\
enterpriseContext:\
\
required: true\
\
metadata:\
\
required: true\
\
transaction:\
\
policy: ATOMIC\
\
execution:\
\
policy: SYNCHRONOUS\
\
events:\
\
publishes:\
- EnterpriseCreated\
- EnterpriseHierarchyUpdated\
\
audit:\
\
enabled: true\
\
observability:\
\
telemetry: STANDARD\
\
tests:\
\
required: true

The actual implementation technology may represent the CBAM in YAML,
JSON, XML, or another governed serialization format.

Its logical structure shall remain canonical.

**A.6.6 Manifest Ownership**

The CBAM shall be owned by the Business Domain responsible for the
Business Activity.

Ownership includes:

-   creation;

-   version management;

-   governance approval;

-   lifecycle management;

-   retirement.

Only approved manifests may be consumed by runtime infrastructure or
AI-assisted engineering tools.

**A.6.7 Manifest Validation**

Before implementation begins, every CBAM shall be validated for:

-   structural completeness;

-   schema compliance;

-   BAC consistency;

-   Business Object existence;

-   Metadata dependency validity;

-   Authorization dependency validity;

-   Event registration;

-   Workflow references;

-   Transaction policy validity.

An invalid CBAM shall prevent implementation.

**A.6.8 Manifest Versioning**

The CBAM shall be versioned independently from implementation code.

Every version shall preserve:

-   backward compatibility where applicable;

-   traceability to the corresponding BAC;

-   implementation history;

-   governance approvals;

-   effective dates.

Implementation artifacts shall reference the CBAM version used during
generation.

**A.6.9 Runtime Usage**

The Runtime Execution Architecture may consume the CBAM to support:

-   Business Activity discovery;

-   registration;

-   dependency resolution;

-   validation;

-   observability;

-   documentation;

-   runtime diagnostics.

The CBAM is descriptive rather than executable.

Runtime Components shall not derive business behavior solely from the
CBAM.

**A.6.10 AI-Assisted Engineering**

Claude Code and future AI-assisted engineering platforms shall consume
the CBAM as the primary implementation specification.

The CBAM provides sufficient information to generate:

-   Business Activity skeletons;

-   validation components;

-   authorization hooks;

-   transaction boundaries;

-   event publication logic;

-   audit integration;

-   observability instrumentation;

-   test scaffolding;

-   documentation.

AI-generated implementations shall remain faithful to the Business
Activity Contract and shall not infer additional business behavior
beyond the governed specifications.

**A.6.11 Architectural Guarantees**

The Canonical Business Activity Manifest guarantees:

-   a single machine-readable implementation contract;

-   deterministic Business Activity generation;

-   consistent runtime registration;

-   governance-aligned implementation;

-   traceability between business architecture and implementation;

-   technology-independent implementation specifications;

-   standardized AI-assisted software generation.

Every Business Activity within the Aurex Intelligent Operating
Center shall possess a governed Canonical Business Activity Manifest,
ensuring that implementation remains consistent, automatable, auditable,
and fully aligned with the constitutional principles established
throughout IMP-001.

**A.7 Canonical Business Activity Context (BACX)**

**A.7.1 Purpose**

The Canonical Business Activity Context (BACX) defines the complete
execution context supplied to every Business Activity within the
Aurex Intelligent Operating Center.

The BACX represents the runtime realization of the Business Activity
Contract and serves as the single source of execution context throughout
the lifecycle of a Business Activity.

Rather than independently resolving authorization, metadata, enterprise
context, workflow information, transaction state, or runtime policies,
Business Activities shall receive a fully constructed BACX from the
Business Activity Engine.

Business Activities consume context.

They do not construct it.

**A.7.2 Architectural Principle**

Every Business Activity shall execute using exactly one Business
Activity Context.

The Business Activity Context encapsulates all runtime information
required for execution.

Business Activities shall not retrieve runtime dependencies directly
from platform services.

Instead, all required execution context shall be resolved before
Business Rule execution and supplied through the BACX.

This ensures:

-   deterministic execution;

-   implementation consistency;

-   simplified testing;

-   runtime observability;

-   loose coupling between Business Activities and platform services.

**A.7.3 Context Ownership**

The BACX shall be constructed exclusively by the Business Activity
Engine.

Business Activities shall treat the BACX as immutable.

No Business Activity shall modify the BACX during execution.

Changes to execution context require the creation of a new Business
Activity.

**A.7.4 Canonical Context Structure**

Every BACX shall contain the following logical sections.

  -----------------------------------------------------------------------
  **Section**                                        **Mandatory**
  -------------------------------------------------- --------------------
  Request Context                                    ✓

  Business Activity Information                      ✓

  Organization Context                               ✓

  Enterprise Context                                 ✓

  Authorization Context                              ✓

  Metadata Context                                   ✓

  Workflow Context                                   ✓

  Transaction Context                                ✓

  Execution Policies                                 ✓

  Observability Context                              ✓

  AI Context                                         Optional

  Runtime Extensions                                 Optional
  -----------------------------------------------------------------------

The logical structure shall remain consistent across all Business
Activities regardless of implementation technology.

**A.7.5 Reference BACX Structure**

The following illustrates the canonical structure for the **Create
Enterprise** Business Activity.

request:\
\
requestId:\
correlationId:\
timestamp:\
locale:\
timezone:\
\
businessActivity:\
\
activityId:\
activityName:\
activityVersion:\
\
organization:\
\
organizationId:\
\
enterprise:\
\
enterpriseNode:\
enterpriseView:\
hierarchy:\
reportingScope:\
\
authorization:\
\
identityId:\
membershipId:\
roles:\
permissions:\
assignments:\
delegations:\
\
metadata:\
\
configuration:\
businessRules:\
referenceData:\
executionPolicies:\
\
workflow:\
\
workflowId:\
currentStage:\
approvalContext:\
\
transaction:\
\
transactionId:\
isolationPolicy:\
compensationPolicy:\
\
execution:\
\
executionMode:\
retryPolicy:\
idempotencyKey:\
\
observability:\
\
traceId:\
telemetryContext:\
\
ai:\
\
enabled:\
confidenceThreshold:

This represents the logical contract.

Implementation technologies may serialize the context differently.

**A.7.6 Context Resolution Lifecycle**

The Business Activity Engine shall construct the BACX using the
following sequence.

Incoming Request\
│\
Identity Resolution\
│\
Authorization Resolution\
│\
Enterprise Context Resolution\
│\
Metadata Resolution\
│\
Workflow Resolution\
│\
Transaction Creation\
│\
Execution Policy Resolution\
│\
Business Activity Context (BACX)\
│\
Business Activity Execution

Business Rule execution shall begin only after successful completion of
context construction.

**A.7.7 Context Immutability**

Once created, the BACX shall remain immutable throughout Business
Activity execution.

Immutability guarantees:

-   reproducible execution;

-   deterministic testing;

-   audit integrity;

-   traceability;

-   replay support;

-   simplified debugging.

If execution requires additional context, a subsequent Business Activity
shall be initiated with a newly constructed BACX.

**A.7.8 Runtime Collaboration**

The Business Activity Engine assembles the BACX by collaborating with
platform capabilities including:

-   Authorization Framework

-   Enterprise Relationship Engine

-   Metadata Framework

-   Workflow Engine

-   Transaction Manager

-   Observability Platform

-   AI Runtime (where applicable)

Business Activities remain unaware of these collaborations.

They interact exclusively with the BACX.

**A.7.9 Testing Benefits**

The BACX enables deterministic testing because all external runtime
dependencies are encapsulated within a single object.

Testing frameworks may construct synthetic BACX instances to simulate:

-   authorization scenarios;

-   enterprise structures;

-   metadata configurations;

-   workflow states;

-   transaction policies;

-   AI-enabled and AI-disabled execution paths.

This significantly reduces the complexity of Business Activity testing.

**A.7.10 Architectural Guarantees**

The Canonical Business Activity Context guarantees:

-   a single execution contract for every Business Activity;

-   deterministic runtime behavior;

-   separation between platform infrastructure and business logic;

-   immutable execution context;

-   simplified testing and debugging;

-   technology-independent execution semantics;

-   complete traceability and observability.

Every Business Activity executed within the Aurex Intelligent
Operating Center shall receive a fully resolved and immutable Business
Activity Context from the Business Activity Engine, ensuring consistent,
governed, and reproducible execution independent of implementation
technology or deployment environment.

**Architectural Observation (One Improvement)**

I would make **BACX** a **first-class architectural artifact**,
alongside:

-   **BAC** (Business Contract)

-   **CBAM** (Machine-readable Contract)

-   **BACX** (Runtime Execution Contract)

Together they form a complete trilogy:

-   **BAC** defines **what** the Business Activity must accomplish.

-   **CBAM** defines **how** the Business Activity is described to
    engineering and AI tooling.

-   **BACX** defines **what the Business Activity receives at runtime**.

I believe this separation is elegant, easy to understand, and highly
scalable. It creates a clear boundary between business specification,
implementation specification, and runtime execution without introducing
unnecessary complexity. This is the kind of pattern that can remain
stable for many years as the Aurex platform evolves.

**A.8 Canonical Runtime Execution Pipeline**

**A.8.1 Purpose**

The Canonical Runtime Execution Pipeline defines the normative execution
sequence for every Business Activity within the Aurex Intelligent
Operating Center.

It demonstrates how the Business Activity Engine transforms a Business
Activity Contract (BAC), Canonical Business Activity Manifest (CBAM),
and Business Activity Context (BACX) into a governed business outcome.

The Runtime Execution Pipeline is the implementation realization of the
Business Activity Lifecycle defined in IMP-001.

Every Business Activity shall execute using this pipeline unless an
approved architectural exception exists.

**A.8.2 Architectural Principle**

Business Activities execute through a standardized runtime pipeline.

The pipeline is owned by the Business Activity Engine.

Business Activities contribute only business-specific logic.

The Business Activity Engine coordinates:

-   validation;

-   authorization;

-   metadata resolution;

-   Enterprise Context;

-   workflow coordination;

-   transaction management;

-   event publication;

-   audit recording;

-   observability.

This separation ensures that Business Activities remain focused
exclusively on business behavior.

**A.8.3 Canonical Execution Flow**

Every Business Activity shall execute using the following runtime
sequence.

Client Request\
│\
Business Activity Resolution\
│\
BAC Validation\
│\
CBAM Resolution\
│\
BACX Construction\
│\
Business Validation\
│\
Authorization Evaluation\
│\
Metadata Resolution\
│\
Enterprise Context Resolution\
│\
Workflow Evaluation\
│\
Transaction Creation\
│\
Business Rule Execution\
│\
Business Object Changes\
│\
Transaction Commit\
│\
Domain Event Publication\
│\
Audit Recording\
│\
Telemetry Publication\
│\
Business Response

No Business Activity shall alter this execution order without explicit
architectural approval.

**A.8.4 Phase 1 --- Activity Resolution**

The Business Activity Engine shall identify the Business Activity using
the incoming request.

Resolution shall determine:

-   Business Activity Identifier

-   Business Domain

-   Activity Version

-   Business Object

-   Activity Type

The Business Activity Registry shall be the authoritative source for
Activity discovery.

**A.8.5 Phase 2 --- Contract Resolution**

The Business Activity Engine shall retrieve:

-   Business Activity Contract (BAC)

-   Canonical Business Activity Manifest (CBAM)

These contracts determine the execution characteristics of the Business
Activity.

The implementation shall not infer execution behavior outside these
governed specifications.

**A.8.6 Phase 3 --- Context Construction**

The Business Activity Engine shall construct the Business Activity
Context (BACX).

Construction includes:

-   Request Context

-   Authorization Context

-   Enterprise Context

-   Metadata Context

-   Workflow Context

-   Transaction Context

-   Execution Policies

-   Observability Context

Business Activity execution shall not begin until BACX construction has
completed successfully.

**A.8.7 Phase 4 --- Validation**

Validation occurs before any business state is modified.

Validation shall include:

-   Input validation

-   Mandatory field validation

-   Data type validation

-   Business preconditions

-   Metadata validation

-   Reference data validation

Validation failures terminate execution without creating side effects.

**A.8.8 Phase 5 --- Authorization**

Authorization shall be evaluated using the Authorization Framework
defined in URA-001.

Evaluation may include:

-   Identity

-   Membership

-   Roles

-   Permissions

-   Assignments

-   Delegations

-   Approval Authority

-   Enterprise Scope

Business Activities shall consume the authorization decision.

They shall not implement authorization logic.

**A.8.9 Phase 6 --- Runtime Resolution**

Before Business Rule execution, the Business Activity Engine shall
resolve all runtime dependencies.

These include:

-   Metadata

-   Enterprise Context

-   Workflow Context

-   Execution Policies

-   Transaction Policy

-   AI Policy

Business Rules shall execute against fully resolved runtime information.

**A.8.10 Phase 7 --- Business Rule Execution**

This is the only phase owned by the Business Activity implementation.

Typical responsibilities include:

-   evaluating business rules;

-   updating Business Objects;

-   coordinating aggregates;

-   invoking domain services;

-   creating business outcomes.

Business Activities shall not perform infrastructure responsibilities
during this phase.

**A.8.11 Phase 8 --- Transaction Commit**

Upon successful Business Rule execution:

-   Business Objects shall be persisted.

-   Transaction consistency shall be verified.

-   Commit shall complete before any downstream notification.

Business outcomes become authoritative only after successful transaction
commitment.

**A.8.12 Phase 9 --- Post-Commit Activities**

Following successful commitment, the Business Activity Engine shall
coordinate:

-   Domain Event publication

-   Audit recording

-   Workflow progression

-   Knowledge Graph synchronization requests

-   Notification requests

-   Integration Events

-   Telemetry publication

These activities shall not modify committed Business Objects.

**A.8.13 Phase 10 --- Response Construction**

The Business Activity Engine shall construct the Business Response.

The response shall include:

-   Activity Status

-   Business Result

-   Correlation Identifier

-   Version Information

-   Audit Reference (where appropriate)

-   Warnings (if applicable)

Implementation details shall not be exposed.

Responses communicate business outcomes.

**A.8.14 Failure Handling**

Failures shall terminate execution at the earliest safe point.

Recovery behavior shall follow the Failure & Recovery policies defined
elsewhere in IMP-001.

Partial execution shall not result in inconsistent Business Objects.

**A.8.15 Architectural Guarantees**

The Canonical Runtime Execution Pipeline guarantees:

-   a single execution model for all Business Activities;

-   deterministic execution sequencing;

-   centralized governance;

-   separation of business logic from platform concerns;

-   consistent transaction management;

-   post-commit event publication;

-   complete auditability and observability;

-   technology-independent runtime execution.

Every Business Activity executed within the Aurex Intelligent
Operating Center shall follow the Canonical Runtime Execution Pipeline,
ensuring that business execution remains consistent, governed,
predictable, and fully aligned with the constitutional principles
established throughout IMP-001.

**Architect\'s Review**

I believe this section completes the conceptual bridge between
**specification** and **implementation**.

We now have four complementary artifacts:

-   **BAC** → Defines **what** the Business Activity must achieve.

-   **CBAM** → Defines **how** the Business Activity is described to
    engineering tools and AI.

-   **BACX** → Defines **the complete runtime context** supplied to the
    Business Activity.

-   **Runtime Execution Pipeline** → Defines **how** the Business
    Activity is executed by the Business Activity Engine.

This progression is intentional and complete. From this point onward
(Validation Rules, Authorization, Metadata Resolution, Transaction
Execution, etc.), we are no longer introducing new architectural
concepts---we are instantiating these four foundational artifacts for
the **Create Enterprise** reference implementation. That makes the
remainder of the appendix more concrete and implementation-focused while
avoiding duplication of the constitutional sections already defined in
IMP-001. I believe this is the correct transition point.

**A.9 Canonical Reference Implementation Walkthrough**

**A.9.1 Purpose**

This section demonstrates the end-to-end implementation of the **Create
Enterprise** Business Activity using the architectural principles
defined throughout IMP-001.

Rather than introducing new architectural concepts, this walkthrough
illustrates how the Business Activity Engine coordinates the Business
Activity Contract (BAC), Canonical Business Activity Manifest (CBAM),
Business Activity Context (BACX), and Runtime Execution Pipeline to
realize a complete business operation.

The walkthrough is normative and serves as the reference implementation
pattern for all future Business Activities.

**A.9.2 Implementation Overview**

The **Create Enterprise** Business Activity follows the canonical
execution sequence illustrated below.

Client Request\
│\
Resolve Business Activity\
│\
Load BAC + CBAM\
│\
Construct BACX\
│\
Validate Request\
│\
Authorize Request\
│\
Resolve Metadata\
│\
Resolve Enterprise Context\
│\
Begin Transaction\
│\
Execute Business Rules\
│\
Persist Enterprise Aggregate\
│\
Commit Transaction\
│\
Publish Domain Events\
│\
Record Audit\
│\
Publish Telemetry\
│\
Return Response

This sequence is identical for every Business Activity executed by the
Business Activity Engine.

Only the business-specific rules vary.

**A.9.3 Step 1 --- Client Request**

The client submits a request to create a new Enterprise.

Example request information may include:

  -----------------------------------------------------------------------
  **Input**                  **Example**
  -------------------------- --------------------------------------------
  Organization               Aurex Demo Organization

  Enterprise Name            India Manufacturing Division

  Enterprise Type            Business Unit

  Parent Enterprise          Global Manufacturing

  Jurisdiction               India

  Effective Date             01-Apr-2027
  -----------------------------------------------------------------------

At this stage, no Business Objects have been modified.

**A.9.4 Step 2 --- Business Activity Resolution**

The Business Activity Engine determines that the request maps to:

  -----------------------------------------------------------------------
  **Property**                   **Value**
  ------------------------------ ----------------------------------------
  Activity                       Create Enterprise

  Domain                         ESRM

  Business Object                Enterprise

  Activity Type                  Create

  Version                        Current Active Version
  -----------------------------------------------------------------------

The Activity Registry returns the corresponding BAC and CBAM.

**A.9.5 Step 3 --- Context Construction**

The Business Activity Engine constructs the BACX by gathering:

-   authenticated user identity;

-   Organization membership;

-   Enterprise Context;

-   resolved metadata;

-   execution policies;

-   workflow context;

-   transaction policy;

-   observability identifiers.

The Business Activity implementation receives **one immutable BACX**.

It performs no additional infrastructure lookups.

**A.9.6 Step 4 --- Business Validation**

The Business Activity validates:

-   mandatory inputs;

-   Enterprise Name uniqueness;

-   Enterprise Code uniqueness;

-   Parent Enterprise existence;

-   Enterprise Type validity;

-   Organization ownership;

-   metadata completeness.

Any validation failure terminates execution before the transaction
begins.

**A.9.7 Step 5 --- Authorization**

The Business Activity requests an authorization decision from the
Authorization Framework.

Typical evaluation includes:

-   Identity

-   Membership

-   Role

-   Permission

-   Assignment

-   Enterprise Scope

The Business Activity receives only the authorization result.

It does not evaluate authorization rules itself.

**A.9.8 Step 6 --- Metadata & Enterprise Resolution**

Before Business Rule execution, the Business Activity Engine resolves:

-   Enterprise Types;

-   Jurisdictions;

-   Legal Entity classifications;

-   Naming policies;

-   Organization policies;

-   Enterprise hierarchy;

-   Reporting scope.

Business logic executes using resolved metadata rather than querying
repositories directly.

**A.9.9 Step 7 --- Business Execution**

The Business Activity now performs only domain-specific logic.

Typical operations include:

-   creating the Enterprise Aggregate;

-   assigning initial status;

-   establishing parent-child relationships;

-   initializing governance attributes;

-   preparing audit information.

No infrastructure concerns are implemented within this step.

**A.9.10 Step 8 --- Transaction Completion**

The Business Activity Engine:

-   persists the Enterprise Aggregate;

-   verifies transactional consistency;

-   commits the transaction.

The Enterprise Business Object becomes authoritative only after
successful commitment.

**A.9.11 Step 9 --- Post-Commit Processing**

Following transaction commitment, the Business Activity Engine
coordinates:

-   publication of EnterpriseCreated;

-   publication of EnterpriseHierarchyUpdated;

-   audit recording;

-   workflow initiation (if applicable);

-   Knowledge Graph synchronization request;

-   telemetry publication.

These operations observe the committed business state and do not modify
it.

**A.9.12 Step 10 --- Response**

The Business Activity Engine constructs the response.

Typical response elements include:

  -----------------------------------------------------------------------
  **Output**                    **Description**
  ----------------------------- -----------------------------------------
  Enterprise Identifier         Newly created Enterprise

  Activity Status               Completed

  Correlation Identifier        Traceability

  Version                       Initial Business Object Version

  Audit Reference               Audit Record Identifier
  -----------------------------------------------------------------------

The response communicates the business outcome without exposing
implementation details.

**A.9.13 Implementation Summary**

This walkthrough demonstrates that a Business Activity implementation is
intentionally small.

The Business Activity implementation focuses exclusively on business
behavior.

All cross-cutting concerns---including authorization, metadata
resolution, Enterprise Context construction, transaction coordination,
event publication, auditing, and observability---are provided by the
Business Activity Engine.

This separation of responsibilities is the defining implementation
principle of the Aurex Intelligent Operating Center and shall be
preserved across all Business Activities.

**Architect\'s Recommendation**

From this point, I recommend the remaining appendix be concise and
practical:

-   **A.10** --- Reference Folder Structure

-   **A.11** --- Reference Source Code Organization

-   **A.12** --- Claude Code Generation Example

-   **A.13** --- Reference Test Suite

-   **A.14** --- Implementation Readiness Checklist

-   **A.15** --- Appendix Summary

This avoids repeating concepts already covered in IMP-001 while giving
developers and AI coding agents exactly what they need to start
building. I think this is a stronger and cleaner ending than expanding
into many more architecture-heavy sections.

**A.10 Canonical Business Activity Project Structure**

**A.10.1 Purpose**

This section defines the canonical project organization for implementing
Business Activities within the Aurex Intelligent Operating Center.

The objective is to ensure that every Business Activity is implemented
using a consistent, discoverable, maintainable, and
technology-independent structure.

A standardized project structure improves:

-   implementation consistency;

-   code discoverability;

-   maintainability;

-   automated code generation;

-   testing;

-   documentation;

-   onboarding;

-   architectural governance.

All Business Activities shall conform to this structure unless an
approved architectural exception exists.

**A.10.2 Architectural Principle**

Project structure shall reflect business architecture.

Implementation shall be organized around Business Activities and
Business Objects rather than technical layers.

The project organization shall make business intent immediately
recognizable.

**A.10.3 Canonical Structure**

Every Business Activity implementation shall contain the following
logical components.

Business Activity\
│\
├── Contract\
├── Manifest\
├── Activity\
├── Validation\
├── Authorization\
├── Business Rules\
├── Domain Services\
├── Events\
├── Workflow\
├── Audit\
├── Tests\
└── Documentation

The physical realization may differ by programming language, but the
logical organization shall remain consistent.

**A.10.4 Reference Project Organization**

The following illustrates the canonical organization for the **Create
Enterprise** Business Activity.

enterprise/\
\
create-enterprise/\
\
business-activity.yaml\
\
contract/\
\
create-enterprise-bac.yaml\
\
manifest/\
\
create-enterprise-cbam.yaml\
\
activity/\
\
create_enterprise_activity.\*\
\
validation/\
\
create_enterprise_validator.\*\
\
business-rules/\
\
enterprise_creation_rules.\*\
\
services/\
\
enterprise_domain_service.\*\
\
workflow/\
\
create_enterprise_workflow.\*\
\
events/\
\
enterprise_created_event.\*\
\
enterprise_hierarchy_updated_event.\*\
\
audit/\
\
create_enterprise_audit.\*\
\
tests/\
\
unit/\
\
integration/\
\
authorization/\
\
idempotency/\
\
performance/\
\
docs/\
\
implementation.md

The extension (\*) is implementation-specific (Python, Java, C#, Go,
etc.).

**A.10.5 Component Responsibilities**

Each project component has a single responsibility.

  -----------------------------------------------------------------------
  **Component**     **Responsibility**
  ----------------- -----------------------------------------------------
  Contract          Business Activity Contract (BAC)

  Manifest          Canonical Business Activity Manifest (CBAM)

  Activity          Business Activity implementation

  Validation        Input and business validation

  Business Rules    Domain-specific rules

  Services          Domain orchestration and reusable domain logic

  Workflow          Workflow coordination hooks

  Events            Domain Event definitions

  Audit             Audit enrichment and recording support

  Tests             Automated verification

  Documentation     Activity-specific implementation guidance
  -----------------------------------------------------------------------

Each component shall remain cohesive and independently maintainable.

**A.10.6 Dependency Rules**

Dependencies shall follow the canonical implementation direction.

Activity\
│\
├── Validation\
├── Business Rules\
├── Domain Services\
├── Workflow\
├── Events\
└── Audit

The following dependencies are prohibited:

-   Validation invoking Activity

-   Events invoking Business Rules

-   Workflow modifying Business Objects directly

-   Tests acting as production dependencies

-   Documentation referenced by runtime code

Circular dependencies shall not exist.

**A.10.7 Naming Conventions**

Business Activity artifacts shall use consistent business-oriented
naming.

Examples include:

-   create_enterprise_activity

-   approve_evidence_activity

-   publish_report_activity

-   assign_metric_owner_activity

Technical names such as:

-   controller

-   service_impl

-   crud_service

-   entity_manager

shall not be used to identify Business Activities.

Business terminology shall always take precedence.

**A.10.8 Generated Artifacts**

For every approved Business Activity, Claude Code (or another AI
engineering platform) should generate the following minimum artifacts:

-   Business Activity implementation

-   BAC reference

-   CBAM reference

-   Validator

-   Domain Rule module

-   Event definitions

-   Unit tests

-   Integration tests

-   Authorization tests

-   Performance tests

-   Documentation

Generation shall be deterministic and repeatable.

**A.10.9 Architectural Guarantees**

The Canonical Business Activity Project Structure guarantees:

-   consistent project organization;

-   clear separation of responsibilities;

-   business-oriented implementation;

-   simplified navigation;

-   deterministic AI-assisted code generation;

-   maintainable codebases;

-   technology-independent implementation organization.

Every Business Activity implemented within the Aurex Intelligent
Operating Center shall conform to the Canonical Business Activity
Project Structure, ensuring that all implementations remain
architecturally consistent, discoverable, maintainable, and aligned with
the business-first principles established throughout IMP-001.

**Architect\'s Observation (One Suggestion)**

I think this section should be **the only place in IMP-001 that talks
about source code organization**. All earlier sections should remain
technology-neutral and implementation-independent.

By keeping project structure here, we maintain a clean separation:

-   **Sections 1--7** → Constitutional architecture.

-   **Appendix A (A.1--A.9)** → Canonical implementation model.

-   **A.10 onward** → Practical engineering guidance.

That keeps IMP-001 cohesive while giving developers and AI coding agents
a clear, standardized implementation target. I believe this is the right
balance between architectural purity and engineering pragmatism.

**A.11 Canonical AI Code Generation Contract (AICGC)**

**A.11.1 Purpose**

The Canonical AI Code Generation Contract (AICGC) defines the mandatory
engineering contract governing AI-assisted generation of Business
Activities within the Aurex Intelligent Operating Center.

The objective of the AICGC is to ensure that every AI-generated
implementation conforms to the constitutional architecture established
by:

-   Blueprint

-   SD-001

-   SD-002

-   SD-003

-   URA-001

-   ERG-001

-   CMD-001

-   IMP-001

The AICGC establishes a deterministic interface between architectural
specifications and AI-assisted software engineering.

It is independent of any specific AI model or coding platform.

**A.11.2 Architectural Principle**

AI generates implementations.

Architecture governs implementations.

AI shall never invent architecture.

AI shall implement only the behavior explicitly defined by the
constitutional documents.

Where ambiguity exists, AI shall request clarification rather than infer
business behavior.

**A.11.3 AI Input Contract**

Every AI-assisted code generation request shall receive the following
mandatory inputs.

  -----------------------------------------------------------------------
  **Input**                                       **Source**
  ----------------------------------------------- -----------------------
  Business Activity Contract (BAC)                IMP-001

  Canonical Business Activity Manifest (CBAM)     IMP-001

  Business Activity Context (BACX)                IMP-001

  Business Object Definition                      SD-002

  Metadata Definitions                            CMD-001

  Enterprise Context                              ERG-001

  Authorization Model                             URA-001

  Business Activity Policies                      IMP-001

  Coding Standards                                Technical Architecture
  -----------------------------------------------------------------------

No implementation shall be generated without these governed inputs.

**A.11.4 AI Output Contract**

Every generated Business Activity shall include, at minimum:

  -----------------------------------------------------------------------
  **Artifact**                                         **Mandatory**
  ---------------------------------------------------- ------------------
  Business Activity implementation                     ✓

  Aggregate updates                                    ✓

  Validators                                           ✓

  Domain services                                      ✓

  Repository interfaces                                ✓

  Domain Events                                        ✓

  Unit tests                                           ✓

  Integration tests                                    ✓

  Authorization tests                                  ✓

  Performance tests                                    ✓

  API specification updates                            ✓

  Documentation                                        ✓
  -----------------------------------------------------------------------

Generated artifacts shall remain synchronized with the CBAM.

**A.11.5 Mandatory Generation Rules**

AI-generated implementations shall:

-   implement exactly one Business Activity;

-   follow the Business Activity Engine execution pipeline;

-   preserve Business Activity boundaries;

-   use Business Objects defined in SD-002;

-   consume metadata from CMD-001;

-   consume Enterprise Context from ERG-001;

-   consume authorization decisions from URA-001;

-   publish Domain Events after successful transaction commitment;

-   record audit information;

-   generate observability instrumentation;

-   generate automated tests.

No additional architectural behavior shall be introduced.

**A.11.6 Prohibited Behaviors**

AI-assisted implementations shall never:

-   bypass the Business Activity Engine;

-   embed authorization logic;

-   hardcode metadata;

-   hardcode workflow logic;

-   publish Domain Events before transaction commitment;

-   access infrastructure directly from Business Rules;

-   modify Enterprise Context directly;

-   implement CRUD operations as Business Activities;

-   create undocumented Business Objects;

-   invent business rules.

Any generated implementation violating these principles shall be
considered architecturally non-compliant.

**A.11.7 Generation Validation**

Every generated implementation shall be validated against the following
criteria.

  -----------------------------------------------------------------------
  **Validation**                                          **Required**
  ------------------------------------------------------- ---------------
  BAC compliance                                          ✓

  CBAM compliance                                         ✓

  SD-002 compliance                                       ✓

  URA-001 compliance                                      ✓

  ERG-001 compliance                                      ✓

  CMD-001 compliance                                      ✓

  IMP-001 compliance                                      ✓

  Architectural dependency validation                     ✓

  Test completeness                                       ✓
  -----------------------------------------------------------------------

Only compliant implementations may proceed to engineering review.

**A.11.8 Human Review**

AI-assisted generation does not eliminate engineering responsibility.

Every generated implementation shall undergo:

-   architectural review;

-   engineering review;

-   security review;

-   testing review;

-   business validation.

Approval remains the responsibility of authorized human reviewers.

**A.11.9 Extensibility**

The AICGC is AI-platform independent.

It shall support integration with:

-   Claude Code

-   OpenAI Codex

-   GitHub Copilot

-   Cursor

-   Windsurf

-   Gemini Code Assist

-   future enterprise AI engineering platforms

The governing contract shall remain unchanged.

Only adapter prompts may vary.

**A.11.10 Architectural Guarantees**

The Canonical AI Code Generation Contract guarantees:

-   deterministic AI-assisted implementation;

-   architectural compliance;

-   technology independence;

-   consistent Business Activity realization;

-   reproducible code generation;

-   governed human oversight;

-   complete traceability between architecture and implementation.

Every AI-assisted implementation within the Aurex Intelligent
Operating Center shall conform to the Canonical AI Code Generation
Contract, ensuring that generated software faithfully realizes the
constitutional architecture without introducing unintended business
behavior, architectural inconsistencies, or technology-specific
assumptions.

**Architect\'s Recommendation**

I believe this is stronger than a \"Claude Code Prompt Template.\"

A constitutional document should **never bind the platform to a single
AI vendor**. By defining a **Canonical AI Code Generation Contract**,
IMP-001 remains relevant regardless of which AI engineering platform the
organization adopts in the future.

Then, outside IMP-001, you can maintain separate, versioned prompt
libraries such as:

-   prompts/claude-code/

-   prompts/openai-codex/

-   prompts/github-copilot/

-   prompts/cursor/

Those become implementation assets, while **IMP-001 remains the enduring
architectural standard**. I believe this separation is much more robust
for a platform intended to evolve over many years.

**A.12 Engineering Readiness Standard (ERS)**

**A.12.1 Purpose**

The Engineering Readiness Standard (ERS) defines the mandatory readiness
criteria that shall be satisfied before a Business Activity proceeds
through implementation, testing, deployment, and production release
within the Aurex Intelligent Operating Center.

The objective of the ERS is to ensure that every Business Activity is:

-   architecturally complete;

-   business validated;

-   implementation ready;

-   testable;

-   observable;

-   secure;

-   deployable;

-   maintainable.

No Business Activity shall advance to the next engineering stage until
the applicable readiness criteria have been satisfied.

**A.12.2 Architectural Principle**

Engineering quality shall be verified before implementation progresses.

Readiness shall be evaluated using objective criteria rather than
subjective judgment.

Every Business Activity shall demonstrate constitutional compliance
before code enters production.

**A.12.3 Readiness Lifecycle**

The Engineering Readiness Standard defines five sequential readiness
gates.

Business Specification\
│\
──────────────\
ERS-1\
Architecture Ready\
──────────────\
│\
──────────────\
ERS-2\
Implementation Ready\
──────────────\
│\
──────────────\
ERS-3\
Verification Ready\
──────────────\
│\
──────────────\
ERS-4\
Deployment Ready\
──────────────\
│\
──────────────\
ERS-5\
Production Ready

Each gate shall be completed before progressing to the next.

**A.12.4 ERS-1 --- Architecture Ready**

The following criteria shall be satisfied before implementation begins.

  --------------------------------------------------------------------------
  **Requirement**                                            **Mandatory**
  ---------------------------------------------------------- ---------------
  Business Activity Contract (BAC) approved                  ✓

  Canonical Business Activity Manifest (CBAM) approved       ✓

  Business Object defined in SD-002                          ✓

  Metadata defined in CMD-001                                ✓

  Authorization requirements identified                      ✓

  Enterprise Context identified                              ✓

  Business Rules documented                                  ✓

  Activity Type identified                                   ✓

  Architectural review completed                             ✓
  --------------------------------------------------------------------------

Failure of any mandatory criterion prevents implementation.

**A.12.5 ERS-2 --- Implementation Ready**

Before development begins, the implementation team shall confirm:

  -----------------------------------------------------------------------
  **Requirement**                                       **Mandatory**
  ----------------------------------------------------- -----------------
  Project structure established                         ✓

  Source repository created                             ✓

  Coding standards identified                           ✓

  Generated artifacts reviewed                          ✓

  Event definitions completed                           ✓

  Transaction policy defined                            ✓

  Error handling defined                                ✓

  Observability requirements defined                    ✓
  -----------------------------------------------------------------------

AI-generated implementations shall also satisfy these requirements.

**A.12.6 ERS-3 --- Verification Ready**

Before release candidate creation, verification shall confirm:

  -----------------------------------------------------------------------
  **Requirement**                                    **Mandatory**
  -------------------------------------------------- --------------------
  Unit tests complete                                ✓

  Integration tests complete                         ✓

  Authorization tests complete                       ✓

  Performance tests complete                         ✓

  Idempotency verified                               ✓

  Concurrency validated                              ✓

  Event publication validated                        ✓

  Audit verification completed                       ✓

  Static analysis completed                          ✓
  -----------------------------------------------------------------------

Testing shall validate business behavior rather than implementation
details.

**A.12.7 ERS-4 --- Deployment Ready**

Prior to deployment, the following shall be verified.

  -----------------------------------------------------------------------
  **Requirement**                                      **Mandatory**
  ---------------------------------------------------- ------------------
  Configuration validated                              ✓

  Environment variables verified                       ✓

  Secrets configured                                   ✓

  Migration scripts validated                          ✓

  Rollback strategy approved                           ✓

  Monitoring configured                                ✓

  Alerting configured                                  ✓

  Deployment approval completed                        ✓
  -----------------------------------------------------------------------

Deployment readiness shall be environment-specific.

**A.12.8 ERS-5 --- Production Ready**

Before production activation, the following shall be confirmed.

  -----------------------------------------------------------------------
  **Requirement**                                       **Mandatory**
  ----------------------------------------------------- -----------------
  Business approval received                            ✓

  Security approval completed                           ✓

  Architecture compliance confirmed                     ✓

  Performance targets achieved                          ✓

  Operational runbooks available                        ✓

  Support ownership assigned                            ✓

  Production monitoring active                          ✓

  Release authorization granted                         ✓
  -----------------------------------------------------------------------

Production deployment shall not occur without completion of all
mandatory criteria.

**A.12.9 Compliance Verification**

Every Business Activity shall demonstrate compliance with the
constitutional architecture.

Verification shall include alignment with:

-   Blueprint

-   SD-001

-   SD-002

-   SD-003

-   URA-001

-   ERG-001

-   CMD-001

-   IMP-001

Compliance evidence shall be retained as part of the engineering audit
trail.

**A.12.10 AI-Assisted Engineering Readiness**

Where AI-assisted development is used, additional verification shall
confirm:

-   AI input specifications are complete.

-   Generated artifacts match the approved CBAM.

-   No prohibited implementation patterns exist.

-   Human engineering review has been completed.

-   Generated tests adequately cover business scenarios.

-   AI-generated documentation has been reviewed for accuracy.

AI assistance does not replace engineering accountability.

**A.12.11 Architectural Guarantees**

The Engineering Readiness Standard guarantees:

-   objective implementation readiness;

-   constitutional compliance;

-   consistent engineering quality;

-   comprehensive verification;

-   controlled deployment;

-   production governance;

-   human accountability for AI-assisted engineering.

Every Business Activity implemented within the Aurex Intelligent
Operating Center shall satisfy the Engineering Readiness Standard before
progressing through implementation, verification, deployment, and
production release, ensuring that all engineering activities remain
governed, repeatable, measurable, and aligned with the constitutional
architecture of the platform.

**One Final Recommendation**

After **A.12**, I would add **only one final appendix section**:

**A.13 --- Closing Statement & Implementation Adoption**

Not another technical section.

A short constitutional closing that states:

-   IMP-001 is the authoritative implementation standard.

-   All Business Activities shall conform to it.

-   Future evolution occurs through versioned governance.

-   Deviations require architectural approval.

Then **freeze IMP-001 Version 1.0**.

I would resist adding anything beyond that. At that point, the document
is no longer missing implementation guidance---it has become a complete
implementation constitution for the Aurex platform.

**A.13 Constitutional Adoption & Evolution**

**A.13.1 Purpose**

This appendix formally establishes the Canonical Business Activity
Implementation Pattern (IMP-001) as the authoritative implementation
standard for the Aurex Intelligent Operating Center.

It defines the governance principles for adopting, maintaining,
evolving, and enforcing the implementation architecture throughout the
lifecycle of the platform.

Upon approval, IMP-001 shall become the single constitutional authority
governing the implementation of Business Activities across all Business
Domains, Runtime Components, engineering teams, and AI-assisted software
development platforms.

**A.13.2 Constitutional Adoption**

The Aurex Intelligent Operating Center adopts IMP-001 as the
mandatory implementation constitution for Business Activity realization.

Every Business Activity shall be designed, implemented, tested,
deployed, and maintained in accordance with the principles established
within this document.

No implementation methodology shall supersede or contradict the
constitutional principles defined herein.

**A.13.3 Scope of Applicability**

IMP-001 applies to all Business Activities implemented within the
Aurex Intelligent Operating Center, including but not limited to:

-   Enterprise Management

-   Business Resilience Intelligence

-   Reporting

-   Evidence Management

-   Materiality Assessment

-   KPI Management

-   Workflow Management

-   Administration

-   Platform Services

-   Future Business Domains

The standard applies equally to:

-   human-developed software;

-   AI-assisted software;

-   internal platform services;

-   external extension modules;

-   partner-developed capabilities.

**A.13.4 Relationship with the Constitutional Architecture**

IMP-001 derives its authority from, and shall remain consistent with,
the constitutional architecture of the Aurex platform.

The constitutional documents collectively define:

  -----------------------------------------------------------------------
  **Constitutional         **Responsibility**
  Document**               
  ------------------------ ----------------------------------------------
  Blueprint                Enterprise Platform Vision

  SD-001                   User Experience Architecture

  SD-002                   Canonical Business Object Architecture

  SD-003                   Enterprise Interaction Architecture

  URA-001                  Identity, Authorization & Assignment

  ERG-001                  Enterprise Structure & Relationship Management

  CMD-001                  Canonical Metadata Architecture

  **IMP-001**              Canonical Business Activity Implementation
                           Pattern
  -----------------------------------------------------------------------

Together, these documents constitute the authoritative architectural
foundation of the Aurex Intelligent Operating Center.

Implementation shall conform to all constitutional documents
simultaneously.

**A.13.5 Governance**

Ownership of IMP-001 shall reside with the Aurex Architecture
Governance Board.

Governance responsibilities include:

-   architectural stewardship;

-   version management;

-   change approval;

-   implementation compliance;

-   architectural exception review;

-   periodic constitutional review.

Architectural governance shall preserve the stability and integrity of
the implementation standard.

**A.13.6 Evolution Principles**

IMP-001 is intended to evolve in a controlled and governed manner.

Future revisions shall adhere to the following principles:

-   preserve backward architectural compatibility where practical;

-   introduce new implementation capabilities without compromising
    existing constitutional principles;

-   avoid unnecessary complexity;

-   maintain technology independence;

-   remain implementation-focused rather than technology-specific.

Evolution shall be deliberate rather than incremental.

**A.13.7 Architectural Exceptions**

Where exceptional business or technical circumstances require deviation
from IMP-001:

-   the deviation shall be documented;

-   the business justification shall be recorded;

-   the architectural impact shall be assessed;

-   formal approval shall be obtained from Architecture Governance.

Architectural exceptions shall remain exceptional.

They shall not become alternative implementation standards.

**A.13.8 Compliance**

Compliance with IMP-001 shall be verified through:

-   architecture reviews;

-   implementation reviews;

-   automated validation;

-   AI-generated code verification;

-   quality assurance;

-   release governance.

Compliance evidence shall be retained as part of the engineering
lifecycle.

**A.13.9 Future Technology Independence**

The principles established within IMP-001 shall remain independent of:

-   programming languages;

-   frameworks;

-   databases;

-   workflow engines;

-   AI coding platforms;

-   cloud providers;

-   deployment technologies;

-   development tools.

Technologies may evolve.

Implementation principles shall remain stable.

**A.13.10 Constitutional Statement**

The Canonical Business Activity Implementation Pattern establishes the
immutable implementation principles governing the realization of
business capabilities within the Aurex Intelligent Operating Center.

Every Business Activity, irrespective of Business Domain, implementation
technology, engineering methodology, or AI-assisted development
platform, shall conform to the constitutional principles defined within
this document.

Business intent shall remain the foundation of implementation.

Business Activities shall remain the canonical unit of execution.

Platform capabilities shall remain reusable.

Architecture shall govern implementation.

Technology shall serve architecture.

Through these principles, the Aurex Intelligent Operating Center
preserves a consistent, governed, scalable, observable, and
technology-independent implementation model capable of supporting the
long-term evolution of the enterprise platform.

**My Final Assessment of IMP-001 — Updated for v1.1**

*(This supersedes the v1.0 assessment below, which claimed completeness across "Sections 1-7" without Sections 8-12. That claim was found inaccurate against the document's own originally-stated scope during the Version 1.0 constitutional validation. Retained below for audit history, not as the current position.)*

**Freeze IMP-001 Version 1.1.** Sections 8-12 (API Standards, Event Implementation Standards, Frontend Standards, Testing Strategy, CI/CD & DevOps) close the five gaps identified in that validation - each traces to a specific principle already locked in SD-001, SD-002, SD-003, URA-001, ERG-001, or the Technical Architecture, rather than introducing new architectural decisions. Sections 1-7 and Appendix A required no changes; the validation confirmed them architecturally sound. This version's completeness claim is checkable: every topic named in the original planning outline (now corrected above) has a corresponding written section, with zero exceptions - unlike v1.0, which claimed completeness while silently omitting five of its own stated topics.

---

**My Final Assessment of IMP-001 (v1.0 - superseded, retained for history)**

Having now gone through the entire document and helped refine its
concluding appendices, I would make one final recommendation.

**Freeze IMP-001 Version 1.0.**

Not because it is perfect---no architecture ever is---but because it has
reached the point of **architectural completeness**.

It now contains:

-   **Constitutional principles** (Sections 1--7).

-   **Normative implementation blueprint** (Appendix A).

-   **AI-independent engineering guidance**.

-   **Engineering readiness and governance**.

-   **Controlled evolution model**.

At this stage, **the marginal value of adding more content is lower than
the value of implementing the platform**.

If I were acting as Chief Architect, I would sign off IMP-001 Version
1.0 and direct the engineering team to begin implementation, allowing
future refinements to emerge from real implementation experience rather
than speculative architecture. I believe that\'s the healthiest point at
which to transition from design to delivery.

---

**Section 8 — API Standards**

**8.1 Purpose**

This section defines the mandatory standard for every API endpoint exposed by the Aurex platform. It exists to close a gap identified during the Version 1.0 constitutional validation: the original document specified how Business Objects and Business Activities are implemented internally, but not how they are exposed for consumption by the frontend, external integrations, or AI-assisted development tools.

**8.2 Every Endpoint Maps to Exactly One Business Activity**

**IMP-API-001 — No Endpoint-Per-Table**

APIs shall never expose raw CRUD operations against a database table. Every endpoint corresponds to exactly one Business Activity Contract (BAC), per Appendix A.5. An endpoint named `POST /enterprises` does not exist; `POST /activities/create-enterprise` does — the URL names the Business Activity, not the underlying object, consistent with Business Activities Over CRUD (Section 1).

**IMP-API-002 — Authorization Resolves Before Execution, Not During**

Every endpoint shall resolve authorization through URA-001's Authorization Resolution Precedence (URA-001-76: Named User > Group > Approval Authority > Business Role > Domain Permission) as a pre-execution gate, never as an inline check buried inside business logic. An endpoint that begins executing before authorization resolves is non-compliant regardless of whether it later rejects the request — the resolution must be the first action taken, and must be independently testable (see Section 11.3).

**IMP-API-003 — Every Response Carries Confidence, Not Just Data**

Per L14 (Confidence Always Visible), any endpoint returning a value sourced from `metric_registry`, `kpi_registry`, or any CIL-derived table shall include that value's confidence score and evidence reference in the same response payload — never as a separate endpoint the frontend must additionally call. A response containing a number with no accompanying confidence field is non-compliant.

**IMP-API-004 — Errors Are Explained, Never Swallowed**

Per L11 (No Black-Box Conclusions), an API error response shall state what failed, why, and — where the failure is a business rule (not a system fault) — which specific rule was violated, by reference to its principle ID (e.g., "rejected: URA-001-88, delegation requires an end date"). Generic 400/500 responses with no business-rule reference are non-compliant for any rule-driven rejection.

**8.3 Versioning**

API versions follow the same effective-dating discipline SD-002-011 establishes for every business object: a breaking change to an endpoint's contract requires a new version path (`/v2/...`), the prior version remains callable for the minimum deprecation window SD-001-110 establishes (two releases), and the deprecation is itself an audited event, not a silent removal.

**8.4 Reference Endpoint**

Following the pattern of Appendix A.5.1's reference Business Activity ("Create Enterprise"), the reference endpoint for this section is:

`POST /activities/create-enterprise` — resolves authorization (IMP-API-002) against the Enterprise domain's Domain Permission, executes the Create Enterprise Business Activity Contract (Appendix A.5.2) exactly as specified there, returns the created Enterprise Node's identity plus its resolved confidence and evidence references (IMP-API-003) if any fields were AI-populated during creation, or a business-rule-referenced rejection (IMP-API-004) if validation failed.

---

**Section 9 — Event Implementation Standards**

**9.1 Purpose**

This section defines the mandatory standard for implementing domain events. It closes a second gap from the constitutional validation: the platform's event architecture is defined at the data-model level (Technical Architecture) and the interaction-law level (SD-003), but the engineering pattern for *implementing* an event handler was not specified.

**9.2 The Two Event Systems Are Never Conflated**

**IMP-EVT-001 — External Events and Workflow Events Use Separate Handlers**

Per the resolution already established in the Technical Architecture and URA-001 v2.1: `event_registry` (external-world events — market, regulatory, climate signals) and `workflow_event_registry` (internal workflow events — ENTER, APPROVE, ESCALATE, DELEGATE) are structurally distinct tables governing distinct concerns. Engineering shall implement two separate event-handling pipelines, never one generic "event handler" that branches on event type. A single handler function that processes both an external market signal and an internal APPROVE action is non-compliant — these are different domains with different authorization requirements (external events carry no URA-001 authorization context; workflow events always do).

**9.3 Idempotent by Construction**

**IMP-EVT-002 — Every Handler Checks for Prior Processing Before Acting**

Every event handler shall check whether the event has already been processed (by event ID, not by re-deriving state) before executing its side effect. This is the same idempotency discipline Appendix A's Business Activity pattern requires, applied at the event layer: a workflow event delivered twice (network retry, queue redelivery) shall produce the same end state as delivered once, verified by a stored "already processed" marker, not by the handler's logic happening to be naturally idempotent.

**9.4 Ordering and Replay**

**IMP-EVT-003 — Events Within One Business Activity Execution Are Ordered; Across Activities They Are Not Guaranteed To Be**

Events generated within a single Business Activity's execution pipeline (Section 6) preserve their emission order. Events from different, concurrently-executing Business Activities carry no cross-activity ordering guarantee. Any implementation requiring cross-activity ordering shall make that dependency explicit via a stated precondition on the dependent activity's Business Activity Contract, never assume ordering that isn't structurally guaranteed.

**9.5 Reference Event Handler**

Following the "Create Enterprise" reference activity (Appendix A.5.1), its terminal event `ENTERPRISE_CREATED` is handled by: checking `workflow_event_log` for a prior record of this exact event ID (IMP-EVT-002) before proceeding; if unprocessed, updating the dependent `enterprise_view_registry` projections and recording the new processed-marker in the same transaction (Section 6's Transaction Management applies identically here); if already processed, returning success without re-executing the side effect.

---

**Section 10 — Frontend Standards**

**10.1 Purpose**

This section defines the mandatory engineering standard for implementing SD-001 v2.0's screen and widget principles as actual frontend code. It closes a third gap: SD-001 defines what a screen must be; this section defines how a frontend engineer or AI coding tool builds one.

**10.2 Screens Render From `screen_registry`, Never From Hardcoded Routes**

**IMP-FE-001 — No Screen Exists Outside the Registry**

Per SD-001-016 (Screens Are Metadata, Not Code), a frontend route/page shall never be created without a corresponding `screen_registry` row. The frontend's routing layer reads `screen_registry` at build or runtime and generates navigation from it (SD-001-018) — a developer hardcoding a new route bypasses this and is non-compliant, regardless of how correct the resulting page looks.

**IMP-FE-002 — The Sacred 12 Constraints Are Enforced in Frontend Code, Not Assumed From the Database Trigger**

The database trigger (`trg_sacred_12_cap`) prevents an invalid *configuration* state; it does not prevent a frontend component from rendering a Guided Completion widget inside a screen flagged `is_sacred_12 = TRUE`. The frontend component library shall check `screen_registry.is_sacred_12` and `allows_guided_completion` before rendering any data-collection widget, and refuse to render one if the screen is Sacred 12 — this is a second, independent enforcement layer, not a redundant one, since the trigger protects the data and the frontend check protects the rendered experience.

**IMP-FE-003 — The Action Center Component Enforces Its Own Cap Independently of the Backend Trigger**

Per L38, the frontend Action Center component shall never render more than 7 action items regardless of how many `intelligence_work_queue` rows the API returns — if the backend ever returns 8 (a defect, since `trg_action_center_max_seven` should prevent this), the frontend still caps display at 7 and logs the anomaly, rather than rendering an 8th item because the API happened to send it. Defense in depth, not trust in a single layer.

**10.3 Progressive Disclosure Is a Component Contract, Not a Convention**

**IMP-FE-004**

Per SD-001-021, every data-bearing widget component shall implement four distinct render states (Summary, Details, Evidence, Audit History) as a required prop interface, not as an ad-hoc pattern individual developers may or may not follow. A widget missing one of the four states is an incomplete implementation, not a stylistic choice.

**10.4 Reference Component**

The reference widget for this section is the Evidence Panel (SD-001-020): renders `metric_registry`'s confidence score and evidence reference (IMP-API-003's response contract) at Summary level by default, expands to the full evidence chain (IMP-FE-004's Evidence state) on user interaction, and never appears on a screen where `screen_registry.is_sacred_12 = TRUE` in its data-collecting form (IMP-FE-002) — only in its read-only, consuming form, per ERG-001/SD-001's shared principle that the Sacred 12 consume intelligence, they do not discover it.

---

**Section 11 — Testing Strategy**

**11.1 Purpose**

This section defines the mandatory test strategy. It closes a fourth gap: the document specifies a Definition of Done (Appendix A.5.8) that references "tests pass," without specifying what must be tested or at what layer.

**11.2 Business Activity Contract Tests Are the Primary Layer, Not Unit Tests**

**IMP-TEST-001**

The primary test layer for Aurex is not conventional unit testing of internal functions — it is **Business Activity Contract testing**: for every Business Activity, a test suite verifies that its behavior matches its approved BAC (Appendix A.5) exactly, including every stated precondition, every side effect, and every terminal event. A Business Activity with passing unit tests but no BAC-conformance test is not done, per the Definition of Done this section extends.

**11.3 Authorization Boundary Tests Are Mandatory and Independent**

**IMP-TEST-002**

Every endpoint (Section 8) requires a dedicated test verifying that URA-001's Authorization Resolution Precedence resolves correctly for at least: a Named User override, a Group-based grant, and a Domain Permission-only fallback — proving the precedence chain (URA-001-76), not just proving "authorized users can access, unauthorized cannot." A test suite that only checks the boundary case (authorized/unauthorized) without checking precedence order is insufficient.

**11.4 Idempotency Tests Are Required for Every Event Handler and Every Seed Script**

**IMP-TEST-003**

Per Section 9.3 (IMP-EVT-002) and the Master Data Population Specification's own idempotency requirement, every event handler and every seed population script requires a test that executes it twice and asserts identical end state — not merely "runs without error twice."

**11.5 Language Purge Is a CI-Enforced Test, Not a Manual Review Step**

**IMP-TEST-004**

Given the volume of language-purge corrections required across every constitutional document in this platform's history, this is elevated from a manual review checklist item to a mandatory automated test: any CI pipeline run scans newly generated content (screen labels, narrative text, report templates) against the binding substitution table and fails the build if a banned term (ESG, Sustainability, Carbon, Net Zero, Green Bond, Scope 1/2/3, Diversity Metrics, CSRD) appears outside an explicitly-tagged internal reference table (per the precedent established for `framework_registry`'s legitimate specialist content). This closes the gap where every document in this platform's history needed a manual language-purge pass after the fact.

**11.6 Enterprise Intelligence Requires Contract Tests at the Knowledge, Retrieval, and Agent Boundaries** *(added under the Enterprise Intelligence Engineering Architecture Enhancement, Phase 3)*

**IMP-TEST-005**

Section 13's Knowledge Graph, Retrieval, and Agent Orchestration implementation patterns each require the same Contract testing discipline IMP-TEST-001 already establishes for Business Activities, applied at three additional boundaries: (1) a `KnowledgeGraphRepository` contract test verifying that a write is visible through both its Postgres registry row and its Neo4j graph reference, per RTA-001 §12.7's synchronization guarantee; (2) a `RetrievalService` contract test verifying that a query returns results ranked consistently with `vector_index_registry.retrieval_mode`, and that every returned result carries a citation locator, per RTA-001 §13.7; (3) an `AgentOrchestrator` contract test verifying that every execution reaches the Ask User Gate (RTA-001 §13.12a) only when all five Termination Criteria are independently, verifiably false — never on a mocked shortcut. A Section 13 implementation with passing unit tests but no contract test at these three boundaries is not done, per the same Definition of Done IMP-TEST-001 extends.

**11.7 Enterprise Intelligence Orchestration Requires Contract and Determinism Tests at Eleven Further Boundaries** *(added under the Enterprise Intelligence Engineering Architecture Enhancement, Phase 3, AMD-013)*

**IMP-TEST-006**

Section 13.6–13.14's patterns each require a contract test verifying they honor the runtime rule they implement, never merely that they return a value: (1) `Planner` — a produced `Plan` is validated against every RTA-001 §13.6b Planner Responsibility field being present and non-null, and a `replan()` call is verified to produce a new `Plan` instance, never a mutation of the prior one; (2) `ExecutionCapabilityResolver` — verified to never return a capability whose permission, availability, health, or policy check failed, and never to leak which registry (Agent/Tool/Reasoning Engine) answered through the returned `ExecutableCapability`'s type; (3) `DiscoveryProviderResolver` — verified to return every active, in-scope provider when more than one matches, never a single provider by default; (4) `ReasoningEngineResolver` — verified that `ExecutableReasoningEngine.invoke()` accepts and returns only contract-shaped objects, with a test asserting no vendor SDK type is reachable from the interface's public surface (a compile-time or reflection-based check, not a runtime one); (5) `ExecutionStrategy` — each of the five implementations independently tested against the same `TaskGraph` fixture, asserting Sequential never begins a task before its predecessor completes and Parallel never blocks an independent task on an unrelated one; (6) Multi-Agent execution — a Capability Delegation test verifying a delegation absent from `agent_tool_grant` is refused by the resolver, never by the delegating capability's own logic; (7) `EvidenceFusionService` — verified to compute all seven `evidence_fusion_registry` dimensions but never to write `sufficiency_determination` itself; (8) the Ask User Gate — a test asserting the gate remains closed when any one of its conditions (RTA-001 §13.12a) is untested/unknown, never defaulting to open; (9) the Evidence Sufficiency Gate — a test asserting all three determinations (SUFFICIENT / INSUFFICIENT_CONTINUE / INSUFFICIENT_ESCALATE) are independently reachable from distinct fixture inputs, not just the two extremes; (10) Knowledge updates — a `PermissionEnforcingKnowledgeGraphRepository` test verifying a write is refused when `knowledge_graph_write_flag` is false, structurally (via the decorator), not by convention; (11) Memory updates — the equivalent test for `memory_write_flag` against `MemoryRepository`. A Section 13.6–13.14 implementation with passing unit tests but no contract/determinism test at these eleven boundaries is not done, per the same Definition of Done IMP-TEST-001 extends.

---

**Section 12 — CI/CD & DevOps**

**12.1 Purpose**

This section defines the mandatory deployment pipeline standard. It closes the fifth and final gap from the constitutional validation.

**12.2 Schema Migrations Follow the Same Deprecation Discipline as Business Objects**

**IMP-CICD-001**

A schema change (new table, new column, renamed column) is itself subject to SD-001-110's deprecation floor: a column being removed or renamed remains available (via a database view or dual-write, engineer's choice) for the same minimum two-release window applied to every other deprecation in this platform (`role_registry`, `consolidation_method`, and the deprecations already executed in the locked Technical Architecture are the reference precedent). No migration in CI/CD may drop a column in the same release that stops writing to it.

**12.3 Seed Data Execution Is a Pipeline Stage, Not a Manual Step**

**IMP-CICD-002**

The Master Data Population Specification (MDP-001) executes as an automated, idempotent pipeline stage on environment provisioning — never as a manually-run script an engineer executes once and forgets. Per MDP-001's own idempotency rule, this stage is safe to re-run on every deployment without duplicating rows, which is what makes automating it (rather than gating it behind manual judgment) safe.

**12.4 Environment Promotion Requires Constitutional Document Version Alignment**

**IMP-CICD-003**

Before promoting a build to any environment, the pipeline verifies that the deployed code's assumed versions of SD-001 through ERG-001 and CMD-001 match the versions actually locked at build time (tracked via `architecture_version_registry`, Section A of the Master Data Population Specification). A build referencing SD-002 v1.0 principles while v2.0 is the locked version fails this check rather than deploying against a stale architectural assumption.

**12.5 Reference Pipeline**

Build → run `IMP-TEST-001` through `IMP-TEST-006` → verify `architecture_version_registry` alignment (IMP-CICD-003) → apply pending migrations under the deprecation floor (IMP-CICD-001) → execute MDP-001 seed stage (IMP-CICD-002) → provision/verify Enterprise Intelligence infrastructure (IMP-CICD-004) → provision/verify distributed orchestration infrastructure (IMP-CICD-005) → promote.

**12.6 Enterprise Intelligence Infrastructure Provisioning Is a Pipeline Stage** *(added under the Enterprise Intelligence Engineering Architecture Enhancement, Phase 3)*

**IMP-CICD-004**

Provisioning or verifying the Neo4j Aura graph instance, the `vector_index_registry` indices, and the `ai_tool_registry`'s platform-default rows (Master Technical Architecture, AMD-012, Part F Addendum) is a pipeline stage, following IMP-CICD-002's same idempotent-on-every-deployment discipline — never a manually-run provisioning script. A build that reaches promotion without this stage having verified the graph instance and default vector indices exist fails the pipeline, consistent with IMP-CICD-003's version-alignment check.

**12.7 Distributed Orchestration Infrastructure Provisioning and Observability** *(added under the Enterprise Intelligence Engineering Architecture Enhancement, Phase 3, AMD-013)*

**IMP-CICD-005**

`Planner` (§13.6), `ExecutionCapabilityResolver` (§13.7), `DiscoveryProviderResolver` (§13.8), and `ReasoningEngineResolver` (§13.9) instances are stateless services and shall be deployed horizontally scalable behind a load balancer, following the same principle IMP-CICD-004 already applies to infrastructure provisioning: no manual scaling step, and no single-instance deployment assumed anywhere in Section 13.6–13.14's implementation guidance. High availability for `agent_registry`, `discovery_provider_registry`, `reasoning_engine_registry`, and `discovery_strategy_registry` default-row provisioning (Master Technical Architecture, AMD-013 Phase 1) is verified as part of this pipeline stage, extending IMP-CICD-004's Enterprise Intelligence infrastructure check rather than duplicating it. Every pattern in Section 13.6–13.14 is observable per Section 13's own §13.15 pointer to this stage: `Planner` Plan/Replan events, `ExecutionCapabilityResolver`/`DiscoveryProviderResolver`/`ReasoningEngineResolver` resolution outcomes, `EvidenceFusionService` dimension scores, and every RTA-001 §22.12 Runtime Event (including the AMD-013 additions, `EVIDENCE_FUSED` and `REPLANNED`) shall emit telemetry through the same Observability Platform every other runtime in this document already reports to — no Section 13.6–13.14 pattern introduces a separate, parallel telemetry mechanism.

---

**Section 13 — Specialized Engineering Methodologies** *(retitled under the Runtime Engineering Methodology governance determination, WP-02 — Enterprise Intelligence Implementation Patterns, §§13.1-13.16, originally added under the Enterprise Intelligence Engineering Architecture Enhancement, Phase 3, are unchanged and now constitute this Section's first engineering specialization; Runtime Component Engineering, §§13.17-13.25, is added as its second)*

**13.1 Purpose**

This section closes the implementation-pattern gap the post-Stage-III Enterprise Intelligence Execution Architecture Readiness Review identified: Master Technical Architecture (AMD-012) now specifies what the Knowledge Graph, Memory Graph, Enterprise RAG, Vector Database, and AI Tool Registry *are*; RTA-001 (§§12, 13, 21, 22) now specifies how they *execute*. Neither specifies how an engineer *builds* them. This section is implementation guidance only — coding patterns, interfaces, and reference structure. It does not restate architecture (Master Technical Architecture's exclusive scope) or runtime execution sequencing (RTA-001's exclusive scope); every pattern below cites the architectural or runtime authority it implements rather than re-describing it.

**13.2 Knowledge Graph Implementation Pattern**

**IMP-EI-001**

A Knowledge Asset is implemented using the same Canonical Business Object Stack Section 5.3 already mandates (Aggregate Root → Metadata → Business Rules → Validation → Persistence → Repository → Domain Service), applied to the `knowledge_asset_registry` and `enterprise_knowledge_graph_registry` tables Master Technical Architecture (AMD-012) defines. The Persistence layer is dual: a `KnowledgeGraphRepository` interface exposes one implementation writing to PostgreSQL (the registry rows) and one writing to the Neo4j driver (the traversable graph), coordinated so that a single Domain Service call updates both — the engineer never writes to Neo4j and PostgreSQL from two independent call sites. The synchronization sequence this Repository's write path follows is RTA-001 §12.7's Graph Synchronization Pipeline; it is not re-specified here.

**13.3 Enterprise RAG & Retrieval Implementation Pattern**

**IMP-EI-002**

`Backend/Services/AIService/services/rag_engine.py`, `embedding_provider.py`, and `vector_provider.py` are this pattern's existing canonical reference implementation, in the same sense Appendix A is the canonical reference implementation for Section 6 — this section formalizes their existing shape as the mandatory pattern, rather than introducing a new one:

- A `RAGService` domain service, dependency-injected with an `EmbeddingProvider` and a `VectorProvider` interface (already the actual constructor shape of `RAGEngine`) — no Business Activity may call an embedding model or vector store directly; every call passes through `RAGService`.
- `EmbeddingProvider` and `VectorProvider` are interfaces, not concrete classes, so the embedding model and vector database named in Master Technical Architecture's frozen technology stack can be substituted in tests (§13.6 below) without a `RAGService` code change.
- `RAGService.retrieve()` returns a result set including, for every item, the `document_chunk_registry` row it came from — never bare text — so that Citation Generation (RTA-001 §13, AI Response stage) has a locator to attach without a second lookup.
- Reranking and hybrid-mode combination (`vector_index_registry.retrieval_mode`) are implemented as strategy objects injected into `RAGService`, not as conditional branches inside it — a new retrieval mode is added by registering a new strategy, never by editing `RAGService` itself.

**13.4 Chunking Strategy Implementation Pattern**

**IMP-EI-003**

A `ChunkingStrategy` interface, implemented per source document type (structured table, prose document, transcript), producing `document_chunk_registry` rows. Default parameters: sentence-boundary-aware splitting, target chunk size and overlap configurable per `ChunkingStrategy` implementation, never hardcoded in the caller. Every produced chunk carries `chunk_locator` (page/section/table/cell, per SD-002-043) at creation time — a chunk without a locator is a defect in the `ChunkingStrategy` implementation, not an acceptable partial result. Chunking runs as part of Document Ingestion (Master Technical Architecture Part F Addendum's Document Ingestion Service); it is never deferred to first-query time.

**13.5 Agent Orchestration Implementation Pattern**

**IMP-EI-004**

An `AgentOrchestrator` domain service implementing RTA-001 §13.6a's Agent Execution Lifecycle as code, composed of three injected interfaces mirroring RTA-001's own §13.6b/§13.6c/§13.9a naming exactly, so that a reader moving between RTA-001 and this codebase finds the same vocabulary:

- `Planner` — produces a Plan and its Termination Criterion (RTA-001 §13.6b). Implemented as a strategy per AI Capability Category (RTA-001 §13.5), not a single monolithic planner.
- `TaskDecomposer` — decomposes a Plan's sub-tasks (RTA-001 §13.6c). A sub-task resolving to a Business Activity is dispatched through the existing `BusinessActivityEngine` interface (Section 6.15), never through a path `AgentOrchestrator` maintains itself — this is a hard dependency, not a convention.
- `ToolSelector` — selects from `ai_tool_registry` (RTA-001 §13.9a) via a `ToolRegistryRepository`, itself following the same Repository pattern as §13.2 above.

`AgentOrchestrator` itself contains no business logic — it sequences calls to these three interfaces and to `RAGService` (§13.3) and `KnowledgeGraphRepository` (§13.2), exactly mirroring RTA-001 §22's state machine. The state machine's states (REQUESTED, DISCOVERING, ...) are implemented as an explicit enum the orchestrator transitions through, not inferred from control flow, so that RTA-001 §22.12's Runtime Events can be emitted deterministically at each transition.

**13.5a AMD-013 Phase 3 Note**

Sections 13.6 through 13.14 below extend this Section under the Enterprise Intelligence Orchestration Enhancement (AMD-013 Phase 3). Every pattern in them resolves abstractions dynamically at runtime, per this phase's governing Implementation Philosophy: no interface, type signature, or dependency-injection binding anywhere below names a specific AI vendor, LLM vendor, agent framework, MCP, AI Foundry, AI Skill, or AI Function — every such choice is resolved through Master Technical Architecture's registries and RTA-001's runtime policies, referenced by name and never restated.

**13.6 Planner Implementation Pattern**

**IMP-EI-005**

A `Planner` interface, one implementation per AI Capability Category (RTA-001 §13.5), matching 13.5's own `AgentOrchestrator` composition:

- `Planner.initialize(PlanningContext)` — `PlanningContext` carries the execution objective, the resolved Enterprise Context (RTA-001 §10), and, on Replanning, the prior Plan and its failure or Result Evaluation reason. `PlanningContext` is a value object, never a mutable shared state the rest of the pipeline reaches into.
- `Planner.produce() → Plan` — a `Plan` is an immutable value object fixing every element RTA-001 §13.6b's Planner Responsibilities list requires: execution strategy, discovery strategy, capability requirements (not concrete capabilities — see §13.7), provider/source requirements, execution ordering, a `TaskGraph`, `RetryPolicy`, `TimeoutPolicy`, `CostPolicy`, `LatencyPolicy`, `EscalationPolicy`, and `CompletionPolicy`. A `Plan` is never mutated after `produce()` returns — Dynamic Replanning (below) always produces a new `Plan` instance.
- Goal decomposition, task graph construction, and dependency graph generation are internal `Planner` responsibilities producing the `TaskGraph` — a directed graph of sub-tasks and their dependencies, the same graph Task Decomposition (RTA-001 §13.6c) and Execution Graph generation (§13.10 below) consume. `TaskGraph` construction never assumes a specific execution strategy; strategy is applied to an already-built `TaskGraph`, never baked into its construction.
- `Planner.replan(PlanningContext, priorPlan, reason) → Plan` — a distinct method, implementing RTA-001 §13.6b's Replanning rule: every Replan is a new, separately auditable `Plan`, produced through this method only, never through re-invoking `produce()` on mutated state.
- Retry Planning and Completion Planning are `Plan` attributes (`RetryPolicy`, `CompletionPolicy`), not separate planners — a single `Plan` carries its own retry and completion behavior end to end.

**13.7 Execution Capability Resolver Pattern**

**IMP-EI-006**

An `ExecutionCapabilityResolver` interface implementing RTA-001 §13.9b's Execution Capability Selection and Master Technical Architecture's Execution Capability conceptual abstraction (Part F Addendum, AMD-013 Phase 1A) as code:

- `ExecutionCapabilityResolver.resolve(CapabilityRequirement) → ExecutableCapability` — `CapabilityRequirement` names a role (Invoking, Invoked, or Transforming) and a declared contract, never a specific Agent, Tool, or Reasoning Engine by identity. Internally, the resolver queries whichever of Agent Registry, AI Tool Registry, or Reasoning Engine Registry realizes the requested role, via the same Repository pattern §13.2 and §13.5 already establish — the caller of `resolve()` never knows or cares which registry answered.
- Resolution evaluates, in order: **permission** (the capability's declared read/write flags against the requester's Authorization Context, per RTA-001 §13.7b), **availability** (an injected `AvailabilityCheck` port, never a hardcoded ping), **health** (an injected `HealthCheck` port), and **policy** (the capability's governing policy, reused from `confidence_scoring_registry` via §13.2's Repository pattern, never re-implemented).
- `ExecutionCapabilityResolver.resolve()` returns an `ExecutableCapability` — a single, uniform interface (`invoke(input) → output`) regardless of whether the underlying realization is an Agent, a Tool, or a Reasoning Engine. No caller of `ExecutableCapability.invoke()` ever branches on which registry produced it — this is the resolver's entire purpose: Agent, Tool, and Reasoning Engine are architectural roles the resolver implements dynamically, never fixed types the implementation depends on.

**13.8 Discovery Provider Resolver Pattern**

**IMP-EI-007**

A `DiscoveryProviderResolver` interface implementing RTA-001 §13.6f's provider-selection runtime rule:

- `DiscoveryProviderResolver.resolve(ProviderCategory, DiscoveryCriteria) → List<ExecutableProvider>` — `ProviderCategory` is Enterprise, External, or Real-Time, matching Discovery Provider Registry's `provider_category` (Master Technical Architecture). The resolver queries the registry via the Repository pattern and **never returns a single provider when multiple active, in-scope providers match** — implementing RTA-001 §13.6f's rule that the runtime shall not assume a single source represents complete enterprise knowledge.
- Before returning, the resolver evaluates each candidate's availability, permissions, latency, cost, freshness, and health through the same injected-port pattern §13.7 establishes (`AvailabilityCheck`, `HealthCheck`) plus a `LatencyProbe` and `CostEstimator` — all pluggable, none hardcoded per named provider type (SharePoint, SAP, Bloomberg, and so on are configuration rows, per Master Technical Architecture's `provider_type` enumeration; none of them appears in this resolver's code).
- `ExecutableProvider`, like `ExecutableCapability` (§13.7), is a uniform interface (`fetch(query) → List<RawItem>`) — the resolver's caller never branches on provider type.

**13.9 Reasoning Engine Resolver Pattern**

**IMP-EI-008**

A `ReasoningEngineResolver` interface implementing vendor-independent reasoning, per RTA-001 §13.9b/§13.9c:

- `ReasoningEngineResolver.resolve(TaskRequirement) → ExecutableReasoningEngine` — selects among commercial, enterprise-proprietary, open-weight, and future engine categories (Reasoning Engine Registry's `engine_category`, Master Technical Architecture) using the same cost/performance/data-classification/latency criteria Model Selection (RTA-001 §13.9) already fixes.
- `ExecutableReasoningEngine` exposes exactly one method: `invoke(ContractInput) → ContractOutput`, where `ContractInput` and `ContractOutput` are generated or validated from the selected engine's `input_contract_schema_json`/`output_contract_schema_json` (Reasoning Engine Registry) — the Reasoning Contract RTA-001 §13.9c governs. No vendor SDK type (an OpenAI response object, an Anthropic message type, a Gemini candidate type) ever appears in this interface or in any type that implements it; adapting a specific vendor's SDK to `ContractInput`/`ContractOutput` is this pattern's own internal, encapsulated concern, never exposed to a caller.
- Swapping the underlying model — GPT for Claude, Claude for an enterprise-hosted model — is a `reasoning_engine_registry` configuration change and a new `ExecutableReasoningEngine` implementation registered against it, never a change to any calling code.

**13.10 Execution Strategy Pattern**

**IMP-EI-009**

One `ExecutionStrategy` interface (`execute(TaskGraph, ExecutionCapabilityResolver) → List<Result>`), with one implementing class per RTA-001 §13.6d strategy — `SequentialExecutionStrategy`, `ParallelExecutionStrategy`, `HybridExecutionStrategy`, `DynamicGraphExecutionStrategy`, `AdaptiveExecutionStrategy` — following the classic Strategy pattern. The Planner (§13.6) selects a strategy by name, resolved from Discovery Strategy Registry (Master Technical Architecture) through a factory/registry lookup keyed on `strategy_type`, never a conditional or switch statement branching on strategy inline in the orchestrator. `AdaptiveExecutionStrategy` is implemented as a composite that itself selects among the other four per sub-task, per RTA-001 §13.6d's Adaptive semantics — it does not introduce a sixth execution mechanism of its own.

**13.11 Multi-Agent Implementation Pattern**

**IMP-EI-010**

Single-capability, multiple-capability, parallel, sequential, adaptive, and graph-based capability execution are not six separate implementations — they are `ExecutionStrategy` (§13.10) applied to the set of `ExecutableCapability` instances (§13.7) a Plan's `TaskGraph` names. `AgentOrchestrator` (§13.5) composes `Planner` (§13.6), `ExecutionCapabilityResolver` (§13.7), and `ExecutionStrategy` (§13.10); it introduces no further orchestration concept. Capability Delegation (RTA-001 §13.6e) — one `ExecutableCapability` invoking another — is implemented as a nested `ExecutionCapabilityResolver.resolve()` call from within a capability's own `invoke()` implementation, gated by the same grant check (`agent_tool_grant`, Master Technical Architecture) the resolver already enforces; delegation never bypasses the resolver. No orchestration framework (LangGraph, CrewAI, AutoGen, Semantic Kernel, or any other) is named in any interface, type, or dependency-injection binding in this pattern; where a concrete `ExecutionStrategy` implementation uses one internally, it is fully encapsulated behind that implementation's own `execute()` method and never exposed.

**13.12 Evidence Fusion Pattern**

**IMP-EI-011**

An `EvidenceFusionService` implementing the data pipeline RTA-001 §13.11a's continuous fusion runtime behavior requires, and nothing beyond it:

- **Evidence Collection** — accepts evidence items as they arrive from any `ExecutableCapability`, `ExecutableProvider`, or modality normalization (§13.14), never polling or batching by default.
- **Evidence Normalization** — maps each item to the Enterprise Evidence Model's common shape before merging.
- **Evidence Correlation** — groups items supporting or contradicting the same intelligence element, feeding the Correlation Node's contradiction handling (RTA-001 §22.5) — this pattern detects candidate correlations; RTA-001 governs what happens on a contradiction.
- **Evidence Consolidation** — merges correlated items into the current `evidence_fusion_registry` row (Master Technical Architecture), updating `fused_from_json` with full traceability, per SD-002-049.
- **Evidence Quality and Evidence Sufficiency** — this pattern computes and persists the seven `evidence_fusion_registry` dimension scores (Coverage, Quality, Diversity, Freshness, Consistency, Confidence, Cost, Latency) as data; it does **not** decide `sufficiency_determination` — that determination is the Evidence Sufficiency Gate's runtime rule (RTA-001 §13.11b), consumed by `AgentOrchestrator`, never recomputed by `EvidenceFusionService` itself.

**13.13 Knowledge & Memory Pattern**

**IMP-EI-012**

`KnowledgeGraphRepository` (§13.2) and a parallel `MemoryRepository` provide Knowledge and Memory access and updates; a `ContextService` provides Enterprise Context retrieval and persistence, per RTA-001 §13.7's Context Assembly. Permission Enforcement (RTA-001 §13.7b) is implemented as a decorator wrapping every one of these three repositories/services — `PermissionEnforcingKnowledgeGraphRepository`, and equivalently for Memory and Context — checking the invoking capability's declared read/write flags (Agent Registry, Master Technical Architecture) before delegating to the underlying repository. Business logic never performs this check inline; it is structurally impossible to reach the underlying repository without passing through the decorator, since only the decorator is registered for dependency injection.

**13.14 Discovery Pipeline Pattern**

**IMP-EI-013**

An end-to-end pipeline, implemented as a Chain of Responsibility with one independently testable, independently swappable stage per step, realizing RTA-001 §22.4's DISCOVERING state in full:

Discovery (§13.8's `DiscoveryProviderResolver.resolve().fetch()`) → Normalization (implementing RTA-001 §13.7a's Multi-Modal Normalization Runtime, one `Normalizer` implementation per `modality_type`) → Knowledge Object generation (persisted via a `KnowledgeObjectRepository` to `enterprise_knowledge_object_registry`, Master Technical Architecture) → Embedding (§13.3's `EmbeddingProvider`) → Retrieval (§13.3's `RAGService`) → Evidence creation (via `EvidenceFusionService`, §13.12) → Knowledge update and Memory update (via §13.13's decorated repositories).

Each stage depends only on the interface of the stage before it, never its concrete implementation — a new modality's `Normalizer` or a new provider's fetch behavior is added without changing any other stage.

**13.15 Testing and Deployment**

Testing for §13.2–§13.5 is governed by Section 11.6 (IMP-TEST-005); testing for §13.6–§13.14 is governed by Section 11.7 (IMP-TEST-006, added under AMD-013 Phase 3). Deployment/provisioning for §13.2–§13.5 is governed by Section 12.6 (IMP-CICD-004); deployment for §13.6–§13.14 is governed by Section 12.7 (IMP-CICD-005, added under AMD-013 Phase 3). None is restated here.

**13.16 Implementation Sequence**

Knowledge Graph Repository (§13.2) → Retrieval Service (§13.3), which depends on Document Chunking (§13.4) → Discovery Provider Resolver (§13.8) and Reasoning Engine Resolver (§13.9), which depend on Execution Capability Resolver (§13.7) → Execution Strategy (§13.10) → Planner (§13.6), which depends on all preceding resolvers and strategies being available to plan against → Agent Orchestrator (§13.5) and Multi-Agent Pattern (§13.11), which compose the Planner, resolvers, and strategies → Evidence Fusion (§13.12) and Knowledge & Memory (§13.13), consumed throughout → Discovery Pipeline (§13.14), which composes Discovery, Normalization, Embedding, Retrieval, Evidence, Knowledge, and Memory into one end-to-end flow, and depends on every preceding pattern in this section. No pattern in this section is independently implementable out of this order without stubbing the dependency this sequence states.

---

**13.17 Engineering Specialization Framework** *(added under the Runtime Engineering Methodology governance determination, WP-02)*

An Engineering Specialization is a domain of implementable units sharing a common Layer 1 constitutional source of truth (per ARCH-000 §3) but requiring engineering treatment distinct from Business Activity Engineering's own experiential shape (ERB/EX/Persona, derived via PE-001 from CAP-001). Section 13 is IMP-001's canonical home for every such specialization, per IMP-001's own Layer 3 mandate (ARCH-000 §3: "these documents define how constitutional architecture is engineered") and the unqualified "Enterprise Engineering" concern ARCH-000 §6 assigns to IMP-001 alone.

Two specializations exist as of this version:

- **Enterprise Intelligence Engineering** (§§13.1-13.16) — implements EIA-001's Knowledge Graph, Memory, and AI Runtime Components (RTA-001 §§12, 13, 21, 22), engineered directly through this Section with no Layer 2 intermediary, per the precedent this Section itself already established.
- **Runtime Component Engineering** (§§13.17-13.25) — implements RTA-001's remaining Runtime Components (§§6-11, 14-19), following the identical precedent.

**Governing rule.** Every specialization added to this Section MAY define its own Contract, Registry, and Readiness Assessment, shaped to its own object type. Every specialization SHALL reuse, never re-invent, the common Enterprise Engineering lifecycle (§6.23's Version Lifecycle and Canonical Version Model), governance principles (§6.22.12's Registry Governance principle, generalized), review methodology, Completion Gate, and Certification discipline (CLAUDE.md §19.7). A specialization's Contract, Registry, and Readiness Assessment are permitted to differ from every other specialization's; its lifecycle, governance, review, gate, and certification discipline are not.

**The common artifact families.** Engineering Contract, Engineering Registry, and Engineering Readiness Assessment are each an abstract Enterprise Engineering artifact type with, currently, two specializations apiece:

```
Enterprise Engineering Artifact (abstract)
├── Engineering Contract
│   ├── Business Activity Contract (BAC) ............ §6.7
│   └── Runtime Component Contract (RCC) ............ §13.20
├── Engineering Registry
│   ├── Business Activity Registry (BAR) ............ §6.22
│   └── Runtime Component Registry (RCR) ............ §13.22
└── Engineering Readiness Assessment
    ├── Implementation Readiness Assessment (IRA) .... capability-scoped
    └── Runtime Readiness Assessment (RRA) ........... §13.23
```

No existing artifact — BAC, BAR, or IRA — is redefined, restructured, or renamed by this abstraction. §6.7, §6.22, and §6.23 remain exactly as written; this diagram states only that they are, in retrospect, the Business Activity specialization of a pattern Runtime Component Engineering now specializes a second time.

**Permanent extension point.** This Section is designed to accommodate further specializations without amendment to this framework and without a new top-level chapter or a new canonical document: Integration Engineering, Data Pipeline Engineering, AI Runtime Engineering, Workflow Runtime Engineering, and others not yet named are each added as a further `§13.N` range following this same recipe — its own Contract, Registry, and Readiness Assessment, reusing the common lifecycle, governance, review, Completion Gate, and Certification discipline stated above. Should a future domain of implementable units prove genuinely incapable of fitting this specialization model, that is itself a determination to be made at that time, against that domain's own evidence — it is not assumed or foreclosed here.

**13.18 Runtime Component Engineering — Purpose**

This specialization engineers RTA-001's Runtime Components: Business Activity Runtime (§6), Workflow Runtime (§7), Event Runtime (§8), Metadata Runtime (§9), Enterprise Context Runtime (§10), Authorization Runtime (§11), Transaction Runtime (§14), Caching & Performance Runtime (§15), Integration Runtime (§16), Observability Runtime (§17), Failure & Recovery Runtime (§18), and Deployment Runtime (§19). It excludes the Knowledge Graph, AI, and Memory Runtime Components (RTA-001 §§12, 13, 21), which remain Enterprise Intelligence Engineering's own scope (§§13.2-13.16) and are not re-engineered here.

Per §13.17, this is a specialization of Enterprise Engineering, not a separate discipline. It does not redefine RTA-001 (Runtime Architecture remains RTA-001's sole authority), Master Technical Architecture, or any Business Activity — each Runtime Component pattern below cites the RTA-001 section it implements rather than restating it, exactly as §§13.2-13.16 already do for RTA-001 §§12/13/21/22.

**13.19 Runtime Component Model**

A Runtime Component is the implementable realization of one RTA-001 Runtime section. Every Runtime Component has:

- **Runtime Domain** — the owning RTA-001 section (e.g., §9, Metadata Runtime).
- **Runtime Responsibilities** — consumed by reference from that section's own Runtime Responsibilities table, never restated.
- **Runtime Position** — consumed by reference from that section's own Runtime Position statement.
- **Architectural Guarantees** — consumed by reference from that section's own Architectural Guarantees.

This model describes engineering shape only. It does not redefine architecture — RTA-001 remains the sole authority for what each Runtime Component is and how it behaves; this Section states only how an engineer builds it, mirroring the boundary §13.1 already draws for Enterprise Intelligence's own Runtime Components.

**13.20 Runtime Component Contract (RCC)**

Every Runtime Component shall have a Runtime Component Contract, the Runtime Component specialization of Engineering Contract (§13.17):

  -----------------------------------------------------------------------
  **Attribute**              **Description**
  -------------------------- --------------------------------------------
  Component Identifier       Unique ID

  Runtime Domain              Owning RTA-001 section (§13.19)

  Component Type              Category

  Runtime Intent               Purpose

  Runtime Responsibilities     Consumed from RTA-001 (§13.19)

  Input Contract                Required inputs

  Output Contract               Expected outputs

  Authorization                  Required permissions

  Events                          Published events

  Observability                   Required telemetry

  Dependencies                     See §13.21

  Definition of Done                Completion criteria
  -----------------------------------------------------------------------

The RCC is the authoritative specification for implementation, mirroring the role BAC (§6.7) plays for Business Activities.

**13.21 Runtime Component Dependencies**

Every Runtime Component Contract's Dependencies attribute (§13.20) is populated per this model:

- **Depends On** — every other Runtime Component this component's own behavior presumes, stated by Component Identifier.
- **Required Runtime Components** — the subset of Depends On without which this component cannot operate at all.
- **Optional Runtime Components** — the subset of Depends On this component degrades gracefully without, rather than failing.

Dependency declarations are recorded in the Runtime Component Registry (§13.22) against each component's entry, and verified during the Runtime Readiness Assessment (§13.23) before implementation begins — mirroring, generalized rather than copied, the Dependency Management principle BAR already establishes at §6.22.11 for Business Activities.

**13.22 Runtime Component Registry (RCR)**

The Runtime Component Registry is the canonical inventory of Runtime Components, analogous to BAR (§6.22) for Business Activities — an independent registry, not an extension of BAR, per the same one-concern-one-owner discipline that keeps every other Engineering Registry specialization separate.

The RCR holds, for every registered Runtime Component: its Runtime Component Contract (§13.20), its dependency declarations (§13.21), and its current lifecycle status. Status is tracked here, in the registry, exactly as Business Activity status is tracked in BAR (§6.22.9) rather than left to the separate versioning discipline alone — a Runtime Component's current state is always answerable by querying the RCR directly.

Lifecycle status reuses the same six states already governing Business Activities (§6.23) — **Draft, Registered, Approved, Active, Deprecated, Retired** — applied here to Runtime Components. No new state model is introduced; only Approved and Active Runtime Components are available for consumption by a Business Activity or another Runtime Component.

Registry governance and observability follow the same principles §6.22.12 (Registry Governance) and §6.22.13 (Registry Observability) already establish for BAR, generalized to Runtime Components rather than restated.

**13.23 Runtime Readiness Assessment (RRA)**

Every Runtime Component shall undergo a Runtime Readiness Assessment before implementation begins, occupying the same lifecycle position an Implementation Readiness Assessment occupies for a Business Activity — produced first, gating what follows.

An RRA's assessment criteria are Runtime-specific and do not reuse IRA's own Capability-shaped sections (Capability Assessment, Business Activity Assessment, UI Impact Matrix), which do not apply to a Runtime Component:

- Runtime Responsibilities (per §13.19's consumption from RTA-001)
- State Management
- Configuration
- Thread Safety
- Failure Behaviour
- Recovery
- Observability
- Performance
- Scalability
- Dependency Readiness (verified against §13.21's declarations)
- Runtime Guarantees (per §13.19's Architectural Guarantees)

**13.24 Runtime Component Versioning**

Runtime Components follow the same Version Lifecycle and Canonical Version Model already defined at §6.23, applied to Runtime Components rather than Business Activities. No new lifecycle or version model is introduced here.

**13.25 Runtime Component Review, Completion Gate, and Certification**

Every Runtime Component is subject to the same Independent Review, Completion Gate, and Certification discipline CLAUDE.md §19.7 already establishes for Business Activities, substituting "Runtime Component" for "Business Activity" throughout that section's requirements — including that the implementation agent shall not certify its own work, and that no further Runtime Component's implementation shall begin until the current one has passed this same gate. This section references that discipline; it does not restate, redefine, or relocate it.

---

**Appendix B — WP-05 Reference Pointer**

WP-05 (Access Management, C-002) is the canonical reference implementation of the Work Package Closure & Release Gate Sequence defined at §2.13a. The full retrospective — execution statistics, defects discovered, V&V findings, and the methodology improvements they justified — is recorded once, in `METH-002_WP-05_Engineering_Methodology_Improvements.md`, and is not restated here. This document's own §2.13a states the adopted rule; `METH-002` is the sole source for the evidence and history behind it, per this repository's own single-authoritative-source discipline.

---

