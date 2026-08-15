# main.py
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Core configuration configurations
from config.settings import settings
from models.database import init_db

# Custom logging and tenancy middlewares
from middleware.logging import LoggingMiddleware
from middleware.tenant import TenantHeaderMiddleware

# Router controllers
from routers.health import router as health_router
from routers.extraction import router as extraction_router
from routers.validation import router as validation_router
from routers.scoring import router as scoring_router
from routers.search import router as search_router
from routers.conversation import router as conversation_router
from routers.knowledge_assets import router as knowledge_assets_router
from routers.discovery_providers import router as discovery_providers_router
from routers.intelligence_candidates import router as intelligence_candidates_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Execution bounds covering app lifespan milestones (startup and shutdown)."""
    # Trigger database schema assembly for active connections
    await init_db()
    yield

# Configure central FastAPI application
app = FastAPI(
    title=f"{settings.platform_name} Enterprise AI Service",
    description="Multi-tenant unstructured data extraction and compliance rating system.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Apply CORS middleware parameters according to configuration standards
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins if hasattr(settings, "allowed_origins") else ["*"],
    allow_credentials=settings.allow_credentials if hasattr(settings, "allow_credentials") else True,
    allow_methods=settings.allow_methods if hasattr(settings, "allow_methods") else ["*"],
    allow_headers=settings.allow_headers if hasattr(settings, "allow_headers") else ["*"],
)

# Bind custom system metrics logging middleware
app.add_middleware(LoggingMiddleware)

# Bind strict multi-tenant isolation header tracking gates
app.add_middleware(TenantHeaderMiddleware)

# Bind router divisions
app.include_router(health_router)
app.include_router(extraction_router)
app.include_router(validation_router)
app.include_router(scoring_router)
app.include_router(search_router)
app.include_router(conversation_router)
app.include_router(knowledge_assets_router)
app.include_router(discovery_providers_router)
app.include_router(intelligence_candidates_router)

@app.get("/", tags=["Root"])
async def root_welcome_portal():
    return {
        "portal": f"Welcome to the {settings.platform_name} AI Core Microservice Engine.",
        "version": "1.0.0",
        "region": settings.region,
        "environment": settings.environment,
        "specifications": "/docs"
    }

if __name__ == "__main__":
    # Start ASGI runner
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)
