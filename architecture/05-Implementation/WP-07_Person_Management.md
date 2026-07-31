# WP-07 — Person Management

**Work Package ID:** WP-07
**Type:** Business Capability Work Package
**Capability ID:** C-006
**Capability Name:** Person Management
**Governing Capability Specification:** `PE-001-C006_Person_Management.docx`, Version 1.1 (Gold Standard correction pass)
**Status:** **CHARTERED**
**Chartered By:** Repository Owner
**Chartering Date:** 2026-07-31
**Governing IRA:** Not yet created. Implementation authority does not exist until `IRA-007` is drafted per repository methodology (`METH-002`, `IMP-001`) and concludes **READY**.
**This document defines the Work Package charter only. No Implementation Readiness Assessment, Business Activity decomposition, design, source code, test, API, or database change is created by this document.**

---

## 1. Business Objective

Manage enterprise persons (`CAP-001`, verbatim). Realize the Enterprise Experience through which the platform establishes, recognizes, distinguishes, understands, corrects, enriches, and preserves Authoritative Person Context across Enterprise Journeys — independent of whether that person can yet authenticate (Identity, `C-001`), belongs to an organization (Membership, `C-007`), holds a role or permission, occupies a place in the enterprise structure, or has been granted access to anything.

## 2. Scope

`PE-001-C006`'s full capability architecture, per its own Chapter 2–4:

- **1 Capability Experience Blueprint** — `CRB-C006`
- **7 Enterprise Experience Blueprints (ERBs)** — `ERB-C006-01` through `ERB-C006-07`, answering the capability's own guiding architectural question (Establish, Understand, Distinguish, Review Duplicate, Correct, Enrich, Preserve/Hand-off)
- **12 Enterprise Experiences (EXs)** — `EX-C006-01` through `EX-C006-12`:
  1. Recognize Incoming Person Reference
  2. Establish New Person Context
  3. Understand Authoritative Person Context
  4. Distinguish Candidate Person Matches
  5. Resolve Conflicting Person Context
  6. Review Potential Duplicate Person Indication
  7. Correct Person Context
  8. Enrich Person Context
  9. Preserve Person Context Across Enterprise Journeys
  10. Hand Off Person Context to Identity Establishment
  11. Hand Off Person Context to Membership Establishment
  12. Continue from Person Context Decision
- **9 capability-specific Experience Contracts** (`5.1`–`5.9`)

Exact Business Activity decomposition, minimum-scope determination (if any), and the disposition of the pre-existing, currently unaudited `EX-C006-01`/`EX-C006-02` implementation (see §4 below) are **not decided by this charter** — they are `IRA-007`'s own determination, per this repository's own `IRA-005 §12`/`IRA-006 §12` precedent of scope decisions being made at the IRA stage, not the charter stage.

## 3. Out of Scope

Per `PE-001-C006 §1.4`, verbatim:

- **Identity Management (`C-001`)** — authentication, credentials, single sign-on, and how a person logs in (`URA-001`).
- **Membership Management (`C-007`)** — organizational authority, licenses, membership lifecycle (`URA-001`).
- **Role & Permission Management (`C-003`) and Access Management (`C-002`)** — authorization of any kind.
- **Enterprise Structure Management (`C-005`)** and enterprise structure/relationship semantics generally (`ERG-001`).
- **Workspace Management (`C-008`)** — workspace provisioning and composition.
- Business Activity execution, orchestration mechanics, workflow or state-machine implementation (`IMP-001` and owning specifications).
- Database, API, event, service, routing, component, or screen design.
- Capability identity, naming, and business-intent definition (`CAP-001`).

C-006 transfers preserved Person context at the ownership boundary; it does not act on another capability's behalf.

## 4. Dependencies

- **Primary Specification:** `URA-001` (Person/Identity/Membership semantics, per `ADR-001`).
- **Cross-Specification Dependency:** `ERG-001` — referenced only for Membership home-node placement, never redefined.
- **No dependency on any not-yet-built capability.** All of `C-006`'s own inputs already exist or are self-contained.
- **Unblocks two other uncharted capabilities.** `PE-001-C001` (Identity Management) and `PE-001-C008` (Workspace Management) each name Authoritative Person Context, produced by `C-006`, as a required, consumed Cross-Specification Dependency in their own Document Control sections. Neither can be soundly chartered ahead of `C-006` without building against a Person Context that has itself never been governed.
- **Disclosed pre-existing implementation (not part of this charter's authority, recorded for `IRA-007`'s attention):** `Backend/Services/AuthService/routers/person.py`, `services/person_recognition_service.py`, `services/establish_person_context_service.py`, `repositories/person_repository.py`, `repositories/identity_repository.py`, and `tests/test_person.py` already implement `EX-C006-01` (Recognize Incoming Person Reference) and `EX-C006-02` (Establish New Person Context), with passing tests. This code was committed `34cf7fe` (2026-07-20), one day before `WP-00` (`d5150ab`, 2026-07-21) — it predates this repository's entire IRA/Independent Certification/V&V governance discipline entirely, and was not named in `WP-00`/`WP-00A`'s own declared scope (`WPR-001`: *"None — predates the IRA/CERT governance process... no capability-specific ERB/EX/BR was implemented"*). It has never been through an IRA, never Independently Certified, never V&V Audited. This charter does not authorize reuse, modification, or removal of this code — `IRA-007` shall explicitly evaluate and disclose its disposition (reuse-and-certify against `PE-001-C006` v1.1, or rebuild) as part of its own Gap Analysis, since the code may target an earlier, uncorrected revision of the specification (`PE-001-C006`'s own Revision History records a 1.0→1.1 correction pass affecting recognition-authority wording).

## 5. Success Criteria

This Work Package shall be considered `CLOSED` only when:

- `IRA-007` is drafted per repository methodology (`METH-002`, `IMP-001`) and concludes **READY**.
- Every Business Activity `IRA-007` charters is implemented, unit and integration tested, and independently reviewed.
- The full five-gate `CLAUDE.md §19.7b` closure sequence passes: Independent Certification, Verification & Validation Audit, Remediation (if required) with Independent Verification, and Release Readiness Audit.
- Zero regressions against the full AuthService test suite.
- The pre-existing `EX-C006-01`/`EX-C006-02` implementation's disposition (§4) is explicitly resolved and disclosed in `IRA-007`, not silently inherited or silently discarded.
- All Technical Debt raised is recorded in `TECH-DEBT.md` per `CLAUDE.md §19.8`.
- `WPR-001` and `WP-REG-001` are updated to `CLOSED` status with the resolving commit hash.

## 6. Repository Authority

Chartered under Repository Owner authority, per this repository's own Work Package chartering precedent (`WP-01` through `WP-06`, each chartered by explicit Repository Owner instruction, recorded in `WPR-001`/`WP-REG-001`). This charter is a governance activity only.

**Implementation authority does not exist under this charter.** No source code, test, API, schema, migration, or design artifact may be created citing this document as authorization. Implementation authority begins only once `IRA-007` is drafted and concludes **READY**, and the Repository Owner explicitly instructs execution of the newly-ready Work Package — the same two-step gate (Charter → IRA-READY → explicit execution instruction) already applied to `WP-06`.

## 7. Governing Documents

`CAP-001` (capability identity and Business Intent) · `PE-001` (Enterprise Experience methodology) · `PE-001-C006_Person_Management.docx` v1.1 (governing Capability Specification) · `URA-001` (Primary Specification) · `ADR-001` (Primary Specification correction, `ERG-001` → `URA-001`) · `CLAUDE.md` (repository operating rules, §14/§16/§17/§18/§19) · `METH-002` / `ADR-017` (engineering methodology) · `IMP-001` (implementation playbook) · `WPR-001` (roadmap authority) · `WP-REG-001` (execution-status authority) · `DOC-000` (documentation register).

---

*This charter records that WP-07 exists and is authorized to proceed to the Implementation Readiness Assessment stage. It does not itself authorize implementation.*
