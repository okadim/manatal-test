# app/models/candidate.py

from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional
from datetime import date, datetime

class Experience(BaseModel):
    company: str
    role: str
    start_date: date
    end_date: Optional[date] = None  # Allow None if still "Present"

    @validator('end_date', pre=True, always=True)
    def validate_end_date(cls, value):
        # Handle both "Present" and "present" as None
        if str(value).lower() == "present":
            return None
        # Attempt to parse other values as dates
        return datetime.strptime(value, '%Y-%m-%d').date()

class Education(BaseModel):
    institution: Optional[str] = None  # Set institution as optional
    degree: str
    year_of_graduation: int

class Candidate(BaseModel):
    first_name: str
    last_name: str
    birthdate: date
    age: int
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = ""
    skills: List[str]
    experiences: List[Experience]
    education: List[Education]
    
    # Computed fields
    full_name: Optional[str] = None
    experience_years: Optional[float] = None  # Rounded to 1 decimal point

    def __init__(self, **data):
        super().__init__(**data)
        # Set computed fields
        self.full_name = f"{self.first_name} {self.last_name}"
        self.experience_years = self.calculate_experience_years()

    def calculate_experience_years(self):
        total_experience = 0
        for exp in self.experiences:
            start_date = exp.start_date
            end_date = exp.end_date or datetime.now().date()  # Use current date if end_date is None
            duration = (end_date - start_date).days / 365.25
            total_experience += duration
        return round(total_experience, 1)
