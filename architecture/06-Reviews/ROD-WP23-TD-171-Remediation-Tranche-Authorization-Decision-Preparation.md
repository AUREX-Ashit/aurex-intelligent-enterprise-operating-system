# ROD-WP23 — TD-171 Remediation Tranche Authorization (Gate R2) — Decision Preparation

**Work Package:** `WP-23`, TD-171 remediation tranche (Charter §21a, ACCEPTED / IN FORCE).
**Prepared:** 2026-09-30, by Repository Owner instruction ("Prepare the TD-171 remediation tranche authorization package"). Baseline HEAD: `7f479bd`.

~~**Nothing is authorized.**~~
- ~~**Gate R2 remains NOT SATISFIED** until an explicit Repository Owner decision is recorded.~~
- *(2026-09-30, §19.)* **Repository Owner decision: OPTION A — AUTHORIZE.** **Gate R2 SATISFIED.** The bounded TD-171 remediation tranche under Charter §21a is **AUTHORIZED**, subject to the §19.2 conditions. **R3–R6 remain NOT SATISFIED. TD-171 remains OPEN.** M2 and M2-P are unchanged and unauthorized.
- No Charter, BAR code, test, migration, `BAR-INDEX.md`, `TECH-DEBT.md`, IRA, WP-BAE-001 or ADR change.

---

## §1 Decision Status / Executive Summary

**Status:** ~~**READY FOR RO DECISION — NO OPTION SELECTED.**~~ **DECIDED: OPTION A — AUTHORIZE (Gate R2 SATISFIED)** *(2026-09-30; §19)*.

- The tranche is fully **defined and governed** at the level Gate R2 requires:
  - scope, ownership, mechanism, work items, gates, closure criteria and stop conditions are fixed in accepted §21a (`7f479bd`);
  - it rests on OQ-R-1 to OQ-R-7 (`691f079`).
- The items that are **not** yet available, including every infrastructure prerequisite, are placed by §21a.7 itself in **Gate R3**, which follows R2:
  - the implementation design and `§19` checklist;
  - the act-citation rule;
  - canonical environment designation;
  - database roles;
  - reconciliation access;
  - PostgreSQL verification.
- They therefore constrain what an R2 authorization can lead to. They do not prevent the R2 decision (§6, §11).
- Unchanged: **§21a ACCEPTED / IN FORCE; R1 SATISFIED; R2 NOT SATISFIED.**

## §2 Decision Question

**Should the Repository Owner authorize implementation of the bounded WP-23 TD-171 remediation tranche established by accepted §21a?**

Whatever the answer, this decision does **not** authorize:
- M2 or M2-P;
- Workstreams D–H;
- BAR identifier or identity redesign;
- a new authorization architecture.

## §3 Authority and Existing Decisions

| Authority | Content |
|---|---|
| WP-23 Charter §4, §7, §14, §15, §16, §20 | BAR owns registration (D2). The registering act is RO-authorized. No new authorization architecture. Existing audit. The five-gate model |
| Charter **§21a** (ACCEPTED, `7f479bd`) | The tranche: purpose, authority, scope A–K, non-reopening, responsibility, R-01–R-10, gates R1–R6, closure, prerequisites, M2 boundary, stop conditions |
| `ROD-WP23-TD-171-Remediation-Decision-Preparation.md §19` | OQ-R-1 to OQ-R-7 |
| `ROD-BAE-001-TD-171-BAR-Consumption-Decision-Preparation.md §17` | TD-171 must close before M2 authorization; BAR/WP-23 owns remediation |
| RD-23-02, RD-23-03, RD-23-04; Gate 1 CERT-F-04; Gate 5 G5-01, G5-08, C-1 | The A–C tranche model; the layered authority model; the TD-171 origin and hard condition |

No new authority model is introduced.

## §4 Current Governance State

| Item | State |
|---|---|
| §21a | ACCEPTED / IN FORCE |
| Gate R1 | SATISFIED |
| TD-171 remediation tranche | DECIDED / NOT AUTHORIZED |
| Gates R2–R6 | NOT SATISFIED |
| TD-171 | OPEN, remediation required |
| Workstreams A–C | ACCEPTED (not reopened). WP-23 OPEN |
| M2 | NOT AUTHORIZED / NOT STARTED |
| M2-P | CHARTERED / NOT AUTHORIZED / NOT STARTED |

## §5 Evidence Reviewed (2026-09-30, HEAD `7f479bd`)

**Legend:**
- DECIDED: governance decision made.
- DESIGNED: implementation design exists.
- AVAILABLE: the capability or resource exists.
- VERIFIED: independently evidenced.
- AUTHORIZED: implementation permitted.

| Area | Evidence | Status |
|---|---|---|
| **A. Governance** | §21a (scope A–K, R-01–R-10, R1–R6, 14 closure criteria, 10 stop conditions); OQ-R-1–7 | DECIDED. R1 VERIFIED (accepted). Not AUTHORIZED |
| **B. BAR implementation** | `services/bar_registration_service.py` `register()`: free-text `registering_act` (a citation, "not verified here"); no caller-authority check; `actor_id` optional; atomic ledger and registration insert (savepoint); `record_audit`/`publish_event` including `registering_act`. Test-only callers; no router | AVAILABLE (the current, unremediated behaviour) |
| | `BAR-INDEX.md` §3: **zero entries** | — |
| | Tests: `tests/test_bar_identifier_service.py`, `tests/test_bar_registration_service.py`, `tests/test_bar_transaction_safety.py` (the last enforces SQLite FKs). TD-172 records non-evidential or misnamed collision tests | AVAILABLE. Not remediation tests |
| | Implementation record: `architecture/05-Implementation/IMP-REPORT-WP-23_Enterprise_BAR_Mechanism.md` | AVAILABLE |
| **C. Production-control prerequisites** | **Database roles:** one `DATABASE_URL` (`config.py`); `Config/platform-config.yaml` notes local superuser use and an **ungranted** `auth_service_user`; no `GRANT`/`CREATE ROLE` anywhere in `Backend/`, `database/` or CI | **NOT AVAILABLE** |
| | **PostgreSQL:** no local PostgreSQL (Docker daemon unavailable; `psql` not installed). CI `.github/workflows/authservice-ci.yml` bootstrap job runs an **ephemeral** `postgres:16`. TD-176 Open | **NOT VERIFIED.** An ephemeral CI venue is AVAILABLE; no target environment |
| | **Reconciliation access:** no deployment job, target environment or controlled read access | **NOT AVAILABLE** |
| | **Canonical production environment:** a process-level classification exists (`config.py` `settings.environment`, "development" default; `ENVIRONMENT=production`/`prod` recognized by `services/bootstrap_service.py`). It designates **no** specific canonical BAR/AuthService database | DECIDED in principle (OQ-R-5). **NOT DESIGNATED** |
| **D. Governing-act mechanism** | Repository convention: CBOR-INDEX rows point to ADRs (`ADR-037`/`040`/`041`) in `architecture/07-Decisions/ADR-NNN_*.md`. **Machine-verifiable now:** the existence of a cited ADR/ROD file by identifier and path. **Not machine-verifiable now:** that its content names the identifier, reference, capability/WP, intent and authority, because there is no structured field convention. There is no governance-document check in CI | DECIDED (OQ-R-4 form). **NOT DESIGNED** (citation rule) |
| **E. Technical debt** | **TD-171:** Open. **TD-176:** Open (verify before the first real registering act). **TD-172 to TD-175** (tests, model/migration drift, allocator/overflow, identifier CHECK): Open, BAR-adjacent, **outside §21a scope** (§21a.3 excludes identifier-allocation redesign). **TD-170, TD-165:** M2-related, not relevant to the tranche | — |

## §6 R2 Preconditions

| # | Precondition | Status | Effect |
|---|---|---|---|
| 1 | §21a accepted | **SATISFIED** (`7f479bd`) | — |
| 2 | Remediation scope defined | **SATISFIED** (§21a.3) | — |
| 3 | Ownership defined | **SATISFIED** (§21a.5) | — |
| 4 | Implementation design / `§19` checklist | **OUTSTANDING** | NON-BLOCKING for R2. §21a.7 places it in **R3**. BLOCKING for R4 |
| 5 | Act-citation validation rule | **DECIDED / NOT DESIGNED** (existence is resolvable; content correspondence needs a structured convention) | NON-BLOCKING for R2. R3 item |
| 6 | Canonical production environment designation | **OUTSTANDING: external** (a classification exists; no designated database) | NON-BLOCKING for R2. **BLOCKING for R3 completion and R4** |
| 7 | Database-role provisioning | **OUTSTANDING: external; NOT AVAILABLE** | NON-BLOCKING for R2. **BLOCKING for R4** (role separation, unauthorized-write negative control) |
| 8 | Controlled reconciliation read access | **OUTSTANDING: external; NOT AVAILABLE** | NON-BLOCKING for R2. **BLOCKING for R4/R5** (environment reconciliation) |
| 9 | PostgreSQL verification | **NOT VERIFIED** (TD-176 Open; an ephemeral CI venue exists) | NON-BLOCKING for R2. **BLOCKING for closure** (§21a.8 item 9) |
| 10 | Test strategy | **OUTSTANDING** (closure criteria define what must be proven; TD-172 notes weak existing tests) | NON-BLOCKING for R2. R3 item |
| 11 | Closure and independent-review model | **SATISFIED as definition** (§21a.7–§21a.8, Charter §16). Execution future | — |
| 12 | `TECH-DEBT.md` sync and G5-08 reassessment | **Future closure requirement** (R6) | — |
| 13 | No conflict with the A–C acceptance | **SATISFIED** (§21a.4; the RD-23-02/04 notes are unchanged since `b0f5a12`) | — |
| 14 | No M2/M2-P scope contamination | **SATISFIED** (§21a.3 exclusions; §21a.10) | — |

**Conclusion.**
- Items 1–3, 11, 13 and 14 are satisfied.
- Items 4–10 are unsatisfied. By the Charter's own gate order they belong to **R3 and later**.
- **No R2 decision precondition is blocking.** Several items block implementation progress beyond R3.

## §7 Authorization Boundary (what R2 would authorize, if granted)

**It would authorize only implementation of the bounded tranche under §21a:**
- establishing the governed production registration operation;
- enforcing governing-act validation;
- removing unrestricted production registration writes;
- establishing the required database write/read separation (**in-repository specification only**; provisioning is external);
- implementing repository CI verification;
- implementing `BAR-INDEX.md` consistency verification;
- implementing environment reconciliation (**using infrastructure-provided access only**);
- implementing ungoverned-row quarantine/block handling;
- performing the required PostgreSQL verification;
- producing evidence for R3–R6.

**It would not:**
- satisfy R3–R6;
- provision infrastructure;
- designate the production environment;
- authorize any work outside §21a.3.

## §8 Implementation Scope (from §21a.6; no new scope)

| Item | Purpose | Expected evidence | Owner | Gate |
|---|---|---|---|---|
| R-01 | Governed registration operation and act validation | Valid registration; invalid/mismatched act rejected (§21a.8 items 1–2). *The citation rule is to be designed* | WP-23/BAR | R3 (design), R4, R5 |
| R-02 | Production write-path restriction | No unrestricted production `register()` path; negative control (item 5) | WP-23/BAR | R3, R4, R5 |
| R-03 | Database-role separation | Read path cannot write; write path is the only writer (item 6). *Role design at R3; provisioning external* | WP-23/BAR (specification); infrastructure (provisioning) | R3, R4, R5 |
| R-04 | Repository CI act/index verification | Index ↔ act consistency (item 3). *CI mechanism at R3* | WP-23/BAR | R3, R4 |
| R-05 | Environment reconciliation | Row ↔ index ↔ governance per environment (item 10). *Needs access* | WP-23/BAR; infrastructure (access) | R3, R4, R5 |
| R-06 | Canonical production environment designation | A designation recorded, and multi-environment issuance prevented. *External* | Infrastructure/deployment; WP-23/BAR (enforcement design) | R3 |
| R-07 | Ungoverned-row handling | Classification, quarantine/block, evidence (item 11) | WP-23/BAR | R3, R4, R5 |
| R-08 | PostgreSQL verification | TD-176-class evidence (item 9) | WP-23/BAR | R4, R5 |
| R-09 | Independent verification/review | `§19.7b` gate records (item 12) | Independent reviewers | R5 |
| R-10 | Closure and governance synchronization | TD-171 closure; `TECH-DEBT.md` sync; G5-08 reassessment (items 13–14) | WP-23/BAR (separately authorized sync) | R6 |

## §9 Explicit Exclusions (preserved from §21a.3/§21a.4)

Not authorized under any option:
- reopening Workstreams A–C;
- Workstreams D–H;
- identifier allocation redesign or BAR identity redesign (D5 unchanged), including TD-173/TD-174/TD-175 remediation;
- new authority seats or a new authorization architecture;
- a new act registry;
- M2, M2-P or BAE runtime resolution;
- a replacement/unbinding lifecycle;
- tenant-specific BAR identity;
- a new Work Package;
- any Business Activity registration or identifier assignment.

## §10 Dependencies / External Preconditions

These sit outside the repository team's current authority. They are **not downgraded**: each must exist before the gate named.

| Dependency | Owner | Required before |
|---|---|---|
| Canonical production environment designation (OQ-R-5) | Infrastructure/deployment | R3 completion (§21a.7), and any environment reconciliation or governed write to a deployed environment |
| Database-role provisioning (OQ-R-3) | Infrastructure/deployment | R4 (role-separation and unauthorized-write evidence) |
| Controlled read-only reconciliation access (OQ-R-6) | Infrastructure/deployment | R4/R5 environment reconciliation |
| PostgreSQL environment for verification | CI ephemeral venue exists. The target environment is infrastructure | R5/closure (TD-176) |
| Deployment/CI access for the governed operation | Infrastructure/deployment | R4 controlled deployment verification |

## §11 Gates and Verification

| Gate | State | What R2 does |
|---|---|---|
| R1: amendment accepted | **SATISFIED** (`7f479bd`) | — |
| **R2: tranche authorized** | **THIS DECISION** | Grants permission to implement within §7. **Satisfies R2 only** |
| R3: design and readiness complete | NOT SATISFIED | Unaffected. Needs the design, `§19` checklist, citation rule, role and reconciliation design, and confirmed environment designation and infrastructure |
| R4: implementation and controlled deployment verification | NOT SATISFIED | Unaffected. Needs R3 and the external prerequisites |
| R5: independent verification/review | NOT SATISFIED | Unaffected |
| R6: closure evidence and governance synchronization | NOT SATISFIED | Unaffected. Only R6 permits TD-171 closure |

## §12 Risks / Stop Conditions

**Carried forward:** all §21a.11 stop conditions.

**Evidence-supported implementation risks:**

| Risk | Evidence |
|---|---|
| The unrestricted `register()` path persists into production | `register()` has no restriction today (§5 B) |
| Role separation cannot be established | No role pattern; single `DATABASE_URL`; `auth_service_user` ungranted (§5 C) |
| The canonical environment cannot be identified | No designated database. The environment classification is process-level only (§5 C) |
| Persistent state cannot be reconciled | No deployment environment or access (§5 C) |
| Governing acts cannot be machine-verified beyond existence | There is no structured act convention (§5 D) |
| Ungoverned existing rows | Deployed databases cannot be inspected (remediation ROD §11) |
| PostgreSQL verification gaps | No local PostgreSQL; TD-176 Open (§5 C, E) |
| **Scope leakage into BAR-adjacent debt** | The tranche touches the same service and tables as TD-172/TD-173/TD-174/TD-175, which are outside §21a.3. Remediating them would need separate authorization |
| Scope leakage into M2/M2-P | §21a.10; RD-M2-07 |
| Accidental reopening of A–C | §21a.4 |

## §13 Authorization Options (neutral; all procedurally valid under §21a.7)

*(2026-09-30: the Repository Owner selected **Option A**; §19. All three options are preserved as presented.)*

| Option | Effect | Procedural basis |
|---|---|---|
| **A: Authorize** | R2 satisfied. Implementation may proceed within §7, gated by R3–R6 as written. External prerequisites are handled at R3/R4 | §21a.7 already places design and infrastructure confirmation in R3 |
| **B: Authorize with explicit preconditions** | R2 satisfied, but implementation may not begin until named prerequisites exist (for example environment designation, role provisioning, read access, a PostgreSQL venue) | Adds conditions stricter than §21a.7 without changing it. Valid as an RO decision |
| **C: Do not authorize yet** | R2 stays NOT SATISFIED. The tranche stays DECIDED / NOT AUTHORIZED until named blockers are resolved | Always available. TD-171 stays OPEN, and M2 stays blocked |

No option is selected.

## §14 Decision Forms (copy-pasteable; not pre-filled)

Each form preserves: §21a acceptance; the A–C acceptance; TD-171 closure only at R6; M2 NOT AUTHORIZED / NOT STARTED; M2-P CHARTERED / NOT AUTHORIZED / NOT STARTED; R3–R6 unsatisfied.

**Option A**
> Repository Owner decision, [date]: Gate R2 of WP-23 Charter §21a is SATISFIED. The TD-171 remediation tranche is AUTHORIZED for implementation strictly within §21a.3 and the authorization boundary of this package's §7. Gates R3–R6 remain NOT SATISFIED and govern progress. §21a remains ACCEPTED / IN FORCE. Workstreams A–C remain accepted and are not reopened. TD-171 remains OPEN until closed at R6. This decision does not authorize M2 (NOT AUTHORIZED / NOT STARTED), M2-P (CHARTERED / NOT AUTHORIZED / NOT STARTED), Workstreams D–H, or any infrastructure provisioning.

**Option B**
> Repository Owner decision, [date]: Gate R2 of WP-23 Charter §21a is SATISFIED, subject to the following preconditions, which must be evidenced before any implementation begins: [list]. Until they are evidenced, no implementation may start. Otherwise identical to Option A: R3–R6 NOT SATISFIED; §21a ACCEPTED; A–C not reopened; TD-171 OPEN until R6; M2 and M2-P unauthorized.

**Option C**
> Repository Owner decision, [date]: Gate R2 of WP-23 Charter §21a is NOT granted at this time. The TD-171 remediation tranche remains DECIDED / NOT AUTHORIZED pending: [list]. §21a remains ACCEPTED / IN FORCE. A–C are not reopened. TD-171 remains OPEN. M2 remains NOT AUTHORIZED / NOT STARTED; M2-P remains CHARTERED / NOT AUTHORIZED / NOT STARTED.

## §15 Post-Authorization Controls (if A or B is granted; none started here)

1. **Implementation-readiness gate (R3):** a `CLAUDE.md §19` checklist for the tranche; Gap Analysis; Architectural Impact Assessment. The design is frozen before R4.
2. **Design deliverables:** the act-citation rule; the governed-operation invocation form; the role design; the CI verification design; the reconciliation design; the quarantine design; the test strategy against §21a.8.
3. **External confirmation:** environment designation, roles and access confirmed before R3 completes.
4. **Implementation boundary:** exactly §7. Stop on any §21a.11 condition or §12 risk materializing.
5. **Evidence capture:** in the existing WP-23 implementation record (`IMP-REPORT-WP-23 …`), in a tranche section, per the existing convention.
6. **Governance synchronization** (`WPR-001` WP-23 row, `TECH-DEBT.md`): only by separate authorization.

## §16 Traceability

| Source | Applied in |
|---|---|
| Charter §21a (§21a.3–§21a.12), accepted `7f479bd` | §1, §6–§12 |
| OQ-R-1 to OQ-R-7 (remediation ROD §19, `691f079`) | §3, §8, §10 |
| TD-171; TD-176; TD-172–TD-175 | §5 E, §6, §12 |
| A–C acceptance (RD-23-02; C-3; `b0f5a12`); RD-23-03; RD-23-04 | §3, §6 item 13, §9 |
| TD-171 decision ROD §17 | §3 |
| M2/M2-P governance (IRA-BAE-001-M2 §13; RD-M2-07) | §2, §9, §12 |
| BAR artifacts: `services/bar_registration_service.py`; the BAR tests; `BAR-INDEX.md`; `IMP-REPORT-WP-23 …`; `config.py`; `services/bootstrap_service.py`; `Config/platform-config.yaml`; `.github/workflows/authservice-ci.yml` | §5 |

No new decision ID is introduced.

## §17 Open Questions / Outstanding Items

**Governance decisions already made:** OQ-R-1 to OQ-R-7 (not reopened).

**The decision now required:** R2 (§13).

**Implementation design questions (R3; not RO decisions unless escalated):**
- the structured, machine-verifiable form of the ADR/ROD registering act and its citation rule;
- the invocation form of the governed operation;
- whether the existing `ENVIRONMENT` classification participates in enforcing single canonical issuance;
- the tranche evidence record's placement within `IMP-REPORT-WP-23`.

**External infrastructure prerequisites:**
- canonical production database designation;
- database-role provisioning;
- controlled read-only reconciliation access;
- a target PostgreSQL environment;
- deployment/CI access for the governed operation.

## §18 Readiness Statement

~~**READY FOR RO DECISION.**~~ *(2026-09-30: **DECIDED**, Option A; §19.)*
- R2 is now a decision point. All R2-level definitions are in accepted §21a, and every unsatisfied item is placed by §21a.7 in R3 or later (§6, §11).
- **Preparing this package does not authorize the tranche.**
- §21a is ACCEPTED / IN FORCE; R1 SATISFIED; **R2 NOT SATISFIED**; R3–R6 NOT SATISFIED.
- TD-171 is OPEN. M2 is NOT AUTHORIZED / NOT STARTED. M2-P is CHARTERED / NOT AUTHORIZED / NOT STARTED.

## §19 Repository Owner Decision Record — Gate R2 (2026-09-30)

**Recorded** by direct Repository Owner instruction ("Record the Repository Owner decision for Gate R2 of the WP-23 TD-171 remediation tranche"). The decision is recorded as stated and is not reinterpreted. **Governance recording only; no implementation is performed by this record.**

### 19.1 Decision

| Field | Recorded |
|---|---|
| **Decision** | **OPTION A — AUTHORIZE** |
| **Gate** | **R2**: now **SATISFIED** |
| **Basis** | Accepted WP-23 Charter §21a (`7f479bd`); this authorization-preparation ROD (§1–§18); OQ-R-1 to OQ-R-7 (`691f079`) |
| **Scope** | **Only** implementation of the bounded WP-23 TD-171 remediation tranche defined by §21a, within this ROD's §7 boundary |
| **Not authorized** | Workstreams D–H; reopening Workstreams A–C; BAR identifier redesign; identifier-assignment redesign; new authority seats; new authorization architecture; a new act registry; tenant-specific BAR identity; a replacement/unbinding lifecycle; M2 implementation; M2-P implementation; BAE runtime-resolution implementation; any unrelated technical-debt remediation |
| **R3–R6** | **Remain NOT SATISFIED.** They are mandatory future gates and are not collapsed: R3 (design/readiness); R4 (implementation and controlled deployment verification); R5 (independent verification/review); R6 (closure evidence and governance synchronization) |
| **TD-171** | **OPEN** until the R6 closure criteria (§21a.8) are satisfied |
| **M2 / M2-P** | Unchanged. M2 **NOT AUTHORIZED / NOT STARTED**; M2-P **CHARTERED / NOT AUTHORIZED / NOT STARTED** |

### 19.2 Conditions of the authorization (as recorded)

1. The implementation team must remain strictly within §21a.
2. The existing A–C acceptance remains intact and is not reopened.
3. The machine-verifiable governing-act citation rule must be designed and approved within R3 before implementation relying on that rule proceeds.
4. The canonical production BAR/AuthService environment must be explicitly designated before production reconciliation or identifier authority is established.
5. The required database-role separation must be designed and provisioned before production write-path enforcement is accepted.
6. Controlled, read-only reconciliation access must be provided by the infrastructure/deployment owner before environment reconciliation is performed.
7. PostgreSQL verification required by TD-176 must be completed before closure.
8. Any existing ungoverned persistent rows, if discovered, must be quarantined/blocked, and must not be silently adopted, deleted or rewritten.
9. Any newly discovered scope outside §21a must **STOP** and needs separate authorization.
10. R3 must independently confirm implementation readiness before implementation proceeds beyond the applicable design boundary.
11. R5 independent verification remains mandatory.
12. TD-171 does not close at R2. It remains OPEN until the R6 closure criteria are satisfied.
13. The G5-08 severity reassessment remains a later closure activity. It must not be performed, or represented as completed, now.
14. M2 remains NOT AUTHORIZED / NOT STARTED. M2-P remains CHARTERED / NOT AUTHORIZED / NOT STARTED.

**Technical-debt boundary.**
- This authorization does **not** authorize remediation of **TD-172, TD-173, TD-174 or TD-175**.
- If implementation encounters one of them and work on it is needed, implementation **STOPS** and obtains separate authorization, unless §21a's existing scope explicitly covers it.

### 19.3 Gate state after this decision

| Gate | State |
|---|---|
| R1: amendment accepted | SATISFIED (`7f479bd`) |
| **R2: tranche authorized** | **SATISFIED** (this record) |
| R3: design/readiness | NOT SATISFIED |
| R4: implementation and controlled deployment verification | NOT SATISFIED |
| R5: independent verification/review | NOT SATISFIED |
| R6: closure evidence and governance synchronization | NOT SATISFIED |

### 19.4 Governance synchronization noted (not performed)

- **WP-23 Charter §21a.7** still shows R2 as "Not satisfied" (Charter text at `7f479bd`).
- This ROD is the authoritative R2 decision record.
- Reflecting it in the Charter, the `WPR-001` WP-23 row and `IMP-REPORT-WP-23` needs **separate authorization**. It is not performed here, per the instruction not to modify the Charter further.

### 19.5 State summary

| Item | State |
|---|---|
| §21a | ACCEPTED / IN FORCE |
| TD-171 remediation tranche | **AUTHORIZED** (R2), subject to §19.2. **R3–R6 NOT SATISFIED** |
| TD-171 | **OPEN** until R6 |
| Workstreams A–C | ACCEPTED, not reopened. WP-23 OPEN |
| M2 | NOT AUTHORIZED / NOT STARTED |
| M2-P | CHARTERED / NOT AUTHORIZED / NOT STARTED |

*~~End of decision preparation. No implementation. Nothing staged, committed or pushed.~~ End of decision record. Gate R2 SATISFIED (Option A, 2026-09-30). R3–R6 NOT SATISFIED. TD-171 OPEN. No implementation performed.*
