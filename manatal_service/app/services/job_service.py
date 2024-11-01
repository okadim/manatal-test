# app/services/job_service.py

import json
from app.utils.extractors import extract_skills, extract_education, extract_experience, extract_responsibilities, normalize_education_levels
from sentence_transformers import SentenceTransformer
# Add imports
import faiss
import numpy as np


def load_jobs_from_json(file_path):
    with open(file_path, 'r') as file:
        try:
            data = json.load(file)
            return data.get("jobs", [])
        except json.JSONDecodeError:
            return []

def process_job(job_data):
    # Use existing extracted data if available
    job_title = job_data.get('job_title')
    skills = job_data.get('extracted_skills') or extract_skills(job_data.get('job_description', ''))
    education_required = job_data.get('extracted_education') or extract_education(job_data.get('job_description', ''))
    experience_required = job_data.get('extracted_experience') or extract_experience(job_data.get('job_description', ''))
    responsibilities = job_data.get('extracted_responsibilities') or extract_responsibilities(job_data.get('job_description', ''))

    # Normalize education levels
    normalized_education = normalize_education_levels(education_required)

    # Return a dictionary with extracted data
    return {
        'job_title': job_title, 
        'skills': skills,
        'education_required': normalized_education,
        'experience_required': experience_required,
        'responsibilities': responsibilities,
        'location': job_data.get('location', '').strip(),
        'employment_type': job_data.get('employment_type', '').strip()
    }


def prepare_job_text(requirements):
    parts = [
        f"Job Title: {requirements.get('job_title', '')}",
        f"Job Description: {requirements.get('job_description', '')}",
        f"Responsibilities: {', '.join(requirements.get('responsibilities', []))}",
        f"Required Skills: {', '.join(requirements.get('skills', []))}",
        f"Education Required: {', '.join(requirements.get('education_required', []))}",
        f"Experience Required: {requirements.get('experience_required', '0')} years",
        f"Location: {requirements.get('location', '')}",
        f"Employment Type: {requirements.get('employment_type', '')}"
    ]
    return '. '.join(parts)


def generate_job_embedding(job_text):
    print("Job text:", job_text)  # Debug print
    model = SentenceTransformer('all-distilroberta-v1')
    job_embedding = model.encode(job_text)
    job_embedding = np.array(job_embedding).reshape(1, -1)
    faiss.normalize_L2(job_embedding)
    return job_embedding


def process_and_store_job(job_id):
    # Load all jobs
    jobs = load_jobs_from_json('data/generated_job_postings.json')
    
    # Find the job with the specified job_id
    job_data = next((job for job in jobs if job.get("job_id") == job_id), None)
    
    if job_data is None:
        raise KeyError(f"Job with ID {job_id} not found.")
    
    # Process job data with extracted information if available
    processed_data = process_job(job_data)
    job_text = prepare_job_text(processed_data)
    
    # Generate embedding
    job_embedding = generate_job_embedding(job_text)
    
    # Return processed job and embedding
    return job_data, job_embedding


# Load jobs from JSON
def load_jobs_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data.get("jobs", [])

# Save jobs back to JSON
def save_jobs_to_json(file_path, jobs):
    with open(file_path, 'w') as file:
        json.dump({"jobs": jobs}, file, indent=4)


def update_job_data(job_id, updated_data, file_path='data/generated_job_postings.json'):
    # Load all jobs
    jobs = load_jobs_from_json(file_path)
    
    # Find the job and update the specific fields
    for job in jobs:
        if job["job_id"] == job_id:
            # Overwrite only the `extracted_*` fields
            job["extracted_skills"] = updated_data.get("extracted_skills", job["extracted_skills"])
            job["extracted_education"] = updated_data.get("extracted_education", job["extracted_education"])
            job["extracted_experience"] = updated_data.get("extracted_experience", job["extracted_experience"])
            job["extracted_responsibilities"] = updated_data.get("extracted_responsibilities", job["extracted_responsibilities"])
            break
    
    # Save the updated jobs back to JSON
    save_jobs_to_json(file_path, jobs)
