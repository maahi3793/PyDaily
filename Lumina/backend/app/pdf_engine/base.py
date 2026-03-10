"""Abstract base class for PDF parsers."""

from abc import ABC, abstractmethod


class PDFParser(ABC):
    """Base interface for all PDF parser implementations.

    Every concrete parser must implement `parse()` which accepts a
    file path and returns the extracted raw text as a string.
    """

    @abstractmethod
    def parse(self, file_path: str) -> tuple[list[str], list[list]]:
        """Parse a PDF file and return its raw text pages and native TOC.

        Args:
            file_path: Absolute path to the PDF file.

        Returns:
            Tuple of `(pages_text, toc)` where `pages_text` is `[str, str, ...]` and toc is `[[level, title, page], ...]`.

        Raises:
            Exception: If parsing fails for any reason.
        """
        raise NotImplementedError
