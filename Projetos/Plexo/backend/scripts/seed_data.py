#!/usr/bin/env python3
# Database seeding script for Plexo system.
"""
Seed database with initial data for development and testing.
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession
from app.config.database import get_session_factory
from app.config.settings import get_settings
from app.core.logging import get_logger, setup_logging
from app.models.agent import Agent, AgentStatus, AgentType
from app.models.task import Task, TaskStatus, TaskPriority
from app.models.message import Message, MessageType, MessageStatus
from app.models.memory.short_term import ShortTermMemory
from app.models.memory.long_term import LongTermMemory

logger = get_logger(__name__)


async def seed_agents(session: AsyncSession) -> list[Agent]:
    """Seed initial agents."""
    logger.info("Seeding agents...")
    
    agents = [
        Agent(
            name="coordinator",
            type=AgentType.COORDINATOR,
            status=AgentStatus.ACTIVE,
            capabilities={"coordinate": True, "manage": True, "delegate": True},
            config={"max_workers": 10, "timeout": 60},
        ),
        Agent(
            name="worker_1",
            type=AgentType.WORKER,
            status=AgentStatus.IDLE,
            capabilities={"process": True, "analyze": True},
            config={"timeout": 30, "max_retries": 3},
        ),
        Agent(
            name="worker_2",
            type=AgentType.WORKER,
            status=AgentStatus.IDLE,
            capabilities={"process": True, "transform": True},
            config={"timeout": 30, "max_retries": 3},
        ),
        Agent(
            name="monitor",
            type=AgentType.MONITOR,
            status=AgentStatus.ACTIVE,
            capabilities={"monitor": True, "alert": True, "report": True},
            config={"check_interval": 10, "alert_threshold": 0.8},
        ),
    ]
    
    for agent in agents:
        session.add(agent)
    
    await session.commit()
    
    for agent in agents:
        await session.refresh(agent)
    
    logger.info(f"Seeded {len(agents)} agents")
    return agents


async def seed_tasks(session: AsyncSession, agents: list[Agent]) -> list[Task]:
    """Seed initial tasks."""
    logger.info("Seeding tasks...")
    
    tasks = [
        Task(
            name="process_data_batch_1",
            status=TaskStatus.PENDING,
            priority=TaskPriority.HIGH,
            payload={"batch_id": 1, "records": 1000, "action": "process"},
            agent_id=agents[1].id,
        ),
        Task(
            name="analyze_metrics",
            status=TaskStatus.PENDING,
            priority=TaskPriority.MEDIUM,
            payload={"metric_type": "performance", "period": "daily"},
            agent_id=agents[1].id,
        ),
        Task(
            name="transform_dataset",
            status=TaskStatus.RUNNING,
            priority=TaskPriority.MEDIUM,
            payload={"dataset_id": "ds_001", "format": "json"},
            agent_id=agents[2].id,
        ),
        Task(
            name="generate_report",
            status=TaskStatus.COMPLETED,
            priority=TaskPriority.LOW,
            payload={"report_type": "summary", "period": "weekly"},
            result={"status": "success", "file": "report_2026_03.pdf"},
            agent_id=agents[3].id,
        ),
    ]
    
    for task in tasks:
        session.add(task)
    
    await session.commit()
    
    for task in tasks:
        await session.refresh(task)
    
    logger.info(f"Seeded {len(tasks)} tasks")
    return tasks


async def seed_messages(session: AsyncSession, agents: list[Agent]) -> list[Message]:
    """Seed initial messages."""
    logger.info("Seeding messages...")
    
    messages = [
        Message(
            sender_id=agents[0].id,
            receiver_id=agents[1].id,
            content="Start processing batch 1",
            message_type=MessageType.DIRECT,
            status=MessageStatus.DELIVERED,
        ),
        Message(
            sender_id=agents[1].id,
            receiver_id=agents[0].id,
            content="Batch 1 processing started",
            message_type=MessageType.DIRECT,
            status=MessageStatus.READ,
        ),
        Message(
            sender_id=agents[0].id,
            receiver_id=None,
            content="System maintenance scheduled for tonight",
            message_type=MessageType.BROADCAST,
            status=MessageStatus.SENT,
        ),
        Message(
            sender_id=agents[3].id,
            receiver_id=agents[0].id,
            content="Weekly report generated successfully",
            message_type=MessageType.DIRECT,
            status=MessageStatus.DELIVERED,
        ),
    ]
    
    for message in messages:
        session.add(message)
    
    await session.commit()
    
    for message in messages:
        await session.refresh(message)
    
    logger.info(f"Seeded {len(messages)} messages")
    return messages


async def seed_memory(session: AsyncSession, agents: list[Agent]):
    """Seed initial memory data."""
    logger.info("Seeding memory data...")
    
    short_term_memories = [
        ShortTermMemory(
            agent_id=agents[0].id,
            session_id="session_001",
            context={"current_task": "coordination", "active_workers": 2},
            ttl=3600,
        ),
        ShortTermMemory(
            agent_id=agents[1].id,
            session_id="session_002",
            context={"current_batch": 1, "processed_records": 450},
            ttl=1800,
        ),
    ]
    
    long_term_memories = [
        LongTermMemory(
            agent_id=agents[0].id,
            content="Coordination strategy: delegate tasks based on worker capabilities",
            knowledge={"strategy": "capability_based", "success_rate": 0.95},
            importance=90,
            tags=["strategy", "coordination"],
        ),
        LongTermMemory(
            agent_id=agents[1].id,
            content="Processing optimization: batch size 1000 yields best performance",
            knowledge={"optimal_batch_size": 1000, "avg_time": 45.2},
            importance=85,
            tags=["optimization", "performance"],
        ),
    ]
    
    for memory in short_term_memories:
        session.add(memory)
    
    for memory in long_term_memories:
        session.add(memory)
    
    await session.commit()
    
    logger.info(f"Seeded {len(short_term_memories)} short-term and {len(long_term_memories)} long-term memories")


async def clear_existing_data(session: AsyncSession):
    """Clear existing data from database."""
    logger.info("Clearing existing data...")
    
    try:
        await session.execute("DELETE FROM short_term_memory")
        await session.execute("DELETE FROM long_term_memory")
        await session.execute("DELETE FROM messages")
        await session.execute("DELETE FROM tasks")
        await session.execute("DELETE FROM agents")
        await session.commit()
        
        logger.info("Existing data cleared")
        
    except Exception as e:
        logger.error(f"Failed to clear existing data: {e}")
        await session.rollback()
        raise


async def main():
    """Main seeding function."""
    setup_logging()
    settings = get_settings()
    
    logger.info("Starting database seeding...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    
    try:
        session_factory = get_session_factory()
        
        async with session_factory() as session:
            await clear_existing_data(session)
            
            agents = await seed_agents(session)
            tasks = await seed_tasks(session, agents)
            messages = await seed_messages(session, agents)
            await seed_memory(session, agents)
        
        logger.info("Database seeding completed successfully")
        return 0
        
    except Exception as e:
        logger.error(f"Database seeding failed: {e}")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
