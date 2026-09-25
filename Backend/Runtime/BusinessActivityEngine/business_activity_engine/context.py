"""
Business Activity Engine -- invocation and execution context (WP-BAE-001 M1).

`BusinessActivityInvocation` is the transport-independent request an
invoker (FastAPI adapter, event subscriber, scheduler, AI caller --
`IMP-001 §6.15.3`) hands to the engine. It carries identity and
organization derived from the caller's authenticated claims, never from
the payload (`§6.17.7`; `CLAUDE.md §21.4`). Callers never supply a
pre-built context (`§6.16.6`).

`BusinessActivityContext` is constructed once, by the engine only, and
is immutable (`§6.17.2`, `§6.17.16`). `ContextSection` names
`§6.17.5`'s ten canonical sections. M1 populates only the sections
with a real source; the rest are reported unavailable, never fabricated
(`IRA-BAE-001-M1 §7`, C5). Full context construction is M3.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from types import MappingProxyType

from .identity import BusinessActivityIdentifier


class ContextSection(str, Enum):
    """`IMP-001 §6.17.5` canonical context sections."""

    ACTIVITY = "ACTIVITY"
    IDENTITY = "IDENTITY"
    ORGANIZATION = "ORGANIZATION"
    ENTERPRISE = "ENTERPRISE"
    AUTHORIZATION = "AUTHORIZATION"
    WORKFLOW = "WORKFLOW"
    REQUEST = "REQUEST"
    TRANSACTION = "TRANSACTION"
    AI = "AI"
    RUNTIME = "RUNTIME"


@dataclass(frozen=True)
class BusinessActivityInvocation:
    """A request to execute one BAR-registered Business Activity."""

    identifier: BusinessActivityIdentifier
    identity_id: str
    organization_id: str
    membership_id: str | None = None
    session_id: str | None = None
    correlation_id: str | None = None
    payload: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.identifier, BusinessActivityIdentifier):
            raise TypeError("identifier must be a BusinessActivityIdentifier (a BAR-issued BA-NNNNNN value).")
        object.__setattr__(self, "payload", MappingProxyType(dict(self.payload)))


@dataclass(frozen=True)
class BusinessActivityContext:
    """The immutable execution context (M1 subset of `§6.17`)."""

    identifier: BusinessActivityIdentifier
    identity_id: str
    organization_id: str
    membership_id: str | None
    session_id: str | None
    correlation_id: str
    started_at: datetime

    AVAILABLE_SECTIONS = (
        ContextSection.ACTIVITY,
        ContextSection.IDENTITY,
        ContextSection.ORGANIZATION,
        ContextSection.RUNTIME,
    )
    """Sections M1 has a real source for: identifier; caller identity/membership/session; organization; correlation/start time."""

    @property
    def unavailable_sections(self) -> tuple[ContextSection, ...]:
        return tuple(section for section in ContextSection if section not in self.AVAILABLE_SECTIONS)
