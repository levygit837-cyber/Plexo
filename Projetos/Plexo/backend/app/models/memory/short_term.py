"""Short-term memory model for agents."""

from typing import Dict, Any, Optional
from datetime import datetime, timedelta

from sqlalchemy import JSON, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class ShortTermMemory(BaseModel):
    """Short-term memory model for agent session context.

    Attributes:
        agent_id: ID of the agent this memory belongs to
        session_id: Unique session identifier
        context: Session context data
        ttl: Time-to-live in seconds
        expires_at: Expiration timestamp
        metadata: Additional metadata
    """

    __tablename__ = "short_term_memory"

    agent_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("agents.id", ondelete="CASCADE"), nullable=False, index=True
    )
    session_id: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    context: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    ttl: Mapped[int] = mapped_column(
        Integer, nullable=False, default=3600
    )  # Default 1 hour
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    metadata: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True, default=dict)

    # Relationships
    # agent: Mapped["Agent"] = relationship("Agent", back_populates="short_term_memories")

    def __repr__(self) -> str:
        """String representation of the short-term memory."""
        return f"ShortTermMemory(id={self.id}, agent_id={self.agent_id}, session_id={self.session_id!r})"

    def is_expired(self) -> bool:
        """Check if memory has expired.

        Returns:
            bool: True if memory has expired, False otherwise
        """
        return datetime.utcnow() >= self.expires_at

    def extend_ttl(self, additional_seconds: int) -> None:
        """Extend the time-to-live of the memory.

        Args:
            additional_seconds: Number of seconds to add to TTL
        """
        self.ttl += additional_seconds
        self.expires_at = datetime.utcnow() + timedelta(seconds=self.ttl)

    def refresh(self) -> None:
        """Refresh the memory expiration time based on current TTL."""
        self.expires_at = datetime.utcnow() + timedelta(seconds=self.ttl)

    def get_context_value(self, key: str, default: Any = None) -> Any:
        """Get a value from the context dictionary.

        Args:
            key: Context key
            default: Default value if key not found

        Returns:
            Any: Context value or default
        """
        return self.context.get(key, default)

    def set_context_value(self, key: str, value: Any) -> None:
        """Set a value in the context dictionary.

        Args:
            key: Context key
            value: Value to set
        """
        self.context[key] = value

    def clear_context(self) -> None:
        """Clear all context data."""
        self.context = {}