import chromadb

print("1")

# غیرفعال کردن telemetry تا ارور posthog رو نگیرید
client = chromadb.Client(settings=chromadb.Settings(anonymized_telemetry=False))

print("2")

# پاس دادن embedding_function=None تا اصلاً سراغ ONNX نره
collection = client.get_or_create_collection(
    name="test",
    embedding_function=None 
)

print("3")

try:
    collection.add(
        ids=["1"],
        embeddings=[[0.0] * 384],
        documents=["hello world"],
        metadatas=[{"title": "test"}]
    )
    print("4")
    print(collection.count())
    print("5")
except Exception as e:
    print(f"Error during add: {e}")
