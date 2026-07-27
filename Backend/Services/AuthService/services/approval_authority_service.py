"""
WP-02 — Role & Permission Management (C-003).

Business Activity implemented here: BA-03 Establish Approval Authority,
realizing PE-001-C003's ERB-C003-01 (Define Authorization Policy
Structure) / EX-C003-03 (Establish Approval Authority). See IRA-002 for
the full ERB/EX -> Business Activity mapping.

Follows DomainPermissionService.establish()'s exact pattern (WP-02
BA-02): structural existence pre-checks (organization, and domain where
scope_type is DOMAIN), record_audit / publish_event for SD-002-054's
seven audit questions and RTA-001 §4.13 Domain Event Publication.

scope_type's own internal consistency (exactly one anchor populated per
scope_type) is validated at the request layer
(schemas/approval_authority.py's model_validator) and re-enforced at the
database layer (ck_approval_authorities_scope_consistency) — this
service only needs to confirm the referenced Organization and, where
applicable, Domain actually exist.

Authorization disposition (mirrors IRA-002 §2.7's BA-01 precedent and
BA-02's TD-022 precedent exactly): PE-001-C003's EX-C003-03 requires
confirmed Corporate Admin or Domain Owner authority. Neither exists as a
distinct, enforceable claim today (Corporate Admin: same ADR-002 gap as
BA-01; Domain Owner: same Domain-is-ownership-free gap as BA-02). This
method therefore gates on the same interim PLATFORM_ADMIN dependency,
disclosed here as a stated simplification and recorded as technical debt
(TD-023).
"""

from __future__ import annotations

from fastapi import HTTPException, status

from models.approval_authority import ApprovalAuthority, ApprovalScopeType
from repositories.approval_authority_repository import ApprovalAuthorityRepository
from repositories.domain_repository import DomainRepository
from repositories.organization_repository import OrganizationRepository
from schemas.approval_authority import EstablishApprovalAuthorityRequest
from observability import record_audit, publish_event, AuditStatus


class ApprovalAuthorityService:
    """Business Activity orchestrator for Approval Authority establishment (WP-02 BA-03)."""

    def __init__(
        self,
        approval_authority_repo: ApprovalAuthorityRepository,
        organization_repo: OrganizationRepository,
        domain_repo: DomainRepository,
    ) -> None:
        self.approval_authority_repo = approval_authority_repo
        self.organization_repo = organization_repo
        self.domain_repo = domain_repo

    async def establish(
        self, request: EstablishApprovalAuthorityRequest, actor_id: str | None = None
    ) -> ApprovalAuthority:
        """
        Business Activity: Establish Approval Authority (BA-03).

        Structural rules (BR-C003-01, EX-C003-03 Context Required):
        - The target Organization must already exist (404 if not —
          required for every scope, including GLOBAL/COMPANY).
        - Where scope_type is DOMAIN, the target Domain must already
          exist (404 if not — "the target Domain, already established",
          same discipline as BA-02).
        - scope_type/domain_id/object_type/object_id's mutual consistency
          is validated before this method is ever reached (422, via
          EstablishApprovalAuthorityRequest's model_validator).
        """
        organization = await self.organization_repo.get_by_id(request.organization_id)
        if organization is None:
            record_audit(
                action="ESTABLISH_APPROVAL_AUTHORITY",
                resource=f"organization:{request.organization_id}",
                status=AuditStatus.DENIED,
                actor_id=actor_id or "SYSTEM",
                metadata={"reason": "target organization does not exist"},
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No organization found with id '{request.organization_id}'.",
            )

        if request.scope_type == ApprovalScopeType.DOMAIN:
            domain = await self.domain_repo.get_by_id(request.domain_id)
            if domain is None:
                record_audit(
                    action="ESTABLISH_APPROVAL_AUTHORITY",
                    resource=f"domain:{request.domain_id}",
                    status=AuditStatus.DENIED,
                    actor_id=actor_id or "SYSTEM",
                    metadata={"reason": "target domain does not exist"},
                )
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No domain found with id '{request.domain_id}'.",
                )

        approval_authority = await self.approval_authority_repo.create(
            {
                "organization_id": request.organization_id,
                "authority_name": request.authority_name,
                "approval_strategy": request.approval_strategy.value,
                "majority_threshold_pct": request.majority_threshold_pct,
                "scope_type": request.scope_type.value,
                "domain_id": request.domain_id,
                "object_type": request.object_type,
                "object_id": request.object_id,
            }
        )
        await self.approval_authority_repo.session.flush()

        record_audit(
            action="ESTABLISH_APPROVAL_AUTHORITY",
            resource=f"approval_authority:{approval_authority.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={
                "organization_id": str(approval_authority.organization_id),
                "authority_name": approval_authority.authority_name,
                "approval_strategy": approval_authority.approval_strategy,
                "scope_type": approval_authority.scope_type,
            },
        )
        publish_event(
            "APPROVAL_AUTHORITY_ESTABLISHED",
            {
                "approval_authority_id": str(approval_authority.id),
                "organization_id": str(approval_authority.organization_id),
                "authority_name": approval_authority.authority_name,
                "approval_strategy": approval_authority.approval_strategy,
                "scope_type": approval_authority.scope_type,
                "domain_id": str(approval_authority.domain_id) if approval_authority.domain_id else None,
                "object_type": approval_authority.object_type,
                "object_id": str(approval_authority.object_id) if approval_authority.object_id else None,
            },
        )
        return approval_authority
