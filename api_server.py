"""
api_server.py
--------------
A small Flask API that wraps the RAG engine so the React front-end can
talk to it over HTTP.

Setup:
    pip install -r requirements.txt
    export OPENAI_API_KEY="your-key-here"

Run:
    python api_server.py

The knowledge base is loaded and embedded once at startup (not on every
request), so the first request after startup may take a second or two,
but every request after that is fast.
"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from rag_core import RagEngine

app = Flask(__name__)
CORS(app)  # allows the React dev server (different port) to call this API

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
        print("Starting API server on http://localhost:5000 ...")
        app.run(port=5001, debug=True)
