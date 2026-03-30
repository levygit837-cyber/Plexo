"""
Plexo Multi-Agent System - Main Application Entry Point
"""
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config.settings import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Manage application lifecycle events (startup/shutdown).
    """
    settings = get_settings()
    
    # Startup
    print(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"📝 Environment: {settings.APP_ENV}")
    print(f"🔧 Debug mode: {settings.DEBUG}")
    
    # TODO: Initialize database connections
    # TODO: Initialize KuzuDB
    # TODO: Initialize RabbitMQ connections
    # TODO: Initialize Redis connections
    # TODO: Start SPADE agents registry
    
    yield
    
    # Shutdown
    print(f"🛑 Shutting down {settings.APP_NAME}")
    
    # TODO: Close database connections
    # TODO: Close KuzuDB connections
    # TODO: Close RabbitMQ connections
    # TODO: Close Redis connections
    # TODO: Stop SPADE agents


def create_app() -> FastAPI:
    """
    Factory function to create FastAPI application instance.
    
    Returns:
        FastAPI: Configured FastAPI application
    """
    settings = get_settings()
    
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Plexo Multi-Agent System Backend API",
        docs_url=f"{settings.API_V1_PREFIX}/docs",
        redoc_url=f"{settings.API_V1_PREFIX}/redoc",
        openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
        lifespan=lifespan,
    )
    
    setup_middleware(app)
    setup_routes(app)
    setup_exception_handlers(app)
    
    return app


def setup_middleware(app: FastAPI) -> None:
    """
    Configure application middlewares.
    
    Args:
        app: FastAPI application instance
    """
    settings = get_settings()
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # TODO: Add logging middleware
    # TODO: Add metrics middleware
    # TODO: Add request ID middleware


def setup_routes(app: FastAPI) -> None:
    """
    Register application routers.
    
    Args:
        app: FastAPI application instance
    """
    settings = get_settings()
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """Basic health check endpoint."""
        return JSONResponse(
            content={
                "status": "healthy",
                "app": settings.APP_NAME,
                "version": settings.APP_VERSION,
                "environment": settings.APP_ENV,
            }
        )
    
    # TODO: Register API v1 router
    # from app.api.v1.router import api_router
    # app.include_router(api_router, prefix=settings.API_V1_PREFIX)


def setup_exception_handlers(app: FastAPI) -> None:
    """
    Register exception handlers.
    
    Args:
        app: FastAPI application instance
    """
    # TODO: Add custom exception handlers
    # TODO: Add validation error handler
    # TODO: Add 404 handler
    # TODO: Add 500 handler
    pass


# Create application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    settings = get_settings()
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )