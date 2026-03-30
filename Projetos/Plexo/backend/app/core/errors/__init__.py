"""Error handling module for Plexo system."""

from .agent_errors import (
    AgentCapabilityError,
    AgentCommunicationError,
    AgentError,
    AgentNotFoundError,
    AgentRegistrationError,
    AgentStateError,
    AgentTimeoutError,
    BehaviorError,
    XMPPError,
)
from .api_errors import (
    APIError,
    BadRequestError,
    ConflictError,
    ForbiddenError,
    InternalServerError,
    NotFoundAPIError,
    RateLimitError,
    ServiceUnavailableError,
    UnauthorizedError,
)
from .base import (
    ConfigurationError,
    DatabaseError,
    NotFoundError,
    PlexoException,
    ValidationError,
)
from .handlers import register_exception_handlers

__all__ = [
    # Base exceptions
    "PlexoException",
    "ValidationError",
    "NotFoundError",
    "ConfigurationError",
    "DatabaseError",
    # API exceptions
    "APIError",
    "BadRequestError",
    "UnauthorizedError",
    "ForbiddenError",
    "NotFoundAPIError",
    "ConflictError",
    "RateLimitError",
    "InternalServerError",
    "ServiceUnavailableError",
    # Agent exceptions
    "AgentError",
    "AgentNotFoundError",
    "AgentRegistrationError",
    "AgentCommunicationError",
    "AgentTimeoutError",
    "AgentStateError",
    "AgentCapabilityError",
    "XMPPError",
    "BehaviorError",
    # Handlers
    "register_exception_handlers",
]