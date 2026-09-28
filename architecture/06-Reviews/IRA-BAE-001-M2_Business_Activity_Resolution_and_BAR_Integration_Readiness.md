# IRA-BAE-001-M2 — Business Activity Engine: Business Activity Resolution & BAR Integration — Readiness Assessment and Design

**Work Package:** `WP-BAE-001` (Business Activity Engine), milestone **M2 — Business Activity Resolution & BAR Integration**
**Prepared:** 2026-09-25, per direct Repository Owner instruction ("prepare M2 properly so that implementation can begin once the Repository Owner authorizes it"). Design / readiness only.
**Status:** ~~**READINESS ASSESSMENT — NOT IMPLEMENTATION-READY.** One blocking dependency finding (§3.1) and six Repository Owner decisions (§14) must be resolved before M2 code.~~ *(Updated 2026-09-25 — Repository Owner decision pass, §0.)* **READINESS ASSESSMENT — NOT IMPLEMENTATION-READY.**
- Decided: RD-M2-01, RD-M2-03, RD-M2-04 and RD-M2-06; RD-M2-05 is decided in principle.
- ~~**RD-M2-02 remains OPEN**; see `ROD-BAE-001-M2-Identifier-Implementation-Binding-Decision-Preparation.md`.~~ *(Updated 2026-09-28.)* **RD-M2-02 decided: Option B2** (governed persistent binding registry), recorded in `ADR-043` and `ROD-BAE-001-M2 …` §0.6. M2 remains **NOT AUTHORIZED**.
- ~~M2 is blocked until WP-23 Workstreams A–C are closed and independently verified (RD-M2-01), and until RD-M2-02 is decided.~~ *(Updated 2026-09-28.)* The **RD-M2-01 prerequisite is satisfied** (§0): WP-23 A–C were accepted, committed (`b0f5a12`) and independently verified; WP-23 is not certified or closed and remains OPEN. **RD-M2-02 is decided** (Option B2, `ADR-043`). **Neither decision authorizes M2.** FO-2 (the M2 detailed design redone for B2, `ADR-043 §9`) ~~remains outstanding~~ ~~*(2026-09-28: design prepared in §16, **pending RO approval**)*~~ *(2026-09-28: **FO-2 design approved**; OQ-1 to OQ-4 decided, §16.L. Not M2 authorization; ~~FO-1,~~ FO-3, the §13 regeneration and the M2 authorization remain outstanding, §16.K. FO-1: the Master Technical Architecture was amended on 2026-09-28 (AMD-017, v7.4))*, and **TD-171 remains OPEN** (`ROD-BAE-001-M2 §0.5`).
- *(2026-09-29.)* **RD-M2-07 DECIDED:** Option B. A pre-M2 WP-BAE-001 milestone, **M2-P**, owns the B2 binding store, write operation and CI act-citation verification; M2 stays read-only. **RD-M2-08 DECIDED:** Option (a). Infrastructure is an external operational prerequisite. See `ROD-BAE-001-M2-Binding-Infrastructure-Ownership-Decision-Preparation.md` §11.
  - Governance decision: **complete**.
  - Infrastructure and M2-P implementation: **outstanding**.
  - M2 authorization: **outstanding**.
  - The full B2 §13 regeneration is the **next governance task**.
- **M2 remains NOT AUTHORIZED and NOT STARTED.**
**Baseline:** M1 ACCEPTED — COMPLETE (`94c99a1`; roadmap `ddf4869`). Governance prerequisites `aa263bc`.

**This document creates nothing executable.** No code, test, migration, schema, API, route, manifest, binding, BAR change, Business Activity registration, or identifier assignment. It amends no Charter, ADR, `IMP-001`, `RTA-001`, WP-23 artifact, or BAR artifact. Where a design choice is proposed it is marked `[DESIGN — pending approval]`; where a choice belongs to the Repository Owner it is listed in §14 and not assumed.

---

## 0. Repository Owner Decision Record — M2 Readiness Decisions

**Recorded:** 2026-09-25, by direct Repository Owner instruction ("GOVERNANCE/READINESS DECISION PASS ONLY"), responding to §14 of this document. Each decision is recorded as stated and is not reinterpreted. The instruction reaffirms: **M2 remains NOT AUTHORIZED and NOT STARTED; do not implement M2.**

| ID | Repository Owner decision (as recorded) | Status after this revision |
|---|---|---|
| **RD-M2-01** WP-23 A–C prerequisite | **SELECTED.** WP-23 BAR Workstreams A–C must be formally closed/committed and independently verified **before M2 implementation begins**. Stale governance statements that describe BAR A–C as already "delivered", "certified" or equivalent must be reconciled against the actual repository state, **without silently rewriting history**. WP-23 A–C remains a separate Work Package and governance boundary. **M2 does not absorb WP-23.** | **RESOLVED** (decision). ~~The prerequisite is **OPEN**: the closure-readiness assessment and stale-statement inventory are in `IRA-WP-23-AC_BAR_Workstreams_A-C_Closure_Readiness.md`. No statement was corrected in this pass~~ *(Updated 2026-09-28.)* **Prerequisite SATISFIED.** The evidence:<br>– WP-23 A–C were **independently verified**: Gate 1 (historical STOP; its blockers were subsequently resolved), Gate 2 (historical FAIL), Gate 3 remediation, Gate 4 PASS, Gate 5 PASS WITH CONDITIONS.<br>– They were **ACCEPTED** by the Repository Owner (`IRA-WP-23-AC §0.2`). ACCEPTED is the RD-23-02 terminal state for the A–C tranche, and it stands for this decision's "formally closed/committed".<br>– They were **COMMITTED** in `b0f5a12e84a9a3f7d9622bcbea4cee87b934be85`.<br>– The stale "delivered/certified" statements were **reconciled without rewriting history** (C-4), in `bae8350b89771c48ad0b9acd57c829cdb62be615`.<br>**WP-23 is NOT certified and NOT closed; it remains OPEN, with Workstreams D–H not implemented.** Satisfying this prerequisite does **not** authorize M2 |
| **RD-M2-02** Identifier → implementation binding | **NOT SELECTED — OPEN.** A focused architectural decision package is required, because the proposed host start-up binding table would establish the authoritative runtime mapping between the canonical identifier and executable implementation; it is not an implementation detail. The package must compare at least: A. host-service start-up binding table; B. governed persistent/documented binding registry; C. any other repository-supported mechanism, if evidence exists. **No option is selected; none is implemented.** | ~~**OPEN — RO decision required.**~~ **DECIDED 2026-09-28 — Option B2**: a governed database table holds the authoritative binding; the code-side realization is subordinate; reconciliation is required (`ADR-043`; `ROD-BAE-001-M2 …` §0.6). Prepared in `ROD-BAE-001-M2-Identifier-Implementation-Binding-Decision-Preparation.md`. The §7 "M-B recommended" wording above is superseded as a recommendation: it is retained as the analysis at that date, not as a pending selection. *(2026-09-28: B2 corresponds most closely to this document's §7 **M-C** ("BAE-owned persistent binding table"), which §7 assessed as not recommended; that assessment is retained as historical analysis. The §7 and §13.2–§13.4 M-B design text (composition-root binding, `binding.py`, "no table, no migration") does not reflect the decided form and must be redone for B2 (`ADR-043 §6`, FO-2) before any M2 implementation authorization.)* |
| **RD-M2-03** `§6.16.5` verification scope | **SELECTED.** M2 verifies only (1) the canonical Business Activity identifier and (2) BAR registration status. The other four `§6.16.5` checks (Activity Version, Supported Invocation Method, Business Domain, Required Platform Version) remain explicitly **NOT VERIFIED — NO AUTHORITATIVE SOURCE**. No source is invented. The gap is recorded as technical debt. **M2 resolution must be organization-independent**, and tests must show that two unrelated Organizations do not produce different Business Activity resolution merely because of tenant context. | **RESOLVED.** Gap recorded as `TD-170`. "Activity Status" is verified only in D2's two-state form (registered or not), as §6 records; `§6.22.9`'s "Only Active" check stays unverifiable and is included in `TD-170` |
| **RD-M2-04** WP-23 Workstream E relationship | **SELECTED.** The BAE consumes BAR registration state. WP-23 Workstream E remains the BAR-side execution-gate authority. The BAE must not duplicate or redefine Workstream E. The WP-23 Charter is **not** modified by this decision. | **RESOLVED** |
| **RD-M2-05** Host integration | **SELECTED IN PRINCIPLE.** M2 may use an additive AuthService integration boundary, proposed as `Backend/Services/AuthService/bae_integration/`, subject to the detailed M2 implementation design. **This does not authorize implementation.** No unrelated AuthService refactoring is authorized. | **RESOLVED IN PRINCIPLE**; detailed design and implementation authorization pending |
| **RD-M2-06** Reference vs invocation | **SELECTED.** M2 resolves an **opaque implementation reference** and does **not** invoke it. The invocation contract is deferred to the later milestone the governing WP-BAE-001 design identifies, currently **M5**. No invocation signature is introduced in M2 for convenience. | **RESOLVED** |
| **RD-M2-07** B2 binding infrastructure ownership *(added 2026-09-29)* | **SELECTED: Option B.** A separate pre-M2 milestone within WP-BAE-001 (**M2-P**) owns C1 (table, schema, migration), C2 (governed deployment-time write) and C3 (CI act-citation verification). M2 remains a read-only consumer; it owns C5 (start-up reconciliation) and C7 (`BindingSource` adapter). FO-2 §16.A is not reopened | **DECIDED** (`ROD-BAE-001-M2-Binding-Infrastructure-Ownership-Decision-Preparation.md` §11). It authorizes no implementation |
| **RD-M2-08** Infrastructure prerequisites *(added 2026-09-29)* | **SELECTED: Option (a).** CI target-store access and database-role provisioning are an external operational prerequisite, required before the first governed binding write against a deployed environment. FQ-7 stays REQUIRED. CI must not claim target-store reconciliation without an accessible target store. No infrastructure Work Package is created | **DECIDED** (`ROD-BAE-001-M2-Binding-Infrastructure-Ownership-Decision-Preparation.md` §11). FQ-6 and FQ-7 evidence remain **OUTSTANDING** |

**Immediate engineering priority, per RD-M2-01:** WP-23 Workstreams A–C closure, **not** M2. Workstreams D and E, a BAR-to-BAE adapter, any BAE M2 code, any Business Activity registration and any identifier assignment all remain out of scope.

---

## 1. Governing Sources Reviewed (`CLAUDE.md §17`, `§19.1`)

Read directly from the repository for this assessment. Prior session summaries were not treated as authoritative.

| Source | Sections relied on | Repository state |
|---|---|---|
| `WP-BAE-001_Business_Activity_Engine_Charter.md` | §5, §8, §9, §10 (M1 disposition note; M2; M3–M5 boundaries), §17 | Committed (`94c99a1`) |
| `IMP-REPORT-WP-BAE-001_Business_Activity_Engine.md` | Authorization, delivered files, remediation, TD-165 re-target, M1 Acceptance and Closure | Committed |
| `IRA-BAE-001-M1_Runtime_Contract_and_Gap_Analysis.md` | §0 (`RO-M1-01`–`12`), §8, §9, §13, §14.1 (`X-02`–`X-05`, `X-15`), §14.5 (`D-03`, `D-09`), §15 (M2 prerequisites 1–5), §16 | Committed |
| `IRA-BAE-001-M1_Independent_Review.md`; `…_Remediation_Independent_Review.md` | F-02 (strict bool), F-06–F-08 (→ TD-167–169), O-04 (TD-165 → M2) | Committed |
| `ADR-042` | §3 (`RO-M1-01`–`03`), §4.3, §6, §7 | Committed |
| `Backend/Runtime/BusinessActivityEngine/` (all modules, README, tests) | The actual M1 contract (§2) | Committed |
| `ENTERPRISE-BAR-MECHANISM-DESIGN-AND-IMPLEMENTATION-READINESS.md` | §3, §4, §9 (discovery), §10 (gate), §19a (D9) | **Untracked** |
| `WP-23_Enterprise_BAR_Mechanism_Implementation_Charter.md` | §3 (D1–D9), §4, §8 (Workstream D), §9 (Workstream E), §19–§20 | **Untracked** |
| `ROD-ENTERPRISE-BAR-Decision-Preparation.md` | §0b (D2), §0d (D5), §0e (D6), §8 (design-time vs runtime) | **Untracked** |
| `BAR-INDEX.md` | §2–§4, closing status line | **Untracked**; zero registrations |
| `BAR-WP23-WORKSTREAM-D-…-INVESTIGATION.md` | §0 (Option B), §8 | Committed (`aa263bc`) |
| AuthService BAR A–C: `models/bar_registration.py`, `models/bar_identifier_ledger.py`, `repositories/bar_registration_repository.py`, `repositories/bar_identifier_repository.py`, `services/bar_registration_service.py`, `services/bar_identifier_service.py`, their migrations and tests | Full read of registration model, repository, service | **Untracked** (§3.1) |
| `IMP-001_Implementation_Playbook.md` | §6.4, §6.5, §6.7 (BAC), §6.14 (CBAM), §6.15.4, §6.16.3, §6.16.5, §6.22.1–§6.22.9, §6.22.14, §6.23.8, §6.23.16, §6.29.2–§6.29.12 | Committed |
| `RTA-001 - Runtime Architecture and Execution.md` `[LOCKED]` | §4.7, §6.6 (discovery), §6.7 (Manifest Resolution) | Committed |
| `Backend/Runtime/AuthorizationEngine` contract; `AuthService/authz_integration/runtime_engine_path.py` | Import mechanism (TD-165) | Committed |
| `TECH-DEBT.md` | TD-165–TD-169 | Committed (`94c99a1`) |
| `CLAUDE.md` | §8, §16–§19, §19.7/§19.7b, §21.4 | — |

---

## 2. Authoritative Baseline — What M1 Actually Delivered

Verified against the committed code, not the reports.

| Element | M1 as delivered | M2 relevance |
|---|---|---|
| `BusinessActivityIdentifier` | Shape-only `BA-\d{6}` value object; never issues or checks registration | Reused unchanged — the canonical invocation identity (§4 A) |
| `BusinessActivityInvocation` | `identifier` (typed), `identity_id`, `organization_id`, optional membership/session/correlation, frozen `payload` | Reused unchanged |
| `RegistrationSource.is_registered(identifier) -> bool` | Only a real `True` proceeds; `False` → `ACTIVITY_NOT_REGISTERED`; non-bool or exception → `EXECUTION_FAILED` | **Insufficient for M2**: a bool cannot distinguish a malformed BAR answer from an unavailable one beyond "raised vs non-bool", and carries no registration record (§5 E) |
| `ManifestResolver.resolve(identifier) -> ManifestResolution(status, reason)` | Status enum `RESOLVED` / `NOT_IMPLEMENTED`; carries **no content**. Only `UnimplementedManifestResolver` ships | Must be extended to carry a resolved binding and a "registered but unresolved" outcome |
| `engine.py` Activity Resolution stage | Registration check, then manifest resolution; any non-`RESOLVED` → `NOT_IMPLEMENTED` | M2 replaces the `NOT_IMPLEMENTED` branch with real outcomes and hands the resolved activity to stage 3 |
| Package boundary tests | Core may not import `sqlalchemy`, BAR/service/`models`/`repositories` modules, `importlib`, `pkgutil`, `os`, `glob`, `sys`; may not reference `register`/`BarRegistration*` names | **Constrains placement**: any concrete BAR adapter must live host-side, outside the BAE core (§5 F, §12) |
| Result invariant | `COMPLETED` only if all sixteen stages complete | Unchanged; M2 cannot produce `COMPLETED` (stages 5–16 remain M3+) |

**M1 did not deliver:** a concrete BAR adapter, any manifest content or schema, any identifier → implementation mapping, host integration, or packaging (`TD-165`). All are M2 subjects (`RO-M1-03`, `RO-M1-04`; TD-165 re-targeted to M2).

---

## 3. Blocking Findings

### 3.1 B-1 — M2's sole external dependency (BAR A–C) is uncommitted and has no certification record

**Evidence (directly verified 2026-09-25):**
- Every BAR A–C file is untracked. `git ls-files Backend/Services/AuthService | grep bar_` returns nothing, and no commit in any branch touches `models/bar_registration.py`. This covers the models, repositories, services, both migrations (`2026_09_22_0900-…_bar_identifier_ledger.py`, `2026_09_22_1000-…_bar_registration.py`) and tests.
- `WP-23_Enterprise_BAR_Mechanism_Implementation_Charter.md`, `ENTERPRISE-BAR-…-READINESS.md`, `ROD-ENTERPRISE-BAR-…` and `BAR-INDEX.md` are also untracked.
- No `IMP-REPORT`, `CERT`, `VV-AUDIT` or `RRA` artifact exists for WP-23, committed or not.
- `BAR-INDEX.md`'s closing line records Workstream A as "**IMPLEMENTED — READY FOR INDEPENDENT VERIFICATION**".
- `WPR-001`'s working-tree WP-23 row reads "**CHARTERED — IMPLEMENTATION NOT YET COMPLETED**".

**Conflict with committed BAE governance:**
- `WP-BAE-001` Charter §10 M2 says "BAR (`WP-23` Workstreams A–C, **already delivered**)". The §9 diagram at line 131 says "WP-23, already delivered".
- `IRA-BAE-001` line 69 says "**Delivered, certified, and directly reusable as-is**".
- `WPR-001`'s WP-BAE-001 Dependencies cell says "delivered and certified".
- These are factual statements the repository does not support. BAR A–C is implemented in the working tree only. The M1 regression figure "BAR A–C + WP-13: 33 passed" was measured against untracked code.

**Why it blocks M2:**
- An M2 host adapter would import `repositories.bar_registration_repository`. Committing that adapter without BAR would produce a commit that does not import. Committing it with BAR would bundle WP-23 A–C into a WP-BAE-001 commit, contrary to `CLAUDE.md §8` and the one-capability, one-owner rule.
- `CLAUDE.md §19.8.5` does not allow a dependency on unverified code to be deferred as debt.

**Not corrected here.** The stale "delivered/certified" statements in the Charter, `IRA-BAE-001` and `WPR-001` are recorded only. Correcting them needs a separately authorized narrow pass, like `RO-M1-12`. → **RD-M2-01**.

### 3.2 B-2 — No governed source binds a Business Activity Identifier to executable code

**Evidence:**
- `ADR-042 §4.3` requires "an explicit, governed manifest/registry contract" but defines none.
- `IMP-001 §6.29.6` (CBAM v2 canonical attributes) lists Identity, Classification, Intent, Contracts, Authorization, Workflow, Metadata, Events, Transactions, Execution, AI, Observability, Error Handling, Testing and Governance. **None of them names an implementation, handler, entry point or code reference.** `§6.14` (CBAM v1) has none either, and neither do `RTA-001 §6.7` `[LOCKED]` or `§4.7`.
- `§6.29.2`: "The Manifest shall never be derived from implementation."
- No CBAM instance exists anywhere in the repository. `ROD-ENTERPRISE-BAR` §8 confirms: "no physical CBAM file exists anywhere in this repository".
- Existing Business Activities have no uniform invocable shape. They are bespoke service methods (for example `OfferingDefinitionService.establish(...)`) called from FastAPI routers.

**Consequence.** The *ownership* of the mapping is decided (`RO-M1-03`: the BAE). Its *form and location* are not decided anywhere. Choosing one is exactly the kind of architectural choice that `CLAUDE.md §18`/`§19.4` forbid making by assumption. → **RD-M2-02** (options in §7).

### 3.3 B-3 — Four of the six `§6.16.5` verification data have no authoritative source

This is the per-datum analysis required by `RO-M1-05`; see §6. Whether M2 may complete Activity Resolution while these data are reported as unverified is a Repository Owner decision. → **RD-M2-03**.

---

## 4. Answers — Identity and BAR (A–D)

**A. Canonical Business Activity invocation identity.**
- The identity is the **BAR-issued `BA-NNNNNN` Business Activity Identifier**: D5 (`ROD-ENTERPRISE-BAR §0d`), `IMP-001 §6.22.1b`/`SD-002-004`, format per `BAR-INDEX.md §2` `[IMPLEMENTATION DESIGN]`.
- In the BAE it is the existing `BusinessActivityIdentifier` value object, carried in `BusinessActivityInvocation.identifier`. No other identity is introduced; the `business_activity_reference`, `C-XXX` and `WP-NN` values are never invocation keys.
- Version is not part of the identity (§6, Activity Version).

**B. How the BAE obtains it.**
- The **invoker** supplies it (`IMP-001 §6.15.3`: FastAPI adapter, event subscriber, scheduler, AI caller). The BAE neither derives nor looks it up.
- The BAE validates shape at construction (M1) and registration through BAR (M2).
- The BAE never infers an identifier from a route, function name or module path (`ADR-042 §4.3`).
- How a *given invoker* knows the identifier for the activity it fronts belongs to the first consumer's own adapter (M7). M2 designs none.

**C. Exact BAR lookup required.** *(FO-2 note, 2026-09-28: the BAR lookup below is unchanged under B2. §16.B adds a second, separate read-only lookup of the governed binding, so "exactly one read-only query per invocation" becomes two, one per authority.)*
- Exactly one read-only query per invocation: `BarRegistrationRepository.get_by_identifier(identifier: str) -> BarRegistration | None` (untracked; see B-1). This is the surface the Charter §10 M2 names.
- `get_by_work_package_and_reference` is **not** used. It is BAR's duplicate-registration helper and would key resolution on non-canonical fields.
- `BarRegistrationService.register`, `BarIdentifierService` and every write path are never called.
- No enumeration or list query is needed. The BAE resolves a single named identifier and never "discovers" a population, so Workstream D's enumeration contract is not required by M2 (§8).

**D. Exact data BAR must return to the BAE.**

| Field | Needed by M2? | Use |
|---|---|---|
| `identifier` | **Yes** | Must equal the requested identifier exactly; a mismatch is a malformed response |
| `registration_status` | **Yes** | Must be exactly `"REGISTERED"`, the only legal value under D2 and the table's CHECK constraint; anything else is malformed |
| `owning_capability`, `owning_work_package` | Carried, not verified | Traceability in the resolved activity and stage report. Not used for resolution, and not a substitute for Business Domain (§6) |
| `registering_act`, `registered_at`, `is_retroactive`, `business_activity_reference` | Carried only | Traceability; no runtime decision depends on them |

**Existing BAR data is sufficient for M2's registration step. No BAR field is missing for the registration check.** The data BAR does not hold (version, lifecycle status, invocation method, domain, platform version, implementation mapping) is excluded from BAR by D2/D6, and `ADR-042 §7` forbids adding it. M2 therefore requires **no BAR schema or contract change** (§3 of the task). The gaps are recorded as manifest-side gaps (§6, §7).

---

## 5. Answers — Outcome Discrimination (E)

`[DESIGN — pending approval]`: extend the M1 `RegistrationSource` port so that it returns a typed lookup instead of a bare `bool`, and extend `ManifestResolver` so that it returns content. The five cases are then distinguished structurally, never by truthiness (F-02 discipline preserved):

| Case | Detected where | Proposed stage result | Proposed `ExecutionOutcome` |
|---|---|---|---|
| **Not registered** | Adapter: `get_by_identifier` returns `None` → lookup `NOT_REGISTERED` | `TERMINATED` | `ACTIVITY_NOT_REGISTERED` (existing) |
| **Registered but unresolved** | Lookup `REGISTERED`, but the Manifest Resolver has no binding → `UNRESOLVED` | `TERMINATED` | new `ACTIVITY_NOT_RESOLVED` (proposed; `§6.16.5`: "Activities that cannot be resolved shall terminate before execution begins") |
| **Resolved** | Lookup `REGISTERED`, binding found and self-consistent (§7) | `COMPLETED`; resolved activity handed to stage 3 | — (continues) |
| **Malformed BAR response** | Engine: the lookup is not a `RegistrationLookup`; or a record's `identifier` ≠ requested; or `registration_status` ≠ `"REGISTERED"`; or a `REGISTERED` lookup without a record | `TERMINATED` | `EXECUTION_FAILED`, with discriminator `MALFORMED_REGISTRATION_RESPONSE` |
| **Unavailable BAR dependency** | Adapter or engine: the query raises (connection, session or SQL error) | `TERMINATED` | `EXECUTION_FAILED`, with discriminator `REGISTRATION_SOURCE_UNAVAILABLE` |

- A malformed *manifest binding* is handled the same way: discriminator `MALFORMED_MANIFEST_BINDING`, detected when the binding's declared identifier ≠ the requested identifier, or when a binding has no implementation.
- The discriminators are a stage-level reason code. They are deliberately **not** the canonical `IMP-001 §6.28` error taxonomy, which belongs to M6 (`D-06`).
- Raw exception text must not be copied into `reason` for these new paths. This avoids widening `TD-169`.
- `TD-167` (a `None` manifest resolution raising `AttributeError`) is closed by the same strict type check. It is re-targeted to M2 in its own register entry.

---

## 6. Per-Datum Source Analysis (`RO-M1-05`; `IMP-001 §6.16.5`; `D-03`)

| `§6.16.5` datum | BAR (D2) | CBAM (`§6.14`/`§6.29.6`) | Instance exists? | Finding |
|---|---|---|---|---|
| Activity Identifier | **Yes**: `bar_registration.identifier` (FK to ledger, unique) | Identity: Activity Identifier | BAR: yes | **Verifiable in M2** |
| Activity Status | Two-state only (row present = `REGISTERED`); `§6.22.9`'s six-state lifecycle excluded by D2/D6 | Identity: Status | No CBAM instance | **Verifiable only as "registered"**, which is D2's decided gate (`ENTERPRISE-BAR-… §10`: registration state is the "sole authoritative source" for execution eligibility). "Only Active may execute" (`§6.22.9`) cannot be verified: no source holds "Active" |
| Activity Version | Excluded (D2/D6) | Identity: Version | No | **No source.** `§6.23.8` version resolution cannot run. Only the single-version assumption `§6.29.5` ("exactly one active Manifest") is available, and nothing records even that |
| Supported Invocation Method | Excluded (`§6.22.8`'s API Endpoint / Scheduled Job / Event Trigger dimensions are outside D2) | **Not a CBAM attribute** | No | **No source anywhere** |
| Business Domain | Not held; `owning_capability` (`C-XXX`) is a capability, not a domain, and must not be substituted | Business Classification: Business Domain | No | **No source** |
| Required Platform Version | Not held | **Not a CBAM attribute** | No | **No source anywhere** |

**Conclusion.**
- M2 can authoritatively verify Activity Identifier and registration status (two-state). Nothing else is verifiable.
- Verifying Version or Business Domain requires a manifest instance to exist, which depends on RD-M2-02.
- Invocation Method and Required Platform Version have no defined attribute in any canonical source. Verifying them would first require an `IMP-001` CBAM amendment, which is outside M2's scope.
- `[DESIGN — pending approval]`: M2 verifies Identifier and registration only. It reports the other four in the stage report as `NOT VERIFIED — no authoritative source`, never as passed. The gap is recorded as a new Technical Debt / dependency item. → **RD-M2-03**.

---

## 7. Answers — Implementation Resolution (F, G, H) and the Manifest Contract

*(FO-2 note, 2026-09-28: RD-M2-02 selected **B2** (`ADR-043`). The M-B design below is preserved as the analysis at 2026-09-25 and is superseded for M2 by §16.)*

**What an implementation reference is.**
- The reference is **the object the BAE will later invoke at Business Rule Execution (stage 9, M5)**.
- M2 only *binds and returns* it. It never invokes it.
- Its callable signature depends on the M3 context and the M5 execution contract. Fixing it in M2 would pre-empt both. → **RD-M2-06**.

**Minimum manifest contract** `[DESIGN — pending approval]`, derived from `§6.29.6` Identity only (`D-09`), with nothing invented:

| Element | Source | Notes |
|---|---|---|
| `identifier` | CBAM Identity: Activity Identifier | Must equal the BAR identifier |
| `version` | CBAM Identity: Version | Declared only; not verified (§6) |
| `implementation` | **No canonical attribute** (B-2) | The one element no source defines. Its existence as a manifest-held element is itself part of RD-M2-02 |

All other `§6.29.6` sections (Authorization, Transactions, Execution, …) are consumed by later milestones (M4/M5/M6). M2 does not model them.

**Where the mapping lives (F) and how it is populated (G): options for RD-M2-02.**

| Option | Where the binding lives | How it is populated | Satisfies the no-discovery rule (H)? | Needs | Assessment |
|---|---|---|---|---|---|
| **M-A: Governed manifest artifact** | A versioned, per-BA CBAM instance file in the repository, listed in one explicit index | Authored by a governance act per BA; loaded by the host through an explicit, index-listed path (not a path derived from the identifier, which would be a naming convention, `§6.22.8`) | Yes, if index-listed | A new governed artifact type and storage location; a CBAM schema extension adding an implementation reference (an `IMP-001` amendment via ADR); still needs a code-side step to turn the file reference into an object, which would be a string-to-code dynamic import that the M1 boundary tests forbid, or else option M-B underneath | Most faithful to "governed manifest"; largest; requires constitutional work first |
| **M-B: Explicit composition-root binding** | Code in the **hosting service's composition root**: an explicitly constructed, immutable table `{BA-NNNNNN → (manifest identity, implementation object)}` passed to a BAE-owned, content-free resolver | Written by hand in the host's wiring for each BA a capability migrates (first one at M7). Built once at host start-up by explicit construction; no decorators, no import side effects | Yes: nothing is scanned, imported by name, decorated, or read from routes | Only BAE-side generic types in M2; no table, no file format, no migration | **Smallest sufficient option; recommended.** Open question for the RO: does a code-reviewed composition table count as the "governed" contract `ADR-042 §4.3` requires, given `§6.29.2` ("never derived from implementation")? The binding would reference the implementation but not be derived from it |
| **M-C: BAE-owned persistent binding table** | A new table in the host database: identifier → implementation reference string | Rows written by a governance act | The string must be turned into code by dynamic import, which is too close to module lookup by name and is forbidden by the M1 boundary tests | New table, migration, write path, per-host placement (`RO-M1-11`) | Not recommended; largest; overlaps BAR's persistence role |

**How the design avoids each prohibited mechanism (H)**, for M-B, and equally for M-A with an index:
- **Filesystem scanning:** none; no path is globbed or listed.
- **Decorator scanning:** none; no decorator exists or is read.
- **Route discovery:** none; FastAPI apps and routers are never read.
- **Import-time registration:** none; the binding table is built by explicit construction at composition, and module import has no side effect.
- **Duplicated BAR authority:** the binding table holds no registration state and issues nothing. A binding for an unregistered identifier is inert, because BAR is consulted first and the BAE never treats a binding as proof of registration.
- The existing boundary tests (no `importlib`, `pkgutil`, `os`, `glob` or `sys` in the core) are kept and extended (§13).

**Determinism.**
- Resolution is a pure lookup of one identifier in an immutable mapping built once.
- There is no version selection (§6), fallback, default binding, prefix match or ordering dependence.
- Construction fails fast on a duplicate identifier, an identifier mismatch or a missing implementation.

**Fail-closed.**
- A missing binding → `ACTIVITY_NOT_RESOLVED`.
- An inconsistent binding → `EXECUTION_FAILED` (`MALFORMED_MANIFEST_BINDING`).
- A resolver exception → `EXECUTION_FAILED`.
- No path fabricates a resolution.

---

## 8. Answers — Authority Boundaries (I)

| Authority | Owns | Does not own | M2 touch point |
|---|---|---|---|
| **BAR** (WP-23 A–C, D2/D5) | Registration, identifier issuance, registration state (two-state) | Implementation mapping (`ADR-042 §7`), version, lifecycle, invocation | Read-only `get_by_identifier`, host-side |
| **WP-23 Workstream E** (`RO-M1-04`) | The BAR-side execution-gate mechanism and authority | Runtime enforcement inside the BAE | **Not built.** See RD-M2-04 |
| **WP-23 Workstream D** | Integration of registry-exclusive discovery into the BAE | — | **Not needed by M2.** M2 resolves one named identifier and enumerates nothing. Workstream D stays deferred and dependent on WP-BAE-001 |
| **BAE** (`RO-M1-03`/`04`) | Runtime resolution, identifier → implementation binding, consuming and enforcing the registration prerequisite, orchestration | Registration, issuance, business rules | M2 itself |
| **Capability / business logic** | Its rules, Business Objects and implementation object | Being discovered, or binding itself | None in M2. A capability first supplies an implementation object to a binding at M7 |

---

## 9. Answers — Consumer, Reuse, New Work, Deferral (J, K, L, M)

**J. What an actual first Business Activity consumer requires** (M7, not M2). All of the following are needed:
- a Business Activity actually registered in BAR (none today; `BAR-INDEX.md` has zero rows; C-024 BA-01 stays unregistered under C-024 D10);
- the RD-M2-02 binding for it;
- its implementation exposed in the RD-M2-06 invocation shape (M5);
- an invoker adapter that constructs `BusinessActivityInvocation` from authenticated claims;
- the hosting boundary decision (`RO-M1-11`);
- stages M3–M6.

**M2 needs no first consumer.** It is verifiable with test-only bindings and BAR rows seeded in the test database, following WP-23's own test pattern. **No first consumer is identified or created here.**

**K. Reusable as-is:**
- M1's `BusinessActivityIdentifier`, `BusinessActivityInvocation`, pipeline, result invariant, `_Run`, logging, and the fail-closed exception handling;
- `BarRegistrationRepository.get_by_identifier` (subject to B-1);
- the `BarRegistration` eight-field record;
- AuthService's `AsyncSession` and test harness;
- the `runtime_engine_path.py` pattern, reused as a precedent and not modified.

**L. Newly implemented in M2** (subject to §14 decisions):
- the typed registration lookup result and the extended `RegistrationSource` port;
- the extended `ManifestResolution` (the `UNRESOLVED` status, and a `ResolvedBusinessActivity` carrying the registration record and the binding);
- a content-free, explicitly constructed resolver (M-B);
- the proposed `ACTIVITY_NOT_RESOLVED` outcome and the stage discriminators;
- the engine's stage 2 → stage 3 hand-off;
- the host-side BAR registration adapter in AuthService;
- a host import path for the BAE (TD-165);
- tests and documentation.

**M. Explicitly deferred:**

| Item | To |
|---|---|
| Invocation signature of the implementation; Business Rule Execution | M5 (RD-M2-06) |
| Full context construction; use of the resolved activity inside context | M3 |
| Per-BA authorization-policy source (M1 prerequisite 4; candidate CBAM Authorization Requirements) | M4, **undecided**. M2 records only that the minimum manifest carries no authorization data, and that M4 must source it through the RD-M2-02 mechanism or another decided source |
| Version resolution (`§6.23.8`), lifecycle beyond two-state, invocation method, domain, platform version | Beyond M2; each needs a source first (§6) |
| Workstream D (enumeration discovery) and Workstream E (BAR-side gate mechanism) | WP-23, deferred |
| Cross-service BAR access for non-AuthService hosts | `RO-M1-11`, first-consumer selection |
| Canonical error taxonomy (`§6.28`) | M6 (`D-06`); M2 discriminators are interim |
| `RTA-001` RC-01–RC-03 corrections; stale-document pass (`IRA-BAE-001-M1 §16` Condition 2); the B-1 stale "delivered/certified" statements | Separately authorized passes |

---

## 10. Dependency Analysis (§5 of the task)

| Dependency | State | M2 impact |
|---|---|---|
| **WP-23 BAR A–C** | Implemented, **untracked, uncertified** (B-1) | **Blocking** until RD-M2-01 is decided |
| **WP-23 Workstream E** | Not built | M2 must either consume the raw read surface as the interim gate consumption, or wait. RD-M2-04 |
| **WP-23 Workstream D** | Deferred, dependent on WP-BAE-001 | Not required by M2 (§8) |
| **AuthorizationEngine / WP-RTA-001** | Committed, certified with conditions, unmodified | Not touched by M2. M2 changes nothing in stage 4 |
| **Existing capability implementations** | Bespoke service methods; no uniform invocable shape | Not touched. Their shape is why RD-M2-06 is deferred |
| **Existing FastAPI routers** | Operative path for all 21 existing BAs (D8) | Not touched, and never read for discovery |
| **Existing runtime registration mechanism** | None exists besides BAR registration itself | None to reuse; none is to be created |
| **Service/container wiring** | FastAPI `Depends` per router; no DI container; AuthService imports the AuthorizationEngine through `runtime_engine_path.py` | The host adapter and BAE import path are **host-service integration**, excluded from M1 by the F-01 disposition and not explicitly granted to M2 by the Charter. RD-M2-05 |
| **Packaging (TD-165)** | Re-targeted to M2 | Resolved by the RD-M2-05 choice (a sibling path module, or formal packaging) |

**M2 cannot be implemented independently today.** It needs RD-M2-01 (the dependency state) and RD-M2-02 (the binding form) at minimum. No M3, M4, M5 or M6 work is required, provided RD-M2-06 is decided as "reference only, invocation deferred".

---

## 11. M2 Execution Contract (limited to what M2 owns)

*(FO-2 note, 2026-09-28: superseded for B2 by the §16.B resolution flow, which adds the governed binding and realization steps. The contract below is preserved as written.)*

```
BusinessActivityInvocation (from invoker; identifier = BAR-issued BA-NNNNNN)
  │
  ▼ Stage 1  REQUEST_RECEPTION            (M1, unchanged)
  ▼ Stage 2  ACTIVITY_RESOLUTION          (M2)
  │   2a Activity Identity Resolution  — identifier already a validated BusinessActivityIdentifier; no derivation
  │   2b BAR Registration Verification — RegistrationSource.lookup(identifier)          [host adapter, read-only]
  │        raises                        → EXECUTION_FAILED  (REGISTRATION_SOURCE_UNAVAILABLE)
  │        not a RegistrationLookup      → EXECUTION_FAILED  (MALFORMED_REGISTRATION_RESPONSE)
  │        NOT_REGISTERED                → ACTIVITY_NOT_REGISTERED
  │        REGISTERED, record inconsistent (identifier ≠, status ≠ REGISTERED, record missing)
  │                                      → EXECUTION_FAILED  (MALFORMED_REGISTRATION_RESPONSE)
  │   2c Implementation Resolution     — ManifestResolver.resolve(identifier)            [BAE-owned, explicit binding]
  │        raises / wrong type           → EXECUTION_FAILED
  │        UNRESOLVED                    → ACTIVITY_NOT_RESOLVED
  │        binding inconsistent          → EXECUTION_FAILED  (MALFORMED_MANIFEST_BINDING)
  │        RESOLVED                      → ResolvedBusinessActivity(identifier, registration record, manifest identity, implementation ref)
  │   2d Unverifiable §6.16.5 data reported NOT VERIFIED in the stage report (RD-M2-03)
  ▼ Stage 3  EXECUTION_CONTEXT_INITIALIZATION  receives ResolvedBusinessActivity  (M1 subset; full context M3)
  ▼ Stage 4  AUTHORIZATION_EVALUATION     (M1, unchanged; activity-scoped policy M4)
  ▼ Stage 5+ NOT_IMPLEMENTED              (unchanged; implementation reference is never invoked in M2)
```

The pipeline order, the sixteen stages, the result invariant and stage 4 are unchanged (`RO-M1-02`). M2 cannot yield `COMPLETED`.

---

## 12. Tenant-Isolation Placement (M1 prerequisite 5; `X-15`; `CLAUDE.md §21.4`)

- `bar_registration` has no organization column. Registration is platform-global by design (D2).
- M2 creates **no endpoint**, so `§21.4`'s endpoint checklist does not attach literally. Its full application stays at M3/M4 (context and authorization), as `IRA-BAE-001-M1 §9` records.
- The identifier is a platform-global identifier, not a tenant-owned foreign object. §21.4(c)'s "unrelated tenant's identifier" probe therefore has no tenant-owned object to probe.
- The Charter M2 verification text still requires tenant-isolation tests "applied fresh". M2 applies them in the form that is meaningful here (§13 T-7). These tests must prove that resolution is **organization-independent** (identical outcome for two unrelated Organizations) and that no organization or claim data reaches the BAR query or the binding lookup.
- The RO is asked to confirm this placement: RD-M2-03, item b.

---

## 13. `CLAUDE.md §19` M2 Implementation-Start Checklist (B2)

**Status: REGENERATED FOR B2 (2026-09-29) — PREPARED, NOT APPROVED. M2 implementation is NOT AUTHORIZED and NOT STARTED.** No M2 code may be written until every box in 13.1 is ticked by a Repository Owner act.

*Regeneration note (2026-09-29).*
- By Repository Owner instruction ("Proceed with the FULL §13 B2 REGENERATION"), this section **replaces** the M-B checklist of 2026-09-25 and its dated annotations of 2026-09-28/29.
- That version is preserved in repository history (last committed in `5f43cec`). Historical decisions elsewhere in this document (§0, §7, §11, §14 to §16) are unchanged.
- Basis:
  - `ADR-043` (B2);
  - FO-2 (§16, §16.L);
  - FO-3 (`TDS-BAE-001-M2-FO3 …`, §15.A, §15.B);
  - RD-M2-07 and RD-M2-08 (`ROD-BAE-001-M2-Binding-Infrastructure-Ownership-Decision-Preparation.md §11`).
- Every test below is **planned and required**. None of the B2 tests exists yet.

### 13.1 Authorization and prerequisites

**Satisfied** (decisions and designs complete):
- [x] **RD-M2-01:** BAR A–C prerequisite satisfied (§0; `b0f5a12`, `bae8350`). WP-23 remains OPEN (D–H not implemented).
- [x] **RD-M2-02:** B2 selected; `ADR-043` Accepted (`1a36969`).
- [x] **RD-M2-03:** only the identifier and registration status are verified; organization-independent resolution (§0, §12). *Its TD-170 recording is outstanding; see below.*
- [x] **RD-M2-04:** the BAE consumes BAR registration state; Workstream E is unchanged (§0).
- [x] **RD-M2-06:** M2 resolves an opaque reference; invocation belongs to M5 (§0).
- [x] **FO-1:** Master Technical Architecture AMD-017, v7.4 PART K (`867af46`).
- [x] **FO-2:** design approved, OQ-1 to OQ-4 decided (§16, §16.L; `accc127`).
- [x] **FO-3:** design approved (`e7c713b`). **Not implemented.**
- [x] **FQ-1 to FQ-8:** decided (FO-3 §15.A).
- [x] **IP-3:** resolved; `approved_by_actor_id` withdrawn (FO-3 §15.B).

**Decided, not implemented:**
- [x] **RD-M2-07:** Option B. The pre-M2 milestone **M2-P** owns C1 to C3; M2 owns C5 and C7 (§0).
- [x] **RD-M2-08:** Option (a). Infrastructure is an external operational prerequisite (§0).
- [x] **M2-P charter:** added to `WP-BAE-001` Charter §10 (`5f43cec`). **NOT AUTHORIZED / NOT STARTED.**

**Outstanding / blocking (each must be resolved before M2 authorization):**
- [ ] **M2-P:** implementation authorized, implemented and passed through its own `§19.7` gate (§13.10), so that M2 consumes a real, accepted binding store.
- [ ] **RD-M2-05:** detailed host-integration design, including:
  - the BAE import path or packaging choice (TD-165);
  - the host start-up wiring point for start-up reconciliation (§13.4, §13.9).
- [ ] **TD-171:** closed, or an explicit Repository Owner decision on how M2 may consume `bar_registration` while TD-171 is open (§16.H).
- [ ] **TD-170:** the register entry committed. It is currently present only in the uncommitted working tree, and RD-M2-03 relies on it.
- [ ] **TD-165:** packaging or path-module resolution, per RD-M2-05.
- [ ] **TD-176:** a PostgreSQL/asyncpg verification method and environment available for M2 (§13.7, T-18).
- [ ] **FQ-6:** target-store CI access (RD-M2-08). This does not block M2 code. It must exist before the first governed binding write to a deployed environment, and before any claim of target-store reconciliation.
- [ ] **FQ-7:** evidence that the read-only adapter role and the write role are provisionable. This is required for T-17. If infeasible, the constraint is recorded and FQ-7 is not weakened.
- [ ] **This regenerated §13** accepted by the Repository Owner.
- [ ] Explicit Repository Owner **M2 implementation authorization**, naming its scope (Charter §17). It must be AuthService-only (§13.2).

**M2 is NOT AUTHORIZED / NOT STARTED.** **M2-P is CHARTERED, NOT AUTHORIZED / NOT STARTED.**

### 13.2 Exact M2 implementation scope

M2 is a **read-only resolver and consumer**. It consumes the binding store **created by M2-P**. It does not own, create, change or write that store (RD-M2-07; FO-2 §16.A).

| # | In scope | Governing basis |
|---|---|---|
| 1 | **Typed registration lookup:** extend the M1 `RegistrationSource.is_registered -> bool` port to a typed `lookup` returning a registration result | §5; FO-2 §16.E |
| 2 | **BAR registration verification (stage 2b):** read-only, first, over `BarRegistrationRepository.get_by_identifier`. `NOT_REGISTERED` stops resolution | FO-2 §16.B; RD-M2-03, RD-M2-04 |
| 3 | **`BindingSource` port:** a new BAE-owned port, consulted only after 2b (stage 2c) | FO-2 §16.B, §16.E |
| 4 | **Read-only host binding adapter:** SELECT-only against M2-P's store, on the host's own session. It raises on failure and never converts a failure into "no binding". No caching (OQ-3) | FO-2 §16.E; FO-3 §12 |
| 5 | **Reference-keyed realization:** an immutable, explicitly constructed, fail-fast mapping from implementation reference to implementation object, supplied by the host (stage 2e) | FO-2 §16.D |
| 6 | **Reconciliation logic:** comparing binding references with realization keys, with the four states | FO-2 §16.F; FQ-6 |
| 7 | **Host start-up reconciliation:** fails closed **per identifier**; the host is not aborted | FQ-6; RD-M2-07 (C5) |
| 8 | **`REALIZATION_UNAVAILABLE`:** a binding without a realization gives `EXECUTION_FAILED` / `REALIZATION_UNAVAILABLE`, with no fallback | FO-2 §16.I |
| 9 | **Organization-independent lookup:** no organization or claims input to either lookup | RD-M2-03; §12; K-9 |
| 10 | **Opaque handle:** `ResolvedBusinessActivity(identifier, registration record, binding record, opaque handle)` returned to stage 3 | FO-2 §16.B (2f) |
| 11 | **M5 boundary:** the handle is never invoked; there are no invocation, signature or transaction semantics | RD-M2-06; FO-2 §16.G |
| 12 | **M1 integration preserved:** the sixteen stages, pipeline order, result invariant and stage 4 are unchanged; M2 never yields `COMPLETED` | `RO-M1-02`; §11 |

**Scope limitation.** M2 is authorized, if at all, for **AuthService as the only hosting service**. A non-AuthService host needs a cross-service BAR read, which is deferred under `RO-M1-11` (FQ-5). M2 introduces no such read.

**Outside M2:**
- **M2-P:** C1 table/schema/migration, C2 governed deployment-time write, C3 CI act-citation verification.
- **RD-M2-08 infrastructure:** C4 CI target-store access and reconciliation infrastructure; C6 role provisioning.

### 13.3 Governing documents

| Source | Relied on for |
|---|---|
| `WP-BAE-001_Business_Activity_Engine_Charter.md` §10 (M1, **M2-P**, M2, M5), §13, §17 | Milestone scope, gates, authorization rule |
| `WPR-001_Work_Package_Roadmap.md`, WP-BAE-001 row | Registered status |
| `ADR-042` (`RO-M1-01` to `RO-M1-03`; §4.1, §4.3, §6 + 2026-09-29 addendum, §7) | In-process placement; BAE ownership of the mapping; prohibited discovery |
| `ADR-043` (§4.1 to §4.4, K-2, K-7, K-10, §6, §7, §12 addendum) | B2 authority model |
| `Master_Technical_Architecture.md` v7.4, AMD-017, PART K (K.1 to K.9) | The architectural concept of the binding, reconciliation and the write/read separation |
| This document: §0 (RD-M2-01 to RD-M2-08), §5, §6, §12, §16 (FO-2) and §16.L | Decisions; outcome model; per-datum scope; tenant placement; the B2 design |
| `TDS-BAE-001-M2-FO3_…_Governed_Write_Path.md` §4 to §14, §15.A, §15.B, §17 | Physical contract that M2 reads (fields, uniqueness, many-to-one), failure semantics, reconciliation |
| `ROD-BAE-001-M2-Identifier-Implementation-Binding-Decision-Preparation.md` (K-1 to K-11, §0.5) | Constraints; TD-171 separation |
| `ROD-BAE-001-M2-Binding-Infrastructure-Ownership-Decision-Preparation.md` §11 | RD-M2-07 and RD-M2-08 |
| `IMP-001` §6.15.4, §6.16.3, §6.16.5, §6.22.8; §6.17 to §6.19 as boundaries only | Activity Resolution; pipeline; termination before execution; registry-exclusive discovery |
| `RTA-001 §6.6`, `§6.7` `[LOCKED]` | No implementation-specific discovery |
| `TECH-DEBT.md`: TD-165, TD-167, TD-170, TD-171, TD-175, TD-176 | Packaging; the resolver-result test; unverified data; the BAR act-to-row gap; the identifier CHECK; PostgreSQL |
| `RO-M1-11` (`IRA-BAE-001-M1 §0`) | Cross-service BAR access, deferred |
| `CLAUDE.md` §8, §18, §19, §19.7, §19.7b, §21.4 | Service boundaries, change control, gates, tenant-isolation checklist |

### 13.4 Expected M2 file list

File roles are fixed here. **New filenames are fixed at implementation design** and recorded in the M2 authorization. Any deviation from these roles is a STOP.

**A. M2 files (the M2 commit boundary):**

| Location | Role | Change |
|---|---|---|
| `Backend/Runtime/BusinessActivityEngine/business_activity_engine/ports.py` | Typed registration lookup; `RegistrationSource.lookup`; the `BindingSource` port and binding result; `ResolvedBusinessActivity` | Modify |
| `…/business_activity_engine/` *(new module; name at design)* | Realization type: immutable, reference-keyed, fail-fast construction | New |
| `…/business_activity_engine/` *(new module, or within an existing module; decided at design)* | Reconciliation logic, persistence-free | New or modify |
| `…/business_activity_engine/engine.py` | Stage 2 flow 2a to 2f (§16.B) and hand-off to stage 3. No change to stage 4 or later | Modify |
| `…/business_activity_engine/results.py` | `ACTIVITY_NOT_RESOLVED` and the §16.I stage discriminators (interim, not `§6.28`) | Modify |
| `…/business_activity_engine/__init__.py`, `README.md` | Exports; the M2 contract | Modify |
| `Backend/Runtime/BusinessActivityEngine/tests/` (`test_engine.py`, `test_contracts.py`, `test_package_boundary.py`, plus new resolution, realization and reconciliation tests) | T-1 to T-5, T-7 to T-15, T-19 to T-21 (§13.6) | Modify / new |
| `Backend/Services/AuthService/bae_integration/` *(new package, RD-M2-05)* | Host adapters: `RegistrationSource` over `get_by_identifier`; `BindingSource` over the M2-P store (read-only). Realization construction. The start-up reconciliation hook. The BAE import path (TD-165, interim) | New |
| **Host start-up wiring point** *(existing AuthService module to be named by RD-M2-05)* | The minimal call that runs start-up reconciliation | Modify, **only if RD-M2-05 approves it** |
| `Backend/Services/AuthService/tests/` *(new adapter and reconciliation tests)* | T-6, T-16 to T-18, T-20 | New |
| `IMP-REPORT-WP-BAE-001`, Charter status lines, `WPR-001` WP-BAE-001 row, `TECH-DEBT.md` (WP-BAE-001 items only) | Governance synchronization at acceptance | WP-BAE-001 hunks only |

**Unchanged (verified at the gate):**
- every BAR A–C file, migration and test;
- `BAR-INDEX.md`; the WP-23 Charter;
- `Backend/Runtime/AuthorizationEngine/**`; `authz_integration/**`;
- every router, capability service and model not named above;
- every M2-P file;
- `IMP-001`, `RTA-001`, `ADR-042`, `ADR-043`.

`binding.py` (the M-B resolver) is **not** part of the B2 design.

**B. M2-P files: outside this checklist and outside the M2 commit boundary.**
- The binding table model, migration, write operation and CI act-citation check, in the AuthService migration chain.
- These are governed by M2-P's own `§19` checklist.

**C. Infrastructure provisioning: outside repository M2 scope.**
- Target-environment access for CI reconciliation; database roles and credentials (RD-M2-08).

### 13.5 Dependencies and external prerequisites

| Class | Dependency | State | Needed for |
|---|---|---|---|
| **A. Governance** | RD-M2-05 detailed design, including TD-165 and the start-up wiring point | OUTSTANDING | M2 authorization |
| | TD-171 closure or RO decision | OUTSTANDING (OPEN) | M2 authorization |
| | TD-170 register entry committed | OUTSTANDING | M2 authorization |
| | Acceptance of this §13 | OUTSTANDING | M2 authorization |
| **B. M2-P** | M2-P authorized, implemented and passed through its own `§19.7` gate; its store readable by the M2 adapter | NOT AUTHORIZED / NOT STARTED | Before M2 consumes a real binding store (T-16 to T-18) |
| **C. Infrastructure (RD-M2-08)** | FQ-7: read-only adapter role and write role provisionable | OUTSTANDING | T-17; first deployed write |
| | FQ-6: CI access to the target binding store | OUTSTANDING | The first governed binding write to a deployed environment; any claim of target-store reconciliation. Not M2 code |
| | TD-176: PostgreSQL/asyncpg verification environment | OUTSTANDING | T-18; M2 acceptance (TD-176: "before … the first execution-eligibility consumer") |
| **D. Existing M1 runtime** | M1 (`94c99a1`); BAR A–C read surface (`b0f5a12`); AuthorizationEngine (unchanged) | Committed | All M2 work |
| **E. Deferred** | `RO-M1-11` / FQ-5: cross-service BAR read | DEFERRED | Any non-AuthService host. Excluded from M2 |
| | M5: invocation contract, realized-object validation, transactions (`§6.19`) | DEFERRED | Not M2 |
| | M3, M4, M6: context, activity-scoped policy, error taxonomy | DEFERRED | Not M2 |
| | TD-170: the four unverifiable `§6.16.5` data | OPEN | Reported as NOT VERIFIED by M2 |
| | TD-175: BAR identifier CHECK | OPEN (non-blocking) | A BAR schema pass. Not M2 |

A decision existing does not satisfy any row above. Only the stated evidence does.

### 13.6 Verification / test matrix

Each test is purpose-built, with negative controls where §19.7b applies. **Status: planned and required.** Existing M1 test files are named where a test extends them; no B2 test exists yet.

| ID | Test | Basis | Status |
|---|---|---|---|
| T-1 | **M1 engine regression, extended:** M1 pipeline behaviour and stage order unchanged (`test_engine.py`). Each §16.I stage-2 case yields exactly its outcome and discriminator; later stages are `NOT_REACHED` | `RO-M1-02`; §16.I | Existing file; extension planned |
| T-2 | **M1 contract and strict-typing regression, extended** (`test_contracts.py`, F-02): a truthy non-lookup, `REGISTERED` with no record, a mismatched identifier, or `registration_status` ≠ `REGISTERED` each give `MALFORMED_REGISTRATION_RESPONSE` | §5; F-02 | Existing file; extension planned |
| T-3 | **Fail-fast realization:** construction rejects a duplicate reference, an empty reference or a missing object. The mapping is immutable and reference-keyed. There is no default, prefix or fallback entry. The same input gives the same output | §16.D | Planned |
| T-4 | **No invocation:** a spy implementation records zero calls on every path, including resolution success and reconciliation | RD-M2-06; §16.G | Planned |
| T-5 | **Boundary:** the core imports no `sqlalchemy`, BAR, `models`, `repositories`, `importlib`, `pkgutil`, `os`, `glob` or `sys` (`test_package_boundary.py`, extended). Adapters issue SELECT only. `implementation_reference` is never imported dynamically. There is no scanning, decorator or import-time registration | K-3, K-10; `RTA-001 §6.6` | Existing file; extension planned |
| T-6 | **BAR registration adapter, read-only, on an FK-enforcing harness** (as `test_bar_transaction_safety.py` does; the shared `conftest.py` does not enforce FKs):<br>– a seeded registration gives `REGISTERED` with the exact record;<br>– absent gives `NOT_REGISTERED`;<br>– a failure raises, giving `REGISTRATION_SOURCE_UNAVAILABLE`;<br>– ledger and registration counts are unchanged, with no flush or commit | §16.E; §19.7b parity | Planned |
| T-7 | **Organization independence:** two unrelated Organizations get identical resolution for the same identifier. No organization or claim reaches the BAR or binding lookup | RD-M2-03; §12; `§21.4` | Planned |
| T-8 | **TD-167:** a `None` or wrongly typed resolver, lookup or binding result gives `EXECUTION_FAILED` and never raises | TD-167 | Planned |
| T-9 | **Result-invariant regression:** no path yields `COMPLETED`; stage 5 onward stays `NOT_IMPLEMENTED` | M1 invariant | Existing behaviour; regression planned |
| T-10 | **Mutation probes** (§19.7b): remove, in turn, the identifier-equality check, the status check, the strict type check, the binding-identifier check and the realization-presence check. Each removal must be caught | §19.7b | Planned |
| T-11 | **`BindingSource` behaviour:**<br>– present gives the binding record;<br>– absent gives `ACTIVITY_NOT_RESOLVED` / `BINDING_ABSENT`;<br>– raises gives `BINDING_SOURCE_UNAVAILABLE`;<br>– an identifier ≠ requested, an empty reference, or more than one row (a defensive case) gives `MALFORMED_BINDING_RESPONSE` | §16.I | Planned |
| T-12 | **Unregistered or invalid identifier:** a malformed identifier is rejected at M1 construction. A well-formed unregistered identifier gives `ACTIVITY_NOT_REGISTERED`, and the binding lookup is **never reached**, even if a binding row exists | §16.B; §16.I | Planned |
| T-13 | **`REALIZATION_UNAVAILABLE`:** a binding with no realization entry gives `EXECUTION_FAILED` / `REALIZATION_UNAVAILABLE`, with no fallback | §16.I; FQ-6 | Planned |
| T-14 | **Many-to-one:** two identifiers bound to one `implementation_reference` both resolve to the same handle. No uniqueness is assumed | FQ-4 | Planned |
| T-15 | **Start-up reconciliation:**<br>– aligned passes;<br>– a binding without a realization fails closed **for that identifier only**, other identifiers still resolve, and the host is not aborted;<br>– a realization without a binding is a reported orphan;<br>– missing binding and missing realization are distinguished;<br>– nothing is invoked | FQ-6; §16.F | Planned |
| T-16 | **Binding adapter against M2-P's real table,** on an FK-enforcing harness: correct reads; row count unchanged; no INSERT, UPDATE, DELETE, flush or commit issued | FO-3 §12; §16.E | Planned (needs M2-P) |
| T-17 | **Database read-only role:** the adapter runs under the read-only role, and a write attempt is rejected by the database. Without provisioned roles this is **OUTSTANDING evidence, never passed** | FQ-7; RD-M2-08 | Planned (needs infrastructure) |
| T-18 | **PostgreSQL/asyncpg:** T-6, T-11, T-15 and T-16 run on PostgreSQL | TD-176 | Planned (needs environment) |
| T-19 | **No binding writes from M2:** a session spy and a static check show no M2 module writes the binding store, and no write, replace or unbind API exists in M2 | FQ-1 (c), FQ-3; RD-M2-07 | Planned |
| T-20 | **No BAR writes from M2:** BAR counts unchanged; no BAR service write method is called; no identifier is issued | K-2; D2, D5 | Planned |
| T-21 | **No discovery:** an unknown reference is never resolved through import or scanning; realization comes only from explicit construction | K-3, K-10; `ADR-042 §4.3` | Planned |

**Mapping of the §13.6 coverage list:**

| Coverage item | Tests |
|---|---|
| `BindingSource` behaviour | T-11 |
| Missing binding | T-11 |
| Invalid or unregistered identifier | T-12 |
| `REALIZATION_UNAVAILABLE` | T-13 |
| Shared reference | T-14 |
| Start-up fail-closed | T-15 |
| Read-only role | T-17 |
| PostgreSQL | T-18 |
| Two organizations | T-7 |
| No binding writes | T-19 |
| No BAR writes | T-20 |
| No discovery | T-5, T-21 |
| M2/M5 boundary | T-4, T-9 |

### 13.7 Regression baselines

**Historical only, not to be reused:** BAE 93; AuthorizationEngine 106; AuthService BAR A–C + WP-13 subset 33; AuthService full 972 (2026-09-25). These predate `355ebbe`, `203bed1`, `b0f5a12` and later commits.

**Fresh measurement is required**, both before M2 implementation starts (the pre-change baseline) and at M2 acceptance. Each measurement uses `Backend/Services/AuthService/venv/Scripts/python.exe -m pytest`:

| Suite | Path | Notes |
|---|---|---|
| BAE full | `Backend/Runtime/BusinessActivityEngine/tests/` | Not run by CI; measured locally |
| AuthorizationEngine full | `Backend/Runtime/AuthorizationEngine/tests/` | Unchanged by M2 |
| AuthService BAR A–C | `tests/test_bar_identifier_service.py`, `test_bar_registration_service.py`, `test_bar_transaction_safety.py` | Must stay green and unchanged |
| AuthService full | `Backend/Services/AuthService/tests/` | Needs `JWT_SECRET_KEY` and `JWT_ALGORITHM=HS256` set (TD-010). This mirrors `.github/workflows/authservice-ci.yml`'s `pytest tests/` job |
| PostgreSQL evidence | T-6, T-11, T-15, T-16 on PostgreSQL/asyncpg | TD-176. The CI bootstrap job has a `postgres:16` service, but the test job runs on SQLite. The venue must be fixed at authorization |

The frontend is untouched, so no frontend build is required. Every count is recorded as measured, never copied.

### 13.8 Forbidden scope / explicit exclusions

**M2-P is outside the M2 implementation and commit boundary.** M2 must not:
- create a binding table or a binding migration, or **any** table or migration;
- write, replace or unbind binding rows (FQ-3);
- expose an HTTP or runtime binding-write path (FQ-1 (c));
- perform a runtime authority check for binding creation (FQ-1 (c));
- add an actor or approver field (IP-3), or host, tenant or lifecycle columns (OQ-1, OQ-2, FO-3 §4);
- make `implementation_reference` UNIQUE (FQ-4);
- read BAR across services outside `RO-M1-11` (FQ-5);
- write BAR registration, change BAR schema, service or repository code, register a Business Activity, or issue or assign an identifier (K-2);
- populate `BAR-INDEX.md`;
- use dynamic import, filesystem, module, decorator or route scanning, or import-time registration (K-3, K-10);
- cache or snapshot bindings (OQ-3) unless separately authorized;
- invoke the opaque handle, or define an invocation signature or transaction semantics (M5);
- do Workstream D or E; M3, M4 or M6 work;
- bind a real capability activity;
- modify a router, capability service or AuthorizationEngine file;
- modify an existing AuthService module other than the RD-M2-05-approved start-up wiring point;
- implement any TD-171 work;
- provision infrastructure (RD-M2-08);
- use `git add -A` / `git add .`; push.

### 13.9 Stop conditions (implementation halts and reports)

Retained:
- any need to change BAR;
- any field or datum not listed in §4 D, §6 or FO-3 §4;
- a binding form other than B2;
- a need to invoke an implementation or fix its signature;
- a regression failure;
- any M3 to M6 dependency surfacing;
- any conflict with `ADR-042`, `ADR-043`, D2, D5 or D8.

B2-specific:
- M2 begins writing the binding store, or its scope expands into M2-P;
- M2 creates a BAR identity or writes BAR registration;
- a runtime binding-authority check is introduced;
- FQ-7 role separation proves infeasible (record the constraint; never weaken it);
- a second binding row becomes possible for one identifier, or `implementation_reference` becomes UNIQUE;
- a cross-service BAR read appears without `RO-M1-11`;
- dynamic import or discovery appears;
- reconciliation cannot distinguish a missing binding from a missing realization, or start-up does not fail closed per identifier;
- the PostgreSQL evidence TD-176 requires is absent at acceptance;
- the TD-171 boundary is violated (M2 treats TD-171 as resolved, or implements its enforcement);
- M2 invokes the resolved implementation;
- the start-up wiring point needs an AuthService change RD-M2-05 did not approve;
- M2-P's store does not offer what the read-only adapter needs;
- any undocumented governance decision becomes necessary.

### 13.10 Independent review and release-readiness gates

This sequence is defined here; it is **not authorized** by this document.

**M2-P gates first.** M2-P has its **own** `§19` checklist, implementation authorization and `§19.7` gate, including independent review. M2 does not consume M2-P's physical store until that gate passes. M2-P acceptance is not M2 acceptance, and the reverse also holds.

**M2 gates, in order:**
1. Implementation is completed within the authorized M2 scope (§13.2, §13.4).
2. The M2 targeted tests (§13.6) pass.
3. The full regression suites (§13.7) pass, with fresh counts recorded.
4. PostgreSQL verification (T-18, TD-176) passes. T-17 passes, or is recorded as outstanding infrastructure evidence under RD-M2-08.
5. A **fresh-context independent reviewer** examines the implementation. The reviewer re-runs the suites and performs from-scratch probes with negative controls (§19.7, §19.7b).
6. All Critical, High and Medium findings are resolved, or explicitly governed (`§19.8.5`). Any remediation is independently verified.
7. A release-readiness audit covers git status, commit scope and governance-document accuracy.
8. Repository Owner acceptance.
9. M2 closure, only after the authorized gates. The Work Package–level five-gate closure remains at M7.

### 13.11 Commit boundary

- **A. M2-P:** its own implementation and governance commits, under its own authorized scope. Never combined with M2.
- **B. M2:** after Repository Owner acceptance of M2, one M2 commit containing only the §13.4 A files and the WP-BAE-001 hunks of shared governance files.
  - no M2-P schema or migration files;
  - no infrastructure provisioning;
  - no BAR A–C changes;
  - no TD-171 implementation.
- **C. Governance:** only when explicitly authorized.
- **Throughout:** exact-path staging only (never `git add -A` / `git add .`). No push without the Repository Owner's separate instruction and the §19.7b gates the RO requires.

---

## 14. Repository Owner Decisions Required

| ID | Decision | Options | Recommendation |
|---|---|---|---|
| **RD-M2-01** | BAR A–C dependency state (B-1) | (a) Close WP-23 A–C first: commit, then the independent verification WP-23's own Charter §16 requires, then M2. (b) Authorize M2 against uncommitted BAR, with an M2 commit that may only follow a WP-23 A–C commit. (c) Other | **(a).** M2 should consume a verified, committed surface. Also authorize a narrow correction of the "delivered/certified" statements (Charter §9 line 131 and §10 M2; `IRA-BAE-001` line 69; `WPR-001` WP-BAE-001 Dependencies cell) |
| **RD-M2-02** | Binding form and location (B-2, §7) | M-A governed manifest artifact; M-B explicit composition-root binding; M-C BAE-owned table | **M-B**, with an explicit RO ruling that a code-reviewed composition binding satisfies `ADR-042 §4.3`'s "governed" contract. If the RO holds that a governed *document* is required, M-A needs an `IMP-001` CBAM amendment and ADR first, and M2 stays blocked until then |
| **RD-M2-03** | (a) `§6.16.5` scope; (b) tenant placement | (a) Verify Identifier + registration only and report the other four as NOT VERIFIED with debt recorded; or require sources first (blocks M2). (b) Confirm §12 | (a) Verify minimum and disclose, per `RO-M1-05` ("minimum authoritative contract"). (b) Confirm |
| **RD-M2-04** | Workstream E relationship | (a) The BAE's host adapter over `get_by_identifier` is the runtime *consumption* of BAR's registration state; Workstream E keeps the BAR-side gate mechanism and may later supply a gate interface the adapter switches to; the WP-23 Charter is unchanged. (b) Build Workstream E first | **(a).** Consistent with `RO-M1-04` (the BAE consumes and enforces; it does not re-implement). The adapter holds no gate policy of its own |
| **RD-M2-05** | Host integration in M2 | (a) Authorize a new, additive `AuthService/bae_integration/` package (adapter + BAE import path, TD-165 interim) with no other AuthService change. (b) Formal packaging (`pyproject.toml`) for both Runtime packages. (c) Defer the host adapter to M7 and deliver only BAE-side M2 | **(a)**, with (b) left as TD-165's long-term resolution. (c) would leave M2's "real query against BAR" objective unmet |
| **RD-M2-06** | Implementation reference vs invocation contract | (a) M2 binds and returns an opaque implementation reference, never invoked; M5 defines the invocation signature. (b) M2 defines the signature now | **(a).** (b) depends on M3 context and M5 execution semantics |

**No decision above is assumed by this document.** Each recommendation is a recommendation only.

*(Updated 2026-09-25.)* The Repository Owner's decisions on the six items are recorded in §0. The table above is preserved as the analysis presented for decision. Where §0 differs from a recommendation here, §0 governs; in particular, RD-M2-02 was **not** selected and remains OPEN.

---

## 15. Readiness Statement

*(Updated 2026-09-25, following the §0 decisions.)* **M2 remains NOT implementation-ready, NOT AUTHORIZED and NOT STARTED.** Two things remain before implementation authorization can be requested:
1. the RD-M2-01 prerequisite: WP-23 A–C closure, verification and statement reconciliation;
2. an RD-M2-02 decision.

*(Reconciliation, 2026-09-28.)* Both items listed above are now resolved:
1. the RD-M2-01 prerequisite is **satisfied** (§0, §13.1): WP-23 A–C were accepted, committed and independently verified; WP-23 is not certified or closed and remains OPEN;
2. RD-M2-02 is **decided**: Option B2, `ADR-043`.

**M2 remains NOT AUTHORIZED and NOT STARTED, and is not implementation-ready.** Remaining prerequisites before any M2 authorization request include:
- **FO-2:** the M2 detailed design must be redone for B2 (`ADR-043 §9`); ~~*(2026-09-28: prepared in §16, pending RO approval. The full list of remaining prerequisites is in §16.K.)*~~ *(2026-09-28: **FO-2 design approved** (§16.L). FO-2 design approval is **not** M2 implementation authorization. Remaining prerequisites (~~FO-1,~~ FO-3, TD-171, the §13 regeneration and the explicit M2 authorization) are in §16.K. FO-1: the Master Technical Architecture was amended (AMD-017, 2026-09-28).)* *(2026-09-29: FO-3 is DESIGN APPROVED / NOT IMPLEMENTED (`e7c713b`). RD-M2-07/08 are decided (§0). M2-P implementation, infrastructure, TD-171, TD-176, the TD-170 commit, RD-M2-05/TD-165, the §13 regeneration and the M2 authorization remain outstanding; see §16.K.)*
- **TD-171:** act-to-row enforcement must exist before `bar_registration` decides execution eligibility (`ROD-BAE-001-M2 §0.5`).

The original statement follows, unchanged.

**M2 is NOT implementation-ready.**
- The runtime contract (§11), outcome model (§5), BAR field usage (§4 D), test strategy (§13.6) and file scope (§13.4) are designed. They are ready to execute once RD-M2-01 to RD-M2-06 are decided and M2 is explicitly authorized.
- **No BAR schema or contract change is required.** Existing BAR data is sufficient for registration verification. The missing data belongs on the manifest side and is excluded from BAR by D2/D6.
- **Implementation mapping is not resolved.** Ownership is decided (`RO-M1-03`); form and location are not (B-2, RD-M2-02).
- **M2 does not depend on M3–M6 work**, provided RD-M2-06 is decided as (a).

**Integrity:**
- No code, test, migration, schema, API, route, manifest, binding or BAR artifact was created or modified.
- No Business Activity was registered, and no identifier was assigned.
- No Charter, ADR, `IMP-001`, `RTA-001`, WP-23 or TECH-DEBT entry was changed.
- The stale statements found (§3.1) are recorded, not corrected.
- Nothing was staged, committed or pushed.

---

## 16. FO-2 — M2 Redesign for Option B2 (2026-09-28)

**Prepared** by Repository Owner instruction: "Proceed with FO-2 — M2 redesign for B2, DESIGN ONLY." This is the follow-on `ADR-043 §9` FO-2 requires.

**Status:** ~~**DESIGN PREPARED — PENDING REPOSITORY OWNER APPROVAL.**~~ *(Updated 2026-09-28, §16.L.)* **FO-2 DESIGN APPROVED** (OQ-1 to OQ-4 decided by the RO). **M2 remains NOT AUTHORIZED and NOT STARTED.** ~~FO-1,~~ FO-3, TD-171, the §13 regeneration and the M2 authorization remain outstanding (§16.K). *(2026-09-28: FO-1 architecture amended, AMD-017 in the Master Technical Architecture v7.4; §16.K.)* *(2026-09-29: FO-3 DESIGN APPROVED / NOT IMPLEMENTED, `e7c713b`. RD-M2-07/08 decided; §16.K.)*
- It supersedes, for B2, the M-B design in §7 (binding options), §11 (execution contract), §13.2 (scope) and §13.4 (file list). Those sections are preserved as the analysis at 2026-09-25.
- The §5 outcome model, §6 per-datum analysis and §12 tenant placement **still apply**, extended here.
- Every design choice below is `[DESIGN — pending approval]` unless it restates a decided source.
- No code, table, schema, migration, adapter, test or binding row is created.

**Governing sources, re-read for this section:**
- `ADR-043` (B2, §4.1 to §4.4, §9);
- `ADR-042 §4.3`;
- `ROD-BAE-001-M2 …` (K-1 to K-11, §0.2 to §0.6);
- this document's §0 (RD-M2-01 to 06);
- `IMP-001 §6.15.4` ("Activity Resolution — Locate the Business Activity implementation") and `§6.16.5` ("resolve … using the Business Activity Registry … Activities that cannot be resolved shall terminate before execution begins");
- the committed M1 ports (`Backend/Runtime/BusinessActivityEngine/business_activity_engine/ports.py`: `RegistrationSource.is_registered -> bool`, the content-free `ManifestResolver`/`ManifestResolution`);
- `identity.py` (`BA-\d{6}` shape validation at construction);
- the committed BAR read surface (`BarRegistrationRepository.get_by_identifier`, `b0f5a12`);
- `ROD-WP-23-AC …` §0 (RD-23-03);
- `TECH-DEBT.md` TD-170, TD-171 and TD-176.

### 16.A M2 responsibility boundary under B2

| M2 will | M2 will not |
|---|---|
| Resolve a validated `BA-NNNNNN` identifier to a `ResolvedBusinessActivity` in stage 2 (`ACTIVITY_RESOLUTION`) and hand it to stage 3 | Invoke, import or execute the implementation (RD-M2-06; M5) |
| Consume BAR registration state read-only, through a host adapter (RD-M2-04) | Write, change or re-define BAR registration or identifiers (K-2); implement the Workstream E gate |
| Consume the **governed binding** read-only, through a host adapter (`ADR-043 §4.1`) | Create, change or retire bindings; define the governed write path (that is the FO-1/FO-3 and binding-governance design, §16.C) |
| Look the implementation reference up in a host-supplied, immutable **realization** (§16.D) | Discover implementations: no dynamic import, scanning, decorators, route inspection or naming heuristics (K-3/K-10) |
| Verify only the identifier and registration status of `§6.16.5` and report the other four data as NOT VERIFIED (RD-M2-03, TD-170) | Invent sources for version, invocation method, domain or platform version |
| Produce stage outcomes and discriminators (§16.I) | Define the canonical `§6.28` error taxonomy (M6) or any HTTP/API behaviour (none exists for the BAE) |
| Resolve identically for any organization (RD-M2-03, K-9) | Take organization or claims into the BAR or binding lookups |

### 16.B Resolution flow (stage 2, replacing the §11 M-B flow)

```
BusinessActivityInvocation (identifier already a validated BusinessActivityIdentifier — M1)
  ▼ Stage 2  ACTIVITY_RESOLUTION
  │  2a Identity         identifier from the invoker; never derived (§4 B)
  │  2b BAR registration  RegistrationSource.lookup(identifier)            ── host adapter → BAR (bar_registration, read-only)
  │                       authority: BAR (D2/D5).  NOT registered → stop (ACTIVITY_NOT_REGISTERED)
  │  2c Governed binding  BindingSource.lookup(identifier)                 ── host adapter → the host's binding table (read-only)
  │                       authority: governed binding (ADR-043).  no binding → stop (ACTIVITY_NOT_RESOLVED)
  │  2d Binding validation record identifier == requested; implementation reference present and well-formed
  │  2e Realization       Realization.get(implementation_reference)        ── immutable, host-constructed, BAE-owned type
  │                       authority: none — subordinate; must conform to 2c
  │  2f Result            ResolvedBusinessActivity(identifier, registration record, binding record, opaque implementation handle)
  ▼ Stage 3  EXECUTION_CONTEXT_INITIALIZATION (receives ResolvedBusinessActivity; M1 subset; M3)
  ▼ Stage 4  AUTHORIZATION_EVALUATION (unchanged)
  ▼ Stage 5+ NOT_IMPLEMENTED — the implementation handle is never invoked in M2
```

**Two authorities, kept separate:**
- **BAR registration (2b)** answers "is this canonical Business Activity registered?"
- **The governed binding (2c)** answers "which implementation is it bound to?"

A binding never implies registration: 2b always runs first, and a binding for an unregistered identifier is inert. Registration never implies a binding: 2c must independently find one. Neither authority reads or writes the other's store.

**Query count.** This supersedes §4 C's "exactly one read-only query per invocation". Under B2 there are two read-only queries per invocation, one registration and one binding, and neither writes.

### 16.C Governed binding model — conceptual contract (FO-3 fixes the physical form)

`[DESIGN — pending approval]`. This is a minimum contract. No physical schema is created, and FO-1/FO-3 remain outstanding.

| Element | Required? | Meaning and basis |
|---|---|---|
| **Business Activity Identifier** | **Yes** | The `BA-NNNNNN` value. It keys the binding and must equal the BAR-issued identifier. **At most one current binding per identifier per hosting service** (uniqueness), so that resolution is deterministic (`ADR-043 §4.4`) |
| **Implementation reference** | **Yes** | The opaque, non-empty value `ADR-043 §4.2` defines. Never interpreted as a module path or import target (K-3/K-10). Its physical form belongs to FO-3 |
| **Governing act** | **Yes** | A citation of the governance act that created or last changed the binding. `ADR-043 §4.1` makes binding changes governance acts; this mirrors `bar_registration.registering_act`. It gives traceability, not verification (see the TD-171 analogue below) |
| **Bound-at timestamp** | **Yes** | When the binding was recorded. Audit traceability, mirroring `bar_registration.registered_at` |
| Hosting service | **Not a required column** | K-7 / `ADR-043 §4.4` put one table in each hosting service, so the host is implied by where the table lives. An explicit value would be needed only if bindings were ever consolidated across hosts (`RO-M1-11`, deferred). ~~**Open question OQ-1**~~ **OQ-1 DECIDED (2026-09-28, §16.L): no explicit hosting-service value;** the host is implied by the table's location |
| Binding status / lifecycle | **Not in the minimum** | A row present means bound, mirroring BAR's D2 two-state model. No version, suspension or retirement state is introduced: `§6.22.9`/`§6.23.8` have no source, per TD-170, and none is invented. "Invalid or unsupported state" in §16.I therefore means a malformed record, not a lifecycle value. ~~**Open question OQ-2:** whether the RO wants an explicit unbinding or retirement semantic~~ **OQ-2 DECIDED (2026-09-28, §16.L): no unbinding or retirement lifecycle in M2;** present = bound. A future lifecycle needs a separate governed decision |
| Effective/current semantics | Implied | Uniqueness makes the single row *the* current binding. There are no effective-dating or version columns (see OQ-2) |
| Tenant column | **None** | The binding is platform-global (K-9; `ADR-043 §4.4`). `CLAUDE.md §21.4` must be re-checked if a write endpoint is ever added |
| FK to `bar_registration` | **No** `[DESIGN — pending approval]` | A non-AuthService host cannot hold one, because BAR lives in AuthService's database (`RO-M1-11`). The authorities also stay separate: registration is checked at run time in 2b, not by a constraint. Integrity for the binding table's own fields (non-null, uniqueness) is expected to be enforced by the database |

**Integrity expectations.**
- The identifier is well-formed (`BA-\d{6}`), one row per identifier, and the implementation reference is non-empty.
- **Writes only through a governed write path** citing a governance act (`ADR-043 §4.1`, `§7`). That write path, its authorization and its act-to-row enforcement are **not designed here**; they belong with FO-1/FO-3.
- **TD-171 analogue.** Without act-to-row enforcement, a binding row would carry the same fail-open governance risk TD-171 records for `bar_registration`. This redesign **records** that risk as a requirement on the future write-path design. It does **not** resolve it, and it does **not** absorb TD-171 (§16.H).

### 16.D Code-side realization (subordinate)

`[DESIGN — pending approval]`.
- **Shape.** An immutable mapping from **implementation reference → implementation object**, constructed explicitly in the hosting service's composition root. It is passed into the BAE as a BAE-owned, content-free type, the same construction discipline §7 described for M-B.
- **The key is the implementation reference, not the BAR identifier.** Code therefore never asserts which Business Activity it implements, and the BAR identifier appears in code nowhere as an independent authority.
- **Subordination.** A realization entry is never proof of a binding, because stage 2 reaches the realization only through a governed binding (2c → 2e). A realization entry no binding points to is inert. When the realization and the governed binding differ, the governed binding wins, and the mismatch is a failure (§16.I), never a fallback.
- **Construction is fail-fast:** duplicate references, an empty reference, or a missing implementation object all make construction fail (`ROD-BAE-001-M2 §6` disciplines).
- **Prohibited:**
  - dynamic import or `importlib`-style resolution of the stored reference;
  - filesystem, module, decorator or route scanning;
  - import-time self-registration;
  - naming-convention or runtime guessing;
  - a BAR identifier held in code as an independent source of authority;
  - realization content overriding, or standing in for, the governed binding;
  - any default, fallback or prefix-matched entry.
- **Opacity (RD-M2-06).** The implementation object's type is unconstrained in M2. M2 validates only that an entry exists for the reference, and never inspects or calls it.

### 16.E Host-side adapter

`[DESIGN — pending approval]`. The integration boundary is under RD-M2-05, selected in principle: `Backend/Services/AuthService/bae_integration/`.
- **Responsibility.** Implement two BAE-owned ports read-only against the hosting service's own session:
  - **`RegistrationSource`**, over `BarRegistrationRepository.get_by_identifier`, extended from the M1 `bool` port to a typed lookup (§5);
  - **`BindingSource`** (new port), over the host's governed binding table.
- **Boundary.** The adapter translates host persistence into BAE port results, and nothing else:
  - no writes, flushes or commits;
  - ~~no caching policy unless a refresh rule is approved (**OQ-3**, `ADR-043 §4.4`);~~ **no caching in M2** (OQ-3 DECIDED, 2026-09-28, §16.L). `BindingSource` reads the governed binding directly; any future cache or refresh mechanism must be separately designed and governed (`ADR-043 §4.4`);
  - no organization or claims input;
  - no fallback between the two sources.
- **Failure translation.** Session or database failures are **raised**, never converted into "not registered" or "no binding". The BAE maps them to `*_SOURCE_UNAVAILABLE` (§16.I).
- **The BAE core stays persistence-free** (K-10): the core imports no adapter, repository or table. Hosts inject the adapters.
- **Per host** (K-7): each hosting service provides its own `BindingSource` over its own table. A non-AuthService host's `RegistrationSource` depends on the deferred `RO-M1-11`.

### 16.F Reconciliation (designed, not implemented)

`[DESIGN — pending approval]`. Reconciliation compares, per hosting service, the set of implementation references in that host's governed binding table with the set of keys in that host's realization.

| State | Meaning | Expected treatment |
|---|---|---|
| **Aligned** | Every bound reference has a realization entry, and every realization entry is referenced by at least one binding | Valid |
| **Binding without realization** | A governed binding points to a reference the host's code does not realize (deployment drift, or a binding recorded before the code shipped) | **Reconciliation failure.** At run time, resolution of that identifier fails closed: `EXECUTION_FAILED` / `REALIZATION_UNAVAILABLE` (§16.I) |
| **Realization without binding** | Code realizes a reference no governed binding uses | **Reported orphan.** It has no runtime effect (unreachable, §16.D) and is not treated as a binding |
| **Both exist but disagree** | Under reference-keyed realization, this can only be (i) a realization entry whose declared reference differs from its key, or (ii) a binding row inconsistent with the requested identifier | (i) rejected at realization construction (fail-fast); (ii) `MALFORMED_BINDING_RESPONSE` at run time (§16.I). A realization/implementation *contract* mismatch is an M5 concern (§16.G) |

**Where it runs.** ~~The check point is **open question OQ-4:** a pre-deployment/CI consistency check, a host start-up check, or both.~~ **OQ-4 DECIDED (2026-09-28, §16.L): both.** The check is designed for (1) pre-deployment/CI validation and (2) host start-up validation. It fails closed and never invokes a Business Activity. The ROD's B-with-realization framing calls for "a mandatory consistency test" (`ROD-BAE-001-M2 §4`). Nothing is implemented.

**Relation to BAR reconciliation.** This reconciles *binding ↔ realization*. It is not the RD-23-03 *registering act ↔ `bar_registration` ↔ `BAR-INDEX.md`* reconciliation, which remains TD-171.

### 16.G M2 / M5 boundary (RD-M2-06, preserved)

- **M2** establishes resolution and binding semantics. It returns an **opaque implementation handle** inside `ResolvedBusinessActivity` and **never invokes it**. A spy-based test is still required (§13.6 T-4).
- **Deferred to M5:**
  - the implementation's invocation signature and contract;
  - validating that a realized object satisfies that contract;
  - Business Rule Execution;
  - transaction semantics (`IMP-001 §6.19`).
- **Also deferred:** full context construction (M3); activity-scoped authorization policy (M4); the canonical error taxonomy (M6).

### 16.H BAR execution-gate boundary (RD-M2-04, preserved) and TD-171

- **Workstream E** remains the BAR-side execution-gate authority. The BAE *consumes* registration state (2b) and holds no gate policy of its own (RD-M2-04). The implementation binding (2c–2e) is a BAE-side resolution concern, distinct from BAR execution eligibility.
- **TD-171 is not absorbed and not resolved by this redesign.** Stage 2b makes a registration-based stop decision, so an implemented M2 would use `bar_registration` to decide whether a Business Activity proceeds. That is exactly the use TD-171's hard condition prohibits until act-to-row enforcement exists (`ROD-BAE-001-M2 §0.5`).
- **TD-171 therefore remains a prerequisite to any M2 implementation authorization** (§16.K). The Repository Owner must either close it or explicitly decide how M2 may proceed while it is open. This design does neither.

### 16.I Failure and denial semantics

`[DESIGN — pending approval]`. This extends §5. The outcomes are stage-level. There is no HTTP or API behaviour, because none exists for the BAE; mapping to transport errors is the invoker adapter's concern (M7) and the `§6.28` taxonomy's (M6). Raw exception text is not copied into `reason` (TD-169).

| Case | Detected at | Stage 2 result | `ExecutionOutcome` / discriminator |
|---|---|---|---|
| Malformed identifier (not `BA-\d{6}`) | M1 identifier construction | never reaches the engine | construction error (M1, unchanged) |
| **Unknown BAR identifier** (well-formed, never issued) | 2b: no `bar_registration` row | TERMINATED | `ACTIVITY_NOT_REGISTERED`. M2 reads registration only, so an unissued identifier and an issued-but-unregistered one are indistinguishable, and need not be told apart (RD-M2-03) |
| **Not registered** | 2b | TERMINATED | `ACTIVITY_NOT_REGISTERED` (existing) |
| Registration source unavailable | 2b raises | TERMINATED | `EXECUTION_FAILED` / `REGISTRATION_SOURCE_UNAVAILABLE` (§5) |
| Malformed registration response | 2b | TERMINATED | `EXECUTION_FAILED` / `MALFORMED_REGISTRATION_RESPONSE` (§5) |
| **Registered, no binding** | 2c: no binding row | TERMINATED | `ACTIVITY_NOT_RESOLVED` (proposed in §5) / `BINDING_ABSENT`. A governance state, not a platform fault |
| Binding source unavailable | 2c raises | TERMINATED | `EXECUTION_FAILED` / `BINDING_SOURCE_UNAVAILABLE` |
| **Conflicting / invalid binding** (identifier ≠ requested, empty or malformed reference, more than one current row) | 2d | TERMINATED | `EXECUTION_FAILED` / `MALFORMED_BINDING_RESPONSE` |
| **Binding with unavailable realization** (including a *stale* binding whose reference the code no longer realizes) | 2e | TERMINATED | `EXECUTION_FAILED` / `REALIZATION_UNAVAILABLE`. A reconciliation failure, §16.F |
| Unsupported binding state | 2d | TERMINATED | Under the minimum model there is no state column (§16.C), so any unrecognized record shape is `MALFORMED_BINDING_RESPONSE`. ~~OQ-2 governs any future state~~ OQ-2 is decided (§16.L): no lifecycle in M2, and any future state needs a separate governed decision |
| Resolved | 2f | COMPLETED → stage 3 | — (M2 never yields overall `COMPLETED`) |

**Rules:**
- Every non-resolved path **terminates before execution begins** (`IMP-001 §6.16.5`).
- No path fabricates a resolution, falls back to another binding or reference, or treats a realization entry as a binding.

### 16.J Governance and traceability

| Source | How this redesign conforms |
|---|---|
| RD-M2-01 | Satisfied (§0). It depends on WP-23 A–C as committed (`b0f5a12`) |
| RD-M2-02 / `ADR-043` | B2 applied: the governed binding is authoritative (16.C), realization is subordinate (16.D), reconciliation is designed (16.F), and the implementation reference is opaque (16.D, 16.G) |
| RD-M2-03 | Only the identifier and registration status are verified; the other four data are NOT VERIFIED (TD-170); organization-independent (16.A, 16.E) |
| RD-M2-04 | BAE consumes registration state; Workstream E is untouched (16.H) |
| RD-M2-05 | Additive `bae_integration/` host boundary (16.E). Detailed design only; no implementation authorized |
| RD-M2-06 | Reference only; invocation deferred to M5 (16.G) |
| `ADR-042 §4.3` | BAE owns resolution; prohibited discovery mechanisms respected (16.D) |
| `IMP-001 §6.15.4` / `§6.16.5` | "Locate the Business Activity implementation … using the Business Activity Registry"; unresolved activities terminate before execution (16.B, 16.I). `§6.17` to `§6.19` (context, authorization integration, transactions) are untouched by M2 (16.G) |
| WP-23 A–C | Read-only consumer of `get_by_identifier`. No BAR code, schema or `BAR-INDEX.md` change (K-2) |
| FO-1 / FO-3 | The physical table, its Master Technical Architecture record and the physical reference form remain outstanding. 16.C is conceptual only. *(2026-09-29: FO-1 is done, `867af46`. FO-3 is design-approved and not implemented, `e7c713b`. Its physical implementation is owned by M2-P (RD-M2-07))* |
| TD-171 | Recorded as a prerequisite and as an analogue risk for the binding write path; not resolved (16.C, 16.H) |
| TD-176 | PostgreSQL/asyncpg verification applies equally to the binding table and adapter. Carried to the §13.10 verification plan |

### 16.K Readiness impact

**What FO-2 now resolves (as a design, ~~pending RO approval~~ *approved 2026-09-28, §16.L*):**
- the B2-consistent M2 responsibility boundary;
- the two-authority resolution flow;
- the minimum conceptual binding contract;
- the reference-keyed, subordinate realization;
- the host-adapter boundary;
- the reconciliation states;
- the failure semantics.

These replace the M-B design in §7, §11, §13.2 and §13.4.

**What remains unresolved:**
- ~~**OQ-1:** whether the binding carries an explicit hosting-service value.~~ **DECIDED** (§16.L): no explicit value.
- ~~**OQ-2:** any binding lifecycle beyond present-equals-bound.~~ **DECIDED** (§16.L): none in M2.
- ~~**OQ-3:** the adapter refresh or caching rule (`ADR-043 §4.4` "needs a defined refresh rule").~~ **DECIDED** (§16.L): no caching in M2.
- ~~**OQ-4:** where reconciliation runs.~~ **DECIDED** (§16.L): both pre-deployment/CI and host start-up.
- ~~**FO-1:** the Master Technical Architecture amendment.~~ **Amended 2026-09-28:** AMD-017, `Master_Technical_Architecture.md` v7.4, PART K ADDENDUM (architectural record only; the physical form is FO-3).
- **FO-3:** the physical binding schema and implementation-reference form, plus the governed write path and its authorization.
- **TD-171:** open, with its hard condition.
- **TD-170:** the four unverifiable `§6.16.5` data.
- **TD-176:** PostgreSQL verification.
- **`RO-M1-11`:** cross-service BAR access for non-AuthService hosts.
- A revised §13 checklist (files, tests, stop conditions) regenerated for B2 once 16.A to 16.I are approved.

**Why this is not M2 authorization.** FO-2 is a design artifact prepared on instruction. It creates nothing executable and changes no decision. `WP-BAE-001` Charter §17 requires an explicit Repository Owner act naming the M2 scope, and §13.1 keeps that box unticked.

**Prerequisites before an M2 implementation authorization request can be considered:**
1. ~~RO approval of this FO-2 design (16.A to 16.I), with answers to OQ-1 to OQ-4.~~ **DONE (2026-09-28, §16.L):** OQ-1 to OQ-4 decided; FO-2 design approved. This is not M2 authorization.
2. ~~FO-1: an approved Master Technical Architecture amendment for the binding table.~~ **DONE (2026-09-28):** FO-1 architecture amended (AMD-017, MTA v7.4). This records the concept only; the physical table is FO-3.
3. FO-3: the approved physical binding contract and implementation-reference form, including the governed write path and its authorization.
4. **TD-171** closed, or an explicit RO decision on how M2 may consume `bar_registration` while TD-171 is open.
5. A §13 implementation-start checklist regenerated for B2: files, tests (including FK/constraint-enforced and PostgreSQL-verification items, TD-176) and stop conditions.
6. The explicit M2 implementation authorization naming its scope (Charter §17).

**M2 remains NOT AUTHORIZED and NOT STARTED.** WP-23 remains OPEN (A–C accepted and committed; D–H not implemented). TD-171 remains OPEN.

*(Readiness reassessment, 2026-09-28, after §16.L.)* **FO-2 design approved ≠ M2 implementation authorized.**

| # | Prerequisite before an M2 implementation authorization request | State |
|---|---|---|
| 1 | FO-2 design approved, with OQ-1 to OQ-4 answered | **DONE** (§16.L) |
| 2 | FO-1: Master Technical Architecture amendment for the binding table | ~~**OUTSTANDING** (not authorized)~~ **DONE 2026-09-28**: architecture amended, design prerequisite satisfied (AMD-017, `Master_Technical_Architecture.md` v7.4, PART K ADDENDUM). Architectural record only; ~~not committed yet~~ *committed `867af46` (2026-09-29 reconciliation)* |
| 3 | FO-3: physical binding contract and implementation-reference form, governed write path and its authorization, and act-to-row enforcement for bindings | ~~**OUTSTANDING** (not authorized)~~ **DESIGN APPROVED / NOT IMPLEMENTED** (2026-09-29, `e7c713b`; FQ-1 to FQ-8 decided; IP-3 resolved). Physical implementation is owned by M2-P (row 7) |
| 4 | TD-171 closed, or an explicit RO decision on how M2 may consume `bar_registration` while it is open | **OUTSTANDING**; TD-171 **OPEN** |
| 5 | §13 implementation-start checklist regenerated for B2 (files, tests including FK/constraint-enforced and PostgreSQL items, TD-176, and stop conditions), now reflecting OQ-1 to OQ-4: no host column, no lifecycle, no cache, and reconciliation in CI and at host start-up | **OUTSTANDING**. *(2026-09-29: the **next governance task**, after RD-M2-07/08 and before M2 authorization.)* |
| 6 | Explicit M2 implementation authorization naming its scope (Charter §17) | **OUTSTANDING** |
| 7 | *(Added 2026-09-29.)* RD-M2-07: ownership of the B2 binding infrastructure | **DECIDED** (Option B). **M2-P** owns C1 to C3; M2 owns C5 and C7. **M2-P implementation: NOT AUTHORIZED / NOT STARTED**, and it must pass its own `§19.7` gate before M2 |
| 8 | *(Added 2026-09-29.)* RD-M2-08: infrastructure prerequisites | **DECIDED** (Option (a)). The infrastructure itself remains **OUTSTANDING**: FQ-6 target-store access and FQ-7 role provisioning must exist before the first governed binding write against a deployed environment. FQ-7 is not weakened |
| 9 | *(Added 2026-09-29.)* TD-176: PostgreSQL verification before the first execution-eligibility consumer | **OUTSTANDING** |
| 10 | *(Added 2026-09-29.)* TD-170: register entry committed | **OUTSTANDING** (present only in the uncommitted working tree) |
| 11 | *(Added 2026-09-29.)* RD-M2-05 detailed design and the TD-165 packaging choice | **OUTSTANDING**; a governance decision is required |

TD-170 (the four unverifiable `§6.16.5` data), TD-176 (PostgreSQL verification) and `RO-M1-11` (cross-service BAR access) remain open matters carried into prerequisites 3 and 5.

**Integrity (§16):**
- No code, model, migration, schema, table, adapter, realization, test or binding row was created.
- No BAR or BAE file was modified.
- TD-170 and TD-171 are unchanged.
- ADR-042, ADR-043, the ROD, `IMP-001`, `RTA-001` and the Master Technical Architecture are unchanged.
- Nothing was staged, committed or pushed.

### 16.L Repository Owner Decision Record — OQ-1 to OQ-4 (2026-09-28)

**Recorded** by direct Repository Owner instruction ("Record the following Repository Owner (RO) decisions for OQ-1 through OQ-4 in the existing FO-2 governance artifact"). Each decision is recorded as stated and is not reinterpreted.

| OQ | Decision | Rationale (as recorded by the RO) | Affected §16 design |
|---|---|---|---|
| **OQ-1** — Hosting service | **DECIDED: no explicit hosting-service value.** The governed binding table is host-specific, and the hosting service is implied by the table's physical location. No hosting-service column is added to the conceptual B2 binding contract | Consistent with `ADR-043 §4.4`. One binding table per hosting service is the governed model. It avoids redundant host identity. Cross-host consolidation stays outside M2 and would need a separate governed decision | §16.C "Hosting service" row |
| **OQ-2** — Binding lifecycle | **DECIDED: no explicit unbinding or retirement lifecycle in M2.** For M2, a row present means bound. No status or lifecycle column, and no unbinding semantic, is introduced. Any lifecycle beyond present-equals-bound needs a separate governed decision | It keeps M2's binding contract minimal, preserves the two-state model in §16, and does not prevent a future governed lifecycle decision | §16.C "Binding status / lifecycle" and "Effective/current semantics"; §16.I "Unsupported binding state" |
| **OQ-3** — Adapter refresh/caching | **DECIDED: no caching in M2.** `BindingSource` reads the governed binding directly. No cache or refresh mechanism is part of M2. Any future caching or refresh requirement must be separately designed and governed before implementation | It preserves the authoritative governed database binding, avoids a second state or stale binding source, and is consistent with `ADR-043 §4.4`'s requirement that any refresh rule be explicitly defined | §16.E host-side adapter |
| **OQ-4** — Reconciliation location | **DECIDED: both.** The binding-to-realization consistency check is designed for (1) pre-deployment/CI validation **and** (2) host start-up validation | CI catches governed-binding/code-realization mismatches before deployment. Host start-up is a runtime safety check against an inconsistent deployed state. The check fails closed and does not invoke Business Activities. It satisfies the ROD's requirement for "a mandatory consistency test" (`ROD-BAE-001-M2 §4`) and preserves the M2/M5 boundary | §16.F reconciliation |

**Effect on FO-2.**
- OQ-1 to OQ-4 are resolved, and the corresponding §16 design choices are approved.
- §16.K prerequisite 1 required "RO approval of this FO-2 design (16.A to 16.I), with answers to OQ-1 to OQ-4". On the basis of this instruction, which describes the result as "FO-2 design approved", **the FO-2 design (16.A to 16.I, as decided here) is recorded as APPROVED.** The status is therefore **FO-2 DESIGN APPROVED**.

**FO-2 design approval is not M2 implementation authorization.** These decisions do **not**:
- authorize FO-3;
- authorize FO-1 implementation;
- close TD-171;
- authorize M2;
- create any runtime implementation.

**M2 remains NOT AUTHORIZED and NOT STARTED.**

*End of IRA-BAE-001-M2.*
