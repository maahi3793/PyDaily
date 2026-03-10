"""Token estimation and chunk management for AI requests.

Prevents sending oversized payloads to AI providers.
Uses a word-count heuristic for token estimation.
"""

from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

# Rough heuristic: ~1 token per 0.75 words (or ~4 chars)
CHARS_PER_TOKEN = 4


def estimate_tokens(text: str) -> int:
    """Estimate the number of tokens in a text string.

    Uses a character-count heuristic: ~4 characters per token.
    This is intentionally conservative to avoid hitting limits.
    """
    return max(1, len(text) // CHARS_PER_TOKEN)


def chunk_text(text: str, max_tokens: int | None = None) -> list[str]:
    """Split text into chunks that fit within the token limit.

    Args:
        text: The text to chunk.
        max_tokens: Maximum tokens per chunk. Defaults to settings.max_chunk_tokens.

    Returns:
        List of text chunks, each within the token limit.
    """
    if max_tokens is None:
        max_tokens = settings.max_chunk_tokens

    estimated = estimate_tokens(text)

    if estimated <= max_tokens:
        return [text]

    max_chars = max_tokens * CHARS_PER_TOKEN
    chunks: list[str] = []

    # Split on paragraph boundaries first
    paragraphs = text.split("\n\n")
    current_chunk: list[str] = []
    current_size = 0

    for para in paragraphs:
        para_size = len(para)

        if current_size + para_size > max_chars and current_chunk:
            chunks.append("\n\n".join(current_chunk))
            current_chunk = []
            current_size = 0

        # If a single paragraph exceeds the limit, split on sentences
        if para_size > max_chars:
            sentences = para.replace(". ", ".\n").split("\n")
            for sentence in sentences:
                if current_size + len(sentence) > max_chars and current_chunk:
                    chunks.append("\n\n".join(current_chunk))
                    current_chunk = []
                    current_size = 0
                current_chunk.append(sentence)
                current_size += len(sentence)
        else:
            current_chunk.append(para)
            current_size += para_size

    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

    logger.info(
        "Text chunked",
        extra={
            "token_count": estimated,
            "chunk_count": len(chunks),
        },
    )
    return chunks


def prepare_for_ai(text: str, max_tokens: int | None = None) -> list[str]:
    """Prepare text for AI consumption by chunking if necessary.

    This is the main entry point for the token manager.
    Returns a list of chunks ready to send to an AI provider.
    """
    if not text or not text.strip():
        return []

    return chunk_text(text.strip(), max_tokens)
