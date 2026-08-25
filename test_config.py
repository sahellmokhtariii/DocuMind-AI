from backend.core.config import settings

print("App Name:", settings.APP_NAME)
print("Version:", settings.APP_VERSION)

print("Model:", settings.OLLAMA_MODEL)
print("Ollama:", settings.OLLAMA_URL)

print("Top K:", settings.TOP_K)

print("Sites:")
for name, url in settings.DOC_SITES.items():
    print(f"  {name}: {url}")

print("Raw Dir:", settings.RAW_DATA_DIR)
print("Processed Dir:", settings.PROCESSED_DATA_DIR)
print("Vector DB:", settings.CHROMA_DB_PATH)
print("Logs:", settings.LOG_DIR)