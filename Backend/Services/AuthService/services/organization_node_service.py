"""
WP-04 — Enterprise Structure Management (C-005).

Business Activities implemented here:
  BA-01 Establish Organization Node (ERB-C005-01 / EX-C005-01, -02 per
  PE-001-C005; ERG-001-02/03).
  BA-02 Understand Structural Position (ERB-C005-02 / EX-C005-03 per
  PE-001-C005).

Realizes CAP-001 C-005 per IRA-004's Structural-Identity-subset scope
(§9/§11). PE-001-C005 itself governs the experience layer only and
states no domain Business Rule for either a minimal Establish or a
minimal View (IRA-004 §5) — BA-01's actual governing rules are
ERG-001-02 (Bounded Context Separation Within EnterpriseNode) and
ERG-001-03 (Node-to-Membership Linkage). Follows IMP-001 §6.3's
Business Activity Lifecycle (Request -> Validation -> Business Rule
Execution -> Business Object Update -> Domain Event Publication ->
Audit Recording -> Response), reusing OrganizationService.establish()'s
exact duplicate-check-then-create pattern (WP-01), including the same
IntegrityError race-closing catch OrganizationService's own docstring
documents (uq_organization_nodes_node_code, WP-03 BA-01's own
constraint).

BA-02 reuses OrganizationService.get_details()'s exact read-only shape
(WP-01): no audit record or domain event, on the same basis already
established for every prior WP's own first read-side Business Activity.
EX-C005-03's own Purpose text ("understand surrounding structural
context and position... relationships") is only partially realized
here — this Business Activity returns a single OrganizationNode's own
Structural Identity fields; traversing "surrounding relationships"
requires `organization_hierarchy`, which does not exist yet (deferred,
TD-045, the same disclosed-scoping-decision class as BA-01's own
TD-043).
"""

from __future__ import annotations

from uuid import UUID

from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from models.organization_node import OrganizationNode
from repositories.organization_node_repository import OrganizationNodeRepository
from schemas.organization_node import EstablishOrganizationNodeRequest
from observability import record_audit, publish_event, AuditStatus


class OrganizationNodeService:
    """Business Activity orchestrator for Enterprise Structure Management (WP-04)."""

    def __init__(self, organization_node_repo: OrganizationNodeRepository) -> None:
        self.organization_node_repo = organization_node_repo

    async def establish(
        self, request: EstablishOrganizationNodeRequest, actor_id: str | None = None
    ) -> OrganizationNode:
        """
        Business Activity: Establish Organization Node (BA-01).

        Business Rule (ERG-001-02): node_code must be unique
        platform-wide, enforced both here (for a clean 409) and by the
        database's uq_organization_nodes_node_code constraint (already
        in place since WP-03 BA-01) as a second line of defense against
        a concurrent duplicate request.

        Only Structural Identity fields are persisted (IRA-004 §9/§11):
        node_code, node_name, node_type, legal_entity_name,
        business_unit, sector, operational_status, effective_from,
        effective_to. active_flag defaults to True (model default),
        mirroring how Organization's own establish() leaves its
        equivalent default untouched. geography_id, parent_available_
        flag, and the materiality/risk/scenario/passport scores are not
        accepted here — deferred per TD-043, not silently dropped.
        """
        existing = await self.organization_node_repo.get_by_code(request.node_code)
        if existing is not None:
            record_audit(
                action="ESTABLISH_ORGANIZATION_NODE",
                resource=f"organization_node:{request.node_code}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "node_code already exists"},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"An organization node with code '{request.node_code}' already exists.",
            )

        try:
            organization_node = await self.organization_node_repo.create(
                {
                    "node_code": request.node_code,
                    "node_name": request.node_name,
                    "node_type": request.node_type,
                    "legal_entity_name": request.legal_entity_name,
                    "business_unit": request.business_unit,
                    "sector": request.sector,
                    "operational_status": request.operational_status,
                    "effective_from": request.effective_from,
                    "effective_to": request.effective_to,
                }
            )
            await self.organization_node_repo.session.flush()
        except IntegrityError:
            # Closes the race window between the pre-check above and this
            # insert, the identical concurrent-duplicate defense
            # OrganizationService.establish() (WP-01) already documents.
            await self.organization_node_repo.session.rollback()
            record_audit(
                action="ESTABLISH_ORGANIZATION_NODE",
                resource=f"organization_node:{request.node_code}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "node_code already exists (concurrent creation)"},
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"An organization node with code '{request.node_code}' already exists.",
            )

        record_audit(
            action="ESTABLISH_ORGANIZATION_NODE",
            resource=f"organization_node:{organization_node.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={"node_code": organization_node.node_code},
        )
        publish_event(
            "ORGANIZATION_NODE_ESTABLISHED",
            {
                "organization_node_id": str(organization_node.id),
                "node_code": organization_node.node_code,
                "node_name": organization_node.node_name,
                "node_type": organization_node.node_type,
            },
        )
        return organization_node

    async def get_details(self, organization_node_id: UUID) -> OrganizationNode:
        """
        Business Activity: Understand Structural Position (BA-02).

        Read-only — no audit record or domain event, on the same basis
        already established for Organization's own read-side Business
        Activity (OrganizationService.get_details() does not audit
        either; only the write path, establish(), does). Reuses
        BaseRepository.get_by_id() via OrganizationNodeRepository as-is
        — no new repository method required.

        Realizes only the single-node half of EX-C005-03's own Purpose
        ("understand surrounding structural context and position").
        "Surrounding relationships" requires `organization_hierarchy`,
        which does not exist yet — deferred, not silently claimed as
        satisfied (TD-045).
        """
        organization_node = await self.organization_node_repo.get_by_id(organization_node_id)
        if organization_node is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No organization node exists with id '{organization_node_id}'.",
            )
        return organization_node
