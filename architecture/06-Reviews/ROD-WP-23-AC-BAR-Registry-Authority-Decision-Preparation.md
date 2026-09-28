# ROD-WP-23-AC — BAR Registry Authority: Decision Preparation (RD-23-03)

**Work Package:** `WP-23` (Enterprise BAR Mechanism), Workstreams A–C tranche (RD-23-02)
**Prepared:** 2026-09-25, per the Repository Owner's RD-23-03 instruction (`IRA-WP-23-AC_BAR_Workstreams_A-C_Closure_Readiness.md §0`): "KEEP OPEN. Do NOT select BAR-INDEX, the registering act, or the bar_registration table as authoritative yet. Prepare a focused decision-preparation artifact … Do not create an ADR yet."
**Status:** ~~**DECISION PREPARATION — NO OPTION SELECTED.**~~ *(Updated 2026-09-25.)* **DECIDED — Option D (Layered Authority Model), by the Repository Owner (§0).** The analysis below (§1–§8) is preserved unchanged as the analysis presented for decision.
- No ADR is created (see §0.3).
- No change is made to the `bar_registration` docstring, the BAR services, the schema, the design document or the WP-23 Charter. *(Note added 2026-09-28, Gate 5 condition C-2, `RRA-WP-23-AC` ST-12: this was accurate for this decision record at the time. Later, separately authorized acts changed some of these: the Charter §21 and design §19 rows C/D under RD-23-04; the `bar_registration` model and service docstrings, and the service transaction handling, under the Gate 3 remediation (CERT-F-03, VV-F-01, VV-F-02), verified at Gate 4. No schema changed. RD-23-03 itself is unchanged.)*
- No code, schema, migration or test is created.

---

## 0. Repository Owner Decision Record — RD-23-03

**Recorded:** 2026-09-25, by direct Repository Owner instruction: "SELECT OPTION D — LAYERED AUTHORITY MODEL." The decision is recorded as stated and is not reinterpreted.

### 0.1 The authority model (as decided)

| Layer | Record | Authority | Answers | Must not |
|---|---|---|---|---|
| **1. Governance registration authority** | The **registering act** / governed registration record | **Governance authority.** It establishes that registration was authorized, the governing decision or act, who or what authority registered the Business Activity, and the governance reason and traceability | "Was this registration authorized, by whom, and why?" | — |
| **2. Runtime execution registration** | The persistent **`bar_registration` table** | **The runtime source queried by execution-time BAR logic** | "Is this canonical Business Activity currently registered for execution?" | Be treated, by the existence of a row alone, as proof that the underlying governance authorization exists |
| **3. Governance catalogue / index** | **`BAR-INDEX.md`** | Human and governance visibility and traceability | "What is registered, and where is its act?" | Serve as the runtime execution lookup source, or become a second runtime authority |
| **4. Reconciliation** | — | The governance registration record and the runtime registration must remain **traceably related** | — | The exact automated reconciliation or enforcement mechanism is **not** decided and is **not** invented here |

### 0.2 What this decision does not authorize (as decided)

- Redesigning BAR registration, or changing `register()` semantics.
- Adding governance-act validation.
- Adding database fields or changing the BAR schema.
- Implementing Workstream E or WP-BAE-001 M2.
- Creating a new authorization service.

**The decision establishes the authority model only.**

### 0.3 ADR requirement: examined, not required by existing rules

- **The rule.** `CLAUDE.md §19` (line 431): "Architecture SHALL NOT evolve during implementation unless explicitly approved through the existing ADR process."
- **The design delegated this question.** `ENTERPRISE-BAR-MECHANISM-DESIGN-AND-IMPLEMENTATION-READINESS.md §6` left the runtime-store question to "a downstream engineering decision within Workstream C/D (§18), not fixed now". It named "Both is the most likely eventual shape" (governance index plus runtime store), and it made "the future registering act … authoritative; the index is … not a competing source of truth".
- **Option D does not change D1–D9.** It selects that anticipated shape within the D2/D7-decided boundary, and introduces no new entity, table, column, API or permission.
- **Precedent.** The same design's §19a (D9) was likewise recorded as an implementation-planning determination without an ADR.
- **Conclusion: an ADR is not required by an existing rule.** The Repository Owner may still elect one.
- **Correction to this document's own analysis.** The §6 "Needs an ADR / constitutional change?" row stated "ADR" for every option, including D. That overstated the requirement as a rule. For D it is at most a recommendation. The row is preserved as written, and this note governs.

### 0.4 Implementation gap (verified by the implementer; recorded for independent review, **not fixed**)

Per the decision's instruction ("If the current implementation has no enforcement linking the registering act to `bar_registration`, record that as a verified implementation gap/finding for independent review rather than silently fixing it"):

| # | Gap | Evidence (source) |
|---|---|---|
| GAP-23-03-1 | **No enforcement links a registering act to a `bar_registration` row.** `registering_act` is a required, non-blank, free-text `String(255)` that is never validated against any act. `register()` has no caller-authority check, `actor_id` is optional, and no router exists. Any in-process caller can create a runtime registration with no governance act. This is the Layer 2 "must not" risk | `services/bar_registration_service.py` (`register`, `_validate_required_fields`); `models/bar_registration.py` (`registering_act`) |
| GAP-23-03-2 | **No reconciliation exists between `bar_registration` and `BAR-INDEX.md`.** The service does not write the index, and no check compares them | `services/bar_registration_service.py` docstring ("This service does NOT populate `BAR-INDEX.md`") |
| GAP-23-03-3 | **Runtime code docstrings still claim the superseded authority.** `models/bar_registration.py` says "this table … is the authoritative persisted record of Business Activity registration". `services/bar_registration_service.py` says "this mechanism … is the authoritative registration act". Both conflict with Layers 1–2. They were **not changed**, because the decision does not authorize modifying BAR runtime code in this pass. *(Synchronized 2026-09-28, ST-12: **closed.** The docstrings were corrected to the layered model under the RO-authorized Gate 3 remediation (Gate 1 CERT-F-03) and verified at Gate 4 (PASS) and Gate 5.)* | Both docstrings |

Classification (severity, remediation now or deferral as debt under `§19.8.5`/`§19.8.7`) belongs to the independent reviewers, not to the implementer.

---

## 1. The Decision

**Question.** Which record is authoritative for a Business Activity's BAR registration, and for what purpose?

The question has two halves that must not be conflated:

| Term | Meaning in this document | Consumer |
|---|---|---|
| **Governance registration** | The act and record by which the platform's governance *decides* that a Business Activity is registered: who authorized it, when, citing which Charter, IMP-REPORT or Work Package, and with which BAR-issued identifier. It is the answer to an auditor's "why is this registered?" | Reviewers, auditors, future IRAs (`IMP-001 §6.2a` Mandatory Context Discovery), the Repository Owner |
| **Runtime execution registration** | The machine-queryable fact, available at invocation time, that a given `BA-NNNNNN` is registered and therefore execution-eligible under D2/D8. It is the answer to the gate's "may this run?" | The BAE (WP-BAE-001 M2: `get_by_identifier`), Workstream E (execution gate), Workstream D (discovery) |

The design already separated these explicitly and left the runtime half undecided (`ENTERPRISE-BAR-MECHANISM-DESIGN-AND-IMPLEMENTATION-READINESS.md §6`): "The Markdown index is the authoritative governance record … whether a database table also exists as the *runtime* mechanism … is a downstream engineering decision within Workstream C/D … not fixed now."

## 2. Why It Is Open: The Current Conflicting Statements (verbatim)

| Source | State | Statement |
|---|---|---|
| Design §6 | Untracked | "The Markdown index is the authoritative governance record (mirroring CBOR)". Also: "the future registering act … is authoritative; the index is a cross-Work-Package summary of those acts, not a competing source of truth" |
| `BAR-INDEX.md §1` | Untracked | "`BAR-INDEX.md` (this document) is authoritative for Business Activity BAR registration". Also: "Each entry's registering act … remains the authoritative registration record; this index is a pointer to it" |
| `models/bar_registration.py` docstring | Untracked | "D7 — this table, not `WPR-001` and not `CBOR-INDEX.md`, is the authoritative persisted record of Business Activity registration" |
| `services/bar_registration_service.py` docstring | Untracked | "D7 (`§0f`) — this mechanism … is the authoritative registration act". Also, the service "does NOT populate `BAR-INDEX.md`", so the index and the table can diverge by design |
| WP-23 Charter §7 and §21 row C | Untracked | Workstream C is "a registering-act convention mirroring the CBOR-ADR pattern", rated "Low risk — **governance-only, no runtime**" |
| `ENTERPRISE-BAR-… §10` | Untracked | BAR's "registration-state field … is the **sole authoritative source** for whether a given Business Activity is execution-eligible" |
| `ROD-ENTERPRISE-BAR` D7 (`§0f`) | Untracked | BAR maintains its own separate authoritative registration record, distinct from `WPR-001`. D7 decides separateness from `WPR-001`, **not** the form of the record |

**Resulting gap.** Three artifacts each claim authority, and the implementation has created a runtime store that no decision has yet placed in the authority model. D7 is cited by both the index and the table, but it does not choose between them.

## 3. Fixed Constraints (already decided; not reopened)

| # | Constraint | Source |
|---|---|---|
| K-1 | BAR scope is the D2 LOCKED minimum: registration, canonical identity, execution-time gate, discovery-exclusivity. Registration state is **two-state** | D2 |
| K-2 | BAR is the canonical identifier authority; the identifier is assigned **at** registration, never earlier | D5 |
| K-3 | BAR's record is separate from `WPR-001` and `CBOR-INDEX.md`; linked by pointer, never merged | D7 |
| K-4 | Registration authority is a **Repository-Owner-authorized registering act**, mirroring CBOR-ADR | Design §14; Charter §7, §14 |
| K-5 | Execution eligibility is derived from BAR registration state alone; discovery must never use scanning or naming conventions | Design §9, §10; `RTA-001 §6.6`; `IMP-001 §6.22.8` |
| K-6 | The BAE *consumes* BAR registration state; Workstream E remains the BAR-side execution-gate authority; the BAE must not duplicate it | RD-M2-04; `ADR-042 §7` |
| K-7 | M2 resolution is organization-independent; BAR is platform-global | RD-M2-03; design §18 |
| K-8 | D8/D9 transitional policy: 21 existing BAs execute pre-registration; future BAs are gated immediately | D8, D9 |

## 4. Repository Evidence for a Layered Model (option D)

- **The design itself names it** (§6): "**Both is the most likely eventual shape** — a governance index for human/audit traceability … plus a runtime-queryable store for the Engine's own actual discovery/gating queries — but this document does not commit to that shape as a decision." Its §18 registration flow ends "record in the index → (optionally) propagate to a runtime store".
- **CBOR precedent (governance half only).** `CBOR-INDEX.md §1`: "Each entry's registering ADR remains the authoritative registration record; this index is a pointer to it." Business Objects have no runtime store, so CBOR is precedent for the act/index relationship, not for runtime.
- **No existing runtime precedent** synchronizes a Markdown governance record with a database table in this repository. `admin-navigation.ts` (code-held navigation substituting for required metadata, recorded as "a documented, temporary deviation") is the nearest analogue of a code/record split, and there it is treated as a deviation.

The evidence therefore **supports option D as a candidate**, and supports its governance half by direct precedent. It supplies **no precedent** for the reconciliation mechanism a layered model would need.

## 5. Options

- **A — `BAR-INDEX.md` authoritative.** The Markdown index is the single source of truth for registration, both governance and runtime. The table either does not exist or is a cache with no authority.
- **B — The registering act authoritative.** Each discrete, RO-authorized act (an ADR/ROD-style document) is the source of truth, exactly as CBOR-ADR is for Business Objects. Both the index and any table are derived pointers or projections.
- **C — `bar_registration` table authoritative.** The persistent runtime table is the single source of truth, as its own docstring claims. The index becomes a human-readable report, and the act becomes a citation string (`registering_act`).
- **D — Layered.** Governance authority and runtime authority are assigned to **different** records, and the relationship between them is defined explicitly. The candidate layering the evidence supports is: the **registering act** is governance-authoritative; **`BAR-INDEX.md`** is the governance pointer or summary; the **`bar_registration` table** is runtime-authoritative *for execution-time lookup only*, and is subordinate to the act, meaning a row may exist only as the effect of a cited act. Variants: D1, the table is written by the act's execution, so the act precedes the row; D2, the row is created first and the act ratifies it (this conflicts with K-4's "act performs registration" and is listed for completeness).

## 6. Comparison

| Dimension | A. `BAR-INDEX.md` | B. Registering act | C. `bar_registration` table | D. Layered (act → index; act → table) |
|---|---|---|---|---|
| **Governance authority** (who decides registration) | Whoever amends the index under §8 of the index | The RO-authorized act (K-4), fully | The caller of `BarRegistrationService.register()`. No authorization is enforced by the code today: there is no router and no caller check, and `actor_id` is optional | The act (as in B) |
| **Runtime authority** (what the gate consults) | The index. It is not machine-queryable in a governed way at run time: parsing Markdown at invocation would be new, fragile tooling, and it lives outside the deployed service | The act. It is not machine-queryable at all; runtime needs a projection | The table: queryable, indexed, transactional | The table, for execution-time lookup only |
| **Source of truth** | One document | N documents (one per act) | One table per hosting database (AuthService today) | Governance: the acts. Runtime: the table. Each authoritative only for its own purpose |
| **Update lifecycle** | Edit and commit the Markdown | Author and approve an act; the index row is added at the same time | A service call inside a transaction; the identifier is issued atomically (B+C implementation) | The act is approved, then `register()` is executed citing the act (populating `registering_act`), then the index row is added citing both the act and the issued `BA-NNNNNN` |
| **Consistency / reconciliation mechanism** | None needed if single-store. If a table also exists, it must be derived from the index, which requires a new parser or loader | Index and table are both projections of acts; both need reconciliation against the acts | None needed if single-store. The index becomes a report, and *drift is permitted by design today* (the service does not write the index) | **Required and currently undefined.** Candidate: a mandatory consistency check that the table's `(identifier, business_activity_reference, owning_capability, owning_work_package, registering_act, is_retroactive)` set equals the index's §3 rows. Where it runs (a test, a Gate 5 RRA check, a startup check) is part of the decision. No such check exists |
| **Auditability** | Git history of one file | Strongest: each act is a reviewed, approved artifact with rationale | Row timestamps, plus the log-based `record_audit` / `publish_event` stand-ins (not an audit platform). No approval evidence in the row beyond a free-text `registering_act` string | Act (approval and rationale) + git history (index) + row timestamp and audit log (runtime). The strongest audit, *if* reconciliation holds |
| **Execution-time lookup** | Not viable without new tooling; parsing Markdown at run time is contrary to the "governed contract" spirit | Not viable | Viable today: `BarRegistrationRepository.get_by_identifier` | Viable: the table. The gate never reads Markdown |
| **Relationship to BA identifier issuance** (D5: issued *at* registration) | Issuance happens elsewhere (the ledger); the index only records the number. The ledger and the index can disagree | The act must cite an identifier, but issuance is performed by code (the ledger). The act and the ledger can disagree unless the act is executed through `register()` | Coherent today: `register()` issues and registers atomically (ledger + row, one flush). This is the only option where D5's "at registration" is structurally enforced | Coherent if D1 ordering holds: the act authorizes, `register()` issues and registers atomically, and the index records the result. An issued-but-unregistered identifier can arise only from `issue_identifier()` used standalone (disclosed in `bar_identifier_service.py`) |
| **Relationship to the BAE** (M2 reads `get_by_identifier`) | The BAE could not consult it; M2's designed surface would be non-authoritative | Same as A | The BAE reads the authoritative record directly | The BAE reads the runtime-authoritative record. Governance authority stays outside the BAE (K-6) |
| **Relationship to Workstream E** (the BAR-side gate authority) | E would need a runtime projection anyway, so it collapses into D | Same as A | E gates on the table; E's policy (D8/D9 transitional carve-out) sits on top | E gates on the table. Whether E also verifies reconciliation status (for example, refusing to honour a row absent from the index) is an E design question this decision would bound |
| **Failure / reconciliation semantics** | Index edited without a table row: the gate cannot see it (if a table exists). Table row without an index entry: an ungoverned registration | Act approved but not executed: registered in governance, not at run time (fails closed: the gate denies). Row without an act: ungoverned | Row inserted without an approved act (any code path calling `register()`): **registered and execution-eligible with no governance act**. This is the fail-open direction for governance. The CHECK and FK constraints protect data shape, not authority | Row without an act or index entry: detected by reconciliation; its runtime effect depends on whether E treats unreconciled rows as eligible (fail-open) or ineligible (fail-closed); undecided. Act and index without a row: the gate denies (fail-closed) |
| **Needs an ADR / constitutional change?** | ADR (it contradicts the design's "runtime store" direction and forecloses runtime lookup). Likely removal or demotion of the table (a scope change to built code) | ADR, plus the runtime question is still unanswered. Collapses into D for runtime | ADR. It contradicts design §6 ("Markdown index is the authoritative governance record") and Charter §21 row C ("governance-only, no runtime"). It demotes `BAR-INDEX.md §1`. The unenforced-authority gap in `register()` must be closed (who may call it) | ADR, ratifying the layering (the design's own "most likely shape"), defining reconciliation, and settling the Charter §21 row C wording. The lowest contradiction with existing text, but the most new mechanism |
| **Effect on the built A–C code** | The table is unused or removed | The table is re-framed as a projection | None to the code. Docstrings already claim this; the index and design text change | Docstrings in `bar_registration.py` and `bar_registration_service.py` ("the authoritative …") would need narrowing to "runtime-authoritative, subordinate to the act". The reconciliation mechanism is new work, placed in the tranche or deferred as debt |

## 7. Observations (for the Repository Owner; not a selection)

- **Only C and D can serve execution-time lookup** without new parsing tooling. A and B each leave WP-BAE-001 M2's designed surface (`get_by_identifier`) and Workstream E with no authoritative runtime source. In practice they collapse into D for runtime.
- **The most material risk in C, as built, is authority, not data integrity.** Any code path calling `register()` creates an execution-eligible registration, and nothing in code requires a governance act. That is the fail-open direction relative to K-4. D inherits the same exposure unless reconciliation, or an authorization check on `register()`, closes it.
- **D is the design's own named "most likely shape".** It is also the option most consistent with the current texts taken together (design §6/§10, the index §1 pointer wording, CBOR precedent). Its cost is a reconciliation mechanism that has no repository precedent.
- **This decision bounds Gate 1's check G1-2** (`IRA-WP-23-AC §9.1`): whether the runtime table is within the Charter's Workstream C authorization depends on which option is chosen.
- **Interaction with RD-M2-02** (`ROD-BAE-001-M2-…`). That decision asks the same structural question for the identifier → implementation binding: documented record versus persistent or code-held store. Deciding RD-23-03 first may inform RD-M2-02. This document does not link them.
- **The A–C tranche can close under any option**, but only after the chosen option's text corrections are applied, because the current docstrings and `BAR-INDEX.md §1` contradict every option except, partially, D. Under A or B, closure also requires a disposition of the built table.

## 8. What This Document Does Not Do

- It selects no option and records no ranking.
- It creates no ADR and modifies no ADR, design document, Charter, `BAR-INDEX.md` authority text or code docstring.
- It creates no reconciliation mechanism, check, table, migration, router, adapter or test.
- It registers no Business Activity and issues or assigns no identifier.
- It does not touch Workstreams D or E or WP-BAE-001 M2.
- Nothing is staged, committed or pushed.

---

~~**RD-23-03 — OPEN — RO decision required.**~~

**RD-23-03 — DECIDED (2026-09-25) — Option D, Layered Authority Model (§0).**
