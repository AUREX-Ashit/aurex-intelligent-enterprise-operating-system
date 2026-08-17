# events/knowledge_asset_events.py
"""
WP-14 BA-04 Increment — Knowledge Asset Lifecycle Transition + `ACCEPTED`
Domain Event (`TDS-014 §8`/`§10`, `BA04-INC-DEC-006`).

Event contract is FROZEN by `TDS-014 §8` — `event_name`/`event_version`/
the four payload fields are not implementation discretion. This is the
first concrete `BaseEvent` subclass anywhere in this repository (no
precedent existed to reuse for envelope wiring beyond the framework's
own base classes, independently confirmed during Technical Design).

Represents the FACT "this Knowledge Asset transitioned to ACCEPTED" —
never a BA-05 command. BA-04 does not construct, and this class does not
carry, any Knowledge Graph relationship-creation instruction; that
belongs entirely to BA-05's own future, separately-authorized
`KnowledgeGraphSyncHandler` (`RO-DEC-WP14-BA05-02`, `TDS-014 §17`).

`knowledge_asset_id`/`organization_id` carry usable defaults so
`Backend/Shared/Events/event_registry.py::EventRegistry.register()`'s own
temp-instantiation probe (`event_cls(event_id=..., tenant_id=...,
correlation_id=..., user_id=...)`, no payload kwargs) succeeds without
falling back to its own class-attribute path — a real gap independently
identified during the BA-04 Increment's own final authorization review
(no other concrete `BaseEvent` subclass exists anywhere to have
previously surfaced it).
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict

_BACKEND_ROOT = Path(__file__).resolve().parents[3]
if str(_BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(_BACKEND_ROOT))

from aurex.backend.shared.events.event_base import BaseEvent
from aurex.backend.shared.events.event_registry import EventRegistry
from aurex.backend.shared.events.exceptions import EventValidationError


class KnowledgeAssetAcceptedEvent(BaseEvent):
    """`aurex.aiservice.knowledge_asset.accepted`, v`1.0.0` (`TDS-014 §8`)."""

    def __init__(
        self,
        knowledge_asset_id: str = "",
        organization_id: str = "",
        previous_status: str = "PROPOSED",
        new_status: str = "ACCEPTED",
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.knowledge_asset_id = knowledge_asset_id
        self.organization_id = organization_id
        self.previous_status = previous_status
        self.new_status = new_status

    @property
    def event_name(self) -> str:
        return "aurex.aiservice.knowledge_asset.accepted"

    @property
    def event_version(self) -> str:
        return "1.0.0"

    def validate(self) -> None:
        if not self.knowledge_asset_id:
            raise EventValidationError("knowledge_asset_id is required")
        if not self.organization_id:
            raise EventValidationError("organization_id is required")
        if self.previous_status != "PROPOSED":
            raise EventValidationError("previous_status must be 'PROPOSED' (TDS-014 §2 scope)")
        if self.new_status != "ACCEPTED":
            raise EventValidationError("new_status must be 'ACCEPTED' — this event represents no other outcome")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "knowledge_asset_id": self.knowledge_asset_id,
            "organization_id": self.organization_id,
            "previous_status": self.previous_status,
            "new_status": self.new_status,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "KnowledgeAssetAcceptedEvent":
        return cls(
            knowledge_asset_id=data["knowledge_asset_id"],
            organization_id=data["organization_id"],
            previous_status=data.get("previous_status", "PROPOSED"),
            new_status=data.get("new_status", "ACCEPTED"),
            event_id=data.get("event_id"),
            timestamp=data.get("timestamp"),
            correlation_id=data.get("correlation_id"),
            tenant_id=data.get("tenant_id"),
            user_id=data.get("user_id"),
        )


EventRegistry().register(KnowledgeAssetAcceptedEvent)
