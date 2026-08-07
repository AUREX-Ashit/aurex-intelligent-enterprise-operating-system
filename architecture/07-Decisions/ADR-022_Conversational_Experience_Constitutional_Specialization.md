# ADR-022 — Conversational Experience: Constitutional Specialization of the AI-Native Enterprise Experience Framework

**Status:** Accepted
**Classification:** Architecture Governance / Presentation Architecture Extension (specialization of an existing extension point)
**Decided by:** Repository owner (architecture governance authority), through the Conversational Experience Constitutional Design Workshop, its own Concept Discovery Report, and a Constitutional Placement Recommendation (session record, 2026-08-07) — the same decision-authority pattern `ADR-006` through `ADR-021` already established. **Disclosure, carried forward from `ADR-020`/`ADR-021`'s own precedent:** this ADR's preceding discovery, workshop, validation, and placement passes were conducted in the same session as this ADR's own authoring and were not independently reviewed by a party uninvolved in producing them, unlike the fresh-context reviewer discipline `CLAUDE.md §19.7` requires for Work Package certification. This ADR is the first and only artifact from that process persisted to the repository — no intermediate discovery/workshop/validation document exists as a separate repository file.
**Affected Documents:** None edited by this ADR. This ADR records three constitutional decisions and directs, but does not itself perform, a future amendment pass extending `SD-001 §16` (new principles continuing from `SD-001-119`) and a new `SER-001` entry. **`ARCH-000` requires no amendment** — the existing "Experience governance" row (added per `ADR-021`) already covers this specialization, since it extends `SD-001 §16` rather than establishing a new governance dimension. `RTA-001`, `PE-001`, `CAP-001`, `URA-001`, `CMD-001`, `IMP-001`, and `WP-REG-001` are unaffected.
**Affected Code:** None. This ADR is constitutional and implementation-neutral; it authorizes no code, API, schema, screen, component, or engineering pattern.

---

## 1. Context

The Release D Readiness Assessment (session record, preceding this ADR) found that `ADR-020` (AI Session Management) and `ADR-021` (AI-Native Enterprise Experience Framework), while resolving the backend and compositional layers required for AI-native interaction, left one narrow, explicitly-disclosed gap: `SD-001-113`'s own inner-boundary test classifies Conversational Experience as content whose interaction pattern is not already served by existing `SD-001` contracts, and `ADR-021 §5` named it directly as a genuinely novel Experience shape not resolved by that ADR. `C-094`'s own Business Intent — "Manage AI interactions" — is the capability this gap would first be exercised by, and `CLAUDE.md §20.4`'s Demonstrability standard cannot be satisfied for it without closing this gap first.

A Concept Discovery Report searched the repository directly (beyond citations already established this session) for competing or duplicate conversational/copilot material and found none: `RTA-001 §13.15a` owns the Conversation/Interaction runtime constructs (unaffected by this ADR); `SD-001 §16` owns the Experience Framework's own composition rules and already named "AI Session Management/Conversation/Interaction" as one of its own extension points (`SD-001-116`) without defining its realization; `SER-001 SE-037`/`SE-050` track `C-094` and "Executive Copilot" as future work, not architecture. No duplicate ownership was found anywhere.

A three-concept Constitutional Design Workshop resolved the gap, each concept presented with alternatives and amended by the Repository Owner before the next began — mirroring, and in each of its three concepts refining, the discipline `ADR-020`'s and `ADR-021`'s own workshops established. A Constitutional Placement Recommendation then determined, using the Repository Owner's own approved Concept 1 language as direct evidence ("Conversational Experience remains an SD-001 specialization **of** the AI-Native Enterprise Experience Framework"), that this specialization extends `SD-001 §16` rather than becoming a new Section or document — correcting an earlier, less precise tentative placement.

**Relationship to existing ownership:** this ADR does not transfer, dilute, or duplicate `SD-001`'s ownership of Presentation Architecture, `RTA-001`'s ownership of Conversation/Interaction, or `ADR-021`'s own Experience Framework decisions. It specializes one extension point that Framework already named.

## 2. Decision

### Decision 1 — Conversational Experience Definition and Structural Anchor

A Conversational Experience presents exactly one Conversation. The Conversation is composed of one or more Interactions as defined by `ADR-020`. The presentation model shall preserve the identity, ordering, and accountability of those Interactions. The visual representation of an Interaction (including turns, streaming, progressive rendering, or other presentation constructs) is governed by the Conversational Experience specialization and is not constitutionally required to maintain a strict one-to-one visual mapping with the Interaction.

### Decision 2 — Reuse of Existing Constitutional Constructs

Whenever a Conversational Experience presents behavior that is already governed by an existing constitutional construct, the Experience shall compose and surface that construct rather than introducing an independent presentation-specific mechanism. The Experience Framework shall remain a composition layer, never a source of parallel runtime behavior. Human approval pauses shall compose the existing Ask User Gate (`RTA-001 §13.12a`). Multi-agent visualization shall compose the existing Cross-Lifecycle Agent Handoff (`ADR-020` Decision 5). Any future constitutional construct introduced elsewhere in the repository shall automatically fall under this same reuse principle, without requiring amendment to this specialization or to `ADR-021`.

### Decision 3 — Contract Composition Remains Interaction-Scoped

Contract composition remains Interaction-scoped. A Conversation does not own Evidence, Confidence, Explainability, Progressive Disclosure, or any other presentation contract. These remain properties of individual Interaction outputs. A Conversation provides continuity and ordering only, never presentation aggregation. Every Interaction independently composes the existing `SD-001` contracts (`SD-001-117`). Any future Conversation-level roll-up, summary, dashboard, analytics, or similar presentation shall be treated as a separate capability requiring its own constitutional justification, never implicitly introduced through this specialization.

## 3. Constitutional Principles

1. Accountability and structural identity remain fixed at the Interaction; visual representation is not constitutionally constrained beyond preserving that identity, ordering, and accountability. *(Decision 1)*
2. The Experience layer never becomes a source of parallel runtime or presentation-specific behavior — any behavior already governed by an existing constitutional construct must be composed, never re-implemented, and this obligation extends automatically to constructs not yet introduced. *(Decision 2)*
3. Conversation-level continuity and Interaction-level presentation contracts are distinct, non-overlapping properties — a Conversation is never a presentation-aggregation unit. *(Decision 3)*
4. **Constitutional ownership is determined by architectural responsibility, not by the number of workshops or decisions required to discover that responsibility.** An architectural specialization shall not become a new top-level constitutional concern solely because its internal design required an independent constitutional workshop. This principle is recorded here as a general governance statement, not specific to this ADR alone — it is the same reasoning that already produced one `RTA-001` extension from `ADR-020`'s five workshop concepts, one `SD-001` extension from `ADR-021`'s six workshop concepts, and one `SD-001 §16` extension, rather than a new Section, from this ADR's own three.

## 4. Constitutional Ownership

- **`SD-001` remains the constitutional owner.** This specialization extends `§16` — it is not a new major Section and not a new constitutional document.
- **`ARCH-000` requires no amendment.** The existing "Experience governance" row (`§7c`, added per `ADR-021`) already covers this specialization in full, since it names `SD-001 §16` generally rather than a specific principle range within it.
- **`RTA-001`, `PE-001`, and `CAP-001` ownership is unchanged.** Conversation/Interaction remain `RTA-001`'s own runtime constructs; Workspace/CRB/ERB remain `PE-001`'s own; `C-094`'s identity remains `CAP-001`'s own.
- **No new Layer 1 concern is introduced.**

## 5. Explicit Non-Decisions

This ADR does not define, and none of the following is authorized, implied, or made engineerable by this ADR:

- Screens, widgets, UI layouts, chat interfaces, or any component
- APIs, endpoints, request/response contracts
- Frontend technology, frameworks, or libraries
- Database schemas, storage engines, physical repositories
- Streaming mechanics, progressive-rendering algorithms, or any runtime implementation (deferred to a future, separately-authorized `IMP-001` specialization, mirroring how `ADR-020` and `ADR-021` each preceded their own engineering specializations by one full governance cycle)
- Work Package chartering of any kind, including `WP-12`
- Any Conversation-level roll-up, summary, dashboard, or analytics capability (per Decision 3, explicitly reserved for its own future constitutional justification)
- Multi-agent visualization's own concrete presentation, or human-approval-pause's own concrete presentation — only the obligation to compose the existing Handoff and Ask User Gate constructs is decided here

## 6. Traceability

| Decision | `SD-001` | `RTA-001` | `ADR-020` | `ADR-021` |
|---|---|---|---|---|
| 1. Definition & Structural Anchor | `§16` extension (new principles) | `§13.15a` (Conversation/Interaction, reused) | Accountability, inherited | `SD-001-113`, `SD-001-116` (named extension point) |
| 2. Construct Reuse | `§16` extension | `§13.12a` (Ask User Gate) | Decision 5 (Handoff) | `SD-001-117` (reuse discipline, generalized) |
| 3. Interaction-Scoped Composition | `§16` extension | — | Conversation/Interaction distinction, reused | `SD-001-117` (scope confirmed) |

## 7. Consequences

- Three new principles now exist within `SD-001 §16`'s own ownership, extending but not restructuring it — no new Section, no new document.
- `ADR-021`'s own "Experience Framework is a composition layer" principle is reaffirmed and generalized (Decision 2), now binding on every future constitutional construct automatically.
- The Release D Readiness Assessment's single remaining blocker is now constitutionally addressed. Engineering the specialization (an `IMP-001` pass, mirroring `§13.26–38` and `§13.39–53`) and any subsequent `WP-12` chartering remain future, separately-authorized activities.
- **Constitutional migration is required in a subsequent activity and is explicitly not performed by this ADR.** `SD-001` remains unmodified at the close of this ADR.

## 8. Migration Directives

- **`SD-001`** — extend `§16` with new principles continuing from `SD-001-119`, recording Decisions 1–3 and Constitutional Principles 1–4 above.
- **`SER-001`** — one new entry, mirroring `SE-064`/`SE-065`'s own precedent — not inherited silently under `SE-065`, whose own Remarks column already discloses this as a separately-gapped item.
- **`ARCH-000`, `RTA-001`, `PE-001`, `CAP-001`, `URA-001`, `CMD-001`, `IMP-001`, `WP-REG-001`** — no change directed.

## 9. Compatibility Statement

This ADR:

- **Preserves constitutional ownership** — `SD-001` retains sole ownership; no other document's ownership is touched.
- **Preserves layering** — no new Layer 1 concern; `ARCH-000 §8`'s parallel structure unchanged.
- **Preserves reuse-before-create** — every principle composes an existing construct (`§13.15a`, `§13.12a`, `ADR-020` Decision 5, `SD-001-117`); zero new runtime or presentation mechanisms.
- **Preserves separation of concerns** — Runtime, Workspace, Capability identity, and Presentation each remain exactly as they were.
- **Introduces no duplicate ownership** — confirmed by the Constitutional Placement Recommendation's own evaluation of, and rejection of, both a new Section and a standalone document.

## 10. Validation

- Every one of the three workshop decisions is represented in §2, in the terms already approved, including each Repository Owner amendment, none reworded to change its meaning.
- No new constitutional concept was introduced beyond this specialization's own extension of an already-named slot and the general governance principle (§3.4) explicitly requested for recording.
- No approved concept was modified.
- No engineering content was added.
- No migration was performed — `SD-001` and every other repository document remain exactly as they were before this ADR.

## 11. Status

**Accepted.**
