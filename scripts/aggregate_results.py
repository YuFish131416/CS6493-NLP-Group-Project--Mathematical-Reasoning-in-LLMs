"""
Aggregate all checkpoint results into unified final results.

Reads per-problem checkpoint files from results/checkpoints/,
deduplicates by problem combination, and produces:
  - results/json/final_results.json   (full results with all responses)
  - results/json/final_summary.json   (aggregated statistics only)

Usage:
    python scripts/aggregate_results.py
"""

import os
import sys
import json
import statistics
from collections import defaultdict
from datetime import datetime

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
os.chdir(project_root)

RESULTS_DIR = "results"
JSON_DIR = os.path.join(RESULTS_DIR, "json")
CHECKPOINT_BASE = os.path.join(RESULTS_DIR, "checkpoints")


def load_all_checkpoints():
    """Load all checkpoint files across all runs, deduplicating by problem combo."""
    all_results = {}  # key: model__method__dataset__problem_id -> result dict

    if not os.path.exists(CHECKPOINT_BASE):
        print(f"ERROR: Checkpoint directory not found: {CHECKPOINT_BASE}")
        sys.exit(1)

    for run_dir in sorted(os.listdir(CHECKPOINT_BASE)):
        run_path = os.path.join(CHECKPOINT_BASE, run_dir)
        if not os.path.isdir(run_path):
            continue

        for fname in os.listdir(run_path):
            if not fname.endswith(".json"):
                continue
            key = fname.replace(".json", "")
            filepath = os.path.join(run_path, fname)

            with open(filepath, "r", encoding="utf-8") as f:
                result = json.load(f)

            # Keep the latest result for each unique problem combo
            if key not in all_results:
                all_results[key] = result
            else:
                existing_ts = all_results[key].get("timestamp", "")
                new_ts = result.get("timestamp", "")
                if new_ts > existing_ts:
                    all_results[key] = result

    return all_results


def compute_summary(results_list):
    """Compute summary statistics grouped by model x method x dataset."""
    groups = defaultdict(list)

    for r in results_list:
        model = r.get("model_name", "unknown")
        method = r.get("prompt_method", "unknown")
        dataset = r.get("dataset", "unknown")
        key = f"{model}__{method}__{dataset}"
        groups[key].append(r)

    summary = {}
    for key, items in sorted(groups.items()):
        parts = key.split("__")
        model, method, dataset = parts[0], parts[1], parts[2]

        total = len(items)
        correct = sum(1 for r in items if r.get("is_correct", False))
        accuracy = correct / total if total > 0 else 0.0

        extracted = sum(
            1 for r in items
            if r.get("extracted_answer") is not None and r.get("extracted_answer") != ""
        )
        extract_rate = extracted / total if total > 0 else 0.0

        latencies = [r.get("latency_ms", 0) for r in items if r.get("latency_ms", 0) > 0]
        avg_latency = statistics.mean(latencies) if latencies else 0.0

        lengths = [r.get("response_length", 0) for r in items if r.get("response_length", 0) > 0]
        avg_length = statistics.mean(lengths) if lengths else 0.0

        summary[key] = {
            "model": model,
            "method": method,
            "dataset": dataset,
            "accuracy": round(accuracy, 4),
            "correct": correct,
            "total": total,
            "extract_success_rate": round(extract_rate, 4),
            "avg_latency_ms": round(avg_latency, 1),
            "avg_response_length": round(avg_length, 1),
        }

    return summary


def compute_aggregated_views(summary):
    """Compute aggregated views: by model, by method, by dataset."""
    model_stats = defaultdict(lambda: {"correct": 0, "total": 0})
    method_stats = defaultdict(lambda: {"correct": 0, "total": 0})
    dataset_stats = defaultdict(lambda: {"correct": 0, "total": 0})

    for val in summary.values():
        model_stats[val["model"]]["correct"] += val["correct"]
        model_stats[val["model"]]["total"] += val["total"]

        method_stats[val["method"]]["correct"] += val["correct"]
        method_stats[val["method"]]["total"] += val["total"]

        dataset_stats[val["dataset"]]["correct"] += val["correct"]
        dataset_stats[val["dataset"]]["total"] += val["total"]

    def to_acc(stats):
        return {
            k: {
                "correct": v["correct"],
                "total": v["total"],
                "accuracy": round(v["correct"] / v["total"], 4) if v["total"] > 0 else 0.0,
            }
            for k, v in stats.items()
        }

    return {
        "by_model": to_acc(model_stats),
        "by_method": to_acc(method_stats),
        "by_dataset": to_acc(dataset_stats),
    }


def main():
    print("=" * 60)
    print("AGGREGATING ALL EXPERIMENT RESULTS")
    print("=" * 60)

    all_results = load_all_checkpoints()
    results_list = list(all_results.values())
    print(f"\nTotal unique problem results: {len(results_list)}")

    summary = compute_summary(results_list)
    print(f"Unique model x method x dataset combos: {len(summary)}")

    agg = compute_aggregated_views(summary)

    total_problems = len(results_list)
    total_correct = sum(1 for r in results_list if r.get("is_correct", False))
    overall_accuracy = total_correct / total_problems if total_problems > 0 else 0.0

    # Print table
    print(f"\n{'Model':<20} {'Method':<20} {'Dataset':<12} {'Accuracy':>10} {'Correct':>10} {'Total':>8}")
    print("-" * 82)
    for val in sorted(summary.values(), key=lambda x: (x["model"], x["method"], x["dataset"])):
        print(
            f"{val['model']:<20} {val['method']:<20} {val['dataset']:<12} "
            f"{val['accuracy']:>9.2%} {val['correct']:>10} {val['total']:>8}"
        )
    print(f"\n{'OVERALL':>52} {overall_accuracy:>9.2%} {total_correct:>10} {total_problems:>8}")

    print(f"\n--- By Model ---")
    for k, v in sorted(agg["by_model"].items()):
        print(f"  {k:<25} {v['accuracy']:>8.2%}  ({v['correct']}/{v['total']})")

    print(f"\n--- By Method ---")
    for k, v in sorted(agg["by_method"].items()):
        print(f"  {k:<25} {v['accuracy']:>8.2%}  ({v['correct']}/{v['total']})")

    print(f"\n--- By Dataset ---")
    for k, v in sorted(agg["by_dataset"].items()):
        print(f"  {k:<25} {v['accuracy']:>8.2%}  ({v['correct']}/{v['total']})")

    # Save outputs
    os.makedirs(JSON_DIR, exist_ok=True)

    final_results = {
        "run_id": "final_aggregated",
        "description": "Aggregated results from all experiment runs",
        "config": {
            "models": sorted(set(r.get("model_name", "") for r in results_list)),
            "prompt_methods": sorted(set(r.get("prompt_method", "") for r in results_list)),
            "datasets": sorted(set(r.get("dataset", "") for r in results_list)),
        },
        "total_problems": total_problems,
        "total_correct": total_correct,
        "overall_accuracy": round(overall_accuracy, 4),
        "summary": summary,
        "aggregated": agg,
        "responses": results_list,
        "completed_at": datetime.now().isoformat(),
    }

    final_path = os.path.join(JSON_DIR, "final_results.json")
    with open(final_path, "w", encoding="utf-8") as f:
        json.dump(final_results, f, indent=2, ensure_ascii=False, default=str)
    print(f"\nFull results saved to: {final_path}")

    summary_data = {
        "run_id": "final_aggregated",
        "total_problems": total_problems,
        "total_correct": total_correct,
        "overall_accuracy": round(overall_accuracy, 4),
        "summary": summary,
        "aggregated": agg,
        "completed_at": datetime.now().isoformat(),
    }

    summary_path = os.path.join(JSON_DIR, "final_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False, default=str)
    print(f"Summary saved to: {summary_path}")


if __name__ == "__main__":
    main()
