"""
Aurex Shared package namespace root.

This package intentionally has no content of its own. Its five
sub-packages (config, database, events, logging, security) each
redirect their own __path__ to the corresponding, already-written
Backend/Shared/<Component> directory — see each sub-package's own
__init__.py docstring for why, and TD-105 in TECH-DEBT.md for the
disclosed scope of this fix.
"""
