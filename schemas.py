from pydantic import BaseModel
from typing import List

class Subjective(BaseModel):
    chief_complaint: str
    hpi: str

class Objective(BaseModel):
    exam: str
    vitals: str
    labs: str

class Plan(BaseModel):
    medications: List[str]
    labs: List[str]
    referrals: List[str]
    instructions: List[str]
    follow_up: str

class SOAPNote(BaseModel):
    subjective: Subjective
    objective: Objective
    assessment: List[str]
    plan: Plan
    visit_summary: str
