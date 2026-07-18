# DS-001: AUREX Design System
### Version 1.0 — RELEASED

**Status:** RELEASED — Version 1.0, Constitutional Baseline Published (Chapters 1–22). See "DS-001 — Version and Release Record" for the governing release record.
**Scope:** Defines the canonical visual language of AUREX, the Intelligent Enterprise Operating Center, across every presentation surface of the Enterprise Intelligence Fabric.
**Companion documents:** SD-001 (Enterprise Presentation Architecture), SD-002 (Universal Business Object Rules), SD-003 (Enterprise Interaction Laws), ERG-001 (Enterprise Relationship Graph)
**Governing framework:** ARCH-000 — Enterprise Operating System Architecture Manifest

---

## Document Architecture (Frozen)

The scaffolding below was established through iterative architectural review and is now frozen. Chapters are authored progressively against this scaffolding; the scaffolding itself does not change without a new round of architectural review.

### Table of Contents

1. Purpose, Vision & Scope
2. Relationship to SD-001
3. Design Principles
4. Brand Identity & Product Branding
5. Logo System
6. Color System
7. Typography
8. Iconography
9. Illustration Standards
10. Design Tokens
11. Theme Architecture (Light / Dark / High-Contrast / Boardroom / White-label)
12. White-Label Branding & Multi-Brand Token Mapping
13. Component Visual Standards
14. AUREX Domain Visual Language
    14.1 Evidence Visual Standards
    14.2 Confidence Visual Standards
    14.3 Explainability Visual Standards
    14.4 AI-Generated Content Visual Standards
    14.5 Recommendation Visual Standards
    14.6 Knowledge Graph Visual Standards
    14.7 Enterprise Relationship Visual Standards
    14.8 Business Activity Visual Standards
    14.9 Decision Support Visual Standards
    14.10 Risk Indicator Visual Standards
    14.11 Trust Indicator Visual Standards
15. Motion Language & Animation Standards
16. Responsive Visual Behaviour
17. Accessibility Styling
18. Dashboard, Chart & Data Visualization Language
19. Empty State Design
20. Loading Experience
21. Notification Styling
22. Design Governance
    22.1 Design Review Process
    22.2 Token Governance
    22.3 Component Governance
    22.4 Contribution Process
    22.5 Approval Workflow
    22.6 Versioning Strategy
    22.7 Deprecation Policy
    22.8 Compatibility Policy
    22.9 Migration Guidance
    22.10 Release Management
23. Appendix A: Token Reference Tables
24. Appendix B: Component Visual Spec Sheets
25. Appendix C: Cross-Reference Index to SD-001 / SD-002 / ERG-001

Chapter 14 is named for the AUREX platform rather than for any single capability so that it remains extensible to domain concepts not yet defined, without requiring renumbering.

### Ownership Matrix

| Topic | Owner | Boundary note |
|---|---|---|
| Brand Identity, Product Branding, Logo System | **DS-001** | Not addressed anywhere in SD-001 (§1.3: SD-001 "intentionally avoids prescribing visual design"). |
| Typography, Color System, Iconography, Illustration Standards | **DS-001** | `SD-001-062` (color never the only indicator) and `SD-001-066` (icon cultural neutrality) are behavioral rules SD-001 keeps; DS-001 owns the palette/icon set that satisfies them. |
| Design Tokens | **DS-001** | Full token taxonomy defined here; no equivalent exists in SD-001. |
| Theme Architecture, White-label Branding | **DS-001** (visual) / **SD-002** (tenant config) | `SD-002-CANDIDATE-013` reserves the tenant metadata for which theme/brand is active. DS-001 owns the token sets and visual assets that metadata selects. |
| Component Visual Standards | **DS-001** (look) / **SD-001** (behavior) | SD-001 §5 owns widget metadata and behavior. DS-001 owns how each component renders. |
| Motion Language, Animation Standards | **DS-001** (spec) / **SD-001** (when) | `SD-001-056` mandates lower motion for Sacred 12 as a behavioral rule. DS-001 owns the easing/duration tokens and choreography. |
| Responsive Visual Behaviour | **DS-001** (visual) / **SD-001** (structural) | SD-001 §11 owns what must never be hidden at small viewports (`SD-001-071`). DS-001 owns the breakpoint/spacing token behavior. |
| Accessibility Styling | **DS-001** (implementation) / **SD-001** (mandate) | SD-001 §10 mandates that accessibility modes exist (`SD-001-063`). DS-001 owns the token values for each mode. |
| Dashboard Visual Standards, Chart Styling, Data Visualization Language | **DS-001** | Not addressed in SD-001 beyond "Dashboard" as a named layout-template slot (`SD-001-024`, structural only). |
| Empty State Design | **DS-001** (visual) / **SD-001** (behavior) | `SD-001-025/041` mandate that an empty state be actionable. DS-001 owns its visual treatment. |
| Loading Experience | **DS-001** (visual) / **SD-001** (behavior) | `SD-001-026/077-083` mandate progress %, ETA, and performance budgets. DS-001 owns skeleton/spinner/progress-bar styling. |
| Notification Styling | **DS-001** | Not addressed in SD-001. |
| Design Governance | **DS-001** | Applies the versioning/deprecation discipline SD-001 already established for screens/widgets (`SD-001-023`, `SD-001-110`) to tokens and components. |
| Evidence, Confidence, Explainability, AI-generated content, Recommendations, Decision Support, Risk/Trust Indicators — *visual treatment* | **DS-001** (visual) / **SD-001** (behavior) | SD-001 §3–4 owns the governing rules (six-step resolution sequence, disclosed confidence formula, no-black-box-conclusions, delegated-authority trust thresholds). DS-001 owns only how these render. It never restates or alters the confidence formula, resolution sequence, or delegation model. |
| Business Activities — *visual treatment* | **DS-001** (visual) / **SD-002 §5** (business object) + **SD-001-009** (behavior) | SD-002 defines Business Activity as a governed business object type. DS-001 owns only the Business Activity Card's visual rendering. |
| Knowledge Graphs, Enterprise Relationships — *visual treatment* | **DS-001** (visual) / **SD-002-013** + **ERG-001** (structural) | SD-002-013 and ERG-001 both claim structural ownership of relationship/graph modeling — a pre-existing question between those two documents, not resolved or duplicated here. DS-001 owns only node/edge/graph visualization styling. |
| Enterprise Intelligence (generation/interpretation) | **EIA-001** *(referenced, not yet authored — per ARCH-000)* | Open dependency: Chapter 14's visual standards for AI-generated content and Enterprise Intelligence artifacts are written against current SD-001 principles only, and must be re-checked once EIA-001 is authored. |

**Confirmed excluded from DS-001** (owned by SD-001, no action needed): Presentation Architecture, Screen Architecture, Navigation Architecture, Widget Metadata, Layout Metadata, Guided Completion, Evidence Presentation, Question Engine, Adaptive Experience, Presentation Behaviour, Performance Architecture, Localization Architecture, Marketplace Architecture, Future Platform Architecture.

### Component Catalogue

Canonical taxonomy — valid independent of implementation status.

- **Foundation Components** — Button, Input Field, Select, Checkbox, Radio, Toggle/Switch, Textarea, Label, Icon, Avatar, Badge, Tag/Chip, Divider, Tooltip
- **Layout Components** — Card, Panel, Modal/Dialog, Drawer, Grid, Container, Section, Accordion, Tabs, Splitter/Resizable Pane
- **Navigation Components** — Navigation Shell, Breadcrumb, Menu, Sidebar, Pagination, Stepper, Command Palette
- **Interaction Components** — Form, Search Bar, Filter Bar, Bulk Action Row, Saved View Selector, Notification/Toast, Progress Indicator, Loading Indicator, Empty State
- **Enterprise Intelligence Components** — Guided Completion Card, Question Engine Prompt, Business Activity Card, Action Center, DNA-Adaptive Rendering Surface
- **Evidence Components** — Evidence Panel, Confidence Indicator, Explainability Panel, Source Citation, Audit Trail Viewer, Conflict/Discrepancy Indicator
- **Visualization Components** — Chart Primitives (bar, line, trend, waterfall), Risk Matrix, Coverage Card, Timeline, Heatmap, Data Table, Sparkline, KPI/Stat Tile, Knowledge Graph Renderer
- **Collaboration Components** — Comment Thread, Mention, Assignment Panel, Approval Queue, Activity Feed
- **Executive Components** — Executive Header, Strategic Narrative Card, Executive Summary Tile, Boardroom Display Card, Consequence Statement

### Design Token Catalogue

Taxonomy only — category and purpose, no values.

| Token Category | Governs |
|---|---|
| Brand Tokens | Canonical brand-identity values that seed every other category |
| Color Tokens | Semantic and raw color values (surface, text, border, interactive) |
| Typography Tokens | Font family, scale, weight, line-height, letter-spacing |
| Spacing Tokens | Base spacing scale (padding, margin, gap) |
| Sizing Tokens | Component dimension scale |
| Radius Tokens | Corner-rounding scale |
| Border Tokens | Border width and style scale |
| Elevation Tokens | Layering/depth scale |
| Shadow Tokens | Shadow definitions bound to elevation |
| Opacity Tokens | Transparency scale (disabled, overlay, scrim) |
| Motion Tokens | Duration and easing-curve primitives |
| Animation Tokens | Named animation sequences composed from motion tokens |
| Transition Tokens | State-change transition definitions (hover, focus, expand/collapse) |
| Icon Tokens | Icon sizing, stroke-weight, grid alignment |
| Grid Tokens | Layout grid column/gutter/margin definitions |
| Breakpoint Tokens | Responsive viewport thresholds |
| Z-Index Tokens | Stacking-order scale |
| Focus Tokens | Focus-ring style and offset (accessibility) |
| Cursor Tokens | Pointer/cursor state definitions |
| Illustration Tokens | Illustration style, palette, sizing constraints |
| Chart Tokens | Data-visualization-specific color, spacing, typography values |
| AI Tokens | AI-specific visual semantics — how AI-originated content, confidence, and reasoning state are visually distinguished from human-entered or system-verified content |
| Semantic Tokens | Purpose-named tokens (success/warning/danger/info) mapping to raw values |
| State Tokens | Interaction-state values (default/hover/active/disabled/selected/loading) |

### Freeze Statement

The document architecture above — Table of Contents, Ownership Matrix, Component Catalogue, and Design Token Catalogue — is frozen as of this version. Chapter content is authored progressively against this scaffolding. Any future change to the scaffolding itself requires a new round of architectural review, not a silent edit during chapter authoring.

---

## SECTION 1: Purpose, Vision & Scope

### 1.1 Purpose

This document defines the canonical Visual Language of AUREX, the Intelligent Enterprise Operating Center delivered by the CorpStage Enterprise Operating System.

It establishes the brand identity, color system, typography, iconography, design tokens, theme architecture, component visual standards, and domain-specific visual language through which every presentation surface governed by SD-001 (Enterprise Presentation Architecture) is rendered.

DS-001 does not define what is presented, how screens behave, what business objects exist, or how users interact with the platform — those are the exclusive responsibility of SD-001, SD-002, and SD-003 respectively, as recorded in the Ownership Matrix above. DS-001 defines only how the platform looks: the single visual system through which those architectures become visible, legible, and recognizable as one product, regardless of screen, device, tenant, or white-label configuration.

### 1.2 Vision

Enterprise Intelligence is only as trustworthy as it is legible. A platform that presents evidence-driven, explainable, governed intelligence through an inconsistent, ad hoc, or visually noisy surface undermines the very trust SD-001's Presentation Architecture exists to build.

AUREX exists to make that trust visible at a glance — through one coherent visual system, applied without exception, across every screen, every device, every tenant, and every white-label deployment the Enterprise Operating System serves.

The AUREX visual language is founded on the same architectural discipline that governs the rest of the Enterprise Operating System:

One visual system, infinite tenants — a color, type, and token system that supports unlimited white-label and multi-brand configurations without ever forking the underlying design system, consistent with SD-001's platform-adaptation principle (`SD-001-033`) applied to appearance rather than behavior.

Calm by default, urgent by exception — visual intensity is reserved for what genuinely requires attention; executive surfaces render with deliberately lower saturation and motion than operational surfaces, in direct visual service of `SD-001-056`.

Evidence made visible, not just present — confidence, provenance, and AI-origination are never ambiguous; the AUREX Domain Visual Language (Chapter 14) exists specifically so that evidence-backed intelligence is visually distinguishable from unverified or AI-generated content at a glance, without requiring a click to find out.

Accessible without exception — every color, type, and motion decision is made within the accessibility mandates SD-001 §10 establishes, never around them.

One token, every surface — nothing in AUREX is a one-off visual decision; every color, space, radius, shadow, and motion value traces back to a governed design token, so that a single change propagates consistently rather than requiring surface-by-surface rework.

### 1.3 Scope

DS-001 governs every visually rendered surface of the Enterprise Intelligence Fabric, across both presentation layers defined by SD-001 §8 (Layer 1 Operational Intelligence and Layer 2 Executive Cognition), including but not limited to:

Brand identity and product branding
Logo systems and white-label brand variants
Color systems and semantic color mapping
Typography and type scale
Iconography and illustration
The complete design token taxonomy
Theme architecture, including light, dark, high-contrast, boardroom, and white-label themes
Component visual standards, for every category in the Component Catalogue above
The AUREX Domain Visual Language governing evidence, confidence, explainability, AI-generated content, recommendations, knowledge graphs, enterprise relationships, business activities, decision support, and risk and trust indicators
Motion and animation
Responsive visual behaviour
Accessibility styling
Dashboard, chart, and data visualization styling
Empty state, loading, and notification visual design
Governance of the design system's own lifecycle — review, versioning, deprecation, and release

DS-001 does not prescribe presentation architecture, screen structure, navigation models, business object definitions, interaction behavior, or enterprise intelligence generation. Where a topic sits at the boundary between visual form and governed behavior, the Ownership Matrix above is the authoritative resolution, and DS-001's chapter on that topic references — rather than restates — the owning document's rule.

Consistent with SD-001-104/105/106, DS-001 is independent of any specific AI provider, reporting framework, or industry. It is not independent of the platform's own architecture: every visual standard in this document exists to render SD-001, SD-002, SD-003, and ERG-001 faithfully, never to reinterpret them.

---

*End of Chapter 1.*

---

## SECTION 2: Relationship with SD-001

This chapter is the canonical boundary contract between SD-001 (Enterprise Presentation Architecture) and DS-001 (AUREX Design System). Every future architectural or implementation decision touching both documents shall be resolved by reference to this chapter, not by independent judgment.

### 2.1 Purpose

SD-001 and DS-001 exist as two documents, not one, because they govern two architecturally distinct concerns that must remain independently evolvable.

SD-001 governs what a screen is, what it contains, how it behaves, and what it must never hide. It answers questions of structure, metadata, sequencing, and governance. It was written, and remains valid, without any reference to color, typography, or visual form — SD-001 §1.3 states this explicitly: the Presentation Architecture "intentionally avoids prescribing visual design, user interface technology, or implementation frameworks."

DS-001 governs how that same screen looks, feels, and is visually experienced. It answers questions of color, type, token, theme, motion, and visual rendering. DS-001 has no authority over what appears on a screen, only over how what SD-001 places there is rendered.

Separation is constitutional, not organizational. A single merged document would force every future change — a new brand color, a new screen anatomy — through one document's governance process, coupling concerns that have no reason to change together. Two documents allow SD-001 to evolve platform behavior and DS-001 to evolve platform appearance independently, each under its own review discipline, without either blocking the other.

**DS-001-001: Two Documents, One Architecture, No Overlap**
SD-001 and DS-001 together form one constitutional architecture for everything a user sees. Neither document is complete without the other, and neither document may be read as authoritative for the concern the other owns. Any requirement that appears to require both a structural and a visual answer shall be split across both documents rather than answered wholly within one.

### 2.2 Architectural Relationship

SD-001 and DS-001 are complementary, not competing, architectures. SD-001 defines the Enterprise Presentation Architecture: the structural and behavioral contract for every screen, widget, and interaction surface. DS-001 defines the AUREX Design System: the visual language through which that structural contract is rendered.

Neither document duplicates the other. Where SD-001 states that a widget is collapsible, movable, and independently addressable metadata (`SD-001-017`), DS-001 states nothing about whether a widget may be collapsed or moved — it states only what a collapsed, expanded, hovered, or focused widget looks like. Where SD-001 states that every empty state must be actionable (`SD-001-025`), DS-001 states nothing about what action an empty state must offer — it states only how that empty state is visually composed.

This relationship is asymmetric in one respect: SD-001 can be fully specified without DS-001 (a screen's structure and behavior are complete descriptions on their own), but DS-001 cannot be meaningfully authored without SD-001, because DS-001's chapters exist to render surfaces SD-001 has already defined. DS-001 is therefore a downstream, consuming architecture with respect to SD-001, while remaining a peer constitutional document within ARCH-000's Layer 1 classification.

### 2.3 Ownership Principles

The boundary between SD-001 and DS-001 is governed by six constitutional distinctions. Every future ownership question shall be resolved by applying these distinctions in order.

**DS-001-002: Structure vs. Appearance**
SD-001 owns structure — what elements exist on a screen, in what arrangement, in what hierarchy. DS-001 owns appearance — how each structural element is colored, sized, spaced, and styled. A screen's structure remains identical whether rendered in the Light or Dark theme; only its appearance changes.

**DS-001-003: Behaviour vs. Visual Language**
SD-001 owns behaviour — what happens when a user acts, what sequence a screen follows, what a widget does. DS-001 owns visual language — the vocabulary of color, iconography, and motion through which behaviour is made perceivable. DS-001 shall never define a new behaviour to justify a visual effect; if a visual requirement implies a new behaviour, the behaviour shall be specified in SD-001 first.

**DS-001-004: Metadata vs. Tokens**
SD-001 owns metadata — the structural records (`screen_code`, `widget_code`, `widget_type`) that define what a screen or widget is. DS-001 owns tokens — the design constants (color, spacing, radius, motion values) that define how metadata-defined elements render. A widget's metadata is identical across every tenant; only the token values resolved for that tenant's theme differ.

**DS-001-005: Navigation vs. Branding**
SD-001 owns navigation — the menu structure, route hierarchy, and navigation metadata (`SD-001-018`). DS-001 owns branding — the logo, brand color, and product identity displayed within that navigation structure. DS-001 shall never define which items appear in a navigation tree, only how the navigation surface is visually branded.

**DS-001-006: Rendering Rules vs. Design Rules**
SD-001 owns rendering rules — the conditions under which content appears, is hidden, or changes (progressive disclosure levels, DNA-adaptive rendering, escalation visibility). DS-001 owns design rules — the visual treatment applied once SD-001 has determined that content should render. DS-001 shall never override an SD-001 rendering condition to achieve a visual outcome.

**DS-001-007: User Experience Behaviour vs. Visual Experience**
SD-001 owns the User Experience Behaviour — how a user's journey through Guided Completion, approval, or evidence review proceeds. DS-001 owns the Visual Experience — the calm, consistent, brand-coherent surface that journey is experienced through. A user's path through a business activity does not change between tenants; the visual surface of that path does.

### 2.4 Ownership Matrix

| Topic | Owner | Supporting Document | Reason |
|---|---|---|---|
| Screen Architecture | SD-001 | SD-001 §5, §7 | Screen anatomy, zones, and structure are structural/behavioral, not visual. |
| Layout | SD-001 | SD-001 §5 (`SD-001-016`, `SD-001-024`) | Layout templates are structural metadata; DS-001 supplies only the spacing/grid tokens a layout consumes, never the layout's existence or selection. |
| Widgets | SD-001 | SD-001 §5 (`SD-001-017`) | Widget metadata, behavior, and composability are SD-001's; DS-001 governs only a widget's visual rendering (Chapter 13). |
| Metadata | SD-001 | SD-001 §5, §7 | All structural metadata belongs to SD-001; DS-001 has no metadata layer, only token definitions. |
| Navigation | SD-001 | SD-001 §5 (`SD-001-018`) | Navigation tree and route metadata are SD-001's exclusively; DS-001 governs only navigation-surface branding. |
| Design Tokens | DS-001 | DS-001 Ch. 10 | No equivalent construct exists in SD-001. |
| Themes | DS-001 (visual) / SD-002 (selection) | DS-001 Ch. 11; `SD-002-CANDIDATE-013` | Theme token sets are DS-001's; which theme a tenant is assigned is SD-002 tenant configuration. |
| Typography | DS-001 | DS-001 Ch. 7 | Not addressed in SD-001. |
| Color System | DS-001 | DS-001 Ch. 6 | SD-001 retains only the behavioral rule that color is never the sole indicator (`SD-001-062`); the palette itself is DS-001's. |
| Motion | DS-001 (spec) / SD-001 (when) | DS-001 Ch. 15; `SD-001-056` | SD-001 mandates when motion must be reduced (Sacred 12); DS-001 defines the actual easing/duration values. |
| Components | DS-001 (visual) / SD-001 (behavior) | DS-001 Ch. 13; SD-001 §5 | Same behavior/appearance split as Widgets. |
| Charts | DS-001 | DS-001 Ch. 18 | Not addressed in SD-001 beyond the generic "Dashboard" layout-template slot. |
| Accessibility | DS-001 (styling) / SD-001 (mandate) | DS-001 Ch. 17; SD-001 §10 | SD-001 mandates that accessibility modes exist and how they behave; DS-001 defines the token values that satisfy the mandate. |
| White-label | DS-001 (visual) / SD-002 (config) | DS-001 Ch. 12; `SD-002-CANDIDATE-013` | Same visual/configuration split as Themes. |
| AI Visual Language | DS-001 | DS-001 Ch. 14.4; AI Tokens (Ch. 10) | SD-001 owns AI behavior and transparency requirements (`SD-001-012`); DS-001 owns only how AI-originated content is visually distinguished. |
| Evidence Visual Language | DS-001 (visual) / SD-001 (behavior) | DS-001 Ch. 14.1; SD-001 §4 | SD-001 owns the evidence rule (one click away, disclosed confidence formula); DS-001 owns its visual expression. |
| Executive Dashboards | DS-001 (visual) / SD-001 (structural) | DS-001 Ch. 14.9, Executive Components; SD-001 §8 | SD-001 defines the Sacred 12's structural and behavioral rules (one question, seven actions, calm-tone mandate); DS-001 defines the visual system implementing calm tone. |
| Responsive Behaviour | DS-001 (visual) / SD-001 (structural) | DS-001 Ch. 16; SD-001 §11 | SD-001 mandates what must never be hidden at small viewports; DS-001 defines breakpoint/spacing token behavior. |
| Visual States | DS-001 | State Tokens (Ch. 10) | Interaction-state styling (hover/active/disabled/loading) is a token-level visual concern; the business rule that triggers a state remains SD-001/SD-002's. |

No row in this matrix assigns a topic to both documents without a stated split between its behavioral and visual halves. Where a split exists, DS-001 owns only the half named "visual," "styling," or "spec."

### 2.5 Design Consumption Model

DS-001 is consumed downstream of SD-001, never in parallel with it and never ahead of it. The dependency flow is:

```
Business Rules
      │
      ▼
Presentation Architecture (SD-001)
      │
      ▼
Design System (DS-001)
      │
      ▼
Enterprise Experience (PE-001)
      │
      ▼
Implementation Playbook (IMP-001)
      │
      ▼
Frontend Components
      │
      ▼
Rendered Experience
```

Business rules determine what must be presented and what governance the presentation must preserve. SD-001 translates those rules into presentation structure and behavior. DS-001 supplies the visual system that structure is rendered through. PE-001 and IMP-001 translate the combined SD-001/DS-001 contract into capability-specific and engineering-specific specifications. Frontend components implement that specification. The rendered experience is the observable result.

**DS-001-008: DS-001 Is Consumed, Never Bypassed**
No layer downstream of DS-001 in this model — PE-001, IMP-001, or frontend implementation — may introduce a color, token, type scale, or component visual treatment that does not originate in DS-001. A downstream layer that needs a visual capability DS-001 does not yet define shall request an extension to DS-001, not originate its own.

### 2.6 Traceability

Every visual specification in DS-001 shall be traceable to one of two origins:

A named SD-001 principle it renders — in which case the DS-001 chapter shall cite that principle by ID (as Chapter 1 cites `SD-001-033`, `SD-001-056`, `SD-001-104`–`106`) rather than restate the behavior the principle establishes.

An independent visual concern with no SD-001 antecedent — such as brand color, typeface, or icon style — in which case no citation is required, but the chapter shall state plainly that the concern is visual-only and carries no behavioral implication.

**DS-001-009: Every Visual Specification Traces to a Stated Origin**
A DS-001 chapter that introduces a visual rule without either citing the SD-001 principle it renders or stating that the rule is visual-only is incomplete. Untraceable visual rules are the mechanism by which two documents drift into silent duplication; traceability is how DS-001 prevents that drift by construction.

### 2.7 Governance Rules

**DS-001-010: Cross-Reference Instead of Duplication**
SD-001 may reference DS-001 for the visual realization of a principle it establishes. DS-001 may reference SD-001 for the behavioral origin of a visual requirement it renders. Neither document shall restate the other's content under a new heading, a paraphrase, or a "for context" summary. A reference is a citation by document and principle ID, never a copy.

**DS-001-011: Behaviour Changes Originate in SD-001**
Any change to what a screen does, what a widget contains, what sequence a user follows, or what governance a presentation surface must preserve shall be authored as a change to SD-001. DS-001 shall not be used to introduce behavioral change through a visual mechanism (for example, using a hidden or collapsed default style to suppress content SD-001 requires to be visible).

**DS-001-012: Visual Changes Originate in DS-001**
Any change to color, typography, iconography, token values, theme composition, motion, or component visual treatment shall be authored as a change to DS-001. SD-001 shall not specify a color, font, or visual measurement; if a draft change to SD-001 includes one, it shall be relocated to DS-001 before that change is accepted, following the same relocation discipline SD-001 v2.0 already applied to its own Appendices A and B.

### 2.8 Future Evolution

DS-001 is the single, canonical source of AUREX's visual language for every constitutional, engineering, and implementation document that follows it in the ARCH-000 dependency model — including PE-001 (Enterprise Experience Foundation & Methodology), PE-001-Cxxx (Capability-Specific Enterprise Experience Specifications), IMP-001 (Implementation Playbook), future capability documents, UX specifications, frontend engineering standards, the Marketplace architecture, and AI agents that generate or render user-facing content.

**DS-001-013: All Future Documents Inherit AUREX; None May Reinvent It**
No future document — capability-specific, engineering, or implementation — may define its own color system, typography, token set, or component visual standard. Every future document that touches visual rendering shall consume DS-001's tokens, themes, and component catalogue by reference. A capability document that requires a visual treatment DS-001 does not yet define shall request an extension to DS-001 (per the Design Governance chapter's Contribution Process, §22.4) rather than define a parallel, capability-local design system. This is the same "no forking" discipline SD-001-033 already establishes for platform behavior, extended here to platform appearance.

---

### Chapter 2 Validation

Before this chapter is considered complete, it has been checked against its own governance rules: no SD-001 structural, behavioral, or metadata rule is restated (§2.3, `DS-001-002`–`007` each cite rather than reproduce the SD-001 principle they distinguish from); no implementation technology, markup, or styling code is present; every ownership boundary in the matrix (§2.4) names both an owner and a stated reason, leaving no topic ambiguous; and the consumption model (§2.5) and future-evolution rule (§2.8) establish the mechanism — extension request to DS-001, never a parallel design system — by which future architectural conflicts of the kind this chapter exists to prevent are foreclosed.

*End of Chapter 2.*

---

## SECTION 3: Design Principles

### 3.1 Introduction

A Design System governed by subjective preference cannot remain coherent as the enterprises, brands, and technologies it serves change around it. If a color is chosen because a designer liked it, there is no basis on which to evaluate the next designer's different preference; the system drifts, decision by unrecorded decision, until "the AUREX look" is whatever the most recent contributor believed it to be.

This chapter exists to remove that failure mode. It establishes a fixed set of constitutional design principles — statements of what AUREX visual decisions must achieve, not statements of what any particular token, palette, or component looks like today. A principle in this chapter is written to remain true regardless of which brand colors DS-001 later specifies, which frontend framework renders them, or which enterprise's white-label theme is active. Where SD-001 established that presentation architecture must be independent of business domain, industry, and implementation technology (`SD-001` §1.3), this chapter establishes the equivalent independence for visual decisions: these principles do not expire when a rebrand happens, a design tool changes, or a new device class is supported. They are the constitutional layer beneath every token, theme, component, and future visual artifact this document will go on to specify.

### 3.2 Canonical Design Principles

**DS-001-014: One Visual Language**
*Statement.* AUREX presents one visual language across every screen, tenant, device, and white-label deployment. There is no "operational-theme AUREX" and "executive-theme AUREX" as separate systems — only one system rendering itself with contextually different density and tone.
*Architectural Rationale.* A platform whose appearance fragments by module or team erodes the same enterprise trust that a fragmented data model would erode. Visual fragmentation is architecture debt with a user-facing symptom.
*Practical Implications.* Any new visual capability is added to the one system, never built as a parallel or module-specific style sheet of decisions.

**DS-001-015: One Token, Every Surface**
*Statement.* Every color, space, radius, shadow, and motion value used anywhere in AUREX resolves from a governed design token. No surface defines its own one-off visual value.
*Architectural Rationale.* A value used once outside the token system cannot be changed once, only found and changed everywhere it was copied. Tokens are what make a single design decision propagate as a single edit rather than a search-and-fix exercise.
*Practical Implications.* A future chapter or component that appears to need a value the token catalogue does not yet contain requires a token extension, not a local exception.

**DS-001-016: Calm by Default, Loud by Exception**
*Statement.* Visual intensity — saturation, contrast, motion, size — is reserved for what genuinely requires attention. The default state of any surface is calm.
*Architectural Rationale.* This is the direct visual expression of `SD-001-056`'s mandate that Sacred 12 screens use a calmer, lower-motion, lower-saturation treatment, extended here as a default posture for the entire system, not only executive screens.
*Practical Implications.* Urgency is earned through a stated, evidenced reason (per `SD-001-043`'s evidence requirement for Action Center items), never manufactured through color or motion alone.

**DS-001-017: Clarity Before Decoration**
*Statement.* A visual element earns its place by making information easier to understand. Decoration that does not aid understanding is not part of AUREX.
*Architectural Rationale.* SD-001 established that presentation exists to create understanding, not to increase information density (`SD-001` §2.5). Clarity Before Decoration is the visual-form corollary: nothing may be added to a screen's appearance that competes with that understanding.
*Practical Implications.* A proposed illustration, texture, or ornamental treatment must be justified by what it clarifies, not by how it looks in isolation.

**DS-001-018: Consistency Before Creativity**
*Statement.* A component looks the same way everywhere it appears. Novelty is never introduced for its own sake.
*Architectural Rationale.* This principle restates SD-001's LAW-17 (Consistency Over Creativity) at the level of visual design, completing the lineage from platform law to constitutional presentation principle to constitutional design principle.
*Practical Implications.* A new screen or capability reuses the existing component catalogue and token set; it does not invent a bespoke visual treatment to feel distinctive.

**DS-001-019: Accessibility Is Mandatory, Not Optional**
*Statement.* Every visual decision is made within accessibility constraints from the outset. Accessibility is never a mode added after a design is finished.
*Architectural Rationale.* SD-001 establishes accessibility as the baseline configuration, not an opt-in (`SD-001-059`). A design system that treats accessible styling as a later pass rather than a starting constraint cannot honor that mandate.
*Practical Implications.* Contrast, focus visibility, and non-color status indication are evaluated at the same time a token or component is designed, not audited afterward.

**DS-001-020: Motion Must Communicate, Never Decorate**
*Statement.* Every animation exists to help a user understand a state change, a relationship, or a system response. Motion with no communicative purpose does not belong in AUREX.
*Architectural Rationale.* SD-001 requires that in-progress operations be visibly transparent (`SD-001-026`) and that Sacred 12 surfaces stay low-motion (`SD-001-056`). Motion that decorates rather than communicates works against both.
*Practical Implications.* A proposed animation must be describable as answering a specific user question ("what changed," "where did this go," "is this still working") before it is accepted.

**DS-001-021: Brand Without Distraction**
*Statement.* Brand identity is present and recognizable, but never louder than the enterprise intelligence it frames.
*Architectural Rationale.* Human attention is the platform's most valuable resource and shall never be wasted (`SD-001` §1.6, LAW-28). Branding that competes for attention against the evidence, confidence, or recommendation a screen exists to convey violates this resource directly.
*Practical Implications.* Logo, brand color, and product identity occupy fixed, predictable positions; they do not expand, animate, or intensify to draw attention to themselves.

**DS-001-022: Every Visual Element Has Purpose**
*Statement.* Nothing renders on a screen without an identifiable reason for being there in the form it takes.
*Architectural Rationale.* This generalizes SD-001's discipline of restraint — most concretely codified as the Action Center's seven-item cap (`SD-001-043`) — into a standing test applied to every visual element, not only actions.
*Practical Implications.* A component, icon, or visual flourish that cannot state what it communicates is a candidate for removal, regardless of how established it has become.

**DS-001-023: Progressive Visual Disclosure**
*Statement.* Visual density increases only as a user chooses to go deeper. The first view of any surface is its calmest, simplest rendering.
*Architectural Rationale.* This is the visual rendering of SD-001's four-level information model — Summary → Details → Evidence → Audit History (`SD-001-021`). SD-001 defines the levels exist and their order; DS-001 defines how each level looks and how the transition between levels is perceived.
*Practical Implications.* Detail, evidence, and audit-level visual treatments are designed as expansions of the summary view, not as separately styled destinations.

**DS-001-024: Visual Trust Builds Enterprise Trust**
*Statement.* How trustworthy a piece of intelligence looks is part of how trustworthy the platform is. Confidence, evidence, and provenance must be visually legible without requiring interpretation.
*Architectural Rationale.* SD-001 mandates that confidence is always visible, never buried (`SD-001-010`). A confidence indicator that is technically present but visually indistinguishable from decorative content fails that mandate in practice even while satisfying it in the abstract.
*Practical Implications.* Confidence, evidence, and AI-origination require a distinct, recognizable visual vocabulary — the specific subject of Chapter 14 — not a generic styling treatment shared with unrelated content.

**DS-001-025: Themes Change Appearance, Never Meaning**
*Statement.* Switching between Light, Dark, High-Contrast, Boardroom, or any white-label theme changes how a screen looks. It never changes what a screen means, what data it shows, or what action is available.
*Architectural Rationale.* This extends Chapter 2's Structure vs. Appearance distinction (`DS-001-002`) into the specific case of theming: a theme is by definition an appearance-layer construct, and a theme that altered meaning would be, by that same distinction, no longer a theme but an undocumented behavioral change.
*Practical Implications.* A theme is validated by confirming that identical business content produces identical information across every theme — only its visual expression differs.

**DS-001-026: Design Must Scale Across Enterprises**
*Statement.* The visual system supports any enterprise's brand, department structure, and Enterprise DNA profile without a redesign.
*Architectural Rationale.* SD-001 requires that a screen's rendered behavior adapt to a tenant's resolved Enterprise DNA profile without code change (`SD-001-027`). Design Must Scale Across Enterprises is the visual-system precondition for that adaptation: the token and theme architecture must already contain the range of expression DNA-adaptive rendering will select from.
*Practical Implications.* A visual specification is evaluated against the full range of enterprise contexts it must serve — consensus-driven and centralized, conservative and aggressive, exception-based and detail-oriented — not only the context most recently in front of the designer.

**DS-001-027: Extend, Never Fork**
*Statement.* A new capability, tenant, or white-label deployment extends the existing design system. It never creates a second, parallel one.
*Architectural Rationale.* This is `DS-001-013`'s (Chapter 2) inheritance rule, restated here as a first-order design principle rather than only a governance rule for future documents — because forking is as often a design-time temptation ("just this once, a custom look") as it is a governance failure.
*Practical Implications.* A request for a visual treatment outside the current catalogue is resolved as a token or component extension proposal (§22.4), never as a one-off exception built outside the system.

**DS-001-028: Beauty Through Simplicity**
*Statement.* Visual elegance in AUREX is achieved by removing what is unnecessary, not by adding what is impressive.
*Architectural Rationale.* This principle has no SD-001 behavioral antecedent — it is a purely visual, aesthetic commitment, permitted under Chapter 2 §2.6's provision that visual-only concerns require no behavioral citation, only an explicit statement that none exists.
*Practical Implications.* When two visual solutions communicate equally well, the simpler one is the AUREX-conformant one, regardless of which is more visually elaborate.

### 3.3 Relationship with SD-001 Principles

The Design Principles above complement SD-001's Presentation Principles; they do not replace, restate, or substitute for them. Where a Design Principle above renders an SD-001 principle visually, it cites that principle rather than reproducing its meaning — consistent with the traceability rule established in Chapter 2 (`DS-001-009`).

| DS-001 Principle | Related SD-001 Principle | Relationship |
|---|---|---|
| `DS-001-014` One Visual Language | `SD-001-033` DNA Profiles Do Not Fork the Platform | Same anti-fragmentation discipline, applied to appearance instead of behavior. |
| `DS-001-015` One Token, Every Surface | `SD-001-016` Screens Are Metadata, Not Code | Mirrors metadata-driven consistency, applied to visual constants instead of screen structure. |
| `DS-001-016` Calm by Default, Loud by Exception | `SD-001-056` Calm Executive Seriousness | Direct visual implementation, generalized as a system-wide default posture. |
| `DS-001-017` Clarity Before Decoration | `SD-001` §2.5 Presentation Creates Understanding, Not Information | Visual-form corollary of the same understanding-first philosophy. |
| `DS-001-018` Consistency Before Creativity | SD-001 LAW-17 Consistency Over Creativity | Same law, restated at the visual-design level. |
| `DS-001-019` Accessibility Is Mandatory | `SD-001-059` Accessibility by Default | Visual-styling counterpart to the accessibility mandate. |
| `DS-001-020` Motion Must Communicate | `SD-001-026` Screen Performance Transparency; `SD-001-056` | Motion in service of stated system state and calm-tone requirements, never decoration. |
| `DS-001-021` Brand Without Distraction | SD-001 LAW-28 Human Attention Is the Most Valuable Resource | Branding must not compete with the attention SD-001 protects. |
| `DS-001-022` Every Visual Element Has Purpose | `SD-001-043` Action Center, Maximum Seven | Same discipline of restraint, generalized beyond actions to all visual elements. |
| `DS-001-023` Progressive Visual Disclosure | `SD-001-021` Progressive Disclosure | Visual rendering of SD-001's four information levels. |
| `DS-001-024` Visual Trust Builds Enterprise Trust | `SD-001-010` Confidence Is Always Visible | Visual legibility as the practical precondition for the confidence mandate. |
| `DS-001-025` Themes Change Appearance, Never Meaning | `DS-001-002` Structure vs. Appearance (Chapter 2) | Internal extension of Chapter 2's own distinction to the specific case of theming. |
| `DS-001-026` Design Must Scale Across Enterprises | `SD-001-027` Enterprise DNA Is a Resolved Screen Input | Visual-system precondition for DNA-adaptive rendering. |
| `DS-001-027` Extend, Never Fork | `DS-001-013` (Chapter 2); `SD-001-033` | Restates the platform's anti-fork discipline as a first-order design principle. |
| `DS-001-028` Beauty Through Simplicity | — | Visual-only; no behavioral counterpart required (Chapter 2 §2.6). |

### 3.4 Applying the Principles

These principles are not aspirational language; they are the test every future visual decision in AUREX must pass before acceptance.

For **Components** (Chapter 13), a new or revised component visual standard is evaluated against Consistency Before Creativity, Every Visual Element Has Purpose, and Accessibility Is Mandatory before it is added to the catalogue.

For **Themes** (Chapter 11), a new theme is evaluated against Themes Change Appearance, Never Meaning and One Token, Every Surface — a theme that requires a token the catalogue does not define, or that alters what information a screen conveys, does not qualify as a theme.

For **Tokens** (Chapter 10), a proposed token is evaluated against One Token, Every Surface and Design Must Scale Across Enterprises — a token defined for a single surface's convenience, rather than for reuse across the system, is not accepted.

For **Dashboards** (Chapter 18), visual density and chart treatment are evaluated against Calm by Default, Loud by Exception and Progressive Visual Disclosure.

For **AI-generated content** (Chapter 14), visual distinction from human-verified content is evaluated against Visual Trust Builds Enterprise Trust and Motion Must Communicate, Never Decorate.

For **White-label branding** (Chapter 12), a partner or tenant brand adaptation is evaluated against Brand Without Distraction and Extend, Never Fork — a white-label request that would require forking the token system to satisfy is redirected to a token extension instead.

For **Executive Experiences** (Chapter 14.9, Executive Components), visual treatment is evaluated against Calm by Default, Loud by Exception and Beauty Through Simplicity, consistent with SD-001's Sacred 12 tone mandate.

For **Mobile Experiences** (Chapter 16), visual adaptation is evaluated against Progressive Visual Disclosure and Design Must Scale Across Enterprises — density changes with viewport, but no principle in this chapter is suspended because a surface is smaller.

No component, theme, token, or visual artifact is accepted into AUREX without being checked against this section. This obligation is formalized as the Design Review Process in Chapter 22.1.

### 3.5 Governance

**DS-001-029: Principle Evolution Is Constitutional, Not Editorial**
The fifteen Canonical Design Principles in §3.2 SHALL evolve rarely, and only through the same constitutional review discipline applied to SD-001's own principles. A new principle SHALL NOT be introduced to justify a single design decision already made; it is introduced only when a recurring class of decisions demonstrates that no existing principle governs it. An existing principle SHALL NOT be reworded, narrowed, or removed without architectural approval at the same governance level that approved this chapter. A principle's number, once assigned, is permanent — a retired principle is marked retired, never renumbered or reassigned to different content, preserving the traceability this chapter depends on.

---

### Chapter 3 Validation

This chapter has been checked against Chapter 2's own governance rules before completion: no principle restates an SD-001 structural or behavioral rule — each either cites the SD-001 principle it visually renders (§3.3) or is explicitly marked visual-only (`DS-001-028`); no token value, color, or implementation technology appears anywhere in this chapter; every principle is stated as a durable architectural commitment rather than a current-state description, so that none expires when branding, frameworks, or devices change; and §3.4 establishes the mechanism by which these principles bind future chapters rather than remaining aspirational.

*End of Chapter 3.*

---

## SECTION 4: Brand Identity & Product Branding

This chapter establishes the constitutional identity of AUREX as a product — what the brand must represent and how it may and may not be expressed. It defines architectural intent only. It does not define a logo, a palette, a typeface, or any artwork; those specifications belong to Chapters 5 through 11 and shall be evaluated against the philosophy this chapter establishes, not the reverse.

### 4.1 Brand Philosophy

AUREX is the visual identity of an Enterprise Intelligence Fabric — a platform whose purpose, as SD-001 establishes, is to help organizations continuously understand themselves, understand the external world, and make better business decisions (`SD-001` §1.2). The brand exists to make that purpose feel true on sight, before a user reads a single number.

The AUREX identity shall communicate:

**Trust** — the visual identity of a system whose conclusions are evidence-first and never opinion-first (`SD-001` §1.6) must itself be visually trustworthy: consistent, unornamented, and free of anything that reads as persuasion rather than information.

**Intelligence** — the identity communicates a system that interprets, not merely displays; it looks like something that understands what it is showing, not a container decorated around raw data.

**Clarity** — nothing in the brand's expression may compete with the clarity SD-001 requires of the screens it decorates (`SD-001` §2.5).

**Enterprise-grade credibility** — the identity is built for boardrooms and operational teams alike, not for a consumer audience; it favors precision over charm.

**Calm confidence** — the brand does not need to raise its voice to be credible. This is the identity-level expression of `DS-001-016` (Calm by Default, Loud by Exception).

**Precision** — every element of the identity is deliberate; nothing is present because it is decorative or fashionable.

**Transparency** — the identity never suggests certainty the underlying intelligence does not have. It shall not visually overstate confidence, completeness, or authority.

**Explainability** — even the brand itself, when questioned, should be describable in terms of what it represents and why — consistent with SD-001's constitutional requirement that every conclusion the platform presents be explainable (`SD-001` §1.6).

These attributes describe enterprise intelligence, not consumer software. AUREX is not designed to delight in the way a consumer application seeks engagement; it is designed to be trusted in the way an instrument a CEO relies on for a board decision must be trusted. Every future brand decision — logo (Chapter 5), color (Chapter 6), typography (Chapter 7) — is evaluated against this distinction first.

### 4.2 Brand Positioning

AUREX is an Enterprise Operating Center. It is not a reporting tool, a dashboard product, or a workflow application, and its brand shall never position it as one.

The brand shall convey:

**Understanding over dashboards** — AUREX is positioned as a system that builds understanding, of which a dashboard is only one possible rendering, consistent with SD-001's principle that presentation experiences consume Enterprise Intelligence rather than constitute it (`SD-001` §1.6).

**Intelligence over reporting** — reports are outcomes of the platform's intelligence, not the platform's purpose (`SD-001` §2.7). The brand shall never position AUREX primarily as a reporting product, even where reporting is one of its visible capabilities.

**Guidance over workflow** — AUREX guides a user toward resolution — through Guided Completion, evidence, and recommendation — rather than routing them through a workflow to be completed. The brand shall reflect a system that helps, not one that merely processes.

**Confidence over complexity** — the enterprise problems AUREX addresses are genuinely complex; the brand shall never make that complexity a visual identity. AUREX is positioned as the thing that makes complexity navigable, not as a proud display of the complexity itself.

### 4.3 Brand Personality

The AUREX personality is: calm, confident, intelligent, professional, honest, transparent, purposeful, and modern without being fashionable.

Modern without being fashionable is a deliberate distinction. AUREX shall look current, not dated — but it shall never adopt a visual trend for the sake of appearing contemporary. A personality built on trend-following would itself violate `DS-001-018` (Consistency Before Creativity) the moment the trend passed. AUREX's modernity is expressed through precision and restraint, which do not go out of date, rather than through stylistic novelty, which does.

This personality is not decorative language; it is a constraint that governs every later visual decision. A typography choice (Chapter 7) that reads as playful rather than professional fails this personality regardless of its legibility. A motion treatment (Chapter 15) that reads as flashy rather than purposeful fails this personality regardless of its technical smoothness. Later chapters shall be evaluated for conformance to this personality before they are evaluated for anything else.

### 4.4 Brand Expression Principles

**DS-001-030: Product Before Logo**
The product experience — the intelligence AUREX surfaces, the trust it earns through evidence and explainability — is always more important than any mark that represents it. A logo is a signature, not the substance. No future decision shall inflate the visual prominence of the AUREX mark at the expense of the content it accompanies.

**DS-001-031: Branding Supports Understanding, Never Competes With It**
Every branded element — logo, brand color, product identity — is subordinate to the same understanding-first purpose that governs all presentation (`SD-001` §2.5). Branding shall never be placed, sized, colored, or animated in a way that draws attention away from evidence, confidence, or recommendation content. This extends `DS-001-021` (Brand Without Distraction) from a design principle into an enforceable brand-expression rule.

**DS-001-032: Brand Consistency Across Every Tenant**
The AUREX product identity is expressed identically across every tenant, regardless of that tenant's white-label configuration, industry, or Enterprise DNA profile. Tenant-level customization changes tenant branding (§4.5); it does not change what AUREX itself is.

**DS-001-033: White-Label Shall Never Obscure the AUREX Identity**
A white-label or partner-branded deployment may present a tenant's or partner's own brand prominently, but it shall never fully remove or obscure that the underlying platform is AUREX. The mechanism by which product identity and tenant identity coexist is defined in Chapter 12; this principle establishes the constitutional floor that Chapter 12's mechanism must not fall below.

**DS-001-034: Every Visual Asset Reinforces Trust**
No visual asset — brand or otherwise — is neutral with respect to trust. An asset that is inconsistent, low-fidelity, or careless in its execution erodes the same trust that SD-001's evidence and confidence principles work to build (`SD-001-010` through `SD-001-014`). Every asset associated with the AUREX brand is held to the standard of an instrument a board relies on, not a marketing artifact.

**DS-001-040: The Brand Shall Never Misrepresent Capability**
*Statement.* The AUREX brand SHALL accurately represent the maturity, capability, confidence, explainability, and scope of the Enterprise Intelligence Fabric. Branding SHALL NOT imply intelligence, automation, certainty, accuracy, autonomy, or capability that the underlying platform cannot genuinely deliver.
*Architectural Rationale.* This principle is the brand-level expression of SD-001's evidence-first philosophy (`SD-001` §1.6: "Presentation is evidence-first, never opinion-first") and its constitutional rule that trust thresholds are delegated human authority, never autonomous AI decision-making (`SD-001-013`). A brand that visually overstates what the platform does undermines the same trust the platform's evidence and confidence architecture exists to earn — the identity would be asserting a certainty the system itself is constitutionally required to disclose as uncertain. Aspirational marketing that outruns genuine capability is therefore not a brand risk external to this design system; it is a direct violation of it.
*Practical Implications.* A brand asset, campaign visual, or product description SHALL NOT depict AUREX autonomously deciding, fully automating a judgment, or achieving certainty where the platform's own architecture requires human governance and disclosed confidence (`SD-001-013`, `SD-001-014`). Where platform capability changes, brand expression describing that capability SHALL be revised to match it — never the reverse.

*(Numbered DS-001-040 as the next constitutionally assigned identifier, per `DS-001-029`'s permanence rule, rather than DS-001-035 — that number, along with DS-001-036 through DS-001-039, was already assigned to the Governance principles in §4.6 at the time this principle was added.)*

### 4.5 Relationship with White-label Branding

AUREX's identity operates across four distinct tiers, each with a different scope of authority:

**Product Brand** — AUREX itself: the constitutional identity defined in this chapter. It is the one identity that exists in every deployment, unconditionally.

**Tenant Brand** — a customer organization's own branding, applied within the token and theme architecture Chapter 12 defines. A tenant brand customizes appearance; it operates entirely within the governance this document establishes and cannot alter what AUREX is.

**Partner Brand** — a reseller's or systems integrator's branding, applied where AUREX is delivered through a partner relationship. Partner branding is subject to the same constitutional floor as tenant branding (`DS-001-033`).

**Marketplace Brand** — the branding of a marketplace-distributed extension, widget, or template (SD-001 §14). A marketplace brand identifies the extension's origin; it does not extend to rebranding the platform surface the extension appears within.

AUREX always remains the underlying product identity. White-labeling — at the tenant, partner, or marketplace tier — customizes presentation strictly within the governance DS-001 defines; it does not create a new brand, a forked identity, or an exception to the principles in §4.4. The specific token architecture, visual mechanics, and boundary conditions by which white-label branding is technically achieved are defined in Chapter 12; this section establishes only that Chapter 12's mechanism operates beneath, and in service of, the constitutional brand this chapter defines.

### 4.6 Governance

**DS-001-035: The Four-Tier Brand Model Is Fixed**
The distinction between Product, Tenant, Partner, and Marketplace brand (§4.5) is a constitutional structure. A future chapter, capability, or implementation SHALL NOT introduce an additional brand tier, or collapse two of the four tiers into one, without architectural review at the level that approved this chapter.

**DS-001-036: Brand Identity Evolves Deliberately, Not Reactively**
Changes to the AUREX brand philosophy, positioning, or personality defined in §4.1–4.3 SHALL be made deliberately, through the same constitutional review discipline as any other change to this document, and never as a reaction to a single campaign, competitor, or short-term initiative.

**DS-001-037: Marketing Campaigns Shall Not Redefine the Constitutional Brand**
A marketing campaign may express the AUREX brand within the philosophy and expression principles this chapter defines. It SHALL NOT introduce a positioning, personality trait, or visual identity that conflicts with this chapter. Where a campaign requires an expression this chapter does not yet support, the chapter is amended first, through constitutional review — the campaign does not proceed ahead of it.

**DS-001-038: Temporary Branding Shall Not Affect the Design System**
A time-bound treatment — an event, an anniversary, a seasonal moment — SHALL NOT alter any token, theme, or component defined elsewhere in this document, and SHALL NOT be implemented in a way that persists beyond its stated duration. Temporary branding exists, if at all, entirely outside the governed design system, never as a variant within it.

**DS-001-039: Product Identity Shall Remain Stable Across Releases**
The AUREX product identity defined in this chapter SHALL remain recognizable and consistent across platform releases. A release may extend the token and component system that expresses the brand (Chapters 6–13); it SHALL NOT alter what the brand fundamentally represents without the same constitutional review this chapter itself required.

---

### Chapter 4 Validation

This chapter defines philosophy and governance only: no logo, color, typeface, or artwork is specified anywhere above — those remain reserved for Chapters 5 (Logo System), 6 (Color System), and 7 (Typography), which this chapter's principles will govern once authored. No marketing slogan or campaign language appears; §4.6 instead constrains marketing to operate within this chapter rather than substituting for it. Every attribute, positioning statement, and personality trait in §4.1–4.3 is stated as a durable characteristic of what AUREX *is*, not as a description of any current asset, so the chapter remains valid regardless of which specific visual assets later chapters define.

*End of Chapter 4.*

---

## SECTION 5: Logo System

This chapter defines the constitutional architecture of the AUREX Logo System — the categories of official marks, their hierarchy, their governing usage rules, and their behavior across rendering contexts. It defines architectural intent only. It does not define artwork, SVG or image assets, pixel dimensions, or any measurement; those specifications live in the design asset repository and are implementation, not architecture.

### 5.1 Purpose

A logo is commonly treated as a marketing artifact — something a brand team produces and a design tool renders. Within AUREX, the Logo System is instead a constitutional asset, because the mark is the single visual element most directly responsible for a user's instantaneous answer to the question "what am I looking at, and can I trust it?"

Consistency of identity is a precondition for enterprise trust, not a decoration of it. A user who sees the same mark behave predictably — appearing in the same category of place, at the same relative prominence, meaning the same thing — across every screen, tenant, and device extends to that mark the same trust SD-001's evidence and confidence architecture works to earn for the intelligence it accompanies (`DS-001-024`, Chapter 3). A logo that varies unpredictably, by contrast, introduces exactly the kind of ambiguity SD-001's evidence-first philosophy exists to eliminate. This chapter therefore governs the Logo System with the same constitutional discipline as any other architectural concern in this document, not as a lighter-weight marketing appendix to it.

### 5.2 Logo Architecture

The AUREX identity is expressed through a closed, defined set of official mark categories. Each category has a distinct role; none is interchangeable with another.

| Mark Category | Role |
|---|---|
| Primary Product Mark | The complete, unabbreviated expression of the AUREX identity, combining symbol and wordmark. The default and preferred mark wherever context and space permit it to appear in full. |
| Product Wordmark | The AUREX name rendered alone, used where the symbol component is unnecessary or where a text-only context requires the name to carry the identity by itself. |
| Product Symbol | The abstracted mark without the wordmark, used only where the Primary Product Mark has already established recognition in the same context and space does not permit the full mark. |
| Compact Mark | A reduced-complexity expression of the Product Symbol reserved for the smallest rendering contexts, where the Product Symbol itself would lose recognizability. |
| Application Mark | The identity as it represents AUREX as an installed or launched application, distinct from its use in a document or communication context. |
| Platform Certification Mark | A mark asserting that a capability, extension, or integration has been certified conformant with AUREX's canonical architecture — an assertion of governance conformance, not of authorship. |
| Marketplace Verified Mark | A mark asserting that a marketplace-distributed extension or widget has passed SD-001's marketplace admission criteria (`SD-001-100`). Distinct from the Platform Certification Mark: it verifies a listing, not core-platform conformance. |

**DS-001-041: The Logo System Is a Closed, Governed Set of Marks**
No mark exists outside the seven categories above. A future need that appears to require a new kind of mark is resolved by proposing an extension to this closed set through constitutional review (§5.7), never by an ad hoc variant produced outside it. This is `DS-001-027` (Extend, Never Fork) applied specifically to the Logo System.

### 5.3 Identity Hierarchy

The Logo System expresses the same four-tier brand model Chapter 4 establishes — Product, Tenant, Partner, and Marketplace Brand (§4.5) — as a set of marks with contextual precedence.

| Context | Precedent Identity | Note |
|---|---|---|
| Core platform screens (Layer 1 & Layer 2) | AUREX Product Identity | Tenant brand is expressed through theme tokens (Chapter 12), not by displaying a competing mark in place of the Primary Product Mark. |
| Tenant-branded deployment | Tenant Identity, foregrounded — AUREX Product Identity, attributed | Per `DS-001-033`, the AUREX identity remains present even when the tenant's own brand is visually dominant. |
| Partner-delivered deployment | Partner Identity, foregrounded — AUREX Product Identity, attributed | Same constitutional floor as a tenant deployment. |
| Marketplace listing | Marketplace Verified Mark, alongside the extension author's own identity | Does not carry Product Mark precedence; identifies the listing, not the platform. |
| Certification context | Platform Certification Mark | Independent of tenant or partner context; asserts conformance only, not ownership. |

**DS-001-042: Identity Precedence Is Contextual, Not Absolute**
Which identity is visually foregrounded changes by context, as the table above establishes; that AUREX remains present in some recognizable form does not change, in any context, per `DS-001-033`. A future context not covered by the table above shall be resolved by determining which of the four brand tiers (Chapter 4 §4.5) applies, then applying the same attribution floor — never by inventing a precedence rule outside this section.

### 5.4 Usage Principles

**DS-001-043: One Canonical Master Logo**
Each mark category in §5.2 has exactly one canonical form. There is no "preferred" and "alternate" version of the same mark competing for use in the same context; where a category requires more than one rendering (for example, across themes, per §5.6), those renderings are governed variations of the one canonical form, not independent alternatives.

**DS-001-044: No Unofficial Variants**
A mark shall not be redrawn, recolored outside the governed theme mechanism (§5.6), distorted, combined with unofficial elements, or otherwise altered outside this chapter's governance. This is `DS-001-018` (Consistency Before Creativity) applied to the Logo System specifically: creative reinterpretation of the mark is not permitted regardless of the context that seems to invite it.

**DS-001-045: The Logo Never Competes With Enterprise Intelligence**
Consistent with `DS-001-021` (Brand Without Distraction) and `DS-001-031` (Branding Supports Understanding, Never Competes With It), no mark shall be sized, positioned, animated, or emphasized in a way that draws attention away from evidence, confidence, or recommendation content. The mark identifies; it does not compete for the attention the content it accompanies is entitled to.

**DS-001-046: The Logo Scales Without Changing Meaning**
A mark rendered at any permitted scale — from Application Mark to Compact Mark — communicates the identical identity. Scale changes which category of mark is appropriate to a context (§5.2); it never changes what the mark, once selected, means.

**DS-001-047: Product Identity Remains Recognizable at Every Scale**
Within the range of contexts the Logo System is designed to serve, the AUREX identity remains recognizable. A rendering context that would require the mark to be reduced below recognizability is not a valid context for any mark in §5.2; it requires either a different mark category or falls outside the Logo System's intended scope.

**DS-001-048: The Logo Shall Not Imply Ownership of Tenant Data**
The AUREX mark identifies the platform. It shall never be presented in a manner suggesting that AUREX, rather than the tenant, owns, controls, or holds proprietary rights to a tenant's business data. This distinction is constitutional: SD-002's ownership model assigns every business object a named Business Owner and System of Record independent of platform identity, and the Logo System shall not visually contradict that assignment.

### 5.5 Protected Zones

Every mark in §5.2 requires a protected zone around it within which no other visual element — text, imagery, competing marks, or interface chrome — may intrude. This chapter defines the architectural concept only; the specific dimensions of that zone for each mark are an asset-repository specification, not a DS-001 concern.

The protected zone exists to preserve four properties, not to enforce an aesthetic:

**Safe area** — the minimum surrounding space required before any other element may be placed, ensuring the mark is never visually crowded.

**Isolation space** — the requirement that the mark not be placed directly against competing visual complexity (dense text, imagery, or another mark) regardless of whether the safe area's spacing requirement is technically satisfied.

**Minimum visibility** — the assurance that, at any permitted scale (§5.4), the mark remains perceivable against its background rather than approaching illegibility.

**Recognition** — the ultimate property the other three exist to protect: that a user encountering the mark, in any governed context, recognizes it as AUREX without conscious effort.

**DS-001-049: Protected Zones Preserve Recognition, Not Aesthetics**
A protected-zone violation is defined by whether it degrades recognition, not by whether it looks visually crowded. A context that satisfies recognition through means other than empty space around the mark is not, for that reason alone, non-conformant — but a context that technically preserves the letter of a safe-area rule while degrading recognition in substance is non-conformant. The specific measurements implementing this test are defined in the asset repository and are out of scope for this chapter.

### 5.6 Logo Behaviour

The AUREX mark renders across Light, Dark, High-Contrast, and white-label themes (Chapter 11), across printed media, and across accessibility modes (Chapter 17). In every one of these contexts, the mark's identity is invariant even as its specific rendering adapts — the same relationship Chapter 3 establishes between theme and meaning generally.

**DS-001-050: Logo Identity Is Invariant Across Theme and Medium**
Switching theme, medium, or accessibility mode changes how the mark is rendered — its contrast treatment in High-Contrast mode, its color resolution in Dark theme, its reproduction in printed media — but never changes which mark category is displayed or what it identifies. This is `DS-001-025` (Themes Change Appearance, Never Meaning) applied to the Logo System: a mark that required a different symbol, not merely a different rendering, to remain legible in a given theme would indicate a defect in that theme's token design (Chapter 11), not a legitimate logo variant. The specific color and contrast values each theme resolves the mark through are defined in Chapters 6 and 11, not here.

### 5.7 Governance

**DS-001-051: Logo Evolution Is Rare and Constitutionally Reviewed**
The Logo System defined in §5.2 changes rarely, and only through the same constitutional review discipline as any other change to this document. A change to a mark is not a routine design update; it is a change to the single most recognizable expression of the AUREX identity and is governed accordingly.

**DS-001-052: Legacy Logos Are Archived, Never Reused**
When a mark is retired, it is archived for historical and audit reference — consistent with SD-001's Enterprise Memory principle that nothing is silently discarded (`SD-001-111`) — and shall never be returned to active use, repurposed for a different mark category, or reintroduced for a nostalgic or campaign purpose. A retired mark's identity is permanently retired with it.

**DS-001-053: Certification and Verification Marks Require Approval**
The Platform Certification Mark and Marketplace Verified Mark (§5.2) are applied only through an explicit approval process; neither may be self-applied by a capability owner, partner, or marketplace contributor. This mirrors SD-001's marketplace admission governance (`SD-001-100`, `SD-001-102`): a mark asserting conformance is only as trustworthy as the approval process behind it.

**DS-001-054: Marketplace Badges Conform to Canonical Rules**
A marketplace listing may display the Marketplace Verified Mark only in the form and context this chapter and the asset repository define. It shall not be resized, recolored, paired with unofficial claims, or presented in a way that implies a higher level of platform endorsement than SD-001's admission criteria actually establish.

**DS-001-055: Logos Shall Never Convey System State**
*Statement.* The AUREX Logo System exists solely to establish and preserve product identity. Official AUREX marks SHALL NOT be used to communicate operational status, system health, AI confidence, workflow state, approval state, processing state, tenant status, platform availability, security posture, or any other business or operational condition.
*Architectural Rationale.* Identity and operational communication are constitutionally separate concerns. Operational meaning is governed by SD-001 (Presentation Architecture), PE-001 (Enterprise Experience), and capability-specific presentation models — never by the Logo System. Confidence, evidence, and status already have a dedicated visual vocabulary elsewhere in this document (Chapter 14; State Tokens, Chapter 10); overloading the mark itself with state would create a second, competing channel for information SD-001 already requires to be visible through its own governed mechanisms (`SD-001-010`, `SD-001-026`), undermining rather than reinforcing the One Visual Language principle (`DS-001-014`).
*Practical Implications.* A mark shall never change color, animate, badge, or otherwise visually mutate to represent whether a system is healthy, an approval is pending, an AI-generated result is confident, or a tenant's subscription is active. Where such conditions must be communicated, they are rendered through the components these chapters define instead — Badge, Confidence Indicator, Notification/Toast (Chapters 10, 13, 14) — never through the logo. A design proposal that asks the logo to "light up" or otherwise carry state is redirected to the appropriate Evidence or Interaction component instead.

---

### Chapter 5 Validation

This chapter defines architecture, not artwork: no color, typeface, SVG, PNG, Figma reference, CSS, pixel dimension, or measurement appears anywhere above — Protected Zones (§5.5) and Logo Behaviour (§5.6) are stated as architectural properties and explicitly deferred to the asset repository and to Chapters 6/11 respectively for their concrete values. No content restates Chapter 4's brand philosophy or Chapter 6's forthcoming color system; each cross-reference (`DS-001-021`, `DS-001-025`, `DS-001-033`) cites rather than reproduces. The Logo System remains technology-independent throughout — every principle is stated as true regardless of what rendering technology, file format, or design tool eventually produces the marks it governs.

*End of Chapter 5.*

---

## SECTION 6: Color System

This chapter defines the constitutional architecture of colour within AUREX — how colour functions as a system, not what any specific colour is. It defines architectural intent only. It does not define hex, RGB, HSL, Pantone, or CMYK values, gradients, token values, or theme palettes; those specifications belong to the Design Asset Repository and the Token Library, and are governed by Chapters 10 and 11 respectively, not by this chapter.

### 6.1 Purpose

Colour in AUREX is a semantic architectural language, not decoration. A colour applied to a screen is a claim about meaning — that a value is favorable, that an item requires attention, that content originated from AI rather than a verified source — and every such claim is subject to the same evidence-first discipline SD-001 applies to any other claim the platform makes (`SD-001` §1.6).

Colour exists in AUREX to improve understanding, recognition, and trust — never to make a screen more visually interesting. A colour system that cannot state, for every colour it defines, what business meaning that colour communicates is not an architecture; it is a palette, and palettes are not sufficient for a platform whose presentation is constitutionally required to be evidence-first and explainable. This chapter establishes the discipline that keeps AUREX's colour system the former rather than the latter.

### 6.2 Colour Philosophy

**DS-001-056: Colour Communicates Meaning, It Does Not Decorate**
Every colour used within AUREX exists because it communicates something — a semantic state, a brand identity, a data value. A colour introduced because a screen "needs more visual interest" has no place in this architecture. This is `DS-001-022` (Every Visual Element Has Purpose) applied specifically to colour.

**DS-001-057: Colour Reinforces Understanding**
Colour is used to make an already-present meaning faster to perceive — distinguishing a warning from a confirmation at a glance — never to introduce a meaning that exists only in colour. Colour accelerates understanding SD-001's presentation architecture already establishes; it does not originate understanding on its own.

**DS-001-058: Colour Never Replaces Information**
No business fact, state, or value is communicated by colour alone with no accompanying text, icon, or label. This is the colour-system precondition for SD-001's constitutional rule that colour is never the only indicator (`SD-001-062`); §6.6 states the accessibility consequence of this principle in full.

**DS-001-059: Colour Reduces Cognitive Effort**
A well-architected colour system lets a user recognize state, category, or priority without reading — a screen a user can partially understand at a glance is one where colour has done its job. A colour system that requires a legend to be interpreted has failed this principle.

**DS-001-060: Colour Remains Calm**
Consistent with `DS-001-016` (Calm by Default, Loud by Exception), the AUREX colour system's default expression is restrained. Saturation and intensity are reserved for the feedback and semantic states that genuinely warrant them, never applied broadly for visual energy.

**DS-001-061: Colour Supports Enterprise Decision-Making**
Every colour family this chapter establishes (§6.3) exists in service of a user's ability to make a better business decision faster — evaluating risk, recognizing confidence, distinguishing priority. A proposed colour or family that cannot be justified against this purpose is not admitted to the architecture.

### 6.3 Colour Architecture

AUREX defines fifteen constitutional colour families. The objective of this architecture is not to introduce additional colours — no colour value is defined anywhere in this document — but to establish a semantic structure rich enough to support the Design Tokens, Themes, Components, and Enterprise Intelligence visuals that later chapters define. Each family has a distinct purpose and architectural intent; none substitutes for another.

**Brand Colours**
*Purpose:* Express AUREX and tenant/partner brand identity (Chapter 4) within the governed token system.
*Architectural Intent:* Provides the identity layer that every white-label and tenant variant customizes through, remaining the one family Chapter 4's four-tier brand model (§4.5) governs.

**Neutral Colours**
*Purpose:* Provide the achromatic foundation — the grays and near-grays — that structures every screen's visual hierarchy independent of brand or semantic colour.
*Architectural Intent:* Establishes the base layer every other family composes against, so brand and semantic colour remain legible and distinct rather than competing with an equally saturated background.

**Surface Colours**
*Purpose:* Define the visual layering of interface surfaces — background, card, panel, overlay — establishing depth and hierarchy.
*Architectural Intent:* Encodes elevation and containment as colour relationships, working in concert with Elevation and Shadow Tokens (Chapter 10) rather than relying on shadow alone.

**Content Colours**
*Purpose:* Govern text, icon, and foreground legibility against the surfaces they appear on.
*Architectural Intent:* Guarantees every surface/content colour pairing meets the legibility standard Chapter 17 (Accessibility Styling) requires, independent of which surface or theme is active.

**Border & Divider Colours**
*Purpose:* Define the colour vocabulary for separating regions, fields, and components without relying on spacing alone.
*Architectural Intent:* Remains a distinct, lower-emphasis family from Content Colours, so structural separation never competes visually with legible content.

**Semantic Status Colours**
*Purpose:* Carry a fixed business meaning (success, warning, danger, info) independent of any specific hue, so meaning is portable across themes.
*Architectural Intent:* The constitutional successor to this chapter's original Semantic Colours family, renamed to distinguish platform-wide status meaning from the more specific Evidence, Confidence, and Decision Support families below, each of which now carries its own dedicated semantic architecture rather than being folded into one generic "semantic" family.

**Feedback Colours**
*Purpose:* Communicate the outcome of a user action or system response (confirmation, error, caution), distinct from ambient semantic state.
*Architectural Intent:* Governs transient, action-triggered colour — a submitted form, a failed request — as distinct from the persistent Semantic Status Colours describing an object's ongoing state.

**Evidence Colours**
*Purpose:* Distinguish evidence-backed content from unverified or asserted content, in direct service of SD-001's evidence-first mandate (`SD-001` §1.6).
*Architectural Intent:* Establishes a dedicated semantic family for a concept central to the Enterprise Intelligence Fabric, rather than overloading Semantic Status Colours with a meaning that has no natural success/warning/danger analogue. Its visual realization is defined in Chapter 14 (§14.1).

**Confidence Colours**
*Purpose:* Express the degree of confidence attached to a value or conclusion, independent of whether that value is favorable or unfavorable.
*Architectural Intent:* Confidence is orthogonal to sentiment — a low-confidence favorable number and a high-confidence unfavorable number are both real conditions this family must represent without collapsing into Semantic Status Colours' favorable/unfavorable axis. Its visual realization is defined in Chapter 14 (§14.2).

**AI Colours**
*Purpose:* Distinguish content along the full AI-involvement provenance spectrum, from fully AI-generated to fully human-verified.
*Architectural Intent:* Architected to support, at minimum, five constitutionally distinct provenance states — AI-generated, AI-assisted, AI-inferred, AI-validated, and human-verified AI output — rather than a single undifferentiated "AI or not AI" signal, in service of SD-001's requirement that AI-generated conclusions distinguish what was inferred from what was found directly (`SD-001-012`). No visual treatment for any of these states is defined here; that specification belongs to Chapter 14 (§14.4).

**Decision Support Colours**
*Purpose:* Represent the colour vocabulary attached to recommendations and decision-relevant intelligence, distinguishing a recommendation from a raw observation.
*Architectural Intent:* Recommendations carry a different constitutional status than data — SD-001 requires that a recommendation never be presented as a decision (`SD-001-013`) — and require a colour family that visually preserves that distinction rather than rendering a recommendation indistinguishable from a confirmed fact.

**Data Visualisation Colours**
*Purpose:* Govern chart, graph, and quantitative-display colour, calibrated for perceptual accuracy rather than brand expression.
*Architectural Intent:* Optimized for accurate quantitative perception — ordering, magnitude, categorical distinction — even where that optimization diverges from Brand Colours' identity-expression goals.

**Accessibility Colours**
*Purpose:* Define the contrast-compliant, colour-vision-safe variants every other family resolves to under accessibility modes (Chapter 17).
*Architectural Intent:* Functions as a resolution layer across all fourteen other families rather than a family with independent content of its own — every family above requires an Accessibility Colours counterpart, not only a default rendering.

**Focus & Interaction Colours**
*Purpose:* Govern the colour expression of interactive state — focus, hover, active, selected — distinct from the State Tokens (Chapter 10) that define the states themselves.
*Architectural Intent:* Provides the colour vocabulary that satisfies SD-001's keyboard-first, visibly-focused navigation mandate (`SD-001-060`), ensuring focus is always colour-legible in addition to whatever other visual treatment accompanies it.

**White-label Mapping Layer**
*Purpose:* Defines how every family above remaps for a tenant's or partner's white-label brand (Chapter 12), without altering which family a given meaning belongs to.
*Architectural Intent:* Is not itself a source of colour meaning; it is the governed substitution mechanism by which Brand Colours — and only Brand Colours, per `DS-001-076` — vary by tenant while every semantic family above remains platform-constant. Its mechanics are fully specified in Chapter 12.

**DS-001-062: The Colour Architecture Is a Closed, Named Set of Families**
No colour is introduced outside the fifteen families above. A need that appears to require a new kind of colour is resolved by proposing an extension to this closed set through constitutional review (§6.8), never by an unnamed, one-off colour applied outside any family. This is `DS-001-027` (Extend, Never Fork) applied to the Colour System.

### 6.4 Semantic Colour Principles

**DS-001-063: One Meaning, Everywhere**
A given semantic colour means the same thing on every screen, in every capability, for every tenant. A colour meaning "danger" in one context and "brand accent" in another is a defect, not a valid local adaptation.

**DS-001-064: One Family Per Concept**
Each business concept a colour can represent is assigned to exactly one colour family (§6.3). A confidence-related concept is never expressed through Brand Colours; a brand-related concept is never expressed through Semantic Colours. Mixing families to represent one concept fragments the meaning that meaning is supposed to carry.

**DS-001-065: No Capability-Specific Colours**
A capability, module, or Business Activity shall not define a colour meaning that applies only within itself. All semantic colour meaning is platform-wide, defined in this chapter and its token realization (Chapter 10), never locally scoped.

**DS-001-066: Colour Never Changes Business Meaning**
Applying, removing, or changing the colour associated with a value never changes what that value means, what decision it should inform, or what data it represents. Colour is a rendering of meaning that already exists elsewhere in the platform's data and business-object model (SD-002); it is never the sole location where that meaning is defined.

**DS-001-067: Themes Change Appearance, Not Semantics**
A theme (Chapter 11) may change which specific token value a semantic colour resolves to; it never changes which concept that semantic colour represents. This is `DS-001-025` (Themes Change Appearance, Never Meaning) applied specifically to colour: "danger" remains "danger" in Light, Dark, High-Contrast, and every white-label theme, even as its rendered value differs across them.

**DS-001-067A: Semantic Colour Meaning Is Immutable**
*Statement.* A semantic meaning SHALL NOT migrate from one semantic colour family to another merely because branding, themes, or visual styles evolve. Evidence always represents evidence. Confidence always represents confidence. Risk always represents risk.
*Architectural Rationale.* Branding (Chapter 4) may change appearance. Themes (Chapter 11) may change rendering. Tokens (Chapter 10) may change resolved values. None of these changes carries the authority to alter which family a business concept belongs to (§6.3) or what that concept means (§6.4). This principle is the temporal counterpart to `DS-001-063` (One Meaning, Everywhere): where `DS-001-063` guarantees meaning is constant across every simultaneous context, `DS-001-067A` guarantees meaning is constant across every future revision of this document's downstream chapters.
*Practical Implications.* A future rebrand, theme redesign, or token-value migration (Chapters 4, 10, 11) may change how Evidence Colours, Confidence Colours, or any other family renders. None of them may reassign what Evidence, Confidence, or Risk semantically belongs to, or move a concept from one family to another, without constitutional review of this chapter itself (§6.8).

### 6.5 Relationship with Design Tokens

Colour has no existence within AUREX outside the Design Token system. A colour used anywhere in the platform is a resolved Colour Token (Chapter 10, §6.3's families) — never a value chosen or entered independently of that system.

**DS-001-068: Colour Is Resolved Only Through Design Tokens**
Implementations SHALL consume colour exclusively through the token system Chapter 10 defines. No implementation, capability, or extension shall hard-code a colour value outside that system. This is `DS-001-015` (One Token, Every Surface) applied specifically to colour, and it is the mechanism by which §6.4's semantic consistency principles are actually enforceable rather than aspirational: a hard-coded colour cannot be governed, retheme, or verified for accessibility compliance the way a token can.

### 6.6 Accessibility

**DS-001-069: Colour Alone Never Carries Meaning**
This chapter's colour architecture is built to satisfy SD-001's constitutional accessibility rule that colour is never the only indicator (`SD-001-062`): every semantic and feedback colour family (§6.3) is architected to always accompany a non-colour signal — text, icon, or pattern — never to stand alone. SD-001 establishes the requirement; this principle is the colour system's structural commitment to being capable of satisfying it in every instance.

**DS-001-070: The Colour System Is Perceivable Regardless of Colour Vision**
Every colour family is architected to remain distinguishable under common colour-vision variations, and to resolve to validated high-contrast variants under the accessibility modes SD-001 requires to exist (`SD-001-063`). A colour pairing that depends on typical colour vision to be distinguished is not a valid semantic pairing.

**DS-001-071: The Colour System Remains Coherent Across Dark Mode and Print**
The meaning a colour carries (§6.4) is preserved when rendered in Dark theme or in printed media, even where the specific value resolved for that meaning necessarily differs by medium. A colour architecture that only functions correctly in one rendering medium is incomplete.

**DS-001-072: AI-Originated Content Is Colour-Explainable**
The AI Colours family (§6.3) exists so that a user can determine, from colour alone as one signal among others, which of the AI-involvement provenance states — AI-generated, AI-assisted, AI-inferred, AI-validated, or human-verified AI output — applies to content before them, rather than only a binary AI/not-AI signal, in direct service of SD-001's requirement that AI-generated conclusions expose their reasoning and origin on demand (`SD-001-012`). The specific visual standards for each provenance state are defined in Chapter 14; this principle establishes only that the Colour System is architected to support them.

### 6.7 Enterprise Intelligence Colour Language

Enterprise Intelligence introduces semantic concepts — Evidence, Confidence, Explainability, AI Origin, Recommendations, Risks, Business Activities — that have no equivalent in a conventional application's colour system. A generic Semantic Status Colours family (success, warning, danger, info) is insufficient to represent them: confidence is not a status, evidence is not a warning, and AI origin is not a feedback outcome. §6.3 accordingly establishes Evidence Colours, Confidence Colours, AI Colours, and Decision Support Colours as their own constitutional families, distinct from the general-purpose families a conventional application would consider sufficient.

This section, and §6.3's family definitions, establish only the semantic architecture — that these concepts exist, are distinct from one another and from generic status, and belong to named families. This chapter does not define how Evidence, Confidence, Explainability, AI Origin, Recommendations, Risks, or Business Activities are actually rendered in colour. Their visual realization is defined downstream, by:

Chapter 10 (Design Tokens) — the specific token values these families resolve to.
Chapter 11 (Theme Architecture) — how those token values vary across Light, Dark, High-Contrast, Boardroom, and white-label themes.
Chapter 13 (Component Visual Standards) — how Evidence Components, Confidence Indicators, and related components apply these families.
Chapter 14 (AUREX Domain Visual Language) — the complete visual standards for Evidence, Confidence, Explainability, AI-Generated Content, Recommendations, Knowledge Graphs, Enterprise Relationships, Business Activities, Decision Support, Risk Indicators, and Trust Indicators.

**DS-001-072A: Enterprise Intelligence Concepts Have Their Own Colour Semantics**
*Statement.* Evidence, Confidence, AI Origin, and Decision Support are semantically distinct from generic Semantic Status Colours and from one another. No downstream chapter shall render one of these concepts by reusing a generic status colour's meaning.
*Architectural Rationale.* Collapsing Enterprise Intelligence concepts into generic status colour would misrepresent them — a low-confidence value is not "a warning" in the way a failed validation is a warning; it is a distinct epistemic state requiring its own vocabulary, consistent with SD-001's requirement that confidence be visible and its computation disclosed (`SD-001-010`, `SD-001-011`) rather than approximated through an unrelated colour meaning.
*Practical Implications.* Chapters 10, 11, 13, and 14 shall realize Evidence, Confidence, AI, and Decision Support Colours as their own token and component vocabularies, never as re-skinned Semantic Status Colours.

### 6.8 Governance

**DS-001-073: Colour Evolution Is Rare and Constitutionally Reviewed**
The fifteen colour families and their semantic assignments (§6.3–6.4) change rarely, and only through the same constitutional review discipline as any other change to this document.

**DS-001-074: New Semantic Colour Families Require Constitutional Review**
A proposed sixteenth colour family, or a proposed new semantic meaning within an existing family, is admitted only through constitutional review — never through unilateral introduction by a design contributor, capability team, or implementation effort.

**DS-001-075: Capability Teams Shall Not Introduce Colours**
Consistent with `DS-001-065` (No Capability-Specific Colours), a capability or Business Activity team has no authority to introduce a new colour, family, or semantic meaning. A capability that requires a colour meaning this chapter does not yet support proposes an extension through the Design Governance contribution process (Chapter 22 §22.4).

**DS-001-076: White-Label Colour Remains Governed**
A tenant's or partner's white-label brand colour (Chapter 12) is applied only within the Brand Colours family and the token mechanism that family defines. White-labeling customizes which brand colour is active; it never grants authority to introduce a new colour family or override a semantic colour's meaning.

**DS-001-077: Marketing Colour Shall Never Redefine Product Semantics**
A marketing or campaign use of colour, however it is applied outside the product surface, shall never cause a semantic colour's platform meaning to be reinterpreted. This is `DS-001-037` (Marketing Campaigns Shall Not Redefine the Constitutional Brand, Chapter 4) applied specifically to colour semantics.

---

### Chapter 6 Validation

This chapter defines architecture, not palette: no hex, RGB, HSL, Pantone, CMYK, gradient, token value, or theme palette appears anywhere above, including within the expanded fifteen-family architecture (§6.3) and the Enterprise Intelligence Colour Language section (§6.7) — both state purpose and semantic intent only. Every reference to how a colour is actually resolved or rendered is deferred explicitly to Chapter 10 (Design Tokens), Chapter 11 (Theme Architecture), Chapter 13 (Component Visual Standards), or Chapter 14 (AUREX Domain Visual Language), and no content here restates what those chapters will define. Every accessibility principle in §6.6 cites SD-001's governing mandate (`SD-001-062`, `SD-001-063`, `SD-001-012`) rather than restating it, consistent with the traceability rule established in Chapter 2. `DS-001-067A` and `DS-001-072A` preserve, rather than expand, this chapter's existing scope — they constrain how meaning may change over time and clarify that Enterprise Intelligence concepts are semantically distinct, without defining any new visual treatment. The Colour System remains technology-independent throughout — every principle is stated as true regardless of what design tool, file format, or rendering technology eventually produces the colours it governs.

*End of Chapter 6.*

---

## SECTION 7: Typography

This chapter defines the constitutional architecture of Typography within AUREX. Typography is treated as the Enterprise Reading Architecture — the system governing how written information supports comprehension, cognition, decision-making, and enterprise trust — not as a collection of fonts or text styles. It defines architectural intent only. It does not define font families, font names, sizes, line heights, weights, CSS, variable fonts, typography token values, or any rendering technology; those specifications belong to the Design Asset Repository and the Design Token System (Chapter 10).

### 7.1 Purpose

Typography exists in AUREX to improve comprehension, not to improve appearance. A typographic choice that makes a screen look more refined but makes a number harder to read correctly has failed its purpose, regardless of its visual sophistication.

Typography is the primary medium through which Enterprise Intelligence is communicated. Evidence, confidence, recommendations, and explanations are, in the overwhelming majority of cases, read before they are seen in any other form — a chart is glanced at, but a conclusion is read. This chapter's discipline exists because SD-001 requires that every conclusion be explainable and every insight traceable (`SD-001` §1.6): an explanation that is technically present but typographically difficult to read fails that requirement in practice even while satisfying it in the abstract, in exactly the way Chapter 6 established for colour and confidence (`DS-001-024`).

### 7.2 Typography Philosophy

**DS-001-078: Reading Before Decoration**
Typography's first obligation is to be read correctly and efficiently. Decorative typographic treatment — for its own visual effect — is never permitted to compromise that obligation. This is `DS-001-017` (Clarity Before Decoration, Chapter 3) applied specifically to text.

**DS-001-079: Typography Encodes Information Hierarchy**
The relative typographic treatment of two pieces of text is itself information: it tells a user which is more structurally important without requiring them to read either first. Typography that fails to encode hierarchy forces a user to determine importance by reading everything, defeating the purpose of hierarchy entirely.

**DS-001-080: Typography Serves Cognitive Clarity**
Every typographic decision is evaluated by whether it reduces the cognitive effort required to understand what is being read, consistent with `DS-001-059` (Colour Reduces Cognitive Effort, Chapter 6) applied to the written word.

**DS-001-081: Enterprise Readability Is Non-Negotiable**
Readability is evaluated against the enterprise reading contexts this chapter defines (§7.3) — sustained analytical reading, rapid executive scanning, precise evidence review — not against a single generic readability standard. A typographic system that reads well in one context and poorly in another is incomplete, not merely imperfect.

**DS-001-082: Typographic Calm**
Consistent with `DS-001-016` (Calm by Default, Loud by Exception, Chapter 3), typographic emphasis — weight, size, contrast — is reserved for what genuinely warrants it. A screen where everything is emphasized communicates the same as a screen where nothing is.

**DS-001-083: Precision Over Style**
Where a typographic choice must trade stylistic distinctiveness against precision of communication, precision governs. AUREX's typographic identity is expressed through consistency and restraint (`DS-001-018`, Consistency Before Creativity), not through stylistic novelty.

**DS-001-084: Reading Efficiency**
Typography is architected so that a user extracts the meaning they need in the minimum time the content genuinely requires — neither artificially compressed past legibility nor artificially expanded past necessity.

**DS-001-084A: Typography Preserves Context**
*Statement.* Typography SHALL help a user immediately recognize the nature of the information they are reading. It SHALL reinforce contextual awareness across Enterprise Intelligence, not merely improve readability in isolation. At minimum, the Reading Architecture SHALL clearly distinguish Enterprise Intelligence, Evidence, AI Explanation, Operational Data, Collaboration, and Governance Information from one another. It SHALL NOT allow visually similar presentation to obscure fundamentally different categories of enterprise information.
*Architectural Rationale.* This principle sits between §7.2's readability-focused philosophy and §7.3's seven Reading Layers: it establishes that the Reading Architecture's purpose is not only to make each individual layer legible, but to make the boundary between layers perceivable without requiring a user to read metadata to determine what kind of content they are looking at. This is the typographic counterpart to `DS-001-072` (AI-Originated Content Is Colour-Explainable, Chapter 6) and SD-001's requirement that AI-generated conclusions expose their origin (`SD-001-012`) — typography must never typographically launder an AI Explanation into looking identical to an Evidence citation or an Operational field.
*Practical Implications.* The six categories named above map onto the Reading Architecture's existing layers (§7.3) rather than constituting a second, parallel taxonomy: Evidence maps to Evidence Reading, AI Explanation to AI Explanation Reading, Operational Data to Operational Reading, Collaboration to Collaboration Reading, and Governance Information to Administrative Reading; Enterprise Intelligence spans Executive and Analytical Reading as the general category both layers serve. This principle's obligation is that these six categories remain typographically distinguishable from one another — it does not add new layers to §7.3's closed set (`DS-001-085`). A future Reading Architecture extension that would cause two of these categories to become indistinguishable is non-conformant regardless of any other merit.

### 7.3 Reading Architecture

Enterprise Intelligence is read in constitutionally distinct contexts, each with a different relationship between reading speed, density, and precision. AUREX defines seven reading layers.

| Reading Layer | Purpose |
|---|---|
| Executive Reading | Supports the Sacred 12's calm, low-effort scanning (SD-001 §8) — headline meaning perceivable in seconds, minimal density, maximum clarity. |
| Analytical Reading | Supports sustained, detail-level reading during investigation and drill-down (`SD-001-021`, the Details level of Progressive Disclosure) — denser than Executive Reading, still calm. |
| Operational Reading | Supports the day-to-day scanning of Layer 1 operational screens — task lists, queues, forms — optimized for speed and repeated use. |
| Evidence Reading | Supports careful reading of source material, citations, and provenance (SD-001 §4) — favors precision and unambiguous reference over scanning speed. |
| AI Explanation Reading | Supports reading AI-generated reasoning chains and explanations (`SD-001-012`) — read as typographically distinct from both Evidence Reading and human-authored content, per Chapter 14's AI visual language. |
| Collaboration Reading | Supports comments, mentions, and asynchronous discussion (`SD-001-039`) — an informal register, still governed, distinct from formal record-level content. |
| Administrative Reading | Supports configuration, governance, and settings screens — favors unambiguous precision over narrative or persuasive register. |

**DS-001-085: The Reading Architecture Is a Closed, Named Set of Layers**
No reading context exists outside the seven layers above. A future need that appears to require a new reading context is resolved by proposing an extension to this closed set through constitutional review (§7.8), never by an ad hoc typographic treatment invented outside it. This is `DS-001-027` (Extend, Never Fork) applied to the Reading Architecture.

### 7.4 Information Hierarchy Principles

**DS-001-086: Same Hierarchy Everywhere**
A given level of typographic hierarchy — heading, subheading, body, caption — communicates the same structural importance on every screen, in every capability, for every tenant. This is `DS-001-063` (One Meaning, Everywhere, Chapter 6) applied to typography.

**DS-001-087: Headings Communicate Structure**
A heading's role is to make a screen's structure navigable, not to provide visual emphasis for its own sake. A heading used because a designer wanted a piece of text to stand out, rather than because it introduces a genuine structural division, misuses the hierarchy.

**DS-001-088: Body Communicates Understanding**
Body text is the primary vehicle through which Enterprise Intelligence's understanding-first purpose (SD-001 §2.5) is delivered. It is optimized for comprehension across sustained reading, not for visual texture or density.

**DS-001-089: Supporting Text Never Competes**
Captions, labels, timestamps, and metadata text never visually compete with heading or body text for attention. This is `DS-001-022` (Every Visual Element Has Purpose, Chapter 3) applied to the typographic register of supporting text specifically.

**DS-001-090: Typography Never Changes Business Meaning**
Applying, removing, or changing typographic emphasis never changes what a value means, what decision it should inform, or what data it represents. This is `DS-001-066` (Colour Never Changes Business Meaning, Chapter 6) applied to typography: a bolded number remains the same number.

**DS-001-091: Hierarchy Remains Stable Across Themes**
A theme (Chapter 11) may change how a given hierarchy level is rendered; it never changes which hierarchy level a piece of text occupies. This is `DS-001-025` (Themes Change Appearance, Never Meaning, Chapter 3) applied to typography.

### 7.5 Relationship with Design Tokens

**DS-001-092: Typography Is Resolved Only Through Design Tokens**
Implementations SHALL consume typography exclusively through the Typography Tokens Chapter 10 defines. No implementation, capability, or extension shall define an independent font family, scale, weight, or line-height outside that system. This is `DS-001-015` (One Token, Every Surface, Chapter 3) applied specifically to typography, mirroring `DS-001-068`'s treatment of colour (Chapter 6): a hard-coded typographic value cannot be governed, rethemed, or verified for accessibility compliance the way a token can.

### 7.6 Accessibility

**DS-001-093: Typography Is Architected for Screen-Reader Compatibility**
Every typographic hierarchy level and reading-layer treatment (§7.3–7.4) is architected to declare its structural role in a form a screen reader can announce, in direct service of SD-001's requirement that every widget declare its accessible name, role, and state (`SD-001-061`).

**DS-001-094: Typography Remains Legible Under Zoom and Responsive Reflow**
Typographic hierarchy and reading-layer distinctions remain legible and structurally intact under zoom and under the responsive reflow Chapter 16 governs. A hierarchy that only functions correctly at a single zoom level or viewport is incomplete.

**DS-001-095: Typography Adapts Density Across Reading Layers Without Losing Legibility**
The density appropriate to Executive Reading, Long-Form Evidence Reading, and AI Explanation Reading differs by design (§7.3); none of that variation is permitted to fall below the legibility standard this chapter and Chapter 17 (Accessibility Styling) establish. Density is a calibrated architectural choice per reading layer, never an accessibility trade-off.

**DS-001-096: Typography Shall Never Reduce Accessibility**
No typographic decision — for brand distinctiveness, for density, for stylistic effect — is permitted if it reduces accessibility below the baseline SD-001 establishes as non-optional (`SD-001-059`). Where a typographic preference and an accessibility requirement conflict, the accessibility requirement governs without exception.

### 7.7 Typography for Enterprise Intelligence

Enterprise Intelligence introduces reading requirements beyond those found in conventional enterprise software: Evidence Narratives, AI Reasoning Chains, Confidence Explanations, Recommendation Narratives, Executive Summaries, and Regulatory Disclosures each demand a distinct reading experience that a conventional application's typography system — built for forms, tables, and static documents — was never designed to support.

This section, and the Reading Architecture it extends (§7.3), establish only the constitutional reading requirement — that these six reading experiences exist, are distinct from one another, and require typographic treatment capable of serving them. This chapter does not define how Evidence Narratives, AI Reasoning Chains, Confidence Explanations, Recommendation Narratives, Executive Summaries, or Regulatory Disclosures are actually typeset. Their detailed realization is governed downstream, by:

Chapter 10 (Design Tokens) — the specific typography token values these reading experiences resolve to.
Chapter 11 (Theme Architecture) — how those token values vary across Light, Dark, High-Contrast, Boardroom, and white-label themes.
Chapter 13 (Component Visual Standards) — how Evidence Components, Confidence Indicators, and related components apply typographic treatment.
Chapter 14 (AUREX Domain Visual Language) — the complete visual standards for Evidence, Confidence, Explainability, AI-Generated Content, Recommendations, and Decision Support.

**DS-001-096A: Enterprise Intelligence Reading Experiences Require Their Own Typographic Treatment**
*Statement.* Evidence Narratives, AI Reasoning Chains, Confidence Explanations, Recommendation Narratives, Executive Summaries, and Regulatory Disclosures are reading experiences the Reading Architecture (§7.3) must be capable of serving distinctly. No downstream chapter shall render one of these experiences using an undifferentiated body-text treatment that erases the distinction `DS-001-084A` requires.
*Architectural Rationale.* A conventional application's typography system assumes a narrower range of content than Enterprise Intelligence produces — it was not designed to distinguish a regulatory disclosure from an AI-generated reasoning chain, because a conventional application does not generate reasoning chains at all. Reusing that narrower system without extension would silently collapse distinctions `DS-001-084A` and SD-001's evidence/explainability principles (`SD-001-011`, `SD-001-012`) require to remain visible.
*Practical Implications.* Chapters 10, 11, 13, and 14 shall realize typographic treatment for each of the six reading experiences above within the Reading Architecture's existing layers (§7.3) — Evidence Narratives and Regulatory Disclosures within Evidence and Administrative Reading respectively, AI Reasoning Chains and Confidence Explanations within AI Explanation Reading, Recommendation Narratives and Executive Summaries within Analytical and Executive Reading — never as an unrelated, parallel typography system. No typography value, font, or implementation guidance is introduced by this section.

### 7.8 Governance

**DS-001-097: Typography Evolves Rarely and Constitutionally**
The Reading Architecture and Information Hierarchy Principles this chapter establishes (§7.3–7.4) change rarely, and only through the same constitutional review discipline as any other change to this document.

**DS-001-098: Reading Hierarchy Remains Stable**
The relative ordering and meaning of hierarchy levels (§7.4) SHALL NOT be reordered or reinterpreted across releases. A heading SHALL NOT become a body-equivalent level, or vice versa, without constitutional review.

**DS-001-099: Capability Teams Shall Not Introduce Typography Systems**
Consistent with `DS-001-075` (Capability Teams Shall Not Introduce Colours, Chapter 6), a capability or Business Activity team has no authority to introduce a new reading layer, hierarchy level, or typographic treatment. A capability that requires typographic support this chapter does not yet provide proposes an extension through the Design Governance contribution process (Chapter 22 §22.4).

**DS-001-100: White-Label Branding Shall Not Redefine Typography Architecture**
A tenant's or partner's white-label configuration (Chapter 12) may vary within the typographic token system Chapter 10 defines; it shall never redefine the Reading Architecture (§7.3) or Information Hierarchy (§7.4) themselves. This is `DS-001-076` (White-Label Colour Remains Governed, Chapter 6) applied to typography.

**DS-001-101: Marketing Typography Shall Never Affect Product Typography**
A marketing or campaign use of typography, however it is applied outside the product surface, shall never cause a product typographic hierarchy or reading-layer treatment to be reinterpreted. This is `DS-001-037` (Marketing Campaigns Shall Not Redefine the Constitutional Brand, Chapter 4) applied specifically to typography.

---

### Chapter 7 Validation

This chapter defines the Enterprise Reading Architecture, not a font specification: no font family, font name, size, line height, weight, CSS, variable-font mechanism, typography token value, design software, or platform-specific rendering technology appears anywhere above, including within `DS-001-084A` and the Typography for Enterprise Intelligence section (§7.7) — both state contextual and reading-experience requirements only. Every reference to how typography is actually resolved or rendered is deferred explicitly to Chapter 10 (Design Tokens), Chapter 11 (Theme Architecture), Chapter 13 (Component Visual Standards), or Chapter 14 (AUREX Domain Visual Language), consistent with the deferral pattern Chapter 6 established for colour. Every accessibility principle in §7.6 cites SD-001's governing mandate (`SD-001-059`, `SD-001-061`) rather than restating it. `DS-001-084A` and `DS-001-096A` extend the six-experience and six-category requirements within the Reading Architecture's existing closed set of seven layers (§7.3, `DS-001-085`) rather than introducing a parallel taxonomy. Typography is positioned throughout as an architecture of reading and comprehension rather than as a stylistic system, and every principle is stated as true regardless of what typeface or rendering technology later chapters or implementations select.

*End of Chapter 7.*

---

## SECTION 8: Iconography

This chapter defines the constitutional architecture of Iconography within AUREX. Icons are treated as a Semantic Symbol Architecture — a governed vocabulary that reinforces enterprise understanding — not as decorative graphics. It defines architectural intent only. It does not define icon artwork, icon libraries, SVG assets, sizes, stroke widths, pixel grids, design software, or any rendering technology; those specifications belong to the Design Asset Repository and the Design Token System (Chapter 10).

### 8.1 Purpose

An icon in AUREX exists to improve recognition, reduce cognitive effort, and reinforce enterprise understanding — never to decorate a screen or fill visual space. A user encountering a well-architected icon recognizes its meaning before they would finish reading the equivalent word, which is precisely why an icon carries constitutional weight equal to the text it accompanies: a wrong or ambiguous icon misinforms exactly as a wrong word would, only faster and less consciously.

Because icons are perceived before they are consciously read, they are held to the same evidence-first, explainable standard SD-001 applies to every other element of presentation (`SD-001` §1.6). An icon is a claim about meaning, compressed into a symbol; this chapter exists to ensure that claim is always accurate, consistent, and governed.

### 8.2 Icon Philosophy

**DS-001-102: Symbols Before Decoration**
An icon exists because it represents a concept, action, or state — never because a screen benefits from additional visual texture. This is `DS-001-022` (Every Visual Element Has Purpose, Chapter 3) applied specifically to iconography.

**DS-001-103: Recognition Before Memorization**
An icon's form is evaluated by whether its meaning is recognizable on first encounter, not by whether a meaning can eventually be memorized through repeated exposure. An icon that requires a legend to be understood has failed this principle regardless of how elegant its form is.

**DS-001-104: Universal Interpretation**
An icon's meaning is architected to be interpretable across the enterprise contexts AUREX serves — different industries, regions, and cultural contexts — consistent with SD-001's cultural-neutrality mandate (`SD-001-066`). An icon whose meaning depends on a single cultural or regional convention is not a valid platform-wide icon.

**DS-001-105: Cognitive Efficiency**
Icons exist to let a user process meaning faster than text alone would allow. This is `DS-001-059` (Colour Reduces Cognitive Effort, Chapter 6) applied to symbols: an icon that takes longer to interpret than the word it replaces has inverted its own purpose.

**DS-001-106: Enterprise Precision**
An icon's meaning is exact, not approximate. Where a concept cannot be represented with precision, it is represented with text instead of an imprecise icon — an ambiguous symbol is worse than no symbol, because it appears authoritative while communicating uncertainly.

**DS-001-107: Calm Visual Language**
Consistent with `DS-001-016` (Calm by Default, Loud by Exception, Chapter 3), icons are rendered with restraint by default; visual intensity is reserved for icons representing genuinely urgent or exceptional conditions.

### 8.3 Semantic Icon Architecture

AUREX defines eleven constitutional icon families. Each has a distinct purpose; none substitutes for another.

| Icon Family | Purpose |
|---|---|
| Navigation Icons | Represent wayfinding and structural traversal (menus, breadcrumbs, expand/collapse) — the icon-level counterpart to SD-001's Navigation Architecture (`SD-001-018`), never a substitute for it. |
| Action Icons | Represent an available user action (save, delete, approve, assign), paired with the Action Center's evidence requirement (`SD-001-043`) where the action originates there. |
| Status Icons | Represent the lifecycle or condition of a business object, distinct from Semantic Status Colours (Chapter 6, §6.3) and never replacing the colour or text they accompany. |
| Evidence Icons | Represent the presence, type, or source of evidence — the icon-level counterpart to Evidence Colours (Chapter 6) and Evidence Components (Chapter 13). |
| AI Icons | Distinguish AI-generated, AI-assisted, AI-inferred, AI-validated, and human-verified AI content, mirroring the five-state provenance spectrum AI Colours defines (Chapter 6, §6.3). |
| Confidence Icons | Represent the degree of confidence attached to a value or conclusion, paired with Confidence Colours (Chapter 6) rather than substituting for them. |
| Risk Icons | Represent risk category or severity, distinct from the favorable/unfavorable axis Semantic Status Colours express, consistent with Decision Support Colours' distinct semantic status (Chapter 6). |
| Collaboration Icons | Represent comments, mentions, assignments, and collaborative state (`SD-001-039`). |
| Business Activity Icons | Represent named Business Activities (`SD-001-009`; SD-002 §5), helping a user recognize an activity by symbol before reading its name. |
| Governance Icons | Represent approval, audit, versioning, and governance state — the icon-level counterpart to SD-001's audit-visibility mandate (`SD-001-040`). |
| Marketplace Icons | Represent marketplace listings and categories — distinct from the Marketplace Verified Mark (Chapter 5, §5.2), which is a Logo System asset, not an icon. |

**DS-001-108: The Icon System Is a Closed, Named Set of Families**
No icon exists outside the eleven families above. A future need that appears to require a new kind of icon is resolved by proposing an extension to this closed set through constitutional review (§8.7), never by an ad hoc symbol invented outside it. This is `DS-001-027` (Extend, Never Fork) applied to Iconography.

### 8.4 Semantic Principles

**DS-001-109: One Meaning, Everywhere**
A given icon means the same thing on every screen, in every capability, for every tenant. This is `DS-001-063` (One Meaning, Everywhere, Chapter 6) applied to iconography.

**DS-001-110: One Icon Per Concept**
Each business concept an icon can represent is assigned to exactly one icon within its family (§8.3). Two different icons representing the same concept in different contexts fragments recognition in exactly the way `DS-001-064` (One Family Per Concept, Chapter 6) prohibits for colour.

**DS-001-111: Icons Reinforce Meaning, They Do Not Originate It**
An icon accelerates recognition of a meaning that exists independently of the icon — in the platform's data and business-object model (SD-002) or in SD-001's presentation rules. An icon is never the sole location where a meaning is defined.

**DS-001-112: Icons Never Replace Text**
No business fact, state, or value is communicated by an icon alone with no accompanying text or accessible label. This is `DS-001-058` (Colour Never Replaces Information, Chapter 6) applied to iconography, and the icon-level expression of SD-001's rule that colour — and, by the same logic, any single visual signal — is never the only indicator (`SD-001-062`).

**DS-001-113: Icons Remain Stable Across Themes**
A theme (Chapter 11) may change an icon's rendered stroke, weight, or colour resolution; it never changes which icon represents a given concept or what that icon means. This is `DS-001-025` (Themes Change Appearance, Never Meaning, Chapter 3) applied to iconography.

**DS-001-114: Icons Never Redefine Business Meaning**
Applying, removing, or changing an icon associated with a value never changes what that value means, what decision it should inform, or what data it represents. This is `DS-001-066` (Colour Never Changes Business Meaning, Chapter 6) applied to iconography.

### 8.5 Relationship with Design Tokens

**DS-001-115: Iconography Is Resolved Only Through the Governed Token and Asset System**
Implementations SHALL consume iconography exclusively through the Icon Tokens Chapter 10 defines and the governed asset system they resolve to. No implementation, capability, or extension shall introduce an icon outside that system. This is `DS-001-015` (One Token, Every Surface, Chapter 3) applied specifically to iconography, mirroring `DS-001-068` (colour, Chapter 6) and `DS-001-092` (typography, Chapter 7): an icon introduced outside the governed system cannot be verified against §8.3's closed family set or §8.4's semantic principles.

### 8.6 Accessibility

**DS-001-116: Every Icon Declares an Accessible Name**
Every icon, whether decorative-adjacent or functionally interactive, declares an accessible name a screen reader can announce, in direct service of SD-001's requirement that every widget declare its accessible name, role, and state (`SD-001-061`).

**DS-001-117: Interactive Icons Always Pair With a Perceivable Label**
An icon that triggers an action is never presented without an accompanying perceivable label — visible text, a tooltip surfaced through the same interaction model as the icon itself, or an equivalent — so that a sighted user unfamiliar with the icon's convention is not excluded from understanding it. This is distinct from, and in addition to, `DS-001-112`'s semantic-completeness rule: this principle addresses perceivability for users who do not use assistive technology but do not yet recognize the icon.

**DS-001-118: Icon Meaning Remains Perceivable Under High-Contrast Rendering**
An icon's form remains distinguishable and its meaning intact when rendered under the High-Contrast accessibility mode SD-001 requires to exist (`SD-001-063`). An icon whose recognizability depends on a colour or contrast level unavailable in High-Contrast mode is non-conformant.

**DS-001-119: Icon Recognition Accommodates Cognitive Accessibility**
Icon forms favor familiar, unambiguous, low-complexity symbols over novel or abstract ones, consistent with SD-001's broader accessibility and inclusivity mandate (`SD-001` §10). A symbol that requires sustained cognitive effort to decode works against the same cognitive-efficiency purpose this chapter establishes in §8.2.

### 8.7 Governance

**DS-001-120: Icon Evolution Is Rare and Constitutionally Reviewed**
The Icon System defined in §8.3 changes rarely, and only through the same constitutional review discipline as any other change to this document.

**DS-001-121: New Icon Families Require Constitutional Review**
A proposed twelfth icon family, or a proposed new semantic meaning within an existing family, is admitted only through constitutional review — never through unilateral introduction by a design contributor, capability team, or implementation effort.

**DS-001-122: Capability Teams Shall Not Introduce Icon Systems**
Consistent with `DS-001-075` (Capability Teams Shall Not Introduce Colours, Chapter 6) and `DS-001-099` (typography, Chapter 7), a capability or Business Activity team has no authority to introduce a new icon, family, or semantic meaning. A capability that requires an icon meaning this chapter does not yet support proposes an extension through the Design Governance contribution process (Chapter 22 §22.4).

**DS-001-123: White-Label Branding Shall Not Redefine Icon Semantics**
A tenant's or partner's white-label configuration (Chapter 12) may vary an icon's rendered style within the token system Chapter 10 defines; it shall never redefine which icon represents a concept or what that concept means. This is `DS-001-076` (White-Label Colour Remains Governed, Chapter 6) applied to iconography.

**DS-001-124: Marketing Icons Shall Never Affect Product Iconography**
A marketing or campaign use of an icon, however it is applied outside the product surface, shall never cause a product icon's platform meaning to be reinterpreted. This is `DS-001-037` (Marketing Campaigns Shall Not Redefine the Constitutional Brand, Chapter 4) applied specifically to iconography.

---

### Chapter 8 Validation

This chapter defines a Semantic Symbol Architecture, not artwork: no SVG, PNG, icon library, size, stroke width, pixel grid, design software, or rendering technology appears anywhere above. Every reference to how an icon is actually resolved or rendered is deferred explicitly to Chapter 10 (Design Tokens) and the governed asset system it defines. No content restates Chapter 5's Logo System (Marketplace Icons are explicitly distinguished from the Marketplace Verified Mark) or Chapter 6's Colour System (AI, Confidence, and Risk Icons are stated as paired with, never substituting for, their colour-family counterparts). Icons are positioned throughout as a governed semantic vocabulary — eleven closed families (§8.3) and six semantic principles (§8.4) — rather than a decorative graphic set, and every principle is stated as true regardless of what icon library or rendering technology later chapters or implementations select.

*End of Chapter 8.*

---

## SECTION 9: Illustration Standards

This chapter defines the constitutional architecture of Illustration within AUREX. Illustrations are treated as explanatory communication assets that improve understanding of Enterprise Intelligence — never as decorative artwork. It defines architectural intent only. It does not define illustration artwork, graphic assets, characters, mascots, image libraries, file formats, resolution, rendering tools, or design software; those specifications belong to the Design Asset Repository.

### 9.1 Purpose

An illustration in AUREX exists to improve understanding of something that is difficult to communicate in text or data alone — a relationship, a sequence, a concept — never to provide visual decoration or ambient warmth to a screen. Where an icon (Chapter 8) compresses a single concept into an instantly recognizable symbol, an illustration explains something a symbol is too small to carry: a process, a relationship, or an explanation with multiple interdependent parts.

Illustration is explanatory visual communication, held to the same standard SD-001 applies to every other explanatory mechanism on the platform: it must consume and clarify Enterprise Intelligence, never originate or embellish it (`SD-001` §1.6). An illustration that makes a screen more visually appealing but does not make its subject more understandable has not satisfied this chapter's purpose, regardless of its craft.

### 9.2 Illustration Philosophy

**DS-001-125: Explanation Before Decoration**
An illustration exists because it explains something — a process, a relationship, a state — that is genuinely difficult to communicate without it. This is `DS-001-017` (Clarity Before Decoration, Chapter 3) applied specifically to illustration.

**DS-001-126: Visual Storytelling Serves Understanding**
Where an illustration depicts a sequence or narrative, that narrative exists to make a real business process more comprehensible, never to entertain independently of the process it depicts.

**DS-001-127: Enterprise Credibility**
Illustration style reflects the same enterprise-grade credibility Chapter 4 establishes for the AUREX brand (`DS-001-030`–`034`). An illustration that reads as consumer-playful rather than enterprise-credible undermines the trust this document's every other chapter works to build.

**DS-001-128: Cognitive Simplicity**
An illustration is evaluated by how much faster it makes its subject understood, not by its visual complexity or detail. An illustration that requires as much interpretive effort as the text it accompanies has failed this principle.

**DS-001-129: Calm Communication**
Consistent with `DS-001-016` (Calm by Default, Loud by Exception, Chapter 3), illustration is used deliberately and sparingly, reserved for moments — onboarding, empty states, complex explanation — that genuinely benefit from it, never applied broadly for visual warmth.

**DS-001-130: Inclusive Representation**
Where an illustration depicts people, roles, or enterprise contexts, that depiction is inclusive and free of assumptions about geography, culture, gender, or industry that would exclude or misrepresent any enterprise AUREX serves — consistent with SD-001's cultural-neutrality mandate (`SD-001-066`).

**DS-001-131: Timeless Visual Language**
Illustration style favors durability over trend. This is `DS-001-018` (Consistency Before Creativity, Chapter 3) applied to illustration: a style built to look current for one season ages out of the constitutional identity Chapter 4 requires to remain stable across releases (`DS-001-039`).

### 9.3 Illustration Architecture

AUREX defines ten constitutional illustration families. Each has a distinct purpose; none substitutes for another.

| Illustration Family | Purpose |
|---|---|
| Onboarding Illustrations | Orient a new user to a capability or workspace during first use, reducing the cognitive gap between unfamiliarity and productive use. |
| Empty State Illustrations | Accompany the actionable empty states SD-001 requires (`SD-001-025`, `SD-001-041`) — illustrating what is missing and reinforcing, never replacing, the resolution paths those states must offer. |
| Process Illustrations | Explain a sequential business process (an approval chain, a data-resolution sequence) as a single comprehensible visual, never a substitute for the process's actual metadata (SD-001 §5). |
| Workflow Illustrations | Explain the structure of a multi-step workflow coordinating multiple actors or systems — distinct in scope from Process Illustrations' single linear sequence. |
| Enterprise Intelligence Illustrations | Explain how Enterprise Understanding, External World Intelligence, and Enterprise Intelligence relate (`SD-001` §1.2) — the conceptual illustrations §9.7 governs in full. |
| AI Explainability Illustrations | Illustrate how an AI-generated conclusion was reached, in direct service of SD-001's no-black-box mandate (`SD-001-012`). |
| Evidence Illustrations | Illustrate the relationship between a conclusion and the evidence supporting it (SD-001 §4) — distinct from Evidence Icons (Chapter 8) and Evidence Colours (Chapter 6) in that illustration explains a relationship rather than marking a single data point. |
| Success & Achievement Illustrations | Mark the completion of a Business Activity or milestone, used sparingly and consistent with Calm by Default (`DS-001-016`). |
| Learning & Guidance Illustrations | Support in-product guidance and Guided Completion (`SD-001-004`) by illustrating a concept a user is being walked through. |
| Marketplace Illustrations | Represent marketplace listings and categories at the illustration level, distinct from Marketplace Icons (Chapter 8) and the Marketplace Verified Mark (Chapter 5). |

**DS-001-132: The Illustration System Is a Closed, Named Set of Families**
No illustration exists outside the ten families above. A future need that appears to require a new kind of illustration is resolved by proposing an extension to this closed set through constitutional review (§9.8), never by an ad hoc illustration invented outside it. This is `DS-001-027` (Extend, Never Fork) applied to Illustration.

### 9.4 Semantic Principles

**DS-001-133: One Illustration Purpose Per Context**
A given screen context uses at most one illustration for one clearly identifiable purpose. Layering multiple illustrations to explain multiple things at once fragments the understanding each was meant to build.

**DS-001-134: Illustrations Reinforce Understanding**
An illustration accelerates understanding of something already true elsewhere in the platform's data and business logic (SD-002, SD-001); it is never the sole location where a fact or relationship is established.

**DS-001-135: Illustrations Never Replace Enterprise Data**
An illustration explains data or a process; it never stands in for the data itself. A screen shall not present an illustration in place of the evidence, confidence, or business object information SD-001 requires to be actually visible (`SD-001-010`, `SD-001-015`).

**DS-001-136: Illustrations Never Exaggerate Capability**
An illustration depicting AI reasoning, automation, or platform capability shall represent that capability accurately, never more advanced, autonomous, or certain than the platform genuinely is. This is `DS-001-040` (The Brand Shall Never Misrepresent Capability, Chapter 4) applied specifically to illustration.

**DS-001-137: Illustrations Remain Culturally Neutral**
This restates `DS-001-130` (Inclusive Representation) as a semantic, not only philosophical, requirement: an illustration's meaning shall not depend on a culturally specific reference that would be misunderstood or exclude any enterprise context AUREX serves.

**DS-001-138: Illustrations Remain Stable Across Themes**
A theme (Chapter 11) may change an illustration's rendered palette or contrast treatment; it never changes what the illustration depicts or means. This is `DS-001-025` (Themes Change Appearance, Never Meaning, Chapter 3) applied to illustration.

### 9.5 Relationship with Design Tokens

**DS-001-139: Illustrations Are Resolved Only Through the Governed Asset and Token Architecture**
Implementations SHALL consume illustration exclusively through the governed asset system and the Illustration Tokens Chapter 10 defines. No implementation, capability, or extension shall introduce an illustration outside that system. This mirrors `DS-001-068` (colour), `DS-001-092` (typography), and `DS-001-115` (iconography): an illustration introduced outside the governed system cannot be verified against §9.3's closed family set or §9.4's semantic principles.

### 9.6 Accessibility

**DS-001-140: Every Illustration Carries an Alternative Description**
Every illustration carries a text alternative describing what it depicts and why, sufficient for a screen-reader user to receive the same explanatory content a sighted user receives — in direct service of SD-001's requirement that every widget declare its accessible name, role, and state (`SD-001-061`).

**DS-001-141: Illustrations Accommodate Cognitive Accessibility**
Illustration content favors clear, literal representation over abstract or metaphorical depiction where the two would communicate differently to different users, consistent with SD-001's broader accessibility and inclusivity mandate (`SD-001` §10).

**DS-001-142: Illustrations Are Screen-Reader Compatible**
An illustration's alternative description (`DS-001-140`) is structured so a screen reader announces it in a form equivalent to, not a lesser version of, the explanatory content the illustration provides visually.

**DS-001-143: Illustrations Remain Legible Under Contrast and Print Rendering**
An illustration's explanatory content remains perceivable under the High-Contrast accessibility mode (`SD-001-063`) and in printed media, even where its specific rendering necessarily differs by mode or medium.

**DS-001-144: Illustrations Shall Never Reduce Accessibility**
No illustration — however explanatory its intent — is permitted if its presence reduces the accessibility of the content it accompanies below the baseline SD-001 establishes as non-optional (`SD-001-059`). Where an illustration and an accessibility requirement conflict, the accessibility requirement governs without exception.

### 9.7 Illustrations for Enterprise Intelligence

Enterprise Intelligence introduces explanatory visual requirements beyond those found in conventional enterprise software: enterprise relationship diagrams, AI reasoning illustrations, evidence flow illustrations, confidence explanations, recommendation journeys, and governance workflows each require an explanatory visual form that a conventional application — with no AI reasoning to explain and no evidence graph to depict — was never designed to support.

This section, and the Enterprise Intelligence Illustrations family it extends (§9.3), establish only the constitutional requirement — that these six explanatory categories exist, are distinct from the other nine illustration families, and require illustrative treatment capable of serving them. This chapter does not define how enterprise relationship diagrams, AI reasoning illustrations, evidence flow illustrations, confidence explanations, recommendation journeys, or governance workflows are actually drawn. Their detailed realization is governed downstream, by:

Chapter 10 (Design Tokens) — the specific illustration token values these explanatory categories resolve to.
Chapter 11 (Theme Architecture) — how those token values vary across Light, Dark, High-Contrast, Boardroom, and white-label themes.
Chapter 13 (Component Visual Standards) — how Visualization and Evidence Components apply illustrative treatment.
Chapter 14 (AUREX Domain Visual Language) — the complete visual standards for Evidence, Confidence, Explainability, AI-Generated Content, Recommendations, Knowledge Graphs, Enterprise Relationships, and Decision Support.

**DS-001-145: Enterprise Intelligence Illustration Requirements Are Constitutional, Not Decorative**
*Statement.* Enterprise relationship diagrams, AI reasoning illustrations, evidence flow illustrations, confidence explanations, recommendation journeys, and governance workflows are explanatory requirements the Illustration Architecture (§9.3) must be capable of serving through the Enterprise Intelligence Illustrations family, not optional embellishments a capability may include or omit at will.
*Architectural Rationale.* SD-001 requires that AI-generated conclusions expose their reasoning chain on demand (`SD-001-012`) and that relationships and evidence remain traceable (`SD-001` §1.6). Where a reasoning chain or evidence relationship is genuinely difficult to communicate in text alone, an illustration capable of explaining it is not a decorative nicety — it is part of how SD-001's explainability mandate is actually satisfied in practice.
*Practical Implications.* Chapters 10, 11, 13, and 14 shall realize illustrative treatment for each of the six categories above within the Enterprise Intelligence Illustrations family (§9.3) — never as an unrelated, parallel illustration system, and never by omitting illustrative support for a category on the grounds that it is difficult to draw.

### 9.8 Governance

**DS-001-146: Illustration Evolution Is Rare and Constitutionally Reviewed**
The Illustration System defined in §9.3 changes rarely, and only through the same constitutional review discipline as any other change to this document.

**DS-001-147: New Illustration Families Require Constitutional Review**
A proposed eleventh illustration family, or a proposed new purpose within an existing family, is admitted only through constitutional review — never through unilateral introduction by a design contributor, capability team, or implementation effort.

**DS-001-148: Capability Teams Shall Not Introduce Illustration Systems**
Consistent with `DS-001-075` (colour, Chapter 6), `DS-001-099` (typography, Chapter 7), and `DS-001-122` (iconography, Chapter 8), a capability or Business Activity team has no authority to introduce a new illustration, family, or explanatory purpose. A capability that requires illustrative support this chapter does not yet provide proposes an extension through the Design Governance contribution process (Chapter 22 §22.4).

**DS-001-149: White-Label Branding Shall Not Redefine Illustration Semantics**
A tenant's or partner's white-label configuration (Chapter 12) may vary an illustration's rendered palette within the token system Chapter 10 defines; it shall never redefine which illustration family serves a purpose or what a given illustration depicts. This is `DS-001-076` (White-Label Colour Remains Governed, Chapter 6) applied to illustration.

**DS-001-150: Marketing Illustrations Shall Never Affect Product Illustrations**
A marketing or campaign use of illustration, however it is applied outside the product surface, shall never cause a product illustration's purpose or meaning to be reinterpreted. This is `DS-001-037` (Marketing Campaigns Shall Not Redefine the Constitutional Brand, Chapter 4) applied specifically to illustration.

---

### Chapter 9 Validation

This chapter defines explanatory communication architecture, not artwork: no illustration artwork, graphic asset, character, mascot, image library, file format, resolution, rendering tool, or design software appears anywhere above. Every reference to how an illustration is actually rendered is deferred explicitly to Chapter 10 (Design Tokens), Chapter 11 (Theme Architecture), Chapter 13 (Component Visual Standards), or Chapter 14 (AUREX Domain Visual Language), and no content here restates what those chapters will define. Illustrations are positioned throughout as explanatory communication — ten closed families (§9.3), six semantic principles (§9.4), and a dedicated Enterprise Intelligence requirement (§9.7) — never as decoration, and every principle is stated as true regardless of what artistic style, file format, or rendering technology later chapters or implementations select.

*End of Chapter 9.*

---

## SECTION 10: Enterprise Design Token System

This chapter defines the Enterprise Design Token System as the governed semantic contract through which the constitutional design principles this document establishes are realized consistently across implementation technologies. Design principles establish meaning; the Token System preserves those meanings; implementations consume those meanings. It defines constitutional principles only. It does not define token values, JSON structures, CSS variables, Figma variables, platform-specific implementations, or file formats; those belong to implementation repositories.

This chapter's atomic token family table (§10.3) realizes, in full, the Design Token Catalogue frozen in this document's Document Architecture section. No family is added to or removed from that frozen list here.

### 10.1 Purpose

Design Tokens exist because Chapters 4 through 9 establish meaning — brand identity, colour semantics, reading hierarchy, icon families, illustration purposes — that must survive contact with implementation without being diluted, reinterpreted, or hard-coded into a form only one technology can read. A token is the constitutional contract between architecture and implementation: it names a meaning once, in this document, and every implementation technology that will ever render AUREX consumes that meaning by reference rather than by re-deriving it.

This chapter's place in that contract follows a fixed conceptual dependency chain: Constitutional Design Principles (Chapters 4 through 9) establish Semantic Meaning; the Design Token System (this chapter) preserves that meaning; the Theme System (Chapter 11) resolves it into context-specific values; Component Standards (Chapter 13) apply those values to rendered components; and Implementation Technologies consume the result. Each layer consumes the layer immediately above it without redefining it — no layer reaches backward to reinterpret a meaning a prior layer established, and no layer invents meaning of its own to pass downward. This chain is conceptual only; it introduces no implementation guidance.

Without tokens, every chapter this document has authored so far would remain a set of principles with no enforceable connection to what actually renders. Tokens are the mechanism by which `DS-001-015` (One Token, Every Surface, Chapter 3) becomes literally true rather than aspirational.

### 10.2 Token Philosophy

**DS-001-151: Semantics Before Values**
A token's identity is its meaning, not its current resolved value. "Danger" is a token because it names a meaning Chapter 6 establishes; the specific colour it resolves to is a downstream implementation detail, never the token's defining characteristic.

**DS-001-152: One Meaning, Everywhere**
A given token means the same thing on every screen, in every capability, for every tenant, in every implementation technology. This is the same discipline `DS-001-063`, `DS-001-086`, `DS-001-109`, and `DS-001-133` establish for colour, typography, iconography, and illustration respectively, generalized here to the token system that realizes all four.

**DS-001-153: Platform Independence**
A token's definition makes no assumption about the operating system, device class, or platform rendering it. This is `SD-001`'s technology-independence principle (§1.3), extended to the token layer that ultimately touches implementation.

**DS-001-154: Technology Neutrality**
A token's definition makes no assumption about the frontend framework, rendering engine, or design tool that will consume it. A token is defined by what it means, never by the syntax a particular technology uses to express it.

**DS-001-155: Evolution Without Breaking Meaning**
An implementation technology may change — a framework may be replaced, a rendering engine upgraded — without requiring any chapter of this document to be rewritten, because the token layer absorbs that change. This is the specific mechanism by which `SD-001-104`–`106` (AI provider, framework, and industry independence) extend to the visual layer.

**DS-001-156: Consistency Through Abstraction**
Consistency across the platform is achieved because every surface consumes the same token, not because every surface is independently reviewed for consistency. Abstraction is the enforcement mechanism, not a documentation convenience.

### 10.3 Token Architecture

AUREX's token system has two tiers: twenty-three **atomic token families** — the closed, frozen set this document's Document Architecture establishes — and a set of **Compositional Token Groupings**, named combinations of atomic families assembled to serve a specific enterprise or domain purpose. A compositional grouping carries no token content of its own; it exists only as a governed combination of atomic tokens.

**Atomic Token Families**

| Token Family | Purpose |
|---|---|
| Brand Tokens | Canonical brand-identity values that seed every other family — the token-level realization of Chapter 4's Brand Identity. |
| Colour Tokens | Semantic and raw colour values realizing Chapter 6's fifteen colour families. |
| Typography Tokens | Font family, scale, weight, line-height, and letter-spacing realizing Chapter 7's Reading Architecture. |
| Spacing Tokens | The base spacing scale governing padding, margin, and gap. |
| Sizing Tokens | The component dimension scale. |
| Radius Tokens | The corner-rounding scale. |
| Border Tokens | Border width and style scale. |
| Elevation Tokens | The layering/depth scale expressing containment and hierarchy. |
| Shadow Tokens | Shadow definitions bound to Elevation Tokens. |
| Opacity Tokens | The transparency scale governing disabled, overlay, and scrim states. |
| Motion Tokens | Duration and easing-curve primitives. |
| Animation Tokens | Named animation sequences composed from Motion Tokens. |
| Transition Tokens | State-change transition definitions (hover, focus, expand/collapse). |
| Icon Tokens | Icon sizing, stroke-weight, and grid alignment realizing Chapter 8's Semantic Icon Architecture. |
| Grid Tokens | Layout grid column, gutter, and margin definitions. |
| Breakpoint Tokens | Responsive viewport thresholds. |
| Z-Index Tokens | The stacking-order scale. |
| Focus Tokens | Focus-ring style and offset values. |
| Cursor Tokens | Pointer/cursor state definitions. |
| Illustration Tokens | Illustration style, palette, and sizing constraints realizing Chapter 9's Illustration Architecture. |
| Chart Tokens | Data-visualisation-specific colour, spacing, and typography values. |
| AI Tokens | AI-specific visual semantics realizing the AI provenance spectrum Chapter 6 establishes (§6.3). |
| Semantic Tokens | Purpose-named tokens (success/warning/danger/info) mapping to raw values. |
| State Tokens | Interaction-state values (default/hover/active/disabled/selected/loading). |

**DS-001-157: The Atomic Token Architecture Is a Closed, Named Set of Twenty-Three Families**
No atomic token family exists outside the twenty-three above. This set is identical to, and does not extend, the Design Token Catalogue frozen in this document's Document Architecture section. A future need that appears to require a new atomic family is resolved by proposing an extension to this closed set through constitutional review of the frozen scaffold itself (§10.9), never by an ad hoc token family invented outside it.

**Compositional Token Groupings**

**DS-001-158: Compositional Token Groupings Combine Atomic Families, They Do Not Add to Them**
*Statement.* A Compositional Token Grouping is a named combination of two or more atomic token families (above) assembled to serve a specific enterprise or domain purpose. It is not itself an atomic family, carries no token content of its own, and does not expand the closed set `DS-001-157` establishes.
*Architectural Rationale.* Certain enterprise concepts — Layout, Interaction, Accessibility, Evidence, Confidence, Marketplace — are real, recurring compositional needs, but none of them is a distinct visual substance the way colour or typography is: a layout is spacing, sizing, and grid working together; evidence is colour, icon, typography, and illustration working together. Naming these combinations lets this chapter satisfy real architectural need without inflating the atomic set every future colour, icon, or typography addition would then have to reconcile against. This mirrors how Chapter 6 already treats Accessibility Colours as "a resolution layer across... other families rather than a family with independent content of its own" (§6.3) — generalized here across the entire token system.
*Practical Implications.* A request for a new "kind" of token is evaluated first against whether it is a genuinely new visual substance (requiring atomic extension, `DS-001-157`) or a new combination of existing substances (requiring only a new named Compositional Grouping, which is a lighter-weight governance action per §10.9).

| Compositional Grouping | Composed From | Purpose |
|---|---|---|
| Layout Tokens | Grid, Spacing, Sizing | Governs how atomic spacing, sizing, and grid values combine to produce a screen's layout structure, consumed by the layout templates SD-001 defines (`SD-001-024`). |
| Interaction Tokens | State, Focus, Cursor, Transition | Governs how atomic state, focus, cursor, and transition values combine to express interactive behavior consistently across every component (Chapter 13). |
| Accessibility Tokens | Focus, Colour (Accessibility Colours, Ch. 6 §6.3), Typography, Opacity | Governs how atomic families resolve under the accessibility modes SD-001 requires to exist (`SD-001-063`) — a resolution layer across families, not independent content. |
| Evidence Tokens | Colour (Evidence Colours), Icon (Evidence Icons), Typography (Evidence Reading), Illustration (Evidence Illustrations) | Governs how the atomic families realize Evidence as one coherent visual concept — the token-level composition underlying Chapter 14 §14.1. |
| Confidence Tokens | Colour (Confidence Colours), Icon (Confidence Icons), Typography (Confidence Explanations, Ch. 7 §7.7) | Governs how the atomic families realize Confidence as one coherent visual concept — the token-level composition underlying Chapter 14 §14.2. |
| Marketplace Tokens | Icon (Marketplace Icons), Illustration (Marketplace Illustrations), Brand (Marketplace Verified Mark context, Ch. 5 §5.2) | Governs how the atomic families realize marketplace listing and category presentation, distinct from the Marketplace Verified Mark itself, which remains a Logo System asset. |

### 10.4 Semantic Principles

**DS-001-159: Tokens Represent Meaning**
*Statement.* Every token's primary identity is the meaning it carries, established in Chapters 4 through 9. A token with no traceable meaning in those chapters is not a valid AUREX token. Design Tokens SHALL NOT originate meaning: meaning SHALL be established only by the constitutional chapters that precede this one. The Token System exists solely to preserve, communicate, and consistently realize those meanings across every implementation technology.
*Architectural Rationale.* A token system with authority to originate meaning would invert this document's constitutional order: Chapters 4 through 9 would become downstream consumers of decisions made inside a chapter whose stated purpose is implementation-facing abstraction, not meaning-making. Confining meaning-origination to the preceding chapters keeps the dependency chain §10.1 establishes — Constitutional Design Principles → Semantic Meaning → Design Token System → Theme System → Component Standards → Implementation Technologies — running in one direction only, consistent with `DS-001-165` (Tokens Realize, They Do Not Redefine, Chapters 5 Through 9).
*Practical Implications.* A proposed token that does not trace to an existing meaning in Chapters 4 through 9 is not resolved by defining the meaning inside this chapter — it is resolved by first establishing that meaning in the owning chapter through constitutional review, then adding the corresponding token here. This chapter's own §10.3 and §10.8 compositional groupings follow exactly this order: each cites the owning chapter (Chapter 5, 6, 7, 8, or 9) whose meaning it realizes, never asserting a meaning independently.

**DS-001-160: Tokens Never Represent Implementation**
A token never encodes a framework-specific syntax, a file format, or a platform-specific mechanism. This is `DS-001-154` (Technology Neutrality) restated as a semantic boundary: the moment a token's definition requires knowing which technology consumes it, it has stopped being architecture.

**DS-001-161: One Token Per Semantic Concept**
Each meaning established in Chapters 4 through 9 is realized by exactly one token (atomic or compositional). Two tokens representing the same meaning fragment the consistency the token system exists to guarantee.

**DS-001-162: Token Meaning Is Immutable**
A token's meaning does not change when its resolved value changes. This is `DS-001-067A` (Semantic Colour Meaning Is Immutable, Chapter 6) generalized to the entire token system: rebrand, retheme, or re-platform may change what a token resolves to; none of them may change what the token means.

**DS-001-163: Tokens Survive Technology Change**
A token's identity and meaning persist across a change in rendering technology, framework, or design tool. Only its implementation-layer resolution mechanism changes; the token itself, and every chapter that references it by ID, does not.

**DS-001-164: Themes Resolve Tokens, They Do Not Define Them**
A theme (Chapter 11) selects which value a token resolves to in a given context; it never originates a token's meaning or existence. This is `DS-001-025` (Themes Change Appearance, Never Meaning, Chapter 3) applied at the token-system level, and the principle §10.6 elaborates in full.

### 10.5 Relationship with Previous Chapters

**DS-001-165: Tokens Realize, They Do Not Redefine, Chapters 5 Through 9**
The Design Token System exists to make the Logo System (Chapter 5), Colour System (Chapter 6), Typography (Chapter 7), Iconography (Chapter 8), and Illustration Standards (Chapter 9) implementable — it does not restate, reinterpret, or hold independent authority over any meaning those chapters establish. Where this chapter's token family table (§10.3) describes a family's purpose, that description is a pointer to the owning chapter's authority, never a competing definition. A conflict between this chapter's description of a family and the owning chapter's definition is resolved in the owning chapter's favor without exception.

### 10.6 Relationship with Theme Architecture

**DS-001-166: Tokens Define Semantics; Themes Resolve Appearance**
Tokens and themes divide labor precisely, occupying adjacent links in the dependency chain §10.1 establishes: a token (this chapter) defines what a meaning is and that it exists; a theme (Chapter 11) is the next layer downstream and defines what value that token resolves to in a specific rendering context — Light, Dark, High-Contrast, Boardroom, or a white-label brand. Neither layer performs the other's function, and neither reaches backward to redefine the layer above it. A theme that appeared to change what a token means, rather than merely what it resolves to, would indicate a defect in that theme's design (Chapter 11), not a legitimate theme variation — the same test `DS-001-050` already applies to the Logo System and `DS-001-067` applies to colour, generalized here to the full Token System Chapter 11 themes consume.

### 10.7 Accessibility

**DS-001-167: Accessibility Is Resolved Through Tokens, Not Overrides**
Accessibility modes (Chapter 17) are satisfied by resolving existing tokens differently — through the Accessibility Tokens grouping (§10.3) — never by an implementation-specific override applied outside the token system. An accessibility fix that bypasses tokens cannot be verified, propagated, or guaranteed to remain correct as the underlying tokens evolve.

**DS-001-168: Tokens Support High-Contrast Resolution Without Exception**
Every atomic token family capable of visual expression (Colour, Typography, Icon, Illustration, Border, Focus) has a defined High-Contrast resolution path through the Accessibility Tokens grouping. A token family with no such path is incomplete, consistent with SD-001's mandate that accessibility modes exist without exception (`SD-001-063`).

**DS-001-169: Tokens Support Responsive Scaling Across Devices**
Sizing, Spacing, Typography, and Grid Tokens resolve appropriately across the Breakpoint Tokens (§10.3) spectrum, ensuring the responsive behavior Chapter 16 governs is achieved through token resolution rather than device-specific hard-coding.

**DS-001-170: Tokens Preserve Multi-Device and Print Consistency**
A token's meaning, and the relative relationship between tokens (hierarchy, emphasis, semantic pairing), is preserved whether resolved for desktop, mobile, boardroom display, or print. Only the resolved value differs by context, never the meaning the token carries.

### 10.8 Enterprise Intelligence Tokens

AUREX introduces semantic token requirements for Evidence, Confidence, AI, Recommendations, Business Activities, and Governance — concepts central to the Enterprise Intelligence Fabric with no equivalent in a conventional application's token system. Evidence Tokens and Confidence Tokens are Compositional Token Groupings already established in §10.3; AI Tokens is itself an atomic family (§10.3). This section extends the same compositional treatment to Recommendations, Business Activities, and Governance.

| Compositional Grouping | Composed From | Purpose |
|---|---|---|
| Recommendation Tokens | Colour (Decision Support Colours, Ch. 6 §6.3), Icon (Action Icons, Ch. 8 §8.3), Typography (Recommendation Narratives, Ch. 7 §7.7) | Governs how atomic families realize Recommendations as a coherent visual concept distinct from confirmed data, consistent with SD-001's recommendation-never-decision principle (`SD-001-013`) — the token-level composition underlying Chapter 14 §14.5. |
| Business Activity Tokens | Icon (Business Activity Icons, Ch. 8 §8.3), Typography (`SD-001-009`), Illustration (Process, Workflow, and Learning & Guidance Illustrations, Ch. 9 §9.3) | Governs how atomic families realize named Business Activities as a recognizable, consistent visual unit — the token-level composition underlying Chapter 14 §14.8. |
| Governance Tokens | Icon (Governance Icons, Ch. 8 §8.3), Colour (Semantic Status Colours, Ch. 6 §6.3) | Governs how atomic families realize approval, audit, and governance state — the token-level composition underlying SD-001's audit-visibility and Action Center requirements (`SD-001-040`, `SD-001-043`). |

**DS-001-171: Enterprise Intelligence Token Groupings Are Compositional, Not Atomic**
*Statement.* Evidence, Confidence, Recommendation, Business Activity, and Governance Tokens are Compositional Token Groupings (`DS-001-158`) realized through the twenty-three atomic families (§10.3); AI Tokens is itself an atomic family and is not affected by this principle. None of the five compositional groupings named in this section expands the closed atomic set `DS-001-157` establishes.
*Architectural Rationale.* Enterprise Intelligence concepts are genuinely distinct in meaning (Chapters 6 §6.7, 7 §7.7, 9 §9.7 each establish this for colour, typography, and illustration respectively) without being distinct visual substances — the same relationship §10.3 establishes for Layout, Interaction, Accessibility, and Marketplace. Treating them as compositional rather than atomic keeps the token system's substance count closed while still giving Enterprise Intelligence the named, governed architecture its constitutional importance requires.
*Practical Implications.* This chapter defines the architecture only. The detailed token values these five groupings resolve to, and their visual realization, are governed downstream by Chapter 11 (Theme Architecture), Chapter 13 (Component Visual Standards), and Chapter 14 (AUREX Domain Visual Language) — no value or visual treatment is introduced here.

### 10.9 Governance

**DS-001-172: Token Evolution Is Rare and Constitutionally Reviewed**
The atomic token architecture (§10.3) changes rarely, and only through the same constitutional review discipline as any other change to this document's frozen scaffolding.

**DS-001-173: New Atomic Token Families Require Constitutional Review of the Frozen Scaffold**
A proposed twenty-fourth atomic family is admitted only through constitutional review of the Document Architecture's frozen Token Catalogue itself — never through unilateral introduction within a chapter, and never by relabeling a Compositional Token Grouping as atomic to bypass that review.

**DS-001-174: Capability Teams Shall Not Introduce Independent Token Systems**
Consistent with `DS-001-075`, `DS-001-099`, `DS-001-122`, and `DS-001-148` (colour, typography, iconography, and illustration, respectively), a capability or Business Activity team has no authority to introduce a new atomic family or Compositional Token Grouping. A capability that requires token support this chapter does not yet provide proposes an extension through the Design Governance contribution process (Chapter 22 §22.4).

**DS-001-175: White-Label Themes Consume Tokens, They Do Not Originate Them**
A tenant's or partner's white-label theme (Chapter 11, Chapter 12) resolves existing tokens to brand-specific values; it never introduces a token, atomic or compositional, that does not already exist in this chapter's architecture.

**DS-001-176: Marketing Shall Never Redefine Tokens**
A marketing or campaign use of any visual element, however it is applied outside the product surface, shall never cause a token's meaning to be reinterpreted. This is `DS-001-037` (Marketing Campaigns Shall Not Redefine the Constitutional Brand, Chapter 4) applied at the token-system level.

---

### Chapter 10 Validation

This chapter is positioned throughout as a constitutional Design Standard, not a Presentation Architecture document: the chapter title, introduction, and every general reference to the governed token system now read "Design Token System," reserving "Token Architecture" and "Design Token Catalogue" exclusively for §10.3's structural description of the frozen, closed atomic set — the distinction Improvement 1 requires. No token value, JSON structure, CSS variable, Figma variable, platform-specific mechanism, or file format appears anywhere above. The atomic token family table (§10.3) reproduces the frozen Document Architecture's Design Token Catalogue exactly — twenty-three families, no additions, no removals (`DS-001-157`) — and the six families named in this chapter's original brief that do not appear in that frozen list (Layout, Interaction, Accessibility, Evidence, Confidence, Marketplace) remain Compositional Token Groupings of existing atomic families (`DS-001-158`), not new atomic entries. `DS-001-159`, as strengthened, states explicitly that tokens SHALL NOT originate meaning — meaning is established only by Chapters 4 through 9 — closing off any reading of this chapter as a source of new design authority. The conceptual dependency chain (Constitutional Design Principles → Semantic Meaning → Design Token System → Theme System → Component Standards → Implementation Technologies) is stated in prose in §10.1, §10.6, and `DS-001-159` without any diagram or implementation guidance. Tokens remain purely semantic throughout: every principle in §10.4 defines what a token *is* and *means*, never what it *renders as*. No content in §10.5 or §10.6 restates Chapters 5–9 or anticipates Chapter 11; each instead states the boundary and defers to the owning chapter's authority.

*End of Chapter 10.*

---

## SECTION 11: Theme System

This chapter defines the constitutional principles governing the AUREX Theme System — the governed resolution layer between the Design Token System (Chapter 10) and rendered user interfaces. Themes SHALL resolve appearance. Themes SHALL NOT originate meaning. This chapter does not define CSS, theme files, JSON, variables, rendering engines, style sheets, platform-specific implementations, or design software; those belong to implementation repositories.

*A naming note before proceeding:* this chapter's brief refers to an "Executive Presentation Theme." The frozen Document Architecture's Table of Contents names the same theme class "Boardroom" (Chapter 11's frozen title: "Theme Architecture (Light / Dark / High-Contrast / Boardroom / White-label)"), and four prior chapters (3, 6, 7, 9) already cross-reference "Boardroom" by that exact name. To avoid contradicting the frozen scaffold and the terminology already published in earlier chapters, §11.3 below uses "Boardroom Theme" as the constitutional name and states explicitly that it is the class through which the Executive Presentation context is resolved.

### 11.1 Purpose

Themes exist because a single set of token meanings (Chapter 10) must still render differently across genuinely different contexts — a dim room, a boardroom display, a printed page, a partner's own brand — without any of those contexts changing what the platform is telling its user. The Theme System is the governed layer that makes this possible: it is where Semantic Meaning, already fixed by Chapters 4 through 10, is resolved into a context-specific rendering.

Themes consume tokens. Themes never redefine tokens. This is the constitutional boundary the entire chapter exists to protect: a theme is permitted to decide that "danger" renders as a particular value in Dark Theme and a different value in Light Theme, but it is never permitted to decide that a screen means something different because Dark Theme happens to be active. This is the next link in the dependency chain Chapter 10 establishes (§10.1): Constitutional Design Principles → Semantic Meaning → Design Token System → **Theme System** → Component Standards → Implementation Technologies.

### 11.2 Theme Philosophy

**DS-001-177: Appearance Follows Meaning**
A theme's entire content is an answer to "how does this already-established meaning look here?" — never to "what does this mean here?" Appearance is theme's whole jurisdiction; meaning is never within it.

**DS-001-178: Themes Consume Semantics**
A theme is a consumer of the Token System's semantics (Chapter 10), positioned exactly where §11.1's dependency chain places it. A theme that behaved as an independent source of meaning would collapse the one-directional chain that chain depends on.

**DS-001-179: Themes Never Redefine Meaning**
This is the theme-level restatement of `DS-001-164` (Themes Resolve Tokens, They Do Not Define Them, Chapter 10) and `DS-001-025` (Themes Change Appearance, Never Meaning, Chapter 3): no theme, current or future, may alter what a token, colour, icon, or illustration means. A theme proposal that would require a meaning change is not a theme proposal — it is a change request against the owning chapter (4 through 9), to be resolved there first.

**DS-001-180: Consistency Across Themes**
The same interaction, in the same context, produces the same experience of meaning regardless of which theme is active. A user moving from Light to Dark Theme, or from a tenant's white-label theme to AUREX's default, never has to relearn what a colour, icon, or status indicator means.

**DS-001-181: Theme Technology Independence**
A theme's definition makes no assumption about the rendering technology, framework, or platform that will implement it. This is `DS-001-154` (Technology Neutrality, Chapter 10) extended to the resolution layer.

**DS-001-182: Evolution Without Semantic Change**
A theme may be refined, extended, or re-rendered as implementation technology evolves without requiring any change to the meanings Chapters 4 through 10 establish. This is the theme-level expression of `DS-001-155` (Evolution Without Breaking Meaning, Chapter 10).

### 11.3 Theme Model

AUREX defines five constitutional theme classes. These are constitutional theme classes, not implementation assets — no file, stylesheet, or rendering artifact is defined here.

| Theme Class | Purpose |
|---|---|
| Light Theme | The default, high-luminance rendering context for standard working conditions. |
| Dark Theme | The reduced-luminance rendering context for low-ambient-light conditions, preserving every semantic meaning Light Theme carries. |
| High-Contrast Theme | The accessibility-mandated rendering context satisfying SD-001's requirement that high-contrast, colour-vision-safe modes exist without exception (`SD-001-063`). |
| Boardroom Theme | The large-format, low-interaction, low-motion rendering context for shared executive and governance displays, satisfying SD-001's Boardroom Display Modes requirement (`SD-001-074`) and expressing the calm executive tone `DS-001-016` and `SD-001-056` establish. Boardroom Theme is the constitutional class through which the Executive Presentation context named in this chapter's brief is resolved. |
| White-label Theme | The tenant- or partner-branded rendering context, resolving Brand Tokens (Chapter 10, §10.3) to a customer's or partner's own identity within the governance §11.6 establishes. |

**DS-001-183: The Theme Model Is a Closed, Named Set of Five Classes**
No theme exists outside the five classes above. A future need that appears to require a new theme class is resolved by proposing an extension to this closed set through constitutional review (§11.9), never by an ad hoc rendering context invented outside it. This is `DS-001-027` (Extend, Never Fork) applied to the Theme System.

### 11.4 Theme Principles

**DS-001-184: One Meaning Across Every Theme**
A token's meaning is identical across all five theme classes. This is `DS-001-152` (One Meaning, Everywhere, Chapter 10) applied specifically to theme resolution.

**DS-001-185: Themes Resolve Tokens**
*Statement.* A theme's function is to assign each token a context-appropriate value. This is the theme's entire positive function; nothing else is within a theme's authority. Themes SHALL resolve every governed Design Token through an approved Theme Class (§11.3). No governed Design Token SHALL remain unresolved. A theme SHALL NOT bypass the Design Token System. Every rendered experience SHALL be produced only through Theme resolution of governed Design Tokens.
*Architectural Rationale.* A token left unresolved by every approved Theme Class is a meaning Chapters 4 through 10 have established with no path to ever actually rendering — a silent gap between architecture and the rendered experience this document exists to govern. Requiring total resolution closes that gap structurally: it is not sufficient for a theme to resolve only the tokens a designer happened to reach for, because Chapter 10's atomic and compositional catalogue (§10.3, §10.8) is the complete governed vocabulary, and any subset left unresolved would mean some constitutional meaning has no way to become visible.
*Practical Implications.* Introducing a new atomic family or Compositional Token Grouping in Chapter 10 (per `DS-001-173`, constitutional review of the frozen scaffold) carries an implicit obligation for every one of the five Theme Classes (§11.3) to resolve it before that addition is considered complete — a new token with no corresponding resolution in Light, Dark, High-Contrast, Boardroom, and White-label Theme is an incomplete constitutional change, not merely an incomplete implementation detail.

**DS-001-186: Themes Never Create Tokens**
A theme has no authority to introduce a token, atomic or compositional, that does not already exist in Chapter 10's architecture. This is `DS-001-175` (White-Label Themes Consume Tokens, They Do Not Originate Them, Chapter 10) generalized to every theme class, not white-label alone.

**DS-001-187: Themes Never Bypass Tokens**
An implementation resolving a theme SHALL do so entirely through the token system; no theme may specify a value that does not resolve through a governed token. This is `DS-001-092`, `DS-001-115`, and `DS-001-139`'s "resolved only through tokens" discipline (typography, iconography, illustration), generalized here to the resolution layer as a whole.

**DS-001-188: Themes Preserve Accessibility**
No theme class, including Light and Dark Theme, may resolve a token in a manner that falls below the accessibility baseline SD-001 establishes as non-optional (`SD-001-059`). Accessibility is not a property of the High-Contrast theme alone; it is a property every theme must satisfy.

**DS-001-189: Themes Preserve Enterprise Intelligence Semantics**
No theme class may resolve an Evidence, Confidence, AI, Recommendation, Business Activity, or Governance Token grouping (Chapter 10, §10.3, §10.8) in a way that obscures the distinction those groupings exist to preserve (`DS-001-072A`, Chapter 6). §11.8 states this principle in full.

### 11.5 Relationship with the Design Token System

The Token System (Chapter 10) defines semantic meaning. The Theme System (this chapter) resolves token values. These are adjacent, non-overlapping links in the dependency chain §11.1 establishes.

**DS-001-190: Themes Consume Only Governed Design Tokens**
Themes SHALL consume only the atomic families and Compositional Token Groupings Chapter 10 defines (§10.3, §10.8). No theme may resolve a value that does not trace to a governed token. This is the theme-level enforcement mechanism for `DS-001-165` (Tokens Realize, They Do Not Redefine, Chapters 5 Through 9): if themes could resolve values outside the token system, that system's guarantee of realizing — never redefining — the constitutional chapters would no longer hold at the rendering layer.

### 11.5A Theme Resolution Order

Every rendered experience is produced through the same governed semantic flow, extending the dependency chain §11.1 introduces one layer further:

Constitutional Design Principles → Semantic Meaning → Design Token System → Theme System → Component Standards → Rendered Experience

Each downstream layer consumes the output of the layer immediately above it; no downstream layer may redefine any upstream layer. Within this sequence: Themes resolve Design Tokens (§11.4, §11.5). Components (Chapter 13) consume resolved Themes. Rendered interfaces consume Components. This subsection is conceptual only; it introduces no CSS, JSON, variable, rendering engine, style sheet, or platform-specific implementation.

**DS-001-190A: The Theme Resolution Order Is Strictly One-Directional**
*Statement.* The resolution sequence — Constitutional Design Principles, Semantic Meaning, Design Token System, Theme System, Component Standards, Rendered Experience — proceeds in one direction only. No layer reaches backward to alter a decision an upstream layer has already made, and no layer is permitted to skip a layer between itself and the meaning it ultimately depends on.
*Architectural Rationale.* This is the same one-directional discipline `DS-001-159`'s Architectural Rationale (Chapter 10) establishes for the Token System specifically, extended here across the full chain through Component Standards and the Rendered Experience. A bidirectional or skip-permitting chain would allow a downstream layer — a component's implementation, or a theme's own resolution logic — to originate meaning by accident, precisely the failure `DS-001-179` (Themes Never Redefine Meaning) exists to prevent.
*Practical Implications.* A component (Chapter 13) that requires a visual value not already resolved by a theme is never satisfied by having the component define that value directly — the gap is resolved by extending the Theme System's resolution (§11.5A) or, if the underlying token itself is missing, the Design Token System (Chapter 10), always moving the fix upstream to the correct layer rather than downstream around it.

### 11.6 White-label Themes

**DS-001-191: White-Label Themes Realize Chapter 4's Brand Tiers, They Do Not Add to Them**
*Statement.* Customer, Partner, Marketplace, and Corporate branding within the Theme System resolve to the four-tier brand model Chapter 4 establishes (§4.5) — Product, Tenant, Partner, and Marketplace Brand. Customer branding and Corporate branding both realize Tenant Brand; Partner branding realizes Partner Brand; Marketplace branding realizes Marketplace Brand. No white-label theme introduces a fifth, independent brand tier.
*Architectural Rationale.* Chapter 4 already closed the brand-tier question (`DS-001-035`, The Four-Tier Brand Model Is Fixed); a Theme System that recognized a different branding taxonomy at the resolution layer would silently reopen a question Chapter 4 settled, in exactly the way `DS-001-179` prohibits.
*Practical Implications.* Detailed token-mapping mechanics for white-label branding are governed by Chapter 12 (White-Label Branding & Multi-Brand Token Mapping); this chapter establishes only that such branding is a Theme System resolution, never an independent branding mechanism outside it.

**DS-001-192: Brand Customization Remains Within the Constitutional Theme System**
Brand customization SHALL remain within the Theme System's governed resolution mechanism (White-label Theme, §11.3); no tenant, partner, or marketplace brand customization may introduce a rendering path outside it. This is the theme-level enforcement of `DS-001-033` (White-Label Shall Never Obscure the AUREX Identity, Chapter 4) and `DS-001-076` (White-Label Colour Remains Governed, Chapter 6).

### 11.7 Accessibility

**DS-001-193: The High-Contrast Theme Satisfies SD-001's Accessibility Mandate Without Exception**
High-Contrast Theme (§11.3) is the constitutional realization of SD-001's requirement that a high-contrast mode exist (`SD-001-063`); it resolves every token family capable of visual expression, with no family exempted.

**DS-001-194: Every Theme Supports the Accessibility Modes SD-001 Requires**
Reduced-motion and large-text accessibility modes (`SD-001-063`) are supported identically across all five theme classes, not only within High-Contrast Theme. Accessibility mode and theme class are independent, orthogonal selections.

**DS-001-195: Themes Preserve Meaning Under Print Rendering**
A theme's resolution to printed media preserves the meaning every token carries, even where the specific rendered value necessarily differs from any screen-based theme. This is `DS-001-071` (The Colour System Remains Coherent Across Dark Mode and Print, Chapter 6) generalized to the full Theme System.

**DS-001-196: Themes Preserve Meaning Under Responsive Rendering**
A theme's resolution across viewport sizes (Chapter 16) preserves meaning identically at every breakpoint; only density and layout, governed by Layout Tokens (Chapter 10, §10.3), vary.

**DS-001-197: Themes Preserve Multi-Device Consistency**
A user encountering the same content under the same theme on different devices receives the same meaning, rendered appropriately to each device's context. This is `DS-001-170` (Tokens Preserve Multi-Device and Print Consistency, Chapter 10) applied at the theme-resolution layer.

### 11.8 Enterprise Intelligence Themes

Enterprise Intelligence introduces additional visual resolution requirements for Evidence, Confidence, AI, Recommendations, Governance, and Business Activities — the Compositional Token Groupings Chapter 10 establishes for these concepts (§10.3, §10.8). Themes resolve these semantic concepts. They never redefine them.

**DS-001-198: Themes Resolve Enterprise Intelligence Token Groupings, They Never Redefine Them**
*Statement.* The Evidence, Confidence, AI, Recommendation, Business Activity, and Governance Token groupings are resolved, not redefined, by every theme class in §11.3. A theme may change how Evidence Tokens render in Dark Theme versus Light Theme; it never changes what Evidence, Confidence, or any other Enterprise Intelligence concept means.
*Architectural Rationale.* These groupings carry constitutional weight distinct from ordinary visual preference (`DS-001-072A`, Chapter 6) precisely because they are how SD-001's evidence-first, explainable presentation mandate (`SD-001` §1.6) is made visible at all. A theme permitted to reinterpret them would be permitted, indirectly, to weaken that mandate simply by shipping a new theme — the exact failure mode `DS-001-179` exists to foreclose.
*Practical Implications.* A Boardroom Theme rendering of a Confidence Token, for instance, may be visually calmer and less saturated than its Light Theme rendering (consistent with `DS-001-016`), but it shall communicate the identical confidence level. Detailed token values for each theme's resolution of these groupings are an implementation-repository concern, not defined here.

### 11.9 Governance

**DS-001-199: Theme Evolution Is Rare and Constitutionally Reviewed**
The Theme Model defined in §11.3 changes rarely, and only through the same constitutional review discipline as any other change to this document.

**DS-001-200: New Theme Classes Require Constitutional Review**
A proposed sixth theme class is admitted only through constitutional review of this chapter — never through unilateral introduction by a design contributor, capability team, or implementation effort.

**DS-001-201: Capability Teams Shall Not Introduce Theme Systems**
Consistent with `DS-001-174` (Capability Teams Shall Not Introduce Independent Token Systems, Chapter 10) and the equivalent principles in Chapters 6 through 9, a capability or Business Activity team has no authority to introduce a new theme class or an independent resolution mechanism. A capability that requires theme support this chapter does not yet provide proposes an extension through the Design Governance contribution process (Chapter 22 §22.4).

**DS-001-202: White-Label Themes Consume Tokens, They Do Not Originate Them**
This restates `DS-001-175` (Chapter 10) as this chapter's own governing rule for the Theme System specifically: a white-label theme resolves existing tokens to brand-specific values and never introduces a token that does not already exist in Chapter 10's architecture.

**DS-001-203: Marketing Shall Never Redefine Themes**
A marketing or campaign use of any visual element, however it is applied outside the product surface, shall never cause a theme's resolution of a token to be reinterpreted as a change in meaning. This is `DS-001-176` (Marketing Shall Never Redefine Tokens, Chapter 10) applied specifically to theme resolution.

---

### Chapter 11 Validation

This chapter defines the Theme System's constitutional resolution role, not its implementation: no CSS, theme file, JSON, variable, rendering engine, style sheet, platform-specific implementation, or design software appears anywhere above, including within the strengthened `DS-001-185` and the new §11.5A Theme Resolution Order, both of which state resolution obligations and sequencing in prose only. Every principle enforces the same boundary from a different angle — themes resolve appearance, they never originate meaning (`DS-001-177`–`179`, `DS-001-185`–`187`, `DS-001-190A`, `DS-001-198`) — and every principle that touches Enterprise Intelligence content (§11.8) or white-label branding (§11.6, unchanged by this refinement) explicitly defers redefinition authority to Chapter 4, Chapter 6, or Chapter 10 rather than asserting it here. The "Executive Presentation Theme" named in this chapter's original brief is reconciled, not silently renamed or silently dropped, to "Boardroom Theme" — the name the frozen Document Architecture and four prior chapters already use — with the reconciliation stated explicitly at the top of this chapter. Themes consume only governed Design Tokens throughout (`DS-001-190`) and are now required to resolve every one of them without exception (`DS-001-185`); the dependency chain extended by §11.5A (`DS-001-190A`) remains strictly one-directional through Component Standards and the Rendered Experience, with no overlap into Chapter 10's or Chapter 12's territory. The Theme Classes (§11.3) and white-label governance (§11.6) are unchanged by this refinement. The Theme System remains technology-independent throughout.

*End of Chapter 11.*

---

## SECTION 12: White-label Branding & Multi-Brand Token Mapping

This chapter defines the constitutional principles governing how multiple brands coexist within AUREX without changing semantic meaning. It governs how Corporate, Tenant, Partner, and Marketplace Brand are realized through the Theme System (Chapter 11) and Design Token System (Chapter 10). Branding customizes appearance. Branding SHALL NEVER customize meaning. This chapter does not define logos, brand assets, CSS, JSON, variables, theme files, rendering engines, platform-specific implementations, or design software; those belong to Chapter 5, Chapter 4, or implementation repositories.

*A naming note before proceeding:* this chapter's brief names AUREX's own brand tier "Corporate Brand." Chapter 4 §4.5 names this same tier "Product Brand" — one of its four constitutional tiers, alongside Tenant, Partner, and Marketplace Brand. §12.3 below maps "Corporate Brand" to Chapter 4's "Product Brand" directly, adding no fifth tier. Separately, Chapter 11's `DS-001-191` already used the lowercase phrase "Corporate branding" in a narrower, scenario-level sense — describing a large enterprise customer's branding request, which that principle correctly classifies as an instance of **Tenant** Brand. That usage predates this chapter, cannot be revised here, and is not in conflict with this chapter's terminology once the two are distinguished: Chapter 11's "corporate branding" names a *customer scenario* realized through Tenant Brand; this chapter's "Corporate Brand" names AUREX's own *constitutional tier*, equivalent to Chapter 4's Product Brand. §12.5 below addresses the Chapter 11 scenario explicitly, under Customer Branding, to remove any ambiguity.

### 12.1 Purpose

Multi-brand capability exists because every enterprise AUREX serves has its own identity, and the platform's presentation must be able to express that identity without becoming a different platform in the process. An organization may see its own brand throughout its AUREX deployment; a partner may deliver AUREX under its own name; a marketplace extension may carry its author's identity — and in every case, the Enterprise Intelligence being presented, and everything SD-001 and this document require of how it is presented, remains identical underneath.

White-label Branding is not an independent capability. It is a governed realization of Chapter 4's Brand Identity, expressed entirely through the Theme System (Chapter 11) resolving the Design Token System (Chapter 10). This chapter defines the constitutional principles that keep that realization governed rather than open-ended.

**DS-001-204: One Semantic System**
Every brand variant AUREX renders is a presentation of the same underlying semantic system Chapters 4 through 11 establish. There is no brand-specific fork of what a colour, icon, confidence indicator, or evidence panel means.

### 12.2 White-label Philosophy

**DS-001-205: Multiple Brand Identities**
AUREX supports an unbounded number of tenant, partner, and marketplace brand identities simultaneously, each fully realized, none compromising another. Multiplicity of appearance is a design goal; multiplicity of meaning is not.

**DS-001-206: Appearance Follows Meaning**
This restates `DS-001-177` (Chapter 11) at the brand-resolution layer: a brand's presentation is always an answer to "how does this already-established meaning look for this organization?" — never to "what does this mean for this organization?"

**DS-001-207: Branding Preserves Trust**
A brand variant is evaluated by whether it preserves the trust SD-001's evidence and confidence architecture builds (`SD-001-010`–`014`) and Chapter 4 requires branding to reinforce, never compete with (`DS-001-031`). A brand treatment that makes evidence harder to find or confidence harder to read has failed regardless of how faithfully it expresses the tenant's identity.

**DS-001-208: Brand Independence**
Chapters 4 through 11 remain fully valid with no brand variant applied at all — the AUREX default identity — and remain equally valid under any number of brand variants. No chapter's principles depend on a specific brand being active.

**DS-001-209: Technology Independence**
A brand's realization makes no assumption about the platform, framework, or rendering technology that implements it, consistent with `DS-001-153`–`154` (Chapter 10) and `DS-001-181` (Chapter 11) extended to the brand-resolution layer.

### 12.3 Constitutional Brand Mapping

This chapter governs exactly the four brand tiers Chapter 4 §4.5 already establishes. No tier is added, removed, or redefined here.

| This Chapter's Term | Chapter 4 Term (§4.5) | Realization |
|---|---|---|
| Corporate Brand | Product Brand | AUREX's own constitutional identity — present, at minimum by attribution, in every deployment (`DS-001-032`, `DS-001-033`). |
| Tenant Brand | Tenant Brand | A customer organization's own branding, realized through White-label Theme (Chapter 11, §11.3). |
| Partner Brand | Partner Brand | A reseller's or systems integrator's branding, subject to the same constitutional floor as Tenant Brand (`DS-001-033`). |
| Marketplace Brand | Marketplace Brand | A marketplace extension's authorship identity (SD-001 §14), never extending to the platform surface the extension appears within. |

**DS-001-210: Corporate Brand Realizes Chapter 4's Product Brand, No Tier Is Added**
*Statement.* "Corporate Brand," as used throughout this chapter, is the constitutional name for the tier Chapter 4 §4.5 defines as "Product Brand." The two terms name the same tier. This chapter's four-tier mapping table (§12.3) is exhaustive; no fifth tier exists anywhere in this chapter's principles.
*Architectural Rationale.* Chapter 4 closed the brand-tier question with `DS-001-035` (The Four-Tier Brand Model Is Fixed). A chapter governing multi-brand token mapping that appeared to recognize a different or additional taxonomy would silently reopen that closed question, in exactly the way `DS-001-179` (Chapter 11) prohibits for theme resolution generally.
*Practical Implications.* Every principle in this chapter that refers to "Corporate Brand" is, without exception, referring to Chapter 4's Product Brand tier. Where this chapter's own text or a prior chapter (Chapter 11, `DS-001-191`) uses "corporate" in a different, scenario-level sense, §12.5 disambiguates that usage explicitly rather than allowing two meanings to coexist silently.

### 12.4 Multi-Brand Token Mapping

Brand identity is realized through a fixed conceptual sequence: Brand Identity (Chapter 4) is expressed as Brand Tokens (Chapter 10, §10.3); Brand Tokens are resolved by the Theme System (Chapter 11, specifically White-label Theme, §11.3); and that resolution produces the Rendered Experience. This is the same one-directional discipline `DS-001-190A` (Chapter 11) establishes, applied specifically to brand.

**DS-001-211: Brand Mapping Consumes the Design Token System; It Neither Originates Meaning Nor Creates Tokens**
*Statement.* Brand mapping SHALL consume the Design Token System (Chapter 10) exclusively. Brand mapping SHALL NOT originate semantic meaning. Brand mapping SHALL NOT create Design Tokens. Brand mapping SHALL NOT bypass the Theme System.
*Architectural Rationale.* Brand mapping sits at the same layer §11.5A places Theme resolution generally — it is not a separate channel alongside the Theme System, but a specific, governed use of it (White-label Theme, §11.3). Permitting brand mapping to originate meaning, invent tokens, or resolve values outside the Theme System would create exactly the kind of parallel, ungoverned rendering path `DS-001-192` (Chapter 11) already prohibits.
*Practical Implications.* A tenant or partner requesting a brand treatment the current Brand Tokens (Chapter 10, §10.3) cannot express is not satisfied by inventing a one-off value for that tenant — the request is resolved by extending Chapter 10's token architecture through constitutional review (`DS-001-173`), after which every brand, not only the requesting one, may draw on the extension.

### 12.5 White-label Resolution Principles

Customer, Partner, Marketplace, Subsidiary, and Regional branding are not additional tiers beyond the four §12.3 establishes — each is a governed resolution scenario realized within one of those four tiers.

| Resolution Scenario | Realized Through | Note |
|---|---|---|
| Customer Branding | Tenant Brand | Includes the "corporate branding" scenario Chapter 11's `DS-001-191` names — a large enterprise customer's own identity, realized as any Tenant Brand is. |
| Partner Branding | Partner Brand | As defined in §12.3. |
| Marketplace Branding | Marketplace Brand | As defined in §12.3. |
| Subsidiary Branding | Tenant Brand | A single tenant operating multiple subsidiary-level brand variations remains one Tenant Brand realization with multiple governed White-label Theme instances, never a separate tier per subsidiary. |
| Regional Branding | Tenant Brand or Partner Brand | Region-specific presentation needs are resolved within the tenant's or partner's existing tier, coordinated with the localization model Chapter 13 (Internationalization, SD-001 §13) governs — never as an independent brand tier keyed to geography. |

**DS-001-212: All Branding Variations Are Governed Resolutions of One Semantic Platform**
Every scenario in the table above — however many instances a single tenant or partner requires — resolves through the four constitutional tiers §12.3 establishes and the Theme System §12.4 governs. No volume or complexity of brand variation creates a new tier, a new resolution mechanism, or an exception to `DS-001-211`.

**DS-001-212A: Brand Resolution Shall Never Be Detectable Through Behavior**
*Statement.* Brand Resolution SHALL affect visual identity only. Brand Resolution SHALL NEVER alter Navigation, User Workflows, Permissions, Business Rules, Enterprise Intelligence, Interaction Behaviour, Platform Capabilities, or Functional Outcomes.
*Architectural Rationale.* Brand Resolution exists solely to express organizational identity. Platform behaviour belongs to the Enterprise Platform, not to Brand Resolution. A user should immediately recognize the organization's visual identity without experiencing a different product. Branding customizes appearance. Branding SHALL NEVER customize behaviour. This is the behavioral counterpart to `DS-001-206` (Appearance Follows Meaning) and `DS-001-213` (Branding Preserves Enterprise Intelligence Semantics): where those principles guard what a brand may mean, this principle guards what a brand may do — and closes the same boundary Chapter 2's Ownership Matrix drew at the outset between SD-001 (Presentation Architecture, which owns Navigation, Guided Completion, and Adaptive Experience) and DS-001 (which owns none of them).
*Practical Implications.* Two organizations operating under different brands, but with identical permissions, configuration, subscriptions, and data, SHALL experience identical platform behaviour. Any behavioural difference between them is governed by platform configuration, authorization, licensing, or business rules — never by Brand Resolution. A brand proposal that would require a navigation item to appear, a workflow step to be skipped, or a capability to be unlocked is not a Brand Resolution request; it is a configuration, authorization, or business-rule request routed to SD-001, SD-002, or URA-001, never satisfied within this chapter's mechanism.

### 12.6 Enterprise Intelligence Branding

**DS-001-213: Branding Preserves Enterprise Intelligence Semantics Without Exception**
*Statement.* Evidence, Confidence, AI, Recommendation, Governance, and Business Activity semantics — the Compositional Token Groupings Chapter 10 establishes (§10.3, §10.8) and every theme resolves without redefinition (`DS-001-198`, Chapter 11) — are preserved identically under every brand this chapter governs. Branding may alter appearance. Branding SHALL NEVER alter semantic interpretation.
*Architectural Rationale.* Brand resolution is downstream of Theme resolution in the dependency chain this chapter extends (§12.4); `DS-001-198` already forecloses theme-level reinterpretation of these groupings, and a brand variant that reopened what a theme has already closed would violate that principle indirectly rather than directly — a distinction without a difference from the standpoint of SD-001's evidence-first mandate (`SD-001` §1.6).
*Practical Implications.* A tenant's or partner's brand may render a Confidence Token in that brand's own palette and typographic voice, but the confidence level communicated, and a user's ability to correctly read it, remains identical to the AUREX default. A brand request that would require softening, obscuring, or reinterpreting an Evidence, Confidence, AI, Recommendation, Governance, or Business Activity signal is declined as a brand request and, if genuinely warranted, redirected to constitutional review of the owning chapter.

### 12.7 Accessibility

**DS-001-214: Branding Shall Never Weaken Accessibility**
No brand variant, however faithfully it expresses a tenant's or partner's identity, may resolve a token below the accessibility baseline SD-001 establishes as non-optional (`SD-001-059`) or that `DS-001-188` (Chapter 11) requires of every theme. Brand identity and accessibility compliance are never traded against each other.

**DS-001-215: High-Contrast Theme Functions Identically Under Every Brand**
High-Contrast Theme (Chapter 11, §11.3) resolves correctly regardless of which brand's tokens it is resolving. A brand's palette may inform High-Contrast Theme's specific values; it may never disable or degrade High-Contrast Theme's function.

**DS-001-216: Responsive and Print Rendering Remain Consistent Under Every Brand**
The responsive and print-rendering consistency `DS-001-195`–`197` (Chapter 11) establish for every theme holds identically for every brand resolved through those themes. A brand variant that functions correctly only at one viewport or only on screen, never in print, is incomplete.

### 12.8 Governance

**DS-001-217: Brand Evolution Requires Constitutional Review**
Changes to the four-tier brand mapping (§12.3) or the resolution scenarios (§12.5) SHALL be made only through the same constitutional review discipline as any other change to this document.

**DS-001-218: New Brand Categories Require Constitutional Approval**
A proposed fifth brand tier, or a proposed resolution scenario that does not map to one of the four existing tiers, is admitted only through constitutional review — never through unilateral introduction by a design contributor, capability team, or implementation effort.

**DS-001-219: Capability Teams Shall Not Introduce Branding Systems**
Consistent with `DS-001-201` (Capability Teams Shall Not Introduce Theme Systems, Chapter 11) and the equivalent principles in Chapters 6 through 10, a capability or Business Activity team has no authority to introduce a new brand tier, resolution scenario, or independent branding mechanism.

**DS-001-220: Marketing Shall Not Redefine Constitutional Branding**
A marketing or campaign use of any brand variant, however it is applied outside the product surface, shall never cause this chapter's four-tier mapping or resolution principles to be reinterpreted. This is `DS-001-203` (Marketing Shall Never Redefine Themes, Chapter 11) applied specifically to multi-brand token mapping.

**DS-001-221: White-Label Implementations Consume Governed Themes**
Every white-label implementation SHALL consume the Theme System's governed White-label Theme (Chapter 11, §11.3) exclusively; no implementation may render brand-specific appearance through a mechanism outside it.

**DS-001-222: White-Label Implementations Consume Governed Design Tokens**
Every white-label implementation SHALL consume the Design Token System's governed Brand Tokens (Chapter 10, §10.3) exclusively; no implementation may introduce a brand-specific value that does not resolve through a governed token, consistent with `DS-001-211`.

---

### Chapter 12 Validation

This chapter governs brand resolution as a constitutional concern, not an implementation: no logo, brand asset, CSS, JSON, variable, theme file, rendering engine, platform-specific implementation, or design software appears anywhere above. The "Corporate Brand" terminology collision between this chapter's brief and Chapter 11's `DS-001-191` is named and resolved explicitly (chapter-opening note, §12.3, `DS-001-210`) rather than left for a reader to discover as an inconsistency, and no tier beyond Chapter 4's existing four is introduced (`DS-001-218`). Branding never changes semantic meaning throughout (`DS-001-206`, `DS-001-213`); branding consumes Themes (`DS-001-221`); Themes consume Design Tokens (Chapter 11, `DS-001-190`); Design Tokens preserve constitutional meaning (Chapter 10, `DS-001-159`, `DS-001-162`). Enterprise Intelligence semantics remain unchanged under every brand without exception (`DS-001-213`). `DS-001-212A` establishes Brand Resolution as a purely visual identity layer, explicitly barred from altering navigation, workflows, permissions, business rules, Enterprise Intelligence, interaction behaviour, platform capabilities, or functional outcomes — behaviour remains the exclusive concern of SD-001, SD-002, and URA-001, never of this chapter. The extended dependency chain — Constitutional Design Principles → Semantic Meaning → Design Token System → Theme System → **Brand Resolution** → Component Standards → Rendered Experience — is stated in prose only (§12.4), with no diagram and no implementation guidance, and this chapter's own content occupies exactly the Brand Resolution link, without redefining Chapter 4, Chapter 10, or Chapter 11.

*End of Chapter 12.*

---

## SECTION 13: Component Visual Standards

This chapter defines the constitutional principles governing Component Visual Standards within AUREX. Components are the first reusable visual building blocks that consume the outputs of the Design Token System (Chapter 10), Theme System (Chapter 11), and Brand Resolution (Chapter 12). Components SHALL NOT originate semantic meaning. Components SHALL consume governed Themes. Components SHALL preserve constitutional meaning. This chapter does not define React, Angular, or Vue components, HTML, CSS, Figma components, design libraries, code generation, or any rendering implementation; those belong to implementation repositories.

*A naming note before proceeding:* this chapter's brief organizes components as Primitive, Composite, Layout, Navigation, Data Presentation, and Enterprise Intelligence Components. The frozen Document Architecture's Component Catalogue instead names nine categories: Foundation, Layout, Navigation, Interaction, Enterprise Intelligence, Evidence, Visualization, Collaboration, and Executive Components. §13.3 below reconciles the two directly rather than silently favoring one: "Primitive" and "Foundation" name the same tier; "Composite" names the structural relationship every other frozen category already has to that tier, not an additional category; "Data Presentation" and "Visualization" name the same category. The frozen catalogue's remaining categories (Interaction, Evidence, Collaboration, Executive) are preserved in full — this chapter's brief says "such as," not "only," and no frozen category is dropped.

### 13.1 Purpose

Components exist because Chapters 4 through 12 establish meaning, tokens, themes, and brand resolutions that must still be assembled into something a user actually encounters as a single, recognizable interface element. A Component is the reusable, consistent visual realization of everything upstream of it: it provides one governed form for "a button," "an evidence panel," or "an executive summary tile" so that meaning already established does not have to be reassembled differently every time it appears.

Components are the point in the dependency chain (§13.4) where constitutional meaning becomes a concrete, reusable visual unit. Without a governed Component layer, every screen that needed to express the same meaning would be free to assemble tokens, themes, and brand resolution differently, defeating `DS-001-014` (One Visual Language, Chapter 3) at the exact layer where a user actually looks.

### 13.2 Component Philosophy

**DS-001-223: Components Consume Meaning**
A component's visual form realizes meaning Chapters 4 through 12 already establish. It does not interpret that meaning independently.

**DS-001-224: Components Never Create Meaning**
A component has no authority to introduce a colour, icon, typographic treatment, or brand expression that does not already trace to a governed token, theme, or brand resolution. This is `DS-001-165` (Tokens Realize, They Do Not Redefine, Chapters 5 Through 9) extended one layer further, to the components that consume tokens.

**DS-001-225: Components Maximize Consistency**
A component's value is precisely that it renders identically everywhere it is used. This is `DS-001-018` (Consistency Before Creativity, Chapter 3) realized structurally: consistency is not achieved by each screen being reviewed for it, but by every screen using the same governed component.

**DS-001-226: Components Remain Technology Independent**
A component's definition makes no assumption about the frontend framework, rendering engine, or platform that will implement it, consistent with `DS-001-154` (Chapter 10), `DS-001-181` (Chapter 11), and `DS-001-209` (Chapter 12) extended to the component layer.

**DS-001-227: Components Preserve Accessibility**
No component may render in a manner that falls below the accessibility baseline SD-001 establishes as non-optional (`SD-001-059`) or that `DS-001-188` (Chapter 11) requires of every theme a component consumes. §13.6 states this principle in full.

**DS-001-228: Components Preserve Enterprise Intelligence Semantics**
No component rendering Evidence, Confidence, AI, Recommendation, Governance, or Business Activity content may obscure the distinctions those Compositional Token Groupings exist to preserve (Chapter 10, §10.3, §10.8; Chapter 11, `DS-001-198`). §13.5 states this principle in full.

### 13.3 Component Taxonomy

| This Chapter's Term | Frozen Catalogue Category | Relationship |
|---|---|---|
| Primitive Components | Foundation Components | The same tier — the atomic, non-decomposable visual elements (Button, Input Field, Icon, Badge, and the rest of the frozen Foundation list) every other category is built from. |
| Composite Components | Layout, Navigation, Interaction, Enterprise Intelligence, Evidence, Visualization, Collaboration, and Executive Components | Names the structural relationship, not an additional category: each of the frozen catalogue's other eight categories is, by construction, assembled from Primitive Components combined through Layout Tokens (Chapter 10, §10.3). |
| Layout Components | Layout Components | Exact match. |
| Navigation Components | Navigation Components | Exact match. |
| Data Presentation Components | Visualization Components | The same category — chart, table, and quantitative-display components. |
| Enterprise Intelligence Components | Enterprise Intelligence Components and Evidence Components | Both frozen categories together realize this chapter's Enterprise Intelligence scope; §13.5 addresses both explicitly. |

**DS-001-229: The Component Taxonomy Realizes the Frozen Nine-Category Catalogue Through a Primitive/Composite Structure**
*Statement.* Every component in AUREX belongs to exactly one of the frozen catalogue's nine categories, and is additionally classified as Primitive (Foundation Components only) or Composite (every other category). This two-dimensional structure is a description of the frozen catalogue, not a replacement for it.
*Architectural Rationale.* The Primitive/Composite distinction mirrors the Atomic/Compositional structure Chapter 10 establishes for tokens (`DS-001-158`): just as a Compositional Token Grouping carries no content of its own and exists only as a governed combination of atomic tokens, a Composite Component carries no visual substance beyond what its constituent Primitive Components and Layout Tokens already provide. Naming this relationship lets the taxonomy answer "what is this component built from" without requiring the frozen catalogue itself to be restructured.
*Practical Implications.* A request for a "new kind" of component is evaluated first against whether it is a genuinely new Primitive (requiring extension of Foundation Components, subject to `DS-001-233`) or a new Composite assembled from existing Primitives (a lighter-weight design exercise within an existing frozen category). No frozen category is renamed, merged, or removed by this classification.

### 13.4 Component Composition

Components consume Brand Resolution (Chapter 12), which resolves through the Theme System (Chapter 11), which resolves Design Tokens (Chapter 10) — the same one-directional chain §12.4 and `DS-001-190A` (Chapter 11) establish, extended one layer further to arrive at Components.

**DS-001-230: Components Consume Brand Resolution, Theme System, and Design Tokens Without Exception**
*Statement.* Components SHALL consume Brand Resolution, the Theme System, and the Design Token System in that order. Components SHALL NEVER bypass Themes. Components SHALL NEVER bypass Design Tokens.
*Architectural Rationale.* A component that resolved a value directly from a token, skipping the Theme System, would render identically regardless of active theme — silently breaking Light, Dark, High-Contrast, Boardroom, and every white-label theme's ability to differentiate that component, and violating `DS-001-187` (Themes Never Bypass Tokens, Chapter 11) from the opposite direction. A component that resolved its own value independent of Brand Resolution would render identically regardless of active brand, violating `DS-001-211` (Chapter 12) the same way.
*Practical Implications.* A component's specification never references a token value directly; it references the theme-and-brand-resolved output of that token. Where a component appears to require a value no theme currently resolves, the gap is fixed upstream — in the Theme System (Chapter 11) or, if the token itself is missing, the Design Token System (Chapter 10) — never by the component defining a bypass value locally.

**DS-001-230A: Components Shall Never Be Capability Specific**
*Statement.* Components are constitutional visual building blocks. Components SHALL belong to the Design System. Components SHALL NOT belong to any Capability, Business Activity, Module, Workflow, or Product Feature.
*Architectural Rationale.* A Component exists to realize reusable visual meaning (`DS-001-223`). Business Capabilities consume Components; Components do not belong to Capabilities. If Components became capability-specific, the Design System would fragment into multiple competing component libraries, breaking `DS-001-014` (One Visual Language, Chapter 3) at the exact layer this chapter exists to protect. This is the ownership-level counterpart to `DS-001-234` (Capability Teams Shall Not Introduce Component Systems): that principle bars a capability from creating a new component system; this principle bars a capability from claiming ownership of any component, new or existing, within the one system that exists.
*Practical Implications.* A Business Activity may assemble Components. A Capability may consume Components. Neither owns them. Changes a Capability requires SHALL improve the shared Component Standard — through the Design Governance contribution process (Chapter 22 §22.4) — rather than creating a Capability-specific variant. A component named or scoped after a specific capability (for example, a component usable only within one Business Activity) is a defect in the taxonomy (§13.3), not a legitimate specialization.

### 13.5 Enterprise Intelligence Components

**DS-001-231: Enterprise Intelligence and Evidence Components Preserve Meaning, They Never Reinterpret It**
*Statement.* Components rendering Evidence, Confidence, AI, Recommendation, Governance, or Business Activity content — realized through the frozen catalogue's Enterprise Intelligence Components and Evidence Components categories (§13.3) — preserve the meaning Chapter 10's Compositional Token Groupings (§10.3, §10.8) and Chapter 11's theme resolution (`DS-001-198`) establish. Components preserve meaning. Components never reinterpret meaning.
*Architectural Rationale.* This is the component-layer link in the same chain `DS-001-213` (Chapter 12) enforces for brand resolution: each layer downstream of Chapter 10's original meaning — Theme, Brand, and now Component — repeats the identical constraint, because meaning that survives every layer except the last one a user actually sees has still, in practice, failed to survive.
*Practical Implications.* An Evidence Panel, Confidence Indicator, Action Center, Business Activity Card, or Guided Completion Card renders the confidence level, evidence relationship, or governance state it is given exactly as given — never softened, amplified, or reframed for a particular screen's visual convenience. A design request that would require such a component to communicate something other than the meaning it was handed is not a component-design request; it is redirected to constitutional review of the owning chapter.

### 13.6 Accessibility

**DS-001-232: Components Preserve Accessibility, Responsive, Print, High-Contrast, and Keyboard-Navigation Behaviour Without Redefining Meaning**
*Statement.* Every component SHALL preserve accessibility (`SD-001-059`), responsive behaviour (Chapter 16), print behaviour, High-Contrast Theme rendering (`DS-001-193`, Chapter 11), and keyboard navigation (`SD-001-060`) — in every case without redefining the meaning it renders.
*Architectural Rationale.* These five properties are not independent component features to be individually implemented; they are the component-layer expression of accessibility and consistency guarantees Chapters 6 through 11 already establish at the token and theme layers (`DS-001-070`, `DS-001-094`, `DS-001-168`, `DS-001-215`). A component that satisfies them by accident, rather than by correctly consuming its upstream tokens and themes, is not verifiably conformant even if it currently behaves correctly.
*Practical Implications.* A component is not accessible, responsive, print-safe, or high-contrast-safe because it was individually tested to be so — it is accessible because it correctly consumes Accessibility Tokens, Breakpoint Tokens, and Focus Tokens (Chapter 10, §10.3) through a theme that itself satisfies `DS-001-188`. Verification confirms the component consumes these correctly; it does not substitute a component-specific accessibility implementation for that consumption.

### 13.7 Governance

**DS-001-233: New Component Categories Require Constitutional Approval**
A proposed tenth component category, or a change to the Primitive/Composite structure §13.3 establishes, is admitted only through constitutional review of both this chapter and the frozen Document Architecture's Component Catalogue — never through unilateral introduction by a design contributor, capability team, or implementation effort.

**DS-001-234: Capability Teams Shall Not Introduce Component Systems**
Consistent with `DS-001-219` (Chapter 12) and the equivalent principles in Chapters 6 through 11, a capability or Business Activity team has no authority to introduce a new component category or an independent component library. A capability that requires a component this chapter's taxonomy does not yet provide proposes an extension through the Design Governance contribution process (Chapter 22 §22.4).

**DS-001-235: Components Consume Governed Themes**
Every component SHALL consume the Theme System's governed output (Chapter 11) exclusively; no component may render appearance through a mechanism outside it.

**DS-001-236: Components Consume Governed Design Tokens**
Every component SHALL consume the Design Token System's governed output (Chapter 10) exclusively; no component may introduce a value that does not resolve through a governed token.

**DS-001-237: Components Consume Governed Brand Resolution**
Every component SHALL consume Brand Resolution's governed output (Chapter 12) exclusively; no component may render brand-specific appearance through a mechanism outside it.

---

### Chapter 13 Validation

This chapter governs component visual standards as a constitutional concern, not an implementation: no React, Angular, or Vue component, HTML, CSS, Figma component, design library, code-generation mechanism, or rendering implementation appears anywhere above. The taxonomy naming collision between this chapter's brief and the frozen nine-category Component Catalogue is named and resolved explicitly (chapter-opening note, §13.3, `DS-001-229`), with every frozen category preserved and none renamed, merged, or dropped. Components never originate semantic meaning throughout (`DS-001-223`–`224`, `DS-001-231`); components consume Brand Resolution, Themes, and Design Tokens without exception (`DS-001-230`, `DS-001-235`–`237`); Enterprise Intelligence semantics remain unchanged at the component layer (`DS-001-228`, `DS-001-231`). `DS-001-230A` establishes that Components belong to the Design System alone — never to a Capability, Business Activity, Module, Workflow, or Product Feature — closing off capability-scoped component forks as the ownership-level counterpart to `DS-001-234`'s bar on capability-introduced component systems. The constitutional dependency chain — Constitutional Design Principles → Semantic Meaning → Design Token System → Theme System → Brand Resolution → **Component Visual Standards** → Rendered Experience — is stated in prose only (§13.1, §13.4), with no diagram and no implementation guidance, and this chapter's own content occupies exactly the Component Visual Standards link, without redefining Chapters 10 through 12.

*End of Chapter 13.*

---

## SECTION 14: AUREX Domain Visual Language

*A process note before proceeding:* this turn's brief proposed authoring Chapter 14 as "Interaction Patterns & Behavioural Consistency." Chapter 14 is frozen, in this document's Document Architecture, as "AUREX Domain Visual Language," with eleven named subsections (14.1–14.11) already cited by exact section number across Chapters 6, 7, 9, 10, 11, 12, and 13. Given the scale of that dependency, this conflict was raised for explicit resolution before drafting rather than reconciled by naming alone; the confirmed direction is to author Chapter 14 exactly as frozen and hold the Interaction Patterns brief for a future, separately numbered chapter.

This chapter defines the complete constitutional visual standard for AUREX's eleven Enterprise Intelligence domain concepts — Evidence, Confidence, Explainability, AI-Generated Content, Recommendations, Knowledge Graphs, Enterprise Relationships, Business Activities, Decision Support, Risk Indicators, and Trust Indicators. It defines no new colour, icon, typography, illustration, token, or component. It does not define token values, CSS, JSON, or any implementation technology. Every visual standard below is an assembly of families, groupings, and categories Chapters 6 through 13 already establish, applied to the specific domain concept each subsection governs.

**DS-001-238: Chapter 14 Integrates, It Does Not Originate**
*Statement.* This chapter defines no new colour family, icon family, typography reading layer, illustration family, token grouping, or component category. Every visual standard in this chapter is an assembly of elements Chapters 6 through 13 already establish, applied specifically to the eleven Enterprise Intelligence domain concepts SD-001 identifies as requiring dedicated visual treatment.
*Architectural Rationale.* This is the domain-concept-level expression of the same no-origination discipline running through every chapter since Chapter 10 (`DS-001-159`, `DS-001-165`, `DS-001-224`): a chapter positioned this late in the dependency chain has no remaining authority to introduce meaning Chapters 4 through 9 have not already established. Chapter 14's value is integrative — assembling what is already governed into one coherent, complete standard per domain concept — not originative.
*Practical Implications.* Each subsection below names the specific colour, icon, typography, illustration, token, and component elements that compose its domain concept's complete visual standard, and states the completeness test that standard must pass. A rendering of Evidence, Confidence, or any other concept below that omits one of its named elements, or substitutes an element this chapter does not name, is non-conformant regardless of how visually coherent it appears in isolation.

### 14.1 Evidence Visual Standards

Evidence renders SD-001's requirement that evidence be one click away from any value it supports (`SD-001-015`) and that presentation remain evidence-first (`SD-001` §1.6). Its complete visual standard is composed of: Evidence Colours (Chapter 6, §6.3); Evidence Icons (Chapter 8, §8.3); the Evidence Reading layer and Evidence Narratives (Chapter 7, §7.3, §7.7); Evidence Illustrations (Chapter 9, §9.3); Evidence Tokens (Chapter 10, §10.3); and the Evidence Components category — Evidence Panel, Source Citation, Audit Trail Viewer, Conflict/Discrepancy Indicator (Chapter 13, §13.3).

**DS-001-239: Evidence Is Complete Only When All Six Elements Render Together**
A rendering of evidence-backed content is constitutionally complete only when it draws on all six elements named above. A conclusion coloured with Evidence Colours but carrying no Source Citation component, or a Source Citation with no Evidence Reading-layer typographic treatment, is an incomplete realization of this standard, not a valid partial one.

### 14.2 Confidence Visual Standards

Confidence renders SD-001's requirement that confidence be always visible and its computation disclosed (`SD-001-010`, `SD-001-011`). Its complete visual standard is composed of: Confidence Colours (Chapter 6, §6.3); Confidence Icons (Chapter 8, §8.3); Confidence Explanations within AI Explanation Reading (Chapter 7, §7.7); Confidence Tokens (Chapter 10, §10.3); and the Confidence Indicator component (Chapter 13, Evidence Components category).

**DS-001-240: Confidence Is Never Rendered Through Colour Alone**
Consistent with `DS-001-069` (Colour Alone Never Carries Meaning, Chapter 6), a Confidence Indicator's colour is always accompanied by its Confidence Icon and, where the underlying formula is queried, its Confidence Explanation typography. A confidence value expressed through colour with no accompanying icon or disclosed-formula access point is incomplete.

### 14.3 Explainability Visual Standards

Explainability renders SD-001's no-black-box mandate (`SD-001-012`): every AI-generated conclusion must expose its reasoning, evidence used, and what was inferred versus found directly. Explainability has no dedicated colour, icon, or token family of its own — it is realized entirely through the combination of Evidence and AI families: Evidence Colours and Evidence Tokens (for what was found), AI Colours and AI Tokens (for what was inferred), AI Explanation Reading and AI Reasoning Chains typography (Chapter 7, §7.3, §7.7), AI Explainability Illustrations (Chapter 9, §9.3), and the Explainability Panel component (Chapter 13, Evidence Components category).

**DS-001-241: Explainability Is a Composed Standard, Not an Eleventh Family**
Explainability's visual standard is the coordinated combination of Evidence and AI elements named above, not an independent family requiring its own colour or token. A design proposal for a dedicated "Explainability Colour" is redirected to this composition rather than accepted as a new atomic or compositional family.

### 14.4 AI-Generated Content Visual Standards

AI-Generated Content renders SD-001's requirement that AI remain an embedded, transparent capability (`SD-001` §2.6) and that its conclusions distinguish inference from direct discovery (`SD-001-012`). Its complete visual standard is composed of: AI Colours (Chapter 6, §6.3), architected to support five distinct provenance states — AI-generated, AI-assisted, AI-inferred, AI-validated, and human-verified AI output; AI Icons (Chapter 8, §8.3), mirroring the same five-state spectrum; AI Explanation Reading (Chapter 7, §7.3); AI Tokens (Chapter 10, §10.3, an atomic family); and the DNA-Adaptive Rendering Surface and Guided Completion Card components (Chapter 13, Enterprise Intelligence Components category).

**DS-001-242: Each of the Five AI Provenance States Is Visually Distinct From Every Other State, Not Only From Human Content**
*Statement.* AI-generated, AI-assisted, AI-inferred, AI-validated, and human-verified AI output SHALL each be visually distinguishable from every one of the other four states, not only from human-entered or system-verified content generally.
*Architectural Rationale.* Chapters 6 and 8 established that AI Colours and AI Icons must support this five-state spectrum, but neither chapter completed the requirement that the five states be mutually distinguishable — a gap this principle closes, consistent with SD-001's requirement that AI-generated conclusions distinguish what was inferred from what was found directly (`SD-001-012`), which presumes the distinctions themselves are perceivable.
*Practical Implications.* A design that renders AI-inferred and AI-validated content identically, on the theory that both are "AI-related," fails this principle. Each state's Colour and Icon pairing is verified pairwise against the other four, not only against the human/AI boundary.

### 14.5 Recommendation Visual Standards

Recommendations render SD-001's constitutional distinction that a recommendation is never presented as a decision (`SD-001-013`). Its complete visual standard is composed of: Decision Support Colours (Chapter 6, §6.3); Action Icons (Chapter 8, §8.3); Recommendation Narratives within Analytical and Executive Reading (Chapter 7, §7.3, §7.7); Recommendation Tokens (Chapter 10, §10.8); and the Action Center component (Chapter 13, Enterprise Intelligence Components category).

**DS-001-243: A Recommendation Is Never Rendered Indistinguishably From a Confirmed Fact**
A recommendation's complete visual standard exists specifically to prevent the rendering failure `SD-001-013` warns against: Decision Support Colours and their accompanying Action Icon are mandatory precisely so that a recommendation cannot be visually confused with data the platform has confirmed rather than merely suggested.

### 14.6 Knowledge Graph Visual Standards

Knowledge Graph visualization renders structural content whose canonical data model belongs to SD-002-013 and ERG-001 (Chapter 2, Ownership Matrix) — this chapter governs only its rendering. Its complete visual standard is composed of: Data Visualisation Colours (Chapter 6, §6.3), calibrated for node and edge perceptual distinction; Chart Tokens (Chapter 10, §10.3); and the Knowledge Graph Renderer component (Chapter 13, Data Presentation / Visualization Components category).

**DS-001-244: Knowledge Graph Rendering Never Asserts Structural Authority It Does Not Have**
The Knowledge Graph Renderer visualizes whatever relationship data SD-002-013 or ERG-001 supplies; it never resolves, infers, or displays a relationship those systems have not already established. This is the visual-layer expression of the boundary Chapter 2's Ownership Matrix draws between DS-001 (styling) and SD-002/ERG-001 (structure).

### 14.7 Enterprise Relationship Visual Standards

Enterprise Relationship visualization — organizational, hierarchical, and structural relationship diagrams distinct from the general-purpose Knowledge Graph Renderer's arbitrary relationship rendering — renders the Enterprise Relationship Graph ERG-001 defines structurally (Chapter 2, Ownership Matrix). Its complete visual standard is composed of: the Enterprise Intelligence Illustrations family, specifically enterprise relationship diagrams (Chapter 9, §9.3, §9.7); Data Visualisation Colours (Chapter 6, §6.3); and the Knowledge Graph Renderer component shared with §14.6 where a relationship is graph-structured, or a dedicated diagram illustration where it is not.

**DS-001-245: Enterprise Relationship Visualization Distinguishes Organizational Structure From Arbitrary Relationship Data**
Where §14.6 governs the rendering of arbitrary enterprise relationship data, this section governs specifically organizational and hierarchical structure. A single visual treatment is not required to serve both; a design may use a diagram-based illustration for organizational structure and a graph renderer for arbitrary relationships, provided each conforms to its own named standard.

### 14.8 Business Activity Visual Standards

Business Activities render SD-001's requirement that named activities replace questionnaires (`SD-001-009`) and SD-002's governance of Business Activity as a business object (SD-002 §5). Its complete visual standard is composed of: Business Activity Icons (Chapter 8, §8.3); Process, Workflow, and Learning & Guidance Illustrations (Chapter 9, §9.3); Business Activity Tokens (Chapter 10, §10.8); and the Business Activity Card component (Chapter 13, Enterprise Intelligence Components category).

**DS-001-246: A Business Activity Is Recognizable by Symbol Before Its Name Is Read**
Consistent with `DS-001-103` (Recognition Before Memorization, Chapter 8), a Business Activity Card's icon and illustrative treatment are sufficient, together, for a returning user to recognize the activity before reading its title — the visual standard exists to make this recognition possible, not merely decorative.

### 14.9 Decision Support Visual Standards

Decision Support renders the Sacred 12's structural and tonal requirements (SD-001 §8) — specifically that every insight state its business consequence (`SD-001-057`) within the calm, low-motion executive tone `SD-001-056` and `DS-001-016` establish. Its complete visual standard is composed of: Decision Support Colours (Chapter 6, §6.3, shared with §14.5); the Executive Reading layer (Chapter 7, §7.3); the Executive Components category — Executive Header, Strategic Narrative Card, Executive Summary Tile, Boardroom Display Card, Consequence Statement (Chapter 13, §13.3); and Boardroom Theme (Chapter 11, §11.3) as the primary resolution context.

**DS-001-247: Decision Support Content Never Renders Outside Boardroom Theme's Calm Constraint**
A Decision Support surface rendered in any theme — not Boardroom Theme alone — still satisfies `DS-001-016` (Calm by Default, Loud by Exception): Decision Support is a content category with a constitutionally calm visual register, not a register that only applies when Boardroom Theme happens to be active.

### 14.10 Risk Indicator Visual Standards

Risk Indicators render risk category and severity along an axis distinct from Semantic Status Colours' favorable/unfavorable axis (Chapter 6, §6.3, Decision Support Colours). Its complete visual standard is composed of: Decision Support Colours; Risk Icons (Chapter 8, §8.3); and the Risk Matrix component (Chapter 13, Data Presentation / Visualization Components category).

**DS-001-248: Risk Severity Is Rendered Along Its Own Axis, Never Collapsed Into Favorable/Unfavorable**
A Risk Indicator's severity — low, moderate, high, critical — is visually distinct from a Semantic Status Colour's favorable/unfavorable signal (`DS-001-064`, One Family Per Concept, Chapter 6). A design that renders risk severity using Semantic Status Colours directly, rather than Decision Support Colours and Risk Icons, conflates two constitutionally distinct concepts.

### 14.11 Trust Indicator Visual Standards

Trust Indicators render SD-001's overarching evidence-first, explainable philosophy (`SD-001` §1.6) and this document's own founding principle that visual trust builds enterprise trust (`DS-001-024`, Chapter 3). Trust is not an independent twelfth family — it is the aggregate, perceivable effect of Evidence (§14.1), Confidence (§14.2), Explainability (§14.3), and AI-Generated Content (§14.4) visual standards functioning correctly together, reinforced by Governance Tokens and Governance Icons (Chapter 10, §10.8; Chapter 8, §8.3) where audit and approval state contribute to trust.

**DS-001-249: Trust Is the Composite Outcome of the Preceding Ten Standards, Not an Eleventh Standard**
*Statement.* No dedicated "Trust Colour," "Trust Icon," or "Trust Token" exists or is needed. A screen is trustworthy in appearance exactly to the degree that its Evidence, Confidence, Explainability, AI-Generated Content, Recommendation, Knowledge Graph, Enterprise Relationship, Business Activity, Decision Support, and Risk Indicator visual standards (§14.1–14.10) are each independently satisfied.
*Architectural Rationale.* This closes the chapter on the same note `DS-001-238` opens it: Chapter 14 integrates, it does not originate. Trust is the clearest possible case of that principle — it would be architecturally incoherent for this chapter to define a twelfth, independent "Trust" standard when trust is definitionally the reader's perception of whether the preceding ten are each functioning as designed.
*Practical Implications.* A reported "trust problem" with a screen is diagnosed by checking which of §14.1 through §14.10's standards is incompletely rendered, never treated as a standalone Trust Indicator defect to be fixed independently of those ten.

**DS-001-249A: Domain Visual Language Shall Remain Stable Across Capabilities**
*Statement.* The Domain Visual Language defined in this chapter belongs to the Enterprise Design System. It SHALL remain identical across every Capability, Workspace, Business Activity, Industry Pack, Tenant, and Product Module. Evidence SHALL always look like Evidence. Confidence SHALL always look like Confidence. AI SHALL always look like AI. Risk SHALL always look like Risk. Trust SHALL always emerge from the same governed visual standards.
*Architectural Rationale.* Enterprise Intelligence depends upon immediate visual recognition. Users SHALL NOT relearn visual meaning when moving between Capabilities or Industry Packs. The Domain Visual Language is therefore a constitutional enterprise language rather than a capability-specific language — the same status `DS-001-014` (One Visual Language, Chapter 3) and `DS-001-230A` (Components Shall Never Be Capability Specific, Chapter 13) already establish for the platform's visual language and its components generally, extended here explicitly to the eleven domain concepts this chapter governs, including their stability across Industry Packs specifically.
*Practical Implications.* Capability teams MAY compose §14.1–14.11's standards. They SHALL NOT redefine them. Industry Packs MAY extend business semantics — new capabilities, terminology, or domain objects — consistent with how Industry Packs extend the canonical vocabulary without replacing it; they SHALL NOT redefine Domain Visual Language. White-label implementations MAY change appearance through governed Brand Resolution (Chapter 12) and Theme resolution (Chapter 11); they SHALL NOT redefine Domain Visual Language. A capability, Industry Pack, or white-label deployment proposing a different visual treatment for Evidence, Confidence, AI, Risk, or any other concept in this chapter is proposing a change to this chapter, subject to the same constitutional review as any other change to it — never a local variation adopted unilaterally.

---

### Chapter 14 Validation

This chapter completes, without redefining, the visual standards eight prior chapters (6, 7, 8, 9, 10, 11, 12, 13) have been citing forward to "Chapter 14" throughout — every cross-reference made in those chapters to a §14.x section is now satisfied by the corresponding subsection above. No new colour, icon, typography, illustration, token, or component is introduced anywhere in this chapter (`DS-001-238`); every subsection instead names the specific prior-chapter elements that compose its domain concept's complete standard. Explainability (§14.3) and Trust (§14.11) are explicitly identified as composed standards rather than independent families, closing two potential ambiguities left open by earlier chapters' forward references. The five-state AI provenance spectrum, referenced without full elaboration since Chapter 6, is completed here (`DS-001-242`) with the pairwise-distinguishability requirement it was always missing. `DS-001-249A` extends this chapter's stability guarantee explicitly across Capabilities, Workspaces, Business Activities, Industry Packs, Tenants, and Product Modules — none may compose without redefining, and white-label implementations remain confined to Chapter 11/12's governed Brand and Theme resolution. No token value, CSS, JSON, or implementation technology appears anywhere above. The conflict between this turn's original "Interaction Patterns" brief and the frozen Chapter 14 scope was surfaced and resolved before any content was drafted, per the process note at the top of this chapter.

*End of Chapter 14.*

---

## SECTION 15: Motion Language & Animation Standards

*A verification note before proceeding:* this chapter's title and scope were verified against the frozen Document Architecture before drafting, per explicit instruction. The frozen scaffold reserves no subsections for Chapter 15 and states its scope only through the Ownership Matrix: "Motion Language, Animation Standards | DS-001 (spec) / SD-001 (when) | `SD-001-056` mandates lower motion for Sacred 12 as a behavioral rule. DS-001 owns the easing/duration tokens and choreography." Two earlier chapters cite Chapter 15 by number — Chapter 2 §2.4 (the Ownership Matrix row above) and Chapter 4 §4.3 ("A motion treatment (Chapter 15) that reads as flashy rather than purposeful fails this personality"). No competing brief was supplied for this chapter; its subsection structure below follows the pattern established by Chapters 6 through 13.

This chapter defines the constitutional architecture of Motion and Animation within AUREX — the specification and choreography of movement, building on `DS-001-020` (Motion Must Communicate, Never Decorate, Chapter 3). It defines architectural intent only. It does not define duration values, easing-curve mathematics, CSS transitions, animation libraries, or any rendering technology; those belong to the Motion, Animation, and Transition Tokens (Chapter 10) and implementation repositories.

### 15.1 Purpose

SD-001 establishes when motion must be reduced — Sacred 12 surfaces render calmer and lower-motion than operational surfaces (`SD-001-056`) — and that in-progress operations remain visibly transparent (`SD-001-026`). This chapter establishes what AUREX's motion actually is: the specification and choreography that satisfies those behavioral requirements. Motion in AUREX exists to help a user understand a state change, a relationship, or a system response; `DS-001-020` already forecloses motion that decorates rather than communicates. This chapter's purpose is to give that foreclosure a complete constitutional architecture — categories, semantic principles, and governance — rather than leaving it a single, unelaborated principle.

### 15.2 Motion Philosophy

**DS-001-250: Motion Is Governed Choreography, Not Ornament**
Every motion in AUREX is a deliberate, governed choice, traceable to the state change or system response it communicates. This extends `DS-001-020` from a prohibition (motion shall not decorate) into a positive discipline (motion is choreographed, not improvised).

**DS-001-251: Motion Duration Reflects Semantic Weight**
A brief motion communicates a minor, low-consequence change; a longer motion communicates something more structurally significant. Duration is itself meaningful, consistent with `DS-001-022` (Every Visual Element Has Purpose, Chapter 3) applied to time.

**DS-001-252: Motion Direction Reflects Spatial and Causal Relationship**
Where motion has a direction — an element entering, exiting, or transforming — that direction communicates where content came from or where it is going, never an arbitrary stylistic choice.

**DS-001-253: Motion Defaults to Restraint**
Consistent with `DS-001-016` (Calm by Default, Loud by Exception, Chapter 3), motion intensity and frequency default to the minimum sufficient to communicate the change occurring; visual energy is never motion's own justification.

**DS-001-254: Motion Never Substitutes for a Stated System Status**
Motion may accompany a stated status (a percentage, an estimated completion time, per `SD-001-026`) but never replaces it. A spinner or pulsing animation with no accompanying stated progress is an incomplete implementation of SD-001's performance-transparency mandate, not a valid alternative to it.

### 15.3 Motion & Animation Architecture

AUREX defines eight constitutional motion categories. Each has a distinct communicative purpose; none substitutes for another.

| Motion Category | Purpose |
|---|---|
| Micro-Interaction Motion | Immediate feedback on hover, focus, and press — confirming an interactive element has registered a user's input. |
| State-Transition Motion | Communicates a component moving between states — expand/collapse, show/hide — consistent with State and Transition Tokens (Chapter 10, §10.3). |
| Navigation Motion | Communicates movement between screens or views, reinforcing the spatial and hierarchical relationship SD-001's navigation architecture establishes (`SD-001-018`). |
| Progress & Loading Motion | Accompanies a stated in-progress operation (`SD-001-026`); realized in full by Chapter 20 (Loading Experience). |
| Notification Motion | Accompanies the appearance and dismissal of a notification or toast; realized in full by Chapter 21 (Notification Styling). |
| Data-Update Motion | Communicates that a specific, already-visible value has changed, consistent with SD-001's incremental-refresh principle (`SD-001-081`) — the screen updates the values that changed, not a full re-render. |
| AI-Reasoning Motion | Communicates that AI inference or discovery is actively in progress, distinct from generic Progress & Loading Motion — realized in full by Chapter 14, §14.4 (AI-Generated Content Visual Standards). |
| Executive/Boardroom Motion | The deliberately reduced-intensity expression of every other category, resolved specifically by Boardroom Theme (§15.6). |

**DS-001-255: The Motion Taxonomy Is a Closed, Named Set of Eight Categories**
No motion exists outside the eight categories above. A future need that appears to require a new motion category is resolved by proposing an extension to this closed set through constitutional review (§15.9), never by an ad hoc animation invented outside it. This is `DS-001-027` (Extend, Never Fork) applied to Motion.

### 15.4 Semantic Principles

**DS-001-256: One Motion Meaning, Everywhere**
A given motion category communicates the same thing on every screen, in every capability, for every tenant. This is `DS-001-063` (One Meaning, Everywhere, Chapter 6) applied to motion.

**DS-001-257: Motion Never Changes Business Meaning**
Applying, removing, or changing a motion treatment never changes what a value means, what decision it should inform, or what data it represents. This is `DS-001-066` (Colour Never Changes Business Meaning, Chapter 6) applied to motion.

**DS-001-258: Motion Remains Stable Across Themes**
A theme (Chapter 11) may change a motion's specific duration or easing resolution; it never changes which motion category applies or what that category communicates. This is `DS-001-025` (Themes Change Appearance, Never Meaning, Chapter 3) applied to motion.

### 15.5 Relationship with Design Tokens

**DS-001-259: Motion Is Resolved Only Through Motion, Animation, and Transition Tokens**
Implementations SHALL consume motion exclusively through the Motion Tokens, Animation Tokens, and Transition Tokens Chapter 10 defines (§10.3). No implementation, capability, or extension shall hard-code a duration, easing curve, or animation sequence outside that system. This is `DS-001-015` (One Token, Every Surface, Chapter 3) applied specifically to motion, mirroring `DS-001-068` (colour), `DS-001-092` (typography), `DS-001-115` (iconography), and `DS-001-139` (illustration).

**DS-001-259A: Motion Shall Preserve Temporal Consistency Across the Platform**
*Statement.* A given Motion Category SHALL exhibit a consistent temporal character across every Capability, Workspace, Business Activity, Industry Pack, Tenant, and Product Module. Users SHALL learn one Motion Language for the entire platform. Motion SHALL reinforce familiarity rather than novelty.
*Architectural Rationale.* Motion forms part of the Enterprise Visual Language. Just as Colour (Chapter 6), Typography (Chapter 7), Icons (Chapter 8), Illustrations (Chapter 9), Components (Chapter 13), and the Domain Visual Language (Chapter 14, `DS-001-249A`) remain stable across Capabilities, Industry Packs, and Tenants, Motion SHALL remain equally stable. Consistency reduces cognitive load and improves user confidence, extending `DS-001-256` (One Motion Meaning, Everywhere) from a single-instant guarantee into a standing platform-wide one.
*Practical Implications.* Capability teams MAY consume Motion Categories (§15.3). They SHALL NOT redefine their temporal behaviour. Industry Packs MAY compose Motion Categories. They SHALL NOT create capability-specific motion styles. White-label implementations MAY resolve Motion Tokens through the governed Theme System (Chapter 11); they SHALL NOT redefine Motion semantics. A capability, Industry Pack, or white-label deployment proposing a different temporal character for an existing Motion Category is proposing a change to this chapter, subject to the same constitutional review as any other change to it — never a local variation adopted unilaterally.

### 15.6 Motion and Theme

**DS-001-260: Boardroom Theme Resolves Every Motion Category to Its Lowest Registered Intensity**
Boardroom Theme (Chapter 11, §11.3) resolves each of the eight motion categories above to its lowest defined intensity, in direct service of SD-001's Boardroom Display Modes requirement (`SD-001-074`) and calm executive tone mandate (`SD-001-056`). This is the motion-specific realization of `DS-001-247` (Chapter 14): Decision Support and executive content carry a constitutionally calm visual register regardless of which theme happens to be active, and Boardroom Theme is where that register is most fully expressed for motion specifically.

### 15.7 Accessibility

**DS-001-261: Reduced-Motion Mode Disables Non-Essential Motion Without Removing Communicated Meaning**
The reduced-motion accessibility mode SD-001 requires to exist (`SD-001-063`) suppresses or minimizes every motion category's animated expression while preserving the state change, relationship, or system response that motion communicated — through an instant transition or a static equivalent, never through silently dropping the information. This is `DS-001-194` (Every Theme Supports the Accessibility Modes SD-001 Requires, Chapter 11) applied specifically to motion.

### 15.8 Enterprise Intelligence Motion

**DS-001-262: AI-Reasoning-in-Progress Motion Is Distinct From Generic Loading Motion**
AI-Reasoning Motion (§15.3) is visually distinct from generic Progress & Loading Motion, so that a user can tell, from motion alone as one signal among others, whether the platform is performing routine data retrieval or active AI inference — consistent with the AI provenance distinctions Chapter 14 §14.4 establishes and `DS-001-242`'s pairwise-distinguishability requirement. The specific motion treatment is a Chapter 14 / implementation-repository concern; this principle establishes only that the two categories must remain distinguishable.

### 15.9 Governance

**DS-001-263: Motion Evolution Is Rare and Constitutionally Reviewed**
The Motion Taxonomy defined in §15.3 changes rarely, and only through the same constitutional review discipline as any other change to this document.

**DS-001-264: New Motion Categories Require Constitutional Review**
A proposed ninth motion category is admitted only through constitutional review — never through unilateral introduction by a design contributor, capability team, or implementation effort.

**DS-001-265: Capability Teams Shall Not Introduce Motion Systems**
Consistent with the equivalent principles in Chapters 6 through 13, a capability or Business Activity team has no authority to introduce a new motion category or an independent animation system. A capability that requires motion support this chapter does not yet provide proposes an extension through the Design Governance contribution process (Chapter 22 §22.4).

**DS-001-266: White-Label Branding Shall Not Redefine Motion Semantics**
A tenant's or partner's white-label configuration (Chapter 12) may vary motion's specific duration or easing resolution within the token system Chapter 10 defines; it shall never redefine which motion category applies or what that category communicates. This is `DS-001-076` (White-Label Colour Remains Governed, Chapter 6) applied to motion.

**DS-001-267: Marketing Motion Shall Never Affect Product Motion**
A marketing or campaign use of motion, however it is applied outside the product surface, shall never cause a product motion category's meaning to be reinterpreted. This is `DS-001-037` (Marketing Campaigns Shall Not Redefine the Constitutional Brand, Chapter 4) applied specifically to motion.

---

### Chapter 15 Validation

This chapter defines motion as governed choreography, not implementation: no duration value, easing-curve mathematics, CSS transition, animation library, or rendering technology appears anywhere above, including within `DS-001-259A`, which states its cross-platform stability requirement in prose only. Every reference to how motion is actually resolved is deferred explicitly to Chapter 10 (Motion, Animation, and Transition Tokens) and Chapter 11 (Theme Architecture), consistent with the deferral pattern every prior visual-language chapter established. No content restates `DS-001-020` (Chapter 3) or `SD-001-026`/`SD-001-056`; each is cited and extended into a complete architecture instead. AI-Reasoning Motion (§15.8) and Executive/Boardroom Motion (§15.6) are explicitly cross-referenced to, not redefined from, Chapter 14 and Chapter 11 respectively. Motion remains part of the Enterprise Visual Language throughout (`DS-001-259A`), identical across every Capability, Industry Pack, and Tenant, and continues to consume only Design Tokens and Themes — never an independent resolution path. The chapter's scope was verified against the frozen Document Architecture before drafting, per the process note at the top of this chapter, and no subsection or title deviates from that verification.

*End of Chapter 15.*

---

## SECTION 16: Responsive Visual Behaviour

*A verification note before proceeding:* this chapter's title and scope were verified against the frozen Document Architecture before drafting. The frozen scaffold reserves no subsections for Chapter 16 and states its scope only through the Ownership Matrix: "Responsive Visual Behaviour | DS-001 (visual) / SD-001 (structural) | SD-001 §11 owns what must never be hidden at small viewports (`SD-001-071`). DS-001 owns the breakpoint/spacing token behavior." Six earlier chapters cite Chapter 16 by number (§2.4, §3.4, `DS-001-094`, `DS-001-169`, `DS-001-196`, `DS-001-232`). No competing brief was supplied; this chapter's structure follows the pattern established by Chapters 6 through 15, and its taxonomy (§16.3) is framed around how visual tokens respond across viewports rather than which device class is active — the latter remaining SD-001-076's structural concern.

This chapter defines the constitutional architecture of Responsive Visual Behaviour within AUREX — how the visual system adapts across viewport sizes while preserving every meaning Chapters 4 through 15 establish. It defines architectural intent only. It does not define breakpoint pixel values, CSS media queries, responsive frameworks, or any rendering technology; those belong to the Breakpoint Tokens (Chapter 10) and implementation repositories.

### 16.1 Purpose

SD-001 requires that responsive widget density adapt to viewport without ever hiding the confidence, evidence, or ownership data Sections 4 and 9 require (`SD-001-071`), and that the platform detect device class and adapt its layout template automatically (`SD-001-076`). This chapter establishes the visual mechanism that satisfies the first requirement: how spacing, sizing, layout, and typography actually change across viewports so that adaptation never becomes omission. Responsiveness in AUREX is density changing in service of the same meaning, never meaning changing in service of density.

### 16.2 Responsive Philosophy

**DS-001-268: Density Adapts, Meaning Does Not**
A screen's visual density — spacing, sizing, information per view — changes across viewports. What that screen means, and what it requires a user to know, does not. This is the responsive-specific restatement of `DS-001-025` (Themes Change Appearance, Never Meaning, Chapter 3), applied to viewport rather than theme.

**DS-001-269: Responsive Behaviour Is Progressive Disclosure Applied to Viewport**
A constrained viewport is not a reason to hide content; it is a reason to apply `DS-001-023` (Progressive Visual Disclosure, Chapter 3) more aggressively at the summary level, exposing detail on the same click path a larger viewport exposes it, never removing that path.

**DS-001-270: Every Viewport Is a First-Class Rendering Context**
No viewport size is treated as a reduced or secondary version of another. This is `DS-001-026` (Design Must Scale Across Enterprises, Chapter 3) extended from enterprise context to device context, and the visual-layer expression of SD-001's mandate that mobile be a first-class platform, not a reduced view (`SD-001-070`).

**DS-001-271: Responsive Behaviour Defaults to Restraint**
Consistent with `DS-001-016` (Calm by Default, Loud by Exception, Chapter 3), density increases at larger viewports are additive refinement, never a baseline a smaller viewport is failing to meet.

### 16.3 Responsive Architecture

AUREX defines five constitutional responsive behaviour categories — each describing how visual tokens and components respond across viewports, not which device class is active (a determination SD-001-076 governs structurally).

| Responsive Behaviour Category | Purpose |
|---|---|
| Density Adaptation | Governs how Spacing, Sizing, and Grid Tokens (Chapter 10, §10.3) resolve differently across the Breakpoint Token spectrum. |
| Layout Reflow | Governs how Layout Components (Chapter 13, §13.3) rearrange their constituent Primitive Components across viewports without altering content. |
| Content Prioritization | Governs which content renders first and which becomes progressively disclosed at constrained viewports, per `DS-001-269` — never which content is omitted entirely. |
| Touch Target Adaptation | Governs how Sizing and Spacing Tokens adjust to satisfy touch-interaction requirements at compact viewports, without changing what a control means or does. |
| Boardroom / Large-Format Adaptation | Governs the large-format, low-interaction rendering Boardroom Theme (Chapter 11, §11.3) resolves, sharing the same underlying Breakpoint Token spectrum as compact-viewport adaptation, at the opposite end of it. |

**DS-001-272: The Responsive Behaviour Taxonomy Is a Closed, Named Set of Five Categories**
No responsive behaviour exists outside the five categories above. A future need that appears to require a new category is resolved by proposing an extension to this closed set through constitutional review (§16.9), never by an ad hoc adaptation invented outside it. This is `DS-001-027` (Extend, Never Fork) applied to Responsive Visual Behaviour.

### 16.4 Semantic Principles

**DS-001-273: One Meaning Across Every Viewport**
A given colour, icon, typographic hierarchy level, or component meaning is identical at every viewport. This is `DS-001-063` (One Meaning, Everywhere, Chapter 6) applied to viewport.

**DS-001-274: Responsive Behaviour Never Hides Evidence, Confidence, or Ownership Data**
This chapter's every category (§16.3) is constrained by SD-001's explicit mandate that confidence, evidence, and ownership data survive responsive adaptation without exception (`SD-001-071`). A design that achieves density adaptation by omitting an Evidence Component, Confidence Indicator, or ownership attribution at a compact viewport does not satisfy Density Adaptation or Content Prioritization — it violates them.

**DS-001-275: Responsive Behaviour Never Changes Business Meaning**
Applying, removing, or changing a viewport's density treatment never changes what a value means, what decision it should inform, or what data it represents. This is `DS-001-066` (Colour Never Changes Business Meaning, Chapter 6) applied to viewport.

### 16.5 Relationship with Design Tokens

**DS-001-276: Responsive Behaviour Is Resolved Only Through Breakpoint, Sizing, Spacing, and Grid Tokens**
Implementations SHALL consume responsive behaviour exclusively through the Breakpoint, Sizing, Spacing, and Grid Tokens Chapter 10 defines (§10.3), composed through the Layout Tokens grouping (§10.3). No implementation, capability, or extension shall hard-code a viewport-specific value outside that system. This is `DS-001-015` (One Token, Every Surface, Chapter 3) applied specifically to responsive behaviour, mirroring the equivalent principles in Chapters 6 through 9 and 15.

### 16.6 Relationship with the Theme System

**DS-001-277: Themes Preserve Meaning Identically Across Every Breakpoint**
This restates `DS-001-196` (Themes Preserve Meaning Under Responsive Rendering, Chapter 11) as this chapter's own governing rule: a theme's resolution across viewport sizes preserves meaning identically at every breakpoint, with only density and layout varying. Chapter 16 and Chapter 11 govern the same guarantee from opposite directions — this chapter from the responsive-behaviour side, Chapter 11 from the theme-resolution side — and neither restates the other's full content.

### 16.7 Accessibility

**DS-001-278: Responsive Behaviour Remains Legible Under Zoom**
This restates `DS-001-094` (Typography Remains Legible Under Zoom and Responsive Reflow, Chapter 7) as this chapter's own governing rule: responsive adaptation and zoom are independent, orthogonal accessibility dimensions, and a layout that reflows correctly across breakpoints but breaks under zoom is non-conformant.

**DS-001-279: Touch Target Adaptation Satisfies Accessibility Minimums Without Redefining Meaning**
Touch Target Adaptation (§16.3) resolves Sizing and Spacing Tokens to satisfy the accessibility minimums SD-001 establishes as non-optional (`SD-001-059`) at compact viewports; it never changes what the enlarged control does or means relative to its pointer-driven equivalent at larger viewports.

### 16.8 Enterprise Intelligence Responsive Behaviour

**DS-001-280: Enterprise Intelligence Components Never Degrade Below Their Chapter 14 Standard at Any Viewport**
The Evidence, Confidence, Explainability, AI-Generated Content, Recommendation, Knowledge Graph, Enterprise Relationship, Business Activity, Decision Support, Risk Indicator, and Trust Indicator visual standards Chapter 14 establishes (§14.1–14.11) apply identically at every viewport this chapter's taxonomy governs. Density Adaptation may change how an Evidence Panel or Confidence Indicator is laid out at a compact viewport; it never renders that component with fewer of Chapter 14's required elements than its full-viewport equivalent.

**DS-001-280A: Responsive Behaviour Shall Preserve Cognitive Continuity**
*Statement.* Responsive Behaviour SHALL preserve the user's mental model when moving between viewport sizes. A user transitioning between compact, standard, large, or boardroom viewports SHALL recognize the same information, relationships, visual hierarchy, Domain Visual Language, and Enterprise Intelligence semantics, even though presentation density, layout, or spacing may change.
*Architectural Rationale.* Responsive Behaviour exists to optimize presentation, not to create different experiences. Users SHALL NOT relearn the platform simply because the viewport changes. Cognitive continuity is therefore a constitutional requirement of Responsive Visual Behaviour, not an incidental benefit of it — the experiential synthesis of `DS-001-268` (Density Adapts, Meaning Does Not), `DS-001-273` (One Meaning Across Every Viewport), and `DS-001-280` (Enterprise Intelligence Components Never Degrade), stated here as what a user actually perceives when those three principles are jointly satisfied.
*Practical Implications.* Layouts MAY reflow. Components MAY resize. Information MAY be progressively disclosed (`DS-001-269`). Semantic meaning, visual hierarchy, and Enterprise Intelligence concepts SHALL remain unchanged. A responsive redesign that satisfies every individual token and component rule in this chapter but still leaves a returning user disoriented by the transition has failed this principle, and is grounds for review even where no other principle in this chapter was technically violated.

### 16.9 Governance

**DS-001-281: Responsive Behaviour Evolves Rarely and Constitutionally**
The Responsive Behaviour Taxonomy defined in §16.3 changes rarely, and only through the same constitutional review discipline as any other change to this document.

**DS-001-282: New Responsive Categories Require Constitutional Review**
A proposed sixth responsive behaviour category is admitted only through constitutional review — never through unilateral introduction by a design contributor, capability team, or implementation effort.

**DS-001-283: Capability Teams Shall Not Introduce Responsive Systems**
Consistent with the equivalent principles in Chapters 6 through 15, a capability or Business Activity team has no authority to introduce a new responsive behaviour category or an independent responsive framework. A capability that requires responsive support this chapter does not yet provide proposes an extension through the Design Governance contribution process (Chapter 22 §22.4).

**DS-001-284: White-Label Branding Shall Not Redefine Responsive Semantics**
A tenant's or partner's white-label configuration (Chapter 12) may vary the specific token values responsive behaviour resolves to; it shall never redefine which category applies at a given viewport or what that category preserves. This is `DS-001-076` (White-Label Colour Remains Governed, Chapter 6) applied to responsive behaviour.

**DS-001-285: Marketing Shall Never Affect Product Responsive Behaviour**
A marketing or campaign surface's responsive treatment, however it is applied outside the product surface, shall never cause a product responsive behaviour category to be reinterpreted. This is `DS-001-037` (Marketing Campaigns Shall Not Redefine the Constitutional Brand, Chapter 4) applied specifically to responsive behaviour.

---

### Chapter 16 Validation

This chapter defines responsive behaviour as governed token resolution, not implementation: no breakpoint pixel value, CSS media query, responsive framework, or rendering technology appears anywhere above, including within `DS-001-280A`, which states its cognitive-continuity requirement in prose only. Every reference to how responsive behaviour is actually resolved is deferred explicitly to Chapter 10 (Breakpoint, Sizing, Spacing, and Grid Tokens) and Chapter 11 (Theme Architecture), consistent with the deferral pattern every prior chapter established. `DS-001-274` and `DS-001-280` make SD-001-071's never-hide mandate and Chapter 14's completeness standard explicit constraints on every category in §16.3, closing the exact failure mode ("density adaptation via omission") the Ownership Matrix's split between DS-001 (visual) and SD-001 (structural) exists to prevent. `DS-001-280A` synthesizes those two principles, plus `DS-001-268` and `DS-001-273`, into the user-perceived outcome they jointly guarantee — cognitive continuity across viewport transitions — without introducing any new token, mandate, or overlap with SD-001's own structural principles. `DS-001-277` and `DS-001-278` cross-reference rather than restate `DS-001-196` (Chapter 11) and `DS-001-094` (Chapter 7). The chapter's scope was verified against the frozen Document Architecture before drafting, per the process note at the top of this chapter, and no subsection or title deviates from that verification.

*End of Chapter 16.*

---

## SECTION 17: Accessibility Styling

*A verification note before proceeding:* this chapter's title and scope were verified against the frozen Document Architecture before drafting. Five earlier chapters cite Chapter 17 by number (§5.6, two entries in §6.3, `DS-001-095`, `DS-001-167`), including two references to "the legibility standard this chapter... establishes" — a standard not yet defined anywhere in this document. No competing brief was supplied. Eleven chapters (5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16) already established their own domain-specific accessibility principles; this chapter does not restate them. Its role is to define the closed set of accessibility modes DS-001 styles, state the legibility standard by name, index the eleven prior chapters' principles, and complete the SD-001 §10 mandates no chapter has yet addressed.

This chapter defines the constitutional architecture of Accessibility Styling within AUREX — the token-level realization of the accessibility modes SD-001 §10 mandates must exist. It defines architectural intent only. It does not define contrast ratios, WCAG conformance levels as numeric targets, ARIA attribute syntax, or any implementation technology; those belong to Accessibility Tokens (Chapter 10, §10.3) and implementation repositories.

### 17.1 Purpose

SD-001 establishes that accessibility is the baseline configuration, not an opt-in mode (`SD-001-059`), and requires that high-contrast, reduced-motion, and large-text modes exist (`SD-001-063`). Eleven prior chapters have each, independently, ensured their own domain — colour, typography, icons, illustration, tokens, themes, branding, components, motion, responsive behaviour — satisfies that mandate. This chapter exists to complete what no single prior chapter could: naming the accessibility modes themselves as a closed constitutional set, defining the legibility standard those chapters build toward, and closing the handful of SD-001 §10 mandates (reading complexity, cultural neutrality, inclusive collaboration, human dignity, testing-as-release-gate) that remain unaddressed until now.

### 17.2 Accessibility Mode Architecture

AUREX styles three constitutional accessibility modes, each satisfying a distinct clause of `SD-001-063`.

| Accessibility Mode | Purpose | Primary Token Path |
|---|---|---|
| High-Contrast Mode | Satisfies SD-001's high-contrast requirement; realized as High-Contrast Theme (Chapter 11, §11.3) and Accessibility Colours (Chapter 6, §6.3). | Accessibility Tokens grouping (Chapter 10, §10.3) |
| Reduced-Motion Mode | Satisfies SD-001's reduced-motion requirement; suppresses non-essential motion while preserving communicated meaning (`DS-001-261`, Chapter 15). | Motion, Animation, and Transition Tokens, resolved through Accessibility Tokens |
| Large-Text Mode | Satisfies SD-001's large-text requirement; scales Typography Tokens while preserving the Reading Architecture's hierarchy (Chapter 7, §7.4) and reading-layer distinctions. | Typography Tokens, resolved through Accessibility Tokens |

**DS-001-286: The Accessibility Mode Architecture Is a Closed, Named Set of Three Modes**
No accessibility mode exists outside High-Contrast, Reduced-Motion, and Large-Text. A future need that appears to require a new mode is resolved by proposing an extension to this closed set through constitutional review (§17.9), never by an ad hoc styling variant invented outside it. This is `DS-001-027` (Extend, Never Fork) applied to Accessibility Styling. Every mode is orthogonal to every other — a user may activate any combination simultaneously, consistent with `DS-001-194` (Chapter 11).

### 17.3 The Legibility Standard

**DS-001-287: The Legibility Standard**
*Statement.* Content satisfies the AUREX Legibility Standard when it remains correctly perceivable and correctly interpretable under all three accessibility modes (§17.2), at every viewport (Chapter 16), under every theme (Chapter 11), and in printed media, without requiring the reader to already know what the content says.
*Architectural Rationale.* Chapters 6 and 7 each referenced "the legibility standard this chapter and Chapter 17 establish" before this chapter existed to define it — a forward reference this principle now closes. Legibility is defined as a testable property (perceivable, interpretable, under stated conditions, without prior knowledge) rather than a subjective aesthetic judgment, because a standard that cannot be tested cannot be a release gate (§17.8).
*Practical Implications.* A design is not legible because it looks clear to someone who already knows what it should say — it is legible when a first-time reader, using any accessibility mode, at any supported viewport, in any theme, correctly perceives and interprets it. This is the test `DS-001-095` (Chapter 7) and the Content Colours entry (Chapter 6, §6.3) already presumed exists.

### 17.4 Relationship with Design Tokens

**DS-001-288: Accessibility Styling Is Resolved Only Through the Accessibility Tokens Grouping**
Implementations SHALL consume accessibility styling exclusively through the Accessibility Tokens Compositional Grouping Chapter 10 defines (§10.3) — itself composed of Focus, Colour, Typography, and Opacity Tokens. No implementation, capability, or extension shall hard-code an accessibility-mode-specific value outside that system. This restates `DS-001-167` (Chapter 10) as this chapter's own governing rule: an accessibility fix applied outside the token system cannot be verified against the Legibility Standard (§17.3) or propagated when the underlying tokens evolve.

### 17.5 Consolidated Accessibility Index

This chapter indexes, rather than restates, the accessibility principles eleven prior chapters already established. Each remains authoritative in its own chapter; this table exists so Accessibility Styling is discoverable as one coherent standard rather than eleven scattered ones.

| Chapter | Accessibility Principles |
|---|---|
| Chapter 5 (Logo System) | `DS-001-050` — logo identity invariant across theme, medium, and accessibility mode |
| Chapter 6 (Colour System) | `DS-001-069`–`072` — colour never the sole indicator, colour-vision-safe, dark-mode/print coherence, AI colour-explainability |
| Chapter 7 (Typography) | `DS-001-093`–`096` — screen-reader compatibility, zoom/reflow legibility, density without legibility loss, accessibility never reduced |
| Chapter 8 (Iconography) | `DS-001-116`–`119` — accessible names, perceivable labels, high-contrast legibility, cognitive accessibility |
| Chapter 9 (Illustration) | `DS-001-140`–`144` — alternative descriptions, cognitive accessibility, screen-reader compatibility, contrast/print legibility, accessibility never reduced |
| Chapter 10 (Design Tokens) | `DS-001-167`–`170` — resolved through tokens not overrides, high-contrast paths mandatory, responsive scaling, multi-device/print consistency |
| Chapter 11 (Theme System) | `DS-001-193`–`197` — High-Contrast Theme mandate, every mode supported by every theme, print/responsive/multi-device consistency |
| Chapter 12 (White-Label Branding) | `DS-001-214`–`216` — branding never weakens accessibility, High-Contrast functions under every brand, responsive/print consistency |
| Chapter 13 (Component Standards) | `DS-001-232` — components preserve accessibility, responsive, print, high-contrast, and keyboard-navigation behaviour |
| Chapter 15 (Motion) | `DS-001-261` — reduced-motion suppresses animation without removing communicated meaning |
| Chapter 16 (Responsive Behaviour) | `DS-001-278`–`279` — legible under zoom, touch targets satisfy accessibility minimums |

**DS-001-289: This Chapter Indexes, It Does Not Duplicate, Prior Chapters' Accessibility Principles**
The table above is a navigational aid, not an independent restatement. A conflict between this chapter's summary of a prior principle and that principle's own text is resolved in the owning chapter's favor without exception, consistent with `DS-001-165` (Chapter 10).

### 17.6 Completing SD-001 §10

Four of SD-001's accessibility mandates (§10) have no prior chapter addressing them. This section closes each.

**DS-001-290: Reading Complexity Preferences Resolve Through Typography Tokens, Never a Parallel Reading Architecture**
SD-001's plain-language executive-summary preference (`SD-001-065`) is satisfied by Large-Text Mode's typographic resolution (§17.2) applied to a content-simplification decision SD-001, not DS-001, governs. DS-001 provides the styling capability; it does not decide when plain language is offered.

**DS-001-291: Cultural Neutrality Is a Cross-Family Verification Requirement, Not a Single Family**
SD-001's cultural-neutrality mandate (`SD-001-066`) is already addressed per-family — icons (`DS-001-104`, Chapter 8) and illustrations (`DS-001-130`, `DS-001-137`, Chapter 9). This principle establishes that cultural neutrality is additionally verified as a cross-family property: a colour, icon, and illustration combination that is individually neutral but collectively carries unintended meaning in a specific market fails this requirement even though no single family failed it alone.

**DS-001-292: Inclusive Collaboration Styling Extends to Collaboration Components**
SD-001's inclusive-collaboration mandate (`SD-001-067`) — asynchronous, timezone-neutral, language-mixed collaboration — is styled through the Collaboration Components category (Chapter 13, §13.3: Comment Thread, Mention, Assignment Panel, Approval Queue, Activity Feed), using the same Accessibility Tokens grouping (§17.4) as every other component.

**DS-001-293: Human Dignity by Design Governs Error and Empty State Tone**
SD-001's human-dignity mandate (`SD-001-069`) — no screen frames a user as the cause of failure — is a styling constraint on Empty State (Chapter 19) and future error-state visual treatment: tone, colour, and iconography frame the system's next step, never the user's fault, consistent with `DS-001-069`'s language requirement extended to visual language.

### 17.7 Enterprise Intelligence Accessibility

**DS-001-294: Enterprise Intelligence Visual Standards Are Verified Under Every Accessibility Mode**
Each of Chapter 14's eleven domain visual standards (§14.1–14.11) is verified against all three accessibility modes (§17.2), not only against its own chapter's accessibility principles. An Evidence Panel that satisfies `DS-001-239` (Chapter 14) but becomes illegible under Large-Text Mode has not satisfied the Legibility Standard (§17.3) and is not release-conformant regardless of its Chapter 14 completeness.

### 17.8 Accessibility Testing as a Release Gate

**DS-001-295: Accessibility Conformance Is a First-Class Release Gate for DS-001 Itself**
Consistent with SD-001's requirement that no screen ships without an accessibility test pass on the same footing as a functional test pass (`SD-001-068`), no token, theme, component, or domain visual standard defined by this document ships without verification against the Legibility Standard (§17.3) under all three accessibility modes (§17.2). This is a DS-001-level release gate, not only an SD-001-level one; the specific testing and release process is governed by Design Governance (Chapter 22, §22.1, §22.10).

**DS-001-295A: Accessibility Shall Preserve Enterprise Equality**
*Statement.* Accessibility Styling SHALL ensure that every user, regardless of accessibility mode, receives equivalent Enterprise Intelligence. Accessibility modes MAY change presentation. Accessibility modes SHALL NEVER reduce Business Meaning, Enterprise Context, Evidence, Confidence, Explainability, Governance Information, or Decision Quality.
*Architectural Rationale.* Accessibility exists to remove barriers, not to reduce information. Enterprise users operating under any Accessibility Mode shall receive equivalent decision-making capability. Accessibility therefore preserves equality of Enterprise Intelligence rather than merely improving visual usability — extending `DS-001-294` (Enterprise Intelligence Visual Standards Are Verified Under Every Accessibility Mode) from a verification requirement into the outcome that verification exists to guarantee, and completing the Legibility Standard's (`DS-001-287`) "correctly interpretable" clause specifically for Chapter 14's eleven domain concepts.
*Practical Implications.* Large-Text Mode, Reduced-Motion Mode, and High-Contrast Mode (§17.2) may alter visual presentation. They SHALL NOT reduce Enterprise Intelligence. Every accessibility mode shall preserve decision confidence, governance traceability, and evidence transparency. A mode that satisfies §17.2's styling requirements while causing a Confidence Indicator or Evidence Panel to communicate less than its default rendering fails this principle regardless of its technical conformance to the mode's own styling rules.

### 17.9 Governance

**DS-001-296: Accessibility Styling Evolves Rarely and Constitutionally**
The Accessibility Mode Architecture (§17.2) and Legibility Standard (§17.3) change rarely, and only through the same constitutional review discipline as any other change to this document.

**DS-001-297: New Accessibility Modes Require Constitutional Review**
A proposed fourth accessibility mode is admitted only through constitutional review — never through unilateral introduction by a design contributor, capability team, or implementation effort.

**DS-001-298: Capability Teams Shall Not Introduce Accessibility Systems**
Consistent with the equivalent principles in Chapters 6 through 16, a capability or Business Activity team has no authority to introduce a new accessibility mode or an independent accessibility mechanism. A capability that requires accessibility support this chapter does not yet provide proposes an extension through the Design Governance contribution process (Chapter 22 §22.4).

**DS-001-299: White-Label Branding Shall Never Weaken Accessibility Styling**
This restates `DS-001-214` (Chapter 12) as this chapter's own governing rule: no brand variant, however faithfully it expresses a tenant's or partner's identity, may resolve a token below the Legibility Standard (§17.3).

**DS-001-300: Marketing Shall Never Affect Product Accessibility Styling**
A marketing or campaign surface's accessibility treatment, however it is applied outside the product surface, shall never cause a product accessibility mode to be reinterpreted or weakened. This is `DS-001-037` (Chapter 4) applied specifically to accessibility styling.

---

### Chapter 17 Validation

This chapter defines accessibility styling as governed token resolution, not implementation: no contrast ratio, WCAG numeric target, ARIA syntax, or implementation technology appears anywhere above, including within `DS-001-295A`, which states its equality requirement in prose only. Eleven prior chapters' accessibility principles are indexed (§17.5, `DS-001-289`), not duplicated — each conflict-resolution default favors the owning chapter. The "legibility standard" two chapters referenced by name without it existing is now defined (`DS-001-287`), closing that forward reference. Four previously unaddressed SD-001 §10 mandates — reading complexity, cultural neutrality as a cross-family property, inclusive collaboration, and human dignity — are completed (§17.6) without duplicating the per-family work Chapters 6 through 9 already did. Chapter 14's domain visual standards are extended, not restated, into an explicit accessibility-mode verification requirement (`DS-001-294`), which `DS-001-295A` carries one step further into a guaranteed outcome: no accessibility mode may reduce Business Meaning, Enterprise Context, Evidence, Confidence, Explainability, Governance Information, or Decision Quality — a constraint stated entirely at the level of what a mode preserves, with no overlap into SD-001's own behavioral or structural mandates. The chapter's scope was verified against the frozen Document Architecture before drafting, per the process note at the top of this chapter, and no subsection or title deviates from that verification.

*End of Chapter 17.*

---

## SECTION 18: Dashboard, Chart & Data Visualization Language

*A verification note before proceeding:* this chapter's title and scope were verified against the frozen Document Architecture before drafting. No subsections are frozen. Four earlier chapters cross-reference this chapter's content by number or by forward-used concept (§2.4 twice, §3.4, and Chapter 14 §14.6/§14.10, which already cite "Data Visualisation Colours," "Chart Tokens," "Knowledge Graph Renderer," and "Risk Matrix" as though defined). No competing brief was supplied.

**This chapter is primarily an integration chapter**, in the same sense Chapters 14 and 17 are: it introduces no new colour, icon, typography, or token family. It completes the visual language Chapter 6 (Data Visualisation Colours) and Chapter 10 (Chart Tokens) already named but did not fully specify, and supplies the visual standards for the nine Visualization Components Chapter 13's frozen catalogue already lists. It also draws an explicit boundary the Ownership Matrix implies but never states directly: Executive Dashboard treatment is Chapter 14 §14.9's domain-specific composition; this chapter supplies the general-purpose data visualization language that composition, and every other domain concept's chart needs, draws upon.

### 18.1 Purpose

SD-001 names "Dashboard" only as a structural layout-template slot (`SD-001-024`) and evaluates dashboard and chart treatment against `DS-001-016` (Calm by Default, Loud by Exception) and `DS-001-023` (Progressive Visual Disclosure), per Chapter 3 §3.4. Beyond that structural placeholder, SD-001 says nothing about how a chart, dashboard, or data visualization actually looks — this is entirely DS-001's constitutional territory (Ownership Matrix, §2.4). This chapter exists to complete that territory: to give Data Visualisation Colours and Chart Tokens their full visual standard, and to define the nine Visualization Components Chapter 13 already named.

### 18.2 Dashboard & Chart Philosophy

**DS-001-301: Dashboards Are Evaluated Against Calm by Default and Progressive Disclosure**
This restates, as this chapter's own governing rule, the evaluation criteria Chapter 3 §3.4 already established: a dashboard's visual density defaults to calm (`DS-001-016`), and additional density is revealed only as a user chooses to go deeper (`DS-001-023`). No dashboard or chart in AUREX is exempt from either test.

**DS-001-302: Charts Communicate Before They Impress**
A chart exists to make a quantitative relationship faster to understand than the underlying numbers alone would allow. This is `DS-001-017` (Clarity Before Decoration, Chapter 3) applied specifically to data visualization: a chart type chosen for visual sophistication over the clarity of the relationship it depicts is not conformant, regardless of its technical polish.

### 18.3 Data Visualization Component Architecture

This chapter supplies the visual standard for each of the nine Visualization Components the frozen Component Catalogue (Chapter 13, §13.3) already names.

| Component | Purpose | Composed From |
|---|---|---|
| Chart Primitives (bar, line, trend, waterfall) | Render quantitative relationships — magnitude, trend, composition — as directly comparable visual marks. | Data Visualisation Colours (Chapter 6, §6.3); Chart Tokens (Chapter 10, §10.3) |
| Risk Matrix | Render risk severity against likelihood on a two-axis grid. | Decision Support Colours; Risk Icons (Chapter 8, §8.3) — as already established by Chapter 14, `DS-001-248` |
| Coverage Card | Summarize completeness of a discovery or evidence-gathering effort. | Data Visualisation Colours; Evidence Tokens (Chapter 10, §10.8) |
| Timeline | Render a chronological sequence of events, decisions, or state changes. | Data Visualisation Colours; Chart Tokens |
| Heatmap | Render density or intensity across a two-dimensional grid. | Data Visualisation Colours, calibrated for sequential perceptual accuracy (§18.4) |
| Data Table | Render tabular data with row- and column-level structure. | Content Colours (Chapter 6, §6.3); Typography (Chapter 7, Analytical Reading) |
| Sparkline | Render a compact, label-free trend indicator inline with other content. | Chart Tokens |
| KPI / Stat Tile | Render a single headline metric with its business consequence, per `SD-001-057`. | Typography (Executive Reading, Chapter 7, §7.3); Decision Support Colours where the metric carries evaluative meaning |
| Knowledge Graph Renderer | Render arbitrary relationship data as nodes and edges. | Fully specified by Chapter 14, §14.6 (`DS-001-244`) |

**DS-001-303: The Data Visualization Component Set Is Closed, Realizing the Frozen Catalogue's Visualization Components Category**
No visualization component exists outside the nine above. This set is identical to, and does not extend, Chapter 13's frozen Visualization Components category. A future need that appears to require a new visualization component is resolved by proposing an extension to this closed set through constitutional review of both this chapter and Chapter 13 (§18.9), never by an ad hoc chart type invented outside it.

### 18.4 Chart Colour & Perceptual Accuracy

**DS-001-304: Chart Colour Is Calibrated for Perceptual Accuracy, Not Brand Expression**
*Statement.* This completes Chapter 6's Data Visualisation Colours entry (§6.3): chart colour is selected and ordered for accurate quantitative perception — correct ordering, correct magnitude judgment, correct categorical distinction — even where that selection diverges from Brand Colours' identity-expression goals.
*Architectural Rationale.* A chart whose colour sequence is chosen for brand harmony rather than perceptual accuracy can misrepresent the data it displays — an ordinal colour scale that doesn't perceptually order, or a categorical palette with insufficient distinction between adjacent categories, communicates incorrectly regardless of how on-brand it looks. This would violate SD-001's evidence-first mandate (`SD-001` §1.6) as surely as an inaccurate number would.
*Practical Implications.* Where Brand Colours (white-label or default) and perceptually accurate chart colour would conflict, Chart Tokens resolve toward perceptual accuracy; Brand Colours' influence on data visualization is limited to accent and chrome, never to the data-bearing marks themselves.

**DS-001-305: Categorical, Sequential, and Diverging Chart Palettes Are Constitutionally Distinct**
A chart distinguishing unordered categories, a chart showing a single ordered progression (low to high), and a chart showing divergence from a meaningful midpoint (below/above target) each require a distinct palette structure. Chart Tokens (Chapter 10, §10.3) resolve each purpose separately; a categorical palette is never reused for a sequential or diverging purpose, and vice versa, consistent with `DS-001-064` (One Family Per Concept, Chapter 6).

### 18.5 Relationship with Design Tokens

**DS-001-306: Data Visualization Is Resolved Only Through Chart Tokens and Data Visualisation Colours**
Implementations SHALL consume data visualization exclusively through Chart Tokens (Chapter 10, §10.3) and Data Visualisation Colours (Chapter 6, §6.3). No implementation, capability, or extension shall hard-code a chart colour, spacing, or typographic value outside that system. This is `DS-001-015` (One Token, Every Surface, Chapter 3) applied specifically to data visualization, mirroring the equivalent principles in every prior visual-language chapter.

### 18.6 Dashboard Composition

**DS-001-307: A Dashboard Is a Governed Composition of Visualization Components Within SD-001's Dashboard Layout Template**
A Dashboard is not an independent visual construct; it is an assembly of one or more Visualization Components (§18.3) placed within the Dashboard layout template SD-001 defines structurally (`SD-001-024`). This chapter governs how each component looks; SD-001 governs which template positions it within, consistent with the Structure vs. Appearance boundary Chapter 2 establishes (`DS-001-002`).

**DS-001-308: Operational Dashboards and Executive Dashboards Share One Component Set, Different Density**
An operational (Layer 1) dashboard and an Executive (Sacred 12) dashboard draw on the identical nine-component set (§18.3); they differ only in density and calm-tone register — the Executive Dashboard resolving through Boardroom Theme's lowest-intensity registrations (`DS-001-247`, `DS-001-260`), the operational dashboard resolving through Light or Dark Theme's fuller density. Neither dashboard type has a component the other lacks.

### 18.7 Relationship with Chapter 14

**DS-001-309: This Chapter Supplies the General Data Visualization Language; Chapter 14 Composes It for Domain-Specific Concepts**
This chapter's colour calibration (§18.4), token resolution (§18.5), and nine-component catalogue (§18.3) are the general-purpose visualization language every domain concept's chart or graph needs draws upon. Chapter 14 composes that language for specific Enterprise Intelligence concepts — Knowledge Graph Visual Standards (§14.6) and Risk Indicator Visual Standards (§14.10) already do so, citing this chapter's Knowledge Graph Renderer and Risk Matrix components respectively. This chapter does not restate those compositions; Chapter 14 remains their sole authority.

**DS-001-309A: Data Visualization Shall Preserve Decision Integrity**
*Statement.* Data Visualization exists to improve understanding. It SHALL NEVER influence interpretation through visual exaggeration, visual suppression, or visual ambiguity. Every Dashboard, Chart, Graph, Matrix, Timeline, Coverage Card, and Data Table SHALL faithfully preserve the meaning established by the underlying Enterprise Intelligence.
*Architectural Rationale.* Enterprise decisions depend upon trustworthy visual representation. Visualizations exist to communicate information, not to persuade users toward a predetermined conclusion. Decision Integrity therefore requires that visual representation remain faithful to the underlying Enterprise Intelligence. This principle extends Chapter 14's Domain Visual Language — specifically `DS-001-243` (A Recommendation Is Never Rendered Indistinguishably From a Confirmed Fact) and `DS-001-249` (Trust Is the Composite Outcome of the Preceding Ten Standards) — into quantitative visual communication, and is the data-visualization-specific expression of `DS-001-302` (Charts Communicate Before They Impress, §18.2): a chart that impresses by distorting is the clearest possible failure of that principle.
*Practical Implications.* Visual emphasis MAY improve comprehension. Visual emphasis SHALL NOT distort meaning. Scaling, grouping, aggregation, highlighting, or filtering SHALL preserve semantic accuracy — a truncated axis that exaggerates a difference, a grouping that obscures an outlier, or a filter that silently removes unfavorable data all fail this principle regardless of whether the underlying Chart Tokens (§18.5) were technically applied correctly. A visualization that changes the user's interpretation without a corresponding change in the underlying Enterprise Intelligence fails this constitutional principle.

### 18.8 Accessibility

**DS-001-310: Chart Series Differentiation Never Relies on Colour Alone**
This restates `DS-001-069` (Colour Alone Never Carries Meaning, Chapter 6) as this chapter's own governing rule for chart series specifically: every categorical chart series is distinguishable through pattern, marker shape, or direct labeling in addition to colour, satisfying the Legibility Standard (Chapter 17, §17.3) under colour-vision variation.

**DS-001-311: Data Tables Satisfy Screen-Reader Tabular Navigation**
A Data Table component (§18.3) declares row and column structure in a form a screen reader can navigate as a table, not merely announce as unstructured text, consistent with SD-001's screen-reader compatibility mandate (`SD-001-061`) and the Legibility Standard (Chapter 17, §17.3).

### 18.9 Governance

**DS-001-312: Data Visualization Language Evolves Rarely and Constitutionally**
The Data Visualization Component Architecture (§18.3) and chart colour calibration (§18.4) change rarely, and only through the same constitutional review discipline as any other change to this document.

**DS-001-313: New Visualization Component Types Require Constitutional Review**
A proposed tenth visualization component is admitted only through constitutional review of both this chapter and Chapter 13's frozen catalogue — never through unilateral introduction by a design contributor, capability team, or implementation effort.

**DS-001-314: Capability Teams Shall Not Introduce Chart Systems**
Consistent with the equivalent principles in Chapters 6 through 17, a capability or Business Activity team has no authority to introduce a new chart type, palette structure, or independent visualization system. A capability that requires visualization support this chapter does not yet provide proposes an extension through the Design Governance contribution process (Chapter 22 §22.4).

**DS-001-315: White-Label Branding Shall Not Redefine Chart Semantics**
A tenant's or partner's white-label configuration (Chapter 12) may vary chart chrome and accent within the Brand Colours family; it shall never redefine a chart's perceptually calibrated data-bearing colours (§18.4) or a Visualization Component's meaning. This is `DS-001-076` (Chapter 6) applied to data visualization.

**DS-001-316: Marketing Shall Never Affect Product Data Visualization**
A marketing or campaign use of a chart or dashboard visual, however it is applied outside the product surface, shall never cause a product chart's perceptual calibration or component meaning to be reinterpreted. This is `DS-001-037` (Chapter 4) applied specifically to data visualization.

---

### Chapter 18 Validation

This chapter completes, without redefining, the Data Visualisation Colours (Chapter 6) and Chart Tokens (Chapter 10) families and supplies the visual standards for Chapter 13's nine frozen Visualization Components — closing the forward references Chapter 14 §14.6 and §14.10 already made to this content. No new colour, icon, typography, or token family is introduced (`DS-001-306`); every principle instead names the Chapter 6/10 elements it completes. §18.7 (`DS-001-309`) states explicitly, as instructed, that this is an integration chapter, and draws the boundary the Ownership Matrix implies but never states: Executive Dashboard composition remains Chapter 14 §14.9's authority, not restated here. `DS-001-309A` extends, rather than duplicates, Chapter 14's `DS-001-243` and `DS-001-249` into quantitative visual communication specifically — preserving Decision Integrity against exaggeration, suppression, or ambiguity through scaling, grouping, aggregation, highlighting, or filtering, with no restatement of Chapter 14's own domain-concept principles. No CSS, HTML, JSON, JavaScript, React, Vue, Angular, rendering engine, or framework-specific content appears anywhere above. The constitutional dependency chain remains intact — this chapter's components consume Chart Tokens and Data Visualisation Colours exactly as Chapter 13's components consume tokens, themes, and brand resolution generally (`DS-001-230`). The chapter's scope was verified against the frozen Document Architecture before drafting, per the process note at the top of this chapter, and no subsection or title deviates from that verification.

*End of Chapter 18.*

---

## SECTION 19: Empty State Design

*A verification note before proceeding:* this chapter's title and scope were verified against the frozen Document Architecture before drafting. No subsections are frozen. Two prior chapters already establish content this chapter must integrate rather than restate — Chapter 9's Empty State Illustrations family (§9.3) and Chapter 17's `DS-001-293` (empty-state tone must never blame the user). No competing brief was supplied.

**This chapter is a hybrid chapter, not a purely integrative one.** It integrates the two elements named above without restating them. It also introduces constitutional principles no prior chapter has defined: the Empty State's structural composition, what an empty state must communicate, and how empty states preserve Enterprise Intelligence, user confidence, and trust specifically. Where this chapter states a new principle, it is marked as new; where it draws on Chapter 9 or Chapter 17, it cites rather than reproduces.

### 19.1 Purpose

SD-001 mandates that an empty state never say "No data found" — it must state what is missing and offer the same resolution paths as Guided Completion (`SD-001-025`, `SD-001-041`, `SD-001-004`). This chapter defines the visual treatment that mandate requires: an Empty State is not the absence of a screen's content — it is a screen's content, communicating that a resolution attempt is available and inviting the user into it. This is a resolution opportunity, not an absence notice.

### 19.2 Empty State Philosophy

**DS-001-317: An Empty State Is a Resolution Opportunity, Not an Absence Notice**
*[New principle.]* An Empty State's visual treatment communicates possibility, not deficiency. It renders with the same constitutional seriousness as any screen carrying data, because per `SD-001-025` it is never merely reporting an absence — it is always offering a path to resolve one.

**DS-001-318: Empty States Communicate Without Blame**
This restates `DS-001-293` (Chapter 17) as this chapter's own governing rule: an Empty State's tone, colour, and iconography frame the system's next step, never the user's fault for the absence they encountered.

**DS-001-319: Empty States Guide Toward the Next Step in the Six-Step Resolution Sequence**
*[New principle.]* An Empty State's visual guidance corresponds to wherever SD-001's six-step resolution sequence (`SD-001-004`: Extract → Retrieve → Infer → Confirm → Route → Ask) currently stands for the missing content — never to a generic "add data" prompt disconnected from what the platform has already attempted.

### 19.3 Empty State Visual Composition

*[New — no prior chapter defines Empty State's structural composition.]* An Empty State is composed of four constitutional elements.

| Element | Purpose | Composed From |
|---|---|---|
| Illustration | Depicts what is missing, sparingly and calmly. | Empty State Illustrations (Chapter 9, §9.3) — already fully defined; not restated here. |
| Message | States plainly what is missing, in one line, without blame. | Content Colours, Neutral Colours (Chapter 6, §6.3); Body-level typography (Chapter 7, Operational Reading). |
| Guidance | States what the platform has already attempted, per `SD-001-005`, before any manual action is requested. | Evidence Reading typography (Chapter 7, §7.3), where the guidance references a resolution attempt already made. |
| Action | Offers the next available resolution step — discover, upload, or enter manually, per `SD-001-004`'s ordering. | Action Icons (Chapter 8, §8.3); Action Center visual treatment (Chapter 13, Enterprise Intelligence Components), scaled to a single-action context. |

**DS-001-320: Empty State Composition Is a Closed, Four-Element Structure**
*[New principle.]* No Empty State renders outside the four elements above. A future need that appears to require a fifth element is resolved by proposing an extension to this closed structure through constitutional review (§19.9), never by an ad hoc addition invented outside it. This is `DS-001-027` (Extend, Never Fork) applied to Empty State Design.

### 19.4 What Empty States Communicate

**DS-001-321: Absence, Incompleteness, Next Action, and Guidance Are Distinct Communicative Purposes, Each Required**
*[New principle.]* An Empty State's Message (§19.3) communicates absence or incompleteness — that something specific is missing, not that the screen has failed. Its Guidance communicates what has already been attempted. Its Action communicates the next available step. These four purposes — absence, incompleteness, next action, guidance — are each required and are never collapsed into a single generic statement; a screen that only states absence without guidance or a next action satisfies none of `SD-001-025`'s actionability mandate.

### 19.5 Preserving Enterprise Intelligence

**DS-001-322: An Empty Enterprise Intelligence Component States What the Six-Step Sequence Already Attempted**
*[New principle.]* Where an Empty State appears within an Enterprise Intelligence Component — an Evidence Panel with no evidence yet found, a Confidence Indicator with nothing yet to score, a Business Activity Card not yet started — its Guidance (§19.3) states specifically which of `SD-001-004`'s six steps has been attempted for that component's content, consistent with Chapter 14's completeness discipline (`DS-001-238`): an incomplete Enterprise Intelligence rendering is still held to Chapter 14's standard for what it does show, even while what it is missing is exactly the empty state's subject.

### 19.6 Preserving User Confidence & Trust

**DS-001-323: Empty State Tone Reinforces, Never Undermines, Visual Trust**
*[New principle.]* An Empty State is rendered with the same calm, credible visual register `DS-001-024` (Visual Trust Builds Enterprise Trust, Chapter 3) requires of every other screen state. A user encountering an empty state should trust the platform exactly as much as when it is showing complete data — an anxious, alarming, or apologetic visual register undermines that trust regardless of how actionable the state's guidance technically is.

**DS-001-323A: Empty States Shall Preserve User Momentum**
*[New principle.]* *Statement.* An Empty State SHALL preserve the user's progress towards a meaningful outcome. An Empty State SHALL NEVER become a dead end. Every Empty State SHALL either explain the current situation, guide the user towards the next meaningful action, or confirm that no further action is required.
*Architectural Rationale.* Enterprise users interact with the platform to accomplish Business Activities, not to observe system states. An Empty State therefore exists to maintain user momentum rather than interrupt it. This principle extends `DS-001-318` (Empty States Communicate Without Blame) and `DS-001-323` (Empty State Tone Reinforces, Never Undermines, Visual Trust) into user progression: a blame-free, trustworthy empty state that still leaves a user with no sense of what happens next has satisfied tone without satisfying momentum — a distinct failure mode this principle closes.
*Practical Implications.* An Empty State MAY communicate absence, waiting, or incompleteness. It SHALL always communicate what happens next. Users SHALL never be left uncertain about the appropriate next action. Where an Empty State genuinely requires no further user action — a resolution is already in progress via the six-step sequence (`SD-001-004`) — its Guidance element (§19.3) states that explicitly, rather than leaving silence to be misread as inaction.

### 19.7 Relationship with Design Tokens

**DS-001-324: Empty State Visual Composition Is Resolved Only Through Governed Tokens**
*[New principle, following the established pattern.]* Implementations SHALL consume Empty State visual composition (§19.3) exclusively through governed Colour, Typography, Icon, and Illustration Tokens (Chapter 10). No implementation, capability, or extension shall hard-code an empty-state-specific value outside that system. This is `DS-001-015` (One Token, Every Surface, Chapter 3) applied specifically to Empty State Design.

### 19.8 Accessibility

**DS-001-325: Empty State Guidance Is Perceivable Without Requiring Sight of the Illustration**
*[New principle.]* An Empty State's Message, Guidance, and Action (§19.3) each carry their full meaning independent of the Illustration element — a screen-reader user who does not perceive the illustration receives the identical absence, guidance, and next-action information a sighted user receives. This is `DS-001-140` (Every Illustration Carries an Alternative Description, Chapter 9) applied specifically to Empty State's illustration, and satisfies the Legibility Standard (Chapter 17, §17.3).

### 19.9 Governance

**DS-001-326: Empty State Design Evolves Rarely and Constitutionally**
The four-element composition (§19.3) and communicative-purpose taxonomy (§19.4) change rarely, and only through the same constitutional review discipline as any other change to this document.

**DS-001-327: Capability Teams Shall Not Introduce Empty State Systems**
Consistent with the equivalent principles in Chapters 6 through 18, a capability or Business Activity team has no authority to introduce an Empty State composition outside §19.3's four elements. A capability that requires empty-state support this chapter does not yet provide proposes an extension through the Design Governance contribution process (Chapter 22 §22.4).

**DS-001-328: White-Label Branding Shall Not Redefine Empty State Tone**
A tenant's or partner's white-label configuration (Chapter 12) may vary Empty State's token-resolved appearance; it shall never redefine the no-blame tone (`DS-001-318`) or the four-element structure (§19.3). This is `DS-001-076` (Chapter 6) applied to Empty State Design.

**DS-001-329: Marketing Shall Never Affect Product Empty State Design**
A marketing or campaign surface's empty-state-like treatment, however it is applied outside the product surface, shall never cause a product Empty State's composition or tone to be reinterpreted. This is `DS-001-037` (Chapter 4) applied specifically to Empty State Design.

---

### Chapter 19 Validation

This chapter is explicitly identified as hybrid (opening note): it integrates Chapter 9's Empty State Illustrations (§9.3, not restated) and Chapter 17's `DS-001-293` (cited as `DS-001-318`, not restated), while introducing new principles — marked `[New]` throughout — for structural composition (§19.3, `DS-001-320`), communicative purpose (§19.4, `DS-001-321`), Enterprise Intelligence preservation (§19.5, `DS-001-322`), and trust preservation (§19.6, `DS-001-323`) that no prior chapter defined. Empty States never imply failure or user blame throughout (`DS-001-317`, `DS-001-318`, `DS-001-323`); they preserve Enterprise Intelligence (`DS-001-322`) and user confidence and trust (`DS-001-323`) by name, satisfying every item this chapter's validation was asked to verify. `DS-001-323A` extends `DS-001-318` and `DS-001-323` into user momentum specifically — no Empty State may become a dead end, and silence is never left to be misread as inaction — without restating either principle or overlapping Chapter 17's own tone mandate. No CSS, HTML, JSON, JavaScript, React, Vue, Angular, Figma implementation, or rendering-engine content appears anywhere above. The constitutional dependency chain remains intact — Empty State composition consumes governed tokens exclusively (`DS-001-324`), never an independent visual path. The chapter's scope was verified against the frozen Document Architecture before drafting, per the process note at the top of this chapter, and no subsection or title deviates from that verification.

*End of Chapter 19.*

---

## SECTION 20: Loading Experience

*A verification note before proceeding:* this chapter's title and scope were verified against the frozen Document Architecture before drafting. No subsections are frozen. Chapter 15 already forward-references this chapter directly (`DS-001` §15.3: "realized in full by Chapter 20") and draws the boundary between Progress & Loading Motion (here) and AI-Reasoning Motion (Chapter 14, §14.4, `DS-001-262`). No competing brief was supplied.

**This chapter is hybrid**, in the same sense Chapter 19 is. It completes Chapter 15's deferred Progress & Loading Motion specification and consumes the Progress Indicator and Loading Indicator components Chapter 13's frozen catalogue already names, without restating either. It also introduces new constitutional principles no prior chapter defined — most notably, that SD-001's "silently" clause for intelligent caching (`SD-001-080`) constitutionally requires the *absence* of loading treatment in a specific, named case. New principles are marked `[New]`.

### 20.1 Purpose

SD-001 requires that in-progress operations be shown with a stated percentage and estimated completion time (`SD-001-026`), that no operation over one second render without a progress indicator (`SD-001-078`), that perceived performance matter as much as actual performance (`SD-001-077`), and that background processing remain visible, never silently consuming resources unseen (`SD-001-082`). This chapter defines the visual treatment satisfying those mandates. Loading exists to preserve trust while Enterprise Intelligence is being prepared — it must reinforce that work is progressing, never that the system has stopped.

### 20.2 Loading Philosophy

**DS-001-330: Loading Communicates Continuity, Not Interruption**
*[New.]* A loading state is a continuation of the screen the user was already on, not a break from it. Its visual treatment preserves layout and context (skeleton placeholders preserving shape, per §20.3) rather than replacing the screen with an unrelated waiting indicator.

**DS-001-331: Loading Communicates Operational Honesty**
*[New.]* A loading treatment shows only what is actually true about the operation it represents — a percentage only where a percentage is genuinely computable, a completion estimate only where one is genuinely known. This is the visual-layer expression of `SD-001-026`'s stated-percentage-and-ETA mandate.

**DS-001-332: Loading Never Communicates False Progress**
*[New.]* No loading treatment advances, animates, or otherwise implies progress that has not genuinely occurred. An indeterminate spinner communicates "activity is occurring," never a specific degree of completion it cannot verify — the distinction §20.3 makes precise.

**DS-001-333: Loading Never Becomes Visual Noise**
Consistent with `DS-001-016` (Calm by Default, Loud by Exception, Chapter 3), a loading treatment's visual intensity is proportionate to the operation it represents — a brief, sub-second operation warrants a subtler treatment than a multi-step, multi-second one.

### 20.3 Loading Treatment Architecture

*[New — no prior chapter defines Loading's structural composition.]* AUREX defines five constitutional loading treatments.

| Treatment | Purpose | When Used |
|---|---|---|
| Skeleton Placeholder | Approximates the shape and layout of content about to load, preserving `DS-001-330`'s continuity. | Below-the-fold or asynchronously loading widgets, per SD-001's progressive-loading mandate (`SD-001-079`). |
| Progress Indicator (Determinate) | Shows a stated percentage and estimated completion time. | Any operation exceeding the one-second threshold SD-001 sets (`SD-001-078`), where a percentage is genuinely computable, per `SD-001-026`. |
| Activity Indicator (Indeterminate) | Communicates that activity is occurring without implying a specific degree of completion. | Operations where a percentage is not yet meaningfully computable, consistent with `DS-001-332`. |
| Background Processing Indicator | A persistent, header-level indicator (per `SD-001-034`) showing that AI or discovery activity is running behind the current screen. | Any background process, always visible per SD-001's transparent-background-processing mandate (`SD-001-082`) — never hidden. |
| Incremental Refresh Highlight | Marks specifically which values changed when a screen updates, without a full-screen reload treatment. | New evidence arriving on an already-rendered screen, per SD-001's incremental-refresh mandate (`SD-001-081`). |

**DS-001-334: The Loading Treatment Architecture Is a Closed, Named Set of Five Treatments**
*[New.]* No loading treatment exists outside the five above. A future need that appears to require a new treatment is resolved by proposing an extension to this closed set through constitutional review (§20.9), never by an ad hoc waiting indicator invented outside it. This is `DS-001-027` (Extend, Never Fork) applied to Loading Experience.

### 20.4 Operational Honesty

**DS-001-335: Loading Never Overstates Progress It Cannot Verify**
*[New.]* A Progress Indicator (Determinate, §20.3) displays a percentage only when that percentage reflects a genuinely measured degree of completion. Where completion cannot be genuinely measured, the Activity Indicator (Indeterminate) is used instead — a determinate-looking treatment applied to an indeterminate operation is a form of `DS-001-332`'s prohibited false progress, regardless of intent.

**DS-001-336: Silent Cache Refresh Shows No Loading Treatment**
*[New.]* *Statement.* Where SD-001's intelligent-caching mandate applies — a previously resolved, high-confidence value rendering instantly from cache while a background refresh check runs silently (`SD-001-080`) — no loading treatment from §20.3 is shown for that refresh. The value renders as already complete.
*Architectural Rationale.* SD-001-080 uses the word "silently" deliberately: a refresh check the user is not meant to perceive would be contradicted by any visible loading treatment accompanying it. This is the one case in this chapter where the constitutionally correct visual treatment is the explicit absence of one, and it is stated here precisely so that absence is not mistaken for an oversight.
*Practical Implications.* A design that adds a subtle loading indicator "just to be safe" during a silent cache refresh violates `SD-001-080` regardless of how unobtrusive that indicator is. If the underlying refresh discovers the cached value was stale, the resulting change is communicated through Incremental Refresh Highlight (§20.3) once the new value is known — never through a loading treatment shown during the silent check itself.

**DS-001-336A: Loading Experience Shall Preserve Temporal Trust**
*[New.]* *Statement.* The Loading Experience SHALL accurately communicate the relationship between user action and system progress. Loading SHALL NEVER create the perception that work is occurring when no meaningful work is being performed. Likewise, Loading SHALL NEVER conceal meaningful processing that materially affects user understanding.
*Architectural Rationale.* Enterprise users make decisions while interacting with the platform. Their confidence depends not only upon what is shown, but also upon when information becomes available. Temporal Trust therefore requires that the Loading Experience honestly reflect the operational state of the platform. This principle extends `DS-001-331` (Operational Honesty) and `DS-001-336` (Silent Cache Refresh) into a single constitutional guarantee: the first governs what a loading treatment claims while visible, the second governs when a loading treatment must not appear at all, and this principle governs the two failure directions between them — fabricated activity and concealed activity — as one unified requirement rather than two separate rules that happen to point the same way.
*Practical Implications.* Loading indicators MAY communicate preparation, processing, retrieval, or synchronization. They SHALL NEVER simulate progress. They SHALL NEVER delay completion for visual effect — an operation that finishes in 200ms is never artificially extended to make a progress indicator feel substantial. They SHALL NEVER hide significant background processing that changes Enterprise Intelligence, consistent with SD-001's transparent-background-processing mandate (`SD-001-082`).

### 20.5 Preserving Enterprise Trust & Decision Confidence

**DS-001-337: Loading Treatment for Enterprise Intelligence Components Preserves Their Chapter 14 Standard While Incomplete**
*[New.]* Where a loading treatment applies to an Evidence Panel, Confidence Indicator, or any other Enterprise Intelligence Component (Chapter 14), it renders as a Skeleton Placeholder matching that component's completed shape (§20.3) — never as a generic spinner substituted for the component entirely. This preserves `DS-001-024` (Visual Trust Builds Enterprise Trust, Chapter 3): a user should recognize what kind of intelligence is loading, not only that something is.

### 20.6 Relationship with Motion

**DS-001-338: Progress & Loading Motion Is Fully Specified Here, Completing Chapter 15's Forward Reference**
Chapter 15's Progress & Loading Motion category (`§15.3`) is fully realized by this chapter's five treatments (§20.3): each treatment's motion — a skeleton's subtle shimmer, a determinate bar's fill, an indeterminate indicator's cycle — draws on Motion Tokens (Chapter 10, §10.3) exactly as Chapter 15 governs, and is not redefined here. This chapter and Chapter 15 do not duplicate one another: Chapter 15 establishes that loading motion communicates rather than decorates; this chapter establishes what loading actually is.

### 20.7 Relationship with Design Tokens

**DS-001-339: Loading Treatment Is Resolved Only Through Governed Tokens**
*[New, following the established pattern.]* Implementations SHALL consume loading treatment (§20.3) exclusively through governed Colour, Motion, Animation, and State Tokens (Chapter 10). No implementation, capability, or extension shall hard-code a loading-specific value outside that system. This is `DS-001-015` (One Token, Every Surface, Chapter 3) applied specifically to Loading Experience.

### 20.8 Accessibility

**DS-001-340: Loading State Changes Are Perceivable to Assistive Technology**
*[New.]* A transition into or out of a loading state (§20.3) is perceivable to assistive technology at the moment it occurs, not only through the visual treatment itself — satisfying the Legibility Standard (Chapter 17, §17.3) and SD-001's screen-reader compatibility mandate (`SD-001-061`).

### 20.9 Governance

**DS-001-341: Loading Experience Evolves Rarely and Constitutionally**
The Loading Treatment Architecture (§20.3) changes rarely, and only through the same constitutional review discipline as any other change to this document.

**DS-001-342: Capability Teams Shall Not Introduce Loading Systems**
Consistent with the equivalent principles in Chapters 6 through 19, a capability or Business Activity team has no authority to introduce a loading treatment outside §20.3's five. A capability that requires loading support this chapter does not yet provide proposes an extension through the Design Governance contribution process (Chapter 22 §22.4).

**DS-001-343: White-Label Branding Shall Not Redefine Loading Honesty**
A tenant's or partner's white-label configuration (Chapter 12) may vary loading treatment's token-resolved appearance; it shall never redefine `DS-001-331`'s operational-honesty requirement or `DS-001-336`'s silent-refresh rule. This is `DS-001-076` (Chapter 6) applied to Loading Experience.

**DS-001-344: Marketing Shall Never Affect Product Loading Experience**
A marketing or campaign surface's loading-like treatment, however it is applied outside the product surface, shall never cause a product loading treatment's meaning to be reinterpreted. This is `DS-001-037` (Chapter 4) applied specifically to Loading Experience.

---

### Chapter 20 Validation

This chapter is explicitly identified as hybrid (opening note): it completes Chapter 15's `§15.3` forward reference to Progress & Loading Motion (`DS-001-338`) and consumes Chapter 13's Progress/Loading Indicator components, without restating either. New principles are marked `[New]` throughout, most notably `DS-001-336`, which establishes the constitutionally required *absence* of loading treatment during SD-001-080's silent cache refresh — a case easy to overlook and stated here explicitly. `DS-001-336A` unifies `DS-001-331` and `DS-001-336` into a single Temporal Trust guarantee covering both failure directions — fabricated activity and concealed activity — without restating either principle or overlapping Chapter 15's motion-communicates-not-decorates discipline. Loading preserves Enterprise Trust (`DS-001-337`) and communicates operational honesty (`DS-001-331`, `DS-001-335`, `DS-001-336A`) by name; it never exaggerates progress (`DS-001-332`, `DS-001-335`, `DS-001-336A`) or misleads users (`DS-001-336`, `DS-001-336A`). No CSS, HTML, JSON, JavaScript, React, Angular, Vue, spinner implementation, skeleton-loader implementation, progress-bar implementation, animation library, or rendering-engine content appears anywhere above. The constitutional dependency chain remains intact — loading treatment consumes governed tokens exclusively (`DS-001-339`), never an independent visual path. The chapter's scope was verified against the frozen Document Architecture before drafting, per the process note at the top of this chapter, and no subsection or title deviates from that verification.

*End of Chapter 20.*

---

## SECTION 21: Notification Styling

*A verification note before proceeding:* this chapter's title and scope were verified against the frozen Document Architecture before drafting. No subsections are frozen. The Ownership Matrix notes this topic is "Not addressed in SD-001" — unusual among this document's chapters. Chapter 15 forward-references this chapter directly (`§15.3`: "realized in full by Chapter 21"), and Chapter 13's frozen catalogue already names Notification/Toast as a component. No competing brief was supplied.

**This chapter is primarily new**, not integrative. There is no SD-001 mandate to render here, unlike most prior chapters. The one integration duty is completing Chapter 15's deferred Notification Motion specification; the severity taxonomy, three-element composition, and calm-notification discipline below are new constitutional territory, marked `[New]` throughout. Chapters 6, 14, 17, 19, and 20 are cross-referenced where relevant, never restated.

### 21.1 Purpose

*[New.]* A notification exists to tell a user something happened, why it matters to their business responsibility, and what — if anything — they should do next. Because no SD-001 mandate governs this territory, this chapter carries full constitutional weight for defining what a notification communicates and how, subject only to the general principles Chapters 3 and 6 already establish (calm by default, semantic colour discipline) and the motion category Chapter 15 already named.

### 21.2 Notification Philosophy

**DS-001-345: Notifications Communicate Significance, Not Just Occurrence**
*[New.]* A notification exists because something occurred that carries business significance to the user receiving it — not because the system wants to report every event it is capable of reporting. An occurrence with no business significance to the recipient does not warrant a notification.

**DS-001-346: Notifications Communicate Actionability**
*[New.]* Where a notification implies a user response is available or required, that response is stated, not implied. A notification that reports an outcome with no indication of whether or how to respond leaves the user to guess.

**DS-001-347: Notifications Never Exaggerate Urgency**
*[New.]* A notification's visual intensity reflects the actual business significance of what occurred, never an inflated significance intended to guarantee attention. This is `DS-001-016` (Calm by Default, Loud by Exception, Chapter 3) applied specifically to notifications: urgency is earned by the event, never manufactured by the notification's own styling.

**DS-001-348: Notifications Never Create Ambiguity**
*[New.]* A notification states plainly what happened; it never requires the user to infer meaning from tone, colour, or icon alone. This is `DS-001-058` (Colour Never Replaces Information, Chapter 6) applied to notifications.

**DS-001-349: Notifications Never Become Visual Overload**
*[New.]* Multiple simultaneous notifications are governed, prioritized, and never permitted to accumulate into a visual field a user cannot parse. This extends `DS-001-043`'s Action Center discipline (SD-001, seven-item cap) to notification volume specifically: an unbounded stack of notifications is as much a failure of restraint as an unbounded action list.

### 21.3 Notification Severity Architecture

*[New.]* Notification severity realizes Chapter 6's existing Semantic Status Colours family (§6.3) directly — it does not introduce a parallel severity scale.

| Severity | Realizes | Purpose |
|---|---|---|
| Success | Semantic Status Colours — success | Confirms a user action or system process completed as intended. |
| Informational | Semantic Status Colours — info | Communicates a neutral, non-evaluative occurrence worth the user's awareness. |
| Warning | Semantic Status Colours — warning | Communicates an occurrence requiring attention before it becomes a problem. |
| Danger | Semantic Status Colours — danger | Communicates a failure or a condition requiring prompt user response. |

**DS-001-350: The Notification Severity Taxonomy Realizes Chapter 6's Semantic Status Colours, It Does Not Add a Fifth**
No notification severity exists outside the four Semantic Status Colours already establish (Chapter 6, §6.3). A future need that appears to require a new severity is resolved by proposing an extension to Chapter 6's closed colour-family set through constitutional review, never by inventing a notification-specific severity outside it. This is `DS-001-064` (One Family Per Concept, Chapter 6) applied to notification severity.

### 21.4 Notification Composition

*[New — no prior chapter defines Notification's structural composition.]* A notification is composed of three constitutional elements, corresponding to the three questions `DS-001-345`–`346` establish it must answer.

| Element | Answers | Composed From |
|---|---|---|
| What Happened | The occurrence itself, stated plainly. | Notification Severity (§21.3); Content Colours, Typography (Chapter 6, §6.3; Chapter 7, Operational Reading) |
| Why It Matters | The business significance to the recipient. | Typography (Chapter 7, Analytical or Operational Reading, matching the recipient's context) |
| What Happens Next | The available or required response, if any. | Action Icons (Chapter 8, §8.3), where a response is available |

**DS-001-351: Notification Composition Is a Closed, Three-Element Structure**
No notification renders outside the three elements above, though "Why It Matters" or "What Happens Next" may be omitted where genuinely inapplicable (a purely informational notification with no required response omits the third element rather than fabricating one). A future need that appears to require a fourth element is resolved through constitutional review (§21.10), never by an ad hoc addition. This is `DS-001-027` (Extend, Never Fork) applied to Notification Styling.

### 21.5 Calm Notification Discipline

**DS-001-352: Notification Intensity Is Proportionate to Business Significance, Never to System Convenience**
*[New.]* A notification's visual weight — size, colour saturation, persistence, and motion — scales with the business significance of what occurred (§21.3), never with how convenient a given intensity is for the system raising it. A background synchronization completing on schedule does not warrant the same visual weight as a governance approval requiring response, regardless of how technically significant either event is to the system internally.

**DS-001-352A: Notifications Shall Preserve Attention Integrity**
*[New.]* *Statement.* Notifications SHALL compete for user attention only to the extent justified by their Business Significance. Notifications SHALL NEVER interrupt Enterprise Intelligence work without constitutional justification.
*Architectural Rationale.* Enterprise users operate within complex decision-making contexts. Every unnecessary interruption increases cognitive load and reduces decision quality. Attention is therefore a governed enterprise resource. Notification Styling exists to protect that resource, not consume it. This principle extends `DS-001-347` (Notifications Never Exaggerate Urgency) and `DS-001-349` (Notifications Never Become Visual Overload) into attention management: those two principles govern a single notification's intensity and a notification stack's volume respectively; this principle governs the resource both exist to protect — the user's capacity to continue the Enterprise Intelligence work a notification interrupted.
*Practical Implications.* Notifications MAY request attention. Notifications SHALL NOT demand attention without proportional Business Significance (§21.3). Multiple notifications SHALL preserve the user's ability to continue meaningful work — consistent with `DS-001-349`'s governed-volume discipline, now stated as an attention-preservation outcome rather than only a visual-density rule. Enterprise Intelligence SHALL remain the user's primary focus; a notification's composition (§21.4) is evaluated by whether it can be acknowledged without abandoning that focus, not only by whether it is visually legible.

### 21.6 Preserving Enterprise Intelligence

**DS-001-353: A Notification Referencing Enterprise Intelligence Content Preserves Its Chapter 14 Standard**
*[New.]* Where a notification references Evidence, Confidence, AI-Generated Content, a Recommendation, or any other Enterprise Intelligence concept (Chapter 14), it uses that concept's own colour, icon, and typographic treatment (§14.1–14.11) within the notification's composition (§21.4) — never a generic notification treatment that strips the concept of its Chapter 14 visual identity. A notification announcing a new AI-generated recommendation carries the same AI provenance and Decision Support treatment that recommendation would carry anywhere else in the platform.

### 21.7 Relationship with Motion

**DS-001-354: Notification Motion Is Fully Specified Here, Completing Chapter 15's Forward Reference**
Chapter 15's Notification Motion category (`§15.3`) is fully realized by this chapter: a notification's appearance and dismissal draw on Motion and Transition Tokens (Chapter 10, §10.3) exactly as Chapter 15 governs, calibrated to the severity-proportionate intensity `DS-001-352` establishes. This chapter and Chapter 15 do not duplicate one another: Chapter 15 establishes that notification motion communicates rather than decorates; this chapter establishes what a notification actually is and when it appears.

### 21.8 Relationship with Design Tokens

**DS-001-355: Notification Styling Is Resolved Only Through Governed Tokens**
*[New, following the established pattern.]* Implementations SHALL consume notification styling (§21.3–21.4) exclusively through governed Semantic Status Colours, Typography, Icon, and Motion Tokens (Chapter 10). No implementation, capability, or extension shall hard-code a notification-specific value outside that system. This is `DS-001-015` (One Token, Every Surface, Chapter 3) applied specifically to Notification Styling.

### 21.9 Accessibility

**DS-001-356: Notification Appearance Is Announced to Assistive Technology Without Interrupting Current Focus**
*[New.]* A notification's appearance is perceivable to assistive technology at the moment it occurs, without forcibly relocating a screen reader user's focus away from the task they were already engaged in — satisfying the Legibility Standard (Chapter 17, §17.3) and SD-001's screen-reader compatibility mandate (`SD-001-061`) without the disorientation an interrupted focus would cause.

### 21.10 Governance

**DS-001-357: Notification Styling Evolves Rarely and Constitutionally**
The Notification Severity Architecture (§21.3) and Composition (§21.4) change rarely, and only through the same constitutional review discipline as any other change to this document.

**DS-001-358: Capability Teams Shall Not Introduce Notification Systems**
Consistent with the equivalent principles in Chapters 6 through 20, a capability or Business Activity team has no authority to introduce a notification severity outside §21.3's four or a composition outside §21.4's three elements. A capability that requires notification support this chapter does not yet provide proposes an extension through the Design Governance contribution process (Chapter 22 §22.4).

**DS-001-359: White-Label Branding Shall Not Redefine Notification Severity**
A tenant's or partner's white-label configuration (Chapter 12) may vary notification's token-resolved appearance; it shall never redefine which severity a notification carries or what that severity means. This is `DS-001-076` (Chapter 6) applied to Notification Styling.

**DS-001-360: Marketing Shall Never Affect Product Notification Styling**
A marketing or campaign use of a notification-like treatment, however it is applied outside the product surface, shall never cause a product notification's severity or composition to be reinterpreted. This is `DS-001-037` (Chapter 4) applied specifically to Notification Styling.

---

### Chapter 21 Validation

This chapter is explicitly identified as primarily new (opening note): unlike most prior chapters, no SD-001 mandate exists for this territory, so this chapter originates its severity taxonomy (§21.3, `DS-001-350`) and three-element composition (§21.4, `DS-001-351`) as new constitutional principles, marked `[New]` throughout, while completing only Chapter 15's `§15.3` forward reference to Notification Motion (`DS-001-354`) without restating it. Notifications preserve Enterprise Trust and Enterprise Intelligence (`DS-001-353`) by name; they communicate significance (`DS-001-345`) and actionability (`DS-001-346`); they never exaggerate urgency (`DS-001-347`) or become visual noise (`DS-001-349`, `DS-001-352`). `DS-001-352A` unifies `DS-001-347` and `DS-001-349` into an explicit attention-preservation guarantee — Enterprise Intelligence work remains the user's primary focus, and notification volume is evaluated by whether it can be acknowledged without abandoning that focus — without restating either source principle or overlapping Chapter 20's loading-experience territory. No toast, snackbar, email, or push-notification implementation, CSS, HTML, JSON, JavaScript, React, Vue, Angular, or framework-specific content appears anywhere above. The constitutional dependency chain remains intact — notification styling consumes governed tokens exclusively (`DS-001-355`), never an independent visual path. The chapter's scope was verified against the frozen Document Architecture before drafting, per the process note at the top of this chapter, and no subsection or title deviates from that verification.

*End of Chapter 21.*

---

## SECTION 22: Design Governance

*Status: COMPLETE. This chapter was authored in dependency order, not reading order — the authoring sequence was §22.5 → §22.1 → §22.4 → §22.2 → §22.3 → §22.6 → §22.7 → §22.8 → §22.9 → §22.10, because every constitutional review this chapter defines depends on the authority §22.5 establishes. The chapter reads 22.1 through 22.10, per the frozen Document Architecture. All ten subsections are authored and frozen; no further Chapter 22 authoring remains.*

This chapter governs the lifecycle, evolution, and constitutional integrity of the entire AUREX Design System — how a change to any token, theme, brand resolution, component, or domain visual standard this document defines is proposed, reviewed, approved, versioned, released, and, where necessary, deprecated.

**The Implementation Boundary.** DS-001 governs constitutional design principles only. It defines meaning, tokens, themes, brand resolution, components, and the governance of how all of these evolve. It does not govern implementation. Implementation belongs to implementation specifications and engineering documents — IMP-001 (Implementation Playbook) and Master Technical Architecture, per ARCH-000's Layer 3 classification — and the implementation repositories every prior chapter has consistently deferred to. Every process this chapter defines governs the specification DS-001 approves, never its build. This boundary is restated here, prominently, because Chapter 22 is the one place in this document where a governance process could otherwise be mistaken for an implementation process.

**The Constitutional Sequence.** This chapter's ten subsections realize one continuous narrative:

Authority → Approval → Review → Change Control → Versioning → Exception Process → Constitutional Change Lifecycle → Cross-document Synchronization → Release Governance → Compliance & Audit → Continuous Improvement

| Sequence Beat | Realized By |
|---|---|
| Authority | §22.5 |
| Approval | §22.5 |
| Review | §22.1 |
| Change Control | §22.2, §22.3, §22.4 |
| Versioning | §22.6 |
| Exception Process | §22.5 |
| Constitutional Change Lifecycle | This chapter-level framing |
| Cross-document Synchronization | §22.8 |
| Release Governance | §22.10 |
| Compliance & Audit | §22.6, §22.7, §22.9, §22.10 jointly |
| Continuous Improvement | No subsection — the outcome of the Lifecycle and §22.10 operating correctly, not a process requiring separate governance |

**The Constitutional Change Lifecycle.** Every constitutional change to this document follows: Proposal (§22.4) → Impact Analysis (§22.2/§22.3 + §22.8) → Architectural Review (§22.1) → Constitutional Approval (§22.5) → *Implementation, outside DS-001's scope, per the Implementation Boundary above* → Verification (§22.1 + §22.10) → Cross-document Synchronization (§22.8) → Release (§22.10) → Audit (§22.6) → Archive (§22.7).

### 22.1 Design Review Process

**This section owns:** Constitutional Design Review; Review Principles; Review Criteria; Review Inputs; Review Outputs; Architectural Conformance Verification.
**This section does not own:** Approval Authority and Approval Outcomes (§22.5); Versioning (§22.6); Contribution Workflow (§22.4); Release Governance (§22.10); Compatibility (§22.8); Deprecation (§22.7); Implementation (outside DS-001's scope entirely, per the Implementation Boundary this chapter opens with). Each is cross-referenced below, never restated.

**Constitutional Design Review**

**DS-001-376: Review Verifies Conformance, It Does Not Originate Meaning**
*Statement.* Constitutional Design Review is the process by which a proposed change is checked against this document's existing principles, tokens, themes, and closed systems. Review does not create meaning, does not decide whether a proposal is approved, and does not itself constitute constitutional authority.
*Architectural Rationale.* This is the process-level restatement of `DS-001-159` (Tokens Represent Meaning, Chapter 10) and `DS-001-165` (Tokens Realize, They Do Not Redefine, Chapters 5 Through 9), extended to the review process itself: a process this late in the constitutional chain has no more authority to originate meaning than a token or theme does. Review is diagnostic, not generative.
*Practical Implications.* A reviewer who finds a proposal lacking does not amend it into conformance during review — the proposal is returned to its proposer (§22.4) for revision, or to the reviewing authority (§22.5, `DS-001-361`) for a Rejection or Exception determination. Review reports what is true of a proposal's conformance; it does not make the proposal conformant by rewriting it.

**DS-001-377: Review Elaborates, Rather Than Restates, the Scope §22.5 Establishes**
`DS-001-364` (§22.5) already establishes, at the constitutional level, that review evaluates conformance, consistency, adherence to principles, and compliance with closed systems — and does not evaluate artistic preference, implementation quality, coding approach, subjective design taste, or implementation aesthetics. This section elaborates that scope into the specific, closed set of criteria (below) a reviewer actually applies; it does not restate or narrow `DS-001-364`'s exclusions, which remain governed entirely by §22.5.

**Review Principles**

**DS-001-378: Review Is Applied Uniformly Regardless of Proposal Source**
The same review criteria (below) apply whether a proposal originates from a capability team, a white-label implementation request, or an internally identified gap in this document's own coverage. No proposal source receives a lighter or heavier review than another.

**Review Criteria**

Every constitutional review evaluates a proposal against the following eleven criteria.

| Criterion | What It Verifies | Owning Chapter(s) |
|---|---|---|
| DS-001 Design Principles | The proposal conforms to the fifteen Canonical Design Principles. | Chapter 3 |
| One Visual Language | The proposal does not fragment AUREX into a parallel or capability-specific system. | `DS-001-014`, Chapter 3 |
| Semantic Consistency | The proposal's meaning is identical everywhere it would apply. | `DS-001-063` and its chapter-specific restatements |
| Closed Systems | The proposal respects the closed-set boundary of whichever family it touches. | Chapters 5–21, each chapter's own closed-set principle |
| Token Architecture | The proposal resolves only through governed Design Tokens. | Chapter 10 |
| Theme Architecture | The proposal resolves appearance without originating meaning. | Chapter 11 |
| Brand Architecture | The proposal respects the four-tier brand model and never alters behaviour. | Chapter 4, Chapter 12 |
| Component Architecture | The proposal belongs to the Design System, never a capability. | Chapter 13, `DS-001-230A` |
| Ownership Boundaries | The proposal does not cross into SD-001, SD-002, or ERG-001's territory. | Chapter 2, Ownership Matrix |
| Cross-document Consistency | The proposal remains consistent with what SD-001, SD-002, and ARCH-000 currently state. | §22.8 (Compatibility Policy) |
| Architectural Traceability | The proposal cites the SD-001 or DS-001 principle it renders, or is marked visual-only. | Chapter 2, `DS-001-009` |

**DS-001-379: The Constitutional Review Criteria Are a Closed, Named Set of Eleven**
*Statement.* Every constitutional review evaluates a proposal against exactly the eleven criteria above. No review applies a twelfth, unnamed criterion, and no review omits one of the eleven.
*Architectural Rationale.* An open-ended or reviewer-discretionary criteria set would reintroduce, at the review layer, exactly the risk `DS-001-368A` (§22.5) forecloses at the approval layer — a proposal's fate depending on which reviewer happened to conduct the review, rather than on this document's own architecture. Closing the criteria set to eleven, each traceable to a specific chapter, keeps review as deterministic as the closed sets it checks.
*Practical Implications.* A future need that appears to require a twelfth review criterion is resolved by proposing an extension to this closed set through the same constitutional review discipline every other closed set in this document requires (`DS-001-027`, Extend, Never Fork) — never by a reviewer applying an ad hoc twelfth criterion informally.

**DS-001-380: Every Criterion Is Independently Verified; None Is Weighted Against Another**
A proposal is not approved on review because it satisfies most of the eleven criteria, or because its strength on one criterion offsets a weakness on another. Each of the eleven is verified independently, with an independent result.

**DS-001-381: A Single Criterion Failure Is Sufficient to Determine Non-Conformance**
A proposal that fails any one of the eleven criteria is non-conformant, regardless of how fully it satisfies the remaining ten. This is the review-level consequence of `DS-001-380`: independent verification without weighting means a single failure cannot be outweighed by strength elsewhere.

**Review Inputs**

**DS-001-382: A Reviewable Proposal Contains a Complete Constitutional Record**
*Statement.* Constitutional Design Review begins only once a proposal states what is being proposed, which of the eleven criteria it has been checked against by its proposer, and which existing chapter, principle, or closed system it touches or extends. A proposal lacking this record is not yet reviewable.
*Architectural Rationale.* This section owns Review Inputs but not the Contribution Workflow that produces them (§22.4) — this principle states only the minimum completeness a submission must have before review can begin, without prescribing how that submission is made, tracked, or routed, which remains §22.4's exclusive territory.
*Practical Implications.* An incomplete proposal is not reviewed and rejected on its merits — it is returned as incomplete, distinct from a Rejection outcome (`DS-001-365`, §22.5), because it was never evaluated against the eleven criteria in the first place.

**Review Outputs**

**DS-001-383: Review Produces a Conformance Determination, Not an Approval Outcome**
*Statement.* The output of Constitutional Design Review is a conformance determination — a statement of which of the eleven criteria the proposal satisfies and which, if any, it fails. Review does not itself produce an Approval, Exception, or Rejection; those three outcomes belong exclusively to the constitutional authority §22.5 establishes (`DS-001-361`, `DS-001-365`).
*Architectural Rationale.* Collapsing review and approval into a single act would violate the ownership boundary this chapter's architecture fixes at its outset: §22.1 owns review, §22.5 owns approval, and the Authority → Approval → Review beat of the Constitutional Sequence depends on review remaining a distinct, prior step feeding an authority that is not itself the reviewer.
*Practical Implications.* A conformance determination of "fails Ownership Boundaries," for instance, does not itself reject the proposal — it is the evidence the constitutional authority (§22.5) considers when reaching a Rejection, Exception, or, where the failure is resolved through revision, an eventual Approval.

**Architectural Conformance Verification**

**DS-001-384: Conformance Verification Is Repeatable and Traceable**
A conformance determination reached for a given proposal, against the same eleven criteria, produces the same result regardless of who conducts the verification or when — consistent with `DS-001-374`'s (§22.5) traceability guarantee for constitutional decisions generally, extended here to the review evidence that precedes those decisions. A conformance determination that could not be independently reproduced would undermine the record §22.5's approval outcomes depend on.

---

### §22.1 Validation

§22.1 owns review only: Constitutional Design Review, Review Principles, Review Criteria, Review Inputs, Review Outputs, and Architectural Conformance Verification are its complete scope, stated explicitly at this section's opening. §22.5 owns approval: every reference to an Approval, Exception, or Rejection outcome above (`DS-001-383`) points to §22.5 rather than asserting the outcome here, and `DS-001-377` explicitly declines to restate or narrow `DS-001-364`'s already-established scope, elaborating it instead. No implementation guidance appears anywhere above — no code review, UX review, Figma review, sprint review, engineering review, pull request, Git, Jira, or CI/CD process is named or implied; the eleven review criteria are stated entirely at the constitutional specification level. No organizational structure is introduced — this section states what is verified and how, never who sits on a team or how a meeting is run. No overlap exists with Versioning (§22.6), Contribution Workflow (§22.4, cross-referenced by `DS-001-382` without restating it), Release Governance (§22.10), Compatibility (§22.8, cross-referenced by the Cross-document Consistency criterion without restating it), or Deprecation (§22.7). Constitutional review evaluates architectural conformance only: the eleven criteria table names exactly what is checked, and `DS-001-379`'s closed-set discipline forecloses any criterion — including artistic taste or implementation quality — being applied outside that named set.

*§22.1 complete and frozen. Chapter 22 is complete; no further Chapter 22 authoring remains.*

### 22.2 Token Governance

**This section owns:** Design Token Governance; Token Lifecycle Governance; Token Classification Governance; Token Evolution Rules; Token Extension Rules; Token Integrity; Token Consistency; Token Registry Governance.
**This section does not own:** Constitutional Review (§22.1); Approval Authority and Outcomes (§22.5); Component Governance (§22.3); Contribution Workflow (§22.4); Versioning (§22.6); Deprecation (§22.7); Compatibility (§22.8); Migration (§22.9); Release Management (§22.10); Implementation (outside DS-001's scope entirely, per the Implementation Boundary this chapter opens with). Each is cross-referenced below, never restated.

**Design Token Governance**

**DS-001-385: This Section Governs Token Evolution, Not Token Definition**
*Statement.* §22.2 governs how the token system Chapter 10 defines evolves over time — extension, classification enforcement, lifecycle, integrity, and registry maintenance. It does not define what a token is, what the twenty-three atomic families or six Compositional Token Groupings are, or what any token means.
*Architectural Rationale.* This is the token-specific instance of the ownership discipline this chapter has followed since §22.1: a governance section this far downstream in the constitutional chain has no authority to originate or redefine the meaning Chapter 10 already established (`DS-001-159`, `DS-001-165`). §22.2 exists because a closed system, once defined, still needs a governed process for how it grows — not because Chapter 10's definition was incomplete.
*Practical Implications.* A reader looking for what "Colour Tokens" or "Evidence Tokens" means finds that answer in Chapter 10, never here. A reader looking for how a twenty-fourth atomic family would be proposed, evaluated, and integrated into the registry finds that answer here.

**DS-001-386: Token Governance Reinforces, It Does Not Redefine, Chapters 10 Through 12**
Every principle in this section presupposes, and does not restate, the architecture Chapter 10 (Design Token System), Chapter 11 (Theme System), and Chapter 12 (White-Label Branding & Multi-Brand Token Mapping) already establish: the closed twenty-three-family atomic set (`DS-001-157`), the six Compositional Token Groupings (`DS-001-158`), themes resolving rather than originating token meaning (`DS-001-164`, `DS-001-166`), and brand resolution consuming rather than originating tokens (`DS-001-211`, `DS-001-222`). Where a principle below appears to overlap one of these, the earlier chapter's principle governs; this section only adds the evolution and integrity discipline those chapters do not themselves state.

**Token Classification Governance**

**DS-001-387: Atomic and Compositional Classification Is Fixed at Approval and Never Reassigned Retroactively**
*Statement.* Whether a proposed token is classified as an atomic family member (extending Chapter 10's twenty-three) or a Compositional Token Grouping (extending Chapter 10's six) is determined at the point of constitutional approval (§22.5) and does not change afterward. A token approved as compositional is never later reclassified as atomic, or the reverse, without being retired and reproposed under the new classification.
*Architectural Rationale.* `DS-001-158` (Chapter 10) already distinguishes atomic families from Compositional Token Groupings by what they are — atomic families are visual substances, compositional groupings are named combinations of them. Allowing a token's classification to drift after approval would let a governance decision quietly change what kind of thing a token is, without the constitutional review (§22.1) or approval (§22.5) that classification decision originally required.
*Practical Implications.* A proposal that appears compositional at submission but is later found to actually require new atomic content is not silently upgraded — it is returned through the review process (§22.1) as a new, differently classified proposal, subject to the heavier atomic-family review tier `DS-001-173` (Chapter 10) already establishes.

**Token Lifecycle Governance**

**DS-001-388: Every Token Has a Governed Lifecycle From Proposal to Retirement**
*Statement.* A token's constitutional existence proceeds through named lifecycle stages: Proposed (submitted per §22.4), Under Review (§22.1), Approved or granted as an Exception (§22.5), Active (in governed use), and, where applicable, Deprecated and Retired (§22.7). No token exists in this document outside one of these stages at any time.
*Architectural Rationale.* Chapter 10 defines what tokens are; it does not state that a token's existence is itself a governed, staged process rather than a fact fixed permanently at authoring time. This principle closes that gap, consistent with `SD-002-010`'s (Universal Versioning) precedent that every governed object supports full historical, stage-aware tracking.
*Practical Implications.* This section states that the lifecycle exists and what its stages are named; it does not itself define how a token moves between Approved and Exception status (§22.5), how it is deprecated (§22.7), or how a version of it is recorded (§22.6) — each transition is governed by its owning section, cross-referenced rather than restated here.

**DS-001-389: A Token's Current Lifecycle Stage Is Always Determinable**
A governed token's current stage (`DS-001-388`) is never ambiguous or undocumented — it is always resolvable from the Token Registry (below). A token with no determinable lifecycle stage is not a governed token.

**Token Evolution & Extension Rules**

**DS-001-390: Atomic Family Extension and Compositional Grouping Extension Are Governed as Distinct Weight Classes**
This restates, as this section's own governing rule, the distinction Chapter 10 already draws — `DS-001-173` requiring constitutional review "of the frozen scaffold itself" for a new atomic family, against `DS-001-158`'s lighter-weight treatment for a new Compositional Token Grouping: the eleven review criteria §22.1 applies are the same for both, but the Token Architecture criterion is evaluated more strictly for a proposal touching the frozen twenty-three than for one proposing a new combination of them.

**DS-001-391: Token Extension Never Fragments the One Token System**
Every extension to the token system — atomic or compositional — remains within Chapter 10's single, closed architecture. This is `DS-001-027` (Extend, Never Fork, Chapter 3) applied specifically to token governance: an extension that behaved as a parallel or capability-specific token mechanism, however small, would not be an extension at all but a fork, regardless of how it was justified.

**Token Integrity**

**DS-001-392: No Two Governed Tokens May Share One Semantic Meaning**
*Statement.* Once a token is approved for a given semantic meaning, no second token — atomic or compositional — may be approved for that same meaning. A proposal that would duplicate an existing token's meaning is non-conformant under the Semantic Consistency criterion (§22.1) regardless of what family or grouping it is proposed under.
*Architectural Rationale.* This is the governance-enforcement mechanism for `DS-001-161` (One Token Per Semantic Concept, Chapter 10): Chapter 10 states the principle; this section states how review and the registry (below) actually keep it true as the token system grows over time, rather than only at the moment Chapter 10 was authored.
*Practical Implications.* A proposal that appears to need "another Evidence Colour" for a subtly different purpose is resolved by determining whether the purpose is actually a new semantic concept (warranting a genuinely new token) or a variant of an existing one (warranting reuse of the existing token, not a duplicate).

**DS-001-393: A Token Carries Exactly One Semantic Meaning, Never Several**
The inverse of `DS-001-392`: a single token is never approved to carry two unrelated meanings depending on context. Where two genuinely distinct meanings would otherwise share one token, they are proposed and governed as two separate tokens instead.

**Token Consistency**

**DS-001-394: Cross-Theme, Cross-Brand, and Cross-Platform Consistency Are Verified at Every Lifecycle Stage, Not Only at Approval**
*Statement.* A token's consistency across every theme (Chapter 11), every brand resolution (Chapter 12), and every implementation platform (`DS-001-153`–`154`, Chapter 10) is verified not only when the token is first approved, but at every subsequent lifecycle stage (`DS-001-388`) — including when the theme system itself changes, when a new brand tier variant is added, or when the token's Active status is reaffirmed.
*Architectural Rationale.* A token that was cross-theme and cross-brand consistent at approval can drift out of consistency if a later, unrelated change to Chapter 11 or Chapter 12 is not checked against every already-approved token — the same silent-orphaning risk this chapter's Cross-document Synchronization discipline (§22.8) exists to prevent at the document level, applied here at the token level.
*Practical Implications.* A change to Theme or Brand governance (evaluated against §22.1's Theme Architecture and Brand Architecture criteria in its own right) includes verifying that every already-Active token remains consistent under the change — not only that the change itself is internally coherent.

**Token Registry Governance**

**DS-001-395: The Token Registry Is the Single Authoritative Record of Every Governed Token**
*Statement.* Every token this document governs — every atomic family member and every Compositional Token Grouping — has exactly one record in a single Token Registry, stating its classification (`DS-001-387`), its current lifecycle stage (`DS-001-389`), and its semantic meaning (`DS-001-392`–`393`). No token exists in governed use without a corresponding registry record.
*Architectural Rationale.* This is the practical mechanism by which `DS-001-392`'s no-duplicate-meaning guarantee and `DS-001-389`'s always-determinable-stage guarantee are actually verifiable rather than aspirational — a registry is what makes "no two tokens share one meaning" a checkable fact rather than a hoped-for outcome.
*Practical Implications.* The Token Registry is a governance artifact, not an implementation asset — it records constitutional facts about tokens (classification, stage, meaning, approving authority per `DS-001-374`), never token values, file formats, or build outputs, which remain entirely outside DS-001's scope per the Implementation Boundary this chapter opens with.

**DS-001-396: No Capability-Owned Token Registry May Exist**
This restates, as this section's own governing rule, `DS-001-174`'s (Chapter 10) prohibition on capability teams introducing independent token systems, applied specifically to the registry: a capability team, white-label implementation, or marketplace extension may consume the single Token Registry (`DS-001-395`); none may maintain a parallel registry of its own tokens, however small.

---

### §22.2 Validation

Token Governance remains constitutional throughout: every principle above states a governance rule (classification permanence, lifecycle staging, extension weight class, integrity, consistency verification, registry authority), never a token value, CSS variable, JSON structure, Figma variable, implementation repository, rendering engine, token build system, Style Dictionary reference, or frontend framework. Chapters 10–12 remain the owners of Token Architecture: `DS-001-385` and `DS-001-386` state this explicitly at this section's opening, and every principle below cites rather than restates `DS-001-157`, `DS-001-158`, `DS-001-159`, `DS-001-161`, `DS-001-164`, `DS-001-166`, `DS-001-173`, `DS-001-174`, `DS-001-211`, and `DS-001-222`. §22.2 governs token evolution, not token definition, per `DS-001-385`'s explicit statement. Approval remains owned by §22.5 (`DS-001-387`, `DS-001-388` both defer the actual approval and exception mechanics rather than restating them); Review remains owned by §22.1 (`DS-001-387`, `DS-001-390` both defer to its eleven criteria rather than defining new ones). Component Governance is not duplicated — no component, only token, content appears above. Contribution Workflow is not duplicated — `DS-001-388` names Proposed as a lifecycle stage without defining how a proposal is submitted, tracked, or routed. Versioning is not duplicated — `DS-001-388` names lifecycle stages without defining how a version number or history record is produced, deferring that to §22.6. Closed token families remain constitutionally protected: `DS-001-387` fixes classification permanently at approval, and `DS-001-390`–`391` ensure extension never fragments the single closed system. No independent token systems can emerge: `DS-001-391` and `DS-001-396` jointly foreclose both a parallel token mechanism and a parallel registry, extending `DS-001-174`'s (Chapter 10) prohibition into an enforceable, registry-backed governance discipline.

*§22.2 complete and frozen. Chapter 22 is complete; no further Chapter 22 authoring remains.*

### 22.3 Component Governance

**This section owns:** Component Governance; Component Lifecycle Governance; Component Classification Governance; Component Evolution Rules; Component Extension Rules; Component Integrity; Component Registry Governance; Component Dependency Governance.
**This section does not own:** Constitutional Review (§22.1); Approval Authority and Outcomes (§22.5); Token Governance (§22.2); Contribution Workflow (§22.4); Versioning (§22.6); Deprecation (§22.7); Compatibility (§22.8); Migration (§22.9); Release Management (§22.10); Implementation (outside DS-001's scope entirely, per the Implementation Boundary this chapter opens with). Each is cross-referenced below, never restated.

**Component Governance**

**DS-001-397: This Section Governs Component Evolution, Not Component Definition**
*Statement.* §22.3 governs how the component system Chapter 13 defines evolves over time — extension, classification enforcement, lifecycle, integrity, dependency protection, and registry maintenance. It does not define what a component is, what the nine frozen categories or the Primitive/Composite structure are, or what any component's visual standard consists of.
*Architectural Rationale.* This is the component-specific instance of the same ownership discipline §22.2 already applies to tokens: a governance section this far downstream in the constitutional chain has no authority to originate or redefine the architecture Chapter 13 already established (`DS-001-223`, `DS-001-224`). §22.3 exists because a closed taxonomy, once defined, still needs a governed process for how it grows — not because Chapter 13's definition was incomplete.
*Practical Implications.* A reader looking for what a Confidence Indicator or a Business Activity Card is finds that answer in Chapter 13, never here. A reader looking for how a tenth component category would be proposed, evaluated, and integrated into the registry finds that answer here.

**DS-001-398: Component Governance Reinforces, It Does Not Redefine, Chapter 13**
Every principle in this section presupposes, and does not restate, the architecture Chapter 13 already establishes: the closed nine-category Component Catalogue and its Primitive/Composite structure (`DS-001-229`), components consuming meaning rather than creating it (`DS-001-223`, `DS-001-224`), components consuming Brand Resolution, the Theme System, and Design Tokens without exception (`DS-001-230`), and components never belonging to a Capability (`DS-001-230A`). Where a principle below appears to overlap one of these, the earlier chapter's principle governs; this section only adds the evolution, integrity, and dependency discipline Chapter 13 does not itself state.

**Component Classification Governance**

**DS-001-399: Primitive and Composite Classification Is Fixed at Approval and Never Reassigned Retroactively**
*Statement.* Whether a proposed component is classified as a Primitive (extending Chapter 13's Foundation Components) or a Composite (extending one of the other eight frozen categories) is determined at the point of constitutional approval (§22.5) and does not change afterward. A component approved as Composite is never later reclassified as Primitive, or the reverse, without being retired and reproposed under the new classification.
*Architectural Rationale.* This is the component-level restatement of `DS-001-387` (§22.2), applying the same classification-permanence discipline Token Governance already establishes to the Primitive/Composite structure `DS-001-229` (Chapter 13) defines. Allowing a component's classification to drift after approval would let a governance decision quietly change what kind of thing a component is, without the constitutional review (§22.1) or approval (§22.5) that classification decision originally required.
*Practical Implications.* A proposal that appears Composite at submission but is later found to actually require new Primitive content is not silently upgraded — it is returned through the review process (§22.1) as a new, differently classified proposal.

**Component Lifecycle Governance**

**DS-001-400: Every Component Has a Governed Lifecycle From Proposal to Retirement**
A component's constitutional existence proceeds through named lifecycle stages: Proposed (submitted per §22.4), Under Review (§22.1), Approved or granted as an Exception (§22.5), Active (in governed use), and, where applicable, Deprecated and Retired (§22.7). No component exists in this document outside one of these stages at any time. This mirrors `DS-001-388`'s (§22.2) token lifecycle exactly, applied to components; each transition is governed by its owning section, cross-referenced rather than restated here.

**DS-001-401: A Component's Current Lifecycle Stage Is Always Determinable**
A governed component's current stage (`DS-001-400`) is never ambiguous or undocumented — it is always resolvable from the Component Registry (below). A component with no determinable lifecycle stage is not a governed component.

**Component Evolution & Extension Rules**

**DS-001-402: New Component Categories and New Composites Within Existing Categories Are Governed as Distinct Weight Classes**
This restates, as this section's own governing rule, the distinction Chapter 13 already draws — `DS-001-233` requiring constitutional review "of both this chapter and the frozen Document Architecture's Component Catalogue" for a new component category, against a lighter-weight review for a new Composite assembled from existing Primitives within an already-frozen category: the eleven review criteria §22.1 applies are the same for both, but the Component Architecture criterion is evaluated more strictly for a proposal touching the frozen nine-category set than for one composing existing Primitives into a new Composite.

**DS-001-403: Component Extension Never Fragments the One Component System**
Every extension to the component system — new category or new Composite — remains within Chapter 13's single, closed taxonomy. This is `DS-001-027` (Extend, Never Fork, Chapter 3) applied specifically to component governance, mirroring `DS-001-391`'s (§22.2) treatment of tokens: an extension that behaved as a parallel or capability-specific component mechanism, however small, would not be an extension at all but a fork.

**Component Integrity**

**DS-001-404: One Semantic Purpose Per Component**
Each governed component serves exactly one identifiable business or visual purpose. A component proposed to serve two unrelated purposes depending on context is not one component — it is two components that have not yet been separated.

**DS-001-405: No Two Components May Represent the Same Business Meaning**
*Statement.* Once a component is approved to represent a given business meaning — a Confidence Indicator representing confidence, a Business Activity Card representing a Business Activity — no second component may be approved to represent that same meaning. A proposal that would duplicate an existing component's represented meaning is non-conformant under the Semantic Consistency criterion (§22.1) regardless of what category it is proposed under.
*Architectural Rationale.* This is the component-level mirror of `DS-001-392` (§22.2): Chapter 13 establishes that components consume rather than originate meaning; this section states how review and the registry (below) actually keep one meaning mapped to one component as the system grows over time.
*Practical Implications.* A proposal for "another way to show confidence" is resolved by determining whether it is a genuinely new business meaning (warranting a new component) or a visual variant of the existing Confidence Indicator (warranting reuse, governed as a theme- or token-level variation, not a duplicate component).

**Component Composition Governance**

**DS-001-406: Component Composition Preserves Architectural Integrity**
A Composite component's composition — which Primitives and Layout Tokens it is assembled from — is itself subject to the same review criteria (§22.1) as the component's initial approval. A Composite may not be recomposed from different Primitives after approval without that recomposition passing through review again, consistent with `DS-001-399`'s classification-permanence discipline extended to composition specifically.

**DS-001-407: Components Consume Governed Design Tokens, They Never Redefine Token Meaning**
This restates, as this section's own governing rule, `DS-001-224` and `DS-001-236` (Chapter 13): a component's evolution never introduces a token-meaning change through the back door of a component update. Where a component's evolution appears to require a token's meaning to change, the change is proposed to Token Governance (§22.2) in its own right — a component proposal is never itself sufficient authority to alter what a token means.

**Component Dependency Governance**

**DS-001-408: A Component Shall Never Be Retired While Constitutional Artefacts Still Depend Upon It**
*Statement.* No component (`DS-001-400`, Retired stage) is retired while a composed Composite component, a design pattern, a template, a layout, or a documentation reference within this document still depends upon it. Retirement is withheld until every such dependency is itself resolved — either migrated to a replacement or retired alongside it.
*Architectural Rationale.* This is the component-level equivalent of the orphan-reference protection this chapter's Cross-document Synchronization discipline (§22.8) exists to prevent at the document level, and the direct sibling of `DS-001-392`'s (§22.2) token-integrity guarantee: a component retired out from under a Composite that depends on it does not remove the dependency, it silently breaks it, leaving a constitutional artefact that references something no longer governed. Retirement without dependency resolution is a hidden fork, not a clean retirement.
*Practical Implications.* The specific mechanics of how a dependent artefact is migrated away from a component being retired belong exclusively to §22.9 (Migration Guidance) — this principle states only the constitutional precondition that retirement may not proceed until that migration, or an equivalent joint retirement, is complete; it does not itself define how migration is performed.

**DS-001-409: Component Dependency Integrity Is Preserved Throughout the Lifecycle**
A component's dependency relationships — what it is composed from (`DS-001-406`) and what depends on it (`DS-001-408`) — are maintained accurately at every lifecycle stage (`DS-001-400`), not reconstructed only at the point of a proposed retirement. Dependency integrity that is verified only when needed, rather than maintained continuously, cannot reliably support `DS-001-408`'s retirement precondition.

**Component Registry Governance**

**DS-001-410: The Component Registry Is the Single Authoritative Record of Every Governed Component**
*Statement.* Every component this document governs — every Primitive and every Composite, across all nine frozen categories — has exactly one record in a single Component Registry, stating its classification (`DS-001-399`), its current lifecycle stage (`DS-001-401`), its represented business meaning (`DS-001-405`), and its dependency relationships (`DS-001-409`). No component exists in governed use without a corresponding registry record.
*Architectural Rationale.* This is the practical mechanism by which `DS-001-405`'s no-duplicate-meaning guarantee and `DS-001-408`'s retirement precondition are actually verifiable rather than aspirational — a registry is what makes "nothing depends on this component" a checkable fact rather than a hoped-for outcome.
*Practical Implications.* The Component Registry is a governance artifact, not an implementation asset — it records constitutional facts about components (classification, stage, meaning, dependencies, approving authority per `DS-001-374`), never component code, markup, or rendering output, which remain entirely outside DS-001's scope per the Implementation Boundary this chapter opens with.

**DS-001-411: No Capability-Owned Component Library May Exist**
This restates, as this section's own governing rule, `DS-001-234`'s and `DS-001-230A`'s (Chapter 13) prohibition on capability teams introducing independent component systems or claiming component ownership, applied specifically to the registry: a capability team, white-label implementation, or marketplace extension may consume the single Component Registry (`DS-001-410`); none may maintain a parallel library of its own components, however small.

**Cross-Theme, Cross-Brand & Cross-Platform Consistency**

**DS-001-412: Cross-Theme, Cross-Brand, and Cross-Platform Consistency Are Verified at Every Lifecycle Stage, Not Only at Approval**
This mirrors `DS-001-394`'s (§22.2) token-level principle exactly, applied to components: a component's consistency across every theme (Chapter 11), every brand resolution (Chapter 12), and every implementation platform is verified not only when the component is first approved, but at every subsequent lifecycle stage — including when the theme system, brand model, or an underlying token the component consumes changes.

---

### §22.3 Validation

Component Governance remains constitutional throughout: every principle above states a governance rule (classification permanence, lifecycle staging, extension weight class, integrity, composition governance, dependency protection, registry authority), never a React, Vue, or Angular component, HTML, CSS, Storybook reference, frontend repository, rendering technology, or engineering implementation detail. Chapter 13 remains the owner of Component Architecture: `DS-001-397` and `DS-001-398` state this explicitly at this section's opening, and every principle below cites rather than restates `DS-001-223`, `DS-001-224`, `DS-001-229`, `DS-001-230`, `DS-001-230A`, `DS-001-233`, `DS-001-234`, and `DS-001-236`. §22.3 governs component evolution, not component definition, per `DS-001-397`'s explicit statement. Approval remains owned by §22.5 (`DS-001-399`, `DS-001-400` both defer the actual approval and exception mechanics rather than restating them); Review remains owned by §22.1 (`DS-001-399`, `DS-001-402` both defer to its eleven criteria rather than defining new ones). Token Governance is not duplicated — `DS-001-407` cites §22.2's territory rather than restating token-meaning rules. Contribution Workflow is not duplicated — `DS-001-400` names Proposed as a lifecycle stage without defining how a proposal is submitted, tracked, or routed. Versioning is not duplicated — `DS-001-400` names lifecycle stages without defining how a version number or history record is produced, deferring that to §22.6. Component dependencies remain constitutionally protected: `DS-001-408` establishes that retirement cannot proceed while composed Components, design patterns, templates, layouts, or documentation references still depend on the component being retired, with migration mechanics explicitly deferred to §22.9 rather than defined here, and `DS-001-409` requires dependency integrity be maintained continuously, not only checked at retirement time. No independent component libraries can emerge: `DS-001-403` and `DS-001-411` jointly foreclose both a parallel component mechanism and a parallel registry, extending `DS-001-234`'s and `DS-001-230A`'s (Chapter 13) prohibitions into an enforceable, registry-backed governance discipline.

*§22.3 complete and frozen. Chapter 22 is complete; no further Chapter 22 authoring remains.*

### 22.4 Contribution Process

**This section owns:** Constitutional Contribution Process; Proposal Submission; Proposal Completeness; Proposal Classification; Proposal Routing; Proposal Traceability; Proposal Lifecycle; Proposal Withdrawal; Proposal Resubmission.
**This section does not own:** Constitutional Review (§22.1); Approval Authority and Outcomes (§22.5); Token Governance (§22.2); Component Governance (§22.3); Versioning (§22.6); Deprecation (§22.7); Compatibility (§22.8); Migration (§22.9); Release Management (§22.10); Implementation (outside DS-001's scope entirely, per the Implementation Boundary this chapter opens with). Each is cross-referenced below, never restated.

**DS-001-413: This Section Governs Proposals, Not Constitutional Change**
*Statement.* §22.4 governs how a request for constitutional consideration enters this document's governance process — its identity, completeness, classification, routing, lifecycle, withdrawal, and traceability. It does not govern whether that request is accepted, what criteria it is judged against, or what happens to the token, component, or other closed system it concerns once accepted.
*Architectural Rationale.* This is the proposal-specific instance of the ownership discipline §22.1, §22.2, and §22.3 have each already applied to their own territory: a governance section whose entire subject is the request has no authority over the decision that request produces. Roughly eighteen principles across Chapters 6 through 21 already promise that a capability requiring something this document does not yet provide "proposes an extension through the Design Governance contribution process (Chapter 22 §22.4)" — this section is where that promise is redeemed, and nowhere else.
*Practical Implications.* A reader looking for what happens to a proposal once submitted — is it accepted, on what grounds, by whom — finds that answer in §22.1 (review) and §22.5 (approval), never here. A reader looking for how a proposal is identified, completed, classified, and tracked before it reaches review finds that answer here.

**DS-001-414: A Proposal Never Modifies DS-001 Until Approved Under §22.5**
*Statement.* A proposal, at every stage of its lifecycle governed by this section, is a request for constitutional consideration. It is not itself a constitutional change, carries no constitutional authority, and does not alter any token, theme, component, or principle this document establishes — regardless of how complete, well-classified, or far advanced through this section's lifecycle it is.
*Architectural Rationale.* This is the constitutional floor this entire section rests on: if a sufficiently well-formed proposal could be treated as provisionally binding before an Approval outcome (`DS-001-365`, §22.5) is actually reached, the review (§22.1) and approval (§22.5) this chapter's Constitutional Sequence establishes as prerequisite steps would be reduced to formalities applied after the fact. A proposal's completeness is a precondition for review, never a substitute for approval.
*Practical Implications.* An implementation, capability, or white-label deployment that begins consuming a proposed — but not yet approved — token, component, or theme as though it were governed is not conforming to a proposal; it is violating the Implementation Boundary and every closed-set principle the proposal would, if approved, extend.

**Proposal Identity & Completeness**

**DS-001-415: Every Proposal Has a Unique, Permanent Identity**
A proposal is assigned an identity at submission that is never reused, reassigned, or shared with another proposal, regardless of the proposal's eventual disposition (`DS-001-421`). This is the proposal-level application of the identity-permanence discipline `DS-001-029` (Chapter 3) already establishes for principle numbers, extended here to the request that may eventually produce one.

**DS-001-416: Every Proposal Declares a Defined Scope and the Constitutional Elements It Affects**
A proposal states, at submission, precisely which token, theme, brand tier, component, or other closed-set element it proposes to extend, and precisely what it does not touch. An open-ended or unscoped proposal is not a valid submission.

**DS-001-417: Proposal Completeness Is Verified at Submission, Consistent With §22.1's Reviewability Requirement**
This section verifies, at the point of submission, the same completeness `DS-001-382` (§22.1) requires before review may begin — what is being proposed, which review criteria the proposer believes it satisfies, and which existing chapter or principle it touches or extends. §22.4 does not restate `DS-001-382`'s criteria; it is the point at which that completeness is first checked, before a proposal is classified (below) or forwarded to review at all.

**Proposal Classification & Routing**

**DS-001-418: Every Proposal Is Classified Before Review**
A proposal is classified — as token-related, component-related, or otherwise — before it reaches the review process §22.1 governs. Classification determines routing (below); it does not itself determine conformance, which remains §22.1's exclusive evaluation.

**DS-001-419: Classification Routes a Proposal to Its Owning Governance Section**
*Statement.* A classified proposal is routed to the governance section that owns the element it proposes to extend — a token or theme proposal to §22.2's evolution discipline, a component proposal to §22.3's — before, and separate from, its routing to §22.1 for review.
*Architectural Rationale.* §22.2 and §22.3 each already state that they govern evolution through the weight-class distinctions specific to tokens (`DS-001-390`) and components (`DS-001-402`) respectively. Routing at the contribution stage is what actually delivers a proposal to the correct weight-class treatment those sections define, rather than leaving that determination to happen inconsistently once review is already underway.
*Practical Implications.* A proposal misrouted at this stage — a component proposal evaluated under token governance's rules, or the reverse — is corrected before review proceeds, not discovered as a defect partway through §22.1's evaluation.

**Proposal Lifecycle**

**DS-001-420: A Proposal's Lifecycle Is Distinct From, and Precedes, a Token's or Component's Own Lifecycle**
*Statement.* A proposal's lifecycle — Submitted, Completeness-Verified, Classified, Routed, and, once review and approval conclude, Disposed (below) — is separate from the Proposed-through-Retired lifecycle `DS-001-388` (§22.2) and `DS-001-400` (§22.3) establish for an approved token or component. A proposal's lifecycle ends at disposition; a token's or component's lifecycle only begins if that disposition is Approval or Exception.
*Architectural Rationale.* Conflating the two lifecycles would obscure the exact moment `DS-001-414` fixes as constitutionally significant — the boundary between "requested" and "governed." Keeping them distinct is what makes that boundary auditable rather than a matter of interpretation.
*Practical Implications.* A proposal's own identity (`DS-001-415`) is never reused as the identity of the token or component its Approval eventually produces — the two remain permanently distinct and cross-referenced to one another, not merged into one record.

**DS-001-421: Every Proposal Reaches a Final Recorded Disposition**
A proposal does not remain indefinitely in a submitted, classified, or routed state. It reaches one of a closed set of final dispositions: Approved (per §22.5's Approval outcome), Granted as an Exception (per §22.5), Rejected (per §22.5), or Withdrawn (below, by the proposer before either). No proposal is abandoned without one of these four being recorded.

**Proposal Withdrawal & Resubmission**

**DS-001-422: A Proposal May Be Withdrawn Before Approval**
The proposer of a still-pending proposal may withdraw it at any point before a §22.5 disposition is reached. Withdrawal is a disposition in its own right (`DS-001-421`) and requires no justification beyond the proposer's own decision, distinguishing it from a Rejection, which requires the reviewing authority's stated reason (`DS-001-367`, §22.5).

**DS-001-423: A Withdrawn Proposal Never Alters Constitutional History**
A withdrawn proposal leaves no trace in this document's governed tokens, themes, components, or principles — because, per `DS-001-414`, it never altered any of them while pending. Its record (below) persists for traceability; its content does not.

**DS-001-424: A Rejected Proposal May Be Resubmitted Only as a New Proposal With Explicit Reference to the Earlier Decision**
*Statement.* A proposal that has received a Rejection disposition is not reopened or amended in place. It may be resubmitted only as a new proposal, with its own new identity (`DS-001-415`), that explicitly references the prior proposal's identity and the reason recorded for its rejection (`DS-001-367`, §22.5).
*Architectural Rationale.* Permitting a rejected proposal to be silently reopened would allow a proposer to route around an adverse constitutional determination by attrition rather than by addressing the reason for it. Requiring explicit reference to the prior rejection forces the resubmission to demonstrate — to the reviewing authority, not only to the proposer — that the original reason has actually been addressed.
*Practical Implications.* A resubmission that does not reference its predecessor's rejection reason is treated as incomplete under `DS-001-417`, not as a fresh, unrelated proposal.

**DS-001-425: Superseded Proposals Remain Historically Traceable**
Where a proposal is superseded by a later, related proposal — rather than rejected outright — both remain permanently recorded and cross-referenced to one another. Supersession is not a form of deletion; it is a recorded relationship between two distinct, individually traceable proposals.

**Proposal Traceability & Archival**

**DS-001-426: Every Proposal Is Traceable Throughout Its Entire Lifecycle**
A proposal's identity (`DS-001-415`), scope (`DS-001-416`), classification and routing (`DS-001-418`–`419`), and final disposition (`DS-001-421`) are recorded and reconstructable at any later date, regardless of that disposition — Approved, Exception, Rejected, or Withdrawn alike. This is the proposal-stage realization of the same traceability guarantee `DS-001-374` (§22.5) establishes for constitutional decisions and `DS-001-395`/`DS-001-410` (§22.2/§22.3) establish for the registries those decisions populate.

**DS-001-427: No Proposal May Become Orphaned or Untraceable**
*Statement.* A proposal SHALL NOT exist without a determinable current state, a determinable classification, and a determinable eventual disposition once one is reached. A proposal that cannot be traced to its origin, its current status, or its outcome is a defect in this section's governance, not an acceptable exception to it.
*Architectural Rationale.* This closes the same failure mode `DS-001-408` (§22.3) closes for component retirement and `DS-001-389`/`DS-001-401` (§22.2/§22.3) close for token and component lifecycle stages, applied here at the earliest possible point in the Constitutional Change Lifecycle — an untraceable proposal is a gap this chapter's entire governance discipline exists to prevent from ever opening in the first place.
*Practical Implications.* This principle is the constitutional guarantee that the eighteen "propose an extension through §22.4" citations across Chapters 6 through 21 resolve to a real, auditable process — not to a submission that could, in practice, disappear without record.

---

### §22.4 Validation

Contribution Process governs proposals only, throughout: every principle above concerns identity, completeness, classification, routing, lifecycle, withdrawal, or traceability of a request, never the criteria by which it is judged or the authority that judges it. Review remains owned by §22.1: `DS-001-417` and `DS-001-419` both cross-reference `DS-001-382`'s reviewability requirement and the eleven review criteria without restating either. Approval remains owned by §22.5: `DS-001-414` states explicitly that no proposal modifies DS-001 until an Approval outcome is reached under §22.5, and `DS-001-421`'s four final dispositions (Approved, Exception, Rejected, Withdrawn) name §22.5's outcomes by reference rather than redefining them. Token Governance is not duplicated — `DS-001-419` routes to §22.2's evolution discipline without restating `DS-001-390`'s weight-class distinction. Component Governance is not duplicated — the same principle routes to §22.3 without restating `DS-001-402`. Versioning is not duplicated — `DS-001-420` explicitly separates a proposal's own lifecycle from the token's or component's lifecycle §22.6 will version, without defining version numbers or history records here. Migration is not duplicated — no principle above defines how a dependent artefact migrates away from anything; `DS-001-408`'s (§22.3) deferral to §22.9 is cited, not reopened. No implementation guidance appears anywhere above — no issue tracker, pull request, Git workflow, Jira board, CI/CD process, or project-management procedure is named or implied; every mechanism is stated at the constitutional specification level (identity, scope, disposition) rather than the operational one. Every proposal remains traceable: `DS-001-415`, `DS-001-425`, `DS-001-426`, and `DS-001-427` jointly guarantee that no proposal — approved, exception, rejected, withdrawn, or superseded — can become orphaned or unrecoverable. No proposal modifies DS-001 without constitutional approval: `DS-001-414` states this as the section's constitutional floor, and every subsequent principle operates within that constraint without exception.

*§22.4 complete and frozen. Chapter 22 is complete; no further Chapter 22 authoring remains.*

### 22.5 Approval Workflow

*This section is the constitutional authority upon which every other governance process in this chapter depends. It is drafted first for exactly that reason, per the approved authoring sequence.*

**This section owns:** Constitutional Approval; Constitutional Review Authority; Approval Outcomes; Exception Approval.
**This section does not own:** Versioning (§22.6); Contribution Workflow (§22.4); Release Governance (§22.10); Compatibility (§22.8); Deprecation (§22.7); Implementation (outside DS-001's scope entirely, per the Implementation Boundary above). Each is cross-referenced below, never restated.

**Constitutional Review Authority**

**DS-001-361: A Named Constitutional Authority Reviews Every Proposed Change**
*Statement.* Every proposed change to this document — a new token, theme class, component category, brand tier, or any other closed set this document establishes — is reviewed by a named constitutional authority before it may be approved. No change is self-reviewing.
*Architectural Rationale.* This document has cited "constitutional review" roughly twenty times across Chapters 5 through 21 without ever naming who performs it. `SD-002-060` establishes the precedent this section follows: Global CIL changes rest with a named authority (the CorpStage Governance Board), not an unnamed process. This section does not invent a new committee or organizational structure — DS-001 defines that a named constitutional authority must exist and what it must never be (below), not the org chart that seats it, consistent with this document's constitutional-not-organizational character throughout.
*Practical Implications.* Every one of this document's "requires constitutional review" citations (Chapters 5–21) now resolves to this principle: the review is performed by the same constitutional governance authority ARCH-000 §11 and `SD-002-060` already establish for the Enterprise Operating System's other canonical documents, not a DS-001-specific body invented in isolation.

**DS-001-362: Constitutional Authority Cannot Be Delegated to Implementation Teams**
An implementation team — the engineers, designers, or contributors who build against an approved specification — has no constitutional review authority, regardless of seniority or platform expertise. This is the direct consequence of the Implementation Boundary this chapter opens with: a team whose function is to implement DS-001 cannot simultaneously hold the authority to change what DS-001 requires them to implement.

**DS-001-363: Capability Teams Cannot Approve Constitutional Changes**
This restates, as this chapter's own governing rule, the constraint every domain chapter's governance section already imposes (`DS-001-075`, `DS-001-099`, `DS-001-122`, and the equivalent principle in every chapter through Chapter 21): a capability or Business Activity team may propose a change (§22.4) but may never approve one. Proposal and approval are constitutionally separated, without exception.

**Constitutional Review Process & Approval Outcomes**

**DS-001-364: Every Constitutional Change Requires Review Before Approval**
*Statement.* No proposed change reaches an approval outcome (below) without first passing through the review process §22.1 defines. This ordering is fixed: review precedes approval, never the reverse, consistent with the Constitutional Sequence this chapter opens with. That review evaluates constitutional conformance, architectural consistency, adherence to this document's governing principles, and compliance with the closed systems Chapters 5 through 21 establish. It does not evaluate artistic preference, implementation quality, coding approach, subjective design taste, or implementation aesthetics.
*Architectural Rationale.* This is the review-process-level restatement of the Implementation Boundary this chapter opens with: the Design System governs constitutional correctness, never implementation quality, which belongs entirely to implementation specifications and engineering documents outside DS-001. A review that evaluated artistic preference or coding approach would be performing a function this document has no authority over and no basis to perform consistently — those judgments belong to the teams and documents responsible for implementation, not to the constitutional authority `DS-001-361` establishes.
*Practical Implications.* A proposal is not returned for revision because a reviewer finds it aesthetically unappealing, nor approved because a reviewer finds it well-executed — either judgment is out of scope for constitutional review. A proposal is returned or rejected only for failing conformance, consistency, adherence to principles, or compliance with a closed system; it is approved only for satisfying all four.

**DS-001-365: Every Review Concludes in One of Three Recorded Outcomes**
*Statement.* A constitutional review concludes in exactly one of three outcomes: Approval (the change is permanently accepted into this document, subject to §22.6's versioning discipline), Exception (the change is temporarily accepted, subject to this section's Exception Approval principles below), or Rejection (the change is not accepted). No fourth outcome exists, and no review may conclude without reaching one of the three.
*Architectural Rationale.* An unresolved or indefinitely pending review is functionally equivalent to a silent, undocumented exception — the exact failure mode this section's Exception Approval principles exist to prevent. Closing the outcome set to three, with no "pending indefinitely" state, forecloses that failure mode structurally.
*Practical Implications.* A proposal that cannot yet be evaluated (insufficient information, unresolved dependency) is not left open — it is Rejected with a stated reason inviting resubmission, never left in an unrecorded limbo state.

**DS-001-366: Every Approval Is Recorded**
An Approval outcome is recorded with the authority who granted it, the date, and the specific change approved, feeding directly into §22.6's versioning discipline. An unrecorded approval is not a valid approval.

**DS-001-367: Every Rejection Is Recorded**
A Rejection outcome is recorded with the authority who issued it, the date, and the stated reason. This is not a courtesy — it is what makes `DS-001-374`'s traceability guarantee (below) true of rejections as well as approvals, and what allows a resubmission to demonstrate it has addressed the original reason rather than repeating an already-rejected proposal unchanged.

**DS-001-368: Implementation Convenience Is Never Sufficient Justification**
*Statement.* A proposed change justified primarily by implementation convenience — that it would be easier to build, faster to ship, or simpler to maintain in a specific technology — does not meet the bar for constitutional approval on that basis alone.
*Architectural Rationale.* This is the approval-outcome-level enforcement of the Implementation Boundary this chapter opens with: if implementation convenience were sufficient justification, the implementation layer would be governing the specification layer in practice, regardless of what this document says in principle. Every closed set in Chapters 5 through 21 exists because meaning, not build convenience, determines what belongs in AUREX.
*Practical Implications.* A proposal citing implementation convenience is not rejected for that reason alone — the convenience may be noted — but it must independently satisfy the same architectural and design-principle criteria (§22.1) every other proposal does. Convenience alone never substitutes for that evaluation.

**DS-001-368A: Constitutional Approval Shall Never Be Determined by Consensus Alone**
*[Numbered as a lettered insertion because `DS-001-369` through `DS-001-375` are already assigned and cross-referenced elsewhere in this section, per the lettered-suffix convention this document has used consistently since Chapter 4.]*
*Statement.* A proposal does not become constitutionally valid because many contributors support it, senior stakeholders prefer it, it is popular, it is easier to implement, or it aligns with current implementation preferences. Approval SHALL be determined solely by conformance to the constitutional architecture and governing principles this document establishes.
*Architectural Rationale.* This is the consensus-specific extension of `DS-001-368` (Implementation Convenience Is Never Sufficient Justification): where that principle forecloses build-convenience as a justification, this principle forecloses popularity and stakeholder preference as one. Both share the same underlying failure mode — a proposal gaining acceptance through a route other than the constitutional evaluation `DS-001-361`'s named authority is required to perform. A design system whose closed sets (Chapters 5 through 21) could be extended by popular demand rather than architectural conformance would cease to be constitutional in substance, regardless of what this document claims of itself in principle.
*Practical Implications.* A proposal with unanimous support and a proposal with none are evaluated by the same constitutional criteria and may reach the same outcome either way — support level is not itself evidence of conformance. Where popularity and constitutional conformance align, the proposal is approved because it conforms, not because it is popular; the distinction is not merely semantic — it is what keeps `DS-001-361`'s named authority answerable to this document's principles rather than to whichever preference is most widely held at a given moment.

**Constitutional Exception Approval**

**DS-001-369: An Exception Is a Time-Bound, Not a Permanent, Approval Outcome**
An Exception is constitutionally distinct from an Approval: it grants temporary, conditional acceptance of a deviation from an existing closed set or principle, never a permanent addition to it. Where an Approval extends this document's closed sets (per Chapters 5–21's "constitutional review" provisions), an Exception permits a bounded deviation from them without extending them.

**DS-001-370: Every Exception Requires Written Justification and Architectural Impact Assessment**
*Statement.* No Exception is granted without a written justification stating why the deviation is necessary and an architectural impact assessment stating what this document's other principles, tokens, themes, or components the deviation touches.
*Architectural Rationale.* An exception granted without a stated impact assessment cannot be evaluated against the same constitutional discipline an Approval requires — it would be a lesser form of review producing a form of change with real consequences, the exact asymmetry this document's absolute "SHALL NEVER" language throughout Chapters 5–21 is designed to prevent.
*Practical Implications.* The justification and impact assessment are recorded alongside the Exception itself (`DS-001-374`), and are reviewed again at the Exception's mandatory review point (below) — not only at the moment it is granted.

**DS-001-371: Every Exception Is Time-Bound and Subject to Mandatory Review**
An Exception is granted for a stated, bounded duration — never indefinitely — and is reviewed by the constitutional authority (`DS-001-361`) at or before its stated expiry. The mandatory review determines whether the underlying justification still holds, whether the deviation should instead be resolved through a permanent Approval (extending the relevant closed set through ordinary constitutional review), or whether the Exception lapses.

**DS-001-372: Permanent Exceptions Are Prohibited**
*Statement.* No Exception may be granted without an end date, renewed indefinitely without re-justification, or otherwise treated as a permanent deviation from this document's principles.
*Architectural Rationale.* A permanent exception is, in substance, an unreviewed amendment to this document — it changes what is actually true of AUREX's visual system without passing through the constitutional review and versioning discipline an actual amendment requires (`DS-001-364`, §22.6). Prohibiting permanence closes that back door structurally rather than relying on restraint.
*Practical Implications.* A deviation that has proven, at repeated mandatory reviews, to be genuinely permanent is not renewed as an exception indefinitely — it is redirected to ordinary constitutional review (§22.1, `DS-001-364`) to either become a permanent Approval or be definitively rejected. An exception is never a substitute for that decision; it is only a bridge to it.

**DS-001-373: Every Exception Is Mandatorily Retired**
An Exception that is not converted to a permanent Approval at or before a mandatory review reaches its stated expiry and is retired automatically — the deviation it permitted ceases, and the underlying element reverts to constitutional conformance. Retirement is not discretionary and does not require a separate approval action to take effect; only continuation requires one.

**Constitutional Decision Recording, Traceability & Accountability**

**DS-001-374: Every Constitutional Decision Is Traceable to Its Authority, Justification, and Outcome**
Every Approval, Rejection, and Exception (`DS-001-365`) is recorded with the authority who decided it, the justification considered, and the outcome reached, in a form that can be reconstructed at any later date. This is the §22.5-level realization of `SD-002-010`'s universal versioning principle (full historical state, comparison, restoration) applied to governance decisions themselves, not only to the tokens and components those decisions concern.

**DS-001-375: Constitutional Accountability Rests With the Reviewing Authority, Not the Requesting Party**
Once a change is approved, accountability for that change having satisfied this document's constitutional discipline rests with the authority that approved it (`DS-001-361`), not with the capability team or contributor that proposed it. A capability team that proposes a change in good faith is not accountable for a defect in constitutional review it had no authority to perform.

---

### §22.5 Validation

Constitutional authority is defined (`DS-001-361`) without inventing an organizational chart or team structure — it cross-references the precedent ARCH-000 §11 and `SD-002-060` already establish, consistent with this document's constitutional-not-organizational character. Approval authority is defined through three closed outcomes (`DS-001-365`) with recording requirements for each (`DS-001-366`, `DS-001-367`). Exception governance is fully defined — written justification and impact assessment (`DS-001-370`), mandatory time-bound review (`DS-001-371`), mandatory retirement (`DS-001-373`) — and permanent exceptions are explicitly and structurally prohibited (`DS-001-372`), not merely discouraged. Ownership boundaries are stated explicitly at this section's opening: Versioning, Contribution Workflow, Release Governance, Compatibility, Deprecation, and Implementation are each named and cross-referenced to their owning section rather than restated. No meeting procedure, organization chart, team structure, Jira workflow, Git workflow, pull request, CI/CD process, DevOps practice, or source-control mechanism appears anywhere above — every process is stated at the constitutional level (who decides, what is recorded, how long an exception lasts) without prescribing how any of it is operationally executed. No overlap exists with any other Chapter 22 section: this section is cited by, and defers implementation of, every other subsection's own governance content, exactly as the approved Chapter 22 architecture specifies.

Two refinements are incorporated. Constitutional approval is based solely on constitutional conformance: `DS-001-364`, as strengthened, states explicitly that review evaluates constitutional conformance, architectural consistency, adherence to governing principles, and compliance with this document's closed systems — and nothing else. Popularity, consensus, seniority, and implementation preference are explicitly excluded as approval criteria: `DS-001-368A` forecloses consensus, popularity, and stakeholder preference as sufficient justification, extending `DS-001-368`'s existing foreclosure of implementation convenience into the same principle family, without referencing any voting process, committee, or organizational mechanism. Implementation quality remains outside the scope of DS-001 governance throughout: `DS-001-364`'s strengthened text now states directly that artistic preference, implementation quality, coding approach, subjective design taste, and implementation aesthetics are not evaluated by constitutional review, restating the Implementation Boundary this chapter opens with at the point where a reader would most plausibly expect it to be tested. Numbering is unaffected beyond the single lettered insertion (`DS-001-368A`); ownership boundaries, Constitutional Review Authority, Approval Outcomes, Exception Approval, Traceability, Accountability, the chapter opening, the Constitutional Sequence, and the Constitutional Change Lifecycle are all unchanged.

*§22.5 complete and frozen. Chapter 22 is complete; no further Chapter 22 authoring remains.*

### 22.6 Versioning Strategy

**This section owns:** Constitutional Versioning; Version Identity; Version Evolution; Version Relationships; Historical Integrity; Version Traceability; Version Baselines; Constitutional Version Registry.
**This section does not own:** Review (§22.1); Approval (§22.5); Token Governance (§22.2); Component Governance (§22.3); Contribution Process (§22.4); Deprecation (§22.7); Compatibility (§22.8); Migration (§22.9); Release Management (§22.10); Implementation Versioning (outside DS-001's scope entirely, per the Implementation Boundary this chapter opens with). Each is cross-referenced below, never restated.

Review determines conformance (§22.1). Approval authorizes change (§22.5). Versioning records constitutional history — this section's entire scope. Deprecation governs retirement (§22.7). Compatibility governs coexistence (§22.8). Migration governs transition (§22.9). Release Management governs publication (§22.10). None of those seven responsibilities belongs to §22.6.

**DS-001-428: This Section Governs Constitutional Versioning, Not Review, Approval, Deprecation, Compatibility, Migration, or Release**
*Statement.* §22.6 governs the identity, lineage, immutability, and traceability of this document's own constitutional history — every version of DS-001 itself, and every token, theme, component, or principle's attribution to the version that introduced or amended it. It does not determine whether a change is approved, retire an element, resolve coexistence between versions, guide a transition, or govern publication.
*Architectural Rationale.* This is the versioning-specific instance of the ownership discipline every subsection of this chapter has applied to its own territory since §22.1: a section whose entire subject is *recording* constitutional history has no authority over what enters that history or what is later done with an entry in it. The frozen Document Architecture's own Ownership Matrix names this section's charter directly — applying the versioning discipline `SD-001-023` and `SD-001-110` already establish for screens and widgets to tokens and components.
*Practical Implications.* A reader looking for whether a proposal was accepted finds that answer in §22.5. A reader looking for what version of DS-001 a given principle first appeared in, and what changed since, finds that answer here.

**DS-001-429: Every Constitutional Change Belongs to a Version**
No Approval or Exception outcome (`DS-001-365`, §22.5) takes effect as part of an unversioned, ambient state of this document. Every constitutional change — a new token, a strengthened principle, a lettered insertion — belongs to a specific, identified version of DS-001, consistent with this document's own header, which already declares itself "Version 1.0."

**Version Identity**

**DS-001-430: Every Version Has a Permanent, Unique Identity**
A version of DS-001 is identified in a form that is never reused, reassigned, or shared with another version, mirroring the identity-permanence discipline `DS-001-029` (Chapter 3) already establishes for individual principle numbers, applied here to the document as a whole.

**DS-001-431: The Lettered-Suffix Convention Is the Governed Mechanism for Mid-Sequence Constitutional Insertion**
*Statement.* A constitutional principle inserted into an already-published, already-cross-referenced sequence of principle identifiers is numbered using the base identifier immediately preceding its insertion point, suffixed with a letter — for example, `DS-001-368A`, inserted immediately after `DS-001-368` — never the next unused integer in the overall sequence.
*Architectural Rationale.* This document has used this exact convention sixteen times (`067A`, `072A`, `084A`, `096A`, `190A`, `212A`, `230A`, `249A`, `259A`, `280A`, `295A`, `309A`, `323A`, `336A`, `352A`, and `368A`) without, until now, formally documenting the rule those insertions followed. The convention exists because a mid-sequence integer insertion would force renumbering of every subsequent already-published, already-cross-referenced identifier — breaking every citation this document makes to those identifiers from within itself, in exactly the way `DS-001-437`'s prohibition on rewriting constitutional history exists to prevent. A lettered suffix inserts new content without disturbing a single identifier that already exists.
*Practical Implications.* The lettered-suffix convention is used only when inserting a refinement into content whose surrounding integer sequence has already been assigned and cross-referenced elsewhere in this document — never for a chapter's original authoring, where identifiers are assigned sequentially as the chapter is first drafted. A lettered suffix is never itself further subdivided; a location requiring more than one inserted principle receives sequential letters (`368A`, `368B`, and so forth) at the same insertion point, never a nested suffix.

**Version Evolution & Relationships**

**DS-001-432: Every Version Records Its Constitutional Predecessor**
Every version of DS-001 after the first identifies the specific prior version it evolved from. No version exists with an undeclared or ambiguous predecessor.

**DS-001-433: Every Version Identifies the Constitutional Changes It Introduces**
A version's record states, specifically, which principles, tokens, or closed-set elements it added, strengthened, or otherwise changed relative to its predecessor (`DS-001-432`) — not merely that a new version exists, but what constitutional difference it makes.

**DS-001-434: Version Lineage Is Preserved as an Unbroken Chain**
The chain of predecessor relationships (`DS-001-432`) from any given version back to this document's first version is never broken, gapped, or ambiguous at any point. A version whose lineage cannot be traced to the original is not a valid version of this document.

**Historical Integrity & Immutability**

**DS-001-435: Published Versions Are Immutable**
*Statement.* Once a version of DS-001 is published, its content does not change. No principle, token, or closed-set element recorded as part of a published version is later edited within that version's own record.
*Architectural Rationale.* This is the versioning-level enforcement of `DS-001-162` (Token Meaning Is Immutable, Chapter 10) and `DS-001-029` (Principle Evolution Is Constitutional, Not Editorial, Chapter 3), generalized from individual tokens and principles to the document as a whole: a document whose published versions could be silently altered would make every citation this document contains — to itself, and to it from any future consuming document (Chapter 2, `DS-001-013`) — unreliable the moment it was made.
*Practical Implications.* A defect discovered in a published version is not corrected by editing that version's record — it is corrected through a newer version (`DS-001-436`), which records the correction as a constitutional change in its own right, attributable to its own version identity.

**DS-001-436: Corrections Occur Only Through Newer Versions, Never Through Editing a Published One**
This is the direct consequence of `DS-001-435`, stated as its own operative rule: a correction to this document takes the same path as any other constitutional change — proposal (§22.4), review (§22.1), approval (§22.5) — and is recorded in a new version, never applied retroactively to an already-published one.

**DS-001-437: Constitutional History Is Never Rewritten**
The record of what a given version of DS-001 stated, when it was published, and what changed since is permanent and is never revised to read as though a later understanding had applied from the start. This is the principle `DS-001-431`'s lettered-suffix convention exists specifically to protect.

**DS-001-438: Superseded Versions Remain Authoritative Historical Records**
A version superseded by a later one does not become invalid or unreliable as a record of what this document constitutionally stated at that point in its history — it remains the authoritative account of that period, exactly as `DS-001-425` (§22.4) already establishes for a superseded proposal.

**Version Traceability**

**DS-001-439: Every Constitutional Element Identifies the Version That Introduced It**
Every token, theme, component, or principle this document governs states, as part of its record, the specific version of DS-001 in which it first appeared — extending the same attribution discipline the Token Registry (`DS-001-395`, §22.2) and Component Registry (`DS-001-410`, §22.3) already require, generalized here to every constitutional element regardless of registry.

**DS-001-440: Every Constitutional Amendment Identifies the Version in Which It Occurred**
Where an existing element is later strengthened, extended, or otherwise amended — as `DS-001-159` (Chapter 10) and `DS-001-364` (§22.5) both were — the amendment identifies the version in which it occurred, distinct from the version that introduced the element originally. An element's full history is the complete list of versions in which it was introduced and subsequently amended.

**DS-001-441: Historical Versions Remain Reproducible**
Any past version of DS-001 can be reconstructed in full from this section's records, exactly as it existed at the time it was published, regardless of how many later versions have since superseded it. This is the document-level realization of `SD-002-010`'s universal versioning principle (effective-dated reconstruction of "what was true as of any given date").

**Version Baselines**

**DS-001-442: Baselines Are Explicitly Identifiable Versions**
A baseline — a version designated as the reference point for a release (§22.10), a compatibility determination (§22.8), or a migration target (§22.9) — is always one of this document's own identified versions (`DS-001-430`), never an informally described or approximate state. This section states only that baselines are identifiable versions; what makes a given version a baseline for release, compatibility, or migration purposes belongs to those respective sections.

**Constitutional Version Registry**

**DS-001-443: A Single Authoritative Version Registry Exists as a Governance Artifact**
*Statement.* Every version of DS-001, and every constitutional element's introduction and amendment history (`DS-001-439`–`440`), has exactly one record in a single Version Registry. No token, component, or principle's version history exists outside it, and no parallel or capability-specific version record may exist alongside it.
*Architectural Rationale.* This is the practical mechanism by which `DS-001-434`'s unbroken-lineage guarantee and `DS-001-441`'s reproducibility guarantee are actually verifiable rather than aspirational, mirroring `DS-001-395` (§22.2) and `DS-001-410` (§22.3): a registry is what makes "this document's full constitutional history" a checkable fact rather than a claim.
*Practical Implications.* The Version Registry is a governance artifact, not a source-control system — it records constitutional facts about versions (identity, predecessor, changes introduced, elements attributed), never commit hashes, branch names, or repository structures, which remain entirely outside DS-001's scope per the Implementation Boundary this chapter opens with.

---

### §22.6 Validation

Versioning remains constitutional throughout: every principle above states a governance rule about identity, lineage, immutability, or traceability of this document's own history, never a Git version, source-control mechanism, package version, npm version, software semantic-versioning example, build number, deployment version, or release-pipeline detail. Historical integrity is preserved: `DS-001-437` states this directly, and `DS-001-431`'s formalized lettered-suffix convention is presented as the specific mechanism that has protected it throughout this document's own authoring. Published versions are immutable: `DS-001-435` states this as an explicit rule, with `DS-001-436` naming the only permitted path for a correction — a new version, never an edit to an old one. Constitutional history cannot be rewritten: `DS-001-437` and `DS-001-438` jointly guarantee that a superseded version remains an authoritative record of its own period rather than being revised or invalidated. Approval remains owned by §22.5 — `DS-001-429` and `DS-001-436` both cross-reference the Approval outcome and the review/approval path a correction takes without restating either. Review remains owned by §22.1 — no principle above states or implies a conformance criterion of its own. Deprecation is not duplicated — `DS-001-442` names baselines as identifiable versions without defining retirement, deferring entirely to §22.7. Compatibility is not duplicated — the same principle names baselines as a shared concept without defining what makes versions compatible, deferring to §22.8. Migration is not duplicated — nothing above defines how a transition between versions is performed, deferring to §22.9. Release Management is not duplicated — nothing above defines what makes a version publishable, deferring to §22.10. Every constitutional element remains historically traceable: `DS-001-439`–`441` jointly guarantee that every token, component, and principle's full version history — introduction, amendment, and reconstruction at any past point — is recoverable from the single Version Registry `DS-001-443` establishes.

*§22.6 complete and frozen. Chapter 22 is complete; no further Chapter 22 authoring remains.*

### 22.7 Deprecation Policy

**This section owns:** Constitutional Deprecation; Deprecation Principles; Deprecation Lifecycle; Deprecation Notice; Deprecation Traceability; Retirement Eligibility; Historical Preservation.
**This section does not own:** Review (§22.1); Approval (§22.5); Token Governance (§22.2); Component Governance (§22.3); Contribution Process (§22.4); Versioning (§22.6); Compatibility (§22.8); Migration (§22.9); Release Management (§22.10); Implementation (outside DS-001's scope entirely, per the Implementation Boundary this chapter opens with). Each is cross-referenced below, never restated.

Review determines conformance (§22.1). Approval authorizes deprecation (§22.5). Versioning records history (§22.6). Deprecation governs constitutional retirement — this section's entire scope. Compatibility governs coexistence (§22.8). Migration governs transition (§22.9). Release Management governs publication (§22.10). None of those six other responsibilities is duplicated below.

**DS-001-444: This Section Governs Constitutional Deprecation, Not Retirement Mechanics of Any Other Kind**
*Statement.* §22.7 governs how a constitutional element — a token, theme, component, or principle — is marked deprecated, how deprecation notice precedes retirement, and how retirement, once eligible, preserves rather than erases constitutional history. It does not govern implementation removal, source code cleanup, repository maintenance, software support periods, product lifecycle, or engineering rollout.
*Architectural Rationale.* This is the deprecation-specific instance of the ownership discipline every subsection of this chapter has applied since §22.1: deprecation is a constitutional status this document records about itself, not an instruction to any implementation about what to delete or when. The frozen Document Architecture's own Ownership Matrix already names the precedent this section applies — `SD-001-023` and `SD-001-110`'s screen/widget versioning and deprecation discipline, extended to tokens and components.
*Practical Implications.* A reader looking for when an implementation must stop supporting a deprecated element finds that answer outside DS-001 entirely, in implementation specifications and engineering documents, per the Implementation Boundary this chapter opens with. A reader looking for what it constitutionally means for an element to be deprecated, and what must be true before it may be retired, finds that answer here.

**DS-001-445: No Constitutional Element Becomes Deprecated Implicitly**
Deprecation is a stated, recorded status, never an inference drawn from an element's age, disuse, or absence from recent chapters. An element not explicitly marked deprecated remains fully governed and conformant, regardless of how long it has existed unchanged.

**DS-001-446: Deprecation Requires Constitutional Approval Under §22.5**
Marking an element deprecated is itself a constitutional change, subject to the same proposal (§22.4), review (§22.1), and approval (§22.5) discipline as any other. No element is deprecated by informal agreement, by an implementation team's decision, or by the passage of time alone.

**Deprecation Lifecycle & Notice**

**DS-001-447: Deprecation Is a Named Lifecycle Stage, Distinct From and Preceding Retirement**
This restates, as this section's own governing rule, the Deprecated stage `DS-001-388` (§22.2) and `DS-001-400` (§22.3) already name in the token and component lifecycle: Deprecated and Retired are two distinct stages, not one. An element may remain Deprecated — governed, still conformant, but marked for eventual retirement — for as long as `DS-001-449`'s notice period and `DS-001-451`'s dependency condition require.

**DS-001-448: Every Deprecated Element Records the Version in Which It Became Deprecated**
This extends `DS-001-440`'s (§22.6) amendment-attribution discipline specifically to deprecation: the version identity in which an element's status changed to Deprecated is recorded as part of its constitutional history, alongside the version that originally introduced it (`DS-001-439`, §22.6).

**DS-001-449: Deprecation Notice Precedes Retirement by a Stated Minimum Period**
*Statement.* An element marked Deprecated remains in that stage for no less than the minimum notice period `SD-001-110` establishes — a minimum of two major platform releases — before it becomes eligible for retirement. No element proceeds directly from Active to Retired.
*Architectural Rationale.* This is the direct application, at the constitutional-element level, of `SD-001-110`'s named deprecation policy, which this chapter's frozen objective already commits DS-001 to applying to tokens and components. A shorter or undefined notice period would leave capabilities and implementations no reliable window to migrate away from the element before it disappears from governance.
*Practical Implications.* The notice period is a constitutional minimum, not a target — an element may remain Deprecated longer than the minimum where `DS-001-451`'s dependency condition has not yet cleared, but never shorter.

**Retirement Eligibility**

**DS-001-450: Retirement May Occur Only After Constitutional Deprecation**
No element is retired directly from Active status. Retirement eligibility begins only once an element has completed the Deprecated stage (`DS-001-447`) and satisfied its minimum notice period (`DS-001-449`).

**DS-001-451: Retirement Is Withheld While Constitutional Artefacts Still Depend on the Element**
*Statement.* An element eligible for retirement under `DS-001-450` is nonetheless not retired while any other governed token, theme, component, or principle still depends on it. Retirement proceeds only once every such dependency is itself resolved — migrated to a replacement, or retired alongside it.
*Architectural Rationale.* This generalizes `DS-001-408` (§22.3), which establishes exactly this precondition for components specifically, to every constitutional element this document governs — tokens, themes, brand tiers, and principles alike face the same orphan-reference risk a component retired out from under a dependent Composite already illustrates.
*Practical Implications.* The specific mechanics of how a dependent element migrates away from the one being retired belong exclusively to §22.9 (Migration Guidance) — this principle states only the constitutional precondition that retirement may not proceed until that migration, or an equivalent joint retirement, is complete.

**DS-001-452: Retirement Never Erases Constitutional History**
Retiring an element changes its current governance status from Deprecated to Retired; it does not remove the element's record, its introduction and amendment history (`DS-001-439`–`440`, §22.6), or any version in which it was Active or Deprecated. Retirement is a status change recorded in history, never a deletion of history.

**Deprecation Traceability & Historical Preservation**

**DS-001-453: Deprecation Never Removes Historical Validity**
An element's Deprecated or Retired status in the current version of DS-001 does not retroactively make it non-conformant within any past version where it was Active. This is the deprecation-specific application of `DS-001-438` (§22.6): a superseded version remains an authoritative record of what was true when it was published, regardless of what has since been deprecated or retired.

**DS-001-454: Deprecated and Retired Elements Remain Historically Valid Within the Versions That Governed Them**
An implementation or artefact correctly built against a past version of DS-001 was, and remains, conformant with respect to that version, even after the element it relied on has since been deprecated or retired in a later version. Conformance is always evaluated against a stated version, never against the current state of this document by default.

**DS-001-455: Historical Versions Remain Internally Consistent After Later Deprecation**
Marking an element deprecated in a later version does not introduce an inconsistency into any earlier version's own record — each version, reconstructed per `DS-001-441` (§22.6), reads exactly as it did when published, with the element shown as Active throughout, regardless of its status in versions that came after.

**DS-001-456: Deprecation Status Is Permanently Traceable**
An element's complete deprecation history — the version it was deprecated in (`DS-001-448`), the notice period served (`DS-001-449`), and, if applicable, the version it was retired in — is recorded in the Version Registry (`DS-001-443`, §22.6) and remains reconstructable at any later date, exactly as every other constitutional decision this document records.

**DS-001-457: Constitutional References Remain Resolvable Even After Retirement**
*Statement.* A citation elsewhere in this document to a retired element — for example, a cross-reference from a still-Active principle — remains resolvable to that element's historical record after retirement. A citation is never left pointing to nothing.
*Architectural Rationale.* This closes the same orphaned-reference risk `DS-001-451` closes for dependency-blocked retirement, extended to the case where retirement has already occurred: a citation that resolves to silence would violate `DS-001-437`'s (§22.6) prohibition on constitutional history being effectively rewritten by omission, even where no text was literally deleted.
*Practical Implications.* A future reader encountering a citation to a retired element is shown that element's historical record — what it was, when it was deprecated and retired, and why — never a broken or dangling reference.

---

### §22.7 Validation

Deprecation remains constitutional throughout: every principle above states a governance rule about status, notice, eligibility, or traceability, never an implementation removal instruction, source-code cleanup task, repository-maintenance procedure, software support period, product-lifecycle plan, or engineering rollout step. Deprecation never deletes history: `DS-001-452` states this directly, and `DS-001-457` extends it to guarantee that citations to a retired element remain resolvable rather than dangling. Historical validity is preserved: `DS-001-453`–`455` jointly guarantee that a past version's own record, and any implementation correctly built against it, remains conformant regardless of what has since been deprecated or retired in a later version. Retirement is governed: `DS-001-450` fixes deprecation as a mandatory precondition, `DS-001-449` fixes the minimum notice period at `SD-001-110`'s two-release standard, and `DS-001-451` withholds retirement until every dependency is resolved, generalizing `DS-001-408`'s (§22.3) component-specific rule to every constitutional element. Approval remains owned by §22.5 — `DS-001-446` states explicitly that deprecation itself requires approval under §22.5 rather than defining a separate deprecation-approval mechanism. Review remains owned by §22.1 — no principle above states or implies a conformance criterion of its own. Versioning is not duplicated — `DS-001-448` and `DS-001-456` both cite the Version Registry and amendment-attribution discipline §22.6 owns without restating it. Compatibility is not duplicated — nothing above defines what makes a deprecated element compatible or incompatible with another version, deferring entirely to §22.8. Migration is not duplicated — `DS-001-451`'s deferral to §22.9 is cited, not reopened, exactly as `DS-001-408` (§22.3) already deferred it. Release Management is not duplicated — nothing above defines what makes a version publishable, deferring to §22.10. Every deprecated constitutional element remains historically traceable: `DS-001-448`, `DS-001-456`, and `DS-001-457` jointly guarantee that an element's deprecation and retirement history, and every citation to it, remains permanently recoverable.

*§22.7 complete and frozen. Chapter 22 is complete; no further Chapter 22 authoring remains.*

### 22.8 Compatibility Policy

**This section owns:** Constitutional Compatibility; Compatibility Principles; Compatibility Classification; Compatibility Guarantees; Cross-Version Compatibility; Cross-Document Compatibility; Compatibility Traceability; Compatibility Verification.
**This section does not own:** Review (§22.1); Approval (§22.5); Token Governance (§22.2); Component Governance (§22.3); Contribution Process (§22.4); Versioning (§22.6); Deprecation (§22.7); Migration (§22.9); Release Management (§22.10); Implementation (outside DS-001's scope entirely, per the Implementation Boundary this chapter opens with). Each is cross-referenced below, never restated.

Review evaluates conformance (§22.1). Approval authorizes constitutional change (§22.5). Versioning records constitutional history (§22.6). Deprecation governs retirement (§22.7). Compatibility governs coexistence — this section's entire scope. Migration governs transition (§22.9). Release Management governs publication (§22.10). None of those six other responsibilities belongs to another section.

**DS-001-458: This Section Governs Constitutional Coexistence, Not Implementation Compatibility**
*Statement.* §22.8 governs whether constitutional elements — within DS-001 across versions, and between DS-001 and the canonical specifications it depends on — may coexist without violating this document's architecture. It does not govern software backward compatibility, API compatibility, browser compatibility, framework compatibility, runtime compatibility, or implementation testing.
*Architectural Rationale.* This is the compatibility-specific instance of the ownership discipline every subsection of this chapter has applied since §22.1: whether two governed elements can coexist constitutionally is a question this document answers about itself; whether a browser or framework can run them is answered entirely outside DS-001, per the Implementation Boundary this chapter opens with.
*Practical Implications.* A reader looking for whether a specific rendering engine supports a specific token value finds that answer outside DS-001 entirely. A reader looking for whether two versions of DS-001, or DS-001 and a change to SD-001, can be constitutionally relied upon together finds that answer here.

**DS-001-459: Compatibility Is Determined Constitutionally, Never by Implementation Behaviour**
A compatibility determination is reached by evaluating two elements or versions against this document's own architecture — semantic meaning, closed-set membership, ownership boundaries — never by observing whether an implementation happens to render them without error. An implementation that renders two constitutionally incompatible elements without visible failure has not made them compatible; it has simply not yet exposed the incompatibility.

**DS-001-460: No Compatibility Determination Is Assumed; Every One Is Explicit**
Two versions, or two constitutional elements, are never presumed compatible by default merely because no incompatibility has been reported. A compatibility determination is a stated, recorded outcome (below), reached through the same evaluative discipline `DS-001-459` establishes — silence is not a determination.

**Compatibility Classification**

**DS-001-461: Every Compatibility Determination Is Classified as Compatible, Incompatible, or Conditionally Compatible**
*Statement.* A compatibility determination between two versions or elements concludes in one of three classifications: Compatible (coexistence introduces no constitutional conflict), Incompatible (coexistence violates this document's architecture), or Conditionally Compatible (coexistence is constitutional only under a stated condition, such as a specific theme or brand context). No fourth classification exists.
*Architectural Rationale.* This mirrors `DS-001-365`'s (§22.5) closed three-outcome structure for review, applied to compatibility: a closed classification set is what makes compatibility determinations comparable and auditable across this document's entire history, rather than each determination inventing its own descriptive language.
*Practical Implications.* A determination that cannot be cleanly classified into one of the three is not yet complete — it is returned for further evaluation, never recorded as an ambiguous fourth state.

**Cross-Version Compatibility**

**DS-001-462: Compatibility Applies Across Every Governed Constitutional Element**
Compatibility determinations are made across Tokens (§22.2), Themes (Chapter 11), Components (§22.3), and any pattern or template this document or its future chapters govern — no category of constitutional element is exempt from requiring an explicit compatibility determination when it changes.

**DS-001-463: Compatibility Is Version-Aware**
Every compatibility determination is made between two specifically identified versions (`DS-001-430`, §22.6), never between an element and an undated, ambient notion of "the current state" of this document. A determination that a given element is compatible "with DS-001" without stating which version of DS-001 is incomplete.

**DS-001-464: Constitutional Incompatibility Requires Constitutional Approval Before Publication**
*Statement.* Where a proposed change would render a constitutional element incompatible with a version that previously depended on it, that incompatibility is not published silently as a side effect of the change's own approval — the incompatibility itself is identified, classified (`DS-001-461`), and confirmed as an accepted consequence through the same constitutional approval (§22.5) that authorized the underlying change.
*Architectural Rationale.* A change could be fully conformant under §22.1's eleven review criteria and still introduce an incompatibility its proposer never intended or noticed — impact analysis, the stage of this chapter's Constitutional Change Lifecycle that precedes Architectural Review, exists precisely to surface exactly this kind of consequence before publication, not after.
*Practical Implications.* A change's approval record (`DS-001-374`, §22.5) includes any Incompatible or Conditionally Compatible determination it introduces, so that the incompatibility is a documented, accepted decision rather than a defect discovered later.

**Cross-Document Compatibility**

**DS-001-465: Cross-Document Compatibility Extends This Document's Coexistence Discipline to Every Canonical Specification DS-001 Depends On**
*Statement.* This document maintains an explicit compatibility relationship with every canonical specification it cites — principally SD-001, SD-002, and ARCH-000, and, where relevant, ERG-001, ADR-001, and the canonical CIL. Where DS-001 cites a specific principle by ID from one of these documents, that citation's continued validity is a compatibility concern this section governs, not a fact assumed to remain true indefinitely.
*Architectural Rationale.* Every chapter of this document that renders an SD-001 or SD-002 mandate does so by citing a specific principle ID — dozens of such citations exist. Those citations were, until this section, a one-directional dependency with no stated process for what happens if the cited principle is later renumbered, reinterpreted, or retired by its own owning document's governance. This section closes that gap.
*Practical Implications.* IMP-001 and PE-001, named in Chapter 2 (`DS-001-013`) as future inheritors of this document, are included in this same cross-document compatibility discipline from the direction of consumption: their citations of DS-001 principle IDs are, once they exist, subject to the identical concern this section addresses for DS-001's own citations of SD-001 and SD-002.

**DS-001-466: A Constitutional Reference Shall Never Become Silently Orphaned When Its Source Document Changes**
*Statement.* Where SD-001, SD-002, ARCH-000, an ADR, or the canonical CIL changes in a way that affects a principle DS-001 cites, that citation is reviewed at the next constitutional review cycle (§22.1) — reclassified as Compatible, Incompatible, or Conditionally Compatible (`DS-001-461`) — and never left silently pointing to a principle that no longer means what DS-001's citation of it presumed.
*Architectural Rationale.* This is the cross-document application of `DS-001-457`'s (§22.7) guarantee that a citation to a retired element remains resolvable rather than dangling, extended from citations within DS-001 to citations DS-001 makes outward. A design system whose own constitutional grounding could silently drift out of alignment with the documents it claims to render would eventually cite authority that no longer exists in the form cited.
*Practical Implications.* This principle does not obligate DS-001 to monitor SD-001, SD-002, ARCH-000, ADRs, or the CIL continuously — it obligates that when such a change becomes known, through the same constitutional review process (§22.1) that already governs every other proposal, the affected citation is resolved rather than left unaddressed indefinitely.

**DS-001-467: The Constitutional Dependency Matrix Is a Living Governance Artifact**
*Statement.* This document's dependency footprint — which canonical documents it cites, and, once registered in ARCH-000 and consumed by PE-001 or IMP-001, which documents cite it — is maintained as a living record, not a fixed analysis frozen at any single point in this document's authoring.
*Architectural Rationale.* A dependency graph produced once and never revisited would drift out of accuracy the moment any cited document, or DS-001 itself, changes — the same staleness risk `DS-001-466` addresses for individual citations, applied here to the aggregate picture of DS-001's dependencies. Treating the matrix as living, updated through this document's own Constitutional Change Lifecycle, is what keeps it a reliable governance artifact rather than a historical snapshot.
*Practical Implications.* Every constitutional change that adds, removes, or reinterprets a citation to another canonical document (`DS-001-465`) updates the Dependency Matrix as part of that change's own record, consistent with the Impact Analysis stage of the Constitutional Change Lifecycle this chapter's opening establishes.

**Compatibility Traceability & Verification**

**DS-001-468: Compatibility Determinations Remain Permanently Traceable**
Every compatibility determination — its classification (`DS-001-461`), the versions or elements it concerns (`DS-001-463`), and the constitutional approval that accepted any resulting incompatibility (`DS-001-464`) — is recorded and reconstructable at any later date, consistent with the traceability discipline `DS-001-374` (§22.5) and `DS-001-441` (§22.6) already establish for decisions and versions respectively.

**DS-001-469: Compatibility Never Rewrites Historical Versions**
A compatibility determination made about a past version does not alter that version's own published record (`DS-001-435`, §22.6). It is recorded as a new, dated determination referencing the historical version, never as a retroactive edit to it.

**DS-001-470: Compatibility Verification Is Repeatable and Deterministic**
A compatibility determination reached between two specific, identified versions or elements produces the same classification regardless of who performs the determination or when — mirroring `DS-001-384`'s (§22.1) repeatability guarantee for conformance verification, applied here to compatibility specifically.

**DS-001-471: No Constitutional Element May Silently Become Incompatible**
*Statement.* An element's compatibility status with a prior version or a dependent document SHALL NOT change as an undocumented side effect of an unrelated constitutional change. Any change with the potential to alter an existing compatibility determination is evaluated for that effect explicitly, as part of that change's own impact analysis, before it is approved.
*Architectural Rationale.* This is the closing guarantee of this section: `DS-001-460` establishes that compatibility is never assumed by default; this principle establishes the mirror case, that compatibility already established is never lost by default either. Both directions must hold for compatibility to be a genuinely governed property rather than an incidental one.
*Practical Implications.* A proposal's impact analysis (evaluated as part of §22.1's review) includes checking whether the proposed change would alter the compatibility classification of any existing, already-recorded determination — not only whether the proposal itself introduces a new one.

---

### §22.8 Validation

Compatibility remains constitutional throughout: every principle above states a governance rule about coexistence, classification, or traceability, never a software backward-compatibility rule, API contract, browser-support matrix, framework-version requirement, runtime behaviour, or implementation-testing procedure. No implementation compatibility appears anywhere above. Compatibility is explicit and traceable: `DS-001-460` forecloses assumed compatibility, and `DS-001-468` guarantees every determination is permanently reconstructable. Historical integrity is preserved: `DS-001-469` states that compatibility determinations never rewrite a historical version's own published record, consistent with `DS-001-435` and `DS-001-437` (§22.6). Cross-document consistency is maintained: `DS-001-465`–`467` establish the cross-document compatibility discipline this document's citations of SD-001, SD-002, ARCH-000, ERG-001, ADR-001, and the canonical CIL require, with `DS-001-466` specifically closing the "silently orphaned reference" gap and `DS-001-467` establishing the Dependency Matrix as a living, continuously updated governance artifact rather than a one-time analysis. Approval remains owned by §22.5 — `DS-001-464` and `DS-001-471` both cross-reference constitutional approval rather than defining a separate compatibility-approval mechanism. Review remains owned by §22.1 — `DS-001-464` and `DS-001-471` both cross-reference §22.1's review and impact analysis rather than defining new conformance criteria. Versioning is not duplicated — `DS-001-463` and `DS-001-469` both cite §22.6's version identity and immutability discipline without restating it. Deprecation is not duplicated — nothing above defines when or how an element is deprecated, only how its compatibility is subsequently determined. Migration is not duplicated — nothing above defines how a transition between incompatible versions is performed, deferring entirely to §22.9. Release Management is not duplicated — nothing above defines what makes a version publishable, deferring to §22.10. No constitutional incompatibility can emerge without governance: `DS-001-464` requires every incompatibility to be identified, classified, and approved before publication, and `DS-001-471` closes the reverse case, ensuring no already-established compatibility is silently lost either.

*§22.8 complete and frozen. Chapter 22 is complete; no further Chapter 22 authoring remains.*

### 22.9 Migration Guidance

**This section owns:** Constitutional Migration; Migration Principles; Migration Eligibility; Migration Traceability; Migration Integrity; Migration Completion.
**This section does not own:** Review (§22.1); Approval (§22.5); Token Governance (§22.2); Component Governance (§22.3); Contribution Process (§22.4); Versioning (§22.6); Deprecation (§22.7); Compatibility (§22.8); Release Management (§22.10); Implementation (outside DS-001's scope entirely, per the Implementation Boundary this chapter opens with). Each is cross-referenced below, never restated.

Review determines conformance (§22.1). Approval authorizes constitutional change (§22.5). Versioning records constitutional history (§22.6). Deprecation governs retirement (§22.7). Compatibility governs coexistence (§22.8). Migration governs constitutional transition — this section's entire scope. Release Management governs constitutional publication (§22.10). None of those six other responsibilities is duplicated below.

**DS-001-472: This Section Governs Constitutional Migration, Not Implementation Rollout**
*Statement.* §22.9 governs the constitutional record of a governed transition — from a source token, component, theme, or principle to its replacement — including eligibility, integrity, traceability, and completion. It does not govern deployment sequencing, software upgrade procedures, release execution, operational cut-over, data migration, or any other engineering activity.
*Architectural Rationale.* This is the migration-specific instance of the ownership discipline every subsection of this chapter has applied since §22.1: a constitutional migration record states that a dependent artefact has been redirected from one governed element to another, and when; it does not instruct any implementation team on how, or in what sequence, to perform that redirection in running software. `DS-001-408` (§22.3) and `DS-001-451` (§22.7) each already deferred their retirement-precondition migration mechanics to this section by name — this is where that deferral is resolved.
*Practical Implications.* A reader looking for how to sequence a production deployment, or what operational steps a rollout requires, finds that answer entirely outside DS-001, in implementation specifications and engineering documents, per the Implementation Boundary this chapter opens with. A reader looking for what it constitutionally means for a dependent artefact to have migrated, and how that migration is recorded, finds that answer here.

**DS-001-473: Migration Is the Governed Transition Between Two Constitutionally Approved States**
A migration record connects exactly two constitutional states — a source (typically a Deprecated or Retired element, per `DS-001-447`, §22.7) and a destination (an Active element that constitutionally replaces it) — both of which were themselves reached through ordinary constitutional review and approval (§22.1, §22.5). Migration does not itself approve either state; it records the governed passage between two states each already approved on their own terms.

**DS-001-474: Migration Occurs Only Between Constitutionally Approved States**
No migration record connects a source or destination that has not itself completed review (§22.1) and approval (§22.5). A migration to an unapproved, still-pending proposal is not a valid migration record — it is, at most, a stated intention pending that proposal's own disposition (`DS-001-421`, §22.4).

**Migration Principles**

**DS-001-475: Migration Never Bypasses Versioning**
Every migration record identifies the specific versions (`DS-001-430`, §22.6) its source and destination belong to. A migration that does not state which version it migrates from and to has not satisfied this section's baseline requirement, regardless of how complete its other content is.

**DS-001-476: Migration Never Bypasses Compatibility Evaluation**
*Statement.* A migration is recorded only once the compatibility relationship between its source and destination has been determined and classified (`DS-001-461`, §22.8). Migration eligibility depends on that determination already existing; migration does not itself determine compatibility.
*Architectural Rationale.* This fixes the ordering the Constitutional Change Lifecycle already implies: Compatibility (§22.8) determines whether two states may coexist or must transition; Migration (this section) records how a dependent artefact makes that transition once it is known to be necessary. Reversing this order — migrating before compatibility is known — would make the migration record meaningless, since it would not yet be established what the destination actually requires of a dependent artefact.
*Practical Implications.* A migration record cites the specific compatibility determination (§22.8) that established the transition was needed, rather than restating or re-deriving the compatibility analysis itself.

**DS-001-477: Migration Is Explicit, Never Implicit or Assumed**
A dependent artefact is never presumed to have migrated merely because its source element was retired. Migration is a stated, recorded event distinct from retirement (`DS-001-450`–`452`, §22.7) itself — retirement marks the source's status; migration marks the dependent artefact's own transition, and the two are never conflated.

**Migration Eligibility**

**DS-001-478: Every Migration Identifies Its Source and Destination Constitutional Versions**
A migration record states, unambiguously, the specific version-identified source element (`DS-001-473`) it transitions from and the specific version-identified destination element it transitions to. A migration record naming only one side of the transition is incomplete.

**DS-001-479: Migration Eligibility Depends on a Prior Compatibility Determination**
This restates, as this section's own governing rule, `DS-001-476`'s ordering requirement: an element becomes eligible to serve as a migration destination only once §22.8 has classified its relationship to the source as Compatible, Incompatible (requiring the migration), or Conditionally Compatible (requiring the migration to state which condition applies).

**DS-001-480: A Dependency-Blocked Retirement Is the Most Common Trigger for a Required Migration**
*Statement.* Where `DS-001-451` (§22.7) withholds a component's retirement because another constitutional artefact still depends on it, that dependency is resolved through exactly the migration record this section governs — the dependent artefact is migrated to a replacement, recorded per `DS-001-478`, before the retirement §22.7 was withholding can proceed.
*Architectural Rationale.* This is the explicit resolution of the deferral `DS-001-408` (§22.3) and `DS-001-451` (§22.7) each made by name to this section: both principles state that retirement is blocked by an unresolved dependency and that the mechanics of resolving it belong to §22.9. This principle is where that mechanics is actually defined.
*Practical Implications.* A component, token, or theme's retirement record (§22.7) cites the specific migration record or records (this section) that resolved each dependency blocking it — retirement and migration remain two distinct, cross-referenced records, never merged into one.

**Migration Integrity**

**DS-001-481: Migration Preserves Constitutional Integrity Throughout Transition**
At every point during a recorded migration — before, during, and after — both the source and destination elements remain individually conformant to the review criteria (§22.1) that originally approved them. Migration is a change in a dependent artefact's relationship to two already-conformant elements; it is never an occasion for either element's own conformance to lapse.

**DS-001-482: Migration Never Changes Historical Versions**
A migration record is created going forward from the point the migration occurs; it does not retroactively alter the historical version (`DS-001-435`, §22.6) in which the source element was originally introduced or was still Active. The dependent artefact's relationship to the source element within that historical version remains exactly as it was.

**DS-001-483: Migration Failure Never Corrupts Constitutional History**
*Statement.* Where a recorded migration does not reach completion (`DS-001-485`, below), that incomplete state is itself recorded (`DS-001-486`) rather than leaving the migration record ambiguous, partially written, or silently removed. An incomplete migration never causes the source or destination element's own historical record to become inconsistent.
*Architectural Rationale.* This is the migration-specific application of `DS-001-437` (§22.6, Constitutional History Is Never Rewritten): a failure at the migration stage is a fact about the migration, not license to retroactively tidy the historical record as though the failed attempt had not occurred.
*Practical Implications.* An incomplete migration is diagnosed and either resumed to completion or explicitly abandoned (`DS-001-486`) — never left to quietly disappear from this document's governance record.

**Migration Traceability & Completion**

**DS-001-484: Every Migration Remains Permanently Traceable**
A migration record — its source, destination, governing compatibility determination (`DS-001-479`), and completion status (below) — is recorded and reconstructable at any later date, consistent with the traceability discipline `DS-001-374` (§22.5), `DS-001-441` (§22.6), and `DS-001-456` (§22.7) already establish for decisions, versions, and deprecation history respectively.

**DS-001-485: Migration Completion Is Explicitly Recorded**
A migration reaches a defined completion state only when explicitly recorded as complete — never inferred from the passage of time, from the source element's eventual retirement, or from the absence of any reported problem. Completion is a stated fact, not a default assumption.

**DS-001-486: An Incomplete Migration Is a Distinct, Recorded State, Never a Silent Gap**
A migration that has been initiated but not yet reached completion (`DS-001-485`) is recorded in that specific state — In Progress — rather than being indistinguishable from a migration that was never started or one that has already completed. This closed set of three states (Not Started, In Progress, Complete) is the only vocabulary a migration record uses to describe its own status.

---

### §22.9 Validation

Migration remains constitutional throughout: every principle above states a governance rule about the recorded transition between two approved constitutional states, never an implementation rollout step, deployment sequence, software upgrade procedure, release execution detail, operational cut-over instruction, or data-migration mechanic. No implementation migration appears anywhere above. Migration preserves constitutional history: `DS-001-482` states directly that a migration record never alters the historical version it originates from, and `DS-001-483` guarantees that even a failed or incomplete migration cannot corrupt that history, consistent with `DS-001-437` (§22.6). Migration is version-aware: `DS-001-475` and `DS-001-478` both require a migration record to identify its specific source and destination versions, never an undated or ambient transition. Migration remains traceable: `DS-001-484` extends the traceability discipline `DS-001-374`, `DS-001-441`, and `DS-001-456` already establish to migration records specifically. Approval remains owned by §22.5 — `DS-001-474` states explicitly that migration occurs only between states that have already completed §22.5's approval, never approving anything itself. Review remains owned by §22.1 — `DS-001-474` and `DS-001-481` both cross-reference §22.1's review criteria without redefining conformance. Versioning is not duplicated — `DS-001-475` and `DS-001-478` cite §22.6's version identity discipline without restating it. Deprecation is not duplicated — `DS-001-480` cites `DS-001-451` (§22.7) as the trigger for migration without redefining retirement eligibility or notice periods. Compatibility is not duplicated — `DS-001-476` and `DS-001-479` both require a prior §22.8 compatibility determination as migration's precondition, never determining compatibility themselves. Release Management is not duplicated — nothing above defines what makes a version publishable, deferring entirely to §22.10. Every migration preserves constitutional integrity: `DS-001-481` requires both source and destination to remain independently conformant throughout, and `DS-001-483`–`486` jointly ensure that migration status — Not Started, In Progress, or Complete — is always explicit, never assumed or silently lost.

*§22.9 complete and frozen. Chapter 22 is complete; no further Chapter 22 authoring remains.*

### 22.10 Release Management

**This section owns:** Constitutional Publication; Release Identity; Release Baselines; Release Scope; Release Traceability; Release Integrity; Release Records.
**This section does not own:** Review (§22.1); Approval (§22.5); Token Governance (§22.2); Component Governance (§22.3); Contribution Process (§22.4); Versioning (§22.6); Deprecation (§22.7); Compatibility (§22.8); Migration (§22.9); Implementation; Software Release Processes (all outside DS-001's scope entirely, per the Implementation Boundary this chapter opens with). Each is cross-referenced below, never restated.

Review evaluates constitutional conformance (§22.1). Approval authorizes constitutional change (§22.5). Versioning records constitutional history (§22.6). Deprecation governs retirement (§22.7). Compatibility governs coexistence (§22.8). Migration governs constitutional transition (§22.9). Release Management governs constitutional publication — this section's entire scope. None of those responsibilities overlap.

**DS-001-487: This Section Governs Constitutional Publication, Not Software Release**
*Statement.* §22.10 governs how an already constitutionally approved version of this document becomes a published release — its identity, baseline scope, historical preservation, and traceability. It does not govern software releases, deployment, package publication, CI/CD, Git tags, build pipelines, release trains, engineering schedules, or operational rollout.
*Architectural Rationale.* This is the final instance of the ownership discipline every subsection of this chapter has applied since §22.1: publication, at the constitutional level, is the act of declaring a specific, already-approved version the authoritative statement of this document — a governance act, not an engineering one. A release that changes how software is built or deployed is an implementation-layer event entirely outside DS-001, per the Implementation Boundary this chapter opens with.
*Practical Implications.* A reader looking for how a release is packaged, tagged, or deployed finds that answer entirely outside DS-001. A reader looking for what constitutionally makes a version a release, and what that release permanently records, finds that answer here.

**DS-001-488: Publication Follows Approval and Versioning, in That Order**
No version is published without first completing constitutional approval (§22.5) and being assigned a permanent version identity (`DS-001-430`, §22.6). Publication is the final constitutional act in the Constitutional Change Lifecycle this chapter's opening establishes — it never precedes, substitutes for, or occurs independently of either.

**DS-001-489: Every Release Publishes Exactly One Identified Constitutional Baseline**
A release names one specific version (`DS-001-430`, §22.6) as its published baseline. A release that publishes an unversioned or ambiguously scoped state is not a valid release under this section.

**Release Identity & Baselines**

**DS-001-490: A Release Baseline Is a Specific, Already-Approved Version**
This completes `DS-001-442`'s (§22.6) statement that a baseline is always one of this document's own identified versions, by defining what makes a baseline a release baseline specifically: a version that has completed approval (§22.5), been assigned permanent identity (§22.6), and been designated for publication under this section. §22.6 states that baselines are identifiable versions; this section states what makes one of those versions a released baseline.

**DS-001-491: Only Constitutionally Approved Versions May Be Released**
No version reaches release under this section without having reached an Approval outcome (`DS-001-365`, §22.5) for every constitutional change it contains. A version containing even one still-pending or Exception-only element is not eligible for release as a permanent baseline until that element's own disposition is finalized.

**Release Scope**

**DS-001-492: Publication Never Alters the Approved Constitutional Content It Publishes**
Publishing a version changes that version's status from approved-but-unpublished to released; it does not modify a single token, component, theme, or principle the approved version already contains. This is the release-stage restatement of `DS-001-435` (§22.6, Published Versions Are Immutable), applied at the moment of publication itself rather than only afterward.

**DS-001-493: A Release Does Not Redefine Compatibility, Migration, or Deprecation**
A release publishes what §22.6, §22.7, §22.8, and §22.9 have already determined — version content, deprecation status, compatibility classifications, and migration records — without re-deciding any of them. Publication is downstream of those four sections' own governance, never a parallel or overriding determination.

**Release Integrity & Historical Preservation**

**DS-001-494: Constitutional Publication Is Immutable Once Released**
A released version's content, once published, is never edited within that release. This mirrors `DS-001-435`/`436` (§22.6) exactly, restated here because publication is the point at which immutability becomes externally observable and consequential, not merely an internal drafting discipline.

**DS-001-495: Historical Releases Remain Permanently Accessible**
Every past release remains accessible in full, exactly as it was published, for as long as this document exists — regardless of how many later releases have superseded it. This is the release-level realization of `DS-001-441`'s (§22.6) reproducibility guarantee, applied specifically to the published, externally consumable form of a version.

**DS-001-496: Publication Never Rewrites Constitutional History**
No release, however significant, retroactively alters what an earlier release stated or implies that an earlier release should be read differently in light of later understanding. This is `DS-001-437` (§22.6) restated as this section's own governing rule for the specific, externally visible act of publication.

**Release Traceability & Records**

**DS-001-497: Every Release Permanently Records the Version Published**
A release's record states, permanently, which specific version (`DS-001-430`, §22.6) it published, when, and under which constitutional approval (`DS-001-374`, §22.5). This record does not change after the fact.

**DS-001-498: Every Release Is Historically Traceable**
A release's complete record — its published version, its date, its approval, and its baseline scope (`DS-001-489`) — is reconstructable at any later date, consistent with the traceability discipline every other section of this chapter establishes for its own governance artifacts.

**DS-001-499: A Single Authoritative Release Register Exists as a Governance Artifact**
*Statement.* Every constitutional release of DS-001 has exactly one record in a single Release Register, stating its published version, its baseline scope, and its date. No release exists without a corresponding register record, and no parallel or capability-specific release record may exist alongside it.
*Architectural Rationale.* This is the practical mechanism by which `DS-001-495`'s permanent-accessibility guarantee and `DS-001-498`'s traceability guarantee are actually verifiable, mirroring the Token Registry (`DS-001-395`, §22.2), Component Registry (`DS-001-410`, §22.3), and Version Registry (`DS-001-443`, §22.6) this chapter already establishes.
*Practical Implications.* The Release Register is a governance artifact, not a build or deployment system — it records constitutional facts about releases, never package versions, build numbers, or deployment identifiers, which remain entirely outside DS-001's scope per the Implementation Boundary this chapter opens with.

**Constitutional Registration**

**DS-001-500: DS-001's Own Registration in ARCH-000 Is a Documented, Outstanding Release-Governance Activity**
*Statement.* DS-001's own first constitutional release is not complete, in the fullest sense ARCH-000 §11 (Manifest Governance) requires, until DS-001 is registered in the Architecture Manifest as a recognized constitutional document. This section documents that registration as an owned, timed, and dependent release-governance activity. It does not perform that registration, and it does not modify ARCH-000.
*Architectural Rationale.* Every chapter of this document, from its opening freeze statement onward, has flagged this same outstanding action rather than performing it — consistent with the Implementation Boundary and the constitutional-change discipline this entire chapter establishes: a document does not register itself into a manifest it does not own. ARCH-000 §11 states the manifest "shall be updated whenever a constitutional architecture document is added"; that update is ARCH-000's own governed act, not DS-001's.
*Practical Implications.* Owner: the constitutional authority responsible for ARCH-000 itself, not the authority §22.5 establishes for DS-001's own internal review. Timing: after DS-001's first version reaches release under this section (`DS-001-489`), never before — a document cannot be registered as released before it has been. Dependency: this registration is a precondition for the cross-document consumption Chapter 2 (`DS-001-013`) anticipates from PE-001, PE-001-Cxxx, and IMP-001, and for the "documents that reference DS-001" row of the Dependency Matrix (§22.8) to contain any entries at all. Release Responsibility: recording that this registration has occurred, once it does, is this section's responsibility (`DS-001-497`); performing it is not.

**DS-001-501: The Release Gate Verifies Accessibility Conformance Alongside Every Other Release Criterion**
This closes Chapter 17's direct forward reference (`DS-001-295`: "the specific testing and release process is governed by Design Governance, Chapter 22, §22.1, §22.10"): no version is released under this section without having passed both Architectural Review (§22.1, against its eleven criteria) and verification against the Legibility Standard (Chapter 17, §17.3) under all three accessibility modes (§17.2). Accessibility conformance is not a separate, optional release gate — it is one criterion among the release conditions this section enforces, per `DS-001-491`'s approval requirement.

**DS-001-502: Continuous Improvement Is the Outcome of This Chapter Operating Correctly, Not a Governed Process of Its Own**
*Statement.* Continuous Improvement — the ongoing refinement of AUREX across successive releases — is not a governed process this chapter defines separately. It is the observed outcome of the Constitutional Change Lifecycle, from Proposal (§22.4) through Release (this section), operating correctly and repeatedly over time.
*Architectural Rationale.* This closes the final open item this chapter's own approved architecture identified: no frozen subsection title accommodates Continuous Improvement as its own topic, and none should — inventing an eleventh section to govern an outcome, rather than a process, would misrepresent what Continuous Improvement actually is. A design system does not improve continuously because a section instructs it to; it improves continuously because Proposal, Review, Approval, Versioning, Deprecation, Compatibility, Migration, and Release each function as this chapter defines them, release after release.
*Practical Implications.* A question of the form "how does DS-001 govern continuous improvement" is answered by pointing to this chapter as a whole — its Constitutional Sequence and Constitutional Change Lifecycle — never to a missing eleventh subsection. Continuous Improvement is measured by observing the Release Register (`DS-001-499`) across successive releases, not by a separate governance record kept for that purpose alone.

---

### §22.10 Validation

Release Management remains constitutional throughout: every principle above states a governance rule about publication identity, baseline scope, historical preservation, or traceability, never a software release process, deployment mechanic, package-publication step, CI/CD pipeline, Git tag, build pipeline, release train, engineering schedule, or operational rollout procedure. No implementation release process appears anywhere above. Publication follows approval: `DS-001-488` and `DS-001-491` both fix constitutional approval (§22.5) as a strict precondition to release. Publication follows versioning: the same principles fix permanent version identity (§22.6) as an equally strict precondition, in the stated order. Historical integrity is preserved: `DS-001-494`–`496` jointly restate and extend `DS-001-435`–`437` (§22.6) to the specific, externally visible act of publication. Release records remain permanently traceable: `DS-001-497`–`499` establish the Release Register as the single authoritative record, mirroring every other registry this chapter has established. Approval remains owned by §22.5 — `DS-001-491` cross-references its Approval outcome rather than defining a separate release-approval mechanism. Versioning is not duplicated — `DS-001-490` completes, rather than restates, `DS-001-442`'s (§22.6) baseline principle. Deprecation is not duplicated — `DS-001-493` cites §22.7's determinations without redefining retirement. Compatibility is not duplicated — the same principle cites §22.8's determinations without redefining coexistence. Migration is not duplicated — it cites §22.9's records without redefining transition. Every release identifies one immutable constitutional baseline: `DS-001-489` and `DS-001-494` jointly guarantee this without exception. Beyond the requested checks, this section also closes two items the approved Chapter 22 architecture left open: `DS-001-500` documents, without performing, DS-001's own outstanding ARCH-000 registration — naming its owner, timing, dependency, and release responsibility, per the earlier-approved decision to document rather than act; `DS-001-501` closes Chapter 17's direct forward reference to this section; and `DS-001-502` resolves Continuous Improvement as an outcome of this chapter as a whole rather than a missing eleventh subsection, consistent with Decision 1 of the approved architecture.

*§22.10 complete.*

**Chapter 22 Complete.**
