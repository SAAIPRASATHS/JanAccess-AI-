"""
Smart Persona Mode — Configuration & Mappings.
Centralises all persona-specific data used by both the API and AI service.
"""

# ─── Valid Persona Labels ────────────────────────────────────────
PERSONA_OPTIONS = [
    "Farmer",
    "Student",
    "Job Seeker",
    "Small Business Owner",
    "Senior Citizen",
    "Differently Abled",
]


# ─── Persona → Extra AI System-Prompt Instructions ──────────────
PERSONA_SYSTEM_PROMPTS: dict[str, str] = {
    "Farmer": (
        "Prioritize agriculture-related schemes, crop insurance, subsidies, "
        "mandi (market) prices, PM-KISAN, and MGNREGA. Suggest seasonal "
        "farming tips when relevant."
    ),
    "Student": (
        "Prioritize scholarships, education loans, skill development "
        "programs, entrance exam guidance, and free learning resources."
    ),
    "Job Seeker": (
        "Prioritize government job portals, resume building tips, PMKVY "
        "skill training, placement-linked courses, and employment exchanges."
    ),
    "Small Business Owner": (
        "Prioritize MUDRA loans, MSME registration, GST guidance, Startup "
        "India schemes, and digital payment adoption tips."
    ),
    "Senior Citizen": (
        "Prioritize pension schemes (IGNOAPS, APY), Ayushman Bharat health "
        "coverage, senior citizen savings schemes, and elder-care helplines."
    ),
    "Differently Abled": (
        "Prioritize disability pension, UDID registration, assistive device "
        "schemes, reservation-based opportunities, and accessible government "
        "services."
    ),
}


# ─── Persona → Quick-Action Buttons (label + pre-filled query) ──
PERSONA_QUICK_ACTIONS: dict[str, list[dict[str, str]]] = {
    "Farmer": [
        {"label": "🌾 Crop Subsidy",   "query": "What crop subsidies are available for farmers?"},
        {"label": "📊 Mandi Prices",    "query": "Show me the latest mandi prices for crops."},
        {"label": "🌧️ Crop Insurance",  "query": "How do I apply for crop insurance?"},
        {"label": "💰 PM-KISAN",        "query": "Tell me about PM-KISAN income support scheme."},
    ],
    "Student": [
        {"label": "🎓 Scholarships",    "query": "What scholarships are available for students?"},
        {"label": "📚 Skill Courses",    "query": "Show me free government skill courses."},
        {"label": "🏦 Education Loans",  "query": "How to apply for an education loan?"},
        {"label": "📝 Exam Guidance",    "query": "Guide me on government competitive exams."},
    ],
    "Job Seeker": [
        {"label": "🏛️ Govt Jobs",       "query": "What government jobs are open right now?"},
        {"label": "📄 Resume Help",      "query": "Help me build a strong resume."},
        {"label": "🛠️ Skill Training",   "query": "What free skill training programs are available?"},
        {"label": "💼 Placement",        "query": "How to register on employment exchanges?"},
    ],
    "Small Business Owner": [
        {"label": "🏦 MUDRA Loan",      "query": "How to apply for a MUDRA loan?"},
        {"label": "📋 MSME Register",    "query": "How do I register my business as MSME?"},
        {"label": "💡 Startup India",    "query": "Tell me about Startup India benefits."},
        {"label": "📱 Digital Payments",  "query": "How to adopt digital payments for my shop?"},
    ],
    "Senior Citizen": [
        {"label": "🏥 Health Cover",     "query": "What health insurance is available for senior citizens?"},
        {"label": "💰 Pension Schemes",  "query": "Tell me about pension schemes for seniors."},
        {"label": "🏦 Savings Schemes",  "query": "What savings schemes are best for senior citizens?"},
        {"label": "📞 Elder Helpline",   "query": "What helplines are available for senior citizens?"},
    ],
    "Differently Abled": [
        {"label": "🆔 UDID Card",       "query": "How do I apply for a UDID disability card?"},
        {"label": "💰 Disability Pension", "query": "What disability pension schemes are available?"},
        {"label": "🦽 Assistive Devices", "query": "How to get free assistive devices from the government?"},
        {"label": "💼 Job Reservation",   "query": "What job reservations exist for differently abled persons?"},
    ],
}
