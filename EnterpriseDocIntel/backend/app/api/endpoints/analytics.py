from fastapi import APIRouter
from app.services.vector_store import VectorStore

router = APIRouter()
vector_store = VectorStore()

@router.get("/stats")
async def get_system_stats():
    """Retrieve high-level statistics for the Analytics dashboard."""
    stats = vector_store.get_collection_stats()
    
    # In a full production system, token usage would be fetched from a SQL DB
    # For this architecture, we return mock summary data that the frontend chart will augment
    
    return {
        "vector_db_count": stats["count"],
        "system_health": "Healthy",
        "rag_efficiency_score": 0.92,  # 92% token reduction 
        "total_tokens_saved": 450000,
        "active_indices": 1
    }
