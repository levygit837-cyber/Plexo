"""Task service for managing task business logic."""

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.core.logging.logger import get_logger
from app.core.errors.api_errors import NotFoundError, ValidationError

logger = get_logger(__name__)


class TaskService:
    """Service layer for task operations."""

    def __init__(self, db: AsyncSession):
        """Initialize task service.
        
        Args:
            db: Database session
        """
        self.db = db

    async def create_task(self, data: TaskCreate) -> Task:
        """Create a new task.
        
        Args:
            data: Task creation data
            
        Returns:
            Created task
        """
        try:
            task = Task(
                title=data.title,
                description=data.description,
                status="pending",
                priority=data.priority or 0,
                agent_id=data.agent_id,
                payload=data.payload or {},
                result=None,
            )
            self.db.add(task)
            await self.db.commit()
            await self.db.refresh(task)
            logger.info(f"Task created: {task.id}")
            return task
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Failed to create task: {e}")
            raise ValidationError(f"Failed to create task: {str(e)}")

    async def get_task(self, task_id: int) -> Task:
        """Get task by ID.
        
        Args:
            task_id: Task ID
            
        Returns:
            Task instance
            
        Raises:
            NotFoundError: If task not found
        """
        result = await self.db.execute(
            select(Task).where(Task.id == task_id)
        )
        task = result.scalar_one_or_none()
        
        if not task:
            raise NotFoundError(f"Task with id {task_id} not found")
        
        return task

    async def list_tasks(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        agent_id: Optional[int] = None,
        priority: Optional[int] = None,
    ) -> List[Task]:
        """List tasks with optional filters.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            status: Filter by status
            agent_id: Filter by agent ID
            priority: Filter by priority
            
        Returns:
            List of tasks
        """
        query = select(Task)
        
        if status:
            query = query.where(Task.status == status)
        if agent_id:
            query = query.where(Task.agent_id == agent_id)
        if priority is not None:
            query = query.where(Task.priority == priority)
        
        query = query.offset(skip).limit(limit).order_by(Task.priority.desc(), Task.created_at)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def update_task(
        self,
        task_id: int,
        data: TaskUpdate,
    ) -> Task:
        """Update task.
        
        Args:
            task_id: Task ID
            data: Update data
            
        Returns:
            Updated task
        """
        task = await self.get_task(task_id)
        
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)
        
        try:
            await self.db.commit()
            await self.db.refresh(task)
            logger.info(f"Task updated: {task_id}")
            return task
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Failed to update task: {e}")
            raise ValidationError(f"Failed to update task: {str(e)}")

    async def delete_task(self, task_id: int) -> None:
        """Delete task.
        
        Args:
            task_id: Task ID
        """
        task = await self.get_task(task_id)
        
        try:
            await self.db.delete(task)
            await self.db.commit()
            logger.info(f"Task deleted: {task_id}")
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Failed to delete task: {e}")
            raise ValidationError(f"Failed to delete task: {str(e)}")

    async def complete_task(self, task_id: int, result: dict) -> Task:
        """Mark task as completed.
        
        Args:
            task_id: Task ID
            result: Task result data
            
        Returns:
            Completed task
        """
        task = await self.get_task(task_id)
        task.status = "completed"
        task.result = result
        
        try:
            await self.db.commit()
            await self.db.refresh(task)
            logger.info(f"Task completed: {task_id}")
            return task
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Failed to complete task: {e}")
            raise ValidationError(f"Failed to complete task: {str(e)}")

    async def fail_task(self, task_id: int, error: str) -> Task:
        """Mark task as failed.
        
        Args:
            task_id: Task ID
            error: Error message
            
        Returns:
            Failed task
        """
        task = await self.get_task(task_id)
        task.status = "failed"
        task.result = {"error": error}
        
        try:
            await self.db.commit()
            await self.db.refresh(task)
            logger.info(f"Task failed: {task_id}")
            return task
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Failed to mark task as failed: {e}")
            raise ValidationError(f"Failed to mark task as failed: {str(e)}")

    async def start_task(self, task_id: int) -> Task:
        """Mark task as running.
        
        Args:
            task_id: Task ID
            
        Returns:
            Running task
        """
        task = await self.get_task(task_id)
        task.status = "running"
        
        try:
            await self.db.commit()
            await self.db.refresh(task)
            logger.info(f"Task started: {task_id}")
            return task
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Failed to start task: {e}")
            raise ValidationError(f"Failed to start task: {str(e)}")