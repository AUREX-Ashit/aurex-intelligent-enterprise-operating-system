# ADR-015 — Access Evaluation Outcome Registered as a Canonical Business Object (WP-05, C-002)

**Status:** Accepted
**Classification:** Architecture Governance / Business Object Registration
**Decided by:** Repository owner (architecture governance authority), during WP-05's own IRA-005 constitutional analysis — the same decision-authority pattern `ADR-006`/`ADR-008`/`ADR-009`/`ADR-011`/`ADR-012`/`ADR-013` already established for WP-04, applying `CMD-001 §26.3a`'s eligibility test (adopted per `ADR-014`) for the first time to a new capability.
**Affected Documents:** `architecture/05-Implementation/IRA-005_WP-05_Access_Management_Implementation_Readiness_Assessment.md` (§11 records the full registration entry this ADR authorizes) — no other document amended. **CMD-001 is not amended. ADR-006 through ADR-014 are not amended or revisited.**

---

## Context

`IRA-005` performed the first Mandatory Context Discovery pass (`IMP-001 §6.2a`) under the post-WP-04 methodology (`ADR-014`) against `PE-001-C002`'s own §1.16 Context Model, which names six constructs: Governed Request Context, Access Evaluation Outcome, Preserved Access Evaluation Outcome, Superseded Access Evaluation Outcome, Invalidated Access Evaluation Outcome, and Deferred Access Evaluation Outcome. Applying `CMD-001 §26.3a`'s three-step eligibility test to each (`IRA-005` §5):

- **Access Evaluation Outcome** passes all three steps: independent identity (a discrete, identifiable determination for one specific object/event/Identity combination, referenceable after the request that produced it no longer exists); the Cross-Experience Reference Test (consumed as Required/Consumed Context by EX-C002-05/06/07/08 — Enterprise Experiences separately invoked from the one that produces it — and stated by Contract 5.6 to be handed to dependent capabilities' own Enterprise Experiences as an Entry Context precondition); and a governed lifecycle (§1.18/Chapter 6: Created → Preserved → {Superseded | Invalidated | Expired}, explicit and traceable, not a silent state change).
- **Governed Request Context** fails Step 1: §1.16 itself states it "is not a canonical domain state, not an EIO," and it is consumed only within the single ERB that receives it, never retrieved again by a later, separately-invoked Enterprise Experience. Transient, not eligible.
- **Preserved/Superseded/Invalidated/Deferred Access Evaluation Outcome** (four candidates) each fail Step 1: every governing ERB/EX's own Context Created field states plainly that nothing new is produced by these transitions ("Nothing new — this ERB bounds and eventually expires an existing outcome," ERB-C002-02; "Nothing new where the outcome is a refresh," EX-C002-07). Each is a Validity Status label of the single Access Evaluation Outcome object, not a separately-identifiable object of its own.

**This is a materially different eligibility outcome than any single WP-04 registration cycle produced**: six named constructs resolve to exactly one registration, not multiple. `IRA-005` §5.4 discloses this explicitly as a deliberate "merge into one" result of applying the test honestly, not a shortcut taken to avoid registering more.

**Eligibility is not re-derived here** beyond what is stated above — `IRA-005` §5 performs the full step-by-step analysis; this ADR adopts its result rather than duplicating it.

---

## Decision

1. **Register "Access Evaluation Outcome" as a canonical Business Object**, identifier `AEO-000001`, per SD-002 §2, CMD-001 §26.3/§26.3a/§26.4. The full registration entry is recorded in **IRA-005 §11**, which this ADR adopts by reference rather than duplicating here.
2. **Do not register** Governed Request Context (transient) or the four Preserved/Superseded/Invalidated/Deferred constructs (Validity Status of `AEO-000001`, not separate objects) — per `IRA-005` §5's own eligibility analysis, disclosed as a negative finding rather than silently omitted.
3. **This ADR does not authorize any Business Activity's implementation.** CMD-001 §26.7 (Physical Implementation Mapping) remains entirely unset for `AEO-000001`. Every candidate Business Activity (BA-01 through BA-04, `IRA-005` §3) still requires its own fresh implementation-readiness gap analysis per CLAUDE.md §19.7 before any code, migration, or schema is written.
4. **This ADR does not resolve the Authorization Engine governance question** `IRA-005` §9/§10.2 item 3 separately discloses — who, if anyone within this repository's current governance, is authorized to build the URA-001-76 precedence-chain resolver / RTA-001 Authorization Engine that BA-01's Permitted/Denied outcome branches require. That is a distinct, open governance decision, explicitly not decided by this registration. Registering `AEO-000001` does not depend on, and does not presuppose the answer to, that question — the object's own existence, shape, and lifecycle are independent of how (or whether yet) its Outcome Type value is computed.
5. **This ADR does not create a pattern-level ADR** (an `ADR-010` equivalent). `IRA-005` §6 finds C-002's lifecycle to be single-object (one object moving through states), not a WP-04-style multi-object chain — the ordinary CMD-001 §26.4 registration shape, not a pattern requiring separate recognition.

## Rationale

This decision applies CMD-001 §26.3's own registration mechanism, refined by `ADR-014`'s newly adopted §26.3a eligibility test, to the first Business Object candidate discovered under the new methodology — and demonstrates the methodology working as designed: the bounded Context Discovery scan (`IMP-001 §6.2a`) found the governing Context Model section in one upfront pass (during IRA drafting, before any Business Activity began), rather than requiring six separate mid-implementation stop/resume cycles the way WP-04's own discovery did. The eligibility test itself (`CMD-001 §26.3a`) correctly distinguished one genuine Business Object from five look-alikes that do not qualify, preventing both under-registration (missing `AEO-000001`) and over-registration (fabricating four redundant lifecycle-state objects) in the same pass.

Registering `AEO-000001` now, ahead of any implementation and ahead of the separately-disclosed Authorization Engine question being resolved, mirrors `WP-04`'s own precedent directly: `RSC-000001` was registered, and `BA-08` implemented at Option A scope, before its own downstream mechanism (ERG-001 structural mutation) existed anywhere in the repository, with that gap disclosed as `TD-070` rather than blocking registration. The one disclosed difference (`IRA-005` §10.5): because a wrong Access Evaluation Outcome determination is a security defect rather than an incomplete data-mutation record, the unresolved mechanism here is escalated as a Governance Backlog Item requiring an explicit decision (`IRA-005` §10.3), not deferred as ordinary Technical Debt — CLAUDE.md §19.8.5 already prohibits deferring security defects that way. The registration itself is exactly as safe, and exactly as independently justified, as `RSC-000001`'s was.

## Consequences

- WP-05's own Business Object eligibility question is resolved for the six constructs `IRA-005` §4 discovered: one registered (`AEO-000001`), five explicitly not (disclosed, not omitted).
- `IRA-005` §11 records the full registration entry; no other document changes as a result of this ADR.
- CMD-001 itself is not amended, consistent with its LOCKED status; this registration exercises CMD-001 §26.3's own existing mechanism.
- The Authorization Engine ownership question (`IRA-005` §9/§10.2 item 3) remains open and unresolved by this ADR — WP-05's Business Activity implementation, particularly BA-01's Permitted/Denied branches, remains NOT READY until it is separately decided by the repository owner.
- No implementation, schema, migration, API, or code exists or is authorized as a result of this ADR.

## Status

**Accepted**
