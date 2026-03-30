"""
Base exception classes for Plexo system.

This module defines the base exception hierarchy and common error handling utilities.
"""

import logging
from typing import Any, Dict, Optional
from datetime import datetime


class PlexoException(Exception):
    """
    Base exception for all Plexo errors.
    
    Attributes:
        message: Human-readable error message
        code: Error code for programmatic handling
        details: Additional error context
        timestamp: When the error occurred
    """
    
    def __init__(
        self,
        message: str,
        code: str = "PLEXO_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}
        self.timestamp = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert exception to dictionary format.
        
        Returns:
            Dictionary representation of the error
        """
        return {
            "error": {
                "code": self.code,
                "message": self.message,
                "details": self.details,
                "timestamp": self.timestamp.isoformat(),
            }
        }
    
    def log(self, logger: logging.Logger) -> None:
        """
        Log the exception with appropriate context.
        
        Args:
            logger: Logger instance to use
        """
        logger.error(
            self.message,
            extra={
                "error_code": self.code,
                "error_details": self.details,
                "timestamp": self.timestamp.isoformat(),
            },
        )


class ValidationError(PlexoException):
    """Raised when input validation fails."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="VALIDATION_ERROR", details=details)


class NotFoundError(PlexoException):
    """Raised when a requested resource is not found."""
    
    def __init__(self, resource: str, identifier: Any):
        message = f"{resource} with identifier '{identifier}' not found"
        super().__init__(
            message,
            code="NOT_FOUND",
            details={"resource": resource, "identifier": str(identifier)},
        )


class ConfigurationError(PlexoException):
    """Raised when there's a configuration issue."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="CONFIGURATION_ERROR", details=details)


class DatabaseError(PlexoException):
    """Raised when a database operation fails."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="DATABASE_ERROR", details=details)