# ROD-ENTERPRISE-BAR — Enterprise Business Activity Registry Governance Decision Preparation

**Document type:** Repository Owner decision-preparation record — began as a **preparation** record presenting evidence-backed options without selecting one; now records the Repository Owner's explicit selection of all seven original `§14` decisions (§0, §0b, §0c, §0d, §0e, §0f) plus one further decision, D8, that emerged during the consolidated BAR mechanism design stage (§0g) — not one of the original seven questions, but the same class of Repository Owner decision, arising directly from a blocking ambiguity the design stage itself surfaced and declined to resolve by inference (`ENTERPRISE-BAR-MECHANISM-DESIGN-AND-IMPLEMENTATION-READINESS.md §21`/`§22`, Open Issue 1). Same class and sequence as `ROD-C024-BAR_Treatment_Decision_Preparation.md`'s own preparation-then-decision pattern.

**Prepared:** 2026-09-19, per direct Repository Owner instruction, transforming `BAR_ENTERPRISE_MECHANISM_DECISION_INVESTIGATION.md §14`'s seven evidence-backed questions into a formal decision-preparation artifact.

**Governing precedent for this document's own format:** `ROD-C024-BAR_Treatment_Decision_Preparation.md` (capability-scoped BAR decision preparation, C-024 BA-01 only) and `ROD-C022-B_Lifecycle_and_BAR_Decisions.md` (C-022 BA-01 only). This document is the **enterprise-scoped** counterpart those two documents each explicitly disclosed needing (`ADR-037 §Decision item 5`: "a future enterprise-level decision may establish the canonical BAR mechanism"; `ROD-C024-BAR §0`: "deferred pending a future enterprise-level BAR-mechanism decision"). It does not reopen, alter, or reinterpret either of those two capability-scoped decisions.

**Status:** Decision 1 — **DECIDED — Option A selected** (recorded 2026-09-19, §0 below). Decision 2 — **DECIDED — Option A (LOCKED minimum scope) selected** (recorded 2026-09-20, §0b below). Decision 3 — **DECIDED — Option A (retroactive registration, all 21 rows) selected** (recorded 2026-09-20, §0c below). Decision 5 — **DECIDED — Authority: Option A (BAR is canonical authority); Timing: at BAR registration** (recorded 2026-09-20, §0d below). Decision 6 — **DECIDED — Option A (no `IMP-001` amendment required)** (recorded 2026-09-20, §0e below). Decision 7 — **DECIDED — Option B (separate BAR registration index/registry, distinct from `WPR-001`)** (recorded 2026-09-20, §0f below). Decision 8 — **DECIDED — Option B (transitional gate — existing Business Activities continue executing during a governed transition; only future BAs are gated immediately)** (recorded 2026-09-21, §0g below). Decision 4 — **MOOT** (contingent on Option B, which was not selected for Decision 1). **All eight decisions are now resolved.** No BAR mechanism has been designed or built; no Business Activity has been registered; no identifier has been assigned — the next governed stage (BAR implementation) requires separate authorization, not begun here.

**Classification key:** `[LOCKED]` — verbatim constitutional text. `[ACTIVE]` — verbatim from a Status: Active document (`IMP-001`). `[FACT]` — directly verified repository fact. `[PRECEDENT]` — a prior Repository Owner decision, cited for procedure/comparison only, never as enterprise policy. `[INFERENCE]` — a conclusion drawn from combining sources, flagged as such. `[RO DECISION REQUIRED]` — an open question requiring Repository Owner resolution. `[RO DECISION]` — a Repository Owner decision now recorded.

---

## 0. Repository Owner Decision — Decision 1 (Recorded 2026-09-19)

**`[RO DECISION]` Decision 1 is answered: OPTION A — AUREX establishes a canonical enterprise Business Activity Registry (BAR) mechanism.**

Recorded 2026-09-19, per direct Repository Owner instruction, following presentation of Decision 1's own root-decision consequences (§6 below, both options presented with symmetric, non-evaluative structure) without either option being inferred, assumed, or pre-selected by the preparing session. The Repository Owner selected Option A explicitly, in response to a direct presentation of both options' sourced consequences — not inferred from the LOCKED obligation's existence, the absence of a current mechanism, the C-021/C-022 precedents, or C-024 D10, consistent with this document's own governing instruction not to draw that inference.

**Exact scope of what D1 decides:**
- AUREX establishes a canonical enterprise BAR mechanism/governance capability, discharging the enterprise-level branch of the `SD-002-034`/`COM-001-060`/`PLT-001-030`/`GRC-001-070` obligation `§14`'s Decision 1 named.
- This opens, as the next governed stage, preparation of Decisions 2 (BAR scope), 3 (retroactive vs. prospective registration), 5 (Business Activity Identifier authority), 6 (`IMP-001 §6.22` amendment question), and 7 (`WPR-001` vs. separate index relationship) — each to be presented and decided on its own, in the same non-evaluative, no-mechanism-design manner this document's own §7 already used.

**Exact scope of what D1 does NOT decide (restated, not expanded, from §6's own "What it would NOT authorize" row):**
- Does **not** itself authorize implementation of any kind.
- Does **not** itself authorize database/schema design, APIs, or runtime architecture.
- Does **not** itself authorize retroactive registration of any specific existing Business Activity — that is Decision 3, separately open.
- Does **not** itself register any Business Activity or assign any `BA-NNNNNN` identifier.
- Does **not** modify `IMP-001`, `COM-001`, `CMD-001`, `SD-002`, `PLT-001`, `GRC-001`, or `CLAUDE.md`.
- Does **not** specify any BAR implementation design (schema, API, runtime class, service topology, storage, or workflow) — that remains future, separately governed engineering work.
- Does **not** alter, reopen, or reinterpret `C-024 D10` (`ROD-C024-BAR_Treatment_Decision_Preparation.md §0`). `D10` remains **DECIDED — Option A — deferred**, scoped to C-024 BA-01 only. D10 was reached independently, on C-024's own governing text, before this enterprise decision existed, and is not converted into an enterprise BAR policy, retroactively re-characterized, or treated as a precedent for this decision (or vice versa) by this recording.
- Does **not** pre-decide Decisions 2, 3, 5, 6, or 7 — each remains open, to be prepared and presented as its own governed decision.
- Does **not** trigger Decision 4, which is now moot (contingent on Option B, not selected).

**Next governed stage:** Preparation of Decisions 2, 3, 5, 6, and 7, each as its own decision-preparation exercise — not begun by this recording, and not to be begun automatically without separate authorization.

---

## 0b. Repository Owner Decision — Decision 2 (Recorded 2026-09-20)

**`[RO DECISION]` Decision 2 is answered: OPTION A — the canonical enterprise BAR is scoped to the LOCKED minimum.**

Recorded 2026-09-20, per direct Repository Owner instruction, following presentation of Decision 2's own consequences (§7 "Decision 2" subsection below, D2.7/D2.8, both options presented with symmetric, non-evaluative structure) without either option being inferred, assumed, or pre-selected by the preparing session. The Repository Owner selected Option A explicitly, in response to a direct presentation of both options' sourced consequences.

**Exact scope of what D2 decides:**
- The canonical enterprise BAR, once built (per D1's own future governed stage), is scoped to the four responsibilities this document's D2.5 independently found to be LOCKED: (1) Business Activity cataloguing/registration (`SD-002-034`, `COM-001-060`/`PLT-001-030`/`GRC-001-070`); (2) canonical Business Activity identity, format only (`SD-002-004`); (3) execution-time registration gating (`COM-001-005`/`PLT-001-004`/`GRC-001-008`); (4) discovery exclusively through the Business Activity Registry (`RTA-001 §6.6`, LOCKED, subject to D2.5's own practical-trigger caveat).
- Every other `IMP-001 §6.22` responsibility (full attribute/schema set beyond Identity, status/lifecycle model, version management, dependency management, registry governance workflow, observability, and the full seven-item validation checklist) is **excluded** from the enterprise BAR's decided scope and **remains governed by its existing mechanism** (design-time BAC/CBAM for content, direct `record_audit`/`publish_event` for audit, direct FastAPI dependency injection for authorization) **unless separately decided** in a future governed stage.

**Exact scope of what D2 does NOT decide (restated, not expanded, from D2.14/§7's own framing):**
- Does **not** decide Business Activity Identifier format, issuer, or assignment timing — Decision 5, separately open.
- Does **not** decide retroactive vs. prospective registration for the 20+ already-certified Business Activities — Decision 3, separately open.
- Does **not** decide whether `IMP-001 §6.22` itself requires amendment to reflect this narrower adopted scope — Decision 6, separately open. (D2.7 already noted a minimal-scope selection makes a `§6.22` amendment *more likely relevant* as a future question — this recording does not resolve that question, only flags that D6 is now the live form of it.)
- Does **not** decide whether `WPR-001` gains a BAR column or a separate `BAR-INDEX.md` is created — Decision 7, separately open.
- Does **not** itself authorize implementation, schema/API/runtime design, or any specific technical workflow for even the four LOCKED-minimum responsibilities — that remains future, separately governed engineering work.
- Does **not** register any Business Activity or assign any `BA-NNNNNN` identifier.
- Does **not** modify `IMP-001`, `COM-001`, `CMD-001`, `SD-002`, `PLT-001`, `GRC-001`, `RTA-001`, or `CLAUDE.md`.
- Does **not** alter, reopen, or reinterpret `C-024 D10` (`ROD-C024-BAR_Treatment_Decision_Preparation.md §0`). `D10` remains **DECIDED — Option A — deferred**, scoped to C-024 BA-01 only, and is not converted into an enterprise BAR exemption, policy, or precedent by this recording.
- Does **not** mark any BAR mechanism as built or implemented — D1/D2 together establish *that* AUREX will build one and *what minimum scope* it must have; no mechanism exists yet, and none is created by this recording.

**Next governed stage:** Preparation of Decisions 3, 5, 6, and 7, each as its own decision-preparation exercise — not begun by this recording, and not to be begun automatically without separate authorization.

---

## 0c. Repository Owner Decision — Decision 3 (Recorded 2026-09-20)

**`[RO DECISION]` Decision 3 is answered: OPTION A — BAR registration applies retroactively to all Business Activities already existing in the repository.**

Recorded 2026-09-20, per direct Repository Owner instruction, following presentation of Decision 3's own three source-supported options (§7 "Decision 3" subsection below, D3.6/D3.7/D3.8, presented with symmetric, non-evaluative structure) without any option being inferred, assumed, or pre-selected by the preparing session. An initial response to the presentation repeated the task's own instructions rather than selecting an option; per this document's own governing "do not infer the Repository Owner's choice" discipline, no selection was recorded from that response — the option was re-presented and the Repository Owner then selected Option A explicitly.

**Exact scope of what D3 decides:**
- BAR registration (per D1's establishment and D2's decided LOCKED-minimum scope — cataloguing/registration, canonical identity, execution-time gate, discovery-exclusivity) applies to all 21 Business Activity rows identified in this document's own D3.4 inventory: the nineteen implemented/certified Work Packages (WP-01, 02, 03 [partial], 04–12, 14–21) and WP-22/C-024 BA-01 (chartered, CBOR-registered as `BIA-000001`, implementation NOT STARTED).
- This establishes, as a matter of enterprise governance direction, that the historical absence of BAR treatment across nineteen Work Packages (investigation §7's own "undiscovered, not satisfied or exempted" finding) is to be eventually remedied by registration, rather than left as a permanent, unaddressed gap.

**Exact scope of what D3 does NOT decide (restated, not expanded, from D3.6's own framing):**
- Does **not** itself perform any registration — no Business Activity in the D3.4 inventory is registered by this recording; the table's own "Existing BAR registration: None" column is unchanged by this decision.
- Does **not** itself assign any `BA-NNNNNN` identifier to any of the 21 rows — identifier assignment authority and timing remain Decision 5, separately open, and this recording does not pre-decide it.
- Does **not** itself specify transition sequencing, retrofit methodology, or which source (`IMP-REPORT-WP-XX`, Charter, or other) is authoritative for reconstructing each historical BA's registration content — D3.6 flagged these as open methodological questions, and none is resolved here.
- Does **not** itself resolve whether the execution-time gate (part of D2's decided scope) applies to an existing BA's *continued* execution before its own retroactive registration completes, or only once retrofitted — D3.11's own unresolved question is **not settled** by selecting Option A; retroactivity of *registration* and the *execution-gate's own temporal reach* remain textually distinct questions, and this recording resolves only the former.
- Does **not** reopen, resolve, or characterize as a "reopening" the `CLOSED — CERTIFIED` status of any of the nineteen already-certified Work Packages — whether a future retroactive-registration act is itself treated as reopening those closures is not decided by this recording (D3.6's own unresolved flag on this point stands).
- Does **not** decide Decision 5 (identifier authority/timing), Decision 6 (`IMP-001 §6.22` amendment), or Decision 7 (`WPR-001` vs. separate `BAR-INDEX.md`) — each remains open, and D3's own execution depends on at least Decision 5 being separately resolved before any actual identifier assignment can occur (D3.10's own dependency finding, unchanged).
- Does **not** alter, reopen, or reinterpret `C-024 D10` (`ROD-C024-BAR_Treatment_Decision_Preparation.md §0`). `D10` remains **DECIDED — Option A — deferred**, scoped to C-024 BA-01 only. BA-01 is **not automatically registered** by this D3 recording — per D3.4's own category-C placement and D3.13's own finding, BA-01 is NOT STARTED and therefore falls outside the "already-implemented" population this Option A decision addresses; it would be governed prospectively (as any not-yet-implemented BA is) regardless of D3's outcome, unless and until a separate, later, explicit action changes that.
- Does **not** create a migration, retrofit plan, runtime exception, or grandfathering mechanism — none is designed by this recording.
- Does **not** modify `COM-001`, `CMD-001`, `IMP-001`, `SD-002`, `PLT-001`, `GRC-001`, `RTA-001`, `CLAUDE.md`, `WPR-001`, or `CBOR-INDEX.md`.

**Transitional implication, disclosed not resolved:** selecting Option A means the eventual retroactive-registration exercise D3.6 described (identity + registration record per BA, per D2's own decided minimum scope) is the enterprise governance direction — but *when* and *how* that exercise occurs, and whether it requires reopening any closed Work Package's own certification, are questions this recording does not answer and defers to the future governed stage (Decision 5, and any subsequent implementation-planning decision this document does not anticipate in detail).

**Relationship to D2:** D2's own LOCKED-minimum scope (identity + registration record + execution gate + discovery, excluding the fuller `§6.22` attribute set) directly bounds what the Option A retroactive exercise must eventually reconstruct for each of the 21 rows — a materially smaller undertaking than a full-`§6.22`-scope retroactive exercise would have been, consistent with D3.6's own scope-dependency finding.

**Next governed stage:** Preparation of Decisions 5, 6, and 7, each as its own decision-preparation exercise — not begun by this recording, and not to be begun automatically without separate authorization.

---

## 0d. Repository Owner Decision — Decision 5 (Recorded 2026-09-20)

**`[RO DECISION]` Decision 5 is answered on both of its dimensions: Authority — OPTION A, BAR is the canonical Business Activity Identifier authority. Timing — at BAR registration.**

Recorded 2026-09-20, per direct Repository Owner instruction, following presentation of D5's own two dimensions as separate selectable sets (§7 "Decision 5" subsection below, D5.8/D5.9, both authority options and all source-supported timing points presented with symmetric, non-evaluative structure) without either dimension being inferred, assumed, or pre-selected by the preparing session, and without inferring either selection from precedent or from the combination most convenient for implementation. The Repository Owner selected both dimensions explicitly.

**Exact scope of what D5 decides:**
- **Authority:** BAR itself (once built, per D1's own future governed stage, at D2's own decided LOCKED-minimum scope) is the canonical source of truth for the Business Activity Identifier — BAR creates and controls the identifier internally; no separate, external registering act (the Option B alternative, mirroring the CBOR-ADR pattern) is established.
- **Timing:** the identifier is assigned at BAR registration — the point `IMP-001 §6.22.7` already ties to the execution gate, per D5.9's own finding that this is "the most source-direct option." This is consistent with, and satisfies, the one constitutional floor `COM-001-005` establishes (identity must exist before first execution) without committing to any of the other, source-unconfirmed candidate points (creation, Chartering, WP registration, implementation authorization).

**Exact scope of what D5 does NOT decide (restated, not expanded, from D5.8/D5.9's own framing):**
- Does **not** create, reserve, or assign any actual `BA-NNNNNN` identifier to any Business Activity, including any of D3's 21 retroactive rows or C-024 BA-01.
- Does **not** register any Business Activity.
- Does **not** specify any technical mechanism for how BAR would internally generate the identifier (sequence, database structure, service) — that remains future, separately governed engineering work, per D5.8's own "implementation consequence" finding.
- Does **not** decide Decision 6 (whether `IMP-001 §6.22` requires amendment) or Decision 7 (`WPR-001` vs. separate `BAR-INDEX.md`) — both remain open. D5.13's own dependency finding is reaffirmed: because Option A (not Option B) was selected, D5's own outcome has **no** dependency on D7 being resolved first, and D7's own eventual resolution is unaffected by this recording.
- Does **not** modify `COM-001`, `CMD-001`, `IMP-001`, `SD-002`, `PLT-001`, `GRC-001`, `RTA-001`, `CLAUDE.md`, `WPR-001`, or `CBOR-INDEX.md`.
- Does **not** alter, reopen, or reinterpret `C-024 D10` (`ROD-C024-BAR_Treatment_Decision_Preparation.md §0`). `D10` remains **DECIDED — Option A — deferred**, scoped to C-024 BA-01 only. **No Business Activity Identifier is created for BA-01 by this recording** — BA-01 remains NOT STARTED and would only become eligible to receive an identifier once it actually reaches BAR registration, a future contingency this recording does not create or accelerate.
- Does **not** perform, sequence, or plan the D3 retroactive-registration exercise for the 21 existing rows — it establishes only that, once that exercise occurs, BAR itself (not a separate registering act) will be the authority, and registration itself (not an earlier point) will be the trigger. The exercise's own sequencing (single omnibus act vs. per-BA, order, timing of the historical backfill) remains unresolved future implementation-planning work, as D5.10 already flagged.

**D3 interaction, now clarified (not newly decided):** D3's own 21-row retroactive population will each receive its identifier from BAR itself, at the point each row is individually registered into BAR — not from any separate registering act, and not before BAR registration occurs. This does not by itself schedule or perform that registration.

**Next governed stage:** Preparation of Decisions 6 and 7, each as its own decision-preparation exercise — not begun by this recording, and not to be begun automatically without separate authorization.

---

## 0e. Repository Owner Decision — Decision 6 (Recorded 2026-09-20)

**`[RO DECISION]` Decision 6 is answered: OPTION A — No `IMP-001 §6.22` amendment is required.**

Recorded 2026-09-20, per direct Repository Owner instruction, following presentation of D6's own two options (§7 "Decision 6" subsection below, D6.13, both presented with symmetric, non-evaluative structure covering thirteen consequence dimensions) without either option being inferred, assumed, or pre-selected by the preparing session, and without inferring the selection from D2, D5, source hierarchy, implementation convenience, documentation quality, or prior precedent. The Repository Owner selected Option A explicitly.

**Exact scope of what D6 decides:**
- The enterprise BAR (established per D1, scoped per D2 to the LOCKED minimum — cataloguing/registration, canonical identity, execution-time gate, discovery-exclusivity) owns exactly those four responsibilities. `IMP-001 §6.22`'s own broader text (the eight-of-nine `§6.22.3` Engine functions, the seven-item `§6.22.7` validation checklist, `§6.22.5`/`§6.22.6`'s fuller attribute schema beyond Identity, `§6.22.9`–`§6.22.13`'s status/version/dependency/governance/observability provisions) remains `IMP-001`'s own broader implementation-methodology content, unamended, and is **not** to be read as silently expanding the enterprise BAR's own decided LOCKED-minimum scope.
- `§6.22` is read, per this recording, the same way `RTA-001`'s own fuller runtime design is already read in actual repository practice (per `WP-RTA-001`'s own narrow, incremental realization) — as an aspirational engineering target, not as a statement of the enterprise BAR's own current, decided scope.

**Exact scope of what D6 does NOT decide (restated, not expanded, from D6.13's own Option A framing):**
- Does **not** change D2's own decided scope — the four LOCKED-minimum responsibilities remain exactly as D2 recorded them.
- Does **not** eliminate, retire, or invalidate `§6.22`'s own broader methodology — it remains available as future engineering guidance, unamended, exactly as written.
- Does **not** authorize any BAR implementation, schema, API, runtime design, or mechanism build.
- Does **not** settle Decision 7 (`WPR-001` vs. separate BAR registration index) — it remains open and unaffected by this recording.
- Does **not** register any Business Activity or assign any `BA-NNNNNN` identifier.
- Does **not** modify `IMP-001`, `COM-001`, `CMD-001`, `SD-002`, `PLT-001`, `GRC-001`, `RTA-001`, `CLAUDE.md`, `WPR-001`, or `CBOR-INDEX.md` — no source document is amended by this recording, consistent with Option A's own text (no amendment).
- Does **not** alter, reopen, or reinterpret `C-024 D10` (`ROD-C024-BAR_Treatment_Decision_Preparation.md §0`). `D10` remains **DECIDED — Option A — deferred**, scoped to C-024 BA-01 only, unaffected by this recording.
- Does **not** promote any of `§6.22`'s broader (non-D2) responsibilities to LOCKED status, and does **not** demote any of the four D2-decided responsibilities to optional status — the BAR/`IMP-001` boundary established in D6.4/D6.5 (this section, and D2.5/D2.6 before it) remains exactly as previously found.

**D2/D3/D5 interaction, restated not altered:** D2's own scope, D3's own retroactive-registration direction, and D5's own identity-authority/timing decision are each unaffected by this recording — D6 answers only the separate question of whether `§6.22`'s *text* needed correcting to match those already-recorded decisions, and answers it "no."

**Next governed stage:** Preparation of Decision 7, as its own decision-preparation exercise — not begun by this recording, and not to be begun automatically without separate authorization. This is the final enterprise BAR decision remaining open.

---

## 0f. Repository Owner Decision — Decision 7 (Recorded 2026-09-20)

**`[RO DECISION]` Decision 7 is answered: OPTION B — the enterprise BAR maintains its own authoritative Business Activity registration record, separate from `WPR-001`.**

Recorded 2026-09-20, per direct Repository Owner instruction, following presentation of D7's own two options (§7 "Decision 7" subsection below, D7.6/D7.7, presented with symmetric, non-evaluative structure covering seventeen consequence dimensions) without either option being inferred, assumed, or pre-selected by the preparing session, and without inferring the selection from D1, D2, D5, D6, prior precedent, or implementation convenience. The Repository Owner selected Option B explicitly. **This is the seventh and final of the seven `§14` enterprise BAR decisions — all seven are now recorded.**

**Exact scope of what D7 decides:**
- The enterprise BAR's own future registration record is **authoritative** for Business Activity registration, structurally separate from `WPR-001` — mirroring, but not derived from, `CBOR-INDEX.md`'s own existing separation from `WPR-001` for Business Objects (`ONT-001 §2`'s own "two distinct registries, neither a subset of the other" finding, extended by this decision to a third, BA-centric register).
- `WPR-001` remains authoritative for Work Package → Capability assignment only, exactly as its own `§1` Purpose statement already declares — its own scope is **not** expanded by this recording.
- The future BAR registration record and `WPR-001` are **linked, not merged** — a Business Activity's own future BAR entry would cross-reference its owning WP's `WPR-001` row (and Charter, and `IMP-REPORT`), and vice versa, without either artifact absorbing the other's own authority.

**Exact scope of what D7 does NOT decide (restated, not expanded, from D7.7's own framing):**
- Does **not** create `BAR-INDEX.md` or any other physically-named artifact — the *decision* that a separate index will exist is recorded; the artifact itself is not created here.
- Does **not** design any database, schema, API, or runtime mechanism for that future index — purely future, separately governed engineering work.
- Does **not** register any Business Activity or assign any `BA-NNNNNN` identifier to any of D3's 21 retroactive rows, or to any future Business Activity.
- Does **not** change **who** issues the identifier — D5's own decision (BAR is the canonical identifier authority, at BAR registration) is unaffected; D7 only fixes **where** that already-decided authority's own output is recorded.
- Does **not** reopen or change D6 — `IMP-001 §6.22` remains unamended; this recording does not revisit that decision, though it notes (per D7.11's own finding) that a separate index makes `§6.22`'s own "the Registry" language read more literally as a dedicated artifact, a fact for any future D6 revisit, not decided here.
- Does **not** modify `WPR-001`, `CBOR-INDEX.md`, `COM-001`, `CMD-001`, `IMP-001`, `SD-002`, `PLT-001`, `GRC-001`, `RTA-001`, or `CLAUDE.md`.
- Does **not** alter, reopen, or reinterpret `C-024 D10` (`ROD-C024-BAR_Treatment_Decision_Preparation.md §0`). `D10` remains **DECIDED — Option A — deferred**, scoped to C-024 BA-01 only. **BA-01 is not automatically registered** by this recording — it remains NOT STARTED, and `BIA-000001`/WP-22/the Charter are all unaffected.
- Does **not** begin the retroactive-registration exercise for D3's 21 existing rows — each would, per Option B's own consequence table (D7.12), eventually require a new per-Business-Activity entry in the future separate index, cross-referencing its own existing `WPR-001` row — but no such entry is created now.
- Does **not** begin BAR mechanism design, implementation, or any consolidated BAR build. Per this task's own explicit instruction, the next governed stage after D7 is a **separately authorized** consolidated BAR mechanism design/implementation-preparation stage — this recording does not initiate it.

**Enterprise BAR decision chain, now complete (at the time of §0f):** D1 = ACCEPTED (Establish). D2 = ACCEPTED (LOCKED minimum scope). D3 = ACCEPTED (retroactive registration, all 21 rows). D4 = MOOT. D5 = ACCEPTED (BAR is identifier authority, at BAR registration). D6 = ACCEPTED (no `IMP-001` amendment required). D7 = ACCEPTED (separate BAR registration index, distinct from `WPR-001`). **All seven `§14` questions were resolved as of this point.** The subsequent consolidated BAR mechanism design stage then surfaced one further, previously-undiscovered decision (D8, §0g below), not one of the original seven.

---

## 0g. Repository Owner Decision — Decision 8 (Recorded 2026-09-21)

**`[RO DECISION]` Decision 8 is answered: OPTION B — a transitional gate. Existing Business Activities continue executing during a governed retroactive-registration transition; only newly introduced/future Business Activities are gated immediately upon BAR becoming operational.**

**D8 decision statement:** Given that D2 makes the execution-time registration gate part of BAR's own decided minimum scope, and D3 makes all 21 existing Business Activities eventually subject to retroactive registration, what happens to those 21 rows' own execution *before* that retroactive registration is individually completed — does the gate apply to them immediately once BAR exists, or only once each is transitioned/registered? **D8 is distinct from D3** — D3 decided *that* registration eventually occurs; D8 decides what happens to execution *before* it does.

**Why D8 was required:** the consolidated BAR mechanism design (`ENTERPRISE-BAR-MECHANISM-DESIGN-AND-IMPLEMENTATION-READINESS.md §21`/`§22`) identified this as the single blocking open issue preventing Workstreams D (discovery) and E (execution gate) from being built safely — building the gate without an answer risked either an undisclosed grandfathering rule (if built to silently exempt the 21 rows) or an undisclosed breaking change (if built to silently interrupt their production-shaped, already-certified execution).

**Source-first re-verification performed for this recording, re-confirming (not re-deriving) the same silence already found at D3.5/D3.11/D6.9/§21 of the design document:** `COM-001-005` ("No commercial Business Activity shall be executed until registered in the BAR"), `COM-001-060` ("once implemented"), `SD-002-034`, `PLT-001-030`, `GRC-001-070`, `RTA-001 §6.6`, and `IMP-001 §6.22`'s own execution-gate/discovery text (`§6.22.7`, `§6.22.8`, `§6.22.15`) were each re-checked, again, for any language addressing transition, grandfathering, migration, effective date, or pre-existing execution. **None exists.** The gate is stated unconditionally, but no source states *when* that condition begins to apply relative to a Business Activity that was already executing before BAR existed. This silence is not resolved by historical precedent, implementation convenience, assumption, or analogy — consistent with every prior instruction in this decision chain.

**Exact scope of what D8 decides:**
- The BAR execution-time gate (D2's own decided scope) applies **immediately** to newly introduced/future Business Activities, from the moment BAR becomes operational.
- The BAR execution-time gate does **not** apply to any of D3's 21 existing Business Activity rows until each is individually, retroactively registered — those rows continue executing uninterrupted in the interim.
- This is a **governed transition state**, not a permanent exemption: each of the 21 rows remains fully subject to D3's own registration obligation, which remains outstanding and undischarged until actually performed.

**Exact scope of what D8 does NOT decide:**
- Does **not** set a specific transition duration or deadline — no date, quarter, or Work Package milestone is fixed by this recording; per this task's own instruction not to invent a specific duration, none is invented.
- Does **not** fix the eventual enforcement mechanism for closing the transition (e.g., whether gating switches on per-row as each is registered, or via a single future cutover date for all remaining unregistered rows) — this remains open, future implementation-planning work.
- Does **not** change D3 — all 21 rows remain subject to eventual registration exactly as D3 already decided; D8 only addresses the execution consequence in the interim.
- Does **not** change D2 — the execution gate remains part of BAR's own decided LOCKED-minimum scope; D8 only fixes when it takes effect for the 21 pre-existing rows specifically.
- Does **not** change D5 — BAR remains the identifier authority, at BAR registration, unaffected.
- Does **not** create, register, or modify any Business Activity, assign any identifier, or begin any retrofit.
- Does **not** modify `COM-001`, `CMD-001`, `IMP-001`, `SD-002`, `PLT-001`, `GRC-001`, `RTA-001`, `CLAUDE.md`, `WPR-001`, or `CBOR-INDEX.md`.
- Does **not** alter, reopen, or reinterpret `C-024 D10` (`ROD-C024-BAR_Treatment_Decision_Preparation.md §0`). `D10` remains **DECIDED — Option A — deferred**, scoped to C-024 BA-01 only, unaffected. BA-01 is not currently executing, so D8's own transitional-gate policy has no present effect on it; once BA-01 is actually implemented (a future, separately authorized act), it would be a **future** Business Activity relative to whenever BAR actually goes live, and would therefore be gated immediately from its own first execution under D8's own Option A branch for future BAs — not treated as one of the 21 "existing" rows this transition covers.
- Does **not** begin BAR implementation of any kind (§ Step 7 boundary, this task).

**Existing Business Activity consequence, by row (re-confirmed against the actual 21-row inventory, `ROD-ENTERPRISE-BAR §D3.4`/design document §11), no modification performed:**

| Item | Consequence under D8 (Option B) |
|---|---|
| C-040 / WP-16 | Continues executing uninterrupted; remains subject to eventual D3 registration |
| C-023 / WP-17 | Same |
| WP-18 (Approval Authority runtime binding) | Same |
| C-132 / WP-19 | Same |
| C-021 / WP-20 | Same — `CLOSED — CERTIFIED — RELEASE-READY` status and continued execution both preserved; `ADR-037`'s own prior BAR deferral is unaffected |
| C-022 / WP-21 | Same — `ROD-C022-B D10`'s own prior BAR deferral is unaffected |
| C-024 / WP-22 | Not currently executing (NOT STARTED) — D8 has no present effect; `C-024 D10` unaffected |
| All other 14 of the 21 rows (WP-01–15, minus WP-13 which is not a chartered BA) | Continue executing uninterrupted; remain subject to eventual D3 registration |

**No certified Work Package is reopened, interrupted, or modified by this recording.**

**Next governed stage:** BAR implementation (Workstreams A–H, per the design document's own §18/§19) may now proceed toward a future implementation authorization for Workstreams A/B/C/F/G unconditionally, and for Workstreams D/E (discovery, execution gate) under D8's own now-decided transitional policy specifically (immediate gate for future BAs; deferred gate for the 21 existing rows pending their own individual registration) — not begun by this recording, and not to be begun automatically without separate authorization.

---

## 1. Executive Purpose

This document exists to let the Repository Owner decide the enterprise-level Business Activity Registry (BAR) governance question **without this session silently deciding it**. It does not select Option A or Option B for the primary question, does not rank or score any option, does not design a BAR mechanism, does not assign a Business Activity Identifier, does not register any Business Activity, and does not modify `C-024 D10` or any other capability-scoped BAR decision.

It transforms `BAR_ENTERPRISE_MECHANISM_DECISION_INVESTIGATION.md §14`'s seven questions into a structured decision set: each question's exact governance language, why it is required, its authoritative source basis, its dependency on the other six, and — where the sources genuinely support more than one path — the options and their factual consequences, stated without evaluation.

---

## 2. Current Authoritative BAR State (as of 2026-09-19, independently re-verified for this document)

- A genuine, `[LOCKED]` enterprise-wide obligation exists: every Business Activity satisfying `SD-002-034` is to be catalogued in a Business Activity Registry (BAR), and no commercial Business Activity is to be **executed** until so registered (`COM-001-005`). The identical obligation is independently restated for the platform (`PLT-001-004`/`-030`) and governance (`GRC-001-008`/`-070`) domains, and confirmed as universal, not domain-specific, by `OPM-001-013`.
- **No BAR mechanism exists anywhere in this repository** — no registry file, no database table, no identifier ever assigned, no runtime lookup, no validation, no Business Activity Engine. Confirmed independently for this document by re-running the repository-wide search (`BAR-INDEX`, `Business_Activity_Registry`, `BA-NNNNNN` token, `BusinessActivityEngine`/`business_activity_registry` code identifiers) — zero hits beyond the illustrative `BA-000089` citations in constitutional text and the two disclosed code-comment absences (`Backend/Services/AIService/schemas/conversation.py:37`, `Backend/Runtime/AuthorizationEngine/authorization/models.py:51`).
- `IMP-001 §6.7`/`§6.14` (`[ACTIVE]`) govern the Business Activity's design-time content (Business Activity Contract, Canonical Business Activity Manifest). Neither is itself a runtime registry, discovery mechanism, or execution gate — `IMP-001 §6.22` is the distinct, also-unbuilt, engineering specification for that.
- The minimal-vs-full `IMP-001 §6.22` scope question (whether the LOCKED minimum requires the entire Business Activity Engine design or a materially smaller mechanism) is **not answered by any source examined**, independently re-confirmed for this document.
- `C-024 BA-01`'s own `D10` (`ROD-C024-BAR_Treatment_Decision_Preparation.md §0`): **DECIDED — Option A selected, 2026-09-19** — BAR treatment for C-024 BA-01 is deferred; not registered; no BAR identifier assigned; no enterprise exemption created; scoped to C-024 BA-01 only. This document does not change, reinterpret, or expand that scope.
- `C-024` CBOR registration is **complete** — `BIA-000001` (`ADR-041`). WP-22 is registered (`WPR-001`). C-024 implementation remains **NOT STARTED**.
- Three capability-scoped precedents exist, all deferring, all explicitly self-limited to their own capability: `ADR-037 §Decision item 5` (C-021/WP-20, 2026-09-08), `ROD-C022-B D10` (C-022/WP-21, 2026-09-15), `ROD-C024-BAR §0` (C-024/WP-22, 2026-09-19). None purports to bind any other capability, and none is treated as enterprise policy by this document.

---

## 3. Source Inventory (read directly for this document, not carried forward from the investigation's own summary)

- `SD-002_Universal_Business_Object_Rules.md` — `SD-002-004`, `SD-002-034`/`-035`. **Status: LOCKED.**
- `COM-001_Commercial_and_Subscription_Architecture.md` — `COM-001-005`, `COM-001-060`/`-061`. **Status: LOCKED — Certified, CR-3.0.** Re-read verbatim: "No commercial Business Activity shall be executed until registered in the BAR (`IMP-001 §6.22`)" (`COM-001-005`); "Every commercial action described in Sections 5–9... is a Business Activity per `SD-002 §5`, registered in the Business Activity Registry (`IMP-001 §6.22`) once implemented, per `COM-001-005`" (`COM-001-060`).
- `CMD-001_Canonical_Data_Model.md` — `§26.3`/`§26.3a`/`§26.4`/`§26.4a`/`§26.4b` (CBOR — cited for the CBOR/BAR distinction, re-confirmed `§26.3a`'s Canonical Business Object Eligibility Test has no BAR counterpart anywhere in this document); `§8.10`, cited in `ROD-C024-BAR §3`, characterizing BAR as an "Architectural Enhancement (Recommended)" at that citation point — a materially softer characterization than `COM-001-005`/`-060`'s own LOCKED mandatory language, and not resolved by this document (see §8 below).
- `PLT-001_Enterprise_Platform_Architecture.md` — `PLT-001-004`, `PLT-001-030`/`-031`. **Status: LOCKED**, identical "Registration Precedes Implementation"/"BAR Integration" formula to `COM-001`, re-verified verbatim.
- `GRC-001_Governance_Risk_and_Compliance_Architecture.md` — `GRC-001-008`, `GRC-001-070`/`-071`. **Status: LOCKED**, same formula, re-verified verbatim.
- `OPM-001_Enterprise_Operating_Model_Architecture.md` — `OPM-001-013` ("every domain document's own constructs remain individually responsible for their own BAR/CBOR registration... OPM-001 adds no registration obligation beyond what `SD-002-004/034/035` already establish"), `OPM-001-050`, `OPM-001-083`. **Status: LOCKED.**
- `ONT-001_Enterprise_Ontology_Architecture.md` — `ONT-001-051` (No BAR/CBOR Impact) and `ONT-001 §2` (Domain Ownership & Explicit Boundaries — "the registries of instances," confirming BAR and CBOR are two distinct registries, neither a subset of the other).
- `RTA-001 - Runtime Architecture and Execution.md` — `§3.6` (Business Activity Registry), `§6` ("Every executable business operation within the Aurex Intelligent Operating Center shall execute through the Business Activity Runtime" — re-verified verbatim, line 1124), `§11`. **Status: LOCKED.**
- `IMP-001_Implementation_Playbook.md` — `§6.7` (BAC — re-read in full: Activity Identifier, Domain, Object, Type, Intent, I/O Contract, Pre/Postconditions, Authorization, Events, Workflow, Audit, AI Assistance, Definition of Done, Idempotency), `§6.14` (CBAM — re-read in full: a machine-readable manifest with an overlapping but not identical attribute set), `§6.22.1`–`§6.22.15` (BAR full specification — re-read `§6.22.7`, "A Business Activity shall not be executable until successfully registered," and `§6.22.8`, "The Business Activity Engine shall discover Business Activities exclusively through the Registry," both verbatim). **Status: Active** — governs current engineering practice, evolves via Controlled Evolution (`ARCH-000 §12.6`).
- `CLAUDE.md` (current, checked into this repository) — searched in full for `BAR`/`Business Activity Registry`: **zero hits**, re-confirmed for this document. `§19.7`/`§19.7b`/`§20`/`§21` govern Business Activity completion gates but never name BAR.
- `WPR-001_Work_Package_Roadmap.md` — header row (`WP | Capability | Capability Name | Status | Governing IRA | Certification`) re-confirmed to carry no BAR/BA-Identifier column, for all WP-00 through WP-22.
- `CBOR-INDEX.md` — re-confirmed §1: "this Index registers Business Objects, not Business Activities." Its own prose narrates each capability's BAR-deferral decision (`OFR-000001`, `CAC-000001`, `BIA-000001` entries) as historical color, not as a BAR registration act.
- `C-021`/`WP-20` chain — `ADR-037 §Decision item 5` re-read verbatim (RO decision 2026-09-08: "do NOT create any BAR registry... a future enterprise-level decision may establish the canonical BAR mechanism").
- `C-022`/`WP-21` chain — `ROD-C022-B D10` (Option A, 2026-09-15).
- `C-024`/`WP-22` chain — `ROD-C024-BAR_Treatment_Decision_Preparation.md` (full document re-read, including the now-recorded `§0` decision), `IRA-C024_CBOR_Eligibility.md`, `ADR-041` (re-read `§Decision item 5`: "This ADR does not perform BAR registration"; `§Decision item 6`: "This ADR does not assign a Business Activity Identifier"), `WP-22_C024_BA-01_Establish_Billing_Arrangement_Charter.md §24`/`§27`.
- `ADR-039` (Commercial Account CBOR preparation) — identifier-timing precedent only, re-confirmed not a BAR artifact.
- Census artifacts: `AUREX_ENTERPRISE_FEATURE_CAPABILITY_COVERAGE_MATRIX.md §4` (per-WP `CBOR | BAR` column, confirming "Not performed"/"Deferred by RO decision" for every WP examined, none contradicting the investigation's own finding); `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md` (confirmed **stale** for C-024 — still describes "no Charter, WP, or Business Activity selection has occurred" as of its last correction pass, predating WP-22's chartering, CBOR registration, and D9/D10; addressed narrowly in §12 below, not as part of this document's substantive BAR analysis).
- Repository-wide search performed fresh for this document for `BAR`, `Business Activity Registry`, `Business Activity Identifier`, `BAR mechanism`, `activity registry` — no result beyond what `BAR_ENTERPRISE_MECHANISM_DECISION_INVESTIGATION.md §4`/`§6` already catalogued.

---

## 4. The Seven Repository Owner Decision Questions (re-extracted verbatim in substance from §14)

| # | Decision question (governance language) | Why required | Authoritative source basis | Classification |
|---|---|---|---|---|
| 1 | Does AUREX establish a canonical enterprise Business Activity Registry (BAR) mechanism now, or does it formally defer this to a future enterprise governance initiative? | `COM-001-005`/`-060` and their `PLT-001`/`GRC-001` counterparts impose a LOCKED obligation with no repository-wide disposition; three capability-scoped deferrals exist but none constitutes enterprise policy | `COM-001-005`/`-060`, `PLT-001-004`/`-030`, `GRC-001-008`/`-070`, `SD-002-034` | Constitutional/LOCKED obligation; **enterprise disposition is unresolved** |
| 2 | If established (Option A): what scope — a minimal LOCKED-compliant catalogue, or the full `IMP-001 §6.22` Business Activity Engine design? | `IMP-001 §6.22` describes an integrated mechanism (identity + registry + runtime discovery + execution gate + governance workflow) without distinguishing a minimal LOCKED-compliant subset from the full engineering design | `IMP-001 §6.22.1`–`§6.22.15` (Active, evolvable); `COM-001-005`/`-060` (LOCKED minimum) | Implementation methodology (`IMP-001`) vs. constitutional minimum (`COM-001`/`SD-002`); **unresolved ambiguity** |
| 3 | If established: does registration apply retroactively to the twenty-plus already-certified/implemented Business Activities that never raised the question, or only prospectively? | No source states whether the LOCKED cataloguing obligation is retroactively curable or only prospectively binding; nineteen of twenty-two Work Packages never raised BAR at all | `SD-002-034` (universal, no stated timing exception); repository Business Activity inventory (`[FACT]`) | Constitutional obligation's timing scope; **unresolved, no source addresses retroactivity** |
| 4 | If deferred (Option B): does the deferral apply enterprise-wide, or only to the capabilities that have already raised it case-by-case (C-021/C-022/C-024)? | Each of the three existing deferrals explicitly disclaims creating a "repository-wide policy"; if this decision itself is drawn broadly, it would be the first artifact to actually do so | `ADR-037 §Decision item 5`, `ROD-C022-B D10`, `ROD-C024-BAR §0` — each self-limiting, verbatim | Precedent (non-binding) vs. the enterprise decision this document prepares; **this is the one place the RO is being asked to do something the precedents deliberately did not do** |
| 5 | Business Activity Identifier authority: if BAR is established, who assigns `BA-NNNNNN` identifiers, and at what governance point? | `SD-002-004` establishes the identity form but assigns no authority or timing; the CBOR precedent (identifier assigned only at registration, never earlier — `ADR-039 §Decision item 1`, `ADR-040 §Decision item 1`, `ADR-041 §Decision item 1`) is the only analogous governance pattern in this repository | `SD-002-004`; CBOR identifier-timing precedent (`[PRECEDENT]`, not binding by cross-domain default) | Governance-authority assignment; **depends on Decision 1 being "establish"** |
| 6 | Relationship to `IMP-001`: does establishing BAR require amending `IMP-001 §6.22` to fix the minimal-vs-full scope ambiguity, or is that left to a future engineering decision within whatever scope Decision 2 selects? | `IMP-001` is Active/evolvable (`ARCH-000 §12.6` Controlled Evolution), not LOCKED — amending it is procedurally available but not automatically required by establishing BAR | `IMP-001` document header (Status: Active); `ARCH-000 §12.6` (Controlled Evolution, cited, not independently re-read for this document beyond its citation in `IMP-001`'s own header) | Implementation methodology governance; **depends on Decision 2's scope choice** |
| 7 | Relationship to `WPR-001`: does `WPR-001`'s own table structure gain a BAR-status column, or does BAR remain a separately-tracked register exactly as `CBOR-INDEX.md` is separate from `WPR-001` today? | `WPR-001`'s own table structure has no BAR field today (re-confirmed §3 above); `CBOR-INDEX.md` demonstrates the "separate index" pattern already works for CBOR | `WPR-001` §3 table structure (`[FACT]`); `CBOR-INDEX.md`'s own existing separation from `WPR-001` (`[FACT]`, structural precedent) | Registry-architecture placement; **depends on Decision 1/2 (there is nothing to place a column for until a mechanism, or the decision not to build one, exists)** |

No additional decision is manufactured. All seven trace directly to a gap or ambiguity independently re-confirmed in §2–§3 above.

---

## 5. Decision Dependency Structure

| Decision | Depends on | Can be decided independently? | Evidence |
|---|---|---|---|
| 1. Establish BAR now vs. defer | — (root decision) | Yes — this is the entry point | All six other decisions are conditioned on this one's outcome, per their own "if established"/"if deferred" framing in `§14` |
| 2. BAR scope (minimal vs. full `§6.22`) | Decision 1 = Establish | No — a scope question presupposes something is being built | `§14` Decision 2 is explicitly framed "If established (Option A): what scope?" |
| 3. Retroactive vs. prospective registration | Decisions 1 AND 2 | No — retroactive registration of which existing BAs, in what form, cannot be evaluated until it is known whether BAR is built at all, and at what scope (a minimal catalogue's retroactive backfill is a materially smaller undertaking than the full Business Activity Engine's) | Investigation §12, Option A's own "Impact on existing BAs" row: "Depending on scope chosen, some or all could require identifier backfill" |
| 4. Scope of a deferral (enterprise-wide vs. case-by-case only) | Decision 1 = Defer | No — this question only exists if Decision 1 selects deferral; it is the Option-B-side mirror of Decision 3 | `§14` Decision 4 is explicitly framed "If deferred (Option B): does the deferral apply enterprise-wide..." |
| 5. Business Activity Identifier authority | Decision 1 = Establish, and (in substance) Decision 2 | No — identifier assignment authority is meaningless without a mechanism to assign into, and the governance point ("at registration") presupposes a registration event that Decision 2's scope choice defines | `§14` Decision 5 is explicitly framed "if BAR is established" |
| 6. `IMP-001` amendment | Decision 1 = Establish, and Decision 2 | No — whether `§6.22`'s ambiguity needs fixing by amendment depends on which scope (minimal or full) is chosen; a minimal mechanism might not need `§6.22` touched at all, while a full-engine build likely would | `§14` Decision 6's own framing: "does establishing BAR require amending... or is that left to a future engineering decision within whatever scope is chosen in Decision 2" |
| 7. `WPR-001` relationship | Decision 1, and in substance Decision 2 | No — there is nothing to place a column for, or to decide to keep separate, until it is known whether a mechanism exists and what it looks like | `[INFERENCE]`, drawn from the structural fact that `CBOR-INDEX.md`'s own separateness from `WPR-001` is only meaningful because CBOR itself exists as a built mechanism |

**Structural summary:** Decision 1 is the sole root. Decisions 2, 3, 5, 6, 7 chain beneath the "Establish" branch (2 first, then 3/5/6/7 each independently downstream of 2). Decision 4 is the sole item beneath the "Defer" branch. No decision below Decision 1 can be meaningfully answered before Decision 1 is made — the investigation's own §14 phrasing ("If established..." / "If deferred...") already encodes this, and this document does not depart from it. This document does not select an order for the Repository Owner to answer them in beyond what their own logical dependency requires (Decision 1 first); it identifies the structure, not a sequencing preference beyond that structural necessity.

---

## 6. Primary Enterprise Decision — Option A vs. Option B

**No option is selected below. Both are re-examined directly against source text, not carried forward from the investigation's own characterization.**

### OPTION A — Establish a canonical enterprise BAR mechanism now ✅ **SELECTED** (recorded 2026-09-19, per §0)

**Exact source basis:** `SD-002-004`/`-034` (identity + cataloguing obligation), `COM-001-005`/`-060` (execution-gate, commercial domain), `PLT-001-004`/`-030`, `GRC-001-008`/`-070` (identical obligation, platform/governance domains), `OPM-001-013` (confirms universality), `IMP-001 §6.22` (the only existing engineering design to draw from, Active not LOCKED).

**What it would authorize:** creation of a BAR mechanism (scope per Decision 2); assignment of `BA-NNNNNN` identifiers (authority/timing per Decision 5); a registration event that could, depending on Decision 3, apply to existing and/or future Business Activities.

**What it would NOT authorize:** any specific technical design (database schema, API, runtime class, service topology) — that remains future, separately governed engineering work; retroactive registration of any specific existing Business Activity (a separate act under Decision 3); any change to `C-024 D10` or any other capability-scoped deferral, which would remain valid decisions made under the prior (no-mechanism) state unless separately revisited.

**Immediate governance consequences:** a new mandatory step would need to be reflected somewhere in Business Activity governance (exact placement is Decision 7); `CLAUDE.md §21.3`'s Standard Work Package Lifecycle and/or `§19.7b`'s gate sequence would need a cross-reference this document is not authorized to make (a `CLAUDE.md` amendment is out of this document's scope per its own change boundary).

**Consequence for Business Activity creation:** a central catalogue-collision check would become possible for new BAs going forward (scope-dependent — a minimal catalogue supports this; a full engine additionally supports runtime discovery).

**Consequence for Chartering:** Charters (per `IMP-001 §6.7`/`§6.14`) already narrate BAC-equivalent content in prose; establishing BAR does not, by itself, change what a Charter must contain — it adds a downstream registration step after or alongside chartering, exact placement per Decision 5.

**Consequence for `WPR-001`:** per Decision 7 — either a new column, or a separate index mirroring `CBOR-INDEX.md`'s own precedent.

**Consequence for Business Activity Identifier assignment:** would begin for the first time in this repository's history; timing/authority per Decision 5.

**Consequence for execution-time discovery:** if the full `§6.22` scope is adopted, `§6.22.8`'s verbatim rule ("The Business Activity Engine shall discover Business Activities exclusively through the Registry") would make the registry the sole discovery path — a materially larger runtime change than a minimal catalogue, which need not affect discovery at all (`[INFERENCE]`, since no source distinguishes discovery obligations by scope level).

**Consequence for execution-time gating:** `§6.22.7`'s verbatim rule ("A Business Activity shall not be executable until successfully registered") would apply, matching `COM-001-005`'s own execution gate for commercial-domain BAs, once triggered.

**Consequence for audit/assurance:** currently functions via direct `record_audit`/`publish_event` calls without registry mediation (`[FACT]`, verified across implemented WPs); `IMP-001 §6.22.6` names Events/Audit as a registry-tracked category only if the full-scope design is built — no source states the current mechanism is deficient or requires registry mediation to function correctly.

**Consequence for future agent/runtime orchestration:** `[FACT]` no source ties BAR to AI agent execution/orchestration beyond `IMP-001 §6.22.6`'s "AI" attribute category and `§6.12`'s general "AI shall not execute Business Activities autonomously unless explicitly permitted by governance." If a future Business Activity is intended for AI-agent invocation, `§6.22`'s AI-configuration fields would need a home; none exists outside the unbuilt BAR. This is source-supported as a *future* consequence, not a current blocker (no such agent-invoked Business Activity exists yet in this repository).

**Consequence for already-existing Business Activities:** all 20+ already-certified/implemented BAs (per the investigation's §7 inventory) would face the retroactive-registration question — Decision 3, not resolved by choosing Option A alone.

**Consequence for future Business Activities:** every future BA would need to satisfy whatever registration timing Decision 5 sets before executing (`COM-001-005`), and — if full `§6.22` scope is adopted — before being discoverable at all (`§6.22.8`).

**Consequence for C-024 BA-01 specifically:** BA-01 could proceed to implementation without further BAR-specific delay only if the new mechanism's registration timing is satisfied before **execution**, exactly as `COM-001-005` already requires; **`D10` would need no reopening either way**, since D10 only deferred the decision, not a specific registration timeline (re-verified directly against `ROD-C024-BAR §0`, unchanged by this document).

**Required follow-on artifacts:** a `BAR-INDEX.md` (or equivalent) mirroring `CBOR-INDEX.md`'s own Amendment Procedure; a registering-ADR pattern per Business Activity; potentially an `IMP-001`/`CLAUDE.md` amendment (Decision 6/7) — none of which this document creates.

**Unresolved questions this option leaves open even if selected:** Decisions 2, 3, 5, 6, 7 in full — Option A alone answers none of them.

### OPTION B — Continue without an enterprise BAR mechanism; formally defer to a future enterprise governance initiative

**Exact source basis:** the unbroken precedent of three prior deferrals with zero subsequent gate blockage (`ADR-037`, `ROD-C022-B D10`, `ROD-C024-BAR §0`); `COM-001-005`'s own execution-gate (not implementation-gate) framing, which textually permits continued implementation/certification work while the obligation remains outstanding; the fact that 19 of 22 Work Packages have already, in effect, operated this way without any decision ever being recorded for them.

**What it would authorize:** continued implementation, certification, and closure of future Business Activities without a BAR mechanism, exactly as has occurred for 22 of 22 Work Packages to date.

**What it would NOT authorize:** discharge of the underlying `COM-001-005`/`-060` (and `PLT-001`/`GRC-001` counterpart) LOCKED obligation, which remains outstanding, not satisfied, and not waived — Option B is a deferral of the *decision*, not a repeal of the constitutional text.

**Immediate governance consequences:** none — no new gate, no new artifact type, no `CLAUDE.md`/`IMP-001` change.

**Consequence for Business Activity creation:** unchanged from current practice.

**Consequence for Chartering:** unchanged — Charters continue to narrate BAR as a future prerequisite (as WP-20/21/22 already do) or not mention it (as WP-16 through WP-19 do).

**Consequence for `WPR-001`:** unchanged — no column added.

**Consequence for Business Activity Identifier assignment:** continues not to occur; every BA remains identified only by informal, per-Charter ordinal labels, not a `SD-002-004`-form identity.

**Consequence for execution-time discovery/gating:** the LOCKED execution-gate obligation (`COM-001-005`) remains outstanding for any commercial-domain BA that reaches actual execution — a genuinely unresolved condition this document does not resolve any further than the investigation already disclosed it (whether "execution" has occurred, in a sense distinct from "implemented and certified," for any C-020–C-025 construct to date is not established by any source examined).

**Consequence for audit/assurance:** none observed — functions today without BAR, as under Option A's own equivalent row.

**Consequence for future agent/runtime orchestration:** unresolved, same as under Option A — no source currently makes this a blocker either way.

**Consequence for already-existing Business Activities:** none — no change to any already-certified Work Package's status.

**Consequence for future Business Activities:** each future commercial-domain (`COM-001` Sections 5–9) BA would need its own case-by-case BAR-deferral decision before implementation/Charter conclusion (mirroring `ADR-037`/`ROD-C022-B`/`ROD-C024-BAR`), **unless** Decision 4 resolves this deferral broadly enough to cover future cases without a fresh decision each time.

**Consequence for C-024 BA-01 specifically:** no change — `D10` already reflects this option's own logic for C-024 BA-01, and remains valid and unaffected regardless of whether Option B is formally adopted enterprise-wide.

**Required follow-on artifacts:** none beyond this document's own record, and (if selected) whatever record of Decision 4's scope the Repository Owner directs.

**Unresolved questions this option leaves open even if selected:** Decision 4 in full.

**No third, materially distinct alternative was found in the sources examined**, re-confirmed independently for this document. A middle path ("build only the minimal catalogue now, defer the full engine") is Option A with Decision 2 resolved toward the minimal end — not a separate option, and not manufactured as one here.

---

## 7. The Remaining Six Decisions — Options and Consequences

### Decision 2 — Enterprise BAR Scope (full decision preparation, expanded 2026-09-19 following Decision 1's selection of Option A)

**Status: D2 — DECIDED — Option A (LOCKED minimum scope) selected, recorded 2026-09-20, §0b above.**

#### D2.1 — Decision Statement

Given Decision 1 = Establish, what exact scope should the canonical enterprise BAR mechanism have? Specifically: which BAR responsibilities are constitutionally mandatory (LOCKED minimum), which are supported only by `IMP-001 §6.22`'s Active engineering methodology as extended/optional scope, which belong to another AUREX mechanism entirely, and which remain unresolved?

#### D2.2 — Why D2 Is Required

Decision 1 authorized establishing *a* BAR but decided nothing about *what* that BAR must contain. `IMP-001 §6.22` (re-read in full for this section, `§6.22.1`–`§6.22.15`) describes an integrated mechanism — canonical identity, registry contents/attributes, registration validation, exclusive discovery, lifecycle status, version management, dependency management, governance workflow, and observability — without itself distinguishing which of these are the constitutional minimum `COM-001-005`/`-060`/`SD-002-034` actually requires versus which are `IMP-001`'s own (Active, evolvable) engineering elaboration. Building the wrong scope — too little to discharge the LOCKED obligation, or an unauthorized amount of unnecessary engineering work — is a live risk this decision exists to prevent.

#### D2.3 — Authoritative Source Basis (re-read directly for this section)

- `SD-002-004` (Universal Identity), `SD-002-034` (Business Activities Rules, formalization note) — `[LOCKED]`.
- `COM-001-005` (Registration Precedes Implementation), `COM-001-060` (BAR Integration) — `[LOCKED]`, re-verified verbatim: "No commercial Business Activity shall be executed until registered in the BAR"; "registered in the Business Activity Registry... once implemented."
- `PLT-001-004`/`-030`, `GRC-001-008`/`-070` — `[LOCKED]`, identical formula, platform/governance domains.
- `IMP-001 §6.22.1`–`§6.22.15` — `[ACTIVE]`, re-read in full for this section (not from summary):
  - `§6.22.1` (Purpose): "the authoritative source for Business Activity discovery, execution, governance, monitoring, and lifecycle management."
  - `§6.22.1a` (Constitutional Authority): "The Business Activity Registry operationalizes, at the engineering layer, the identity and rules SD-002 §5 already establishes at the constitutional layer... IMP-001 does not redefine Business Activity semantics here — per §1.2, it governs how the platform is built, not what is built."
  - `§6.22.2` (Architectural Principle): "Business Activities are platform assets. Platform assets shall be registered... The Registry is the source of truth."
  - `§6.22.3` (Registry Ownership): the Business Activity Engine "shall use the Registry for" nine listed functions (Discovery, Version Resolution, Contract Validation, Execution Policy Resolution, Authorization Resolution, Workflow Integration, Event Configuration, AI Integration, Monitoring, Lifecycle Governance).
  - `§6.22.5`/`§6.22.6` (Registry Contents/Canonical Attributes): a full attribute set across eight categories (Identity, Classification, Ownership, Execution, Security, Workflow, Events, AI, Runtime).
  - `§6.22.7` (Activity Registration), verbatim: "A Business Activity shall not be executable until successfully registered." Validation list: Business Activity Contract, Manifest Completeness, Version Compatibility, Dependency Resolution, Authorization Configuration, Event Definitions, Workflow References, AI Configuration.
  - `§6.22.8` (Activity Discovery), verbatim: "The Business Activity Engine shall discover Business Activities exclusively through the Registry."
  - `§6.22.9` (Activity Status): Draft/Registered/Active/Suspended/Deprecated/Retired; "Only Active Business Activities may be executed."
  - `§6.22.10` (Registry Version Management), `§6.22.11` (Dependency Management), `§6.22.12` (Registry Governance: "Registry modifications shall themselves be governed Business Activities"), `§6.22.13` (Registry Observability) — each a distinct responsibility category.
  - `§6.22.14` (Relationship with CBAM): "The CBAM describes **what** the Business Activity is. The Registry describes **how** the platform manages it."
  - `§6.22.15` (Architectural Guarantees): "Every executable Business Activity... shall be registered in the Business Activity Registry before becoming available for execution."
- `RTA-001 §3.6` (Business Activity Registry, within the LOCKED Runtime Execution Architecture), re-read directly: "Primary responsibilities include: Activity discovery, Version resolution, Manifest resolution, Execution policy lookup, Dependency resolution, Registration governance. The Registry contains execution metadata. It does not execute Business Activities."
- `RTA-001 §6.6` (Activity Discovery, within Section 6 — Business Activity Runtime, also LOCKED) — a **newly independently re-verified finding for this section**, distinct from `IMP-001 §6.22.8`: verbatim, "The Business Activity Engine shall discover executable Business Activities exclusively through the Business Activity Registry... Business Activities shall never be discovered through implementation-specific mechanisms." This is textually distinct from, but substantively reinforcing, `IMP-001 §6.22.8`'s own discovery-exclusivity rule — and because `RTA-001` (unlike `IMP-001`) carries **LOCKED** status, "exclusive discovery through the registry" is asserted independently in a LOCKED document, not only in `IMP-001`'s Active methodology. This is material to D2.4/D2.5 below and was not fully credited in this document's earlier (§8, pre-D2) IMP-001-only framing of the discovery question.
- `CMD-001 §8.10` (Architectural Enhancement — Recommended), re-verified directly: "I recommend introducing a Business Activity Registry (BAR)" — phrased as an authorial recommendation, not LOCKED mandatory text, in a section format `CMD-001` uses identically for over a dozen other "recommended" registries/mechanisms throughout the same document (`§3.14`, `§4.10`, `§5.16`, `§6.14`, `§7.10`, `§9.11`, etc.) — none of which is treated elsewhere in this repository as LOCKED. This is a materially softer characterization than `COM-001-005`/`-060`'s own LOCKED mandatory language, and the two are not reconciled by any source — flagged as an unresolved tension, not resolved here (see D2.9).

#### D2.4 — Step 1: What "BAR Scope" Actually Means (Responsibility Taxonomy)

Re-deriving from `§6.22`/`RTA-001 §3.6`/`§6.6` rather than assuming "scope" means a technical feature list, the sources support distinguishing these candidate BAR responsibilities:

| Candidate responsibility | Source | Belongs to BAR, or elsewhere? |
|---|---|---|
| What Business Activities are catalogued (which BAs get an entry) | `SD-002-034`, `COM-001-060` | BAR |
| Canonical identity (the `BA-NNNNNN` identifier itself) | `SD-002-004`, `IMP-001 §6.22.1b` | Identity *format* is `SD-002-004`'s; *assignment authority/timing* is Decision 5, not D2 |
| Registration state/lifecycle (Draft/Registered/Active/Suspended/Deprecated/Retired) | `IMP-001 §6.22.9` | BAR (Active-methodology elaboration; not itself in the LOCKED minimum text — see D2.5) |
| Execution-time registration gate (must be registered before executable) | `COM-001-005`, `IMP-001 §6.22.7`, `IMP-001 §6.22.15` | BAR — this is the LOCKED minimum's own core mechanism |
| Discovery (how the runtime finds a BA to execute) | `IMP-001 §6.22.8`, `RTA-001 §6.6` (LOCKED) | BAR |
| Execution-time lookup/resolution (version, manifest, execution policy) | `IMP-001 §6.22.3`, `RTA-001 §3.6`/`§6.4` | BAR (Active/`RTA-001`-elaboration; not independently LOCKED beyond the discovery/gate minimum) |
| Validation (contract/manifest/version/dependency/authorization/event/workflow completeness at registration) | `IMP-001 §6.22.7` | BAR, but as an Active-methodology elaboration of *how* registration is validated, not a separately LOCKED obligation |
| Governance linkage (registration approval, activation, suspension, retirement as governed Business Activities in their own right) | `IMP-001 §6.22.12` | BAR (Active elaboration) — **not source-supported as LOCKED** |
| Traceability | No source ties this to BAR specifically beyond general auditability (`§6.22.15`) | Currently achieved via Charter/ADR/ROD cross-reference (§9 of this document), not BAR-specific |
| Audit/assurance | `IMP-001 §6.22.6` (Events category) | Currently achieved directly (`record_audit`/`publish_event`) without BAR mediation (`[FACT]`, re-confirmed §7 investigation finding); `§6.22`'s registry-tracked Events category is Active-elaboration only, not LOCKED |
| Authorization interaction | `IMP-001 §6.22.3`/`§6.22.6` (Authorization Resolution) | Currently direct (`require_platform_admin` and peers); registry-mediated authorization is Active-elaboration only |
| Orchestration/runtime interaction (AI agent invocation) | `IMP-001 §6.22.6` AI category, `§6.12` | Not currently source-supported as a BAR-mandatory responsibility — no agent-invoked BA exists yet (re-confirmed, unchanged from the investigation's own §10 finding) |

**A. Business Activity design-time governance** (BAC/`§6.7`, CBAM/`§6.14`, Charter) is confirmed, again, to be distinct from **B. BAR responsibilities** (§8 of this document already established this; not re-litigated here). D2 concerns category B only.

#### D2.5 — Step 2: The LOCKED Minimum (extracted directly, not assumed from `§6.22`)

| Responsibility | Exact source | Mandatory? | Why | Lifecycle point | Evidence type |
|---|---|---|---|---|---|
| Business Activity registration (cataloguing) | `SD-002-034` formalization note; `COM-001-060`/`PLT-001-030`/`GRC-001-070` | **Yes** | "Every Activity satisfying `SD-002-034` is catalogued in the Business Activity Registry" — unconditional | Cataloguing (timing per domain: commercial "once implemented," `COM-001-060`) | `[LOCKED]` |
| Canonical Business Activity identity | `SD-002-004` | **Yes** | Universal Identity applies to all business objects, explicitly including BAs (`BA-000089` example) | Assignment timing = Decision 5, not itself part of the LOCKED minimum's scope question | `[LOCKED]` |
| Execution-time gate (not executable until registered) | `COM-001-005`; `PLT-001-004`; `GRC-001-008` | **Yes** | "No commercial Business Activity shall be executed until registered in the BAR" — verbatim, unconditional for commercial domain, identical formula for platform/governance | Execution (a later gate than implementation) | `[LOCKED]` |
| Business Activity discoverability through BAR (exclusive discovery) | `RTA-001 §6.6` (LOCKED: "shall discover executable Business Activities exclusively through the Business Activity Registry... shall never be discovered through implementation-specific mechanisms") | **Yes, once the Runtime Execution Architecture is the discovery path** | This is LOCKED text, independent of `IMP-001 §6.22.8`'s own (Active) parallel statement — re-verified as a distinct, reinforcing source | Execution-time (discovery precedes execution) | `[LOCKED]`, with the caveat below |
| Registration status (Draft/Registered/Active/.../Retired lifecycle model) | `IMP-001 §6.22.9` only | **Not established as LOCKED** | No `SD-002`/`COM-001`/`PLT-001`/`GRC-001` text requires a specific status taxonomy — only that registration precede execution | N/A | `[ACTIVE]` (methodology), not `[LOCKED]` |
| Registration lookup / version / execution-policy resolution | `IMP-001 §6.22.3`, `RTA-001 §3.6`/`§6.4` | **Not established as LOCKED beyond the discovery minimum** | These are `RTA-001`'s own (LOCKED) runtime responsibilities for *how the runtime uses* the registry once execution occurs through it, but no source states a smaller BAR (satisfying only cataloguing + identity + execution-gate + discovery) would fail to satisfy the constitutional minimum | Execution-time, if/when the Runtime Execution Architecture is engaged | `[LOCKED]` for the runtime-collaboration principle in the abstract (`RTA-001 §6.1`: "every executable business operation... shall execute through the Business Activity Runtime"); **`[ACTIVE]`/unresolved for whether every registry attribute `§6.22.6` lists is itself required to satisfy that principle** |
| Validation (contract/manifest/version/dependency/authorization/event/workflow) | `IMP-001 §6.22.7` only | **Not established as LOCKED** | No constitutional text requires this specific validation checklist; it is `IMP-001`'s own engineering elaboration of how registration integrity is enforced | Registration | `[ACTIVE]` |
| Governance traceability (registration approval, activation, suspension, retirement as governed Business Activities) | `IMP-001 §6.22.12` only | **Not established as LOCKED** | Same reasoning | Ongoing | `[ACTIVE]` |
| Version management, dependency management, observability | `IMP-001 §6.22.10`/`§6.22.11`/`§6.22.13` only | **Not established as LOCKED** | Same reasoning | Ongoing | `[ACTIVE]` |

**Caveat on the discovery row:** `RTA-001 §6.1` frames the Business Activity Runtime (of which BAR-based discovery is one part) as engaging "every executable business operation" — but the investigation's own §5 finding, re-confirmed here, is that `RTA-001`'s own runtime model is "entirely unbuilt" for any Business Activity in this repository to date, and `WP-RTA-001` (the one runtime initiative actually chartered) was narrowly scoped to the Authorization Engine only, not the Business Activity Runtime/BAR. **This document does not resolve whether a LOCKED requirement that currently applies to zero executing Business Activities (because none executes through the Runtime Execution Architecture yet) is "mandatory now" in a practical sense, or "mandatory once the Runtime Execution Architecture is engaged" — both readings are textually available and neither is selected here.**

**LOCKED minimum, stated plainly:** cataloguing (identity + registration) and an execution-time gate are the only two responsibilities this document finds unambiguously LOCKED and unconditional today. Exclusive discovery through the registry is LOCKED **in principle** (`RTA-001 §6.6`) but its practical trigger point is tied to the same not-yet-engaged Runtime Execution Architecture the investigation already found unbuilt for every existing Business Activity. Every other `§6.22` responsibility (status lifecycle, version management, dependency management, governance workflow, observability, validation checklist) is `IMP-001`'s own Active-methodology elaboration, not independently established as LOCKED by this document's review.

#### D2.6 — Step 3: `IMP-001 §6.22` Subsection-by-Subsection Analysis

| Subsection | Exact responsibility | Classification | Belongs in |
|---|---|---|---|
| `§6.22.1` Purpose | Registry is "the authoritative source for... discovery, execution, governance, monitoring, and lifecycle management" | Implementation methodology (framing statement) | Mandatory scope, framing only — not itself an enforceable rule |
| `§6.22.1a` Constitutional Authority | BAR "operationalizes" `SD-002 §5`; "governs how the platform is built, not what is built" | Explanatory text, self-limiting | N/A — a scope disclaimer, not a responsibility |
| `§6.22.1b` Identifier Strategy | Identifier format = `SD-002-004`'s, not a new format | Constitutional cross-reference | Identity format is mandatory (via `SD-002-004`); assignment authority is Decision 5 |
| `§6.22.2` Architectural Principle | "Platform assets shall be registered... Registry is the source of truth" | Implementation methodology (restates the LOCKED cataloguing obligation in engineering terms) | Mandatory scope (restates `SD-002-034`) |
| `§6.22.3` Registry Ownership | Nine Business Activity Engine functions (Discovery, Version Resolution, Contract Validation, Execution Policy Resolution, Authorization Resolution, Workflow Integration, Event Configuration, AI Integration, Monitoring, Lifecycle Governance) | Architectural prescription | Extended/optional scope — only Discovery is independently LOCKED (`RTA-001 §6.6`); the other eight are Active-methodology only |
| `§6.22.4` Registry Architecture | Diagram — Business Domains register → Registry → Business Activity Engine executes | Architectural prescription (illustrative) | Explanatory — not itself a separate responsibility |
| `§6.22.5` Registry Contents | Ten metadata categories, "execution metadata, not business data" | Architectural prescription | Extended/optional scope |
| `§6.22.6` Canonical Registry Attributes | Eight attribute groups (Identity, Classification, Ownership, Execution, Security, Workflow, Events, AI, Runtime) — a large, detailed schema | Architectural prescription | Extended/optional scope — Identity alone traces to `SD-002-004` (mandatory); the remaining seven groups are Active-methodology elaboration |
| `§6.22.7` Activity Registration | "Shall not be executable until successfully registered"; validation checklist | Constitutional restatement (execution gate) + implementation methodology (validation checklist) | The gate itself is mandatory (restates `COM-001-005`); the seven-item validation checklist is extended/optional scope |
| `§6.22.8` Activity Discovery | "Shall discover... exclusively through the Registry" | Implementation methodology, reinforced by `RTA-001 §6.6`'s independently LOCKED parallel statement | Mandatory in principle (via `RTA-001`), subject to the practical-trigger caveat in D2.5 |
| `§6.22.9` Activity Status | Six-state lifecycle; "only Active... may be executed" | Implementation methodology | Extended/optional scope — not independently LOCKED |
| `§6.22.10` Registry Version Management | Version history, compatibility, migration | Implementation methodology | Extended/optional scope |
| `§6.22.11` Dependency Management | Dependency tracking across Business Objects/Metadata/Workflows/Events/AI Models/Integrations/Feature Flags | Implementation methodology | Extended/optional scope |
| `§6.22.12` Registry Governance | Registration approval, activation, suspension, retirement as "governed Business Activities" | Implementation methodology | Extended/optional scope — **unresolved ambiguity**: if registry modifications are themselves Business Activities, do they also require BAR registration, and would this be circular for the first such Business Activity? No source resolves this; flagged, not resolved. |
| `§6.22.13` Registry Observability | Nine metrics | Implementation methodology | Extended/optional scope |
| `§6.22.14` Relationship with CBAM | "CBAM describes what; Registry describes how the platform manages it" | Explanatory (boundary statement) | Confirms, does not expand, the BAR/CBAM (design-time vs. runtime) boundary already established in §8 of this document |
| `§6.22.15` Architectural Guarantees | Eight guarantees; "every executable Business Activity... shall be registered... before becoming available for execution" | Constitutional restatement (execution gate, again) + implementation methodology (the eight guarantees) | The execution-gate restatement is mandatory; the eight named "guarantees" (centralized discovery, standardized metadata, lifecycle management, version governance, dependency transparency, consistent execution policies, observability, auditability) are extended/optional scope, not independently LOCKED |

**On over-generalizing from `§6.22.8`:** re-verified again for this section — `§6.22.8`'s own text is narrowly about *discovery* ("shall discover Business Activities exclusively through the Registry"), and does not itself state or imply the validation checklist (`§6.22.7`), the status lifecycle (`§6.22.9`), or the governance-workflow requirement (`§6.22.12`). This document does not extend `§6.22.8`'s own narrow discovery claim into a broader mandate — each `§6.22` subsection is classified on its own text, not by association with its neighbors.

#### D2.7 — Step 4: Minimal vs. Full Scope (and whether a third, materially distinct option exists)

**OPTION A — Minimum BAR Scope ✅ SELECTED (recorded 2026-09-20, per §0b)**

*Source basis:* `SD-002-004`/`-034`, `COM-001-005`/`-060`/`PLT-001-004`/`-030`/`GRC-001-008`/`-070` (the LOCKED cataloguing + execution-gate obligation), `RTA-001 §6.6` (LOCKED discovery-exclusivity, subject to D2.5's practical-trigger caveat).

*Included:* canonical BA identity (format only — assignment mechanics = Decision 5); a registration record per BA (cataloguing); an execution-time gate (`§6.22.7`'s core rule, without its full validation checklist); registry-mediated discovery (once/if the Runtime Execution Architecture is engaged).

*Excluded:* the full `§6.22.6` attribute schema beyond Identity; status lifecycle (`§6.22.9`); version management (`§6.22.10`); dependency management (`§6.22.11`); registry governance workflow (`§6.22.12`); observability (`§6.22.13`); the seven-item validation checklist (`§6.22.7`) beyond whatever minimal check discharges the gate itself.

*What remains delegated elsewhere:* design-time content stays with BAC/CBAM (`§6.7`/`§6.14`, IMP-001); audit/assurance stays with the existing direct `record_audit`/`publish_event` mechanism; authorization stays with direct FastAPI dependency injection, unchanged.

*New governance responsibilities arising:* a minimal registering act (mirroring the CBOR ADR pattern) per BA; nothing else new.

*Impact on existing BAs:* a smaller retroactive-backfill exercise if Decision 3 selects retroactive (identity + one registration record per BA, not a full metadata population).

*Impact on future BAs:* a smaller registration step to satisfy before execution.

*Impact on execution:* the gate applies; full runtime discovery only if/when `RTA-001`'s Runtime Execution Architecture is separately engaged (unresolved trigger point, per D2.5).

*Impact on assurance/audit:* none — unchanged from current practice.

*Impact on C-024:* none directly — `D10` remains a deferral regardless (§ D2.13 below).

*Follow-on decisions required:* Decision 5 (identifier authority), Decision 7 (`WPR-001` vs. index placement) become smaller-scoped questions under this option; Decision 6 (`IMP-001` amendment) becomes more likely necessary, since a minimal BAR would leave most of `§6.22`'s own text describing an unbuilt superset.

**OPTION B — Full `IMP-001 §6.22` BAR Scope**

*Source basis:* `IMP-001 §6.22.1`–`§6.22.15` in its entirety, `RTA-001 §3.6`/`§6` (the fuller Runtime Execution Architecture BAR sits within).

*Included:* everything in D2.6's table — full attribute schema, validation checklist, status lifecycle, version management, dependency management, governance workflow, observability, and registry-mediated discovery/execution-policy/authorization/workflow/event/AI resolution as the Business Activity Engine's exclusive source (`§6.22.3`).

*Excluded:* nothing within `§6.22`'s own stated scope; design-time content (BAC/CBAM) remains outside BAR either way (§8 of this document, unchanged).

*What remains delegated elsewhere:* still nothing outside `§6.22` itself is absorbed — this option does not expand BAR beyond what `§6.22` already claims for it.

*New governance responsibilities arising:* registry governance itself becomes "governed Business Activities" (`§6.22.12`) — the unresolved circularity question flagged in D2.6 becomes live under this option specifically.

*Impact on existing BAs:* a materially larger retroactive-backfill exercise if Decision 3 selects retroactive — full metadata population (all eight `§6.22.6` categories) per BA, not just identity + a registration record.

*Impact on future BAs:* a materially larger registration step; authorization, workflow, events, and AI configuration would need to be expressed twice (once in the BAC/CBAM design-time artifact, once in the BAR runtime registry) unless the two are mechanically synchronized — a design question this document does not resolve (no mechanism design).

*Impact on execution:* the Business Activity Engine becomes the exclusive execution path for every registered BA (`§6.22.3`), a materially larger runtime change than Option A's own narrower discovery-only claim.

*Impact on assurance/audit:* `§6.22.6`'s Events category and `§6.22.13`'s observability metrics would become registry-tracked, potentially duplicating (or replacing) the current direct `record_audit`/`publish_event` mechanism — this document flags the duplication risk (§ D2.9) without resolving which prevails.

*Impact on C-024:* none directly — `D10` remains a deferral regardless (§ D2.13).

*Follow-on decisions required:* the investigation's own §12 finding, re-confirmed here, that full realization "would very likely require a dedicated Work Package or enterprise initiative of its own, comparable in scope to `WP-RTA-001`'s own narrower [Authorization Engine only] undertaking" — Decisions 5/6/7 would each be answered at a correspondingly larger scale.

**No third, materially distinct option was found.** A "build the minimal set now, add `§6.22`'s remaining categories incrementally later" path is a sequencing variant of Option A (build minimal, treat the rest as future extension) rather than a separate scope definition — this document does not manufacture it as "Option C," consistent with the investigation's own §12 finding that an intermediate path "is Option A with its own scope question resolved toward the minimal end."

#### D2.8 — Consequences of Each Option (consolidated, non-evaluative)

| Dimension | Option A (minimum) | Option B (full `§6.22`) |
|---|---|---|
| Existing BAs | Smaller backfill exercise if Decision 3 = retroactive | Larger backfill exercise if Decision 3 = retroactive |
| Future BAs | Smaller registration step | Larger registration step; possible BAC/CBAM ↔ BAR duplication |
| Execution | Gate applies; discovery trigger point unresolved (D2.5) | Gate + exclusive Engine-mediated execution path |
| Audit/assurance | Unchanged from current practice | Potential registry-mediated duplication of `record_audit`/`publish_event` |
| C-024 | No direct impact either way | No direct impact either way |
| Follow-on governance work | `IMP-001` amendment (Decision 6) more likely needed | `WP-RTA-001`-scale initiative likely needed |

No dimension in this table is scored, ranked, or characterized as better for either option.

#### D2.9 — BAR vs. `IMP-001` Boundary (re-confirmed, not re-litigated from §8)

§8 of this document already established the design-time (BAC/CBAM) vs. runtime (BAR) boundary. D2 adds one further distinction `§8` did not need to make: within `§6.22` itself, only the cataloguing obligation (`§6.22.2`, restating `SD-002-034`), the execution gate (`§6.22.7`/`§6.22.15`, restating `COM-001-005`), and discovery-exclusivity (`§6.22.8`, reinforced by the independently LOCKED `RTA-001 §6.6`) trace to a LOCKED source outside `IMP-001` itself. Every other `§6.22` subsection (ownership functions, contents, attributes, status, versioning, dependency management, governance workflow, observability) is `IMP-001`'s own Active-methodology content, with no LOCKED counterpart found anywhere else in `COM-001`/`CMD-001`/`SD-002`/`PLT-001`/`GRC-001`/`OPM-001`/`ONT-001`. This is the same class of finding `CMD-001 §8.10`'s own "Architectural Enhancement (Recommended)" framing independently suggests (D2.3) — two different documents, read separately, both point toward BAR's fuller elaboration being methodology/recommendation rather than constitutional mandate, though neither source states this conclusion explicitly, and this document does not treat convergence between two non-LOCKED characterizations as itself a LOCKED finding.

#### D2.10 — BAR vs. `WPR-001` vs. CBOR Boundary (re-confirmed against §9 of this document)

| Mechanism | Currently governs | Evidence | Potential BAR interaction | Conflict/duplication? |
|---|---|---|---|---|
| `WPR-001` | WP-level status/certification | `WPR-001 §3` header, no BAR field | Decision 7 (unresolved: column vs. separate index) | None currently — nothing to duplicate yet |
| CBOR (`CBOR-INDEX.md`) | Business Object registration | `CBOR-INDEX.md §1` | None — `ONT-001 §2` confirms BAR and CBOR are structurally distinct regardless of D2's outcome | None, at any D2 scope |
| Charter/BAC/CBAM | Design-time BA content | `IMP-001 §6.7`/`§6.14`, WP-16–22 Charters | Full-scope BAR (`§6.22.6`) would need to express authorization/workflow/events/AI a second time unless synchronized with the design-time artifact — a duplication risk unique to Option B, not Option A (Option A's minimal attribute set does not overlap with BAC/CBAM's own fuller content) | Possible under Option B only; not resolved here (no mechanism design) |
| Capability registry (`CAP-001`) | Capability-level identity/status | `CAP-001`, zero BAR mentions | None — one layer above WP/BA | None |

This document does not design the future architecture and does not assume BAR should replace or merely duplicate `WPR-001`/CBOR — both remain open per Decision 7 and this table's own findings.

#### D2.11 — Existing Business Activity Impact (using the actual inventory, no migration performed)

- **Implemented/certified BAs (WP-01–WP-19, minus WP-13):** under Option A, a retroactive exercise (if Decision 3 selects it) would need only identity + a registration record per BA; under Option B, the same exercise would need full `§6.22.6` metadata population. Neither option performs this exercise here.
- **Chartered/closed, previously-deferred (WP-20/C-021, WP-21/C-022):** each capability's own prior BAR deferral (`ADR-037`, `ROD-C022-B D10`) is unaffected by D2 either way — D2 concerns the future mechanism's scope, not a reopening of either capability's own decision.
- **C-024 BA-01:** NOT STARTED; unaffected either way (D2.13).
- **No identifier is assigned and no Business Activity is registered by this section**, regardless of which option a future decision selects.

#### D2.12 — C-024 Impact

- **WP-22:** unaffected — D2 concerns a future mechanism's scope, not any capability's own governance chain.
- **BA-01:** unaffected — remains NOT STARTED.
- **CBOR `BIA-000001`:** unaffected — CBOR is structurally independent of BAR (D2.10).
- **Charter:** unaffected.
- **Implementation readiness:** unaffected — `D10` already establishes that BAR treatment (at any future scope) does not block BA-01's implementation from proceeding once CBOR/Charter prerequisites are separately satisfied.
- **Future dependency, described not created:** whichever scope D2 eventually selects would define what C-024 BA-01 (or any capability) must eventually satisfy under `COM-001-005`'s own execution gate, if and when D10's own deferral is later revisited — a future contingency, not a current blocker. **`D10` is not reinterpreted, reopened, or narrowed by this section.**

#### D2.13 — Dependencies with D3/D5/D6/D7 (none pre-decided)

| Decision | Relationship to D2 | Can D2 be decided without it? |
|---|---|---|
| D3 (retroactivity) | D2's scope determines *how large* a retroactive exercise would be, but D3 (whether to do one at all) is logically independent of *which* scope is chosen — D2 does not need D3 answered first, though D3 needs D2 answered first (already established in §5's dependency table) | Yes — D2 can be decided before D3 |
| D5 (identifier authority) | D2 determines what a BAR registration record contains, but not who assigns the identifier within it — D5 remains a separate governance-authority question at any D2 scope | Yes — D2 can be decided before D5 |
| D6 (`IMP-001` amendment) | Directly shaped by D2's outcome (D2.7: minimal scope makes a `§6.22` amendment more likely needed; full scope makes it less likely needed, since `§6.22` would then describe what is actually built) | No — D6 cannot be meaningfully decided before D2 |
| D7 (`WPR-001` vs. index) | Partially shaped by D2 (a minimal catalogue's placement question is smaller in scope than a full engine's), but the structural argument for a separate index (D2.10, `ONT-001 §2`'s BA-vs-WP centricity distinction) applies at either D2 scope | Partially — the *structural* case for D7 does not depend on D2, but the *content* of what would populate either placement does |

No dependent decision (D3, D5, D6, D7) is pre-decided by this section.

#### D2.14 — Exact Question for the Repository Owner

"Given that AUREX establishes a canonical enterprise BAR (Decision 1), what is its scope: the minimum LOCKED-compliant catalogue (identity + registration + execution gate + discovery-exclusivity), the full `IMP-001 §6.22` Business Activity Engine design (all fifteen subsections), or does the Repository Owner wish to designate a different scope boundary than either — and if so, which specific `§6.22` responsibilities are included?"

#### D2.15 — Explicit Statement

~~**D2 remains UNDECIDED. No BAR scope option has been selected.**~~ *(Superseded 2026-09-20 — see §0b.)* **D2 has been selected — Option A, LOCKED minimum scope (recorded 2026-09-20, §0b).** Decisions 3, 5, 6, and 7 remain unselected — none is silently resolved by D2's own selection.

---

### Decision 3 — Enterprise BAR Registration Retroactivity (full decision preparation, expanded 2026-09-20 following D1/D2's selection)

**Status: D3 — DECIDED — Option A (retroactive registration, all 21 rows) selected, recorded 2026-09-20, §0c above.**

#### D3.1 — Decision Statement

Given that AUREX establishes a canonical enterprise BAR (D1) scoped to the LOCKED minimum (D2 — cataloguing/registration, canonical identity, execution-time gate, discovery-exclusivity), does BAR registration apply retrospectively to Business Activities that already exist in the repository, or prospectively only to future Business Activities?

#### D3.2 — Why D3 Is Required

D1/D2 establish *that* a BAR will exist and *what minimum it must contain*, but decide nothing about *when* that obligation attaches relative to a Business Activity's own history. The investigation's own §7 finding — independently re-confirmed below — is that nineteen of twenty-two Work Packages never raised the BAR question at all, not because any LOCKED text exempts them, but because the question went undiscovered. Once a BAR actually exists (per D1), this silent gap becomes an active question the Repository Owner must resolve rather than an abstract one.

#### D3.3 — Authoritative Source Basis (re-verified directly for this section)

- `SD-002-034` formalization note — `[LOCKED]`, re-read verbatim: "every Activity satisfying `SD-002-034` is catalogued in the Business Activity Registry" — unconditional, no temporal qualifier.
- `COM-001-005` — `[LOCKED]`, re-read verbatim: "No commercial Business Activity shall be executed until registered in the BAR" — phrased as a gate on the *act* of execution, not on a stated calendar date; does not state whether it applies only to BAs first executed after some future date, or to every execution event including of an already-implemented BA.
- `COM-001-060` — `[LOCKED]`, re-read verbatim: registered "once implemented" — a lifecycle-relative trigger ("once implemented"), not a calendar-relative one; textually silent on whether "once implemented" means "once implementation completes, whenever that was" (which would include historical BAs) or "once implementation completes, from this decision forward" (which would not).
- `PLT-001-004`/`-030`, `GRC-001-008`/`-070` — `[LOCKED]`, identical formula, re-verified, same silence.
- `RTA-001 §6.6` — `[LOCKED]`, re-read verbatim: "shall discover executable Business Activities exclusively through the Business Activity Registry" — silent on whether this exclusivity applies to Business Activities that were already executable before the Registry existed.
- `IMP-001 §6.22` (`§6.22.1`–`§6.22.15`, re-read in full for D2 and re-checked here) — contains no transition, migration, grandfathering, or retroactivity clause anywhere in its fifteen subsections. `§6.23.11` ("Version Migration") governs migration *between versions of an already-registered Business Activity*, not the initial-registration transition of a pre-existing, never-registered one — a different question, not textually applicable here.
- `CLAUDE.md` — re-searched in full for `BAR`, `retroactiv`, `grandfather`, `transition` in a Business-Activity-registration sense: **zero relevant hits**, re-confirmed.
- Repository-wide search performed fresh for this section across `architecture/02-Constitutional/` for `grandfather`, `transition`, `migrat`, `retroactiv`, `existing Business Activit`, `already implemented`, `already registered`: no hit anywhere ties any of these terms to Business-Activity-registration timing. The `CMD-001`/`IMP-001` hits found (version migration, state-transition lifecycles, schema-migration discipline) all concern different subjects — an individual Business Activity's own runtime state machine, or CBOR/schema versioning — not the transition of a *pre-existing, unregistered* Business Activity into a *newly-created* registry.

#### D3.4 — Actual Existing-Business-Activity Inventory (re-derived directly from `WPR-001`, `CBOR-INDEX.md`, and each cited governance chain — not invented, no identifier assumed where none exists)

| Capability | WP | BA | Charter state | Implementation state | Certification | Existing BA Identifier | Existing BAR registration | Evidence |
|---|---|---|---|---|---|---|---|---|
| C-004 | WP-01 | BA-01–08 (informal ordinal labels) | Predates formal Charter convention | IMPLEMENTED | CLOSED — CERTIFIED | **None** | **None** | `IMP-REPORT-WP-01` |
| C-003 | WP-02, WP-06 | Various (informal) | Predates formal Charter convention | IMPLEMENTED | CLOSED — CERTIFIED | **None** | **None** | `IMP-REPORT-WP-02`/`WP-06` |
| C-007 | WP-03 | BA-01,02,03,06–11 (9 of 11; BA-04/05 BLOCKED) | Predates formal Charter convention | PARTIAL | CERTIFIED (partial) | **None** | **None** | `IMP-REPORT-WP-03` |
| C-005 | WP-04 | BA-01–09 | Predates formal Charter convention | IMPLEMENTED (9/9) | CLOSED — CERTIFIED | **None** (6 Business *Objects* registered — not BAs) | **None** | `IMP-REPORT-WP-04` |
| C-002 | WP-05 | BA-01–06 | Predates formal Charter convention | IMPLEMENTED (minimum scope) | CLOSED — CERTIFIED | **None** (1 Business Object registered) | **None** | `IMP-REPORT-WP-05`; `ADR-015` — zero BAR mentions |
| C-006 | WP-07 | (informal) | Predates formal Charter convention | IMPLEMENTED | CLOSED — CERTIFIED | **None** | **None** | `WPR-001` WP-07 row |
| C-001 | WP-08 | (informal) | Predates formal Charter convention | IMPLEMENTED | CLOSED — CERTIFIED | **None** | **None** | `WPR-001` WP-08 row |
| C-008 | WP-09 | (informal) | Predates formal Charter convention | IMPLEMENTED | CLOSED — CERTIFIED | **None** | **None** | `WPR-001` WP-09 row |
| C-041 | WP-10 | (informal) | Predates formal Charter convention | IMPLEMENTED | CLOSED — CERTIFIED | **None** (1 Business Object registered) | **None** | `IMP-REPORT-WP-10`; `ADR-019` — zero BAR mentions |
| C-093 | WP-11 | BA-01/02/03 | Predates formal Charter convention | IMPLEMENTED — PARTIAL (stub backing) | CLOSED — CERTIFIED | **None** | **None** | `IMP-REPORT-WP-11` |
| C-094 | WP-12 | BA-01/02/03 | Predates formal Charter convention | IMPLEMENTED — PARTIAL (stub backing) | CLOSED — CERTIFIED WITH FINDINGS | **None** | **None** | `IMP-REPORT-WP-12` |
| — (Runtime, cross-cutting) | WP-13 | Not decomposed into formal BAs | N/A | IN PROGRESS | Not certified | **N/A — not a chartered Business Activity** | **N/A** | `WPR-001` WP-13 row |
| C-090/091/092 | WP-14 | BA-01–05 | Predates formal Charter convention | IMPLEMENTED | CLOSED — CERTIFIED | **None** | **None** | `IMP-REPORT-WP-14` |
| C-066 | WP-15 | BA-01 | Predates formal Charter convention | IMPLEMENTED | CLOSED — CERTIFIED | **None** | **None** | `IMP-REPORT-WP-15` |
| C-040 | WP-16 | BA-01 | `WP-16` Charter | IMPLEMENTATION COMPLETE | CLOSED — CERTIFIED | **None** | **None** (not a `COM-001` construct — never raised) | `IMP-REPORT-WP-16`; `CERT-WP-16` |
| C-023 | WP-17 | BA-01 | `WP-17` Charter | IMPLEMENTED | Gate 1 PASSED (per R9) | **None** | **None** (not a `COM-001` construct — never raised) | `WPR-001` WP-17 row |
| C-003 (runtime binding) | WP-18 | Repository-wide infra, backend-only | `WP-18` Charter | IMPLEMENTATION COMPLETE | CLOSED — CERTIFIED — RELEASE-READY | **None** | **None** (never raised) | `IMP-REPORT-WP-18`; `CERT-WP-18` |
| C-132 | WP-19 | BA-01 | `WP-19` Charter | IMPLEMENTATION COMPLETE | FORMALLY CLOSED — CERTIFIED — RELEASE-READY | **None** | **None** (not a `COM-001` construct — never raised) | `WPR-001` WP-19 row |
| C-021 | WP-20 | BA-01 | `WP-20` Charter | IMPLEMENTED | CLOSED — CERTIFIED — RELEASE-READY | **None** | **Explicitly raised and deferred** (`ADR-037 §Decision item 5`, 2026-09-08) | `ADR-037` |
| C-022 | WP-21 | BA-01 | `WP-21` Charter | IMPLEMENTATION COMPLETE | CLOSED — CERTIFIED — RELEASE-READY | **None** | **Explicitly raised and deferred** (`ROD-C022-B D10`, 2026-09-15) | `ADR-040`; `ROD-C022-B` |
| C-024 | WP-22 | BA-01 | `WP-22` Charter | **NOT STARTED** | Not certified | **None** | **Explicitly raised and deferred** (`ROD-C024-BAR §0`, D10, Option A, 2026-09-19) | `ROD-C024-BAR...md` |

**Categorization (per Step 2's own A–F taxonomy):**
- **A. Implemented/certified:** WP-01, 02, 04, 05, 06, 07, 08, 09, 10, 11, 12, 14, 15, 16, 17 (Gate 1 only, per R9 note), 18, 19, 20, 21 — nineteen Work Packages.
- **B. Implemented but uncertified:** **none independently identified** — WP-03 is certified-partial (not "uncertified"); WP-13 is in-progress, not "implemented." No Work Package fits this category as distinct from A or D.
- **C. Chartered but not implemented:** WP-22/C-024 BA-01 only — Charter exists, `WPR-001`-registered, CBOR-registered (`BIA-000001`), implementation NOT STARTED.
- **D. Deferred/non-started BAs beyond category C:** none independently identified beyond WP-22 itself.
- **E. Explicitly defined but not WP-registered activities:** none independently identified — every informal `BA-NN` label found traces to a WP already in the table above; no "orphan" Business Activity definition exists outside a WP.
- **F. Activities mentioned only in methodology/examples:** `BA-000089` — an illustrative identifier example cited in `SD-002-004`, `CMD-001 §26.4a`, `IMP-001 §6.22.1b`. **Not a real Business Activity — an example only, re-confirmed.**

**No `BA-NNNNNN` identifier exists for any row in this table.** No WP number is equated with a Business Activity Identifier; no Charter is equated with a BAR registration; no CBOR identifier (`OFR-000001`, `CAC-000001`, `BIA-000001`, `AEO-000001`, `CFG-000001`, `SCI`/`POC`/`IMC`/`RVC`/`VLC`/`RSC`-000001) is equated with a Business Activity Identifier — each is a distinct, structurally separate identifier space (`ONT-001 §2`).

#### D3.5 — Explicit LOCKED Requirements Relevant to Timing/Retroactivity

| Question | Finding | Source | Explicit or inferred? |
|---|---|---|---|
| Does any LOCKED source explicitly address existing Business Activities? | **No** | Searched `SD-002-034`, `COM-001-005`/`-060`, `PLT-001-004`/`-030`, `GRC-001-008`/`-070`, `RTA-001 §6.6` in full — none mentions "existing," "previously implemented," or an equivalent phrase in connection with BAR | Silence, not a finding either way |
| Does any LOCKED source explicitly address future-only application? | **No** | Same sources — none states "future" or "from this date forward" | Silence, not a finding either way |
| Does any source provide a transitional clause? | **No** | Repository-wide search, this section | Genuine governance gap |
| Does any source provide a grandfathering mechanism? | **No** | Same search | Genuine governance gap |
| Does any source define "migration" in this context? | **No** — `IMP-001 §6.23.11`'s "Version Migration" concerns version-to-version migration of an *already-registered* BA, a textually different subject | `IMP-001 §6.23.11` | Explicit text exists, but for a different question |
| Does any source define registration timing generally? | **Partially** — `COM-001-005` ties BAR to *execution*, `COM-001-060` ties it to "once implemented" — both lifecycle-relative, neither calendar-relative | `COM-001-005`/`-060` | Explicit, but does not resolve retroactivity either way |
| Does any source define execution eligibility for a BA that predates the registry? | **No** | Same search | Genuine governance gap |

**This document does not infer retroactivity merely because the obligation says "every Activity" (`SD-002-034`), and does not infer grandfathering merely because no transition clause exists.** Both are equally available readings of the same silence, and this section records that silence as a genuine governance gap rather than resolving it by inference in either direction — consistent with the governing instruction for this task.

#### D3.6 — OPTION A — Retroactive Registration ✅ SELECTED (recorded 2026-09-20, per §0c)

**Text:** All Business Activities already existing within the repository's defined scope (the 21-row inventory in D3.4, categories A–C) must ultimately be catalogued/registered in the enterprise BAR.

**Source basis:** `SD-002-034`'s own unconditional, universal phrasing ("every Activity satisfying `SD-002-034`") — nothing in it textually distinguishes an already-implemented BA from a future one.

**Which existing BAs would need treatment:** All nineteen category-A Work Packages' own Business Activities (informal `BA-NN` labels, no `SD-002-004`-form identity), plus category-C's WP-22/C-024 BA-01 once it reaches whatever lifecycle point registration attaches to.

**Whether identifiers must be assigned:** Yes, under this option — every row in D3.4 currently shows "None" in the Existing BA Identifier column; retroactive registration would require assigning a `BA-NNNNNN` identifier to each, per `SD-002-004`'s own identity form (assignment authority/timing remains Decision 5, not decided here).

**Whether historical activities need metadata reconstruction:** Depends on D2's already-decided minimum scope (identity + registration record + gate + discovery only) — under D2's own LOCKED-minimum scope, reconstruction would be limited to identity and a registration record, not the fuller `§6.22.6` attribute set D2 already excluded from the decided scope.

**Whether already-certified BAs require governance retrofit:** This is a live, unresolved question this section flags rather than answers — `CLAUDE.md §19.7`'s Business Activity Completion Gate does not currently name BAR as a completion criterion for any of the nineteen already-`CLOSED — CERTIFIED` Work Packages; whether retroactive registration would be treated as reopening that closed status, or as a separate, non-reopening administrative act, is not stated by any source examined.

**Whether execution is affected before retrofit:** Under this option, if the execution-time gate (`COM-001-005`, part of D2's decided minimum) is read to apply to *every* execution event including of an already-implemented BA, then an unregistered historical BA could, in principle, become non-executable the moment BAR becomes operational, until retrofitted. No source states whether this reading is intended (§D3.11 below).

**Whether `WPR-001`/Charter/CBOR records are sufficient sources for reconstruction:** `[FACT]`, re-confirmed — every WP examined has an `IMP-REPORT-WP-XX`, and several have a Charter narrating BAC-equivalent content in prose; these could plausibly source an identity + registration record reconstruction, but no source states they are *sufficient* or *authoritative* for that purpose — this is an unresolved methodological question, not decided here.

**Whether any existing BA could remain outside BAR:** Not addressed by any source under this option's own text — `SD-002-034`'s universal phrasing does not carve out an exception for any specific WP.

**Whether transition sequencing is needed:** `[INFERENCE]`, disclosed as such — twenty-one rows require some ordering if retroactive registration is selected, but no source specifies one; this section does not propose a sequence.

**No retrofit is performed by this section.**

#### D3.7 — OPTION B — Prospective Registration

**Text:** BAR registration applies only to Business Activities created/authorized after the enterprise BAR becomes operational; the 21-row existing inventory (D3.4) is not retroactively registered.

**Source basis:** the unbroken fact that no Work Package to date — including four already `CLOSED — CERTIFIED — RELEASE-READY` (WP-17 partially, WP-19, WP-20, WP-21) — was ever required to register in a BAR to reach that status, and no gate (`CLAUDE.md §19.7b`'s five-gate sequence, applied to each) treated the undischarged obligation as a release blocker for any of them.

**Treatment of already-existing BAs:** remain exactly as currently governed — Charter, `IMP-REPORT`, Certification/V&V/Release-Readiness records — with no BAR entry.

**Whether they remain executable:** `[Unresolved, same ambiguity as D3.6]` — if the execution-time gate is read as attaching only to newly-registered BAs going forward, existing BAs remain executable without interruption; if read as a universal, retroactive-in-effect gate the moment BAR exists, they would not, regardless of which option (A or B) is selected for *new* registration — this is the same D3.11 ambiguity, not created or resolved by choosing Option B.

**Whether existing governance artifacts remain authoritative:** `[FACT]`, under this option, yes — no source displaces `IMP-REPORT-WP-XX`/Charter/Certification records as the authoritative account of an existing BA's own governance history.

**Whether execution-time gating can coexist with grandfathered BAs:** This is precisely D3.11's own open question — Option B's own text does not itself state a grandfathering rule; it states only that *new* registration does not apply to *existing* BAs, which is a narrower claim than "existing BAs are exempt from the execution gate forever." This document does not manufacture a grandfathering rule to fill that gap.

**Whether explicit transitional treatment is required:** `[RO DECISION REQUIRED]`, flagged, not resolved — if the execution gate's own scope is read broadly, some transitional statement would eventually be needed even under Option B; this section identifies the need without proposing the statement's content.

**Whether future BAs alone are gated:** Yes, under this option's own text — the twenty-one existing rows in D3.4 are not part of the registration population Option B creates going forward.

**This option does not create a permanent exemption by itself** — it is a statement about registration *timing* for a specific set of already-existing BAs, not a statement that `COM-001-005`/`-060`'s own LOCKED obligation is waived for them; the obligation's own text remains outstanding for those BAs regardless (mirroring the reasoning already established for Decision 1's own Option B, §12 of this document).

#### D3.8 — Additional Source-Supported Option

**A third, materially distinct option is genuinely supported by the inventory itself (D3.4), not manufactured for symmetry:** *retroactive registration limited to Business Activities that have reached a specific lifecycle trigger point, with the rest treated prospectively.* Two forms of this are visible in the actual evidence:

- **Trigger = "currently executable in production-shaped form."** All nineteen category-A (implemented/certified) rows would register; category C (WP-22/C-024, NOT STARTED) would be treated prospectively, since it has not yet reached the point `COM-001-060`'s own "once implemented" language contemplates.
- **Trigger = "already explicitly raised the BAR question."** Only WP-20/C-021, WP-21/C-022, and WP-22/C-024 — the three capabilities whose own governance chain already named BAR as an outstanding item (`ADR-037`, `ROD-C022-B D10`, `ROD-C024-BAR D10`) — would register under this narrower reading; the other eighteen (which never raised the question at all) would not, absent a separate decision.

Both variants are genuinely distinguishable from Option A (all 21 rows) and Option B (zero existing rows) by the inventory's own structure (D3.4's A/C categorization, and the "raised vs. never raised" column), not invented to inflate the option count. Neither is selected here.

#### D3.9 — Execution-Time Consequences (D2's scope includes the execution gate and discovery-exclusivity — analyzed against each option, not designed)

| Question | Option A (retroactive) | Option B (prospective) | Additional option (trigger-based) |
|---|---|---|---|
| Can an existing BA execute if not registered? | Only until its own retrofit completes (if the gate is read as universal) — an unresolved reading either way (D3.11) | Yes, if existing BAs are read as outside the gate's practical scope — same unresolved reading | Depends on which trigger a given BA falls under |
| Can a future BA execute before BAR registration? | No — `COM-001-005`'s gate applies to any BA reaching execution, and Option A does not change that for future BAs either | No — same, Option B's own scope is "future BAs register prospectively," not "future BAs are exempt" | Same — no option under consideration exempts future BAs from the gate |
| Does the option imply a transition period? | Yes — a backfill exercise across 21 rows, sequencing not specified (D3.6) | Not for existing BAs; potentially yes if a later trigger-based retrofit is added | Yes, for whichever subset is chosen |
| Does the option create a runtime exception/grandfathering mechanism? | No — it resolves the question by registering everything, so no exception is needed | Implicitly, yes, in effect — existing BAs continue executing without BAR registration, which is a de facto exception even if not labelled one | Yes, for whichever rows are excluded from the immediate trigger |
| Would such an exception require governance authorization? | N/A | `[RO DECISION REQUIRED]`, flagged — if Option B is ever selected and the execution gate is read broadly, an explicit governance statement authorizing continued execution of unregistered existing BAs would likely be needed; this section does not draft one | Same, for the excluded subset |

**No runtime mechanism is designed by this table** — it states governance consequences only.

#### D3.10 — Relationship to Existing Governance (`WPR-001` / Charter / `IMP-001` / CBOR / future BAR index — D5/D6/D7 identified as dependencies, not resolved)

- **`WPR-001`:** re-confirmed, no BAR field exists in its table structure (`§3` header, unchanged since D1's own review). Whether a retroactive registration exercise would be recorded there or in a separate index is Decision 7's own question, not decided here — D3 only establishes *whether* a backfill happens, not *where* it would be recorded.
- **Charter:** existing Charters (WP-16 through WP-22) already narrate BAC-equivalent content in prose; none would need retroactive amendment under any D3 option, since Charter content is a `IMP-001 §6.7`/`§6.14` design-time artifact, structurally distinct from BAR (§8 of this document).
- **`IMP-001`:** contains no retroactivity clause (D3.5); whether `§6.22` itself needs amendment to address transition is folded into Decision 6, not decided here.
- **CBOR:** structurally independent of BAR (`ONT-001 §2`, re-confirmed); a Business Activity's own BAR-registration timing has no bearing on any of the ten already-registered Business Objects' own CBOR status, and vice versa.
- **Future BAR index:** whichever form Decision 7 eventually selects (a `WPR-001` column or a separate `BAR-INDEX.md`) would be the eventual recording mechanism for whatever D3 selects — this section does not presuppose which.

**D5 (identifier authority) and D6 (`IMP-001` amendment) are explicitly identified as dependencies, not resolved:** D3's own Option A cannot be executed without D5 first (or concurrently) establishing who assigns the 21 missing identifiers and when; D6 interacts with D3 to the extent a retroactive-registration transition clause, if ever written, might itself be the `IMP-001` amendment D6 contemplates.

#### D3.11 — Transitional / Grandfathering Question (identified, not resolved)

The repository's existing governance is **silent** on: grandfathering, transitional execution, historical-certification interaction with a new registration requirement, existing runtime eligibility once a registry exists, and retrofit timing (D3.5). This silence creates a genuine, distinct governance question this section identifies as a consequence of D1/D2 rather than resolving: **once BAR exists and its execution-time gate is live (per D2's decided scope), does that gate apply to Business Activities that were already executing before BAR existed, or only to Business Activities that begin executing after BAR exists?** No source answers this. This document does not silently create a grandfathering rule to answer it, and does not silently assume retroactive gating either — both are flagged as the same open question D3.9's own table already surfaces, carried forward rather than resolved.

#### D3.12 — Existing Business Activity Impact (per Step 8's seven named items, consequence only, no modification performed)

| Item | Consequence under Option A (retroactive) | Consequence under Option B (prospective) |
|---|---|---|
| 1. C-040 / WP-16 | Would require identity + registration-record backfill; `CLOSED — CERTIFIED` status implication unresolved (D3.6) | No BAR entry; existing Charter/`IMP-REPORT-WP-16`/`CERT-WP-16` records remain authoritative unchanged |
| 2. C-023 / WP-17 | Same backfill question | Same — unchanged |
| 3. Approval Authority / WP-18 | Same backfill question, though WP-18 is repository-wide infra rather than a capability-scoped commercial BA | Same — unchanged |
| 4. C-132 / WP-19 | Same backfill question | Same — unchanged |
| 5. C-021 / WP-20 | Backfill would apply on top of `ADR-037`'s own existing BAR deferral — not a reopening of `ADR-037` itself, but a new act layered on it | `ADR-037`'s own deferral continues exactly as recorded; no new act |
| 6. C-022 / WP-21 | Same, layered on `ROD-C022-B D10` | `ROD-C022-B D10` continues exactly as recorded |
| 7. C-024 / WP-22 | BA-01 is NOT STARTED — falls outside the "already-implemented" backfill population either way; would be governed prospectively regardless of D3's outcome, per D3.4's own category-C placement | Same — BA-01's own treatment is unaffected by D3's choice, since it has not yet reached execution |

**No modification was made to any of the seven items above.**

#### D3.13 — C-024 Impact

- **`D10` status:** unchanged — `D10` (`ROD-C024-BAR_Treatment_Decision_Preparation.md §0`, Option A, deferred, scoped to C-024 BA-01 only) is neither reopened nor reinterpreted by this section.
- **Is D3 the same question as D10?** No — `D10` concerns whether C-024 BA-01 specifically must register *before implementation proceeds* (already answered: no, deferred). D3 concerns whether a *future enterprise BAR*, once it exists, would apply *retroactively to BAs implemented before it existed* — a question D10 explicitly disclosed as still outstanding ("the `COM-001-060` execution-time obligation remains outstanding... deferred pending a future enterprise-level BAR-mechanism decision") and did not itself resolve.
- **Does D3 automatically register BA-01?** No, and BA-01 is NOT STARTED in any case — it is not part of the "already-implemented" retroactive population under any D3 option (D3.4, D3.12 row 7).
- **Does D3 change WP-22, CBOR `BIA-000001`, or the Charter?** No.

#### D3.14 — Exact Question for the Repository Owner

"Given that AUREX establishes a canonical enterprise BAR scoped to the LOCKED minimum (D1/D2), does registration apply retroactively to the 21 Business Activities already existing in the repository (in whole, per Option A; in part, per the trigger-based additional option; or not at all, per Option B), and — regardless of which is chosen — does the execution-time gate apply to those existing Business Activities' own continued execution, or only to Business Activities that begin executing after BAR exists?"

#### D3.15 — Explicit Statement

~~**D3 remains UNDECIDED. No retroactive/prospective registration option has been selected.**~~ *(Superseded 2026-09-20 — see §0c.)* **D3 has been selected — Option A, retroactive registration for all 21 existing Business Activity rows (recorded 2026-09-20, §0c).** Decisions 5, 6, and 7 remain unselected — none is silently resolved by D3's own selection. No Business Activity was registered, no identifier assigned, and no retrofit performed by this recording.

---

### Decision 4 — Scope of a deferral, if Option B is selected

**Decision statement:** If BAR is formally deferred, does the deferral apply enterprise-wide (covering the nineteen Work Packages that never raised the question, and future non-commercial-domain Business Activities), or only to the specific capabilities that have already raised it case-by-case (C-021/C-022/C-024)?

**Why required:** each of the three existing case-by-case deferrals explicitly states it does not create a "repository-wide policy." If the Repository Owner's own enterprise-level deferral decision is itself drawn broadly, it would be the first artifact in this repository to actually create that repository-wide policy — a materially different act than any of the three precedents performed, and one this document flags rather than assumes.

**Authoritative sources:** `ADR-037 §Decision item 5`, `ROD-C022-B D10`, `ROD-C024-BAR §0` — each self-limiting, re-verified verbatim for this document.

**Option A (enterprise-wide deferral):** genuinely supported — nothing prevents the Repository Owner from making a broader decision than any prior capability-scoped one; this is exactly the kind of decision `ADR-037`/`ROD-C022-B`/`ROD-C024-BAR` each disclosed was outside their own capability-scoped authority to make.

**Option B (case-by-case only, left open for the next capability):** genuinely supported by simple continuation of the existing pattern — each future `COM-001` Section 5–9 capability raises and defers its own BAR question again, as three have already done.

**Consequence of each:** Enterprise-wide — the nineteen-Work-Package "undiscovered, not satisfied or exempted" pattern (investigation §7 finding) becomes formally, prospectively acknowledged and closed as a known, accepted condition rather than an open gap; future non-`COM-001` Business Activities (`PLT-001`/`GRC-001` domains, none yet implemented) would also be covered without needing to raise the question themselves. Case-by-case only — the pattern continues exactly as today; each future capability re-derives the same conclusion independently, as WP-20/21/22 each did.

**What it explicitly does not decide:** Decisions 5/6/7 — those apply only under Option A (Establish) and have no analogue under a deferral.

**Dependencies:** Decision 1 = Defer (precondition).

**Impact on existing governance:** if enterprise-wide, formally closes the nineteen-Work-Package open question the investigation surfaced in §7/§15 without resolving whether that pattern "requires remediation" — this document explicitly does not judge that question either, consistent with the investigation's own disclosed scope limit.

**Impact on future Business Activities:** determines whether every future capability must independently re-raise and re-defer the BAR question, or whether this decision covers them prospectively.

**Impact on C-024:** none — `D10` is unaffected either way, since it is a capability-scoped decision already made under the prior (undecided-enterprise-question) state.

**Would implementation/design work be triggered:** No — deferral, by definition, triggers no build.

**Exact RO question:** "If AUREX defers the enterprise BAR mechanism, does that deferral apply enterprise-wide, or does each future capability continue to raise and resolve the question individually?"

---

### Decision 5 — Enterprise BAR Business Activity Identifier Authority / Timing (full decision preparation, expanded 2026-09-20 following D1/D2/D3's selections)

**Status: D5 — DECIDED — Authority: Option A (BAR is canonical authority); Timing: at BAR registration. Recorded 2026-09-20, §0d above.**

#### D5.1 — Decision Question

Given D1 (Establish), D2 (LOCKED minimum scope, which already includes "canonical Business Activity identity" as one of its four decided responsibilities), and D3 (retroactive registration for all 21 existing rows) — who or what is authoritative for Business Activity Identifier assignment, and when is the identifier assigned? This section does not decide identifier format, exact prefix, registry implementation, BAR database structure, API, runtime mechanism, or retroactive migration mechanics.

#### D5.2 — Why D5 Is Required

D2 already decided that canonical Business Activity identity is part of the enterprise BAR's LOCKED-minimum scope, and D3 already decided that registration (which necessarily includes identity, per D2) applies retroactively to all 21 existing rows. Neither decision addressed *who* assigns the `PREFIX-NNNNNN` identifier or *at what governance point* — `SD-002-004` establishes only the identity's *format*, not its issuing authority or timing. Without D5, D3's own retroactive-registration direction cannot actually be executed for any of the 21 rows, and no future Business Activity can acquire an identity either.

#### D5.3 — Current Business Activity Identifier Inventory (re-verified directly for this section, not assumed unchanged)

Repository-wide search performed fresh for `Business Activity Identifier`, `BA-`, `BAI-`, `Activity Identifier`, `identifier authority`, `identifier assigned`, `registration identifier`, `canonical identity`, `registry identifier`:

| Item | Finding | Evidence |
|---|---|---|
| Any real Business Activity with an assigned `BA-NNNNNN` identifier | **None** | Repository-wide search, zero hits beyond the illustrative example below |
| Identifier format(s) in use for Business Activities | **None in use** — only a prescribed format exists (`PREFIX-NNNNNN`, `SD-002-004`), never applied | `SD-002-004`, `IMP-001 §6.22.1b` |
| Illustrative-only identifier | `BA-000089` | Cited in `SD-002-004`, `CMD-001 §26.4a`, `IMP-001 §6.22.1b` — explicitly a worked example, never an actual assignment, re-confirmed |
| Is any identifier assigned by `WPR-001`? | **No** — `WPR-001 §3`'s own table header (`WP \| Capability \| Capability Name \| Status \| Governing IRA \| Certification`) has no identifier column, re-confirmed unchanged | `WPR-001 §3` |
| Is any identifier assigned by Charter? | **No** — Charters (WP-16 through WP-22) use informal ordinal labels ("BA-01") in prose, never an `SD-002-004`-form identity | Direct inspection, WP-16–22 Charters |
| Is any identifier assigned by BAR? | **N/A** — no BAR mechanism exists yet (D1's own establishment has not been engineered) | Re-confirmed, unchanged since D1 |
| Is any identifier assigned by another registry? | **No** — `CBOR-INDEX.md` assigns **Business Object** identifiers (`OFR-000001`, `CAC-000001`, `BIA-000001`, `AEO-000001`, `CFG-000001`, and six `SCI`/`POC`/`IMC`/`RVC`/`VLC`/`RSC`-000001 entries), a structurally distinct namespace from Business Activity identity (`ONT-001 §2`, re-confirmed) | `CBOR-INDEX.md §3` |

**Explicit distinctions preserved, not equated:** a WP number (`WP-22`) is not a Business Activity Identifier; an informal Charter-level BA label (`BA-01`) is not a Business Activity Identifier; `BIA-000001` is a **Business Object** Identifier (Billing Arrangement, `CMD-001 §26`), not a Business Activity Identifier; no CBOR identifier of any kind is a Business Activity Identifier. **Re-verified: this remains true as of this section's own fresh search — nothing has changed since D1/D2/D3's own findings.**

#### D5.4 — LOCKED Requirements Concerning Business Activity Identity (re-extracted directly)

| Requirement | Source | Exact meaning | Authority | Timing | Evidence type |
|---|---|---|---|---|---|
| Every Business Activity possesses a globally unique, permanent identity | `SD-002-004` | `PREFIX-NNNNNN` form, e.g. `BA-000089` (illustrative) | **Not stated** | **Not stated** | `[LOCKED]` |
| Every Activity satisfying `SD-002-034` is catalogued in BAR | `SD-002-034` formalization note | Cataloguing obligation | **Not stated** — does not name BAR's own internal issuing authority | **Not stated** — "catalogued," no calendar or lifecycle point named | `[LOCKED]` |
| No commercial BA executed until registered | `COM-001-005` | Execution gate | **Not stated** | Ties registration to *before execution*, a floor not a specific point | `[LOCKED]` |
| BAR Integration, commercial domain | `COM-001-060` | Registered "once implemented" | **Not stated** | Lifecycle-relative ("once implemented"), not a specific authority/timing rule for the identifier itself | `[LOCKED]` |

**Finding: no LOCKED source specifies identifier authority or timing.** All four LOCKED provisions establish *that* identity/registration must occur and *before what gate* (execution); none names *who* assigns the identifier or *the precise governance point* within the implementation lifecycle at which assignment occurs. This is a genuine gap, not resolved by inference.

#### D5.5 — Active (Methodology) Requirements Concerning Business Activity Identity

| Requirement | Source | Exact meaning | Authority | Timing | Evidence type |
|---|---|---|---|---|---|
| Activity Identifier is the format `SD-002-004` establishes | `IMP-001 §6.22.1b` | "This section does not define a competing identifier format" | Cross-references `SD-002-004`; does not itself name an issuer | Not stated | `[ACTIVE]` |
| Activity Identifier is one of ten registry attribute categories | `IMP-001 §6.22.6` (Identity block) | Identity is a registry-held attribute | Implies the Registry *holds* the identifier once assigned; does not state the Registry *issues* it | Not stated — `§6.22.7`'s own registration-validation checklist checks for a complete "Business Activity Contract," not identity issuance specifically | `[ACTIVE]` |
| A Business Activity "shall not be executable until successfully registered" | `IMP-001 §6.22.7` | Execution gate, restating `COM-001-005` | Not stated | Ties the identity's own practical necessity to before-registration-completes, no earlier point specified | `[ACTIVE]` |

**Finding: `IMP-001` likewise does not specify identifier authority or timing** — it restates the LOCKED gate and confirms the format cross-reference, but assigns no issuing role to the Business Activity Engine, the Registry, or any other named actor.

#### D5.6 — Relationship to BAR, `WPR-001`, CBOR, Charter (identity boundaries, not decided)

| Artifact/mechanism | Current role | Identity authority | Relevant evidence | Possible D5 interaction |
|---|---|---|---|---|
| BAR (D1-established, D2-scoped) | Would hold canonical BA identity as part of its own decided LOCKED-minimum scope | **Candidate** — D2 already places identity inside BAR's own scope, but D2 did not decide BAR is the *issuer*, only that identity is part of what BAR *holds/tracks* | `D2.5`/`D2.6` of this document | Direct — Option A below |
| `WPR-001` | WP-level status/certification tracking, no identifier field | **Not currently an identity authority** for anything (WP numbers are not identifiers) | `WPR-001 §3` header | Only if Decision 7 later places identity assignment inside a `WPR-001` extension — not decided here |
| CBOR (`CBOR-INDEX.md`) | Business **Object** identity authority, via registering ADR | **Authoritative for Business Objects only** — structurally separate from Business Activities (`ONT-001 §2`) | `CBOR-INDEX.md §1`, `ONT-001 §2` | Procedural-pattern precedent only (§D5.7 below) — not itself an authority for BAs |
| Charter | Design-time BA content (informal ordinal label only) | **Not an identity authority** — no Charter has ever assigned an `SD-002-004`-form identity | Direct inspection, WP-16–22 | Possible timing candidate (assign at Chartering) — a timing option, not an authority mechanism, discussed at D5.8 |
| Capability registry (`CAP-001`) | Capability-level identity/status | **Not an identity authority** for Business Activities — one layer above WP/BA | `CAP-001`, zero BAR/BA mentions | None |

**No mechanism is currently, unambiguously canonical for Business Activity identity** — because none currently assigns one at all. Whether BAR itself becomes canonical, or an external act (mirroring CBOR's registering-ADR pattern) remains canonical with BAR merely recording the result, is precisely D5's own open question (§D5.7). **D7 (`WPR-001` vs. separate BAR index) is identified as a dependency, not decided:** where a future identifier is *recorded* (a `WPR-001` column vs. a separate index) is a placement question distinct from who *assigns* it — D5 does not resolve D7, and D7's own eventual resolution does not, by itself, resolve D5.

#### D5.7 — The CBOR Precedent: What Transfers and What Does Not (Step 5's own anti-analogy discipline)

`C-024`'s own `BIA-000001` is a **Business Object** Identifier (Billing Arrangement, `CMD-001 §26`) — re-confirmed, **not** a Business Activity Identifier, and this section does not create one by analogy to it. What the CBOR precedent (`ADR-039 §Decision item 1`, `ADR-040 §Decision item 1`, `ADR-041 §Decision item 1`, each re-verified directly for this section) actually establishes, and what does/does not transfer:

- **Transfers as a procedural pattern only:** each CBOR identifier was assigned at a single, discrete, Repository-Owner-authorized registering act (an ADR) — never at an earlier preparatory stage (`IRA-C024_CBOR_Eligibility.md` itself assigns no identifier; `ADR-041` does). This is evidence of *a* governance pattern this repository has actually used, transferable as a template for *how* a discrete assignment act could work, if the Repository Owner chooses to model Business Activity assignment on it.
- **Does not transfer:** the specific identifier value, prefix-derivation logic, or the CBOR register itself. `ONT-001 §2`'s own finding — "the registries of instances... BAR and CBOR are two distinct registries, neither a subset of the other" — means CBOR's own registering-ADR act has no automatic jurisdiction over Business Activity identity; extending the *pattern* to BAs would require a **new** application of that pattern to a new subject, not a transfer of CBOR's own existing authority.
- **Does not establish** that BAR itself must, or must not, be the issuer — the CBOR precedent is a Business-Object-side answer to "who assigns," useful only as comparison evidence for how this repository has resolved an analogous question once before, precisely per this document's own `[PRECEDENT]` classification discipline (a precedent, examined for procedure/comparison, never treated as automatically-transferable enterprise policy).

#### D5.8 — Authority Options

**OPTION A — BAR is the canonical Business Activity Identifier authority. ✅ SELECTED (recorded 2026-09-20, per §0d)** BAR itself (once built, at D2's own decided minimum scope, which already includes identity) issues and controls the identifier internally, at BAR-registration time.

- *Source basis:* `IMP-001 §6.22.2` ("The Registry is the source of truth"), `§6.22.6`'s own Identity attribute category, and D2's own prior decision that canonical identity is part of BAR's decided LOCKED-minimum scope — Option A is a natural extension of a scope decision already made, though D2 itself did not decide *this specific* authority/timing question.
- *What it authorizes:* BAR, once engineered, would generate/hold the identifier as part of its own registration act — no separate external registering act would be needed.
- *What it does not authorize:* any specific technical mechanism for how BAR would generate the identifier (sequence, database, service) — that is future engineering work, not decided here.
- *Assignment timing:* at BAR registration (the point `IMP-001 §6.22.7` already ties to the execution gate).
- *Authority/source of truth:* BAR itself.
- *Effect on existing BAs (D3's 21 rows):* each of the 21 rows would receive its identifier only once BAR is actually built and each row is individually registered into it — a later, engineering-dependent event, not something this decision performs.
- *Effect on future BAs:* every future BA would acquire its identity at the same BAR-registration point, once BAR exists.
- *Relationship to `WPR-001`:* none directly — Option A does not require `WPR-001` to hold or assign anything.
- *Relationship to CBOR:* none — structurally independent (`ONT-001 §2`).
- *Relationship to Charter:* none — Charters remain design-time, pre-registration artifacts under this option.
- *Dependency on D7:* Option A does not itself require D7 to be resolved first — BAR could hold/issue the identifier internally regardless of whether its own status is later tracked via a `WPR-001` column or a separate index.
- *Implementation consequence:* BAR's own eventual engineering design (out of scope here) would need an identifier-generation mechanism.
- *Unresolved questions:* whether BAR's own internal issuance requires a distinct human/governance approval step (mirroring the CBOR ADR's own Repository-Owner-authorized act) or could be a purely mechanical/automated act — not addressed by any source.

**OPTION B — An existing governance mechanism (a dedicated registering act, mirroring the CBOR-ADR pattern) remains identifier authority; BAR records but does not issue.** A discrete, Repository-Owner-authorized registering act (an ADR or equivalent) assigns the `BA-NNNNNN` identifier, structurally separate from and prior to (or alongside) BAR's own internal registry entry — BAR then records, rather than generates, the identifier.

- *Source basis:* the CBOR precedent (§D5.7) as a transferable *procedural* template — re-confirmed as the only actually-existing analogous governance mechanism in this repository, though not automatically authoritative for Business Activities by cross-domain default.
- *What it authorizes:* a dedicated Business-Activity-Identifier-registering act, distinct from BAR's own registry function.
- *What it does not authorize:* any claim that the *existing* CBOR-ADR mechanism itself already has jurisdiction over Business Activities — it does not (`ONT-001 §2`); Option B would require **establishing a new instance** of the same procedural pattern for a new subject, not merely reusing the existing one.
- *Assignment timing:* at the dedicated registering act, which could occur before, concurrently with, or as a formal precondition to BAR's own registration event — the exact relative sequencing is not decided here.
- *Authority/source of truth:* the registering act (e.g., an ADR), not BAR itself.
- *Effect on existing BAs:* the same 21-row population would each need its own registering act (mirroring the 21 separate CBOR-style ADRs this would imply, one per BA, unless a single omnibus act is chosen instead — not decided here) before BAR could record any of them.
- *Effect on future BAs:* every future BA would need its own registering act before BAR could record it — a heavier per-BA governance step than Option A's own internal-issuance model.
- *Relationship to `WPR-001`:* none directly, unless the registering act's own record is placed there (a Decision 7 question).
- *Relationship to CBOR:* procedural-pattern analogy only, not a shared registry (§D5.7).
- *Relationship to Charter:* none directly — the registering act would be a separate artifact from the Charter, mirroring how CBOR ADRs are separate from Charters today.
- *Dependency on D7:* stronger dependency than Option A's — where each registering act's own record lives is closely tied to Decision 7's own resolution.
- *Implementation consequence:* a new governance-artifact pattern (a Business-Activity-Identifier-registering act) would need to be established, mirroring but distinct from the existing CBOR-ADR pattern.
- *Unresolved questions:* whether a single registering act could cover multiple BAs (an omnibus act, given D3's own 21-row retroactive population) or whether one act per BA is required, mirroring CBOR's own one-ADR-per-object practice to date — not addressed by any source.

**No third, materially distinct option was found and none is manufactured for symmetry.** A hybrid ("BAR issues for future BAs; a registering act handles the 21-row retroactive backlog") is a sequencing/scope variant combining elements of A and B rather than a materially distinct third authority model — noted here, not presented as a separate "Option C," consistent with this document's own established practice (§12 of the investigation) of not manufacturing options for completeness.

#### D5.9 — Timing Options (treated as a distinct dimension from authority, per the governing instruction)

| Candidate timing point | Evidence for | Evidence against | Consequence for D3's 21-row population | Consequence for future BAs | Transition/migration rule required? |
|---|---|---|---|---|---|
| At Business Activity creation (informal definition) | None found | No source ties identity to the earliest, informal definition point | Would require reconstructing a "creation date" for each of the 21 rows, most of which predate any formal Charter convention (`WP-01`–`WP-15`) | Applies from the moment a BA is first conceived, before Charter | Yes — historical "creation" dates would need reconstruction |
| At Chartering | None found directly; Charters already narrate BAC-equivalent content (`IMP-001 §6.7`) | The CBOR precedent (§D5.7) shows identifiers are **not** assigned at an earlier preparatory/assessment stage — cutting against, not for, this option, by extension/analogy only, not directly | 21 rows have Charters (or `IMP-REPORT` equivalents) already — a usable trigger point if selected | Every future Charter would need to trigger assignment | Possibly — depends on whether pre-2026 informal Charters count |
| At WP registration (`WPR-001`) | `WPR-001` already registers every WP | `WPR-001`'s own table structure has no identifier field today (`[FACT]`) | All 21 rows are already `WPR-001`-registered — a usable trigger point if selected | Every future WP registration would need to trigger assignment | Possibly — `WPR-001`'s own structure would need extension (Decision 7 territory) |
| **At BAR registration ✅ SELECTED (recorded 2026-09-20, per §0d)** | `IMP-001 §6.22.7` ties registration to the execution gate directly | None found against | Requires BAR to actually exist and each of the 21 rows to be individually registered into it — the most source-direct option, but also the most engineering-dependent | Every future BA registers into BAR before executing, per `COM-001-005` | No separate rule needed — registration IS the trigger |
| At implementation authorization | None found | `COM-001-060`'s own "once implemented" language is a *later* point than authorization, not authorization itself | Would predate the point `COM-001-060` itself names | Would predate `COM-001-060`'s own trigger for future BAs too | Not directly addressed |
| Before first execution (a floor, not a specific point) | `COM-001-005`'s own gate — the only unconditional timing floor any source establishes | N/A — this is a minimum, not a specific point | Trivially satisfied by any option above, since none proposes assignment after execution | Same — a floor all other candidate points already satisfy | No — this is the constitutional floor every other option must respect, not a competing option |

**No timing point is chosen.** `COM-001-005`'s "before execution" is the only source-established floor; every other candidate point in this table is source-plausible but source-unconfirmed as *the* required point.

#### D5.10 — D3 Interaction (D3 is now RETROACTIVE — analyzed, not executed)

- **Are identifiers required before retroactive BAR registration can occur?** Yes — D2 already places canonical identity inside BAR's own decided minimum scope, and D3's own retroactive-registration direction (§0c) necessarily includes identity for each of the 21 rows, since D2's scope is what D3 said applies retroactively. D5 must therefore be resolved (at least at the authority/timing level this section addresses) before any actual identifier can be assigned to any of the 21 rows.
- **Must D5 be completed before any D3 execution?** Yes, for the identity component specifically — D3's own §0c already flagged this exact dependency ("D3's own execution explicitly depends on D5... being separately resolved before any actual identifier assignment can occur"); this section confirms and does not alter that finding.
- **Can the existing 21 BAs be identified from existing authoritative records?** Partially — every row in D3.4's inventory has at least a `WPR-001` entry and an `IMP-REPORT-WP-XX` (or equivalent) narrating its own scope and certification history; these are plausible *sourcing* material for a future registration act, but no source states they are *sufficient* for that purpose without further reconstruction (the same open question D3.6 already flagged).
- **Is historical reconstruction required?** Under D2's own decided minimum scope (identity + registration record only, not the full `§6.22.6` attribute set), reconstruction burden is limited to establishing each row's own identity and a basic registration record — not the fuller metadata a full-scope BAR would have required. This is a direct, favorable consequence of D2's own prior decision, re-confirmed here.
- **Is a separate future transition decision still needed?** Yes — the *sequencing* of a 21-row (or fewer, per any future exception) registration exercise (order, whether single omnibus act or 21 individual acts, who performs it) is not resolved by D5 alone and is not manufactured as an eighth enterprise decision here, consistent with `§14`'s own seven-question scope — it is flagged as necessary future implementation-planning work, triggered once D5's own authority/timing question is resolved.

**No migration is performed by this section.**

#### D5.11 — Existing Business Activity Impact (Step 9's seven named items, identifier state only, no assignment performed)

| Item | Does any identifier exist today? | Evidence |
|---|---|---|
| WP-16 / C-040 | **No** | `IMP-REPORT-WP-16`, `WPR-001` WP-16 row — informal "BA-01" label only |
| WP-17 / C-023 | **No** | `WPR-001` WP-17 row — informal "BA-01" label only |
| WP-18 (Approval Authority runtime binding) | **No** | `IMP-REPORT-WP-18` — repository-wide infra, no BA identifier |
| WP-19 / C-132 | **No** | `WPR-001` WP-19 row — informal "BA-01" label only |
| WP-20 / C-021 | **No** — `OFR-000001` is a Business **Object** identifier, not a Business Activity Identifier | `ADR-037`, `CBOR-INDEX.md` |
| WP-21 / C-022 | **No** — `CAC-000001` is a Business **Object** identifier | `ADR-040`, `CBOR-INDEX.md` |
| WP-22 / C-024 | **No** — `BIA-000001` is a Business **Object** identifier (Billing Arrangement), not a Business Activity Identifier for BA-01 | `ADR-041 §Decision item 6`, re-verified: "This ADR does not assign a Business Activity Identifier... No `BA-NNNNNN` identifier is assigned by this ADR to BA-01 or to any other C-024 Business Activity." |

**No identifier is assigned to any of these seven items, or to any other row in the 21-row inventory, by this section.**

#### D5.12 — C-024 Impact

- **`D10`:** unchanged — `D10` (`ROD-C024-BAR_Treatment_Decision_Preparation.md §0`, Option A, deferred, C-024 BA-01 only) is neither reopened nor reinterpreted by this section.
- **CBOR `BIA-000001`:** unaffected — remains a Business Object identifier, structurally distinct from any future Business Activity Identifier BA-01 might eventually receive.
- **WP-22 / Charter:** unaffected.
- **Implementation status:** remains NOT STARTED.
- **Future impact of D5 on C-024, described not created:** once D5's own authority/timing question is eventually resolved, and once BA-01 reaches whatever lifecycle point that resolution names as the assignment trigger, BA-01 would be eligible to receive a `BA-NNNNNN` identifier through whatever mechanism is chosen — but this remains a future contingency; **no Business Activity Identifier is assigned to BA-01 by this section, and the Charter is not changed.**

#### D5.13 — D6/D7 Dependencies (identified, not resolved)

| Question | Relationship to D5 |
|---|---|
| Can D5 be decided independently of D6 (`IMP-001 §6.22` amendment)? | Largely yes — D5 concerns *authority and timing*, a governance question; D6 concerns whether `IMP-001`'s own text needs amending to reflect D2's adopted scope, a documentation question. The two are not mutually exclusive, but D5's own outcome (especially if Option B is selected, introducing a new registering-act pattern `IMP-001` does not currently describe) could itself become part of what D6's eventual amendment would need to capture. |
| Can D5 be decided independently of D7 (`WPR-001` vs. BAR index)? | Partially — D5's own Option A (BAR-internal issuance) does not require D7 to be resolved first (§D5.8). Option B (a separate registering act) has a stronger practical dependency on D7, since where that act's own record is placed is closely tied to D7's own resolution. D5 does not decide D7 either way. |
| Does D5 affect D7? | Yes, in one direction — if Option B is selected, D7's own eventual resolution would need to accommodate a registering-act record in addition to whatever BAR-status placement D7 itself decides; if Option A is selected, D7 remains unaffected by D5's own choice. |
| Does D5 affect D6? | Possibly — see above; not decided here. |

**Neither D6 nor D7 is decided by this section.**

#### D5.14 — Evidence Matrix

| Assertion | Source | Evidence type |
|---|---|---|
| No Business Activity Identifier exists anywhere in the repository today | Repository-wide search, fresh for this section | `[FACT]` |
| `BA-000089` is illustrative only | `SD-002-004`, `CMD-001 §26.4a`, `IMP-001 §6.22.1b` | `[FACT]` |
| `SD-002-004` establishes format, not authority or timing | Direct re-read | `[LOCKED]`, absence noted |
| `IMP-001 §6.22.1b`/`§6.22.6`/`§6.22.7` do not name an issuer | Direct re-read | `[ACTIVE]`, absence noted |
| CBOR identifiers (`OFR`/`CAC`/`BIA`/`AEO`/`CFG`-000001, six `SCI`/`POC`/`IMC`/`RVC`/`VLC`/`RSC`-000001) are Business Object identifiers, not Business Activity identifiers | `CBOR-INDEX.md §3`, `ONT-001 §2` | `[FACT]` + `[LOCKED]` |
| CBOR identifiers assigned only at the registering ADR, never earlier | `ADR-039`/`-040`/`-041 §Decision item 1` | `[PRECEDENT]`, non-binding by cross-domain default |
| `ADR-041` explicitly does not assign a Business Activity Identifier to BA-01 | `ADR-041 §Decision item 6`, re-verified verbatim | `[FACT]` |
| `WPR-001` has no identifier column | `WPR-001 §3` header | `[FACT]` |

#### D5.15 — Exact Question for the Repository Owner

"Given that AUREX establishes a canonical enterprise BAR (D1) scoped to the LOCKED minimum including canonical identity (D2), and that registration applies retroactively to all 21 existing Business Activity rows (D3), who is authoritative for assigning a Business Activity's own `BA-NNNNNN` identifier — BAR itself, internally, at BAR-registration time (Option A), or a discrete, Repository-Owner-authorized registering act mirroring the CBOR-ADR pattern, with BAR recording rather than issuing the identifier (Option B) — and at what governance point does assignment occur?"

#### D5.16 — Explicit Statement

~~**D5 remains UNDECIDED. No Business Activity Identifier authority or timing option has been selected.**~~ *(Superseded 2026-09-20 — see §0d.)* **D5 has been selected on both dimensions — Authority: Option A, BAR is the canonical authority; Timing: at BAR registration (recorded 2026-09-20, §0d).** Decisions 6 and 7 remain unselected — neither is silently resolved by D5's own selections. No identifier was assigned or reserved by this recording.

---

### Decision 6 — Enterprise BAR / `IMP-001 §6.22` Relationship and Amendment (full decision preparation, expanded 2026-09-20 following D1/D2/D3/D5's selections)

**Status: D6 — DECIDED — Option A (no `IMP-001` amendment required) selected, recorded 2026-09-20, §0e above.**

#### D6.1 — Decision Statement

Given D2's decision to establish only the LOCKED minimum BAR scope, what is the correct governance relationship between BAR and `IMP-001 §6.22`, and does `§6.22` require amendment? This is a governance-boundary question, not an engineering one — it does not assume the minimum-scope selection automatically requires amendment, and does not assume `§6.22` must remain untouched either.

#### D6.2 — Why D6 Is Required

D2 selected a BAR scope (cataloguing/registration, canonical identity, execution-time gate, discovery-exclusivity) materially narrower than `IMP-001 §6.22`'s own fifteen-subsection design. D5 then decided BAR is the canonical identifier authority, at BAR-registration time — a specific answer `§6.22` itself does not give (D5.4/D5.5's own finding: `§6.22` never names an issuer). Once BAR is actually built at D2's decided scope, `§6.22`'s own text will describe additional responsibilities (status lifecycle, version management, dependency management, governance workflow, observability, the full attribute schema, and identifier-issuance silence) that the enterprise BAR, as decided, will not implement. Whether that gap between text and built system requires correcting `§6.22`'s own words, or is an acceptable, already-precedented condition, is D6's own question.

#### D6.3 — Source Hierarchy (Step 2, re-established directly from source headers, not assumed)

| Source | Classification | Basis |
|---|---|---|
| `SD-002-004`/`-034`, `COM-001-005`/`-060`, `PLT-001-004`/`-030`, `GRC-001-008`/`-070` | **LOCKED / constitutional** | Document headers, re-confirmed unchanged across all prior D1–D5 sections |
| `RTA-001 §3.6`/`§6.6` | **LOCKED / constitutional** | `RTA-001` document header: "Status: LOCKED," re-confirmed |
| `IMP-001 §6.22` (and `§6.7`/`§6.14`) | **Implementation methodology, Active** | `IMP-001` document header, line 6: "Status: Active — governs current engineering practice; evolves via Controlled Evolution (`ARCH-000 §12.6`)" |
| `ARCH-000 §12.6` | **Constitutional governance mechanism** | Re-read directly for this section: `ARCH-000 §12.6`'s own title is "**Constitutional** Evolution," and its own text opens "A **Locked/Released Constitutional Document** changes only by: CERT correction... ADR... Architecture Board approval... Versioning." |

**Finding — a source-hierarchy nuance disclosed, not resolved:** `IMP-001`'s own header cites `ARCH-000 §12.6` as its change mechanism, but `§12.6`'s own text, read directly, governs "A Locked/Released Constitutional Document" specifically — and `IMP-001` is explicitly **not** Locked/Released; it is Active. Whether `§12.6`'s full CERT-correction/ADR/Architecture-Board-approval machinery literally applies to an Active document's own evolution, or whether `IMP-001`'s citation of `§12.6` is a looser analogy to "changes go through governed process, not silent edits," is not resolved by any source this section examined. This bears on Option B's own mechanics (§D6.6) without being decided here.

1. **Which source is LOCKED/constitutional?** `SD-002`, `COM-001`, `PLT-001`, `GRC-001`, `RTA-001` — all re-confirmed.
2. **Which source is implementation methodology?** `IMP-001` in full, including `§6.22`.
3. **Is `IMP-001 §6.22` subordinate to or constrained by the LOCKED BAR decisions?** Yes — `§6.22.1a` itself states this directly, verbatim: "IMP-001 does not redefine Business Activity semantics here — per §1.2, it governs how the platform is built, not what is built." `§6.22` cannot itself expand or contract what `SD-002-034`/`COM-001-005`/`-060` require; it can only describe *how* the platform satisfies them.
4. **Is `§6.22` normative methodology, architectural prescription, or a mixture?** A mixture, re-confirmed from D2.6's own subsection-by-subsection classification (reused, not repeated, below at D6.4): some subsections restate a LOCKED requirement in engineering terms (`§6.22.2`, `§6.22.7`'s gate clause, `§6.22.15`'s gate clause), while most (`§6.22.3`, `§6.22.5`, `§6.22.6` beyond Identity, `§6.22.9`–`§6.22.13`) are `IMP-001`'s own architectural prescription with no independent LOCKED counterpart.
5. **Does any `§6.22` provision independently create a requirement stronger than D2?** No provision was found that imposes an obligation beyond what `SD-002`/`COM-001`/`PLT-001`/`GRC-001`/`RTA-001` already establish — `§6.22.1a`'s own self-limiting text (point 3 above) forecloses this by its own design.

**No unresolved source conflict was found between the LOCKED layer and `IMP-001`'s own text** — `§6.22.1a` already discloses `IMP-001`'s own subordinate role, so there is no genuine authority contest, only a **scope gap** (D2's narrower decided scope vs. `§6.22`'s fuller elaboration), which is a documentation-accuracy question, not a hierarchy conflict. This is a materially different finding than "a conflict exists requiring RO intervention to resolve authority" — no such intervention is needed on the hierarchy question itself; RO intervention (D6) is needed only on the narrower documentation-accuracy question.

#### D6.4 — Complete `§6.22` Mapping (reusing D2.6's own subsection classification, cross-referenced not repeated, with the BAR-after-D2 column added)

| `§6.22` item | Responsibility | BAR after D2? | `IMP-001` responsibility? | LOCKED source? | Status |
|---|---|---|---|---|---|
| `§6.22.1` Purpose | Framing statement | N/A (framing only) | Yes | No | Explanatory |
| `§6.22.1a` Constitutional Authority | Self-limiting disclaimer | N/A | Yes | No (but restates `§1.2`'s own scope limit) | Explanatory, load-bearing for D6.3 point 3 |
| `§6.22.1b` Identifier Strategy | Format cross-reference to `SD-002-004` | **Yes** — identity is D2's own decided scope | Format only; authority = D5, decided | Format: `[LOCKED]` (`SD-002-004`) | Partially superseded by D5 — see D6.8 |
| `§6.22.2` Architectural Principle | "Platform assets shall be registered... Registry is the source of truth" | **Yes** — restates the LOCKED cataloguing obligation | Yes, in engineering phrasing | Yes (`SD-002-034`) | Consistent with D2 |
| `§6.22.3` Registry Ownership | Nine Engine functions (Discovery, Version Resolution, Contract Validation, Execution Policy Resolution, Authorization Resolution, Workflow Integration, Event Configuration, AI Integration, Monitoring, Lifecycle Governance) | **No, except Discovery** | Yes | Only Discovery (`RTA-001 §6.6`) | **8 of 9 functions exceed D2's decided scope** |
| `§6.22.4` Registry Architecture | Diagram | N/A | Yes | No | Illustrative |
| `§6.22.5` Registry Contents | Ten metadata categories | **No, except Identity** | Yes | No | Exceeds D2 |
| `§6.22.6` Canonical Registry Attributes | Eight attribute groups | **Identity only** | Yes (seven of eight groups) | Identity only | Exceeds D2 for seven of eight groups |
| `§6.22.7` Activity Registration | Execution gate + seven-item validation checklist | **Gate: Yes. Checklist: No** | Checklist: Yes | Gate: `[LOCKED]` (`COM-001-005`) | Gate consistent with D2; checklist exceeds D2 |
| `§6.22.8` Activity Discovery | "Shall discover Business Activities exclusively through the Registry" | **Yes** | Restates, reinforced by `RTA-001 §6.6` | `[LOCKED]` via `RTA-001 §6.6` | Consistent with D2 (§D6.6 below) |
| `§6.22.9` Activity Status | Six-state lifecycle | **No** | Yes | No | Exceeds D2 |
| `§6.22.10` Registry Version Management | Version history | **No** | Yes | No | Exceeds D2 |
| `§6.22.11` Dependency Management | Cross-BA dependency tracking | **No** | Yes | No | Exceeds D2 |
| `§6.22.12` Registry Governance | Registration approval/activation/suspension/retirement as governed BAs | **No** | Yes | No | Exceeds D2 |
| `§6.22.13` Registry Observability | Nine metrics | **No** | Yes | No | Exceeds D2 |
| `§6.22.14` Relationship with CBAM | "CBAM describes what; Registry describes how" | N/A (boundary statement) | Yes | No | Explanatory, unaffected by D2 |
| `§6.22.15` Architectural Guarantees | Eight guarantees + execution-gate restatement | **Gate: Yes. Eight guarantees: No** | Eight guarantees: Yes | Gate: `[LOCKED]` | Gate consistent with D2; guarantees exceed D2 |

**Summary:** of `§6.22`'s fifteen subsections, four items are consistent with D2's decided scope as-is (`§6.22.2`, the gate clauses in `§6.22.7`/`§6.22.15`, and `§6.22.8`/discovery); the Identity portions of `§6.22.1b`/`§6.22.5`/`§6.22.6` are consistent in substance but superseded in specific detail by D5's own authority/timing decision (§D6.8); the remaining ten-plus items (validation checklist, status lifecycle, version management, dependency management, governance workflow, observability, and eight of nine `§6.22.3` Engine functions) describe responsibilities D2 did not include in the enterprise BAR's decided scope.

#### D6.5 — What D2 Changed for `§6.22` (Step 4, critical conflation test per Step 5)

D2 did not modify `§6.22`'s own text and does not, by itself, make an amendment necessary — **this section does not use D2 as proof that amendment is required**, per this task's own governing instruction. What D2 did was establish, as enterprise governance fact, that the *built* BAR will implement only four of `§6.22`'s many described responsibilities. This creates a **documentation-accuracy question** (does `§6.22`'s own text still accurately describe what the enterprise BAR is), not a **validity question** (D2's own decision is not invalidated by `§6.22`'s broader text, since `§6.22.1a` already subordinates `§6.22` to the LOCKED layer, and the LOCKED layer itself does not require the broader scope — D2.5's own finding, re-confirmed here).

**Critical conflation test, applied:** `§6.22` genuinely contains two different things — (A) responsibilities independently LOCKED via `SD-002-034`/`COM-001-005`/`-060`/`RTA-001 §6.6` (cataloguing, the execution gate, discovery), which remain BAR's regardless of D2's own wording, because they do not depend on `§6.22`'s own text to exist; and (B) `IMP-001`'s own broader Business Activity engineering methodology (validation checklist, lifecycle, versioning, dependency management, governance workflow, observability, eight of nine Engine functions), which are `§6.22`'s own architectural prescription, not independently LOCKED. **This section does not treat every mention of "Registry" in `§6.22` as proof that responsibility belongs inside the enterprise BAR** (category B items remain `IMP-001`'s own content, exercised by whatever mechanism actually performs them today — direct `record_audit`/`publish_event`, direct FastAPI authorization, etc., per D2.4's own responsibility-taxonomy finding) — **and does not strip a genuinely LOCKED responsibility out of BAR merely because it happens to appear inside `§6.22`** (category A items remain BAR's own scope regardless of how `§6.22` phrases them).

#### D6.6 — `§6.22.8` Activity Discovery — Re-Verified Wording (Step 6)

Re-read directly, again, for this section: `IMP-001 §6.22.8`, verbatim: *"The Business Activity Engine shall discover Business Activities exclusively through the Registry."* `RTA-001 §6.6`, verbatim: *"The Business Activity Engine shall discover executable Business Activities exclusively through the Business Activity Registry... Business Activities shall never be discovered through implementation-specific mechanisms."*

**Are these the same requirement?** No — they are textually distinct provisions in two different documents (one Active methodology, one LOCKED constitutional text), but they assert the same substantive rule (exclusive discovery through the Registry) using different, non-identical wording. **Do they reinforce each other?** Yes — `RTA-001`'s own LOCKED status independently establishes the rule `IMP-001 §6.22.8` also states in Active-methodology form; neither depends on the other for validity. **Do they establish a BAR responsibility, or a broader Runtime Execution Architecture obligation outside BAR?** Both — `RTA-001 §6.6` sits within `RTA-001`'s own Section 6 ("Business Activity Runtime," the broader Runtime Execution Architecture), while `IMP-001 §6.22.8` sits within BAR's own engineering specification. The rule is stated once at the Runtime-Architecture level (LOCKED) and once at the BAR-engineering level (Active), consistent with `RTA-001 §3.6`'s own summary ("Primary responsibilities include: Activity discovery... The Registry contains execution metadata") — discovery is a BAR *function* exercised *within* the broader Runtime Execution Architecture, not a competing, separate obligation. **Neither source is overextended here** — this finding does not go beyond what D2.5/D2.6 already established when D2 was decided; it is re-confirmed, not expanded.

#### D6.7 — Execution-Gate Analysis (Step 7)

| Source | Exact wording (re-verified) | Relationship |
|---|---|---|
| `COM-001-005` | "No commercial Business Activity shall be executed until registered in the BAR" | LOCKED, commercial-domain gate |
| `COM-001-060` | "registered in the Business Activity Registry... once implemented" | LOCKED, maturation timing |
| `IMP-001 §6.22.7` | "A Business Activity shall not be executable until successfully registered" | Active — **correctly expresses** the LOCKED gate in domain-neutral engineering language (no "commercial" qualifier — a broader phrasing than `COM-001-005`'s own commercial-domain-specific text, but not in conflict, since `PLT-001-004`/`GRC-001-008` independently impose the identical gate for their own domains, making `§6.22.7`'s domain-neutral phrasing an accurate synthesis, not an overreach) |
| `IMP-001 §6.22.15` | "shall be registered in the Business Activity Registry before becoming available for execution" | Active — restates the same gate a second time, within the "Architectural Guarantees" framing |

**Finding:** `IMP-001` **correctly expresses** the LOCKED BAR execution-gate requirement — it does not add methodology beyond what the LOCKED sources collectively already require (its domain-neutral phrasing synthesizes `COM-001-005`/`PLT-001-004`/`GRC-001-008`'s three domain-specific statements accurately, not incorrectly), and the two internal restatements (`§6.22.7`, `§6.22.15`) duplicate each other within `IMP-001` itself but do not conflict with the LOCKED text. **No wording conflict was found.** No text is modified by this finding.

#### D6.8 — D5 Identity Interaction (Step 8)

D5 decided: BAR is the canonical Business Activity Identifier authority; assignment occurs at BAR registration. Checked against `§6.22.1b` ("The Activity Identifier referenced throughout this section is governed by `SD-002-004`... This section does not define a competing identifier format") and `§6.22.6`'s own Identity attribute category (Activity Identifier, Activity Name, Activity Code, Version, Status):

**Is there a conflict?** No direct textual conflict — `§6.22.1b` addresses *format* only and explicitly declines to address authority ("does not define a competing identifier format" is a format statement, not an authority statement); `§6.22.6` lists Identity as an attribute the Registry *holds*, which is consistent with D5's own "BAR is canonical authority" finding (BAR holding the identifier is what "canonical authority" means in practice). **Is there a gap, not a conflict?** Yes — `§6.22` never states *who issues* the identifier or *when*, exactly as D5.4/D5.5 already found; D5 has now filled that gap with a specific answer (BAR, at registration) that `§6.22`'s own silence does not contradict but also does not itself state. **Does this require D6 amendment?** This is a live question this section identifies, not resolves: if `§6.22` is ever amended for other reasons (the broader scope gap, §D6.4), D5's own now-decided answer (BAR is the issuer, at registration) could be incorporated into `§6.22.1b`'s own text at that time — but D5's own decision does not, by itself, create a standalone amendment requirement, since D5 fills a silence rather than contradicting existing text.

#### D6.9 — D3 Retroactivity Interaction (Step 9)

Repository-wide search re-performed for this section, specifically inside `§6.22`, for any language assuming: only prospective registration; that existing activities already have identifiers; a migration model; or a transition requirement. **No such language exists anywhwere in `§6.22`'s fifteen subsections** — re-confirmed, consistent with D3.5's own prior finding (which searched the same document for the same absence and found none). `§6.22.10`'s own "Registry Version Management" and `§6.23.11`'s "Version Migration" concern version-to-version migration of an *already-registered* Business Activity, not the initial-registration transition of a pre-existing, never-registered one — the same distinction D3.5 already drew, re-confirmed unchanged. **No retroactive migration plan is created by this finding.**

#### D6.10 — Existing Business Activity Impact

| Option | Effect on existing certified BAs (WP-01–WP-21) | Effect on WP-22/C-024 | Effect on future BAs |
|---|---|---|---|
| Option A (no amendment) | None — `§6.22`'s own text is unaffected either way; D3's own retroactive-registration direction (already decided) is unaffected by whether `§6.22` is later amended | None — `D10` unaffected, BA-01 not registered or modified | Future BAs would be built against `§6.22`'s own text as a *target* description exceeding the enterprise BAR's actual decided scope — the same reading discipline `RTA-001`/`WP-RTA-001` already established as acceptable practice |
| Option B (amend `§6.22`) | None directly — an amendment corrects `§6.22`'s own text, it does not itself register or modify any BA | None — `D10` unaffected | Future BAs would be built against a `§6.22` that accurately states the enterprise BAR's actual decided scope, reducing (but not eliminating, since D2's own scope could later expand) the target-vs-built gap |

**No BA is registered or modified by either option, or by this section.**

#### D6.11 — C-024 Impact

- **`D10`:** unchanged — `D10` remains **DECIDED — Option A — deferred**, scoped to C-024 BA-01 only, unaffected by either D6 option.
- **`BIA-000001`, WP-22, Charter:** unaffected.
- **Implementation status:** remains NOT STARTED.
- **No `IMP-001` provision governing C-024 BA-01 specifically changes as a result of this section** — `§6.22` is a general, cross-capability specification; nothing in this section singles out C-024.

#### D6.12 — D7 Dependency (identified, not decided)

D6 and D7 are explicitly distinguished, per this section's own governing instruction: D6 concerns whether `§6.22`'s *text* needs correcting; D7 concerns where a future BA's *registration status* is *tracked* (`WPR-001` column vs. separate `BAR-INDEX.md`). **D6 does not decide D7.** A dependency exists in one direction only: if `§6.22` is amended (Option B) to reflect D2's decided scope, that amendment could also state where registration status is tracked, once D7 is separately resolved — but D6 does not need D7 resolved first to decide its own question, and D7's own eventual resolution does not require D6 to be resolved first either (they are independently decidable, though a combined future documentation pass could address both together — a sequencing observation, not a decision).

#### D6.13 — Source-Backed Decision Options

**OPTION A — No `IMP-001` amendment required. ✅ SELECTED (recorded 2026-09-20, per §0e)** BAR owns the four LOCKED-minimum responsibilities (D2's own decided scope); the remaining `§6.22` responsibilities remain `IMP-001`'s own broader methodology, read as an aspirational target rather than the enterprise BAR's own current binding scope — mirroring `RTA-001`/`WP-RTA-001`'s own already-accepted incremental-realization pattern (re-confirmed, D6.10). *Source basis:* `§6.22.1a`'s own self-limiting text; the `RTA-001`/`WP-RTA-001` precedent for treating a LOCKED-adjacent, fuller architectural design as incrementally realized without requiring the underlying text to be corrected first. *What it authorizes:* continuing to read `§6.22` as-is, with the scope gap (D6.4) understood as a known, disclosed condition. *What it does not authorize:* any claim that `§6.22`'s own text is thereby made inaccurate or invalid — Option A treats the gap as acceptable, not as an error requiring correction.

**OPTION B — Amend `IMP-001 §6.22`.** Explicitly reconcile `§6.22`'s own text with D2's decided BAR boundary, so it no longer appears to assign the eight-of-nine `§6.22.3` Engine functions, the seven-item validation checklist, the status lifecycle, version/dependency management, governance workflow, and observability to the enterprise BAR where D2 did not include them, and optionally incorporate D5's own now-decided identity-authority/timing answer into `§6.22.1b`. *Source basis:* `§19.8` Technical Debt discipline's own general principle that a disclosed, known documentation-reality gap is the class of condition that discipline exists to surface rather than leave permanently silent (cited by analogy — `§19.8` itself governs code-level Technical Debt, not constitutional-methodology-document accuracy directly, so this is `[INFERENCE]`, not a direct textual mandate to amend). *What it would need to change, without actually changing it:* `§6.22.3`'s own nine-function list would need a scope qualifier distinguishing the four D2-decided functions from the five not currently built; `§6.22.5`/`§6.22.6` would need the same distinction for registry contents/attributes; `§6.22.9`–`§6.22.13` would need to be marked as not-yet-adopted-scope; `§6.22.1b` could optionally incorporate D5's own authority/timing answer. *What it does not authorize:* this section does not draft that amendment text, and no such text is created here.

**No third, materially distinct relationship was found and none is manufactured.** A "formal three-way split of `§6.22` responsibilities between BAR, `IMP-001`, and another enterprise mechanism" (the Step 4 Option C prompt) is not supported by any source examined — no source names a third mechanism that would absorb any `§6.22` responsibility not already accounted for as either "BAR's own LOCKED-minimum scope" or "`IMP-001`'s own broader, currently-unbuilt methodology." Options A and B already exhaust the source-supported relationship space.

#### D6.14 — Exact Question for the Repository Owner

"Given that the enterprise BAR is established at only the LOCKED-minimum scope (D2), and that `IMP-001 §6.22`'s own text describes a materially larger design across eleven of its fifteen subsections that the enterprise BAR does not currently implement — should `§6.22` be amended now to reflect the adopted scope (Option A: no; Option B: yes), understanding that neither option changes what is LOCKED, what BAR actually does, or any C-024 governance artifact?"

#### D6.15 — Explicit Statement

~~**D6 remains UNDECIDED. No decision has been made to amend or leave `IMP-001 §6.22` unchanged.**~~ *(Superseded 2026-09-20 — see §0e.)* **D6 has been selected — Option A, no `IMP-001` amendment required (recorded 2026-09-20, §0e).** Decision 7 remains unselected — it is not silently resolved by D6's own selection. `IMP-001` was not modified.

---

### Decision 7 — Enterprise BAR Registration Record / Index Placement (full decision preparation, expanded 2026-09-20 following D1/D2/D3/D5/D6's selections)

**Status: D7 — DECIDED — Option B (separate BAR registration index, distinct from `WPR-001`) selected, recorded 2026-09-20, §0f above. All seven enterprise BAR decisions are now resolved.**

#### D7.1 — Decision Statement

Where should authoritative Business Activity BAR registration records live, and how should BAR relate to `WPR-001`? Specifically: does `WPR-001` remain the authoritative registration record and BAR use/extend it (Option A), or does BAR have its own canonical registration/index, separate from `WPR-001` (Option B)? This is a record-authority/placement question, not BAR mechanism design.

#### D7.2 — Why D7 Is Required

D5 already decided BAR is the canonical Business Activity Identifier authority, with assignment at BAR registration — but D5 did not decide *where* that registration record physically lives or which existing artifact, if any, hosts it. D3's own retroactive-registration direction (all 21 existing rows) makes this a practical, not merely theoretical, question: any future registration act needs a destination. Neither D1 nor D2 nor D3 nor D5 named one.

#### D7.3 — Current BA-Record Landscape (Step 2, re-inventoried directly, not assumed)

| Artifact | What BA fact it records | Authority | Identifier | Registration state | Scope | Evidence |
|---|---|---|---|---|---|---|
| `WPR-001` | WP → Capability assignment, WP status, Governing IRA, Certification | **Self-declared, explicitly WP-scoped only** (§D7.4 below) | None (no BA or identifier field) | None (no registration-state field) | One row per Work Package, not per Business Activity | `WPR-001 §1`/`§3`, re-read directly |
| `CBOR-INDEX.md` | Business **Object** registration (`OFR`/`CAC`/`BIA`/`AEO`/`CFG`-000001, six `SCI`/`POC`/`IMC`/`RVC`/`VLC`/`RSC`-000001) | Authoritative index, pointer to each registering ADR | Business Object identifiers only | Tracks registration events for Objects | Business-Object-centric | `CBOR-INDEX.md §1`, re-confirmed |
| Charter (per-WP) | Design-time BA scope, dependencies, exclusions, informal "BA-01" ordinal label | Design-time narration only, no registration authority | None | None | Per-WP, informal | Direct inspection, WP-16–22 |
| `CAP-001` (capability registry) | Capability identity/status | Capability-level only | None (no BA field) | None | One layer above WP/BA | `CAP-001`, zero BAR/BA mentions, re-confirmed |
| `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md` | A cross-referenced narrative summarizing Capability → WP → BA status, including a `CBOR \| BAR` column in its own §4 Work Package Register table | **Explicitly self-described as non-authoritative** — its own §1 states: "Not an IRA, not an ADR, not a Work Package, not a charter. Creates no capability. Modifies no architecture. Authorizes no implementation." | None assigned by this document itself | Narrates, does not register | Cross-cutting census/traceability artifact, not a registration mechanism | `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md §1`, re-read directly for this section |
| BAR (D1-established, D2-scoped, D5-identity-decided) | Would hold canonical BA identity + registration record, per D2's own decided scope | Canonical for identity (D5) | Canonical, once built | Canonical, once built | Business-Activity-centric | This document's own D1/D2/D5 |

**No location currently records an actual Business Activity registration** — this table's own "Registration state" column is empty everywhere except BAR's own future, not-yet-built row. **This document does not assume a future BAR index is required simply because BAR is conceptually separate** (per this task's own governing instruction) — that conclusion is examined, not presumed, at D7.6/D7.7 below.

#### D7.4 — `WPR-001`'s Own Declared Responsibility (Step 3, re-verified directly against its own text)

`WPR-001 §1` (Purpose), re-read verbatim for this section: *"Before this document existed, no repository artifact defined which Work Package (WP-NN) implements which PE-001 capability (C-XXX)... **This document is the single, authoritative source for Work Package → Capability assignment.** Future IRAs SHALL cite this document for WP ownership rather than inferring it. This document does not itself approve or authorize implementation of any WP it lists."*

**Finding:** `WPR-001`'s own self-declared scope is **Work Package → Capability assignment**, nothing broader. It does not claim to be a Business Activity registry, a Business Activity identity source, or a registration record of any kind — re-confirmed by its own §3 table structure (`WP | Capability | Capability Name | Status | Governing IRA | Certification`), which has no Business Activity, identifier, or BAR-registration field. `WPR-001`'s own document header additionally classifies itself explicitly: *"Type: Governance Registry (not a Constitutional Document under ARCH-000 §12 — this is an implementation-sequencing record, analogous in authority scope to an ADR, not a Layer-1 architecture specification)."*

**No authoritative source — not `WPR-001` itself, not `COM-001`/`CMD-001`/`SD-002`/`PLT-001`/`GRC-001`/`RTA-001`, not `IMP-001`, not `CLAUDE.md` — states that `WPR-001` is, or is intended to become, the canonical Business Activity registry.** This is stated explicitly, per this section's own governing instruction, rather than left implicit.

#### D7.5 — BAR's Own Responsibility (Step 4, per D2's decided LOCKED-minimum scope)

D2 already decided BAR's scope is: (1) cataloguing/registration, (2) canonical identity, (3) execution-time gate, (4) discovery-exclusivity. D5 decided BAR is the identity authority, at BAR-registration time. Together, these establish that BAR itself must be authoritative for: which Business Activities exist and are registered; each one's canonical `BA-NNNNNN` identity; whether each is currently execution-eligible; and how each is discovered at runtime (`IMP-001 §6.22.8`, `RTA-001 §6.6`). **Whether these responsibilities "naturally require" a separate authoritative registration record, as opposed to being layered onto an existing one, is not self-evident from the LOCKED text alone** — `SD-002-034`'s own cataloguing obligation states only that a BA must be catalogued "in the Business Activity Registry," which is consistent with either a `WPR-001` extension styled as "the Business Activity Registry" or a wholly separate artifact of that name; the LOCKED text does not itself mandate a particular physical location. This section does not design the storage implementation either way.

#### D7.6 — OPTION A — `WPR-001` as Authoritative Record

**Interpretation:** `WPR-001` remains the canonical record of Business Activity registration; BAR consumes/uses `WPR-001`'s own record for its four LOCKED-minimum responsibilities; no separate BAR index is created.

**Is this supported by source evidence?** Not directly — no source states `WPR-001` should, or already does, serve this role (D7.4's own finding). It is a *plausible* option only in the sense that `WPR-001` is the one document already tracking every Work Package end-to-end, and extending it is one of two structurally available paths, not because any source names it as the intended BAR host.

- **Identity:** would require `WPR-001` to gain an identifier field it does not have today — a `WPR-001` structural change (not performed here).
- **Registration:** would require `WPR-001` to gain a registration-state field it does not have today.
- **Execution gate:** unaffected by *where* the record lives — the gate itself (`COM-001-005`) is a runtime rule, not a storage-location rule.
- **Discovery:** `IMP-001 §6.22.8`/`RTA-001 §6.6` require discovery "exclusively through the Registry" — if `WPR-001` itself became "the Registry" for this purpose, discovery would need to query `WPR-001`; this is not foreclosed by any source, but also not the pattern CBOR already established (a separate index).
- **Retroactive registration of all 21 BAs (D3):** every one of the 21 rows is already `WPR-001`-registered at the WP level — extending `WPR-001` would let the retroactive exercise attach to already-existing rows, rather than creating new ones from scratch.
- **Future BAs:** would register by extending their own future `WPR-001` row.
- **Interaction with D5:** BAR (per D5) is the identifier authority regardless of where the record lives — Option A would mean BAR issues the identifier *into* a `WPR-001` field, not that `WPR-001` itself becomes the issuer.
- **Interaction with D6 (open):** if `WPR-001` becomes the record host, `§6.22`'s own text (D6's subject) would need to describe the Registry as `WPR-001`-hosted, if D6 is ever amended — a consideration for D6, not decided here.
- **Audit/traceability:** `WPR-001` already carries Certification/Governing-IRA linkage; a BA-registration field would sit alongside that existing traceability chain.
- **Risk of conflating WP identity with BA identity, explicitly flagged:** `WPR-001` is WP-centric (one row per Work Package); the investigation's own §7 inventory shows several WPs contain multiple Business Activities (e.g., WP-01's BA-01 through BA-08, WP-04's BA-01 through BA-09). A single `WPR-001` row cannot hold multiple distinct Business Activity identities/registration states without either (a) becoming a one-to-many structure foreign to `WPR-001`'s own current one-row-per-WP design, or (b) conflating a WP's own identity with its (possibly several) BAs' identities — a structural mismatch this option does not resolve.

**This option is not called better, safer, or preferred.**

#### D7.7 — OPTION B — Separate BAR Registration Index/Registry ✅ SELECTED (recorded 2026-09-20, per §0f)

**Interpretation:** BAR maintains its own authoritative Business Activity registration record, structurally separate from `WPR-001`; `WPR-001` remains authoritative for Work Package governance only; the two are linked (e.g., by cross-reference) but distinct.

**Is this supported by source evidence?** Yes, as a structural precedent — `CBOR-INDEX.md` already demonstrates exactly this pattern for Business Objects: a registry separate from `WPR-001`, Business-Object-centric rather than Work-Package-centric, explicitly declared as its own kind of artifact (`CBOR-INDEX.md §1`: "this index registers Business Objects, not Business Activities" — confirming CBOR's own self-awareness that a parallel, BA-centric index would be a distinct, not-yet-existing artifact). `ONT-001 §2`'s own finding ("the registries of instances... BAR and CBOR are two distinct registries, neither a subset of the other") independently supports BAR having its own registry, structurally parallel to but separate from CBOR — and, by the same centricity logic, separate from `WPR-001`.

- **Identity:** BAR's own index would hold the `BA-NNNNNN` identifier directly, with no `WPR-001` field needed.
- **Registration:** BAR's own index would be the registration-state record directly.
- **Execution gate:** same as Option A — unaffected by storage location; the gate is a runtime rule.
- **Discovery:** directly consistent with `IMP-001 §6.22.8`/`RTA-001 §6.6`'s own "exclusively through the Registry" language, if "the Registry" is read as BAR's own dedicated artifact (the more literal reading of that phrase, though not the only textually available one).
- **Retroactive registration of all 21 BAs (D3):** each of the 21 rows would need a *new* entry created in the separate index (cross-referencing its own `WPR-001` row, Charter, and `IMP-REPORT`), rather than extending an existing `WPR-001` row.
- **Future BAs:** would register into the separate index directly, cross-referenced from `WPR-001`.
- **Interaction with D5:** BAR (per D5) issues the identifier directly into its own index — no intermediary artifact.
- **Interaction with D6 (open):** a separate index would make `§6.22`'s own "the Registry" language more directly literal (a dedicated artifact), which could make certain `§6.22` wording *more* naturally separable from `IMP-001`'s broader methodology if D6 later selects amendment — a consideration for D6, not decided here.
- **Traceability:** would require an explicit cross-reference convention between the new index and `WPR-001` (mirroring how `CBOR-INDEX.md` entries already cross-reference their own registering ADR and, indirectly, the owning WP).
- **Duplication risk:** a WP-level status (`WPR-001`) and a BA-level status (the new index) would need to stay consistent for any WP whose own overall status depends on its BAs' individual registration states — a synchronization burden Option A does not have, since it has only one record to maintain per WP-to-BA mapping (subject to Option A's own one-to-many structural mismatch, D7.6).
- **Authority boundaries:** clean and non-overlapping — `WPR-001` for WP governance, the new index for BA registration, `CBOR-INDEX.md` for Business Object registration — three distinct, non-conflicting registers, consistent with `ONT-001 §2`'s own "neither a subset of the other" finding extended by analogy to a third register.

**This option is not called better, safer, or preferred.**

#### D7.8 — Additional Source-Supported Option

No third, materially distinct placement option was found. A hybrid ("`WPR-001` gains a lightweight status flag while a separate index holds the full registration record") is a *detail-level* combination of elements from both options, not a materially distinct third authority model — noted, not presented as a separate "Option C," consistent with this document's own established practice of not manufacturing options for completeness (§12 of the investigation, D2.7, D3.8's own identical disclipline).

#### D7.9 — Authority-Boundary Analysis (Step 4/7 synthesis)

| Boundary | Option A | Option B |
|---|---|---|
| `WPR-001`'s own declared scope (D7.4) | Would be **exceeded** — `WPR-001`'s own Purpose statement is "Work Package → Capability assignment" only; extending it to BA registration would expand that self-declared scope, a change to `WPR-001` this document is not authorized to make and does not perform | **Preserved as-is** — `WPR-001` continues doing exactly what its own Purpose statement already says |
| CBOR precedent consistency | Diverges from the CBOR pattern (CBOR is separate from `WPR-001`) | Consistent with the CBOR pattern |
| WP-vs-BA centricity | Structural mismatch for multi-BA WPs (D7.6) | No mismatch — BA-centric by design |

#### D7.10 — D5 Interaction (Step 7)

D5 already decided BAR is the canonical identifier authority, at BAR-registration time. **Under either D7 option, BAR remains the issuer** — D7 only determines *where the issued identifier is written down*, not *who issues it*. Could duplicate identifiers arise? Only if both `WPR-001` and a separate index each independently attempted to hold a BA's own identity without one being clearly the authoritative record and the other a mere reference — a risk this section flags as a reason authority boundaries (D7.9) matter, not a risk either option, correctly implemented, would necessarily create. No identifier format or schema is invented here.

#### D7.11 — D6 Interaction (Step 8, D6 remains OPEN, not decided here)

D7's outcome could make D6's own question easier or harder to answer, but does not decide it: a separate BAR registry (Option B) would make `§6.22`'s own "the Registry" language read more literally as a dedicated artifact, potentially making the scope-gap distinctions D6.4 already identified easier to state precisely in any future amendment; keeping `WPR-001` authoritative (Option A) would require any future `§6.22` amendment to explain that "the Registry" refers to a `WPR-001` extension rather than a dedicated artifact — a slightly less direct mapping to `§6.22`'s own existing phrasing. **Neither observation decides D6**, which remains a separate, open question about `§6.22`'s own text, not about where records are physically kept.

#### D7.12 — D3 Retroactive-Population Consequence (Step 9, no registration performed)

| | Option A | Option B |
|---|---|---|
| What the future registration exercise would have to record, per row | An identifier + registration-state field added to each of the 21 rows' own existing `WPR-001` entries (subject to the multi-BA structural question, D7.6, for WPs with more than one BA) | A new entry per Business Activity (not per WP) in the separate index, cross-referencing the existing `WPR-001` row, Charter, and `IMP-REPORT` |
| Rows requiring more than one entry (multi-BA WPs, e.g. WP-01 BA-01–08, WP-04 BA-01–09) | Ambiguous under Option A's own one-row-per-WP structure (D7.6) | Naturally one entry per BA (Option B's own BA-centric design) |

**No registration, identifier assignment, or migration record is created by this table.**

#### D7.13 — Existing Business Activity Impact

No existing BA (any of the 21 rows) is registered, modified, or assigned an identifier by this section, under either option. The consequence tables above (D7.6/D7.7/D7.12) describe what a *future* registration exercise would need to do, not an act performed now.

#### D7.14 — C-024 Impact

- **`D10`:** unchanged — remains **DECIDED — Option A — deferred**, scoped to C-024 BA-01 only.
- **`BIA-000001`, WP-22, Charter:** unaffected under either option.
- **Implementation status:** remains NOT STARTED.
- **BA-01 is not automatically registered** by this section under either option — it would, like every other row, require the future registration exercise (not performed here) once D6/D7 and any remaining engineering decisions are resolved.

#### D7.15 — Decision Dependency (Step 11)

**Can D7 be decided independently of D6?** Largely yes — D7 concerns *where* records are authoritative; D6 concerns whether `§6.22`'s *text* needs correcting. Neither requires the other to be resolved first, though (per D7.11) D7's own outcome could make D6's eventual amendment (if selected) easier or harder to phrase precisely. **What D7 resolves:** the record-authority/placement question alone. **What D7 does not resolve:** D6 (text amendment), any BAR technical/storage design, or the retroactive-registration exercise's own sequencing (already flagged as open, non-manufactured future work, at D3.10/D5.10).

#### D7.16 — Exact Question for the Repository Owner

"Given that `WPR-001`'s own Purpose statement scopes it explicitly to Work Package → Capability assignment (not Business Activity registration), and that `CBOR-INDEX.md` already demonstrates a working separate-register pattern for Business Objects — should the enterprise BAR's own registration records be recorded as an extension to `WPR-001` (Option A), or as BAR's own separate registration index, structurally parallel to but distinct from `CBOR-INDEX.md` (Option B)?"

#### D7.17 — Evidence Matrix

| Assertion | Source | Evidence type |
|---|---|---|
| `WPR-001`'s own scope is WP → Capability assignment only, not BA registration | `WPR-001 §1`, re-read verbatim | `[FACT]` |
| `WPR-001` is a Governance Registry, not a Constitutional Document | `WPR-001` document header | `[FACT]` |
| `WPR-001 §3`'s table structure has no BA/identifier/registration field | Direct structural inspection | `[FACT]` |
| `CBOR-INDEX.md` is a working precedent for a register separate from `WPR-001` | `CBOR-INDEX.md §1` | `[FACT]` + `[PRECEDENT]` |
| BAR and CBOR are two distinct registries, neither a subset of the other | `ONT-001 §2` | `[LOCKED]`, verbatim |
| No source states `WPR-001` is, or should become, the canonical Business Activity registry | Repository-wide review, this section | `[FACT]` (absence) |
| `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md` is explicitly non-authoritative | Its own §1 | `[FACT]` |
| Several WPs contain more than one Business Activity | Investigation §7 inventory, re-confirmed (WP-01, WP-04, etc.) | `[FACT]` |

#### D7.18 — Explicit Statement

~~**D7 remains UNDECIDED. No registration-record placement option has been selected.**~~ *(Superseded 2026-09-20 — see §0f.)* **D7 has been selected — Option B, a separate BAR registration index distinct from `WPR-001` (recorded 2026-09-20, §0f). All seven enterprise BAR decisions are now resolved.** No `BAR-INDEX.md` was created, no registry was built, and no Business Activity or identifier was registered/assigned by this recording.

---

## 8. IMP-001 vs. BAR — Explicit Boundary (re-verified directly against source text for this document)

**A. Business Activity design-time methodology (`IMP-001`, already exists, already governs current practice):**
- `§6.7` **Business Activity Contract (BAC)** — re-read in full: Activity Identifier, Business Domain, Business Object, Activity Type, Business Intent, Input/Output Contract, Preconditions, Postconditions, Authorization, Events, Workflow, Audit, AI Assistance, Definition of Done, Idempotency. Verbatim: "The BAC is the authoritative specification for implementation."
- `§6.14` **Canonical Business Activity Manifest (CBAM)** — re-read in full: Business Domain, Business Object, Activity Name, Activity Type, Business Intent, Input/Output Contract, Business Rules, Authorization Requirements, Workflow Integration, Events, Metadata Dependencies, AI Assistance, Test Requirements, Version. A machine-readable counterpart to the BAC, overlapping but not identical in attribute set.
- Both are **design-time** artifacts describing one Business Activity. Every Charter examined (WP-16 through WP-22) narrates BAC-equivalent content in prose without a discrete, named artifact of either kind; no physical CBAM file exists anywhere in this repository.

**B. BAR (`IMP-001 §6.22`, does not exist, LOCKED obligation to exist unsatisfied):**
- Canonical identity assignment (`§6.22.6`, tied to `SD-002-004`).
- Runtime, queryable, centrally-owned metadata store (full attribute set, `§6.22.6`).
- Registration validation (`§6.22.7`, verbatim: "A Business Activity shall not be executable until successfully registered").
- **Exclusive discovery mechanism** (`§6.22.8`, verbatim: "The Business Activity Engine shall discover Business Activities exclusively through the Registry").
- Lifecycle-status model, version management, dependency management, governance workflow, observability (`§6.22.9`–`§6.22.13`).
- A live, cross-Activity runtime infrastructure component of the Business Activity Runtime (`RTA-001 §3.6`/`§6`), distinct from and layered atop the design-time BAC/CBAM.

**What remains outside `IMP-001` entirely:** the runtime enforcement layer — execution-time gating, exclusive discovery, and centrally-mediated authorization/audit/monitoring. `IMP-001 §6.7`/`§6.14` govern *what a Business Activity is documented as*; they cannot, by themselves, discharge an *execution-time gate*, because a design-time document sitting in a repository is not a runtime mechanism. This is the same finding the investigation reached in its own §8, independently re-confirmed here against the primary text rather than accepted on the investigation's own say-so.

**The minimum-scope ambiguity is preserved, not resolved, here:** whether the LOCKED minimum (catalogue + execution gate) requires building the *entire* `§6.22` design or could be satisfied by something materially smaller is not answered by any source this document examined either. This document does not fill that gap with a software-architecture preference — it is Decision 2, left to the Repository Owner.

---

## 9. Relationship Among Existing Registries (WPR-001 / CBOR / BAR / Identifier Namespace / Charter / Capability Registry)

| Register/artifact | What it currently governs | Authoritative for | Overlaps with | Source |
|---|---|---|---|---|
| `CAP-001` | Capability identity and status (43 capabilities) | Capability-level existence/status only | Nothing else in this table — operates one layer above WP/BA | `CAP-001_Enterprise_Capability_Registry.md`; confirmed zero BAR mentions |
| `WPR-001` | Work Package identity, status, governing IRA, certification | WP-level lifecycle tracking | Partially overlaps with a future BAR only if Decision 7 selects a `WPR-001` column | `WPR-001 §3` table header, re-confirmed no BAR/BA-Identifier field |
| `CBOR-INDEX.md` | Business Object registration (`CMD-001 §26`) | Sole authoritative index for registered Business Objects | None with BAR — `ONT-001 §2`/`ONT-001-051` both confirm BAR and CBOR are "two distinct registries, neither a subset of the other" | `CBOR-INDEX.md §1`; `ONT-001 §2` |
| Charter (per-WP) | Design-time narration of BA scope, dependencies, exclusions | Governing document for what a specific BA is chartered to do | Overlaps in *content* with BAC/CBAM (`IMP-001 §6.7`/`§6.14`), which Charters currently satisfy in prose without a discrete artifact | Direct inspection of WP-16 through WP-22 Charters |
| Business Activity Identifier namespace (`BA-NNNNNN`) | Does not currently exist | N/A — zero assignments repository-wide | Would be BAR's own responsibility if established (`SD-002-004`, `IMP-001 §6.22.1b`) | `[FACT]`, repository-wide search |
| BAR (`IMP-001 §6.22`) | Does not currently exist | Would be the authoritative runtime registry for Business Activities, if built | Distinct from CBOR by design (`ONT-001 §2`); distinct from Charter/BAC/CBAM (design-time vs. runtime, §8 above); relationship to `WPR-001` is Decision 7, unresolved | `IMP-001 §6.22`; `RTA-001 §3.6`/`§6` |

**Duplication assessment:** No duplication currently exists, because BAR does not exist to duplicate anything. If established, the only genuine duplication risk the sources support is between a `WPR-001` BAR column and a dedicated `BAR-INDEX.md` (Decision 7) — not between BAR and CBOR (structurally distinct by design, per `ONT-001`) or between BAR and Charter/BAC/CBAM (design-time vs. runtime, per §8 above).

**Source of truth vs. derived registry:** No source states whether a future BAR would be the *source of truth* for Business Activity identity (mirroring CBOR's role for Business Objects, where the registering ADR is authoritative and `CBOR-INDEX.md` is "a pointer to it," per `CBOR-INDEX.md §1`) or a *derived* index summarizing decisions made elsewhere. This is not resolved by any source and is not resolved here — it is folded into Decision 7's own unresolved scope, not manufactured as an eighth decision, since `§14` names seven and no additional dependency makes an eighth unavoidable.

---

## 10. Existing Business Activity Impact

Re-derived from the investigation's own §7 inventory, independently spot-checked against `AUREX_ENTERPRISE_FEATURE_CAPABILITY_COVERAGE_MATRIX.md §4`'s per-WP BAR column for this document (corroborating, not contradicting, the inventory):

- **Previously implemented/certified BAs (WP-01 through WP-19, minus WP-13 in progress):** nineteen Work Packages never raised the BAR question. Under Option A + Decision 3 = retroactive, these would face a backfill question the Repository Owner has not yet been asked. Under Option A + Decision 3 = prospective-only, or under Option B in any form, none of these WPs' own `CLOSED — CERTIFIED` status changes.
- **Chartered and implemented but only recently closed (WP-20/C-021, WP-21/C-022):** each already explicitly raised and deferred its own BAR question (`ADR-037`, `ROD-C022-B D10`). Neither deferral is reopened by this document. Whether an eventual enterprise BAR mechanism would supersede or require re-confirmation of either capability-scoped deferral is not decided here — it would depend on Decision 3/4's own resolution, applied at that future time.
- **Chartered, CBOR-registered, not yet implemented (WP-22/C-024 BA-01):** `D10` deferral stands, unaffected (§11 below).
- **In-progress (WP-13):** not a chartered Business Activity in its own right (cross-cutting runtime work); not part of the BA inventory this document's analysis addresses.

**Migration/retrofit consequence, documented not solved:** if Option A is selected with Decision 3 = retroactive, an identifier-backfill and registration exercise across 20+ Business Activities would follow, scale dependent on Decision 2's scope choice. This document states this as a factual consequence per the governing instruction ("If the enterprise decision would create a migration/retrofit issue for existing BAs, document it as a consequence rather than solving it") and does not propose how such an exercise would be sequenced, resourced, or governed.

---

## 11. C-024 Impact

- **Does this document change `C-024 D10`?** No. `D10` (`ROD-C024-BAR_Treatment_Decision_Preparation.md §0`, Option A, recorded 2026-09-19) is restated in §2 above verbatim in substance and is not edited, struck through, or superseded by any part of this document.
- **Does it affect WP-22?** No — WP-22's own registration in `WPR-001`, Charter scope (§5–§22 of the Charter), and implementation status (NOT STARTED) are unchanged.
- **Does it affect CBOR `BIA-000001`?** No — `ADR-041`'s registration is a Business Object registration, structurally independent of BAR (§9 above), and is not touched by this document.
- **Does it affect the Charter?** No — the Charter's own §24/§27 already name BAR as an outstanding prerequisite without deciding it; this document does not alter that framing.
- **Does it affect implementation readiness?** No new blocker is created. `D10` already establishes that BAR treatment does not block C-024 BA-01's implementation from proceeding (once CBOR and the Charter's other prerequisites are separately satisfied) — this document's own preparation of the *enterprise* question does not change that capability-scoped conclusion, consistent with `D10 §0`'s own text: "this decision does not require any fresh RO decision specifically for C-024... any future decision C-024 requires is the same one every other deferred capability requires: the enterprise-level Option A/B choice."

**No LOCKED conflict was found that would require reopening `D10`.** `COM-001-005`'s BAR clause gates **execution**, not implementation or Charter/decision-recording; C-024 BA-01 has not been implemented and has not been executed. This is the same conflict-check the investigation's own §11 performed and this document does not depart from it.

---

## 12. Governance Consequences

- **No hard blocker exists.** Per §6 above (Option B row) and the unbroken three-capability precedent, deferring the enterprise decision does not, by itself, block any Work Package's implementation, certification, or closure — this pattern has held for all 22 Work Packages to date, and no source examined states otherwise.
- **The LOCKED obligation remains outstanding either way.** Selecting neither option (i.e., taking no action) is not itself a resolution — `COM-001-005`/`-060` and their `PLT-001`/`GRC-001` counterparts remain unsatisfied constitutional text regardless of how long a decision is deferred. This document does not treat "no decision yet" as equivalent to "Option B selected" — those are different states, and only the Repository Owner's own explicit instruction converts the former into the latter (exactly as occurred for `D10` itself, which existed as "UNDECIDED" before the Repository Owner's own instruction converted it to "DECIDED — Option A," per `ROD-C024-BAR`'s own §0/§10 structure).
- **Census synchronization:** `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md`'s own C-024 narrative (row 42, and its D-002 section narrative) was found stale — still stating "no Charter, WP, or Business Activity selection has occurred," which predates WP-22's chartering, `BIA-000001` CBOR registration, and D9/D10. This document corrects only that specific staleness, using the same preserve-and-correct convention already established in that same document for C-021/C-022/C-023 (struck-through historical text preserved, corrected text appended, no other capability row touched), and adds the same document's now-appropriate note that the enterprise BAR question is under Repository Owner decision preparation (this document), not resolved. `AUREX_ENTERPRISE_FEATURE_CAPABILITY_COVERAGE_MATRIX.md` was left untouched — it has no WP-22 row at all yet, and creating one would exceed "updating an existing place for BAR status" (it would require composing a new capability row from scratch, which is a larger act than this document's own change-boundary authorizes).

---

## 13. Explicit Non-Decisions / Boundaries

This document does NOT:
- select Option A or Option B for the primary enterprise decision, or for any of the six subordinate decisions;
- rank, score, or characterize any option as better, safer, preferred, or recommended;
- design a BAR mechanism (schema, API, runtime class, service topology, storage, or workflow);
- assign a Business Activity Identifier;
- register any Business Activity;
- modify `COM-001`, `CMD-001`, `IMP-001`, `SD-002`, `PLT-001`, `GRC-001`, `CLAUDE.md`, `WPR-001`, or `CBOR-INDEX.md`;
- modify any C-024 ROD, IRA, TDS, Charter, D9, D10, CBOR eligibility artifact, or `ADR-041`;
- create an ADR (no genuine architectural conflict requiring one was found — §11's conflict-check found none);
- resolve whether the nineteen-Work-Package "undiscovered, not satisfied or exempted" pattern (investigation §7/§15) itself requires remediation;
- resolve whether "execution" (`COM-001-005`'s trigger) has a meaning distinct from "implemented and certified" for any commercial-domain construct;
- resolve Finding 3 from the prior independent review of the investigation (missing census cross-references) beyond the narrow, convention-following correction described in §12 above, which was performed because this task's own CENSUS section explicitly called for it — not as a general remediation of that finding.

---

## 14. Exact Questions for the Repository Owner (consolidated)

1. Does AUREX establish a canonical enterprise BAR mechanism now, or formally defer it to a future enterprise governance initiative?
2. If established: minimal LOCKED-compliant catalogue, or the full `IMP-001 §6.22` Business Activity Engine design?
3. If established: does registration apply retroactively to already-certified Business Activities, or only prospectively?
4. If deferred: does the deferral apply enterprise-wide, or only case-by-case as each capability raises it?
5. If established: who assigns `BA-NNNNNN` identifiers, and at what governance point?
6. If established at less than full `§6.22` scope: is `IMP-001 §6.22` amended now, or left as an unamended future-target design?
7. If established: does `WPR-001` gain a BAR column, or does BAR remain a separate index mirroring `CBOR-INDEX.md`?

---

## 15. Evidence Matrix

| Assertion | Source | File/Section | Evidence type |
|---|---|---|---|
| BAR obligation is universal, LOCKED, and unsatisfied | `SD-002-034`; `COM-001-005`/`-060`; `PLT-001-004`/`-030`; `GRC-001-008`/`-070`; `OPM-001-013` | Respective files, re-verified verbatim for this document | `[LOCKED]` |
| No BAR mechanism exists anywhere | Repository-wide search, code comments | `AIService/schemas/conversation.py:37`; `AuthorizationEngine/models.py:51` | `[FACT]` |
| `IMP-001 §6.22.7`/`§6.22.8` verbatim | Direct re-read | `IMP-001_Implementation_Playbook.md:5161-5162, 5184-5187` | `[ACTIVE]`, verbatim |
| BAC/CBAM (`§6.7`/`§6.14`) are design-time, not runtime | Direct re-read | `IMP-001_Implementation_Playbook.md:2105-2150, 2283-2317` | `[ACTIVE]`, verbatim |
| CBOR identifier-timing precedent (assigned only at registering act) | Direct re-read | `ADR-039 §Decision item 1`; `ADR-040 §Decision item 1`; `ADR-041 §Decision item 1` | `[PRECEDENT]`, non-binding by cross-domain default, cited for governance-pattern comparison only |
| Three capability-scoped BAR deferrals, each self-limiting | Direct re-read | `ADR-037 §Decision item 5`; `ROD-C022-B D10`; `ROD-C024-BAR §0` | `[PRECEDENT]`, not enterprise policy |
| `WPR-001`/`CBOR-INDEX.md` structural separation, no BAR field in either | Direct re-read | `WPR-001 §3` header; `CBOR-INDEX.md §1` | `[FACT]` |
| BAR/CBOR are two distinct registries | Direct re-read | `ONT-001 §2` (line 29); `ONT-001-051` | `[LOCKED]`, verbatim |
| C-024 D10 unaffected by this document | Direct re-read, conflict re-checked | `ROD-C024-BAR_Treatment_Decision_Preparation.md §0` | `[FACT]` + `[INFERENCE]` (conflict-check), disclosed |
| Census staleness (C-024 narrative) | Direct re-read | `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md` row 42, line 183 | `[FACT]` |

---

## 16. Self-Review

- **No BAR mechanism, registry, or identifier was created by this document.** Confirmed — this document only reorganizes and cross-references existing evidence. **Confirmed.**
- **No Business Activity was registered.** Confirmed.
- **`C-024 D10` was not reopened, altered, or reinterpreted** — §11 restates it verbatim in substance and only re-runs the same conflict-check the investigation already performed, finding no conflict, consistent with the investigation's own finding. **Confirmed.**
- **`COM-001`, `CMD-001`, `IMP-001`, `SD-002`, `PLT-001`, `GRC-001`, `CLAUDE.md`, `WPR-001`, `CBOR-INDEX.md`, and every C-024 ROD/IRA/TDS/Charter/D9/D10/CBOR-eligibility artifact/`ADR-041` were read, not modified.** Confirmed.
- **No option was selected anywhere in §6 or §7** — every option is presented with symmetric structure (source basis / what it authorizes / what it does not / consequences) and no evaluative adjective ("better," "safer," "preferred," "recommended," "correct") appears attached to any option. **Confirmed.**
- **Where only one option was genuinely source-supported (Decision 5), this was stated as a fact about the evidentiary record, not converted into an endorsement.** Confirmed.
- **All seven `§14` decisions are represented, in the same substance as the investigation's own text, with no reduction to "build vs. defer" only.** Confirmed — six subordinate decisions (§7) are each given their own full treatment, not folded into the primary decision.
- **Decision dependencies were identified, not chosen for the Repository Owner** — §5's dependency table states logical necessity (e.g., "a scope question presupposes something is being built"), not a sequencing preference. Confirmed.
- **The `IMP-001`/BAR distinction is explicit and source-verified**, not asserted from the investigation's own summary — §8 re-quotes `§6.7`/`§6.14`/`§6.22.7`/`§6.22.8` directly from the primary text. Confirmed.
- **`WPR-001`/CBOR/BAR relationships are source-backed**, not invented — §9's table cites a specific file/section for every cell. Confirmed.
- **Existing Business Activity impact is included** (§10), independently cross-checked against a second census artifact beyond the investigation's own citations. Confirmed.
- **Only two files were touched: this new artifact, and a narrowly-scoped, convention-following correction to `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md`'s own C-024 cells**, explicitly authorized by this task's own CENSUS instruction and change boundary. No other file was modified. Confirmed.

---

## 17. Explicit Statement

~~**No Repository Owner option has been selected in this artifact.**~~ ~~*(Superseded 2026-09-19 — see §0.)* **Decision 1 has been selected...**~~ ~~*(Superseded 2026-09-20 — see §0b.)* **Decisions 1 and 2 have been selected...**~~ ~~*(Superseded 2026-09-20 — see §0c.)* **Decisions 1, 2, and 3 have been selected...**~~ ~~*(Superseded 2026-09-20 — see §0d.)* **Decisions 1, 2, 3, and 5 have been selected...**~~ ~~*(Superseded 2026-09-20 — see §0e.)* **Decisions 1, 2, 3, 5, and 6 have been selected...** No option has been selected for Decision 7...~~ *(Superseded 2026-09-20 — see §0f.)* **All seven Repository Owner enterprise BAR decisions have now been selected** — Decision 1: Option A, Establish (recorded 2026-09-19, §0); Decision 2: Option A, LOCKED minimum scope (recorded 2026-09-20, §0b); Decision 3: Option A, retroactive registration for all 21 existing Business Activity rows (recorded 2026-09-20, §0c); Decision 5: Authority — Option A, BAR is canonical authority; Timing — at BAR registration (recorded 2026-09-20, §0d); Decision 6: Option A, no `IMP-001 §6.22` amendment required (recorded 2026-09-20, §0e); Decision 7: Option B, a separate BAR registration index distinct from `WPR-001` (recorded 2026-09-20, §0f). Decision 4 is moot (contingent on Option B, which was not selected for Decision 1). **No BAR mechanism design, Business Activity registration, or identifier assignment has occurred — the next governed stage (consolidated BAR mechanism design/implementation preparation) requires separate Repository Owner authorization, not begun here.**

*End of ROD-ENTERPRISE-BAR-Decision-Preparation. All seven enterprise BAR decisions DECIDED: Decision 1 — Option A — Establish (§0, 2026-09-19). Decision 2 — Option A — LOCKED minimum scope (§0b, 2026-09-20). Decision 3 — Option A — retroactive registration, all 21 rows (§0c, 2026-09-20). Decision 5 — Authority: Option A (BAR canonical); Timing: at BAR registration (§0d, 2026-09-20). Decision 6 — Option A — no `IMP-001` amendment required (§0e, 2026-09-20). Decision 7 — Option B — separate BAR registration index, distinct from `WPR-001` (§0f, 2026-09-20). Decision 4: MOOT. No BAR mechanism was created or designed. No `BAR-INDEX.md` or other registry artifact was created. No Business Activity Identifier was assigned or reserved. No Business Activity was registered. No migration or retrofit was performed. No source document (`COM-001`, `CMD-001`, `IMP-001`, `SD-002`, `PLT-001`, `GRC-001`, `RTA-001`, `CLAUDE.md`, `WPR-001`, `CBOR-INDEX.md`) was modified. `C-024 D10` unchanged, scoped only to C-024 BA-01, not converted into an enterprise BAR policy; BA-01 is not automatically registered by any of D3, D5, D6, or D7. Every C-024 governance artifact was read, not modified. No ADR created. The next governed stage — consolidated BAR mechanism design/implementation preparation — is not begun and requires separate Repository Owner authorization. Nothing staged, committed, or pushed.*
