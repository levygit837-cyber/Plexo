"""Message endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.api.deps import get_message_service
from app.services.message_service import MessageService
from app.schemas.message import MessageCreate, MessageUpdate, MessageResponse
from app.core.logging.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_message(
    data: MessageCreate,
    service: MessageService = Depends(get_message_service)
):
    """Create a new message.
    
    Args:
        data: Message creation data
        service: Message service instance
        
    Returns:
        Created message
    """
    message = await service.create_message(data)
    return MessageResponse.model_validate(message)


@router.get("/{message_id}", response_model=MessageResponse)
async def get_message(
    message_id: int,
    service: MessageService = Depends(get_message_service)
):
    """Get message by ID.
    
    Args:
        message_id: Message ID
        service: Message service instance
        
    Returns:
        Message details
    """
    message = await service.get_message(message_id)
    return MessageResponse.model_validate(message)


@router.get("/", response_model=List[MessageResponse])
async def list_messages(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    sender_id: Optional[int] = None,
    receiver_id: Optional[int] = None,
    message_type: Optional[str] = None,
    service: MessageService = Depends(get_message_service)
):
    """List messages with optional filters.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        sender_id: Filter by sender ID
        receiver_id: Filter by receiver ID
        message_type: Filter by message type
        service: Message service instance
        
    Returns:
        List of messages
    """
    messages = await service.list_messages(
        skip=skip,
        limit=limit,
        sender_id=sender_id,
        receiver_id=receiver_id,
        message_type=message_type
    )
    return [MessageResponse.model_validate(message) for message in messages]


@router.get("/conversation/{agent1_id}/{agent2_id}", response_model=List[MessageResponse])
async def get_conversation(
    agent1_id: int,
    agent2_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: MessageService = Depends(get_message_service)
):
    """Get conversation between two agents.
    
    Args:
        agent1_id: First agent ID
        agent2_id: Second agent ID
        skip: Number of records to skip
        limit: Maximum number of records to return
        service: Message service instance
        
    Returns:
        List of messages in conversation
    """
    messages = await service.get_conversation(
        agent1_id=agent1_id,
        agent2_id=agent2_id,
        skip=skip,
        limit=limit
    )
    return [MessageResponse.model_validate(message) for message in messages]


@router.put("/{message_id}", response_model=MessageResponse)
async def update_message(
    message_id: int,
    data: MessageUpdate,
    service: MessageService = Depends(get_message_service)
):
    """Update message.
    
    Args:
        message_id: Message ID
        data: Update data
        service: Message service instance
        
    Returns:
        Updated message
    """
    message = await service.update_message(message_id, data)
    return MessageResponse.model_validate(message)


@router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(
    message_id: int,
    service: MessageService = Depends(get_message_service)
):
    """Delete message.
    
    Args:
        message_id: Message ID
        service: Message service instance
    """
    await service.delete_message(message_id)


@router.post("/{message_id}/read", response_model=MessageResponse)
async def mark_message_as_read(
    message_id: int,
    service: MessageService = Depends(get_message_service)
):
    """Mark message as read.
    
    Args:
        message_id: Message ID
        service: Message service instance
        
    Returns:
        Updated message
    """
    message = await service.mark_as_read(message_id)
    return MessageResponse.model_validate(message)