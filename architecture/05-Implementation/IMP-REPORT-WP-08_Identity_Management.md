# IMP-REPORT-WP-08 — Identity Management (C-001)

**Work Package:** WP-08 — Identity Management (C-001)
**Governing Readiness Assessment:** `IRA-008_WP-08_Identity_Management_Implementation_Readiness_Assessment.md` (Accepted — READY, scoped: 3 Business Activities realizing `EX-C001-06`/`07`/`08`; `EX-C001-01`/`02` excluded — `TD-102`; `EX-C001-03`/`04`/`05` satisfied by construction — no new work).
**Governing Business Object:** None newly registered. `Identity`/`Person` (pre-governance, `34cf7fe`) reused unchanged. One new audit-trail table (`IdentityRecoveryRequest`) fails `CMD-001 §26.3a`'s eligibility test — not a registered canonical Business Object (`IRA-008 §6`).
**Governing Capability Specification:** `PE-001-C001_Identity_Management.docx` v1.1 (`CRB-C001`; `ERB-C001-01` through `04`; `EX-C001-01` through `08`).
**Scope of this report:** BA-01 through BA-03, backend and frontend (`CLAUDE.md §20` — this is the first Work Package chartered under the Enterprise Experience Standard).

---

## BA-01 — Detect and Resolve Disrupted Identity Context (`EX-C001-06`)

### Business Activity Contract (`IMP-001 §6.7`)

- **Business Intent:** Re-confirm a currently-held Identity Context against `C-006`'s Authoritative Person Context rather than trusting the last-known JWT claim state (`Contract 5.6`).
- **Disposition:** New. Read-only re-confirmation, no persistence — mirrors `OrganizationService.get_details()`'s/`PersonUnderstandingService.understand()`'s own established precedent (`WP-01`/`WP-07`).
- **Input Contract:** none (acts on the caller's own current Identity, from JWT claims).
- **Output Contract:** `IdentityStatusResponse` (`identity_id`, `person_id`, `status`: `CURRENT`/`UNRESOLVED`, `checked_at`).
- **Business Rules:** `CURRENT` only if the associated `Person.is_active`; `UNRESOLVED` otherwise (missing or deactivated Person). `RTA-001`'s own runtime signal not consulted — conditional (`"where relevant"`) per `EX-C001-06`'s own Context Required, and not production ready.
- **Authorization Rules:** Authenticated only (`get_current_claims`) — a self-referential check, not an administrative action.
- **Audit Requirements:** None — read-only.
- **Tests:** `test_refresh_status_current_for_active_person`, `test_refresh_status_unresolved_for_deactivated_person`, `test_refresh_status_raises_404_for_unknown_identity` (service); `test_refresh_status_returns_current`, `test_refresh_status_returns_unresolved_for_deactivated_person`, `test_refresh_status_requires_authentication`, `test_refresh_status_does_not_require_tenant_header` (API).

## BA-02 — Recover Inaccessible Identity Context, self-service (`EX-C001-07`)

### Business Activity Contract

- **Business Intent:** Route a Person toward a governed re-establishment path (new Identity or re-resolution of an existing one) when their established Identity has become unusable — never performing the technical credential-recovery mechanism itself.
- **Disposition:** New. Scoped to self-service only (`IRA-008 §4.5`) — administrator-initiated recovery excluded, `TD-100`.
- **Input Contract:** `RecoverIdentityRequest` (`person_id`, `reason`).
- **Output Contract:** `IdentityRecoveryRequestResponse` (`id`, `person_id`, `routed_path`: `NEW_IDENTITY`/`RE_RESOLUTION`, `status`: `PENDING`, `created_at`).
- **Business Rules:** `person_id` in the request body must equal the caller's own JWT `person_id` claim (403 on mismatch). Routing determined by whether the Person holds any existing `Identity` record. Never creates an `Identity`; never performs establishment (`ERB-C001-01` excluded, `TD-102`).
- **Authorization Rules:** Authenticated only, plus the self-service `person_id` match check above.
- **Audit Requirements:** `record_audit("RECOVER_IDENTITY", ...)` on success and on denial; `publish_event("IDENTITY_RECOVERY_REQUESTED", ...)` on success.
- **Tests:** `test_request_recovery_routes_to_re_resolution_when_identity_exists`, `test_request_recovery_routes_to_new_identity_when_no_identity_exists`, `test_request_recovery_raises_404_for_unknown_person`, `test_request_recovery_raises_404_for_deactivated_person` (service); `test_recover_identity_succeeds_for_own_person`, `test_recover_identity_rejects_person_id_mismatch`, `test_recover_identity_rejects_unknown_person`, `test_recover_identity_rejects_empty_reason`, `test_recover_identity_requires_authentication` (API).

## BA-03 — Classify Identity Hand-off Rejection (`EX-C001-08`)

### Business Activity Contract

- **Business Intent:** Classify a dependent capability's Identity Context hand-off rejection as capability-scoped insufficiency (Identity Context preserved) or an integrity signal (routed for re-resolution) — never trusting the reporting capability's own stated reason as the classification basis.
- **Disposition:** New. Classification-only, no persistence. **Design corrected during IRA drafting** to mirror the closer, more authoritative precedent found on further discovery — `WP-02` BA-10's `AuthorizationPolicyConflictService.classify_handoff_rejection()` (committed `ffaaec6`) — rather than the more generic static-routing-table pattern `IRA-007` BA-05 used. Classification is computed entirely by re-invoking BA-01's own `IdentityStatusService.refresh()` against the Identity Context's own independently-verifiable current state.
- **Input Contract:** `ClassifyHandoffRejectionRequest` (`identity_id`, `rejecting_capability`, `stated_reason`).
- **Output Contract:** `HandoffRejectionOutcome` (`classification`, `identity_context_preserved`, `routed_to`, `explanation`, `checked_at`).
- **Business Rules:** `stated_reason` recorded for audit traceability only, never used to determine `classification` (`Contract 5.7`) — verified directly by `test_classify_never_uses_stated_reason_as_basis`.
- **Authorization Rules:** Authenticated only.
- **Audit Requirements:** `record_audit("CLASSIFY_IDENTITY_HANDOFF_REJECTION", ...)`.
- **Tests:** `test_classify_capability_scoped_when_identity_current`, `test_classify_integrity_signal_when_identity_unresolved`, `test_classify_never_uses_stated_reason_as_basis` (service); `test_classify_handoff_rejection_capability_scoped`, `test_classify_handoff_rejection_integrity_signal`, `test_classify_handoff_rejection_unknown_identity`, `test_classify_handoff_rejection_requires_authentication` (API). No caller exists yet anywhere in this repository — disclosed, `TD-101`.

## `EX-C001-01`/`02` — Excluded (No BA)

`ERB-C001-01` (Establish New Identity Context) requires an unconditional Access Evaluation Outcome (`Contract 5.3`), structurally unobtainable per `IRA-005 §12`'s own disclosed root cause. Excluded from this Work Package's scope, disclosed at chartering time and confirmed by `IRA-008 §4.1`. Tracked as `TD-102`.

## `EX-C001-03`/`04`/`05` — Satisfied by Construction (No Dedicated BA)

`POST /auth/login` (unmodified) realizes `EX-C001-03`/`04`'s own deterministic resolution and Authoritative Identity Context production; `POST /auth/refresh` (unmodified) realizes `EX-C001-05`'s own continuity property. See `IRA-008 §4.2`/`§4.3` for the full disclosed reasoning — neither EX produces a distinct resource of its own for a dedicated endpoint to expose, mirroring `IRA-007 §7.1`/`§7.2`'s own precedent for `EX-C006-09`/`12`.

---

## Frontend / Enterprise Experience (`CLAUDE.md §20`, Plan B — `IRA-008 §7`)

This is the first Work Package delivering a frontend under the Enterprise Experience Standard.

- **Extended, not created:** `source/frontend/src/features/identity-access/components/IdentityAccessScreen.tsx` (existing screen, existing `identity-access` navigation slot in `admin-navigation.ts`) — the "Identity Management" `UnsupportedCapabilityNotice` block is replaced with real `IdentityStatusSection`/`IdentityRecoverySection` components; retitled and retained (accurately) for the still-unbuilt raw Identity-record view/list gap.
- **New:** `src/features/identity/state/useIdentityManagement.ts` (state-machine hook, mirrors `usePersonManagement.ts`), `src/features/identity/components/{IdentityStatusSection,IdentityRecoverySection}.tsx`, `src/services/identity-api.ts`, `src/types/identity.ts`.
- **Reused, not invented:** `Card`/`Button`/`Input`/`Form`/`Spinner`/`StatusBadge` (existing DS-001-aligned component library); `useAuth()`/`useNotifications()`/`apiClient` (existing infrastructure).
- **States implemented (`CLAUDE.md §20.6`):** loading (`Spinner` during in-flight requests), empty (BA-02's form-only initial state), validation (client-side `reason` presence check, `disabled` submit), error (`FormBanner` + toast via `useNotifications`), confirmation (success toast + inline result panel), per `IRA-008 §7`.
- **Not applicable, disclosed (`IRA-008 §7`):** Guided Completion, confidence/evidence panels, DNA-adaptive rendering, Sacred 12 tiering — none apply to an administrative identity-context action screen, consistent with the `Person`/`Organization` screens this Work Package extends.
- **Verification:** `tsc --noEmit` — 0 errors. `eslint` on all new/modified files — 0 problems.

---

## Documents Updated

- `Backend/Services/AuthService/models/identity_recovery_request.py` (new)
- `Backend/Services/AuthService/models/__init__.py` (modified — registers `IdentityRecoveryRequest`)
- `Backend/Services/AuthService/repositories/identity_recovery_request_repository.py` (new)
- `Backend/Services/AuthService/schemas/identity.py` (new)
- `Backend/Services/AuthService/services/identity_status_service.py` (new)
- `Backend/Services/AuthService/services/identity_recovery_service.py` (new)
- `Backend/Services/AuthService/services/identity_handoff_classification_service.py` (new)
- `Backend/Services/AuthService/routers/identity.py` (new)
- `Backend/Services/AuthService/main.py` (modified — mounts `identity.router` at `/identity`)
- `Backend/Services/AuthService/middleware/tenant.py` (modified — `/identity` prefix exemption)
- `Backend/Services/AuthService/alembic/versions/2026_08_11_0900-b1d6f4c8a3e7_identity_management.py` (new)
- `Backend/Services/AuthService/tests/test_identity_service.py` (new, 10 tests)
- `Backend/Services/AuthService/tests/test_identity_api.py` (new, 13 tests)
- `source/frontend/src/types/identity.ts` (new)
- `source/frontend/src/services/identity-api.ts` (new)
- `source/frontend/src/features/identity/state/useIdentityManagement.ts` (new)
- `source/frontend/src/features/identity/components/IdentityStatusSection.tsx` (new)
- `source/frontend/src/features/identity/components/IdentityRecoverySection.tsx` (new)
- `source/frontend/src/features/identity-access/components/IdentityAccessScreen.tsx` (modified)
- `architecture/05-Implementation/WP-08_Identity_Management.md` (charter, committed `c9dd215`)
- `architecture/05-Implementation/IRA-008_WP-08_Identity_Management_Implementation_Readiness_Assessment.md` (new)
- `architecture/06-Reviews/TECH-DEBT.md` (modified — `TD-100` through `TD-102` added)

---

## Validation

- **Backend:** `pytest tests/ -q` (with `JWT_SECRET_KEY` set, `TD-010` pre-existing environment note) → **687 passed, 0 failed** (664 prior + 23 new: 10 service-layer + 13 API), 185.15s, zero regressions.
- **Migration:** `alembic heads` → single head, `b1d6f4c8a3e7`.
- **Frontend:** `tsc --noEmit` → 0 errors. `eslint` (new/modified files) → 0 problems.
- **App wiring:** `main.py` imports cleanly; `POST /identity/refresh-status`, `POST /identity/recover`, `POST /identity/classify-handoff-rejection` all present in the route table.

---

## Technical Debt Raised

`TD-100` (Medium — BA-02 self-service-only scoping), `TD-101` (Low — BA-03's classification endpoint has no caller yet), `TD-102` (Medium — `ERB-C001-01` excluded in full). All recorded in `TECH-DEBT.md` per `CLAUDE.md §19.8.2`.

---

## Status (BA-01 through BA-03)

All three Business Activities: **Implementation Complete**. `EX-C001-01`/`02`: **Excluded** (disclosed, `TD-102`). `EX-C001-03`/`04`/`05`: **Satisfied by construction** (no new work). Ready for Independent Certification per `CLAUDE.md §19.7`/`§19.7b`, extended by `§20.7`.

---

*End of IMP-REPORT-WP-08.*
