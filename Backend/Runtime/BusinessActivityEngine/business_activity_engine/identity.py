"""
Business Activity Engine -- Business Activity identity (WP-BAE-001 M1).

Represents a BAR-issued Business Activity Identifier. BAR is the
canonical identifier authority (D5, `ROD-ENTERPRISE-BAR-Decision-
Preparation.md §0d`); the format is BAR's own `BA-NNNNNN` (six-digit,
zero-padded -- `BAR-INDEX.md §2`, `SD-002-004` via `IMP-001 §6.22.1b`).

This module validates shape only. It never issues, allocates, reserves,
or reformats an identifier, and it cannot tell whether an identifier is
registered -- only BAR can (see `ports.RegistrationSource`).
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_IDENTIFIER_PATTERN = re.compile(r"BA-\d{6}")


class InvalidBusinessActivityIdentifierError(ValueError):
    """Raised when a value does not have BAR's `BA-NNNNNN` shape."""


@dataclass(frozen=True)
class BusinessActivityIdentifier:
    """An immutable, shape-validated BAR-issued `BA-NNNNNN` identifier."""

    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str) or not _IDENTIFIER_PATTERN.fullmatch(self.value):
            raise InvalidBusinessActivityIdentifierError(
                f"{self.value!r} is not a BAR-issued Business Activity Identifier (expected 'BA-NNNNNN')."
            )

    def __str__(self) -> str:
        return self.value
