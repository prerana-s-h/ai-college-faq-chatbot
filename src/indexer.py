"""
FAISS vector index module.
Handles embedding generation, index creation, and similarity search.
"""

import os
import sys

# Add parent directory to path for config import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Tuple
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

import config
from src.processor import load_faqs_from_json, load_scraped_content, chunk_documents
from src.pdf_loader import load_pdfs


def get_embeddings():
    """Initialize the embedding model."""
    print(f"[Indexer] Loading embedding model: {config.EMBEDDING_MODEL}")
    return HuggingFaceEmbeddings(
        model_name=config.EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def gather_all_documents() -> List[Document]:
    """Collect documents from all sources: FAQs, PDFs, and scraped content."""
    all_docs = []

    # 1. Load sample FAQs
    if os.path.exists(config.SAMPLE_FAQ_PATH):
        faq_docs = load_faqs_from_json(config.SAMPLE_FAQ_PATH)
        all_docs.extend(faq_docs)

    # 2. Load PDFs
    pdf_docs = load_pdfs(config.PDF_DIR)
    all_docs.extend(pdf_docs)

    # 3. Load scraped content
    scraped_file = os.path.join(config.SCRAPED_DIR, "scraped_content.json")
    if os.path.exists(scraped_file):
        web_docs = load_scraped_content(scraped_file)
        all_docs.extend(web_docs)

    print(f"[Indexer] Total documents gathered: {len(all_docs)}")
    return all_docs


def build_index(documents: List[Document] = None) -> FAISS:
    """Build FAISS index from documents."""
    if documents is None:
        documents = gather_all_documents()

    if not documents:
        raise ValueError("No documents found to index. Add FAQs, PDFs, or scrape content first.")

    # Chunk the documents
    chunks = chunk_documents(
        documents,
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
    )

    # Generate embeddings and create index
    embeddings = get_embeddings()
    print(f"[Indexer] Building FAISS index from {len(chunks)} chunks...")
    vector_store = FAISS.from_documents(chunks, embeddings)
    print("[Indexer] FAISS index built successfully!")

    return vector_store


def save_index(vector_store: FAISS, path: str = None):
    """Save FAISS index to disk."""
    path = path or config.FAISS_INDEX_DIR
    os.makedirs(path, exist_ok=True)
    vector_store.save_local(path)
    print(f"[Indexer] Index saved to {path}")


def load_index(path: str = None) -> FAISS:
    """Load FAISS index from disk."""
    path = path or config.FAISS_INDEX_DIR
    embeddings = get_embeddings()
    vector_store = FAISS.load_local(
        path, embeddings, allow_dangerous_deserialization=True
    )
    print(f"[Indexer] Index loaded from {path}")
    return vector_store


def get_or_build_index() -> FAISS:
    """Load existing index or build a new one."""
    index_file = os.path.join(config.FAISS_INDEX_DIR, "index.faiss")

    if os.path.exists(index_file):
        print("[Indexer] Found existing FAISS index, loading...")
        return load_index()
    else:
        print("[Indexer] No existing index found, building new one...")
        vector_store = build_index()
        save_index(vector_store)
        return vector_store
