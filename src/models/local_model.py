"""
Local GGUF model loading and CPU inference.
Uses llama-cpp-python for efficient CPU-based inference with quantized models.
"""

import os
import time
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class LocalModel:
    """
    Wrapper for local GGUF model inference via llama-cpp-python.

    Supports Q4_K_M quantized models (~1GB) for CPU inference.
    """

    def __init__(
        self,
        model_path: str,
        max_context: int = 4096,
        system_prompt: Optional[str] = None,
        n_ctx: Optional[int] = None,
        n_threads: Optional[int] = None,
    ):
        self.model_path = model_path
        self.max_context = max_context
        self.system_prompt = system_prompt or "You are a helpful assistant."
        self.n_ctx = n_ctx or min(max_context, 4096)
        self.n_threads = n_threads or (os.cpu_count() or 4)
        self._model = None
        self._loaded = False

    def load(self) -> None:
        """Load the model into memory. Must be called before infer()."""
        if self._loaded:
            logger.info(f"Model already loaded: {self.model_path}")
            return

        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"Model file not found: {self.model_path}. "
                f"Please download the GGUF model and place it at this path."
            )

        logger.info(
            f"Loading local model from {self.model_path} "
            f"(ctx={self.n_ctx}, threads={self.n_threads})..."
        )

        try:
            from llama_cpp import Llama
        except ImportError:
            raise ImportError(
                "llama-cpp-python is required for local model inference. "
                "Install it with: pip install llama-cpp-python"
            )

        self._model = Llama(
            model_path=self.model_path,
            n_ctx=self.n_ctx,
            n_threads=self.n_threads,
            verbose=False,
        )
        self._loaded = True
        logger.info("Model loaded successfully.")

    def infer(
        self,
        prompt: str,
        temperature: float = 0.0,
        max_tokens: int = 2048,
        stop: Optional[list] = None,
    ) -> str:
        """
        Run inference on the local model.

        Args:
            prompt: The formatted prompt text (user message).
            temperature: Generation temperature (0.0 for deterministic).
            max_tokens: Maximum tokens to generate.
            stop: Optional stop sequences.

        Returns:
            Generated response text.
        """
        if not self._loaded:
            self.load()

        start_time = time.time()

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt},
        ]

        response = self._model.create_chat_completion(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stop=stop or [],
        )

        elapsed_ms = (time.time() - start_time) * 1000
        output_text = response["choices"][0]["message"]["content"]
        token_count = response.get("usage", {}).get("completion_tokens", 0)

        logger.info(
            f"Inference completed in {elapsed_ms:.0f}ms, "
            f"{token_count} tokens generated."
        )
        return output_text

    def is_loaded(self) -> bool:
        return self._loaded

    def unload(self) -> None:
        if self._model is not None:
            del self._model
            self._model = None
            self._loaded = False
            logger.info("Model unloaded.")
