"""Abstract interface for services."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, TypeVar

from app.schemas.base import BaseCreateSchema, BaseUpdateSchema, PaginationParams

T = TypeVar("T")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseCreateSchema)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseUpdateSchema)


class Service(ABC, Generic[T, CreateSchemaType, UpdateSchemaType]):
    """Abstract interface for service layer operations."""

    @abstractmethod
    async def create(self, data: CreateSchemaType) -> T:
        """Create a new entity.

        Args:
            data: Creation data schema

        Returns:
            T: Created entity

        Raises:
            ServiceError: If creation fails
        """
        pass

    @abstractmethod
    async def get(self, entity_id: int) -> Optional[T]:
        """Get an entity by ID.

        Args:
            entity_id: Entity identifier

        Returns:
            Optional[T]: Entity if found, None otherwise
        """
        pass

    @abstractmethod
    async def get_or_fail(self, entity_id: int) -> T:
        """Get an entity by ID or raise exception.

        Args:
            entity_id: Entity identifier

        Returns:
            T: Entity

        Raises:
            NotFoundError: If entity not found
        """
        pass

    @abstractmethod
    async def list(
        self,
        filters: Optional[Dict[str, Any]] = None,
        pagination: Optional[PaginationParams] = None,
    ) -> List[T]:
        """List entities with optional filters and pagination.

        Args:
            filters: Optional filter criteria
            pagination: Optional pagination parameters

        Returns:
            List[T]: List of entities
        """
        pass

    @abstractmethod
    async def update(self, entity_id: int, data: UpdateSchemaType) -> T:
        """Update an entity.

        Args:
            entity_id: Entity identifier
            data: Update data schema

        Returns:
            T: Updated entity

        Raises:
            NotFoundError: If entity not found
            ServiceError: If update fails
        """
        pass

    @abstractmethod
    async def delete(self, entity_id: int) -> bool:
        """Delete an entity.

        Args:
            entity_id: Entity identifier

        Returns:
            bool: True if deleted, False otherwise

        Raises:
            NotFoundError: If entity not found
            ServiceError: If deletion fails
        """
        pass

    @abstractmethod
    async def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count entities with optional filters.

        Args:
            filters: Optional filter criteria

        Returns:
            int: Number of entities
        """
        pass

    @abstractmethod
    async def exists(self, entity_id: int) -> bool:
        """Check if an entity exists.

        Args:
            entity_id: Entity identifier

        Returns:
            bool: True if exists, False otherwise
        """
        pass


class IAsyncService(ABC):
    """Abstract interface for asynchronous service operations."""

    @abstractmethod
    async def execute_async(self, task_data: Dict[str, Any]) -> str:
        """Execute an asynchronous task.

        Args:
            task_data: Task data dictionary

        Returns:
            str: Task ID for tracking

        Raises:
            ServiceError: If task submission fails
        """
        pass

    @abstractmethod
    async def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get the status of an asynchronous task.

        Args:
            task_id: Task identifier

        Returns:
            Dict[str, Any]: Task status information

        Raises:
            NotFoundError: If task not found
        """
        pass

    @abstractmethod
    async def cancel_task(self, task_id: str) -> bool:
        """Cancel an asynchronous task.

        Args:
            task_id: Task identifier

        Returns:
            bool: True if cancelled, False otherwise

        Raises:
            NotFoundError: If task not found
        """
        pass