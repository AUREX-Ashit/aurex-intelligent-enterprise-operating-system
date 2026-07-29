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

Every entry below originates from WP-04 (Enterprise Structure Management, C-005).

---

## 3. Register

| Business Object Identifier | Canonical Name | Owning Capability | Registering ADR | IRA-004 Section |
|---|---|---|---|---|
| `SCI-000001` | Structural Change Intent | C-005 (Enterprise Structure Management) | ADR-006 | §21 |
| `POC-000001` | Proposed Outcome Context | C-005 (Enterprise Structure Management) | ADR-008 | §22 |
| `IMC-000001` | Impact Context | C-005 (Enterprise Structure Management) | ADR-009 | §23 |
| `RVC-000001` | Review Context | C-005 (Enterprise Structure Management) | ADR-011 | §25 |
| `VLC-000001` | Validation Context | C-005 (Enterprise Structure Management) | ADR-012 | §26 |
| `RSC-000001` | Resulting Structural Context | C-005 (Enterprise Structure Management) | ADR-013 | §27 |

**Pattern-level decision (not itself a registration):** `ADR-010` recognizes the six objects above as one coherent Structural Context Lifecycle (IRA-004 §24). It is cited by `ADR-011`, `ADR-012`, and `ADR-013` for eligibility rather than each re-deriving the Cross-Experience Reference Test independently, but it does not register a Business Object of its own and therefore has no row in §3.

**Phase-scope decision (not a registration):** `ADR-007` resolves BA-04's own v1 target-type scope (EnterpriseNode-only). It is a phased-implementation-scope decision, not a Business Object registration, and therefore has no row in §3.

---

## 4. Amendment Procedure

Add a new row when, and only when, a candidate concept passes CMD-001 §26.3a's Canonical Business Object Eligibility Test and is registered via its own ADR under CMD-001 §26.4's Canonical Registration Structure. Do not add speculative or pending entries. Do not remove an entry once registered, even if the owning Business Activity is later superseded — CMD-001 §26's own registration is a constitutional record, not an implementation-status field.
