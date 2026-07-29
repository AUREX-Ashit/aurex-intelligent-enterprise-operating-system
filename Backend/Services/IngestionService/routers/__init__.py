"""
Aurex Router Modules (HTTP interface mappings).
"""
from .ingestion import ingestion_router
from .health import health_router

__all__ = ["ingestion_router", "health_router"]
