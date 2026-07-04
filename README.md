# RAG Portfolio Chatbot

A minimal Retrieval-Augmented Generation (RAG) chatbot built with the OpenAI API.
It answers questions about my background and projects by retrieving relevant
context from a knowledge base using embeddings, then passing that context to
an LLM to generate a grounded answer.

## Why this project

Built as a hands-on demonstration of core RAG concepts — chunking, embeddings,
semantic similarity search, and grounded generation — using the OpenAI API.

## How it works

1. `knowledge_base.txt` holds facts about my projects and background, split
   into sections.
2. Each section is embedded using OpenAI's `text-embedding-3-small` model.
3. When you ask a question, it's embedded too, and compared against every
   chunk using cosine similarity.
4. The top matching chunk(s) are inserted into the prompt as context.
5. `gpt-4o-mini` generates an answer grounded in that context.

## Setup

```bash
pip install -r requirements.txt

# Mac/Linux
export OPENAI_API_KEY="your-key-here"

# Windows (PowerShell)
setx OPENAI_API_KEY "your-key-here"
```

## Run

```bash
python rag_chatbot.py
```

Then ask things like:
- "What is SellersPoint built with?"
- "Tell me about EduLite"
- "What tech stack does Assani know?"

## Next steps (roadmap)

- Swap in-memory embeddings for a proper vector database (e.g. FAISS,
  Pinecone, or Azure AI Search)
- Add a simple React front-end
- Deploy as a containerized API endpoint on Azure

## For my CV / cover letter

> Built a Retrieval-Augmented Generation (RAG) chatbot using the OpenAI API,
> implementing embedding-based semantic search to retrieve relevant context
> and generate grounded LLM responses.
