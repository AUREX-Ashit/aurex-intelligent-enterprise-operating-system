# ADR-037 — Offering Definition Registered as a Canonical Business Object (WP-20, C-021)

**Status:** Accepted
**Classification:** Architecture Governance / Business Object Registration
**Decided by:** Repository Owner (architecture governance authority), as an explicit governance prerequisite named in the WP-20 / C-021 BA-01 Implementation Authorization ("C-021 — REPOSITORY OWNER IMPLEMENTATION AUTHORIZATION — WP-20 / BA-01", 2026-09-08: *"CBOR / BAR … Perform them only as authorized governance prerequisites required by the implementation sequence. Do not expand their scope beyond: Offering Definition Business Object registration; C-021 BA-01 Business Activity registration."*) — the same decision-authority pattern `ADR-006`/`ADR-008`/`ADR-009`/`ADR-011`/`ADR-012`/`ADR-013` (WP-04), `ADR-015` (WP-05), and `ADR-019` (WP-10) already established.
**Affected Documents:** `architecture/05-Implementation/IRA-C021_Product_and_Service_Catalog_Implementation_Readiness_Assessment.md` (§8 records the full `CMD-001 §26.3a` eligibility analysis this ADR adopts); `architecture/05-Implementation/TDS-C021_Product_and_Service_Catalog_Minimum_BA_Technical_Design.md` (§7 restates it and names this ADR as the mandatory registration prerequisite); `architecture/00-Governance/CBOR-INDEX.md` (§3 register row added). **`CMD-001` is not amended. `COM-001` is not amended (its `COM-001-005`/`-061` already mandate this registration). `ADR-006` through `ADR-036` are not amended or revisited.**

---

## Context

`COM-001` (LOCKED, EARB Constitutional Recertification CR-3.0) already binds this outcome directly, independent of the general-purpose `§26.3a` test:

- **`COM-001-005` (Registration Precedes Implementation):** every commercial construct is registered in the CBOR (and the BAR) before implementation.
- **`COM-001-061` (CBOR Integration):** *"Every construct in Sections 5–9 (Subscription, Offering Definition, Customer, Commercial Account, Customer–Account Relationship, Billing Arrangement, Billing Period, Billing Standing, Contract) is a Business Object per SD-002 §2, registered in the Canonical Business Object Register (CMD-001 §26) once implemented, per COM-001-005. Each becomes an Enterprise Information Object (CMD-001 §26.4b) upon that registration."*

C-021's Offering Definition is the Section 6 construct (`COM-001-020`…`-026`). WP-20 BA-01 is the first implementation of any `COM-001` Section 5–9 construct, so this is the first CBOR registration under `COM-001-061`.

`IRA-C021 §8` and `TDS-C021 §7` performed the full `CMD-001 §26.3a` Canonical Business Object Eligibility Test on "Offering Definition", per the RO-authorized minimum scope (`ROD-C021` D4 — establish / list / read a `draft` Atomic Offering Definition):

- **Step 1 (Independent Identity):** satisfied — a `PREFIX-NNNNNN` Universal Identity (`COM-001-001`) persisting as the Authoritative Offering Definition Context beyond any single request; `ROD-C021` D4 authorizes `list`/`read` as distinct later actions against a previously-established record.
- **Step 2 (Cross-Experience Reference Test):** satisfied — the Offering Reference is explicitly named as Consumed Context, retrieved *by identity*, by capabilities other than the one that produces it: C-020 consumes it to anchor and shape a Subscription (`COM-001-011` — "consumed, never recomputed, from … the Offering"); `PE-001-C021 §2.10` / `ERB-C021-06` name C-024 (Billing) and C-025 (Contract) as downstream consumers.
- **Step 3 (Governed Lifecycle):** satisfied — `COM-001-025` (Version Management) and `COM-001-020` describe a real `draft → published → retired` lifecycle, Retirement terminal, Historical Definitions retained in lineage ("never deletion"); a persisted `draft` state is later invalidated by a subsequent publication event.

**Composite:** Step 1 AND (Step 2 OR Step 3) — here all three hold. **Eligible for canonical registration.**

**Eligibility is not re-derived here** beyond the summary above — `IRA-C021 §8` and `TDS-C021 §7` perform the full step-by-step analysis; this ADR adopts their result rather than duplicating it, mirroring `ADR-019`'s adoption of `IRA-010 §6`.

---

## Decision

1. **Register "Offering Definition" as a canonical Business Object**, identifier **`OFR-000001`**, per `SD-002 §2`, `CMD-001 §26.3`/`§26.3a`/`§26.4`, and `COM-001-061`. The registration entry:

   | `CMD-001 §26.4` attribute | Value |
   |---|---|
   | Business Object Identifier | `OFR-000001` |
   | Canonical Name | Offering Definition |
   | Owning Capability | C-021 (Product & Service Catalog) |
   | Owning Specification | `COM-001` §6 (`COM-001-020`…`-026`) |
   | Aggregate Root | The Offering Definition record itself (no child entities in BA-01 — composition/relationships are excluded, `ROD-C021` D5). |
   | Primary Data Category | Commercial / Master Data (the enterprise's authoritative definition of what may be offered). |
   | Identity Structure | `id` (UUID surrogate) + `offering_reference` (the `COM-001-001` Universal Identity `PREFIX-NNNNNN`, system-assigned, unique — the stable, externally-citable Offering Reference). |
   | Lifecycle Model | `COM-001-020` offering state: `draft → published → retired` (Retirement terminal; Historical Definitions retained via `version` / `supersedes_id` on version change, `COM-001-025`). **BA-01 exercises only the establishment of `draft`; the transitions are a future C-021 increment.** |
   | Physical Implementation Mapping (`CMD-001 §26.7`) | `Backend/Services/AuthService` — table `c021_offering_definition`, model `models/c021_offering_definition.py`, migration `2026_09_08_0900-e5f6a7b8c9d0_c021_offering_definition.py`. Host per `TDS-C021 §5` (Repository Owner Option A — `AuthService`). |
   | Tenant Scope | **Platform-global** — no `organization_id` column (`ROD-C021` D8). |

2. **`CBOR-INDEX.md` §3 is amended** to add the `OFR-000001` row, per its own Amendment Procedure (§4): "Add a new row when… a candidate concept passes `CMD-001 §26.3a`'s Canonical Business Object Eligibility Test and is registered via its own ADR." This ADR performs that registration.

3. **Scope is strictly the Offering Definition Business Object**, per the Implementation Authorization's own instruction ("Do not expand their scope beyond: Offering Definition Business Object registration"). No other `COM-001` Section 5–9 construct (Subscription, Customer, Commercial Account, Customer–Account Relationship, Billing, Contract) is registered here — each remains a future registration when its own capability is implemented.

4. **This ADR does not authorize any Business Activity's implementation** beyond what the Repository Owner's WP-20 / C-021 BA-01 Implementation Authorization already authorizes. `CMD-001 §26.7` (Physical Implementation Mapping) is set by WP-20's own backend implementation (model, migration, repository), which proceeds under this registration, not independently of it.

5. **This ADR does not perform BAR registration.** `COM-001-060` (BAR Integration) requires the BA-01 Business Activity to be registered in the Business Activity Registry (`IMP-001 §6.22`) "once implemented." **No physical Business Activity Registry artifact exists in this repository** (unlike `CBOR-INDEX.md`), `IMP-001 §6.22` defines the BAR as platform-managed **runtime** metadata, and no prior Work Package (including `WP-17` and `WP-19`, both CLOSED — CERTIFIED) performed a discrete BAR-registration artifact. Establishing a BAR registry file or mechanism would be a new governance/architectural artifact beyond `TDS-C021`, which the Implementation Authorization directed be raised as **STOP-AND-REPORT**. **Repository Owner decision, 2026-09-08 ("C-021 / WP-20 — BAR DECISION + GATE 2 V&V AUTHORIZATION"):** the STOP-AND-REPORT is **resolved by RO decision** — do NOT create any BAR registry / `BAR-INDEX` / BAR file / database or runtime mechanism as part of WP-20; WP-20 does not create a BAR mechanism; the CBOR (complete — this ADR) vs. BAR (no canonical mechanism) distinction is preserved; a future enterprise-level decision may establish the canonical BAR mechanism; this decision does not create or imply C-021 ownership of the BAR mechanism and does not reopen `COM-001` or redesign the Business Activity Registry. Full text: `IMP-REPORT-WP-20 §3.1`. **This ADR still performs only the CBOR registration** (`OFR-000001`); BAR registration for the C-021 BA-01 Business Activity is deferred to that future enterprise-level BAR-mechanism decision.

6. **This ADR does not create a pattern-level ADR** (an `ADR-010` equivalent). A single Business Object with a state-model lifecycle is the ordinary `CMD-001 §26.4` registration shape.

## Rationale

`COM-001-005` and `COM-001-061` make CBOR registration of the Offering Definition a stated constitutional requirement for C-021 specifically — stronger and more direct than the general `§26.3a` test alone (the same way `CMD-001 §12.8` reinforced `ADR-019`'s registration of Configuration). The `§26.3a` analysis (`IRA-C021 §8`, `TDS-C021 §7`) confirms eligibility on all three steps, so there is no tension to resolve — the test's role here is confirmation, not decision. Registering `OFR-000001` now, alongside WP-20's migration/model implementation, mirrors `RSC-000001` (WP-04), `AEO-000001` (WP-05), and `CFG-000001` (WP-10): registration precedes and grounds implementation, never the reverse.

## Consequences

- C-021's Business Object eligibility question (`IRA-C021 §8`, `TDS-C021 §7`) is resolved: one registered — `OFR-000001` — the Offering Definition.
- `CBOR-INDEX.md` §3 gains one new row for `OFR-000001`.
- `CMD-001` and `COM-001` are not amended, consistent with their LOCKED status; this registration exercises `CMD-001 §26.3`'s own existing mechanism as `COM-001-061` directs.
- WP-20's backend implementation (model, migration, repository, service, API) and its frontend proceed under this registration.
- ~~BAR registration for the BA-01 Business Activity remains an **open governance item** pending a Repository Owner decision on the BAR mechanism (`WP-20 §26`, `IMP-REPORT-WP-20 §3`)~~ *(Corrected 2026-09-13, Gate 5 attempt #6 finding `G6-02` — this was accurate only before Decision item 5 above was resolved; it now self-contradicts this same ADR's own item 5.)* **BAR registration for the BA-01 Business Activity was resolved by Repository Owner decision, 2026-09-08 (Decision item 5 above; full text `IMP-REPORT-WP-20 §3.1`)** — WP-20 does not create a BAR mechanism, and the `COM-001-060` obligation is deferred to a future enterprise-level BAR-mechanism decision, not outstanding on this ADR or on WP-20. It does not block the WP-20 implementation (`COM-001-060`'s own "once implemented" wording), and no BAR mechanism has been, or will be, invented here.

## Status

**Accepted**

## Correction (2026-09-13, documentation-only)

The `## Consequences` section's BAR-registration bullet (above) was found live-inaccurate by an independent Gate 5 Release Readiness reviewer (finding `G6-02`, Gate 5 attempt #6 for WP-20 / C-021 BA-01) and corrected via strikethrough-preserve on the same pass this note records. **No decision in this ADR is altered.** Decision item 5 (above) already correctly recorded the Repository Owner's 2026-09-08 BAR resolution at the time this ADR was accepted; only the Consequences section's own restatement of that fact had drifted out of sync. This correction: does not reopen this ADR's Decision or Rationale; does not create a BAR registry, `BAR-INDEX`, or runtime mechanism; does not alter `COM-001`, `CMD-001`, or any RO decision; and does not affect this ADR's own `Accepted` status. ~~WP-20 / C-021 BA-01 remains NOT certified, NOT closed, NOT release-ready as of this correction; a fresh, independent Gate 5 re-attempt is pending.~~ *(Superseded 2026-09-14 — the fresh, independent Gate 5 re-attempt referenced here has since occurred (attempt #9, PASS, after eight prior FAIL attempts each remediated), and WP-20 / C-021 BA-01 is now FORMALLY CLOSED — CERTIFIED — RELEASE-READY. See `WPR-001` WP-20 row, `CERT-WP-20 §13`, `IMP-REPORT-WP-20 §26`. This ADR's own Decision and Rationale are unaffected.)*
