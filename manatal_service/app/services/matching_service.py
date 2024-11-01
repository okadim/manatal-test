from app.services.job_service import process_and_store_job
from app.utils.extractors import extract_education, normalize_education_levels
import faiss
import numpy as np
import pickle

def find_top_candidates(job_id, k=5, exp_weight=0.1):
    # Process job data and get embedding and required years of experience
    job_data, job_embedding = process_and_store_job(job_id)
    required_skills = set(job_data.get("extracted_skills", []))
    required_experience = float(job_data.get("extracted_experience", 0))  # Required experience in years
    required_education = set(job_data.get("extracted_education", []))

    # Debug: Print required job details
    print(f"Job Skills: {required_skills}, Job Experience: {required_experience}, Job Education: {required_education}")

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
        similarity_score = float(distance)

        # Reasons initialization
        reasons = []

        # Skill match reason
        candidate_skills = set(candidate_metadata.get('skills', []))
        matched_skills = candidate_skills.intersection(required_skills)
        if matched_skills:
            reasons.append(f"Matched skills: {', '.join(matched_skills)}")
        
        # Debug: Print candidate skills and matched skills
        print(f"Candidate Skills: {candidate_skills}, Matched Skills: {matched_skills}")

        # Experience reason
        candidate_experience = candidate_metadata.get('experience_years', 0)
        experience_difference = abs(candidate_experience - required_experience)
        if experience_difference <= 1:
            reasons.append(f"Experience closely matches required experience ({candidate_experience} years)")

        # Debug: Print candidate experience and difference
        print(f"Candidate Experience: {candidate_experience}, Experience Difference: {experience_difference}")

        # Education match reason with flexible matching
        candidate_education = normalize_education_levels(candidate_metadata.get('education', []))
        matched_education = set(candidate_education).intersection(required_education)
        if matched_education:
            reasons.append(f"Education matches: {', '.join(matched_education)}")
        if matched_education:
            reasons.append(f"Education matches: {', '.join(matched_education)}")
        
        # Debug: Print candidate education and matched education
        print(f"Candidate Education: {candidate_education}, Matched Education: {matched_education}")

        # Role relevance reason
        candidate_roles = candidate_metadata.get('roles', [])
        relevant_roles = [role for role in candidate_roles if any(req in role for req in required_skills)]
        if relevant_roles:
            reasons.append(f"Relevant roles: {', '.join(relevant_roles)}")
        
        # Debug: Print candidate roles and relevant roles
        print(f"Candidate Roles: {candidate_roles}, Relevant Roles: {relevant_roles}")

        # Calculate experience score and combined score
        experience_score = 1 - min(experience_difference / max(required_experience, 1), 1)
        combined_score = (1 - exp_weight) * similarity_score + exp_weight * experience_score

        # Construct candidate dictionary
        candidate = {
            'rank': rank + 1,
            'email': candidate_id,
            'full_name': candidate_metadata['full_name'],
            'similarity_score': similarity_score,
            'experience_score': experience_score,
            'combined_score': combined_score,
            'skills': candidate_metadata.get('skills', []),
            'education': candidate_metadata.get('education', []),
            'experience_years': candidate_metadata.get('experience_years', 0),
            'roles': candidate_metadata.get('roles', []),
            'location': candidate_metadata.get('location', ''),
            'reasons': reasons  # Adding reasons for recommendation
        }
        top_candidates.append(candidate)

    # Sort candidates by combined score
    top_candidates = sorted(top_candidates, key=lambda x: x['combined_score'], reverse=True)

    return top_candidates[:k]
