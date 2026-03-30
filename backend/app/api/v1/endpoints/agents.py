"""Agent endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.api.deps import get_agent_service
from app.services.agent_service import AgentService
from app.schemas.agent import AgentCreate, AgentUpdate, AgentResponse
from app.core.logging.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post("/", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    data: AgentCreate,
    service: AgentService = Depends(get_agent_service)
):
    """Create a new agent.
    
    Args:
        data: Agent creation data
        service: Agent service instance
        
    Returns:
        Created agent
    """
    agent = await service.create_agent(data)
    return AgentResponse.model_validate(agent)


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: int,
    service: AgentService = Depends(get_agent_service)
):
    """Get agent by ID.
    
    Args:
        agent_id: Agent ID
        service: Agent service instance
        
    Returns:
        Agent details
    """
    agent = await service.get_agent(agent_id)
    return AgentResponse.model_validate(agent)


@router.get("/", response_model=List[AgentResponse])
async def list_agents(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = None,
    agent_type: Optional[str] = None,
    service: AgentService = Depends(get_agent_service)
):
    """List agents with optional filters.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        status: Filter by status
        agent_type: Filter by type
        service: Agent service instance
        
    Returns:
        List of agents
    """
    agents = await service.list_agents(
        skip=skip,
        limit=limit,
        status=status,
        agent_type=agent_type
    )
    return [AgentResponse.model_validate(agent) for agent in agents]


@router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: int,
    data: AgentUpdate,
    service: AgentService = Depends(get_agent_service)
):
    """Update agent.
    
    Args:
        agent_id: Agent ID
        data: Update data
        service: Agent service instance
        
    Returns:
        Updated agent
    """
    agent = await service.update_agent(agent_id, data)
    return AgentResponse.model_validate(agent)


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(
    agent_id: int,
    service: AgentService = Depends(get_agent_service)
):
    """Delete agent.
    
    Args:
        agent_id: Agent ID
        service: Agent service instance
    """
    await service.delete_agent(agent_id)


@router.post("/{agent_id}/activate", response_model=AgentResponse)
async def activate_agent(
    agent_id: int,
    service: AgentService = Depends(get_agent_service)
):
    """Activate agent.
    
    Args:
        agent_id: Agent ID
        service: Agent service instance
        
    Returns:
        Activated agent
    """
    agent = await service.activate_agent(agent_id)
    return AgentResponse.model_validate(agent)


@router.post("/{agent_id}/deactivate", response_model=AgentResponse)
async def deactivate_agent(
    agent_id: int,
    service: AgentService = Depends(get_agent_service)
):
    """Deactivate agent.
    
    Args:
        agent_id: Agent ID
        service: Agent service instance
        
    Returns:
        Deactivated agent
    """
    agent = await service.deactivate_agent(agent_id)
    return AgentResponse.model_validate(agent)