# RAG Portfolio Chatbot

A Retrieval-Augmented Generation (RAG) chatbot built with the OpenAI API,
with both a CLI and a React front-end. It answers questions about my
background and projects by retrieving relevant context from a knowledge
base using embeddings, then passing that context to an LLM to generate a
grounded answer.

## Why this project

Built as a hands-on demonstration of core RAG concepts — chunking,
embeddings, semantic similarity search, and grounded generation — using
the OpenAI API, plus a small full-stack layer (Flask API + React front-end)
around it.

## How it works

1. `knowledge_base.txt` holds facts about my projects and background, split
   into sections.
2. Each section is embedded using OpenAI's `text-embedding-3-small` model.
3. When you ask a question, it's embedded too, and compared against every
   chunk using cosine similarity.
4. The top matching chunk(s) are inserted into the prompt as context.
5. `gpt-4o-mini` generates an answer grounded in that context.

## Project structure

```
rag-portfolio-bot/
├── knowledge_base.txt   # the "documents" the bot retrieves from
├── rag_core.py          # shared embedding + retrieval + generation logic
├── rag_chatbot.py        # command-line version
├── api_server.py         # Flask API used by the React front-end
├── requirements.txt
└── frontend/              # React (Vite) chat interface
    └── src/
        ├── App.jsx
        └── App.css
```

## Setup

```bash
pip install -r requirements.txt

# Mac/Linux
export OPENAI_API_KEY="your-key-here"

# Windows (PowerShell)
setx OPENAI_API_KEY "your-key-here"
```

## Run the CLI version

```bash
python rag_chatbot.py
```

## Run the full-stack version (Flask + React)

Open two terminals.

**Terminal 1 — start the API:**
```bash
python api_server.py
```
This starts the backend at `http://localhost:5000`. The first request
after startup takes a second longer while the knowledge base is embedded.

**Terminal 2 — start the React app:**
```bash
cd frontend
npm install
npm run dev
```
This starts the front-end at `http://localhost:5173`. Open that URL in
your browser and start asking questions.

Try things like:
- "What is SellersPoint built with?"
- "Tell me about EduLite"
- "What tech stack does Assani know?"

## Next steps (roadmap)

- Swap in-memory embeddings for a proper vector database (e.g. FAISS,
  Pinecone, or Azure AI Search)
- Deploy the API in a container and host it on Azure
- Add conversation memory (multi-turn chat instead of one-off Q&A)

## For my CV / cover letter

> Built a full-stack Retrieval-Augmented Generation (RAG) chatbot: a
> Flask API using the OpenAI API for embeddings and generation, and a
> React front-end for the chat interface.
