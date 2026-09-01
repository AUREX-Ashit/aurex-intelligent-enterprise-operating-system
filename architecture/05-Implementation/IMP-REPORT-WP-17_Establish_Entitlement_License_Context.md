# IMP-REPORT-WP-17 — Establish Entitlement/License Context (Administrative) (C-023, BA-01)

**Work Package:** WP-17
**Capability:** C-023 — Licensing & Entitlement (`CAP-001` line 77, Domain D-002 "Commercial & Subscription", Primary Specification `URA-001`, Active — unchanged; **C-023 capability-wide status remains 🔴 RED — Not Implementation Ready**, `IRA-C023 §16`)
**Business Activity:** BA-01 — Establish Entitlement/License Context (Administrative)
**Governing charter:** `WP-17_C023_BA-01_Establish_Entitlement_License_Context_Business_Activity_Charter.md`
**Governing Technical Design:** `TDS-C023_Licensing_and_Entitlement_Minimum_BA.md` (accepted; twice independently reviewed — accuracy: no material error, `§27`; chartering sufficiency: **TDS SUFFICIENT FOR BA CHARTERING**, `§28`)
**Governing IRA:** `IRA-C023_Licensing_and_Entitlement_Implementation_Readiness_Assessment.md` (Accepted 2026-08-27; classification 🔴 RED — Not Implementation Ready, unchanged; six Repository Owner Decisions resolved — `§18.13`/`§19.13`/`§20.12`/`§21.12`/`§22.13`/`§23.13`)
**Governing service-hosting decision:** `ADR-036` — Licensing & Entitlement (C-023) Persistence Implementation Ownership (Status: **Accepted**; `AuthService` is the C-023 implementation / service host for the current modular-monolith phase; does **not** transfer C-023 business-capability ownership)
**Consumed infrastructure (certified, not modified by this Work Package):** WP-18 — Bind and Resolve Approval Authority (C-003), governed by `TDS-018`, **CLOSED — CERTIFIED — RELEASE-READY** through all five `CLAUDE.md §19.7b` gates (`CERT-WP-18`, `VV-AUDIT-WP-18`, `RRA-WP-18`, Repository Owner Closure Decision `IMP-REPORT-WP-18 §7`). Provides `require_approval_authority()` / `enforce_approval_authority()` / `resolve_approval_authority()` and the `membership_approval_authority` binding.

---

## 1. Repository Owner Implementation Authorization (Recorded Verbatim)

The Repository Owner explicitly granted Implementation Authorization for WP-17 / BA-01 on **2026-09-01**, following the final readiness check and its independent review (no material defect; no unresolved Category-B implementation blocker). The authorization is reproduced exactly as issued, with no wording, date, or scope added or altered:

> **A — I, as Repository Owner, explicitly grant Implementation Authorization for WP-17 / BA-01 now.**
>
> Record the authorization exactly within the scope, boundaries, and exclusions established in the immediately preceding readiness assessment.
>
> **Authorized scope:**
> - WP-17 / BA-01: "Establish Entitlement/License Context (Administrative)"
> - AuthService hosting per accepted ADR-036
> - Required persistence/model/migration/repository/service/router/schema work
> - Approval Authority enforcement using the certified WP-18 infrastructure
> - Decision 6 read-only reference to membership.license_type; never write or duplicate it
> - Exactly the two authorized frontend items
> - Existing audit/observability infrastructure
> - Fail-closed security and tenant-isolation requirements
> - Required testing, including CLAUDE.md §21.4 tenant-isolation checklist
> - Full certification/closure sequence under CLAUDE.md §19.7b
>
> **Explicit exclusions:**
> - Broader C-023 implementation
> - Consumption / Allocation
> - Entitlement Catalog administration
> - Subscription semantics
> - Billing
> - C-020 / C-025 source hand-off
> - Migration / offboarding
> - Cross-tenant sharing
> - Authorization Engine Option-A / M2–M6 redesign
> - AuthorityHolder replacement
> - Group infrastructure
> - Any Decision 3 or Decision 4 implementation
> - Any new service boundary
> - Any schema decision not supported by canonical sources
>
> **Important:**
> 1. This authorization applies ONLY to WP-17 / BA-01.
> 2. C-023 capability-wide status remains RED.
> 3. WP-17 is authorized but is NOT thereby implemented or certified.
> 4. Do NOT begin implementation in this task.
> 5. Do NOT modify implementation files.
> 6. Record my authorization as a formal governance artifact using the repository's established authorization/change-control convention.
> 7. Preserve the exact authorization scope and exclusions above.
> 8. Do not reopen or alter Decisions 1–6.
> 9. Do not silently resolve the documented schema-shape question. If implementation later requires a governance/design decision, use the mandated STOP-and-report mechanism.
> 10. Do not silently resolve any frontend DS-001 / Workspace / Navigation gap; use the mandated STOP-and-report mechanism if encountered.

This authorization was preceded by an independent, fresh-context readiness review (no material defect; ADR-036 confirmed Accepted and genuinely resolving `WP-17 §8`; WP-18 confirmed satisfying Decision 1's runtime-enforcement dependency without reinterpreting Decision 1; no Category-B blocker; no fired Decision 3/4 trigger; no silent scope expansion), and by the independently-verified R7 governance-documentation reconciliation (commit `0a07cd9`).

## 2. Authorized Scope (as recorded — the binding scope of this authorization)

Implementation SHALL be confined to WP-17 / BA-01 "Establish Entitlement/License Context (Administrative)" exactly as chartered (`WP-17` charter) and designed (`TDS-C023`), lifecycle `(none) → ACTIVE` establish/continuing outcome only (`WP-17 §9`; `TDS-C023 §4`). It includes:

1. **Persistence hosted in `AuthService`**, per `ADR-036` (modular-monolith phase) — the C-023 Licensing/Entitlement governance-layer registry (working name `entitlement_license_registry`, `TDS-C023 §6.3`), its repository, service, and any router/schema. **Persistence references `membership` and `organization` by their `AuthService`-owned primary keys, intra-service — no cross-service foreign key (`CLAUDE.md §8`).**
2. **Model, migration, repository, service, router, schema** for the above.
3. **Approval Authority enforcement via the certified WP-18 infrastructure** — `require_approval_authority("Entitlement/License Commit Authority")` / `enforce_approval_authority()` / `resolve_approval_authority()` (fail-closed, `ANY_ONE`-only, no `PLATFORM_ADMIN`/`AUREX_ADMIN` bypass), establishing the C-023 `approval_authorities` instance (`scope_type = 'COMPANY'`, `approval_strategy = 'ANY_ONE'`, one per participating Organization, `authority_name = "Entitlement/License Commit Authority"`, `TDS-C023 §7.1`–`§7.6`) via the already-certified `ApprovalAuthorityService.establish()` (`WP-02` BA-03), and its currently-effective `membership_approval_authority` binding row(s) via the already-certified `MembershipApprovalAuthorityService.bind()` (`WP-18`). **Ordinary use of the now-certified mechanisms — not new architecture.**
4. **Decision 6 read-only reference to `membership.license_type`** — referenced by value at establish/resolve time only; **never written, duplicated, migrated, deprecated, or redefined**; no `ALTER` to `memberships` (`IRA-C023 §18.13`; `TDS-C023 §6.1`/`§6.3` item 11; `WP-17 §7`).
5. **Exactly the two authorized frontend items** — (1) Establish License/Entitlement; (2) display the resulting establishment/status outcome (`IRA-C023 §23.13` Decision 5; `WP-17 §21`; `TDS-C023 §17`). **Nothing beyond** — no administration console, Consumption/Allocation/Catalog/Billing/Subscription UI.
6. **Audit / observability via the existing `observability.py` infrastructure** (`record_audit` / `publish_event` / `AuditStatus`) — every bind, every resolve outcome (`AUTHORIZED` and every denial reason), every establish; no new audit subsystem; no raw JWT / secrets / authorization headers persisted (`TDS-C023 §16`).
7. **Fail-closed security and tenant isolation** — every authorization branch denies by default; Organization isolation enforced independently at bind time (service-layer cross-Organization rejection) and at resolution time (resolver Organization-match against an `X-Tenant-ID`-derived target independent of the caller's own claims) (`TDS-C023 §22`).
8. **Testing** — `CLAUDE.md §21.4` Mandatory Tenant-Isolation Test Checklist (two distinct unrelated Organizations with no shared row; cross-Organization visibility probe; explicit foreign-identifier-acceptance probe) **plus** `TDS-C023 §21` V&V expectations (a negative control proving the runtime-enforcement contract denies by default; a concurrent-establish race test mirroring `MembershipService.establish()`'s existing coverage).
9. **Full certification / closure** under the `CLAUDE.md §19.7b` five-gate sequence (Gate 1 Independent Certification → Gate 2 V&V Audit → Gates 3–4 if remediation is required → Gate 5 Release Readiness Audit) plus the `CLAUDE.md §21.3`/`§20` Enterprise-Experience and demonstrability requirements.

## 3. Explicit Exclusions (as recorded — NOT authorized by this grant)

- Broader C-023 implementation of any kind beyond BA-01's chartered minimum scope.
- License **Consumption** and **Allocation** (`URA-001-116`) — implementation, schema, or authority assignment (`IRA-C023 §22.13` Decision 4, deferred, **not reopened, not implemented**).
- Global **Entitlement Type / Feature Catalog** administration — creation, modification, or governance of global Entitlement Types, or any authority assignment for it (`IRA-C023 §21.12` Decision 3, deferred, **not reopened, not implemented**).
- **Subscription** semantics — duration alignment, renewal, termination, expiry-on-subscription-event (`TDS-C023 §10.2`, remains Pending Canonical Binding; `WP-17 §23`). `effective_from`/`effective_to` are independent Commit-time business dates only.
- **Billing** linkage or workflows.
- **C-020 / C-025** source hand-off consumption (`EX-C023-02`) — no `C-020` WP, no `C-025` WP, no source-hand-off interface (`IRA-C023 §20.12` Decision 2).
- **Migration / offboarding**, **cross-tenant sharing**, Technical Provisioning.
- Any **Authorization Engine Option-A / M2–M6** redesign — the WP-18 Option B (direct FastAPI-dependency) integration is what is consumed; no `ApprovalAuthorityResolver` (Runtime Engine tier resolver) work is authorized.
- **`AuthorityHolder` replacement** or modification — its `CheckConstraint IN ('AI-001', 'AI-002')` is untouched.
- **Group infrastructure** (`group_registry` / `group_membership` / any `group_approval_authority`-shaped binding).
- Any **Decision 3 or Decision 4 implementation**.
- Any **new service boundary** — no `CommercialService` / `LicensingService` / `SubscriptionService` / `BillingService`; `CLAUDE.md §18` architectural-change control is not invoked or relaxed by this grant.
- Any **schema decision not supported by current canonical sources** — see §4.
- Suspend / revoke / reactivate outcomes of `ERB-C023-05` (`EX-C023-12`/`-13`) — establish (continuing) outcome only.

## 4. Implementation-Time STOP-and-Report Obligations (mandated, not pre-resolved by this authorization)

1. **Schema shape.** `Master_Technical_Architecture.md` defines two separate canonical tables — `license_registry` (per-Membership: `license_id`, `membership_id`, `license_type`) and `entitlement_registry` (per-Organization: `entitlement_id`, `organization_id`, `entitlement_code`, `effective_from`, `effective_to`). `TDS-C023 §6.3` sketches a single working-name `entitlement_license_registry` with a richer shape (a `status` lifecycle column, effective dates on the license side, an Entitlement Source Reference, the four `URA-001-115` specialized license types). **This authorization does NOT decide one-table-vs-two, the exact column set, constraints, or indexes.** The implementing session SHALL author an implementation-time Technical Design for the schema and SHALL perform a `CLAUDE.md §18` / `§19.4` **STOP-and-report** before running any migration, exactly as `TDS-016` did for `tenant_registry` (`ADR-036` Consequences; `TDS-C023 §6.3` item 12, `§23`). Any schema shape not directly supported by a canonical source requires an explicit Repository Owner decision obtained through that STOP-and-report — it SHALL NOT be assumed.
2. **Frontend DS-001 / Workspace / Navigation.** `TDS-C023 §17.1` discloses that no canonical Workspace assignment exists for C-023 and Workspace/Navigation placement is not designed. If, during implementation, `DS-001` does not define a component, token, pattern, Workspace, or Navigation placement the two authorized frontend items require, the implementing session SHALL perform a `CLAUDE.md §19.1` / `§20.5` **STOP-and-report** and obtain clarification — it SHALL NOT invent one.

## 5. Disclosed Implementation-Time Consideration (recorded, not a blocker)

Per `IRA-C023 §21.6` / `TDS-C023 §19` / `WP-17 §5`: BA-01 only ever **references an already-recognized Entitlement Type** (it never creates one — Decision 3's trigger is not fired). Consequently the **License half** of the BA (Membership-anchored, `URA-001-111`/`-115` fixed enum) is fully exercisable, while the **Entitlement half** is *vacuously blocked* end-to-end wherever no Entitlement Type is yet recognized/catalogued anywhere. The implementing session SHALL deliver and demonstrate the License path fully, and SHALL deliver the Entitlement path with the "already-recognized type" precondition **without** implementing catalog-governance semantics; if demonstrating the Entitlement establishment path end-to-end (`CLAUDE.md §20.4`) turns out to require the deferred catalog-governance mechanism, the implementing session SHALL STOP-and-report rather than build it.

## 6. Implementation Status

**IMPLEMENTATION NOT STARTED.** No production code, schema, migration, router, service, repository, model, test, or frontend component has been created or modified for C-023 / WP-17 in the pass that recorded this authorization. `git grep` for `entitlement_license_registry` / `license_registry` / `entitlement_registry` in `Backend/` at the recording commit returns zero implementing hits.

## 7. Explicit Confirmations

- **This authorization applies ONLY to WP-17 / BA-01.** No broader C-023 implementation is authorized or implied.
- **C-023 capability-wide status remains 🔴 RED — Not Implementation Ready** (`IRA-C023 §16`, unchanged). This authorization is a WP-17/BA-01-scoped decision; it is **not** a capability-wide readiness change and is **not** a change to GREEN, YELLOW, or any other classification.
- **WP-17 is authorized but is NOT thereby implemented or certified.** No `CLAUDE.md §19.7b` gate has been dispatched or passed. Certification and closure remain subject to the full five-gate sequence.
- **IRA-C023 Decisions 1–6 are not reopened, altered, or reinterpreted** by this authorization.
- **The schema-shape question is not resolved** by this authorization — it is bound to the §4(1) STOP-and-report obligation.
- **`ADR-036` is unchanged** (Status: Accepted) — this authorization consumes it, it does not modify it.
- **`TDS-018` and the certified WP-18 are unchanged** — this authorization consumes WP-18's delivered infrastructure as a dependency.
- **No new service boundary** is created or implied — implementation is in `AuthService`, per `ADR-036`.
- Nothing was staged, committed, or pushed by the pass that created this artifact beyond the governance-artifact files enumerated in §8.

## 8. Change Control

**File created:** this document — `architecture/05-Implementation/IMP-REPORT-WP-17_Establish_Entitlement_License_Context.md` — recording the Repository Owner Implementation Authorization for WP-17 / BA-01 (2026-09-01, verbatim, §1) and the binding authorized scope (§2), explicit exclusions (§3), and mandated implementation-time STOP-and-report obligations (§4).

**Files modified (authorization-recording change-control, strikethrough-preserve — mirroring the `IMP-REPORT-WP-18` authorization-recording convention):**
- `WP-17_C023_BA-01_Establish_Entitlement_License_Context_Business_Activity_Charter.md` — Status line and "Final state" line updated from "IMPLEMENTATION NOT YET AUTHORIZED" to "IMPLEMENTATION AUTHORIZED (2026-09-01, per this report §1)"; a Change Control entry appended. The charter's scope (§19), exclusions, Decisions summary (§22), and every other section are unchanged.
- `IRA-C023_Licensing_and_Entitlement_Implementation_Readiness_Assessment.md` — the §16 R7-addendum clause "WP-17 remains CHARTERED / NOT AUTHORIZED …" and the preceding note's "No implementation authorization is granted or implied. WP-17 is not authorized …" reconciled (strikethrough-preserve) to record that WP-17/BA-01 implementation is now authorized per this report §1. **The 🔴 RED capability-wide classification, the §13 gate assessments, and Decisions 1–6 are explicitly unchanged.**
- `WPR-001_Work_Package_Roadmap.md` — the WP-17 row status updated from "CHARTERED — NOT AUTHORIZED …" to "CHARTERED — IMPLEMENTATION AUTHORIZED (2026-09-01), NOT YET COMPLETE, NOT CERTIFIED" (strikethrough-preserve); a maintenance note appended. No other row altered.

**Not modified:** any `Backend/` file, migration, test, model, service, router, or schema; `ADR-036`; `TDS-018`; any WP-18 certification artifact; `TDS-C023`'s design sections; `CAP-001`; `URA-001`; `PE-001-C023`; `Master_Technical_Architecture.md`; any C-040 / WP-16 artifact; any unrelated `WPR-001` row; any of IRA-C023 Decisions §18.13 / §19.13 / §20.12 / §21.12 / §22.13 / §23.13.

---

*End of authorization record. No application code, schema, migration, ADR, `TDS-018`, `ADR-036`, or WP-18 certification artifact was created or modified in recording this authorization. Implementation has NOT started. Nothing was pushed.*
