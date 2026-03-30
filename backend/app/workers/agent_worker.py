# Agent worker for processing agent-related tasks.
# FEATURE: Multi-Agent Communication

from typing import Any, Dict
import asyncio

from app.workers.base_worker import BaseWorker
from app.queues.tasks.agent_tasks import AGENT_TASK_HANDLERS
from app.core.logging import get_logger

logger = get_logger(__name__)


class AgentWorker(BaseWorker):
    """Worker for processing agent-related tasks."""
    
    def __init__(self, queue_name: str = "agents", prefetch_count: int = 10):
        super().__init__(queue_name, prefetch_count)
        self._register_handlers()
    
    def _register_handlers(self) -> None:
        """Register all agent task handlers."""
        for task_type, handler in AGENT_TASK_HANDLERS.items():
            self.register_handler(task_type, handler)
        
        self._logger.info(
            f"Registered {len(AGENT_TASK_HANDLERS)} agent task handlers",
            extra={"handler_count": len(AGENT_TASK_HANDLERS)}
        )
    
    async def process_task(self, task: Dict[str, Any]) -> Any:
        """Process an agent-related task."""
        task_type = task.get("type", "unknown")
        
        self._logger.info(
            f"Processing agent task of type '{task_type}'",
            extra={"task_type": task_type, "task_id": task.get("id")}
        )
        
        handler = AGENT_TASK_HANDLERS.get(task_type)
        if handler:
            return await handler(task)
        
        self._logger.warning(
            f"No handler found for agent task type '{task_type}'",
            extra={"task_type": task_type}
        )
        
        return {
            "status": "skipped",
            "message": f"No handler for agent task type '{task_type}'",
            "task_type": task_type
        }


async def start_agent_worker(queue_name: str = "agents", prefetch_count: int = 10) -> None:
    """Start the agent worker."""
    worker = AgentWorker(queue_name, prefetch_count)
    worker.setup_signal_handlers()
    
    logger.info(
        f"Starting agent worker for queue '{queue_name}'",
        extra={"queue": queue_name, "prefetch_count": prefetch_count}
    )
    
    await worker.start()


if __name__ == "__main__":
    asyncio.run(start_agent_worker())
