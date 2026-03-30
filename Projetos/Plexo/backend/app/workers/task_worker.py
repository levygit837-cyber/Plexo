# Task worker for processing general system tasks.
# FEATURE: Task Processing

from typing import Any, Dict
import asyncio

from app.workers.base_worker import BaseWorker
from app.queues.tasks.background_tasks import BACKGROUND_TASK_HANDLERS
from app.core.logging import get_logger

logger = get_logger(__name__)


class TaskWorker(BaseWorker):
    """Worker for processing general system tasks."""
    
    def __init__(self, queue_name: str = "tasks", prefetch_count: int = 10):
        super().__init__(queue_name, prefetch_count)
        self._register_handlers()
    
    def _register_handlers(self) -> None:
        """Register all background task handlers."""
        for task_type, handler in BACKGROUND_TASK_HANDLERS.items():
            self.register_handler(task_type, handler)
        
        self._logger.info(
            f"Registered {len(BACKGROUND_TASK_HANDLERS)} task handlers",
            extra={"handler_count": len(BACKGROUND_TASK_HANDLERS)}
        )
    
    async def process_task(self, task: Dict[str, Any]) -> Any:
        """Process a general task."""
        task_type = task.get("type", "unknown")
        
        self._logger.info(
            f"Processing task of type '{task_type}'",
            extra={"task_type": task_type, "task_id": task.get("id")}
        )
        
        handler = BACKGROUND_TASK_HANDLERS.get(task_type)
        if handler:
            return await handler(task)
        
        self._logger.warning(
            f"No handler found for task type '{task_type}'",
            extra={"task_type": task_type}
        )
        
        return {
            "status": "skipped",
            "message": f"No handler for task type '{task_type}'",
            "task_type": task_type
        }


async def start_task_worker(queue_name: str = "tasks", prefetch_count: int = 10) -> None:
    """Start the task worker."""
    worker = TaskWorker(queue_name, prefetch_count)
    worker.setup_signal_handlers()
    
    logger.info(
        f"Starting task worker for queue '{queue_name}'",
        extra={"queue": queue_name, "prefetch_count": prefetch_count}
    )
    
    await worker.start()


if __name__ == "__main__":
    asyncio.run(start_task_worker())
