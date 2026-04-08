"""
Download and verify all 3 benchmark datasets from HuggingFace.

Datasets:
  - MATH-500: 500 competition-level math problems
  - GSM8K: 1,319 grade-school math word problems
  - AIME 2024: 30 advanced competition problems

Usage:
    python scripts/download_datasets.py
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
os.chdir(project_root)

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

from src.data.loader import load_dataset, DATASET_CONFIG
from src.data.preprocessor import preprocess_dataset


def main():
    logger.info("=" * 60)
    logger.info("DOWNLOADING BENCHMARK DATASETS")
    logger.info("=" * 60)
    logger.info("")

    datasets_info = {}

    for name in ["math500", "gsm8k", "aime2024"]:
        logger.info("-" * 60)
        logger.info(
            "Dataset: %s  (HuggingFace ID: %s)",
            name, DATASET_CONFIG[name]["hf_id"]
        )
        logger.info("-" * 60)
        try:
            # Load from HuggingFace (uses default HF cache)
            raw = load_dataset(name)
            logger.info("  Raw dataset size: %d", len(raw))

            # Preprocess into unified format
            problems = preprocess_dataset(raw, name)
            logger.info("  Preprocessed: %d problems", len(problems))

            # Preview first problem
            if problems:
                p = problems[0]
                logger.info("  Sample problem:")
                logger.info("    ID: %s", p["id"])
                prob_text = p["problem"][:150].replace("\n", " ")
                logger.info("    Problem: %s...", prob_text)
                logger.info("    Answer: %s", p["answer"])

            datasets_info[name] = {
                "raw_size": len(raw),
                "preprocessed_size": len(problems),
                "status": "OK",
            }
        except Exception as e:
            import traceback
            logger.error("FAILED to load %s: %s", name, e)
            logger.error(traceback.format_exc())
            datasets_info[name] = {"status": "FAILED", "error": str(e)}

    # Print summary
    logger.info("")
    logger.info("=" * 60)
    logger.info("DOWNLOAD SUMMARY")
    logger.info("=" * 60)

    all_ok = True
    for name, info in datasets_info.items():
        if info["status"] == "OK":
            logger.info(
                "  %-10s OK  (%d raw -> %d preprocessed)",
                name, info["raw_size"], info["preprocessed_size"],
            )
        else:
            logger.info("  %-10s FAILED  (%s)", name, info.get("error", ""))
            all_ok = False

    if all_ok:
        logger.info("")
        logger.info("All 3 datasets downloaded and preprocessed successfully!")
    else:
        logger.info("")
        logger.error("Some datasets failed. Check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
