import os
import json
import re
import time
import random
import openai

# Set OpenAI API key (ensure it's securely stored)
openai.api_key = "i-could-have-create-an-env-file-but-lazy-today"

# Example lists of names, addresses, and job titles
# Example lists of names
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
    "Myanmar": ["Yangon", "Mandalay", "Naypyidaw", "Bago", "Taunggyi", "Pyin Oo Lwin"],
    "United States": ["New York", "San Francisco", "Los Angeles", "Chicago", "Austin", "Seattle", "Miami"],
    "India": ["Mumbai", "Delhi", "Bangalore", "Chennai", "Hyderabad", "Ahmedabad", "Kolkata", "Pune"],
    "Japan": ["Tokyo", "Osaka", "Kyoto", "Fukuoka", "Nagoya", "Hiroshima", "Sapporo"],
    "Palestine": ["Jerusalem", "Ramallah", "Gaza", "Bethlehem", "Hebron", "Nablus"],
    "Morocco": ["Casablanca", "Rabat", "Marrakech", "Fes", "Tangier", "Agadir", "Chefchaouen"],
    "Turkey": ["Istanbul", "Izmir", "Ankara", "Bursa", "Antalya", "Konya", "Gaziantep"],
    "France": ["Paris", "Grenoble", "Lyon", "Marseille", "Nice", "Toulouse", "Bordeaux"],
    "Brazil": ["São Paulo", "Rio de Janeiro", "Brasília", "Salvador", "Fortaleza", "Curitiba"],
    "Canada": ["Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa", "Quebec City"],
    "United Kingdom": ["London", "Manchester", "Birmingham", "Edinburgh", "Glasgow", "Liverpool"],
    "Germany": ["Berlin", "Munich", "Frankfurt", "Hamburg", "Cologne", "Stuttgart"],
    "Australia": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide", "Gold Coast"],
    "China": ["Beijing", "Shanghai", "Guangzhou", "Shenzhen", "Chengdu", "Wuhan"],
    "South Korea": ["Seoul", "Busan", "Incheon", "Daegu", "Daejeon", "Gwangju"],
    "South Africa": ["Johannesburg", "Cape Town", "Pretoria", "Durban", "Bloemfontein"],
    "Italy": ["Rome", "Milan", "Naples", "Turin", "Florence", "Venice"],
    "Spain": ["Madrid", "Barcelona", "Valencia", "Seville", "Bilbao", "Malaga"]
}


job_titles = [
    "Data Scientist", "Data Engineer", "Data Analyst", "Product Manager", "Talent Acquisition",
    "HR", "AI Engineer", "ML Engineer", "Software Developer", "Python Software Engineer",
    "Barber", "Butcher", "Legal Counsel", "Lead Data Scientist", "Senior Solution Architect",
    "Judoka", "Oil Engineer", "M&A Analyst", "Growth Hacker",
    "Trader", "Quantitative Analyst", "UX/UI Designer", "Marketing Manager", "Operations Manager",
    "Cybersecurity Specialist", "Content Strategist", "Supply Chain Analyst", "Blockchain Developer",
    "Business Development Manager", "Customer Success Manager", "Chief Marketing Officer",
    "Environmental Consultant", "Sales Executive", "Full Stack Developer", "Quality Assurance Engineer",
    "Digital Transformation Consultant", "Biotech Researcher", "Public Relations Specialist", "IOT Engineer", "Industrial Engineer", "Supply Planner"
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
    return random.choice(job_titles)

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
    "skills": ["string", "string", "..."],
    "experiences": [
        {{
            "company": "string",
            "role": "{job_title}",
            "start_date": "YYYY-MM-DD",
            "end_date": "YYYY-MM-DD or 'Present'"
        }},
        ...
    ],
    "education": [
        {{
            "institution": "string",
            "degree": "string",
            "year_of_graduation": integer
        }},
        ...
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
    num_candidates = 400  # Adjust the number as needed
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
    with open("generated_100_candidates.json", "w") as f:
        json.dump(candidates, f, indent=4)

    print(f"\nGenerated {len(candidates)} candidate profiles successfully.")

if __name__ == "__main__":
    main()
