# schemas/resume.py
from pydantic import BaseModel
from typing import List, Optional

class ExperienceItem(BaseModel):
    company: Optional[str]
    role: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    description: Optional[str]

class EducationItem(BaseModel):
    institution: Optional[str]
    degree: Optional[str]
    start_year: Optional[str]
    end_year: Optional[str]

class Resume(BaseModel):
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    location: Optional[str]
    links: List[str] = []
    summary: Optional[str]
    skills: List[str] = []
    experience: List[ExperienceItem] = []
    education: List[EducationItem] = []
    certifications: List[str] = []