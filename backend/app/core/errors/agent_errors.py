"""
Agent-specific exception classes for Plexo system.

This module defines exceptions related to agent operations and SPADE communication.
"""

from typing import Any, Dict, Optional

from .base import PlexoException


class AgentError(PlexoException):
    """Base class for agent-related errors."""
    
    def __init__(
        self,
        message: str,
        code: str = "AGENT_ERROR",
        agent_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        if details is None:
            details = {}
        if agent_id:
            details["agent_id"] = agent_id
        super().__init__(message, code, details)
        self.agent_id = agent_id


class AgentNotFoundError(AgentError):
    """Raised when an agent is not found in the registry."""
    
    def __init__(self, agent_id: str):
        message = f"Agent with ID '{agent_id}' not found"
        super().__init__(message, code="AGENT_NOT_FOUND", agent_id=agent_id)


class AgentRegistrationError(AgentError):
    """Raised when agent registration fails."""
    
    def __init__(self, agent_id: str, reason: str, details: Optional[Dict[str, Any]] = None):
        message = f"Failed to register agent '{agent_id}': {reason}"
        super().__init__(message, code="AGENT_REGISTRATION_FAILED", agent_id=agent_id, details=details)


class AgentCommunicationError(AgentError):
    """Raised when agent-to-agent communication fails."""
    
    def __init__(
        self,
        message: str,
        sender_id: Optional[str] = None,
        receiver_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        if details is None:
            details = {}
        if sender_id:
            details["sender_id"] = sender_id
        if receiver_id:
            details["receiver_id"] = receiver_id
        super().__init__(message, code="AGENT_COMMUNICATION_ERROR", details=details)


class AgentTimeoutError(AgentError):
    """Raised when an agent operation times out."""
    
    def __init__(self, agent_id: str, operation: str, timeout: float):
        message = f"Agent '{agent_id}' operation '{operation}' timed out after {timeout}s"
        super().__init__(
            message,
            code="AGENT_TIMEOUT",
            agent_id=agent_id,
            details={"operation": operation, "timeout": timeout},
        )


class AgentStateError(AgentError):
    """Raised when an agent is in an invalid state for an operation."""
    
    def __init__(self, agent_id: str, current_state: str, expected_state: str):
        message = f"Agent '{agent_id}' is in state '{current_state}', expected '{expected_state}'"
        super().__init__(
            message,
            code="AGENT_INVALID_STATE",
            agent_id=agent_id,
            details={"current_state": current_state, "expected_state": expected_state},
        )


class AgentCapabilityError(AgentError):
    """Raised when an agent doesn't have the required capability."""
    
    def __init__(self, agent_id: str, capability: str):
        message = f"Agent '{agent_id}' does not have capability '{capability}'"
        super().__init__(
            message,
            code="AGENT_CAPABILITY_MISSING",
            agent_id=agent_id,
            details={"capability": capability},
        )


class XMPPError(AgentError):
    """Raised when XMPP protocol operations fail."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="XMPP_ERROR", details=details)


class BehaviorError(AgentError):
    """Raised when an agent behavior fails."""
    
    def __init__(self, agent_id: str, behavior_name: str, reason: str):
        message = f"Behavior '{behavior_name}' failed for agent '{agent_id}': {reason}"
        super().__init__(
            message,
            code="BEHAVIOR_ERROR",
            agent_id=agent_id,
            details={"behavior": behavior_name, "reason": reason},
        )