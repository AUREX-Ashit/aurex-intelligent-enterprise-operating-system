# WP-21 — BA-01 (C-022 Customer & Account Management) — Establish Commercial Account — Business Activity Charter

**Work Package:** WP-21 — ~~the next unclaimed Work Package number, verified directly this pass against `WPR-001` (highest row: `WP-20`, C-021, FORMALLY CLOSED — CERTIFIED — RELEASE-READY) and `WP-REG-001` (highest registered row: `WP-16`); no `WP-21` row, reference, or reservation exists anywhere in `WPR-001`, `WP-REG-001`, or any other governance register checked this session. This Charter claims the number for its own self-identification only — it does not add a row to `WPR-001`, `WP-REG-001`, or `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md`; that registration remains a separate, subsequent act, not performed here.~~ *(Superseded 2026-09-15 — WP-21 has since been formally registered in `WPR-001` (row added, per its own §3 Maintenance Rule condition (b)) and in `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md` (C-022 row updated), per direct Repository Owner instruction ("Proceed with the next C-022 governance actions... WP REGISTRATION"). `WP-REG-001` was re-checked at that pass and found not updated for `WP-16` through `WP-20` either — consistent with that unbroken four-Work-Package precedent, `WP-REG-001` is not updated for `WP-21`, disclosed rather than silently skipped. `WPR-001` remains the operative registry.)*

**Business Activity:** BA-01 — Establish Commercial Account

**Capability:** C-022 Customer & Account Management (`CAP-001` line 76, Domain D-002 Commercial & Subscription, owning specification `COM-001` §7 — LOCKED under EARB Constitutional Recertification CR-3.0; Enterprise Experience Specification `PE-001-C022` v1.2, Active)

**Status:** ~~**CHARTERED.** Implementation is **NOT** authorized by this document. CBOR registration is **NOT** performed by this document (`ADR-039` remains preparation-only). BAR registration is **NOT** performed and is deferred (`ROD-C022-B` D10). No WP registration, no schema, no migration, no code, no test.~~ *(Superseded 2026-09-15 — see the "Implementation Authorization" section below.)* **CHARTERED — CBOR REGISTERED (`ADR-040` — Business Object `CAC-000001`; `CBOR-INDEX.md` §3 row added) — BAR REGISTRATION DEFERRED BY REPOSITORY OWNER DECISION (`ROD-C022-B` D10, Option A) — WP REGISTERED (`WPR-001` row added) — IMPLEMENTATION AUTHORIZED (Repository Owner, 2026-09-15).** Implementation itself has **NOT** begun under this same instruction — no schema, migration, model, repository, service, router, frontend, or test exists as of this recording.

**Prepared under:** direct Repository Owner instruction ("AUREX — C-022 — PREPARE C-022 CHARTER FOR BA-01"), 2026-09-15, following `ROD-C022`, `ROD-C022-A`, `ROD-C022-B` (D9 = Option A, D10 = Option A, both recorded 2026-09-15), `ADR-038` (Accepted, Option A), `ADR-039` (CBOR registration preparation), `IRA-C022`, `TDS-C022` (including the `[C-3]`/`[C-4]`/`[C-5]` remediation pass), and the independent review `IRA-TDS-C022_Independent_Review.md` (Gate: PASS WITH CONDITIONS, all seven conditions now resolved or deferred by explicit RO decision — §22 below).

**A note on document type, disclosed rather than assumed (mirrors `WP-15`/`WP-16`/`WP-17`/`WP-19`/`WP-20 BA-01`'s own identical disclosure):** this repository's established convention charters at the Work Package level, with per-Business-Activity charter detail specified inside the governing IRA/TDS. `WP-14 BA-04` onward established a Business-Activity-level charter as repeated repository precedent. This document follows that shape.

**Governing basis for BA-01, stated explicitly:** `CAP-001` (C-022 registration, line 76) → `COM-001` §4/§7 (`COM-001-001`/`-002`/`-003`/`-005`/`-030`…`-036`/`-060`/`-061` — LOCKED) → `PE-001-C022` v1.2 (Enterprise Experience Specification — Active) → `ROD-C022-Customer-and-Account-Management-Capability-Boundary-and-Minimum-Scope.md` (D1–D6) → `IRA-C022-Customer-and-Account-Management.md` (🟢 GREEN-leaning readiness) → `TDS-C022_Customer_and_Account_Management_Minimum_BA_Technical_Design.md` (prepared, independently reviewed, `[C-3]`/`[C-4]`/`[C-5]` remediated) → independent gate (`IRA-TDS-C022_Independent_Review.md`, PASS WITH CONDITIONS) → `ROD-C022-A` (D7 classification, D8 read/list) → `ADR-038` (classification conflict, Option A) → `ADR-039` (CBOR registration preparation) → `ROD-C022-B` (D9 lifecycle-pattern, D10 BAR) → this charter.

---

## Classification Key

Mirrors `WP-20 BA-01`'s own key:
- **A** — already determined by governing documents
- **B** — determined by repository precedent
- **C** — a design specification, not yet built (no implementation exists)
- **D → RESOLVED** — was open, now resolved by a recorded decision (`ROD-C022-A` D7/D8, `ROD-C022-B` D9/D10, `ADR-038`)

---

## 1. Business Activity Identity — [A]

BA-01, WP-21, Capability C-022 Customer & Account Management (`CAP-001` D-002, Active). Governed physical Business Object (once implemented — no implementation exists yet): a new C-022-owned **Commercial Account** record (conceptual table `c022_commercial_account`, `TDS-C022 §6.1`), the enterprise's Authoritative Commercial Account Context for exactly one standalone account. **Eligible for `CMD-001 §26.3a` CBOR registration** — Step 1 (Independent Identity) + Step 2 (Cross-Experience Reference — `COM-001-036` names C-020/C-021/C-023/C-024/C-025 as consumers by identity) + Step 3 (Governed Lifecycle) all satisfied (`IRA-C022 §11`, `ADR-039 §3`). **Registration preparation only recorded via `ADR-039`; no Business Object Identifier is assigned and `CBOR-INDEX.md` is not amended.** Write path — establishes exactly one active Commercial Account per call, with a system-assigned Account Reference. No edit, delete, state transition, read, or list is designed (`TDS-C022 §2`/`§15`; `ROD-C022-A` D8).

## 2. Business Intent (Scope) — [A]

Verbatim basis, `CAP-001` line 76: *"Manage customer relationships."* BA-01 realizes only a narrow slice of that broader capability intent, per `ROD-C022` D1/D5: a persisted, **platform-global** Commercial Account record supporting **establish only**. BA-01 does not manage a "customer relationship" in any general sense — Customer establishment and the Customer–Account Relationship are both explicitly out of scope (§20) — it produces exactly one authoritative commercial-container fact (`COM-001-033`) that a later C-022 increment, and downstream capabilities (`COM-001-036`), may build upon.

**Scope, stated explicitly:**
- **In scope:** establish one Authoritative Commercial Account (system-assigned, stable Account Reference in `PREFIX-NNNNNN` form per `COM-001-001`, inherited by Section 7; canonical `account_name`; status defaulted to `active`; hierarchy column declared but always `NULL`); platform-global scope; `AuthService` hosting; `require_platform_admin`-gated.
- **Out of scope:** see §20.

## 3. Trigger — [A]

Caller-invoked. A `PLATFORM_ADMIN` acts directly against C-022's own host (`AuthService`) — `POST /commercial-accounts` (`TDS-C022 §15`). There is **no cross-service write path, no write-fan-in, and no event-bus trigger** — the Commercial Account is established by a single, direct, authenticated administrative action.

## 4. Actor / Persona — [A]

`PLATFORM_ADMIN` for the establish operation, per `ROD-C022 §H`/D5 and the `C-003`/`C-021` platform-global precedent (`TDS-C022 §12`, independently confirmed genuine — not merely asserted — by `IRA-TDS-C022_Independent_Review.md §5.5`: `require_platform_admin` exists at `dependencies.py:46`, and the design is an exact, additive match to the certified `/roles`/`/offerings` exemption pattern). No dedicated "Account Steward" or equivalent narrative persona is named in `COM-001` or `PE-001-C022`'s scope for BA-01; none is invented here.

## 5. Preconditions — [A]

- An authenticated caller holding the `PLATFORM_ADMIN` role (`dependencies.require_platform_admin`, live, unchanged).
- **No** precondition requires an Organization, a `Membership`, an `X-Tenant-ID` header, a Customer, a Customer–Account Relationship, a Subscription, an Entitlement, or any event/broker infrastructure — none is used or designed for this increment (`ROD-C022` D1/D2/D3/D5; `TDS-C022 §2`/§5).

## 6. Input Contract — [C, not yet built]

`EstablishCommercialAccountRequest` (design only, `TDS-C022 §8`): `account_name` (str, required, non-blank). `id`, `account_reference`, `status`, `parent_account_id`, `created_by_actor_id` are **never caller-supplied** — the system assigns them (`TDS-C022 §8`, mirroring `c021_offering_definition`'s own "caller cannot override" pattern).

## 7. Business Rules — [A]

- `account_name`: required, non-blank; no uniqueness invariant (`COM-001-033` states none; `TDS-C022 §6.1`/§8).
- `status` is one of the closed set `{active, suspended, retired}` (`[INFERENCE]`, `TDS-C022 §6.1`, supported by `EX-C022-05`/`EX-C022-06`'s Account-inclusive retire/reactivate triggers, not verbatim `COM-001-033` text). **BA-01 writes and only ever writes `'active'`** — no transition endpoint exists (`ROD-C022 §H`; `TDS-C022 §9`).
- `account_reference` **SHALL** be of the form `PREFIX-NNNNNN`, per `COM-001-001` (Universal Identity, Section 4), **inherited in full by Section 7** per `COM-001` line 44's own inheritance clause. This is a corrected position: `TDS-C022 §7`'s original reasoning (declining the format on the premise that Section 7 does not "repeat" `COM-001-001` the way other sections do) was independently found factually defective (`IRA-TDS-C022_Independent_Review.md §5.3`/§9, `[C-3]`) — verified directly that no Section 5–9 construct ever repeats `COM-001-001`'s clause (it appears exactly once, in Section 4), and that `TDS-C021 §9.3`'s own precedent (`OFFERING_REFERENCE_PREFIX = "OFFERING"`, shipped in `c021_offering_definition.py`) confirms the format is inherited, not exempted, by non-repetition. `account_reference` is `UNIQUE`, system-assigned; only the concrete allocation **mechanism** remains `[IMPLEMENTATION-TIME]` (`TDS-C022 §7`).
- `parent_account_id` is declared in the schema (`COM-001-033`'s hierarchy-position fact) but **never written non-NULL by BA-01** — no relate/transfer/counterparty concept exists at this scope (`TDS-C022 §10`).
- **No `classification` attribute exists anywhere in BA-01's data model or business rules** — see §18 below; this is settled, not open.

## 8. Data Model (Conceptual — Not Yet Implemented) — [C]

`[DESIGN, TDS-C022 §6.1]` Conceptual table `c022_commercial_account` — **no migration, model, or table currently exists.**

| Field | Conceptual type | Null? | Notes |
|---|---|---|---|
| `id` | UUID, PK | NOT NULL | Record identity. |
| `account_reference` | String(30), UNIQUE | NOT NULL | `PREFIX-NNNNNN`, system-assigned (§7 above). |
| `account_name` | String(255) | NOT NULL | Minimum canonical identity (`COM-001-033`). |
| `status` | String(20), CHECK `{active,suspended,retired}`, default `'active'` | NOT NULL | BA-01 writes only `'active'`. |
| `parent_account_id` | UUID, FK self-referential | NULLABLE | Declared, never exercised by BA-01. |
| `created_by_actor_id` | UUID (not FK) | NOT NULL | Audit citation of the `PLATFORM_ADMIN` caller. |
| `created_at` / `updated_at` | `DateTime(timezone=True)` | NOT NULL / NULLABLE | Standard platform timestamps. |

**No `organization_id` column** (D2, platform-global). **No `classification` column** (§18). Ownership: `AuthService` exclusively; no other service reads or writes this table.

## 9. Service/Module Placement (Design Only) — [C]

`Backend/Services/AuthService/` — `models/c022_commercial_account.py`, `repositories/c022_commercial_account_repository.py`, `services/commercial_account_service.py`, `routers/commercial_account.py`, `schemas/commercial_account.py` — naming mirrors `c021_offering_definition`'s own file layout (`TDS-C022 §13`). No new service (`ROD-C022` D3).

## 10. API Contract (Design Only) — [C]

`POST /commercial-accounts` — `Depends(require_platform_admin)`. Request: `{account_name: str}` only. Response: 201, the persisted row (`id`, `account_reference`, `account_name`, `status="active"`, `parent_account_id=null`, `created_at`). **No other route is designed** — `ROD-C022 §H` names only "establish"; `ROD-C022-A` D8 confirms this remains establish-only (`TDS-C022 §15`).

## 11. Authorization and Tenant-Middleware Treatment — [A]

Every BA-01 route is gated by the existing `Depends(require_platform_admin)` dependency — the certified `C-003`/`C-021` pattern, not the tenant-scoped gate (`ROD-C022` D3/D5). `middleware/tenant.py`'s exemption list gains one new prefix pair (`/commercial-accounts`, `/commercial-accounts/`) on the same `/roles`/`/offerings` basis (`TDS-C022 §12`).

## 12. Scope / Platform-Global Behavior — [A]

`ROD-C022` D2: platform-global. No `organization_id` column (§8). `CLAUDE.md §21.4`'s Mandatory Tenant-Isolation Test Checklist is structurally not applicable, identical treatment to `C-021`'s D8 (`TDS-C022 §11`). Substitute assurance: (a) non-`PLATFORM_ADMIN` denied; (b) `PLATFORM_ADMIN` succeeds; (c) live table introspection + ORM metadata confirming no `organization_id`/`tenant*` column.

## 13. Account Hierarchy Handling — [A]

Hierarchy is declared in the schema (`parent_account_id`) but **NOT exercised by BA-01** — every BA-01-established row has `parent_account_id = NULL`. No relate/transfer/counterparty concept exists at this scope (`ROD-C022 §H`; `TDS-C022 §10`).

## 14. Account Status Semantics — [A]

BA-01 writes exactly one status value, `'active'`, at establish time, and exposes no mechanism to change it. The closed set `{active, suspended, retired}` is declared for constitutional-model correctness, not because BA-01 exercises suspend/retire (`TDS-C022 §9`).

## 15. Commercial Account Classification — Settled, Not Open — [D → RESOLVED, `ADR-038`, `ROD-C022-A` D7]

`ADR-038` (Accepted, Option A, 2026-09-15): **the Authoritative Commercial Account Context does NOT carry a "classification" attribute.** This resolves the genuine `CLAUDE.md §16` conflict independently identified between LOCKED `COM-001-033` (silent on Account classification) and Active `PE-001-C022` (affirmative on Account classification in four places — `EX-C022-04`, `C022-O02`, `§1.4` Scope, the Guiding Architectural Question). `ROD-C022-A §B.2` D7 independently confirms Option A. **No `classification` column exists in §8's schema, and none may be added by any future implementation session without a fresh, express Repository Owner decision superseding `ADR-038`.** The underlying `COM-001-033` ↔ `PE-001-C022` conflict itself remains logged as a separate, later architecture-governance correction item — not reopened, not resolved, by this Charter.

## 16. Lifecycle-Pattern Realization — Settled, Not Open — [D → RESOLVED, `ROD-C022-B` D9, Option A]

`COM-001-002` (Anchor/Authoritative/Resulting) and `COM-001-003` (Intent Precedes Proposal), both LOCKED and inherited in full by Section 7, distinguish Anchor, Intent, Proposed, Assessment, and Authoritative/Resulting as roles that must never be conflated. `TDS-C022 §15`'s single-call `POST /commercial-accounts` design realizes none of Anchor, Intent, Proposed, or Assessment as separately observable constructs — disclosed explicitly, not silently, at `TDS-C022 §15.1` (remediation of independent-review finding `[C-5]`, `IRA-TDS-C022_Independent_Review.md §5.6`).

**`ROD-C022-B` D9 (recorded 2026-09-15): Option A — ACCEPT COLLAPSED MINIMUM SLICE.** The single-call establish design is accepted for BA-01. Anchor, Intent, Proposed, and Assessment **remain conceptually distinct architectural roles** per `COM-001-002`/`COM-001-003` — this decision does not dissolve or redefine those roles; it holds only that BA-01 may realize all of them internally within one externally invoked establish flow, with no separate externally observable API required for each stage at this minimum scope. This decision was made explicitly for C-022 on its own governing text, informed by (but not automatically granted by) the certified `c021_offering_definition` precedent. `TDS-C022 §15.1` remains exactly as designed; no TDS redesign is required. `TDS-C022 §21` item 5 is resolved by this decision.

## 17. CBOR Registration Status — Settled Eligibility, Registration Executed — [D → RESOLVED]

**Eligibility (`CMD-001 §26.3a`):** re-verified directly (`ADR-039 §3`) — Step 1 (Independent Identity) satisfied via the persisted Account Reference; Step 2 (Cross-Experience Reference) satisfied via `COM-001-036`'s naming of C-020/C-021/C-023/C-024/C-025 as consumers by identity; Step 3 (Governed Lifecycle) satisfied via `COM-001-033`'s status attribute and `PE-001-C022`'s full lifecycle. **Eligible.**

~~**Registration:** `ADR-039_Commercial_Account_Canonical_Business_Object_Registration_Preparation.md` (Status: PROPOSED — REGISTRATION PREPARATION ONLY) already performs this eligibility analysis and assembles the `CMD-001 §26.4` registration content ahead of implementation, but **does not assign a Business Object Identifier and does not amend `CBOR-INDEX.md`.** `ADR-039 §8`/`§10` recommends (Option B) that actual registration be deferred until Charter/Implementation Authorization exists, mirroring `ADR-037`'s own executed precedent for `OFR-000001` exactly.

**This Charter does not perform CBOR registration and does not assign a Business Object Identifier.** Per `COM-001-005` (registration precedes implementation), **actual CBOR registration remains a mandatory prerequisite before implementation authorization, not before this Charter.** The Repository Owner's own next-step sequencing (`ROD-C022-B §E`) places CBOR registration at step 3, alongside Charter/Implementation Authorization — i.e., a distinct, subsequent act to this Charter, not performed here.~~

*(Superseded 2026-09-15 — per direct Repository Owner instruction bundling CBOR registration with WP registration and Implementation Authorization, actual registration has since been performed.)* **Registration executed:** `ADR-040_Commercial_Account_Canonical_Business_Object_Registration.md` (Accepted) assigns Business Object Identifier **`CAC-000001`** and amends `CBOR-INDEX.md §3` (new row added), adopting `ADR-039`'s own eligibility analysis and registration content by reference rather than re-deriving it. `ADR-039` itself is **unmodified** — it remains the historical preparation record; `ADR-040` is the execution record. The Physical Implementation Mapping (`CMD-001 §26.7`) remains **explicitly conceptual/planned** in `ADR-040`'s own registration table — no implementation exists yet, and that row will require a follow-up correction once it does, exactly as `ADR-039` originally anticipated. No classification, lifecycle expansion, or cross-capability semantic was introduced by this registration — `ADR-040`'s content is a verbatim adoption of `ADR-039 §4`'s own already-reviewed table, plus the now-assigned identifier.

## 18. BAR Treatment — Settled, Deferred — [D → RESOLVED, `ROD-C022-B` D10, Option A]

`COM-001-060` (LOCKED) names "establish" among the actions requiring Business Activity Registry (BAR) registration "once implemented," per `IMP-001 §6.22`. **No physical BAR mechanism exists anywhere in this repository** — confirmed directly (no `BAR-INDEX` or equivalent file exists); `ADR-037 §Decision item 5` independently confirms the same absence held for WP-17 (C-023) and WP-19 (C-132) as well.

**`ROD-C022-B` D10 (recorded 2026-09-15): Option A — DEFER BAR MECHANISM.** No BAR registry, `BAR-INDEX`, database, or runtime mechanism is created by C-022. **No Business Activity Identifier is assigned** — `IMP-001 §6.22.1b`'s `PREFIX-NNNNNN` format governs a future assignment, not a present one; there is no registry to assign into. BA-01 may proceed toward implementation without BAR registration, consistent with `COM-001-005`'s own execution-gate (not implementation-gate) wording for BAR. The `COM-001-060` execution-time obligation remains **deferred**, pending a future enterprise-level BAR-mechanism decision — mirroring `ADR-037`'s disposition for C-021, made here as C-022's own fresh, explicit decision rather than an assumed carry-forward. This does not reopen `COM-001`, does not redesign the Business Activity Registry, and does not establish C-022 ownership of any future BAR mechanism.

## 19. Testing Implications (Design Only, `TDS-C022 §20`) — [C]

Minimum test set, mirroring `test_offering_definition.py`'s own structure: establish happy path + persistence; `account_reference` is system-assigned, unique, `PREFIX-NNNNNN`-conformant; caller cannot override `account_reference`/`id`/`status`/`parent_account_id`; blank `account_name` → 422; non-`PLATFORM_ADMIN` → 403; no-role → 403; missing/malformed `Authorization` → 400; schema assertion (no `organization_id`, no `classification`, live introspection + ORM metadata); establish emits a SUCCESS audit record; a purpose-built end-to-end establish probe (`CLAUDE.md §19.7b` method note). Exact test count and naming remain `[IMPLEMENTATION-TIME]`.

## 20. Out-of-Scope Boundaries — [A]

Consolidated from `ROD-C022 §H` (restated, not reinterpreted):
- Customer establishment of any kind.
- Customer–Account Relationship establishment (`COM-001-034` requires an existing Customer Anchor *and* an existing Commercial Account Anchor — structurally not a first-slice concern).
- Reclassification, retirement, or reactivation of a Commercial Account (no transition endpoint exists — §14).
- Merge, split, or transfer (`ERB-C022-04`, structural/multi-party transitions).
- Any Subscription (C-020), Billing (C-024), Contract (C-025), or Entitlement (C-023) functionality.
- Any CRM/sales-pipeline/case-management/ERP-Customer-Master functionality.
- Any Organization (C-004) equivalence or reference of any kind.
- Tenant isolation of any kind.
- Identity (C-001/URA-001) or Person (C-006) reference wiring.
- Read, list, or retrieval of any established Commercial Account (`ROD-C022-A` D8).
- Any lifecycle policy beyond what `PE-001-C022`/`COM-001 §7` already canonically define — none invented locally.
- Any Commercial Account `classification` attribute (§15).
- CBOR actual registration and Business Object Identifier assignment (§17).
- BAR mechanism creation and Business Activity Identifier assignment (§18).
- **Frontend / Enterprise Experience** — resolved as backend-only, not merely deferred (§21 below — this is the one out-of-scope item this Charter itself resolves, rather than restates from `ROD-C022`).

**This scope SHALL NOT be expanded except by an explicit, separately-recorded Repository Owner decision** (`ROD-C022 §H`).

## 21. Enterprise Experience Scope Decision — `CLAUDE.md §20.3` [D → RESOLVED, determined by this Charter from direct repository evidence, per explicit instruction — not inferred by analogy]

**RESOLVED, Option: Backend-only.**

**Determination:** BA-01 (Establish Commercial Account) **SHALL be chartered backend-only**, the disclosed exception `CLAUDE.md §20.3` permits for "a specific Business Activity within" a Work Package.

**Evidentiary chain supporting this determination (cited, not invented):**

1. `ROD-C022-A §C.2` D8 (already an explicit RO decision, not reopened here): BA-01 is confirmed **establish-only** — no read, no list, no retrieval capability exists or is authorized.
2. `IRA-TDS-C022_Independent_Review.md §7.2` item 3 (independently derived, re-verified directly for this Charter): *"`§20.3` requires, for each Business Activity a Work Package charters, 'Frontend, Navigation, Enterprise Experience' and 'The end-to-end user journey'; `§20.4` requires demonstrability through 'a real persona, using the real frontend'; `§20.6` requires 'a loading state … an empty state' and `IMP-001 §10.3`'s four content-disclosure states (Summary, Details, Evidence, Audit History). **Every one of these presupposes read.** A write-only capability cannot render a Summary, a Details view, an Audit History, or an empty state."* Because BA-01 has no read/list endpoint (item 1) and none is authorized, `§20.3`/`§20.4`/`§20.6`'s demonstrability and content-disclosure-state requirements are **structurally impossible to satisfy** for this Business Activity as currently scoped — there is no established record a frontend screen could ever load, display, or show an empty state for.
3. `IRA-TDS-C022_Independent_Review.md §7.3`'s own determination named exactly two paths to close `[C-2]`: (i) extend `ROD-C022 §H` to authorize read/list, or (ii) confirm establish-only **together with** an explicit `§20.3` backend-only charter determination and a recorded acknowledgement that `COM-001-036` distribution is deferred. `ROD-C022-A` D8 selected path (ii)'s premise (establish-only confirmed, read/list not extended) — making the backend-only determination this Charter now records the **necessary, evidence-compelled companion** to a decision already made, not an independent scope choice invented here.
4. `ROD-C022-A §C.2` itself states, verbatim: *"Any future Charter for C-022 BA-01 MUST include an explicit `CLAUDE.md §20.3` backend-only determination... Without that explicit determination, a Work Package built on an establish-only BA-01 cannot satisfy `§20.3`/`§20.4`/`§20.6`'s demonstrability and content-disclosure-state requirements."* This Charter satisfies that mandatory requirement.

**No frontend/UI implementation is required for WP-21 Independent Certification, V&V Audit, Release Readiness Audit, or closure.** `POST /commercial-accounts` (backend only, once implemented) satisfies BA-01's own Vertical Slice Requirement in full under this Option exception, per `CLAUDE.md §20.3`'s own text.

**Accepted, recorded consequence (per `ROD-C022-A §C.2`, not reopened by this Charter):** `COM-001-036` reference distribution to C-020/C-021/C-023/C-024/C-025 remains unrealizable after the establish call — the Account Reference is available exactly once, in the 201 response body. **C-020 remains blocked** from consuming a genuine, retrievable Commercial Account reference until a later C-022 Business Activity (with read/list) exists. This Charter does not solve that dependency; it only confirms BA-01 alone does not fully discharge it, consistent with `ROD-C022-A`'s own accepted-consequence framing.

**Scope of this decision, stated explicitly:**
- Applies **only** to BA-01/WP-21's own current chartered scope (Establish Commercial Account). It is a scope decision for this Business Activity, not a constitutional prohibition on Enterprise Experience for C-022 generally.
- Does **not** mean C-022 can never have a frontend, or that future Commercial Account screens (a read/list/detail view, once authorized) are foreclosed. A future, separately-chartered Business Activity remains fully possible.
- Does **not** expand BA-01's own scope (§20) — Customer, Relationship, reclassification, merge/split/transfer, and all other exclusions remain in force, unaffected by this decision.
- Does **not** alter `IRA-C022`'s own readiness classification, which this decision neither depends on nor modifies.

## 22. Independent Review Findings and Resolution Status

`IRA-TDS-C022_Independent_Review.md` (Gate: **PASS WITH CONDITIONS**) identified seven conditions. All are now resolved or explicitly, deliberately deferred by recorded Repository Owner decision:

| Finding | Nature | Resolution | Recorded in |
|---|---|---|---|
| `[C-1]` Classification | `[STOP]` — fresh RO decision required | **Resolved, Option A** (no classification attribute) | `ADR-038`, `ROD-C022-A` D7 |
| `[C-2]` Read/list | `[STOP]` — fresh RO decision required | **Resolved, Option A** (establish-only) + `§20.3` backend-only determination | `ROD-C022-A` D8, this Charter §21 |
| `[C-3]` `COM-001-001` inheritance | Mandatory TDS correction | **Corrected** — `PREFIX-NNNNNN` confirmed inherited | `TDS-C022 §7` |
| `[C-4]` Citation misattribution | Mandatory TDS correction | **Corrected** — three misattributions fixed | `TDS-C022 §3/§4/§10` |
| `[C-5]` Lifecycle-pattern conformance | Mandatory disclosure + RO-level scope determination | Disclosed (`TDS-C022 §15.1`); **RO determination: Option A**, collapsed design accepted | `ROD-C022-B` D9, this Charter §16 |
| `[C-6]` CBOR | Carried-forward hard constitutional gate | Eligibility confirmed; **registration preparation complete, actual registration deferred to Charter/Implementation Authorization** | `ADR-039`, this Charter §17 |
| `[C-7]` BAR | Carried-forward hard constitutional gate | **RO decision: Option A**, deferred, no mechanism created | `ROD-C022-B` D10, this Charter §18 |

**No condition was closed by inference or by this Charter's own unilateral authority** — each resolution above traces to an explicit, separately-recorded Repository Owner decision or a directly-verified factual correction, consistent with this repository's no-self-certification and no-silent-resolution discipline throughout the C-022 governance sequence.

## 23. Repository Owner Decisions Recorded (summary)

| Decision | Content | Record |
|---|---|---|
| D1–D6 | Capability boundary, scope model (platform-global), service hosting (`AuthService`), Identity/Person deferral, BA-01 boundary, `IRA-C022` authorization | `ROD-C022` |
| D7 | No Commercial Account classification attribute | `ROD-C022-A`, `ADR-038` |
| D8 | Establish-only; no read/list; accepted consequences | `ROD-C022-A` |
| D9 | Accept collapsed single-call lifecycle realization | `ROD-C022-B` |
| D10 | Defer BAR mechanism; no identifier assigned | `ROD-C022-B` |

This is the complete set of Repository Owner decisions this Charter relies upon; none is reopened, reinterpreted, or expanded here.

## 24. Governing Basis / Traceability

See header. Full evidentiary chain, re-verified directly for this Charter (not assumed from prior summaries): `COM-001-001/-002/-003/-005/-030…036/-060/-061` (LOCKED); `PE-001-C022 §1.14/§1.16`, `EX-C022-04/05/06`, `C022-O02/O05`, `ERB-C022-06` (Active); `CMD-001 §8.10/§26.3a/§26.4/§26.7`; `IMP-001 §6.22/§6.22.1a/§6.22.1b`; `CLAUDE.md §19.3/§19.4/§20.3/§20.4/§20.6/§21.4`; `ADR-037` (C-021 precedent); `ROD-C022`, `ROD-C022-A`, `ROD-C022-B`; `ADR-038`, `ADR-039`; `IRA-C022`; `TDS-C022`; `IRA-TDS-C022_Independent_Review.md`.

## 25. What This Charter (as originally prepared) Did Not Authorize — Now Superseded in Part

~~- Implementation of any kind — no schema, migration, model, repository, service, router, schema module, frontend, or test is created by this Charter.
- CBOR actual registration or Business Object Identifier assignment (`ADR-039` remains preparation-only; `CBOR-INDEX.md` is not amended by this Charter).
- BAR registry creation, Business Activity Identifier assignment, or BAR registration (`ROD-C022-B` D10 remains in force).
- WP registration in `WPR-001`, `WP-REG-001`, or `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md` — this Charter claims the `WP-21` number for self-identification only (header); it does not add a row to any registry.
- Reopening `ROD-C022` D1–D6, `ROD-C022-A` D7–D8, `ROD-C022-B` D9–D10, or `ADR-038`.
- Any expansion of BA-01's own scope beyond §2/§20.
- Implementation Authorization — a Repository Owner act this Charter is a prerequisite to, not a substitute for.~~

*(Superseded 2026-09-15 — CBOR registration, WP registration, and Implementation Authorization have since been performed, as one controlled bundle, per direct Repository Owner instruction. See §25a below for the current, complete list of what remains NOT authorized.)*

## 25a. Implementation Authorization (Recorded 2026-09-15)

**`[RO DECISION]` Implementation of WP-21 / C-022 BA-01 (Establish Commercial Account) is AUTHORIZED**, per direct Repository Owner instruction ("Proceed with the next C-022 governance actions, as one controlled bundle: 1. CBOR REGISTRATION 2. WP REGISTRATION 3. IMPLEMENTATION AUTHORIZATION"), 2026-09-15.

**Authorization is scoped exactly to this Charter's own approved content — §1–§20 — and no further:**
- The single `POST /commercial-accounts` establish endpoint (§10), the conceptual schema of §8 (including the explicit absence of a `classification` column), the `PREFIX-NNNNNN` Account Reference requirement (§7), the declared-but-unexercised hierarchy column (§13), and the `active`-only status write (§14) — exactly as designed in `TDS-C022` and restated in this Charter. **No field, endpoint, or business rule beyond §1–§20 is authorized.**
- **`ROD-C022-B` D9 (Option A — accept the collapsed single-call lifecycle realization) and D10 (Option A — defer BAR mechanism) are explicitly preserved, not reopened, by this authorization.** Anchor/Intent/Proposed/Assessment remain conceptually distinct architectural roles per `COM-001-002`/`COM-001-003` (§16); no BAR registry, mechanism, or Business Activity Identifier is created or implied by this authorization (§18).
- **Every Charter exclusion (§20) is explicitly preserved.** This authorization does not extend to Customer establishment, the Customer–Account Relationship, reclassification/retirement/reactivation, merge/split/transfer, Subscription/Billing/Contract/Entitlement functionality, CRM functionality, Organization equivalence, tenant isolation, Identity/Person wiring, read/list of any established Commercial Account, any Commercial Account `classification` attribute, or any lifecycle policy beyond `PE-001-C022`/`COM-001 §7`'s own canonical definition.
- **The `§20.3` backend-only determination (§21) is preserved and binding** — no frontend/UI implementation is required or authorized for this Business Activity's own Independent Certification, V&V Audit, Release Readiness Audit, or closure.
- **`ADR-038`'s Option A (no classification attribute) and `ADR-040`'s CBOR registration (`CAC-000001`) are both preserved, unaltered, and unreopened by this authorization.**

**This Implementation Authorization does NOT itself authorize implementation to begin within this same task** — the governance-actions bundle that recorded it ("AUREX — Proceed with the next C-022 governance actions... CBOR REGISTRATION / WP REGISTRATION / IMPLEMENTATION AUTHORIZATION") was explicitly limited to governance registration and authorization recording, not to writing, modifying, or generating any application code. No schema, migration, model, repository, service, router, schema module, frontend, or test exists as of this recording, and none was created by the same task that recorded this authorization. A future, separately-initiated implementation task is required before any code is written.

## 25b. What Remains NOT Authorized (current, complete list)

- Implementation itself — no schema, migration, model, repository, service, router, schema module, frontend, or test has been created by any document in this governance sequence, including this one.
- Any expansion of BA-01's own scope beyond §2/§20/§25a.
- Reopening `ROD-C022` D1–D6, `ROD-C022-A` D7–D8, `ROD-C022-B` D9–D10, `ADR-038`, or `ADR-040`.
- A BAR mechanism, registry, or Business Activity Identifier of any kind.
- Any Commercial Account `classification` attribute.
- Read, list, or retrieval of any established Commercial Account.
- Any frontend/Enterprise Experience delivery for this Business Activity (§21, binding).

---

## 26. Self-Review (performed on this Charter before delivery)

**Scope leakage:** Checked against `ROD-C022 §H`'s exhaustive exclusion list (§20 above) — every exclusion is restated verbatim or by accurate paraphrase; none is narrowed. No Customer, Relationship, Subscription, Billing, Contract, Entitlement, CRM, Organization-equivalence, tenant-isolation, Identity/Person-wiring, or invented-lifecycle content appears anywhere in §1–§19. **No leakage found.**

**Unsupported semantics:** Every `[A]`/`[D → RESOLVED]` claim in §1–§19 cites a specific governing document and, where a correction was involved, the specific independent-review finding (`[C-3]`/`[C-4]`/`[C-5]`) that drove it. No new business rule, field, or endpoint appears that is not already present in `TDS-C022`. **No unsupported semantics found.**

**Lifecycle contradictions:** §16 (D9) explicitly preserves Anchor/Intent/Proposed/Assessment as distinct conceptual roles per `COM-001-002`/`COM-001-003`, consistent with §7's rules and §8's schema (no fields or endpoints implying a different lifecycle model were introduced). §14/§18's `active`-only write and deferred BAR treatment do not contradict §16's acceptance of the collapsed realization. **No contradiction found.**

**CBOR/BAR boundary violations (original review):** §17 (as originally written) stated eligibility (settled) but explicitly withheld registration and identifier assignment, consistent with `ADR-039`'s own preparation-only status at that time. §18 states BAR eligibility-once-implemented but explicitly withholds mechanism creation and identifier assignment, consistent with `ROD-C022-B` D10. Neither section implied the other's resolution — `COM-001-005`'s own two-clause, independent-requirement structure was preserved. **No boundary violation found (at original preparation).**

**`§20.3` backend-only determination:** Present at §21, with a four-point evidentiary chain (D8 → independent review §7.2/§7.3 → `ROD-C022-A`'s own mandatory-language requirement), not asserted without support. Confirmed consistent with `ROD-C022-A §C.2`'s own instruction that this determination be "reported and justified per `§19.4`'s STOP-and-report discipline, not silently assumed." **Satisfied.**

**No factual inconsistency was discovered during original preparation that would make this Charter impossible to write** — `ROD-C022`, `ROD-C022-A`, `ROD-C022-B`, `ADR-038`, `ADR-039`, `TDS-C022`, and the independent review were all found mutually consistent on direct re-verification; no document required modification.

### 26a. Self-Review Addendum — CBOR/WP Registration + Implementation Authorization Pass (2026-09-15)

**CBOR/BAR boundary, re-checked after §17 was updated:** §17 now records actual registration (`ADR-040`, `CAC-000001`) while §18 continues to withhold BAR mechanism creation/identifier assignment. `COM-001-005`'s two-clause, independent-requirement structure remains preserved — CBOR execution did not trigger, require, or imply any BAR action. **No boundary violation found.**

**Classification/lifecycle/scope leakage in the registration documents:** `ADR-040 §3` item 4 explicitly re-confirms no classification, lifecycle expansion, or cross-capability semantic was introduced; its registration table (§3 item 1) is a verbatim adoption of `ADR-039 §4`'s own already-reviewed content plus the identifier. `WPR-001`'s new WP-21 row and the delivery-map's updated C-022 row both restate, rather than alter, the same Charter scope (§2/§20). **No leakage found.**

**Implementation Authorization scope check (§25a):** explicitly bounded to §1–§20's own approved content; explicitly re-preserves D9, D10, `ADR-038`, and every Charter exclusion; explicitly states it does not itself authorize code to be written within the same task. **Consistent with the governing instruction's own "does NOT itself authorize implementation" clause.**

**Unrelated/pre-existing content check:** `WPR-001`'s C-023/C-040/D-003 content and every other pre-existing WP row were not touched — the edit was anchored immediately after the WP-19 row, inserting only the new WP-21 row and its own maintenance note. The delivery map's C-023 row and all other capability rows were not touched — only the C-022 row (line 40) and the D-002 summary line (line 183) were edited, both narrowly, via strikethrough-preserve. `CBOR-INDEX.md`'s existing nine rows and `ADR-039` were not altered. **No unrelated content disturbed.**

**No factual inconsistency was found during this pass that would have made registration impossible.** `ADR-039`, `ROD-C022-B`, `ADR-038`, `WPR-001`, `WP-REG-001`, `CBOR-INDEX.md`, and the delivery map were all re-verified directly and found mutually consistent.

---

*End of WP-21 / C-022 BA-01 Charter. Status: CHARTERED — CBOR REGISTERED (`ADR-040` — `CAC-000001`) — BAR DEFERRED (`ROD-C022-B` D10) — WP REGISTERED (`WPR-001`) — IMPLEMENTATION AUTHORIZED (2026-09-15). Implementation itself has NOT begun — no schema, migration, code, or test created. Nothing staged, committed, or pushed.*
