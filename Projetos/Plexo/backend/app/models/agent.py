"""Agent model for database persistence."""

from typing import Dict, Any

from sqlalchemy import JSON, String, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
import enum

from app.models.base import BaseModel


class AgentStatus(str, enum.Enum):
    """Agent status enumeration."""

    IDLE = "idle"
    ACTIVE = "active"
    BUSY = "busy"
    ERROR = "error"
    STOPPED = "stopped"


class AgentType(str, enum.Enum):
    """Agent type enumeration."""

    COORDINATOR = "coordinator"
    WORKER = "worker"
    SPECIALIST = "specialist"
    MONITOR = "monitor"


class Agent(BaseModel):
    """Agent model for database persistence.

    Attributes:
        name: Agent name
        type: Agent type (coordinator, worker, specialist, monitor)
        status: Current agent status
        capabilities: Dictionary of agent capabilities
        config: Agent configuration dictionary
        jid: XMPP JID (Jabber ID) for SPADE communication
        metadata: Additional metadata
    """

    __tablename__ = "agents"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    type: Mapped[AgentType] = mapped_column(
        SQLEnum(AgentType), nullable=False, index=True
    )
    status: Mapped[AgentStatus] = mapped_column(
        SQLEnum(AgentStatus), nullable=False, default=AgentStatus.IDLE, index=True
    )
    capabilities: Mapped[Dict[str, Any]] = mapped_column(
        JSON, nullable=False, default=dict
    )
    config: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    jid: Mapped[str] = mapped_column(
        String(255), nullable=True, unique=True, index=True
    )
    metadata: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True, default=dict)

    def __repr__(self) -> str:
        """String representation of the agent."""
        return f"Agent(id={self.id}, name={self.name!r}, type={self.type.value}, status={self.status.value})"

    def is_active(self) -> bool:
        """Check if agent is active.

        Returns:
            bool: True if agent is active, False otherwise
        """
        return self.status == AgentStatus.ACTIVE

    def is_available(self) -> bool:
        """Check if agent is available for tasks.

        Returns:
            bool: True if agent is idle or active, False otherwise
        """
        return self.status in (AgentStatus.IDLE, AgentStatus.ACTIVE)

    def has_capability(self, capability: str) -> bool:
        """Check if agent has a specific capability.

        Args:
            capability: Capability name to check

        Returns:
            bool: True if agent has the capability, False otherwise
        """
        return capability in self.capabilities