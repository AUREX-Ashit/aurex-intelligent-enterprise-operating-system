import hashlib
from datetime import datetime, timedelta, timezone
from typing import Union
from uuid import UUID

from jose import jwt, JWTError
from fastapi import HTTPException, status
from passlib.context import CryptContext

from schemas.auth import (
    LoginRequest,
    TokenPayload,
    TokenResponse,
    RefreshTokenResponse,
    OrganizationOption,
    OrganizationSelectionResponse,
)
from repositories.identity_repository import IdentityRepository
from repositories.membership_repository import MembershipRepository
from repositories.refresh_token_repository import RefreshTokenRepository
from config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

_INVALID_CREDENTIALS = "Invalid email or password."
_INVALID_TOKEN       = "Credentials verification failed."


class AuthService:
    """
    Business service layer for R-001 authentication.
    Orchestrates the Identity → Person → Membership → Role chain
    and issues JWTs containing the five required claims.
    """

    def __init__(
        self,
        identity_repo: IdentityRepository,
        membership_repo: MembershipRepository,
        refresh_token_repo: RefreshTokenRepository,
    ) -> None:
        self.identity_repo      = identity_repo
        self.membership_repo    = membership_repo
        self.refresh_token_repo = refresh_token_repo

    # ------------------------------------------------------------------
    # Password helpers
    # ------------------------------------------------------------------

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    # ------------------------------------------------------------------
    # Token helpers
    # ------------------------------------------------------------------

    def _hash_token(self, raw_token: str) -> str:
        """SHA-256 hex digest of a JWT string — stored as RefreshToken.token_hash."""
        return hashlib.sha256(raw_token.encode()).hexdigest()

    def create_access_token(
        self,
        payload: TokenPayload,
        expires_delta: timedelta | None = None,
    ) -> str:
        """
        Builds a signed access token containing the five R-001 JWT claims.
        """
        expire = datetime.now(timezone.utc) + (
            expires_delta or timedelta(minutes=settings.access_token_expiry_minutes)
        )
        claims = {
            "person_id":       str(payload.person_id),
            "identity_id":     str(payload.identity_id),
            "organization_id": str(payload.organization_id),
            "membership_id":   str(payload.membership_id),
            "role_code":       payload.role_code,
            "exp":             expire,
            "type":            "access",
        }
        return jwt.encode(claims, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

    def create_refresh_token(
        self,
        payload: TokenPayload,
        expires_delta: timedelta | None = None,
    ) -> str:
        """
        Builds a signed refresh token with the same R-001 claims.
        The raw token is never stored — only its SHA-256 hash is persisted.
        """
        expire = datetime.now(timezone.utc) + (
            expires_delta or timedelta(days=settings.refresh_token_expiry_days)
        )
        claims = {
            "person_id":       str(payload.person_id),
            "identity_id":     str(payload.identity_id),
            "organization_id": str(payload.organization_id),
            "membership_id":   str(payload.membership_id),
            "role_code":       payload.role_code,
            "exp":             expire,
            "type":            "refresh",
        }
        return jwt.encode(claims, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

    # ------------------------------------------------------------------
    # Login
    # ------------------------------------------------------------------

    async def authenticate_user(
        self,
        login_data: LoginRequest,
        organization_id: UUID | None,
    ) -> Union[TokenResponse, OrganizationSelectionResponse]:
        """
        Executes the R-001 authentication chain:
          Identity (email) → verify password
          → Membership (person + org) → Role
          → TokenPayload → JWT pair → persist RefreshToken

        When organization_id is None and the person belongs to more than one
        active organization, returns OrganizationSelectionResponse instead of
        issuing a token. The client must re-POST with X-Tenant-ID set.
        """

        # Step 1 — resolve Identity by email
        identity = await self.identity_repo.get_by_email(login_data.email)
        if not identity:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=_INVALID_CREDENTIALS,
            )

        # Step 2 — verify LOCAL password (OAuth identities have no password_hash)
        if not identity.password_hash:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=_INVALID_CREDENTIALS,
            )
        if not self.verify_password(login_data.password, identity.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=_INVALID_CREDENTIALS,
            )

        # Step 3 — resolve Membership
        if organization_id is not None:
            # Caller supplied X-Tenant-ID — direct org-scoped login
            membership = await self.membership_repo.get_active_membership(
                identity.person_id, organization_id
            )
            if not membership:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No active membership found for this organization.",
                )
        else:
            # No org context — discover all active memberships
            memberships = await self.membership_repo.get_person_memberships(
                identity.person_id
            )
            if not memberships:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No active organization memberships found for this account.",
                )
            if len(memberships) > 1:
                # Person belongs to multiple orgs — ask the client to select
                return OrganizationSelectionResponse(
                    organizations=[
                        OrganizationOption(
                            organization_id=m.organization_id,
                            organization_name=m.organization.organization_name,
                            role_code=m.role.role_code,
                        )
                        for m in memberships
                    ]
                )
            membership = memberships[0]

        # Step 4 — build R-001 TokenPayload
        token_payload = TokenPayload(
            person_id=identity.person_id,
            identity_id=identity.id,
            organization_id=membership.organization_id,
            membership_id=membership.id,
            role_code=membership.role.role_code,
        )

        # Step 5 — generate token pair
        access_token  = self.create_access_token(token_payload)
        refresh_token = self.create_refresh_token(token_payload)

        # Step 6 — persist refresh token (hash only — never store plaintext)
        refresh_expires = datetime.now(timezone.utc) + timedelta(
            days=settings.refresh_token_expiry_days
        )
        await self.refresh_token_repo.create({
            "identity_id": identity.id,
            "token_hash":  self._hash_token(refresh_token),
            "expires_at":  refresh_expires,
        })

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.access_token_expiry_minutes * 60,
            refresh_token=refresh_token,
        )

    # ------------------------------------------------------------------
    # Token refresh
    # ------------------------------------------------------------------

    async def refresh_session_token(self, refresh_token: str) -> RefreshTokenResponse:
        """
        Validates a refresh token against the database and re-issues an access token.

        Checks performed in order:
          1. JWT signature and expiry
          2. type == "refresh"
          3. token_hash present in refresh_tokens table
          4. is_revoked == False
          5. expires_at not passed (belt-and-suspenders over JWT exp)
          6. Membership still active (catches mid-session role/org changes)
        """
        # Step 1 — decode and verify JWT signature + expiry
        try:
            claims = jwt.decode(
                refresh_token,
                settings.jwt_secret_key,
                algorithms=[settings.jwt_algorithm],
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=_INVALID_TOKEN,
            )

        # Step 2 — confirm token type
        if claims.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token type.",
            )

        # Step 3 — extract and validate R-001 claims
        person_id_str       = claims.get("person_id")
        identity_id_str     = claims.get("identity_id")
        organization_id_str = claims.get("organization_id")

        if not all([person_id_str, identity_id_str, organization_id_str]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=_INVALID_TOKEN,
            )

        try:
            person_id       = UUID(person_id_str)
            identity_id     = UUID(identity_id_str)
            organization_id = UUID(organization_id_str)
        except (ValueError, TypeError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=_INVALID_TOKEN,
            )

        # Step 4 — look up stored token by hash
        token_hash    = self._hash_token(refresh_token)
        stored_token  = await self.refresh_token_repo.get_by_token_hash(token_hash)
        if not stored_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=_INVALID_TOKEN,
            )

        # Step 5 — check revocation and expiry
        if stored_token.is_revoked:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=_INVALID_TOKEN,
            )
        if stored_token.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=_INVALID_TOKEN,
            )

        # Step 6 — re-validate membership (role or status may have changed)
        membership = await self.membership_repo.get_active_membership(
            person_id, organization_id
        )
        if not membership:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Organization access has been revoked.",
            )

        # Step 7 — build fresh payload from current membership state
        token_payload = TokenPayload(
            person_id=person_id,
            identity_id=identity_id,
            organization_id=organization_id,
            membership_id=membership.id,
            role_code=membership.role.role_code,
        )

        new_access_token = self.create_access_token(token_payload)
        return RefreshTokenResponse(
            access_token=new_access_token,
            token_type="bearer",
            expires_in=settings.access_token_expiry_minutes * 60,
        )
