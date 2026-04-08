"""
Model router — dispatches inference requests to the correct backend
(local GGUF model or API model).
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


class ModelNotFoundError(Exception):
    """Raised when a model name is not registered in the router."""
    pass


class ModelRouter:
    """
    Central router that manages multiple model backends and dispatches
    inference requests to the correct one based on model name.
    """

    def __init__(self, config: dict):
        """
        Initialize model router with configuration.

        Args:
            config: Full configuration dict with 'models' section.
                    Each model entry must have 'type' ("local" or "api")
                    and corresponding parameters.
        """
        self.config = config
        self._models = {}
        self._load_models(config.get("models", {}))

    def _load_models(self, models_config: dict) -> None:
        """Initialize model backends from config."""
        for name, model_cfg in models_config.items():
            model_type = model_cfg.get("type")
            if model_type == "local":
                from .local_model import LocalModel
                self._models[name] = LocalModel(
                    model_path=model_cfg["model_path"],
                    max_context=model_cfg.get("max_context", 4096),
                    system_prompt=model_cfg.get("system_prompt"),
                )
                logger.info(f"Registered local model: {name}")
            elif model_type == "api":
                from .api_model import APIModel
                self._models[name] = APIModel(
                    api_base=model_cfg["api_base"],
                    api_key_env=model_cfg["api_key_env"],
                    model_id=model_cfg.get("model_id", name),
                    max_context=model_cfg.get("max_context", 4096),
                    system_prompt=model_cfg.get("system_prompt"),
                )
                logger.info(f"Registered API model: {name}")
            else:
                logger.warning(f"Unknown model type '{model_type}' for '{name}', skipping.")

    def get_model(self, model_name: str):
        """
        Get a model backend by name.

        Raises:
            ModelNotFoundError: If model_name is not registered.
        """
        if model_name not in self._models:
            available = ", ".join(self._models.keys())
            raise ModelNotFoundError(
                f"Model '{model_name}' not found. Available: {available}"
            )
        return self._models[model_name]

    def infer(
        self,
        prompt: str,
        model_name: str,
        temperature: float = 0.0,
        max_tokens: int = 2048,
        stop: Optional[list] = None,
    ) -> str:
        """
        Route inference request to the appropriate model.

        Args:
            prompt: Formatted prompt text.
            model_name: Registered model identifier.
            temperature: Generation temperature.
            max_tokens: Maximum tokens to generate.
            stop: Optional stop sequences.

        Returns:
            Generated response text.
        """
        model = self.get_model(model_name)
        logger.debug(f"Routing to model: {model_name}")
        return model.infer(
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            stop=stop,
        )

    def list_models(self) -> list:
        """Return list of registered model names."""
        return list(self._models.keys())

    def is_local(self, model_name: str) -> bool:
        """Check if a model runs locally (vs API)."""
        model = self.get_model(model_name)
        return hasattr(model, "_model")  # LocalModel has _model attribute
