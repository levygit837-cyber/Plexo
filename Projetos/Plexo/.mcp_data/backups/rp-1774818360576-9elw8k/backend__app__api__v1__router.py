"""Main router for API v1."""

from fastapi import APIRouter
from app.api.v1.endpoints import health, agents, tasks, messages, llamacpp

router = APIRouter()

# Include all endpoint routers
router.include_router(
    health.router,
    tags=["health"]
)

router.include_router(
    agents.router,
    prefix="/agents",
    tags=["agents"]
)

router.include_router(
    tasks.router,
    prefix="/tasks",
    tags=["tasks"]
)

router.include_router(
    messages.router,
    prefix="/messages",
    tags=["messages"]
)

router.include_router(
    llamacpp.router,
    prefix="/llamacpp",
    tags=["llamacpp"]
)
