"""
Utility functions for applicant management.
"""
import os
from PyPDF2 import PdfReader


def extract_text_from_pdf(pdf_path):
    """
    Extract text content from PDF resume.

    Args:
        pdf_path: Path to PDF file

    Returns:
        Extracted text as string
    """
    try:
        if not os.path.exists(pdf_path):
            return "Resume file not found."

        reader = PdfReader(pdf_path)
        text = ""

        for page in reader.pages:
            text += page.extract_text() + "\n"

        return text.strip() if text.strip() else "Unable to extract text from resume."

    except Exception as e:
        return f"Error reading resume: {str(e)}"