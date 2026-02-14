"""
Analytics Router — Dashboard statistics, admin endpoints, and persona usage.
"""
import logging
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.database import get_db
from backend.models import Interaction, SearchHistory, DocumentAnalysis, Scheme

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/summary")
async def get_analytics_summary(db: Session = Depends(get_db)):
    """
    Returns summary statistics for the analytics dashboard.
    Now includes persona_breakdown.
    """
    total_queries = db.query(Interaction).count()
    total_documents = db.query(DocumentAnalysis).count()
    total_schemes = db.query(Scheme).count()

    # Category breakdown from search history
    category_rows = (
        db.query(SearchHistory.category, func.count(SearchHistory.id))
        .filter(SearchHistory.category.isnot(None))
        .group_by(SearchHistory.category)
        .all()
    )
    category_breakdown = {cat: count for cat, count in category_rows}

    # Persona breakdown from interactions
    persona_rows = (
        db.query(Interaction.persona, func.count(Interaction.id))
        .filter(Interaction.persona.isnot(None))
        .group_by(Interaction.persona)
        .all()
    )
    persona_breakdown = {persona: count for persona, count in persona_rows}

    # Recent queries
    recent = (
        db.query(Interaction)
        .order_by(Interaction.timestamp.desc())
        .limit(10)
        .all()
    )
    recent_queries = [
        {
            "query": i.query,
            "response": (i.response or "")[:100] + "..." if i.response and len(i.response) > 100 else i.response,
            "persona": i.persona,
            "timestamp": str(i.timestamp)
        }
        for i in recent
    ]

    return {
        "total_queries": total_queries,
        "total_documents": total_documents,
        "total_schemes": total_schemes,
        "category_breakdown": category_breakdown,
        "persona_breakdown": persona_breakdown,
        "recent_queries": recent_queries
    }


@router.get("/top-schemes")
async def get_top_schemes(
    limit: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    Admin endpoint: returns the most searched/matched schemes.
    """
    # Parse matched_schemes from SearchHistory and count occurrences
    history = db.query(SearchHistory.matched_schemes).filter(
        SearchHistory.matched_schemes.isnot(None)
    ).all()

    scheme_counts = {}
    for (matched,) in history:
        if matched:
            for name in matched.split(","):
                name = name.strip()
                if name:
                    scheme_counts[name] = scheme_counts.get(name, 0) + 1

    # Sort by count descending
    sorted_schemes = sorted(scheme_counts.items(), key=lambda x: x[1], reverse=True)[:limit]

    return {
        "top_schemes": [
            {"name": name, "search_count": count}
            for name, count in sorted_schemes
        ]
    }


@router.get("/history")
async def get_search_history(
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Returns paginated search history.
    """
    history = (
        db.query(SearchHistory)
        .order_by(SearchHistory.timestamp.desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "id": h.id,
            "query": h.query_text,
            "category": h.category,
            "persona": h.persona,
            "matched_schemes": h.matched_schemes,
            "timestamp": str(h.timestamp)
        }
        for h in history
    ]


@router.get("/persona-usage")
async def get_persona_usage(db: Session = Depends(get_db)):
    """
    GET /analytics/persona-usage
    Returns:
      - most_selected_persona
      - persona_counts — {persona: count}
      - top_topics_per_persona — {persona: [top-3 categories]}
    """
    # Count interactions per persona
    persona_rows = (
        db.query(Interaction.persona, func.count(Interaction.id))
        .filter(Interaction.persona.isnot(None))
        .group_by(Interaction.persona)
        .order_by(func.count(Interaction.id).desc())
        .all()
    )

    persona_counts = {persona: count for persona, count in persona_rows}
    most_selected = persona_rows[0][0] if persona_rows else None

    # Top categories per persona from search_history
    all_persona_categories = (
        db.query(SearchHistory.persona, SearchHistory.category, func.count(SearchHistory.id))
        .filter(SearchHistory.persona.isnot(None), SearchHistory.category.isnot(None))
        .group_by(SearchHistory.persona, SearchHistory.category)
        .order_by(SearchHistory.persona, func.count(SearchHistory.id).desc())
        .all()
    )

    top_topics: dict[str, list[str]] = {}
    for persona, category, _count in all_persona_categories:
        if persona not in top_topics:
            top_topics[persona] = []
        if len(top_topics[persona]) < 3:
            top_topics[persona].append(category)

    return {
        "most_selected_persona": most_selected,
        "persona_counts": persona_counts,
        "top_topics_per_persona": top_topics,
    }
