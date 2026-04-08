"""
Dataset loader for MATH-500, GSM8K, and AIME 2024.
Loads datasets from HuggingFace Hub with local caching support.
"""

import os
import logging
from typing import Optional

from datasets import load_dataset as hf_load_dataset

logger = logging.getLogger(__name__)

# Dataset configuration registry
DATASET_CONFIG = {
    "math500": {
        "hf_id": "HuggingFaceH4/MATH-500",
        "split": "test",
        "description": "500 competition-level math problems from the MATH dataset",
    },
    "gsm8k": {
        "hf_id": "openai/gsm8k",
        "split": "test",
        "description": "8,500 grade school math word problems (test set: ~1,319)",
    },
    "aime2024": {
        "hf_id": "HuggingFaceH4/aime_2024",
        "split": "train",
        "description": "AIME 2024 competition problems (30 problems from AIME I & II)",
    },
}


def load_dataset(
    dataset_name: str,
    split: Optional[str] = None,
    cache_dir: Optional[str] = None,
) -> object:
    """
    Load a benchmark dataset from HuggingFace Hub or local cache.

    Args:
        dataset_name: One of "math500", "gsm8k", "aime2024".
        split: Dataset split to load. If None, uses the default split.
        cache_dir: Local directory for caching downloaded datasets.
                   If None, uses default HuggingFace cache directory.

    Returns:
        HuggingFace Dataset object.

    Raises:
        ValueError: If dataset_name is not one of the supported values.
    """
    if dataset_name not in DATASET_CONFIG:
        valid = ", ".join(DATASET_CONFIG.keys())
        raise ValueError(
            f"Unknown dataset '{dataset_name}'. Supported: {valid}"
        )

    config = DATASET_CONFIG[dataset_name]
    hf_id = config["hf_id"]
    use_split = split or config["split"]

    logger.info(
        f"Loading dataset '{dataset_name}' from HuggingFace: {hf_id} (split={use_split})"
    )

    # Build load kwargs — only include cache_dir if explicitly provided
    load_kwargs = {
        "split": use_split,
    }
    if cache_dir:
        os.makedirs(cache_dir, exist_ok=True)
        load_kwargs["cache_dir"] = cache_dir

    # GSM8K requires specifying the "main" config name
    if dataset_name == "gsm8k":
        load_kwargs["name"] = "main"

    # trust_remote_code for datasets that may have loading scripts
    load_kwargs["trust_remote_code"] = True

    dataset = hf_load_dataset(hf_id, **load_kwargs)

    logger.info(
        f"Loaded {len(dataset)} examples from '{dataset_name}'"
    )
    return dataset


def get_available_datasets() -> list:
    """Return list of all supported dataset names."""
    return list(DATASET_CONFIG.keys())


def get_dataset_info(dataset_name: str) -> dict:
    """Return configuration and metadata for a specific dataset."""
    if dataset_name not in DATASET_CONFIG:
        raise ValueError(f"Unknown dataset: {dataset_name}")
    return DATASET_CONFIG[dataset_name]
