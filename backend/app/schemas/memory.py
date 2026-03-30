"""Memory schemas for API requests and responses."""

from typing import Dict, Any, Optional, List
from datetime import datetime

from pydantic import Field, field_validator

from app.schemas.base import (
    BaseSchema,
    BaseDBSchema,
    BaseCreateSchema,
    BaseUpdateSchema,
    BaseResponseSchema,
)


# Short-term memory schemas


class ShortTermMemoryBase(BaseSchema):
    """Base short-term memory schema with common fields."""

    session_id: str = Field(..., max_length=255, description="Unique session identifier")
    context: Dict[str, Any] = Field(
        default_factory=dict, description="Session context data"
    )
    ttl: int = Field(default=3600, ge=60, le=86400, description="Time-to-live in seconds")
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional metadata"
    )


class ShortTermMemoryCreate(ShortTermMemoryBase, BaseCreateSchema):
    """Schema for creating a new short-term memory."""

    agent_id: int = Field(..., description="ID of the agent")

    @field_validator("session_id")
    @classmethod
    def validate_session_id(cls, v: str) -> str:
        """Validate session ID."""
        if not v.strip():
            raise ValueError("Session ID cannot be empty")
        return v.strip()


class ShortTermMemoryUpdate(BaseUpdateSchema):
    """Schema for updating a short-term memory."""

    context: Optional[Dict[str, Any]] = Field(
        default=None, description="Session context data"
    )
    ttl: Optional[int] = Field(
        default=None, ge=60, le=86400, description="Time-to-live in seconds"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional metadata"
    )


class ShortTermMemoryResponse(ShortTermMemoryBase, BaseResponseSchema):
    """Schema for short-term memory API responses."""

    agent_id: int = Field(..., description="ID of the agent")
    expires_at: datetime = Field(..., description="Expiration timestamp")


class ShortTermMemoryListResponse(BaseSchema):
    """Schema for listing short-term memories."""

    memories: List[ShortTermMemoryResponse] = Field(
        default_factory=list, description="List of short-term memories"
    )
    total: int = Field(..., description="Total number of memories")


# Long-term memory schemas


class LongTermMemoryBase(BaseSchema):
    """Base long-term memory schema with common fields."""

    knowledge_type: str = Field(
        ..., max_length=50, description="Type of knowledge"
    )
    content: str = Field(..., min_length=1, description="Memory content")
    tags: List[str] = Field(default_factory=list, description="Tags for categorization")
    importance: int = Field(
        default=50, ge=0, le=100, description="Importance score (0-100)"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional metadata"
    )


class LongTermMemoryCreate(LongTermMemoryBase, BaseCreateSchema):
    """Schema for creating a new long-term memory."""

    agent_id: int = Field(..., description="ID of the agent")
    embeddings: Optional[List[float]] = Field(
        default=None, description="Vector embeddings"
    )

    @field_validator("content")
    @classmethod
    def validate_content(cls, v: str) -> str:
        """Validate memory content."""
        if not v.strip():
            raise ValueError("Memory content cannot be empty")
        return v.strip()


class LongTermMemoryUpdate(BaseUpdateSchema):
    """Schema for updating a long-term memory."""

    knowledge_type: Optional[str] = Field(
        default=None, max_length=50, description="Type of knowledge"
    )
    content: Optional[str] = Field(
        default=None, min_length=1, description="Memory content"
    )
    embeddings: Optional[List[float]] = Field(
        default=None, description="Vector embeddings"
    )
    tags: Optional[List[str]] = Field(
        default=None, description="Tags for categorization"
    )
    importance: Optional[int] = Field(
        default=None, ge=0, le=100, description="Importance score (0-100)"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional metadata"
    )

    @field_validator("content")
    @classmethod
    def validate_content(cls, v: Optional[str]) -> Optional[str]:
        """Validate memory content."""
        if v is not None and not v.strip():
            raise ValueError("Memory content cannot be empty")
        return v.strip() if v else None


class LongTermMemoryResponse(LongTermMemoryBase, BaseResponseSchema):
    """Schema for long-term memory API responses."""

    agent_id: int = Field(..., description="ID of the agent")
    embeddings: Optional[List[float]] = Field(
        default=None, description="Vector embeddings"
    )
    access_count: int = Field(default=0, description="Number of accesses")


class LongTermMemoryListResponse(BaseSchema):
    """Schema for listing long-term memories."""

    memories: List[LongTermMemoryResponse] = Field(
        default_factory=list, description="List of long-term memories"
    )
    total: int = Field(..., description="Total number of memories")


# Memory search schemas


class MemorySearchQuery(BaseSchema):
    """Schema for searching memories."""

    query: str = Field(..., min_length=1, description="Search query")
    knowledge_types: Optional[List[str]] = Field(
        default=None, description="Filter by knowledge types"
    )
    tags: Optional[List[str]] = Field(default=None, description="Filter by tags")
    min_importance: Optional[int] = Field(
        default=None, ge=0, le=100, description="Minimum importance score"
    )
    limit: int = Field(default=10, ge=1, le=100, description="Maximum results")


class MemorySearchResult(BaseSchema):
    """Schema for memory search results."""

    memory: LongTermMemoryResponse = Field(..., description="Memory object")
    relevance_score: float = Field(..., description="Relevance score (0-1)")


class MemorySearchResponse(BaseSchema):
    """Schema for memory search response."""

    results: List[MemorySearchResult] = Field(
        default_factory=list, description="Search results"
    )
    total: int = Field(..., description="Total number of results")