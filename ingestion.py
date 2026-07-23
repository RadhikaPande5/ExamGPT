import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

CHROMA_PERSIST_DIR = "./chroma_db"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

def get_embeddings():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def load_and_chunk_pdf(file_path: str, doc_type: str, metadata_extra: dict = None):
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
    return text_splitter.split_documents(docs)

def ingest_pdf(file_path: str, doc_type: str, metadata_extra: dict = None):
    chunks = load_and_chunk_pdf(file_path, doc_type, metadata_extra)
    embeddings = get_embeddings()

    vectordb = Chroma(
        persist_directory=CHROMA_PERSIST_DIR,
        embedding_function=embeddings,
        collection_name="examgpt_collection"
    )
    vectordb.add_documents(chunks)
    if hasattr(vectordb, "persist"):
        vectordb.persist()
    return len(chunks)

def clear_vectorstore():
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
    embeddings = get_embeddings()
    return Chroma(
        persist_directory=CHROMA_PERSIST_DIR,
        embedding_function=embeddings,
        collection_name="examgpt_collection"
    )