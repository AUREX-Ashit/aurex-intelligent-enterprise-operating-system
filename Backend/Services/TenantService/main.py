from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from config.settings import settings
from routers.tenant import router as tenant_router
from middleware.tenant import TenantHeaderMiddleware
from middleware.logging import StructuredLoggingMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles startup operations (e.g., database connection pool initialization, cache configs, metadata logging)
    and shutdown cleanups.
    """
    # Startup logging
    print(f"Bootstrapping '{settings.platform.name}' TenantService...")
    print(f"Environment: {settings.platform.environment} in Region: {settings.platform.region}")
    print(f"Primary Database Engine: {settings.database.primary_engine}")
    print(f"Primary AI LLM Provider: {settings.ai.primary_provider}")
    
    yield
    
    # Shutdown cleaning
    print("Shutting down TenantService connection pools...")


app = FastAPI(
    title="CorpStage TenantService",
    description="Production-grade, asynchronous SaaS Tenant & Organization Provisioning Microservice.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# App state configuration
app.state.env = settings.platform.environment

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors.allow_origins,
    allow_credentials=settings.cors.allow_credentials,
    allow_methods=settings.cors.allow_methods,
    allow_headers=settings.cors.allow_headers,
)

# Core Business Middlewares (order: Logging -> TenantHeader)
app.add_middleware(TenantHeaderMiddleware)
app.add_middleware(StructuredLoggingMiddleware)


# Global routers registration
app.include_router(tenant_router)


@app.get("/", tags=["Monitoring"])
async def root():
    """
    Standard index endpoint returning platform description and specification links.
    """
    return {
        "platform": settings.platform.name,
        "service": "TenantService",
        "status": "online",
        "environment": settings.platform.environment,
        "docs_url": "/docs",
        "active_features": {
            "copilot": settings.feature_flags.enable_copilot,
            "rag": settings.feature_flags.enable_rag,
            "financial_intelligence": settings.feature_flags.enable_financial_intelligence
        }
    }


@app.get("/health", tags=["Monitoring"])
async def health_check():
    """
    Platform health endpoint used by container orchestration systems (Kubernetes, AWS ECS, Azure App Service).
    Performs quick sub-system verification.
    """
    return {
        "status": "healthy",
        "version": "1.0.0",
        "database": "connected" if settings.database.postgresql.enabled else "disabled",
        "ai_gateway": "ready" if settings.ai.providers.azure_openai.enabled else "offline",
        "storage": "connected" if settings.storage.primary_provider else "disabled"
    }


# ==========================================
# Exception Handlers
# ==========================================
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """
    Gracefully formats unhandled application errors inside JSON blocks to hide technical stack traces.
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "InternalServerError",
            "message": "A critical system error occurred. Please contact CorpStage Operations.",
            "details": str(exc) if settings.platform.environment == "development" else None
        }
    )
