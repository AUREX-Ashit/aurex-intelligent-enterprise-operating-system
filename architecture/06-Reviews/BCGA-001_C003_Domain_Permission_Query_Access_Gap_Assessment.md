# BCGA-001 — Business Capability Gap Assessment

## C-003 (Role & Permission Management) — Domain Permission Viewing & Querying

**Document ID:** BCGA-001
**Document Type:** Business Capability Gap Assessment. Not an IRA, not an ADR, not an amendment to `PE-001-C003`. Advisory only — produced for repository-owner review to determine whether `PE-001-C003` should be amended before WP-06 is chartered.
**Trigger:** A repository-owner request to charter WP-06 for "C-003 — Domain Permission Read APIs." Before drafting `IRA-006`, the governing capability specification was checked and found not to authorize this scope (per `CLAUDE.md §17`'s mandatory STOP-and-report requirement).
**Author posture:** Same session that identified the gap. This assessment is fact-finding and recommendation only — it makes no implementation decision, edits no governing document, and does not itself authorize any Enterprise Experience.
**Date:** 2026-07-31

---

## 1. Executive Summary

`PE-001-C003` (Role & Permission Management) does not authorize a Domain Permission read or query capability. Its own Chapter 4 engineers exactly ten Enterprise Experiences, all already implemented by WP-02, none of which retrieves, displays, or lists the current state of a Domain Permission (or any other authorization policy object). This is not a deliberately scoped exclusion the specification discloses and defers — no `Pending Canonical Binding` marker, no `Chapter 9` "Explicitly Not Decided" entry, and no `Chapter 9.6` Experience Decision Record addresses it anywhere in the document's own text.

More specifically: `PE-001-C003 Chapter 3` states `ERB-C003-01`'s own Experience Lifecycle Mapping as **"Discover, Understand, Decide, Transition"** (`PE-001 §16.2`'s canonical four-stage model) — but `Chapter 4` authors only the Enterprise Experiences realizing the *Decide/Transition* stage (`EX-C003-02` "Establish Domain Permission," and its four sibling per-type establishment EXs). No Enterprise Experience realizes the *Discover* or *Understand* stages `ERB-C003-01` itself already declares. The specification's own internal validation (`Chapter 9.5`) checked only that "every ERB has at least one realizing EX" — a weaker bar than "every stage of every ERB's own declared lifecycle mapping is realized" — so this gap exists beneath the document's own QA threshold, not despite it.

**Recommendation:** one minimum, additive Enterprise Experience — `EX-C003-11`, "Understand Domain Permission Context" — closes this specific gap without redesigning any existing EX, ERB, or Contract. `PE-001-C003`'s own three-ERB structure absorbs it without amendment; only `Chapter 4`'s EX count (ten → eleven) and `Chapter 5`'s Contract count (eight → nine, or fewer if the new EX reuses an existing Contract) change.

---

## 2. Scope of This Assessment

**In scope:** Whether `PE-001-C003`, as currently approved, authorizes any Enterprise Experience under which viewing or querying a Domain Permission's current state could be implemented; if not, the minimum additional Enterprise Experience(s) that would close the gap.

**Out of scope, per explicit instruction:**
- No edit to `PE-001-C003` is made or proposed as a drafted amendment — only a recommendation.
- No `IRA-006` is drafted.
- No implementation, schema, API, or test code is written.
- The identical gap likely exists for the other five authorization policy object types (`Role`, `Approval Authority`, `Delegation Policy`, `Runtime Assignment Policy`) — noted in §6.3 as a related finding, but this assessment's own recommendation is scoped to Domain Permission specifically, matching the repository-owner's own stated WP-06 scope.

---

## 3. Methodology

`PE-001-C003_Role_Permission_Management.docx` is a binary `.docx` file — the same class of limitation `VV-AUDIT-WP-05` disclosed for `PE-001-C002` (unreadable as text by the tools normally available). Rather than relying on `IRA-002`'s own secondhand summary of it (the approach the prior review used), this assessment extracted the document's actual text directly: the `.docx` was unzipped (a `.docx` is a ZIP archive), `word/document.xml` was extracted, and XML markup was stripped to recover the specification's own verbatim prose, paragraph by paragraph. Every quotation and citation below is drawn from that direct extraction, not from `IRA-002`'s paraphrase, and can be independently reproduced by the same method.

Cross-checked against: `IRA-002_WP-02_Role_Permission_Management_Implementation_Readiness_Assessment.md` (the derived Business Activity list WP-02 actually implemented), `IMP-REPORT-WP-02_Role_Permission_Management.md`, `TECH-DEBT.md` (`TD-022`, `TD-027`, `TD-028`, the only Domain-Permission-adjacent entries found), and direct inspection of `Backend/Services/AuthService/routers/domain_permission.py` (confirmed: seven `POST` endpoints — `establish`, `version`, `deprecate`, `retire`, `check-dependencies`, `resolve-dependency`, `report-handoff-rejection` — zero `GET` endpoints).

---

## 4. Why Domain Permission Read APIs Cannot Be Implemented Under the Current Approved PE-001-C003

### 4.1 The complete, self-described-complete Enterprise Experience list

`PE-001-C003 Chapter 4` opens: *"This chapter engineers ten Enterprise Experiences, each governed by exactly one ERB from Chapter 3."* The ten, verbatim from the extracted document:

| EX | Title | ERB |
|---|---|---|
| EX-C003-01 | Establish Business or System Role | ERB-C003-01 |
| EX-C003-02 | Establish Domain Permission | ERB-C003-01 |
| EX-C003-03 | Establish Approval Authority | ERB-C003-01 |
| EX-C003-04 | Establish Delegation Policy | ERB-C003-01 |
| EX-C003-05 | Establish Runtime Assignment Policy | ERB-C003-01 |
| EX-C003-06 | Produce Rejected or Unresolved Authorization Policy Definition Outcome | ERB-C003-01 |
| EX-C003-07 | Version and Re-effective-Date Authorization Policy Object | ERB-C003-02 |
| EX-C003-08 | Deprecate or Retire Authorization Policy Object | ERB-C003-02 |
| EX-C003-09 | Detect and Resolve Authorization Policy Dependency Conflict | ERB-C003-03 |
| EX-C003-10 | Resolve Dependent Capability Authorization Policy Hand-off Rejection | ERB-C003-03 |

All ten are already implemented — this is exactly WP-02's own nine Business Activities (`EX-C003-06` realized inline within `EX-C003-01`'s own service method, per `IRA-002 §2.9`). **None of the ten retrieves, displays, or lists an authorization policy object's current state.** `EX-C003-09` is the closest ("Query + Update," per `IRA-002`'s own typing) but its query is narrowly scoped to *dependency conflicts on a proposed change* — it does not expose a general-purpose way to look up a Domain Permission by identity or to list Domain Permissions matching a criterion.

### 4.2 The specification's own declared lifecycle mapping is only partially realized

`Chapter 1.7` states the capability's own high-level progression: *"Define (Discover, Understand, Decide, Transition) → Govern Lifecycle (Execute, Validate, Transition) → Resolve Dependency/Hand-off (Validate, Transition) → Complete."*

`Chapter 3`'s own `ERB-C003-01` overview restates this specifically for the Define ERB: **"Experience Lifecycle Mapping — Discover, Understand, Decide, Transition (PE-001 16.2)."**

`Chapter 4` then authors `EX-C003-01` through `EX-C003-05` — five Enterprise Experiences, one per authorization policy object type — each realizing only the *Decide, Transition* portion of that four-stage mapping (each is titled "Establish X," a decision-and-transition verb). **No Enterprise Experience anywhere in the document realizes the *Discover* or *Understand* stages `ERB-C003-01` itself already declares as part of its own lifecycle.** This is not an inference from silence; it is the specification's own stated model for its own first ERB, left partially unrealized by its own Chapter 4.

### 4.3 The gap is undisclosed, not deliberately deferred

`PE-001-C003` is careful and explicit everywhere it *does* defer something: every unresolved traceability identifier is marked `Pending Canonical Binding` (Business Activity/EAC bindings, Enterprise Journey identifiers, Autonomous Agent defining-authority), and `Chapter 9.6`'s own "Experience Decision Record" documents two considered-and-rejected design alternatives (differentiating the six establishment ERBs further; a local "Authorization Runtime Context" construct) with explicit reasoning for each rejection. Searching the full extracted text for any comparable disclosure of a deferred read/view/query capability — `Pending Canonical Binding`, `out of scope`, `future`, `deferred` — returns nothing addressing this gap. The document's own internal validation claim (`Chapter 9.5`, echoed at `Chapter 4`'s own opening line) is only that "every ERB has at least one realizing EX" — true, and satisfied — but that is a materially weaker bar than "every stage of every ERB's own declared lifecycle mapping is realized," which is not true for `ERB-C003-01`'s *Discover/Understand* stages. The gap exists beneath the specification's own stated validation threshold; it was not found because it was not the thing being checked for, not because it was checked for and excluded.

### 4.4 Confirmed independently: no implementation exists, and nothing in this repository currently needs one

Direct inspection of `Backend/Services/AuthService/routers/domain_permission.py` confirms zero `GET` endpoints exist. `TECH-DEBT.md`'s only Domain-Permission-adjacent entries (`TD-022`, authorization-persona gap; `TD-027`, concurrent-versioning race; `TD-028`, `has_active_dependents()` always-`False` for Domain Permission) do not mention a missing read path — this specific gap has never been previously disclosed anywhere in the repository's own governance trail, including by WP-02's own Independent Review or Certification. No other capability's code currently queries `DomainPermission` records directly (notably, WP-05's own Access Evaluation `BA-01` queries `Membership`, `Domain`, and `ApprovalAuthority`, but never `DomainPermission`) — there is no existing internal-technical-dependency justification either, only the specification-level gap identified above.

### 4.5 Conclusion

Per `CLAUDE.md §17`: *"If the required behaviour, structure or business rule is not explicitly documented... STOP... Never fill architectural or business gaps using assumptions."* `PE-001-C003` does not document a Domain Permission viewing or querying capability, under any of its ten Enterprise Experiences, and does not disclose this as a deliberate exclusion. Implementation cannot proceed under the current approved specification without inventing business requirements the specification itself never authorized — exactly what `§17` prohibits.

---

## 5. Recommended Minimum Additional Enterprise Experience

One new Enterprise Experience, added under the existing `ERB-C003-01`, closes the gap identified in §4 without amending any other part of `PE-001-C003`'s structure.

### EX-C003-11 — Understand Domain Permission Context

| Attribute | Value |
|---|---|
| **Experience ID** | `EX-C003-11` |
| **Name** | Understand Domain Permission Context |
| **Governing ERB** | `ERB-C003-01` (Define Authorization Policy Structure) — realizes the *Discover, Understand* stages of that ERB's own already-declared Experience Lifecycle Mapping (§4.2), left unrealized by `EX-C003-02` alone. |
| **Business objective** | Enable an authorized caller to retrieve the current state of a specific, identified Domain Permission grant, and to query/list Domain Permission grants matching stated criteria (e.g., by Domain, by Membership, by current status), so the caller can confirm what authorization policy currently exists before acting on it or reasoning about it. |
| **Business justification** | `ERB-C003-01`'s own declared lifecycle requires a *Discover/Understand* stage that no Enterprise Experience currently realizes for any of the six object types (§4.2). For Domain Permission specifically, this is not merely a documentation gap: `EX-C003-02`'s own duplicate-prevention rule (`BR-C003-01`) and `EX-C003-09`'s dependency-conflict review both presuppose a caller can determine what already exists, yet the specification provides no Enterprise Experience — and consequently no API — through which that determination is made. Today it can only be done by direct database inspection, outside any governed Enterprise Experience. |
| **Relationship to existing experiences** | Strictly downstream and read-only. Consumes `EX-C003-02`/`07`/`08`'s own `Context Produced` (the object's current version/state) — never mutates it, never gates it, never duplicates their own decision logic, and produces no new Context construct beyond what those experiences already establish. Directly supports: `EX-C003-02` (checking for an existing grant before proposing a new one, avoiding a blind `409`); `EX-C003-07`/`08` (confirming current state before proposing a version, deprecation, or retirement); `EX-C003-09` (inspecting the specific grant named in a reported dependency). |
| **Customer-facing or internal** | Both, primarily internal/administrative. Participating Personas mirror `ERB-C003-01`'s own (`Corporate Admin`, `Domain Admin`, `Domain Owner` — the same personas already authorized to establish and govern Domain Permission, per `PE-001-C003 Chapter 1.9`/`3`, now also authorized to view what has been established). Also the technical foundation any future dependent capability would need were it to begin consulting Domain Permission grants directly (no such consumer exists today — see §4.4). |

### 5.1 Alternatives considered and rejected

Mirroring `PE-001-C003`'s own `Chapter 9.6` Experience Decision Record discipline — documenting what was *not* proposed, and why, rather than silently omitting it:

- **A separate EX for single-item view versus list/query, mirroring `PE-001-C007`'s own split between `EX-C007-03` (Understand Membership Context) and `EX-C007-07` (Surface Multi-Organization Membership Awareness).** Rejected: that split was justified there by a materially different business purpose and a distinct, evidenced Participating Persona (Platform Oversight Participant, auditing across an organizational boundary the subject's own single-item view does not cross). No comparable, evidenced cross-boundary audit need exists for Domain Permission today (§4.4) — `PE-001-C003` itself already establishes precedent for bundling a query concern into a single EX (`EX-C003-09`, typed "Query + Update"). Proposing a second EX ahead of an evidenced need would violate the same anti-template, anti-invention discipline `PE-001-C003`'s own `Chapter 9.6` already applies to itself.
- **One Understand/Query EX per authorization policy object type (five total, mirroring `EX-C003-02` through `05`'s own per-type differentiation for Establish).** Rejected for this assessment's own scope: the repository-owner's stated WP-06 scope is Domain Permission specifically (§2), and the identical gap for the other five types, while real (§6.3), has not been independently evidenced or requested here. Recommending five new EXs to close a gap only one of them was asked about would exceed "minimum."
- **A new ERB, rather than a new EX under the existing `ERB-C003-01`.** Rejected: `ERB-C003-01`'s own text already declares "Discover, Understand" as part of its own Experience Lifecycle Mapping (§4.2) — the gap is an unrealized stage of an existing ERB, not a missing ERB. Adding a new ERB would contradict the specification's own stated model rather than complete it.

---

## 6. Impact Assessment

### 6.1 Effect on PE-001-C003's own structure, if adopted

- `Chapter 4`'s Enterprise Experience count: ten → eleven.
- `Chapter 3`'s ERB count: unchanged (three). `ERB-C003-01`'s own Experience Lifecycle Mapping becomes fully realized for the first time.
- `Chapter 5`'s Capability Experience Contract count: potentially unchanged at eight, if `EX-C003-11` is realized under an existing Contract shape (a read-only Contract variant of `EX-C003-02`'s own), or nine if a dedicated Contract is warranted — this determination is deferred to the amendment itself, not made by this assessment.
- No existing EX, ERB, Contract, Business Rule, or Invariant is altered, redefined, or relocated.

### 6.2 Effect on WP-02's own certified status

None. `EX-C003-11` is purely additive read access to an object WP-02 already establishes and governs — it does not reopen, modify, or require re-certification of any of WP-02's own nine already-certified Business Activities.

### 6.3 Related finding: the same gap likely exists for the other five object types

`EX-C003-01`, `03`, `04`, `05` (Establish Role, Approval Authority, Delegation Policy, Runtime Assignment Policy) share the identical structural gap `EX-C003-02` has — none of the other four object types has a realized *Discover/Understand* Enterprise Experience either, for the same textual reason (§4.2 applies to all five equally, not to Domain Permission specifically). This assessment does not recommend closing that broader gap now — it is noted here so the repository owner can decide whether to charter it alongside `EX-C003-11` or address it in a later, separately-scoped assessment, consistent with `CLAUDE.md §19.5`'s Reuse→Configure→Extend→Compose→Create discipline (the smallest sufficient scope, not the largest speculative one).

---

## 7. What This Assessment Does Not Do

Per explicit instruction:

- **`PE-001-C003` has not been modified.** No section, ERB, EX, Contract, or Chapter of the governing `.docx` was edited.
- **`IRA-006` has not been drafted.** No Business Activity list, Gap Analysis, or implementation-readiness determination has been produced.
- **No implementation, schema, API, test, or migration has been written.**
- **`WP-REG-001`/`WPR-001` have not been updated** — WP-06 remains uncharted; this assessment is an input to that decision, not the decision itself.

---

## 8. Recommendation to Repository Owner

This assessment recommends `EX-C003-11` ("Understand Domain Permission Context," §5) as the minimum Enterprise Experience required to make Domain Permission viewing and querying implementable under `PE-001-C003`. Three paths forward, for the repository owner's own decision — this assessment does not select among them:

1. **Amend `PE-001-C003`** to add `EX-C003-11` (and its own Contract, per §6.1), then charter `WP-06` under the amended specification and draft `IRA-006` against it.
2. **Decline** — Domain Permission viewing/querying remains unimplemented; `WP-06` is not chartered for this scope. `PE-001-C003` remains unchanged.
3. **Broaden the amendment** to also address §6.3's related finding (the same gap for the other five object types) in the same specification pass, before chartering `WP-06`.

No implementation of any kind should proceed until one of these paths is selected and, if 1 or 3, the corresponding `PE-001-C003` amendment is actually made and approved.

---

*End of BCGA-001.*
