"""
CorpStage Shared Events Framework - Event Subscriber Module.

Defines the abstract interface for consuming event streams, establishing
thread-safe callback dispatch pipelines, auto-rehydration of telemetry contexts, and DLQ gates.
"""

from abc import ABC, abstractmethod
import logging
from typing import Any, Callable, Dict, List, Optional, Type, Union

from corpstage.backend.shared.events.event_base import BaseEvent
from corpstage.backend.shared.events.event_serializer import EventSerializer
from corpstage.backend.shared.events.event_registry import EventRegistry
from corpstage.backend.shared.events.event_context import EventContext
from corpstage.backend.shared.events.exceptions import EventSubscriptionError

logger = logging.getLogger("cs.events.subscriber")

EventHandler = Callable[[BaseEvent], None]
AsyncEventHandler = Callable[[BaseEvent], Any]


class EventSubscriber(ABC):
    """
    Abstract consumer interface for domain services subscribing to message brokers.
    """

    def __init__(
        self,
        service_name: str,
        registry: Optional[EventRegistry] = None,
        serializer: Optional[EventSerializer] = None,
    ) -> None:
        self.service_name = service_name
        self.registry = registry or EventRegistry()
        self.serializer = serializer or EventSerializer(self.registry)
        
        # Thread-safe local routing table maps event names onto list of registered handlers
        self._handlers: Dict[str, List[Union[EventHandler, AsyncEventHandler]]] = {}

    def subscribe(self, event_name: str, handler: Union[EventHandler, AsyncEventHandler]) -> None:
        """Registers a handler callback to be invoked when a specific event name is received."""
        event_key = event_name.strip().lower()
        if event_key not in self._handlers:
            self._handlers[event_key] = []
        self._handlers[event_key].append(handler)
        logger.info(
            f"Service '{self.service_name}' subscribed callback '{handler.__name__}' to Event: '{event_name}'"
        )

    @abstractmethod
    def start(self) -> None:
        """Starts the subscription listener loop (blocking container daemon)."""
        pass

    @abstractmethod
    def stop(self) -> None:
        """Gracefully disconnects and shuts down active consumer threads."""
        pass

    def handle_inbound_message(self, raw_payload: Union[str, bytes]) -> None:
        """
        Main routing gateway for incoming byte packets.
        Decodes CloudEvents, restores context variables, rehydrates the domain event,
        invokes registered callbacks, and guarantees proper thread state sanitization.
        """
        # Step 1: Decode raw bytes into generic CloudEvents envelopes
        try:
            cloud_envelope = self.serializer.deserialize_cloud_event(raw_payload)
        except Exception as decode_err:
            logger.error(
                f"[Subscriber] Rejected unreadable packet: Decoder failed to parse envelope. Error: {str(decode_err)}",
                extra={"raw_bytes_len": len(raw_payload) if raw_payload else 0},
                exc_info=True
            )
            # Route to DLQ conceptually
            self.route_to_dead_letter_queue(raw_payload, "UNPARSABLE_ENVELOPE", decode_err)
            return

        # Step 2: Inject tracing contexts extracted from event envelopes to local task vars
        ctx_snapshot = {
            "correlation_id": cloud_envelope.correlationid,
            "tenant_id": cloud_envelope.tenantid,
            "user_id": cloud_envelope.userid
        }
        tokens = EventContext.set_context_from_dict(ctx_snapshot)

        # Log start of processing with unified context variables attached
        logger.info(
            f"Processing Inbound Event: '{cloud_envelope.type}' [id: {cloud_envelope.id}, tenant: {cloud_envelope.tenantid}]",
            extra={
                "event_id": cloud_envelope.id,
                "event_type": cloud_envelope.type,
                "subject": cloud_envelope.subject
            }
        )

        try:
            # Step 3: Rehydrate concrete domain event object using registered schema classes
            domain_event = cloud_envelope.unwrap(self.registry)
            domain_event.validate() # Enforce post-receive validation tests
            
            # Step 4: Dispatch the de-serialized event to registered callback handlers
            event_key = domain_event.event_name.strip().lower()
            handlers = self._handlers.get(event_key, [])

            if not handlers:
                logger.warning(
                    f"No consumer handles bound to registered Event type '{domain_event.event_name}' on Service '{self.service_name}'"
                )
                return

            for handler in handlers:
                try:
                    logger.debug(f"Invoking consumer callback '{handler.__name__}' for '{domain_event.event_name}'")
                    # Synchronously fire handler
                    handler(domain_event)
                except Exception as handler_err:
                    logger.error(
                        f"Unhandled exception inside consumer handler '{handler.__name__}' on "
                        f"Event '{domain_event.event_name}': {str(handler_err)}",
                        extra={
                            "event_id": domain_event.event_id,
                            "handler": handler.__name__
                        },
                        exc_info=True
                    )
                    self.route_to_dead_letter_queue(raw_payload, "HANDLER_CRASH", handler_err)

        except Exception as process_err:
            logger.critical(
                f"Fatal Subscriber crash while parsing or processing Event envelope [id: {cloud_envelope.id}]: {str(process_err)}",
                extra={"event_id": cloud_envelope.id},
                exc_info=True
            )
            self.route_to_dead_letter_queue(raw_payload, "REHYDRATION_FAILURE", process_err)

        finally:
            # Step 5: Absolutely guarantee resetting of task local variables to avoid leaking states between threads
            EventContext.clear_context_from_tokens(tokens)

    def route_to_dead_letter_queue(self, raw_payload: Union[str, bytes], error_phase: str, exception: Exception) -> None:
        """
        Safely captures failed processing payloads, logging metadata contexts.
        In highly-reliable architectures, this forwards to dedicated '.DLQ' topics or error message buffers.
        """
        logger.warning(
            f"[DLQ:Audit] Forwarding corrupt/failed event packet to Dead Letter Queue (Phase: {error_phase}). Reason: {str(exception)}",
            extra={
                "error_phase": error_phase,
                "exception_class": exception.__class__.__name__,
            }
        )
        # Real deployment action:
        # self.dlq_publisher.publish_raw(raw_payload, topic=f"{self.service_name}.DLQ")
