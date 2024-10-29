from app.services.job_service import process_and_store_job
import faiss
import numpy as np
import pickle

def find_top_candidates(job_id, k=5):
    # Process job data and get embedding
    job_data, job_embedding = process_and_store_job(job_id)

    # Normalize job embedding
    job_embedding = np.array(job_embedding).astype('float32')
    faiss.normalize_L2(job_embedding.reshape(1, -1))

    # Load FAISS index and candidate metadata
    index = faiss.read_index('data/candidate_faiss_index.bin')
    with open('data/candidate_metadata.pkl', 'rb') as f:
        data = pickle.load(f)
        candidate_ids = data['ids']
        candidate_metadata_list = data['metadata']

    # Perform similarity search
    distances, indices = index.search(job_embedding.reshape(1, -1), k)
    indices = indices[0]
    distances = distances[0]

    top_candidates = []
    for rank, (idx, distance) in enumerate(zip(indices, distances)):
        candidate_metadata = candidate_metadata_list[idx]
        candidate_id = candidate_ids[idx]
        similarity_score = float(distance)  # Convert to Python float

        candidate = {
            'rank': rank + 1,
            'email': candidate_id,
            'full_name': candidate_metadata['full_name'],
            'similarity_score': similarity_score,  # Now it's a standard Python float
            'skills': candidate_metadata.get('skills', []),
            'education': candidate_metadata.get('education', []),
            'experience_years': candidate_metadata.get('experience_years', 0),
            'roles': candidate_metadata.get('roles', []),
            'location': candidate_metadata.get('location', '')
        }
        top_candidates.append(candidate)

    return top_candidates