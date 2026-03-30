"""Health check endpoint."""

from fastapi import APIRouter, Depends
from app.api.deps import verify_api_health
from app.core.logging.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint.
    
    Returns:
        dict: Health status
    """
    await verify_api_health()
    return {
        "status": "healthy",
        "message": "All services are operational"
    }


@router.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check endpoint.
    
    Returns:
        dict: Detailed health status of all services
    """
    from app.services.infrastructure.database_service import get_database_service
    from app.services.infrastructure.cache_service import get_cache_service
    from app.services.infrastructure.queue_service import get_queue_service
    
    db_service = get_database_service()
    cache_service = get_cache_service()
    queue_service = get_queue_service()
    
    db_healthy = await db_service.health_check()
    cache_healthy = await cache_service.health_check()
    queue_healthy = await queue_service.health_check()
    
    overall_healthy = all([db_healthy, cache_healthy, queue_healthy])
    
    return {
        "status": "healthy" if overall_healthy else "unhealthy",
        "services": {
            "database": "healthy" if db_healthy else "unhealthy",
            "cache": "healthy" if cache_healthy else "unhealthy",
            "queue": "healthy" if queue_healthy else "unhealthy"
        }
    }


@router.get("/ping")
async def ping():
    """Simple ping endpoint.
    
    Returns:
        dict: Pong response
    """
    return {"message": "pong"}