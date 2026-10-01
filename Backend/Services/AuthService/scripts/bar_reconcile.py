"""
Enterprise BAR — TD-171 (WP-23 Charter §21a), R-05/R-07: the mandatory
deployment reconciliation step (OD-5 deployment-level block).

Classifies the target environment's `bar_registration` rows against the
repository governance evidence (`services.bar_reconciliation`) and exits
non-zero on any non-valid OD-5 state, so the deployment does not proceed.

    cd Backend/Services/AuthService
    BAR_RECONCILIATION_DATABASE_URL=... python -m scripts.bar_reconcile [--repository-root PATH]

The database URL must be configured explicitly; when it is absent or
invalid the step fails closed as *reconciliation failure*. Only SELECT
statements are issued. That the connection is a read-only principal is an
external prerequisite (EP-03) and is NOT verified here; which environment
is canonical is OD-4 (external) and is NOT checked here.

Exit code 0: every row valid. 1: integrity failure (blocked). 2:
reconciliation failure (blocked; never read as clean).
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from pathlib import Path

from sqlalchemy.engine import make_url
from sqlalchemy.exc import ArgumentError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from services.bar_governance_evidence import DEFAULT_REPOSITORY_ROOT
from services.bar_reconciliation import ReconciliationReport, failure_report, reconcile_environment

RECONCILIATION_URL_ENV = "BAR_RECONCILIATION_DATABASE_URL"


async def run(database_url: str | None, repository_root: Path) -> ReconciliationReport:
    if not database_url or not database_url.strip():
        return failure_report(f"{RECONCILIATION_URL_ENV} is not set.")
    try:
        make_url(database_url.strip())
    except ArgumentError:
        return failure_report(f"{RECONCILIATION_URL_ENV} is not a valid database URL.")
    engine = create_async_engine(database_url.strip())
    try:
        async with async_sessionmaker(engine, class_=AsyncSession)() as session:
            return await reconcile_environment(session, repository_root)
    finally:
        await engine.dispose()


def main(argv: list[str] | None = None, environ: dict[str, str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="BAR environment reconciliation (read-only, OD-5 block).")
    parser.add_argument("--repository-root", type=Path, default=DEFAULT_REPOSITORY_ROOT)
    args = parser.parse_args(argv)
    environ = os.environ if environ is None else environ
    report = asyncio.run(run(environ.get(RECONCILIATION_URL_ENV), args.repository_root))
    print(report.render())
    return report.exit_code


if __name__ == "__main__":
    sys.exit(main())
