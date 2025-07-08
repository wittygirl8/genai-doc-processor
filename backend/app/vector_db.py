from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_chunks(chunks):
    return model.encode(chunks)

def build_index(embeddings):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index

def semantic_search(query, index, chunks, top_k=3):
    q_vec = model.encode([query])
    D, I = index.search(np.array(q_vec), top_k)
    return [chunks[i] for i in I[0]]
