from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class QueryRequest(BaseModel):
    query: str = Field(..., description="The user's question")
    model: str = Field(default="gemini-2.0-flash", description="The LLM to use for generation")

class TokenUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    estimated_cost_usd: float

class QueryResponse(BaseModel):
    answer: str
    retrieved_context: str
    confidence_score: float
    usage: TokenUsage
    latency_ms: Dict[str, float]
