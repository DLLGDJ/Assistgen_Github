from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os

from ..infra.sqlite import default_db_path


@dataclass(frozen=True)
class AppSettings:
    db_path: Path
    conversation_store: str
    llm_provider: str
    llm_base_url: str
    llm_api_key: str
    llm_default_model: str
    llm_timeout_seconds: float


def load_settings() -> AppSettings:
    db_path = Path(os.getenv("ASSISTGEN_DB_PATH", str(default_db_path())))
    conversation_store = os.getenv("ASSISTGEN_CONVERSATION_STORE", "sqlite").strip().lower() or "sqlite"
    llm_provider = os.getenv("ASSISTGEN_LLM_PROVIDER", "mock").strip().lower() or "mock"
    llm_base_url = os.getenv("ASSISTGEN_LLM_BASE_URL", "").strip()
    llm_api_key = os.getenv("ASSISTGEN_LLM_API_KEY", "").strip()
    llm_default_model = os.getenv("ASSISTGEN_LLM_DEFAULT_MODEL", "deepseek-chat").strip() or "deepseek-chat"
    llm_timeout_seconds = float(os.getenv("ASSISTGEN_LLM_TIMEOUT_SECONDS", "60"))
    return AppSettings(
        db_path=db_path,
        conversation_store=conversation_store,
        llm_provider=llm_provider,
        llm_base_url=llm_base_url,
        llm_api_key=llm_api_key,
        llm_default_model=llm_default_model,
        llm_timeout_seconds=llm_timeout_seconds,
    )


