"""
Math expression parsing and answer normalization.
Uses sympy for robust mathematical equivalence checking.
"""

import re
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def normalize_answer(answer: str) -> str:
    """
    Normalize a math answer to canonical form for comparison.

    Handles:
        - Whitespace normalization
        - Fraction forms (e.g., "1/2")
        - Decimal forms (e.g., "0.5")
        - LaTeX removal
        - Trailing zeros
        - Negation formats
    """
    if not answer:
        return ""

    # Strip whitespace
    answer = answer.strip()

    # Remove LaTeX formatting
    answer = answer.strip('$')
    answer = re.sub(r'\\text\{([^}]*)\}', r'\1', answer)
    answer = re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}', r'(\1)/(\2)', answer)
    answer = re.sub(r'\\sqrt\{([^{}]*)\}', r'sqrt(\1)', answer)
    answer = answer.replace('\\times', '*')
    answer = answer.replace('\\div', '/')
    answer = re.sub(r'\\[,;]?quad?', '', answer)
    answer = re.sub(r'\\[a-zA-Z]+', '', answer)
    answer = answer.replace('{', '').replace('}', '')

    # Handle percentage
    if answer.endswith('%'):
        try:
            val = float(answer[:-1].strip()) / 100
            answer = str(val)
        except ValueError:
            pass

    # Remove trailing period BEFORE sympy (avoids "5." becoming "5.00000000000000")
    if answer.endswith('.') and not answer.endswith('..'):
        answer = answer[:-1].strip()

    # Try sympy simplification
    answer = _try_sympy_simplify(answer)

    # Clean up
    answer = re.sub(r'\s+', ' ', answer).strip()
    if answer.endswith('.'):
        answer = answer[:-1].strip()

    return answer


def answers_match(pred: str, truth: str) -> bool:
    """
    Check if two answers are mathematically equivalent.

    First normalizes both answers, then tries:
    1. Direct string comparison
    2. Sympy expression evaluation
    3. Numeric comparison with tolerance

    Args:
        pred: Predicted answer string.
        truth: Ground truth answer string.

    Returns:
        True if answers are equivalent.
    """
    if not pred or not truth:
        return False

    pred_norm = normalize_answer(pred)
    truth_norm = normalize_answer(truth)

    if not pred_norm or not truth_norm:
        return False

    # Direct string match (case-insensitive)
    if pred_norm.lower() == truth_norm.lower():
        return True

    # Try numeric comparison
    try:
        pred_num = _to_number(pred_norm)
        truth_num = _to_number(truth_norm)
        if pred_num is not None and truth_num is not None:
            return abs(pred_num - truth_num) < 1e-6
    except (ValueError, TypeError):
        pass

    # Try sympy symbolic comparison
    try:
        from sympy import simplify, sympify
        pred_expr = simplify(sympify(pred_norm))
        truth_expr = simplify(sympify(truth_norm))
        return pred_expr == truth_expr
    except Exception:
        pass

    return False


def _try_sympy_simplify(expr: str) -> str:
    """Try to simplify an expression using sympy."""
    try:
        from sympy import simplify, sympify, Rational
        result = simplify(sympify(expr))
        # Convert Rational to string nicely
        if isinstance(result, Rational):
            return str(float(result)) if result.q != 1 else str(result.p)
        return str(result)
    except Exception:
        return expr


def _to_number(s: str) -> Optional[float]:
    """Try to convert a string to a float."""
    try:
        # Handle fraction notation like "3/4"
        if '/' in s and s.count('/') == 1:
            num, den = s.split('/')
            return float(num) / float(den)
        return float(s)
    except (ValueError, ZeroDivisionError):
        return None
