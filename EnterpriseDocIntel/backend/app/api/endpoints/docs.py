import os
import uuid
import time
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List

from app.models.document import DocumentUploadResponse
from app.services.document_parser import DocumentParser
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
from app.core.config import settings

router = APIRouter()

# Instantiate services
# In a real enterprise app, these might be injected via Depends()
embedding_service = EmbeddingService()
vector_store = VectorStore()

@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    chunk_size: int = Form(1000),
    chunk_overlap: int = Form(200)
):
    """
    Upload a document, parse text, chunk, embed, and store in ChromaDB.
    """
    if file.size and file.size > 20 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File too large. Max 20MB.")
        
    doc_id = str(uuid.uuid4())
    temp_path = f"{settings.CHROMADB_DIR}/temp_{file.filename}"
    
    try:
        # Save to temp
        with open(temp_path, "wb") as buffer:
            buffer.write(await file.read())
            
        # 1. Parse
        text = DocumentParser.parse(temp_path, file.filename)
        if not text.strip():
            raise ValueError("Document appears to be empty after parsing.")
            
        # 2. Chunk
        chunks = DocumentParser.chunk_text(text, chunk_size, chunk_overlap)
        
        # 3. Embed
        embeddings, emb_latency = embedding_service.generate_embeddings(chunks)
        
        # 4. Store
        metadata = {
            "filename": file.filename,
            "upload_time": time.time(),
            "source": "manual_upload"
        }
        db_latency = vector_store.insert_chunks(doc_id, chunks, embeddings, metadata)
        
        return DocumentUploadResponse(
            filename=file.filename,
            status="success",
            message=f"Successfully processed {len(chunks)} chunks in {emb_latency+db_latency:.2f}ms",
            document_id=doc_id,
            chunks_created=len(chunks)
        )
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@router.delete("/reset")
async def reset_database():
    """Admin endpoint to wipe the vector database."""
    vector_store.reset_collection()
    return {"status": "success", "message": "Database reset."}
