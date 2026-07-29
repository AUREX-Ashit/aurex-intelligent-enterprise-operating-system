# ADR-010 — The Structural Context Lifecycle Recognized as a Canonical Architectural Pattern (WP-04, C-005)

**Status:** Accepted
**Classification:** Architecture Governance / Canonical Pattern Recognition
**Decided by:** Repository owner (architecture governance authority), during WP-04's own BA-06 implementation-readiness assessment — the same decision-authority pattern ADR-006/008/009 already established, applied here to a pattern rather than a single object.
**Affected Documents:** `architecture/05-Implementation/IRA-004_WP-04_Enterprise_Structure_Management_Implementation_Readiness_Assessment.md` (§24 records this pattern's recognition) — no other document amended. **SD-002 and CMD-001 are not amended. ERG-001 is not amended. ADR-006, ADR-007, ADR-008, and ADR-009 are not amended or revisited — each remains the specific registration/scope decision it always was; this ADR does not retroactively change how any of them was decided, only records that they were, in hindsight, each an instance of one already-declared specification pattern.**

---

## Context

BA-03, BA-04, and BA-05 each independently applied SD-002 §2's Universal Business Object Blueprint and the Cross-Experience Reference Test to a construct their own implementation-readiness assessment surfaced — Structural Change Intent (ADR-006), Proposed Outcome Context (ADR-008), and Impact Context (ADR-009) respectively — each time re-deriving the eligibility analysis from PE-001-C005's own ERB/EX chapters (Chapters 40–41) in isolation. BA-06's own readiness assessment then identified a fourth candidate, Review Context, prompting a fresh repository review that consulted PE-001-C005 **Chapter 38** for the first time in this Work Package.

That review found PE-001-C005 does not leave this pattern to be inferred. **§38.15 ("C-005 Context Model")** is a named, formal table enumerating ten Context types, **§38.17 ("Context Transitions")** gives their formal transition semantics as one linear sequence, and Chapter 43's governance invariants — most decisively **GS-INV-006** ("Impact, Review and Validation Context SHALL identify the exact proposal revision to which they apply") and **GS-INV-007** ("A material proposal revision SHALL invalidate dependent readiness and SHALL trigger reassessment of affected impact or review context") — govern multiple stages of this sequence jointly, as one family, not as unrelated rules that happen to resemble each other.

§38.15's own table, cross-referenced against what has already been registered:

| Context (§38.15) | Rule (§38.15, verbatim) | Status |
|---|---|---|
| Enterprise Context | "Mandatory throughout." | Cross-cutting session context — not a Business Object |
| Structural Focus | "Preserved until explicitly changed." | Points at EnterpriseNode (ERG-001) — not itself a Business Object |
| Journey Intent | "Preserved through review and completion." | Cross-cutting session context — not a Business Object |
| Change Intent Context | "Created before a governed proposal." | **SCI-000001 (ADR-006)** |
| Proposed Outcome Context | "Never represented as current authoritative structure." | **POC-000001 (ADR-008)** |
| Comparison / Impact Context | "Preserved during assessment and review." | **IMC-000001 (ADR-009)** |
| Review Context | "Preserved through resolution and validation." | Candidate — not registered by this ADR |
| Validation Context | "Invalidated by material proposal change." | Candidate — not registered by this ADR |
| Resulting Structural Context | "Structural context produced by successful completion." | Candidate — not registered by this ADR |
| Navigation Context | "Preserved where practical." | Cross-cutting UX/session state — not a Business Object |

Three of the six substantive rows are already registered, independently, through three near-identical analytical passes. This ADR recognizes, once, what §38.15 already states: these six rows are stages of **one specification-declared pipeline**, not six unrelated discoveries.

---

## Decision

1. **The "Structural Context Lifecycle" is recognized as a canonical architectural pattern of C-005**, consisting of the six substantive Context stages named in PE-001-C005 §38.15 (Change Intent Context → Proposed Outcome Context → Comparison/Impact Context → Review Context → Validation Context → Resulting Structural Context), governed by §38.17's transition semantics and Chapter 43's GS-INV-003 through GS-INV-012 invariants.
2. **This recognition does not itself register any Business Object.** Structural Change Intent, Proposed Outcome Context, and Impact Context remain registered exactly as ADR-006, ADR-008, and ADR-009 each independently decided — this ADR changes nothing about those three entries (IRA-004 §21/§22/§23 are unamended). Review Context, Validation Context, and Resulting Structural Context remain **unregistered** — this ADR does not register them either, per this task's own explicit instruction.
3. **Each remaining Context object still requires its own independent CBOR registration** under CMD-001 §26.3/§26.4 before its own owning Business Activity implements it — its own Business Object Identifier, Aggregate Root, Owner, Lifecycle Model, and Relationship Mapping, exactly as SCI-000001/POC-000001/IMC-000001 each received. **This pattern is never a substitute for that registration.**
4. **Future registrations of a Structural Context Lifecycle member may reference this ADR instead of re-deriving the SD-002 §2 eligibility analysis from first principles.** The general question — "is a §38.15 Context Model row eligible for CBOR registration" — is answered once, here, by direct application of §38.15/§38.17/GS-INV-006-007 to the pattern as a whole. Each object's own registration still independently supplies its own §26.4 attributes (identifier, owner, lifecycle detail, relationships) — only the *eligibility* derivation is shared, not the registration content.
5. **No Context Business Object is merged, combined, or represented as a single aggregate.** Structural Change Intent, Proposed Outcome Context, Impact Context, Review Context, Validation Context, and Resulting Structural Context each remain their own Aggregate Root with their own identity (SD-002-004), consistent with CLAUDE.md's Golden Rule ("One entity, one definition") and with how ADR-006/008/009 already registered the first three. This ADR recognizes a *sequence* of independently-identified objects, not a merged supertype.
6. **SD-002 and CMD-001 are not amended.** This ADR exercises SD-002 §2's own eligibility test and CMD-001 §26.3's own registration mechanism against a pattern PE-001-C005 already declares; it introduces no new constitutional rule, no new registration attribute, and no exception to §26.3's registration-precedes-implementation sequencing.

## Rationale

§38.15 is not new evidence about the world — it is text that already existed in PE-001-C005 before this Work Package began, simply not consulted by any Business Activity's own readiness assessment until BA-06's. Continuing to treat each remaining Context stage as an independent discovery would repeat, a third and fourth time, an analytical derivation §38.15/§38.17/GS-INV-006-007 already settle collectively. Recognizing the pattern once — without registering its remaining members, and without weakening the requirement that each still be individually registered — converts redundant re-derivation into a single referenceable precedent, consistent with CLAUDE.md §19.8's own general principle that a recurring, already-settled observation should be tracked once and cited thereafter rather than re-argued.

## Consequences

- IRA-004 §24 records this pattern's recognition, cross-referencing §21/§22/§23 (already-registered members) and naming Review Context, Validation Context, and Resulting Structural Context as its remaining, not-yet-registered members.
- BA-06 remains blocked on Review Context's own individual registration — this ADR does not unblock BA-06 by itself. A future, separately-scoped registration task (mirroring ADR-006/008/009's own registration-entry format) may now reference this ADR for the eligibility question, rather than re-deriving it.
- ADR-006, ADR-007, ADR-008, and ADR-009 are unamended and unrevisited.
- SD-002, CMD-001, ERG-001, and IMP-001 are unamended.
- No implementation, schema, migration, API, or code exists or is authorized as a result of this ADR.

## Status

**Accepted**
