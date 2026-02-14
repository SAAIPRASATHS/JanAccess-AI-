# JanAccess AI - Requirements Document

## 1. Project Overview

JanAccess AI is a voice-first civic intelligence platform designed to democratize access to government services, schemes, job opportunities, and skill development programs for underserved communities in India. The platform leverages AI-powered conversational interfaces to break down barriers of literacy, language, and digital complexity, enabling citizens to discover and access public services through natural voice interactions.

### Tech Stack
- **Frontend**: React, Tailwind CSS, Framer Motion
- **Backend**: FastAPI (Python)
- **AI Services**: OpenAI API, Whisper (Speech-to-text), gTTS (Text-to-speech)
- **Database**: SQLite (demo), PostgreSQL (production)
- **Deployment**: Vercel (frontend), Render (backend)

## 2. Problem Statement

Millions of citizens in underserved communities face significant barriers when trying to access government schemes, job opportunities, and public services:

- **Digital Literacy Gap**: Complex government portals and forms are difficult to navigate for users with limited digital literacy
- **Language Barriers**: Most government services are available only in English or limited regional languages
- **Information Overload**: Citizens struggle to identify which schemes they are eligible for among hundreds of options
- **Document Complexity**: Legal and policy documents are written in complex language that is hard to understand
- **Accessibility Issues**: Traditional text-based interfaces exclude users with visual impairments or reading difficulties
- **Connectivity Constraints**: Many rural areas have limited internet bandwidth

JanAccess AI addresses these challenges by providing a voice-first, persona-aware AI assistant that simplifies access to civic services.

## 3. Objectives

### Primary Objectives
1. Enable voice-based interaction for discovering and accessing government schemes and services
2. Provide personalized recommendations based on user personas (Farmer, Student, Job Seeker, Senior Citizen, Small Business Owner)
3. Simplify eligibility checking for government schemes through conversational AI
4. Explain complex government documents in simple, accessible language
5. Connect users with relevant skill development programs and job opportunities

### Secondary Objectives
1. Support low-bandwidth environments for rural accessibility
2. Provide analytics for understanding user needs and service gaps
3. Create a scalable platform that can be extended to additional services and languages
4. Demonstrate social impact potential for hackathon evaluation

## 4. Target Users

### Primary User Personas

#### 4.1 Farmers
- **Needs**: Agricultural subsidies, crop insurance, market prices, weather information, farming techniques
- **Characteristics**: Limited digital literacy, prefer voice interaction, regional language speakers
- **Pain Points**: Complex application processes, lack of awareness about available schemes

#### 4.2 Students
- **Needs**: Scholarships, educational loans, skill development programs, career guidance
- **Characteristics**: Moderate digital literacy, mobile-first users, seeking quick information
- **Pain Points**: Information scattered across multiple portals, eligibility confusion

#### 4.3 Job Seekers
- **Needs**: Job listings, skill training, resume building, interview preparation, employment schemes
- **Characteristics**: Varied digital literacy, urgent need for employment, seeking personalized recommendations
- **Pain Points**: Mismatch between skills and opportunities, lack of guidance

#### 4.4 Senior Citizens
- **Needs**: Pension schemes, healthcare benefits, senior citizen cards, tax benefits
- **Characteristics**: Low digital literacy, prefer simple interfaces, need patient assistance
- **Pain Points**: Complex digital processes, small text, confusing navigation

#### 4.5 Small Business Owners
- **Needs**: Business loans, MSME schemes, tax information, licensing guidance, market access
- **Characteristics**: Time-constrained, need quick actionable information, moderate digital literacy
- **Pain Points**: Bureaucratic complexity, lack of personalized guidance

## 5. Functional Requirements

### 5.1 Voice-First AI Assistant

#### 5.1.1 Speech-to-Text (STT)
- **FR-1.1**: System shall accept voice input from users through microphone
- **FR-1.2**: System shall convert speech to text using Whisper API with accuracy >90%
- **FR-1.3**: System shall support multiple Indian languages (Hindi, English as minimum)
- **FR-1.4**: System shall handle background noise and varying audio quality
- **FR-1.5**: System shall provide visual feedback during voice recording

#### 5.1.2 Text-to-Speech (TTS)
- **FR-1.6**: System shall convert AI responses to natural-sounding speech using gTTS
- **FR-1.7**: System shall support language-specific voice output matching user's input language
- **FR-1.8**: System shall allow users to pause, replay, or skip audio responses
- **FR-1.9**: System shall provide adjustable speech rate for accessibility

#### 5.1.3 Conversational AI
- **FR-1.10**: System shall use OpenAI API to generate contextually relevant responses
- **FR-1.11**: System shall maintain conversation context across multiple turns
- **FR-1.12**: System shall handle clarifying questions and follow-up queries
- **FR-1.13**: System shall provide fallback responses for unrecognized queries
- **FR-1.14**: System shall support both voice and text input modes

### 5.2 Persona-Based Personalization

#### 5.2.1 Persona Selection
- **FR-2.1**: System shall allow users to select their persona (Farmer, Student, Job Seeker, Senior Citizen, Small Business Owner)
- **FR-2.2**: System shall customize AI responses based on selected persona
- **FR-2.3**: System shall allow users to switch personas during a session
- **FR-2.4**: System shall remember user's persona preference across sessions

#### 5.2.2 Personalized Content
- **FR-2.5**: System shall filter scheme recommendations based on persona relevance
- **FR-2.6**: System shall adjust language complexity based on persona (simpler for Senior Citizens)
- **FR-2.7**: System shall prioritize information types relevant to each persona
- **FR-2.8**: System shall provide persona-specific examples and use cases

### 5.3 Government Scheme Search

#### 5.3.1 Scheme Discovery
- **FR-3.1**: System shall maintain a database of government schemes across central and state levels
- **FR-3.2**: System shall allow users to search schemes by keywords, categories, or natural language queries
- **FR-3.3**: System shall display scheme details including benefits, eligibility, application process, and deadlines
- **FR-3.4**: System shall provide direct links to official scheme portals
- **FR-3.5**: System shall categorize schemes by type (financial aid, subsidies, training, healthcare, etc.)

#### 5.3.2 Scheme Recommendations
- **FR-3.6**: System shall recommend top 3-5 relevant schemes based on user persona and query
- **FR-3.7**: System shall explain why each scheme is recommended
- **FR-3.8**: System shall rank schemes by relevance and application deadline urgency
- **FR-3.9**: System shall highlight newly launched schemes

### 5.4 Smart Eligibility Checker

#### 5.4.1 Eligibility Assessment
- **FR-4.1**: System shall collect user information through conversational interface (age, income, location, occupation, etc.)
- **FR-4.2**: System shall evaluate eligibility against scheme criteria automatically
- **FR-4.3**: System shall provide clear yes/no eligibility determination with reasoning
- **FR-4.4**: System shall identify missing information required for eligibility check
- **FR-4.5**: System shall suggest alternative schemes if user is ineligible

#### 5.4.2 Application Guidance
- **FR-4.6**: System shall provide step-by-step application instructions for eligible schemes
- **FR-4.7**: System shall list required documents for application
- **FR-4.8**: System shall provide application deadlines and important dates
- **FR-4.9**: System shall offer to save eligibility results for future reference

### 5.5 Document Explainer

#### 5.5.1 Document Upload
- **FR-5.1**: System shall allow users to upload government documents (PDF, images)
- **FR-5.2**: System shall support document upload up to 10MB in size
- **FR-5.3**: System shall extract text from uploaded documents using OCR if needed
- **FR-5.4**: System shall validate document format and provide error messages for unsupported formats

#### 5.5.2 Document Simplification
- **FR-5.5**: System shall analyze uploaded documents using AI
- **FR-5.6**: System shall provide simplified summaries in plain language
- **FR-5.7**: System shall answer specific questions about document content
- **FR-5.8**: System shall highlight key information (deadlines, requirements, benefits)
- **FR-5.9**: System shall explain legal or technical terms in simple language

### 5.6 Skill & Job Recommendation Engine

#### 5.6.1 Skill Assessment
- **FR-6.1**: System shall collect information about user's current skills through conversation
- **FR-6.2**: System shall identify skill gaps for desired job roles
- **FR-6.3**: System shall recommend relevant skill development programs and courses
- **FR-6.4**: System shall provide information about free/subsidized government training programs

#### 5.6.2 Job Matching
- **FR-6.5**: System shall maintain a database of job opportunities from government and partner sources
- **FR-6.6**: System shall match users with relevant job openings based on skills and location
- **FR-6.7**: System shall provide job details including requirements, salary range, and application process
- **FR-6.8**: System shall suggest career pathways and growth opportunities

### 5.7 Low Bandwidth Mode

#### 5.7.1 Optimized Performance
- **FR-7.1**: System shall detect user's network speed and automatically switch to low bandwidth mode
- **FR-7.2**: System shall provide text-only responses when bandwidth is limited
- **FR-7.3**: System shall compress audio files for faster transmission in low bandwidth mode
- **FR-7.4**: System shall cache frequently accessed content locally
- **FR-7.5**: System shall allow manual toggle between normal and low bandwidth modes

#### 5.7.2 Offline Capabilities
- **FR-7.6**: System shall provide basic scheme information offline using cached data
- **FR-7.7**: System shall queue user queries for processing when connection is restored
- **FR-7.8**: System shall indicate offline status clearly to users

### 5.8 Analytics Dashboard

#### 5.8.1 User Analytics
- **FR-8.1**: System shall track user interactions (queries, schemes viewed, eligibility checks)
- **FR-8.2**: System shall display user demographics by persona type
- **FR-8.3**: System shall show most searched schemes and topics
- **FR-8.4**: System shall track user engagement metrics (session duration, return rate)

#### 5.8.2 Impact Metrics
- **FR-8.5**: System shall display total number of users served
- **FR-8.6**: System shall track successful scheme applications initiated through platform
- **FR-8.7**: System shall identify underserved areas and user needs
- **FR-8.8**: System shall generate reports for stakeholders and hackathon judges

## 6. Non-Functional Requirements

### 6.1 Performance

#### 6.1.1 Response Time
- **NFR-1.1**: Voice-to-text conversion shall complete within 3 seconds for 30-second audio clips
- **NFR-1.2**: AI response generation shall complete within 5 seconds for standard queries
- **NFR-1.3**: Text-to-speech conversion shall complete within 2 seconds for 200-word responses
- **NFR-1.4**: Page load time shall be under 3 seconds on 3G connections
- **NFR-1.5**: API response time shall be under 500ms for 95% of requests

#### 6.1.2 Throughput
- **NFR-1.6**: System shall support at least 100 concurrent users during demo
- **NFR-1.7**: System shall handle 1000 requests per hour without degradation

### 6.2 Scalability

- **NFR-2.1**: System architecture shall support horizontal scaling for increased user load
- **NFR-2.2**: Database shall be designed to scale from SQLite (demo) to PostgreSQL (production)
- **NFR-2.3**: System shall support addition of new personas without code refactoring
- **NFR-2.4**: System shall support addition of new languages through configuration
- **NFR-2.5**: API design shall be modular to allow independent scaling of services

### 6.3 Security

#### 6.3.1 Data Protection
- **NFR-3.1**: User personal information shall be encrypted at rest and in transit
- **NFR-3.2**: System shall comply with data privacy regulations (GDPR, Indian IT Act)
- **NFR-3.3**: Uploaded documents shall be automatically deleted after 24 hours
- **NFR-3.4**: System shall not store sensitive information like Aadhaar numbers permanently

#### 6.3.2 Authentication & Authorization
- **NFR-3.5**: API endpoints shall be protected with authentication tokens
- **NFR-3.6**: Admin dashboard shall require secure login credentials
- **NFR-3.7**: System shall implement rate limiting to prevent abuse (100 requests/hour per user)

### 6.4 Accessibility

- **NFR-4.1**: System shall be usable by users with visual impairments through voice interface
- **NFR-4.2**: UI shall support screen readers and keyboard navigation
- **NFR-4.3**: Text shall have minimum contrast ratio of 4.5:1 for readability
- **NFR-4.4**: UI elements shall be large enough for users with motor impairments (minimum 44x44px touch targets)
- **NFR-4.5**: System shall support adjustable font sizes
- **NFR-4.6**: Error messages shall be clear and provide actionable guidance

### 6.5 Maintainability

- **NFR-5.1**: Code shall follow PEP 8 style guide for Python and ESLint standards for JavaScript
- **NFR-5.2**: System shall have comprehensive API documentation using OpenAPI/Swagger
- **NFR-5.3**: Code shall include inline comments for complex logic
- **NFR-5.4**: System shall have modular architecture with clear separation of concerns
- **NFR-5.5**: Configuration shall be externalized using environment variables
- **NFR-5.6**: System shall include logging for debugging and monitoring

### 6.6 Reliability

- **NFR-6.1**: System shall have 95% uptime during hackathon demo period
- **NFR-6.2**: System shall gracefully handle API failures with fallback mechanisms
- **NFR-6.3**: System shall validate all user inputs to prevent crashes
- **NFR-6.4**: System shall provide meaningful error messages for all failure scenarios

### 6.7 Usability

- **NFR-7.1**: New users shall be able to complete their first query within 2 minutes without training
- **NFR-7.2**: System shall provide onboarding tutorial for first-time users
- **NFR-7.3**: UI shall be intuitive and require minimal text reading
- **NFR-7.4**: System shall provide visual and audio feedback for all user actions
- **NFR-7.5**: System shall support both mobile and desktop interfaces

## 7. System Constraints

### 7.1 Technical Constraints
- **C-1**: System must use OpenAI API which has rate limits and costs per token
- **C-2**: Whisper API has file size limits (25MB) and processing time constraints
- **C-3**: Free tier deployment platforms (Vercel, Render) have resource limitations
- **C-4**: SQLite database has concurrency limitations for demo version
- **C-5**: gTTS has limited voice quality compared to premium TTS services

### 7.2 Time Constraints
- **C-6**: Project must be completed within hackathon timeline (typically 24-48 hours)
- **C-7**: Demo must be functional and stable for judging presentation
- **C-8**: Documentation must be completed alongside development

### 7.3 Resource Constraints
- **C-9**: Limited API credits for OpenAI during development and demo
- **C-10**: Team size and skill distribution may limit parallel development
- **C-11**: Testing must be done with limited real user feedback

### 7.4 Data Constraints
- **C-12**: Government scheme data must be manually curated or scraped from public sources
- **C-13**: Real-time scheme updates may not be available
- **C-14**: Job listings may be limited to publicly available sources

## 8. Assumptions

### 8.1 User Assumptions
- **A-1**: Users have access to a smartphone or computer with microphone
- **A-2**: Users have basic familiarity with voice assistants (Alexa, Google Assistant)
- **A-3**: Users are willing to share basic demographic information for personalization
- **A-4**: Users have at least 2G/3G internet connectivity

### 8.2 Technical Assumptions
- **A-5**: OpenAI API will remain accessible and stable during demo
- **A-6**: Deployment platforms (Vercel, Render) will have sufficient uptime
- **A-7**: Government scheme information is publicly available and can be legally used
- **A-8**: Third-party APIs (Whisper, gTTS) will function as documented

### 8.3 Business Assumptions
- **A-9**: Project demonstrates sufficient social impact for hackathon evaluation
- **A-10**: Solution addresses a real problem faced by target users
- **A-11**: Platform can attract partnerships with government or NGOs post-hackathon
- **A-12**: Users will trust AI-generated information if properly sourced

## 9. Deployment Plan

### 9.1 Development Environment
- Local development using Python virtual environment and Node.js
- SQLite database for rapid prototyping
- Environment variables for API keys and configuration

### 9.2 Staging Environment
- Frontend deployed to Vercel preview branch
- Backend deployed to Render free tier
- SQLite database with seed data for testing

### 9.3 Production Environment (Demo)
- **Frontend**: Deployed to Vercel with custom domain
- **Backend**: Deployed to Render with HTTPS enabled
- **Database**: SQLite for demo, migration path to PostgreSQL documented
- **Static Assets**: Audio files and documents served from backend static folder
- **Environment Variables**: Securely configured on deployment platforms

### 9.4 Deployment Steps
1. Set up Vercel project and connect GitHub repository (frontend)
2. Configure build settings (npm run build)
3. Set up Render web service and connect GitHub repository (backend)
4. Configure environment variables (OpenAI API key, database URL)
5. Deploy backend and verify API endpoints
6. Update frontend API base URL to point to deployed backend
7. Deploy frontend and verify end-to-end functionality
8. Seed database with sample schemes and data
9. Perform smoke testing on deployed environment
10. Monitor logs and performance during demo

### 9.5 Rollback Plan
- Keep previous working deployment active until new version is verified
- Maintain local backup of database
- Document manual rollback steps for both frontend and backend

## 10. Future Enhancements

### 10.1 Short-Term Enhancements (Post-Hackathon)
- **E-1**: Add support for more Indian regional languages (Tamil, Telugu, Bengali, Marathi)
- **E-2**: Integrate real-time government scheme APIs where available
- **E-3**: Implement user authentication and profile management
- **E-4**: Add SMS-based interface for users without smartphones
- **E-5**: Create mobile apps (Android/iOS) for better offline support
- **E-6**: Implement advanced analytics with ML-based insights

### 10.2 Medium-Term Enhancements
- **E-7**: Partner with government departments for official scheme data feeds
- **E-8**: Add video tutorials and visual guides for complex processes
- **E-9**: Implement community forum for users to share experiences
- **E-10**: Add chatbot integration with WhatsApp and Telegram
- **E-11**: Develop offline-first PWA with service workers
- **E-12**: Implement AI-powered application form filling assistance

### 10.3 Long-Term Vision
- **E-13**: Expand to cover all government services (healthcare, education, legal aid)
- **E-14**: Implement blockchain-based verification for application tracking
- **E-15**: Create API marketplace for third-party integrations
- **E-16**: Develop AI model fine-tuned on Indian government schemes and policies
- **E-17**: Scale to other developing countries with similar challenges
- **E-18**: Implement voice biometrics for secure authentication
- **E-19**: Add AR features for document scanning and form filling
- **E-20**: Create impact measurement framework with government partnerships

---

**Document Version**: 1.0  
**Last Updated**: February 14, 2026  
**Status**: Draft for Hackathon Submission  
**Owner**: JanAccess AI Team
