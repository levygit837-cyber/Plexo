# RabbitMQ consumer for consuming messages from queues.
# Handles message processing with acknowledgment and error handling.

from typing import Any, Callable, Dict, Optional
import json
import asyncio
from aio_pika import IncomingMessage
from aio_pika.abc import AbstractChannel, AbstractQueue

from app.config.rabbitmq import get_channel
from app.core.logging import get_logger
from app.core.errors.base import PlexoException

logger = get_logger(__name__)


class ConsumerError(PlexoException):
    """Exception raised when consumer operations fail."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details)


class QueueConsumer:
    """Consumer for consuming messages from RabbitMQ queues."""
    
    def __init__(self, queue_name: str, prefetch_count: int = 10):
        self._queue_name = queue_name
        self._prefetch_count = prefetch_count
        self._channel: Optional[AbstractChannel] = None
        self._queue: Optional[AbstractQueue] = None
        self._logger = get_logger(__name__)
        self._handlers: Dict[str, Callable] = {}
        self._is_consuming = False
    
    async def connect(self) -> None:
        """Establish connection to RabbitMQ and declare queue."""
        try:
            self._channel = await get_channel()
            await self._channel.set_qos(prefetch_count=self._prefetch_count)
            
            self._queue = await self._channel.declare_queue(
                self._queue_name,
                durable=True
            )
            
            self._logger.info(
                f"Consumer connected to queue '{self._queue_name}'",
                extra={"queue": self._queue_name}
            )
        
        except Exception as e:
            self._logger.error(f"Failed to connect consumer: {e}")
            raise ConsumerError(f"Failed to connect to RabbitMQ: {e}")
    
    async def disconnect(self) -> None:
        """Close connection to RabbitMQ."""
        self._is_consuming = False
        
        if self._channel and not self._channel.is_closed:
            await self._channel.close()
            self._logger.info(
                f"Consumer disconnected from queue '{self._queue_name}'",
                extra={"queue": self._queue_name}
            )
    
    def register_handler(self, message_type: str, handler: Callable) -> None:
        """Register a handler for a specific message type."""
        self._handlers[message_type] = handler
        self._logger.debug(
            f"Registered handler for message type '{message_type}'",
            extra={"message_type": message_type}
        )
    
    async def _process_message(self, message: IncomingMessage) -> None:
        """Process a single message."""
        async with message.process():
            try:
                body = json.loads(message.body.decode())
                message_type = body.get("type", "default")
                
                self._logger.debug(
                    f"Processing message of type '{message_type}'",
                    extra={"message_type": message_type, "queue": self._queue_name}
                )
                
                handler = self._handlers.get(message_type)
                if handler:
                    await handler(body)
                else:
                    self._logger.warning(
                        f"No handler registered for message type '{message_type}'",
                        extra={"message_type": message_type}
                    )
                
                await message.ack()
                
            except json.JSONDecodeError as e:
                self._logger.error(
                    f"Failed to decode message: {e}",
                    extra={"error": str(e)}
                )
                await message.reject(requeue=False)
            
            except Exception as e:
                self._logger.error(
                    f"Failed to process message: {e}",
                    extra={"error": str(e)}
                )
                await message.reject(requeue=True)
    
    async def start_consuming(self) -> None:
        """Start consuming messages from the queue."""
        if not self._channel or not self._queue:
            await self.connect()
        
        self._is_consuming = True
        
        try:
            self._logger.info(
                f"Started consuming from queue '{self._queue_name}'",
                extra={"queue": self._queue_name}
            )
            
            await self._queue.consume(self._process_message)
            
            while self._is_consuming:
                await asyncio.sleep(1)
        
        except Exception as e:
            self._logger.error(
                f"Error while consuming from queue '{self._queue_name}': {e}",
                extra={"queue": self._queue_name, "error": str(e)}
            )
            raise ConsumerError(
                f"Failed to consume from queue '{self._queue_name}'",
                details={"queue": self._queue_name, "error": str(e)}
            )
    
    async def stop_consuming(self) -> None:
        """Stop consuming messages."""
        self._is_consuming = False
        self._logger.info(
            f"Stopped consuming from queue '{self._queue_name}'",
            extra={"queue": self._queue_name}
        )


def create_consumer(queue_name: str, prefetch_count: int = 10) -> QueueConsumer:
    """Create a new consumer instance."""
    return QueueConsumer(queue_name, prefetch_count)
