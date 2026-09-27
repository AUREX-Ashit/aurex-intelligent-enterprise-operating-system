# ADR-040 — Commercial Account Registered as a Canonical Business Object (WP-21, C-022)

**Status:** Accepted
**Classification:** Architecture Governance / Business Object Registration (Execution)
**Decided by:** Repository Owner (architecture governance authority), as an explicit governance prerequisite named in the WP-21 / C-022 BA-01 governance-actions bundle ("Proceed with the next C-022 governance actions, as one controlled bundle: 1. CBOR REGISTRATION 2. WP REGISTRATION 3. IMPLEMENTATION AUTHORIZATION", 2026-09-15) — the same decision-authority pattern `ADR-006`–`ADR-013` (WP-04), `ADR-015` (WP-05), `ADR-019` (WP-10), and `ADR-037` (WP-20) already established.
**Affected Documents:** `architecture/00-Governance/CBOR-INDEX.md` (§3 register row added). **`CMD-001` is not amended. `COM-001` is not amended (its `COM-001-005`/`-061` already mandate this registration). `ADR-006` through `ADR-039` are not amended or revisited.**

---

## 1. Relationship to `ADR-039`

`ADR-039_Commercial_Account_Canonical_Business_Object_Registration_Preparation.md` (Status: PROPOSED — REGISTRATION PREPARATION ONLY) already performed, in full, the `CMD-001 §26.3a` eligibility analysis and assembled the `§26.4`/`§26.7` registration content for Commercial Account, ahead of implementation. `ADR-039` explicitly withheld two things: (a) assignment of a Business Object Identifier, and (b) amendment of `CBOR-INDEX.md`, pending a separate, explicit Repository Owner authorization to perform the registration act itself (`ADR-039 §5`/§10`).

**This ADR is that separate, explicit authorization, now executed.** It does not re-derive or alter `ADR-039`'s own eligibility analysis, registration-content table, or Physical Implementation Mapping reasoning — it adopts them by reference, exactly as `ADR-037`'s own rationale adopted `IRA-C021 §8`'s analysis rather than repeating it. `ADR-039` itself is **not modified** by this ADR — it remains the historical record of the preparation step; this ADR is the historical record of the execution step, mirroring the two-artifact shape this repository already uses elsewhere for a preparation/execution split (e.g., `ROD-C022`/`ROD-C022-A`/`ROD-C022-B` as sequential, non-overwriting addenda).

## 2. Eligibility (adopted from `ADR-039 §3`, not re-derived)

`CMD-001 §26.3a` Canonical Business Object Eligibility Test, as independently confirmed in `ADR-039 §3` and `IRA-C022 §11`: Step 1 (Independent Identity) — satisfied, a persisted Account Reference beyond any single request; Step 2 (Cross-Experience Reference) — satisfied, `COM-001-036` names C-020/C-021 (conditional)/C-023/C-024/C-025 as consumers by identity; Step 3 (Governed Lifecycle) — satisfied, `COM-001-033`'s status attribute and the full `PE-001-C022` lifecycle. **Eligible for canonical registration.**

## 3. Decision

1. **Register "Commercial Account" as a canonical Business Object**, identifier **`CAC-000001`**, per `SD-002 §2`, `CMD-001 §26.3`/`§26.3a`/`§26.4`, and `COM-001-061`.

   **Identifier determination:** `CAC-000001` was selected as the next valid, non-colliding identifier following this repository's own `PREFIX-NNNNNN` convention (`CMD-001 §26.4a`/`SD-002-004`). Verified directly against `CBOR-INDEX.md §3` before assignment: the nine existing entries use `SCI`, `POC`, `IMC`, `RVC`, `VLC`, `RSC`, `AEO`, `CFG`, `OFR` — `CAC` collides with none of them, and a repository-wide search confirms no other document reserves or uses `CAC-000001` for any other purpose. `CAC` is derived directly from the canonical name ("Commercial ACcount"), consistent with the convention's mixed derivation pattern (some entries are multi-word acronyms — `AEO`, `RSC` — others are single-word abbreviations — `OFR`, `CFG`). This is the object's first and only registered instance, hence sequence `000001`, matching every existing entry's own first-instance numbering.

   The registration entry, per `ADR-039 §4`'s already-prepared content (reproduced here for the completed record, unaltered in substance):

   | `CMD-001 §26.4` attribute | Value |
   |---|---|
   | Business Object Identifier | `CAC-000001` |
   | Canonical Name | Commercial Account |
   | Owning Capability | C-022 (Customer & Account Management) |
   | Owning Specification | `COM-001` §7 (`COM-001-030`…`-036`) |
   | Aggregate Root | The Authoritative Commercial Account Context itself. **Excludes** the Authoritative Customer–Account Relationship Context and any Customer-authority concern (`COM-001-030`'s Three Independent Authorities rule). No child entities in BA-01. |
   | Primary Data Category | Commercial / Master Data. |
   | Identity Structure | `id` (UUID surrogate) + `account_reference` (`COM-001-001` Universal Identity `PREFIX-NNNNNN`, system-assigned, unique). |
   | Lifecycle Model | `COM-001-033` Account status. **BA-01 exercises only establishment of `active`; reclassify/retire/reactivate are a future C-022 increment.** No classification attribute (`ADR-038` Option A). Single-call establish realization of `COM-001-002`/`-003`'s lifecycle pattern accepted per `ROD-C022-B` D9, Option A. |
   | Physical Implementation Mapping (`CMD-001 §26.7`) | **Still conceptual/planned — no implementation exists as of this ADR.** `AuthService`, table `c022_commercial_account` (`TDS-C022 §6.1`), model `models/c022_commercial_account.py`, router `routers/commercial_account.py` (all per `TDS-C022 §9`/`§10`, design only). **This row will require a follow-up correction to substitute the real migration filename and confirmed route set once implementation exists** — mirroring `ADR-037`'s own row, which cited a real, already-existing migration because registration there occurred alongside implementation. This registration precedes implementation (permitted, not required, by `COM-001-005`), a deliberate, disclosed departure from `ADR-037`'s own bundled-with-implementation precedent, made at explicit Repository Owner direction. |
   | Tenant Scope | **Platform-global** — no `organization_id` column (`ROD-C022` D2). |

2. **`CBOR-INDEX.md` §3 is amended** to add the `CAC-000001` row, per its own Amendment Procedure (§4): "Add a new row when… a candidate concept passes `CMD-001 §26.3a`'s Eligibility Test and is registered via its own ADR." This ADR performs that registration.

3. **Scope is strictly the Commercial Account Business Object**, per the governing instruction's own bundle framing ("CBOR registration is now authorized, but it must be actual registration only... Do not introduce classification, lifecycle, Customer, Organization, Identity, Person, Subscription, Billing, Contract, or Entitlement semantics beyond the approved Charter"). No other `COM-001` Section 5–9 construct is registered here.

4. **No classification, lifecycle expansion, Customer, Organization, Identity, Person, Subscription, Billing, Contract, or Entitlement semantic is introduced by this registration.** The registration entry (item 1 above) reproduces exactly `ADR-039`'s own already-reviewed content — no field, value, or characterization differs from `ADR-039 §4` except the identifier itself (now assigned) and the Physical Implementation Mapping's own explicit "still conceptual" framing (unchanged in substance, restated for the completed record).

5. **This ADR does not perform BAR registration.** `COM-001-060` (BAR Integration) applies to the BA-01 Business Activity once implemented. **No physical Business Activity Registry artifact exists in this repository.** `ROD-C022-B` D10 (Option A, 2026-09-15) already resolved this as C-022's own explicit decision: no BAR registry/mechanism is created, no Business Activity Identifier is assigned, and the `COM-001-060` obligation is deferred to a future enterprise-level BAR-mechanism decision — mirroring `ADR-037`'s own disposition for C-021. **This ADR still performs only the CBOR registration** (`CAC-000001`); no BAR identifier or mechanism is created or implied.

6. **This ADR does not authorize implementation of BA-01 by itself.** Implementation Authorization is a separate Repository Owner act, recorded in `WP-21_C022_BA-01_Establish_Commercial_Account_Business_Activity_Charter.md`'s own "Implementation Authorization" section (added in the same governance pass as this ADR, per the same bundled instruction), not performed by this document.

7. **This ADR does not create a pattern-level ADR.** A single Business Object with a state-model lifecycle is the ordinary `CMD-001 §26.4` registration shape, per `ADR-037 §Decision item 6`'s identical reasoning.

## Rationale

`COM-001-005` and `COM-001-061` make CBOR registration of Commercial Account a stated constitutional requirement for C-022 specifically. `ADR-039`'s own eligibility analysis (adopted at §2 above) confirms all three `§26.3a` steps independently — this ADR's role is to execute the registration `ADR-039` prepared, following explicit Repository Owner authorization, not to re-decide eligibility.

**Sequencing note, disclosed rather than silently normalized:** unlike `ADR-037` (which registered `OFR-000001` alongside real, already-existing implementation), this registration precedes any C-022 implementation, migration, model, or code — the Repository Owner's own bundled instruction explicitly authorized CBOR registration, WP registration, and Implementation Authorization together, ahead of implementation itself. `ADR-039 §8` had recommended the `ADR-037`-mirroring sequencing (Option B — defer registration until Charter/Implementation Authorization exists); the Repository Owner's own subsequent instruction bundles registration with Charter/Implementation Authorization rather than with completed implementation, which is `ADR-039 §8`'s Option B in substance (registration occurs alongside Charter/Implementation Authorization, not before either) — not `ADR-039`'s rejected Option A (registration before any Charter exists at all). This ADR records that alignment explicitly rather than leaving it to be inferred.

## Consequences

- C-022 BA-01's Business Object eligibility question (`IRA-C022 §11`, `ADR-039 §3`) is resolved: one registered — `CAC-000001` — Commercial Account.
- `CBOR-INDEX.md` §3 gains one new row for `CAC-000001`.
- `CMD-001` and `COM-001` are not amended, consistent with their LOCKED status.
- `ADR-039` is not amended — it remains the historical preparation record; this ADR is the execution record.
- No BAR registration occurs; `ROD-C022-B` D10 (deferred, no mechanism, no identifier) is unaffected and unaltered.
- No classification attribute, lifecycle expansion, or cross-capability semantic (Customer, Organization, Identity, Person, Subscription, Billing, Contract, Entitlement) is introduced.
- The Physical Implementation Mapping (item 1 table, Lifecycle Model/Physical Implementation Mapping rows) remains explicitly conceptual/planned and will require a follow-up correction once real implementation exists, exactly as `ADR-039 §6`/§10` already anticipated.
- Implementation Authorization for WP-21 / C-022 BA-01 is recorded separately, in the Charter, per the same governance pass's own bundled instruction — not performed by this ADR.

## Status

**Accepted**
