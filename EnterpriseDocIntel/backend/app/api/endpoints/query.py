from fastapi import APIRouter, HTTPException, Depends
import time
import logging

from app.models.query import QueryRequest, QueryResponse
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
from app.services.llm_service import LLMService

logger = logging.getLogger(__name__)
router = APIRouter()

embedding_service = EmbeddingService()
vector_store = VectorStore()
llm_service = LLMService()

@router.post("/", response_model=QueryResponse)
async def process_query(request: QueryRequest, api_key: str = None):
    """
    Process a user query using Hybrid RAG:
    1. Embed query
    2. Search local ChromaDB for context
    3. Pass context + query to Gemini
    """
    # Use header or environment for key (simplified for this router)
    # In full enterprise, we'd use security dependencies
    
    try:
        # 1. Embed Query
        embeddings, emb_latency = embedding_service.generate_embeddings([request.query])
        query_embedding = embeddings[0]
        
        # 2. Vector Search (Retrieve Top 3 Chunks)
        documents, distances, search_latency = vector_store.search(query_embedding, n_results=3)
        
        if not documents:
            retrieved_context = "No relevant context found in the enterprise database."
            confidence = 0.0
            logger.warning("ChromaDB returned NO documents for this query.")
        else:
            # Combine retrieved chunks
            retrieved_context = "\n\n---\n\n".join(documents)
            # Distance: Lower is better in Chroma L2 space. Converting to a faux confidence score.
            confidence = max(0.0, 1.0 - (distances[0] if distances else 1.0))
            
            print(f"\n[DEBUG] ----- RETRIEVED CONTEXT FROM CHROMA -----")
            print(f"[DEBUG] Best Distance: {distances[0] if distances else 'N/A'}")
            print(f"{retrieved_context[:500]}...\n-----------------------------------------------\n")

        # 3. LLM Generation
        answer, token_usage, llm_latency = llm_service.generate_response(
            query=request.query,
            retrieved_context=retrieved_context,
            api_key=api_key,
            model_name=request.model
        )
        
        latency_breakdown = {
            "embedding_ms": round(emb_latency, 2),
            "retrieval_ms": round(search_latency, 2),
            "llm_ms": round(llm_latency, 2),
            "total_ms": round(emb_latency + search_latency + llm_latency, 2)
        }
        
        return QueryResponse(
            answer=answer,
            retrieved_context=retrieved_context,
            confidence_score=round(confidence, 4),
            usage=token_usage,
            latency_ms=latency_breakdown
        )
        
    except ValueError as ve:
        logger.error(f"Value Error during query: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Server Error during query: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error during LLM processing.")
