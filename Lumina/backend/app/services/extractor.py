"""Deterministic structured content extraction from raw PDF text.

No AI is used here — all extraction is regex/heuristic-based.
"""

import re
from typing import Any

from app.utils.logger import get_logger

logger = get_logger(__name__)

# ── Regex patterns ──────────────────────────────────────────────

# Matches "Chapter 1", "Chapter 12: Title", "CHAPTER 1 - Title", etc.
CHAPTER_RE = re.compile(
    r"^(?:chapter)\s+(\d+)\s*[:\-–—.]?\s*(.*)",
    re.IGNORECASE | re.MULTILINE,
)

# Matches section-like headings:
#   "1.2 Some Heading", "1.2.3 Some Heading", "Section 2: Heading"
SECTION_RE = re.compile(
    r"^(?:(?:\d+\.)+\d*\s+(.+)|(?:section)\s+\d+\s*[:\-–—.]?\s*(.+))",
    re.IGNORECASE | re.MULTILINE,
)

# Heuristic: ALL-CAPS lines of 4+ chars that aren't chapter titles → treat as headings
ALLCAPS_HEADING_RE = re.compile(r"^([A-Z][A-Z\s]{3,})$", re.MULTILINE)

# Code block detection: lines indented by 4+ spaces or a tab
CODE_BLOCK_RE = re.compile(r"((?:^(?:    |\t).+\n?)+)", re.MULTILINE)


def _detect_code_blocks(text: str) -> tuple[str, list[str]]:
    """Extract code blocks from text and return (cleaned_text, code_blocks)."""
    code_blocks: list[str] = []

    def _replacer(match: re.Match) -> str:
        block = match.group(1).strip()
        if len(block) > 20:  # Ignore tiny indented fragments
            code_blocks.append(block)
            return "\n[CODE_BLOCK]\n"
        return match.group(0)

    cleaned = CODE_BLOCK_RE.sub(_replacer, text)
    return cleaned, code_blocks


def _split_into_sections(chapter_text: str) -> list[dict[str, Any]]:
    """Split chapter text into sections using heading heuristics."""
    cleaned_text, code_blocks = _detect_code_blocks(chapter_text)
    code_idx = 0

    # Find all heading positions
    headings: list[tuple[int, str]] = []
    for m in SECTION_RE.finditer(cleaned_text):
        heading = (m.group(1) or m.group(2) or "").strip()
        if heading:
            headings.append((m.start(), heading))

    for m in ALLCAPS_HEADING_RE.finditer(cleaned_text):
        heading = m.group(1).strip().title()
        if heading and len(heading.split()) <= 8:
            headings.append((m.start(), heading))

    # Sort by position and deduplicate nearby headings
    headings.sort(key=lambda x: x[0])

    if not headings:
        # No sections detected — whole chapter is one section
        content = cleaned_text.strip()
        section_code: list[str] = []
        while "[CODE_BLOCK]" in content and code_idx < len(code_blocks):
            content = content.replace("[CODE_BLOCK]", "", 1)
            section_code.append(code_blocks[code_idx])
            code_idx += 1
        return [{"heading": "Content", "content": content, "code_blocks": section_code}]

    sections: list[dict[str, Any]] = []
    for i, (pos, heading) in enumerate(headings):
        end_pos = headings[i + 1][0] if i + 1 < len(headings) else len(cleaned_text)
        content = cleaned_text[pos:end_pos].strip()

        # Remove the heading line itself from content
        content_lines = content.split("\n", 1)
        content = content_lines[1].strip() if len(content_lines) > 1 else ""

        section_code = []
        while "[CODE_BLOCK]" in content and code_idx < len(code_blocks):
            content = content.replace("[CODE_BLOCK]", "", 1)
            section_code.append(code_blocks[code_idx])
            code_idx += 1

        sections.append({
            "heading": heading,
            "content": content,
            "code_blocks": section_code,
        })

    return sections


def _extract_via_toc(book_title: str, pages_text: list[str], toc: list[list]) -> dict[str, Any] | None:
    """Extract chapters using the PDF's native Table of Contents."""
    chapter_entries = []
    for item in toc:
        if len(item) < 3:
            continue
        title = str(item[1]).strip()
        page_num = int(item[2])
        
        match = re.match(r"^(?:chapter)\s+(\d+)\s*[:\-–—.]?\s*(.*)", title, re.IGNORECASE)
        if match:
            chapter_entries.append({
                "chapter_number": int(match.group(1)),
                "title": match.group(2).strip() or title,
                "start_page": page_num
            })
            
    if not chapter_entries:
        return None  # No valid chapters found in TOC, fallback to regex
        
    chapters: list[dict[str, Any]] = []
    
    for i, entry in enumerate(chapter_entries):
        # PyMuPDF TOC pages are 1-indexed
        start_idx = max(0, entry["start_page"] - 1)
        if i + 1 < len(chapter_entries):
            end_idx = max(0, chapter_entries[i+1]["start_page"] - 1)
        else:
            end_idx = len(pages_text)
            
        chapter_pages = pages_text[start_idx:end_idx]
        chapter_text = "\n\n".join(chapter_pages).strip()
        
        sections = _split_into_sections(chapter_text)
        chapters.append({
            "chapter_number": entry["chapter_number"],
            "title": entry["title"],
            "sections": sections
        })
        
    logger.info("Extraction via native TOC succeeded", extra={"book_id": book_title, "chapter_count": len(chapters)})
    return {
        "book_title": book_title,
        "chapters": chapters
    }


def extract_structure(
    raw_text: str, 
    book_title: str = "Untitled", 
    pages_text: list[str] | None = None, 
    toc: list[list] | None = None
) -> dict[str, Any]:
    """Convert raw PDF text into a structured book JSON.

    Returns a dict matching the schema:
    {
        "book_title": str,
        "chapters": [
            {
                "chapter_number": int,
                "title": str,
                "sections": [
                    { "heading": str, "content": str, "code_blocks": [str] }
                ]
            }
        ]
    }
    """
    logger.info("Starting structure extraction", extra={"book_id": book_title})

    # Try native TOC extraction first (Perfect accuracy)
    if pages_text and toc:
        toc_result = _extract_via_toc(book_title, pages_text, toc)
        if toc_result:
            return toc_result

    # Fallback to RegEx textual extraction (Heuristic)
    logger.info("Falling back to regex extraction", extra={"book_id": book_title})
    chapters: list[dict[str, Any]] = []
    chapter_matches = list(CHAPTER_RE.finditer(raw_text))

    valid_matches = []
    for match in chapter_matches:
        title = match.group(2).strip()
        # Heuristic: TOC entries often end with a page number preceded by dots or large spaces
        if bool(re.search(r'(?:\.\s*){2,}\d+$', title)) or bool(re.search(r'\s{3,}\d+$', title)):
            continue
        valid_matches.append(match)

    # Deduplicate chapters by keeping the last occurrence of each chapter number.
    # This automatically discards any remaining front-matter/TOC references
    # since the actual chapter content comes last in the PDF text flow.
    last_occurrences = {}
    for match in valid_matches:
        num = int(match.group(1))
        last_occurrences[num] = match
        
    valid_matches = sorted(last_occurrences.values(), key=lambda m: m.start())

    if not valid_matches:
        # No chapter markers found — treat entire text as single chapter
        logger.info("No chapter markers found — treating as single chapter")
        sections = _split_into_sections(raw_text)
        chapters.append({
            "chapter_number": 1,
            "title": book_title,
            "sections": sections,
        })
    else:
        for i, match in enumerate(valid_matches):
            chapter_num = int(match.group(1))
            chapter_title = match.group(2).strip() or f"Chapter {chapter_num}"

            start = match.start()
            end = valid_matches[i + 1].start() if i + 1 < len(valid_matches) else len(raw_text)
            chapter_text = raw_text[start:end]

            # Remove the chapter heading from the text body
            chapter_text = chapter_text[match.end() - start:].strip()

            sections = _split_into_sections(chapter_text)
            chapters.append({
                "chapter_number": chapter_num,
                "title": chapter_title,
                "sections": sections,
            })

    result = {
        "book_title": book_title,
        "chapters": chapters,
    }

    logger.info(
        "Structure extraction complete",
        extra={"book_id": book_title, "chapter_count": len(chapters)},
    )
    return result
