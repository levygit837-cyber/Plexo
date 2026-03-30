"""
API-specific exception classes for Plexo system.

This module defines exceptions related to HTTP API operations.
"""

from typing import Any, Dict, Optional

from .base import PlexoException


class APIError(PlexoException):
    """Base class for API-related errors."""
    
    def __init__(
        self,
        message: str,
        code: str = "API_ERROR",
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message, code, details)
        self.status_code = status_code


class BadRequestError(APIError):
    """Raised when the request is malformed or invalid."""
    
    def __init__(self, message: str = "Bad request", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="BAD_REQUEST", status_code=400, details=details)


class UnauthorizedError(APIError):
    """Raised when authentication is required but not provided."""
    
    def __init__(self, message: str = "Unauthorized", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="UNAUTHORIZED", status_code=401, details=details)


class ForbiddenError(APIError):
    """Raised when the user doesn't have permission to access a resource."""
    
    def __init__(self, message: str = "Forbidden", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="FORBIDDEN", status_code=403, details=details)


class NotFoundAPIError(APIError):
    """Raised when a requested API resource is not found."""
    
    def __init__(self, resource: str, identifier: Any):
        message = f"{resource} with identifier '{identifier}' not found"
        super().__init__(
            message,
            code="NOT_FOUND",
            status_code=404,
            details={"resource": resource, "identifier": str(identifier)},
        )


class ConflictError(APIError):
    """Raised when there's a conflict with the current state."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="CONFLICT", status_code=409, details=details)


class RateLimitError(APIError):
    """Raised when rate limit is exceeded."""
    
    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        if details is None:
            details = {}
        if retry_after:
            details["retry_after"] = retry_after
        super().__init__(message, code="RATE_LIMIT_EXCEEDED", status_code=429, details=details)


class InternalServerError(APIError):
    """Raised when an unexpected internal error occurs."""
    
    def __init__(self, message: str = "Internal server error", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="INTERNAL_SERVER_ERROR", status_code=500, details=details)


class ServiceUnavailableError(APIError):
    """Raised when a service is temporarily unavailable."""
    
    def __init__(self, message: str = "Service unavailable", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="SERVICE_UNAVAILABLE", status_code=503, details=details)