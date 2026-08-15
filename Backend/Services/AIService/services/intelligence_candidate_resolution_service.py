# services/intelligence_candidate_resolution_service.py
"""
WP-14 BA-03 — Resolve Enterprise Intelligence Candidate (Convergence
Decision). A separate service class from BA-02's own
`IntelligenceCandidateService` — mirrors WP-11's own established
precedent of one service class per Business Activity sharing a resource
family (`SearchIndexConfigurationService` for BA-01,
`ContentRegistrationService` for BA-03, both against `vector_index_
registry`/`evidence_registry`) — chosen specifically so BA-02's own
existing service constructor is never touched.

Gated by `PLATFORM_ADMIN` at the router — Binding 5 names "a Governance
Manager," which has no seeded role anywhere in this repository
(`ADR-002`/`TD-021`-class gap), same interim measure this repository
already uses platform-wide (`IRA-014 §10`).

Semantic Matching (`IRA-014 §6`'s own "invokes Semantic Matching
(`RTA-001 §13.9c` Reasoning Contract call) before persisting a
NEW_CDE_CREATED outcome") is implemented as a disclosed, non-AI
placeholder — `RTA-001 §13.9c` itself states it "defines no reasoning
algorithm... anywhere in this document," and no real Reasoning Engine is
wired anywhere in this platform (`TD-133`, WP-12's own disclosed,
platform-wide gap). This service performs a real, functioning
case-insensitive exact-name match against the caller's own existing
Tenant CDEs — the only real, populated data source available
(`metric_registry`, the Global canonical library Binding 3 actually
describes matching against, has zero physical rows anywhere in this
repository) — mirroring WP-11's own "disclosed fixed-size placeholder"
precedent (`services/content_registration_service.py::_fixed_size_chunks`)
exactly: a real code path always executes, its own limitation is
disclosed, not silently hidden behind a fabricated AI result.

Confidence (`SD-002-025`) is left `NULL` on the created Evidence row —
`confidence_scoring_registry` has no physical model anywhere in this
repository (same disposition already established for BA-01's
`governing_policy_id` and BA-04's `confidence_rule_id`) — registered as
new Technical Debt (`TD-144`) rather than fabricated.

**Gate 1 remediation, Finding 1 (concurrent double-resolution race):**
`resolve()` no longer decides `PENDING`-vs-already-resolved from the
`candidate` object `get_by_id` returned — that read is stale the instant
a concurrent request commits. The actual guard is
`UnclassifiedIntelligenceRegistryRepository.claim_for_resolution`, an
atomic, database-enforced `UPDATE ... WHERE resolution_status =
'PENDING'` — see that method's own docstring for the full mechanism. No
side-effecting row (`customer_metric_registry`, `evidence_registry`) is
ever created before the claim succeeds, so a losing concurrent request
creates zero artifacts, never an orphan.

**Gate 1 remediation, Finding 2 (`semantic_match_result_metric_id`
semantics):** this column is contractually reserved for a **Global**
`metric_registry` match (`Master_Technical_Architecture.md`'s own
`COMMENT ON COLUMN`) — it is now always written as `None`/`NULL`, never
populated with a Tenant `customer_metric_id`, correcting a column-
semantics violation the Gate 1 independent certification found. The
real, functioning same-organization Tenant-CDE duplicate heuristic keeps
running (`TD-145`) and is still surfaced to the caller, but only via the
response's own `same_organization_duplicate_customer_metric_id` field —
never persisted into this LOCKED, Global-only column.

**Gate 2 V&V remediation, Finding 1 (unhandled 500 on duplicate
`metric_code`):** the independent V&V Audit found that an ordinary,
non-concurrent `NEW_CDE_CREATED` resolution using a `metric_code` already
present for the caller's own Organization raised an uncaught
`IntegrityError` (`uq_customer_metric_registry_org_code`), reaching the
caller as a bare `500`. `CLAUDE.md §19.8.5` prohibits deferring broken,
ordinary-use-reachable functionality as Technical Debt, so this is fixed,
not disclosed-and-left: the `customer_metric_repo.create()` call is now
wrapped in a narrow `except IntegrityError`, rolling back the whole
transaction (which also reverts `claim_for_resolution`'s own UPDATE,
returning the candidate to `PENDING`) and returning `409 Conflict` — see
the exception handler's own comment for why the catch is safely narrow.
`IRA-014 §6`'s own BA-03 row does not specify what should happen on this
exact collision (no "resolve to the existing metric" or equivalent rule
is documented anywhere), so no richer business rule is invented here;
`409 Conflict` reuses this same endpoint's own already-established
response shape for a resolution conflict. Disclosed as `TD-149`.

**Post-remediation audit finding (independent Gate 4 review):** `resolve()`
previously called `record_audit()` only on the success path. All three
failure/conflict branches (404 not-found; 409 already-resolved; 409
duplicate `metric_code`) now also record an audit entry, using
`AuditStatus.DENIED` — mirroring `ConversationService.close()`'s own
established precedent exactly (`services/conversation_service.py`: a 404
not-found and a 409 invalid-transition are both `DENIED`, not `FAILED`).
`AuditStatus.FAILED` is reserved, by this repository's own established
convention (`services/interaction_service.py`'s `except Exception` block),
for an unexpected system-level fault during an operation expected to
succeed — none of these three outcomes is that; each is a foreseeable,
correctly-handled business-rule rejection, so `DENIED` is the correct
status for all three, not `FAILED`. No new audit field, framework, or
event architecture was introduced — only additional calls to the
already-imported `record_audit()`.
"""
from __future__ import annotations

import uuid

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from observability import AuditStatus, record_audit
from repositories.customer_metric_repository import CustomerMetricRegistryRepository
from repositories.search_repository import EvidenceRegistryRepository
from repositories.unclassified_intelligence_repository import UnclassifiedIntelligenceRegistryRepository
from schemas.unclassified_intelligence import (
    ResolveIntelligenceCandidateRequest,
    ResolvedIntelligenceCandidateResponse,
)


class IntelligenceCandidateResolutionService:
    """Business Activity orchestrator for BA-03."""

    def __init__(
        self,
        db_session: AsyncSession,
        candidate_repo: UnclassifiedIntelligenceRegistryRepository,
        customer_metric_repo: CustomerMetricRegistryRepository,
        evidence_repo: EvidenceRegistryRepository,
    ) -> None:
        self.db = db_session
        self.candidate_repo = candidate_repo
        self.customer_metric_repo = customer_metric_repo
        self.evidence_repo = evidence_repo

    async def resolve(
        self,
        organization_id: uuid.UUID,
        actor_id: uuid.UUID,
        unclassified_id: uuid.UUID,
        request: ResolveIntelligenceCandidateRequest,
    ) -> ResolvedIntelligenceCandidateResponse:
        candidate = await self.candidate_repo.get_by_id(organization_id, unclassified_id)
        if candidate is None:
            record_audit(
                action="RESOLVE_INTELLIGENCE_CANDIDATE",
                resource=f"unclassified_intelligence:{unclassified_id}",
                status=AuditStatus.DENIED,
                actor_id=str(actor_id),
                tenant_id=str(organization_id),
                metadata={"reason": "candidate not found or not visible to this organization"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No Intelligence Candidate with that id is visible to your own Organization.",
            )

        # Gate 1 remediation, Finding 1: the atomic claim — not the
        # `candidate` object's own possibly-stale `resolution_status` — is
        # the sole source of truth for "may this request proceed." No
        # side-effecting row is created until this returns True.
        claimed = await self.candidate_repo.claim_for_resolution(
            organization_id,
            unclassified_id,
            resolution_status=request.outcome,
            resolved_by_user_id=actor_id,
        )
        if not claimed:
            record_audit(
                action="RESOLVE_INTELLIGENCE_CANDIDATE",
                resource=f"unclassified_intelligence:{unclassified_id}",
                status=AuditStatus.DENIED,
                actor_id=str(actor_id),
                tenant_id=str(organization_id),
                metadata={"reason": "candidate already resolved"},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This candidate was already resolved — a candidate may be resolved exactly once.",
            )

        resolved_metric_id: uuid.UUID | None = None
        resolved_customer_metric_id: uuid.UUID | None = None
        semantic_match_attempted = None
        same_organization_duplicate_customer_metric_id: uuid.UUID | None = None
        evidence_id: uuid.UUID | None = None

        if request.outcome == "DISCARDED":
            # Binding 5: "mark not relevant and discard." No CDE, no
            # Evidence — SD-002-041 governs CDEs, not a discard act. This is
            # an implementation-time reading of a genuine IRA-014 §6 BA-03
            # tension against that same row's own Acceptance Criteria text
            # ("every resolved outcome carries an Evidence reference") —
            # disclosed, not silently resolved; see TD-148.
            pass

        elif request.outcome == "MAPPED_TO_EXISTING":
            resolved_metric_id = request.metric_id
            evidence = await self.evidence_repo.create_linked(
                organization_id=organization_id,
                linked_entity_type="metric_registry",
                linked_entity_id=request.metric_id,
                evidence_source=candidate.source_document_reference,
                file_reference=candidate.source_page_section,
            )
            evidence_id = evidence.evidence_id

        else:  # NEW_CDE_CREATED
            existing_match = await self.customer_metric_repo.find_same_org_by_exact_name(
                organization_id, request.metric_name
            )
            semantic_match_attempted = True
            if existing_match is not None:
                # Gate 1 remediation, Finding 2: this is a same-organization
                # Tenant-CDE duplicate, never a Global metric_registry match
                # — it must never be written into `semantic_match_result_
                # metric_id`/`semantic_match_score` (both LOCKED, Global-only
                # columns). Surfaced only via the response's own dedicated
                # field; see module docstring.
                same_organization_duplicate_customer_metric_id = existing_match.customer_metric_id

            try:
                new_metric = await self.customer_metric_repo.create(
                    organization_id=organization_id,
                    requested_by_user_id=actor_id,
                    metric_name=request.metric_name,
                    metric_code=request.metric_code,
                    metric_description=request.metric_description,
                    unit_of_measure=request.unit_of_measure,
                    formula_logic=request.formula_logic,
                    semantic_match_attempted_flag=True,
                    semantic_match_result_metric_id=None,
                    semantic_match_score=None,
                    semantic_match_rejected_reason=request.semantic_match_rejected_reason,
                )
            except IntegrityError:
                # Gate 2 V&V remediation, Finding 1: `create()` performs
                # exactly one INSERT into customer_metric_registry, and that
                # INSERT is subject to exactly one realistically triggerable
                # constraint — uq_customer_metric_registry_org_code, UNIQUE
                # (organization_id, metric_code). Every other constraint on
                # this table (the three CHECKs, the PK) is satisfied by
                # construction: cde_tier/approval_status are fixed defaults
                # this call never overrides, and customer_metric_id is a
                # fresh uuid4. A bare `except IntegrityError` here is
                # therefore a safe, specific match for the metric_code
                # conflict, not a blanket swallow of unrelated database
                # errors — the same narrow-catch shape already established
                # in this repository's own AuthService precedent
                # (OrganizationService.establish/RoleService.create, both
                # `except IntegrityError` with no message inspection, for
                # the identical reason: one INSERT, one realistic
                # constraint). Rolling back the whole transaction also
                # reverts claim_for_resolution's own UPDATE (same
                # transaction, never yet committed), returning the candidate
                # to PENDING so a retry with a different metric_code is
                # possible — no partial customer_metric_registry row is
                # left, and evidence_repo.create_linked below is never
                # reached, so no orphan Evidence row either. IRA-014 §6's
                # own BA-03 row is silent on what should happen when a
                # caller's chosen metric_code collides with an existing
                # Tenant CDE — no document specifies "resolve to the
                # existing metric" or any other business rule for this
                # case, so that richer behaviour is not invented here.
                # 409 Conflict is not a new response shape for this
                # endpoint (the already-resolved-candidate case already
                # uses it) and is the same "existing contractually
                # supported conflict/validation response" this repository
                # already uses platform-wide for a unique-constraint
                # collision; see TD-149.
                await self.db.rollback()
                record_audit(
                    action="RESOLVE_INTELLIGENCE_CANDIDATE",
                    resource=f"unclassified_intelligence:{unclassified_id}",
                    status=AuditStatus.DENIED,
                    actor_id=str(actor_id),
                    tenant_id=str(organization_id),
                    metadata={"reason": "duplicate metric_code within organization", "metric_code": request.metric_code},
                )
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=(
                        f"A Customer Metric with code '{request.metric_code}' already exists in your "
                        "own Organization. Resolve this candidate as MAPPED_TO_EXISTING against the "
                        "existing metric instead, or choose a different metric_code."
                    ),
                )
            resolved_customer_metric_id = new_metric.customer_metric_id

            evidence = await self.evidence_repo.create_linked(
                organization_id=organization_id,
                linked_entity_type="customer_metric_registry",
                linked_entity_id=new_metric.customer_metric_id,
                evidence_source=candidate.source_document_reference,
                file_reference=candidate.source_page_section,
            )
            evidence_id = evidence.evidence_id

        await self.candidate_repo.attach_resolution_target(
            candidate,
            resolved_metric_id=resolved_metric_id,
            resolved_customer_metric_id=resolved_customer_metric_id,
        )

        await self.db.commit()
        await self.db.refresh(candidate)

        record_audit(
            action="RESOLVE_INTELLIGENCE_CANDIDATE",
            resource=f"unclassified_intelligence:{candidate.unclassified_id}",
            status=AuditStatus.SUCCESS,
            actor_id=str(actor_id),
            tenant_id=str(organization_id),
            metadata={"outcome": request.outcome},
        )

        return ResolvedIntelligenceCandidateResponse(
            unclassified_id=candidate.unclassified_id,
            resolution_status=candidate.resolution_status,
            resolved_by_user_id=candidate.resolved_by_user_id,
            resolved_at=candidate.resolved_at,
            resolved_metric_id=candidate.resolved_metric_id,
            resolved_customer_metric_id=candidate.resolved_customer_metric_id,
            semantic_match_attempted_flag=semantic_match_attempted,
            semantic_match_result_metric_id=None,
            semantic_match_score=None,
            same_organization_duplicate_customer_metric_id=same_organization_duplicate_customer_metric_id,
            evidence_id=evidence_id,
        )
