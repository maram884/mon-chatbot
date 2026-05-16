import faiss
import numpy as np

class VectorStore:

    def __init__(self, embeddings):

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)

        self.index.add(np.array(embeddings).astype("float32"))

        self.documents = []

    def set_data(self, docs, sources):

        self.documents = list(zip(docs, sources))

    def search(self, query_embedding, k=3):

        distances, indices = self.index.search(
            np.array(query_embedding).astype("float32"),
            k
        )

        results = []

        for idx in indices[0]:

            if idx < len(self.documents):

                results.append(self.documents[idx])

        return results