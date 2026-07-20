from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/health", summary="Health check endpoint", response_class=JSONResponse)
async def health_check() -> JSONResponse:
    """
    Performs platform status checks.
    Useful for container schedulers (Kubernetes, AWS ECS, Cloud Run) to verify container readiness.
    """
    # In full scaffold mode, this can verify database engine connectivity and Cache pools.
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "healthy",
            "service": "CorpStage AuthService",
            "dependencies": {
                "database": "uninitialized",
                "cache": "uninitialized"
            }
        }
    )
