"""
JanAccess AI — FastAPI Application Entry Point.
A voice-first civic intelligence assistant.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables before anything else
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers import assistant, eligibility, document, skills, analytics
from database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

# Ensure static directories exist
Path("static/audio").mkdir(parents=True, exist_ok=True)
Path("static/uploads").mkdir(parents=True, exist_ok=True)
Path("static/documents").mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="JanAccess AI API",
    description="Voice-first civic intelligence assistant for underserved communities.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Mount Static Files for audio/document serving
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS Configuration
cors_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://[::1]:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://[::1]:3000"
]

print(f"INFO: CORS Origins allowed: {cors_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(assistant.router,    prefix="/api/assistant",    tags=["Assistant"])
app.include_router(eligibility.router,  prefix="/api/eligibility",  tags=["Eligibility"])
app.include_router(document.router,     prefix="/api/document",     tags=["Document"])
app.include_router(skills.router,       prefix="/api/skills",       tags=["Skills & Jobs"])
app.include_router(analytics.router,    prefix="/api/analytics",    tags=["Analytics"])


@app.get("/", tags=["Health"])
def read_root():
    """Health check endpoint."""
    return {
        "message": "JanAccess AI Backend is running!",
        "version": "1.0.0",
        "docs": "/docs"
    }
