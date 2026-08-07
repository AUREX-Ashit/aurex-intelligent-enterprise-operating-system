"""
WP-12 — AI Conversation Management (C-094). Local observability primitive.

REUSE NOTE (Mandatory Implementation Contract): Backend/Shared/Logging
(LoggerFactory, AuditLogger, CorrelationContext) is the platform's intended
shared framework for exactly this purpose and was evaluated first, per
Reuse before Create. It cannot currently be imported — every module in
Backend/Shared/Logging imports from the package path
`aurex.backend.shared...`, but no `aurex` package exists anywhere in this
repository — the same pre-existing, platform-wide defect
`Backend/Services/AuthService/observability.py`'s own module docstring
already discloses (WP-00 Platform Bootstrap). Fixing it is out of this
Work Package's own scope.

`SER-001 SE-035` already tracks that `record_audit` was never wired into
AIService by any prior Work Package (WP-11 inherited, did not close, this
gap). `TDS-012 §8` determined that wiring it for WP-12's own BA-01/BA-02
state-changing actions is in scope, not deferrable Technical Debt, since
leaving AI-Conversation-specific actions unaudited would be a
`CLAUDE.md §19.8.5`-class gap. This module is therefore a second,
mechanical instance of AuthService's own local-substitute pattern —
deliberately mirroring its design (contextvars-based correlation context,
the same `AuditStatus` vocabulary, the same `record_audit` signature) so
that migrating both services to the shared framework later, once its
import paths are fixed, is one mechanical change applied twice, not two
separate designs to reconcile.
"""

from __future__ import annotations

import json
import logging
from contextvars import ContextVar
from enum import Enum
from typing import Any, Optional
from uuid import uuid4

_correlation_id: ContextVar[Optional[str]] = ContextVar("correlation_id", default=None)

_audit_logger = logging.getLogger("aiservice.audit")


class CorrelationContext:
    """Task-local correlation ID, mirroring AuthService's observability.py's own contextvars design."""

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
    """Mirrors AuthService's observability.py's own AuditStatus vocabulary exactly."""
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
