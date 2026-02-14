from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.main import app as main_app

# Vercel serverless function handler
app = main_app

# Configure CORS for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your Vercel domain after deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# This is the handler Vercel will use
handler = app
