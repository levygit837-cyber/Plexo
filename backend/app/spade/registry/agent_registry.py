# Agent registry for managing active SPADE agents.
# FEATURE: Multi-Agent Communication

from typing import Optional, Dict, Any, List
import asyncio
from datetime import datetime
from threading import Lock

from app.core.logging import get_logger
from app.core.errors import AgentNotFoundError, AgentRegistrationError
from app.interfaces.agent_interface import IAgent, IAgentRegistry
from app.models.agent import AgentStatus


logger = get_logger(__name__)


class AgentRegistry(IAgentRegistry):
    """
    Registry for managing active SPADE agents.
    
    Implements IAgentRegistry interface.
    Provides thread-safe registration, lookup, and lifecycle management.
    """

    _instance: Optional['AgentRegistry'] = None
    _lock: Lock = Lock()

    def __new__(cls):
        """
        Singleton pattern implementation.
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initialize AgentRegistry.
        """
        if not hasattr(self, '_initialized'):
            self._agents: Dict[str, IAgent] = {}
            self._jid_to_id: Dict[str, str] = {}
            self._logger = get_logger(__name__)
            self._initialized = True

    async def register(self, agent: IAgent) -> None:
        """
        Register agent in registry.
        
        Implements IAgentRegistry.register()
        
        Args:
            agent: Agent to register
        """
        agent_id = agent.agent_id
        
        if agent_id in self._agents:
            raise AgentRegistrationError(
                agent_id=agent_id,
                reason="Agent already registered"
            )
        
        try:
            self._agents[agent_id] = agent
            
            if hasattr(agent, 'jid'):
                self._jid_to_id[str(agent.jid)] = agent_id
            
            self._logger.info(
                f"Agent {agent_id} registered",
                extra={"agent_id": agent_id, "total_agents": len(self._agents)}
            )
            
        except Exception as e:
            self._logger.error(f"Failed to register agent {agent_id}: {e}")
            raise AgentRegistrationError(
                agent_id=agent_id,
                reason=str(e)
            )

    async def unregister(self, agent_id: str) -> None:
        """
        Unregister agent from registry.
        
        Implements IAgentRegistry.unregister()
        
        Args:
            agent_id: ID of agent to unregister
        """
        if agent_id not in self._agents:
            raise AgentNotFoundError(agent_id=agent_id)
        
        try:
            agent = self._agents[agent_id]
            
            if hasattr(agent, 'jid'):
                jid = str(agent.jid)
                if jid in self._jid_to_id:
                    del self._jid_to_id[jid]
            
            del self._agents[agent_id]
            
            self._logger.info(
                f"Agent {agent_id} unregistered",
                extra={"agent_id": agent_id, "total_agents": len(self._agents)}
            )
            
        except Exception as e:
            self._logger.error(f"Failed to unregister agent {agent_id}: {e}")
            raise

    async def get(self, agent_id: str) -> Optional[IAgent]:
        """
        Get agent by ID.
        
        Implements IAgentRegistry.get()
        
        Args:
            agent_id: Agent ID
            
        Returns:
            Agent instance or None
        """
        return self._agents.get(agent_id)

    async def get_by_jid(self, jid: str) -> Optional[IAgent]:
        """
        Get agent by JID.
        
        Args:
            jid: Agent JID
            
        Returns:
            Agent instance or None
        """
        agent_id = self._jid_to_id.get(jid)
        if agent_id:
            return self._agents.get(agent_id)
        return None

    async def list_all(self) -> List[IAgent]:
        """
        List all registered agents.
        
        Implements IAgentRegistry.list_all()
        
        Returns:
            List of all agents
        """
        return list(self._agents.values())

    async def list_by_status(self, status: AgentStatus) -> List[IAgent]:
        """
        List agents by status.
        
        Implements IAgentRegistry.list_by_status()
        
        Args:
            status: Agent status to filter by
            
        Returns:
            List of agents with matching status
        """
        return [
            agent for agent in self._agents.values()
            if agent.get_status() == status
        ]

    async def list_by_capability(self, capability: str) -> List[IAgent]:
        """
        List agents by capability.
        
        Implements IAgentRegistry.list_by_capability()
        
        Args:
            capability: Capability to filter by
            
        Returns:
            List of agents with matching capability
        """
        return [
            agent for agent in self._agents.values()
            if agent.has_capability(capability)
        ]

    async def exists(self, agent_id: str) -> bool:
        """
        Check if agent exists in registry.
        
        Implements IAgentRegistry.exists()
        
        Args:
            agent_id: Agent ID to check
            
        Returns:
            True if agent exists
        """
        return agent_id in self._agents

    async def count(self) -> int:
        """
        Get total number of registered agents.
        
        Implements IAgentRegistry.count()
        
        Returns:
            Number of registered agents
        """
        return len(self._agents)

    async def clear(self) -> None:
        """
        Clear all registered agents.
        
        Implements IAgentRegistry.clear()
        """
        self._logger.warning("Clearing all registered agents")
        self._agents.clear()
        self._jid_to_id.clear()

    async def get_stats(self) -> Dict[str, Any]:
        """
        Get registry statistics.
        
        Returns:
            Dictionary with registry stats
        """
        status_counts = {}
        for agent in self._agents.values():
            status = agent.get_status().value
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            "total_agents": len(self._agents),
            "status_counts": status_counts,
            "registered_jids": len(self._jid_to_id),
        }

    async def find_available_agent(self, capability: Optional[str] = None) -> Optional[IAgent]:
        """
        Find an available agent, optionally with specific capability.
        
        Args:
            capability: Optional capability requirement
            
        Returns:
            Available agent or None
        """
        for agent in self._agents.values():
            if agent.get_status() == AgentStatus.IDLE:
                if capability is None or agent.has_capability(capability):
                    return agent
        return None

    async def broadcast_to_all(self, message_content: str, metadata: Optional[Dict[str, Any]] = None) -> int:
        """
        Broadcast message to all registered agents.
        
        Args:
            message_content: Message content
            metadata: Optional message metadata
            
        Returns:
            Number of agents message was sent to
        """
        sent_count = 0
        
        for agent in self._agents.values():
            try:
                if hasattr(agent, 'jid'):
                    await agent.send_message(
                        to_jid=str(agent.jid),
                        content=message_content,
                        metadata=metadata
                    )
                    sent_count += 1
            except Exception as e:
                self._logger.error(
                    f"Failed to broadcast to agent {agent.agent_id}: {e}",
                    extra={"agent_id": agent.agent_id}
                )
        
        return sent_count


def get_agent_registry() -> AgentRegistry:
    """
    Get singleton instance of AgentRegistry.
    
    Returns:
        AgentRegistry instance
    """
    return AgentRegistry()
