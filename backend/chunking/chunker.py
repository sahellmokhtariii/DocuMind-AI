import json
from pathlib import Path

from backend.core.config import settings
from backend.core.logger import app_logger


class TextChunker:
    """
    Split documents into overlapping chunks.
    """

    def __init__(
        self,
        chunk_size: int = settings.CHUNK_SIZE,
        overlap: int = settings.CHUNK_OVERLAP,
        min_chunk_size: int = settings.MIN_CHUNK_SIZE,
    ):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.min_chunk_size = min_chunk_size

    # ----------------------------------------------------
    # Split Text
    # ----------------------------------------------------

    def split_text(self, text: str):

        if not text:
            return []

        chunks = []

        start = 0
        text_length = len(text)

        while start < text_length:

            end = start + self.chunk_size

            chunk = text[start:end].strip()

            if len(chunk) >= self.min_chunk_size:
                chunks.append(chunk)

            start += self.chunk_size - self.overlap

        return chunks

    # ----------------------------------------------------
    # Process Documents
    # ----------------------------------------------------

    def process_documents(self, documents):

        results = []

        chunk_id = 0

        for document in documents:

            pieces = self.split_text(document["text"])

            for idx, chunk in enumerate(pieces):

                results.append(
                    {
                        "chunk_id": chunk_id,
                        "document_title": document["title"],
                        "document_url": document["url"],
                        "section_title": document["title"],
                        "chunk_index": idx,
                        "text": chunk,
                    }
                )

                chunk_id += 1

        return results

    # ----------------------------------------------------
    # Process File
    # ----------------------------------------------------

    def process_file(
        self,
        input_file: Path,
        output_file: Path,
    ):

        app_logger.info(f"Loading: {input_file}")

        with open(input_file, "r", encoding="utf-8") as f:
            documents = json.load(f)

        chunks = self.process_documents(documents)

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(
                chunks,
                f,
                ensure_ascii=False,
                indent=2,
            )

        app_logger.success(
            f"Saved {len(chunks)} chunks -> {output_file}"
        )