# ROD-BAE-001 — TD-171 and M2 Consumption of BAR Registration — Decision Preparation

**Work Package:** `WP-BAE-001`, milestone M2. The subject is `TECH-DEBT.md` TD-171 (WP-23 A–C).
**Prepared:** 2026-09-30, by Repository Owner instruction ("Prepare the TD-171 Decision Package for M2"). Baseline HEAD: `d0102fb`.
**Status:** ~~**READY FOR DECISION — NO OPTION SELECTED.** A recommendation appears in §10. It is not a decision.~~ **DECIDED — TD-171 / M2 BAR CONSUMPTION** *(2026-09-30, Repository Owner; §17)*: **Option A.** TD-171 must be closed before M2 is authorized. **TD-171 remains OPEN**; remediation is still required.
- *(2026-09-30: the preparation in §1–§16 is preserved as the analysis presented for decision.)*

**Nothing is changed or authorized.**
- `TECH-DEBT.md`, BAR code, tests and migrations, the IRA, WP-BAE-001, WP-23, the ADRs and the Master Technical Architecture are unchanged.
- **M2 remains NOT AUTHORIZED / NOT STARTED. M2-P remains CHARTERED / NOT AUTHORIZED / NOT STARTED. TD-171 remains OPEN.**

---

## §1 Decision Statement

**TD-171 disposition for M2.** Before M2 authorization, one of two things must happen:
- TD-171 is remediated and closed; or
- the Repository Owner explicitly decides under what bounded conditions M2 may consume `bar_registration` while TD-171 remains open.

`IRA-BAE-001-M2 §16.H` and `ROD-BAE-001-M2 §0.5` already frame the question in those terms: "The Repository Owner must either close it or explicitly decide how M2 may proceed while it is open."

## §2 Current Status

*(2026-09-30: superseded by §17. The decision is recorded; the text below records the status at preparation.)*

**READY FOR DECISION.**
- TD-171 traces to reliable, consistent evidence (§4).
- The current wording agrees with its originating findings (one omission is noted in §4).
- No option requires changing BAR authority, reopening WP-23's delivered A–C scope, writing BAR from M2, or changing `ADR-043` or FO-2/FO-3.
- Options B and C would vary an accepted gate condition (§5). That is a Repository Owner act, not a stop condition.

## §3 TD-171: exact current statement (`TECH-DEBT.md`, HEAD `d0102fb`)

> **No enforcement links a registering act to a runtime BAR registration, and no reconciliation exists between `bar_registration` and `BAR-INDEX.md`** (WP-23 A–C; CERT-F-04, GAP-23-03-1/2).
> – `BarRegistrationService.register()` accepts any non-blank free-text `registering_act` and verifies it against no governance act.
> – It performs no caller-authority check; `actor_id` is optional; no router exists.
> – The service does not write `BAR-INDEX.md`, and no check compares the table with the index.
> Under RD-23-03 (layered authority model) a runtime row is **not** proof of governance authorization … Latent today: nothing consumes `bar_registration` and no non-test caller of `register()` exists. RD-23-03 §0.2 expressly does not authorize fixing it now. Severity **Medium** … **Hard precondition (Gate 1 / Gate 5 condition):** it becomes a governance and security boundary, fail-open, once anything reads `bar_registration` to decide execution eligibility.

**Category:** Security / Governance. **Priority:** High.
**Planned Resolution:** "**Must be closed before `bar_registration` is used to decide whether a Business Activity may execute** (Workstream E, **WP-BAE-001 M2** or any other execution-eligibility consumer), through a separately decided act-to-row enforcement and reconciliation mechanism. Not scheduled by this entry."
**Status:** Open. **Owner:** AuthService (Backend).

## §4 Origin and Evidence

| Step | Artifact | Content |
|---|---|---|
| 1. Gap found by the implementer | `ROD-WP-23-AC-BAR-Registry-Authority-Decision-Preparation.md §0.4` (RD-23-03, Option D, 2026-09-25) | **GAP-23-03-1:** "No enforcement links a registering act to a `bar_registration` row … Any in-process caller can create a runtime registration with no governance act. This is the Layer 2 'must not' risk." **GAP-23-03-2:** no table↔index reconciliation. (GAP-23-03-3, stale docstrings, was closed at Gate 3/4.) §0.2 does not authorize "adding governance-act validation" or "implementing Workstream E or WP-BAE-001 M2" |
| 2. Gate 1 (independent certification) | `CERT-WP-23-AC …` **CERT-F-04** (Medium) | Confirms GAP-23-03-1/2 at `services/bar_registration_service.py:100-134, 229-244`: "It becomes a security and authority boundary (fail-open for governance) **once Workstream E or BAE M2 reads `bar_registration` for eligibility**." Blocking: "No, if registered as TD **with the condition that it closes before any execution-eligibility consumer is built**" |
| 3. Gate 5 (release readiness) | `RRA-WP-23-AC …` **G5-08**; **G5-01**; condition **C-1** | G5-08: "It becomes a governance-authority, fail-open boundary once Workstream E or M2 reads the table for eligibility. The C-1 TD entry must carry a hard precondition that it closes before any such consumer is built, **and its severity must be assessed against `§19.8.7`'s High criterion ('weakens a security … boundary') at that point**." C-1: register it with the hard precondition |
| 4. Registration | `TECH-DEBT.md` TD-171 (C-1, completed 2026-09-28) | As §3 |
| 5. Acceptance carry-forward | `IRA-WP-23-AC …` (C-3 acceptance, lines 85, 312, 343) | "**TD-171's hard condition** carries forward: act-to-row enforcement and reconciliation must be in place **before `bar_registration` is used to decide whether a Business Activity may execute**." "TD-171 remains OPEN, with its hard execution-eligibility condition in force." |
| 6. B2 chain | `ROD-BAE-001-M2 …` §0.5; `ADR-043 §7`; `IRA-BAE-001-M2 §16.H`, §13.1, §13.9; FO-3 §16; RD-M2-07 and RD-M2-05 records | Each keeps TD-171 OPEN and separate. §16.H: "an implemented M2 would use `bar_registration` to decide whether a Business Activity proceeds. That is exactly the use TD-171's hard condition prohibits" |

**Consistency finding.**
- The TD-171 wording agrees with CERT-F-04, G5-08 and the acceptance record.
- **One omission:** G5-08 required that TD-171's "severity must be assessed against `§19.8.7`'s High criterion … at that point", meaning when a consumer is built. The TD-171 entry records "Severity Medium, as rated at Gate 1 and Gate 5" but does not carry the reassessment requirement.
- This is recorded here and **not** corrected (§14, OQ-171-4).

## §5 Remediation and History Since Opening

- **Not remediated.** No act-to-row enforcement or table↔index reconciliation exists. The `register()` semantics are unchanged since `b0f5a12`.
- **GAP-23-03-3 is closed** (docstrings, Gate 3/4). It is not part of TD-171.
- **Intentionally left open:** RD-23-03 §0.2, CERT-F-04 and G5-08 all defer it as debt, **conditionally**. The condition closes it before any execution-eligibility consumer is built.
- **Later B2 decisions assumed it stays open:** `ADR-043 §7`, FO-3 §16 (with the note that "FQ-2's eventual answer may inform TD-171"), RD-M2-07 (§3 F-9), RD-M2-05 (§21.4).
- **Exposure today, verified 2026-09-30:**
  - there is no non-test caller of `BarRegistrationService.register()` or of `BarRegistrationService` in AuthService (the `.register(` hit in `dependencies.py:140` is an unrelated `ResolverRegistry`);
  - no migration or script seeds `bar_registration`;
  - `BAR-INDEX.md` has zero registrations;
  - no router exposes registration;
  - nothing reads `bar_registration` outside BAR's own service and tests.

## §6 Existing BAR Authority Model (RD-23-03 Option D, decided)

| Layer | Record | Must not |
|---|---|---|
| 1. Governance registration authority | Registering act | — |
| 2. Runtime execution registration | `bar_registration`, "the runtime source queried by execution-time BAR logic" | **Be treated, by the existence of a row alone, as proof that the underlying governance authorization exists** |
| 3. Catalogue | `BAR-INDEX.md` | Serve as the runtime lookup |
| 4. Reconciliation | Governance ↔ runtime stay traceably related | The mechanism is **not** decided |

TD-171 is the absence of the Layer 1 → Layer 2 link and of the Layer 4 mechanism.

## §7 Exact M2 → BAR Interaction (approved design; not implemented)

- **Stage 2b** (FO-2 §16.B, §16.E): `RegistrationSource.lookup(identifier)` → host adapter → `BarRegistrationRepository.get_by_identifier` (a plain `SELECT`, `repositories/bar_registration_repository.py:36-38`).
- **Consequence:** `NOT_REGISTERED` gives `ACTIVITY_NOT_REGISTERED`, and resolution **terminates**. `REGISTERED` proceeds to the binding lookup (2c).
- M2 never writes BAR, never registers, and never infers registration from any other source.
- M2 never invokes (M5). In M2, stage 5 onward stays `NOT_IMPLEMENTED`, AuthService exposes no BAE execution path, and the first real consumer is M7 (Charter §10).

## §8 Dependency Analysis

| Concern | TD-171 relevance | Finding |
|---|---|---|
| **A. BAR identity/authority** (D2, D5; ledger) | None | Identifier issuance is unaffected. TD-171 does not concern identity allocation |
| **B. BAR registration write path** (`register()`) | **Direct: this is where the defect is** | Any in-process caller can create a Layer 2 row with an unverified act and no authority check |
| **C. BAR registration read path** (`get_by_identifier`) | **Consequential** | The read is correct as code. But M2's use of it **treats row existence as execution eligibility**, which is exactly the Layer 2 "must not" and the CERT-F-04/G5-08 trigger. The defect in B becomes fail-open **through** C |
| **D. BAE resolution** (stage 2b) | **Direct consumer** | M2 is an "execution-eligibility consumer" in the sense of CERT-F-04 ("BAE M2"), G5-08 ("M2") and TD-171 ("WP-BAE-001 M2"): its 2b outcome decides whether resolution proceeds. Read-only does **not** neutralize the risk, because the risk lies in trusting what was written |
| **E. Binding-store authority** (B2, M2-P) | None | A separate record with a separate write path (FQ-1 (c)) and CI act verification (FQ-2 (a)). FO-3 act-to-row enforcement is not TD-171 (FO-3 §16) |
| **F. M2 execution** | **Latent in M2** | M2 never executes (RD-M2-06; M5). The fail-open outcome, an unauthorized row allowing execution, needs an execution path, which does not exist until M5/M7. But the gate itself is built in M2 |

**Answer to the critical question.** TD-171 **is** relevant to M2's read of `bar_registration`. The defect is on the write side (B), but the originating evidence places the trigger at the moment an eligibility consumer reads the table (C → D), and names M2. M2's read is therefore not outside TD-171's boundary. What M2 does **not** do is execute (F). That is the only fact on which a bounded alternative (Option C) could rest.

## §9 Candidate Decision Options

| | **A: close TD-171 before M2 authorization** | **B: M2 proceeds, TD-171 stays open, unconditionally (read-only contract only)** | **C: conditional. M2 may be implemented while TD-171 is open; closure moves to before any execution path** |
|---|---|---|---|
| Summary | A separately decided act-to-row enforcement and reconciliation mechanism is designed, implemented and independently verified, and TD-171 closed, before M2 is authorized | M2 reads `bar_registration` under the §7 read-only contract; TD-171 is deferred with no new trigger | M2 builds stage 2b, but TD-171 must close **before** any of: M5 invocation; any router or invoker that runs a BAE-resolved activity; the first real `bar_registration` row used by the BAE (to be fixed by the RO; OQ-171-3) |
| Consistency with evidence | **Fully consistent** with CERT-F-04, G5-08, C-1, the acceptance record, TD-171, `IRA §16.H` and `ROD-BAE-001-M2 §0.5` | **Contradicts** CERT-F-04 ("closes before any execution-eligibility consumer is **built**"), G5-08 and TD-171's Planned Resolution, which names M2. It also ignores G5-08's High reassessment (`§19.8.7` → `§19.8.5`: security defects are not deferrable) | **Varies** the accepted condition's trigger from "consumer built" to "execution path exists". It is anchored in §8 F. It still needs G5-08's severity reassessment |
| Architectural consequence | None. RD-23-03 Layers 1–4 are completed on the BAR side | Layer 2 "must not" is violated once M2 is live | Layer 2 risk is latent in M2 and must close before execution |
| Implementation consequence | BAR-side work (act-to-row enforcement, reconciliation) under BAR's owner (WP-23, which remains OPEN, D–H not implemented), with its own design, decision and five-gate verification. The mechanism is **not decided** (TD-171: "separately decided") | None beyond M2 | M2 as designed, plus a guard that no execution path is added. TD-171 work before M5/M7 |
| Governance consequence | M2 authorization waits on TD-171 closure. No gate condition is varied | Gate 1/5 conditions and the WP-23 acceptance carry-forward are overridden. Needs an RO decision **and** a TD-171 Planned Resolution amendment | An RO decision varying the CERT-F-04/G5-08/C-1 trigger, the TD-171 Planned Resolution amendment (separately authorized), and a G5-08 severity reassessment recorded |
| Security/control consequence | Closed before any consumer exists | **Fail-open governance boundary** once any caller writes a row | No execution exposure in M2. The risk carries to the execution trigger |
| Impact on §13 | §13.1 TD-171 box satisfied by closure. §13.5 A "TD-171 closure". No scope change | §13.1 box satisfied by decision. §13.9's "TD-171 boundary violated" stop needs redefinition | §13.1 box satisfied by decision. New §13.8/§13.9 entries: no execution path; TD-171 closure before M5/M7. §13.5 dependency moved |
| New ADR/ROD | A decision record (this ROD); a separate design/decision for the TD-171 mechanism. ADR not required by an existing rule (RD-23-03 §0.3 precedent) | Decision record here; ADR not required by rule | Decision record here; ADR not required by rule; RO may elect one given the varied gate condition |

No other option is supported by repository evidence. "Reinterpret stage 2b as not an eligibility decision" is excluded: it contradicts `§16.H` and the gate findings.

## §10 Recommended Option (not a decision)

*(2026-09-30: the Repository Owner selected Option A; §17.1.)*

**Option A** is recommended.
- It is the only option consistent, without variation, with the accepted Gate 1 and Gate 5 conditions, the WP-23 A–C acceptance carry-forward and TD-171's own Planned Resolution, all of which name M2.
- G5-08 requires severity reassessment against the High criterion ("weakens a security … boundary") when a consumer is built. On that reassessment, the defect is a candidate `§19.8.5` non-deferrable security defect, which technical-debt deferral cannot carry.

**Option C** is the only governed alternative if the Repository Owner prefers to proceed with M2 first. It is anchored in the fact that M2 never executes. It requires:
- an explicit variation of the accepted trigger;
- the G5-08 reassessment recorded;
- a TD-171 Planned Resolution amendment;
- the §12 controls.

**Option B is not recommended.** It overrides accepted gate conditions with no compensating control.

## §11 Impact on B2 §13 (not edited)

| §13 item | A | C |
|---|---|---|
| §13.1 TD-171 box | Ticked on independent verification of closure | Ticked on the RO decision, with conditions |
| §13.5 A | "TD-171 closure" (BAR-side, WP-23 owner) | "TD-171 closure before execution trigger" |
| §13.8 | Unchanged | Add: no router, invoker or execution path for BAE-resolved activities; no M5 work |
| §13.9 | "TD-171 boundary violated" stays | Redefined: any execution path appearing before TD-171 closure |
| §13.2 scope | Unchanged | Unchanged |

## §12 Required Controls / Acceptance Conditions

**Under every option** (already in the approved design):
- M2 never writes or registers BAR (§13.8);
- M2 never infers registration from another source;
- `get_by_identifier` is the only BAR read;
- failures raise, and are never converted to "registered";
- BAR stays the canonical authority.

**Additionally under A:**
- a separately decided act-to-row enforcement and reconciliation mechanism, owned by BAR (WP-23);
- implemented and independently verified (`§19.7b`, with negative controls);
- TD-171 closed in `TECH-DEBT.md` by separate authorization.

**Additionally under C:**
1. The G5-08 severity reassessment is recorded.
2. The TD-171 Planned Resolution is amended, by separate authorization, to the RO-fixed trigger.
3. §13.8 and §13.9 are extended as in §11.
4. An independent reviewer verifies at M2 acceptance that no execution path exists.
5. TD-171 closes before the trigger. M5/M7 authorization cannot be requested while it is open.

## §13 Traceability

| Source | Used for |
|---|---|
| `TECH-DEBT.md` TD-171 (and TD-165, TD-170, TD-176 as context; unaffected) | §3 |
| `ROD-WP-23-AC …` §0.1, §0.2, §0.4 (RD-23-03) | §4, §6 |
| `CERT-WP-23-AC …` CERT-F-04 | §4, §9 |
| `RRA-WP-23-AC …` G5-01, G5-08, C-1 | §4, §9, §10 |
| `IRA-WP-23-AC …` C-3 acceptance (TD-171 carry-forward) | §4, §9 |
| `services/bar_registration_service.py`, `repositories/bar_registration_repository.py:36-38` | §5, §7, §8 |
| `ROD-BAE-001-M2 …` §0.5; `ADR-043 §7`; `IRA-BAE-001-M2` §13.1, §13.5, §13.8, §13.9, §16.B, §16.E, §16.H | §1, §7, §8, §11 |
| FO-3 §16; RD-M2-07 (§3 F-9); RD-M2-05 (§21.4) | §5, §8 E |
| `WP-BAE-001` Charter §10 (M5, M7) | §7, §8 F |
| `CLAUDE.md` §19.7b, §19.8.5, §19.8.7 | §9, §10, §12 |

## §14 Open Questions for the Repository Owner

*(2026-09-30: all five are decided; §17. The table is preserved as presented.)*

| ID | Question | Evidenced options |
|---|---|---|
| **OQ-171-1** | TD-171 disposition for M2 | A (recommended), B, C (§9) |
| **OQ-171-2** | Under A: who designs and delivers the act-to-row enforcement and reconciliation mechanism? | TD-171 says "separately decided" and "not scheduled". BAR's owner is WP-23 (OPEN). No workstream or mechanism is decided. FQ-2's CI-citation approach "may inform" it (FO-3 §16) |
| **OQ-171-3** | Under C: the exact trigger replacing "consumer built" | Before M5 invocation work; before any execution path or router; before the first real `bar_registration` row consumed by the BAE; or a combination |
| **OQ-171-4** | Record now the G5-08 severity reassessment ("assessed against `§19.8.7`'s High criterion … at that point"), which the TD-171 entry omits? | Reassess now (High, `§19.8.5` implications), or defer reassessment to the trigger point (C only) |
| **OQ-171-5** | Authorize a `TECH-DEBT.md` amendment to record the outcome (A: closure path; C: amended Planned Resolution and severity)? | Yes, as a separate governance task, or no |

## §15 Decision Readiness Statement

~~**READY FOR DECISION — NO OPTION SELECTED.**~~ *(2026-09-30: **DECIDED**, Option A; §17.)*
- **TD-171 must be closed before M2 under the current accepted conditions** (Option A).
- M2 may proceed while it is open **only** if the Repository Owner explicitly varies those conditions (Option C, with §12 controls).
- This package does not do so.

**M2 remains NOT AUTHORIZED / NOT STARTED. M2-P remains CHARTERED / NOT AUTHORIZED / NOT STARTED. TD-171 remains OPEN.**

## §16 Evidence Inventory

| Evidence | Location |
|---|---|
| TD-171 entry | `architecture/06-Reviews/TECH-DEBT.md` (HEAD `d0102fb`) |
| RD-23-03 decision, GAP-23-03-1/2/3 | `architecture/06-Reviews/ROD-WP-23-AC-BAR-Registry-Authority-Decision-Preparation.md` §0 |
| CERT-F-04 | `architecture/06-Reviews/CERT-WP-23-AC_BAR_Workstreams_A-C.md` (finding table) |
| G5-01, G5-08, C-1 | `architecture/06-Reviews/RRA-WP-23-AC_BAR_Workstreams_A-C_Release_Readiness_Audit.md` |
| Acceptance carry-forward | `architecture/06-Reviews/IRA-WP-23-AC_BAR_Workstreams_A-C_Closure_Readiness.md` (lines 85, 312, 343) |
| BAR write path | `Backend/Services/AuthService/services/bar_registration_service.py` (`register`) |
| BAR read path | `Backend/Services/AuthService/repositories/bar_registration_repository.py:36-38` |
| No non-test caller; no seeded rows | Repository search, 2026-09-30 (§5) |
| Zero registrations | `architecture/00-Governance/BAR-INDEX.md` |
| M2 design | `IRA-BAE-001-M2` §13, §16.B, §16.E, §16.H (`66f0aed`, `3303237`, `d0102fb`) |
| B2 records | `ADR-043`; `TDS-BAE-001-M2-FO3 …` §16; `ROD-BAE-001-M2-Binding-Infrastructure-Ownership …` §11; `ROD-BAE-001-RD-M2-05 …` §21 |

## §17 Repository Owner Decision Record (2026-09-30)

**Recorded** by direct Repository Owner instruction ("Record the Repository Owner decision for TD-171"). Each decision is recorded as stated and is not reinterpreted.

**Governance only.** No TD-171 remediation, BAR code, test, migration or `BAR-INDEX.md` change. No M2 or M2-P work, `bae_integration/`, `main.py` or CI change. No `TECH-DEBT.md`, IRA, WP-BAE-001 or WP-23 change. No ADR.

### 17.1 Decisions

| OQ | Selected | Decision (as recorded) | Rationale | Implementation / governance consequence | Out of scope |
|---|---|---|---|---|---|
| **OQ-171-1** Disposition | **Option A** | **TD-171 must be closed before M2 is authorized.**<br>– M2 may not be authorized while TD-171 remains OPEN.<br>– No special exception is created for M2.<br>– Option B is **rejected**: it would override accepted WP-23 conditions without a compensating control.<br>– Option C is **not selected** | It preserves the existing WP-23 Gate 1/Gate 5 condition (CERT-F-04, G5-08, C-1) and the A–C acceptance carry-forward. M2's read-only BAR contract does not compensate for an untrusted BAR registration write path (§8 C–D) | The §13.1 TD-171 box can be satisfied only by independently verified closure of TD-171. M2 authorization cannot be requested before then | Any exception, variation or deferred trigger for M2 |
| **OQ-171-2** Enforcement ownership | **BAR / WP-23** | BAR (WP-23) owns the design and delivery of the TD-171 enforcement and reconciliation mechanism. TD-171 is a **BAR governance/control defect, not an M2 defect**. It must **not** be solved by adding compensating governance logic to BAE M2. The mechanism must establish a trustworthy relationship between the governing act and the BAR registration row, and must address the `BAR-INDEX.md` reconciliation gap TD-171 identifies | TD-171 is the missing link between RD-23-03 Layer 1 and Layer 2, plus the missing Layer 4 (§6), on BAR's write path (§8 B) | A future **WP-23-specific decision/design package** must define the mechanism. FO-3's governing-act/CI-citation approach (FQ-2 (a)) may be considered as evidence or input only; it is **not adopted** as the TD-171 implementation | Selecting the technical mechanism; any BAE-side compensation |
| **OQ-171-3** Trigger | **None: no deferred trigger** | Because Option A is selected, TD-171 closure is a prerequisite to **M2 authorization**. "Before M5", "before an execution path" and "before the first real BAR row" are **not** sufficient. M2 cannot receive implementation authorization while TD-171 is OPEN | It follows from OQ-171-1 | §13's TD-171 prerequisite stays a hard authorization gate | Any trigger later than M2 authorization |
| **OQ-171-4** G5-08 severity reassessment | **Yes, the requirement is recorded** | G5-08's requirement to reassess TD-171's severity against the `§19.8.7` High criterion **when an execution-eligibility consumer is built** is preserved. The reassessment is **not performed now**. It must occur at the applicable future gate, after the relevant consumer exists. **No new severity is assigned now** | It keeps the Gate 5 requirement (§4 omission finding) without inventing a rating | The current debt state (Severity Medium, Priority High, Open) is unchanged. The future reassessment is a separate, later obligation | Performing the reassessment; assigning a severity |
| **OQ-171-5** `TECH-DEBT.md` | **Yes in principle; no change now** | A separately authorized governance synchronization should later update `TECH-DEBT.md` to reflect this decision and the G5-08 reassessment requirement. **This ROD is the authoritative decision record for now** | Mutating the register was not authorized in this task (`§19.8.2` still applies) | A future synchronization task | Any `TECH-DEBT.md` change now |

### 17.2 Resulting responsibilities

| Area | Responsibility |
|---|---|
| **BAR / WP-23** | Owns TD-171 remediation; the governing-act-to-registration control mechanism; `BAR-INDEX.md` reconciliation. Through a future WP-23-specific decision/design package |
| **BAE M2** | Remains a read-only consumer. Must not write or register BAR. Must not compensate for an untrusted BAR write path. **Cannot be authorized until TD-171 is closed** |
| **M2-P** | Only its already-decided binding-infrastructure scope (RD-M2-07: C1–C3). Unaffected by TD-171 |

### 17.3 Traceability

| Source | Link |
|---|---|
| RD-23-03 (`ROD-WP-23-AC …` §0.1, §0.2, §0.4) | The Layer 1–4 model; GAP-23-03-1/2 are TD-171's content (OQ-171-2) |
| Gate 1 **CERT-F-04** (`CERT-WP-23-AC …`) | "closes before any execution-eligibility consumer is built" (OQ-171-1, OQ-171-3) |
| Gate 5 **G5-01** (`RRA-WP-23-AC …`) | Required registration of the debt (the basis of C-1) |
| Gate 5 **G5-08** | Hard precondition; severity reassessment at the consumer (OQ-171-1, OQ-171-4) |
| WP-23 A–C acceptance condition **C-1** and carry-forward (`IRA-WP-23-AC …`) | Preserved without variation (OQ-171-1) |
| **TD-171** (`TECH-DEBT.md`) | Remains OPEN. A future synchronization is identified (OQ-171-5) |
| `ADR-042` (`RO-M1-03`: BAR authority unchanged; the BAE consumes) | BAE M2 stays a consumer (§17.2) |
| `ADR-043` (§7: TD-171 separate from B2) | M2-P/B2 unaffected (§17.2) |
| FO-2 (`IRA-BAE-001-M2 §16.B`, §16.E, §16.H) | Stage 2b read-only contract; the §16.H prerequisite is now decided as closure |
| FO-3 (§16; FQ-2 (a)) | Input to a future WP-23 mechanism only; not adopted (OQ-171-2) |
| RD-M2-05 (`ROD-BAE-001-RD-M2-05 …` §21) | Host decision unchanged; TD-171 OPEN (§21.4) |
| §13 (`IRA-BAE-001-M2` §13.1, §13.5, §13.8, §13.9) | The TD-171 prerequisite is a hard authorization gate, satisfied only by closure. §13 is not edited here |

None of these sources was changed.

### 17.4 State after this decision

| Item | State |
|---|---|
| **TD-171** | **OPEN: remediation still required** (not closed by selecting Option A) |
| M2 | **NOT AUTHORIZED / NOT STARTED** |
| M2-P | CHARTERED / NOT AUTHORIZED / NOT STARTED |
| §13 | PREPARED / NOT APPROVED |
| RD-M2-05, RD-M2-07, RD-M2-08 | DECIDED (unchanged) |

### 17.5 Compact decision table

| OQ | Decision |
|---|---|
| OQ-171-1 | **Option A:** TD-171 must close before M2 authorization. B rejected; C not selected; no M2 exception |
| OQ-171-2 | BAR/WP-23 owns the enforcement and reconciliation mechanism, via a future WP-23 package. Not an M2 defect; no BAE compensation. FO-3's approach is input only |
| OQ-171-3 | No deferred trigger. Closure is a prerequisite to M2 authorization |
| OQ-171-4 | G5-08 severity reassessment requirement preserved, to occur at the future consumer gate. Not performed now; no new severity |
| OQ-171-5 | `TECH-DEBT.md` update in principle, as a separate future synchronization. No change now; this ROD is authoritative |

*~~End of decision preparation. READY FOR DECISION. No implementation. Nothing staged, committed or pushed.~~ End of decision record. DECIDED 2026-09-30 (Option A). TD-171 OPEN. No implementation. M2 NOT AUTHORIZED / NOT STARTED.*
