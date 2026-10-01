"""
Enterprise BAR — TD-171 remediation tranche (WP-23 Charter §21a), R-01/R-02:
the governed BAR registration operation.

This module is the only production module permitted to invoke
`BarRegistrationService.register()` (static guard:
`tests/test_bar_write_path_guard.py`). It is the governance/control
boundary around the existing, unchanged Workstream C registration
service, which remains the business operation and the authoritative
persistence path (transaction, savepoint/collision handling, integrity
classification, audit/event emission, uniqueness constraints).

Two phases, following the approved two-part governed act (OD-1; D5:
the identifier is assigned at BAR registration, never earlier):

  1. `execute(act_path, request)`: the act must carry the authorization
     component only. The request is matched against it, the existing
     `register()` issues the identifier, and the operation returns the
     execution-addendum text recording the identifier actually issued.
     The row is NOT yet governed: OD-5 blocking applies until the
     addendum is committed to the governing act.
  2. `confirm(act_path)`: the act must be complete (authorization +
     execution addendum; an authorization-only act fails closed). The
     addendum is verified against the persisted row. Only then is the
     registration confirmed as governed.

Deployment-time write contract (repository side only): the operation
connects through an explicitly configured deployment write capability
(`BAR_GOVERNED_WRITE_DATABASE_URL`), separate from the runtime
`DATABASE_URL`, and fails closed when it is absent or invalid. This does
NOT establish or verify database-role separation: provisioning the
write-capable principal and proving the runtime role cannot write BAR
are external prerequisites (EP-02, EP-04). No role name is assumed.

Validation of the act itself is delegated entirely to
`services.bar_governed_act` (slice 1); nothing here re-parses it.
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date, timezone
from enum import Enum
from pathlib import Path

from sqlalchemy.engine import make_url
from sqlalchemy.exc import ArgumentError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from models.bar_registration import BarRegistration
from observability import AuditStatus, CorrelationContext, record_audit
from repositories.bar_identifier_repository import BarIdentifierRepository
from repositories.bar_registration_repository import BarRegistrationRepository
from services.bar_governed_act import (
    EXECUTION_ACT_TYPE,
    EXECUTION_TITLE,
    REGISTRATION_INTENT,
    GovernedAct,
    GovernedActAuthorization,
    load_governed_act,
)
from services.bar_registration_service import BarRegistrationService

DEPLOYMENT_WRITE_URL_ENV = "BAR_GOVERNED_WRITE_DATABASE_URL"
_ACTION = "BAR_GOVERNED_REGISTRATION"


# ------------------------------------------------------------------ errors


class GovernedRegistrationErrorCode(str, Enum):
    WRITE_CAPABILITY_UNAVAILABLE = "WRITE_CAPABILITY_UNAVAILABLE"
    WRITE_CAPABILITY_INVALID = "WRITE_CAPABILITY_INVALID"
    ALREADY_EXECUTED = "ALREADY_EXECUTED"
    REQUEST_MISMATCH = "REQUEST_MISMATCH"
    REGISTRATION_MISSING = "REGISTRATION_MISSING"
    EVIDENCE_MISMATCH = "EVIDENCE_MISMATCH"


class GovernedRegistrationError(RuntimeError):
    """Base class for every refusal of the governed registration operation."""

    def __init__(self, code: GovernedRegistrationErrorCode, message: str, *, field: str | None = None) -> None:
        super().__init__(f"{code.value}: {message}")
        self.code = code
        self.field = field


class DeploymentWriteCapabilityUnavailable(GovernedRegistrationError):
    """No deployment write capability is configured; the operation cannot write."""


class DeploymentWriteCapabilityInvalid(GovernedRegistrationError):
    """The configured deployment write capability is unusable or not separate from the runtime."""


class GovernedActAlreadyExecuted(GovernedRegistrationError):
    """The act already carries an execution addendum; executing it again is refused."""


class GovernedRegistrationRequestMismatch(GovernedRegistrationError):
    """The registration request does not match the act's authorization component."""


class GovernedRegistrationMissing(GovernedRegistrationError):
    """The identifier recorded in the execution addendum has no persisted registration."""


class GovernedRegistrationEvidenceMismatch(GovernedRegistrationError):
    """The persisted registration disagrees with the complete governed act."""


# ------------------------------------------------- deployment write contract


@dataclass(frozen=True)
class DeploymentWriteCapability:
    """
    The explicitly configured deployment-time write connection. Holding one
    is the only way to construct the governed operation. It is validated as
    present, parseable and distinct from the runtime connection; it is not
    proof that the database enforces role separation (EP-02).
    """

    database_url: str

    @classmethod
    def from_environment(
        cls,
        environ: Mapping[str, str] | None = None,
        *,
        runtime_database_url: str | None = None,
    ) -> "DeploymentWriteCapability":
        environ = os.environ if environ is None else environ
        if runtime_database_url is None:
            from config import settings

            runtime_database_url = settings.database_url
        return cls.validate(environ.get(DEPLOYMENT_WRITE_URL_ENV, ""), runtime_database_url=runtime_database_url)

    @classmethod
    def validate(cls, database_url: str | None, *, runtime_database_url: str | None) -> "DeploymentWriteCapability":
        if not database_url or not database_url.strip():
            raise DeploymentWriteCapabilityUnavailable(
                GovernedRegistrationErrorCode.WRITE_CAPABILITY_UNAVAILABLE,
                f"no deployment write capability configured ({DEPLOYMENT_WRITE_URL_ENV} is not set).",
            )
        try:
            url = make_url(database_url.strip())
        except ArgumentError as exc:
            raise DeploymentWriteCapabilityInvalid(
                GovernedRegistrationErrorCode.WRITE_CAPABILITY_INVALID,
                f"{DEPLOYMENT_WRITE_URL_ENV} is not a valid database URL.",
            ) from exc
        if runtime_database_url:
            try:
                runtime_url = make_url(runtime_database_url)
            except ArgumentError:
                runtime_url = None
            if runtime_url is not None and url == runtime_url:
                raise DeploymentWriteCapabilityInvalid(
                    GovernedRegistrationErrorCode.WRITE_CAPABILITY_INVALID,
                    f"{DEPLOYMENT_WRITE_URL_ENV} must be a separate deployment connection, "
                    "not the runtime DATABASE_URL.",
                )
        return cls(database_url=database_url.strip())


# ------------------------------------------------------------ request/result


@dataclass(frozen=True)
class GovernedRegistrationRequest:
    business_activity_reference: str
    owning_capability: str
    owning_work_package: str
    is_retroactive: bool
    registration_intent: str = REGISTRATION_INTENT


@dataclass(frozen=True)
class GovernedRegistrationExecution:
    """Outcome of `execute()`: registered, but not governed until the addendum is committed."""

    governing_act_id: str
    bar_business_activity_identifier: str
    execution_reference: str
    executed_on: date
    execution_addendum: str


@dataclass(frozen=True)
class GovernedRegistrationConfirmation:
    """Outcome of `confirm()`: the registration is linked to complete governed evidence."""

    governing_act_id: str
    bar_business_activity_identifier: str
    execution_reference: str


def render_execution_addendum(
    authorization: GovernedActAuthorization,
    *,
    bar_business_activity_identifier: str,
    execution_reference: str,
    executed_on: date,
) -> str:
    """The §17.1.3 execution addendum for an issued identifier (parsed by slice 1)."""
    rows = [
        ("act_type", EXECUTION_ACT_TYPE),
        ("addendum_of", authorization.governing_act_id),
        ("bar_business_activity_identifier", bar_business_activity_identifier),
        ("business_activity_reference", authorization.business_activity_reference),
        ("owning_capability", authorization.owning_capability),
        ("owning_work_package", authorization.owning_work_package),
        ("registration_intent", authorization.registration_intent),
        ("execution_reference", execution_reference),
        ("executed_on", executed_on.isoformat()),
    ]
    for field, value in rows:
        if "|" in value or "\n" in value:
            raise ValueError(f"execution addendum value for '{field}' cannot be rendered in a table: {value!r}")
    body = "\n".join(f"| `{field}` | {value} |" for field, value in rows)
    return (
        f"## Execution Addendum ({executed_on.isoformat()})\n\n"
        f"**{EXECUTION_TITLE}**\n\n"
        "| Field | Value |\n|---|---|\n"
        f"{body}\n"
    )


# --------------------------------------------------------------- operation


class GovernedBarRegistrationOperation:
    """The deployment-time governed BAR registration operation (TD-171)."""

    def __init__(self, capability: DeploymentWriteCapability) -> None:
        if not isinstance(capability, DeploymentWriteCapability):
            raise DeploymentWriteCapabilityUnavailable(
                GovernedRegistrationErrorCode.WRITE_CAPABILITY_UNAVAILABLE,
                "a validated DeploymentWriteCapability is required.",
            )
        self.capability = capability

    async def execute(
        self, act_path: Path | str, request: GovernedRegistrationRequest, *, actor_id: str | None = None
    ) -> GovernedRegistrationExecution:
        act = load_governed_act(act_path)
        authorization = act.authorization
        if act.execution is not None:
            self._deny(authorization.governing_act_id, GovernedRegistrationErrorCode.ALREADY_EXECUTED, actor_id)
            raise GovernedActAlreadyExecuted(
                GovernedRegistrationErrorCode.ALREADY_EXECUTED,
                f"'{act.source_name}' already has an execution addendum; it cannot be executed again.",
            )
        self._match_request(authorization, request, actor_id)

        execution_reference = CorrelationContext.new()
        async with self._session() as session:
            service = BarRegistrationService(BarRegistrationRepository(session), BarIdentifierRepository(session))
            try:
                registration = await service.register(
                    business_activity_reference=authorization.business_activity_reference,
                    owning_capability=authorization.owning_capability,
                    owning_work_package=authorization.owning_work_package,
                    registering_act=authorization.governing_act_id,
                    is_retroactive=authorization.retroactive,
                    actor_id=actor_id,
                )
                await session.commit()
            except BaseException:
                await session.rollback()
                raise

        executed_on = registration.registered_at.astimezone(timezone.utc).date()
        return GovernedRegistrationExecution(
            governing_act_id=authorization.governing_act_id,
            bar_business_activity_identifier=registration.identifier,
            execution_reference=execution_reference,
            executed_on=executed_on,
            execution_addendum=render_execution_addendum(
                authorization,
                bar_business_activity_identifier=registration.identifier,
                execution_reference=execution_reference,
                executed_on=executed_on,
            ),
        )

    async def confirm(self, act_path: Path | str, *, actor_id: str | None = None) -> GovernedRegistrationConfirmation:
        act = load_governed_act(act_path)
        execution = act.require_complete()
        async with self._session() as session:
            registration = await BarRegistrationRepository(session).get_by_identifier(
                execution.bar_business_activity_identifier
            )
        if registration is None:
            self._deny(act.authorization.governing_act_id, GovernedRegistrationErrorCode.REGISTRATION_MISSING, actor_id)
            raise GovernedRegistrationMissing(
                GovernedRegistrationErrorCode.REGISTRATION_MISSING,
                f"identifier '{execution.bar_business_activity_identifier}' recorded in "
                f"'{act.source_name}' has no persisted registration.",
                field="bar_business_activity_identifier",
            )
        self._match_registration(act, registration, actor_id)
        record_audit(
            action=_ACTION,
            resource=f"bar_registration:{registration.id}",
            status=AuditStatus.SUCCESS,
            actor_id=actor_id or "SYSTEM",
            metadata={
                "phase": "confirm",
                "governing_act_id": act.authorization.governing_act_id,
                "identifier": registration.identifier,
                "execution_reference": execution.execution_reference,
            },
        )
        return GovernedRegistrationConfirmation(
            governing_act_id=act.authorization.governing_act_id,
            bar_business_activity_identifier=registration.identifier,
            execution_reference=execution.execution_reference,
        )

    # -------------------------------------------------------------- internals

    def _session(self) -> "_OwnedSession":
        return _OwnedSession(self.capability.database_url)

    def _match_request(
        self, authorization: GovernedActAuthorization, request: GovernedRegistrationRequest, actor_id: str | None
    ) -> None:
        expected = {
            "business_activity_reference": authorization.business_activity_reference,
            "owning_capability": authorization.owning_capability,
            "owning_work_package": authorization.owning_work_package,
            "is_retroactive": authorization.retroactive,
            "registration_intent": authorization.registration_intent,
        }
        for field, value in expected.items():
            if getattr(request, field) != value:
                self._deny(authorization.governing_act_id, GovernedRegistrationErrorCode.REQUEST_MISMATCH, actor_id, field)
                raise GovernedRegistrationRequestMismatch(
                    GovernedRegistrationErrorCode.REQUEST_MISMATCH,
                    f"request '{field}' {getattr(request, field)!r} does not match the act's {value!r}.",
                    field=field,
                )

    def _match_registration(self, act: GovernedAct, registration: BarRegistration, actor_id: str | None) -> None:
        authorization, execution = act.authorization, act.require_complete()
        expected = {
            "identifier": execution.bar_business_activity_identifier,
            "registering_act": authorization.governing_act_id,
            "business_activity_reference": authorization.business_activity_reference,
            "owning_capability": authorization.owning_capability,
            "owning_work_package": authorization.owning_work_package,
            "is_retroactive": authorization.retroactive,
        }
        for field, value in expected.items():
            if getattr(registration, field) != value:
                self._deny(authorization.governing_act_id, GovernedRegistrationErrorCode.EVIDENCE_MISMATCH, actor_id, field)
                raise GovernedRegistrationEvidenceMismatch(
                    GovernedRegistrationErrorCode.EVIDENCE_MISMATCH,
                    f"persisted registration '{field}' {getattr(registration, field)!r} does not "
                    f"match the governed act's {value!r}.",
                    field=field,
                )

    @staticmethod
    def _deny(
        governing_act_id: str, code: GovernedRegistrationErrorCode, actor_id: str | None, field: str | None = None
    ) -> None:
        record_audit(
            action=_ACTION,
            resource="bar_registration:governed",
            status=AuditStatus.DENIED,
            actor_id=actor_id or "SYSTEM",
            metadata={"governing_act_id": governing_act_id, "code": code.value, "field": field},
        )


class _OwnedSession:
    """A session on the deployment write connection; the engine lives only for one phase."""

    def __init__(self, database_url: str) -> None:
        self._engine = create_async_engine(database_url)
        self._session: AsyncSession | None = None

    async def __aenter__(self) -> AsyncSession:
        self._session = async_sessionmaker(self._engine, class_=AsyncSession, expire_on_commit=False)()
        return self._session

    async def __aexit__(self, *_exc: object) -> None:
        try:
            if self._session is not None:
                await self._session.close()
        finally:
            await self._engine.dispose()
