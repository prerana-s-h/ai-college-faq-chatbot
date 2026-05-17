"""
Centralized configuration for the College FAQ Chatbot.
Loads environment variables and defines constants.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── Groq API ──────────────────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# ── Embedding Model ──────────────────────────────────────
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# ── RAG Settings ─────────────────────────────────────────
CHUNK_SIZE = 300          # tokens per chunk
CHUNK_OVERLAP = 50        # overlap between chunks
TOP_K = 4                 # number of retrieved documents
MEMORY_WINDOW = 5         # conversation turns to remember
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.35"))

# ── Paths ────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
PDF_DIR = os.path.join(DATA_DIR, "pdfs")
SCRAPED_DIR = os.path.join(DATA_DIR, "scraped")
FAISS_INDEX_DIR = os.path.join(BASE_DIR, "faiss_index")
LOG_DIR = os.path.join(BASE_DIR, "logs")
UNANSWERED_LOG = os.path.join(LOG_DIR, "unanswered.log")
SAMPLE_FAQ_PATH = os.path.join(DATA_DIR, "sample_faqs.json")

# ── Fallback ─────────────────────────────────────────────
FALLBACK_EMAIL = os.getenv("FALLBACK_EMAIL", "admissions@college.edu")

# ── System Prompt ────────────────────────────────────────
SYSTEM_PROMPT = """You are a friendly and helpful college admissions assistant. 
Your role is to answer student questions about admissions, courses, fees, 
hostel facilities, scholarships, placements, exams, and campus life.

Rules:
1. Answer ONLY from the provided context below. Do not make up information.
2. Be concise, friendly, and accurate.
3. If the context doesn't contain the answer, say so politely and suggest contacting the admissions office.
4. Format your answers clearly with bullet points when listing multiple items.
5. Include specific numbers, dates, and details when available in the context.

Context:
{context}

Conversation History:
{chat_history}
"""

# ── Supported Languages ──────────────────────────────────
SUPPORTED_LANGUAGES = {
    "English": "en",
    "हिन्दी (Hindi)": "hi",
    "தமிழ் (Tamil)": "ta",
    "తెలుగు (Telugu)": "te",
    "ಕನ್ನಡ (Kannada)": "kn",
    "বাংলা (Bengali)": "bn",
    "मराठी (Marathi)": "mr",
}

# ── Ensure directories exist ────────────────────────────
for d in [DATA_DIR, PDF_DIR, SCRAPED_DIR, FAISS_INDEX_DIR, LOG_DIR]:
    os.makedirs(d, exist_ok=True)
