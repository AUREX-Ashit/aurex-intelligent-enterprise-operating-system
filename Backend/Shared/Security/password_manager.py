"""
Aurex Shared Security Framework - Password Manager Module.

Provides highly secure hashing, stretching (bcrypt), and complexity validation 
routines for user passwords. Implements resilient fallbacks for robust 
enterprise deployment adaptability.
"""

import re
import os
import hashlib
import logging
from typing import Optional, Any

# Supports passlib for unified server-level cryptography context
try:
    from passlib.context import CryptContext
    _PASSLIB_AVAILABLE = True
except ImportError:
    _PASSLIB_AVAILABLE = False

from aurex.backend.shared.security.exceptions import (
    PasswordHashingError,
    WeakPasswordError
)

logger = logging.getLogger("Aurex.Security.PasswordManager")


class PasswordManager:
    """
    Unified cryptographically backed password manager. Validates complexity rules
    and translates string keys into secure hashed state footprints.
    """

    _pwd_context = None

    @classmethod
    def _get_context(cls) -> Any:
        """Retrieves or builds the passlib CryptContext using bcrypt."""
        if cls._pwd_context is None:
            if _PASSLIB_AVAILABLE:
                # Use passlib with default bcrypt schemes and optimized rounds
                cls._pwd_context = CryptContext(
                    schemes=["bcrypt"],
                    deprecated="auto",
                    bcrypt__rounds=12
                )
            else:
                logger.warning(
                    "passlib is uninstalled. Falling back to native hashlib PBKDF2 stretching algorithm. "
                    "For production environments, please configure 'passlib[bcrypt]'."
                )
        return cls._pwd_context

    @classmethod
    def hash_password(cls, plain_text_password: str) -> str:
        """
        Derives a cryptographic secure hash representing the plaintext password.
        Uses stretching to counteract rainbow table queries or GPU attack matrices.
        """
        if not plain_text_password:
            raise PasswordHashingError("Password digest calculation refused: input cannot be empty.")

        try:
            context = cls._get_context()
            if _PASSLIB_AVAILABLE and context:
                return context.hash(plain_text_password)
            else:
                # High-resigned Native pbkdf2_hmac stretching in python
                salt = os.urandom(16)
                key = hashlib.pbkdf2_hmac(
                    'sha256', 
                    plain_text_password.encode('utf-8'), 
                    salt, 
                    100000
                )
                # Combine salt and key to match flat string structure
                return f"pbkdf2_sha256$100000${salt.hex()}${key.hex()}"
        except Exception as e:
            raise PasswordHashingError(f"Password encryption stage failed: {str(e)}")

    @classmethod
    def verify_password(cls, plain_text_password: str, hashed_password: str) -> bool:
        """
        Safely validates credentials, comparing a plaintext password against a stored hash.
        Protected against timing-based lateral estimation attacks (constant time comparison).
        """
        if not plain_text_password or not hashed_password:
            return False

        try:
            context = cls._get_context()
            if _PASSLIB_AVAILABLE and context:
                # Check using bcrypt passlib Context
                # Handles timing attacks natively
                try:
                    return context.verify(plain_text_password, hashed_password)
                except Exception:
                    # If verification fails, check if the password uses our fallback hashing
                    if hashed_password.startswith("pbkdf2_sha256$"):
                        return cls._verify_native_fallback(plain_text_password, hashed_password)
                    return False
            else:
                return cls._verify_native_fallback(plain_text_password, hashed_password)
        except Exception as e:
            logger.error(f"Error during cryptographic password evaluation: {str(e)}")
            return False

    @classmethod
    def _verify_native_fallback(cls, plain_text_password: str, hashed_password: str) -> bool:
        """Helper handling custom pbkdf2 constant-time validation match."""
        try:
            parts = hashed_password.split("$")
            if len(parts) != 4 or parts[0] != "pbkdf2_sha256":
                return False
                
            iterations = int(parts[1])
            salt = bytes.fromhex(parts[2])
            original_key = bytes.fromhex(parts[3])
            
            check_key = hashlib.pbkdf2_hmac(
                'sha256', 
                plain_text_password.encode('utf-8'), 
                salt, 
                iterations
            )
            
            # Use constant-time comparison helper from secrets/hmac package
            import hmac
            return hmac.compare_digest(original_key, check_key)
        except Exception as e:
            logger.warning(f"Native fallback check rejected state: {str(e)}")
            return False

    @classmethod
    def validate_complexity(cls, password: str) -> None:
        """
        Enforces corporate-wide credential security policies (complexity, count, digits).
        Fails-fast with meaningful messages if criteria aren't met.
        
        Requirements:
        - Minimum length: 12 characters (enterprise baseline requirement)
        - At least 1 uppercase letter
        - At least 1 lowercase letter
        - At least 1 numeric digit
        - At least 1 special character
        """
        if len(password) < 12:
            raise WeakPasswordError("Weak authentication: password must be at least 12 characters in length.")

        if not re.search(r"[A-Z]", password):
            raise WeakPasswordError("Weak authentication: password must contain at least one uppercase letter (A-Z).")

        if not re.search(r"[a-z]", password):
            raise WeakPasswordError("Weak authentication: password must contain at least one lowercase letter (a-z).")

        if not re.search(r"\d", password):
            raise WeakPasswordError("Weak authentication: password must contain at least one numeric digit (0-9).")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise WeakPasswordError("Weak authentication: password must contain at least one special character (e.g. !, @, #, $, etc.).")
