# CAR-001 — Capability Amendment Report

## PE-001-C003 (Role & Permission Management) — Version 1.0 → 1.1, EX-C003-11

**Document ID:** CAR-001
**Document Type:** Capability Amendment Report. This is a **business capability engineering activity, not a Work Package implementation activity.** No `IRA-006` was created. No Work Package was initialized. No implementation code, schema, API, service, or test was written.
**Trigger:** Repository-owner acceptance of `BCGA-001_C003_Domain_Permission_Query_Access_Gap_Assessment.md` and an explicit instruction to amend `PE-001-C003` to resolve the accepted gap before any Work Package is chartered.
**Amended artifact:** `docs/Product/PE-001/capabilities/C-003/PE-001-C003_Role_Permission_Management.docx` — Version 1.0 → **Version 1.1**.
**Date:** 2026-07-31

---

## 1. The Accepted Gap

`BCGA-001` established, with direct textual evidence extracted from `PE-001-C003` itself (the `.docx` was unzipped and its raw XML read directly, not inferred secondhand), that:

- `PE-001-C003 Chapter 4` engineered exactly ten Enterprise Experiences, all already implemented by WP-02, none of which retrieves, displays, or lists an authorization policy object's current state.
- `Chapter 3`'s own `ERB-C003-01` overview declares its Experience Lifecycle Mapping as **"Discover, Understand, Decide, Transition"** — but `Chapter 4` authored Enterprise Experiences realizing only the *Decide, Transition* stages (the five "Establish X" experiences, `EX-C003-01` through `05`). No Enterprise Experience realized the *Discover* or *Understand* stages `ERB-C003-01` itself already declared as part of its own lifecycle.
- This gap was undisclosed, not deliberately deferred — no `Pending Canonical Binding` marker or `Chapter 9.6` Experience Decision Record entry addressed it anywhere in the specification's own text.

`BCGA-001`'s recommendation — one minimum, additive Enterprise Experience, `EX-C003-11` ("Understand Domain Permission Context"), added under the existing `ERB-C003-01` — is the amendment this report records.

---

## 2. Amendment Performed

### 2.1 Method

`PE-001-C003_Role_Permission_Management.docx` is a binary `.docx` (a ZIP archive of OOXML). The amendment was performed by: unzipping the archive, editing `word/document.xml` directly via precise, anchored text substitutions and one structural insertion (each verified for uniqueness before being applied — no substitution was made against an ambiguous or non-unique anchor), validating the result as well-formed XML (`xml.etree.ElementTree.fromstring`, passed) and as a valid ZIP archive (`zipfile.testzip()`, passed — no corrupted member), then replacing the original file. Every other archive member (`styles.xml`, `numbering.xml`, `comments.xml`, etc.) was copied byte-for-byte unchanged. The original file was under git version control with no uncommitted changes before this amendment began, providing a clean rollback point if any step had failed (`git checkout -- <path>` would have restored it; not needed — every validation passed).

### 2.2 New Enterprise Experience

**`EX-C003-11` — Understand Domain Permission Context**, inserted into `Chapter 4` physically between `EX-C003-06` and `EX-C003-07` (grouping it with its own governing ERB's other Enterprise Experiences, consistent with `Chapter 4`'s own reading order) while keeping its ID number `11` — the next sequential, unused EX number — per the explicit instruction to preserve all existing numbering.

| Field | Value |
|---|---|
| Governing ERB | `ERB-C003-01` (unchanged — no new ERB introduced) |
| Trigger | A Corporate Admin, Domain Admin, or Domain Owner needs to confirm the current state of a specific Domain Permission, or to determine which Domain Permissions currently exist for a given Domain or Membership, before proposing a new grant, a lifecycle change, or reviewing a reported dependency. |
| Purpose | Retrieves the current governed state of a specific Domain Permission by its own identity, or a filtered list of Domain Permissions matching a stated Domain, Membership, or status criterion, without establishing, versioning, deprecating, retiring, or otherwise altering any object it returns. |
| Participating Personas | Corporate Admin (`URA-001-32`); Domain Owner (`URA-001-45`); Domain Admin (`URA-001-46`) — the same defining-authority personas `ERB-C003-01` already establishes for Domain Permission. |
| Context Consumed | The Domain Permission's own current governed state, as produced by `EX-C003-02` (establishment), `EX-C003-07` (versioning), or `EX-C003-08` (deprecation/retirement) — never re-derived or independently computed. |
| Context Produced | The requested Domain Permission's own current state, or a matching list, presented exactly as governed. |
| AI Assistance | AI MAY summarize current state or identify likely-duplicate/inconsistent grants (Contract 5.8); AI SHALL NOT establish, amend, deprecate, retire, or approve any object it surfaces. |
| Lifecycle Participation | **Discover, Understand** — the two `ERB-C003-01` lifecycle stages no prior Enterprise Experience realized. |
| Business Activity References | Pending Canonical Binding (same convention as all ten pre-existing EXs). |

The full field set (Trigger, Purpose, Business Goal, Business Value, Participating Personas, Participating Workspaces, all seven Context Engineering dimensions, Navigation/Collaboration Expectations, AI Assistance, Experience Outcome, Success Criteria, Experience Completion, Lifecycle Participation, Business Activity References) was authored by cloning `EX-C003-02`'s own XML structure verbatim and substituting content — every formatting element (heading style, metadata table, spacing, run properties) is identical in kind to its ten siblings.

### 2.3 Contract extension (no new Contract)

`Contract 5.1` (Authorization Policy Definition Authority) received one new bullet, extending — not replacing — its existing three:

> "The same defining-authority personas confirmed under this Contract to establish, version, deprecate, or retire an authorization policy object SHALL also be authorized to view its current governed state (`EX-C003-11`, added Version 1.1); viewing confers no authority to establish, amend, deprecate, retire, or approve any object."

`Chapter 5`'s Contract count remains **eight**, unchanged — per `BCGA-001 §5.1`'s own stated preference for the minimal-structure option where an existing Contract can be extended rather than a ninth invented.

### 2.4 Cross-references synchronized

Every place in the document that enumerated Enterprise Experience counts, ID lists, or completeness claims was located and updated, not only the two `BCGA-001` had already flagged:

| Location | Before | After |
|---|---|---|
| `Chapter 1` summary | "three-ERB / ten-EX / eight-Contract" | "three-ERB / eleven-EX / eight-Contract" (with the Version 1.0 baseline figure preserved as history) |
| `Chapter 4` opening | "This chapter engineers ten Enterprise Experiences" | "eleven Enterprise Experiences" |
| `Chapter 9.5` completeness narrative | "ERB-C003-01 → EX-C003-01/02/03/04/05/06 ... ten EXs traces to exactly one governing ERB" | "...EX-C003-01/02/03/04/05/06/11 ... eleven EXs..." |
| `Appendix B` — ERB-to-EX Map | `ERB-C003-01` row: "EX-C003-01, ..., EX-C003-06" | "...EX-C003-06, EX-C003-11" |
| `Appendix C` — Publication Conformance Checklist | "Three ERBs and ten EXs derived independently" | "Three ERBs and eleven EXs (ten derived independently at Version 1.0; EX-C003-11 added at Version 1.1 per BCGA-001)" |
| `Chapter 8`/`Chapter 9.16` validation statements | "assessed as publication-ready at Version 1.0" / "APPROVED ... Version 1.0" | "Version 1.1", each with an added sentence stating the amendment re-validates only its own added content and does not reopen the Version 1.0 baseline |
| Title page, Document Control table | "Version 1.0" (×2) | "Version 1.1" |
| Revision History table | (1.0 row only) | 1.0 row preserved unedited; new 1.1 row added describing this amendment |

No occurrence of "ten Enterprise Experiences," "ten EXs," or "Version 1.0" remains anywhere in the document **except** as a deliberate historical citation (the original 1.0 Revision History row, and the amendment's own new text explicitly distinguishing what the Version 1.0 baseline established from what Version 1.1 added). Every such remaining occurrence was individually reviewed and confirmed correct in context (§4 below).

---

## 3. Rationale

Every choice made in §2 traces to `BCGA-001`'s own §5/§5.1 analysis, adopted without deviation:

- **New EX under the existing ERB, not a new ERB** — `ERB-C003-01`'s own text already declares "Discover, Understand" as part of its own lifecycle mapping; the gap is an unrealized stage of an existing ERB, not a missing ERB.
- **One EX, not two (view and query bundled)** — `PE-001-C003` already has precedent for bundling a query concern into a single EX (`EX-C003-09`, "Query + Update"); no evidenced, materially distinct cross-boundary audit need exists to justify a second EX (unlike `C-007`'s own evidenced split between `EX-C007-03` and `EX-C007-07`).
- **Scoped to Domain Permission, not all six object types** — matching the repository owner's own stated WP-06 scope; the identical gap for the other five types is real (`BCGA-001 §6.3`) but not addressed here, avoiding recommending five additional EXs to close a gap only one was asked about.
- **Contract extension, not a new Contract** — the visibility rule is a minimal, natural extension of Contract 5.1's own existing statement of who owns the definitional structure; inventing a ninth Contract for a single clarifying sentence would not be the minimum sufficient change.

---

## 4. Internal Consistency Verification

Performed directly against the amended document (re-extracted and read in full after the amendment, not assumed from the edit script's own success):

| Check | Result |
|---|---|
| Enterprise Experiences complete | **Pass.** Eleven `EX` headings confirmed present, in document order, each with its own metadata table (`EX` ID, Governing ERB) and full field set. No duplicate ID, no missing field. |
| Lifecycle mappings internally consistent | **Pass.** `ERB-C003-01`'s own declared "Discover, Understand, Decide, Transition" is now fully realized across its six Enterprise Experiences: `EX-01`–`05` each declare "Discover, Decide, Transition"; `EX-06` declares "Discover, Complete"; `EX-C003-11` declares "Discover, Understand" — the two stages no prior EX covered. |
| Business Rules remain valid | **Pass.** `BR-C003-01` through `08` were read in full post-amendment; none required a wording change. `EX-C003-11` cites `BR-C003-01` (duplicate-prevention) and `EX-C003-09` (dependency review) accurately, as read-only downstream consumers of state those rules already govern. |
| Cross-references remain correct | **Pass.** `EX-C003-11` references `ERB-C003-01`, `Contract 5.1`, `Contract 5.8`, `EX-C003-02`, `EX-C003-07`, `EX-C003-08`, `EX-C003-09` — every one verified to exist, unrenumbered, with the meaning `EX-C003-11`'s own text ascribes to it. |
| No unintended impacts | **Pass.** A full-document diff-equivalent check (re-extracted plain text, grep across the entire document) confirmed every remaining "ten Enterprise Experiences"/"ten EXs"/"Version 1.0" occurrence is a deliberate historical citation (§2.4), not a missed or contradictory reference. No existing EX, ERB, Contract, or Business Rule was renumbered, relocated, or altered in substance. |
| Document validity | **Pass.** `xml.etree.ElementTree.fromstring` parsed the amended `word/document.xml` without error; `zipfile.testzip()` reported no corrupted archive member; the amended file re-opens as a valid 22-member `.docx` archive. |

---

## 5. Change Impact Analysis

| Dimension | Impact |
|---|---|
| **Business Rules** | None altered. `EX-C003-11` introduces no new Business Rule (`BR-C003-09` was considered and rejected in favor of the Contract 5.1 extension — a rule this narrow did not warrant its own numbered entry, per the same minimum-sufficient-change discipline `BCGA-001 §5.1` already applied). |
| **Domain Model** | None. No new entity, table, or column is introduced by this amendment — `EX-C003-11` is a business-capability-layer addition only. Any schema implication (e.g., what a "query by status" filter maps to) is deferred to a future `IRA-006`, explicitly not drafted here. |
| **APIs** | None built. `EX-C003-11` authorizes a future API (e.g., a `GET` endpoint on Domain Permission) to exist; it does not itself specify or implement one. |
| **Services** | None. No service code was written or modified. |
| **Security** | Contract 5.1's extension is the only security-relevant change: it makes explicit, for the first time, that the same defining-authority personas who may establish/govern a Domain Permission may also view it — closing an authorization-model ambiguity a future implementation would otherwise have had to infer. No existing authorization boundary is loosened or removed. |
| **Audit** | None yet. A future implementation of `EX-C003-11` would need its own audit requirements (mirroring every other WP-02/WP-05 Business Activity's own `record_audit()` discipline) — not specified by this capability-layer amendment, which states business intent, not implementation mechanics. |
| **Existing Work Packages** | None. WP-02's own `CLOSED — Certified` status and all nine of its already-certified Business Activities are unaffected — this amendment is purely additive to the specification, not a reopening of any implemented, certified code. |
| **Future Work Packages** | WP-06 (or whatever Work Package eventually implements `EX-C003-11`) now has a governing Enterprise Experience to draft an `IRA` against — the precise blocker `BCGA-001` identified is closed. The identical, still-open gap for the other five authorization policy object types (`BCGA-001 §6.3`) remains available for a future, separately-scoped capability amendment, not implied or pre-authorized by this one. |

### 5.1 Additional documentation requiring amendment

- `DOC-000_Documentation_Catalogue.md` — `BCGA-001`'s own row updated from "repository-owner decision pending" to "Accepted and acted upon," and this report (`CAR-001`) indexed. (Completed in the same pass as this report, per `WP-REG-001 §3`'s own documentation-tense discipline, itself adopted from `METH-002` following WP-05's own governance-staleness finding — the same lesson applied here rather than left to a future reviewer to rediscover.)
- `WPR-001` / `WP-REG-001` — **not modified.** WP-06 remains uncharted, per the explicit instruction not to initialize it. These registers track Work Package execution status, not capability specification versions; nothing in their own scope changed.
- `IRA-006` — **not created**, per explicit instruction.

---

## 6. Recommendation

`PE-001-C003` Version 1.1 is internally consistent, complete against its own declared lifecycle model, and introduces no unauthorized architecture (no new entity, table, API, service boundary, or ERB — `CLAUDE.md §18`'s own prohibition list is fully respected; the amendment is confined to the capability specification layer, which is the layer `BCGA-001` identified as incomplete). Every verification in §4 passed against the actual amended document, not against the edit script's own claims.

**"PE-001-C003 is approved as the authoritative business specification for chartering WP-06."**

---

*End of CAR-001. Execution ends here — no IRA-006, no Work Package initialization, no implementation code.*
