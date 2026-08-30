# ROD — C-040 Blocker Closure Assessment

**Type:** Repository Owner Decision Brief / Implementation-Readiness Gap Analysis (decision-support artifact — decides nothing, authorizes no implementation)
**Arising from:** the Repository Owner's direction to stop meta-governance expansion, now that `AI-001` and `AI-002` are both executed, and determine exactly which remaining C-040 RED blockers are genuinely implementation-blocking versus safely deferrable.
**Prepared:** 2026-08-25
**Status:** Awaiting Repository Owner review. This brief authorizes no implementation, no ADR, no BA, no `tenant_registry` adoption.

---

## 1. Purpose

`IRA-C040_Tenant_Administration_Business_Function_and_Implementation_Readiness_Assessment.md` (re-read in full for this brief, not merely cited) found C-040 RED with five of seven readiness gates failing, four self-declared "Pending Canonical Binding" governance gaps, and zero canonical Business Activities — every one of the eight candidate BAs classified Category D under `IMP-001 §6.2b`. That assessment predates `ADR-024`–`ADR-033` and `AI-001`/`AI-002`. This brief re-examines every blocker `IRA-C040` named, against the now-current baseline, and classifies each precisely — not to declare C-040 GREEN, but to establish the minimum remaining closure path.

---

## 2. Baseline

Re-read directly for this brief: `IRA-C040` (full document, `architecture/05-Implementation/`); `ADR-024` through `ADR-033`; `AI-001`; `AI-002`; `ADR-002`; and the C-040 ROD sequence this conversation produced. `PE-001-C040`'s own content is relied upon exclusively through `IRA-C040`'s own exhaustive, citation-backed extraction of it (`IRA-C040` read the full `.docx` directly and quoted every material Business Rule, Invariant, and ERB) — this brief does not re-open the `.docx` itself, consistent with `IRA-C040`'s own already-thorough treatment and this task's own instruction not to modify it.

**Confirmed unchanged:** `tenant_registry` = DEFERRED. `PE-001-C040` document-synchronization debt = unaddressed (§14 of `IRA-C040`, non-blocking). C-040 Primary Specification = SD-002, unaffected.

**Confirmed changed since `IRA-C040`:** Tenant–Organization cardinality (`ADR-025` = 1:1, resolving `IRA-C040 §7`'s own "PENDING CANONICAL BINDING" finding, which predates it). Business Approval Authority and Infrastructure Allocation Authority both now constitutionally exist (`AI-001`, `AI-002`), resolving the *identity* half of `IRA-C040 §12`'s "Canonical Tenant identity/identifier-allocation authority" and the *provisioning* quarter of `IRA-C040 §13`'s four approval-authority gaps — but not their *mechanism* or *membership* halves (§3 below).

---

## 3. Blocker-by-Blocker Reassessment

### 1. Business Approval Authority

**Evidence:** `ADR-029 §10` (Canonization); `AI-001` (Key-2 appointment, executed).
**Why it does not block (as an identity question):** the constitutional authority now exists, with boundaries fixed and an executed appointment record.
**Why a residual gap remains:** `AI-001 §10` explicitly leaves membership, quorum, voting, chair, and tenure unpopulated — the authority exists but has no accountability point capable of actually deciding anything yet. This residual is item **7** below, not restated twice.
**Classification: D** — the authority-*identity* question `IRA-C040 §12`/`§18` item 1 named is resolved. (The membership/accountability-point question is separately tracked as item 7, classified A.)
**Artifact/action needed:** none, for identity. See item 7 for the remaining action.
**Repository Owner decision required:** No, for identity (already made). Yes, for item 7.
**New ADR required:** No.
**Dependencies:** None on other blockers for this item specifically.

### 2. Infrastructure Allocation Authority

**Evidence:** `ADR-029 §11` (Canonization); `AI-002` (Key-2 appointment, executed).
**Classification: D** — identical basis and reasoning to item 1, for this authority.
**Artifact/action needed:** none, for identity. See item 7.
**Repository Owner decision required:** No, for identity. Yes, for item 7.
**New ADR required:** No.
**Dependencies:** None on other blockers for this item specifically.

### 3. Technical Provisioning Authority

**Evidence:** `ADR-026 §13`, `AI-001 §10`, `AI-002 §10` — all three explicitly and consistently leave this untouched. `IRA-C040 §11`'s own CBAIP table classifies "Execution" as Undefined but ties this to the absence of a canonical Tenant object, not independently to Technical Provisioning specifically.
**Why it does not block a minimum-scope BA:** `ADR-026`'s own three-step model (Approval → Allocation → Provisioning) already treats Provisioning as a distinct, downstream, execution-layer concern separable from the constitutional decision/allocation steps — directly analogous to the already-formalized `CLAUDE.md §19.5` worked example (WP-04's own Option A minimum-scope precedent: produce the decision/context outcome, explicitly disclose the downstream mutation mechanism as deferred, rather than inventing it). A first Business Activity could be scoped to produce a "Resulting Tenant Administrative Context" recording an approved-and-allocated Tenant, with actual infrastructure provisioning explicitly out of scope and disclosed, mirroring that precedent exactly.
**Classification: B** — resolvable during implementation design (a TDS may explicitly bound/defer it, disclosed, not invented), not requiring a further Repository Owner constitutional decision before a minimum-scope BA can be charter-ready.
**Artifact/action needed:** an explicit scope-boundary statement in the eventual BA charter/TDS.
**Repository Owner decision required:** Only the scoping decision to charter a minimum-scope BA at all (§5 below) — not a separate Technical Provisioning decision.
**New ADR required:** No, for a minimum-scope BA. Possibly yes, later, if/when Technical Provisioning itself is formally designed — not now.
**Dependencies:** None blocking; downstream of BA charter scoping.

### 4. Tenant System-of-Record Custodianship

**Evidence:** `ADR-027 §11`/`§13.4`; `AI-001 §10`; `AI-002 §10` — all three explicitly state custodianship "is not assumed to travel with either authority" and remains unresolved.
**Why it is entangled with, but distinct from, item 5:** custodianship (who is *responsible for* the system of record) is a governance question; whether a system of record *exists at all* (item 5) is a prior, more fundamental question. Custodianship cannot be meaningfully assigned before something exists to be custodian *of*.
**Classification: B** — can be bounded during implementation design once item 5 is resolved (e.g., "the service implementing the adopted system of record is its de facto custodian until separately decided," disclosed as a minimum-scope choice) — does not independently require its own prior Repository Owner decision, though the Repository Owner may still choose to make one explicitly.
**Artifact/action needed:** an explicit disclosure in the eventual TDS, contingent on item 5's resolution.
**Repository Owner decision required:** Optional, not mandatory, if TDS-level disclosure is accepted instead.
**New ADR required:** No, unless the Repository Owner prefers to resolve it constitutionally rather than via disclosed TDS scoping.
**Dependencies:** Item 5 (must exist before custodianship is meaningful).

### 5. tenant_registry Status

**Evidence:** `IRA-C040 §8` Gate 3 — "❌ FAIL. Core entities are not defined as canonical Business Objects anywhere. Zero CBOR registration, zero Backend model, zero migration." `ADR-027 §13.1`/`§13.2` — the existing `tenant_registry` draft schema does not enforce `ADR-025`'s own 1:1 cardinality (no uniqueness constraint) and is not `SD-002 §2`-conformant (no versioning, no event-sourced lifecycle, no CBOR registration). `SER-001` SE-052 reaffirms DEFERRED status.
**Why it blocks:** this is `IRA-C040`'s own single most consequential finding — every implementation-layer CBAIP dimension (Persistence, Execution, Events) is Undefined specifically because no canonical Tenant object exists anywhere to persist to. Neither `AI-001` nor `AI-002` touches this — both explicitly prohibit themselves from adopting or modifying `tenant_registry`.
**Classification: A — must be resolved before C-040 can become Implementation Ready.** This is the one blocker this brief finds unambiguously in Category A, unresolved by anything in the `ADR-024`–`ADR-033`/`AI-001`/`AI-002` sequence, and structurally prior to items 4, 6, and 10.
**Artifact/action needed:** a Repository Owner decision on whether `tenant_registry` (remediated per `ADR-027 §13.1`/`§13.2`'s own disclosed gaps) or an alternative mechanism becomes the canonical Tenant system of record, followed by CBOR registration and, eventually, a migration — none of which is authorized by this brief.
**Repository Owner decision required:** Yes — this is the single decision this brief identifies as most load-bearing for the entire remaining closure path.
**New ADR required:** Likely yes, mirroring `ADR-003`'s own precedent for the analogous `TenantService` question, per `IRA-C040 §20`'s own recommendation.
**Dependencies:** None upstream; items 4, 6, and 10 all depend downstream on this one.

### 6. Tenant Approval/Allocation Workflow

**Evidence:** `ADR-029 §9` (three-stage sequence); `AI-001 §9`, `AI-002 §9` (each confirms its own authority is populated but exercises no function yet, since "no Tenant establishment request exists" for either).
**Why it does not require a further constitutional decision:** the *authorities* are now named (items 1–2); connecting them procedurally — how a request flows from intake through Approval to Allocation — is ordinary Business Activity/TDS design work, not a governance gap.
**Classification: B** — ordinary implementation-level design, to be performed once items 5 and 9 (system of record; request intake) are addressed.
**Artifact/action needed:** BA/TDS design.
**Repository Owner decision required:** No, beyond the BA-charter scoping decision already counted under item 5/§5 below.
**New ADR required:** No.
**Dependencies:** Items 5, 7, 9.

### 7. Authority Membership/Accountability-Point Mechanics

**Evidence:** `ADR-031 §9`–`§10` (membership/formation model); `AI-001 §10` (membership originally left `PENDING CANONICAL BINDING`, since resolved — see below); `AI-002 §10` (accountability point explicitly left unpopulated, still true).

**`AI-001` — Business Governance Authority:**
- Constitutionally established (`ADR-029 §10`, `AI-001`).
- **Populated.** One accountable human member, Ashit Padhi, appointed through `AI-003_Business_Governance_Authority_Accountable_Member_Appointment.md` — a further, genuinely independent Key-2 case, distinct from `AI-001`'s own founding act, that named the actual accountable individual per `ADR-035`'s minimum-membership structure.
- `AI-001` is therefore capable of having, and does have, a human accountability point. **This half of item 7 is CLOSED for membership/accountability population.**

**`AI-002` — Infrastructure Allocation Authority:**
- Constitutionally established (`ADR-029 §11`, `AI-002`).
- **Still unpopulated**, after twelve independent Key-2 cases across two candidates (full case history in `TD-157`, not restated here).
- **The Key-2 appointment mechanism remains valid and available** (`ADR-030`–`033`) and has already executed successfully twice, for `AI-001` and `AI-003`. **The problem is not a failure of the Key-2 mechanism** — it correctly produced twelve reasoned declines, never an invalid appointment.
- **Current blocker:** `AI-002` cannot currently be populated because no candidate has yet reached a successful independent Key-2 appointment. This is tracked as **`TD-157` — Open — BLOCKED.**

**Current evidence position, for the currently-tested candidate ("Sarika Rath"):**
- Candidate identity is established (an independently inspected LinkedIn reference confirmed the name).
- Substantive consent wording, when supplied, is adequate in content, if genuinely attributable to her.
- **The remaining issue is inspectable consent provenance** — whether such wording can be independently verified as actually hers, as distinct from being composed on her behalf within the same conversational channel as everything else in each case.
- Reachability remains a separate, currently untested consideration.
- A claimed WhatsApp screenshot was not available for inspection by the independent appointer and therefore cannot be treated as verified evidence.
- **This does NOT establish that Sarika Rath is ineligible** — no case has found a disqualifying constitutional rule against her.
- **This does NOT establish that no suitable second human exists in reality** — only that none is currently evidenced with sufficient inspectable provenance.
- **This does NOT establish that Key-2 is defective** — the mechanism remains sound and has already produced a valid appointment (`AI-003`).

**Critical distinction, preserved:** *"No suitable second human is currently evidenced with sufficient inspectable provenance"* is **not** equivalent to *"No suitable second human exists."* The repository can establish only the former. The Repository Owner may propose/designate a candidate for an independent Key-2 case; the Repository Owner does not itself perform Key 2. Every proposed candidate must be independently assessed through the established mechanism. Candidate identity evidence, candidate-originated consent/awareness, consent provenance, reachability, constitutional eligibility, and actual appointment execution remain separate questions, none collapsed into another.

**Evidence accumulated (summarized; full detail in `TD-157`, not reproduced here):** Ashit Padhi cannot currently occupy `AI-002` because he already occupies `AI-001` and the current one-seat-per-authority structure provides no recusal/alternate-decision mechanism. Repository-wide searches found no second human identity in canonical/repository evidence. The Rajeev/Rajeev Mendiratta cases did not result in appointment because the independent appointers found insufficient evidence at different stages (bare-name ambiguity, then absent independent corroboration, then absent candidate-originated consent/reachability). The Sarika Rath cases likewise did not result in appointment because no independently inspectable candidate-originated confirmation of awareness/consent/reachability was ever available across every form tested — a Repository Owner assertion of her agreement, a claimed message that proved uninspectable (twice), a fuller quoted statement whose provenance remained unverifiable, and a claimed WhatsApp screenshot that was never actually accessible to the appointer — none was treated as equivalent to her own independently-verifiable communication. **None of LinkedIn, git history, employment records, or WhatsApp is a mandatory constitutional requirement — each is a possible evidence source only**, per `ROD-C040-AI-002-Minimum-Human-Identity-and-Accountability-Evidence.md`. Candidate-originated consent/reachability is not a newly-adopted constitutional requirement either — it is an evidentiary consideration each independent appointer reasoned to from `ADR-029 §11`'s own active-decision-act requirements and `ADR-030 §8` condition 4's own diligence standard, case by case.

**AI membership:** the prior conclusion that ongoing AI membership is not evidence-supported under the current canonical framework (`ROD-C040-AI-Ongoing-Authority-Membership-Analysis.md`) is preserved and not reopened or redesigned here. AI remains execution/assistance support only, never the accountable constitutional decision-maker, for either C-040 authority.

**Why this is NOT a new governance gap requiring fresh meta-governance design:** the mechanism for populating `AI-002`'s seat already exists, already works (as `AI-001`/`AI-003` demonstrate), and remains available for further cases. What remains is identifying a candidate with sufficient identity-and-consent evidence, not designing a new mechanism.

**Classification: A — remains unresolved; must be resolved before `AI-002` can functionally act.** `AI-001`'s own half of this item is closed; `AI-002`'s is not.

**Artifact/action needed:** a further, genuinely independent Key-2 case for `AI-002`'s accountability point, once a candidate with sufficient durable identity attribution and independently-inspectable, candidate-originated consent/reachability evidence is identified — no new Appointment Instrument authored by this document, none created here.

**Repository Owner decision required:** Not to continue searching for or proposing a candidate — this requires no further governance decision. Would be required only to pursue the alternative resolution path (a dedicated future ADR changing the current separation-of-duties/single-accountability-point model) — not designed, proposed, or authorized here.

**New ADR required:** No, to continue pursuing a candidate. Would be required only for the alternative resolution path just described — not performed here.

**Dependencies:** None upstream (independent of item 5); items 6, 8, 9 depend downstream on this, specifically on `AI-002`'s own remaining half.

**Resolution paths, stated precisely, none pursued here:**
- **(A)** Obtain genuinely inspectable candidate-originated evidence and run another independent Key-2 case.
- **(B)** Identify another eligible human candidate and run a fresh independent Key-2 case.
- **(C)** Any constitutional/mechanism change (a per-request recusal/delegation mechanism, or an expanded membership structure) remains a separate future Repository Owner decision and is **not designed or authorized here.**

**Technical Debt Reference:** **`TD-157` — Open — BLOCKED** (`architecture/06-Reviews/TECH-DEBT.md`) is the current tracking artifact for this blocker, now refined to record the full twelve-case evidence history (eight evidence/attempt groupings) and the precise blocker wording above. **`TD-157` tracks the unresolved `AI-002` accountability-point blocker; it does not resolve it, and does not change this item's Classification A status.** The Key-2 mechanism itself remains sound and is not the blocker; AI ongoing membership remains prohibited and is not reopened; no recusal/delegation mechanism has been created; no membership structure has been changed; no second seat has been created; no governance institution has been created. The twelve declined cases narrow what closure would require — they do not themselves resolve the blocker. Full evidentiary basis: `ROD-C040-Infrastructure-Allocation-Authority-Key-2-Case-Outcome.md`, `ROD-C040-Infrastructure-Authority-Human-Candidate-Search.md`, `ROD-C040-AI-002-Second-Human-Candidate-Search.md`, `ROD-C040-AI-002-Rajeev-Candidate-Eligibility.md`, `ROD-C040-AI-002-Rajeev-Mendiratta-Candidate-Eligibility.md`, `ROD-C040-AI-002-Rajeev-Mendiratta-LinkedIn-Reference-Candidate-Eligibility.md`, `ROD-C040-AI-002-Minimum-Human-Identity-and-Accountability-Evidence.md`, `ROD-C040-AI-002-Rajeev-Mendiratta-Appointment-Case-Outcome.md`, `ROD-C040-AI-002-Sarika-Rath-Appointment-Case-Outcome.md`, `ROD-C040-AI-002-Sarika-Rath-Consent-Appointment-Case-Outcome.md`, `ROD-C040-AI-002-Sarika-Rath-Message-Verification-Case-Outcome.md`, `ROD-C040-AI-002-Sarika-Rath-LinkedIn-Reference-Appointment-Case-Outcome.md`, `ROD-C040-AI-002-Sarika-Rath-Second-Message-Verification-Case-Outcome.md`, `ROD-C040-AI-002-Sarika-Rath-Direct-Message-Appointment-Case-Outcome.md`, `ROD-C040-AI-002-Sarika-Rath-WhatsApp-Screenshot-Appointment-Case-Outcome.md`, `ROD-C040-AI-002-Sarika-Consent-Provenance-and-Evidence-Requirements.md`, and `AI-003_Business_Governance_Authority_Accountable_Member_Appointment.md`.

**C-040 status, restated for this item's own scope:** Remains RED — Not Implementation Ready. `AI-002`'s accountability point remains the outstanding authority-accountability blocker within this item. `tenant_registry` remediation, Technical Provisioning Authority, and a fresh IRA remain downstream/outstanding items exactly as already recorded elsewhere in this brief (items 4, 5, and §4) — unaffected by, and not resolved by, anything in this item.

### 8. Executor Relationships

**Evidence:** `ADR-029 §13` (explicit: "This ADR does **not** state that `AUREX_ADMIN` is the Business Approval Authority... does **not** state that `AUREX_ADMIN` is the Infrastructure Allocation Authority"); `AI-001 §10`, `AI-002 §10` (both leave executor unresolved).
**Why it does not require a prior Repository Owner decision:** each authority's own MAY list already permits it to "delegate execution without transferring the decision" — a minimum-scope TDS could simply have the appointed accountability point execute directly (no separate executor) as an explicit, disclosed v1 choice, deferring a distinct executor design to a later increment.
**Classification: B** — resolvable during implementation design, disclosed and bounded, not requiring further governance action first.
**Artifact/action needed:** an explicit disclosure in the eventual TDS.
**Repository Owner decision required:** No, if TDS-level disclosure is accepted.
**New ADR required:** No.
**Dependencies:** Item 7 (an accountability point must exist before "does it execute directly" is even askable).

### 9. Request-Intake Mechanism

**Evidence:** `IRA-C040 §11` — "Trigger: Defined (§4 EX-C040-04 through -08)" at the *experience* level; no API/intake mechanism exists at the *implementation* level (`IRA-C040 §15` item 11 — "UNDEFINED... explicitly Out of Scope by the specification itself").
**Classification: B** — ordinary TDS/API design work, correctly deferred by `PE-001-C040` itself to implementation, not a governance gap.
**Artifact/action needed:** TDS design, post-BA-charter.
**Repository Owner decision required:** No.
**New ADR required:** No.
**Dependencies:** Items 5, 7.

### 10. Tenant Identity Allocation Mechanism

**Evidence:** same as item 5 — the *technical* means of generating/recording a canonical Tenant identifier is inseparable from whatever system of record item 5 resolves.
**Classification: A**, entirely by inheritance from item 5 — this is not an independent gap, it is item 5's own downstream implementation-mechanics consequence, and cannot be resolved before item 5 is.
**Artifact/action needed:** none beyond item 5's own resolution.
**Repository Owner decision required:** Subsumed by item 5.
**New ADR required:** Subsumed by item 5.
**Dependencies:** Item 5, exclusively.

### 11. PE-001-C040 Document Synchronization Debt

**Evidence:** `IRA-C040 §14` — full Document Synchronization Debt Register, 15 locations classified (9 valid, 4 drift, 1 ambiguous, 1 maintenance-only). `IRA-C040 §15` item 3/18 — explicitly "Non-blocking for architecture; blocking for publication-readiness re-certification only."
**Classification: C — can remain unresolved without blocking implementation readiness**, exactly as `IRA-C040` itself already concluded. Not reopened or reassessed differently here.
**Artifact/action needed:** a future, separately-scoped document-maintenance pass (not a mechanical find-replace, per `IRA-C040 §14`'s own conclusion).
**Repository Owner decision required:** Only to authorize that future pass, whenever convenient — not gating.
**New ADR required:** No.
**Dependencies:** None.

### 12. Canonical Business Activities

**Evidence:** `IRA-C040 §10` — zero canonical BAs exist; all eight candidates classify Category D under `IMP-001 §6.2b`, because every execution path terminated at the same three constitutional gaps (BR-C040-15/03/13) `IRA-C040` itself named.
**Reassessment:** the specific gaps causing the Category-D classification are now substantially narrowed (identity resolved, cardinality resolved, provisioning-approval-authority resolved) — but a fresh `IMP-001 §6.2b` reclassification has not been performed, and `IMP-001 §6.2b`'s own explicit rule states a D→C reclassification does not, by itself, authorize implementation.
**Classification: A** — this is the outcome closure produces, not an independent input blocker with its own decision; it requires a fresh IRA re-assessment (§4 below) and a BA charter, both explicitly out of scope for this brief and for the entire `ADR-024`–`ADR-033`/`AI-001`/`AI-002` governance sequence.
**Artifact/action needed:** a fresh, dedicated IRA re-assessment (`CLAUDE.md §19.7`) once items 5/7 close, followed by BA charter.
**Repository Owner decision required:** Yes — authorization to commission the fresh IRA re-assessment, once items 5/7 are addressed.
**New ADR required:** No, for the reassessment itself.
**Dependencies:** Items 5, 7 (and, for full BR-C040-13 closure, item 16).

### 13. C-040 Contracts/Invariants/Business Rules

**Evidence:** `IRA-C040 §9` — "All 15 Business Rules (BR-C040-01 through -15) and all 17 Invariants (INV-C040-01 through -17) were read in full... None were manufactured for this assessment."
**Classification: D — already resolved/complete.** No gap found by `IRA-C040`, and nothing in this brief's own review finds a defect in that finding.
**Artifact/action needed:** none.
**Repository Owner decision required:** No.
**New ADR required:** No.
**Dependencies:** None.

### 14. Dependency on WP-16

**Evidence:** searched across this entire decision sequence (`ADR-024`–`ADR-033`, `AI-001`, `AI-002`, every C-040/meta-governance ROD) — `WP-16` is named only in explicit negative statements ("not created, not authorized") throughout.
**Classification: C** — no genuine dependency exists; WP numbering occurs at implementation-authorization time, downstream of readiness closure, not a prerequisite to it.
**Artifact/action needed:** none.
**Repository Owner decision required:** No.
**New ADR required:** No.
**Dependencies:** None.

### 15. Dependency on ADR-002

**Evidence:** `ADR-002` (Accepted, Option A) establishes `AUREX_ADMIN` as canonical, `PLATFORM_ADMIN` as legacy/interim, with the universal-bypass-semantics question left as its own separate follow-on (`ADR-002 §17a`). `AI-001`/`AI-002` both explicitly state they do not inherit `PLATFORM_ADMIN`'s bypass semantics.
**Classification: C** — no C-040 Business Activity or authority in this sequence requires the bypass-scope follow-on to be resolved first; it remains a separate, broader security/architecture question, correctly tracked independently and not gating C-040.
**Artifact/action needed:** none, for C-040 specifically.
**Repository Owner decision required:** No, for C-040. (The bypass-scope question itself remains open as its own separate matter, unaffected by this brief.)
**New ADR required:** No, for C-040.
**Dependencies:** None.

### 16. Remaining Constitutional/Cardinality/Authority Ambiguity

**Evidence:** cardinality — resolved (`ADR-025`). Business Approval/Infrastructure Allocation identity — resolved (`AI-001`/`AI-002`). **Newly and precisely surfaced by this brief:** `IRA-C040 §7`/`§13`'s own BR-C040-13 names **four** separate approval authorities — provisioning, migration, offboarding, and cross-tenant sharing. `ADR-026`'s own title ("Tenant Establishment Uses Dual...") and `ADR-029 §10`'s own scope (Business Approval for *establishment* specifically) confirm the entire `ADR-024`–`ADR-033`/`AI-001`/`AI-002` sequence addressed **only the provisioning/establishment quarter of BR-C040-13.** Migration approval authority, offboarding approval authority, and cross-tenant sharing approval authority (`TECH-DEBT.md` TD-040, already found Low-severity/non-blocking by `IRA-C040 §12`, since no sharing agreement currently exists to need one) remain **entirely untouched** by this entire session's own governance work.
**Classification: B** — resolvable via explicit scoping, not requiring three further full constitutional-authority sequences before a minimum-scope BA can proceed. A first BA can be chartered covering Tenant *establishment* only (already-resolved authorities), with migration, offboarding, and cross-tenant-sharing approval authority explicitly disclosed as out of scope for that first BA — directly mirroring the `CLAUDE.md §19.5` WP-04 Option A worked-example precedent this repository's own methodology already formalizes.
**Artifact/action needed:** an explicit scope-boundary disclosure in the eventual BA charter; separate future governance sequences (mirroring this entire one) for migration, offboarding, and cross-tenant-sharing approval authority, whenever those become active priorities.
**Repository Owner decision required:** Yes — the scoping decision to charter establishment-only first (counted once, under item 12/§5, not duplicated here).
**New ADR required:** No, for the scoping decision itself; yes, eventually, for each of the three remaining authorities, following this same session's own now-proven methodology.
**Dependencies:** None blocking a minimum-scope BA; blocks only a *full-scope* C-040 implementation covering all four BR-C040-13 authorities.

### 17. Other IMP-001-Methodology Blockers

**Evidence:** `IRA-C040 §16`'s own seven readiness gates — Gate 3 (Domain, FAIL — item 5), Gate 4 (Tenant, FAIL — resolved for cardinality/identity, open for system-of-record/membership), Gate 5 (Business Activities, FAIL — item 12), Gate 6 (Governance, FAIL — substantially narrowed, §4 below), Gate 7 (Implementation, FAIL — downstream of all the above). `IMP-001 §6.2b`'s own explicit rule that a D→C reclassification does not, by itself, authorize implementation (already cited under item 12).
**Classification:** not a single additional blocker — this item confirms no *methodological* requirement was missed by the sixteen items above; every one of `IRA-C040`'s own seven gates maps onto at least one already-classified item.
**Artifact/action needed:** the fresh IRA re-assessment already counted under item 12.
**Repository Owner decision required:** Subsumed by item 12.
**New ADR required:** None beyond what items 5/7/16 already name.
**Dependencies:** All of the above.

---

## 4. Dependency-Ordered C-040 Closure Plan

```text
1. Repository Owner decision: adopt (remediated) tenant_registry, or an
   alternative system-of-record mechanism, as C-040's canonical Tenant
   system of record.                                        [Item 5, 10]
        │
        ├──► CBOR registration + eventual schema/migration (implementation,
        │    not performed by any governance artifact in this sequence)
        │
        ▼
2. Repository Owner decision: Business Governance Authority's own
   membership structure (count, fixed vs. dynamic).                [Item 7]
        │
        ▼
3. Execute further Key-2 appointments (AI-003 for Business Governance
   Authority membership; AI-004 for Infrastructure Allocation Authority's
   own accountability point) — using the already-ratified Two-Key
   mechanism, no new ADR required.                                  [Item 7]
        │
        ▼
4. Repository Owner scoping decision: charter a minimum-scope first BA
   covering Tenant establishment only (Business Approval → Infrastructure
   Allocation), explicitly excluding Technical Provisioning, migration,
   offboarding, and cross-tenant-sharing approval authority as disclosed
   future scope.                                       [Items 3, 6, 8, 9, 16]
        │
        ▼
5. Fresh, dedicated IRA re-assessment (CLAUDE.md §19.7), re-running
   IMP-001 §6.2b's own A–E classification against the now-current
   baseline for the minimum-scope BA specifically.                [Item 12]
        │
        ▼
6. BA charter, TDS authoring, implementation authorization — none
   performed by this brief or any prior artifact in this sequence.
```

Items 11 (document sync), 14 (WP-16), and 15 (ADR-002 bypass scope) sit outside this critical path entirely — none blocks any step above.

---

## 5. Minimum Number of Remaining Decisions

**Three**, precisely:

1. `tenant_registry` adoption (or alternative) — the sole genuine architectural Category-A gap this brief finds.
2. Business Governance Authority membership structure.
3. Minimum-scope BA-charter scoping decision (establishment-only, disclosing Provisioning/migration/offboarding/sharing as future scope).

Every other open item either requires no further decision (resolved, Category D), is bounded via ordinary TDS disclosure (Category B, no Repository Owner action required), or is confirmed non-blocking (Category C).

---

## 6. Minimum Number of Remaining Governance Artifacts

- **One ADR** (tenant_registry adoption or alternative, mirroring `ADR-003`'s own `TenantService` precedent).
- **Two further Appointment Instruments** (`AI-003`, `AI-004`) for actual membership/accountability points, using the already-ratified mechanism — no new ADR required for these.
- **Zero further meta-governance ADRs** — `ADR-030`–`ADR-033`'s own mechanism is confirmed sufficient and is not reopened by this brief.

---

## 7. Minimum Implementation Artifacts Required Before a Fresh IRA

- Canonical Tenant system-of-record decision executed (CBOR registration; schema/migration need not be *complete*, but the *mechanism* must be canonically settled).
- Both authorities' membership/accountability points actually appointed (`AI-003`/`AI-004`).
- An explicit BA-charter scoping decision on record (even informally, prior to the fresh IRA itself, since the fresh IRA needs a defined scope to assess against).

No code, API, migration, or Business Activity implementation is required before the fresh IRA — the IRA re-assesses readiness against the now-resolved governance baseline, it does not require implementation to already exist.

---

## 8. What Can Now Stop Being Investigated

- **The meta-governance mechanism itself** (Two-Key Model, per-case eligibility, Key-1/Key-2 separation, Appointment Instrument form) — confirmed sufficient, twice-proven in practice (`AI-001`, `AI-002`), not reopened by this brief and not requiring further design work.
- **Tenant–Organization cardinality** — settled (`ADR-025`), not revisited by any item above.
- **Business Approval and Infrastructure Allocation authority *identity*** — settled (`AI-001`, `AI-002`), not revisited.
- **C-040's own Business Rules, Invariants, and Enterprise Response Behaviors** — confirmed complete by `IRA-C040` and not reopened here.
- **The `PE-001-C040` architecture-authority question (SD-002 vs. SD-001)** — settled by prior Repository Owner decision, `CAP-001` v1.6, not reopened.
- **Migration/offboarding/cross-tenant-sharing approval authority** — not abandoned, but confirmed non-blocking for a minimum-scope first BA (item 16) and can be set aside until that scope is actively pursued.
- **`ADR-002`'s own bypass-scope follow-on question** — confirmed non-blocking for C-040 specifically (item 15); tracked separately, not by C-040 work.

---

## 9. Explicit Non-Decisions

This brief does **not**:

- Create an ADR (the one identified as needed, `tenant_registry` adoption, is named but not drafted).
- Adopt, activate, or modify `tenant_registry`.
- Create code, schema, API, migration, or a Business Activity.
- Authorize `WP-16` or any Work Package.
- Modify `SD-002`, `URA-001`, `RTA-001`, `ARCH-000`, `CMD-001`, `CLAUDE.md`, `PE-001-C040`, or any existing ADR.
- Upgrade C-040's readiness status.
- Appoint any further authority members (`AI-003`/`AI-004` are named as needed, not created).
- Resolve migration, offboarding, or cross-tenant-sharing approval authority.

---

## 10. C-040 Status

**C-040 remains RED — Not Implementation Ready.** This brief substantially narrows the remaining path (from `IRA-C040`'s own four open governance gaps and 5-of-7 failing gates to three concrete remaining decisions), but resolves none of them itself.

---

## 11. Change Control

**Files created:** this document only — `architecture/06-Reviews/ROD-C040-Blocker-Closure-Assessment.md`.

**Files modified:** none. `IRA-C040`, `PE-001-C040`, `SD-002`, `ADR-024`–`ADR-033`, `AI-001`, `AI-002`, every prior `ROD-*` brief, `tenant_registry`, and `CLAUDE.md` were all read-only for this task. No code, migration, API, Business Activity, or Work Package was created or modified. No ADR was created. No authority members were appointed. `ADR-024`–`ADR-033` remain Accepted, unchanged. `tenant_registry` remains DEFERRED, unchanged. C-040 remains RED — Not Implementation Ready.
