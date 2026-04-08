"""
Least-to-Most prompting.
Decomposes complex problems into simpler sub-problems, then solves them sequentially.
"""

from typing import Optional, List
from .base import PromptMethod


class LeastToMost(PromptMethod):
    """
    Least-to-Most prompting.

    Two-phase approach:
    1. Decompose: Break the complex problem into simpler sub-questions.
    2. Solve Sequentially: Answer each sub-question, feeding answers
       as context for subsequent sub-questions.
    """

    DECOMPOSE_TEMPLATE = """Break down the following math problem into simpler sub-questions. List them in order from simplest to most complex. Each sub-question should build on the previous ones.

Problem:
{problem}

List the sub-questions:"""

    SOLVE_TEMPLATE = """Here is a math problem and its decomposition into sub-questions:
Problem: {problem}

Sub-questions:
{sub_questions}

Solve each sub-question in order. Use the answer from each sub-question to help solve the next one. Put your final answer in \\boxed{{}}.

Please solve step by step:"""

    @property
    def name(self) -> str:
        return "least_to_most"

    @property
    def is_multi_pass(self) -> bool:
        return True

    def format(self, problem: str, **kwargs) -> str:
        """
        Format problem for decomposition.

        Args:
            problem: The math problem text.
        """
        sub_questions = kwargs.get("sub_questions")
        if sub_questions:
            return self.SOLVE_TEMPLATE.format(
                problem=problem,
                sub_questions=sub_questions,
            )
        return self.DECOMPOSE_TEMPLATE.format(problem=problem)

    def format_with_subquestions(self, problem: str, sub_questions: str) -> str:
        """
        Format problem with pre-decomposed sub-questions for solving.

        Args:
            problem: The original math problem.
            sub_questions: The decomposed sub-questions as a formatted string.
        """
        return self.SOLVE_TEMPLATE.format(
            problem=problem, sub_questions=sub_questions
        )

    def parse_subquestions(self, decomposition_response: str) -> List[str]:
        """
        Parse the model's decomposition response into a list of sub-questions.

        Attempts to extract numbered or bulleted items.

        Args:
            decomposition_response: Model output from the decomposition prompt.

        Returns:
            List of sub-question strings.
        """
        import re
        lines = decomposition_response.strip().split('\n')
        sub_questions = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            # Remove numbering/bullets: "1.", "1)", "- ", "* ", "1. ", etc.
            cleaned = re.sub(r'^[\d\.\)\-\*\s]+', '', line).strip()
            if cleaned and len(cleaned) > 3:
                sub_questions.append(cleaned)
        return sub_questions if sub_questions else [decomposition_response.strip()]
