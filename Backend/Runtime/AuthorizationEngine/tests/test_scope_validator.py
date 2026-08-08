"""
Unit tests for WP-RTA-001 Milestone M5 -- Enterprise Scope Validation.

Covers: valid scope, invalid scope, missing scope. No database, no
authorization decision is ever produced by this module.
"""

from __future__ import annotations

import pytest

from authorization import AuthorizationContext, EnterpriseScopeValidationError, EnterpriseScopeValidator


def _context(**overrides) -> AuthorizationContext:
    defaults = dict(identity_id="person-1", organization_id="org-1")
    defaults.update(overrides)
    return AuthorizationContext(**defaults)


def test_valid_scope_passes() -> None:
    validator = EnterpriseScopeValidator()

    validator.validate(_context(organization_id="org-1", enterprise_scope="node-42"))  # must not raise


def test_valid_scope_with_no_enterprise_scope_passes() -> None:
    """enterprise_scope is Optional -- absence alone is not malformed."""
    validator = EnterpriseScopeValidator()

    validator.validate(_context(organization_id="org-1", enterprise_scope=None))  # must not raise


def test_missing_organization_id_is_rejected() -> None:
    validator = EnterpriseScopeValidator()

    with pytest.raises(EnterpriseScopeValidationError):
        validator.validate(_context(organization_id=""))


def test_blank_organization_id_is_rejected() -> None:
    validator = EnterpriseScopeValidator()

    with pytest.raises(EnterpriseScopeValidationError):
        validator.validate(_context(organization_id="   "))


def test_blank_enterprise_scope_is_rejected_as_inconsistent() -> None:
    """Present-but-empty is malformed, distinct from simply absent (None)."""
    validator = EnterpriseScopeValidator()

    with pytest.raises(EnterpriseScopeValidationError):
        validator.validate(_context(organization_id="org-1", enterprise_scope="   "))


def test_validator_never_returns_a_value_resembling_a_decision() -> None:
    """Validation must not perform authorization decisions -- confirmed by its own return contract."""
    validator = EnterpriseScopeValidator()

    result = validator.validate(_context())

    assert result is None
