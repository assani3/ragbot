# RAG Portfolio Chatbot

A full-stack Retrieval-Augmented Generation (RAG) chatbot, deployed end to
end: a Flask API on Azure App Service, a React front-end on Azure Static
Web Apps with CI/CD via GitHub Actions, and OpenAI's API for embeddings
and generation.

**Live demo:** https://polite-hill-03d730a10.7.azurestaticapps.net/

It answers questions about my background and projects by retrieving
relevant context from a knowledge base using embeddings, then passing
that context to an LLM to generate a grounded answer — rather than
letting the model guess or hallucinate.

## How it works

1. `knowledge_base.txt` holds some facts about my projects and background,
   split into sections.
2. Each section is embedded using OpenAI's `text-embedding-3-small` model.
3. When a question comes in, it's embedded too, and compared against
   every chunk using cosine similarity.
4. The most relevant chunk(s) are inserted into the prompt as context.
5. `gpt-4o-mini` generates an answer grounded in that context.

```
User question
     │
     ▼
Embed question  ──────────────►  Compare to embedded knowledge base
     │                                    │ (cosine similarity)
     │                                    ▼
     │                          Top matching chunk(s)
     │                                    │
     ▼                                    ▼
              Chat completion (context + question)
                          │
                          ▼
                  Grounded answer
```

## Tech stack

| Layer            | Tech                                                      |
|------------------|-----------------------------------------------------------|
| LLM & embeddings | OpenAI API (`gpt-4o-mini`, `text-embedding-3-small`)      |
| Backend          | Python, Flask, Flask-CORS, Gunicorn                       |
| Retrieval        | NumPy (cosine similarity, in-memory vector store)         |
| Frontend         | React (Vite)                                              |
| Hosting          | Azure App Service (API), Azure Static Web Apps (frontend) |
| CI/CD            | GitHub Actions (auto-deploy on push, via Static Web Apps) |

## Architecture

```
┌──────────────────────┐         ┌───────────────────────┐
│   React front-end    │  HTTPS  │    Flask API          │
│   (Azure Static Web  │ ──────► │   (Azure App Service) │
│    Apps)             │         │                       │
└──────────────────────┘         └───────────┬───────────┘
      ▲                                      │
      │ auto-deploy on push                  │ calls
      │                                      ▼
┌──────────────────────┐         ┌───────────────────────┐
│   GitHub repo        │         │    OpenAI API         │
│   (GitHub Actions CI)│         │  (embeddings + chat)  │
└──────────────────────┘         └───────────────────────┘
```

## Project structure

```
rag-portfolio-bot/
├── knowledge_base.txt   # the "documents" the bot retrieves from
├── rag_core.py          # shared embedding + retrieval + generation logic
├── rag_chatbot.py        # command-line version
├── api_server.py         # Flask API deployed to Azure App Service
├── requirements.txt
└── frontend/              # React (Vite) chat interface, deployed to
    │                      # Azure Static Web Apps
    └── src/
        ├── App.jsx
        ├── App.css
        └── main.jsx
```

## Running it locally

**1. Install dependencies:**
```bash
pip install -r requirements.txt
```

**2. Set your OpenAI API key:**
```bash
# Mac/Linux
export OPENAI_API_KEY="your-key-here"

# Windows (PowerShell)
setx OPENAI_API_KEY "your-key-here"
```

**3a. Run the CLI version:**
```bash
python rag_chatbot.py
```

**3b. Or run the full local stack (Flask + React):**

By default, `frontend/src/App.jsx` points at the live Azure API, so the
front-end works locally with zero backend setup. If you'd rather run
your own local backend instead:

Terminal 1 — start the local API:
```bash
python api_server.py
```
Runs at `http://localhost:5001`.

Then update `API_URL` in `frontend/src/App.jsx` to
`http://localhost:5001/api/chat`.

Terminal 2 — start the React app:
```bash
cd frontend
npm install
npm run dev
```
Runs at `http://localhost:5173`.

Try asking:
- "What is SellersPoint built with?"
- "Tell me about EduLite"
- "What tech stack does Assani know?"
- "How does this bot work?"

## Deployment notes

- **API (Azure App Service):** Linux, Python 3.11, deployed via
  `az webapp up`. Runs through Gunicorn rather than Flask's dev server.
  `OPENAI_API_KEY` and `ALLOWED_ORIGIN` are set as Application Settings,
  never hardcoded. `SCM_DO_BUILD_DURING_DEPLOYMENT=true` is required so
  Azure actually installs `requirements.txt` during deploy — without it,
  dependencies silently don't get installed and the container crashes on
  startup with a `ModuleNotFoundError`.
- **Frontend (Azure Static Web Apps):** connected directly to this GitHub
  repo. Every push to `main` triggers an automatic build and deploy via
  GitHub Actions — no manual redeploy needed.
- **CORS:** the API's `ALLOWED_ORIGIN` setting must match the deployed
  front-end's exact URL, or the browser blocks requests with a CORS
  error even though the API itself is healthy.

## Design notes

- **In-memory vector store**: embeddings are computed once at startup and
  kept in a NumPy array rather than a database — appropriate for a small,
  static knowledge base. A production version would swap this for a real
  vector database.
- **Grounded, not open-ended**: the system prompt instructs the model to
  only answer from retrieved context and say "I don't know" otherwise,
  reducing hallucination.
- **Shared core logic**: `rag_core.py` holds all embedding/retrieval/
  generation code so both the CLI and the API call identical logic — no
  duplicated prompts or retrieval code to keep in sync.

## Next steps / roadmap

- Swap in-memory embeddings for a proper vector database (FAISS,
  Pinecone, or Azure AI Search)
- Add multi-turn conversation memory
- Add automated evaluation of answer quality against a test question set
- Move the Flask API into a container and explore Azure Container Apps

## About

Built by Assani, a Software Engineer based in Pretoria, South Africa,
BSc IT (Software Engineering), Eduvos.