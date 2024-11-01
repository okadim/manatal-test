import os
import json
import re
import time
import random
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
openai.api_key = os.getenv('OPEN_AI_KEY')

# Example lists of names, addresses, and job titles
first_names = [
    "Than", "Aung", "Soe", "Ploy", "Siri", "Maria", "Juan", "Rico", "James", "Anne", "Omar",
    "Nina", "Ethan", "Liam", "Noah", "Emma", "Olivia", "Ava", "Sophia", "Amelia", "Mia", "Zara",
    "Isabella", "Aiden", "Lucas", "Elijah", "Mason", "Aria", "Chloe", "Lily", "Henry", "Grace",
    "Benjamin", "Leo", "Daniel", "Ella", "Victoria", "Isla", "Jack", "Max", "Alexander", "Samir",
    "Ali", "Noura", "Rana", "Jasmine", "Tariq", "Ahmed", "Carlos", "Marta", "Pablo"
]

last_names = [
    "Win", "Santos", "Nguyen", "Wong", "Garcia", "Rodriguez", "Kumar", "Li", "Tan", "Pérez", "Kadim",
    "Johnson", "Smith", "Brown", "Jones", "Miller", "Davis", "Martinez", "Lopez", "Wilson", "Evans",
    "Thomas", "Anderson", "Moore", "Martin", "White", "Clark", "Hall", "Walker", "Allen", "Young",
    "King", "Scott", "Green", "Baker", "Adams", "Nelson", "Hill", "Campbell", "Mitchell", "Perez",
    "Roberts", "Murphy", "Carter", "Bailey", "Rivera", "Sanchez", "Ramirez", "Flores", "Chavez", "Patel"
]

cities_by_country = {
    "Thailand": ["Bangkok", "Chiang Mai", "Phuket", "Pattaya", "Udon Thani", "Surat Thani"],
    "Philippines": ["Manila", "Cebu City", "Davao", "Quezon City", "Makati", "Taguig"],
    "United States": ["New York", "San Francisco", "Los Angeles", "Chicago", "Austin", "Seattle", "Miami"],
    "India": ["Mumbai", "Delhi", "Bangalore", "Chennai", "Hyderabad", "Kolkata", "Pune"],
    "Japan": ["Tokyo", "Osaka", "Kyoto", "Nagoya", "Hiroshima", "Sapporo"],
    "Morocco": ["Casablanca", "Rabat", "Marrakech", "Fes", "Tangier", "Chefchaouen"],
    "Turkey": ["Istanbul", "Izmir", "Ankara", "Antalya", "Bursa"],
    "France": ["Paris", "Lyon", "Marseille", "Nice", "Bordeaux"],
}

# Extended list of job titles with logical career paths and skills
job_skills_experiences = {
    "Data Scientist": {
        "skills": ["Python", "Machine Learning", "Data Analysis", "Statistics", "SQL"],
        "experiences": ["Data Analyst", "Junior Data Scientist", "Research Assistant"]
    },
    "Marketing Manager": {
        "skills": ["Marketing Strategy", "SEO", "Content Creation", "Social Media", "Brand Management"],
        "experiences": ["Marketing Specialist", "Social Media Coordinator", "Brand Strategist"]
    },
    "Software Developer": {
        "skills": ["Java", "Python", "C++", "Software Development", "APIs"],
        "experiences": ["Junior Developer", "Software Engineer Intern", "Full Stack Developer"]
    },
    "Product Manager": {
        "skills": ["Product Strategy", "Project Management", "Market Research", "Agile"],
        "experiences": ["Product Analyst", "Associate Product Manager", "Project Coordinator"]
    },
    "Accountant": {
        "skills": ["Financial Reporting", "Accounting", "Tax Preparation", "Bookkeeping", "Budgeting"],
        "experiences": ["Accounting Assistant", "Junior Accountant", "Finance Intern"]
    },
    "Financial Analyst": {
        "skills": ["Financial Modeling", "Excel", "Investment Analysis", "Forecasting", "Budgeting"],
        "experiences": ["Financial Assistant", "Budget Analyst", "Junior Financial Analyst"]
    },
    "Strategy Consultant": {
        "skills": ["Strategic Planning", "Business Analysis", "Market Research", "Project Management", "Data Analysis"],
        "experiences": ["Consulting Analyst", "Business Consultant", "Junior Strategy Consultant"]
    },
    "HR Specialist": {
        "skills": ["Recruitment", "Employee Relations", "HR Policies", "Payroll", "Onboarding"],
        "experiences": ["HR Assistant", "Recruiter", "HR Coordinator"]
    },
    "Operations Manager": {
        "skills": ["Process Improvement", "Logistics", "Inventory Management", "Supply Chain Management"],
        "experiences": ["Operations Coordinator", "Supply Chain Analyst", "Production Supervisor"]
    },
}

# Extended university list
universities = [
    "University of California, Berkeley", "Harvard University", "Stanford University",
    "University of Oxford", "Massachusetts Institute of Technology", "University of Tokyo",
    "National University of Singapore", "University of Cambridge", "Peking University",
    "University of Sydney", "Sorbonne University", "University of Cape Town",
    "University of Toronto", "Kyoto University", "McGill University",
    "Technical University of Munich", "Lomonosov Moscow State University",
    "Pontifical Catholic University of Chile", "University of Melbourne",
]

def random_address():
    country = random.choice(list(cities_by_country.keys()))
    city = random.choice(cities_by_country[country])
    street_number = random.randint(1, 999)
    return f"{street_number} {city} St, {city}, {country}"

def random_name():
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    return first_name, last_name

def random_job_title():
    return random.choice(list(job_skills_experiences.keys()))

def extract_json_from_response(response_text):
    response_text = response_text.strip()
    if response_text.startswith("```"):
        response_text = response_text.strip("`")
        response_text = re.sub(r'^json\n', '', response_text, flags=re.IGNORECASE).strip()
    try:
        json_obj = json.loads(response_text)
        return json_obj
    except json.JSONDecodeError:
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            json_text = json_match.group(0)
            try:
                json_obj = json.loads(json_text)
                return json_obj
            except json.JSONDecodeError:
                return None
        else:
            return None

def generate_candidate_profile(first_name, last_name, address, job_title):
    system_prompt = "You are a helpful assistant that generates realistic candidate profiles in JSON format."

    # Retrieve related skills and experiences based on job title
    job_data = job_skills_experiences.get(job_title, {"skills": ["General Skill"], "experiences": ["General Role"]})
    skills = job_data["skills"]
    previous_roles = job_data["experiences"]

    # Generate realistic job experiences
    experiences = [
        {
            "company": f"Company {i + 1}",
            "role": random.choice(previous_roles),
            "start_date": f"{2020 - i}-01-01",
            "end_date": f"{2021 - i}-12-31" if i < 2 else "Present"
        }
        for i in range(random.randint(1, 3))  # Generate 1-3 experiences
    ]

    user_prompt = f"""
Generate a realistic candidate profile in JSON format with the provided first name, last name, address, and job title.
Ensure the JSON syntax is proper and details are realistic.

{{
    "first_name": "{first_name}",
    "last_name": "{last_name}",
    "birthdate": "YYYY-MM-DD",
    "age": integer,
    "email": "{first_name.lower()}.{last_name.lower()}@example.com",
    "phone": "+1-555-123-4567",
    "address": "{address}",
    "job_title": "{job_title}",
    "skills": {json.dumps(skills)},
    "experiences": {json.dumps(experiences)},
    "education": [
        {{
            "institution": "University of {random.choice(universities)}",
            "degree": random.choice(["Bachelor's", "Master's", "Ph.D."]),
            "year_of_graduation": random.randint(2005, 2022)
        }}
    ]
}}
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=800,
        temperature=0.8,
        n=1
    )
    candidate_profile_text = response['choices'][0]['message']['content']
    return candidate_profile_text

def main():
    num_candidates = 100  # Adjust the number as needed
    candidates = []

    for i in range(num_candidates):
        print(f"Generating candidate profile {i + 1}/{num_candidates}")
        
        # Generate unique name, address, and job title
        first_name, last_name = random_name()
        address = random_address()
        job_title = random_job_title()
        
        # Generate profile
        candidate_profile_text = generate_candidate_profile(first_name, last_name, address, job_title)
        candidate_profile = extract_json_from_response(candidate_profile_text)
        
        if candidate_profile:
            candidates.append(candidate_profile)
        else:
            print("Failed to extract JSON from the response.")
            continue
        time.sleep(0.2)  # Adjust sleep time if necessary

    # Output generated candidates
    with open("generated_candidates.json", "w") as f:
        json.dump(candidates, f, indent=4)

    print(f"\nGenerated {len(candidates)} candidate profiles successfully.")

if __name__ == "__main__":
    main()
