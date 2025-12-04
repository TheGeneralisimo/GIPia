from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from ingest import ingest_file
from vector_store import load_or_create_index, add_to_index, search_in_index
import uvicorn

app = FastAPI(title="Chat RAG - Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar/crear índice en memoria
index, metadata = load_or_create_index()

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    # ingest_file acepta un file-like y filename
    text = ingest_file(await file.read(), file.filename)
    added = add_to_index(text, index, metadata, source=file.filename)
    return {"status": "ok", "indexed_chunks": added}

@app.post("/chat")
async def chat(payload: dict):
    prompt = payload.get("prompt", "")
    if not prompt:
        return {"response": "Error: envía 'prompt' en JSON"}
    context = search_in_index(prompt, index, metadata, k=3)
    # Respuesta simple de RAG; puedes integrar un LLM para mejor formato
    respuesta = f"Contexto recuperado:\n\n{context}\n\nRespuesta final: (ejemplo automático)"
    return {"response": respuesta}

if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)
