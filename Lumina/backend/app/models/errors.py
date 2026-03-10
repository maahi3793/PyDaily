"""Pydantic error response models for consistent API error handling."""

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Standard error response returned by all API endpoints."""

    error: bool = True
    type: str
    message: str


# ── Common error types ──────────────────────────────────────────

def parsing_error(message: str) -> dict:
    return ErrorResponse(type="PARSING_ERROR", message=message).model_dump()


def ai_not_configured() -> dict:
    return ErrorResponse(
        type="AI_NOT_CONFIGURED",
        message="AI is not configured. Set API keys in .env to enable AI features.",
    ).model_dump()


def ai_quota_error(message: str = "AI provider quota exceeded. Try again later.") -> dict:
    return ErrorResponse(type="AI_QUOTA_ERROR", message=message).model_dump()


def ai_error(message: str) -> dict:
    return ErrorResponse(type="AI_ERROR", message=message).model_dump()


def validation_error(message: str) -> dict:
    return ErrorResponse(type="VALIDATION_ERROR", message=message).model_dump()


def not_found(resource: str = "Resource") -> dict:
    return ErrorResponse(type="NOT_FOUND", message=f"{resource} not found.").model_dump()
