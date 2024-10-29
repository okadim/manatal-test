import json
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from datetime import datetime
import faiss
import numpy as np
import pickle
import os
import asyncio

def load_candidates_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        candidates = data
    return candidates

def extract_candidate_skills(skills_list):
    return skills_list

def extract_candidate_education(education_list):
    degrees = []
    for edu in education_list:
        degree = edu.get('degree', '')
        degrees.append(degree)
    return degrees

def calculate_experience_years(experiences):
    total_experience = 0
    for exp in experiences:
        start_date = exp.get('start_date')
        end_date = exp.get('end_date', 'Present')
        
        if end_date == 'Present':
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
        
        duration = (end_date_obj - start_date_obj).days / 365.25
        total_experience += duration
    return round(total_experience, 1)

def extract_candidate_roles(experiences):
    roles = [exp.get('role', '') for exp in experiences]
    return roles

def process_candidates(candidates):
    processed_candidates = []
    for candidate in tqdm(candidates, desc="Processing Candidates"):
        candidate_skills = extract_candidate_skills(candidate.get('skills', []))
        candidate_education = extract_candidate_education(candidate.get('education', []))
        candidate_experience_years = calculate_experience_years(candidate.get('experiences', []))
        candidate_roles = extract_candidate_roles(candidate.get('experiences', []))
        
        processed_candidate = {
            "full_name": f"{candidate['first_name']} {candidate['last_name']}",
            "email": candidate.get('email', ''),
            "skills": candidate_skills,
            "education": candidate_education,
            "experience_years": candidate_experience_years,
            "roles": candidate_roles,
            "location": candidate.get('address', '')
        }
        processed_candidates.append(processed_candidate)
    return processed_candidates

def prepare_candidate_text(candidate):
    parts = [
        f"Name: {candidate['full_name']}",
        f"Skills: {', '.join(candidate['skills'])}",
        f"Education: {', '.join(candidate['education'])}",
        f"Experience: {candidate['experience_years']} years",
        f"Roles: {', '.join(candidate['roles'])}",
        f"Location: {candidate['location']}"
    ]
    return '. '.join(parts)

def generate_and_store_candidate_embeddings(processed_candidates):
    model = SentenceTransformer('all-distilroberta-v1')
    embedding_dim = model.get_sentence_embedding_dimension()

    # Prepare data for FAISS
    candidate_texts = []
    candidate_ids = []
    candidate_metadata = []

    for candidate in tqdm(processed_candidates, desc="Preparing Candidate Embeddings"):
        candidate_text = prepare_candidate_text(candidate)
        candidate_texts.append(candidate_text)
        candidate_ids.append(candidate['email'])
        candidate_metadata.append(candidate)

    # Generate embeddings
    embeddings = model.encode(candidate_texts, show_progress_bar=True)
    embeddings = np.array(embeddings).astype('float32')

    # Normalize embeddings for cosine similarity
    faiss.normalize_L2(embeddings)

    # Build FAISS index
    index = faiss.IndexFlatIP(embedding_dim)  # Using Inner Product for Cosine Similarity
    index.add(embeddings)

    # Ensure the 'data' directory exists
    if not os.path.exists('data'):
        os.makedirs('data')

    # Save the index and metadata
    faiss.write_index(index, 'data/candidate_faiss_index.bin')

    with open('data/candidate_metadata.pkl', 'wb') as f:
        pickle.dump({'ids': candidate_ids, 'metadata': candidate_metadata}, f)


async def process_and_store_candidates():
    file_path = "data/generated_candidates.json"
    candidates = load_candidates_from_json(file_path)
    processed_candidates = process_candidates(candidates)

    # Simulate async behavior by wrapping synchronous operations in asyncio
    await asyncio.to_thread(generate_and_store_candidate_embeddings, processed_candidates)
    return "done"
