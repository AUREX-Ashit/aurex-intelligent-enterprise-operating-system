# =============================================================================
# AUREX Enterprise Operating System
#
# ROI-001
# Master Architecture Discovery Prompt
#
# Repository Owner Instruction
#
# Version: 1.0
#
# Status:
# Canonical
#
# =============================================================================

# Repository Owner Instruction

This instruction authorizes an Architecture Discovery exercise.

It is intended to determine whether the current repository architecture
requires architectural evolution.

The objective is NOT to redesign the platform.

The objective is NOT to invent new capabilities.

The objective is NOT to modernize documentation.

The objective is NOT to perform implementation.

The objective is to determine, strictly from repository evidence, whether
the existing architecture has naturally evolved to require refinement,
extension or consolidation.

Architecture shall be derived.

Architecture shall never be invented.

Repository evidence always takes precedence over assumption.

===============================================================================
CORE PRINCIPLES
===============================================================================

The repository is the single source of truth.

Every architectural recommendation shall be derived from:

• approved repository documents

• approved architecture

• approved capabilities

• approved implementation

• approved governance

No recommendation may contradict an approved architectural decision
unless repository evidence demonstrates that the previous decision is no
longer internally consistent.

Where possible:

Prefer evolution.

Avoid replacement.

Prefer extension.

Avoid duplication.

Prefer consolidation.

Avoid architectural proliferation.

===============================================================================
DISCOVERY PHILOSOPHY
===============================================================================

This exercise exists to answer one question only.

"Has the architecture naturally evolved to require a new architectural
concept?"

Do NOT attempt to create architecture because an idea appears useful.

Do NOT introduce concepts simply because they are modern.

Do NOT recommend new components because they are fashionable.

Instead:

Observe.

Analyse.

Derive.

Validate.

Only then recommend.

===============================================================================
ARCHITECTURAL DISCIPLINE
===============================================================================

Every recommendation shall satisfy all of the following:

1.
Repository evidence exists.

2.
The recommendation solves a demonstrated architectural problem.

3.
The recommendation reduces complexity.

4.
The recommendation increases consistency.

5.
The recommendation avoids duplication.

6.
The recommendation improves Enterprise Experience.

7.
The recommendation improves Executive Experience.

8.
The recommendation aligns with the Enterprise Intelligence Fabric.

9.
The recommendation aligns with Implementation Methodology v2.

10.
The recommendation aligns with the Product Roadmap.

If any criterion cannot be demonstrated,
the recommendation shall not be made.

===============================================================================
AUTHORITATIVE SOURCES
===============================================================================

The repository remains the only authoritative source.

Use every approved document that is materially relevant.

Typical sources include (but are not limited to):

• CAP-001

• PE-001

• SD-001

• DS-001

• IMP-001

• SER-001

• METH-003

• CLAUDE.md

• Product Milestone Roadmap

• Architecture Evolution Roadmap

• Architecture Evolution Implementation Programme

• Approved ADRs

• Approved IRAs

• Approved Work Package Charters

• Implementation Reports

• Certification Reports

• Validation Reports

• Repository Governance Documents

Reuse repository knowledge wherever possible.

Do NOT perform unnecessary repository-wide reviews.

Do NOT duplicate previous investigations unless repository evidence has
materially changed.

===============================================================================
GENERAL DISCOVERY RULES
===============================================================================

Throughout this exercise:

Prefer extending existing architecture.

Prefer reusing existing Business Objects.

Prefer reusing existing Capabilities.

Prefer reusing existing Services.

Prefer reusing existing Workflows.

Prefer reusing existing Enterprise Experience.

Prefer reusing existing Executive Experience.

Do not create duplicate architectural concepts.

Do not create parallel architectures.

Do not silently redefine approved terminology.

Every conclusion shall include repository evidence.

===============================================================================
STOP CONDITIONS
===============================================================================

This section authorizes discovery only.

No implementation shall occur.

No code shall be written.

No architecture shall be modified.

No implementation artefacts shall be created.

No capabilities shall be redesigned.

No roadmap shall be modified.

No implementation shall begin.

Proceed to the Discovery Phases.

===============================================================================
DISCOVERY METHODOLOGY
===============================================================================

Every Architecture Discovery exercise shall follow the same canonical
methodology.

The objective is to ensure that architectural evolution is always
evidence-based, repeatable, traceable and independently verifiable.

No discovery exercise may skip any phase unless the Repository Owner
explicitly authorizes doing so.

===============================================================================
PHASE 1 — PROBLEM DEFINITION
===============================================================================

Clearly define the architectural question to be answered.

The problem statement shall identify:

• Current architectural concern

• Business concern

• Enterprise concern

• Executive concern

• Repository concern

• Scope

• Out of scope

Do not assume the problem statement is correct.

Validate the problem statement against repository evidence.

If the problem statement is invalid,
document the finding before continuing.

===============================================================================
PHASE 2 — CURRENT ARCHITECTURE ASSESSMENT
===============================================================================

Determine how the repository currently solves the problem.

Review every materially relevant architectural document.

Identify:

• Existing capabilities

• Existing business objects

• Existing services

• Existing workflows

• Existing registries

• Existing governance

• Existing implementation

• Existing user experience

Do not recommend anything during this phase.

Only document the current architecture.

===============================================================================
PHASE 3 — ARCHITECTURAL GAP ANALYSIS
===============================================================================

Determine whether the current architecture contains:

• Functional gaps

• Structural gaps

• Governance gaps

• Enterprise Experience gaps

• Executive Experience gaps

• Implementation gaps

• Strategic Enhancement gaps

• Traceability gaps

For every identified gap:

Provide repository evidence.

Do not infer gaps without evidence.

===============================================================================
PHASE 4 — ARCHITECTURAL CONSOLIDATION
===============================================================================

Determine whether the identified responsibilities already exist elsewhere
within the repository.

Before recommending any new architectural concept determine whether the
problem can instead be solved by:

• Extending an existing capability

• Extending an existing business object

• Extending an existing registry

• Extending an existing workflow

• Extending an existing Enterprise Experience

• Extending an existing Executive Experience

Architecture shall always prefer consolidation over expansion.

===============================================================================
PHASE 5 — EVOLUTION OPTIONS
===============================================================================

Where architectural evolution appears justified,
identify every viable option.

Examples:

Option 1

No change.

Option 2

Minor enhancement.

Option 3

Capability extension.

Option 4

Business object extension.

Option 5

Registry consolidation.

Option 6

Canonical architectural evolution.

Do not recommend a preferred option yet.

===============================================================================
PHASE 6 — IMPACT ANALYSIS
===============================================================================

For every option evaluate impact on:

• Enterprise Architecture

• Business Capabilities

• Business Objects

• Services

• APIs

• Data Model

• Enterprise Experience

• Executive Experience

• Design System

• Presentation Architecture

• Strategic Enhancements

• Work Packages

• Product Roadmap

• Implementation Methodology

• Governance

• Technical Debt

• Release Planning

Provide evidence for every identified impact.

===============================================================================
PHASE 7 — IMPLEMENTATION FEASIBILITY
===============================================================================

Determine whether the proposed evolution is:

• Immediately implementable

• Requires prerequisite work

• Requires governance approval

• Requires roadmap changes

• Requires capability changes

• Requires implementation methodology updates

Identify all dependencies.

Identify all implementation risks.

===============================================================================
PHASE 8 — REPOSITORY ALIGNMENT
===============================================================================

Validate alignment with:

• CAP-001

• PE-001

• SD-001

• DS-001

• IMP-001

• SER-001

• METH-003

• CLAUDE.md

• Product Roadmap

• Architecture Roadmap

• Approved ADRs

• Approved IRAs

No recommendation may contradict repository governance without explicit
repository evidence.

===============================================================================
PHASE 9 — RECOMMENDATION
===============================================================================

Recommend exactly ONE architectural direction.

Possible outcomes include:

• No Change

• Minor Refinement

• Architectural Consolidation

• Canonical Architectural Evolution

• Alternative Repository-Evidence-Based Recommendation

Provide complete justification.

Explain why every alternative was rejected.

===============================================================================
PHASE 10 — IMPLEMENTATION RECOMMENDATIONS
===============================================================================

If architectural evolution is recommended,
identify:

• Required documentation updates

• Required governance updates

• Required implementation changes

• Required Work Packages

• Required Strategic Enhancements

• Migration strategy

• Risks

This phase shall recommend implementation.

It shall never perform implementation.

===============================================================================
DISCOVERY COMPLETION
===============================================================================

Before completion verify that:

✓ Every discovery phase has been completed.

✓ Every recommendation is supported by repository evidence.

✓ No unnecessary architectural concepts have been introduced.

✓ Existing architecture has been reused wherever possible.

✓ Repository governance remains internally consistent.

Only then may the Architecture Discovery exercise proceed to its
domain-specific evaluation phases.

===============================================================================
DOMAIN-SPECIFIC DISCOVERY
===============================================================================

The previous sections establish the canonical Architecture Discovery
Methodology.

This section defines the architecture domain that shall be evaluated.

The Repository Owner shall clearly identify the architectural domain
before discovery begins.

Examples include:

• Enterprise Intelligence Exchange

• Enterprise Search

• Enterprise Discovery

• Executive Cognition

• Enterprise Memory

• Enterprise AI Governance

• Enterprise Configuration

• Marketplace

• Identity Federation

• Knowledge Fabric

• AI Agent Orchestration

The discovery process shall remain identical.

Only the architectural domain changes.

===============================================================================
DOMAIN OBJECTIVES
===============================================================================

Clearly define the architectural objective.

Examples include:

Determine whether the repository now requires a canonical Enterprise
Intelligence Exchange.

Determine whether Executive Cognition requires its own canonical
architecture.

Determine whether AI Governance should evolve into a first-class
Business Capability.

Determine whether Enterprise Memory should become part of the Enterprise
Intelligence Fabric.

Do not assume the answer.

Derive the answer.

===============================================================================
DOMAIN SCOPE
===============================================================================

Clearly define:

In Scope

Examples

• Business capabilities

• Business objects

• Registries

• Policies

• Enterprise Experience

• Executive Experience

• Runtime architecture

• Governance

• Strategic Enhancements

Out of Scope

Examples

• Implementation

• Coding

• APIs

• Database schema

• UI implementation

• Performance optimisation

• Testing

• Deployment

Discovery shall never drift outside the defined scope.

===============================================================================
DOMAIN QUESTIONS
===============================================================================

The Repository Owner shall explicitly define the questions to be answered.

Examples

Current Architecture

How does the repository currently solve this problem?

Business Objects

Which Business Objects currently exist?

Capabilities

Which Capabilities currently own these responsibilities?

Enterprise Experience

How is the Enterprise Experience currently realised?

Executive Experience

How is the Executive Experience currently realised?

Governance

Which governance documents already define this area?

Strategic Enhancements

Which Strategic Enhancements already support this architecture?

Roadmap

How does this affect future Releases and Work Packages?

===============================================================================
DOMAIN ANALYSIS
===============================================================================

For the selected architecture domain determine:

Current Responsibilities

Current Ownership

Current Governance

Current Runtime

Current User Experience

Current Executive Experience

Current Technical Architecture

Current Strategic Enhancements

Current Implementation Status

Current Technical Debt

Determine whether:

Responsibilities overlap.

Responsibilities conflict.

Responsibilities are duplicated.

Responsibilities are fragmented.

Responsibilities are missing.

Provide repository evidence for every finding.

===============================================================================
DOMAIN CONSOLIDATION
===============================================================================

Before recommending any new architectural concept determine whether the
architecture can instead evolve by extending existing repository assets.

Evaluate:

Existing Business Objects

Existing Capabilities

Existing Registries

Existing Runtime Components

Existing Enterprise Experience

Existing Executive Experience

Existing Governance

Existing Work Packages

Existing Strategic Enhancements

Existing Roadmap

Architecture shall always prefer:

Extension

Consolidation

Reuse

Simplification

Avoid:

Duplication

Parallel architectures

Competing models

Redundant registries

===============================================================================
CANONICAL ARCHITECTURE TEST
===============================================================================

Only if repository evidence demonstrates that the current architecture
cannot adequately solve the identified problem shall a canonical
architectural evolution be recommended.

The proposed architecture shall demonstrate:

A single source of truth.

Clear ownership.

Clear governance.

Clear runtime responsibility.

Clear Business Objects.

Clear Business Capabilities.

Clear Enterprise Experience.

Clear Executive Experience.

Clear implementation roadmap.

Clear traceability.

===============================================================================
DISCOVERY OUTPUT
===============================================================================

The Architecture Discovery shall produce:

1. Current Repository Assessment

2. Architectural Findings

3. Gap Analysis

4. Consolidation Opportunities

5. Business Object Assessment

6. Capability Assessment

7. Enterprise Experience Assessment

8. Executive Experience Assessment

9. Governance Assessment

10. Strategic Enhancement Assessment

11. Roadmap Assessment

12. Final Recommendation

The recommendation shall always include repository evidence.

No architectural recommendation shall rely solely upon opinion,
preference or industry trend.

===============================================================================
DOMAIN COMPLETION
===============================================================================

When the Architecture Discovery concludes:

The Repository Owner may either:

Accept the recommendation.

Reject the recommendation.

Request further investigation.

Authorize architectural evolution.

Authorize implementation planning.

Discovery itself never authorizes implementation.

===============================================================================
ARCHITECTURAL EVALUATION FRAMEWORK
===============================================================================

Every Architecture Discovery exercise shall evaluate the selected
architecture domain using the same canonical Enterprise Architecture
framework.

The objective is to ensure that every recommendation is evaluated from
all relevant architectural perspectives rather than only from a
technical viewpoint.

No perspective may be omitted without Repository Owner approval.

===============================================================================
BUSINESS ARCHITECTURE
===============================================================================

Determine the impact on Business Architecture.

Evaluate:

Business Vision

Business Strategy

Business Goals

Business Outcomes

Business Capabilities

Business Activities

Business Processes

Business Objects

Business Events

Business Rules

Business Policies

Business Stakeholders

Business Roles

Business Responsibilities

Business Ownership

Business Lifecycle

Business Value

Determine whether the proposed architecture:

Introduces new Business Capabilities.

Extends existing Business Capabilities.

Consolidates existing Business Capabilities.

Creates duplicated responsibilities.

Violates capability ownership.

Provide repository evidence.

===============================================================================
INFORMATION ARCHITECTURE
===============================================================================

Determine the impact on Information Architecture.

Evaluate:

Enterprise Information

Knowledge Assets

Enterprise Memory

Evidence

Metadata

Reference Data

Master Data

Taxonomy

Ontology

Classification

Vocabulary

Terminology

Semantic Models

Knowledge Graph

Vector Knowledge

Structured Data

Unstructured Data

Determine:

Which information becomes canonical.

Who owns the information.

How information flows.

How information is governed.

How information is versioned.

===============================================================================
APPLICATION ARCHITECTURE
===============================================================================

Determine the impact on Application Architecture.

Evaluate:

Applications

Services

Microservices

Modules

Registries

Workspaces

Runtime Components

User Interfaces

Enterprise APIs

Integration APIs

AI Components

Workflow Engines

Reasoning Engines

Marketplace Components

Connector Components

Determine:

Service ownership.

Application ownership.

Interaction patterns.

Runtime dependencies.

Avoid duplicated services.

===============================================================================
TECHNOLOGY ARCHITECTURE
===============================================================================

Determine the impact on Technology Architecture.

Evaluate:

Cloud Services

Storage

Databases

Vector Databases

Knowledge Stores

Search Engines

Event Bus

Queues

Streaming

Caching

Security

Identity

Secrets

Networking

Observability

Monitoring

Logging

Performance

Scalability

Availability

Reliability

Disaster Recovery

Do not redesign technology.

Only identify architectural implications.

===============================================================================
DATA GOVERNANCE
===============================================================================

Determine:

Data ownership.

Data stewardship.

Data lineage.

Data quality.

Data lifecycle.

Data residency.

Retention.

Archival.

Evidence provenance.

Determine whether governance changes are required.

===============================================================================
SECURITY ARCHITECTURE
===============================================================================

Determine:

Authentication.

Authorization.

Identity.

Tenant isolation.

Secrets.

Credential management.

Zero Trust.

Least privilege.

Audit.

Compliance.

Privacy.

Encryption.

Certificate management.

Security monitoring.

Incident response.

Determine whether the proposed architecture introduces new security
responsibilities.

===============================================================================
AI ARCHITECTURE
===============================================================================

Determine:

AI Providers.

LLM Providers.

Embedding Models.

Reasoning Engines.

Prompt Management.

Prompt Templates.

Tool Registry.

MCP Servers.

Agent Framework.

Multi-Agent Orchestration.

AI Governance.

AI Safety.

AI Observability.

AI Cost Management.

AI Policies.

AI Explainability.

Evidence Traceability.

Confidence Scoring.

Determine whether AI architecture remains consistent.

===============================================================================
ENTERPRISE EXPERIENCE
===============================================================================

Evaluate impact on:

PE-001

Enterprise Workspaces

Navigation

Information Architecture

Workflow

Productivity

Discover First

Evidence First

Progressive Disclosure

Minimal Cognitive Load

Accessibility

Enterprise Branding

Localization

Configuration

White Label

Determine whether Enterprise Experience improves.

===============================================================================
EXECUTIVE EXPERIENCE
===============================================================================

Evaluate:

Executive Cognition.

Decision Support.

Enterprise Intelligence.

Strategic Insights.

Executive Dashboards.

Executive Summaries.

Explainability.

Evidence Traceability.

Cross-enterprise Visibility.

Enterprise DNA.

Adaptive Experience.

Sacred 12.

Determine whether Executive Experience improves.

===============================================================================
IMPLEMENTATION ARCHITECTURE
===============================================================================

Evaluate:

Implementation Methodology.

Work Packages.

Implementation Reports.

Certification.

Validation.

Verification.

Technical Debt.

Release Readiness.

Roadmap.

Migration.

Dependencies.

Determine implementation feasibility.

===============================================================================
COMMERCIAL ARCHITECTURE
===============================================================================

Evaluate:

Licensing.

Subscriptions.

Marketplace.

Usage Pricing.

AI Credits.

Cost Centres.

Budgets.

Department Chargeback.

Bring Your Own Licence.

Commercial Governance.

Marketplace Certification.

Marketplace Publishing.

Marketplace Versioning.

Marketplace Retirement.

Determine commercial viability.

===============================================================================
ARCHITECTURAL QUALITY ATTRIBUTES
===============================================================================

Every recommendation shall be evaluated against:

Simplicity

Maintainability

Scalability

Security

Performance

Availability

Reliability

Extensibility

Configurability

Observability

Auditability

Governability

Explainability

Usability

Accessibility

Enterprise Readiness

Executive Readiness

Operational Readiness

Commercial Readiness

Global Readiness

The recommendation shall explicitly state whether each quality
attribute is improved, unchanged or degraded.

===============================================================================
ARCHITECTURAL COMPLETENESS CHECK
===============================================================================

Before proceeding to recommendations verify:

✓ Business Architecture evaluated

✓ Information Architecture evaluated

✓ Application Architecture evaluated

✓ Technology Architecture evaluated

✓ Security Architecture evaluated

✓ AI Architecture evaluated

✓ Enterprise Experience evaluated

✓ Executive Experience evaluated

✓ Commercial Architecture evaluated

✓ Implementation Architecture evaluated

✓ Quality Attributes evaluated

Only after all perspectives have been evaluated may architectural
recommendations be produced.

===============================================================================
DISCOVERY DELIVERABLES, GOVERNANCE & COMPLETION
===============================================================================

Every Architecture Discovery exercise shall produce a complete,
evidence-based architectural recommendation.

The recommendation shall become the basis for Repository Owner decision
making.

Architecture Discovery itself shall never modify the repository.

===============================================================================
MANDATORY DELIVERABLES
===============================================================================

The Discovery shall produce a Review Document containing, at minimum,
the following sections.

1.
Executive Summary

2.
Problem Statement

3.
Discovery Scope

4.
Current Repository Assessment

5.
Architectural Findings

6.
Repository Evidence

7.
Business Architecture Assessment

8.
Information Architecture Assessment

9.
Application Architecture Assessment

10.
Technology Architecture Assessment

11.
Security Architecture Assessment

12.
AI Architecture Assessment

13.
Enterprise Experience Assessment

14.
Executive Experience Assessment

15.
Commercial Architecture Assessment

16.
Implementation Architecture Assessment

17.
Strategic Enhancement Assessment

18.
Repository Governance Assessment

19.
Architectural Gap Analysis

20.
Consolidation Opportunities

21.
Canonical Business Objects

22.
Capability Assessment

23.
Implementation Roadmap Impact

24.
Release Impact

25.
Work Package Impact

26.
Risk Assessment

27.
Alternative Architectural Options

28.
Recommended Architectural Direction

29.
Repository Update Recommendations

30.
Final Recommendation

===============================================================================
MANDATORY VALIDATION
===============================================================================

Before presenting the recommendation verify that:

✓ Every discovery phase has completed.

✓ Every architectural perspective has been evaluated.

✓ Every recommendation is supported by repository evidence.

✓ Every recommendation has complete traceability.

✓ No recommendation contradicts approved architecture.

✓ Existing architecture has been reused wherever possible.

✓ Architectural duplication has been avoided.

✓ Enterprise Experience has been considered.

✓ Executive Experience has been considered.

✓ Strategic Enhancements have been considered.

✓ Implementation Methodology has been considered.

Only after successful validation may the recommendation be presented.

===============================================================================
REPOSITORY UPDATE RULES
===============================================================================

Architecture Discovery shall not directly modify canonical repository
documents unless explicitly authorized by the Repository Owner.

If architectural evolution is recommended, identify exactly which
repository artefacts require update.

Examples include:

• CAP-001

• PE-001

• SD-001

• DS-001

• IMP-001

• SER-001

• METH-003

• Product Milestone Roadmap

• Architecture Evolution Roadmap

• Architecture Evolution Implementation Programme

• ADRs

• IRAs

• Work Package Charters

• Implementation Reports

• Documentation Catalogue

Only recommend updates.

Do not perform them.

===============================================================================
REPOSITORY OWNER DECISION
===============================================================================

The Architecture Discovery concludes with one of the following outcomes.

Outcome 1

No architectural evolution required.

Outcome 2

Minor architectural refinement recommended.

Outcome 3

Canonical architectural evolution recommended.

Outcome 4

Further investigation required.

Outcome 5

Repository evidence is insufficient to reach a conclusion.

The Repository Owner shall decide whether to:

Accept

Reject

Request clarification

Request further investigation

Authorize architectural evolution

Authorize implementation planning

Architecture Discovery never authorizes implementation.

===============================================================================
IMPLEMENTATION AUTHORIZATION
===============================================================================

If the Repository Owner accepts the recommendation,
implementation shall occur only through the approved repository
governance process.

Typical sequence:

Architecture Discovery

↓

Repository Owner Decision

↓

Architecture Update (if required)

↓

ADR (if required)

↓

Capability Update (if required)

↓

Strategic Enhancement Update (if required)

↓

Roadmap Update (if required)

↓

Work Package Charter

↓

Implementation Readiness Assessment (IRA)

↓

Implementation Authorization

↓

Implementation

↓

Verification

↓

Validation

↓

Certification

↓

Release Readiness

↓

Closure

No implementation shall commence before the appropriate governance
artefacts have been completed and approved.

===============================================================================
DISCOVERY SUCCESS CRITERIA
===============================================================================

A successful Architecture Discovery is one that:

Derives architecture rather than inventing it.

Reuses architecture rather than duplicating it.

Extends architecture rather than replacing it.

Simplifies architecture rather than complicating it.

Strengthens Enterprise Experience.

Strengthens Executive Experience.

Strengthens Enterprise Intelligence.

Strengthens repository governance.

Improves long-term maintainability.

Provides complete traceability.

Supports future implementation.

===============================================================================
END OF ROI-001
===============================================================================