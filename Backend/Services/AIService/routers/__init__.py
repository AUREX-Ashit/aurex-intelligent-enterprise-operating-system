# routers/__init__.py
from routers.extraction import router as extraction_router
from routers.validation import router as validation_router
from routers.scoring import router as scoring_router
from routers.health import router as health_router
from routers.search import router as search_router

__all__ = ["extraction_router", "validation_router", "scoring_router", "health_router", "search_router"]
