"""
CorpStage Shared Security Framework - Exceptions Module.

Provides custom, strongly-typed enterprise exceptions for the security,
authentication, role management, and tenant authorization boundaries.
Supports detailed telemetry logging and precise API response formatting.
"""

class SecurityError(Exception):
    """Base exception for all security-related errors in the CorpStage platform."""
    pass


# Authentication (JWT) Exceptions
class AuthenticationError(SecurityError):
    """Raised when authentication fails due to invalid parameters, missing tokens, or verification failures."""
    pass


class InvalidTokenError(AuthenticationError):
    """Raised when a signature verification fails, token format is corrupt, or claims are malformed."""
    pass


class TokenExpiredError(InvalidTokenError):
    """Raised specifically when a validated JWT has exceeded its exp timestamp claim."""
    pass


class TokenRevokedError(InvalidTokenError):
    """Raised when a JWT is matched against active security blacklist engines."""
    pass


# Cryptography / Password Exceptions
class PasswordError(SecurityError):
    """Base exception for password operations."""
    pass


class PasswordHashingError(PasswordError):
    """Raised when password hashing, stretching, or verification routines fail."""
    pass


class WeakPasswordError(PasswordError):
    """Raised during user creation or reset when password complexity constraints are not satisfied."""
    pass


# Authorization (RBAC / ABAC) Exceptions
class AuthorizationError(SecurityError):
    """Base exception for authorization permission boundary check failures."""
    pass


class PermissionDeniedError(AuthorizationError):
    """Raised when an authenticated principal attempts to access a resource without sufficient roles or permissions."""
    pass


class TenantAuthorizationError(AuthorizationError):
    """
    Raised when an authenticated principal attempts to cross tenant query boundaries,
    violating multi-tenant schema isolation guards.
    """
    pass


class SecurityContextError(SecurityError):
    """Raised when attempting to query or modify thread-local security context state in an uninitialized thread context."""
    pass
