# app/utils/embedding.py

import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle

# Load the embedding model once and reuse it
model = SentenceTransformer('all-distilroberta-v1')
embedding_dim = model.get_sentence_embedding_dimension()

def generate_text_embedding(text):
    """Generate an embedding for a single text."""
    embedding = model.encode(text)
    embedding = np.array(embedding).astype('float32')
    faiss.normalize_L2(embedding.reshape(1, -1))
    return embedding

def batch_generate_embeddings(texts):
    """Generate embeddings for a batch of texts."""
    embeddings = model.encode(texts, show_progress_bar=True)
    embeddings = np.array(embeddings).astype('float32')
    faiss.normalize_L2(embeddings)
    return embeddings

def save_embeddings_to_faiss(embeddings, ids, metadata, index_file='data/candidate_faiss_index.bin', metadata_file='data/candidate_metadata.pkl'):
    """Save embeddings to FAISS and metadata to a pickle file."""
    # Create FAISS index
    index = faiss.IndexFlatIP(embedding_dim)  # Inner Product for Cosine Similarity
    index.add(embeddings)

    # Ensure the 'data' directory exists
    if not os.path.exists('data'):
        os.makedirs('data')

    # Save the index and metadata
    faiss.write_index(index, index_file)
    with open(metadata_file, 'wb') as f:
        pickle.dump({'ids': ids, 'metadata': metadata}, f)
