import io
import pdfplumber
import docx
import pandas as pd
from pathlib import Path

def ingest_pdf_bytes(bts):
    # pdfplumber expects a file-like; use BytesIO
    with pdfplumber.open(io.BytesIO(bts)) as pdf:
        pages = [p.extract_text() or '' for p in pdf.pages]
    text = '\n'.join(pages)
    if len(text.strip()) < 100:
        # PDF probablemente escaneado -> fallback minimal (no OCR here)
        return text
    return text

def ingest_docx_bytes(bts):
    # python-docx doesn't support bytes directly; write to temp file-like
    f = io.BytesIO(bts)
    doc = docx.Document(f)
    return '\n'.join([p.text for p in doc.paragraphs])

def ingest_excel_bytes(bts):
    f = io.BytesIO(bts)
    sheets = pd.read_excel(f, sheet_name=None)
    out = []
    for name, df in sheets.items():
        out.append(f"=== Hoja: {name} ===")
        out.append(df.to_csv(index=False))
    return '\n'.join(out)

def ingest_text_bytes(bts):
    try:
        return bts.decode('utf-8')
    except:
        return bts.decode('latin-1', errors='ignore')

def ingest_file(file_bytes, filename):
    suffix = Path(filename).suffix.lower()
    if suffix == '.pdf':
        return ingest_pdf_bytes(file_bytes)
    if suffix in ('.docx',):
        return ingest_docx_bytes(file_bytes)
    if suffix in ('.xls', '.xlsx'):
        return ingest_excel_bytes(file_bytes)
    # fallback plain text
    return ingest_text_bytes(file_bytes)
