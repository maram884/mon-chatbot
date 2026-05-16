import os
from PyPDF2 import PdfReader

# 1. Gestion dynamique du dossier
# On récupère le chemin du dossier où se trouve ce script (data.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Liste des noms de fichiers PDF
pdf_files = [
    "diabete.pdf", 
    "les maladie et risqueq.pdf", 
    "medical_knowledge_complete.pdf"
]

documents = []
sources = []

def extract_text_from_pdf(file_path):
    """Fonction pour extraire le texte d'un PDF."""
    try:
        reader = PdfReader(file_path)
        full_text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                # On ajoute un espace entre les pages pour éviter de coller les mots
                full_text += content + "\n"
        return full_text.strip()
    except Exception as e:
        print(f"Erreur lors de la lecture de {file_path}: {e}")
        return None

# 3. Remplissage automatique des listes
print("Démarrage du chargement des documents...")

for file_name in pdf_files:
    # On crée le chemin complet : dossier_du_script + nom_du_fichier
    full_path = os.path.join(current_dir, file_name)
    
    if os.path.exists(full_path):
        text = extract_text_from_pdf(full_path)
        if text:
            documents.append(text)
            sources.append(file_name)
            print(f"✅ Chargé : {file_name}")
        else:
            print(f"⚠️  Le fichier {file_name} est vide ou illisible.")
    else:
        # Si le fichier n'est pas trouvé, on affiche le chemin complet pour vous aider
        print(f"❌ Fichier manquant : {file_name}")
        print(f"   Cherché à l'emplacement : {full_path}")

print("-" * 30)
print(f"Chargement terminé : {len(documents)} documents prêts.")