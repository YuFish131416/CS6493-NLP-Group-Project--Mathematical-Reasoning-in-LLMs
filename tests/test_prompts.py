"""Tests for prompt method modules."""

import pytest
from src.prompts import CoT, SelfConsistency, SelfRefine, LeastToMost, PVP


SAMPLE_PROBLEM = "Find the value of x if 3x + 7 = 22."


class TestCoT:
    def test_name(self):
        assert CoT().name == "cot"

    def test_format_contains_problem(self):
        prompt = CoT().format(SAMPLE_PROBLEM)
        assert SAMPLE_PROBLEM in prompt

    def test_format_contains_cot_instruction(self):
        prompt = CoT().format(SAMPLE_PROBLEM)
        assert "step by step" in prompt.lower()

    def test_not_multi_pass(self):
        assert CoT().is_multi_pass is False


class TestSelfConsistency:
    def test_name(self):
        assert SelfConsistency().name == "self_consistency"

    def test_format(self):
        prompt = SelfConsistency().format(SAMPLE_PROBLEM)
        assert SAMPLE_PROBLEM in prompt

    def test_is_multi_pass(self):
        assert SelfConsistency().is_multi_pass is True

    def test_aggregate_majority(self):
        sc = SelfConsistency()
        answers = ["5", "5", "5", "7", "7"]
        result = sc.aggregate([""] * 5, answers)
        assert result == "5"

    def test_aggregate_tie(self):
        sc = SelfConsistency()
        answers = ["5", "7"]
        result = sc.aggregate([""] * 2, answers)
        # Counter.most_common returns first found in case of tie
        assert result in ["5", "7"]

    def test_n_samples_config(self):
        sc = SelfConsistency(config={"n_samples": 10})
        assert sc.n_samples == 10


class TestSelfRefine:
    def test_name(self):
        assert SelfRefine().name == "self_refine"

    def test_format_solve(self):
        prompt = SelfRefine().format(SAMPLE_PROBLEM)
        assert SAMPLE_PROBLEM in prompt

    def test_format_critique(self):
        sr = SelfRefine()
        prompt = sr.format_critique(SAMPLE_PROBLEM, "x = 5")
        assert SAMPLE_PROBLEM in prompt
        assert "x = 5" in prompt
        assert "critique" in prompt.lower() or "review" in prompt.lower()

    def test_format_refine(self):
        sr = SelfRefine()
        prompt = sr.format_refine(SAMPLE_PROBLEM, "x = 5", "Check arithmetic.")
        assert "improve" in prompt.lower() or "correct" in prompt.lower()

    def test_is_multi_pass(self):
        assert SelfRefine().is_multi_pass is True

    def test_max_rounds_config(self):
        sr = SelfRefine(config={"max_refine_rounds": 3})
        assert sr.max_rounds == 3


class TestLeastToMost:
    def test_name(self):
        assert LeastToMost().name == "least_to_most"

    def test_format_decompose(self):
        prompt = LeastToMost().format(SAMPLE_PROBLEM)
        assert SAMPLE_PROBLEM in prompt
        assert "sub" in prompt.lower() or "break" in prompt.lower()

    def test_format_with_subquestions(self):
        ltm = LeastToMost()
        prompt = ltm.format_with_subquestions(SAMPLE_PROBLEM, "1. What is 3x?\n2. What is 3x + 7?")
        assert SAMPLE_PROBLEM in prompt

    def test_parse_subquestions(self):
        ltm = LeastToMost()
        response = "1. Find 3x\n2. Solve 3x + 7 = 22\n3. Calculate x"
        subs = ltm.parse_subquestions(response)
        assert len(subs) >= 2

    def test_is_multi_pass(self):
        assert LeastToMost().is_multi_pass is True


class TestPVP:
    def test_name(self):
        assert PVP().name == "pvp"

    def test_format(self):
        prompt = PVP().format(SAMPLE_PROBLEM)
        assert SAMPLE_PROBLEM in prompt

    def test_contains_verification(self):
        prompt = PVP().format(SAMPLE_PROBLEM)
        assert "verif" in prompt.lower()

    def test_not_multi_pass(self):
        assert PVP().is_multi_pass is False

    def test_contains_step_check(self):
        prompt = PVP().format(SAMPLE_PROBLEM)
        assert "step" in prompt.lower()
        assert "correct" in prompt.lower() or "error" in prompt.lower()
