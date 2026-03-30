"""Agent service for managing agent business logic."""

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.agent import Agent
from app.schemas.agent import AgentCreate, AgentUpdate, AgentResponse
from app.core.logging.logger import get_logger
from app.core.errors.api_errors import NotFoundError, ValidationError

logger = get_logger(__name__)


class AgentService:
    """Service layer for agent operations."""

    def __init__(self, db: AsyncSession):
        """Initialize agent service.
        
        Args:
            db: Database session
        """
        self.db = db

    async def create_agent(self, data: AgentCreate) -> Agent:
        """Create a new agent.
        
        Args:
            data: Agent creation data
            
        Returns:
            Created agent
        """
        try:
            agent = Agent(
                name=data.name,
                type=data.type,
                status="inactive",
                capabilities=data.capabilities or {},
                config=data.config or {},
            )
            self.db.add(agent)
            await self.db.commit()
            await self.db.refresh(agent)
            logger.info(f"Agent created: {agent.id}")
            return agent
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Failed to create agent: {e}")
            raise ValidationError(f"Failed to create agent: {str(e)}")

    async def get_agent(self, agent_id: int) -> Agent:
        """Get agent by ID.
        
        Args:
            agent_id: Agent ID
            
        Returns:
            Agent instance
            
        Raises:
            NotFoundError: If agent not found
        """
        result = await self.db.execute(
            select(Agent).where(Agent.id == agent_id)
        )
        agent = result.scalar_one_or_none()
        
        if not agent:
            raise NotFoundError(f"Agent with id {agent_id} not found")
        
        return agent

    async def list_agents(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        agent_type: Optional[str] = None,
    ) -> List[Agent]:
        """List agents with optional filters.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            status: Filter by status
            agent_type: Filter by type
            
        Returns:
            List of agents
        """
        query = select(Agent)
        
        if status:
            query = query.where(Agent.status == status)
        if agent_type:
            query = query.where(Agent.type == agent_type)
        
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def update_agent(
        self,
        agent_id: int,
        data: AgentUpdate,
    ) -> Agent:
        """Update agent.
        
        Args:
            agent_id: Agent ID
            data: Update data
            
        Returns:
            Updated agent
        """
        agent = await self.get_agent(agent_id)
        
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(agent, field, value)
        
        try:
            await self.db.commit()
            await self.db.refresh(agent)
            logger.info(f"Agent updated: {agent_id}")
            return agent
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Failed to update agent: {e}")
            raise ValidationError(f"Failed to update agent: {str(e)}")

    async def delete_agent(self, agent_id: int) -> None:
        """Delete agent.
        
        Args:
            agent_id: Agent ID
        """
        agent = await self.get_agent(agent_id)
        
        try:
            await self.db.delete(agent)
            await self.db.commit()
            logger.info(f"Agent deleted: {agent_id}")
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Failed to delete agent: {e}")
            raise ValidationError(f"Failed to delete agent: {str(e)}")

    async def activate_agent(self, agent_id: int) -> Agent:
        """Activate agent.
        
        Args:
            agent_id: Agent ID
            
        Returns:
            Activated agent
        """
        agent = await self.get_agent(agent_id)
        agent.status = "active"
        
        try:
            await self.db.commit()
            await self.db.refresh(agent)
            logger.info(f"Agent activated: {agent_id}")
            return agent
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Failed to activate agent: {e}")
            raise ValidationError(f"Failed to activate agent: {str(e)}")

    async def deactivate_agent(self, agent_id: int) -> Agent:
        """Deactivate agent.
        
        Args:
            agent_id: Agent ID
            
        Returns:
            Deactivated agent
        """
        agent = await self.get_agent(agent_id)
        agent.status = "inactive"
        
        try:
            await self.db.commit()
            await self.db.refresh(agent)
            logger.info(f"Agent deactivated: {agent_id}")
            return agent
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Failed to deactivate agent: {e}")
            raise ValidationError(f"Failed to deactivate agent: {str(e)}")