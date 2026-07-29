# ADR-011 — Review Context Registered as a Canonical Business Object (WP-04, C-005)

**Status:** Accepted
**Classification:** Architecture Governance / Business Object Registration
**Decided by:** Repository owner (architecture governance authority), during WP-04's own BA-06 constitutional alignment — the same decision-authority pattern ADR-006/ADR-008/ADR-009 already established, this time citing `ADR-010` for eligibility rather than re-deriving it.
**Affected Documents:** `architecture/05-Implementation/IRA-004_WP-04_Enterprise_Structure_Management_Implementation_Readiness_Assessment.md` (§25 records the full registration entry this ADR authorizes; §4/§7/§10 updated to reference it) — no other document amended. **ERG-001 is not amended. ADR-006, ADR-007, ADR-008, ADR-009, and ADR-010 are not amended or revisited.**

---

## Context

`ADR-010` recognized the Structural Context Lifecycle — six substantive Context stages explicitly declared by PE-001-C005 §38.15/§38.17 and governed jointly by Chapter 43's GS-INV-003 through GS-INV-012 — as a canonical architectural pattern, without itself registering any of the three then-outstanding members (Review Context, Validation Context, Resulting Structural Context). Per ADR-010's own Decision point 4, future registrations of a Structural Context Lifecycle member may cite that ADR for the eligibility question instead of re-deriving the SD-002 §2 analysis from first principles — while still independently supplying each object's own CMD-001 §26.4 attributes.

This ADR performs that registration for the fourth stage: **Review Context**, PE-001-C005's own §38.15 row (Meaning: "Review purpose, concerns, decisions and unresolved issues"; Rule: "Preserved through resolution and validation"), produced by ERB-C005-06/EX-C005-08 (Review Proposed Structural Outcome) and consumed within the same Business Activity by EX-C005-09 (Resolve Structural Review Concerns).

**Eligibility is not re-derived here** — it is inherited from ADR-010's own recognition of the pattern as a whole, corroborated directly by GS-INV-006 ("Impact, Review and Validation Context SHALL identify the exact proposal revision to which they apply") naming Review Context alongside the already-registered Impact Context under one governing rule, and by BR-C005-006 ("Review SHALL identify the exact proposal revision under review"), which presupposes a real, persisted, identifiable record — the same SD-002-004 independent-identity signal already accepted for SCI-000001/POC-000001/IMC-000001.

---

## Decision

1. **Register "Review Context" as a canonical Business Object**, identifier `RVC-000001`, per SD-002 §2, CMD-001 §26.3/§26.4, and `ADR-010`'s own pattern recognition. The full registration entry is recorded in **IRA-004 §25**, which this ADR adopts by reference rather than duplicating here.
2. **Correct IRA-004's own BA-06 disposition (§10)** to reflect that Review Context is now registered, replacing the prior placeholder disposition ("B, likely, pending BA-04" — written before BA-06's own gap analysis and before this Work Package's Context Lifecycle pattern was recognized).
3. **This ADR does not authorize BA-06's implementation.** CMD-001 §26.7 (Physical Implementation Mapping) remains entirely unset for RVC-000001. BA-06 still requires its own fresh implementation-readiness gap analysis per CLAUDE.md §19.7 before any code, migration, or schema is written.
4. **This ADR does not resolve EX-C005-09's own disclosed ambiguity** — whether "resolve concerns" produces a distinct artifact of Review Context or simply invokes BA-04's already-implemented Refine mechanism (a new `StructuralProposal` revision) remains open, exactly as disclosed when BA-06 first identified Review Context as a candidate. That is BA-06's own future implementation-readiness gap analysis's question, not a registration question.
5. **This ADR does not revisit ADR-006, ADR-007, ADR-008, ADR-009, or ADR-010.** SCI-000001's, POC-000001's, and IMC-000001's own registrations (IRA-004 §21/§22/§23) are unamended; the Structural Context Lifecycle pattern (IRA-004 §24) is unamended.
6. **Validation Context and Resulting Structural Context remain unregistered.** This ADR registers Review Context only — the fifth and sixth pattern stages each require their own future, separately-scoped registration.

## Rationale

This decision applies CMD-001 §26.3's own registration mechanism to the fourth member of a pattern already recognized in full (ADR-010), using the eligibility analysis ADR-010 already performed rather than re-deriving it — precisely the efficiency ADR-010 existed to create. The alternative — implementing BA-06 (which necessarily requires persisting Review Context, since BR-C005-006 requires it be identifiable and re-referenceable, the same "Create, not transient" disposition every prior stage required) without registering the object first — would repeat, unremediated, the exact defect ADR-006/008/009 each existed to prevent.

## Consequences

- BA-06's own Business Object registration question is resolved; BA-06 remains subject to its own future implementation-readiness gap analysis — not implemented by this ADR.
- IRA-004 §4, §7, and §10 are updated to reference this ADR and IRA-004 §25; §21/§22/§23 (SCI-000001/POC-000001/IMC-000001) and §24 (the pattern itself) are unamended; no other document changes.
- CMD-001 itself is not amended, consistent with its LOCKED status.
- The Governance Backlog Item already recorded at IRA-004 §21 (whether WP-04-registered objects should eventually be consolidated into CMD-001 §26 itself) applies identically to RVC-000001 and is not re-recorded.
- Validation Context and Resulting Structural Context remain the two outstanding Structural Context Lifecycle members, each requiring its own future registration mirroring this one.
- No implementation, schema, migration, API, or code exists or is authorized as a result of this ADR.

## Status

**Accepted**
