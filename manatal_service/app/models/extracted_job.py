from pydantic import BaseModel
from typing import List, Dict, Optional, Union  # Add Union here


class ExtractedData(BaseModel):
    extracted_skills: List[str]
    extracted_education: List[str]
    extracted_experience: Union[str, int]  # Accepts both string and integer values
    extracted_responsibilities: List[str]
