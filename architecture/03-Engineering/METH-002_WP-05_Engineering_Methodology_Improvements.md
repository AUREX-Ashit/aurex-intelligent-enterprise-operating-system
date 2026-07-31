# METH-002 — Engineering Methodology Improvements (Post-WP-05 Retrospective)

**Status:** Proposal. Reviewed by `ADR-017` (Adoption of Post-WP-05 Engineering Methodology). This document itself is not edited by that ADR's adoption — it remains the source retrospective, mirroring `METH-001`'s own precedent exactly.
**Classification:** Governance / Methodology Retrospective
**Source Work Package:** WP-05 — Access Management (C-002), minimum scope (`IRA-005 §12`). The first Work Package in this repository to complete a full post-certification correction cycle: an Independent Certification that itself proved incomplete, a deeper audit that found what it missed, remediation, independent re-verification of that remediation, and a final release-readiness gate — five genuinely independent verification passes in sequence, each performed by a fresh-context reviewer with no involvement in the work it was reviewing.
**Reviewed for this retrospective:** `CLAUDE.md` (full, especially §19.7/§19.8), `IMP-001_Implementation_Playbook.md` (§2, §6.3, §6.7), `IRA-005_WP-05_Access_Management_Implementation_Readiness_Assessment.md`, `IMP-REPORT-WP-05_Access_Management.md` (including its Correction section), `CERT-WP-05_Access_Management.md`, `VV-AUDIT-WP-05_Access_Management.md`, `VV-AUDIT-WP-05_Remediation_Verification.md`, `RELEASE-AUDIT-WP-05.md`, `TECH-DEBT.md` (TD-079 through TD-089), and the full WP-05 commit history (`84b095b` through `4f1752c`).

---

## Executive Summary

WP-05 delivered its four authorized Business Activities correctly on the first implementation pass — no Business Activity was reworked, no scope was exceeded, and the one constitutional requirement the Work Package could least afford to get wrong (never fabricating a Permitted/Denied Access Evaluation Outcome) held from the first line of code through every subsequent review. But the Work Package's own **first** Independent Certification (`CERT-WP-05`, PASS WITH OBSERVATIONS) — performed exactly as `CLAUDE.md §19.7` and `ADR-014` already require, by a genuinely independent, fresh-context reviewer who re-ran the tests and traced the code — nonetheless missed **two High-severity, `CLAUDE.md §19.8.5`-class defects**: an orphan foreign-key write (F-01) that would fail with HTTP 500 on the declared production database, and a cross-tenant data leak (F-02) in the Approval Authority lookup. Both were real, both were demonstrated empirically, and neither was a subtle judgment call — they were structurally invisible to the *specific* verification method Certification used (read the code, re-run the existing tests), because the existing test harness and fixtures shared exactly the blind spots the defects depended on.

A second, more rigorous audit (`VV-AUDIT-WP-05`) found both defects — not by reading the code more carefully, but by writing new, purpose-built runtime probes designed to violate the assumptions the code silently depended on (foreign-key enforcement, a second organization). Remediation followed, and — critically — was **not** accepted on the implementing session's own say-so: a third independent reviewer re-verified the fix from scratch, including **negative controls** that proved the verification probes actually detect the original defects (by running them against the pre-fix code and confirming they reproduce both bugs). A fourth independent reviewer then performed a Release Readiness Audit focused specifically on git/governance synchronization, and caught a class of staleness defect (documentation describing a superseded state) that none of the three prior, content-focused reviews had been looking for.

This document proposes **seven methodology improvements**, all directly evidenced by what actually happened during WP-05's own execution — most of them formalizing a verification escalation that worked when improvised under pressure, converting it into a named, repeatable, mandatory sequence.

---

## Methodology Improvements

### 1. Independent Certification Alone Is Not Sufficient — a Multi-Stage Verification Escalation Is Required

**Current process (per `ADR-014`):** A Work Package closes with a single Independent Certification pass, performed by a genuinely independent, fresh-context reviewer who re-verifies claims against actual source, migrations, and test execution. This was correctly performed for WP-05 (`CERT-WP-05`) and returned PASS WITH OBSERVATIONS.

**What actually happened:** That certification missed two High-severity, non-deferrable defects. A second, independently-dispatched reviewer — given a broader mandate (a full 14-phase Verification & Validation audit, including a Requirements Traceability Matrix, exhaustive specification-conformance checking, and purpose-built empirical probes rather than only reading code and re-running existing tests) — found both. Remediation was then verified by a *third* independent reviewer, and the resulting release state was verified by a *fourth*. Each of the four passes caught something the one before it did not: Certification confirmed scope conformance and constitutional correctness but missed the two structural defects; the V&V audit found the two defects plus a self-certification process gap (its own Finding F-06, re: `TD-081`); the Remediation Verification pass confirmed the fix was genuine, not merely claimed, via negative controls; the Release Readiness Audit found a governance-staleness defect (stale "Not committed" fields) none of the first three were positioned to notice, since none of them was specifically checking git-state-versus-documentation consistency as its primary lens.

**Improved process:** Adopt the four-stage sequence WP-05 actually validated as the **standard Work Package closure sequence**, not a discretionary escalation: Independent Certification → Verification & Validation Audit → Remediation (if the V&V audit finds anything) → Independent Verification of Remediation → Release Readiness Audit → Git Push. Each stage is performed by a reviewer independent of every stage before it, per the same `CLAUDE.md §19.7` discipline already governing Certification.

**Rationale:** This is not a theoretical improvement — it is a direct report of what caught two real, otherwise-undetected security/data-integrity defects in a certified Work Package. The four stages are not redundant with each other: each was demonstrated, concretely, to catch a distinct class of problem the others did not.

**Expected benefit:** Materially reduces the chance that a Work Package reaches `CLOSED — CERTIFIED` status while still carrying an undisclosed, non-deferrable defect — the exact failure mode `CLAUDE.md §19.8.5` already prohibits deferring but had no mechanism to reliably detect before WP-05.

**Impact on future Work Packages:** Every future Work Package closure follows the same five-gate sequence (Certification, V&V, Remediation-if-needed, Remediation Verification-if-remediation-occurred, Release Readiness Audit) before a push is authorized.

**Migration guidance:** Formalize as `CLAUDE.md §19.7b` (new subsection, immediately following the existing §19.7 Business Activity Completion Gate and its Independent Certification text) and as `IMP-001 §2.13a` (Work Package Closure & Release Gate Sequence), cross-referencing rather than duplicating the governing rule.

---

### 2. Verification Must Include Empirical, Runtime Probes and Negative Controls — Not Code Reading and Test Re-Execution Alone

**Current process:** Independent Certification's own established method (per `ADR-014`'s own §3 item 2) is to re-verify claims against actual source, migrations, and test execution — i.e., read the code and re-run the existing tests.

**What actually happened:** `CERT-WP-05` did exactly this, correctly, and still missed both defects — because both were invisible to the *existing* test suite by construction (the harness didn't enforce foreign keys; the fixtures never used a second organization). `VV-AUDIT-WP-05` found both only by writing **new, purpose-built runtime probes** specifically designed to exercise a condition the existing suite structurally could not reach. The remediation-verification pass went one step further: it proved its own probes were meaningful, not tautological, by running them against the pre-fix code extracted from `git HEAD` and confirming they **reproduced** both original defects (a negative control) before trusting that their passing against the fixed code meant anything.

**Improved process:** Any verification pass beyond standard Certification (i.e., a V&V Audit or a Remediation Verification) shall include at least one purpose-built, from-scratch probe per defect class under review, and — when re-verifying a remediation specifically — a negative control demonstrating the probe reproduces the original defect against the pre-fix code.

**Rationale:** "Re-run the existing tests" only proves the code satisfies what the existing tests already check. It provides zero evidence about a defect the existing tests were never designed to catch. WP-05 demonstrates this is not a hypothetical gap — it is exactly how two real defects survived a genuine, correctly-performed Independent Certification.

**Expected benefit:** Verification passes stop being a more careful re-reading of the same evidence and start being an independent search for evidence the implementation and its own tests never produced.

**Impact on future Work Packages:** Any V&V Audit or Remediation Verification is expected to write and execute its own test code, not only read and re-run what exists.

**Migration guidance:** Fold into the same `CLAUDE.md §19.7b` addition proposed in Improvement #1, as an explicit method requirement for the V&V and Remediation Verification stages specifically (not required for standard Certification, which retains its existing, lighter-weight method per `ADR-014`).

---

### 3. Test-Harness and Fixture Production-Parity Must Be an Explicit Verification Checklist Item

**Current process:** No document in this repository requires a verifier to check whether the test harness's own behavior (e.g., SQLite's default foreign-key enforcement, which is off) matches the declared production database's behavior (PostgreSQL, which enforces foreign keys unconditionally per `CLAUDE.md §9`), or whether shared test fixtures exercise more than one organization when tenant isolation is a relevant property.

**What actually happened:** Both F-01 and F-02 existed, undetected, for exactly this reason: `tests/conftest.py` uses SQLite with no `PRAGMA foreign_keys=ON` listener, and every WP-05 fixture prior to remediation seeded exactly one organization. Once the V&V audit specifically asked "does the test database enforce what production enforces?" and "does any test exercise a second tenant?", both defects were found immediately.

**Improved process:** Add an explicit checklist to the V&V Audit method (alongside Improvement #2): does the test harness enforce every constraint the declared production database enforces unconditionally (foreign keys, check constraints, uniqueness)? Does at least one test exercise more than one tenant/organization for any capability whose data model includes an `organization_id` or equivalent boundary?

**Rationale:** This is the specific, named root cause both WP-05 defects share. A generic "write more tests" recommendation would not have reliably surfaced either one; this specific pair of questions would have, and did, once finally asked.

**Expected benefit:** Converts a root-cause finding from a one-time discovery into a standing question every future V&V Audit asks by default, rather than needing to be independently rediscovered.

**Impact on future Work Packages:** Any capability with a multi-tenant data boundary, and any capability whose test harness differs materially from its production database, is checked against this specific pair of questions during its own V&V Audit.

**Migration guidance:** Fold into the same `CLAUDE.md §19.7b` addition as Improvements #1 and #2, as a named sub-checklist ("harness parity check").

---

### 4. Any Remediation — However Small — Requires Independent Re-Verification Before a Work Package's Status Is Restored

**Current process:** `ADR-014` (via `METH-001` Improvement #8) already requires a genuinely independent reviewer for Certification. It does not explicitly state whether a *subsequent correction* to an already-certified Work Package requires the same discipline.

**What actually happened:** `TD-081` — a narrow, three-test API-coverage gap, about as small a finding as this repository's Technical Debt register records — was fixed by the implementing session and recorded `Closed` without a second reviewer confirming it. `VV-AUDIT-WP-05` (auditing the *original* certified state, not specifically re-litigating TD-081) flagged this as its own Finding F-06: the fix was, in fact, correct, but the *process* of accepting a self-attested fix without independent re-review was itself the gap, regardless of the fix's own correctness. The much larger F-01/F-02 remediation that followed was deliberately **not** treated the same way — a third independent reviewer was dispatched specifically because of this finding, and specifically because "the fix is obviously correct" is exactly the judgment that TD-081's own history shows should not be trusted from the implementing session alone.

**Improved process:** State explicitly: any remediation of any Independent Review, V&V Audit, or Certification finding — regardless of the finding's own severity — requires independent re-verification before the Work Package's certified status is restored or the finding's Technical Debt entry is closed. "The fix is small" is not an exception.

**Rationale:** WP-05 provides a paired, concrete data point: a small, self-attested fix that turned out to be correct but was still flagged as a process gap, immediately followed by a large fix that was independently verified and passed. The size of the fix did not predict whether independent verification would matter to the process's own integrity — only whether skipping it was noticed.

**Expected benefit:** Removes "this is obviously fine" as an implicit, undocumented exception to the independent-review discipline `CLAUDE.md §19.7` already establishes for original implementation.

**Impact on future Work Packages:** Every remediation, of every size, gets the same independent-verification step Improvement #1's escalation already formalizes.

**Migration guidance:** State explicitly within the same `CLAUDE.md §19.7b` addition: "remediation of any finding, regardless of severity, requires independent verification before the associated status is restored or the Technical Debt entry is closed."

---

### 5. Structural Elimination Is Preferred Over Defensive Suppression When Remediating a Defect

**Current process:** No documented preference exists between (a) narrowing a code path so an invalid state becomes structurally unreachable, and (b) wrapping the existing code path in defensive error handling (`try`/`except`) that catches the resulting failure after it occurs.

**What actually happened:** F-01's own remediation had three candidate shapes (the V&V audit itself enumerated them): narrow `evaluate()`'s scope so an unknown Membership 404s before any write is attempted (mirroring the pre-existing Domain-not-found precedent already in the same method); make the foreign key nullable; or wrap the write in `try`/`except IntegrityError`. The first option was chosen, and the audit's own Remediation Verification pass specifically confirmed the resulting property structurally — "the row-write-under-invalid-FK scenario is structurally unreachable, not merely untested" — rather than merely confirming an exception was now caught.

**Improved process:** When remediating a defect caused by attempting an operation that should never have been attempted for the case in question (as opposed to a defect in the operation's own logic), prefer eliminating the invalid case structurally — especially where an existing precedent for doing so already exists elsewhere in the same file or module — over adding defensive handling around the still-attempted operation.

**Rationale:** This is a direct, concrete evidenced application of the already-adopted Reuse→Configure→Extend→Compose→Create discipline (`CLAUDE.md §19.5`) and the Minimum Constitutional Slice Analysis (`ADR-014 §4` item 5) to defect remediation specifically, not only to new-feature scoping — WP-05 is the first Work Package to demonstrate the technique applied to fixing an already-shipped defect rather than scoping a not-yet-built feature.

**Expected benefit:** Produces fixes that are independently verifiable as structurally correct (as F-01's remediation was), rather than merely "no longer observed to fail" (which a defensive `try`/`except` would have left as the only available claim).

**Impact on future Work Packages:** Applies to any future defect remediation where the root cause is "this operation should never have been attempted here," not only to new-feature scope decisions.

**Migration guidance:** Add as a cross-reference note under `CLAUDE.md §19.5`'s own existing worked example (BA-08's Option A/B/C analysis, added by `ADR-014 §4` item 5) — a second worked example, not a new rule.

---

### 6. Governance Documents Must Be Updated to Final Tense in the Same Pass a Gate Completes

**Current process:** No explicit requirement exists that a governance document's own forward-looking language ("pending," "is being dispatched," "not yet committed") be updated to past/final tense in the same pass that the event it describes actually concludes.

**What actually happened:** Three separate instances of exactly this staleness were found across WP-05's own governance trail: `CERT-WP-05`'s addendum and `IMP-REPORT-WP-05`'s Correction section both retained present/future-tense language ("is being dispatched," "pending") describing the third reviewer's confirmation after that confirmation had already landed; and — most concretely — `WP-REG-001`'s own `Repository Commit` fields continued to read "Not committed" after real commits existed, caught only by the fourth reviewer's Release Readiness Audit (its own Observation O-1). None of these were substantive errors — the authoritative status fields elsewhere in the same documents were correct — but each required a dedicated follow-up correction pass to fix.

**Improved process:** When a governance document is updated to record a gate's completion, the same editing pass shall also correct any forward-looking language elsewhere in the same document (or in a document it supersedes/addends) describing that gate as pending, in progress, or not yet performed.

**Rationale:** This is a narrow, low-severity, but repeatedly-observed pattern — three independent instances within one Work Package's own closure sequence — worth naming so it is checked for deliberately rather than rediscovered by whichever reviewer happens to read the stale sentence next.

**Expected benefit:** Reduces the number of small, dedicated cleanup passes required after a gate completes.

**Impact on future Work Packages:** A one-line addition to whatever checklist accompanies updating `WP-REG-001`/`WPR-001`/`IMP-REPORT-WP-XX`/`CERT-WP-XX` at each lifecycle transition.

**Migration guidance:** Add a one-line note to `WP-REG-001 §3`'s own "SHALL be updated whenever" list: "and any forward-looking language elsewhere describing the same transition is corrected to final tense in the same pass."

---

### 7. A Dispatched Independent-Reviewer Subagent Interrupted by a Transient Error Should Be Resumed, Not Restarted

**Current process:** No documented guidance exists for what to do when a dispatched independent-review subagent is interrupted mid-task by an infrastructure or connection error (as opposed to the subagent itself reaching a substantive conclusion).

**What actually happened:** The Remediation Verification reviewer was interrupted twice by transient connection/stall errors, each time after having already produced real, evidenced partial progress (e.g., "All 24 independent checks pass. Now a negative control…" at the point of the second interruption). Resuming the same agent from its own transcript (rather than dispatching a fresh agent from scratch) preserved that progress without duplicating work or risking a second agent re-deriving — and potentially inconsistently re-deriving — evidence the first had already gathered correctly.

**Rationale:** This is distinct from, and complementary to, the already-adopted (informative) Business Activity Resume Protocol (`METH-001` Improvement #6), which addresses an *implementing session's own* interruption. This is the same underlying discipline — verify what already happened before deciding how to proceed, never discard verified partial progress — applied to a *dispatched reviewer subagent's* interruption specifically.

**Expected benefit:** Avoids wasted verification effort and avoids the risk of two independently-dispatched passes producing subtly different findings about the same evidence due to non-determinism, when one already-in-progress pass could simply continue.

**Impact on future Work Packages:** Applies to any future dispatched Independent Review, V&V Audit, Remediation Verification, or Release Readiness Audit subagent that stalls or errors before producing its final determination.

**Migration guidance:** Add as an informative (not normative — mirroring `METH-001` Improvement #6's own classification) operational note near wherever `CLAUDE.md §19.7b` documents the dispatch procedure for independent reviewers.

---

## Additional Findings (confirmatory, not new proposals)

- **Minimum-scope authorization worked exactly as designed, with no gap found.** `IRA-005 §12`'s deliberate narrowing of BA-01 to its Unresolved/Deferred branches only (Permitted/Denied explicitly excluded pending a real `WP-RTA-001` `TierResolver`) held through every one of the five verification passes — no reviewer at any stage found a code path that could produce a fabricated Permitted/Denied outcome. This confirms, rather than newly proposes, the already-adopted Reuse→Configure→Extend→Compose→Create discipline and `ADR-014`'s own Minimum Constitutional Slice Analysis; no change is proposed here.
- **HTTP 501 is a reusable, exemplary pattern for an explicitly-out-of-scope request, worth naming.** BA-01's decline path (a request that would require a Permitted/Denied determination) returns HTTP 501 with a detail citing the specific authorizing document and section, rather than fabricating a decision (which `CLAUDE.md §19.8.5` prohibits) or silently declining (which would be unexplained to the caller). Two independent reviewers (`VV-AUDIT-WP-05` and `RELEASE-AUDIT-WP-05`) separately commended this as correct and well-justified. Worth citing as a reference pattern the next time a Business Activity must decline a request that is outside its own currently-authorized scope, without inventing a new response-shape convention each time.

---

## Priority

| # | Improvement | Priority |
|---|---|---|
| 1 | Multi-stage independent verification escalation (Certification → V&V → Remediation → Remediation Verification → Release Readiness Audit) | **High** — directly caught two High-severity, non-deferrable defects a correctly-performed Certification alone missed. |
| 2 | Empirical probes + negative controls as the required V&V/Remediation-Verification method | **High** — this is *how* Improvement #1 actually works; without it, additional review stages would likely repeat Certification's own blind spot. |
| 3 | Test-harness/fixture production-parity checklist | **High** — the specific, named root cause of both defects; converts a one-time discovery into a standing check. |
| 4 | Mandatory independent re-verification of any remediation, regardless of size | Medium — closes a real, evidenced process gap (`TD-081`'s own history), tightening a rule (`METH-001` #8) that already existed in principle. |
| 5 | Structural elimination preferred over defensive suppression for defect remediation | Medium — a specific, evidenced technique refinement with narrower applicability than #1–3. |
| 6 | Governance documents updated to final tense in the same pass a gate completes | Low — real and repeatedly observed, but cosmetic/non-blocking in every instance found. |
| 7 | Resume, not restart, an interrupted independent-reviewer subagent | Low — an operational/session-management practice; no correctness risk was ever observed to materialize from it. |

---

## Recommended Document Updates (not performed automatically — proposal only)

- `CLAUDE.md` — new §19.7b (Improvements #1–#4), immediately following the existing §19.7 Business Activity Completion Gate / Independent Certification text.
- `IMP-001_Implementation_Playbook.md` — new §2.13a, Work Package Closure & Release Gate Sequence (Improvement #1's lifecycle diagram, cross-referencing `CLAUDE.md §19.7b` rather than duplicating its governing text); a new Appendix B, a short reference pointer naming WP-05 as the canonical reference implementation and directing readers to this document for the retrospective evidence — not a second copy of it.
- `CLAUDE.md §19.5` — a second worked example cross-referenced alongside the existing BA-08 example (Improvement #5).
- `WP-REG-001_Enterprise_Work_Package_Register.md §3` — one-line addition to the "SHALL be updated whenever" list (Improvement #6).
- `DOC-000_Documentation_Catalogue.md` — index this document and its governing ADR.

---

## Expected Impact

If adopted before the next Work Package begins: every future Work Package closes through the same five-gate sequence WP-05 validated, with each gate performed by a reviewer independent of every gate before it, using empirical probes and (where remediation occurred) negative controls rather than code review and test re-execution alone. The remaining improvements (remediation-verification discipline regardless of finding size, structural-elimination preference, documentation-tense discipline, reviewer-subagent resume practice) compound in value as more Work Packages accumulate, without changing how any single Business Activity is implemented.

---

*End of METH-002. This document is a proposal. No governing document has been modified. No repository file listed under "Recommended Document Updates" has been changed as a result of producing this retrospective.*
