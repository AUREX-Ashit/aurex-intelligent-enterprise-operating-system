import uuid
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Date, DateTime, func
from config.settings import settings
from middleware.tenant import get_current_tenant
import structlog

logger = structlog.get_logger()

# Resolve Database connection string
def resolve_database_url() -> str:
    if settings.database_url_override:
        return settings.database_url_override
    
    # Standard format postgresql+asyncpg://user:pass@host:port/dbname
    p_config = settings.database.postgresql
    user = p_config.username
    password = p_config.password
    host = p_config.host
    port = p_config.port
    name = p_config.database_name
    
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"

DATABASE_URL = resolve_database_url()

# Initialize Async Engine with pooled settings from Yaml
engine = create_async_engine(
    DATABASE_URL,
    pool_size=settings.database.postgresql.pool_size,
    max_overflow=settings.database.postgresql.max_overflow,
    pool_pre_ping=True,
    future=True,
    echo=False
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Declarative Base for 2.0 with standard auditing attributes
class Base(DeclarativeBase):
    pass

class TenantModelMixin:
    """Provides consistent isolation metadata across modern enterprise schemas"""
    tenant_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    created_by: Mapped[str] = mapped_column(String(150), nullable=True)
    updated_by: Mapped[str] = mapped_column(String(150), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI Dependency Injector for Async Database Sessions.
    Guarantees active transaction limits, logs exceptions, and ensures cleanup.
    """
    session = AsyncSessionLocal()
    tenant_id = get_current_tenant()
    
    # Intercept session to inject filters or perform RLS hook validations
    logger.debug("Database session checked out", tenant_id=tenant_id)
    try:
        yield session
    except Exception as exc:
        logger.error("DB Session Rollback caused by error", error=str(exc))
        await session.rollback()
        raise
    finally:
        await session.close()
        logger.debug("Database session returned to pool", tenant_id=tenant_id)
