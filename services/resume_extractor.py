
import os
from pypdf import PdfReader
from docx import Document


def extract_text(file_path):

    extension = os.path.splitext(file_path)[1].lower()

    text = ""

    # Extract text from PDF
    if extension == ".pdf":

        reader = PdfReader(file_path)

        for page in reader.pages:
            text += page.extract_text() or ""

    # Extract text from DOCX
    elif extension == ".docx":

        document = Document(file_path)

        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"

    else:
        raise ValueError("Unsupported file format")

    return text
