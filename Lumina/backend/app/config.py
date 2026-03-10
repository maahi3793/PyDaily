"""Application configuration via Pydantic Settings."""

from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """LumiLearn application settings.

    All AI-related keys are optional — the system works fully without them.
    """

    # AI provider selection
    ai_provider: str = "gemini"
    ai_model: str = "gemini-1.5-flash"

    # API keys (all optional)
    gemini_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None

    # Local model
    local_model_url: str = "http://localhost:11434/api/generate"

    # Token management
    max_chunk_tokens: int = 2000

    # App paths
    upload_dir: str = "./uploads"
    database_url: str = "./lumilearn.db"
    log_level: str = "INFO"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }

    @property
    def upload_path(self) -> Path:
        path = Path(self.upload_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def db_path(self) -> Path:
        return Path(self.database_url)

    def ai_enabled(self) -> bool:
        """Check if the selected AI provider has a valid key configured."""
        provider = self.ai_provider.lower()
        if provider == "gemini":
            return bool(self.gemini_api_key)
        elif provider == "openai":
            return bool(self.openai_api_key)
        elif provider == "anthropic":
            return bool(self.anthropic_api_key)
        elif provider == "local":
            return bool(self.local_model_url)
        return False


settings = Settings()
