"""Abstract interface for repositories."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class Repository(ABC, Generic[ModelType]):
    """Abstract interface for repository layer operations."""

    @abstractmethod
    async def create(self, db: AsyncSession, data: Dict[str, Any]) -> ModelType:
        """Create a new entity in the database.

        Args:
            db: Database session
            data: Entity data dictionary

        Returns:
            ModelType: Created entity

        Raises:
            RepositoryError: If creation fails
        """
        pass

    @abstractmethod
    async def get(self, db: AsyncSession, entity_id: int) -> Optional[ModelType]:
        """Get an entity by ID.

        Args:
            db: Database session
            entity_id: Entity identifier

        Returns:
            Optional[ModelType]: Entity if found, None otherwise
        """
        pass

    @abstractmethod
    async def get_multi(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[ModelType]:
        """Get multiple entities with pagination and filters.

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            filters: Optional filter criteria

        Returns:
            List[ModelType]: List of entities
        """
        pass

    @abstractmethod
    async def update(
        self, db: AsyncSession, entity_id: int, data: Dict[str, Any]
    ) -> Optional[ModelType]:
        """Update an entity.

        Args:
            db: Database session
            entity_id: Entity identifier
            data: Update data dictionary

        Returns:
            Optional[ModelType]: Updated entity if found, None otherwise

        Raises:
            RepositoryError: If update fails
        """
        pass

    @abstractmethod
    async def delete(self, db: AsyncSession, entity_id: int) -> bool:
        """Delete an entity.

        Args:
            db: Database session
            entity_id: Entity identifier

        Returns:
            bool: True if deleted, False if not found

        Raises:
            RepositoryError: If deletion fails
        """
        pass

    @abstractmethod
    async def count(
        self, db: AsyncSession, filters: Optional[Dict[str, Any]] = None
    ) -> int:
        """Count entities with optional filters.

        Args:
            db: Database session
            filters: Optional filter criteria

        Returns:
            int: Number of entities
        """
        pass

    @abstractmethod
    async def exists(self, db: AsyncSession, entity_id: int) -> bool:
        """Check if an entity exists.

        Args:
            db: Database session
            entity_id: Entity identifier

        Returns:
            bool: True if exists, False otherwise
        """
        pass

    @abstractmethod
    async def get_by_field(
        self, db: AsyncSession, field: str, value: Any
    ) -> Optional[ModelType]:
        """Get an entity by a specific field value.

        Args:
            db: Database session
            field: Field name
            value: Field value

        Returns:
            Optional[ModelType]: Entity if found, None otherwise
        """
        pass

    @abstractmethod
    async def get_multi_by_field(
        self, db: AsyncSession, field: str, value: Any
    ) -> List[ModelType]:
        """Get multiple entities by a specific field value.

        Args:
            db: Database session
            field: Field name
            value: Field value

        Returns:
            List[ModelType]: List of entities
        """
        pass


class TransactionalRepository(ABC):
    """Abstract interface for transactional repository operations."""

    @abstractmethod
    async def begin_transaction(self, db: AsyncSession) -> None:
        """Begin a database transaction.

        Args:
            db: Database session

        Raises:
            RepositoryError: If transaction fails to begin
        """
        pass

    @abstractmethod
    async def commit_transaction(self, db: AsyncSession) -> None:
        """Commit a database transaction.

        Args:
            db: Database session

        Raises:
            RepositoryError: If commit fails
        """
        pass

    @abstractmethod
    async def rollback_transaction(self, db: AsyncSession) -> None:
        """Rollback a database transaction.

        Args:
            db: Database session

        Raises:
            RepositoryError: If rollback fails
        """
        pass