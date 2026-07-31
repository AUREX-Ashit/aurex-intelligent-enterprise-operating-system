# ADR-017 — Adoption of Post-WP-05 Engineering Methodology

**Status:** Accepted
**Classification:** Architecture Governance / Methodology Adoption
**Decided by:** Repository owner (architecture governance authority), following the same decision-authority pattern `ADR-014` already established — this time authorizing a methodology change surfaced by WP-05's own certification-correction cycle rather than by iterative Canonical Business Object discovery.
**Affected Documents:** **None edited by this ADR.** This ADR is the governance authorization that permits `CLAUDE.md` and `IMP-001` to be edited in this same coordinated implementation pass, per its own §7 Implementation Roadmap below. Consistent with `ADR-014`'s own precedent, the actual edits are performed as a distinct, disclosed follow-on action, not folded silently into this decision record.

---

## 1. Context

WP-05 (Access Management, C-002) is the first Work Package in this repository to complete a full post-certification correction cycle. Its own Independent Certification (`CERT-WP-05`), performed exactly as `CLAUDE.md §19.7` and `ADR-014` already require — by a genuinely independent, fresh-context reviewer who re-verified claims against actual source and re-ran the test suite — returned PASS WITH OBSERVATIONS. A second, more rigorous audit (`VV-AUDIT-WP-05`), dispatched independently of that certification, subsequently found two High-severity defects the certification had missed, both falling inside `CLAUDE.md §19.8.5`'s own list of categories Technical Debt SHALL NOT be used to defer. Both were remediated, the remediation was independently re-verified by a third reviewer (`VV-AUDIT-WP-05_Remediation_Verification.md`, CONFIRMED WITH OBSERVATIONS), and the resulting release state was independently audited by a fourth reviewer (`RELEASE-AUDIT-WP-05.md`, APPROVED FOR PUSH) before this ADR was drafted.

`METH-002` (`architecture/03-Engineering/METH-002_WP-05_Engineering_Methodology_Improvements.md`) documents this finding and six further, related findings in full, each directly evidenced by WP-05's own execution — no theoretical or speculative improvement is proposed. This ADR evaluates each against the same criteria `ADR-014` used (risk of introducing unnecessary process, duplicating an existing rule, reducing implementation velocity, or conflicting with constitutional governance) and renders a decision for each: Accept, Accept with Modification, Reject/Merge, or Defer.

**Why this decision is made now, before WP-06:** METH-002's own central finding — that Independent Certification alone did not catch two real, non-deferrable defects in a Work Package that was, by every other measure, correctly and carefully implemented — has immediate, unconditional relevance to every future Work Package's own closure, not only to capabilities resembling C-002. Deferring adoption until after a second Work Package independently rediscovers the same gap would mean knowingly re-accepting a demonstrated risk for no benefit.

---

## 2. Decision

**This ADR adopts the METH-002 findings as follows, item by item, with no further re-litigation of the reasoning already documented there.** This ADR does not itself edit `CLAUDE.md` or `IMP-001`; it authorizes the coordinated implementation pass enumerated in §7 below, in the sequence stated there, and no other edits beyond them.

---

## 3. Approved Improvements

Accepted, as proposed, without modification:

1. **CLAUDE.md §19.7b — Multi-Stage Independent Verification Escalation**, formalizing the five-gate Work Package closure sequence WP-05 validated: Independent Certification → Verification & Validation Audit → Remediation (if the V&V audit finds anything) → Independent Verification of Remediation → Release Readiness Audit → Git Push, each performed by a reviewer independent of every stage before it. *(METH-002 item #1.)*
2. **CLAUDE.md §19.7b — Empirical probe and negative-control method requirement**, stating that any verification pass beyond standard Certification (a V&V Audit or a Remediation Verification) must include purpose-built runtime probes per defect class under review, and, when re-verifying a remediation specifically, a negative control demonstrating the probe reproduces the original defect against the pre-fix code. *(METH-002 item #2.)*
3. **CLAUDE.md §19.7b — Test-harness/fixture production-parity checklist**, requiring a V&V Audit to explicitly check whether the test harness enforces every constraint the declared production database enforces unconditionally, and whether at least one test exercises more than one tenant for any capability with a tenant boundary. *(METH-002 item #3.)*
4. **CLAUDE.md §19.7b — Mandatory independent re-verification of any remediation, regardless of finding size.** Explicitly removes "the fix is obviously small/correct" as an implicit exception to the independent-verification discipline already required for original implementation. *(METH-002 item #4.)*
5. **CLAUDE.md §19.5 — second worked example**, cross-referencing F-01's own remediation (structural elimination of an invalid case, matching an existing precedent already in the same file, preferred over defensive `try`/`except` suppression) alongside the existing BA-08 worked example `ADR-014 §4` item 5 already added. *(METH-002 item #5.)*
6. **WP-REG-001 §3 — one-line addition** to the "SHALL be updated whenever" list, requiring forward-looking language elsewhere in the same or an addended document to be corrected to final tense in the same pass a gate completes. *(METH-002 item #6.)*
7. **IMP-001 §2.13a — Work Package Closure & Release Gate Sequence**, a new subsection presenting Improvement #1's own validated lifecycle diagram at the engineering-methodology level, cross-referencing `CLAUDE.md §19.7b` for the governing rule rather than duplicating it — consistent with `IMP-001 §1.4`'s own stated boundary ("It does not have authority to alter [constitutional/governance documents]; it translates their principles into engineering practice").
8. **IMP-001 — new Appendix B, "WP-05 Reference Pointer"**, naming WP-05 as the canonical reference implementation of the validated closure sequence (mirroring Appendix A's own existing role, for the closure process specifically) and pointing to `METH-002` as the sole source for the retrospective evidence, execution statistics, defects, and findings — deliberately **not** restating that content a second time, per this repository's own single-authoritative-source discipline. (Revised from an earlier draft of this ADR, which proposed a full summarizing appendix; corrected before adoption to avoid duplicating `METH-002`.)

---

## 4. Modified Improvements

**None.** Unlike `ADR-014`, no item required modification from its originally-proposed form — every improvement in `METH-002` was already scoped conservatively (evidence-first, no speculative generalization) at proposal time, per the drafting instruction that produced it.

---

## 5. Deferred Items

**None.** Every item in `METH-002` is adopted (§3) or classified informative rather than normative at the point of adoption itself (§6, Improvement #7) — no item is set aside pending further data, unlike `ADR-014`'s own deferred large-IRA-splitting item.

---

## 6. Rejected / Merged Items

**No item was rejected.** One item is adopted in **informative**, not normative, form — mirroring `ADR-014 §4` item 3's own treatment of the Business Activity Resume Protocol:

- **Reviewer-subagent interruption resume practice (`METH-002` item #7)** — adopted as an informative operational note (documents an already-proven practice; its absence would not by itself produce an incorrect verification outcome, only wasted effort), not as a mandatory gate. Placed as a note near the `CLAUDE.md §19.7b` dispatch procedure, mirroring exactly where `ADR-014` placed the analogous Business Activity Resume Protocol relative to `IMP-001 §6.3`.

---

## 7. Implementation Roadmap

The coordinated implementation pass this ADR authorizes shall proceed in the following order:

**1. `CLAUDE.md`** — Add new §19.7b (Multi-Stage Independent Verification Escalation), immediately following the existing §19.7 Business Activity Completion Gate / Independent Certification text: the five-gate sequence (§3 item 1), the empirical-probe/negative-control method requirement (§3 item 2), the harness-parity checklist (§3 item 3), the no-size-exception remediation-verification rule (§3 item 4), and the informative reviewer-subagent resume note (§6). Also add the second worked example to §19.5 (§3 item 5). Sequenced first because §7 item 2's own `IMP-001 §2.13a` addition is defined as a cross-reference to this text, not a duplicate of it — nothing downstream can correctly cross-reference a rule that does not yet exist in canonical form.

**2. `IMP-001`** — In one coordinated pass: (a) new §2.13a, Work Package Closure & Release Gate Sequence, presenting the same five-gate diagram at the engineering-methodology level and cross-referencing `CLAUDE.md §19.7b` (§3 item 7); (b) a new Appendix B, "WP-05 Reference Pointer" (§3 item 8). Sequenced second because (a) depends on `CLAUDE.md §19.7b` already existing.

**3. `WP-REG-001`** — Add the one-line addition to §3's own "SHALL be updated whenever" list (§3 item 6). Does not depend on either prior step; sequenced third only to keep the roadmap's own three-step shape simple.

**This ADR does not perform any of the three steps above.** Each is performed as its own distinct, disclosed edit in this same session's implementation pass, mirroring `ADR-014`'s own precedent of separating authorization from execution even when both occur close together in time.

---

## 8. Consequences

- Every future Work Package closure follows the same five-gate sequence WP-05 validated: Independent Certification, Verification & Validation Audit, Remediation (if needed), Independent Verification of Remediation (if remediation occurred), Release Readiness Audit, then Git Push — closing a gap `ADR-014`'s own single-stage Certification requirement left open in practice, even though it was correctly implemented.
- Every future V&V Audit and Remediation Verification is required, not merely encouraged, to use empirical probes and (for remediation specifically) negative controls, rather than relying on code review and existing-test re-execution alone.
- Every future remediation of any finding, regardless of severity, requires independent re-verification before the associated status is restored — closing the specific process gap `VV-AUDIT-WP-05`'s own Finding F-06 identified in `TD-081`'s history.
- No existing registration, certification, or Work Package status is affected. `CERT-WP-01` through `CERT-WP-04`, and WP-05's own now-restored `CLOSED — CERTIFIED` status, are not re-opened or re-audited by this ADR.
- `CLAUDE.md §19.7`'s own existing text is not altered — §19.7b is purely additive, exercising the same "operationalize a lesson without amending existing locked or already-adopted text" discipline `ADR-014` already used.
- `IMP-001`'s own Section 2 (Canonical Implementation Lifecycle) numbering is not altered — §2.13a is inserted as a lettered subsection, the same non-renumbering convention `ADR-014` already established for `CMD-001 §26.3a` and `IMP-001 §6.7a`.

## Status

**Accepted**
