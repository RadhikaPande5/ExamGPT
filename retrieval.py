import os
from typing import List, Tuple
from google import genai

from ingestion import get_vectorstore


api_key = os.environ["GOOGLE_API_KEY"]
client = genai.Client(api_key=api_key)


def retrieve_relevant_chunks(query: str, k: int = 5) -> List:
    vectordb = get_vectorstore()
    docs_with_scores = vectordb.similarity_search_with_score(query, k=k)
    return docs_with_scores


def extract_citation_info(doc) -> str:
    source = doc.metadata.get("source", "unknown")
    page = doc.metadata.get("page", "?")
    return f"[{source}, p. {page}]"


def build_prompt(query: str, retrieved_chunks: List) -> str:
    context_parts = []
    for i, (doc, score) in enumerate(retrieved_chunks):
        cite = extract_citation_info(doc)
        context_parts.append(f"--- Context chunk {i+1} {cite} ---\n{doc.page_content}")

    context_text = "\n\n".join(context_parts)

    prompt = f"""You are an exam preparation assistant. Answer the student's question **only** using the provided context.
If the context does not contain the answer, say "I cannot answer that from the provided materials."

When you use information from a chunk, cite it in the answer like this: {cite} (e.g., "According to the notes, photosynthesis... [notes.pdf, p. 3]").

Context:
{context_text}

Student question: {query}
Answer:"""
    return prompt


def ask_gemini(query: str, k: int = 5) -> Tuple[str, List, str]:

    retrieved = retrieve_relevant_chunks(query, k)

    prompt = build_prompt(query, retrieved)

    response = client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=prompt,
    )
    answer = response.text

    pyq_info = []
    seen = set()
    for doc, _ in retrieved:
        if doc.metadata.get("doc_type") == "pyq":
            year = doc.metadata.get("year", "????")
            q_num = doc.metadata.get("question_num", "?")
            ident = f"Q{q_num} ({year})"
            if ident not in seen:
                pyq_info.append(ident)
                seen.add(ident)

    if pyq_info:
        if len(pyq_info) >= 2:
            pyq_mention = "📌 This concept appeared in: " + ", ".join(pyq_info) + " — **high‑frequency topic**."
        else:
            pyq_mention = "📌 This concept appeared in: " + ", ".join(pyq_info) + "."
    else:
        pyq_mention = ""

    return answer, retrieved, pyq_mention