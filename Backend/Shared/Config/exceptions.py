"""
Aurex Shared Configuration Framework - Exceptions Module.

This module defines custom enterprise exceptions for the configuration framework
to support fail-fast behavior and precise diagnostics.
"""

class ConfigError(Exception):
    """Base exception for all configuration framework errors."""
    pass


class ConfigFileNotFoundError(ConfigError):
    """Raised when the platform-config.yaml or specified config path is not found."""
    pass


class YAMLValidationError(ConfigError):
    """Raised when the YAML file has invalid structure, formatting, or fails structural schema check."""
    pass


class MissingRequiredValueError(ConfigError):
    """Raised when a mandatory configuration value (e.g., JWT secret, DB password) is missing and not provided in the environment."""
    pass


class TypeMismatchError(ConfigError):
    """Raised when an environment variable override does not match the expected type of the configuration property."""
    pass


class ImmutableConfigError(ConfigError):
    """Raised when an application code attempts to modify a frozen configuration setting at runtime."""
    pass
