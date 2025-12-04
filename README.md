# Chat RAG - Proyecto prototipo

Proyecto mínimo para un chat en línea que ingesta documentos (PDF, Word, Excel), los vectoriza con SentenceTransformers y responde usando búsqueda basada en FAISS (RAG básico).

## Estructura
- backend/: FastAPI (endpoints /upload y /chat)
- frontend/: HTML + JS simple (subida y chat)
- Dockerfile: imagen lista para desplegar (incluye tesseract)
- requirements.txt: dependencias Python

## Requisitos locales
- Python 3.10+
- (Opcional) Tesseract instalado si necesitas OCR (la imagen Docker ya lo incluye)

## Ejecutar en local (modo desarrollo)
1. Crear entorno virtual y activar
    ```bash
    python -m venv venv
    source venv/bin/activate  # o venv\Scripts\activate en Windows
    pip install -r requirements.txt
    ```
2. Ejecutar backend (desde la carpeta raíz del proyecto):
    ```bash
    cd backend
    uvicorn app:app --reload --host 0.0.0.0 --port 8000
    ```
3. Abrir frontend/index.html en tu navegador (o servirlo con un static server)

## Despliegue en Render (opción gratuita / bajo costo)
Opción A - Deploy con Docker (recomendado si necesitas tesseract):
1. Subir repo a GitHub.
2. Crear un nuevo servicio en Render -> "Web Service" -> conectar repo.
3. Seleccionar "Docker" como método de despliegue.
4. Render construirá la imagen usando el Dockerfile y expondrá la URL pública.
5. Actualiza `frontend/app.js` reemplazando `<REPLACE_WITH_BACKEND_URL>` por la URL pública del backend.

Opción B - Deploy sin Docker (rápido):
1. Subir repo a GitHub.
2. Crear servicio "Web Service" en Render y seleccionar Python.
3. Configurar build command: `pip install -r requirements.txt`
4. Start command: `uvicorn backend.app:app --host 0.0.0.0 --port 8000`
5. Nota: si usas OCR (pytesseract/pdf2image), el entorno gestionado puede no tener tesseract instalado; usa Docker para garantizarlo.

## Notas importantes
- FAISS es local en memoria: para producción usa una vector DB persistente (Weaviate, Milvus, Pinecone).
- Este prototipo no implementa autenticación ni control de acceso; si vas a exponer datos sensibles, añade autenticación y HTTPS (Render ya provee HTTPS).
- Si el volumen de documentos es grande, considera pasar el procesamiento a un worker o usar almacenamiento persistente.

## ¿Quieres que genere un ZIP listo para descargar e instrucciones paso a paso para desplegar en Render?

Sí: ya está incluido: descarga el ZIP y procede con los pasos del README.
