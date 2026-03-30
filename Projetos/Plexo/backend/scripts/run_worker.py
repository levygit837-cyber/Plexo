#!/usr/bin/env python3
# Worker execution script for Plexo system.
"""
Start RabbitMQ workers for processing tasks and agent operations.
"""

import asyncio
import sys
import signal
from pathlib import Path
from typing import Optional
import argparse

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config.settings import get_settings
from app.core.logging import get_logger, setup_logging
from app.workers.task_worker import start_task_worker
from app.workers.agent_worker import start_agent_worker

logger = get_logger(__name__)


class WorkerManager:
    """Manage worker lifecycle and graceful shutdown."""
    
    def __init__(self):
        self.workers = []
        self.shutdown_event = asyncio.Event()
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        logger.info(f"Received signal {signum}, initiating graceful shutdown...")
        self.shutdown_event.set()
    
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown."""
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    async def start_worker(self, worker_type: str, queue_name: str, prefetch_count: int):
        """Start a specific worker type."""
        logger.info(f"Starting {worker_type} worker on queue '{queue_name}'...")
        
        try:
            if worker_type == "task":
                await start_task_worker(queue_name, prefetch_count)
            elif worker_type == "agent":
                await start_agent_worker(queue_name, prefetch_count)
            else:
                raise ValueError(f"Unknown worker type: {worker_type}")
                
        except Exception as e:
            logger.error(f"Worker {worker_type} failed: {e}")
            raise
    
    async def run(self, worker_type: str, queue_name: str, prefetch_count: int):
        """Run worker with graceful shutdown support."""
        self.setup_signal_handlers()
        
        worker_task = asyncio.create_task(
            self.start_worker(worker_type, queue_name, prefetch_count)
        )
        
        self.workers.append(worker_task)
        
        await self.shutdown_event.wait()
        
        logger.info("Stopping workers...")
        
        for worker in self.workers:
            worker.cancel()
        
        await asyncio.gather(*self.workers, return_exceptions=True)
        
        logger.info("All workers stopped")


async def main():
    """Main worker execution function."""
    parser = argparse.ArgumentParser(description="Run Plexo workers")
    parser.add_argument(
        "--type",
        choices=["task", "agent", "all"],
        default="all",
        help="Worker type to run (default: all)"
    )
    parser.add_argument(
        "--queue",
        type=str,
        help="Queue name (default: based on worker type)"
    )
    parser.add_argument(
        "--prefetch",
        type=int,
        default=10,
        help="Prefetch count for worker (default: 10)"
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level (default: INFO)"
    )
    
    args = parser.parse_args()
    
    setup_logging(level=args.log_level)
    settings = get_settings()
    
    logger.info("Starting Plexo workers...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Worker type: {args.type}")
    logger.info(f"Prefetch count: {args.prefetch}")
    
    manager = WorkerManager()
    
    try:
        if args.type == "all":
            logger.info("Starting all workers...")
            
            task_queue = args.queue or "tasks"
            agent_queue = args.queue or "agents"
            
            task_worker = asyncio.create_task(
                manager.start_worker("task", task_queue, args.prefetch)
            )
            agent_worker = asyncio.create_task(
                manager.start_worker("agent", agent_queue, args.prefetch)
            )
            
            manager.workers.extend([task_worker, agent_worker])
            
            manager.setup_signal_handlers()
            await manager.shutdown_event.wait()
            
            logger.info("Stopping all workers...")
            
            for worker in manager.workers:
                worker.cancel()
            
            await asyncio.gather(*manager.workers, return_exceptions=True)
            
        else:
            queue_name = args.queue or ("tasks" if args.type == "task" else "agents")
            await manager.run(args.type, queue_name, args.prefetch)
        
        logger.info("Workers shutdown completed")
        return 0
        
    except Exception as e:
        logger.error(f"Worker execution failed: {e}")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
