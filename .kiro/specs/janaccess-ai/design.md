# JanAccess AI - Technical Design Document

## 1. System Architecture Overview

JanAccess AI follows a modern three-tier architecture with clear separation between presentation, business logic, and data layers. The system is designed as a voice-first platform with AI at its core, enabling natural language interactions for accessing civic services.

### Architecture Layers

**Presentation Layer (Frontend)**
- React-based SPA with Tailwind CSS for responsive UI
- Framer Motion for smooth animations and transitions
- Voice input/output handling through Web Audio API
- Real-time chat interface with persona-aware styling

**Application Layer (Backend)**
- FastAPI REST API with async request handling
- Service-oriented architecture with clear separation of concerns
- AI orchestration layer managing OpenAI, Whisper, and gTTS integrations
- Business logic for eligibility checking and scheme matching

**Data Layer**
- SQLite for demo/development (easy setup, zero configuration)
- PostgreSQL-ready schema for production scaling
- File storage for audio files and uploaded documents
- In-memory caching for frequently accessed data

### Component Interaction Flow

```
User Voice Input → Frontend (React) → Backend API (FastAPI) → AI Services (OpenAI/Whisper)
                                                              ↓
                                                         Database (SQLite)
                                                              ↓
AI Response ← Frontend ← Backend ← gTTS ← OpenAI Response
```


## 2. High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  React Frontend (Vercel)                                  │   │
│  │  - PersonaSelector    - ChatWindow    - VoiceInput       │   │
│  │  - EligibilityForm    - DocumentUpload - Dashboard       │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↕ HTTPS/REST
┌─────────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                           │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  FastAPI Backend (Render)                                 │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐         │   │
│  │  │  Routers   │  │  Services  │  │   Models   │         │   │
│  │  │  - chat    │→ │  - ai      │→ │  - User    │         │   │
│  │  │  - persona │  │  - speech  │  │  - Scheme  │         │   │
│  │  │  - scheme  │  │  - elig.   │  │  - Chat    │         │   │
│  │  └────────────┘  └────────────┘  └────────────┘         │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                      EXTERNAL SERVICES                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   OpenAI     │  │   Whisper    │  │     gTTS     │         │
│  │   GPT-4      │  │   STT API    │  │   TTS API    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                         DATA LAYER                               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  SQLite/PostgreSQL                                        │   │
│  │  - users  - personas  - schemes  - chats  - analytics    │   │
│  └──────────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  File Storage (Static)                                    │   │
│  │  - /audio/*.mp3  - /documents/*.pdf  - /uploads/*        │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow Patterns

**Voice Query Flow**:
1. User speaks → Frontend captures audio → POST /api/chat (audio file)
2. Backend receives audio → Whisper API converts to text
3. Text + persona context → OpenAI API generates response
4. Response text → gTTS converts to audio
5. Backend returns {text, audio_url} → Frontend plays audio

**Eligibility Check Flow**:
1. User provides info via chat → Frontend collects structured data
2. POST /api/eligibility with user data
3. Eligibility engine evaluates against scheme criteria
4. Returns eligibility result + reasoning + next steps

**Document Explainer Flow**:
1. User uploads document → POST /api/document/upload
2. Backend extracts text (OCR if needed)
3. Text sent to OpenAI with "simplify" prompt
4. Returns simplified summary + key points


## 3. Frontend Design

### 3.1 React Component Structure

```
src/
├── main.jsx                    # App entry point
├── App.jsx                     # Root component with routing
├── pages/
│   ├── Home.jsx               # Landing page with persona selection
│   └── Dashboard.jsx          # Main chat interface
├── components/
│   ├── PersonaSelector.jsx    # Persona cards with icons
│   ├── ChatWindow.jsx         # Message display with voice playback
│   ├── VoiceInput.jsx         # Microphone recording UI
│   ├── EligibilityForm.jsx    # Structured data collection
│   ├── DocumentUpload.jsx     # Drag-drop file upload
│   └── SkillJobForm.jsx       # Job/skill matching form
├── services/
│   └── api.js                 # Axios API client
└── assets/
    └── icons/                 # Persona and UI icons
```

### 3.2 Component Design Details

#### PersonaSelector Component
```javascript
// State: selectedPersona, personas[]
// Props: onPersonaSelect(persona)
// Features:
// - Grid layout of persona cards (5 personas)
// - Each card shows icon, title, description
// - Hover animation (scale + shadow)
// - Active state highlighting
// - Responsive: 1 col mobile, 2 col tablet, 3 col desktop
```

**Styling Strategy**:
- Tailwind utility classes for rapid development
- Custom color palette per persona (green=farmer, blue=student, etc.)
- Consistent spacing using Tailwind spacing scale (p-4, m-6, gap-4)
- Responsive breakpoints: sm:, md:, lg:, xl:

**Framer Motion Animations**:
- Card entrance: `initial={{opacity:0, y:20}} animate={{opacity:1, y:0}}`
- Hover effect: `whileHover={{scale:1.05}}`
- Stagger children for sequential card appearance

#### ChatWindow Component
```javascript
// State: messages[], isPlaying, currentAudio
// Props: persona, onSendMessage(text)
// Features:
// - Auto-scroll to latest message
// - Message bubbles (user=right, AI=left)
// - Audio playback controls for AI responses
// - Loading indicator during AI processing
// - Persona-specific AI avatar/color
```

**Message Structure**:
```javascript
{
  id: uuid,
  role: 'user' | 'assistant',
  content: string,
  audioUrl?: string,
  timestamp: Date,
  persona?: string
}
```

**Styling**:
- User messages: bg-blue-500 text-white rounded-l-lg
- AI messages: bg-gray-100 text-gray-900 rounded-r-lg
- Smooth scroll behavior with `scroll-behavior: smooth`
- Max width constraint for readability (max-w-3xl)

#### VoiceInput Component
```javascript
// State: isRecording, audioBlob, recordingTime
// Features:
// - MediaRecorder API for audio capture
// - Visual recording indicator (pulsing red dot)
// - Recording timer display
// - Waveform visualization (optional)
// - Stop/cancel recording controls
```

**Recording Flow**:
1. User clicks mic button → Request microphone permission
2. Start MediaRecorder → Update UI to recording state
3. Capture audio chunks → Store in audioBlob
4. Stop recording → Convert blob to File
5. Upload to backend → Display in chat

**Accessibility**:
- Keyboard shortcuts (Space to record, Esc to cancel)
- Screen reader announcements for recording state
- High contrast recording indicator

#### EligibilityForm Component
```javascript
// State: formData{age, income, location, occupation, etc.}
// Features:
// - Multi-step form with progress indicator
// - Conditional fields based on persona
// - Input validation with error messages
// - Auto-save to localStorage
// - Submit to /api/eligibility endpoint
```

**Form Fields by Persona**:
- Common: age, location, income
- Farmer: land_size, crop_type
- Student: education_level, course
- Job Seeker: skills[], experience
- Senior Citizen: pension_status
- Business Owner: business_type, employees

#### DocumentUpload Component
```javascript
// State: uploadedFile, uploadProgress, isProcessing
// Features:
// - Drag-and-drop zone with visual feedback
// - File type validation (PDF, JPG, PNG)
// - File size validation (max 10MB)
// - Upload progress bar
// - Preview of uploaded document
```

### 3.3 Styling Strategy

**Tailwind Configuration** (`tailwind.config.js`):
```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        farmer: '#10b981',    // green
        student: '#3b82f6',   // blue
        jobseeker: '#f59e0b', // amber
        senior: '#8b5cf6',    // purple
        business: '#ef4444'   // red
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      }
    }
  }
}
```

**Responsive Design Approach**:
- Mobile-first design (base styles for mobile)
- Breakpoint strategy: sm(640px), md(768px), lg(1024px)
- Touch-friendly targets (min 44x44px)
- Collapsible navigation for mobile

### 3.4 Framer Motion Animation Patterns

**Page Transitions**:
```javascript
const pageVariants = {
  initial: { opacity: 0, x: -20 },
  animate: { opacity: 1, x: 0 },
  exit: { opacity: 0, x: 20 }
}
```

**Message Animations**:
```javascript
const messageVariants = {
  hidden: { opacity: 0, y: 20, scale: 0.95 },
  visible: { opacity: 1, y: 0, scale: 1 }
}
```

**Loading States**:
- Skeleton screens with shimmer effect
- Spinner with rotation animation
- Typing indicator (three dots bouncing)


## 4. Backend Architecture

### 4.1 FastAPI Project Structure

```
backend/
├── main.py                      # FastAPI app initialization, CORS, middleware
├── database.py                  # SQLAlchemy engine, session management
├── models.py                    # SQLAlchemy ORM models
├── schemas.py                   # Pydantic request/response schemas
├── persona_config.py            # Persona definitions and prompts
├── seed.py                      # Database seeding script
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variable template
├── routers/
│   ├── __init__.py
│   ├── chat.py                 # Chat and voice endpoints
│   ├── persona.py              # Persona management
│   ├── scheme.py               # Scheme search and details
│   ├── eligibility.py          # Eligibility checking
│   ├── document.py             # Document upload and explanation
│   ├── job.py                  # Job and skill matching
│   └── analytics.py            # Analytics and reporting
├── services/
│   ├── __init__.py
│   ├── ai_service.py           # OpenAI integration
│   ├── speech_service.py       # Whisper + gTTS integration
│   ├── eligibility_engine.py   # Eligibility logic
│   └── document_service.py     # Document processing
└── static/
    ├── audio/                  # Generated TTS audio files
    ├── documents/              # Processed documents
    └── uploads/                # User uploaded files
```

### 4.2 Main Application Setup (`main.py`)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers import chat, persona, scheme, eligibility, document, analytics
from database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="JanAccess AI API",
    description="Voice-first civic intelligence platform",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://janaccess.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(persona.router, prefix="/api/persona", tags=["persona"])
app.include_router(scheme.router, prefix="/api/schemes", tags=["schemes"])
app.include_router(eligibility.router, prefix="/api/eligibility", tags=["eligibility"])
app.include_router(document.router, prefix="/api/document", tags=["document"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])

@app.get("/")
async def root():
    return {"message": "JanAccess AI API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### 4.3 Router Layer Design

#### Chat Router (`routers/chat.py`)
```python
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from services.ai_service import AIService
from services.speech_service import SpeechService
from database import get_db
import schemas

router = APIRouter()

@router.post("/message", response_model=schemas.ChatResponse)
async def send_message(
    request: schemas.ChatRequest,
    db: Session = Depends(get_db)
):
    """Handle text-based chat messages"""
    # Get persona context
    # Call AI service with persona-aware prompt
    # Save to database
    # Return response
    pass

@router.post("/voice", response_model=schemas.ChatResponse)
async def send_voice(
    audio: UploadFile = File(...),
    persona: str = Form(...),
    db: Session = Depends(get_db)
):
    """Handle voice input with STT + AI + TTS"""
    # Convert audio to text (Whisper)
    # Process with AI service
    # Convert response to speech (gTTS)
    # Return text + audio URL
    pass

@router.get("/history/{user_id}")
async def get_chat_history(
    user_id: str,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Retrieve chat history for a user"""
    pass
```

#### Eligibility Router (`routers/eligibility.py`)
```python
@router.post("/check", response_model=schemas.EligibilityResponse)
async def check_eligibility(
    request: schemas.EligibilityRequest,
    db: Session = Depends(get_db)
):
    """Check user eligibility for schemes"""
    # Extract user data
    # Get relevant schemes from database
    # Run eligibility engine
    # Return matched schemes with reasoning
    pass

@router.get("/schemes/{scheme_id}/requirements")
async def get_scheme_requirements(scheme_id: int, db: Session = Depends(get_db)):
    """Get detailed requirements for a scheme"""
    pass
```

### 4.4 Service Layer Design

#### AI Service (`services/ai_service.py`)
```python
import openai
from persona_config import PERSONA_PROMPTS

class AIService:
    def __init__(self, api_key: str):
        openai.api_key = api_key
    
    def generate_response(
        self,
        user_message: str,
        persona: str,
        conversation_history: list = None
    ) -> str:
        """Generate AI response with persona context"""
        
        # Build system prompt with persona
        system_prompt = self._build_system_prompt(persona)
        
        # Build messages array
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history
        if conversation_history:
            messages.extend(conversation_history)
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    
    def _build_system_prompt(self, persona: str) -> str:
        """Build persona-specific system prompt"""
        base_prompt = """You are JanAccess AI, a helpful assistant that helps 
        Indian citizens access government schemes and services."""
        
        persona_context = PERSONA_PROMPTS.get(persona, "")
        
        return f"{base_prompt}\n\n{persona_context}"
    
    def extract_scheme_info(self, query: str) -> dict:
        """Extract structured information from user query"""
        # Use OpenAI function calling to extract entities
        pass
```

#### Speech Service (`services/speech_service.py`)
```python
import openai
from gtts import gTTS
import uuid
import os

class SpeechService:
    def __init__(self, whisper_api_key: str):
        self.whisper_api_key = whisper_api_key
    
    async def speech_to_text(self, audio_file_path: str) -> str:
        """Convert audio to text using Whisper"""
        with open(audio_file_path, "rb") as audio_file:
            transcript = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file,
                language="hi"  # Hindi, can be dynamic
            )
        return transcript.text
    
    def text_to_speech(self, text: str, language: str = "hi") -> str:
        """Convert text to speech using gTTS"""
        # Generate unique filename
        audio_id = str(uuid.uuid4())
        audio_path = f"static/audio/{audio_id}.mp3"
        
        # Generate speech
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(audio_path)
        
        # Return URL path
        return f"/static/audio/{audio_id}.mp3"
    
    def cleanup_old_audio(self, max_age_hours: int = 24):
        """Delete audio files older than specified hours"""
        # Cleanup logic for disk space management
        pass
```

#### Eligibility Engine (`services/eligibility_engine.py`)
```python
class EligibilityEngine:
    def __init__(self, db_session):
        self.db = db_session
    
    def check_eligibility(self, user_data: dict, scheme_id: int = None) -> list:
        """
        Check user eligibility against schemes
        Returns list of (scheme, eligibility_status, reasoning)
        """
        # Get schemes to check
        if scheme_id:
            schemes = [self.db.query(Scheme).get(scheme_id)]
        else:
            schemes = self.db.query(Scheme).all()
        
        results = []
        for scheme in schemes:
            is_eligible, reasoning = self._evaluate_scheme(user_data, scheme)
            results.append({
                "scheme": scheme,
                "eligible": is_eligible,
                "reasoning": reasoning,
                "confidence": self._calculate_confidence(user_data, scheme)
            })
        
        # Sort by eligibility and confidence
        results.sort(key=lambda x: (x["eligible"], x["confidence"]), reverse=True)
        
        return results
    
    def _evaluate_scheme(self, user_data: dict, scheme) -> tuple:
        """Evaluate single scheme eligibility"""
        criteria = scheme.eligibility_criteria  # JSON field
        
        checks = []
        
        # Age check
        if "age_min" in criteria:
            if user_data.get("age", 0) < criteria["age_min"]:
                return False, f"Age must be at least {criteria['age_min']}"
            checks.append("age_ok")
        
        # Income check
        if "income_max" in criteria:
            if user_data.get("income", float('inf')) > criteria["income_max"]:
                return False, f"Income must be below {criteria['income_max']}"
            checks.append("income_ok")
        
        # Location check
        if "states" in criteria:
            if user_data.get("state") not in criteria["states"]:
                return False, f"Scheme available only in: {', '.join(criteria['states'])}"
            checks.append("location_ok")
        
        # Persona check
        if "personas" in criteria:
            if user_data.get("persona") not in criteria["personas"]:
                return False, "Scheme not applicable for your profile"
            checks.append("persona_ok")
        
        # All checks passed
        return True, f"Eligible: {', '.join(checks)}"
    
    def _calculate_confidence(self, user_data: dict, scheme) -> float:
        """Calculate confidence score (0-1) for eligibility"""
        # Based on completeness of user data
        required_fields = scheme.eligibility_criteria.keys()
        provided_fields = [f for f in required_fields if f in user_data]
        return len(provided_fields) / len(required_fields) if required_fields else 1.0
```


## 5. AI Integration Design

### 5.1 OpenAI Integration Strategy

#### Persona-Based Prompt Engineering

**System Prompt Template**:
```python
PERSONA_PROMPTS = {
    "farmer": """
    You are assisting a farmer in India. Use simple language and focus on:
    - Agricultural schemes and subsidies
    - Crop insurance and weather information
    - Market prices and selling opportunities
    - Farming techniques and best practices
    
    Keep responses concise and practical. Use examples from farming context.
    Avoid technical jargon. Speak respectfully using "aap" form.
    """,
    
    "student": """
    You are assisting a student in India. Focus on:
    - Scholarships and educational financial aid
    - Skill development programs and courses
    - Career guidance and higher education options
    - Exam preparation resources
    
    Be encouraging and motivational. Use clear, educational language.
    Provide step-by-step guidance for applications.
    """,
    
    "jobseeker": """
    You are assisting a job seeker in India. Focus on:
    - Job opportunities and employment schemes
    - Skill training and certification programs
    - Resume building and interview preparation
    - Career transition guidance
    
    Be supportive and action-oriented. Provide practical next steps.
    Focus on matching skills with opportunities.
    """,
    
    "senior": """
    You are assisting a senior citizen in India. Focus on:
    - Pension schemes and retirement benefits
    - Healthcare schemes and medical support
    - Senior citizen cards and concessions
    - Tax benefits and financial planning
    
    Use very simple language. Be patient and respectful.
    Break down complex processes into small steps.
    Avoid abbreviations and technical terms.
    """,
    
    "business": """
    You are assisting a small business owner in India. Focus on:
    - MSME schemes and business loans
    - Tax information and compliance
    - Licensing and registration guidance
    - Market access and growth opportunities
    
    Be professional and efficient. Provide actionable business advice.
    Focus on practical implementation and ROI.
    """
}
```

#### Function Calling for Structured Data

```python
SCHEME_EXTRACTION_FUNCTION = {
    "name": "extract_scheme_query",
    "description": "Extract structured information from user's scheme query",
    "parameters": {
        "type": "object",
        "properties": {
            "intent": {
                "type": "string",
                "enum": ["search_scheme", "check_eligibility", "explain_scheme", "apply_guidance"],
                "description": "User's primary intent"
            },
            "scheme_category": {
                "type": "string",
                "enum": ["financial_aid", "subsidy", "loan", "training", "healthcare", "pension"],
                "description": "Category of scheme user is interested in"
            },
            "user_context": {
                "type": "object",
                "properties": {
                    "age": {"type": "integer"},
                    "income": {"type": "number"},
                    "location": {"type": "string"},
                    "occupation": {"type": "string"}
                }
            }
        },
        "required": ["intent"]
    }
}
```

### 5.2 Whisper Speech-to-Text Flow

```
Audio Input (User) 
    ↓
Frontend captures audio via MediaRecorder
    ↓
Audio blob converted to File (WAV/MP3)
    ↓
POST /api/chat/voice with multipart/form-data
    ↓
Backend saves temporary file
    ↓
Whisper API call with audio file
    ↓
Transcribed text returned
    ↓
Text processed by OpenAI
    ↓
Cleanup temporary audio file
```

**Implementation Details**:
```python
async def process_voice_input(audio_file: UploadFile) -> str:
    # Save uploaded file temporarily
    temp_path = f"temp/{uuid.uuid4()}.mp3"
    with open(temp_path, "wb") as f:
        f.write(await audio_file.read())
    
    # Call Whisper API
    try:
        transcript = await speech_service.speech_to_text(temp_path)
    finally:
        # Cleanup temp file
        os.remove(temp_path)
    
    return transcript
```

**Error Handling**:
- Audio too short (< 1 second): Return error message
- Audio too long (> 25MB): Chunk and process separately
- Whisper API failure: Fallback to text input prompt
- Unsupported format: Convert using ffmpeg

### 5.3 gTTS Text-to-Speech Flow

```
AI Response Text
    ↓
Detect language (Hindi/English)
    ↓
gTTS generation with language parameter
    ↓
Save MP3 to static/audio/{uuid}.mp3
    ↓
Return audio URL in response
    ↓
Frontend plays audio via HTML5 Audio API
    ↓
Background cleanup job (delete files > 24h old)
```

**Implementation**:
```python
def generate_audio_response(text: str, language: str = "hi") -> dict:
    # Generate audio
    audio_url = speech_service.text_to_speech(text, language)
    
    # Return both text and audio
    return {
        "text": text,
        "audio_url": f"{BASE_URL}{audio_url}",
        "language": language
    }
```

**Optimization Strategies**:
- Cache common responses (greetings, FAQs)
- Compress audio files (reduce bitrate for mobile)
- Use CDN for audio delivery in production
- Implement audio streaming for long responses

### 5.4 Conversation Context Management

```python
class ConversationManager:
    def __init__(self, max_history: int = 10):
        self.max_history = max_history
    
    def build_context(self, user_id: str, db_session) -> list:
        """Build conversation context from database"""
        # Get recent messages
        messages = db_session.query(ChatMessage)\
            .filter(ChatMessage.user_id == user_id)\
            .order_by(ChatMessage.timestamp.desc())\
            .limit(self.max_history)\
            .all()
        
        # Convert to OpenAI format
        context = []
        for msg in reversed(messages):
            context.append({
                "role": msg.role,
                "content": msg.content
            })
        
        return context
    
    def should_reset_context(self, last_message_time, current_time) -> bool:
        """Reset context if conversation is stale (> 30 minutes)"""
        return (current_time - last_message_time).seconds > 1800
```


## 6. Database Schema

### 6.1 SQLAlchemy Models (`models.py`)

```python
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)  # UUID
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    
    # User profile
    persona = Column(String, nullable=True)  # Current persona
    language = Column(String, default="hi")  # Preferred language
    
    # Demographics (optional, for eligibility)
    age = Column(Integer, nullable=True)
    income = Column(Float, nullable=True)
    location = Column(String, nullable=True)
    state = Column(String, nullable=True)
    occupation = Column(String, nullable=True)
    
    # Relationships
    chat_messages = relationship("ChatMessage", back_populates="user")
    eligibility_checks = relationship("EligibilityCheck", back_populates="user")
    
class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id"))
    
    role = Column(String)  # 'user' or 'assistant'
    content = Column(Text)
    audio_url = Column(String, nullable=True)
    
    persona = Column(String)  # Persona active during this message
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Metadata
    input_type = Column(String)  # 'text' or 'voice'
    processing_time = Column(Float, nullable=True)  # Seconds
    
    # Relationships
    user = relationship("User", back_populates="chat_messages")

class Scheme(Base):
    __tablename__ = "schemes"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Basic info
    name = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String)  # 'financial_aid', 'subsidy', 'loan', etc.
    
    # Eligibility
    eligibility_criteria = Column(JSON)  # Structured criteria
    target_personas = Column(JSON)  # List of applicable personas
    
    # Details
    benefits = Column(Text)
    required_documents = Column(JSON)  # List of documents
    application_process = Column(Text)
    official_url = Column(String)
    
    # Metadata
    government_level = Column(String)  # 'central', 'state', 'district'
    state = Column(String, nullable=True)  # If state-specific
    department = Column(String)
    
    # Status
    is_active = Column(Boolean, default=True)
    deadline = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    eligibility_checks = relationship("EligibilityCheck", back_populates="scheme")

class EligibilityCheck(Base):
    __tablename__ = "eligibility_checks"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id"))
    scheme_id = Column(Integer, ForeignKey("schemes.id"))
    
    # Result
    is_eligible = Column(Boolean)
    confidence_score = Column(Float)  # 0.0 to 1.0
    reasoning = Column(Text)
    
    # User data at time of check
    user_data_snapshot = Column(JSON)
    
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="eligibility_checks")
    scheme = relationship("Scheme", back_populates="eligibility_checks")

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id"))
    
    # File info
    filename = Column(String)
    file_path = Column(String)
    file_size = Column(Integer)  # Bytes
    file_type = Column(String)  # 'pdf', 'image'
    
    # Processing
    extracted_text = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    key_points = Column(JSON, nullable=True)
    
    # Metadata
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime)  # Auto-delete after 24h

class Analytics(Base):
    __tablename__ = "analytics"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Event tracking
    event_type = Column(String)  # 'query', 'eligibility_check', 'document_upload', etc.
    persona = Column(String, nullable=True)
    
    # Aggregated data
    metadata = Column(JSON)  # Flexible event data
    
    timestamp = Column(DateTime, default=datetime.utcnow)
    date = Column(String)  # YYYY-MM-DD for daily aggregation
```

### 6.2 Pydantic Schemas (`schemas.py`)

```python
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ChatRequest(BaseModel):
    user_id: str
    message: str
    persona: str
    input_type: str = "text"

class ChatResponse(BaseModel):
    message_id: int
    content: str
    audio_url: Optional[str] = None
    timestamp: datetime
    processing_time: float

class EligibilityRequest(BaseModel):
    user_id: str
    persona: str
    age: Optional[int] = None
    income: Optional[float] = None
    location: Optional[str] = None
    state: Optional[str] = None
    occupation: Optional[str] = None
    additional_data: Optional[dict] = None

class SchemeInfo(BaseModel):
    id: int
    name: str
    description: str
    category: str
    benefits: str
    official_url: Optional[str]

class EligibilityResult(BaseModel):
    scheme: SchemeInfo
    eligible: bool
    confidence: float
    reasoning: str

class EligibilityResponse(BaseModel):
    results: List[EligibilityResult]
    total_checked: int
    eligible_count: int

class DocumentUploadResponse(BaseModel):
    document_id: int
    filename: str
    summary: str
    key_points: List[str]
    expires_at: datetime

class AnalyticsResponse(BaseModel):
    total_users: int
    total_queries: int
    queries_by_persona: dict
    top_schemes: List[dict]
    eligibility_checks: int
```

### 6.3 Database Initialization

```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./janaccess_ai.db")

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency for routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 6.4 Sample Data Seeding (`seed.py`)

```python
from database import SessionLocal, engine
from models import Base, Scheme
import json

def seed_schemes():
    db = SessionLocal()
    
    schemes = [
        {
            "name": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
            "description": "Direct income support of ₹6000 per year to farmer families",
            "category": "financial_aid",
            "eligibility_criteria": {
                "personas": ["farmer"],
                "land_ownership": "required",
                "income_max": 200000
            },
            "target_personas": ["farmer"],
            "benefits": "₹2000 every 4 months directly to bank account",
            "required_documents": ["Aadhaar", "Bank Account", "Land Records"],
            "application_process": "Apply online at pmkisan.gov.in or visit nearest CSC",
            "official_url": "https://pmkisan.gov.in",
            "government_level": "central",
            "department": "Ministry of Agriculture"
        },
        {
            "name": "National Scholarship Portal",
            "description": "Various scholarships for students from different backgrounds",
            "category": "financial_aid",
            "eligibility_criteria": {
                "personas": ["student"],
                "age_min": 16,
                "age_max": 25,
                "income_max": 800000
            },
            "target_personas": ["student"],
            "benefits": "₹10,000 to ₹50,000 per year based on course",
            "required_documents": ["Aadhaar", "Income Certificate", "Marksheets"],
            "application_process": "Register on scholarships.gov.in and apply",
            "official_url": "https://scholarships.gov.in",
            "government_level": "central",
            "department": "Ministry of Education"
        }
        # Add more schemes...
    ]
    
    for scheme_data in schemes:
        scheme = Scheme(**scheme_data)
        db.add(scheme)
    
    db.commit()
    db.close()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    seed_schemes()
    print("Database seeded successfully!")
```


## 7. API Endpoints

### 7.1 Chat Endpoints

#### POST /api/chat/message
**Description**: Send text message to AI assistant

**Request**:
```json
{
  "user_id": "uuid-string",
  "message": "What schemes are available for farmers?",
  "persona": "farmer"
}
```

**Response**:
```json
{
  "message_id": 123,
  "content": "There are several schemes for farmers including PM-KISAN...",
  "audio_url": "/static/audio/abc-123.mp3",
  "timestamp": "2026-02-14T10:30:00Z",
  "processing_time": 2.5
}
```

#### POST /api/chat/voice
**Description**: Send voice message (multipart form data)

**Request**:
```
Content-Type: multipart/form-data
- audio: File (audio/mp3, audio/wav)
- user_id: string
- persona: string
```

**Response**: Same as /message endpoint

#### GET /api/chat/history/{user_id}
**Description**: Retrieve chat history

**Query Parameters**:
- limit: int (default: 50)
- offset: int (default: 0)

**Response**:
```json
{
  "messages": [
    {
      "id": 123,
      "role": "user",
      "content": "Hello",
      "timestamp": "2026-02-14T10:30:00Z"
    },
    {
      "id": 124,
      "role": "assistant",
      "content": "Namaste! How can I help you?",
      "audio_url": "/static/audio/xyz.mp3",
      "timestamp": "2026-02-14T10:30:05Z"
    }
  ],
  "total": 100,
  "has_more": true
}
```

### 7.2 Persona Endpoints

#### GET /api/persona/list
**Description**: Get available personas

**Response**:
```json
{
  "personas": [
    {
      "id": "farmer",
      "name": "Farmer",
      "description": "Agricultural workers and landowners",
      "icon": "🌾",
      "color": "#10b981"
    },
    {
      "id": "student",
      "name": "Student",
      "description": "Students seeking education support",
      "icon": "🎓",
      "color": "#3b82f6"
    }
  ]
}
```

#### POST /api/persona/select
**Description**: Set user's active persona

**Request**:
```json
{
  "user_id": "uuid-string",
  "persona": "farmer"
}
```

**Response**:
```json
{
  "success": true,
  "persona": "farmer",
  "message": "Persona updated successfully"
}
```

### 7.3 Scheme Endpoints

#### GET /api/schemes/search
**Description**: Search government schemes

**Query Parameters**:
- q: string (search query)
- persona: string (filter by persona)
- category: string (filter by category)
- limit: int (default: 10)

**Response**:
```json
{
  "schemes": [
    {
      "id": 1,
      "name": "PM-KISAN",
      "description": "Direct income support for farmers",
      "category": "financial_aid",
      "benefits": "₹6000 per year",
      "official_url": "https://pmkisan.gov.in"
    }
  ],
  "total": 25,
  "page": 1
}
```

#### GET /api/schemes/{scheme_id}
**Description**: Get detailed scheme information

**Response**:
```json
{
  "id": 1,
  "name": "PM-KISAN",
  "description": "Direct income support for farmers",
  "category": "financial_aid",
  "eligibility_criteria": {
    "personas": ["farmer"],
    "land_ownership": "required"
  },
  "benefits": "₹6000 per year in 3 installments",
  "required_documents": ["Aadhaar", "Bank Account", "Land Records"],
  "application_process": "Step-by-step guide...",
  "official_url": "https://pmkisan.gov.in",
  "deadline": null
}
```

### 7.4 Eligibility Endpoints

#### POST /api/eligibility/check
**Description**: Check eligibility for schemes

**Request**:
```json
{
  "user_id": "uuid-string",
  "persona": "farmer",
  "age": 45,
  "income": 150000,
  "location": "Punjab",
  "state": "Punjab",
  "occupation": "farmer",
  "additional_data": {
    "land_size": 2.5,
    "crop_type": "wheat"
  }
}
```

**Response**:
```json
{
  "results": [
    {
      "scheme": {
        "id": 1,
        "name": "PM-KISAN",
        "description": "Direct income support",
        "category": "financial_aid",
        "benefits": "₹6000 per year",
        "official_url": "https://pmkisan.gov.in"
      },
      "eligible": true,
      "confidence": 0.95,
      "reasoning": "Eligible: age_ok, income_ok, location_ok, persona_ok"
    },
    {
      "scheme": {
        "id": 5,
        "name": "Crop Insurance Scheme",
        "description": "Insurance for crop damage",
        "category": "insurance",
        "benefits": "Up to 100% crop value coverage",
        "official_url": "https://pmfby.gov.in"
      },
      "eligible": true,
      "confidence": 0.88,
      "reasoning": "Eligible: persona_ok, land_ownership_ok"
    }
  ],
  "total_checked": 15,
  "eligible_count": 2
}
```

#### GET /api/eligibility/history/{user_id}
**Description**: Get user's eligibility check history

**Response**:
```json
{
  "checks": [
    {
      "id": 1,
      "scheme_name": "PM-KISAN",
      "eligible": true,
      "confidence": 0.95,
      "timestamp": "2026-02-14T10:30:00Z"
    }
  ],
  "total": 5
}
```

### 7.5 Document Endpoints

#### POST /api/document/upload
**Description**: Upload document for explanation

**Request**:
```
Content-Type: multipart/form-data
- file: File (PDF, JPG, PNG)
- user_id: string
```

**Response**:
```json
{
  "document_id": 42,
  "filename": "scheme_document.pdf",
  "summary": "This document explains the PM-KISAN scheme eligibility...",
  "key_points": [
    "Eligibility: All farmer families with cultivable land",
    "Benefit: ₹6000 per year in 3 installments",
    "Application: Online at pmkisan.gov.in"
  ],
  "expires_at": "2026-02-15T10:30:00Z"
}
```

#### POST /api/document/explain
**Description**: Ask questions about uploaded document

**Request**:
```json
{
  "document_id": 42,
  "question": "What documents are required for application?"
}
```

**Response**:
```json
{
  "answer": "According to the document, you need: 1) Aadhaar card, 2) Bank account details, 3) Land ownership records",
  "confidence": 0.92
}
```

### 7.6 Job & Skill Endpoints

#### POST /api/jobs/match
**Description**: Match user with relevant jobs

**Request**:
```json
{
  "user_id": "uuid-string",
  "skills": ["data entry", "computer basics"],
  "location": "Delhi",
  "experience_years": 2
}
```

**Response**:
```json
{
  "jobs": [
    {
      "id": 1,
      "title": "Data Entry Operator",
      "company": "Government Office",
      "location": "Delhi",
      "salary_range": "15000-20000",
      "required_skills": ["data entry", "MS Office"],
      "match_score": 0.85
    }
  ],
  "total": 10
}
```

#### POST /api/skills/recommend
**Description**: Recommend skill development programs

**Request**:
```json
{
  "user_id": "uuid-string",
  "current_skills": ["basic computer"],
  "target_role": "web developer"
}
```

**Response**:
```json
{
  "recommendations": [
    {
      "program_name": "PMKVY Web Development Course",
      "provider": "National Skill Development Corporation",
      "duration": "3 months",
      "cost": "Free",
      "skills_covered": ["HTML", "CSS", "JavaScript"],
      "certification": true,
      "enrollment_url": "https://pmkvyofficial.org"
    }
  ],
  "skill_gap": ["HTML", "CSS", "JavaScript", "React"]
}
```

### 7.7 Analytics Endpoints

#### GET /api/analytics/dashboard
**Description**: Get analytics dashboard data (admin only)

**Response**:
```json
{
  "total_users": 1250,
  "total_queries": 5430,
  "queries_by_persona": {
    "farmer": 1200,
    "student": 1800,
    "jobseeker": 1500,
    "senior": 600,
    "business": 330
  },
  "top_schemes": [
    {
      "scheme_name": "PM-KISAN",
      "views": 450,
      "eligibility_checks": 320
    },
    {
      "scheme_name": "National Scholarship Portal",
      "views": 380,
      "eligibility_checks": 290
    }
  ],
  "eligibility_checks": 2100,
  "document_uploads": 450,
  "average_response_time": 3.2
}
```

#### POST /api/analytics/event
**Description**: Track analytics event

**Request**:
```json
{
  "event_type": "scheme_view",
  "persona": "farmer",
  "metadata": {
    "scheme_id": 1,
    "scheme_name": "PM-KISAN"
  }
}
```

**Response**:
```json
{
  "success": true,
  "event_id": 12345
}
```


## 8. Voice Processing Workflow

### 8.1 End-to-End Voice Interaction Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ STEP 1: Voice Input Capture (Frontend)                          │
├─────────────────────────────────────────────────────────────────┤
│ User clicks microphone button                                    │
│   ↓                                                              │
│ Request microphone permission (navigator.mediaDevices)          │
│   ↓                                                              │
│ Start MediaRecorder with audio constraints                      │
│   ↓                                                              │
│ Capture audio chunks in real-time                               │
│   ↓                                                              │
│ Display recording indicator (pulsing animation)                 │
│   ↓                                                              │
│ User stops recording or auto-stop after 60 seconds              │
│   ↓                                                              │
│ Combine chunks into Blob                                        │
│   ↓                                                              │
│ Convert Blob to File object (audio.mp3)                         │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 2: Upload to Backend                                       │
├─────────────────────────────────────────────────────────────────┤
│ Create FormData with audio file + metadata                      │
│   ↓                                                              │
│ POST /api/chat/voice (multipart/form-data)                      │
│   ↓                                                              │
│ Show loading state in UI                                        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 3: Speech-to-Text (Backend)                                │
├─────────────────────────────────────────────────────────────────┤
│ Receive audio file in FastAPI endpoint                          │
│   ↓                                                              │
│ Save to temporary location (temp/{uuid}.mp3)                    │
│   ↓                                                              │
│ Validate file size (< 25MB) and format                          │
│   ↓                                                              │
│ Call Whisper API with audio file                                │
│   - model: "whisper-1"                                           │
│   - language: "hi" (Hindi) or auto-detect                       │
│   ↓                                                              │
│ Receive transcribed text                                        │
│   ↓                                                              │
│ Delete temporary audio file                                     │
│   ↓                                                              │
│ Log transcription for analytics                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 4: AI Processing (Backend)                                 │
├─────────────────────────────────────────────────────────────────┤
│ Get user's conversation history from database                   │
│   ↓                                                              │
│ Build persona-specific system prompt                            │
│   ↓                                                              │
│ Construct messages array:                                       │
│   - System prompt with persona context                          │
│   - Conversation history (last 10 messages)                     │
│   - Current user message (transcribed text)                     │
│   ↓                                                              │
│ Call OpenAI Chat Completion API                                 │
│   - model: "gpt-4"                                               │
│   - temperature: 0.7                                             │
│   - max_tokens: 500                                              │
│   ↓                                                              │
│ Receive AI response text                                        │
│   ↓                                                              │
│ Save user message and AI response to database                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 5: Text-to-Speech (Backend)                                │
├─────────────────────────────────────────────────────────────────┤
│ Detect response language (Hindi/English)                        │
│   ↓                                                              │
│ Generate unique audio ID (UUID)                                 │
│   ↓                                                              │
│ Call gTTS with response text                                    │
│   - lang: "hi" or "en"                                           │
│   - slow: False                                                  │
│   ↓                                                              │
│ Save audio to static/audio/{uuid}.mp3                           │
│   ↓                                                              │
│ Generate public URL for audio file                              │
│   ↓                                                              │
│ Schedule cleanup job (delete after 24 hours)                    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 6: Response to Frontend                                    │
├─────────────────────────────────────────────────────────────────┤
│ Return JSON response:                                            │
│   {                                                              │
│     "message_id": 123,                                           │
│     "content": "AI response text...",                            │
│     "audio_url": "/static/audio/abc-123.mp3",                   │
│     "timestamp": "2026-02-14T10:30:00Z",                        │
│     "processing_time": 4.2                                       │
│   }                                                              │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 7: Audio Playback (Frontend)                               │
├─────────────────────────────────────────────────────────────────┤
│ Receive response from backend                                   │
│   ↓                                                              │
│ Display text message in chat window                             │
│   ↓                                                              │
│ Create Audio object with audio_url                              │
│   ↓                                                              │
│ Auto-play audio response                                        │
│   ↓                                                              │
│ Show audio controls (pause, replay, speed)                      │
│   ↓                                                              │
│ Update UI when audio finishes playing                           │
└─────────────────────────────────────────────────────────────────┘
```

### 8.2 Frontend Voice Implementation

```javascript
// VoiceInput.jsx
import { useState, useRef } from 'react';

export default function VoiceInput({ onVoiceMessage, persona }) {
  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);
  const timerRef = useRef(null);

  const startRecording = async () => {
    try {
      // Request microphone access
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          sampleRate: 44100
        } 
      });

      // Create MediaRecorder
      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm'
      });

      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      // Collect audio chunks
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };

      // Handle recording stop
      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(chunksRef.current, { type: 'audio/webm' });
        const audioFile = new File([audioBlob], 'voice.webm', { type: 'audio/webm' });
        
        // Upload to backend
        await onVoiceMessage(audioFile);
        
        // Cleanup
        stream.getTracks().forEach(track => track.stop());
        setRecordingTime(0);
      };

      // Start recording
      mediaRecorder.start(100); // Collect data every 100ms
      setIsRecording(true);

      // Start timer
      timerRef.current = setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);

      // Auto-stop after 60 seconds
      setTimeout(() => {
        if (mediaRecorderRef.current?.state === 'recording') {
          stopRecording();
        }
      }, 60000);

    } catch (error) {
      console.error('Microphone access denied:', error);
      alert('Please allow microphone access to use voice input');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current?.state === 'recording') {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      clearInterval(timerRef.current);
    }
  };

  return (
    <div className="voice-input">
      {!isRecording ? (
        <button onClick={startRecording} className="mic-button">
          🎤 Hold to Speak
        </button>
      ) : (
        <div className="recording-indicator">
          <div className="pulse-dot" />
          <span>Recording... {recordingTime}s</span>
          <button onClick={stopRecording}>Stop</button>
        </div>
      )}
    </div>
  );
}
```

### 8.3 Backend Voice Processing

```python
# routers/chat.py
from fastapi import APIRouter, UploadFile, File, Form, Depends
from services.speech_service import SpeechService
from services.ai_service import AIService
import uuid
import os

router = APIRouter()

@router.post("/voice")
async def process_voice_message(
    audio: UploadFile = File(...),
    user_id: str = Form(...),
    persona: str = Form(...),
    db: Session = Depends(get_db)
):
    start_time = time.time()
    
    # Save uploaded audio temporarily
    temp_id = str(uuid.uuid4())
    temp_path = f"temp/{temp_id}.webm"
    
    with open(temp_path, "wb") as f:
        content = await audio.read()
        f.write(content)
    
    try:
        # Step 1: Speech to Text
        speech_service = SpeechService()
        transcribed_text = await speech_service.speech_to_text(temp_path)
        
        # Step 2: AI Processing
        ai_service = AIService()
        
        # Get conversation history
        history = get_conversation_history(user_id, db)
        
        # Generate AI response
        ai_response = ai_service.generate_response(
            user_message=transcribed_text,
            persona=persona,
            conversation_history=history
        )
        
        # Step 3: Text to Speech
        audio_url = speech_service.text_to_speech(
            text=ai_response,
            language="hi"  # Can be dynamic based on detection
        )
        
        # Step 4: Save to database
        user_message = ChatMessage(
            user_id=user_id,
            role="user",
            content=transcribed_text,
            persona=persona,
            input_type="voice"
        )
        db.add(user_message)
        
        assistant_message = ChatMessage(
            user_id=user_id,
            role="assistant",
            content=ai_response,
            audio_url=audio_url,
            persona=persona,
            processing_time=time.time() - start_time
        )
        db.add(assistant_message)
        db.commit()
        
        return {
            "message_id": assistant_message.id,
            "content": ai_response,
            "audio_url": audio_url,
            "timestamp": assistant_message.timestamp,
            "processing_time": time.time() - start_time
        }
        
    finally:
        # Cleanup temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)
```

### 8.4 Error Handling & Edge Cases

**Audio Quality Issues**:
- Background noise: Whisper handles reasonably well
- Low volume: Normalize audio before sending to Whisper
- Multiple speakers: Warn user to speak alone

**Network Issues**:
- Upload timeout: Implement retry logic with exponential backoff
- Partial upload: Use chunked upload for large files
- Connection loss: Queue message for retry when online

**API Failures**:
- Whisper API down: Fallback to text input prompt
- OpenAI API rate limit: Queue request and notify user
- gTTS failure: Return text-only response

**Performance Optimization**:
- Compress audio on frontend before upload (reduce file size)
- Use WebM format (better compression than MP3)
- Implement audio streaming for real-time processing
- Cache common responses to reduce API calls


## 9. Security Considerations

### 9.1 Input Validation

#### API Request Validation
```python
# schemas.py - Pydantic models enforce validation
from pydantic import BaseModel, Field, validator
from typing import Optional

class ChatRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=100)
    message: str = Field(..., min_length=1, max_length=5000)
    persona: str = Field(..., regex="^(farmer|student|jobseeker|senior|business)$")
    
    @validator('message')
    def sanitize_message(cls, v):
        # Remove potentially harmful characters
        return v.strip()

class EligibilityRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=100)
    age: Optional[int] = Field(None, ge=0, le=150)
    income: Optional[float] = Field(None, ge=0, le=100000000)
    
    @validator('income')
    def validate_income(cls, v):
        if v is not None and v < 0:
            raise ValueError('Income cannot be negative')
        return v
```

#### File Upload Validation
```python
from fastapi import UploadFile, HTTPException

ALLOWED_AUDIO_TYPES = ["audio/webm", "audio/mp3", "audio/wav", "audio/mpeg"]
ALLOWED_DOCUMENT_TYPES = ["application/pdf", "image/jpeg", "image/png"]
MAX_AUDIO_SIZE = 25 * 1024 * 1024  # 25MB (Whisper limit)
MAX_DOCUMENT_SIZE = 10 * 1024 * 1024  # 10MB

async def validate_audio_upload(file: UploadFile):
    # Check content type
    if file.content_type not in ALLOWED_AUDIO_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {ALLOWED_AUDIO_TYPES}"
        )
    
    # Check file size
    content = await file.read()
    if len(content) > MAX_AUDIO_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {MAX_AUDIO_SIZE / 1024 / 1024}MB"
        )
    
    # Reset file pointer
    await file.seek(0)
    
    return file

async def validate_document_upload(file: UploadFile):
    if file.content_type not in ALLOWED_DOCUMENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {ALLOWED_DOCUMENT_TYPES}"
        )
    
    content = await file.read()
    if len(content) > MAX_DOCUMENT_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {MAX_DOCUMENT_SIZE / 1024 / 1024}MB"
        )
    
    await file.seek(0)
    return file
```

#### SQL Injection Prevention
```python
# Using SQLAlchemy ORM prevents SQL injection
# Always use parameterized queries

# GOOD - Using ORM
schemes = db.query(Scheme).filter(Scheme.name.like(f"%{search_term}%")).all()

# GOOD - Using parameters
db.execute(
    "SELECT * FROM schemes WHERE name LIKE :search",
    {"search": f"%{search_term}%"}
)

# BAD - Never do this
# db.execute(f"SELECT * FROM schemes WHERE name LIKE '%{search_term}%'")
```

### 9.2 API Key Protection

#### Environment Variables
```python
# .env file (never commit to git)
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
DATABASE_URL=postgresql://user:pass@host:5432/db
SECRET_KEY=your-secret-key-here
ALLOWED_ORIGINS=https://janaccess.vercel.app,http://localhost:5173

# Load in application
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set")
```

#### .env.example Template
```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Database Configuration
DATABASE_URL=sqlite:///./janaccess_ai.db
# For production: postgresql://user:password@host:5432/database

# Application Configuration
SECRET_KEY=your-secret-key-for-jwt
ALLOWED_ORIGINS=http://localhost:5173,https://yourdomain.com

# File Storage
MAX_AUDIO_SIZE_MB=25
MAX_DOCUMENT_SIZE_MB=10
AUDIO_CLEANUP_HOURS=24

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000
```

#### Secrets Management in Deployment
```bash
# Render.com - Set environment variables in dashboard
# Vercel - Set in project settings

# For local development
cp .env.example .env
# Edit .env with actual values
```

### 9.3 CORS Configuration

```python
# main.py
from fastapi.middleware.cors import CORSMiddleware

# Development origins
DEV_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173"
]

# Production origins
PROD_ORIGINS = [
    "https://janaccess.vercel.app",
    "https://janaccess-ai.vercel.app"
]

# Get allowed origins from environment
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",")
if not ALLOWED_ORIGINS or ALLOWED_ORIGINS == [""]:
    ALLOWED_ORIGINS = DEV_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    max_age=3600  # Cache preflight requests for 1 hour
)
```

### 9.4 Rate Limiting

```python
from fastapi import Request, HTTPException
from collections import defaultdict
from datetime import datetime, timedelta
import asyncio

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests = defaultdict(list)
    
    async def check_rate_limit(self, user_id: str):
        now = datetime.utcnow()
        minute_ago = now - timedelta(minutes=1)
        
        # Clean old requests
        self.requests[user_id] = [
            req_time for req_time in self.requests[user_id]
            if req_time > minute_ago
        ]
        
        # Check limit
        if len(self.requests[user_id]) >= self.requests_per_minute:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again later."
            )
        
        # Add current request
        self.requests[user_id].append(now)

# Global rate limiter
rate_limiter = RateLimiter(requests_per_minute=60)

# Use in endpoints
@router.post("/chat/message")
async def send_message(request: ChatRequest):
    await rate_limiter.check_rate_limit(request.user_id)
    # Process request...
```

### 9.5 Data Privacy & Compliance

#### Personal Data Handling
```python
# models.py - Sensitive data handling
from sqlalchemy import Column, String, LargeBinary
from cryptography.fernet import Fernet
import os

# Encryption key (store in environment)
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY").encode()
cipher = Fernet(ENCRYPTION_KEY)

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)
    
    # Encrypt sensitive fields
    _phone = Column("phone", LargeBinary, nullable=True)
    
    @property
    def phone(self):
        if self._phone:
            return cipher.decrypt(self._phone).decode()
        return None
    
    @phone.setter
    def phone(self, value):
        if value:
            self._phone = cipher.encrypt(value.encode())
        else:
            self._phone = None
```

#### Data Retention Policy
```python
# Automatic cleanup of old data
from datetime import datetime, timedelta

async def cleanup_old_data():
    """Run daily to clean up expired data"""
    db = SessionLocal()
    
    try:
        # Delete audio files older than 24 hours
        cutoff_time = datetime.utcnow() - timedelta(hours=24)
        old_messages = db.query(ChatMessage)\
            .filter(ChatMessage.timestamp < cutoff_time)\
            .filter(ChatMessage.audio_url.isnot(None))\
            .all()
        
        for message in old_messages:
            # Delete audio file
            audio_path = message.audio_url.replace("/static/", "static/")
            if os.path.exists(audio_path):
                os.remove(audio_path)
            
            # Clear audio URL from database
            message.audio_url = None
        
        # Delete expired documents
        expired_docs = db.query(Document)\
            .filter(Document.expires_at < datetime.utcnow())\
            .all()
        
        for doc in expired_docs:
            # Delete file
            if os.path.exists(doc.file_path):
                os.remove(doc.file_path)
            
            # Delete database record
            db.delete(doc)
        
        db.commit()
        
    finally:
        db.close()

# Schedule with APScheduler or run as cron job
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()
scheduler.add_job(cleanup_old_data, 'cron', hour=2)  # Run at 2 AM daily
scheduler.start()
```

#### GDPR Compliance Features
```python
@router.delete("/user/{user_id}/data")
async def delete_user_data(user_id: str, db: Session = Depends(get_db)):
    """Allow users to delete their data (Right to be Forgotten)"""
    
    # Delete chat messages
    db.query(ChatMessage).filter(ChatMessage.user_id == user_id).delete()
    
    # Delete eligibility checks
    db.query(EligibilityCheck).filter(EligibilityCheck.user_id == user_id).delete()
    
    # Delete documents
    docs = db.query(Document).filter(Document.user_id == user_id).all()
    for doc in docs:
        if os.path.exists(doc.file_path):
            os.remove(doc.file_path)
    db.query(Document).filter(Document.user_id == user_id).delete()
    
    # Delete user
    db.query(User).filter(User.id == user_id).delete()
    
    db.commit()
    
    return {"message": "User data deleted successfully"}

@router.get("/user/{user_id}/export")
async def export_user_data(user_id: str, db: Session = Depends(get_db)):
    """Export user data (Right to Data Portability)"""
    
    user = db.query(User).get(user_id)
    messages = db.query(ChatMessage).filter(ChatMessage.user_id == user_id).all()
    checks = db.query(EligibilityCheck).filter(EligibilityCheck.user_id == user_id).all()
    
    export_data = {
        "user": {
            "id": user.id,
            "persona": user.persona,
            "created_at": user.created_at.isoformat()
        },
        "messages": [
            {
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat()
            }
            for msg in messages
        ],
        "eligibility_checks": [
            {
                "scheme_name": check.scheme.name,
                "eligible": check.is_eligible,
                "timestamp": check.timestamp.isoformat()
            }
            for check in checks
        ]
    }
    
    return export_data
```

### 9.6 Content Security

#### XSS Prevention
```javascript
// Frontend - Sanitize user input before rendering
import DOMPurify from 'dompurify';

function ChatMessage({ content }) {
  // Sanitize HTML content
  const sanitizedContent = DOMPurify.sanitize(content);
  
  return (
    <div dangerouslySetInnerHTML={{ __html: sanitizedContent }} />
  );
}
```

#### HTTPS Enforcement
```python
# main.py - Redirect HTTP to HTTPS in production
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

if os.getenv("ENVIRONMENT") == "production":
    app.add_middleware(HTTPSRedirectMiddleware)
```


## 10. Deployment Architecture

### 10.1 Frontend Deployment (Vercel)

#### Project Structure for Vercel
```
frontend/
├── package.json
├── vite.config.js
├── vercel.json          # Vercel configuration
├── .env.production      # Production environment variables
└── src/
```

#### vercel.json Configuration
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-XSS-Protection",
          "value": "1; mode=block"
        }
      ]
    }
  ],
  "env": {
    "VITE_API_BASE_URL": "@api_base_url"
  }
}
```

#### Environment Variables (Vercel Dashboard)
```bash
# Production
VITE_API_BASE_URL=https://janaccess-api.onrender.com

# Preview/Development
VITE_API_BASE_URL=https://janaccess-api-dev.onrender.com
```

#### Deployment Steps
```bash
# 1. Install Vercel CLI
npm install -g vercel

# 2. Login to Vercel
vercel login

# 3. Link project
cd frontend
vercel link

# 4. Deploy to production
vercel --prod

# Or use GitHub integration for automatic deployments
```

#### Build Optimization
```javascript
// vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom'],
          'framer-motion': ['framer-motion']
        }
      }
    },
    chunkSizeWarningLimit: 1000
  }
})
```

### 10.2 Backend Deployment (Render)

#### Project Structure for Render
```
backend/
├── main.py
├── requirements.txt
├── render.yaml          # Render configuration
├── Procfile            # Process definition
└── runtime.txt         # Python version
```

#### render.yaml Configuration
```yaml
services:
  - type: web
    name: janaccess-api
    env: python
    region: singapore
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: OPENAI_API_KEY
        sync: false
      - key: DATABASE_URL
        sync: false
      - key: ALLOWED_ORIGINS
        value: https://janaccess.vercel.app
    autoDeploy: true
```

#### requirements.txt
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
python-multipart==0.0.6
openai==1.3.5
gtts==2.4.0
python-dotenv==1.0.0
psycopg2-binary==2.9.9
alembic==1.12.1
```

#### Procfile
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT --workers 2
```

#### runtime.txt
```
python-3.11.0
```

#### Environment Variables (Render Dashboard)
```bash
# API Keys
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx

# Database
DATABASE_URL=postgresql://user:pass@host:5432/janaccess_db

# Application
SECRET_KEY=your-secret-key-here
ALLOWED_ORIGINS=https://janaccess.vercel.app,http://localhost:5173
ENVIRONMENT=production

# File Storage
MAX_AUDIO_SIZE_MB=25
MAX_DOCUMENT_SIZE_MB=10
AUDIO_CLEANUP_HOURS=24
```

#### Deployment Steps
```bash
# 1. Create Render account and connect GitHub

# 2. Create new Web Service
# - Select repository
# - Choose Python environment
# - Set build and start commands

# 3. Add environment variables in dashboard

# 4. Deploy
# Automatic deployment on git push to main branch
```

### 10.3 Database Setup

#### SQLite (Development/Demo)
```python
# database.py
DATABASE_URL = "sqlite:///./janaccess_ai.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
```

#### PostgreSQL (Production)
```python
# database.py
import os

DATABASE_URL = os.getenv("DATABASE_URL")

# Render provides postgres:// but SQLAlchemy needs postgresql://
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
```

#### Database Migration with Alembic
```bash
# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial schema"

# Apply migration
alembic upgrade head
```

#### Render PostgreSQL Setup
```bash
# 1. Create PostgreSQL database in Render dashboard
# 2. Copy connection string
# 3. Add to environment variables as DATABASE_URL
# 4. Run migrations on first deploy
```

### 10.4 Static File Storage

#### Local Storage (Demo)
```python
# main.py
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static"), name="static")

# Directory structure
static/
├── audio/          # Generated TTS files
├── documents/      # Processed documents
└── uploads/        # User uploads
```

#### Cloud Storage (Production - Future)
```python
# For production scaling, use cloud storage
# AWS S3, Google Cloud Storage, or Cloudinary

import boto3
from botocore.exceptions import ClientError

class S3Storage:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('AWS_SECRET_KEY')
        )
        self.bucket_name = os.getenv('S3_BUCKET_NAME')
    
    def upload_file(self, file_path: str, object_name: str):
        try:
            self.s3_client.upload_file(file_path, self.bucket_name, object_name)
            return f"https://{self.bucket_name}.s3.amazonaws.com/{object_name}"
        except ClientError as e:
            print(f"Error uploading to S3: {e}")
            return None
```

### 10.5 CI/CD Pipeline

#### GitHub Actions Workflow
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      
      - name: Run tests
        run: |
          cd backend
          pytest tests/
  
  deploy-frontend:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
  
  deploy-backend:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Trigger Render Deploy
        run: |
          curl -X POST ${{ secrets.RENDER_DEPLOY_HOOK }}
```

### 10.6 Monitoring & Logging

#### Application Logging
```python
# main.py
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler('app.log', maxBytes=10485760, backupCount=5),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Log requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Status: {response.status_code}")
    return response
```

#### Error Tracking (Sentry)
```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

if os.getenv("ENVIRONMENT") == "production":
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        integrations=[FastApiIntegration()],
        traces_sample_rate=0.1
    )
```

#### Health Check Endpoint
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }
```


## 11. Scalability Strategy

### 11.1 Database Migration: SQLite to PostgreSQL

#### Migration Planning
```python
# Step 1: Update database.py to support both
import os
from sqlalchemy import create_engine

def get_database_url():
    """Get database URL based on environment"""
    db_url = os.getenv("DATABASE_URL")
    
    if not db_url:
        # Default to SQLite for development
        return "sqlite:///./janaccess_ai.db"
    
    # Fix Render's postgres:// to postgresql://
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    
    return db_url

DATABASE_URL = get_database_url()

# SQLite needs check_same_thread=False
connect_args = {}
if "sqlite" in DATABASE_URL:
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
```

#### Data Migration Script
```python
# migrate_to_postgres.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models

# Source (SQLite)
sqlite_engine = create_engine("sqlite:///./janaccess_ai.db")
SQLiteSession = sessionmaker(bind=sqlite_engine)

# Target (PostgreSQL)
postgres_url = os.getenv("POSTGRES_URL")
postgres_engine = create_engine(postgres_url)
PostgresSession = sessionmaker(bind=postgres_engine)

def migrate_data():
    """Migrate data from SQLite to PostgreSQL"""
    
    # Create tables in PostgreSQL
    models.Base.metadata.create_all(bind=postgres_engine)
    
    sqlite_session = SQLiteSession()
    postgres_session = PostgresSession()
    
    try:
        # Migrate users
        users = sqlite_session.query(models.User).all()
        for user in users:
            postgres_session.merge(user)
        
        # Migrate schemes
        schemes = sqlite_session.query(models.Scheme).all()
        for scheme in schemes:
            postgres_session.merge(scheme)
        
        # Migrate chat messages
        messages = sqlite_session.query(models.ChatMessage).all()
        for message in messages:
            postgres_session.merge(message)
        
        postgres_session.commit()
        print("Migration completed successfully!")
        
    except Exception as e:
        postgres_session.rollback()
        print(f"Migration failed: {e}")
    
    finally:
        sqlite_session.close()
        postgres_session.close()

if __name__ == "__main__":
    migrate_data()
```

### 11.2 Caching Strategy

#### Redis Integration
```python
# cache.py
import redis
import json
import os
from typing import Optional

class CacheService:
    def __init__(self):
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.redis_client = redis.from_url(redis_url, decode_responses=True)
    
    def get(self, key: str) -> Optional[dict]:
        """Get cached value"""
        value = self.redis_client.get(key)
        if value:
            return json.loads(value)
        return None
    
    def set(self, key: str, value: dict, ttl: int = 3600):
        """Set cached value with TTL (default 1 hour)"""
        self.redis_client.setex(
            key,
            ttl,
            json.dumps(value)
        )
    
    def delete(self, key: str):
        """Delete cached value"""
        self.redis_client.delete(key)
    
    def clear_pattern(self, pattern: str):
        """Clear all keys matching pattern"""
        keys = self.redis_client.keys(pattern)
        if keys:
            self.redis_client.delete(*keys)

# Global cache instance
cache = CacheService()
```

#### Caching Implementation
```python
# routers/scheme.py
from cache import cache

@router.get("/schemes/search")
async def search_schemes(
    q: str,
    persona: Optional[str] = None,
    db: Session = Depends(get_db)
):
    # Generate cache key
    cache_key = f"schemes:search:{q}:{persona}"
    
    # Check cache
    cached_result = cache.get(cache_key)
    if cached_result:
        logger.info(f"Cache hit for {cache_key}")
        return cached_result
    
    # Query database
    query = db.query(Scheme)
    
    if q:
        query = query.filter(Scheme.name.ilike(f"%{q}%"))
    
    if persona:
        query = query.filter(Scheme.target_personas.contains([persona]))
    
    schemes = query.limit(10).all()
    
    result = {
        "schemes": [scheme_to_dict(s) for s in schemes],
        "total": query.count()
    }
    
    # Cache result for 1 hour
    cache.set(cache_key, result, ttl=3600)
    
    return result
```

#### Cache Invalidation
```python
@router.post("/schemes")
async def create_scheme(scheme: SchemeCreate, db: Session = Depends(get_db)):
    """Create new scheme and invalidate cache"""
    
    new_scheme = Scheme(**scheme.dict())
    db.add(new_scheme)
    db.commit()
    
    # Invalidate all scheme search caches
    cache.clear_pattern("schemes:search:*")
    
    return new_scheme
```

### 11.3 Async FastAPI Optimization

#### Async Database Operations
```python
# database.py - Async SQLAlchemy
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Async engine
async_engine = create_async_engine(
    DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
    echo=False
)

# Async session factory
AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Async dependency
async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session
```

#### Async Route Handlers
```python
# routers/chat.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

@router.post("/message")
async def send_message(
    request: ChatRequest,
    db: AsyncSession = Depends(get_async_db)
):
    # Async database query
    result = await db.execute(
        select(User).where(User.id == request.user_id)
    )
    user = result.scalar_one_or_none()
    
    # Async AI service call
    response = await ai_service.generate_response_async(
        user_message=request.message,
        persona=request.persona
    )
    
    # Async database insert
    message = ChatMessage(
        user_id=request.user_id,
        role="assistant",
        content=response
    )
    db.add(message)
    await db.commit()
    
    return {"content": response}
```

#### Concurrent API Calls
```python
import asyncio
from typing import List

async def process_multiple_schemes(user_data: dict, scheme_ids: List[int]):
    """Check eligibility for multiple schemes concurrently"""
    
    async def check_single_scheme(scheme_id: int):
        # Async eligibility check
        return await eligibility_engine.check_eligibility_async(
            user_data, scheme_id
        )
    
    # Run all checks concurrently
    results = await asyncio.gather(
        *[check_single_scheme(sid) for sid in scheme_ids]
    )
    
    return results
```

### 11.4 Load Balancing & Horizontal Scaling

#### Multiple Worker Processes
```bash
# Procfile - Multiple Uvicorn workers
web: uvicorn main:app --host 0.0.0.0 --port $PORT --workers 4
```

#### Gunicorn with Uvicorn Workers
```bash
# For better production performance
pip install gunicorn

# Procfile
web: gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

#### Worker Configuration
```python
# Calculate optimal workers
import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
keepalive = 5
```

### 11.5 API Response Optimization

#### Response Compression
```python
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

#### Pagination
```python
from typing import Optional

@router.get("/schemes")
async def list_schemes(
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db)
):
    # Validate pagination
    page = max(1, page)
    page_size = min(100, max(1, page_size))
    
    # Calculate offset
    offset = (page - 1) * page_size
    
    # Query with pagination
    query = db.query(Scheme)
    total = query.count()
    schemes = query.offset(offset).limit(page_size).all()
    
    return {
        "schemes": [scheme_to_dict(s) for s in schemes],
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": (total + page_size - 1) // page_size
        }
    }
```

#### Field Selection
```python
@router.get("/schemes/{scheme_id}")
async def get_scheme(
    scheme_id: int,
    fields: Optional[str] = None,  # Comma-separated field names
    db: Session = Depends(get_db)
):
    scheme = db.query(Scheme).get(scheme_id)
    
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")
    
    # Return only requested fields
    if fields:
        field_list = fields.split(",")
        return {
            field: getattr(scheme, field)
            for field in field_list
            if hasattr(scheme, field)
        }
    
    return scheme_to_dict(scheme)
```

### 11.6 Background Task Processing

#### Celery Integration
```python
# celery_app.py
from celery import Celery
import os

celery_app = Celery(
    "janaccess",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379/0")
)

@celery_app.task
def cleanup_old_audio_files():
    """Background task to clean up old audio files"""
    from datetime import datetime, timedelta
    import os
    
    cutoff_time = datetime.utcnow() - timedelta(hours=24)
    audio_dir = "static/audio"
    
    for filename in os.listdir(audio_dir):
        file_path = os.path.join(audio_dir, filename)
        file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        
        if file_time < cutoff_time:
            os.remove(file_path)
            print(f"Deleted old audio file: {filename}")

@celery_app.task
def send_analytics_report():
    """Generate and send daily analytics report"""
    # Implementation
    pass
```

#### FastAPI Background Tasks
```python
from fastapi import BackgroundTasks

@router.post("/document/upload")
async def upload_document(
    file: UploadFile,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # Save file immediately
    file_path = save_uploaded_file(file)
    
    # Process document in background
    background_tasks.add_task(
        process_document_async,
        file_path,
        db
    )
    
    return {"message": "Document uploaded, processing in background"}

async def process_document_async(file_path: str, db: Session):
    """Process document asynchronously"""
    # Extract text
    text = extract_text_from_pdf(file_path)
    
    # Generate summary with AI
    summary = await ai_service.summarize_document(text)
    
    # Update database
    # ...
```

### 11.7 Performance Monitoring

#### Prometheus Metrics
```python
from prometheus_client import Counter, Histogram, generate_latest
from fastapi import Response

# Define metrics
request_count = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    
    request_count.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    
    request_duration.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)
    
    return response

@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type="text/plain")
```

---

## 12. Testing Strategy

### 12.1 Unit Tests
```python
# tests/test_eligibility_engine.py
import pytest
from services.eligibility_engine import EligibilityEngine

def test_age_eligibility():
    engine = EligibilityEngine(db_session=mock_db)
    
    user_data = {"age": 25, "persona": "student"}
    scheme = create_mock_scheme(age_min=18, age_max=30)
    
    is_eligible, reasoning = engine._evaluate_scheme(user_data, scheme)
    
    assert is_eligible == True
    assert "age_ok" in reasoning
```

### 12.2 Integration Tests
```python
# tests/test_api.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_chat_endpoint():
    response = client.post("/api/chat/message", json={
        "user_id": "test-user",
        "message": "What schemes are available?",
        "persona": "farmer"
    })
    
    assert response.status_code == 200
    assert "content" in response.json()
```

---

**Document Version**: 1.0  
**Last Updated**: February 14, 2026  
**Status**: Technical Design Complete  
**Owner**: JanAccess AI Team
