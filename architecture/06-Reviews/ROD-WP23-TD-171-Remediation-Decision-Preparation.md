# ROD-WP23 — TD-171 Remediation (BAR Registration Governance and BAR-INDEX Reconciliation) — Decision Preparation

**Work Package:** `WP-23` (Enterprise BAR Mechanism). The owner is BAR/WP-23, per the TD-171 decision (`ROD-BAE-001-TD-171-BAR-Consumption-Decision-Preparation.md §17`, OQ-171-2).
**Prepared:** 2026-09-30, by Repository Owner instruction ("Prepare the WP-23 TD-171 Remediation Decision Package"). Baseline HEAD: `72cfc10`.
**Status:** ~~**READY FOR DECISION — NO OPTION SELECTED.** A recommendation appears in §14. It is not a decision.~~ **DECIDED — WP-23 TD-171 REMEDIATION** *(2026-09-30, Repository Owner; §19)*: vehicle **B**, a new WP-23 remediation tranche; mechanism **D**, a governed deployment-time operation plus CI verification and reconciliation. **No implementation is authorized. TD-171 remains OPEN.**
- *(2026-09-30: the preparation in §1–§18 is preserved as the analysis presented for decision.)*

**Nothing is changed or authorized.**
- No BAR code, test, migration or `BAR-INDEX.md` change. No BAE M2 or M2-P change.
- No change to `TECH-DEBT.md`, the IRA, WP-BAE-001, the WP-23 Charter, ADRs or the Master Technical Architecture.
- **TD-171 remains OPEN** (remediation required). **M2 remains NOT AUTHORIZED / NOT STARTED. M2-P remains CHARTERED / NOT AUTHORIZED / NOT STARTED.**

---

## §1 Decision Statement

**How is TD-171 to be remediated, and by which WP-23 vehicle?** The remediation must:
- establish a trustworthy relationship between each Business Activity's governing registering act and its `bar_registration` row (GAP-23-03-1);
- reconcile `bar_registration` with `BAR-INDEX.md` (GAP-23-03-2);
- be verified to the standard that allows TD-171 to close.

TD-171 closure is a prerequisite to M2 authorization (OQ-171-1, OQ-171-3).

## §2 Current Status

*(2026-09-30: superseded by §19. The decisions are recorded; the text below records the status at preparation.)*

**READY FOR DECISION.** None of the stop conditions applies:
- TD-171 is traced to its source evidence (§4).
- No new constitutional authority role is needed. The authority model is already decided: WP-23 Charter §7 and §14; RD-23-03 (§10).
- Canonical BAR identity authority (D5) is unchanged.
- The B2 binding architecture is untouched.
- Governed data is established. Deployed data cannot be inspected; §11 turns that into a closure criterion.
- The authority models found are consistent.

One genuine open design question is identified: which environment's identifier issuance is canonical for `BAR-INDEX.md` (§6.3, OQ-R-5). It is a decision, not a contradiction.

## §3 TD-171: the exact problem

From `TECH-DEBT.md` (HEAD):
- **"No enforcement links a registering act to a runtime BAR registration, and no reconciliation exists between `bar_registration` and `BAR-INDEX.md`"**.
- `register()` "accepts any non-blank free-text `registering_act` and verifies it against no governance act".
- It "performs no caller-authority check; `actor_id` is optional; no router exists".
- It "does not write `BAR-INDEX.md`, and no check compares the table with the index".
- Hard precondition: it becomes a fail-open governance and security boundary once anything reads `bar_registration` for execution eligibility.
- Category Security/Governance. Priority High. Severity Medium. Open. Owner AuthService.

**Decided on 2026-09-30:**
- TD-171 must close before M2 authorization.
- BAR/WP-23 owns the remediation.
- There is no BAE compensation.
- The G5-08 severity reassessment is a future obligation.
- `TECH-DEBT.md` synchronization is separate.

## §4 Evidence and Origin (re-verified against the current repository)

| Artifact | Content |
|---|---|
| `ROD-WP-23-AC-BAR-Registry-Authority-Decision-Preparation.md` §0.1 (RD-23-03, Option D) | Layers: 1, registering act (governance authority); 2, `bar_registration` (runtime execution registration; "must not" be treated as proof of authorization by a row's existence alone); 3, `BAR-INDEX.md` (catalogue); 4, reconciliation (mechanism not decided) |
| Same, §0.4 | **GAP-23-03-1:** "Any in-process caller can create a runtime registration with no governance act." **GAP-23-03-2:** no table↔index reconciliation. GAP-23-03-3 (docstrings) is closed |
| `CERT-WP-23-AC …` CERT-F-04 (Gate 1, Medium) | Confirms GAP-1/2 at `services/bar_registration_service.py`. Deferrable only if it "closes before any execution-eligibility consumer is built" |
| `RRA-WP-23-AC …` G5-01, **G5-08**, **C-1** (Gate 5) | Register as TD with the hard precondition. Reassess severity against `§19.8.7` High when the consumer is built |
| `IRA-WP-23-AC …` (A–C acceptance) | TD-171's hard condition carries forward. WP-23 remains OPEN |
| `WP-23_…_Charter.md` §7 | Registering act: "a discrete, **Repository-Owner-authorized act per Business Activity**, citing its own Charter/`IMP-REPORT`/WP, **that creates its BAR index entry and triggers its own identifier issuance**" (mirroring the CBOR-ADR pattern) |
| Same, §14 | "registration authority (**a Repository-Owner-authorized registering act**, mirroring the CBOR-ADR pattern) … **No new authorization architecture is created**" |
| Same, §15 | Audit reuses `record_audit`/`publish_event`; no C-114 |
| Same, §21 row C (as corrected by RD-23-04) | Acceptance: "Each act cites its own Charter/`IMP-REPORT`/WP; collision-checked before registering." Test: "Governance-artifact review per act." Includes the runtime store |
| Same, §20, §22 | Authorized scope is Workstreams A–G. A–C is a separately closable tranche (RD-23-02). WP-23 remains OPEN |
| `BAR-INDEX.md` §3, §8 | Eight columns: Identifier, Reference, Owning Capability, Owning Work Package, Registration Status, Registering Act, Registration Date, Retroactive. **Zero entries.** §8: add a row "when, and only when" a registering act is performed |

## §5 Current BAR Write-Path Analysis (`services/bar_registration_service.py`)

- `register(business_activity_reference, owning_capability, owning_work_package, registering_act, is_retroactive, actor_id=None)`:
  - validates non-blank fields;
  - checks the (work package, reference) collision;
  - allocates `BA-NNNNNN` and inserts the ledger row and registration row atomically (savepoint);
  - emits `record_audit` (SUCCESS/DENIED/FAILED, with `registering_act` in metadata, `actor_id or "SYSTEM"`) and `publish_event`.
- Its docstring states that `registering_act` "is a citation, not verified here". It also says a future Workstream F, or a capability's own BA implementation, "will call `register()` directly".
- **Callers today:** tests only. There is no router, and no other module writes BAR tables (search, 2026-09-30).

**Which characteristics are TD-171 and which are observations:**

| Characteristic | Classification | Reason |
|---|---|---|
| Free-text `registering_act`, verified against no act | **Core (GAP-23-03-1)** | The missing Layer 1 → Layer 2 link |
| No caller-authority check | **Contributing condition** | It is why "any in-process caller" can create a row. Under Charter §14, registration authority is the **act**, not a runtime caller role. The remediation must ensure rows arise **only from a governed act**. A runtime role check is one possible control, not a requirement of the authority model (§10) |
| `actor_id` optional | **Observation** (audit completeness) | Audit defaults to `SYSTEM`. The executor's identity is not the authority (compare FO-3 IP-3: approval is carried by the act) |
| No router | **Mitigating fact** | It limits exposure today. It is not a control |
| Service does not write `BAR-INDEX.md` | **By design** (D7; Layer 3 is governance-maintained, index §8) | The gap is Layer 4 reconciliation (GAP-23-03-2), not the service failing to write the index |

## §6 Current BAR-INDEX Analysis

### 6.1 Canonical source per field

| Field | Canonical source | Reconcile? |
|---|---|---|
| Business Activity Identifier | The runtime ledger (`register()` issues it, D5) | **Yes:** a one-to-one correspondence of identifiers between index and table |
| Business Activity Reference, Owning Capability, Owning Work Package, Retroactive | The **registering act** (Layer 1; Charter §7; derived from the Charter, `IMP-REPORT` or WP) | **Yes:** index and row must both equal the act |
| Registering Act | The act's own identifier | **Yes:** index and row cite the same act, which must exist |
| Registration Status | Two-state (row present = `REGISTERED`; D2) | **Yes:** the index says "Registered" exactly when a row exists |
| Registration Date | Runtime `registered_at` | Informational. Date-level agreement at most |

### 6.2 Where reconciliation can run (repository evidence)

- **CI (repository only):** it can verify index ↔ act. Each index row's act exists in the repository and names the same reference, capability, WP and retroactive flag, and identifiers are unique in the index. CI **cannot** read a deployed `bar_registration`: there is no target environment and no deployment job (`.github/workflows/authservice-ci.yml`). That is the same limitation RD-M2-08 records for FQ-6.
- **Deployment-time (governed operation):** the operation that executes an act can verify, at the time of the write, that the row it created matches the act, and can produce the index row content for the governed index change.
- **Environment check (row ↔ index):** this requires read access to each environment's `bar_registration`, an external prerequisite of the RD-M2-08 class (OQ-R-6).
- **Periodic:** no scheduler exists in the repository. Not evidenced.

### 6.3 Open design question: which issuance is canonical

- `register()` allocates identifiers from each database's own ledger.
- `BAR-INDEX.md` is a single repository document.
- With more than one persistent environment, the same act could receive different identifiers in different environments.
- The repository has no deployment topology, so this has not yet arisen.
- D5 is not changed by answering it. But the reconciliation design must fix which environment's issuance the index records, and how other environments relate. **→ OQ-R-5.** *(2026-09-30: decided: a single designated canonical production environment; §19.1.)*

## §7 Governance-Act Model

- **Already decided:** Charter §7 and §14 say the act is a Repository-Owner-authorized record mirroring the **CBOR-ADR pattern**. `CBOR-INDEX.md` rows point to ADRs such as `ADR-037`, `ADR-040` and `ADR-041`.
- **Minimum durable relationship (RQ-171-1):** act identifier ↔ (reference, capability, WP, retroactive) ↔ row (identifier, same fields, `registering_act` = act identifier) ↔ index row (same identifier and fields, pointer to the act).
- **Verification level options:**

| Option | Verdict |
|---|---|
| Citation only | The current state; TD-171 itself |
| **Verified against repository governance records** (the act exists, is RO-authorized, and names the fields) | **Existing mechanism.** Mirrors CBOR-ADR. The same class as FQ-2 (a) for bindings (input only, per OQ-171-2) |
| A canonical, database-backed act registry | A **new architectural layer** and a new governed object. It would need its own ADR and decision. Not required by any rule found |

## §8 Remediation Options

Two independent axes: **vehicle** (who delivers it, and under which WP-23 scope) and **mechanism** (how the control works).

### 8.1 Vehicle options

| | **A: extend Workstream C** | **B: new WP-23 remediation tranche** (working label "C-R", name for the RO) | **C: new Work Package** |
|---|---|---|---|
| Fit | Workstream C *is* the registering-act convention (Charter §7, §21 row C). TD-171 is the unfinished part of it | Same content. It leaves the A–C tranche's ACCEPTED record (RD-23-02, C-3) intact | A separate "BAR Governance Integrity" WP |
| Governance impact | **Reopens an ACCEPTED tranche** (RD-23-02 terminal state) and its gate record | Needs a **Charter §21/§20 amendment** by the RO to add the tranche. A–C stay frozen | Splits BAR registration ownership from BAR (D2: BAR owns registration) against "one capability, one owner"; needs a new Charter, IRA and registration |
| Scope impact | Within the existing §20 A–G authorization | A bounded addition to WP-23. WP-23 remains OPEN, so nothing is reopened | New scope container |
| Verification burden | Re-gates C (and the tranche) | Its own five-gate sequence (Charter §16; `§19.7b`) | A full new WP lifecycle |
| Effect on M2 | Closure gates M2 (unchanged) | Same | Same, with more lead time |
| ADR/ROD | Decision record; no ADR required by rule | Decision record plus Charter amendment; no ADR required by rule | New Charter; possibly an ADR |

### 8.2 Mechanism options

| | **D: governed data operation plus CI verification** (no new runtime authority layer) | **R1: runtime role check** (`require_platform_admin` on a new route or caller) | **R2: authority-holder seat** (`require_authority_holder`) | **R3: database-level act enforcement** |
|---|---|---|---|---|
| Summary | Rows are created only by a governed, reviewed deployment-time operation executing a specific RO act. CI verifies index ↔ act. The operation verifies row ↔ act at write time. Row ↔ index is checked against each environment's table. Existing `record_audit`/`publish_event` | Add an HTTP route or caller gated by a claims check | Gate `register()` by a live authority-holder lookup | FK or constraint from row to an act table |
| Fit to authority model | **Matches Charter §7/§14** (the authority is the RO act; "no new authorization architecture") and the approved FO-3 pattern for bindings (FQ-1 (c), FQ-2 (a); input only) | Claims-only is the same fail-open class TD-171 describes (FO-3 FQ-1 (a) analysis). Adds a runtime write path the Charter does not require | AI-001/AI-002 are C-040 authorities, and AI-002 is unpopulated (TD-157). A BAR seat would be a **new authority identity**, which is a stop trigger. Excluded | Needs a canonical act registry (§7), a new architecture layer. Excluded unless separately decided |
| Security/control | Needs a control ensuring **only** the governed operation calls `register()` (sub-options: DB-role separation, the FQ-7 analogue, which is an infrastructure prerequisite; and/or a CI static check that no non-test caller of `register()` exists outside the governed operation) | Weak | — | Strong but needs new architecture |
| Data/backfill | None (§11) | None | — | Needs act rows for every registration |

## §9 Ownership and WP-23 Scope (RQ-171-4)

- **Owner:** BAR/WP-23 (decided, OQ-171-2).
- **Scope fit:** the content is squarely Workstream C (Charter §7: the act "creates its BAR index entry and triggers its own identifier issuance"; §21 C acceptance "each act cites its own Charter/`IMP-REPORT`/WP").
- **Vehicle choice:** turns on whether to reopen the accepted A–C tranche (Option A) or add a tranche (Option B). Option C conflicts with D2 single ownership.
- **Relation to other workstreams:**
  - Workstream F (retroactive registrations) is the first real caller of `register()`, so it must follow the remediated mechanism.
  - Workstream G (verification and audit wiring) depends on A–F and does not fit a TD-171 fix delivered ahead of F.

## §10 Authority Model (RQ-171-5)

- **No runtime authority check is required by the authority model.** Registration authority is the Repository-Owner-authorized registering act (Charter §14; RD-23-03 Layer 1).
- The control TD-171 lacks is that **a row can exist only as the execution of a verified act**.
- Existing mechanisms reviewed:
  - `require_platform_admin`: claims-only;
  - `require_authority_holder`: AI-001 and AI-002 only, both C-040-scoped;
  - `enforce_approval_authority`: organization-scoped, while BAR is platform-global;
  - the `tenant_registry` runtime-gated write.
- None is designed for BAR registration. Adopting any of them as the BAR authority would either reproduce TD-171's fail-open class or need a **new authority identity** (a stop condition). Mechanism D needs neither.

## §11 Data / Backfill Analysis (RQ-171-7, RQ-171-8)

| Data class | Finding (2026-09-30) |
|---|---|
| Migration-defined data | None. BAR migrations `a7b8c9d0e1f2` and `b8c9d0e1f2a3` create tables only |
| Repository-seeded data | None. No script or bootstrap writes BAR tables |
| `BAR-INDEX.md` | **Zero entries** (§3; closing status line) |
| Governed registrations (RO registering acts) | **None performed.** Charter §19, and the 21-row and C-024 BA-01 records, show none authorized |
| Test fixtures | Rows are created only in test databases (`tests/test_bar_registration_service.py`, `tests/test_bar_transaction_safety.py`) |
| Local development file | `Backend/Services/AuthService/dev_manual_check.db` (untracked, git-ignored, dated 2026-07-17, before BAR). **No `bar_*` tables** (read-only inspection) |
| Deployed databases | **Cannot be inspected.** No PostgreSQL or deployment environment is available to this session |

**Conclusion:**
- No governed registration exists, so **no governed backfill is required**.
- Any row in a deployed database would have been created without a registering act, and so would be ungoverned by definition.
- Its treatment (quarantine, removal, or re-registration through a real act) needs a **separate authorization**. No destructive operation is proposed.
- **Closure criterion (§12):** each persistent environment is verified to contain only act-reconciled rows, or none, before TD-171 closes.

## §12 Verification and Closure Criteria (RQ-171-9)

TD-171 may close only when all of the following hold, verified by the remediation vehicle's own `§19.7b` gates (Charter §16):
1. **Positive path:** a real or fixture RO act executed by the governed operation yields a row whose fields equal the act, plus a matching index row.
2. **Missing or invalid act:** a citation to a nonexistent act, or an act not naming the reference, capability or WP, is rejected before any row exists. CI fails on an index row whose act is missing or mismatched.
3. **Mismatched index:** a row without an index entry, an index entry without a row, or any field disagreement is detected by the reconciliation check.
4. **Duplicate:** existing collision and uniqueness guards still hold (unchanged).
5. **Unauthorized attempt:** a write outside the governed operation is prevented by the chosen control, either database role or static check (OQ-R-3). A negative-control probe proves it.
6. **Rollback:** a failure at any step leaves no row, no ledger entry and no index change (the existing savepoint behaviour plus the operation's own atomicity).
7. **Audit:** `record_audit`/`publish_event` evidence cites the act (existing; verified present).
8. **PostgreSQL:** criteria 1–6 are verified on PostgreSQL/asyncpg. This interacts with TD-176, which must be verified "before the first real registering act".
9. **Environment state:** §11's criterion is met for every persistent environment.
10. **Independent review:** fresh-context certification, V&V (with negative controls against the pre-fix code), and release readiness (`§19.7b`).
11. **Register synchronization:** `TECH-DEBT.md` is updated by separate authorization (OQ-171-5). The G5-08 severity reassessment is performed at the consumer gate (OQ-171-4).

## §13 M2 Boundary (RQ-171-10)

- **M2 must:**
  - consume only `BarRegistrationRepository.get_by_identifier` through the read-only `RegistrationSource`;
  - require the `REGISTERED` state;
  - fail (raise or terminate) rather than infer registration;
  - remain read-only.
- **M2 must not:**
  - validate governing acts;
  - reconcile `BAR-INDEX.md`;
  - repair, write or create BAR rows;
  - compensate for TD-171 in any way.
- **Before M2 can consume BAR registration:** TD-171 is closed under §12, and M2 is separately authorized (with every other §13.1 prerequisite).

## §14 Recommended Option (not a decision)

*(2026-09-30: the Repository Owner selected vehicle B and mechanism D; §19.1.)*

**Vehicle: Option B**, a new WP-23 remediation tranche added by a Charter amendment. It keeps the ACCEPTED A–C record intact, keeps ownership with BAR (D2), and gives the fix its own five-gate verification.
- Option A is the closest content fit, but it reopens an accepted tranche.
- Option C splits ownership.

**Mechanism: Option D:**
- a governed registering act (ADR/ROD-style repository record, mirroring CBOR-ADR);
- execution only through a governed, reviewed deployment-time operation;
- CI verification of index ↔ act;
- write-time row ↔ act verification;
- environment row ↔ index reconciliation;
- existing audit.

It matches Charter §7/§14 and RD-23-03 without a new authority role or act registry. R1 is weak; R2 and R3 need new architecture.

## §15 Open Repository Owner Decisions

*(2026-09-30: OQ-R-1 to OQ-R-7 are decided; §19. The table is preserved as presented.)*

| ID | Question | Evidenced options |
|---|---|---|
| **OQ-R-1** | Vehicle | A (extend C, reopening the accepted tranche); **B** (new tranche plus Charter amendment); C (new WP) |
| **OQ-R-2** | Mechanism | **D**; R1; (R2 and R3 excluded without new architecture) |
| **OQ-R-3** | Control restricting `register()` to the governed operation | Database-role separation (an infrastructure prerequisite, as FQ-7); CI static caller check; both |
| **OQ-R-4** | Act form | ADR/ROD-style record per registration (CBOR-ADR mirror); a BAR-specific registering-act series within the repository |
| **OQ-R-5** | Canonical issuance environment for `BAR-INDEX.md` (§6.3) | Designate one persistent environment as canonical; alternatives to be defined. D5 is unchanged |
| **OQ-R-6** | Environment row ↔ index reconciliation access | Treat it as an external operational prerequisite (as RD-M2-08); or scope infrastructure separately |
| **OQ-R-7** | Treatment of any ungoverned row found in a deployed environment | Separate authorization at that time (quarantine or removal, or re-registration through an act) |

## §16 Traceability

| Source | Used in |
|---|---|
| `TECH-DEBT.md` TD-171 (and TD-157, TD-176) | §3, §10, §12 |
| RD-23-03 (`ROD-WP-23-AC …` §0.1, §0.2, §0.4) | §4, §5, §7 |
| CERT-F-04; G5-01, G5-08, C-1; A–C acceptance (`IRA-WP-23-AC …`) | §4, §12 |
| WP-23 Charter §7, §14, §15, §16, §20, §21 (RD-23-04 note), §22 (RD-23-02 note) | §4, §7–§10 |
| `BAR-INDEX.md` §3, §8 | §4, §6 |
| `services/bar_registration_service.py`; `repositories/bar_registration_repository.py`; BAR migrations; BAR tests | §5, §11 |
| `ROD-BAE-001-TD-171-BAR-Consumption-Decision-Preparation.md §17` (OQ-171-1 to OQ-171-5) | §1, §3, §9, §13 |
| FO-3 (`TDS-BAE-001-M2-FO3 …` FQ-1 (c), FQ-2 (a), FQ-7, IP-3) | §5, §7, §8 (input only) |
| RD-M2-08 (`ROD-BAE-001-M2-Binding-Infrastructure-Ownership …` §11) | §6.2, OQ-R-6 |
| `IRA-BAE-001-M2` §13.1, §16.H; RD-M2-05 §21 | §13 |
| `dependencies.py` (`require_platform_admin`, `require_authority_holder`, `enforce_approval_authority`); `observability.py` | §5, §10 |
| `.github/workflows/authservice-ci.yml` | §6.2 |
| `CLAUDE.md` §19.7b, §19.8.5, §19.8.7 | §12 |

## §17 Evidence Inventory

| Evidence | Location |
|---|---|
| TD-171 | `architecture/06-Reviews/TECH-DEBT.md` (HEAD `72cfc10`) |
| TD-171 decision | `architecture/06-Reviews/ROD-BAE-001-TD-171-BAR-Consumption-Decision-Preparation.md` §17 |
| RD-23-03, GAP-23-03-1/2 | `architecture/06-Reviews/ROD-WP-23-AC-BAR-Registry-Authority-Decision-Preparation.md` §0 |
| Gate 1, Gate 5, acceptance | `CERT-WP-23-AC_…`, `RRA-WP-23-AC_…`, `IRA-WP-23-AC_…` (`architecture/06-Reviews/`) |
| Charter | `architecture/05-Implementation/WP-23_Enterprise_BAR_Mechanism_Implementation_Charter.md` |
| Index | `architecture/00-Governance/BAR-INDEX.md` |
| Write path | `Backend/Services/AuthService/services/bar_registration_service.py` |
| Read path | `Backend/Services/AuthService/repositories/bar_registration_repository.py` |
| Data state | Migrations `2026_09_22_0900-…`, `2026_09_22_1000-…`; `scripts/`; `dev_manual_check.db` (read-only inspection); repository search, 2026-09-30 |

## §18 Readiness Statement

~~**READY FOR DECISION — NO OPTION SELECTED.**~~ *(2026-09-30: **DECIDED**; §19.)*
- **Recommended:** vehicle B with mechanism D.
- **Seven open decisions:** OQ-R-1 to OQ-R-7.
- The remediation itself is **not authorized** by this document. After the decision, it needs:
  - a Charter amendment (under B);
  - an implementation authorization;
  - its own `§19` checklist.

**TD-171: OPEN (remediation required). M2: NOT AUTHORIZED / NOT STARTED. M2-P: CHARTERED / NOT AUTHORIZED / NOT STARTED.**

## §19 Repository Owner Decision Record (2026-09-30)

**Recorded** by direct Repository Owner instruction ("Record the Repository Owner decisions for OQ-R-1 through OQ-R-7"). Each decision is recorded as stated and is not reinterpreted.

**Governance only.** No remediation implementation. No change to BAR code, tests, migrations, `BAR-INDEX.md`, `TECH-DEBT.md`, the WP-23 Charter, the IRA, WP-BAE-001, M2 or M2-P. No ADR.

### 19.1 Decisions

| OQ | Selected | Decision (as recorded) | Rationale | Governance consequence | Implementation consequence (future, not authorized) | Out of scope |
|---|---|---|---|---|---|---|
| **OQ-R-1** Vehicle | **Option B** | A new, bounded **WP-23 TD-171 remediation tranche** under WP-23.<br>– Workstreams A–C remain accepted and historically intact; the remediation is **not** a silent extension of the accepted A–C closure.<br>– BAR/WP-23 remains the owner.<br>– **No** new independent Work Package is created.<br>– The tranche has its own implementation boundary, verification gate and closure record | It preserves the RD-23-02/C-3 acceptance record and D2 single ownership (§8.1, §9) | **A WP-23 Charter amendment and explicit remediation-tranche authorization are required before implementation** | The tranche follows its own `§19` checklist and `§19.7b` gates (Charter §16) | Amending the Charter now; reopening A–C; a new WP |
| **OQ-R-2** Mechanism | **Option D** | A governed deployment-time registration operation, combined with repository/CI verification and `BAR-INDEX.md` reconciliation. **Intended control model:**<br>1. A Repository-Owner-authorized governing act establishes the registration.<br>2. The governed operation validates the act and the registration information before creating the persistent BAR row.<br>3. The governed operation is the **only permitted production path** for persistent BAR registration.<br>4. CI verifies governing-act references and `BAR-INDEX.md` consistency verifiable from repository material.<br>5. Environment-level reconciliation verifies persistent rows against the canonical governance/index state.<br>6. Existing `record_audit`/`publish_event` remain part of the evidence trail | It matches Charter §7/§14 and RD-23-03 without a new authority role or act registry (§8.2, §10) | — | The exact mechanism is **not yet designed or implemented**. It belongs to the tranche's implementation design | Any claim that the mechanism exists |
| **OQ-R-3** `register()` control | **Governed operation + database-role separation** | The existing low-level `register()` must **not** remain an unrestricted, application-callable production write path. The future design must establish:<br>– a dedicated governed registration write operation;<br>– **database-role separation**, so the BAE/M2 read path cannot perform BAR registration writes;<br>– the governed write path as the only production component granted registration-write capability;<br>– **negative testing** proving an unauthorized caller cannot create a persistent BAR registration | It closes "any in-process caller" (GAP-23-03-1) without a runtime authority identity (§10) | **No** new runtime authority identity. **No** `require_platform_admin` as the primary governance control. **No** new constitutional authority seat | Role names, grants and deployment configuration are implementation-design work. **Database-role provisioning is not established** | Provisioning now; any new authority identity |
| **OQ-R-4** Act form | **Repository governance record: ADR/ROD-style act** | The governing act is a durable repository governance record that explicitly identifies:<br>– the BAR Business Activity Identifier;<br>– the Business Activity reference;<br>– the owning capability and/or Work Package, as applicable;<br>– the governing decision or authorization;<br>– the registration intent;<br>– the applicable repository governance authority.<br>The existing ADR/ROD-style pattern may be used | It mirrors CBOR-ADR (Charter §7) with no new architecture layer (§7) | **No** new canonical act registry. **No** database-backed governance-act architecture. An arbitrary free-text `registering_act` string is **not** sufficient | The implementation must define the exact machine-verifiable citation and validation rule | Designing that rule now |
| **OQ-R-5** Canonical issuance environment | **A single designated canonical production environment** | BAR identifier issuance is canonical only in the designated production BAR/AuthService database.<br>– BAR identifiers are enterprise-global canonical identifiers, not allocated independently per environment.<br>– Other environments must not issue competing persistent BAR identifiers.<br>– Non-production and test environments may use isolated test identifiers and data, which never become canonical registrations.<br>– `BAR-INDEX.md` represents the canonical enterprise registration state, not any development or test database | It resolves §6.3 with D5 unchanged | **The repository does not currently define a production environment** (no deployment configuration or pipeline, §6.2). Designating it is an **implementation/deployment prerequisite** | The design must name the designated environment and prevent accidental multi-environment canonical issuance | Naming or configuring an environment now |
| **OQ-R-6** Reconciliation access | **The deployment/infrastructure owner provides controlled read access** | The infrastructure/deployment owner provides the controlled database access needed to reconcile persistent BAR rows against the canonical `BAR-INDEX.md`/governance state.<br>– The reconciliation consumer receives **read-only**, environment-scoped, controlled access.<br>– **BAE M2 is not the reconciliation owner** and obtains no BAR write access.<br>– CI may verify repository/index consistency without database access.<br>– Row ↔ index reconciliation requires controlled access to the designated environment's database | It is consistent with RD-M2-08's external-prerequisite treatment (§6.2) | FQ-6-style infrastructure provisioning remains an **external prerequisite** where applicable | Access is provided by infrastructure. **No such access currently exists** | Claiming access exists |
| **OQ-R-7** Ungoverned rows | **Quarantine/block; neither accept nor delete automatically** | A persistent row that cannot be shown to have the required governing act and canonical index correspondence is an **ungoverned registration**. It is not valid execution eligibility. It must not be silently adopted into `BAR-INDEX.md`, deleted or rewritten. It is quarantined/blocked pending explicit governance disposition, with the finding and evidence recorded. Any backfill, recreation, correction or deletion needs a **separately authorized** remediation decision | It preserves data and avoids destructive action without authorization (§11) | — | — | **This does not imply such rows exist.** No local persistent BAR rows were found. Deployed environments are unverifiable (§11) |

### 19.2 Responsibility boundary

| Area | Responsibility |
|---|---|
| **BAR / WP-23 remediation tranche** | Governs the registration write path. Validates governing acts. Establishes BAR registration integrity. Owns `BAR-INDEX.md` reconciliation. Owns TD-171 closure |
| **Infrastructure / deployment** | Provides the required controlled database access. Provisions database roles and access as required |
| **BAE M2** | Remains read-only. Reads canonical BAR registration. Never writes or registers BAR. Never repairs or reconciles BAR. Never validates governing acts as a substitute for BAR governance. **Remains blocked until TD-171 closes** |
| **M2-P** | Only its previously decided binding-infrastructure scope (RD-M2-07) |

### 19.3 Implementation authorization, G5-08 and `TECH-DEBT.md`

- **These decisions do not authorize remediation implementation.** A WP-23 Charter amendment and remediation-tranche authorization remain required.
- **Remaining prerequisites before implementation and closure:**
  - the Charter amendment and tranche authorization;
  - the tranche's `§19` checklist and implementation design, including the act-validation rule, the operation, role design and the reconciliation check;
  - designation of the canonical production environment;
  - infrastructure-provided database roles and controlled read access;
  - TD-176 PostgreSQL verification ("before the first real registering act");
  - the §12 closure criteria verified through `§19.7b`.
- **G5-08:** the obligation to reassess TD-171's severity against the `§19.8.7` High criterion when the execution-eligibility consumer trigger occurs is **preserved**. It is not performed here, and TD-171's severity is unchanged.
- **`TECH-DEBT.md`:** not modified. A future authorized synchronization must update TD-171 with the selected vehicle and mechanism, the decision status and the G5-08 reassessment obligation.

### 19.4 Traceability

| Source | Link |
|---|---|
| RD-23-03 (`ROD-WP-23-AC …` §0) | The Layer 1–4 model that OQ-R-2 and OQ-R-4 implement. GAP-23-03-1/2 |
| Gate 1 **CERT-F-04** | The defect and its closure condition (OQ-R-3) |
| Gate 5 **G5-01**, **G5-08**, **C-1** | TD registration; severity reassessment (§19.3) |
| WP-23 A–C acceptance (`IRA-WP-23-AC …`; RD-23-02) | Preserved intact (OQ-R-1) |
| TD-171 decision ROD (`ROD-BAE-001-TD-171 …` §17) | Owner BAR/WP-23; closure before M2; no BAE compensation (§19.2) |
| `ADR-042` (`RO-M1-03`) | BAR authority unchanged; the BAE consumes |
| `ADR-043` | B2 binding unaffected (§8.2 R3 excluded) |
| FO-2 (`IRA-BAE-001-M2 §16.B`, §16.E) | M2 read-only contract (§19.2) |
| FO-3 (FQ-1 (c), FQ-2 (a), FQ-7) | A precedent used as input for OQ-R-2, R-3 and R-4. Not adopted as TD-171's implementation (OQ-171-2) |
| RD-M2-05 (`ROD-BAE-001-RD-M2-05 …` §21) | M2 host: read-only BAR access only |
| RD-M2-07 | M2-P scope unchanged (§19.2) |
| RD-M2-08 | The external-infrastructure-prerequisite precedent (OQ-R-6) |

None of these sources was changed.

### 19.5 State after this decision

| Item | State |
|---|---|
| **TD-171** | **OPEN: remediation required** |
| WP-23 remediation tranche | Decided in principle. Charter amendment and authorization **outstanding** |
| M2 | **NOT AUTHORIZED / NOT STARTED** |
| M2-P | CHARTERED / NOT AUTHORIZED / NOT STARTED |

### 19.6 Compact decision table

| OQ | Decision |
|---|---|
| OQ-R-1 | **B:** new bounded WP-23 remediation tranche. A–C intact; no new WP; Charter amendment required |
| OQ-R-2 | **D:** governed deployment-time operation plus CI verification plus environment reconciliation. Mechanism not yet designed |
| OQ-R-3 | Governed operation plus database-role separation. `register()` is not an unrestricted production path. No new authority identity; not `require_platform_admin`. Provisioning not established |
| OQ-R-4 | Repository ADR/ROD-style act naming identifier, reference, capability/WP, decision, intent and authority. No act registry. Free text is insufficient |
| OQ-R-5 | A single designated canonical production environment issues identifiers. The environment is not yet defined (a prerequisite) |
| OQ-R-6 | Infrastructure provides controlled, read-only, environment-scoped access. M2 is not the owner. Not yet existing |
| OQ-R-7 | Ungoverned rows are quarantined/blocked. No silent adopt, delete or rewrite. A separate authorization is needed for any fix |

*~~End of decision preparation. No implementation. Nothing staged, committed or pushed.~~ End of decision record. DECIDED 2026-09-30 (vehicle B, mechanism D). TD-171 OPEN. No implementation authorized. M2 NOT AUTHORIZED / NOT STARTED.*
