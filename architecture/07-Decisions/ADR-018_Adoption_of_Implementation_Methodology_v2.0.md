# ADR-018 — Adoption of Implementation Methodology v2.0

**Status:** Accepted
**Classification:** Architecture Governance / Methodology Adoption
**Decided by:** Repository Owner (architecture governance authority), per direct instruction ("Implementation Methodology v2.0 Establishment / WP-10 Planning Authorization," 2026-08-02) — the same decision-authority pattern `ADR-014`/`ADR-017` already established, this time authorizing a methodology formalization following WP-09's own complete, certified, five-gate closure, the first Work Package to run this repository's own full lifecycle end to end under `CLAUDE.md §20`.
**Affected Documents:** **None edited by this ADR.** This ADR is the governance authorization that permits `CLAUDE.md` to be edited in the same coordinated implementation pass, per §5 (Implementation Roadmap) below. Consistent with `ADR-014`/`ADR-017`'s own precedent, the actual edit is performed as a distinct, disclosed follow-on action, not folded silently into this decision record.

---

## 1. Context

`METH-003` (`architecture/03-Engineering/METH-003_Implementation_Methodology_v2.md`) documents three genuine, evidenced lessons from WP-09's own execution: (1) a proven reuse-without-reopening pattern for a later Business Activity extending an earlier, already-approved one; (2) a mandatory, proactive tenant-isolation test checklist, directly evidenced by the one `CLAUDE.md §19.8.5`-class defect this repository's own five-gate sequence has found in new code (WP-09's own Gate 2 finding, the same root cause `VV-AUDIT-WP-05`'s own F-02 already named in an unrelated Work Package); and (3) two genuine process changes the Repository Owner has directly authorized — a Standard Work Package Lifecycle naming Strategic Enhancement Review, Historical Screen Review, and Executive Cognition Review as formal pre-Business-Activity steps, and a relaxed commit/approval cadence (one Repository Owner authorization per complete Work Package, not per Business Activity).

Unlike `METH-001`/`METH-002` — each triggered by a single Work Package's own retrospective finding — `METH-003` is triggered by an explicit Repository Owner instruction establishing methodology for all remaining Releases (B through F), not by an audit finding requiring correction. Its own adoption criteria are accordingly not "does this fix a defect" but "does this correctly synthesize already-canonical authority without redefining it, and are its genuinely new elements explicitly Repository-Owner-authorized."

## 2. Decision

**This ADR adopts `METH-003` in full**, with no modification, no deferral, and no rejection — every element was either (a) already Repository-Owner-authorized by the establishing instruction itself, or (b) a direct, cited restatement of already-canonical authority (`IMP-001`, `CLAUDE.md §20`, `PE-001`, `SD-001`, `DS-001`), verified against those sources during drafting, not invented.

## 3. Approved Improvements

1. **Dual-Dimension Business Activity Completion checklist (`METH-003 §2`)** — a single practical checklist combining `CLAUDE.md §20.3`'s Vertical Slice Requirement and `§20.7`'s Work Package Completion Gate Extension, which previously had to be inferred from two separate sections each time. Restatement only; no new rule.
2. **Reuse-Without-Reopening Pattern (`METH-003 §3.2`)** — names the additive-method pattern WP-09's own BA-03 established as the standard approach for a later Business Activity reusing an earlier one's own logic, per `CLAUDE.md §19.5`'s existing Reuse-first order.
3. **Mandatory Tenant-Isolation Test Checklist (`METH-003 §3.3`)** — the one genuinely new testing requirement, converting `WP-09`'s own Gate 2 V&V Audit finding (and its exact precedent, `VV-AUDIT-WP-05`'s own F-02) from a reactive audit discovery into a proactive submission gate for every endpoint whose data model carries an organization/tenant boundary.
4. **Standard Work Package Lifecycle (`METH-003 §4`)** — formalizes Strategic Enhancement Review, Historical Screen Review, and Executive Cognition Review as named steps preceding Business Activity work, per the establishing instruction's own explicit Phase 8.
5. **Relaxed commit/approval cadence (`METH-003 §5`)** — one Repository Owner authorization executes one complete Work Package, not one Business Activity; multiple logical commits remain encouraged. Per the establishing instruction's own explicit authorization, justified by WP-09's own demonstration that the five-gate sequence catches what needs catching without per-Business-Activity checkpoints.
6. **World-Class Enterprise Experience Evaluation checklist (`METH-003 §9`)** — consolidates already-scattered principles across `PE-001` Chapters 5/6/8, `SD-001` Sections 2/5/9/10/11, and `CLAUDE.md §20.5` into one checklist applied at Independent Certification. Restatement only; `§20.5`'s own "interaction-quality reference only, never visual imitation" constraint is preserved verbatim, not relaxed.

## 4. Modified Improvements

**None.** Every element of `METH-003` was scoped, at drafting time, to either restate existing canonical authority with a citation or implement an element the establishing Repository Owner instruction itself explicitly authorized — no independent judgment call required correction before adoption.

## 5. Implementation Roadmap

The coordinated implementation pass this ADR authorizes:

**`CLAUDE.md`** — add a new, purely additive **§21, "Implementation Methodology v2.0 (WP-10 onward)"** — mirroring exactly how `§20` itself was added ("Formalized per direct Repository Owner governance instruction... Prospective Only... does NOT reopen any Work Package already CLOSED") and how `ADR-017` added `§19.7b` (new section, no existing text altered, no renumbering). The new section states the Standard Work Package Lifecycle and relaxed cadence at constitutional-document weight, and points to `METH-003` for the full synthesis and evidentiary basis, per this repository's own single-authoritative-source discipline — it does not duplicate `METH-003`'s own content a second time.

**This ADR does not perform that edit.** It is performed as its own distinct, disclosed edit in this same implementation pass, mirroring `ADR-014`/`ADR-017`'s own precedent of separating authorization from execution.

## 6. Consequences

- Every Work Package from WP-10 onward follows the Standard Work Package Lifecycle (`METH-003 §4`) and the relaxed, per-Work-Package (not per-Business-Activity) approval cadence (`METH-003 §5`).
- Every new endpoint with an organization/tenant boundary must satisfy the Mandatory Tenant-Isolation Test Checklist (`METH-003 §3.3`) before Independent Certification — closing the specific, twice-recurring gap `VV-AUDIT-WP-05`'s F-02 and `VV-AUDIT-WP-09`'s Finding 2 both independently found.
- WP-01 through WP-09 are **not** reopened or re-audited by this ADR — each remains valid under the governance that existed at its own certification, the same principle `CLAUDE.md §20.1` already applies to §20 itself, extended here to `§21`.
- `CLAUDE.md`'s own existing §1–§20 text is not altered — `§21` is purely additive, the same "operationalize without amending existing adopted text" discipline `ADR-014`/`ADR-017` already used.
- `IMP-001`, `PE-001`, `SD-001`, `DS-001` are not edited by this ADR — `METH-003` synthesizes their existing content; it does not claim to supersede any of it, per `CLAUDE.md §16`.

## Status

**Accepted**
