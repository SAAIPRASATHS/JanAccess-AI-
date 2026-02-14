"""
Assistant Router — Chat and Voice endpoints (persona-aware).
"""
import os
import uuid
import shutil
import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Query
from sqlalchemy.orm import Session

from database import get_db
from models import Interaction, Scheme, SearchHistory
from services import ai_service, speech_service
from persona_config import PERSONA_OPTIONS

logger = logging.getLogger(__name__)
router = APIRouter()

# Synonym map: user might say "farmer" but DB has "rural", "employment"
_SYNONYMS = {
    "farmer": ["rural", "employment", "mgnrega", "agriculture", "kisan"],
    "farm": ["rural", "agriculture", "mgnrega", "kisan"],
    "house": ["housing", "awas", "pmay"],
    "home": ["housing", "awas", "pmay"],
    "doctor": ["health", "hospital", "ayushman"],
    "medicine": ["health", "hospital", "ayushman"],
    "school": ["education", "scholarship", "study"],
    "college": ["education", "scholarship", "study"],
    "work": ["employment", "job", "skill", "mgnrega"],
    "money": ["income", "welfare", "benefit"],
    "gas": ["ujjwala", "lpg", "cooking"],
    "cooking": ["ujjwala", "lpg", "gas"],
    "poor": ["bpl", "welfare", "income"],
    "learn": ["skill", "training", "kaushal", "education"],
}


def _keyword_match_schemes(query: str, schemes: list) -> list:
    """Smart keyword search with synonym expansion and scoring."""
    query_lower = query.lower()
    words = [w for w in query_lower.split() if len(w) > 2]

    # If user says something very broad like "government schemes" or just "schemes"
    broad_terms = {"government", "scheme", "schemes", "sarkari", "yojana", "all"}
    if any(w in broad_terms for w in words):
        return schemes  # Return all schemes

    # Expand synonyms
    expanded_words = set(words)
    for word in words:
        if word in _SYNONYMS:
            expanded_words.update(_SYNONYMS[word])

    # Score each scheme
    scored = []
    for scheme in schemes:
        searchable = " ".join([
            (scheme.name or ""),
            (scheme.category or ""),
            (scheme.description or ""),
            (scheme.eligibility_criteria or ""),
            (scheme.benefits or ""),
        ]).lower()

        score = sum(1 for w in expanded_words if w in searchable)
        if score > 0:
            scored.append((scheme, score))

    # Sort by score descending, return top matches
    scored.sort(key=lambda x: x[1], reverse=True)
    return [s for s, _ in scored[:6]]


def _validate_persona(persona: str | None) -> str | None:
    """Return the persona if it is valid, else None."""
    if persona and persona in PERSONA_OPTIONS:
        return persona
    return None


@router.post("/chat")
async def chat_interaction(
    query: str = Query(..., min_length=1, max_length=2000),
    user_id: Optional[str] = "demo_user",
    persona: Optional[str] = Query(default=None, description="User persona for personalised responses"),
    low_bandwidth: Optional[bool] = False,
    db: Session = Depends(get_db)
):
    print(f"DEBUG: CHAT REQUEST RECEIVED - query={query}, persona={persona}")
    """
    Text-based chat endpoint.
    Analyzes query → Finds relevant schemes → Generates AI response → Returns text + audio.
    Accepts an optional `persona` to personalise the AI response.
    """
    persona = _validate_persona(persona)
    print(f"DEBUG: Chat request received - query: {query}, persona: {persona}")

    try:
        # 1. Fetch all schemes for context
        schemes = db.query(Scheme).all()
        print(f"DEBUG: Found {len(schemes)} schemes")

        # 2. Try AI-based scheme matching first, fall back to keyword search
        relevant_schemes = []
        matched_ids = await ai_service.match_schemes(query, schemes)
        if matched_ids:
            relevant_schemes = [s for s in schemes if s.id in matched_ids]

        # Fallback: smart keyword matching with scoring
        if not relevant_schemes:
            relevant_schemes = _keyword_match_schemes(query, schemes)

        # 3. Build context (include websites for AI to reference)
        context = "\n".join([
            f"• {s.name} ({s.category}): {s.description}\n  Website: {s.website}" 
            for s in relevant_schemes
        ]) if relevant_schemes else ""

        # 4. Generate AI response (persona-aware)
        print("DEBUG: Calling AI service...")
        response_text = await ai_service.generate_conversational_response(query, context, persona)
        print(f"DEBUG: AI response received: {response_text[:50]}...")

        # 5. Log interaction
        interaction = Interaction(
            user_id=user_id,
            query=query,
            response=response_text,
            persona=persona,
        )
        db.add(interaction)

        # 6. Log search history for analytics
        search_entry = SearchHistory(
            query_text=query,
            category=relevant_schemes[0].category if relevant_schemes else None,
            persona=persona,
            matched_schemes=",".join([s.name for s in relevant_schemes]) if relevant_schemes else None
        )
        db.add(search_entry)
        db.commit()

        # 7. Generate audio (skip in low bandwidth mode)
        audio_url = None
        if not low_bandwidth:
            audio_path = speech_service.text_to_speech(response_text)
            if audio_path:
                audio_url = f"/static/audio/{os.path.basename(audio_path)}"

        return {
            "text_response": response_text,
            "audio_url": audio_url,
            "schemes": [
                {"name": s.name, "website": s.website} 
                for s in relevant_schemes
            ],
            "persona": persona,
        }

    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail="An error occurred processing your request.")


@router.post("/voice-chat")
async def voice_interaction(
    file: UploadFile = File(...),
    user_id: Optional[str] = "demo_user",
    persona: Optional[str] = Query(default=None, description="User persona"),
    db: Session = Depends(get_db)
):
    """
    Voice-based chat endpoint.
    Receives audio → Transcribes via Whisper → Processes as chat → Returns text + audio.
    """
    persona = _validate_persona(persona)

    # Save uploaded audio
    upload_dir = "static/uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = f"{upload_dir}/{uuid.uuid4()}.webm"

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Transcribe
        transcribed_text = await speech_service.transcribe_audio(file_path)

        # Use chat logic
        result = await chat_interaction(
            query=transcribed_text, user_id=user_id, persona=persona, db=db
        )

        # Add transcribed text to response
        result["transcribed_text"] = transcribed_text
        return result

    except Exception as e:
        logger.error(f"Voice chat error: {e}")
        raise HTTPException(status_code=500, detail="Voice processing failed.")
    finally:
        # Cleanup uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError:
                pass


@router.get("/persona-options")
async def get_persona_options():
    """Return the list of available personas and their quick actions."""
    from persona_config import PERSONA_QUICK_ACTIONS
    return {
        "personas": PERSONA_OPTIONS,
        "quick_actions": PERSONA_QUICK_ACTIONS,
    }
