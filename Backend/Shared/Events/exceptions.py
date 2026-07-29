"""
Aurex Shared Events Framework - Exceptions Module.

Provides custom, strongly-typed enterprise exceptions for event lifecycle stages,
including context validation, serialization failures, and network dispatch bounds.
"""

class EventError(Exception):
    """Base exception for all event-related errors in the Aurex Events Framework."""
    pass


class EventValidationError(EventError):
    """Raised when an event payload fails validation schema or version bounds constraints."""
    pass


class EventSerializationError(EventError):
    """Raised when serializer adapters fail to encode or decode event stream payloads."""
    pass


class EventRegistryError(EventError):
    """Raised when event schema types or names conflict or are missing from the Event Registry."""
    pass


class EventPublishError(EventError):
    """Raised when publisher adapters encounter dispatch-level issues with downstream brokers."""
    pass


class EventSubscriptionError(EventError):
    """Raised when subscriber listeners crash or fail during event packet consumption."""
    pass
