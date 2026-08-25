from typing import List

import chromadb
import ollama

from backend.core.config import settings
from backend.core.logger import app_logger


class Retriever:
    """
    Retrieve the most relevant chunks from ChromaDB.
    """

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path=str(settings.CHROMA_DB_PATH)
        )

        self.collection = self.client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION_NAME
        )

        app_logger.success("Retriever initialized.")

    def search(
        self,
        question: str,
        top_k: int = 5,
    ) -> List[dict]:
        """
        Search similar chunks.
        """

        app_logger.info(f"Searching: {question}")

        embedding = ollama.embed(
            model=settings.EMBEDDING_MODEL,
            input=question,
        )["embeddings"][0]

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        retrieved = []

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances,
        ):
            retrieved.append(
                {
                    "text": document,
                    "title": metadata.get("title", ""),
                    "url": metadata.get("url", ""),
                    "chunk_index": metadata.get("chunk_index", 0),
                    "distance": float(distance),
                }
            )

        app_logger.success(
            f"Found {len(retrieved)} chunks."
        )

        return retrieved