"""
Business Activity Engine -- collaborator boundaries (WP-BAE-001 M1).

Every collaborator the engine consults is injected through one of the
interfaces below. There is no discovery, scanning, decorator
registration, or hidden global lookup anywhere in this package
(ADR-042 / `RO-M1-03`; `RTA-001 §6.6`).

  * `RegistrationSource` -- BAR, read-only. The BAE consumes/enforces
    the registration prerequisite; BAR (and WP-23 Workstream E's gate
    authority) owns registration state (`RO-M1-04`). The concrete
    BAR-backed implementation and its interface boundary are M2.
  * `ManifestResolver` -- runtime Manifest Resolution, owned by the BAE
    (ADR-042 / `RO-M1-03`). M1 defines the outcome only, never a
    manifest schema; the minimum manifest contract is M2. The only
    implementation shipped is `UnimplementedManifestResolver`.
  * `Authorizer` -- the existing Authorization Runtime Engine contract,
    structurally satisfied, unmodified, by
    `adapters.authorization_adapter.AuthorizationAdapter` (WP-RTA-001
    M4). The Authorization Engine remains the sole decision authority
    (`RTA-001 §11.2`).
  * `TransactionBoundary` -- the transaction-ownership contract
    (`IMP-001 §6.19.3`): only the BAE commits or rolls back, on the
    hosting service's own session (ADR-042 / `RO-M1-01`). Business
    logic never receives it. The M1 engine opens no transaction; the
    Persistence Coordination and Transaction Commit stages are M5.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol

from adapters.authorization_adapter import AuthorizationRequest
from authorization.models import EvaluationResult

from .identity import BusinessActivityIdentifier


class RegistrationSource(Protocol):
    """Read-only view of BAR's authoritative registration state. Must return a real bool; anything else fails closed."""

    async def is_registered(self, identifier: BusinessActivityIdentifier) -> bool: ...


class ManifestResolutionStatus(str, Enum):
    RESOLVED = "RESOLVED"
    NOT_IMPLEMENTED = "NOT_IMPLEMENTED"


@dataclass(frozen=True)
class ManifestResolution:
    """The outcome of resolving an identifier to its manifest. Carries no manifest content until M2 defines it."""

    status: ManifestResolutionStatus
    reason: str


class ManifestResolver(Protocol):
    async def resolve(self, identifier: BusinessActivityIdentifier) -> ManifestResolution: ...


class UnimplementedManifestResolver:
    """The M1 Manifest Resolution boundary: always NOT_IMPLEMENTED, never a fabricated resolution."""

    async def resolve(self, identifier: BusinessActivityIdentifier) -> ManifestResolution:
        return ManifestResolution(
            status=ManifestResolutionStatus.NOT_IMPLEMENTED,
            reason=(
                f"Manifest Resolution for {identifier} is not implemented: the minimum manifest "
                "contract is WP-BAE-001 M2 (ADR-042, RO-M1-03)."
            ),
        )


class Authorizer(Protocol):
    async def evaluate(self, request: AuthorizationRequest) -> EvaluationResult: ...


class TransactionBoundary(Protocol):
    """The hosting service's unit of work. Opened, committed, and rolled back only by the BAE."""

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...
