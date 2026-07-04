"""
api_server.py
--------------
A small Flask API that wraps the RAG engine so the React front-end can
talk to it over HTTP.

Local setup:
    pip install -r requirements.txt
    export OPENAI_API_KEY="your-key-here"

Local run:
    python api_server.py

Azure App Service setup:
    Set these as Application Settings (Configuration > Application settings)
    in the Azure Portal, NOT hardcoded in this file:
      - OPENAI_API_KEY   = your real key
      - ALLOWED_ORIGIN    = the URL of your deployed React app,
                            e.g. https://your-app-name.azurestaticapps.net
    Azure sets the PORT environment variable automatically; this app reads
    it below.

The knowledge base is loaded and embedded once at startup (not on every
request), so the first request after startup may take a second or two,
but every request after that is fast.
"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from rag_core import RagEngine

app = Flask(__name__)

# In production, restrict CORS to your actual front-end URL via the
# ALLOWED_ORIGIN app setting. Falls back to "*" for local development.
allowed_origin = os.getenv("ALLOWED_ORIGIN", "*")
CORS(app, origins=[allowed_origin] if allowed_origin != "*" else "*")

engine = None  # loaded lazily on first request, see get_engine()


def get_engine() -> RagEngine:
    global engine
    if engine is None:
        engine = RagEngine()
    return engine


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    question = (data.get("question") or "").strip()

    if not question:
        return jsonify({"error": "Please include a 'question' in the request body."}), 400

    try:
        rag = get_engine()
        answer = rag.ask(question)
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: Set the OPENAI_API_KEY environment variable first.")
    else:
        port = int(os.environ.get("PORT", 5001))
        print(f"Starting API server on http://localhost:{port} ...")
        app.run(host="0.0.0.0", port=port, debug=True)