from pathlib import Path

from backend.chunking.chunker import TextChunker
from backend.core.config import settings

chunker = TextChunker()

chunker.process_file(
    input_file=settings.RAW_DATA_DIR / "python_docs.json",
    output_file=settings.PROCESSED_DATA_DIR / "chunks.json",
)