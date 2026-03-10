"""Primary PDF parser using PyMuPDF (fitz)."""

from app.pdf_engine.base import PDFParser
from app.utils.logger import get_logger

logger = get_logger(__name__)


class PyMuPDFParser(PDFParser):
    """PDF parser backed by PyMuPDF.

    This is the primary (preferred) parser. It is generally
    faster and handles a wider range of PDF encodings.
    """

    def parse(self, file_path: str) -> tuple[list[str], list[list]]:
        """Extract text and TOC from a PDF using PyMuPDF."""
        import fitz  # PyMuPDF

        logger.info("Parsing PDF with PyMuPDF", extra={"parser": "pymupdf", "file_path": file_path})
        try:
            doc = fitz.open(file_path)
            toc = doc.get_toc()
            
            pages: list[str] = []
            for page_num, page in enumerate(doc, start=1):
                text = page.get_text("text").strip()
                pages.append(text)
            doc.close()

            if not any(p for p in pages):
                raise ValueError("PyMuPDF extracted zero text from the document")

            logger.info(
                "PyMuPDF parsing complete",
                extra={"parser": "pymupdf", "file_path": file_path, "total_pages": len(pages), "toc_entries": len(toc)},
            )
            return pages, toc

        except Exception as e:
            logger.error(
                "PyMuPDF parsing failed",
                extra={"parser": "pymupdf", "file_path": file_path, "error": str(e)},
            )
            raise
