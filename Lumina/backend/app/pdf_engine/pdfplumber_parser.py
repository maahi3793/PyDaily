"""Fallback PDF parser using pdfplumber."""

from app.pdf_engine.base import PDFParser
from app.utils.logger import get_logger

logger = get_logger(__name__)


class PdfPlumberParser(PDFParser):
    """PDF parser backed by pdfplumber.

    Used as a fallback when PyMuPDF fails. pdfplumber uses a
    different extraction approach and may succeed on PDFs that
    PyMuPDF cannot handle.
    """

    def parse(self, file_path: str) -> tuple[list[str], list[list]]:
        """Extract text from a PDF using pdfplumber."""
        import pdfplumber

        logger.info("Parsing PDF with pdfplumber", extra={"parser": "pdfplumber", "file_path": file_path})
        try:
            pages: list[str] = []
            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages, start=1):
                    text = page.extract_text()
                    pages.append(text if text else "")

            if not any(p for p in pages):
                raise ValueError("pdfplumber extracted zero text from the document")

            logger.info(
                "pdfplumber parsing complete",
                extra={"parser": "pdfplumber", "file_path": file_path, "total_pages": len(pages)},
            )
            return pages, []

        except Exception as e:
            logger.error(
                "pdfplumber parsing failed",
                extra={"parser": "pdfplumber", "file_path": file_path, "error": str(e)},
            )
            raise
