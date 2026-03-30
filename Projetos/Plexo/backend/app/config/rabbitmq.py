"""
RabbitMQ configuration for async message queuing.

This module provides RabbitMQ connection management and channel pooling
for task queues and inter-service communication.
"""

from typing import Optional

import aio_pika
from aio_pika import Connection, Channel, ExchangeType
from aio_pika.pool import Pool

from .settings import get_settings


# Global connection and channel pools
_connection_pool: Optional[Pool] = None
_channel_pool: Optional[Pool] = None


async def get_connection() -> Connection:
    """
    Create a new RabbitMQ connection.
    
    Returns:
        aio_pika Connection instance
    """
    settings = get_settings()
    return await aio_pika.connect_robust(
        settings.rabbitmq_url,
        timeout=settings.rabbitmq_connection_timeout,
    )


async def get_channel() -> Channel:
    """
    Get a channel from an existing connection.
    
    Returns:
        aio_pika Channel instance
    """
    connection_pool = await get_connection_pool()
    async with connection_pool.acquire() as connection:
        return await connection.channel()


async def get_connection_pool() -> Pool:
    """
    Get or create the connection pool.
    
    Returns:
        Connection pool instance
    """
    global _connection_pool
    if _connection_pool is None:
        settings = get_settings()
        _connection_pool = Pool(
            get_connection,
            max_size=settings.rabbitmq_pool_size,
        )
    return _connection_pool


async def get_channel_pool() -> Pool:
    """
    Get or create the channel pool.
    
    Returns:
        Channel pool instance
    """
    global _channel_pool
    if _channel_pool is None:
        settings = get_settings()
        
        async def get_channel_from_pool():
            connection_pool = await get_connection_pool()
            async with connection_pool.acquire() as connection:
                return await connection.channel()
        
        _channel_pool = Pool(
            get_channel_from_pool,
            max_size=settings.rabbitmq_pool_size * 2,
        )
    return _channel_pool


async def init_rabbitmq() -> None:
    """
    Initialize RabbitMQ exchanges and queues.
    
    This creates the necessary exchanges and queues for the application.
    """
    channel_pool = await get_channel_pool()
    
    async with channel_pool.acquire() as channel:
        # Declare exchanges
        await channel.declare_exchange(
            "plexo.tasks",
            ExchangeType.TOPIC,
            durable=True,
        )
        
        await channel.declare_exchange(
            "plexo.agents",
            ExchangeType.TOPIC,
            durable=True,
        )
        
        await channel.declare_exchange(
            "plexo.events",
            ExchangeType.FANOUT,
            durable=True,
        )
        
        # Declare queues
        await channel.declare_queue(
            "plexo.tasks.high_priority",
            durable=True,
            arguments={"x-max-priority": 10},
        )
        
        await channel.declare_queue(
            "plexo.tasks.normal_priority",
            durable=True,
            arguments={"x-max-priority": 5},
        )
        
        await channel.declare_queue(
            "plexo.tasks.low_priority",
            durable=True,
            arguments={"x-max-priority": 1},
        )
        
        await channel.declare_queue(
            "plexo.agents.messages",
            durable=True,
        )
        
        await channel.declare_queue(
            "plexo.agents.commands",
            durable=True,
        )
        
        # Bind queues to exchanges
        tasks_exchange = await channel.get_exchange("plexo.tasks")
        
        high_priority_queue = await channel.get_queue("plexo.tasks.high_priority")
        await high_priority_queue.bind(tasks_exchange, routing_key="task.high.*")
        
        normal_priority_queue = await channel.get_queue("plexo.tasks.normal_priority")
        await normal_priority_queue.bind(tasks_exchange, routing_key="task.normal.*")
        
        low_priority_queue = await channel.get_queue("plexo.tasks.low_priority")
        await low_priority_queue.bind(tasks_exchange, routing_key="task.low.*")
        
        agents_exchange = await channel.get_exchange("plexo.agents")
        
        messages_queue = await channel.get_queue("plexo.agents.messages")
        await messages_queue.bind(agents_exchange, routing_key="agent.message.*")
        
        commands_queue = await channel.get_queue("plexo.agents.commands")
        await commands_queue.bind(agents_exchange, routing_key="agent.command.*")


async def close_rabbitmq() -> None:
    """
    Close RabbitMQ connections and cleanup resources.
    
    This should be called during application shutdown.
    """
    global _connection_pool, _channel_pool
    
    if _channel_pool is not None:
        await _channel_pool.close()
        _channel_pool = None
    
    if _connection_pool is not None:
        await _connection_pool.close()
        _connection_pool = None


async def publish_message(
    exchange: str,
    routing_key: str,
    message: bytes,
    priority: int = 0,
) -> None:
    """
    Publish a message to RabbitMQ.
    
    Args:
        exchange: Exchange name
        routing_key: Routing key for the message
        message: Message body as bytes
        priority: Message priority (0-10)
    """
    channel_pool = await get_channel_pool()
    
    async with channel_pool.acquire() as channel:
        exchange_obj = await channel.get_exchange(exchange)
        
        await exchange_obj.publish(
            aio_pika.Message(
                body=message,
                priority=priority,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key=routing_key,
        )


async def consume_queue(
    queue_name: str,
    callback,
    prefetch_count: int = 10,
) -> None:
    """
    Start consuming messages from a queue.
    
    Args:
        queue_name: Name of the queue to consume
        callback: Async callback function to process messages
        prefetch_count: Number of messages to prefetch
    """
    channel_pool = await get_channel_pool()
    
    async with channel_pool.acquire() as channel:
        await channel.set_qos(prefetch_count=prefetch_count)
        
        queue = await channel.get_queue(queue_name)
        
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    await callback(message)