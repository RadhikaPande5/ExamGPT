import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

# Constants
CHROMA_PERSIST_DIR = "./chroma_db"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

def get_embeddings():
    """Initialise Gemini embeddings (uses GOOGLE_API_KEY from env or streamlit secrets)."""
    return GoogleGenerativeAIEmbeddings(model="models/embedding-001")

def load_and_chunk_pdf(file_path: str, doc_type: str, metadata_extra: dict = None) -> list[Document]:
    """
    Load PDF, split into page‑aware chunks, attach metadata.
    doc_type: "notes" or "pyq"
    metadata_extra: dict with keys like "year", "question_num" (for PYQs)
    """
    loader = PyPDFLoader(file_path)
    docs = loader.load()   

    source_name = os.path.basename(file_path)
    for doc in docs:
        doc.metadata["source"] = source_name
        doc.metadata["doc_type"] = doc_type
        if metadata_extra:
            doc.metadata.update(metadata_extra)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(docs)
    return chunks

def ingest_pdf(file_path: str, doc_type: str, metadata_extra: dict = None):
    """
    Process a single PDF and add its chunks to Chroma.
    Chroma collection is created/loaded with a fixed name.
    """
    chunks = load_and_chunk_pdf(file_path, doc_type, metadata_extra)
    embeddings = get_embeddings()

    vectordb = Chroma(
        persist_directory=CHROMA_PERSIST_DIR,
        embedding_function=embeddings,
        collection_name="examgpt_collection"
    )
    vectordb.add_documents(chunks)
    vectordb.persist()
    return len(chunks)

def clear_vectorstore():
    """Wipe the entire collection (for a fresh start)."""
    embeddings = get_embeddings()
    vectordb = Chroma(
        persist_directory=CHROMA_PERSIST_DIR,
        embedding_function=embeddings,
        collection_name="examgpt_collection"
    )
    vectordb.delete_collection()
    Chroma(
        persist_directory=CHROMA_PERSIST_DIR,
        embedding_function=embeddings,
        collection_name="examgpt_collection"
    ).persist()

def get_vectorstore():
    """Return the existing Chroma instance (for retrieval)."""
    embeddings = get_embeddings()
    return Chroma(
        persist_directory=CHROMA_PERSIST_DIR,
        embedding_function=embeddings,
        collection_name="examgpt_collection"
    )
