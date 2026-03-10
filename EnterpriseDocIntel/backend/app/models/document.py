from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class DocumentUploadResponse(BaseModel):
    filename: str
    status: str
    message: str
    document_id: Optional[str] = None
    chunks_created: Optional[int] = 0
    error_details: Optional[str] = None

class DocumentMetadata(BaseModel):
    document_id: str
    filename: str
    chunk_count: int
    upload_date: float
    file_size_bytes: int
