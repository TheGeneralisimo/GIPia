import os
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    UnstructuredWordDocumentLoader
)

load_dotenv()

DATA_DIR = "data/"
DB_DIR = "db/"


def load_documents():
    docs = []

    for root, dirs, files in os.walk(DATA_DIR):
        for f in files:
            path = os.path.join(root, f)

            if f.endswith(".txt"):
                loader = TextLoader(path, encoding="utf-8")
            elif f.endswith(".pdf"):
                loader = PyPDFLoader(path)
            elif f.endswith(".docx"):
                loader = UnstructuredWordDocumentLoader(path)
            else:
                print(f"Archivo no soportado: {f}")
                continue

            docs.extend(loader.load())

    return docs


def ingest():
    # cargar documentos
    documents = load_documents()
    print(f"Documentos cargados: {len(documents)}")

    # dividir chunks con la librería nueva
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)
    print(f"Chunks generados: {len(chunks)}")

    # embeddings HF
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # crear vectorstore
    db = FAISS.from_documents(chunks, embeddings)

    # guardar
    db.save_local(DB_DIR)

    print("Vectorstore creado y guardado exitosamente.")


if __name__ == "__main__":
    ingest()
