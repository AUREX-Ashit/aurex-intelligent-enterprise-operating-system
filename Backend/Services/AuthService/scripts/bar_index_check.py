"""
Enterprise BAR — TD-171 (WP-23 Charter §21a), R-04: CI repository check.

Checks `BAR-INDEX.md` §3 against the governed acts in both directions
(`services.bar_governance_evidence`). Repository-only: no database
connection, and no act or index is created or modified.

    cd Backend/Services/AuthService
    python -m scripts.bar_index_check [--repository-root PATH]

Exit code 0 when no blocking finding exists, 1 on a blocking finding, 2
when the evidence cannot be read.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from services.bar_governance_evidence import DEFAULT_REPOSITORY_ROOT, BarIndexUnreadable, check_repository

EXIT_CLEAN = 0
EXIT_BLOCKING = 1
EXIT_UNREADABLE = 2


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="BAR-INDEX.md <-> governed act consistency check (read-only).")
    parser.add_argument("--repository-root", type=Path, default=DEFAULT_REPOSITORY_ROOT)
    args = parser.parse_args(argv)
    try:
        findings = check_repository(args.repository_root)
    except (BarIndexUnreadable, OSError, UnicodeDecodeError) as exc:
        print(f"BAR index check: evidence unreadable: {exc}")
        return EXIT_UNREADABLE
    for finding in findings:
        marker = "BLOCKING" if finding.blocking else "notice"
        print(f"[{marker}] {finding.code.value} {finding.subject}: {finding.detail}")
    blocking = [f for f in findings if f.blocking]
    print(f"BAR index check: {len(blocking)} blocking finding(s), {len(findings) - len(blocking)} notice(s).")
    return EXIT_BLOCKING if blocking else EXIT_CLEAN


if __name__ == "__main__":
    sys.exit(main())
