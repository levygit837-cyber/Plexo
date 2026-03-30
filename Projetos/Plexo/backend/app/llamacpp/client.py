"""
LLama.cpp HTTP Client

OpenAI-compatible client for llama-server REST API.
Supports both chat completions and completions endpoints.
"""

import httpx
import json
import logging
from typing import AsyncIterator, Optional
from dataclasses import dataclass

from .config import get_llamacpp_config

logger = logging.getLogger(__name__)


@dataclass
class CompletionRequest:
    """Request for text completion."""

    prompt: str
    max_tokens: int = 4096
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 40
    repeat_penalty: float = 1.1
    stop: list[str] | None = None
    stream: bool = False


@dataclass
class ChatMessage:
    """Chat message structure."""

    role: str  # "system", "user", "assistant"
    content: str


@dataclass
class ChatCompletionRequest:
    """Request for chat completion."""

    messages: list[ChatMessage]
    max_tokens: int = 4096
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 40
    repeat_penalty: float = 1.1
    stop: list[str] | None = None
    stream: bool = False


class LlamaCppClient:
    """HTTP client for llama-server OpenAI-compatible API."""

    def __init__(self):
        self.config = get_llamacpp_config()
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create async HTTP client."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.config.api_base_url,
                timeout=httpx.Timeout(self.config.server_timeout),
                limits=httpx.Limits(
                    max_connections=self.config.parallel * 2,
                    max_keepalive_connections=self.config.parallel,
                ),
            )
        return self._client

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()

    async def health_check(self) -> bool:
        """Check if llama-server is healthy."""
        try:
            client = await self._get_client()
            response = await client.get(self.config.health_url)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False

    async def completion(self, request: CompletionRequest) -> dict:
        """Send a completion request to llama-server."""
        client = await self._get_client()

        payload = {
            "prompt": request.prompt,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "top_p": request.top_p,
            "top_k": request.top_k,
            "repeat_penalty": request.repeat_penalty,
            "stream": request.stream,
        }

        if request.stop:
            payload["stop"] = request.stop

        response = await client.post("/completions", json=payload)
        response.raise_for_status()
        return response.json()

    async def chat_completion(self, request: ChatCompletionRequest) -> dict:
        """Send a chat completion request to llama-server."""
        client = await self._get_client()

        messages = [
            {"role": msg.role, "content": msg.content} for msg in request.messages
        ]

        payload = {
            "messages": messages,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "top_p": request.top_p,
            "top_k": request.top_k,
            "repeat_penalty": request.repeat_penalty,
            "stream": request.stream,
        }

        if request.stop:
            payload["stop"] = request.stop

        response = await client.post("/chat/completions", json=payload)
        response.raise_for_status()
        return response.json()

    async def chat_completion_stream(
        self, request: ChatCompletionRequest
    ) -> AsyncIterator[str]:
        """Stream chat completion responses."""
        client = await self._get_client()

        messages = [
            {"role": msg.role, "content": msg.content} for msg in request.messages
        ]

        payload = {
            "messages": messages,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "top_p": request.top_p,
            "top_k": request.top_k,
            "repeat_penalty": request.repeat_penalty,
            "stream": True,
        }

        if request.stop:
            payload["stop"] = request.stop

        async with client.stream(
            "POST", "/chat/completions", json=payload
        ) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]
                    if data.strip() == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data)
                        if "choices" in chunk and len(chunk["choices"]) > 0:
                            delta = chunk["choices"][0].get("delta", {})
                            if "content" in delta:
                                yield delta["content"]
                    except json.JSONDecodeError:
                        continue

    async def get_model_info(self) -> dict:
        """Get model information from llama-server."""
        client = await self._get_client()
        response = await client.get("/models")
        response.raise_for_status()
        return response.json()


# Singleton client instance
_client: Optional[LlamaCppClient] = None


async def get_llamacpp_client() -> LlamaCppClient:
    """Get or create the singleton client."""
    global _client
    if _client is None:
        _client = LlamaCppClient()
    return _client