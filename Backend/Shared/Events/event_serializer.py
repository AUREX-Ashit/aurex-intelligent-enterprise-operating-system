"""
Aurex Shared Events Framework - Event Serializer.

Implements highly-performant JSON serialization and deserialization adapters for
structured event envelopes, protecting transport streams from binary conversion failures.
"""

import json
import datetime
from typing import Any, Dict, Optional, Union

from aurex.backend.shared.events.event_base import BaseEvent
from aurex.backend.shared.events.cloud_event import CloudEvent
from aurex.backend.shared.events.event_registry import EventRegistry
from aurex.backend.shared.events.exceptions import EventSerializationError


class DecimalAndDateEncoder(json.JSONEncoder):
    """Fallback JSON encoder serialization helper for advanced types like decimals and datetimes."""
    def default(self, obj: Any) -> Any:
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        try:
            from decimal import Decimal
            if isinstance(obj, Decimal):
                return float(obj)
        except ImportError:
            pass
        return super().default(obj)


class EventSerializer:
    """
    Serializer interface enabling safe transformation of Python event structures
    into wire-level raw representations (strings/bytes).
    """

    def __init__(self, registry: Optional[EventRegistry] = None) -> None:
        self.registry = registry or EventRegistry()

    def serialize_cloud_event(self, cloud_event: CloudEvent, to_bytes: bool = False) -> Union[str, bytes]:
        """
        Encodes a CNCF CloudEvent wrapper into a standard JSON representation.
        """
        try:
            dictionary_format = cloud_event.to_dict()
            json_string = json.dumps(dictionary_format, cls=DecimalAndDateEncoder)
            return json_string.encode("utf-8") if to_bytes else json_string
        except Exception as err:
            raise EventSerializationError(
                f"Failed to serialize CloudEvent envelope to wire format: {str(err)}"
            ) from err

    def deserialize_cloud_event(self, source_payload: Union[str, bytes]) -> CloudEvent:
        """
        Decodes incoming byte streams or raw strings back into a validated CloudEvent snapshot.
        """
        try:
            decoded_string = (
                source_payload.decode("utf-8") if isinstance(source_payload, bytes) else source_payload
            )
            dictionary_format = json.loads(decoded_string)
            return CloudEvent.from_dict(dictionary_format)
        except Exception as err:
            raise EventSerializationError(
                f"Failed to deserialize inbound byte streams into a validated CloudEvent: {str(err)}"
            ) from err

    def serialize_domain_event(
        self,
        domain_event: BaseEvent,
        source_service: str,
        subject: Optional[str] = None,
        to_bytes: bool = False,
    ) -> Union[str, bytes]:
        """
        Directly wraps and serializes a native domain event into a CloudEvent payload.
        """
        wrapped_envelope = CloudEvent.wrap(
            event=domain_event,
            source_service=source_service,
            subject=subject
        )
        return self.serialize_cloud_event(wrapped_envelope, to_bytes=to_bytes)

    def deserialize_domain_event(self, source_payload: Union[str, bytes]) -> BaseEvent:
        """
        Deserializes a raw event payload, resolves its schema from registry, and unrolls
        the completely re-hydrated strongly-typed concrete BaseEvent instantly.
        """
        cloud_envelope = self.deserialize_cloud_event(source_payload)
        try:
            return cloud_envelope.unwrap(self.registry)
        except Exception as registry_err:
            raise EventSerializationError(
                f"Completed bytes decoding but failed to resolve dynamic domain mappings from registry: "
                f"{str(registry_err)}"
            ) from registry_err
