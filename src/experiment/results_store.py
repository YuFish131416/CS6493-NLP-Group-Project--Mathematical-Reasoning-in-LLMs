"""
Results storage and persistence.
Saves and loads experiment results as JSON files.
"""

import json
import os
import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)


class ResultsStore:
    """
    JSON-based results persistence with checkpoint support.
    """

    def __init__(self, output_dir: str = "results"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, "checkpoints"), exist_ok=True)

    def save(self, results: dict, path: Optional[str] = None) -> str:
        """
        Save experiment results to JSON file.

        Args:
            results: Results dict to persist.
            path: Output file path. If None, auto-generates from run_id.

        Returns:
            The file path where results were saved.
        """
        if path is None:
            run_id = results.get("run_id", "unknown")
            path = os.path.join(self.output_dir, f"{run_id}_results.json")

        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)

        logger.info(f"Results saved to {path}")
        return path

    def load(self, path: str) -> dict:
        """
        Load experiment results from JSON file.

        Args:
            path: Path to the results JSON file.

        Returns:
            Loaded results dict.
        """
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"Results loaded from {path}")
        return data

    def save_checkpoint(
        self,
        run_id: str,
        model_name: str,
        method_name: str,
        dataset_name: str,
        problem_id: str,
        result: dict,
    ) -> None:
        """
        Save a single problem result as a checkpoint.

        Checkpoints are small JSON files that allow resuming experiments.
        """
        ckpt_dir = os.path.join(self.output_dir, "checkpoints", run_id)
        os.makedirs(ckpt_dir, exist_ok=True)

        ckpt_name = f"{model_name}__{method_name}__{dataset_name}__{problem_id}.json"
        ckpt_path = os.path.join(ckpt_dir, ckpt_name)

        with open(ckpt_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False, default=str)

    def load_checkpoints(self, run_id: str) -> list:
        """
        Get list of completed problem IDs for a given run.

        Returns:
            List of checkpoint filenames (without .json extension).
        """
        ckpt_dir = os.path.join(self.output_dir, "checkpoints", run_id)
        if not os.path.exists(ckpt_dir):
            return []

        checkpoints = []
        for fname in os.listdir(ckpt_dir):
            if fname.endswith('.json'):
                checkpoints.append(fname[:-5])  # Remove .json
        return checkpoints

    def load_all_checkpoints(self, run_id: str) -> list:
        """
        Load all checkpoint results for a given run.

        Returns:
            List of result dicts.
        """
        ckpt_dir = os.path.join(self.output_dir, "checkpoints", run_id)
        if not os.path.exists(ckpt_dir):
            return []

        results = []
        for fname in sorted(os.listdir(ckpt_dir)):
            if fname.endswith('.json'):
                with open(os.path.join(ckpt_dir, fname), 'r', encoding='utf-8') as f:
                    results.append(json.load(f))
        return results

    def clear_checkpoints(self, run_id: str) -> None:
        """Remove all checkpoints for a given run."""
        import shutil
        ckpt_dir = os.path.join(self.output_dir, "checkpoints", run_id)
        if os.path.exists(ckpt_dir):
            shutil.rmtree(ckpt_dir)
            logger.info(f"Cleared checkpoints for run {run_id}")

    def list_runs(self) -> list:
        """List all run IDs that have results."""
        results_dir = self.output_dir
        runs = []
        if os.path.exists(results_dir):
            for fname in os.listdir(results_dir):
                if fname.endswith('_results.json'):
                    run_id = fname.replace('_results.json', '')
                    runs.append(run_id)
        return sorted(runs)
