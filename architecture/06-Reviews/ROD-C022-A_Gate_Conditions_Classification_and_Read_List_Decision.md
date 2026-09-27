# ROD-C022-A — Resolution of Independent Gate Conditions [C-1] Classification and [C-2] Read/List

**Document type:** Repository Owner Decision record — a follow-up decision, resolving two blocking (`[STOP]`) conditions raised by an independent pre-implementation review. Same class as `ROD-C022-Customer-and-Account-Management-Capability-Boundary-and-Minimum-Scope.md`, of which this is an explicit amendment/addendum, not a replacement — mirroring the established `-A`-suffix corrective-pass naming convention (`TDS-C023-A`).

**Capability:** C-022 Customer & Account Management (`CAP-001` line 76 — Active, Domain D-002 Commercial & Subscription, owning specification `COM-001` — LOCKED under EARB Constitutional Recertification CR-3.0).

**Recorded:** 2026-09-15, per direct Repository Owner instruction ("AUREX — C-022 BA-01 — RESOLVE INDEPENDENT GATE CONDITIONS"), following the independent review `architecture/06-Reviews/IRA-TDS-C022_Independent_Review.md` (Gate decision: **PASS WITH CONDITIONS**), which found two blocking conditions — `[C-1]` Classification and `[C-2]` Read/List — each requiring a fresh, explicit Repository Owner decision before any Charter, WP registration, or implementation may proceed on the affected item.

**Independent review identified:** `architecture/06-Reviews/IRA-TDS-C022_Independent_Review.md`, §6 (`[C-1]`) and §7 (`[C-2]`), §9 (Mandatory Conditions). The review was performed by a reviewer with no involvement in drafting `ROD-C022`, `IRA-C022`, or `TDS-C022`, per this repository's own no-self-certification discipline. Its findings are treated here as the authoritative evidentiary basis for these two decisions — not re-derived independently by this document, and not second-guessed.

**Classification key:** `[FACT]` — repository fact, as independently verified by the cited review. `[RO DECISION]` — a Repository Owner decision, now made. `[CARRIED FORWARD]` — a review finding restated here for completeness, not resolved by this document.

---

## A. Relationship to `ROD-C022` D1–D6

`[FACT]` `ROD-C022`'s own D1–D6 (First Delivery Slice; Scope Model; Service Hosting; Identity/Person References; BA Boundary; Next Governance Step) are **unchanged and not reopened by this document.** This document resolves exactly two conditions the independent review raised against `ROD-C022 §H`'s own boundary text and `TDS-C022`'s realization of it — it does not revisit D1, D2, D3, D4, or D6, and it narrows (does not expand) the scope description in D5/§H.

---

## B. RO Decision 1 — Commercial Account Classification (`[C-1]`)

### B.1 Evidence presented (verbatim, from the independent review)

`[FACT]` `COM-001-033` (LOCKED), complete text: *"identity, Account-to-Account hierarchy position, and status."* **No classification attribute.**

`[FACT]` `PE-001-C022` (Active, v1.2) affirmatively attaches classification to the **Account** context in four places, independently re-derived by the review, not previously caught by `ROD-C022`/`IRA-C022`/`TDS-C022`:
1. `EX-C022-04` Trigger: *"An existing Authoritative Customer Context's **or Authoritative Account Context's classification** no longer reflects the enterprise's understanding of the relationship."*
2. `C022-O02`: *"Every change to **a Customer's or Account's classification**..."*
3. `§1.4 Scope`: *"...reclassifying... the Authoritative Customer Context **and the Authoritative Account Context**..."*
4. Guiding Architectural Question: *"...including that representation's **classification**, hierarchy, and lineage through establishment, **reclassification**..."*

`[FACT]` This is a genuine conflict between a **LOCKED constitutional document** (`COM-001-033`, silent) and an **Active Enterprise Experience Specification** (`PE-001-C022`, affirmative in four places) — a `CLAUDE.md §16` canonical-authority conflict, not a `ROD-C022` drafting imprecision as originally characterized by `TDS-C022 §4`.

### B.2 `[RO DECISION — D7]`

**Option A: BA-01 does NOT include Commercial Account classification.**

`ROD-C022 §H`'s original wording ("identity/classification/status") is treated as imprecise for BA-01's own purposes. The authoritative Account model for BA-01 remains `COM-001-033` exactly as written — identity, hierarchy position (declared, not exercised — unchanged from `TDS-C022 §10`), and status. No `classification` column is authorized for BA-01.

**The `COM-001-033` ↔ `PE-001-C022` conflict itself is NOT resolved by this decision.** It is logged as a **separate, later architecture-governance correction item** — outside the scope of the C-022 BA-01 decision sequence — requiring its own future Repository Owner / EARB review under `CLAUDE.md §16`'s own procedure (identify the conflicting definitions; identify the declared canonical owner; review applicable ADRs; report before changing anything). **This decision does not itself perform that §16 procedure, and does not determine which document is "correct."** It only determines that BA-01, as a minimum first slice, does not need the answer to proceed.

**Consequence for `TDS-C022`:** `TDS-C022 §4`/§6.1's own exclusion of the `classification` column is **confirmed correct in outcome**, though its own characterization of the conflict (as ROD imprecision against COM-001 silence, rather than a genuine LOCKED-vs-Active conflict) should be corrected in a future `TDS-C022` revision pass, per the independent review's `[C-4]` citation-accuracy condition — **not performed by this document** (§D below).

---

## C. RO Decision 2 — Read/List / Reference Distribution (`[C-2]`)

### C.1 Evidence presented (verbatim, from the independent review)

`[FACT]` `ROD-C022 §H`, in-scope list, names only: *"Establish one Authoritative Commercial Account... A system-assigned, stable Account Reference... Minimum canonical Account identity... and status... Platform-global scope... `AuthService` hosting... the existing `require_platform_admin`-shaped authorization pattern."* Neither "list," "read," nor "retrieve" appears anywhere in §H. §H closes: *"This scope SHALL NOT be expanded except by an explicit, separately-recorded Repository Owner decision."*

`[FACT]` `COM-001-036`: *"The stable Customer Reference, Commercial Account Reference,... are made available for consumption by Subscription (C-020)..."* `[FACT]` `C022-O05`: *"Downstream capabilities... **always receive** a stable Customer/Account Reference."* A write-only endpoint makes the reference available exactly once, in the establish response body — nothing can retrieve it afterward.

`[FACT]` The C-022 investigation sequence was originally motivated by C-020's own inability to proceed without a genuine Customer/Account reference (`ROD-C022 §A`; the prior C-020 investigation). An establish-only BA-01 does not, by itself, make that reference consumable by a future C-020.

`[FACT]` `CLAUDE.md §20.3`/`§20.4`/`§20.6` presuppose read/demonstrability for any Business Activity a Work Package charters, unless the Work Package (or the specific Business Activity) is explicitly, separately chartered as backend-only, per `§19.4`'s own STOP-and-report discipline.

### C.2 `[RO DECISION — D8]`

**Option A: Keep BA-01 strictly establish-only.**

No read/list capability is authorized by this decision. `ROD-C022 §H`'s original "establish only" boundary is confirmed and **not expanded**.

**Accepted consequences, explicitly recorded, not silently absorbed:**
- Reference retrieval and `COM-001-036` distribution are **deferred to a later C-022 Business Activity**, not solved by BA-01.
- **C-020 remains blocked** from consuming a genuine, retrievable Commercial Account reference until that later Business Activity exists. This decision does not change the sequencing finding from the earlier C-020/C-022 investigations — it only confirms that BA-01 alone does not fully discharge it.
- **Any future Charter for C-022 BA-01 MUST include an explicit `CLAUDE.md §20.3` backend-only determination**, reported and justified per `§19.4`'s STOP-and-report discipline, not silently assumed. Without that explicit determination, a Work Package built on an establish-only BA-01 cannot satisfy `§20.3`/`§20.4`/`§20.6`'s demonstrability and content-disclosure-state requirements, per the independent review's own finding (§7.2 item 3).

---

## D. What Remains Unauthorized / Unresolved (explicitly not closed by this document)

**Not authorized by this decision record:**
- A Charter, WP registration, schema, migration, or implementation of any kind.
- The `CLAUDE.md §16` architecture-governance conflict-resolution procedure for `COM-001-033` ↔ `PE-001-C022` (§B.2) — logged as a separate future item, not performed here.
- A `TDS-C022` revision correcting the review's carried-forward conditions:
  - **`[C-3]`** — `TDS-C022 §7`'s reference-format reasoning (declining `COM-001-001`'s `PREFIX-NNNNNN` format) was found factually defective by the independent review and requires a TDS correction — narrows scope, requires no new RO decision, but is **not performed by this document**.
  - **`[C-4]`** — citation misattributions in `ROD-C022`/`IRA-C022`/`TDS-C022` (`PE-001-C022` wording tagged as LOCKED `COM-001` text) require correction — **not performed by this document**.
  - **`[C-5]`** — `TDS-C022`'s single-call establish design does not disclose its relationship to `COM-001-002`/`COM-001-003`'s Anchor/Intent/Proposed/Assessment lifecycle pattern, nor the `ERB-C022-01`-vs-`ERB-C022-06` mapping correction — requires disclosure and an RO-level scope determination on whether a single-step establish is an accepted minimum-slice deferral — **not performed by this document**.
- **`[C-6]`** CBOR registration (Commercial Account is eligible per `CMD-001 §26.3a`, independently confirmed; no ADR yet exists) — a mandatory pre-implementation-authorization prerequisite, **not performed by this document.**
- **`[C-7]`** BAR (`COM-001-060`; no BAR mechanism exists repository-wide) — requires its own explicit Repository Owner decision, the same class every prior BA-01 required, **not performed by this document.**

**This document resolves exactly `[C-1]` and `[C-2]`, and nothing else.** No Charter or WP registration may proceed until `[C-3]`–`[C-7]` are also addressed, per the independent review's own §9/§10.

---

*End of ROD-C022-A. D1–D6 (original `ROD-C022`) unchanged. D7 (Classification, Option A) and D8 (Read/List, Option A) recorded above. `[C-3]`–`[C-7]` remain open. No Charter, WP registration, schema, migration, API, frontend, ADR, CBOR registration, BAR registration, commit, or push is authorized by this document.*
