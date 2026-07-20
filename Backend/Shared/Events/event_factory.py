"""
CorpStage Shared Events Framework - Event Factory Module.

Provides flexible, fluent builder APIs and factory interfaces to construct
fully contextualized domain event definitions and generic messages.
"""

from typing import Any, Dict, Optional, Type

from corpstage.backend.shared.events.event_base import BaseEvent
from corpstage.backend.shared.events.cloud_event import CloudEvent
from corpstage.backend.shared.events.event_context import EventContext


class EventFactory:
    """
    Constructs contextualized domain events and standard CloudEvents envelopes.
    """

    @classmethod
    def create_custom_event(
        cls,
        event_class: Type[BaseEvent],
        *args: Any,
        tenant_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        user_id: Optional[str] = None,
        **kwargs: Any,
    ) -> BaseEvent:
        """
        Builds a concrete strongly-typed BaseEvent subclass instance.
        Resolves tracking headers, and injects context parameters seamlessly.
        """
        # Resolve active tracing context fallbacks
        context = EventContext.export_context()
        
        resolved_tenant = tenant_id or context.get("tenant_id") or "SYSTEM"
        resolved_correlation = correlation_id or context.get("correlation_id")
        resolved_user = user_id or context.get("user_id") or "ANONYMOUS"

        # Construct and validate physical payload object
        event_instance = event_class(
            *args,
            tenant_id=resolved_tenant,
            correlation_id=resolved_correlation,
            user_id=resolved_user,
            **kwargs
        )
        event_instance.validate()
        return event_instance

    @classmethod
    def create_envelope(
        cls,
        domain_event: BaseEvent,
        source_service: str,
        subject: Optional[str] = None,
    ) -> CloudEvent:
        """
        Wraps a domain event inside a standard CNCF CloudEvent envelope.
        """
        return CloudEvent.wrap(
            event=domain_event,
            source_service=source_service,
            subject=subject
        )
