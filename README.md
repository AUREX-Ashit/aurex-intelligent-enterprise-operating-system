# CorpStage Enterprise Operating System (EOS)

> **Enterprise Operating System for AI-Native, Capability-Driven
> Enterprises**

------------------------------------------------------------------------

## Overview

The CorpStage Enterprise Operating System (EOS) is a modular,
enterprise-grade platform for building, operating, and evolving
intelligent business capabilities.

Rather than implementing isolated applications, the platform provides
reusable domain services, canonical enterprise models, and configurable
business capabilities.

This repository is architecture-driven and implementation-focused.

------------------------------------------------------------------------

## Vision

Build a production-quality Enterprise Operating System that is:

-   Modular
-   Capability-driven
-   AI-enabled
-   Secure by design
-   Event-driven
-   Observable
-   Extensible
-   Cloud-native

------------------------------------------------------------------------

## Repository Structure

``` text
.
├── .github/
├── architecture/
├── cil/
├── decisions/
├── docs/
├── prompts/
├── source/
│   ├── backend/
│   ├── frontend/
│   ├── database/
│   ├── infrastructure/
│   ├── scripts/
│   └── tests/
├── ARCHITECTURE.md
├── CLAUDE.md
└── README.md
```

------------------------------------------------------------------------

## Repository Entry Points

  File              Purpose
  ----------------- --------------------------------------------
  README.md         Project overview and onboarding
  ARCHITECTURE.md   Repository navigation and architecture map
  CLAUDE.md         AI engineering guide for Claude Code

------------------------------------------------------------------------

## Technology Stack

### Backend

-   Python
-   FastAPI
-   SQLAlchemy
-   Alembic
-   Pydantic

### Frontend

-   React
-   Next.js
-   TypeScript

### Platform

-   PostgreSQL
-   Redis
-   Docker
-   Azure OpenAI

------------------------------------------------------------------------

## Development Workflow

1.  Understand the requirement.
2.  Review architecture.
3.  Review ADRs.
4.  Consult the relevant CIL.
5.  Search existing implementation.
6.  Design.
7.  Implement.
8.  Test.
9.  Review.
10. Commit.

------------------------------------------------------------------------

## Getting Started

### Prerequisites

-   Git
-   Docker & Docker Compose
-   Python
-   Node.js
-   Visual Studio Code
-   Claude Code

### Clone

``` bash
git clone <repository-url>
cd <repository-folder>
```

### Backend

``` bash
docker compose up -d
cd source/backend
uvicorn main:app --reload
```

### Frontend

``` bash
cd source/frontend
npm install
npm run dev
```

------------------------------------------------------------------------

## Engineering Principles

-   Search before creating.
-   Extend before replacing.
-   Reuse before duplicating.
-   Respect architectural boundaries.
-   Protect canonical enterprise concepts.
-   Keep services cohesive.
-   Add tests with every change.

------------------------------------------------------------------------

## Testing

Backend:

``` bash
pytest
```

Frontend:

``` bash
npm test
```

------------------------------------------------------------------------

## Documentation

  Topic                             Location
  --------------------------------- ---------------
  Enterprise Architecture           architecture/
  Canonical Information Libraries   cil/
  Architecture Decisions            decisions/
  Product Documentation             docs/
  AI Prompts                        prompts/

------------------------------------------------------------------------

## Contributing

-   Read ARCHITECTURE.md.
-   Review CLAUDE.md.
-   Follow repository conventions.
-   Keep changes focused.
-   Ensure all tests pass.

------------------------------------------------------------------------

## Current Phase

**Sprint 1 -- Platform Foundation**

Primary objectives:

-   Platform scaffolding
-   Authentication & Identity
-   Organization & Membership
-   RBAC
-   Database foundation
-   API foundation
-   CI/CD
-   Automated testing

------------------------------------------------------------------------

## License

Copyright © CorpStage. All rights reserved unless otherwise specified.
