# CBOR-INDEX — Canonical Business Object Register Index

**Status:** Living document — amended as new Business Objects are registered.
**Owning rule:** CMD-001 §26 (Canonical Business Object Register), operationalized by CMD-001 §26.3a (Canonical Business Object Eligibility Test).
**Relocated per:** ADR-014 §4 item 4 — this index lives in `architecture/00-Governance/`, not `architecture/02-Constitutional/`, because it is a living, frequently-amended cross-Work-Package index (the same class of artifact as `WPR-001`), not LOCKED constitutional text.

---

## 1. Purpose

This index lists every Canonical Business Object registered under CMD-001 §26 across all Work Packages, in one place, so that a future Work Package's own Mandatory Context Discovery (IMP-001 §6.2a) can check for an existing registration before proposing a new one.

This index does not itself register anything. Each entry's registering ADR remains the authoritative registration record; this index is a pointer to it.

---

## 2. Coverage Confirmation

Per ADR-014 §4 item 4, this index was backfilled by searching the repository for existing registrations, not assumed. `IRA-001`, `IRA-002`, and `IRA-003` (WP-01, WP-02, WP-03) were checked for Business Object Identifier / CMD-001 §26 registrations and contain none. No capability-specification review for an equivalent Context Model section (analogous to PE-001-C005 §38.15) was performed for PE-001-C004 or PE-001-C007 as part of this backfill — this remains genuinely unresolved, as ADR-014 §7 step 4 itself discloses, and is not asserted here as "no Business Objects exist" for those capabilities, only as "none are yet registered."

Entries originate from WP-04 (Enterprise Structure Management, C-005), WP-05 (Access Management, C-002), WP-10 (Configuration Management, C-041), WP-20 (Product & Service Catalog, C-021), and WP-21 (Customer & Account Management, C-022). The `AEO-000001` row was added 2026-08-02 as an incidental correction (`ADR-019` §Decision item 6): `ADR-015` registered it but this Index's own Amendment Procedure was not separately executed at WP-05 closure, so the row was missing until now — `ADR-015`'s own decision is unchanged. The `OFR-000001` row was added 2026-09-08 by `ADR-037` (WP-20 / C-021 BA-01), executing this Index's Amendment Procedure in the same governance pass — the first CBOR registration mandated by `COM-001-005`/`-061` for a `COM-001` Section 5–9 commercial construct. ~~`COM-001-060`'s companion BAR registration for the C-021 BA-01 Business Activity is a separate, still-open governance item (no physical BAR artifact exists in this repository) — see `WP-20 §26` / `IMP-REPORT-WP-20 §3`~~ *(Corrected 2026-09-13, Gate 5 attempt #7 finding `G7-01` — this was accurate only before the Repository Owner's BAR decision. Current: the `COM-001-060` companion BAR-registration question was resolved by Repository Owner decision, 2026-09-08 — no BAR mechanism was created, none is invented here, and it is not a dependency of this Index's own OFR-000001 registration. Full text: `IMP-REPORT-WP-20 §3.1`; also recorded in `WP-20 §26`, `ADR-037` §Decision item 5 and its own Correction note, and the `WPR-001` WP-20 row.)* It is not recorded here regardless, because this Index registers Business Objects, not Business Activities — that remains true independent of the BAR decision's own resolution.

The `CAC-000001` row was added 2026-09-15 by `ADR-040` (WP-21 / C-022 BA-01), executing this Index's Amendment Procedure. Eligibility and registration content were first assembled, without executing registration, by `ADR-039_Commercial_Account_Canonical_Business_Object_Registration_Preparation.md` (Status: PROPOSED — REGISTRATION PREPARATION ONLY, unchanged, unmodified by this registration); `ADR-040` is the separate, subsequent Repository Owner authorization that executes it, per direct Repository Owner instruction ("Proceed with the next C-022 governance actions... CBOR REGISTRATION / WP REGISTRATION / IMPLEMENTATION AUTHORIZATION"). This registration precedes C-022 implementation — no `c022_commercial_account` table, model, migration, or API exists as of this entry; `ADR-040`'s own Physical Implementation Mapping row is explicitly conceptual/planned and will require a follow-up correction once implementation exists, mirroring the disclosure convention this Index already used for `OFR-000001`'s own BAR note above. The `COM-001-060` companion BAR registration for the C-022 BA-01 Business Activity is a separate, still-open governance item, resolved as **deferred** by explicit Repository Owner decision (`ROD-C022-B` D10, Option A, 2026-09-15) — no BAR mechanism was created, none is invented here, and it is not a dependency of this Index's own `CAC-000001` registration, for the identical reason `OFR-000001`'s own entry above already establishes.

---

## 3. Register

| Business Object Identifier | Canonical Name | Owning Capability | Registering ADR | Source IRA Section |
|---|---|---|---|---|
| `SCI-000001` | Structural Change Intent | C-005 (Enterprise Structure Management) | ADR-006 | §21 |
| `POC-000001` | Proposed Outcome Context | C-005 (Enterprise Structure Management) | ADR-008 | §22 |
| `IMC-000001` | Impact Context | C-005 (Enterprise Structure Management) | ADR-009 | §23 |
| `RVC-000001` | Review Context | C-005 (Enterprise Structure Management) | ADR-011 | §25 |
| `VLC-000001` | Validation Context | C-005 (Enterprise Structure Management) | ADR-012 | §26 |
| `RSC-000001` | Resulting Structural Context | C-005 (Enterprise Structure Management) | ADR-013 | §27 |
| `AEO-000001` | Access Evaluation Outcome | C-002 (Access Management) | ADR-015 | IRA-005 §11 |
| `CFG-000001` | Configuration Entry | C-041 (Configuration Management) | ADR-019 | IRA-010 §6 |
| `OFR-000001` | Offering Definition | C-021 (Product & Service Catalog) | ADR-037 | IRA-C021 §8 |
| `CAC-000001` | Commercial Account | C-022 (Customer & Account Management) | ADR-040 | IRA-C022 §11 |

**Pattern-level decision (not itself a registration):** `ADR-010` recognizes the six objects above as one coherent Structural Context Lifecycle (IRA-004 §24). It is cited by `ADR-011`, `ADR-012`, and `ADR-013` for eligibility rather than each re-deriving the Cross-Experience Reference Test independently, but it does not register a Business Object of its own and therefore has no row in §3.

**Phase-scope decision (not a registration):** `ADR-007` resolves BA-04's own v1 target-type scope (EnterpriseNode-only). It is a phased-implementation-scope decision, not a Business Object registration, and therefore has no row in §3.

---

## 4. Amendment Procedure

Add a new row when, and only when, a candidate concept passes CMD-001 §26.3a's Canonical Business Object Eligibility Test and is registered via its own ADR under CMD-001 §26.4's Canonical Registration Structure. Do not add speculative or pending entries. Do not remove an entry once registered, even if the owning Business Activity is later superseded — CMD-001 §26's own registration is a constitutional record, not an implementation-status field.
