"""
RabbitMQ producer for publishing messages to queues.
"""

from typing import Any, Dict, Optional
import json
import asyncio
from aio_pika import Message, DeliveryMode
from aio_pika.abc import AbstractChannel

from app.config.rabbitmq import get_channel
from app.core.logging import get_logger
from app.core.errors.base import PlexoException

logger = get_logger(__name__)


class ProducerError(PlexoException):
    """Exception raised when producer operations fail."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details)


class QueueProducer:
    """Producer for publishing messages to RabbitMQ queues."""
    
    def __init__(self):
        self._channel: Optional[AbstractChannel] = None
        self._logger = get_logger(__name__)
    
    async def connect(self) -> None:
        """Establish connection to RabbitMQ."""
        try:
            self._channel = await get_channel()
            self._logger.info("Producer connected to RabbitMQ")
        except Exception as e:
            self._logger.error(f"Failed to connect producer: {e}")
            raise ProducerError(f"Failed to connect to RabbitMQ: {e}")
    
    async def disconnect(self) -> None:
        """Close connection to RabbitMQ."""
        if self._channel and not self._channel.is_closed:
            await self._channel.close()
            self._logger.info("Producer disconnected from RabbitMQ")
    
    async def publish(
        self,
        queue_name: str,
        message: Dict[str, Any],
        priority: int = 5,
        persistent: bool = True,
        expiration: Optional[int] = None
    ) -> None:
        """Publish a message to a queue."""
        if not self._channel:
            await self.connect()
        
        try:
            message_body = json.dumps(message).encode()
            
            delivery_mode = DeliveryMode.PERSISTENT if persistent else DeliveryMode.NOT_PERSISTENT
            
            aio_message = Message(
                body=message_body,
                delivery_mode=delivery_mode,
                priority=priority,
                expiration=expiration
            )
            
            await self._channel.default_exchange.publish(
                aio_message,
                routing_key=queue_name
            )
            
            self._logger.debug(
                f"Published message to queue '{queue_name}'",
                extra={"queue": queue_name, "priority": priority}
            )
        
        except Exception as e:
            self._logger.error(
                f"Failed to publish message to queue '{queue_name}': {e}",
                extra={"queue": queue_name, "error": str(e)}
            )
            raise ProducerError(
                f"Failed to publish message to queue '{queue_name}'",
                details={"queue": queue_name, "error": str(e)}
            )
    
    async def publish_batch(
        self,
        queue_name: str,
        messages: list[Dict[str, Any]],
        priority: int = 5,
        persistent: bool = True
    ) -> None:
        """Publish multiple messages to a queue."""
        if not self._channel:
            await self.connect()
        
        try:
            tasks = [
                self.publish(queue_name, msg, priority, persistent)
                for msg in messages
            ]
            await asyncio.gather(*tasks)
            
            self._logger.info(
                f"Published {len(messages)} messages to queue '{queue_name}'",
                extra={"queue": queue_name, "count": len(messages)}
            )
        
        except Exception as e:
            self._logger.error(
                f"Failed to publish batch to queue '{queue_name}': {e}",
                extra={"queue": queue_name, "error": str(e)}
            )
            raise ProducerError(
                f"Failed to publish batch to queue '{queue_name}'",
                details={"queue": queue_name, "error": str(e)}
            )


_producer_instance: Optional[QueueProducer] = None


def get_producer() -> QueueProducer:
    """Get singleton producer instance."""
    global _producer_instance
    if _producer_instance is None:
        _producer_instance = QueueProducer()
    return _producer_instance


async def publish_task(
    queue: str,
    task: Dict[str, Any],
    priority: int = 5
) -> None:
    """Publish a task to a queue."""
    producer = get_producer()
    await producer.publish(queue, task, priority=priority)
