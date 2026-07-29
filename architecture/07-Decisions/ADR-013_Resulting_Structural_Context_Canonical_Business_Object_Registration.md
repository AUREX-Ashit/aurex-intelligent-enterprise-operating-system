# ADR-013 — Resulting Structural Context Registered as a Canonical Business Object (WP-04, C-005)

**Status:** Accepted
**Classification:** Architecture Governance / Business Object Registration
**Decided by:** Repository owner (architecture governance authority), during WP-04's own BA-08 constitutional alignment — the same decision-authority pattern ADR-006/ADR-008/ADR-009/ADR-011/ADR-012 already established, citing `ADR-010` for eligibility rather than re-deriving it.
**Affected Documents:** `architecture/05-Implementation/IRA-004_WP-04_Enterprise_Structure_Management_Implementation_Readiness_Assessment.md` (§27 records the full registration entry this ADR authorizes; §4/§7/§10 updated to reference it) — no other document amended. **ERG-001 is not amended. ADR-006 through ADR-012 are not amended or revisited.**

---

## Context

`ADR-010` recognized the Structural Context Lifecycle — six substantive Context stages declared by PE-001-C005 §38.15/§38.17 and governed jointly by Chapter 43's GS-INV-003 through GS-INV-012 — as a canonical architectural pattern. Five members are already registered (SCI-000001, POC-000001, IMC-000001, RVC-000001, VLC-000001). BA-08's own implementation-readiness assessment independently re-confirmed, without relying on the prior five registrations as precedent alone, that **Resulting Structural Context** — the pattern's sixth and final stage, produced by ERB-C005-08/EX-C005-11 — satisfies both SD-002 §2's Universal Business Object Blueprint and the Cross-Experience Reference Test, on the most literal textual evidence of any of the six stages:

- **§38.15** (C-005 Context Model): named row — "Resulting Structural Context — Structural context produced by successful completion. — Transferred to downstream journeys."
- **§38.17** (Context Transitions): "Validation → completion: Produces Resulting Structural Context and closes proposal context as completed."
- **EX-C005-12 (BA-09's own governing EX)** — a separately-invoked, later Business Activity (listed distinctly from BA-08 in IRA-004 §4, though sharing ERB-C005-08) — Required Context, verbatim: "**Resulting Structural Context** and next enterprise objective." An exact, literal term match — the cleanest cross-Business-Activity anchor of any of the six pattern stages.
- **GS-INV-008** — "Resulting Structural Context SHALL be created only after successful completion of the validated structural transition."
- **GS-INV-012** — "Completion SHALL identify the exact validated proposal revision from which Resulting Structural Context was produced."
- **BR-C005-009** — "Completion SHALL produce Resulting Structural Context," mapped directly to BA-08 (IRA-004 §5).

**Eligibility is not re-derived here in full** — per `ADR-010`'s own Decision point 4, this registration cites that ADR's pattern recognition for the general question, while independently supplying Resulting Structural Context's own CMD-001 §26.4 attributes below.

**A structural difference from its five siblings, disclosed rather than glossed over:** unlike SCI-000001/POC-000001/IMC-000001/RVC-000001/VLC-000001, EX-C005-11's own Invalidated Context text ("Transient proposal/review context closes as completed") describes the *prior* stages' own contexts being closed as a *result* of this stage completing — it does not describe Resulting Structural Context's own state ever being invalidated by a later material revision. Resulting Structural Context represents the terminal, successfully-completed outcome; PE-001-C005's own text gives it no "invalidated by revision" lifecycle transition the way every earlier stage has. This ADR's own registration (§27) reflects that difference rather than mechanically copying the five-sibling pattern.

---

## Decision

1. **Register "Resulting Structural Context" as a canonical Business Object**, identifier `RSC-000001`, per SD-002 §2, CMD-001 §26.3/§26.4, and `ADR-010`'s own pattern recognition. The full registration entry is recorded in **IRA-004 §27**, which this ADR adopts by reference rather than duplicating here.
2. **Correct IRA-004's own BA-08 disposition (§10)** to reflect that Resulting Structural Context is now registered, superseding the prior disposition ("Category C — Requires organization_hierarchy/consolidation_determination," written before the Structural Context Lifecycle pattern was discovered and before Resulting Structural Context was analyzed as its own Business Object).
3. **This ADR does not authorize BA-08's implementation.** CMD-001 §26.7 (Physical Implementation Mapping) remains entirely unset for RSC-000001. BA-08 still requires its own fresh implementation-readiness gap analysis per CLAUDE.md §19.7 before any code, migration, or schema is written.
4. **This ADR does not resolve the ERG-001-mutation-scope question BA-08's own readiness assessment separately disclosed** — whether/how completing a transition actually mutates `organization_nodes` or any future `organization_hierarchy`/`consolidation_determination` table, given no structured change-representation exists anywhere upstream of this stage (every `StructuralProposal` carries only free text). That is BA-08's own future implementation-readiness gap analysis's question, explicitly not decided here — this ADR registers the C-005 experience-layer completion record only, not any ERG-001 domain mutation.
5. **This ADR does not decide whether "Downstream Continuation Context"** (named in §40.9's own Exit Context and EX-C005-12's own Produced Context, distinct from Resulting Structural Context itself) requires its own CBOR registration — that is BA-09's own future eligibility question, not assumed either way by this ADR.
6. **This ADR does not revisit ADR-006 through ADR-012.** SCI-000001's, POC-000001's, IMC-000001's, RVC-000001's, and VLC-000001's own registrations (IRA-004 §21/§22/§23/§25/§26) are unamended; the Structural Context Lifecycle pattern (IRA-004 §24) is unamended.

## Rationale

This decision applies CMD-001 §26.3's own registration mechanism to the sixth and final member of a pattern already recognized in full, using evidence independently re-confirmed (not merely assumed) during BA-08's own readiness assessment to be the most literal of any stage's own case — EX-C005-12's exact-term Required Context reference. The alternative — implementing BA-08 (which necessarily requires persisting Resulting Structural Context, since BR-C005-009 states completion SHALL produce it and GS-INV-012 requires exact traceability to the validated revision) without registering the object first — would repeat, unremediated, the exact defect ADR-006/008/009/011/012 each existed to prevent.

## Consequences

- BA-08's own Business Object registration question is resolved; BA-08 remains subject to its own future implementation-readiness gap analysis — not implemented by this ADR. The separately-disclosed ERG-001-mutation-scope question remains open and is not resolved here.
- IRA-004 §4, §7, and §10 are updated to reference this ADR and IRA-004 §27; §21/§22/§23/§24/§25/§26 are unamended; no other document changes.
- CMD-001 itself is not amended, consistent with its LOCKED status.
- The Governance Backlog Item already recorded at IRA-004 §21 (whether WP-04-registered objects should eventually be consolidated into CMD-001 §26 itself) applies identically to RSC-000001 and is not re-recorded.
- The Structural Context Lifecycle (`ADR-010`) is now fully registered end-to-end: all six stages (SCI-000001 → POC-000001 → IMC-000001 → RVC-000001 → VLC-000001 → RSC-000001) carry a CBOR identifier. No further pattern member remains outstanding.
- No implementation, schema, migration, API, or code exists or is authorized as a result of this ADR.

## Status

**Accepted**
