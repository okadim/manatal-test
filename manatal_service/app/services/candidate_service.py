# app/services/candidate_service.py

import json
from tqdm import tqdm
from datetime import datetime
import os
import asyncio
from app.models.candidate import Candidate
from app.utils.embeddings import batch_generate_embeddings, save_embeddings_to_faiss

# Function to load candidates from multiple JSON files
def load_candidates_from_json(file_paths):
    candidates = []
    for file_path in file_paths:
        with open(file_path, 'r') as f:
            candidates.extend(json.load(f))
    return candidates

def process_candidates(candidates):
    processed_candidates = []
    for candidate_data in tqdm(candidates, desc="Processing Candidates"):
        candidate = Candidate(**candidate_data)
        processed_candidate = {
            "full_name": candidate.full_name,
            "email": candidate.email,
            "skills": candidate.skills,
            "education": [edu.degree for edu in candidate.education],
            "experience_years": candidate.experience_years,
            "roles": [exp.role for exp in candidate.experiences],
            "location": candidate.address
        }
        processed_candidates.append(processed_candidate)
    return processed_candidates

def prepare_candidate_text(candidate):
    parts = [
        #f"Name: {candidate['full_name']}",
        f"Skills: {', '.join(candidate['skills'])}",
        f"Education: {', '.join(candidate['education'])}",
        f"Experience: {candidate['experience_years']} years",
        f"Roles: {', '.join(candidate['roles'])}",
        f"Location: {candidate['location']}"
    ]
    return '. '.join(parts)

def generate_and_store_candidate_embeddings(processed_candidates):
    # Prepare data for embedding generation
    candidate_texts = [prepare_candidate_text(candidate) for candidate in processed_candidates]
    candidate_ids = [candidate['email'] for candidate in processed_candidates]
    candidate_metadata = processed_candidates

    # Generate embeddings using embedding.py
    embeddings = batch_generate_embeddings(candidate_texts)

    # Save embeddings and metadata to FAISS and pickle files
    save_embeddings_to_faiss(embeddings, candidate_ids, candidate_metadata)

# Your asynchronous function
async def process_and_store_candidates():
    file_paths = [
        "data/generated_candidates_chunk_1.json",
        "data/generated_candidates_chunk_2.json",
        "data/generated_candidates_chunk_3.json"
    ]
    
    # Load candidates from the 3 files
    candidates = load_candidates_from_json(file_paths)
    
    # Process the loaded candidates
    processed_candidates = process_candidates(candidates)
    
    # Generate and store embeddings asynchronously
    await asyncio.to_thread(generate_and_store_candidate_embeddings, processed_candidates)
    
    return "done"
