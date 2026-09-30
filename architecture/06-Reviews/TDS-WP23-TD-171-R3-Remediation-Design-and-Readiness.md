# TDS-WP23-TD-171-R3 — TD-171 Remediation Tranche: Design and Readiness Package (Gate R3)

**Work Package:** `WP-23`, TD-171 remediation tranche (Charter §21a, ACCEPTED / IN FORCE; **AUTHORIZED** at Gate R2, `d2aaade`).
**Prepared:** 2026-09-30, by Repository Owner instruction ("Prepare the R3 Design and Readiness Package"). Baseline HEAD: `032d8d8`.

**Gate R3: NOT SATISFIED.** This package makes R3 assessable. It does not satisfy R3.
- **Verdict (§15): NOT READY FOR R3 ACCEPTANCE REVIEW.**
- *(2026-09-30.)* Repository Owner design decisions **OD-1, OD-2, OD-3 and OD-5 are DECIDED** (§17.1). **OD-4 remains OPEN** (an external prerequisite). The verdict is unchanged, because the external prerequisites §21a.7 requires within R3 are still absent (§15).
- The package creates no code, test, migration, schema, CI change, role, grant or environment.
- No existing file is modified.

**Status vocabulary:**

| Term | Meaning |
|---|---|
| DECIDED | Governance decision exists |
| DESIGNED | This package specifies it conceptually |
| SPECIFIED | Machine-checkable rule fixed |
| AVAILABLE | The resource exists |
| PROVISIONED | Created for this purpose |
| VERIFIED | Independently evidenced |
| READY | Nothing blocks the next gate |
| AUTHORIZED | Implementation permitted |

---

## §1 Design Authority and Boundary

| Authority | Content |
|---|---|
| R2 (`ROD-WP23-TD-171-Remediation-Tranche-Authorization-Decision-Preparation.md §19`, `d2aaade`) | OPTION A — AUTHORIZE, subject to 14 binding conditions (§19.2), including condition 3 (the act-citation rule is designed and approved within R3), condition 4 (canonical environment designated), condition 5 (roles designed and provisioned), condition 6 (read access) and condition 10 (R3 confirms readiness) |
| Charter §21a (accepted `7f479bd`; R2 synchronized `032d8d8`) | Scope A–K; R-01–R-10; gates R1–R6; closure criteria; stop conditions |
| OQ-R-1 to OQ-R-7 (`ROD-WP23-TD-171-Remediation-Decision-Preparation.md §19`) | B / D / governed operation + roles / ADR-ROD act / single canonical environment / infrastructure read access / quarantine-block |
| A–C non-reopening (§21a.4; RD-23-02) | Workstreams A–C stay accepted |

**This package designs the authorized tranche.**
- It does not expand the tranche or reopen A–C.
- It does not authorize Workstreams D–H, M2 or M2-P.
- Where the investigation finds that a design choice needs a Repository Owner decision, the choice is recorded as an **open decision question** (§17), not selected.

## §2 Current Repository Baseline (observed at `032d8d8`)

| Item | Observed fact | Design assumption? |
|---|---|---|
| Registration model | `models/bar_registration.py`: `bar_registration`. A `registration_status` CHECK allows only `'REGISTERED'` (D2 two-state). `identifier` is UNIQUE and FK to `bar_identifier_ledger.identifier`. UNIQUE (work package, reference). `registering_act` is free text | No |
| Identifier ledger | `models/bar_identifier_ledger.py`: `identifier` UNIQUE | No |
| Registration service | `register()` validates non-blank fields, checks the (WP, reference) collision, and allocates plus inserts ledger and registration rows atomically in a savepoint (`begin_nested`). It emits `record_audit` (with `registering_act`) and `publish_event`. `registering_act` is "a citation, not verified here" | No |
| **Second write path** | `services/bar_identifier_service.py` `issue_identifier()` writes **ledger** rows independently of registration (the duplicated allocator is TD-174) | No |
| Callers | `register()` and `issue_identifier()` have **no non-test callers**. No router exists | No |
| Repository | `repositories/bar_registration_repository.py`: `get_by_identifier`, `get_by_work_package_and_reference`, `count_registered` (read) | No |
| `BAR-INDEX.md` | §3 register: **zero entries**. §8: add a row only when a registering act is performed | No |
| Tests | `tests/test_bar_identifier_service.py`, `tests/test_bar_registration_service.py`, `tests/test_bar_transaction_safety.py` (SQLite; FK pragma in the last). TD-172: misnamed or non-evidential collision tests. Shared `conftest.py` is hard-wired to in-memory SQLite | No |
| Migrations | `a7b8c9d0e1f2` (ledger), `b8c9d0e1f2a3` (registration). No migration names `b8c9d0e1f2a3` as its `down_revision` | No |
| Environment config | `config.py` `settings.environment` (default `"development"`). `services/bootstrap_service.py` treats `production`/`prod` as production (bootstrap credential gating). **No specific database is designated** | No |
| Database connection | A single `DATABASE_URL` (`config.py`; `models/database.py` single engine). `Config/platform-config.yaml`: local superuser; `auth_service_user` intended, not granted | No |
| PostgreSQL | No local PostgreSQL (Docker unavailable; `psql` not installed). CI `authservice-ci.yml`: the **test** job runs SQLite pytest; the **bootstrap** job runs an ephemeral `postgres:16` with `alembic upgrade head`, bootstrap and `/ready` | No |
| Role/grant patterns | None: no `GRANT`, `CREATE ROLE` or `SET ROLE` in `Backend/`, `database/` or CI | No |
| Authorization patterns | `require_platform_admin` (claims), `require_authority_holder` (AI-001/AI-002, C-040), `enforce_approval_authority` (organization). None applies to BAR (remediation ROD §10) | No |
| Audit/event | `observability.record_audit`/`publish_event`, log-based stand-ins (C-114 not implemented) | No |
| Governed deployment-time operation precedent | `scripts/run_bootstrap.py`, run as a separate process (`python -m scripts.run_bootstrap`) in CI and deployment; idempotent | No |
| Act precedent (CBOR-ADR) | `CBOR-INDEX.md` rows cite a "Registering ADR" by ID (e.g. `ADR-006`). The ADRs (e.g. `ADR-037`) carry a bold header block (`**Status:** Accepted`, `**Decided by:** Repository Owner …`). **The registered identifier is not a structured header field** | No |

Deployed-database state cannot be observed (remediation ROD §11).

## §3 R-01: Governed Registration Operation (DESIGNED in part; **not SPECIFIED**)

**Design.** A single governed operation, run as a separate, reviewed deployment-time process following the `scripts/run_bootstrap.py` precedent, performs a registration only when:
1. the cited act file exists in the repository at the conventional path for its identifier;
2. its header marks it Accepted and decided by the Repository Owner;
3. its structured fields name the Business Activity reference, the owning capability and/or WP, the registration intent and the governing authority;
4. the requested registration equals those fields;
5. the (WP, reference) pair is not already registered.

It then calls the existing atomic allocation and insert, and emits the existing audit and event records citing the act.

**Failure semantics (DESIGNED):**
- A missing act, or an act that is not Accepted, is refused before any write.
- An act that doesn't name the requested registration is refused before any write.
- A malformed act (a required field missing or unparseable) is refused before any write.
- An existing (WP, reference) registration is refused (existing collision path; no second row).
- A transaction failure leaves no ledger row, registration row or index change (existing savepoint behaviour plus operation atomicity).
- Every refusal emits audit DENIED/FAILED with the act citation.

**Not yet specifiable:**
- **The act's structured field convention.** CBOR-ADRs have no structured identifier field, so a new header-field convention is needed. The convention itself is a governance-document convention: **open decision OD-3**.
- **The identifier-timing conflict** (**open decision OD-1**, §17). OQ-R-4 requires the act to "explicitly identify the BAR Business Activity Identifier". But D5 (`BAR-INDEX.md` §2: "the identifier is assigned at BAR registration — never earlier") and Charter §7 (the act "triggers its own identifier issuance") mean the act cannot contain the identifier before the operation issues it. Candidate resolutions:
  - (i) a two-part act: an authorization part before execution, and a dated execution addendum recording the issued identifier, verified by CI and reconciliation;
  - (ii) the act pre-states the expected identifier, and the operation verifies equality. This is in tension with D5's "never earlier";
  - (iii) other.

  Per `CLAUDE.md §16`, this is not resolved by assumption.

~~**Status:** DECIDED (OQ-R-2, R-4). Operation shape DESIGNED. Citation rule **NOT SPECIFIED** (OD-1, OD-3).~~

*(2026-09-30, RO decision, §17.1.)* **OD-1 (two-part act) and OD-3 (structured governed-act convention) are applied:**
- The operation validates the **authorization component** (§17.1.3 A) before issuance.
- It then calls the existing atomic allocation and insert, where the identifier is issued at registration, never earlier (D5 unchanged).
- It then **produces the execution addendum** (§17.1.3 B), recording the issued identifier and the execution reference. The addendum is recorded in the repository through a governed commit.
- The registration is **governed only when both parts are linked and jointly verified**.
- Until the addendum is committed, the row is not yet governed. Reconciliation reports it (§7) and the OD-5 deployment-level block applies (§9).
- Validation is deterministic, from the metadata fields. The free-text `registering_act` is not the control; it carries the `governing_act_id`.

**Status (updated):** DECIDED. DESIGNED. The convention is SPECIFIED at field level (§17.1.3), subject to R3 acceptance review, implementation and verification.

## §4 R-02: Production Write-Path Restriction (DESIGNED; one open scope question)

- **Callers:** `register()` and `issue_identifier()` have no non-test callers, and there is no router (§2). No production caller has to be migrated.
- **Design:**
  - the governed operation (§3) is the only production path that invokes registration;
  - the application runtime is denied registration writes **at the database** (R-03), so any direct invocation of `register()` from the running service fails;
  - a repository CI check (R-04) asserts that no non-test module other than the governed operation references `register()` or `issue_identifier()`.
  - The service methods stay callable in tests, and no method is deleted or renamed.
- **Negative tests (R4):** a `register()` call under the runtime role fails with no row. A static check fails on a new non-test caller.
- **Workstream C code:**
  - touched only to add the act-validation call path and restrictions;
  - no change to allocation, identifier format or ledger semantics, which stay excluded (TD-173, TD-174, TD-175);
  - performed under the §21a boundary. The A–C acceptance record is not altered (§21a.4).
- **Open: OD-2.** Does the restriction also cover `issue_identifier()`, the ledger-only write path? Uncontrolled identifier issuance would contradict OQ-R-5, which forbids competing canonical identifiers. §21a.3 C names the "production write-path restriction" for *registration*; restricting access is not allocation redesign. A decision is needed on whether it is inside §21a.

~~**Status:** DESIGNED, subject to OD-2.~~

*(2026-09-30, RO decision, §17.1.)* **OD-2 decided: both `issue_identifier()` and `register()` are canonical BAR write paths and are governed.**
- "No current production callers" is **not** sufficient governance.
- Final production model: one governed deployment-time BAR write authority; no unrestricted application/runtime path for identifier issuance or registration; no competing issuer; BAE/M2 read-only.
- **Mechanism (this design):**
  - the runtime database principal has **no INSERT, UPDATE or DELETE on either `bar_identifier_ledger` or `bar_registration`** (§5);
  - the governed-operation principal is the only one able to write them;
  - the §4 static caller check covers both methods.
- **Negative verification (R4):** runtime code cannot issue a canonical identifier (T-R); runtime code cannot register (I, J); the governed operation is the controlled production write path (A, M).
- **B/C determination:** this restricts **access**. It does not change issuance or allocation semantics, the identifier format or ledger behaviour, and `register()` already writes the ledger itself. It is therefore incorporated into the tranche design under §21a.3 C–D. **No Workstream B/C design amendment is required.** A wording synchronization of §21a.6 R-02/R-03 is required (§17.2).

**Status (updated):** DECIDED. DESIGNED, subject to implementation and verification.

## §5 R-03: Database-Role Separation (DESIGNED conceptually; **NOT PROVISIONED**)

- **Current:** one `DATABASE_URL` and one engine. Local config uses a superuser. There are no roles or grants.
- **Consequence:** BAE M2 runs in-process in AuthService on the **same** `db_manager` engine (RD-M2-05). "BAE/M2 cannot write registrations" is therefore only achievable if the **AuthService runtime role itself** lacks BAR write privileges.
- **Conceptual model** (no role names; names are infrastructure's):

| Principal | Privileges on `bar_registration`, `bar_identifier_ledger` | Owner | Provisioned by |
|---|---|---|---|
| Schema/migration principal | DDL (existing migration flow) | Infrastructure | Infrastructure |
| **Runtime principal** (AuthService process, including in-process BAE/M2) | **SELECT only**; INSERT, UPDATE and DELETE revoked | Infrastructure | Infrastructure (REVOKE/GRANT) |
| **Governed-operation principal** (the deployment-time process) | SELECT and INSERT as required by the atomic allocation and insert. No UPDATE or DELETE unless OD-5 requires it | Infrastructure | Infrastructure |

- **Migration responsibility:** grants are environment-specific and name infrastructure roles, so they are **not** placed in Alembic migrations unless infrastructure decides otherwise (**external**).
- **Failure behaviour:** a write under the runtime principal is refused by PostgreSQL. The operation refuses to run unless it is connected as the governed-operation principal (a check performed at run time).
- **Evidence:** role separation can only be proven on **PostgreSQL**. SQLite has no roles.
- **Status:** DECIDED (OQ-R-3). DESIGNED conceptually. **NOT PROVISIONED** (external; condition 5).

## §6 R-04: Repository CI Verification (DESIGNED; depends on OD-1 and OD-3)

**Repository-only checks** (no database access):
- every `BAR-INDEX.md` §3 row cites an act that exists and is Accepted;
- the act's structured fields equal the row's reference, capability/WP and retroactive flag;
- identifiers and (WP, reference) pairs are unique in the index;
- no index row lacks an act, and no act claims a registration missing from the index (under OD-1 (i), once the execution addendum exists);
- malformed citations fail;
- the §4 static caller check.

**CI infrastructure:** the existing test job (Python, repository checkout) can host repository-only checks. Adding them is within R-04, under OQ-05-4-style limits.

**Not a database authority:** CI never reads or asserts deployed state.

~~**Status:** DESIGNED. The field rules depend on OD-1 and OD-3.~~

*(2026-09-30, RO decision, §17.1.)* Additional repository-only checks from OD-1 and OD-3:
- every act has a well-formed metadata table (§17.1.3), and every required field is present;
- `governing_act_id` equals the record's identifier;
- every execution addendum's `addendum_of` resolves to an Accepted authorization component, and its reference, capability, WP and intent equal the authorization's;
- every `BAR-INDEX.md` row's identifier equals exactly one addendum's `bar_identifier`;
- no authorization has two addenda.

**Status (updated):** DESIGNED.

## §7 R-05: Environment Reconciliation (DESIGNED; **access NOT AVAILABLE**)

Compares persistent rows, the `BAR-INDEX.md` §3 rows and the acts, per environment, using read-only access (OQ-R-6):

| State | Condition | Disposition |
|---|---|---|
| Valid governed | Row = index = act | Accepted |
| Missing governance evidence | A row whose act is absent or not Accepted | Blocked/quarantined (OD-5) |
| Missing index entry | A row with no index row | Blocked/quarantined |
| Index-only | An index row with no persistent row (in the canonical environment) | Reported. The governance record is inconsistent; resolved by separate authorization |
| Mismatched | Fields disagree | Blocked/quarantined |
| Duplicate/conflicting | Prevented by UNIQUE constraints; reported if found | Blocked/quarantined |
| Ungoverned | Any row not demonstrably governed | Blocked/quarantined (R-07) |

There is no automatic deletion, adoption or rewrite. Reconciliation writes nothing.

*(2026-09-30, RO decision, §17.1.)* **OD-5 state set.** Each state below except *valid* is a **deployment integrity failure** handled by the §9 deployment-level block:
- **valid registered row:** authorization and addendum are linked and jointly verified, and row = index = act;
- **missing governing act:** no authorization or addendum resolves, including "execution addendum not yet committed";
- **malformed governing act:** the metadata table is absent, a required field is missing, or a value is unparseable;
- **mismatched governing act:** a field disagrees between row, index, authorization and addendum;
- **duplicate/conflicting evidence:** two addenda, or two index rows, for one identifier or (WP, reference);
- **ungoverned row:** a row with no governing evidence at all;
- **reconciliation failure:** the check itself cannot complete (for example, the store is unreadable). It is never read as "clean".

**Status:** DESIGNED. **Access NOT AVAILABLE** (external; condition 6).

## §8 R-06: Canonical Production Environment (**NOT READY**)

- **Observed:** `ENVIRONMENT=production` is a process classification that gates bootstrap credentials. It is **not** a designation of the canonical BAR identifier database. There is no deployment configuration, database identity or environment governance record.
- **Required designation record** (external; infrastructure/deployment owner, recorded under WP-23):
  - which database instance is canonical;
  - how the governed operation identifies it before writing;
  - how non-canonical environments are prevented from running the operation, or from treating their identifiers as canonical;
  - how non-production data stays isolated.
- **Enforcement design:** the operation refuses to run unless the target matches the recorded canonical designation. Non-canonical environments may run only test registrations, never cited in `BAR-INDEX.md`. The exact identity check depends on the designation form (**OD-4**).
- **Status:** DECIDED (OQ-R-5). **NOT DESIGNATED. NOT READY** (external; condition 4; §21a.7 R3).

## §9 R-07: Ungoverned-Row Handling (**design conflict: OD-5**)

- **Detection and classification:** by reconciliation (§7). Evidence is captured as a reconciliation report citing row, index and act state.
- **Prohibited:** silent adoption, deletion or rewrite, and treating row existence as execution eligibility.
- **Conflict.**
  - `bar_registration` has a single allowed state (`registration_status` CHECK = `'REGISTERED'`), and BAE M2 treats "row exists" as registered.
  - M2 must not compensate (OQ-171-2), and any schema change must be justified inside §21a.
  - So a quarantined row **cannot be blocked from execution eligibility** without one of the following. Each needs a decision:
    - (i) a schema-level quarantine marker (changes the D2 two-state record);
    - (ii) moving the row to a separate quarantine store by an authorized operation (a disposition, needing separate authorization under OQ-R-7);
    - (iii) a **deployment-level block**: no execution-eligibility consumer may be deployed or authorized against an environment with any unresolved ungoverned row, and TD-171 cannot close while one exists. There is no schema change and no M2 logic;
    - (iv) other.
- **Current evidence:** no ungoverned rows are evidenced (none locally). Deployed environments are **not verified**.
- ~~**Status:** DECIDED (OQ-R-7). Blocking mechanism **NOT DESIGNED** (OD-5).~~
- *(2026-09-30, RO decision, §17.1.)* **OD-5 decided: deployment-level block.**
  - **No new BAR registration status** and no change to the `bar_registration` lifecycle.
  - Any §7 non-valid state is a **deployment integrity failure**.
  - The WP-23 reconciliation control, run as a mandatory deployment step against the designated environment:
    - **detects** the condition;
    - **blocks** the environment from treating the row as canonical: the deployment does not proceed to normal operation, no execution-eligibility consumer may be deployed or authorized against it, and TD-171 cannot close;
    - **surfaces** the exact discrepancy in the reconciliation report;
    - **preserves** the row unchanged;
    - **requires a separately governed remediation** before normal operation proceeds.
  - **M2 does not compensate.** It adds no interpretation of BAR state (OQ-171-2).
- **Status (updated):** DECIDED. DESIGNED, subject to implementation and verification. Remaining design detail: whether an AuthService start-up integrity check is also required in addition to the deployment step (§17.3).

## §10 R-08: PostgreSQL Verification (plan DESIGNED; **NOT VERIFIED**)

- **Available:** CI bootstrap job ephemeral `postgres:16` (migrations applied). **Not available:** local PostgreSQL; target environment.
- **Harness gap:** `tests/conftest.py` is SQLite-only. BAR PostgreSQL tests need a PostgreSQL-capable fixture (an R4 implementation item within R-08).
- **R4 PostgreSQL evidence required:**
  - BAR registration and allocation, including a real concurrent collision (TD-176);
  - savepoint rollback;
  - role separation (§5): runtime write refused, operation write permitted;
  - the reconciliation queries;
  - the governed operation end to end on a migrated database.

  SQLite results do not count.
- **Status:** plan DESIGNED. **NOT VERIFIED** (TD-176 Open; condition 7).

## §11 Test / Verification Matrix (R4; **no test exists yet**)

| ID | Case | Type | Needs |
|---|---|---|---|
| A | Valid governed registration | Integration + PostgreSQL | OD-1, OD-3 |
| B | Missing act | Unit/integration (negative) | — |
| C | Wrong/mismatched act | Unit/integration (negative) | OD-3 |
| D | Malformed citation | Unit (negative) | OD-3 |
| E | Duplicate registration | Integration + PostgreSQL | — |
| F | Conflicting `BAR-INDEX.md` entry | CI repository check | OD-3 |
| G | Missing `BAR-INDEX.md` entry | CI + reconciliation | OD-1 |
| H | Ungoverned persistent row | Reconciliation | OD-5 |
| I | Unauthorized registration writer | PostgreSQL role test (negative/security) | Roles |
| J | Read-only consumer attempts a write | PostgreSQL role test (negative/security) | Roles |
| K | Transaction rollback | Integration + PostgreSQL | — |
| L | Audit/event evidence cites the act | Integration | — |
| M | PostgreSQL execution of A, E, K, O | PostgreSQL | Harness |
| N | Role separation | PostgreSQL | Roles |
| O | Reconciliation states (§7) | Reconciliation | Access, or a controlled test database |
| P | Canonical-environment isolation | Deployment | OD-4, designation |
| Q | Static caller check (§4), both `register()` and `issue_identifier()` (OD-2) | CI | — |
| R | *(2026-09-30, OD-2.)* Runtime principal attempts `issue_identifier()`: refused, no ledger row | PostgreSQL role test (negative/security) | Roles |
| S | *(2026-09-30, OD-1/OD-5.)* Row with authorization but no committed addendum is reported "missing governing act" and blocks; clears once the addendum is committed | Reconciliation + CI | — |

Negative controls against the pre-fix code are required at R5 (`§19.7b`).

## §12 Design Artifacts Required Before R3 Can Be Satisfied

| # | Artifact | State |
|---|---|---|
| 1 | Governed-act machine-verification specification | ~~**Blocked by OD-1, OD-3**~~ DESIGNED (§17.1.3), subject to R3 acceptance |
| 2 | Governed registration operation design | DESIGNED (§3) |
| 3 | Write/read database-role design | DESIGNED conceptually (§5) |
| 4 | CI validation design | DESIGNED (§6), pending OD-1/OD-3 |
| 5 | Reconciliation design | DESIGNED (§7) |
| 6 | Canonical environment designation record | **External; absent** |
| 7 | Ungoverned-row handling procedure | ~~**Blocked by OD-5**~~ DESIGNED (§7, §9; OD-5) |
| 8 | PostgreSQL verification plan | DESIGNED (§10) |
| 9 | Test matrix | DESIGNED (§11) |
| 10 | Implementation/change boundary | DESIGNED (§16) ~~, pending OD-2~~ (OD-2 decided) |
| 11 | R4 evidence plan | DESIGNED (§16) |

## §13 R3 Readiness Checklist

| ID | Requirement | Evidence | Status | Blocking? | Owner | Next gate |
|---|---|---|---|---|---|---|
| C-01 | §21a accepted | `7f479bd` | SATISFIED | — | RO | — |
| C-02 | R2 authorization | `d2aaade` | SATISFIED | — | RO | — |
| C-03 | Scope | §21a.3 | SATISFIED | — | — | — |
| C-04 | Ownership | §21a.5 | SATISFIED | — | — | — |
| C-05 | Governing-act validation | §3; §17.1 | ~~**OUTSTANDING** (OD-1, OD-3)~~ **DESIGNED**, decision resolved (OD-1, OD-3), subject to implementation and verification | ~~**Yes**~~ No (for design) | WP-23 | R4/R5 |
| C-06 | Write-path restriction | §4; §17.1 | ~~DESIGNED (OD-2 open)~~ **DESIGNED**, decision resolved (OD-2), subject to implementation and verification | ~~**Yes** (OD-2)~~ No (for design) | WP-23 | R4/R5 |
| C-07 | Database-role separation | §5 | **DESIGNED CONCEPTUALLY / EXTERNAL PROVISIONING REQUIRED** | **Yes** | Infrastructure | R3 confirmation, R4 |
| C-08 | CI verification | §6 | DESIGNED ~~(depends on C-05)~~ (C-05 design resolved) | ~~Yes (via C-05)~~ No (for design) | WP-23 | R4 |
| C-09 | Reconciliation access | §7 | **EXTERNAL PREREQUISITE — NOT AVAILABLE** (reconciliation design: DESIGNED) | **Yes** | Infrastructure | R3 confirmation, R4 |
| C-10 | Canonical environment designation | §8 | **OPEN / EXTERNAL PREREQUISITE — DO NOT INVENT** (OD-4 open) | **Yes** | Infrastructure | R3 |
| C-11 | Ungoverned-row handling | §9; §17.1 | ~~**OUTSTANDING** (OD-5)~~ **DESIGNED**, decision resolved (OD-5), subject to implementation and verification | ~~**Yes**~~ No (for design) | WP-23 | R4/R5 |
| C-12 | PostgreSQL plan | §10 | DESIGNED. NOT YET VERIFIED | No for R3; yes for closure | WP-23 | R4/R5 |
| C-13 | Test matrix | §11 | DESIGNED | No | WP-23 | R4 |
| C-14 | Deployment evidence plan | §16 | DESIGNED (depends on C-10) | Via C-10 | WP-23 + Infrastructure | R4 |
| C-15 | Independent review plan | §21a.7 R5; Charter §16 | DESIGNED | No | Reviewers | R5 |
| C-16 | Closure synchronization plan | §21a.8; R2 §19.2 items 12–13 | DESIGNED | No | WP-23 (separate authorization) | R6 |

## §14 Stop Conditions

**Carried forward:** §21a.11 in full.

**R3-specific** (evidence-supported):
- governing-act validation cannot be made machine-verifiable (OD-1, OD-3 unresolved);
- an unrestricted production write path remains, including `issue_identifier()` if OD-2 includes it;
- role separation cannot be established on PostgreSQL;
- the canonical environment remains undesignated;
- reconciliation access cannot be established;
- PostgreSQL verification cannot be performed;
- ungoverned rows are discovered without an authorized disposition or a decided blocking mechanism (OD-5);
- the work needs allocation, identifier-format or ledger-semantics changes (TD-173, TD-174, TD-175);
- the scope expands to D–H;
- the A–C acceptance is reopened;
- M2 or M2-P work is introduced;
- M2 is asked to compensate.
- *(2026-09-30.)* any runtime or application path, other than the governed operation, can write either BAR table (OD-2);
- a deployment proceeds past a §7 non-valid state (OD-5 block bypassed);
- an identifier is pre-created to satisfy an act (OD-1; D5).

## §15 R3 Gate Decision

**R3 = NOT SATISFIED.**

**NOT READY FOR R3 ACCEPTANCE REVIEW.**
- ~~**Unresolved design decisions needing the Repository Owner:** OD-1, OD-2, OD-3 and OD-5. OD-4 follows the external designation.~~ *(2026-09-30: OD-1, OD-2, OD-3 and OD-5 **DECIDED**, §17.1. **OD-4 remains OPEN**; it depends on the external designation.)*
- **External prerequisites absent:**
  - canonical environment designation (C-10);
  - role provisioning (C-07);
  - reconciliation access (C-09).

  Charter §21a.7 requires these to be confirmed within R3.
- **Designed and complete apart from the above:** the operation shape, write-path restriction, conceptual role model, CI checks, reconciliation states, PostgreSQL plan, test matrix, evidence plan, and review and closure plans.

**External Prerequisites Request Note (synchronized 2026-09-30).**
- *Governance synchronization only.* It creates or alters no decision, and does not change this section's conclusion.
- The TD-171 R3 external-prerequisites request (`TDS-WP23-TD-171-R3-External-Prerequisites-Request.md`, `7a3b639`) was **issued to Platform Engineering**, the ownership role in `OPERATIONAL_OWNERSHIP.md`.
- It is recorded in IMP-REPORT-WP-23 (`566d424`), the WPR-001 WP-23 row (`76acac2`), Charter §21a.9 (`4e0f24a`) and the remediation ROD §19.8 (`4765a95`).
- **Issuance/status only.** It does not evidence any action by Platform Engineering.
- The prerequisites remain **external to repository implementation**.

| EP | Prerequisite | Status |
|---|---|---|
| EP-01 | Canonical production environment/database designation | **REQUESTED / NOT PROVIDED** |
| EP-02 | DB-role separation and controlled production write path | **REQUESTED / NOT PROVIDED** |
| EP-03 | Controlled environment-scoped read-only reconciliation access | **REQUESTED / NOT PROVIDED** |
| EP-04 | PostgreSQL verification environment | **REQUESTED / NOT PROVIDED** |

- None of EP-01 to EP-04 is provisioned, available, verified, accepted or completed.
- The request satisfies **no** R3 checklist item. C-05, C-06, C-07, C-09, C-10 and C-11 keep their §13 states.
- OD-1, OD-2, OD-3 and OD-5 remain DECIDED. OD-4 remains OPEN / EXTERNAL.
- **R3 remains NOT SATISFIED / NOT READY FOR R3 ACCEPTANCE REVIEW. TD-171 remains OPEN.**

## §16 R4 Handoff (defined; not started)

R4 would consume:
- the **approved** R3 design (§3–§11, with OD-1 to OD-5 decided); *(2026-09-30: OD-1, OD-2, OD-3 and OD-5 decided; OD-4 open)*
- the implementation boundary: the governed operation, act validation, runtime restriction, CI checks, reconciliation, quarantine/block mechanism, PostgreSQL harness and tests. No allocation, format, ledger-semantics, D–H, M2 or M2-P change;
- the test matrix (§11);
- the environment prerequisites (designation, roles, access);
- the role model (§5);
- the act-validation specification (OD-1, OD-3);
- the reconciliation specification (§7);
- the evidence plan: the §11 results including PostgreSQL, the role negative tests, and controlled deployment of the operation against the designated environment;
- the stop conditions (§14).

## §17 Open Decision Questions (Repository Owner) and Design Questions

*(2026-09-30: OD-1, OD-2, OD-3 and OD-5 are decided; §17.1. OD-4 remains open. The table below is preserved as presented.)*

| ID | Question | Evidence | Candidate resolutions (not selected) |
|---|---|---|---|
| **OD-1** | Identifier timing: how the act "identifies" the identifier (OQ-R-4), given D5 ("assigned at BAR registration — never earlier") and Charter §7 ("triggers its own identifier issuance") | `BAR-INDEX.md` §2 D5; Charter §6–§7; remediation ROD §19 OQ-R-4 | (i) two-part act (authorization, then a dated execution addendum recording the issued identifier); (ii) expected identifier pre-stated, with equality verified; (iii) other |
| **OD-2** | Does the write-path restriction include `issue_identifier()` (the ledger-only path)? | `services/bar_identifier_service.py`; OQ-R-5; §21a.3 C | Include (restriction, not redesign); exclude with justification |
| **OD-3** | Registering-act form and structured field convention (a BAR act series, ADR vs ROD, header fields) | CBOR-ADR header block; no structured identifier field; OQ-R-4 | A header-field extension of the ADR convention; a dedicated registering-act series; other |
| **OD-4** | The canonical-environment identity check (depends on the external designation form) | §8 | Fixed once the designation record exists |
| **OD-5** | The mechanism that blocks execution eligibility of a quarantined row without M2 compensation | §9; `registration_status` CHECK; OQ-R-7; OQ-171-2 | (i) schema marker; (ii) quarantine store via authorized disposition; (iii) deployment-level block; (iv) other |

**Implementation design questions (R3, within WP-23):**
- the PostgreSQL test fixture form;
- the static caller-check mechanism;
- the reconciliation report format.

**External prerequisites:**
- canonical environment designation;
- role provisioning;
- read access;
- a target PostgreSQL environment.

### 17.1 Repository Owner Decision Record (2026-09-30)

*Recorded by direct Repository Owner instruction ("We are now making the Repository Owner design decisions for OD-1, OD-2, OD-3 and OD-5"). Each decision is recorded as stated and is not reinterpreted. Design only: no implementation.*

**17.1.1 Decisions**

| ID | Decision | Status |
|---|---|---|
| **OD-1** | **Two-part governed act (option (i)).**<br>– (1) An **authorization component** establishes the governed authorization and registration intent for a specific Business Activity before the identifier exists.<br>– (2) An **execution/registration addendum** is created by the governed deployment-time registration operation after issuance, and records the actual BAR Business Activity Identifier issued.<br>– A registration is governed **only when both parts are linked and jointly verified**.<br>– The addendum is machine-verifiable against: identifier, reference, owning capability, owning WP, governing authorization, registration intent and issued identifier.<br>– BAR remains the canonical identifier authority. Issuance happens at registration, never earlier. No identifier is pre-created. No competing authority. **D5 is not altered** | **DECIDED** |
| **OD-2** | **Both BAR write paths are governed.**<br>– `issue_identifier()` and `register()` are canonical BAR write paths, and neither remains an unrestricted production application-service write path.<br>– Final model: one governed deployment-time BAR write authority; no unrestricted runtime path for identifier issuance; no competing issuer; BAE/M2 read-only; the governed operation is the production mechanism for BAR writes.<br>– **"No current production callers" is not sufficient governance.**<br>– Negative verification is required later (§4; §11 I, J, R).<br>– Incorporated into the tranche design; **no Workstream B/C design amendment** (§4) | **DECIDED** |
| **OD-3** | **Structured governed-record convention** (§17.1.3). Repository governance records remain the authoritative human-readable acts, carrying a structured, stable, machine-readable metadata block. **No act registry. No new runtime authority** | **DECIDED** |
| **OD-4** | Canonical-environment identity check | **OPEN / EXTERNAL PREREQUISITE.** Not decided. No environment name, database identity, connection identifier or designation is invented |
| **OD-5** | **Deployment-level block** (§9).<br>– No new BAR registration status; the `bar_registration` lifecycle is unchanged.<br>– An ungoverned or unverifiable row is a deployment integrity failure: detected, blocked from being treated as canonical, surfaced, preserved unchanged, and requires separately governed remediation.<br>– No silent delete, rewrite, adoption or reinterpretation. **M2 does not compensate**.<br>– States distinguished in §7 | **DECIDED** |

**17.1.2 Distinction (OD-3)**
- **A. Repository governance record:** the ADR/ROD-style Markdown act (human-readable, RO-authorized, per Charter §7 and §14 and the CBOR-ADR precedent). The execution addendum is a **dated section appended to the same record**, following the repository's dated-addendum convention, committed through a governed commit.
- **B. Machine-verifiable citation/metadata:** a `| Field | Value |` metadata table, the form 15 existing architecture documents already use. No architecture document uses YAML front matter. There is one table per part.
- **C. Runtime validation inputs:** the values parsed from B, plus the requested registration parameters, read by the governed deployment-time operation from the repository checkout it runs with. They are not read from free text.

**17.1.3 Minimum field set** *(field names may be adjusted at R3 acceptance review only to match repository convention; semantics fixed)*

**A. Authorization component** (table titled "BAR Registration Authorization"):

| Field | Value rule |
|---|---|
| `governing_act_id` | Equals the record's own identifier (for example its ADR/ROD identifier) |
| `act_type` | Literal `BAR-REGISTRATION-AUTHORIZATION` |
| `business_activity_reference` | The Business Activity reference, as it will appear in `bar_registration` and `BAR-INDEX.md` |
| `owning_capability` | A `CAP-001` capability identifier |
| `owning_work_package` | A `WPR-001` Work Package identifier |
| `retroactive` | `true`/`false`. It mirrors the existing `is_retroactive` column and `BAR-INDEX.md` "Retroactive" column, which the row already carries |
| `registration_intent` | Literal `REGISTER` |
| `authorization_reference` | The Repository Owner decision authorizing this registration (a record identifier) |
| `governance_authority` | Literal `Repository Owner` |

**B. Execution addendum** (dated section; table titled "BAR Registration Execution"):

| Field | Value rule |
|---|---|
| `act_type` | Literal `BAR-REGISTRATION-EXECUTION` |
| `addendum_of` | Equals the authorization's `governing_act_id` |
| `bar_business_activity_identifier` | The issued `BA-NNNNNN` |
| `business_activity_reference`, `owning_capability`, `owning_work_package`, `registration_intent` | Equal to the authorization component |
| `execution_reference` | The governed operation's run evidence reference (the audit/event correlation) |
| `executed_on` | Date of issuance |

**17.2 Cross-cutting consistency analysis** *(inspection only; no other document is modified in this pass)*

| Document / statement | Finding | Classification |
|---|---|---|
| Charter §21a.6 R-01 ("act … naming the BAR Business Activity Identifier") | Consistent under OD-1: the identifier is named in the execution addendum of the same act. A clarifying note is useful | **1. Required governance synchronization** (clarification). *(Reconciled 2026-09-30: **COMPLETED / SYNCHRONIZED** in `649f55a`, Charter §21a.6 R-01 note.)* |
| Charter §21a.6 R-02 ("`register()` does not remain an unrestricted … production write path") and R-03 ("only the governed write path holds registration-write capability") | OD-2 extends these to `issue_identifier()` and the ledger. It is within §21a.3 C–D (access restriction, not allocation redesign) | **1. Required governance synchronization** (wording). Not a scope amendment. *(Reconciled 2026-09-30: **COMPLETED / SYNCHRONIZED** in `649f55a`, Charter §21a.6 R-02 and R-03 notes.)* |
| Charter §21a.6 R-07 ("classify, quarantine or block") | OD-5 selects "block". Consistent | **4. No change required** |
| Charter §21a.3 exclusions (identifier allocation redesign; D5 unchanged) | OD-1 and OD-2 preserve D5 and allocation | **4. No change required** |
| Remediation ROD §19: OQ-R-4 (act identifies the identifier) | Satisfied by OD-1's addendum | **4. No change required.** An optional pointer could be added at R6 |
| Remediation ROD §19: OQ-R-3 (`register()` restriction) | Extended by OD-2 to `issue_identifier()` | **1. Governance synchronization** (a pointer to OD-2). *(Reconciled 2026-09-30: **COMPLETED / SYNCHRONIZED** in `649f55a`, ROD §19.1 OQ-R-3 pointer and §19.7.)* |
| R2 ROD §19.2 condition 3 (citation rule designed and approved within R3) | Advanced by OD-1 and OD-3. Approval still happens at R3 acceptance | **4. No change required** |
| `BAR-INDEX.md` §3 ("Registering Act" column) and §8 procedure | The column cites `governing_act_id`, and both parts live in one record. Consistent. §8 may later cite the convention when the first registration occurs | **4. No change now.** A future **1** at R4/R6 |
| Workstream B/C design (`ENTERPRISE-BAR-MECHANISM-DESIGN-AND-IMPLEMENTATION-READINESS.md` §18; Charter §7 "mirroring the CBOR-ADR pattern") | OD-3 extends the CBOR-ADR-mirroring convention with a metadata block. No contradiction. The convention is recorded in this TDS | **2. Design amendment** (recorded here). No change to the design document now |
| `IMP-REPORT-WP-23` | Records R2 status. It should record R3 design decisions at R3 acceptance | **1.** Future synchronization (at R3). *(Reconciled 2026-09-30: the R3 design-decision synchronization is **COMPLETED / SYNCHRONIZED** in `560d0fa`, ahead of R3 acceptance. R3 itself remains NOT SATISFIED.)* |
| `WPR-001` WP-23 row | Consistent (R2 authorized; R3 not satisfied) | **4. No change required** |
| `ADR-043` | A separate binding store. Unaffected | **4. No change required** |
| RD-M2-05 (AuthService in-process on the shared engine; OQ-05-3) | A read-only runtime principal on BAR tables is consistent with M2's read-only contract. The test harness must provision it explicitly (OQ-05-3) | **4. No change required** |
| `TECH-DEBT.md` TD-171 | Its synchronization is already a separate future task (OQ-171-5) | **1.** Future (already identified) |
| TD-172, TD-173, TD-174 (duplicated allocator), TD-175, TD-176, TD-096 | OD-2 governs both paths without de-duplicating (TD-174 stays out of scope). The others are unaffected | **4. No change required** |

**No additional architectural decision is required** beyond OD-1, OD-2, OD-3 and OD-5. The "execution addendum pending" interval is covered jointly by OD-1 (governed only when both parts are linked) and OD-5 (block until resolved).

**17.3 Remaining R3 design questions** (within WP-23; not RO decisions unless escalated):
- whether an AuthService start-up integrity check is required in addition to the mandatory deployment reconciliation step (OD-5 enforcement point);
- the sequencing procedure binding a governed operation run to its addendum commit (who commits, and when);
- the PostgreSQL test fixture form;
- the static caller-check mechanism;
- the reconciliation report format;
- the final field-name confirmation at R3 acceptance review (§17.1.3).

## §18 Traceability

| Source | Applied |
|---|---|
| Charter §21a (§21a.3, §21a.4, §21a.6–§21a.11); §6, §7, §14, §15 | §1, §3–§14 |
| OQ-R-1 to OQ-R-7 | §1, §3–§9 |
| R2 §19 (conditions 3–10) | §1, §13, §15 |
| TD-171 | Subject |
| TD-176 | §10 |
| TD-172, TD-173, TD-174, TD-175 | §2, §4, §14 (excluded) |
| A–C acceptance (RD-23-02; `b0f5a12`); RD-23-03; RD-23-04 | §1, §4 |
| BAR code: models, services, repository, migrations, tests; `BAR-INDEX.md`; `CBOR-INDEX.md`; `ADR-037` | §2 |
| `config.py`, `models/database.py`, `services/bootstrap_service.py`, `scripts/run_bootstrap.py`, `Config/platform-config.yaml`, `.github/workflows/authservice-ci.yml` | §2, §5, §8, §10 |
| M2/M2-P: RD-M2-05 (in-process, shared engine); RD-M2-07; OQ-171-2 | §5, §9, §14 |

## Final Status

| Item | State |
|---|---|
| R2 | AUTHORIZED |
| R3 | **NOT SATISFIED** (NOT READY FOR R3 ACCEPTANCE REVIEW) |
| R4 | NOT SATISFIED |
| R5 | NOT SATISFIED |
| R6 | NOT SATISFIED |
| TD-171 | OPEN |
| M2 | NOT AUTHORIZED / NOT STARTED |
| M2-P | CHARTERED / NOT AUTHORIZED / NOT STARTED |

*(2026-09-30.)*

| OD | Decision | Status |
|---|---|---|
| OD-1 | Two-part governed act | DECIDED |
| OD-2 | Both BAR write paths governed | DECIDED |
| OD-3 | Structured governed-act convention | DECIDED |
| OD-4 | Canonical environment designation | OPEN / EXTERNAL |
| OD-5 | Deployment-level block | DECIDED |

*End of R3 design and readiness package. No implementation. Nothing staged, committed or pushed.*
