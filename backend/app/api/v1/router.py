# FEATURE: API
# Main router for API v1.

from fastapi import APIRouter
from app.api.v1.endpoints import health, agents, tasks, messages, llamacpp, p2p

router = APIRouter()

router.include_router(health.router, prefix="/health", tags=["health"])
router.include_router(agents.router, prefix="/agents", tags=["agents"])
router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
router.include_router(messages.router, prefix="/messages", tags=["messages"])
router.include_router(llamacpp.router, prefix="/llamacpp", tags=["llamacpp"])
router.include_router(p2p.router, prefix="/p2p", tags=["p2p"])
