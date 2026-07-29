# ADR-014 — Adoption of Post-WP-04 Engineering Methodology

**Status:** Accepted
**Classification:** Architecture Governance / Methodology Adoption
**Decided by:** Repository owner (architecture governance authority), following the same decision-authority pattern ADR-006 through ADR-013 already established — this time authorizing a methodology change rather than a single Work Package's own implementation or registration decision.
**Affected Documents:** **None edited by this ADR.** This ADR is the governance authorization that permits `CMD-001`, `IMP-001`, `CLAUDE.md`, and a new `architecture/00-Governance/CBOR-INDEX.md` to be edited in a future, separately-scoped implementation pass. No governing document's text changes as a result of this ADR.

---

## 1. Context

WP-04 (Enterprise Structure Management, C-005) is the first Work Package in this repository to require *iterative* Canonical Business Object discovery: six registrations (`ADR-006`, `ADR-008`, `ADR-009`, `ADR-011`, `ADR-012`, `ADR-013`) plus a pattern-recognition decision (`ADR-010`), each surfaced independently, one at a time, during six separate Business Activities' own readiness assessments. Every one of the six registrations was correct — `CERT-WP-04`'s own independent verification (a fresh-context subagent re-deriving every material claim against actual source, not trusting documentation) confirmed no Business Object was invented and none was missed, and the eligibility test used (SD-002 §2's Blueprint plus a Cross-Experience Reference Test) never produced a wrong answer across all eight applications, positive and negative.

What was not correct was the *process shape*: PE-001-C005 §38.15, a section explicitly titled "C-005 Context Model," already declared all six stages in one place, but no Business Activity's own readiness assessment consulted it until the sixth Business Activity's own turn. This produced six separate "discover mid-implementation → STOP → register → resume" cycles where one upfront registration pass, performed at Work Package chartering, would have sufficed. `METH-001` (`architecture/03-Engineering/METH-001_Engineering_Methodology_Improvements.md`) documents this finding and nine further, related findings in full; a subsequent Governance Review evaluated each against the risk of introducing unnecessary process, duplicating an existing rule, reducing implementation velocity, or conflicting with constitutional governance, and rendered a decision — Accept, Accept with Modification, Reject/Merge, or Defer — for each.

**Why governance changes are required before WP-05 begins:** METH-001's own single highest-leverage finding (mandatory upfront Context Discovery) only produces its full benefit if the *next* Work Package's own IRA is drafted under the new procedure from the start. Retrofitting the rule onto an IRA already drafted the old way recovers none of the benefit. WP-05's own chartering is therefore the correct, and last practical, point at which to adopt this methodology before its central benefit is lost to timing.

---

## 2. Decision

**This ADR adopts the METH-001 Governance Review's decisions exactly, with no further re-litigation.** Every determination in that review — Accept, Accept with Modification, Reject/Merge, Defer — is adopted as stated, without this ADR re-opening or re-deriving any of them. This ADR does not itself edit `CMD-001`, `IMP-001`, `CLAUDE.md`, or `SD-002`; it authorizes a future, separately-scoped implementation pass to make exactly the edits enumerated in §7 below, in the sequence stated there, and no other edits beyond them.

---

## 3. Approved Improvements

Accepted, as proposed, without modification:

1. **CMD-001 §26.3a — Named Business Object eligibility test**, combining SD-002 §2's Universal Business Object Blueprint with the Cross-Experience Reference Test as a citable, three-step procedure, plus a "Negative Indicators" subsection (the transient-context checklist). *(METH-001 items #2 and #5, merged into one CMD-001 addition.)*
2. **CLAUDE.md §19.7 clarification — mandatory fresh-context reviewer for Independent Certification.** Certification must dispatch a genuinely independent reviewer (subagent or separate party) to re-verify claims against actual source, migrations, and test execution; synthesis from the implementing session's own memory does not satisfy "independent." *(METH-001 item #8.)*
3. **CLAUDE.md §19.8 — Technical Debt severity rubric** (High/Medium/Low criteria, tied to whether a gap defeats the capability's own CAP-001 Business Intent or weakens a security/tenant-isolation boundary, versus an internal completeness gap). *(METH-001 item #10.)*
4. **IMP-001 §5 — Canonical Business Object implementation-name-vs-CBOR-name disclosure convention**, formalizing the already-proven, six-for-six-applied practice of an implementation class carrying a different, code-idiomatic name from its registered canonical name, always cross-referenced in the model's own docstring.
5. **IMP-001 §6.7 — new required Business Activity Contract field**: guarded-vs-idempotent transition disclosure, for any write endpoint callable twice against the same target.

---

## 4. Modified Improvements

Accepted, with the stated modification — the modification itself is adopted, not the original wording:

1. **Mandatory Context Discovery at IRA-drafting time (IMP-001)** — adopted in **bounded form**: a structured table-of-contents / section-header scan for any chapter analogous to PE-001-C005 §38 (a named, cross-cutting Context/Object/Data Model declaration), not an open-ended full-text re-read of the governing specification. A capability's own ERB analysis noting a generic-journey shape (rather than independent lifecycle verbs) is adopted as a **secondary trigger** for the same scan, folded into this one procedure rather than standing as its own separate rule. *(METH-001 items #1 and #4, merged.)*
2. **Constitutional-vs-Implementation-blocker distinction (IMP-001)** — adopted **together with** canonicalizing the Gap Analysis A–E category scheme itself into IMP-001, since that scheme has been copy-pasted by convention across IRA-001 through IRA-004 without ever being defined once in a canonical document. The new distinction is adopted as a clarifying layer on top of a now-canonicalized foundation, not as a standalone addition to an undefined scheme. *(METH-001 item #3, modified.)*
3. **Business Activity Resume Protocol (IMP-001)** — adopted, but classified **informative, not normative**: documents an already-proven practice; its absence would not by itself produce an incorrect outcome, so it does not become a mandatory gate. *(METH-001 item #6, modified.)*
4. **Central CBOR index** — adopted, but **relocated** from the originally-proposed `architecture/02-Constitutional/` to **`architecture/00-Governance/CBOR-INDEX.md`**. `02-Constitutional/` houses LOCKED, rarely-amended constitutional text (`CMD-001`, `SD-002`, `ERG-001`); a living, frequently-updated cross-Work-Package index is structurally the same class of artifact as `WPR-001` (which already lives in `00-Governance/`), not a constitutional document, and placing it among LOCKED documents would misrepresent its own amendment status. *(METH-001 item #9, modified.)*
5. **"Minimum Constitutional Slice Analysis" (CLAUDE.md §19.5)** — adopted as a **worked example added to the existing §19.5 text** (illustrating BA-08's own Option A/B/C decision), not as a newly-named, standalone technique. The underlying discipline is already CLAUDE.md §19.5's own Reuse→Configure→Extend→Compose→Create rule; naming a second, parallel term for the same rule was assessed as a duplication risk, not a genuine addition.

---

## 5. Deferred Items

**Split large, multi-registration IRAs into a companion document — DEFERRED.** METH-001's own text rates this "a scaling concern, not yet a live problem," citing exactly one data point (`IRA-004` itself), which — despite growing to 27 sections — produced no identified defect, delay, or navigation failure. Standardizing a document-splitting convention now, before a second real multi-registration Work Package exists to validate the proposed shape against, risks prescribing a structure that does not fit whatever that next case actually needs. **This item is not rejected — it remains open for reconsideration once a second Work Package's own Context Discovery (per §4.1 above) surfaces more than two or three Business Objects at once.**

---

## 6. Rejected / Merged Items

**No item was rejected outright without replacement.** One item was merged into another rather than retained as a standalone rule:

- **Mandatory Context Lifecycle analysis trigger (originally METH-001 item #4)** — merged into the Context Discovery procedure (§4 item 1, above) as a secondary trigger condition, not retained as its own separately-numbered rule. Rationale: both items trigger the identical downstream action (a full Context/Object Model scan) from two different signals (document structure vs. ERB-content inference); keeping them as two separately-numbered rules risked the two drifting out of sync with each other as one was edited and the other was not, with no corresponding benefit from the separation.

---

## 7. Implementation Roadmap

The future, separately-scoped implementation pass this ADR authorizes shall proceed in the following order:

**1. CMD-001** — Add new §26.3a (the named eligibility test + negative-indicator checklist, §3 item 1 above). This is sequenced first because §4 item 1's own Context Discovery mandate and the CBOR-INDEX's own entry format both reference this test; nothing downstream can correctly cite a procedure that does not yet exist in canonical form.

**2. IMP-001** — In one coordinated pass: (a) the bounded, TOC-scoped Context Discovery mandate with its ERB-journey secondary trigger (§4 item 1); (b) canonicalization of the Gap Analysis A–E scheme plus the Constitutional-vs-Implementation-blocker distinction (§4 item 2); (c) the implementation-name-vs-CBOR-name disclosure convention at §5 (§3 item 4); (d) the new guarded-vs-idempotent Business Activity Contract field at §6.7 (§3 item 5); (e) the informative Business Activity Resume Protocol note near §6.3 (§4 item 3). Sequenced second because (a) depends on CMD-001 §26.3a already existing.

**3. CLAUDE.md** — In one coordinated pass: (a) the §19.7 clarification mandating a fresh-context reviewer for Independent Certification (§3 item 2); (b) the §19.8 Technical Debt severity rubric (§3 item 3); (c) the §19.5 worked-example addition (§4 item 5). None of these three depends on CMD-001 or IMP-001 having already changed; they are sequenced third only to keep the roadmap's own four-step shape simple, not because of a technical dependency.

**4. `architecture/00-Governance/CBOR-INDEX.md`** — Create the new index and backfill it with WP-04's own six registered Business Objects (`SCI-000001` through `RSC-000001`), plus a confirmation pass on whether WP-01/02/03 registered anything under the (now-canonicalized) CMD-001 §26.3a test — genuinely unresolved by this ADR and by METH-001 alike, since neither PE-001-C004 nor PE-001-C007 was reviewed for an equivalent Context Model section. Sequenced last because its own entry format should mirror the now-finalized CMD-001 §26.3a test, and because it is the one net-new document among the four, lowest-risk to sequence after the three edits to existing governing documents are settled.

**This ADR does not perform any of the four steps above.** Each remains its own future, separately-scoped implementation task.

---

## 8. Consequences

- WP-05's own IRA, if drafted after this ADR's own four-step roadmap is executed, benefits from the single highest-leverage finding of this retrospective: any capability whose governing specification contains a §38.15-equivalent Context Model section has that model fully discovered and eligibility-tested in one pass, before any Business Activity begins, rather than piecemeal across the Work Package's own lifetime.
- Every future `CERT-WP-XX` is required, not merely encouraged, to use a genuinely independent, fresh-context reviewer — closing a previously-latent self-certification risk CLAUDE.md §19.7 already prohibited in principle but never operationalized.
- Every future Technical Debt entry can be assigned a severity against a stated rubric rather than an ad hoc judgment call.
- No existing registration, certification, or Work Package status is affected. `SCI-000001` through `RSC-000001`'s own registrations remain valid as-is; `CERT-WP-01` through `CERT-WP-04` are not re-opened or re-audited by this ADR.
- `CMD-001` remains LOCKED in substance — §26.3a is additive, exercising the same "operationalize an existing rule without amending its core text" discipline `ADR-006` through `ADR-013` already used for CBOR registration itself, not a precedent for reopening CMD-001's own locked content more broadly.
- The one deferred item (splitting large IRAs) remains genuinely open, not silently dropped — it is expected to be revisited the first time a future Work Package's own Context Discovery pass surfaces enough Business Objects at once to make the question live again.

## Status

**Accepted**
