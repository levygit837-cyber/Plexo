"""Abstract interface for agents."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from app.schemas.agent import AgentCreate, AgentResponse, AgentUpdate


class Agent(ABC):
    """Abstract interface for agent operations."""

    @abstractmethod
    async def setup(self) -> None:
        """Initialize agent and its behaviors.

        Raises:
            AgentError: If setup fails
        """
        pass

    @abstractmethod
    async def start(self) -> None:
        """Start the agent.

        Raises:
            AgentError: If agent fails to start
        """
        pass

    @abstractmethod
    async def stop(self) -> None:
        """Stop the agent gracefully.

        Raises:
            AgentError: If agent fails to stop
        """
        pass

    @abstractmethod
    async def send_message(self, to_jid: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Send a message to another agent.

        Args:
            to_jid: Target agent JID
            content: Message content
            metadata: Optional message metadata

        Raises:
            AgentError: If message fails to send
        """
        pass

    @abstractmethod
    async def receive_message(self, message: Any) -> None:
        """Process received message.

        Args:
            message: Received message object

        Raises:
            AgentError: If message processing fails
        """
        pass

    @abstractmethod
    async def get_status(self) -> Dict[str, Any]:
        """Get current agent status.

        Returns:
            Dict[str, Any]: Agent status information
        """
        pass

    @abstractmethod
    async def update_capabilities(self, capabilities: Dict[str, Any]) -> None:
        """Update agent capabilities.

        Args:
            capabilities: New capabilities dictionary

        Raises:
            AgentError: If update fails
        """
        pass


class AgentRegistry(ABC):
    """Abstract interface for agent registry operations."""

    @abstractmethod
    async def register(self, agent_id: str, agent: IAgent) -> None:
        """Register an agent in the registry.

        Args:
            agent_id: Unique agent identifier
            agent: Agent instance

        Raises:
            AgentError: If registration fails
        """
        pass

    @abstractmethod
    async def unregister(self, agent_id: str) -> None:
        """Unregister an agent from the registry.

        Args:
            agent_id: Agent identifier to unregister

        Raises:
            AgentError: If unregistration fails
        """
        pass

    @abstractmethod
    async def get(self, agent_id: str) -> Optional[IAgent]:
        """Get an agent from the registry.

        Args:
            agent_id: Agent identifier

        Returns:
            Optional[IAgent]: Agent instance if found, None otherwise
        """
        pass

    @abstractmethod
    async def list_all(self) -> List[str]:
        """List all registered agent IDs.

        Returns:
            List[str]: List of agent IDs
        """
        pass

    @abstractmethod
    async def is_registered(self, agent_id: str) -> bool:
        """Check if an agent is registered.

        Args:
            agent_id: Agent identifier

        Returns:
            bool: True if registered, False otherwise
        """
        pass