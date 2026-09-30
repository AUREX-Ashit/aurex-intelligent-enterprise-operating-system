# TDS-WP23-TD-171-R3 — External Prerequisites Request (Gate R3)

**Work Package:** `WP-23`, TD-171 remediation tranche (Charter §21a; AUTHORIZED at R2, `d2aaade`).
**Addressed to:** **Platform Engineering**, the repository-defined owner of "Deployment and release" and "Database ownership" (`Backend/Services/AuthService/docs/OPERATIONAL_OWNERSHIP.md`, "Ownership model"). Ownership there is defined by responsibility, not by named individuals.
**Prepared:** 2026-09-30, by Repository Owner instruction ("Prepare the TD-171 external prerequisites request package"). Baseline HEAD: `560d0fa`.
**Status:** **REQUEST ISSUED — ALL FOUR PREREQUISITES REQUESTED / NOT PROVIDED.**

---

## §1 Purpose

The TD-171 remediation tranche is designed at R3 (`TDS-WP23-TD-171-R3-Remediation-Design-and-Readiness.md`, `fa93fc7`), but R3 cannot be accepted yet:
- Charter §21a.7 defines R3 as "Design and readiness complete: … environment designation and infrastructure prerequisites confirmed".
- Four prerequisites are outside the repository team's authority.

This request states, for someone not involved in the repository governance discussions:
- **what** is needed;
- **why**;
- **what evidence** must be returned;
- **which R3 criterion** it serves;
- **what must not be assumed or invented**.

**Background in one paragraph.**
- The Business Activity Registry (BAR) lives in AuthService's database, in two tables: `bar_identifier_ledger` and `bar_registration`.
- BAR issues enterprise-global Business Activity Identifiers (`BA-NNNNNN`).
- Today any code in the AuthService process could write those tables (TD-171).
- The approved design makes a **governed deployment-time operation** the only production BAR writer. The AuthService **runtime** gets read-only access to BAR, and a **reconciliation** check compares the canonical database with the repository's governance records.
- The design is decided. The infrastructure it relies on does not exist yet.

## §2 Current R3 State

| Item | State |
|---|---|
| R2 | AUTHORIZED |
| R3 | **NOT SATISFIED / NOT READY FOR R3 ACCEPTANCE REVIEW** |
| R4–R6 | NOT SATISFIED |
| Design decisions | OD-1, OD-2, OD-3 and OD-5 DESIGN DECIDED. **OD-4 OPEN / EXTERNAL** (TDS §17.1; Charter §21a.6; remediation ROD §19.7; IMP-REPORT) |
| TD-171 | OPEN |
| M2 | NOT AUTHORIZED / NOT STARTED |
| M2-P | CHARTERED / NOT AUTHORIZED / NOT STARTED |

## §3 External Prerequisites Summary

| ID | Requirement | Owner | Evidence required | R3 criterion | Status |
|---|---|---|---|---|---|
| **EP-01** | Canonical production BAR/AuthService database designation | Platform Engineering | An authoritative designation of the production environment and database instance (§4) | **C-10**; OD-4; OQ-R-5; Charter §21a.6 R-06, §21a.7 R3 | **REQUESTED / NOT PROVIDED** |
| **EP-02** | Database-role separation for the BAR tables | Platform Engineering | Role identities, grant/revoke evidence, connection-to-role mapping, a demonstration that the runtime cannot write (§5) | **C-07**; OD-2; Charter §21a.6 R-03; OQ-R-3 | **REQUESTED / NOT PROVIDED** |
| **EP-03** | Controlled, read-only reconciliation access to the canonical database | Platform Engineering | Access mechanism, principal, scope, read-only enforcement, environment binding, ability to run the check (§6) | **C-09**; OQ-R-6; Charter §21a.7 | **REQUESTED / NOT PROVIDED** |
| **EP-04** | PostgreSQL verification environment for R4 tests | Platform Engineering (CI/CD) | Confirmation of a PostgreSQL CI capability able to run role, transaction and reconciliation tests (§7) | **C-12** (PostgreSQL plan), supporting **C-07** and **C-09** tests; TD-176; R-08 | **REQUESTED / NOT PROVIDED** |

## §4 EP-01 — Canonical Production Environment Designation

**Need.** One actual production AuthService database must be designated as the **canonical** BAR database: the only place where enterprise-global BAR identifiers are issued (OQ-R-5, decided). No other environment may issue competing canonical identifiers, and test or non-production data never becomes canonical.

**Why the existing flag is not enough.**
- AuthService already has `ENVIRONMENT=production`: `config.py` `settings.environment`, recognized by `services/bootstrap_service.py` to gate bootstrap credentials.
- That flag classifies a **process**. It does not identify **which database instance** is canonical.
- Two processes could both run with `ENVIRONMENT=production` against different databases. EP-01 must name the instance.

**Requested:**
- the designated production environment;
- the database instance, identified sufficiently for governance verification;
- the authoritative basis for the designation;
- how non-canonical environments are identifiable as non-canonical.

**Not to be invented by the repository:** environment name, database name, connection string, host, subscription or resource ID. The repository has no deployment configuration or pipeline beyond CI (`.github/workflows/authservice-ci.yml`), so this must come from Platform Engineering.

**Serves:** C-10 and OD-4; the environment identity check the governed operation performs before writing (TDS §8).

## §5 EP-02 — Database-Role Separation

**Need** (OD-2, decided; TDS §5):

| Principal | Required on `bar_identifier_ledger` and `bar_registration` |
|---|---|
| **AuthService runtime** (the application process, including in-process BAE/M2) | **SELECT only**. **No INSERT, UPDATE or DELETE** |
| **Governed deployment-time operation** | The only production principal allowed to INSERT (as the existing atomic allocation and insert requires). No UPDATE or DELETE unless a separately governed remediation requires it |
| Schema/migration principal | The existing migration flow (DDL), as today |

**Evidence dependency found in the repository.**
- The governed operation follows the `scripts/run_bootstrap.py` precedent: a separate process (`python -m scripts.run_bootstrap`).
- That script connects through the **same** `db_manager` / `DATABASE_URL` as the runtime (`scripts/run_bootstrap.py` uses `models.database.db_manager`).
- The deployment mechanism must therefore let the governed operation connect with a **different** principal from the runtime. This does not exist today.

**Requested:**
1. provision the separation;
2. provide the actual role identities once created;
3. provide the grants/revokes, or equivalent authoritative evidence, for both BAR tables;
4. identify which runtime connection uses the restricted principal;
5. identify which controlled deployment process uses the write-capable principal, and how it receives its credentials separately;
6. demonstrate that runtime access cannot INSERT, UPDATE or DELETE either BAR table.

**The states are distinct:**
- DESIGN REQUIREMENT: this section; met.
- PROVISIONED INFRASTRUCTURE: items 1–5; requested.
- VERIFIED RUNTIME BEHAVIOUR: item 6 here, then independently at R4/R5; requested.

**Not to be invented:** role names, grant scripts or credentials. Roles are not placed in Alembic migrations unless Platform Engineering decides so (TDS §5).

**Serves:** C-07; Charter §21a.6 R-03; OQ-R-3.

## §6 EP-03 — Controlled Read-Only Reconciliation Access

**Need.** The reconciliation control (TDS §7) compares canonical BAR rows with `BAR-INDEX.md` and the repository's governing acts. It must be able to read the canonical database without becoming another BAR writer (OQ-R-6, decided).

**Requested access:**
- read-only;
- scoped to the canonical environment (EP-01);
- controlled;
- sufficient to read `bar_identifier_ledger`, `bar_registration`, and the canonical environment's identity (for the EP-01 binding).

The governance evidence (acts, `BAR-INDEX.md`) is read from the repository, not the database.

**Requested evidence:**
- the access mechanism;
- the identity/principal used;
- the scope;
- read-only enforcement (the principal cannot create, modify or delete BAR records);
- the environment binding;
- a demonstration that the reconciliation query or check can run.

**Explicitly not requested:** write access, unrestricted production credentials, or access to any other schema or service. BAE M2 is **not** the reconciliation owner and gets no BAR write access.

**Serves:** C-09; OQ-R-6; Charter §21a.7.

## §7 EP-04 — PostgreSQL Verification Environment

**Repository evidence:**
- `.github/workflows/authservice-ci.yml` has two jobs:
  - the **test** job runs `pytest tests/` on SQLite;
  - the **bootstrap** job starts an ephemeral `postgres:16` service (`POSTGRES_USER`/`POSTGRES_DB` `authservice`), runs `alembic upgrade head`, runs `scripts.run_bootstrap` twice, and checks `/ready`.
- The shared test harness `tests/conftest.py` is SQLite-only.
- Role separation and PostgreSQL transaction behaviour cannot be verified on SQLite (TD-176; TDS §10).

**Requested:** confirm that R4 may use the **existing ephemeral PostgreSQL 16 CI capability**, extended as needed to run PostgreSQL-backed BAR tests. Confirm whether that CI database principal can create roles and grants inside the ephemeral database, so role separation can be tested (the evidence dependency). The tests cover:
- role separation;
- runtime write denial;
- the governed write path;
- rollback and transaction behaviour;
- reconciliation queries;
- the TD-171 negative cases (TDS §11).

No new permanent environment is requested if the existing capability suffices.

**Distinction.** CI/test PostgreSQL is **not** the canonical production environment. EP-04 provides test evidence. It never satisfies C-10, and test identifiers are never canonical (OQ-R-5).

**Serves:** C-12 (the PostgreSQL plan); supports the C-07 and C-09 tests; TD-176; R-08.

## §8 Evidence Required From Platform Engineering

| EP | Minimum evidence to return |
|---|---|
| EP-01 | A dated, attributable designation naming the canonical production environment and database instance, and how non-canonical environments are distinguished |
| EP-02 | Role identities; grants/revokes on both BAR tables; the runtime-to-role and governed-operation-to-role mapping, including the separate credential path; a runtime write-denial demonstration |
| EP-03 | The principal, mechanism, scope and environment binding; read-only enforcement evidence; a demonstration that the reconciliation check runs |
| EP-04 | CI job and PostgreSQL version; confirmation of role-creation capability in CI; confirmation of transaction-test capability; a reference to where the tests will run |

## §9 R3 Acceptance Mapping

| R3 criterion (TDS §13) | Prerequisite | Effect when evidence is provided |
|---|---|---|
| C-07 Database-role separation | EP-02 (and EP-04 for tests) | Moves from EXTERNAL PROVISIONING REQUIRED toward confirmation at R3 review |
| C-09 Reconciliation access | EP-03 | Moves from NOT AVAILABLE toward confirmation at R3 review |
| C-10 Canonical environment designation | EP-01 | Allows OD-4 to be decided (the identity check) |
| C-12 PostgreSQL plan | EP-04 | Allows the R4 PostgreSQL evidence to be produced (TD-176) |

Returned evidence is **input** to the R3 acceptance review. **The Repository Owner / R3 acceptance review decides** whether the prerequisites satisfy Charter §21a.7.

## §10 Explicit Non-Requirements / Things Not To Invent

This request does **not**:
1. authorize infrastructure changes;
2. authorize production writes;
3. designate a production environment itself;
4. create database roles;
5. grant reconciliation access;
6. satisfy R3.

**Nothing below may be assumed or filled in by the repository:**
- environment, database, host, subscription or resource names;
- connection strings or credentials;
- role names or grant scripts;
- any "production" status inferred from `ENVIRONMENT=production` alone.

**Governance boundaries:**
- Platform Engineering's confirmation must be **returned as evidence** (§11).
- **M2 remains unauthorized.** **TD-171 remains OPEN** until the governed remediation gates (R3–R6) are completed.
- Operational ownership grants no authority to change architecture (`OPERATIONAL_OWNERSHIP.md`, "Change control").

## §11 Handoff / Response Record (to be completed by Platform Engineering)

**EP-01**
- Canonical production environment: [TBD — infrastructure owner]
- Canonical database: [TBD — infrastructure owner]
- How non-canonical environments are distinguished: [TBD — infrastructure owner]
- Authoritative designation/evidence: [TBD — infrastructure owner]
- Date: [TBD — infrastructure owner]
- Owner: [TBD — infrastructure owner]

**EP-02**
- Runtime (restricted) principal: [TBD — infrastructure owner]
- Governed-operation (write-capable) principal: [TBD — infrastructure owner]
- Separate credential path for the governed operation: [TBD — infrastructure owner]
- BAR table grants/revokes (`bar_identifier_ledger`, `bar_registration`): [TBD — infrastructure owner]
- Runtime write-denial evidence: [TBD — infrastructure owner]
- Date: [TBD — infrastructure owner]
- Owner: [TBD — infrastructure owner]

**EP-03**
- Read-only reconciliation principal: [TBD — infrastructure owner]
- Environment: [TBD — infrastructure owner]
- Scope: [TBD — infrastructure owner]
- Read-only enforcement evidence: [TBD — infrastructure owner]
- Connection/access mechanism: [TBD — infrastructure owner]
- Demonstration that the reconciliation check runs: [TBD — infrastructure owner]
- Date: [TBD — infrastructure owner]
- Owner: [TBD — infrastructure owner]

**EP-04**
- PostgreSQL environment: [TBD — infrastructure owner]
- Version: [TBD — infrastructure owner]
- CI job: [TBD — infrastructure owner]
- Role-creation/role-test capability: [TBD — infrastructure owner]
- Transaction-test capability: [TBD — infrastructure owner]
- Evidence: [TBD — infrastructure owner]
- Date: [TBD — infrastructure owner]
- Owner: [TBD — infrastructure owner]

## §12 Status

| Item | State |
|---|---|
| EP-01 | REQUESTED / NOT PROVIDED |
| EP-02 | REQUESTED / NOT PROVIDED |
| EP-03 | REQUESTED / NOT PROVIDED |
| EP-04 | REQUESTED / NOT PROVIDED |
| R3 | **NOT SATISFIED / NOT READY FOR R3 ACCEPTANCE REVIEW** |
| TD-171 | OPEN |
| M2 | NOT AUTHORIZED / NOT STARTED |
| M2-P | CHARTERED / NOT AUTHORIZED / NOT STARTED |

**Traceability:**
- TDS R3 §5, §7, §8, §10, §13, §17.1 (`fa93fc7`);
- Charter §21a.6 (R-03, R-06), §21a.7 (`649f55a`);
- remediation ROD §19 (OQ-R-3, OQ-R-5, OQ-R-6), §19.7;
- IMP-REPORT-WP-23, TD-171 tranche status (`560d0fa`);
- TD-176;
- `OPERATIONAL_OWNERSHIP.md`;
- `.github/workflows/authservice-ci.yml`;
- `scripts/run_bootstrap.py`;
- `config.py`;
- `services/bootstrap_service.py`;
- `tests/conftest.py`.

*End of request package. No infrastructure changed. Nothing staged, committed or pushed.*
