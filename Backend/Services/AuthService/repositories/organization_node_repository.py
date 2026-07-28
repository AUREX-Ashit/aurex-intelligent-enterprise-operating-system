from sqlalchemy.ext.asyncio import AsyncSession

from models.organization_node import OrganizationNode
from repositories.base_repository import BaseRepository


class OrganizationNodeRepository(BaseRepository[OrganizationNode]):
    """
    Repository for Organization Node records (WP-03 BA-01's minimal
    home-node anchor — see models/organization_node.py).

    No custom query methods yet: BA-01 only needs the inherited
    get_by_id() to validate a caller-supplied home_node_id (BR-C007-002/
    007). No establish()-style write path is added here — no Business
    Activity in this repository owns creating these rows yet (TD-032).
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(OrganizationNode, session)
