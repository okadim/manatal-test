import random
import json
import datetime

# Load the existing candidate profiles
with open('data/generated_candidates.json', 'r') as file:
    existing_candidates = json.load(file)

new_candidates = []
num_new_candidates = 100000 - len(existing_candidates)

first_names = ["Mason", "Liam", "Noah", "Olivia", "Emma", "Ava", "Sophia", "Isabella", "Amelia", "Mia"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Martinez", "Hernandez"]
job_titles = ["Data Analyst", "Software Engineer", "Project Manager", "Business Analyst", "Marketing Specialist"]
skills_pool = [
    "Data analysis", "Statistical analysis", "Data visualization", "SQL", "Python", "Java", "C++", "Machine Learning",
    "Project management", "SEO", "Digital Marketing", "Leadership", "Communication", "Teamwork", "AWS", "Docker"
]
education_degrees = [
    "Bachelor of Science in Computer Science", "Master of Business Administration", "Bachelor of Arts in Marketing",
    "PhD in Artificial Intelligence", "Diploma in Project Management"
]
institutions = ["University of Technology Sydney", "Harvard University", "Stanford University", "MIT", "Cambridge University"]
locations = ["New York, USA", "San Francisco, USA", "London, UK", "Paris, France", "Berlin, Germany", "Sydney, Australia"]

for i in range(num_new_candidates):
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    birth_year = random.randint(1970, 2000)
    birthdate = datetime.date(birth_year, random.randint(1, 12), random.randint(1, 28))
    age = datetime.date.today().year - birth_year
    email = f"{first_name.lower()}.{last_name.lower()}{i + len(existing_candidates)}@example.com"
    phone = f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
    address = f"{random.randint(100, 999)} {random.choice(locations)}"
    job_title = random.choice(job_titles)
    skills = random.sample(skills_pool, random.randint(3, 6))
    
    experiences = [
        {
            "company": f"Company {random.randint(1, 100)}",
            "role": job_title,
            "start_date": f"{random.randint(2005, 2015)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
            "end_date": "Present" if random.choice([True, False]) else f"{random.randint(2016, 2023)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
        }
    ]

    education = [
        {
            "institution": random.choice(institutions),
            "degree": random.choice(education_degrees),
            "year_of_graduation": random.randint(2000, 2020)
        }
    ]

    candidate = {
        "first_name": first_name,
        "last_name": last_name,
        "birthdate": str(birthdate),
        "age": age,
        "email": email,
        "phone": phone,
        "address": address,
        "job_title": job_title,
        "skills": skills,
        "experiences": experiences,
        "education": education
    }

    new_candidates.append(candidate)

# Combine with existing candidates and save
all_candidates = existing_candidates + new_candidates

with open('data/generated_candidates.json', 'w') as file:
    json.dump(all_candidates, file, indent=4)
