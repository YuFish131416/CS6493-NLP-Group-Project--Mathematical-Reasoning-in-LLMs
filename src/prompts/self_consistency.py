"""
Self-Consistency prompting.
Generates multiple independent responses and takes majority vote on the final answer.
"""

from collections import Counter
from typing import Optional
from .base import PromptMethod


class SelfConsistency(PromptMethod):
    """
    Self-Consistency prompting.

    Uses the same prompt as CoT but samples multiple responses (with temperature > 0)
    and selects the most common answer via majority vote.
    """

    SC_TEMPLATE = """Solve the following math problem step by step. Show your reasoning clearly and put your final answer in \\boxed{{}}.

Problem:
{problem}

Please reason step by step:"""

    def __init__(self, config: dict = None):
        super().__init__(config)
        self.n_samples = config.get("n_samples", 5) if config else 5

    @property
    def name(self) -> str:
        return "self_consistency"

    @property
    def is_multi_pass(self) -> bool:
        return True

    def format(self, problem: str, **kwargs) -> str:
        """
        Format problem (same as CoT — sampling is controlled at inference level).

        Args:
            problem: The math problem text.
        """
        return self.SC_TEMPLATE.format(problem=problem)

    def aggregate(self, responses: list, answers: Optional[list] = None) -> str:
        """
        Aggregate multiple responses via majority vote.

        Args:
            responses: List of full model response texts.
            answers: Optional pre-extracted answers. If provided, uses these
                     directly for voting. Otherwise, uses raw responses.

        Returns:
            The most common answer string.
        """
        if answers is None:
            answers = responses

        counter = Counter(answers)
        most_common = counter.most_common(1)
        if not most_common:
            return ""
        return most_common[0][0]
