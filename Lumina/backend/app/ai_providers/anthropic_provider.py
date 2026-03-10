"""Anthropic provider (placeholder — requires API key to function)."""

from typing import Any

from app.ai_providers.base import AIProvider
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class AnthropicProvider(AIProvider):
    """Anthropic (Claude) API provider.

    Placeholder implementation — will work once ANTHROPIC_API_KEY is set
    and the `anthropic` package is installed.
    """

    def __init__(self) -> None:
        if not settings.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY is not configured")

        self._api_key = settings.anthropic_api_key
        self._model_name = settings.ai_model if "claude" in settings.ai_model else "claude-3-haiku-20240307"

    @property
    def provider_name(self) -> str:
        return "anthropic"

    @property
    def model_name(self) -> str:
        return self._model_name

    async def generate(self, prompt: str) -> Any:
        """Generate a response using Anthropic's messages API."""
        try:
            import httpx

            logger.info(
                "Anthropic generate request",
                extra={"provider": "anthropic", "model": self._model_name},
            )

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": self._api_key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json",
                    },
                    json={
                        "model": self._model_name,
                        "max_tokens": 1024,
                        "messages": [{"role": "user", "content": prompt}],
                    },
                    timeout=60.0,
                )
                response.raise_for_status()
                data = response.json()

            text = data.get("content", [{}])[0].get("text", "")
            logger.info(
                "Anthropic generate success",
                extra={"provider": "anthropic", "model": self._model_name},
            )
            return text

        except Exception as e:
            logger.error(
                "Anthropic generate failed",
                extra={"provider": "anthropic", "model": self._model_name, "error": str(e)},
            )
            raise
