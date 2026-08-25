from pathlib import Path

from loguru import logger

from backend.core.config import settings


# =====================================================
# Log Directory
# =====================================================
LOG_FILE: Path = settings.LOG_DIR / "documind.log"


# =====================================================
# Configure Logger
# =====================================================
logger.remove()

# Console Logger
logger.add(
    sink=lambda msg: print(msg, end=""),
    level=settings.LOG_LEVEL,
    colorize=True,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    ),
)

# File Logger
logger.add(
    LOG_FILE,
    level=settings.LOG_LEVEL,
    rotation="10 MB",
    retention="14 days",
    compression="zip",
    encoding="utf-8",
    enqueue=True,
    format=(
        "{time:YYYY-MM-DD HH:mm:ss} | "
        "{level: <8} | "
        "{name}:{function}:{line} | "
        "{message}"
    ),
)


# =====================================================
# Export Logger
# =====================================================
app_logger = logger