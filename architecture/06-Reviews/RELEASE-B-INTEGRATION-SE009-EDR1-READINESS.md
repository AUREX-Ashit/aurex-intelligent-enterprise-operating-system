# Release B Integration, SE-009 Enterprise Experience Gate & EDR-1 Preparation

**Release:** Release B = [WP-09 (Workspace Management, C-008) → WP-10 (Configuration Management, C-041)] — Milestone 1, "The Configured Enterprise" (`PRODUCT-MILESTONE-ROADMAP.md §3`)
**Prepared by:** Implementing session (Claude Code), per Repository Owner Instruction "Release B Integration, Certification & EDR-1 Preparation"
**Scope of this document:** Phase 1 (Release B Integration), Phase 2 (SE-009 Enterprise Experience Gate), Phase 5 (EDR-1 Preparation) — the three phases this instruction frames as direct validation/remediation work, as distinct from Phase 3 (Independent Release B Certification) and Phase 4 (Independent Release B Readiness Assessment), each performed separately by a fresh-context, independent reviewer per this repository's own established `CLAUDE.md §19.7`/`§19.7b` discipline (self-certification is prohibited; the implementing session may validate and remediate, but may not certify its own work).
**Date:** 2026-08-02

---

## Phase 1 — Release B Integration

### 1.1 End-to-end workflows

BA-01 (Resolve Enterprise Configuration) and BA-02 (Establish/Update Enterprise Configuration) form a real, working end-to-end loop, independently re-verified this pass by direct code read: `POST /configuration` (BA-02) writes a versioned `ACTIVE` row; `GET /configuration` (BA-01) resolves it ahead of the Platform Default on the very next call, for the caller's own `X-Tenant-ID`-matched Organization only (Finding B-1's own remediation, `require_matching_tenant_or_platform_admin`). No mocked or stubbed step anywhere in this loop. **Status: Working.**

### 1.2 Configuration → Workspace integration

Investigated directly: WP-09's own `WorkspaceSwitcher.tsx` does not switch between different tenant Organizations — its "Workspaces" are static admin nav-item groupings within the *same* `PLATFORM_ADMIN` session (`config/workspaces.ts`, unchanged since WP-09; `IRA-009 §7`'s own disclosed "fallback/seed only" design, not a per-tenant switch). A genuine cross-tenant Organization change happens only at login (`OrganizationSelectionResponse`), which is a full session remount, not an in-place switch. `useResolvedTheme`'s own dependency (`session.status === "authenticated"`) therefore correctly re-resolves Configuration exactly once per authenticated session — there is no code path today where a caller's own effective Organization changes without a full remount, so no stale-Configuration-after-switch defect exists. **Status: No integration defect found** — the initially-suspected "Configuration doesn't refresh on Workspace switch" concern does not apply, because "switching Workspace" does not currently cross a tenant boundary at all.

### 1.3 Enterprise terminology / Branding

Confirmed by direct search (`grep` across `source/frontend/src` for any reference to the Configuration resolution API or types outside the Configuration feature module itself): **no screen anywhere in the platform consumes resolved Terminology, Branding, Accessibility, or Localization** — only Theme is consumed platform-wide (via `AdminShell`). This exactly matches `TD-117`'s own already-disclosed scope boundary from WP-10's own closure; not a new finding. See §5 (EDR-1 demonstration-scenario impact) below for why this specifically matters for EDR-1's own script, distinct from Release B integration correctness.

### 1.4 Theme integration

**Status: Working, and improved this pass.** `AdminShell.tsx` resolves and applies Theme platform-wide on every `/platform-admin/(workspace)` route via `useResolvedTheme`. One real gap found and remediated: establishing a new `THEME` override via the admin screen (`EstablishConfigurationSection.tsx`) previously had no visible effect until the next full page reload — `useResolvedTheme` only resolves once per session mount, and nothing re-applied the theme after a successful establish. Fixed in `useConfigurationManagement.ts`'s own `establish()`: on a successful `THEME`/`theme_class` establishment, the new value is applied to `document.documentElement` immediately, giving the same instant confirmation every other establish-type action in this codebase already provides (`CLAUDE.md §20.6`'s own confirmation-state requirement). Verified via `tsc --noEmit` (0 errors) and `eslint` (0 problems). This is a small, targeted UX-completeness fix to an already-existing capability, not a new capability.

### 1.5 Navigation / Enterprise Shell

**Status: Working.** WP-10 reuses the pre-existing `system-configuration` nav item/route rather than adding a new one (confirmed via `git show` at WP-10's own closure). `AdminShell` is the single, unmodified-in-structure shell both WP-09 (Workspace Switcher in `GlobalHeader`) and WP-10 (Theme resolution) now integrate into — one Enterprise Shell, not two parallel ones.

### 1.6 Executive Experience / Discover First / Evidence First

- **Executive Experience:** Neither WP-09 nor WP-10 charters an Executive-persona-specific screen (both are Discover-stage, platform-administration-facing capabilities per `IRA-009`/`IRA-010`); no gap relative to either charter's own disclosed scope.
- **Discover First:** WP-10's `ConfigurationManagementScreen` shows the Entries list (what already exists) *before* the Establish form (what could be added) — the same "see what exists, then act" ordering principle, though not the literal "search-then-establish" pattern `SE-003` names (Configuration establishment is a direct value-set, not a candidate search — there is no external entity to search for). `SE-003` itself (extending Discover-First to Membership/Organization Node) remains `Unassigned WP`/Deferred in `SER-001` — not WP-09's or WP-10's own scope; see §5.4 below.
- **Evidence First:** Not applicable — neither capability produces AI-originated content requiring an evidence citation.

**Phase 1 conclusion:** one real integration/UX gap found (Theme establish not applying live) and remediated. No other blocking integration issue found.

---

## Phase 2 — SE-009 Enterprise Experience Gate

`SE-009` (`SER-001` §1): "Enterprise Experience Gate for EDRs — a lightweight checklist appended to Gate 5 for demonstration releases. Ensure every Enterprise Demonstration Release meets a baseline UX bar before showing customers." This is the first execution of `SE-009` anywhere in this repository — no prior template exists; the checklist below is constructed directly from this instruction's own Phase 2 item list, scoped to Release B's own delivered surface (WP-09 + WP-10 and their integration into the pre-existing Enterprise Shell), not a full re-audit of WP-01 through WP-08 (each already independently certified through its own five-gate sequence).

| Dimension | Finding |
|---|---|
| **Enterprise Experience** | Theme resolution is genuinely enterprise-differentiating (an Organization's own established Theme renders platform-wide). Terminology/Branding/Accessibility/Localization are not yet consumed anywhere (§1.3) — a real Enterprise Experience *completeness* gap relative to the Roadmap's own Milestone 1 description, not a defect in what was actually chartered (`TD-117`, already disclosed). |
| **Executive Experience** | Not chartered for either WP-09 or WP-10 — no gap relative to scope. |
| **Design System (DS-001) compliance** | `theme.css`'s four new `[data-theme]` blocks realize `DS-001-193`'s own Theme Model. The Accessibility facet's `high_contrast_enabled` key duplicates a mode `DS-001-193`'s own `HIGH_CONTRAST` Theme class already provides, and the actually-required `DS-001-194` modes (reduced-motion, large-text) remain unimplemented anywhere platform-wide — already disclosed as `TD-119` (High severity, non-blocking) at WP-10's own Gate 2 V&V Audit. Not re-raised as a new item here. |
| **Screen consistency** | `ConfigurationManagementScreen` reuses the exact same `Card`/`Button`/`Input`/`Table`/`FormField`/`StatusBadge`/`LoadingState` component set every other platform-admin screen uses — no parallel/bespoke styling introduced. |
| **Navigation** | Confirmed no new nav item was added; the pre-existing `system-configuration` entry was reused (§1.5). |
| **Accessibility** | Shared components (`Menu`, `Sidebar`, `Input`) carry proper ARIA roles/labels (`role="menu"`/`"menuitem"`, `aria-haspopup`, `aria-expanded`, `aria-current`, `aria-invalid`, `nav aria-label`) — confirmed by direct grep of `components/ui/*.tsx`; WP-10's own screens inherit this by reuse, introducing no new accessibility regression. True reduced-motion/large-text modes remain unimplemented platform-wide (`TD-119`, already disclosed, not new). |
| **Branding** | Core/single-logo establishable and resolvable; not yet rendered by `GlobalHeader` (`TD-117`, already disclosed). Dual-logo/White-label remain excluded per `IRA-010 §4.3`'s own disclosed, DS-001-unspecified basis. |
| **Discoverability** | The Establish form's own Facet/Key selection uses closed-set toggle buttons (mirroring `EstablishMembershipSection`'s own precedent) rather than free-text guessing — a caller cannot select an invalid Facet/Key combination for the four structured facets. |
| **Progressive Disclosure** | `SE-001` (the four-state Summary/Details/Evidence/Audit History contract) remains `Unassigned WP`/Deferred platform-wide — zero conforming components exist anywhere in the repository, including in WP-09/WP-10 (`ConfigurationEntriesSection` is a flat table, the same disposition every prior WP's own data list has). Not a WP-10-specific gap; a pre-existing, repository-wide, already-disclosed deferral, unchanged by this Release. |
| **Executive usability** | N/A — no Executive-facing screen chartered in Release B. |
| **AI interaction** | N/A — neither capability involves AI-originated content. |
| **Overall product quality** | Both capabilities are real, tested, and demonstrable end-to-end (not mocked or stubbed). The gap between the Roadmap's own aspirational Milestone 1 "Enterprise Experience Delivered" description and what was actually chartered/built (§5.4) is the most consequential finding of this Gate — not a quality defect in the code that exists, but a scope-accuracy question the Repository Owner should resolve before EDR-1's own script is finalized. |

**Blocking issues found: none.** No remediation beyond §1.4's Theme-live-apply fix was required or performed.

---

## Phase 5 — EDR-1 Preparation

`PRODUCT-MILESTONE-ROADMAP.md §3`'s own Milestone 1 entry names four **Expected Demonstration Scenarios**. Each is validated against the platform's actual, current capability — not assumed:

### 5.1 "Switch workspaces"

**Demonstrable.** `WorkspaceSwitcher` (WP-09) works as built and certified.

### 5.2 "Show the same screen rendered with a different enterprise's terminology, colors, and theme"

**Partially demonstrable.** *Colors/Theme*: fully demonstrable and now live (§1.4) — establish a `THEME` override for one Organization via the admin screen and the platform visibly re-themes immediately. *Terminology*: **not demonstrable as scenario-scripted** — no screen anywhere renders a resolved Terminology override; only the Configuration admin screen itself can establish one (§1.3/`TD-117`). A live demo script naming "a different enterprise's terminology" rendered on "the same screen" cannot be performed today outside the admin establish/list screen itself.

### 5.3 "Demonstrate an accessibility mode live"

**Demonstrable, via a different mechanism than the Accessibility facet's own literal keys.** `TD-119` (WP-10 Gate 2) already found that `high_contrast_enabled` duplicates Theme's own `HIGH_CONTRAST` class, and that neither reduced-motion nor large-text (the actually-`DS-001-194`-required modes) is implemented anywhere. **Recommendation for the EDR-1 script:** demonstrate the accessibility-adjacent mode via `THEME = HIGH_CONTRAST` (fully live, per §1.4's own fix), not via the Accessibility facet's own `high_contrast_enabled` key (establishable, but its effect is currently identical to, not distinct from, the Theme mechanism already being demonstrated in §5.2).

### 5.4 "Show a saved, named view of a filtered list"

**Not demonstrable — out of Release B's own actually-chartered scope.** `SER-001` records `SE-004` (Saved Views) as `Release B`-timeframe but `Unassigned WP`, Deferred — neither `IRA-009` nor `IRA-010` ever claimed this scope, and neither Work Package's own Implementation Report was obligated to address it (confirmed: `IMP-REPORT-WP-09`/`IMP-REPORT-WP-10` correctly do not mention `SE-001`/`SE-003`/`SE-004`, since none was allocated to either WP). **This is a Product Milestone Roadmap description-accuracy gap, not an implementation defect in WP-09 or WP-10** — the Roadmap's own Milestone 1 "Enterprise Experience Delivered" bullet names Saved Views and Discover-First parity (`SE-003`) as delivered outcomes of Release B, but neither was ever chartered into either of Release B's own two Work Packages. Building `SE-004` now would require implementing a new, unchartered capability, which this instruction's own Phase 5 explicitly prohibits ("Do NOT implement new capabilities").

### 5.5 Cohesiveness assessment

The platform presents as a single, coherent Enterprise Operating System for every scenario within Release B's own actually-chartered scope: one Enterprise Shell, one navigation model, one Theme system now demonstrably live end-to-end, one Workspace switcher. The scenarios that are *not* demonstrable (5.2's Terminology half, 5.4 entirely) are not incoherence — they are capabilities the Roadmap's own aspirational description named but that were never actually allocated to a chartering Work Package. This is a scripting/scoping decision for the Repository Owner, not a platform defect: **either descope EDR-1's own demonstration script to the four scenarios above minus the unbuilt Terminology/Saved-Views elements, or treat their absence as a disclosed, accepted limitation of this specific demonstration.**

---

## Summary of findings carried into governance (Phase 6)

1. **Remediated this pass:** Theme establish now applies live (`useConfigurationManagement.ts`) — closes §1.4/§5.2's own gap.
2. **Disclosed, not remediated (out of Release B's own chartered scope, "do not implement new capabilities"):** `SE-004` (Saved Views) and `SE-003` (Discover-First parity extension) remain `Unassigned WP`/Deferred — the Product Milestone Roadmap's own Milestone 1 "Enterprise Experience Delivered" description should be corrected or the Repository Owner should explicitly accept this gap before EDR-1's own script is finalized.
3. **No new Technical Debt entries required** — every gap found either was already disclosed (`TD-117`, `TD-119`) or is a Roadmap-description accuracy question, not an implementation defect, carried forward as a Phase 6 governance note rather than a code-level TD entry.
4. **No blocking defect found** in Phase 1 or Phase 2. Release B Integration and the SE-009 Enterprise Experience Gate are both complete.
