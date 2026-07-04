"""
RAG Portfolio Chatbot
----------------------
A minimal Retrieval-Augmented Generation (RAG) chatbot using the OpenAI API.

How it works:
1. Load a knowledge base (knowledge_base.txt) and split it into chunks.
2. Generate an embedding for each chunk using OpenAI's embedding model.
3. When the user asks a question, embed the question too.
4. Use cosine similarity to find the most relevant chunk(s).
5. Pass those chunks as context to a chat completion call, so the model
   answers using grounded information instead of guessing.

Setup:
    pip install openai numpy
    export OPENAI_API_KEY="your-key-here"     (Mac/Linux)
    setx OPENAI_API_KEY "your-key-here"        (Windows, then reopen terminal)

Run:
    python rag_chatbot.py
"""

import os
import numpy as np
from openai import OpenAI

client = OpenAI()  # reads OPENAI_API_KEY from environment automatically

EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"
KNOWLEDGE_BASE_FILE = "knowledge_base.txt"


def load_chunks(filepath: str) -> list[str]:
    """Split the knowledge base into chunks using the '###' section markers."""
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    raw_chunks = text.split("###")
    chunks = [c.strip() for c in raw_chunks if c.strip()]
    return chunks


def embed_texts(texts: list[str]) -> np.ndarray:
    """Get embeddings for a list of texts, returned as a numpy array."""
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    return np.array([item.embedding for item in response.data])


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    a_norm = a / np.linalg.norm(a, axis=1, keepdims=True)
    b_norm = b / np.linalg.norm(b)
    return a_norm @ b_norm


def retrieve_relevant_chunks(question: str, chunks: list[str],
                              chunk_embeddings: np.ndarray, top_k: int = 2) -> list[str]:
    question_embedding = embed_texts([question])[0]
    similarities = cosine_similarity(chunk_embeddings, question_embedding)
    top_indices = np.argsort(similarities)[::-1][:top_k]
    return [chunks[i] for i in top_indices]


def ask(question: str, chunks: list[str], chunk_embeddings: np.ndarray) -> str:
    relevant_chunks = retrieve_relevant_chunks(question, chunks, chunk_embeddings)
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


def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: Set the OPENAI_API_KEY environment variable first.")
        return

    print("Loading and embedding knowledge base...")
    chunks = load_chunks(KNOWLEDGE_BASE_FILE)
    chunk_embeddings = embed_texts(chunks)
    print(f"Ready! Loaded {len(chunks)} knowledge chunks.\n")

    print("Ask me anything about Assani's projects (type 'exit' to quit).\n")
    while True:
        question = input("You: ").strip()
        if question.lower() in ("exit", "quit"):
            break
        if not question:
            continue
        answer = ask(question, chunks, chunk_embeddings)
        print(f"Bot: {answer}\n")


if __name__ == "__main__":
    main()
