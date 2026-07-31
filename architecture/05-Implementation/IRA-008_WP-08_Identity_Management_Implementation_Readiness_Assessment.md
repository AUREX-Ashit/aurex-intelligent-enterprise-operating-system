# IRA-008 — WP-08 Identity Management (C-001) — Implementation Readiness Assessment

**Document ID:** IRA-008
**Work Package:** WP-08
**Capability:** C-001 — Identity Management
**Governing Specification:** `PE-001-C001_Identity_Management.docx`, Version 1.1
**Status:** ACCEPTED — READY (at the scope determined in §9)
**Prepared By:** Engineering Governance session (Claude Code), under Repository Owner Execution Authorization
**Date:** 2026-07-31

---

## 1. Purpose

Determines whether, and at what scope, WP-08 (chartered `WP-08_Identity_Management.md`) may proceed to implementation, per `CLAUDE.md §19`/`§20` and `METH-002`. Per the charter's own §6 (Enterprise Experience Requirement), this IRA produces **two** implementation plans — **Plan A** (Business Capability Implementation, §4–§6) and **Plan B** (Enterprise Experience Implementation, §8) — neither of which designs screens or writes code; both are planning determinations only.

---

## 2. Governing Documents Reviewed

- `PE-001-C001_Identity_Management.docx` v1.1 — full text extracted directly from `word/document.xml` (not summarized; freshness verified byte-identical against the current repository source, `85e2dcfcbd634347368e55822a22361c`).
- `WP-08_Identity_Management.md` (charter).
- `CLAUDE.md` §16–§20 (canonical authority resolution, architectural change control, implementation checklist, Enterprise Experience Standard).
- `METH-002` / `ADR-017` (engineering methodology, five-gate closure).
- `IMP-001_Implementation_Playbook.md` §5/§6/§8/§10/§11 (Business Activity pattern, API standards, Frontend Standards, Testing Strategy).
- `SD-001 — Enterprise Presentation Architecture.md` (full text, v2.0).
- `CMD-001` §26.3a (Canonical Business Object Eligibility Test).
- `URA-001` §2 (Identity semantics, `URA-001-15`/`16`).
- `WP-RTA-001_Closure_Report.md` §7 (Authorization Runtime Engine production-readiness finding).
- `IRA-005 §12`, `IRA-007 §7.1`/`§7.2`/`§8` (precedent methodology: minimum-scope authorization; satisfied-by-construction disposition; REUSE AND CERTIFY disposition).
- Existing repository source: `Backend/Services/AuthService/{models,repositories,services,routers}` (Identity, Person, Membership, Auth); `source/frontend/src/{app,features,components,config,services,types}` (existing screens, navigation, component library, state-management pattern).

---

## 3. Existing Asset Discovery (Reuse Before Creating, `CLAUDE.md §19.2`)

Direct repository search, not assumption, found the following pre-existing assets bearing on C-001:

| Asset | Location | Status |
|---|---|---|
| `Identity` model | `models/identity.py` | Exists. No `organization_id` column. Committed `34cf7fe` (pre-WP-00, pre-governance), built as R-001 login infrastructure. |
| `IdentityRepository` | `repositories/identity_repository.py` | Exists. `get_by_email`, `get_by_email_with_person` (cited for `EX-C006-01`), `get_primary_identity`, `get_person_identities`. Used only by `auth_service.py` (R-001 login) and `person_recognition_service.py` (WP-07, C-006). No `IdentityService`, no `/identity` router, no C-001-owned endpoint of any kind exists anywhere. |
| `POST /auth/login` | `routers/auth.py` / `services/auth_service.py` | Exists (R-001, owned by `RTA-001`/`IMP-001`, out of C-001 scope per charter §3). Resolves `Identity` by email (deterministic, unique-indexed lookup), verifies password (authentication mechanism, out of scope), resolves `Membership` (C-007), issues a JWT carrying `person_id`/`identity_id`/`organization_id`/`membership_id`/`role_code`. |
| `POST /auth/refresh` | `routers/auth.py` / `services/auth_service.py` | Exists (R-001). Re-validates the refresh token, re-confirms `Membership` still active, re-issues an access token without re-authenticating. |
| `identity-access` navigation slot | `source/frontend/src/config/admin-navigation.ts` | Exists (`href: "/platform-admin/identity-access"`, committed `92701ff`, pre-dates all Business WP governance). Static config, disclosed deviation from `SD-001-018`'s own metadata-driven navigation model (documented in the same commit; no `screen_registry` backend entity exists anywhere in this repository — a platform-wide, pre-existing condition, not introduced by this Work Package). |
| `IdentityAccessScreen.tsx` | `source/frontend/src/features/identity-access/components/` | Exists, committed `34cf7fe` (same pre-governance commit as the backend `Identity` model). Embeds `ProfileSummary` (session claims, from JWT) and `PersonManagementScreen` (C-006), and an explicit, honest `UnsupportedCapabilityNotice` for **"Identity Management"** stating: *"AuthService's Identity model records identity_type, is_primary, is_verified, and last_login_at, but no endpoint reads or lists Identity records — only login and refresh."* This is the disclosed, transient placeholder `CLAUDE.md §20.6` permits during development — it is the correct, existing extension point, not a new navigation item or a new screen this Work Package must invent. |
| DS-001-aligned component library | `source/frontend/src/components/ui/*` | Exists: `Button`, `Card`, `Modal`, `Table`, `Input`, `Form`, `Menu`, `Sidebar`, `Breadcrumb`, `StatusBadge`, `Spinner`, `Toaster`, `CommandPalette`. |
| Established feature pattern | `source/frontend/src/features/{organization,person}/{components,state}` + `src/services/{organization,person}-api.ts` + `src/types/{organization,person}.ts` | Exists, applied twice already (WP-01, WP-07). A local `useState`-based state-machine hook per feature (e.g., `usePersonManagement.ts`), a thin API wrapper module calling the shared `apiClient` (never raw `fetch`), and a `Notifications` integration for network-error toasts. |
| Hand-off rejection classification pattern | `services/authorization_policy_conflict_service.py::classify_handoff_rejection()` | Exists, committed `ffaaec6` (`WP-02` BA-10, `EX-C003-10`, `Contract 5.7`'s C-003 analogue). Classifies entirely from the object's own independently-verifiable current state, never from the reporting capability's stated reason. Reused as the design precedent for BA-03 (§5) after being found on further discovery — corrected from an earlier, less precise citation of `IRA-007` BA-05's simpler static-routing-table pattern. |

**Conclusion:** per `CLAUDE.md §2`/`§19.5` (Reuse → Configure → Extend → Compose → Create), WP-08's own Plan A extends the existing `Identity` model/repository (no new columns), and Plan B extends the existing `IdentityAccessScreen.tsx`/navigation slot/component library/feature pattern. No new navigation item, no new screen shell, no new component, no new state-management pattern is created.

---

## 4. Gap Analysis — Scope Determination Per Enterprise Experience

Each of the 8 EXs is evaluated in turn against real repository evidence (never assumed).

### 4.1 `EX-C001-01`/`EX-C001-02` (`ERB-C001-01`, Establish New Identity Context) — **EXCLUDED**

`ERB-C001-01`'s own Entry Context (`PE-001-C001` Chapter 3): *"An Authoritative Person Context (C-006)... and an Access Evaluation Outcome (C-002) confirming the requesting persona is permitted to provision a new Identity."* `EX-C001-01`'s own Context Required repeats this verbatim. Per `Contract 5.3`: *"Every C-001 Enterprise Experience that performs a governed action (establishment, recovery) SHALL request, and SHALL NOT compute, an Access Evaluation Outcome from C-002 for that action."*

`C-002` (Access Management, `WP-05`) was authorized only at minimum scope (`IRA-005 §12`): a genuine, affirmative Permitted/Denied determination requires a real, production `TierResolver`, which `WP-RTA-001`'s own Closure Report §7 states does not exist for any tier ("Not production ready"). An affirmative Access Evaluation Outcome is therefore structurally unobtainable from this repository's own running code today — the same root cause `IRA-005 §12` already disclosed for `WP-05`'s own excluded branches.

**Disposition, mirroring `IRA-005 §12`'s own precedent exactly:** `EX-C001-01`/`EX-C001-02` (and therefore `ERB-C001-01` in full) are **excluded from this Work Package's authorized scope**, per the charter's own disclosed constraint (`WP-08_Identity_Management.md §2`). This is a scope exclusion, not a defect — the charter disclosed it before this IRA confirmed it.

### 4.2 `EX-C001-03`/`EX-C001-04` (`ERB-C001-02`, Resolve Claimed Identity) — **SATISFIED BY CONSTRUCTION**

`EX-C001-03`'s Trigger: *"An already-established Identity presents itself (a claimed Identity signal) and deterministically matches exactly one established Identity-to-Person association."* Its Context Produced: *"An Authoritative Identity Context, handed to EX-C001-05... and to whichever capability the Person next engages."*

`POST /auth/login` (`auth_service.py`, Step 1) performs exactly this: a deterministic, unique-indexed lookup (`Identity.email` is `unique=True` — non-unique match is structurally impossible in this schema) resolving a claimed Identity (email) to its associated `Person`, and issues a JWT whose claims (`person_id`, `identity_id`, `organization_id`, `membership_id`, `role_code`) are the Authoritative Identity Context handed forward as every dependent router's own Entry Context precondition — precisely `EX-C001-03`'s own stated Context Produced. A failed lookup (`identity_repo.get_by_email` returns `None`) surfaces as `401`, which is `EX-C001-04`'s own "no authoritative association" outcome. Because `email` carries a database-level uniqueness constraint, `EX-C001-04`'s third outcome ("Identity resolution conflict" — a non-unique match) is structurally unreachable in this schema — a scoping fact disclosed here, not a defect requiring new code.

Building a second, dedicated `C-001` endpoint that re-performs this identical lookup would duplicate `POST /auth/login`'s own business logic, violating `CLAUDE.md §8` ("Never duplicate business logic") and `§2` ("Extend before creating"). This determination mirrors `IRA-007 §7.1`/`§7.2`'s own "satisfied by construction" disposition for `EX-C006-09`/`12` exactly, and is independently reinforced by `PE-001-C001`'s own Out of Scope statement (charter §3, verbatim from `§1.5`): *"session implementation, token semantics... owned by RTA-001, IMP-001"* — the resolution mechanism (JWT issuance) is `RTA-001`-owned; only the Enterprise Experience of deterministic resolution is `C-001`'s concern, and that Experience is already realized.

**Disposition:** `EX-C001-03`/`EX-C001-04` are **satisfied by construction** via the existing, unmodified `POST /auth/login`. No new Business Activity, endpoint, or code change. The existing `ProfileSummary.tsx` (displaying `person_id`, `identity_id`, `organization_id`, `membership_id`, role, and session expiry directly from the JWT claims) is, for the same reason, the already-existing, already-correct Enterprise Experience realization of this outcome — not a gap Plan B must close.

### 4.3 `EX-C001-05` (`ERB-C001-03`, Preserve Current Participating Identity Context Continuity) — **SATISFIED BY CONSTRUCTION**

`EX-C001-05`'s own Context Created: *"Nothing new — continuity carries the existing Identity Context forward."* This EX describes an architectural property (uninterrupted, non-redundant availability of the current Identity Context across navigation), not a discrete user-facing action. `POST /auth/refresh` (re-issuing an access token without re-authenticating, re-confirming only `Membership` currency) is the existing mechanism that realizes this property; per `Contract 5.5`, this ERB never satisfies a destination capability's own Access/Membership/Role/Permission/Workspace requirement — and the existing implementation does not attempt to.

**Disposition:** satisfied by construction via the existing, unmodified `POST /auth/refresh`. No new work.

### 4.4 `EX-C001-06` (`ERB-C001-04`, Detect and Resolve Disrupted or Conflicting Identity Context) — **IN SCOPE — BA-01**

Given `RTA-001`'s own runtime Identity Resolution capability is "not production ready" (no automatic revocation/conflict signal source exists), the only presently reachable trigger is a Person or administrator explicitly requesting re-confirmation that a currently-held Identity Context remains valid. `EX-C001-06`'s own Context Required lists the runtime signal only "where relevant" (conditional, not mandatory) — the re-resolution-against-`C-006` path does not depend on `RTA-001`. `Context Created`: *"Nothing new where the outcome is a refresh."* No Access Evaluation Outcome is named in this EX's own Context Required at all.

**Disposition:** in scope, buildable now, without `RTA-001` and without an Access Evaluation Outcome. Realized as **BA-01 — Detect and Resolve Disrupted Identity Context**, a read-only re-confirmation (no persistence — mirrors `IRA-007`'s own BA-03 "Understand" pattern), per §5 below.

### 4.5 `EX-C001-07` (`ERB-C001-04`, Recover Inaccessible Identity Context) — **IN SCOPE (self-service branch) — BA-02**

Context Required: *"a currently valid Authoritative Person Context (C-006)... and an Access Evaluation Outcome (C-002) for the recovery action **where governance requires one**"* — conditional, unlike `ERB-C001-01`'s own unconditional requirement. This Work Package's scope is bounded to the branch where governance does not require a separate Access Evaluation Outcome: a Person requesting governed recovery of their **own** Identity (self-service), which requires only a currently valid Person Context (`C-006`, satisfied — `WP-07` `CLOSED`). Administrator-initiated recovery on another Person's behalf — the branch this EX's own text also names ("a governing administrator initiates recovery on the Person's behalf") — is excluded from this Work Package pending the same Access Evaluation resolver `§4.1` already disclosed as unavailable, mirroring `IRA-005 §12`'s own precedent of authorizing only the branch not blocked.

`Context Produced`: *"a governed recovery request record, routing the Person toward ERB-C001-01... or ERB-C001-02... never a completed technical credential reset performed by this EX itself."* Since `ERB-C001-01` is itself excluded (§4.1), this Work Package's own `EX-C001-07` realization stops at recording the governed recovery request and its routing determination — it does not execute the routed-to establishment, matching this EX's own stated "Experience Completion — Complete once the Person is routed... those ERBs govern the substance of what follows."

**Disposition:** in scope at self-service-only scope. Realized as **BA-02 — Recover Inaccessible Identity Context (self-service)**, per §5 below.

### 4.6 `EX-C001-08` (`ERB-C001-04`, Resolve Dependent Capability Identity Hand-off Rejection) — **IN SCOPE — BA-03**

Purely a classification Business Activity: *"Classifies a dependent capability's Identity Context hand-off rejection as either capability-scoped insufficiency or an Identity Context integrity signal, and routes accordingly."* No Access Evaluation Outcome or `RTA-001` dependency anywhere in this EX's own text. Directly mirrors `IRA-007`'s own BA-05 (`person_conflict_service.py`, classification-only, static routing table, no persistence).

**Disposition:** in scope, no blocker. Realized as **BA-03 — Classify Identity Hand-off Rejection**, per §5 below, mirroring the `IRA-007` BA-05 precedent exactly (no persistence).

### 4.7 Summary

| EX | ERB | Disposition | Realization |
|---|---|---|---|
| `EX-C001-01`/`02` | `ERB-C001-01` | Excluded (Access Evaluation blocker, disclosed by charter) | None this WP |
| `EX-C001-03`/`04` | `ERB-C001-02` | Satisfied by construction | `POST /auth/login` (unmodified) |
| `EX-C001-05` | `ERB-C001-03` | Satisfied by construction | `POST /auth/refresh` (unmodified) |
| `EX-C001-06` | `ERB-C001-04` | In scope | BA-01 |
| `EX-C001-07` | `ERB-C001-04` | In scope (self-service only) | BA-02 |
| `EX-C001-08` | `ERB-C001-04` | In scope | BA-03 |

Per `PE-001-C001 §9.5`, every ERB has at least one realizing EX; this Work Package's own scope leaves `ERB-C001-01` with zero *implemented* EXs (both excluded), which is a disclosed scope exclusion identical in kind to `IRA-005 §12`'s own precedent, not a completeness defect in the governing specification itself (the specification's own completeness test, `§9.5`, passed independently of this Work Package's scope decision).

---

## 5. PLAN A — Business Capability Implementation

### BA-01 — Detect and Resolve Disrupted Identity Context (`EX-C001-06`)

- **Domain Model:** None new. Reads `Identity` (existing) and `Person` (existing, `C-006`) only.
- **Database:** No migration.
- **Repository:** `IdentityRepository` — add `get_by_id(identity_id)` (mirrors `BaseRepository.get_by_id()` already used platform-wide).
- **Service:** New `services/identity_status_service.py` — `refresh(identity_id)`: loads `Identity`, confirms its `Person` (`C-006`) still exists and is not soft-deleted/deactivated; returns a refreshed status outcome (`CURRENT` or `UNRESOLVED`) with the same JWT-claim shape `ProfileSummary` already renders, so the frontend can display it identically. Read-only — no audit record, no domain event, mirroring `OrganizationService.get_details()`'s established precedent (`WP-01`) and `IRA-007`'s BA-03.
- **API:** `POST /identity/refresh-status` — request: `{}` (acts on the caller's own current Identity from JWT claims); response: refreshed status + Identity Context shape, or an explicit unresolved outcome (never a silent 200 with stale data). Gated by authentication only (any authenticated caller may re-confirm their own Identity Context) — no `require_platform_admin` gate, since this is a self-referential check, not an administrative action.
- **Events:** None (read-only re-confirmation, no state change).
- **Testing:** Unit (service: current Person → `CURRENT`; deactivated/missing Person → `UNRESOLVED`) + API (200 current, 200 unresolved, 401 unauthenticated).

### BA-02 — Recover Inaccessible Identity Context, self-service (`EX-C001-07`)

- **Domain Model:** New `IdentityRecoveryRequest` — `id`, `person_id` (FK → `persons.id`), `requested_by_identity_id` (FK → `identities.id`, nullable — the unusable Identity may itself be unreachable), `reason` (free text), `routed_path` (`NEW_IDENTITY` | `RE_RESOLUTION`, per `EX-C001-07`'s own two named routing targets), `status` (`PENDING`, since this WP does not execute the routed-to establishment/resolution itself), `created_at`.
- **Database:** New migration, one table, `CheckConstraint` on `routed_path` and `status` enums, `ForeignKeyConstraint`s to `persons.id`/`identities.id` (nullable).
- **Business Object Eligibility (`CMD-001 §26.3a`):** see §6 below — **not eligible**, same disposition as `IRA-007`'s own four tables.
- **Repository:** `repositories/identity_recovery_request_repository.py` — thin `BaseRepository` subclass.
- **Service:** `services/identity_recovery_service.py` — `request_recovery(person_id, reason)`: confirms a currently valid `Person` Context (`C-006`) exists for `person_id`; determines `routed_path` (`RE_RESOLUTION` if the Person holds at least one existing `Identity` record still on file — even if currently unusable — else `NEW_IDENTITY`); persists the record at `status=PENDING`; does **not** create an `Identity`, does **not** call establishment (`ERB-C001-01` excluded, §4.5).
- **API:** `POST /identity/recover` — request: `{person_id, reason}`; response: `IdentityRecoveryRequestResponse` (id, routed_path, status, created_at). Gated by authentication only, matching the self-service scoping determination in §4.5 — an authenticated caller requests recovery for their own `person_id` only (request-body `person_id` validated against the caller's own JWT `person_id` claim; a mismatch is `403`, preventing one Person from filing a recovery request against another's Identity without the excluded administrator-initiated, Access-Evaluation-gated branch).
- **Events:** `IDENTITY_RECOVERY_REQUESTED` published on successful creation, mirroring `IRA-007`'s own non-canonical audit-trail tables (e.g. `PersonCorrection`'s `PERSON_CONTEXT_CORRECTED`), which publish an event despite not being canonically registered — event-worthiness and canonical Business Object registration are independent determinations.
- **Testing:** Unit (valid Person → `PENDING` record created, correct `routed_path` branch for each case) + API (201 created, 403 person_id mismatch, 404 unknown person_id).

### BA-03 — Classify Identity Hand-off Rejection (`EX-C001-08`)

- **Domain Model:** None (classification-only, no persistence).
- **Database:** No migration.
- **Repository:** None new.
- **Service:** `services/identity_handoff_classification_service.py` — `classify(identity_id, rejecting_capability, stated_reason)`. **Corrected during IRA drafting to mirror the closer, more authoritative precedent found on further discovery: `WP-02` BA-10's own `AuthorizationPolicyConflictService.classify_handoff_rejection()` (committed `ffaaec6`, realizing `EX-C003-10`/`Contract 5.7`'s C-003 analogue) — not the more generic `IRA-007` BA-05 static-routing-table pattern originally cited.** Per that precedent's own governing principle (`PE-001-C001 Contract 5.7`, verbatim: *"The dependent capability's stated rejection reason is a signal, not an authority... SHALL NOT allow a dependent capability to become authoritative for Identity... unless it canonically owns the rejected fact"*), the classification is computed **entirely from the Identity Context's own independently-verifiable current state — never from `stated_reason`**, which is recorded for audit traceability only, exactly as `AuthorizationPolicyConflictService.classify_handoff_rejection()` computes its own classification from `obj.status`/`detect_conflicts()` rather than the reporting capability's own text. Concretely: re-resolves the Identity Context by re-invoking BA-01's own `IdentityStatusService.refresh()` logic against the same `identity_id`; if it re-resolves `CURRENT` (the underlying Person Context is still valid), the rejection is classified `CAPABILITY_SCOPED_INSUFFICIENCY` (Identity Context preserved, unchanged); if it re-resolves `UNRESOLVED`, the rejection is classified `INTEGRITY_SIGNAL` and routed to `EX-C001-06` (`Contract 5.7`: *"A rejection classified as an integrity signal SHALL be routed to ERB-C001-04/EX-C001-06 for re-resolution against source-of-truth facts"*) — realized here as the response naming BA-01's own endpoint as the next step, not as an automatic re-invocation.
- **API:** `POST /identity/classify-handoff-rejection` — request: `{identity_id, rejecting_capability, stated_reason}`; response: `{classification: "CAPABILITY_SCOPED_INSUFFICIENCY" | "INTEGRITY_SIGNAL", identity_context_preserved: bool, routed_to: str | null, explanation: str}`. Gated by authentication only.
- **Events:** None.
- **Testing:** Unit (current Identity/Person → `CAPABILITY_SCOPED_INSUFFICIENCY`, preserved; unresolved Identity/Person → `INTEGRITY_SIGNAL`, routed) + API (200 both branches, 401 unauthenticated, 404 unknown identity_id).

### Cross-cutting

- **`middleware/tenant.py`:** `/identity` prefix added to the exemption list, on the stronger basis already established for `/person` (`Identity` carries no `organization_id` column anywhere in its own model, nor does the new `IdentityRecoveryRequest` table) — not the weaker PLATFORM_ADMIN-interim-gate basis used for `/domain-permissions`/`/access-evaluations`.
- **Authorization:** none of BA-01/02/03 is gated by `require_platform_admin` — each is a self-referential action an authenticated caller performs against their own Identity/Person context, consistent with `Contract 5.3`'s own scoping (only *governed* actions — establishment, recovery — require Access Evaluation, and BA-02's self-service branch is scoped specifically to avoid that requirement per §4.5).
- **Migration:** one new Alembic revision (`IdentityRecoveryRequest` table only), `down_revision` = the current head at implementation time.

---

## 6. Business Object Eligibility Analysis (`CMD-001 §26.3a`)

Applying the three-step test to `IdentityRecoveryRequest` (the only new persisted construct):

1. **Independent Identity** — `IdentityRecoveryRequest` has no existence or business meaning independent of the specific recovery request it records; it is not referenced by any other Enterprise Experience's own Produced Context field anywhere in `PE-001-C001` or any other reviewed capability specification.
2. **Cross-Experience Reference Test** — fails. `EX-C001-07`'s own text names it only as this EX's own Context Created; no other EX or capability specification references it.
3. **Governed Lifecycle** — `EX-C001-07`'s own text: *"Experience Completion — Complete once the Person is routed... those ERBs govern the substance of what follows."* The record's own lifecycle ends at creation (`status=PENDING`); it is not itself governed through further states by this Work Package.

**Result: NOT ELIGIBLE for canonical Business Object registration.** Same disposition as `IRA-007`'s own four audit-trail tables (`PersonDistinctionDecision`, `PersonReconciliationDecision`, `PersonCorrection`, `PersonEnrichment`) — no new ADR required.

---

## 7. PLAN B — Enterprise Experience Implementation

Derived only from `PE-001`, `PE-001-C001`, `SD-001`, `DS-001`, `IMP-001` §10 — per the charter's own §6, this plan identifies what is built; it does not itself design a screen.

- **Enterprise Experiences realized:** `EX-C001-06`, `EX-C001-07` (self-service), `EX-C001-08` (system-facing; see below).
- **User Personas:** any authenticated Person (BA-01, BA-02); `EX-C001-08` is triggered by a dependent capability's own backend hand-off logic, not directly by a human persona — its "screen" surface is limited to displaying an already-classified outcome if a dependent capability's own UI chooses to surface one; WP-08 builds only the classification endpoint (§5), no dedicated screen, since no dependent capability in this repository today calls it (disclosed as Technical Debt, §10).
- **User Journey:** an authenticated user, from the existing Identity & Access Management screen, requests re-confirmation of their current Identity status (BA-01) or, where their Identity has become unusable, requests governed recovery (BA-02).
- **Workspace placement:** the existing `identity-access` slot in `ADMIN_NAV_ITEMS` (`/platform-admin/identity-access`) — no new navigation entry.
- **Screens/Views:** extends the existing `IdentityAccessScreen.tsx`. The current "Identity Management" `UnsupportedCapabilityNotice` block is replaced with a new `IdentityStatusSection` (BA-01: a "Refresh Identity Status" action against `ProfileSummary`'s existing claims display, reusing `Card`/`Button`/`StatusBadge`) and a new `IdentityRecoverySection` (BA-02: a `Form` — reusing the existing `Form`/`Input` components exactly as `EstablishOrganizationForm.tsx`/`EstablishPersonSection.tsx` already do — collecting `reason`, submitting to `POST /identity/recover`, displaying the resulting `routed_path`/`status`). The "Membership Management" and "Organization Association" `UnsupportedCapabilityNotice` entries are untouched (out of `C-001`'s own scope, §3 of the charter).
- **Forms:** one (`IdentityRecoverySection`'s recovery-request form) — `reason` (required, min-length validated client-side before submit, mirroring `EstablishPersonSection.tsx`'s own validation pattern).
- **Tables:** none — neither BA-01 nor BA-02 produces a list; no bulk actions or saved views apply (`SD-001-051`/`052` not applicable at this scope).
- **Search/Filters:** not applicable (no list view).
- **Actions:** "Refresh Identity Status" (BA-01), "Request Recovery" (BA-02) — 2 actions, well under `SD-001-043`'s 7-item Action Center cap; given the low count and the existing precedent (`Person`/`Organization` screens do not use a dedicated Action Center component either), these render as ordinary `Button` actions within their own `Card`, not a separate Action Center widget — mirroring the established precedent rather than introducing a new pattern for two buttons.
- **Validation state:** client-side `reason` presence/length check before submit (`IdentityRecoverySection`), mirroring `EstablishPersonSection.tsx`.
- **Empty state:** not applicable to BA-01 (always returns a status). BA-02: prior to any submission, the section shows its form only (no "empty list" concept applies, since this is an action, not a list view).
- **Error state:** network/API errors surfaced via the existing `useNotifications()` toast pattern (mirrors `usePersonManagement.ts`'s `describeError`), distinct from the validation state per `SD-001-049`.
- **Loading state:** existing `Spinner` component, shown on the action button while its request is in flight (mirrors `usePersonManagement.ts`'s `"recognizing"`/`"establishing"` transient states).
- **Confirmation state:** a success toast (`notify(..., "success")`) plus an inline result panel showing the outcome (refreshed status for BA-01; `routed_path`/`status` for BA-02) — mirrors `PersonResultPanel.tsx`'s own established pattern.
- **Accessibility:** reuses `Card`/`Button`/`Form`/`Input`/`StatusBadge`, each already implementing `SD-001-059`–`062` (accessible name/role/state, keyboard reachability, color-independent status) as established by their existing use in `PersonManagementScreen`/`OrganizationManagementScreen` — no new component, so no new accessibility surface to validate beyond the existing library's own conformance.
- **Responsive behaviour:** inherited from `IdentityAccessScreen`'s existing `space-y-*`/Tailwind responsive classes, identical pattern to the existing `PersonManagementScreen` it already hosts.
- **State management:** a new `useIdentityManagement.ts` hook (mirrors `usePersonManagement.ts` exactly: a typed state union covering idle/loading/success/error per action, `useNotifications()` integration, no new pattern invented) plus a new `identity-api.ts` module (mirrors `person-api.ts`: thin wrappers over `apiClient.post`, no endpoint invented beyond §5's three).
- **Not applicable, disclosed rather than silently omitted (§4.7's own scope determination inherited into Plan B):** Guided Completion/Question Engine (`SD-001` Section 3), Confidence/Evidence panels (Section 4), Enterprise DNA adaptive rendering (Section 6), Sacred 12 tiering (Section 8) — none apply to an administrative identity-context action screen; the existing `Person`/`Organization` screens this Work Package extends already establish this same scoping precedent (neither implements Guided Completion, confidence scoring, DNA adaptation, or Sacred 12 treatment), so this is a consistent, precedented application, not a new judgment call specific to C-001.

---

## 8. Readiness Decision

**READY**, at the scope determined in §4.7: BA-01, BA-02 (self-service only), BA-03, backend and frontend, per Plan A (§5) and Plan B (§7). `ERB-C001-01` (`EX-C001-01`/`02`) excluded per the charter's own disclosed constraint. `EX-C001-03`/`04`/`05` require no new work (satisfied by construction, §4.2/§4.3).

No constitutional blocker. No new canonical Business Object (§6). No new architectural component beyond one table (`IdentityRecoveryRequest`) and the router/service/repository files listed in §5, and their frontend counterparts listed in §7 — all following established, precedented patterns, none inventing a new one.

---

## 9. Anticipated Technical Debt

- **TD-candidate-A** (Medium): BA-02's self-service scoping excludes administrator-initiated recovery on another Person's behalf, pending the same Access Evaluation resolver `§4.1` discloses as unavailable — same root cause as `TD-070`/`IRA-005 §12`'s own exclusions.
- **TD-candidate-B** (Low): `EX-C001-08`'s classification endpoint (BA-03) has no caller anywhere in this repository today — no dependent capability's own backend currently invokes a hand-off-rejection flow. Built per the governing specification's own completeness requirement, disclosed as currently unconsumed.
- **TD-candidate-C** (Low): `ERB-C001-01` is excluded in full — `PE-001-C001 §9.5`'s own ERB→EX realization mapping is therefore not fully *implemented* by this Work Package (though the specification's own completeness test independently passed). Tracked for future resolution once `C-002`'s own Access Evaluation resolver reaches production readiness.

(Final Technical Debt IDs assigned at implementation time, per `CLAUDE.md §19.8.2`.)

---

## 10. Testing Strategy

Per `IMP-001 §11`: Business Activity Contract tests for each of BA-01/02/03 (unit, service-layer); Authorization Boundary tests (401 unauthenticated for all three; 403 person_id-mismatch for BA-02); API tests for every endpoint and status branch listed in §5. Full AuthService regression suite re-run before closure, per every prior Work Package's own precedent.

---

## 11. Repository-Owner Authorization

Authorized for implementation under the Repository Owner Execution Authorization already issued for WP-08's full lifecycle (2026-07-31), which named this IRA's own Plan A/Plan B dual-plan requirement as a precondition. No further approval gate is required before implementation begins, per that authorization's own terms.

---

*End of IRA-008.*
