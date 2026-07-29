# ADR-006 — Structural Change Intent Registered as a Canonical Business Object (WP-04, C-005)

**Status:** Accepted
**Classification:** Architecture Governance / Business Object Registration
**Decided by:** Repository owner (architecture governance authority), during WP-04's own BA-03 gap analysis — the same decision-authority pattern ADR-003/004/005 already established during WP-01's own IRA-001 review.
**Affected Documents:** `architecture/05-Implementation/IRA-004_WP-04_Enterprise_Structure_Management_Implementation_Readiness_Assessment.md` (§21 records the full registration entry this ADR authorizes; §4/§7/§10 updated to reference it) — no other document amended.

---

## Context

IRA-004 §10 originally recorded BA-03 ("Frame Structural Change Intent") as Category D — "Governance clarification required" — reasoning that *"no persisted business object is evident from either PE-001-C005 or ERG-001; whether this is a database concept at all is undetermined."*

An architectural analysis, conducted independently of that framing, found the underlying question was posed incorrectly. The question IRA-004 asked — "does PE-001-C005 draw a database table for this?" — is not the question SD-002/CMD-001 make constitutionally prior. **CMD-001 §26.3** states: *"No Business Object shall be implemented until it has been registered in the Canonical Business Object Register... Registration precedes database design."* Registration eligibility is governed by **SD-002 §2**'s Universal Business Object Blueprint (independent identity, business meaning, ownership, governance, business state, references, traceability, versioned history, relationships) — a test independent of whether any capability specification happens to draw a table.

Applying that test directly to PE-001-C005's own text: EX-C005-04 ("Frame Structural Change Intent") produces "Change Intent Context, target outcome and decision boundary" as its own Created/Produced Context — and, decisively, **EX-C005-05** ("Shape Structural Proposal"), a separately-triggered Enterprise Experience realizing a different ERB (ERB-C005-04) than the one that created it, names "Change Intent Context" as its own **Required Context** and **Consumed Context**. A value that must be retrievable by identity from a later, independently-invoked experience cannot be a transient, request-scoped payload — it is, by construction, an object with independent identity (SD-002-004). EX-C005-04's own text further establishes governed ownership (Structural Steward), an AI-authority boundary (SD-002-019), and a real, if distributed, lifecycle including an explicitly named `SUPERSEDED`/`abandoned` terminal state (Invalidated Context) — satisfying SD-002 §2 on every tested dimension.

**No existing document contradicts this.** ERG-001 is silent (it owns structural/domain objects only, by its own stated boundary — not opposed, simply not the governing authority for an experience-layer construct). CMD-001 §26.4b's own "Pending Canonical Binding" mechanism exists precisely for this situation: a PE-001-Cxxx reference to a Business Object whose CBOR registration has not yet occurred is, by that section's own definition, a Business Object *awaiting* registration — not one that has been rejected.

**Why an ADR, not an inline IRA-004 note alone:** ADR-005 (WP-01) already establishes the repository's own precedent for exactly this situation — a governance decision surfacing during a Work Package's own readiness-assessment review, formalized as its own ADR rather than left as prose inside the IRA. This ADR follows that same discipline. CMD-001 (the constitutional home of CBOR, per DOC-000's own catalogue entry) is **LOCKED** — this ADR does not amend CMD-001's text, rules, or structure; it exercises CMD-001 §26.3's own registration mechanism, the same way any future Business Object registration will, without requiring CMD-001 itself to be reopened.

---

## Decision

1. **Register "Structural Change Intent" as a canonical Business Object**, identifier `SCI-000001`, per SD-002 §2 and CMD-001 §26.3/§26.4. The full registration entry (all sixteen CMD-001 §26.4 attributes, relationship mapping, and Business Activity mapping) is recorded in **IRA-004 §21**, which this ADR adopts by reference rather than duplicating here.
2. **Correct IRA-004's own BA-03 disposition** from Category D ("Governance clarification required") to Category C ("Architecture requires completion — implementation-level") — the constitutional question (is this a database concept at all) is resolved; ordinary implementation-level gap analysis (persistence mechanism, endpoint shape, service/repository design) remains, the same class of work BA-01 itself required.
3. **This ADR does not authorize BA-03's implementation.** CMD-001 §26.7 (Physical Implementation Mapping — tables, APIs, events) remains entirely unset. BA-03 still requires its own fresh implementation-readiness gap analysis per CLAUDE.md §19.7 before any code, migration, or schema is written.
4. **This ADR does not resolve BA-04's own disclosed ambiguity** (IRA-004 §4: which ERG-001 object a "proposal" ultimately attaches to) — Structural Change Intent's own `DERIVED_FROM` relationship to a specific ERG-001 object remains explicitly Pending Canonical Binding.

## Rationale

This decision is based exclusively on canonical documents already present in the repository: SD-002 (Universal Business Object Rules, §§1-2), CMD-001 (§26, Canonical Business Object Register), PE-001-C005 (ERB-C005-03/EX-C005-04, and EX-C005-05's own Required/Consumed Context reference), and IRA-004 itself. No new architecture is invented — SD-002 §2's eligibility test and CMD-001 §26.3's registration requirement both already exist; this ADR applies them to a concept IRA-004 had previously left untested against them.

The alternative — leaving BA-03 permanently blocked on "is this a database concept at all" — mistakes an implementation-detail question (what table, what schema) for the actually-prior constitutional question (does this concept qualify for CBOR registration at all), which SD-002 §2 already answers independently of any table ever being drawn.

## Consequences

- BA-03's Category D blocker is resolved; BA-03 becomes ordinary Category C work, subject to its own future implementation-readiness gap analysis — not implemented by this ADR.
- IRA-004 §4, §7, and §10 are updated to reference this ADR and IRA-004 §21; no other document changes.
- CMD-001 itself is not amended, consistent with its LOCKED status — this ADR exercises §26.3's existing registration mechanism rather than modifying CMD-001's rules.
- A **Governance Backlog Item** is recorded (IRA-004 §21): whether WP-04-registered Business Objects should eventually be consolidated into CMD-001 §26 itself is a future, separately-scoped decision, not made here.
- No implementation, schema, migration, API, or code exists or is authorized as a result of this ADR.

## Status

**Accepted**
