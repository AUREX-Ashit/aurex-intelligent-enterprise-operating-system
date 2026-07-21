"""
WP-00 Platform Bootstrap — automated pipeline entrypoint.

This is the "automated, idempotent pipeline stage" IMP-CICD-002 requires,
replacing the previously manual `docker exec ... psql -f scripts/07_....sql`
invocation documented in scripts/07_bootstrap_platform_admin.sql's own
"HOW TO RUN" section. Run this from CI/CD (see .github/workflows) or
locally for developer environment setup:

    cd Backend/Services/AuthService
    python -m scripts.run_bootstrap

Exit code 0 on success (including a no-op re-run); non-zero on failure.
Prerequisites unchanged from the original scripts: Alembic migration
applied (`alembic upgrade head`) before this runs — schema migration
remains its own pipeline stage (IMP-CICD-001), not this script's concern.
"""

from __future__ import annotations

import asyncio
import logging
import sys

from config import settings
from models.database import db_manager
from observability import CorrelationContext
from services.bootstrap_service import BootstrapService

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger("authservice.bootstrap.cli")


async def main() -> int:
    CorrelationContext.new()

    if not settings.bootstrap_enabled:
        logger.warning("bootstrap.enabled=false in configuration — skipping (this is not a failure).")
        return 0

    await db_manager.initialize()
    try:
        async for session in db_manager.get_session():
            service = BootstrapService(session)
            result = await service.run()
            logger.info(
                "Bootstrap complete: %s rows created this run (roles=%d permissions=%d "
                "role_permissions=%d organizations=%d persons=%d identities=%d memberships=%d)",
                result.total_created,
                result.roles_created,
                result.permissions_created,
                result.role_permissions_created,
                result.organizations_created,
                result.persons_created,
                result.identities_created,
                result.memberships_created,
            )
            break
        return 0
    except Exception:
        logger.exception("Bootstrap failed.")
        return 1
    finally:
        await db_manager.close()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
