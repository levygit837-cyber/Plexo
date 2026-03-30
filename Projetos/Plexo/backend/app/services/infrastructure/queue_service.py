"""Queue service for managing RabbitMQ connections and message operations."""

from typing import Any, Callable, Optional
from aio_pika import connect_robust, Message, ExchangeType
from aio_pika.abc import AbstractConnection, AbstractChannel, AbstractQueue, AbstractExchange
from app.config.settings import get_settings
from app.core.logging.logger import get_logger
import json

logger = get_logger(__name__)


class QueueService:
    """Service for managing queue operations with RabbitMQ."""

    def __init__(self):
        """Initialize queue service."""
        self.settings = get_settings()
        self.connection: Optional[AbstractConnection] = None
        self.channel: Optional[AbstractChannel] = None
        self.exchanges: dict[str, AbstractExchange] = {}
        self.queues: dict[str, AbstractQueue] = {}

    async def initialize(self) -> None:
        """Initialize RabbitMQ connection and channel."""
        try:
            self.connection = await connect_robust(
                self.settings.RABBITMQ_URL,
                timeout=10,
            )
            self.channel = await self.connection.channel()
            await self.channel.set_qos(prefetch_count=10)
            logger.info("Queue service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize queue service: {e}")
            raise

    async def close(self) -> None:
        """Close RabbitMQ connections."""
        if self.channel:
            await self.channel.close()
        if self.connection:
            await self.connection.close()
        logger.info("Queue connections closed")

    async def declare_exchange(
        self,
        name: str,
        exchange_type: ExchangeType = ExchangeType.DIRECT,
        durable: bool = True,
    ) -> AbstractExchange:
        """Declare an exchange.
        
        Args:
            name: Exchange name
            exchange_type: Type of exchange
            durable: Whether exchange survives broker restart
            
        Returns:
            Declared exchange
        """
        if name in self.exchanges:
            return self.exchanges[name]
        
        exchange = await self.channel.declare_exchange(
            name,
            exchange_type,
            durable=durable,
        )
        self.exchanges[name] = exchange
        logger.info(f"Exchange '{name}' declared")
        return exchange

    async def declare_queue(
        self,
        name: str,
        durable: bool = True,
        exclusive: bool = False,
    ) -> AbstractQueue:
        """Declare a queue.
        
        Args:
            name: Queue name
            durable: Whether queue survives broker restart
            exclusive: Whether queue is exclusive to this connection
            
        Returns:
            Declared queue
        """
        if name in self.queues:
            return self.queues[name]
        
        queue = await self.channel.declare_queue(
            name,
            durable=durable,
            exclusive=exclusive,
        )
        self.queues[name] = queue
        logger.info(f"Queue '{name}' declared")
        return queue

    async def bind_queue(
        self,
        queue_name: str,
        exchange_name: str,
        routing_key: str = "",
    ) -> None:
        """Bind queue to exchange.
        
        Args:
            queue_name: Queue name
            exchange_name: Exchange name
            routing_key: Routing key for binding
        """
        queue = self.queues.get(queue_name)
        exchange = self.exchanges.get(exchange_name)
        
        if not queue or not exchange:
            raise ValueError("Queue or exchange not declared")
        
        await queue.bind(exchange, routing_key=routing_key)
        logger.info(f"Queue '{queue_name}' bound to exchange '{exchange_name}'")

    async def publish(
        self,
        exchange_name: str,
        routing_key: str,
        message: Any,
        priority: int = 0,
    ) -> None:
        """Publish message to exchange.
        
        Args:
            exchange_name: Exchange name
            routing_key: Routing key
            message: Message payload
            priority: Message priority (0-9)
        """
        try:
            exchange = self.exchanges.get(exchange_name)
            if not exchange:
                raise ValueError(f"Exchange '{exchange_name}' not declared")
            
            body = json.dumps(message).encode()
            msg = Message(
                body=body,
                priority=priority,
                content_type="application/json",
            )
            
            await exchange.publish(msg, routing_key=routing_key)
            logger.debug(f"Message published to '{exchange_name}' with key '{routing_key}'")
        except Exception as e:
            logger.error(f"Failed to publish message: {e}")
            raise

    async def consume(
        self,
        queue_name: str,
        callback: Callable,
        auto_ack: bool = False,
    ) -> None:
        """Start consuming messages from queue.
        
        Args:
            queue_name: Queue name
            callback: Callback function to process messages
            auto_ack: Whether to auto-acknowledge messages
        """
        try:
            queue = self.queues.get(queue_name)
            if not queue:
                raise ValueError(f"Queue '{queue_name}' not declared")
            
            async def process_message(message):
                async with message.process(ignore_processed=auto_ack):
                    try:
                        body = json.loads(message.body.decode())
                        await callback(body)
                    except Exception as e:
                        logger.error(f"Error processing message: {e}")
                        raise
            
            await queue.consume(process_message)
            logger.info(f"Started consuming from queue '{queue_name}'")
        except Exception as e:
            logger.error(f"Failed to start consumer: {e}")
            raise

    async def health_check(self) -> bool:
        """Check queue health.
        
        Returns:
            True if queue is healthy
        """
        try:
            if not self.connection or self.connection.is_closed:
                return False
            return True
        except Exception as e:
            logger.error(f"Queue health check failed: {e}")
            return False


# Global queue service instance
_queue_service: Optional[QueueService] = None


def get_queue_service() -> QueueService:
    """Get global queue service instance.
    
    Returns:
        QueueService: Queue service instance
    """
    global _queue_service
    if _queue_service is None:
        _queue_service = QueueService()
    return _queue_service