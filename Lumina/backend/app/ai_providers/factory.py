"""AI provider factory — selects provider based on environment config.

Returns None if no provider can be initialized (no keys configured).
The system must function fully without an AI provider.
"""

from typing import Optional

from app.ai_providers.base import AIProvider
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


def get_ai_provider() -> Optional[AIProvider]:
    """Create and return the configured AI provider, or None.

    Selection order:
    1. Use AI_PROVIDER env var to pick the provider class.
    2. Attempt to initialize it.
    3. If initialization fails (missing key), log and return None.

    Returns:
        An AIProvider instance, or None if AI is unavailable.
    """
    provider_name = settings.ai_provider.lower()

    try:
        if provider_name == "gemini":
            from app.ai_providers.gemini_provider import GeminiProvider
            provider = GeminiProvider()

        elif provider_name == "openai":
            from app.ai_providers.openai_provider import OpenAIProvider
            provider = OpenAIProvider()

        elif provider_name == "anthropic":
            from app.ai_providers.anthropic_provider import AnthropicProvider
            provider = AnthropicProvider()

        elif provider_name == "local":
            from app.ai_providers.local_provider import LocalProvider
            provider = LocalProvider()

        else:
            logger.warning(
                f"Unknown AI provider '{provider_name}', AI disabled",
                extra={"provider": provider_name},
            )
            return None

        logger.info(
            f"AI provider initialized: {provider.provider_name} ({provider.model_name})",
            extra={"provider": provider.provider_name, "model": provider.model_name},
        )
        return provider

    except ValueError as e:
        logger.info(
            f"AI provider '{provider_name}' not configured: {e}",
            extra={"provider": provider_name, "error": str(e)},
        )
        return None
    except Exception as e:
        logger.error(
            f"AI provider '{provider_name}' initialization failed: {e}",
            extra={"provider": provider_name, "error": str(e)},
        )
        return None
