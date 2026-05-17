"""
Multilingual translation support module.
Uses deep-translator (Google Translate wrapper) for query/response translation.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from deep_translator import GoogleTranslator

    TRANSLATION_AVAILABLE = True
    print("[Translator] deep-translator loaded successfully.")
except ImportError:
    TRANSLATION_AVAILABLE = False
    print("[Translator] deep-translator not installed. Multilingual support disabled.")


def _chunk_text(text: str, max_chars: int = 4500) -> list:
    """Split text into chunks that fit within Google Translate's limit."""
    if len(text) <= max_chars:
        return [text]

    chunks = []
    sentences = text.replace(". ", ".\n").split("\n")
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= max_chars:
            current_chunk += (" " + sentence) if current_chunk else sentence
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk)

    return chunks if chunks else [text[:max_chars]]


def translate_to_english(text: str, source_lang: str = None) -> str:
    """Translate text to English for retrieval."""
    if not TRANSLATION_AVAILABLE or not text.strip():
        return text
    if source_lang == "en":
        return text
    try:
        src = source_lang if source_lang and source_lang != "auto" else "auto"
        translator = GoogleTranslator(source=src, target="en")

        chunks = _chunk_text(text)
        translated_chunks = []
        for chunk in chunks:
            result = translator.translate(chunk)
            translated_chunks.append(result if result else chunk)

        return " ".join(translated_chunks)
    except Exception as e:
        print(f"[Translator] Translation to English failed: {e}")
        return text


def translate_from_english(text: str, target_lang: str) -> str:
    """Translate English text back to the target language."""
    if not TRANSLATION_AVAILABLE or not text.strip():
        return text
    if target_lang == "en":
        return text
    try:
        translator = GoogleTranslator(source="en", target=target_lang)

        chunks = _chunk_text(text)
        translated_chunks = []
        for chunk in chunks:
            result = translator.translate(chunk)
            translated_chunks.append(result if result else chunk)

        return " ".join(translated_chunks)
    except Exception as e:
        print(f"[Translator] Translation from English failed: {e}")
        return text
