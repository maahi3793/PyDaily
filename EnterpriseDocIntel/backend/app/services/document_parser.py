import os
import fitz # PyMuPDF
import docx2txt
import logging

logger = logging.getLogger(__name__)

class DocumentParser:
    @staticmethod
    def parse_pdf(file_path: str) -> str:
        """Extract text from a PDF file."""
        text = ""
        try:
            # Using PyMuPDF (fitz) which is much more resilient to malformed PDFs than PyPDF2
            doc = fitz.open(file_path)
            for page in doc:
                extracted = page.get_text()
                if extracted:
                    text += extracted + "\n"
            doc.close()
        except Exception as e:
            logger.error(f"Failed to parse PDF {file_path}: {str(e)}")
            raise ValueError(f"Failed to extract text from PDF: {str(e)}")
        return text

    @staticmethod
    def parse_docx(file_path: str) -> str:
        """Extract text from a DOCX file."""
        try:
            text = docx2txt.process(file_path)
            return text
        except Exception as e:
            logger.error(f"Failed to parse DOCX {file_path}: {str(e)}")
            raise ValueError(f"Failed to extract text from DOCX: {str(e)}")

    @staticmethod
    def parse_txt(file_path: str) -> str:
        """Extract text from a plain TXT or code file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except UnicodeDecodeError:
            # Fallback for non-utf8 encodings sometimes found in logs
            with open(file_path, "r", encoding="latin-1") as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to read text file {file_path}: {str(e)}")
            raise ValueError(f"Failed to read text file: {str(e)}")

    @classmethod
    def parse(cls, file_path: str, filename: str) -> str:
        """Route to the correct parser based on extension."""
        ext = filename.lower().split(".")[-1]
        
        if ext == "pdf":
            return cls.parse_pdf(file_path)
        elif ext in ["doc", "docx"]:
            return cls.parse_docx(file_path)
        elif ext in ["txt", "md", "csv", "json", "py", "js", "java", "html"]:
            return cls.parse_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: .{ext}")

    @staticmethod
    def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list[str]:
        """
        Split text into overlapping chunks.
        Very simplistic word-based naive chunker for enterprise safety (no strange NLP edges).
        """
        words = text.split()
        chunks = []
        i = 0
        while i < len(words):
            chunk_words = words[i:i + chunk_size]
            chunks.append(" ".join(chunk_words))
            # Move forward by the chunk size MINUS the overlap
            # Ensure we always step forward by at least 1 to avoid infinite loops
            step = max(1, chunk_size - chunk_overlap)
            i += step
        return chunks
