from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.refresh_token import RefreshToken
from repositories.base_repository import BaseRepository


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    """
    Repository for RefreshToken records.
    Provides token lookup by hash for revocation and session validation.
    create() is inherited from BaseRepository and used for token persistence.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(RefreshToken, session)

    async def get_by_token_hash(self, token_hash: str) -> RefreshToken | None:
        """
        Looks up a RefreshToken by its SHA-256 hash.
        Called on every /auth/refresh request to validate the token before re-issuing.
        token_hash has a unique index so this is always a single indexed row lookup.
        Returns None when the hash is not found (token never issued or already purged).
        """
        query = select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        result = await self.session.execute(query)
        return result.scalars().first()
