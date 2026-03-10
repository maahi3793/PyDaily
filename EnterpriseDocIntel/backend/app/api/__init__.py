from fastapi import APIRouter
from .endpoints import docs, query, analytics

api_router = APIRouter()
api_router.include_router(docs.router, prefix="/docs", tags=["documents"])
api_router.include_router(query.router, prefix="/query", tags=["queries"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
