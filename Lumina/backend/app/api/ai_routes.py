"""AI-related API routes.

POST /ai/summarize-section   — Summarize a section using AI
POST /ai/generate-questions  — Generate questions from a section

All AI endpoints use:
  - Token chunk manager
  - Response normalizer
  - Graceful error handling
"""

from fastapi import APIRouter, HTTPException

from app.ai_providers.factory import get_ai_provider
from app.database import get_section_by_id
from app.models.errors import ai_error, ai_not_configured, ai_quota_error, not_found
from app.models.schemas import AIGenerateQuestionsRequest, AIResponse, AISummarizeRequest
from app.services.normalizer import normalize_ai_response
from app.token_manager.chunk_manager import prepare_for_ai
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/ai", tags=["AI"])


def _get_text_from_request(section_id: int | None, text: str | None) -> str:
    """Resolve text content from either a section ID or direct text."""
    if text and text.strip():
        return text.strip()

    if section_id:
        section = get_section_by_id(section_id)
        if not section:
            raise HTTPException(status_code=404, detail=not_found("Section"))
        return section.get("content", "")

    raise HTTPException(
        status_code=400,
        detail={"error": True, "type": "VALIDATION_ERROR", "message": "Provide either section_id or text."},
    )


@router.post("/summarize-section", response_model=AIResponse)
async def summarize_section(request: AISummarizeRequest):
    """Summarize a section or provided text using the configured AI provider."""
    provider = get_ai_provider()
    if provider is None:
        raise HTTPException(status_code=503, detail=ai_not_configured())

    content = _get_text_from_request(request.section_id, request.text)
    if not content:
        raise HTTPException(
            status_code=400,
            detail={"error": True, "type": "VALIDATION_ERROR", "message": "No content to summarize."},
        )

    chunks = prepare_for_ai(content)
    results: list[str] = []

    for i, chunk in enumerate(chunks):
        prompt = (
            "Provide a clear, concise summary of the following technical content. "
            "Focus on key concepts, definitions, and important details:\n\n"
            f"{chunk}"
        )

        try:
            raw_response = await provider.generate(prompt)
            normalized = normalize_ai_response(raw_response)
            results.append(normalized)
            logger.info(
                f"Chunk {i + 1}/{len(chunks)} summarized",
                extra={"provider": provider.provider_name, "model": provider.model_name},
            )
        except Exception as e:
            error_str = str(e).lower()
            if any(k in error_str for k in ("quota", "rate limit", "429")):
                raise HTTPException(status_code=429, detail=ai_quota_error(str(e)))
            logger.error("AI summarize failed", extra={"error": str(e)})
            raise HTTPException(status_code=500, detail=ai_error(str(e)))

    return AIResponse(
        success=True,
        result="\n\n".join(results),
        model_used=provider.model_name,
        provider=provider.provider_name,
        chunks_processed=len(chunks),
    )


@router.post("/generate-questions", response_model=AIResponse)
async def generate_questions(request: AIGenerateQuestionsRequest):
    """Generate study questions from section content using AI."""
    provider = get_ai_provider()
    if provider is None:
        raise HTTPException(status_code=503, detail=ai_not_configured())

    content = _get_text_from_request(request.section_id, request.text)
    if not content:
        raise HTTPException(
            status_code=400,
            detail={"error": True, "type": "VALIDATION_ERROR", "message": "No content to generate questions from."},
        )

    chunks = prepare_for_ai(content)
    all_questions: list[str] = []

    questions_per_chunk = max(1, request.count // len(chunks)) if chunks else request.count

    for i, chunk in enumerate(chunks):
        prompt = (
            f"Generate exactly {questions_per_chunk} study questions based on the following "
            f"technical content. Format them as a numbered list:\n\n{chunk}"
        )

        try:
            raw_response = await provider.generate(prompt)
            normalized = normalize_ai_response(raw_response)
            all_questions.append(normalized)
            logger.info(
                f"Questions generated for chunk {i + 1}/{len(chunks)}",
                extra={"provider": provider.provider_name, "model": provider.model_name},
            )
        except Exception as e:
            error_str = str(e).lower()
            if any(k in error_str for k in ("quota", "rate limit", "429")):
                raise HTTPException(status_code=429, detail=ai_quota_error(str(e)))
            logger.error("AI question generation failed", extra={"error": str(e)})
            raise HTTPException(status_code=500, detail=ai_error(str(e)))

    return AIResponse(
        success=True,
        result="\n\n".join(all_questions),
        model_used=provider.model_name,
        provider=provider.provider_name,
        chunks_processed=len(chunks),
    )
