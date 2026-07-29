# ADR-008 — Proposed Outcome Context Registered as a Canonical Business Object (WP-04, C-005)

**Status:** Accepted
**Classification:** Architecture Governance / Business Object Registration
**Decided by:** Repository owner (architecture governance authority), during WP-04's own BA-04 constitutional analysis — the same decision-authority pattern ADR-004/005/006/007 already established during a Work Package's own readiness-assessment review.
**Affected Documents:** `architecture/05-Implementation/IRA-004_WP-04_Enterprise_Structure_Management_Implementation_Readiness_Assessment.md` (§22 records the full registration entry this ADR authorizes; §4/§7/§10 updated to reference it) — no other document amended. **ERG-001 is not amended. `ADR-007`'s own EnterpriseNode-only v1 scope decision is not amended.**

---

## Context

The BA-04 constitutional analysis (this Work Package's own prior turn, Architectural Decision Report) applied SD-002 §2's Universal Business Object Blueprint and the Cross-Experience Reference Test to "Proposed Outcome Context" (PE-001-C005, ERB-C005-04/EX-C005-05, BA-04's own produced object) and found it qualifies as a canonical Business Object — on stronger evidence than SCI-000001's own registration required. Where SCI-000001 (Structural Change Intent) was registered on the strength of a single downstream Required-Context reference (EX-C005-05), Proposed Outcome Context is named, in one paraphrase or another ("proposal," "coherent proposal," "reviewed proposal"), as Required/Consumed Context by **three** separately-invoked Enterprise Experiences governed by **three different ERBs**:

- EX-C005-07 (ERB-C005-05, BA-05): "Coherent proposal and current authoritative structural context."
- EX-C005-08 (ERB-C005-06, BA-06): "Proposal, Impact Context and review purpose."
- EX-C005-10 (ERB-C005-07, BA-07): "Reviewed proposal, resolved concerns and Impact Context."

A construct that three independently-triggered downstream experiences must retrieve, unchanged, by identity cannot be a transient, request-scoped payload under SD-002-004 — the identical reasoning ADR-006 already established as constitutional precedent for this repository (§21), applied here to a stronger fact pattern.

**No existing document contradicts this.** ERG-001 is silent (it owns structural/domain objects only, by its own stated boundary — Proposed Outcome Context is an experience-layer construct, not one of ERG-001's five structural objects). CMD-001 §26.4b's own "Pending Canonical Binding" mechanism already anticipated exactly this situation.

**Why an ADR, not an inline IRA-004 note alone:** ADR-006 already establishes the repository's own precedent for exactly this situation — a governance decision surfacing during a Work Package's own readiness-assessment review, formalized as its own ADR rather than left as prose inside the IRA. This ADR follows that same discipline. CMD-001 remains **LOCKED** — this ADR does not amend CMD-001's text, rules, or structure; it exercises CMD-001 §26.3's own registration mechanism, the same way SCI-000001's registration did, without requiring CMD-001 itself to be reopened.

---

## Decision

1. **Register "Proposed Outcome Context" as a canonical Business Object**, identifier `POC-000001`, per SD-002 §2 and CMD-001 §26.3/§26.4. The full registration entry (all sixteen CMD-001 §26.4 attributes, relationship mapping, and Business Activity mapping) is recorded in **IRA-004 §22**, which this ADR adopts by reference rather than duplicating here.
2. **Correct IRA-004's own BA-04 disposition note (§10)** to record that both of BA-04's constitutional questions — target-type scope (`ADR-007`) and Business Object registration (this ADR) — are now resolved. BA-04's Category remains **C** (Architecture requires completion — implementation-level), unchanged in classification from the disposition ADR-007 already established; this ADR does not reclassify it further, it removes the second of two open constitutional items under that classification.
3. **This ADR does not authorize BA-04's implementation.** CMD-001 §26.7 (Physical Implementation Mapping — tables, APIs, events) remains entirely unset for POC-000001. BA-04 still requires its own fresh implementation-readiness gap analysis per CLAUDE.md §19.7 before any code, migration, or schema is written.
4. **This ADR does not amend `ADR-007`.** POC-000001's own `DERIVED_FROM` relationship to EnterpriseNode is recorded in IRA-004 §22 as "Bound for BA-04 v1" strictly *because* ADR-007 already decided that scope for BA-04's implementation — this registration reflects that prior decision, it does not make a new one. EnterpriseRelationship/ConsolidationDetermination-targeted proposal support remains deferred exactly as ADR-007 left it.
5. **This ADR does not narrow SCI-000001's own registration.** IRA-004 §21 (Structural Change Intent's own CBOR entry) is unamended by this decision; the two objects' mutual relationship (`PRECEDES`/`DERIVED_FROM`) is recorded consistently in both §21 and §22 without either entry being rewritten to accommodate the other.

## Rationale

This decision is based exclusively on canonical documents already present in the repository: SD-002 (§2), CMD-001 (§26), PE-001-C005 (EX-C005-05 through EX-C005-10's own Required/Produced/Consumed Context text), and IRA-004/ADR-006/ADR-007 themselves. No new architecture is invented — SD-002 §2's eligibility test and CMD-001 §26.3's registration requirement both already exist and were already applied once, to SCI-000001; this ADR applies the identical, already-accepted test to a second concept the same readiness assessment surfaced.

The alternative — implementing BA-04 (which necessarily requires a new table for Proposed Outcome Context, the same "Create, not Extend" disposition SCI-000001 itself required) without registering the object first — would directly contradict CMD-001 §26.3's own unconditional sequencing rule ("Registration precedes database design"), the same rule that stopped BA-03 until SCI-000001 was registered.

## Consequences

- BA-04's second open constitutional question (Business Object registration) is resolved; BA-04 remains Category C, subject to its own future implementation-readiness gap analysis — not implemented by this ADR.
- IRA-004 §4, §7, and §10 are updated to reference this ADR and IRA-004 §22; §21 (SCI-000001) is unamended; no other document changes.
- CMD-001 itself is not amended, consistent with its LOCKED status.
- The Governance Backlog Item already recorded at IRA-004 §21 (whether WP-04-registered objects should eventually be consolidated into CMD-001 §26 itself) applies identically to POC-000001 and is not re-recorded.
- No implementation, schema, migration, API, or code exists or is authorized as a result of this ADR.

## Status

**Accepted**
