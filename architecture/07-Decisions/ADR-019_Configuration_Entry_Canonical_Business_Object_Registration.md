# ADR-019 — Configuration Entry Registered as a Canonical Business Object (WP-10, C-041)

**Status:** Accepted
**Classification:** Architecture Governance / Business Object Registration
**Decided by:** Repository owner (architecture governance authority), during WP-10's own implementation-time `CMD-001 §26.3a` eligibility analysis (`IRA-010 §6`) — the same decision-authority pattern `ADR-006`/`ADR-008`/`ADR-009`/`ADR-011`/`ADR-012`/`ADR-013` (WP-04) and `ADR-015` (WP-05) already established.
**Affected Documents:** `architecture/05-Implementation/IRA-010_WP-10_Configuration_Management_Implementation_Readiness_Assessment.md` (§6 records the full registration entry this ADR authorizes); `architecture/00-Governance/CBOR-INDEX.md` (§3 register row added). **CMD-001 is not amended. ADR-006 through ADR-018 are not amended or revisited.**

---

## Context

`IRA-010 §6` disclosed, at charter/readiness stage, that a new Configuration record construct was anticipated and that full `CMD-001 §26.3a` eligibility analysis was deferred to implementation time because it requires the exact schema shape, not yet designed at IRA stage — mirroring the same disclosed-not-skipped pattern `IRA-005` used for `AEO-000001` before WP-05 began.

`CMD-001 §12.8` ("Configuration as Business Objects") already states directly that "Configuration itself shall be modeled as Business Objects," independent of the general-purpose §26.3a test. Applying §26.3a at implementation time (`IRA-010 §6`) confirms this holds for WP-10's own candidate:

- **Step 1 (Independent Identity):** satisfied — a Configuration record has identity separable from the request that produced it, written by one BA-02 call and later read by identity in unrelated requests.
- **Step 2 (Cross-Experience Reference Test):** satisfied — BA-01 (Resolve Enterprise Configuration), a Business Activity distinct from and separately invoked from BA-02 (Establish/Update Enterprise Configuration), retrieves records BA-02 produced, by identity; every already-certified WP-01–WP-09 screen consuming resolved Terminology/Theme/Localization is a further independent instance of the same pattern.
- **Step 3 (Governed Lifecycle):** satisfied — `CMD-001 §12.5` mandates Versioning, Effective Dating, Lifecycle State, and Audit Trail as non-optional characteristics; a new version supersedes the prior one at its own effective date, not a transient value.

`IRA-010 §6` further determined the correct registration **shape**: the five in-scope facets (Terminology, Branding-core, Theme-core, Accessibility Profiles, Localization-narrow — `IRA-010 §4.8`) share identical identity structure (Scope + Category + Key), identical `§12.5` lifecycle/versioning/audit mechanics, and identical `§12.6`/`§12.7` resolution algorithm, differing only in `§12.3` Category and payload shape. This is one canonical Business Object family with a Category discriminant, not five separate registrations — the same "several apparent candidates resolve to one real identity" outcome `ADR-015` reached for `AEO-000001`'s own six named constructs.

**Eligibility is not re-derived here** beyond what is stated above — `IRA-010 §6` performs the full step-by-step analysis and records the complete `§26.4` registration entry; this ADR adopts its result rather than duplicating it.

---

## Decision

1. **Register "Configuration Entry" as a canonical Business Object**, identifier `CFG-000001`, per SD-002 §2, CMD-001 §26.3/§26.3a/§26.4. The full registration entry is recorded in **IRA-010 §6**, which this ADR adopts by reference rather than duplicating here.
2. **One registration, not five.** Terminology, Branding (core), Theme (core), Accessibility Profile, and Localization (Default Language) are Categories/Keys of the single `CFG-000001` family, not separate Business Objects — per `IRA-010 §6`'s own registration-shape analysis.
3. **`CBOR-INDEX.md` §3 is amended** to add `CFG-000001`, per its own Amendment Procedure (§4): "Add a new row when... a candidate concept passes CMD-001 §26.3a's Canonical Business Object Eligibility Test and is registered via its own ADR." This ADR performs that registration.
4. **This ADR does not authorize any Business Activity's implementation beyond what `IRA-010`'s own Readiness Decision (§8) already authorizes.** `CMD-001 §26.7` (Physical Implementation Mapping) is set by WP-10's own backend implementation (model, migration, repository), which proceeds under this registration, not independently of it.
5. **This ADR does not create a pattern-level ADR** (an `ADR-010` equivalent). A single Business Object family with a Category discriminant is the ordinary `CMD-001 §26.4` registration shape, not a multi-object lifecycle chain requiring separate pattern recognition.
6. **Incidental correction, not a new decision:** `CBOR-INDEX.md` §3 was found, during this amendment, to be missing the `AEO-000001` row `ADR-015` (WP-05) registered — `ADR-015` itself states "no other document changes as a result of this ADR," meaning the Index's own Amendment Procedure was not separately executed at WP-05 closure. This ADR adds the missing `AEO-000001` row alongside the new `CFG-000001` row as a data-integrity correction to the Index (Golden Rule 10 — "leave the repository in a better state"), not as a re-opening of `ADR-015`'s own decision, which is unchanged.

## Rationale

This decision applies `CMD-001 §26.3`'s registration mechanism, via the `§26.3a` eligibility test (`ADR-014`), to WP-10's own candidate — and is reinforced, unusually directly, by `CMD-001 §12.8` itself already stating in plain text that Configuration is modeled as Business Objects. The test's main analytical work here is not deciding *whether* to register (§12.8 already answers that) but deciding the registration's correct *shape* — one family across five facets, not five families — which follows directly from `IRA-010 §5`'s own prior two-Business-Activity (not five-facet) BA split reasoning, grounded in `SD-002-077`'s metadata-driven object pattern.

Registering `CFG-000001` now, ahead of migration/model implementation, mirrors both `RSC-000001` (WP-04) and `AEO-000001` (WP-05): registration precedes and grounds implementation, never the reverse.

## Consequences

- WP-10's own Business Object eligibility question (`IRA-010 §6`) is resolved: one registered (`CFG-000001`), covering all five in-scope facets.
- `IRA-010 §6` records the full registration entry; `CBOR-INDEX.md` §3 gains one new row for `CFG-000001` and one corrective row for the previously-unindexed `AEO-000001`.
- `CMD-001` itself is not amended, consistent with its LOCKED status; this registration exercises `CMD-001 §26.3`'s own existing mechanism.
- WP-10's backend implementation (model, migration, repository, services, API) proceeds under this registration.

## Status

**Accepted**
