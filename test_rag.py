from backend.rag.rag import RAG

rag = RAG()

answer = rag.ask(
    "How do I install Python?"
)

print("\n")
print("=" * 80)
print(answer)