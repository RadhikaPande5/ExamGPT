import streamlit as st
import tempfile
import os
from ingestion import ingest_pdf, clear_vectorstore
from retrieval import ask_gemini, extract_citation_info

st.set_page_config(page_title="ExamGPT", layout="wide")
st.title("📚 ExamGPT — Your Exam Prep Assistant")

if "processed" not in st.session_state:
    st.session_state.processed = False
    st.session_state.chat_history = []

    st.header("📂 Upload Study Materials")

    notes_files = st.file_uploader(
        "Upload **class notes** (PDF)", type="pdf", accept_multiple_files=True,
        key="notes_uploader"
    )
    pyq_files = st.file_uploader(
        "Upload **previous year question papers** (PDF)", type="pdf", accept_multiple_files=True,
        key="pyq_uploader"
    )

    pyq_year = st.text_input("Year of uploaded PYQs (e.g., 2023)", value="")

    process_btn = st.button("Process All Documents", type="primary")

    if process_btn:
        if not notes_files and not pyq_files:
            st.error("Please upload at least one PDF.")
        else:
            with st.spinner("🔨 Chunking, embedding, and storing documents... This may take a moment."):
                clear_vectorstore()

                total_chunks = 0
                for file in notes_files:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                        tmp.write(file.read())
                        tmp_path = tmp.name
                    chunks = ingest_pdf(tmp_path, doc_type="notes")
                    total_chunks += chunks
                    os.unlink(tmp_path)

                if pyq_files:
                    year = pyq_year.strip() if pyq_year.strip() else "unknown"
                    for file in pyq_files:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                            tmp.write(file.read())
                            tmp_path = tmp.name
                        metadata = {"year": year, "question_num": "all"}
                        chunks = ingest_pdf(tmp_path, doc_type="pyq", metadata_extra=metadata)
                        total_chunks += chunks
                        os.unlink(tmp_path)

            st.session_state.processed = True
            st.success(f"✅ Processed {len(notes_files) if notes_files else 0} notes + {len(pyq_files) if pyq_files else 0} PYQ PDFs → {total_chunks} chunks stored.")
            st.session_state.chat_history = []

if st.session_state.processed:
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "sources" in msg and msg["sources"]:
                with st.expander("📖 Sources"):
                    for src in msg["sources"]:
                        st.markdown(f"- {src}")

    query = st.chat_input("Ask a question about your study materials...")
    if query:
        st.session_state.chat_history.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        with st.spinner("🤔 Thinking..."):
            answer, retrieved_chunks, pyq_mention = ask_gemini(query)

        if pyq_mention:
            answer = pyq_mention + "\n\n" + answer

        sources = []
        for doc, _ in retrieved_chunks:
            sources.append(extract_citation_info(doc))

        with st.chat_message("assistant"):
            st.markdown(answer)
            if sources:
                with st.expander("📖 Sources"):
                    for src in sources:
                        st.markdown(f"- {src}")

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer,
            "sources": sources
        })
else:
    st.info("Upload your class notes and PYQ PDFs in the sidebar, then click **Process All Documents** to start chatting.")

st.markdown("---")
st.caption("ExamGPT – Your personal AI tutor built with RAG, Gemini, and Streamlit.")
