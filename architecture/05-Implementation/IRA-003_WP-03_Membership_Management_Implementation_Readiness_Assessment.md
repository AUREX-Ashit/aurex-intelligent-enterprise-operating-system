# IRA-003 — WP-03 Implementation Readiness Assessment
### Membership Management (C-007)

**Status:** Approved — WP-03 READY (BA-01 only; BA-02 onward re-assessed per Business Activity, per the Business Activity Completion Gate, CLAUDE.md §19.7) — pending final sign-off per this document's own Completion Criteria (§20)
**Classification:** Implementation Readiness Assessment (canonical IRA template, per IRA-001/IRA-002)
**Work Package:** WP-03 — Membership Management (C-007), per `WPR-001_Work_Package_Roadmap.md`
**Governing capability specification:** `PE-001-C007_Membership_Management.docx` (extracted and reviewed in full, independently re-extracted twice during this readiness cycle to guard against stale recollection). Six canonical ERBs (ERB-C007-01 through -06). Thirteen Enterprise Experiences (EX-C007-01 through -13). Fourteen Business Rules (BR-C007-001 through -014). Ten Chapter 5 Contracts (5.1–5.10, corrected during Independent Review — see §6). Nine document chapters (Chapter 9 — Gold Standard Conformance Baseline — has no counterpart in PE-001-C003).
**Documents reviewed:** CLAUDE.md (§14, §16, §17, §19.1–§19.8), ARCH-000, CAP-001 (§2 Registry, C-007 entry: Primary Specification URA-001, Status Active), URA-001 (URA-001-15/16/17b/25/28/37/38/39/57/59/106/111 — Person/Identity/Membership/home-node/multi-role/group principles), ERG-001 (ERG-001-02, -03 — EnterpriseNode bounded context and Node-to-Membership Linkage, the graph-side half of the URA-001-17b joint fix), IMP-001 (§6 CBAIP — the pattern WP-03 will use; §13.17–13.25 Runtime Component Engineering — read in full and confirmed **not applicable**, see §9 below), Master Technical Architecture (AMD-011 changelog; `membership_registry`, `membership_business_role`, `membership_approval_authority`, `group_registry`, `group_membership`, `organization_node` DDL), WPR-001 (this Work Package's own roadmap entry), IRA-001/IRA-002 (precedent format and the BA-01-only implementation-scoping discipline both already established), IMP-REPORT-WP-01/IMP-REPORT-WP-02 (precedent Business Activity implementation pattern and Independent Review discipline), CERT-WP-01/CERT-WP-02 (precedent certification discipline and the self-certification prohibition this Work Package will also observe), TECH-DEBT.md (TD-016, TD-028 — both directly name a future "Membership Management work package" as their resolution path), current AuthService repository structure (`models/membership.py`, `repositories/membership_repository.py` — already exist, read-only; no service/router/schema/tests yet; `models/person.py`, `models/identity.py`, `routers/person.py` — C-006's own pre-governance-process implementation, consumed as a Legacy Baseline dependency per this Work Package's own governance observation, §16).

---

## 1. Scope

This IRA governs **WP-03 — Membership Management (C-007)**, per `WPR-001`'s authoritative roadmap. Following the identical discipline IRA-002 established for WP-02: this document derives the full Business Activity list for all six ERBs (§4), but **fully gap-analyzes and authorizes implementation of BA-01 only** ("Establish Membership Context"). BA-02 through the remainder of the list each require their own fresh gap analysis before implementation begins, per the Business Activity Completion Gate (CLAUDE.md §19.7) — exactly the precedent WP-02 followed successfully across all ten of its own Business Activities.

This IRA does not implement code, create a migration, or modify architecture. It is itself an assessment artifact.

---

## 2. Capability Summary

- **Primary Capability:** C-007 Membership Management (CAP-001 line 58) — Primary Specification **URA-001**, Status **Active**, Business Intent "Manage enterprise memberships" (verbatim).
- **Capability boundary, quoted verbatim (PE-001-C007 Chapter 1, reaffirmed at 1.4/1.8/5.9/5.10):** "C-007 does not grant or revoke Access." / "**C-007 does not assign or remove Roles or Permissions.**"
- **Runtime Execution Boundary:** Not directly touched. C-007 never evaluates or performs a runtime authorization decision — that remains RTA-001's Authorization Engine and C-002's exclusive concern, mirroring the boundary C-003 (WP-02) already established for itself.
- **Upstream Dependencies (consumed, never redefined):** C-006 (Authoritative Person Context — see §16, Governance Observation), C-004 (Organization Context — WP-01, closed), C-005/ERG-001 (structural/home-node validation, EnterpriseNode).
- **Downstream Consumers:** C-002 (Access Management, future), C-003 (Role & Permission Management, WP-02, closed — TD-028's own resolution depends on this Work Package producing real Membership-anchored dependents, though see §17's exclusion of `membership_business_role`/`membership_approval_authority` from this Work Package's own scope).
- **Explicitly excluded from this capability (verbatim, reaffirmed):** Role/Permission assignment, Access grant/revocation. Also excluded, confirmed independently against C-002's and C-003's own texts (§17): the assignment-join tables (`membership_business_role`, `membership_approval_authority`) that Master Technical Architecture specifies but no capability currently claims.

---

## 3. Enterprise Reference Blueprints (ERBs)

| ERB | Name | Purpose (verbatim, condensed) | Realizing EXs |
|---|---|---|---|
| ERB-C007-01 | Establish Membership Context | Recognize an existing Membership deterministically, or establish a new one, for a resolved Person and a valid Organization. | EX-C007-01, -02 |
| ERB-C007-02 | Understand Membership Context | Present a Membership's authoritative context, current authority consequence, and provenance for a business decision. | EX-C007-03 |
| ERB-C007-03 | Maintain Membership Terms | Resolve conflicting terms, change terms under governance, and reconfirm home-node structural congruence. | EX-C007-04, -05, -06 |
| ERB-C007-04 | Govern Membership Lifecycle | Transition a Membership's standing where the governing lifecycle authority permits it, and determine whether a routed non-active Membership may be reactivated, non-destructively. | EX-C007-07, -08 |
| ERB-C007-05 | Preserve Multi-Organization Membership Context | Surface and present a Person's Membership portfolio across Organizations under disciplined cross-tenant visibility. | EX-C007-09, -10 |
| ERB-C007-06 | Preserve Membership Context Across Enterprise Journeys and Hand Off to Dependent Capabilities | Carry resolved Membership context forward without re-establishment, and hand it off explicitly at the ownership boundary. | EX-C007-11, -12, -13 |

All six independently re-confirmed by fresh docx extraction during this readiness cycle (not carried from memory).

---

## 4. Business Activities (derived, mirroring IRA-002's ERB→EX→BA discipline — no canonical BA identifier exists in PE-001-C007 itself)

| BA | Business Activity | Type | Business Object | Governing ERB/EX | Status |
|---|---|---|---|---|---|
| **BA-01** | **Establish Membership Context** | Create | Membership | ERB-C007-01 / EX-C007-01, -02 | ✅ **Implemented under this IRA** |
| BA-02 | Understand Membership Context (read/view) | Query | Membership | ERB-C007-02 / EX-C007-03 | ⏳ Not started — first read-side EX either WP has implemented; see §17 |
| BA-03 | Maintain Membership Terms | Update | Membership | ERB-C007-03 / EX-C007-04, -05 | ⏳ Not started |
| BA-04 | Reconfirm Home-Node Structural Congruence | Update (validation) | Membership | ERB-C007-03 / EX-C007-06 | 🛑 **BLOCKED — External Capability Dependency (C-005).** Confirmed NOT collapsed into BA-03 (BA-03's own gap analysis, `IMP-REPORT-WP-03`). EX-C007-06's own Trigger requires a structural-change signal from C-005/ERG-001; C-005 is registered Active (CAP-001) but has no IRA, Work Package, or implementation anywhere in this repository (WPR-001 §2/§3), and no such signal producer exists in ERG-001, Master Technical Architecture, or the codebase. Full disposition recorded in `IMP-REPORT-WP-03`'s own "BA-04 — Readiness Assessment (CLOSED — BLOCKED)" section. Remains blocked pending C-005's own future charter. |
| BA-05 | Govern Membership Standing (Lifecycle Transition) | Update (state transition) | Membership | ERB-C007-04 / EX-C007-07 | 🛑 **BLOCKED — Governance Decision Required.** Contract 5.3 explicitly forbids C-007 from inventing a standing-transition matrix unless a canonical authority establishes one; none exists anywhere in this repository (URA-001-20 names states only; no ADR addresses it). Repository owner elected to defer BA-05 entirely rather than record a new ADR or implement a literal always-rejecting mechanism. Full disposition recorded in `IMP-REPORT-WP-03`'s own "BA-05 — Readiness Assessment (CLOSED — BLOCKED)" section. |
| BA-06 | Reactivate Membership | Update (state transition) | Membership | ERB-C007-04 / EX-C007-08 | ✅ **Implemented and independently reviewed.** Unlike BA-05, Contract 5.3's own "transition to active" sentence plus §6.3's dedicated "Reactivation not permitted by governing lifecycle authority" exception give an unambiguous, complete specification for today's canonical state: recognize the target Membership, always reject (Pending Canonical Binding), never mutate `membership_status` (BR-C007-014). Full disposition in `IMP-REPORT-WP-03`'s own BA-06 section. TD-036/037/038 registered. |
| BA-07 | Preserve Multi-Organization Membership Context | Query | Membership (collection) | ERB-C007-05 / EX-C007-09 | ⏳ Not started |
| BA-08 | Cross-Tenant Visibility Discipline | Query (governance) | Membership (collection) | ERB-C007-05 / EX-C007-10 | ⏳ Not started — may collapse into BA-07; confirm at that BA's own gap analysis |
| BA-09 | Preserve Membership Context Across Enterprise Journeys | Cross-cutting | Membership (context carry-forward) | ERB-C007-06 / EX-C007-11 | ⏳ Not started — governed by Contract 5.5 (§6); the earlier draft's citation of docx §9.6 as a collapse signal was imprecise (§9.6 concerns effective-date expiry, not EX-11/12 collapse) and is withdrawn — do not assume a collapse without direct confirmation at this BA's own gap analysis |
| BA-10 | Hand Off Membership Context to Dependent Capability | Update (classification) | Membership | ERB-C007-06 / EX-C007-12 | ⏳ Not started — governed by its own distinct Contract 5.10 (§6, found during Independent Review), not Contract 5.5 — this argues **against** collapsing BA-10 into BA-09/BA-11, since it has substantively distinct governing content (naming dependent capabilities, explicit accept/reject); confirm at its own gap analysis, do not assume either way |
| BA-11 | (EX-C007-13, if distinct from BA-09/10 after confirmation) | TBD | TBD | ERB-C007-06 / EX-C007-13 | ⏳ Not started — governed by Contract 5.5 (§6); genuinely undetermined whether distinct from BA-09 — requires direct EX-C007-13 text review at that BA's own gap analysis, not assumed here |

**Only BA-01 is fully gap-analyzed and authorized for implementation under this IRA.** The count above (10–11 candidate BAs) is a derivation aid, not a commitment — consistent with IRA-002's own explicit caveat that later BAs "each require their own gap analysis before implementation."

---

## 5. Business Rules (BR-C007-001 through -014)

**Methodology note, disclosed rather than glossed over:** PE-001-C007 does **not** provide an explicit EX↔BR citation anywhere in its own text — Chapter 4 (the thirteen EX blueprints) cites zero `BR-C007-` identifiers within any EX's own write-up, and Chapter 7.3 (the fourteen Business Rules) cites zero `EX-C007-` identifiers within any rule's own statement. Confirmed by direct, exhaustive search of both chapters' full text. **The single exception** is EX-C007-05's own Purpose text, which explicitly names three other EXs by identifier: "...it does not compute or assert the future authority consequence of that date being reached, which **EX-C007-03, EX-C007-11 and EX-C007-12** compute live whenever the Membership[...]" — this one sentence is the only literal, citation-based cross-reference the document provides, and it directly identifies BR-C007-013's governing EXs (below).

Every other row in the table below is therefore a **semantic match** — each BR's own statement matched against each EX's own Purpose/Trigger/Business Goal text (extracted in full, not summarized) — not a citation the document itself makes explicit. This is stated plainly so the mapping is not mistaken for a literal traceability citation it cannot honestly claim to be.

| BR | Statement (verbatim, Chapter 7.3) | Governing EX(s) | Basis |
|---|---|---|---|
| BR-C007-001 | A new Authoritative Membership Context SHALL NOT be established without a prior deterministic recognition lookup. | EX-C007-01, EX-C007-02 | Semantic — EX-02's own Trigger is "Recognition (EX-C007-01) confirms no existing Membership" |
| BR-C007-002 | A Candidate Home-Node Context SHALL NOT be treated as authoritative until explicitly confirmed. | EX-C007-02, EX-C007-06 | Semantic — EX-02 establishes the candidate; EX-06 is the dedicated confirmation/revalidation EX |
| BR-C007-003 | A conflict between requested and existing Membership terms SHALL be classified before it is resolved. | EX-C007-04 | Semantic — EX-04's own Purpose is verbatim "Classify the conflict and route to rejection or to a governed term change" |
| BR-C007-004 | A term change SHALL preserve the pre-change value. | EX-C007-05 | Semantic — EX-05's own Purpose is verbatim "Establish new authoritative terms while preserving prior terms" |
| BR-C007-005 | A standing transition SHALL be applied, and SHALL preserve the pre-transition standing and carry an explicit business reason, only where the governing Membership lifecycle authority permits transition from the current standing to the target standing. | EX-C007-07 | Semantic — near-verbatim overlap with EX-07's own Purpose text |
| BR-C007-006 | Membership terms SHALL remain unaffected by a standing transition, and standing SHALL remain unaffected by a term change. | EX-C007-05, EX-C007-07 | Semantic — the boundary rule between the two EXs that separately own terms (EX-05) and standing (EX-07) |
| BR-C007-007 | A home-node anchor SHALL only reference a node returned by C-005/ERG-001-03's current candidate lookup. | EX-C007-02, EX-C007-06 | Semantic — EX-02 sets the anchor at establishment; EX-06 is its dedicated revalidation EX |
| BR-C007-008 | An Organization SHALL receive, at most, an existence-only signal of a Person's Memberships elsewhere, absent an explicit cross-tenant sharing agreement. | EX-C007-09 | Semantic — EX-09's own Purpose is verbatim "Surface an existence-only signal to the establishing Organization, never detail" |
| BR-C007-009 | A Membership Subject SHALL be able to see the complete detail of their own Membership portfolio. | EX-C007-10 | Semantic — EX-10's own Purpose is verbatim "Present the complete portfolio across Organizations to its own subject" |
| BR-C007-010 | A hand-off to a dependent capability SHALL transfer only the required Membership context, SHALL always include the current Membership Authority Consequence Context, and SHALL record an explicit accepted or returned outcome. | EX-C007-12 | Semantic — EX-12's own Purpose is verbatim "Transfer bounded Membership context to the dependent capability and record the outcome" |
| BR-C007-011 | A downstream rejection of a hand-off SHALL NOT alter the underlying Authoritative Membership Context. | EX-C007-12 | Semantic — the rejection-handling half of the same hand-off EX as BR-010 |
| BR-C007-012 | AI-generated observations SHALL be distinguishable from authoritative Membership context at every point of use. | **All thirteen EXs** (cross-cutting) | Semantic — the rule's own text is "at every point of use," i.e. universal, not scoped to one EX; corresponds to Contract 5.9 (AI Assistance) |
| BR-C007-013 | The passage of an effective end date SHALL NOT be recorded as, or treated as, a standing transition; it SHALL produce only a recomputed Membership Authority Consequence Context. | EX-C007-03, EX-C007-11, EX-C007-12 | **Explicit textual citation** — EX-C007-05's own Purpose text names exactly these three EXs as the ones that "compute live" the authority consequence of an effective date being reached |
| BR-C007-014 | A reactivation SHALL NOT be applied where no canonical authority establishes that the current standing may transition to active; the outcome SHALL instead be explicit and unresolved or rejected. | EX-C007-08 | Semantic — near-verbatim overlap with EX-08's own Purpose text ("SHALL NOT itself assert or invent which source standings are eligible... records the determination as Pending Canonical Binding") |

**Reverse check — every EX has at least one governing BR:** EX-01 (BR-001), EX-02 (BR-001/002/007), EX-03 (BR-013), EX-04 (BR-003), EX-05 (BR-004/006), EX-06 (BR-002/007), EX-07 (BR-005/006), EX-08 (BR-014), EX-09 (BR-008), EX-10 (BR-009), EX-11 (BR-013), EX-12 (BR-010/011/013), EX-13 (BR-012, only via the universal AI-assistance rule — **no EX-specific BR governs EX-13**; recorded here rather than silently omitted). This is disclosed as a genuine finding, not resolved by inventing a rule the document doesn't state — EX-13's own Purpose ("Transfer the resulting Membership context to the next Enterprise Experience or Journey") is a pure continuation mechanic that Chapter 7.3 simply does not separately constrain beyond the universal AI-observation rule.

**BA-01's own governing subset (Establish Membership Context, ERB-C007-01/EX-C007-01–02):** BR-C007-001, BR-C007-002, and BR-C007-007 — all three confirmed above by direct semantic match against EX-01/EX-02's own text.

**BA-01's own governing subset:** BR-C007-001, BR-C007-002 (both directly govern Establish Membership Context) and, at the boundary, BR-C007-007 (home-node anchor validity — directly implicated by §9's `organization_node` finding).

---

## 6. Contracts (Chapter 5, 5.1–5.10)

**Correction, found during Independent Review of this IRA and independently re-verified before being applied:** this section originally claimed nine Contracts (5.1–5.9). Direct re-extraction confirms Chapter 5 contains **ten** Contracts — **Contract 5.10, "C-007 Cross-Capability Hand-off Contract,"** was missed in the original drafting pass. It is real, substantively distinct content (verbatim: "A hand-off SHALL name the specific dependent capability... and the specific Membership context transferred. A hand-off SHALL transfer only the context the dependent capability requires... A hand-off SHALL always include the Membership's current authority consequence, computed fresh... Acceptance or rejection SHALL be explicit...") and is the contract the docx's own Chapter 9.7 Context State Authority Matrix assigns to the Hand-off Context row — not Contract 5.5, which governs the separate, more general context-preservation act.

| Contract | Title | Disposition for WP-03 |
|---|---|---|
| 5.1 | C-007 Membership Context Contract | Governs BA-01 directly — "An Authoritative Membership Context SHALL exist independently of..." |
| 5.2 | Membership Terms & Home-Node Contract | Governs BA-03/BA-04 |
| 5.3 | Membership Lifecycle Contract | Governs BA-05/BA-06 |
| 5.4 | Multiple Membership & Cross-Tenant Visibility Contract | Governs BA-07/BA-08 |
| 5.5 | Context Preservation Contract | Governs BA-09 (EX-C007-11) and BA-11 (EX-C007-13) — the general "carry context forward without re-establishment" act |
| 5.6 | Navigation Contract | Cross-cutting; no dedicated BA — verify at implementation time whether this requires code or is satisfied by consistent routing conventions alone |
| 5.7 | Collaboration Contract | Cross-cutting; C-007's own text states "Most C-007 experiences are single-actor" — likely satisfied by absence for most BAs, mirroring WP-02's own Contract 5.8 disposition; confirm per-BA |
| 5.8 | Experience Consistency Contract | Cross-cutting; satisfied by construction if every BA reuses the same establish/update/audit/event pattern WP-01/WP-02 already proved |
| 5.9 | AI Assistance Contract | Same disposition as WP-02's Contract 5.8 — satisfied by absence unless a specific BA introduces an AI-assistance feature, which none currently does |
| **5.10** | **Cross-Capability Hand-off Contract** | **Governs BA-10 specifically (EX-C007-12)** — the hand-off-to-dependent-capability act itself (naming C-002/C-003/C-008, transferring only required context, explicit accept/return), distinct from 5.5's more general preservation act. BR-C007-010/011 both trace to this Contract, not to 5.5. |

**Every Contract has either an implementing BA (5.1–5.5, 5.10) or an explicit disposition recorded above (5.6–5.9) — this claim is now accurate; it was false in this section's original drafting, which silently omitted 5.10 entirely.**

---

## 7. Required Business Objects

- **Membership** — already exists (`models/membership.py`), requires extension (§9, §11).
- **EnterpriseNode / `organization_node`** — does not exist in AuthService. Canonically complete (ERG-001-02/03; Master Technical Architecture DDL) but not yet built. **This Work Package's first required build item — see §9.**
- **Person, Identity** — already exist (C-006's Legacy Baseline implementation — §16).
- **Organization** — already exists (WP-01, closed).

No new object type is required beyond these — unlike WP-02, which introduced five new authorization-policy object types, WP-03's Business Object surface is narrower: one primary object (Membership) plus one prerequisite anchor object (EnterpriseNode).

---

## 8. Existing Reusable Implementation (from WP-01 and WP-02)

| Component | Source | Reuse for WP-03 |
|---|---|---|
| `record_audit()` / `publish_event()` (`observability.py`) | WP-00/WP-01 | Direct reuse, no change |
| `BaseRepository[T]` | WP-00/WP-01 | Direct reuse for `MembershipRepository`'s new write methods |
| Tenant middleware pattern | WP-01 | Reuse as-is; confirm whether `/memberships` needs a tenant exemption (Memberships are Organization-scoped, unlike Roles — likely **not** exempt, unlike `/roles`/`/organizations`) |
| `require_platform_admin` | WP-01/WP-02 | Reuse as the same disclosed interim gate; inherits the same ADR-002-dependent limitation WP-02 already logged five times (TD-021–025) — not new debt |
| Establish→Version→Deprecate/Retire Business Activity shape (§6 CBAIP) | WP-01 (Organization lifecycle), WP-02 (BA-07/08) | Directly reusable for BA-01 (Establish) and BA-05/BA-06 (Govern Lifecycle/Reactivate) |
| `AuthorizationPolicyConflictService`-style single-shared-mechanism pattern | WP-02 (BA-09/BA-10) | Reusable as the template for BA-09/BA-10/BA-11's hand-off/context-preservation logic, if their own gap analysis confirms a comparable shape is needed |
| Pydantic schema pattern (`schemas/*.py`) | WP-01/WP-02 | Direct reuse |
| SQLite-in-memory test fixture (`tests/conftest.py`) | WP-00/WP-01/WP-02 | Direct reuse, no new test infrastructure |
| `MembershipRepository`'s three existing query methods (`get_active_membership`, `get_person_memberships`, `get_primary_membership`) | WP-00 (JWT/login support) | Direct starting point for BA-02 (Understand) and BA-07 (Multi-org) |

---

## 9. Architecture Validation

**Performed now, per this Work Package's own governance instruction, as the first architectural validation:**

- **`organization_node` / EnterpriseNode does not exist in AuthService** — confirmed by direct grep, zero matches anywhere in the codebase.
- **This is not a constitutional gap.** ERG-001-02 (Bounded Context Separation Within EnterpriseNode) and ERG-001-03 (Node-to-Membership Linkage — "the graph-side half of the joint fix with URA-001 v2.1... URA-001-17b now requires every Membership to declare a home node") fully specify this object. Master Technical Architecture's DDL for `organization_node` and `membership_registry.home_node_id UUID REFERENCES organization_node(node_id) NOT NULL` is complete and unambiguous.
- **Disposition:** this is a normal Implementation Gap (category C, per §10), not a Governance Decision or STOP condition. **BA-01's own gap analysis must resolve how `home_node_id` is satisfied** — either build a minimal `organization_node` table now, or adopt an explicitly disclosed interim simplification (e.g., a nullable `home_node_id` pending a fuller ERG-001 implementation), mirroring the precedent WP-01 (ADR-005) and WP-02 (multiple TDs) both already established for comparable simplifications. **This choice is not made here** — it is BA-01's own first implementation decision, to be disclosed in BA-01's own Business Activity Contract, not assumed by this readiness assessment.
- **IMP-001 §13.17–13.25 (Runtime Component Engineering) — confirmed not applicable.** Read in full. This specialization governs RTA-001's infrastructure Runtime Components (Metadata Runtime, Event Runtime, Authorization Runtime, Transaction Runtime, etc.) — a different class of implementable unit from a capability's own Business Activities (§6 CBAIP). C-007 is Business-Activity-shaped, identically to C-004 and C-003. **WP-03 requires no new Runtime Component** and will continue to rely on the same disclosed interim stand-ins (log-only observability, no real event bus) WP-01/WP-02 already used and disclosed (ADR-005, TD-018) — this is inherited, not newly introduced.

---

## 10. Gap Analysis (per Business Activity, category A–E)

| BA | Category | Reasoning |
|---|---|---|
| BA-01 — Establish Membership Context | **C** (Architecture requires completion — implementation-level) | `organization_node` build decision (§9); otherwise straightforward Establish-shape reuse |
| BA-02 — Understand Membership Context | **B** (Existing implementation can be reused) | `MembershipRepository`'s existing read methods are a direct starting point |
| BA-03/BA-04 — Maintain Terms / Home-Node Congruence | **B** | Extends `memberships` table fields; standard update pattern |
| BA-05/BA-06 — Govern Lifecycle / Reactivate | **B** | Mirrors WP-01's `activate()`/`suspend()`/`retire()` and WP-02's `deprecate()`/`retire()` directly |
| BA-07/BA-08 — Multi-Org / Cross-Tenant Visibility | **B** | `get_person_memberships()` is a direct starting point |
| BA-09/BA-11 — Context Preservation (Contract 5.5) | **B**, pending confirmation of whether these two collapse into one BA | Mirrors WP-02 BA-09/BA-10's shared-mechanism pattern |
| BA-10 — Hand-off (Contract 5.10, its own distinct governing contract) | **B** | Mirrors WP-02 BA-10's own shared-mechanism pattern; less likely to collapse with BA-09/11 given its distinct Contract |
| *(cross-cutting)* Role/Permission-assignment tables (`membership_business_role`, `membership_approval_authority`) | **D** (Governance clarification required) | **Explicitly excluded from WP-03's own scope** (§17) — recorded as a Governance Backlog Item, not absorbed here |
| *(cross-cutting)* C-006 dependency status | **D**, already resolved by governance instruction | Treated as Legacy Baseline (§16) — no retroactive IRA/certification required before WP-03 begins |

**No Business Activity meets category E (genuine STOP condition).**

---

## 11. Required Migrations

- **BA-01:** Extend `memberships` (add canonical fields per §9's resolved disposition — `membership_type`, `lifecycle_state` naming alignment; `home_node_id` per §9's build decision); create `organization_node` if that is the disposition selected. Single new migration, chained onto the existing head (`c3e9a5f7b2d4`), following the exact chaining discipline WP-01/WP-02 both used.
- **BA-02 onward:** None currently anticipated beyond BA-01's own migration — to be confirmed at each BA's own gap analysis, not assumed here.

---

## 12. Required APIs

- **BA-01:** `POST /memberships` (Establish) — not yet drafted; this IRA identifies it as the anticipated endpoint, per the same level of specificity IRA-002 §2.4 used for BA-01's own `POST /roles`. This IRA does not itself authorize drafting — that remains a separate approval step.
- **BA-02 onward:** Not enumerated here. Each later Business Activity's own specific endpoint shape (read, term-change, lifecycle-transition, multi-org, hand-off) is a decision for that Business Activity's own future gap analysis, mirroring IRA-002's own precedent of not speculating on BA-02 through BA-10's endpoint shapes in advance.

---

## 13. Required Repositories

- **BA-01:** Extend `MembershipRepository` with a `create()`-path method (currently read-only). Reuse `BaseRepository[Membership]`.
- **BA-02 onward:** No new repository class anticipated — extend the same `MembershipRepository`, mirroring how WP-02 extended one repository per object type rather than fragmenting logic.

---

## 14. Required Services

- **BA-01:** New `MembershipService` (does not exist today) — `establish()` following the identical existence-check → business-rule-check → mutate → audit → publish-event shape WP-01/WP-02 both used.
- **BA-02 onward:** Extend the same `MembershipService`, mirroring WP-02's single-service-per-object-type discipline.

---

## 15. Required Schemas

- **BA-01:** `schemas/membership.py` — `EstablishMembershipRequest`, `MembershipResponse`. Reuse the exact Pydantic pattern WP-01/WP-02 both used; no new validation framework.

---

## 16. Governance Observation — C-006 (Person Management) Dependency Status

Per explicit governance instruction already recorded in this readiness cycle: C-006's implementation (`routers/person.py`'s `/recognize` and `/establish` endpoints, `EX-C006-01`/`EX-C006-02`) predates the current IRA/IMP-REPORT/CERT governance process entirely (commit `34cf7fe`, 2026-07-20, one day before WP-00's own bootstrap commit `d5150ab`, 2026-07-21). It is implemented, tested (`test_person.py`), and committed. **C-006 is treated as a Legacy Baseline dependency**, consumable by WP-03 as-is, the same treatment WPR-001 already gives WP-00/WP-00A. **No retroactive IRA or certification is required before WP-03 begins.**

---

## 17. Governance Backlog Item — Membership-Role-Assignment Ownership (Explicitly Out of WP-03's Scope)

Independently re-confirmed twice during this readiness cycle, fresh from the docx both times: **"C-007 does not assign or remove Roles or Permissions"** (PE-001-C007, reaffirmed at §1.4/1.8/5.9/5.10). None of C-007's six ERBs (§3) mentions Role or Permission assignment. C-002's own docx confirms it "does not redefine" Membership, Role, Permission, Entitlement, Delegation, Runtime Assignment, Organization, or Workspace — it only consumes already-resolved facts. C-003's own IRA-002 excludes "Membership... ownership" from its scope.

**Conclusion: `membership_business_role`, `membership_approval_authority`, `group_registry`, and `group_membership` — though fully specified in Master Technical Architecture — are claimed by no capability's own governing text.** This is recorded here as a **Governance Backlog Item, explicitly outside WP-03's scope**, per direct instruction. It is **not** absorbed into this Work Package, not gap-analyzed for implementation here, and not assigned a BA number above. Resolution (which capability, if any, owns this) is a repository-owner/architecture-governance decision, to be raised separately — not invented, assumed, or silently resolved by this IRA.

---

## 18. Test Strategy

Same discipline as IRA-001 §2.10/IRA-002 §2.10: IMP-TEST-001 (Business Activity Contract tests) as the primary layer, IMP-TEST-002 (Authorization Boundary tests, constrained by the same `require_platform_admin` interim-gate disposition WP-02 already established). `test_membership_service.py` (unit) and `test_membership_api.py` (API/integration), using the existing `tests/conftest.py` SQLite-in-memory fixture — no new test infrastructure. BA-01's own test suite must additionally cover the `organization_node`/`home_node_id` disposition selected in §9, whichever it turns out to be.

---

## 19. Risks

| Risk | Severity | Mitigation |
|---|---|---|
| `organization_node`'s build-or-defer decision (§9) is made carelessly at BA-01 time, without disclosure | Medium | This IRA explicitly flags it as BA-01's first required decision, mirroring how IRA-001/IRA-002 both flagged comparable items in advance rather than letting them surface silently mid-implementation |
| The Role-assignment ownership gap (§17) is later mistaken for WP-03's own responsibility by a future reader | Low (given this document's explicit exclusion) | Recorded explicitly here and in WPR-001-adjacent governance notes; future IRAs should cite this section rather than re-discover the gap |
| BA-09/BA-11's EX-C007-11/13 inline-collapse question (§4) is assumed rather than confirmed | Low | Explicitly flagged as "not assumed here" in §4; must be resolved at that BA's own gap analysis, mirroring WP-02's own BA-06 precedent-setting decision process. BA-10 is a weaker collapse candidate given its own distinct governing Contract (5.10, §6). |
| The `memberships.role_id` legacy column (a single-role-per-membership shape, inconsistent with URA-001-37's multi-role requirement) is inadvertently touched by BA-01 | Low | BA-01 as scoped here only *extends* `memberships` with canonical fields; it does not touch `role_id`'s existing shape, and multi-role assignment is out of scope entirely per §17 |
| Same `PLATFORM_ADMIN`-only interim authorization gate WP-01/WP-02 both carried forward recurs a third time | Low (disclosed, consistent pattern) | Inherited, not new; will be logged as its own TD entry at BA-01's own Independent Review, exactly as WP-02 did five times (TD-021–025) |

---

## 20. Technical Debt Carried Forward

- **TD-016** (WP-01) — names "Role & Permission Management or Membership Management work package" as its resolution path. **Still open; WP-03 does not resolve it under BA-01** (it concerns AuthService's login flow, `authenticate_user()`, not Membership establishment) — to be revisited explicitly once a later WP-03 Business Activity reaches lifecycle/status territory, not assumed resolved by this IRA.
- **TD-028** (WP-02) — names `membership_approval_authority` as part of its resolution path. **Still open; explicitly not resolved by WP-03** per §17's own scope exclusion — TD-028 remains open after WP-03 closes, and this should be stated plainly in WP-03's own eventual completion report rather than implied closed.
- **ADR-002** (Proposed, not Accepted) — same unresolved authorization-catalog question WP-02 carried five times (TD-021–025); WP-03's own `require_platform_admin` reuse (§8) will inherit it identically, not newly.

---

## Completion Criteria

This IRA is complete when:
- BA-01 has a full Business Activity Contract per IMP-001 §6.7 (Business Intent, Input/Output Contract, Business Rules, Validation Rules, Authorization Rules, Domain Events, Audit Requirements, Tests) — **drafted at BA-01 implementation time, not here.**
- BR-C007-001, BR-C007-002, and (per §9's resolved disposition) BR-C007-007 are satisfied and tested.
- The `organization_node`/`home_node_id` disposition (§9) is explicitly disclosed, not silently assumed.
- No new database table, column, or architecture is invented beyond what §9 and §11 already scope.
- The Role-assignment ownership gap (§17) remains excluded from WP-03's own implementation and is not silently absorbed.
- ADR-002's live status and BA-01's own disposition relative to it are disclosed, mirroring IRA-002's own precedent exactly.

**Governing document status:** This IRA does not create any ADR or AMD, does not modify architecture, does not implement BA-01, and does not resolve ADR-002 or the Role-assignment ownership question. It records BA-01's scope, the one architectural decision BA-01 itself must make and disclose (§9), and the point at which each later Business Activity will require its own fresh gap analysis — exactly the discipline IRA-001 and IRA-002 both already established and CLAUDE.md §19.7 requires.
