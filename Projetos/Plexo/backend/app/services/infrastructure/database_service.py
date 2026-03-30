"""Database service for managing database connections and operations."""

from typing import AsyncGenerator, Optional
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from app.config.settings import get_settings
from app.core.logging.logger import get_logger

logger = get_logger(__name__)


class DatabaseService:
    """Service for managing database connections and sessions."""

    def __init__(self):
        """Initialize database service."""
        self.settings = get_settings()
        self.engine = None
        self.session_factory = None

    async def initialize(self) -> None:
        """Initialize database engine and session factory."""
        try:
            self.engine = create_async_engine(
                self.settings.DATABASE_URL,
                echo=self.settings.DEBUG,
                poolclass=NullPool if self.settings.TESTING else None,
                pool_pre_ping=True,
            )
            self.session_factory = async_sessionmaker(
                self.engine,
                class_=AsyncSession,
                expire_on_commit=False,
            )
            logger.info("Database service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database service: {e}")
            raise

    async def close(self) -> None:
        """Close database connections."""
        if self.engine:
            await self.engine.dispose()
            logger.info("Database connections closed")

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get database session.
        
        Yields:
            AsyncSession: Database session
        """
        if not self.session_factory:
            raise RuntimeError("Database service not initialized")
        
        async with self.session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def health_check(self) -> bool:
        """Check database health.
        
        Returns:
            bool: True if database is healthy
        """
        try:
            async with self.session_factory() as session:
                await session.execute("SELECT 1")
                return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False


# Global database service instance
_db_service: Optional[DatabaseService] = None


def get_database_service() -> DatabaseService:
    """Get global database service instance.
    
    Returns:
        DatabaseService: Database service instance
    """
    global _db_service
    if _db_service is None:
        _db_service = DatabaseService()
    return _db_service