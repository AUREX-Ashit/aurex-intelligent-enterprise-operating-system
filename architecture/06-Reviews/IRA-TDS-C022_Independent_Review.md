# IRA-TDS-C022 — Independent Review of the C-022 Pre-Implementation Governance Gate

**Document type:** Independent Review of a pre-implementation governance gate (`ROD-C022` → `IRA-C022` → `TDS-C022`), performed by a reviewer with no involvement in the drafting of any of the three artifacts under review, per this repository's established no-self-certification discipline (`CLAUDE.md §19.7`, extended by `§19.7b`'s independence requirement to every gate).

**Gate reviewed:** Capability-boundary and technical-design governance for **C-022 Customer & Account Management**, first Business Activity "Establish Commercial Account." No Work Package is registered, no Charter exists, and no implementation exists. This review therefore assesses governance artifacts only — it is not a Gate 1 Certification, a Gate 2 V&V Audit, or a Gate 5 Release Readiness Audit, none of which is yet applicable.

**Reviewed:** 2026-09-15.

**Artifacts under review:**
- `architecture/06-Reviews/ROD-C022-Customer-and-Account-Management-Capability-Boundary-and-Minimum-Scope.md`
- `architecture/06-Reviews/IRA-C022-Customer-and-Account-Management.md`
- `architecture/06-Reviews/TDS-C022_Customer_and_Account_Management_Minimum_BA_Technical_Design.md`

**Classification key:** `[FACT]` — independently verified by this reviewer against the primary source named. `[FINDING]` — a review conclusion. `[CONDITION]` — a mandatory condition attached to the gate decision. `[STOP]` — work that SHALL NOT proceed until a named decision is recorded.

---

## 0. Gate Decision

> ### **PASS WITH CONDITIONS**
>
> The three artifacts are substantially sound. Their central discipline — surfacing conflicts rather than inventing resolutions — was independently confirmed to have been applied honestly, and the single most important judgment in the sequence (refusing to invent a Commercial Account `classification` column) is **correct**. The gate nevertheless does not pass cleanly, because:
>
> - **Two blocking conditions require a fresh, explicit Repository Owner decision before any Charter, WP registration, or implementation work begins** (`[C-1]` classification; `[C-2]` read/list). Both are `[STOP]` items.
> - **Three mandatory corrective conditions** apply to `TDS-C022` before it may be treated as an implementable design (`[C-3]` `COM-001-001` Universal Identity inheritance; `[C-4]` citation misattribution; `[C-5]` commercial lifecycle-pattern conformance).
> - **Two carried-forward conditions** restate hard constitutional gates the artifacts themselves correctly identified (`[C-6]` CBOR; `[C-7]` BAR).
>
> Conditions are stated in full in §9. This review does not resolve any of them, and no condition may be closed by a future implementing session on its own authority.

---

## 1. Scope Reviewed

| # | Review question (from the review mandate) | Addressed in |
|---|---|---|
| A | `IRA-C022` — readiness verdict, dependency identification, hard-dependency test, CBOR/BAR treatment, completeness of risks/assumptions/deferrals | §4 |
| B | `TDS-C022` — scope fidelity, schema conformance to `COM-001-033`, reference generation, scope/hosting carry-forward, authorization derivation, sufficiency for implementation, hierarchy semantics, precedent-vs-semantics discipline | §5 |
| C.1 | Classification — critical scope issue | §6 |
| C.2 | Read/list — critical scope issue | §7 |
| — | Dependency/readiness assessment | §4.2–§4.3, §8.1 |
| — | Security/design assessment | §5.5–§5.7, §8.2 |
| — | Gate decision, conditions, STOP requirements | §0, §9, §10 |

**Out of scope of this review:** C-020 governance; C-021/WP-20 governance (consulted for precedent only); any change to the artifacts under review; any registry, delivery map, CBOR/BAR artifact, code, test, migration, API, or frontend file.

---

## 2. Evidence Independently Re-Derived

This reviewer did **not** accept any quotation appearing in `ROD-C022`, `IRA-C022`, or `TDS-C022`. Every load-bearing citation below was re-read from the primary source.

| Source | How read | Verified |
|---|---|---|
| `architecture/02-Constitutional/COM-001_Commercial_and_Subscription_Architecture.md` | Direct read, §1–§4 (L1–65), §5–§7 (L67–136), §8–§10 + Index + Freeze (L137–216) | ✅ |
| `architecture/02-Constitutional/CAP-001_Enterprise_Capability_Registry.md` | Direct read, line 76 | ✅ |
| `docs/Product/PE-001/capabilities/C-022/PE-001-C022- Customer_and_Account_Management.docx` | Extracted independently (zip → `word/document.xml` → XML-strip → entity-decode) to a scratch directory **outside the repository**; 2,558 lines of plain text; §1.4, §1.5, §1.6, §1.9, §1.14, §1.15, §1.16, §1.17, Ch.3 (ERB-C022-01, -06), Ch.4 (EX-C022-04, -05, -06) read directly | ✅ |
| `architecture/02-Constitutional/CMD-001_Canonical_Data_Model.md` §26.3a | Direct read, L11897–11917 | ✅ |
| `architecture/06-Reviews/ROD-C021-…-Minimum-Scope.md` | D4 / §G / §H read (precedent only) | ✅ |
| `architecture/05-Implementation/TDS-C021_…_Technical_Design.md` | §9.3 / §9.1 / O1 / RTM read (precedent only) | ✅ |
| `architecture/05-Implementation/IRA-C021_…_Readiness_Assessment.md` | §8 CBOR steps read (precedent only) | ✅ |
| `Backend/Services/AuthService/models/c021_offering_definition.py` | Full read (208 lines) | ✅ |
| `Backend/Services/AuthService/models/role.py`, `models/c023_entitlement_context.py`, `middleware/tenant.py`, `dependencies.py`, `routers/offering.py`, `services/offering_definition_service.py` | Targeted read | ✅ |
| `architecture/00-Governance/CBOR-INDEX.md` | Read for existing registrations | ✅ |

---

## 3. Primary-Source Findings (the factual base for everything below)

### 3.1 `COM-001-033` — actual, complete, verbatim text

`[FACT]` `COM-001_Commercial_and_Subscription_Architecture.md`, line 126, Section 7:

> **COM-001-033: Authoritative Account Context**
> The single current, canonical commercial-container fact for a Commercial Account: identity, Account-to-Account hierarchy position, and status. Keyed only to its own Commercial Account Anchor. Never equivalent to a Workspace, Organization, Identity, Membership, or Billing Account.

That is the clause in its entirety. Three attributes: **identity, Account-to-Account hierarchy position, status.** No classification attribute.

### 3.2 `COM-001-032` — actual, complete, verbatim text

`[FACT]` Same file, line 123:

> **COM-001-032: Authoritative Customer Context**
> The single current, canonical identity fact for a Customer: legal-entity or person identity reference, classification, and status. Keyed only to its own Customer Anchor; exactly one per anchor.

Classification is present, and is a **Customer** attribute.

### 3.3 `PE-001-C022 §1.16` — the two context-model rows, verbatim

`[FACT]` **Authoritative Customer Context** row, Meaning column:

> The single current, canonical identity fact for a Customer: legal-entity or person identity reference, classification (e.g., segment, partner/reseller/distributor designation), and current status (active, suspended, retired).

`[FACT]` **Authoritative Account Context** row, Meaning column:

> The single current, canonical commercial-container fact for a Commercial Account: its own identity, its Account-to-Account hierarchy position (parent Account reference, where applicable), and its current status. It does not itself enumerate associated Customers as an identity fact — that association is the Authoritative Customer–Account Relationship Context's concern.

`[FACT]` Same row, Rule column (closing clause):

> …never equivalent to a Workspace, Organization, Identity, Membership, ERP company code, CRM account record, or Billing Account.

### 3.4 `PE-001-C022` elsewhere — classification **is** attached to Commercial Account

This is the single most consequential finding of this review, and it is **not** recorded in any of the three artifacts.

`[FACT]` **`EX-C022-04` — Frame Commercial Party Reclassification Intent** (§4.5), Trigger, verbatim:

> An existing Authoritative Customer Context's **or Authoritative Account Context's classification** no longer reflects the enterprise's understanding of the relationship.

`[FACT]` **`C022-O02` — Deliberate Commercial Party Evolution** (§1.6), Experience Meaning, verbatim:

> Every change to **a Customer's or Account's classification**, or to a hierarchy/ownership relationship, begins from explicit, attributable business intent…

`[FACT]` **§1.4 Scope**, verbatim:

> …establishing, understanding, **reclassifying**, retiring and reactivating the Authoritative Customer Context **and the Authoritative Account Context**…

`[FACT]` **Guiding Architectural Question** (Document Control / §1.3), verbatim:

> …who its Customer is and which Commercial Account that Customer's relationship is organized through — **including that representation's classification, hierarchy, and lineage** through establishment, reclassification, relationship change, merger, division, transfer, retirement, and reactivation…

`[FACT]` **`COM-001-060`**, verbatim, lists `reclassify` among the commercial actions in Sections 5–9 that are Business Activities.

### 3.5 `COM-001` Section 4 is inherited in full by Section 7

`[FACT]` `COM-001`, line 45, the preamble to Section 4, verbatim:

> *(Every construct in Sections 5–9 inherits this section in full, mirroring SD-002 §2's inheritance discipline. **Sections 5–9 state only what is distinctive to each construct.**)*

`[FACT]` `COM-001-001` (line 48), verbatim:

> **COM-001-001: Universal Identity**
> Every commercial object possesses a globally unique, permanent identity in `PREFIX-NNNNNN` form, per SD-002-004, alongside a canonical name and version.

`[FACT]` Independently verified: **neither** Section 5 (Subscription, `COM-001-010`–`-015`) **nor** Section 6 (Offering Definition, `COM-001-020`–`-026`) restates `PREFIX-NNNNNN`. Non-restatement is the documented, expected behaviour of every Section 5–9 construct, not a signal of non-applicability.

### 3.6 `ERB-C022-01` is the **Anchor** stage, not the authoritative establishment

`[FACT]` `PE-001-C022` §3.1, ERB portfolio row, verbatim — `ERB-C022-01` "Establish Commercial Party Context", Purpose: *"Resolve the Commercial Party Anchor Context and the existence fact for Authoritative Customer/Account Context."* Stage: **Anchor**. Realizing EX: `EX-C022-01`.

`[FACT]` `ERB-C022-01` Context Produced, verbatim: *"A resolved and confirmed Commercial Party Anchor Context handed to ERB-C022-02…"*

`[FACT]` `ERB-C022-01` Dependencies line, verbatim, complete: **"PE-001 Context Preservation Model."** — the artifacts' quotation of this line is accurate.

`[FACT]` `PE-001-C022 §1.16`, verbatim: *"For a proposed new commercial party, the Commercial Party Anchor Context anchors the establishment thread only: it SHALL NOT assert that a Customer or Commercial Account already exists, and SHALL NOT itself create an authoritative Customer Reference or Commercial Account Reference; **the first Authoritative Customer Context and/or Authoritative Account Context for that anchor is produced only through successful establishment Commit (ERB-C022-06)**."*

`[FACT]` `ERB-C022-06` (Commit) Entry Context, verbatim: *"An assessed Proposed Commercial Party Context and/or Proposed Commercial Relationship Context with its Commercial Dependency Assessment Context."* Dependencies, verbatim: *"C-002 (referenced only where a canonical authority requires an Access Evaluation Outcome for the commitment itself, distinct from Workspace-entry Access); C-020/C-023/C-024/C-025 (dependency references, consumed)."*

### 3.7 `PE-001-C022 §1.15` — an explicit implementation-readiness disclaimer

`[FACT]` Verbatim:

> No canonical Business Activity or EAC identifier for any C-022 Enterprise Experience exists in the supplied canonical baseline; every reference in this document is recorded as Pending Canonical Binding per IMP-001's authority over Business Activity realization. This does not block publication (Chapter 8.7) and **does not claim implementation readiness for any unresolved binding.**

### 3.8 `CAP-001` line 76

`[FACT]` Verbatim: `| C-022 | Customer & Account Management | Manage customer relationships. | **COM-001** | Active |` — at line 76 exactly. Every artifact's citation of this line is accurate.

---

## 4. Findings — `IRA-C022`

### 4.1 Is the 🟢 GREEN-leaning readiness conclusion justified?

`[FINDING — SUBSTANTIALLY YES, with a material qualification]`

The verdict is carefully worded — *"READY FOR TECHNICAL DESIGN PREPARATION"*, not ready for implementation — and `IRA-C022 §7`/`§9` explicitly disclaim IRA acceptance and implementation authorization. On that narrow claim the verdict is justified: `COM-001 §7` is LOCKED and fully specifies the Account construct; `PE-001-C022` v1.2 is Active and Gold-Standard-engineered; hosting, scope, and boundary were resolved by `ROD-C022` before the IRA ran; and the repository-wide zero-implementation finding was independently confirmed (no `c022_*` file exists in `Backend/` or `source/frontend/src`).

**Qualification:** `PE-001-C022 §1.15` (§3.7 above) states that the specification *"does not claim implementation readiness for any unresolved binding."* The IRA does not cite this clause. Its conclusion is not contradicted by it — the IRA stops at design readiness — but the governing specification's own explicit non-readiness disclaimer is the most directly on-point sentence in the entire document about C-022's readiness, and its absence from a readiness assessment is a gap in evidence rather than an error in conclusion.

### 4.2 Are dependencies correctly identified?

`[FINDING — YES. Every dependency claim independently verified against `PE-001-C022 §1.9`.]`

| Claim | Primary source | Verdict |
|---|---|---|
| C-004 Organization explicitly **not** a dependency | §1.9: *"Reference boundary only — C-022 explicitly does not consume C-004's Organization construct for Customer representation; noted here to preserve the boundary, **not as a dependency of substance**."* | ✅ Accurate, verbatim |
| C-001 Identity / C-006 Person optional, deferred | §1.9: *"consumed only where an individual Customer's identity is also an authenticated principal — Pending Canonical Binding where unavailable"* / *"consumed only where an individual Customer is also a known Person — Pending Canonical Binding where unavailable"* | ✅ Accurate |
| C-002/URA-001 required, satisfied by existing pattern | §1.9: *"Access Evaluation Outcome for any C-022 operation that canonically requires one…"*; `require_platform_admin` verified to exist at `dependencies.py:46` | ✅ Accurate |
| C-040 Tenant deferred, Pending Canonical Binding | §1.9: *"Tenant container reference, where Customer/Account scope depends on tenant context — Pending Canonical Binding where detailed semantics are unavailable in the supplied baseline."* | ✅ Accurate |
| C-020/C-023/C-024/C-025 downstream consumers, not dependencies | `COM-001-036`, verified | ✅ Accurate |

### 4.3 Is BA-01 implementable without an unsatisfied hard dependency? Does `ERB-C022-01`'s dependency list really contain nothing beyond "PE-001 Context Preservation Model"?

`[FINDING — the quotation is accurate, but it is the dependency list of the wrong ERB for what BA-01 actually does.]`

`ERB-C022-01`'s Dependencies line is verbatim *"PE-001 Context Preservation Model."* — confirmed (§3.6). `IRA-C022 §6` quotes it correctly and, to its credit, qualifies it as *"no capability dependency at all **for the Anchor stage**."*

However, `IRA-C022 §6` then draws the conclusion **"no hard, unsatisfied dependency exists"** for BA-01 as a whole, and `ROD-C022 §A` states more loosely that *"C-022's own establishment path (`ERB-C022-01`) lists its dependencies as 'PE-001 Context Preservation Model' only."*

Both rest on a mis-mapping. `ERB-C022-01` **does not establish an Authoritative Account Context.** It produces a strictly non-authoritative Commercial Party Anchor Context and hands it to `ERB-C022-02` (§3.6). `PE-001-C022 §1.16` is unambiguous that *"the first … Authoritative Account Context for that anchor is produced only through successful establishment Commit (**ERB-C022-06**)."* `TDS-C022 §6`/`§15` designs BA-01 to persist exactly that Authoritative Account Context. The governing ERB for BA-01's actual outcome is therefore `ERB-C022-06`, whose own Dependencies line names **C-002** and **C-020/C-023/C-024/C-025**.

**Does this overturn the conclusion? No — but it changes its basis.** Re-tested directly against `ERB-C022-06` for the establish case specifically:

- **C-002** — *"referenced only where a canonical authority requires an Access Evaluation Outcome for the commitment itself."* Satisfied by the existing, certified `require_platform_admin` dependency. Not unsatisfied.
- **C-020/C-023/C-024/C-025** — consumed as *"dependency references"* into the `Commercial Dependency Assessment Context`, which `ERB-C022-05` describes as material *"especially before a merge, split, transfer, or retirement."* For a **new** Account establishment there is no prior standing and therefore no downstream dependency to assess. Not unsatisfied.

`[FINDING]` **The conclusion "no hard, unsatisfied dependency exists for BA-01" survives independent re-derivation** — but it survives on `ERB-C022-06` evidence that neither the ROD nor the IRA examined, not on the `ERB-C022-01` evidence both cited. The artifacts reached a correct answer by an unsound route. This is a **reasoning defect, not a readiness defect**, and it is recorded here so that the conclusion rests on verified ground. It does not, by itself, block the gate.

It does, however, have a downstream consequence for the TDS's design — see `[C-5]` (§5.6).

### 4.4 Are the CBOR eligibility findings and the BAR treatment correctly characterized?

`[FINDING — YES, both. Independently re-derived.]`

**CBOR, against `CMD-001 §26.3a` as actually written** (§3.x, L11897–11907). The test's pass rule is verbatim: *"A candidate that satisfies Step 1 and at least one of Steps 2–3 is eligible."* Re-applying it:

- **Step 1 — Independent Identity.** Satisfied. A persisted Commercial Account with a system-assigned reference is not *"a value that exists only for the duration of one request/response cycle."*
- **Step 2 — Cross-Experience Reference.** Satisfied. `COM-001-036` names C-020, C-021 (conditional), C-023, C-024 and C-025 as consumers of the Commercial Account Reference by identity; `ERB-C022-07` is a distinct, separately-invoked Enterprise Experience consuming it.
- **Step 3 — Governed Lifecycle.** Satisfied. `COM-001-033`'s status attribute plus the `ERB-C022-03`/`-06` reclassify/retire/reactivate lifecycle.

`IRA-C022 §11`'s claim that all three steps are satisfied is correct and more conservative than the test requires. **Verified.**

`[FACT]` `CBOR-INDEX.md` independently checked: no Commercial Account entry exists. The `OFR-000001` / `ADR-037` precedent the IRA cites is real (row 37).

**BAR.** `COM-001-005`, verbatim: *"No commercial Business Activity shall be executed until registered in the BAR (IMP-001 §6.22)."* `COM-001-060`, verbatim, names `establish` among the actions so registered. `[FACT]` `CBOR-INDEX.md` L21 independently confirms *"no physical BAR artifact exists in this repository"* and that the WP-20 BAR question was closed by an explicit Repository Owner decision on 2026-09-08. `IRA-C022 §11`'s treatment — that BAR *"requires the same class of RO decision at implementation-authorization time … not silently assumed resolved by analogy"* — is **correct and correctly refuses the analogy**. Carried forward as `[C-7]`.

### 4.5 Are risks, assumptions, and deferred decisions complete enough to support a future RO authorization?

`[FINDING — ADEQUATE, with two omissions.]`

`§12.1`–`§12.3` are unusually disciplined: assumptions are stated rather than made silently, the classification discrepancy is surfaced rather than resolved, and deferrals carry recorded triggers. Two items are missing:

1. The `ERB-C022-01` vs `ERB-C022-06` mapping error (§4.3) is not disclosed, so a Repository Owner reading the IRA would believe BA-01's dependency position had been tested against the ERB that actually produces BA-01's outcome. It had not been.
2. `PE-001-C022 §1.15`'s explicit *"does not claim implementation readiness for any unresolved binding"* is not cited (§4.1).

Neither is disqualifying for a *design-readiness* verdict. Both should be visible to the Repository Owner at the authorization decision.

---

## 5. Findings — `TDS-C022`

### 5.1 Does the design implement only the `ROD-C022`-authorized BA-01 boundary, with no scope creep?

`[FINDING — YES. No scope creep detected.]`

Cross-checked `TDS-C022 §2`/`§6`/`§15` line-by-line against `ROD-C022 §H`'s in-scope and out-of-scope lists. Every §H exclusion is honoured: no Customer entity, no Relationship entity, no reclassify/retire/reactivate endpoint, no merge/split/transfer, no C-020/C-023/C-024/C-025 behaviour, no CRM/ERP construct, no Organization reference of any kind, no `organization_id`, no Identity/Person reference column, no invented lifecycle policy.

The one place the TDS goes beyond a literal reading — declaring the closed status set `{active, suspended, retired}` while implementing no transition (`§2`, `§9`) — is **explicitly justified, correctly bounded, and not scope creep**: no route, service method, or UI can change the value, and the pattern matches a certified precedent (verified: `c021_offering_definition.OFFERING_STATES` declares `draft`/`published`/`retired`, BA-01 writes only `draft`, model docstring L27–33). The design is, if anything, narrower than §H permits.

### 5.2 Does `c022_commercial_account` correctly model `COM-001-033` as actually written?

`[FINDING — YES on all three canonical attributes.]`

| `COM-001-033` attribute (verbatim, §3.1) | TDS design | Verdict |
|---|---|---|
| identity | `id` (UUID PK) + `account_reference` (String(30), UNIQUE) + `account_name` (String(255)) | ✅ |
| Account-to-Account hierarchy position | `parent_account_id` (self-referential FK, NULLABLE, declared-not-exercised) | ✅ |
| status | `status` String(20), CHECK closed set, default `'active'` | ✅ |
| *(no classification attribute)* | `classification` deliberately absent, with the conflict documented | ✅ — see §6 |
| *"Never equivalent to a … Organization…"* | No `organization_id`; no Organization reference of any kind | ✅ |

`[FINDING]` The schema is a faithful realization of `COM-001-033`'s three attributes. Two design additions — `created_by_actor_id`, `created_at`/`updated_at` — are audit/platform conventions, verified present in `c021_offering_definition` (L180–199), and carry no business semantics.

### 5.3 Is the Account Reference generation/uniqueness design technically sound?

`[FINDING — the *mechanism* is sound; the *format* determination is defective. See `[C-3]`.]`

**Sound:** the `id` + `account_reference` split mirrors the verified `c021_offering_definition` shape (L106–122). The plain whole-table `UNIQUE` constraint is correct at BA-01 scope, since no in-place versioning exists. The allocate-and-retry concurrency design was independently verified against the certified implementation — `services/offering_definition_service.py` L96–131 implements exactly `_next_offering_reference()` → insert → `except IntegrityError` → `await session.rollback()` → retry → bounded failure with a retry-advisory error. `TDS-C022 §18`'s citation of this pattern is accurate.

**Defective:** `TDS-C022 §7` declines to require the `PREFIX-NNNNNN` format, reasoning verbatim:

> `COM-001-030`–`036` (the Customer/Account section) does **not** repeat `COM-001-001`'s Universal Identity clause the way `COM-001-010`/`011` did for Subscription or the way Offering Definition's own section does — so this TDS does **not** assume `ACCOUNT-NNNNNN` is mandated.

Both halves of this reasoning are contradicted by the primary sources:

1. `[FACT]` **The premise is factually false.** Independently verified (§3.5): **neither** `COM-001-010`/`-011` **nor** Section 6 repeats `PREFIX-NNNNNN`. No Section 5–9 construct does. The contrast the TDS draws does not exist.
2. `[FACT]` **Non-repetition is the documented norm, not a signal of non-applicability.** `COM-001` Section 4's own preamble (line 45) states verbatim: *"Every construct in Sections 5–9 inherits this section in full … Sections 5–9 state only what is distinctive to each construct."* Silence in Section 7 is therefore evidence of inheritance, not of exemption.
3. `[FACT]` **The certified precedent reads it the opposite way.** `TDS-C021 §9.3` states verbatim that *"realizing **`COM-001-001`'s mandated format** is new implementation work"*, and `TDS-C021 §9.1` describes `offering_reference` as *"The `COM-001-001` Universal Identity (`PREFIX-NNNNNN`)"*. The shipped model confirms it: `c021_offering_definition.py` L35–41 declares `OFFERING_REFERENCE_PREFIX = "OFFERING"` under the comment *"`COM-001-001` Universal Identity prefix"*, and L71–77 states *"`offering_reference` is the `COM-001-001` Universal Identity (`PREFIX-NNNNNN`)"*.
4. `[FACT]` **`[RO DECISION] O1` did not "fix" the format, as `TDS-C022 §7` asserts.** `TDS-C021 §9.3` records O1's actual content verbatim: *"A PostgreSQL `SEQUENCE` is NOT an architectural requirement. The concrete mechanism … is intentionally left to implementation design."* O1 governed the **allocation mechanism**, not the format. The format came from `COM-001-001`.

`[FINDING]` `TDS-C022 §7` declines to apply a LOCKED constitutional requirement on the strength of a reading that the LOCKED document's own inheritance preamble, and the certified precedent it cites, both contradict. This is the most consequential technical defect in the TDS. **Correcting it narrows scope rather than widening it** — it converts an open implementation-time choice into a constitutionally fixed constraint — so it requires no new Repository Owner decision, only a TDS correction. Recorded as `[C-3]`.

### 5.4 Are platform-global scope and `AuthService` hosting faithfully carried from the ROD?

`[FINDING — YES, faithfully and without reinterpretation.]`

`TDS-C022 §5` carries `ROD-C022` D3 (`AuthService`) with no re-analysis, correctly treating it as already decided. `§6.1`/`§11` carry D2 (platform-global) as the structural absence of `organization_id`, explicitly labelled *"a structural expression of D2, not an omission."* Independently verified: `roles` and `c021_offering_definition` both carry no `organization_id` (confirmed by direct read of both models). The `§21.4` not-applicable determination plus the three-part substitute assurance (non-`PLATFORM_ADMIN` denied; `PLATFORM_ADMIN` succeeds; automated no-`organization_id` assertion via live introspection **and** ORM metadata) matches the certified C-021 treatment. Faithful.

### 5.5 Is the authorization/tenant-middleware design correctly derived from the actual certified precedent?

`[FINDING — YES. Verified against source, not merely asserted.]`

- `[FACT]` `require_platform_admin` exists at `Backend/Services/AuthService/dependencies.py:46`.
- `[FACT]` `routers/offering.py` gates all three routes with `Depends(require_platform_admin)` (L61, L86, L113) — the pattern the TDS cites is real and certified.
- `[FACT]` `middleware/tenant.py` L238–239 implements exactly the prefix-pair exemption shape: `path == "/roles" or path.startswith("/roles/") or path == "/offerings" or path.startswith("/offerings/")`. `TDS-C022 §12`'s design — *"gains one new prefix pair (e.g. `/commercial-accounts`, `/commercial-accounts/`) on the same `/roles`/`/offerings` basis, with a rationale comment citing `ROD-C022` D2"* — is an exact, additive match to the existing certified mechanism, including the in-file rationale-comment convention visible at L29–58.

The derivation is genuine, not asserted. The design correctly selects `require_platform_admin` over `require_matching_tenant_or_platform_admin`, consistent with D2.

### 5.6 Are persistence, API, validation, audit/event, concurrency, and negative-control requirements sufficient to build from without inventing semantics?

`[FINDING — SUFFICIENT for the endpoint designed, with one conformance gap.]`

Sufficient: the schema table (§6.1) is fully specified to type/nullability/constraint level; validation rules (§8, §16) name every field and its rejection behaviour; audit (§17) names the exact `record_audit` action string and metadata; concurrency (§18) names the retry discipline; negative controls (§19) and the test set (§20) are concrete and checkable; acceptance criteria (§23) are stated as observable outcomes. An implementing session could build the designed endpoint without inventing semantics.

**Conformance gap.** `TDS-C022 §15` designs a single `POST /commercial-accounts` taking `{account_name}` and returning a persisted Authoritative Account Context. That collapses the entire canonical commercial lifecycle into one call. Against the primary sources:

- `[FACT]` `COM-001-002` (inherited in full by Section 7, per §3.5), verbatim: *"Every commercial construct below distinguishes three roles, never conflated: an **Anchor Context** …, an **Authoritative Context** …, and a **Resulting Context** …"*
- `[FACT]` `COM-001-003`, verbatim: *"Every commercial action states its business reason and target outcome (an Intent Context) before any candidate change (a Proposed Context) is shaped."*
- `[FACT]` `ERB-C022-06` Entry Context, verbatim: *"An assessed Proposed Commercial Party Context and/or Proposed Commercial Relationship Context with its Commercial Dependency Assessment Context."*
- `[FACT]` `PE-001-C022 §1.14`, verbatim, names the mandatory stage progression: *"Anchor → Understand Standing → Frame Lifecycle Intent / Frame Structural Intent → Shape & Assess → Commit → Distribute Reference."*

The designed endpoint realizes none of Anchor, Intent, Proposal, or Assessment as distinct constructs. `ROD-C022 §H` authorizes "Establish Commercial Account" as a minimum slice and is silent on lifecycle-pattern realization, so this is not a §H violation — but `COM-001-002`/`-003` are LOCKED, are inherited in full by Section 7, and are nowhere addressed in `TDS-C022`. A design that does not mention the constitutional lifecycle pattern its own construct inherits has not demonstrated conformance to it. This connects directly to §4.3: because the artifacts mapped BA-01 to `ERB-C022-01` (the Anchor stage) rather than `ERB-C022-06` (the Commit stage), the Intent/Proposal/Assessment preconditions that `ERB-C022-06` actually carries never entered the design's field of view.

`[FINDING]` This requires **explicit disclosure and an RO-level scope determination** — either that a single-step establish is the accepted minimum realization with the Anchor/Intent/Proposal stages disclosed as deferred, or that the minimum slice must realize them. This reviewer does **not** resolve it. Recorded as `[C-5]`.

### 5.7 Are hierarchy semantics correctly kept declared-but-unexercised?

`[FINDING — YES. Correct, well-reasoned, and consistent with the certified precedent — though resting partly on a misattributed quotation.]`

`TDS-C022 §10`/`§6.1` declare `parent_account_id` as a nullable self-referential FK, never written non-NULL by BA-01, so a future structural increment needs no `ALTER`. Independently verified against the precedent: `c021_offering_definition.supersedes_id` is a nullable self-referential `ForeignKey("c021_offering_definition.id")` (L174–178) documented as *"Declared for the future increment; BA-01 always NULL."* Exact match. This is fully consistent with `ROD-C022 §H` excluding all structural transitions.

**Caveat.** `§10`'s supporting argument — *"`COM-001-033` names hierarchy as part of the canonical Account fact ('where applicable') — the parenthetical itself signals hierarchy is conditional"* — rests on a parenthetical that **is not in `COM-001-033`** (§3.1). The phrase *"(parent Account reference, where applicable)"* comes from `PE-001-C022 §1.16`'s Account row (§3.3). The conclusion is nonetheless correct, because `PE-001-C022` is an Active governing source and does contain it. Citation defect only; see `[C-4]`.

### 5.8 Has any business semantic been copied from C-021 (or elsewhere) without independent constitutional justification?

`[FINDING — NO. This discipline was applied correctly and is the TDS's strongest quality.]`

Every C-021 citation was checked against `c021_offering_definition.py` to classify it as *mechanism* or *semantics*:

| TDS-C022 citation | Classification | Verified |
|---|---|---|
| UUID PK + `default=uuid4` | Mechanism (platform convention) | ✅ L106–109 |
| `reference` String(30) UNIQUE alongside UUID PK | Mechanism (identity shape) | ✅ L112–117 |
| `String(255)` name, no uniqueness invariant | Mechanism | ✅ L124–128 |
| Declare-full-closed-set / write-one-value status | Mechanism (schema pattern) | ✅ L27–33, L159–164 |
| Nullable self-referential FK, declared-not-exercised | Mechanism (forward-compatibility) | ✅ L174–178 |
| `created_by_actor_id` UUID, **not** a FK | Mechanism (audit convention) | ✅ L180–187 |
| `record_audit` / `publish_event` | Mechanism | ✅ |
| `BaseRepository[...]` | Mechanism | ✅ |
| Allocate-and-retry on `IntegrityError` | Mechanism | ✅ `offering_definition_service.py` L96–131 |

`[FINDING]` **No C-021 business semantic was imported.** `offering_kind` (the `COM-001-021` Product↔Service axis), `category_ref` (`COM-001-024`), `list_price_reference` (`COM-001-020` / D6), and `version` (`COM-001-025`) — all present in the C-021 model — are each correctly absent from the C-022 design. Every C-022 attribute traces to `COM-001-033` or to a platform convention. Each status/hierarchy inference is separately labelled `[INFERENCE]` rather than presented as fact. This is exactly the discipline `CLAUDE.md §19.5` requires.

One related observation: the status-set inference in `§6.1` is correctly flagged. Independently verified — `PE-001-C022 §1.16`'s `(active, suspended, retired)` enumeration is indeed attached only to the **Customer** row; the Account row says only *"its current status"* (§3.3). The TDS's characterization is accurate and its `[INFERENCE]` label is warranted.

---

## 6. Critical Scope Issue C.1 — Classification

### 6.1 The question, re-derived from primary sources only

**Does `COM-001-033` define a "classification" attribute for Commercial Account, or is classification exclusively a `COM-001-032` Customer attribute?**

`[FACT]` **`COM-001-033` defines no classification attribute.** Its complete attribute list is *identity, Account-to-Account hierarchy position, and status* (§3.1, read directly from line 126). This reviewer confirms it independently: there is no classification concept anywhere in the clause.

`[FACT]` **`COM-001-032` does define classification, for Customer** (§3.2, line 123).

`[FACT]` **`PE-001-C022 §1.16`'s Account context row likewise omits classification** (§3.3).

**On the narrow textual question, `IRA-C022 §9` and `TDS-C022 §4` are correct.**

### 6.2 What the artifacts missed

`[FINDING]` `TDS-C022 §4`'s determination table records:

| `PE-001-C022 §1.16` (Active, Enterprise Experience Spec) | **No.** |

and concludes *"again, no classification attribute for Account, **in either governing document**."*

That conclusion is **not supported by `PE-001-C022` read as a whole.** Four passages in the same Active specification attach classification to Commercial Account explicitly (§3.4, each quoted verbatim there):

1. **`EX-C022-04` Trigger** — *"An existing Authoritative Customer Context's **or Authoritative Account Context's classification** no longer reflects the enterprise's understanding of the relationship."* This is the most explicit statement in any governing document on the question, and it says the Authoritative Account Context **has** a classification.
2. **`C022-O02`** — *"Every change to **a Customer's or Account's classification** …"*
3. **`§1.4 Scope`** — *"establishing, understanding, **reclassifying** … the Authoritative Customer Context **and the Authoritative Account Context**"*
4. **Guiding Architectural Question** — *"including that representation's **classification**, hierarchy, and lineage through establishment, **reclassification**, …"*

`[FINDING — methodological inconsistency]` The TDS **already accepts EX-portfolio evidence as probative** — `§6.1` uses `EX-C022-05`/`EX-C022-06` to extend the Customer status enumeration to Account, reasoning that those EXs *"confirm retire/reactivate applies to Account as well as Customer."* But `EX-C022-04` is **strictly stronger evidence** for classification than `EX-C022-05`/`-06` are for status: `EX-C022-04` names the attribute on the Account context directly (*"Authoritative Account Context's classification"*), whereas `EX-C022-05`/`-06` name only the construct generically (*"a Customer's or Commercial Account's standing"*). The TDS applied EX-portfolio reasoning where it expanded the schema and withheld it where it would have expanded the schema further. That asymmetry is not defended anywhere in the document.

### 6.3 Was excluding the column the correct response?

`[FINDING — YES. The decision is correct; the *characterization* of why is not.]`

Excluding `classification` was right, for a reason stronger than the one the TDS gave: inventing a column with no LOCKED constitutional basis would violate `CLAUDE.md §18` (no new database columns unless explicitly documented) and `§19.4`'s STOP-and-report discipline. Flagging rather than inventing is precisely correct, and this reviewer endorses it.

What the TDS should additionally have done: identified this as a **`CLAUDE.md §16` canonical-authority conflict** and invoked §16's procedure. It instead framed the matter as ROD imprecision against COM-001 silence — a framing that makes it look like a drafting slip correctable by clarification. On the full evidence it is not.

### 6.4 Determination — (a) or (b)?

> `[FINDING]` **(b) — this genuinely requires a fresh, explicit Repository Owner decision before implementation can proceed.** It is **not** merely imprecise ROD wording that the LOCKED `COM-001` model already clarifies.

Reasoning:

1. **It is a conflict between two canonical documents, not a ROD drafting error.** `COM-001-033` (LOCKED, Constitutional, Layer 1) omits Account classification. `PE-001-C022` (Active, Enterprise Experience Specification) asserts it in `EX-C022-04`, `C022-O02`, `§1.4`, and the Guiding Architectural Question. `ROD-C022 §H` is not the only source attaching classification to Account, as `TDS-C022 §4`'s table claims — `PE-001-C022` does too, in four places. That table is materially incomplete and should not be relied on as the evidentiary basis for a decision.

2. **`CLAUDE.md §16` governs this exact situation**, verbatim: *"If two canonical documents appear to conflict: 1. Stop implementation. 2. Identify the conflicting definitions. 3. Identify the declared canonical owner. 4. Review applicable ADRs. 5. Report the conflict before changing code. **Never resolve canonical architecture conflicts by assumption.**"* Treating `COM-001-033`'s silence as settling the matter would resolve the conflict by assumption — the one thing §16 prohibits.

3. **`COM-001`'s own Authoring Note makes the omission ambiguous in origin.** `[FACT]` `COM-001` line 15, verbatim: *"This document is an extraction and constitutional formalization exercise, not new business invention … Every business concept defined below … already exists, fully engineered, in the four Active PE-001-Cxxx Experience specifications (… PE-001-C022 v1.2 …)."* COM-001 declares itself an **extraction** from `PE-001-C022`. Its omission of an attribute that the source specification states four times is therefore as plausibly an **extraction gap** as a deliberate exclusion. Only the Repository Owner (or EARB) can determine which — a reviewer, a TDS, or an implementing session cannot.

4. **`ROD-C022 §H` remains a recorded Repository Owner decision.** Silently narrowing it on the strength of a LOCKED clause whose own source document contradicts it would be an implementation session overriding a recorded RO decision — the inverse of the discipline `§17`/`§18` require.

5. **The consequence is asymmetric and non-trivial.** If Account classification is genuine, shipping without the column means the first C-022 increment establishes an Authoritative Account Context that cannot carry one of its own canonical attributes, and a later `ALTER` would be required — precisely the outcome the TDS's own declared-but-unexercised discipline (`parent_account_id`, `status`) exists to avoid. The TDS applied that forward-compatibility discipline to hierarchy and status but not to classification, without explaining the difference.

> ### `[STOP]` **No Charter, WP registration, schema, migration, or implementation touching the Commercial Account attribute set may proceed until the Repository Owner records an explicit decision on whether the Authoritative Commercial Account Context carries a classification attribute** — resolving the `COM-001-033` ↔ `PE-001-C022` (`EX-C022-04` / `C022-O02` / `§1.4` / GAQ) conflict under `CLAUDE.md §16`. If the decision is that classification **is** a genuine Account attribute, an ADR amending or annotating LOCKED `COM-001-033` is required, since `COM-001` is LOCKED and may not be changed by implementation (`§18`, `§19.6`).

This reviewer records the conflict and its full evidence. This reviewer does **not** resolve it, and expresses no view on which reading is correct.

---

## 7. Critical Scope Issue C.2 — Read/List

### 7.1 Is the TDS's reading of `ROD-C022 §H` correct?

`[FINDING — YES. The TDS's reading is literally and correctly derived from §H's actual text.]`

`[FACT]` `ROD-C022 §H`, read directly. Heading, verbatim: *"**Authorized, and only:** **"Establish Commercial Account."**"* In-scope list, verbatim and complete:

> - Establish one Authoritative Commercial Account.
> - A system-assigned, stable Account Reference.
> - Minimum canonical Account identity, classification, and status (`COM-001-033`).
> - Platform-global scope (§E), `AuthService` hosting (§F), the existing `require_platform_admin`-shaped authorization pattern.

`[FACT]` Neither "list", "read", nor "retrieve" appears anywhere in §H — not in the in-scope list, and not in the out-of-scope list either. §H closes, verbatim: *"**This scope SHALL NOT be expanded except by an explicit, separately-recorded Repository Owner decision.**"*

`[FACT]` The contrast the TDS draws with C-021 is accurate. `ROD-C021` D4, verbatim (line 22): *"…identity, name, Product/Service classification, opaque category reference, optional opaque `list_price_reference`, `draft` state, **list, read**."* And `ROD-C021 §H`'s in-scope line names *"…`draft` state; **list**; **read**; produce the Authoritative Offering Definition Context…"*. `[FACT]` The shipped implementation matches: `routers/offering.py` carries one POST (L27) and two GETs (L67, L92).

`[FINDING]` `TDS-C022 §14`/`§15`/`§21` are therefore **correct** to refuse to include read/list by analogy. Given §H's explicit no-expansion clause, assuming read/list would have been an unauthorized scope expansion. **The TDS made the right call and flagged rather than assumed.** This reviewer endorses the refusal.

### 7.2 Should read/list nevertheless have been included?

`[FINDING — not by the TDS's own authority, no. But the omission has consequences the artifacts do not record, and those consequences make an RO decision necessary rather than optional.]`

Four independently verified consequences:

1. **`COM-001-036` / `C022-O05` reference distribution becomes unrealizable after the establish call.** `[FACT]` `COM-001-036`, verbatim: *"The stable Customer Reference, Commercial Account Reference, and/or Customer–Account Relationship Reference, **plus Account hierarchy and status**, are made available for consumption by Subscription (C-020), Product & Service Catalog (C-021, conditional segment reference), Licensing & Entitlement (C-023), Billing (C-024), and Contract (C-025)."* `[FACT]` `C022-O05`, verbatim: *"Downstream capabilities … **always receive** a stable Customer/Account Reference."* A write-only endpoint makes the reference available exactly once, in the 201 response body. Nothing can retrieve it afterwards.

2. **The stated purpose of the entire C-022 investigation is not reached.** Per `ROD-C022 §A`/`IRA-C022 §4`, C-022 is being built because C-020 *"cannot proceed without a genuine Customer/Account reference."* A future C-020 cannot consume a reference it has no endpoint to resolve.

3. **`CLAUDE.md §20` cannot be satisfied.** `[FACT]` `§20.3` requires, for each Business Activity a Work Package charters, *"Frontend, Navigation, Enterprise Experience"* and *"The end-to-end user journey"*; `§20.4` requires demonstrability through *"a real persona, using the real frontend"*; `§20.6` requires *"a loading state … an empty state"* and IMP-001 §10.3's four content-disclosure states (Summary, Details, Evidence, Audit History). Every one of these presupposes read. A write-only capability cannot render a Summary, a Details view, an Audit History, or an empty state. Unless the future WP is explicitly chartered **backend-only** — a decision `§20.3`/`§20.4` require to be *"reported and justified per §19.4's own STOP-and-report discipline, not silently assumed"* — BA-01 as designed cannot close a `§20`-governed Work Package.

4. **A minor CBOR-evidence note.** `[FACT]` `IRA-C021 §8` grounded its Step 1 finding partly on *"D4 explicitly authorizes `list`/`read` as distinct later actions against a previously-established record."* `IRA-C022 §11` grounds Step 2 on `COM-001-036` instead, which is independently sufficient — so CBOR eligibility does **not** depend on read/list. Noted only to confirm the C-022 finding stands on its own.

`[FINDING]` The TDS was right not to add read/list. But the effect is that BA-01 as currently scoped produces a Business Object nothing can subsequently retrieve, cannot satisfy `COM-001-036`, cannot advance the C-020 dependency that motivated C-022, and cannot close a `§20`-governed Work Package without an explicit backend-only charter decision. None of this is recorded in `IRA-C022` or `TDS-C022`, both of which treat read/list as a neutral open question.

### 7.3 Determination

> `[FINDING]` **A fresh, explicit Repository Owner decision is required** — either (i) extending `ROD-C022 §H` to authorize read/list for BA-01 (per §H's own expansion clause), or (ii) confirming establish-only **together with** an explicit `§20.3` backend-only charter determination and a recorded acknowledgement that `COM-001-036` distribution is deferred to a later increment.
>
> `[STOP]` **No Charter or WP registration for C-022 BA-01 may proceed until this decision is recorded.** The choice materially determines whether the resulting Work Package can satisfy `CLAUDE.md §20.3`/`§20.4`/`§20.7`, and is therefore a charter-shaping decision, not an implementation detail.

This reviewer does not resolve it and expresses no preference between (i) and (ii).

---

## 8. Dependency / Readiness and Security / Design Assessments

### 8.1 Dependency and readiness

| Dimension | Assessment |
|---|---|
| Governance substrate | **Complete.** `COM-001 §7` LOCKED; `PE-001-C022` v1.2 Active, 1 CRB / 8 ERB / 17 EX, independently confirmed by full extraction. |
| Hard unsatisfied dependencies | **None** — conclusion confirmed, but re-derived by this reviewer against `ERB-C022-06` rather than the `ERB-C022-01` the artifacts cited (§4.3). |
| Existing implementation | **Zero.** No `c022_*` artifact anywhere in `Backend/` or `source/frontend/src`. Independently confirmed. |
| Reusable mechanisms | **Fully available and verified in source** — `require_platform_admin` (`dependencies.py:46`), tenant-exemption prefix pairs (`middleware/tenant.py:238–239`), `BaseRepository`, `record_audit`/`publish_event`, allocate-and-retry (`offering_definition_service.py:96–131`). No new mechanism required. |
| Blocking pre-implementation registrations | **Two, both open and both hard constitutional gates** — CBOR (`COM-001-005`/`-061`; no Commercial Account row in `CBOR-INDEX.md`) and BAR (`COM-001-005`/`-060`; no BAR mechanism exists repository-wide). Correctly identified by both IRA and TDS. |
| Readiness for **technical design** | **Confirmed**, subject to §9's conditions. |
| Readiness for **implementation** | **NOT reached.** Two `[STOP]` decisions plus two registration gates remain open. `PE-001-C022 §1.15` independently disclaims implementation readiness for any unresolved binding, and every C-022 BA/EAC binding is unresolved. |

### 8.2 Security and design

| Dimension | Assessment |
|---|---|
| Authorization | **Sound.** `require_platform_admin` on every route, correctly chosen over the tenant-scoped gate given D2. Derivation verified against certified source, not asserted. |
| Tenant isolation | **Structurally N/A and correctly handled.** Platform-global by `ROD-C022` D2 recorded on C-022's own `§1.9`/`COM-001-033` basis, not inferred from C-021. `§21.4` correctly assessed as inapplicable, with a three-part substitute assurance including an automated no-`organization_id` assertion via both live introspection and ORM metadata. |
| Input trust boundary | **Sound.** `account_reference`/`id`/`status`/`parent_account_id` are never caller-supplied, enforced structurally by absence from the request schema rather than by runtime override-and-reject — matching the certified C-021 pattern. |
| Negative controls | **Adequate** for the designed endpoint: 403 non-`PLATFORM_ADMIN`, 403 no-role-claim, 400 missing/malformed `Authorization`, 422 blank name, schema-absence proofs, plus a purpose-built end-to-end probe per `§19.7b`. |
| Cross-tenant identifier acceptance (`§21.4(c)`) | **N/A as designed** — the establish request accepts no foreign-object identifier. Would require re-assessment if `parent_account_id` ever becomes caller-supplied. |
| Concurrency | **Sound.** `UNIQUE` + allocate-and-retry, verified against certified implementation. |
| Audit | **Sound.** Reuses `record_audit`; `publish_event` correctly disclosed as a structured-log stand-in rather than a real event bus. |
| Data integrity | **One open risk** — the classification question (§6). If resolved affirmatively later, a schema `ALTER` on a shipped Business Object would be required. |
| Identity format | **Defective** — `PREFIX-NNNNNN` not applied; see `[C-3]`. |

---

## 9. Mandatory Conditions

### Blocking — require a fresh Repository Owner decision, with `[STOP]`

**`[C-1]` Classification `[STOP]`** — Record an explicit Repository Owner decision resolving whether the Authoritative Commercial Account Context carries a classification attribute, treating this as a `CLAUDE.md §16` canonical-authority conflict between LOCKED `COM-001-033` (silent) and Active `PE-001-C022` (`EX-C022-04`, `C022-O02`, `§1.4`, GAQ — all affirmative). The decision SHALL be taken on the **complete** evidence in §3.4/§6.2 of this review, not on `TDS-C022 §4`'s determination table, which records `PE-001-C022` as answering "No" and is materially incomplete. If the decision is affirmative, an ADR is required, since `COM-001` is LOCKED. **No Charter, WP registration, schema, migration, or implementation touching the Account attribute set may proceed until this is recorded.**

**`[C-2]` Read/List `[STOP]`** — Record an explicit Repository Owner decision either (i) extending `ROD-C022 §H` to authorize read/list for BA-01, or (ii) confirming establish-only together with an explicit `CLAUDE.md §20.3` backend-only charter determination and a recorded acknowledgement that `COM-001-036` reference distribution is deferred. The decision SHALL be informed by §7.2's four consequences, none of which is recorded in `IRA-C022` or `TDS-C022`. **No Charter or WP registration may proceed until this is recorded.**

### Mandatory corrections to `TDS-C022` before it is treated as implementable

**`[C-3]` `COM-001-001` Universal Identity.** `TDS-C022 §7` SHALL be corrected to apply `COM-001-001`'s `PREFIX-NNNNNN` format to `account_reference`. Its present reasoning is contradicted by (a) `COM-001` Section 4's inheritance preamble (line 45), (b) the fact that no Section 5–9 construct restates the clause, and (c) `TDS-C021 §9.3`'s explicit *"`COM-001-001`'s mandated format"* plus `c021_offering_definition.py` L35–41/L71–77. `[RO DECISION] O1` governed the allocation **mechanism**, not the format. This correction narrows scope and requires no new RO decision. The concrete prefix token should align with the `[C-6]` CBOR Business Object Identifier, per the `TDS-C021 §9.3` precedent.

**`[C-4]` Citation accuracy.** Three `[FACT]`-tagged quotations attribute `PE-001-C022 §1.16` wording to LOCKED `COM-001` clauses. Each SHALL be re-attributed to its true source:
- *"(parent Account reference, where applicable)"* — `PE-001-C022 §1.16`, **not** `COM-001-033` (`TDS-C022 §3`/`§10`, `IRA-C022 §8`). Load-bearing: `TDS-C022 §10`'s hierarchy argument rests on it.
- *"ERP company code, CRM account record"* — `PE-001-C022 §1.16` Rule column, **not** `COM-001-033` (`ROD-C022 §A`, `IRA-C022 §3`).
- *"(e.g., segment, partner/reseller/distributor designation)"* and *"current status"* — `PE-001-C022 §1.16`, **not** `COM-001-032` (`TDS-C022 §4`).

In every case the substantive conclusion survives, because the true source is an Active governing document. The defect is attributional. It matters because these documents' authority rests on verbatim fidelity to LOCKED text, and because `[C-1]` turns on exactly this LOCKED-versus-Active distinction. Correcting `ROD-C022`/`IRA-C022` is a Repository Owner matter; this reviewer modified nothing.

**`[C-5]` Commercial lifecycle-pattern conformance `[disclosure + RO scope determination]`.** `TDS-C022` SHALL disclose that its single-call `POST /commercial-accounts` realizes none of the Anchor, Intent, Proposed, or Assessment contexts that `COM-001-002`/`COM-001-003` (inherited in full by Section 7 per `COM-001` line 45) and `ERB-C022-06`'s own Entry Context require, and SHALL record whether this is an accepted minimum-slice deferral or a gap requiring design change. Related: the `ERB-C022-01` vs `ERB-C022-06` mapping error (§4.3) SHALL be disclosed to the Repository Owner, since both `ROD-C022 §A` and `IRA-C022 §6` rest their no-unsatisfied-dependency finding on the Anchor-stage ERB rather than the Commit-stage ERB that actually produces BA-01's outcome. This reviewer independently re-derived the finding against `ERB-C022-06` and it **holds** — but the Repository Owner should be authorizing on verified grounds.

### Carried forward — hard constitutional gates, correctly identified by the artifacts

**`[C-6]` CBOR registration.** `COM-001-005`, verbatim: *"no persistent commercial Business Object shall be implemented until registered in the CBOR."* `COM-001-061` names Commercial Account explicitly. Eligibility independently re-verified against `CMD-001 §26.3a` (§4.4). No Commercial Account row exists in `CBOR-INDEX.md`. A registration ADR mirroring `ADR-037` is required **before** implementation.

**`[C-7]` BAR.** `COM-001-005`, verbatim: *"No commercial Business Activity shall be executed until registered in the BAR."* `COM-001-060` names `establish`. No BAR mechanism exists repository-wide (independently confirmed at `CBOR-INDEX.md` L21). Requires the same class of explicit Repository Owner decision every prior BA-01 required. `IRA-C022 §11`'s refusal to assume this resolved by analogy is endorsed.

---

## 10. Summary of the Gate Decision

> ### **PASS WITH CONDITIONS**

`ROD-C022`, `IRA-C022`, and `TDS-C022` are competent, disciplined, and — on the central question this review was asked to test hardest — **correct**. The refusal to invent a Commercial Account `classification` column is the right call under `CLAUDE.md §18`, and the refusal to add read/list by analogy to C-021 is the right call under `ROD-C022 §H`'s own no-expansion clause. Neither refusal was a guess; both were flagged for decision. No business semantic was copied from C-021. Every reusable-mechanism citation checked against live source proved accurate.

The gate does not pass cleanly for three reasons: the classification question is a genuine `§16` canonical conflict that the artifacts under-characterized by missing four affirmative `PE-001-C022` passages; the read/list question carries `COM-001-036` and `§20` consequences the artifacts do not record; and `TDS-C022 §7` declines a LOCKED constitutional identity requirement on reasoning the LOCKED document's own inheritance preamble and the certified WP-20 precedent both contradict.

`[C-1]` and `[C-2]` are **`[STOP]` items requiring fresh Repository Owner decisions before any Charter, WP registration, or implementation work begins.** `[C-3]`–`[C-5]` are mandatory corrections to `TDS-C022`. `[C-6]`–`[C-7]` remain open hard constitutional gates.

**This review does not resolve any condition, does not grant IRA acceptance, does not authorize `TDS-C022` finalization, and does not authorize a Charter, WP registration, or implementation of any kind.**

---

## 11. Reviewer Independence and Change Control

**Independence.** This reviewer had no involvement in authoring `ROD-C022`, `IRA-C022`, or `TDS-C022`, and entered this task with no prior context on them. No quotation appearing in any artifact under review was accepted at face value; every load-bearing citation was re-read from its primary source, including an independent extraction of the `.docx` Enterprise Experience Specification performed by this reviewer (§2). Findings in §3.4, §3.5, §3.6, §5.3, §5.6, and §7.2 were derived from primary sources and are **not** restatements of anything the artifacts claim.

**Files created by this pass:** this document — `architecture/06-Reviews/IRA-TDS-C022_Independent_Review.md`. Verified not to exist before this pass.

**Files read, not modified:** `CLAUDE.md`; `COM-001_Commercial_and_Subscription_Architecture.md`; `CAP-001_Enterprise_Capability_Registry.md`; `CMD-001_Canonical_Data_Model.md` (§26.3a); `PE-001-C022- Customer_and_Account_Management.docx`; `ROD-C022`; `IRA-C022`; `TDS-C022`; `ROD-C021`; `IRA-C021`; `TDS-C021`; `CBOR-INDEX.md`; `Backend/Services/AuthService/` — `models/c021_offering_definition.py`, `models/role.py`, `models/c023_entitlement_context.py`, `middleware/tenant.py`, `dependencies.py`, `routers/offering.py`, `services/offering_definition_service.py`.

**Not modified:** `ROD-C022`, `IRA-C022`, `TDS-C022`; any LOCKED constitutional document; any `PE-001` document; `CBOR-INDEX.md`; `WPR-001`; `WP-REG-001`; `MASTER-CAPABILITY-FEATURE-BA-WP-DELIVERY-MAP.md`; `TECH-DEBT.md`; any ADR; any C-020/C-021/C-023/C-040 governance artifact; any `Backend/` or `source/frontend/` file, migration, test, or API. No Charter was created. No WP number was registered. No CBOR or BAR registration was performed. Temporary `.docx` extraction artifacts were written to a session scratch directory outside the repository and form no part of it. **Nothing was staged, committed, or pushed.**

*End of IRA-TDS-C022 Independent Review. Gate decision: PASS WITH CONDITIONS. `[C-1]` (classification) and `[C-2]` (read/list) are `[STOP]` items — each requires a fresh, explicit Repository Owner decision before any Charter, Work Package registration, or implementation work proceeds on the affected item.*
