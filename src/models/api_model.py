"""
API model inference for OpenAI-compatible endpoints.
Supports GPT-4o-mini (OpenAI) and DeepSeek Chat (DeepSeek API).
"""

import os
import time
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class APIModel:
    """
    Wrapper for API-based model inference using OpenAI SDK.
    Compatible with any OpenAI-compatible API endpoint.
    """

    def __init__(
        self,
        api_base: str,
        api_key_env: str,
        model_id: str,
        max_context: int = 4096,
        system_prompt: Optional[str] = None,
    ):
        """
        Initialize API model client.

        Args:
            api_base: API endpoint URL (e.g., "https://api.openai.com/v1").
            api_key_env: Environment variable name containing the API key.
            model_id: Model identifier for the API (e.g., "gpt-4o-mini").
            max_context: Maximum context window size.
            system_prompt: Default system prompt.
        """
        self.api_base = api_base
        self.api_key_env = api_key_env
        self.model_id = model_id
        self.max_context = max_context
        self.system_prompt = system_prompt or "You are a helpful assistant."
        self._client = None

    def _get_client(self):
        """Lazy-initialize the OpenAI client."""
        if self._client is not None:
            return self._client

        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError(
                "openai package is required for API inference. "
                "Install it with: pip install openai"
            )

        api_key = os.environ.get(self.api_key_env, "")
        if not api_key:
            raise ValueError(
                f"API key not found. Set the environment variable "
                f"'{self.api_key_env}' in your .env file."
            )

        self._client = OpenAI(
            base_url=self.api_base,
            api_key=api_key,
        )
        return self._client

    def infer(
        self,
        prompt: str,
        temperature: float = 0.0,
        max_tokens: int = 2048,
        stop: Optional[list] = None,
    ) -> str:
        """
        Run inference via API.

        Args:
            prompt: The user message text.
            temperature: Generation temperature.
            max_tokens: Maximum tokens to generate.
            stop: Optional stop sequences.

        Returns:
            Generated response text.
        """
        client = self._get_client()
        start_time = time.time()

        kwargs = {
            "model": self.model_id,
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if stop:
            kwargs["stop"] = stop

        response = client.chat.completions.create(**kwargs)
        elapsed_ms = (time.time() - start_time) * 1000

        output_text = response.choices[0].message.content
        token_count = response.usage.completion_tokens if response.usage else 0

        logger.info(
            f"API inference ({self.model_id}) completed in {elapsed_ms:.0f}ms, "
            f"{token_count} tokens generated."
        )
        return output_text

    def is_loaded(self) -> bool:
        """API models are always 'loaded' (stateless)."""
        return True
