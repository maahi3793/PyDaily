"""SQLite database setup and connection management."""

import json
import sqlite3
from contextlib import contextmanager
from typing import Any, Generator

from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

_DB_PATH = str(settings.db_path)

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    filename TEXT NOT NULL,
    raw_text TEXT,
    structured_content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS chapters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    chapter_number INTEGER NOT NULL,
    title TEXT NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS sections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chapter_id INTEGER NOT NULL,
    heading TEXT NOT NULL,
    content TEXT,
    code_blocks TEXT DEFAULT '[]',
    section_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chapter_id) REFERENCES chapters(id) ON DELETE CASCADE
);
"""


@contextmanager
def get_db() -> Generator[sqlite3.Connection, None, None]:
    """Yield a database connection with row factory set."""
    conn = sqlite3.connect(_DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    """Create tables if they do not exist."""
    try:
        with get_db() as conn:
            conn.executescript(SCHEMA_SQL)
        logger.info("Database initialized", extra={"db_path": _DB_PATH})
    except Exception as e:
        logger.error("Database initialization failed", extra={"error": str(e)})
        raise


def insert_book(title: str, filename: str, raw_text: str, structured_content: dict) -> int:
    """Insert a book and return its ID."""
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO books (title, filename, raw_text, structured_content) VALUES (?, ?, ?, ?)",
            (title, filename, raw_text, json.dumps(structured_content)),
        )
        return cursor.lastrowid


def insert_chapter(book_id: int, chapter_number: int, title: str, content: str) -> int:
    """Insert a chapter and return its ID."""
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO chapters (book_id, chapter_number, title, content) VALUES (?, ?, ?, ?)",
            (book_id, chapter_number, title, content),
        )
        return cursor.lastrowid


def insert_section(chapter_id: int, heading: str, content: str, code_blocks: list, order: int) -> int:
    """Insert a section and return its ID."""
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO sections (chapter_id, heading, content, code_blocks, section_order) VALUES (?, ?, ?, ?, ?)",
            (chapter_id, heading, content, json.dumps(code_blocks), order),
        )
        return cursor.lastrowid


def get_all_books() -> list[dict[str, Any]]:
    """Retrieve all books (without raw_text for efficiency)."""
    with get_db() as conn:
        rows = conn.execute(
            "SELECT id, title, filename, created_at FROM books ORDER BY created_at DESC"
        ).fetchall()
        return [dict(row) for row in rows]


def get_book_by_id(book_id: int) -> dict[str, Any] | None:
    """Retrieve a single book with its chapters."""
    with get_db() as conn:
        book = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
        if not book:
            return None
        book_dict = dict(book)
        if book_dict.get("structured_content"):
            book_dict["structured_content"] = json.loads(book_dict["structured_content"])

        chapters = conn.execute(
            "SELECT id, chapter_number, title, created_at FROM chapters WHERE book_id = ? ORDER BY chapter_number",
            (book_id,),
        ).fetchall()
        book_dict["chapters"] = [dict(c) for c in chapters]
        return book_dict


def get_chapter_by_id(chapter_id: int) -> dict[str, Any] | None:
    """Retrieve a chapter with its sections."""
    with get_db() as conn:
        chapter = conn.execute("SELECT * FROM chapters WHERE id = ?", (chapter_id,)).fetchone()
        if not chapter:
            return None
        chapter_dict = dict(chapter)

        sections = conn.execute(
            "SELECT * FROM sections WHERE chapter_id = ? ORDER BY section_order",
            (chapter_id,),
        ).fetchall()
        section_list = []
        for s in sections:
            sd = dict(s)
            sd["code_blocks"] = json.loads(sd.get("code_blocks", "[]"))
            section_list.append(sd)
        chapter_dict["sections"] = section_list
        return chapter_dict


def get_section_by_id(section_id: int) -> dict[str, Any] | None:
    """Retrieve a single section."""
    with get_db() as conn:
        section = conn.execute("SELECT * FROM sections WHERE id = ?", (section_id,)).fetchone()
        if not section:
            return None
        sd = dict(section)
        sd["code_blocks"] = json.loads(sd.get("code_blocks", "[]"))
        return sd
