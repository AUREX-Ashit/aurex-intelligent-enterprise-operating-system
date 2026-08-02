# WP-10 — Configuration Management (C-041)

**Work Package ID:** WP-10
**Type:** Business Capability
**Capability ID / Name:** C-041 — Configuration Management
**Governing Capability Specification:** **No dedicated `PE-001-C041.docx` exists** — `docs/Product/PE-001/capabilities/` contains capability specifications through `C-040` only. Per `CAP-001_Enterprise_Capability_Registry.md` v1.5, C-041's own Primary Specification field names **SD-002** (`SD-002_Universal_Business_Object_Rules.md`), not PE-001. Direct verification confirms this division is real, not a documentation gap: `SD-002 §10` (`SD-002-077` through `085`, "Metadata, Configuration & Extensibility Rules") owns the *object pattern* every Configuration record follows (metadata-driven, tenant-configurable, versioned, audited — never hardcoded); `CMD-001 §12` owns the *canonical content* — six named Configuration Categories (Platform, Tenant, UI, Integration, AI, Notification) and the eight-tier Scope Hierarchy (Global Platform → Region → Country → Tenant → Enterprise → Business Domain → Business Object → User) already applied once in this repository's own history (Release A2's AI Preferences resolution, `TD-110`). This charter's own governing basis is therefore `SD-002 §10` + `CMD-001 §12`, jointly — not a single capability docx, disclosed here rather than silently assumed.
**Status:** CHARTERED
**Chartered By:** Repository Owner instruction ("Implementation Methodology v2.0 Establishment / WP-10 Planning Authorization"), 2026-08-02
**Chartering Date:** 2026-08-02
**Governing IRA:** `IRA-010_WP-10_Configuration_Management_Implementation_Readiness_Assessment.md` (created alongside this charter)

**This charter authorizes progression to the Implementation Readiness Assessment stage only. It does not itself authorize implementation.** Per this repository's own established precedent (WP-01 through WP-09's own charter documents), full-lifecycle implementation authority requires a separate, subsequent Repository Owner authorization after the IRA is reviewed and accepted.

---

## 1. Purpose / Business Objective

Per `CAP-001`'s own Business Intent for C-041, verbatim: **"Manage enterprise configuration."** Per `PRODUCT-MILESTONE-ROADMAP.md §3` (Milestone 1 — "The Configured Enterprise"): "Prove the platform reflects *this specific enterprise* — its name, language, branding, and accessibility needs — not a generic template." WP-10 is the primary carrier of this Business Objective — WP-09 (Workspace Management) delivered navigation; WP-10 is where an enterprise's own identity actually appears on screen.

## 2. Scope

Per `ARCHITECTURE-EVOLUTION-IMPLEMENTATION-PROGRAMME.md`'s own R16 classification and `SER-001`'s own `SE-011` umbrella entry, WP-10's own candidate scope consists of six facets, each independently traceable to `CMD-001 §12.3`'s own named Configuration Categories:

| Facet | `CMD-001 §12.3` Category | `SER-001` Entry | Independent of Release A? |
|---|---|---|---|
| Terminology | (spans Platform/Tenant, per `SD-002-079`'s own role/label metadata pattern) | `SE-012` | Yes |
| Branding (incl. dual-logo) | Platform Configuration ("Branding") | `SE-013` | Yes |
| Theme | UI Configuration ("Themes") | `SE-002` (accessibility modes) | Yes |
| Localization | Tenant Configuration ("Default Language") | (facet of `SE-011`) | Yes |
| Accessibility Profiles | UI Configuration | `SE-002` | Yes |
| AI Configuration | AI Configuration ("LLM Selection," "Embedding Model") | `SE-014` | Yes, contingent (see §5) |

**Which of these facets this Work Package is actually authorized to implement is determined by the accompanying IRA's own Gap Analysis (`IRA-010 §4`), not pre-decided here** — per this repository's own established charter/IRA separation of concerns (WP-01 through WP-09 precedent).

**Disclosed at chartering time, not deferred to IRA discovery:** two facets carry a known, pre-existing contingency, both already surfaced by prior governance passes in this repository, neither newly discovered here:

1. **Configuration Profiles** (a template/preset mechanism for the above facets, per `SD-002-085`'s own extensibility principle) has a soft dependency on two currently-unratified `SD-002` extensibility candidates (`SD-002-CANDIDATE-016`, Operating Model Templates; `SD-002-CANDIDATE-026`, Configuration Templates — `SER-001 SE-015`/`SE-016`). If unresolved at IRA time, this facet SHALL be explicitly scoped out rather than built against an unratified specification, per `IRA-RELEASE-A`'s own prior finding and `CLAUDE.md §20.6`'s own "no placeholder/unspecified functionality" discipline.
2. **Branding's own dual-logo support** has an unresolved specification gap — two source documents (`PRODUCT-MILESTONE-ROADMAP.md`, framing it as "contingent on a Repository Owner decision already flagged in the Roadmap"; `STRATEGIC-PLATFORM-CAPABILITY-TRACEABILITY-REPORT.md`, framing it as "not traceable to any document found... Blocked") disagree on whether this is spec'd-but-undecided or entirely unspecified. `IRA-010` SHALL determine which framing is accurate by direct primary-source verification, not assume either.

## 3. Business Activities

Not pre-specified in this charter. Per this repository's own established convention (`IRA-005 §12`, `IRA-007`, `IRA-008 §5`, `IRA-009 §5` — Business Activities are determined during Gap Analysis, not chartered in advance), the Business Activities this Work Package will realize are determined by `IRA-010 §5` (Plan A), against whichever facets that Gap Analysis finds in scope.

## 4. Out of Scope

- Any facet `IRA-010`'s own Gap Analysis excludes (§2 above).
- C-042 (Preference & Personalization) — a distinct, Planned capability (`SER-001 SE-036`); per `TD-110`'s own already-established resolution, user-level configuration is structurally accommodated within C-041's own existing Scope Hierarchy (`CMD-001 §12.6`, down to the User tier) without requiring C-042 to separately own any part of it — this charter does not reopen that determination.
- Enterprise Intelligence-dependent AI capability (model *behavior*, reasoning, orchestration) — C-041's own AI Configuration facet governs *which* vendor/model/embedding an enterprise selects (`CMD-001 §12.3`), never *what the selected AI does* (`EIA-001`/`RTA-001 §13`'s own exclusive ownership, unchanged).
- Any capability, screen, or navigation entry not already reachable through existing, established navigation (`admin-navigation.ts`, `config/workspaces.ts`) — no new top-level navigation area is authorized by this charter; extension of the existing shell only, per `CLAUDE.md §20.5`.
- Governed Workspace entry/switch/re-entry (`SER-001 SE-020`) — unrelated to this capability, remains WP-09's own disclosed exclusion.

## 5. Dependencies

Per `CMD-001 §12`/`SD-002 §10`: no other capability's own Business Object is consumed structurally (Configuration records are, by `SD-002-077`'s own principle, metadata records with no cross-capability foreign-key dependency in the way Membership depends on Organization, for example). The two contingencies named in §2 above are the only live dependencies:

- `SD-002-CANDIDATE-016`/`026` ratification decision (R7, Release A3) — soft dependency, Configuration Profiles facet only.
- Dual-logo specification clarification — soft dependency, Branding facet's own dual-logo element only; the remainder of Branding (single-logo, color palette, typography-within-DS-001's-own-bounds) is not affected.

**No dependency on `TD-111`/the Access Evaluation `TierResolver` gap exists anywhere in this charter's own scope** — unlike WP-08/WP-09, Configuration Management performs no governed authorization-adjacent transition; every facet is a self-referential, tenant/user-scoped configuration read/write, consistent with `CMD-001 §12.5`'s own "Tenant Scope: Mandatory" characteristic, not an Access-Evaluation-gated action.

## 6. Enterprise Experience Requirement (`CLAUDE.md §20`/`§21`)

This Work Package is chartered under both the Enterprise Experience Standard (`CLAUDE.md §20`) and Implementation Methodology v2.0 (`CLAUDE.md §21`, `METH-003`) — the first Work Package to be chartered under `§21`. Per `§21.3`'s own Standard Work Package Lifecycle, `IRA-010` SHALL include: a Strategic Enhancement Review (against `SER-001`), a Historical Screen Review (against `HISTORICAL-SCREEN-REALIZATION-MATRIX.md`), an Executive Cognition Review (against `EXECUTIVE-COGNITION-REALIZATION-STRATEGY.md`), and the dual-dimension Plan A (Business Capability)/Plan B (Enterprise Experience) `§20.6`'s own methodology already requires — worksheet per `ENTERPRISE-EXPERIENCE-REALIZATION-STRATEGY.md`.

## 7. Deliverables / Acceptance Criteria

Deliverables and acceptance criteria are scope-dependent and therefore determined by `IRA-010`'s own Readiness Decision (§8), not fixed here in advance — consistent with §3 above. At minimum, whatever scope is authorized shall meet every element of `CLAUDE.md §14`'s Definition of Done, including Independent Certification, Verification & Validation, and Release Readiness per `§19.7`/`§19.7b`, extended by `§20.7`/`§21`.

## 8. Risks

- **No dedicated capability specification exists** (§0/Governing Capability Specification, above) — the Gap Analysis rests on synthesizing `SD-002 §10` and `CMD-001 §12` directly, a different methodology from every prior Work Package's own "extract the PE-001-Cxxx docx" pattern. Disclosed, not treated as a blocker: both source documents are Locked/Active constitutional specifications with directly on-point content, per §0 above.
- **Two disclosed contingencies** (§2) may narrow the authorized scope at IRA time, mirroring WP-09's own precedent of a charter-time-disclosed narrowing later confirmed by the IRA's own Gap Analysis.
- **Largest facet count of any Work Package chartered to date** (six named facets) — `IRA-010` SHALL apply the same "Reuse → Configure → Extend → Compose → Create" discipline (`CLAUDE.md §19.5`) to each facet independently, avoiding treating "Configuration Management" as one undifferentiated Business Activity.

## 9. Technical Assumptions

- `theme.css` (`source/frontend/src/styles/`) exists today as a single, hardcoded `:root` block (91 lines) — no dark mode, no High-Contrast, no per-tenant variation. Confirmed via direct file read, not assumed.
- No terminology-override, localization/i18n, or branding-configuration infrastructure exists anywhere in the current frontend (confirmed via direct repository search) — this Work Package's own frontend implementation, whatever its final IRA-determined scope, begins from zero existing Configuration-specific frontend code for most facets, mirroring WP-09's own "begins from zero" precedent for its own backend.
- No backend Configuration Management service, model, or table exists anywhere in this repository (confirmed via repository-wide search) for any of the six named facets.

## 10. Architecture Impact

None anticipated pending `IRA-010`'s own Gap Analysis and `CMD-001 §26.3a` Business Object Eligibility Analysis. Every facet is already named within `CMD-001 §12.3`'s own existing Configuration Categories — no new category, no new canonical concept. Any new persisted construct (a Configuration record table) is subject to the same eligibility test every prior Work Package's own new tables have passed through, not assumed here.

## 11. Testing Strategy

Per `IMP-001 §11`, extended by `CLAUDE.md §21.4`'s own Mandatory Tenant-Isolation Test Checklist: every Configuration record carries `CMD-001 §12.5`'s own mandatory Tenant Scope — any new endpoint SHALL therefore include the two-tenant negative-control test class `§21.4` now requires as a submission gate, not a reactive audit finding, per `METH-003`'s own directly-evidenced lesson from `VV-AUDIT-WP-09`'s Finding 2.

## 12. Exit Criteria

Per `CLAUDE.md §19.7`/`§19.7b`/`§20.7`/`§21`: Business Activities realized (per the IRA's own final scope) marked Implementation Complete; Independent Certification passed; Verification & Validation Audit passed (or any finding remediated and independently re-verified); Release Readiness Audit passed; end-to-end demonstrability confirmed for whatever scope was authorized; Strategic Enhancement/Historical Screen/Executive Cognition Reviews completed per `§21.3`; repository committed. Only after all of the above may WP-10 be marked CLOSED. Per `CLAUDE.md §21.5`, one Repository Owner authorization executes this entire Work Package — not per-Business-Activity re-approval, mirroring the cadence WP-09's own success validated.

## 13. Repository Authority

Implementation authority does not exist under this charter alone. Per this repository's own established process, full-lifecycle execution requires the accompanying IRA to be accepted, followed by a separate, explicit Repository Owner authorization.

## 14. Governing Documents

- `SD-002_Universal_Business_Object_Rules.md §10` (Metadata, Configuration & Extensibility Rules — Primary Specification per `CAP-001`)
- `CMD-001_Canonical_Data_Model.md §12` (Configuration Categories, Scope Hierarchy — canonical content authority)
- `CAP-001_Enterprise_Capability_Registry.md` (C-041 registration)
- `DS-001 — AUREX Design System.md` (Theme system — for the Theme/Accessibility Profiles facets)
- `PRODUCT-MILESTONE-ROADMAP.md §3` (Milestone 1 — Business/Customer/Executive Value framing for this Work Package)
- `CLAUDE.md §16`–`§21` (canonical authority resolution, architectural change control, implementation checklist, Enterprise Experience Standard, Implementation Methodology v2.0)
- `METH-003_Implementation_Methodology_v2.md`, `SER-001_Strategic_Enhancement_Register.md`, `ENTERPRISE-EXPERIENCE-REALIZATION-STRATEGY.md`, `EXECUTIVE-COGNITION-REALIZATION-STRATEGY.md`, `HISTORICAL-SCREEN-REALIZATION-MATRIX.md` (companion planning artifacts this charter is chartered under)
- `WP-09`'s own Charter, `IRA-009`, `IMP-REPORT-WP-09` (precedent methodology, most recently proven)

---

*This charter records that WP-10 exists and is authorized to proceed to the Implementation Readiness Assessment stage. It does not itself authorize implementation.*
