"""
WP-00 Platform Bootstrap — local observability primitives.

REUSE NOTE (Mandatory Implementation Contract): Backend/Shared/Logging
(LoggerFactory, AuditLogger, CorrelationContext) and Backend/Shared/Events
(EventPublisher, CloudEvent) are the platform's intended shared frameworks
for exactly this purpose and were evaluated first, per Reuse before Create.
They cannot currently be imported: every module in Backend/Shared/Logging
and Backend/Shared/Events imports from the package path
`aurex.backend.shared...`, but no `aurex` package exists anywhere
in this repository (no setup.py/pyproject.toml, no matching directory
structure) — the import fails immediately (`ModuleNotFoundError`). This is
a pre-existing defect, not introduced by WP-00. Fixing it is a platform-wide
concern spanning AIService, IngestionService, ReportingService, and
TenantService as well as AuthService, which is out of WP-00's "Platform
Bootstrap" scope. This module is a minimal, explicitly temporary local
substitute, deliberately mirroring Backend/Shared/Logging's own design
(contextvars-based correlation context, structured audit records with the
same AuditStatus vocabulary) so that migrating callers to the shared
framework later — once its import paths are fixed — is a mechanical,
low-risk change, not a redesign.
"""

from __future__ import annotations

import json
import logging
import time
from contextvars import ContextVar
from enum import Enum
from typing import Any, Optional
from uuid import uuid4

_correlation_id: ContextVar[Optional[str]] = ContextVar("correlation_id", default=None)

_audit_logger = logging.getLogger("authservice.audit")
_event_logger = logging.getLogger("authservice.events")
_metrics_logger = logging.getLogger("authservice.metrics")


class CorrelationContext:
    """Task-local correlation ID, mirroring Backend/Shared/Logging's contextvars design."""

    @classmethod
    def new(cls) -> str:
        value = str(uuid4())
        _correlation_id.set(value)
        return value

    @classmethod
    def get(cls) -> Optional[str]:
        return _correlation_id.get()

    @classmethod
    def set(cls, value: str) -> None:
        _correlation_id.set(value)


class AuditStatus(str, Enum):
    """Mirrors Backend/Shared/Logging/audit_logger.py's AuditStatus vocabulary."""
    SUCCESS = "SUCCESS"
    DENIED = "DENIED"
    FAILED = "FAILED"


def record_audit(
    action: str,
    resource: str,
    status: AuditStatus,
    actor_id: str = "SYSTEM",
    tenant_id: Optional[str] = None,
    metadata: Optional[dict[str, Any]] = None,
) -> None:
    """
    Emits one structured, append-only audit record per SD-002-054's seven
    questions (Who, What, Why, When, How, Using Which Evidence, Under Which
    Policy) — 'Who'=actor_id, 'What'=action/resource, 'When'=timestamp (added
    by the log formatter), 'How'/'Evidence'/'Policy' carried in metadata.
    """
    payload = {
        "audit": True,
        "action": action.upper(),
        "resource": resource,
        "status": status.value,
        "actor_id": actor_id,
        "tenant_id": tenant_id or "PLATFORM",
        "correlation_id": CorrelationContext.get(),
        "metadata": metadata or {},
    }
    _audit_logger.info(json.dumps(payload))


def publish_event(event_type: str, payload: dict[str, Any]) -> None:
    """
    Emits one structured Domain Event record, following the naming and
    intent already established by RTA-001 §22.12 (Runtime Events) and
    SD-002-052 (event-sourcing principle): every state transition generates
    an immutable, observable event. This is a structured-log-based stand-in
    for Backend/Shared/Events' EventPublisher/CloudEvent abstraction (see
    module docstring) — the event *shape* (type + payload + correlation)
    is compatible with CloudEvent's own fields, so migrating to a real
    broker-backed publisher later requires no change to callers of this
    function's signature.
    """
    record = {
        "event": True,
        "event_type": event_type,
        "correlation_id": CorrelationContext.get(),
        "payload": payload,
    }
    _event_logger.info(json.dumps(record))


def record_metric(name: str, value: float, tags: Optional[dict[str, str]] = None) -> None:
    """
    Emits one structured metric line. A dependency-light stand-in for a
    Prometheus/OpenTelemetry metrics client — genuine metrics-backend
    integration is a platform-wide infrastructure concern beyond WP-00's
    bootstrap scope (no metrics client is listed in requirements.txt for
    any service in this repository today). The structured shape below
    (name/value/tags) already matches the label model a real client would
    use, so this is a mechanical swap later, not a redesign.
    """
    _metrics_logger.info(json.dumps({"metric": True, "name": name, "value": value, "tags": tags or {}}))


class Timer:
    """Context manager measuring elapsed seconds, for latency metrics."""

    def __init__(self) -> None:
        self._start: float = 0.0
        self.elapsed_seconds: float = 0.0

    def __enter__(self) -> "Timer":
        self._start = time.perf_counter()
        return self

    def __exit__(self, *_exc: object) -> None:
        self.elapsed_seconds = time.perf_counter() - self._start
