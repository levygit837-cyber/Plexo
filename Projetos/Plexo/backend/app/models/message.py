"""Message model for database persistence."""

from typing import Dict, Any, Optional
from datetime import datetime

from sqlalchemy import JSON, String, Text, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
import enum

from app.models.base import BaseModel


class MessageType(str, enum.Enum):
    """Message type enumeration."""

    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"
    BROADCAST = "broadcast"
    ERROR = "error"


class MessageStatus(str, enum.Enum):
    """Message status enumeration."""

    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"


class Message(BaseModel):
    """Message model for database persistence.

    Attributes:
        sender_id: ID of the agent sending the message
        receiver_id: ID of the agent receiving the message
        sender_jid: XMPP JID of the sender
        receiver_jid: XMPP JID of the receiver
        message_type: Type of message
        status: Current message status
        subject: Message subject
        content: Message content
        metadata: Additional metadata
        parent_message_id: ID of parent message (for threading)
        delivered_at: Timestamp when message was delivered
        read_at: Timestamp when message was read
    """

    __tablename__ = "messages"

    sender_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("agents.id", ondelete="SET NULL"), nullable=True, index=True
    )
    receiver_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("agents.id", ondelete="SET NULL"), nullable=True, index=True
    )
    sender_jid: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    receiver_jid: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    message_type: Mapped[MessageType] = mapped_column(
        SQLEnum(MessageType), nullable=False, default=MessageType.REQUEST, index=True
    )
    status: Mapped[MessageStatus] = mapped_column(
        SQLEnum(MessageStatus), nullable=False, default=MessageStatus.PENDING, index=True
    )
    subject: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    metadata: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True, default=dict)
    parent_message_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("messages.id", ondelete="SET NULL"), nullable=True, index=True
    )
    delivered_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    read_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    # Relationships
    # sender: Mapped["Agent"] = relationship("Agent", foreign_keys=[sender_id])
    # receiver: Mapped["Agent"] = relationship("Agent", foreign_keys=[receiver_id])
    # parent_message: Mapped["Message"] = relationship("Message", remote_side=[id])

    def __repr__(self) -> str:
        """String representation of the message."""
        return f"Message(id={self.id}, type={self.message_type.value}, status={self.status.value}, from={self.sender_jid}, to={self.receiver_jid})"

    def is_pending(self) -> bool:
        """Check if message is pending.

        Returns:
            bool: True if message is pending, False otherwise
        """
        return self.status == MessageStatus.PENDING

    def is_sent(self) -> bool:
        """Check if message is sent.

        Returns:
            bool: True if message is sent, False otherwise
        """
        return self.status == MessageStatus.SENT

    def is_delivered(self) -> bool:
        """Check if message is delivered.

        Returns:
            bool: True if message is delivered, False otherwise
        """
        return self.status == MessageStatus.DELIVERED

    def is_read(self) -> bool:
        """Check if message is read.

        Returns:
            bool: True if message is read, False otherwise
        """
        return self.status == MessageStatus.READ

    def is_failed(self) -> bool:
        """Check if message has failed.

        Returns:
            bool: True if message has failed, False otherwise
        """
        return self.status == MessageStatus.FAILED

    def mark_as_sent(self) -> None:
        """Mark message as sent."""
        self.status = MessageStatus.SENT

    def mark_as_delivered(self) -> None:
        """Mark message as delivered."""
        self.status = MessageStatus.DELIVERED
        self.delivered_at = datetime.utcnow()

    def mark_as_read(self) -> None:
        """Mark message as read."""
        self.status = MessageStatus.READ
        self.read_at = datetime.utcnow()

    def mark_as_failed(self) -> None:
        """Mark message as failed."""
        self.status = MessageStatus.FAILED