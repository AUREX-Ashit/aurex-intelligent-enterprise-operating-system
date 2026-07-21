# ADR-004 — Organization Canonical Schema Scope for WP-01

**Status:** Accepted
**Classification:** Architecture Governance / Data Model Scope
**Decided by:** Repository owner (architecture governance authority), 2026-07-20, during WP-01 Implementation Readiness Assessment (IRA-001) review.
**Affected Documents:** None amended — Master Technical Architecture's `organization_master` definition is unchanged; this ADR scopes WP-01's implementation against it, it does not redefine it.

---

## Context

IRA-001 found a substantial gap between AuthService's current `organizations` table (7 columns: id, organization_code, organization_name, organization_type, is_active, created_at, updated_at) and Master Technical Architecture's canonical `organization_master` table (~25 columns, including `tenant_id`, sector/industry taxonomy references, `reporting_framework_json`, `onboarding_stage`, `business_resilience_maturity_score`, board/reporting configuration flags, etc.). No document stated whether WP-01 must implement the full canonical shape or a scoped subset.

## Decision

**Master Technical Architecture's `organization_master` remains the complete canonical Organization model** — this ADR does not alter it. **WP-01 implements only the subset of that model required for:**

- Organization Lifecycle (create, activate, suspend)
- CRUD (create, read, update)
- Profile (name, code, type, descriptive fields)
- Configuration (organization-level settings needed by WP-01's own scope)
- Search (by name/code)
- Validation (uniqueness, required fields)

**The remaining canonical attributes** (industry taxonomy references, reporting framework configuration, business resilience/board-meeting fields, onboarding-stage tracking, revenue/employee-count fields, etc.) **are explicitly deferred and will be introduced incrementally by future work packages**, as those work packages' own scopes require the fields (e.g., a future Reporting/Onboarding work package would add `reporting_framework_json`, `onboarding_stage`, etc.).

## Rationale

Building the full 25-column canonical shape in WP-01 would pull in fields with no current consumer (no work package yet uses `business_resilience_maturity_score` or `reporting_framework_json`), inflating WP-01's scope beyond its stated Business Activities and risking premature, unvalidated schema decisions for fields whose real shape will only become clear when the work package that actually needs them is planned. Implementing a validated subset now, with the full canonical model as the acknowledged long-term target, is consistent with IMP-001's incremental Business Activity delivery model and avoids speculative schema design.

## Consequences

- WP-01's Alembic migration(s) extend `organizations` with only the columns needed for the six areas listed above (exact column list determined during WP-01 design, not by this ADR).
- Every deferred canonical field remains a known, tracked gap — not a silent omission. Future work packages that need a deferred field extend the table additively; this ADR pre-authorizes that pattern rather than requiring a new ADR each time, provided the addition is purely additive (IMP-CICD-001's deprecation-floor discipline still applies to any later rename/removal).
- `organization_master`'s canonical definition in Master Technical Architecture is not modified, superseded, or forked by this decision.

## Status

**Accepted**
