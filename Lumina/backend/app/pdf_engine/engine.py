"""PDF parsing orchestrator with automatic fallback."""

from app.pdf_engine.base import PDFParser
from app.pdf_engine.pymupdf_parser import PyMuPDFParser
from app.pdf_engine.pdfplumber_parser import PdfPlumberParser
from app.utils.logger import get_logger

logger = get_logger(__name__)


class PDFEngine:
    """Orchestrator that tries parsers in priority order.

    1. Try PyMuPDF (primary)
    2. On failure → log, try pdfplumber (secondary)
    3. If both fail → return structured error dict
    """

    def __init__(self) -> None:
        self._parsers: list[tuple[str, PDFParser]] = [
            ("pymupdf", PyMuPDFParser()),
            ("pdfplumber", PdfPlumberParser()),
        ]

    def parse(self, file_path: str) -> dict:
        """Attempt to parse a PDF, falling back through parsers.

        Returns:
            dict with keys:
                success (bool): Whether any parser succeeded.
                text (str): Extracted text (empty string on failure).
                parser_used (str | None): Name of the parser that succeeded.
                errors (list[str]): Error messages from failed parsers.
        """
        errors: list[str] = []

        for name, parser in self._parsers:
            try:
                pages_text, toc = parser.parse(file_path)
                logger.info(
                    "PDF parsed successfully",
                    extra={"parser": name, "file_path": file_path, "total_pages": len(pages_text), "toc_entries": len(toc)},
                )
                return {
                    "success": True,
                    "pages_text": pages_text,
                    "text": "\n\n".join(pages_text),
                    "toc": toc,
                    "parser_used": name,
                    "errors": errors,
                }
            except Exception as e:
                error_msg = f"{name}: {str(e)}"
                errors.append(error_msg)
                logger.warning(
                    f"Parser '{name}' failed, trying next",
                    extra={"parser": name, "file_path": file_path, "error": str(e)},
                )

        logger.error(
            "All PDF parsers failed",
            extra={"file_path": file_path, "error": "; ".join(errors)},
        )
        return {
            "success": False,
            "pages_text": [],
            "text": "",
            "toc": [],
            "parser_used": None,
            "errors": errors,
        }


# Module-level singleton
pdf_engine = PDFEngine()
