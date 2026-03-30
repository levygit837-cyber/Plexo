"""
LLama.cpp Server Launcher

Manages the lifecycle of the llama-server process.
Provides start, stop, restart, and health monitoring.
"""

import asyncio
import logging
import os
import signal
import subprocess
from pathlib import Path
from typing import Optional

from .config import get_llamacpp_config

logger = logging.getLogger(__name__)


class LlamaServerLauncher:
    """Manages the llama-server process lifecycle."""

    def __init__(self):
        self.config = get_llamacpp_config()
        self._process: Optional[subprocess.Popen] = None
        self._monitor_task: Optional[asyncio.Task] = None
        self._running = False

    @property
    def is_running(self) -> bool:
        """Check if the server process is running."""
        if self._process is None:
            return False
        return self._process.poll() is None

    async def start(self) -> bool:
        """Start the llama-server process."""
        if self.is_running:
            logger.info("llama-server is already running")
            return True

        binary_path = Path(self.config.binary_path)
        if not binary_path.exists():
            logger.error(f"llama-server binary not found: {binary_path}")
            return False

        model_path = Path(self.config.model_path)
        if not model_path.exists():
            logger.error(f"Model file not found: {model_path}")
            return False

        args = self.config.get_server_args()
        logger.info(f"Starting llama-server: {' '.join(args)}")

        try:
            self._process = subprocess.Popen(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid if os.name != "nt" else None,
            )

            ready = await self._wait_for_ready(timeout=120)

            if ready:
                self._running = True
                self._monitor_task = asyncio.create_task(self._monitor_process())
                logger.info(
                    f"llama-server started on {self.config.server_host}:{self.config.server_port}"
                )
                return True
            else:
                logger.error("llama-server failed to start within timeout")
                await self.stop()
                return False

        except Exception as e:
            logger.error(f"Failed to start llama-server: {e}")
            return False

    async def stop(self) -> None:
        """Stop the llama-server process."""
        self._running = False

        if self._monitor_task:
            self._monitor_task.cancel()
            try:
                await self._monitor_task
            except asyncio.CancelledError:
                pass

        if self._process and self.is_running:
            logger.info("Stopping llama-server...")
            try:
                if os.name != "nt":
                    os.killpg(os.getpgid(self._process.pid), signal.SIGTERM)
                else:
                    self._process.terminate()

                try:
                    await asyncio.wait_for(
                        asyncio.to_thread(self._process.wait), timeout=30
                    )
                except asyncio.TimeoutError:
                    logger.warning("Force killing llama-server...")
                    if os.name != "nt":
                        os.killpg(os.getpgid(self._process.pid), signal.SIGKILL)
                    else:
                        self._process.kill()

            except Exception as e:
                logger.error(f"Error stopping llama-server: {e}")

        self._process = None
        logger.info("llama-server stopped")

    async def restart(self) -> bool:
        """Restart the llama-server process."""
        logger.info("Restarting llama-server...")
        await self.stop()
        await asyncio.sleep(2)
        return await self.start()

    async def _wait_for_ready(self, timeout: int = 120) -> bool:
        """Wait for the server to be ready."""
        import httpx

        start_time = asyncio.get_event_loop().time()
        health_url = self.config.health_url

        while (asyncio.get_event_loop().time() - start_time) < timeout:
            if self._process and self._process.poll() is not None:
                stdout = self._process.stdout.read().decode() if self._process.stdout else ""
                stderr = self._process.stderr.read().decode() if self._process.stderr else ""
                logger.error(f"llama-server exited: stdout={stdout}, stderr={stderr}")
                return False

            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(health_url, timeout=5)
                    if response.status_code == 200:
                        return True
            except Exception:
                pass

            await asyncio.sleep(2)

        return False

    async def _monitor_process(self) -> None:
        """Monitor the server process and log output."""
        if not self._process:
            return

        while self._running and self.is_running:
            if self._process.stderr:
                line = self._process.stderr.readline()
                if line:
                    logger.debug(f"llama-server: {line.decode().strip()}")
            await asyncio.sleep(0.1)

    async def get_status(self) -> dict:
        """Get server status information."""
        return {
            "running": self.is_running,
            "pid": self._process.pid if self._process else None,
            "host": self.config.server_host,
            "port": self.config.server_port,
            "model": Path(self.config.model_path).name,
            "ctx_size": self.config.ctx_size,
            "gpu_layers": self.config.n_gpu_layers,
        }


_launcher: Optional[LlamaServerLauncher] = None


def get_llamacpp_launcher() -> LlamaServerLauncher:
    """Get or create the singleton launcher."""
    global _launcher
    if _launcher is None:
        _launcher = LlamaServerLauncher()
    return _launcher