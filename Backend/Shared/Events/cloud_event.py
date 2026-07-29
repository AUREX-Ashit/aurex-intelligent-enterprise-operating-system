"""
Aurex Shared Events Framework - CNCF CloudEvents Module.

Provides standard v1.0 CloudEvents wrapper envelopes for cross-service messages, Ensure
interoperability on standard routers and brokers like Kafka, RabbitMQ, and Azure Service Bus.
"""

import datetime
import json
from typing import Any, Dict, Optional, Type, TYPE_CHECKING

from aurex.backend.shared.events.exceptions import EventValidationError
from aurex.backend.shared.events.event_base import BaseEvent

if TYPE_CHECKING:
    from aurex.backend.shared.events.event_registry import EventRegistry


class CloudEvent:
    """
    Representation of a CNCF CloudEvents v1.0 compliant wrapper envelope.
    Includes lowercase extension attributes to bypass modern broker transport limits.
    """

    SPEC_VERSION: str = "1.0"

    def __init__(
        self,
        id: str,
        source: str,
        type: str,
        data: Dict[str, Any],
        time: Optional[datetime.datetime] = None,
        subject: Optional[str] = None,
        datacontenttype: str = "application/json",
        # Corporate Context Extensions (must be strictly lowercase alphanumeric per CNCF Spec)
        correlationid: Optional[str] = None,
        tenantid: Optional[str] = None,
        userid: Optional[str] = None,
        datacontentversion: str = "1.0.0",
        extensions: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.id = id
        self.source = source
        self.type = type
        self.data = data
        self.time = time or datetime.datetime.now(datetime.timezone.utc)
        self.subject = subject
        self.datacontenttype = datacontenttype
        self.datacontentversion = datacontentversion
        
        # Core Extensions
        self.correlationid = correlationid
        self.tenantid = tenantid
        self.userid = userid
        
        self.extensions: Dict[str, Any] = extensions or {}

    @classmethod
    def wrap(cls, event: BaseEvent, source_service: str, subject: Optional[str] = None) -> "CloudEvent":
        """
        Wraps a Aurex BaseEvent inside a CNCF standard envelope.
        """
        event.validate() # Enforce schema checks prior to routing
        return cls(
            id=event.event_id,
            source=f"aurex://services/{source_service}",
            type=event.event_name,
            data=event.to_dict(),
            time=event.timestamp,
            subject=subject or f"tenant/{event.tenant_id}",
            correlationid=event.correlation_id,
            tenantid=event.tenant_id,
            userid=event.user_id,
            datacontentversion=event.event_version
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Serializes CloudEvent envelope structure into standard JSON-compliant dictionary map.
        """
        payload: Dict[str, Any] = {
            "specversion": self.SPEC_VERSION,
            "id": self.id,
            "source": self.source,
            "type": self.type,
            "subject": self.subject,
            "time": self.time.isoformat() if isinstance(self.time, datetime.datetime) else self.time,
            "datacontenttype": self.datacontenttype,
            "datacontentversion": self.datacontentversion,
            "data": self.data,
        }

        # Inject standard CNCF CloudEvent Extensions
        if self.correlationid:
            payload["correlationid"] = self.correlationid
        if self.tenantid:
            payload["tenantid"] = self.tenantid
        if self.userid:
            payload["userid"] = self.userid

        # Inject other custom extensions if supplied
        for key, value in self.extensions.items():
            normalized_key = key.lower().replace("_", "").replace("-", "")
            payload[normalized_key] = value

        return payload

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CloudEvent":
        """
        De-serializes a dictionary to construct a CloudEvent envelope.
        """
        # Validate mandatory properties according to CNCF specifications
        mandatory = ["specversion", "id", "source", "type", "data"]
        for field in mandatory:
            if field not in data:
                raise EventValidationError(f"Invalid CloudEvent payload: missing mandatory property '{field}'")

        if data["specversion"] != cls.SPEC_VERSION:
            raise EventValidationError(f"Unsupported CloudEvent specversion: '{data['specversion']}'")

        # Parse timing formats
        time_val = None
        if "time" in data:
            try:
                time_val = datetime.datetime.fromisoformat(data["time"].replace("Z", "+00:00"))
            except Exception:
                time_val = data["time"]

        extensions = {}
        standard_keys = {
            "specversion", "id", "source", "type", "data", "time", "subject",
            "datacontenttype", "datacontentversion", "correlationid", "tenantid", "userid"
        }
        for key, val in data.items():
            if key not in standard_keys:
                extensions[key] = val

        return cls(
            id=data["id"],
            source=data["source"],
            type=data["type"],
            data=data["data"],
            time=time_val,
            subject=data.get("subject"),
            datacontenttype=data.get("datacontenttype", "application/json"),
            correlationid=data.get("correlationid"),
            tenantid=data.get("tenantid"),
            userid=data.get("userid"),
            datacontentversion=data.get("datacontentversion", "1.0.0"),
            extensions=extensions,
        )

    def unwrap(self, registry: "EventRegistry") -> BaseEvent:
        """
        Resolves physical event mappings via EventRegistry, rebuilding the
        concrete strongly-typed BaseEvent with fully populated contexts.
        """
        # EventRegistry is solved using dynamic typing
        event_class = registry.resolve(self.type, self.datacontentversion)
        
        # Gather all attributes, overriding payload bounds safely
        hydrated_data = {
            **self.data,
            "event_id": self.id,
            "timestamp": self.time if isinstance(self.time, datetime.datetime) else datetime.datetime.fromisoformat(self.time),
            "correlation_id": self.correlationid,
            "tenant_id": self.tenantid,
            "user_id": self.userid,
        }
        
        event_object = event_class.from_dict(hydrated_data)
        return event_object

    def __repr__(self) -> str:
        return f"<CloudEvent spec={self.SPEC_VERSION} id={self.id} type={self.type} source={self.source}>"
