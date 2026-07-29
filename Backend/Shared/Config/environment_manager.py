"""
Aurex Shared Configuration Framework - Environment Manager Module.

This module provides enterprise-grade capabilities to read, normalize, and coerce
environment variable overrides into the corporate configuration structure.
"""

import os
import logging
from typing import Dict, Any, Optional, Set

from aurex.backend.shared.config.exceptions import (
    TypeMismatchError,
    MissingRequiredValueError
)

logger = logging.getLogger("Aurex.Config.EnvironmentManager")


class EnvironmentManager:
    """
    Manages loading, filtering, type casting, and application of 
    environment-based configuration overrides on top of the base YAML configurations.
    """

    PREFIX = "AUREX_"
    SEPARATOR = "__"  # Double underscores for nesting: AUREX__DATABASE__POSTGRESQL__PORT

    REQUIRED_ENV_SECRETS: Set[str] = {
        "AUREX_JWT_SECRET",            # Maps to authentication.jwt.secret
        "AUREX_DATABASE_PASSWORD"      # Map to database.postgresql.password fallback
    }

    @staticmethod
    def get_overrides() -> Dict[str, Any]:
        """
        Scans all system environment variables, filters for Aurex variables
        (specifically starting with 'AUREX_'), and compiles them into a nested dictionary.
        
        Example:
            AUREX__DATABASE__POSTGRESQL__PORT = "5433"
            becomes:
            {'database': {'postgresql': {'port': 5433}}} (after coercion)
        """
        overrides: Dict[str, Any] = {}

        for env_key, env_value in os.environ.items():
            if not env_key.startswith(EnvironmentManager.PREFIX):
                continue
            
            # Skip direct raw secret keys that are handled separately to avoid polluting hierarchical mappings
            if env_key in EnvironmentManager.REQUIRED_ENV_SECRETS:
                continue

            # Parse path from variable
            # Strip prefix (e.g., AUREX_DATABASE_POSTGRESQL_PORT -> DATABASE_POSTGRESQL_PORT)
            path_str = env_key[len(EnvironmentManager.PREFIX):]
            
            # Determine separator (prefer double underscore __, fallback to single underscore if no double is found)
            if EnvironmentManager.SEPARATOR in path_str:
                parts = [p.lower() for p in path_str.split(EnvironmentManager.SEPARATOR)]
            else:
                parts = [p.lower() for p in path_str.split('_')]

            # Build nested dictionary structure
            current = overrides
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                elif not isinstance(current[part], dict):
                    # Path conflict resolved safely (convert node to dict or handle appropriately)
                    current[part] = {}
                current = current[part]
                
            leaf = parts[-1]
            current[leaf] = env_value

        return overrides

    @staticmethod
    def apply_overrides(base_config: Dict[str, Any], overrides: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recursively applies nested environmental overrides onto the base configuration,
        performing dynamic type safety coercion matching the existing types.
        
        Raises:
            TypeMismatchError: If the override type cannot be coerced to the schema type.
        """
        for key, override_val in overrides.items():
            if key not in base_config:
                # Key is new, which is allowed for environmental overrides (e.g. custom or secret keys)
                if isinstance(override_val, dict):
                    base_config[key] = EnvironmentManager.apply_overrides({}, override_val)
                else:
                    base_config[key] = EnvironmentManager._coerce_raw_value(override_val, str)
                continue

            base_val = base_config[key]

            if isinstance(base_val, dict) and isinstance(override_val, dict):
                base_config[key] = EnvironmentManager.apply_overrides(base_val, override_val)
            elif isinstance(base_val, dict) or isinstance(override_val, dict):
                # Type conflict, e.g., overriding a whole sub-dictionary with a scalar or vice versa
                raise TypeMismatchError(
                    f"Configuration mismatch: cannot replace path '{key}' of type {type(base_val).__name__} "
                    f"with override values of type {type(override_val).__name__}."
                )
            else:
                # Both are scalars, coerce type of environmental override to match base
                expected_type = type(base_val)
                try:
                    base_config[key] = EnvironmentManager._coerce_value_to_type(override_val, expected_type, key)
                except ValueError as ex:
                    raise TypeMismatchError(
                        f"Failed to coerce environment override for key '{key}' from value "
                        f"'{override_val}' to expected type {expected_type.__name__}: {str(ex)}"
                    )

        return base_config

    @staticmethod
    def enforce_secrets(config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enforces strict compliance with security rules:
        - JWT secrets MUST exist inside system environment variables.
        - Fails startup with precise instructions if required secrets are absent.
        - Inject secrets safely into the nested dictionary structure.
        """
        jwt_secret = os.getenv("AUREX_JWT_SECRET")
        if not jwt_secret:
            raise MissingRequiredValueError(
                "CRITICAL STARTUP FAILURE: Required environment variable 'AUREX_JWT_SECRET' "
                "is missing! For enterprise compliance, JWT secrets must never be placed in source code or YAML."
            )

        # Inject JWT secret into config['authentication']['jwt']
        if "authentication" not in config:
            config["authentication"] = {}
        if "jwt" not in config["authentication"]:
            config["authentication"]["jwt"] = {}
        
        config["authentication"]["jwt"]["secret"] = jwt_secret

        # Check for Database Password safeguard
        db_password_env = os.getenv("AUREX_DATABASE_PASSWORD")
        if db_password_env:
            # Override database host password
            if "database" in config and "postgresql" in config["database"]:
                config["database"]["postgresql"]["password"] = db_password_env

        return config

    @staticmethod
    def _coerce_value_to_type(val: Any, target_type: type, key_name: str) -> Any:
        """Coerces a scalar value into the target data type securely."""
        if target_type == bool:
            if isinstance(val, bool):
                return val
            if str(val).lower() in ("true", "1", "yes", "on"):
                return True
            if str(val).lower() in ("false", "0", "no", "off"):
                return False
            raise ValueError(f"Value '{val}' is not a valid boolean.")
            
        if target_type == int:
            return int(val)
            
        if target_type == float:
            return float(val)
            
        if target_type == list:
            if isinstance(val, list):
                return val
            # Split comma-separated string for environmental arrays
            return [part.strip() for part in str(val).split(",")]

        return str(val)

    @staticmethod
    def _coerce_raw_value(val: Any, default_type: type = str) -> Any:
        """Infer type when no base key exists for guidance."""
        if isinstance(val, bool):
            return val
        if str(val).lower() in ("true", "yes"):
            return True
        if str(val).lower() in ("false", "no"):
            return False
        try:
            if "." in str(val):
                return float(val)
            return int(val)
        except ValueError:
            pass
        return str(val)
