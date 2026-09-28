# BAR-INDEX — Business Activity Registry Index

**Status:** Living document — amended only when an actual Business Activity is registered via its own registering act (§4).
**Owning decision:** `ROD-ENTERPRISE-BAR-Decision-Preparation.md §0f` (D7) — BAR maintains its own separate authoritative Business Activity registration record, distinct from `WPR-001`.
**Built under:** `WP-23_Enterprise_BAR_Mechanism_Implementation_Charter.md`, Workstream A, per `ENTERPRISE-BAR-MECHANISM-DESIGN-AND-IMPLEMENTATION-READINESS.md §6` (BAR Registration Index Model).
**Structural precedent:** `CBOR-INDEX.md` — this index mirrors its own shape (a living, frequently-amended cross-Work-Package index that is itself a pointer to each registering act, not the registration act's own source of authority) for the structurally analogous Business Activity case, per `ONT-001 §2`'s own finding that BAR and CBOR are "two distinct registries, neither a subset of the other."

---

## 1. Purpose

This index lists every Business Activity registered under the enterprise Business Activity Registry (BAR) mechanism, in one place, so that a future Work Package's own Mandatory Context Discovery (`IMP-001 §6.2a`) can check for an existing registration before proposing a new one, ~~and so that the (not-yet-built) Business Activity Engine has a single authoritative source to query for discovery and execution-gate purposes once Workstreams D/E are implemented.~~ *(Updated 2026-09-25, RD-23-03 Option D.)* It also provides governance visibility into what the runtime registration record (the `bar_registration` table) holds. That table, not this index, is what execution-time BAR logic queries (§1 Authority).

**This index does not itself register anything.** Each entry's registering act (mirroring the CBOR-ADR pattern, per `ROD-ENTERPRISE-BAR §D5.7`) remains the authoritative registration record; this index is a pointer to it, exactly as `CBOR-INDEX.md §1` already establishes for Business Objects.

**Authority, stated explicitly (per D7):**
- ~~**`BAR-INDEX.md` (this document) is authoritative for Business Activity BAR registration** — canonical identity, registration status, and the traceability fields §3 defines.~~ *(Superseded 2026-09-25 by Repository Owner decision **RD-23-03, Option D — Layered Authority Model**; see `architecture/06-Reviews/ROD-WP-23-AC-BAR-Registry-Authority-Decision-Preparation.md §0`.)*
  - **Governance registration authority:** each Business Activity's **registering act**. It establishes that registration was authorized, by which act, by what authority, and why. (This is unchanged from the paragraph above.)
  - **Runtime execution registration:** the persistent **`bar_registration` table**. It is the runtime source queried by execution-time BAR logic. A row there does not, by its existence alone, prove that the governance authorization exists.
  - **`BAR-INDEX.md` (this document):** the **governance catalogue and index**. It provides human and governance visibility and traceability for canonical identity, registration status and the §3 fields. It is **not** the runtime execution lookup source and must not become a second runtime authority.
  - **Reconciliation:** the registering act and the runtime row must remain traceably related. No automated reconciliation or enforcement mechanism is decided yet, and none exists today (`ROD-WP-23-AC §0.4`).
- **`WPR-001` remains authoritative for Work Package → Capability governance only** (`WPR-001 §1`, its own unaltered Purpose statement) — it is not modified by this index and carries no Business Activity registration field.
- **`CBOR-INDEX.md` remains authoritative for Business Object registration only** (`CMD-001 §26`) — it is not modified by this index.
- **These three registries are distinct and cross-referenced by pointer, never merged.** A Business Activity Identifier (`BA-NNNNNN`) is never equated with a Work Package number, a Business Object Identifier (e.g., `BIA-000001`), or a `CAP-001` capability ID.

---

## 2. Governance Baseline (D1–D9, re-confirmed, not re-litigated)

This index implements exactly the enterprise BAR scope already decided in `ROD-ENTERPRISE-BAR-Decision-Preparation.md` — it does not expand, narrow, or reinterpret any of the following:

- **D2 (LOCKED-minimum scope):** BAR owns Business Activity cataloguing/registration, canonical identity, execution-time registration gating, and registry-exclusive discovery — nothing broader. This index's own Register (§3) accordingly carries only the fields those four responsibilities require; it does **not** import `IMP-001 §6.22`'s fuller attribute schema, validation checklist, status/version/dependency-management, governance-workflow, or observability metadata (D2/D6).
- **D5 (identifier authority/timing):** BAR is the canonical Business Activity Identifier authority; the identifier is assigned at BAR registration — never earlier. `BA-NNNNNN` (six-digit, zero-padded, sequential, starting at `BA-000001`) is the proposed concrete format, per `ENTERPRISE-BAR-MECHANISM-DESIGN-AND-IMPLEMENTATION-READINESS.md §5` — **`[IMPLEMENTATION DESIGN — not constitutional text]`**, re-confirmed here, not upgraded to a constitutional requirement by this index's own use of it.
- **D3 (retroactive registration):** all 21 existing Business Activity rows identified in `ROD-ENTERPRISE-BAR §D3.4` / the design document's own §11 are eventually subject to registration in this index. **None is registered by the act of creating this index.** This index is structurally capable of holding all 21 entries (plus any future Business Activity) once each row's own registering act (Workstream C) occurs — see §5 below.
- **D8 (transitional execution gate):** newly introduced/future Business Activities are gated immediately once BAR is operational; the 21 existing rows continue executing during a governed transition until each is individually registered; no permanent exemption. This index does not implement the gate itself (Workstream E) — ~~it exposes the single authoritative `Registration Status` field (§3) that a future gate implementation will consume.~~ *(updated 2026-09-25, RD-23-03 Option D)* a future gate consumes the runtime registration state held in the `bar_registration` table. This index's `Registration Status` column is its governance-visible counterpart.
- **D9 (per-BA cutover):** each existing Business Activity transitions independently, upon completing its own registering act — one row's own unresolved data does not block another. This index's own per-row structure (one row per Business Activity, §3) directly supports this; no population-wide gating field exists anywhere in this index.

---

## 3. Register

**No Business Activity is currently registered.** ~~This is the expected state at the close of Workstream A — this workstream builds the index's own structure; it does not perform any registering act for any of the 21 existing rows or any future Business Activity (Workstream C, not yet executed).~~ *(Updated 2026-09-25, status correction only.)* This remains the expected state. Workstream A built this index's structure. Workstream C's registration mechanism is now **implemented** (~~not yet independently verified or accepted~~ *(synchronized 2026-09-28, ST-10: independently verified at Gates 1, 2 and 4, Gate 5 PASS WITH CONDITIONS; ~~not yet accepted or committed~~ C-3 addendum, 2026-09-28: **accepted** (`IRA-WP-23-AC §0.2`) and committed with that record; not certified)*; `IMP-REPORT-WP-23`), but **no registering act has been performed** for any of the 21 existing rows or for any future Business Activity, and no `bar_registration` row exists outside test databases.

| Business Activity Identifier | Business Activity Reference | Owning Capability | Owning Work Package | Registration Status | Registering Act | Registration Date | Retroactive |
|---|---|---|---|---|---|---|---|
| *(no entries)* | | | | | | | |

**Column definitions (per `ENTERPRISE-BAR-MECHANISM-DESIGN-AND-IMPLEMENTATION-READINESS.md §4`, reproduced exactly, not redesigned here):**
- **Business Activity Identifier** — the canonical `BA-NNNNNN` value, assigned by BAR at registration (D5). Permanent once assigned; never reused.
- **Business Activity Reference** — an informal, human-readable name/description. `[IMPLEMENTATION DESIGN]`.
- **Owning Capability** — the `C-XXX` this Business Activity belongs to, for traceability to `CAP-001`. `CAP-001` itself is not modified by this field.
- **Owning Work Package** — the `WP-NN` this Business Activity belongs to, linking to (never merging with) `WPR-001`.
- **Registration Status** — exactly two literal values: `Registered` or *(blank/absent, meaning not yet registered)*. ~~This is the **sole authoritative field** a future execution-gate implementation (Workstream E) will consume to determine execution eligibility for a Business Activity not covered by D8's own transitional carve-out.~~ *(Updated 2026-09-25, RD-23-03 Option D.)* This column is the governance-visible record of registration status. The runtime field a future execution gate (Workstream E) consumes is `bar_registration.registration_status`, in the runtime table. **No third status value exists** — this index does not adopt `IMP-001 §6.22.9`'s own six-state lifecycle (Draft/Registered/Active/Suspended/Deprecated/Retired), per D2/D6's own exclusion of that broader scope. Deregistration/retirement remains explicitly out of scope (design document §16), consistent with D2's own decided minimum.
- **Registering Act** — a reference to the discrete, Repository-Owner-authorized act (mirroring an ADR) that performed the registration, analogous to `CBOR-INDEX.md §3`'s own "Registering ADR" column.
- **Registration Date** — governance history, for traceability.
- **Retroactive** — `Yes` if the row entered via D3's own backfill population, `No` if it is a prospectively-registered future Business Activity. Recommended for audit clarity, per the design document's own §4 — not itself a LOCKED requirement.

---

## 4. Registration/Transition State Model (per `ENTERPRISE-BAR-MECHANISM-DESIGN-AND-IMPLEMENTATION-READINESS.md §19a.6`, reproduced exactly)

Five distinct concepts govern a Business Activity's own relationship to this index — they are never conflated:

1. **The Business Activity exists as a governed activity** — evidenced by its own Charter/`IMP-REPORT`/WP, entirely independent of BAR (this is true today, for all 21 existing rows, with zero BAR involvement).
2. **The Business Activity has a BAR-issued canonical identifier** — occurs only at registration (§3, `Business Activity Identifier` column populated), per D5. Never assigned earlier.
3. **The Business Activity is registered in BAR** — occurs at the same act as (2); reflected in the `Registration Status` column.
4. **The Business Activity is execution-eligible under BAR** — for a **future** Business Activity, this is identical to (3) (registered = eligible, per D2/`COM-001-005`). For one of the **21 existing, transitional** rows, eligibility during the D8 transition is **not** derived from this index at all — it continues via its own existing, pre-BAR invocation path, entirely outside this index's own purview, until it individually completes (3).
5. **Ordinary business/caller authorization** — a fully separate, already-existing mechanism (`require_platform_admin` and peers, or `Backend/Runtime/AuthorizationEngine`), never represented in this index.

**Discovery (Workstream D, not implemented here)** will query ~~this index's own `Registration Status` field~~ *(updated 2026-09-25, RD-23-03 Option D)* BAR's runtime registration record (the `bar_registration` table), exclusively, per `IMP-001 §6.22.8`/`RTA-001 §6.6` — never by code inspection or naming convention. **The execution gate (Workstream E, not implemented here)** will consume the same runtime registration state, applying D8's own transitional policy: deny an unregistered *future* Business Activity; permit an unregistered *existing* (D3, pre-cutover) Business Activity to continue via its own current path, unaffected by this index's own absence of an entry for it.

---

## 5. Structural Capacity for the 21-Row Retroactive Population (D3) — Not Populated

Per `ROD-ENTERPRISE-BAR §D3.4` / `ENTERPRISE-BAR-MECHANISM-DESIGN-AND-IMPLEMENTATION-READINESS.md §11`, 21 existing Business Activity rows across `WP-01`–`WP-21` are eventually subject to registration in this index (C-024/`WP-22` BA-01 is not part of this population — §7 below). **This index's own §3 table structure is directly capable of holding all 21 entries** — one row per Business Activity, using exactly the columns already defined (§3) — once each row's own registering act (~~Workstream C, not yet built~~ *(updated 2026-09-25: Workstream C implemented, ~~not yet independently verified or accepted~~ (synchronized 2026-09-28, ST-10: independently verified at Gates 1, 2 and 4, Gate 5 PASS WITH CONDITIONS; ~~not yet accepted or committed~~ C-3 addendum, 2026-09-28: accepted and committed; not certified))*) occurs, per each Business Activity's own independent cutover (D9). **No row for any of the 21 is added by this task.** 14 of the 21 have no unresolved data and could proceed ~~immediately once Workstream C exists~~ *(updated 2026-09-25: once the Workstream C mechanism is independently verified and accepted, and each row's own registering act is separately authorized)*; 7 require the data confirmation the design document's own §11/§21 already flagged (multi-BA mapping, BLOCKED-BA treatment, infra-BA treatment) — none of these is resolved by this index's own creation.

---

## 6. Illustrative Example (Not a Registration)

The row below shows the Register's own intended shape once populated. It uses `BA-000089` — the same illustrative identifier already cited, as an example only, in `SD-002-004`, `CMD-001 §26.4a`, and `IMP-001 §6.22.1b` — precisely so this index does not invent a new placeholder token where the constitutional text already supplies one. **This is not a real registration. `BA-000089` is not assigned to any actual Business Activity by this row, and this example does not appear in §3's own Register.**

| Business Activity Identifier | Business Activity Reference | Owning Capability | Owning Work Package | Registration Status | Registering Act | Registration Date | Retroactive |
|---|---|---|---|---|---|---|---|
| `BA-000089` *(illustrative only)* | Example Business Activity | C-000 *(illustrative)* | WP-00 *(illustrative)* | Registered | ADR-000 *(illustrative)* | 0000-00-00 *(illustrative)* | Yes/No *(illustrative)* |

---

## 7. Relationship to C-024

C-024 BA-01 (Establish Billing Arrangement, `WP-22`) is **not registered** in this index. Per `ROD-C024-BAR_Treatment_Decision_Preparation.md §0` (D10, Option A, scoped to C-024 BA-01 only): BAR treatment for BA-01 remains **deferred** — not registered, no identifier assigned, no enterprise exemption created. `D10` is unaffected, unaltered, and not reinterpreted by this index's own creation. `BIA-000001` (the Billing Arrangement **Business Object**, `CBOR-INDEX.md §3`) remains completely separate from, and is never cross-populated with, any future Business Activity Identifier BA-01 might eventually receive. **This index does not add BA-01 as registered, does not assign it an identifier, and does not modify `D10` or the `WP-22` Charter.** It is simply structurally capable of registering BA-01 later, exactly like any other Business Activity, when its own future, separately-authorized registering act occurs.

---

## 8. Amendment Procedure

Add a new row to §3 when, and only when, a Business Activity's own registering act (mirroring the CBOR-ADR pattern) is actually performed, assigning it a `BA-NNNNNN` identifier and a `Registered` status. Do not add speculative, pending, or illustrative entries to §3 (the illustrative example, §6, is deliberately kept outside the Register itself). Do not remove an entry once registered — this index's own registration record is a governance record, not an implementation-status field, mirroring `CBOR-INDEX.md §4`'s own identical rule. Collision-check every new identifier against this index's own existing entries and against the CBOR namespace (`CBOR-INDEX.md §3`) before registering, mirroring `ADR-041`'s own "Identifier collision-checked against `CBOR-INDEX.md` and repository-wide" practice.

---

~~*Workstream A (BAR Registration Index) status: **IMPLEMENTED — READY FOR INDEPENDENT VERIFICATION.** This index's own structure is complete per the approved design (`ENTERPRISE-BAR-MECHANISM-DESIGN-AND-IMPLEMENTATION-READINESS.md §6`); it contains zero actual registrations. Workstreams B (identifier issuance), C (registration mechanism), D (discovery), E (execution gate), F (21-BA retroactive registration/cutover), G (verification/testing), and H (C-024 integration readiness) remain not implemented — this document does not claim, imply, or perform any of them. No Business Activity is registered. No Business Activity Identifier is assigned. `WPR-001` and `CBOR-INDEX.md` are unmodified. `C-024 D10` is unaffected. Nothing staged, committed, or pushed.*~~

*(Status corrected 2026-09-25; the original line above is preserved, struck through. It became stale on 2026-09-22, when Workstreams B and C were implemented after it was written.)*

***WP-23 status: OPEN.*** *Workstreams A–C form a separately closable tranche (RD-23-02, `IRA-WP-23-AC_BAR_Workstreams_A-C_Closure_Readiness.md §0`).*

| Workstream | Status |
|---|---|
| **A** — this index | **IMPLEMENTED** |
| **B** — identifier issuance (`bar_identifier_ledger`, `BarIdentifierService`) | **IMPLEMENTED** |
| **C** — registration mechanism (`bar_registration`, `BarRegistrationService`) | **IMPLEMENTED** |
| **D** — discovery | Not implemented |
| **E** — execution gate | Not implemented |
| **F** — 21-BA retroactive registration/cutover | Not implemented |
| **G** — five-gate verification of the whole Work Package | Not implemented |
| **H** — C-024 integration readiness | Not implemented |

- ~~**A–C are uncommitted, not independently verified, not accepted and not certified.**~~ *(Synchronized 2026-09-28, ST-10.)* **A–C are independently verified** (Gates 1, 2 and 4; Gate 5 PASS WITH CONDITIONS) ~~**but uncommitted, not accepted and not certified.**~~ *(C-3 addendum, 2026-09-28.)* **and ACCEPTED** (`IRA-WP-23-AC §0.2`), committed together with that record; **not certified, not closed.** WP-23 remains OPEN. Workstreams D–H are not implemented. This index still holds zero registrations. See `IMP-REPORT-WP-23_Enterprise_BAR_Mechanism.md`.
- ~~**The authority relationship between this index, the registering act and the `bar_registration` table is OPEN** (RD-23-03, `ROD-WP-23-AC-BAR-Registry-Authority-Decision-Preparation.md`). §1's authority wording is unchanged pending that decision.~~ *(Updated 2026-09-25.)* The authority relationship between this index, the registering act and the `bar_registration` table is **decided: RD-23-03, Option D (layered)**. §1 is updated accordingly.
- **Registrations:** this index contains zero. No Business Activity is registered, and no Business Activity Identifier is assigned or issued outside test databases.
- **Unchanged:** `WPR-001`, `CBOR-INDEX.md` and `C-024 D10` are not changed by this correction.
- Nothing was staged, committed or pushed.
