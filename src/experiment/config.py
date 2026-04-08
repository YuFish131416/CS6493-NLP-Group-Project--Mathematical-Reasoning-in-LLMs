"""
Experiment configuration management.
"""

import os
import time
import uuid
import yaml
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class ExperimentConfig:
    """
    Manages experiment configuration: model-method-dataset combinations
    and hyperparameters.
    """

    def __init__(
        self,
        models: list = None,
        prompt_methods: list = None,
        datasets: list = None,
        sample_size: int = -1,
        temperature: float = 0.0,
        max_tokens: int = 2048,
        seed: int = 42,
        n_samples: int = 5,
        max_refine_rounds: int = 2,
        checkpoint_dir: str = "results/checkpoints",
        output_dir: str = "results",
        run_id: Optional[str] = None,
    ):
        self.run_id = run_id or f"run_{uuid.uuid4().hex[:8]}"
        self.models = models or []
        self.prompt_methods = prompt_methods or []
        self.datasets = datasets or []
        self.sample_size = sample_size
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.seed = seed
        self.n_samples = n_samples
        self.max_refine_rounds = max_refine_rounds
        self.checkpoint_dir = checkpoint_dir
        self.output_dir = output_dir
        self.created_at = time.strftime("%Y-%m-%dT%H:%M:%S")

    @classmethod
    def from_yaml(cls, path: str) -> "ExperimentConfig":
        """Load experiment config from a YAML file."""
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        exp_cfg = data.get("experiments", {})
        paths_cfg = data.get("paths", {})

        # Parse datasets: can be dict (keys=names), comma-separated string, or list
        raw_datasets = data.get("datasets", {})
        if isinstance(raw_datasets, dict):
            datasets = list(raw_datasets.keys())
        elif isinstance(raw_datasets, str):
            datasets = [d.strip() for d in raw_datasets.split(",") if d.strip()]
        elif isinstance(raw_datasets, list):
            datasets = raw_datasets
        else:
            datasets = []

        instance = cls(
            models=list(data.get("models", {}).keys()),
            prompt_methods=["cot", "self_consistency", "self_refine",
                           "least_to_most", "pvp"],
            datasets=datasets,
            sample_size=exp_cfg.get("sample_size", -1),
            temperature=exp_cfg.get("temperature", 0.0),
            max_tokens=exp_cfg.get("max_tokens", 2048),
            seed=exp_cfg.get("seed", 42),
            n_samples=exp_cfg.get("n_samples", 5),
            max_refine_rounds=exp_cfg.get("max_refine_rounds", 2),
            checkpoint_dir=exp_cfg.get("checkpoint_dir", "results/checkpoints"),
            output_dir=exp_cfg.get("output_dir", "results"),
        )
        # Store the raw YAML data for ModelRouter initialization
        instance._raw_yaml = data
        instance._yaml_path = path
        return instance

    def get_model_configs(self, config_path: Optional[str] = None) -> dict:
        """Get model-specific configurations from YAML."""
        if config_path is None:
            return {}
        if not os.path.exists(config_path):
            logger.warning(f"Config file not found: {config_path}")
            return {}
        with open(config_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return data.get("models", {})

    def to_dict(self) -> dict:
        """Serialize config to dict."""
        return {
            "run_id": self.run_id,
            "models": self.models,
            "prompt_methods": self.prompt_methods,
            "datasets": self.datasets,
            "sample_size": self.sample_size,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "seed": self.seed,
            "n_samples": self.n_samples,
            "max_refine_rounds": self.max_refine_rounds,
            "checkpoint_dir": self.checkpoint_dir,
            "output_dir": self.output_dir,
            "created_at": self.created_at,
        }

    def __repr__(self) -> str:
        return (
            f"ExperimentConfig(run_id={self.run_id}, "
            f"models={self.models}, methods={self.prompt_methods}, "
            f"datasets={self.datasets})"
        )
