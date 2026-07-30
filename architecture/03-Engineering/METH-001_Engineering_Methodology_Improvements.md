# METH-001 — Engineering Methodology Improvements (Post-WP-04 Retrospective)

**Status:** Adopted per `ADR-014` (Adoption of Post-WP-04 Engineering Methodology, Accepted). ADR-014 adopted this document's Governance Review decisions exactly (Accept / Accept with Modification / Reject-Merge / Defer per item), without re-litigation. The governing-document edits ADR-014 §7 enumerates (`CMD-001`, `IMP-001`, `CLAUDE.md`, `CBOR-INDEX.md`) were carried out by `WP-METH-001` (commit `1d7416b`). This document itself remains the source retrospective and is not further modified by that adoption.
**Classification:** Governance / Methodology Retrospective
**Source Work Package:** WP-04 — Enterprise Structure Management (C-005), the first Work Package in this repository to require *iterative* Canonical Business Object discovery (six registrations, `ADR-006`/`008`/`009`/`011`/`012`/`013`, plus a pattern-recognition ADR, `ADR-010`) rather than the single-registration pattern WP-01/02/03 never needed.
**Reviewed for this retrospective:** `CLAUDE.md` (full), `IMP-001_Implementation_Playbook.md` (§3.9, §6, §7), `CMD-001_Canonical_Data_Model.md` (§26.3–§26.8), `SD-002_Universal_Business_Object_Rules.md` (§2), `IRA-004` (all 27 sections), `ADR-006` through `ADR-013`, `IMP-REPORT-WP-04`, `CERT-WP-04`, `TECH-DEBT.md` (TD-032, TD-043–070), and the full WP-04 commit history (`f4f0292` through `3cad7db`).

---

## Executive Summary

WP-04 delivered nine Business Activities correctly, but it did so through six separate "discover a Business Object mid-implementation → STOP → register → resume" cycles (BA-03 through BA-08 each independently surfaced an unregistered Canonical Business Object during its own readiness assessment), when a single upfront reading of PE-001-C005 §38.15 — a section explicitly titled "C-005 Context Model," never consulted until BA-06's own turn — would have surfaced all six at once. This is the central, avoidable inefficiency this retrospective identifies. Everything else worked: the SD-002 §2 eligibility test, correctly applied ad hoc, never produced a wrong answer (it correctly said "no" twice — Comparison Context, Downstream Continuation Context — and "yes" six times); the STOP-and-resume discipline never lost state; Independent Review at the Business-Activity level caught two real defects a Work-Package-level review alone would have missed; and Independent Certification via a fresh-context subagent proved the practical way to satisfy CLAUDE.md §19.7's self-certification prohibition without a separate human reviewer.

This document proposes **ten methodology improvements**, most of which formalize a practice that already worked when applied ad hoc, converting it from "something this session figured out under pressure" into "a named, repeatable step every future Work Package starts with."

---

## Methodology Improvements

### 1. Mandatory Context Discovery at Work Package Chartering

**Current process:** A Work Package's IRA (Implementation Readiness Assessment) is drafted by reading the governing capability specification's per-ERB and per-EX chapters (PE-001-Cxxx Chapters 40–41, in the C-005 case) to derive a candidate Business Activity list. Any cross-cutting "Context Model" or "Object Model" section elsewhere in the specification (PE-001-C005 §38.15/§38.17, in this case) is not guaranteed to be read at all — it was not read for WP-04 until BA-06's own turn, five Business Activities and three registrations after WP-04 began.

**Improved process:** Before an IRA is considered draftable, the drafting pass MUST explicitly search the full governing capability specification (every chapter, not only the ERB/EX chapters) for any section that declares a cross-cutting Context Model, Object Model, Data Model, or equivalent named construct-inventory. If one exists, it becomes a mandatory input to the IRA's own Required Business Objects section, read in full, before any Business Activity is scoped.

**Rationale:** PE-001-C005 §38.15 already stated, in one place, everything that took five separate mid-implementation discoveries to surface. The capability specification's own author had already done the discovery work; this repository's own reading discipline simply didn't look in the right chapter until forced to by repeated friction.

**Expected benefit:** Collapses what was six separate STOP/register/resume cycles into one upfront registration pass at Work Package chartering, before BA-01 implementation even begins.

**Impact on future Work Packages:** Any future capability specification with an equivalent "§X.Y Context Model" or "Data Model" section (check every PE-001-Cxxx document for one, not just C-005's) gets its full Business Object inventory registered once, at IRA-drafting time, not discovered piecemeal across the Work Package's own lifetime.

**Migration guidance:** Add an explicit checklist item to IMP-001 §6 (or wherever the IRA drafting procedure is documented): *"Before drafting §4 (Business Activities), search the full governing specification for any cross-cutting Context/Object Model declaration. If found, apply Improvement #2 (below) to every row of it before proceeding."* No retroactive action needed for WP-01/02/03 (neither PE-001-C004 nor PE-001-C007 was checked for an equivalent section during this retrospective — that is itself a gap this improvement would close going forward, not a retroactive claim that one exists).

---

### 2. A Named, Repeatable Canonical Business Object Eligibility Test

**Current process:** SD-002 §2's Universal Business Object Blueprint and a "Cross-Experience Reference Test" (a concept is a Business Object if a separately-invoked, later Business Activity/Enterprise Experience names it as Required/Consumed Context) were applied six times this Work Package, each time re-explained from scratch in the relevant ADR's own Context section. The test itself is sound (six-for-six correct positive results, two-for-two correct negative results) but exists nowhere as a named, citable procedure — only as prose repeated with variation across `ADR-006`/`008`/`009`/`011`/`012`/`013`.

**Improved process:** Formalize the test as a named, numbered procedure — e.g., **"CMD-001 §26.3a — Business Object Eligibility Test"** — with explicit steps: (1) does the construct have independent identity separable from the request that produced it (SD-002-004)? (2) is it named, by content or exact term, as Required/Consumed Context by a Business Activity other than the one producing it? (3) does its own governing text describe a real lifecycle (a state that persists and is later invalidated by a subsequent event), or does it explicitly self-describe as transient? Steps 2–3 are exactly what this Work Package already did ad hoc.

**Rationale:** A named, structured test is faster to apply, easier to audit, and harder to apply inconsistently than re-deriving the same reasoning in prose each time. It also makes the negative cases (Comparison Context, Downstream Continuation Context) easier to defend, since "does its own text call itself transient" becomes an explicit checklist item rather than a judgment call each time.

**Expected benefit:** Reduces the eligibility analysis for a new candidate object from a multi-paragraph derivation to a three-question checklist, directly citable in future ADRs.

**Impact on future Work Packages:** Every future Business-Object registration ADR can cite "CMD-001 §26.3a, steps 1–3: [result]" instead of re-deriving the test's own existence.

**Migration guidance:** Add this as new subsection **CMD-001 §26.3a**, immediately following the existing §26.3 Registration Principle. Does not change §26.3's own text or any existing registration's validity — purely additive.

---

### 3. A Formal Distinction Between Constitutional Blockers and Implementation Blockers

**Current process:** IRA-004's own Gap Analysis (§10) uses an A–E category scheme (inherited from IRA-001/002/003) where Category D means "governance clarification required." In practice, this Work Package correctly treated some Category-D-adjacent questions as requiring a full ADR (BA-04's proposal-target-type scope; every Business Object registration) and correctly treated at least one comparably significant question — BA-08's "does completion mutate real ERG-001 data" — as an ordinary, disclosed implementation decision (Option A/B/C) requiring no ADR at all. The dividing line was reasoned through correctly each time but is not written down anywhere as a rule.

**Improved process:** State the dividing line explicitly: **a question is a Constitutional Blocker (requires an ADR and/or CBOR registration before implementation) if answering it either (a) determines whether a construct is a Canonical Business Object, or (b) requires introducing a new entity, table, API, service boundary, or business rule not already authorized by an existing canonical document (CLAUDE.md §18's own list).** A question is an Implementation Blocker (resolved by disclosure in the IMP-REPORT, no ADR needed) if every candidate answer stays within already-authorized architecture and only decides *how much* of it to build now versus defer.

**Rationale:** BA-08's own Option A/B/C analysis is a clean worked example of applying this line correctly (Options B and C would have required inventing an unauthorized change-representation schema — Constitutional; Option A stayed within already-authorized architecture and only decided scope — Implementation). Writing the rule down means the next Work Package doesn't have to re-derive it under pressure.

**Expected benefit:** Faster, more consistent triage of "does this need an ADR" questions; fewer unnecessary ADRs, and no missed ones.

**Impact on future Work Packages:** Applies to every Gap Analysis category assignment from here forward.

**Migration guidance:** Add as a clarifying note under IRA methodology's own Category D definition (wherever IRA-001's own template first defines the A–E scheme) — does not change any existing category assignment, only documents the test used to make them.

---

### 4. Mandatory Context Lifecycle Analysis for Journey-Shaped Capabilities

**Current process:** PE-001-C005 §38.13 states its own experience progression explicitly ("Discover → Orient → Frame Intent → Shape Outcome → Assess → Review → Validate → Complete or Exit") — a generic journey shape, not a set of independent operations the way PE-001-C004/C007's own ERBs were (each a concrete lifecycle verb: Establish, Suspend, Retire). This structural difference was noted once, early (IRA-004 §3's own "Structural observation"), but its implication — that a journey-shaped capability's Context Model is likely to be one connected pipeline, not several unrelated objects — was not acted on until BA-06.

**Improved process:** When an IRA's own §3 (ERB analysis) notes that a capability's ERBs describe one generic journey rather than several independent operations (the same signal already captured for C-005), that finding should immediately trigger Improvement #1 (mandatory upfront Context Discovery) rather than being logged as an interesting observation and left for a later Business Activity to rediscover the consequence of.

**Rationale:** The early warning sign was already present in this repository's own IRA-004 §3 — it just wasn't connected to the registration work that followed five Business Activities later.

**Expected benefit:** Closes the gap between "we already noticed this is a journey" and "we acted on what that implies."

**Impact on future Work Packages:** Any future capability whose own ERB analysis notes a generic-journey shape (rather than independent lifecycle verbs) gets its full Context Model mapped at IRA-drafting time.

**Migration guidance:** Add a cross-reference from wherever IRA methodology defines §3 (ERB Analysis) to Improvement #1 — "if this section's own finding is a generic journey shape, proceed immediately to full Context Discovery, do not defer."

---

### 5. An Explicit Transient-Context vs. Canonical-Business-Object Checklist

**Current process:** Two candidate constructs were correctly excluded from registration (Comparison Context, BA-04; Downstream Continuation Context, BA-09), each requiring a full re-derivation of why it failed the eligibility test, including, in the second case, noticing that the governing text explicitly self-describes the construct as transient ("C-005-only transient context not required downstream").

**Improved process:** Add an explicit negative-case checklist to Improvement #2's own procedure: a construct is presumptively **not** a Business Object if its own governing text (a) is silent on it outside of one Enterprise Experience's own Produced Context field, or (b) explicitly describes it using words like "transient," "not required downstream," or "closes without being carried forward." Both signals were present, in this exact language, for both correctly-excluded constructs this Work Package found.

**Rationale:** These two negative findings took real, careful analysis to reach; a checklist derived directly from the language that actually decided them makes the next capability's own negative cases faster to recognize.

**Expected benefit:** Reduces the risk of over-registering (treating every produced artifact as a Business Object) as this repository's own Context-Discovery discipline (Improvement #1) becomes more proactive.

**Impact on future Work Packages:** Directly usable the next time a multi-stage capability's own Context Model is discovered upfront and needs sorting into "register" vs. "don't register" buckets.

**Migration guidance:** Fold into the same CMD-001 §26.3a addition proposed in Improvement #2, as an explicit "Negative Indicators" subsection.

---

### 6. A Named Business Activity Interruption/Resume Protocol

**Current process:** This Work Package's own implementation was interrupted and resumed roughly six times (once per Business Object discovery), each resume beginning with an ad hoc "Phase 1: Repository Reconstruction, Phase 2: Interruption Analysis" pass, re-verifying branch/HEAD/Alembic head/IRA/ADRs/IMP-REPORT/WPR-001 fresh each time. This worked flawlessly (no state was ever lost or double-counted) but was re-invented as prose instructions each time rather than following a documented, named procedure.

**Rationale for formalizing:** The pattern that worked — verify branch/HEAD/Alembic head, confirm prior Business Activities' own completion via IMP-REPORT/WPR-001, classify the interrupted item as A (not started)/B (partial)/C (undocumented-complete)/D (other), then resume — is exactly the kind of repeatable procedure IMP-001 already formalizes for other things (e.g., §6.3's own Business Activity Lifecycle).

**Improved process:** Name this the **"Business Activity Resume Protocol"** and document its four phases in IMP-001 directly, so future sessions do not need the phases re-specified by the user's own prompt each time (as happened, correctly but repeatedly, throughout this Work Package).

**Expected benefit:** One less thing to re-explain per resume; a single canonical procedure to audit against.

**Impact on future Work Packages:** Applies identically to any future interrupted Work Package, regardless of why the interruption occurred.

**Migration guidance:** Add as new IMP-001 subsection, adjacent to §6.3 (Business Activity Lifecycle) — purely additive, documents an already-proven practice.

---

### 7. Implementation Readiness: Split Large, Multi-Registration IRAs

**Current process:** IRA-004 grew to 27 sections over the course of WP-04, six of which (§21–§27, excluding §24) are full CMD-001 §26.4 Business Object registration entries, each repeating a substantial "Explicitly Not Decided" boilerplate. The document remains navigable but is now significantly longer than IRA-001/002/003 ever were, none of which needed more than one registration.

**Improved process:** For any Work Package whose own Context Discovery (Improvement #1) surfaces more than two or three Business Objects, register them in a **dedicated companion document** (e.g., `IRA-004-CBOR_Enterprise_Structure_Management_Business_Object_Registrations.md`) rather than accumulating numbered sections inside the IRA itself. The IRA keeps one summary table (object, identifier, registering ADR, one-line status) and a single cross-reference to the companion document.

**Rationale:** This is a scaling concern, not a correctness one — IRA-004 is still fully correct and traceable, but a future capability with, say, ten Context Model rows would produce an even more unwieldy single document.

**Expected benefit:** Keeps the IRA itself focused on Business-Activity-level readiness; isolates the (now-anticipated, per Improvement #1) bulk registration work to its own document.

**Impact on future Work Packages:** Only relevant for capabilities whose Context Discovery pass (Improvement #1) surfaces multiple objects at once — which, if Improvement #1 is adopted, will now be the normal case rather than the one-at-a-time surprise it was for WP-04.

**Migration guidance:** No retroactive change to IRA-004 proposed. Apply to the next Work Package whose own upfront Context Discovery surfaces more than two Business Objects.

---

### 8. Independent Certification Must Use a Genuinely Independent Reviewer

**Current process (this Work Package):** CERT-WP-04 was performed by dispatching a fresh-context subagent with no implementation involvement to independently re-verify claims against source code, before the certifying pass synthesized the subagent's findings into a decision. This was a deliberate choice made in response to CLAUDE.md §19.7's own explicit prohibition ("the implementation agent SHALL NOT certify its own work") — but it was a choice, not a required step; nothing currently mandates it.

**Improved process:** Make this mandatory, not discretionary: **CLAUDE.md §19.7 should state explicitly that Independent Certification requires dispatching a separate, fresh-context reviewer (subagent, or a genuinely different session/party) to re-verify claims against actual source, migrations, and test execution — synthesis of the implementing session's own memory alone does not satisfy "independent."**

**Rationale:** Self-certification-by-recollection is exactly the failure mode §19.7 already exists to prevent; the fresh-context-subagent pattern is a concrete, repeatable way to satisfy the rule that this Work Package discovered worked well but did not formally require.

**Expected benefit:** Removes ambiguity about what "independent" means in practice; every future CERT-WP-XX gets genuine, not assumed, independence.

**Impact on future Work Packages:** Every future Work Package closure follows the same two-step certification shape: dispatch independent verification, then synthesize a decision from its findings.

**Migration guidance:** Add one sentence to CLAUDE.md §19.7's own Independent Certification subsection, formalizing the practice already used for CERT-WP-04. Does not retroactively invalidate CERT-WP-01/02/03 (their own certification methodology was not reviewed as part of this retrospective).

---

### 9. A Central Cross-Work-Package Business Object Registry

**Current process:** CMD-001 §26 describes the Canonical Business Object Register conceptually, but no single, live document actually lists every registered Business Object across every Work Package — each Work Package's own IRA accumulates its own local registrations (IRA-004 §21–§27 for WP-04's six). Checking whether some future capability's own candidate object already exists under a different name requires grepping every prior IRA, not consulting one index.

**Improved process:** Introduce a genuinely central, thin index — e.g., `architecture/02-Constitutional/CBOR-INDEX.md` — listing every registered Business Object (identifier, canonical name, owning capability, registering ADR, owning IRA section) across all Work Packages, updated as a mechanical, one-line-per-object addition whenever a new object is registered. The full registration entry stays in its own Work Package's own IRA; the index only points to it.

**Rationale:** This Work Package alone produced six registrations; a repository with several more capabilities like C-005 will produce dozens, and "grep every IRA" does not scale as a reuse-discovery mechanism.

**Expected benefit:** A future Work Package's own Context Discovery pass (Improvement #1) can check the index first, rather than needing full-text search across every prior IRA to determine if a candidate object already exists.

**Impact on future Work Packages:** Every future registration ADR adds one line to this index as part of its own IRA-alignment commit — a small, mechanical addition to an already-established commit pattern.

**Migration guidance:** Creating the index and backfilling it with WP-04's own six entries (plus checking whether WP-01/02/03 registered anything — a genuine open question this retrospective does not answer, since neither was reviewed here) is itself a small, separate follow-up task, not performed as part of this proposal.

---

### 10. A Technical Debt Severity Rubric

**Current process:** TD severity in this Work Package was assigned as Low for every entry except one (TD-070, High). No documented rubric exists anywhere for what distinguishes Low from Medium from High — each assignment was a reasonable, but ad hoc, judgment call.

**Improved process:** Adopt an explicit rubric, e.g.: **High** = the gap means the capability's own CAP-001-stated Business Intent is not actually delivered, or a security/tenant-isolation boundary is weaker than stated (TD-070 fits this exactly: "Maintain enterprise structure" is not actually performed). **Medium** = the gap affects a cross-capability dependency or a concurrency/race condition with a plausible real-world trigger. **Low** = an internal completeness gap (deferred column, deferred lifecycle state, missing read endpoint) with no external-facing consequence.

**Rationale:** TD-070 was correctly identified as qualitatively different from the other 39 WP-04 TD entries, but "High" as a label only carries real signal if the rubric behind it is consistent and citable, not implicit.

**Expected benefit:** Faster, more defensible severity assignment; easier prioritization when the register grows large enough that severity actually drives triage order.

**Impact on future Work Packages:** Applies to every future TD entry, and could optionally be applied retroactively to re-grade the existing register (not done here — out of scope for a proposal-only retrospective).

**Migration guidance:** Add the rubric to CLAUDE.md §19.8 (Technical Debt Management), as a new subsection clarifying the existing Priority field's own meaning — purely additive, no existing entry's status changes.

---

## Additional Findings (not on the user's own example list)

- **The "implementation name vs. canonical CBOR name" pattern worked well and should be formalized.** Every WP-04 model (`StructuralProposal` for Proposed Outcome Context, `ImpactAssessment` for Impact Context, etc.) used a code-idiomatic class name distinct from its CBOR canonical name, always disclosed in the model's own docstring. This should become a stated convention (e.g., IMP-001 §5, Canonical Business Object Implementation Pattern), not an emergent practice discovered six times independently.
- **The "guarded vs. idempotent state transition" decision should be a mandatory disclosure for every write endpoint that can be called twice against the same target.** BA-06 (resolve concerns) and BA-08 (complete transition) each explicitly decided and documented "guarded, not idempotent" — this should be a required field in every future Business Activity Contract (IMP-001 §6.7), not an optional good practice.
- **The "Option A/B/C minimum-scope analysis" used for BA-08 is a reusable decision technique**, not specific to ERG-001 mutation — it is really "given a governing rule with no specified mechanism, enumerate implementation options from smallest-to-largest architectural commitment, and choose the smallest one that requires inventing nothing." Worth naming (e.g., "Minimum Constitutional Slice Analysis") and citing as a technique in IMP-001 alongside CLAUDE.md §19.5's own Reuse→Configure→Extend→Compose→Create discipline, which it is really a special case of.
- **Business-Activity-level Independent Review (not just the eventual Work-Package-level CERT) caught two real defects this retrospective can point to concretely**: an `id`/`proposal_id` population-ordering bug in BA-04's own service (caught during BA-04's own development, before its own Independent Review even formally ran) and two citation-precision defects in the SCI-000001 registration (caught by BA-03's own Independent Review). This is confirmation, not a new proposal: **keep performing Independent Review at the Business Activity level even when a Work-Package-level certification will also occur later** — the two catch different classes of problem at different levels of granularity, and neither substitutes for the other.

---

## Priority

| # | Improvement | Priority |
|---|---|---|
| 1 | Mandatory Context Discovery at chartering | **High** — the single highest-leverage change; would have saved five separate stop/resume cycles this Work Package alone. |
| 2 | Named Business Object eligibility test | **High** — directly enables #1 to be applied consistently. |
| 3 | Constitutional vs. Implementation blocker distinction | **High** — prevents both over-escalation (unnecessary ADRs) and under-escalation (missed registrations). |
| 4 | Context Lifecycle analysis trigger | Medium — a corollary of #1, useful mainly for journey-shaped capabilities. |
| 5 | Transient-context negative checklist | Medium — refines #2, prevents future over-registration. |
| 6 | Named interruption/resume protocol | Medium — quality-of-life, no correctness risk was ever observed. |
| 7 | Split large multi-registration IRAs | Low — a scaling concern, not yet a live problem. |
| 8 | Mandatory independent-reviewer certification | **High** — directly closes a real self-certification risk CLAUDE.md §19.7 already flags as a rule with no enforcement mechanism. |
| 9 | Central CBOR index | Medium — increasingly valuable as more capabilities are implemented, not urgent today. |
| 10 | TD severity rubric | Low — no misclassification was found this Work Package, but the register will only grow. |

---

## Recommended Document Updates (not performed automatically — proposal only)

- `CMD-001_Canonical_Data_Model.md` — new §26.3a (Improvements #2, #5).
- `SD-002_Universal_Business_Object_Rules.md` — optionally cross-reference §26.3a from §2, if a lighter touch than modifying CMD-001 is preferred.
- `IMP-001_Implementation_Playbook.md` — new subsection near §6.3 (Improvement #6); a note under the IRA-drafting procedure (Improvements #1, #4, #7); a new field in §6.7's Business Activity Contract template (guarded-vs-idempotent disclosure, from Additional Findings); a named citation of the "Minimum Constitutional Slice" technique alongside §19.5's own Reuse→Configure→Extend→Compose→Create discipline (best placed in CLAUDE.md itself, since that is where §19.5 lives — cross-reference from IMP-001).
- `CLAUDE.md` — clarifying note under §19.7 (Improvement #8, mandatory independent-reviewer certification); new subsection under §19.8 (Improvement #10, TD severity rubric); the Constitutional-vs-Implementation-blocker test (Improvement #3) belongs wherever the Gap Analysis A–E category scheme is canonically defined (this retrospective did not locate a single canonical source for that scheme beyond its repeated use in IRA-001 through IRA-004 — worth confirming where it should actually live).
- New document: `architecture/02-Constitutional/CBOR-INDEX.md` (Improvement #9) — creation and backfill proposed as a separate, small follow-up task.

---

## Expected Impact

If adopted before WP-05 begins: any future capability whose governing PE-001-Cxxx specification contains an equivalent multi-stage Context/Object Model section would have that model fully discovered and eligibility-tested in one pass, at IRA-drafting time — converting what took WP-04 nine implementation turns and six separate stop/resume cycles into, at most, one upfront registration pass followed by uninterrupted Business Activity implementation. The remaining improvements (independent certification rigor, TD severity clarity, a central object index) compound in value as more Work Packages accumulate, without changing how any single Work Package is implemented.

---

*End of METH-001. This document is a proposal. No governing document has been modified. No repository file listed under "Recommended Document Updates" has been changed as a result of producing this retrospective.*
