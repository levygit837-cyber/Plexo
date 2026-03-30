"""
Error handlers for FastAPI integration.

This module provides exception handlers that convert Plexo exceptions
into appropriate HTTP responses.
"""

from typing import Union

from fastapi import Request, status
from fastapi.responses import JSONResponse

from .api_errors import APIError
from .agent_errors import AgentError
from .base import PlexoException


async def plexo_exception_handler(request: Request, exc: PlexoException) -> JSONResponse:
    """
    Handle PlexoException and its subclasses.
    
    Args:
        request: FastAPI request object
        exc: The exception that was raised
        
    Returns:
        JSON response with error details
    """
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    
    # Determine status code based on exception type
    if isinstance(exc, APIError):
        status_code = exc.status_code
    
    return JSONResponse(
        status_code=status_code,
        content=exc.to_dict(),
    )


async def agent_exception_handler(request: Request, exc: AgentError) -> JSONResponse:
    """
    Handle AgentError and its subclasses.
    
    Args:
        request: FastAPI request object
        exc: The agent exception that was raised
        
    Returns:
        JSON response with error details
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=exc.to_dict(),
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle unexpected exceptions.
    
    Args:
        request: FastAPI request object
        exc: The exception that was raised
        
    Returns:
        JSON response with generic error message
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred",
                "details": {"exception_type": type(exc).__name__},
            }
        },
    )


def register_exception_handlers(app) -> None:
    """
    Register all exception handlers with the FastAPI application.
    
    Args:
        app: FastAPI application instance
    """
    app.add_exception_handler(PlexoException, plexo_exception_handler)
    app.add_exception_handler(AgentError, agent_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)