"""AI response normalization layer.

All AI responses MUST pass through this before reaching API routes.
Prevents Pydantic validation crashes from unexpected provider formats.
"""

from typing import Any

from app.utils.logger import get_logger

logger = get_logger(__name__)


def normalize_ai_response(response: Any) -> str:
    """Normalize any AI provider response into a clean, human-readable string.

    Handles:
    - Plain strings
    - Dicts with common text keys (text, content, message, response, output)
    - Lists of strings or dicts
    - Nested provider-specific formats (e.g., Gemini's candidates)
    - None / unexpected types

    Returns:
        A clean string. Never returns a raw provider object.
    """
    try:
        if response is None:
            logger.warning("AI response was None")
            return ""

        if isinstance(response, str):
            return response.strip()

        if isinstance(response, dict):
            return _normalize_dict(response)

        if isinstance(response, list):
            return _normalize_list(response)

        # Fallback: try to get .text attribute (Gemini response objects)
        if hasattr(response, "text"):
            text = getattr(response, "text", None)
            if isinstance(text, str):
                return text.strip()

        # Last resort: stringify
        logger.warning(
            "AI response had unexpected type, stringifying",
            extra={"error_type": type(response).__name__},
        )
        return str(response).strip()

    except Exception as e:
        logger.error(
            "AI response normalization failed",
            extra={"error": str(e), "error_type": "NORMALIZATION_ERROR"},
        )
        return ""


def _normalize_dict(d: dict) -> str:
    """Extract readable text from a dict response."""
    # Check common keys in priority order
    for key in ("text", "content", "message", "response", "output", "result", "answer"):
        if key in d:
            val = d[key]
            if isinstance(val, str):
                return val.strip()
            if isinstance(val, list):
                return _normalize_list(val)
            if isinstance(val, dict):
                return _normalize_dict(val)

    # Gemini-style: candidates[0].content.parts[0].text
    if "candidates" in d:
        try:
            parts = d["candidates"][0]["content"]["parts"]
            texts = [p.get("text", "") for p in parts if isinstance(p, dict)]
            return "\n".join(texts).strip()
        except (IndexError, KeyError, TypeError):
            pass

    # OpenAI-style: choices[0].message.content
    if "choices" in d:
        try:
            return d["choices"][0]["message"]["content"].strip()
        except (IndexError, KeyError, TypeError):
            pass

    # Fallback: join all string values
    string_values = [str(v) for v in d.values() if isinstance(v, (str, int, float))]
    return " ".join(string_values).strip() if string_values else str(d)


def _normalize_list(lst: list) -> str:
    """Extract readable text from a list response."""
    parts: list[str] = []
    for item in lst:
        if isinstance(item, str):
            parts.append(item.strip())
        elif isinstance(item, dict):
            parts.append(_normalize_dict(item))
        else:
            parts.append(str(item))
    return "\n".join(parts).strip()
