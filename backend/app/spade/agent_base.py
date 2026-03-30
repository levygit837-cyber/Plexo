# Base class for all SPADE agents in Plexo system.
# FEATURE: Multi-Agent Communication

from typing import Optional, Dict, Any, List
from abc import ABC, abstractmethod
import asyncio
from datetime import datetime

from spade.agent import Agent
from spade.message import Message
from spade.behaviour import CyclicBehaviour

from app.core.logging import get_logger
from app.core.errors import AgentError, AgentCommunicationError, AgentStateError
from app.interfaces.agent_interface import IAgent
from app.models.agent import AgentStatus, AgentType


logger = get_logger(__name__)


class PlexoAgent(Agent, IAgent, ABC):
    """
    Base class for all SPADE agents in Plexo.
    
    Extends SPADE Agent and implements IAgent interface.
    Provides common functionality for agent lifecycle, messaging, and state management.
    """

    def __init__(
        self,
        jid: str,
        password: str,
        agent_id: str,
        agent_type: AgentType,
        capabilities: Optional[List[str]] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize PlexoAgent.
        
        Args:
            jid: XMPP JID (Jabber ID) for the agent
            password: XMPP password
            agent_id: Unique identifier for the agent
            agent_type: Type of agent (from AgentType enum)
            capabilities: List of agent capabilities
            config: Additional configuration
        """
        super().__init__(jid, password)
        self._agent_id = agent_id
        self._agent_type = agent_type
        self._capabilities = capabilities or []
        self._config = config or {}
        self._status = AgentStatus.IDLE
        self._logger = get_logger(f"{__name__}.{agent_id}")
        self._message_handlers: Dict[str, callable] = {}
        self._started_at: Optional[datetime] = None

    @property
    def agent_id(self) -> str:
        """Get agent ID."""
        return self._agent_id

    @property
    def agent_type(self) -> AgentType:
        """Get agent type."""
        return self._agent_type

    @property
    def status(self) -> AgentStatus:
        """Get current agent status."""
        return self._status

    @property
    def capabilities(self) -> List[str]:
        """Get agent capabilities."""
        return self._capabilities.copy()

    async def setup(self) -> None:
        """
        Setup agent on startup.
        
        Override this method to add custom setup logic.
        Called automatically when agent starts.
        """
        self._started_at = datetime.utcnow()
        self._status = AgentStatus.IDLE
        self._logger.info(
            f"Agent {self._agent_id} setup completed",
            extra={"agent_id": self._agent_id, "type": self._agent_type.value}
        )

    async def start(self) -> None:
        """
        Start the agent.
        
        Implements IAgent.start()
        """
        try:
            self._logger.info(f"Starting agent {self._agent_id}")
            await super().start(auto_register=True)
            self._status = AgentStatus.ACTIVE
            self._logger.info(f"Agent {self._agent_id} started successfully")
        except Exception as e:
            self._logger.error(f"Failed to start agent {self._agent_id}: {e}")
            self._status = AgentStatus.ERROR
            raise AgentError(
                message=f"Failed to start agent {self._agent_id}",
                details={"error": str(e)}
            )

    async def stop(self) -> None:
        """
        Stop the agent.
        
        Implements IAgent.stop()
        """
        try:
            self._logger.info(f"Stopping agent {self._agent_id}")
            self._status = AgentStatus.STOPPED
            await super().stop()
            self._logger.info(f"Agent {self._agent_id} stopped successfully")
        except Exception as e:
            self._logger.error(f"Failed to stop agent {self._agent_id}: {e}")
            raise AgentError(
                message=f"Failed to stop agent {self._agent_id}",
                details={"error": str(e)}
            )

    async def send_message(
        self,
        to_jid: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Send message to another agent.
        
        Implements IAgent.send_message()
        
        Args:
            to_jid: Recipient JID
            content: Message content
            metadata: Optional message metadata
        """
        try:
            msg = Message(to=to_jid)
            msg.body = content
            
            if metadata:
                msg.metadata = metadata
            
            msg.set_metadata("sender_id", self._agent_id)
            msg.set_metadata("timestamp", datetime.utcnow().isoformat())
            
            await self.send(msg)
            
            self._logger.debug(
                f"Message sent from {self._agent_id} to {to_jid}",
                extra={"to": to_jid, "content_length": len(content)}
            )
        except Exception as e:
            self._logger.error(f"Failed to send message: {e}")
            raise AgentCommunicationError(
                message=f"Failed to send message from {self._agent_id} to {to_jid}",
                details={"error": str(e), "to_jid": to_jid}
            )

    async def receive_message(self, message: Message) -> None:
        """
        Receive and process incoming message.
        
        Implements IAgent.receive_message()
        
        Args:
            message: Incoming SPADE message
        """
        try:
            sender = str(message.sender)
            content = message.body
            metadata = message.metadata if hasattr(message, 'metadata') else {}
            
            self._logger.debug(
                f"Message received by {self._agent_id} from {sender}",
                extra={"from": sender, "content_length": len(content)}
            )
            
            message_type = metadata.get("type", "default")
            if message_type in self._message_handlers:
                await self._message_handlers[message_type](message)
            else:
                await self.on_message(message)
                
        except Exception as e:
            self._logger.error(f"Failed to process message: {e}")
            raise AgentCommunicationError(
                message=f"Failed to process message in {self._agent_id}",
                details={"error": str(e)}
            )

    @abstractmethod
    async def on_message(self, message: Message) -> None:
        """
        Handle incoming message.
        
        Override this method to implement custom message handling logic.
        
        Args:
            message: Incoming SPADE message
        """
        pass

    async def execute_task(self, task_data: Dict[str, Any]) -> Any:
        """
        Execute a task.
        
        Implements IAgent.execute_task()
        
        Args:
            task_data: Task data dictionary
            
        Returns:
            Task execution result
        """
        try:
            self._status = AgentStatus.BUSY
            self._logger.info(
                f"Agent {self._agent_id} executing task",
                extra={"task_id": task_data.get("id")}
            )
            
            result = await self.process_task(task_data)
            
            self._status = AgentStatus.IDLE
            return result
            
        except Exception as e:
            self._status = AgentStatus.ERROR
            self._logger.error(f"Task execution failed: {e}")
            raise AgentError(
                message=f"Task execution failed in {self._agent_id}",
                details={"error": str(e), "task_data": task_data}
            )

    @abstractmethod
    async def process_task(self, task_data: Dict[str, Any]) -> Any:
        """
        Process task logic.
        
        Override this method to implement custom task processing.
        
        Args:
            task_data: Task data dictionary
            
        Returns:
            Task processing result
        """
        pass

    def get_status(self) -> AgentStatus:
        """
        Get current agent status.
        
        Implements IAgent.get_status()
        
        Returns:
            Current agent status
        """
        return self._status

    def get_capabilities(self) -> List[str]:
        """
        Get agent capabilities.
        
        Implements IAgent.get_capabilities()
        
        Returns:
            List of capabilities
        """
        return self._capabilities.copy()

    def has_capability(self, capability: str) -> bool:
        """
        Check if agent has specific capability.
        
        Implements IAgent.has_capability()
        
        Args:
            capability: Capability to check
            
        Returns:
            True if agent has capability
        """
        return capability in self._capabilities

    def register_message_handler(self, message_type: str, handler: callable) -> None:
        """
        Register custom message handler.
        
        Args:
            message_type: Type of message to handle
            handler: Async callable to handle message
        """
        self._message_handlers[message_type] = handler
        self._logger.debug(f"Registered handler for message type: {message_type}")

    def get_info(self) -> Dict[str, Any]:
        """
        Get agent information.
        
        Returns:
            Dictionary with agent information
        """
        return {
            "id": self._agent_id,
            "jid": str(self.jid),
            "type": self._agent_type.value,
            "status": self._status.value,
            "capabilities": self._capabilities,
            "started_at": self._started_at.isoformat() if self._started_at else None,
            "config": self._config,
        }

    def update_status(self, new_status: AgentStatus) -> None:
        """
        Update agent status.
        
        Args:
            new_status: New status to set
        """
        old_status = self._status
        self._status = new_status
        self._logger.info(
            f"Agent {self._agent_id} status changed",
            extra={"old_status": old_status.value, "new_status": new_status.value}
        )
