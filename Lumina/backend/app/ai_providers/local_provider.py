"""Local model provider (Ollama-compatible via HTTP)."""

from typing import Any

from app.ai_providers.base import AIProvider
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class LocalProvider(AIProvider):
    """Local AI model provider compatible with Ollama's HTTP API.

    Sends requests to a locally running model server.
    """

    def __init__(self) -> None:
        if not settings.local_model_url:
            raise ValueError("LOCAL_MODEL_URL is not configured")

        self._url = settings.local_model_url
        self._model_name = settings.ai_model if settings.ai_model else "llama2"

    @property
    def provider_name(self) -> str:
        return "local"

    @property
    def model_name(self) -> str:
        return self._model_name

    async def generate(self, prompt: str) -> Any:
        """Generate a response from a local Ollama-compatible model."""
        try:
            import httpx

            logger.info(
                "Local model generate request",
                extra={"provider": "local", "model": self._model_name},
            )

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self._url,
                    json={
                        "model": self._model_name,
                        "prompt": prompt,
                        "stream": False,
                    },
                    timeout=120.0,
                )
                response.raise_for_status()
                data = response.json()

            text = data.get("response", "")
            logger.info(
                "Local model generate success",
                extra={"provider": "local", "model": self._model_name},
            )
            return text

        except Exception as e:
            logger.error(
                "Local model generate failed",
                extra={"provider": "local", "model": self._model_name, "error": str(e)},
            )
            raise
