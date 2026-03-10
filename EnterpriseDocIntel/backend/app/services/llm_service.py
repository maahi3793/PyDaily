import os
import time
import logging
from typing import Dict, Any, Tuple
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.core.config import settings

logger = logging.getLogger(__name__)

class LLMService:
    @staticmethod
    def generate_response(query: str, retrieved_context: str, api_key: str, model_name: str) -> Tuple[str, Dict[str, int], float]:
        """
        Send the query and retrieved context to the selected LLM via LangChain.
        Returns (answer, token_usage_estimation, latency_ms).
        """
        if not api_key:
            raise ValueError(f"Missing API Key for model {model_name}. Provide it in settings.")
            
        start_time = time.time()
        
        system_prompt = (
            "You are an Enterprise AI Assistant. Your task is to accurately answer the user's question "
            "using ONLY the provided context retrieved from the firm's document repository. "
            "If the answer is not contained in the context, explicitly state: "
            "'I cannot answer this based on the provided enterprise documents.' "
            "Do NOT hallucinate or use outside knowledge. Keep answers professional, concise, and structured."
        )
        
        user_prompt = f"Context:\n{retrieved_context}\n\nQuestion:\n{query}"
        
        try:
            if model_name.startswith("gpt"):
                llm = ChatOpenAI(
                    model=model_name,
                    api_key=api_key,
                    temperature=0.1
                )
            else:
                llm = ChatGoogleGenerativeAI(
                    model=model_name,
                    google_api_key=api_key,
                    temperature=0.1,
                    convert_system_message_to_human=True,
                )
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = llm.invoke(messages)
            
            # Newer Gemini preview models sometimes return a list of content blocks instead of a string
            if isinstance(response.content, list):
                answer = "".join(
                    str(block.get("text", "")) if isinstance(block, dict) else str(block) 
                    for block in response.content
                )
            else:
                answer = str(response.content)
                
            latency_ms = (time.time() - start_time) * 1000
            
            # For accurate tracking, Langchain models sometimes return active usage metrics in response.response_metadata
            # But the heuristic works reliably across all models as a fallback
            total_prompt = system_prompt + user_prompt
            prompt_tokens_est = len(total_prompt) // 4
            completion_tokens_est = len(answer) // 4
            
            token_usage = {
                "prompt_tokens": prompt_tokens_est,
                "completion_tokens": completion_tokens_est,
                "total_tokens": prompt_tokens_est + completion_tokens_est,
                "estimated_cost_usd": (prompt_tokens_est + completion_tokens_est) * 0.0000001 # Rough heuristic
            }
            
            return answer, token_usage, latency_ms
            
        except Exception as e:
            logger.error(f"LLM generation failed: {str(e)}")
            error_str = str(e).lower()
            if "exhausted" in error_str or "quota" in error_str:
                raise ValueError("API Quota Exhausted. Update billing or key.")
            elif "429" in error_str:
                raise ValueError("Rate limit exceeded. Please wait and try again.")
            elif "API_KEY_INVALID" in error_str or "401" in error_str:
                raise ValueError("Unauthorized: Invalid API key.")
            else:
                raise RuntimeError(f"LLM Provider Error: {str(e)}")
