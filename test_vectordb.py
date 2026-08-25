from backend.vectordb.vectordb import VectorDB
from backend.core.config import settings

db = VectorDB()

db.reset()

db.add_chunks(
    settings.PROCESSED_DATA_DIR / "chunks.json"
)

print("Documents:", db.count())