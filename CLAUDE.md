# CLAUDE.md v2.0

> CorpStage Enterprise Operating System (EOS)
>
> AI Engineering Guide for Claude Code

------------------------------------------------------------------------

# 1. Repository Mission

This repository implements the CorpStage Enterprise Operating System
(EOS).

Claude Code is an engineering partner responsible for producing
production-quality, maintainable, secure, and testable software while
preserving architectural integrity.

Do not duplicate architecture documentation. Use this guide to determine
how to work within the repository.

------------------------------------------------------------------------

# 2. Enterprise Engineering Philosophy

Always:

-   Preserve architecture before implementing features.
-   Extend before creating.
-   Search before implementing.
-   Reuse before duplicating.
-   Prefer capability-driven design.
-   Keep services cohesive.
-   Keep implementations testable.
-   Keep business logic framework-independent.
-   Leave the repository in a better state.

------------------------------------------------------------------------

# 3. Repository Intelligence

## architecture/

Authoritative engineering knowledge.

-   00-Governance --- repository governance and architecture manifest.
-   01-Blueprint --- enterprise capabilities.
-   02-Constitutional --- canonical enterprise rules and models.
-   03-Engineering --- implementation methodology.
-   04-Technical --- technical architecture.
-   05-Implementation --- implementation specifications.
-   06-Reviews --- architecture reviews.
-   07-Decisions --- Architecture Decision Records.
-   99-Archive --- historical material.

## cil/

Canonical enterprise vocabulary.

Consult before introducing:

-   entities
-   attributes
-   KPIs
-   metrics
-   dimensions
-   hierarchies
-   business terminology

Industry Packs extend the CIL. They never replace canonical concepts.

## source/

-   backend --- business logic
-   frontend --- presentation
-   database --- schema and migrations
-   infrastructure --- deployment
-   scripts --- automation
-   tests --- verification

## prompts/

Reusable engineering prompts and templates.

## docs/

Supporting documentation.

------------------------------------------------------------------------

# 4. Repository Navigation

For every request:

1.  Understand the requirement.
2.  Search architecture.
3.  Search decisions.
4.  Search CIL.
5.  Search existing source code.
6.  Extend existing implementation where possible.
7.  Implement.
8.  Test.
9.  Review.
10. Commit.

------------------------------------------------------------------------

# 5. Development Lifecycle

Requirement → Architecture → Existing Code → Design → Implement → Test →
Review → Commit

Never skip validation.

------------------------------------------------------------------------

# 6. Enterprise Modeling Rules

Canonical concepts must remain independent.

-   Organization defines the tenant boundary.
-   Person represents a human.
-   Identity represents authentication.
-   Membership links Person and Organization.
-   Role groups permissions.
-   Permission authorizes actions.

Never merge or duplicate these concepts.

------------------------------------------------------------------------

# 7. Business Activity Rules

Business Activities are the primary implementation unit.

Each Business Activity must:

-   have one purpose
-   be reusable
-   be testable
-   be observable
-   produce deterministic outcomes

Search existing Business Activities before creating new ones.

------------------------------------------------------------------------

# 8. Service Design Rules

Each capability has one owning service.

Never:

-   duplicate business logic
-   bypass service boundaries
-   access another service's database
-   couple unrelated domains

Communicate through APIs or events.

------------------------------------------------------------------------

# 9. Technology Standards

Backend: - Python - FastAPI - SQLAlchemy - Alembic - Pydantic

Frontend: - Next.js - React - TypeScript

Platform: - PostgreSQL - Redis - Docker - Azure OpenAI

Do not introduce alternative frameworks without approval.

------------------------------------------------------------------------

# 10. Coding Standards

-   Use strong typing.
-   Keep functions focused.
-   Keep modules cohesive.
-   Remove dead code.
-   Avoid unnecessary abstractions.
-   Prefer explicit contracts.
-   Never hardcode secrets.
-   Fail fast.
-   Write self-documenting code.

------------------------------------------------------------------------

# 11. Testing & Quality

Every change requires appropriate tests.

Verify:

-   business rules
-   APIs
-   persistence
-   authorization
-   tenant isolation

A failing build blocks the change.

------------------------------------------------------------------------

# 12. Architecture Integrity Rules

Before creating any:

-   service
-   API
-   entity
-   DTO
-   event
-   table
-   utility

Search the repository first.

Prefer:

Extend → Refactor → Reuse

Avoid parallel implementations.

------------------------------------------------------------------------

# 13. AI Behaviour

Claude Code should:

-   protect architecture
-   identify duplication
-   recommend reuse
-   explain architectural concerns
-   ask for clarification when requirements are ambiguous

Never invent architecture or business requirements.

------------------------------------------------------------------------

# 14. Definition of Done

A task is complete only when:

-   implementation is complete
-   architecture is respected
-   the AUREX Design System (DS-001) is respected
-   the governing Capability Specification is respected
-   tests pass
-   security is verified
-   accessibility is verified
-   performance is acceptable
-   tenant isolation is preserved
-   the change is traceable to its governing canonical documents
-   the implementation is maintainable
-   documentation is updated if required
-   build succeeds

------------------------------------------------------------------------

# 15. Golden Rules

1.  Search before creating.
2.  Extend before replacing.
3.  One capability. One owner.
4.  One business rule. One implementation.
5.  Reuse canonical models.
6.  Protect service boundaries.
7.  Test every change.
8.  Never guess.
9.  Preserve architectural integrity.
10. Leave the repository better than you found it.
11. Justify before creating.
12. One entity, one definition. One database table, one responsibility.
13. One API, one responsibility. One event, one purpose. One
    permission, one responsibility.
14. One component, one purpose. One token, one meaning. One theme,
    one behaviour.
15. One visual language. One design system.

# 16. Canonical Authority Resolution

When multiple repository documents address the same concern, determine
the canonical owner before implementation.

Use the document that owns the architectural concern.

Examples:

- Enterprise Architecture → ARCH-000
- Design language, design tokens, themes, brand architecture,
  components, accessibility, responsive behaviour, motion, and design
  governance → DS-001
- Feature behaviour → the governing Capability Specification
- Business implementation → the governing Business Activity
- Enterprise Experience → PE-001
- Capability Experience → PE-001-Cxxx
- Business Activity implementation methodology → IMP-001
- Authorization → URA-001
- Enterprise Intelligence → EIA-001
- Canonical enterprise vocabulary → CIL
- Architecture decisions → ADRs

No implementation may contradict these constitutional authorities.

Do not merge conflicting definitions.

If two canonical documents appear to conflict:

1. Stop implementation.
2. Identify the conflicting definitions.
3. Identify the declared canonical owner.
4. Review applicable ADRs.
5. Report the conflict before changing code.

Never resolve canonical architecture conflicts by assumption.

# 17. Canonical Document Compliance (Mandatory)

The CorpStage Enterprise Operating System has already completed its
Architecture and Design phases.

The repository contains the approved canonical specifications for the
platform.

These documents are the ONLY source of truth.

Before implementing any feature, capability, user journey, API,
database change or UI, Claude Code MUST:

1. Identify the canonical documents governing the requested feature.
2. Review those documents before implementation.
3. List the documents reviewed at the beginning of the implementation report.

Implementation SHALL conform to the approved documentation.

Do NOT implement functionality based on assumptions.

Do NOT infer missing architecture.

Do NOT redesign existing solutions.

If the required behaviour, structure or business rule is not explicitly
documented, if the governing architectural authority cannot be
identified, or if creation of a new artifact cannot be justified
against the existing architecture:

STOP.

Report precisely what information is missing.

Ask for clarification.

Never fill architectural or business gaps using assumptions.

Never guess. Guessing is prohibited.

Implementation follows documentation.

Documentation does not follow implementation.

------------------------------------------------------------------------

# 18. Architectural Change Control

Claude Code is an Implementation Engineer.

It is not authorised to modify the approved architecture.

Do NOT introduce:

• new entities
• new database tables
• new database columns
• new APIs
• new service boundaries
• new workflows
• new business rules
• new navigation models
• new security models
• new technology choices
• new permissions
• new AUREX components, design tokens, or themes
• new background jobs or scheduled processes
• alternative UI libraries, design systems, or token systems
• parallel component libraries
• duplicate Business Activities, APIs, or entities

unless they are explicitly documented or approved.

If implementation appears to require an architectural change:

STOP.

Explain:

• why the change appears necessary
• which canonical documents were reviewed
• which documents appear incomplete
• which APIs are affected
• which database objects are affected
• possible implementation options

Wait for approval before continuing.

Never change architecture to make implementation easier.

# 19. Implementation Start Checklist (Mandatory)

The CorpStage Enterprise Operating System has entered **Architecture
Implementation Mode**.

Enterprise Architecture (ARCH-000), the Design System (DS-001),
Capability Engineering, and Engineering Documentation are complete.
Architecture creation has ended; architecture implementation begins.

Implementation SHALL conform to the approved architecture.

Implementation SHALL NEVER redefine architecture.

Architecture SHALL NOT evolve during implementation unless explicitly
approved through the existing Architecture Decision Record (ADR)
process (`architecture/07-Decisions`).

No implementation work shall begin until the following checklist has
been completed.

-------------------------------------------------------------------------------
19.1 Identify Governing Canonical Assets
-------------------------------------------------------------------------------

Before implementing ANY feature, capability, Business Activity,
workflow, API, database change, screen, or UI component,
Claude Code MUST identify and review every governing canonical asset.

This includes, but is not limited to:

### Architecture & Design

• Architecture Documents
• Capability Documents
• Implementation Specifications
• Architecture Decision Records (ADRs)
• Canonical Information Library (CIL)

### Governance

• Rules
• Laws
• Principles
• Standards
• Guidelines
• Policies
• Conventions
• Business Rules

### Enterprise Objects

• Business Activities
• Entities
• Aggregates
• Database Tables
• Database Views
• Database Functions
• Database Columns
• Relationships
• Enumerations

### Application

• Services
• APIs
• Events
• DTOs
• Workflows
• Permissions
• Roles

### Presentation

• Screens
• User Journeys
• Widgets
• AUREX Components
• Design Tokens
• Themes
• Brand Architecture
• Colours, Typography, Spacing
• Motion and Responsive Behaviour
• Accessibility Behaviour
• Visual Hierarchy and Interaction Patterns

DS-001 is the sole authority for every item in this subsection. Claude
Code SHALL NEVER invent a component, token, theme, colour, typographic
scale, spacing value, motion behaviour, responsive behaviour,
accessibility behaviour, visual hierarchy, or interaction pattern. If
DS-001 does not define something a feature requires, Claude Code SHALL
STOP and request architectural clarification rather than inventing one.

Claude Code SHALL list the governing assets reviewed before
implementation begins.

-------------------------------------------------------------------------------
19.2 Discover Existing Assets
-------------------------------------------------------------------------------

Claude Code SHALL search the repository before creating anything.

For every requested feature, Claude Code MUST identify every existing

• Entity
• Table
• API
• Service
• Business Activity
• Workflow
• Permission
• Role
• Screen
• Component
• Design Token
• Theme
• Business Rule
• Test

already governing the requested functionality.

Failure to perform this search is an architectural violation.

For every identified asset Claude Code SHALL determine whether it is

• Reused
• Extended
• Configured
• Referenced

Creation of new assets is the last option.

-------------------------------------------------------------------------------
19.3 Gap Analysis
-------------------------------------------------------------------------------

Before implementation, Claude Code SHALL produce a Gap Analysis.

The analysis SHALL identify

• Existing assets that satisfy the requirement

• Existing assets requiring extension

• Missing architecture

• Missing documentation

• Potential conflicts

• Why each existing asset cannot satisfy the requirement as-is

• Why extension of an existing asset is insufficient, where applicable

• Why creation of a new artifact is architecturally necessary, if
  proposed

Claude Code SHALL NOT create a new artifact unless this justification
is demonstrated. Creation is always the final option, never the first.

-------------------------------------------------------------------------------
19.4 Architectural Impact Assessment
-------------------------------------------------------------------------------

If implementation appears to require

• new entities

• new database tables

• new database columns

• new APIs

• new services

• new Business Activities

• new workflows

• new permissions

• new events

• new screens

• new UI components

• changes to canonical business rules

Claude Code SHALL STOP.

Claude Code SHALL NOT implement the change.

Instead Claude Code SHALL report

• why the change appears necessary

• which canonical documents were reviewed

• which existing assets were evaluated

• which architecture is affected

• available implementation options

Wait for approval before continuing.

-------------------------------------------------------------------------------
19.5 Implementation Rules
-------------------------------------------------------------------------------

Only after Sections 19.1 through 19.4 have completed successfully
may implementation begin.

Claude Code SHALL always follow this order

Reuse

↓

Configure

↓

Extend

↓

Compose

↓

Create

Claude Code SHALL prefer improving an existing implementation over
creating a parallel implementation.

-------------------------------------------------------------------------------
19.6 Compliance Verification
-------------------------------------------------------------------------------

After implementation Claude Code SHALL verify

✓ Architecture remains unchanged

✓ Existing Business Rules remain unchanged

✓ Existing Laws remain unchanged

✓ Existing Principles remain unchanged

✓ Existing Guidelines remain unchanged

✓ Existing Standards remain unchanged

✓ Existing Policies remain unchanged

✓ Existing Conventions remain unchanged

✓ Existing database tables were reused where applicable

✓ Existing APIs were reused where applicable

✓ Existing Business Activities were reused where applicable

✓ Existing AUREX components were reused where applicable

✓ Existing Design Tokens were reused where applicable

✓ Existing Themes were reused where applicable

✓ DS-001 (Design System) compliance maintained

✓ ARCH-000 (Enterprise Architecture) compliance maintained

✓ Reuse was proven impossible before any creation

✓ Extension was proven insufficient before any creation

✓ Architectural justification was recorded for every new artifact

✓ Tests were updated

✓ Documentation was updated

✓ No undocumented architecture was introduced

If any verification fails,

STOP

and report the violation.

-------------------------------------------------------------------------------
Golden Rule
-------------------------------------------------------------------------------

Implementation follows Architecture.

Implementation SHALL NEVER change

• Architecture

• Rules

• Laws

• Principles

• Standards

• Guidelines

• Policies

• Conventions

• Canonical Business Rules

• Canonical Data Model

• Canonical APIs

• Canonical User Experience

• Canonical Design System

Code is an implementation of the Enterprise Operating System.

Code is NEVER the source of truth.

The approved architecture and canonical documentation remain the
single source of truth.

-------------------------------------------------------------------------------
19.7 Business Activity Completion Gate (Mandatory)
-------------------------------------------------------------------------------

Every Business Activity (BA) SHALL be completed through the full
engineering lifecycle before implementation of the next Business
Activity begins.

A Business Activity SHALL be considered complete only when ALL of the
following conditions have been satisfied.

Implementation

✓ Production-quality implementation is complete.

✓ All required unit, integration and API tests pass.

✓ The Work Package Implementation Report
  (IMP-REPORT-WP-XX) has been updated.

✓ Implementation Status is marked
  "IMPLEMENTATION COMPLETE".

Independent Review

✓ The completed implementation has been submitted for
  independent review.

✓ Review observations (if any) have been addressed.

✓ The implementation has been accepted through
  independent review.

Repository

✓ The accepted implementation has been committed to the repository.

Only after these completion gates have been satisfied may
implementation of the next Business Activity begin.

Claude Code SHALL NOT begin implementation of a new Business Activity
while the current Business Activity:

• is still under implementation

• is awaiting review

• requires remediation

• has not been accepted

• has not been committed

This completion gate is mandatory for every Work Package.

-------------------------------------------------------------------------------
Implementation Reporting & Independent Certification
-------------------------------------------------------------------------------

Implementation Reports (IMP-REPORT-WP-XX) record the implementation
progress, evidence, and status of each Business Activity throughout the
Work Package.

They are maintained by the implementation agent and form the
implementation audit trail.

Implementation Reports SHALL NOT be used as certification artifacts.

Independent Certification (CERT-WP-XX) is a separate governance activity
performed only after completion of the Work Package.

The implementation agent SHALL NOT certify its own work.

Certification SHALL be performed independently using the approved
architecture, implementation reports, source code, tests, APIs,
database migrations, and other implementation evidence.

Only an independently certified Work Package shall be considered
complete.