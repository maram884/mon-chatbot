MediLearn — Assistant Médical Éducatif (RAG)
🏥 Présentation du projet

MediLearn est un assistant intelligent basé sur l’IA et la technologie RAG (Retrieval-Augmented Generation).
Il répond aux questions médicales en utilisant uniquement des sources fiables comme :

🏥 OMS (Organisation Mondiale de la Santé)
📘 HAS (Haute Autorité de Santé)
💊 Vidal
📚 PubMed (extensible)

sous forme des documents PDF locaux

👉 L’objectif est éducatif uniquement : comprendre les concepts médicaux, pas poser de diagnostic

🚀 Fonctionnalités

✔ Chatbot médical intelligent
✔ Recherche basée sur RAG (FAISS + embeddings)
✔ Réponses basées sur sources fiables
✔ Interface web simple (flask, html)
✔ Citations des sources (OMS, HAS, etc.)
✔ Filtrage des questions non médicales
✔ Mode éducatif sécurisé


🎯 Objectifs
Fournir des réponses médicales éducatives fiables
Implémenter un pipeline complet RAG
Permettre une recherche sémantique intelligente
Offrir une interface web simple via Flask
Garantir la sécurité et limiter les réponses hors domaine

⚙️ Technologies utilisées
Python 
Flask 
FAISS (recherche vectorielle)
SentenceTransformers (embeddings)
Groq API (LLM - Llama 3.1)
PyPDF (lecture des documents PDF)
NumPy


🧠 Architecture du système (RAG)
📄 Chargement des documents PDF
✂️ Découpage en chunks
🔢 Conversion en embeddings
🗄️ Indexation dans FAISS
🔍 Recherche des passages pertinents
🤖 Génération de réponse via LLM (Groq)
🌐 Affichage dans interface Flask

Structure du projet

MEDILEARN/
│
├── dataa/                # PDFs médicaux
├── embeddings.py         # Génération des embeddings
├── data_loader.py        # Chargement et chunking des PDFs
├── vector_store.py       # Base vectorielle FAISS
├── retriever.py          # Recherche sémantique
├── agent.py              # Agent RAG + LLM
├── tools.py              # Fonctions utilitaires
├── flask_app.py          # Interface web Flask
├── app.py                # Version CLI
├── config.py             # Configuration globale
├── requirements.txt      # Dépendances
└── templates/
    └── index.html        # Interface utilisateur



💬 Exemple d’utilisation
Question :
Quels sont les symptômes du diabète ?
Réponse :
🧠 Réponse basée sur des sources médicales fiables :

📌 OMS : Le diabète de type 2 est une maladie chronique liée à l'insuline.
📌 PubMed : Les symptômes incluent soif excessive et fatigue.

⚠️ Ceci est un outil éducatif, pas un diagnostic médical.

💬 Fonctionnement
L’utilisateur pose une question médicale
Le système cherche les passages pertinents dans les PDF
Un modèle LLM génère une réponse basée sur ce contexte
La réponse est affichée avec les sources

🔒 Sécurité
Filtrage des questions hors domaine médical
Réponses uniquement éducatives
Avertissement médical systématique :

⚠️ Ceci est un assistant éducatif et ne remplace pas un médecin

⚠️ Limites
Dépendance à la qualité des PDF
Pas de diagnostic médical réel
Peut générer des réponses approximatives
Limité aux documents fournis

🚀 Améliorations futures
Ajout de modèles médicaux spécialisés
Support multi-langue
Amélioration du ranking des documents
Interface plus avancée (React)
Base vectorielle cloud (Pinecone / Weaviate)

👥 Équipe
Maram El Arbi
Omar Ousleti
Ghofrane Nefzi

📅 Projet
Année : 2025–2026
Matière : Intelligence Artificielle Générative
Encadrant : Prof. Zouabi Nourane
Auteur



