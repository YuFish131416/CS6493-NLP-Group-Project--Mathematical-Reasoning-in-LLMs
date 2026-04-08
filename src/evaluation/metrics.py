"""
Evaluation metrics for math reasoning experiments.
"""

import statistics
import logging
from typing import Optional

from .answer_extractor import extract_answer
from .math_parser import answers_match

logger = logging.getLogger(__name__)


def compute_accuracy(predictions: list, ground_truths: list) -> float:
    """
    Compute exact-match accuracy between predictions and ground truths.

    Uses answers_match() for robust mathematical equivalence checking.

    Args:
        predictions: List of extracted answer strings.
        ground_truths: List of ground truth answer strings.

    Returns:
        Accuracy between 0.0 and 1.0.

    Raises:
        ValueError: If lists have different lengths.
    """
    if len(predictions) != len(ground_truths):
        raise ValueError(
            f"Length mismatch: predictions={len(predictions)}, "
            f"ground_truths={len(ground_truths)}"
        )

    if not predictions:
        return 0.0

    correct = sum(
        1 for pred, truth in zip(predictions, ground_truths)
        if answers_match(pred, truth)
    )
    return correct / len(predictions)


def compute_response_lengths(responses: list) -> dict:
    """
    Compute response length statistics.

    Args:
        responses: List of model response strings.

    Returns:
        Dict with keys: mean, median, min, max, std.
    """
    if not responses:
        return {"mean": 0, "median": 0, "min": 0, "max": 0, "std": 0}

    lengths = [len(r) for r in responses]
    return {
        "mean": statistics.mean(lengths),
        "median": statistics.median(lengths),
        "min": min(lengths),
        "max": max(lengths),
        "std": statistics.stdev(lengths) if len(lengths) > 1 else 0,
    }


def compute_token_efficiency(
    accuracies: list,
    token_counts: list,
    per_thousand: bool = True,
) -> dict:
    """
    Compute token efficiency metrics.

    Args:
        accuracies: List of per-problem accuracy values (0 or 1).
        token_counts: List of token counts per problem.
        per_thousand: If True, compute accuracy per 1000 tokens.

    Returns:
        Dict with keys: avg_accuracy, avg_tokens, efficiency (accuracy per 1K tokens).
    """
    if not accuracies or not token_counts:
        return {"avg_accuracy": 0, "avg_tokens": 0, "efficiency": 0}

    avg_acc = sum(accuracies) / len(accuracies)
    avg_tokens = sum(token_counts) / len(token_counts)

    if per_thousand:
        efficiency = avg_acc / (avg_tokens / 1000) if avg_tokens > 0 else 0
    else:
        efficiency = avg_acc / avg_tokens if avg_tokens > 0 else 0

    return {
        "avg_accuracy": avg_acc,
        "avg_tokens": avg_tokens,
        "efficiency": efficiency,
    }


def compute_extraction_success_rate(responses: list) -> float:
    """
    Compute the rate of successful answer extraction from responses.

    Args:
        responses: List of model response strings.

    Returns:
        Rate between 0.0 and 1.0.
    """
    if not responses:
        return 0.0
    success = sum(1 for r in responses if extract_answer(r) is not None)
    return success / len(responses)


def compute_step_correctness(response: str, ground_truth: str) -> float:
    """
    Evaluate what fraction of reasoning steps are correct (exploratory).

    This is an approximate metric that counts the number of step markers
    in the response and checks if the final answer matches.

    NOTE: True step-level verification would require a separate evaluator model.
    This implementation provides a lightweight approximation.

    Args:
        response: Model response text.
        ground_truth: Ground truth answer.

    Returns:
        Step-level correctness ratio between 0.0 and 1.0.
    """
    if not response:
        return 0.0

    # Count step indicators
    import re
    steps = re.findall(
        r'(?:Step\s*\d|^\s*[\d\.\)]\s|Therefore|Thus|So,?|Hence)',
        response,
        re.MULTILINE | re.IGNORECASE,
    )
    num_steps = max(len(steps), 1)

    # Check if final answer is correct
    final_answer = extract_answer(response)
    if final_answer and answers_match(final_answer, ground_truth):
        return 1.0  # If final answer is correct, assume steps are correct
    else:
        return 0.0  # If final answer is wrong, at least some steps are wrong
