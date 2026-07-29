# ADR-002 — Reconcile AuthService Seed Role Catalog with MDP-001 / URA-001

**Status:** Proposed (drafted under IC-001 WP-00 Bootstrap Certification, 2026-07-20 — not yet accepted; requires architecture governance decision)
**Classification:** Data Model / Canonical Vocabulary Governance
**Affected Documents:** MDP-001 (Master Data Population Specification), URA-001 (User, Role, Permission, Event and Assignment)
**Affected Implementation:** `Backend/Services/AuthService/scripts/03_seed_r001_data.sql`, `scripts/bootstrap_data.py`

---

## Context

1. **MDP-001** §B1 specifies `system_role_registry` as exactly 5 fixed rows, sourced verbatim from URA-001-29: `AUREX_ADMIN`, `CORPORATE_ADMIN`, `USER_ADMIN`, `SECURITY_ADMIN`, `DOMAIN_ADMIN`.
2. **MDP-001** §B2 specifies `business_role_registry` (global rows, `organization_id = NULL`) sourced from URA-001-30's named examples: `CEO, CFO, COO, CHRO, CSO, CISO, Company Secretary, Finance Manager, Plant Head, Board Member`.
3. **URA-001-03** states System Roles and Business Roles "remain independent" and must not be conflated.
4. AuthService's baseline seed source (`scripts/03_seed_r001_data.sql`, present in the repository prior to WP-00 and unmodified by it) seeds a single, undifferentiated `roles` table with: `PLATFORM_ADMIN, ORG_ADMIN, ESG_MANAGER, AUDITOR, SUPPLIER_ADMIN, BOARD_MEMBER`. WP-00's `scripts/bootstrap_data.py` ports this catalog verbatim (Reuse-before-Create), introducing no new role codes.
5. Cross-referencing: `BOARD_MEMBER` matches a canonical Business Role name. `PLATFORM_ADMIN`/`ORG_ADMIN` are conceptually adjacent to `AUREX_ADMIN`/`CORPORATE_ADMIN` but use different codes. `ESG_MANAGER`, `AUDITOR`, `SUPPLIER_ADMIN` do not appear in either canonical registry — they read as domain-specific Business Roles for Aurex's ESG/sustainability vertical, but have never been formally added to URA-001-30 or MDP-001 §B2.
6. This conflict was found during IC-001 WP-00 certification (see Backend/Services/AuthService/docs — bootstrap runbook — and the IC-001 certification review matrix). It predates WP-00; WP-00's only action was to operationalize the existing catalog into an automated, CI-gated pipeline (IMP-CICD-002), which raises its practical blast radius without changing its content.

## Decision Required (not made by this ADR)

Architecture governance must choose one of:

**Option A — Rename to conform.** Rename `PLATFORM_ADMIN` → `AUREX_ADMIN` and `ORG_ADMIN` → `CORPORATE_ADMIN`; split the schema into a `system_role_registry`-equivalent and `business_role_registry`-equivalent (or add a discriminator consistent with the existing `is_system_role` column already present on AuthService's `Role` model); move `ESG_MANAGER`/`AUDITOR`/`SUPPLIER_ADMIN` out of the seeded global template set entirely, to be created as tenant-specific custom Business Roles per URA-001-38 at organization onboarding instead.

**Option B — Extend the canonical registry.** Treat `ESG_MANAGER`, `AUDITOR`, `SUPPLIER_ADMIN` as legitimate new canonical Business Roles for Aurex's domain and amend URA-001-30 / MDP-001 §B2's named-example list to include them; separately reconcile `PLATFORM_ADMIN`/`ORG_ADMIN` naming against `AUREX_ADMIN`/`CORPORATE_ADMIN` (Option A's naming fix, without the tenant-scoping change).

**Option C — Hybrid.** Some combination of A and B, decided case-by-case per role.

This ADR does not select an option. It is a data-model and canonical-vocabulary decision outside an AuthService implementation task's authority (CLAUDE.md §18/§19.4).

## Consequences (of leaving this undecided)

- AuthService continues seeding a role catalog that does not match MDP-001 §B1/§B2's specified registry rows.
- Any future service or capability spec (PE-001-C001/C002/C003) that assumes the canonical `system_role_registry`/`business_role_registry` shape will need to reconcile against AuthService's actual seeded data.

## Status

**Proposed** — awaiting architecture governance review. No implementation change has been made under this ADR.
