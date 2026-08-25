from backend.retriever.retriever import Retriever

retriever = Retriever()

results = retriever.search("How to install Python?")

for i, result in enumerate(results, start=1):
    print("\n" + "=" * 80)
    print(f"Result {i}")

    print("Distance:", result.get("distance"))
    print("Title:", result.get("title"))
    print("URL:", result.get("url"))
    print()
    print(result.get("text"))