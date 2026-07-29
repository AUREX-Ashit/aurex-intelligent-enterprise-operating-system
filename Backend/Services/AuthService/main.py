import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from middleware.tenant import TenantMiddleware
from middleware.logging import LoggingMiddleware
from routers import auth, health, organization, organization_establishment_attempt, person, role, domain, domain_permission, approval_authority, delegation_policy, runtime_assignment_policy, membership, organization_node, structural_change_intent, structural_proposal, impact_assessment, structural_review, structural_validation, structural_completion
from models.database import db_manager
from config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Lifespan events manager for FastAPI.
    Handles startup and shutdown of key system resources like database pools.
    """
    logger.info("Initializing application resources...")
    # Initialize the database engine and any global connections
    await db_manager.initialize()
    yield
    logger.info("Tearing down application resources...")
    await db_manager.close()

app = FastAPI(
    title="Aurex Authentication API",
    description="Authentication and authorization APIs for Aurex platform",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Set up CORS with dynamic configurations from Config/platform-config.yaml or environment overrides
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_credentials,
    allow_headers=settings.cors_headers,
    allow_methods=settings.cors_methods,
)

# Register Custom Middlewares
app.add_middleware(TenantMiddleware)
app.add_middleware(LoggingMiddleware)

# General Exception Handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    # Pydantic's raw error dicts embed the original exception instance in
    # ctx.error for any validator that raises a plain ValueError (e.g. a
    # @model_validator) — not JSON-serializable, and unnecessary here since
    # ctx.error's text is already duplicated in the error's own "msg" field.
    errors = [{k: v for k, v in error.items() if k != "ctx"} for error in exc.errors()]
    logger.error(f"Validation error on {request.url.path}: {errors}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": errors,
            "message": "Validation failed for request data."
        }
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.critical(f"Unhandled exception on {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "An internal server error occurred."}
    )

# Include Routers
app.include_router(health.router, prefix="", tags=["Health"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(person.router, prefix="/person", tags=["Person"])
app.include_router(organization.router, prefix="/organizations", tags=["Organization"])
app.include_router(
    organization_establishment_attempt.router,
    prefix="/organization-establishment-attempts",
    tags=["Organization Establishment Attempt"],
)
app.include_router(role.router, prefix="/roles", tags=["Role"])
app.include_router(domain.router, prefix="/domains", tags=["Domain"])
app.include_router(domain_permission.router, prefix="/domain-permissions", tags=["Domain Permission"])
app.include_router(approval_authority.router, prefix="/approval-authorities", tags=["Approval Authority"])
app.include_router(delegation_policy.router, prefix="/delegation-policies", tags=["Delegation Policy"])
app.include_router(runtime_assignment_policy.router, prefix="/runtime-assignment-policies", tags=["Runtime Assignment Policy"])
app.include_router(membership.router, prefix="/memberships", tags=["Membership"])
app.include_router(organization_node.router, prefix="/organization-nodes", tags=["Organization Node"])
app.include_router(structural_change_intent.router, prefix="/structural-change-intents", tags=["Structural Change Intent"])
app.include_router(structural_proposal.router, prefix="/structural-proposals", tags=["Structural Proposal"])
app.include_router(impact_assessment.router, prefix="/impact-assessments", tags=["Impact Assessment"])
app.include_router(structural_review.router, prefix="/structural-reviews", tags=["Structural Review"])
app.include_router(structural_validation.router, prefix="/structural-validations", tags=["Structural Validation"])
app.include_router(structural_completion.router, prefix="/structural-completions", tags=["Structural Completion"])
