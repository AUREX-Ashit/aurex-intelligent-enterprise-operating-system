# CorpStage Enterprise Operating System (EOS)

## Repository Architecture Index

This repository follows an **Architecture → Engineering → Implementation** model.

When working in the repository, always locate the appropriate authoritative source before making changes.

---

# Repository Map

```
/
├── architecture/
├── cil/
├── decisions/
├── docs/
├── prompts/
├── source/
└── .github/
```

---

# Repository Navigation

| If you need... | Start Here |
|----------------|------------|
| Repository governance | `architecture/00-Governance/` |
| Enterprise blueprint | `architecture/01-Blueprint/` |
| Enterprise concepts and constitutional models | `architecture/02-Constitutional/` |
| Engineering methodology | `architecture/03-Engineering/` |
| Technical architecture | `architecture/04-Technical/` |
| Implementation specifications | `architecture/05-Implementation/` |
| Architecture reviews | `architecture/06-Reviews/` |
| Architecture Decision Records (ADRs) | `architecture/07-Decisions/` |
| Canonical enterprise vocabulary | `cil/` |
| Industry-specific extensions | `cil/industry-packs/` |
| Product documentation | `docs/` |
| AI engineering prompts | `prompts/` |
| Backend implementation | `source/backend/` |
| Frontend implementation | `source/frontend/` |
| Database | `source/database/` |
| Infrastructure | `source/infrastructure/` |
| Build & automation | `source/scripts/` |
| Testing | `source/tests/` |

---

# Repository Search Order

When implementing any feature:

1. Understand the requirement.
2. Search the Architecture.
3. Review relevant ADRs.
4. Review the appropriate CIL.
5. Search the existing source code.
6. Reuse before creating.
7. Implement.
8. Test.
9. Commit.

---

# Engineering Principles

Always:

- Search before creating.
- Extend before replacing.
- Reuse before duplicating.
- Respect service boundaries.
- Protect canonical enterprise concepts.
- Keep business logic inside the owning service.
- Add tests with every change.

---

# Golden Rules

- One capability → One owning service.
- One business rule → One implementation.
- One enterprise concept → One canonical definition.
- One source of truth for enterprise data.
- Never duplicate business logic.
- Never bypass architectural boundaries.
- Never introduce enterprise concepts without checking the CIL.
- Leave the repository better than you found it.

---

# Technology Stack

**Backend**

- Python
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic

**Frontend**

- Next.js
- React
- TypeScript

**Platform**

- PostgreSQL
- Redis
- Docker
- Azure OpenAI

---

# Before Creating Anything

Before creating a new:

- Service
- API
- Business Activity
- Entity
- Database Table
- DTO
- Event
- Utility
- Component

Always search the repository first.

If an implementation already exists:

**Extend → Refactor → Reuse**

Do not create parallel implementations.

---

**Repository Objective**

Build a modular, enterprise-grade Enterprise Operating System that remains simple, consistent, extensible, secure, and maintainable over the long term.