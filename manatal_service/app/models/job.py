from pydantic import BaseModel
from typing import List, Dict, Optional

class Job(BaseModel):
    job_title: str
    job_description: str
    budget: Dict[str, str]
    location: str
    company_name: str
    employment_type: str
    required_skills: List[str]
    extracted_text: Optional[str] = None  # Optional field to display extracted information
