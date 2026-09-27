# ADR-039 — Commercial Account Canonical Business Object Registration (Preparation)

**Status:** PROPOSED — REGISTRATION PREPARATION ONLY. **This ADR does not perform CBOR registration.** `CBOR-INDEX.md` is not amended by this document. No Business Object Identifier is assigned. A separate, explicit Repository Owner authorization is required before the actual registration act (identifier assignment + `CBOR-INDEX.md §3` row addition) is performed.

**Classification:** Architecture Governance / Canonical Business Object Eligibility & Registration Preparation.

**Decided by:** Not yet decided — prepared per direct Repository Owner instruction ("AUREX — C-022 — PREPARE CBOR ADR"), following the read-only CBOR-readiness investigation performed the same session, which found Commercial Account eligible under `CMD-001 §26.3a` and identified that a dedicated ADR is required before registration, mirroring `ADR-037`'s own precedent for Offering Definition.

**Affected Documents:** None amended by this ADR. `CMD-001`, `COM-001`, `PE-001-C022`, `ROD-C022`, `ROD-C022-A`, `ADR-038`, `IRA-C022`, `TDS-C022`, and `CBOR-INDEX.md` are read-only evidentiary sources this ADR builds upon; none is modified by this ADR.

**Affected Code:** None. No migration, model, schema, API, or test is created or modified by this ADR. **No implementation exists for C-022 as of this ADR** — confirmed by repository-wide search: no `c022_*` file exists anywhere in `Backend/` or `source/frontend/src`.

---

## 1. Purpose

Prepare, for a future Repository Owner registration decision, the Canonical Business Object Registration record for **Commercial Account** — the Business Object `TDS-C022`'s authorized "Establish Commercial Account" Business Activity (`ROD-C022`/`ROD-C022-A`) will persist. This ADR performs the `CMD-001 §26.3a` eligibility analysis and assembles the `§26.4`/`§26.7` registration content **ahead of implementation**, mirroring `ADR-037`'s own role for Offering Definition — but, unlike `ADR-037`, is prepared **before** any Charter, WP registration, or implementation exists for C-022, and therefore **explicitly stops short of the registration act itself** (§9).

---

## 2. Context

`COM-001-005` (LOCKED), verbatim: *"Per `CMD-001 §26.3`, no persistent commercial Business Object shall be implemented until registered in the CBOR."* `COM-001-061` (LOCKED), verbatim: *"Every construct in Sections 5–9 (Subscription, Offering Definition, Customer, **Commercial Account**, Customer–Account Relationship, Billing Arrangement, Billing Period, Billing Standing, Contract) is a Business Object per `SD-002 §2`, registered in the Canonical Business Object Register (`CMD-001 §26`) once implemented, per `COM-001-005`."* Commercial Account is therefore named, explicitly and by name, as a construct requiring CBOR registration once implemented.

C-022's governance sequence to date — `ROD-C022` (capability boundary and BA-01 minimum scope), `IRA-C022` (readiness assessment, 🟢 GREEN-leaning), `TDS-C022` (technical design for "Establish Commercial Account"), `IRA-TDS-C022_Independent_Review.md` (independent gate, PASS WITH CONDITIONS), `ROD-C022-A` (resolving two of those conditions — classification and read/list), and `ADR-038` (resolving the `COM-001-033`↔`PE-001-C022` classification conflict, Option A) — has established a stable, RO-decided BA-01 boundary sufficient to describe Commercial Account's registration content, even though no Charter, WP, or implementation yet exists.

---

## 3. `CMD-001 §26.3a` Eligibility Analysis

Re-verified directly against `CMD-001` for this ADR, not merely cited from `IRA-C022 §11`:

**Step 1 — Independent Identity.** *"Does the candidate have identity separable from the request that produced it? A value that exists only for one request/response cycle is not a Business Object."* `COM-001-033` defines the Authoritative Account Context as a persisted, keyed fact ("Keyed only to its own Commercial Account Anchor... exactly one exists per Commercial Account Anchor at any time"), not a transient response value. **Satisfied.**

**Step 2 — Cross-Experience Reference Test.** *"Named as Required or Consumed Context by a Business Activity or Enterprise Experience other than the one that produces it."* `COM-001-036` (LOCKED), verbatim: *"The stable Customer Reference, **Commercial Account Reference**, and/or Customer–Account Relationship Reference, plus Account hierarchy and status, are made available for consumption by Subscription (C-020), Product & Service Catalog (C-021, conditional segment reference), Licensing & Entitlement (C-023), Billing (C-024), and Contract (C-025)."* Five other capabilities are named as consumers by identity. **Satisfied.** (This finding does not depend on, and is not weakened by, `ROD-C022-A` D8's establish-only scope — the cross-reference test concerns the governing text's own naming of consumers, not whether BA-01's current API happens to expose a retrieval path; see §11.)

**Step 3 — Governed Lifecycle.** *"A state that persists and is later invalidated by a subsequent event, or explicitly self-describes as transient."* `COM-001-033`'s own status attribute, plus `PE-001-C022`'s full reclassify/retire/reactivate lifecycle (`ERB-C022-03`, `ERB-C022-06`), describe a real, persisting, invalidatable state. **Satisfied**, independent of how much of that lifecycle BA-01 itself exercises (see §12).

**Result:** Step 1 satisfied, and both of Steps 2–3 satisfied (only one is required). **Commercial Account is eligible for registration under `CMD-001 §26.3`/`§26.4`.**

---

## 4. `CMD-001 §26.4` Registration Content (prepared, not yet entered into `CBOR-INDEX.md`)

Following `ADR-037`'s own adapted registration-table precedent, not `§26.4`'s full 16-attribute list verbatim (consistent with every prior CBOR ADR in this repository):

| `CMD-001 §26.4` attribute | Value |
|---|---|
| Business Object Identifier | **Not assigned by this ADR** — see §5. |
| Canonical Name | Commercial Account |
| Owning Capability | C-022 (Customer & Account Management) |
| Owning Specification | `COM-001` §7 (`COM-001-030`–`036`) |
| Aggregate Root | The Authoritative Commercial Account Context itself. **Excludes** the Authoritative Customer–Account Relationship Context and any Customer-authority concern — `COM-001-030`'s own "three independent authorities" rule keeps Customer, Account, and Relationship separately keyed, never combined into one aggregate. No child entities in BA-01 (relate/transfer/merge/split are excluded, `ROD-C022 §H`). |
| Primary Data Category | Commercial / Master Data (the enterprise's authoritative record of a Commercial Account, mirroring `ADR-037`'s own classification of Offering Definition as Commercial/Master Data). |
| Identity Structure | `id` (UUID surrogate) + `account_reference` (the `COM-001-001` Universal Identity, `PREFIX-NNNNNN` form, system-assigned, unique — the stable, externally-citable Account Reference). Per `TDS-C022 §7`, as corrected during this session's independent-review remediation pass: `COM-001-001` is inherited in full by Section 7 (`COM-001` line 44's own inheritance preamble), so the `PREFIX-NNNNNN` format is a LOCKED requirement, not an open implementation choice — only the concrete generation *mechanism* remains implementation-time. |
| Lifecycle Model | `COM-001-033`'s Account status attribute — `PE-001-C022`'s illustrative set is `{active, suspended, retired}` (an `[INFERENCE]`, per `TDS-C022 §6.1`, not a verbatim `COM-001-033` enumeration). **BA-01 exercises only establishment, writing `status = 'active'`; reclassify/retire/reactivate are future C-022 increments**, not implemented or authorized here (`ROD-C022-A §H`). No classification-based lifecycle branching exists — `ADR-038` Option A confirms Commercial Account carries no classification attribute (§7 below). |
| Physical Implementation Mapping (`CMD-001 §26.7`) | **Conceptual / planned only — no implementation exists.** See §6. |
| Tenant Scope | **Platform-global** — no `organization_id` column, per `ROD-C022` D2. |

---

## 5. Business Object Identifier — Not Assigned by This ADR

**Determination: an identifier is not legitimately assignable at this stage, and none is assigned.** `CMD-001 §26.4a` governs the identifier *format* (`PREFIX-NNNNNN`, per `SD-002-004`) but not a separate reservation procedure distinct from registration itself. Direct inspection of every prior CBOR ADR (`ADR-006`, `-008`, `-009`, `-011`, `-012`, `-013`, `-015`, `-019`, `-037`) shows the Business Object Identifier is always assigned **as part of the same act** that amends `CBOR-INDEX.md §3` — `ADR-037`'s own Decision item 1 ("Register... identifier `OFR-000001`") and Decision item 2 ("`CBOR-INDEX.md §3` is amended to add the `OFR-000001` row") occur together, in the same document, as one registration act. No precedent exists anywhere in this repository for assigning an identifier in advance of that act, and this task's own explicit prohibition on amending `CBOR-INDEX.md` means the uniqueness check that act performs (confirming the identifier does not collide with an existing row) cannot itself be completed here. **Assigning a specific identifier now would therefore not be a legitimate application of the repository's own convention — it would invent a step the convention does not have.** The Business Object Identifier for Commercial Account **shall be assigned at the time actual registration is authorized and performed**, following the same `PREFIX-NNNNNN` convention every prior registration used (illustratively, a three-letter prefix derived from "Commercial Account" — not committed to here, not binding, and not to be treated as reserved).

---

## 6. Physical Implementation Mapping — Explicitly Conceptual / Planned, Not Implemented

**No migration, table, API, or event currently exists for Commercial Account.** The mapping below is drawn entirely from `TDS-C022`'s own *conceptual* design (its own Technical Design, itself explicitly not an implementation) and is labeled accordingly — it does not claim, and must not be read as claiming, that any of the following has been built.

| `CMD-001 §26.7` attribute | Conceptual / planned value | Source |
|---|---|---|
| Physical Tables (planned) | `c022_commercial_account` (**not created**) | `TDS-C022 §6.1`, conceptual schema |
| APIs (planned) | `POST /commercial-accounts` establish only (**not implemented**). **No `GET`/list/read endpoint is planned or claimed** — `ROD-C022-A` D8 authorizes establish only; `TDS-C022 §15` explicitly designs no other route. | `TDS-C022 §15` |
| Events Published (planned) | `record_audit(action="ESTABLISH_COMMERCIAL_ACCOUNT", ...)` + `publish_event("COMMERCIAL_ACCOUNT_ESTABLISHED", ...)` (**not implemented** — existing structured-log stand-in, not a real event bus, per `IRA-C021 §16`'s identical disclosure for the same mechanism class) | `TDS-C022 §17` |
| Events Consumed | None designed. | `TDS-C022` |
| Service host (planned) | `AuthService`, per `ROD-C022` D3 (**no code exists**). | `TDS-C022 §5`/`§13` |

**This table is forward-looking design documentation, not a record of built infrastructure.** It exists so that, if and when a Repository Owner authorizes actual registration, the Physical Implementation Mapping can be completed by substituting the real migration filename and confirmed route set for these planned values — mirroring exactly how `ADR-037`'s own equivalent row cited the real, already-existing `c021_offering_definition` migration filename at the point *that* ADR was finalized. **Until implementation exists, this row cannot be finalized**, and this ADR does not attempt to finalize it.

---

## 7. Consistency with `ADR-038` (Classification) and `ROD-C022-A` (D7/D8)

**No classification attribute appears anywhere in this ADR's registration content (§4) or physical mapping (§6).** This is a deliberate, verified consistency with `ADR-038`'s own recorded decision (§0, Option A — "the Authoritative Commercial Account Context does NOT carry a 'classification' attribute") and `ROD-C022-A §B.2`'s D7. `ADR-038` and `ROD-C022-A` are read-only sources for this ADR and are not reopened, reinterpreted, or altered.

**No read/list capability appears anywhere in §6's Physical Implementation Mapping.** This is a deliberate, verified consistency with `ROD-C022-A §C.2`'s D8 ("BA-01 remains establish-only... NO read/list functionality"). `ROD-C022-A` is not reopened, reinterpreted, or altered by this ADR.

---

## 8. `CMD-001 §26.3`/`COM-001-005` Governance Basis

`COM-001-005` requires CBOR registration before **implementation** — it does not require registration before Charter or WP registration, and no C-022 Charter or WP exists as of this ADR. This ADR performs the eligibility analysis and assembles the registration content **in advance of implementation**, consistent with `COM-001-005`'s own requirement, but **does not perform the registration act itself** (identifier assignment + `CBOR-INDEX.md §3` amendment) — that remains a separate, explicit, future Repository Owner authorization (§9). This sequencing choice — preparing the ADR ahead of Charter/implementation, rather than bundling it with them as `ADR-037` did for C-021 — is a deliberate departure from the one prior executed precedent, made explicit here rather than silently assumed to be equivalent (per the read-only investigation's own §F/§G findings).

---

## 9. What This ADR Does NOT Authorize

- **CBOR registration itself.** `CBOR-INDEX.md` is not amended. No Business Object Identifier is assigned (§5).
- **BAR registration or any BAR decision.** `COM-001-005` treats CBOR (Business Object) and BAR (Business Activity) registration as independent, parallel requirements — confirmed directly against `CBOR-INDEX.md §2`'s own precedent for `OFR-000001`, which states its BAR question "is not recorded here regardless, because this Index registers Business Objects, not Business Activities." This ADR does not require, perform, or comment further on BAR (`IRA-C022 §11`, `[C-7]`, unchanged).
- **Resolution of the `TDS-C022 §15.1` lifecycle-pattern-realization question** — unchanged, remains open.
- **Resolution of the `PE-001-C022` classification-passage correction `ADR-038 §9` identifies as future work** — unchanged, remains open, not performed here.
- Any Charter, WP registration, or implementation of any kind.
- Any modification to `COM-001`, `PE-001-C022`, `CMD-001`, `ROD-C022`, `ROD-C022-A`, `ADR-038`, `IRA-C022`, or `TDS-C022`.

---

## 10. Remaining Prerequisites Before Actual Registration

1. **A separate, explicit Repository Owner authorization** to perform the registration act itself (assign the Business Object Identifier; amend `CBOR-INDEX.md §3`).
2. **A decision on sequencing** (§8) — whether registration proceeds now, ahead of Charter/implementation (accepting a conceptual-only Physical Implementation Mapping until implementation catches up), or is deferred until Charter/WP/implementation exist, mirroring `ADR-037`'s own precedent exactly.
3. If registration proceeds ahead of implementation: an explicit acknowledgment that §6's Physical Implementation Mapping will need a follow-up correction once real code exists, to replace "planned" values with actual ones — mirroring how `TDS-C021`/`ADR-037` themselves were kept current as WP-20 progressed.
4. **Independent of CBOR:** BAR remains a separate, still-open item (`IRA-C022 §11`, `[C-7]`) — not a prerequisite to CBOR registration, but still required before implementation, per `COM-001-005`'s own parallel clause.

---

## 11. Note on `ROD-C022-A` D8 and Step 2 Eligibility

Recorded for completeness, not resolved here: `COM-001-036`'s naming of Commercial Account as consumed by five other capabilities is a **constitutional-text** fact, established independent of whether BA-01's own current API can actually satisfy that consumption. `ROD-C022-A` D8 (establish-only, no read/list) does not affect CBOR eligibility (§3, Step 2) but does mean that, today, nothing can retrieve the reference a future Subscription (C-020) would need to consume — a previously-disclosed tension (`IRA-TDS-C022_Independent_Review.md §7.2`) that this ADR does not resolve and is not authorized to resolve.

---

## 12. Note on Lifecycle Scope

Recorded for completeness, not resolved here: `TDS-C022 §15.1`'s own open question — whether BA-01's single-call establish design adequately realizes `COM-001-002`/`-003`'s inherited Anchor/Intent/Proposed/Assessment lifecycle pattern — does not affect CBOR eligibility (§3, Step 3, which tests the *governing text's* description of a lifecycle, not the *implementation's* fidelity to it) and is not addressed further by this ADR.

---

## 13. Traceability

| Item | Source |
|---|---|
| CBOR eligibility investigation (read-only) | "AUREX — C-022 BA-01 — INVESTIGATE CBOR REGISTRATION READINESS," this session |
| Structural precedent | `ADR-037_Offering_Definition_Canonical_Business_Object_Registration.md` |
| Classification consistency | `ADR-038 §0` (Option A); `ROD-C022-A §B.2` (D7) |
| Read/list consistency | `ROD-C022-A §C.2` (D8) |
| Identity Structure / `PREFIX-NNNNNN` correction | `TDS-C022 §7` (post-`[C-3]`-remediation) |
| Aggregate Root exclusion of Relationship | `COM-001-030` (Three Independent Authorities) |

---

*End of ADR-039. Status: PROPOSED — REGISTRATION PREPARATION ONLY. No Business Object Identifier assigned. `CBOR-INDEX.md` not amended. No BAR action taken or required. No classification attribute included, consistent with `ADR-038`. No read/list capability claimed, consistent with `ROD-C022-A` D8. No implementation exists and none is authorized by this ADR. The next action is a separate, explicit Repository Owner decision on whether and when to perform actual CBOR registration. Nothing was staged, committed, or pushed.*
