from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from models.database import db_manager
from services.bootstrap_service import BootstrapService
from services.feature_flag_service import feature_flags

router = APIRouter()


@router.get("/health", summary="Liveness probe", response_class=JSONResponse)
async def health_check(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> JSONResponse:
    """
    Liveness: is the process itself up and able to reach its dependencies?
    Per Kubernetes/ECS/Cloud Run convention, this answers "should the
    scheduler restart this container?" — it does not answer "should this
    container receive traffic?" (that is /ready, below). Reuses the same
    db_manager.get_session dependency every other router in this service
    depends on (routers/auth.py, routers/person.py), so the test suite's
    existing app.dependency_overrides[db_manager.get_session] override
    applies here identically — no parallel session-acquisition path.
    """
    try:
        await session.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception:
        db_status = "unhealthy"

    overall_healthy = db_status == "healthy"
    return JSONResponse(
        status_code=status.HTTP_200_OK if overall_healthy else status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "status": "healthy" if overall_healthy else "unhealthy",
            "service": "CorpStage AuthService",
            "dependencies": {"database": db_status},
        },
    )


@router.get("/ready", summary="Readiness probe (WP-00)", response_class=JSONResponse)
async def readiness_check(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
) -> JSONResponse:
    """
    Readiness: can this instance correctly serve traffic right now?
    Distinct from liveness — a process can be alive (DB reachable) but not
    yet ready (bootstrap seed data not yet applied, so the Platform
    Administrator cannot log in). Per the Aurex Platform Administrator
    Roadmap's Operational Readiness framework: "the platform SHALL be
    observable from the first Work Package."
    """
    try:
        await session.execute(text("SELECT 1"))
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "not_ready", "reason": "database_unreachable"},
        )

    try:
        bootstrapped = await BootstrapService(session).is_bootstrapped()
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "not_ready", "reason": "bootstrap_check_failed"},
        )

    if not bootstrapped:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "not_ready", "reason": "bootstrap_not_applied"},
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "ready",
            "service": "CorpStage AuthService",
            "bootstrap": "complete",
            "feature_flags": feature_flags.all_flags(),
        },
    )
