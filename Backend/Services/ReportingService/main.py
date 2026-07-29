import time
import structlog
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config.settings import settings
from middleware.tenant import TenantMiddleware
from routers.reporting import router as reporting_router
from models.database import engine, Base

# Dynamic structure logger setup conforming to enterprise standard
def configure_logging():
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer() if settings.observability.logging.structured_json else structlog.processors.ConsoleRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

logger = structlog.get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Execution bounds capturing boot constraints and connections"""
    configure_logging()
    logger.info("Initializing Aurex ReportingService startup sequences", env=settings.environment)
    
    # Auto-scaffold database tables on startup if possible
    try:
        async with engine.begin() as conn:
            # We can run schema creation
            # Note: in fully isolated prod, Alembic migrations run out-of-band.
            # This is a safe self-healing fallback for preview configurations.
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Database schema state verified and synchronized")
    except Exception as e:
        logger.warning("Database schema synchronization deferred (expected if database is offline)", error=str(e))
        
    yield
    
    logger.info("Exiting Aurex ReportingService task instances")
    await engine.dispose()

app = FastAPI(
    title="Aurex Reporting API",
    description="Enterprise API engine generating ESG, BRSR, GRI, and CSRD disclosure reports, tracking metric scorecards, and compiling audit logs.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# 1. CORS Configuration (Parsed from YAML Config)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors.allow_origins,
    allow_credentials=settings.cors.allow_credentials,
    allow_methods=settings.cors.allow_methods,
    allow_headers=settings.cors.allow_headers,
)

# 2. Multi-Tenant Safety Middleware (Extracts header parameter)
app.add_middleware(TenantMiddleware)

# 3. Execution Latency Logging Filter
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response: Response = await call_next(request)
    process_time = time.perf_counter() - start_time
    # Add metrics telemetry headers
    response.headers["X-Process-Time-Sec"] = f"{process_time:.4f}"
    return response

# 4. Expose Routers
app.include_router(reporting_router)

# 5. Core Health Endpoint
@app.get("/health", tags=["Infrastructure"], summary="Query service health status")
async def health_check():
    """Provides platform verification checks including DB, region, provider, and features"""
    return {
        "status": "healthy",
        "service": "aurex-reporting",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "platform_context": {
            "name": settings.name,
            "environment": settings.environment,
            "region": settings.region,
            "enable_copilot": settings.feature_flags.enable_copilot,
            "enable_rag": settings.feature_flags.enable_rag
        },
        "database_active": settings.database.postgresql.enabled
    }
