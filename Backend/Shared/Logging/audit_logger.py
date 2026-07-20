"""
CorpStage Shared Logging Framework - Audit Logger Module.

Provides compliance-grade immutable audit trails capturing security-sensitive actions,
system administration operations, identity challenges, and data modifications.
"""

from typing import Any, Dict, Optional
from enum import Enum

from corpstage.backend.shared.logging.logger_factory import LoggerFactory
from corpstage.backend.shared.logging.correlation_context import CorrelationContext

# Fetch dedicated audit logger. In high-security systems, this logger can be
# routed to specialized append-only systems or secure SIEM channels like Azure Monitor.
audit_logger = LoggerFactory.get_logger("cs.security.audit")


class AuditStatus(str, Enum):
    """Reflects structural results of the auditable transaction."""
    SUCCESS = "SUCCESS"
    DENIED = "DENIED"
    FAILED = "FAILED"
    CHALLENGED = "CHALLENGED"


class AuditLogger:
    """
    Enterprise audit telemetry manager. Guarantees consistent capturing of
    actors, resource scopes, and authorization outcomes for compliance and SIEM auditing.
    """

    @classmethod
    def log(
        cls,
        action: str,
        resource: str,
        status: AuditStatus,
        actor_id: Optional[str] = None,
        tenant_id: Optional[str] = None,
        client_ip: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Submits structured audit trace record enclosing explicit security contexts.
        Attempts fallback resolution using global task-local contexts if parameters are omitted.
        """
        # Context extraction fallbacks
        resolved_actor = actor_id or CorrelationContext.get_user_id() or "ANONYMOUS"
        resolved_tenant = tenant_id or CorrelationContext.get_tenant_id() or "SYSTEM"
        
        audit_payload = {
            "audit_marker": True,
            "action": action.upper(),
            "resource": resource,
            "status": status.value,
            "actor_id": resolved_actor,
            "tenant_id": resolved_tenant,
            "client_ip": client_ip or "0.0.0.0",
            "metadata": metadata or {}
        }

        log_message = (
            f"Audit Log: Actor [{resolved_actor}] executed [{action.upper()}] "
            f"on Resource [{resource}] under Tenant [{resolved_tenant}] -> Status [{status.value}]"
        )

        # Escalate log level based on action failure bounds
        if status in [AuditStatus.DENIED, AuditStatus.FAILED]:
            audit_logger.warning(log_message, extra=audit_payload)
        else:
            audit_logger.info(log_message, extra=audit_payload)

    @classmethod
    def log_success(
        cls,
        action: str,
        resource: str,
        actor_id: Optional[str] = None,
        tenant_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Convenience wrapper for routine successful auditable interactions."""
        cls.log(
            action=action,
            resource=resource,
            status=AuditStatus.SUCCESS,
            actor_id=actor_id,
            tenant_id=tenant_id,
            metadata=metadata
        )

    @classmethod
    def log_denied(
        cls,
        action: str,
        resource: str,
        actor_id: Optional[str] = None,
        tenant_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Convenience wrapper for blocked authorization boundaries."""
        cls.log(
            action=action,
            resource=resource,
            status=AuditStatus.DENIED,
            actor_id=actor_id,
            tenant_id=tenant_id,
            metadata=metadata
        )

    @classmethod
    def log_failure(
        cls,
        action: str,
        resource: str,
        error_message: str,
        actor_id: Optional[str] = None,
        tenant_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Convenience wrapper highlighting execution errors on compliance paths."""
        meta = metadata or {}
        meta["error_message"] = error_message
        cls.log(
            action=action,
            resource=resource,
            status=AuditStatus.FAILED,
            actor_id=actor_id,
            tenant_id=tenant_id,
            metadata=meta
        )
