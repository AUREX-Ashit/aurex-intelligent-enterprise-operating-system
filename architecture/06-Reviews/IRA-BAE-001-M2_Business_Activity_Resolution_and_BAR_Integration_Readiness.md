# IRA-BAE-001-M2 — Business Activity Engine: Business Activity Resolution & BAR Integration — Readiness Assessment and Design

**Work Package:** `WP-BAE-001` (Business Activity Engine), milestone **M2 — Business Activity Resolution & BAR Integration**
**Prepared:** 2026-09-25, per direct Repository Owner instruction ("prepare M2 properly so that implementation can begin once the Repository Owner authorizes it"). Design / readiness only.
**Status:** ~~**READINESS ASSESSMENT — NOT IMPLEMENTATION-READY.** One blocking dependency finding (§3.1) and six Repository Owner decisions (§14) must be resolved before M2 code.~~ *(Updated 2026-09-25 — Repository Owner decision pass, §0.)* **READINESS ASSESSMENT — NOT IMPLEMENTATION-READY.**
- Decided: RD-M2-01, RD-M2-03, RD-M2-04 and RD-M2-06; RD-M2-05 is decided in principle.
- ~~**RD-M2-02 remains OPEN**; see `ROD-BAE-001-M2-Identifier-Implementation-Binding-Decision-Preparation.md`.~~ *(Updated 2026-09-28.)* **RD-M2-02 decided: Option B2** (governed persistent binding registry), recorded in `ADR-043` and `ROD-BAE-001-M2 …` §0.6. M2 remains **NOT AUTHORIZED**.
- M2 is blocked until WP-23 Workstreams A–C are closed and independently verified (RD-M2-01), and until RD-M2-02 is decided.
- **M2 remains NOT AUTHORIZED and NOT STARTED.**
**Baseline:** M1 ACCEPTED — COMPLETE (`94c99a1`; roadmap `ddf4869`). Governance prerequisites `aa263bc`.

**This document creates nothing executable.** No code, test, migration, schema, API, route, manifest, binding, BAR change, Business Activity registration, or identifier assignment. It amends no Charter, ADR, `IMP-001`, `RTA-001`, WP-23 artifact, or BAR artifact. Where a design choice is proposed it is marked `[DESIGN — pending approval]`; where a choice belongs to the Repository Owner it is listed in §14 and not assumed.

---

## 0. Repository Owner Decision Record — M2 Readiness Decisions

**Recorded:** 2026-09-25, by direct Repository Owner instruction ("GOVERNANCE/READINESS DECISION PASS ONLY"), responding to §14 of this document. Each decision is recorded as stated and is not reinterpreted. The instruction reaffirms: **M2 remains NOT AUTHORIZED and NOT STARTED; do not implement M2.**

| ID | Repository Owner decision (as recorded) | Status after this revision |
|---|---|---|
| **RD-M2-01** WP-23 A–C prerequisite | **SELECTED.** WP-23 BAR Workstreams A–C must be formally closed/committed and independently verified **before M2 implementation begins**. Stale governance statements that describe BAR A–C as already "delivered", "certified" or equivalent must be reconciled against the actual repository state, **without silently rewriting history**. WP-23 A–C remains a separate Work Package and governance boundary. **M2 does not absorb WP-23.** | **RESOLVED** (decision). The prerequisite is **OPEN**: the closure-readiness assessment and stale-statement inventory are in `IRA-WP-23-AC_BAR_Workstreams_A-C_Closure_Readiness.md`. No statement was corrected in this pass |
| **RD-M2-02** Identifier → implementation binding | **NOT SELECTED — OPEN.** A focused architectural decision package is required, because the proposed host start-up binding table would establish the authoritative runtime mapping between the canonical identifier and executable implementation; it is not an implementation detail. The package must compare at least: A. host-service start-up binding table; B. governed persistent/documented binding registry; C. any other repository-supported mechanism, if evidence exists. **No option is selected; none is implemented.** | ~~**OPEN — RO decision required.**~~ **DECIDED 2026-09-28 — Option B2**: a governed database table holds the authoritative binding; the code-side realization is subordinate; reconciliation is required (`ADR-043`; `ROD-BAE-001-M2 …` §0.6). Prepared in `ROD-BAE-001-M2-Identifier-Implementation-Binding-Decision-Preparation.md`. The §7 "M-B recommended" wording above is superseded as a recommendation: it is retained as the analysis at that date, not as a pending selection. *(2026-09-28: B2 corresponds most closely to this document's §7 **M-C** ("BAE-owned persistent binding table"), which §7 assessed as not recommended; that assessment is retained as historical analysis. The §7 and §13.2–§13.4 M-B design text (composition-root binding, `binding.py`, "no table, no migration") does not reflect the decided form and must be redone for B2 (`ADR-043 §6`, FO-2) before any M2 implementation authorization.)* |
| **RD-M2-03** `§6.16.5` verification scope | **SELECTED.** M2 verifies only (1) the canonical Business Activity identifier and (2) BAR registration status. The other four `§6.16.5` checks (Activity Version, Supported Invocation Method, Business Domain, Required Platform Version) remain explicitly **NOT VERIFIED — NO AUTHORITATIVE SOURCE**. No source is invented. The gap is recorded as technical debt. **M2 resolution must be organization-independent**, and tests must show that two unrelated Organizations do not produce different Business Activity resolution merely because of tenant context. | **RESOLVED.** Gap recorded as `TD-170`. "Activity Status" is verified only in D2's two-state form (registered or not), as §6 records; `§6.22.9`'s "Only Active" check stays unverifiable and is included in `TD-170` |
| **RD-M2-04** WP-23 Workstream E relationship | **SELECTED.** The BAE consumes BAR registration state. WP-23 Workstream E remains the BAR-side execution-gate authority. The BAE must not duplicate or redefine Workstream E. The WP-23 Charter is **not** modified by this decision. | **RESOLVED** |
| **RD-M2-05** Host integration | **SELECTED IN PRINCIPLE.** M2 may use an additive AuthService integration boundary, proposed as `Backend/Services/AuthService/bae_integration/`, subject to the detailed M2 implementation design. **This does not authorize implementation.** No unrelated AuthService refactoring is authorized. | **RESOLVED IN PRINCIPLE**; detailed design and implementation authorization pending |
| **RD-M2-06** Reference vs invocation | **SELECTED.** M2 resolves an **opaque implementation reference** and does **not** invoke it. The invocation contract is deferred to the later milestone the governing WP-BAE-001 design identifies, currently **M5**. No invocation signature is introduced in M2 for convenience. | **RESOLVED** |

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

**C. Exact BAR lookup required.**
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

## 13. `CLAUDE.md §19` M2 Implementation-Start Checklist

**Status: PREPARED — NOT APPROVED. M2 implementation is NOT AUTHORIZED.** No code may be written until every box in 13.1 is ticked by a Repository Owner act.

### 13.1 Preconditions (all required)
- [x] **RD-M2-01** BAR A–C dependency state decided (§3.1). *(Decided 2026-09-25, §0.)*
- [ ] **RD-M2-01 prerequisite met:** WP-23 Workstreams A–C closed, committed and independently verified; stale statements reconciled (`IRA-WP-23-AC_…_Closure_Readiness.md`).
- [x] **RD-M2-02** Binding form and location decided (§7). ~~**OPEN.**~~ *(Decided 2026-09-28: Option B2, `ADR-043`. The M2 detailed design must be redone for B2; see §0.)*
- [x] **RD-M2-03** Per-datum verification scope and tenant placement decided (§6, §12). *(Decided 2026-09-25, §0; `TD-170`.)*
- [x] **RD-M2-04** Workstream E relationship decided (§8). *(Decided 2026-09-25, §0.)*
- [ ] **RD-M2-05** Host integration and packaging (TD-165) scope decided (§10). *(Decided in principle 2026-09-25, §0; detailed design pending.)*
- [x] **RD-M2-06** Implementation-reference vs invocation-contract split decided (§7). *(Decided 2026-09-25, §0.)*
- [ ] Explicit Repository Owner **M2 implementation authorization**, naming its scope (Charter §17).

### 13.2 Authorized scope (proposed, if §14 recommendations are adopted)
The M2 subset of the Charter §10 M2 objective:
- the typed read-only BAR registration consumption;
- the five-way outcome discrimination (§5);
- the explicit, content-free BAE resolver (M-B) and the minimum manifest identity;
- the stage 2 → stage 3 hand-off of `ResolvedBusinessActivity`;
- the AuthService host adapter over `get_by_identifier`;
- the BAE import path for AuthService (TD-165);
- tests and documentation.

### 13.3 Governing documents
The sources in §1 (Charter §10 M2; ADR-042 `RO-M1-01`–`03`; `IRA-BAE-001-M1` §0, §9, §15; `IMP-001 §6.16.5`, `§6.22.7`–`§6.22.8`, `§6.29.6`; `RTA-001 §6.6`–`§6.7`; D2, D5, D8), plus this document and the recorded §14 decisions.

### 13.4 Files expected to change (under the §14 recommendations; any deviation is a STOP)

| File | Change |
|---|---|
| `Backend/Runtime/BusinessActivityEngine/business_activity_engine/ports.py` | Typed `RegistrationLookup`; `RegistrationSource.lookup`; `ManifestResolutionStatus.UNRESOLVED`; `ResolvedBusinessActivity`; resolver content |
| `…/business_activity_engine/binding.py` *(new)* | Content-free, explicitly constructed, immutable binding resolver (M-B); fail-fast construction |
| `…/business_activity_engine/engine.py` | Stage 2 outcomes per §11; hand-off to stage 3; no stage-4+ change |
| `…/business_activity_engine/results.py` | `ACTIVITY_NOT_RESOLVED`; stage discriminator field (interim, not `§6.28`) |
| `…/business_activity_engine/__init__.py`, `README.md` | Exports; M2 contract |
| `…/tests/test_engine.py`, `test_contracts.py`, `test_package_boundary.py`, `test_resolution.py` *(new)* | See 13.6 |
| `Backend/Services/AuthService/bae_integration/__init__.py`, `bar_registration_source.py`, `runtime_path.py` *(new, host side)* | Read-only adapter over `get_by_identifier`; BAE import path (TD-165). `authz_integration/runtime_engine_path.py` is **not** modified |
| `Backend/Services/AuthService/tests/test_bae_bar_registration_source.py` *(new)* | Adapter tests |
| `IMP-REPORT-WP-BAE-001`, Charter status lines, `TECH-DEBT.md` (TD-165, TD-167, new source-gap item), `WPR-001` WP-BAE-001 row | Governance synchronization (WP-BAE-001 hunks only) |

**Unchanged (verified at gate):** every BAR A–C file, migration and test; `BAR-INDEX.md`; the WP-23 Charter; `Backend/Runtime/AuthorizationEngine/**`; `authz_integration/**`; every router, capability service and model; `IMP-001`; `RTA-001`; ADR-042.

### 13.5 Dependencies
BAR A–C in a committed, verified state (per RD-M2-01); M1 (committed); AuthorizationEngine (unchanged).

### 13.6 Tests required
Each test must be purpose-built, with negative controls where §19.7b applies.

| ID | Test |
|---|---|
| T-1 | Each of the five §5 cases yields exactly its stage status and outcome; the other stages are `NOT_REACHED` |
| T-2 | Strict typing: a truthy non-lookup, a `REGISTERED` lookup with no record, a record with a mismatched identifier, and `registration_status` ≠ `"REGISTERED"` each fail closed as malformed (extends F-02) |
| T-3 | The resolver: unknown identifier → `UNRESOLVED`; construction rejects duplicates, mismatched identity and missing implementation; the mapping is immutable after construction; same input → same output |
| T-4 | The implementation reference is **never invoked** in M2 (a spy implementation records zero calls on every path) |
| T-5 | Boundary: the core still imports no `sqlalchemy`, BAR, `importlib`, `pkgutil`, `os`, `glob` or `sys`; the binding module has no decorator or registry-global state; the host adapter calls only `get_by_identifier` |
| T-6 | Host adapter, against a real session in the AuthService harness with FK enforcement confirmed (§19.7b parity): a seeded registration → `REGISTERED` with the exact record; absent → `NOT_REGISTERED`; session or DB failure → raises → `REGISTRATION_SOURCE_UNAVAILABLE`; **read-only proof** (`count_registered` and ledger count unchanged; no flush or commit issued) |
| T-7 | Tenant: two unrelated Organizations invoking the same identifier get an identical resolution; the organization and claims are never passed to the BAR query or the binding lookup |
| T-8 | TD-167: a `None` or non-`ManifestResolution` resolver result returns `EXECUTION_FAILED`, never raises |
| T-9 | No path yields `COMPLETED`; the result invariant holds |
| T-10 | Mutation probes: remove the identifier-equality check, the status check and the strict type check in turn; each must be caught (§19.7b method requirement) |

### 13.7 Regression suites (must pass, counts re-measured)
- BAE full suite (baseline 93);
- `Backend/Runtime/AuthorizationEngine` (106);
- AuthService BAR A–C + WP-13 (33);
- AuthService full suite (972);
- the frontend is untouched, so no frontend build is required.

### 13.8 Forbidden scope
- Any BAR write, schema, service, repository or migration change.
- Registering a BA, or assigning or issuing an identifier.
- Populating `BAR-INDEX.md`.
- Workstream D or E.
- M3 context construction, M4 authorization changes, M5 execution or transactions, M6 errors, state or observability.
- Invoking an implementation.
- Creating a first consumer or binding any real capability activity.
- Modifying any router, capability service or AuthorizationEngine file.
- Filesystem, decorator, route or import-time discovery.
- A new table or migration.
- `git add -A` / `git add .`; push.

### 13.9 Stop conditions (implementation halts and reports)
- Any need to change BAR.
- Any field or datum not listed in §4 D or §6.
- A binding form other than the decided one.
- A need to invoke an implementation or to fix its signature.
- A need to modify an existing AuthService module beyond adding the new `bae_integration` package.
- A regression failure.
- Any M3–M6 dependency surfacing.
- Any conflict with ADR-042, D2, D5 or D8.

### 13.10 Independent review
- On completion, M2 is submitted to a **fresh-context independent reviewer** (§19.7). The reviewer re-runs the suites and performs from-scratch probes per §19.7b.
- Any remediation is independently verified before acceptance, as done for M1.
- The Work Package-level five-gate closure remains at WP closure (M7).

### 13.11 Commit and push boundary
- Nothing is committed before RO acceptance of M2.
- Then one M2 commit, staging only the 13.4 files and the WP-BAE-001 hunks of shared governance files.
- No push without the RO's separate instruction and the §19.7b gates the RO requires.

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

*End of IRA-BAE-001-M2.*
