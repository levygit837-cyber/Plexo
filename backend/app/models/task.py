"""Task model for database persistence."""

from typing import Dict, Any, Optional
from datetime import datetime

from sqlalchemy import JSON, String, Text, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.models.base import BaseModel


class TaskStatus(str, enum.Enum):
    """Task status enumeration."""

    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETRYING = "retrying"


class TaskPriority(str, enum.Enum):
    """Task priority enumeration."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class Task(BaseModel):
    """Task model for database persistence.

    Attributes:
        name: Task name
        description: Task description
        status: Current task status
        priority: Task priority level
        agent_id: ID of the agent assigned to this task
        payload: Task input data
        result: Task output data
        error: Error information if task failed
        started_at: Timestamp when task started execution
        completed_at: Timestamp when task completed
        retry_count: Number of retry attempts
        max_retries: Maximum number of retries allowed
        metadata: Additional metadata
    """

    __tablename__ = "tasks"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[TaskStatus] = mapped_column(
        SQLEnum(TaskStatus), nullable=False, default=TaskStatus.PENDING, index=True
    )
    priority: Mapped[TaskPriority] = mapped_column(
        SQLEnum(TaskPriority), nullable=False, default=TaskPriority.NORMAL, index=True
    )
    agent_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("agents.id", ondelete="SET NULL"), nullable=True, index=True
    )
    payload: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    result: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    error: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    started_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    retry_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    max_retries: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    metadata: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True, default=dict)

    # Relationships
    # agent: Mapped["Agent"] = relationship("Agent", back_populates="tasks")

    def __repr__(self) -> str:
        """String representation of the task."""
        return f"Task(id={self.id}, name={self.name!r}, status={self.status.value}, priority={self.priority.value})"

    def is_pending(self) -> bool:
        """Check if task is pending.

        Returns:
            bool: True if task is pending, False otherwise
        """
        return self.status == TaskStatus.PENDING

    def is_running(self) -> bool:
        """Check if task is running.

        Returns:
            bool: True if task is running, False otherwise
        """
        return self.status == TaskStatus.RUNNING

    def is_completed(self) -> bool:
        """Check if task is completed.

        Returns:
            bool: True if task is completed, False otherwise
        """
        return self.status == TaskStatus.COMPLETED

    def is_failed(self) -> bool:
        """Check if task has failed.

        Returns:
            bool: True if task has failed, False otherwise
        """
        return self.status == TaskStatus.FAILED

    def can_retry(self) -> bool:
        """Check if task can be retried.

        Returns:
            bool: True if task can be retried, False otherwise
        """
        return self.is_failed() and self.retry_count < self.max_retries

    def get_duration(self) -> Optional[float]:
        """Get task execution duration in seconds.

        Returns:
            Optional[float]: Duration in seconds if task has started, None otherwise
        """
        if not self.started_at:
            return None
        
        end_time = self.completed_at or datetime.utcnow()
        return (end_time - self.started_at).total_seconds()