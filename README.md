# ExamGPT

A RAG-powered exam prep assistant. Upload your notes and previous year question papers (PYQs), then ask questions. Every answer includes source citations and highlights concepts that appeared in past exams.

## Quick Start

1. Clone the repo & install dependencies:
   ```bash
   git clone https://github.com/RadhikaPande5/ExamGPT
   cd ExamGPT
   pip install -r requirements.txt
   ```

2. Add your Google API key in `.streamlit/secrets.toml`:
   ```toml
   GOOGLE_API_KEY = "your-key"
   ```

3. Run the app:
   ```bash
   streamlit run app.py
   ```

## Core Features

- Cited answers (document + page number)
- PYQ frequency alerts (flags high‑yield topics)
- Fully local embeddings (no API needed for processing)
- Private, offline vector storage (ChromaDB)

## How It Works

PDFs → chunked & embedded (HuggingFace) → stored in ChromaDB → relevant chunks retrieved → Gemini generates an answer with citations → if chunks are from a PYQ, a frequency alert is prepended.

## Tech Stack

Streamlit · LangChain · ChromaDB · HuggingFace `all-MiniLM-L6-v2` · Google Gemini (`gemini-flash-lite-latest`)