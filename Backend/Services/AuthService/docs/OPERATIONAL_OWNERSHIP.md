# Operational Ownership: AuthService

Governing work package: AUREX Platform Administrator Implementation Roadmap, WP-00
(Platform Bootstrap) — closes the "operational ownership confirmation" execution
prerequisite carried into WP-00's Implementation Readiness Checklist.

This document defines who is responsible for AuthService in operation. Per CLAUDE.md
§8 ("Each capability has one owning service"), AuthService is the single owning service
for the Identity, Access, Role & Permission, and Membership capabilities (C-001–C-003,
C-007). This document extends that architectural ownership to operational
responsibility: the role accountable for the service once it is running in an
environment, not just the code that implements it.

## Ownership model

AuthService is owned by the **Platform Engineering function** — the same organizational
function responsible for the Aurex Platform Administrator journey it exists to serve.
Ownership is defined by responsibility, not by named individuals, since this repository
does not assign engineers to teams; whichever team is designated Platform Engineering at
deployment time assumes the responsibilities below.

| Responsibility | Owner | Scope |
|---|---|---|
| Code changes, review, and merge | Platform Engineering | `Backend/Services/AuthService/**` |
| Architecture and canonical data model compliance | Architecture governance (per CLAUDE.md §16–19) | Constitutional/engineering documents in `architecture/` |
| Deployment and release | Platform Engineering | CI/CD pipeline (`.github/workflows/authservice-ci.yml`), environment promotion |
| Production incident response | Platform Engineering (first responder) | Service availability, `/health` and `/ready` failures, bootstrap failures |
| Database ownership | Platform Engineering | AuthService's own schema only — per CLAUDE.md §8, no other service may access it directly |
| Feature flag rollout decisions | Platform Engineering, in coordination with the Work Package owner introducing the flagged behavior | `Config/platform-config.yaml` `feature_flags` section |
| Credential rotation for bootstrap-seeded identities | Platform Engineering | `platform.admin@corpstage.com`, `admin@corpstage.com` |

## Escalation path

1. **Automated detection**: orchestrator (Kubernetes/ECS/equivalent) liveness probe
   against `/health` restarts an unhealthy instance automatically; readiness probe
   against `/ready` removes a not-ready instance from traffic without restarting it.
2. **First response**: Platform Engineering on-call investigates using
   `docs/RUNBOOK_BOOTSTRAP.md` for bootstrap-related failures, or standard
   database/infrastructure runbooks for connectivity failures reported via `/health`'s
   `dependencies.database` field.
3. **Escalation**: if the failure implicates the canonical architecture itself (a
   constitutional document conflict, not an operational fault), escalate to
   architecture governance per CLAUDE.md §16 — operational staff SHALL NOT resolve
   architecture conflicts by assumption.

## Change control

Operational ownership does not grant authority to change architecture. Per CLAUDE.md
§18–19, any operational finding that appears to require a new entity, table, API,
permission, or business rule must stop and be reported through the ADR process — it may
not be resolved as an operational workaround.

## Review cadence

This document is reviewed whenever a new Work Package changes AuthService's runtime
footprint (new endpoints, new background processes, new external dependencies) and, at
minimum, at the start of each subsequent Work Package in the Aurex Platform
Administrator roadmap that touches this service.
