import os
from pypdf import PdfReader
from docx import Document

def parse_resume(file_path):
    """
    Extract text from a resume file (PDF or DOCX).
    """
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    try:
        if ext == '.pdf':
            return _extract_from_pdf(file_path)
        elif ext == '.docx':
            return _extract_from_docx(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")
    except Exception as e:
        print(f"Error parsing resume: {e}")
        return ""

def _extract_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as f:
        reader = PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text.strip()

def _extract_from_docx(file_path):
    doc = Document(file_path)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return "\n".join(text).strip()
