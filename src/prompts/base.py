"""
Base class for all prompt methods.
"""


class PromptMethod:
    """
    Abstract base class for prompting strategies.

    Every prompt method must implement:
        - name: property returning the method identifier
        - format(problem, **kwargs): returns a formatted prompt string
    """

    def __init__(self, config: dict = None):
        self.config = config or {}

    @property
    def name(self) -> str:
        """Return the method name identifier."""
        raise NotImplementedError("Subclasses must define 'name' property")

    @property
    def is_multi_pass(self) -> bool:
        """Whether this method requires multiple inference passes."""
        return False

    def format(self, problem: str, **kwargs) -> str:
        """
        Format a math problem into the specific prompt template.

        Args:
            problem: The math problem text.
            **kwargs: Method-specific parameters.

        Returns:
            Formatted prompt string ready for model input.
        """
        raise NotImplementedError("Subclasses must implement format()")

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"
