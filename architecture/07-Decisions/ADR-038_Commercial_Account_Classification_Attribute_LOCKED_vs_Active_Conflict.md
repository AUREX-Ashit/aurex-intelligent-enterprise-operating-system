# ADR-038 — Commercial Account Classification Attribute: `COM-001-033` (LOCKED) vs. `PE-001-C022` (Active) Conflict

**Status:** ~~PROPOSED — AWAITING REPOSITORY OWNER DECISION. **This ADR does not resolve the conflict it documents.** No option below is selected, endorsed, or defaulted to by this document.~~ *(Superseded 2026-09-15 — see §0. The Repository Owner has decided.)* **Accepted — Option A selected** (Commercial Account does NOT carry a classification attribute). Decided 2026-09-15, per direct Repository Owner instruction ("AUREX — ADR-038 — REPOSITORY OWNER DECISION"). Full decision record: §0.

**Classification:** Architecture Governance / Canonical-Authority Conflict (`CLAUDE.md §16`).

**Raised by:** the independent pre-implementation review of C-022's governance gate (`architecture/06-Reviews/IRA-TDS-C022_Independent_Review.md §6`), which found that `TDS-C022 §4`'s own characterization of this conflict — as `ROD-C022 §H` wording imprecision, clarified by LOCKED `COM-001-033`'s silence — was materially incomplete, because `PE-001-C022` (Active) affirmatively attaches classification to Commercial Account in multiple places `TDS-C022`'s original determination had not located. `ROD-C022-A_Gate_Conditions_Classification_and_Read_List_Decision.md §B` recorded an interim Repository Owner decision (D7, Option A — no classification field in BA-01) **while explicitly logging the underlying `COM-001-033` ↔ `PE-001-C022` conflict as a separate, later architecture-governance correction item** — this ADR is that separate item.

**Affected Documents:** None amended by this ADR. `COM-001`, `PE-001-C022`, `ROD-C022`, `ROD-C022-A`, `IRA-C022`, `TDS-C022`, and `IRA-TDS-C022_Independent_Review.md` are read-only evidentiary sources this ADR builds upon; none is modified by this ADR.

**Affected Code:** None. No migration, model, schema, or test is created or modified by this ADR.

---

## 0. Repository Owner Decision (Recorded 2026-09-15)

**`[RO DECISION]` Option A is selected: the Authoritative Commercial Account Context does NOT carry a "classification" attribute.**

**Decision, verbatim in substance, per direct Repository Owner instruction:**

1. The Authoritative Commercial Account Context does **not** carry a "classification" attribute.
2. `COM-001-033` remains authoritative as written for Commercial Account: identity, hierarchy position, status. **`COM-001-033` is unchanged by this decision** — this decision confirms it as written; it does not amend, annotate, or otherwise touch the LOCKED text (§2.1).
3. No classification column, property, API field, validation rule, persistence field, event field, or other Account-classification semantic is authorized for C-022 BA-01.
4. The four affirmative Commercial Account classification references in `PE-001-C022` (§2.3) are therefore **inconsistent with this Repository Owner decision.**
5. That `PE-001-C022` inconsistency is handled as a **separate, future architecture-governance correction** — not performed by this ADR, not performed as part of this decision (§9).
6. `PE-001-C022` is **not modified** by this decision.
7. `COM-001` (LOCKED) is **not modified** by this decision.

**Rationale (as recorded):** Selecting Option A treats `COM-001-033` — the LOCKED, constitutional, Section-7 statement of the Commercial Account's own canonical fact set — as the controlling source for what BA-01 may persist, rather than treating `PE-001-C022`'s narrative-section classification references as having silently expanded a LOCKED construct's attribute set. This is the option that requires no LOCKED-document amendment (§6, Option A vs. Option B) and imposes no implementation block — it is available to apply immediately, without further governance process, because it changes nothing about what `COM-001-033` already says.

**Relationship to `ROD-C022-A` D7:** this decision **confirms and reinforces** `ROD-C022-A §B.2`'s existing D7 disposition (Option A — no classification field in BA-01). `ROD-C022-A` D7 is not superseded, altered, or reopened by this ADR — it is now doubly recorded: once as `ROD-C022-A`'s own interim BA-01-scoped decision, and now as this ADR's own resolution of the underlying LOCKED-vs-Active conflict `ROD-C022-A §B.2` had explicitly deferred. Both records are consistent and point to the same outcome.

**BA-01 implementation consequence:** none — `TDS-C022`'s current schema (§6.1, no `classification` column) already reflects this outcome and requires no further change on this specific point. No new implementation, schema, migration, or API work is triggered by this decision.

**Required future governance correction (not performed here):** `PE-001-C022`'s four affirmative classification-to-Account passages (`§1.4`, `C022-O02`, `EX-C022-04`'s Trigger and Business Goal, and the Guiding Architectural Question) now stand as a disclosed, uncorrected inconsistency against this Repository Owner decision. A future, separately-authorized `PE-001-C022` maintenance pass is required to reconcile them — mirroring the established precedent for other `PE-001-Cxxx` doc-sync corrections in this repository (e.g., the `PE-001-C021`/`PE-001-C040` masthead corrections). **This ADR does not perform that correction, does not schedule it, and does not authorize modifying `PE-001-C022` as part of this decision task.**

**This decision does NOT authorize:** modification of `PE-001-C022`; modification of `COM-001`; read/list scope for BA-01 (`ROD-C022-A` D8, untouched); lifecycle-pattern realization (`TDS-C022 §15.1`'s own unresolved item, untouched); CBOR registration eligibility or performance (`IRA-C022 §11`, `[C-6]`, untouched); BAR decision or registration (`IRA-C022 §11`, `[C-7]`, untouched); a Charter; a WP registration; implementation of any kind; or any schema/migration/API/frontend/code change. Each remains exactly as it stood before this decision (§12).

---

## 1. Context

C-022 Customer & Account Management's first Business Activity ("Establish Commercial Account") was investigated, decided (`ROD-C022`), assessed for readiness (`IRA-C022`), and technically designed (`TDS-C022`) across a sequence of governance passes this session. An independent reviewer, with no involvement in drafting any of those artifacts, found that the Authoritative Commercial Account Context's own attribute set is described inconsistently by two governing sources of different constitutional weight: `COM-001-033` (LOCKED, Section 7 of the Commercial & Subscription Architecture) and `PE-001-C022` (Active, v1.2, the Enterprise Experience Specification `COM-001` itself declares was extracted from). This is a `CLAUDE.md §16` canonical-authority conflict — *"If two canonical documents appear to conflict: 1. Stop implementation. 2. Identify the conflicting definitions. 3. Identify the declared canonical owner. 4. Review applicable ADRs. 5. Report the conflict before changing code. Never resolve canonical architecture conflicts by assumption."* This ADR performs steps 2, 3 (identification only — see §7), and 5 of that procedure. It does not perform step 4 in the sense of resolving the conflict; it is itself the ADR record §16 calls for, submitted for Repository Owner decision.

`COM-001`'s own Authoring Note (line 15, re-read directly for this ADR) states: *"This document is an extraction and constitutional formalization exercise, not new business invention... Every business concept defined below... already exists, fully engineered, in the four Active PE-001-Cxxx Experience specifications (... `PE-001-C022` v1.2 ...)."* `COM-001` therefore declares itself derived from `PE-001-C022`, among other sources — which is precisely why `COM-001-033`'s silence on classification is not self-evidently a deliberate exclusion; it is at least as plausibly an extraction gap. Only the Repository Owner (or an EARB review, if this ADR's resolution is judged to require one) can determine which.

---

## 2. Exact Conflicting Evidence

### 2.1 `COM-001-033` (LOCKED), re-read directly, complete text

> **COM-001-033: Authoritative Account Context**
> The single current, canonical commercial-container fact for a Commercial Account: identity, Account-to-Account hierarchy position, and status. Keyed only to its own Commercial Account Anchor. Never equivalent to a Workspace, Organization, Identity, Membership, or Billing Account.

Three attributes, exhaustively stated: **identity, hierarchy position, status.** No classification attribute anywhere in the clause.

### 2.2 `COM-001-032` (LOCKED), for contrast — the adjacent Customer clause, which DOES define classification

> **COM-001-032: Authoritative Customer Context**
> The single current, canonical identity fact for a Customer: legal-entity or person identity reference, classification, and status. Keyed only to its own Customer Anchor; exactly one per anchor.

Classification is present here — but this clause governs **Customer**, not Account.

### 2.3 `PE-001-C022` v1.2 (Active), re-extracted and re-read directly, four affirmative passages attaching classification to **Account**

> **`EX-C022-04` — Frame Commercial Party Reclassification Intent, Trigger:** "An existing Authoritative Customer Context's **or Authoritative Account Context's classification** no longer reflects the enterprise's understanding of the relationship."
>
> **`EX-C022-04`, Business Goal:** "Ensure classification changes are deliberate and attributable, never a silent correction."
>
> **`C022-O02` — Deliberate Commercial Party Evolution:** "Every change to **a Customer's or Account's classification**, or to a hierarchy/ownership relationship, begins from explicit, attributable business intent; the Authoritative Customer Context **and Authoritative Account Context** are never silently mutated."
>
> **`§1.4` Scope:** "...establishing, understanding, **reclassifying**, retiring and reactivating the Authoritative Customer Context **and the Authoritative Account Context**..."
>
> **Guiding Architectural Question (Document Control):** "...who its Customer is and which Commercial Account that Customer's relationship is organized through — **including that representation's classification**, hierarchy, and lineage through establishment, **reclassification**, relationship change, merger, division, transfer, retirement, and reactivation..."

`PE-001-C022 §1.16`'s own context-model table, by contrast, describes the Authoritative Account Context row using only *"its own identity, its Account-to-Account hierarchy position (parent Account reference, where applicable), and its current status"* — no classification attribute appears in that specific table row. **The conflict is therefore not merely between two documents, but between one document's own summary table (§1.16) and that same document's own narrative sections (§1.4, `C022-O02`, `EX-C022-04`, the GAQ) — all four of the narrative passages are unambiguous that reclassification, and therefore classification, applies to Account as well as Customer.**

### 2.4 Summary of the conflict

| Source | Weight | Does it attribute classification to Commercial Account? |
|---|---|---|
| `COM-001-033` | LOCKED (Constitutional, EARB CR-3.0) | **No.** |
| `PE-001-C022 §1.16` context-model table | Active (Enterprise Experience Spec) | No (table row is silent). |
| `PE-001-C022` — `§1.4`, `C022-O02`, `EX-C022-04`, GAQ | Active (same specification, narrative sections) | **Yes, in four places.** |

---

## 3. Impact on C-022 BA-01

If classification is a genuine Account attribute and BA-01 ships without it, the Authoritative Commercial Account Context BA-01 establishes cannot represent one of its own canonical facts, and a later schema `ALTER` would be required to add it — the exact outcome `TDS-C022`'s own "declare the full lifecycle shape now" discipline (already applied to `status` and `parent_account_id`) exists to avoid. If classification is not a genuine Account attribute, no impact — the current `TDS-C022` schema (§6.1, no `classification` column) is already correct as designed.

`ROD-C022-A` D7 (Option A — no classification field in BA-01) governs BA-01 today, and **is not altered by this ADR.** This ADR exists specifically because D7's own resolution left the underlying `COM-001-033` ↔ `PE-001-C022` conflict open, logged for a later, separate resolution — this is that resolution attempt, submitted for decision, not a re-litigation of D7 itself (see §12).

---

## 4. Impact on Downstream Capabilities (only where supported by the sources)

`COM-001-036` names Subscription (C-020), Product & Service Catalog (C-021, conditional), Licensing & Entitlement (C-023), Billing (C-024), and Contract (C-025) as consumers of *"the stable Customer Reference, Commercial Account Reference,... plus Account hierarchy and status"* — **`COM-001-036` itself does not name classification** among the attributes distributed downstream, only hierarchy and status. `[FINDING, not resolved by this ADR]` This raises a secondary question the sources do not directly settle: even if Commercial Account does carry a classification attribute (Option B, §6), `COM-001-036`'s own silence on distributing it means no downstream capability's own governing text currently claims to consume it. This ADR does not resolve whether that is itself an oversight or a deliberate limitation — it is noted here only because the evidence supports raising it, not inventing a downstream consumer that no source names.

No other downstream impact is supported by direct evidence; this ADR does not speculate further.

---

## 5. `[FACT]` `CLAUDE.md §16` Canonical Owner Identification (step 3 of the required procedure)

Per `CLAUDE.md §16`'s own resolution-owner examples, capability-specific Enterprise Experience content is normally owned by the relevant `PE-001-Cxxx` specification, while cross-capability constitutional data models are owned by their Layer-1 constitutional document — here, `COM-001`. **Both documents claim authority over the same fact (the Account's own attribute set) in this instance**, which is precisely the condition `§16` names as requiring escalation rather than a default-owner resolution: *"If two canonical documents appear to conflict... identify the declared canonical owner... review applicable ADRs... never resolve by assumption."* `COM-001` is LOCKED under EARB Constitutional Recertification CR-3.0 — amending it, if Option B is selected, requires the EARB-governed LOCKED-document amendment process, not an implementation-session edit (`CLAUDE.md §18`, `§19.6`).

---

## 6. Decision Options

### Option A — Commercial Account does NOT carry a classification attribute

- `COM-001-033` remains authoritative as written — identity, hierarchy position, status only.
- `PE-001-C022`'s four affirmative classification references (§2.3) are treated as requiring a later correction — either removed, or reframed so they no longer assert Account-level classification (e.g., limited to Customer, with the reclassification EX/Outcome text narrowed accordingly). That correction is **not performed by this ADR** and would itself require its own governance pass against `PE-001-C022` (an Active, not LOCKED, document — correctable through the normal `PE-001` maintenance-pass process already used elsewhere in this repository, e.g. the `PE-001-C040`/`PE-001-C021` masthead doc-sync debt precedent).
- `C-022` BA-01 remains without a classification field (consistent with `ROD-C022-A` D7's existing interim disposition).

### Option B — Commercial Account DOES carry a classification attribute

- `PE-001-C022`'s affirmative classification semantics (§2.3) are retained and treated as the more complete/correct statement of C-022's actual architecture.
- `COM-001-033` is treated as an incomplete extraction — silent because the extraction that produced `COM-001` (per its own Authoring Note, §1) did not carry this attribute forward, not because it was deliberately excluded.
- `COM-001-033` **must be formally amended or annotated** through the LOCKED-architecture governance process (EARB, or whatever process this repository's constitution designates for amending a document under Constitutional Recertification CR-3.0) before any implementation may rely on a Commercial Account classification field.
- **BA-01 implementation involving the classification attribute remains blocked** until that governance change is completed — this option does not authorize adding the field to `TDS-C022`/`c022_commercial_account` merely by virtue of being selected; the LOCKED-document amendment must complete first (§10).

### Option C — no materially different legitimate option found

This ADR's own re-read of `COM-001-033`, `COM-001-032`, `PE-001-C022`, and `ROD-C022-A` found no third resolution shape the sources themselves support (e.g., no evidence anywhere suggests a partial/conditional classification attribute, or a distinct third construct). No Option C is proposed, consistent with the instruction not to invent one where the sources do not support it.

---

## 7. Recommendation → Decision Recorded

~~**None is made.** No repository artifact was found, on the sources re-read for this ADR (`ROD-C022`, `ROD-C022-A`, `IRA-C022`, `TDS-C022`, `IRA-TDS-C022_Independent_Review.md`), that records an explicit Repository Owner decision resolving this exact `COM-001-033` ↔ `PE-001-C022` conflict — `ROD-C022-A §B.2` explicitly defers it: *"The `COM-001-033` ↔ `PE-001-C022` conflict itself is NOT resolved by this decision... logged as a separate, later architecture-governance correction item."* Per this ADR's own governing instruction, **this ADR therefore does not make a substantive recommendation and requires an explicit Repository Owner decision between Option A and Option B** (or a Repository-Owner-identified alternative, if the Repository Owner judges the sources support one this ADR did not find).~~ *(Superseded 2026-09-15 — the Repository Owner has since decided. See §0.)*

**The Repository Owner has selected Option A** (§0). This section is preserved, struck, as the historical record of this ADR's own state before the decision was recorded — accurate as of drafting, before the Repository Owner instruction that produced §0.

---

## 8. Consequences of Each Option

**If Option A is selected:** `TDS-C022`'s current schema (no `classification` column) requires no further change on this point. `PE-001-C022` carries a disclosed, uncorrected internal inconsistency until a future `PE-001` maintenance pass reconciles its four narrative passages with its own §1.16 table and with `COM-001-033`. No LOCKED-document amendment is required.

**If Option B is selected:** `COM-001-033` requires a formal LOCKED-document amendment before any implementation may add the field. `TDS-C022` would require a follow-up revision once that amendment exists, adding a `classification` column to `c022_commercial_account` (exact type/enumeration to be determined at that later TDS revision — not by this ADR). Until the amendment completes, `TDS-C022`'s current no-classification schema remains the only implementable design, identical in practical effect to Option A in the interim.

---

## 9. Required Governance Actions After the Repository Owner Decision

**Option A was selected (§0).** The applicable action:

- A future `PE-001-C022` maintenance pass (outside this ADR's own scope, not scheduled or performed here) to reconcile `§1.4`/`C022-O02`/`EX-C022-04`/GAQ with `§1.16` and `COM-001-033`. **This ADR does not modify `PE-001-C022`, does not schedule that future pass, and does not authorize it as part of the decision recorded in §0.**
- No action against `TDS-C022` is required — its current schema already reflects Option A.
- `COM-001` requires no amendment, since Option A (not Option B) was selected.
- This ADR's own `Status` field has been updated from `PROPOSED — AWAITING REPOSITORY OWNER DECISION` to `Accepted — Option A selected` (§0, header).

~~**If Option B:** initiation of this repository's LOCKED-document amendment process for `COM-001-033`...; only after that amendment is recorded may a `TDS-C022` revision add the classification column.~~ *(Not applicable — Option B was not selected. Preserved as historical record of the option considered and not chosen.)*

---

## 10. Explicit Implementation Gate

~~**No Commercial Account `classification` field may be implemented... until this conflict is formally resolved by an explicit Repository Owner decision recorded against this ADR...**~~ *(Superseded 2026-09-15 — the conflict has now been formally resolved. See §0.)*

**Resolved gate, current:** Option A having been selected (§0), **no Commercial Account `classification` field is authorized for C-022 BA-01, permanently, unless a future, separate Repository Owner decision supersedes this one.** This is not merely "not yet implemented" — it is now an affirmatively decided architectural position, consistent with `ROD-C022-A` D7 and `TDS-C022`'s current design (no classification column). This gate remains in force and is not loosened by any other pending C-022 item (read/list, lifecycle-pattern realization, CBOR, BAR, Charter, or WP registration — §12).

---

## 11. Traceability

| Item | Source |
|---|---|
| Conflict originally surfaced | `TDS-C022 §4` (original drafting pass) |
| Conflict found materially incomplete, four passages identified | `IRA-TDS-C022_Independent_Review.md §6.2`/`§6.4` |
| Interim RO decision — BA-01 excludes classification, conflict logged separately | `ROD-C022-A_Gate_Conditions_Classification_and_Read_List_Decision.md §B.2` (D7, Option A) |
| `TDS-C022` factual-citation correction (conclusion corrected to reflect the four passages) | `TDS-C022 §4` (remediation pass, this session) |
| This ADR | Performs the "separate, later architecture-governance correction item" `ROD-C022-A §B.2`/§D explicitly deferred |

---

## 12. Scope Boundary — What This ADR Does NOT Address

This ADR concerns **only** the Commercial Account classification conflict. It does not address, resolve, reopen, or comment substantively on: read/list scope for BA-01 (`ROD-C022-A` D8, unchanged); lifecycle-pattern realization (`TDS-C022 §15.1`'s own unresolved item, unchanged); CBOR registration eligibility or performance (`IRA-C022 §11`, `[C-6]`, unchanged); BAR (`IRA-C022 §11`, `[C-7]`, unchanged); any Charter, WP registration, or implementation authorization of any kind. `ROD-C022-A` D7 **remains authoritative and in force** — BA-01 excludes the classification field — until and unless superseded by an explicit new Repository Owner decision recorded against this ADR.

---

*End of ADR-038. Status: **Accepted — Option A selected** (Commercial Account does NOT carry a classification attribute), decided 2026-09-15 (§0). `COM-001-033` is unchanged and confirmed as written. `PE-001-C022` is unchanged; its four affirmative classification-to-Account passages are disclosed as an inconsistency against this decision, to be corrected in a future, separate, not-yet-authorized `PE-001-C022` maintenance pass. `ROD-C022-A` D7 is unchanged, confirmed, and remains in force. Read/list, lifecycle-pattern realization, CBOR, BAR, Charter, and WP registration are all untouched and remain exactly as they stood before this decision. No implementation, schema, migration, API, or frontend change is authorized by this ADR. Nothing was staged, committed, or pushed.*
