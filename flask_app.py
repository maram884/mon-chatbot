"""
MediLearn — Flask App Complète
Fonctionnalités :
  - /api/status        : état du système
  - /api/chat          : réponse normale avec historique
  - /api/chat/stream   : streaming de la réponse (bonus)
  - /api/upload        : upload de PDF (bonus)
  - Mode éducatif — aucun diagnostic médical
"""

from flask import Flask, render_template, request, jsonify, Response, stream_with_context
import os, sys, json, time

# ── Importation modules métier ────────────────────────────
try:
    from data_loader import documents, sources
    from embeddings import get_embeddings
    from vector_store import VectorStore
    from agent import medilearn_agent, medilearn_agent_stream
except ImportError as e:
    print(f"❌ Erreur d'importation : {e}")
    print("Vérifiez que data_loader.py, embeddings.py, vector_store.py, agent.py sont présents.")
    sys.exit(1)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 32 * 1024 * 1024  # 32 Mo max upload

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploaded_pdfs")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ── Initialisation moteur RAG ─────────────────────────────
print("⚙️  Initialisation du moteur MediLearn...")
_ready = False
_error_msg = ""
vector_store_global = None

try:
    embeddings_data = get_embeddings(documents)
    vector_store_global = VectorStore(embeddings_data)
    vector_store_global.set_data(documents, sources)
    _ready = True
    print(f"✅ MediLearn prêt — {len(documents)} chunks chargés.")
except Exception as e:
    _error_msg = str(e)
    print(f"❌ Erreur initialisation : {e}")

# ── Routes ────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/status")
def status():
    if _ready:
        return jsonify({"ready": True, "chunks": len(documents)})
    return jsonify({"ready": False, "error": _error_msg or "Initialisation en cours…"})


@app.route("/api/chat", methods=["POST"])
def chat():
    """Réponse classique (non streamée) avec historique."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Requête invalide"}), 400

    question = data.get("question", "").strip()
    history  = data.get("history", [])   # liste de {role, content}

    if not question:
        return jsonify({"error": "Question vide"}), 400
    if not _ready or vector_store_global is None:
        return jsonify({"error": "Moteur non initialisé — réessayez dans quelques secondes."}), 503

    try:
        response = medilearn_agent(question, vector_store_global, history=history)
        return jsonify({"response": response, "status": "success"})
    except Exception as e:
        print(f"❌ Erreur chat : {e}")
        return jsonify({"error": "Erreur interne", "detail": str(e)}), 500


@app.route("/api/chat/stream", methods=["POST"])
def chat_stream():
    """Streaming SSE — bonus."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Requête invalide"}), 400

    question = data.get("question", "").strip()
    history  = data.get("history", [])

    if not question:
        return jsonify({"error": "Question vide"}), 400
    if not _ready or vector_store_global is None:
        def _err():
            yield f"data: {json.dumps({'error': 'Moteur non prêt'})}\n\n"
        return Response(stream_with_context(_err()), mimetype="text/event-stream")

    def generate():
        try:
            for chunk in medilearn_agent_stream(question, vector_store_global, history=history):
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"
            yield f"data: {json.dumps({'done': True})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        }
    )


@app.route("/api/upload", methods=["POST"])
def upload():
    """Upload d'un PDF et ré-indexation — bonus."""
    if "file" not in request.files:
        return jsonify({"error": "Aucun fichier reçu"}), 400

    f = request.files["file"]
    if not f.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Seuls les fichiers PDF sont acceptés"}), 400

    save_path = os.path.join(UPLOAD_FOLDER, f.filename)
    f.save(save_path)

    # Ré-indexation à chaud
    global vector_store_global, documents, sources, _ready
    try:
        from data_loader import load_pdf
        new_docs, new_srcs = load_pdf(save_path)
        documents.extend(new_docs)
        sources.extend(new_srcs)
        embeddings_data = get_embeddings(documents)
        vector_store_global = VectorStore(embeddings_data)
        vector_store_global.set_data(documents, sources)
        _ready = True
        return jsonify({
            "success": True,
            "message": f"'{f.filename}' indexé — {len(new_docs)} nouveaux chunks ajoutés.",
            "total_chunks": len(documents)
        })
    except Exception as e:
        return jsonify({"error": f"Erreur d'indexation : {str(e)}"}), 500


# ── Lancement ─────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000, use_reloader=False)