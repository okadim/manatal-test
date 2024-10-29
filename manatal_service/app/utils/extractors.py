# app/utils/extractors.py

import spacy
import re
from flashtext import KeywordProcessor

# Load the spaCy English language model
nlp = spacy.load('en_core_web_sm')

# Define skill lists
programming_languages = ["Python", "JavaScript", "Java", "C++", "C#", "Ruby", "Go", "Swift", "Kotlin"]
frameworks = ["Django", "Flask", "React", "Angular", "Vue.js", "Spring", "Ruby on Rails", "ASP.NET"]
databases = ["PostgreSQL", "MySQL", "MongoDB", "SQLite", "Oracle", "SQL Server"]
cloud_services = ["AWS", "Azure", "Google Cloud", "GCP", "IBM Cloud", "Oracle Cloud"]
technologies = ["Machine Learning", "Artificial Intelligence", "Big Data", "Microservices", "Docker", "Kubernetes"]
supply_chain_skills = [
    "Supply Chain Management",
    "Logistics",
    "Inventory Management",
    "ERP",
    "SAP",
    "MS Office",
    "Google Suite",
    "Lingo",
    "WMS",
    "Procurement",
    "Vendor Management",
    "Forecasting",
    "Data Analysis",
    "Process Improvement"
]

# Combine all skills into one list
all_skills_list = programming_languages + frameworks + databases + cloud_services + technologies + supply_chain_skills

# Education levels
education_levels = [
    "High School Diploma",
    "Associate's Degree",
    "Bachelor's Degree",
    "Bachelor of Science",
    "Bachelor of Arts",
    "Master's Degree",
    "Master of Science",
    "Master of Arts",
    "MBA",
    "PhD",
    "Doctorate"
]

# Initialize keyword processors
skill_processor = KeywordProcessor(case_sensitive=False)
skill_processor.add_keywords_from_list(all_skills_list)

education_processor = KeywordProcessor(case_sensitive=False)
education_processor.add_keywords_from_list(education_levels)

# Function to extract skills
def extract_skills(text):
    skills_found = skill_processor.extract_keywords(text)
    return list(set(skills_found))

# Function to extract education requirements
# Function to extract education requirements
def extract_education(text):
    education_found = set()

    # Updated patterns to match education levels more accurately
    patterns = [
        r"(Bachelor(?:'s)?(?: of)?(?: in)? [A-Za-z\s]+)",  # Matches variations of bachelor's degrees
        r"(Master(?:'s)?(?: of)?(?: in)? [A-Za-z\s]+)",  # Matches variations of master's degrees
        r"(MBA)",
        r"(PhD(?: in [A-Za-z\s]+)?)",
        r"(Doctorate(?: in [A-Za-z\s]+)?)",
        r"(Degree in [A-Za-z\s]+)",
        r"(Diploma in [A-Za-z\s]+)",
        r"(Certification in [A-Za-z\s]+)"
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            education_level = match.strip()
            education_found.add(education_level)

    return list(education_found)


# Function to normalize education levels
def normalize_education_levels(education_list):
    normalized_levels = []
    mapping = {
        r"Master(?:'s)?.*": "Master's Degree",
        r"Master of .*": "Master's Degree",
        r"Masters.*": "Master's Degree",
        r"Bachelor(?:'s)?.*": "Bachelor's Degree",
        r"Bachelor of .*": "Bachelor's Degree",
        r"PhD.*": "PhD",
        r"Doctorate.*": "PhD",
        r"Degree in .*": "Other Degree",
        r"Diploma in .*": "Diploma",
        r"Certification in .*": "Certification"
    }

    for edu in education_list:
        normalized = False
        for pattern, standard in mapping.items():
            if re.match(pattern, edu, re.IGNORECASE):
                normalized_levels.append(standard)
                normalized = True
                break
        if not normalized:
            normalized_levels.append(edu)
    return list(set(normalized_levels))



# Function to extract experience requirements
def extract_experience(text):
    doc = nlp(text)
    experience_years = 0
    
    # Updated patterns to capture different phrases for experience
    patterns = [
        r'(\d+)\+?\s+years? of experience',  # Matches "X years of experience"
        r'(?i)(?:at least|minimum of|minimum|more than|over)\s+(\d+)\s+years?',  # Matches "At least X years", "Minimum of X years", etc.
        r'(\d+)\+?\s+years',  # Matches "X years"
        r'(?i)(?:minimum of|at least|more than|over)\s+(\d+)\s+years?\s+(?:as|in|working as|working in)'  # Matches phrases like "Minimum of X years as a..."
    ]
    
    for sent in doc.sents:
        for pattern in patterns:
            matches = re.findall(pattern, sent.text)
            if matches:
                years = [int(match) for match in matches]
                experience_years = max(years)
                break
        if experience_years > 0:
            break

    return experience_years


# Add this function to extract responsibilities based on the summary script
# Function to extract responsibilities
def extract_responsibilities(text):
    # Split the text into lines based on newlines or bullet points
    lines = re.split(r'\n+|•|\*|-', text)
    # Remove empty lines and strip whitespace
    responsibilities = [line.strip() for line in lines if line.strip()]
    return responsibilities

