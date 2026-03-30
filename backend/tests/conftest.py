"""
Pytest configuration and shared fixtures for Plexo tests.
"""

import asyncio
import pytest
from typing import AsyncGenerator, Generator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock

from app.main import create_app
from app.models.base import Base
from app.config.settings import get_settings
from app.models.agent import Agent, AgentStatus, AgentType
from app.models.task import Task, TaskStatus, TaskPriority
from app.models.message import Message, MessageType, MessageStatus


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    """Create test database engine with SQLite in-memory."""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    await engine.dispose()


@pytest.fixture
async def test_db(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create test database session."""
    async_session = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest.fixture
def test_client() -> TestClient:
    """Create FastAPI test client."""
    app = create_app()
    return TestClient(app)


@pytest.fixture
def mock_settings():
    """Mock application settings."""
    settings = get_settings()
    settings.ENVIRONMENT = "test"
    settings.DATABASE_URL = "sqlite+aiosqlite:///:memory:"
    settings.REDIS_URL = "redis://localhost:6379/1"
    settings.RABBITMQ_URL = "amqp://guest:guest@localhost:5672/test"
    return settings


@pytest.fixture
def mock_agent() -> Agent:
    """Create mock agent for testing."""
    return Agent(
        id=1,
        name="test_agent",
        type=AgentType.WORKER,
        status=AgentStatus.IDLE,
        capabilities={"test": True},
        config={"test_mode": True},
    )


@pytest.fixture
def mock_task() -> Task:
    """Create mock task for testing."""
    return Task(
        id=1,
        name="test_task",
        status=TaskStatus.PENDING,
        priority=TaskPriority.MEDIUM,
        payload={"test": "data"},
        agent_id=1,
    )


@pytest.fixture
def mock_message() -> Message:
    """Create mock message for testing."""
    return Message(
        id=1,
        sender_id=1,
        receiver_id=2,
        content="test message",
        message_type=MessageType.DIRECT,
        status=MessageStatus.PENDING,
    )


@pytest.fixture
def mock_rabbitmq():
    """Mock RabbitMQ connection and channel."""
    mock_connection = AsyncMock()
    mock_channel = AsyncMock()
    mock_connection.channel.return_value = mock_channel
    return {"connection": mock_connection, "channel": mock_channel}


@pytest.fixture
def mock_redis():
    """Mock Redis client."""
    mock_client = MagicMock()
    mock_client.get = AsyncMock(return_value=None)
    mock_client.set = AsyncMock(return_value=True)
    mock_client.delete = AsyncMock(return_value=True)
    mock_client.exists = AsyncMock(return_value=False)
    return mock_client


@pytest.fixture
def mock_kuzu():
    """Mock KuzuDB connection."""
    mock_db = MagicMock()
    mock_conn = MagicMock()
    mock_db.get_connection.return_value = mock_conn
    return {"db": mock_db, "connection": mock_conn}


@pytest.fixture
async def sample_agents(test_db: AsyncSession) -> list[Agent]:
    """Create sample agents in test database."""
    agents = [
        Agent(
            name="coordinator",
            type=AgentType.COORDINATOR,
            status=AgentStatus.ACTIVE,
            capabilities={"coordinate": True, "manage": True},
            config={"max_workers": 10},
        ),
        Agent(
            name="worker_1",
            type=AgentType.WORKER,
            status=AgentStatus.IDLE,
            capabilities={"process": True},
            config={"timeout": 30},
        ),
        Agent(
            name="worker_2",
            type=AgentType.WORKER,
            status=AgentStatus.BUSY,
            capabilities={"process": True},
            config={"timeout": 30},
        ),
    ]
    
    for agent in agents:
        test_db.add(agent)
    
    await test_db.commit()
    
    for agent in agents:
        await test_db.refresh(agent)
    
    return agents


@pytest.fixture
async def sample_tasks(test_db: AsyncSession, sample_agents: list[Agent]) -> list[Task]:
    """Create sample tasks in test database."""
    tasks = [
        Task(
            name="task_1",
            status=TaskStatus.PENDING,
            priority=TaskPriority.HIGH,
            payload={"action": "process"},
            agent_id=sample_agents[1].id,
        ),
        Task(
            name="task_2",
            status=TaskStatus.RUNNING,
            priority=TaskPriority.MEDIUM,
            payload={"action": "analyze"},
            agent_id=sample_agents[2].id,
        ),
        Task(
            name="task_3",
            status=TaskStatus.COMPLETED,
            priority=TaskPriority.LOW,
            payload={"action": "report"},
            result={"status": "success"},
            agent_id=sample_agents[1].id,
        ),
    ]
    
    for task in tasks:
        test_db.add(task)
    
    await test_db.commit()
    
    for task in tasks:
        await test_db.refresh(task)
    
    return tasks


@pytest.fixture
async def sample_messages(test_db: AsyncSession, sample_agents: list[Agent]) -> list[Message]:
    """Create sample messages in test database."""
    messages = [
        Message(
            sender_id=sample_agents[0].id,
            receiver_id=sample_agents[1].id,
            content="Start processing",
            message_type=MessageType.DIRECT,
            status=MessageStatus.DELIVERED,
        ),
        Message(
            sender_id=sample_agents[1].id,
            receiver_id=sample_agents[0].id,
            content="Processing started",
            message_type=MessageType.DIRECT,
            status=MessageStatus.READ,
        ),
        Message(
            sender_id=sample_agents[0].id,
            receiver_id=None,
            content="System announcement",
            message_type=MessageType.BROADCAST,
            status=MessageStatus.SENT,
        ),
    ]
    
    for message in messages:
        test_db.add(message)
    
    await test_db.commit()
    
    for message in messages:
        await test_db.refresh(message)
    
    return messages
