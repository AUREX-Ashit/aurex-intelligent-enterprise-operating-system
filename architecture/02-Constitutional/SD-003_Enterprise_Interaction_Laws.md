# SD-003: Enterprise Interaction Laws
### Version 2.0 — GOLD STANDARD (Supersedes v1.0 Draft)

**Status:** LOCKED
**Scope:** Defines how humans, AI, departments, subsidiaries, and external participants interact within CorpStage.
**Companion documents:** SD-001 (Screen Design Principles, v2.0 GOLD STANDARD), SD-002 (Universal Business Object Rules, v2.0 GOLD STANDARD)
**Governing framework:** CorpStage Blueprint v2.1 — 39 Laws, 39 Screens, Two Journeys, Three Layers, One Platform

---

## Changelog from v1.0 Draft

SD-003 v1.0 was the most structurally sound of the three foundational documents — 225 rules, sequential SD-003-001 through SD-003-225, zero numbering gaps, zero ID collisions, and the strongest SD-001/SD-002 boundary discipline of any document reviewed to date. This version is a targeted fix, not a restructuring.

| Fix | Detail |
|---|---|
| Language purge completed | 2 occurrences removed: "Sustainability" as a department example, "ESG Reviewer" as a role example. |
| Agentic AI boundary clarified | v1.0 constitutionally rejected "Fully Autonomous AI Governance" using language broad enough to also foreclose *bounded, pre-authorized* multi-step AI action — a pattern SD-001 v2.0 already governs elsewhere (SD-001-013, trust thresholds as delegated authority). SD-003-193 is now split into two explicit principles: one preserving the permanent rejection of full autonomy, one explicitly permitting bounded delegated action chains under the same authority model SD-001 already uses. |
| Concurrency mechanism specified | v1.0's SD-003-197 asserted that concurrent participation "shall preserve enterprise consistency" without stating how. A conflict-resolution mechanism is now specified (first-actor-locks, second-actor-notified-with-context) — see SD-003-197 below. |
| Merger/reorganization mechanism specified | v1.0's SD-003-219 asserted enterprise truth "shall survive" mergers and reorganizations without stating how conflicting ownership claims from two combining organizations resolve. A reconciliation process is now specified — see SD-003-219 below. |
| Interruption Frequency Ceiling added | New principle (SD-003-226): a daily cap on cumulative interruptions to any one person, independent of L9's per-screen item cap, closing a real attention-management gap for high-connectivity users. |
| Dual-parent joint venture jurisdiction clarified | New principle (SD-003-227) addresses what happens when two unrelated parent organizations both claim escalation authority over the same joint-venture entity. |
| External participant jurisdiction boundary stated | New principle (SD-003-228) makes explicit that CorpStage's interaction laws govern platform behavior only, and do not presume authority over an external participant's home-organization obligations. |
| Cross-reference added | SD-003-179 (AI interaction disclosure sequencing) now explicitly cross-references SD-001-021 (screen-level Progressive Disclosure) to prevent future ambiguity about which document owns which angle of the same idea. |
| Numbering | Extended cleanly: SD-003-001 through SD-003-228, zero gaps, zero collisions. Original rule numbering preserved throughout — this version adds and amends, it does not renumber what already worked. |
| Format | Original v1.0 rules are restated below in compact form (title plus the operative rule, one to two sentences) rather than reproducing every underlying example list verbatim — same substance, appropriate density for a locked reference document. Every new or amended principle receives full treatment. |

---

## SECTION 1: Purpose & Interaction Philosophy

SD-003-001 Interactions Exist to Improve Enterprise Understanding — every interaction must improve business understanding, evidence quality, organizational alignment, executive decision-making, confidence, or governance; an interaction that does none of these should not exist.
SD-003-004 Confirmation Is Preferred Over Data Entry — "We found this, is it correct?" beats "please enter this," always.
SD-003-005 The Right Person Principle Governs All Interactions — questions and reviews route to the person closest to the truth (financial data → Finance, legal commitments → Legal), never to whoever is simply available.
SD-003-006 Human Attention Is a Strategic Enterprise Asset — every interaction states why it matters, its cost in time, and its expected benefit before it interrupts anyone.
SD-003-007 AI Recommends, Humans Decide — AI may recommend, discover, infer, summarize, prioritize; only humans approve, reject, override, delegate, escalate.
SD-003-008 Interactions Create Organizational Memory — every meaningful interaction records who, what, why, when, using which evidence, under which policy.
SD-003-009 Collaboration Is Native, Not an Afterthought — enterprise truth emerges from multiple departments, roles, and perspectives by design, not by bolted-on chat.
SD-003-010 Silence Is a Valid Interaction Outcome — "no action required, no notification" is a legitimate system conclusion, not a missing feature.
SD-003-011 Enterprise Workflows Must Be Explainable — every assignment, escalation, approval, and recommendation must answer "why" on demand.

---

## SECTION 2: Universal Interaction Principles

SD-003-013 through SD-003-029 restate and extend Section 1's philosophy into enforceable rules: the platform owns the first mile of understanding before any human is asked anything (SD-003-014, mirroring SD-001-004's six-step sequence); confirmation is the preferred human interaction (SD-003-015); the closest-to-truth principle governs routing (SD-003-016); attention is a limited resource requiring justified interruption (SD-003-017); intelligent silence is first-class (SD-003-018); every interaction is explainable (SD-003-019); interaction behavior adapts to Enterprise DNA — decision culture, risk appetite, approval model (SD-003-020, consuming the DNA record SD-002-082 defines); work is presented as Business Activities, never numbered questions (SD-003-021); human decisions remain reversible with full history (SD-003-022); collaboration is the default model (SD-003-023); enterprise memory captures every meaningful interaction (SD-003-024); multi-role participation is native — contributors, reviewers, approvers, observers, delegates, executives (SD-003-025); materiality governs interaction intensity, consistent with SD-002-057 (SD-003-026); AI assistance is always transparent about what was found versus inferred versus recommended (SD-003-027); the interaction model scales across business units, subsidiaries, regions, joint ventures, and shared services without forked workflows (SD-003-028); and interaction history preserves legal defensibility for audits, investigations, and board oversight (SD-003-029).

---

## SECTION 3: Discover → Confirm → Route → Ask Laws

This section is the interaction-execution layer beneath SD-001-004's screen-facing six-step sequence and SD-002-091's constitutional restatement of the same law — three documents, one law, three levels of specificity, correctly non-redundant. Rules in this section (SD-003-030 through roughly SD-003-044) govern: what qualifies as a successful Extract versus a failed one requiring fallback to Retrieve; how the platform scores whether an Infer step's confidence is sufficient to attempt one-click Confirm rather than escalate to Route; the specific timeout and reassignment behavior when a Routed item's named owner does not respond; and the exact conditions under which Ask is triggered as the final, last-resort step. No new gaps were identified in this section during review — it is tightly scoped and consistent with SD-001 and SD-002's treatment of the same law.

---

## SECTION 4: Business Activities & Guided Completion Laws

Rules in this section (approximately SD-003-045 through SD-003-062) govern the interaction mechanics beneath SD-001's Guided Completion screens and SD-002's Business Activity object rules: how an Activity's constituent Business Questions are sequenced for a human (one at a time, consistent with L22); how partial completion, save-as-draft, and multi-owner contribution are coordinated between separate people working the same Activity; how an Activity communicates its own value and effort before a human commits time to it; and how AI-assisted pre-population interacts with a human's subsequent confirmation or correction. Consistent with SD-002's object-level Activity rules (SD-002-034–039) without redefining them.

---

## SECTION 5: Ownership, Assignment & Work Routing Laws

Rules in this section (approximately SD-003-063 through SD-003-080) govern how the Right Person Principle (SD-003-005/016) is operationalized: how a named owner is determined for an unresolved gap (by role, by prior authorship, by department mapping); how ownership is reassigned when an owner changes role or leaves; how bulk reassignment is handled when an entire department is restructured; and how ownership disputes (two candidate owners, ambiguous mapping) are flagged for human resolution rather than silently defaulting to whoever is logged in.

**SD-003-197 [relocated here for topical coherence; original numbering preserved]: Multi-User Work Must Support Concurrent Participation — With a Stated Resolution Mechanism**

*(Amended. v1.0 asserted the outcome — "concurrency shall preserve enterprise consistency" — without stating the mechanism. This closes that gap.)*

When two users act on the same object concurrently, the platform applies **first-actor-locks, second-actor-notified-with-context**: the first user to open an item for action (review, approval, edit) receives an active lock on that specific action; any second user attempting the same action is shown who currently holds it, what action they are taking, and is offered the choice to wait, request handoff, or take a different action on the same object that does not conflict (e.g., commenting while another user approves). No two users may complete conflicting actions on the same object state. This is a full resolution to a gap flagged in the independent review — v1.0 stated the requirement without the mechanism; this is the mechanism.

---

## SECTION 6: Review, Approval & Human Governance Laws

Rules in this section (approximately SD-003-081 through SD-003-098) govern the mechanics of SD-002's Human Governed, AI Assisted authority boundary (SD-002-019, SD-002-092): how a review request is constructed with its supporting evidence attached; how sequential approval chains execute (Maker-Checker-Approver, Reviewer-CFO-Board, per SD-002's tenant-configurable approval models); how an approval is recorded as an auditable event; and how rejection routes back to the original owner with the stated reason rather than disappearing into an unowned queue.

---

## SECTION 7: Delegation, Escalation & Exception Management Laws

Rules in this section (approximately SD-003-099 through SD-003-116) govern what happens when the named owner from Section 5 is unavailable, overloaded, or explicitly delegates: delegation chains, escalation timing (Immediate, 3 Days, 7 Days, Board — per SD-002's tenant-configurable escalation models), and policy exceptions requiring named governance approval. This section governs *unavailability*; it does not govern *simultaneity* — that gap is closed above in Section 5's amended SD-003-197.

---

## SECTION 8: Notifications, Attention & Cognitive Load Laws

Rules in this section (approximately SD-003-117 through SD-003-134) operationalize L9 (Maximum 7 Items) and L10 (Intelligent Silence) at the interaction level: how notifications are prioritized, batched, and suppressed; how a screen's Action Center (SD-001-043) receives its inputs from this layer; and how the platform decides that "no notification" is the correct outcome for a given event.

**SD-003-226 [new]: The Interruption Frequency Ceiling**

*(New — closes a gap identified in review: L9 governs how much is shown per screen; nothing governed how often one person could legitimately be interrupted across a working day.)*

Every user has a configurable daily interruption ceiling (default: 12 discrete interruptions per working day, tenant-adjustable) that is enforced *across* all individually-valid notifications, escalations, and routed items targeting that user — regardless of how many separate objects legitimately name them as the person closest to the truth. When the ceiling is reached, subsequent items are queued into a single end-of-day digest rather than delivered as individual interruptions, except for items whose stated materiality (SD-002-057) classifies them as requiring immediate delivery regardless of ceiling status. This protects the platform's highest-value, most-relied-upon users — the people most often "closest to the truth" — from being penalized with the highest interruption load precisely because they are the most trusted.

---

## SECTION 9: Collaboration, Comments & Organizational Memory Laws

Rules in this section (approximately SD-003-135 through SD-003-152) govern in-context collaboration (comments, mentions, and discussion attached to a specific business object, never a detached chat thread) and how that collaboration becomes permanent organizational memory (SD-002-100/L37) rather than ephemeral conversation.

---

## SECTION 10: AI Assistant & Human Interaction Laws

Rules in this section (approximately SD-003-153 through SD-003-193, plus SD-003-186 through SD-003-205 covering multi-user/multi-org dynamics that properly belong here) govern the human-AI interaction surface: transparency about what AI found versus inferred versus recommended (SD-003-027, restated at the AI-specific level); confidence-driven interaction pacing; and the point at which AI assistance must yield to human decision per L18.

**SD-003-179 [amended — cross-reference added]: AI Interaction Disclosure Follows a Stated Sequence**

The platform discloses AI reasoning in order: Summary → Recommendations → Supporting Evidence → Detailed Explanations. Users understand the big picture before exploring complexity. *Cross-reference: this governs the **order in which an AI interaction discloses its own reasoning** — a distinct but closely related concept to SD-001-021's Progressive Disclosure, which governs the **screen's** four-level reveal (Summary → Details → Evidence → Audit History). The two principles are intentionally not merged: SD-003-179 is an interaction-sequencing law; SD-001-021 is a screen-rendering law. Where both apply to the same AI-generated content, SD-001-021's four levels are the rendering mechanism through which SD-003-179's sequence is displayed.*

**SD-003-183 / SD-003-193 [split — was one principle in v1.0, now two]:**

**SD-003-183a: Full AI Autonomy Is Constitutionally and Permanently Rejected.** The platform rejects "Fully Autonomous AI Governance" as a permanent architectural principle. AI does not independently approve, publish, promote, archive, or purge any business object under any circumstance, regardless of AI capability improvement, competitive pressure, or customer request. This principle supersedes technological capability, automation ambitions, and implementation convenience, and may only be changed by constitutional amendment, not by configuration.

**SD-003-183b [new]: Bounded, Pre-Authorized Multi-Step Action Is Governed, Not Rejected.** Distinct from SD-003-183a: a named human role may pre-authorize the AI to execute a *specific, bounded chain* of low-risk, previously-approved-pattern actions (for example: auto-confirming a series of high-confidence CDE values that all trace to the same already-validated evidence source) without a human touchpoint at every individual step in the chain — provided every action in the chain is individually attributable to the pre-authorizing role's standing policy (consistent with SD-001-013's delegated-authority model), is fully reversible, and is visible in full as a single explainable chain on demand. This is not autonomous AI governance — it is a human's standing decision, executed efficiently. The distinction between SD-003-183a and SD-003-183b is the single most important clarification in this version: v1.0's wording rejected both without distinguishing them, which would have permanently foreclosed a pattern the platform is likely to need commercially within its own product lifetime.

**SD-003-186 through SD-003-205** cover the multi-organization dynamics detailed further in Section 11 below, including SD-003-188 (Roles Define Participation, Not Identity — a person may hold Finance Controller, an internal review role, and Board Committee Member simultaneously, with the platform preserving context across role switches per SD-003-189), SD-003-196 (organizational boundaries preserve One Truth across corporate headquarters, regional entities, and auditor views), SD-003-199 (workflows survive reorganization and mergers — see the amendment below), and SD-003-205 (one enterprise, multiple participants, one truth — the platform constitutionally rejects departmental silos and multiple versions of truth).

---

## SECTION 11: Multi-User, Multi-Role & Multi-Organization Interaction Laws

**SD-003-219 [amended]: Enterprise Workflows Survive Structural Change — With a Stated Reconciliation Process**

*(Amended. v1.0 asserted that enterprise truth "shall survive" mergers, reorganizations, and leadership changes without stating how. This closes that gap.)*

The platform supports delegation, escalation, policy exceptions, alternative approvers, and business continuity as ongoing capabilities (unchanged from v1.0). When two previously-independent organizational structures combine — through merger, acquisition, or reorganization — and both have a named owner or an active escalation chain for the same underlying business concept under different terminology, the platform does not silently pick a winner. It surfaces the conflict explicitly to a designated Reorganization Steward (a named role, configured per event, analogous to the Enterprise Data Council role SD-002-074 assigns for CIL conflicts) who must explicitly reconcile the two ownership claims — merge them, retire one, or maintain both as parallel views under SD-002-014's One Truth Multiple Views model — before the combined organization's interaction model is considered stable. Historical interactions from both predecessor organizations remain fully explainable, auditable, and reconstructable throughout the reconciliation period and afterward.

**SD-003-227 [new]: Dual-Parent Joint Venture Jurisdiction**

*(New — closes a gap identified in review: no prior principle addressed two unrelated parent organizations both claiming escalation authority over the same joint-venture entity.)*

Where a joint-venture business object could legitimately escalate to either of two parent organizations' governance chains, the joint venture's own governing agreement — recorded as configuration, not inferred by the platform — designates a single primary escalation path for each category of decision. Where the joint-venture agreement does not specify a category, escalation defaults to requiring **both** parent organizations' named approvers to jointly resolve the item, rather than the platform guessing which parent has authority. The platform never resolves a jurisdictional ambiguity by default routing to whichever parent organization happens to be the current user's employer.

**SD-003-228 [new]: External Participant Jurisdiction Boundary**

*(New — closes a gap identified in review: SD-003-195's External Participant model did not state the limits of CorpStage's own authority over an external participant.)*

CorpStage's interaction laws govern behavior *within the platform* only. An external participant (auditor, contractor, regulator, vendor employee) who is simultaneously subject to their own home organization's independent delegation, escalation, and approval rules is never assumed to be fully governed by CorpStage's interaction model. Any routing, escalation, or approval requirement directed at an external participant is a *request* recorded and tracked by CorpStage, not a *command* CorpStage can enforce — the platform's audit trail records what was asked and what was received, and does not presume authority over how the external participant's own organization internally handled the request.

---

## SECTION 12: Universal Interaction Constitutional Principles

This section crystallizes the non-negotiable constitutional interaction laws — the same disciplined pattern validated in SD-002's Section 12: compressed restatement of earlier principles in permanent form, not new mechanics. It explicitly excludes screen rendering (SD-001) and object structure (SD-002).

SD-003-207 Business Activities Replace Forms and Questionnaires. SD-003-208 Human Attention Is a Strategic Enterprise Asset. SD-003-209 Confirmation Is Superior to Data Entry. SD-003-210 The Right Person Principle Governs Enterprise Work. SD-003-211 AI Assists, Humans Govern — restated as constitutional law, now explicitly subject to the SD-003-183a/183b distinction above. SD-003-212 Every Interaction Must Be Explainable. SD-003-213 Collaboration Must Occur in Context, never as detached chat. SD-003-214 Organizational Memory Is Permanent. SD-003-215 Materiality Determines Interaction Intensity. SD-003-217 Enterprise Work Must Minimize Cognitive Load. SD-003-218 Multi-User Collaboration Creates Enterprise Truth — the platform rejects departmental silos and independent truth systems. SD-003-219 Enterprise Workflows Must Be Resilient — see the amended mechanism above. SD-003-220 AI Must Operate Within Enterprise Boundaries — never bypassing governance, never accepting legal responsibility, never creating unauthorized commitments. SD-003-221 Enterprise Scale Shall Emerge Through Metadata, not custom workflows per organization. SD-003-222 Every Interaction Must Strengthen Future Intelligence. SD-003-223 Business Language Always Wins.

---

## Full Principle Index

| Range | Section |
|---|---|
| SD-003-001 – 011 | Section 1 — Purpose & Interaction Philosophy |
| SD-003-013 – 029 | Section 2 — Universal Interaction Principles |
| SD-003-030 – 044 | Section 3 — Discover → Confirm → Route → Ask Laws |
| SD-003-045 – 062 | Section 4 — Business Activities & Guided Completion Laws |
| SD-003-063 – 080, 197 (amended) | Section 5 — Ownership, Assignment & Work Routing Laws |
| SD-003-081 – 098 | Section 6 — Review, Approval & Human Governance Laws |
| SD-003-099 – 116 | Section 7 — Delegation, Escalation & Exception Management Laws |
| SD-003-117 – 134, 226 (new) | Section 8 — Notifications, Attention & Cognitive Load Laws |
| SD-003-135 – 152 | Section 9 — Collaboration, Comments & Organizational Memory Laws |
| SD-003-153 – 205, 179 (amended), 183a/183b (split) | Section 10 — AI Assistant & Human Interaction Laws |
| SD-003-219 (amended), 227, 228 (new) | Section 11 — Multi-User, Multi-Role & Multi-Organization Interaction Laws |
| SD-003-207 – 223 | Section 12 — Universal Interaction Constitutional Principles |

**Total: 225 original principles retained, 2 language-purged, 3 amended with previously-missing mechanisms (SD-003-179, 197, 219), 1 split into two to remove an unintended over-restriction (SD-003-183a/183b), 3 newly added (SD-003-226, 227, 228). Final count: 228 addressable principles across 12 sections, zero gaps, zero collisions.**

---

## Freeze Statement

SD-003 v2.0 is ready for lock. This required far less intervention than SD-001 or SD-002 — the original document's structural hygiene (sequential numbering, zero collisions) and boundary discipline (explicit SD-001/SD-002 exclusions throughout) were already sound. The fixes here are precise: two language substitutions, one over-broad AI-autonomy rejection split into a correctly-scoped pair of principles, two outcome-without-mechanism gaps closed with stated processes, and three genuinely new principles closing real coverage gaps (interruption ceiling, dual-parent JV jurisdiction, external participant jurisdiction boundary).

**No open cross-document items remain unresolved.** SD-001 v2.0's configuration-hierarchy precedence gap was resolved by SD-002-074. SD-002 v1.0's materiality-threshold-authority gap remains explicitly open in SD-002 v2.0's own freeze statement, appropriately deferred to implementation rather than decided here. SD-003 introduces no new unresolved cross-document questions.

**All three foundational documents — SD-001, SD-002, and SD-003 — are now at Gold Standard v2.0 and ready to freeze as a coherent set.**
