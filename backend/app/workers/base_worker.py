# Base worker class for processing tasks from RabbitMQ queues.
# FEATURE: Task Processing

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Callable
import asyncio
import signal
from app.queues.consumer import QueueConsumer
from app.core.logging import get_logger
from app.core.errors.base import PlexoException
from app.core.metrics import track_latency
import time

logger = get_logger(__name__)


class WorkerError(PlexoException):
    """Exception raised when worker operations fail."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details)


class BaseWorker(ABC):
    """Abstract base class for all workers."""
    
    def __init__(self, queue_name: str, prefetch_count: int = 10):
        self._queue_name = queue_name
        self._prefetch_count = prefetch_count
        self._consumer: Optional[QueueConsumer] = None
        self._logger = get_logger(__name__)
        self._is_running = False
        self._handlers: Dict[str, Callable] = {}
    
    @abstractmethod
    async def process_task(self, task: Dict[str, Any]) -> Any:
        """Process a single task. Must be implemented by subclasses."""
        pass
    
    def register_handler(self, task_type: str, handler: Callable) -> None:
        """Register a handler for a specific task type."""
        self._handlers[task_type] = handler
        self._logger.debug(
            f"Registered handler for task type '{task_type}'",
            extra={"task_type": task_type}
        )
    
    async def _handle_task(self, message: Dict[str, Any]) -> None:
        """Handle a task message from the queue."""
        start_time = time.time()
        task_type = message.get("type", "unknown")
        
        try:
            self._logger.info(
                f"Processing task of type '{task_type}'",
                extra={"task_type": task_type, "queue": self._queue_name}
            )
            
            handler = self._handlers.get(task_type)
            if handler:
                result = await handler(message)
                self._logger.info(
                    f"Task '{task_type}' completed successfully",
                    extra={"task_type": task_type, "result": result}
                )
            else:
                result = await self.process_task(message)
                self._logger.info(
                    f"Task '{task_type}' processed successfully",
                    extra={"task_type": task_type, "result": result}
                )
            
            duration = time.time() - start_time
            track_latency(f"worker.{self._queue_name}.{task_type}", duration)
        
        except Exception as e:
            duration = time.time() - start_time
            self._logger.error(
                f"Failed to process task '{task_type}': {e}",
                extra={"task_type": task_type, "error": str(e), "duration": duration}
            )
            raise WorkerError(
                f"Failed to process task '{task_type}'",
                details={"task_type": task_type, "error": str(e)}
            )
    
    async def start(self) -> None:
        """Start the worker."""
        if self._is_running:
            self._logger.warning(f"Worker for queue '{self._queue_name}' is already running")
            return
        
        try:
            self._consumer = QueueConsumer(self._queue_name, self._prefetch_count)
            await self._consumer.connect()
            
            for task_type, handler in self._handlers.items():
                self._consumer.register_handler(task_type, self._handle_task)
            
            self._is_running = True
            
            self._logger.info(
                f"Worker started for queue '{self._queue_name}'",
                extra={"queue": self._queue_name}
            )
            
            await self._consumer.start_consuming()
        
        except Exception as e:
            self._logger.error(
                f"Failed to start worker for queue '{self._queue_name}': {e}",
                extra={"queue": self._queue_name, "error": str(e)}
            )
            raise WorkerError(
                f"Failed to start worker for queue '{self._queue_name}'",
                details={"queue": self._queue_name, "error": str(e)}
            )
    
    async def stop(self) -> None:
        """Stop the worker."""
        if not self._is_running:
            self._logger.warning(f"Worker for queue '{self._queue_name}' is not running")
            return
        
        try:
            self._is_running = False
            
            if self._consumer:
                await self._consumer.stop_consuming()
                await self._consumer.disconnect()
            
            self._logger.info(
                f"Worker stopped for queue '{self._queue_name}'",
                extra={"queue": self._queue_name}
            )
        
        except Exception as e:
            self._logger.error(
                f"Failed to stop worker for queue '{self._queue_name}': {e}",
                extra={"queue": self._queue_name, "error": str(e)}
            )
            raise WorkerError(
                f"Failed to stop worker for queue '{self._queue_name}'",
                details={"queue": self._queue_name, "error": str(e)}
            )
    
    def setup_signal_handlers(self) -> None:
        """Setup signal handlers for graceful shutdown."""
        def signal_handler(signum, frame):
            self._logger.info(
                f"Received signal {signum}, shutting down worker",
                extra={"signal": signum}
            )
            asyncio.create_task(self.stop())
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
