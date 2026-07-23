from typing import List, Tuple
from langchain_google_genai import ChatGoogleGenerativeAI
from ingestion import get_vectorstore

def retrieve_relevant_chunks(query: str, k: int = 5) -> List:
    """
    Get top‑k chunks from Chroma along with their metadata.
    Returns list of (Document, score).
    """
    vectordb = get_vectorstore()
    docs_with_scores = vectordb.similarity_search_with_score(query, k=k)
    return docs_with_scores

def extract_citation_info(doc) -> str:
    """Build a short citation string from chunk metadata."""
    source = doc.metadata.get("source", "unknown")
    page = doc.metadata.get("page", "?")
    return f"[{source}, p. {page}]"

def build_prompt(query: str, retrieved_chunks: List) -> str:
    """
    Create the final prompt for Gemini, embedding retrieved text and
    demanding source citations.
    """
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
    """
    Full retrieval + generation pipeline.
    Returns (answer_text, retrieved_chunks_list, pyq_mention_string).
    """

    retrieved = retrieve_relevant_chunks(query, k)

    prompt = build_prompt(query, retrieved)

    llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.1)
    response = llm.invoke(prompt)
    answer = response.content

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