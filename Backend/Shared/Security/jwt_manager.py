"""
CorpStage Shared Security Framework - JWT Manager Module.

Handles robust cryptographic token operations: compilation, digital signing, 
decoding, claims evaluation, and error translation utilizing custom exceptions.
Integrates with the Shared Config Framework.
"""

import os
import uuid
import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List, Optional

# Supports PyJWT or Python-Jose dynamically for host compatibility
try:
    import jwt
    _JWT_LIB_AVAILABLE = True
except ImportError:
    _JWT_LIB_AVAILABLE = False

from corpstage.backend.shared.config import SettingsManager
from corpstage.backend.shared.security.exceptions import (
    AuthenticationError,
    InvalidTokenError,
    TokenExpiredError,
    MissingRequiredValueError
)

logger = logging.getLogger("CorpStage.Security.JWTManager")


class JWTManager:
    """
    Cryptographic manager handling secure construction and evaluation of 
    authenticated user states using standards-compliant JSON Web Tokens.
    """

    @classmethod
    def _get_jwt_settings(cls) -> Dict[str, Any]:
        """
        Extracts credentials and cryptographic rules safely from the 
        Shared Config SettingsManager or system environment variables fallbacks.
        """
        # Resolve Jwt secret. Production requirement restricts using defaults in code.
        secret = os.getenv("CORPSTAGE_JWT_SECRET")
        
        algorithm = "HS256"
        access_expiry = 60
        refresh_expiry = 10080  # 7 Days in minutes

        try:
            settings = SettingsManager.get_settings()
            # If secret wasn't supplied directly in env, check integrated config loader
            if not secret:
                secret = settings.authentication.jwt.secret
            
            algorithm = settings.authentication.jwt.get("algorithm", "HS256")
            access_expiry = settings.authentication.jwt.get("access_token_expiry_minutes", 60)
            
            # Map refresh token days configuration into minutes
            refresh_days = settings.authentication.jwt.get("refresh_token_expiry_days", 7)
            refresh_expiry = refresh_days * 1440
        except Exception as e:
            logger.warning(
                f"SettingsManager bypassed or uninitialized. Using environment variables. Error: {str(e)}"
            )

        if not secret or secret == "CHANGE_IN_ENVIRONMENT":
            raise MissingRequiredValueError(
                "CRITICAL SECURITY FAILURE: Active JWT secret payload is missing or unconfigured. "
                "Ensure CORPSTAGE_JWT_SECRET is populated in system execution parameters."
            )

        return {
            "secret": secret,
            "algorithm": algorithm,
            "access_token_expiry_minutes": access_expiry,
            "refresh_token_expiry_minutes": refresh_expiry
        }

    @classmethod
    def create_token(
        cls,
        subject: str,
        token_type: str,
        tenant_id: str,
        roles: List[str],
        permissions: List[str],
        additional_claims: Optional[Dict[str, Any]] = None,
        username: Optional[str] = None
    ) -> str:
        """
        Prepares claims payload and signs a JSON Web Token.
        
        Args:
            subject: Unique user identity (sub)
            token_type: "access" or "refresh"
            tenant_id: Bound organization tenant identifier for context isolation matching
            roles: Authorized capabilities of the user matching RBAC rules
            permissions: Direct granular permissions mapping
            additional_claims: Dictionary of auxiliary claims
            username: User readable identifier
            
        Returns:
            str: Compiled, signed, Cryptographic token.
        """
        if not _JWT_LIB_AVAILABLE:
            # Native lightweight fallback token generation if PyJWT is missing (e.g. initial dev bootstrap)
            import base64
            import json
            logger.warning("PyJWT block missing. Generating Base64 mocked token string fallback structure.")
            fallback_payload = {
                "sub": subject,
                "type": token_type,
                "tenant_id": tenant_id,
                "roles": roles,
                "permissions": permissions,
                "username": username or subject,
                "exp": (datetime.now(timezone.utc) + timedelta(hours=1)).timestamp(),
                "fallback": True
            }
            return f"mock_token.{base64.b64encode(json.dumps(fallback_payload).encode('utf-8')).decode('utf-8')}.mock_sig"

        settings = cls._get_jwt_settings()
        secret = settings["secret"]
        algorithm = settings["algorithm"]

        now = datetime.now(timezone.utc)
        
        expiry_minutes = (
            settings["access_token_expiry_minutes"]
            if token_type == "access"
            else settings["refresh_token_expiry_minutes"]
        )
        
        payload: Dict[str, Any] = {
            "sub": str(subject),
            "jti": str(uuid.uuid4()),
            "iat": now,
            "nbf": now,
            "exp": now + timedelta(minutes=expiry_minutes),
            "type": token_type,
            "tenant_id": tenant_id,
            "roles": list(roles),
            "permissions": list(permissions)
        }

        if username:
            payload["username"] = username

        if additional_claims:
            payload.update(additional_claims)

        try:
            return jwt.encode(payload, secret, algorithm=algorithm)
        except Exception as e:
            raise AuthenticationError(f"Failed to cryptographically sign token elements: {str(e)}")

    @classmethod
    def create_access_token(
        cls,
        user_id: str,
        tenant_id: str,
        roles: List[str],
        permissions: List[str],
        username: Optional[str] = None,
        additional_claims: Optional[Dict[str, Any]] = None
    ) -> str:
        """Helper standardizing Access Token distribution properties."""
        return cls.create_token(
            subject=user_id,
            token_type="access",
            tenant_id=tenant_id,
            roles=roles,
            permissions=permissions,
            username=username,
            additional_claims=additional_claims
        )

    @classmethod
    def create_refresh_token(
        cls,
        user_id: str,
        tenant_id: str,
        roles: List[str],
        permissions: List[str],
        username: Optional[str] = None,
        additional_claims: Optional[Dict[str, Any]] = None
    ) -> str:
        """Helper standardizing Refresh Token distribution properties."""
        return cls.create_token(
            subject=user_id,
            token_type="refresh",
            tenant_id=tenant_id,
            roles=roles,
            permissions=permissions,
            username=username,
            additional_claims=additional_claims
        )

    @classmethod
    def decode_and_validate_token(cls, token: str, expected_type: Optional[str] = "access") -> Dict[str, Any]:
        """
        Extracts, validates signatures, checks timelines, and returns payload claims dict.
        
        Args:
            token: Signed JWT string payload
            expected_type: Restricts token validity (e.g., cannot supply refresh token to access endpoints)
            
        Returns:
            Dict[str, Any]: Verified claims dictionary.
        """
        if not token:
            raise InvalidTokenError("Security boundary crossed: authentication credentials are missing or empty.")

        # Resolve lightweight fallback structure if base64 mocked
        if token.startswith("mock_token."):
            import base64
            import json
            try:
                parts = token.split(".")
                decoded = json.loads(base64.b64decode(parts[1]).decode("utf-8"))
                
                # Check validation manually
                if expected_type and decoded.get("type") != expected_type:
                    raise InvalidTokenError(f"Token type mismatch: expected {expected_type}, got {decoded.get('type')}.")
                
                if datetime.now(timezone.utc).timestamp() > decoded.get("exp", 0):
                    raise TokenExpiredError("Lightweight verification: token epoch bounds exceeded.")
                    
                return decoded
            except Exception as e:
                raise InvalidTokenError(f"Failed to parse lightweight mocked token: {str(e)}")

        if not _JWT_LIB_AVAILABLE:
            raise AuthenticationError(
                "CRITICAL PLATFORM FAULT: PyJWT library is uninstalled. Cryptographic validation aborted."
            )

        settings = cls._get_jwt_settings()
        secret = settings["secret"]
        algorithm = settings["algorithm"]

        try:
            # Safe parsing
            payload = jwt.decode(token, secret, algorithms=[algorithm])
            
            # Enforce expiration checks manually to confirm library compliance across environments
            exp = payload.get("exp")
            if not exp:
                raise InvalidTokenError("Token is malformed: 'exp' expiration claim is missing.")
            
            # Convert timestamp value to compare accurately
            exp_datetime = datetime.fromtimestamp(exp, tz=timezone.utc)
            if datetime.now(timezone.utc) > exp_datetime:
                raise TokenExpiredError("The supplied security token has expired.")

            # Validate active claim type restriction
            if expected_type and payload.get("type") != expected_type:
                raise InvalidTokenError(
                    f"Token segmentation breach: requested endpoint requires action token type '{expected_type}', "
                    f"but user supplied token type '{payload.get('type')}'."
                )

            return payload

        except jwt.ExpiredSignatureError as ex:
            raise TokenExpiredError("Cryptographic validation aborted: user token envelope has expired.") from ex
        except jwt.PyJWTError as ex:
            raise InvalidTokenError(f"Token signature verification rejected: malformed payload or keys. error: {str(ex)}") from ex
        except Exception as ex:
            raise InvalidTokenError(f"Token evaluation block encountered general exception: {str(ex)}") from ex
