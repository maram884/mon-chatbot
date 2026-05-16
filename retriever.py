from embeddings import model

def retrieve(query, vector_store, k=3):

    query_embedding = model.encode([query])

    results = vector_store.search(query_embedding, k)

    return results