import logging
import time
from typing import List, Tuple
from sentence_transformers import SentenceTransformer
from app.core.config import settings

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self):
        self.model_name = settings.EMBEDDING_MODEL
        self.model = None
        self._load_model()
        
    def _load_model(self):
        """Lazy load the sentence transformer model to CPU."""
        start = time.time()
        logger.info(f"Loading embedding model: {self.model_name}...")
        try:
            # device='cpu' explicitly locks this to non-GPU execution for free local usage
            self.model = SentenceTransformer(self.model_name, device='cpu')
            logger.info(f"Model loaded in {time.time() - start:.2f}s")
        except Exception as e:
            logger.error(f"CRITICAL: Failed to load embedding model. {str(e)}")
            raise RuntimeError(f"Embedding model initialization failed: {str(e)}")

    def generate_embeddings(self, texts: List[str]) -> Tuple[List[List[float]], float]:
        """
        Generate embeddings for a list of text chunks.
        Returns the embeddings and the latency in milliseconds.
        """
        if not self.model:
            raise RuntimeError("Embedding model is not loaded.")
            
        start_time = time.time()
        try:
            # encode() returns a numpy array, convert to standard lists for Chroma
            embeddings_np = self.model.encode(texts, show_progress_bar=False)
            embeddings = embeddings_np.tolist()
            
            latency_ms = (time.time() - start_time) * 1000
            return embeddings, latency_ms
            
        except Exception as e:
            logger.error(f"Embedding generation failed: {str(e)}")
            raise RuntimeError(f"Failed to generate embeddings: {str(e)}")
