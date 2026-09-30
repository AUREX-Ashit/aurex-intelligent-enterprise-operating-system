# WP-23 — Enterprise Business Activity Registry (BAR) Mechanism Implementation Charter

## 1. Document Control

**Work Package:** WP-23 — the next unclaimed Work Package number, verified directly this pass against `WPR-001` (highest row: `WP-22`, C-024, CHARTERED, implementation NOT STARTED). Repository-wide search for `WP-23` returned exactly one prior hit: `ENTERPRISE-BAR-MECHANISM-DESIGN-AND-IMPLEMENTATION-READINESS.md §19a.12`, which identified `WP-23` as a candidate number only, not a reservation or registration. No `WP-23` row, reference, or reservation exists anywhere in `WPR-001` or any other governance register checked this session. This Charter claims the number for its own self-identification only — it does not add a row to `WPR-001`; that registration is a separate, subsequent act, performed in §31 below (this Charter's own companion registration step, not silently assumed).

**Nature of this Work Package:** cross-cutting platform infrastructure, not a single capability's own Business Activity — the same class of Work Package as `WP-13` (Authorization Runtime Integration) and `WP-RTA-001` (Authorization Runtime Engine), neither of which charters a single `C-XXX` capability's own business outcome, but each of which builds a mechanism multiple capabilities subsequently consume.

**Governing capability:** none — this Work Package has no `CAP-001` capability of its own. It implements the enterprise Business Activity Registry (BAR) mechanism the seven original `§14` questions plus D8/D9 (implementation-planning determination) already fully decided, per `ROD-ENTERPRISE-BAR-Decision-Preparation.md`.

**Status:** **CHARTERED.** Implementation is authorized to begin **only** within the boundary §20/§29 of this Charter state, subject to the standard `CLAUDE.md §19.7b` five-gate closure sequence before release. No BAR mechanism is built by this Charter. No Business Activity is registered. No Business Activity Identifier is assigned. No `WPR-001` row exists until §31's own registration step is separately performed. *(2026-09-30: a **proposed** amendment, §21a (TD-171 remediation tranche), has been prepared. It is **not accepted and not authorized**; §20 is unchanged until Gate R1/R2.)* *(2026-09-30, Repository Owner acceptance: §21a is **ACCEPTED / IN FORCE** (Gate R1 satisfied). The TD-171 remediation tranche remains **NOT AUTHORIZED** (Gate R2 not satisfied). §20 is unchanged.)* *(2026-09-30, R2 synchronization: the Repository Owner **authorized** the TD-171 remediation tranche, Option A, **Gate R2 SATISFIED** (`ROD-WP23-TD-171-Remediation-Tranche-Authorization-Decision-Preparation.md` §19 (`d2aaade`)). **R3–R6 remain NOT SATISFIED. TD-171 remains OPEN.** §20 is unchanged.)*

**Prepared under:** direct Repository Owner instruction ("Proceed with the consolidated next governed stage: WP-23 — Enterprise BAR Mechanism Implementation"), 2026-09-22, following the complete enterprise BAR governance sequence: `BAR_ENTERPRISE_MECHANISM_DECISION_INVESTIGATION.md` → `ROD-ENTERPRISE-BAR-Decision-Preparation.md` (D1 Establish, D2 LOCKED-minimum scope, D3 retroactive registration, D4 moot, D5 identifier authority/timing, D6 no `IMP-001` amendment, D7 separate registration index, D8 transitional execution gate) → `ENTERPRISE-BAR-MECHANISM-DESIGN-AND-IMPLEMENTATION-READINESS.md` (consolidated design, READY WITH CONDITIONS; §19a, D9 per-BA cutover, an implementation-planning determination, not a new Repository Owner decision) → this Charter.

**A note on document type, disclosed rather than assumed:** unlike `WP-15`–`WP-22`'s own per-Business-Activity charter shape (a single BA's own implementation boundary), this Charter's own shape mirrors `WP-13`/`WP-RTA-001`'s own cross-cutting-mechanism charters, adapted to the 23-section structure this task's own governing instruction specified, so that the completed D1–D9 governance/design record translates into one implementation boundary covering a multi-workstream platform mechanism rather than one Business Activity.

---

## 2. Purpose

Translate the accepted enterprise BAR governance chain (D1–D8, `ROD-ENTERPRISE-BAR-Decision-Preparation.md`) and the completed consolidated design (`ENTERPRISE-BAR-MECHANISM-DESIGN-AND-IMPLEMENTATION-READINESS.md`, including its own §19a per-BA cutover determination) into an implementation authorization boundary for the enterprise Business Activity Registry mechanism. This is not implementation — it is the governance act that, subject to the boundary §20/§29 states, permits an engineering team to begin implementing precisely the design already specifies, subject to the standard `CLAUDE.md §19.7b` five-gate closure sequence before release.

---

## 3. Authoritative D1–D9 Baseline

Independently re-read for this Charter, not assumed from any prior summary: `ROD-ENTERPRISE-BAR-Decision-Preparation.md §0`/`§0b`/`§0c`/`§0d`/`§0e`/`§0f`/`§0g`; `ENTERPRISE-BAR-MECHANISM-DESIGN-AND-IMPLEMENTATION-READINESS.md` in full, including its own 2026-09-22 D8/§19a synchronization updates; `BAR_ENTERPRISE_MECHANISM_DECISION_INVESTIGATION.md` (the original evidentiary record).

| Decision | Outcome | Record |
|---|---|---|
| D1 | Establish a canonical enterprise BAR | `ROD-ENTERPRISE-BAR §0` |
| D2 | LOCKED-minimum scope: cataloguing/registration, canonical identity, execution-time gate, discovery-exclusivity | `ROD-ENTERPRISE-BAR §0b` |
| D3 | Registration applies retroactively to all 21 existing Business Activity rows | `ROD-ENTERPRISE-BAR §0c` |
| D4 | Moot | `ROD-ENTERPRISE-BAR §0` |
| D5 | BAR is the canonical Business Activity Identifier authority; assignment at BAR registration | `ROD-ENTERPRISE-BAR §0d` |
| D6 | No `IMP-001 §6.22` amendment required | `ROD-ENTERPRISE-BAR §0e` |
| D7 | BAR maintains its own separate registration index, distinct from `WPR-001` | `ROD-ENTERPRISE-BAR §0f` |
| D8 | Transitional execution gate — existing BAs continue executing during a governed transition; future BAs gated immediately; no permanent exemption; no cutover mechanism fixed by D8 itself | `ROD-ENTERPRISE-BAR §0g` |
| D9 | Per-BA cutover mechanism (implementation-planning determination, not a new Repository Owner decision) — each existing BA independently validated, registered, identified, verified, and moved to normal gating; one row's own unresolved data does not block another | `ENTERPRISE-BAR-MECHANISM-DESIGN-AND-IMPLEMENTATION-READINESS.md §19a` |

**Governing chain:** `BAR_ENTERPRISE_MECHANISM_DECISION_INVESTIGATION.md` → `ROD-ENTERPRISE-BAR-Decision-Preparation.md` (D1–D8) → `ENTERPRISE-BAR-MECHANISM-DESIGN-AND-IMPLEMENTATION-READINESS.md` (design + §19a/D9) → this Charter. **This Charter does not reopen, alter, or reinterpret any of D1–D9.**

---

## 4. Enterprise BAR Responsibility Boundary

Reproduced from the design document's own §3, not redesigned here: BAR **owns** Business Activity cataloguing/registration, canonical identity, execution-time gating, and registry-exclusive discovery (D2). BAR **does not** own Work Package governance (`WPR-001`), Charter governance, capability governance, Business Object governance (CBOR), general authorization policy, or any of `IMP-001 §6.22`'s broader responsibilities not included in D2 (validation checklist, status/version/dependency/governance-workflow/observability — D2/D6). **This Charter authorizes implementation of exactly the D2-decided boundary — nothing broader.**

---

## 5. BAR Registration / Index

Per D7 and the design document's own §6: BAR maintains its own separate authoritative registration index, distinct from `WPR-001`, structurally mirroring `CBOR-INDEX.md`'s own "pointer to the registering act" role. This Charter authorizes **building** this index (Workstream A) — it does not create `BAR-INDEX.md` itself. `WPR-001` is not modified, extended, or merged.

---

## 6. Business Activity Identifier Issuance

Per D5: BAR is the canonical Business Activity Identifier authority; the identifier is assigned at BAR registration. The design document's own §5 proposes `BA-NNNNNN` (six-digit, zero-padded, sequential) as the concrete format — **re-confirmed here as `[IMPLEMENTATION DESIGN — not constitutional text]`**, not a LOCKED requirement: the prefix is justified by the `BA-000089` illustrative example already used identically in `SD-002-004`/`CMD-001 §26.4a`/`IMP-001 §6.22.1b`, and the sequential pattern mirrors every existing CBOR identifier — but the format itself remains an engineering choice this Charter authorizes implementing, not a constitutional mandate. This Charter authorizes **building** the issuance mechanism (Workstream B) — no identifier is assigned by this Charter. `BA-NNNNNN` is never confused with, derived from, or cross-populated against: a WP number, a `CAP-001` capability ID, or any CBOR Business Object identifier (including `BIA-000001`).

---

## 7. Registration Mechanism

Per the design document's own §18, a registering-act convention mirroring the CBOR-ADR pattern (Workstream C) — a discrete, Repository-Owner-authorized act per Business Activity, citing its own Charter/`IMP-REPORT`/WP, that creates its BAR index entry and triggers its own identifier issuance (§6). This Charter authorizes **building** this mechanism; it does not perform any registering act itself.

---

## 8. Discovery Mechanism

Per D2/`RTA-001 §6.6` and the design document's own §9: the (not-yet-built) Business Activity Engine discovers executable Business Activities **exclusively** through BAR — never through implementation scanning or naming conventions. Per D8/§19a, this exclusivity applies immediately to future Business Activities; for the 21 existing rows, each continues via its own current, pre-BAR invocation path until it individually completes its own cutover (§19a.5 of the design). This Charter authorizes **building** this integration (Workstream D) at whatever pace the still-unbuilt general Business Activity Engine allows — a genuine engineering dependency this Charter does not resolve or accelerate.

---

## 9. Execution-Time Registration Gate

Per D2/`COM-001-005`/`PLT-001-004`/`GRC-001-008` and the design document's own §10: a Business Activity must be BAR-registered before it is execution-eligible. This Charter authorizes **building** this gate (Workstream E), implementing D8's own temporal-reach policy and D9's own per-row cutover mechanism (§10/§11 below) — it does not itself deny or permit any specific Business Activity's own execution.

---

## 10. D8 Transitional Execution Policy (preserved exactly, not reinterpreted)

- Newly introduced/future Business Activities are gated **immediately** once BAR is operational.
- The 21 existing Business Activities (D3) continue executing **uninterrupted** during the governed transition.
- Every one of the 21 remains **fully subject** to D3's own registration obligation — undischarged until performed.
- **No permanent exemption exists.**
- **No transition duration, deadline, or cutover date is invented by this Charter** — none was fixed by D8, and none is fixed here.

---

## 11. D9 Per-BA Cutover (preserved exactly, not reinterpreted)

For each existing Business Activity, independently: (1) validate its own registration data against §5's own mandatory fields (design document §4); (2) register it in BAR; (3) BAR assigns its own `BA-NNNNNN` identifier at that act (§6); (4) verify per the design document's own §19a.8 criteria; (5) move that Business Activity — and only that one — from transitional treatment to normal BAR-gated execution. **One Business Activity's own unresolved data does not block, delay, or otherwise affect any other Business Activity's own cutover.** This Charter authorizes implementing this mechanism (Workstream F's own engineering build) — it does not itself perform any row's own cutover.

---

## 12. 21-BA Retroactive Registration

Per D3 and the design document's own §11 inventory (reproduced by reference, not restated row-by-row here, to avoid any risk of divergence from the authoritative table): all 21 existing Business Activity rows across `WP-01`–`WP-21` are subject to eventual BAR registration via §11's own per-BA cutover mechanism. **Row 21 does not exist in this population** — C-024/`WP-22` BA-01 is NOT STARTED and is governed separately (§16 below), not as part of this 21-row set (the design document's own 21-row count already excludes it, counting only implemented/certified/partial rows).

---

## 13. Existing BA Data-Confirmation Process

Per the design document's own §11/§21 (Open Issues 2–4), 14 of the 21 rows have no unresolved data and may proceed through §11's own cutover flow without further confirmation; 7 rows require an explicit RO/governance confirmation step (multi-BA mapping for informal Charters; BLOCKED-BA treatment for `WP-03`'s own BA-04/05; infra-BA treatment for `WP-18`) before *their own* registration may proceed. **This Charter does not resolve any of these three confirmation items** — each remains open, to be resolved as ordinary implementation-planning detail during Workstream F's own execution, per row, without blocking the other 14 rows or any future Business Activity.

---

## 14. Security / Authority

Reproduced from the design document's own §14: registration authority (a Repository-Owner-authorized registering act, mirroring the CBOR-ADR pattern), execution authorization (the existing, unmodified per-endpoint mechanism — `require_platform_admin` and peers, or `Backend/Runtime/AuthorizationEngine` where already integrated), and business-user authorization are kept explicitly distinct. **No new authorization architecture is created** — this Charter authorizes reusing the existing mechanism exclusively.

---

## 15. Audit / Traceability

Reproduced from the design document's own §15: registration events, registration authority, and execution-gate evidence reuse the existing `record_audit`/`publish_event` pattern already used throughout `AuthService`/`AIService`. **No new enterprise audit platform is authorized** — this is explicitly not a C-114 (Audit & Assurance) implementation.

---

## 16. Testing and Independent Verification

Every workstream (§21 below) is subject to `CLAUDE.md §19.7b`'s own five-gate closure sequence (Independent Certification, V&V Audit, Remediation if needed, Independent Verification of Remediation, Release Readiness Audit) before this Work Package may be considered complete — no gate is skipped or abbreviated for this Work Package's own cross-cutting nature. Per `CLAUDE.md §21.4`'s own Mandatory Tenant-Isolation Test Checklist: flagged for confirmation at actual implementation time whether BAR's own runtime store (if built, per the design document's own §6) carries any tenant-scoped data — currently expected not to, since BAR is platform-global metadata about Business Activities, not tenant data, but this Charter does not pre-decide that finding.

---

## 17. Rollout and Containment

Prospective registration (new Business Activities, gated immediately per D8) and retroactive registration (the 21 existing rows, per-row per D9) proceed independently — neither blocks the other. Each of Workstreams A–G carries its own containment profile per the design document's own §19 (reproduced there, not restated here): additive, low-risk for A/B/C/F/G; moderate, feature-flaggable for D; moderate, per-row-independent for E (D9's own per-row cutover removes the population-wide failure mode a single omnibus cutover would have carried).

---

## 18. Failure / Partial-Completion Handling

Reproduced from the design document's own §19a.7: if some rows register successfully while others fail data validation, encounter an identifier collision, or surface a conflicting source record, the successful rows proceed to normal BAR-gated execution individually; the failing/stalled rows remain in "Not Registered (Transitional)" — still executing under D8, never exempted, never permanently blocked, simply not yet advanced. **No new governance exemption is created by any failure or partial-completion scenario.**

---

## 19. Explicit Exclusions / Non-Authorized Scope

This Charter does **not** authorize:

- implementation of any `IMP-001 §6.22` responsibility beyond D2's own decided four (full attribute schema, validation checklist, status/version/dependency/governance-workflow/observability — D2/D6, unchanged);
- any amendment to `IMP-001`, `COM-001`, `CMD-001`, `SD-002`, `PLT-001`, `GRC-001`, `RTA-001`, or `CLAUDE.md`;
- replacement of `WPR-001` as the Work Package → Capability authority (D7, unchanged);
- replacement of `CBOR-INDEX.md` or absorption of Business Object registration into BAR;
- a generalized authorization platform beyond reusing the existing mechanism (§14);
- a generalized audit platform beyond reusing the existing mechanism (§15);
- ERP, CRM, or general workflow-engine functionality of any kind;
- any Runtime Execution Architecture (`RTA-001`) capability beyond the narrow discovery/execution-gate integration §8/§9 describe;
- registration of C-024 BA-01, assignment of a Business Activity Identifier to it, modification of `C-024 D10`, or modification of the `WP-22` Charter (§16 below);
- retroactive registration, identifier assignment, or any code/schema/API/migration/test/frontend artifact — **none of these is created by this Charter itself**; all remain future, separately-gated implementation work performed under, not by, this Charter.

---

## 20. Implementation Authorization Boundary

**WP-23 is authorized to implement the enterprise BAR mechanism strictly within Workstreams A–G (§21), as specified in `ENTERPRISE-BAR-MECHANISM-DESIGN-AND-IMPLEMENTATION-READINESS.md` and this Charter.** This authorization does **not** extend to: unrelated capability work of any kind; alteration of D1–D9; modification of any constitutional document; redesign of C-024 or any other capability's own governance; or arbitrary platform refactoring unconnected to the BAR mechanism itself. Every workstream remains subject to `CLAUDE.md §19.7b`'s own five-gate closure sequence before release — this Charter authorizes beginning implementation; it does not itself certify, verify, or release any of it.

---

## 21. Dependencies (Implementation Workstreams, made implementation-ready)

| Workstream | Deliverable | Dependency | Acceptance criteria | Test expectation | Containment/rollback |
|---|---|---|---|---|---|
| **A. BAR index/registry** | `BAR-INDEX.md` (or equivalent), structurally mirroring `CBOR-INDEX.md` (design §6) | None (first workstream) | Structural shape matches the design document's own §4 registration-model fields | Structural validation | Low risk — additive, new file |
| **B. Business Activity identifier** | Issuer mechanism for `BA-NNNNNN` (design §5) | Workstream A | Uniqueness/format enforced; no collision with any existing identifier namespace (CBOR or otherwise) | Uniqueness/format tests | Low risk |
| **C. BAR registration** | Registering-act convention (design §7). *(Correction 2026-09-25, RD-23-04: also includes the runtime BAR registration store and mechanism already built, `bar_registration` / `BarRegistrationService`; see the note below this table)* | Workstreams A, B | Each act cites its own Charter/`IMP-REPORT`/WP; collision-checked before registering | Governance-artifact review per act | ~~Low risk — governance-only, no runtime~~ *(Correction 2026-09-25, RD-23-04:)* Low risk — additive; includes the runtime registration store (not a runtime consumer, gate or discovery path) |
| **D. Discovery integration** | Engine query surface against the index/store (design §9), excluding unregistered future BAs, leaving not-yet-cutover existing rows untouched | Workstreams A–C; whether/when the general Business Activity Engine is built | Discovery correctly excludes unregistered future BAs; leaves existing rows' own current routes untouched pre-cutover | Independent V&V per `CLAUDE.md §19.7b` | Moderate — ~~first runtime component~~ *(Correction 2026-09-25, RD-23-04:)* first runtime **consumer** component (Business Activity Engine / discovery integration; **not implemented**); feature-flag discovery-gated paths |
| **E. Execution gate** | Gate implementing D8/D9's own per-row transitional policy (design §10, §19a) | Workstream D | Gate denies unregistered future BAs, permits cutover-completed rows, does not deny any not-yet-cutover existing row | Full regression suite; independent V&V | Moderate — per-row independence (D9) limits blast radius of any single failure |
| **F. 21-BA retroactive registration/cutover** | Each of the 21 rows individually cut over per §19a.5 of the design (14 immediately eligible; 7 pending their own data confirmation, §13 above) | Workstreams A–C; the 7 rows' own confirmations | No certification record altered; each cutover row independently satisfies the design document's own §19a.8 six-item verification | Independent reviewer confirms no reopening of any WP's own certification, per row | Low risk — additive, per-row; a single row's own failure does not affect the other 20 |
| **G. Verification/testing/governance** | Full test suite, audit-hook wiring (reusing existing mechanism, §15), `CLAUDE.md §19.7b` five-gate closure | Workstreams A–F | Per `CLAUDE.md §19.7b`'s own gate criteria | Same five-gate sequence | Low risk |
| **H. C-024 integration readiness** | No action within this Charter's own scope — confirmation only, at the future point BA-01 is separately authorized for implementation, that it follows Workstreams A–C's own established mechanism | `C-024 D10` (unchanged) | N/A until BA-01 implementation is separately authorized | N/A | N/A |

*(Correction note, 2026-09-25 — Repository Owner decision **RD-23-04**, resolving Gate 1 finding CERT-F-01 in `architecture/06-Reviews/CERT-WP-23-AC_BAR_Workstreams_A-C.md`. It is recorded in `architecture/06-Reviews/IRA-WP-23-AC_BAR_Workstreams_A-C_Closure_Readiness.md §0`. The original wording of rows C and D is preserved above, struck through.)*
- **The contradiction.** Row C called Workstream C "governance-only, no runtime", and row D called Workstream D the "first runtime component". Yet §20 authorizes work "as specified in" the design, and design §6 delegated the runtime-store question to Workstreams C/D.
- **Ratification.** The Repository Owner **ratifies the runtime construction already performed under Workstreams B and C** as within the authorized WP-23 design boundary: `bar_identifier_ledger`, `bar_registration`, their repositories and services, and migrations `a7b8c9d0e1f2` and `b8c9d0e1f2a3`.
- **Workstream C** accordingly includes the runtime BAR registration store and mechanism already built.
- **Workstream D** remains the Business Activity Engine / discovery integration work. It is the first runtime *consumer* of BAR and **has not been implemented**.
- **The layered authority model of RD-23-03 remains authoritative:**
  - the registering act is the governance authority;
  - `bar_registration` is the execution-time runtime record;
  - `BAR-INDEX.md` is the human governance catalogue;
  - reconciliation between the governance and runtime records remains required.
- **This correction is not** an expansion of WP-23 scope. It does not authorize Workstream D or E, WP-BAE-001 M2, any Business Activity registration, runtime execution gating or any new runtime behaviour. No other Charter text is amended.

---

## 21a. TD-171 Remediation Tranche (~~PROPOSED AMENDMENT — NOT ACCEPTED, NOT AUTHORIZED~~ ACCEPTED AMENDMENT — IN FORCE; ~~TRANCHE NOT AUTHORIZED~~ TRANCHE AUTHORIZED (R2); R3–R6 NOT SATISFIED)

**Amendment status:** ~~**PROPOSED.**~~ **ACCEPTED — IN FORCE** *(2026-09-30; Repository Owner Acceptance Record below)*.
- Prepared 2026-09-30 by Repository Owner instruction ("Prepare the WP-23 Charter amendment for the TD-171 remediation tranche"), as a governance-design task.
- ~~**This section is not in force until the Repository Owner accepts it (Gate R1).**~~ *(2026-09-30: accepted; Gate R1 satisfied; in force.)*
- **It authorizes no implementation.** The tranche needs separate authorization (Gate R2). *(2026-09-30: R2 satisfied; see the R2 Synchronization Note below.)*
- Preparing it satisfies **none** of the gates in §21a.7.
- Until accepted, §20's authorization boundary (Workstreams A–G) is unchanged.

**Repository Owner Acceptance Record (2026-09-30).** *(Recorded by direct Repository Owner instruction: "Record RO acceptance of the §21a WP-23 Charter amendment." Recorded as stated and not reinterpreted.)*
- The Repository Owner has reviewed and **accepted §21a**. The acceptance is of **the Charter amendment itself**, committed in `e5287e2`.
- §21a is **ACCEPTED / IN FORCE**. Under §21a.7, this acceptance is **Gate R1**, which is now satisfied.
- **The acceptance does not authorize the TD-171 remediation tranche.**
  - The tranche needs its own explicit implementation authorization (Gate R2).
  - Gates **R2 to R6 remain not satisfied**.
  - **No implementation is authorized** by this record.
  - §20's authorization boundary (Workstreams A–G) is unchanged.
- Workstreams **A–C remain ACCEPTED and are not reopened** (§21a.4). **WP-23 remains OPEN.**
- **TD-171 remains OPEN** until remediation is actually completed and closed under §21a.8.
- **No decided content changes.** OQ-R-1 to OQ-R-7, the mechanism, scope, ownership, exclusions, closure criteria, stop conditions, and the M2 and M2-P boundaries (§21a.1 to §21a.12) are accepted as written.
- **M2 remains NOT AUTHORIZED / NOT STARTED. M2-P remains CHARTERED / NOT AUTHORIZED / NOT STARTED.**

**R2 Synchronization Note (2026-09-30).** *(Governance synchronization of an already-recorded decision. No new decision.)*
- **Authoritative record:** `ROD-WP23-TD-171-Remediation-Tranche-Authorization-Decision-Preparation.md` §19 (`d2aaade`). **Decision: OPTION A — AUTHORIZE. Gate R2 SATISFIED.**
- **What it authorizes:** implementation of **only** the bounded TD-171 remediation tranche defined by this §21a, subject to the **14 binding conditions in that ROD's §19.2**.
- **The distinction is preserved:** this amendment's acceptance is **R1**; the tranche's authorization is **R2**.
- **Gates R3–R6 remain NOT SATISFIED and mandatory.** In particular:
  - R3 design/readiness, including the act-citation rule;
  - canonical production environment designation, database-role separation and reconciliation access, all outstanding;
  - TD-176 PostgreSQL verification before closure.
- **Not implemented, not completed.** Authorization implies no implementation. **TD-171 remains OPEN** until R6.
- **Not authorized:** TD-172 to TD-175 remediation. Workstreams A–C remain accepted and are not reopened, and WP-23 remains OPEN.
- **M2 remains NOT AUTHORIZED / NOT STARTED. M2-P remains CHARTERED / NOT AUTHORIZED / NOT STARTED.**

### 21a.1 Purpose

The tranche remediates **TD-171** (`TECH-DEBT.md`):
- no enforcement links a registering act to a runtime `bar_registration` row (GAP-23-03-1);
- no reconciliation exists between `bar_registration` and `BAR-INDEX.md` (GAP-23-03-2).

Its purpose is to close that BAR registration-governance gap before any downstream execution-eligibility consumer, **including WP-BAE-001 M2**, relies on BAR registration state. This fulfils the Gate 1/Gate 5 condition (CERT-F-04; G5-08; C-1) that the A–C acceptance carries forward.

### 21a.2 Authority

- The existing WP-23 governance authority. BAR owns registration (D2, §4). Registration authority is a Repository-Owner-authorized registering act (§7, §14); RD-23-03 layered model.
- `ROD-BAE-001-TD-171-BAR-Consumption-Decision-Preparation.md §17`: TD-171 must close before M2 authorization; BAR/WP-23 owns remediation.
- `ROD-WP23-TD-171-Remediation-Decision-Preparation.md §19`: **OQ-R-1 to OQ-R-7** (commit `691f079`).
- **No new authority model is created.** §14's "No new authorization architecture is created" applies unchanged.

### 21a.3 Scope (bounded)

The tranche covers only:
- **A.** A governed registration operation.
- **B.** Governing-act validation.
- **C.** Production write-path restriction.
- **D.** Database-role separation.
- **E.** Repository CI verification.
- **F.** `BAR-INDEX.md` consistency checks.
- **G.** Environment-level row ↔ index ↔ governance reconciliation.
- **H.** Preservation of audit and event evidence (the existing `record_audit`/`publish_event`, §15).
- **I.** Handling of ungoverned rows.
- **J.** PostgreSQL verification required by TD-176, where applicable.
- **K.** Independent review and closure evidence.

**The tranche does not cover:**
- BAR identity redesign or redesign of identifier allocation (D5 unchanged);
- new authority seats or a new authorization architecture;
- WP-BAE-001 M2 or M2-P implementation, or BAE runtime resolution;
- any replacement or unbinding lifecycle;
- a new act registry;
- tenant-specific BAR identity;
- a new Work Package;
- Workstreams D–H;
- any Business Activity registration or identifier assignment.

### 21a.4 Relationship to Workstreams A–C (not reopened)

- Workstreams **A–C remain ACCEPTED** (RD-23-02; C-3 acceptance, `IRA-WP-23-AC …`), committed in `b0f5a12`. **Their acceptance is not revoked or reopened.**
- This tranche does not rewrite their historical implementation, acceptance records, commit boundaries or closure decisions.
- Any remediation touching existing registration code is performed **under this tranche's own boundary**, not by retroactively altering the A–C acceptance.
- **WP-23 remains OPEN** (§22, RD-23-02 note). The tranche is a new, bounded tranche within WP-23, with its own implementation boundary, gate sequence and closure record.

### 21a.5 Responsibility

| Party | Responsibility |
|---|---|
| **WP-23 / BAR** | Owns the tranche: the governed registration write path; governing-act validation; registration integrity; `BAR-INDEX.md` reconciliation; TD-171 closure |
| **Infrastructure / deployment owner** | Designates the canonical production environment (OQ-R-5); provisions database roles (OQ-R-3); provides controlled, read-only, environment-scoped reconciliation access (OQ-R-6) |
| **WP-BAE-001 M2** | Downstream **consumer only**, read-only. Not a remediation owner. Never writes, registers, repairs or reconciles BAR, and never validates acts in place of BAR governance |
| **WP-BAE-001 M2-P** | Not an owner. No BAR write authority. Scope unchanged (RD-M2-07) |

### 21a.6 Work items (governance/design level; identifiers local to this section)

| ID | Work item | Basis |
|---|---|---|
| R-01 | Governed registration operation and governing-act validation. The act is a repository ADR/ROD-style record naming the BAR Business Activity Identifier, the Business Activity reference, the owning capability and/or Work Package, the governing decision, the registration intent and the governance authority. A free-text `registering_act` alone is insufficient. **The machine-verifiable citation rule is to be designed** *(R3 design synchronization, 2026-09-30, from `TDS-WP23-TD-171-R3-Remediation-Design-and-Readiness.md` §17.1 (`fa93fc7`); synchronization only, no new decision: **OD-1** — the act is a **two-part governed record**: an authorization component, before issuance, and an execution addendum that records the **BAR Business Activity Identifier actually issued at registration**. D5 is unchanged, and no identifier is pre-created. Until the addendum is present the row is not governed, and the OD-5 block applies. **OD-3** — machine-verifiable metadata uses a `\| Field \| Value \|` block, with fields specified in the TDS §17.1.3, subject to R3 acceptance. No act registry.)* | OQ-R-2, OQ-R-4 |
| R-02 | Production write-path restriction: the governed operation is the only production registration-write path. `register()` does not remain an unrestricted, application-callable production write path *(R3 design synchronization, 2026-09-30, from `TDS-WP23-TD-171-R3-Remediation-Design-and-Readiness.md` §17.1 (`fa93fc7`); synchronization only, no new decision: **OD-2** — this applies to **both** canonical BAR write paths, `register()` **and** `issue_identifier()`. Application/runtime callers can neither issue identifiers nor register, and static caller verification covers both methods. This is a restriction within §21a.3 C–D, not a Workstream B/C scope expansion.)* | OQ-R-2, OQ-R-3 |
| R-03 | Database-role separation: the BAE/M2 read path cannot write registrations, and only the governed write path holds registration-write capability. Negative tests are required *(R3 design synchronization, 2026-09-30, from `TDS-WP23-TD-171-R3-Remediation-Design-and-Readiness.md` §17.1 (`fa93fc7`); synchronization only, no new decision: **OD-2** — the AuthService runtime database role holds **no INSERT, UPDATE or DELETE** on either BAR table (`bar_identifier_ledger`, `bar_registration`). The governed deployment-time operation is the controlled production write path. No new runtime authority. Provisioning remains an external prerequisite.)* | OQ-R-3 |
| R-04 | Repository CI verification of governing-act references and `BAR-INDEX.md` consistency (no database access) | OQ-R-2, OQ-R-6 |
| R-05 | Environment-level reconciliation of persistent rows against the canonical governance and index state, using infrastructure-provided read-only access | OQ-R-2, OQ-R-6 |
| R-06 | Designation of the single canonical production BAR/AuthService database. Identifiers are enterprise-global; no competing canonical issuance; non-production data never becomes canonical. **Not yet designated** *(R3 design synchronization, 2026-09-30, from `TDS-WP23-TD-171-R3-Remediation-Design-and-Readiness.md` §17.1 (`fa93fc7`); synchronization only, no new decision: **OD-4 remains OPEN / EXTERNAL PREREQUISITE.** No environment name, database identity, connection identifier or deployment designation is recorded.)* | OQ-R-5 |
| R-07 | Ungoverned-row handling: classify, quarantine or block, record evidence. Never silently adopt, delete or rewrite. Any disposition needs separate authorization *(R3 design synchronization, 2026-09-30, from `TDS-WP23-TD-171-R3-Remediation-Design-and-Readiness.md` §17.1 (`fa93fc7`); synchronization only, no new decision: **OD-5** — a **deployment-level integrity block**: detect, block, report, preserve, and require separately governed remediation. **No new BAR registration status.** No silent delete, rewrite, adoption or reinterpretation. M2 does not compensate. The seven R3 states stay distinct (TDS §7).)* | OQ-R-7 |
| R-08 | PostgreSQL/asyncpg verification | TD-176 |
| R-09 | Independent verification and review (`CLAUDE.md §19.7b`, §16), with negative controls | §16; ROD §12 |
| R-10 | Closure and governance synchronization: TD-171 closure record; `TECH-DEBT.md` synchronization; the G5-08 severity reassessment at the applicable consumer gate | ROD §19.3; OQ-171-4, OQ-171-5 |

No filename, class, endpoint, migration, SQL, role name or environment name is fixed here.

**R3 Design Synchronization Note (2026-09-30).**
- The rows above carry dated synchronization notes for the Repository Owner design decisions recorded in `TDS-WP23-TD-171-R3-Remediation-Design-and-Readiness.md` §17.1 (`fa93fc7`).
- **OD-1** (two-part governed act), **OD-2** (both BAR write paths governed), **OD-3** (structured `| Field | Value |` governed-act convention; no act registry) and **OD-5** (deployment-level block; no new status) are **DECIDED**. **OD-4** (canonical environment designation) remains **OPEN / EXTERNAL**.
- This is synchronization of decisions already made, not a new decision. §21a scope, exclusions, gates and closure criteria are unchanged.
- **R3 remains NOT SATISFIED** (NOT READY FOR R3 ACCEPTANCE REVIEW). **TD-171 remains OPEN.** No implementation has started.

### 21a.7 Gates

| Gate | Condition | State at preparation |
|---|---|---|
| **R1** | This Charter amendment accepted by the Repository Owner | ~~**Not satisfied**~~ **Satisfied** (2026-09-30, Repository Owner Acceptance Record, §21a) |
| **R2** | The remediation tranche separately authorized for implementation | ~~**Not satisfied**~~ **Satisfied**: TD-171 remediation tranche authorized under §21a (2026-09-30, Option A; `ROD-WP23-TD-171-Remediation-Tranche-Authorization-Decision-Preparation.md` §19 (`d2aaade`)) |
| **R3** | Design and readiness complete: the tranche's `CLAUDE.md §19` checklist; the act-citation rule; the operation, role and reconciliation design; environment designation and infrastructure prerequisites confirmed | **Not satisfied** |
| **R4** | Implementation and controlled deployment verification complete | **Not satisfied** |
| **R5** | Independent verification and review complete: the §16 / `§19.7b` sequence, including remediation re-verification if needed | **Not satisfied** |
| **R6** | Closure evidence recorded. `TECH-DEBT.md` synchronization and G5-08 reassessment complete | **Not satisfied** |

**Preparing this amendment satisfies none of R1–R6.** *(2026-09-30: the Repository Owner's acceptance satisfies **R1 only**. **R2 to R6 remain not satisfied.** The tranche is not authorized.)* *(2026-09-30, R2 synchronization: **R2 SATISFIED**; the tranche is **authorized**. **R3 to R6 remain not satisfied.**)*

### 21a.8 Closure criteria

These trace to `ROD-WP23-TD-171 … §12` and the `§19.7b` model. TD-171 may close only with evidence of:
1. a valid governed registration;
2. rejection of an invalid or mismatched act;
3. `BAR-INDEX.md` consistency;
4. duplicate handling;
5. an unauthorized-write negative control;
6. role separation;
7. rollback and failure behaviour;
8. audit and event evidence;
9. PostgreSQL verification;
10. reconciliation across every applicable persistent environment;
11. ungoverned-row handling;
12. independent review;
13. `TECH-DEBT.md` synchronization;
14. the G5-08 severity reassessment.

The G5-08 reassessment is **not** performed by this amendment.

### 21a.9 Outstanding prerequisites

All of the following are outstanding:
- canonical production environment designation;
- infrastructure database roles;
- controlled read access;
- the exact machine-verifiable act-citation rule;
- the remediation design and `§19` checklist;
- TD-176 PostgreSQL verification;
- ~~tranche authorization (R2).~~ *(Reconciled 2026-09-30: **SATISFIED / COMPLETED**. R2 was authorized in `d2aaade` and synchronized into Charter §21a.7, WPR-001 and IMP-REPORT-WP-23 in `032d8d8`. This entry had been retained here, stale; see the R2 Status Reconciliation below.)*

**R3 External Prerequisites Request Note (synchronized 2026-09-30).**
- *Synchronization only; no new decision.* The TD-171 R3 external-prerequisites request (`TDS-WP23-TD-171-R3-External-Prerequisites-Request.md`, `7a3b639`; recorded in IMP-REPORT-WP-23 `566d424` and the WPR-001 WP-23 row `76acac2`) has been **issued to Platform Engineering**, the ownership role in `OPERATIONAL_OWNERSHIP.md`.
- The request records issuance only. It does not record any action by Platform Engineering.
- These are **external prerequisites, not repository implementation**. None is provisioned, available, verified, accepted or completed. ~~The list above and the R1–R6 gates are unchanged.~~ *(Reconciled 2026-09-30: the list above is unchanged **except** its stale "tranche authorization (R2)" entry, now reconciled as SATISFIED. The R1–R6 gate states in §21a.7 are unchanged.)*

| EP | Prerequisite | Status |
|---|---|---|
| EP-01 | Canonical production environment/database designation | **REQUESTED / NOT PROVIDED** |
| EP-02 | DB-role separation and controlled production write path | **REQUESTED / NOT PROVIDED** |
| EP-03 | Controlled, environment-scoped, read-only reconciliation access | **REQUESTED / NOT PROVIDED** |
| EP-04 | PostgreSQL verification environment | **REQUESTED / NOT PROVIDED** |

- **R3 remains NOT SATISFIED / NOT READY FOR R3 ACCEPTANCE REVIEW. TD-171 remains OPEN.**

**R2 Status Reconciliation (2026-09-30).**
- *Reconciliation of a stale status only; no new decision.* R2 (tranche authorization) was already **SATISFIED** by the Repository Owner decision in `d2aaade`, and `032d8d8` synchronized it into §21a.7.
- This §21a.9 list had nonetheless kept "tranche authorization (R2)" as outstanding. The R3 External Prerequisites Request Note above (`4e0f24a`) carried that stale entry forward.
- A read-only cross-record reconciliation identified the inconsistency. The stale wording is preserved above, struck through.
- **Now aligned with §21a.7:** R1 SATISFIED; **R2 SATISFIED**; R3–R6 NOT SATISFIED. The R2 decision and its scope, R-01 to R-10, and OD-1 to OD-5 (OD-1, OD-2, OD-3, OD-5 DECIDED; OD-4 OPEN / EXTERNAL) are unchanged.
- **Still outstanding:** the other items in the list above, and EP-01 to EP-04, all **REQUESTED / NOT PROVIDED**.
- **R3 remains NOT SATISFIED / NOT READY FOR R3 ACCEPTANCE REVIEW. TD-171 remains OPEN.**

### 21a.10 Boundary with WP-BAE-001 M2

- **TD-171 closure is a prerequisite to M2 authorization.** This amendment does **not** authorize M2.
- **M2 remains NOT AUTHORIZED / NOT STARTED. M2-P remains CHARTERED / NOT AUTHORIZED / NOT STARTED.**
- The tranche must close before M2 may consume BAR registration state as execution eligibility.

### 21a.11 Stop conditions

Tranche work halts and reports on any of the following:
- scope expansion beyond TD-171 (§21a.3);
- any attempt to reopen the A–C acceptance;
- missing governing-act validation;
- an unrestricted production `register()` remaining;
- inability to establish write/read database-role separation (recorded, never weakened);
- inability to inspect or reconcile the canonical environment;
- PostgreSQL verification failure;
- discovery of ungoverned persistent rows without an authorized disposition;
- any attempt to make M2 the remediation owner;
- any attempt to authorize M2 through this amendment.

### 21a.12 Traceability

| Source | Applied in |
|---|---|
| OQ-R-1 (vehicle B: bounded tranche; A–C intact; no new WP) | §21a, §21a.4, §21a.7 R1–R2 |
| OQ-R-2 (mechanism D) | §21a.3 A, E–G; R-01, R-02, R-04, R-05 |
| OQ-R-3 (governed operation + database-role separation; no new authority identity; not `require_platform_admin`) | §21a.3 C–D; R-02, R-03 |
| OQ-R-4 (ADR/ROD-style act; no act registry) | R-01 |
| OQ-R-5 (single canonical production environment; not yet designated) | R-06; §21a.9 |
| OQ-R-6 (infrastructure-provided read-only access; M2 not the owner) | §21a.5; R-04, R-05 |
| OQ-R-7 (quarantine/block ungoverned rows) | R-07; §21a.11 |
| `ROD-BAE-001-TD-171 … §17`; TD-171; CERT-F-04; G5-01, G5-08, C-1; RD-23-02; RD-23-03; RD-23-04 | §21a.1, §21a.2, §21a.4, §21a.10 |
| This Charter §4, §7, §14, §15, §16, §20, §22 | §21a.2–§21a.4 |

No new decision is made by this section.

---

## 22. Acceptance Criteria

This Work Package is complete only when, per `CLAUDE.md §19.7`'s own Business Activity Completion Gate and `§19.7b`'s own five-gate closure sequence: Workstreams A–G are each independently certified, V&V-audited, and Release-Readiness-audited; the 14 immediately-eligible existing rows have completed their own cutover; the 7 data-confirmation rows either complete their own cutover or remain explicitly, disclosedly transitional pending their own future confirmation (not silently dropped); no existing certification record was reopened or altered; `C-024 D10` remains unchanged; and no constitutional document was modified.

*(Note added 2026-09-25 — Repository Owner decision **RD-23-02**, recorded in `architecture/06-Reviews/IRA-WP-23-AC_BAR_Workstreams_A-C_Closure_Readiness.md §0`. This is a narrow closure-unit decision. It does not amend any other text of this Charter, including the Work Package completion criteria above.)*
- Workstreams **A–C** may be treated as a **separately closable implementation tranche** within WP-23. The tranche may reach IMPLEMENTED → INDEPENDENTLY VERIFIED → ACCEPTED.
- **WP-23 as a whole remains OPEN.** Workstreams D and E, and the remaining workstreams, stay incomplete.
- Acceptance of the A–C tranche does **not** make WP-23 COMPLETE, CLOSED or CERTIFIED. The Work Package-level completion conditions above and the §16/§20 five-gate sequence remain unchanged and still apply at WP-23 completion.

---

## 23. Self-Review (performed on this Charter before delivery)

- **D1–D9 were re-read directly for this Charter, not assumed from summary** (§3). **Confirmed.**
- **No settled decision (D1–D9) is reopened, altered, or reinterpreted anywhere in this Charter** — §10/§11 restate D8/D9 verbatim in substance. **Confirmed.**
- **D2's own LOCKED-minimum scope remains the controlling boundary** — §4/§19 explicitly exclude every broader `IMP-001 §6.22` responsibility. **Confirmed.**
- **D5's identifier authority/timing is preserved** — §6 restates BAR-issues-at-registration, with the `BA-NNNNNN` format explicitly re-labeled `[IMPLEMENTATION DESIGN]`, not constitutional text. **Confirmed.**
- **D7's separate BAR registry is preserved** — §5 authorizes building a registry distinct from `WPR-001`; `WPR-001` is not modified by this Charter. **Confirmed.**
- **D8's transitional execution policy is preserved exactly** — §10, verbatim in substance, no invented deadline/duration/bypass. **Confirmed.**
- **D9's per-BA cutover is preserved exactly** — §11, verbatim in substance, no invented population-wide gating. **Confirmed.**
- **All 21 existing Business Activities remain subject to eventual registration** — §12, unchanged from D3. **Confirmed.**
- **The 7 rows' own unresolved data items remain unresolved** — §13 explicitly declines to resolve multi-BA mapping, BLOCKED-BA treatment, or infra-BA treatment. **Confirmed.**
- **`C-024 D10` remains unchanged** — §16/§19 explicitly exclude BA-01 registration, identifier assignment, `D10` modification, and Charter modification from this Work Package's own scope. **Confirmed.**
- **No Business Activity was registered; no Business Activity Identifier was assigned; no `BAR-INDEX.md`, database, API, runtime service, migration, test, or frontend artifact was created by this Charter itself.** **Confirmed.**
- **`WP-23` was verified genuinely unclaimed** before this Charter's own drafting — repository-wide search performed, one prior candidate-only reference found (design document §19a.12), no reservation or registration existed. **Confirmed.**
- **This Charter does not itself register `WP-23` in `WPR-001`** — that is a separate, subsequent act (§31, this same governed stage, performed after this Charter's own self-review). **Confirmed, per this section's own boundary.**

---

*End of WP-23 — Enterprise BAR Mechanism Implementation Charter. Chartered, not implemented. D1–D9 preserved exactly, not reopened. `C-024 D10` unchanged, scoped only to C-024 BA-01. No `BAR-INDEX.md`, database, API, runtime service, migration, test, or frontend artifact was created. No Business Activity was registered. No Business Activity Identifier was assigned. Nothing staged, committed, or pushed.*
