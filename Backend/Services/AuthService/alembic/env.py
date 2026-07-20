import asyncio
import sys
from logging.config import fileConfig
from pathlib import Path

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context

# ---------------------------------------------------------------------------
# Ensure the AuthService root is on sys.path so application modules resolve.
# This file lives at <root>/alembic/env.py — one level up is the root.
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# ---------------------------------------------------------------------------
# Import every R-001 model so that Base.metadata is fully populated before
# Alembic compares against the database. The models/__init__.py side-effect
# import registers Organization, Person, Identity, Role, Permission,
# RolePermission, Membership, and RefreshToken with Base.
# ---------------------------------------------------------------------------
import models  # noqa: F401 — populates Base.metadata as a side effect
from models.database import Base
from config import settings

# ---------------------------------------------------------------------------
# Alembic config object (wraps alembic.ini)
# ---------------------------------------------------------------------------
alembic_cfg = context.config

if alembic_cfg.config_file_name is not None:
    fileConfig(alembic_cfg.config_file_name)

# All 8 R-001 tables are captured here. Legacy TenantModel / UserModel are
# intentionally NOT imported and therefore NOT in target_metadata.
target_metadata = Base.metadata

# Override the database URL from application config.
# This guarantees migrations always target the same database as the application.
# Requires DATABASE_URL env var or a valid Config/platform-config.yaml.
if not settings.database_url:
    raise RuntimeError(
        "Database URL is not configured. "
        "Set DATABASE_URL environment variable or configure "
        "database.url in Config/platform-config.yaml."
    )
alembic_cfg.set_main_option("sqlalchemy.url", settings.database_url)


# ---------------------------------------------------------------------------
# Offline mode — generates a .sql script without connecting to the database.
# Usage: alembic upgrade head --sql > migration.sql
# The asyncpg driver is not used here; Alembic parses the dialect only.
# ---------------------------------------------------------------------------
def run_migrations_offline() -> None:
    url = alembic_cfg.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
        include_schemas=True,
    )
    with context.begin_transaction():
        context.run_migrations()


# ---------------------------------------------------------------------------
# Online mode — connects to the database and runs migrations.
# Uses the async engine directly since the application uses asyncpg throughout.
# ---------------------------------------------------------------------------
def _run_migrations_sync(connection) -> None:
    """Synchronous callback passed to connection.run_sync()."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
        include_schemas=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    engine = create_async_engine(
        settings.database_url,
        poolclass=pool.NullPool,
        echo=False,
    )
    async with engine.connect() as connection:
        await connection.run_sync(_run_migrations_sync)
    await engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
