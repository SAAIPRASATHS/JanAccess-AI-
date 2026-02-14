"""
Eligibility Router — Smart eligibility checking with AI explanation.
"""
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Scheme
from schemas import EligibilityCriteria, EligibilityResponse
from services import eligibility_engine, ai_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/check", response_model=EligibilityResponse)
async def check_eligibility(
    criteria: EligibilityCriteria,
    db: Session = Depends(get_db)
):
    """
    Check eligibility based on user profile.
    Uses rule-based engine + AI-generated human-friendly explanation.
    """
    try:
        # 1. Fetch all schemes
        all_schemes = db.query(Scheme).all()
        if not all_schemes:
            return EligibilityResponse(
                eligible_schemes=[],
                ai_explanation="No schemes are currently in the database. Please try again later.",
                total_found=0
            )

        # 2. Run rule-based eligibility engine
        eligible = eligibility_engine.get_eligible_schemes(criteria, all_schemes)

        # 3. Format eligible schemes
        eligible_data = [
            {
                "name": s.name,
                "category": s.category,
                "benefits": s.benefits,
                "documents_required": s.documents_required,
                "application_process": s.application_process,
                "contact_info": s.contact_info
            }
            for s in eligible
        ]

        # 4. Generate AI explanation
        user_profile = {
            "age": criteria.age,
            "income": criteria.income,
            "category": criteria.category,
            "location": criteria.location
        }
        explanation = await ai_service.explain_eligibility(user_profile, eligible)

        return EligibilityResponse(
            eligible_schemes=eligible_data,
            ai_explanation=explanation,
            total_found=len(eligible)
        )

    except Exception as e:
        logger.error(f"Eligibility check error: {e}")
        raise HTTPException(status_code=500, detail="Eligibility check failed.")
