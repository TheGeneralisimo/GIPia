FROM python:3.10-slim

# Instalar dependencias del sistema (tesseract si se requiere OCR)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    poppler-utils \
    tesseract-ocr \
    tesseract-ocr-spa \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY ./backend /app/backend
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 8000
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
