# ADR-021 — AI-Native Enterprise Experience Framework: Constitutional Foundation

**Status:** Accepted
**Classification:** Architecture Governance / Presentation Architecture Extension
**Decided by:** Repository owner (architecture governance authority), through the AI-Native Enterprise Experience Constitutional Discovery and its own six-concept Constitutional Design Workshop, followed by a Constitutional Compatibility Validation and a Constitutional Home Resolution (session record, 2026-08-07) — the same decision-authority pattern `ADR-006` through `ADR-020` already established. **Disclosure, carried forward from `ADR-020`'s own precedent:** this ADR's preceding discovery, workshop, validation, and placement-resolution passes were conducted in the same session as this ADR's own authoring and were not independently reviewed by a party uninvolved in producing them, unlike the fresh-context reviewer discipline `CLAUDE.md §19.7` requires for Work Package certification. This ADR is the first and only artifact from that process persisted to the repository — no intermediate discovery/workshop/validation document exists as a separate repository file.
**Affected Documents:** None edited by this ADR. This ADR records six constitutional decisions and directs, but does not itself perform, a future amendment pass to `SD-001` (primary — one new major Section, per the Constitutional Home Resolution) and, where the migration exercise finds it warranted, a minor cross-reference in `ARCH-000 §8` and a new tracked entry in `SER-001`. `PE-001`, `RTA-001`, `CAP-001`, `URA-001`, `CMD-001`, `IMP-001`, and `WP-REG-001` are unaffected by this ADR.
**Affected Code:** None. This ADR is constitutional and implementation-neutral; it authorizes no code, API, schema, screen, widget, or engineering pattern.

---

## 1. Context

The Release D Initiation Assessment (session record, preceding this ADR) found that a mandatory dimension of `CLAUDE.md §20`'s own Vertical Slice Requirement — Enterprise Experience — had no constitutional grounding for AI-native content, blocking responsible chartering of `C-094` or any Release D capability. An initial framing of this gap as "Conversational Interfaces" was explicitly corrected by the Repository Owner: *"AUREX is an AI-Native Enterprise Operating System. It is NOT a chatbot. Conversation is only one possible Enterprise Experience."* The subsequent AI-Native Enterprise Experience Constitutional Discovery reviewed twenty-seven named candidate concepts (Conversational Experiences, Executive/Enterprise Copilot, AI Workspace Experiences, Agent Collaboration, Human Approval/Override, Progressive Disclosure, Evidence Presentation, and others) against the existing repository and found the gap real but narrower than first assumed: `SD-001` already owns and has realized several individual presentation contracts relevant to AI-originated content (Progressive Disclosure, `SD-001-021`; the Evidence Panel, `SD-001-020`; Explainability, `SD-001 LAW-26`; the Action Center, `SD-001-043`) — but no constitutional framework existed to state how these already-owned contracts compose for AI-Native content specifically, how accountability is preserved when AI-originated content is presented, or how such presentation relates to Workspace navigation and the Capability layer.

A six-concept Constitutional Design Workshop resolved this gap concept by concept, each with alternatives presented and one decision approved before the next began, mirroring the discipline `ADR-020`'s own workshop already established. A Constitutional Compatibility Validation checked all six decisions against `ARCH-000`, `CAP-001`, `CMD-001`, `RTA-001`, `SD-001`, `SD-002`, `PE-001`, `URA-001`, `SER-001`, `IMP-001`, and `CLAUDE.md`, finding zero conflicts and one minor, non-blocking clarification (formal ratification of the Framework's own name, resolved by this ADR, §2 below). A Constitutional Home Resolution then determined, using `SD-001`'s own demonstrated fifteen-Section structure and `IMP-001 §13.17`'s own sibling-layer precedent as direct evidence, that the Framework belongs inside `SD-001` as a new major Section — not a new constitutional document — closing the one remaining open question before this ADR could be responsibly authored.

**Relationship to existing `SD-001` ownership:** this ADR does not transfer, dilute, or duplicate `SD-001`'s existing constitutional ownership of Presentation Architecture (`CLAUDE.md §16`/`§20.2`). It specializes that ownership, exactly as `SD-001`'s own existing fifteen Sections each already specialize one coherent presentation sub-concern.

## 2. Decision

**The Framework is named the AI-Native Enterprise Experience Framework**, ratifying the working label used throughout the preceding discovery and workshop as the term of record — the one open item the Compatibility Validation identified, resolved here rather than left implicit.

### Decision 1 — AI-Native Experience Definition & Scope

AI-Native Experience is defined on two tiers. The outer, inclusive membership boundary is content-origin-based: any Enterprise Experience whose content originates, even partially, from an AI Runtime execution (`RTA-001 §13`) is AI-Native by definition. The inner boundary, determining what requires new Framework architecture, is pattern-novelty-based: only Experience whose interaction pattern itself — not merely its content — is structurally different from what `SD-001`'s existing contracts already serve requires new work. Content inside the outer boundary but outside the inner one (Evidence Presentation, Recommendations, Progressive Disclosure, AI-generated Enterprise Actions) is AI-Native by definition and already adequately served by existing `SD-001` contracts.

### Decision 2 — Experience–Runtime–Business Activity Accountability Boundary

AI-Native Experience remains within `SD-001`'s existing scope, gains no new Layer 1 constitutional status, never executes Business Activities, never owns canonical or durable state, and never becomes an independent accountability mechanism. It explicitly inherits the same non-accountable position `ADR-020` already established for Interaction relative to Conversation: accountability remains fixed exclusively with Business Activities (`RTA-001 §13.2`/`§13.3`), regardless of how many layers of presentation sit between a Business Activity and the AI Runtime output it presents.

### Decision 3 — Experience–Workspace Relationship

Workspace (`PE-001 §13.5`) provides Context; Conversation (`ADR-020`) provides Continuity — two independent, non-conflicting properties. AI-Native Experience is embedded within Workspace navigation, never a new parallel navigation layer, consistent with every prior capability's own delivery precedent and Decision 2's own augment-never-replace boundary. Whether a specific capability's own Conversation is Workspace-bound or portable across Workspaces remains that capability's own CRB/ERB decision, per `PE-001 §13.5`'s own existing delegation — this Framework does not override that delegation with a universal rule. A Conversation's own identity (`ADR-020`) carries no Workspace field of its own at the `RTA-001` layer, leaving that delegation genuinely open for each capability to exercise.

### Decision 4 — Experience Framework Composition Model

AI-Native Experience is a **Composition Framework**, mirroring `IMP-001 §13.17`'s own proven model at the presentation layer: a small set of universally mandatory rules (Business Activity accountability; Explainability; Runtime Event and Runtime Policy reuse with no parallel mechanism; Workspace embedding and Navigation reuse), a set of mandatory-reuse component contracts applied wherever content shape matches and never re-invented (Progressive Disclosure; the Evidence Panel; Confidence), and a set of capability-owned extension points pulled in only where a specific capability's own content requires them, each remaining governed by its own existing document (AI Session Management/Conversation/Interaction; Agent Collaboration; Human Approval/Human Override; Recommendations; Enterprise Intelligence; Enterprise Search). Enterprise Context (`ERG-001`) is inherited automatically, requiring no new Framework rule.

### Decision 5 — Relationship with Existing SD-001 Component Contracts

The Framework owns interaction **composition only** — never new interaction principles and never new interaction contracts. Progressive Disclosure, the Evidence Panel, Explainability, Confidence, the Action Center, Notification patterns, and every existing `SD-001` Law and Presentation Architecture principle are inherited unchanged. Recommendations and Notification patterns remain independently owned, capability- and mechanism-specific respectively. `SD-001` itself is the Framework's own host document, not superseded or paralleled by it. `PE-001` (Experience Architecture) is unaffected, its own relationship to the Framework already resolved by Decision 3.

### Decision 6 — Experience Framework Relationship to the Capability Layer

AI-Native Experience adopts a **content-triggered mandatory adoption** model, capability-agnostic: the Framework's mandatory tier (Decision 4) applies automatically and without exception whenever, and only when, a capability's own Experience presents content originating from an AI Runtime execution — regardless of that capability's own `CAP-001` domain, and not restricted to D-005 (Enterprise Intelligence). The Framework is not itself a `CAP-001` entry and owns no capability behavior. The governing chain is: **Framework (`SD-001`, capability-agnostic composition rules) → Capability (`CAP-001`, Business Intent, triggers the mandatory tier if AI-content is present) → CRB (capability-specific realization, per `PE-001 §13.5`) → ERB (enterprise-specific variation) → Work Package (charters implementation) → Implementation (`IMP-001`-governed build)** — each step consuming, never redefining, the step above it.

## 3. Constitutional Principles

The following principles are recorded as approved, binding constitutional statements, each traceable to the Decision above that established it:

1. AI-Native Experience is defined by content origin (inclusive) and pattern novelty (Framework-scope-determining) — two distinct tests serving two distinct questions, never conflated. *(Decision 1)*
2. AI-Native Experience carries no independent accountability, executes nothing, and owns no canonical state — accountability remains exclusively with Business Activities, inherited from `ADR-020`'s own precedent. *(Decision 2)*
3. Workspace provides Context; Conversation provides Continuity — independent properties, neither subsuming the other; Experience is embedded within Workspace navigation, never a parallel layer. *(Decision 3)*
4. The Framework is a Composition Framework: mandatory universal rules, mandatory-reuse component contracts, and capability-owned extension points — never a single specialization, never a mere descriptive collection, never a coordination authority with its own execution standing. *(Decision 4)*
5. The Framework owns composition only — it introduces zero new interaction principles and zero new interaction contracts; every existing `SD-001` contract it references is inherited unchanged. *(Decision 5)*
6. Adoption is content-triggered and capability-agnostic — mandatory the moment AI-Runtime-originated content is present, inapplicable otherwise, and never restricted to any single `CAP-001` domain. *(Decision 6)*

## 4. Constitutional Ownership

- **`SD-001` remains the constitutional owner** of the AI-Native Enterprise Experience Framework, exactly as it already owns Presentation Architecture generally (`CLAUDE.md §16`/`§20.2`).
- **No new Layer 1 concern is introduced.** `ARCH-000 §8`'s Architectural Dependency Model, which places `SD-001` and `RTA-001` as parallel Layer 1 entries, is unchanged.
- **No new Presentation Architecture document is created.** The Constitutional Home Resolution found, using `SD-001`'s own demonstrated fifteen-Section structure and `IMP-001 §13.17`'s own explicit sibling-layer precedent, that a standalone document would create the duplicate ownership `CLAUDE.md §16`'s single-owner assignment already exists to prevent.
- **The Framework is a specialization of `SD-001`**, structurally identical in shape to `SD-001`'s own existing fifteen Sections, each already specializing one coherent presentation sub-concern.

## 5. Explicit Non-Decisions

This ADR does not define, and none of the following is authorized, implied, or made engineerable by this ADR:

- Screens, widgets, UI layouts, chat interfaces, copilot interfaces, or any component
- APIs, endpoints, request/response contracts
- Frontend technology, frameworks, or libraries
- Database schemas, storage engines, physical repositories
- Runtime implementation, orchestration algorithms, or engineering patterns (deferred to a future, separately-authorized `IMP-001` specialization, mirroring how `ADR-020` preceded its own `IMP-001 §§13.26–13.38` specialization by one full governance cycle)
- Work Package chartering of any kind, including `WP-12`
- The genuinely novel Experience shapes the preceding Discovery found ungrounded — Conversational Experience presentation itself, Multi-Agent/Agent Collaboration Experience, interactive Human Approval/Override Experience, and Workspace/Cross-Workspace/Navigation-specific AI Experience — each remains its own future, separate constitutional concern, not resolved by this ADR, consistent with the Discovery's own finding that these are several independent concerns, not one

## 6. Traceability

| Workshop Concept | `SD-001` | `PE-001` | `RTA-001` | `CAP-001` | `ADR-020` |
|---|---|---|---|---|---|
| 1. Definition & Scope | New Section (host) | — | `§13.1` (outer-tier source) | — | — |
| 2. Accountability Boundary | New Section | — | `§13.1`–`§13.3`, `§13.6c` | — | Clarification 3 (direct precedent) |
| 3. Workspace Relationship | New Section | `§13.5` (Workspace/CRB/ERB, unchanged) | — | — | Decision 1 ("business continuity" language) |
| 4. Composition Model | New Section | — | — | — | — |
| 5. SD-001 Contract Relationship | `SD-001-020`/`021`/`LAW-26`/`§4`/`§7`/`§9` (unchanged, cited) | — | — | — | — |
| 6. Capability Layer Relationship | New Section | `§13.5` (CRB/ERB chain) | — | Domain-range discipline (confirmed inapplicable to the Framework itself) | — |

## 7. Consequences

- One new constitutional concept (the AI-Native Enterprise Experience Framework, as a `SD-001` specialization) and six principles now exist within `SD-001`'s ownership, extending but not modifying any of its fifteen existing Sections.
- No capability, entity, permission, navigation model, Business Activity, or existing `SD-001` contract is created, modified, or reassigned by this ADR. `C-094` remains Planned, unchanged.
- The Release D Initiation Assessment's own Enterprise Experience gap finding is now constitutionally addressed at the framework level — engineering the specific gaps that gap named (Conversational, Multi-Agent, Approval/Override presentation) remains future work, per §5 above.
- **Constitutional migration is required in a subsequent activity and is explicitly not performed by this ADR.** `SD-001` remains unmodified at the close of this ADR.

## 8. Migration Directives

The following repository documents are directed to be updated in a later, separately-authorized migration exercise — none is updated by this ADR:

- **`SD-001`** (primary) — one new major Section recording Decisions 1–6 and the six Constitutional Principles, continuing the existing `SD-001-XXX` principle numbering from `SD-001-111` onward (the sequence currently reaches `SD-001-110` in `Section 15`).
- **`ARCH-000`** — a possible minor cross-reference within `§8`'s own prose noting the Framework's existence as a `SD-001` specialization; the exact touch point was left unconfirmed by the Constitutional Home Resolution and is to be determined during migration, not asserted here.
- **`SER-001`** — one new Strategic Enhancement entry, mirroring `SE-061`'s own precedent for AI Session Management.
- **`PE-001`, `RTA-001`, `CAP-001`, `URA-001`, `CMD-001`, `IMP-001`, `WP-REG-001`** — no change directed.

## 9. Compatibility Statement

This ADR:

- **Preserves constitutional ownership** — `SD-001` retains sole ownership of Presentation Architecture; no other document's ownership is touched.
- **Preserves layering** — no new Layer 1 concern is introduced; `ARCH-000 §8`'s parallel Presentation/Runtime structure is unchanged.
- **Preserves reuse-before-create** — every principle and contract this Framework composes is reused from an existing owner; zero new principles, zero new contracts, zero new documents.
- **Preserves separation of concerns** — Runtime (`RTA-001`), Workspace (`PE-001`), Capability identity (`CAP-001`), and Presentation (`SD-001`) each remain exactly as they were.
- **Introduces no duplicate ownership** — the Constitutional Home Resolution's own evaluation of a standalone-document alternative found it would have created exactly the duplication this statement confirms was avoided.

## 10. Validation

- Every one of the six workshop decisions is represented in §2, in the terms already approved — none reworded to change its meaning.
- No new constitutional concept was introduced beyond the Framework's own name, ratified per the one open item the Compatibility Validation identified.
- No approved concept was modified.
- No engineering content was added — every reference to `IMP-001` in this ADR is a citation of precedent or a forward-pointer to future, separately-authorized work, never new engineering guidance.
- No migration was performed — `SD-001` and every other repository document remain exactly as they were before this ADR.

## 11. Status

**Accepted.**
