"""
rag_core.py
-----------
Shared RAG logic: load the knowledge base, embed it, and answer questions.
Used by both rag_chatbot.py (CLI) and api_server.py (Flask API for the
React front-end).
"""

import os
import numpy as np
from openai import OpenAI

EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"
KNOWLEDGE_BASE_FILE = os.path.join(os.path.dirname(__file__), "knowledge_base.txt")

client = OpenAI()  # reads OPENAI_API_KEY from environment automatically


def load_chunks(filepath: str = KNOWLEDGE_BASE_FILE) -> list[str]:
    """Split the knowledge base into chunks using the '###' section markers."""
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    raw_chunks = text.split("###")
    return [c.strip() for c in raw_chunks if c.strip()]


def embed_texts(texts: list[str]) -> np.ndarray:
    """Get embeddings for a list of texts, returned as a numpy array."""
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    return np.array([item.embedding for item in response.data])


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    a_norm = a / np.linalg.norm(a, axis=1, keepdims=True)
    b_norm = b / np.linalg.norm(b)
    return a_norm @ b_norm


class RagEngine:
    """Loads the knowledge base once, then answers questions cheaply."""

    def __init__(self, filepath: str = KNOWLEDGE_BASE_FILE):
        self.chunks = load_chunks(filepath)
        self.chunk_embeddings = embed_texts(self.chunks)

    def retrieve(self, question: str, top_k: int = 2) -> list[str]:
        question_embedding = embed_texts([question])[0]
        similarities = cosine_similarity(self.chunk_embeddings, question_embedding)
        top_indices = np.argsort(similarities)[::-1][:top_k]
        return [self.chunks[i] for i in top_indices]

    def ask(self, question: str) -> str:
        relevant_chunks = self.retrieve(question)
        context = "\n\n".join(relevant_chunks)

        system_prompt = (
            "You are a helpful assistant answering questions about Assani's "
            "background and portfolio projects. Only use the provided context "
            "to answer. If the answer isn't in the context, say you don't know."
        )
        user_prompt = f"Context:\n{context}\n\nQuestion: {question}"

        response = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.choices[0].message.content
