from sqlalchemy.ext.asyncio import AsyncSession

from models.person import Person
from repositories.base_repository import BaseRepository


class PersonRepository(BaseRepository[Person]):
    """
    Repository for Person records.

    No custom query methods yet — establishment (EX-C006-02) needs only the
    inherited create(); recognition (EX-C006-01) resolves Person through
    IdentityRepository.get_by_email_with_person(), not through this
    repository. Added here because Person is an aggregate root with no
    prior repository, per IMP-001 §5.4's mandatory Repository artifact.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Person, session)
