"""
CorpStage Shared Configuration Framework

A unified, multi-service configuration delivery mechanism built for Enterprise-grade
resiliency, fail-fast validations, strict environment secrets insulation, and 
hierarchical overrides.
"""

from corpstage.backend.shared.config.exceptions import (
    ConfigError,
    ConfigFileNotFoundError,
    YAMLValidationError,
    MissingRequiredValueError,
    TypeMismatchError,
    ImmutableConfigError
)
from corpstage.backend.shared.config.yaml_parser import YAMLParser
from corpstage.backend.shared.config.environment_manager import EnvironmentManager
from corpstage.backend.shared.config.settings_manager import SettingsManager, SettingsNode
from corpstage.backend.shared.config.config_loader import ConfigLoader

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
