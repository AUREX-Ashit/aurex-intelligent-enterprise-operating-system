"""
CorpStage Shared Events Framework - Event Base Module.

Declares the parent abstract class and dataclass constraints defining
CorpStage messages, enforcing domain model versioning, state validation, and identity tracking.
"""

from abc import ABC, abstractmethod
import datetime
from typing import Dict, Any, Optional
import uuid

from corpstage.backend.shared.events.exceptions import EventValidationError
from corpstage.backend.shared.events.event_context import EventContext


class BaseEvent(ABC):
    """
    Abstract Base Class for all CorpStage domain events.
    Enforces unified tracking, standard naming schemas, and built-in contract validations.
    """

    def __init__(
        self,
        event_id: Optional[str] = None,
        timestamp: Optional[datetime.datetime] = None,
        correlation_id: Optional[str] = None,
        tenant_id: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> None:
        # Immutable Event Identification
        self.event_id: str = event_id or str(uuid.uuid4())
        self.timestamp: datetime.datetime = timestamp or datetime.datetime.now(datetime.timezone.utc)
        
        # Hydrate context values, prioritising provided triggers then falling back to task context variables
        context = EventContext.export_context()
        self.correlation_id: str = correlation_id or context.get("correlation_id") or str(uuid.uuid4())
        self.tenant_id: str = tenant_id or context.get("tenant_id") or "SYSTEM"
        self.user_id: str = user_id or context.get("user_id") or "ANONYMOUS"

    @property
    @abstractmethod
    def event_name(self) -> str:
        """
        Unique, dot-notated logical name identifier for the event schema definition.
        Example: "corpstage.auth.user.created" or "corpstage.ingestion.job.started"
        """
        pass

    @property
    @abstractmethod
    def event_version(self) -> str:
        """
        Semantic version identifier of the event payload schema.
        Example: "1.0.0" or "2.1.0"
        """
        pass

    @abstractmethod
    def validate(self) -> None:
        """
        Validates internal constraints and payload contracts.
        Should raise EventValidationError if parameters violate class state limits.
        """
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """
        Serializes internal payload attributes into primitive Python keys.
        """
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BaseEvent":
        """
        Re-hydrates the domain event from a dictionary payload.
        """
        pass

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} name={self.event_name} v={self.event_version} "
            f"id={self.event_id} tenant={self.tenant_id}>"
        )
