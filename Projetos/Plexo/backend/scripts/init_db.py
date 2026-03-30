#!/usr/bin/env python3
# Database initialization script for Plexo system.
"""
Initialize PostgreSQL database with tables and initial schema.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config.database import init_db, get_engine
from app.config.kuzu import init_kuzu_schema
from app.config.settings import get_settings
from app.core.logging import get_logger, setup_logging
from app.models.base import Base

logger = get_logger(__name__)


async def create_tables():
    """Create all database tables."""
    logger.info("Creating database tables...")
    
    try:
        engine = get_engine()
        
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        logger.info("Database tables created successfully")
        
        await engine.dispose()
        
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise


async def initialize_kuzu():
    """Initialize KuzuDB schema for graph database."""
    logger.info("Initializing KuzuDB schema...")
    
    try:
        await init_kuzu_schema()
        logger.info("KuzuDB schema initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize KuzuDB schema: {e}")
        raise


async def verify_database():
    """Verify database connection and tables."""
    logger.info("Verifying database connection...")
    
    try:
        engine = get_engine()
        
        async with engine.connect() as conn:
            result = await conn.execute("SELECT 1")
            await result.fetchone()
        
        logger.info("Database connection verified")
        
        await engine.dispose()
        
    except Exception as e:
        logger.error(f"Database verification failed: {e}")
        raise


async def main():
    """Main initialization function."""
    setup_logging()
    settings = get_settings()
    
    logger.info("Starting database initialization...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Database URL: {settings.DATABASE_URL.split('@')[-1]}")
    
    try:
        await verify_database()
        await create_tables()
        await initialize_kuzu()
        
        logger.info("Database initialization completed successfully")
        return 0
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
