"""OpenAI provider (placeholder — requires API key to function)."""

from typing import Any

from app.ai_providers.base import AIProvider
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class OpenAIProvider(AIProvider):
    """OpenAI API provider.

    This is a functional placeholder — it will work when
    OPENAI_API_KEY is configured, but is not the default provider.
    """

    def __init__(self) -> None:
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is not configured")

        from openai import AsyncOpenAI

        self._client = AsyncOpenAI(api_key=settings.openai_api_key)
        self._model_name = settings.ai_model if "gpt" in settings.ai_model else "gpt-3.5-turbo"

    @property
    def provider_name(self) -> str:
        return "openai"

    @property
    def model_name(self) -> str:
        return self._model_name

    async def generate(self, prompt: str) -> Any:
        """Generate a response using OpenAI's chat completion API."""
        try:
            logger.info(
                "OpenAI generate request",
                extra={"provider": "openai", "model": self._model_name},
            )
            response = await self._client.chat.completions.create(
                model=self._model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            text = response.choices[0].message.content
            logger.info(
                "OpenAI generate success",
                extra={"provider": "openai", "model": self._model_name},
            )
            return text

        except Exception as e:
            logger.error(
                "OpenAI generate failed",
                extra={"provider": "openai", "model": self._model_name, "error": str(e)},
            )
            raise
