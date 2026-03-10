import os
import chromadb
from chromadb.config import Settings
import logging
import time
from typing import List, Dict, Any, Tuple
from app.core.config import settings

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self):
        # Ensure the persistence directory exists
        os.makedirs(settings.CHROMADB_DIR, exist_ok=True)
        
        # Initialize standard local Chroma client
        self.client = chromadb.PersistentClient(path=settings.CHROMADB_DIR)
        
        # We'll use a single collection for all enterprise docs
        self.collection_name = "enterprise_docs"
        self.collection = self.client.get_or_create_collection(name=self.collection_name)
        logger.info(f"Connected to ChromaDB at {settings.CHROMADB_DIR}, Collection: {self.collection_name}")

    def insert_chunks(self, document_id: str, chunks: List[str], embeddings: List[List[float]], metadata: Dict[str, Any] = None) -> float:
        """
        Insert pre-embedded chunks into the vector store.
        Returns insertion latency in milliseconds.
        """
        if not chunks or not embeddings:
            raise ValueError("Chunks and embeddings cannot be empty")
            
        start_time = time.time()
        
        # Build IDs for each chunk
        ids = [f"{document_id}_chunk_{i}" for i in range(len(chunks))]
        
        # Assign parent metadata to each chunk so we can trace it back
        metadatas = []
        for i in range(len(chunks)):
            meta = metadata.copy() if metadata else {}
            meta.update({"document_id": document_id, "chunk_index": i})
            metadatas.append(meta)
            
        try:
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=chunks,
                metadatas=metadatas
            )
            latency_ms = (time.time() - start_time) * 1000
            logger.info(f"Inserted {len(chunks)} chunks for doc {document_id} in {latency_ms:.2f}ms")
            return latency_ms
        except Exception as e:
            logger.error(f"Failed to insert chunks into ChromaDB: {str(e)}")
            raise RuntimeError(f"ChromaDB insertion failed: {str(e)}")

    def search(self, query_embedding: List[float], n_results: int = 3) -> Tuple[List[str], List[float], float]:
        """
        Search for the most relevant chunks using the query embedding.
        Returns (documents, distances, latency_ms).
        """
        start_time = time.time()
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            
            # Extract lists from the single-query batch result
            documents = results.get("documents", [[]])[0]
            distances = results.get("distances", [[]])[0]
            
            latency_ms = (time.time() - start_time) * 1000
            return documents, distances, latency_ms
            
        except Exception as e:
            logger.error(f"Vector search failed: {str(e)}")
            raise RuntimeError(f"ChromaDB search failed: {str(e)}")

    def get_collection_stats(self) -> Dict[str, int]:
        """Return total number of vectors stored."""
        return {"count": self.collection.count()}

    def reset_collection(self):
        """DANGER: Drops and recreates the collection."""
        logger.warning(f"Resetting collection {self.collection_name}")
        self.client.delete_collection(self.collection_name)
        self.collection = self.client.get_or_create_collection(name=self.collection_name)
