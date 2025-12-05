from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

app = FastAPI(title="Chat RAG Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------- Cargar VectorStore FAISS --------
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Cargar FAISS desde la carpeta db/
db = FAISS.load_local(
    "db",
    embeddings,
    allow_dangerous_deserialization=True
)

@app.get("/ping")
def ping():
    return {"status": "ok"}

@app.post("/chat")
async def chat(payload: dict):
    query = payload.get("prompt", "")
    if not query:
        return {"response": "Error: falta 'prompt' en JSON"}

    docs = db.similarity_search(query, k=3)
    context = "\n---\n".join([d.page_content for d in docs])

    return {
        "response": context
    }

# Motor de arranque para Render
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
