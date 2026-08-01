# CLAUDE.md v2.0

> Aurex Enterprise Operating System (EOS)
>
> AI Engineering Guide for Claude Code

------------------------------------------------------------------------

# 1. Repository Mission

This repository implements the Aurex Enterprise Operating System
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

-   frontend --- presentation

`source/backend`, `source/database`, `source/infrastructure`,
`source/scripts`, and `source/tests` exist as empty placeholder
directories only. Actual implementation lives elsewhere in the
repository:

-   Backend/ --- business logic (Backend/Services/* per service,
    Backend/Runtime/AuthorizationEngine, Backend/Shared/* shared
    platform framework)
-   database/ --- schema and migrations (repo root; each service under
    Backend/Services/* also carries its own alembic/ migration chain)

Corrected per Release A1 (Foundation Repairs), 2026-08-01 — this section
previously stated `source/backend`/`source/database` as the business
logic and schema locations; direct verification found both empty and
the real implementation at the paths above.

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
-   the Enterprise Experience Standard (§20) is satisfied, where applicable
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

The Aurex Enterprise Operating System has already completed its
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

The Aurex Enterprise Operating System has entered **Architecture
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

**Worked example (formalized per ADR-014 — METH-001):** WP-04's BA-08
("Complete Structural Transition") illustrates this rule at the
minimum-scope decision point. Three implementation scopes were
identified — Option A (produce Resulting Structural Context only, no
`organization_nodes` mutation), Option B (also mutate
`organization_nodes` directly), Option C (also create new
`organization_hierarchy`/`consolidation_determination` tables). Option A
was selected because it is the smallest scope that satisfies the
governing Enterprise Experience's own Produced Context without inventing
an ERG-001 structural-mutation mechanism nowhere documented in canonical
architecture — Options B and C would each have required exactly the kind
of undocumented new database object §18 and §19.4 already prohibit. The
deferred mutation mechanism was disclosed as Technical Debt (`TD-070`)
rather than silently built. This is the Reuse → Configure → Extend →
Compose → Create order applied to a scope decision, not only to a
build-vs-reuse decision: the smallest sufficient option in that order is
the correct one, and what it deliberately excludes is disclosed, not
hidden.

**Second worked example — defect remediation (formalized per ADR-017 —
METH-002):** WP-05's own F-01 remediation (an Access Evaluation Outcome
write attempted for a Membership that did not exist, violating a
non-nullable foreign key) illustrates the same Reuse → Configure →
Extend → Compose → Create order applied to fixing an already-shipped
defect, not only to scoping a not-yet-built feature. Three remediation
shapes were identified — (a) narrow the code path so the invalid case
becomes structurally unreachable, matching the pre-existing
domain-not-found precedent already present in the same method; (b) make
the foreign key nullable; (c) wrap the write in a `try`/`except`
handler that catches the resulting database error after it occurs.
Option (a) was selected — Reuse of an existing, already-correct pattern
in the same file — over (c), which would have added new defensive
handling around a write that should never have been attempted for that
case, and over (b), which would have required a schema change and a new
governance decision about the object's own anchor becoming optional.
The chosen fix was independently confirmed to make the invalid write
structurally unreachable, not merely no-longer-observed-to-fail — the
distinguishing property this rule's own Reuse-first preference is meant
to produce.

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

**Fresh-context reviewer requirement (formalized per ADR-014 —
METH-001):** "Independently" requires a genuinely independent reviewer —
a fresh-context subagent or a separate reviewing party that re-derives
and re-verifies material claims (test execution, migration state, API
conformance) against actual source, rather than synthesizing a
certification from the implementing session's own conversational memory.
Certification produced from the implementing session's own memory, no
matter how thorough, does not satisfy this section — the implementation
agent SHALL NOT certify its own work, and a same-context "review" of the
same session's own claims is self-certification in substance even when
it is not labelled as such.

Only an independently certified Work Package shall be considered
complete.

-------------------------------------------------------------------------------
19.7b Multi-Stage Independent Verification Escalation (Mandatory,
formalized per ADR-017 — METH-002)
-------------------------------------------------------------------------------

WP-05 demonstrated that Independent Certification (19.7 above), even
when correctly performed by a genuinely independent, fresh-context
reviewer, is not by itself sufficient to guarantee that no
non-deferrable defect (19.8.5) remains undisclosed in a Work Package
recorded as certified. Certification alone missed two High-severity
defects that a deeper, differently-scoped audit subsequently found.

Every Work Package SHALL therefore close through the following gate
sequence, each gate performed by a reviewer independent of every gate
before it:

1. Independent Certification (19.7).

2. Verification & Validation (V&V) Audit — a fresh-context reviewer,
   uninvolved in the implementation or the Certification pass,
   re-examines the Work Package against its own governing
   specifications with a broader, more exhaustive mandate than
   Certification's own re-verification (a Requirements Traceability
   Matrix, exhaustive specification-conformance checking, and
   empirical probing per the method requirement below) — not merely a
   repeat of Certification's own method at greater length.

3. Remediation — if the V&V Audit finds anything requiring correction,
   the implementing session remediates it.

4. Independent Verification of Remediation — a further fresh-context
   reviewer, uninvolved in the implementation, the original
   Certification, the V&V Audit, or the remediation itself,
   independently confirms the remediation before the Work Package's
   certified status is restored. This step is REQUIRED for every
   remediation, regardless of the underlying finding's own severity —
   "the fix is small" or "the fix is obviously correct" is not an
   exception. A remediation accepted on the implementing session's own
   say-so, without this step, does not satisfy this section, for the
   same reason self-certification does not satisfy 19.7.

5. Release Readiness Audit — a further fresh-context reviewer verifies
   git status, commit history, repository-wide consistency between
   source, tests, and governance documents, full regression test
   results, and governance-document accuracy, before authorizing a
   push to the remote repository. This gate exists specifically to
   catch governance-documentation staleness (e.g., a status field still
   describing a superseded or already-completed state) that a
   content-focused review is not positioned to notice, since checking
   documentation-versus-actual-repository-state accuracy is not that
   review's own primary lens.

**Method requirement for gates 2 and 4 (V&V Audit and Independent
Verification of Remediation):** re-reading source code and re-running
the existing test suite, by themselves, only prove the implementation
satisfies what the existing tests already check — they provide no
evidence about a defect the existing tests were never designed to
catch, which is exactly how WP-05's own two defects survived a
correctly-performed Certification. Each such gate SHALL therefore
include at least one purpose-built, from-scratch runtime probe per
defect class under review, not adapted from the existing test suite.
When re-verifying a remediation specifically, the reviewer SHALL also
run a negative control — the same probe executed against the pre-fix
code (e.g., extracted from the prior commit) — to confirm the probe
actually reproduces the original defect, before treating the probe's
passing against the corrected code as meaningful evidence.

**Harness/fixture production-parity checklist (part of the V&V Audit,
gate 2):** does the test harness enforce every constraint the declared
production database enforces unconditionally (foreign keys, check
constraints, uniqueness)? Does at least one test exercise more than
one tenant/organization for any capability whose data model includes
an organization boundary? Both of WP-05's own undetected defects
existed specifically because the shared test harness and fixtures did
not answer "yes" to these two questions — this checklist item is not
speculative, it is the named root cause.

**Interrupted reviewer subagents (informative, not a mandatory gate):**
where a dispatched independent reviewer (any of gates 2, 4, or 5) is
interrupted mid-task by a transient infrastructure or connection error
— as opposed to reaching a substantive conclusion — resume the same
agent from its own transcript rather than dispatching a fresh agent
from scratch, so that already-verified partial progress is not
discarded and is not put at risk of being inconsistently re-derived by
a second, independent pass.

Only a Work Package that has completed every gate this section
requires (Certification; V&V Audit; Remediation and its Independent
Verification, if remediation occurred; Release Readiness Audit) may be
pushed to the remote repository.

19.8 Technical Debt Management (Mandatory)

Technical Debt is recognised as a normal outcome of iterative software
development.

Technical Debt SHALL be visible, traceable, prioritised, and actively
managed.

Technical Debt SHALL NEVER be hidden, ignored, or repeatedly carried
forward without being recorded.

19.8.1 Definition

Technical Debt includes non-blocking implementation observations that:

• do not justify failing Independent Review

• do not require an Architecture Decision Record (ADR)

• do not require immediate remediation

• are intentionally deferred to a future Business Activity,
Work Package, or release

Examples include:

• additional test coverage

• performance improvements

• refactoring opportunities

• code simplification

• improved observability

• improved diagnostics

• enhanced validation

• concurrency improvements

• non-critical UX improvements

19.8.2 Mandatory Recording

Every accepted Technical Debt item SHALL be recorded in the repository
Technical Debt Register.

Location:

architecture/06-Reviews/TECH-DEBT.md

Each entry SHALL include:

• Technical Debt ID

• Description

• Raised In

• Priority

• Planned Resolution

• Status

Technical Debt SHALL NOT exist solely within Independent Review reports,
implementation reports, commit messages, or chat history.

19.8.3 Independent Review Behaviour

Once a Technical Debt item has been recorded:

Future Independent Reviews SHALL reference the Technical Debt ID rather
than repeating the full observation.

Example:

Observation:

Tracked as TD-001.

No additional discussion required.

This prevents recurring observations from being repeatedly copied into
multiple review reports.

19.8.4 Resolution

Technical Debt may be resolved by:

• the current Business Activity

• a future Business Activity

• Work Package Closure

• a later Work Package

• a dedicated technical improvement initiative

When resolved:

• update the Technical Debt Register

• record the resolving Work Package or Business Activity

• change the Status to Closed

19.8.5 Technical Debt Governance

Technical Debt SHALL NOT be used to defer:

• architectural defects

• security defects

• data integrity defects

• tenant isolation defects

• failing tests

• build failures

• broken functionality

• mandatory compliance requirements

Such issues SHALL be remediated before the Business Activity Completion
Gate (§19.7) is satisfied.

19.8.6 Guiding Principle

Technical Debt is acceptable only when it is:

• visible

• justified

• prioritised

• planned

• tracked

• eventually resolved

The objective is to maintain continuous delivery without compromising
long-term maintainability, architectural integrity, or software quality.

19.8.7 Technical Debt Severity Rubric (formalized per ADR-014 — METH-001)

Every Technical Debt entry SHALL be assigned a severity of High, Medium,
or Low against the following rubric, so that severity is a stated
judgment against a fixed standard rather than an ad hoc label.

High —

• the gap defeats the governing capability's own stated Business Intent
  (CAP-001), even if only for a disclosed subset of cases; or

• the gap weakens a security or tenant-isolation boundary, even if no
  exploit is currently known.

Example: `TD-070` (WP-04) — no real ERG-001 structural-mutation
mechanism exists yet, so a completed structural transition does not
actually change enterprise structure. This defeats C-005's own Business
Intent for a disclosed subset of cases (any transition whose outcome
must be reflected in `organization_nodes` or a hierarchy/consolidation
table) and is rated High for that reason, not merely because it is
large.

Medium —

• the gap is an internal completeness or robustness concern (additional
  test coverage, performance headroom, refactoring, improved
  observability, enhanced validation, concurrency hardening) that does
  not defeat the capability's stated Business Intent and does not touch
  a security or tenant-isolation boundary, but is expected to require
  resolution before the capability is exercised at production scale or
  by a downstream capability that depends on it.

Low —

• the gap is a non-critical improvement (minor UX polish, diagnostic
  convenience, naming or documentation clarity) whose absence has no
  effect on correctness, security, or another capability's ability to
  depend on this one.

Severity is independent of Priority (§19.8.2's own Technical Debt
Register field): a High-severity item may still be deliberately deferred
with a documented Planned Resolution, exactly as `TD-070` was — severity
states how much is at stake if the gap is never closed; Priority states
when it is planned to be closed. Neither field substitutes for the
other, and §19.8.5's own governance list (Technical Debt SHALL NOT defer
architectural, security, data-integrity, or tenant-isolation defects, or
failing tests or build failures) already prohibits deferring severity
that would itself be disqualifying — this rubric classifies debt that
has already passed that gate, it does not relax it.

# 20. Enterprise Experience Standard (Mandatory, Prospective Only)

*(Formalized per direct Repository Owner governance instruction,
2026-07-31.)*

## 20.1 Scope and Applicability

This section governs every Work Package for which implementation has
not yet begun as of this section's own addition to this document. As
of this addition, WP-01 through WP-07 are CLOSED; this standard governs
WP-08 onward.

It does NOT reopen any Work Package already CLOSED. A Work Package
certified before this section existed remains valid under the
governance that existed at the time of its own certification — the
same principle §19.8.7's own severity rubric applies to Technical Debt
("classifies debt that has already passed that gate, it does not
relax it"), applied here to Work Package governance itself.

## 20.2 Canonical Authority — No Duplication

This section states an additional Work Package **completion** condition.
It does not define, and shall never be read to redefine, any of the
following — each remains sole authority for its own concern, per §16:

- Presentation Architecture (what a screen must be) → SD-001
- Design System (visual language, tokens, themes, components,
  accessibility) → DS-001
- Enterprise Experience methodology (Journeys, Personas, Workspaces,
  CRBs, ERBs, EXs, Navigation, Context Preservation) → PE-001 /
  PE-001-Cxxx
- Engineering implementation standard — including Frontend Standards
  (IMP-001 §10) and the Business Activity/Business Object
  implementation pattern (IMP-001 §5/§6) → IMP-001

Where this section states a requirement, it governs **when** a Work
Package may be considered complete. It does not restate **how** to
build the frontend, the backend, or any canonical component — IMP-001,
SD-001, and DS-001 already govern that exhaustively, and this section
shall never be amended to duplicate them.

## 20.3 Vertical Slice Requirement

Unless a Work Package's own charter explicitly designates it
infrastructure-only (a Work Package that delivers no Business Activity,
e.g. WP-RTA-001) or a specific Business Activity within it explicitly
backend-only, every Work Package SHALL deliver, for each Business
Activity it charters:

- Database, Domain Model, Repository, Service, API — per IMP-001 §5/§6/§8
- Frontend, Navigation, Enterprise Experience — per SD-001, DS-001,
  PE-001, engineered per IMP-001 §10
- The end-to-end user journey connecting the two
- Unit tests and integration tests — per IMP-001 §11
- Documentation — per §19.7's own Implementation Report requirement
- Independent Certification, Verification & Validation, and Release
  Readiness — per §19.7 / §19.7b

A Work Package that implements only the backend half of this list,
without disclosing and justifying the frontend/Enterprise Experience
half as out of scope through the Gap Analysis (§19.3) and an explicit
repository-owner charter decision, is incomplete.

## 20.4 Demonstrability

Every Business Activity a Work Package charters SHALL be demonstrable
through the running application — a real persona, using the real
frontend, exercising the real API, producing a real, persisted outcome.
A Business Activity satisfied only by an automated test suite, with no
operable screen a persona can actually use, does not meet this standard
unless the Work Package's own charter explicitly designates it
infrastructure-only or backend-only — a scope decision that SHALL be
reported and justified per §19.4's own STOP-and-report discipline, not
silently assumed.

## 20.5 World-Class Frontend Standard — Interaction-Quality Reference Only

Every screen SHALL meet the interaction quality, workflow efficiency,
discoverability, responsiveness, accessibility, and enterprise
usability standard exemplified by production enterprise software such
as Microsoft Fabric, Microsoft Dynamics 365, Salesforce Lightning,
Stripe Dashboard, Atlassian Cloud, Linear, Notion, Figma, and the
Vercel Dashboard.

These products are engineering references for interaction quality
only. Claude Code SHALL NOT copy their visual design, layout, branding,
or component styling. DS-001 remains the sole authority for every
visual and component decision, per §19.1. Where DS-001 does not define
something one of these references suggests, Claude Code SHALL STOP and
request clarification (§19.1) — never substitute a referenced product's
own visual treatment for a missing DS-001 definition.

## 20.6 Implementation Quality Baseline

Every screen and widget a Work Package delivers SHALL implement, in
addition to IMP-001 §10.3's own four content-disclosure states
(Summary, Details, Evidence, Audit History):

- a loading state
- an empty state
- a validation state
- an error state
- a confirmation state

against real API integration. Placeholder UI, mocked workflows, and
hard-coded demonstration data may exist transiently during development
but SHALL NOT remain at the point a Business Activity is submitted for
Independent Certification.

Metadata-driven UI (screens rendered from `screen_registry`, per
IMP-FE-001) and keyboard accessibility are mandatory, per IMP-001 §10.2
and SD-001's own accessibility principles respectively — restated here
only as a completion-gate checkpoint, not as a new rule.

## 20.7 Work Package Completion Gate Extension

§19.7's Business Activity Completion Gate and §19.7b's five-gate Work
Package closure sequence are extended, for every Work Package within
this section's own scope (§20.1), by one further condition: Independent
Certification (§19.7) SHALL NOT pass until, in addition to §19.7's own
existing checklist:

- Backend capability is complete.
- Enterprise Experience is complete.
- Navigation is complete.
- The end-to-end workflow is demonstrable in the running application.
- Frontend and backend are fully integrated — no mocked API response,
  no stubbed service call.

An Independent Certification that passes a Work Package meeting only
the backend half of this list, within this section's own scope, does
not satisfy §19.7 — for the same reason a same-context self-certification
does not satisfy it: the completion condition it purports to certify
was not actually met.

Where a Work Package is explicitly chartered infrastructure-only or
backend-only (§20.3), this extension does not apply to it — the
charter's own disclosed scope decision governs, per §19.4.