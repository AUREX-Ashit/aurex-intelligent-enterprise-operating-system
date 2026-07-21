# ADR-003 — Organization Management (C-004) Implementation Ownership for WP-01

**Status:** Accepted
**Classification:** Architecture Governance / Service Ownership
**Decided by:** Repository owner (architecture governance authority), 2026-07-20, during WP-01 Implementation Readiness Assessment (IRA-001) review.
**Affected Documents:** None amended — this ADR resolves an implementation-ownership ambiguity that CAP-001/ARCH-000/ERG-001 do not themselves address (service assignment is outside CAP-001's registry schema).

---

## Context

IRA-001 (WP-01 Implementation Readiness Assessment) found two services with conflicting claims on Organization Management (C-004):

- **`Backend/Services/AuthService`** has a real, migrated `Organization` SQLAlchemy model (`organizations` table, 7 columns), already load-bearing for WP-00's `Membership.organization_id` FK and bootstrap seed data.
- **`Backend/Services/TenantService`** self-describes (README, `main.py` FastAPI description) as a "Tenant, Organization, and Workspace provisioning microservice," but its actual implementation is a fully mocked scaffold: every route returns hardcoded/fabricated data, `get_db()` never yields a real session, all repository methods are stubs, and no Alembic migration exists for its `Tenant`/`TenantConfig`/`TenantUser` tables.

CAP-001 and ARCH-000 do not assign a microservice to any capability — that mapping is an implementation decision outside their registry schema, per IRA-001 §3 (Architecture Impact Matrix) and CLAUDE.md §8's requirement that each capability have exactly one owning service.

## Decision

1. **`AuthService` is the implementation owner for Organization Management (C-004) during WP-01** and the current modular-monolith phase of the platform.
2. **`TenantService` remains scaffolding** — not authoritative for Organization data, not to be built out in parallel with WP-01, and not to be treated as a second owner of C-004.
3. **Future service extraction** (splitting Organization Management into its own deployable service, or reconciling it with `TenantService`'s `Tenant` concept) **will be evaluated after the modular-monolith phase**, as a separate, explicitly-scoped architectural decision — not decided by this ADR.

## Rationale

AuthService already carries the only real, persisted, migrated implementation of the Organization concept, and other WP-00 work (Membership, bootstrap seeding) already depends on it. Building a second, competing implementation in TenantService while its scaffold has zero real persistence would violate CLAUDE.md §8 ("Never duplicate business logic... never couple unrelated domains") and Golden Rule 3 ("One capability. One owner."). Consolidating ownership in AuthService for the current phase avoids that duplication with the lowest-risk, lowest-rework path.

## Consequences

- WP-01 builds `routers/organization.py`, `services/organization_service.py`, `repositories/organization_repository.py`, and related schemas inside `Backend/Services/AuthService`.
- `TenantService`'s existing mocked `/tenant/*` routes are left untouched by WP-01 — not extended, not migrated, not deleted.
- A future ADR is required before any service-extraction or TenantService/AuthService reconciliation work begins; this ADR does not authorize that work.
- This decision does not change CAP-001, ARCH-000, or ERG-001 — it resolves an implementation-layer question those documents intentionally leave open.

## Status

**Accepted**
