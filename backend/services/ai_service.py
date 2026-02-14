"""
AI Service — Groq / OpenAI API integration with graceful fallbacks.
All functions work without an API key by returning mock responses.
"""
import os
import json
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

# Initialize AI client (may be None if no key)
_client = None

def _get_client():
    """Lazy-load the async client. Prefers Groq, falls back to OpenAI."""
    global _client
    if _client is None:
        groq_key = os.getenv("GROQ_API_KEY", "")
        openai_key = os.getenv("OPENAI_API_KEY", "")

        try:
            from openai import AsyncOpenAI

            if groq_key:
                _client = AsyncOpenAI(
                    api_key=groq_key,
                    base_url="https://api.groq.com/openai/v1",
                )
                logger.info("Using Groq API")
            elif openai_key and openai_key != "your_openai_api_key_here":
                _client = AsyncOpenAI(api_key=openai_key)
                logger.info("Using OpenAI API")
        except Exception as e:
            logger.warning(f"Could not initialize AI client: {e}")
    return _client

# Configurable model — Groq uses Llama, OpenAI uses gpt-3.5-turbo
AI_MODEL = os.getenv("AI_MODEL", "llama-3.3-70b-versatile")


# ─── System Prompts ──────────────────────────────────────────────

SYSTEM_CIVIC = (
    "You are JanAccess AI, a helpful civic intelligence assistant for India. "
    "Always simplify to Grade 5 reading level. Avoid technical jargon. "
    "Provide actionable next steps. Be empathetic and respectful. "
    "Keep answers concise — under 200 words. "
    "When suggesting schemes, mention that official portal links are available in the suggestions."
)

SYSTEM_SIMPLIFY = (
    "You are a clear language expert. Rewrite the following text to be simple, "
    "easy to understand (Grade 5 level), and actionable. Remove jargon. "
    "Add bullet points for key steps. Keep it under 250 words."
)


# ─── Core AI Functions ──────────────────────────────────────────

async def analyze_query(query: str) -> Dict[str, Any]:
    """Identify user intent from the query."""
    client = _get_client()
    if not client:
        return {"intent": "general_query", "entities": {}}

    try:
        response = await client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "system", "content": (
                    "Extract user intent (scheme_search, eligibility_check, "
                    "document_help, skill_query, general_query) and key entities "
                    "(income, age, location, category). Return ONLY JSON."
                )},
                {"role": "user", "content": query}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        logger.error(f"analyze_query error: {e}")
        return {"intent": "general_query", "entities": {}}


def _build_system_prompt(persona: str | None = None) -> str:
    """Build the system prompt, optionally enriched with persona instructions."""
    prompt = SYSTEM_CIVIC
    if persona:
        from backend.persona_config import PERSONA_SYSTEM_PROMPTS
        extra = PERSONA_SYSTEM_PROMPTS.get(persona, "")
        if extra:
            prompt += (
                f" You are assisting a {persona}. "
                f"Tailor recommendations and explanations specifically for this category. "
                f"{extra}"
            )
    return prompt


async def generate_conversational_response(
    user_query: str, context: str, persona: str | None = None
) -> str:
    """Generate an empathetic, simple response — persona-aware."""
    client = _get_client()
    if not client:
        return _fallback_response(user_query, context)

    system_prompt = _build_system_prompt(persona)

    try:
        response = await client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context:\n{context}\n\nUser Question: {user_query}"}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"generate_response error: {e}")
        return _fallback_response(user_query, context)


async def match_schemes(user_query: str, schemes: list) -> List[int]:
    """Use AI to find relevant schemes from a list."""
    client = _get_client()
    if not client or not schemes:
        return []

    try:
        scheme_texts = [
            f"ID: {s.id}, Name: {s.name}, Category: {s.category}, Description: {s.description[:100]}"
            for s in schemes[:10]
        ]
        response = await client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "system", "content": "Return a JSON object with key 'ids' containing an array of relevant scheme IDs."},
                {"role": "user", "content": f"User asked: \"{user_query}\"\n\nSchemes:\n{json.dumps(scheme_texts)}\n\nWhich are most relevant?"}
            ],
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        content = json.loads(response.choices[0].message.content)
        return content.get("ids", []) if isinstance(content, dict) else content
    except Exception as e:
        logger.error(f"match_schemes error: {e}")
        return []


async def simplify_text(text: str) -> str:
    """Simplify complex government text to Grade 5 reading level."""
    client = _get_client()
    if not client:
        return f"Here is a simpler version of the document:\n\n{text[:500]}..."

    try:
        response = await client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_SIMPLIFY},
                {"role": "user", "content": text[:3000]}  # Limit context
            ],
            temperature=0.5,
            max_tokens=600
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"simplify_text error: {e}")
        return f"Here is a simpler version of the document:\n\n{text[:500]}..."


async def explain_eligibility(user_profile: dict, eligible_schemes: list) -> str:
    """Generate a human-friendly explanation of eligibility results."""
    client = _get_client()

    scheme_names = [s.get("name", s) if isinstance(s, dict) else s.name for s in eligible_schemes]
    profile_str = f"Age: {user_profile.get('age')}, Income: ₹{user_profile.get('income')}, Category: {user_profile.get('category')}, Location: {user_profile.get('location')}"

    if not client:
        if scheme_names:
            return (
                f"Based on your profile ({profile_str}), you may be eligible for: "
                f"{', '.join(scheme_names)}. "
                "Visit your nearest Common Service Centre (CSC) or the respective scheme's "
                "official website to apply. Carry your Aadhaar card, income certificate, "
                "and category certificate."
            )
        return "Based on the information provided, we couldn't find matching schemes. Try adjusting your criteria or visit a local CSC for guidance."

    try:
        response = await client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_CIVIC},
                {"role": "user", "content": (
                    f"User profile: {profile_str}\n"
                    f"Eligible schemes: {', '.join(scheme_names)}\n\n"
                    "Explain in simple words which schemes this person qualifies for and "
                    "what steps they should take next. Be encouraging."
                )}
            ],
            temperature=0.7,
            max_tokens=400
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"explain_eligibility error: {e}")
        return f"You may be eligible for: {', '.join(scheme_names)}. Visit your nearest CSC to apply."


async def recommend_skills(education: str, interest: str, location: str) -> dict:
    """AI-powered skill and job recommendations."""
    client = _get_client()

    fallback = {
        "recommendations": [
            {"title": "Digital Literacy Program", "type": "training", "description": "Learn basic computer skills, internet usage, and digital payments.", "provider": "PMGDISHA", "location": location},
            {"title": "Tailoring & Fashion Design", "type": "training", "description": "Professional tailoring course with certification.", "provider": "PMKVY Centre", "location": location},
            {"title": "Data Entry Operator", "type": "job", "description": "Entry-level data entry position in government offices.", "provider": "National Career Service", "location": location},
            {"title": "Mobile Phone Repair", "type": "training", "description": "Learn smartphone repair and start your own business.", "provider": "Skill India", "location": location},
            {"title": "Community Health Worker", "type": "job", "description": "Work as an ASHA worker or health volunteer in your community.", "provider": "NHM", "location": location},
        ],
        "ai_summary": f"Based on your {education} education and interest in {interest}, here are relevant opportunities near {location}. These programs are either free or subsidized by the government."
    }

    if not client:
        return fallback

    try:
        response = await client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "system", "content": (
                    "You are a career advisor for underserved communities in India. "
                    "Return a JSON object with two keys: "
                    "'recommendations' (array of objects with title, type (training/job), description, provider, location) "
                    "and 'ai_summary' (a short encouraging paragraph). "
                    "Include both government programs and private opportunities. Max 5 items."
                )},
                {"role": "user", "content": (
                    f"Education: {education}\n"
                    f"Interest: {interest}\n"
                    f"Location: {location}\n\n"
                    "Suggest relevant training programs and jobs."
                )}
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        result = json.loads(response.choices[0].message.content)
        if "recommendations" not in result:
            return fallback
        return result
    except Exception as e:
        logger.error(f"recommend_skills error: {e}")
        return fallback


async def generate_next_steps(text: str) -> str:
    """Generate actionable next steps from a document."""
    client = _get_client()
    if not client:
        return "1. Read through the document carefully.\n2. Note any deadlines mentioned.\n3. Gather the required documents.\n4. Visit your nearest government office or CSC for help."

    try:
        response = await client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "system", "content": "Extract 3-5 actionable next steps from this document. Be specific and simple."},
                {"role": "user", "content": text[:2000]}
            ],
            temperature=0.5,
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"generate_next_steps error: {e}")
        return "1. Read the document carefully.\n2. Note deadlines.\n3. Visit your nearest CSC."


# ─── Fallback Helpers ────────────────────────────────────────────

def _fallback_response(query: str, context: str) -> str:
    """Generate a helpful response without AI when the API is unavailable."""
    query_lower = query.lower()

    if context and context.strip():
        return (
            f"Here's what I found:\n\n{context}\n\n"
            "For more details, visit your nearest Common Service Centre (CSC) or "
            "call the relevant helpline number."
        )

    if any(w in query_lower for w in ["housing", "house", "awas", "pmay"]):
        return (
            "PM Awas Yojana (PMAY) helps families build affordable homes.\n\n"
            "• For families with income below ₹3 lakh (EWS) to ₹18 lakh.\n"
            "• Apply at: pmaymis.gov.in or your nearest municipal office.\n"
            "• Documents: Aadhaar, income proof, bank details.\n"
            "• Helpline: 1800-11-3377"
        )

    if any(w in query_lower for w in ["health", "hospital", "ayushman", "insurance"]):
        return (
            "Ayushman Bharat (PM-JAY) provides free health insurance up to ₹5 lakh.\n\n"
            "• Check eligibility at mera.pmjay.gov.in\n"
            "• Visit any empanelled hospital with your Aadhaar card.\n"
            "• Helpline: 14555"
        )

    if any(w in query_lower for w in ["scholarship", "education", "study"]):
        return (
            "Post Matric Scholarship is available for SC/ST/OBC students.\n\n"
            "• Family income must be below ₹2.5 lakh/year.\n"
            "• Apply at: scholarships.gov.in\n"
            "• Documents: Caste certificate, income proof, marksheet.\n"
            "• Helpline: 0120-6619540"
        )

    if any(w in query_lower for w in ["skill", "job", "training", "kaushal"]):
        return (
            "PM Kaushal Vikas Yojana (PMKVY) offers free skill training.\n\n"
            "• For youth aged 15-45 years.\n"
            "• Free training + certification + placement help.\n"
            "• Register at: pmkvyofficial.org\n"
            "• Helpline: 088000-55555"
        )

    if any(w in query_lower for w in ["farmer", "farm", "rural", "agriculture", "kisan", "crop"]):
        return (
            "MGNREGA guarantees 100 days of employment to rural households.\n\n"
            "• Provides minimum wage for unskilled manual work.\n"
            "• Apply at your nearest Gram Panchayat office.\n"
            "• Documents: Aadhaar card, address proof.\n"
            "• Helpline: 1800-345-22-44\n\n"
            "Also check: PM-KISAN scheme for direct income support to farmers."
        )

    if any(w in query_lower for w in ["employment", "work", "nrega", "mgnrega", "wage"]):
        return (
            "MGNREGA provides 100 days of guaranteed employment per year.\n\n"
            "• Available for adults in rural areas.\n"
            "• Minimum wage payment guaranteed.\n"
            "• Register at your Gram Panchayat for a job card.\n"
            "• Helpline: 1800-345-22-44"
        )

    if any(w in query_lower for w in ["women", "woman", "ujjwala", "gas", "lpg", "cooking"]):
        return (
            "PM Ujjwala Yojana provides free LPG gas connections.\n\n"
            "• For women from BPL (Below Poverty Line) families.\n"
            "• Free LPG connection + first refill.\n"
            "• Apply at your nearest LPG distributor.\n"
            "• Documents: BPL card, Aadhaar, bank passbook.\n"
            "• Helpline: 1800-266-6696"
        )

    if any(w in query_lower for w in ["welfare", "government", "benefit", "sarkari", "yojana", "scheme"]):
        return (
            "Here are some major government schemes available:\n\n"
            "• PM Awas Yojana (PMAY) — Affordable housing assistance\n"
            "• Ayushman Bharat (PM-JAY) — Free health insurance up to Rs 5 lakh\n"
            "• Post Matric Scholarship — For SC/ST/OBC students\n"
            "• PMKVY — Free skill training and certification\n"
            "• MGNREGA — 100 days guaranteed rural employment\n"
            "• PM Ujjwala Yojana — Free LPG connections for BPL families\n\n"
            "Ask me about any specific scheme to learn more!"
        )

    return (
        "Thank you for your question. I can help you with:\n\n"
        "• Government schemes (housing, health, education)\n"
        "• Eligibility checking\n"
        "• Document simplification\n"
        "• Skill and job recommendations\n\n"
        "Try asking things like:\n"
        "- \"Tell me about housing schemes\"\n"
        "- \"Scholarships for SC students\"\n"
        "- \"Free health insurance\"\n"
        "- \"Farmer schemes\"\n\n"
        "Or visit your nearest CSC for in-person help."
    )
