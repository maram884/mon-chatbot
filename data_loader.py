import os
from pypdf import PdfReader
from config import CHUNK_SIZE

DATA_FOLDER = "dataa"

documents = []
sources = []

def split_text(text, chunk_size=CHUNK_SIZE):
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])

    return chunks

def extract_text_from_pdf(file_path):
    try:
        reader = PdfReader(file_path)

        full_text = ""

        for page in reader.pages:
            text = page.extract_text()

            if text:
                full_text += text + "\n"

        return full_text

    except Exception as e:
        print(f"Erreur PDF {file_path}: {e}")
        return ""

print("📄 Chargement des PDFs...")

for file in os.listdir(DATA_FOLDER):

    if file.endswith(".pdf"):

        path = os.path.join(DATA_FOLDER, file)

        text = extract_text_from_pdf(path)

        chunks = split_text(text)

        for chunk in chunks:
            documents.append(chunk)
            sources.append(file)

        print(f"✅ {file} chargé avec {len(chunks)} chunks")

print(f"\n📚 Total chunks : {len(documents)}")