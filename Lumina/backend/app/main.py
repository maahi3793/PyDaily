"""LumiLearn — FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.books import router as books_router
from app.api.ai_routes import router as ai_router
from app.config import settings
from app.database import init_db
from app.utils.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="LumiLearn API",
    description="Technical PDF parser and AI-powered study tool",
    version="1.0.0",
)

# CORS — allow Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(books_router, tags=["Books"])
app.include_router(ai_router)


@app.on_event("startup")
async def startup():
    """Initialize database and log startup configuration."""
    init_db()
    ai_status = "enabled" if settings.ai_enabled() else "disabled (no API key)"
    logger.info(
        "LumiLearn API started",
        extra={
            "provider": settings.ai_provider,
            "model": settings.ai_model,
            "error": None,
        },
    )
    logger.info(f"AI status: {ai_status}")


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "app": "LumiLearn",
        "version": "1.0.0",
        "ai_enabled": settings.ai_enabled(),
        "disclaimer": "This tool is for personal use only. Users must own uploaded material.",
    }
