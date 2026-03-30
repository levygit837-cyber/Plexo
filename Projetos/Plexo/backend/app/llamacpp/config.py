"""
LLama.cpp Configuration for Plexo

Configures llama-server with TurboQuant CUDA for maximum performance.
Target: 128k context on RTX 4060 (8GB VRAM) with Qwen3.5-4B Q4_K_M.
"""

import os
from pathlib import Path
from pydantic import BaseModel
from typing import Optional


class LlamaCppConfig(BaseModel):
    """Configuration for llama-server instance."""

    # Model configuration
    model_path: str = os.getenv(
        "LLAMACPP_MODEL_PATH",
        str(
            Path.home()
            / ".lmstudio/models/Jackrong/Qwen3.5-4B-Claude-4.6-Opus-Reasoning-Distilled-v2-GGUF/Qwen3.5-4B.Q4_K_M.gguf"
        ),
    )

    # Server configuration
    server_host: str = os.getenv("LLAMACPP_HOST", "127.0.0.1")
    server_port: int = int(os.getenv("LLAMACPP_PORT", "8081"))
    server_timeout: int = int(os.getenv("LLAMACPP_TIMEOUT", "300"))

    # Binary path (compiled turbo3-cuda)
    binary_path: str = os.getenv(
        "LLAMACPP_BINARY_PATH",
        str(Path("/tmp/turbo3-cuda/build/bin/llama-server")),
    )

    # === MAXIMUM PERFORMANCE SETTINGS (RTX 4060 8GB) ===

    # Context size - TARGET 128K with TurboQuant KV cache compression
    ctx_size: int = int(os.getenv("LLAMACPP_CTX_SIZE", "131072"))  # 128k

    # GPU layers - ALL layers on GPU for maximum performance
    n_gpu_layers: int = int(os.getenv("LLAMACPP_GPU_LAYERS", "99"))

    # Batch size for prompt processing
    batch_size: int = int(os.getenv("LLAMACPP_BATCH_SIZE", "2048"))

    # Micro-batch size for generation
    ubatch_size: int = int(os.getenv("LLAMACPP_UBATCH_SIZE", "1024"))

    # CPU threads - MAXIMUM (use all available cores)
    threads: int = int(os.getenv("LLAMACPP_THREADS", str(os.cpu_count() or 8)))

    # Parallel sequences for concurrent requests
    parallel: int = int(os.getenv("LLAMACPP_PARALLEL", "4"))

    # === TURBOQUANT KV CACHE COMPRESSION ===

    # Enable TurboQuant for KV cache (3-bit PolarQuant)
    # This allows 128k context within 8GB VRAM
    flash_attn: bool = os.getenv("LLAMACPP_FLASH_ATTN", "true").lower() == "true"

    # === TOKEN EFFICIENCY OPTIMIZATIONS ===

    # Continuous batching for maximum throughput
    cont_batching: bool = os.getenv("LLAMACPP_CONT_BATCHING", "true").lower() == "true"

    # Mlock model in RAM (prevent swapping)
    mlock: bool = os.getenv("LLAMACPP_MLOCK", "true").lower() == "true"

    # Use memory-mapped I/O
    use_mmap: bool = os.getenv("LLAMACPP_USE_MMAP", "true").lower() == "true"

    # No KV offload to CPU (keep everything on GPU)
    no_kv_offload: bool = os.getenv("LLAMACPP_NO_KV_OFFLOAD", "false").lower() == "true"

    # === SAMPLING PARAMETERS ===

    # Temperature for generation
    temperature: float = float(os.getenv("LLAMACPP_TEMPERATURE", "0.7"))

    # Top-p (nucleus sampling)
    top_p: float = float(os.getenv("LLAMACPP_TOP_P", "0.9"))

    # Top-k sampling
    top_k: int = int(os.getenv("LLAMACPP_TOP_K", "40"))

    # Repeat penalty
    repeat_penalty: float = float(os.getenv("LLAMACPP_REPEAT_PENALTY", "1.1"))

    # Max tokens per generation
    max_tokens: int = int(os.getenv("LLAMACPP_MAX_TOKENS", "4096"))

    def get_server_args(self) -> list[str]:
        """Generate llama-server command line arguments."""
        args = [
            self.binary_path,
            "--model", self.model_path,
            "--host", self.server_host,
            "--port", str(self.server_port),
            "--ctx-size", str(self.ctx_size),
            "--n-gpu-layers", str(self.n_gpu_layers),
            "--batch-size", str(self.batch_size),
            "--ubatch-size", str(self.ubatch_size),
            "--threads", str(self.threads),
            "--parallel", str(self.parallel),
            "--timeout", str(self.server_timeout),
        ]

        if self.flash_attn:
            args.append("--flash-attn")

        if self.cont_batching:
            args.append("--cont-batching")

        if self.mlock:
            args.append("--mlock")

        if self.use_mmap:
            args.append("--use-mmap")

        if self.no_kv_offload:
            args.append("--no-kv-offload")

        return args

    @property
    def api_base_url(self) -> str:
        """Base URL for the llama-server API."""
        return f"http://{self.server_host}:{self.server_port}/v1"

    @property
    def health_url(self) -> str:
        """Health check endpoint."""
        return f"http://{self.server_host}:{self.server_port}/health"


# Singleton config instance
_config: Optional[LlamaCppConfig] = None


def get_llamacpp_config() -> LlamaCppConfig:
    """Get or create the singleton configuration."""
    global _config
    if _config is None:
        _config = LlamaCppConfig()
    return _config