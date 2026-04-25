import faiss
import numpy as np

dimension = 384

index = faiss.IndexFlatL2(dimension)

doc_store = []

def add_embedding(embedding, metadata):
    vector = np.array([embedding]).astype('float32')
    index.add(vector)
    doc_store.append(metadata)


def search_embedding(query_embedding, k=5):
    query_vector = np.array([query_embedding]).astype('float32')
    distances, indices = index.search(query_vector, k)

    results = []
    for idx in indices[0]:
        if idx < len(doc_store):
            results.append(doc_store[idx])

    return results
