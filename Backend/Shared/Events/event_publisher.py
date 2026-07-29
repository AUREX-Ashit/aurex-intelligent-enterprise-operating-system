"""
Aurex Shared Events Framework - Event Publisher Module.

Declares abstract integration adapters and architectural interfaces for publishing
events across disparate enterprise message brokers (such as Apache Kafka and Azure Service Bus).
"""

from abc import ABC, abstractmethod
import logging
from typing import Any, Dict, List, Optional, Tuple, TYPE_CHECKING, Union

from aurex.backend.shared.events.event_base import BaseEvent
from aurex.backend.shared.events.cloud_event import CloudEvent
from aurex.backend.shared.events.event_serializer import EventSerializer
from aurex.backend.shared.events.exceptions import EventPublishError

# Fetch core logger proxy
logger = logging.getLogger("cs.events.publisher")


class EventPublisher(ABC):
    """
    Abstract Port for outbound event adapters.
    Microservices inject this abstraction, decoupling domain behaviors from brokers.
    """

    def __init__(self, service_name: str, serializer: Optional[EventSerializer] = None) -> None:
        self.service_name = service_name
        self.serializer = serializer or EventSerializer()

    @abstractmethod
    def publish(self, event: BaseEvent, destination: str, partition_key: Optional[str] = None) -> None:
        """
        Synchronously encodes and dispatches the domain event package to a broker.
        """
        pass

    @abstractmethod
    async def publish_async(self, event: BaseEvent, destination: str, partition_key: Optional[str] = None) -> None:
        """
        Asynchronously encodes and dispatches the domain event package.
        """
        pass

    @abstractmethod
    def publish_batch(self, events: List[BaseEvent], destination: str) -> None:
        """
        Dispatches multiple event logs in a single structural transactional broker block.
        """
        pass


class KafkaEventPublisher(EventPublisher):
    """
    Production-grade Kafka Event Publisher design wrapper.
    Converts CloudEvents into raw byte messages, mapping corporate context attributes (correlationid,
    tenantid) directly onto Kafka Message Headers and routing queries strictly by Partition Keys.
    """

    def __init__(
        self,
        service_name: str,
        bootstrap_servers: Union[str, List[str]],
        serializer: Optional[EventSerializer] = None,
        kafka_producer_config: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(service_name=service_name, serializer=serializer)
        self.bootstrap_servers = bootstrap_servers
        self.config = kafka_producer_config or {}
        
        # In actual deployment, import 'confluent_kafka' or 'kafka-python'
        # Self._producer = Producer({"bootstrap.servers": self.bootstrap_servers, **self.config})
        logger.info(
            f"Kafka Event Publisher configured for Service: '{service_name}' on brokers: '{bootstrap_servers}'"
        )

    def _prepare_fields(self, event: BaseEvent) -> Tuple[bytes, bytes, List[Tuple[str, bytes]]]:
        """Maps standard CloudEvent wrappers into Kafka-native message objects."""
        envelope = CloudEvent.wrap(event=event, source_service=self.service_name)
        serialized_bytes = self.serializer.serialize_cloud_event(envelope, to_bytes=True)
        
        # Enforce Partition key preservation. Pinning to tenant_id guarantees message ordering
        # constraint checks inside a single tenant execution domain in Kafka partitions.
        routing_key = bytes(event.tenant_id, "utf-8")
        
        # Serialize CloudEvent meta context extensions to bytes headers
        headers = [
            ("ce_specversion", b"1.0"),
            ("ce_id", bytes(envelope.id, "utf-8")),
            ("ce_source", bytes(envelope.source, "utf-8")),
            ("ce_type", bytes(envelope.type, "utf-8")),
            ("ce_tenantid", bytes(envelope.tenantid or "SYSTEM", "utf-8")),
            ("ce_correlationid", bytes(envelope.correlationid or "", "utf-8")),
            ("ce_userid", bytes(envelope.userid or "ANONYMOUS", "utf-8")),
        ]
        
        return cast_bytes(serialized_bytes), routing_key, headers

    def publish(self, event: BaseEvent, destination: str, partition_key: Optional[str] = None) -> None:
        """Publishes event to a specific Kafka Topic synchronous."""
        try:
            payload, resolved_key, headers = self._prepare_fields(event)
            p_key = bytes(partition_key, "utf-8") if partition_key else resolved_key
            
            logger.debug(
                f"[Kafka:Publish] Sending Event '{event.event_name}' [id: {event.event_id}] "
                f"to Topic '{destination}' PartitionKey: '{p_key.decode()}'"
            )
            
            # --- MOCK OUTBOUND BROADCAST FOR ARCHITECTURE STAGE ---
            # self._producer.produce(topic=destination, key=p_key, value=payload, headers=headers)
            # self._producer.flush()
            
        except Exception as kafka_err:
            raise EventPublishError(
                f"Kafka producer failed to dispatch event '{event.event_name}': {str(kafka_err)}"
            ) from kafka_err

    async def publish_async(self, event: BaseEvent, destination: str, partition_key: Optional[str] = None) -> None:
        """Non-blocking asynchronous publish loop mapping asyncio loops to Kafka queues."""
        # Under async architectures, run producing on threadpools or use 'aiokafka'
        # In mock stage, simply run the synchronous publish loop
        self.publish(event, destination, partition_key)

    def publish_batch(self, events: List[BaseEvent], destination: str) -> None:
        """Transactional batch producer execution pipeline."""
        try:
            logger.info(f"[Kafka:Batch] Publishing {len(events)} events sequence, topic={destination}")
            for ev in events:
                self.publish(ev, destination)
        except Exception as err:
            raise EventPublishError(f"Kafka Batch dispatch failed: {str(err)}") from err


class AzureServiceBusEventPublisher(EventPublisher):
    """
    Production-grade Azure Service Bus Publisher design wrapper.
    Converts CloudEvents into native Service Bus messages, utilizing sessionId for multi-tenant
    strict order alignment, subject for event topic categorization, and applicationProperties
    for custom payload routing metrics.
    """

    def __init__(
        self,
        service_name: str,
        connection_string: str,
        serializer: Optional[EventSerializer] = None,
    ) -> None:
        super().__init__(service_name=service_name, serializer=serializer)
        self.connection_string = connection_string
        
        # In real deployment, import azure.servicebus:
        # self._client = ServiceBusClient.from_connection_string(conn_str=self.connection_string)
        logger.info(f"Azure Service Bus Publisher configured for service '{service_name}'")

    def _prepare_service_bus_message(self, event: BaseEvent) -> Dict[str, Any]:
        """Prepares a property dictionary modeling an azure.servicebus.ServiceBusMessage."""
        envelope = CloudEvent.wrap(event=event, source_service=self.service_name)
        serialized_bytes = self.serializer.serialize_cloud_event(envelope, to_bytes=True)

        return {
            "body": serialized_bytes,
            "message_id": envelope.id,
            "subject": envelope.type, # Map event.name directly to Subject header field
            "session_id": envelope.tenantid, # Enable session-locking FIFO capabilities per tenant
            "correlation_id": envelope.correlationid,
            "application_properties": {
                "source": envelope.source,
                "tenantid": envelope.tenantid or "SYSTEM",
                "userid": envelope.userid or "ANONYMOUS",
                "datacontentversion": envelope.datacontentversion
            }
        }

    def publish(self, event: BaseEvent, destination: str, partition_key: Optional[str] = None) -> None:
        """Synchronously pushes message to Service Bus Queue or Topic."""
        try:
            msg_properties = self._prepare_service_bus_message(event)
            if partition_key:
                msg_properties["session_id"] = partition_key

            logger.debug(
                f"[ServiceBus:Publish] Sending Event '{event.event_name}' [id: {event.event_id}] "
                f"to Queue/Topic '{destination}' [SessionId: {msg_properties['session_id']}]"
            )

            # In actual SDK:
            # sender = self._client.get_topic_sender(topic_name=destination)
            # msg = ServiceBusMessage(**msg_properties)
            # sender.send_messages(msg)

        except Exception as sb_err:
            raise EventPublishError(
                f"Azure Service Bus publisher failed to execute: {str(sb_err)}"
            ) from sb_err

    async def publish_async(self, event: BaseEvent, destination: str, partition_key: Optional[str] = None) -> None:
        """Asynchronously dispatches message leveraging async Azure SDK loops."""
        self.publish(event, destination, partition_key)

    def publish_batch(self, events: List[BaseEvent], destination: str) -> None:
        """Publishes multiple events transactionally using Service Bus batching buffers."""
        try:
            logger.info(f"[ServiceBus:Batch] Loading batch of {len(events)} limits onto queue '{destination}'")
            # In actual SDK:
            # sender = self._client.get_topic_sender(topic_name=destination)
            # batch = sender.create_message_batch()
            # for event in events:
            #     batch.try_add_message(ServiceBusMessage(**self._prepare_service_bus_message(event)))
            # sender.send_messages(batch)
            for ev in events:
                self.publish(ev, destination)
        except Exception as err:
            raise EventPublishError(f"Azure Service Bus Batch dispatch failed: {str(err)}") from err


def cast_bytes(val: Union[str, bytes]) -> bytes:
    """Type-safe normalization to bytes."""
    if isinstance(val, str):
        return val.encode("utf-8")
    return val
