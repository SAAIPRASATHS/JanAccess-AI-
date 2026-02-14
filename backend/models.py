"""
SQLAlchemy ORM models for JanAccess AI.
"""
from sqlalchemy import Column, Integer, String, Text, Float, TIMESTAMP
from datetime import datetime
from backend.database import Base


class Scheme(Base):
    """Government scheme information."""
    __tablename__ = "schemes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    category = Column(String, index=True)          # Education, Health, Housing, etc.
    description = Column(Text)
    eligibility_criteria = Column(Text)
    benefits = Column(Text)
    application_process = Column(Text)
    documents_required = Column(Text)
    contact_info = Column(String)
    min_age = Column(Integer, default=0)
    max_age = Column(Integer, default=100)
    max_income = Column(Float, default=0)           # 0 = no limit
    target_categories = Column(String, default="All")  # Comma-separated: "SC,ST,OBC,General"
    website = Column(String, nullable=True)         # Official portal URL


class Interaction(Base):
    """Chat interaction log."""
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, default="demo_user")
    query = Column(Text, nullable=False)
    response = Column(Text)
    persona = Column(String, nullable=True, index=True)
    timestamp = Column(TIMESTAMP, default=datetime.utcnow)
    voice_file_path = Column(String, nullable=True)


class DocumentAnalysis(Base):
    """Uploaded document analysis results."""
    __tablename__ = "document_analyses"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    content_summary = Column(Text)
    simplification = Column(Text)
    uploaded_at = Column(TIMESTAMP, default=datetime.utcnow)


class SearchHistory(Base):
    """Tracks search queries for analytics."""
    __tablename__ = "search_history"

    id = Column(Integer, primary_key=True, index=True)
    query_text = Column(Text, nullable=False)
    category = Column(String, nullable=True)
    persona = Column(String, nullable=True, index=True)
    matched_schemes = Column(Text, nullable=True)   # Comma-separated scheme names
    timestamp = Column(TIMESTAMP, default=datetime.utcnow)
