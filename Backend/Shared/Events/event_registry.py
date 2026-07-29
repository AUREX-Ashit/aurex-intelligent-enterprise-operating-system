"""
Aurex Shared Events Framework - Event Registry.

Secures and manages physical-to-logical type mapping, ensuring any subscriber daemon thread
can look up appropriate schemas to rehydrate incoming byte payloads.
"""

import threading
from typing import Dict, Any, Type, Optional, Tuple

from aurex.backend.shared.events.event_base import BaseEvent
from aurex.backend.shared.events.exceptions import EventRegistryError


class EventRegistry:
    """
    Thread-safe schemas registry binding event string signifiers
    (e.g., 'aurex.auth.user.created') and version constraints to their Python representations.
    """

    _instance: Optional["EventRegistry"] = None
    _lock: threading.Lock = threading.Lock()

    def __new__(cls, *args: Any, **kwargs: Any) -> "EventRegistry":
        """Singleton pattern wrapper to preserve mapping table registry across thread scopes."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._registry = {} # type: ignore
        return cls._instance

    def _get_key(self, event_name: str, event_version: str) -> Tuple[str, str]:
        return (event_name.strip().lower(), event_version.strip())

    def register(self, event_cls: Type[BaseEvent]) -> None:
        """
        Dynamically registers custom implementation subclasses into lookup table.
        Rejects conflicts or violations to avoid injection issues on production.
        """
        # Instantiate empty signature temporarily to read properties
        try:
            # We construct a mock instance safely without parameters or use Class attributes if defined.
            # To handle non-default constructors safely, we can query class properties or create short instantiators.
            # Best practice: inspect class properties directly. We can temporarily instantiate standard default structures.
            temp_obj = event_cls(
                event_id="init_test", 
                tenant_id="SYSTEM", 
                correlation_id="init_test", 
                user_id="init_test"
            )
            name = temp_obj.event_name
            version = temp_obj.event_version
        except Exception as e:
            # Fallback to class name extraction if standard instantiator fails
            name = getattr(event_cls, "EVENT_NAME", None) or getattr(event_cls, "event_name", None)
            version = getattr(event_cls, "EVENT_VERSION", None) or getattr(event_cls, "event_version", "1.0.0")
            
            if not name or callable(name):
                # Prompt user error if naming attributes are completely missing
                raise EventRegistryError(
                    f"Candidate class {event_cls.__name__} must expose 'event_name' and 'event_version' constraints."
                ) from e

        key = self._get_key(name, version)
        
        with self._lock:
            if key in self._registry:
                existing_cls = self._registry[key]
                if existing_cls is not event_cls:
                    raise EventRegistryError(
                        f"Collision detected: Type combination '{name}:{version}' is already map bounded to "
                        f"'{existing_cls.__name__}'. Re-registration rejected."
                    )
            self._registry[key] = event_cls

    def resolve(self, event_name: str, event_version: str) -> Type[BaseEvent]:
        """
        Resolves a concrete BaseEvent subclass from catalog.
        """
        key = self._get_key(event_name, event_version)
        
        with self._lock:
            event_cls = self._registry.get(key)
            if not event_cls:
                # Try fallback: match only name with matching major version bounds if exact matches are unavailable
                major_version = event_version.split(".")[0]
                for (registered_name, registered_version), candidate_cls in self._registry.items():
                    if registered_name == key[0] and registered_version.split(".")[0] == major_version:
                        return candidate_cls
                
                raise EventRegistryError(
                    f"UnresolvedSchemaException: No registered event type maps to '{event_name}' with version '{event_version}'"
                )
            return event_cls

    def clear(self) -> None:
        """Flushes all mappings from memory. Primarily used for unit testing."""
        with self._lock:
            self._registry.clear()
