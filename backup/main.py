# app/pipeline.py
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
    ext = os.path.splitext(path)[1].lower()
    if ext in [".pdf"]:
        return parse_pdf(path)
    elif ext in [".docx"]:
        return parse_docx(path)
    elif ext in [".jpg", ".jpeg", ".png"]:
        return parse_image(path)
    else:
        raise ValueError("Unsupported file type")

def to_json(text: str) -> dict:
    sections = split_sections(text)
    ents = extract_entities(text)

    skills = extract_skills(sections.get("skills", sections.get("technical skills", "")))
    edu = extract_education(sections.get("education", ""))
    exp = extract_experience(sections.get("experience", sections.get("work experience", "")))

    name = ents["PERSON"][0] if ents["PERSON"] else None
    location = ents["GPE"][0] if ents["GPE"] else None

    return {
        "name": name,
        "email": extract_email(text),
        "phone": extract_phone(text),
        "location": location,
        "links": extract_links(text),
        "summary": sections.get("summary", sections.get("profile", None)),
        "skills": skills,
        "experience": exp,
        "education": edu,
        "certifications": sections.get("certifications", "").splitlines()
    }