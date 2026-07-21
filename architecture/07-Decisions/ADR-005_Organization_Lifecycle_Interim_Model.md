# ADR-005 — Organization Lifecycle Interim Model, Pending Metadata Runtime

**Status:** Accepted
**Classification:** Architecture Governance / Runtime Dependency
**Decided by:** Repository owner (architecture governance authority), 2026-07-20, during WP-01 Implementation Readiness Assessment (IRA-001) review.
**Affected Documents:** None amended — SD-002 §7 (SD-002-051/052) remains the target architecture; this ADR records an approved interim implementation pending its infrastructure prerequisite.

---

## Context

SD-002-051 requires every business object's lifecycle to be metadata-driven, tenant-configurable, version-controlled, and governed through permissions. SD-002-052 requires every lifecycle transition to be event-driven. Both presume a Metadata Runtime and Event Bus (RTA-001 §9) that **do not exist anywhere in this repository** — confirmed repeatedly across WP-00, WP-00A, and IRA-001 (zero `MetadataEngine`/`MetadataRuntime` hits repo-wide; `observability.py`'s `publish_event()` is a log-only stand-in, not a real event bus).

WP-01's approved scope includes "Organization Lifecycle" (activation/suspension), which has no canonical state model defined anywhere — only a boolean `is_active` (AuthService) / `active_flag` (Master Technical Architecture's `organization_master`).

## Decision

**The metadata-driven, event-sourced lifecycle defined by SD-002 §7 remains the target architecture** — this ADR does not weaken or replace that requirement.

**Until the Metadata Runtime is implemented, WP-01 shall use an interim lifecycle model** — a simple state representation (e.g., `ACTIVE` / `SUSPENDED`) implemented as an ordinary column, not a metadata-driven configuration — **with clearly documented extension points** marking exactly where a future Metadata Runtime integration replaces the interim mechanism.

This follows the same interim-implementation pattern already used and documented in WP-00 for `feature_flag_service.py` (interim vs. RTA-001's Metadata Runtime) and `observability.py` (interim vs. `Backend/Shared/Logging`/`Events`) — both accepted at WP-00's IC-001 certification.

## Rationale

Blocking WP-01 on a Metadata Runtime that has no scoped work package of its own would stall Organization Management indefinitely. WP-00 already established, and IC-001 certified, that a transparently-documented interim implementation — built to be mechanically replaceable, not a redesign, once the canonical infrastructure exists — is an acceptable and architecture-compliant pattern for exactly this situation.

## Consequences

- WP-01 implements Organization lifecycle as a plain status field/enum with application-level transition logic (Activate/Suspend Business Activities), not a metadata-driven state machine.
- Every lifecycle transition still publishes a Domain Event (via `observability.py`'s existing interim mechanism) and produces an audit record (SD-002-054's seven questions) — the interim scope applies to *how* lifecycle is modeled and configured, not to whether transitions are audited/observable, which remain mandatory per IMP-001 §6.3.
- Code implementing the interim lifecycle model must carry an explicit comment/docstring identifying it as interim and naming this ADR, mirroring `observability.py`'s and `feature_flag_service.py`'s existing self-documentation pattern.
- When a Metadata Runtime work package is planned, migrating Organization's lifecycle to it is that work package's scope, not a WP-01 obligation.

## Status

**Accepted**
