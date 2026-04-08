"""Tests for answer extraction module."""

import pytest
from src.evaluation.answer_extractor import extract_answer, extract_all_answers


class TestExtractAnswer:
    def test_boxed_answer(self):
        resp = "After solving, the answer is \\boxed{42}."
        assert extract_answer(resp) == "42"

    def test_boxed_nested(self):
        resp = "Therefore, \\boxed{\\frac{3}{4}}."
        assert extract_answer(resp) == "\\frac{3}{4}"

    def test_gsm8k_format(self):
        resp = "Let me solve this step by step...\n#### 15"
        assert extract_answer(resp) == "15"

    def test_the_answer_is(self):
        resp = "After calculation, the answer is 7."
        assert extract_answer(resp) == "7"

    def test_therefore(self):
        resp = "Step 1: ... Step 2: ... Therefore, 100"
        assert extract_answer(resp) == "100"

    def test_latex_inline(self):
        resp = "The result is $x = 5$."
        assert extract_answer(resp) == "x = 5"

    def test_equals_sign(self):
        resp = "Solving: x = 3"
        assert extract_answer(resp) == "3"

    def test_fallback_last_number(self):
        resp = "The calculation yields various results, and finally 99."
        assert extract_answer(resp) == "99"

    def test_empty_response(self):
        assert extract_answer("") is None
        assert extract_answer(None) is None

    def test_answer_extraction(self):
        resp = "The answer is \\boxed{5} and also #### 10."
        results = extract_all_answers(resp)
        assert len(results) >= 2


class TestExtractAllAnswers:
    def test_multiple_patterns(self):
        resp = "We get \\boxed{3} from the first method.\n#### 5"
        results = extract_all_answers(resp)
        assert "3" in results
        assert "5" in results

    def test_empty(self):
        assert extract_all_answers("") == []
