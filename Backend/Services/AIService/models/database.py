# models/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, declared_attr
from config.settings import settings

# Custom declarative base with multi-tenant awareness defaults
class CustomBase:
    @declared_attr
    def __tablename__(cls) -> str:
        # Convert CamelCase class name into snake_case table name
        import re
        name = cls.__name__
        if name.endswith("Model"):
            name = name[:-5]
        return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower() + "s"

Base = declarative_base(cls=CustomBase)

# Configure asynchronous connection pool
engine = create_async_engine(
    settings.database_url,
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
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

async def get_db():
    """FastAPI Dependency injection generator yielding isolated transactions."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_db():
    """Initializes schema setup for dev environments."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
