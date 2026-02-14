"""
Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ─── Assistant ───────────────────────────────────────────────────

class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000)
    user_id: str = "demo_user"
    persona: Optional[str] = None


class ChatResponse(BaseModel):
    text_response: str
    audio_url: Optional[str] = None
    schemes: List[str] = []
    transcribed_text: Optional[str] = None


# ─── Schemes ─────────────────────────────────────────────────────

class SchemeCreate(BaseModel):
    name: str
    category: str
    description: str
    benefits: str
    eligibility_criteria: str
    application_process: str
    documents_required: str
    contact_info: str


class SchemeResponse(SchemeCreate):
    id: int
    class Config:
        from_attributes = True


# ─── Eligibility ─────────────────────────────────────────────────

class EligibilityCriteria(BaseModel):
    age: int = Field(..., ge=1, le=120)
    income: float = Field(..., ge=0)
    category: str = Field(..., min_length=1)       # SC / ST / OBC / General
    location: str = Field(..., min_length=1)
    education_level: Optional[str] = None
    interests: Optional[str] = None


class EligibilityResponse(BaseModel):
    eligible_schemes: List[dict]
    ai_explanation: str
    total_found: int


# ─── Document ────────────────────────────────────────────────────

class AnalysisResponse(BaseModel):
    filename: str
    summary: str
    simplification: str
    next_steps: str


# ─── Skills & Jobs ───────────────────────────────────────────────

class SkillJobInput(BaseModel):
    education_level: str = Field(..., min_length=1)
    interest: str = Field(..., min_length=1)
    location: str = Field(..., min_length=1)


class SkillJobRecommendation(BaseModel):
    title: str
    type: str                     # "training" or "job"
    description: str
    provider: Optional[str] = None
    location: Optional[str] = None


class SkillJobResponse(BaseModel):
    recommendations: List[SkillJobRecommendation]
    ai_summary: str


# ─── Analytics ───────────────────────────────────────────────────

class AnalyticsSummary(BaseModel):
    total_queries: int
    total_documents: int
    top_schemes: List[dict]
    category_breakdown: dict
    persona_breakdown: dict = {}
    recent_queries: List[dict]


class PersonaUsageResponse(BaseModel):
    most_selected_persona: Optional[str] = None
    persona_counts: dict = {}
    top_topics_per_persona: dict = {}
