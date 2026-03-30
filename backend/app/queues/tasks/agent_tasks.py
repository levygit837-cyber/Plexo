# Agent-related tasks for RabbitMQ queue processing.
# FEATURE: Multi-Agent Communication

from typing import Any, Dict, Optional
import asyncio
from datetime import datetime

from app.core.logging import get_logger
from app.core.errors.base import PlexoException
from app.models.agent import AgentStatus
from app.schemas.agent import AgentCreate, AgentUpdate

logger = get_logger(__name__)


class AgentTaskError(PlexoException):
    """Exception raised when agent task operations fail."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details)


async def create_agent_task(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Task to create a new agent."""
    try:
        logger.info(
            "Processing create agent task",
            extra={"agent_name": payload.get("name")}
        )
        
        return {
            "status": "success",
            "message": "Agent created successfully",
            "agent_id": payload.get("id"),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error(
            f"Failed to create agent: {e}",
            extra={"error": str(e), "payload": payload}
        )
        raise AgentTaskError(
            "Failed to create agent",
            details={"error": str(e), "payload": payload}
        )


async def update_agent_task(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Task to update an existing agent."""
    try:
        agent_id = payload.get("agent_id")
        logger.info(
            "Processing update agent task",
            extra={"agent_id": agent_id}
        )
        
        return {
            "status": "success",
            "message": "Agent updated successfully",
            "agent_id": agent_id,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error(
            f"Failed to update agent: {e}",
            extra={"error": str(e), "payload": payload}
        )
        raise AgentTaskError(
            "Failed to update agent",
            details={"error": str(e), "payload": payload}
        )


async def delete_agent_task(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Task to delete an agent."""
    try:
        agent_id = payload.get("agent_id")
        logger.info(
            "Processing delete agent task",
            extra={"agent_id": agent_id}
        )
        
        return {
            "status": "success",
            "message": "Agent deleted successfully",
            "agent_id": agent_id,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error(
            f"Failed to delete agent: {e}",
            extra={"error": str(e), "payload": payload}
        )
        raise AgentTaskError(
            "Failed to delete agent",
            details={"error": str(e), "payload": payload}
        )


async def start_agent_task(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Task to start an agent."""
    try:
        agent_id = payload.get("agent_id")
        logger.info(
            "Processing start agent task",
            extra={"agent_id": agent_id}
        )
        
        return {
            "status": "success",
            "message": "Agent started successfully",
            "agent_id": agent_id,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error(
            f"Failed to start agent: {e}",
            extra={"error": str(e), "payload": payload}
        )
        raise AgentTaskError(
            "Failed to start agent",
            details={"error": str(e), "payload": payload}
        )


async def stop_agent_task(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Task to stop an agent."""
    try:
        agent_id = payload.get("agent_id")
        logger.info(
            "Processing stop agent task",
            extra={"agent_id": agent_id}
        )
        
        return {
            "status": "success",
            "message": "Agent stopped successfully",
            "agent_id": agent_id,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error(
            f"Failed to stop agent: {e}",
            extra={"error": str(e), "payload": payload}
        )
        raise AgentTaskError(
            "Failed to stop agent",
            details={"error": str(e), "payload": payload}
        )


async def send_message_task(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Task to send a message between agents."""
    try:
        sender_id = payload.get("sender_id")
        receiver_id = payload.get("receiver_id")
        
        logger.info(
            "Processing send message task",
            extra={"sender_id": sender_id, "receiver_id": receiver_id}
        )
        
        return {
            "status": "success",
            "message": "Message sent successfully",
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error(
            f"Failed to send message: {e}",
            extra={"error": str(e), "payload": payload}
        )
        raise AgentTaskError(
            "Failed to send message",
            details={"error": str(e), "payload": payload}
        )


AGENT_TASK_HANDLERS = {
    "create_agent": create_agent_task,
    "update_agent": update_agent_task,
    "delete_agent": delete_agent_task,
    "start_agent": start_agent_task,
    "stop_agent": stop_agent_task,
    "send_message": send_message_task,
}
