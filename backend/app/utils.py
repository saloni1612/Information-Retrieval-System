import os
import uuid
from pathlib import Path
from PyPDF2 import PdfReader

UPLOAD_FOLDER = Path("../uploads")

def save_pdf(file, name):
    os.makedirs("pdfs", exist_ok=True)  # Ensure the directory exists
    file_location = f"pdfs/{name}.pdf"
    with open(file_location, "wb") as f:
        f.write(file.file.read())
    return file_location


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract all text from a PDF."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text
