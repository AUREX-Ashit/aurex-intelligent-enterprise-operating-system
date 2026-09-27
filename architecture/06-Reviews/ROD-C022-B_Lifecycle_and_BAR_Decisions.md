# ROD-C022-B — Lifecycle-Pattern Realization (D9) and BAR Treatment (D10) Decisions

**Status:** D9 = Option A (selected); D10 = Option A (selected) — recorded 2026-09-15 (§0).

**Document type:** Repository Owner Decision record — a follow-up addendum to `ROD-C022`/`ROD-C022-A`, same class, same `-suffix` addendum convention (mirroring `ROD-C022-A`'s own relationship to `ROD-C022`, and `TDS-C023-A`'s relationship to `TDS-C023`). This document does not replace or reopen either prior record.

**Capability:** C-022 Customer & Account Management (`CAP-001` line 76 — Active, Domain D-002 Commercial & Subscription, owning specification `COM-001` — LOCKED under EARB Constitutional Recertification CR-3.0).

**Recorded:** 2026-09-15, per direct Repository Owner instruction ("AUREX — C-022 BA-01 — PREPARE ROD-C022-B"), following the combined read-only investigation ("AUREX — C-022 BA-01 — BUNDLE REMAINING GOVERNANCE INVESTIGATION") that identified two remaining, still-open governance decisions after `ROD-C022-A` D7/D8 and `ADR-038`/`ADR-039` — lifecycle-pattern realization and BAR treatment — neither a `CLAUDE.md §16` canonical conflict, both minimum-scope/readiness determinations of the same class as `ROD-C022-A` D7/D8.

**Classification key:** `[FACT]` — repository fact, directly re-verified for this document, not carried forward from the prior investigation's summary alone. `[RO DECISION]` — a Repository Owner decision now made. `[CARRIED FORWARD]` — restated for completeness, not resolved here.

---

## 0. Repository Owner Decision (Recorded 2026-09-15)

Per direct Repository Owner instruction ("D9 = A, D10 = A"), following presentation of both decisions without either being inferred, assumed, or selected by the preparing session:

- **D9 = Option A — ACCEPT COLLAPSED MINIMUM SLICE.** The single-call `TDS-C022 §15` establish design is accepted for BA-01. Full decision text and consequences recorded at §B.3 below, now marked as selected.
- **D10 = Option A — DEFER BAR MECHANISM.** No BAR registry/mechanism is created by C-022; no Business Activity Identifier is assigned; BA-01 may proceed without BAR registration, mirroring `ADR-037`'s WP-20 treatment as C-022's own explicit decision. Full decision text and consequences recorded at §C.3 below, now marked as selected.

**What this recording does NOT do:** it does not create the C-022 Charter, does not authorize implementation, does not create a BAR mechanism, does not assign a Business Activity Identifier, does not perform CBOR registration (governed separately by `ADR-039`), and does not alter `ROD-C022` D1–D6, `ROD-C022-A` D7–D8, or `ADR-038`. Per §E's own recorded sequencing note, D9/D10 selection is step (1) only — the C-022 Charter (step 2, including the `§20.3` backend-only determination `ROD-C022-A §C.2` requires), CBOR registration (step 3), and implementation (step 4) remain separate, subsequent actions not performed here and not to be inferred from this recording.

---

## A. Relationship to `ROD-C022` D1–D6 and `ROD-C022-A` D7–D8

`[FACT]` `ROD-C022`'s D1–D6 and `ROD-C022-A`'s D7 (no classification attribute, Option A) and D8 (establish-only, no read/list, Option A) are **unchanged and not reopened by this document.** `ROD-C022 §H`'s in-scope/out-of-scope list is not expanded or narrowed here. This document resolves exactly two further questions the combined investigation identified as open after D1–D8 — it adds D9 and D10; it does not touch D1–D8.

`[FACT]` This document **does not alter `ADR-038`.** `ADR-038`'s Option A decision (no classification attribute for Commercial Account) stands exactly as recorded; D9/D10 concern lifecycle-interaction shape and Business Activity registration respectively, neither of which bears on the classification question `ADR-038` resolved.

`[FACT]` **CBOR registration for Commercial Account remains governed separately by `ADR-039`.** `ADR-039` already performs the `CMD-001 §26.3a` eligibility analysis and prepares (without executing) the registration content; this document does not revisit, weaken, or substitute for it. D9/D10 concern Business *Activity* realization and registration (BA-01's interaction shape and BAR status), which `ADR-039 §9`/§11`/§12` already explicitly separated from CBOR eligibility.

---

## B. D9 — Lifecycle-Pattern Realization

### B.1 Evidence, re-verified directly against primary sources for this document

`[FACT]` `COM-001-002` (Section 4, LOCKED, inherited in full by Section 7 per `COM-001` line 44's own inheritance clause), verbatim: *"Every commercial construct below distinguishes three roles, never conflated: an **Anchor Context** (experience-scoped, non-authoritative, resolves which candidate object an action concerns), an **Authoritative Context** (the single current, canonical fact...), and a **Resulting Context** (the commit-produced transition outcome...). No Anchor Context is itself authoritative. No two Authoritative Contexts exist concurrently for the same anchor."*

`[FACT]` `COM-001-003` (Section 4, LOCKED, likewise inherited), verbatim: *"Every commercial action states its business reason and target outcome (an Intent Context) before any candidate change (a Proposed Context) is shaped. A Proposed Context is never authoritative and carries the Intent Context that motivated it."*

`[FACT]` `PE-001-C022 §1.14` names the mandatory stage progression, verbatim: *"Anchor → Understand Standing → Frame Lifecycle Intent / Frame Structural Intent → Shape & Assess → Commit → Distribute Reference."*

`[FACT]` `ERB-C022-06`'s own Entry Context, verbatim: *"An assessed Proposed Commercial Party Context and/or Proposed Commercial Relationship Context with its Commercial Dependency Assessment Context."* — presupposing that Proposed/Assessment contexts already exist by the time Commit (`ERB-C022-06`) runs.

`[FACT]` `TDS-C022 §15`'s design is a single `POST /commercial-accounts` call taking `{account_name}` and directly returning a persisted Authoritative Account Context. `TDS-C022 §15.1` (added during the `[C-3]`–`[C-5]` remediation pass) discloses, without resolving: *"the single-call `POST /commercial-accounts` design above realizes **none** of the Anchor, Intent, Proposed, or Assessment stages as distinct, separately-observable constructs."*

`[FACT]` `IRA-TDS-C022_Independent_Review.md §5.6` (re-read directly for this document): found the schema/API/validation/audit/concurrency/negative-control content of `TDS-C022` sufficient to build from, but identified this same conformance gap and concluded: *"This requires explicit disclosure and an RO-level scope determination — either that a single-step establish is the accepted minimum realization with the Anchor/Intent/Proposal stages disclosed as deferred, or that the minimum slice must realize them. This reviewer does not resolve it."* Recorded as finding `[C-5]`. `TDS-C022 §21` item 5, re-read directly, confirms: *"Not resolved by this document."*

`[FACT]` `c021_offering_definition`'s certified `establish()` (C-021 BA-01) uses the identical collapsed, single-call shape, and that Business Activity completed full five-gate closure (`WPR-001` WP-20 row; `CERT-WP-20`). This is real, on-point, certified precedent — but for a different Business Object under a different `PE-001-Cxxx` specification, and the independent review declined to treat it as automatically dispositive for C-022.

### B.2 The exact unresolved question

> Is a single-call "Establish Commercial Account" flow — collapsing Anchor, Intent, Proposed, and Assessment into one request/response cycle — an accepted minimum-slice realization of `COM-001-002` and `COM-001-003` for C-022 BA-01?

### B.3 `[RO DECISION — D9]` — **SELECTED: Option A** (recorded 2026-09-15, per §0)

**OPTION A — ACCEPT COLLAPSED MINIMUM SLICE** ✅ **SELECTED**
- The single-call establish design in `TDS-C022 §15` is accepted for BA-01.
- Anchor, Intent, Proposed, and Assessment remain conceptually distinct architectural roles per `COM-001-002`/`COM-001-003` — this decision does not dissolve or redefine those roles.
- BA-01 may realize all of them internally within one externally invoked establish flow; no separate, externally observable API is required for each stage at this minimum scope.
- `TDS-C022 §15.1` may remain exactly as designed; no TDS revision is required by this option.
- This option is **informed by**, but **not automatically granted by**, the certified `c021_offering_definition` precedent — this decision is being made explicitly for C-022 on its own governing text (`COM-001-002`/`003`, `PE-001-C022 §1.14`, `ERB-C022-06`), not inferred by analogy to a different Business Object.

**OPTION B — REQUIRE SEPARATE STAGES** *(not selected)*
- The single-call collapsed design is **not** accepted for BA-01.
- BA-01 must realize the Anchor/Intent/Proposed/Assessment stages separately, to the extent `COM-001-002`/`COM-001-003` require, before implementation authorization.
- `TDS-C022` (at minimum §15, §15.1, and any dependent sections — §6.1 schema, §8 API, §16 validation, §17 audit) must be redesigned as a multi-step flow before implementation authorization proceeds.
- This option does not itself specify the redesign — a subsequent TDS revision pass would be required, scoped separately from this decision.

**Consequence of the selected Option A:** `TDS-C022 §15`'s single-call establish design is confirmed acceptable for BA-01 as written; `TDS-C022 §15.1`'s disclosure stands as the permanent record of this decision's own basis and requires no further correction or redesign. `TDS-C022 §21` item 5 is resolved by this decision. This decision governs C-022 BA-01 only. It does not reopen, weaken, or reinterpret the C-021 `c021_offering_definition` precedent's own certified status, and does not establish a repository-wide policy for every future Business Activity — each remains its own scope determination against its own governing `PE-001-Cxxx` specification, consistent with `IRA-TDS-C022_Independent_Review.md §5.6`'s own refusal to resolve this by analogy. This decision does not, by itself, authorize the C-022 Charter or implementation — D10 (below) and the Charter's own `§20.3` determination remain separate steps.

---

## C. D10 — BAR Treatment

### C.1 Evidence, re-verified directly against primary sources for this document

`[FACT]` `COM-001-005` (LOCKED), verbatim, two separate clauses: *"Per `CMD-001 §26.3`, no persistent commercial Business Object shall be **implemented** until registered in the CBOR. No commercial Business Activity shall be **executed** until registered in the BAR (`IMP-001 §6.22`), per `SD-002-004`/`034`'s WP-3 formalization."* — CBOR gates **implementation**; BAR gates **execution**. This asymmetry is stated in the governing text itself, not inferred.

`[FACT]` `COM-001-060` (LOCKED), verbatim: *"Every commercial action described in Sections 5–9 (establish, change, renew, terminate, define, revise, publish, retire, reclassify, merge, split, relate, transfer, determine, adjust, reverse) is a Business Activity per `SD-002 §5`, registered in the Business Activity Registry (`IMP-001 §6.22`) **once implemented**, per `COM-001-005`."* "Establish" is named explicitly — BA-01 is BAR-subject once implemented; this is not in question.

`[FACT]` `CMD-001 §8.10`, re-read directly: the Business Activity Registry is introduced only as an **"Architectural Enhancement (Recommended)"** — not a LOCKED, fully specified registration mechanism with its own eligibility test, unlike CBOR's `§26` (which has `§26.3a` eligibility, `§26.4` structure, `§26.7` mapping). `IMP-001 §6.22` (Engineering Playbook, not Constitutional layer) defines the BAR's intended structure and `§6.22.1a` states: *"IMP-001 does not redefine Business Activity semantics here — per §1.2, it governs how the platform is built, not what is built."* `IMP-001 §6.22.1b` defines the identifier format (`PREFIX-NNNNNN`, e.g. `BA-000089`) but only as the format a future registration would use.

`[FACT]` **No physical BAR registry/mechanism exists anywhere in this repository.** Direct repository-wide search (`find`, this session) for any `BAR-INDEX`/`Business_Activity_Registry`-named file returns no result — no equivalent of `CBOR-INDEX.md` exists for BAR.

`[FACT]` `ADR-037 §Decision item 5`, re-read directly and in full: records that no prior Work Package — **explicitly including WP-17 (C-023) and WP-19 (C-132), both CLOSED** — performed a discrete BAR-registration artifact, and records the Repository Owner's own 2026-09-08 decision ("C-021 / WP-20 — BAR DECISION + GATE 2 V&V AUTHORIZATION"): *"do NOT create any BAR registry / `BAR-INDEX` / BAR file / database or runtime mechanism as part of WP-20; WP-20 does not create a BAR mechanism... a future enterprise-level decision may establish the canonical BAR mechanism; this decision does not create or imply C-021 ownership of the BAR mechanism and does not reopen `COM-001` or redesign the Business Activity Registry."* WP-20 / C-021 BA-01 subsequently completed full five-gate closure (Gate 5 attempt #9, PASS) and is FORMALLY CLOSED — CERTIFIED — RELEASE-READY, without any BAR mechanism ever having been created.

`[FACT]` That 2026-09-08 decision is, **by its own text, scoped to WP-20** ("as part of WP-20," "does not create or imply C-021 ownership") — it does not, on its own terms, automatically bind C-022. `TDS-C022 §21` item 4, re-read directly: *"BAR. `COM-001-060` will apply to the eventual Business Activity once implemented — the same class of Repository Owner decision every prior BA-01 (`C-021`, `C-023`, `C-132`) required (no mechanism exists; none is invented). Not addressed by `ROD-C022`; requires its own decision before implementation authorization, not silently assumed resolved by analogy."*

### C.2 The exact question

> May C-022 BA-01 proceed without a BAR mechanism/registration, following the Repository Owner's existing WP-20 precedent (`ADR-037 §Decision item 5`)?

### C.3 `[RO DECISION — D10]` — **SELECTED: Option A** (recorded 2026-09-15, per §0)

**OPTION A — DEFER BAR MECHANISM** ✅ **SELECTED**
- No BAR registry, `BAR-INDEX`, database, or runtime mechanism is created by C-022.
- No Business Activity Identifier is assigned now — `IMP-001 §6.22.1b`'s format governs a future assignment, not a present one; there is no registry to assign into.
- BA-01 may proceed toward implementation without BAR registration, consistent with `COM-001-005`'s own execution-gate (not implementation-gate) wording for BAR.
- The `COM-001-060` execution-time BAR obligation remains **deferred**, pending a future enterprise-level BAR-mechanism decision — the same disposition `ADR-037` recorded for C-021, made here as C-022's own fresh decision rather than assumed automatically carried forward.
- This explicitly does not reopen `COM-001`, does not redesign the Business Activity Registry, and does not establish C-022 ownership of any future BAR mechanism — mirroring `ADR-037`'s own disclaimers.

**OPTION B — REQUIRE BAR RESOLUTION FIRST** *(not selected)*
- C-022 BA-01 **cannot** proceed to implementation until a BAR governance mechanism/registration path is established repository-wide (or for C-022 specifically) and the required registration is completed.
- This would require a new, separate architecture/engineering initiative to build the BAR mechanism `CMD-001 §8.10`/`IMP-001 §6.22` describe — no such initiative currently exists, and none is created or authorized by this document.

**Consequence of the selected Option A:** No BAR registry, `BAR-INDEX`, database, or runtime mechanism is created by this decision. No Business Activity Identifier is assigned. BA-01 is confirmed as not blocked on BAR for implementation purposes, consistent with `COM-001-005`'s execution-gate (not implementation-gate) wording for BAR; the `COM-001-060` execution-time obligation remains deferred pending a future enterprise-level BAR-mechanism decision, mirroring `ADR-037 §Decision item 5`'s disposition for C-021, now made as C-022's own explicit decision rather than an assumed carry-forward. `TDS-C022 §21` item 4 is resolved by this decision. This decision does not create a BAR registry, does not assign a Business Activity Identifier, and does not perform any BAR registration — those actions are excluded regardless of which option is selected, exactly as `ADR-037`'s own decision excluded them for C-021. This decision does not, by itself, authorize the C-022 Charter or implementation — the Charter's own `§20.3` determination remains a separate step.

---

## D. What This Document Does NOT Authorize

- Any Charter, WP registration, schema, migration, API, frontend, or implementation of any kind.
- A `TDS-C022` revision (even if Option B is selected for D9 — the redesign itself is separate follow-up work, not performed here).
- Any BAR registry, `BAR-INDEX`, database, or runtime mechanism, regardless of which D10 option is selected.
- Any Business Activity Identifier assignment.
- CBOR registration (governed separately and exclusively by `ADR-039`; unaffected by D9/D10).
- Reopening `ROD-C022` D1–D6, `ROD-C022-A` D7–D8, or `ADR-038`'s Option A decision.
- The `§20.3` backend-only Charter determination `ROD-C022-A §C.2` already requires for any future C-022 Charter — that determination remains a separate, still-pending step, not performed by this document.

**No implementation is authorized by D9/D10 having now been decided (§0).** With both selected (D9 = A, D10 = A, recorded 2026-09-15), step (1) of §E's sequence is complete; a Charter (including the `§20.3` determination), and — per `ADR-039`'s own Option B recommendation — actual CBOR registration, remain separate, subsequent steps this document does not perform or authorize.

---

## E. Sequencing Note (step 1 now complete; steps 2–4 not executed)

The combined investigation that produced this document's D9/D10 questions also recommended a four-step sequence: (1) resolve D9/D10 via this ROD; (2) prepare the C-022 Charter, including the `§20.3` backend-only determination; (3) perform actual CBOR registration alongside Charter/Implementation Authorization, consistent with `ADR-039` Option B; (4) proceed through the standard implementation gates. **Step (1) is now complete — D9 = A and D10 = A were explicitly selected by the Repository Owner (§0), not inferred by this document.** Steps (2)–(4) are not performed here and require separate, subsequent authorization.

---

## F. Traceability

| Item | Source |
|---|---|
| Combined investigation identifying D9/D10 as open | "AUREX — C-022 BA-01 — BUNDLE REMAINING GOVERNANCE INVESTIGATION," this session |
| D9 evidentiary basis | `COM-001-002`, `COM-001-003`, `PE-001-C022 §1.14`, `ERB-C022-06` Entry Context, `TDS-C022 §15`/§15.1/§21 item 5, `IRA-TDS-C022_Independent_Review.md §5.6` (`[C-5]`) |
| D10 evidentiary basis | `COM-001-005`, `COM-001-060`, `CMD-001 §8.10`, `IMP-001 §6.22`/§6.22.1a/§6.22.1b, `ADR-037 §Decision item 5`, `TDS-C022 §21` item 4 |
| Prior, unaltered decisions | `ROD-C022` D1–D6, `ROD-C022-A` D7–D8, `ADR-038` (Option A) |
| Separately governed | `ADR-039` (CBOR registration preparation) |

---

*End of ROD-C022-B. D9 (lifecycle-pattern realization) = **Option A, selected** and D10 (BAR treatment) = **Option A, selected**, both recorded 2026-09-15 per §0, following explicit Repository Owner instruction rather than inference or analogy. `ROD-C022` D1–D6 and `ROD-C022-A` D7–D8 unchanged. `ADR-038` unaltered. CBOR registration remains governed separately by `ADR-039`. No Charter, WP registration, BAR registry/mechanism, Business Activity Identifier, BAR registration, CBOR registration, schema, migration, API, frontend, or implementation is authorized, created, or performed by this document. Nothing staged, committed, or pushed.*
