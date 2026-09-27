# TDS-C022 — Customer & Account Management (C-022) — Minimum BA-01 Technical Design

**Document status:** PREPARED FOR INDEPENDENT REVIEW. No WP is registered. No BA charter exists. No CBOR ADR is created. No BAR registration is performed. No implementation of any kind exists. This document translates the already-decided `ROD-C022` boundary into an implementable technical design; **it does not expand business scope beyond `ROD-C022` §H, and it does not reopen D1–D6.**

**Repository Owner authorization basis:** direct instruction "AUREX — C-022 CUSTOMER & ACCOUNT MANAGEMENT — PREPARE TDS-C022 FOR BA-01," following `ROD-C022-Customer-and-Account-Management-Capability-Boundary-and-Minimum-Scope.md` (D1–D6) and `IRA-C022-Customer-and-Account-Management.md` (🟢 GREEN-leaning readiness verdict).

**Classification key** (mirrors `TDS-C021`'s own convention): `[FACT]` — repository fact / verbatim from a LOCKED or Active source. `[RO DECISION]` — a Repository Owner decision already made (`ROD-C022` D1–D6). `[DESIGN]` — a technical design choice made by this document, within the RO-decided boundary. `[INFERENCE]` — a design choice reasoned from evidence but not verbatim-stated; flagged as such, never presented as fact. `[UNRESOLVED — RO/TDS DECISION REQUIRED]` — an item this document explicitly does not resolve. `[IMPLEMENTATION-TIME]` — left to the implementing session, provided stated constraints are met.

---

## 1. Purpose

`[RO DECISION]` Design, at the conceptual/technical-design level, the smallest implementable realization of `ROD-C022` D1/D5: **"Establish Commercial Account"** — one Authoritative Commercial Account, a system-assigned stable Account Reference, minimum canonical identity and status, platform-global, `AuthService`-hosted, `require_platform_admin`-gated. This document creates no migration, model, repository, service, router, schema, frontend, or test — it is Technical Design governance, per the same discipline `TDS-C021`/`TDS-C132` already established.

---

## 2. BA Boundary (carried forward from `ROD-C022` §H — not reinterpreted)

`[RO DECISION]` **In scope:** establish exactly one Authoritative Commercial Account; system-assigned stable Account Reference; minimum canonical Account identity and status; platform-global scope; `AuthService`-hosted; existing `require_platform_admin` authorization pattern.

`[RO DECISION]` **Explicitly out of scope** (verbatim from `ROD-C022` §H, restated not reinterpreted): Customer establishment of any kind; Customer–Account Relationship establishment; reclassification; merge/split/transfer; any Subscription (C-020), Billing (C-024), Contract (C-025), or Entitlement (C-023) functionality; any CRM/sales-pipeline/case-management/ERP-Customer-Master functionality; any Organization (C-004) equivalence or reference; tenant isolation of any kind; Identity (C-001/URA-001) or Person (C-006) reference wiring; any invented lifecycle policy.

`[DESIGN]` **Retire/reactivate:** per this task's own carve-out ("unless already required merely to represent the minimum authoritative status"), BA-01 does **not** implement a retire or reactivate *operation* (no endpoint, no transition). It does, however, declare the full canonical status vocabulary in the schema (§6.1) so the record can represent its own current status truthfully from day one — exactly the "declare the full lifecycle shape, exercise a subset" pattern `c021_offering_definition.state` already established for `WP-20`. This is not a scope expansion: no route, service method, or UI ever changes status away from its established default.

---

## 3. Authoritative Domain / Entity Ownership (Assessment 2)

**`[CORRECTED — remediation of independent-review finding `[C-4]`]`** The `COM-001-033` quotation below previously included a parenthetical ("parent Account reference, where applicable") that does not appear in `COM-001-033`'s own text — it is `PE-001-C022 §1.16` wording, now correctly re-attributed.

`[FACT]` `COM-001-033` (LOCKED), verbatim, complete: *"The single current, canonical commercial-container fact for a Commercial Account: identity, Account-to-Account hierarchy position, and status. Keyed only to its own Commercial Account Anchor. Never equivalent to a Workspace, Organization, Identity, Membership, or Billing Account."* `[FACT]` `PE-001-C022 §1.16`'s own Account row adds the parenthetical gloss *"(parent Account reference, where applicable)"* to "hierarchy position" — Active-specification elaboration, not LOCKED `COM-001` text; both are consistent, and the gloss is used at §6.1/§10 below where the hierarchy design is discussed. `[FACT]` `COM-001-035`: a committed transition promotes only the specific concern(s) it actually changed — Customer, Account, or Relationship — never an undifferentiated combined promotion.

`[DESIGN]` BA-01 owns exactly one entity: the Authoritative Account Context. No other capability's table is read or written. `C-004` Organization is not consumed, not referenced, and not equivalent — `[RO DECISION]` `ROD-C022` §I: *"Not consumed, not referenced, not equivalent... N/A by explicit decision."*

---

## 4. Critical Classification Issue — Explicit Handling (Not Silently Resolved)

**This section exists specifically because `IRA-C022 §9`/`§12.3` flagged a genuine discrepancy that this TDS is required to handle explicitly, per direct instruction, rather than reconcile quietly.**

`[FACT]` `ROD-C022 §H`'s own BA-01 boundary text states: *"minimum canonical account identity/classification/status."*

**`[CORRECTED — remediation of independent-review finding `[C-4]`]`** The two quotations immediately below previously carried parenthetical wording not actually present in `COM-001-032`/`033`'s own LOCKED text (that wording is `PE-001-C022 §1.16`'s, correctly attributed there instead). The corrected quotations follow; the substantive conclusion — no classification attribute in `COM-001-033` — is unaffected by the citation fix.

`[FACT]` `COM-001-033` (LOCKED), verbatim, complete: *"identity, Account-to-Account hierarchy position, and status."* **No "classification" attribute appears anywhere in `COM-001-033`'s text.**

`[FACT]` `COM-001-032` (LOCKED), verbatim, complete, the adjacent clause governing **Customer**, not Account: *"legal-entity or person identity reference, **classification**, and status."* Classification is textually and substantively a **Customer**-authority attribute in the LOCKED constitutional source. (`COM-001-032` itself carries no illustrative examples of classification values — the "(e.g., segment, partner/reseller/distributor designation)" gloss appearing below is `PE-001-C022 §1.16` Active-specification elaboration, not LOCKED text.)

**`[CORRECTED — remediation of independent-review finding `[C-5]`, `IRA-TDS-C022_Independent_Review.md §6.2`]`** The conclusion previously drawn here — that "no classification attribute for Account" holds "in either governing document" — was independently found materially incomplete on re-verification. It is corrected below rather than silently rewritten.

~~`[FACT]` `PE-001-C022 §1.16`'s own context-model table mirrors the same split: the Authoritative Customer Context row names *"classification (e.g., segment, partner/reseller/distributor designation)"*; the Authoritative Account Context row names only *"its own identity, its Account-to-Account hierarchy position..., and its current status"* — again, no classification attribute for Account, in either governing document.~~ *(Corrected — this claim is accurate only for `§1.16`'s own context-model table row, considered in isolation. It is not accurate for `PE-001-C022` as a whole. Independently re-verified: `PE-001-C022` affirmatively attaches classification to the Authoritative **Account** Context in at least four other places — `EX-C022-04` Trigger, verbatim: "An existing Authoritative Customer Context's **or Authoritative Account Context's classification** no longer reflects the enterprise's understanding of the relationship"; `C022-O02`, verbatim: "Every change to **a Customer's or Account's classification**..."; `§1.4 Scope`, verbatim: "...reclassifying... the Authoritative Customer Context **and the Authoritative Account Context**..."; the Guiding Architectural Question, verbatim: "...including that representation's **classification**, hierarchy, and lineage through establishment, **reclassification**...". `§1.16`'s own table is therefore not representative of the full specification on this point.)*

**Consequence, scoped narrowly:** this is a genuine conflict between LOCKED `COM-001-033` (silent on Account classification) and Active `PE-001-C022` (affirmative on Account classification in four places) — a `CLAUDE.md §16` canonical-authority conflict, not merely `ROD-C022 §H` wording imprecision as this section previously framed it. **This correction does not reopen `ROD-C022-A` D7.** `ROD-C022-A §B.2` already recorded, on the complete evidence (including these four passages, per the independent review that surfaced them), that BA-01 excludes the classification field (Option A), and that the underlying `COM-001-033` ↔ `PE-001-C022` conflict is logged as a separate, later architecture-governance correction item, not resolved by this TDS, this correction, or any implementation session. The schema at §6.1 is unchanged by this correction — it already excluded `classification`, and remains correct in outcome.

**Determination of what each source says (no invention, no reconciliation):**

| Source | Does it define an Account "classification" attribute? |
|---|---|
| `COM-001-033` (LOCKED, constitutional) | **No.** |
| `PE-001-C022 §1.16` (Active, Enterprise Experience Spec) | **No.** |
| `COM-001-032` (LOCKED, constitutional) | Defines classification, but for **Customer**, not Account. |
| `ROD-C022 §H` (Repository Owner decision record) | States "identity/classification/status" for the Account BA-01 boundary — **the only source that attaches "classification" to Account.** |

`[DESIGN — the position this TDS takes, and why]` A LOCKED constitutional clause (`COM-001-033`) constrains what a Repository Owner decision record may authorize for a given Business Object — a ROD cannot expand a LOCKED entity's own canonical fact set merely by restating it imprecisely, and nothing in `ROD-C022`'s own rationale text (§E) discusses "classification" as a deliberate, reasoned addition; it appears only once, in the summary boundary line, alongside "identity" and "status," in a pattern that reads as an inherited restatement of `COM-001-032`'s Customer wording rather than an intentional, independently-justified expansion of the Account model. **This TDS therefore does not invent a `classification` column** — doing so would violate the explicit instruction *"do not invent an Account classification field merely to satisfy the ROD wording"* and would introduce a field with no LOCKED constitutional basis.

**This does not "remove an approved requirement" silently** — the conflict is documented here, in full, with both readings preserved verbatim, and is carried forward as an explicit unresolved item (§21) requiring Repository Owner confirmation before implementation authorization: either (a) `ROD-C022 §H`'s wording is confirmed to have been an imprecise restatement, and the Account schema correctly has no classification field (matching `COM-001-033` as written), or (b) the Repository Owner explicitly intends a Commercial Account classification concept and records a fresh, express decision to that effect — which would itself be a new RO decision, not something this TDS or any future implementation session may infer or add unilaterally.

**Design consequence for this document:** §6.1's schema table below does **not** include a `classification` column, and this is called out again at that point, not silently.

---

## 5. Selected Service Host

`[RO DECISION]` `ROD-C022` D3: **`AuthService`.** No further analysis is required — the ROD already resolved this, unlike `C-021`'s own IRA-stage gap (`IRA-C021 §17`). Rationale on record: reuse of existing architecture and the unbroken precedent of `WP-20`/`WP-17` hosting their own commercial-adjacent capabilities in `AuthService`.

---

## 6. Commercial Account Data Model (Assessment 3) — Schema-Shape STOP-and-Report (`CLAUDE.md §18`/`§19.4`), conceptual level only

`[DESIGN]` No migration, ORM model, database table, repository, service, router, frontend, or test is created by this document. Precedent read directly for this design: `models/c021_offering_definition.py` (WP-20, closed, certified), `models/role.py`, `models/c023_entitlement_context.py`.

### 6.1 Proposed table (conceptual): `c022_commercial_account`

| Field | Conceptual type | Null? | Notes / precedent |
|---|---|---|---|
| `id` | UUID, PK, default `uuid4` | NOT NULL | Record identity + audit correlation id. Every `AuthService` model's PK convention. |
| `account_reference` | String(30), UNIQUE | NOT NULL | System-assigned stable Account Reference (`ROD-C022` D1/D5; `COM-001-036`'s "stable Customer/Account Reference"). Format and generation mechanism per §7. |
| `account_name` | String(255) | NOT NULL | Minimum canonical identity (`COM-001-033`: "its own identity"). Precedent: `offering_name`, `role.role_name`. No uniqueness invariant imposed (§6.5) — `COM-001-033` states no such invariant, mirroring `COM-001 §6`'s own silence on offering-name uniqueness. |
| ~~`classification`~~ | — | — | **Deliberately absent.** See §4 — `COM-001-033` defines no Account classification attribute; inventing one to satisfy `ROD-C022 §H`'s imprecise wording is explicitly prohibited by this task's own instruction. `[UNRESOLVED — RO DECISION REQUIRED]` before this can change (§21). |
| `status` | String(20), `CheckConstraint "status IN ('active','suspended','retired')"`, default `'active'` | NOT NULL | `[INFERENCE, not verbatim `COM-001-033` text]` — `COM-001-033` names "current status" without an explicit enumerated set for Account specifically. `PE-001-C022 §1.16`'s illustrative `(active, suspended, retired)` set is textually attached to the *Customer* context row, but `EX-C022-05`/`EX-C022-06` ("A business reason to close **a Customer's or Account's** standing"; "A previously retired **Customer/Account**...") confirm retire/reactivate applies to Account as well as Customer — supporting, by inference, the same three-value set for Account. **BA-01 writes only `'active'`** — the full set is declared for schema correctness (mirroring `c021_offering_definition.state`'s "declare the full closed set, write one value" pattern) but no transition endpoint exists (§2). |
| `parent_account_id` | UUID, FK → `c022_commercial_account.id` | NULLABLE | `COM-001-033`'s own "Account-to-Account hierarchy position," glossed by `PE-001-C022 §1.16` as "(parent Account reference, where applicable)" *(citation corrected — `[C-4]`)*. **Declared in the schema so a future hierarchy/relationship increment needs no `ALTER`; never written non-NULL by BA-01** (BA-01 establishes exactly one standalone account, no counterparty, no relate/transfer — `ROD-C022` §H excludes structural transitions entirely). Precedent: `c021_offering_definition.supersedes_id` (self-referential, nullable, declared-not-exercised), `role.supersedes_id`. |
| `created_by_actor_id` | UUID | NOT NULL | Point-in-time audit citation of the `PLATFORM_ADMIN` caller's `person_id`. **NOT a foreign key** — precedent: `c023_entitlement_context.committed_by_actor_id`, `c021_offering_definition.created_by_actor_id`. |
| `created_at` | `DateTime(timezone=True)`, default now() | NOT NULL | Standard platform timestamp. |
| `updated_at` | `DateTime(timezone=True)`, `onupdate` now() | NULLABLE | Standard platform timestamp. |

**No `organization_id` column** — `[RO DECISION]` D2, platform-global. Precedent: `roles`, `c021_offering_definition` both carry no `organization_id`. This is a structural expression of D2, not an omission.

### 6.2 Ownership

`[DESIGN]` `AuthService` exclusively (§5). No other service reads or writes `c022_commercial_account`.

---

## 7. Account Reference Generation and Uniqueness (Assessment 4)

`[DESIGN]` Two identifiers, mirroring `c021_offering_definition`'s own `id` + `offering_reference` split: `id` (UUID PK, internal handle) and `account_reference` (the stable, external, system-assigned reference `COM-001-036` names as consumable by downstream capabilities).

**`[CORRECTED — remediation of independent-review finding `[C-3]`, `IRA-TDS-C022_Independent_Review.md §5.3`/§9]`** The reasoning previously recorded here was factually incorrect and is corrected below rather than silently rewritten, per this repository's own no-silent-fix discipline.

~~`[UNRESOLVED — IMPLEMENTATION-TIME, not an RO decision]` `ROD-C022`/`IRA-C022` do not specify an exact reference format (unlike `C-021`'s own `[RO DECISION] O1`, which fixed `PREFIX-NNNNNN` per `COM-001-001`). `COM-001-030`–`036` (the Customer/Account section) does **not** repeat `COM-001-001`'s Universal Identity clause the way `COM-001-010`/`011` did for Subscription or the way Offering Definition's own section does — so this TDS does **not** assume `ACCOUNT-NNNNNN` is mandated.~~ *(Corrected — this reasoning was independently re-checked against `COM-001` directly and found factually wrong on both premises. First, the contrast drawn does not exist: re-verified directly against `COM-001` — neither `COM-001-010`/`011` (Subscription, Section 5) nor Section 6 (Offering Definition) repeats `COM-001-001`'s `PREFIX-NNNNNN` clause either; the string `PREFIX-NNNNNN` occurs exactly once in the entire document, in Section 4. Second, non-repetition is the document's own stated norm, not a signal of exemption: `COM-001` line 44, verbatim — "Every construct in Sections 5–9 inherits this section in full... Sections 5–9 state only what is distinctive to each construct." Section 7's silence on identity format is therefore evidence of inheritance, not evidence that Commercial Account is exempt from `COM-001-001`. Third, the certified `C-021` precedent reads the opposite way: `TDS-C021 §9.3` states verbatim that "realizing `COM-001-001`'s mandated format is new implementation work," and the shipped `c021_offering_definition.py` (L35–41) declares `OFFERING_REFERENCE_PREFIX = "OFFERING"` under the comment "`COM-001-001` Universal Identity prefix." `[RO DECISION] O1` did not "fix" the format — it fixed only the **allocation mechanism** as implementation-time-flexible; the `PREFIX-NNNNNN` format itself was already a LOCKED constitutional requirement, independent of O1.)*

**Current, corrected position:** `[FACT]` `COM-001-001` (Section 4, inherited in full by Section 7 per `COM-001` line 44) requires every commercial object — including Commercial Account — to carry *"a globally unique, permanent identity in `PREFIX-NNNNNN` form."* This is **not** an open Repository Owner question; it is an already-LOCKED constitutional requirement that this TDS previously, incorrectly, treated as unresolved. `[DESIGN]` `account_reference` SHALL be of the form `PREFIX-NNNNNN` — six-digit zero-padded numeric suffix, prefix token `[IMPLEMENTATION-TIME]` (to align with the future CBOR Business Object Identifier, mirroring `TDS-C021 §9.3`'s own treatment of `offering_reference`'s prefix). `[DESIGN]` Consistent with the `[RO DECISION] O1` precedent (which this TDS reuses as a *mechanism* pattern, not a *business-semantics* copy — `ROD-C022` records no equivalent O1-style decision of its own, and none is required, since the format itself is already fixed by `COM-001-001`): the concrete **generation mechanism** (a DB sequence, an in-transaction `MAX+1` with retry, an application-level allocator, or equivalent) remains `[IMPLEMENTATION-TIME]`, provided the acceptance properties (system-assigned; monotonic; `PREFIX-NNNNNN`; unique; concurrency-safe) are met. **This correction narrows the design space (from "format undetermined" to "format constitutionally fixed") — it does not expand BA-01's business scope, invent a new Account Reference format, or copy any C-021 business semantic; it corrects a misapplied architectural-reference-generation *mechanism* citation to align with the LOCKED requirement both C-021 and C-022 equally inherit.**

`[DESIGN]` `account_reference` — **UNIQUE** (plain unique index, whole-table). No in-place versioning exists at BA-01 scope, so a plain unique constraint is correct (mirrors `TDS-C021 §9.5`'s own reasoning for `offering_reference`).

---

## 8. Minimum Required Fields and Validation (Assessment 5)

`[DESIGN]`
- `account_name`: required, non-blank (mirrors `offering_name`'s / `role.role_name`'s blank-rejection pattern). No uniqueness invariant (§6.1).
- `account_reference`, `id`, `status`, `parent_account_id`, `created_by_actor_id`: never caller-supplied — system-assigned or system-derived only, mirroring `offering_reference`/`state`/`version`/`supersedes_id`'s own "caller cannot override" pattern in `c021_offering_definition`.
- No other field exists in the establish request per §6.1/§4.

---

## 9. Account Status Semantics — Only to the Extent Already Authorized (Assessment 6)

`[DESIGN]` See §6.1. **BA-01 writes exactly one status value, `'active'`, at establish time, and exposes no mechanism to change it.** The closed set `{active, suspended, retired}` is declared in the schema for constitutional-model correctness (`COM-001-033`'s "current status" concern) and future-increment readiness, not because BA-01 itself exercises suspend/retire. This is consistent with, and does not exceed, the task's own explicit carve-out in §2 above.

---

## 10. Account Hierarchy Handling — Explicit Determination (Assessment 7)

**Explicitly determined, not left ambiguous:** `[DESIGN]` **Hierarchy is declared in the schema (`parent_account_id`, §6.1) but is NOT exercised by BA-01.** BA-01 establishes exactly one standalone Commercial Account with no counterparty and no relate/transfer intent (`ROD-C022 §H` excludes Relationship establishment and all structural transitions outright). `COM-001-033` names hierarchy position as part of the canonical Account fact; `PE-001-C022 §1.16` glosses it *"(parent Account reference, where applicable)"* *(citation corrected — `[C-4]`, this gloss is `PE-001-C022`'s, not `COM-001-033`'s own text)* — the parenthetical itself signals hierarchy is conditional, not mandatory, for every Account. BA-01's own standalone establishment is exactly the "not applicable" case: the column exists so a future structural-transition increment (`ERB-C022-04`) needs no `ALTER`, but every BA-01-established row has `parent_account_id = NULL`.

---

## 11. Scope / Platform-Global Behavior (Assessment 8)

`[RO DECISION]` `ROD-C022` D2: platform-global. `[DESIGN]` No `organization_id` column (§6.1); `CLAUDE.md §21.4`'s Mandatory Tenant-Isolation Test Checklist is structurally not applicable, identical treatment to `C-021`'s own D8 (`TDS-C021 §11`). Substitute assurance (mirrors `TDS-C021`/`IRA-C021` exactly): (a) non-`PLATFORM_ADMIN` denied on the establish route; (b) `PLATFORM_ADMIN` succeeds; (c) an automated assertion, via both live table introspection and ORM metadata, that `c022_commercial_account` has no `organization_id`/`tenant*` column.

---

## 12. Authorization and Tenant-Middleware Treatment (Assessment 9, part 1)

`[RO DECISION]` `ROD-C022` D3/D5: every BA-01 route is gated by the existing `Depends(require_platform_admin)` dependency — the certified `C-003`/`C-021` pattern, **not** the tenant-scoped `require_matching_tenant_or_platform_admin` gate. `[DESIGN]` `middleware/tenant.py`'s exemption list gains one new prefix pair (e.g. `/commercial-accounts`, `/commercial-accounts/`) on the same `/roles`/`/offerings` basis, with a rationale comment citing `ROD-C022` D2.

---

## 13. Service/Module Placement (Assessment 10)

`[DESIGN]` `Backend/Services/AuthService/` — `models/c022_commercial_account.py`, `repositories/c022_commercial_account_repository.py`, `services/commercial_account_service.py`, `routers/commercial_account.py`, `schemas/commercial_account.py` — naming mirrors `c021_offering_definition`'s own file layout exactly. No new service (§5).

---

## 14. Repository / Persistence Design (Assessment 11)

`[DESIGN]` `CommercialAccountRepository(BaseRepository[CommercialAccount])` — the same generic base every prior capability uses. Minimum methods: `create()` (insert), `get_by_id()`, `get_by_account_reference()`. `[DESIGN]` Whether `list_all()` is required is addressed in §15 (API contract) — `ROD-C022 §H` authorizes "establish" only, and does not name "list"/"read" the way `ROD-C021` D4 explicitly did for C-021; this TDS does not assume list/read are in scope merely by analogy (§21).

---

## 15. API Contract and Endpoint Behavior (Assessment 12)

`[UNRESOLVED — flagged, not assumed]` `ROD-C022 §H` names only **"establish"** in its authorized boundary. Unlike `ROD-C021` D4 (which explicitly named "establish/list/read"), `ROD-C022` does not explicitly authorize a read/list endpoint for BA-01. `[DESIGN]` This TDS designs the establish endpoint only, and records read/list as a `[FUTURE TDS QUESTION]` / RO-confirmation item (§21) rather than silently including or silently excluding it.

- `POST /commercial-accounts` — `Depends(require_platform_admin)`. Request: `{account_name: str}` only (§8). Response: 201, the persisted row (`id`, `account_reference`, `account_name`, `status="active"`, `parent_account_id=null`, `created_at`).

No other route is designed by this document.

### 15.1 Commercial Lifecycle-Pattern Conformance — Explicit Disclosure (remediation of independent-review finding `[C-5]`, `IRA-TDS-C022_Independent_Review.md §5.6`)

`[FACT]` `COM-001-002` (Section 4, inherited in full by Section 7 per `COM-001` line 44), verbatim: *"Every commercial construct below distinguishes three roles, never conflated: an Anchor Context..., an Authoritative Context..., and a Resulting Context..."* `[FACT]` `COM-001-003`, verbatim: *"Every commercial action states its business reason and target outcome (an Intent Context) before any candidate change (a Proposed Context) is shaped."* `[FACT]` `PE-001-C022 §1.14` names the mandatory stage progression: *"Anchor → Understand Standing → Frame Lifecycle Intent / Frame Structural Intent → Shape & Assess → Commit → Distribute Reference."* `[FACT]` `ERB-C022-06`'s own Entry Context, verbatim: *"An assessed Proposed Commercial Party Context and/or Proposed Commercial Relationship Context with its Commercial Dependency Assessment Context."*

**Disclosed, not silently omitted:** the single-call `POST /commercial-accounts` design above realizes **none** of the Anchor, Intent, Proposed, or Assessment stages as distinct, separately-observable constructs — it collapses the full `Anchor → Frame Lifecycle Intent → Shape & Assess → Commit` progression into one request/response cycle. This is the same pattern `c021_offering_definition`'s own `establish()` uses (a single call, no separate anchor/intent/proposal step), and `ROD-C022 §H` is silent on whether BA-01 must realize the lifecycle pattern as distinct steps or may collapse it — §H names only the outcome ("Establish one Authoritative Commercial Account"), not the interaction shape.

**This TDS does not resolve, by inference, whether a collapsed single-call realization is an accepted minimum-slice deferral or a gap requiring a multi-step design.** Recording it as an unresolved item rather than assuming either answer:

> `[UNRESOLVED — RO / architecture-governance determination, not decided here]` Is a single-call establish (collapsing Anchor/Intent/Proposed/Assessment into one request) an acceptable minimum-slice realization of `COM-001-002`/`COM-001-003`'s inherited lifecycle pattern for BA-01, consistent with the `c021_offering_definition` precedent — or does `COM-001-002`/`COM-001-003` require these to be separately observable even at BA-01's minimum scope? This TDS's own design (§15) assumes the former, mirroring the certified C-021 precedent, but this assumption is now disclosed explicitly rather than left implicit, per the independent review's finding. **No new lifecycle semantics, reclassification, retirement/reactivation, merge/split/transfer, or other out-of-scope behavior is introduced by raising this question** — it concerns only whether BA-01's single existing operation (establish) should be internally structured as one step or several, not whether any additional operation is authorized.

This disclosure does not change §15's design — the single-call endpoint remains as specified — and does not reopen `ROD-C022-A` D7/D8.

---

## 16. Error / Validation Behavior (Assessment 13)

`[DESIGN]` Blank/whitespace `account_name` → 422. Missing/malformed `Authorization` header → 400/401 (existing `AuthService` global behavior). Non-`PLATFORM_ADMIN` caller → 403. Any caller-supplied `account_reference`/`id`/`status`/`parent_account_id` in the request body → ignored (not present in the schema at all, per §8) — mirrors `c021_offering_definition`'s own "not in the schema" enforcement rather than a runtime override-and-reject check.

---

## 17. Audit / Event Behavior Using Existing AUREX Mechanisms (Assessment 14)

`[DESIGN]` `record_audit(action="ESTABLISH_COMMERCIAL_ACCOUNT", actor_id=<person_id>, status=SUCCESS, metadata={account_reference, account_name})` on success, mirroring `c021_offering_definition`'s `ESTABLISH_OFFERING_DEFINITION` pattern exactly (`SD-002 §6` Evidence, `COM-001-063`-class discipline). No new audit or event mechanism. `publish_event("COMMERCIAL_ACCOUNT_ESTABLISHED", {...})` alongside, using the existing structured-log stand-in — not a real event bus, consistent with `IRA-C021 §16`'s own disclosure for the identical pattern.

---

## 18. Idempotency / Concurrency Considerations (Assessment 15)

`[DESIGN]` The only concurrency point is `account_reference` allocation — covered by the `UNIQUE` constraint plus an allocate-and-retry discipline (`except IntegrityError → rollback → retry`), the same backstop `role_service.establish` and `OfferingDefinitionService.establish` already certify. No content-level idempotency invariant exists on `account_name` — `COM-001-033` states none, mirroring `COM-001 §6`'s own silence on offering-name uniqueness (`TDS-C021 §9.5`'s identical reasoning).

---

## 19. Security and Negative-Control Requirements (Assessment 16)

`[DESIGN]` Required negative controls at implementation/test time: non-`PLATFORM_ADMIN` → 403; no-role-claim → 403; missing/malformed `Authorization` → 400; live table introspection + ORM metadata both confirming no `organization_id`/`tenant*` column (§11); caller-supplied `account_reference`/`id`/`status`/`parent_account_id` proven absent from the accepted request schema (§8, §16).

---

## 20. Testing Implications (Assessment 17)

`[DESIGN]` Minimum test set, mirroring `test_offering_definition.py`'s own structure: establish happy path + persistence; `account_reference` is system-assigned, unique, monotonic-or-otherwise-acceptance-property-conformant (§7); caller cannot override `account_reference`/`id`/`status`/`parent_account_id`; blank `account_name` → 422; non-`PLATFORM_ADMIN` → 403; no-role → 403; missing/malformed `Authorization` → 400; schema assertion (no `organization_id`, live introspection + ORM metadata); establish emits a SUCCESS audit record; a purpose-built end-to-end establish probe (`CLAUDE.md §19.7b` method note). Exact test count and naming are `[IMPLEMENTATION-TIME]`.

---

## 21. Explicit Unresolved Decisions and Assumptions (Assessment 21 content, consolidated)

**`[UNRESOLVED — RO DECISION REQUIRED before implementation authorization]`**
1. **The classification discrepancy (§4).** This TDS does not include a `classification` column. If the Repository Owner intends one, a fresh, explicit decision is required — this TDS does not invent it, and does not treat `ROD-C022 §H`'s wording as sufficient authority on its own given `COM-001-033`'s silence.
2. **Whether BA-01 includes a read/list endpoint.** `ROD-C022 §H` names only "establish"; this TDS designs establish only (§15). If read/list is intended (as it was explicitly for `C-021`'s own BA-01), that should be confirmed before implementation, not assumed by analogy.
3. **CBOR registration.** `IRA-C022 §11` found Commercial Account CBOR-eligible under `CMD-001 §26.3a` (all three steps satisfied). Registration itself (a future ADR, mirroring `ADR-037`) is not performed by this document and remains a mandatory pre-implementation-authorization prerequisite.
4. **BAR.** `COM-001-060` will apply to the eventual Business Activity once implemented — the same class of Repository Owner decision every prior BA-01 (`C-021`, `C-023`, `C-132`) required (no mechanism exists; none is invented). Not addressed by `ROD-C022`; requires its own decision before implementation authorization, not silently assumed resolved by analogy.
5. **Commercial lifecycle-pattern conformance (§15.1, remediation item `[C-5]`).** Whether BA-01's single-call establish design is an accepted minimum-slice realization of `COM-001-002`/`COM-001-003`'s inherited Anchor/Intent/Proposed/Assessment pattern, or requires a multi-step design. Not resolved by this document.

**`[FUTURE TDS QUESTION]` (a later C-022 increment's own TDS, not this one):** Customer establishment; Customer–Account Relationship; reclassification/retire/reactivate operations; merge/split/transfer; Identity/Person wiring; a future tenant-scoped Account relationship (`ROD-C022 §E`'s own closing sentence — not permanently foreclosed, requires its own future RO decision).

**`[IMPLEMENTATION-TIME]` (no further TDS or RO decision needed, provided constraints are met):** exact `account_reference` generation mechanism, provided it meets the acceptance properties in §7; exact `String` length bounds and index/constraint naming; exact route prefix.

**Assumptions stated explicitly (not silently made):**
- This TDS assumes the `parent_account_id` hierarchy column should be declared-but-unexercised (§10) rather than omitted entirely, mirroring the `c021_offering_definition.supersedes_id` precedent — a reasoned design choice, not a Repository Owner mandate.
- This TDS assumes the account-status closed set is `{active, suspended, retired}` by inference from `EX-C022-05`/`06` (§6.1) — not a verbatim `COM-001-033` enumeration.

---

## 22. Traceability Back to `ROD-C022` and `IRA-C022`

| # | Requirement (source) | Design element (this TDS) |
|---|---|---|
| 1 | Establish one Authoritative Commercial Account (`ROD-C022` D1/D5) | §6, §15 |
| 2 | System-assigned stable Account Reference (`ROD-C022` D1/D5; `COM-001-036`) | §7 |
| 3 | Minimum canonical identity/status (`ROD-C022` §H; `COM-001-033`) | §6.1, §9 — classification excluded, see §4 |
| 4 | Platform-global scope (`ROD-C022` D2) | §6.1, §11 |
| 5 | `AuthService` hosting (`ROD-C022` D3) | §5, §13 |
| 6 | Existing `require_platform_admin` pattern (`ROD-C022` D3/D5) | §12 |
| 7 | Identity/Person deferred (`ROD-C022` D4) | §6.1 (no reference columns designed) |
| 8 | No Customer, no Relationship, no reclassify/retire/reactivate op, no merge/split/transfer (`ROD-C022` §H) | §2, §9, §10, §15 (none designed) |
| 9 | CBOR eligibility confirmed, not performed (`IRA-C022 §11`) | §21 item 3 |
| 10 | Classification discrepancy surfaced, not resolved (`IRA-C022 §9`/`§12.3`) | §4, §21 item 1 |

No requirement above was manufactured; every row traces to a `ROD-C022` decision, a `COM-001`/`PE-001-C022` clause, or an `IRA-C022` finding.

---

## 23. Implementation Acceptance Criteria (Assessment 22)

`[DESIGN]` If implementation is later, separately authorized: a `PLATFORM_ADMIN` `POST /commercial-accounts` with a valid `account_name` returns 201 with a persisted row (`status="active"`, `parent_account_id=null`); the caller cannot supply or override `account_reference`/`id`/`status`/`parent_account_id`; two establishes yield distinct account references meeting the §7 acceptance properties; a non-`PLATFORM_ADMIN` caller receives 403; the table carries no `organization_id`/`tenant*` column (live introspection + ORM metadata); a SUCCESS audit record is emitted on establish. **This is an acceptance-criteria design statement, not an implementation authorization.**

---

## 24. What This Document Does NOT Authorize

Consistent with `TDS-C021`'s own closing discipline: this document does not authorize a WP registration, a BA-01 charter, Implementation Authorization, any schema/migration/ORM model/repository/service/router/test, any frontend implementation, a CBOR ADR, BAR registration, a commit, or a push. It does not alter any LOCKED document, `ROD-C022`, `IRA-C022`, `ROD-C021`, `IRA-C021`, `WP-20` or its governance artifacts, `CBOR-INDEX.md`, `WPR-001`, `WP-REG-001`, `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md`, or any C-020/C-023/C-040 governance content.

---

## 25. Change Control

**Original drafting pass:** created this document — `architecture/06-Reviews/TDS-C022_Customer_and_Account_Management_Minimum_BA_Technical_Design.md`.

**Remediation pass (2026-09-15, "AUREX — C-022 BA-01 — REMEDIATE INDEPENDENT REVIEW FINDINGS C-3 THROUGH C-7"):** corrected §7 (`[C-3]` — the `COM-001-001` `PREFIX-NNNNNN` inheritance reasoning was factually wrong and is corrected via strikethrough-preserve); §3/§4 (`[C-4]` — three citation misattributions, where `PE-001-C022 §1.16` wording had been tagged as LOCKED `COM-001-032`/`033` text, corrected); §6.1/§10 (`[C-4]`, the `parent_account_id` parenthetical misattribution, corrected); §4 (`[C-5]` re: classification — corrected the "no classification attribute in either governing document" conclusion, which independent re-verification found materially incomplete against `PE-001-C022`'s own `EX-C022-04`/`C022-O02`/`§1.4`/GAQ); new §15.1 (`[C-5]` re: lifecycle-pattern conformance — explicit disclosure added, one new unresolved item recorded, not resolved by inference); §21 item 5 added (the §15.1 unresolved item). **`[C-6]` (CBOR) and `[C-7]` (BAR) required no `TDS-C022` correction** — re-verified against `CMD-001 §26.3a` and `COM-001-005`/`-060`/`-061` directly; the original document's own treatment was found accurate on independent re-check and is unchanged. Every correction is strikethrough-preserved, not silently rewritten, per this repository's own no-silent-fix discipline. `ROD-C022-A` D7/D8 are not reopened by any of these corrections — where a correction touches classification (§4) or the establish-only design (§15.1), the correction is explicitly scoped as a factual/citation fix or a disclosure, not a re-litigation of the recorded decision.

**Files read for cross-reference, not modified, this remediation pass:** `IRA-TDS-C022_Independent_Review.md` (§3, §5.3, §5.6, §6.2, §9 — the findings this pass remediates); `ROD-C022-A_Gate_Conditions_Classification_and_Read_List_Decision.md` (D7/D8, confirmed unchanged and not reopened); `COM-001` (re-read directly: line 44 Section 4 inheritance preamble, `COM-001-001`, `COM-001-002`, `COM-001-003`, `COM-001-032`, `COM-001-033`, `COM-001-035`); `PE-001-C022_Customer_and_Account_Management.docx` (v1.2, re-extracted and re-read directly: `§1.14`, `EX-C022-04`, `C022-O02`, `§1.4`, the Guiding Architectural Question, `ERB-C022-06`'s own Entry Context and Dependencies); `TDS-C021_Product_and_Service_Catalog_Minimum_BA_Technical_Design.md` §9.3 (precedent re-verified); `Backend/Services/AuthService/models/c021_offering_definition.py` (L35–41, L71–77, re-verified for the `OFFERING_REFERENCE_PREFIX`/`COM-001-001` citation).

**Not modified, either pass:** any LOCKED constitutional document; `ROD-C022`; `ROD-C022-A`; `IRA-C022`; `IRA-TDS-C022_Independent_Review.md`; `ROD-C021`; `IRA-C021`; `WP-20` or any of its governance artifacts; `CBOR-INDEX.md`; `WPR-001`; `WP-REG-001`; `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md`; any C-020, C-023, or C-040 governance artifact; any `Backend/` or `source/frontend/` file, migration, or test. No WP number is registered. No CBOR or BAR registration was performed. Nothing was staged, committed, or pushed.

*End of TDS-C022. `[C-1]`/`[C-2]` (classification, read/list) remain resolved by `ROD-C022-A` D7/D8, not reopened here. `[C-3]`/`[C-4]` are corrected by this remediation pass. `[C-5]`'s lifecycle-pattern question, and `[C-6]`/`[C-7]` (CBOR, BAR), remain explicitly unresolved and are not to be silently closed by any future pass without their own recorded decision.*
