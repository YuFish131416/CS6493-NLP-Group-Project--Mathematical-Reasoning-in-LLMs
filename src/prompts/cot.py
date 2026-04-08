"""
Chain-of-Thought (CoT) prompting.
Classic approach: instruct the model to reason step by step.
"""

from .base import PromptMethod


class CoT(PromptMethod):
    """
    Chain-of-Thought prompting.

    Adds a "Let's think step by step" instruction to encourage
    the model to show its reasoning process before giving the answer.
    """

    COT_TEMPLATE = """Solve the following math problem step by step. Show your reasoning clearly and put your final answer in \\boxed{{}}.

Problem:
{problem}

Please reason step by step:"""

    @property
    def name(self) -> str:
        return "cot"

    def format(self, problem: str, **kwargs) -> str:
        """
        Format problem with Chain-of-Thought instructions.

        Args:
            problem: The math problem text.

        Returns:
            Prompt string with CoT instructions.
        """
        return self.COT_TEMPLATE.format(problem=problem)
