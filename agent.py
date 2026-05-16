from groq import Groq
from config import GROQ_API_KEY
from retriever import retrieve
from tools import (
    is_medical_question,
    safety_warning,
    format_context
)

# ─────────────────────────────────────────────────────────────
# Initialisation du client Groq
# ─────────────────────────────────────────────────────────────

client = Groq(api_key=GROQ_API_KEY)


# ─────────────────────────────────────────────────────────────
# Fonction principale MediLearn
# ─────────────────────────────────────────────────────────────

def medilearn_agent(question, vector_store, history=None):
    """
    Agent MediLearn :
    - Vérifie si la question est médicale
    - Recherche dans les PDFs (RAG)
    - Génère une réponse concise avec Groq
    """

    # Initialisation historique si absent
    if history is None:
        history = []

    # ── 1. Vérification question médicale ──────────────────
    if not is_medical_question(question):
        return (
            "❌ Désolé, je ne peux répondre qu'aux questions médicales "
            "(maladies, symptômes, traitements, prévention, médicaments)."
        )

    try:

        # ── 2. Recherche contexte RAG ───────────────────────
        context_data = retrieve(question, vector_store)

        if not context_data:
            return (
                "❌ Aucune information pertinente trouvée dans la base documentaire.\n\n"
                f"{safety_warning()}"
            )

        # Format du contexte pour l'IA
        context_text_for_ai = format_context(context_data)

        # ── 3. Construction historique conversation ─────────
        history_text = ""

        for msg in history[-5:]:
            role = msg.get("role", "")
            content = msg.get("content", "")

            if role == "user":
                history_text += f"Utilisateur : {content}\n"

            elif role == "assistant":
                history_text += f"Assistant : {content}\n"

        # ── 4. Prompt IA ────────────────────────────────────
        prompt = f"""
Tu es MediLearn, un assistant médical éducatif.

Règles importantes :
- Réponds uniquement avec les informations des documents.
- Réponse claire et concise.
- Maximum 4 phrases.
- Ne jamais inventer d'information.
- Ne jamais faire de diagnostic médical réel.
- Conseiller de consulter un médecin si nécessaire.

HISTORIQUE :
{history_text}

DOCUMENTS :
{context_text_for_ai}

QUESTION :
{question}

RÉPONSE :
"""

        # ── 5. Appel modèle Groq ────────────────────────────
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Tu es un assistant médical éducatif fiable, "
                        "professionnel et synthétique."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.1-8b-instant",
            temperature=0.2,
            max_tokens=300,
        )

        ai_answer = chat_completion.choices[0].message.content.strip()

        # ── 6. Nettoyage sources ────────────────────────────
        unique_sources = []

        for doc, source in context_data:
            if source not in unique_sources:
                unique_sources.append(source)

        sources_str = ", ".join(unique_sources)

        # ── 7. Réponse finale ───────────────────────────────
        final_output = (
            f"🧠 Analyse :\n{ai_answer}\n\n"
            f"📖 Sources : {sources_str}\n\n"
            f"{safety_warning()}"
        )

        return final_output

    except Exception as e:
        return f"❌ Erreur technique MediLearn : {str(e)}"


# ─────────────────────────────────────────────────────────────
# Streaming de réponse (pour Flask SSE)
# ─────────────────────────────────────────────────────────────

def medilearn_agent_stream(question, vector_store, history=None):
    """
    Version streaming de MediLearn.
    Envoie la réponse morceau par morceau.
    """

    response = medilearn_agent(question, vector_store, history)

    words = response.split()

    for word in words:
        yield word + " "