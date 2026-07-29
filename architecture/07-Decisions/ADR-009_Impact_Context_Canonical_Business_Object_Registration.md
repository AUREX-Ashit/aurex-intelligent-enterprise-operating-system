# ADR-009 — Impact Context Registered as a Canonical Business Object (WP-04, C-005)

**Status:** Accepted
**Classification:** Architecture Governance / Business Object Registration
**Decided by:** Repository owner (architecture governance authority), during WP-04's own BA-05 implementation-readiness assessment — the same decision-authority pattern ADR-006/ADR-008 already established.
**Affected Documents:** `architecture/05-Implementation/IRA-004_WP-04_Enterprise_Structure_Management_Implementation_Readiness_Assessment.md` (§23 records the full registration entry this ADR authorizes; §4/§7/§10 updated to reference it) — no other document amended. **ERG-001 is not amended. ADR-006, ADR-007, and ADR-008 are not amended or revisited.**

---

## Context

BA-05's own implementation-readiness assessment (this Work Package's own prior turn) applied the identical SD-002 §2 Universal Business Object Blueprint test and Cross-Experience Reference Test already used for SCI-000001 (ADR-006) and POC-000001 (ADR-008) to "Impact Context" (PE-001-C005, ERB-C005-05/EX-C005-07, BA-05's own produced object) and found it qualifies:

- EX-C005-08 (ERB-C005-06, BA-06): Required/Consumed Context, verbatim: "Proposal, **Impact Context** and review purpose."
- EX-C005-10 (ERB-C005-07, BA-07): Required/Consumed Context, verbatim: "Reviewed proposal, resolved concerns and **Impact Context**."

Two separately-invoked Enterprise Experiences, governed by two different ERBs than BA-05's own ERB-C005-05, each name Impact Context as their own Required Context — the identical decisive-evidence pattern already accepted twice in this Work Package. PE-001-C005's own Chapter 42 text independently corroborates this: "Impact Context is mandatory for review readiness unless a canonical journey records a traceable exception" — treating it as a standing, referenceable artifact, not a value discarded after EX-C005-07 completes.

Applying SD-002 §2 directly: independent identity (must be retrievable, unchanged, by BA-06 and BA-07); a real lifecycle (EX-C005-07's own Invalidated Context: "Impact observations invalidated by material proposal revision"); governed ownership (Structural Steward, Structural Reviewer); and an explicit AI-authority boundary (EX-C005-07's own AI Assistance clause) — every dimension already tested for SCI-000001 and POC-000001.

**No existing document contradicts this.** ERG-001 is silent (it owns structural/domain objects only). CMD-001 §26.4b's own "Pending Canonical Binding" mechanism already anticipated exactly this situation.

**Why an ADR, not an inline IRA-004 note alone:** ADR-006 and ADR-008 already establish the repository's own precedent for exactly this situation — a governance decision surfacing during a Work Package's own readiness-assessment review, formalized as its own ADR. This ADR follows that same discipline a third time. CMD-001 remains **LOCKED** — this ADR does not amend CMD-001's text, rules, or structure; it exercises CMD-001 §26.3's own existing registration mechanism.

---

## Decision

1. **Register "Impact Context" as a canonical Business Object**, identifier `IMC-000001`, per SD-002 §2 and CMD-001 §26.3/§26.4. The full registration entry is recorded in **IRA-004 §23**, which this ADR adopts by reference rather than duplicating here.
2. **Correct IRA-004's own BA-05 disposition (§10)** from Category D ("Depends on BA-04's own resolution first" — stale, since BA-04 is now implemented) to Category C (Architecture requires completion — implementation-level), recording that both BA-05's dependency on BA-04 and its own Business Object registration question are now resolved.
3. **This ADR does not authorize BA-05's implementation.** CMD-001 §26.7 (Physical Implementation Mapping) remains entirely unset for IMC-000001. BA-05 still requires its own fresh implementation-readiness gap analysis per CLAUDE.md §19.7 before any code, migration, or schema is written.
4. **This ADR does not revisit ADR-006, ADR-007, or ADR-008.** SCI-000001's and POC-000001's own registrations (IRA-004 §21/§22) are unamended; ADR-007's EnterpriseNode-only v1 proposal-target scope is unamended and unaffected.
5. **This ADR does not decide whether "Review Context" (BA-06) or "Validation Context" (BA-07) require their own CBOR registration.** Each is that future Business Activity's own eligibility question, to be tested against SD-002 §2 at that Business Activity's own readiness-assessment time — not assumed, and not foreclosed, by this decision.

## Rationale

This decision applies exclusively already-accepted constitutional machinery (SD-002 §2, CMD-001 §26.3) to a third concept this Work Package's own methodology surfaced, using the same evidentiary standard already validated twice. The alternative — implementing BA-05 (which requires persisting its computed output for BA-06/BA-07 to later retrieve, the same "Create, not transient" disposition SCI-000001/POC-000001 both required) without registering the object first — would directly contradict CMD-001 §26.3's own unconditional sequencing rule, repeating the exact defect ADR-006/ADR-008 each existed to prevent.

## Consequences

- BA-05's Business Object registration question is resolved; BA-05 remains Category C, subject to its own future implementation-readiness gap analysis — not implemented by this ADR.
- IRA-004 §4, §7, and §10 are updated to reference this ADR and IRA-004 §23; §21/§22 (SCI-000001/POC-000001) are unamended; no other document changes.
- CMD-001 itself is not amended, consistent with its LOCKED status.
- The Governance Backlog Item already recorded at IRA-004 §21 (whether WP-04-registered objects should eventually be consolidated into CMD-001 §26 itself) applies identically to IMC-000001 and is not re-recorded.
- No implementation, schema, migration, API, or code exists or is authorized as a result of this ADR.

## Status

**Accepted**
