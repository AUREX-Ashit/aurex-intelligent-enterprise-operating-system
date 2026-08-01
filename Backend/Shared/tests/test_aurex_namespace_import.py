"""
TD-105 regression test — the `aurex.backend.shared.*` import-path defect.

Every module in Backend/Shared/{Config,Database,Events,Logging,Security}
already imports its siblings via the absolute path
`aurex.backend.shared.<component>.<module>`. No `aurex` package existed
anywhere in the repository, so every one of those imports failed with
ModuleNotFoundError (see Backend/Services/AuthService/observability.py's
own docstring, and TECH-DEBT.md TD-105).

Backend/aurex/backend/shared/<component>/__init__.py now makes that path
resolve, without moving, renaming, or duplicating a single line of
Backend/Shared's own content. This test proves the fix, run from the
Backend/ directory (or with Backend/ on sys.path — see conftest below).

Two of the five components (Database, Security) surface separate,
pre-existing content defects of their own once actually reachable for
the first time — a SyntaxError in Database/engine_factory.py and a
missing exception class reference in Security/jwt_manager.py. Neither is
part of the import-path defect this test guards; both are disclosed as
new Technical Debt (TD-106, TD-107) rather than fixed here, per Release
A1's own explicit "do not expand scope" instruction. This test asserts
full success only for the three components unaffected by those separate
defects, and asserts that the path-redirection mechanism itself (not
each component's own content) is sound for all five.
"""

import sys
from pathlib import Path

_BACKEND_ROOT = Path(__file__).resolve().parents[2]
if str(_BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(_BACKEND_ROOT))


def test_logging_namespace_imports_fully():
    import aurex.backend.shared.logging as logging_pkg

    assert logging_pkg.LoggerFactory is not None
    assert logging_pkg.AuditLogger is not None
    assert logging_pkg.CorrelationContext is not None
    assert logging_pkg.AuditStatus is not None


def test_events_namespace_imports_fully():
    import aurex.backend.shared.events as events_pkg

    assert events_pkg.EventPublisher is not None
    assert events_pkg.CloudEvent is not None
    assert events_pkg.EventRegistry is not None


def test_config_namespace_imports_fully():
    import aurex.backend.shared.config as config_pkg

    assert config_pkg.ConfigLoader is not None
    assert config_pkg.SettingsManager is not None


def test_database_namespace_reaches_real_content_not_module_not_found():
    """
    Proves the ORIGINAL defect (ModuleNotFoundError: no `aurex` package)
    is fixed, without asserting Database's own content is bug-free — it
    isn't (a pre-existing SyntaxError in engine_factory.py, disclosed as
    new Technical Debt, not fixed by this pass). The redirect succeeded
    if the failure we get is that downstream SyntaxError, propagated as
    an ImportError chain — not ModuleNotFoundError, which is what every
    caller got before this fix existed.
    """
    for name in list(sys.modules):
        if name.startswith("aurex.backend.shared.database"):
            del sys.modules[name]

    try:
        import aurex.backend.shared.database  # noqa: F401
    except SyntaxError:
        pass  # exec() of the real __init__.py raised directly — expected
    except ImportError as exc:
        assert "SyntaxError" in repr(exc.__cause__) or isinstance(exc.__cause__, SyntaxError)
    except ModuleNotFoundError:
        raise AssertionError(
            "aurex.backend.shared.database is still unreachable — the import-path fix regressed"
        )
    else:
        raise AssertionError(
            "Database's own pre-existing SyntaxError (engine_factory.py) appears to be fixed — "
            "update this test to a full positive assertion and close TD-106"
        )


def test_security_namespace_reaches_real_content_not_module_not_found():
    """
    Same rationale as the Database test above — Backend/Shared/Security's
    own jwt_manager.py references an exception class that does not exist
    in security's own exceptions.py (disclosed as new Technical Debt, not
    fixed by this pass). Proves the redirect works by asserting we reach
    that specific, different failure, not ModuleNotFoundError.
    """
    for name in list(sys.modules):
        if name.startswith("aurex.backend.shared.security"):
            del sys.modules[name]

    try:
        import aurex.backend.shared.security  # noqa: F401
    except ImportError as exc:
        assert "MissingRequiredValueError" in str(exc)
    except ModuleNotFoundError:
        raise AssertionError(
            "aurex.backend.shared.security is still unreachable — the import-path fix regressed"
        )
    else:
        raise AssertionError(
            "Security's own pre-existing ImportError (jwt_manager.py) appears to be fixed — "
            "update this test to a full positive assertion and close TD-107"
        )
