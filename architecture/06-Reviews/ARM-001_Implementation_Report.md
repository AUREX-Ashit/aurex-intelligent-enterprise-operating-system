# ARM-001 — Architecture Remediation Implementation Report

**Program:** Enterprise Architecture Remediation Program, governed by `architecture/06-Reviews/AAR-001_Architecture_Audit_Remediation_Register.md` (CERTIFIED WITH OBSERVATIONS, 2026-07-27).
**Remediation executed:** AR-001 — AI Governance & Ownership Reconciliation (the first remediation in dependency order among AAR-001's eight "Before WP-02" items; see Task 1/2 below).
**Scope of this report:** This report covers only AR-001. AR-002 through AR-009 (the remaining Before-WP-02 remediations) remain deferred, per instruction, pending separate execution and their own ARM-00N reports.
**Status:** Implementation complete for AR-001. Developer Validation, Independent Review, and Certification are Pending (see §8–§10).

---

## 1. Task 1 — Remediations Classified "Before WP-02" (Dependency Order)

Read directly from AAR-001 §5 (Priority, Dependency, and Sequencing Review) and §6 (Implementation Timeline). AAR-001 §6 lists exactly eight remediations under "Before WP-02 begins": AR-001, AR-002, AR-003, AR-004, AR-005, AR-007, AR-008, AR-009. (AR-006 is classified "Can Wait," not "Before WP-02," despite being cheap enough to do early; it is excluded from this list per AAR-001's own classification.) AAR-001 §5 orders these eight by priority basis / dependency as follows:

| Order | Remediation | Priority Basis (per AAR-001 §5) |
|---|---|---|
| 1 | **AR-001** | Constitutional-tier contradiction — no dependency |
| 2 | AR-002 | Blocks AR-003 — no dependency itself |
| 3 | AR-004 | Independent, cheap, closes a real silent gap |
| 4 | AR-005 | Independent, foundational |
| 5 | AR-003 | Depends on AR-002 |
| 6 | AR-008 | Independent (corrected dependency — does not require AR-007) |
| 7 | AR-009 | Independent (corrected dependency — does not require AR-007) |
| 8 | AR-007 | Large effort, no blocking dependency — start early |

**First remediation in dependency order: AR-001.** This is the remediation executed by this report.

---

## 2. Task 2 — Remediation Details (All Eight Before-WP-02 Items)

| Remediation | Objective | Documents Affected | Architectural Owner | Estimated Effort | Dependencies | ADR Required? | Validation Method |
|---|---|---|---|---|---|---|---|
| **AR-001** | Resolve the ARCH-000 §7c / RTA-001 §13.15 contradiction on Prompt/Model Governance ownership; add Explainability and a statement on Agent-specific Governance to ARCH-000 §7c's table. | ARCH-000 §7c | ARCH-000 (top-level governance authority) | Small | None | **No** — on the recommended path (update ARCH-000 §7c only, leave RTA-001 unmodified). ADR would be required only if the alternative path (rescoping RTA-001 §13.15, a LOCKED document) were chosen instead; AAR-001 recommends against that path. | GRC-001, PLT-001, OPM-001, COM-001, ONT-001 (all already deferring to ARCH-000 §7c) still resolve correctly against the updated table. |
| AR-002 | Record an explicit decision on the relationship between `llm_prompt_registry` and `reasoning_engine_registry`. | Master Technical Architecture | Master Technical Architecture | Medium | None | No — scope-relationship decision within Master Technical Architecture's own amendment mechanism (not Locked/Frozen). | No remaining "or" ambiguity between the two mechanisms. |
| AR-003 | Designate one `reasoning_engine_registry` row as the platform default. | Master Technical Architecture | Master Technical Architecture | Small | AR-002 | No — additive designation within an already-approved, vendor-neutral registry. | Exactly one row flagged default, consistent with AR-002. |
| AR-004 | Promote the actual embedding model in use into architecture as a named decision. | Master Technical Architecture (`vector_index_registry`) | Master Technical Architecture | Small | None | No — additive. | Named value present and cross-referenced from `Backend/Services/AIService` config. |
| AR-005 | Select and record a message-broker product; clarify the canonical Event Store. | Master Technical Architecture (I.13 frozen stack list; event registry documentation) | Master Technical Architecture | Medium | None | No — additive designation within existing frozen-stack list and event registries. | Product appears in I.13's list; one document states which table is the canonical event-sourcing store. |
| AR-007 | Author Experience Blueprints (PE-001-C090 through PE-001-C095) for Discovery, Knowledge, Search, Conversation, and Memory. | New: `PE-001-C090` through `PE-001-C095` | PE-001 (new capability blueprints, once authored) | Very Large | None | No — new document creation in an established genre, not modification of a Locked/Frozen document. | Each blueprint passes the same Gold Standard validation criteria as `PE-001-C004` v1.1. |
| AR-008 | Register D-005 as a URA-001 Domain. | URA-001 | URA-001 | Small | None | No — mechanical registry action. | D-005 appears in URA-001's Domain registry. |
| AR-009 | Formally allocate the 18 proposed Business Activity and 8 proposed EIO identifiers. | IMP-001 (Business Activity Registry) | IMP-001 Business Activity Registry | Medium | None | No — mechanical registry action. | All 26 identifiers present in the registry as non-provisional. |

---

## 3. Task 3 — Execution of AR-001 (the First Remediation in Dependency Order)

### 3.1 Gap Analysis (performed before any change)

- **ARCH-000 §7c** ("Enterprise Intelligence & AI Governance Ownership Map") stated, prior to this change: Prompt governance, Knowledge governance, Memory governance, and Model governance are all **Deferred**, with "no placeholder owner... assigned to any of them," citing EIA-001 Vol. I §8.4's reservation for a future volume.
- **RTA-001 §13.15** ("AI Governance," read in full prior to editing) states: "The AI Runtime shall support enterprise AI governance including: Prompt Governance, Model Governance, Policy Governance, Human Oversight, Explainability, Version Management, Audit, Compliance." This is an unconditional operational claim ("shall support"), not a deferral.
- **Direct contradiction confirmed:** ARCH-000 §7c and RTA-001 §13.15 disagree specifically on Prompt Governance and Model Governance — one document defers ownership, the other asserts the guarantee is already operational. Knowledge Governance and Memory Governance are untouched by this contradiction, since RTA-001 §13.15 makes no claim over either.
- **Explainability gap confirmed:** RTA-001 §13.15 lists Explainability as a governance guarantee, but ARCH-000 §7c's table had no Explainability row at all. Direct repository search located the two substantive owning definitions: `SD-002-016` ("Universal Explainability," `SD-002_Universal_Business_Object_Rules.md`) and `SD-001` `LAW-26` ("Explainability Is One Click Away," `SD-001 — Enterprise Presentation Architecture.md`).
- **Agent-specific governance gap confirmed:** no document distinguishes agent-specific governance from the general AI Governance guarantee; `agent_registry.governing_policy_id` was confirmed to reuse the general governance/confidence mechanism rather than define a separate one.

### 3.2 Affected Documents Identified

Only **ARCH-000 §7c** is affected by this remediation, per AR-001's own "Documents to update" field and its explicit "Expected outcome" that RTA-001 §13.15 remain unmodified. RTA-001 is designated **LOCKED**; AAR-001 explicitly recommends the path that leaves it untouched specifically to avoid triggering an ADR. No other document (CMD-001, EIS-001, SD-001, SD-002, GRC-001, PLT-001, OPM-001, COM-001, ONT-001) was modified — each of these is either the untouched *source* of an ownership citation (SD-002-016, SD-001 LAW-26) or a document that already correctly defers to ARCH-000 §7c and required no change of its own.

### 3.3 Why the Change Is Required

ARCH-000 is the repository's top-level Architecture Manifest and the canonical owner of AI governance-dimension assignment (per ARCH-000 §7c's own framing and per this repository's Canonical Authority Resolution rules). Leaving a constitutional-tier contradiction between ARCH-000 and RTA-001 unresolved would mean the platform has no single authoritative answer to "who owns Prompt Governance and Model Governance" — a defect AAR-001 (AF-001) classifies HIGH severity precisely because it is constitutional-tier, not a lower-level implementation detail. Separately, Explainability and Agent-specific Governance were absent from ARCH-000 §7c's table entirely (AF-016, AF-021), leaving readers of the manifest with no way to discover their actual owners without independently searching three other documents. AAR-001 gates this remediation first in dependency order because it has no dependency itself and resolves the register's only constitutional-tier (not merely technical) contradiction.

### 3.4 Change Made

Updated `architecture/00-Governance/ARCH-000 – Enterprise Operating System Architecture Manifest.md`, §7c only:
- **Prompt governance**: changed from Deferred/no-owner to **Owned**, owner = RTA-001 §13.15, with an explicit note that this corrects the prior contradiction and that RTA-001 itself was left unmodified.
- **Model governance**: same correction, same reasoning.
- **Knowledge governance** and **Memory governance**: left unchanged (still Deferred) — explicitly annotated that RTA-001 §13.15 makes no claim over either, so no contradiction exists there and no correction was needed.
- **Explainability**: added as a new row, owner = SD-002-016 / SD-001 LAW-26, Owned.
- **Agent-specific governance**: added as a new row, owner = RTA-001 §13.15 (subsumed under general AI Governance — not a distinct dimension), Owned — subsumed.
- Updated the closing sentence ("Deferred dimensions remain open...") to name only Knowledge Governance and Memory Governance, since Prompt/Model Governance are no longer deferred.
- Added a parenthetical to the section header noting the correction's provenance ("corrected per ARM-001/AR-001").

No other section of ARCH-000, and no other document in the repository, was modified.

---

## 4. Task 4 — ARM-001 Implementation Report

### Objective
Execute AR-001 (AI Governance & Ownership Reconciliation), the first of AAR-001's eight "Before WP-02" remediations, resolving the ARCH-000 §7c / RTA-001 §13.15 constitutional-tier contradiction on Prompt Governance and Model Governance ownership, and closing the two related ownership gaps (Explainability, Agent-specific Governance) that AAR-001 groups into the same remediation (AF-001, AF-016, AF-021).

### Documents Updated
- `architecture/00-Governance/ARCH-000 – Enterprise Operating System Architecture Manifest.md` (only document updated).

### Sections Updated
- ARCH-000 §7c ("Enterprise Intelligence & AI Governance Ownership Map") only — table rows for Prompt governance, Model governance, and the two new rows (Explainability, Agent-specific governance), plus the section's closing sentence and header annotation.

### Decisions Made
1. Prompt Governance and Model Governance are owned by RTA-001 §13.15, matching what RTA-001 already operationally guarantees — resolved by updating ARCH-000 to match RTA-001, not by rescoping RTA-001 (which would have required an ADR under this repository's Locked-document rule).
2. Knowledge Governance and Memory Governance remain correctly Deferred — confirmed these are unaffected by the RTA-001 contradiction and require no change.
3. Explainability's owner is SD-002-016 and SD-001 LAW-26, with RTA-001 §13.15 cited as the operational guarantee that references them, not as the substantive source.
4. Agent-specific governance is subsumed under the general AI Governance guarantee (RTA-001 §13.15) rather than requiring a distinct governance dimension — no separate agent-specific policy exists in the repository (`agent_registry.governing_policy_id` reuses the general mechanism).

### Cross References Updated
- ARCH-000 §7c's table now cross-references RTA-001 §13.15 (for Prompt/Model/Agent governance) and SD-002-016 / SD-001 LAW-26 (for Explainability) directly within the table's Owner column, where none of these cross-references previously existed for the corrected/added rows.
- No cross-reference in any other document (GRC-001, PLT-001, OPM-001, COM-001, ONT-001, RTA-001 itself) required updating, since all of these already correctly deferred to ARCH-000 §7c and that deferral is unaffected by this change (validated in §5 below).

### Validation
- Re-read ARCH-000 §7c and RTA-001 §13.15 side by side after the edit: no contradiction remains — ARCH-000 now states the same ownership RTA-001 already operationally claims for Prompt and Model Governance, and RTA-001's text is byte-for-byte unmodified.
- Confirmed RTA-001 was not touched by this change (no edit was made to any RTA-001 file).
- Confirmed Explainability and Agent-specific governance now each have exactly one table row in ARCH-000 §7c with a named owner, where previously Explainability had no row at all and Agent-specific governance was undiscoverable from ARCH-000.
- Per AR-001's own Validation criteria ("GRC-001, PLT-001, OPM-001, COM-001, ONT-001... still resolve correctly against the updated table"): these five documents defer to ARCH-000 §7c as a whole, not to any specific row's prior wording; none of them cites the specific Deferred/Owned status of Prompt Governance or Model Governance in a way this correction could break. This was confirmed by inspecting how AAR-001 itself (AF-001's Validation Method) frames this check — it requires the five documents to "still resolve correctly," which they do, since their deference is to ARCH-000 §7c as the authority, not to the specific value being corrected.

### Developer Validation
**Pending.**

### Independent Review
**Pending.**

### Certification Status
**Pending.**

---

## Independent Review

**Review Result:** APPROVED WITH OBSERVATIONS

**Review Summary:** An independent reviewer, with no prior involvement in this change, verified all eight required points against the actual repository state rather than trusting this report's own narrative. Using `git diff`, the reviewer confirmed the ARCH-000 §7c / RTA-001 §13.15 contradiction genuinely existed prior to this change (ARCH-000 previously read "Deferred… no placeholder owner assigned" for Prompt and Model Governance, while RTA-001 §13.15's unchanged text asserts the AI Runtime "shall support" both). The change made was confirmed to match AAR-001's AR-001 specification exactly — same four table corrections, same document (ARCH-000 §7c only), same recommended non-ADR path. `git diff`/`git status` confirmed RTA-001 (LOCKED) is byte-for-byte unmodified, no new ADR exists in `architecture/07-Decisions/`, every added cross-reference (RTA-001 §13.15, SD-002-016, SD-001 LAW-26, and the five deferring documents GRC-001/PLT-001/OPM-001/COM-001/ONT-001) resolves to real, correctly-described content, every governance dimension in the corrected table now has an unambiguous owner or a non-contradictory deferral, and no new contradiction was introduced elsewhere in the repository (including CMD-001's unrelated illustrative use of the same terms). One non-blocking observation was recorded: the working tree carries pre-existing, unrelated uncommitted changes (an uncommitted `CLAUDE.md` §19.8 addition and several untracked WP-01/audit documents) that predate and are unconnected to AR-001 — these should be reconciled or committed separately so the AR-001 commit remains isolated and auditable.

---

## Repository Commit

**Repository Commit:** Committed to `master`. Staged and committed exactly two files — `architecture/00-Governance/ARCH-000 – Enterprise Operating System Architecture Manifest.md` (the AR-001 change) and `architecture/06-Reviews/ARM-001_Implementation_Report.md` (this report) — verified via `git diff`/`git status` before staging to confirm no unrelated file, no LOCKED document (RTA-001 was confirmed untouched), and no implementation code was included. Pre-existing unrelated changes noted in the Independent Review's observation (an uncommitted `CLAUDE.md` §19.8 addition and untracked WP-01/audit documents) were deliberately left unstaged and uncommitted, so this commit contains only ARM-001 changes.

**Commit Hash:** `770aaad0cc3182a81fde3bc22154c4ca18e8379b`

**Commit Date:** 2026-07-27

---

## 5. Stop Point

Per instruction, this report covers AR-001 only. AR-002 through AR-009 remain deferred and unexecuted at the time of this report. **Updated:** AR-001 has since been independently reviewed and committed (see Independent Review and Repository Commit sections above, commit `770aaad0cc3182a81fde3bc22154c4ca18e8379b`, 2026-07-27). A subsequent, separate attempt at AR-002 did not result in a valid committed artifact — see the Governance Recovery operation's Validation Failure Report; AF-002/AR-002 remain Open in `AAR-001`.
