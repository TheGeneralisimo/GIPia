# ingest.py
"""Production-ready ingestion script"""
import os
from pathlib import Path

import dotenv
from langchain.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

dotenv.load_dotenv()

DATA_DIR = Path("data")
VECTOR_DIR = Path("vectorstore")

def load_documents():
    docs = []
    if not DATA_DIR.exists():
        return docs
    for file in DATA_DIR.rglob("*"):
        if file.suffix.lower() == ".txt":
            docs.extend(TextLoader(str(file)).load())
        elif file.suffix.lower() == ".pdf":
            docs.extend(PyPDFLoader(str(file)).load())
    return docs

def build_vectorstore(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_documents(docs)
    embeddings = OpenAIEmbeddings()
    store = FAISS.from_documents(chunks, embeddings)
    VECTOR_DIR.mkdir(parents=True, exist_ok=True)
    store.save_local(str(VECTOR_DIR))

def main():
    docs = load_documents()
    if not docs:
        print("No documents found.")
        return
    build_vectorstore(docs)
    print("Vectorstore updated successfully.")

if __name__ == "__main__":
    main()
