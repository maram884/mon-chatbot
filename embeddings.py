from sentence_transformers import SentenceTransformer
from config import MODEL_NAME

model = SentenceTransformer(MODEL_NAME)

def get_embeddings(texts):

    embeddings = model.encode(
        texts,
        show_progress_bar=True
    )

    return embeddings