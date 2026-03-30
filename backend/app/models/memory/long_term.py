"""Long-term memory model for agents."""

from typing import Dict, Any, Optional, List

from sqlalchemy import JSON, String, Integer, ForeignKey, Text, ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class LongTermMemory(BaseModel):
    """Long-term memory model for agent persistent knowledge.

    Attributes:
        agent_id: ID of the agent this memory belongs to
        knowledge_type: Type of knowledge (fact, procedure, experience, etc.)
        content: Memory content
        embeddings: Vector embeddings for semantic search
        tags: Tags for categorization
        importance: Importance score (0-100)
        access_count: Number of times this memory has been accessed
        metadata: Additional metadata
    """

    __tablename__ = "long_term_memory"

    agent_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("agents.id", ondelete="CASCADE"), nullable=False, index=True
    )
    knowledge_type: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    embeddings: Mapped[Optional[List[float]]] = mapped_column(
        ARRAY(float), nullable=True
    )
    tags: Mapped[List[str]] = mapped_column(
        ARRAY(String), nullable=False, default=list
    )
    importance: Mapped[int] = mapped_column(
        Integer, nullable=False, default=50
    )  # 0-100 scale
    access_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    metadata: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True, default=dict)

    # Relationships
    # agent: Mapped["Agent"] = relationship("Agent", back_populates="long_term_memories")

    def __repr__(self) -> str:
        """String representation of the long-term memory."""
        return f"LongTermMemory(id={self.id}, agent_id={self.agent_id}, type={self.knowledge_type!r})"

    def increment_access(self) -> None:
        """Increment the access count."""
        self.access_count += 1

    def is_important(self, threshold: int = 70) -> bool:
        """Check if memory is important based on threshold.

        Args:
            threshold: Importance threshold (default: 70)

        Returns:
            bool: True if importance >= threshold, False otherwise
        """
        return self.importance >= threshold

    def has_tag(self, tag: str) -> bool:
        """Check if memory has a specific tag.

        Args:
            tag: Tag to check

        Returns:
            bool: True if tag exists, False otherwise
        """
        return tag in self.tags

    def add_tag(self, tag: str) -> None:
        """Add a tag to the memory.

        Args:
            tag: Tag to add
        """
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the memory.

        Args:
            tag: Tag to remove
        """
        if tag in self.tags:
            self.tags.remove(tag)

    def update_importance(self, new_importance: int) -> None:
        """Update the importance score.

        Args:
            new_importance: New importance score (0-100)

        Raises:
            ValueError: If importance is not in valid range
        """
        if not 0 <= new_importance <= 100:
            raise ValueError("Importance must be between 0 and 100")
        self.importance = new_importance

    def get_metadata_value(self, key: str, default: Any = None) -> Any:
        """Get a value from the metadata dictionary.

        Args:
            key: Metadata key
            default: Default value if key not found

        Returns:
            Any: Metadata value or default
        """
        return self.metadata.get(key, default)

    def set_metadata_value(self, key: str, value: Any) -> None:
        """Set a value in the metadata dictionary.

        Args:
            key: Metadata key
            value: Value to set
        """
        self.metadata[key] = value