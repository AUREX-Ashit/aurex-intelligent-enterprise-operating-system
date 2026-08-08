"""
Runtime Integration Adapters (WP-RTA-001 M4).

The stable interface a future Business Activity (primarily WP-05)
depends on, so it never couples directly to `authorization/*`'s own
internals. Dependency direction is one-way: this package imports from
`authorization`; nothing in `authorization` imports from this package
(enforced by `tests/test_adapter.py`'s own dependency-direction test,
and structurally by living in a separate top-level package within this
Work Package).

No Business Activity is integrated by this milestone -- see
IMP-REPORT-WP-RTA-001 M4. This package exposes the seam only.
"""

from .authorization_adapter import (
    AuthorizationAdapter,
    AuthorizationRequest,
    InvalidAuthorizationRequestError,
)

__all__ = [
    "AuthorizationAdapter",
    "AuthorizationRequest",
    "InvalidAuthorizationRequestError",
]
