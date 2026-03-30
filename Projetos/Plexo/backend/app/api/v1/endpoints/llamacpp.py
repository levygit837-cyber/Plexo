"""
LLama.cpp API Endpoints

Provides REST API for llama.cpp inference service.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/llamacpp", tags=["llamacpp"])


class ChatRequest(BaseModel):
    """Chat completion request."""

    messages: list[dict[str, str]]
    max_tokens: Optional[int] = 4096
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.9
    top_k: Optional[int] = 40
    stop: Optional[list[str]] = None
    stream: Optional[bool] = False


class CompletionRequest(BaseModel):
    """Text completion request."""

    prompt: str
    max_tokens: Optional[int] = 4096
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.9
    top_k: Optional[int] = 40
    stop: Optional[list[str]] = None
    stream: Optional[bool] = False


@router.get("/health")
async def health_check():
    """Check llama.cpp service health."""
    from backend.app.llamacpp.service import get_llamacpp_service

    try:
        service = await get_llamacpp_service()
        status = await service.get_status()
        return {"status": "ok" if status.get("healthy") else "error", **status}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")


@router.post("/chat")
async def chat_completion(request: ChatRequest):
    """Chat completion endpoint."""
    from backend.app.llamacpp.service import get_llamacpp_service

    try:
        service = await get_llamacpp_service()
        response = await service.chat(
            messages=request.messages,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            top_p=request.top_p,
            top_k=request.top_k,
            stop=request.stop,
        )
        return {
            "choices": [{"message": {"role": "assistant", "content": response}}]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/completions")
async def text_completion(request: CompletionRequest):
    """Text completion endpoint."""
    from backend.app.llamacpp.service import get_llamacpp_service

    try:
        service = await get_llamacpp_service()
        response = await service.generate(
            prompt=request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            top_p=request.top_p,
            top_k=request.top_k,
            stop=request.stop,
        )
        return {"choices": [{"text": response}]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_status():
    """Get detailed service status."""
    from backend.app.llamacpp.service import get_llamacpp_service

    try:
        service = await get_llamacpp_service()
        return await service.get_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))