# METH-003 — AUREX Implementation Methodology v2.0

**Document ID:** METH-003
**Type:** Engineering Methodology Improvement (same class as `METH-001`, `METH-002`)
**Adopted via:** `ADR-018_Adoption_of_Implementation_Methodology_v2.0.md`
**Established by:** Repository Owner Instruction "Implementation Methodology v2.0 Establishment / WP-10 Planning Authorization," 2026-08-02, following WP-09's own complete, certified, five-gate closure — the first Work Package to run this repository's own full lifecycle end to end under `CLAUDE.md §20`.
**Governs:** WP-10 onward, and every remaining Release. **Corrected 2026-08-02** — this line originally read "every remaining Release (B through F)," an unsupported forward-reference independently found, during Independent Validation, to name releases that do not exist anywhere in this repository: `PRODUCT-MILESTONE-ROADMAP.md` and `ARCHITECTURE-EVOLUTION-IMPLEMENTATION-PROGRAMME.md` both define exactly Release A (A1/A2/A3), B, C, and D — nothing beyond D has any content anywhere as of this correction. This document governs whichever Releases the roadmap actually defines at the time each is planned, not a specific letter range asserted here. Does **not** reopen WP-01 through WP-09 — each remains valid under the governance that existed at its own certification, the same principle `CLAUDE.md §20.1` already applies to §20 itself.

**Canonical authority preserved, not redefined (`CLAUDE.md §16`):** this document synthesizes and operationalizes what `IMP-001` (implementation pattern), `CLAUDE.md §19`/`§20` (implementation checklist, Enterprise Experience Standard), and `PE-001`/`SD-001`/`DS-001` (Enterprise Experience, Presentation Architecture, Design System) already establish. It introduces exactly two genuine process changes — the Standard Work Package Lifecycle (§4) and the single-authorization commit cadence (§5) — and one genuine content addition drawn directly from WP-09's own evidence — the Mandatory Tenant-Isolation Test Checklist (§3.3). Everything else in this document is a restatement, for practical use, of authority that already exists elsewhere; where this document and any canonical document it restates ever appear to diverge, the canonical document governs, per `CLAUDE.md §16`.

---

## 1. Why This Document Exists

WP-09 is the first Work Package to complete this repository's own full lifecycle — charter, IRA, three Business Activities, full five-gate closure (`CLAUDE.md §19.7b`) — entirely under the Enterprise Experience Standard (`CLAUDE.md §20`, first exercised by WP-08). It proved the model works, and it surfaced three concrete, generalizable lessons this document formalizes so future Work Packages do not have to rediscover them:

1. **A Business Activity's frontend and backend can be approved and closed independently in the same Work Package, and later Business Activities can reuse a prior one's own logic without ever reopening its approved contract** — BA-03 reused BA-02's own `refresh()` core via a purely additive method (`resolve_status()`), never touching BA-02's own already-tested, already-committed code. This is the general pattern §3.2 below names.
2. **A missing multi-tenant/cross-organization test is not a hypothetical risk — it is the exact, empirically-confirmed root cause of the one `CLAUDE.md §19.8.5`-class defect this repository's own five-gate sequence has found in a Work Package's own new code** (WP-09's own Gate 2 V&V Audit; the same root cause `VV-AUDIT-WP-05`'s own F-02 finding already named for a different Work Package). §3.3 below makes the check mandatory and proactive, not something only a V&V Audit discovers after the fact.
3. **Requiring Repository Owner re-approval after every single Business Activity is a heavier cadence than this methodology needs once the five-gate sequence is proven** — WP-09 ran that cadence three times consecutively and every gate passed cleanly; §5 below relaxes it for WP-10 onward, per the Repository Owner's own explicit authorization.

---

## 2. Dual-Dimension Business Activity Completion (Phase 1)

**A Business Activity is complete only when both dimensions below are complete.** This is not a new rule — it is `CLAUDE.md §20.3`'s own Vertical Slice Requirement and `§20.7`'s own Work Package Completion Gate Extension, restated here as a single practical checklist so it is checked once per Business Activity, not inferred from two separate sections each time.

### 2.A Business Capability Completion

Owned by `IMP-001` (implementation pattern, testing, API/event standards) and `CMD-001`/`URA-001`/the relevant Primary Specification (data, authorization). Not redefined here — this is the existing checklist, named for completeness:

| Dimension | Owning Document |
|---|---|
| Business Rules realized | The governing `PE-001-Cxxx` (Business Rules) |
| Experience Contracts realized | The governing `PE-001-Cxxx` (Experience Contracts, Chapter 5 per-capability) |
| Backend implementation | `IMP-001` §5 (Business Object pattern), §6 (Business Activity pattern) |
| APIs | `IMP-001` §8 |
| Database | `IMP-001` §5, `CMD-001 §26.3a` (Business Object Eligibility) |
| Security / Authorization | `URA-001`, `CLAUDE.md §10` |
| Observability | `IMP-001` §6 (audit/event requirements per Business Activity) |
| Performance | `IMP-001` §11 (Testing Strategy), `SD-001 §12` (Performance & Responsiveness Principles) |
| Testing | `IMP-001` §11, extended by §3 below |
| Documentation | `IMP-001`'s own Implementation Report convention (`IMP-REPORT-WP-XX`) |

### 2.B Enterprise Experience Completion

Owned by `PE-001` (experience philosophy, journeys, personas, workspace, navigation), `SD-001` (presentation architecture, screen anatomy), `DS-001` (design tokens, components, themes). Not redefined here — restated as a checklist per `CLAUDE.md §20.6`:

| Dimension | Owning Document |
|---|---|
| Screens | `SD-001 §5`/`§7` (Screen Composition, Standard Screen Anatomy) |
| User Journeys | `PE-001` Chapter 11 |
| Navigation | `PE-001` Chapter 14 |
| Enterprise Shell | `CLAUDE.md §20.5` ("Do NOT regress into an administration console") |
| Discover First | `PE-001 §5.2` |
| Evidence First | `PE-001` Chapter 23 |
| Progressive Disclosure | `PE-001 §5.6`, `SD-001-021` |
| Accessibility | `SD-001 §10` |
| Responsive Design | `SD-001 §11` |
| Executive Experience | `PE-001` Chapter 12 (Persona Model, Executive Personas) |
| PE-001 / SD-001 / DS-001 realization | as named above |

**Where no Enterprise Experience is required for a given Business Activity, this must be stated with architectural justification, not silently omitted** — WP-09's own BA-03 is the established precedent: `IRA-009 §7` explicitly cited `PE-001-C008`'s own text characterizing `EX-C008-11` as "system-facing," and `IMP-REPORT-WP-09`'s own BA-03 Frontend section states "No frontend deliverable" with that citation, rather than leaving the question unaddressed.

---

## 3. Testing Discipline (extends `IMP-001 §11`, not a replacement)

### 3.1 Baseline (unchanged)

Business Activity Contract tests, Authorization Boundary tests, API tests for every endpoint/status branch, full regression suite before every closure gate — all already required by `IMP-001 §11` and `CLAUDE.md §14`. Unchanged.

### 3.2 Reuse-Without-Reopening Pattern (new, from WP-09's own evidence)

When a later Business Activity in the same Work Package needs a prior, already-approved Business Activity's own logic, the correct pattern — per `CLAUDE.md §19.5`'s Reuse-first order — is a **purely additive public method** on the existing service, never a modification of the prior Business Activity's own already-tested method body. Concretely: `WorkspaceStatusService.resolve_status()` was added alongside the already-committed `refresh()` in the same file, calling the same private core (`_resolve_status()`), with the prior Business Activity's own existing tests re-run unchanged (not rewritten) to prove zero behavioral change. This is now the standard pattern; a Work Package's own Implementation Report SHALL state explicitly, for any such reuse, that the prior Business Activity's own tests were re-run unchanged as evidence.

### 3.3 Mandatory Tenant-Isolation Test Checklist (new, non-optional)

**For every new endpoint whose underlying data model carries an organization/tenant boundary** (i.e., the underlying table has an `organization_id` column, directly or by one-hop join — e.g. `Membership`, `AccessEvaluationOutcome`, `DomainPermission`), the implementing Business Activity's own test suite SHALL include, before that Business Activity is submitted for Independent Certification:

1. At least one test seeding **two distinct, unrelated Organizations** with no shared Person/Membership/foreign-key row.
2. At least one test confirming a caller authenticated in one Organization **cannot** retrieve, infer, or distinguish another Organization's own data through that endpoint, unless the endpoint's own governing specification explicitly authorizes cross-organization visibility (e.g. `BA-01`'s own candidate-resolution endpoint, whose cross-organization behavior is the specification's own intended shape, not a gap).
3. Where an endpoint's own request accepts a foreign-object identifier not derived from the caller's own JWT claims (mirroring `BA-03`'s own `membership_id`), the test suite SHALL explicitly probe whether an unrelated tenant's identifier is accepted — and if the endpoint has no ownership check, the endpoint SHALL be gated (e.g. `require_platform_admin`, the established interim pattern) before submission, not left ungated pending a future audit to discover it.

**Why this is now mandatory, not advisory:** this exact gap (no cross-tenant test existed for `BA-02`/`BA-03`, despite `BA-01`'s own analogous test existing) is the specific, empirically-confirmed cause of the one `CLAUDE.md §19.8.5`-class defect this repository's five-gate sequence has ever found in new code — `WP-09`'s own Gate 2 V&V Audit, mirroring `VV-AUDIT-WP-05`'s own F-02 finding in an unrelated Work Package. The same class of gap has now recurred twice. This checklist converts a reactive audit finding into a proactive submission gate.

---

## 4. Standard Work Package Lifecycle (Phase 8 — new)

Every future Work Package SHALL follow this sequence. Steps 1–3 are new relative to WP-01 through WP-09's own practice — they did not exist as formal, named steps before this document, though their substance (traceability, historical-asset reuse) was always required by `CLAUDE.md §12`/§19.2.

```
Release
   │
   ▼
Work Package (Charter + IRA)
   │
   ▼
Strategic Enhancement Review  ──  SER-001, per §6 below: classify every
   │                               relevant enhancement (Implemented /
   │                               Partially Implemented / Deferred / N/A)
   ▼
Historical Screen Review  ──  Per §7 below: classify every relevant
   │                           historical screen/concept (KEEP / EVOLVE /
   │                           MERGE / RETIRE)
   ▼
Executive Cognition Review  ──  Per §8 below: determine which Executive
   │                             capabilities this Work Package advances,
   │                             defers, or leaves unaffected
   ▼
Business Activity (one or more, per the IRA's own Gap Analysis)
   │
   ▼
Enterprise Experience (§2.B, realized per BA — not deferred to the end)
   │
   ▼
Backend
   │
   ▼
Frontend
   │
   ▼
Testing (§3, including §3.3's mandatory tenant-isolation checklist)
   │
   ▼
Logical Commits (multiple encouraged — §5 below)
   │
   ▼
Independent Verification & Validation (Gate 2, `CLAUDE.md §19.7b`)
   │
   ▼
Independent Certification (Gate 1, performed first in practice per
   │                         precedent, named here in closure order)
   ▼
Release Readiness (Gate 5)
   │
   ▼
Closure
```

**Note on gate ordering:** `CLAUDE.md §19.7b` names Certification as Gate 1 and V&V as Gate 2 because Certification is performed first in every precedent this repository has (WP-05 through WP-09); the diagram above lists them in that same order at the bottom for closure — the "Independent Verification & Validation" and "Independent Certification" lines are not a reordering of `§19.7b`, only this diagram's own visual grouping of "the five gates" as one closure block following Testing.

---

## 5. Commit and Approval Cadence (Phase 8 — relaxed, new)

**One Repository Owner authorization SHALL execute one complete Work Package**, not one Business Activity. This relaxes WP-09's own stricter cadence (a separate Repository Owner approval after every Business Activity), per the Repository Owner's own explicit authorization in this document's own establishing instruction — WP-09 proved the five-gate sequence catches what needs catching without per-BA checkpoints.

- **Multiple logical commits during implementation are encouraged** — one per Business Activity (WP-09's own established pattern) or one per coherent unit of work, whichever the implementing session judges clearer. `git add -A` remains prohibited; every commit stages precisely the files belonging to that logical unit.
- **Repository Owner approval occurs after Work Package completion**, not after each Business Activity, unless an exceptional architectural issue requires earlier intervention (e.g. a genuine ambiguity requiring a STOP-and-report per `CLAUDE.md §17`/§19.4 — those provisions are unchanged by this document).
- The five-gate closure sequence (`CLAUDE.md §19.7b`) remains unchanged and mandatory in full, including genuinely independent, fresh-context reviewers for every gate, and Gate 4's own "regardless of severity" independent-verification-of-remediation requirement.

---

## 6. Strategic Enhancement Review (governs use of `SER-001`)

Before Business Activity work begins, the implementing session SHALL review `SER-001_Strategic_Enhancement_Register.md` and explicitly classify every enhancement relevant to the Work Package's own capability as **Implemented**, **Partially Implemented**, **Deferred**, or **Not Applicable** — recorded in the Work Package's own IRA (a new subsection, "Strategic Enhancement Disposition") and carried into the Implementation Report at closure. No relevant enhancement may be silently unaddressed. See `SER-001` itself (§2 of this document's own companion register) for the register's own schema and maintenance rule.

## 7. Historical Screen Review (governs use of the Historical Screen Realization Matrix)

Before frontend work begins, the implementing session SHALL review `HISTORICAL-SCREEN-REALIZATION-MATRIX.md` for any historical concept mapped to the Work Package's own capability, and confirm the matrix's own classification (KEEP / EVOLVE / MERGE / RETIRE) still holds or requires updating given what the Work Package actually builds. See that document for the full inventory and current classifications.

## 8. Executive Cognition Review (governs use of the Executive Cognition Realization Strategy)

Before implementation begins, the implementing session SHALL review `EXECUTIVE-COGNITION-REALIZATION-STRATEGY.md` and determine, per §6 of that document, which Executive capabilities the Work Package advances (even partially), which it leaves deferred (naming the Release/Work Package that will pick them up, per that document's own tracking discipline), and which are unaffected. This prevents Executive Cognition being silently deferred wholesale to Release D, per this instruction's own explicit Phase 6 mandate.

---

## 9. World-Class Enterprise Experience Evaluation (Phase 5)

Every Enterprise Experience delivered under this methodology SHALL be evaluated, at Independent Certification, against the following principles — already established across `PE-001` (Chapters 5, 6, 8), `SD-001` (Sections 2, 5, 9, 10, 11), and `CLAUDE.md §20.5`, consolidated here as a single checklist, not a new standard:

Simplicity and minimal cognitive load (`PE-001 §5.1`/`6.1`, Outcome Orientation); Discoverability (`PE-001 §5.2`, Discover First); Information density and Progressive Disclosure (`PE-001 §5.6`, `SD-001-021`); Executive-first usability where applicable (`PE-001` Chapter 12); Explainability (`PE-001 §5.8`/`6.7`/Chapter 23); Accessibility (`SD-001 §10`); Keyboard-first productivity (`SD-001 §9`, Universal Design Laws — already the basis for this session's own `useOverlay` focus-trap pattern, reused across every `Menu`-based component to date); Enterprise consistency (`PE-001 §5.9`/`6.5`); Responsive experience (`SD-001 §11`).

**`CLAUDE.md §20.5`'s own constraint stands unchanged: these principles are evaluated as interaction-quality references, never as license to copy any named product's own visual design, layout, or branding.** DS-001 remains sole authority for every visual and component decision; where DS-001 does not define something one of these principles suggests, the implementing session SHALL STOP and request clarification, exactly as `§20.5` already requires.

---

## 10. Governing Documents

`CLAUDE.md §16`–`§20`; `IMP-001_Implementation_Playbook.md`; `PE-001_Enterprise_Experience_Blueprint.md` (Chapters 5–8, 11–17, 22–24); `SD-001 — Enterprise Presentation Architecture.md`; `DS-001 — AUREX Design System.md`; `METH-001`, `METH-002` (precedent methodology-improvement documents this one extends the pattern of); `WP-09`'s own Charter, `IRA-009`, `IMP-REPORT-WP-09`, `CERT-WP-09`, `VV-AUDIT-WP-09`, `VV-AUDIT-WP-09_Remediation_Verification`, `RRA-WP-09` (the evidentiary basis for §1's own three lessons).

---

*End of METH-003. Adopted via `ADR-018_Adoption_of_Implementation_Methodology_v2.0.md`. Governs WP-10 onward.*
