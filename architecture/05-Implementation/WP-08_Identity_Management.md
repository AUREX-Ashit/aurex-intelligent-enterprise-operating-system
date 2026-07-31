# WP-08 — Identity Management

**Work Package ID:** WP-08
**Type:** Business Capability Work Package
**Capability ID:** C-001
**Capability Name:** Identity Management
**Governing Capability Specification:** `PE-001-C001_Identity_Management.docx`, Version 1.1 (Corrected Gold Standard Engineering Pass)
**Status:** **CHARTERED**
**Chartered By:** Repository Owner
**Chartering Date:** 2026-07-31
**Governing IRA:** Not yet created. Implementation authority does not exist until `IRA-008` is drafted per repository methodology (`METH-002`, `IMP-001`, `CLAUDE.md §19`/`§20`) and concludes **READY**.
**This document defines the Work Package charter only. No Implementation Readiness Assessment, Business Activity decomposition, design, source code, API, database object, frontend implementation, or test is created by this document.**

---

## 1. Business Objective

Manage enterprise identities (`CAP-001`, verbatim). Realize the Enterprise Experience through which a presenting authentication instance is established, recognized, continuously preserved, and — where disrupted — safely re-established as a trustworthy Authoritative Identity Context linked to exactly one Person, per `URA-001-16`'s own distinction between Identity (authentication) and Organization Membership.

## 2. Scope

`PE-001-C001`'s full capability architecture, per its own Chapters 2–4:

- **1 Capability Experience Blueprint** — `CRB-C001`
- **4 Enterprise Experience Blueprints (ERBs)**:
  - `ERB-C001-01` — Establish New Identity Context
  - `ERB-C001-02` — Resolve Claimed Identity to Authoritative Identity Context
  - `ERB-C001-03` — Preserve Current Participating Identity Context Continuity
  - `ERB-C001-04` — Resolve Identity Context Disruption, Conflict and Recovery
- **8 Enterprise Experiences (EXs)** — `EX-C001-01` through `EX-C001-08`:
  1. Establish New Identity for Person
  2. Produce Rejected or Unresolved Identity Establishment Outcome
  3. Resolve Claimed Identity to Authoritative Identity Context
  4. Produce Unresolved or Conflicted Identity Resolution Outcome
  5. Continue Enterprise Journey Within Current Participating Identity Context
  6. Detect and Resolve Disrupted or Conflicting Identity Context
  7. Recover Inaccessible Identity Context
  8. Resolve Dependent Capability Identity Hand-off Rejection
- **8 capability-specific Experience Contracts** (Chapter 5)

Exact Business Activity decomposition and minimum-scope determination are **not decided by this charter** — they are `IRA-008`'s own determination, per this repository's own `IRA-005 §12`/`IRA-006 §12`/`IRA-007 §12` precedent of scope decisions being made at the IRA stage, not the charter stage.

**Disclosed architectural constraint for `IRA-008`'s own attention (not resolved by this charter):** `ERB-C001-01`'s own Entry Context requires "an Access Evaluation Outcome (C-002) confirming the requesting persona is permitted to provision a new Identity," and its Experience Flow states the provisioning action halts unless that Access Evaluation Outcome is affirmative. `C-002` (Access Management) was authorized only at minimum scope (`WP-05`, `IRA-005 §12`): a genuine Permitted/Denied determination requires a real `URA-001-76` precedence-chain resolver, which `WP-RTA-001`'s own Closure Report §7 states is "Not production ready." An affirmative Access Evaluation Outcome is therefore structurally unobtainable from this repository's own running code today. This blocks `EX-C001-01`/`EX-C001-02` (`ERB-C001-01`, "Establish New Identity Context") specifically — direct reading of `EX-C001-03` through `08`'s own Context Required fields finds no equivalent dependency for the remaining three ERBs (`EX-C001-07`'s own text names an Access Evaluation Outcome only "where governance requires one," and does not gate the EX's own completion on it). `IRA-008` shall determine, as its own Gap Analysis, whether `ERB-C001-01` is excluded from this Work Package's authorized scope on this basis, mirroring `IRA-005 §12`'s own precedent and root cause exactly — this charter does not pre-decide that determination, it discloses the evidence for it.

## 3. Out of Scope

Per `PE-001-C001 §1.5`, verbatim:

- **Person existence, recognition, or disambiguation (`C-006`).**
- **Membership existence, standing, or effective validity (`C-007`).**
- **Access evaluation and authorization decisions (`C-002`).**
- **Role and Permission definition or assignment (`C-003`).**
- **Organization identity, existence, or validity (`C-004`).**
- **Workspace resolution, entry, or continuity (`C-008`).**
- Authentication mechanisms, password policy, MFA policy, federation protocols, identity-provider implementation, session implementation, token semantics, credential storage, login-screen behaviour, or technical recovery mechanisms — owned by `RTA-001`, `IMP-001`, and the applicable canonical or implementation authority.
- Capability identity, naming, and business-intent definition (`CAP-001`).

`C-001` governs only the establishment, resolution, continuation, and disruption/recovery of Identity **Context** — never the technical authentication mechanism itself, and never the substance of any Enterprise Experience a dependent capability hosts once an Authoritative Identity Context is handed off.

## 4. Dependencies

- **Primary Specification:** `URA-001` §2 (Identity semantics, `URA-001-15`/`16`).
- **Cross-Specification Dependencies (consumed):** `C-006` (Authoritative Person Context — satisfied, `WP-07` CLOSED); `C-002` (Access Evaluation Outcome — satisfied only for the `Unresolved`/`Deferred`/`501` branches `WP-05` implemented; **not** satisfied for a genuine affirmative result, see §2's disclosed constraint).
- **Cross-Specification Dependencies (referenced only, not consumed):** `C-007` (Membership Context), `C-003` (Role and Permission), `C-004` (Organization Context), `C-008` (Workspace Context — `C-001`'s own text: "Identity Management Enterprise Experiences are not themselves Workspace-hosted"), `RTA-001` (Identity Resolution runtime capability, consumed as a signal, never redefined).
- **No dependency on any not-yet-built capability's own existence.** `C-008` is referenced only, never consumed; `C-001` does not require `C-008` to be chartered.
- **Unblocked by `WP-07`'s own closure.** `PE-001-C001`'s own Document Control names `C-006` — Authoritative Person Context, consumed — as a required Cross-Specification Dependency; `WP-07` (Person Management) is now `CLOSED`, satisfying this dependency.

## 5. Success Criteria

This Work Package shall be considered `CLOSED` only when:

- `IRA-008` is drafted per repository methodology (`METH-002`, `IMP-001`, `CLAUDE.md §19`/`§20`) and concludes **READY**.
- `IRA-008` produces **both** required implementation plans in full (§6 below) — a single-plan (backend-only) `IRA-008` does not satisfy this Work Package's own charter.
- Every Business Activity `IRA-008` charters is implemented per **both** plans, unit and integration tested, and independently reviewed.
- The Enterprise Experience delivered for each in-scope Business Activity is demonstrable through the running application, per `CLAUDE.md §20.4`.
- The full five-gate `CLAUDE.md §19.7b` closure sequence passes: Independent Certification, Verification & Validation Audit, Remediation (if required) with Independent Verification, and Release Readiness Audit — each gate additionally verifying `§20`'s own Work Package Completion Gate Extension (`§20.7`): backend complete, Enterprise Experience complete, navigation complete, end-to-end workflow demonstrable, frontend and backend fully integrated.
- Zero regressions against the full AuthService test suite and, where a frontend test suite is introduced, against it.
- The `ERB-C001-01` scope disclosure (§2) is explicitly resolved in `IRA-008` — either included with a demonstrated resolution of the Access Evaluation blocker, or excluded with the same disclosed, precedented reasoning `IRA-005 §12` already established for the identical root cause.
- All Technical Debt raised is recorded in `TECH-DEBT.md` per `CLAUDE.md §19.8`.
- `WPR-001` and `WP-REG-001` are updated to `CLOSED` status with the resolving commit hash.

## 6. Enterprise Experience Requirement (Mandatory — `CLAUDE.md §20`)

**WP-08 is the first Work Package governed by `CLAUDE.md §20` (Enterprise Experience Standard).** `IRA-008` **shall** produce two distinct, complete implementation plans before this Work Package may proceed to implementation. A single-plan `IRA-008` (backend only) does not conclude READY under this charter.

### Plan A — Business Capability Implementation

Derived from `IMP-001` (§5/§6/§8/§11) and this repository's own established Business Activity implementation pattern (`WP-01` through `WP-07` precedent). Shall identify, at minimum:

- Business Activities (candidate decomposition of the in-scope EXs named in §2)
- Domain Model (new/reused entities, relationships)
- Database (new/reused tables, columns, constraints, migrations)
- Repository layer (new/reused repository methods)
- Services (new/reused service methods, Business Rule enforcement)
- APIs (new/reused endpoints, request/response contracts)
- Events (domain events, if any)
- Testing (unit, integration, API test scope)

### Plan B — Enterprise Experience Implementation

Derived **only** from `PE-001`, `PE-001-C001`, `SD-001`, `DS-001`, and `IMP-001` (principally `IMP-001 §10`, Frontend Standards) — never invented, never duplicating what those documents already govern (`CLAUDE.md §20.2`). Shall identify, at minimum:

- Enterprise Experiences (the in-scope `EX-C001-xx` set, per §2)
- User Personas (per `PE-001-C001`'s own Participating Personas fields)
- User Journeys (per `PE-001-C001`'s own Trigger/Navigation Expectations fields)
- Navigation (per `SD-001`'s own navigation principles and `PE-001`'s own Navigation Philosophy)
- Workspace placement (per `PE-001-C001`'s own Participating Workspaces fields and `PE-001` Chapter 13's Workspace Model)
- Screens, Views, Forms, Tables, Search, Filters, Actions (per `SD-001`'s own screen-design principles and `DS-001`'s own component inventory — never inventing a component `DS-001` does not already define, per `CLAUDE.md §19.1`)
- Validation, Error states, Empty states, Loading states (per `IMP-001 §10.3`'s own content-disclosure states and `CLAUDE.md §20.6`'s own interaction-state baseline)
- Accessibility and Responsive behaviour (per `SD-001`'s own accessibility principles and `DS-001`'s own responsive/theme architecture)

**This is a planning requirement on `IRA-008` alone.** This charter does not design a single screen, does not implement any frontend, and does not invent architecture — per this document's own authority limits (§8).

## 7. Repository Authority

Chartered under Repository Owner authority, per this repository's own Work Package chartering precedent (`WP-01` through `WP-07`, each chartered by explicit Repository Owner instruction, recorded in `WPR-001`/`WP-REG-001`). This charter is a governance activity only.

**Implementation authority does not exist under this charter.** No Business Activity decomposition, source code, test, API, database object, frontend implementation, or design artifact may be created citing this document as authorization. Implementation authority begins only once `IRA-008` is drafted, produces both Plan A and Plan B in full, and concludes **READY**, and the Repository Owner explicitly instructs execution of the newly-ready Work Package — the same two-step gate (Charter → IRA-READY → explicit execution instruction) already applied to `WP-06` and `WP-07`.

## 8. Governing Documents

`CAP-001` (capability identity and Business Intent) · `PE-001` (Enterprise Experience methodology) · `PE-001-C001_Identity_Management.docx` v1.1 (governing Capability Specification) · `URA-001` (Primary Specification) · `SD-001` (Enterprise Presentation Architecture) · `DS-001` (AUREX Design System) · `CLAUDE.md` (repository operating rules, §14/§16/§17/§18/§19/§20) · `METH-002` / `ADR-017` (engineering methodology) · `IMP-001` (implementation playbook, including §10 Frontend Standards) · `WPR-001` (roadmap authority) · `WP-REG-001` (execution-status authority) · `DOC-000` (documentation register).

---

*This charter records that WP-08 exists and is authorized to proceed to the Implementation Readiness Assessment stage. It does not itself authorize implementation.*
