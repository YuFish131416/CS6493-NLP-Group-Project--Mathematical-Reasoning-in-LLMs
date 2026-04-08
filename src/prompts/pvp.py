"""
Progressive Verification Prompting (PVP) — Novel Method.
A prompting strategy that intersperses verification checkpoints within
the Chain-of-Thought reasoning process, forcing the model to self-check
each intermediate step before proceeding.
"""

from .base import PromptMethod


class PVP(PromptMethod):
    """
    Progressive Verification Prompting (PVP).

    Key innovation: After each reasoning step, the model is explicitly
    instructed to verify the correctness of that step before moving on.
    This decomposes the self-verification process into smaller, more
    manageable checks, reducing cognitive load and improving accuracy.

    Theoretical basis:
    - Decomposed verification reduces the chance of cascading errors
    - Intermediate checks force the model to maintain logical consistency
    - Self-correction at each step is more effective than post-hoc review
    """

    PVP_TEMPLATE = """Solve the following math problem. Follow these instructions carefully:

1. Break the problem into clear reasoning steps.
2. After EACH step, pause and verify:
   - Is this step logically correct?
   - Does it follow from the previous step?
   - Are there any arithmetic errors?
   If you find an error, correct it immediately before proceeding.
3. After all steps, perform a final review to verify the overall solution is consistent.
4. Put your final answer in \\boxed{{}}.

Problem:
{problem}

Begin solving with progressive verification:"""

    @property
    def name(self) -> str:
        return "pvp"

    @property
    def is_multi_pass(self) -> bool:
        return False

    def format(self, problem: str, **kwargs) -> str:
        """
        Format problem with Progressive Verification Prompting instructions.

        Args:
            problem: The math problem text.

        Returns:
            Prompt string with PVP verification instructions.
        """
        return self.PVP_TEMPLATE.format(problem=problem)
