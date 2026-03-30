"""Message service for managing message business logic."""

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.message import Message
from app.schemas.message import MessageCreate, MessageUpdate, MessageResponse
from app.core.logging.logger import get_logger
from app.core.errors.api_errors import NotFoundError, ValidationError

logger = get_logger(__name__)


class MessageService:
    """Service layer for message operations."""

    def __init__(self, db: AsyncSession):
        """Initialize message service.
        
        Args:
            db: Database session
        """
        self.db = db

    async def create_message(self, data: MessageCreate) -> Message:
        """Create a new message.
        
        Args:
            data: Message creation data
            
        Returns:
            Created message
        """
        try:
            message = Message(
                sender_id=data.sender_id,
                receiver_id=data.receiver_id,
                content=data.content,
                message_type=data.message_type or "text",
                metadata=data.metadata or {},
            )
            self.db.add(message)
            await self.db.commit()
            await self.db.refresh(message)
            logger.info(f"Message created: {message.id}")
            return message
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Failed to create message: {e}")
            raise ValidationError(f"Failed to create message: {str(e)}")

    async def get_message(self, message_id: int) -> Message:
        """Get message by ID.
        
        Args:
            message_id: Message ID
            
        Returns:
            Message instance
            
        Raises:
            NotFoundError: If message not found
        """
        result = await self.db.execute(
            select(Message).where(Message.id == message_id)
        )
        message = result.scalar_one_or_none()
        
        if not message:
            raise NotFoundError(f"Message with id {message_id} not found")
        
        return message

    async def list_messages(
        self,
        skip: int = 0,
        limit: int = 100,
        sender_id: Optional[int] = None,
        receiver_id: Optional[int] = None,
        message_type: Optional[str] = None,
    ) -> List[Message]:
        """List messages with optional filters.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            sender_id: Filter by sender ID
            receiver_id: Filter by receiver ID
            message_type: Filter by message type
            
        Returns:
            List of messages
        """
        query = select(Message)
        
        if sender_id:
            query = query.where(Message.sender_id == sender_id)
        if receiver_id:
            query = query.where(Message.receiver_id == receiver_id)
        if message_type:
            query = query.where(Message.message_type == message_type)
        
        query = query.offset(skip).limit(limit).order_by(Message.created_at.desc())
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_conversation(
        self,
        agent1_id: int,
        agent2_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Message]:
        """Get conversation between two agents.
        
        Args:
            agent1_id: First agent ID
            agent2_id: Second agent ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of messages in conversation
        """
        query = select(Message).where(
            ((Message.sender_id == agent1_id) & (Message.receiver_id == agent2_id)) |
            ((Message.sender_id == agent2_id) & (Message.receiver_id == agent1_id))
        )
        
        query = query.offset(skip).limit(limit).order_by(Message.created_at.desc())
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def update_message(
        self,
        message_id: int,
        data: MessageUpdate,
    ) -> Message:
        """Update message.
        
        Args:
            message_id: Message ID
            data: Update data
            
        Returns:
            Updated message
        """
        message = await self.get_message(message_id)
        
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(message, field, value)
        
        try:
            await self.db.commit()
            await self.db.refresh(message)
            logger.info(f"Message updated: {message_id}")
            return message
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Failed to update message: {e}")
            raise ValidationError(f"Failed to update message: {str(e)}")

    async def delete_message(self, message_id: int) -> None:
        """Delete message.
        
        Args:
            message_id: Message ID
        """
        message = await self.get_message(message_id)
        
        try:
            await self.db.delete(message)
            await self.db.commit()
            logger.info(f"Message deleted: {message_id}")
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Failed to delete message: {e}")
            raise ValidationError(f"Failed to delete message: {str(e)}")

    async def mark_as_read(self, message_id: int) -> Message:
        """Mark message as read.
        
        Args:
            message_id: Message ID
            
        Returns:
            Updated message
        """
        message = await self.get_message(message_id)
        
        if message.metadata is None:
            message.metadata = {}
        message.metadata["read"] = True
        
        try:
            await self.db.commit()
            await self.db.refresh(message)
            logger.info(f"Message marked as read: {message_id}")
            return message
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Failed to mark message as read: {e}")
            raise ValidationError(f"Failed to mark message as read: {str(e)}")