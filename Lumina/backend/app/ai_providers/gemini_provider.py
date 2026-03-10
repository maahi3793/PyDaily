"""Gemini AI provider with model fallback support."""

from typing import Any

from app.ai_providers.base import AIProvider
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

# Fallback models in priority order
GEMINI_FALLBACK_MODELS = [
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-1.0-pro",
]


class GeminiProvider(AIProvider):
    """Google Gemini AI provider.

    Supports automatic fallback to alternative models on quota errors.
    """

    def __init__(self) -> None:
        import google.generativeai as genai

        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is not configured")

        genai.configure(api_key=settings.gemini_api_key)
        self._genai = genai
        self._model_name = settings.ai_model
        self._model = genai.GenerativeModel(self._model_name)

    @property
    def provider_name(self) -> str:
        return "gemini"

    @property
    def model_name(self) -> str:
        return self._model_name

    async def generate(self, prompt: str) -> Any:
        """Generate response with automatic model fallback on quota errors."""
        models_to_try = [self._model_name] + [
            m for m in GEMINI_FALLBACK_MODELS if m != self._model_name
        ]

        last_error: Exception | None = None

        for model_name in models_to_try:
            try:
                logger.info(
                    "Gemini generate request",
                    extra={"provider": "gemini", "model": model_name},
                )
                model = self._genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)

                logger.info(
                    "Gemini generate success",
                    extra={"provider": "gemini", "model": model_name},
                )
                return response.text

            except Exception as e:
                error_str = str(e).lower()
                last_error = e

                is_quota_error = any(
                    keyword in error_str
                    for keyword in ("quota", "rate limit", "429", "resource exhausted", "resourceexhausted")
                )

                if is_quota_error:
                    logger.warning(
                        f"Gemini quota error on model '{model_name}', trying fallback",
                        extra={
                            "provider": "gemini",
                            "model": model_name,
                            "error": str(e),
                            "error_type": "AI_QUOTA_ERROR",
                        },
                    )
                    continue
                else:
                    logger.error(
                        "Gemini non-quota error",
                        extra={
                            "provider": "gemini",
                            "model": model_name,
                            "error": str(e),
                        },
                    )
                    raise

        # All models exhausted
        logger.error(
            "All Gemini models exhausted",
            extra={"provider": "gemini", "error": str(last_error), "retries": len(models_to_try)},
        )
        raise last_error  # type: ignore[misc]
