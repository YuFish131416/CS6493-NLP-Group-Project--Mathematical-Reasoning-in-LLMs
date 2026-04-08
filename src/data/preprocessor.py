"""
Dataset preprocessing for MATH-500, GSM8K, and AIME 2024.
Cleans and normalizes raw HuggingFace dataset entries into a unified format.
"""

import re
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def preprocess_math500(raw_data: object) -> list:
    """
    Clean and normalize MATH-500 dataset entries.

    MATH-500 fields:
        - problem: the math problem text
        - solution: full step-by-step solution with LaTeX
        - answer: the final answer (may be in \\boxed{} format)

    Args:
        raw_data: HuggingFace Dataset object for MATH-500.

    Returns:
        List of dicts with keys: id, problem, answer, solution, level, type, dataset.
    """
    results = []
    for idx, item in enumerate(raw_data):
        problem = item.get("problem", "").strip()
        solution = item.get("solution", "").strip()
        answer_raw = item.get("answer", "").strip()

        # Extract answer from \boxed{} if present
        answer = _extract_boxed_answer(answer_raw) or answer_raw
        answer = _normalize_answer(answer)

        # Parse difficulty level (MATH-500 has levels 1-5, may be "Level 1" format)
        level = item.get("level", None)
        if level is not None:
            if isinstance(level, str):
                # Handle "Level 1", "Level 2" format
                import re as _re
                m = _re.search(r'\d+', str(level))
                level = int(m.group()) if m else None
            else:
                try:
                    level = int(level)
                except (ValueError, TypeError):
                    level = None

        problem_type = item.get("type", None)

        results.append({
            "id": f"math500_{idx}",
            "problem": problem,
            "answer": answer,
            "solution": solution,
            "level": level,
            "type": problem_type,
            "dataset": "math500",
        })

    logger.info(f"Preprocessed {len(results)} MATH-500 problems")
    return results


def preprocess_gsm8k(raw_data: object) -> list:
    """
    Clean and normalize GSM8K dataset entries.

    GSM8K fields:
        - question: the word problem text
        - answer: the solution with final answer after ####

    Args:
        raw_data: HuggingFace Dataset object for GSM8K.

    Returns:
        List of dicts with keys: id, problem, answer, dataset.
    """
    results = []
    for idx, item in enumerate(raw_data):
        problem = item.get("question", "").strip()
        answer_raw = item.get("answer", "").strip()

        # GSM8K stores the final answer after ####
        answer = _extract_gsm8k_answer(answer_raw)
        answer = _normalize_answer(answer)

        results.append({
            "id": f"gsm8k_{idx}",
            "problem": problem,
            "answer": answer,
            "solution": answer_raw,
            "level": None,
            "type": None,
            "dataset": "gsm8k",
        })

    logger.info(f"Preprocessed {len(results)} GSM8K problems")
    return results


def preprocess_aime(raw_data: object) -> list:
    """
    Clean and normalize AIME 2024 dataset entries.

    AIME 2024 fields (varies by source):
        - problem: the competition problem text
        - answer: the integer answer (0-999)
        - solution: optional full solution

    Args:
        raw_data: HuggingFace Dataset object for AIME 2024.

    Returns:
        List of dicts with keys: id, problem, answer, dataset.
    """
    results = []
    for idx, item in enumerate(raw_data):
        # Handle varying field names across AIME datasets
        problem = (
            item.get("problem", "")
            or item.get("question", "")
            or str(item.get("input", ""))
        ).strip()

        answer_raw = (
            str(item.get("answer", ""))
            or str(item.get("output", ""))
            or ""
        ).strip()

        answer = _normalize_answer(answer_raw)

        solution = (
            item.get("solution", "")
            or item.get("reasoning", "")
            or ""
        ).strip()

        results.append({
            "id": f"aime2024_{idx}",
            "problem": problem,
            "answer": answer,
            "solution": solution,
            "level": None,
            "type": None,
            "dataset": "aime2024",
        })

    logger.info(f"Preprocessed {len(results)} AIME 2024 problems")
    return results


def preprocess_dataset(raw_data: object, dataset_name: str) -> list:
    """
    Route to the correct preprocessor based on dataset name.

    Args:
        raw_data: HuggingFace Dataset object.
        dataset_name: One of "math500", "gsm8k", "aime2024".

    Returns:
        List of preprocessed problem dicts.
    """
    preprocessors = {
        "math500": preprocess_math500,
        "gsm8k": preprocess_gsm8k,
        "aime2024": preprocess_aime,
    }

    if dataset_name not in preprocessors:
        raise ValueError(f"No preprocessor for dataset: {dataset_name}")

    return preprocessors[dataset_name](raw_data)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _extract_boxed_answer(text: str) -> Optional[str]:
    """
    Extract the content inside \\boxed{...} from a string.

    Handles nested braces up to one level deep.
    """
    if not text:
        return None

    # Match \boxed{content} with possible nested braces
    match = re.search(r'\\boxed\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}', text)
    if match:
        return match.group(1).strip()

    # Also try without backslash (some datasets may strip it)
    match = re.search(r'boxed\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}', text)
    if match:
        return match.group(1).strip()

    return None


def _extract_gsm8k_answer(text: str) -> str:
    """
    Extract the final answer from GSM8K format.

    GSM8K answers end with '#### <number>' or '#### <expression>'.
    """
    if not text:
        return ""

    # Look for #### marker
    match = re.search(r'####\s*(.+?)$', text, re.DOTALL)
    if match:
        return match.group(1).strip()

    # Fallback: return the last line
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    return lines[-1] if lines else ""


def _normalize_answer(answer: str) -> str:
    """
    Normalize an answer string to a canonical form.

    - Remove LaTeX formatting ($...$, \\text{}, etc.)
    - Strip whitespace
    - Convert known fraction forms
    """
    if not answer:
        return ""

    # Remove surrounding $ signs
    answer = answer.strip('$')

    # Remove \text{...} wrapper but keep content
    answer = re.sub(r'\\text\{([^}]*)\}', r'\1', answer)

    # Remove \frac{a}{b} -> a/b  (simple cases)
    answer = re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}', r'(\1)/(\2)', answer)

    # Remove \sqrt{...}
    answer = re.sub(r'\\sqrt\{([^{}]*)\}', r'sqrt(\1)', answer)

    # Remove \times -> *
    answer = answer.replace('\\times', '*')

    # Remove \, \; \quad (LaTeX spaces)
    answer = re.sub(r'\\[,;]?quad?', '', answer)

    # Remove leftover LaTeX commands
    answer = re.sub(r'\\[a-zA-Z]+(\{[^}]*\})*', '', answer)

    # Remove extra whitespace
    answer = re.sub(r'\s+', ' ', answer).strip()

    # Remove trailing period
    if answer.endswith('.'):
        answer = answer[:-1].strip()

    return answer
