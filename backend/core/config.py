from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# =====================================================
# Project Root Directory
# =====================================================
# backend/core/config.py
#               ↑
# parent.parent.parent -> DocuMind-AI
ROOT_DIR = Path(__file__).resolve().parents[2]
CHROMA_DB_PATH: Path = ROOT_DIR / "vectordb"



class Settings(BaseSettings):
    """
    Centralized application configuration.
    All values can be overridden from the .env file.
    """

    # =====================================================
    # Application
    # =====================================================
    APP_NAME: str = "DocuMind AI"
    APP_VERSION: str = "0.1.0"

    # =====================================================
    # Ollama
    # =====================================================
    OLLAMA_MODEL: str = "qwen2.5:7b"
    OLLAMA_URL: str = "http://localhost:11434"

    # =====================================================
    # Vector Database
    # =====================================================
    CHROMA_DB_PATH: Path = ROOT_DIR / "vectordb"

    CHROMA_COLLECTION_NAME: str = "documentation"

    EMBEDDING_MODEL: str = "all-minilm"

    # =====================================================
    # RAG
    # =====================================================
    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 150
    TOP_K: int = 5
    MIN_CHUNK_SIZE: int = 120

    # =====================================================
    # Crawling
    # =====================================================
    REQUEST_TIMEOUT: int = 20
    MAX_PAGES: int = 300
    MAX_DEPTH: int = 2

    USER_AGENT: str = (
        "DocuMindAI/1.0 "
        "(https://github.com/your-username/DocuMind-AI)"
    )

    DOC_SITES: dict[str, str] = {
        "python": "https://docs.python.org/3/",
        "numpy": "https://numpy.org/doc/",
        "sklearn": "https://scikit-learn.org/stable/",
    }

    # =====================================================
    # Logging
    # =====================================================
    LOG_LEVEL: str = "INFO"

    # =====================================================
    # Paths
    # =====================================================
    RAW_DATA_DIR: Path = ROOT_DIR / "data" / "raw"

    PROCESSED_DATA_DIR: Path = ROOT_DIR / "data" / "processed"

    LOG_DIR: Path = ROOT_DIR / "logs"

    # =====================================================
    # Pydantic Settings
    # =====================================================
    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


# Singleton Settings
settings = Settings()


# =====================================================
# Create Required Directories
# =====================================================
for directory in (
    settings.RAW_DATA_DIR,
    settings.PROCESSED_DATA_DIR,
    settings.LOG_DIR,
    settings.CHROMA_DB_PATH,
):
    directory.mkdir(parents=True, exist_ok=True)