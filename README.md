# 🎓 College FAQ Chatbot — GenAI-Powered Admissions Assistant

An AI-powered FAQ chatbot built with **Groq (Llama 3.3)**, **LangChain**, **FAISS**, and **Streamlit** to answer student questions about college admissions, courses, fees, hostel, scholarships, placements, and campus life.

## ✨ Features

- **Conversational RAG** — Retrieval-Augmented Generation with conversation memory (last 5 turns)
- **Multiple Data Sources** — Supports FAQ JSON, PDF documents, and web-scraped content
- **Multilingual Support** — Hindi, Tamil, Telugu, Kannada, Bengali, Marathi
- **Smart Fallback** — Intent detection, confidence thresholds, unanswered question logging
- **Premium UI** — Dark academic glassmorphic Streamlit interface
- **Quick Topics** — One-click buttons for common query categories

## 🏗️ Architecture

```
Student Question → Language Detection → Translation (if needed)
    → FAISS Similarity Search → Context Retrieval
    → Groq LLM (Llama 3.3) + Conversation Memory
    → Response Generation → Translation Back → Display
```

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| LLM | Groq API (Llama 3.3 70B) |
| Embeddings | all-MiniLM-L6-v2 (sentence-transformers) |
| Vector DB | FAISS (CPU) |
| Framework | LangChain |
| UI | Streamlit |
| Web Scraping | BeautifulSoup4 |
| PDF Parsing | PyPDF2 |
| Translation | googletrans |

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd /path/to/project
pip install -r requirements.txt
```

### 2. Configure API Key
Edit the `.env` file and add your Groq API key:
```
GROQ_API_KEY=your_actual_groq_api_key
```

Get a free key at [console.groq.com](https://console.groq.com/)

### 3. Run the App
```bash
streamlit run app.py
```

The app will automatically build the FAISS index from sample FAQs on first run.

## 📁 Adding Custom Data

### PDF Documents
Place PDF files in the `data/pdfs/` directory and click **🔄 Rebuild** in the sidebar.

### Web Scraping
```python
from src.scraper import CollegeWebScraper

scraper = CollegeWebScraper()
scraper.scrape_site(["https://college-website.edu/admissions", ...])
scraper.save_scraped("data/scraped/")
```
Then click **🔄 Rebuild** in the app.

### Custom FAQs
Edit `data/sample_faqs.json` to add your own Q&A pairs.

## 📂 Project Structure

```
├── app.py              # Streamlit chat interface
├── config.py           # Centralized configuration
├── .env                # API keys (not committed)
├── requirements.txt    # Python dependencies
├── data/
│   ├── sample_faqs.json   # Sample FAQ dataset
│   ├── pdfs/              # PDF documents
│   └── scraped/           # Cached web content
├── src/
│   ├── scraper.py      # Web scraping
│   ├── pdf_loader.py   # PDF extraction
│   ├── processor.py    # Text cleaning & chunking
│   ├── indexer.py       # FAISS index management
│   ├── rag_chain.py    # Conversational RAG chain
│   ├── translator.py   # Multilingual support
│   └── fallback.py     # Fallback & intent detection
├── faiss_index/        # Persisted vector index
└── logs/               # Unanswered question logs
```
