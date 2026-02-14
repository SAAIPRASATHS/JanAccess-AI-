"""
Skills Router — AI-powered skill and job recommendations.
"""
import logging
from fastapi import APIRouter, HTTPException

from schemas import SkillJobInput, SkillJobResponse, SkillJobRecommendation
from services import ai_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/recommend", response_model=SkillJobResponse)
async def get_recommendations(data: SkillJobInput):
    """
    Get personalized skill training and job recommendations
    based on education, interests, and location.
    """
    try:
        result = await ai_service.recommend_skills(
            education=data.education_level,
            interest=data.interest,
            location=data.location
        )

        recommendations = [
            SkillJobRecommendation(
                title=r.get("title", "Program"),
                type=r.get("type", "training"),
                description=r.get("description", ""),
                provider=r.get("provider"),
                location=r.get("location")
            )
            for r in result.get("recommendations", [])
        ]

        return SkillJobResponse(
            recommendations=recommendations,
            ai_summary=result.get("ai_summary", "Here are some recommended programs for you.")
        )

    except Exception as e:
        logger.error(f"Skills recommendation error: {e}")
        raise HTTPException(status_code=500, detail="Could not generate recommendations.")
