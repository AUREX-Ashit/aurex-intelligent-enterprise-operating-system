from uuid import uuid4

from config import settings
from services.feature_flag_service import FeatureFlagService


def test_undeclared_flag_fails_closed() -> None:
    """Security default: an unknown flag name is never treated as enabled."""
    service = FeatureFlagService()
    assert service.is_enabled("ff_does_not_exist") is False


def test_declared_enabled_flag_returns_true(monkeypatch) -> None:
    monkeypatch.setitem(settings.feature_flags, "ff_test_flag", {"enabled": True, "organizations": None})
    service = FeatureFlagService()
    assert service.is_enabled("ff_test_flag") is True


def test_declared_disabled_flag_returns_false(monkeypatch) -> None:
    monkeypatch.setitem(settings.feature_flags, "ff_test_flag", {"enabled": False, "organizations": None})
    service = FeatureFlagService()
    assert service.is_enabled("ff_test_flag") is False


def test_organization_allowlist_scopes_rollout(monkeypatch) -> None:
    """
    Rollback Strategy support: an enabled flag scoped to specific
    organizations is false for any organization not on the allowlist —
    proves the staged-rollout mechanism actually restricts, not just that
    the flag is nominally 'enabled'.
    """
    allowed_org = uuid4()
    other_org = uuid4()
    monkeypatch.setitem(
        settings.feature_flags,
        "ff_test_flag",
        {"enabled": True, "organizations": [str(allowed_org)]},
    )
    service = FeatureFlagService()
    assert service.is_enabled("ff_test_flag", organization_id=allowed_org) is True
    assert service.is_enabled("ff_test_flag", organization_id=other_org) is False


def test_all_flags_reflects_configured_state(monkeypatch) -> None:
    monkeypatch.setitem(settings.feature_flags, "ff_a", {"enabled": True, "organizations": None})
    monkeypatch.setitem(settings.feature_flags, "ff_b", {"enabled": False, "organizations": None})
    service = FeatureFlagService()
    resolved = service.all_flags()
    assert resolved["ff_a"] is True
    assert resolved["ff_b"] is False
