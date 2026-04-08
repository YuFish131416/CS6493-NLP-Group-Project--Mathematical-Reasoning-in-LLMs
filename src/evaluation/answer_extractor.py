"""
Answer extraction from model responses.
Supports multiple common answer formats.
"""

import re
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Patterns to try in order of priority
EXTRACTION_PATTERNS = [
    (r'\\boxed\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}', 1),
    (r'####\s*(.+?)$', 1),
    (r'[Tt]he (?:final )?(?:answer|result) is[:\s]+([^\n.]+)', 1),
    (r'[Aa]nswer[:\s]+([^\n.]+)', 1),
    (r'[Tt]herefore,?\s+(?:the answer is\s+)?([^\n.]+)', 1),
    (r'[Tt]hus,?\s+(?:the answer is\s+)?([^\n.]+)', 1),
    (r'\$\s*([^\$]+?)\s*\$', -1),
    (r'=\s*([^\n\s,]+)\s*$', -1),
]


def extract_answer(response: str) -> Optional[str]:
    """
    Extract the final numeric/mathematical answer from a model response.

    Supported formats:
        - \\boxed{answer}
        - #### answer (GSM8K)
        - "The answer is X"
        - $X$ (LaTeX inline math, last occurrence)
        - "= X" at end of line
    """
    if not response or not response.strip():
        return None

    for pattern, group_idx in EXTRACTION_PATTERNS:
        matches = list(re.finditer(pattern, response, re.MULTILINE))
        if matches:
            if group_idx == -1:
                answer = matches[-1].group(1).strip()
            else:
                answer = matches[0].group(group_idx).strip()
            if answer:
                answer = _clean_extracted(answer)
                if answer:
                    logger.debug(f"Extracted answer: '{answer}' using pattern: {pattern}")
                    return answer

    # Fallback: last number in response
    numbers = re.findall(r'-?\d+\.?\d*', response)
    if numbers:
        last_num = numbers[-1]
        # Remove trailing period if it was captured as part of a sentence ending
        if last_num.endswith('.') and not re.search(r'\.\d', last_num):
            last_num = last_num[:-1]
        logger.debug(f"Extracted answer (fallback last number): '{last_num}'")
        return last_num

    logger.warning("Could not extract answer from response")
    return None


def extract_all_answers(response: str) -> list:
    """Extract all potential answers from a response for debugging."""
    answers = []
    for pattern, group_idx in EXTRACTION_PATTERNS:
        matches = list(re.finditer(pattern, response, re.MULTILINE))
        for match in matches:
            if group_idx == -1:
                ans = match.group(1).strip()
            else:
                ans = match.group(group_idx).strip()
            if ans:
                answers.append(_clean_extracted(ans))
    return answers


def _clean_extracted(answer: str) -> str:
    """Clean up an extracted answer string."""
    # Strip trailing punctuation (but preserve decimals like "3.14")
    answer = answer.strip()
    # Remove trailing punctuation chars that are clearly not part of a number
    while answer and answer[-1] in '.,;:!?' and not (answer[-1] == '.' and len(answer) > 1 and answer[-2].isdigit()):
        answer = answer[:-1].strip()
    answer = answer.strip('$').strip()
    answer = re.sub(r'\\text\{([^}]*)\}', r'\1', answer)
    answer = answer.strip()
    return answer
