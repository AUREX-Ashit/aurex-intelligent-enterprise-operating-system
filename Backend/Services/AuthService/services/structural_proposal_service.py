"""
WP-04 BA-04 — Shape / Refine Proposed Structural Outcome (ERB-C005-04 /
EX-C005-05, -06 per PE-001-C005). Realizes POC-000001, the Proposed
Outcome Context Business Object registered by ADR-008 / IRA-004 §22.
EnterpriseNode-only v1 proposal-target scope per ADR-007.

Follows IMP-001 §6.3's Business Activity Lifecycle. Shape (EX-C005-05)
mirrors the create -> flush -> audit -> event shape every prior
Establish-type Business Activity uses, with two existence checks first
(structural_change_intent_id, target_organization_node_id) instead of
a duplicate check — this object has no natural business key, the same
disclosed difference BA-03 already established for Structural Change
Intent.

Refine (EX-C005-06) is a new pattern in this repository: it does not
update a row in place. It reads the current revision
(StructuralProposalRepository.get_current_revision()), transitions its
own status to SUPERSEDED (a status transition, not a content mutation
— proposed_outcome_description on that row is never altered), and
inserts a new row carrying the next revision_number with the revised
description, the same immutable structural_change_intent_id and
target_organization_node_id copied forward (BR-C005-004: every
revision SHALL remain traceable to the same originating Change
Intent). This realizes POC-000001's own registered append-only
Versioning Policy: no revision's own content is ever overwritten.

Deliberately does not implement VALIDATED or ARCHIVED (IRA-004 §22's
own registered Lifecycle Model, TD-053), does not persist Comparison
Context (TD-054), and exposes no read endpoint for Proposed Outcome
Context itself (TD-055, mirroring TD-051's own identical disposition
for Structural Change Intent). Concurrent Refine calls against the
same proposal_id are not guarded against a revision_number race
(TD-056).
"""

from __future__ import annotations

from uuid import UUID, uuid4

from fastapi import HTTPException, status

from models.structural_proposal import StructuralProposal, StructuralProposalStatus
from repositories.structural_proposal_repository import StructuralProposalRepository
from repositories.structural_change_intent_repository import StructuralChangeIntentRepository
from repositories.organization_node_repository import OrganizationNodeRepository
from schemas.structural_proposal import ShapeStructuralProposalRequest, RefineStructuralProposalRequest
from observability import record_audit, publish_event, AuditStatus


class StructuralProposalService:
    """Business Activity orchestrator for Shape / Refine Proposed Structural Outcome (WP-04 BA-04)."""

    def __init__(
        self,
        structural_proposal_repo: StructuralProposalRepository,
        structural_change_intent_repo: StructuralChangeIntentRepository,
        organization_node_repo: OrganizationNodeRepository,
    ) -> None:
        self.structural_proposal_repo = structural_proposal_repo
        self.structural_change_intent_repo = structural_change_intent_repo
        self.organization_node_repo = organization_node_repo

    async def shape_proposal(
        self, request: ShapeStructuralProposalRequest, actor_id: str | None = None
    ) -> StructuralProposal:
        """
        Business Activity: Shape Structural Proposal (BA-04, EX-C005-05).

        Required Context (EX-C005-05, verbatim): "Change Intent Context
        and current structural context" — both existence-checked before
        creation (404 if either does not exist), the same
        must-be-addressable-and-resolvable discipline ERG-001-03
        already established for Membership.home_node_id.

        Creates revision 1 of a new proposal: proposal_id equals the
        new row's own id (no separate header row/table). The id is
        generated explicitly here, rather than left to the model's own
        default=uuid.uuid4, because that default is not evaluated until
        flush — assigning proposal_id from a not-yet-flushed id would
        read back None.
        """
        structural_change_intent = await self.structural_change_intent_repo.get_by_id(
            request.structural_change_intent_id
        )
        if structural_change_intent is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No structural change intent exists with id '{request.structural_change_intent_id}'.",
            )

        organization_node = await self.organization_node_repo.get_by_id(
            request.target_organization_node_id
        )
        if organization_node is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No organization node exists with id '{request.target_organization_node_id}'.",
            )

        new_id = uuid4()
        proposal = await self.structural_proposal_repo.create(
            {
                "id": new_id,
                "proposal_id": new_id,
                "structural_change_intent_id": request.structural_change_intent_id,
                "target_organization_node_id": request.target_organization_node_id,
                "proposed_outcome_description": request.proposed_outcome_description,
                "revision_number": 1,
                "status": StructuralProposalStatus.CREATED.value,
            }
        )
        await self.structural_proposal_repo.session.flush()

        record_audit(
            action="SHAPE_STRUCTURAL_PROPOSAL",
            resource=f"structural_proposal:{proposal.proposal_id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={"revision_number": proposal.revision_number},
        )
        publish_event(
            "STRUCTURAL_PROPOSAL_SHAPED",
            {
                "proposal_id": str(proposal.proposal_id),
                "revision_id": str(proposal.id),
                "revision_number": proposal.revision_number,
            },
        )
        return proposal

    async def refine_proposal(
        self, proposal_id: UUID, request: RefineStructuralProposalRequest, actor_id: str | None = None
    ) -> StructuralProposal:
        """
        Business Activity: Refine Structural Proposal (BA-04, EX-C005-06).

        Required Context (EX-C005-06, verbatim): "Current proposal
        revision and unresolved proposal concerns" — this Business
        Activity realizes the "current proposal revision" half only;
        "unresolved proposal concerns" belongs to BA-06's own Review
        Context, not yet implemented.

        Append-only: the current revision's own content is never
        altered — only its status transitions to SUPERSEDED (EX-C005-05's
        own Invalidated Context: "Superseded proposal revisions are
        closed but retained in traceability"). structural_change_intent_id
        and target_organization_node_id are copied forward unchanged
        (BR-C005-004).
        """
        current = await self.structural_proposal_repo.get_current_revision(proposal_id)
        if current is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No structural proposal exists with proposal_id '{proposal_id}'.",
            )

        current.status = StructuralProposalStatus.SUPERSEDED.value

        next_revision = await self.structural_proposal_repo.create(
            {
                "proposal_id": current.proposal_id,
                "revision_number": current.revision_number + 1,
                "structural_change_intent_id": current.structural_change_intent_id,
                "target_organization_node_id": current.target_organization_node_id,
                "proposed_outcome_description": request.proposed_outcome_description,
                "status": StructuralProposalStatus.CREATED.value,
            }
        )
        await self.structural_proposal_repo.session.flush()

        record_audit(
            action="REFINE_STRUCTURAL_PROPOSAL",
            resource=f"structural_proposal:{next_revision.proposal_id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={"revision_number": next_revision.revision_number, "superseded_revision_id": str(current.id)},
        )
        publish_event(
            "STRUCTURAL_PROPOSAL_REFINED",
            {
                "proposal_id": str(next_revision.proposal_id),
                "revision_id": str(next_revision.id),
                "revision_number": next_revision.revision_number,
                "superseded_revision_id": str(current.id),
            },
        )
        return next_revision
