"""Agent schemas for API requests and responses."""

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
from app.models.agent import AgentStatus, AgentType


class AgentBase(BaseSchema):
    """Base agent schema with common fields."""

    name: str = Field(..., min_length=1, max_length=255, description="Agent name")
    type: AgentType = Field(..., description="Agent type")
    capabilities: Dict[str, Any] = Field(
        default_factory=dict, description="Agent capabilities"
    )
    config: Dict[str, Any] = Field(
        default_factory=dict, description="Agent configuration"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional metadata"
    )


class AgentCreate(AgentBase, BaseCreateSchema):
    """Schema for creating a new agent."""

    jid: Optional[str] = Field(
        default=None, max_length=255, description="XMPP JID for SPADE communication"
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate agent name."""
        if not v.strip():
            raise ValueError("Agent name cannot be empty")
        return v.strip()


class AgentUpdate(BaseUpdateSchema):
    """Schema for updating an agent."""

    name: Optional[str] = Field(
        default=None, min_length=1, max_length=255, description="Agent name"
    )
    type: Optional[AgentType] = Field(default=None, description="Agent type")
    status: Optional[AgentStatus] = Field(default=None, description="Agent status")
    capabilities: Optional[Dict[str, Any]] = Field(
        default=None, description="Agent capabilities"
    )
    config: Optional[Dict[str, Any]] = Field(
        default=None, description="Agent configuration"
    )
    jid: Optional[str] = Field(
        default=None, max_length=255, description="XMPP JID for SPADE communication"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional metadata"
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        """Validate agent name."""
        if v is not None and not v.strip():
            raise ValueError("Agent name cannot be empty")
        return v.strip() if v else None


class AgentResponse(AgentBase, BaseResponseSchema):
    """Schema for agent API responses."""

    status: AgentStatus = Field(..., description="Current agent status")
    jid: Optional[str] = Field(default=None, description="XMPP JID")


class AgentListResponse(BaseSchema):
    """Schema for listing agents."""

    agents: list[AgentResponse] = Field(
        default_factory=list, description="List of agents"
    )
    total: int = Field(..., description="Total number of agents")


class AgentStatusUpdate(BaseSchema):
    """Schema for updating agent status."""

    status: AgentStatus = Field(..., description="New agent status")


class AgentCapabilityUpdate(BaseSchema):
    """Schema for updating agent capabilities."""

    capabilities: Dict[str, Any] = Field(..., description="Updated capabilities")


class AgentConfigUpdate(BaseSchema):
    """Schema for updating agent configuration."""

    config: Dict[str, Any] = Field(..., description="Updated configuration")