"""Base model for all SQLAlchemy models."""

from datetime import datetime
from typing import Any, Dict, Self

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    pass


class BaseModel(Base):
    """Base model with common fields for all models."""

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert model instance to dictionary.

        Returns:
            Dict[str, Any]: Dictionary representation of the model
        """
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        """Create model instance from dictionary.

        Args:
            data: Dictionary with model data

        Returns:
            Self: New model instance
        """
        return cls(**data)

    def __repr__(self) -> str:
        """String representation of the model."""
        class_name = self.__class__.__name__
        attrs = ", ".join(
            f"{key}={value!r}"
            for key, value in self.to_dict().items()
            if key != "updated_at"
        )
        return f"{class_name}({attrs})"