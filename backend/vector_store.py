from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import math

model = SentenceTransformer('all-MiniLM-L6-v2')

DIM = 384  # dimension for all-MiniLM-L6-v2

def load_or_create_index():
    index = faiss.IndexFlatL2(DIM)
    metadata = []  # list of dicts: {text, source}
    return index, metadata

def chunk_text(text, max_words=200):
    parts = []
    current = ''
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue
        if len((current + ' ' + line).split()) > max_words:
            parts.append(current.strip())
            current = line
        else:
            current = (current + ' ' + line).strip()
    if current:
        parts.append(current)
    return parts

def add_to_index(text, index, metadata, source='unknown'):
    chunks = chunk_text(text)
    if not chunks:
        return 0
    embeddings = model.encode(chunks, convert_to_numpy=True).astype('float32')
    index.add(embeddings)
    for c in chunks:
        metadata.append({'text': c, 'source': source})
    return len(chunks)

def search_in_index(query, index, metadata, k=3):
    if index.ntotal == 0:
        return "(Índice vacío)"
    q = model.encode([query]).astype('float32')
    D, I = index.search(q, k)
    results = []
    for idx in I[0]:
        if idx < len(metadata):
            m = metadata[idx]
            results.append(f"Fuente: {m.get('source')} - Texto: {m.get('text')[:400]}")
    return '\n\n'.join(results)
