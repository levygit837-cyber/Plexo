# Message handling behavior for SPADE agents.
# FEATURE: Multi-Agent Communication

from typing import Optional, Dict, Any, Callable
import asyncio
from datetime import datetime

from spade.message import Message
from spade.template import Template

from app.core.logging import get_logger
from app.core.errors import AgentCommunicationError
from .base_behavior import BaseBehavior


logger = get_logger(__name__)


class MessageBehavior(BaseBehavior):
    """
    Behavior for handling incoming messages.
    
    Listens for messages matching a template and processes them
    using registered handlers.
    """

    def __init__(
        self,
        template: Optional[Template] = None,
        timeout: Optional[float] = None,
    ):
        """
        Initialize MessageBehavior.
        
        Args:
            template: Optional message template to match
            timeout: Optional timeout in seconds for receiving messages
        """
        super().__init__()
        self._template = template
        self._timeout = timeout
        self._message_handlers: Dict[str, Callable] = {}
        self._received_count = 0
        self._processed_count = 0
        self._failed_count = 0

    async def execute(self) -> None:
        """
        Execute message receiving and processing.
        """
        msg = await self.receive(timeout=self._timeout)
        
        if msg:
            self._received_count += 1
            await self.process_message(msg)

    async def process_message(self, message: Message) -> None:
        """
        Process received message.
        
        Args:
            message: Received SPADE message
        """
        try:
            sender = str(message.sender)
            content = message.body
            metadata = message.metadata if hasattr(message, 'metadata') else {}
            
            self._logger.debug(
                f"Processing message from {sender}",
                extra={
                    "agent_jid": str(self.agent.jid),
                    "sender": sender,
                    "content_length": len(content)
                }
            )
            
            message_type = metadata.get("type", "default")
            
            if message_type in self._message_handlers:
                await self._message_handlers[message_type](message)
            else:
                await self.on_message(message)
            
            self._processed_count += 1
            
        except Exception as e:
            self._failed_count += 1
            self._logger.error(
                f"Failed to process message: {e}",
                extra={
                    "agent_jid": str(self.agent.jid),
                    "sender": str(message.sender)
                }
            )
            raise AgentCommunicationError(
                message=f"Failed to process message in {self.agent.jid}",
                details={"error": str(e), "sender": str(message.sender)}
            )

    async def on_message(self, message: Message) -> None:
        """
        Default message handler.
        
        Override this method to implement custom message handling.
        
        Args:
            message: Received SPADE message
        """
        self._logger.info(
            f"Received message: {message.body[:100]}",
            extra={"agent_jid": str(self.agent.jid)}
        )

    def register_handler(self, message_type: str, handler: Callable) -> None:
        """
        Register message handler for specific message type.
        
        Args:
            message_type: Type of message to handle
            handler: Async callable to handle message
        """
        self._message_handlers[message_type] = handler
        self._logger.debug(
            f"Registered handler for message type: {message_type}",
            extra={"agent_jid": str(self.agent.jid)}
        )

    def get_stats(self) -> Dict[str, Any]:
        """
        Get message behavior statistics.
        
        Returns:
            Dictionary with message stats
        """
        base_stats = super().get_stats()
        return {
            **base_stats,
            "received_count": self._received_count,
            "processed_count": self._processed_count,
            "failed_count": self._failed_count,
            "success_rate": (
                self._processed_count / self._received_count
                if self._received_count > 0
                else 0.0
            ),
        }


class BroadcastBehavior(BaseBehavior):
    """
    Behavior for broadcasting messages to multiple agents.
    """

    def __init__(self, recipients: list[str], interval: float = 60.0):
        """
        Initialize BroadcastBehavior.
        
        Args:
            recipients: List of recipient JIDs
            interval: Interval in seconds between broadcasts
        """
        super().__init__(period=interval)
        self._recipients = recipients
        self._broadcast_count = 0

    async def execute(self) -> None:
        """
        Execute broadcast.
        """
        message_content = await self.prepare_broadcast()
        
        if message_content:
            await self.broadcast(message_content)

    async def prepare_broadcast(self) -> Optional[str]:
        """
        Prepare broadcast message content.
        
        Override this method to customize broadcast content.
        
        Returns:
            Message content to broadcast, or None to skip
        """
        return None

    async def broadcast(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Broadcast message to all recipients.
        
        Args:
            content: Message content
            metadata: Optional message metadata
        """
        self._broadcast_count += 1
        
        for recipient in self._recipients:
            try:
                msg = Message(to=recipient)
                msg.body = content
                
                if metadata:
                    msg.metadata = metadata
                
                msg.set_metadata("sender_id", str(self.agent.jid))
                msg.set_metadata("timestamp", datetime.utcnow().isoformat())
                msg.set_metadata("broadcast_id", str(self._broadcast_count))
                
                await self.send(msg)
                
                self._logger.debug(
                    f"Broadcast sent to {recipient}",
                    extra={
                        "agent_jid": str(self.agent.jid),
                        "recipient": recipient,
                        "broadcast_id": self._broadcast_count
                    }
                )
                
            except Exception as e:
                self._logger.error(
                    f"Failed to broadcast to {recipient}: {e}",
                    extra={"agent_jid": str(self.agent.jid), "recipient": recipient}
                )

    def get_stats(self) -> Dict[str, Any]:
        """
        Get broadcast behavior statistics.
        
        Returns:
            Dictionary with broadcast stats
        """
        base_stats = super().get_stats()
        return {
            **base_stats,
            "broadcast_count": self._broadcast_count,
            "recipients_count": len(self._recipients),
        }
