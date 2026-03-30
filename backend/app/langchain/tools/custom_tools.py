# Custom tools for LangChain integration.
# FEATURE: LangChain Integration

from typing import Optional, Dict, Any, Type
import asyncio
from datetime import datetime

from pydantic import BaseModel, Field

from app.core.logging import get_logger
from .base_tool import BaseTool, BaseToolInput


logger = get_logger(__name__)


class AgentQueryInput(BaseToolInput):
    """
    Input schema for agent query tool.
    """
    query: str = Field(..., description="Query to search for agents")
    capability: Optional[str] = Field(None, description="Optional capability filter")


class AgentQueryTool(BaseTool):
    """
    Tool for querying available agents.
    
    Searches for agents in the registry based on query and filters.
    """

    name: str = "agent_query"
    description: str = "Query available agents by capability or status"
    args_schema: Type[BaseModel] = AgentQueryInput

    def _execute(self, query: str, capability: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute agent query.
        
        Args:
            query: Search query
            capability: Optional capability filter
            
        Returns:
            Dictionary with query results
        """
        from app.spade.registry.agent_registry import get_agent_registry
        
        registry = get_agent_registry()
        
        agents = []
        if capability:
            agents = asyncio.run(registry.list_by_capability(capability))
        else:
            agents = asyncio.run(registry.list_all())
        
        return {
            "query": query,
            "capability": capability,
            "count": len(agents),
            "agents": [
                {
                    "id": agent.agent_id,
                    "type": agent.agent_type.value,
                    "status": agent.get_status().value,
                    "capabilities": agent.get_capabilities(),
                }
                for agent in agents
            ],
        }


class MessageSendInput(BaseToolInput):
    """
    Input schema for message send tool.
    """
    to_agent_id: str = Field(..., description="Target agent ID")
    content: str = Field(..., description="Message content")
    message_type: str = Field("default", description="Message type")


class MessageSendTool(BaseTool):
    """
    Tool for sending messages to agents.
    
    Sends messages to specific agents via the registry.
    """

    name: str = "message_send"
    description: str = "Send message to a specific agent"
    args_schema: Type[BaseModel] = MessageSendInput

    def _execute(
        self,
        to_agent_id: str,
        content: str,
        message_type: str = "default"
    ) -> Dict[str, Any]:
        """
        Execute message send.
        
        Args:
            to_agent_id: Target agent ID
            content: Message content
            message_type: Message type
            
        Returns:
            Dictionary with send result
        """
        from app.spade.registry.agent_registry import get_agent_registry
        
        registry = get_agent_registry()
        agent = asyncio.run(registry.get(to_agent_id))
        
        if not agent:
            return {
                "success": False,
                "error": f"Agent {to_agent_id} not found",
            }
        
        try:
            if hasattr(agent, 'jid'):
                asyncio.run(
                    agent.send_message(
                        to_jid=str(agent.jid),
                        content=content,
                        metadata={"type": message_type}
                    )
                )
            
            return {
                "success": True,
                "to_agent_id": to_agent_id,
                "message_type": message_type,
                "timestamp": datetime.utcnow().isoformat(),
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }


class TaskExecuteInput(BaseToolInput):
    """
    Input schema for task execute tool.
    """
    agent_id: str = Field(..., description="Agent ID to execute task")
    task_data: Dict[str, Any] = Field(..., description="Task data")


class TaskExecuteTool(BaseTool):
    """
    Tool for executing tasks on agents.
    
    Delegates task execution to specific agents.
    """

    name: str = "task_execute"
    description: str = "Execute a task on a specific agent"
    args_schema: Type[BaseModel] = TaskExecuteInput

    def _execute(
        self,
        agent_id: str,
        task_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute task on agent.
        
        Args:
            agent_id: Target agent ID
            task_data: Task data
            
        Returns:
            Dictionary with execution result
        """
        from app.spade.registry.agent_registry import get_agent_registry
        
        registry = get_agent_registry()
        agent = asyncio.run(registry.get(agent_id))
        
        if not agent:
            return {
                "success": False,
                "error": f"Agent {agent_id} not found",
            }
        
        try:
            result = asyncio.run(agent.execute_task(task_data))
            
            return {
                "success": True,
                "agent_id": agent_id,
                "result": result,
                "timestamp": datetime.utcnow().isoformat(),
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }


class MemorySearchInput(BaseToolInput):
    """
    Input schema for memory search tool.
    """
    query: str = Field(..., description="Search query")
    agent_id: Optional[str] = Field(None, description="Optional agent ID filter")
    limit: int = Field(10, description="Maximum results to return")


class MemorySearchTool(BaseTool):
    """
    Tool for searching agent memory.
    
    Searches both short-term and long-term memory.
    """

    name: str = "memory_search"
    description: str = "Search agent memory for relevant information"
    args_schema: Type[BaseModel] = MemorySearchInput

    def _execute(
        self,
        query: str,
        agent_id: Optional[str] = None,
        limit: int = 10
    ) -> Dict[str, Any]:
        """
        Execute memory search.
        
        Args:
            query: Search query
            agent_id: Optional agent ID filter
            limit: Maximum results
            
        Returns:
            Dictionary with search results
        """
        return {
            "query": query,
            "agent_id": agent_id,
            "limit": limit,
            "results": [],
            "note": "Memory search implementation pending",
        }


class AgentStatusInput(BaseToolInput):
    """
    Input schema for agent status tool.
    """
    agent_id: str = Field(..., description="Agent ID to check status")


class AgentStatusTool(BaseTool):
    """
    Tool for checking agent status.
    
    Retrieves current status and information about an agent.
    """

    name: str = "agent_status"
    description: str = "Check the status and information of a specific agent"
    args_schema: Type[BaseModel] = AgentStatusInput

    def _execute(self, agent_id: str) -> Dict[str, Any]:
        """
        Execute agent status check.
        
        Args:
            agent_id: Agent ID
            
        Returns:
            Dictionary with agent status
        """
        from app.spade.registry.agent_registry import get_agent_registry
        
        registry = get_agent_registry()
        agent = asyncio.run(registry.get(agent_id))
        
        if not agent:
            return {
                "success": False,
                "error": f"Agent {agent_id} not found",
            }
        
        return {
            "success": True,
            "agent_id": agent_id,
            "status": agent.get_status().value,
            "capabilities": agent.get_capabilities(),
            "info": agent.get_info() if hasattr(agent, 'get_info') else {},
        }


def get_default_tools() -> list[BaseTool]:
    """
    Get list of default tools.
    
    Returns:
        List of default tool instances
    """
    return [
        AgentQueryTool(),
        MessageSendTool(),
        TaskExecuteTool(),
        MemorySearchTool(),
        AgentStatusTool(),
    ]
