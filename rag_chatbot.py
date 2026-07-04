"""
RAG Portfolio Chatbot (CLI)
----------------------------
Command-line version of the RAG chatbot. See rag_core.py for the shared
retrieval/generation logic, and api_server.py for the version that powers
the React front-end.

Setup:
    pip install -r requirements.txt
    export OPENAI_API_KEY="your-key-here"

Run:
    python rag_chatbot.py
"""

import os
from rag_core import RagEngine


def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: Set the OPENAI_API_KEY environment variable first.")
        return

    print("Loading and embedding knowledge base...")
    engine = RagEngine()
    print(f"Ready! Loaded {len(engine.chunks)} knowledge chunks.\n")

    print("Ask me anything about Assani's projects (type 'exit' to quit).\n")
    while True:
        question = input("You: ").strip()
        if question.lower() in ("exit", "quit"):
            break
        if not question:
            continue
        answer = engine.ask(question)
        print(f"Bot: {answer}\n")


if __name__ == "__main__":
    main()
