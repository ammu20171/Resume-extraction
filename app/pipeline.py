import os
from parsers.pdf_parser import parse_pdf
from parsers.docx_parser import parse_docx
from parsers.image_parser import parse_image
from extractors.patterns import extract_email, extract_phone, extract_links
from extractors.nlp import extract_entities
from extractors.sections import split_sections
from extractors.skills import extract_skills
from extractors.education import extract_education
from extractors.experience import extract_experience

def extract_text(path: str) -> str:
    """Extract text from file based on extension"""
    ext = os.path.splitext(path)[1].lower()
    
    if ext == ".pdf":
        return parse_pdf(path)
    elif ext in [".docx", ".doc"]:
        return parse_docx(path)
    elif ext in [".jpg", ".jpeg", ".png", ".tiff", ".bmp"]:
        return parse_image(path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def to_json(text: str) -> dict:
    """Convert extracted text to structured JSON"""
    # Split into sections
    sections = split_sections(text)
    
    # Extract entities
    ents = extract_entities(text)
    
    # Extract skills
    skills_text = sections.get("skills", sections.get("technical skills", ""))
    skills = extract_skills(skills_text)
    
    # Extract education
    edu_text = sections.get("education", sections.get("academic", ""))
    education = extract_education(edu_text)
    
    # Extract experience
    exp_text = sections.get("experience", sections.get("work experience", ""))
    experience = extract_experience(exp_text)
    
    # Get summary
    summary = sections.get("summary", sections.get("objective", sections.get("profile", None)))
    
    # Extract basic info
    name = ents["PERSON"][0] if ents["PERSON"] else None
    location = ents["GPE"][0] if ents["GPE"] else None
    
    # Extract certifications
    cert_text = sections.get("certifications", sections.get("certificates", ""))
    certifications = [c.strip() for c in cert_text.splitlines() if c.strip()] if cert_text else []
    
    return {
        "name": name,
        "email": extract_email(text),
        "phone": extract_phone(text),
        "location": location,
        "links": extract_links(text),
        "summary": summary,
        "skills": skills,
        "experience": experience,
        "education": education,
        "certifications": certifications
    }
