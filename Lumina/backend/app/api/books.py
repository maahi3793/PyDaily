"""Book and chapter API routes.

POST /upload       — Upload and parse a PDF
GET  /books        — List all books
GET  /books/{id}   — Get book detail with chapters
GET  /chapters/{id} — Get chapter with sections
"""

import os
import shutil
from pathlib import Path

from fastapi import APIRouter, File, UploadFile, HTTPException

from app.config import settings
from app.database import (
    get_all_books,
    get_book_by_id,
    get_chapter_by_id,
    insert_book,
    insert_chapter,
    insert_section,
)
from app.models.errors import not_found, parsing_error
from app.models.schemas import BookDetail, BookSummary, ChapterDetail, UploadResponse
from app.pdf_engine.engine import pdf_engine
from app.services.extractor import extract_structure
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """Upload a PDF, parse it, extract structure, and store in database."""
    # Validate file type
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail=parsing_error("Only PDF files are accepted."))

    # Save uploaded file
    upload_path = settings.upload_path / file.filename
    try:
        with open(upload_path, "wb") as f:
            contents = await file.read()
            f.write(contents)
        logger.info("File uploaded", extra={"file_path": str(upload_path)})
    except Exception as e:
        logger.error("File save failed", extra={"error": str(e)})
        raise HTTPException(status_code=500, detail=parsing_error(f"Failed to save file: {e}"))

    # Parse PDF
    result = pdf_engine.parse(str(upload_path))
    if not result["success"]:
        raise HTTPException(
            status_code=422,
            detail=parsing_error(
                f"Failed to parse PDF. Errors: {'; '.join(result['errors'])}"
            ),
        )

    raw_text = result["text"]
    parser_used = result["parser_used"]

    # Extract book title from filename
    book_title = Path(file.filename).stem.replace("_", " ").replace("-", " ").title()

    # Extract structured content
    structured = extract_structure(raw_text, book_title=book_title, pages_text=result["pages_text"], toc=result["toc"])

    # Store in database
    try:
        book_id = insert_book(book_title, file.filename, raw_text, structured)

        chapters_count = 0
        for ch in structured.get("chapters", []):
            # Combine section contents for chapter-level content
            chapter_content = "\n\n".join(
                s.get("content", "") for s in ch.get("sections", [])
            )
            chapter_id = insert_chapter(
                book_id, ch["chapter_number"], ch["title"], chapter_content
            )
            chapters_count += 1

            for order, sec in enumerate(ch.get("sections", [])):
                insert_section(
                    chapter_id,
                    sec.get("heading", "Untitled"),
                    sec.get("content", ""),
                    sec.get("code_blocks", []),
                    order,
                )

        logger.info(
            "Book stored successfully",
            extra={"book_id": book_id, "chapter_count": chapters_count},
        )

        return UploadResponse(
            success=True,
            book_id=book_id,
            title=book_title,
            chapters_count=chapters_count,
            parser_used=parser_used,
            message=f"Successfully parsed and stored '{book_title}' with {chapters_count} chapter(s).",
        )

    except Exception as e:
        logger.error("Database storage failed", extra={"error": str(e)})
        raise HTTPException(status_code=500, detail=parsing_error(f"Database error: {e}"))


@router.get("/books", response_model=list[BookSummary])
async def list_books():
    """Return a list of all uploaded books."""
    return get_all_books()


@router.get("/books/{book_id}")
async def get_book(book_id: int):
    """Return a single book with its chapter list."""
    book = get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail=not_found("Book"))
    return book


@router.get("/chapters/{chapter_id}")
async def get_chapter(chapter_id: int):
    """Return a chapter with its sections."""
    chapter = get_chapter_by_id(chapter_id)
    if not chapter:
        raise HTTPException(status_code=404, detail=not_found("Chapter"))
    return chapter
