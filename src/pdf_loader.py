"""
PDF content extraction module.
Extracts text from PDF files for knowledge base ingestion.
"""

import os
from typing import List
from langchain_core.documents import Document

try:
    from PyPDF2 import PdfReader
except ImportError:
    PdfReader = None


def load_pdfs(directory: str) -> List[Document]:
    """
    Load and extract text from all PDF files in a directory.
    Returns a list of LangChain Document objects with metadata.
    """
    if PdfReader is None:
        print("[PDF Loader] PyPDF2 not installed. Skipping PDF loading.")
        return []

    documents = []

    if not os.path.exists(directory):
        print(f"[PDF Loader] Directory not found: {directory}")
        return documents

    pdf_files = [f for f in os.listdir(directory) if f.lower().endswith(".pdf")]

    if not pdf_files:
        print(f"[PDF Loader] No PDF files found in {directory}")
        return documents

    for filename in pdf_files:
        filepath = os.path.join(directory, filename)
        try:
            reader = PdfReader(filepath)
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text and text.strip():
                    doc = Document(
                        page_content=text.strip(),
                        metadata={
                            "source": filename,
                            "page": i + 1,
                            "type": "pdf",
                        },
                    )
                    documents.append(doc)

            print(f"[PDF Loader] Loaded {len(reader.pages)} pages from {filename}")

        except Exception as e:
            print(f"[PDF Loader] Error reading {filename}: {e}")

    print(f"[PDF Loader] Total documents extracted: {len(documents)}")
    return documents
