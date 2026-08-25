import json
from pathlib import Path

from sentence_transformers import SentenceTransformer

from backend.core.config import settings
from backend.core.logger import app_logger


class EmbeddingGenerator:
    """
    Generate embeddings for document chunks.
    """

    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):

        app_logger.info(f"Loading embedding model: {model_name}")

        self.model = SentenceTransformer(model_name)

        app_logger.success("Embedding model loaded.")

    def embed_text(self, text: str):

        return self.model.encode(
            text,
            normalize_embeddings=True
        )

    def process_file(
        self,
        input_file: Path,
        output_file: Path,
    ):

        app_logger.info(f"Loading chunks: {input_file}")

        with open(input_file, "r", encoding="utf-8") as f:
            chunks = json.load(f)

        results = []

        for chunk in chunks:

            embedding = self.embed_text(chunk["text"])

            results.append(
                {
                    **chunk,
                    "embedding": embedding.tolist()
                }
            )

        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w", encoding="utf-8") as f:

            json.dump(
                results,
                f,
                ensure_ascii=False,
                indent=2
            )

        app_logger.success(
            f"Saved embeddings: {len(results)} chunks"
        )