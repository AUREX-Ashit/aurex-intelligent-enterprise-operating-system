# IRA-WP-23-AC — Enterprise BAR Workstreams A–C: Closure Readiness Assessment

**Work Package:** `WP-23` (Enterprise Business Activity Registry Mechanism), Workstreams **A** (BAR index), **B** (identifier issuance), **C** (registration mechanism) only
**Prepared:** 2026-09-25, per Repository Owner decision **RD-M2-01** (`IRA-BAE-001-M2 §0`): WP-23 A–C must be closed/committed and independently verified before WP-BAE-001 M2 begins, and stale "delivered/certified" statements must be reconciled. **WP-23 remains its own Work Package and governance boundary; WP-BAE-001 M2 does not absorb it.**
**Status:** ~~**READINESS ASSESSMENT — A–C NOT CLOSABLE YET.** Three Repository Owner decisions (§6) and the engineering prerequisites in §5 remain.~~ *(Updated 2026-09-25 — Repository Owner decision pass, §0.)* **READINESS ASSESSMENT — A–C NOT CLOSABLE YET.**
- RD-23-01 and RD-23-02 are decided; ~~**RD-23-03 remains OPEN**~~ **RD-23-03 decided 2026-09-25, Option D (layered)** (`ROD-WP-23-AC-BAR-Registry-Authority-Decision-Preparation.md §0`).
- `IMP-REPORT-WP-23` (A–C tranche) now exists, and the `BAR-INDEX.md` status lines are corrected.
- ~~The commit is blocked by missing prerequisite commits (§0, RD-23-01). Gate 1 cannot be dispatched until the conditions in §10 are met.~~ *(Synchronized 2026-09-28, Gate 5 condition C-2, `RRA-WP-23-AC` ST-1.)* The prerequisite commits now exist: WP-20 `355ebbe`, then WP-21 `203bed1` (C2's parent is C1; committed Alembic head `f6a7b8c9d0e1`). CERT-F-02 is resolved. Gate 1 was dispatched and ran (`CERT-WP-23-AC`).
- ~~**WP-23 remains OPEN. A–C are IMPLEMENTED — not independently verified, not accepted, not certified.**~~ *(Updated 2026-09-25.)* Gates 1 and 2 have run: **Gate 1 STOP; Gate 2 FAIL.**
  - RD-23-04 resolves Gate 1's governance blocker, CERT-F-01, by ratification and a Charter/design correction (§0, §0.1).
  - ~~**VV-F-01 (High) remains OPEN.** Remediation (Gate 3) and its independent verification (Gate 4) are outstanding and not started.~~ *(Synchronized 2026-09-28, Gate 5 condition C-2, ST-2.)* VV-F-01 (High), VV-F-02 and CERT-F-03 were remediated at Gate 3 (2026-09-26) and **independently verified at Gate 4: PASS** (`VV-AUDIT-WP-23-AC_…_Gate-4`).
  - *(Added 2026-09-28.)* **Gate 5: PASS WITH CONDITIONS** (`RRA-WP-23-AC_BAR_Workstreams_A-C_Release_Readiness_Audit.md`). ~~Conditions C-1 (Technical Debt registration: TD-171 to TD-176 and the TD-096 extension) and C-2 (this status synchronization) are now being remediated. C-3 (Repository Owner acceptance record) and C-4 (post-commit reconciliation) are not performed.~~ *(C-3 addendum, 2026-09-28.)* C-1 (TD-171 to TD-176; TD-096 extension) and C-2 (ST-1 to ST-13) are **completed**. **C-3 is satisfied** by the Repository Owner Acceptance Record (§0.2). C-4 (post-commit reconciliation of S-1 to S-12 and CERT-F-11) is **outstanding**.
  - ~~**WP-23 remains OPEN. A–C are IMPLEMENTED — NOT ACCEPTED, not certified, not committed.**~~ *(C-3 addendum, 2026-09-28.)* **WP-23 Workstreams A–C: ACCEPTED** (§0.2; RD-23-02 terminal state; **not certified, not closed**). Committed together with the §0.2 record. **WP-23 as a whole remains OPEN; Workstreams D–H are not implemented.** WP-BAE-001 M2 remains NOT AUTHORIZED and NOT STARTED.

---

## 0. Repository Owner Decision Record — WP-23 A–C Closure Decisions

**Recorded:** 2026-09-25, by direct Repository Owner instruction, responding to §6 of this document. Each decision is recorded as stated and is not reinterpreted. WP-BAE-001 M2 remains **NOT AUTHORIZED and NOT STARTED**.

| ID | Repository Owner decision (as recorded) | Status after this revision |
|---|---|---|
| **RD-23-01** Commit order | **SELECTED.** WP-23 A–C must not be committed in a way that leaves its migrations dependent on uncommitted parent migrations from C-021/C-022. First establish that the required C-021 and C-022 migration ancestry is committed and available; then WP-23 A–C may be committed against those committed ancestors. **Do not** amend C-021/C-022 commits, absorb C-021/C-022 implementation into WP-23, create a combined cross-capability commit, or alter unrelated working-tree changes. If the repository state prevents a clean WP-23 A–C commit, STOP and report exactly what prerequisite commit/order is missing. | **RESOLVED** (decision). ~~**Prerequisite NOT MET: STOP condition reached for the commit.**~~ *(Synchronized 2026-09-28, ST-3.)* **Prerequisite MET:** WP-20 committed as `355ebbe` and WP-21 as `203bed1`, each under explicit RO authorization; committed head `f6a7b8c9d0e1`, onto which the WP-23 migrations chain (verified at Gate 5). See "RD-23-01 — missing prerequisites" below, which is now historical |
| **RD-23-02** Closure unit | **SELECTED.** WP-23 A–C may be treated as a **separately closable implementation tranche** within WP-23. A–C can become IMPLEMENTED / INDEPENDENTLY VERIFIED / ACCEPTED; **WP-23 as a whole remains OPEN**; Workstreams D and E remain incomplete; WP-23 must **not** be labelled fully COMPLETE/CLOSED. The WP-23 Charter is not rewritten; this is a narrow closure-unit decision for A–C. | **RESOLVED.** Recorded here, and as a dated note under WP-23 Charter §22 that does not alter any other Charter text. The tranche's terminal state is **ACCEPTED**, not CERTIFIED or CLOSED: WP-level Certification, V&V and RRA remain at WP-23 completion (Charter §22) |
| **RD-23-03** Registry authority | **KEEP OPEN.** None of `BAR-INDEX.md`, the registering act or the `bar_registration` table is selected as authoritative. A focused decision-preparation artifact is required, distinguishing **governance registration** from **runtime execution registration**. No ADR yet. | ~~**OPEN — RO decision required.**~~ **DECIDED 2026-09-25 — Option D, Layered Authority Model.** Recorded in `ROD-WP-23-AC-BAR-Registry-Authority-Decision-Preparation.md §0`: registering act = governance authority; `bar_registration` = runtime execution registration (a row is not proof of authorization); `BAR-INDEX.md` = governance catalogue, not a runtime source; reconciliation must stay traceable, mechanism not decided. No ADR (examined in §0.3 there: not required by an existing rule). Implementer-identified gaps GAP-23-03-1 to 3 are recorded there for independent review, not fixed |

| **RD-23-04** Gate 1 CERT-F-01, Charter §21 Workstream C/D contradiction *(recorded 2026-09-25)* | **ACCEPTED** Gate 1's finding that Charter §21 contradicts itself. Row C says "governance-only, no runtime" and row D says "first runtime component", yet §20 authorizes work "as specified in" the design, and the design delegated the runtime-store question to Workstreams C/D. RD-23-03 established the authority model but did not amend the Charter or ratify the construction. **RATIFIED** the runtime construction already implemented under Workstreams B and C as within the authorized WP-23 design boundary. This ratifies the construction already performed. It is **not** an expansion of WP-23 scope, and not an authorization of Workstream D, Workstream E, M2, BA registration, runtime execution gating or new runtime behaviour. **AUTHORIZED** a dated correction note on WP-23 Charter §21 rows C and D, and on the matching rows C and D of `ENTERPRISE-BAR-…-READINESS.md §19` | **RESOLVED.** The correction notes are applied, with the historical text struck through: Charter §21 rows C and D plus a note below the table; design §19 rows C and D plus a note below the table. No ADR: no existing rule requires one for this ratification or correction (§0.1 below). CERT-F-01 is resolved by RO act; the other Gate 1 findings are unaffected |

**The original §6 recommendations are superseded where they differ.** RD-23-01's decision matches recommendation (a). RD-23-02 matches recommendation (a), and adds the explicit "WP-23 stays OPEN; A–C terminal state is ACCEPTED" wording.

### 0.1 RD-23-04 — ADR examination and current gate status (2026-09-25)

**ADR: not required by an existing rule.**
- `CLAUDE.md §19` (line 431) requires an ADR only when architecture "evolve[s] during implementation".
- RD-23-04 does not evolve architecture. D1–D9 are unchanged. It ratifies construction inside the design's own delegated boundary (design §6/§18) and corrects contradictory Charter/design text.
- No rule in `CLAUDE.md`, the WP-23 Charter or the design requires an ADR for a Charter correction note. Dated correction notes on Charters are established repository practice, for example the WP-BAE-001 Charter §11 correction under `RO-M1-12`.

**Gate status after RD-23-04:**

| Gate | Artifact | Verdict | Remaining |
|---|---|---|---|
| Gate 1 | `CERT-WP-23-AC_BAR_Workstreams_A-C.md` | **STOP** (recorded result, not re-run) | CERT-F-01 is now resolved by RO act (RD-23-04). **Still OPEN:**<br>– CERT-F-02: RD-23-01 prerequisite commits missing;<br>– CERT-F-03: runtime docstrings contradict RD-23-03; remediation needed;<br>– CERT-F-04 to F-14 (Medium/Low).<br>Gate 1 is not re-certified by this record |
| Gate 2 | `VV-AUDIT-WP-23-AC_BAR_Workstreams_A-C.md` | **FAIL** (recorded result) | *(2026-09-26: VV-F-01 and VV-F-02 remediated under Gate 3; ~~**pending Gate 4 independent verification** and therefore not yet closed.~~ )* *(Synchronized 2026-09-28, ST-4: **independently verified at Gate 4, PASS**. VV-F-07 is closed by later evidence (Gate 4 G4-O-04; Gate 5 probe G5-P1). VV-F-03 is TD-096; VV-F-04 is TD-173; VV-F-05 is TD-174; VV-F-06 is TD-175; O-01 is an RO observation.)* ~~**VV-F-01 (High): OPEN.**~~ A collision or race rollback discards the caller's session work. It cannot be deferred as debt (`§19.8.5`). VV-F-02 to F-07 and O-01 are also open |
| Gate 3 (remediation) | `IMP-REPORT-WP-23 §"Gate 3 Remediation"` | ~~**Not started**~~ **APPLIED 2026-09-26** (RO-authorized) | VV-F-01, VV-F-02 and CERT-F-03 remediated. Implementer evidence: 10 new tests; negative control 7 failed pre-fix; Gate 2 probe reproduces the defect pre-fix and not post-fix; BAR 32 passed; AuthService 982 passed. **Implementer evidence only; not verification** |
| Gate 4 (independent verification of remediation) | ~~—~~ `VV-AUDIT-WP-23-AC_BAR_Workstreams_A-C_Gate-4.md` | ~~**REQUIRED — not started** (not launched without RO authorization)~~ *(Synchronized 2026-09-28, ST-4.)* **PASS** (2026-09-26), "subject only to any separately identified Gate 1 prerequisites or closure conditions" | ~~A fresh-context reviewer, uninvolved in Gates 1–3. Must include a from-scratch probe and a negative control against the pre-fix code. A byte-identical pre-fix snapshot (with SHA-256 sums) is in the session scratchpad `prefix_snapshot/`~~ A fresh-context reviewer ran from-scratch probes with a pre-fix negative control. It classified VV-F-01, VV-F-02 and CERT-F-03 as PASS, and PostgreSQL/asyncpg behaviour as UNVERIFIED (now TD-176) |
| Gate 5 (release readiness) *(row added 2026-09-28)* | `RRA-WP-23-AC_BAR_Workstreams_A-C_Release_Readiness_Audit.md` | **PASS WITH CONDITIONS** (2026-09-28) | ~~C-1 and C-2 are being remediated (RO-authorized 2026-09-28). C-3 (RO acceptance record) is not performed.~~ *(C-3 addendum, 2026-09-28:)* C-1 and C-2 completed; C-3 satisfied (§0.2). C-4 (S-1 to S-12 and CERT-F-11 reconciliation) follows the commit |

*(Note added 2026-09-28, ST-4 synchronization.)* The Gate 1 row above is kept as recorded. Since then, CERT-F-02 has been resolved by the WP-20 and WP-21 commits, and CERT-F-03 and CERT-F-07 have been remediated and verified at Gate 4. The Technical-Debt items Gate 1 required (CERT-F-04, -05, -08, -13, -14) are registered as TD-171 to TD-174. CERT-F-06 is TD-096. Gate 1's recorded verdict remains STOP and was not re-issued (Gate 5 condition C-3).

~~**WP-23 A–C is NOT ACCEPTED, NOT CERTIFIED, NOT COMMITTED and NOT CLOSED. WP-23 remains OPEN.**~~ *(C-3 addendum, 2026-09-28.)* **WP-23 A–C is ACCEPTED** (§0.2) and committed together with that record. It is **NOT CERTIFIED and NOT CLOSED** (RD-23-02). **WP-23 remains OPEN.**

### 0.2 C-3 — Repository Owner Acceptance Record, WP-23 Workstreams A–C (2026-09-28)

**Recorded:** 2026-09-28, by direct Repository Owner instruction ("Proceed with C-3 acceptance and then commit WP-23 A–C, under strict scope control"). The instruction specifies that the entire Gate 1 is **not** re-run.

**Decision: WP-23 Workstreams A–C (the RD-23-02 tranche) are ACCEPTED.**

**Terminology, per RD-23-02 (§0) and Charter §22:**
- The tranche's terminal state is **ACCEPTED**. It is **not** CERTIFIED and **not** CLOSED.
- WP-level Certification, V&V and Release Readiness remain at WP-23 completion.
- **WP-23 as a whole remains OPEN.**

**The historical record is preserved, not rewritten:**
- **Gate 1** (`CERT-WP-23-AC`) recorded **STOP**, and that verdict stays in the record as issued. It was not re-issued.
- **Gate 2** (`VV-AUDIT-WP-23-AC`) recorded **FAIL**, and that verdict also stands as recorded.
- **Gate 5** (`RRA-WP-23-AC_…_Release_Readiness_Audit`) recorded **PASS WITH CONDITIONS**, and that verdict is preserved.

**Acceptance basis.** Every blocking condition identified by Gates 1, 2 and 5 was later resolved by an authorized act and, where it was a defect, independently verified by a fresh-context reviewer:

| Blocking item | Resolution | Evidence |
|---|---|---|
| CERT-F-01 (High, governance: Charter §21 row C/D contradiction) | Repository Owner decision **RD-23-04**: ratification of the past B/C runtime construction and dated Charter §21 / design §19 corrections | §0 above; Charter §21 note; design §19 note. Gate 5 confirmed the scope, with no expansion |
| CERT-F-02 (High, commit order / migration ancestry) | Prerequisite commits **`355ebbe`** (WP-20 / C-021) and **`203bed1`** (WP-21 / C-022), committed head `f6a7b8c9d0e1` | Verified from git history at Gate 5 (`RRA-WP-23-AC §5.1`) |
| CERT-F-03 (Medium, runtime docstrings contradicting RD-23-03) | RO-authorized Gate 3 remediation | Gate 4 PASS (`VV-AUDIT-WP-23-AC_…_Gate-4`); re-read at Gate 5 |
| VV-F-01 (High, whole-session rollback) and CERT-F-07 (same defect) | Gate 3 remediation (a savepoint per attempt) | Gate 4 PASS, with a pre-fix negative control; re-probed at Gate 5 |
| VV-F-02 (Medium, integrity-error misclassification) | Gate 3 remediation | Gate 4 PASS |
| Gate 5 **C-1** (register the Technical Debt) | **Completed 2026-09-28:** TD-171 to TD-176 added and TD-096 extended (CERT-F-06 / VV-F-03, G4-O-01) in `TECH-DEBT.md` | `TECH-DEBT.md` |
| Gate 5 **C-2** (status synchronization ST-1 to ST-13) | **Completed 2026-09-28:** dated, strikethrough-preserving corrections in this document, `IMP-REPORT-WP-23`, `BAR-INDEX.md`, the `WPR-001` WP-23 row and note, `ROD-WP-23-AC` and design §19 rows B/C | Those documents, each tagged "ST-n" |
| Gate 5 **C-3** (the RO acceptance record states its basis) | **Satisfied by this record** | This §0.2 |

**Gate 5's own finding** (`RRA-WP-23-AC`): no open Critical, High or Medium defect, and no `CLAUDE.md §19.8.5` non-deferrable defect.

**Deferred items carried, not waived:**
- TD-096, TD-171 to TD-176, and the Low findings CERT-F-09 to F-13 and G5-03 to G5-06.
- **TD-171's hard condition** carries forward: act-to-row enforcement and reconciliation must be in place **before `bar_registration` is used to decide whether a Business Activity may execute**.
- **Gate 5 C-4** (post-commit reconciliation of S-1 to S-12 and CERT-F-11) remains outstanding. It is the subsequent governance task.

**This acceptance does NOT:**
- certify or close WP-23;
- authorize Workstreams D–H;
- authorize WP-BAE-001 M2, which remains NOT AUTHORIZED and NOT STARTED;
- register a Business Activity or assign a Business Activity Identifier;
- change RD-23-03 or RD-23-04.

**Commit:** WP-23 A–C are committed together with this record, as one commit, using the boundary proposed in `RRA-WP-23-AC §7`. Nothing is pushed.

### RD-23-01 — missing prerequisites (the STOP report the decision requires)

Verified directly on 2026-09-25 with `alembic heads`, `alembic history -r d4e5f6a7b8c9:` and `git ls-files`:

```
c3d4e5f6a7b8 -> d4e5f6a7b8c9   c132_notification            COMMITTED (last committed revision)
d4e5f6a7b8c9 -> e5f6a7b8c9d0   c021_offering_definition     UNTRACKED  (WP-20 / C-021)
e5f6a7b8c9d0 -> f6a7b8c9d0e1   c022_commercial_account      UNTRACKED  (WP-21 / C-022)
f6a7b8c9d0e1 -> a7b8c9d0e1f2   bar_identifier_ledger        UNTRACKED  (WP-23 B)
a7b8c9d0e1f2 -> b8c9d0e1f2a3   bar_registration (head)      UNTRACKED  (WP-23 C)
```

There is one Alembic head and no branch. A clean WP-23 A–C commit needs, **in this order, and each under its own Work Package's authority (none is WP-23 work)**:

1. **A WP-20 (C-021) implementation commit** that includes migration `e5f6a7b8c9d0` together with its C-021 model, repository, service, router, schema, tests and frontend. It must also include its own lines of `models/__init__.py` (the `C021OfferingDefinition` import and `__all__` entry) and its own hunks of the shared modified files (`main.py`, `admin-navigation.ts`, and the other files WP-20 touched). WP-20's closing commit `8323bf3` contained governance documents only. Whether this new commit is permitted after `8323bf3` recorded closure is a WP-20 governance question, not a WP-23 one.
2. **A WP-21 (C-022) implementation commit** that includes migration `f6a7b8c9d0e1` together with its C-022 code, and its own `models/__init__.py` lines (`C022CommercialAccount`). The WP-21 governance artifacts (Charter, IMP-REPORT, CERT, VV-AUDIT, RRA) and WP-21's `WPR-001` row are also untracked.
3. **Only then, the WP-23 A–C commit.**

**Two mechanical constraints for whoever performs those commits:**
- `models/__init__.py` carries all four new imports (C-021, C-022 and both BAR models) in one diff hunk. Each commit must stage only its own lines. `git add -p` is interactive and is not available in this environment, so staging needs a prepared partial patch applied with `git apply --cached`. `git add -A` / `git add .` remain prohibited.
- The WP-23 governance documents are **also** uncommitted: the Charter, `ENTERPRISE-BAR-…-READINESS.md`, `ROD-ENTERPRISE-BAR-…`, `BAR_ENTERPRISE_MECHANISM_DECISION_INVESTIGATION.md`, `BAR-INDEX.md` and WP-23's `WPR-001` row. They belong in the WP-23 A–C commit (or a WP-23 governance commit before it), not in the WP-20 or WP-21 commits.

**Nothing was committed or staged in this pass.** The WP-20 and WP-21 commits are outside this task's authority and outside WP-23.

**Scope rule applied.** This document changes nothing:
- no BAR code, migration, test, `BAR-INDEX.md`, WP-23 Charter, WPR-001 or BAE code;
- no Workstream D or E work, and no BAR-to-BAE adapter;
- no Business Activity registration and no identifier assignment.

Stale statements are listed (§7), not corrected. Nothing is staged, committed or pushed.

---

## 1. Sources Inspected (directly, 2026-09-25)

- **Governance:**
  - `WP-23_Enterprise_BAR_Mechanism_Implementation_Charter.md` (§1, §3, §16, §19–§22);
  - `ENTERPRISE-BAR-MECHANISM-DESIGN-AND-IMPLEMENTATION-READINESS.md` (§4, §6, §9, §10, §18);
  - `ROD-ENTERPRISE-BAR-Decision-Preparation.md` (D2, D5, D7);
  - `BAR-INDEX.md` in full;
  - `WPR-001` WP-23 row (working tree).
- **Code:**
  - `models/bar_identifier_ledger.py`, `models/bar_registration.py`;
  - `repositories/bar_identifier_repository.py`, `repositories/bar_registration_repository.py`;
  - `services/bar_identifier_service.py`, `services/bar_registration_service.py`;
  - `alembic/versions/2026_09_22_0900-a7b8c9d0e1f2_bar_identifier_ledger.py`, `alembic/versions/2026_09_22_1000-b8c9d0e1f2a3_bar_registration.py`;
  - `tests/test_bar_identifier_service.py` (9 tests), `tests/test_bar_registration_service.py` (13 tests);
  - `models/__init__.py` (working-tree diff); `tests/conftest.py`.
- **Evidence gathered:**
  - `git status`, `git ls-files`, `git log --all` for every file above;
  - the Alembic revision chain;
  - a test run of both BAR test files (below).

## 2. Current State

| Item | State |
|---|---|
| Workstream A: `BAR-INDEX.md` | Exists; **untracked**; zero registrations. Its own closing line: "**IMPLEMENTED — READY FOR INDEPENDENT VERIFICATION**" |
| Workstream B: `bar_identifier_ledger` model, repository, service, migration `a7b8c9d0e1f2`, 9 tests | Implemented; **untracked** |
| Workstream C: `bar_registration` model, repository, service, migration `b8c9d0e1f2a3`, 13 tests | Implemented; **untracked** |
| `models/__init__.py` registration of `BarIdentifierLedger`, `BarRegistration` | **Uncommitted modification**, ~~in the same diff hunk as WP-20's `C021OfferingDefinition` and WP-21's `C022CommercialAccount`~~ *(ST-5, 2026-09-28: the C-021 and C-022 lines are now committed in `355ebbe`/`203bed1`; the remaining diff is BAR-only)* |
| Test evidence (2026-09-25, this assessment) | `pytest tests/test_bar_identifier_service.py tests/test_bar_registration_service.py`: **22 passed**. Implementer-authored tests only; not independent evidence. *(ST-5, 2026-09-28: independently re-measured at Gate 5: BAR 32 passed, including the 10 Gate 3 tests; AuthService full suite 982 passed)* |
| `IMP-REPORT` for WP-23 | ~~**Does not exist**~~ *(ST-5, 2026-09-28)* Exists: `IMP-REPORT-WP-23_Enterprise_BAR_Mechanism.md` (A–C tranche, including the Gate 3 remediation) |
| Gate 1–5 artifacts (CERT, VV-AUDIT, RRA) for WP-23 | ~~**None exist**~~ *(ST-5, 2026-09-28)* All exist for the A–C tranche: `CERT-WP-23-AC` (Gate 1, STOP), `VV-AUDIT-WP-23-AC` (Gate 2, FAIL), `VV-AUDIT-WP-23-AC_…_Gate-4` (Gate 4, PASS), `RRA-WP-23-AC_…_Release_Readiness_Audit` (Gate 5, PASS WITH CONDITIONS). The Gate 3 remediation is recorded in the IMP-REPORT |
| WPR-001 WP-23 row | Uncommitted; reads "**CHARTERED — IMPLEMENTATION NOT YET COMPLETED**" *(ST-5/ST-11, 2026-09-28: the row is synchronized with the A–C tranche state)* |
| WP-23 Charter, design, ROD, BAR investigation | **Untracked** |

**Summary.** ~~A–C are **IMPLEMENTED**, **not committed**, **not independently verified**, **not accepted or certified**.~~ *(ST-5, 2026-09-28)* A–C are **IMPLEMENTED** and **independently verified** (Gates 1, 2 and 4, with Gate 5 PASS WITH CONDITIONS), but ~~**not accepted, not certified and not committed**~~ *(C-3 addendum, 2026-09-28: **ACCEPTED** (§0.2) and committed with that record; **not certified, not closed**; WP-23 OPEN)*. Any committed document that says otherwise is stale (§7).

## 3. Findings

**F-1 — Commit-order dependency on other uncommitted Work Packages (blocking).**
- The BAR migrations cannot be committed on their own. The Alembic chain from the last committed head is:
  `d4e5f6a7b8c9` (C-132, **committed**) → `e5f6a7b8c9d0` (C-021 offering definition, WP-20, **untracked**) → `f6a7b8c9d0e1` (C-022 commercial account, WP-21, **untracked**) → `a7b8c9d0e1f2` (BAR ledger) → `b8c9d0e1f2a3` (BAR registration).
- WP-20's closing commit `8323bf3` contained **governance documents only**. The C-021 model, migration, repository, service, router, schema, frontend and tests remain untracked.
- WP-21 is recorded as "CERTIFIED — CLOSED — RELEASE-READY" (`RRA-WP-21`), but its code is also untracked.
- Consequences of committing BAR alone:
  - it would commit a migration whose parent revision does not exist in the repository, so `alembic upgrade` would fail on a clean checkout;
  - `models/__init__.py` would need to be staged hunk-selectively.
- Re-parenting the BAR migrations onto `d4e5f6a7b8c9` would change BAR runtime code and diverge from the chain WP-21's gates verified. It is **not** proposed.

**F-2 — No closure unit exists for A–C alone (decision).**
- WP-23 Charter §22 defines completion only for the whole Work Package: Workstreams A–G certified, V&V-audited and release-readiness-audited, plus the 14-row cutover.
- §20 says every workstream is subject to the five-gate sequence "before release".
- No provision exists for accepting A–C as a unit before D–G. RD-M2-01 requires exactly that, so a Repository Owner disposition is needed. The precedent is WP-BAE-001's milestone-level acceptance of M1, which stayed separate from WP-level closure.

**F-3 — Unresolved authority between `BAR-INDEX.md`, the registering act, and the `bar_registration` table (decision; blocks verification).**
- **Design §6:** the Markdown index is "the authoritative governance record (mirroring CBOR)". The registering act is authoritative and the index is a pointer to it. Whether a database-backed registry is also needed is "**not decided here**".
- **`BAR-INDEX.md §1`:** "`BAR-INDEX.md` … is authoritative for Business Activity BAR registration". It also says the registering act "remains the authoritative registration record; this index is a pointer to it".
- **`bar_registration.py` docstring:** "this table, not `WPR-001` and not `CBOR-INDEX.md`, is the authoritative persisted record of Business Activity registration".
- **`BarRegistrationService`:** deliberately does **not** write `BAR-INDEX.md`, so the two can diverge by design.
- **WP-23 Charter §21, Workstream C:** described as "Registering-act convention … **Low risk — governance-only, no runtime**". The implementation built a runtime table, service, migration and identifier allocation. Whether that is within the Charter §20 authorization ("as specified in the design") is unsettled, given that the design left the runtime store undecided.
- This bears directly on WP-BAE-001 M2: which record does the BAE consult?

**F-4 — Stale status inside `BAR-INDEX.md` (engineering, documentation).**
- The closing line (file modified 2026-09-22 13:30) says Workstreams B and C "remain not implemented".
- B and C code was written 15:24–16:19 on the same day.

**F-5 — No Implementation Report (engineering).** `CLAUDE.md §19.7` requires `IMP-REPORT-WP-23` recording A–C scope, evidence and status. None exists.

**F-6 — Test harness does not enforce foreign keys (verification prerequisite).**
- `tests/conftest.py` builds an in-memory SQLite engine without `PRAGMA foreign_keys=ON`. Only `test_access_evaluation_service.py:240` enables it locally.
- `bar_registration.identifier`'s FK to `bar_identifier_ledger` is presented as the structural guarantee: "enforced by this table's own FK, not merely by application discipline". Neither BAR test file exercises it under enforcement.
- This is the `CLAUDE.md §19.7b` harness/production-parity item, named as the root cause of WP-05's undetected defects.

**F-7 — Independent verification not performed (engineering, gated).** No fresh-context Gate 1 or Gate 2 exists for A–C.

## 4. Path to IMPLEMENTED → INDEPENDENTLY VERIFIED → ACCEPTED

```
RO decisions RD-23-01..03 (§6)
  → [if RD-23-01(a)] WP-20 code and WP-21 code committed under their own closure acts (not WP-23 work)
  → WP-23 A–C documentation completion: IMP-REPORT-WP-23 (A–C); BAR-INDEX.md status line; any F-3 disposition text
  → Independent verification of A–C (fresh-context, §19.7 / §19.7b method):
       Gate 1 Certification; Gate 2 V&V with from-scratch probes, including FK enforcement (F-6),
       identifier format/uniqueness/collision, concurrent registration (unique-constraint backstop),
       atomic ledger+registration rollback, migration upgrade/downgrade on a clean chain, single Alembic head
  → Remediation + independent verification of remediation, if needed
  → RO acceptance of A–C (per RD-23-02)
  → One WP-23 A–C commit (explicit file list; models/__init__.py hunk-selective if still shared)
  → Stale-statement reconciliation (§7), as a separately authorized narrow pass
  → WP-BAE-001 M2 prerequisite (RD-M2-01) satisfied
```

## 5. Prerequisites Remaining to Close WP-23 A–C

| # | Prerequisite | Type | Blocked by |
|---|---|---|---|
| P-1 | Decide the commit-order dependency (F-1) | RO decision RD-23-01 | — |
| P-2 | Commit WP-20 (C-021) and WP-21 (C-022) code, if RD-23-01(a) | Their own closure/commit acts; **not WP-23 work** | P-1 |
| P-3 | Decide the A–C closure unit (F-2) | RO decision RD-23-02 | — |
| P-4 | Decide index/table/registering-act authority and the runtime table's authorization status (F-3) | RO decision RD-23-03 | — |
| P-5 | Write `IMP-REPORT-WP-23` covering A–C (F-5) | Engineering, documentation | P-3, P-4 |
| P-6 | Correct `BAR-INDEX.md`'s closing status line, strikethrough-preserve (F-4); apply any P-4 disposition text | Engineering, documentation | P-4 |
| P-7 | Fresh-context Gate 1 + Gate 2 for A–C, with FK-enforced probes (F-6, F-7) | Independent review | P-5, P-6 |
| P-8 | Remediation and its independent verification, if P-7 finds anything | Engineering + independent review | P-7 |
| P-9 | RO acceptance of A–C | RO act | P-7/P-8 |
| P-10 | WP-23 A–C commit (explicit paths; no `git add -A`) and `WPR-001` WP-23 row synchronization (WP-23 hunks only) | Engineering | P-2, P-9 |
| P-11 | Stale-statement reconciliation (§7) | RO-authorized narrow pass | P-9 (the correct current state is known only then) |

### 5.1 Prerequisite status after the 2026-09-25 decision pass

| # | Status | Evidence / remaining action |
|---|---|---|
| P-1 | **DONE** (decision) | RD-23-01 selected (§0) |
| P-2 | ~~**NOT MET — blocks P-10**~~ **MET** *(ST-6, 2026-09-28)* | ~~The WP-20 and WP-21 implementation commits do not exist (§0, "missing prerequisites"). They are outside WP-23's authority~~ WP-20 committed as `355ebbe` and WP-21 as `203bed1`, each under its own RO authorization, not as WP-23 work |
| P-3 | **DONE** (decision) | RD-23-02 selected (§0); dated note added under WP-23 Charter §22 |
| P-4 | ~~**OPEN**~~ **DONE** (decision, 2026-09-25) | RD-23-03 decided: Option D (`ROD-WP-23-AC …` §0). `BAR-INDEX.md` authority wording updated (§1, §2, §3, §4). Runtime-code docstrings not changed (GAP-23-03-3) |
| P-5 | **DONE, provisionally** | `architecture/05-Implementation/IMP-REPORT-WP-23_Enterprise_BAR_Mechanism.md` (A–C tranche; "IMPLEMENTATION COMPLETE — AWAITING INDEPENDENT VERIFICATION"). Written with P-4 still open, so it records the authority question as open instead of resolving it. It may need a dated update once RD-23-03 is decided |
| P-6 | **DONE** (status lines); P-4 disposition text pending | `BAR-INDEX.md` §3, §5 and the closing status line corrected, with strikethrough preserving the old text. §1's authority wording is deliberately **untouched** until RD-23-03 is decided |
| P-7 | ~~**NOT STARTED — not dispatchable yet**~~ **DONE** *(ST-6, 2026-09-28)* | ~~See §10. Scope and checklist prepared in §9~~ Gate 1 (`CERT-WP-23-AC`, STOP) and Gate 2 (`VV-AUDIT-WP-23-AC`, FAIL) ran with FK-enforced probes |
| P-8 – P-11 | ~~Not started~~ *(ST-6, 2026-09-28)* See the rows below | ~~Depend on P-7~~ |
| P-8 | **DONE** *(added 2026-09-28)* | Gate 3 remediation (IMP-REPORT) and Gate 4 independent verification: PASS. Gate 5: PASS WITH CONDITIONS; ~~C-1 and C-2 are being remediated~~ *(C-3 addendum: C-1 and C-2 completed)* |
| P-9 | ~~**NOT DONE**~~ **DONE** *(C-3 addendum, 2026-09-28)* | RO acceptance of A–C: Gate 5 condition C-3, ~~not performed~~ **satisfied by the Acceptance Record, §0.2** |
| P-10 | ~~**NOT DONE**~~ **DONE with this record** *(C-3 addendum, 2026-09-28)* | WP-23 A–C commit. P-2 is met; the boundary follows `RRA-WP-23-AC §7`. ~~It awaits P-9~~ One commit, made together with §0.2; not pushed |
| P-11 | **NOT DONE** *(added 2026-09-28)* | Stale-statement reconciliation of S-1 to S-12 and CERT-F-11: Gate 5 condition C-4, after the commit |

## 6. Repository Owner Decisions Required for WP-23 A–C

| ID | Decision | Options | Recommendation |
|---|---|---|---|
| **RD-23-01** | Commit-order dependency (F-1) | (a) Commit WP-20 and WP-21 code first under their own already-recorded closures, then WP-23 A–C. (b) Commit WP-20, WP-21 and WP-23 A–C together. (c) Re-parent the BAR migrations | **(a).** It keeps each Work Package's commit boundary. (b) merges boundaries. (c) changes verified runtime code |
| **RD-23-02** | Closure unit (F-2) | (a) A workstream-level acceptance of A–C via an RO disposition note, like WP-BAE-001 M1, while WP-level five-gate closure stays at WP-23 completion. (b) Amend the WP-23 Charter to define an A–C release | **(a).** No Charter amendment; mirrors existing precedent |
| **RD-23-03** | Registry authority (F-3) | (a) Ratify the `bar_registration` table as BAR's **runtime** store, subordinate to the registering act; `BAR-INDEX.md` stays the governance pointer; the table docstring and the index are reconciled; synchronization is defined. (b) Treat the table as exceeding the Charter and remove or defer it. (c) Make the table authoritative and demote `BAR-INDEX.md` | **Not recommended here.** It turns on the design's own "not decided" point and interacts with RD-M2-02 (`ROD-BAE-001-M2-…`, §6). Presented for decision only |

*(Updated 2026-09-25.)* The Repository Owner's decisions are recorded in §0. The table above is preserved as the analysis presented for decision. RD-23-03 was kept OPEN and is analysed in full in `ROD-WP-23-AC-BAR-Registry-Authority-Decision-Preparation.md`, which supersedes the three-option sketch above.

## 7. Stale Governance Statements (committed documents) — Inventory Only, Not Corrected

"Authoritative current state" for every row: WP-23 A–C are **implemented but uncommitted (untracked), with no IMP-REPORT and no independent verification or certification** (§2).

| # | Document (committed) | Exact stale statement | Proposed correction (strikethrough-preserve, dated) |
|---|---|---|---|
| S-1 | `architecture/05-Implementation/IRA-BAE-001_Business_Activity_Engine_Implementation_Readiness_Assessment.md:69` | "Delivered, certified, and directly reusable as-is" | "Implemented (uncommitted, not yet independently verified or certified, per `IRA-WP-23-AC` §2); reusable once WP-23 A–C closure completes (RD-M2-01)" |
| S-2 | `architecture/00-Governance/WPR-001_Work_Package_Roadmap.md:123` (WP-BAE-001 row, Dependencies cell) | "Enterprise BAR (`WP-23` Workstreams A–C, delivered and certified — …)" | "…Workstreams A–C, implemented, pending closure and independent verification (RD-M2-01) — …" |
| S-3 | `architecture/05-Implementation/WP-BAE-001_Business_Activity_Engine_Charter.md:170` (§10 M2 Dependencies) | "BAR (`WP-23` Workstreams A–C, already delivered)" | "…Workstreams A–C, implemented; closure and independent verification required before M2 (RD-M2-01)" |
| S-4 | same Charter `:131` (§9 diagram) | "Enterprise BAR (WP-23, already delivered — queried, never owned or duplicated)" | "(WP-23 A–C implemented, pending closure — queried, never owned or duplicated)" |
| S-5 | same Charter `:167` (§10 M2 Objective) | "BAR's own existing, delivered surface (`BarRegistrationRepository.get_by_identifier`/`get_by_work_package_and_reference`)" | "BAR's implemented surface (`…get_by_identifier`), once WP-23 A–C is closed". Also note that RD-M2-01/`IRA-BAE-001-M2 §4 C` excludes `get_by_work_package_and_reference` from M2 use. Objective scope is otherwise untouched |
| S-6 | `IRA-BAE-001_…_Readiness_Assessment.md:92` | "the one responsibility with a delivered, reusable dependency today" | "…with an implemented (not yet verified) dependency" |
| S-7 | `IRA-BAE-001_…_Readiness_Assessment.md:130` | "BAR's own already-delivered query surface" | "BAR's implemented (not yet verified) query surface" |
| S-8 | `architecture/06-Reviews/IRA-BAE-001-M1_Runtime_Contract_and_Gap_Analysis.md:373` (§13) | "BAR A–C read surface \| M2 \| Delivered; read-only" | "Implemented, uncommitted, unverified; read-only; closure required first (RD-M2-01)" |
| S-9 | `architecture/06-Reviews/BAR-WP23-WORKSTREAM-D-BUSINESS-ACTIVITY-ENGINE-PREREQUISITE-INVESTIGATION.md:142` | "Workstreams A–C remain delivered and usable" | "Workstreams A–C remain implemented (pending closure/verification) and usable" |
| S-10 | same investigation `:144` | "BAR's own decided scope (D1–D9) is fully delivered on the registration side regardless" | "…is fully implemented on the registration side (pending closure/verification) regardless" |
| S-11 | same investigation `:174` | "already substantially delivered by Workstreams A–C" | "already substantially implemented by Workstreams A–C" |
| S-12 | `architecture/05-Implementation/WP-BAE-001_Business_Activity_Engine_Charter.md:218–219` (§11 Dependencies) | "**Already available (delivered, certified, reusable as-is):** — Enterprise BAR (`WP-23` Workstreams A–C) — `bar_identifier_ledger`, `bar_registration`, and their repository/service query surface." | Move the BAR bullet out of "Already available (delivered, certified …)" into a dated note: "Enterprise BAR (`WP-23` Workstreams A–C): implemented, uncommitted, not yet independently verified; closure required before M2 (RD-M2-01)". The heading and the AuthorizationEngine bullet are accurate and stay unchanged |

*(S-12 added 2026-09-25 on re-verification of this inventory against `HEAD` by `git grep`; it was missed in the first pass. The same sweep confirmed these hits are **not** stale: `WPR-001:117`, whose "already-certified" refers to the Authorization Engine adapter; Charter `:100`/`:134`/`:186`, which refer to `WP-RTA-001`; and `IRA-BAE-001-M1_Independent_Review.md:244`, which refers to M1's own delivered scope.)*

**Informational, not stale:**
- Investigation `:124`–`:128` ("**Provided.**") describes what the code provides, which is accurate for implemented code.
- `IMP-REPORT-WP-BAE-001` and commit `94c99a1` cite "BAR A–C + WP-13 33 passed". That is a factual test count, but it was measured against untracked code. A reconciliation pass may annotate it and must not alter it (it is a historical record).

**Not in scope of this inventory:** the uncommitted WP-23 documents themselves (Charter, design, `BAR-INDEX.md`). They are not committed history and are handled by P-6 and the WP-23 closure itself.

### 7.1 Correction timing (added 2026-09-25, per RO instruction: "Do NOT bulk-correct … identify which can only be corrected AFTER WP-23 A–C independent verification/acceptance")

**No S-row is corrected now.** None is needed for A–C closure. Correcting any row now would write a *provisional* state into committed BAE governance, and that state would go stale again at acceptance. The Gate 1 reviewer is instead pointed at this inventory (§9, G1-7), so the stale text cannot be mistaken for evidence.

| Group | Rows | Why they wait | Correction form, once they can be made |
|---|---|---|---|
| **G-A: say "certified"** | S-1, S-2, S-12 | The claim is false now **and stays false after acceptance**: under RD-23-02 the A–C terminal state is ACCEPTED, and WP-level certification happens at WP-23 completion. The correct replacement wording (the acceptance record, the verification artifacts, the commit hash) exists only after P-9 and P-10 | After P-9 and P-10: strike through and replace with "WP-23 A–C tranche implemented, independently verified and accepted (`<acceptance record>`, commit `<hash>`); WP-23 remains OPEN" |
| **G-B: say "delivered"** | S-3, S-4, S-5 (first clause), S-6, S-7, S-8, S-9, S-10, S-11 | The claim was premature when written but will become substantively true at acceptance plus commit. Rewriting now would only be rewritten again | After P-10: a dated annotation beside the original wording, not a rewrite. The annotation records that the statement predated A–C verification and cites the acceptance record and commit. S-8 (M1 analysis) and S-9–S-11 (investigation) are dated review records: annotate only, never alter |
| **G-C: M2 scope point, not A–C status** | S-5 (second clause: `get_by_work_package_and_reference` named as an M2 surface) | Not an A–C status statement. It belongs to WP-BAE-001 M2 scope (`IRA-BAE-001-M2 §4 C`) | At M2 implementation authorization, in the WP-BAE-001 Charter synchronization, not in the A–C pass |

**Rows correctable before A–C acceptance:** none. The informational items (the "33 passed" test count in `IMP-REPORT-WP-BAE-001` and `94c99a1`) are historical records: annotate only, and only after P-10.

## 8. Integrity

- No BAR, BAE, AuthService, migration or test file was modified.
- `BAR-INDEX.md`, the WP-23 Charter and `WPR-001` are unchanged by this document.
- Workstreams D and E were not touched, and no adapter was created.
- No Business Activity was registered, and no identifier was assigned.
- Running the 22 BAR tests left the working tree unchanged (verified by `git status`).
- Nothing was staged, committed or pushed.

*(Integrity addendum, 2026-09-25 decision pass.)* That pass changed governance documents only:
- this document;
- `IMP-REPORT-WP-23_Enterprise_BAR_Mechanism.md` (new);
- `ROD-WP-23-AC-BAR-Registry-Authority-Decision-Preparation.md` (new);
- `BAR-INDEX.md` (status lines only);
- a dated note under WP-23 Charter §22.

No BAR, BAE, AuthorizationEngine, C-021/C-022 or other runtime code, migration or test was modified. No Business Activity was registered, and no identifier was assigned or issued. Nothing was staged, committed or pushed.

---

## 9. Independent Verification Scope — WP-23 A–C Tranche (Gate 1 and Gate 2)

**Prepared, not launched.** `CLAUDE.md §19.7`/`§19.7b` require the reviewers to be fresh-context and independent of the implementing session. No governance rule requires dispatching them immediately after readiness preparation. They are dispatched only when §10's conditions are met and the Repository Owner instructs it. Each gate is performed by a reviewer independent of every earlier gate and of this document's author.

**Object under review (fixed file list; anything else is out of scope):**
- **Workstream A:** `architecture/00-Governance/BAR-INDEX.md`.
- **Workstream B:** `models/bar_identifier_ledger.py`, `repositories/bar_identifier_repository.py`, `services/bar_identifier_service.py`, `alembic/versions/2026_09_22_0900-a7b8c9d0e1f2_bar_identifier_ledger.py`, `tests/test_bar_identifier_service.py`.
- **Workstream C:** `models/bar_registration.py`, `repositories/bar_registration_repository.py`, `services/bar_registration_service.py`, `alembic/versions/2026_09_22_1000-b8c9d0e1f2a3_bar_registration.py`, `tests/test_bar_registration_service.py`.
- **Shared:** the two BAR lines of `models/__init__.py`.
- **Report:** `IMP-REPORT-WP-23_Enterprise_BAR_Mechanism.md`.

All code paths are under `Backend/Services/AuthService/`.

**Governing sources the reviewers read directly:**
- the WP-23 Charter (§3–§7, §14–§16, §19–§22, and the §22 RD-23-02 note);
- `ENTERPRISE-BAR-MECHANISM-DESIGN-AND-IMPLEMENTATION-READINESS.md` (§4, §5, §6, §14–§16, §18, §19a.6);
- `ROD-ENTERPRISE-BAR-Decision-Preparation.md` (D2, D5, D7);
- this document (§0, §3, §7);
- `ROD-WP-23-AC-BAR-Registry-Authority-Decision-Preparation.md`;
- `CLAUDE.md` §19.7, §19.7b, §19.8.5 and §21.4.

### 9.1 Gate 1 — Independent Certification of the A–C tranche

| ID | Check | Pass criterion |
|---|---|---|
| G1-1 | **Report completeness** | `IMP-REPORT-WP-23` names every file in the object list, the governing sources, the design decisions requiring disclosure, the test evidence and the open items. It claims no certification, acceptance or WP-23 closure. Every claim in it is re-derived against source, not accepted from the report |
| G1-2 | **Authorized scope** | Each file traces to Charter §20/§21 Workstreams A, B or C and the design §4–§6/§18. No Workstream D, E, F, G or H behaviour exists (no discovery query, gate, cutover, router, API or adapter). No `IMP-001 §6.22` attribute beyond D2's eight fields. **Explicit sub-check:** Charter §21 row C describes Workstream C as "governance-only, no runtime", yet the implementation includes a runtime table, service and migration. The reviewer must report whether that is within authorization *as RD-23-03 has been decided at the time of review*. If RD-23-03 is still open, the reviewer reports this as an unresolved scope question and does not decide it |
| G1-3 | **Migration ancestry** | `alembic heads` shows exactly one head. `b8c9d0e1f2a3 → a7b8c9d0e1f2 → f6a7b8c9d0e1` is intact. Both BAR migrations are purely additive (no `ALTER` of an existing table). `downgrade()` reverses `upgrade()` exactly. The reviewer records whether the parents `e5f6a7b8c9d0`/`f6a7b8c9d0e1` are **committed** at review time (RD-23-01); if not, the tranche is not commit-eligible |
| G1-4 | **Model/migration parity** | Columns, types, nullability, defaults and server defaults, FK, unique and check constraints, and indexes match between the models and the migrations. Named constraints in the migrations versus `unique=True` in the models, and the extra `ix_bar_registration_identifier` index, are examined and reported as parity or as drift |
| G1-5 | **Tests** | The two BAR test files are re-run by the reviewer, and the AuthService full suite is re-run as regression (counts re-measured, not copied). Each test's assertion is checked for testing what its name claims. Implementer tests are evidence of intent only |
| G1-6 | **Governance artifacts** | `BAR-INDEX.md` status lines match the actual state. §3 still has zero registrations and §6's example is outside the Register. No real Business Activity is registered and no identifier is issued anywhere in the repository. `C-024 D10`, `WPR-001` (beyond the WP-23 row) and `CBOR-INDEX.md` are unchanged by WP-23 |
| G1-7 | **Stale-statement non-reliance** | The reviewer confirms that no conclusion rests on the S-1 to S-12 statements (§7) |
| G1-8 | **Closure-unit correctness (RD-23-02)** | No artifact labels WP-23 COMPLETE, CLOSED or CERTIFIED as a Work Package. D and E are recorded as incomplete. The tranche's claimed terminal state is ACCEPTED (after RO acceptance), not certified or closed. The Charter §22 note does not alter any other Charter text |
| G1-9 | **Tenant isolation (`§21.4`)** | Confirm that neither BAR table carries an organization or tenant column, and that no endpoint exists. Record that `§21.4`(a)–(c) do not attach and why, rather than assuming it |

### 9.2 Gate 2 — Verification & Validation of runtime and data integrity

**Method requirement (`§19.7b`):** at least one **purpose-built, from-scratch runtime probe per defect class** below, written by the Gate 2 reviewer, not adapted from `test_bar_*.py`. Probes live in the reviewer's own scratch location and are not added to the repository unless later authorized.

**FK enforcement requirement (mandatory):**
- The shared harness (`tests/conftest.py`) creates an in-memory SQLite engine **without** `PRAGMA foreign_keys=ON`, so SQLite silently ignores every FK in the existing BAR tests.
- **No FK-integrity conclusion may be drawn from the existing tests.**
- Every FK probe must run in a genuinely enforced environment, in order of preference:
  1. PostgreSQL, the declared production database, with the schema built by `alembic upgrade head`;
  2. otherwise, SQLite with `PRAGMA foreign_keys=ON` set on **every** connection (a `connect` event listener on the engine, not a one-off statement on a single connection). This option must include a positive control proving enforcement is on: an orphan insert must raise before any other FK probe counts.
- The reviewer states which environment was used. Where only SQLite was available, PostgreSQL-specific behaviour (the `substr`/`CAST` allocator, `server_default`, CHECK semantics) is reported as **not verified on the production dialect**, not as passed.

| ID | Defect class | Probe (from scratch) | Pass criterion |
|---|---|---|---|
| G2-1 | **FK integrity** | Insert a `bar_registration` row whose `identifier` is absent from `bar_identifier_ledger`, under enforced FKs (positive control first) | The insert is rejected by the database, not by application code |
| G2-2 | **Identifier uniqueness** | Duplicate `identifier` inserted directly into each table | Rejected by the database |
| G2-3 | **Duplicate registration** | Same `(owning_work_package, business_activity_reference)` pair, both through the service and by direct insert | The service raises `BarRegistrationAlreadyExists`; a direct insert is rejected by `uq_bar_registration_wp_reference`; no ledger row is consumed by the rejected attempt |
| G2-4 | **Two-state status** | Direct insert with `registration_status` other than `REGISTERED` | Rejected by `ck_bar_registration_status` |
| G2-5 | **Atomicity** | Force a failure *after* the ledger insert and *before* flush completes (for example an invalid registration field that reaches the database) | Neither a ledger row nor a registration row survives; no orphaned issued identifier results from the failed registration |
| G2-6 | **Collision retry and exhaustion** | Pre-seed the next candidate identifier to force a collision; then exhaust retries | The retry picks the next free value without a duplicate. Exhaustion raises the documented exception and leaves no partial rows |
| G2-7 | **Caller-session side effects** | Put an **unrelated pending object** in the same session, then trigger a collision retry or a duplicate path | Report whether `session.rollback()` inside `issue_identifier`/`register` discards the caller's unrelated pending work. That is a behavioural fact to disclose (it is in the design docstring only for issuance), and the reviewer classifies it (defect or disclosed behaviour) against `§19.8.5` |
| G2-8 | **Format and sequencing** | Issue across a boundary (seed `BA-000009`, `BA-000099`, `BA-999999`) | Correct zero-padding and `MAX+1` across digit boundaries. Behaviour at `BA-999999` + 1 (width overflow into seven digits versus `String(20)` and `^BA-\d{6}$`) is reported. No reuse after a rolled-back issuance produces a duplicate |
| G2-9 | **Concurrency** | Two sessions or connections racing to issue or register, in the enforced environment if it supports real concurrency | The UNIQUE backstop prevents duplicates; the loser either retries or raises the documented error. If the environment cannot race genuinely, the probe is reported as **not verifiable here** (as the implementer's own tests concede), not as passed |
| G2-10 | **Migrations** | On a clean database: `alembic upgrade head`, `downgrade -1` twice (C, then B), `upgrade head` again | Succeeds with no residue. The schema after upgrade matches the models (parity per G1-4) |
| G2-11 | **Read surface** | `get_by_identifier`, `get_by_work_package_and_reference`, `count_*` | Read-only (no flush or commit issued); an absent key returns `None` |
| G2-12 | **No side effects on governance files** | Run issuance and registration | `BAR-INDEX.md` is unchanged byte-for-byte (the service does not write it) |
| G2-13 | **Negative control** | Re-run G2-1 with enforcement **off** | The orphan insert is **accepted**. This proves G2-1's pass depends on enforcement and demonstrates why the existing harness gives no FK evidence |

**Harness/production-parity checklist (`§19.7b`):** answer explicitly:
- Does the harness enforce every constraint the declared production database enforces (FK, check, unique)? Expected answer: **no for FK**. The reviewer records it and states whether a harness change is required before acceptance (`§19.8.5`) or is recordable debt.
- Does any test span more than one tenant? Expected answer: not applicable, since BAR is platform-global. Confirm by reading the schema.

**Findings handling:** any finding requiring correction triggers `§19.7b` gates 3–4 (implementer remediation, then a further fresh-context verification with a negative control against the pre-fix code) before RO acceptance (P-9).

---

## 10. Gate 1 Readiness Statement (2026-09-25)

**WP-23 A–C is NOT yet ready for Gate 1 dispatch.** Gate 1's own authorized-scope check (G1-2) depends on RD-23-03, and Gate 1's migration-ancestry check (G1-3) can only confirm commit-eligibility once the RD-23-01 prerequisite commits exist.

| Condition | State |
|---|---|
| Implementation present and unchanged since it was written | Yes (files dated 2026-09-22; not modified since) |
| `IMP-REPORT-WP-23` exists (P-5) | **Yes**, provisional on RD-23-03 |
| `BAR-INDEX.md` status accurate (P-6) | **Yes** (status lines) |
| Verification scope prepared (§9) | **Yes** |
| RD-23-03 decided (P-4) | **No.** G1-2 cannot reach a scope conclusion on the runtime table while it is open |
| WP-20 and WP-21 migration ancestry committed (P-2, RD-23-01) | **No.** G1-3 can verify chain *structure* on the working tree, but not commit-eligibility |

*(Updated 2026-09-25.)* **RD-23-03 is now decided (Option D). Gates 1 and 2 are dispatched** to separate fresh-context reviewers on Repository Owner instruction. The RD-23-01 ancestry commits (P-2) are still missing, and G1-3 records that as found.

~~**Dispatchable when:** RD-23-03 is decided, **or** the Repository Owner explicitly rules that Gate 1 may proceed with RD-23-03 open and G1-2 reports the scope question as unresolved. Gate 1 may run before P-2 lands, because RD-23-01 governs the commit, not the review, provided G1-3 records the ancestry commit state as found. The **commit** (P-10) remains blocked until P-2 is met regardless.~~ ~~The last sentence still holds: **the commit (P-10) remains blocked until P-2 is met.**~~ *(Synchronized 2026-09-28, ST-6.)* P-2 is now met (`355ebbe`, `203bed1`). The commit (P-10) is no longer blocked by migration ancestry. ~~It awaits Gate 5 conditions C-1 and C-2 (being remediated) and the Repository Owner's acceptance (C-3).~~ *(C-3 addendum, 2026-09-28: C-1 and C-2 completed; C-3 satisfied (§0.2); the commit is made together with §0.2.)* This §10 statement is historical.
