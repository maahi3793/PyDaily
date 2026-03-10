"""Abstract base class for AI providers."""

from abc import ABC, abstractmethod
from typing import Any


class AIProvider(ABC):
    """Base interface for all AI provider implementations.

    Every concrete provider must implement `generate()`.
    """

    @abstractmethod
    async def generate(self, prompt: str) -> Any:
        """Generate a response for the given prompt.

        Args:
            prompt: The text prompt to send to the AI model.

        Returns:
            The raw response from the provider (will be normalized later).

        Raises:
            Exception: If the provider call fails.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the name of this provider for logging."""
        ...

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Return the model name used by this provider."""
        ...
