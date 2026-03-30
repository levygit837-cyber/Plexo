"""Task endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.api.deps import get_task_service
from app.services.task_service import TaskService
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.core.logging.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    data: TaskCreate,
    service: TaskService = Depends(get_task_service)
):
    """Create a new task.
    
    Args:
        data: Task creation data
        service: Task service instance
        
    Returns:
        Created task
    """
    task = await service.create_task(data)
    return TaskResponse.model_validate(task)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    service: TaskService = Depends(get_task_service)
):
    """Get task by ID.
    
    Args:
        task_id: Task ID
        service: Task service instance
        
    Returns:
        Task details
    """
    task = await service.get_task(task_id)
    return TaskResponse.model_validate(task)


@router.get("/", response_model=List[TaskResponse])
async def list_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = None,
    agent_id: Optional[int] = None,
    priority: Optional[int] = None,
    service: TaskService = Depends(get_task_service)
):
    """List tasks with optional filters.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        status: Filter by status
        agent_id: Filter by agent ID
        priority: Filter by priority
        service: Task service instance
        
    Returns:
        List of tasks
    """
    tasks = await service.list_tasks(
        skip=skip,
        limit=limit,
        status=status,
        agent_id=agent_id,
        priority=priority
    )
    return [TaskResponse.model_validate(task) for task in tasks]


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    data: TaskUpdate,
    service: TaskService = Depends(get_task_service)
):
    """Update task.
    
    Args:
        task_id: Task ID
        data: Update data
        service: Task service instance
        
    Returns:
        Updated task
    """
    task = await service.update_task(task_id, data)
    return TaskResponse.model_validate(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service)
):
    """Delete task.
    
    Args:
        task_id: Task ID
        service: Task service instance
    """
    await service.delete_task(task_id)


@router.post("/{task_id}/start", response_model=TaskResponse)
async def start_task(
    task_id: int,
    service: TaskService = Depends(get_task_service)
):
    """Start task execution.
    
    Args:
        task_id: Task ID
        service: Task service instance
        
    Returns:
        Started task
    """
    task = await service.start_task(task_id)
    return TaskResponse.model_validate(task)


@router.post("/{task_id}/complete", response_model=TaskResponse)
async def complete_task(
    task_id: int,
    result: dict,
    service: TaskService = Depends(get_task_service)
):
    """Mark task as completed.
    
    Args:
        task_id: Task ID
        result: Task result data
        service: Task service instance
        
    Returns:
        Completed task
    """
    task = await service.complete_task(task_id, result)
    return TaskResponse.model_validate(task)


@router.post("/{task_id}/fail", response_model=TaskResponse)
async def fail_task(
    task_id: int,
    error: str,
    service: TaskService = Depends(get_task_service)
):
    """Mark task as failed.
    
    Args:
        task_id: Task ID
        error: Error message
        service: Task service instance
        
    Returns:
        Failed task
    """
    task = await service.fail_task(task_id, error)
    return TaskResponse.model_validate(task)