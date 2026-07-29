from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.organization_node import OrganizationNode
from repositories.base_repository import BaseRepository


class OrganizationNodeRepository(BaseRepository[OrganizationNode]):
    """
    Repository for Organization Node records (ERG-001-02/03's
    EnterpriseNode — see models/organization_node.py).

    WP-03 BA-01 only needed the inherited get_by_id() to validate a
    caller-supplied home_node_id (BR-C007-002/007). WP-04 BA-01
    (Establish Organization Node, IRA-004) adds get_by_code() for the
    pre-flight duplicate check — the same establish()-pattern
    OrganizationRepository.get_by_code() already established for
    Organization (WP-01). The create() write path itself needed no new
    method: BaseRepository already provides it (TD-032's own "no
    establish()-style write path" note referred to no *service* calling
    it yet, not to a missing repository capability).
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(OrganizationNode, session)

    async def get_by_code(self, node_code: str) -> OrganizationNode | None:
        """
        Looks up an OrganizationNode by its unique node_code — the
        natural key used for Establish Organization Node's pre-flight
        duplicate check, mirroring OrganizationRepository.get_by_code().
        """
        result = await self.session.execute(
            select(OrganizationNode).where(OrganizationNode.node_code == node_code)
        )
        return result.scalars().first()
