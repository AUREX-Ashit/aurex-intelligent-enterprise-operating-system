# IRA-RELEASE-A — Foundation Repair — Implementation Readiness Assessment

**Document ID:** IRA-RELEASE-A
**Release:** Release A — Foundation Repair (per `ARCHITECTURE-EVOLUTION-IMPLEMENTATION-PROGRAMME.md` §7, Release Plan)
**Capability:** None — Release A is explicitly not chartered against a CAP-001 capability (Implementation Programme §5, Work Package Mapping: "R2, R3, R4, R5, R6, R7, R8 → No Work Package — pure documentation/governance actions"; "R1 → Infrastructure remediation"; "R29 → Technical Debt")
**Governing Inputs:** `ARCHITECTURE-EVOLUTION-STRATEGIC-ROADMAP.md`, `ARCHITECTURE-EVOLUTION-IMPLEMENTATION-PROGRAMME.md`, `PRODUCT-MILESTONE-ROADMAP.md` (approved planning inputs, per Repository Owner instruction)
**Status:** PARTIALLY READY — see §6 Readiness Decision
**Prepared By:** Engineering Governance session (Claude Code)
**Date:** 2026-08-01

**Note on numbering:** this document is intentionally **not** part of the IRA-001…IRA-008/IRA-RTA-001 series. That series gates Work Packages chartered against a specific CAP-001 capability, per the charter→IRA process the Implementation Programme's own research confirmed (Charter → IRA → five-gate closure). Release A charters nothing — it is infrastructure repair and documentation reconciliation work the Implementation Programme itself classified as outside the Work Package model. Numbering it into that series would misrepresent it as capability-tied. This document follows the same rigor and template shape as a WP IRA (per `IRA-008`'s own structure, read in full before drafting this one) wherever that structure legitimately applies, and departs from it explicitly where it doesn't.

---

## 1. Purpose

Determines whether, and at what scope, Release A (per `ARCHITECTURE-EVOLUTION-IMPLEMENTATION-PROGRAMME.md` §7) may proceed to implementation, per `CLAUDE.md §19` and this Release's own approved planning inputs. Unlike a capability IRA, this assessment does not produce a Plan A/Plan B split (there is no Enterprise Experience or Business Capability being built) — it produces a **governance-tier readiness split**, because Release A's nine constituent items are not uniform in what governance process each requires before implementation, a distinction the Implementation Programme itself did not resolve to this level of precision.

---

## 2. Governing Documents Reviewed

- `ARCHITECTURE-EVOLUTION-IMPLEMENTATION-PROGRAMME.md` §2 (Classification), §3 (Capability Mapping), §4 (Document Update Plan), §5 (Work Package Mapping) — the approved scope source for Release A (items R1, R2, R3, R4, R5, R6, R7, R8, R29).
- `DOC-000_Documentation_Catalogue.md` §8 (Enterprise Documentation Register) — read in full this session to determine each target document's actual Canonical Status and Lifecycle Status (Locked vs. not), and §10 (Document Update Matrix) for the update-trigger rule governing Locked constitutional documents.
- `CLAUDE.md` §18 (Architectural Change Control), §19 (Implementation Start Checklist).
- `ARM-001_Implementation_Report.md` / `AAR-001_Architecture_Audit_Remediation_Register.md` (per `DOC-000` §8) — the precedent this assessment relies on for how a previously-identified ARCH-000 ownership-table inconsistency was actually corrected (commit `770aaad`): as an Implementation Report following an audit finding, not a fresh ADR, and scoped to editing ARCH-000's own table only.
- `ADR-016_Authorization_Runtime_Consolidation.md` (per prior session research this same conversation) — confirms this repository's real precedent for correcting a duplicate/conflicting architectural concept via a full ADR when the correction touches more than one document's own substantive content, not just a cross-reference.
- Direct repository verification this pass: `Backend/Shared/*` module structure and `Backend/Services/AuthService/observability.py`'s own docstring, confirming the `aurex.backend.shared.*` import-path defect (R1) is current and unchanged since the Implementation Programme was written.

---

## 3. Scope Under Assessment

The nine items the Implementation Programme's own Release Plan (§7) assigns to Release A:

| Item | Description | Target(s) |
|---|---|---|
| R1 | Repair `Backend/Shared/Logging`/`Backend/Shared/Events` import defect | Code only — `Backend/Shared/*`, consuming services |
| R2 | Correct CLAUDE.md §3 repository navigation map | `CLAUDE.md` |
| R3 | Reconcile ARCH-000 §7c / RTA-001 §12.16 (Knowledge Governance ownership) | `ARCH-000` (cross-reference correction) |
| R4 | Reconcile `llm_prompt_registry` vs `reasoning_engine_registry` | Master Technical Architecture |
| R5 | Reconcile "Enterprise Operating System" vs "Intelligent Enterprise Operating Center" naming | `ARCH-000` §2, `Complete_Blueprint` |
| R6 | Update CMD-001 §24 to reference AMD-012/013 registries | `CMD-001` |
| R7 | Ratify or retire SD-001's two unratified extensibility candidates | `SD-001` / `SD-002` |
| R8 | Add Explainability as an explicit owned row in ARCH-000 §7c | `ARCH-000` (table addition) |
| R29 | Log the `Backend/Shared` defect in the Technical Debt Register | `TECH-DEBT.md` |

---

## 4. Current-State Verification

Re-verified directly this pass (not assumed stale-safe):

- **R1** — confirmed still present. `Backend/Services/AuthService/observability.py`'s own docstring states its `record_audit`/`publish_event`/`record_metric` primitives are "a temporary stand-in for `Backend/Shared/Logging`/`Backend/Shared/Events`," which exist as complete module trees (`Backend/Shared/{Config,Database,Events,Logging,Security}/*.py`, all present, non-empty) but expect import via `aurex.backend.shared.*` — no `aurex` directory, `setup.py`, or `pyproject.toml` establishing that namespace exists anywhere in the repository. Unchanged from prior findings.
- **R2, R3, R4, R5, R6, R7, R8, R29** — rely on the Implementation Programme's own already-established evidence (same session, same day); no new repository scan performed for these, per this pass's own instruction not to repeat research. No reason to suspect drift in the hours since that evidence was gathered.

---

## 5. Governance-Tier Analysis

The Implementation Programme classified all of R2–R8 identically as "documentation reconciliation... no Work Package required." That classification is correct as far as it goes, but it does not distinguish *which governance process* each document edit requires before it may be made — and those requirements are not uniform. `DOC-000` §8/§10 supplies the answer directly:

| Document | Canonical Status (`DOC-000` §8) | Update Rule (`DOC-000` §10) |
|---|---|---|
| `CLAUDE.md` | Not independently registered — a Supporting Artifact (`DOC-000` §3) | No ADR gate; operational instructions, not a governed architecture document |
| `TECH-DEBT.md` | Governance Registry, Active, **living register** | "Updated When: Debt is introduced or resolved" — routine, no gate |
| `ARCH-000` | Canonical, top-level authority, **AUTHORITATIVE** (not enumerated in §10's Locked-document list) | Precedent (`ARM-001`, commit `770aaad`) shows a self-contained correction to ARCH-000's own table, following an audit finding, proceeds as an Implementation Report — not a fresh ADR — provided the edit is scoped to ARCH-000's own content and doesn't rewrite another document's substance |
| `RTA-001` | Canonical, **LOCKED** | §10: "Only via the Locked-document ADR process, or a certified recertification" |
| `CMD-001` | Canonical, **LOCKED** | Same ADR/recertification requirement |
| `SD-001` | Canonical, **LOCKED (Gold Standard)** | Same ADR/recertification requirement |
| Master Technical Architecture | Canonical, **Active, evolving via amendment log** (not "Locked") | Has its own established lighter-weight mechanism — sequential `AMD-XXX` amendments (`AMD-012`, `AMD-013`, `AMD-014` already exist) — distinct from, and not requiring, a full ADR |
| `Complete_Blueprint` | Not found as its own row in `DOC-000` §8's register (referenced only in §2/§6 as the top-of-stack philosophy document) | Lock status genuinely unclear from available evidence — treated cautiously below, not assumed editable |

Applying this to each item:

- **R3** (ARCH-000 §7c ↔ RTA-001 §12.16): the corrective action available without touching RTA-001 itself — adding a cross-reference/caveat to ARCH-000's own Ownership Map table, mirroring exactly what the `770aaad` precedent already did for the Prompt/Model Governance case — is a same-tier correction. **No ADR required.**
- **R8** (Explainability owner row): a pure addition to ARCH-000's own table, same pattern. **No ADR required.**
- **R2** (CLAUDE.md): not a governed architecture document at all. **No ADR required.**
- **R29** (TECH-DEBT.md entry): explicitly a living register meant for exactly this kind of update. **No ADR required.**
- **R1** (code repair): touches no governed document. **No ADR required.**
- **R4** (`llm_prompt_registry`/`reasoning_engine_registry`): the *mechanism* (an `AMD-XXX` amendment) is already established and does not itself require a new ADR — but *which* registry to deprecate, or how to scope them apart, is a content decision this assessment cannot make on its own authority. **Blocked on a Repository Owner decision, not on process.**
- **R5** (EOS naming): a pure naming decision with no "correct" answer derivable from evidence — this assessment found both terms in active canonical use and cannot resolve which one should govern. Also touches `Complete_Blueprint`, whose lock status is not confirmed. **Blocked on a Repository Owner decision.**
- **R6** (CMD-001 §24 update): CMD-001 is LOCKED, and the edit is to CMD-001's own substantive content (adding table references), not a cross-referencing correction from an unlocked document. **Blocked on the formal ADR/recertification process.**
- **R7** (SD-001 candidate ratification): SD-001 is LOCKED, and ratifying draft candidate text into governed status is unambiguously a content decision plus a Locked-document change. **Blocked on both a Repository Owner decision (ratify vs. retire) and the formal ADR process.**

---

## 6. Readiness Decision

**PARTIALLY READY.**

**Tier 1 — READY, no further gate required:** R1, R2, R3, R8, R29. Five of Release A's nine items may proceed to implementation now, entirely within this assessment's own authority, without inventing new architecture, without touching a Locked document's substantive content, and without requiring a decision only the Repository Owner can make.

**Tier 2 — BLOCKED, genuine implementation blocker, not proceeding under this IRA:** R4, R5, R6, R7. These four require either an explicit Repository Owner decision (R4, R5, R7) or the formal Locked-document ADR/recertification process (R6, R7), or both (R7). This is the "genuine implementation blocker" this pass's own instruction anticipated — surfaced here rather than either silently implemented past the gate or silently dropped from scope. See §10.

This split is a direct consequence of applying `DOC-000` §10's own already-existing rule precisely, not a new process this assessment invents. Implementing Tier 2 items without first satisfying their gate would violate `CLAUDE.md §18`'s prohibition on changing architecture to make implementation easier.

---

## 7. Implementation Plan — Tier 1 (the authorized scope of this Release A pass)

### R1 — Repair `Backend/Shared` import defect

- **Change type:** Code only. No new architecture, no new module — the modules already exist and are already correct in content; only their import path is unreachable.
- **Approach:** establish the `aurex.backend.shared` package path the existing modules already expect (e.g., a package root / `sys.path` entry / installable local package pointing `aurex.backend.shared` at `Backend/Shared`), rather than rewriting every consuming service's own import statements — this is the smaller, more reversible of the two possible fixes, and it makes every existing `from aurex.backend.shared...` import in the codebase work as originally written, rather than requiring every one of them to be edited individually.
- **Verification:** each of `Backend/Shared/{Config,Database,Events,Logging,Security}` imports successfully; `Backend/Services/AuthService/observability.py`'s own documented stand-in note is removed once it can genuinely delegate to the shared modules (or left in place with a corrected note, if full delegation is judged out of scope for this narrow repair — a scope call for the implementing pass, not this IRA).
- **Testing:** an import-only smoke test per shared module; full AuthService regression suite re-run to confirm no consuming service's behavior changed.
- **No database migration, no API change, no new endpoint.**

### R2 — Correct CLAUDE.md §3

- **Change type:** Documentation only.
- **Approach:** update §3's stated paths (`source/backend`, `source/database`) to reflect actual layout (`Backend/*`, `database/*`), matching the correction already recommended in the Architecture Evolution Roadmap §7.
- **Testing:** N/A (documentation).

### R3 — ARCH-000 §7c Knowledge Governance cross-reference

- **Change type:** Documentation only, ARCH-000's own table.
- **Approach:** mirror the `770aaad` precedent exactly — add a note to the Knowledge Governance row acknowledging RTA-001 §12.16's substantive content, and either assign an explicit owner or state why the deferral still stands despite §12.16 (a determination for the implementing pass to make transparently, citing both sections, not silently).
- **Testing:** N/A (documentation).

### R8 — ARCH-000 §7c Explainability row

- **Change type:** Documentation only, ARCH-000's own table.
- **Approach:** add Explainability as an explicit row, citing SD-002-016 as owner, matching the structure of every other row in the same table.
- **Testing:** N/A (documentation).

### R29 — Technical Debt Register entry

- **Change type:** Documentation only, `TECH-DEBT.md`'s own living register.
- **Approach:** one new entry for the `Backend/Shared` import defect (R1), following `TECH-DEBT.md`'s own established entry format. Severity per `CLAUDE.md §19.8.7`'s rubric: **Medium** — does not currently defeat any Active capability's stated Business Intent, but blocks clean Observability/Audit consolidation for future capability work, a real if not-yet-triggered downstream risk. `[PRODUCT JUDGMENT]`, carried forward from the Roadmap. **Note:** if R1 is implemented and closed within this same Release A pass, this entry should be logged as already-resolved (Status: Closed, Resolving action: R1), not left open — `TECH-DEBT.md`'s own discipline is to record resolution, not just introduction.

---

## 8. Anticipated Technical Debt

- **TD-candidate (Release A):** R1's fix establishes the `aurex.backend.shared` import path but does not itself migrate every service's own duplicated stand-in logic (e.g., `AuthService/observability.py`'s own `record_audit`) onto the now-reachable shared modules — that migration is a separate, larger effort than "make the import work," and doing it inside Release A risks scope creep into behavior change this Release's own Foundation Repair framing doesn't cover. Recommend disclosing this as its own Low-severity Technical Debt entry at implementation time, distinct from R29's entry for the import defect itself.

---

## 9. Testing Strategy

Per `IMP-001 §11`, scoped to Tier 1's actual code-touching item (R1 only — R2/R3/R8/R29 are documentation, no test surface): import-smoke tests for each `Backend/Shared` module; full existing AuthService regression suite re-run before this Release A pass closes, per every prior Work Package's own precedent, to confirm the import-path fix introduces no behavioral change to already-passing tests.

---

## 10. Repository-Owner Decisions Required (blocking Tier 2)

1. **R4** — which AI-configuration registry should govern going forward, `llm_prompt_registry` or `reasoning_engine_registry` — or should they be explicitly scoped apart rather than one deprecated?
2. **R5** — is "Enterprise Operating System" or "Intelligent Enterprise Operating Center" the canonical platform-identity name, or are they to be declared explicitly synonymous?
3. **R6** — authorize the CMD-001 §24 update through the Locked-document ADR/recertification process (or decline, leaving the documentation-currency gap disclosed but open).
4. **R7** — ratify or retire the two SD-001 extensibility candidates, and separately authorize whichever outcome through the Locked-document ADR process.

Tier 2 does not proceed under this IRA. A future pass may re-assess Tier 2 once these decisions are made, without needing to re-verify Tier 1's own findings.

---

*End of IRA-RELEASE-A. Tier 1 (R1, R2, R3, R8, R29) is READY for implementation under this assessment. Tier 2 (R4, R5, R6, R7) remains BLOCKED pending Repository Owner decisions and, for R6/R7, the formal Locked-document process. Per Repository Owner instruction, implementation does not begin until this IRA has been reviewed.*
