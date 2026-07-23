# ExamGPT — RAG + PYQ‑Aware Exam Preparation Assistant

Upload your class notes and previous year question papers (PYQs), then chat with an AI grounded only in your documents.  
Every answer includes **source citations** (document + page number) and highlights **exam‑frequency patterns** when a concept matches past questions.

## Quick Start
1. Clone this repo.
2. Install dependencies: `pip install -r requirements.txt`
3. Add your Google API key to `.streamlit/secrets.toml`:
   ```toml
   GOOGLE_API_KEY = "your-key-here"