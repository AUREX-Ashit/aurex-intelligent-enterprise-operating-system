import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config.settings import settings
from routers.ingestion import ingestion_router
from routers.health import health_router
from middleware.logging import CustomLoggingMiddleware
from middleware.tenant import TenantIsolationMiddleware
from models.database import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles microservice startup and teardown routines safely, 
    pre-initializing database schemas in development environments if allowed.
    """
    print(f"[*] Booting {settings.app_name} on {settings.environment} model pool...")
    print(f"[*] Host Isolation Header configured to: '{settings.auth.header_name}'")
    
    # In dry-runs / local development we can pre-create tables to make testing immediate.
    if settings.environment == "development":
        try:
            async with engine.begin() as conn:
                # Creates all tables asynchronously
                await conn.run_sync(Base.metadata.create_all)
            print("[*] SQLAlchemy 2.x tables pre-init generated successfully.")
        except Exception as e:
            print(f"[!] Warning: Could not pre-create database tables on startup link: {e}")
            print("[!] Ensure Postgres database is active or connection string leads correctly.")
            
    yield
    
    # Dispose pools on exit
    await engine.dispose()
    print("[*] Engine connection pool disposed.")


# Instantiate primary FastAPI Core 
app = FastAPI(
    title=settings.app_name,
    description="Aurex Enterprise ESG & Auditing Ingestion Pipeline Microservice.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# 1. Mount Observability and Network Middleware
# Order matters: Logging is the outer boundary, capturing performance of all inner layers
app.add_middleware(CustomLoggingMiddleware)

# Tenant headers isolation security layer
app.add_middleware(TenantIsolationMiddleware)

# Configure Cross-Origin Resource Sharing (CORS) from configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors.allow_origins if hasattr(settings, "cors") else ["*"],
    allow_credentials=settings.cors.allow_credentials if hasattr(settings, "cors") else True,
    allow_methods=settings.cors.allow_methods if hasattr(settings, "cors") else ["*"],
    allow_headers=settings.cors.allow_headers if hasattr(settings, "cors") else ["*"],
)

# 2. Append Modules Routers 
app.include_router(health_router)
app.include_router(ingestion_router)

# Root Index redirection / welcoming payload
@app.get("/", tags=["Operations"], include_in_schema=False)
async def service_index():
    return {
        "service": settings.app_name,
        "api_docs": "/docs",
        "health": "/health",
        "environment": settings.environment,
        "region": settings.region
    }


if __name__ == "__main__":
    # Execute uvicorn server directly if triggered
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)
