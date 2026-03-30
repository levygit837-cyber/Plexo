# FEATURE: API
# FastAPI dependencies for dependency injection.

from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.database import async_session_maker
from app.config.redis import get_redis_client
from app.config.rabbitmq import get_rabbitmq_connection
from app.services.infrastructure.database_service import DatabaseService
from app.services.infrastructure.cache_service import CacheService
from app.services.infrastructure.queue_service import QueueService
from app.services.agent_service import AgentService
from app.services.task_service import TaskService
from app.services.message_service import MessageService
from app.services.xmpp_service import XMPPService
from app.services.p2p_service import P2PService
from app.core.logging.logger import get_logger

logger = get_logger(__name__)

# Global service instances
_xmpp_service: XMPPService = None
_p2p_service: P2PService = None


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session.
    
    Yields:
        AsyncSession: Database session
    """
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


def get_database_service(db: AsyncSession = Depends(get_db)) -> DatabaseService:
    """Get database service instance.
    
    Args:
        db: Database session
        
    Returns:
        DatabaseService: Database service instance
    """
    return DatabaseService(db)


def get_cache_service() -> CacheService:
    """Get cache service instance.
    
    Returns:
        CacheService: Cache service instance
    """
    redis_client = get_redis_client()
    return CacheService(redis_client)


def get_queue_service() -> QueueService:
    """Get queue service instance.
    
    Returns:
        QueueService: Queue service instance
    """
    connection = get_rabbitmq_connection()
    return QueueService(connection)


def get_agent_service(
    db: AsyncSession = Depends(get_db),
    cache: CacheService = Depends(get_cache_service)
) -> AgentService:
    """Get agent service instance.
    
    Args:
        db: Database session
        cache: Cache service
        
    Returns:
        AgentService: Agent service instance
    """
    return AgentService(db, cache)


def get_task_service(
    db: AsyncSession = Depends(get_db),
    cache: CacheService = Depends(get_cache_service)
) -> TaskService:
    """Get task service instance.
    
    Args:
        db: Database session
        cache: Cache service
        
    Returns:
        TaskService: Task service instance
    """
    return TaskService(db, cache)


def get_message_service(
    db: AsyncSession = Depends(get_db),
    cache: CacheService = Depends(get_cache_service)
) -> MessageService:
    """Get message service instance.
    
    Args:
        db: Database session
        cache: Cache service
        
    Returns:
        MessageService: Message service instance
    """
    return MessageService(db, cache)


def get_xmpp_service() -> XMPPService:
    """Get XMPP service instance.
    
    Returns:
        XMPPService: XMPP service instance
    """
    global _xmpp_service
    if _xmpp_service is None:
        _xmpp_service = XMPPService()
    return _xmpp_service


def get_p2p_service(
    xmpp_service: XMPPService = Depends(get_xmpp_service)
) -> P2PService:
    """Get P2P service instance.
    
    Args:
        xmpp_service: XMPP service
        
    Returns:
        P2PService: P2P service instance
    """
    global _p2p_service
    if _p2p_service is None:
        _p2p_service = P2PService(xmpp_service)
    return _p2p_service


async def verify_api_health() -> bool:
    """Verify API health status.
    
    Returns:
        bool: True if API is healthy
    """
    try:
        # Check database
        async with async_session_maker() as session:
            await session.execute("SELECT 1")
        
        # Check Redis
        redis_client = get_redis_client()
        await redis_client.ping()
        
        # Check RabbitMQ
        connection = get_rabbitmq_connection()
        if connection.is_closed:
            return False
        
        logger.info("API health check passed")
        return True
    except Exception as e:
        logger.error(f"API health check failed: {e}")
        return False
