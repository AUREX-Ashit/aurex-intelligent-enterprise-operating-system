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
-   tests pass
-   security is verified
-   tenant isolation is preserved
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

# 16. Canonical Authority Resolution

When multiple repository documents address the same concern, determine
the canonical owner before implementation.

Use the document that owns the architectural concern.

Examples:

- Enterprise Experience → PE-001
- Capability Experience → PE-001-Cxxx
- Business Activity implementation methodology → IMP-001
- Authorization → URA-001
- Enterprise Intelligence → EIA-001
- Canonical enterprise vocabulary → CIL
- Architecture decisions → ADRs

Do not merge conflicting definitions.

If two canonical documents appear to conflict:

1. Stop implementation.
2. Identify the conflicting definitions.
3. Identify the declared canonical owner.
4. Review applicable ADRs.
5. Report the conflict before changing code.

Never resolve canonical architecture conflicts by assumption.