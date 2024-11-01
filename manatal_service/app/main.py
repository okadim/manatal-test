from fastapi import FastAPI, HTTPException, BackgroundTasks
from app.models.job import Job
from app.models.extracted_job import ExtractedData
from app.services.candidate_service import process_and_store_candidates
from app.services.matching_service import find_top_candidates
from app.services.job_service import load_jobs_from_json, process_job, save_jobs_to_json, update_job_data
import os

app = FastAPI()

# Initialize candidates when the app starts (asynchronously)
@app.on_event("startup")
async def startup_event():
    if not os.path.exists('data/candidate_faiss_index.bin') or not os.path.exists('data/candidate_metadata.pkl'):
        # Run candidate processing in the background to avoid blocking the startup
        background_tasks = BackgroundTasks()
        background_tasks.add_task(process_and_store_candidates)
        await background_tasks()


# Endpoint to create a new job
@app.post("/jobs/create")
async def create_job(job: Job, background_tasks: BackgroundTasks):
    file_path = 'data/generated_job_postings.json'
    jobs = load_jobs_from_json(file_path)

    new_job_id = len(jobs) + 1
    job_data = job.dict()
    job_data['job_id'] = new_job_id
    jobs.append(job_data)

    save_jobs_to_json(file_path, jobs)

    # Add the job processing task to background tasks
    background_tasks.add_task(process_job, job_data)

    return {"message": "Job created successfully", "job_id": new_job_id}

# Endpoint to view and edit extracted job data
@app.get("/jobs/{job_id}/view_and_edit", response_model=ExtractedData)
async def view_extracted_data(job_id: int):
    file_path = 'data/generated_job_postings.json'
    jobs = load_jobs_from_json(file_path)

    # Find job by ID
    job_data = next((job for job in jobs if job["job_id"] == job_id), None)
    if not job_data:
        raise HTTPException(status_code=404, detail=f"Job with ID {job_id} not found.")

    # Check if extracted data already exists
    if all(key in job_data for key in ["extracted_skills", "extracted_education", "extracted_experience", "extracted_responsibilities"]):
        # Return the existing extracted data
        return ExtractedData(
            extracted_skills=job_data["extracted_skills"],
            extracted_education=job_data["extracted_education"],
            extracted_experience=job_data["extracted_experience"],
            extracted_responsibilities=job_data["extracted_responsibilities"]
        )

    # Process job to extract information as a structured dictionary
    processed_data = process_job(job_data)

    # Update job_data with extracted information
    job_data["extracted_skills"] = processed_data['skills'] + job_data['required_skills']
    job_data["extracted_education"] = processed_data['education_required']
    job_data["extracted_experience"] = processed_data['experience_required']
    job_data["extracted_responsibilities"] = processed_data['responsibilities']

    # Save the updated jobs list back to the JSON file
    save_jobs_to_json(file_path, jobs)

    # Return the newly structured extracted data as a JSON response
    return ExtractedData(
        extracted_skills=job_data["extracted_skills"],
        extracted_education=job_data["extracted_education"],
        extracted_experience=job_data["extracted_experience"],
        extracted_responsibilities=job_data["extracted_responsibilities"]
    )

# Endpoint to edit and update extracted data
@app.put("/jobs/{job_id}/view_and_edit")
async def edit_extracted_data(job_id: int, updated_data: dict):
    update_job_data(job_id, updated_data)
    return {"message": "Job data updated successfully"}

# Endpoint to find top candidates for a job
@app.get("/jobs/{job_id}/match_candidates")
def get_top_candidates(job_id: int, k: int = 5):
    top_candidates = find_top_candidates(job_id, k)  # Removed `await`
    return [
        {
            'rank': candidate['rank'],
            'full_name': candidate['full_name'],
            'similarity_score': round(candidate['combined_score'], 4),
            'skills': candidate['skills'],
            'education': candidate['education'],
            'experience_years': candidate['experience_years'],
            'roles': candidate['roles'],
            'location': candidate['location'],
            'reasons': candidate['reasons']  # Adding reasons for recommendation
        }
        for candidate in top_candidates
    ]
