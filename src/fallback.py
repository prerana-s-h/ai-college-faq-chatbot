"""
Fallback handling and intent detection module.
Handles low-confidence responses and logs unanswered questions.
"""

import os
import re
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


# Intent patterns for common query types
INTENT_PATTERNS = {
    "fee_enquiry": [
        r"\bfee[s]?\b", r"\btuition\b", r"\bcost\b", r"\bcharges?\b",
        r"\bpayment\b", r"\binstall?ment\b", r"\bexpense\b", r"\bprice\b",
    ],
    "admission_date": [
        r"\bdeadline\b", r"\blast date\b", r"\bwhen.*admiss\b",
        r"\bapplication.*date\b", r"\bregistration.*date\b", r"\bopen.*admiss\b",
    ],
    "contact": [
        r"\bcontact\b", r"\bphone\b", r"\bcall\b", r"\bemail\b",
        r"\baddress\b", r"\blocation\b", r"\bhelpline\b", r"\boffice\b",
    ],
    "placement": [
        r"\bplacement\b", r"\bjob\b", r"\brecruit\b", r"\bpackage\b",
        r"\bsalary\b", r"\bcompan(y|ies)\b", r"\bhir(e|ing)\b",
    ],
    "hostel": [
        r"\bhostel\b", r"\baccommodation\b", r"\broom\b", r"\bmess\b",
        r"\bboarding\b", r"\bdormitor\b",
    ],
    "scholarship": [
        r"\bscholarship\b", r"\bfinancial aid\b", r"\bfree\s?ship\b",
        r"\bconcession\b", r"\bwaiver\b", r"\bmerit\b",
    ],
    "exam": [
        r"\bexam\b", r"\btest\b", r"\bgrading\b", r"\bmark[s]?\b",
        r"\bresult\b", r"\bsyllabus\b", r"\battendance\b",
    ],
}


def detect_intent(query: str) -> str:
    """Detect the intent/category of a query using keyword patterns."""
    query_lower = query.lower()
    for intent, patterns in INTENT_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, query_lower):
                return intent
    return "general"


def check_similarity_threshold(scores: list, threshold: float = None) -> bool:
    """Check if the best similarity score meets the confidence threshold."""
    threshold = threshold or config.SIMILARITY_THRESHOLD
    if not scores:
        return False
    # FAISS returns L2 distance — lower is better
    # For normalized embeddings, distance < threshold means relevant
    best_score = min(scores) if scores else float("inf")
    return best_score < threshold


def get_fallback_message(intent: str = "general") -> str:
    """Generate a helpful fallback message based on detected intent."""
    base = f"I don't have enough information to answer that accurately."

    intent_hints = {
        "fee_enquiry": "For detailed fee information, please contact the accounts department.",
        "admission_date": "For the latest admission dates, please check the official admissions page.",
        "contact": "You can reach the main office for contact details.",
        "placement": "For placement-related queries, please contact the Training & Placement Cell.",
        "hostel": "For hostel availability and booking, contact the hostel warden's office.",
        "scholarship": "For scholarship details, visit the scholarship cell during office hours.",
        "exam": "For exam schedules and results, check the student portal or contact the exam cell.",
    }

    hint = intent_hints.get(intent, "")
    email_line = f"\n\n📧 You can also email us at **{config.FALLBACK_EMAIL}** for assistance."

    return f"{base} {hint}{email_line}"


def log_unanswered(query: str, intent: str = "general"):
    """Log unanswered questions for future knowledge base expansion."""
    os.makedirs(config.LOG_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] Intent: {intent} | Query: {query}\n"

    with open(config.UNANSWERED_LOG, "a", encoding="utf-8") as f:
        f.write(log_entry)
