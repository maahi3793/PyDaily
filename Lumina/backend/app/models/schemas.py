"""Pydantic request/response schemas for API endpoints."""

from typing import Any, Optional

from pydantic import BaseModel


# ── Book schemas ────────────────────────────────────────────────

class BookSummary(BaseModel):
    id: int
    title: str
    filename: str
    created_at: str


class SectionResponse(BaseModel):
    id: int
    heading: str
    content: str
    code_blocks: list[str] = []
    section_order: int = 0


class ChapterSummary(BaseModel):
    id: int
    chapter_number: int
    title: str
    created_at: Optional[str] = None


class ChapterDetail(BaseModel):
    id: int
    book_id: int
    chapter_number: int
    title: str
    content: Optional[str] = None
    sections: list[SectionResponse] = []
    created_at: Optional[str] = None


class BookDetail(BaseModel):
    id: int
    title: str
    filename: str
    structured_content: Optional[dict[str, Any]] = None
    chapters: list[ChapterSummary] = []
    created_at: str


class UploadResponse(BaseModel):
    success: bool
    book_id: Optional[int] = None
    title: str
    chapters_count: int = 0
    parser_used: Optional[str] = None
    message: str


# ── AI schemas ──────────────────────────────────────────────────

class AISummarizeRequest(BaseModel):
    section_id: Optional[int] = None
    text: Optional[str] = None


class AIGenerateQuestionsRequest(BaseModel):
    section_id: Optional[int] = None
    text: Optional[str] = None
    count: int = 5


class AIResponse(BaseModel):
    success: bool
    result: str
    model_used: Optional[str] = None
    provider: Optional[str] = None
    chunks_processed: int = 0
