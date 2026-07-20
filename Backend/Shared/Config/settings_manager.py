"""
CorpStage Shared Configuration Framework - Settings Manager Module.

This module wraps raw nested configuration dictionaries into a highly-typed,
immutable, dotted-attribute access interface (SettingsNode) to provide safe,
elegant, autocomplete-friendly, and secure consumption of configuration parameters.
"""

from typing import Dict, Any, Optional
from corpstage.backend.shared.config.exceptions import ImmutableConfigError


class SettingsNode:
    """
    An immutable, recursive object wrapper over dictionaries allowing dotted-attribute
    access (e.g. settings.database.postgresql.host) and preventing runtime alterations.
    """

    def __init__(self, data: Dict[str, Any]):
        # Store internal references using __dict__ directly to bypass Immutable restrictions in constructor
        object.__setattr__(self, "_raw_data", data)
        for key, value in data.items():
            if isinstance(value, dict):
                object.__setattr__(self, key, SettingsNode(value))
            else:
                object.__setattr__(self, key, value)

    def get(self, path: str, default: Any = None) -> Any:
        """
        Supports dynamic lookup of configuration paths using string separators.
        e.g., settings.get("database.postgresql.host")
        """
        parts = path.split(".")
        current: Any = self
        for part in parts:
            if not isinstance(current, SettingsNode):
                return default
            if hasattr(current, part):
                current = getattr(current, part)
            else:
                return default
        return current

    def to_dict(self) -> Dict[str, Any]:
        """Converts the SettingNode structure recursively back to a standard Python dictionary."""
        return self._raw_data

    def __setattr__(self, name: str, value: Any) -> None:
        raise ImmutableConfigError(
            f"MUTATION SECURITY EXCEPTION: Configuration value '{name}' cannot be modified. "
            "CorpStage Shared Configuration is strictly immutable after initialization."
        )

    def __delattr__(self, name: str) -> None:
        raise ImmutableConfigError(
            f"MUTATION SECURITY EXCEPTION: Configuration value '{name}' cannot be deleted. "
            "CorpStage Shared Configuration is strictly immutable after initialization."
        )

    def __repr__(self) -> str:
        keys = [k for k in self.__dict__.keys() if not k.startswith("_")]
        return f"SettingsNode({', '.join(keys)})"


class SettingsManager:
    """
    Acts as the state holder and single source of truth for loading, holding,
    and serving the immutable CorpStage configurations across service boundary.
    """

    _instance: Optional[SettingsNode] = None

    @classmethod
    def get_settings(cls) -> SettingsNode:
        """
        Retrieves the global settings instance.
        
        Raises:
            RuntimeError: If Settings are accessed prior to being loaded via ConfigLoader.
        """
        if cls._instance is None:
            raise RuntimeError(
                "CorpStage Config Framework is uninitialized. "
                "Invoke ConfigLoader.initialize() during application startup before querying settings."
            )
        return cls._instance

    @classmethod
    def load_from_dict(cls, config_data: Dict[str, Any]) -> SettingsNode:
        """Initializes or replaces the global unified settings from a base dictionary representation."""
        cls._instance = SettingsNode(config_data)
        return cls._instance
