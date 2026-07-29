"""
Aurex Shared Configuration Framework

A unified, multi-service configuration delivery mechanism built for Enterprise-grade
resiliency, fail-fast validations, strict environment secrets insulation, and 
hierarchical overrides.
"""

from aurex.backend.shared.config.exceptions import (
    ConfigError,
    ConfigFileNotFoundError,
    YAMLValidationError,
    MissingRequiredValueError,
    TypeMismatchError,
    ImmutableConfigError
)
from aurex.backend.shared.config.yaml_parser import YAMLParser
from aurex.backend.shared.config.environment_manager import EnvironmentManager
from aurex.backend.shared.config.settings_manager import SettingsManager, SettingsNode
from aurex.backend.shared.config.config_loader import ConfigLoader

__all__ = [
    "ConfigLoader",
    "SettingsManager",
    "SettingsNode",
    "YAMLParser",
    "EnvironmentManager",
    "ConfigError",
    "ConfigFileNotFoundError",
    "YAMLValidationError",
    "MissingRequiredValueError",
    "TypeMismatchError",
    "ImmutableConfigError",
]
