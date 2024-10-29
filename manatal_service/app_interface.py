import streamlit as st
import requests
import time
import pickle

# Base URL of your FastAPI app (update this if running on a different port)
BASE_URL = "http://127.0.0.1:8000"

st.title("Job Management and Candidate Matching Interface")

# Section to create a new job
st.header("Create a New Job")
job_title = st.text_input("Job Title")
job_description = st.text_area("Job Description")
location = st.text_input("Location")
employment_type = st.selectbox("Employment Type", ["Full-time", "Part-time", "Contract"])
required_skills = st.text_area("Required Skills (comma-separated)")
company_name = st.text_input("Company Name")

# Budget fields
budget_min = st.number_input("Minimum Budget", min_value=0)
budget_max = st.number_input("Maximum Budget", min_value=0)
budget_currency = st.selectbox("Currency", ["USD", "EUR", "GBP"])

create_job_button = st.button("Create Job")

if create_job_button:
    job_data = {
        "job_title": job_title,
        "job_description": job_description,
        "location": location,
        "employment_type": employment_type,
        "required_skills": required_skills.split(","),
        "company_name": company_name,
        "budget": {
            "min": str(budget_min),  # Convert to string to match your model type
            "max": str(budget_max),  # Convert to string to match your model type
            "currency": budget_currency
        }
    }
    response = requests.post(f"{BASE_URL}/jobs/create", json=job_data)
    if response.status_code == 200:
        st.success(f"Job created successfully with ID: {response.json()['job_id']}")
    else:
        st.error(f"Failed to create job: {response.text}")

# Section to view and edit extracted job data
st.header("View and Edit Extracted Job Data")
view_job_id = st.number_input("Job ID to View", min_value=1, step=1)
view_job_button = st.button("View Extracted Data")

# Use session state to maintain extracted data between view and edit
if view_job_button or f"extracted_data_{view_job_id}" in st.session_state:
    response = requests.get(f"{BASE_URL}/jobs/{view_job_id}/view_and_edit")
    if response.status_code == 200:
        extracted_data = response.json()
        st.session_state[f"extracted_data_{view_job_id}"] = extracted_data

        st.write("Extracted Skills:", ", ".join(extracted_data["extracted_skills"]))
        st.write("Extracted Education:", ", ".join(extracted_data["extracted_education"]))
        st.write("Extracted Experience:", extracted_data["extracted_experience"])
        st.write("Extracted Responsibilities:", ", ".join(extracted_data["extracted_responsibilities"]))

        # Prefill the edit section with the existing extracted data
        edit_skills = st.text_area("Extracted Skills (comma-separated)", ", ".join(extracted_data["extracted_skills"]))
        edit_education = st.text_area("Extracted Education (comma-separated)", ", ".join(extracted_data["extracted_education"]))
        edit_experience = st.text_input("Extracted Experience", extracted_data["extracted_experience"])
        edit_responsibilities = st.text_area("Extracted Responsibilities (comma-separated)", ", ".join(extracted_data["extracted_responsibilities"]))

        # Section to edit extracted data
        edit_job_button = st.button("Edit Job Data")

        if edit_job_button:
            updated_data = {
                "extracted_skills": edit_skills.split(","),
                "extracted_education": edit_education.split(","),
                "extracted_experience": edit_experience,
                "extracted_responsibilities": edit_responsibilities.split(",")
            }
            response = requests.put(f"{BASE_URL}/jobs/{view_job_id}/view_and_edit", json=updated_data)
            if response.status_code == 200:
                st.success("Job data updated successfully")
            else:
                st.error(f"Failed to update job data: {response.text}")
    else:
        st.error(f"Failed to view job data: {response.text}")

# Section to find top candidates for a job
st.header("Find Top Candidates for a Job")
match_job_id = st.number_input("Job ID for Matching", min_value=1, step=1)
num_candidates = st.slider("Number of Top Candidates to Retrieve", min_value=1, max_value=100, value=5)
match_candidates_button = st.button("Find Top Candidates")

if match_candidates_button:
    start_time = time.time()  # Start the timer
    response = requests.get(f"{BASE_URL}/jobs/{match_job_id}/match_candidates?k={num_candidates}")
    end_time = time.time()  # End the timer
    response_time = end_time - start_time

    if response.status_code == 200:
        st.write(f"Response Time: {response_time:.2f} seconds")
        top_candidates = response.json()
        with open('data/candidate_metadata.pkl', 'rb') as f:
            data = pickle.load(f)
            total_candidates = len(data['metadata'])
        st.write(f"Total Candidates in Database: {total_candidates}")
        for candidate in top_candidates:
            st.write("Rank:", candidate["rank"])
            st.write("Name:", candidate["full_name"])
            st.write("Similarity Score:", candidate["similarity_score"])
            st.write("Skills:", ", ".join(candidate["skills"]))
            st.write("Education:", ", ".join(candidate["education"]))
            st.write("Experience Years:", candidate["experience_years"])
            st.write("Roles:", ", ".join(candidate["roles"]))
            st.write("Location:", candidate["location"])
            st.write("---")
    else:
        st.error(f"Failed to retrieve top candidates: {response.text}")
