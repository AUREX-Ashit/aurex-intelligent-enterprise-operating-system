# ADR-012 — Validation Context Registered as a Canonical Business Object (WP-04, C-005)

**Status:** Accepted
**Classification:** Architecture Governance / Business Object Registration
**Decided by:** Repository owner (architecture governance authority), during WP-04's own BA-07 constitutional alignment — the same decision-authority pattern ADR-006/ADR-008/ADR-009/ADR-011 already established, citing `ADR-010` for eligibility rather than re-deriving it.
**Affected Documents:** `architecture/05-Implementation/IRA-004_WP-04_Enterprise_Structure_Management_Implementation_Readiness_Assessment.md` (§26 records the full registration entry this ADR authorizes; §4/§7/§10 updated to reference it) — no other document amended. **ERG-001 is not amended. ADR-006, ADR-007, ADR-008, ADR-009, ADR-010, and ADR-011 are not amended or revisited.**

---

## Context

`ADR-010` recognized the Structural Context Lifecycle — six substantive Context stages declared by PE-001-C005 §38.15/§38.17 and governed jointly by Chapter 43's GS-INV-003 through GS-INV-012 — as a canonical architectural pattern. Four members are already registered (SCI-000001, POC-000001, IMC-000001, RVC-000001). BA-07's own implementation-readiness assessment independently re-confirmed, without relying on the prior four registrations as precedent alone, that **Validation Context** — the pattern's fifth stage, produced by ERB-C005-07/EX-C005-10 — satisfies both SD-002 §2's Universal Business Object Blueprint and the Cross-Experience Reference Test, on evidence at least as decisive as any prior stage's own case:

- **§38.15** (C-005 Context Model): named row — "Validation Context — Readiness of the exact reviewed proposal revision. — Invalidated by material proposal change."
- **§38.17** (Context Transitions): "Review → validation: Creates Validation Context for the exact reviewed proposal."
- **§40.8** (ERB-C005-07's own Chapter 40 entry): Exit Context — "Validated Transition Context or explicit return-to-resolution context."
- **§40.9** (ERB-C005-08's own Chapter 40 entry): Entry Context — "**Validated Transition Context**" — a separately-invoked Business Activity (BA-08) under a different ERB (ERB-C005-08) explicitly requiring this as its own formal entry condition, a cleaner cross-ERB anchor than several prior stages' own evidence.
- **GS-INV-006** — "Impact, Review and **Validation Context** SHALL identify the exact proposal revision to which they apply" — named alongside the two already-registered siblings under one governing rule.
- **GS-INV-007/GS-INV-008/GS-INV-012** — govern invalidation-on-revision, the precondition for Resulting Structural Context, and completion's own traceability to the exact validated revision, respectively.

**Eligibility is not re-derived here in full** — per `ADR-010`'s own Decision point 4, this registration cites that ADR's pattern recognition for the general question, while independently supplying Validation Context's own CMD-001 §26.4 attributes below.

---

## Decision

1. **Register "Validation Context" as a canonical Business Object**, identifier `VLC-000001`, per SD-002 §2, CMD-001 §26.3/§26.4, and `ADR-010`'s own pattern recognition. The full registration entry is recorded in **IRA-004 §26**, which this ADR adopts by reference rather than duplicating here.
2. **Correct IRA-004's own BA-07 disposition (§10)** to reflect that Validation Context is now registered, replacing the prior placeholder disposition ("B, likely, pending BA-04/BA-06" — written before either existed).
3. **This ADR does not authorize BA-07's implementation.** CMD-001 §26.7 (Physical Implementation Mapping) remains entirely unset for VLC-000001. BA-07 still requires its own fresh implementation-readiness gap analysis per CLAUDE.md §19.7 before any code, migration, or schema is written.
4. **This ADR does not decide how the "readiness result" is represented.** EX-C005-10's own Exit Context offers two outcomes ("Validated Transition Context or explicit return-to-resolution context") — whether this is a field on Validation Context itself, a row created only on success, or another representation is BA-07's own future implementation-readiness gap analysis's question, not decided here.
5. **This ADR does not revisit ADR-006 through ADR-011.** SCI-000001's, POC-000001's, IMC-000001's, and RVC-000001's own registrations (IRA-004 §21/§22/§23/§25) are unamended; the Structural Context Lifecycle pattern (IRA-004 §24) is unamended.
6. **Resulting Structural Context remains unregistered.** This ADR registers Validation Context only — the pattern's sixth and final stage requires its own future, separately-scoped registration.

## Rationale

This decision applies CMD-001 §26.3's own registration mechanism to the fifth member of a pattern already recognized in full, using evidence independently re-confirmed (not merely assumed) during BA-07's own readiness assessment to be at least as decisive as any prior stage — most notably §40.9's own formal Entry Context declaration, a cleaner textual anchor than the paraphrase-based evidence Review Context's own registration relied on. The alternative — implementing BA-07 (which necessarily requires persisting Validation Context, since BR-C005-006-class exact-revision identification and BR-C005-005's own invalidation rule both presuppose a real, persisted record) without registering the object first — would repeat, unremediated, the exact defect ADR-006/008/009/011 each existed to prevent.

## Consequences

- BA-07's own Business Object registration question is resolved; BA-07 remains subject to its own future implementation-readiness gap analysis — not implemented by this ADR.
- IRA-004 §4, §7, and §10 are updated to reference this ADR and IRA-004 §26; §21/§22/§23/§24/§25 are unamended; no other document changes.
- CMD-001 itself is not amended, consistent with its LOCKED status.
- The Governance Backlog Item already recorded at IRA-004 §21 (whether WP-04-registered objects should eventually be consolidated into CMD-001 §26 itself) applies identically to VLC-000001 and is not re-recorded.
- Resulting Structural Context remains the sole outstanding Structural Context Lifecycle member, requiring its own future registration mirroring this one.
- No implementation, schema, migration, API, or code exists or is authorized as a result of this ADR.

## Status

**Accepted**
