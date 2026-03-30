"""Message schemas for API requests and responses."""

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
from app.models.message import MessageType, MessageStatus


class MessageBase(BaseSchema):
    """Base message schema with common fields."""

    sender_jid: str = Field(..., max_length=255, description="Sender XMPP JID")
    receiver_jid: str = Field(..., max_length=255, description="Receiver XMPP JID")
    message_type: MessageType = Field(
        default=MessageType.REQUEST, description="Message type"
    )
    subject: Optional[str] = Field(
        default=None, max_length=255, description="Message subject"
    )
    content: str = Field(..., min_length=1, description="Message content")
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional metadata"
    )


class MessageCreate(MessageBase, BaseCreateSchema):
    """Schema for creating a new message."""

    sender_id: Optional[int] = Field(default=None, description="Sender agent ID")
    receiver_id: Optional[int] = Field(default=None, description="Receiver agent ID")
    parent_message_id: Optional[int] = Field(
        default=None, description="Parent message ID for threading"
    )

    @field_validator("content")
    @classmethod
    def validate_content(cls, v: str) -> str:
        """Validate message content."""
        if not v.strip():
            raise ValueError("Message content cannot be empty")
        return v.strip()


class MessageUpdate(BaseUpdateSchema):
    """Schema for updating a message."""

    status: Optional[MessageStatus] = Field(default=None, description="Message status")
    content: Optional[str] = Field(
        default=None, min_length=1, description="Message content"
    )
    subject: Optional[str] = Field(
        default=None, max_length=255, description="Message subject"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional metadata"
    )

    @field_validator("content")
    @classmethod
    def validate_content(cls, v: Optional[str]) -> Optional[str]:
        """Validate message content."""
        if v is not None and not v.strip():
            raise ValueError("Message content cannot be empty")
        return v.strip() if v else None


class MessageResponse(MessageBase, BaseResponseSchema):
    """Schema for message API responses."""

    status: MessageStatus = Field(..., description="Current message status")
    sender_id: Optional[int] = Field(default=None, description="Sender agent ID")
    receiver_id: Optional[int] = Field(default=None, description="Receiver agent ID")
    parent_message_id: Optional[int] = Field(
        default=None, description="Parent message ID"
    )
    delivered_at: Optional[datetime] = Field(
        default=None, description="Delivery timestamp"
    )
    read_at: Optional[datetime] = Field(default=None, description="Read timestamp")


class MessageListResponse(BaseSchema):
    """Schema for listing messages."""

    messages: list[MessageResponse] = Field(
        default_factory=list, description="List of messages"
    )
    total: int = Field(..., description="Total number of messages")


class MessageStatusUpdate(BaseSchema):
    """Schema for updating message status."""

    status: MessageStatus = Field(..., description="New message status")


class MessageThread(BaseSchema):
    """Schema for message thread."""

    parent_message: MessageResponse = Field(..., description="Parent message")
    replies: list[MessageResponse] = Field(
        default_factory=list, description="Reply messages"
    )
    total_replies: int = Field(..., description="Total number of replies")


class MessageSend(BaseSchema):
    """Schema for sending a message via XMPP."""

    to_jid: str = Field(..., max_length=255, description="Receiver XMPP JID")
    content: str = Field(..., min_length=1, description="Message content")
    subject: Optional[str] = Field(
        default=None, max_length=255, description="Message subject"
    )
    message_type: MessageType = Field(
        default=MessageType.REQUEST, description="Message type"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional metadata"
    )

    @field_validator("content")
    @classmethod
    def validate_content(cls, v: str) -> str:
        """Validate message content."""
        if not v.strip():
            raise ValueError("Message content cannot be empty")
        return v.strip()


class MessageBroadcast(BaseSchema):
    """Schema for broadcasting a message to multiple agents."""

    to_jids: list[str] = Field(..., min_length=1, description="List of receiver JIDs")
    content: str = Field(..., min_length=1, description="Message content")
    subject: Optional[str] = Field(
        default=None, max_length=255, description="Message subject"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional metadata"
    )

    @field_validator("content")
    @classmethod
    def validate_content(cls, v: str) -> str:
        """Validate message content."""
        if not v.strip():
            raise ValueError("Message content cannot be empty")
        return v.strip()