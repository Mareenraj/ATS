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


def analyze_cv_with_gemini(resume_text, job_description, job_title, job_requirements):
    """
    Use Gemini AI to analyze CV relevance to job description.

    Args:
        resume_text: Extracted text from applicant's resume
        job_description: Job description text
        job_title: Title of the job
        job_requirements: Required qualifications for the job

    Returns:
        Dictionary with analysis results or error message
    """
    try:
        import google.generativeai as genai

        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            return {"error": "Gemini API key not configured"}

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')

        prompt = f"""You are an expert HR recruiter assistant. Analyze the following candidate's resume against the job requirements and provide a detailed assessment.

**Job Title:** {job_title}

**Job Description:**
{job_description}

**Job Requirements:**
{job_requirements}

**Candidate's Resume:**
{resume_text}

Please provide your analysis in the following format:

1. **Match Score:** (Give a percentage from 0-100% indicating how well the candidate matches the job requirements)

2. **Key Matching Skills:** (List the skills from the resume that match the job requirements)

3. **Missing Skills/Gaps:** (List any required skills or qualifications that are missing from the resume)

4. **Experience Relevance:** (Assess how relevant the candidate's experience is to this role)

5. **Overall Recommendation:** (Provide a brief recommendation: Strong Match, Good Match, Partial Match, or Poor Match, with a one-line explanation)

Be concise but thorough in your analysis."""

        response = model.generate_content(prompt)

        # Clean up markdown formatting (remove asterisks)
        clean_text = response.text.replace('**', '').replace('*', '•')

        return {
            "success": True,
            "analysis": clean_text
        }

    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower():
            return {"error": "Rate limit exceeded. Please wait 30 seconds and try again."}
        return {"error": f"AI analysis failed: {error_msg[:200]}"}
