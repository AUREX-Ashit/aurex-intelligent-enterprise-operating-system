"""
WP-00 Platform Bootstrap — Feature Flag Service.

Per the Aurex Platform Administrator Roadmap (Refinement 8's Enterprise
Readiness Checklist and every subsequent WP's Rollback Strategy), this is
the canonical mechanism every future work package gates its rollout behind.

Design: configuration-driven, not a new architectural concept. This reuses
config.py's existing YAML-with-environment-override pattern exactly
(Config/platform-config.yaml -> Settings._load_from_yaml /
Settings._load_from_env) rather than introducing a third-party feature-flag
service — consistent with this platform's own established discipline that
event types, confidence rules, and tool types are all configuration-driven
rows/values, never hardcoded (Master Technical Architecture, AMD-003/012).
A SaaS feature-flag platform is unnecessary for this program's MVP scale
(Aurex Platform Administrator Roadmap, Performance Framework) and is not
introduced here.
"""

from __future__ import annotations

from typing import Optional
from uuid import UUID

from config import settings
from observability import record_audit, AuditStatus


class FeatureFlagService:
    """
    Resolves whether a named feature flag is enabled, optionally scoped to
    an Organization. Flags are read from Settings.feature_flags (sourced
    from Config/platform-config.yaml's `feature_flags` section, with
    environment-variable overrides of the form FF_<FLAG_NAME>=true/false),
    never hardcoded in calling code.
    """

    def is_enabled(self, flag_name: str, organization_id: Optional[UUID] = None) -> bool:
        flags = settings.feature_flags
        if flag_name not in flags:
            # Fail closed: an undeclared flag is never silently treated as enabled.
            record_audit(
                action="FEATURE_FLAG_LOOKUP",
                resource=flag_name,
                status=AuditStatus.DENIED,
                metadata={"reason": "flag_not_declared", "organization_id": str(organization_id) if organization_id else None},
            )
            return False

        flag_config = flags[flag_name]
        enabled = bool(flag_config.get("enabled", False))

        # Optional per-organization allowlist, for staged/controlled rollout
        # (Aurex Roadmap Rollback Strategy: "disabling it reverts to a
        # maintenance page, never a partial/broken state" — an allowlist is
        # the same mechanism used in reverse, for gradual enablement).
        allowlist = flag_config.get("organizations")
        if enabled and allowlist and organization_id is not None:
            enabled = str(organization_id) in allowlist

        return enabled

    def all_flags(self) -> dict[str, bool]:
        """Returns the current resolved state of every declared flag — used by the readiness endpoint."""
        return {name: self.is_enabled(name) for name in settings.feature_flags}


feature_flags = FeatureFlagService()
