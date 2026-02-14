# JanAccess AI - Voice-First Civic Intelligence Assistant

A platform designed to help underserved communities access government schemes, public services, and job opportunities using AI-powered voice and text interfaces.

## Tech Stack
- **Frontend:** React (Vite), Tailwind CSS, Framer Motion
- **Backend:** FastAPI (Python), SQLAlchemy, SQLite
- **AI:** OpenAI (GPT-3.5/4), Whisper (Speech-to-Text), gTTS (Text-to-Speech)

## Setup Instructions

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file from `.env.example` and add your `OPENAI_API_KEY`.
5. Seed the database with sample schemes:
   ```bash
   python seed.py
   ```
6. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

## Key Features
- **Voice-First Chat:** Hands-free interaction using speech-to-text and text-to-speech.
- **Scheme Search:** Intelligent retrieval of government schemes.
- **Eligibility Checker:** Rule-based and AI-powered eligibility verification.
- **Document Explainer:** Simplification of complex government notices and forms.
- **Skill/Job Recommendations:** personalized suggestions based on education and interests.

## Deployment
- **Frontend:** Optimized for Vercel.
- **Backend:** Optimized for Render/Railway/Heroku.
- **Database:** Ready for PostgreSQL migration.
