import chromadb

client = chromadb.PersistentClient(path="./vectordb_test")

print("1")

collection = client.get_or_create_collection("documentation")

print("2")