"""
LLama.cpp Inference Service

High-level service for LLM inference via llama-server.
Integrates with Plexo agent system for local LLM capabilities.
"""

import logging
from typing import Optional, AsyncIterator

from .config import get_llamacpp_config
from .client import (
    LlamaCppClient,
    ChatCompletionRequest,
    ChatMessage,
    CompletionRequest,
    get_llamacpp_client,
)
from .launcher import get_llamacpp_launcher

logger = logging.getLogger(__name__)


class LlamaCppService:
    """Service for LLM inference via llama.cpp server."""

    def __init__(self):
        self.config = get_llamacpp_config()
        self.launcher = get_llamacpp_launcher()
        self._client: Optional[LlamaCppClient] = None

    async def initialize(self) -> bool:
        """Initialize the inference service."""
        logger.info("Initializing llama.cpp inference service...")

        # Start the llama-server
        success = await self.launcher.start()
        if not success:
            logger.error("Failed to start llama-server")
            return False

        # Get client
        self._client = await get_llamacpp_client()

        # Verify health
        healthy = await self._client.health_check()
        if not healthy:
            logger.error("llama-server is not healthy")
            return False

        logger.info("llama.cpp inference service initialized successfully")
        return True

    async def shutdown(self) -> None:
        """Shutdown the inference service."""
        logger.info("Shutting down llama.cpp inference service...")

        if self._client:
            await self._client.close()

        await self.launcher.stop()
        logger.info("llama.cpp inference service shut down")

    async def generate(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        top_k: Optional[int] = None,
        repeat_penalty: Optional[float] = None,
        stop: Optional[list[str]] = None,
    ) -> str:
        """Generate text completion."""
        if not self._client:
            raise RuntimeError("Service not initialized")

        request = CompletionRequest(
            prompt=prompt,
            max_tokens=max_tokens or self.config.max_tokens,
            temperature=temperature or self.config.temperature,
            top_p=top_p or self.config.top_p,
            top_k=top_k or self.config.top_k,
            repeat_penalty=repeat_penalty or self.config.repeat_penalty,
            stop=stop,
            stream=False,
        )

        result = await self._client.completion(request)
        return result.get("choices", [{}])[0].get("text", "")

    async def chat(
        self,
        messages: list[dict[str, str]],
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        top_k: Optional[int] = None,
        repeat_penalty: Optional[float] = None,
        stop: Optional[list[str]] = None,
    ) -> str:
        """Chat completion."""
        if not self._client:
            raise RuntimeError("Service not initialized")

        chat_messages = [
            ChatMessage(role=msg["role"], content=msg["content"]) for msg in messages
        ]

        request = ChatCompletionRequest(
            messages=chat_messages,
            max_tokens=max_tokens or self.config.max_tokens,
            temperature=temperature or self.config.temperature,
            top_p=top_p or self.config.top_p,
            top_k=top_k or self.config.top_k,
            repeat_penalty=repeat_penalty or self.config.repeat_penalty,
            stop=stop,
            stream=False,
        )

        result = await self._client.chat_completion(request)
        return result.get("choices", [{}])[0].get("message", {}).get("content", "")

    async def chat_stream(
        self,
        messages: list[dict[str, str]],
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        top_k: Optional[int] = None,
        repeat_penalty: Optional[float] = None,
        stop: Optional[list[str]] = None,
    ) -> AsyncIterator[str]:
        """Stream chat completion."""
        if not self._client:
            raise RuntimeError("Service not initialized")

        chat_messages = [
            ChatMessage(role=msg["role"], content=msg["content"]) for msg in messages
        ]

        request = ChatCompletionRequest(
            messages=chat_messages,
            max_tokens=max_tokens or self.config.max_tokens,
            temperature=temperature or self.config.temperature,
            top_p=top_p or self.config.top_p,
            top_k=top_k or self.config.top_k,
            repeat_penalty=repeat_penalty or self.config.repeat_penalty,
            stop=stop,
            stream=True,
        )

        async for chunk in self._client.chat_completion_stream(request):
            yield chunk

    async def get_status(self) -> dict:
        """Get service status."""
        launcher_status = await self.launcher.get_status()

        health = False
        if self._client:
            health = await self._client.health_check()

        return {
            **launcher_status,
            "healthy": health,
            "api_url": self.config.api_base_url,
            "model_path": self.config.model_path,
        }


_service: Optional[LlamaCppService] = None


async def get_llamacpp_service() -> LlamaCppService:
    """Get or create the singleton service."""
    global _service
    if _service is None:
        _service = LlamaCppService()
    return _service