"""
Aurex Shared Events Framework.

An enterprise-ready, CNCF CloudEvents-compatible, schema-validating,
tenant-aware asynchronous event routing library designed for Apache Kafka and Azure Service Bus.
"""

from aurex.backend.shared.events.exceptions import (
    EventError,
    EventValidationError,
    EventSerializationError,
    EventRegistryError,
    EventPublishError,
    EventSubscriptionError,
)
from aurex.backend.shared.events.event_context import (
    EventContext,
)
from aurex.backend.shared.events.event_base import (
    BaseEvent,
)
from aurex.backend.shared.events.cloud_event import (
    CloudEvent,
)
from aurex.backend.shared.events.event_registry import (
    EventRegistry,
)
from aurex.backend.shared.events.event_serializer import (
    EventSerializer,
)
from aurex.backend.shared.events.event_factory import (
    EventFactory,
)
from aurex.backend.shared.events.event_publisher import (
    EventPublisher,
    KafkaEventPublisher,
    AzureServiceBusEventPublisher,
)
from aurex.backend.shared.events.event_subscriber import (
    EventSubscriber,
)

__all__ = [
    # Custom Exceptions
    "EventError",
    "EventValidationError",
    "EventSerializationError",
    "EventRegistryError",
    "EventPublishError",
    "EventSubscriptionError",
    
    # Event Context
    "EventContext",
    
    # Base Event contracts
    "BaseEvent",
    "CloudEvent",
    
    # Registries & Serializers
    "EventRegistry",
    "EventSerializer",
    "EventFactory",
    
    # Publisher adaptions
    "EventPublisher",
    "KafkaEventPublisher",
    "AzureServiceBusEventPublisher",
    
    # Consumer limits
    "EventSubscriber",
]
