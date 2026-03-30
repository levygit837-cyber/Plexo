"""FastAPI dependencies for dependency injection."""

from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.infrastructure.database_service import get_database_service
from app.services.infrastructure.cache_service import get_cache_service
from app.services.infrastructure.queue_service import get_queue_service
from app.services.agent_service import AgentService
from app.services.task_service import TaskService
from app.services.message_service import MessageService
from app.core.logging.logger import get_logger

logger = get_logger(__name__)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session dependency.
    
    Yields:
        AsyncSession: Database session
    """
    db_service = get_database_service()
    async for session in db_service.get_session():
        yield session


async def get_agent_service(
    db: AsyncSession = Depends(get_db)
) -> AgentService:
    """Get agent service dependency.
    
    Args:
        db: Database session
        
    Returns:
        AgentService: Agent service instance
    """
    return AgentService(db)


async def get_task_service(
    db: AsyncSession = Depends(get_db)
) -> TaskService:
    """Get task service dependency.
    
    Args:
        db: Database session
        
    Returns:
        TaskService: Task service instance
    """
    return TaskService(db)


async def get_message_service(
    db: AsyncSession = Depends(get_db)
) -> MessageService:
    """Get message service dependency.
    
    Args:
        db: Database session
        
    Returns:
        MessageService: Message service instance
    """
    return MessageService(db)


def get_cache():
    """Get cache service dependency.
    
    Returns:
        CacheService: Cache service instance
    """
    return get_cache_service()


def get_queue():
    """Get queue service dependency.
    
    Returns:
        QueueService: Queue service instance
    """
    return get_queue_service()


async def verify_api_health() -> bool:
    """Verify API health status.
    
    Returns:
        bool: True if API is healthy
        
    Raises:
        HTTPException: If API is unhealthy
    """
    try:
        db_service = get_database_service()
        cache_service = get_cache_service()
        queue_service = get_queue_service()
        
        db_healthy = await db_service.health_check()
        cache_healthy = await cache_service.health_check()
        queue_healthy = await queue_service.health_check()
        
        if not all([db_healthy, cache_healthy, queue_healthy]):
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="One or more services are unhealthy"
            )
        
        return True
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Health check failed: {str(e)}"
        )