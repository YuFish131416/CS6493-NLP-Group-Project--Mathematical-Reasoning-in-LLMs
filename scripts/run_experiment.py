"""
Full experiment runner with progress tracking and resume support.
Runs all model x method x dataset combinations with checkpointing.

Usage:
    python scripts/run_experiment.py --config config/config.local.yaml --sample-size 5
    python scripts/run_experiment.py --sample-size 5 --models qwen2.5-math --datasets gsm8k
    python scripts/run_experiment.py --sample-size 20  # Full experiment
"""
import sys
import os
import time
import argparse
import logging

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
os.chdir(project_root)

from src.experiment.config import ExperimentConfig
from src.experiment.runner import Runner


def main():
    parser = argparse.ArgumentParser(description="Run math reasoning experiments")
    parser.add_argument(
        "--config", type=str, default="config/config.local.yaml",
        help="Path to experiment config YAML file"
    )
    parser.add_argument(
        "--sample-size", type=int, default=None,
        help="Override sample size (number of problems per dataset)"
    )
    parser.add_argument(
        "--models", type=str, default=None,
        help="Comma-separated model names to run (overrides config)"
    )
    parser.add_argument(
        "--methods", type=str, default=None,
        help="Comma-separated prompt methods to run (overrides config)"
    )
    parser.add_argument(
        "--datasets", type=str, default=None,
        help="Comma-separated dataset names to run (overrides config)"
    )
    parser.add_argument(
        "--run-id", type=str, default=None,
        help="Custom run ID (for checkpoint resume)"
    )
    parser.add_argument(
        "--n-samples", type=int, default=None,
        help="Override n_samples for self-consistency (default from config)"
    )
    parser.add_argument(
        "--max-refine-rounds", type=int, default=None,
        help="Override max_refine_rounds for self-refine (default from config)"
    )
    parser.add_argument(
        "--verbose", action="store_true",
        help="Enable verbose logging"
    )
    args = parser.parse_args()

    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    os.makedirs("tmp", exist_ok=True)
    os.makedirs("results", exist_ok=True)
    os.makedirs("results/checkpoints", exist_ok=True)

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("tmp/experiment.log", encoding="utf-8"),
        ]
    )
    logger = logging.getLogger(__name__)

    # Load config
    logger.info("Loading config from %s", args.config)
    config = ExperimentConfig.from_yaml(args.config)

    # Apply overrides
    if args.sample_size is not None:
        config.sample_size = args.sample_size
    if args.models:
        config.models = [m.strip() for m in args.models.split(",")]
    if args.methods:
        config.prompt_methods = [m.strip() for m in args.methods.split(",")]
    if args.datasets:
        config.datasets = [d.strip() for d in args.datasets.split(",")]
    if args.run_id:
        config.run_id = args.run_id
    if args.n_samples is not None:
        config.n_samples = args.n_samples
    if args.max_refine_rounds is not None:
        config.max_refine_rounds = args.max_refine_rounds

    # Print experiment plan
    total_combos = len(config.models) * len(config.prompt_methods) * len(config.datasets)
    total_problems = total_combos * config.sample_size if config.sample_size > 0 else "all"

    logger.info("=" * 70)
    logger.info("EXPERIMENT CONFIGURATION")
    logger.info("=" * 70)
    logger.info("Run ID: %s", config.run_id)
    logger.info("Models: %s", config.models)
    logger.info("Methods: %s", config.prompt_methods)
    logger.info("Datasets: %s", config.datasets)
    logger.info("Sample size: %s", config.sample_size)
    logger.info("Self-consistency samples: %d", config.n_samples)
    logger.info("Self-refine rounds: %d", config.max_refine_rounds)
    logger.info("Total combinations: %d", total_combos)
    logger.info("Total problems (approx): %s", total_problems)
    logger.info("=" * 70)

    # Create runner (ModelRouter is auto-created from config._raw_yaml)
    runner = Runner(config)

    if runner.router is None:
        logger.error("No model router available. Check your config file.")
        sys.exit(1)

    logger.info("Available models: %s", runner.router.list_models())

    # Run experiments
    start = time.time()
    results = runner.run()
    elapsed = time.time() - start

    # Print summary
    print("\n" + "=" * 70)
    print("EXPERIMENT RESULTS SUMMARY")
    print("=" * 70)
    print("Run ID: %s" % results["run_id"])
    print("Total problems: %d" % results["total_problems"])
    print("Total correct: %d" % results["total_correct"])
    print("Overall accuracy: %.4f" % results["overall_accuracy"])
    print("Total time: %.1f seconds (%.1f minutes)" % (elapsed, elapsed / 60))
    print()

    # Per-combo results
    for key, summary in results.get("summary", {}).items():
        print("  %s x %s x %s: accuracy=%.4f (%d/%d) extract=%.2f" % (
            summary["model"], summary["method"], summary["dataset"],
            summary["accuracy"], summary["correct"], summary["total"],
            summary["extract_success_rate"]
        ))

    # Per-model aggregate
    print("\n  Per-Model:")
    for model in config.models:
        m_results = [s for s in results["summary"].values() if s["model"] == model]
        if m_results:
            total_c = sum(s["correct"] for s in m_results)
            total_n = sum(s["total"] for s in m_results)
            print("    %s: %.4f (%d/%d)" % (model, total_c / total_n if total_n else 0, total_c, total_n))

    # Per-method aggregate
    print("\n  Per-Method:")
    for method in config.prompt_methods:
        m_results = [s for s in results["summary"].values() if s["method"] == method]
        if m_results:
            total_c = sum(s["correct"] for s in m_results)
            total_n = sum(s["total"] for s in m_results)
            print("    %s: %.4f (%d/%d)" % (method, total_c / total_n if total_n else 0, total_c, total_n))

    # Per-dataset aggregate
    print("\n  Per-Dataset:")
    for ds in config.datasets:
        d_results = [s for s in results["summary"].values() if s["dataset"] == ds]
        if d_results:
            total_c = sum(s["correct"] for s in d_results)
            total_n = sum(s["total"] for s in d_results)
            print("    %s: %.4f (%d/%d)" % (ds, total_c / total_n if total_n else 0, total_c, total_n))

    print("\nResults saved to: %s" % config.output_dir)
    print("=" * 70)


if __name__ == "__main__":
    main()
