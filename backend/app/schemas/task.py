"""Task schemas for API requests and responses."""

from typing import Dict, Any, Optional
from datetime import datetime

from pydantic import Field, field_validator

from app.schemas.base import (
    BaseSchema,
    BaseDBSchema,
    BaseCreateSchema,
    BaseUpdateSchema,
    BaseResponseSchema,
)
from app.models.task import TaskStatus, TaskPriority


class TaskBase(BaseSchema):
    """Base task schema with common fields."""

    name: str = Field(..., min_length=1, max_length=255, description="Task name")
    description: Optional[str] = Field(default=None, description="Task description")
    priority: TaskPriority = Field(
        default=TaskPriority.NORMAL, description="Task priority"
    )
    payload: Dict[str, Any] = Field(
        default_factory=dict, description="Task input data"
    )
    max_retries: int = Field(default=3, ge=0, le=10, description="Maximum retries")
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional metadata"
    )


class TaskCreate(TaskBase, BaseCreateSchema):
    """Schema for creating a new task."""

    agent_id: Optional[int] = Field(
        default=None, description="ID of agent to assign task to"
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate task name."""
        if not v.strip():
            raise ValueError("Task name cannot be empty")
        return v.strip()


class TaskUpdate(BaseUpdateSchema):
    """Schema for updating a task."""

    name: Optional[str] = Field(
        default=None, min_length=1, max_length=255, description="Task name"
    )
    description: Optional[str] = Field(default=None, description="Task description")
    status: Optional[TaskStatus] = Field(default=None, description="Task status")
    priority: Optional[TaskPriority] = Field(default=None, description="Task priority")
    agent_id: Optional[int] = Field(default=None, description="Assigned agent ID")
    payload: Optional[Dict[str, Any]] = Field(
        default=None, description="Task input data"
    )
    result: Optional[Dict[str, Any]] = Field(
        default=None, description="Task output data"
    )
    error: Optional[Dict[str, Any]] = Field(
        default=None, description="Error information"
    )
    max_retries: Optional[int] = Field(
        default=None, ge=0, le=10, description="Maximum retries"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional metadata"
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        """Validate task name."""
        if v is not None and not v.strip():
            raise ValueError("Task name cannot be empty")
        return v.strip() if v else None


class TaskResponse(TaskBase, BaseResponseSchema):
    """Schema for task API responses."""

    status: TaskStatus = Field(..., description="Current task status")
    agent_id: Optional[int] = Field(default=None, description="Assigned agent ID")
    result: Optional[Dict[str, Any]] = Field(
        default=None, description="Task output data"
    )
    error: Optional[Dict[str, Any]] = Field(
        default=None, description="Error information"
    )
    started_at: Optional[datetime] = Field(
        default=None, description="Task start timestamp"
    )
    completed_at: Optional[datetime] = Field(
        default=None, description="Task completion timestamp"
    )
    retry_count: int = Field(default=0, description="Number of retry attempts")


class TaskListResponse(BaseSchema):
    """Schema for listing tasks."""

    tasks: list[TaskResponse] = Field(default_factory=list, description="List of tasks")
    total: int = Field(..., description="Total number of tasks")


class TaskStatusUpdate(BaseSchema):
    """Schema for updating task status."""

    status: TaskStatus = Field(..., description="New task status")


class TaskAssignment(BaseSchema):
    """Schema for assigning a task to an agent."""

    agent_id: int = Field(..., description="ID of agent to assign task to")


class TaskRetry(BaseSchema):
    """Schema for retrying a failed task."""

    reset_retry_count: bool = Field(
        default=False, description="Whether to reset retry count"
    )


class TaskCancel(BaseSchema):
    """Schema for cancelling a task."""

    reason: Optional[str] = Field(default=None, description="Cancellation reason")