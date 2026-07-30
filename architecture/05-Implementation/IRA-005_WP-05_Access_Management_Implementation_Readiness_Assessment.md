# IRA-005 — WP-05 Implementation Readiness Assessment

**Document ID:** IRA-005
**Work Package:** WP-05
**Capability:** C-002 — Access Management
**Governing Specification:** `docs/Product/PE-001/capabilities/C-002/PE-001-C002_Access_Management.docx` (Version 1.0, Initial Gold Standard Engineering Pass — Independent Derivation, APPROVED for publication per its own Chapter 9.16)
**Methodology Applied:** ADR-014 / WP-METH-001 (IMP-001 §6.2a Mandatory Context Discovery, §6.2b Gap Analysis Category Scheme, CMD-001 §26.3a Canonical Business Object Eligibility Test) — applied in full, as the first IRA drafted after their adoption.
**Status:** Assessment only. No implementation, no code, no migration, no ADR, no Canonical Business Object registration is performed by this document.

Treat the Git repository as the ONLY source of truth. Every claim below is sourced from `docs/Product/PE-001/capabilities/C-002/PE-001-C002_Access_Management.docx` (extracted and read directly for this assessment), `architecture/02-Constitutional/CAP-001_Enterprise_Capability_Registry.md`, `architecture/02-Constitutional/URA-001 - User, Role, Permission, Event and ssignment.md`, `architecture/02-Constitutional/RTA-001 - Runtime Architecture and Execution.md`, `architecture/00-Governance/WPR-001_Work_Package_Roadmap.md`, `architecture/06-Reviews/TECH-DEBT.md`, and a direct search of `Backend/Services/AuthService` and `Backend/Shared/Security`. No claim is drawn from conversational memory.

---

## 1. Executive Summary

C-002 (Access Management) is Active in CAP-001 (line 53) and has never had a Work Package, an IRA, or any implementation anywhere in this repository — confirmed independently here and previously disclosed as a Governance Backlog Item in `IRA-003` §17 and `IRA-004` §17. This assessment finds:

- **Capability boundary is well-specified.** PE-001-C002 v1.0 is a complete, internally validated, Gold-Standard-passed specification: 1 CRB, 3 ERBs, 8 EXs, 8 Business Rules, 7 Contracts, and an explicit Context Model (§1.16) — the trigger condition for IMP-001 §6.2a's own bounded Context Discovery scan (§3 below).
- **Business Object eligibility resolves to exactly one registration candidate**, not several. Of six named context constructs, only **Access Evaluation Outcome** is independently identified, cross-experience-referenced, and governed by a real lifecycle; the other five are either transient (Governed Request Context) or lifecycle-state labels of the same one object (Preserved/Superseded/Invalidated/Deferred), not separate objects (§4 below).
- **A single-object lifecycle, not a multi-object chain.** Unlike WP-04's Structural Context Lifecycle (six distinct objects, each produced by a separate Business Activity and consumed by a later one), C-002's lifecycle is one object moving through states within a bounded execution scope. `ADR-010`'s pattern does not apply here, and this assessment does not propose an equivalent pattern-level ADR (§5 below).
- **A genuine, capability-defining readiness blocker exists**, distinct in kind from anything WP-01 through WP-04 encountered. PE-001-C002 itself places the actual authorization-decision computation ("the Authorization Engine's own decision-computation logic... any API, database, microservice, frontend component, or technical state machine") explicitly **out of C-002's own scope** (§1.5), assigning it to RTA-001/IMP-001. RTA-001 §11.2 names this Authorization Engine as "the sole authority for runtime authorization decisions." **No implementation of this engine, or of a URA-001-76 precedence-chain resolver, exists anywhere in this repository** (confirmed by direct search, §6 below), and the `Group` construct URA-001-76 itself requires (Named User > **Group** > Approval Authority > Business Role > Domain Permission) has no model anywhere in AuthService. This is not an ordinary implementation gap: a stubbed or approximated decision engine risks producing a false `Permitted` outcome, which CLAUDE.md §19.8.5 already prohibits deferring as ordinary Technical Debt (Technical Debt SHALL NOT be used to defer security defects). The Business Activity realizing ERB-C002-01 (the capability's own central purpose — "govern access rights") is therefore assessed as **Category D, bordering E** (§6-§7 below), and this assessment recommends the matter be raised as a Governance Backlog Item rather than silently scoped down or silently built.
- **A meaningful, non-blocked minimum slice exists.** The two other ERBs (Preserve/Bound validity; Resolve disruption and hand-off-rejection classification) and two of ERB-C002-01's own four outcome branches (Unresolved, Deferred) do not require the missing decision engine and are assessed Category C.

**Overall Readiness Decision: NOT READY for WP-05's full scope (C-002's central Evaluate-and-decide purpose is blocked). A disclosed, minimum-scope subset is READY, contingent on the governance decision recommended in §9.**

---

## 2. Capability Analysis

| Attribute | Value |
|---|---|
| Capability | C-002 — Access Management |
| Business Intent (CAP-001, verbatim) | "Govern access rights." |
| CRB | CRB-C002 |
| ERB Count | 3 |
| EX Count | 8 |
| Experience Contract Count | 7 |
| Business Rule Count | 8 (BR-C002-01 through BR-C002-08) |
| Primary Specification Authority | URA-001 §6 (URA-001-71–86, Event Architecture & Runtime Assignment Model, specifically URA-001-76 Authorization Resolution Precedence) |
| Runtime Decision Authority (consumed, not owned) | RTA-001 §11 (Authorization Runtime / Authorization Engine) |
| Capability Identity Authority | CAP-001 |
| Out of Scope (PE-001-C002 §1.5, verbatim in relevant part) | "Identity establishment... Role and Permission definition or assignment (C-003); Delegation, Escalation, and Runtime Assignment definition (URA-001, no dedicated PE-001-Cxxx yet authored)... the Authorization Engine's own decision-computation logic, authorization-engine implementation, policy language, IAM/RBAC/ABAC implementation, credential or authentication mechanisms (owned by RTA-001, IMP-001, and the applicable canonical or implementation authority); any API, database, microservice, frontend component, or technical state machine." |
| Cross-Specification Dependencies | C-001 (Identity, consumed), C-007 (Membership, consumed), C-004 (Organization, referenced), C-003 (Role/Permission/Delegation/Runtime Assignment, referenced) |

**Enterprise Reference Blueprints (ERBs):**

| ERB | Title | Governing clause of the Guiding Architectural Question |
|---|---|---|
| ERB-C002-01 | Evaluate Access for a Governed Request | "Determine... whether [a specific governed request] is currently permitted — producing a scoped... Access Evaluation Outcome... it consumes but never redefines" |
| ERB-C002-02 | Preserve and Bound Access Evaluation Outcome Validity | "Producing a scoped, temporally-bounded Access Evaluation Outcome" |
| ERB-C002-03 | Resolve Access Context Disruption and Re-evaluation | "Safely re-evaluates... rather than assuming its continuity, whenever the request or its governing context changes" |

**Enterprise Experiences (EXs):**

| EX | Title | Governing ERB |
|---|---|---|
| EX-C002-01 | Produce Permitted Access Evaluation Outcome | ERB-C002-01 |
| EX-C002-02 | Produce Denied Access Evaluation Outcome | ERB-C002-01 |
| EX-C002-03 | Produce Unresolved Access Evaluation Outcome | ERB-C002-01 |
| EX-C002-04 | Produce Deferred Access Evaluation Outcome Pending Approval | ERB-C002-01 |
| EX-C002-05 | Preserve Access Evaluation Outcome Within Governed Execution Scope | ERB-C002-02 |
| EX-C002-06 | Expire Access Evaluation Outcome at Scope Boundary | ERB-C002-02 |
| EX-C002-07 | Detect and Resolve Access Context Change | ERB-C002-03 |
| EX-C002-08 | Resolve Dependent Capability Access Hand-off Rejection | ERB-C002-03 |

**Business Rules (Chapter 7.2):** BR-C002-01 through BR-C002-08 — govern (respectively) exclusive derivation from owning authorities, the four-outcome closed set, execution-scoped validity, mandatory re-resolution on context change, hand-off-rejection classification-before-scoping, non-substitution of Identity/Membership/Persona for a resolved permission, prohibition on inventing an authorization-engine mechanism (Pending Canonical Binding instead), and the bounded-delegation-only Autonomous Agent restriction.

**Contracts (Chapter 5):** 5.1 Access Context Authority, 5.2 Access Evaluation Orchestration, 5.3 Access Outcome Semantics, 5.4 Access Scope and Validity, 5.5 Access Re-evaluation and Context Change, 5.6 Cross-Capability Access Hand-off, 5.7 AI Assistance and Explainability.

---

## 3. Business Activities (derived — no canonical BA identifier exists in PE-001-C002 itself; §1.15 records every Business Activity/EAC reference as Pending Canonical Binding, naming IMP-001 as the authority for eventual realization — this section is that realization, mirroring the discipline IRA-001 through IRA-004 already applied for their own capabilities)

Following IMP-001 §6.8's "business-meaningful" granularity standard and the same discipline WP-04 applied when a single Business Activity realized multiple related EXs sharing one Contract (e.g., WP-04 BA-06 realized both "review" and "resolve concerns" under one Business Activity), five candidate Business Activities are proposed:

| Candidate BA | Realizes | Business-Meaningful Action |
|---|---|---|
| BA-01 — Evaluate Access for a Governed Request | ERB-C002-01 (EX-C002-01/02/03/04) | Produce exactly one of Permitted/Denied/Unresolved/Deferred for a specific governed request |
| BA-02 — Preserve and Bound Access Evaluation Outcome Validity | ERB-C002-02 (EX-C002-05/06) | Hold an outcome as valid for its governed execution and expire it at that boundary |
| BA-03 — Detect and Resolve Access Context Change | ERB-C002-03 (EX-C002-07) | Re-resolve an outcome when a governing fact changes |
| BA-04 — Resolve Dependent Capability Access Hand-off Rejection | ERB-C002-03 (EX-C002-08) | Classify and route a dependent capability's rejection of a produced outcome |

BA-02 merges EX-05/06 (opposite triggers of the same "how long is this outcome valid" concern, per ERB-C002-02's own single Contract 5.4 governance) rather than splitting them, mirroring WP-04's own EX-merging precedent. BA-03 and BA-04 are kept separate, unlike BA-02's merge, because they are triggered by materially different signals (a governing-fact change vs. an explicit dependent-capability rejection) and Contract 5.6 governs BA-04 specifically, distinct from Contract 5.5's governance of BA-03 — the same "same-ERB, different-EX, different-Contract stays separate" reasoning IRA-003 §5.10 already applied to its own Contract-driven BA split.

**This numbering is a candidate proposal only.** No Business Activity, EAC, or canonical identifier is created or bound by this IRA — per IMP-001 §1.15's own Pending Canonical Binding disposition, formal binding remains a future action, exactly as it was for WP-04's own BA numbering at IRA-004 time.

---

## 4. Context Discovery (IMP-001 §6.2a, Bounded Scan)

Per IMP-001 §6.2a, PE-001-C002's table of contents / section-header structure was scanned for a chapter analogous to a named, cross-cutting Context/Object/Data Model declaration. **§1.16 "Context Model" is exactly such a section**, stating explicitly: "The Access-specific context constructs engineered by this capability are: Governed Request Context, Access Evaluation Outcome, Preserved Access Evaluation Outcome, Superseded Access Evaluation Outcome, Invalidated Access Evaluation Outcome, and Deferred Access Evaluation Outcome." This triggers the full eligibility pass below, performed upfront in this one IRA — the exact benefit ADR-014 §8 (Consequences) identified as the point of adopting §6.2a: "any capability whose governing specification contains a §38.15-equivalent Context Model section has that model fully discovered and eligibility-tested in one pass, before any Business Activity begins."

The secondary trigger (a generic multi-stage journey shape per an ERB analysis) is also independently present here: ERB-C002-01 → ERB-C002-02 → ERB-C002-03 is itself a generic evaluate → bound → re-evaluate shape, reinforcing the primary trigger rather than needing to be relied upon alone.

Six named constructs were identified from §1.16 and cross-checked against §1.17 (Context Preservation), §1.18 (Context Transitions), Chapter 3's seven-dimension context engineering (Required/Created/Consumed/Preserved/Produced/Superseded/Invalidated) across all three ERBs, and Chapter 4's identical engineering across all eight EXs. No additional named context construct was found beyond these six — this scan is bounded to §1.16 and its direct cross-references, per §6.2a's own bounded-procedure discipline, not an unrestricted document search.

**Cross-reference sections reviewed:** Chapter 6 (Enterprise Transitions & Experience Navigation — the disruption/re-evaluation category table), Chapter 8.3 (Traceability Matrix), Chapter 9.7 (Context State Authority Matrix — itself a governance-owned mapping of each construct to its authoritative lifecycle stage and Contract, directly informative for §5 below).

---

## 5. Business Object Eligibility Analysis (CMD-001 §26.3a)

Each of the six constructs identified in §4 is tested against CMD-001 §26.3a's three-step procedure.

### 5.1 Access Evaluation Outcome

- **Step 1 — Independent Identity.** Yes. A discrete, identifiable record for one specific object/event/Identity combination (§1.16), distinguishable from the request that produced it and capable of being referenced afterward (preserved, superseded, invalidated, handed off) independent of that request's own continued existence (SD-002-004 satisfied).
- **Step 2 — Cross-Experience Reference Test.** Yes, and more strongly evidenced than several of WP-04's own registrations. Within PE-001-C002 itself, the object produced by ERB-C002-01 (EX-01–04) is separately, explicitly consumed as Required/Consumed Context by EX-C002-05/06 (ERB-C002-02, a separately-triggered Enterprise Experience) and by EX-C002-07/08 (ERB-C002-03, likewise separately triggered) — satisfying "retrieved, by identity, from a separately-invoked later Business Activity or Enterprise Experience" within the same document. Beyond C-002's own boundary, Contract 5.6 and §2.5 (Exit Context) both state it is produced "as a stable, inspectable precondition for any dependent capability's own Enterprise Experience" — the same cross-capability hand-off shape WP-03's own Contract 5.10 used to justify BA-10's existence.
- **Step 3 — Governed Lifecycle.** Yes. §1.18 (Context Transitions) and Chapter 6 both state an explicit, real lifecycle: Created (evaluation) → Preserved (within scope) → {Superseded (re-resolution differs) | Invalidated (context change found materially different) | Expired (scope boundary reached)}. This is a persisting state that is later invalidated by a subsequent event, not a value that exists only for one request/response cycle.

**Determination: Eligible. Canonical Business Object.** Recommended for registration (§9), with a Lifecycle Model spanning two independent dimensions — an **Outcome Type** (Permitted / Denied / Unresolved / Deferred, fixed at creation) and a **Validity Status** (Created → Preserved → {Superseded | Invalidated | Expired}) — both drawn directly from Chapter 9.7's own Context State Authority Matrix, not invented by this assessment.

### 5.2 Preserved / Superseded / Invalidated / Deferred Access Evaluation Outcome (four candidates, assessed together)

- **Step 1 — Independent Identity.** **No**, for all four. Re-reading each governing ERB/EX's own Context Created field is decisive: ERB-C002-02's own text states "Nothing new — this ERB bounds and eventually expires an existing outcome; it never produces a new determination itself." EX-C002-05's Context Created: "Nothing new." EX-C002-07's (ERB-C002-03) Context Created: "Nothing new where the outcome is a refresh; no replacement outcome is invented where re-resolution finds a different determination." Where a genuinely new determination is produced (a different outcome after re-resolution), the governing text is explicit that this is achieved by **re-invoking ERB-C002-01** — i.e., producing a fresh Access Evaluation Outcome, not a new object type called "Superseded Access Evaluation Outcome." Each of these four labels has the same identity as the one Access Evaluation Outcome record whose Validity Status they name; none is separably identifiable from it.
- **Steps 2–3.** Not reached — Step 1 already fails for all four, and CMD-001 §26.3a requires Step 1 plus at least one of Steps 2–3; failing Step 1 alone is dispositive.
- **Negative Indicator match.** These four match the CMD-001 §26.3a Negative Indicator pattern by direct analogy to WP-04's own excluded cases (Comparison Context, Downstream Continuation Context): each is a status/disposition of an already-registered object, not a construct with its own governed lifecycle beginning at its own Creation event.

**Determination: Not eligible. Not separate Business Objects.** These four are the **Validity Status** and **Outcome Type** values of §5.1's single registration, exactly as Chapter 9.7's own Context State Authority Matrix already frames them (each mapped to "Access Evaluation Outcome," never to its own row). Registering four additional objects here would duplicate one Business Object under four names — precisely the "One entity, one definition" violation CLAUDE.md §15 (Golden Rule 12) prohibits. This is a materially different eligibility outcome than any single WP-04 registration cycle produced, and is disclosed here as a deliberate, reasoned "merge into one" result, not a shortcut.

### 5.3 Governed Request Context

- **Step 1 — Independent Identity.** No. §1.16 itself states this "is not a canonical domain state, not an EIO" and Chapter 3's own Context Consumed field for ERB-C002-01 confirms it is consumed exactly as produced elsewhere (by the capability that originates the governed request), never created or persisted by C-002 itself. It does not outlive the single evaluation act it enters — no later, separately-invoked EX retrieves it by identity once ERB-C002-01 has consumed it.
- **Steps 2–3.** Not reached; Step 1 fails and no Step 2/3 evidence exists — it is named only as Entry Context to the one ERB that consumes it, with no later ERB or EX naming it as Required or Consumed Context (the CMD-001 §26.3a Negative Indicator's own first bullet, verbatim).

**Determination: Not eligible. Transient Context**, consistent with the specification's own explicit self-description in §1.16.

### 5.4 Summary

| Candidate | Step 1 | Step 2 | Step 3 | Determination |
|---|---|---|---|---|
| Access Evaluation Outcome | Pass | Pass | Pass | **Canonical Business Object** |
| Preserved / Superseded / Invalidated / Deferred Access Evaluation Outcome (×4) | Fail | N/A | N/A | Not eligible — Validity Status/Outcome Type of the one object above |
| Governed Request Context | Fail | N/A | N/A | Transient Context |

**Net result: one Canonical Business Object candidate, not six** — a materially different, and materially cheaper, outcome than WP-04's own six-object discovery, and worth stating plainly: the eligibility test does not always multiply; here it consolidates.

---

## 6. Context Lifecycle

PE-001-C002 defines **a lifecycle, not a set of independent operations** — §1.18 and Chapter 6 both state explicit, traceable transitions (Created → Preserved → {Superseded | Invalidated | Expired}), never a silent or implicit change, satisfying PE-001 15.5's own transition-disclosure requirement.

**This is a single-object lifecycle, not a multi-object chain**, and this distinction matters for whether `ADR-010`'s own pattern-recognition precedent applies. WP-04's Structural Context Lifecycle was six *distinct* Business Objects (SCI → POC → IMC → RVC → VLC → RSC), each newly *Created* by a separate, later-invoked Business Activity, each consuming the previous object's identity as its own Required Context. C-002's lifecycle is the *opposite* shape: **one** object (Access Evaluation Outcome, §5.1), created once by ERB-C002-01, whose only subsequent transitions are changes to that same object's own Validity Status and (on re-resolution) potential replacement by a freshly-created object of the identical type — never a second, third, or further *type* of object entering the chain.

**Determination: No pattern-level ADR (an ADR-010 equivalent) is warranted.** A single object with a stated Lifecycle Model is exactly CMD-001 §26.4's own standard registration shape (a "Lifecycle Model" attribute on one registration) — the ordinary case IRA-001 through IRA-004 already registered without needing a pattern-recognition ADR (`SCI-000001` itself, before `ADR-010` existed, registered the same way). Recognizing this explicitly here — rather than assuming every Context Model section implies a WP-04-style chain — is itself a direct product of IMP-001 §6.2a's bounded scan being genuinely applied rather than pattern-matched superficially.

**Registration timing:** Yes, registration is required before the Business Activity that creates the object (BA-01, §3) begins implementation, per CMD-001 §26.3's own registration-precedes-implementation principle — but only one registration, performed upfront, not iteratively discovered across multiple Business Activities the way WP-04's six were.

---

## 7. Gap Analysis (IMP-001 §6.2b, category A–E)

| Candidate BA | Category | Reasoning |
|---|---|---|
| BA-01 — Evaluate Access for a Governed Request | **D, bordering E** (Governance clarification required — see §9) | The capability's own central purpose. Two of its four outcome branches (Unresolved, Deferred) require no decision engine and are independently buildable using already-existing C-004/C-007/`ApprovalAuthority` facts — but PE-001-C002 §1.5 explicitly places the actual decision-computation mechanism (the URA-001-76 precedence chain, executed by RTA-001's Authorization Engine) **out of C-002's own scope**, and no implementation of it exists anywhere in this repository (§8 below) — nor does the `Group` construct the chain itself requires. Category D reflects that a governance decision (who builds the engine, and whether WP-05 may) is the blocking question, not an ordinary design question; bordering E because, absent that decision, the Permitted/Denied branches specifically have no path forward without inventing exactly the kind of new architectural component (an authorization-engine implementation) CLAUDE.md §18/§19.4 already requires a STOP for. |
| BA-02 — Preserve and Bound Access Evaluation Outcome Validity | **C** (Architecture requires completion — implementation-level) | No decision engine required — bounds and expires an already-produced record against its own stated execution scope. Sequenced after BA-01 exists (needs a real outcome record to operate on), but not blocked by BA-01's own D-rated portion — buildable once even a minimal (Unresolved/Deferred-only) BA-01 slice exists. |
| BA-03 — Detect and Resolve Access Context Change | **C for the detection/classification act; inherits BA-01's D for its own "refresh via fresh evaluation" path** | Re-resolving a changed fact and determining "same or different determination" is itself ordinary implementation-level design once BA-01 exists in some form; where re-resolution must reach a Permitted/Denied determination, it re-enters BA-01's own blocked path, not a new blocker of its own. |
| BA-04 — Resolve Dependent Capability Access Hand-off Rejection | **C** (Architecture requires completion — implementation-level) | Pure classification logic (capability-scoped insufficiency vs. Access Context integrity signal) over an already-produced outcome and a stated rejection reason; requires no decision engine. Routes to BA-03 (and transitively BA-01) only on the integrity-signal path, which is that path's own concern, not BA-04's. |

**No Business Activity meets category E outright** (mirroring WP-01 through WP-04, none of which triggered E either) — BA-01 is assessed D, not E, because a disclosed minimum-scope subset (Unresolved/Deferred outcome branches only, per §9's Option A) provides a genuine, non-fabricated path forward without a governance decision being strictly required to do *something* meaningful; E is reserved for a Business Activity with no path forward under any disclosed scope, which does not describe BA-01's Unresolved/Deferred branches.

**Constitutional-vs-Implementation blocker distinction applied:** BA-01's blocker is constitutional/governance in kind (an unresolved question of architectural ownership — who builds the Authorization Engine, and under which Work Package), not an implementation-level unknown (persistence shape, endpoint naming, and similar questions are not what is blocking it). BA-02/03/04's ordinary sequencing dependency on BA-01 is not itself a Category D condition — IMP-001 §6.2b's own distinction is about the *kind* of open question, and an implementation-ordering dependency on another BA is not a governance question.

---

## 8. Existing Reusable Implementation

Confirmed by direct repository search (`Backend/Services/AuthService`, `Backend/Shared/Security`):

**Exists and reusable:**
- `models/domain_permission.py` + router + service — Domain Permission, one of URA-001-76's five precedence inputs.
- `models/approval_authority.py` + router + service — Approval Authority, another precedence input; directly relevant to BA-01's Deferred branch (EX-C002-04) and to `TD-026`'s own disclosed dependency ("a future Approval Authority resolution/execution capability — C-002/RTA-001 §11, not yet scoped").
- `models/role.py`, `models/delegation_policy.py`, `models/runtime_assignment_policy.py` — partial coverage of Business Role and Delegation/Runtime Assignment inputs, though `runtime_assignment_policy.py`'s own docstring explicitly distinguishes itself from an actual runtime assignment *instance* ("never holds a specific object_type/object_id anchor or assignee — those belong exclusively to the (not yet implemented) `runtime_assignment_registry`").
- `Membership`/`Organization` models (WP-01/WP-03) — cover Identity/Membership/Organization facts BA-01's Unresolved branch needs to check confirmability of.
- `dependencies.require_platform_admin` — the repository-wide interim `PLATFORM_ADMIN`-only gate every prior Work Package's write endpoints use (TD-021 through TD-025, TD-031, TD-034 through TD-036, TD-039, TD-042). Not a precedence-chain implementation; a single role-claim equality check.

**Does not exist anywhere in this repository (confirmed by direct grep, not assumed):**
- Any Authorization Engine, precedence resolver, or function evaluating "is this request permitted" against URA-001-76's chain.
- `Group` / Group Membership — no model, no table, referenced by URA-001-76 itself as a required precedence-chain input.
- `runtime_assignment_registry` — the actual runtime-assignment instance table (as opposed to `RuntimeAssignmentPolicy`, the governed policy).
- `node_permission_assignment` — already disclosed at `IRA-004` §17, reconfirmed here.

**An unused, non-conforming scaffold exists** at `Backend/Shared/Security/` (`authorization_manager.py`, `permission_manager.py`, `role_manager.py`) — flat RBAC + wildcard-string PBAC, imported nowhere in the repository, using a third role catalog matching neither AuthService's seeded roles nor URA-001/MDP-001's canonical catalog. This is **not** a candidate for reuse or extension: it does not implement URA-001-76's precedence chain (no Group, Approval Authority, or Delegation resolution), and CLAUDE.md §12's "Search the repository first... Prefer: Extend → Refactor → Reuse" does not favor extending orphaned, catalog-incompatible code over a correctly-scoped new implementation once BA-01's own governance question (§9) is resolved.

---

## 9. Readiness Decision

**WP-05 is NOT READY to implement its full scope.** The blocker is specific and singular: BA-01's Permitted/Denied outcome branches require a URA-001-76 precedence-chain decision mechanism that PE-001-C002 §1.5 itself places outside C-002's own scope, that exists nowhere in this repository, and that a stubbed or approximated implementation cannot safely substitute for — per CLAUDE.md §19.8.5, a security defect (a wrong authorization determination) is not deferrable as ordinary Technical Debt, and per CLAUDE.md §18/§19.4, a new Authorization Engine component triggers a mandatory STOP-and-report, not a silent build.

**A disclosed minimum-scope subset is READY**, pending the registration in §10.1 (which itself requires no governance decision — CMD-001 §26.3a's own eligibility test is self-executing and was already applied in full in §5): BA-02, BA-03 (its classification portion), and BA-04 have no unresolved constitutional blocker. BA-01 could itself be minimum-scoped (Option A: implement only the Unresolved/Deferred outcome branches, explicitly hard-failing or declining to implement Permitted/Denied pending §9's governance decision — an Option-A-style choice in the same spirit as WP-04 BA-08's, disclosed rather than silently built) — but this assessment does not decide that scope question itself; it is recorded as one of the options in §11 for the repository owner to authorize, consistent with this being a governance decision (§7), not an implementation detail this IRA may resolve unilaterally.

**This is not a repeat of any WP-01 through WP-04 pattern.** Every prior Work Package's blockers were either a same-capability constitutional question (Business Object eligibility, resolved via ADR within that Work Package) or an external Work Package dependency with a known future owner (WP-03 BA-04/BA-05 depending on C-005; WP-04's own `node_permission_assignment` depending on a not-yet-chartered C-002). Here, the blocking component (the Authorization Engine) has **no capability, Work Package, or governing document in this repository that currently claims ownership of building it** — PE-001-C002 assigns it to "RTA-001, IMP-001, and the applicable canonical or implementation authority," and neither RTA-001 (a canonical specification, not an implementation) nor IMP-001 (a methodology playbook) builds runtime components themselves. This ownership gap is the governance question this assessment surfaces, not a question this IRA can resolve by assumption (CLAUDE.md §17: "Never fill architectural or business gaps using assumptions").

---

## 10. Recommendations

### 10.1 CBOR Recommendation

Register **Access Evaluation Outcome** as a Canonical Business Object under CMD-001 §26.4, per the eligibility analysis in §5.1. Recommended registration attributes (for the future registering ADR to complete in full, not fabricated here):

- **Canonical Name:** Access Evaluation Outcome
- **Owning Capability:** C-002 (Access Management)
- **Governing ERB:** ERB-C002-01 (creation); ERB-C002-02 (validity bounding); ERB-C002-03 (re-evaluation)
- **Lifecycle Model:** Outcome Type (Permitted / Denied / Unresolved / Deferred, fixed at creation) × Validity Status (Created → Preserved → {Superseded | Invalidated | Expired}), per Chapter 9.7's own Context State Authority Matrix.
- **Cross-Experience References:** EX-C002-05/06 (ERB-C002-02), EX-C002-07/08 (ERB-C002-03), and every dependent capability's own Enterprise Experience consuming it as an Entry Context precondition (Contract 5.6).

This registration requires no governance decision beyond ordinary IRA/ADR process (mirroring `SCI-000001` through `RSC-000001`'s own registration pattern) and is not blocked by §9's Authorization Engine question — the object's own existence, shape, and lifecycle do not depend on how (or whether yet) a real Permitted/Denied determination is computed.

### 10.2 ADR Recommendations

1. **A registering ADR for Access Evaluation Outcome**, following the same pattern as `ADR-006`/`ADR-008`/`ADR-009`/`ADR-011`/`ADR-012`/`ADR-013` — a future, separately-scoped action, not performed by this IRA.
2. **No pattern-level ADR (no ADR-010 equivalent) is recommended** — §6 explains why: this is a single-object lifecycle, already the ordinary registration shape, not a multi-object pattern requiring separate recognition.
3. **A governance decision on Authorization Engine ownership is recommended as a prerequisite to any BA-01 implementation involving Permitted/Denied outcomes.** This assessment does not itself propose which of the following options is correct — that determination is a repository-owner/architecture-governance decision, consistent with CLAUDE.md §18's STOP-and-report discipline, not an assumption this IRA may fill:
   - **Option 1:** Charter the Authorization Engine (a URA-001-76 precedence resolver, including a `Group` model) as WP-05's own explicit scope, alongside C-002 — recognizing that, absent any other capability or Work Package claiming it, C-002's own Work Package may be the correct place to build it despite PE-001-C002 §1.5's Out-of-Scope framing, since no alternative owner currently exists in this repository.
   - **Option 2:** Charter the Authorization Engine as a separate, prior technical initiative (an RTA-001/IMP-001-owned Work Package of its own), with WP-05 deferred until it exists.
   - **Option 3:** Implement WP-05 to the disclosed minimum scope only (§9's Option A for BA-01: Unresolved/Deferred branches; BA-02, BA-03, BA-04 in full), explicitly declining Permitted/Denied until Option 1 or 2 is separately resolved, and recording the gap as a Governance Backlog Item (§10.3) rather than Technical Debt, per CLAUDE.md §19.8.5's own prohibition on deferring security defects as ordinary debt.

### 10.3 Governance Backlog Item (recorded, not resolved, by this assessment)

**Authorization Engine / URA-001-76 Precedence Resolver Ownership — no capability, Work Package, or governing document in this repository currently claims responsibility for building it**, despite RTA-001 §11.2 naming it "the sole authority for runtime authorization decisions" and PE-001-C002 §1.5 explicitly excluding it from C-002's own scope. This compounds a related, already-partially-disclosed gap: the `Group` construct URA-001-76's own precedence chain requires has no model anywhere in this repository. Mirrors the discipline of `IRA-003` §17 and `IRA-004` §17 — explicitly out of this IRA's own scope to resolve, not silently absorbed, not silently omitted.

### 10.4 Implementation Order (if WP-05 is authorized under §10.2 Option 3, the minimum-scope path)

1. Register Access Evaluation Outcome (§10.1/§10.2 item 1).
2. BA-01 (Option A minimum scope: Unresolved and Deferred branches only; Permitted/Denied explicitly not implemented and explicitly not stubbed).
3. BA-02 (Preserve and Bound) — first meaningful consumer of BA-01's produced records.
4. BA-04 (Hand-off Rejection Classification) — independent of BA-03, may proceed in parallel with it once BA-01/BA-02 exist.
5. BA-03 (Detect and Resolve Context Change) — its own re-resolution path inherits BA-01's Permitted/Denied gap, so its full scope remains bounded to the same minimum (Unresolved/Deferred re-resolution) until §10.2's governance decision resolves.

If WP-05 is authorized under §10.2 Option 1 (build the engine as part of WP-05), this order is superseded by a separate, future IRA addendum scoping that engine's own implementation — not fabricated here, consistent with CLAUDE.md §17's prohibition on inferring missing architecture.

### 10.5 Why Registration Is Recommended Regardless of the Blocker

Registering Access Evaluation Outcome now, independent of §9's unresolved question, mirrors WP-04's own precedent directly: `RSC-000001` (Resulting Structural Context) was registered and BA-08 implemented at Option A scope *before* its own downstream mechanism (ERG-001 structural mutation) existed, with the gap disclosed as `TD-070` rather than blocking the registration itself. The same reasoning applies here with one difference already stated in §10.2 item 3: because a wrong Permitted/Denied result is a security defect rather than an incomplete data-mutation record, the *disclosure vehicle* is a Governance Backlog Item requiring a decision, not an ordinary Technical Debt entry — but the registration itself is exactly as safe, and exactly as independently justified, as `RSC-000001`'s was.

---

## 11. Business Object Registration — Access Evaluation Outcome

**Trigger:** §5.1's own eligibility analysis found Access Evaluation Outcome independently identified, cross-experience-referenced, and governed by a real lifecycle — eligible for registration under CMD-001 §26.3/§26.4. This section performs that registration, per the same discipline `IRA-004` §21–§27 already established: registration precedes implementation, and registering this object does not depend on, or resolve, the Authorization Engine governance question recorded at §9/§10.2 item 3 — the object's own existence, shape, and lifecycle are independent of how (or whether yet) its Outcome Type value is computed.

**Governing decision:** `ADR-015_Access_Evaluation_Outcome_Canonical_Business_Object_Registration.md` records the governance decision authorizing this registration. CMD-001 remains **LOCKED** — this registration exercises CMD-001 §26.3's own existing registration mechanism; it does not amend CMD-001's text, rules, or structure.

### Registration Entry

| Attribute (CMD-001 §26.4) | Value |
|---|---|
| **Business Object Identifier** | `AEO-000001` |
| **Canonical Name** | Access Evaluation Outcome |
| **Business Description** | The scoped, temporally-bounded determination of whether a specific governed request is currently permitted. §1.16's own Context Model, verbatim: an Enterprise Experience context construct, "not a canonical domain state, not an EIO." §2.9 Experience Outcomes, verbatim: "A requester always knows whether a specific action is permitted, why, and for how long." Never authoritative in itself (§1.7) — always derived from Identity, Membership, Role, Permission, Delegation, Runtime Assignment, Organization, and Enterprise Scope facts consumed from their owning authorities via URA-001-76's precedence chain, executed by RTA-001's Authorization Engine. |
| **Business Domain** | Access Management (C-002) |
| **Aggregate Root** | Access Evaluation Outcome itself — per §5.2's own analysis, the four "Preserved/Superseded/Invalidated/Deferred" constructs §1.16 also names are this same object's own Validity Status, not separate objects requiring their own aggregate identity. |
| **Business Owner** | Pending Canonical Binding — unlike PE-001-C005 (which names a "Structural Steward"), PE-001-C002 names no dedicated business-owner or steward role anywhere in its text (confirmed by direct search); §1.11 states only that "every canonical Person-linked persona... participates in Access Management," which is a participation statement, not an ownership designation. |
| **Data Steward** | Pending Canonical Binding — same disclosed gap class as Business Owner; no steward role is named in PE-001-C002. |
| **Primary Data Category** | Transaction — a governed, per-request determination record, consistent with the classification convention every WP-04 Structural Context Lifecycle member already used for its own governed record. |
| **System of Record** | Pending — reserved for BA-01's own future implementation-readiness gap analysis, itself blocked pending §9/§10.2 item 3's governance decision. |
| **Lifecycle Model** | Two independent dimensions, both drawn directly from Chapter 9.7's own Context State Authority Matrix, not invented here: **Outcome Type** (fixed at creation) — PERMITTED / DENIED / UNRESOLVED / DEFERRED (BR-C002-02: exactly one of four, never conflated); and **Validity Status** — CREATED (ERB-C002-01) → PRESERVED (ERB-C002-02, within governed execution scope) → {SUPERSEDED (re-resolution reaches a different determination, or a Deferred outcome's Approval Authority concludes — EX-C002-01 Context Superseded, EX-C002-04 Context Superseded) \| INVALIDATED (context change requires re-evaluation before the execution continues — ERB-C002-03) \| EXPIRED (execution scope boundary reached — EX-C002-06)}. |
| **Versioning Policy** | Full history retained for audit and traceability — EX-C002-06's own Context Preserved field, verbatim: "The historical record of the expired outcome, for audit and traceability purposes." Superseded outcomes likewise "remain a valid historical record of what was current at [their] own time" (EX-C002-01 Context Superseded). |
| **Effective Dating** | Supported, but deliberately narrow — per URA-001-77 and Contract 5.4, validity is Object Scoped, Event Scoped, and Time Scoped to the single governed execution it was produced for; it is never dated across a session, Enterprise Journey, or Workspace by default (§1.17). |
| **Metadata Schema** | Pending — no implementation exists yet. |
| **Security Classification** | Internal (default classification for governed authorization-determination data) — not explicitly stated in PE-001-C002 itself; disclosed as a default assumption, not a textual citation, consistent with CLAUDE.md §17's requirement to distinguish stated fact from assumption. |
| **AI Context** | Contract 5.7, quoted exactly: "AI MAY explain why Access was permitted, denied, unresolved, or deferred; summarize the governing context; identify missing or conflicting Access context; identify that re-evaluation is required; and recommend a governed next step. AI SHALL NOT grant Access, deny Access, override an Access Evaluation Outcome, invent a Permission, infer Membership authority, infer a Role, manufacture a Delegation, manufacture a Runtime Assignment, rank Persons for Access, or otherwise alter the governing Access Evaluation Outcome." |
| **Status** | Draft — newly created registration entry; no separate CBOR-entry-approval governance step is defined anywhere in this repository. |

### Relationship Mapping (CMD-001 §26.5)

| Access Evaluation Outcome | Relationship | Target |
|---|---|---|
| Access Evaluation Outcome | `DERIVED_FROM` | Identity Context (C-001, consumed), Membership Context (C-007, consumed), Role/Permission/Delegation/Runtime Assignment facts (URA-001/C-003, referenced), Organization Context (C-004, referenced) — confirmed by ERB-C002-01's own Context Consumed field. |
| Access Evaluation Outcome | `PRECEDES` | Every dependent capability's own Enterprise Experience that consumes it as an Entry Context precondition (Contract 5.6, §2.5 Exit Context) — Pending Canonical Binding for the specific dependent-capability targets, since no PE-001-Cxxx exists yet for C-003, C-004, or C-008 to name precisely (mirroring PE-001-C002's own §1.9 disclosed pattern). |

### Business Activity Mapping (CMD-001 §26.6)

- **Produces:** BA-01 — Evaluate Access for a Governed Request (candidate identifier, Pending Canonical Binding per §3 of this IRA)
- **Consumes/Transitions:** BA-02 — Preserve and Bound Access Evaluation Outcome Validity; BA-03 — Detect and Resolve Access Context Change; BA-04 — Resolve Dependent Capability Access Hand-off Rejection (all candidate identifiers, Pending Canonical Binding)

### Governing References

- **Governing Business Activities:** BA-01 (create, all four Outcome Type branches), BA-02/BA-03/BA-04 (consume/transition) — candidates, Pending Canonical Binding.
- **Governing Enterprise Experiences:** EX-C002-01/02/03/04 (produce), EX-C002-05/06 (preserve/expire), EX-C002-07/08 (re-evaluate/classify).
- **Governing Business Rules:** BR-C002-01 (exclusive derivation from owning authorities), BR-C002-02 (four-outcome closed set), BR-C002-03 (scope/expiry), BR-C002-04 (mandatory re-resolution on context change), BR-C002-05 (hand-off-rejection classification).
- **Governing Contracts:** 5.1 (Access Context Authority), 5.2 (Access Evaluation Orchestration), 5.3 (Access Outcome Semantics), 5.4 (Access Scope and Validity), 5.5 (Access Re-evaluation and Context Change), 5.6 (Cross-Capability Access Hand-off).

### Explicitly Not Decided by This Registration

- **Physical Implementation Mapping (CMD-001 §26.7)** — Physical Tables, APIs, Events Published/Consumed, Reports, Search Indexes, Knowledge Graph Nodes, AI Embeddings: **all Pending.** No database table, migration, API, or code is authorized or implied by this registration.
- **Business Object Quality Score (CMD-001 §26.8)** — not scored.
- **Whether BA-01 is READY for implementation** — this registration resolves the *constitutional* eligibility question only. Per §9 of this IRA, BA-01's Permitted/Denied branches remain explicitly NOT READY pending the Authorization Engine governance decision (§10.2 item 3). This registration covers the record's own existence, shape, and lifecycle — not the mechanism that computes its Outcome Type value.
- **The specific dependent-capability Business Activities that will eventually consume this object** (Contract 5.6) — Pending Canonical Binding, since no PE-001-Cxxx exists yet for C-003, C-004, or C-008.

---

*End of IRA-005. Registration performed at §11 does not authorize implementation, does not resolve the Authorization Engine governance question (§9/§10.2 item 3), and does not amend CMD-001, which remains LOCKED. Do not begin WP-05 Business Activity implementation pending that governance decision.*
