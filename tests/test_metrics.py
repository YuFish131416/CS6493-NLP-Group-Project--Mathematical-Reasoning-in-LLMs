"""Tests for evaluation metrics module."""

import pytest
from src.evaluation.metrics import (
    compute_accuracy,
    compute_response_lengths,
    compute_token_efficiency,
    compute_extraction_success_rate,
)
from src.evaluation.math_parser import answers_match, normalize_answer


class TestNormalizeAnswer:
    def test_simple_number(self):
        assert normalize_answer("42") == "42"

    def test_latex_dollar(self):
        assert normalize_answer("$5$") == "5"

    def test_latex_frac(self):
        result = normalize_answer("\\frac{1}{2}")
        # sympy simplifies (1)/(2) to 0.5
        assert result in ["0.5", "0.500000000000000", "1/2"] or ("1" in result and "2" in result)

    def test_whitespace(self):
        assert normalize_answer("  7  ") == "7"

    def test_trailing_period(self):
        assert normalize_answer("5.") == "5"

    def test_empty(self):
        assert normalize_answer("") == ""


class TestAnswersMatch:
    def test_exact_match(self):
        assert answers_match("42", "42") is True

    def test_decimal_integer(self):
        assert answers_match("5.0", "5") is True

    def test_fraction_decimal(self):
        assert answers_match("1/2", "0.5") is True

    def test_mismatch(self):
        assert answers_match("100", "99") is False

    def test_empty(self):
        assert answers_match("", "5") is False
        assert answers_match("5", "") is False

    def test_negative(self):
        assert answers_match("-3", "-3") is True

    def test_whitespace_insensitive(self):
        assert answers_match(" 7 ", "7") is True


class TestComputeAccuracy:
    def test_perfect(self):
        assert compute_accuracy(["1", "2", "3"], ["1", "2", "3"]) == 1.0

    def test_zero(self):
        assert compute_accuracy(["1", "2", "3"], ["4", "5", "6"]) == 0.0

    def test_partial(self):
        assert compute_accuracy(["1", "2", "3"], ["1", "2", "9"]) == pytest.approx(2/3)

    def test_empty(self):
        assert compute_accuracy([], []) == 0.0

    def test_length_mismatch(self):
        with pytest.raises(ValueError):
            compute_accuracy(["1"], ["1", "2"])


class TestResponseLengths:
    def test_basic(self):
        result = compute_response_lengths(["hello", "world!"])
        assert result["mean"] == 5.5
        assert result["min"] == 5
        assert result["max"] == 6

    def test_empty(self):
        result = compute_response_lengths([])
        assert result["mean"] == 0


class TestTokenEfficiency:
    def test_basic(self):
        acc = [1, 0, 1, 0]
        tokens = [100, 200, 100, 200]
        result = compute_token_efficiency(acc, tokens)
        assert result["avg_accuracy"] == 0.5
        assert result["avg_tokens"] == 150

    def test_empty(self):
        result = compute_token_efficiency([], [])
        assert result["efficiency"] == 0


class TestExtractionSuccessRate:
    def test_all_success(self):
        rate = compute_extraction_success_rate([
            "The answer is \\boxed{5}",
            "#### 10",
            "The result is 7",
        ])
        assert rate == 1.0

    def test_partial(self):
        rate = compute_extraction_success_rate(["The answer is \\boxed{5}", "just some text with no numbers at all"])
        assert rate == 0.5

    def test_empty(self):
        assert compute_extraction_success_rate([]) == 0.0
