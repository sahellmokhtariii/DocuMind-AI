import ollama

from backend.retriever.retriever import Retriever
from backend.core.logger import app_logger


class RAG:

    def __init__(self):

        self.retriever = Retriever()
        self.model = "qwen2.5:1.5b"

        app_logger.success("RAG initialized.")

    def build_context(self, documents):

        context = ""

        for i, doc in enumerate(documents, start=1):

            context += f"""
==================== Document {i} ====================

Title:
{doc["title"]}

Source:
{doc["url"]}

Content:
{doc["text"]}

"""

        return context

    def ask(self, question: str):

        app_logger.info(f"Question: {question}")

        documents = self.retriever.search(question)

        if len(documents) == 0:
            return "I couldn't find any relevant documentation."

        context = self.build_context(documents)

        prompt = f"""
You are a Retrieval-Augmented Generation (RAG) assistant.

Rules:
1. Answer ONLY from the provided documentation.
2. If the answer is not in the documentation, say:
"I couldn't find the answer in the provided documentation."
3. Do not invent information.
4. At the end include the document title as the source.

================ DOCUMENTATION ================

{context}

================ QUESTION ================

{question}

================ ANSWER ================
"""

        app_logger.info("Sending prompt to Qwen...")

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        answer = response["message"]["content"]

        app_logger.success("Answer generated.")

        return {
            "answer": answer,
            "sources": documents,
        }