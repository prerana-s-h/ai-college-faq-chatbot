"""
Text cleaning and chunking module.
Processes raw text into clean, sized chunks for embedding.
"""

import re
import json
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def clean_text(raw_text: str) -> str:
    """Clean raw text by removing artifacts and normalizing whitespace."""
    # Remove HTML entities
    text = re.sub(r"&[a-zA-Z]+;", " ", raw_text)
    # Remove URLs
    text = re.sub(r"https?://\S+", "", text)
    # Remove email addresses (preserve them as useful info — actually keep emails)
    # Remove excessive whitespace
    text = re.sub(r"\s+", " ", text)
    # Remove special characters but keep punctuation
    text = re.sub(r"[^\w\s.,;:!?()'\"-/₹@]", "", text)
    return text.strip()


def load_faqs_from_json(filepath: str) -> List[Document]:
    """Load FAQ entries from a JSON file into Document objects."""
    documents = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            faqs = json.load(f)

        for faq in faqs:
            # Combine Q&A into a single document for better retrieval
            content = f"Question: {faq['question']}\nAnswer: {faq['answer']}"
            doc = Document(
                page_content=content,
                metadata={
                    "source": "sample_faqs",
                    "category": faq.get("category", "general"),
                    "type": "faq",
                },
            )
            documents.append(doc)

        print(f"[Processor] Loaded {len(documents)} FAQ entries from {filepath}")

    except Exception as e:
        print(f"[Processor] Error loading FAQs: {e}")

    return documents


def load_scraped_content(filepath: str) -> List[Document]:
    """Load scraped web content from JSON into Document objects."""
    documents = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            pages = json.load(f)

        for page in pages:
            if page.get("content"):
                doc = Document(
                    page_content=clean_text(page["content"]),
                    metadata={
                        "source": page.get("url", "unknown"),
                        "title": page.get("title", ""),
                        "type": "web",
                    },
                )
                documents.append(doc)

        print(f"[Processor] Loaded {len(documents)} scraped pages")

    except Exception as e:
        print(f"[Processor] Error loading scraped content: {e}")

    return documents


def chunk_documents(
    documents: List[Document],
    chunk_size: int = 500,
    chunk_overlap: int = 80,
) -> List[Document]:
    """Split documents into smaller chunks for embedding."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", ", ", " ", ""],
    )

    chunks = splitter.split_documents(documents)
    print(f"[Processor] Split {len(documents)} documents into {len(chunks)} chunks")
    return chunks
